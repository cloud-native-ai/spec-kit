"""Contract tests for Feature 107 — Decision Governance (foundational owner-page guards).

This file asserts the contract surface of the owner page
``shared/definitions/decision-definitions.md`` and, later, the pointer discipline of its
adjacent owners and the instruction-section landing. It never asserts prose quality:
section presence is pinned on the ``^## `` heading sequence, the closed vocabulary is pinned
as a row set read out of its own table, and "pointer, not a copy" is decided by comparing
an adjacent owner's headings against the page instead of by reading both documents.

Scenario groups (declared in ``tasks.md``; later packages APPEND new classes/tests without
touching the earlier assertions):

* **F — foundational** (T005): the page exists; § Ownership Declaration names every owned
  surface and the pointer-only duty with its adjacent owners; § Closed Vocabulary carries
  exactly the nine closed terms; no adjacent owner's criteria-table heading is restated.

Red-first tests live in their own modules (``test_decision_governance_guards.py``,
``test_validate_decisions.py``); this module pins the owner-page surface only.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]

OWNER = ROOT / "shared" / "definitions" / "decision-definitions.md"

#: The nine closed terms (T004), verbatim.
NINE_TERMS = (
    "Decision Item",
    "Decision Record",
    "Option",
    "Decision Block",
    "Acknowledgement",
    "Implementation Receipt",
    "Decision Producer",
    "Archive Projection",
    "Decision Class",
)

#: The nine owned surfaces the § Ownership Declaration MUST name (T004), as the English
#: phrases the declaration carries in parentheses.
OWNED_SURFACE_PHRASES = (
    "closed vocabulary",
    "class presentation",
    "option-set contract",
    "record field closure",
    "field-to-owner mapping",
    "archive projection and producer inventory",
    "transmission obligations",
    "enforcement boundary",
    "legacy rules",
)

#: The adjacent owners whose facts the page MUST reach by pointer only (FR-002). The page's
#: pointer table MUST name each path.
ADJACENT_OWNER_PATHS = (
    "shared/guidelines/confirmation-gates.md",
    "shared/guidelines/decision-tension.md",
    "shared/guidelines/fast-fail.md",
    "shared/definitions/superagent-definitions.md",
)

#: Adjacent owner files whose criteria-table H2 headings MUST NOT be restated in the page.
ADJACENT_HEADING_FILES = (
    "shared/guidelines/confirmation-gates.md",
    "shared/guidelines/decision-tension.md",
    "shared/guidelines/fast-fail.md",
    "shared/definitions/superagent-definitions.md",
)

VOCABULARY_ROW_RE = re.compile(r"^\| \*\*(.+?)\*\* \|")


# --------------------------------------------------------------------------- #
# helpers (shared by the groups appended in later packages)
# --------------------------------------------------------------------------- #

def read(path: Path) -> str:
    """Read an artifact, failing as 'missing file' rather than as a wrong assertion."""
    assert path.is_file(), f"missing file: {path}"
    return path.read_text(encoding="utf-8")


def norm(text: str) -> str:
    """Whitespace-normalise an artifact body: the docs hard-wrap prose, the pins are spans."""
    return " ".join(text.split())


def h2_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.startswith("## ")]


def h2_section(text: str, *tokens: str) -> str:
    """Body of the first H2 heading carrying every token, up to the next H2 or EOF."""
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.startswith("## ") and all(token in line for token in tokens):
            start = index
            break
    assert start is not None, f"missing H2 section carrying {tokens!r}"
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return "\n".join(lines[start + 1:end])


# --------------------------------------------------------------------------- #
# F — foundational owner-page guards (T005)
# --------------------------------------------------------------------------- #

def test_owner_page_exists() -> None:
    body = read(OWNER)
    assert body.strip(), "owner page is empty"
    assert body.lstrip().startswith("# "), "owner page carries no level-1 heading"


def test_ownership_declaration_names_every_owned_surface() -> None:
    body = read(OWNER)
    declaration = h2_section(body, "所有权声明", "Ownership Declaration")
    flat = norm(declaration)
    for phrase in OWNED_SURFACE_PHRASES:
        assert phrase in flat, f"§ Ownership Declaration does not name the {phrase!r} surface"
    assert "pointer-only duty" in flat, "§ Ownership Declaration lacks the pointer-only duty"
    for path in ADJACENT_OWNER_PATHS:
        assert path in flat, f"§ Ownership Declaration does not name adjacent owner {path}"


def test_closed_vocabulary_has_exactly_nine_terms() -> None:
    body = read(OWNER)
    section = h2_section(body, "封闭词汇表", "Closed Vocabulary")
    terms = [m.group(1).strip() for m in map(VOCABULARY_ROW_RE.match, section.splitlines()) if m]
    assert len(terms) == len(NINE_TERMS), (
        f"§ Closed Vocabulary carries {len(terms)} term row(s): {terms}"
    )
    assert set(terms) == set(NINE_TERMS), (
        f"§ Closed Vocabulary term set differs: missing={set(NINE_TERMS) - set(terms)}, "
        f"extra={set(terms) - set(NINE_TERMS)}"
    )


def test_no_adjacent_owner_criteria_heading_restated() -> None:
    page_headings = set(h2_lines(read(OWNER)))
    for rel in ADJACENT_HEADING_FILES:
        for heading in h2_lines(read(ROOT / rel)):
            assert heading not in page_headings, (
                f"owner page restates the adjacent heading {heading!r} from {rel}"
            )


# --------------------------------------------------------------------------- #
# US1 — decision text contract and the two decision classes (T009)
# --------------------------------------------------------------------------- #

INSTRUCTION_TEMPLATE = ROOT / "templates" / "instructions-template.md"
FIXTURES = ROOT / "tests" / "fixtures" / "decision-governance"

#: C-102's full-name rule, as the owner page states it (whitespace-normalised pin).
FULL_NAME_PIN = "MUST 使用对象的完整名称，MUST NOT 只用简称"

#: C-103's same-name family, as both the owner page and the instruction section carry it.
SAME_NAME_PINS = ("`same_name_conflict: true`", "`resource_locator`",
                  "business resource group", "region id")


def instruction_section() -> str:
    """Body of the ``## Decision Items（决策项）`` section of the instruction template."""
    return h2_section(read(INSTRUCTION_TEMPLATE), "Decision Items", "决策项")


