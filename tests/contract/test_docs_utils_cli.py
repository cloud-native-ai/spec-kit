"""Contract test: docs-utils.py engine CLI (spec 033, Feature 037).

Driven by ``.specify/specs/033-docs-command/contracts/docs-utils-cli.md``
(C-1…C-10). The engine is stdlib-only, prints a single JSON object to stdout,
and never touches the feedback engine.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "python" / "docs-utils.py"
MIRROR = REPO_ROOT / ".specify" / "scripts" / "python" / "docs-utils.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "docs_command"

ACTIONS = {"scan", "expire", "clean", "archive-check", "stats", "validate", "audit"}


def run_engine(*args: str, cwd: Path | None = None) -> dict:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, cwd=cwd or REPO_ROOT,
    )
    assert proc.returncode == 0, f"engine failed: {proc.stderr}"
    return json.loads(proc.stdout)


@pytest.fixture()
def notes_project(tmp_path: Path) -> Path:
    dst = tmp_path / "proj"
    shutil.copytree(FIXTURES / "notes_samples", dst)
    return dst


@pytest.fixture()
def messy_project(tmp_path: Path) -> Path:
    dst = tmp_path / "proj"
    shutil.copytree(FIXTURES / "messy_project", dst)
    return dst


@pytest.mark.contract
def test_c1_script_exists_with_fixed_action_set():
    assert SCRIPT.is_file(), "scripts/python/docs-utils.py missing"
    source = SCRIPT.read_text(encoding="utf-8")
    for action in ACTIONS:
        assert f'"{action}"' in source, f"action {action} not declared"
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--action", "bogus"],
        capture_output=True, text=True,
    )
    assert proc.returncode != 0, "unknown action must be rejected"


@pytest.mark.contract
def test_c1_mirror_is_byte_identical():
    assert MIRROR.is_file(), ".specify mirror missing"
    assert SCRIPT.read_bytes() == MIRROR.read_bytes(), "mirror drift"


@pytest.mark.contract
def test_c2_scan_groups_and_invalid_suggestions(notes_project: Path):
    out = run_engine("--action", "scan", "--root", str(notes_project))
    for key in ("drafts", "expireds", "archiveds", "invalid"):
        assert key in out, f"scan output missing {key}"
    paths = lambda group: [e["path"] for e in out[group]]  # noqa: E731
    assert any("draft-note.md" in p for p in paths("drafts"))
    assert any("overdue-note.md" in p for p in paths("expireds")), \
        "overdue draft must be reported in expireds group"
    assert any("archived-ok.md" in p for p in paths("archiveds"))
    invalid = [e for e in out["invalid"] if "invalid-note.md" in e["path"]]
    assert invalid, "frontmatter-incomplete note must be reported invalid"
    assert "expires" in invalid[0]["missing"] and "status" in invalid[0]["missing"]
    # default-expiry suggestion = created + 60 days (created 2026-06-01)
    assert invalid[0]["suggestion"]["expires"] == "2026-07-31"


@pytest.mark.contract
def test_c3_expire_marks_but_never_deletes(notes_project: Path):
    out = run_engine("--action", "expire", "--root", str(notes_project))
    assert out["count"] == 1
    assert any("overdue-note.md" in p for p in out["marked"])
    overdue = notes_project / "docs" / "notes" / "overdue-note.md"
    assert overdue.exists(), "expire must not delete files"
    assert "status: expired" in overdue.read_text(encoding="utf-8")
    # idempotency: second run marks nothing
    again = run_engine("--action", "expire", "--root", str(notes_project))
    assert again["count"] == 0


@pytest.mark.contract
def test_c4_clean_dry_run_default_and_yes_gate(notes_project: Path):
    run_engine("--action", "expire", "--root", str(notes_project))
    dry = run_engine("--action", "clean", "--root", str(notes_project))
    assert dry["dry_run"] is True and dry["deleted"] == []
    assert any("overdue-note.md" in p for p in dry["candidates"])
    assert (notes_project / "docs" / "notes" / "overdue-note.md").exists()
    real = run_engine("--action", "clean", "--yes", "--root", str(notes_project))
    assert real["dry_run"] is False
    assert any("overdue-note.md" in p for p in real["deleted"])
    assert not (notes_project / "docs" / "notes" / "overdue-note.md").exists()


@pytest.mark.contract
def test_c5_archive_check_reports_broken_targets(notes_project: Path):
    out = run_engine("--action", "archive-check", "--root", str(notes_project))
    assert any("archived-ok.md" in e["path"] for e in out["ok"])
    broken = [e for e in out["broken"] if "archived-broken.md" in e["path"]]
    assert broken and broken[0]["target"] == "docs/concepts/missing.md"


@pytest.mark.contract
def test_c6_stats_counts(notes_project: Path):
    out = run_engine("--action", "stats", "--root", str(notes_project))
    assert out["total"] == 5
    assert out["drafts"] == 1        # active draft
    assert out["expireds"] == 1      # overdue draft counts as expired-pending
    assert out["archiveds"] == 2


@pytest.mark.contract
def test_c7_validate_deterministic_dimensions(messy_project: Path):
    out = run_engine("--action", "validate", "--root", str(messy_project))
    kinds = {v["kind"] for v in out["violations"]}
    assert "reserved-name-case" in kinds, "lowercase readme.md must be flagged"
    assert "reserved-name-misuse" in kinds, "DESIGN.md misuse must be flagged"
    assert "broken-link" in kinds, "broken relative link must be flagged"
    # validate is read-only
    assert (messy_project / "readme.md").exists()
    assert (messy_project / "DESIGN.md").exists()


@pytest.mark.contract
def test_c8_audit_appends_record_even_for_noop(tmp_path: Path):
    proj = tmp_path / "proj"
    proj.mkdir()
    out = run_engine(
        "--action", "audit", "--root", str(proj),
        "--scope", "full-sweep",
        "--summary", "all dimensions within tolerance",
    )
    assert out["written"] is True
    audit_file = Path(out["path"])
    if not audit_file.is_absolute():
        audit_file = proj / audit_file
    assert audit_file.is_file()
    text = audit_file.read_text(encoding="utf-8")
    assert "full-sweep" in text and "all dimensions within tolerance" in text
    assert ".specify/docs/audit" in str(audit_file).replace("\\", "/")


@pytest.mark.contract
def test_c9_exit_zero_even_with_violations(messy_project: Path):
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--action", "validate", "--root", str(messy_project)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, "violations are a normal report, not an error"


@pytest.mark.contract
def test_c10_engine_does_not_touch_feedback_machinery():
    source = SCRIPT.read_text(encoding="utf-8").lower()
    assert "feedback" not in source, "docs engine must not reference feedback machinery"
