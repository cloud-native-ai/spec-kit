"""Contract test: the driver's direction audit (re-anchor) is present and complete.

The defect this guards: the driver manual was loaded once at session start, and after a long
run the loop rules lost salience — package boundaries ended in approval requests, the state
spine lagged, and probe escapes went unnoticed. The repair is a mandatory fifth checkpoint
part: a bounded reload (T0/T1/T2) plus five binary questions and a three-valued verdict.
"""
from __future__ import annotations

from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "external" / "sdd-loop-driver" / "SKILL.md"
PROTOCOL = ROOT / "skills" / "external" / "sdd-loop-driver" / "references" / "checkpoint-protocol.md"


def test_five_parts_and_direction_audit():
    proto = PROTOCOL.read_text(encoding="utf-8")
    assert "## The five parts (all mandatory)" in proto
    assert "### 5. Direction audit" in proto
    for marker in ("goal_verbatim", "non_goals", "stage_plan", "approval request",
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
