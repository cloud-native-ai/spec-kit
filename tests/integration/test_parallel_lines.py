"""Integration test: the two peer lines deliver without each other (FR-014, SC-005).

Tasks row T043 (blocked by T015 and T054). Two fixtures under `.specify/.tmp/s094/`:

* **Peer A — SDD-only, no goal/team.** The threshold decision on its `tasks.md` returns
  `direct` at equality (complex iff task count > threshold), so that run formally creates
  no goal/team. The empty archive is the *decision's* result, not a skipped creation.
* **Peer B — goal+team, no spec directory.** Both definitions exist on disk with a
  complete canonical binding, the ownership read answers from the record, and the team's
  five run-precondition checks resolve — all with `.specify/specs/` absent from the
  fixture. Neither definition is skipped to fake the relation.

Injecting a "requires the other line" precondition into either branch turns this module
red: peer A would fail while its goal/team are absent, peer B would fail while its spec
directory is absent.

Red-first note: the SDD branch drives the engine's `handoff-decision` action (row T054),
whose implementation is outside this fork's write domain and not yet landed, so the
module is authored red before that engine row lands. The threshold value is read from
its declaration fact, never repeated here.
"""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts/python/goal-utils.py"
READER = REPO_ROOT / "scripts/python/declaration_reader.py"
THRESHOLD_FACT = REPO_ROOT / "shared/declarations/facts/goal-team-handoff-threshold.yaml"

RUN_ID = "r20261109T064500Z-094a"
TASK_ROW = "- [ ] T{n:03d} deliver the fixture row"


def _load_reader():
    spec = importlib.util.spec_from_file_location("declaration_reader_094_parallel", READER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _threshold() -> int:
    body = _load_reader().parse_subset(
        THRESHOLD_FACT.read_text(encoding="utf-8"), str(THRESHOLD_FACT))
    value = body["statement"]["threshold"]
    assert str(value).isdigit(), f"threshold must be an integer literal, got {value!r}"
    return int(value)


def _run(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ENGINE), *args, "--repo-root", str(root), "--json"],
        capture_output=True, text=True, cwd=REPO_ROOT)


def _tasks_file(directory: Path, count: int) -> Path:
    path = directory / "tasks.md"
    rows = "\n".join(TASK_ROW.format(n=index) for index in range(1, count + 1))
    path.write_text(f"# Tasks\n\n{rows}\n", encoding="utf-8")
    return path


def _seed_bound_goal(root: Path, slug: str = "alpha") -> Path:
    path = root / ".specify/anchoring" / slug / "goal.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n"
        "status: active\n"
        "created: 2026-11-09\n"
        "updated: 2026-11-09\n"
        "binding:\n"
        "  owner: command-run\n"
        f"  owner_id: {RUN_ID}\n"
        "  origin: null\n"
        "---\n\n"
        f"# Goal: {slug}\n\n"
        "## Objective\n\n"
        "Deliver the goal+team peer fixture without a spec directory.\n\n"
        "## Success Criteria\n\n"
        "1. The definition stands alone.\n\n"
        "## History\n\n"
        "- 2026-11-09 — created.\n",
        encoding="utf-8")
    return path


def _seed_bound_team(root: Path, slug: str = "crew", goal_slug: str = "alpha") -> Path:
    path = root / ".specify/teams" / slug / "team.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n"
        "lifecycle_state: active\n"
        f"goal_slug: {goal_slug}\n"
        "binding:\n"
        "  owner: command-run\n"
        f"  owner_id: {RUN_ID}\n"
        "  origin: null\n"
        "---\n\n"
        f"# Team: {slug}\n",
        encoding="utf-8")
    return path


@pytest.fixture()
def sandbox():
    base = REPO_ROOT / ".specify/.tmp/s094"
    base.mkdir(parents=True, exist_ok=True)
    root = Path(tempfile.mkdtemp(prefix="parallel-", dir=str(base)))
    try:
        yield root
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_both_peer_fixtures_deliver_independently(sandbox):
    threshold = _threshold()

    # -- Peer A: SDD-only, no goal/team -------------------------------------
    sdd = sandbox / "sdd-only"
    sdd.mkdir()
    tasks = _tasks_file(sdd, threshold)  # equality stays on the simple side

    proc = _run(REPO_ROOT, "handoff-decision", "--tasks", str(tasks))
    assert proc.returncode == 0, (
        f"the SDD line's threshold decision failed: {proc.stdout!r} {proc.stderr!r}")
    payload = json.loads(proc.stdout)
    assert payload["task_count"] == threshold
    assert payload["decision"] == "direct", (
        "a spec at or below the threshold is direct; no goal/team is created (FR-039)")
    assert payload["creation"]["on_direct"] == "none"
    assert not (sdd / ".specify/anchoring").exists(), (
        "the direct decision creates no goal — the absence is the decision's result, "
        "not a skipped creation")
    assert not (sdd / ".specify/teams").exists(), (
        "the direct decision creates no team")

    # -- Peer B: goal+team, no spec directory -------------------------------
    crew = sandbox / "goal-team"
    goal_path = _seed_bound_goal(crew)
    team_path = _seed_bound_team(crew)
    assert goal_path.is_file() and team_path.is_file(), (
        "the goal+team fixture must actually contain both creations, never skip one")
    assert not (crew / ".specify/specs").exists(), (
        "the goal+team line owns its definitions with no spec directory present")

    goal_read = _run(crew, "binding", "goal", "alpha")
    assert goal_read.returncode == 0, (
        f"the goal binding must read without a spec dir: {goal_read.stdout!r}")
    goal_payload = json.loads(goal_read.stdout)
    assert goal_payload["owner"] == "command-run"
    assert goal_payload["origin"] is None

    team_read = _run(crew, "binding", "team", "crew")
    assert team_read.returncode == 0, (
        f"the team binding must read without a spec dir: {team_read.stdout!r}")
    team_payload = json.loads(team_read.stdout)
    assert team_payload["owner"] == "command-run"
    assert team_payload["lifecycle"] == "active"

    checks = _run(crew, "run-checks", "crew")
    assert checks.returncode == 0, (
        "the goal+team line completes its delivery — the five run-precondition checks "
        f"resolve without a spec: {checks.stdout!r} {checks.stderr!r}")
    verdict = json.loads(checks.stdout)
    assert verdict["verdict"] == "ok" and verdict["blocked"] is False, (
        f"run-checks must resolve on the standalone team: {verdict!r}")
    assert verdict["goal_slug"] == "alpha", (
        "the team's identity is its goal_slug, resolved from the record")

    assert not (crew / ".specify/specs").exists(), (
        "no line created a spec directory to satisfy the other")
