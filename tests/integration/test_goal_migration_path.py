"""Integration test for the legacy migration path (037-goal-registry, T057).

US4 / FR-016..FR-019: migration is per-team and optional; it preserves the resolved
objective; it never forces removal of the inline goal; and the other teams are
untouched. A team need not migrate for the mechanism to be usable at all.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
GENERATOR = REPO_ROOT / "skills/create-team/scripts/build-summary-input.py"
GOAL_UTILS = REPO_ROOT / "scripts/python/goal-utils.py"

pytestmark = pytest.mark.integration


def _team(root, slug, *, goal_slug=None, inline="An inline outcome."):
    d = root / ".specify/teams" / slug
    d.mkdir(parents=True, exist_ok=True)
    fm = [f"slug: {slug}", f"name: {slug}", f"goal: {inline}"]
    if goal_slug:
        fm.append(f"goal_slug: {goal_slug}")
    fm.append("pattern: continuous")
    (d / "team.md").write_text("---\n" + "\n".join(fm) + f"\n---\n\n## Goal\n\n{inline}\n",
                               encoding="utf-8")
    (d / "items.jsonl").write_text(
        json.dumps({"event": "created", "item_id": "TI-0001", "title": "w",
                    "phase_ref": "P1", "state": "in-progress"}) + "\n", encoding="utf-8")


def _migrate(root, team_slug, *, drop=False):
    cmd = ["python3", str(GOAL_UTILS), "migrate", team_slug, "--repo-root", str(root), "--json"]
    if drop:
        cmd.append("--drop-inline")
    return subprocess.run(cmd, capture_output=True, text=True)


def _refresh(root, goal_slug):
    proc = subprocess.run(["python3", str(GENERATOR), "--goal", goal_slug,
                           "--repo-root", str(root), "--json"], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_migration_preserves_the_resolved_objective(tmp_path):
    _team(tmp_path, "legacy", inline="Reach a reviewed, stable release.")
    # before: resolves from the inline goal
    before = _refresh(tmp_path, "legacy")
    assert before["goal_source"] == "inline"
    before_desc = yaml.safe_load(
        (tmp_path / ".specify/goal/legacy/summary/data/project-input.yaml").read_text()
    )["project"]["project_desc"]

    proc = _migrate(tmp_path, "legacy")
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["goal_slug"] == "legacy"

    # after: resolves from the definition, same objective
    after = _refresh(tmp_path, "legacy")
    assert after["goal_source"] == "definition"
    after_desc = yaml.safe_load(
        (tmp_path / ".specify/goal/legacy/summary/data/project-input.yaml").read_text()
    )["project"]["project_desc"]
    assert after_desc == before_desc == "Reach a reviewed, stable release."


def test_inline_goal_is_kept_by_default(tmp_path):
    _team(tmp_path, "keep", inline="An outcome worth keeping inline.")
    _migrate(tmp_path, "keep")
    team_md = (tmp_path / ".specify/teams/keep/team.md").read_text(encoding="utf-8")
    assert "goal: An outcome worth keeping inline." in team_md, "inline goal must be retained"
    assert "goal_slug: keep" in team_md, "the team must now reference the definition"


def test_inline_goal_removed_only_on_explicit_opt_in(tmp_path):
    _team(tmp_path, "drop", inline="An outcome to drop inline.")
    _migrate(tmp_path, "drop", drop=True)
    team_md = (tmp_path / ".specify/teams/drop/team.md").read_text(encoding="utf-8")
    assert "goal_slug: drop" in team_md
    assert "goal: An outcome to drop inline." not in team_md


def test_other_teams_are_unaffected(tmp_path):
    _team(tmp_path, "target", inline="Target outcome.")
    _team(tmp_path, "bystander", inline="Bystander outcome.")
    before = (tmp_path / ".specify/teams/bystander/team.md").read_bytes()
    _migrate(tmp_path, "target")
    after = (tmp_path / ".specify/teams/bystander/team.md").read_bytes()
    assert before == after, "migrating one team must not touch another"


def test_migration_is_not_a_precondition_for_the_mechanism(tmp_path):
    """FR-011/FR-018 — an unmigrated inline-only team still resolves and runs."""
    _team(tmp_path, "unmigrated", inline="Still inline, never migrated.")
    report = _refresh(tmp_path, "unmigrated")
    assert report["goal_source"] == "inline"
    assert report["contributing_teams"] == ["unmigrated"]


def test_migrating_an_existing_definition_is_refused(tmp_path):
    _team(tmp_path, "dup", goal_slug="already", inline="x")
    subprocess.run(["python3", str(GOAL_UTILS), "create", "already", "--objective",
                    "Pre-existing.", "--repo-root", str(tmp_path)],
                   capture_output=True, text=True, check=True)
    proc = _migrate(tmp_path, "dup")
    assert proc.returncode == 2, "migrating onto an existing definition must be refused"
