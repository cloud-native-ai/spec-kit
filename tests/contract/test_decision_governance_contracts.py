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
