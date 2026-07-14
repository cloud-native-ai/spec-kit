"""Integration test (US3): consolidated threshold prompt (FR-011, SC-007).

Below threshold ``should_prompt`` is false and no prompt is surfaced; at/over
threshold ``should_prompt`` is true; ``mark-submitted`` resets
``count_since_submission`` to 0 and stamps ``submitted_at``.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.script_api import feedback_utils

pytestmark = pytest.mark.integration


def _record(ws: Path, run_id: str, threshold: int, capsys):
    capsys.readouterr()
    feedback_utils.main([
        "--action", "record", "--workspace-root", str(ws),
        "--unit-id", "/speckit.plan", "--unit-type", "command",
        "--run-id", run_id, "--review", "R", "--points", "P",
        "--threshold", str(threshold),
    ])
    return json.loads(capsys.readouterr().out)


def test_below_threshold_no_prompt(feedback_store: Path, capsys):
    out = _record(feedback_store, "r1", 3, capsys)
    assert out["count_since_submission"] == 1
    assert out["should_prompt"] is False


def test_at_threshold_prompts(feedback_store: Path, capsys):
    _record(feedback_store, "r1", 3, capsys)
    _record(feedback_store, "r2", 3, capsys)
    out = _record(feedback_store, "r3", 3, capsys)
    assert out["count_since_submission"] == 3
    assert out["should_prompt"] is True


def test_mark_submitted_resets_and_stamps(feedback_store: Path, capsys):
    _record(feedback_store, "r1", 3, capsys)
    _record(feedback_store, "r2", 3, capsys)
    _record(feedback_store, "r3", 3, capsys)

    capsys.readouterr()
    feedback_utils.main([
        "--action", "mark-submitted", "--workspace-root", str(feedback_store),
    ])
    result = json.loads(capsys.readouterr().out)
    assert result["reset_from"] == 3
    assert result["submitted_at"] is not None

    index = json.loads(
        (feedback_store / ".specify/memory/feedback/index.json").read_text(encoding="utf-8")
    )
    assert index["count_since_submission"] == 0
    assert index["submitted_at"] == result["submitted_at"]

    # status now below threshold again
    capsys.readouterr()
    feedback_utils.main([
        "--action", "status", "--workspace-root", str(feedback_store),
    ])
    status = json.loads(capsys.readouterr().out)
    assert status["should_prompt"] is False
    assert status["count_since_submission"] == 0
