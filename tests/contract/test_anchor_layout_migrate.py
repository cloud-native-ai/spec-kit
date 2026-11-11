"""Anchor layout migration — detect, apply, merge, refuse and stay idempotent (read/write over a fixture project)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "python" / "anchor-layout-migrate.py"
PLACEHOLDER_DIR = REPO_ROOT / "memory"

ANCHORS = ("features.md", "constitution.md", "glossary.md", "register.md", "tools.md")


def _run(*args, cwd):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args], cwd=str(cwd), capture_output=True, text=True
    )


def _legacy_project(tmp_path: Path) -> Path:
    project = tmp_path / "project"
    specify = project / ".specify"
    memory = specify / "memory"
    (memory / "features").mkdir(parents=True)
    for anchor in ANCHORS:
        (memory / anchor).write_text("# %s\n" % anchor, encoding="utf-8")
    (memory / "features.md").write_text(
        "# features.md\n\n| 041 | Foo Bar | desc | Planned | .specify/features/041.md | .specify/specs/041-foo-bar/requirements.md | when |\n",
        encoding="utf-8",
    )
    (memory / "features" / "041.md").write_text("# 041 — Foo Bar\n", encoding="utf-8")
    (memory / "features" / "042.md").write_text("# 042 — Content Derived\n", encoding="utf-8")
    return project


def test_check_reports_the_plan_and_apply_converges(tmp_path):
    project = _legacy_project(tmp_path)
    check = _run("--action", "check", "--json", "--workspace", str(project), cwd=tmp_path)
    assert check.returncode == 1, check.stderr
    plan = json.loads(check.stdout)
    targets = [step["to"] for step in plan["steps"]]
    assert any(t.endswith("/.specify/features.md") for t in targets)
    assert any(t.endswith("/.specify/tools.md") for t in targets)
    assert any(t.endswith("/.specify/features/041-foo-bar.md") for t in targets), targets
    assert any(t.endswith("/.specify/features/042-content-derived.md") for t in targets), targets

    applied = _run("--action", "apply", "--json", "--workspace", str(project), cwd=tmp_path)
    assert applied.returncode == 0, applied.stderr
    specify = project / ".specify"
    for anchor in ANCHORS:
        assert (specify / anchor).is_file(), anchor
        assert not (specify / "memory" / anchor).exists(), anchor
    assert (specify / "features" / "041-foo-bar.md").is_file()
    assert (specify / "features" / "042-content-derived.md").is_file()

    clean = _run("--action", "check", "--json", "--workspace", str(project), cwd=tmp_path)
    assert clean.returncode == 0, clean.stdout
    assert json.loads(clean.stdout)["clean"] is True

    second = _run("--action", "apply", "--json", "--workspace", str(project), cwd=tmp_path)
    assert second.returncode == 0
    assert json.loads(second.stdout)["applied"] == []


def test_an_existing_real_target_is_merged_not_overwritten(tmp_path):
    project = _legacy_project(tmp_path)
    target = project / ".specify" / "features.md"
    target.write_text("# current policy\n", encoding="utf-8")

    check = _run("--action", "check", "--json", "--workspace", str(project), cwd=tmp_path)
    steps = json.loads(check.stdout)["steps"]
    merges = [step for step in steps if step["kind"] == "merge"]
    assert merges, steps

    applied = _run("--action", "apply", "--json", "--workspace", str(project), cwd=tmp_path)
    assert applied.returncode == 0, applied.stderr
    merged = target.read_text(encoding="utf-8")
    assert "# current policy" in merged
    assert "| 041 | Foo Bar |" in merged
    assert "specify-migrate: legacy anchor" in merged
    assert not (project / ".specify" / "memory" / "features.md").exists()

    archive_root = next(
        (project / ".specify" / "archive" / "anchor-layout").iterdir()
    )
    assert (archive_root / "memory" / "features.md").is_file()
    assert (archive_root / "features.md").is_file()


def test_a_placeholder_target_is_replaced_by_real_legacy_content(tmp_path):
    project = tmp_path / "project"
    specify = project / ".specify"
    memory = specify / "memory"
    memory.mkdir(parents=True)
    legacy = memory / "constitution.md"
    legacy.write_text("# Real constitution\n\nReal principle.\n", encoding="utf-8")
    placeholder = specify / "constitution.md"
    placeholder.write_text(
        "This file is a placeholder for the project constitution. It should be "
        "replaced with actual content during development.\n\n"
        "use `/speckit.constitution` command line to fill content.\n",
        encoding="utf-8",
    )

    check = _run(
        "--action", "check", "--json", "--workspace", str(project),
        "--placeholder-dir", str(PLACEHOLDER_DIR), cwd=tmp_path,
    )
    steps = json.loads(check.stdout)["steps"]
    assert [step["kind"] for step in steps] == ["placeholder-replace"], steps

    applied = _run(
        "--action", "apply", "--json", "--workspace", str(project),
        "--placeholder-dir", str(PLACEHOLDER_DIR), cwd=tmp_path,
    )
    assert applied.returncode == 0, applied.stderr
    assert placeholder.read_text(encoding="utf-8") == "# Real constitution\n\nReal principle.\n"
    assert not legacy.exists()


def test_two_real_feature_registries_are_unioned_by_id(tmp_path):
    project = tmp_path / "project"
    specify = project / ".specify"
    memory = specify / "memory"
    memory.mkdir(parents=True)
    (specify / "features.md").write_text(
        "# Current\n\n**Last Updated**: 2026-02-01\n**Total Features**: 2\n\n"
        "| ID | Name |\n|----|------|\n| 001 | Current-one |\n| 002 | Current-two |\n",
        encoding="utf-8",
    )
    (memory / "features.md").write_text(
        "# Legacy\n\n**Last Updated**: 2026-03-01\n**Total Features**: 2\n\n"
        "| ID | Name |\n|----|------|\n| 001 | Legacy-one |\n| 003 | Legacy-three |\n",
        encoding="utf-8",
    )

    applied = _run("--action", "apply", "--json", "--workspace", str(project), cwd=tmp_path)
    assert applied.returncode == 0, applied.stderr
    merged = (specify / "features.md").read_text(encoding="utf-8")
    assert "Current-one" in merged and "Current-two" in merged
    assert "Legacy-three" in merged, "the legacy-only row was dropped"
    assert "Legacy-one" not in merged, "a duplicate legacy row must not be appended"
    assert "**Total Features**: 3" in merged
    assert "**Last Updated**: 2026-03-01" in merged


def test_an_unmergeable_structural_target_is_refused(tmp_path):
    project = _legacy_project(tmp_path)
    target = project / ".specify" / "features.md"
    target.mkdir()
    (target / "keep.txt").write_text("user content\n", encoding="utf-8")

    check = _run("--action", "check", "--json", "--workspace", str(project), cwd=tmp_path)
    steps = json.loads(check.stdout)["steps"]
    refused = [step for step in steps if step["kind"] == "refuse-existing-target"]
    assert refused, steps

    _run("--action", "apply", "--workspace", str(project), cwd=tmp_path)
    assert (target / "keep.txt").read_text(encoding="utf-8") == "user content\n"
    assert (project / ".specify" / "memory" / "features.md").is_file(), (
        "the legacy file must survive a refused merge"
    )


def test_the_interface_answers_without_acting(tmp_path):
    help_run = _run("--help", cwd=tmp_path)
    assert help_run.returncode == 0 and "--action" in help_run.stdout
    version = _run("--version", cwd=tmp_path)
    assert version.returncode == 0 and "anchor-layout-migrate.py" in version.stdout
