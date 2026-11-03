"""Contract tests for contracts/state-vocabulary.contract.md — SV-03 … SV-11 (Feature 081, T009).

Subject: the two **declared carriers** of the owner document's schemas —

- ``templates/feature-details-template.md`` § Canonical Status State Machine (SV-03 … SV-07)
- ``templates/verification-log-template.md`` (SV-08 … SV-11)

Owner of every literal asserted here: ``shared/workflow/acceptance-hardening.md`` § Feature Status /
§ Verification Vocabulary / § Gates. The carriers are **declared projections**: they physically hold
what the owner defines, so a reader editing a template finds the rules beside the table it is
editing; they may not widen a value domain, and where they disagree with the owner the owner wins
and the carrier is stale.

Red-first (slice 081a, T009): both carriers are rewritten by T012 and T013, so this module is red
until those rows land. The red run is recorded in
``.specify/specs/081-acceptance-hardening/notes/red-first-evidence.md`` § 1.3.

What is deliberately NOT asserted here: the ``.specify/`` mirrors of these two templates. Mirror
parity is a single fact with a single owner — the `sync-mirrors.py --check` run recorded in this
slice's ``verification.md`` (GW-12/GW-13) — and a second copy of it inside a test would be the
drift it claims to catch.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
DETAILS = ROOT / "templates" / "feature-details-template.md"
VERIFICATION = ROOT / "templates" / "verification-log-template.md"

SM_HEADING = re.compile(r"(?m)^###\s+Canonical Status State Machine")
NEXT_HEADING = re.compile(r"(?m)^##\s")

#: The six-value verification vocabulary (owner § Verification Vocabulary). Closed: a gate, a DoD
#: row or a task row may not narrow it, which is why it is asserted as a set and not as a sample.
VERIFICATION_VALUES = ("pass", "fail", "partial", "blocked", "deferred", "unknown")

#: The five measurement-ladder fields, spelled with the criterion-id prefix (SV-09).
LADDER_FIELDS = (
    "_blocked_at",
    "_reduced_measurement",
    "_reduced_measurement_run",
    "_why_reduced_insufficient",
    "_unblock",
)

#: The three-field smoke record (SV-10).
SMOKE_FIELDS = ("smoke_command", "smoke_exit_code", "smoke_evidence_path")

#: The four `Blocked` transitions, as `(from, to)` pairs (owner § Feature Status).
BLOCKED_ROWS = {
    ("Planned", "Blocked"),
    ("Blocked", "Implemented"),
    ("Blocked", "Ready for Review"),
    ("Implemented", "Blocked"),
}


def _state_machine():
    """The § Canonical Status State Machine body — the block that owns the transitions."""
    text = DETAILS.read_text(encoding="utf-8")
    start = SM_HEADING.search(text)
    assert start, "feature-details-template.md no longer carries § Canonical Status State Machine"
    tail = text[start.end():]
    nxt = NEXT_HEADING.search(tail)
    return tail[: nxt.start()] if nxt else tail


def _transitions():
    """`[(from, to, full_row_line)]` for every `| From | To | …` row of the section's tables."""
    rows = []
    for line in _state_machine().splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) < 2:
            continue
        frm, to = cells[0], cells[1]
        if frm in ("From", "") or set(frm) <= {"-", ":", " "}:
            continue
        rows.append((frm, to, stripped))
    return rows


def _conditions():
    """The numbered items of the `Planned → Implemented` condition block, as a contiguous run."""
    body = _state_machine()
    start = re.search(r"(?i)four conjunctive conditions", body)
    assert start, (
        "§ Canonical Status State Machine must state `Planned → Implemented` as four conjunctive "
        "conditions (owner § Feature Status)"
    )
    items = []
    for line in body[start.end():].splitlines():
        match = re.match(r"^\d+\.\s+(.+)$", line)
        if match:
            items.append(match.group(1).strip())
        elif items and line.strip():
            break  # the numbered run ended; later lists belong to other blocks
    return items


# --------------------------------------------------------------------------- #
# SV-03 — four conjunctive conditions, and the three-of-four consequence
# --------------------------------------------------------------------------- #

