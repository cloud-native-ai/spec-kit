"""Contract test (US2): command feedback-step classification.

Driven by ``contracts/command-classification.md``: each of the 14 **complex**
command templates contains the feedback step; each of the 4 **simple** templates
(``agents``, ``constitution``, ``feature``, ``team``) does NOT.
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
    "interview",
]
SIMPLE_COMMANDS = ["agents", "constitution", "feature", "team"]


def test_classification_counts():
    assert len(COMPLEX_COMMANDS) == 16
    assert len(SIMPLE_COMMANDS) == 4


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
