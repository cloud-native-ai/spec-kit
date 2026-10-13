"""Contract tests: phase-2 bindings (056 US5, T031 — red-first).

The three non-wrap-up lifecycle points enter the registry: `@point:situation`
(050 情境评估建议与遥测 — engine handler on trigger-utils.py `assess`),
`@point:phase-boundary` (036 团队阶段边界总结 — agent handler on create-team's
summary-refresh wiring), and `@point:confirm-gate` (044 门控必要性证据 — gate
handler h-gate-evidence bound to EVERY gate-class Object, zero gaps).

Gate-object count note: the spec froze "19 gate Objects" at requirements time;
US1's registration grew the live set (22 at execution). The zero-gap assertion
below derives the set from the registry — the count evolution is recorded in
the task row, never pinned as a literal here.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from tests.script_api import probe_utils

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY = REPO_ROOT / "shared" / "definitions" / "probe-definitions.md"
CREATE_TEAM = REPO_ROOT / "skills" / "internal" / "create-team" / "SKILL.md"
GATES = REPO_ROOT / "shared" / "guidelines" / "confirmation-gates.md"
TRIGGER = REPO_ROOT / "scripts" / "python" / "trigger-utils.py"

SITUATION_HANDLER = "h-situation-assess"
PHASE_HANDLER = "h-team-phase-summary"
GATE_HANDLER = "h-gate-evidence"
PHASE_ANCHOR = "Summary Refresh (all patterns)"
GATE_ANCHOR = "门控观察协议 (Gate Observation Protocol)"


def _handlers():
    text = REGISTRY.read_text(encoding="utf-8")
    return {h["handler_id"]: h for h in probe_utils._table_rows(text, "Handler")}


def _bindings():
    text = REGISTRY.read_text(encoding="utf-8")
    return probe_utils._table_rows(text, "HandlerBinding")


def _gate_object_ids() -> set:
    text = REGISTRY.read_text(encoding="utf-8")
    return {o["object_id"] for o in probe_utils._table_rows(text, "Objects")
            if o.get("class_id", "") in ("command-gate", "skill-gate")}


@pytest.mark.contract
def test_phase2_handlers_registered():
    handlers = _handlers()
    missing = [h for h in (SITUATION_HANDLER, PHASE_HANDLER, GATE_HANDLER)
               if h not in handlers]
    assert not missing, f"phase-2 handlers missing from the registry: {missing}"
    assert handlers[SITUATION_HANDLER]["kind"] == "engine"
    assert handlers[SITUATION_HANDLER]["behavior_owner"] == \
        "scripts/python/trigger-utils.py"
    actions = probe_utils._engine_action_union()
    assert handlers[SITUATION_HANDLER]["action"] in actions, \
        "the situation handler's action must be a real trigger-utils action"
    assert handlers[PHASE_HANDLER]["kind"] == "agent"
    assert PHASE_ANCHOR in CREATE_TEAM.read_text(encoding="utf-8"), \
        "the phase-boundary anchor must be the create-team summary-refresh heading"
    assert handlers[PHASE_HANDLER]["action"] == PHASE_ANCHOR
    assert handlers[GATE_HANDLER]["kind"] == "gate"
    assert GATE_ANCHOR in GATES.read_text(encoding="utf-8"), \
        "the gate-evidence anchor must be a governance entry of confirmation-gates.md"


@pytest.mark.contract
def test_situation_and_phase_boundary_bindings_declared():
    by_handler = {}
    for b in _bindings():
        by_handler.setdefault(b["handler_id"], set()).add(b["selector"])
    assert "@point:situation" in by_handler.get(SITUATION_HANDLER, set()), \
        "the situation point must be subscribed"
    assert "@point:phase-boundary" in by_handler.get(PHASE_HANDLER, set()), \
        "the phase-boundary point must be subscribed"


@pytest.mark.contract
def test_gate_evidence_covers_every_gate_object_zero_gap():
    gates = _gate_object_ids()
    assert gates, "no gate-class objects found — the registry or the walker is broken"
    bound = {b["scope"] for b in _bindings() if b["handler_id"] == GATE_HANDLER}
    unbound = gates - bound
    stale = bound - gates
    assert not unbound, f"gate objects without the h-gate-evidence binding: {sorted(unbound)}"
    assert not stale, f"h-gate-evidence bindings pointing at non-gate objects: {sorted(stale)}"


@pytest.mark.contract
def test_validate_green_with_phase2_rows():
    rc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "python" / "probe-utils.py"),
         "--action", "handlers", "--validate"],
        capture_output=True, text=True, check=False)
    assert rc.returncode == 0, f"validate must stay green with the phase-2 rows: {rc.stderr}"


@pytest.mark.contract
def test_wrap_up_compile_unaffected_by_phase2_rows():
    # Phase-2 points never hit the wrap-up plan: the compiled tree must stay zero-drift.
    rc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "python" / "probe-utils.py"),
         "--action", "compile-embeds", "--check"],
        capture_output=True, text=True, check=False)
    assert rc.returncode == 0, f"compile --check drifted: {rc.stdout}{rc.stderr}"
