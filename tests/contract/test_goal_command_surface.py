"""Structural contract tests for the /speckit.goal command surface (T019).

Contract: .specify/specs/037-goal-registry/contracts/goal-command.contract.md

Pins the delivery fan-out (source → mirror → 5 per-tool copies), the reference doc,
the concept-authority link discipline, and FR-021's option-collision prohibition.
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

CANONICAL = REPO_ROOT / "templates/commands/goal.md"
MIRROR = REPO_ROOT / ".specify/templates/commands/goal.md"
PER_TOOL_COPIES = (
    REPO_ROOT / ".claude/commands/speckit.goal.md",
    REPO_ROOT / ".github/prompts/speckit.goal.prompt.md",
    REPO_ROOT / ".qoder/commands/speckit.goal.md",
    REPO_ROOT / ".opencode/command/speckit.goal.md",
    REPO_ROOT / ".qwen/commands/speckit.goal.toml",
)
REFERENCE_DOC = REPO_ROOT / "docs/reference/commands/goal.md"
ENGINE = REPO_ROOT / "scripts/python/goal-utils.py"
ENGINE_MIRROR = REPO_ROOT / ".specify/scripts/python/goal-utils.py"

AUTHORITY = ".specify/shared/definitions/goal-definitions.md"

pytestmark = pytest.mark.contract


def test_canonical_source_exists():
    assert CANONICAL.is_file(), f"command source of truth missing: {CANONICAL}"


def test_canonical_has_frontmatter_with_a_description():
    text = CANONICAL.read_text(encoding="utf-8")
    assert text.startswith("---\n"), "command template must open with frontmatter"
    head = text.split("---", 2)[1]
    assert "description:" in head


def test_mirror_is_byte_identical():
    assert MIRROR.is_file(), f"mirror missing: {MIRROR}"
    assert MIRROR.read_bytes() == CANONICAL.read_bytes(), (
        "run scripts/python/sync-mirrors.py --write"
    )


@pytest.mark.parametrize("path", PER_TOOL_COPIES, ids=lambda p: p.name)
def test_per_tool_copy_exists_and_is_generated(path):
    assert path.is_file(), f"generated copy missing: {path}"
    text = path.read_text(encoding="utf-8")
    assert "AUTO-GENERATED" in text, f"{path.name} lacks the AUTO-GENERATED header"
    assert "templates/commands/goal.md" in text, (
        f"{path.name} does not name its source template"
    )


def test_qwen_copy_uses_the_toml_form():
    qwen = REPO_ROOT / ".qwen/commands/speckit.goal.toml"
    assert qwen.suffix == ".toml"
    assert "prompt" in qwen.read_text(encoding="utf-8")


def test_reference_doc_exists():
    assert REFERENCE_DOC.is_file(), f"reference doc missing: {REFERENCE_DOC}"


def test_reference_doc_joins_the_one_per_command_convention():
    """docs/reference/commands/ holds one file per command and no index."""
    docs = sorted(p.name for p in (REPO_ROOT / "docs/reference/commands").glob("*.md"))
    assert "goal.md" in docs
    assert "README.md" not in docs, "nested README.md is a reserved-name violation"


def test_engine_exists_with_its_mirror():
    assert ENGINE.is_file()
    assert ENGINE_MIRROR.is_file(), "run sync-mirrors.py --write"
    assert ENGINE.read_bytes() == ENGINE_MIRROR.read_bytes()


# --------------------------------------------------------------------------
# FR-021 — no colliding option name
# --------------------------------------------------------------------------

def test_no_new_goal_option_is_introduced():
    """`--goal` is already claimed with two different meanings, so identity is positional."""
    for path in (CANONICAL, ENGINE):
        text = path.read_text(encoding="utf-8")
        assert "--goal " not in text and '"--goal"' not in text, (
            f"{path.name} introduces a --goal option, colliding with "
            "build-summary-input.py (goal identity) and match-team-preset.py (goal text)"
        )


def test_engine_takes_identity_positionally():
    text = ENGINE.read_text(encoding="utf-8")
    assert 'add_argument("slug")' in text, (
        "goal identity must be a positional argument, not an option"
    )


# --------------------------------------------------------------------------
# Concept-authority discipline (GC-8)
# --------------------------------------------------------------------------

def test_command_links_to_the_concept_authority():
    text = CANONICAL.read_text(encoding="utf-8")
    assert AUTHORITY in text or "goal-definitions.md" in text, (
        "the command must link to the concept authority"
    )


def test_command_does_not_restate_the_concept():
    """GC-8: link, never fork. A second account of the concept is the defect."""
    text = CANONICAL.read_text(encoding="utf-8")
    assert "never restate" in text.lower() or "never restated" in text.lower(), (
        "the command should declare the link-not-restate rule explicitly"
    )


# --------------------------------------------------------------------------
# Mode surface and the confirmation gate
# --------------------------------------------------------------------------

@pytest.mark.parametrize("mode", ["create", "view", "modify", "migrate", "coordinate"])
def test_every_mode_is_documented(mode):
    assert mode in CANONICAL.read_text(encoding="utf-8")


def test_preview_confirm_gate_is_declared():
    text = CANONICAL.read_text(encoding="utf-8").lower()
    assert "confirm" in text and "preview" in text, (
        "the command must declare a preview -> confirm gate before writes"
    )


def test_view_mode_is_declared_read_only():
    text = CANONICAL.read_text(encoding="utf-8")
    assert "read-only" in text or "nothing" in text


def test_wrap_up_steps_present():
    """A complex process-interaction command carries Feedback + Documentation."""
    text = CANONICAL.read_text(encoding="utf-8")
    assert "## Feedback" in text
    assert "## Documentation" in text
    assert "/speckit.goal" in text, "feedback unit-id must be the command id"
