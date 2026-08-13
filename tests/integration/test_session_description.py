"""Integration tests for the session description document (039-session-export, T013).

Contract: .specify/specs/039-session-export/contracts/session-description.contract.md

Fixture-driven black-box runs (synthetic HOME, claude-code storage shape):
the deterministic meta half is asserted field by field, the budget verdict
on both sides of the frozen thresholds, the SESSION.md structure, and the
meta.json ↔ SESSION.md field consistency.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "skills/archive-session/scripts/export.py"

pytestmark = pytest.mark.integration

SID = "bbbbcccc-1111-4222-8333-aaaabbbbcccc"


def _write_session(home: Path, project: Path, records: list[dict]) -> Path:
    proj_dir = home / ".claude" / "projects" / "-fake"
    proj_dir.mkdir(parents=True, exist_ok=True)
    path = proj_dir / f"{SID}.jsonl"
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n",
                    encoding="utf-8")
    return path


def _base_records(project: Path) -> list[dict]:
    return [
        {"cwd": str(project), "type": "user", "timestamp": "2026-08-12T01:00:00.000Z",
         "message": {"role": "user", "content": "探针甲 rhododendron-7"}},
        {"cwd": str(project), "type": "assistant", "timestamp": "2026-08-12T01:05:00.000Z",
         "message": {"role": "assistant", "model": "fixture-model-x", "content": "ok"}},
        {"cwd": str(project), "type": "user", "timestamp": "2026-08-12T01:09:00.000Z",
         "message": {"role": "user", "content": "探针乙"}},
    ]


@pytest.fixture()
def env(tmp_path):
    home = tmp_path / "home"
    project = tmp_path / "proj"
    project.mkdir()
    _write_session(home, project, _base_records(project))
    return home, project


def run_cli(home: Path, project: Path, *args: str) -> subprocess.CompletedProcess:
    environ = {**os.environ, "HOME": str(home)}
    return subprocess.run(
        [sys.executable, str(ENGINE), "--project", str(project), *args],
        capture_output=True, text=True, env=environ, cwd=str(project),
    )


def bundle(project: Path, name: str) -> Path:
    return project / ".session-export" / name


# --------------------------------------------------------------------------
# §2 deterministic meta fields
# --------------------------------------------------------------------------

def test_meta_fields_match_the_records(env):
    home, project = env
    result = run_cli(home, project, "--name", "meta-check", "--tool", "claude-code")
    assert result.returncode == 0, result.stderr
    meta = json.loads((bundle(project, "meta-check") / "session-meta.json")
                      .read_text(encoding="utf-8"))
    assert meta["tool"] == "claude-code"
    assert meta["session_id"] == SID
    assert meta["model"] == "fixture-model-x"
    assert meta["workspace"] == str(project)
    assert meta["started_at"].startswith("2026-08-12T01:00:00")
    assert meta["ended_at"].startswith("2026-08-12T01:09:00")
    assert meta["message_count"] == 3
    assert meta["turn_count"] == 3
    assert meta["exported_at"]
    assert meta["over_summary_budget"] is False
    # freshly written fixture → still active within the snapshot window
    assert meta["snapshot"] is True


# --------------------------------------------------------------------------
# §4 budget verdict, both sides
# --------------------------------------------------------------------------

def test_over_budget_verdict_true_beyond_line_limit(env, tmp_path):
    home, project = env
    big = [{"cwd": str(project), "type": "user", "message": {"role": "user", "content": "x"}}
           for _ in range(50_001)]
    _write_session(home, project, big)
    result = run_cli(home, project, "--name", "big-check", "--tool", "claude-code")
    assert result.returncode == 0, result.stderr
    meta = json.loads((bundle(project, "big-check") / "session-meta.json")
                      .read_text(encoding="utf-8"))
    assert meta["over_summary_budget"] is True, "50,001 lines exceeds the line limit"


def test_within_budget_verdict_false(env):
    home, project = env
    result = run_cli(home, project, "--name", "small-check", "--tool", "claude-code")
    assert result.returncode == 0, result.stderr
    meta = json.loads((bundle(project, "small-check") / "session-meta.json")
                      .read_text(encoding="utf-8"))
    assert meta["over_summary_budget"] is False


# --------------------------------------------------------------------------
# §1/§2 SESSION.md structure and two-form consistency
# --------------------------------------------------------------------------

def test_session_md_structure(env):
    home, project = env
    result = run_cli(home, project, "--name", "doc-check", "--tool", "claude-code")
    assert result.returncode == 0, result.stderr
    text = (bundle(project, "doc-check") / "SESSION.md").read_text(encoding="utf-8")
    assert text.startswith("# Session Description")
    assert f"session-export:claude-code/{SID}" in text, "STR-003 identifier line"
    assert "## 元信息" in text
    assert "## 结构化总结" in text
    assert "agent 补写" in text, "the summary section stays a placeholder until filled"


def test_meta_json_and_session_md_are_field_consistent(env):
    home, project = env
    result = run_cli(home, project, "--name", "consistency", "--tool", "claude-code")
    assert result.returncode == 0, result.stderr
    b = bundle(project, "consistency")
    meta = json.loads((b / "session-meta.json").read_text(encoding="utf-8"))
    text = (b / "SESSION.md").read_text(encoding="utf-8")
    for key in ("tool", "session_id", "workspace", "message_count", "turn_count"):
        assert str(meta[key]) in text, f"meta field {key} missing from SESSION.md"
    assert "fixture-model-x" in text
