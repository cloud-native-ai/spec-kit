"""Unit tests for the goal/team archive-layer resolver (Feature 084, T010/T012).

Rewritten by Feature 094 (FR-041 / SC-010, disposal row 9): the closed archive-layer
set is `goal` / `teams` / `auto` and the retired position-named members are refused.
"""

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


def _seed(root: Path, *, goal_layer: bool = False, team_layer: bool = False) -> Path:
    """Seed the two archive layers; a spec directory is only an origin input now."""
    if goal_layer:
        p = root / ".specify/anchoring/archive-goal/goal.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("# Archive Goal\n", encoding="utf-8")
    if team_layer:
        p = root / ".specify/teams/archive-team/team.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("---\nslug: archive-team\n---\n", encoding="utf-8")
    spec = root / ".specify/specs/084-sample"
    spec.mkdir(parents=True, exist_ok=True)
    return spec


def test_goal_scope_paths(tmp_path: Path):
    scope = goal_utils.resolve_scope(tmp_path, "goal")
    assert scope.scope == "goal"
    assert scope.goal_root == tmp_path / ".specify/anchoring"
    assert scope.team_root == tmp_path / ".specify/teams"
    assert scope.spec_dir is None


def test_teams_scope_paths(tmp_path: Path):
    spec = _seed(tmp_path)
    scope = goal_utils.resolve_scope(tmp_path, "teams", spec)
    assert scope.scope == "teams"
    assert scope.goal_root == tmp_path / ".specify/anchoring"
    assert scope.team_root == tmp_path / ".specify/teams"
    assert scope.goal_definition("g") == tmp_path / ".specify/anchoring/g/goal.md"
    assert scope.team_definition("t") == tmp_path / ".specify/teams/t/team.md"


@pytest.mark.parametrize("retired", ["spec", "global"])
def test_retired_scopes_are_refused(tmp_path: Path, retired: str):
    spec = _seed(tmp_path)
    with pytest.raises(goal_utils.ScopeError, match="outside the closed set"):
        goal_utils.resolve_scope(tmp_path, retired, spec)


def test_spec_dir_must_live_under_specify_specs(tmp_path: Path):
    outside = tmp_path / "outside"
    outside.mkdir()
    with pytest.raises(goal_utils.ScopeError, match="under .specify/specs/"):
        goal_utils.resolve_scope(tmp_path, "goal", outside)


def test_auto_resolves_the_single_non_empty_goal_layer(tmp_path: Path):
    _seed(tmp_path, goal_layer=True)
    scope = goal_utils.resolve_scope(tmp_path, "auto", tmp_path / ".specify/specs/absent")
    assert scope.scope == "goal"
    assert scope.goal_root == tmp_path / ".specify/anchoring"


def test_auto_resolves_the_single_non_empty_team_layer(tmp_path: Path):
    _seed(tmp_path, team_layer=True)
    scope = goal_utils.resolve_scope(tmp_path, "auto", tmp_path / ".specify/specs/absent")
    assert scope.scope == "teams"
    assert scope.team_root == tmp_path / ".specify/teams"


def test_auto_is_ambiguous_when_both_layers_exist(tmp_path: Path):
    _seed(tmp_path, goal_layer=True, team_layer=True)
    with pytest.raises(goal_utils.ScopeError, match="scope-ambiguous"):
        goal_utils.resolve_scope(tmp_path, "auto")


def test_auto_with_team_identity_resolves_the_only_candidate(tmp_path: Path):
    _seed(tmp_path, team_layer=True)
    scope = goal_utils.resolve_scope(tmp_path, "auto", None, team_slug="archive-team")
    assert scope.scope == "teams"
    assert scope.team_root == tmp_path / ".specify/teams"
