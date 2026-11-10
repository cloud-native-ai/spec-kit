"""Contract tests for contracts/state-vocabulary.contract.md — SV-01 … SV-11 (Feature 081).

Subject: the two **declared carriers** of the owner document's schemas —

- ``templates/feature-details-template.md`` § Canonical Status State Machine (SV-03 … SV-07)
- ``templates/verification-log-template.md`` (SV-08 … SV-11)

and, since slice 081d, two further readers of the same owner: the reconciliation of the four
`blocked` literals (SV-01 / SV-02, T002) and the **two remaining vocabulary owners** SV-06 names
beyond the `[FEATURE_STATUS]` token — ``templates/feature-index-template.md`` and
``skills/internal/manage-features/SKILL.md`` (T003).

What this module asserted before 081d, and why the assertions moved: 081a's row T009 pinned
SV-03 … SV-11 only, because those were the clauses whose carriers that slice rewrote. 081d adds
no new carrier for them and edits no existing leg — the `[FEATURE_STATUS]`-token leg
(``test_blocked_is_in_the_feature_status_token``) stays exactly as 081a wrote it and stays the
third of SC-003's 3/3; the additions below are new legs with new subjects, so nothing was moved,
deleted or narrowed to make the module green. The two SV-06 legs are **red before T010** by
design: the index template carries no value-domain list at all today, and the management skill's
`Status vocabulary` line carries five values without `Blocked`.

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
INDEX_TEMPLATE = ROOT / "templates" / "feature-index-template.md"
MANAGE_FEATURES = ROOT / "skills" / "internal" / "manage-features" / "SKILL.md"
OWNER = ROOT / "shared" / "workflow" / "acceptance-hardening.md"

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

#: The four unrelated facts the character sequence `blocked` spells, each with the marker its own
#: carrier physically holds (SV-01). The mapping is asserted, not assumed: every owner below is
#: required to carry its own literal, so a reader that drifted into a pointer fails here.
BLOCKED_LITERAL_OWNERS = {
    "templates/feature-details-template.md": "**Blocked**",
    "templates/verification-log-template.md": "| blocked |",
    "skills/external/sdd-loop-driver/scripts/line-registry.py": "STATE_VALUES",
    "templates/tasks-template.md": "[blockedBy:",
}

#: The status values each vocabulary owner must carry once `Blocked` lands (SV-06). Closed:
#: asserted as a set, so a five-value owner fails rather than passing on a sample. Stale-pin
#: update (2026-11-10, Feature 099 T005; owner `shared/workflow/acceptance-hardening.md`
#: § Feature Status): the domain gains exactly one value `Sealed` with the single transition
#: `Ready for Review → Sealed`, so the pin reads seven.
FEATURE_STATUS_VALUES = (
    "Draft",
    "Planned",
    "Implemented",
    "Blocked",
    "Ready for Review",
    "Sealed",
    "Completed",
)


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


def _reconciliation():
    """The owner sub-block that reconciles the four `blocked` literals (FR-019 / SV-01 / SV-02).

    Read, never assumed: the section is the slice's addition, so its heading is located by the
    fact it states (four `blocked` literals) rather than by a heading string copied from here.
    """
    text = OWNER.read_text(encoding="utf-8")
    start = re.search(r"(?m)^###\s+[^\n]*four\s+`?blocked`?\s+literals", text)
    assert start, (
        "shared/workflow/acceptance-hardening.md § Verification Vocabulary must carry the "
        "reconciliation of the four `blocked` literals (FR-019); no such subsection exists"
    )
    tail = text[start.end():]
    nxt = re.search(r"(?m)^#{1,3}\s", tail)
    return tail[: nxt.start()] if nxt else tail


def _never_regress_rule(text: str) -> str:
    """The `Never regress status` bullet of the management skill, with its indented body."""
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines)
                  if re.match(r"^\s*-\s*\*\*Never regress", l)), None)
    assert start is not None, (
        "skills/internal/manage-features/SKILL.md no longer carries its never-regress rule; the "
        "narrow `Implemented → Blocked` exception has to live in that rule (SV-04)"
    )
    end = start + 1
    while end < len(lines) and (not lines[end].strip() or lines[end].startswith((" ", "\t"))):
        end += 1
    return "\n".join(lines[start:end])


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


# --------------------------------------------------------------------------- #
# SV-01 / SV-02 — the four `blocked` literals are reconciled exactly once (081d T002)
# --------------------------------------------------------------------------- #

def test_the_four_blocked_literals_stay_four():
    """FR-019's carrier: the reconciliation names four owners, one per unrelated fact.

    Added by 081d's T002, which is the row FR-019 owed a carrier to — the requirement named a
    test id and no row created it. The leg is red before T002's owner-doc addition, because until
    then the reconciliation the requirement demands does not exist anywhere.

    Four things are asserted, and each one is the difference between a reconciliation and a
    slogan: every owner is **named** in the section; the named set is **exactly** four (a fifth
    owner is a fifth meaning); every owner **physically holds** the literal it is named for (the
    mapping is real, not a claim about files); and no carrier has **copied** the reconciliation
    back (SV-02 — the reconciliation is written once, in the owner document).
    """
    body = _reconciliation()
    named = {p for p in re.findall(r"`([A-Za-z0-9_./-]+\.(?:md|py))`", body)
             if (ROOT / p).is_file()}
    missing = sorted(set(BLOCKED_LITERAL_OWNERS) - named)
    assert not missing, (
        "the reconciliation must name each of the four `blocked` literal owners; not named: %r "
        "(named: %r)" % (missing, sorted(named))
    )
    assert named == set(BLOCKED_LITERAL_OWNERS), (
        "the reconciliation names %d owner(s) but the four literals have exactly four; a fifth "
        "owner is a fifth meaning, which FR-019 forbids — extra: %r"
        % (len(named), sorted(named - set(BLOCKED_LITERAL_OWNERS)))
    )
    assert re.search(r"(?i)no fifth|fifth meaning", body), (
        "the section must state its own closure — that no fifth meaning may be introduced — "
        "rather than leaving the count to a reader: %r" % body[:200]
    )

    for owner_path, marker in BLOCKED_LITERAL_OWNERS.items():
        carrier = (ROOT / owner_path).read_text(encoding="utf-8")
        assert marker in carrier, (
            "%s is named as an owner of a `blocked` literal but does not carry it (looked for "
            "%r); an owner that lost its literal turns the reconciliation into a bibliography"
            % (owner_path, marker)
        )

    for owner_path in BLOCKED_LITERAL_OWNERS:
        carrier = (ROOT / owner_path).read_text(encoding="utf-8")
        copied = sorted(p for p in BLOCKED_LITERAL_OWNERS if p in carrier)
        assert len(copied) < 4, (
            "SV-02: %s restates the reconciliation (it names all four owners: %r); the four "
            "literals are reconciled once, in shared/workflow/acceptance-hardening.md, and each "
            "carrier must point at that section instead" % (owner_path, copied)
        )

    owner_text = OWNER.read_text(encoding="utf-8")
    assert "Additions to § Verification Vocabulary" not in owner_text, (
        "the § Extension Points bullet that promised this section is still standing; the file "
        "must never carry both a section and a promise of it (FR-019)"
    )


# --------------------------------------------------------------------------- #
# SV-06 — the two remaining vocabulary owners (081d T003, red before T010)
# --------------------------------------------------------------------------- #

def test_the_feature_index_template_carries_a_closed_status_vocabulary():
    """SV-06's first remaining owner — and the leg's subject is that a domain **exists**.

    Added by 081d's T003 and red before T010 lands: measured at 21 lines, the index template's
    only status surface is the `Status` **column header** of its table, so the obligation is to
    add a value domain rather than to insert one value into a list that is already there. A leg
    that assumed the list would pass on a file that has none, which is why the existence of the
    declaration is asserted first and separately.

    The domain must be the file's **own**: a pointer at § Canonical Status State Machine would
    leave the index consumer with no values to read, so the members are required to sit in the
    declaring lines themselves. The transition rows stay with the state-machine owner (SV-03 /
    SV-06), which is why the same leg asserts that no `From | To` row appeared here.
    """
    text = INDEX_TEMPLATE.read_text(encoding="utf-8")
    lines = [l for l in text.splitlines()
             if re.search(r"(?i)status vocabulary|status value", l)]
    assert lines, (
        "templates/feature-index-template.md carries no status value domain at all; SV-06 "
        "requires a closed status vocabulary containing `Blocked`, added beside the table "
        "(today the file's only status surface is the `Status` column header)"
    )
    declared = "\n".join(lines)
    missing = [v for v in FEATURE_STATUS_VALUES if v not in declared]
    assert not missing, (
        "the index template's status vocabulary is missing %r; it must be the file's own value "
        "domain, not a pointer at another file's table — declaring lines: %r"
        % (missing, declared)
    )
    assert re.search(r"(?i)closed", declared), (
        "the index template's vocabulary must declare itself closed, or a writer may invent a "
        "seventh value the state machine does not admit: %r" % declared
    )
    assert not re.search(r"(?m)^\|.*\bFrom\b.*\bTo\b", text), (
        "the index template gained a transition table; the transition rows and the row semantics "
        "stay with `templates/feature-details-template.md` § Canonical Status State Machine (SV-06)"
    )


def test_manage_features_names_blocked_and_points_at_the_machine_for_its_exception():
    """SV-06's second remaining owner, plus FR-022's no-second-copy rule as an assertion.

    Added by 081d's T003 and red before T010 lands: the skill's `Status vocabulary` line reads
    five values and `Blocked` is not one of them, and its never-regress rule carries no
    `Implemented → Blocked` exception at all.

    The exception is required **by pointer**: the rule must name the pointer's target
    (`.specify/templates/feature-details-template.md` § Canonical Status State Machine) and must
    not copy the owner's criteria, so the two facts a reader needs — *that* the exception exists
    and *what* it requires — keep one home each. The no-copy half is the assertion, not the
    intent: the owner's condition sentence and any `From | To` row are required to be absent
    here.
    """
    text = MANAGE_FEATURES.read_text(encoding="utf-8")
    row = next((l for l in text.splitlines()
                if re.match(r"^\s*-\s*Status vocabulary:", l)), None)
    assert row, (
        "skills/internal/manage-features/SKILL.md no longer declares its `Status vocabulary` line; "
        "SV-06 requires that line to carry `Blocked`"
    )
    members = [v.strip().strip("`") for v in row.split(":", 1)[1].split("|")]
    # Stale-pin update (2026-11-10, Feature 099 T005): six -> seven values, `Sealed` joining the
    # closed set; the cardinality moves with FEATURE_STATUS_VALUES and stays an equality pin.
    assert set(members) == set(FEATURE_STATUS_VALUES) and len(members) == 7, (
        "the `Status vocabulary` line must be the seven values %r; measured %r — six values is "
        "the pre-099 shape, and an eighth would be a value the state machine does not admit"
        % (list(FEATURE_STATUS_VALUES), members)
    )

    rule = _never_regress_rule(text)
    assert "Blocked" in rule and "Implemented" in rule, (
        "SV-04: the never-regress rule must carry the narrow `Implemented → Blocked` exception, "
        "by pointer; the rule reads: %r" % rule
    )
    assert re.search(r"(?i)audit", rule) and re.search(r"(?i)evidence", rule), (
        "the exception is an audit correction that cites its evidence — both facts belong to the "
        "rule that grants it: %r" % rule
    )
    assert re.search(r"(\.specify/)?templates/feature-details-template\.md", rule), (
        "the exception must point at the state-machine owner by path; a rule that gestures at "
        "`the template` leaves the criteria unlocatable: %r" % rule
    )
    assert "Canonical Status State Machine" in rule, (
        "the pointer must name its section anchor, not only the file (SV-03/SV-06): %r" % rule
    )
    assert not re.search(r"(?i)four conjunctive conditions", rule), (
        "FR-022: the exception must not copy the owner's criteria — the pointer carries them: %r"
        % rule
    )
    assert not re.search(r"(?m)^\|.*\bFrom\b.*\bTo\b", text), (
        "the management skill gained a transition table; transitions are owned by "
        "`templates/feature-details-template.md` § Canonical Status State Machine and are reached "
        "by pointer (FR-022)"
    )
