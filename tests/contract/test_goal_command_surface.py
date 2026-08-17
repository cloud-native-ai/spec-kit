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
PER_TOOL_COPIES = (
    REPO_ROOT / ".claude/commands/speckit.goal.md",
    REPO_ROOT / ".github/prompts/speckit.goal.prompt.md",
    REPO_ROOT / ".qoder/commands/speckit.goal.md",
    REPO_ROOT / ".opencode/command/speckit.goal.md",
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


# test_mirror_is_byte_identical removed 2026-08-17: the .specify/templates/commands/
# mirror is retired — per-tool copies are generated straight from templates/commands/.


@pytest.mark.parametrize("path", PER_TOOL_COPIES, ids=lambda p: p.name)
def test_per_tool_copy_exists_and_is_generated(path):
    assert path.is_file(), f"generated copy missing: {path}"
    text = path.read_text(encoding="utf-8")
    assert "AUTO-GENERATED" in text, f"{path.name} lacks the AUTO-GENERATED header"
    assert "templates/commands/goal.md" in text, (
        f"{path.name} does not name its source template"
    )


def test_copies_use_the_md_form():
    for path in PER_TOOL_COPIES:
        assert path.suffix == ".md", f"{path.name} should use .md form"


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


# --------------------------------------------------------------------------
# 038 — the targets action group on the command surface
# --------------------------------------------------------------------------

def test_targets_mode_row_is_documented():
    text = CANONICAL.read_text(encoding="utf-8")
    assert "| `targets` |" in text, "Modes table must carry a targets row"


def test_engine_invocation_examples_cover_the_targets_action_group():
    text = CANONICAL.read_text(encoding="utf-8")
    for example in ("targets <goal-slug> --add", "targets <goal-slug> --list",
                    "targets <goal-slug> --set"):
        assert example in text, f"engine example missing: {example}"


def test_targets_routes_through_the_single_authoring_entry():
    """modify-intent routing: no second authoring surface for ## Targets."""
    text = CANONICAL.read_text(encoding="utf-8")
    assert "modify-intent route" in text


def test_review_bifurcation_is_declared_without_an_execution_bypass():
    text = CANONICAL.read_text(encoding="utf-8")
    assert "review bifurcation" in text
    assert "no terminal-execution bypass" in text


@pytest.mark.parametrize("path", PER_TOOL_COPIES, ids=lambda p: p.name)
def test_per_tool_copies_carry_the_targets_content(path):
    """Derived from the same PER_TOOL_COPIES fixture — no second copy list."""
    text = path.read_text(encoding="utf-8")
    assert "targets <goal-slug> --add" in text, f"{path.name} lacks targets content"


def test_engine_implements_the_targets_action():
    text = ENGINE.read_text(encoding="utf-8")
    assert 'add_parser("targets"' in text
