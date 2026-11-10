"""Anchor layout migration — detect, apply, refuse and stay idempotent (read/write over a fixture project)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "python" / "anchor-layout-migrate.py"

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


def test_an_existing_target_is_refused_not_overwritten(tmp_path):
    project = _legacy_project(tmp_path)
    (project / ".specify" / "features.md").write_text("# current policy\n", encoding="utf-8")
    check = _run("--action", "check", "--json", "--workspace", str(project), cwd=tmp_path)
    steps = json.loads(check.stdout)["steps"]
    refused = [s for s in steps if s["kind"] == "refuse-existing-target"]
    assert refused, steps
    _run("--action", "apply", "--workspace", str(project), cwd=tmp_path)
    assert (project / ".specify" / "features.md").read_text(encoding="utf-8") == "# current policy\n"
    assert (project / ".specify" / "memory" / "features.md").is_file(), (
        "the legacy file must survive a refused move (archive-not-delete)"
    )


def test_the_interface_answers_without_acting(tmp_path):
    help_run = _run("--help", cwd=tmp_path)
    assert help_run.returncode == 0 and "--action" in help_run.stdout
    version = _run("--version", cwd=tmp_path)
    assert version.returncode == 0 and "anchor-layout-migrate.py" in version.stdout
