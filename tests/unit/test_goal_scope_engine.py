"""Unit tests for the goal/team scope resolver (Feature 084, T010/T012)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts/python/goal-utils.py"


def _load_engine():
    spec = importlib.util.spec_from_file_location("goal_utils_scope", ENGINE)
    module = importlib.util.module_from_spec(spec)
    sys.modules["goal_utils_scope"] = module
    spec.loader.exec_module(module)
    return module


goal_utils = _load_engine()


def _seed(root: Path, *, global_goal: bool = False, global_team: bool = False,
          spec_goal: bool = False, spec_team: bool = False) -> Path:
    if global_goal:
        p = root / ".specify/goal/global-goal/goal.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("# Global Goal\n", encoding="utf-8")
    if global_team:
        p = root / ".specify/teams/global-team/team.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("---\nslug: global-team\n---\n", encoding="utf-8")
    spec = root / ".specify/specs/084-sample"
    if spec_goal:
        p = spec / "goal/spec-goal/goal.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("# Spec Goal\n", encoding="utf-8")
    if spec_team:
        p = spec / "team/spec-team/team.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("---\nslug: spec-team\n---\n", encoding="utf-8")
    return spec


def test_global_scope_paths(tmp_path: Path):
    scope = goal_utils.resolve_scope(tmp_path, "global")
    assert scope.goal_root == tmp_path / ".specify/goal"
    assert scope.team_root == tmp_path / ".specify/teams"
    assert scope.spec_dir is None


def test_spec_scope_paths(tmp_path: Path):
    spec = _seed(tmp_path, spec_goal=True, spec_team=True)
    scope = goal_utils.resolve_scope(tmp_path, "spec", spec)
    assert scope.scope == "spec"
    assert scope.goal_root == spec / "goal"
    assert scope.team_root == spec / "team"
    assert scope.goal_definition("g") == spec / "goal/g/goal.md"
    assert scope.team_definition("t") == spec / "team/t/team.md"


def test_spec_scope_requires_spec_dir(tmp_path: Path):
    with pytest.raises(goal_utils.ScopeError, match="spec-scope-requires-spec-dir"):
        goal_utils.resolve_scope(tmp_path, "spec")


def test_spec_dir_must_live_under_specify_specs(tmp_path: Path):
    outside = tmp_path / "outside"
    outside.mkdir()
    with pytest.raises(goal_utils.ScopeError, match="under .specify/specs"):
        goal_utils.resolve_scope(tmp_path, "spec", outside)


def test_auto_prefers_spec_when_only_spec_exists(tmp_path: Path):
    spec = _seed(tmp_path, spec_goal=True)
    scope = goal_utils.resolve_scope(tmp_path, "auto", spec)
    assert scope.scope == "spec"
    assert scope.goal_root == spec / "goal"


def test_auto_prefers_global_when_only_global_exists(tmp_path: Path):
    _seed(tmp_path, global_goal=True)
    scope = goal_utils.resolve_scope(tmp_path, "auto", tmp_path / ".specify/specs/absent")
    assert scope.scope == "global"
    assert scope.goal_root == tmp_path / ".specify/goal"


def test_auto_is_ambiguous_when_both_exist(tmp_path: Path):
    spec = _seed(tmp_path, global_goal=True, spec_goal=True)
    with pytest.raises(goal_utils.ScopeError, match="scope-ambiguous"):
        goal_utils.resolve_scope(tmp_path, "auto", spec)


def test_auto_with_team_identity_resolves_the_only_candidate(tmp_path: Path):
    _seed(tmp_path, global_team=True, spec_team=True)
    spec = tmp_path / ".specify/specs/084-sample"
    scope = goal_utils.resolve_scope(tmp_path, "auto", spec, team_slug="spec-team")
    assert scope.scope == "spec"
    assert scope.team_root == spec / "team"
