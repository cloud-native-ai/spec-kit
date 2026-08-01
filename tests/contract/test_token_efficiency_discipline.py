"""Contract tests for Feature 040 token-efficiency discipline doc (spec 035).

Pins contracts/discipline-doc.md: C-D1 (existence + mirror parity), C-D2
(six required sections), C-D3 (normative content), C-D4 (ambient reference),
C-D5 (reference-not-copy).
"""

from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]

DOC = ROOT / "shared" / "guidelines" / "token-efficiency.md"
DOC_MIRROR = ROOT / ".specify" / "shared" / "guidelines" / "token-efficiency.md"
INSTR = ROOT / "templates" / "instructions-template.md"
INSTR_MIRROR = ROOT / ".specify" / "templates" / "instructions-template.md"

SECTION_HEADINGS = [
    "## 程序优先(Program-First)",
    "## 摘要优先(Summary-First)",
    "## 升级阶梯(Escalation Ladder)",
    "## 小文件阈值",
    "## 判定边界",
    "## 消耗观察(Consumption Observation)",
]


def test_cd1_doc_exists():
    assert DOC.is_file(), f"missing discipline doc: {DOC}"


def test_cd1_mirror_byte_identical():
    assert DOC_MIRROR.is_file(), f"missing mirror: {DOC_MIRROR}"
    assert DOC.read_bytes() == DOC_MIRROR.read_bytes(), "discipline doc mirror drift"


def test_cd2_required_sections_present():
    text = DOC.read_text(encoding="utf-8")
    missing = [h for h in SECTION_HEADINGS if h not in text]
    assert not missing, f"missing sections: {missing}"


def test_cd3_program_first_rule_terms():
    text = DOC.read_text(encoding="utf-8")
    for term in ["模式匹配", "结构校验", "计数", "去重", "排序", "比对"]:
        assert term in text, f"fixed-rule term missing: {term}"
    assert "MUST" in text and "MUST NOT" in text


def test_cd3_summary_first_exceptions():
    text = DOC.read_text(encoding="utf-8")
    for marker in ["(a)", "(b)", "(c)"]:
        assert marker in text, f"exception marker missing: {marker}"


def test_cd3_small_file_threshold():
    text = DOC.read_text(encoding="utf-8")
    assert "≤ 100 行" in text, "line-threshold literal missing"
    assert "≤ 10 KB" in text, "size-threshold literal missing"
    assert "唯一定义点" in text, "single-definition-point declaration missing"


def test_cd3_observation_marker_and_no_fabrication():
    text = DOC.read_text(encoding="utf-8")
    assert "token-efficiency" in text, "STR-001 marker convention missing"
    assert "不编造" in text, "no-fabricated-counts rule missing"


def test_cd3_cross_references_not_copies():
    text = DOC.read_text(encoding="utf-8")
    assert "tool-reuse-gate.md" in text, "tool-reuse gate cross-reference missing"
    assert "feedback-step.md" in text, "feedback-step cross-reference missing"


def test_cd4_ambient_reference_in_instructions_template():
    text = INSTR.read_text(encoding="utf-8")
    assert "token-efficiency" in text, "ambient token-efficiency reference missing"
    assert "shared/guidelines/token-efficiency.md" in text, "ambient reference path missing"


def test_cd4_instructions_template_mirror_identical():
    assert INSTR.read_bytes() == INSTR_MIRROR.read_bytes(), "instructions-template mirror drift"


def test_cd4_ambient_reference_does_not_inline_copy():
    text = INSTR.read_text(encoding="utf-8")
    for heading in SECTION_HEADINGS:
        assert heading not in text, f"instructions template inlines discipline section: {heading}"


def test_cd5_headings_only_in_discipline_doc():
    offenders = []
    for base in (ROOT / "shared", ROOT / "templates"):
        for md in base.rglob("*.md"):
            if md == DOC:
                continue
            text = md.read_text(encoding="utf-8", errors="replace")
            for heading in SECTION_HEADINGS:
                if heading in text:
                    offenders.append(f"{md}:{heading}")
    assert not offenders, f"discipline sections copied outside single source: {offenders}"
