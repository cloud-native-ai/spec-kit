"""Structure contract tests for the sdd-loop-driver skill (Feature 058).

One test per contract clause of
`.specify/specs/058-sdd-loop-driver/contracts/skill-structure.md`
(C-1..C-13) and `contracts/distribution-and-docs.md` (C-14..C-19),
following the per-clause test convention of test_run_skills_wiring.py.

Clauses are authored incrementally per user story; each story's tests go
red-first (notes/red-first-evidence.md records the red runs).
"""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "skills" / "external" / "sdd-loop-driver"
SKILL_MD = SKILL_DIR / "SKILL.md"

PINNED_H2_SECTIONS = [
    "What This Skill Does",
    "When to Load",
    "The Loop (U0–U6)",
    "Hard Requirements",
    "Discipline Defaults",
    "References",
    "Boundary",
]


def _skill_text() -> str:
    return SKILL_MD.read_text(encoding="utf-8")


def _parse_frontmatter(text: str):
    """Minimal frontmatter parser (no PyYAML per repo convention).

    Returns (fields: dict[str, str], body: str). Raises if no frontmatter.
    """
    if not text.startswith("---"):
        raise AssertionError("SKILL.md has no frontmatter block")
    end = text.find("\n---", 3)
    assert end != -1, "frontmatter block not closed"
    block = text[4:end]
    body = text[end + 4:].lstrip("\n")
    fields = {}
    for line in block.splitlines():
        if not line.strip():
            continue
        key, _, value = line.partition(":")
        value = value.strip()
        # YAML scalar semantics: surrounding quotes are part of the syntax,
        # not the value (precedent skills quote skill_id the same way).
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fields[key.strip()] = value
    return fields, body


def _h2_sections(text: str) -> list:
    return [
        line[3:].strip()
        for line in text.splitlines()
        if line.startswith("## ")
    ]


# ---------------------------------------------------------------- C-1


def test_c1_frontmatter_four_fields():
    fields, _ = _parse_frontmatter(_skill_text())
    assert set(fields) == {
        "name",
        "description",
        "skill_id",
        "classification",
    }, f"frontmatter must carry exactly the four convention fields, got {sorted(fields)}"
    assert fields["name"] == "sdd-loop-driver"
    assert fields["description"], "description must be non-empty"
    assert "使用SDD开发模式" in fields["description"], (
        "description must carry the one-shot-entry trigger phrase"
    )
    assert "无人值守" in fields["description"]
    assert fields["skill_id"] == (
        "<SKILL:.specify/skills/sdd-loop-driver/SKILL.md>"
    )
    assert fields["classification"] == "external"


# ---------------------------------------------------------------- C-2


def test_c2_classification_tension_annotation():
    _, body = _parse_frontmatter(_skill_text())
    head = body[:600]
    assert "依赖轴" in head, (
        "first body paragraph must state the dependency-axis ruling"
    )
    assert "external" in head
    assert "语义耦合" in head or "spec-kit SDD 流程" in head, (
        "annotation must declare the semantic coupling explicitly"
    )


# ---------------------------------------------------------------- C-3


def test_c3_skill_md_section_set():
    sections = _h2_sections(_skill_text())
    assert sections == PINNED_H2_SECTIONS, (
        f"H2 set must equal the pinned routing skeleton, got {sections}"
    )
