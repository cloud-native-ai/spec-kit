"""Contract tests for the scheduler and dispatch layer — SD-01…SD-16.

Layer under test
----------------
The clause text is owned by ``contracts/scheduler-and-dispatch.md``. The
runtime projection is ``references/decomposition-model.md`` (scheduler and
retry sections) plus the deterministic, test-only simulator
``tests/fixtures/wp_driver_sim.py``. This file pins both: every SD clause keeps
its normative content in the owner, and the simulator demonstrates the
mechanical rules (readiness, slot cap, write-alone, deterministic order,
failure isolation, collection, topology, anti-nesting, re-entry).

Verification/integration (VI-01…VI-14) extends this file in T020.
"""
from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

from fixtures import wp_driver_sim, wp_fixtures

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
DRIVER_ROOT = REPO_ROOT / "skills" / "external" / "sdd-loop-driver"
MODEL_DOC = DRIVER_ROOT / "references" / "decomposition-model.md"
GATE = DRIVER_ROOT / "scripts" / "wp-gate.py"
CONTRACTS = REPO_ROOT / ".specify" / "specs" / "070-subagent-task-teams" / "contracts"

SD_CONTRACT_PINS = {
    "SD-01": (
        "sole scheduler and coordinator",
        "never dispatch other packages",
        "never spawn a driver",
        "never edit the plan",
    ),
    "SD-02": (
        "ledger `verdict=pass`",
        "evidence pointer",
        "not silently dropped",
    ),
    "SD-03": (
        "dispatched alone",
        "effective concurrency is 1",
        "No two write packages",
    ),
    "SD-04": (
        "Up to `slot_cap` read-only packages",
        "The default is 2",
        "ceiling is `min(4, the line's remaining concurrency allowance)`",
    ),
    "SD-05": (
        "topological layer and then `wp_id` lexicographic",
        "actual `dispatch_order` counter separately",
        "never the dispatch timing order",
    ),
    "SD-06": (
        "stops launching new read-only packages",
        "never indefinitely deferred",
    ),
    "SD-07": (
        "one native host subagent per package",
        "MUST NOT launch `qodercli`",
        "host-no-parallel-native",
    ),
    "SD-08": (
        "detached `stage-runner.sh`",
        "`--stage <stage>-<wp_id>`",
        "`WP-<WP_ID_UPPER>-DONE`",
        "No shared runner or shared sentinel",
    ),
    "SD-09": (
        "terminal status (`exit`, `sentinel`)",
        "last non-empty log line",
        "`INCOMPLETE`",
        "`ANOMALY` line",
    ),
    "SD-10": (
        "independent verifier (VI-01)",
        "waits for the verdict",
    ),
    "SD-11": (
        "never cancels unrelated running packages",
        "dependents remain blocked",
        "surfaced, never silently repaired",
    ),
    "SD-12": (
        "unlocked only by a ledger `verdict=pass`",
        "fails twice triggers `wp_failed`",
        "unchanged U5 path",
    ),
    "SD-13": (
        "does not name or load `sdd-loop-driver`",
        "does not instruct the subagent to load any skill",
        "contains no loop logic",
        "not dispatched; the block is recorded",
    ),
    "SD-14": (
        "Each concurrently dispatched package declares its ports",
        "never start a global service",
        "WG-16",
    ),
    "SD-15": (
        "existing `run-agent` / `stage-runner.sh` paths only",
        "adds no dispatcher, queue, broker, daemon, external service, or model API",
    ),
    "SD-16": (
        "fresh plan fence, a fresh plan hash, and a fresh per-package attempt counter",
        "earlier records remain in the spine",
        "re-runs `watch-target.sh --once`",
        "never redispatches a completed package",
    ),
}


def _contract(name: str) -> str:
    return (CONTRACTS / name).read_text(encoding="utf-8")


def _model_text() -> str:
    assert MODEL_DOC.is_file(), "missing runtime owner: %s" % MODEL_DOC
    return MODEL_DOC.read_text(encoding="utf-8")


def _run_gate(*args):
    return subprocess.run(
        [sys.executable, str(GATE), *args], capture_output=True, text=True
    )


def _rehash(plan: dict) -> dict:
    plan["plan_hash"] = wp_fixtures.canonical_hash_of(plan)
    return plan


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


