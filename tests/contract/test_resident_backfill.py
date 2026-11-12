"""Contract tests for the resident-binding backfill action.

Feature 094, `contracts/unified-archive-and-migration.md` C-112 / C-113;
tasks rows T081 and T082 (FR-043, SC-012). Every assertion runs through the
engine CLI; the exhaustiveness sensor is exercised against a fixture copy so
the module itself proves it can turn red (no tree edit).

Feature 101 re-points the Anchor resident's filename to `anchor.md` (the archive
layer's definition filename); the legacy `goal.md` filename remains a readable
retained-source shape for the membership check the engine documents.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

from script_api import run_engine_in_process

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts/python/goal-utils.py"

GOAL_RESIDENT = """---
status: {status}
created: 2026-10-04
updated: 2026-10-05
---

# Anchor: {slug}

## Objective

Hold a resident Anchor definition that predates the binding model.

## Success Criteria

1. The resident becomes readable by the engine.

## History

- 2026-10-04 — created before the binding model existed.
"""

TEAM_RESIDENT = """---
name: resident team {slug}
slug: {slug}
description: A resident team that predates the binding model.
goal: >-
  Keep the resident team readable through the backfill.
goal_slug: {goal_slug}
lifecycle_state: {lifecycle}
territory:
  write:
    - .specify/specs/000-resident/**
---

# Team: {slug}
"""

BINDING = ("binding:\n"
           "  owner: human\n"
           "  owner_id: human\n"
           "  origin: null\n")


def _run(root: Path, *args: str) -> subprocess.CompletedProcess:
    return run_engine_in_process(ENGINE, [*args, "--repo-root", str(root), "--json"])


def _payload(proc: subprocess.CompletedProcess) -> dict:
    assert proc.stdout.strip(), f"no JSON payload; stderr={proc.stderr!r}"
    return json.loads(proc.stdout)


def _seed_goal(root: Path, slug: str, status: str = "active") -> Path:
    path = root / ".specify/anchoring" / slug / "anchor.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(GOAL_RESIDENT.format(slug=slug, status=status), encoding="utf-8")
    return path


def _seed_team(root: Path, slug: str, goal_slug: str = "resident",
               lifecycle: str = "active") -> Path:
    path = root / ".specify/teams" / slug / "team.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(TEAM_RESIDENT.format(slug=slug, goal_slug=goal_slug,
                                         lifecycle=lifecycle), encoding="utf-8")
    return path


def _snapshot(root: Path) -> list[tuple]:
    rows = []
    for path in sorted(root.rglob("*")):
        if path.is_file():
            rows.append((str(path.relative_to(root)), path.stat().st_mtime_ns,
                         hashlib.sha256(path.read_bytes()).hexdigest()))
    return rows


def _hash_minus_binding(path: Path) -> str:
    kept: list[str] = []
    skipping = False
    for line in path.read_text(encoding="utf-8").splitlines(keepends=True):
        if skipping:
            if line[:1] in (" ", "\t"):
                continue
            skipping = False
        if line.startswith("binding:"):
            skipping = True
            continue
        kept.append(line)
    return hashlib.sha256("".join(kept).encode("utf-8")).hexdigest()


def _assert_every_resident_bound(root: Path) -> None:
    """The exhaustiveness sensor: every resident answers the binding read action."""
    residents = [(path, "goal") for path in sorted((root / ".specify/anchoring").glob("*/anchor.md"))]
    residents += [(path, "teams") for path in sorted((root / ".specify/teams").glob("*/team.md"))]
    assert residents, "the fixture must contain residents to judge"
    for path, kind in residents:
        slug = path.parent.name
        proc = _run(root, "binding", kind, slug)
        assert proc.returncode == 0, (
            f"{path} carries no complete binding record: {proc.stdout!r}")
        payload = _payload(proc)
        assert payload["owner"] == "human" and payload["owner_id"] == "human"
        assert payload["origin"] is None


# ---------------------------------------------------------------------------
# T082 / C-113 — dry run writes nothing; apply inserts; second run is a noop;
# an incomplete binding block is refused, never overwritten
# ---------------------------------------------------------------------------

