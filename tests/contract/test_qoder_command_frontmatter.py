"""Contract tests: Qoder command copies carry a description frontmatter.

Qoder documents `description` as a required frontmatter field of
`.qoder/commands/*.md` (rendered in the slash-command palette), so
generate_commands() prepends ``---\\ndescription: ...\\n---`` sourced from the
template's `short-description:` key (falling back to the full `description:`).
Pins: every template defines a short single-line description (<=50 chars),
every Qoder copy carries a non-empty frontmatter description matching its
template, and the AUTO-GENERATED marker survives below the frontmatter.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES_DIR = ROOT / "templates" / "commands"
QODER_DIR = ROOT / ".qoder" / "commands"

FRONTMATTER_RE = re.compile(r"\A---\ndescription: ([^\n]+)\n---\n")
SHORT_DESCRIPTION_RE = re.compile(r"^short-description:\s*(.+)$", re.MULTILINE)


def test_every_template_has_short_description():
    templates = sorted(TEMPLATES_DIR.glob("*.md"))
    assert templates, "no command templates found"
    for template in templates:
        match = SHORT_DESCRIPTION_RE.search(template.read_text(encoding="utf-8"))
        assert match, f"{template.name} missing frontmatter short-description"
        value = match.group(1).strip()
        assert value, f"{template.name} has empty short-description"
        assert len(value) <= 50, (
            f"{template.name} short-description exceeds 50 chars: {value!r}"
        )


def test_qoder_copies_carry_frontmatter_description():
    copies = sorted(QODER_DIR.glob("speckit.*.md"))
    assert copies, "no qoder command copies found"
    for copy in copies:
        match = FRONTMATTER_RE.match(copy.read_text(encoding="utf-8"))
        assert match, f"{copy.name} missing description frontmatter"
        assert match.group(1).strip(), f"{copy.name} has empty description"


def test_qoder_frontmatter_matches_template():
    for copy in sorted(QODER_DIR.glob("speckit.*.md")):
        stem = copy.name[len("speckit.") : -len(".md")]
        template = TEMPLATES_DIR / f"{stem}.md"
        if not template.is_file():
            continue
        short = SHORT_DESCRIPTION_RE.search(template.read_text(encoding="utf-8"))
        frontmatter = FRONTMATTER_RE.match(copy.read_text(encoding="utf-8"))
        assert short and frontmatter, f"{copy.name} frontmatter/template incomplete"
        assert frontmatter.group(1) == short.group(1).strip(), (
            f"{copy.name} frontmatter description drifted from template"
        )


def test_qoder_copies_keep_generated_marker():
    for copy in sorted(QODER_DIR.glob("speckit.*.md")):
        head = "\n".join(copy.read_text(encoding="utf-8").splitlines()[:5])
        assert "AUTO-GENERATED" in head, f"{copy.name} lost AUTO-GENERATED header"
