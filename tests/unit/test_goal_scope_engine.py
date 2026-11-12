"""Unit tests for the definition archive-layer resolver (Feature 084, T010/T012).

Rewritten by Feature 101 (FR-029…FR-031): the closed layer set is `anchor` /
`goals` / `teams` / `auto`, each layer resolves its own filename, and the retired
position-named member `goal` is refused like the other retired names.
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


def _seed(root: Path, *, anchor_layer: bool = False, goal_layer: bool = False,
          team_layer: bool = False) -> Path:
    """Seed the three archive layers; a spec directory is only an origin input now."""
    if anchor_layer:
        p = root / ".specify/anchoring/archive-anchor/anchor.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("# Anchor: archive-anchor\n", encoding="utf-8")
    if goal_layer:
        p = root / ".specify/goals/archive-goal/goal.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("# Goal: archive-goal\n", encoding="utf-8")
    if team_layer:
        p = root / ".specify/teams/archive-team/team.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("---\nslug: archive-team\n---\n", encoding="utf-8")
    spec = root / ".specify/specs/084-sample"
    spec.mkdir(parents=True, exist_ok=True)
    return spec


def test_anchor_scope_paths(tmp_path: Path):
    scope = goal_utils.resolve_scope(tmp_path, "anchor")
    assert scope.scope == "anchor"
    assert scope.anchor_root == tmp_path / ".specify/anchoring"
    assert scope.goals_root == tmp_path / ".specify/goals"
    assert scope.team_root == tmp_path / ".specify/teams"
    assert scope.spec_dir is None


def test_teams_scope_paths(tmp_path: Path):
    spec = _seed(tmp_path)
    scope = goal_utils.resolve_scope(tmp_path, "teams", spec)
    assert scope.scope == "teams"
    assert scope.anchor_root == tmp_path / ".specify/anchoring"
    assert scope.team_root == tmp_path / ".specify/teams"
    assert scope.anchor_definition("g") == tmp_path / ".specify/anchoring/g/anchor.md"
    assert scope.goal_definition("g") == tmp_path / ".specify/goals/g/goal.md"
    assert scope.team_definition("t") == tmp_path / ".specify/teams/t/team.md"


@pytest.mark.parametrize("retired", ["goal", "spec", "global"])
def test_retired_scopes_are_refused(tmp_path: Path, retired: str):
    spec = _seed(tmp_path)
    with pytest.raises(goal_utils.ScopeError, match="outside the closed set"):
        goal_utils.resolve_scope(tmp_path, retired, spec)


def test_spec_dir_must_live_under_specify_specs(tmp_path: Path):
    outside = tmp_path / "outside"
    outside.mkdir()
    with pytest.raises(goal_utils.ScopeError, match="under .specify/specs/"):
        goal_utils.resolve_scope(tmp_path, "anchor", outside)


def test_auto_resolves_the_single_non_empty_anchor_layer(tmp_path: Path):
    _seed(tmp_path, anchor_layer=True)
    scope = goal_utils.resolve_scope(tmp_path, "auto", tmp_path / ".specify/specs/absent")
    assert scope.scope == "anchor"
    assert scope.anchor_root == tmp_path / ".specify/anchoring"


def test_auto_resolves_the_single_non_empty_goal_layer(tmp_path: Path):
    _seed(tmp_path, goal_layer=True)
    scope = goal_utils.resolve_scope(tmp_path, "auto", tmp_path / ".specify/specs/absent")
    assert scope.scope == "goals"
    assert scope.goals_root == tmp_path / ".specify/goals"


def test_auto_resolves_the_single_non_empty_team_layer(tmp_path: Path):
    _seed(tmp_path, team_layer=True)
    scope = goal_utils.resolve_scope(tmp_path, "auto", tmp_path / ".specify/specs/absent")
    assert scope.scope == "teams"
    assert scope.team_root == tmp_path / ".specify/teams"


def test_auto_is_ambiguous_when_both_layers_exist(tmp_path: Path):
    _seed(tmp_path, anchor_layer=True, team_layer=True)
    with pytest.raises(goal_utils.ScopeError, match="scope-ambiguous"):
        goal_utils.resolve_scope(tmp_path, "auto")


def test_auto_with_team_identity_resolves_the_only_candidate(tmp_path: Path):
    _seed(tmp_path, team_layer=True)
    scope = goal_utils.resolve_scope(tmp_path, "auto", None, "archive-team")
    assert scope.scope == "teams"
    assert scope.team_root == tmp_path / ".specify/teams"
