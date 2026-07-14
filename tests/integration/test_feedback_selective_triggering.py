"""Integration test (US3): selective triggering (FR-007, SC-002, SC-004).

Trivial/short flows and simple commands produce zero entries; a qualifying flow
produces exactly one. Trigger policy is encoded by convention: simple command
templates carry no record invocation, so they never write. A qualifying unit
records exactly once per run.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.script_api import feedback_utils

pytestmark = pytest.mark.integration

REPO_ROOT = Path(__file__).resolve().parents[2]
COMMANDS_DIR = REPO_ROOT / "templates" / "commands"
SIMPLE_COMMANDS = ["agents", "constitution", "feature", "team"]
FEEDBACK_MARKER = "feedback-utils.py"


def test_trivial_flow_records_nothing(feedback_store: Path):
    # No record invoked -> the store index is never created.
    assert not (feedback_store / ".specify/memory/feedback/index.json").exists()
    status_ws = feedback_store
    out = feedback_utils.action_status(
        feedback_utils.argparse.Namespace(workspace_root=str(status_ws), threshold=None)
    )
    assert out["total_entries"] == 0
    assert out["count_since_submission"] == 0


def test_simple_commands_carry_no_trigger():
    for cmd in SIMPLE_COMMANDS:
        text = (COMMANDS_DIR / f"{cmd}.md").read_text(encoding="utf-8")
        assert FEEDBACK_MARKER not in text


def test_qualifying_flow_records_exactly_one(feedback_store: Path, capsys):
    capsys.readouterr()
    feedback_utils.main([
        "--action", "record", "--workspace-root", str(feedback_store),
        "--unit-id", "skill:draw-echarts", "--unit-type", "skill",
        "--run-id", "one-shot", "--review", "R", "--points", "P",
    ])
    index = json.loads(
        (feedback_store / ".specify/memory/feedback/index.json").read_text(encoding="utf-8")
    )
    assert index["count_since_submission"] == 1
    assert len(index["entries"]) == 1
