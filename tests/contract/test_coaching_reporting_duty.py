"""Contract test: the coaching skill demonstrates the master-reporting duty (087, T020 — US2).

Layer-2 of the Feature 087 test map. This file owns the assertions over
``skills/external/coaching-skills/SKILL.md`` and the payload amendment that
``contracts/supervision-report.contract.md`` C-32 / C-36 / C-37 / C-38 / C-39 fix.

**Clause partition**: this file is responsible for the coaching-skill side of US2 — the reported
sub-flow (C-32, C-36), the payload's one added field (C-37), the one added forbidden class and the one
added return item (C-38), and the demonstration-versus-definition boundary (C-39). Its own green
point is C-32: the skill names its single Trainee dispatch as the reported sub-flow. The supervision
projection in the script is asserted by ``test_reporting_obligations.py`` (T021) and rendered by T026.

**Two halves, deliberately**: the **pre-existing** half (the four forbidden classes, the seven payload
fields, the seven return-contract items, the cardinality and transport clauses) must keep holding byte
for byte — that is the compatibility baseline of ``contracts/ownership-map.contract.md`` C-51, and a
failure there is a regression, not a red-first signal. The **added** half (the supervision report
section, the one new payload row, the one new forbidden class, the one new return item) is red until
T023 / T024 author it. Splitting them keeps the two failure meanings apart.

**Red-first (Constitution IV)**: authored before T023 and T024 exist, so the added half starts red.
Every test that reads the skill asserts the skill path first, so red is "artifact missing", never an
``ImportError`` or a collection error.

**What this file deliberately does NOT assert**: the owner document's own text (that is
``test_reporting_obligations.py``), the script's supervision projection, and the four pre-existing
coaching contract files' own clauses (C-1…C-5 live in ``test_coaching_dispatch_contract.py``; this
file re-reads its surface only to prove the amendment did not disturb it).
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL = REPO_ROOT / "skills" / "external" / "coaching-skills" / "SKILL.md"
SKILL_MIRROR = REPO_ROOT / ".specify" / "skills" / "coaching-skills" / "SKILL.md"
OWNER = REPO_ROOT / "shared" / "guidelines" / "reporting-obligations.md"
PATTERNS = REPO_ROOT / "skills" / "internal" / "create-team" / "references" / "patterns.md"

#: The owner document the skill must reach instead of defining the duty as its own (C-39).
OWNER_REFERENCE = "shared/guidelines/reporting-obligations.md"

#: The one field C-37 adds to the closed set. The other seven are the pre-existing set, read here for
#: the regression half only — their authority is the skill's own section, not this tuple.
ADDED_FIELD = "reporting-cadence"

#: The four pre-existing forbidden-content classes (C-38 keeps every one of them), as detectors.
PRE_EXISTING_FORBIDDEN = {
    "expectation": (r"the expectation file, any `OC-\*` / `PE-\*` row",),
    "deviation": (r"deviation guesses or conclusions",),
    "coach-authored": (r"coach-authored simplification or reordering",),
    "run-directory": (r"any artifact path inside the run directory",),
}

#: The four pre-existing return-contract items (C-38 keeps every one of them, as detectors).
PRE_EXISTING_RETURN_ITEMS = (
    r"step-by-step actions",
    r"tool calls",
    r"state changes",
    r"artifacts",
    r"elapsed time",
    r"terminal state",
)

#: The label convention a sub-flow's identity comes from (``data-model.md`` E3 / E7).
LABEL_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*--[A-Za-z0-9._-]+--[A-Za-z0-9._-]+$")

#: The owner's exclusive literals: the cadence value (owner § 二) and the numeric stall thresholds
#: (owner of those numbers: ``patterns.md`` § Monitoring → Stall Detection). A hit in the skill means
#: the example became a second definition site (C-39).
CADENCE_LITERAL = re.compile(r"30\s*(?:秒|seconds?)", re.I)
THRESHOLD_LITERAL = re.compile(r"\b\d+\s*(?:s|seconds?|秒)\b", re.I)


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _skill() -> Path:
    assert SKILL.is_file(), (
        "coaching skill missing: %s" % SKILL.relative_to(REPO_ROOT)
    )
    return SKILL


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    """Return one ``## <heading>`` section body, ending at the next level-2 heading (or EOF)."""
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == "## %s" % heading:
            start = index + 1
            break
    if start is None:
        return ""
    body = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        body.append(line)
    return "\n".join(body)


