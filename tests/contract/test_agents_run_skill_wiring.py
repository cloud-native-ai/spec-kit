"""Contract tests for the run dispatch wiring — skill face (104-agents-run, US1+).

Clause source: .specify/specs/104-agents-run/contracts/agents-run-dispatch.contract.md
(C-11..C-22). Presence pins are artifact-class; the runtime content of a payload, the
completeness of a live return, label uniqueness and the probe's execution are
behavior-class.

Clause-class honesty (FR-023): Behavior-class clauses (C-11 / C-12 / C-13 / C-15 /
C-16 / C-18 / C-19) are evidenced by truth-source text + review + mutation drill;
this module does not claim contract coverage of those runtime behaviours. It pins
the truth-source text and its pointers, and nothing more.

Red-first (Constitution IV): authored at T003 before the skill text carries the
role wiring; the C-11..C-15 legs fail against the unchanged tree, while the
C-16..C-22 legs stay red until the US2/US3 slices land (T011 / T013).
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL = REPO_ROOT / "skills" / "internal" / "run-agent" / "SKILL.md"

SEVEN_FIELDS = (
    "parent_identity",
    "child_label",
    "role_declaration",
    "dispatch_duty",
    "depth_position",
    "authority_ref",
    "return_channel",
)

EXACT_SCOPE_BOUNDARY = (
    "**Scope boundary**: Run mode executes a **single** agent on a **single** task."
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _norm(text: str) -> str:
    """Collapse whitespace so a phrase assertion is not defeated by line wrapping."""
    return " ".join(text.split())


def _section(text: str, heading: str) -> str:
    """Body of a markdown heading section, up to the next heading of same-or-higher level."""
    lines = text.splitlines()
    level = len(heading) - len(heading.lstrip("#"))
    start = None
    for i, line in enumerate(lines):
        if line.strip() == heading:
            start = i + 1
            break
    assert start is not None, f"section {heading!r} not found"
    body = []
    for line in lines[start:]:
        if line.startswith("#"):
            head = len(line) - len(line.lstrip("#"))
            if head <= level:
                break
        body.append(line)
    return "\n".join(body)


def _skill() -> str:
    return _norm(_read(SKILL))


def _run_mode() -> str:
    return _norm(_section(_read(SKILL), "### Run Mode (subagent dispatch)"))


def test_c11_presentation_discloses_the_role_relation():
    """C-11: the presentation carries superagent/root, child label and return channel."""
    body = _run_mode()
    assert "superagent" in body, "the presentation does not name the edge's superagent role"
    assert "root" in body, "the root identity is not disclosed"
    assert "child label" in body, "the child label is not disclosed"
    assert "return channel" in body, "the return channel is not disclosed"
    assert "superagent-definitions.md" in body, "the role owner is not cited"
    assert "by pointer" in body, "the role details are not reached by pointer"
    assert "disclosure, not a blocking gate" in body, (
        "the presentation must stay disclosure, never a blocking gate"
    )


def test_c12_downlink_names_the_seven_role_fields():
    """C-12: all seven fields are named and carried by pointer to the owner protocol."""
    body = _run_mode()
    missing = [field for field in SEVEN_FIELDS if f"`{field}`" not in body and field not in body]
    assert not missing, f"the dispatch step does not name these role fields: {missing}"
    assert "The super↔sub Protocol" in body, "the seven-field owner section is not cited"
    assert "by pointer" in body, "the field semantics are not carried by pointer"


def test_c13_four_injections_travel_by_pointer():
    """C-13: the four pre-existing injections are named with their owners."""
    body = _run_mode()
    assert "shared/guidelines/fast-fail.md" in body
    assert "子代理派发注入" in body, "the fast-fail injection owner section is not cited"
    assert "The Concurrency Obligation" in body, "the concurrency obligation owner is missing"
    assert "reporting-obligations.md" in body, "the reporting-duty owner is missing"
    assert "re-anchoring-definitions.md" in body, "the re-anchoring owner is missing"
    assert "four" in body.lower() and "injection" in body.lower(), (
        "the four injections are not named as a set"
    )


def test_c14_role_transition_self_check_keeps_its_literals():
    """C-14: the identifier, the nine slug requirement and the existing phrases remain."""
    text = _skill()
    for literal in (
        "role-transition",
        "Role-Transition Injection",
        "nine item-id slugs",
        "identifier alone is insufficient",
        "payload-construction defect",
    ):
        assert literal in text, f"the role-transition wiring lost its literal: {literal}"
    assert "each of its nine item-id slugs" in text, (
        "the item-by-item self-check is no longer stated"
    )


def test_c15_uplink_requires_the_five_return_elements():
    """C-15: the report step requires the five elements; a miss is incomplete, never backfilled."""
    body = _run_mode()
    assert "The super↔sub Protocol" in body, "the uplink owner section is not cited"
    assert "result or deliverable path" in body
    assert "evidence pointer" in body
    assert "anomaly line" in body and "未发现异常" in body, (
        "the explicit anomaly line (with 未发现异常 for none) is missing"
    )
    assert "concurrency reading" in body and "requested" in body
    assert "effective_reason" in body
    assert "returning executor" in body
    assert "incomplete" in body
    assert "MUST NOT consume" in body, "an incomplete return may still be consumed"
    assert "MUST NOT backfill" in body, "the parent may backfill missing elements"


def test_c16_child_label_reuses_the_dispatch_convention():
    """C-16: label = dispatch.sh <label> = run_id = triplet prefix; retry is a new attempt."""
    body = _run_mode()
    assert "dispatch.sh <label>" in body, "the existing dispatch label carrier is not named"
    assert "run_id" in body and "exec-quant.py --action collect-dispatch" in body
    assert "--run-id <label>" in body, "the label is not passed verbatim as the quant run id"
    for suffix in ("<label>.live.log", "<label>.jsonl", "<label>.status"):
        assert suffix in body, f"the external triplet name is missing: {suffix}"
    assert "new label" in body, "a retry is not stated to use a new label"
    assert "new attempt" in body and "old" in body, "retry-as-new-attempt is not stated"
    assert "watch-model.md" in body and "§ 11" in body, (
        "stale-return attribution is not pointed at the watch model"
    )
    assert "label generator" in body and "child list" in body and "registry" in body, (
        "the zero-new-mechanism boundary of the label convention is not stated"
    )


def test_c17_multi_child_visibility_points_at_existing_carriers():
    """C-17: only the triplet, the exec-quant records and the status-digest role view."""
    body = _run_mode()
    assert "artifact triplet" in body
    assert "exec-quant" in body
    assert "status-digest.py" in body, "the role view carrier is not named"
    for field in ("parent", "roles", "role_set_marker", "depth"):
        assert field in body, f"the role-view field is not named: {field}"
    assert "state store" in body and "renderer" in body, (
        "the no-new-store / no-new-renderer statement is missing"
    )


def test_c18_sdd_probe_applicability_is_narrowed():
    """C-18: the probe runs only for SDD-driver assignments; the refusal shape stays."""
    body = _run_mode()
    assert "sdd-route.py --action authorize" in body
    assert "only when" in body, "the probe's applicability condition is not written down"
    assert "SDD driver" in body, "the narrowed predicate subject is not named"
    assert "MUST NOT invoke the probe" in body, "a normal run is not fenced off the probe"
    assert "MUST NOT be blocked by a missing team/seat" in body
    for token in ("`agent`", "`seat`", "`both`", "source paths", "seat slug"):
        assert token in body, f"the existing refusal shape lost: {token}"


def test_c19_run_stays_a_single_unit_and_records_the_reading():
    """C-19: the exact boundary sentence, no fan-out, and the single-unit reading triple."""
    body = _run_mode()
    assert EXACT_SCOPE_BOUNDARY in body, "the exact scope-boundary sentence was reworded"
    assert "fan out" in body, "the no-fan-out rule is missing"
    assert "multiple command invocations" in body, (
        "multiple runs are not stated to be multiple command invocations"
    )
    assert "requested" in body and "effective" in body and "effective_reason" in body
    assert "single-unit" in body, "the serial reason name is missing"
    assert "not_evaluated" in body, "an absent interval is not recorded as not_evaluated"
    assert "MUST NOT record `0`" in body, "the never-zero rule is missing"


def test_c20_anti_nesting_red_lines_are_preserved():
    """C-20: no driver reference, no skill-load instruction, no loop logic; depth 2 by pointer."""
    text = _skill()
    assert "anti-nesting" in text.lower()
    assert "MUST NOT reference any driver/loop skill" in text
    assert "MUST NOT instruct the subagent to load any skill" in text
    assert "MUST NOT contain loop logic" in text
    assert "depth 2" in text.lower(), "the narrowed depth-2 hierarchy is not cited"


def test_c21_role_is_decided_only_by_the_edge():
    """C-21: the role is a product of the dispatch edge; no switch, entity or fourth category."""
    text = _skill()
    assert "role is decided only by the dispatch edge" in text, (
        "the edge-only role statement is missing"
    )
    assert "superagent-definitions.md" in text, "the role-model owner is not cited"
    for negative in ("activation switch", "role entity", "fourth agent category",
                     "second role definition"):
        assert negative in text, f"the no-second-mechanism role statement lost: {negative}"


def test_c22_zero_second_mechanism_and_clause_class_honesty():
    """C-22: no second dispatch mechanism; behavior-class clauses are not claimed covered."""
    text = _skill()
    for token in ("second dispatch mechanism", "scheduler", "queue", "transport",
                  "notification channel", "persistence root"):
        assert token in text, f"the zero-second-mechanism statement lost: {token}"
    own_source = Path(__file__).read_text(encoding="utf-8")
    assert "Behavior-class clauses (C-11 / C-12 / C-13 / C-15 /" in own_source
    assert "this module does not claim contract coverage of those runtime behaviours" in own_source


# --- US5: failure and partial results are reported honestly (T024) ---
# Red-first (Constitution IV): authored at T024 while the skill text still lacks the bounded
# available list, the corrupt-definition branch, the no-hand-assembly rule and the timeout
# reading. The five legs below pin the text; the runtime conduct of each path is
# behavior-class and is not claimed as covered here.


def test_us5_not_found_reports_a_bounded_list_with_a_create_suggestion():
    """US5: [[STR-002]] + bounded available list (omission declared) + create suggestion + stop."""
    body = _norm(_section(_read(SKILL), "## Input Contract"))
    assert "agent not found" in body, "[[STR-002]] is missing from the resolution path"
    assert "bounded available list" in body, "the not-found path lost its bounded list"
    assert "omission count" in body, "the list truncation does not declare the omission count"
    assert "suggestion" in body and "create" in body, (
        "the not-found path lost its create suggestion"
    )
    assert "no dispatch" in body, "the not-found path is not a zero-dispatch stop"


def test_us5_corrupt_definition_is_named_and_never_merged_with_not_found():
    """US5: a directory with a missing/unreadable definition is `corrupt`, named, never absent."""
    body = _norm(_section(_read(SKILL), "## Input Contract"))
    assert "corrupt" in body, "the corrupt-definition branch is missing"
    assert "定义损坏/不可读" in body, "the corrupt verdict literal is missing"
    assert "named path" in body, "the corrupt verdict does not name the definition path"
    assert "missing or unreadable" in body, "the corrupt trigger condition is not stated"
    assert "MUST NOT be merged with" in body and "not-found" in body, (
        "corrupt and not-found are not kept as distinct verdicts"
    )


def test_us5_config_resolution_failure_stops_without_hand_assembly():
    """US5: a failed resolve stops the dispatch and reports the engine's message, never a fallback."""
    body = _run_mode()
    assert "stops the dispatch" in body, "a failed resolve does not stop the dispatch"
    assert "field/support-set message" in body, (
        "the engine's field/support-set message is not the reported failure"
    )
    assert "MUST NOT hand-assemble" in body, (
        "a failed resolve must not be worked around by assembling arguments by hand"
    )
    assert "MUST NOT merge or normalize configuration itself" in body, (
        "the single-resolver rule is missing"
    )


def test_us5_child_failure_reports_the_partial_result_and_the_reason():
    """US5: failure, timeout and turn-limit all report partial result + reason, never a clean summary."""
    body = _run_mode()
    assert "partial result" in body and "failure reason" in body, (
        "the child-failure reading lost partial result + failure reason"
    )
    assert "times out" in body, "the timeout path is missing from the failure reading"
    assert "turn limit" in body, "the turn-limit path is missing from the failure reading"
    assert "not a summary that hides it" in body, (
        "the failure reading may still be summarized away"
    )


def test_us5_incomplete_return_is_not_consumed_nor_backfilled():
    """US5: a return missing any of the five elements (incl. the anomaly line) is incomplete."""
    body = _run_mode()
    assert "missing any element" in body, "the incomplete-return trigger is not stated"
    assert "incomplete" in body, "the return-completeness verdict is missing"
    assert "anomaly line" in body, "the anomaly line is not part of the completeness check"
    assert "MUST NOT consume" in body, "an incomplete return may still be consumed"
    assert "MUST NOT backfill" in body, "the parent may backfill missing return elements"
