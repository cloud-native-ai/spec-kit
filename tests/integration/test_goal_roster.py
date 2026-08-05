"""Integration tests for the derived team roster (037-goal-registry, T044).

Contract: .specify/specs/037-goal-registry/contracts/team-territory.contract.md

RO-1..RO-4: the roster is derived into summary/, never a field of goal.md; it is
complete against a filesystem scan; identity type is explicit vs inferred; and it is
regenerated wholesale. Detection has exactly one trigger point (DT-2).
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
GENERATOR = REPO_ROOT / "skills/create-team/scripts/build-summary-input.py"
GOAL_UTILS = REPO_ROOT / "scripts/python/goal-utils.py"

pytestmark = pytest.mark.integration


def _team(root, slug, *, goal_slug=None, territory_write=None):
    d = root / ".specify/teams" / slug
    d.mkdir(parents=True, exist_ok=True)
    fm = [f"slug: {slug}", f"name: {slug}", "goal: outcome", "pattern: continuous"]
    if goal_slug:
        fm.append(f"goal_slug: {goal_slug}")
    if territory_write is not None:
        fm.append("territory:")
        fm.append("  write:")
        for w in territory_write:
            fm.append(f"    - {w}")
    (d / "team.md").write_text("---\n" + "\n".join(fm) + "\n---\n\n## Goal\n\noutcome\n",
                               encoding="utf-8")
    (d / "items.jsonl").write_text(
        json.dumps({"event": "created", "item_id": "TI-0001", "title": "w",
                    "phase_ref": "P1", "state": "in-progress"}) + "\n", encoding="utf-8")


def _define(root, slug):
    subprocess.run(["python3", str(GOAL_UTILS), "create", slug, "--objective",
                    "An outcome.", "--repo-root", str(root)],
                   capture_output=True, text=True, check=True)


def _refresh(root, goal_slug):
    proc = subprocess.run(["python3", str(GENERATOR), "--goal", goal_slug,
                           "--repo-root", str(root), "--json"],
                          capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_roster_lists_every_team_sharing_the_goal(tmp_path):
    _team(tmp_path, "a", goal_slug="g", territory_write=["docs/**"])
    _team(tmp_path, "b", goal_slug="g", territory_write=["skills/**"])
    _define(tmp_path, "g")
    report = _refresh(tmp_path, "g")
    roster = report["roster"]
    assert sorted(r["team"] for r in roster) == ["a", "b"]


def test_roster_completeness_against_a_filesystem_scan(tmp_path):
    for s in ("a", "b", "c"):
        _team(tmp_path, s, goal_slug="g")
    _define(tmp_path, "g")
    report = _refresh(tmp_path, "g")
    declared = {p.parent.name for p in (tmp_path / ".specify/teams").glob("*/team.md")
                if "goal_slug: g" in (p.read_text(encoding="utf-8"))}
    assert {r["team"] for r in report["roster"]} == declared


def test_roster_records_identity_type(tmp_path):
    _team(tmp_path, "explicit-team", goal_slug="g")
    _define(tmp_path, "g")
    report = _refresh(tmp_path, "g")
    row = next(r for r in report["roster"] if r["team"] == "explicit-team")
    assert row["identity_type"] == "explicit"


def test_roster_written_to_summary_never_to_goal_md(tmp_path):
    _team(tmp_path, "a", goal_slug="g", territory_write=["docs/**"])
    _define(tmp_path, "g")
    definition = tmp_path / ".specify/goal/g/goal.md"
    before = hashlib.sha256(definition.read_bytes()).hexdigest()
    _refresh(tmp_path, "g")
    after = hashlib.sha256(definition.read_bytes()).hexdigest()
    assert before == after, "roster derivation must not write the authored definition"
    assert (tmp_path / ".specify/goal/g/summary/roster.md").is_file(), (
        "the roster must be materialised under summary/"
    )


def test_roster_is_regenerated_wholesale(tmp_path):
    _team(tmp_path, "a", goal_slug="g")
    _define(tmp_path, "g")
    _refresh(tmp_path, "g")
    _team(tmp_path, "b", goal_slug="g")   # a second team joins
    report = _refresh(tmp_path, "g")
    assert sorted(r["team"] for r in report["roster"]) == ["a", "b"], (
        "the roster must reflect the current team set, not an incrementally patched one"
    )
