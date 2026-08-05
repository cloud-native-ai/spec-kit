"""Integration tests for definition-sourced summaries (037-goal-registry, T036/T037).

US3 / FR-013…FR-015: when a goal definition exists, the summary's project narrative
and milestones come from it (not from any team's `## Goal` body); the "goal bodies
disagree" arbitration item disappears because the definition is the single authority;
with no definition the behaviour is identical to 036; and a refresh never writes the
definition file. T037 pins the not-yet-advanced vs in-progress distinction.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
GENERATOR = REPO_ROOT / "skills/create-team/scripts/build-summary-input.py"
GOAL_UTILS = REPO_ROOT / "scripts/python/goal-utils.py"

pytestmark = pytest.mark.integration


def _team(root: Path, slug: str, *, goal_slug: str, inline_goal: str,
          advancing: bool = True) -> None:
    d = root / ".specify/teams" / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / "team.md").write_text(
        f"---\nslug: {slug}\nname: {slug}\npattern: continuous\n"
        f"goal: {inline_goal}\ngoal_slug: {goal_slug}\n---\n\n## Goal\n\n{inline_goal}\n",
        encoding="utf-8",
    )
    if advancing:
        (d / "items.jsonl").write_text(
            json.dumps({"event": "created", "item_id": "TI-0001", "title": "w",
                        "phase_ref": "P1", "state": "in-progress"}) + "\n",
            encoding="utf-8",
        )


def _define(root: Path, slug: str, objective: str, criteria: list[str]) -> None:
    cmd = ["python3", str(GOAL_UTILS), "create", slug, "--objective", objective,
           "--repo-root", str(root)]
    for c in criteria:
        cmd += ["--criterion", c]
    subprocess.run(cmd, capture_output=True, text=True, check=True)


def _refresh(root: Path, goal_slug: str) -> dict:
    proc = subprocess.run(
        ["python3", str(GENERATOR), "--goal", goal_slug, "--repo-root", str(root), "--json"],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def _form(root: Path, goal_slug: str) -> dict:
    return yaml.safe_load(
        (root / f".specify/goal/{goal_slug}/summary/data/project-input.yaml").read_text(encoding="utf-8")
    )


def test_narrative_and_milestones_come_from_the_definition(tmp_path):
    _team(tmp_path, "a", goal_slug="g", inline_goal="team a wording")
    _team(tmp_path, "b", goal_slug="g", inline_goal="team b wording")
    _define(tmp_path, "g", "The authoritative objective.", ["MS one", "MS two"])
    _refresh(tmp_path, "g")
    form = _form(tmp_path, "g")
    assert form["project"]["project_desc"] == "The authoritative objective."
    assert [m["milestone_name"] for m in form["milestones"]] == ["MS one", "MS two"]
    for m in form["milestones"]:
        assert m["source"].endswith("g/goal.md"), "milestones must cite the definition"


def test_disagreeing_team_bodies_no_longer_raise_arbitration_when_a_definition_exists(tmp_path):
    _team(tmp_path, "a", goal_slug="g", inline_goal="wording one")
    _team(tmp_path, "b", goal_slug="g", inline_goal="totally different wording")
    _define(tmp_path, "g", "Canonical.", ["c"])
    report = _refresh(tmp_path, "g")
    assert not any("GI-4" in g for g in report["material_gaps"]), (
        "with a definition present, differing team bodies are not an arbitration gap"
    )


def test_no_definition_behaviour_is_unchanged_from_036(tmp_path):
    _team(tmp_path, "solo", goal_slug="g", inline_goal="the inline outcome")
    # no _define call and no archive → pure-036 path
    report = _refresh(tmp_path, "g")
    assert report["goal_source"] == "inline"
    form = _form(tmp_path, "g")
    assert form["project"]["project_desc"] == "the inline outcome"


def test_refresh_never_writes_the_definition_file(tmp_path):
    _team(tmp_path, "a", goal_slug="g", inline_goal="x")
    _define(tmp_path, "g", "An objective.", ["c1"])
    definition = tmp_path / ".specify/goal/g/goal.md"
    before = hashlib.sha256(definition.read_bytes()).hexdigest()
    _refresh(tmp_path, "g")
    after = hashlib.sha256(definition.read_bytes()).hexdigest()
    assert before == after, "the summary refresh must not touch the authored definition"


def test_empty_criteria_definition_declares_absence_not_invented_milestones(tmp_path):
    _team(tmp_path, "a", goal_slug="g", inline_goal="x")
    _define(tmp_path, "g", "An objective with no measurable criteria yet.", [])
    report = _refresh(tmp_path, "g")
    form = _form(tmp_path, "g")
    assert form["milestones"] == []
    assert any("None provided" in g or "未提供可验证判据" in g for g in report["material_gaps"]), report["material_gaps"]
