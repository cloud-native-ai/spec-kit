"""Contract test: the driver's direction audit (re-anchor) is present and complete.

The defect this guards: the driver manual was loaded once at session start, and after a long
run the loop rules lost salience — package boundaries ended in approval requests, the state
spine lagged, and probe escapes went unnoticed. The repair is a mandatory fifth checkpoint
part: a bounded reload (T0/T1/T2) plus five binary questions and a three-valued verdict.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
# `SPECKIT_CONTRACT_ROOT` lets the red-control run (T016-T018) point this module at a
# mutated *copy* of the repository root, so a mutant can be shown to red without the
# tracked protocol ever being edited. Unset (the normal run) it is the repository itself.
ROOT = Path(os.environ.get("SPECKIT_CONTRACT_ROOT") or ROOT)
SKILL = ROOT / "skills" / "external" / "sdd-loop-driver" / "SKILL.md"
PROTOCOL = ROOT / "skills" / "external" / "sdd-loop-driver" / "references" / "checkpoint-protocol.md"

AUDIT_HEADING = "### 5. Direction audit"
# The minimal-shape checklist line that must answer question 1 first. The minimal shape is
# the one form a checkpoint is written from, so a goal-first rewrite there is the failure
# this guard exists for.
MINIMAL_Q1_PREFIX = "- Q1 rules:"
# The eight rules the protocol itself names inline; a rewrite that drops one leaves the
# question asking "which rules" with no set to ask against.
# The eighth (`spine written before acting`) is asserted as a PATTERN: the contract names it
# that way in a requirement, the protocol itself asks it as "Is the state spine fresher…" and
# also carries it as `spine written before acting` in the fifth-part bullet. Both forms are the
# same rule; pinning the wording rather than the rule would make the guard a copy-editor.
#
# <!-- 092 handoff: D5 → 090-re-anchoring -->
# One entry per member of the owner's rule anchor (`shared/definitions/re-anchoring-definitions.md`
# §1.1, the only place that enumerates them), numbered ①-⑧ in the owner's order, so the set and
# the owner's list are a one-to-one correspondence and a deleted member reds (092 G3). The
# confirmation gate was missing entirely before this repair; the report discipline was missing
# too and `unattended` / `no approval request` stood for one member between them - both ① forms
# are kept here because the protocol names the rule twice, but they map to the single member ①.
RULE_SET = (
    ("① unattended (no approval request)", r"unattended"),
    ("① unattended (no approval request), verbatim form", r"no approval request"),
    ("② U4 -> next stage", r"U4 -> next"),
    ("③ spine written before acting", r"spine written before acting|spine fresher"),
    ("④ workspace guard", r"workspace-guard --check"),
    ("⑤ fast-fail correction/decision split", r"fast-fail"),
    ("⑥ the gate discipline", r"gate discipline"),
    ("⑦ budget discipline", r"budget"),
    ("⑧ report discipline", r"\breport discipline\b"),
)
# The primary-object sentence carries the goal as a *contracted* half ("the RULES, not the
# goal"), so the order is matched rather than a frozen spelling: a rewrite that names the goal
# first, or states the rules without contrasting them with the goal, reds leg 1.
RULE_FIRST_RE = re.compile(
    r"primary object is the RULES\b.*?\bnot the goal\b|primary object is the rules\b.*?\bnot the goal\b"
)
# The ordering sentence itself: the rule verdict and the action it licenses precede any goal
# statement. Matching it yields the position the additive mutation leg measures against.
RULES_FIRST_STMT_RE = re.compile(
    r"the rule verdict and the action it licenses are stated\s+\**before\**\s+any goal statement"
)
# A goal verdict spelled out *before* that sentence is the goal-first drift this guard exists
# for. Nothing else in part 5 legitimately precedes the sentence with either marker.
GOAL_FIRST_MARKER_RE = re.compile(r"\bgoal\s+verdict\b|\bgoal[- ]first\b", re.I)


def test_five_parts_and_direction_audit():
    proto = PROTOCOL.read_text(encoding="utf-8")
    assert "## The five parts (all mandatory)" in proto
    assert "### 5. Direction audit" in proto
    for marker in ("RULES", "unattended", "approval request",
                   "spine fresher", "workspace-guard --check"):
        assert marker in proto, marker
    for verdict in ("on-track", "correction-applied", "decision-needed"):
        assert verdict in proto, verdict


def test_reload_tiers_are_bounded():
    import re
    proto = re.sub(r"\s+", " ", PROTOCOL.read_text(encoding="utf-8"))
    for tier in ("T0", "T1", "T2"):
        assert tier in proto, tier
    assert "full reload of every reference at every step is forbidden" in proto


def test_skill_carries_the_rule_and_the_owner_pointer():
    skill = SKILL.read_text(encoding="utf-8")
    assert "方向审计（Direction audit）" in skill
    assert "references/checkpoint-protocol.md" in skill
    assert "MUST NOT 以征求用户「继续」收尾" in skill


def test_minimal_shape_has_part_five():
    proto = PROTOCOL.read_text(encoding="utf-8")
    shape = proto.split("## Minimal shape", 1)[1]
    assert "## 5. Direction audit" in shape
    assert "reload tier:" in shape


def _flatten(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def _audit_block(proto: str) -> str:
    """Part 5's body: from its heading to the next H2, proof that the block was found."""
    start = proto.index(AUDIT_HEADING) + len(AUDIT_HEADING)
    end = proto.find("\n## ", start)
    assert end > start, "the direction-audit block is empty"
    return proto[start:end]


