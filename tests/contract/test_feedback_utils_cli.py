"""Contract test: feedback-utils.py engine CLI.

Enforces the CLI contract ``contracts/feedback-utils-cli.md`` for Feature 028.

Covers actions record/status/list/mark-submitted/reindex, exit code 2 on
bad ``--unit-id``, empty ``--review``, empty ``--points``; JSON output shapes;
duplicate ``(unit_id, run_id)`` returns ``duplicate:true`` without incrementing
count.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.script_api import feedback_utils


@pytest.mark.contract
class TestRecordAction:
    def test_record_writes_entry_and_returns_json(self, feedback_store: Path):
        rc = feedback_utils.main([
            "--action", "record", "--workspace-root", str(feedback_store),
            "--unit-id", "/speckit.plan", "--unit-type", "command",
            "--run-id", "test-run-001",
            "--review", "Reviewed my run against plan purpose.",
            "--points", "Improve validation step\nAdd error logging",
        ])
        assert rc == 0

    def test_record_json_output_shape(self, feedback_store: Path, capsys):
        feedback_utils.main([
            "--action", "record", "--workspace-root", str(feedback_store),
            "--unit-id", "skill:analysis-project", "--unit-type", "skill",
            "--run-id", "run-shape-test",
            "--review", "Review text.",
            "--points", "Point one",
        ])
        out = json.loads(capsys.readouterr().out)
        assert set(out.keys()) >= {"id", "path", "duplicate", "count_since_submission", "threshold", "should_prompt"}
        assert out["duplicate"] is False
        assert isinstance(out["count_since_submission"], int)
        assert isinstance(out["threshold"], int)
        assert isinstance(out["should_prompt"], bool)

    def test_record_exit_code_2_on_bad_unit_id(self, feedback_store: Path, capsys):
        rc = feedback_utils.main([
            "--action", "record", "--workspace-root", str(feedback_store),
            "--unit-id", "invalid-source", "--unit-type", "skill",
            "--run-id", "x", "--review", "r", "--points", "p",
        ])
        assert rc == 2
        assert "Invalid --unit-id" in capsys.readouterr().err

    def test_record_exit_code_2_on_empty_review(self, feedback_store: Path, capsys):
        rc = feedback_utils.main([
            "--action", "record", "--workspace-root", str(feedback_store),
            "--unit-id", "/speckit.plan", "--unit-type", "command",
            "--run-id", "x", "--review", "", "--points", "p",
        ])
        assert rc == 2
        assert "review" in capsys.readouterr().err.lower()

    def test_record_exit_code_2_on_empty_points(self, feedback_store: Path, capsys):
        rc = feedback_utils.main([
            "--action", "record", "--workspace-root", str(feedback_store),
            "--unit-id", "/speckit.plan", "--unit-type", "command",
            "--run-id", "x", "--review", "some review", "--points", "",
        ])
        assert rc == 2
        assert "points" in capsys.readouterr().err.lower()

    def test_duplicate_unit_run_returns_duplicate_true(self, feedback_store: Path, capsys):
        for _ in range(2):
            capsys.readouterr()
            feedback_utils.main([
                "--action", "record", "--workspace-root", str(feedback_store),
                "--unit-id", "/speckit.tasks", "--unit-type", "command",
                "--run-id", "dup-run-001",
                "--review", "First review.", "--points", "Point A",
            ])
        out = json.loads(capsys.readouterr().out)
        assert out["duplicate"] is True

    def test_duplicate_does_not_increment_count(self, feedback_store: Path, capsys):
        # First call
        capsys.readouterr()
        feedback_utils.main([
            "--action", "record", "--workspace-root", str(feedback_store),
            "--unit-id", "skill:draw-echarts", "--unit-type", "skill",
            "--run-id", "dup-count-run",
            "--review", "Good run.", "--points", "One point",
        ])
        first = json.loads(capsys.readouterr().out)
        count_after_first = first["count_since_submission"]

        # Second call (duplicate)
        capsys.readouterr()
        feedback_utils.main([
            "--action", "record", "--workspace-root", str(feedback_store),
            "--unit-id", "skill:draw-echarts", "--unit-type", "skill",
            "--run-id", "dup-count-run",
            "--review", "Good run.", "--points", "One point",
        ])
        second = json.loads(capsys.readouterr().out)
        assert second["count_since_submission"] == count_after_first


@pytest.mark.contract
class TestStatusAction:
    def test_status_json_output_shape(self, feedback_store: Path, capsys):
        feedback_utils.main([
            "--action", "status", "--workspace-root", str(feedback_store),
        ])
        out = json.loads(capsys.readouterr().out)
        assert set(out.keys()) >= {
            "count_since_submission", "threshold", "should_prompt",
            "total_entries", "submitted_at",
        }
        assert out["should_prompt"] == (out["count_since_submission"] >= out["threshold"])


@pytest.mark.contract
class TestListAction:
    def test_list_json_returns_matches(self, feedback_store: Path, capsys):
        feedback_utils.main([
            "--action", "record", "--workspace-root", str(feedback_store),
            "--unit-id", "skill:browser-utils", "--unit-type", "skill",
            "--run-id", "list-test-run", "--review", "R", "--points", "P",
        ])
        capsys.readouterr()
        feedback_utils.main([
            "--action", "list", "--workspace-root", str(feedback_store),
            "--format", "json",
        ])
        out = json.loads(capsys.readouterr().out)
        assert "matches" in out and "count" in out
        assert out["count"] >= 1


@pytest.mark.contract
class TestMarkSubmittedAction:
    def test_mark_submitted_output_shape(self, feedback_store: Path, capsys):
        feedback_utils.main([
            "--action", "mark-submitted", "--workspace-root", str(feedback_store),
        ])
        out = json.loads(capsys.readouterr().out)
        assert set(out.keys()) >= {"submitted_at", "reset_from"}
        assert isinstance(out["reset_from"], int)


@pytest.mark.contract
class TestReindexAction:
    def test_reindex_output_shape(self, feedback_store: Path, capsys):
        feedback_utils.main([
            "--action", "reindex", "--workspace-root", str(feedback_store),
        ])
        out = json.loads(capsys.readouterr().out)
        assert "reindexed" in out
        assert isinstance(out["reindexed"], int)
