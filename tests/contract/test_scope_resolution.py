"""Contract tests for the goal/team archive-layer resolver CLI (Feature 085, T011/T012).

Rewritten by Feature 094 (FR-041 / SC-010, disposal row 1): the scope value set is
`goal` / `teams` / `auto`; the retired position-named members are refused with the
parser's invalid-choice exit, and `--spec-dir` never decides a landing or reading point.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from script_api import run_engine_in_process

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts/python/goal-utils.py"


def _seed(root: Path) -> Path:
    global_goal = root / ".specify/anchoring/archive-goal/goal.md"
    global_goal.parent.mkdir(parents=True, exist_ok=True)
    global_goal.write_text("# Archive Goal\n", encoding="utf-8")
    global_team = root / ".specify/teams/archive-team/team.md"
    global_team.parent.mkdir(parents=True, exist_ok=True)
    global_team.write_text("---\nslug: archive-team\n---\n", encoding="utf-8")
    spec = root / ".specify/specs/084-sample"
    spec.mkdir(parents=True, exist_ok=True)
    return spec


def _run(root: Path, *args: str) -> subprocess.CompletedProcess:
    return run_engine_in_process(ENGINE, [*args, "--repo-root", str(root), "--json"])


def test_goal_scope(tmp_path: Path):
    spec = _seed(tmp_path)
    proc = _run(tmp_path, "resolve-scope", "--scope", "goal", "--spec-dir", str(spec))
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["scope"] == "goal"
    assert payload["goal_root"].endswith("/.specify/anchoring")
    assert payload["team_root"].endswith("/.specify/teams")


def test_teams_scope(tmp_path: Path):
    _seed(tmp_path)
    proc = _run(tmp_path, "resolve-scope", "--scope", "teams")
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["scope"] == "teams"
    assert payload["goal_root"].endswith("/.specify/anchoring")
    assert payload["team_root"].endswith("/.specify/teams")


@pytest.mark.parametrize("retired", ["spec", "global"])
def test_retired_scopes_are_rejected_by_the_parser(tmp_path: Path, retired: str):
    _seed(tmp_path)
    proc = _run(tmp_path, "resolve-scope", "--scope", retired)
    assert proc.returncode == 2
    assert "invalid choice" in (proc.stderr + proc.stdout)


def test_auto_ambiguity(tmp_path: Path):
    _seed(tmp_path)
    proc = _run(tmp_path, "resolve-scope", "--scope", "auto")
    assert proc.returncode == 2
    assert "scope-ambiguous" in proc.stdout


def test_list_global_is_unchanged(tmp_path: Path):
    _seed(tmp_path)
    proc = _run(tmp_path, "list")
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert [row["slug"] for row in payload["goals"]] == ["archive-goal"]


def test_spec_dir_never_decides_the_listing(tmp_path: Path):
    spec = _seed(tmp_path)
    proc = _run(tmp_path, "list", "--scope", "goal", "--spec-dir", str(spec))
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert [row["slug"] for row in payload["goals"]] == ["archive-goal"]


def test_write_with_auto_scope_is_rejected(tmp_path: Path):
    _seed(tmp_path)
    proc = _run(tmp_path, "create", "new-goal", "--scope", "auto",
                "--objective", "an outcome")
    assert proc.returncode == 2
    assert "read-only" in proc.stdout


def test_goal_write_leaves_the_team_store_byte_identical_and_no_spec_path(tmp_path: Path):
    spec = _seed(tmp_path)
    team_store = tmp_path / ".specify/teams/archive-team/team.md"
    before = team_store.read_bytes()
    spec_paths_before = {p for p in tmp_path.rglob("*") if ".specify/specs" in p.parts}
    proc = _run(tmp_path, "create", "new-goal", "--scope", "goal",
                "--spec-dir", str(spec), "--objective", "an archive-layer outcome")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert team_store.read_bytes() == before, (
        "a goal-layer write must not touch the team store")
    assert (tmp_path / ".specify/anchoring/new-goal/goal.md").is_file()
    spec_paths_after = {p for p in tmp_path.rglob("*") if ".specify/specs" in p.parts}
    assert spec_paths_after == spec_paths_before, (
        "a definition write must add no path under .specify/specs/")
