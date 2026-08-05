"""Integration test for the coordination round (037-goal-registry, T045).

Contract: .specify/specs/037-goal-registry/contracts/team-territory.contract.md

CR-1..CR-5: the mechanism detects and proposes only; every team.md is byte-unchanged
during the proposal stage; a proposal carries its rationale; a contested area never
remains multi-writable; and a single-team goal initiates no round. Ratification is a
human step, modelled here by the caller writing the agreed territory back to team.md.
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


def _team(root, slug, goal_slug, write):
    d = root / ".specify/teams" / slug
    d.mkdir(parents=True, exist_ok=True)
    fm = [f"slug: {slug}", f"name: {slug}", "goal: outcome", f"goal_slug: {goal_slug}",
          "pattern: continuous", "territory:", "  write:"]
    fm += [f"    - {w}" for w in write]
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


def _hash_team_files(root):
    return {p: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted((root / ".specify/teams").glob("*/team.md"))}


def test_overlap_detected_and_named_to_paths(tmp_path):
    _team(tmp_path, "a", "g", ["docs/**"])
    _team(tmp_path, "b", "g", ["docs/reference/x.md"])
    _define(tmp_path, "g")
    report = _refresh(tmp_path, "g")
    overlaps = [f for f in report["overlaps"] if f["verdict"] == "overlap"]
    assert overlaps, "a write-write collision must be detected"
    assert overlaps[0]["entries"], "the finding must name concrete entries"


def test_detection_does_not_write_any_team_file(tmp_path):
    _team(tmp_path, "a", "g", ["docs/**"])
    _team(tmp_path, "b", "g", ["docs/x.md"])
    _define(tmp_path, "g")
    before = _hash_team_files(tmp_path)
    _refresh(tmp_path, "g")   # detection rides refresh; it must not mutate team.md
    after = _hash_team_files(tmp_path)
    assert before == after, "the proposal/detection stage must leave every team.md byte-identical"


def test_contested_area_is_reported_for_resolution(tmp_path):
    _team(tmp_path, "a", "g", ["shared/**"])
    _team(tmp_path, "b", "g", ["shared/**"])
    _define(tmp_path, "g")
    report = _refresh(tmp_path, "g")
    contested = [f for f in report["overlaps"] if f["verdict"] == "overlap"]
    assert contested, "a mutually-written area must surface as a contested area"
    # it is reported, not silently left multi-writable
    assert report.get("contested_areas"), "contested areas must be enumerated for the round"


def test_read_only_overlap_does_not_trigger_a_contest(tmp_path):
    _team(tmp_path, "a", "g", [])   # no write scope, reads only via default
    d = tmp_path / ".specify/teams/a/team.md"
    d.write_text(d.read_text().replace("  write:\n", "  read:\n    - skills/**\n  write:\n"),
                 encoding="utf-8")
    _team(tmp_path, "b", "g", [])
    e = tmp_path / ".specify/teams/b/team.md"
    e.write_text(e.read_text().replace("  write:\n", "  read:\n    - skills/**\n  write:\n"),
                 encoding="utf-8")
    _define(tmp_path, "g")
    report = _refresh(tmp_path, "g")
    assert not [f for f in report["overlaps"] if f["verdict"] == "overlap"], (
        "read-only overlap is allowed and must not be a contest"
    )


def test_single_team_goal_initiates_no_round(tmp_path):
    _team(tmp_path, "solo", "g", ["docs/**"])
    _define(tmp_path, "g")
    report = _refresh(tmp_path, "g")
    assert not report.get("contested_areas"), "one team → no contested areas"
    assert all(f["verdict"] != "overlap" for f in report.get("overlaps", []))