def test_class_declaration_closed() -> None:
    """C-101: exactly one class from the closed set, judged by holder (A-4)."""
    section = h2_section(read(OWNER), "决策类别", "Decision Classes")
    flat = norm(section)
    assert "持有者(holder)" in flat, (
        "§ Decision Classes does not state that the class is judged by the holder"
    )
    assert "MUST 声明恰一个 `decision_class`" in flat, (
        "§ Decision Classes does not require exactly one decision_class declaration"
    )
    assert "闭集 `human-interactive` / `ai-autonomous`" in flat, (
        "§ Decision Classes does not name the closed class set"
    )
    assert "类缺失、类混合或值域外是缺陷" in flat, (
        "§ Decision Classes does not name the three defect forms"
    )
    assert "类别决定适用的模板与检查集" in flat, (
        "§ Decision Classes does not state that the class picks the template and check set"
    )
    assert "传递不改变类别" in flat, (
        "§ Decision Classes does not state that transmission never re-classes"
    )


def test_full_name_minimum_bar_four_surfaces() -> None:
    """C-102: the two production rules land on four surfaces together."""
    # Surface 1 — the owner page's § Decision Text Contract.
    text_contract = norm(h2_section(read(OWNER), "决策文本契约", "Decision Text Contract"))
    assert FULL_NAME_PIN in text_contract, (
        "owner page § Decision Text Contract does not carry the full-name rule"
    )
    for token in SAME_NAME_PINS:
        assert token in text_contract, (
            f"owner page § Decision Text Contract does not carry {token!r}"
        )
    assert "同名对象 MUST NOT 在没有定位信息时被呈现" in text_contract, (
        "owner page does not ban presenting a same-name object without a locator"
    )

    # Surface 2 — the instruction section (a whole section, not a bullet elsewhere).
    raw = instruction_section()
    instr = norm(raw)
    assert "full name" in instr and "abbreviation" in instr, (
        "instruction section does not carry the full-name rule"
    )
    for token in SAME_NAME_PINS:
        assert token in instr, f"instruction section does not carry {token!r}"
    assert ".specify/shared/definitions/decision-definitions.md" in instr, (
        "instruction section does not point at the owner page"
    )
    assert "**本节字节上限：1,500 B**" in raw, (
        "instruction section does not declare its byte ceiling"
    )
    assert not any(line.strip().startswith("|") for line in raw.splitlines()), (
        "instruction section copies a table from the owner page"
    )

    # Surface 3 — the decision-item templates (owner page § Decision Classes).
    classes = norm(h2_section(read(OWNER), "决策类别", "Decision Classes"))
    assert "完整名称与定位信息(full names and locator)" in classes, (
        "the decision-item templates do not carry the full-name/locator element"
    )
    assert "§ 决策文本契约" in classes, (
        "the decision-item templates do not reach the text contract by pointer"
    )

    # Surface 4 — the guard fixtures plus the named B-01/B-02 review surfaces.
    assert (FIXTURES / "m02" / "red-empty-locator.md").is_file(), (
        "missing M-02 guard fixture"
    )
    assert (FIXTURES / "m08" / "red-variant.md").is_file(), (
        "missing M-08 guard fixture"
    )
    for surface in ("B-01", "B-02"):
        assert surface in text_contract, (
            f"owner page § Decision Text Contract does not name the {surface} review surface"
        )


