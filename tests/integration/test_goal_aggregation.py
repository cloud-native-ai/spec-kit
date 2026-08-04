"""Integration: goal-indexed aggregation across teams (US6).

Covers FR-030…FR-036 and SC-013 / SC-014. The point of a *goal* index — as opposed to
a relocated team index — is that one directory answers "how far has this goal got"
across every team pursuing it, with per-team attribution preserved.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
GENERATOR = REPO_ROOT / "skills/create-team/scripts/build-summary-input.py"
SUMMARIZE = REPO_ROOT / "skills/summarize-project/scripts"
FIXTURES = REPO_ROOT / "tests/fixtures/teams"
SHARED_GOAL = "shared-harvest-goal"

pytestmark = [pytest.mark.integration]
requires_fixtures = pytest.mark.skipif(
    not GENERATOR.is_file() or not (FIXTURES / "goal-share-a").is_dir(),
    reason="generator or shared-goal fixtures unavailable",
)


@pytest.fixture()
def two_teams(tmp_path: Path) -> Path:
    (tmp_path / ".specify/teams").mkdir(parents=True)
    for slug in ("goal-share-a", "goal-share-b"):
        shutil.copytree(FIXTURES / slug, tmp_path / ".specify/teams" / slug)
    for sub in ("templates", "instances"):
        (tmp_path / ".specify/agents" / sub).mkdir(parents=True, exist_ok=True)
    (tmp_path / ".specify/agents/templates/agent-team-supervisor-template.agent.md").write_text(
        "---\nname: Team Supervisor\n---\n", encoding="utf-8"
    )
    return tmp_path


def run(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(GENERATOR), "--repo-root", str(root), "--json", *args],
        capture_output=True, text=True, cwd=str(root),
    )


def form_of(root: Path, goal: str = SHARED_GOAL) -> dict:
    return yaml.safe_load(
        (root / f".specify/project/goal/{goal}/data/project-input.yaml").read_text(encoding="utf-8")
    )


# --------------------------------------------------------------------------
# FR-031 / FR-032 — one goal directory aggregating N teams
# --------------------------------------------------------------------------


@requires_fixtures
def test_both_teams_land_in_one_goal_directory(two_teams: Path) -> None:
    result = run(two_teams, "--goal", SHARED_GOAL)
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    assert sorted(report["contributing_teams"]) == ["goal-share-a", "goal-share-b"]
    goal_dirs = sorted(p.name for p in (two_teams / ".specify/project/goal").iterdir())
    assert goal_dirs == [SHARED_GOAL], f"expected exactly one goal directory, got {goal_dirs}"


@requires_fixtures
def test_triggering_via_either_team_aggregates_the_whole_goal(two_teams: Path) -> None:
    """A team never summarizes in isolation."""
    for slug in ("goal-share-a", "goal-share-b"):
        shutil.rmtree(two_teams / ".specify/project", ignore_errors=True)
        result = run(two_teams, "--team", slug)
        assert result.returncode == 0, result.stdout + result.stderr
        report = json.loads(result.stdout)
        assert sorted(report["contributing_teams"]) == ["goal-share-a", "goal-share-b"], (
            f"triggering via {slug} did not aggregate the sibling team"
        )
        assert report["goal_slug"] == SHARED_GOAL


@requires_fixtures
def test_all_teams_work_items_are_present(two_teams: Path) -> None:
    assert run(two_teams, "--goal", SHARED_GOAL).returncode == 0
    doc = form_of(two_teams)
    ids = {w["item_id"] for w in doc["work_items"]}
    assert ids == {
        "goal-share-a.TI-0001",
        "goal-share-a.TI-0002",
        "goal-share-b.TI-0001",
    }, ids


@requires_fixtures
def test_colliding_per_team_ids_survive_aggregation(two_teams: Path) -> None:
    """FG-15 — both fixtures issue TI-0001; unprefixed this would be exit 3."""
    assert run(two_teams, "--goal", SHARED_GOAL).returncode == 0
    form = two_teams / f".specify/project/goal/{SHARED_GOAL}/data/project-input.yaml"
    load = subprocess.run(
        [sys.executable, str(SUMMARIZE / "project-db.py"), "--db", str(two_teams / "p.db"),
         "--load", str(form)],
        capture_output=True, text=True, cwd=str(two_teams),
    )
    assert load.returncode == 0, (
        "the aggregate form was rejected — id namespacing failed\n" + load.stdout + load.stderr
    )
    check = subprocess.run(
        [sys.executable, str(SUMMARIZE / "project-db.py"), "--db", str(two_teams / "p.db"), "--check"],
        capture_output=True, text=True, cwd=str(two_teams),
    )
    assert check.returncode == 0, check.stdout


@requires_fixtures
def test_every_item_is_attributable_to_its_producing_team(two_teams: Path) -> None:
    """FR-033 — attribution must be machine-decidable."""
    assert run(two_teams, "--goal", SHARED_GOAL).returncode == 0
    doc = form_of(two_teams)
    for row in doc["work_items"]:
        team = row["item_id"].split(".", 1)[0]
        assert team in {"goal-share-a", "goal-share-b"}, row
        assert f"/teams/{team}/" in row["source"], (
            f"id prefix and provenance disagree on attribution: {row}"
        )


@requires_fixtures
def test_phases_stay_namespaced_when_patterns_differ(two_teams: Path) -> None:
    """Edge case — a continuous team and an iteration team share this goal."""
    assert run(two_teams, "--goal", SHARED_GOAL).returncode == 0
    doc = form_of(two_teams)
    prefixes = {p["phase_id"].split(".", 1)[0] for p in doc["phases"]}
    assert prefixes == {"goal-share-a", "goal-share-b"}, prefixes
    orders = [p["phase_order"] for p in doc["phases"]]
    assert len(orders) == len(set(orders)), "phase_order collided across teams"


@requires_fixtures
def test_milestones_are_emitted_once_per_goal_not_per_team(two_teams: Path) -> None:
    """FR-032 — the goal's criteria are one set, however many teams pursue it."""
    assert run(two_teams, "--goal", SHARED_GOAL).returncode == 0
    doc = form_of(two_teams)
    names = [m["milestone_name"] for m in doc["milestones"]]
    assert names, "no milestones derived"
    assert len(names) == len(set(names)), f"milestones duplicated per team: {names}"


