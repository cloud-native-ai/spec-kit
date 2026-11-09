"""Integration test over the real tree's SHAPE — migration clears every residual.

Feature 094, FR-042 / SC-003; tasks row T032. The fixture reproduces the measured
shape of this repository's spec-local trees (per-slug subdirectories, a goal slug
that departs from its spec-directory name, team slugs that depart as well, one
non-default spec per kind) rather than copying live files: the real-tree apply is
a dated evidence run (T079, wp07) and must not be a precondition of this module,
whose reading has to stay stable before and after that run.

Boundary disclosed, not hidden: the two one-level team files the analyze-repair
census found (`<spec>/team/team.md`, no slug directory) are outside the residual
probe's declared form (C-43) and are therefore not part of this fixture's
assertion — the probe reports exactly the two declared globs.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts/python/goal-utils.py"

GOAL_SOURCE = """---
status: active
created: 2026-11-09
updated: 2026-11-09
---

# Goal: {slug}

## Objective

Carry the fixture goal into the unified archive without losing its content.

## Success Criteria

1. Every source file stays readable under trees/.

## History

- 2026-11-09 — created in the spec-local layout.
"""

TEAM_SOURCE = """---
name: fixture team {slug}
slug: {slug}
description: A fixture team modelled on the measured spec-local shape.
goal: >-
  Carry the fixture team into the unified archive with its run history intact.
goal_slug: {goal_slug}
lifecycle_state: {lifecycle}
scope: spec
spec_dir: .specify/specs/{spec}
territory:
  write:
    - .specify/specs/{spec}/**
---

# Team: {slug}
"""

#: The measured shape: eight spec-local pairs in the 085–092 layout. Two entries carry
#: slugs that depart from their spec-directory names, exactly as 088/089 do today.
SHAPE = {
    "085-sdd-temporary-goal-team": ("085-sdd-temporary-goal-team", "085-sdd-temporary-goal-team", "active"),
    "086-efficient-test-execution": ("086-efficient-test-execution", "086-efficient-test-execution", "active"),
    "087-arch-diagram-docs": ("087-arch-diagram-docs", "087-reporting-dogfood", "archived"),
    "088-speckit-visualization": ("088-speckit-visualization", "088-reporting-dogfood", "archived"),
    "089-script-interface-contract": ("script-interface-contract", "086-script-interface-contract", "archived"),
    "090-re-anchoring": ("090-re-anchoring", "090-re-anchoring", "archived"),
    "091-auto-git-closeout": ("091-auto-git-closeout", "091-auto-git-closeout", "archived"),
    "092-non-disposable": ("092-non-disposable", "092-non-disposable", "active"),
}


def _run(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ENGINE), *args, "--repo-root", str(root), "--json"],
        capture_output=True, text=True, cwd=REPO_ROOT)


def _payload(proc: subprocess.CompletedProcess) -> dict:
    assert proc.stdout.strip(), f"no JSON payload; stderr={proc.stderr!r}"
    return json.loads(proc.stdout)


def _build_shape(root: Path) -> dict:
    recorded: dict[str, list[str]] = {"goal": [], "teams": []}
    for spec, (goal_slug, team_slug, lifecycle) in SHAPE.items():
        goal_tree = root / ".specify/specs" / spec / "goal" / goal_slug
        goal_tree.mkdir(parents=True)
        (goal_tree / "goal.md").write_text(
            GOAL_SOURCE.format(slug=goal_slug), encoding="utf-8")
        (goal_tree / "summary").mkdir()
        (goal_tree / "summary" / "summary.md").write_text(
            f"derived summary for {goal_slug}\n", encoding="utf-8")
        team_tree = root / ".specify/specs" / spec / "team" / team_slug
        team_tree.mkdir(parents=True)
        (team_tree / "team.md").write_text(
            TEAM_SOURCE.format(spec=spec, slug=team_slug, goal_slug=goal_slug,
                               lifecycle=lifecycle),
            encoding="utf-8")
        (team_tree / "runs").mkdir()
        (team_tree / "runs" / "20261109T000000Z-report.md").write_text(
            f"run report for {team_slug}\n", encoding="utf-8")
        recorded["goal"].append(goal_slug)
        recorded["teams"].append(team_slug)
    return recorded


def test_every_source_tree_stays_readable_after_migration(tmp_path):
    slugs = _build_shape(tmp_path)

    before = _payload(_run(tmp_path, "probe-residual"))
    assert before["counts"] == {"goal": len(SHAPE), "teams": len(SHAPE)}

    applied = _run(tmp_path, "migrate-archive", "--apply")
    assert applied.returncode == 0, applied.stdout + applied.stderr

    after = _payload(_run(tmp_path, "probe-residual"))
    assert after["counts"] == {"goal": 0, "teams": 0}, (
        "after migration the residual count is zero (SC-003)")

    for spec, (goal_slug, team_slug, _lifecycle) in SHAPE.items():
        goal_target = tmp_path / ".specify/anchoring" / goal_slug / "goal.md"
        team_target = tmp_path / ".specify/teams" / team_slug / "team.md"
        assert goal_target.is_file(), f"unified definition missing: {goal_target}"
        assert team_target.is_file(), f"unified definition missing: {team_target}"
        assert f"origin: {spec}\n" in goal_target.read_text(encoding="utf-8")
        assert f"origin: {spec}\n" in team_target.read_text(encoding="utf-8")
        archived_goal = (tmp_path / ".specify/archive/goal-team/trees" / spec
                         / "goal" / goal_slug)
        archived_team = (tmp_path / ".specify/archive/goal-team/trees" / spec
                         / "teams" / team_slug)
        assert (archived_goal / "goal.md").is_file()
        assert (archived_goal / "summary" / "summary.md").is_file()
        assert (archived_team / "team.md").is_file()
        assert (archived_team / "runs" / "20261109T000000Z-report.md").is_file()

    receipts = tmp_path / ".specify/archive/goal-team/receipts"
    assert len(list(receipts.glob("goal-*.yaml"))) == len(slugs["goal"])
    assert len(list(receipts.glob("teams-*.yaml"))) == len(slugs["teams"])
