"""Contract tests for the goal/team scope resolver CLI (Feature 085, T011/T012)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts/python/goal-utils.py"


def _seed(root: Path) -> Path:
    global_goal = root / ".specify/anchoring/global-goal/goal.md"
    global_goal.parent.mkdir(parents=True, exist_ok=True)
    global_goal.write_text("# Global Goal\n", encoding="utf-8")
    global_team = root / ".specify/teams/global-team/team.md"
    global_team.parent.mkdir(parents=True, exist_ok=True)
    global_team.write_text("---\nslug: global-team\n---\n", encoding="utf-8")
    spec = root / ".specify/specs/084-sample"
    spec_goal = spec / "goal/spec-goal/goal.md"
    spec_goal.parent.mkdir(parents=True, exist_ok=True)
    spec_goal.write_text("# Spec Goal\n", encoding="utf-8")
    spec_team = spec / "team/spec-team/team.md"
    spec_team.parent.mkdir(parents=True, exist_ok=True)
    spec_team.write_text("---\nslug: spec-team\n---\n", encoding="utf-8")
    return spec


def _run(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ENGINE), *args, "--repo-root", str(root), "--json"],
        capture_output=True, text=True, cwd=REPO_ROOT)


def test_global_scope(tmp_path: Path):
    _seed(tmp_path)
    proc = _run(tmp_path, "resolve-scope", "--scope", "global")
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["scope"] == "global"
    assert payload["goal_root"].endswith("/.specify/anchoring")
    assert payload["team_root"].endswith("/.specify/teams")


def test_spec_scope(tmp_path: Path):
    spec = _seed(tmp_path)
    proc = _run(tmp_path, "resolve-scope", "--scope", "spec", "--spec-dir", str(spec))
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["scope"] == "spec"
    assert payload["goal_root"] == str(spec / "goal")
    assert payload["team_root"] == str(spec / "team")


def test_spec_scope_requires_spec_dir(tmp_path: Path):
    _seed(tmp_path)
    proc = _run(tmp_path, "resolve-scope", "--scope", "spec")
    assert proc.returncode == 2
    assert "spec-scope-requires-spec-dir" in proc.stdout


def test_auto_ambiguity(tmp_path: Path):
    spec = _seed(tmp_path)
    proc = _run(tmp_path, "resolve-scope", "--scope", "auto", "--spec-dir", str(spec))
    assert proc.returncode == 2
    assert "scope-ambiguous" in proc.stdout


def test_list_global_is_unchanged(tmp_path: Path):
    _seed(tmp_path)
    proc = _run(tmp_path, "list")
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert [row["slug"] for row in payload["goals"]] == ["global-goal"]


def test_list_spec_is_scoped(tmp_path: Path):
    spec = _seed(tmp_path)
    proc = _run(tmp_path, "list", "--scope", "spec", "--spec-dir", str(spec))
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert [row["slug"] for row in payload["goals"]] == ["spec-goal"]


def test_write_with_auto_scope_is_rejected(tmp_path: Path):
    spec = _seed(tmp_path)
    proc = _run(tmp_path, "create", "new-goal", "--scope", "auto",
                "--spec-dir", str(spec), "--objective", "an outcome")
    assert proc.returncode == 2
    assert "read-only" in proc.stdout


def test_spec_write_leaves_global_stores_byte_identical(tmp_path: Path):
    spec = _seed(tmp_path)
    globals_ = [
        tmp_path / ".specify/anchoring/global-goal/goal.md",
        tmp_path / ".specify/teams/global-team/team.md",
    ]
    before = {path: path.read_bytes() for path in globals_}
    proc = _run(tmp_path, "create", "new-temp-goal", "--scope", "spec",
                "--spec-dir", str(spec), "--objective", "a run-scoped outcome")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    after = {path: path.read_bytes() for path in globals_}
    assert after == before, "a spec-scoped write must not touch the global stores"
    assert (spec / "goal/new-temp-goal/goal.md").is_file()
