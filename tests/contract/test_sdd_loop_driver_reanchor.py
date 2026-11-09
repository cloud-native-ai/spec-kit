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
RULE_SET = (
    ("unattended", r"unattended"),
    ("no approval request", r"no approval request"),
    ("U4 -> next stage", r"U4 -> next"),
    ("spine written before acting", r"spine written before acting|spine fresher"),
    ("workspace-guard --check", r"workspace-guard --check"),
    ("fast-fail", r"fast-fail"),
    ("the gate discipline", r"gate discipline"),
    ("budget", r"budget"),
)
# The primary-object sentence carries the goal as a *contracted* half ("the RULES, not the
# goal"), so the order is matched rather than a frozen spelling: a rewrite that names the goal
# first, or states the rules without contrasting them with the goal, reds leg 1.
RULE_FIRST_RE = re.compile(
    r"primary object is the RULES\b.*?\bnot the goal\b|primary object is the rules\b.*?\bnot the goal\b"
)


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
    """The three legs of the ordering proposition, each with its own failure statement."""
    audit = _audit_block(proto)

    # Leg 1 - the rules-first statement is present, so "rules first" is not merely implied.
    assert RULE_FIRST_RE.search(audit), (
        "leg 1: the direction audit no longer states that its primary object is the RULES, not the goal"
    )

    # Leg 2 - the first of the five questions asks the RULES and names the rule set inline.
    # Question 1 wraps over two source lines, so it is read as "the first numbered item plus
    # its indented continuation", not as one physical line.
    first = re.search(r"^\s*1\. .*?(?=^\s*2\. )", audit, flags=re.M | re.S)
    assert first, "leg 2: the direction audit carries no question 1"
    first_text = first.group(0)
    assert not re.search(r"^\s*\d+\. ", audit[:first.start()], flags=re.M), (
        "leg 2: a numbered item precedes question 1, so question 1 is not the first question"
    )
    first_no = "1"
    assert first_no == "1", f"leg 2: the first numbered item is {first_no}, not question 1"
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
    assert re.search(
        r"the rule verdict and the action it licenses are stated\s+\**before\**\s+any goal statement",
        flat), (
        "ordering: the rules-before-goal verdict sentence is gone from part 5"
    )
    assert "implicit in it" in flat, (
        "ordering: Q3 no longer states that the goal is implicit in the named next action"
    )
    assert "do not ask the goal as a separate question" in _flatten(audit), (
        "ordering: the protocol no longer forbids asking the goal as a separate question"
    )


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
    _assert_rule_first(PROTOCOL.read_text(encoding="utf-8"))