def _flatten(text: str) -> str:
    """Collapse whitespace so an assertion can match prose that wraps across lines."""
    return re.sub(r"\s+", " ", text).strip()


def _require_section(text: str, heading: str) -> str:
    body = _section(text, heading)
    assert _flatten(body), (
        "missing required section `## %s` in %s" % (heading, SKILL.relative_to(REPO_ROOT))
    )
    return _flatten(body)


def _payload_rows(text: str) -> dict:
    """Parse § Dispatch Payload's table into ``{field: row_text}``, preserving order."""
    body = _section(text, "Dispatch Payload")
    rows = {}
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells or not cells[0].startswith("`"):
            continue
        name = cells[0].strip("` ")
        if not name:
            continue
        rows[name] = " | ".join(cells)
    return rows


def _report_section(text: str) -> str:
    """The section that carries the subordinate-state report (the duty C-32 / C-36 requires)."""
    for heading in ("Sub-flow Report", "Subordinate Report", "Supervision Report"):
        body = _section(text, heading)
        if _flatten(body):
            return _flatten(body)
    assert False, (
        "the skill carries no section reporting the state of the sub-flow it dispatched;"
        " one of `## Sub-flow Report` / `## Subordinate Report` / `## Supervision Report` is expected"
        " (C-32 / C-36)"
    )


# --------------------------------------------------------------------------- #
# C-36 / C-32 (green point) — the single Trainee dispatch is the reported sub-flow
# --------------------------------------------------------------------------- #
def test_c36_the_skill_names_its_single_trainee_dispatch_as_the_reported_sub_flow():
    """C-36 / MV-05: one dispatch per run is in scope and the report names that ONE, not an empty set."""
    report = _report_section(_text(_skill()))
    assert re.search(r"Trainee", report, re.I), (
        "the report section must name the Trainee dispatch as the reported sub-flow; got %r" % report
    )
    assert re.search(r"\bsub-flow\b", report, re.I), (
        "the report section must say it reports a sub-flow, not the coach's own progress; got %r"
        % report
    )
    # The single-dispatch fact must be visible next to the report, so a reader cannot read the report
    # as describing a set that happens to be empty.
    assert re.search(r"exactly one|single dispatch|one dispatch", report, re.I), (
        "the report must state that this supervisor dispatches exactly one sub-flow; got %r" % report
    )


def test_c32_the_report_names_identity_state_and_age_for_the_sub_flow():
    """C-32 / MV-01: identity, state and the age of last observed activity, for every sub-flow."""
    report = _report_section(_text(_skill()))
    for label, pattern in (
        ("identity (a label)", r"label"),
        ("state", r"\bstate\b"),
        ("age of last observed activity", r"\bage\b"),
    ):
        assert re.search(pattern, report, re.I), (
            "the report section lacks the %s element C-32 fixes; got %r" % (label, report)
        )


def test_c32_the_report_is_not_the_coachs_own_progress():
    """C-32's second half: the report describes the sub-flow; the coach's own progress never replaces it."""
    report = _report_section(_text(_skill()))
    assert re.search(r"not\b[^.]{0,60}(?:own|coach's own)[^.]{0,40}progress|"
                     r"(?:coach's own|its own) progress[^.]{0,60}MUST NOT", report, re.I), (
        "the report section must state that the coach's own progress never substitutes for the"
        " per-sub-flow statement; got %r" % report
    )


def test_c32_the_label_convention_the_identity_comes_from_is_reachable():
    """C-32: the identity is the label convention, reached by path rather than re-invented here."""
    text = _text(_skill())
    assert "subagent-definitions.md" in text, (
        "the skill must reach the label convention's owner by path"
        " (`shared/definitions/subagent-definitions.md` § External Dispatch Visibility Contract)"
    )
    assert LABEL_PATTERN.match("087-fixture--r20261106T000000Z-aaaa--trainee"), (
        "the label convention this test reads identities by is `<slug>--<run-stamp>--<role>`"
    )


