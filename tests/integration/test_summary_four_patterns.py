"""Integration: the full chain per collaboration pattern.

generator → validate-project-input.py → project-db.py --load → --check

Covers SC-001 (a team per pattern produces a summary from tracked artifacts alone)
and SC-002 (R-tier complete with zero manual form editing).

Real teams supply `continuous` and `iteration`; fixtures supply `serial` and
`parallel`, because the repository has no team of those patterns. Everything runs
inside a temporary repo root so the real `.specify/project/` is never written.
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
REAL_TEAMS = REPO_ROOT / ".specify/teams"
FIXTURE_TEAMS = REPO_ROOT / "tests/fixtures/teams"

pytestmark = [pytest.mark.integration]

requires_chain = pytest.mark.skipif(
    not GENERATOR.is_file() or not (SUMMARIZE / "project-db.py").is_file(),
    reason="generator or summarize-project chain unavailable",
)


def _pattern_of(team_md: Path) -> str:
    for line in team_md.read_text(encoding="utf-8").splitlines():
        if line.startswith("pattern:"):
            return line.split(":", 1)[1].strip()
    return ""


def _teams_by_pattern() -> dict[str, Path]:
    found: dict[str, Path] = {}
    for root in (REAL_TEAMS, FIXTURE_TEAMS):
        if not root.is_dir():
            continue
        for team_md in sorted(root.glob("*/team.md")):
            found.setdefault(_pattern_of(team_md), team_md.parent)
    return found


@pytest.fixture()
def sandbox(tmp_path: Path) -> Path:
    """A temp repo root carrying the agent definitions the roster references."""
    (tmp_path / ".specify/teams").mkdir(parents=True)
    agents_src = REPO_ROOT / ".specify/agents"
    for sub in ("templates", "instances"):
        dest = tmp_path / ".specify/agents" / sub
        dest.mkdir(parents=True, exist_ok=True)
        src = agents_src / sub
        if src.is_dir():
            for agent in src.glob("*.agent.md"):
                shutil.copy2(agent, dest / agent.name)
    return tmp_path


def _install(sandbox: Path, team_dir: Path) -> str:
    dest = sandbox / ".specify/teams" / team_dir.name
    shutil.copytree(team_dir, dest)
    return team_dir.name


def _run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, cwd=str(cwd))


@requires_chain
@pytest.mark.parametrize("pattern", ["continuous", "iteration", "serial", "parallel"])
def test_full_chain_per_pattern(sandbox: Path, pattern: str) -> None:
    teams = _teams_by_pattern()
    team_dir = teams.get(pattern)
    if team_dir is None:
        pytest.fail(
            f"no team available for pattern {pattern!r}; SC-001 requires one per pattern "
            f"(available: {sorted(teams)})"
        )
    slug = _install(sandbox, team_dir)

    # 1. generate the form from tracked artifacts alone — zero manual editing
    gen = _run(
        [sys.executable, str(GENERATOR), "--team", slug, "--json", "--repo-root", str(sandbox)],
        sandbox,
    )
    assert gen.returncode == 0, f"generator failed for {pattern}:\n{gen.stdout}\n{gen.stderr}"
    report = json.loads(gen.stdout)
    assert report["status"] == "produced"
    form = sandbox / report["form"]
    assert form.is_file()

    # 2. R-tier completeness — must be `ready`, not a blocking form-fill
    val = _run(
        [sys.executable, str(SUMMARIZE / "validate-project-input.py"),
         "--input", str(form), "--json"],
        sandbox,
    )
    assert val.returncode == 0, f"validation blocked for {pattern}:\n{val.stdout}\n{val.stderr}"
    verdict = json.loads(val.stdout)
    assert verdict["status"] == "ready", verdict
    assert verdict["missing_required"] == [], verdict["missing_required"]

    # 3. load — the database rejects anything that violates its constraints
    db = sandbox / "project.db"
    load = _run(
        [sys.executable, str(SUMMARIZE / "project-db.py"), "--db", str(db), "--load", str(form)],
        sandbox,
    )
    assert load.returncode == 0, f"load failed for {pattern}:\n{load.stdout}\n{load.stderr}"

    # 4. integrity check
    check = _run(
        [sys.executable, str(SUMMARIZE / "project-db.py"), "--db", str(db), "--check"], sandbox
    )
    assert check.returncode == 0, f"integrity check failed for {pattern}:\n{check.stdout}"


@requires_chain
def test_every_pattern_has_a_team_available() -> None:
    """SC-001 needs all four patterns represented (real teams + fixtures)."""
    teams = _teams_by_pattern()
    missing = {"continuous", "iteration", "serial", "parallel"} - teams.keys()
    assert not missing, f"no team for pattern(s): {sorted(missing)}"


@requires_chain
def test_phases_are_namespaced_by_team(sandbox: Path) -> None:
    """FG-16 — teams on different patterns must not share one phase sequence."""
    teams = _teams_by_pattern()
    slug = _install(sandbox, teams["serial"])
    gen = _run(
        [sys.executable, str(GENERATOR), "--team", slug, "--repo-root", str(sandbox)], sandbox
    )
    assert gen.returncode == 0, gen.stdout + gen.stderr
    doc = yaml.safe_load(
        next(sandbox.rglob("project-input.yaml")).read_text(encoding="utf-8")
    )
    assert doc["phases"], "no phases emitted"
    for phase in doc["phases"]:
        assert phase["phase_id"].startswith(f"{slug}."), phase
        assert phase["phase_name"].startswith(f"{slug} · "), phase


@requires_chain
def test_work_items_are_attributable_to_their_team(sandbox: Path) -> None:
    """FG-17 — attribution is machine-decidable from the id prefix and provenance."""
    teams = _teams_by_pattern()
    slug = _install(sandbox, teams["parallel"])
    assert _run(
        [sys.executable, str(GENERATOR), "--team", slug, "--repo-root", str(sandbox)], sandbox
    ).returncode == 0
    doc = yaml.safe_load(
        next(sandbox.rglob("project-input.yaml")).read_text(encoding="utf-8")
    )
    assert doc["work_items"]
    for row in doc["work_items"]:
        assert row["item_id"].startswith(f"{slug}."), row
        assert f"/teams/{slug}/" in row["source"], row


@requires_chain
def test_unknown_state_yields_no_fabricated_progress(sandbox: Path) -> None:
    """FR-006 — an item without a status signal must not become 0% or not-started."""
    teams = _teams_by_pattern()
    slug = _install(sandbox, teams["parallel"])  # fixture carries one `unknown` item
    assert _run(
        [sys.executable, str(GENERATOR), "--team", slug, "--repo-root", str(sandbox)], sandbox
    ).returncode == 0
    doc = yaml.safe_load(
        next(sandbox.rglob("project-input.yaml")).read_text(encoding="utf-8")
    )
    unknowns = [r for r in doc["work_items"] if not r.get("status")]
    assert unknowns, "fixture should contain an item with no status signal"
    for row in unknowns:
        assert "progress_pct" not in row, f"fabricated progress on an unknown item: {row}"


@requires_chain
def test_real_repo_project_directory_is_not_written(sandbox: Path) -> None:
    """FG-11 / FR-036 — generation must not touch the real delivery tree."""
    real_goal_dir = REPO_ROOT / ".specify/goal"
    before = sorted(p.name for p in real_goal_dir.iterdir()) if real_goal_dir.is_dir() else None
    teams = _teams_by_pattern()
    slug = _install(sandbox, teams["serial"])
    assert _run(
        [sys.executable, str(GENERATOR), "--team", slug, "--repo-root", str(sandbox)], sandbox
    ).returncode == 0
    after = sorted(p.name for p in real_goal_dir.iterdir()) if real_goal_dir.is_dir() else None
    assert before == after, "the real .specify/goal tree changed during a sandboxed run"