def test_human_template_elements() -> None:
    """C-104: the human-interactive template carries every readability element."""
    flat = norm(h2_section(read(OWNER), "决策类别", "Decision Classes"))
    for token in (
        "平实语言",
        "上下文(context)",
        "后果(consequences)与可逆性(reversibility)",
        "默认项(default)",
        "完整名称与定位信息(full names and locator)",
        "shared/guidelines/user-facing-comprehension.md",
        "MUST NOT 只给形式化谓词",
    ):
        assert token in flat, f"human-interactive template lacks {token!r}"


def test_ai_template_elements() -> None:
    """C-105: the ai-autonomous template carries every rigor element."""
    flat = norm(h2_section(read(OWNER), "决策类别", "Decision Classes"))
    for token in (
        "封闭选项集(closed options)",
        "决策谓词/规则",
        "显式假设(assumptions)",
        "可机器核查的证据指针(evidence pointers)",
        "确定性结论与重开条件",
        "MUST NOT 只有散文",
    ):
        assert token in flat, f"ai-autonomous template lacks {token!r}"


# --------------------------------------------------------------------------- #
# US2 — option-set contract pointer discipline (T021)
# --------------------------------------------------------------------------- #

#: The gate-observation protocol's signal value domain (owned by
#: ``shared/guidelines/confirmation-gates.md`` § 门控观察协议). The owner page reaches it
#: by pointer only; any of these literals in the section is a restatement.
GATE_SIGNAL_LITERALS = ("approved-as-is", "asked-questions", "denied", "修改后放行")


def test_human_signal_pointer_only() -> None:
    """C-108: the human choice signal is reached by pointer, never restated."""
    section = norm(h2_section(read(OWNER), "选项集契约", "Option-Set Contract"))
    assert "shared/guidelines/confirmation-gates.md" in section, (
        "§ Option-Set Contract does not reach the gate-observation protocol by path"
    )
    assert "门控观察协议" in section, (
        "§ Option-Set Contract does not name the gate-observation protocol section"
    )
    for literal in GATE_SIGNAL_LITERALS:
        assert literal not in section, (
            "§ Option-Set Contract restates the gate-observation signal value "
            f"{literal!r} instead of pointing at its owner"
        )