@requires_fixtures
def test_people_are_deduped_across_teams(two_teams: Path) -> None:
    assert run(two_teams, "--goal", SHARED_GOAL).returncode == 0
    doc = form_of(two_teams)
    ids = [p["owner_id"] for p in doc["people"]]
    assert len(ids) == len(set(ids)), f"the same agent appears twice: {ids}"


# --------------------------------------------------------------------------
# FR-032 — a non-triggering team keeps its contribution
# --------------------------------------------------------------------------


@requires_fixtures
def test_refreshing_one_team_preserves_the_others_contribution(two_teams: Path) -> None:
    assert run(two_teams, "--team", "goal-share-a").returncode == 0
    before = {w["item_id"] for w in form_of(two_teams)["work_items"]}
    assert any(i.startswith("goal-share-b.") for i in before)

    # team A advances; team B does nothing at all
    ledger = two_teams / ".specify/teams/goal-share-a/items.jsonl"
    with ledger.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({
            "item_id": "TI-0002", "title": "A 团队的第二条目", "phase_ref": "PH-0001",
            "state": "completed",
            "provenance": ".specify/teams/goal-share-a/runs/20260801T090000Z-report.md",
            "ts": "2026-08-02T09:00:00Z", "identity": "explicit",
        }, ensure_ascii=False) + "\n")
    assert run(two_teams, "--team", "goal-share-a").returncode == 0
    after = {w["item_id"] for w in form_of(two_teams)["work_items"]}

    assert before <= after, f"a non-triggering team's items disappeared: {before - after}"
    by_id = {w["item_id"]: w for w in form_of(two_teams)["work_items"]}
    assert by_id["goal-share-a.TI-0002"]["status"] == "已完成"
    assert by_id["goal-share-b.TI-0001"]["status"] == "延期", "team B's state was altered"