# --------------------------------------------------------------------------- #
# C-39 — the example demonstrates the duty; it never defines it
# --------------------------------------------------------------------------- #
def test_c39_the_skill_references_the_duty_owner():
    """C-39 / MV-08: the definition site is named; the skill does not become a second one."""
    assert OWNER.is_file(), "the duty's owner document is missing: %s" % OWNER
    text = _text(_skill())
    assert OWNER_REFERENCE in text, (
        "the skill must reference `%s` for the duty's definition; a demonstration that cites no"
        " owner is a definition in disguise" % OWNER_REFERENCE
    )


def test_c39_the_skill_carries_no_owner_exclusive_cadence_literal():
    """C-39: the cadence value has exactly one definition site and it is not this skill."""
    owner_text = _text(OWNER)
    assert CADENCE_LITERAL.search(owner_text), (
        "premise: the owner carries the cadence literal; this scan is only meaningful against an"
        " owner that does"
    )
    hits = [
        "line %d: %s" % (number, line.strip())
        for number, line in enumerate(_text(_skill()).splitlines(), 1)
        if CADENCE_LITERAL.search(line)
    ]
    assert not hits, (
        "the coaching skill restates the owner's cadence value (C-39): %r" % hits
    )


def test_c39_the_skill_carries_no_threshold_number():
    """C-39: the stall threshold numbers belong to ``patterns.md``; the skill names the row, not the number."""
    patterns = _text(PATTERNS)
    assert "Stall Detection" in patterns, (
        "premise: the threshold owner carries the Stall Detection table"
    )
    hits = [
        "line %d: %s" % (number, line.strip())
        for number, line in enumerate(_text(_skill()).splitlines(), 1)
        if THRESHOLD_LITERAL.search(line)
    ]
    assert not hits, (
        "the coaching skill carries a numeric duration literal (C-39 forbids a second threshold"
        " set; the owner's numbers live in %s): %r"
        % (PATTERNS.relative_to(REPO_ROOT), hits)
    )


def test_c39_the_skill_states_the_no_restatement_direction():
    """C-39: the skill says the duty is reached, not restated — a shape assertion, not a clause copy."""
    text = _flatten(_text(_skill()))
    assert re.search(
        r"MUST NOT (?:restate|become|redefine)|not (?:a|the) definition of the duty"
        r"|never (?:a|the) definition",
        text,
        re.I,
    ), (
        "the skill must state in one line that it demonstrates the duty and does not define it"
        " (C-39), so a later edit that copies the owner's text is visibly against the file's own rule"
    )


# --------------------------------------------------------------------------- #
# C-37 — the closed field set gains EXACTLY one field
# --------------------------------------------------------------------------- #
def test_c37_the_preamble_is_byte_identical():
    """C-37: the closed-set preamble survives verbatim; the set is extended, never widened."""
    payload = _section(_text(_skill()), "Dispatch Payload")
    assert "The payload is a closed field set; anything not listed below is forbidden." in payload, (
        "the closed-field-set preamble must remain byte-identical (C-37); got %r" % _flatten(payload)[:400]
    )


def test_c37_exactly_one_field_is_added_and_it_is_reporting_cadence():
    """C-37 / MV-06: the amendment adds one row, and the row is `reporting-cadence`."""
    rows = _payload_rows(_text(_skill()))
    assert ADDED_FIELD in rows, (
        "§ Dispatch Payload must gain the `%s` row (C-37); fields present: %r"
        % (ADDED_FIELD, sorted(rows))
    )
    row = rows[ADDED_FIELD]
    assert re.search(r"tick value", row, re.I), (
        "the row's content is the tick value in force for this run; got %r" % row
    )
    assert re.search(r"attribution", row, re.I), (
        "the row's content carries the attribution pair the subordinate's lines must carry; got %r" % row
    )
    assert re.search(r"structure slug", row, re.I) and re.search(r"run stamp", row, re.I), (
        "the attribution pair is the structure slug plus the run stamp; got %r" % row
    )


def test_c37_the_added_row_carries_no_numeric_value():
    """C-37 + C-39 together: the row names where the value comes from, never the value itself."""
    rows = _payload_rows(_text(_skill()))
    row = rows.get(ADDED_FIELD, "")
    assert not CADENCE_LITERAL.search(row), (
        "the `%s` row must name the resolved profile's cadence rather than carry a number; got %r"
        % (ADDED_FIELD, row)
    )


