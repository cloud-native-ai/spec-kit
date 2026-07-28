"""Contract test: docs-sync step injection (spec 033 US3).

Driven by ``.specify/specs/033-docs-command/contracts/docs-step-injection.md``
(C-1…C-9): single source of truth ``shared/workflow/docs-step.md``, injected as
a reference-only ``## Documentation`` section into all 14 complex command
templates (adjacent to ``## Feedback``, before ``## Handoffs``); the 4 simple
templates stay clean.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
COMMANDS_DIR = REPO_ROOT / "templates" / "commands"
SOURCE = REPO_ROOT / "shared" / "workflow" / "docs-step.md"
MIRROR = REPO_ROOT / ".specify" / "shared" / "workflow" / "docs-step.md"

COMPLEX_COMMANDS = [
    "requirements", "clarify", "plan", "tasks", "implement",
    "analyze", "checklist", "review", "research",
    "instructions", "tools", "skills", "todo", "docs",
]
SIMPLE_COMMANDS = ["agents", "constitution", "feature", "team"]


def section(text: str, heading: str) -> str:
    m = re.search(rf"^{re.escape(heading)}$(.*?)(?=^## |\Z)", text, re.M | re.S)
    assert m, f"missing {heading}"
    return m.group(1)


@pytest.mark.contract
def test_c1_single_source_and_mirror():
    assert SOURCE.is_file(), "shared/workflow/docs-step.md missing"
    assert MIRROR.is_file(), ".specify mirror missing"
    assert SOURCE.read_bytes() == MIRROR.read_bytes(), "docs-step mirror drift"


@pytest.mark.contract
def test_c2_injection_scope_counts():
    assert len(COMPLEX_COMMANDS) == 14
    assert len(SIMPLE_COMMANDS) == 4


@pytest.mark.contract
@pytest.mark.parametrize("cmd", COMPLEX_COMMANDS)
def test_c3_c4_documentation_section_position_and_reference(cmd: str):
    text = (COMMANDS_DIR / f"{cmd}.md").read_text(encoding="utf-8")
    fb, doc, ho = text.find("## Feedback"), text.find("## Documentation"), text.find("## Handoffs")
    assert doc != -1, f"{cmd}.md missing ## Documentation"
    assert fb != -1 and fb < doc, f"{cmd}.md: ## Documentation must follow ## Feedback"
    assert ho == -1 or doc < ho, f"{cmd}.md: ## Documentation must precede ## Handoffs"
    between = text[fb:doc]
    assert not re.search(r"^## (?!Feedback)", between, re.M), \
        f"{cmd}.md: ## Documentation must be adjacent to ## Feedback"
    body = section(text, "## Documentation")
    assert "docs-step.md" in body, f"{cmd}.md Documentation section must cite docs-step.md"
    assert len(body) < 1500, f"{cmd}.md Documentation section must reference, not copy, the rules"
    assert "需记录" in body and "无需记录" in body, f"{cmd}.md missing the conclusion contract"


@pytest.mark.contract
@pytest.mark.parametrize("cmd", SIMPLE_COMMANDS)
def test_c2_simple_commands_not_injected(cmd: str):
    text = (COMMANDS_DIR / f"{cmd}.md").read_text(encoding="utf-8")
    assert "## Documentation" not in text, f"{cmd}.md must not carry the docs-sync step"


@pytest.mark.contract
def test_c6_c7_incremental_and_zero_new_machinery():
    text = SOURCE.read_text(encoding="utf-8")
    assert "R0" in text and "NEVER trigger" in text, "incremental-only rule missing"
    assert "Non-blocking" in text
    assert "Zero new machinery" in text
