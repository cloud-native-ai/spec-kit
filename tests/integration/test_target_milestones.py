"""Integration tests for done-Target milestone absorption (038-goal-target, T025).

Contract: .specify/specs/038-goal-target/contracts/target-ref-ledger.contract.md §5

done Targets join the existing milestones group carrying their own source marker
(`goal-target:<slug>/goal.md#T-nnn`); criteria projection rows keep their 036
FR-013 semantics; open/dropped Targets never enter the group; when criteria are
empty, done Targets fill the group with a declared source. summarize-project
code/DDL stay untouched — the distinction rides the existing `source` column.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
GENERATOR = REPO_ROOT / "skills/create-team/scripts/build-summary-input.py"
SUMMARIZE_SCRIPTS = REPO_ROOT / "skills/summarize-project"
GOAL = "sliced-goal"

pytestmark = pytest.mark.integration

TARGETS_MIXED = (
    "## Targets\n\n| ID | Target | Status |\n|----|--------|--------|\n"
    "| T-001 | 日志组件拆分完成 | done |\n"
    "| T-002 | 指标采集链路独立可部署 | open |\n"
    "| T-003 | 告警规则全量迁移 | dropped |\n\n"
)


def _write_team(root: Path) -> None:
    team_dir = root / ".specify/teams/team-a"
    team_dir.mkdir(parents=True, exist_ok=True)
    (team_dir / "team.md").write_text(
        f"---\nslug: team-a\nname: team-a\ngoal_slug: {GOAL}\n"
        "pattern: parallel\nmembers: []\n---\n\n## Goal\n\n平台收敛。\n",
        encoding="utf-8",
    )
    row = {
        "item_id": "TI-0001", "title": "一项工作", "phase_ref": "PH-0001",
        "state": "completed", "provenance": ".specify/teams/team-a/runs/x.md",
        "ts": "2026-08-12T00:00:00Z", "target_ref": "T-001",
    }
    (team_dir / "items.jsonl").write_text(
        json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_goal(root: Path, targets: str, criteria: str) -> None:
    goal_dir = root / ".specify/goal" / GOAL
    goal_dir.mkdir(parents=True, exist_ok=True)
    (goal_dir / "goal.md").write_text(
        "---\nstatus: active\ncreated: 2026-08-12\nupdated: 2026-08-12\n---\n\n"
        f"# Goal: {GOAL}\n\n## Objective\n\n平台能力收敛稳定。\n\n"
        f"## Success Criteria\n\n{criteria}\n\n{targets}"
        "## History\n\n- 2026-08-12 — created.\n",
        encoding="utf-8",
    )


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    (tmp_path / ".specify/agents/templates").mkdir(parents=True)
    return tmp_path


def run_generator(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(GENERATOR), "--repo-root", str(root), "--json",
         "--goal", GOAL],
        capture_output=True, text=True, cwd=str(root),
    )


def form_of(root: Path) -> dict:
    return yaml.safe_load(
        (root / f".specify/goal/{GOAL}/summary/data/project-input.yaml")
        .read_text(encoding="utf-8"))


def test_done_target_joins_milestones_with_its_source_marker(repo: Path) -> None:
    _write_goal(repo, TARGETS_MIXED, "1. 判据一保持可测")
    _write_team(repo)
    assert run_generator(repo).returncode == 0
    milestones = form_of(repo)["milestones"]
    by_source = {m["source"]: m for m in milestones}
    target_row = by_source.get(f"goal-target:{GOAL}/goal.md#T-001")
    assert target_row is not None, (
        f"done Target must appear with its source marker; got "
        f"{sorted(by_source)}")
    assert target_row["milestone_name"].startswith("日志组件拆分完成")
    assert target_row.get("status") == "achieved"


def test_criteria_projection_rows_keep_their_semantics(repo: Path) -> None:
    """036 FR-013 unchanged: criteria rows keep the definition relpath source."""
    _write_goal(repo, TARGETS_MIXED, "1. 判据一保持可测")
    _write_team(repo)
    assert run_generator(repo).returncode == 0
    milestones = form_of(repo)["milestones"]
    criteria_rows = [m for m in milestones
                     if m["source"] == f".specify/goal/{GOAL}/goal.md"]
    assert len(criteria_rows) == 1
    assert criteria_rows[0]["milestone_name"].startswith("判据一保持可测")


def test_open_and_dropped_targets_stay_out_of_milestones(repo: Path) -> None:
    _write_goal(repo, TARGETS_MIXED, "1. 判据一保持可测")
    _write_team(repo)
    assert run_generator(repo).returncode == 0
    text = yaml.safe_dump(form_of(repo)["milestones"], allow_unicode=True)
    assert "#T-002" not in text
    assert "#T-003" not in text


def test_empty_criteria_with_done_targets_fills_and_declares(repo: Path) -> None:
    _write_goal(repo, TARGETS_MIXED, "None provided.")
    _write_team(repo)
    result = run_generator(repo)
    assert result.returncode == 0, result.stdout + result.stderr
    milestones = form_of(repo)["milestones"]
    assert any(m["source"].startswith("goal-target:") for m in milestones), (
        "done Targets must fill the group when criteria are empty")
    report = json.loads(result.stdout)
    assert any("goal-target" in g or "Target 来源" in g
               for g in report["material_gaps"]), (
        "the target-sourced fill must be declared")


def test_summarize_project_is_untouched(repo: Path) -> None:
    """D7: absorption rides the existing source column — no engine/DDL change.

    Behavioral guard: the milestones DDL already carries the `source`-shaped
    open set; this test asserts the generator's target rows need no new column.
    """
    ddl = (SUMMARIZE_SCRIPTS / "schema/project.sql").read_text(encoding="utf-8")
    assert "goal-target" not in ddl, (
        "DDL must not hard-code the target source marker")