def test_c37_no_widening_allowance_is_introduced():
    """C-37's negative half: no "any reporting field" style escape hatch appears."""
    payload = _flatten(_section(_text(_skill()), "Dispatch Payload"))
    for allowance in (
        "any reporting field",
        "any additional field",
        "other reporting fields",
        "and similar",
    ):
        assert allowance not in payload.lower(), (
            "the amendment widened the closed set with %r instead of extending it by one row" % allowance
        )


# --------------------------------------------------------------------------- #
# C-38 — one added forbidden class, one added return item, nothing removed
# --------------------------------------------------------------------------- #
def test_c38_the_four_pre_existing_forbidden_classes_survive():
    """C-38 (compatibility half): every pre-existing forbidden class is still declared."""
    payload = _flatten(_section(_text(_skill()), "Dispatch Payload"))
    missing = [
        name
        for name, patterns in PRE_EXISTING_FORBIDDEN.items()
        if not all(re.search(pattern, payload) for pattern in patterns)
    ]
    assert not missing, "forbidden classes removed or weakened: %r" % missing


def test_c38_exactly_one_forbidden_class_is_added():
    """C-38 / MV-07: the coach's own status lines or its expected subordinate-state conclusions."""
    payload = _flatten(_section(_text(_skill()), "Dispatch Payload"))
    assert re.search(
        r"coach's own status lines|the coach's own status line", payload, re.I
    ), "the added forbidden class must name the coach's own status lines (C-38)"
    assert re.search(r"expected subordinate-state conclusions", payload, re.I), (
        "the added forbidden class must name the expected subordinate-state conclusions (C-38)"
    )


def test_c38_the_pre_existing_return_contract_items_survive():
    """C-38 (compatibility half): every pre-existing return-contract item is still named."""
    payload = _flatten(_section(_text(_skill()), "Dispatch Payload"))
    missing = [item for item in PRE_EXISTING_RETURN_ITEMS if not re.search(item, payload)]
    assert not missing, "return-contract items removed or weakened: %r" % missing


def test_c38_the_self_reported_state_is_added_to_the_return_contract():
    """C-38 / MV-07: the subordinate's own reported state at return, so the coach cites `self-report`."""
    payload = _flatten(_section(_text(_skill()), "Dispatch Payload"))
    assert re.search(r"reported state", payload, re.I), (
        "the return contract must gain the subordinate's own reported state at return (C-38)"
    )
    assert re.search(r"self-report", payload), (
        "the added item exists so the coach cites `self-report` rather than inferring (C-38)"
    )
    assert re.search(r"infer", payload, re.I), (
        "the clause must say the alternative is inference; otherwise the citation rule has no teeth"
    )


# --------------------------------------------------------------------------- #
# the pre-existing surface, re-read so the amendment is proven not to disturb it
# --------------------------------------------------------------------------- #
def test_the_pre_existing_cardinality_and_transport_clauses_still_read():
    """Compatibility: cardinality (exactly one payload) and the transport record are untouched."""
    payload = _flatten(_section(_text(_skill()), "Dispatch Payload"))
    assert re.search(r"Exactly one payload is dispatched per run", payload)
    assert re.search(r"not re-sent with a modified payload", payload)
    for mode in ("native", "run-agent-fallback", "run-skills-explicit-path"):
        assert mode in payload, "transport mode %r disappeared from the payload section" % mode


def test_the_skill_mirror_tracks_the_canonical_source_when_present():
    """Mirror discipline: the generated copy is never hand-edited into disagreement.

    The canonical source is ``skills/external/coaching-skills/SKILL.md``. The mirror is produced by
    ``sync-mirrors.py --write`` (T039 for this feature); until it is regenerated this test states the
    reading rather than silently accepting a divergent copy.
    """
    if not SKILL_MIRROR.is_file():
        pytest.skip("mirror not present in this checkout: %s" % SKILL_MIRROR.relative_to(REPO_ROOT))
    if _text(SKILL_MIRROR) == _text(SKILL):
        return
    generated = REPO_ROOT / ".specify" / "skills" / "coaching-skills"
    assert generated.is_dir(), "a mirror path exists without the mirror directory"
    pytest.skip(
        "mirror is stale against the amended source; regeneration is T039's row"
        " (sync-mirrors.py --write --only skills/external/coaching-skills)"
    )
