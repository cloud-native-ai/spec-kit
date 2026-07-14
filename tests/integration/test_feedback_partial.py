"""Integration test (US3): aborted/partial run handling (FR-009).

An aborted/failed run either records nothing or records with ``--partial`` and a
``## Review`` labeled ``**Partial run** —``.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.script_api import feedback_utils

pytestmark = pytest.mark.integration


def test_partial_run_records_labeled_review(feedback_store: Path):
    feedback_utils.main([
        "--action", "record", "--workspace-root", str(feedback_store),
        "--unit-id", "/speckit.implement", "--unit-type", "command",
        "--run-id", "aborted-run",
        "--review", "Setup phase completed before the run was interrupted.",
        "--points", "Add a resumable checkpoint after Foundational",
        "--partial",
    ])
    files = [f for f in (feedback_store / ".specify/memory/feedback").glob("*.md")]
    assert len(files) == 1
    meta, body = feedback_utils.parse_frontmatter(files[0].read_text(encoding="utf-8"))
    assert meta["partial"] is True
    review_section = body.split("## Optimization Points")[0]
    assert "**Partial run**" in review_section


def test_aborted_run_may_record_nothing(feedback_store: Path):
    # Skipping the record entirely is valid: store stays empty.
    assert not (feedback_store / ".specify/memory/feedback/index.json").exists()
    out = feedback_utils.action_status(
        feedback_utils.argparse.Namespace(workspace_root=str(feedback_store), threshold=None)
    )
    assert out["total_entries"] == 0


def test_partial_flag_still_counts_toward_threshold(feedback_store: Path, capsys):
    capsys.readouterr()
    feedback_utils.main([
        "--action", "record", "--workspace-root", str(feedback_store),
        "--unit-id", "skill:browser-utils", "--unit-type", "skill",
        "--run-id", "partial-count", "--review", "Partial.", "--points", "P",
        "--partial",
    ])
    out = json.loads(capsys.readouterr().out)
    assert out["duplicate"] is False
    assert out["count_since_submission"] == 1