def _queued_write_plan() -> dict:
    """Two reads run first; a write depends on one read while another read waits."""
    read_a = wp_fixtures.make_package(
        "plan-wp01", outputs=["findings/read-a.md"], max_turns=120
    )
    read_b = wp_fixtures.make_package(
        "plan-wp02", outputs=["findings/read-b.md"], max_turns=120
    )
    write_c = wp_fixtures.make_write_package(
        "plan-wp03",
        depends_on=["plan-wp01"],
        owned_paths=["src/generated/"],
        outputs=["src/generated/c.md"],
        max_turns=120,
    )
    read_d = wp_fixtures.make_package(
        "plan-wp04", outputs=["findings/read-d.md"], max_turns=120
    )
    return wp_fixtures.make_plan(
        packages=[read_a, read_b, write_c, read_d],
        pattern="serial",
        slot_cap=2,
    )


def _write_pair(overlap: bool = True) -> dict:
    if overlap:
        owned = ["src/generated/"]
    else:
        owned = ["src/first/"]
    first = wp_fixtures.make_write_package(
        "plan-wp01",
        owned_paths=owned,
        outputs=["src/generated/a.md"]
        if overlap
        else ["src/first/a.md"],
    )
    second = wp_fixtures.make_write_package(
        "plan-wp02",
        owned_paths=["src/generated/"]
        if overlap
        else ["src/second/"],
        outputs=["src/generated/b.md"]
        if overlap
        else ["src/second/b.md"],
    )
    return wp_fixtures.make_plan(
        packages=[first, second], pattern="serial", slot_cap=1
    )


def _write_read_plan(ordered: bool = False) -> dict:
    writer = wp_fixtures.make_write_package(
        "plan-wp01",
        owned_paths=["src/generated/"],
        outputs=["src/generated/out.md"],
    )
    reader = wp_fixtures.make_package(
        "plan-wp02",
        inputs=["src/generated/out.md"],
        outputs=["findings/read.md"],
        read_only_paths=["src/generated/out.md"],
        depends_on=["plan-wp01"] if ordered else [],
        resources={
            "ports": "none",
            "tmp_dir": "tmp/plan-wp02",
            "cache_dir": "none",
            "shared_readonly": [],
        },
    )
    return wp_fixtures.make_plan(
        packages=[writer, reader], pattern="serial", slot_cap=2
    )


def _isolate(plan: dict) -> dict:
    for package in plan["packages"]:
        package["resources"] = {
            "ports": "none",
            "tmp_dir": "tmp/%s" % package["wp_id"],
            "cache_dir": "none",
            "shared_readonly": [],
        }
    return plan


def _preflight(tmp_path: Path, plan: dict, owned=(), read_only=(), forbidden=()):
    repo = tmp_path / "repo"
    repo.mkdir(parents=True, exist_ok=True)
    _rehash(plan)
    spine = wp_fixtures.make_spine(repo / "state.md", plan=plan)
    manifest = wp_fixtures.make_manifest(
        repo / "manifest.json",
        owned=owned,
        read_only=read_only,
        forbidden=forbidden,
    )
    return _run_gate(
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
    )


@pytest.mark.parametrize(
    "clause", sorted(SD_CONTRACT_PINS), ids=sorted(SD_CONTRACT_PINS)
)
def test_sd_contract_clause_keeps_its_normative_content(clause):
    """Each SD clause keeps its rule in the owner contract."""
    contract = _contract("scheduler-and-dispatch.md")
    for snippet in SD_CONTRACT_PINS[clause]:
        assert snippet in contract, (clause, snippet)


def test_sd_contract_file_covers_the_closed_clause_set():
    text = _contract("scheduler-and-dispatch.md")
    for index in range(1, 17):
        assert "SD-%02d" % index in text


def test_model_doc_carries_the_runtime_projection():
    text = _model_text()
    for index in range(1, 17):
        assert "SD-%02d" % index in text, index
    for token in (
        "write-alone",
        "host-no-parallel-native",
        "run-agent",
        "stage-runner.sh",
        "watch-target.sh --once",
        "retry_delta",
        "retry-unchanged",
        "retry-exhausted",
        "retry-delta-invalid",
        "never redispatches a completed package",
    ):
        assert token in text, token


def test_sd_01_the_driver_is_the_sole_coordinator():
    """SD-01: one coordinator selects, dispatches, collects, and records."""
    plan = wp_driver_sim.sim_plan()
    result = wp_driver_sim.schedule(plan)

    assert result["coordinator"] == "driver"
    assert [dispatch["wp_id"] for dispatch in result["dispatches"]] == [
        "plan-wp01",
        "plan-wp02",
        "plan-wp03",
    ]
    assert all(
        dispatch["executor_execution"].startswith("executor-")
        for dispatch in result["dispatches"]
    )
    for dispatch in result["dispatches"]:
        assert "dispatched_by" not in dispatch
        assert "nested_dispatch" not in dispatch