def _assert_rule_first(proto: str) -> None:
    """The four legs of the ordering proposition, each with its own failure statement."""
    audit = _audit_block(proto)

    # Leg 1 - the rules-first statement is present, so "rules first" is not merely implied.
    assert RULE_FIRST_RE.search(audit), (
        "leg 1: the direction audit no longer states that its primary object is the RULES, not the goal"
    )

    # Leg 2 - the first of the five questions asks the RULES and names the rule set inline.
    # Question 1 wraps over two source lines, so it is read as "the first numbered item plus
    # its indented continuation", not as one physical line.
    first = re.search(r"^\s*(?P<no>\d+)\. .*?(?=^\s*(?P<next>\d+)\. )", audit, flags=re.M | re.S)
    assert first, "leg 2: the direction audit carries no question 1"
    first_text = first.group(0)
    # Read the actual first item instead of asserting a constant against itself (092 G2):
    # the first numbered item must be numbered 1, and the item after it must be numbered 2.
    # Both readings come from the text, so inserting or renumbering a question reds here.
    first_no = first.group("no")
    assert first_no == "1", f"leg 2: the first numbered item is {first_no}, not question 1"
    following_no = first.group("next")
    assert following_no == "2", (
        f"leg 2: the item after the first is numbered {following_no}, so the question list is not consecutive"
    )
    assert "Which rules govern this step" in first_text, (
        "leg 2: the first question no longer asks which RULES govern the step"
    )
    for rule, pattern in RULE_SET:
        assert re.search(pattern, first_text), f"leg 2: the first question dropped the rule {rule!r}"

    # Leg 3 - in the minimal shape the first question line is the rules line, and the goal
    # is not asked as a question of its own anywhere in the answer.
    shape = proto.split("## Minimal shape", 1)[1]
    shape_lines = [ln.strip() for ln in shape.splitlines() if ln.strip().startswith("- Q")]
    assert shape_lines, "leg 3: the minimal shape prints no question line at all"
    assert shape_lines[0].startswith(MINIMAL_Q1_PREFIX), (
        f"leg 3: the minimal shape's first question line is {shape_lines[0][:60]!r}, not the rules line"
    )
    assert not re.search(r"^- Q1 goal:", shape, flags=re.M), (
        "leg 3: the minimal shape asks the goal as question 1"
    )

    # The ordering claim itself: the protocol states that the rule verdict and the action it
    # licenses are stated BEFORE any goal statement, and that the goal is implicit in Q3 rather
    # than asked separately. These are the propositions SC-002 pins; a rewrite that drops the
    # sentence, flips Q1 to the goal, or asks the goal as a question reds.
    flat = _flatten(audit)
    statement = RULES_FIRST_STMT_RE.search(flat)
    assert statement, (
        "ordering: the rules-before-goal verdict sentence is gone from part 5"
    )
    # Leg 4 - the additive mutation leg (092 G1). The sentence claims the rule verdict comes
    # before "any goal statement", so a goal verdict spelled out ahead of it contradicts the
    # rule it is supposed to state. Nothing in the unmutated block uses either marker before
    # the sentence, so this reds exactly when the ordering is inserted around additively.
    before_statement = flat[:statement.start()]
    goal_marker = GOAL_FIRST_MARKER_RE.search(before_statement)
    assert not goal_marker, (
        "ordering: a goal verdict is stated before the rule verdict "
        f"({goal_marker.group(0)!r} appears ahead of the rules-first sentence)"
    )
    assert "implicit in it" in flat, (
        "ordering: Q3 no longer states that the goal is implicit in the named next action"
    )
    assert "do not ask the goal as a separate question" in flat, (
        "ordering: the protocol no longer forbids asking the goal as a separate question"
    )


