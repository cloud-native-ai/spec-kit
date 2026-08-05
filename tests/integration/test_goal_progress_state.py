"""Progress-state distinction for a defined goal (037-goal-registry, T037).

FR-015: the mechanism must distinguish "goal defined but not yet advanced" from
"goal in progress". A defined goal with no ledger events and no run reports has no
execution material, so the generator declines with its distinct no-material exit
rather than silently emitting a summary that would read as if work were underway.
The positive "who is advancing" surfacing is the roster's job (US5).
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
GENERATOR = REPO_ROOT / "skills/create-team/scripts/build-summary-input.py"
GOAL_UTILS = REPO_ROOT / "scripts/python/goal-utils.py"

pytestmark = pytest.mark.integration


def _team(root: Path, slug: str, goal_slug: str, *, advancing: bool) -> None:
    d = root / ".specify/teams" / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / "team.md").write_text(
        f"---\nslug: {slug}\nname: {slug}\npattern: continuous\n"
        f"goal: placeholder\ngoal_slug: {goal_slug}\n---\n\n## Goal\n\nplaceholder\n",
        encoding="utf-8",
    )
    if advancing:
        (d / "items.jsonl").write_text(
            json.dumps({"event": "created", "item_id": "TI-0001", "title": "w",
                        "phase_ref": "P1", "state": "in-progress"}) + "\n",
            encoding="utf-8",
        )


def _define(root: Path, slug: str, objective: str) -> None:
    subprocess.run(
        ["python3", str(GOAL_UTILS), "create", slug, "--objective", objective,
         "--repo-root", str(root)],
        capture_output=True, text=True, check=True,
    )


def _run(root: Path, goal_slug: str) -> tuple[int, dict]:
    proc = subprocess.run(
        ["python3", str(GENERATOR), "--goal", goal_slug, "--repo-root", str(root), "--json"],
        capture_output=True, text=True,
    )
    return proc.returncode, json.loads(proc.stdout)


def test_defined_but_unadvanced_declines_rather_than_faking_progress(tmp_path):
    _team(tmp_path, "idle", "g", advancing=False)
    _define(tmp_path, "g", "Defined, but nobody has started yet.")
    code, report = _run(tmp_path, "g")
    assert code == 3 or report.get("declined") is True, (
        "a defined-but-unadvanced goal must decline (no material), never be summarised "
        "as if in progress"
    )


def test_advancing_goal_produces_a_summary(tmp_path):
    _team(tmp_path, "busy", "g", advancing=True)
    _define(tmp_path, "g", "Actively being worked on.")
    code, report = _run(tmp_path, "g")
    assert code == 0 and report.get("declined") in (False, None), report
    assert report["contributing_teams"] == ["busy"]


def test_the_two_states_are_distinguishable(tmp_path):
    """The whole point of FR-015: the two situations yield different outcomes."""
    _team(tmp_path, "idle", "gi", advancing=False)
    _define(tmp_path, "gi", "Not started.")
    _team(tmp_path, "busy", "gb", advancing=True)
    _define(tmp_path, "gb", "Started.")
    idle_code, _ = _run(tmp_path, "gi")
    busy_code, _ = _run(tmp_path, "gb")
    assert idle_code != busy_code, (
        "not-yet-advanced and in-progress must be distinguishable, not collapsed"
    )