def test_sd_02_readiness_requires_a_verified_dependency():
    """SD-02: a dependent is ready only on ledger verdict=pass; it is not dropped."""
    plan = wp_driver_sim.sim_plan()
    result = wp_driver_sim.schedule(plan, verdicts={"plan-wp01": "fail"})

    assert "plan-wp03" in result["blocked"]
    assert "plan-wp03" not in result["dispatch_order"]
    assert "plan-wp02" in result["dispatch_order"]
    assert result["stage_gate"] == "fail"


def test_sd_03_write_packages_are_dispatched_alone():
    """SD-03: a write interval overlaps no other interval and runs at concurrency 1."""
    plan = wp_driver_sim.sim_plan()
    result = wp_driver_sim.schedule(plan)
    intervals = _intervals(result)

    write_dispatches = [
        dispatch
        for dispatch in result["dispatches"]
        if dispatch["kind"] == "write"
    ]
    assert len(write_dispatches) == 1
    write = write_dispatches[0]
    assert write["wp_id"] == "plan-wp03"
    assert write["effective_concurrency"] == 1
    for wp_id, interval in intervals.items():
        if wp_id == write["wp_id"]:
            continue
        assert not _overlaps(interval, intervals[write["wp_id"]])


def test_sd_04_read_only_concurrency_respects_the_slot_cap():
    """SD-04: up to slot_cap read-only packages run concurrently."""
    plan = _parallel_reads(count=3, slot_cap=2)
    result = wp_driver_sim.schedule(plan)
    intervals = _intervals(result)

    assert result["max_concurrent"] == 2
    overlapping_pairs = [
        (left, right)
        for offset, left in enumerate(sorted(intervals))
        for right in sorted(intervals)[offset + 1:]
        if _overlaps(intervals[left], intervals[right])
    ]
    assert overlapping_pairs, intervals
    assert len(overlapping_pairs) >= 1


