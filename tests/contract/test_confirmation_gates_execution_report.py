"""Structural contract tests for the execution-report convention.

Contract: execution-report-contract.md C-1..C-5 (requirement 044).
The taxonomy doc carries the convention once; every auto-executed flow surface
references it or carries report instructions.
"""
from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
DOC = REPO_ROOT / "shared" / "guidelines" / "confirmation-gates.md"

AUTO_EXEC_SURFACES = [
    REPO_ROOT / "templates" / "commands" / "team.md",
    REPO_ROOT / "skills" / "create-team" / "SKILL.md",
    REPO_ROOT / "templates" / "commands" / "goal.md",
    REPO_ROOT / "templates" / "commands" / "todo.md",
    REPO_ROOT / "templates" / "commands" / "agents.md",
    REPO_ROOT / "templates" / "commands" / "skills.md",
]


@pytest.fixture(scope="module")
def doc_text() -> str:
    assert DOC.is_file()
    return DOC.read_text(encoding="utf-8")


def test_report_section_three_elements(doc_text: str) -> None:
    assert "执行内容" in doc_text
    assert "产出" in doc_text and "工件" in doc_text
    assert "修改途径" in doc_text


def test_report_granularity_and_failure_rules(doc_text: str) -> None:
    assert "琐碎并入" in doc_text, "trivial-merge granularity rule missing"
    assert "合并呈现" in doc_text or "合并为一次收尾呈现" in doc_text
    assert "失败" in doc_text and "中间产物" in doc_text, "failure reporting clause missing"


def test_nonblocking_submission_notice_rule(doc_text: str) -> None:
    assert "非阻塞" in doc_text
    assert "自动传输" in doc_text


@pytest.mark.parametrize("surface", AUTO_EXEC_SURFACES, ids=lambda p: p.name)
def test_auto_exec_surface_carries_report_instructions(surface: Path) -> None:
    assert surface.is_file(), f"missing surface: {surface}"
    text = surface.read_text(encoding="utf-8")
    has_reference = "confirmation-gates.md" in text or "执行报告" in text
    has_report_words = ("呈现" in text or "Report" in text) and (
        "修改" in text or "modify" in text or "improve" in text
    )
    assert has_reference or has_report_words, (
        f"{surface.name}: no execution-report reference or report+modification instructions"
    )
