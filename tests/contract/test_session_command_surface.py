"""Structural contract tests for the /speckit.session command surface (039, T005).

Contract: .specify/specs/039-session-export/contracts/session-command.contract.md

Template-only artifact: pins the export subcommand grammar, the --name
mandatory discipline, the four preview-gate disclosures, the same-name
interactive-override rule (no --force bypass), and the delegation-to-skill
discipline, plus per-tool copy parity derived from the real copy dirs.
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

CANONICAL = REPO_ROOT / "templates/commands/session.md"
MIRROR = REPO_ROOT / ".specify/templates/commands/session.md"

#: Derived from the real per-tool copy trees (pin hygiene: no phantom paths).
PER_TOOL_COPIES = [
    d / name
    for d, name in [
        (REPO_ROOT / ".claude/commands", "speckit.session.md"),
        (REPO_ROOT / ".github/prompts", "speckit.session.prompt.md"),
        (REPO_ROOT / ".qoder/commands", "speckit.session.md"),
        (REPO_ROOT / ".opencode/command", "speckit.session.md"),
    ]
]

pytestmark = pytest.mark.contract


def test_canonical_source_exists():
    assert CANONICAL.is_file(), f"command source of truth missing: {CANONICAL}"


def test_canonical_has_frontmatter_with_a_description():
    text = CANONICAL.read_text(encoding="utf-8")
    assert text.startswith("---\n"), "command template must open with frontmatter"
    head = text.split("---", 2)[1]
    assert "description:" in head


# --------------------------------------------------------------------------
# §1 grammar
# --------------------------------------------------------------------------

def test_export_grammar_line_present():
    text = CANONICAL.read_text(encoding="utf-8")
    assert "export" in text
    for flag in ("--name", "--session", "--tool", "--verify"):
        assert flag in text, f"export grammar missing {flag}"


def test_name_is_mandatory_and_never_auto_generated():
    text = CANONICAL.read_text(encoding="utf-8")
    assert "必填" in text, "--name mandatory discipline must be stated"


# --------------------------------------------------------------------------
# §2 preview gate disclosures
# --------------------------------------------------------------------------

@pytest.mark.parametrize("element", ["工具", "会话", "目标", "规模"])
def test_preview_gate_discloses_the_four_elements(element):
    text = CANONICAL.read_text(encoding="utf-8")
    assert element in text, f"preview gate missing disclosure element: {element}"


def test_preview_confirm_execute_gate_declared():
    text = CANONICAL.read_text(encoding="utf-8").lower()
    assert "preview" in text and "confirm" in text


# --------------------------------------------------------------------------
# §3 same-name conflict
# --------------------------------------------------------------------------

def test_same_name_conflict_uses_interactive_override():
    text = CANONICAL.read_text(encoding="utf-8")
    assert "覆盖" in text, "override rule must be stated"
    assert "--force" not in text, "no bypass flag may exist or be mentioned"


# --------------------------------------------------------------------------
# delegation discipline
# --------------------------------------------------------------------------

def test_command_delegates_to_the_skill():
    text = CANONICAL.read_text(encoding="utf-8")
    assert "export-session" in text, "must delegate to skills/export-session"


# --------------------------------------------------------------------------
# mirror + per-tool copy parity
# --------------------------------------------------------------------------

def test_mirror_is_byte_identical():
    assert MIRROR.is_file(), f"mirror missing: {MIRROR}"
    assert MIRROR.read_bytes() == CANONICAL.read_bytes(), (
        "run scripts/python/sync-mirrors.py --write"
    )


@pytest.mark.parametrize("path", PER_TOOL_COPIES, ids=lambda p: p.name)
def test_per_tool_copy_exists_and_carries_the_grammar(path):
    assert path.is_file(), f"generated copy missing: {path}"
    text = path.read_text(encoding="utf-8")
    assert "AUTO-GENERATED" in text
    assert "--name" in text and "export" in text
