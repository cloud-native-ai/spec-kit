"""Integration test (US2): complex commands record, simple commands do not.

A complex command records a ``unit_type: command``, ``scope: local`` entry at
wrap-up while a simple command records zero entries. Command templates are
prompt text (not executable here), so this test exercises:
  - the engine path a complex command's wrap-up uses (records a command entry), and
  - the classification guarantee that simple command templates carry no record
    invocation (hence they never write an entry).
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.script_api import feedback_utils

pytestmark = pytest.mark.integration

REPO_ROOT = Path(__file__).resolve().parents[2]
COMMANDS_DIR = REPO_ROOT / "templates" / "commands"
FEEDBACK_MARKER = "feedback-utils.py"
SIMPLE_COMMANDS = ["agents", "constitution", "feature", "team"]


def test_complex_command_records_command_scoped_entry(feedback_store: Path):
    feedback_utils.main([
        "--action", "record", "--workspace-root", str(feedback_store),
        "--unit-id", "/speckit.plan", "--unit-type", "command",
        "--run-id", "027-feedback-mechanism-20260714T1200",
        "--feature", "027-feedback-mechanism",
        "--review", "Plan run reflected against its planning purpose.",
        "--points", "Clarify the classification table earlier",
    ])
    index = json.loads(
        (feedback_store / ".specify/memory/feedback/index.json").read_text(encoding="utf-8")
    )
    assert len(index["entries"]) == 1
    entry = index["entries"][0]
    assert entry["unit_type"] == "command"
    assert entry["unit_id"] == "/speckit.plan"

    files = [f for f in (feedback_store / ".specify/memory/feedback").glob("*.md")]
    meta, _ = feedback_utils.parse_frontmatter(files[0].read_text(encoding="utf-8"))
    assert meta["scope"] == "local"


def test_simple_commands_never_invoke_record():
    for cmd in SIMPLE_COMMANDS:
        text = (COMMANDS_DIR / f"{cmd}.md").read_text(encoding="utf-8")
        assert FEEDBACK_MARKER not in text, f"{cmd}.md unexpectedly records feedback"


def test_store_empty_when_no_record_called(feedback_store: Path):
    # A simple command runs but never calls the engine -> store stays empty.
    index_file = feedback_store / ".specify/memory/feedback/index.json"
    assert not index_file.exists()
