"""Contract tests for a migrated goal definition (Feature 085, T020/T022).

Rewritten by Feature 094 (FR-041 / SC-010, disposal row 2): the temporary/spec-scoped
goal concept is replaced by the binding model. The asserted facts survive — a goal
definition lives in the unified archive, carries its owner, stays active with authored
criteria and is refused when the retired scope is requested; the spec-local tree is a
migration source that must stay readable under the archive's `trees/`.
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
SLUG = "085-sdd-temporary-goal-team"
GOAL_MD = REPO_ROOT / f".specify/anchoring/{SLUG}/goal.md"
ARCHIVED_MD = REPO_ROOT / f".specify/archive/goal-team/trees/{SLUG}/goal/{SLUG}/goal.md"
SPEC_LOCAL_TREE = REPO_ROOT / f".specify/specs/{SLUG}/goal/{SLUG}"
SPEC_DIR = REPO_ROOT / f".specify/specs/{SLUG}"
ENGINE = REPO_ROOT / "scripts/python/goal-utils.py"


def _load_engine():
    spec = importlib.util.spec_from_file_location("goal_utils_temp_goal", ENGINE)
    module = importlib.util.module_from_spec(spec)
    sys.modules["goal_utils_temp_goal"] = module
    spec.loader.exec_module(module)
    return module


goal_utils = _load_engine()


def test_goal_lives_in_the_unified_archive_and_not_the_spec_tree():
    assert GOAL_MD.is_file(), f"archive goal missing: {GOAL_MD}"
    assert not SPEC_LOCAL_TREE.exists(), (
        "the spec-local goal tree is a migration source, not a live landing point")


def test_goal_is_active_with_authored_degree_criteria():
    data = goal_utils.parse_goal(GOAL_MD)
    assert data["status"] == "active"
    assert data["criteria_count"] >= 1
    assert data["objective"].strip()
    for criterion in data["criteria"]:
        assert "SC-" not in criterion, "archive goal criteria must not copy requirement SC rows"


def test_the_definition_carries_its_binding_record():
    meta, _start, _end = goal_utils.read_frontmatter_subset(
        GOAL_MD.read_text(encoding="utf-8"))
    binding = meta.get("binding") or {}
    assert binding.get("owner"), "a goal definition carries its owner"
    assert binding.get("owner_id"), "a goal definition carries the run/actor id"
    assert binding.get("origin") == SLUG, (
        "the migrated definition records its source spec directory as origin")


def test_goal_engine_validates_the_archive_definition():
    proc = subprocess.run(
        [sys.executable, str(ENGINE), "validate", str(GOAL_MD), "--json"],
        capture_output=True, text=True, cwd=REPO_ROOT)
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["valid"] is True


def test_the_archived_source_copy_stays_readable():
    assert ARCHIVED_MD.is_file(), (
        "archive-not-delete: the migrated source stays readable under trees/")


def test_list_names_the_migrated_goal_and_never_the_spec_tree():
    proc = subprocess.run(
        [sys.executable, str(ENGINE), "list", "--json"],
        capture_output=True, text=True, cwd=REPO_ROOT)
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert SLUG in [row["slug"] for row in payload["goals"]]


def test_resolve_scope_returns_the_archive_roots():
    proc = subprocess.run(
        [sys.executable, str(ENGINE), "resolve-scope", "--scope", "goal",
         "--spec-dir", str(SPEC_DIR), "--json"],
        capture_output=True, text=True, cwd=REPO_ROOT)
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["scope"] == "goal"
    assert payload["goal_root"].endswith("/.specify/anchoring")
    assert payload["team_root"].endswith("/.specify/teams")


def test_retired_spec_scope_is_refused():
    proc = subprocess.run(
        [sys.executable, str(ENGINE), "list", "--scope", "spec",
         "--spec-dir", str(SPEC_DIR), "--json"],
        capture_output=True, text=True, cwd=REPO_ROOT)
    assert proc.returncode == 2
    assert "invalid choice" in (proc.stderr + proc.stdout)
