"""Contract test (US2): command feedback-step classification.

Driven by ``contracts/command-classification.md``: each of the 20 **complex**
command templates contains the feedback step; each of the 3 **simple** templates
(``agents``, ``constitution``, ``feature``) does NOT.
"""
from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
COMMANDS_DIR = REPO_ROOT / "templates" / "commands"

# The stable marker embedded by the feedback step (the engine record invocation).
FEEDBACK_MARKER = "feedback-utils.py"

COMPLEX_COMMANDS = [
    "requirements", "clarify", "plan", "tasks", "implement",
    "analyze", "checklist", "review", "research",
    "instructions", "tools", "skills", "todo", "docs", "goal",
    "interview", "feedback", "sanitize", "derive",
    # `team` reclassified simple → complex on 2026-09-23 (user-adjudicated,
    # introspection-20260923T120035Z#F-02): it invokes 4 distinct scripts,
    # emits .specify/teams/<slug>/team.md consumed by run / goal coordinate /
    # improve-team, and consumes the bound goal's Targets — all three criteria
    # of the classification rule hold. Recorded in the contract's table.
    "team",
]
SIMPLE_COMMANDS = ["agents", "constitution", "feature"]


def test_classification_counts():
    assert len(COMPLEX_COMMANDS) == 20
    assert len(SIMPLE_COMMANDS) == 3


@pytest.mark.contract
@pytest.mark.parametrize("cmd", COMPLEX_COMMANDS)
def test_complex_command_carries_feedback_step(cmd: str):
    text = (COMMANDS_DIR / f"{cmd}.md").read_text(encoding="utf-8")
    assert "## Feedback" in text, f"{cmd}.md missing '## Feedback' heading"
    assert FEEDBACK_MARKER in text, f"{cmd}.md missing feedback record invocation"


@pytest.mark.contract
@pytest.mark.parametrize("cmd", SIMPLE_COMMANDS)
def test_simple_command_omits_feedback_step(cmd: str):
    text = (COMMANDS_DIR / f"{cmd}.md").read_text(encoding="utf-8")
    assert FEEDBACK_MARKER not in text, f"{cmd}.md must NOT carry the feedback step"