def test_planned_to_implemented_is_four_conjunctive_conditions():
    conditions = _conditions()
    assert len(conditions) == 4, (
        "the block must carry exactly four conditions (a fifth reopens the bar; a missing one "
        "restores the zero-final-pass hole): %d found — %r" % (len(conditions), conditions)
    )
    zero_open, has_status_row, final_pass, smoke_pass = conditions

    assert "[ ]" in zero_open and "[>" in zero_open, zero_open
    assert re.search(r"(?i)every success criterion", has_status_row), has_status_row
    assert re.search(r"(?i)status row|SC-NNN_status", has_status_row), has_status_row
    assert re.search(r"(?i)final", final_pass) and "pass" in final_pass, final_pass
    assert re.search(r"(?i)smoke", smoke_pass) and "pass" in smoke_pass, smoke_pass

    assert re.search(r"(?i)three of four", _state_machine()), (
        "the conjunctive rule must state its consequence: three of four is `Blocked`, not a "
        "partial pass"
    )


# --------------------------------------------------------------------------- #
# SV-03 → SV-05 — the four `Blocked` rows
# --------------------------------------------------------------------------- #

def test_the_four_blocked_transition_rows_are_present():
    have = {(frm, to) for frm, to, _ in _transitions()}
    missing = sorted(BLOCKED_ROWS - have)
    assert not missing, "missing transition row(s): %r" % (missing,)


def test_blocked_to_ready_for_review_is_explicitly_illegal():
    row = next((r for f, t, r in _transitions() if (f, t) == ("Blocked", "Ready for Review")), None)
    assert row, "the `Blocked → Ready for Review` row is required even though it is illegal"
    assert re.search(r"(?i)illegal|not allowed|no\b", row), (
        "the row must be spelled out as illegal — a blocked feature has not earned review and "
        "must re-enter through `Implemented`: %r" % row
    )


def test_blocked_to_implemented_states_the_two_lifting_conditions():
    row = next((r for f, t, r in _transitions() if (f, t) == ("Blocked", "Implemented")), None)
    assert row, "`Blocked → Implemented` is the only way out of `Blocked`"
    assert re.search(r"(?i)blocker", row), row
    assert re.search(r"(?i)final", row) and "pass" in row, row


def test_planned_to_blocked_states_the_condition():
    row = next((r for f, t, r in _transitions() if (f, t) == ("Planned", "Blocked")), None)
    assert row, "`Planned → Blocked` is the honest landing for a slice that cannot measure"
    assert re.search(r"(?i)final", row), row
    assert re.search(r"(?i)not\b.*pass|non-`?pass", row), row


def test_implemented_to_blocked_is_a_narrow_audit_exception_that_must_cite_evidence():
    """SV-04: never-regress keeps exactly one exception, and that exception owes evidence."""
    row = next((r for f, t, r in _transitions() if (f, t) == ("Implemented", "Blocked")), None)
    assert row, "`Implemented → Blocked` must be stated as the audit-correction exception"
    assert re.search(r"(?i)audit", row), row
    assert re.search(r"(?i)evidence", row), row
    body = _state_machine()
    assert re.search(r"(?i)never regress|never-regress", body), (
        "the never-regress rule must be stated in this block, with its one narrow exception"
    )
    assert re.search(r"(?i)not\b.*evidence|absence of objection|no objection", body), (
        "the block must state what is NOT evidence: an agent's confirmation and the absence of "
        "objection are not evidence (SV-07's boundary, stated where the rule lives)"
    )


# --------------------------------------------------------------------------- #
# SV-05 — the fourth `Implemented → Ready for Review` condition
# --------------------------------------------------------------------------- #

def test_ready_for_review_carries_its_fourth_condition():
    """Stated in this owner block only; every consumer references it and restates nothing."""
    body = _state_machine()
    match = re.search(r"(?i)fourth condition", body)
    assert match, (
        "the block must name its fourth `Implemented → Ready for Review` condition (SV-05); the "
        "other three are already there"
    )
    tail = body[match.start():]
    assert re.search(r"(?i)final", tail) and re.search(r"(?i)blocked", tail), tail[:400]
    assert re.search(r"(?i)waiver", tail), (
        "the condition's escape hatch is an explicit user waiver, and it must be named: %r"
        % tail[:400]
    )
    assert re.search(r"(?i)user", tail), (
        "the waiver is the *user's*; a driver's or agent's confirmation is never one (SV-07)"
    )


# --------------------------------------------------------------------------- #
# SV-06 — the `[FEATURE_STATUS]` token admits `Blocked`
# --------------------------------------------------------------------------- #

def test_blocked_is_in_the_feature_status_token():
    text = DETAILS.read_text(encoding="utf-8")
    row = next((l for l in text.splitlines()
                if l.startswith("|") and "[FEATURE_STATUS]" in l), None)
    assert row, "the Placeholder Glossary lost its [FEATURE_STATUS] row"
    assert "Blocked" in row, (
        "`Blocked` is a first-class status; the token that enumerates the values must admit it: %r"
        % row
    )
    assert re.search(r"(?m)^- \*\*Blocked\*\*:", text), (
        "the Status Tracking list must define `Blocked` beside the other four states"
    )


