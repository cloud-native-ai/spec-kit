"""Contract test: the create-docs / improve-docs skill pair (spec 033, C-18).

The docs domain follows the same create/improve split as tools, agents and teams:
``create-X`` owns creation plus structure, ``improve-X`` owns evidence-driven
refinement of the existing artifact, and improving the *skills themselves* stays
with ``improve-skills``. This test pins that boundary so the pair cannot silently
grow into two overlapping engines.
"""
from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
INSTRUCTIONS = REPO_ROOT / ".specify" / "instructions.md"
PAIR = ("create-docs", "improve-docs")
MAX_LINES = 500


def skill_path(name: str) -> Path:
    return REPO_ROOT / "skills" / name / "SKILL.md"


def mirror_path(name: str) -> Path:
    return REPO_ROOT / ".specify" / "skills" / name / "SKILL.md"


def skill_text(name: str) -> str:
    path = skill_path(name)
    assert path.is_file(), f"skills/{name}/SKILL.md missing"
    return path.read_text(encoding="utf-8")


@pytest.mark.contract
@pytest.mark.parametrize("name", PAIR)
def test_c18_pair_member_shape(name: str):
    text = skill_text(name)
    assert text.startswith("---\n"), f"{name}: frontmatter missing"
    frontmatter = text.split("---", 2)[1]
    assert f"name: {name}" in frontmatter, f"{name}: frontmatter name must match the directory"
    assert "description:" in frontmatter, f"{name}: description missing"
    assert f'skill_id: "<SKILL:.specify/skills/{name}/SKILL.md>"' in frontmatter, \
        f"{name}: skill_id must be the canonical resource id"
    assert "Use this when the user mentions" in frontmatter, f"{name}: description needs triggers"
    assert "## Feedback" in text, f"{name}: mandatory Feedback section missing"
    assert f'"skill:{name}"' in text, f"{name}: feedback unit-id must be skill:{name}"
    assert len(text.splitlines()) < MAX_LINES, f"{name}: SKILL.md exceeds {MAX_LINES} lines"


@pytest.mark.contract
@pytest.mark.parametrize("name", PAIR)
def test_c18_pair_member_is_mirrored(name: str):
    mirror = mirror_path(name)
    assert mirror.is_file(), f".specify/skills/{name}/SKILL.md mirror missing"
    assert mirror.read_bytes() == skill_path(name).read_bytes(), f"{name}: mirror drift"


@pytest.mark.contract
@pytest.mark.parametrize("name", PAIR)
def test_c18_pair_member_registered_exactly_once(name: str):
    registry = INSTRUCTIONS.read_text(encoding="utf-8")
    rows = [line for line in registry.splitlines()
            if line.startswith(f"| {name} |")]
    assert len(rows) == 1, f"{name}: expected exactly one registry row, found {len(rows)}"
    assert f"<SKILL:.specify/skills/{name}/SKILL.md>" in rows[0], f"{name}: row missing skill_id"


@pytest.mark.contract
def test_c18_improve_docs_targets_documents_not_the_skill():
    """The improve half refines documentation artifacts; skill self-improvement is improve-skills."""
    text = skill_text("improve-docs")
    assert "improve-skills" in text, \
        "improve-docs must route skill self-improvement to improve-skills"
    assert "one existing document" in text.lower(), \
        "improve-docs must declare a single existing document as its target"


@pytest.mark.contract
def test_c18_improve_docs_does_not_own_structure():
    """Creation, placement, moves and archiving stay with create-docs."""
    text = skill_text("improve-docs")
    assert "create-docs" in text, "improve-docs must name create-docs as the structure owner"
    for obligation in ("Never create, move, rename, or archive", "hand off"):
        assert obligation in text, f"improve-docs must state the boundary obligation: {obligation}"
    assert "never rewrite" in text.lower(), \
        "improve-docs must forbid rewriting decision history"


@pytest.mark.contract
def test_c18_create_docs_keeps_structural_ownership():
    """The create half remains the desired-state/structure authority for the space."""
    text = skill_text("create-docs")
    assert "Desired-State Baseline" in text, "create-docs must keep the desired-state baseline"
    assert "Bootstrap" in text, "create-docs must keep bootstrap ownership"
