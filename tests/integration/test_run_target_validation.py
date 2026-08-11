"""Integration tests for run --target preview validation (038-goal-target, T013).

Contract: .specify/specs/038-goal-target/contracts/run-target-assignment.contract.md §2

Fixtures build a bound goal definition + team; every verdict is asserted through
goal-utils' parse path (the engine parse_goal is the single source of truth —
same data layer as the T003 foundational work). Verdicts mirror §2's five steps:
resolve binding, dangling, terminal (review bifurcation), cross-goal, goal terminal.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts/python/goal-utils.py"

pytestmark = pytest.mark.integration


def _engine():
    spec = importlib.util.spec_from_file_location("goal_utils_run_target", ENGINE)
    module = importlib.util.module_from_spec(spec)
    sys.modules["goal_utils_run_target"] = module
    spec.loader.exec_module(module)
    return module


goal_utils = _engine()


@pytest.fixture()
def repo(tmp_path):
    """Bound goal + team: team.md declares goal_slug explicitly."""
    goal_utils.create_goal(
        tmp_path, "demo-goal", "A platform outcome holds.", ["判据一"])
    path = goal_utils.definition_path(tmp_path, "demo-goal")
    goal_utils.add_target(path, "日志组件拆分完成")          # T-001 open
    goal_utils.add_target(path, "指标采集链路独立可部署")    # T-002
    goal_utils.add_target(path, "告警规则全量迁移")          # T-003
    goal_utils.set_target_status(path, "T-002", "done")
    goal_utils.set_target_status(path, "T-003", "dropped")
    team_dir = tmp_path / ".specify/teams/demo-team"
    team_dir.mkdir(parents=True)
    (team_dir / "team.md").write_text(
        "---\nslug: demo-team\nname: Demo Team\ngoal_slug: demo-goal\n---\n\n"
        "## Goal\n\nA platform outcome holds.\n",
        encoding="utf-8",
    )
    return tmp_path


def _check(repo, ref, team="demo-team"):
    return goal_utils.preview_target_check(repo, team, ref)


# --------------------------------------------------------------------------
# step 1 — binding resolution (two levels only)
# --------------------------------------------------------------------------

def test_legal_open_reference_passes_with_binding_metadata(repo):
    result = _check(repo, "T-001")
    assert result["verdict"] == "ok"
    assert result["goal_slug"] == "demo-goal"
    assert result["identity_kind"] == "explicit"
    assert result["statement"] == "日志组件拆分完成"
    assert result["status"] == "open"


def test_inferred_binding_is_used_when_goal_slug_is_absent(repo):
    """Second level: the team slug itself names the definition."""
    goal_utils.create_goal(repo, "infer-team", "Inferred outcome.", [])
    team_dir = repo / ".specify/teams/infer-team"
    team_dir.mkdir(parents=True)
    (team_dir / "team.md").write_text(
        "---\nslug: infer-team\nname: Infer\n---\n\n## Goal\n\nInferred outcome.\n",
        encoding="utf-8",
    )
    result = goal_utils.preview_target_check(repo, "infer-team", "T-999")
    assert result["identity_kind"] == "inferred"
    assert result["goal_slug"] == "infer-team"


def test_definitionless_team_with_target_points_to_migrate(repo):
    """FR-010: --target needs a goal definition; inline goals are not enough."""
    team_dir = repo / ".specify/teams/inline-only"
    team_dir.mkdir(parents=True)
    (team_dir / "team.md").write_text(
        "---\nslug: inline-only\nname: Inline\ngoal: 某个内联目标\n---\n",
        encoding="utf-8",
    )
    result = goal_utils.preview_target_check(repo, "inline-only", "T-001")
    assert result["verdict"] == "no-goal-definition"
    assert "migrate" in result["message"]


# --------------------------------------------------------------------------
# step 2 — dangling reference
# --------------------------------------------------------------------------

def test_dangling_reference_is_rejected_with_the_add_suggestion(repo):
    result = _check(repo, "T-999")
    assert result["verdict"] == "dangling"
    assert "--add" in result["message"], "must propose /speckit.goal targets --add"


# --------------------------------------------------------------------------
# step 3 — terminal reference with the review bifurcation
# --------------------------------------------------------------------------

@pytest.mark.parametrize("ref,state", [("T-002", "done"), ("T-003", "dropped")])
def test_terminal_reference_stops_with_review_guidance(repo, ref, state):
    result = _check(repo, ref)
    assert result["verdict"] == "target-terminal"
    assert result["status"] == state
    message = result["message"]
    assert "复核" in message, "must carry the review-bifurcation guidance"
    assert "--set open" in message, "the reopen path must be named"
    assert "旁路" in message or "bypass" in message.lower(), (
        "must state there is no terminal-execution bypass"
    )


# --------------------------------------------------------------------------
# step 4 — cross-goal qualified reference
# --------------------------------------------------------------------------

def test_qualified_form_matching_the_bound_goal_is_accepted(repo):
    result = _check(repo, "demo-goal.T-001")
    assert result["verdict"] == "ok"


def test_cross_goal_qualified_reference_is_rejected(repo):
    result = _check(repo, "other-goal.T-001")
    assert result["verdict"] == "cross-goal"
    assert "绑定" in result["message"] or "binding" in result["message"].lower()


# --------------------------------------------------------------------------
# step 5 — terminal goal refuses assignment
# --------------------------------------------------------------------------

def test_terminal_goal_refuses_assignment(repo):
    goal_utils.set_status(goal_utils.definition_path(repo, "demo-goal"), "achieved")
    result = _check(repo, "T-001")
    assert result["verdict"] == "goal-terminal"
    assert "只读" in result["message"] or "read-only" in result["message"]


# --------------------------------------------------------------------------
# invariants: the check never mutates the definition or the team file
# --------------------------------------------------------------------------

def test_preview_check_is_read_only(repo):
    goal_path = goal_utils.definition_path(repo, "demo-goal")
    team_path = repo / ".specify/teams/demo-team/team.md"
    before_goal = goal_path.read_bytes()
    before_team = team_path.read_bytes()
    for ref in ("T-001", "T-999", "T-002", "other-goal.T-001"):
        _check(repo, ref)
    assert goal_path.read_bytes() == before_goal
    assert team_path.read_bytes() == before_team


def test_malformed_reference_is_an_input_error(repo):
    result = _check(repo, "not-a-target")
    assert result["verdict"] == "input-error"
