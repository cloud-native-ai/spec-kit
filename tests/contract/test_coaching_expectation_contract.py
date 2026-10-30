"""Contract tests for the execution expectation (Feature 078, User Story 2).

Clause source: ``.specify/specs/078-coaching-skills/contracts/expectation.contract.md``
(C-1..C-5). The expectation is a fill-in document, so the tests do two things:

* assert that the template in ``references/prompt-templates.md`` carries the required
  skeleton and the closed row forms, and
* run a small document validator over one compliant expectation and three
  counterexamples (missing ``## Process Efficiency``, undecidable wording, invented
  numbers). The counterexamples MUST be judged red; otherwise the compliant case
  proves nothing.

Literal authority for section names and the expectation path is
``requirements.md`` § Shared Strings (STR-007..STR-009, STR-014).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL = REPO_ROOT / "skills" / "external" / "coaching-skills" / "SKILL.md"
TEMPLATES = (
    REPO_ROOT / "skills" / "external" / "coaching-skills" / "references" / "prompt-templates.md"
)

EXPECTATION_HEADINGS = (
    "Run header",
    "Trainee",
    "Outcome Correctness",
    "Process Efficiency",
    "Assumptions",
    "Unknowns",
    "Forbidden Side Effects",
    "Trainee Failure Semantics",
)

CLOSED_ACCEPTANCE = re.compile(
    r"^(?:pass\|fail|tolerance=\d+(?:\.\d+)?[A-Za-z%]+ severity=(?:low|medium|high))$"
)
UNDECIDABLE = ("roughly", "reasonable", "大致符合")
MAGNITUDE = re.compile(r"^~\d+(?:-\d+)?$")


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str | None:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == f"## {heading}":
            start = index + 1
            break
    if start is None:
        return None
    body: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        body.append(line)
    return "\n".join(body)


def _require_section(text: str, heading: str) -> str:
    body = _section(text, heading)
    assert body is not None and body.strip(), f"missing required section: ## {heading}"
    return re.sub(r"\s+", " ", body).strip()


def _table_rows(text: str, heading: str) -> list[list[str]]:
    body = _section(text, heading)
    assert body is not None, f"missing section: ## {heading}"
    rows: list[list[str]] = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in re.split(r"(?<!\\)\|", stripped)]
        cells = [cell.replace("\\|", "|") for cell in cells[1:-1]]
        if not cells or set("".join(cells)) <= set("-: "):
            continue
        rows.append(cells)
    return rows


def validate_expectation(text: str) -> list[str]:
    """Judge one ``expectation.md`` against C-1..C-3.

    Rules encoded: both dimension sections and all companion headings exist; the OC
    table has the five contract columns, a header row and an ``OC-1`` row whose
    acceptance and deviation cells use the closed form; the PE table has the six
    contract columns; every PE derivation is an anchor or ``validation-gap`` and a
    ``validation-gap`` row carries no invented numbers; undecidable wording is refused
    anywhere in the document.
    """
    errors: list[str] = []
    for heading in EXPECTATION_HEADINGS:
        if _section(text, heading) is None:
            errors.append(f"missing section: ## {heading}")
    if errors:
        return errors

    lowered = text.lower()
    for word in UNDECIDABLE:
        if word.lower() in lowered:
            errors.append(f"undecidable wording: {word}")

    oc_rows = _table_rows(text, "Outcome Correctness")
    assert oc_rows, "the Outcome Correctness table has no rows"
    assert oc_rows[0][:5] == [
        "id",
        "object",
        "acceptance",
        "allowed-deviation",
        "derivation",
    ], f"Outcome Correctness columns drifted: {oc_rows[0]}"
    data_rows = [row for row in oc_rows[1:] if row and row[0].startswith("OC-")]
    if not data_rows:
        errors.append("Outcome Correctness has no OC-* row")
    if not any(row[0] == "OC-1" for row in data_rows):
        errors.append("Outcome Correctness lacks OC-1")
    for row in data_rows:
        if len(row) < 5:
            errors.append(f"OC row has fewer than five cells: {row}")
            continue
        for column in (2, 3):
            if not CLOSED_ACCEPTANCE.match(row[column]):
                errors.append(f"{row[0]} has an open acceptance form: {row[column]}")
        if not row[4].strip():
            errors.append(f"{row[0]} lacks a derivation")

    pe_rows = _table_rows(text, "Process Efficiency")
    assert pe_rows, "the Process Efficiency table has no rows"
    assert pe_rows[0][:6] == [
        "id",
        "steps",
        "tool-calls",
        "retries",
        "critical-path",
        "derivation",
    ], f"Process Efficiency columns drifted: {pe_rows[0]}"
    pe_data = [row for row in pe_rows[1:] if row and row[0].startswith("PE-")]
    if not pe_data:
        errors.append("Process Efficiency has no PE-* row")
    for row in pe_data:
        if len(row) < 6:
            errors.append(f"PE row has fewer than six cells: {row}")
            continue
        derivation = row[5]
        if derivation != "validation-gap" and "#" not in derivation:
            errors.append(f"{row[0]} derivation is neither an anchor nor validation-gap")
        if derivation == "validation-gap":
            if any(cell != "validation-gap" for cell in row[1:5]):
                errors.append(f"{row[0]} invents numbers on a validation-gap row")
        elif not MAGNITUDE.match(row[1]):
            errors.append(f"{row[0]} steps is not an order of magnitude: {row[1]}")
    return errors


COMPLIANT_EXPECTATION = """## Run header
- run-id: 20261030T101500Z-fixture-trainee
- trainee: fixture-trainee (skills/external/fixture-trainee)
- started-at: 2026-10-30T10:14:00Z

