"""Integration: concurrent refresh of one goal directory (US6).

Covers FR-035 / TG-16 / WS-13 and SC-015. Once a goal can be pursued by several
teams, two of them reaching boundaries close together would race on the same
delivery directory — so refreshes serialize, and a half-written directory is a
prohibited state rather than an unlucky outcome.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
GENERATOR = REPO_ROOT / "skills/create-team/scripts/build-summary-input.py"
FIXTURES = REPO_ROOT / "tests/fixtures/teams"
SHARED_GOAL = "shared-harvest-goal"
EXIT_SERIALIZED = 4

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


def refresh(root: Path, team: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(GENERATOR), "--team", team, "--repo-root", str(root), "--json"],
        capture_output=True, text=True, cwd=str(root),
    )


def delivery_dir(root: Path) -> Path:
    return root / f".specify/project/goal/{SHARED_GOAL}"


def form_path(root: Path) -> Path:
    return delivery_dir(root) / "data/project-input.yaml"


# --------------------------------------------------------------------------
# FR-035 / TG-16 — serialization
# --------------------------------------------------------------------------


@requires_fixtures
def test_a_held_lock_makes_the_second_refresh_stand_down(two_teams: Path) -> None:
    """The suppressed refresh reports it, rather than racing or silently no-opping."""
    assert refresh(two_teams, "goal-share-a").returncode == 0
    lock = form_path(two_teams).parent / ".refresh.lock"
    lock.write_text(str(os.getpid()), encoding="utf-8")  # simulate a live sibling refresh
    try:
        result = refresh(two_teams, "goal-share-b")
        assert result.returncode == EXIT_SERIALIZED, result.stdout + result.stderr
        report = json.loads(result.stdout)
        assert report["status"] == "skipped(serialized)"
        assert report["goal_slug"] == SHARED_GOAL
        assert report["reason"], "the suppressed refresh must state why"
    finally:
        lock.unlink(missing_ok=True)


@requires_fixtures
def test_lock_is_released_after_a_successful_refresh(two_teams: Path) -> None:
    assert refresh(two_teams, "goal-share-a").returncode == 0
    assert not (form_path(two_teams).parent / ".refresh.lock").exists(), (
        "the lock outlived its refresh and would block every later run"
    )
    assert refresh(two_teams, "goal-share-b").returncode == 0


@requires_fixtures
def test_a_stale_lock_does_not_block_forever(two_teams: Path) -> None:
    """A lock left behind by a dead run must not wedge the goal permanently."""
    assert refresh(two_teams, "goal-share-a").returncode == 0
    lock = form_path(two_teams).parent / ".refresh.lock"
    lock.write_text("99999999", encoding="utf-8")
    os.utime(lock, (0, 0))  # far in the past → stale
    try:
        assert refresh(two_teams, "goal-share-b").returncode == 0
    finally:
        lock.unlink(missing_ok=True)


@requires_fixtures
def test_concurrent_refreshes_yield_exactly_one_current_summary(two_teams: Path) -> None:
    """SC-015 — one current summary, zero lost updates, zero half-written state."""
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda t: refresh(two_teams, t), ["goal-share-a", "goal-share-b"]))

    codes = sorted(r.returncode for r in results)
    assert codes in ([0, 0], [0, EXIT_SERIALIZED]), (
        f"unexpected exit codes from concurrent refresh: {codes}\n"
        + "\n".join(r.stdout + r.stderr for r in results)
    )
    forms = list(delivery_dir(two_teams).rglob("project-input.yaml"))
    assert len(forms) == 1, f"expected one current form, found {forms}"

    # whichever refresh won, the result must be complete and parseable
    doc = yaml.safe_load(forms[0].read_text(encoding="utf-8"))
    assert doc["project"]["project_name"] == SHARED_GOAL
    assert doc["work_items"], "the surviving form has no work items"
    assert doc["coverage"], "the surviving form has no coverage block"


@requires_fixtures
def test_no_half_written_artifacts_remain(two_teams: Path) -> None:
    """WS-13 — the write is atomic, so no partial temp file survives."""
    with ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(lambda t: refresh(two_teams, t), ["goal-share-a", "goal-share-b"]))
    leftovers = [
        p.name for p in delivery_dir(two_teams).rglob("*")
        if p.is_file() and (p.name.endswith(".tmp") or p.name == ".refresh.lock")
    ]
    assert not leftovers, f"partial or lock artifacts left behind: {leftovers}"


@requires_fixtures
def test_repeated_concurrent_rounds_never_corrupt_the_form(two_teams: Path) -> None:
    """A lost update would show up as a form that no longer parses or loses a team."""
    for _ in range(3):
        with ThreadPoolExecutor(max_workers=2) as pool:
            list(pool.map(lambda t: refresh(two_teams, t), ["goal-share-a", "goal-share-b"]))
        doc = yaml.safe_load(form_path(two_teams).read_text(encoding="utf-8"))
        teams_present = {w["item_id"].split(".", 1)[0] for w in doc["work_items"]}
        assert teams_present == {"goal-share-a", "goal-share-b"}, (
            f"a concurrent round lost a team's contribution: {teams_present}"
        )


@requires_fixtures
def test_serialized_refresh_leaves_the_previous_summary_intact(two_teams: Path) -> None:
    """A stood-down refresh must not damage what is already there."""
    assert refresh(two_teams, "goal-share-a").returncode == 0
    before = hashlib.sha256(form_path(two_teams).read_bytes()).hexdigest()

    lock = form_path(two_teams).parent / ".refresh.lock"
    lock.write_text(str(os.getpid()), encoding="utf-8")
    try:
        assert refresh(two_teams, "goal-share-b").returncode == EXIT_SERIALIZED
    finally:
        lock.unlink(missing_ok=True)

    after = hashlib.sha256(form_path(two_teams).read_bytes()).hexdigest()
    assert after == before, "a serialized (skipped) refresh modified the existing summary"
