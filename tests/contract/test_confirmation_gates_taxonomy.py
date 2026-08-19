"""Structural contract tests for the confirmation-gates taxonomy truth source.

Contract: .specify/specs/044-reduce-confirmation-flows/contracts/confirmation-taxonomy-contract.md
(C-1..C-6) + execution-report-contract.md C-5. Doc-feature gate per constitution.md:93 —
these assert content/structure, not runtime behavior.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
DOC = REPO_ROOT / "shared" / "guidelines" / "confirmation-gates.md"

REQUIRED_SECTIONS = [
    "两级判据",
    "破坏性动作清单",
    "治理保留清单",
    "存疑从严",
    "回流约束",
    "执行报告",
]

DESTRUCTIVE_MIN_ITEMS = [
    "删除",
    "移动",
    "归档",
    "远程推送",
    "覆盖",
]

GOVERNANCE_KEPT_MIN_ROWS = [
    "访谈",
    "宪章",
    "commit",
    "CONFIRM",
    "git-workflow",
    "tools invoke",
]


@pytest.fixture(scope="module")
def doc_text() -> str:
    assert DOC.is_file(), f"taxonomy truth source missing: {DOC}"
    return DOC.read_text(encoding="utf-8")


def _section_bodies(text: str) -> dict[str, str]:
    bodies: dict[str, str] = {}
    matches = list(re.finditer(r"^##\s+(?!#)(.+?)\s*$", text, flags=re.M))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        bodies[m.group(1).strip()] = text[m.end() : end]
    return bodies


def test_all_required_sections_present(doc_text: str) -> None:
    sections = _section_bodies(doc_text)
    for name in REQUIRED_SECTIONS:
        assert any(name in s for s in sections), f"missing section: {name}"


def test_two_level_taxonomy_normative(doc_text: str) -> None:
    body = next(b for s, b in _section_bodies(doc_text).items() if "两级判据" in s)
    assert "MUST" in body
    assert "破坏性" in body and "可逆" in body
    assert "前置" in body and ("自动执行" in body or "自动" in body)


def test_destructive_list_floor(doc_text: str) -> None:
    body = next(b for s, b in _section_bodies(doc_text).items() if "破坏性动作清单" in s)
    bullets = [l for l in body.splitlines() if l.strip().startswith("-")]
    assert len(bullets) >= 4, "destructive list must be conservative and enumerable (>=4)"
    for item in DESTRUCTIVE_MIN_ITEMS:
        assert any(item in b for b in bullets), f"destructive list missing: {item}"


def test_governance_kept_list_floor(doc_text: str) -> None:
    body = next(b for s, b in _section_bodies(doc_text).items() if "治理保留清单" in s)
    for row in GOVERNANCE_KEPT_MIN_ROWS:
        assert row.lower() in body.lower(), f"governance-kept list missing: {row}"


def test_doubtful_strict_rule(doc_text: str) -> None:
    body = next(b for s, b in _section_bodies(doc_text).items() if "存疑从严" in s)
    assert "MUST" in body
    assert "破坏性" in body


def test_anti_backflow_rule(doc_text: str) -> None:
    body = next(b for s, b in _section_bodies(doc_text).items() if "回流约束" in s)
    assert "MUST NOT" in body
    assert "非破坏性" in body or "可逆" in body


def test_execution_report_section_three_elements(doc_text: str) -> None:
    body = next(b for s, b in _section_bodies(doc_text).items() if "执行报告" in s)
    for element in ("执行内容", "产出", "修改"):
        assert element in body, f"execution report section missing element: {element}"
    assert "琐碎" in body, "granularity exemption (trivial merge) missing"
    assert "失败" in body, "failure reporting clause missing"


def test_concept_basis_reference(doc_text: str) -> None:
    assert "reconcile-pattern" in doc_text, "must reference the tiered-confirmation concept basis"
