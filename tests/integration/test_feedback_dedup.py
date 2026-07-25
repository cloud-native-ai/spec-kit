"""Integration test (US3): per-run dedup (FR-008, SC-005).

A second ``record`` for the same ``(unit_id, run_id)`` returns ``duplicate:true``
and leaves ``count_since_submission`` unchanged.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.script_api import feedback_utils

pytestmark = pytest.mark.integration


def _record(ws: Path, unit_id: str, run_id: str, capsys):
    capsys.readouterr()
    feedback_utils.main([
        "--action", "record", "--workspace-root", str(ws),
        "--unit-id", unit_id, "--unit-type", "skill",
        "--run-id", run_id, "--review", "R", "--points", "P",
    ])
    return json.loads(capsys.readouterr().out)


def test_second_record_same_unit_run_is_duplicate(feedback_store: Path, capsys):
    first = _record(feedback_store, "skill:study-project", "nested-run", capsys)
    assert first["duplicate"] is False
    assert first["count_since_submission"] == 1

    second = _record(feedback_store, "skill:study-project", "nested-run", capsys)
    assert second["duplicate"] is True
    assert second["count_since_submission"] == 1  # unchanged

    # Only one entry file on disk
    files = [f for f in (feedback_store / ".specify/memory/feedback").glob("*.md")]
    assert len(files) == 1


def test_nested_command_then_skill_same_run_not_double_counted(feedback_store: Path, capsys):
    # command records once
    capsys.readouterr()
    feedback_utils.main([
        "--action", "record", "--workspace-root", str(feedback_store),
        "--unit-id", "/speckit.plan", "--unit-type", "command",
        "--run-id", "shared-run", "--review", "R", "--points", "P",
    ])
    # a distinct nested skill unit with its OWN unit_id records separately (own scope)
    capsys.readouterr()
    feedback_utils.main([
        "--action", "record", "--workspace-root", str(feedback_store),
        "--unit-id", "skill:study-project", "--unit-type", "skill",
        "--run-id", "shared-run", "--review", "R", "--points", "P",
    ])
    out = json.loads(capsys.readouterr().out)
    assert out["count_since_submission"] == 2  # distinct units, each once

    # re-recording the command for the same run is a no-op
    capsys.readouterr()
    feedback_utils.main([
        "--action", "record", "--workspace-root", str(feedback_store),
        "--unit-id", "/speckit.plan", "--unit-type", "command",
        "--run-id", "shared-run", "--review", "R", "--points", "P",
    ])
    dup = json.loads(capsys.readouterr().out)
    assert dup["duplicate"] is True
    assert dup["count_since_submission"] == 2