def test_sd_05_dispatch_order_is_layer_then_lexicographic(tmp_path):
    """SD-05: dispatch order is deterministic; integration order is declared, not timed."""
    plan = wp_driver_sim.sim_plan()
    first = wp_driver_sim.schedule(plan)
    second = wp_driver_sim.schedule(copy.deepcopy(plan))

    assert first["dispatch_order"] == second["dispatch_order"]
    assert first["dispatch_order"] == ["plan-wp01", "plan-wp02", "plan-wp03"]
    assert [item["dispatch_order"] for item in first["dispatches"]] == [1, 2, 3]
    assert first["dispatch_layers"] == [["plan-wp01", "plan-wp02"], ["plan-wp03"]]

    spine = wp_fixtures.make_spine(
        tmp_path / "state.md", plan=_rehash(copy.deepcopy(plan))
    )
    completed = _run_gate(
        "--spine", str(spine), "--stage", "plan", "--stage-attempt", "1",
        "--check", "plan",
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    gate = json.loads(completed.stdout)
    assert first["dispatch_layers"] == gate["dispatch_layers"]
    assert gate["integration_order"] == [
        "plan-wp01",
        "plan-wp02",
        "plan-wp03",
    ]


def test_sd_06_a_ready_write_is_not_starved_by_new_reads():
    """SD-06: once a write is ready, no new read starts before the write."""
    plan = _queued_write_plan()
    result = wp_driver_sim.schedule(plan)
    intervals = _intervals(result)

    assert result["dispatch_order"] == [
        "plan-wp01",
        "plan-wp02",
        "plan-wp03",
        "plan-wp04",
    ]
    write_start, write_end = intervals["plan-wp03"]
    read_b_end = intervals["plan-wp02"][1]
    read_d_start = intervals["plan-wp04"][0]
    assert write_start >= read_b_end
    assert read_d_start >= write_end


def test_sd_07_local_native_topology_and_serial_fallback():
    """SD-07: native dispatch by default; a host without parallel calls records the fallback."""
    plan = wp_driver_sim.sim_plan()
    native = wp_driver_sim.schedule(plan)
    assert native["topology"]["effective"] == "parallel-native"
    assert all(
        dispatch["topology"] == "parallel-native"
        for dispatch in native["dispatches"]
    )

    serial = wp_driver_sim.schedule(plan, host_parallel=False)
    assert serial["topology"] == {
        "requested": "native",
        "parallel_requested": "yes",
        "effective": "serial",
        "reason": "host-no-parallel-native",
    }
    assert all(
        dispatch["topology"] == "serial-native"
        for dispatch in serial["dispatches"]
    )
    intervals = _intervals(serial)
    ordered = sorted(intervals)
    for left, right in zip(ordered, ordered[1:]):
        assert not _overlaps(intervals[left], intervals[right])
    assert "qodercli" not in _model_text().lower()


def test_sd_08_detached_topology_uses_unique_runners_and_sentinels():
    """SD-08: one detached runner per package, its own label, sentinel, and evidence set."""
    plan = wp_driver_sim.sim_plan()
    result = wp_driver_sim.schedule(plan, topology="detached")
    packages = {package["wp_id"]: package for package in plan["packages"]}

    labels = [dispatch["runner_label"] for dispatch in result["dispatches"]]
    sentinels = [dispatch["sentinel"] for dispatch in result["dispatches"]]
    assert len(set(labels)) == len(labels) == 3
    assert len(set(sentinels)) == len(sentinels) == 3
    for dispatch in result["dispatches"]:
        assert dispatch["runner_label"] == "plan-%s" % dispatch["wp_id"]
        assert dispatch["sentinel"] == packages[dispatch["wp_id"]]["sentinel"]
        for key in ("pid_path", "status_path", "log_path", "heartbeat_path"):
            assert dispatch[key].endswith(
                "/%s.%s" % (dispatch["runner_label"], key.split("_")[0])
            )
    assert all(
        dispatch["topology"] == "detached-runner"
        for dispatch in result["dispatches"]
    )


def test_sd_09_incomplete_results_are_not_verified():
    """SD-09: a missing sentinel, anomaly line, or terminal failure yields no verdict."""
    plan = wp_driver_sim.sim_plan()
    for outcome in ("missing-sentinel", "anomaly", "failed", "stalled"):
        result = wp_driver_sim.schedule(
            plan, outcomes={"plan-wp01": outcome}
        )
        assert result["verdicts"] == [
            verdict
            for verdict in result["verdicts"]
            if verdict["wp_id"] != "plan-wp01"
        ], outcome
        assert "plan-wp01" in result["failed"], outcome
        assert "plan-wp03" in result["blocked"], outcome
        assert "plan-wp02" in {
            verdict["wp_id"] for verdict in result["verdicts"]
        }, outcome
        if outcome in ("missing-sentinel", "anomaly"):
            assert any(
                anomaly["wp_id"] == "plan-wp01"
                for anomaly in result["anomalies"]
            ), outcome
            assert all(
                settle["wp_id"] != "plan-wp01" for settle in result["settles"]
            ), outcome

    clean = wp_driver_sim.schedule(plan)
    for settle in clean["settles"]:
        assert settle["log_last_line"] == settle["sentinel"]


def test_sd_10_each_settled_package_gets_one_independent_verifier():
    """SD-10: one verifier execution per complete package, distinct from the executor."""
    plan = wp_driver_sim.sim_plan()
    result = wp_driver_sim.schedule(plan)

    assert len(result["verifier_dispatches"]) == 3
    executions = [
        dispatch["verifier_execution"]
        for dispatch in result["verifier_dispatches"]
    ]
    assert len(set(executions)) == 3
    for dispatch in result["dispatches"]:
        assert dispatch["executor_execution"] not in executions
    assert {verdict["wp_id"] for verdict in result["verdicts"]} == {
        "plan-wp01",
        "plan-wp02",
        "plan-wp03",
    }
    verdicts_by_wp = {
        verdict["wp_id"]: verdict for verdict in result["verdicts"]
    }
    intervals = _intervals(result)
    assert verdicts_by_wp["plan-wp01"]["at"] <= intervals["plan-wp03"][0]


def test_sd_11_a_failure_does_not_cancel_unrelated_packages():
    """SD-11: a failed package leaves dependents blocked and unrelated work running."""
    plan = wp_driver_sim.sim_plan()
    result = wp_driver_sim.schedule(
        plan, outcomes={"plan-wp01": "failed"}
    )

    assert "plan-wp01" in result["failed"]
    assert "plan-wp02" in result["dispatch_order"]
    assert "plan-wp02" in {
        verdict["wp_id"] for verdict in result["verdicts"]
    }
    assert "plan-wp03" in result["blocked"]
    assert result["stage_gate"] == "fail"


def test_sd_12_unlock_requires_a_pass_verdict():
    """SD-12: pass unlocks; fail and missing verdicts keep dependents blocked."""
    plan = wp_driver_sim.sim_plan()

    passed = wp_driver_sim.schedule(plan)
    assert "plan-wp03" in passed["dispatch_order"]

    for verdict in ("fail", "missing"):
        blocked = wp_driver_sim.schedule(
            plan, verdicts={"plan-wp01": verdict}
        )
        assert "plan-wp03" in blocked["blocked"], verdict
        assert blocked["stage_gate"] == "fail", verdict

    text = _model_text()
    assert "wp_failed" in text
    assert "U5" in text


def test_sd_13_nested_driver_prompts_are_blocked_and_recorded():
    """SD-13: a prompt naming the driver, loading a skill, or carrying loop logic is blocked."""
    clean = wp_driver_sim.check_dispatch_prompt(
        "Implement the bounded package and write the declared output."
    )
    assert clean["ok"] is True
    assert clean["findings"] == []

    cases = {
        "prompt-names-driver": "You are the sdd-loop-driver for this stage.",
        "prompt-loads-skill": "Load the run-agent skill before starting.",
        "prompt-loop-logic": "While packages remain, dispatch the next package.",
    }
    for code, prompt in cases.items():
        result = wp_driver_sim.check_dispatch_prompt(prompt)
        assert result["ok"] is False, prompt
        assert [finding["code"] for finding in result["findings"]] == [code]

    plan = wp_driver_sim.sim_plan()
    scheduled = wp_driver_sim.schedule(
        plan,
        prompts={
            "plan-wp01": "You are the sdd-loop-driver. Load the run-agent skill."
        },
    )
    assert [
        block["wp_id"] for block in scheduled["prompt_blocks"]
    ] == ["plan-wp01"]
    assert "plan-wp01" not in scheduled["dispatch_order"]
    assert "plan-wp02" in scheduled["dispatch_order"]
    assert "plan-wp03" in scheduled["blocked"]
    assert scheduled["stage_gate"] == "fail"


def test_sd_14_resource_isolation_is_enforced_before_dispatch(tmp_path):
    """SD-14: concurrent packages declare isolated resources; WG-16 rejects the rest."""
    plan = _isolate(_parallel_reads(count=2, slot_cap=2))
    admitted = _preflight(tmp_path / "admitted", plan)
    assert admitted.returncode == 0, admitted.stdout + admitted.stderr
    assert json.loads(admitted.stdout)["verdict"] == "admit"

    bare = _parallel_reads(count=2, slot_cap=2)
    for package in bare["packages"]:
        package["resources"] = {
            "ports": "none",
            "tmp_dir": "none",
            "cache_dir": "none",
            "shared_readonly": [],
        }
    rejected = _preflight(tmp_path / "rejected", bare)
    assert rejected.returncode == 1, rejected.stdout + rejected.stderr
    codes = [
        finding["code"] for finding in json.loads(rejected.stdout)["findings"]
    ]
    assert "isolation-missing" in codes
    assert "WG-16" in _model_text()


def test_sd_15_no_new_dispatch_mechanism_is_introduced():
    """SD-15: the dispatch forms are the existing run-agent and stage-runner paths."""
    text = _model_text()
    for token in ("run-agent", "stage-runner.sh", "no dispatcher"):
        assert token in text, token

    scripts = DRIVER_ROOT / "scripts"
    for forbidden in ("scheduler.py", "queue.py", "broker.py", "daemon.py"):
        assert not (scripts / forbidden).exists(), forbidden

    contract = _contract("scheduler-and-dispatch.md")
    assert "adds no dispatcher" in contract


def test_sd_16_reentry_never_redispatches_a_completed_package():
    """SD-16: the spine is authoritative on re-entry; a new stage attempt resets counters."""
    plan = wp_driver_sim.sim_plan()
    resumed = wp_driver_sim.schedule(plan, completed={"plan-wp01"})
    assert resumed["completed_from_spine"] == ["plan-wp01"]
    assert "plan-wp01" not in resumed["dispatch_order"]
    # The ready write takes priority over the newly available read (SD-06).
    assert resumed["dispatch_order"] == ["plan-wp03", "plan-wp02"]
    assert resumed["stage_gate"] == "pass"

    fresh = copy.deepcopy(plan)
    fresh["stage_attempt"] = 2
    _rehash(fresh)
    attempt_two = wp_driver_sim.schedule(fresh)
    assert all(
        "-a2-w1" in dispatch["attempt_id"]
        for dispatch in attempt_two["dispatches"]
    )

    text = _model_text()
    assert "watch-target.sh --once" in text
    assert "never redispatches a completed package" in text
