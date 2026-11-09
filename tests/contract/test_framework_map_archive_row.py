"""Contract test for the framework-map projection of the unified archive (FR-029).

Feature 094, tasks row T073, contract `owner-rewrites-and-tests.md` C-100. The map is the
single source of truth for the `.specify/` layout, so the Goals / Teams rows must name the
two archive layers only, the archive row must name `.specify/archive/goal-team/`, and the
`Feature specs` row must not imply a goal/team subdirectory.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
FRAMEWORK_MAP = REPO_ROOT / "shared/definitions/framework-map.md"

SPEC_LOCAL = re.compile(r"\.specify/specs/[^\s|`'\"]*/(goal|team)")


def _row(text: str, label: str) -> str:
    for line in text.splitlines():
        if line.startswith(f"| {label} |"):
            return line
    raise AssertionError(f"framework-map.md has no {label!r} row")


# ---------------------------------------------------------------------------
# T073 / C-100 — the unified archive is the only goal/team landing point the map names
# ---------------------------------------------------------------------------

def test_the_framework_map_names_the_unified_archive_and_drops_spec_local_goal_team():
    text = FRAMEWORK_MAP.read_text(encoding="utf-8")

    goals = _row(text, "Goals")
    assert ".specify/anchoring/<slug>/" in goals, (
        "the Goals row must name the goal archive layer `.specify/anchoring/<slug>/`")
    assert ".specify/goal/" not in goals, (
        "the Goals row still names the retired `.specify/goal/` directory")
    assert not SPEC_LOCAL.search(goals), (
        f"the Goals row still names a spec-local goal tree: {goals}")

    teams = _row(text, "Teams")
    assert ".specify/teams/<slug>/" in teams, (
        "the Teams row must name `.specify/teams/<slug>/`")
    assert not SPEC_LOCAL.search(teams), (
        f"the Teams row still names a spec-local team tree: {teams}")

    archive = _row(text, "Goal/team archive history")
    assert ".specify/archive/goal-team/" in archive, (
        "the archive row must name the migration history `.specify/archive/goal-team/`")

    specs = _row(text, "Feature specs")
    if re.search(r"\bgoal\b|\bteam\b", specs, re.IGNORECASE):
        assert "no goal/team subdirectory" in specs, (
            "the Feature specs row may only name goal/team to deny them: " + specs)

    # The retired directory survives nowhere in the map, and no spec-local definition
    # store is named at all.
    assert ".specify/goal/" not in text, "the retired goal directory survives in the map"
    hits = [line.strip() for line in text.splitlines() if SPEC_LOCAL.search(line)]
    assert not hits, f"spec-local goal/team trees named in the map: {hits}"
