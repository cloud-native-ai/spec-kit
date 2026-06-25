"""Contract tests for Agent-Specific Configuration feedback system (C-005, C-008)."""
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

FEEDBACK_DIR = ROOT / ".specify" / "memory" / "feedback"

SAMPLE_FEEDBACK = """\
# Agent Execution Feedback

**Source**: browser-utils
**Agent**: claude-code
**Timestamp**: 2026-06-25T14:30:00
**Outcome**: success-with-workaround

## Obstacle
WebFetch tool does not support file:// URLs for local HTML testing.

## Workaround Applied
Used Playwright via Bash tool instead of WebFetch for local file access.

## Suggested Improvement
Add a note in the browser-utils Claude Code guide that file:// URLs require Playwright, not WebFetch.
"""

REQUIRED_FIELDS = [
    "**Source**:",
    "**Agent**:",
    "**Timestamp**:",
    "**Outcome**:",
    "## Obstacle",
    "## Suggested Improvement",
]


class TestC005FeedbackDocumentStructure:
    """C-005: Feedback documents MUST contain required fields."""

    @pytest.mark.contract
    def test_sample_feedback_has_required_fields(self):
        for field in REQUIRED_FIELDS:
            assert field in SAMPLE_FEEDBACK, (
                f"Sample feedback document missing required field: {field}"
            )

    @pytest.mark.contract
    def test_sample_feedback_valid_outcome(self):
        valid_outcomes = [
            "success-with-workaround",
            "partial-failure",
            "full-failure",
        ]
        for outcome in valid_outcomes:
            if outcome in SAMPLE_FEEDBACK:
                return
        pytest.fail("Sample feedback does not contain a valid outcome value")


class TestC008FeedbackDirectoryExistence:
    """C-008: .specify/memory/feedback/ directory MUST exist."""

    @pytest.mark.contract
    def test_feedback_directory_exists(self):
        assert FEEDBACK_DIR.is_dir(), (
            f"Feedback directory does not exist: {FEEDBACK_DIR}"
        )

    @pytest.mark.contract
    def test_feedback_directory_has_gitkeep(self):
        gitkeep = FEEDBACK_DIR / ".gitkeep"
        assert gitkeep.exists(), (
            f".gitkeep file missing in feedback directory: {gitkeep}"
        )
