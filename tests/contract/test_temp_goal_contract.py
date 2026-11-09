"""Contract tests for a spec-scoped goal (Feature 085, T020/T022).

A goal has a scope, never a "temporary" property: this suite pins the spec-scoped
goal — a definition under `<spec-dir>/goal/<slug>/goal.md` — against the global
archive at `.specify/anchoring/`.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_DIR = REPO_ROOT / ".specify/specs/085-sdd-temporary-goal-team"
GOAL_MD = SPEC_DIR / "goal/085-sdd-temporary-goal-team/goal.md"
GLOBAL_GOAL = REPO_ROOT / ".specify/anchoring/085-sdd-temporary-goal-team"
ENGINE = REPO_ROOT / "scripts/python/goal-utils.py"


def _load_engine():
    spec = importlib.util.spec_from_file_location("goal_utils_temp_goal", ENGINE)
    module = importlib.util.module_from_spec(spec)
    sys.modules["goal_utils_temp_goal"] = module
    spec.loader.exec_module(module)
    return module


goal_utils = _load_engine()


def test_goal_lives_under_the_spec_and_not_the_global_archive():
    assert GOAL_MD.is_file(), f"spec-scoped goal missing: {GOAL_MD}"
    assert not GLOBAL_GOAL.exists(), "a spec-scoped goal must not be written into the global archive"


def test_goal_is_active_with_authored_degree_criteria():
    data = goal_utils.parse_goal(GOAL_MD)
    assert data["status"] == "active"
    assert data["criteria_count"] >= 1
    assert data["objective"].strip()
    for criterion in data["criteria"]:
        assert "SC-" not in criterion, "spec-scoped goal criteria must not copy requirement SC rows"


def test_goal_engine_validates_the_spec_scoped_definition():
    proc = subprocess.run(
        [sys.executable, str(ENGINE), "validate", str(GOAL_MD), "--json"],
        capture_output=True, text=True, cwd=REPO_ROOT)
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["valid"] is True


def test_spec_scope_lists_the_spec_scoped_goal():
    proc = subprocess.run(
        [sys.executable, str(ENGINE), "list", "--scope", "spec",
         "--spec-dir", str(SPEC_DIR), "--json"],
        capture_output=True, text=True, cwd=REPO_ROOT)
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert [row["slug"] for row in payload["goals"]] == ["085-sdd-temporary-goal-team"]


def test_global_scope_does_not_list_the_spec_scoped_goal():
    proc = subprocess.run(
        [sys.executable, str(ENGINE), "list", "--json"],
        capture_output=True, text=True, cwd=REPO_ROOT)
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert "085-sdd-temporary-goal-team" not in [row["slug"] for row in payload["goals"]]


def test_resolve_scope_returns_the_spec_roots():
    proc = subprocess.run(
        [sys.executable, str(ENGINE), "resolve-scope", "--scope", "spec",
         "--spec-dir", str(SPEC_DIR), "--json"],
        capture_output=True, text=True, cwd=REPO_ROOT)
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["scope"] == "spec"
    assert payload["goal_root"] == str(SPEC_DIR / "goal")
    assert payload["team_root"] == str(SPEC_DIR / "team")
