"""Structural contract tests for run --target assignment (038-goal-target, T012).

Contract: .specify/specs/038-goal-target/contracts/run-target-assignment.contract.md

US2 lives in the command template: the preview validation, the gate disclosure,
and the report field are authored instructions. This suite pins that the template
carries every normative element the contract declares — grammar line, the
five-step preview, both disclosure forms, the report field, and the explicit
no-terminal-bypass constraint. Copy parity derives from the existing goal-surface
fixture style (no second hard-coded copy list).
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

CANONICAL = REPO_ROOT / "templates/commands/team.md"
PER_TOOL_COPIES = (
    REPO_ROOT / ".claude/commands/speckit.team.md",
    REPO_ROOT / ".github/prompts/speckit.team.prompt.md",
    REPO_ROOT / ".qoder/commands/speckit.team.md",
    REPO_ROOT / ".opencode/command/speckit.team.md",
)

pytestmark = pytest.mark.contract


def test_canonical_exists():
    assert CANONICAL.is_file(), f"command source of truth missing: {CANONICAL}"


# test_mirror_is_byte_identical removed 2026-08-17: the .specify/templates/commands/
# mirror is retired — per-tool copies are generated straight from templates/commands/.


# --------------------------------------------------------------------------
# §1 parameter grammar
# --------------------------------------------------------------------------

def test_run_mode_declares_the_target_parameter_grammar():
    text = CANONICAL.read_text(encoding="utf-8")
    assert "--target" in text, "run mode must accept the --target parameter"
    assert "T-<nnn>" in text or "T-nnn" in text, "local form grammar must appear"
    assert "<goal-slug>.T-" in text or "goal-slug}.T-" in text, (
        "qualified form grammar must appear"
    )


def test_no_target_regression_is_declared_byte_equivalent():
    text = CANONICAL.read_text(encoding="utf-8")
    assert "逐字节" in text or "byte-equivalent" in text.lower(), (
        "SC-002: the no-target path must be declared byte-equivalent"
    )


def test_inline_goal_team_without_definition_points_to_migrate():
    text = CANONICAL.read_text(encoding="utf-8")
    assert "migrate" in text, (
        "FR-010: a --target on a definition-less team must point to /speckit.goal migrate"
    )


# --------------------------------------------------------------------------
# §2 five-step preview validation
# --------------------------------------------------------------------------

def test_preview_declares_all_five_checks():
    text = CANONICAL.read_text(encoding="utf-8")
    for needle in ("悬空", "终态", "跨 goal", "两级身份解析", "只读"):
        assert needle in text, f"preview validation misses: {needle}"


def test_preview_names_goal_utils_parse_as_the_source_of_truth():
    text = CANONICAL.read_text(encoding="utf-8")
    assert "goal-utils" in text, (
        "the engine parse path must be named as the single source of truth"
    )


def test_dangling_reference_proposes_the_add_path():
    text = CANONICAL.read_text(encoding="utf-8")
    assert "targets" in text and "--add" in text, (
        "dangling refs must propose /speckit.goal targets --add"
    )


# --------------------------------------------------------------------------
# §3 gate disclosure lines
# --------------------------------------------------------------------------

def test_disclosure_line_forms_are_pinned():
    text = CANONICAL.read_text(encoding="utf-8")
    assert "本次 Target:" in text, "disclosure line prefix missing"
    assert "本次 Target: 无" in text, "the no-target disclosure form missing"


# --------------------------------------------------------------------------
# §4 run report field
# --------------------------------------------------------------------------

def test_report_carries_the_target_assignment_field():
    text = CANONICAL.read_text(encoding="utf-8")
    assert "**Target 指派**" in text, "report field name missing"


# --------------------------------------------------------------------------
# §5 invariants: no rebinding, no bypass
# --------------------------------------------------------------------------

def test_binding_and_delivery_invariants_are_stated():
    text = CANONICAL.read_text(encoding="utf-8")
    for needle in ("绑定", "身份解析", "交付目录"):
        assert needle in text, f"invariant not stated: {needle}"


def test_no_terminal_execution_bypass_is_declared():
    text = CANONICAL.read_text(encoding="utf-8")
    assert "终态执行旁路" in text, "the no-bypass constraint must be explicit"


def test_review_bifurcation_is_present():
    text = CANONICAL.read_text(encoding="utf-8")
    assert "复核" in text, "the terminal review bifurcation guidance must appear"


# --------------------------------------------------------------------------
# per-tool copies carry the --target content
# --------------------------------------------------------------------------

@pytest.mark.parametrize("path", PER_TOOL_COPIES, ids=lambda p: p.name)
def test_per_tool_copies_carry_target_validation(path):
    assert path.is_file(), f"generated copy missing: {path}"
    text = path.read_text(encoding="utf-8")
    assert "--target" in text, f"{path.name} lacks --target content"
    assert "本次 Target:" in text, f"{path.name} lacks the disclosure line"
