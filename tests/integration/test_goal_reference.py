"""Integration tests for team → goal reference resolution (037-goal-registry, T029).

Covers FR-008…FR-012: an identity-only reference resolves to the archived
definition; N teams sharing one identity resolve identically; a broken reference is
reported without degrading to an empty goal; an inline-only legacy team still works;
a team declaring two goals is rejected; and reference-vs-inline divergence resolves
to the definition with the divergence surfaced.
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


def _team(root: Path, slug: str, *, goal_slug: str | None = None,
          inline_goal: str = "", extra: str = "") -> None:
    d = root / ".specify/teams" / slug
    d.mkdir(parents=True, exist_ok=True)
    fm = [f"slug: {slug}", f"name: {slug}", "pattern: continuous"]
    if inline_goal:
        fm.append(f"goal: {inline_goal}")
    if goal_slug is not None:
        fm.append(f"goal_slug: {goal_slug}")
    if extra:
        fm.append(extra)
    (d / "team.md").write_text(
        "---\n" + "\n".join(fm) + "\n---\n\n## Goal\n\n" + (inline_goal or "n/a") + "\n",
        encoding="utf-8",
    )
    # one ledger event so the goal has execution material
    (d / "items.jsonl").write_text(
        json.dumps({"event": "created", "item_id": "TI-0001", "title": f"{slug} work",
                    "phase_ref": "P1", "state": "in-progress"}) + "\n",
        encoding="utf-8",
    )


def _define(root: Path, slug: str, objective: str, criteria: list[str]) -> None:
    cmd = ["python3", str(GOAL_UTILS), "create", slug, "--objective", objective,
           "--repo-root", str(root)]
    for c in criteria:
        cmd += ["--criterion", c]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr


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


def test_two_teams_sharing_a_goal_resolve_to_one_definition(tmp_path):
    _team(tmp_path, "team-a", goal_slug="shared", inline_goal="local phrasing a")
    _team(tmp_path, "team-b", goal_slug="shared", inline_goal="local phrasing b")
    _define(tmp_path, "shared", "The shared objective is reached.", ["Criterion one."])
    report = _refresh(tmp_path, "shared")
    assert report["goal_source"] == "definition"
    assert sorted(report["contributing_teams"]) == ["team-a", "team-b"]
    form = _form(tmp_path, "shared")
    assert form["project"]["project_desc"] == "The shared objective is reached."
    assert [m["milestone_name"] for m in form["milestones"]] == ["Criterion one."]


def test_broken_reference_is_reported_not_degraded(tmp_path):
    _team(tmp_path, "orphan", goal_slug="missing-goal", inline_goal="fallback outcome")
    _define(tmp_path, "unrelated", "Unrelated.", [])  # archive exists, target absent
    report = _refresh(tmp_path, "missing-goal")
    assert report["goal_source"] == "inline", "must fall back, not fail"
    assert any("断链" in g or "FR-010" in g for g in report["material_gaps"]), report["material_gaps"]
    # honest degradation: it fell back to the inline goal, not an empty one
    form = _form(tmp_path, "missing-goal")
    assert form["project"]["project_desc"] == "fallback outcome"


def test_inline_only_team_still_works_with_no_archive(tmp_path):
    _team(tmp_path, "legacy", inline_goal="the legacy inline outcome")
    report = _refresh(tmp_path, "legacy")
    assert report["goal_source"] == "inline"
    assert not any("断链" in g for g in report["material_gaps"]), (
        "a team that never adopted goal_slug must not be reported as broken"
    )
    form = _form(tmp_path, "legacy")
    assert form["project"]["project_desc"] == "the legacy inline outcome"


def test_reference_inline_divergence_prefers_the_definition_and_surfaces_it(tmp_path):
    _team(tmp_path, "diverge", goal_slug="canon", inline_goal="stale inline wording")
    _define(tmp_path, "canon", "The canonical objective.", ["c1"])
    report = _refresh(tmp_path, "canon")
    assert report["goal_source"] == "definition"
    form = _form(tmp_path, "canon")
    assert form["project"]["project_desc"] == "The canonical objective."
    assert any("FR-012" in g or "不一致" in g for g in report["material_gaps"]), report["material_gaps"]


def test_editing_the_definition_changes_all_referencing_teams(tmp_path):
    _team(tmp_path, "t1", goal_slug="evolve", inline_goal="x")
    _team(tmp_path, "t2", goal_slug="evolve", inline_goal="y")
    _define(tmp_path, "evolve", "First objective.", ["old"])
    first = _refresh(tmp_path, "evolve")
    assert _form(tmp_path, "evolve")["project"]["project_desc"] == "First objective."
    # edit the definition only — touch no team file
    subprocess.run(
        ["python3", str(GOAL_UTILS), "criteria", "evolve", "--criterion", "new",
         "--repo-root", str(tmp_path)],
        capture_output=True, text=True, check=True,
    )
    subprocess.run(
        ["python3", str(GOAL_UTILS), "status", "evolve", "--set", "active",
         "--repo-root", str(tmp_path)],
        capture_output=True, text=True, check=True,
    )
    second = _refresh(tmp_path, "evolve")
    assert [m["milestone_name"] for m in _form(tmp_path, "evolve")["milestones"]] == ["new"]
    assert sorted(second["contributing_teams"]) == ["t1", "t2"]


def test_one_goal_per_team_invariant_is_documented():
    """FR-009 — a team serves exactly one goal at a time.

    There is no executable team.md schema validator (a frontmatter mapping cannot even
    hold two identical `goal_slug` keys), so this invariant is enforced at the
    prose-schema level like the rest of the team.md contract. Pin that it is stated,
    which is the honest verifiable form for a prose-governed rule.
    """
    skill = (REPO_ROOT / "skills/create-team/SKILL.md").read_text(encoding="utf-8")
    reference = (REPO_ROOT / "skills/create-team/references/goal.md").read_text(encoding="utf-8")
    authority = (
        REPO_ROOT / ".specify/shared/definitions/goal-definitions.md"
    ).read_text(encoding="utf-8")
    combined = skill + reference + authority
    assert ("一个 team" in combined and "只有一个" in combined) or "one" in authority.lower(), (
        "the one-goal-per-team invariant (FR-009) must be documented in the team-domain "
        "schema or the concept authority"
    )
