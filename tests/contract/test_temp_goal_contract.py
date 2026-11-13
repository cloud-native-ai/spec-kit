"""Contract tests for an action-level Goal definition (Feature 101, FR-019…FR-027).

Rewritten by Feature 101 (successor of the 085 T020/T022 module and its 094 rewrite):
the temporary/spec-scoped goal concept is now the **action-level Goal** in the goals
archive, while the project-level end state is the **Anchor**. The asserted facts survive
— a goal definition lives in its own archive layer, carries its binding record, stays
active with authored completion conditions and is read through the Goal action group;
the spec-local tree is a migration source that must stay readable under the archive's
`trees/`, and the retired spec scope is still refused.
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
SLUG = "088-speckit-visualization"
GOAL_MD = REPO_ROOT / f".specify/goals/{SLUG}/goal.md"
ANCHOR_LAYER_DIR = REPO_ROOT / f".specify/anchoring/{SLUG}"
ARCHIVED_MD = REPO_ROOT / f".specify/archive/goal-team/trees/{SLUG}/goal/{SLUG}/goal.md"
SPEC_LOCAL_TREE = REPO_ROOT / f".specify/specs/{SLUG}/goal/{SLUG}"
SPEC_DIR = REPO_ROOT / f".specify/specs/{SLUG}"
ENGINE = REPO_ROOT / "scripts/python/goal-utils.py"


def _load_engine():
    spec = importlib.util.spec_from_file_location("goal_utils_action_goal", ENGINE)
    module = importlib.util.module_from_spec(spec)
    sys.modules["goal_utils_action_goal"] = module
    spec.loader.exec_module(module)
    return module


goal_utils = _load_engine()


def test_goal_lives_in_the_goal_archive_and_not_the_spec_tree():
    assert GOAL_MD.is_file(), f"goal-archive definition missing: {GOAL_MD}"
    assert not SPEC_LOCAL_TREE.exists(), (
        "the spec-local goal tree is a migration source, not a live landing point")
    assert not ANCHOR_LAYER_DIR.exists(), (
        "layer separation is absolute: a Goal identity resolves only in .specify/goals/")


def test_goal_is_active_with_authored_completion_conditions():
    data = goal_utils.parse_action_goal(GOAL_MD)
    assert data["status"] == "active"
    assert len(data["conditions"]) >= 1
    assert data["guidance"].strip()
    for condition in data["conditions"]:
        assert "SC-" not in condition, (
            "goal completion conditions must not copy requirement SC rows")


def test_the_definition_carries_its_binding_record():
    meta, _start, _end = goal_utils.read_frontmatter_subset(
        GOAL_MD.read_text(encoding="utf-8"))
    binding = meta.get("binding") or {}
    assert binding.get("owner"), "a goal definition carries its owner"
    assert binding.get("owner_id"), "a goal definition carries the run/actor id"
    assert binding.get("origin") == SLUG, (
        "the migrated definition records its source spec directory as origin")


def test_goal_engine_validates_the_archive_definition():
    proc = subprocess.run([sys.executable, str(ENGINE), "goal-view", SLUG,
                           "--scope", "goals", "--json"],
                          capture_output=True, text=True, cwd=REPO_ROOT)
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["slug"] == SLUG
    assert payload["status"] == "active"


def test_the_archived_source_copy_stays_readable():
    assert ARCHIVED_MD.is_file(), (
        "archive-not-delete: the migrated source stays readable under trees/")


def test_list_names_the_migrated_goal_and_never_the_spec_tree():
    proc = subprocess.run([sys.executable, str(ENGINE), "goal-list", "--json"],
                          capture_output=True, text=True, cwd=REPO_ROOT)
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert SLUG in [row["slug"] for row in payload["goals"]]


def test_resolve_scope_returns_the_archive_roots():
    proc = subprocess.run([sys.executable, str(ENGINE), "resolve-scope", "--scope", "goals",
                           "--spec-dir", str(SPEC_DIR), "--json"],
                          capture_output=True, text=True, cwd=REPO_ROOT)
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["scope"] == "goals"
    assert payload["goals_root"].endswith("/.specify/goals")
    assert payload["anchor_root"].endswith("/.specify/anchoring")
    assert payload["team_root"].endswith("/.specify/teams")


def test_retired_spec_scope_is_refused():
    proc = subprocess.run([sys.executable, str(ENGINE), "goal-list", "--scope", "spec",
                           "--spec-dir", str(SPEC_DIR), "--json"],
                          capture_output=True, text=True, cwd=REPO_ROOT)
    assert proc.returncode == 2
    assert "invalid choice" in (proc.stderr + proc.stdout)
