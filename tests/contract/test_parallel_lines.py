"""Contract tests: the two peer lines, the binding-only ownership answer (US3).

Feature 094, `contracts/binding-and-lifecycle.md` C-25/C-26/C-28/C-29/C-30; tasks rows
T042 and the guards of T045–T048. Every assertion drives the engines as subprocesses (or
reads the two owner surfaces by path), so what is pinned is the surface a consumer calls.

The subject is the **negative**: neither line requires the other to exist, ownership is
answered by the binding record and never by a directory position, one goal admits many
teams without copying its content, the routing layer records an archive layer, and
`run-checks` carries the loaded team's binding additively.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from script_api import run_engine_in_process

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
GOAL_ENGINE = REPO_ROOT / "scripts/python/goal-utils.py"
ROUTE_ENGINE = REPO_ROOT / "scripts/python/sdd-route.py"
TEAM_MECHANISM = (
    REPO_ROOT / "skills/internal/create-team/SKILL.md",
    REPO_ROOT / "skills/internal/create-team/references/create-mode.md",
    REPO_ROOT / "skills/internal/create-team/references/conceptual-model.md",
)

RUN_ID = "r20261109T064500Z-094a"
OTHER_RUN_ID = "r20261110T010203Z-094b"

OBJECTIVE = "PEER-OBJECTIVE-SENTINEL hold the two lines parallel."
CRITERION = "PEER-CRITERION-SENTINEL each line delivers alone."


def _run(root: Path, *args: str) -> subprocess.CompletedProcess:
    return run_engine_in_process(GOAL_ENGINE, [*args, "--repo-root", str(root), "--json"])


def _payload(proc: subprocess.CompletedProcess) -> dict:
    assert proc.returncode == 0, f"{proc.args}: {proc.stdout!r} {proc.stderr!r}"
    return json.loads(proc.stdout)


def _binding_block(owner: str = "command-run", owner_id: str = RUN_ID) -> str:
    return f"binding:\n  owner: {owner}\n  owner_id: {owner_id}\n  origin: null\n"


def _seed_goal(root: Path, slug: str = "alpha", *, owner: str = "command-run",
               layer: str = ".specify/anchoring") -> Path:
    path = root / layer / slug / "goal.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n"
        "status: active\n"
        "created: 2026-11-09\n"
        "updated: 2026-11-09\n"
        f"{_binding_block(owner)}"
        "---\n\n"
        f"# Goal: {slug}\n\n"
        "## Objective\n\n"
        f"{OBJECTIVE}\n\n"
        "## Success Criteria\n\n"
        f"1. {CRITERION}\n\n"
        "## History\n\n"
        "- 2026-11-09 — created.\n",
        encoding="utf-8")
    return path


def _seed_team(root: Path, slug: str = "crew", *, goal_slug: str = "alpha",
               owner: str = "sdd-run", lifecycle: str = "active",
               layer: str = ".specify/teams") -> Path:
    path = root / layer / slug / "team.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n"
        f"name: {slug}\n"
        f"slug: {slug}\n"
        f"lifecycle_state: {lifecycle}\n"
        f"goal_slug: {goal_slug}\n"
        f"{_binding_block(owner, OTHER_RUN_ID)}"
        "---\n\n"
        f"# Team: {slug}\n",
        encoding="utf-8")
    return path


def _tasks_file(directory: Path, count: int) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "tasks.md"
    rows = "\n".join(f"- [ ] T{n:03d} deliver a fixture row" for n in range(1, count + 1))
    path.write_text(f"# Tasks\n\n{rows}\n", encoding="utf-8")
    return path


@pytest.fixture()
def sandbox():
    base = REPO_ROOT / ".specify/.tmp/s094"
    base.mkdir(parents=True, exist_ok=True)
    root = Path(tempfile.mkdtemp(prefix="parallel-lines-", dir=str(base)))
    try:
        yield root
    finally:
        shutil.rmtree(root, ignore_errors=True)


# ---------------------------------------------------------------------------
# T042 / C-25 — the negative: neither line requires the other to exist
# ---------------------------------------------------------------------------

def test_neither_line_requires_the_other_to_exist(sandbox):
    # Peer A — SDD-only: a spec directory and its task table, no goal/team anywhere.
    sdd = sandbox / "sdd-only"
    declaration = sdd / "shared/declarations"
    (declaration / "facts").mkdir(parents=True)
    shutil.copy(REPO_ROOT / "shared/declarations/contract.yaml",
                declaration / "contract.yaml")
    shutil.copy(REPO_ROOT / "shared/declarations/facts/goal-team-handoff-threshold.yaml",
                declaration / "facts/goal-team-handoff-threshold.yaml")
    (sdd / ".specify/specs/999-sdd-peer").mkdir(parents=True)
    tasks = _tasks_file(sdd / ".specify/specs/999-sdd-peer", 3)

    decision = _payload(_run(sdd, "handoff-decision", "--tasks", str(tasks)))
    assert decision["decision"] == "direct", (
        "a small spec decides direct without any goal/team existing")
    assert decision["creation"]["on_direct"] == "none"
    listing = _payload(_run(sdd, "list"))
    assert listing["goals"] == [], "the SDD line reads an empty archive without failing"

    # Peer B — goal+team with no spec directory at all.
    peer = sandbox / "goal-team-only"
    _seed_goal(peer)
    _seed_team(peer)
    assert not (peer / ".specify/specs").exists(), "no spec directory is created to satisfy"
    assert _payload(_run(peer, "binding", "goal", "alpha"))["owner"] == "command-run"
    assert _payload(_run(peer, "binding", "team", "crew"))["owner"] == "sdd-run"
    checks = _payload(_run(peer, "run-checks", "crew"))
    assert checks["goal_slug"] == "alpha"


# ---------------------------------------------------------------------------
# T045 / C-26 — ownership is answered by the record, never by a path prefix
# ---------------------------------------------------------------------------

def test_no_owner_is_derived_from_a_path_prefix(sandbox):
    _seed_goal(sandbox, owner="command-run")
    _seed_team(sandbox, owner="sdd-run")
    # A residual copy under a spec directory carries a DIFFERENT owner. If any read
    # inferred ownership from a directory position, this file would win for "alpha".
    _seed_goal(sandbox, owner="human", layer=".specify/specs/999-peer/goal")
    _seed_team(sandbox, owner="human", layer=".specify/specs/999-peer/team")

    goal = _payload(_run(sandbox, "binding", "goal", "alpha"))
    team = _payload(_run(sandbox, "binding", "team", "crew"))
    assert goal["owner"] == "command-run", (
        "the archive record answers, not the spec-local copy that happens to share the slug")
    assert team["owner"] == "sdd-run"
    assert goal["archive_layer"] == "goal" and team["archive_layer"] == "teams"
    assert goal["path"] == ".specify/anchoring/alpha/goal.md"

    # The read action routes through the record reader the engine already owns; no
    # second ownership computation lives beside it.
    source = GOAL_ENGINE.read_text(encoding="utf-8")
    body = source[source.index("def binding_payload"):]
    body = body[:body.index("\ndef ")]
    assert "read_binding(path)" in body, (
        "binding_payload must answer through read_binding, the one record reader")

    # The team mechanism declares a single team store; a second, position-derived store
    # would reintroduce ownership-by-directory through the back door.
    spec_local = re.compile(r"(?i)(?:\.specify/specs/[^\s`]*|\<spec-dir\>|\<spec\>)/team/")
    offenders = []
    for path in TEAM_MECHANISM:
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if spec_local.search(line):
                offenders.append(f"{path.relative_to(REPO_ROOT)}:{lineno}: {line.strip()[:120]}")
    assert not offenders, (
        "the team mechanism names a position-derived team store; ownership is answered "
        f"by the binding record only: {offenders}")


# ---------------------------------------------------------------------------
# T046 / C-28 — N teams : 1 goal, identity only, closed team lifecycle
# ---------------------------------------------------------------------------

def test_many_teams_may_bind_one_goal_and_no_goal_content_is_copied(sandbox):
    _seed_goal(sandbox)
    crew_a = _seed_team(sandbox, slug="crew-a", owner="sdd-run")
    crew_b = _seed_team(sandbox, slug="crew-b", owner="command-run")

    for slug in ("crew-a", "crew-b"):
        row = _payload(_run(sandbox, "binding", "team", slug))
        assert row["owner"] in ("sdd-run", "command-run")
        checks = _payload(_run(sandbox, "run-checks", slug))
        assert checks["goal_slug"] == "alpha", (
            "both teams resolve the one goal through goal_slug — the only binding axis")

    for path in (crew_a, crew_b):
        text = path.read_text(encoding="utf-8")
        assert OBJECTIVE not in text and CRITERION not in text, (
            f"{path.name} copies the goal's objective/criteria; the team stores identity only")

    bad = _seed_team(sandbox, slug="crew-c", lifecycle="achieved")
    assert bad.is_file()
    proc = _run(sandbox, "run-checks", "crew-c")
    assert proc.returncode != 0, (
        "a team lifecycle outside active/archived is refused, never run")
    assert "team-lifecycle" in proc.stdout, (
        f"the refusal names the closed lifecycle domain: {proc.stdout!r}")


# ---------------------------------------------------------------------------
# T047 / C-29 — authorize records the archive layer, not a retired scope name
# ---------------------------------------------------------------------------

def _seed_authorizable(root: Path) -> tuple[Path, str]:
    team = root / ".specify/teams/crew/team.md"
    team.parent.mkdir(parents=True, exist_ok=True)
    team.write_text(
        "---\n"
        "name: crew\n"
        "slug: crew\n"
        "goal_slug: alpha\n"
        "seats:\n"
        "  seat-driver:\n"
        "    sdd-invocation: allowed\n"
        "members:\n"
        "  - agent: seat-driver\n"
        "    role: driver-host\n"
        "    lifecycle: persistent\n"
        "---\n\n"
        "# Team: crew\n",
        encoding="utf-8")
    agent = root / ".specify/agents/instances/seat-driver.agent.md"
    agent.parent.mkdir(parents=True, exist_ok=True)
    agent.write_text(
        "---\n"
        "name: seat-driver\n"
        "description: fixture agent\n"
        "sdd-invocation: allowed\n"
        "---\n\n"
        "# seat-driver\n",
        encoding="utf-8")
    return agent, "seat-driver"


def test_authorize_records_the_archive_layer_not_a_scope_name(sandbox):
    agent, seat = _seed_authorizable(sandbox)
    base = [sys.executable, str(ROUTE_ENGINE), "--action", "authorize",
            "--agent", str(agent), "--team", "crew", "--seat", seat,
            "--format", "json"]

    proc = subprocess.run(base, capture_output=True, text=True, cwd=str(sandbox))
    assert proc.returncode == 0, f"{proc.stdout!r} {proc.stderr!r}"
    record = json.loads(proc.stdout)
    assert record["effective"] == "allowed"
    assert record["archive_layer"] == "teams", (
        "the record names the archive layer that answered (C-9 value set)")
    assert "scope" not in record, (
        "the retired scope key is replaced in place, not carried beside the new one")

    for retired in ("spec", "global"):
        bad = subprocess.run(base[:-2] + ["--scope", retired, "--format", "json"],
                             capture_output=True, text=True, cwd=str(sandbox))
        assert bad.returncode == 2, (
            f"--scope {retired} must fail with argparse's invalid choice, exit 2")

    named = subprocess.run(base[:-2] + ["--scope", "teams", "--format", "json"],
                           capture_output=True, text=True, cwd=str(sandbox))
    assert named.returncode == 0, f"{named.stdout!r} {named.stderr!r}"
    assert json.loads(named.stdout)["archive_layer"] == "teams"


# ---------------------------------------------------------------------------
# T048 / C-30 — run-checks carries the binding; the resolution keys are unchanged
# ---------------------------------------------------------------------------

def test_run_checks_carries_the_binding_and_keeps_its_resolution_keys(sandbox):
    _seed_goal(sandbox)
    team = _seed_team(sandbox, owner="sdd-run")
    payload = _payload(_run(sandbox, "run-checks", "crew"))
    assert payload["binding"] == {"owner": "sdd-run", "owner_id": OTHER_RUN_ID,
                                  "origin": None}, (
        "the payload carries the loaded team's binding record verbatim")
    assert set(payload["resolution"]) == {"effective", "source", "declared_focus"}, (
        "the existing resolution keys are unchanged; the binding is additive")

    # The record is the source: rewriting it changes the carried binding.
    team.write_text(
        team.read_text(encoding="utf-8").replace(
            f"owner_id: {OTHER_RUN_ID}", f"owner_id: {RUN_ID}"),
        encoding="utf-8")
    reread = _payload(_run(sandbox, "run-checks", "crew"))
    assert reread["binding"]["owner_id"] == RUN_ID

    # A team that predates the binding model keeps working; the key is additive and
    # reports the absence instead of failing the run.
    legacy = sandbox / ".specify/teams/legacy/team.md"
    legacy.parent.mkdir(parents=True)
    legacy.write_text(
        "---\nname: legacy\nslug: legacy\ngoal_slug: alpha\n---\n\n# Team: legacy\n",
        encoding="utf-8")
    old = _payload(_run(sandbox, "run-checks", "legacy"))
    assert old["binding"] is None, (
        "an unbound legacy team reads binding: null — additive, never a behaviour change")