# --------------------------------------------------------------------------- #
# SV-08 — the closed six-value verification vocabulary
# --------------------------------------------------------------------------- #

def test_verification_status_set_is_the_closed_six():
    text = VERIFICATION.read_text(encoding="utf-8")
    for value in VERIFICATION_VALUES:
        assert re.search(r"\b%s\b" % value, text), "the vocabulary lost %r" % value
    assert re.search(r"(?i)closed", text), (
        "the set must be declared closed, or a gate may quietly narrow it to a subset"
    )


def test_blocked_and_deferred_are_distinguished_in_one_sentence_each():
    """SV-08: the distinction is the whole point of the sixth value."""
    text = VERIFICATION.read_text(encoding="utf-8")
    blocked = next((l for l in text.splitlines()
                    if re.search(r"\bblocked\b", l) and re.search(r"(?i)not acceptable", l)), None)
    assert blocked, (
        "`blocked` must be defined as *the environment cannot measure this assertion, so the "
        "feature is not acceptable*"
    )
    deferred = next((l for l in text.splitlines()
                     if re.search(r"\bdeferred\b", l) and re.search(r"(?i)may still", l)), None)
    assert deferred, (
        "`deferred` must be defined as *not attempted this round, the feature may still be "
        "acceptable* — which is why it is legal only on a `supporting` path"
    )
    assert re.search(r"(?i)supporting", text), (
        "the `deferred`-is-legal-only-on-a-supporting-path boundary must be stated with it"
    )


# --------------------------------------------------------------------------- #
# SV-09 — the five ladder fields and the mechanical illegal-row rule
# --------------------------------------------------------------------------- #

def test_the_five_ladder_fields_are_named_with_the_sc_prefix():
    text = VERIFICATION.read_text(encoding="utf-8")
    missing = [f for f in LADDER_FIELDS if f not in text]
    assert not missing, "ladder field(s) not named: %r" % (missing,)
    for field in LADDER_FIELDS:
        assert re.search(r"SC-NNN%s\b" % re.escape(field), text), (
            "the field must be spelled with its `SC-NNN` prefix, not as a bare key: %r" % field
        )
    assert re.search(r"(?i)blocked.*deferred.*partial|partial.*deferred.*blocked", text), (
        "the ladder's obligation attaches to `blocked` / `deferred` / `partial`, all three"
    )


def test_the_illegal_ladder_row_rule_is_mechanical():
    """V-6: non-empty `reduced_measurement` AND `run=no` — no semantic judgement in the trigger."""
    text = VERIFICATION.read_text(encoding="utf-8")
    assert re.search(r"(?i)illegal", text), "the illegal-row rule must be stated"
    assert "_reduced_measurement_run=no" in text or "_reduced_measurement_run`=no" in text, (
        "the trigger's second half must be written verbatim, so a checker can match it"
    )
    assert re.search(r"(?i)non-empty", text), (
        "the first half reads *non-empty*, never `available` — a measurement written down and not "
        "run is the same defect the ladder exists to stop"
    )


# --------------------------------------------------------------------------- #
# SV-10 — exactly one three-field smoke record
# --------------------------------------------------------------------------- #

def test_exactly_one_three_field_smoke_record():
    text = VERIFICATION.read_text(encoding="utf-8")
    for field in SMOKE_FIELDS:
        assert field in text, "the smoke record lost %r" % field
    assert re.search(r"(?i)exactly one", text), (
        "the record is exactly one per feature; a second `smoke_command=` line is a defect, not "
        "a choice"
    )
    assert re.search(r"(?i)evidence path", text) and re.search(r"(?i)exist", text), (
        "the evidence path must be required to exist and be non-empty"
    )


# --------------------------------------------------------------------------- #
# SV-11 — anti-vacuity: the vocabulary is not narrowed and the carriers survived
# --------------------------------------------------------------------------- #

def test_neither_carrier_narrows_the_vocabulary():
    """A gate reading `pass|deferred` silently forbids `partial`; the carrier must forbid that."""
    verification = VERIFICATION.read_text(encoding="utf-8")
    assert re.search(r"(?i)narrow", verification), (
        "the file must state that a DoD row or gate may not narrow the set to a subset"
    )
    body = _state_machine()
    assert len(body.splitlines()) > 20, (
        "the state-machine block survived as a real block, not as a stub left after an edit"
    )