## Trainee
- identifier (verbatim): fixture-trainee
- resolved-path: skills/external/fixture-trainee/SKILL.md
- layer: external
- failure-semantics: stop on unreadable input; report failed without inventing rows

## Outcome Correctness
| id | object | acceptance | allowed-deviation | derivation |
|---|---|---|---|---|
| OC-1 | checklist.md | pass\\|fail | pass\\|fail | SKILL.md#Output |
| OC-2 | all five required rows present | pass\\|fail | pass\\|fail | work.md#Required items |

## Process Efficiency
| id | steps | tool-calls | retries | critical-path | derivation |
|---|---|---|---|---|---|
| PE-1 | ~5-8 | read, write; 1 round | 0 | read -> rows -> write | SKILL.md#Workflow |
| PE-2 | validation-gap | validation-gap | validation-gap | validation-gap | validation-gap |

## Assumptions
- The fixture writes next to the brief.

## Unknowns
- Whether the host exposes step events.

## Forbidden Side Effects
- No Trainee tool, script or command is executed.
- No write inside the Trainee directory.
- No network or external call.
- No claim is created in this phase.

## Trainee Failure Semantics
- Unreadable input stops the run; a per-row failure keeps the row and marks it.
"""


# --------------------------------------------------------------------------- #
# C-1 File Shape and Timing
# --------------------------------------------------------------------------- #


def test_c1_template_carries_every_mandatory_heading_in_order():
    text = _text(TEMPLATES)
    positions = [text.find(f"## {heading}") for heading in EXPECTATION_HEADINGS]
    assert all(position >= 0 for position in positions), "a mandatory heading is missing"
    assert positions == sorted(positions), "mandatory headings are out of order"


def test_c1_expectation_path_and_dispatch_ordering_are_declared():
    text = re.sub(r"\s+", " ", _text(SKILL) + "\n" + _text(TEMPLATES))
    assert ".specify/memory/coaching/<run-id>/expectation.md" in text
    assert re.search(r"before any dispatch action", text, re.IGNORECASE)
    assert re.search(r"`dispatched-at`", text)
    assert re.search(r"ordering evidence", text, re.IGNORECASE)


def test_c1_compliant_expectation_passes_and_missing_section_is_red():
    assert validate_expectation(COMPLIANT_EXPECTATION) == []
    broken = COMPLIANT_EXPECTATION.replace("## Process Efficiency", "## Process Notes")
    errors = validate_expectation(broken)
    assert "missing section: ## Process Efficiency" in errors


# --------------------------------------------------------------------------- #
# C-2 Outcome Correctness Rows
# --------------------------------------------------------------------------- #


def test_c2_closed_acceptance_forms_and_oc1_primary_deliverable():
    text = _text(TEMPLATES)
    body = _require_section(text, "Outcome Correctness")
    assert re.search(r"`OC-1` must name the primary deliverable", body, re.IGNORECASE)
    assert "pass|fail" in body
    assert "tolerance=<number><unit> severity=<low|medium|high>" in body


def test_c2_undecidable_wording_is_refused():
    broken = COMPLIANT_EXPECTATION.replace(
        "| OC-1 | checklist.md | pass\\|fail",
        "| OC-1 | checklist.md | roughly matches",
    )
    errors = validate_expectation(broken)
    assert any("undecidable wording: roughly" in error for error in errors)
    assert any("open acceptance form" in error for error in errors)


# --------------------------------------------------------------------------- #
# C-3 Process Efficiency Rows
# --------------------------------------------------------------------------- #


def test_c3_pe_columns_magnitude_profile_retries_and_critical_path():
    body = _require_section(_text(TEMPLATES), "Process Efficiency")
    for column in ("steps", "tool-calls", "retries", "critical-path", "derivation"):
        assert column in body
    assert re.search(r"order of magnitude", body, re.IGNORECASE)
    assert re.search(r"validation-gap", body)
    assert re.search(r"must not be swapped", body, re.IGNORECASE)


def test_c3_invented_numbers_on_a_validation_gap_row_are_red():
    broken = COMPLIANT_EXPECTATION.replace(
        "| PE-2 | validation-gap | validation-gap | validation-gap | validation-gap | validation-gap |",
        "| PE-2 | ~9-12 | validation-gap | validation-gap | validation-gap | validation-gap |",
    )
    errors = validate_expectation(broken)
    assert any("invents numbers on a validation-gap row" in error for error in errors)


# --------------------------------------------------------------------------- #
# C-4 Derivation Method
# --------------------------------------------------------------------------- #


def test_c4_derivation_reuses_the_mental_simulation_contract_and_logic_audit():
    body = _require_section(_text(TEMPLATES), "Derivation Method")
    for token in (
        "Initial State",
        "Rules",
        "Known Constraints",
        "Assumptions",
        "Unknowns",
        "Natural Language Logic",
        "Programmatic Logic",
    ):
        assert token in body, f"derivation method lacks {token}"
    assert re.search(r"contract as given", body, re.IGNORECASE)
    assert re.search(r"judgement", body, re.IGNORECASE)
    assert re.search(r"deterministic", body, re.IGNORECASE)
    assert re.search(r"failure semantics", body, re.IGNORECASE)


def test_c4_audit_result_is_recorded_in_the_expectation_file():
    text = _text(TEMPLATES)
    body = _require_section(text, "Derivation Method")
    assert re.search(r"Record the audit result in `expectation\.md`", body, re.IGNORECASE)


# --------------------------------------------------------------------------- #
# C-5 Zero Side Effects
# --------------------------------------------------------------------------- #


def test_c5_expectation_phase_declares_the_four_prohibitions():
    body = _require_section(_text(TEMPLATES), "Zero Side Effects of the Expectation Phase")
    assert re.search(r"execute any Trainee tool, script, or command", body, re.IGNORECASE)
    assert re.search(r"write inside the Trainee's directory", body, re.IGNORECASE)
    assert re.search(r"network or external calls", body, re.IGNORECASE)
    assert re.search(r"create the run's claim marker", body, re.IGNORECASE)
    assert re.search(r"only\s+allowed interaction", body, re.IGNORECASE)
    assert ".optimization-claims" not in body
