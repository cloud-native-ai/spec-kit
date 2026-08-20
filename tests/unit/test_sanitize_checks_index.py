"""Unit tests: index-consistency and broken-symlink checkers (requirement 045 / Feature 047).

Pins contracts/sanitize-detection-rules.md §2 C-6..C-9 (features / feedback /
evidence index families, bidirectional) and §3 C-10 (compat symlink set,
three failure states, delegate disposition).
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tests"))

from script_api import sanitize_utils as su  # noqa: E402

FIXTURES = ROOT / "tests" / "fixtures" / "sanitize" / "correctness"


def make_ws(tmp_path: Path) -> Path:
    (tmp_path / ".specify" / "memory" / "features").mkdir(parents=True, exist_ok=True)
    return tmp_path


# --- features family (C-6) -----------------------------------------------------------

def test_features_row_pointing_to_missing_detail(tmp_path):
    ws = make_ws(tmp_path)
    (ws / ".specify" / "memory" / "features.md").write_text(
        FIXTURES.joinpath("features-index.md").read_text(encoding="utf-8"), encoding="utf-8")
    (ws / ".specify" / "memory" / "features" / "098.md").write_text("# 098\n", encoding="utf-8")
    findings = su.check_index_consistency(ws)
    assert any("099" in f["target"] for f in findings), [f["target"] for f in findings]


def test_features_disk_file_without_index_row(tmp_path):
    ws = make_ws(tmp_path)
    (ws / ".specify" / "memory" / "features.md").write_text(
        "| ID | Name | Description | Status | Feature Details | Spec Path | Last Updated |\n"
        "|----|------|-------------|--------|------------------|-----------|--------------|\n"
        "| 098 | Existing | ok | Implemented | .specify/memory/features/098.md | - | 2026-08-01 |\n",
        encoding="utf-8")
    (ws / ".specify" / "memory" / "features" / "098.md").write_text("# 098\n", encoding="utf-8")
    (ws / ".specify" / "memory" / "features" / "077.md").write_text("# 077 orphan\n", encoding="utf-8")
    findings = su.check_index_consistency(ws)
    assert any("077" in f["target"] for f in findings)


# --- feedback family (C-7) -----------------------------------------------------------

def test_feedback_index_entry_without_file(tmp_path):
    ws = make_ws(tmp_path)
    fb = ws / ".specify" / "memory" / "feedback"
    fb.mkdir(parents=True, exist_ok=True)
    (fb / "index.json").write_text(json.dumps({
        "store": "feedback", "updated": "x", "threshold": 10, "count_since_submission": 0,
        "entries": [{"id": "e1", "file": "20260820T000000Z-unit.md"}],
    }), encoding="utf-8")
    findings = su.check_index_consistency(ws)
    assert any("feedback" in f["target"] and "e1" in f["target"] + f["summary"] for f in findings)


def test_feedback_disk_entry_without_index(tmp_path):
    ws = make_ws(tmp_path)
    fb = ws / ".specify" / "memory" / "feedback"
    fb.mkdir(parents=True, exist_ok=True)
    (fb / "index.json").write_text(json.dumps({
        "store": "feedback", "updated": "x", "threshold": 10, "count_since_submission": 0,
        "entries": [],
    }), encoding="utf-8")
    (fb / "20260820T000000Z-unit.md").write_text("# entry\n", encoding="utf-8")
    findings = su.check_index_consistency(ws)
    assert any("20260820T000000Z-unit.md" in f["target"] for f in findings)


def test_feedback_bookkeeping_files_exempt(tmp_path):
    """Store scaffolding (logs / probe-map) is not feedback entries."""
    ws = make_ws(tmp_path)
    fb = ws / ".specify" / "memory" / "feedback"
    fb.mkdir(parents=True, exist_ok=True)
    (fb / "index.json").write_text(json.dumps({
        "store": "feedback", "updated": "x", "threshold": 10, "count_since_submission": 0,
        "entries": [],
    }), encoding="utf-8")
    for name in ("cleanup-log.md", "consume-log.md", "migration-log.md",
                 "migration-plan.md", "probe-map.md"):
        (fb / name).write_text("# bookkeeping\n", encoding="utf-8")
    findings = su.check_index_consistency(ws)
    assert not any(name in f["target"] for f in findings)


# --- evidence family (C-8) -----------------------------------------------------------

def test_evidence_index_run_without_dir(tmp_path):
    ws = make_ws(tmp_path)
    ev = ws / ".specify" / "memory" / "evidence"
    ev.mkdir(parents=True, exist_ok=True)
    (ev / "index.json").write_text(json.dumps({
        "store": "evidence", "updated": "x",
        "entries": [{"runId": "ev-20260820-010000-x", "target": "project"}],
    }), encoding="utf-8")
    findings = su.check_index_consistency(ws)
    assert any("ev-20260820-010000-x" in f["target"] + f["summary"] for f in findings)


def test_evidence_dir_without_index(tmp_path):
    ws = make_ws(tmp_path)
    ev = ws / ".specify" / "memory" / "evidence"
    (ev / "ev-20260820-020000-y").mkdir(parents=True, exist_ok=True)
    (ev / "index.json").write_text(json.dumps({
        "store": "evidence", "updated": "x", "entries": []}), encoding="utf-8")
    findings = su.check_index_consistency(ws)
    assert any("ev-20260820-020000-y" in f["target"] for f in findings)


# --- unparseable index (C-9) -----------------------------------------------------------

def test_unparseable_index_is_single_finding(tmp_path):
    ws = make_ws(tmp_path)
    fb = ws / ".specify" / "memory" / "feedback"
    fb.mkdir(parents=True, exist_ok=True)
    (fb / "index.json").write_text("{corrupt", encoding="utf-8")
    findings = su.check_index_consistency(ws)
    assert len([f for f in findings if "feedback" in f["target"]]) == 1


# --- compat symlinks (C-10) -----------------------------------------------------------

def make_link(ws: Path, name: str, target: str):
    link = ws / name
    link.parent.mkdir(parents=True, exist_ok=True)
    os.symlink(target, link)


def test_missing_symlink_reported_when_tool_surface_exists(tmp_path):
    ws = make_ws(tmp_path)
    (ws / ".claude").mkdir(exist_ok=True)
    (ws / ".github").mkdir(exist_ok=True)
    (ws / ".specify" / "instructions.md").write_text("# instructions\n", encoding="utf-8")
    findings = su.check_broken_symlinks(ws)
    names = {f["target"] for f in findings}
    assert "CLAUDE.md" in names and "AGENTS.md" in names
    assert ".github/skills" in names


def test_missing_symlink_silent_without_tool_surface(tmp_path):
    """A bare workspace (no tool dirs) must not be flagged for absent links."""
    ws = make_ws(tmp_path)
    findings = su.check_broken_symlinks(ws)
    assert findings == []


def test_broken_symlink_target_reported(tmp_path):
    ws = make_ws(tmp_path)
    (ws / "real-target.md").write_text("# ok\n", encoding="utf-8")
    make_link(ws, "CLAUDE.md", "real-target.md")
    (ws / "real-target.md").unlink()  # break the link target
    findings = su.check_broken_symlinks(ws)
    assert any(f["target"] == "CLAUDE.md" for f in findings)


def test_replaced_by_regular_file_reported(tmp_path):
    ws = make_ws(tmp_path)
    make_link(ws, "CLAUDE.md", "some-target.md")
    (ws / "CLAUDE.md").unlink()
    (ws / "CLAUDE.md").write_text("not a symlink anymore\n", encoding="utf-8")
    findings = su.check_broken_symlinks(ws)
    assert any(f["target"] == "CLAUDE.md" for f in findings)


def test_intact_symlink_not_reported(tmp_path):
    ws = make_ws(tmp_path)
    (ws / "some-target.md").write_text("# ok\n", encoding="utf-8")
    make_link(ws, "CLAUDE.md", "some-target.md")
    findings = su.check_broken_symlinks(ws)
    assert not any(f["target"] == "CLAUDE.md" for f in findings)


def test_symlink_findings_delegate(tmp_path):
    ws = make_ws(tmp_path)
    (ws / ".claude").mkdir(exist_ok=True)
    findings = su.check_broken_symlinks(ws)
    assert findings
    for f in findings:
        assert f["disposition"] == "delegate"
        assert "speckit.instructions" in f["summary"]
        assert f["detection"] == "programmatic"
