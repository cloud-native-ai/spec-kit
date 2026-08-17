"""Contract tests for focus_target resolution (042-goal-team-creation, T018).

Contract: .specify/specs/042-goal-team-creation/contracts/focus-target-resolution.contract.md

Two faces are pinned here:
- engine face — `resolve_effective_target(team_md_path, explicit_target=None)`
  (resolution order explicit > focus_target > none, declared_focus passthrough,
  malformed-value input-error stop, effective feeding the unchanged
  preview_target_check five-check);
- template face — the three disclosure forms (including the verbatim
  STR-001 "(团队默认)" suffix), the report line source marker, and the
  resolution-order sentence in templates/commands/team.md.

The function is pure resolution: it never judges; verdicts stay with
preview_target_check (038, unchanged).
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts/python/goal-utils.py"
CANONICAL = REPO_ROOT / "templates/commands/team.md"

STR_TEAM_DEFAULT = "(团队默认)"  # [[STR-001]]

pytestmark = pytest.mark.contract


def _engine():
    spec = importlib.util.spec_from_file_location("goal_utils_focus_contract", ENGINE)
    module = importlib.util.module_from_spec(spec)
    sys.modules["goal_utils_focus_contract"] = module
    spec.loader.exec_module(module)
    return module


goal_utils = _engine()


def _team_md(tmp_path: Path, slug: str, frontmatter_lines: list[str]) -> Path:
    team_md = tmp_path / ".specify/teams" / slug / "team.md"
    team_md.parent.mkdir(parents=True)
    body = "---\n" + "\n".join(frontmatter_lines) + "\n---\n\n# team\n"
    team_md.write_text(body, encoding="utf-8")
    return team_md


@pytest.fixture()
def focused_team_md(tmp_path):
    return _team_md(tmp_path, "demo-team", [
        "slug: demo-team",
        "goal_slug: sliced-goal",
        "focus_target: T-002",
    ])


@pytest.fixture()
def bare_team_md(tmp_path):
    return _team_md(tmp_path, "bare-team", [
        "slug: bare-team",
        "goal_slug: sliced-goal",
    ])


# --------------------------------------------------------------------------
# C-1 resolution order: explicit > focus_target > none
# --------------------------------------------------------------------------

def test_explicit_target_wins_over_declared_focus(focused_team_md):
    out = goal_utils.resolve_effective_target(focused_team_md, "T-001")
    assert out["effective"] == "T-001"
    assert out["source"] == "explicit"
    assert out["declared_focus"] == "T-002"


def test_explicit_equal_to_focus_is_still_explicit(focused_team_md):
    out = goal_utils.resolve_effective_target(focused_team_md, "T-002")
    assert out["source"] == "explicit", "no special case for equal values (C-1)"


def test_declared_focus_becomes_the_team_default(focused_team_md):
    out = goal_utils.resolve_effective_target(focused_team_md, None)
    assert out["effective"] == "T-002"
    assert out["source"] == "team-default"
    assert out["declared_focus"] == "T-002"


def test_no_field_and_no_explicit_is_none(bare_team_md):
    out = goal_utils.resolve_effective_target(bare_team_md, None)
    assert out["effective"] is None
    assert out["source"] == "none"
    assert out["declared_focus"] is None


def test_missing_team_file_is_not_found(bare_team_md):
    with pytest.raises(goal_utils.GoalNotFound):
        goal_utils.resolve_effective_target(
            bare_team_md.parent / "nope" / "team.md", None)


# --------------------------------------------------------------------------
# C-1 malformed focus_target: input-error stop, never silently ignored
# --------------------------------------------------------------------------

def test_malformed_focus_value_stops_with_input_error(tmp_path):
    team_md = _team_md(tmp_path, "bad-team", [
        "slug: bad-team",
        "goal_slug: sliced-goal",
        "focus_target: target-2",
    ])
    out = goal_utils.resolve_effective_target(team_md, None)
    assert out["source"] == "input-error", "malformed config MUST stop, not degrade"
    assert out["effective"] is None
    assert "focus_target" in out["message"]


def test_malformed_focus_does_not_override_explicit(tmp_path):
    team_md = _team_md(tmp_path, "bad-team", [
        "slug: bad-team",
        "goal_slug: sliced-goal",
        "focus_target: nope",
    ])
    out = goal_utils.resolve_effective_target(team_md, "T-001")
    assert out["source"] == "explicit", "explicit resolution never reads the field"
    assert out["effective"] == "T-001"


# --------------------------------------------------------------------------
# C-1 the effective value feeds the unchanged five-check
# --------------------------------------------------------------------------

@pytest.fixture()
def repo_with_targets(tmp_path):
    goal_utils.create_goal(
        tmp_path, "sliced-goal", "A broad platform outcome holds.",
        ["平台整体可用性达到 99.9%"],
    )
    path = goal_utils.definition_path(tmp_path, "sliced-goal")
    goal_utils.add_target(path, "切片一成果形语句")
    goal_utils.add_target(path, "切片二成果形语句")
    return tmp_path


def test_effective_default_resolves_ok_through_five_check(repo_with_targets):
    team_md = _team_md(repo_with_targets, "demo-team", [
        "slug: demo-team",
        "goal_slug: sliced-goal",
        "focus_target: T-002",
    ])
    out = goal_utils.resolve_effective_target(team_md, None)
    verdict = goal_utils.preview_target_check(
        repo_with_targets, "demo-team", out["effective"])
    assert verdict["verdict"] == "ok"
    assert verdict["target_id"] == "T-002"


def test_terminal_default_is_intercepted_by_five_check(repo_with_targets):
    goal_utils.set_target_status(
        goal_utils.definition_path(repo_with_targets, "sliced-goal"),
        "T-002", "dropped")
    team_md = _team_md(repo_with_targets, "demo-team", [
        "slug: demo-team",
        "goal_slug: sliced-goal",
        "focus_target: T-002",
    ])
    out = goal_utils.resolve_effective_target(team_md, None)
    verdict = goal_utils.preview_target_check(
        repo_with_targets, "demo-team", out["effective"])
    assert verdict["verdict"] == "target-terminal", "no terminal bypass (C-3)"


def test_dangling_default_is_intercepted_by_five_check(repo_with_targets):
    team_md = _team_md(repo_with_targets, "demo-team", [
        "slug: demo-team",
        "goal_slug: sliced-goal",
        "focus_target: T-099",
    ])
    out = goal_utils.resolve_effective_target(team_md, None)
    verdict = goal_utils.preview_target_check(
        repo_with_targets, "demo-team", out["effective"])
    assert verdict["verdict"] == "dangling"


# --------------------------------------------------------------------------
# C-2 template face: disclosure forms, report marker, resolution order
# --------------------------------------------------------------------------

def _text() -> str:
    return CANONICAL.read_text(encoding="utf-8")


def test_template_names_the_resolver():
    text = _text()
    assert "resolve_effective_target" in text, "the engine resolver must be named"


def test_template_declares_the_resolution_order():
    text = _text()
    assert "显式" in text and "focus_target" in text, (
        "the explicit > focus_target > none order must be stated"
    )


def test_template_carries_the_team_default_disclosure_suffix():
    text = _text()
    assert STR_TEAM_DEFAULT in text, "STR-001 verbatim suffix missing"
    assert f"(open){STR_TEAM_DEFAULT}" in text, (
        "the team-default disclosure form must be the open form plus the suffix"
    )


def test_template_report_line_carries_the_source_marker():
    text = _text()
    assert "**Target 指派**" in text
    assert STR_TEAM_DEFAULT in text, "the report line must carry the source marker"


def test_template_pins_field_less_equivalence():
    text = _text()
    assert "逐字节等价" in text, (
        "field-less teams MUST stay byte-equivalent to pre-042 behavior"
    )


def test_template_pins_focus_target_semantics():
    text = _text()
    assert "focus_target" in text
    assert "预填" in text, "focus_target is a --target prefill, nothing more"
    assert "不是写域" in text or "非写域" in text, (
        "focus_target MUST be declared as not a write-domain statement"
    )
