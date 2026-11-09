"""Contract test: the Re-Anchoring core concept is owned, landed and agent-facing."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_owner_document_carries_both_concepts_and_the_tiers():
    owner = (ROOT / "shared/definitions/re-anchoring-definitions.md").read_text(encoding="utf-8")
    for token in ("不忘初心", "温故而知新", "规则锚", "T0", "T1", "T2",
                  "on-track", "correction-applied", "decision-needed"):
        assert token in owner, token


def test_both_constitution_surfaces_carry_the_principle():
    title = "Re-Anchoring (不忘初心 · 温故而知新)"
    for rel in (".specify/memory/constitution.md", "templates/constitution-template.md"):
        assert title in (ROOT / rel).read_text(encoding="utf-8"), rel


def test_both_instruction_surfaces_carry_the_ambient_section():
    for rel in ("templates/instructions-template.md", ".specify/instructions.md"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert "## Re-Anchoring (不忘初心 · 温故而知新)" in text, rel
        assert "re-anchoring-definitions.md" in text, rel


def test_agent_definitions_carry_the_obligation_pointer():
    text = (ROOT / "shared/definitions/agent-definitions.md").read_text(encoding="utf-8")
    assert "Re-Anchoring Obligation" in text
    assert "re-anchoring-definitions.md" in text