def _rule_first_verdict(text: str) -> tuple[bool, str]:
    """The guard's verdict on a protocol text: ``(green, reason)``.

    Everything `_assert_rule_first` establishes is folded into one boolean so a mutant can be
    shown to red without its assertion escaping as a test error, and so the reason names the
    leg that broke.
    """
    try:
        _assert_rule_first(text)
    except AssertionError as exc:
        return False, str(exc) or "an ordering assertion failed without a message"
    except (IndexError, ValueError) as exc:
        return False, f"an ordering surface could not be read: {exc}"
    return True, "the rule verdict is stated before any goal statement"


# The exact additive line the G1 mutant inserts, and the sentence line it is inserted before.
GOAL_FIRST_LINE = "Goal verdict: on-track — goal first"
RULES_FIRST_SENTENCE_LINE = "  So the rule verdict and the action it licenses are stated"


def test_direction_audit_asks_the_rules_first_and_states_the_verdict_before_any_goal():
    """The ordering gap (`guard-tests.contract.md` C-7, `direction-audit` C-1/C-2/C-3/C-6).

    The defect this guards: the discipline declares "the review's primary object is the
    RULES", yet nothing reds when the audit drifts back to goal-first — every existing
    green (part 5 present, T0/T1/T2 present, three verdict literals present) still passes
    on a goal-first rewrite, which is exactly how the gap survived. This is the one test
    that fails when question 1 stops asking the rules, when the minimal shape stops
    printing the rules line first, or when the primary-object sentence is reworded to name
    the goal. Red control: `test-evidence/ordering-red-control.txt` (one landed pass arm,
    three mutant fail arms).
    """
    assert PROTOCOL.is_file(), f"protocol not found: {PROTOCOL}"
    green, reason = _rule_first_verdict(PROTOCOL.read_text(encoding="utf-8"))
    assert green, reason


def test_additive_goal_verdict_before_the_rules_verdict_reds(tmp_path):
    """092 G1: the fix round deleted the guard's only positional comparison, so a purely
    additive goal-first insertion stayed green. The clone below differs from the tracked
    protocol by exactly one inserted line, placed immediately before the sentence that
    claims the rule verdict precedes any goal statement.
    """
    source = PROTOCOL.read_text(encoding="utf-8")
    assert RULES_FIRST_SENTENCE_LINE in source, (
        "the rules-first sentence line moved; update the mutant builder before trusting it"
    )

    green, reason = _rule_first_verdict(source)
    assert green, f"the unmutated copy read red: {reason}"

    mutant_text = source.replace(
        RULES_FIRST_SENTENCE_LINE,
        f"  {GOAL_FIRST_LINE}\n{RULES_FIRST_SENTENCE_LINE}",
        1,
    )
    assert mutant_text != source, "the additive insertion did not change the text"

    clone = tmp_path / PROTOCOL.name
    clone.write_text(mutant_text, encoding="utf-8")

    green, reason = _rule_first_verdict(clone.read_text(encoding="utf-8"))
    assert green is False, (
        "the additive mutant stayed green: a goal verdict inserted before the rules-first "
        "sentence must red the guard"
    )
    assert "goal verdict" in reason.lower(), f"red for the wrong reason: {reason}"
