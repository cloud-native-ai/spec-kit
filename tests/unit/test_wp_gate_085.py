"""Unit guards for the Feature 085 additions to the 070 work-package gate."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GATE = ROOT / "skills/external/sdd-loop-driver/scripts/wp-gate.py"


def _load():
    spec = importlib.util.spec_from_file_location("wp_gate_084", GATE)
    module = importlib.util.module_from_spec(spec)
    sys.modules["wp_gate_084"] = module
    spec.loader.exec_module(module)
    return module


wp_gate = _load()


def test_requirements_and_tasks_are_admitted_stages():
    assert "requirements" in wp_gate.STAGES
    assert "tasks" in wp_gate.STAGES


def test_new_decomposition_rules_are_registered():
    assert "decompose-requirements-v1" in wp_gate.RULES
    assert "decompose-tasks-v1" in wp_gate.RULES


def test_legacy_rules_remain_registered():
    for rule in (
        "decompose-plan-v1",
        "decompose-implement-v1",
        "decompose-review-v1",
        "decompose-investigation-v1",
    ):
        assert rule in wp_gate.RULES
