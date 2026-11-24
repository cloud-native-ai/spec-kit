"""F18 residual: GATE/DoD rows are not feature-count claims.

The pre-analyze count face scans every live line for claims such as ``7 任务行`` or
``5 tasks`` and compares them with the artifact's actual task count. A GATE row may
quote a shell count command (``grep -cE '^- \\[[ >]\\]'``) or state a gate result; a
DoD row states a completion condition. Neither is a claim about how many tasks the
feature defines, so counting them produced false positives (backlog F18, residual).

The check stays active for real prose claims: the third line below still reports.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

pytestmark = pytest.mark.unit

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "pre-analyze-check.py"


def _load_engine():
    spec = importlib.util.spec_from_file_location("_pre_analyze_f18", ENGINE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _messages(findings):
    return [finding.get("message", "") for finding in findings]


def test_gate_and_dod_rows_are_not_count_claims(tmp_path):
    engine = _load_engine()
    tasks_md = tmp_path / "tasks.md"
    tasks_md.write_text(
        "# Tasks\n\n"
        "- [ ] T001 Do the thing.\n"
        "- GATE-3: 无遗留开放任务。Check: `grep -cE '^- \\[[ >]\\]' tasks.md` 返回 7 任务行。\n"
        "- DoD-1: 5 tasks remain.\n"
        "The feature contains 9 任务行 total.\n",
        encoding="utf-8",
    )
    findings = []
    engine.check_counts([tasks_md], set(), set(), {"T001"}, findings, tmp_path)
    messages = _messages(findings)

    assert not any("claims 7 tasks" in message for message in messages), (
        "a GATE row's quoted count command was treated as a feature task claim: %r" % messages
    )
    assert not any("claims 5 tasks" in message for message in messages), (
        "a DoD row's completion condition was treated as a feature task claim: %r" % messages
    )
    assert any("claims 9 tasks" in message for message in messages), (
        "a real prose count claim must still be reported: %r" % messages
    )
