"""Contract tests for additive /speckit.docs orchestration (requirement 048, US3)."""
from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
COMMAND = REPO_ROOT / "templates" / "commands" / "docs.md"
REFERENCE = REPO_ROOT / "docs" / "reference" / "commands" / "docs.md"


def command_text() -> str:
    return COMMAND.read_text(encoding="utf-8")


def reference_text() -> str:
    return REFERENCE.read_text(encoding="utf-8")


@pytest.mark.contract
def test_user_input_is_additive_not_replacing_baseline_reconcile() -> None:
    text = command_text()
    assert "baseline reconcile always runs" in text.lower()
    assert "additional actions" in text.lower()
    assert "must not replace" in text.lower()
    assert "writing commission" in text.lower()


@pytest.mark.contract
def test_writing_commission_answers_what_and_where_with_project_evidence() -> None:
    text = command_text().lower()
    assert "what to write" in text
    assert "where it lives" in text
    for source in ["target reader", "task context", "user input", "repository evidence", "writing boundary"]:
        assert source in text, f"content-plan input missing: {source}"


@pytest.mark.contract
def test_placement_uses_one_canonical_home_and_prevents_duplicates() -> None:
    text = command_text().lower()
    assert "search for an existing canonical owner" in text
    assert "exactly one canonical home" in text
    assert "near-duplicate" in text
    assert "improve-docs" in text


@pytest.mark.contract
def test_discovery_routes_refresh_human_indexes_and_agent_map() -> None:
    text = command_text()
    assert "human index" in text.lower()
    assert "/speckit.instructions" in text
    assert ".specify/instructions.md" in text
    assert "Documentation Map" in text
    assert "must not edit compatibility instruction aliases" in text.lower()


@pytest.mark.contract
def test_directional_input_does_not_mutate_target_without_structural_change() -> None:
    text = command_text()
    assert "directional input" in text.lower()
    assert "priority" in text.lower()
    assert "does not change the target declaration" in text.lower()


@pytest.mark.contract
def test_structural_input_updates_managed_block_only_after_existing_r4() -> None:
    text = command_text()
    assert "structural change" in text.lower()
    assert "target-declaration update action" in text.lower()
    assert "same existing r4 plan" in text.lower()
    assert "outside-block bytes" in text


@pytest.mark.contract
def test_handoffs_remain_outside_docs_orchestration() -> None:
    text = command_text()
    assert "create-pages" in text
    assert "improve-skills" in text
    assert "must not become a reconcile action" in text.lower()


@pytest.mark.contract
def test_fanout_announcement_and_abort_semantics_are_public() -> None:
    text = command_text()
    for marker in [
        "announce the full document count",
        "abort before dispatch",
        "completed actions stay completed",
        "pending",
    ]:
        assert marker in text.lower()


@pytest.mark.contract
def test_reference_documents_target_layering_and_dual_routing() -> None:
    text = reference_text()
    assert ".specify/docs/target-structure.md" in text
    assert ".specify/skills/create-docs/SKILL.md" in text
    assert ".specify/skills/improve-docs/SKILL.md" in text
    assert "three-stage" in text.lower()
    assert "additional" in text.lower()
    assert "no per-run cap" in text.lower()
    assert "Target structure declaration" in text


@pytest.mark.contract
def test_reference_does_not_copy_static_baseline_enumerations() -> None:
    text = reference_text()
    assert "README.md" not in text
    assert "concepts/ tutorials/ tasks/ reference/ decisions/ contribute/" not in text
    assert "title/created/expires/status/target/tags" not in text


@pytest.mark.contract
def test_command_keeps_exact_top_level_shape_and_required_literals() -> None:
    text = command_text()
    headings = [line for line in text.splitlines() if line.startswith("## ")]
    assert headings == [
        "## User Input",
        "## Glossary",
        "## Outline",
        "## Feedback",
        "## Documentation",
        "## Handoffs",
    ]
    for marker in [
        "reconcile-pattern.md",
        "docs-utils.py",
        "single source of truth",
        "stop-and-confirm",
        "观察快照",
        "残差报告",
        "审计日志",
        "干跑计划",
    ]:
        assert marker in text
    assert "R0 需求解析" not in text
