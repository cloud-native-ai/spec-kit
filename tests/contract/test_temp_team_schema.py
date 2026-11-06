"""Contract tests for the spec-local Temporary Team schema (Feature 085, T030/T032)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_DIR = REPO_ROOT / ".specify/specs/085-sdd-temporary-goal-team"
TEAM_MD = SPEC_DIR / "team/085-sdd-temporary-goal-team/team.md"
GOAL_UTILS = REPO_ROOT / "scripts/python/goal-utils.py"
SDD_ROUTE = REPO_ROOT / "scripts/python/sdd-route.py"
CANONICAL_STAGES = {
    "requirements", "clarify", "plan", "tasks",
    "checklist", "analyze", "implement", "review",
}


def _text() -> str:
    assert TEAM_MD.is_file(), f"temporary team missing: {TEAM_MD}"
    return TEAM_MD.read_text(encoding="utf-8")


def _frontmatter(text: str) -> list[str]:
    assert text.startswith("---\n"), "team.md must start with frontmatter"
    end = text.index("\n---", 4)
    return text[4:end].splitlines()


def _stage_blocks(fm: list[str]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    in_stage = False
    current = None
    for line in fm:
        if line.strip() == "stage_seats:":
            in_stage = True
            continue
        if in_stage and line and not line.startswith(" "):
            break
        if not in_stage:
            continue
        if line.startswith("  ") and not line.startswith("    ") and line.strip().endswith(":"):
            current = line.strip()[:-1]
            out[current] = {"seats": [], "max_parallel": None}
        elif current and line.strip().startswith("seats:"):
            raw = line.split(":", 1)[1].strip().strip("[]")
            out[current]["seats"] = [s.strip() for s in raw.split(",") if s.strip()]
        elif current and line.strip().startswith("max_parallel:"):
            out[current]["max_parallel"] = int(line.split(":", 1)[1].strip())
    return out


def _members(fm: list[str]) -> list[str]:
    out = []
    in_members = False
    for line in fm:
        if line.strip() == "members:":
            in_members = True
            continue
        if in_members and line and not line.startswith(" "):
            break
        if in_members and line.strip().startswith("- agent:"):
            out.append(line.split(":", 1)[1].strip())
    return out


def test_scope_and_lifecycle_fields():
    fm = "\n".join(_frontmatter(_text()))
    assert "scope: spec" in fm
    assert "spec_dir: .specify/specs/085-sdd-temporary-goal-team" in fm
    assert "goal_slug: 085-sdd-temporary-goal-team" in fm
    assert "lifecycle_state: active" in fm
    assert "isolation: worktree" in fm
    assert "requested: 24" in fm
    assert "effective: 18" in fm


def test_stage_seat_keys_are_canonical_and_bounded():
    blocks = _stage_blocks(_frontmatter(_text()))
    assert set(blocks) == CANONICAL_STAGES
    for stage, block in blocks.items():
        assert block["max_parallel"] is not None, f"{stage}: max_parallel missing"
        assert 1 <= block["max_parallel"] <= 18, f"{stage}: max_parallel out of bounds"


def test_every_stage_seat_resolves_to_a_member():
    members = set(_members(_frontmatter(_text())))
    assert members, "members block is empty"
    for stage, block in _stage_blocks(_frontmatter(_text())).items():
        for seat in block["seats"]:
            assert seat in members, f"{stage}: seat {seat!r} is not a member"


def test_team_stage_dimension_is_not_overloaded():
    fm = "\n".join(_frontmatter(_text()))
    # The members carry role/lifecycle, never an SDD-stage value in a `stage:` key.
    for stage in CANONICAL_STAGES:
        assert f"stage: {stage}" not in fm, f"SDD stage {stage!r} leaked into the Team Stage dimension"


def test_seats_map_is_block_style():
    fm = _frontmatter(_text())
    in_seats = False
    for line in fm:
        if line.strip() == "seats:":
            in_seats = True
            continue
        if in_seats and line and not line.startswith(" "):
            break
        if in_seats:
            assert "{" not in line and "}" not in line, "seats must be a block map, not flow style"


def test_spec_scoped_run_checks_resolves_the_team():
    proc = subprocess.run(
        [sys.executable, str(GOAL_UTILS), "run-checks", "085-sdd-temporary-goal-team",
         "--scope", "spec", "--spec-dir", str(SPEC_DIR), "--json"],
        capture_output=True, text=True, cwd=REPO_ROOT)
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["verdict"] == "ok"
    assert payload["goal_slug"] == "085-sdd-temporary-goal-team"


def test_spec_scoped_authorize_resolves_the_team():
    proc = subprocess.run(
        [sys.executable, str(SDD_ROUTE), "--action", "authorize",
         "--agent", "agents/sdd-plan-coordinator.agent.md",
         "--team", "085-sdd-temporary-goal-team", "--seat", "sdd-plan-coordinator",
         "--scope", "spec", "--spec-dir", str(SPEC_DIR), "--format", "json"],
        capture_output=True, text=True, cwd=REPO_ROOT)
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["scope"] == "spec"
    assert payload["team_slug"] == "085-sdd-temporary-goal-team"
    assert payload["seat_slug"] == "sdd-plan-coordinator"