def test_a_second_backfill_writes_nothing_and_refuses_an_incomplete_binding(tmp_path):
    goal = _seed_goal(tmp_path, "resident")
    team = _seed_team(tmp_path, "resident-crew")
    original_goal = _hash_minus_binding(goal)
    original_team = _hash_minus_binding(team)

    dry = _run(tmp_path, "backfill-bindings", "--dry-run")
    assert dry.returncode == 0, dry.stdout + dry.stderr
    planned = _payload(dry)["definitions"]
    assert {(row["kind"], row["slug"], row["result"]) for row in planned} == {
        ("goal", "resident", "backfilled"),
        ("teams", "resident-crew", "backfilled"),
    }
    assert "binding:" not in goal.read_text(encoding="utf-8"), (
        "a dry run writes nothing (C-112)")

    applied = _run(tmp_path, "backfill-bindings", "--apply")
    assert applied.returncode == 0, applied.stdout + applied.stderr
    for path in (goal, team):
        text = path.read_text(encoding="utf-8")
        assert BINDING in text
        assert _hash_minus_binding(path) == (original_goal if path == goal
                                             else original_team), (
            "every other byte of the definition stays identical (C-113)")
    assert _payload(_run(tmp_path, "binding", "goal", "resident"))["origin"] is None

    before = _snapshot(tmp_path)
    second = _run(tmp_path, "backfill-bindings", "--apply")
    assert second.returncode == 0
    rows = _payload(second)["definitions"]
    assert len(rows) == 2
    assert {row["result"] for row in rows} == {"already-bound"}
    assert _snapshot(tmp_path) == before, "a second backfill performs zero writes"

    # C-113 — an incomplete binding block is refused, named, and not overwritten.
    incomplete = tmp_path / ".specify/anchoring/broken/anchor.md"
    incomplete.parent.mkdir(parents=True)
    incomplete.write_text(
        GOAL_RESIDENT.format(slug="broken", status="active")
        .replace("updated: 2026-10-05\n", "updated: 2026-10-05\nbinding:\n  owner: human\n"),
        encoding="utf-8")
    before_bytes = incomplete.read_bytes()
    refused = _run(tmp_path, "backfill-bindings", "--apply")
    assert refused.returncode == 2, f"stdout={refused.stdout!r} stderr={refused.stderr!r}"
    error = _payload(refused)["error"]
    assert "binding-incomplete" in error and "broken" in error
    assert incomplete.read_bytes() == before_bytes, "an incomplete block is never overwritten"


# ---------------------------------------------------------------------------
# T081 / C-112 — exhaustive over the unified archive; zero writes on re-run;
# the sensor turns red when one resident's binding block disappears
# ---------------------------------------------------------------------------

def test_every_archive_resident_carries_a_binding_after_backfill(tmp_path):
    _seed_goal(tmp_path, "resident")
    _seed_goal(tmp_path, "terminal-resident", status="achieved")
    _seed_team(tmp_path, "resident-crew", goal_slug="resident")
    _seed_team(tmp_path, "archived-crew", goal_slug="resident", lifecycle="archived")

    applied = _run(tmp_path, "backfill-bindings", "--apply")
    assert applied.returncode == 0, applied.stdout + applied.stderr
    counts = _payload(applied)["counts"]
    assert counts["backfilled"] == 4

    _assert_every_resident_bound(tmp_path)

    before = _snapshot(tmp_path)
    second = _run(tmp_path, "backfill-bindings", "--apply")
    assert second.returncode == 0
    rows = _payload(second)["definitions"]
    assert len(rows) == 4, "one already-bound line per definition (C-113)"
    assert {row["result"] for row in rows} == {"already-bound"}
    assert _snapshot(tmp_path) == before

    # Synthetic mutation over a fixture copy (no tree edit): drop one resident's
    # binding block and prove the same sensor turns red.
    mutated = tmp_path / "mutated"
    shutil.copytree(tmp_path / ".specify", mutated / ".specify")
    victim = mutated / ".specify/anchoring/terminal-resident/anchor.md"
    text = victim.read_text(encoding="utf-8")
    victim.write_text(text.replace(BINDING, ""), encoding="utf-8")
    with pytest.raises(AssertionError):
        _assert_every_resident_bound(mutated)
