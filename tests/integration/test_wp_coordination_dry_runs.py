"""Integration dry runs for the Feature 070 coordination layer.

These tests drive the deterministic, test-only simulator in
``tests/fixtures/wp_driver_sim.py`` and — where dispatch must be blocked —
the real ``wp-gate.py --check preflight``. They assert interval relations, not
wall-clock durations, so a slower host does not change the outcome.

Quickstart Scenario C selects two cases by name: ``concurrent_read_only`` and
``write_serialization``.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from fixtures import wp_driver_sim, wp_fixtures

pytestmark = pytest.mark.integration

REPO_ROOT = Path(__file__).resolve().parents[2]
GATE = (
    REPO_ROOT
    / "skills"
    / "external"
    / "sdd-loop-driver"
    / "scripts"
    / "wp-gate.py"
)


def _intervals(result: dict) -> dict:
    return {
        dispatch["wp_id"]: (dispatch["started_at"], dispatch["ended_at"])
        for dispatch in result["dispatches"]
    }


def _overlaps(left, right) -> bool:
    (left_start, left_end), (right_start, right_end) = left, right
    return left_start < right_end and right_start < left_end


def _parallel_reads(count: int = 3, slot_cap: int = 2) -> dict:
    packages = []
    for index in range(1, count + 1):
        packages.append(
            wp_fixtures.make_package(
                "plan-wp%02d" % index,
                source_refs=["plan.md#read-%d" % index],
                inputs=["plan.md"],
                outputs=["findings/read-%d.md" % index],
                read_only_paths=["plan.md"],
                bounded_by={"unit": "tasks", "count": 1},
                max_turns=120,
            )
        )
    return wp_fixtures.make_plan(
        packages=packages, pattern="parallel", slot_cap=slot_cap
    )


def _overlapping_write_plan() -> dict:
    first = wp_fixtures.make_write_package(
        "plan-wp01",
        owned_paths=["src/generated/"],
        outputs=["src/generated/a.md"],
    )
    second = wp_fixtures.make_write_package(
        "plan-wp02",
        owned_paths=["src/generated/"],
        outputs=["src/generated/b.md"],
    )
    return wp_fixtures.make_plan(
        packages=[first, second], pattern="serial", slot_cap=1
    )


def _run_preflight(tmp_path: Path, plan: dict, owned=()):
    repo = tmp_path / "repo"
    repo.mkdir(parents=True, exist_ok=True)
    plan["plan_hash"] = wp_fixtures.canonical_hash_of(plan)
    spine = wp_fixtures.make_spine(repo / "state.md", plan=plan)
    manifest = wp_fixtures.make_manifest(repo / "manifest.json", owned=owned)
    return subprocess.run(
        [
            sys.executable,
            str(GATE),
            "--spine",
            str(spine),
            "--stage",
            plan["stage"],
            "--stage-attempt",
            "1",
            "--check",
            "preflight",
            "--manifest",
            str(manifest),
            "--repo",
            str(repo),
        ],
        capture_output=True,
        text=True,
    )


def _dry_run(tmp_path: Path, plan: dict, owned=()):
    """A driver dry run: dispatch only after the preflight admits the plan."""
    completed = _run_preflight(tmp_path, plan, owned=owned)
    record = json.loads(completed.stdout) if completed.stdout.strip() else {}
    if completed.returncode != 0:
        return {"admitted": False, "gate": record, "dispatch": None}
    return {
        "admitted": True,
        "gate": record,
        "dispatch": wp_driver_sim.schedule(plan),
    }


def test_concurrent_read_only_dispatch_overlaps_intervals():
    """Two independent read-only packages overlap inside the slot cap."""
    plan = _parallel_reads(count=3, slot_cap=2)
    result = wp_driver_sim.schedule(plan)
    intervals = _intervals(result)

    first, second = "plan-wp01", "plan-wp02"
    assert _overlaps(intervals[first], intervals[second])
    assert result["max_concurrent"] == 2
    assert result["stage_gate"] == "pass"
    third_start = intervals["plan-wp03"][0]
    assert third_start >= intervals[first][1]
    assert third_start >= intervals[second][1]


def test_write_serialization_holds_for_the_dependent_write():
    """The write starts after every read interval ends and overlaps nothing."""
    plan = wp_driver_sim.sim_plan()
    result = wp_driver_sim.schedule(plan)
    intervals = _intervals(result)

    write = intervals["plan-wp03"]
    for wp_id, interval in intervals.items():
        if wp_id == "plan-wp03":
            continue
        assert not _overlaps(interval, write), (wp_id, interval, write)
        assert write[0] >= interval[1], (wp_id, interval, write)

    write_dispatch = next(
        dispatch
        for dispatch in result["dispatches"]
        if dispatch["wp_id"] == "plan-wp03"
    )
    assert write_dispatch["effective_concurrency"] == 1


def test_ownership_path_rejection_blocks_dispatch(tmp_path):
    """WG-15 rejects unordered write overlap; the dry run dispatches nothing."""
    plan = _overlapping_write_plan()
    dry = _dry_run(tmp_path, plan, owned=["src/generated/"])

    assert dry["admitted"] is False
    assert dry["dispatch"] is None
    assert dry["gate"]["verdict"] == "reject"
    codes = [finding["code"] for finding in dry["gate"]["findings"]]
    assert "write-write-unordered" in codes
    assert "path-overlap" in codes


def test_dependency_unlocks_only_on_a_pass_verdict():
    """A dependent is dispatched on pass; fail and missing keep it blocked."""
    plan = wp_driver_sim.sim_plan()

    passed = wp_driver_sim.schedule(plan)
    assert "plan-wp03" in passed["dispatch_order"]
    intervals = _intervals(passed)
    verdict = next(
        item for item in passed["verdicts"] if item["wp_id"] == "plan-wp01"
    )
    assert verdict["at"] <= intervals["plan-wp03"][0]

    for verdict_value in ("fail", "missing"):
        blocked = wp_driver_sim.schedule(
            plan, verdicts={"plan-wp01": verdict_value}
        )
        assert "plan-wp03" in blocked["blocked"]
        assert "plan-wp03" not in blocked["dispatch_order"]
        assert blocked["stage_gate"] == "fail"


def test_failure_isolation_leaves_unrelated_work_complete():
    """A failed package does not cancel an unrelated read and keeps dependents blocked."""
    plan = wp_driver_sim.sim_plan()
    result = wp_driver_sim.schedule(
        plan, outcomes={"plan-wp01": "failed"}
    )

    assert "plan-wp01" in result["failed"]
    assert "plan-wp02" in result["dispatch_order"]
    assert "plan-wp02" in {
        item["wp_id"] for item in result["verdicts"]
    }
    assert "plan-wp03" in result["blocked"]
    assert result["stage_gate"] == "fail"
    assert "plan-wp01" in result["dispatch_order"]
    assert "plan-wp03" not in result["dispatch_order"]
