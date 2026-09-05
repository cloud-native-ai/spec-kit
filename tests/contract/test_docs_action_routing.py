"""Contract tests for typed docs reconcile actions and dual-skill routing."""
from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
COMMAND = REPO_ROOT / "templates" / "commands" / "docs.md"


def command_text() -> str:
    return COMMAND.read_text(encoding="utf-8")


@pytest.mark.contract
def test_action_plan_carries_required_fields_and_source() -> None:
    text = command_text()
    for field in ["type", "target", "owning skill", "confirmation tier", "source"]:
        assert field in text.lower(), f"typed action field missing: {field}"
    assert "evidence" in text.lower()


@pytest.mark.contract
def test_routing_is_mechanical_and_complete() -> None:
    text = command_text()
    assert "structure" in text.lower() and "create-docs" in text
    assert "content" in text.lower() and "improve-docs" in text
    assert "mechanically" in text.lower()
    assert "exactly one owning skill" in text.lower()


@pytest.mark.contract
def test_tolerance_and_evidence_prevent_content_churn() -> None:
    text = command_text()
    assert "tolerance band first" in text.lower()
    assert "must not become an action" in text.lower()
    assert "content action requires concrete evidence" in text.lower()
    assert "unobserved" in text.lower()


@pytest.mark.contract
def test_content_dispatch_is_sequential_unbounded_and_announced() -> None:
    text = command_text()
    assert "one document at a time" in text.lower()
    assert "sequential" in text.lower()
    assert "no per-run cap" in text.lower()
    assert "must not truncate" in text.lower()
    assert "announce the full document count" in text.lower()


@pytest.mark.contract
def test_abort_and_residual_report_preserve_progress() -> None:
    text = command_text()
    assert "abort before dispatch" in text.lower()
    assert "completed actions stay completed" in text.lower()
    assert "pending" in text.lower()
    assert "group the residual report by owning skill" in text.lower()
    assert "audit" in text.lower() and "zero convergence" in text.lower()


@pytest.mark.contract
def test_routing_adds_no_new_confirmation_gate() -> None:
    text = command_text()
    assert "does not introduce another gate" in text.lower()
    assert "confirmation gate" not in text.lower()
    assert text.count("stop-and-confirm") == 1
