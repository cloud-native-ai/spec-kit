"""Structural contract tests for the goal-based create branch (042-goal-team-creation, T002).

Contract: .specify/specs/042-goal-team-creation/contracts/goal-based-create.contract.md

US1 lives in the command template: branch recognition (C-1), definition load and
the two rejections (C-2), the four-element analysis disclosure (C-3), the
single-team derivation (C-4 subset), and the landing invariants (C-5). These are
authored instructions, so this suite pins that the template carries every
normative element the contract declares — engine command lines, the verbatim
STR-003 error prefix, the four analysis elements, advisory-not-gate wording, and
the goal.md zero-write red line. Copy parity derives the copy list from the tree
(no second hard-coded list; only tool dirs that actually carry copies are pinned).
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

CANONICAL = REPO_ROOT / "templates/commands/team.md"

# Per-tool copy list is derived from the tree: the six assistant dirs the regen
# script fans out to, filtered down to those that actually hold a copy today.
_COPY_CANDIDATES = (
    REPO_ROOT / ".claude/commands/speckit.team.md",
    REPO_ROOT / ".github/prompts/speckit.team.prompt.md",
    REPO_ROOT / ".opencode/command/speckit.team.md",
    REPO_ROOT / ".qoder/commands/speckit.team.md",
    REPO_ROOT / ".hermes/commands/speckit.team.md",
    REPO_ROOT / ".codex/commands/speckit.team.md",
)
PER_TOOL_COPIES = tuple(p for p in _COPY_CANDIDATES if p.is_file())

STR_GOAL_UNDEFINED = "goal 未定义:"  # [[STR-003]]

pytestmark = pytest.mark.contract


def _text() -> str:
    return CANONICAL.read_text(encoding="utf-8")


def test_canonical_exists():
    assert CANONICAL.is_file(), f"command source of truth missing: {CANONICAL}"


# --------------------------------------------------------------------------
# C-1 branch recognition: deterministic, engine-enumerated, exact match
# --------------------------------------------------------------------------

def test_recognition_is_driven_by_the_engine_enumeration():
    text = _text()
    assert "list --json" in text, (
        "branch recognition MUST be driven by `goal-utils.py list --json`"
    )
    assert "goal-utils.py" in text


def test_recognition_requires_exact_match_with_no_semantic_guessing():
    text = _text()
    assert "精确匹配" in text, "exact-match wording missing"
    assert "语义猜测" in text, "the no-semantic-guessing constraint missing"


def test_near_miss_is_not_a_hit_and_falls_back_to_free_text():
    text = _text()
    assert "近似" in text and "不构成命中" in text, (
        "near-miss-is-not-a-hit rule missing"
    )
    assert "自由文本" in text, "free-text fallback path missing"


def test_branch_entry_requires_user_confirmation():
    text = _text()
    assert "确认" in text, "user confirmation gate before entering the branch missing"


# --------------------------------------------------------------------------
# C-2 definition load and the two rejections
# --------------------------------------------------------------------------

def test_definition_load_parses_and_restates_to_the_user():
    text = _text()
    assert "parse_goal" in text, "engine parse must be named as the loader"
    assert "复述" in text, "the restate-to-user confirmation step missing"


def test_dangling_reference_error_prefix_is_verbatim():
    text = _text()
    assert STR_GOAL_UNDEFINED in text, "STR-003 verbatim prefix missing"


def test_dangling_reference_points_to_goal_create_and_never_degrades():
    text = _text()
    assert "/speckit.goal create" in text, "the recovery pointer missing"
    assert "内联" in text, "the no-silent-degradation-to-inline rule missing"
    assert "零产物" in text or "零写入" in text, "zero-artifact rule missing"


def test_terminal_goal_is_explicitly_rejected_in_create():
    text = _text()
    assert "achieved" in text and "abandoned" in text, (
        "terminal states must be named in the create-side rejection"
    )
    assert "拒绝" in text, "explicit rejection wording missing"


# --------------------------------------------------------------------------
# C-3 four-element analysis disclosure (advisory, not a gate)
# --------------------------------------------------------------------------

def test_analysis_covers_the_four_elements():
    text = _text()
    for element in ("维度", "判据覆盖", "既有 Target", "可达成性"):
        assert element in text, f"analysis element missing: {element}"


def test_analysis_states_rationale_per_element():
    text = _text()
    assert "理由" in text, "per-element rationale requirement missing"


def test_missing_criteria_must_be_declared_not_invented():
    text = _text()
    assert "None provided." in text, (
        "the missing-criteria marker must be declared verbatim, never invented"
    )


def test_analysis_conclusion_is_advisory_not_a_gate():
    text = _text()
    assert "非门禁" in text or ("建议" in text and "裁决" in text), (
        "advisory-not-gate wording missing: the user adjudicates single-team vs decompose"
    )


# --------------------------------------------------------------------------
# C-4 (single-team subset): derivation from the loaded goal
# --------------------------------------------------------------------------

def test_single_team_declares_goal_slug_and_reports_mismatch():
    text = _text()
    assert "goal_slug" in text, "goal_slug reference binding missing"
    assert "定义权威" in text, "definition-authority rule for inline goal missing"


def test_derivation_reasons_enter_the_confirmation_preview():
    text = _text()
    assert "派生理由" in text, "derivation reasons must enter the confirmation preview"


def test_preset_matching_reuses_the_existing_mechanism():
    text = _text()
    assert "match-team-preset.py" in text, "preset matching script must be reused"


# --------------------------------------------------------------------------
# C-5 landing invariants: team.md only, goal.md zero-write
# --------------------------------------------------------------------------

def test_goal_md_zero_write_red_line_is_stated():
    text = _text()
    assert "goal.md" in text, "goal.md write-face rule missing"
    assert "零写入" in text or "零写" in text, (
        "the create branch MUST declare zero writes to goal.md"
    )


# --------------------------------------------------------------------------
# per-tool copies carry the goal-based branch
# --------------------------------------------------------------------------

@pytest.mark.parametrize("path", PER_TOOL_COPIES, ids=lambda p: p.name)
def test_per_tool_copies_carry_the_goal_based_branch(path):
    assert path.is_file(), f"generated copy missing: {path}"
    text = path.read_text(encoding="utf-8")
    assert STR_GOAL_UNDEFINED in text, f"{path.name} lacks the STR-003 prefix"
    assert "判据覆盖" in text, f"{path.name} lacks the analysis disclosure"
