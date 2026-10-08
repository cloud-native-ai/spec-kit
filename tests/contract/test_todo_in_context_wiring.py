"""
Wiring contract for the TODO-in-Context discipline surfaces.

The discipline has one owner (shared/guidelines/todo-in-context.md) plus
pointer surfaces that must stay reachable: the concepts narrative, the
Documentation Map rows (template + this repo's custom instructions), and the
/speckit.todo command template's Philosophy pointer. This test fails when
any surface drifts — renamed, unmirrored, or pointing at a missing file.
"""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
GUIDELINE_SRC = REPO_ROOT / "shared" / "guidelines" / "todo-in-context.md"
GUIDELINE_MIRROR = REPO_ROOT / ".specify" / "shared" / "guidelines" / "todo-in-context.md"
CONCEPTS_DOC = REPO_ROOT / "docs" / "concepts" / "todo-in-context.md"
INSTRUCTIONS_TEMPLATE = REPO_ROOT / "templates" / "instructions-template.md"
LIVE_INSTRUCTIONS = REPO_ROOT / ".specify" / "instructions.md"
TODO_COMMAND_TEMPLATE = REPO_ROOT / "templates" / "commands" / "todo.md"


@pytest.mark.contract
class TestTodoInContextWiring:
    def test_owner_exists_and_declares_ownership(self):
        text = GUIDELINE_SRC.read_text(encoding="utf-8")
        assert "single source of truth" in text
        # owns what it owns by naming its subjects in the opening lines
        head = "\n".join(text.splitlines()[:3])
        for subject in ("TODO-in-Context", "perception"):
            assert subject in head, f"owner opening lines must name {subject}"
        assert "生命周期" in head or "lifecycle" in head

    def test_guideline_is_mirrored_byte_exact(self):
        assert GUIDELINE_MIRROR.is_file(), "guideline mirror missing under .specify/shared/guidelines/"
        src = GUIDELINE_SRC.read_bytes()
        mirror = GUIDELINE_MIRROR.read_bytes()
        assert src == mirror, "guideline source and .specify mirror have drifted"

    def test_concepts_narrative_points_back_at_owner(self):
        text = CONCEPTS_DOC.read_text(encoding="utf-8")
        assert ".specify/shared/guidelines/todo-in-context.md" in text
        assert "docs/concepts/todo-in-context.md" not in text

    def test_instructions_template_carries_map_row(self):
        text = INSTRUCTIONS_TEMPLATE.read_text(encoding="utf-8")
        assert "**TODO-in-Context**" in text
        assert ".specify/shared/guidelines/todo-in-context.md" in text

    def test_live_instructions_carry_map_row(self):
        text = LIVE_INSTRUCTIONS.read_text(encoding="utf-8")
        assert "**TODO-in-Context**" in text
        assert ".specify/shared/guidelines/todo-in-context.md" in text

    def test_command_template_points_at_guideline(self):
        text = TODO_COMMAND_TEMPLATE.read_text(encoding="utf-8")
        assert "todo-in-context" in text
        # pointer shape only: the Philosophy section references the owner, it
        # must not restate the perception obligations
        philosophy = text.split("## User Input", 1)[0]
        for obligation in ("do not silently remove", "must not delete"):
            assert obligation not in philosophy.lower()

    def test_owner_delegates_detection_semantics_to_contract(self):
        text = GUIDELINE_SRC.read_text(encoding="utf-8")
        assert "search-todo-cli.md" in text
        assert "D-9..D-12" in text

    def test_owner_names_command_and_park_boundary(self):
        text = GUIDELINE_SRC.read_text(encoding="utf-8")
        assert "templates/commands/todo.md" in text
        assert ".specify/memory/todo/" in text
