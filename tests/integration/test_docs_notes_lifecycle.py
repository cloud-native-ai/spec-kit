"""Integration tests: notes lifecycle end-to-end (spec 033 US2, SC-003).

Exercises the three exit paths (merge/archive, renew, confirmed delete) plus
overdue naming, on a mutable copy of the notes_samples fixture.
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
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "docs_command"


def run_engine(*args: str) -> dict:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *args], capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


@pytest.fixture()
def proj(tmp_path: Path) -> Path:
    dst = tmp_path / "proj"
    shutil.copytree(FIXTURES / "notes_samples", dst)
    return dst


@pytest.mark.integration
def test_overdue_notes_are_always_named(proj: Path):
    out = run_engine("--action", "scan", "--root", str(proj))
    assert any("overdue-note.md" in e["path"] for e in out["expireds"]), \
        "100% of overdue notes must appear in the pending list"


@pytest.mark.integration
def test_exit_path_archive_with_target_integrity(proj: Path):
    out = run_engine("--action", "archive-check", "--root", str(proj))
    assert any("archived-ok.md" in e["path"] for e in out["ok"])
    assert any("archived-broken.md" in e["path"] for e in out["broken"])


@pytest.mark.integration
def test_exit_path_renew_returns_to_draft(proj: Path):
    run_engine("--action", "expire", "--root", str(proj))
    note = proj / "docs" / "notes" / "overdue-note.md"
    text = note.read_text(encoding="utf-8")
    text = text.replace("status: expired", "status: draft")
    text = text.replace("expires: 2020-03-01", "expires: 2099-12-31")
    note.write_text(text, encoding="utf-8")
    out = run_engine("--action", "scan", "--root", str(proj))
    assert any("overdue-note.md" in e["path"] for e in out["drafts"]), \
        "renewed note must classify as active draft again"
    again = run_engine("--action", "expire", "--root", str(proj))
    assert again["count"] == 0


@pytest.mark.integration
def test_exit_path_confirmed_delete_only_after_yes(proj: Path):
    run_engine("--action", "expire", "--root", str(proj))
    note = proj / "docs" / "notes" / "overdue-note.md"
    dry = run_engine("--action", "clean", "--root", str(proj))
    assert dry["dry_run"] is True and note.exists(), "no deletion without confirmation"
    run_engine("--action", "clean", "--yes", "--root", str(proj))
    assert not note.exists()
    # deletion is scoped to the notes zone: formal-zone file untouched
    assert (proj / "docs" / "concepts" / "caching.md").exists()
