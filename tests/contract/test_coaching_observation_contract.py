"""Contract tests for the observation record (Feature 078, User Story 3).

Clause source: ``.specify/specs/078-coaching-skills/contracts/observation.contract.md``
(C-1..C-6). The record is a fill-in document, so the tests do two things:

* assert that ``references/prompt-templates.md`` carries the record skeleton, the nine
  step columns and the closed source vocabulary, and
* run a small record validator over one compliant observation and five counterexamples
  (a missing section, the gap marker repeated in ``## Gaps``, a dropped step column, a
  gap row removed while the count stays, an incomplete dispatch narrated as completed).
  The counterexamples MUST be judged red; otherwise the compliant case proves nothing.

Literal authority for ``observation-gap`` / ``host-event`` / ``self-report`` and for the
four artifact names is ``requirements.md`` § Shared Strings (STR-006, STR-011, STR-012,
STR-015).
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

OBSERVATION_SECTIONS = ("Run header", "Dispatch", "Steps", "Gaps", "Result")
DISPATCH_FIELDS = ("mode", "dispatched-at", "payload-ref", "returned", "anomaly-line")
STEP_COLUMNS = (
    "step",
    "trigger/instruction",
    "action",
    "tool-call",
    "state-change",
    "artefact",
    "elapsed",
    "source",
    "consistency",
)
SOURCES = ("host-event", "self-report", "observation-gap")
RESULT_STATES = ("completed", "partial", "failed")


# --------------------------------------------------------------------------- #
# markdown helpers
# --------------------------------------------------------------------------- #


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _slice(text: str, start_heading: str, end_heading: str) -> str:
    """Slice between two known outer headings (the skeleton nests ``## `` inside)."""
    start = text.find(f"## {start_heading}")
    assert start >= 0, f"missing outer section: ## {start_heading}"
    end = text.find(f"## {end_heading}", start)
    assert end > start, f"missing outer section: ## {end_heading}"
    return text[start:end]


def _section(text: str, heading: str) -> str | None:
    """Return the body of ``## <heading>`` up to the next ``## `` heading."""
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


# --------------------------------------------------------------------------- #
# record validator (compliant fixture + counterexamples)
# --------------------------------------------------------------------------- #


def _heading_count(text: str, heading: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip() == f"## {heading}")


def validate_observation(text: str) -> list[str]:
    """Judge one ``observation.md`` against C-1..C-5.

    Rules encoded: the five sections exist in order; exactly one dispatch block carries
    the five DispatchRecord fields; the step table has the nine contract columns; every
    ``source`` value is in the closed vocabulary; ``consistency`` carries both closed
    sub-fields; the gap marker appears only on step rows and ``## Gaps`` reports the same
    count by number and by step id; a non-completed result keeps its failure coordinates
    and an incomplete dispatch is never narrated as completed.
    """
    errors: list[str] = []

    positions: list[int] = []
    for heading in OBSERVATION_SECTIONS:
        index = text.find(f"## {heading}")
        if index < 0:
            errors.append(f"missing section: ## {heading}")
        positions.append(index)
    if errors:
        return errors
    if positions != sorted(positions):
        errors.append("sections are out of the contract order")
    if _heading_count(text, "Dispatch") != 1:
        errors.append("the record carries more than one ## Dispatch block")

    dispatch = _section(text, "Dispatch") or ""
    for field in DISPATCH_FIELDS:
        if not re.search(rf"\b{re.escape(field)}:", dispatch):
            errors.append(f"Dispatch lacks the {field} field")

    rows = _table_rows(text, "Steps")
    if not rows:
        errors.append("## Steps carries no table")
        return errors
    if rows[0][: len(STEP_COLUMNS)] != list(STEP_COLUMNS):
        errors.append(f"## Steps columns drifted: {rows[0][: len(STEP_COLUMNS)]}")

    gap_steps: list[str] = []
    for row in rows[1:]:
        if not row or not row[0].startswith("S"):
            continue
        if len(row) < len(STEP_COLUMNS):
            errors.append(f"{row[0]} has fewer than nine cells")
            continue
        source = row[7]
        if source not in SOURCES:
            errors.append(f"{row[0]} carries an open source value: {source}")
        if source == "observation-gap":
            gap_steps.append(row[0])
        consistency = row[8]
        if "on-critical-path:" not in consistency:
            errors.append(f"{row[0]} consistency lacks on-critical-path")
        if "vs-expected-steps:" not in consistency:
            errors.append(f"{row[0]} consistency lacks vs-expected-steps")

    gaps = _section(text, "Gaps") or ""
    if "observation-gap" in gaps:
        errors.append("the gap marker is repeated in ## Gaps")
    reported = re.search(r"gap-count:\s*(\d+)", gaps)
    if not reported:
        errors.append("## Gaps does not report a gap count")
    elif int(reported.group(1)) != len(gap_steps):
        errors.append(
            f"## Gaps reports {reported.group(1)} gap(s), the step table carries "
            f"{len(gap_steps)}"
        )
    if gap_steps:
        named = re.search(r"step ids?:\s*([^)\n]+)", gaps)
        if not named:
            errors.append("## Gaps does not name the gap step ids")
        else:
            ids = {token.strip() for token in re.split(r"[,;]\s*", named.group(1)) if token.strip()}
            missing = sorted(set(gap_steps) - ids)
            if missing:
                errors.append(f"## Gaps omits the gap step id(s): {', '.join(missing)}")

    result = _section(text, "Result") or ""
    state = re.search(r"state:\s*([A-Za-z-]+)", result)
    if not state:
        errors.append("## Result does not state the run state")
    elif state.group(1) not in RESULT_STATES:
        errors.append(f"## Result carries an open state value: {state.group(1)}")
    elif state.group(1) != "completed" and "failure-coordinates:" not in result:
        errors.append("a non-completed result lacks its failure coordinates")

    returned = re.search(r"returned:\s*([A-Za-z-]+)", dispatch)
    if returned and state and returned.group(1) != "completed" and state.group(1) == "completed":
        errors.append("an incomplete dispatch is narrated as completed")
    return errors


COMPLIANT_OBSERVATION = """## Run header
- run-id: 20261030T101500Z-fixture-trainee
- trainee: fixture-trainee (skills/external/fixture-trainee)
- observation-window: 2026-10-30T10:15:02Z .. 2026-10-30T10:16:40Z

## Dispatch
- mode: native
- dispatched-at: 2026-10-30T10:15:00Z
- payload-ref: .specify/memory/coaching/20261030T101500Z-fixture-trainee/dispatch-payload.md
- returned: partial
- anomaly-line: none
- failure-coordinates: S3 refused the rollback row

## Steps
| step | trigger/instruction | action | tool-call | state-change | artefact | elapsed | source | consistency |
|---|---|---|---|---|---|---|---|---|
| S1 | step 1 — read the brief | read work.md | read_file work.md | brief in context | — | 2s | host-event | on-critical-path: yes; vs-expected-steps: within |
| S2 | step 2 — confirm one item | re-read work.md | read_file work.md | none | — | 1s | self-report | on-critical-path: yes; vs-expected-steps: within |
| S3 | step 4 — write a row for item 4 | no channel carried it | — | — | — | — | observation-gap | on-critical-path: yes; vs-expected-steps: beyond |
| S4 | step 4 — write checklist.md | wrote checklist.md | write_file checklist.md | file created | checklist.md | 3s | host-event | on-critical-path: yes; vs-expected-steps: within |

## Gaps
- gap-count: 1
- step ids: S3
- S3 has no observation channel: neither host events nor the structured return described
  the rollback row, so what the subagent decided there is unknown.

## Result
- state: partial
- failure-coordinates: S3, no row for item 4, S1-S2 and S4 completed
"""


# --------------------------------------------------------------------------- #
# C-1 File Shape
# --------------------------------------------------------------------------- #


def test_c1_template_declares_the_five_sections_in_order():
    block = _slice(_text(TEMPLATES), "Observation Record Template", "Deviations Template")
    positions = [block.find(f"## {heading}") for heading in OBSERVATION_SECTIONS]
    assert all(position >= 0 for position in positions), "a mandatory section is missing"
    assert positions == sorted(positions), "the observation sections are out of order"
    assert _heading_count(block, "Dispatch") == 1, (
        "the skeleton must show exactly one dispatch block"
    )


def test_c1_dispatch_block_carries_the_five_record_fields():
    block = _slice(_text(TEMPLATES), "Observation Record Template", "Deviations Template")
    dispatch = block.split("## Dispatch", 1)[1].split("## Steps", 1)[0]
    for field in DISPATCH_FIELDS:
        assert re.search(rf"\b{re.escape(field)}:", dispatch), f"dispatch block lacks {field}"
    assert re.search(r"expectation\.md", dispatch), "the dispatch block must anchor the ordering"


def test_c1_compliant_record_passes_and_a_missing_section_is_red():
    assert validate_observation(COMPLIANT_OBSERVATION) == []
    broken = COMPLIANT_OBSERVATION.replace("## Gaps", "## Gap Notes")
    assert "missing section: ## Gaps" in validate_observation(broken)


# --------------------------------------------------------------------------- #
# C-2 Step Table Columns
# --------------------------------------------------------------------------- #


def test_c2_step_table_carries_the_nine_columns():
    block = _slice(_text(TEMPLATES), "Observation Record Template", "Deviations Template")
    header = "| " + " | ".join(STEP_COLUMNS) + " |"
    assert header in block, "the nine-column step table header is missing"
    assert "`observation-gap`" in block


def test_c2_consistency_is_observation_only():
    text = _text(TEMPLATES) + "\n" + _text(SKILL)
    flat = re.sub(r"\s+", " ", text)
    assert "on-critical-path: yes|no" in flat
    assert "vs-expected-steps: within|beyond" in flat
    assert re.search(
        r"MUST NOT execute the Trainee's verification logic", flat, re.IGNORECASE
    )


def test_c2_a_dropped_column_is_red():
    broken = COMPLIANT_OBSERVATION.replace(
        "| step | trigger/instruction | action | tool-call | state-change | artefact | elapsed | source | consistency |",
        "| step | trigger/instruction | action | tool-call | state-change | artefact | source | consistency |",
    )
    errors = validate_observation(broken)
    assert any("columns drifted" in error for error in errors)


# --------------------------------------------------------------------------- #
# C-3 Source Tagging
# --------------------------------------------------------------------------- #


def test_c3_sources_are_closed_and_host_event_wins_on_conflict():
    block = _slice(_text(TEMPLATES), "Observation Record Template", "Deviations Template")
    for source in SOURCES:
        assert f"`{source}`" in block, f"the source vocabulary lacks {source}"
    flat = re.sub(r"\s+", " ", block)
    assert re.search(r"`host-event` value wins", flat), (
        "a field-level conflict must resolve to the host event"
    )


def test_c3_an_unknown_source_value_is_red():
    broken = COMPLIANT_OBSERVATION.replace(
        "| 1s | self-report |", "| 1s | model-memory |"
    )
    errors = validate_observation(broken)
    assert any("open source value: model-memory" in error for error in errors)


# --------------------------------------------------------------------------- #
# C-4 Gap Marking and Counting
# --------------------------------------------------------------------------- #


def test_c4_gap_marker_lives_only_on_step_rows():
    block = _slice(_text(TEMPLATES), "Observation Record Template", "Deviations Template")
    flat = re.sub(r"\s+", " ", block)
    assert re.search(r"only on step rows", flat, re.IGNORECASE)
    assert re.search(r"does not repeat the marker", flat, re.IGNORECASE)
    assert "gap-count" in block


def test_c4_a_marker_repeated_in_gaps_is_red():
    broken = COMPLIANT_OBSERVATION.replace("- gap-count: 1", "- observation-gap: 1")
    assert "the gap marker is repeated in ## Gaps" in validate_observation(broken)


def test_c4_an_omitted_gap_row_with_a_stale_count_is_red():
    lines = [line for line in COMPLIANT_OBSERVATION.splitlines() if not line.startswith("| S3")]
    errors = validate_observation("\n".join(lines) + "\n")
    assert any("the step table carries 0" in error for error in errors)


# --------------------------------------------------------------------------- #
# C-5 Failure, Timeout, Refusal
# --------------------------------------------------------------------------- #


def test_c5_failure_timeout_and_refusal_keep_their_coordinates():
    block = _slice(_text(TEMPLATES), "Observation Record Template", "Deviations Template")
    flat = re.sub(r"\s+", " ", block)
    for token in ("failed", "timeout", "refused"):
        assert token in flat, f"the record vocabulary lacks {token}"
    assert re.search(r"failure-coordinates", flat)
    assert re.search(r"gaps? (?:MUST NOT|never) mask a failure|never narrate", flat, re.IGNORECASE)


def test_c5_an_incomplete_dispatch_narrated_as_completed_is_red():
    broken = COMPLIANT_OBSERVATION.replace("returned: partial", "returned: failed").replace(
        "- state: partial", "- state: completed"
    )
    assert "an incomplete dispatch is narrated as completed" in validate_observation(broken)


# --------------------------------------------------------------------------- #
# C-6 Evidence Sufficiency
# --------------------------------------------------------------------------- #


def test_c6_no_observation_still_produces_the_record():
    block = _slice(_text(TEMPLATES), "Observation Record Template", "Deviations Template")
    flat = re.sub(r"\s+", " ", block)
    assert re.search(r"no observation could be collected", flat, re.IGNORECASE)
    assert re.search(r"total absence", flat, re.IGNORECASE)
    assert re.search(r"`evidence: none`", flat)
    assert re.search(r"`run: partial`|run stays `partial`", flat)
