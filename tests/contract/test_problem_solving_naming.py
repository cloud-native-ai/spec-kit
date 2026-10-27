"""Contract tests for the Root-Cause Problem Solving and Grounded Naming constraints.

Guards three rules across their landing surfaces:
  1. no symptom suppression + judge success at the whole-run level (constitution X / live VI);
  2. naming priority: user > project convention > sibling imitation > own choice (Grounded Naming);
  3. under version control, delete instead of keeping `.bak` / `.backup` copies (constitution X / live VI).

Surfaces: both constitution files, both instructions templates (+ live), and the
generator skill's MUST-include list.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
TPL = ROOT / "templates" / "constitution-template.md"
TPL_MIRROR = ROOT / ".specify" / "templates" / "constitution-template.md"
LIVE = ROOT / ".specify" / "memory" / "constitution.md"
INSTR_TPL = ROOT / "templates" / "instructions-template.md"
INSTR_MIRROR = ROOT / ".specify" / "templates" / "instructions-template.md"
INSTR_LIVE = ROOT / ".specify" / "instructions.md"
SKILL = ROOT / "skills" / "internal" / "manage-constitution" / "SKILL.md"

NAMING_TITLE = "Grounded Naming"
REMEDIATION_TPL = "Non-Destructive Remediation"
REMEDIATION_LIVE = "Continuous Quality & Observability"
SECTIONS = ("## Root-Cause Problem Solving", "## Grounded Naming")

PRINCIPLE_RE = re.compile(r"^### [IVXLC0-9]+\. (.+)$", re.M)


def _text(path: Path) -> str:
    assert path.is_file(), f"missing file: {path}"
    return path.read_text(encoding="utf-8")


def _flat(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def _principle_block(text: str, title: str) -> str:
    m = re.search(
        rf"^### [IVXLC0-9]+\. {re.escape(title)}\s*$(.*?)(?=^### |^## |\Z)",
        text, re.M | re.S,
    )
    assert m, f"principle {title!r} not found"
    return m.group(0)


def _section(text: str, heading: str) -> str:
    lines = text.splitlines()
    start = next((i for i, ln in enumerate(lines) if ln.strip() == heading), None)
    assert start is not None, f"section heading {heading!r} not found"
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## ") or lines[i].startswith("# "):
            end = i
            break
    return "\n".join(lines[start:end])


def _assert_remediation_rules(block: str) -> None:
    flat = _flat(block)
    for needle in (
        "commenting out the code",
        "skipping or muting a failing command",
        "whole-run level",
        ".bak",
        ".backup",
    ):
        assert needle in flat, f"remediation block missing {needle!r}"
    assert re.search(r"history is an unambiguous backup", flat), (
        "the version-control rule must state why history beats a .bak copy"
    )


def test_template_remediation_blocks_symptom_suppression_and_backup_files():
    _assert_remediation_rules(_principle_block(_text(TPL), REMEDIATION_TPL))


def test_live_quality_principle_carries_both_rules():
    _assert_remediation_rules(_principle_block(_text(LIVE), REMEDIATION_LIVE))


@pytest.mark.parametrize("path", [TPL, LIVE], ids=["template", "live"])
def test_grounded_naming_lands_on_both_sides(path: Path):
    block = _principle_block(_text(path), NAMING_TITLE)
    flat = _flat(block)
    assert re.search(r"first available source", flat), (
        "the principle must state that the first available source decides"
    )
    order = [
        flat.find("User instruction"),
        flat.find("Project convention"),
        flat.find("Sibling imitation"),
        flat.find("Own choice"),
    ]
    assert all(i >= 0 for i in order), f"a priority level is missing: {order}"
    assert order == sorted(order), "the priority levels are out of order"
    assert "every reference" in flat, (
        "a higher-priority name must be carried through every reference"
    )


def test_generator_must_include_lists_grounded_naming():
    assert re.search(r"^  - \*\*Grounded Naming\*\* —", _text(SKILL), re.M), (
        "the constitution generator must carry Grounded Naming in its MUST-include list"
    )


@pytest.mark.parametrize(
    "path", [INSTR_TPL, INSTR_MIRROR, INSTR_LIVE],
    ids=["template", "mirror", "live"],
)
def test_instructions_carry_both_ambient_sections(path: Path):
    text = _text(path)
    for heading in SECTIONS:
        assert heading in text, f"{heading!r} missing from {path.name}"
    root_cause = _flat(_section(text, "## Root-Cause Problem Solving"))
    assert "Symptom suppression" in root_cause
    assert ".bak" in root_cause and "history" in root_cause
    naming = _flat(_section(text, "## Grounded Naming"))
    for needle in ("user instruction", "project convention", "same-kind siblings"):
        assert needle in naming.lower(), f"ambient naming section missing {needle!r}"


def test_template_mirrors_are_in_sync():
    assert TPL.read_bytes() == TPL_MIRROR.read_bytes(), (
        "templates/constitution-template.md drifted from its .specify mirror"
    )
    assert INSTR_TPL.read_bytes() == INSTR_MIRROR.read_bytes(), (
        "templates/instructions-template.md drifted from its .specify mirror"
    )