# --------------------------------------------------------------------------
# FR-034 — inferred goal identity and the migration to an explicit one
# --------------------------------------------------------------------------


@requires_fixtures
def test_team_without_goal_slug_uses_an_inferred_goal_identity(two_teams: Path) -> None:
    team_file = two_teams / ".specify/teams/goal-share-a/team.md"
    team_file.write_text(
        team_file.read_text(encoding="utf-8").replace(f"goal_slug: {SHARED_GOAL}\n", ""),
        encoding="utf-8",
    )
    result = run(two_teams, "--team", "goal-share-a")
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    assert report["goal_slug"] == "goal-share-a"
    assert report["goal_identity"] == "inferred"
    assert any("goal_slug" in f["inferred_from"] or "FR-034" in f["inferred_from"]
               for f in report["inferred_fields"]), report["inferred_fields"]


@requires_fixtures
def test_declaring_goal_slug_migrates_the_team_into_the_shared_goal(two_teams: Path) -> None:
    """FR-034 — after migration the team's history lands in the explicit goal."""
    team_file = two_teams / ".specify/teams/goal-share-a/team.md"
    original = team_file.read_text(encoding="utf-8")
    team_file.write_text(original.replace(f"goal_slug: {SHARED_GOAL}\n", ""), encoding="utf-8")
    assert run(two_teams, "--team", "goal-share-a").returncode == 0
    assert (two_teams / ".specify/project/goal/goal-share-a").is_dir()

    team_file.write_text(original, encoding="utf-8")  # declare it explicitly
    result = run(two_teams, "--team", "goal-share-a")
    assert result.returncode == 0
    report = json.loads(result.stdout)
    assert report["goal_slug"] == SHARED_GOAL
    assert report["goal_identity"] == "explicit"
    ids = {w["item_id"] for w in form_of(two_teams)["work_items"]}
    assert any(i.startswith("goal-share-a.") for i in ids), (
        "the migrated team's history did not land in the explicit goal directory"
    )


@requires_fixtures
def test_goal_prose_divergence_is_reported_for_human_adjudication(two_teams: Path) -> None:
    """GI-4 — the declaration wins; the difference is surfaced, not auto-resolved.

    The frontmatter `goal:` value is the authoritative narrative the generator reads,
    so divergence is introduced there rather than in the `## Goal` body section.
    """
    team_file = two_teams / ".specify/teams/goal-share-b/team.md"
    text = team_file.read_text(encoding="utf-8")
    assert "让团队状态可被目标级读者理解" in text
    team_file.write_text(
        text.replace("让团队状态可被目标级读者理解", "一个实质不同的目标叙述"), encoding="utf-8"
    )
    result = run(two_teams, "--goal", SHARED_GOAL)
    assert result.returncode == 0
    gaps = json.loads(result.stdout)["material_gaps"]
    assert any("goal 正文不一致" in g or "GI-4" in g for g in gaps), gaps


@requires_fixtures
def test_unknown_goal_is_an_input_error(two_teams: Path) -> None:
    assert run(two_teams, "--goal", "no-such-goal").returncode == 2


@requires_fixtures
def test_aggregate_form_passes_the_upstream_validator(two_teams: Path) -> None:
    assert run(two_teams, "--goal", SHARED_GOAL).returncode == 0
    form = two_teams / f".specify/project/goal/{SHARED_GOAL}/data/project-input.yaml"
    val = subprocess.run(
        [sys.executable, str(SUMMARIZE / "validate-project-input.py"), "--input", str(form), "--json"],
        capture_output=True, text=True, cwd=str(two_teams),
    )
    assert val.returncode == 0, val.stdout + val.stderr
    verdict = json.loads(val.stdout)
    assert verdict["status"] == "ready" and verdict["missing_required"] == []
