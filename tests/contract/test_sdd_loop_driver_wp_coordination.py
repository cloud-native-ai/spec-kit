"""Contract tests for the scheduler, dispatch, and verification layers.

Layer under test
----------------
The clause text is owned by ``contracts/scheduler-and-dispatch.md`` (SD-01…SD-16)
and ``contracts/verification-and-integration.md`` (VI-01…VI-14). The runtime
projection is ``references/decomposition-model.md`` (scheduler, retry, and
verification/integration sections) plus the deterministic, test-only simulator
``tests/fixtures/wp_driver_sim.py``. This file pins both: every clause keeps its
normative content in the owner, and the simulator demonstrates the mechanical
rules (readiness, slot cap, write-alone, deterministic order, failure
isolation, collection, topology, anti-nesting, re-entry, independent verdicts,
aggregation, and deterministic integration).
"""
from __future__ import annotations

import copy
import json
import re
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


# ---------------------------------------------------------------------------
# VI-01…VI-14 — independent verification and integration (T020)
# ---------------------------------------------------------------------------

VI_CONTRACT_PINS = {
    "VI-01": (
        "exactly one fresh-context verifier execution",
        "not the package's executor",
        "driver-u4",
        "structurally independent of the executor",
    ),
    "VI-02": (
        "read-only with respect to repository content",
        "`targeted-set-v1`",
        "MUST NOT run a full suite",
    ),
    "VI-03": (
        "`checks[]` (id, kind, command, result, evidence_ref)",
        "`evidence_refs[]`",
        "cover every acceptance criterion",
        "`verified_at`",
    ),
    "VI-04": (
        "missing, unreadable, malformed, or ambiguous verdict counts as `fail`",
        "never inferred from a package self-report",
    ),
    "VI-05": (
        "appends a `verdict` ledger event",
        "verifier_execution, evidence_ptr, at",
        "A package without that event is not verified.",
    ),
    "VI-06": (
        "aggregates the verified verdict set",
        "`required_outputs` minus `integrator_outputs`",
        "both evidence pointers",
    ),
    "VI-07": (
        "topological layers, each layer sorted by `wp_id` lexicographic",
        "recorded in the `integrate` event",
        "not the dispatch order",
    ),
    "VI-08": (
        "stops integration, fails the stage gate",
        "no partial commit presented as a complete stage deliverable",
    ),
    "VI-09": (
        "package executors do not commit",
        "single stage-closing commit",
    ),
    "VI-10": (
        "067 part-commit discipline is preserved",
        "MUST NOT rewrite, squash, or bypass the part commits",
    ),
    "VI-11": (
        "one integrator execution per stage attempt",
        "`stage-integrator` seat",
        "emits `<STAGE>-DONE` as its last non-empty line",
        "never dispatches a package, never re-plans, and never loads the driver",
    ),
    "VI-12": (
        "never satisfies the stage sentinel",
        "Only the integrator's `<STAGE>-DONE`",
    ),
    "VI-13": (
        "unchanged stage-level U4",
        "Package verdicts are inputs and never substitutes",
    ),
    "VI-14": (
        "does not push, force-merge, or auto-merge",
        "remain driver-owned",
    ),
}


def _scheduled(plan, **kwargs):
    dispatch = wp_driver_sim.schedule(plan, **kwargs)
    return dispatch, wp_driver_sim.results_from_schedule(dispatch)


def _clarify_plan() -> dict:
    """Two read-only investigation packages plus an integrator write-back."""
    first = wp_fixtures.make_package(
        "clarify-wp01",
        stage="clarify",
        outputs=["findings/clarify-a.md"],
    )
    second = wp_fixtures.make_package(
        "clarify-wp02",
        stage="clarify",
        outputs=["findings/clarify-b.md"],
    )
    return wp_fixtures.make_plan(
        packages=[first, second],
        stage="clarify",
        decision="decomposed",
        gate_verdict="admit",
        rule="decompose-investigation-v1",
        required_outputs=[
            "findings/clarify-a.md",
            "findings/clarify-b.md",
            "clarifications.md",
        ],
        integrator_outputs=["clarifications.md"],
    )


def _shared_output_plan() -> dict:
    """Two verified packages that claim the same output path."""
    first = wp_fixtures.make_package(
        "plan-wp01", outputs=["findings/shared.md"]
    )
    second = wp_fixtures.make_package(
        "plan-wp02", outputs=["findings/shared.md"]
    )
    return wp_fixtures.make_plan(
        packages=[first, second],
        required_outputs=["findings/shared.md"],
    )


@pytest.mark.parametrize(
    "clause", sorted(VI_CONTRACT_PINS), ids=sorted(VI_CONTRACT_PINS)
)
def test_vi_contract_clause_keeps_its_normative_content(clause):
    """Each VI clause keeps its rule in the owner contract."""
    contract = _contract("verification-and-integration.md")
    for snippet in VI_CONTRACT_PINS[clause]:
        assert snippet in contract, (clause, snippet)


def test_vi_contract_file_covers_the_closed_clause_set():
    text = _contract("verification-and-integration.md")
    for index in range(1, 15):
        assert "VI-%02d" % index in text


def test_vi_model_doc_carries_the_runtime_projection():
    text = _model_text()
    for index in range(1, 15):
        assert "VI-%02d" % index in text, index
    for token in (
        "stage-verifier",
        "stage-integrator",
        "verdict.json",
        "driver-u4",
        "integrator_outputs",
        "closing commit",
        "stage U4",
        "never promoted",
    ):
        assert token in text, token


def test_vi_01_one_independent_verifier_per_settled_package():
    """VI-01: one fresh-context verifier, never the executor."""
    plan = wp_driver_sim.sim_plan()
    dispatch, results = _scheduled(plan)
    verification = wp_driver_sim.verify(plan, results)

    executors = {
        item["wp_id"]: item["executor_execution"]
        for item in dispatch["dispatches"]
    }
    verifiers = verification["verifier_executions"]
    assert sorted(item["wp_id"] for item in verifiers) == [
        "plan-wp01",
        "plan-wp02",
        "plan-wp03",
    ]
    assert len({item["execution_id"] for item in verifiers}) == 3
    for item in verifiers:
        assert item["fresh_context"] is True
        assert item["independent"] is True
        assert item["execution_id"] != executors[item["wp_id"]]
    assert verification["stage_gate"] == "pass"


def test_vi_02_verifier_is_read_only_and_targeted():
    """VI-02: the verifier reads, may run targeted tests, never a full suite."""
    plan = wp_driver_sim.sim_plan()
    _, results = _scheduled(plan)
    verification = wp_driver_sim.verify(plan, results)

    assert verification["repository_writes"] == []
    assert verification["full_suite_runs"] == 0
    assert verification["targeted_tests_only"] is True
    for item in verification["verifier_executions"]:
        assert item["read_only"] is True
    text = _model_text()
    for token in (
        "read-only with respect to repository content",
        "targeted tests",
        "never a full suite",
    ):
        assert token in text, token


def test_vi_03_verdict_record_pins_the_schema(tmp_path):
    """VI-03: the verdict file carries every required field and every criterion."""
    plan = wp_driver_sim.sim_plan()
    _, results = _scheduled(plan)
    verification = wp_driver_sim.verify(plan, results, state_dir=tmp_path)

    record = next(
        item
        for item in verification["verdicts"]
        if item["wp_id"] == "plan-wp01"
    )
    for field in (
        "schema_version",
        "wp_id",
        "stage",
        "stage_attempt",
        "wp_attempt",
        "verdict",
        "checks",
        "evidence_refs",
        "execution_id",
        "verified_at",
    ):
        assert field in record, field
    assert record["schema_version"] == 1
    assert record["verdict"] == "pass"
    assert record["path"] == (
        "wp/line-demo-plan-plan-wp01-a1w1.verdict.json"
    )
    package = next(
        item for item in plan["packages"] if item["wp_id"] == "plan-wp01"
    )
    assert {check["id"] for check in record["checks"]} == {
        item["id"] for item in package["acceptance"]
    }
    for check in record["checks"]:
        assert check["kind"] in (
            "artifact",
            "contract",
            "test",
            "adversarial",
            "ownership",
        )
        assert check["result"] in ("pass", "fail")
        assert "evidence_ref" in check
    assert re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", record["verified_at"]
    )
    on_disk = json.loads(
        (tmp_path / record["path"]).read_text(encoding="utf-8")
    )
    assert on_disk["wp_id"] == "plan-wp01"
    assert on_disk["verdict"] == "pass"
    assert "path" not in on_disk


@pytest.mark.parametrize(
    "value,code",
    [
        ("missing", "verdict-missing"),
        ("unreadable", "verdict-unreadable"),
        ("malformed", "verdict-malformed"),
        ("ambiguous", "verdict-ambiguous"),
    ],
)
def test_vi_04_an_unusable_verdict_counts_as_fail(value, code):
    """VI-04: missing, unreadable, malformed, and ambiguous all fail."""
    plan = wp_driver_sim.sim_plan()
    _, results = _scheduled(plan)
    verification = wp_driver_sim.verify(
        plan, results, verdicts={"plan-wp01": value}
    )

    assert "plan-wp01" in verification["unverified"]
    assert "plan-wp01" not in verification["verified"]
    event = next(
        item
        for item in verification["verdict_events"]
        if item["wp_id"] == "plan-wp01"
    )
    assert event["verdict"] == "fail"
    codes = {
        finding["code"]
        for finding in verification["findings"]
        if finding["wp_id"] == "plan-wp01"
    }
    assert code in codes, codes
    assert verification["stage_gate"] == "fail"


def test_vi_05_a_verdict_event_follows_each_settle():
    """VI-05: the ledger event is the only proof that a package was verified."""
    plan = wp_driver_sim.sim_plan()
    dispatch, results = _scheduled(plan)
    verification = wp_driver_sim.verify(plan, results)

    settles = {
        item["wp_id"]: item["ended_at"] for item in dispatch["settles"]
    }
    events = verification["verdict_events"]
    assert {item["wp_id"] for item in events} == set(settles)
    for event in events:
        assert event["event"] == "verdict"
        for field in (
            "wp_id",
            "verdict",
            "verifier_execution",
            "evidence_ptr",
            "at",
        ):
            assert field in event, field
        assert event["at"] >= settles[event["wp_id"]]
        assert event["verdict"] == "pass"
    assert verification["verified"] == sorted(settles)


def test_vi_06_aggregation_assigns_integrator_outputs_outside_coverage():
    """VI-06: package coverage excludes integrator_outputs; the seat owns them."""
    plan = _clarify_plan()
    run = wp_driver_sim.run_stage(plan)
    integration = run["integration"]
    aggregate = integration["aggregate"]

    assert aggregate["required_package_outputs"] == [
        "findings/clarify-a.md",
        "findings/clarify-b.md",
    ]
    assert aggregate["integrator_outputs_expected"] == [
        "clarifications.md"
    ]
    produced = {
        output
        for outputs in aggregate["package_outputs"].values()
        for output in outputs
    }
    assert produced == {
        "findings/clarify-a.md",
        "findings/clarify-b.md",
    }
    assert integration["integrator"]["integrator_outputs"] == [
        "clarifications.md"
    ]
    assert aggregate["coverage_ok"] is True
    assert aggregate["missing_outputs"] == []
    assert integration["conflict"] is False
    assert integration["stage_gate"] == "pass"


def test_vi_07_integration_order_is_declared_not_dispatched():
    """VI-07: re-entry dispatches out of order; integration keeps graph order."""
    plan = wp_driver_sim.sim_plan()
    reentry = wp_driver_sim.schedule(plan, completed={"plan-wp01"})
    assert reentry["dispatch_order"] == ["plan-wp03", "plan-wp02"]

    verification = {
        "verified": ["plan-wp01", "plan-wp02", "plan-wp03"],
        "failed": [],
        "unverified": [],
        "verdicts": [],
        "verdict_events": [],
        "stage_gate": "pass",
    }
    first = wp_driver_sim.integrate(plan, verification)
    second = wp_driver_sim.integrate(
        copy.deepcopy(plan), copy.deepcopy(verification)
    )

    assert first["integration_order"] == [
        "plan-wp01",
        "plan-wp02",
        "plan-wp03",
    ]
    assert first["integration_order"] == second["integration_order"]
    assert first["integration_order"] != reentry["dispatch_order"]
    assert first["integrate_event"]["order"] == first["integration_order"]


def test_vi_08_conflict_stops_integration_without_a_partial_commit():
    """VI-08: contradictory outputs stop integration and leave no commit."""
    plan = _shared_output_plan()
    run = wp_driver_sim.run_stage(
        plan,
        contents={
            "findings/shared.md": {
                "plan-wp01": "alpha",
                "plan-wp02": "beta",
            }
        },
    )
    integration = run["integration"]

    assert integration["conflict"] is True
    assert integration["commit"] is None
    assert integration["commits"]["closing"] is None
    assert integration["integrator"]["committed"] is False
    assert integration["integrator"]["last_non_empty_line"] != "PLAN-DONE"
    assert integration["stage_gate"] == "fail"
    finding = next(
        item
        for item in integration["findings"]
        if item["code"] == "output-contradiction"
    )
    assert len(finding["evidence_refs"]) == 2


def test_vi_09_plan_stage_has_one_closing_commit_and_no_package_commit():
    """VI-09: non-implement executors never commit; the integrator commits once."""
    plan = wp_driver_sim.sim_plan()
    run = wp_driver_sim.run_stage(plan)
    commits = run["integration"]["commits"]

    assert commits["package_commits"] == []
    assert commits["part_commits"] == []
    assert commits["closing"]
    assert commits["closing"] not in commits["part_commits"]
    assert run["integration"]["integrator"]["committed"] is True

    results = run["results"]
    results["plan-wp02"]["commits"] = ["package-commit"]
    verification = wp_driver_sim.verify(plan, results)
    forbidden = wp_driver_sim.integrate(plan, verification, results=results)
    assert forbidden["conflict"] is True
    assert "package-commit-forbidden" in {
        item["code"] for item in forbidden["findings"]
    }


def test_vi_10_implement_part_commits_are_preserved():
    """VI-10: 067 part commits survive; one closing commit follows."""
    first = wp_fixtures.make_write_package(
        "implement-wp01",
        stage="implement",
        owned_paths=["src/first/"],
        outputs=["src/first/a.md"],
    )
    second = wp_fixtures.make_write_package(
        "implement-wp02",
        stage="implement",
        owned_paths=["src/second/"],
        outputs=["src/second/b.md"],
    )
    plan = wp_fixtures.make_plan(
        packages=[first, second], stage="implement", pattern="serial"
    )
    _, results = _scheduled(plan)
    results["implement-wp01"]["commits"] = ["part-1", "part-2"]
    results["implement-wp02"]["commits"] = ["part-3"]
    verification = wp_driver_sim.verify(plan, results)
    integration = wp_driver_sim.integrate(
        plan, verification, results=results
    )

    commits = integration["commits"]
    assert commits["part_commits"] == ["part-1", "part-2", "part-3"]
    assert commits["closing"]
    assert commits["closing"] not in commits["part_commits"]
    assert commits["rewritten"] == []
    assert commits["squashed"] is False


def test_vi_11_one_integrator_seat_owns_its_outputs_and_sentinel():
    """VI-11: one integrator execution per attempt, owning its sentinel."""
    plan = _clarify_plan()
    run = wp_driver_sim.run_stage(plan)
    integrator = run["integration"]["integrator"]

    assert integrator["seat"] == "stage-integrator"
    assert integrator["execution_id"] == "integrator-clarify-a1"
    assert integrator["integrator_outputs"] == ["clarifications.md"]
    assert integrator["last_non_empty_line"] == "CLARIFY-DONE"
    assert integrator["dispatched_packages"] == []
    assert integrator["replanned"] is False
    assert integrator["loaded_driver"] is False
    assert run["integration"]["integrate_event"]["order"] == [
        "clarify-wp01",
        "clarify-wp02",
    ]


def test_vi_12_package_sentinels_are_never_promoted():
    """VI-12: only the integrator's stage sentinel satisfies the stage."""
    plan = wp_driver_sim.sim_plan()
    normal = wp_driver_sim.run_stage(plan)["integration"]
    assert normal["stage_u4"]["sentinel_ok"] is True

    package_sentinel = wp_fixtures.sentinel_for("plan-wp01")
    assert package_sentinel == "WP-PLAN-WP01-DONE"
    promoted = wp_driver_sim.run_stage(
        plan, integrator_last_line=package_sentinel
    )["integration"]

    assert promoted["stage_u4"]["sentinel"] == package_sentinel
    assert promoted["stage_u4"]["sentinel_ok"] is False
    assert promoted["stage_gate"] == "fail"


def test_vi_13_stage_u4_runs_after_integration_and_is_not_substituted():
    """VI-13: unchanged U4 follows integration; pass verdicts do not replace it."""
    plan = wp_driver_sim.sim_plan()
    run = wp_driver_sim.run_stage(plan)
    integration = run["integration"]

    assert all(
        item["verdict"] == "pass" for item in run["verification"]["verdicts"]
    )
    assert integration["stage_u4"]["at"] > integration["at"]
    assert integration["stage_u4"]["package_verdicts_substitute"] is False
    assert integration["stage_u4"]["gate"] == "pass"

    for key in ("artifact_verification", "discipline_checks"):
        failed = wp_driver_sim.run_stage(plan, u4={key: "fail"})[
            "integration"
        ]
        assert failed["stage_u4"]["sentinel_ok"] is True
        assert failed["stage_u4"]["gate"] == "fail"
        assert failed["stage_gate"] == "fail"


def test_vi_14_closure_and_merge_stay_driver_owned():
    """VI-14: no push or merge is introduced; confirmation gates are preserved."""
    integration = wp_driver_sim.run_stage(wp_driver_sim.sim_plan())[
        "integration"
    ]
    assert integration["closure"] == {
        "owner": "driver",
        "push": False,
        "force_merge": False,
        "auto_merge": False,
        "confirmation_gates": "preserved",
    }
    text = _model_text()
    for token in ("does not push", "force-merge", "driver-owned"):
        assert token in text, token


# ---------------------------------------------------------------------------
# FN-01…FN-16: opt-out, fallback, and non-regression (Feature 070)
# Clause text owner: contracts/fallback-and-nonregression.md.
# Runtime projection: decomposition-model.md §20–§21; behaviour: the
# deterministic decision procedure in tests/fixtures/wp_driver_sim.py.
# ---------------------------------------------------------------------------

FN_CONTRACT = CONTRACTS / "fallback-and-nonregression.md"
RED_FIRST_NOTES = (
    REPO_ROOT
    / ".specify"
    / "specs"
    / "070-subagent-task-teams"
    / "notes"
    / "red-first-evidence.md"
)

FN_CONTRACT_PINS = {
    "FN-01": (
        "decomposition: auto|off",
        "decomposition_stages: <stage>=auto|on|off",
        "decomposition_slot_cap: <int>` (default 2)",
        "decomposition_override: auto|on|off",
        "spine fields, not new command arguments",
    ),
    "FN-02": (
        "hard opt-out",
        "no stage override can re-enable it",
        "stage-attempt override wins over the per-stage map",
        "which wins over the built-in defaults",
    ),
    "FN-03": (
        "`plan`, `implement`, and `review` are `auto`",
        "`analyze` and `clarify` are `off`",
        "`requirements`, `tasks`, and `checklist` are `off`",
    ),
    "FN-04": (
        "`auto` resolves to `decomposed`",
        "at least two packages",
        "WG-13 benefit test",
        "`single-package` with `reason=not-beneficial`",
    ),
    "FN-05": (
        "run the standard single-subagent stage path",
        "unchanged stage prompt",
        "No new argument, field, or service",
        "FR-025 keeps that discipline in force",
    ),
    "FN-06": (
        "`decision=fallback`",
        "`gate-reject`",
        "`decomposition-unavailable`",
        "`not-beneficial`",
        "A fallback always names its cause",
    ),
    "FN-07": (
        "never continues with a partial package set",
        "records the failure reason and the fallback in the spine",
        "or stops if the single-package path is unavailable",
    ),
    "FN-08": (
        "Every stage writes one decomposition decision",
        "the literal `no-gate-run`",
        "The plan fence is the canonical decision record",
        "A silent run is a gate failure",
    ),
    "FN-09": ("Feature 070 adds pre-U4 steps only",),
    "FN-10": (
        "fast lane",
        "two-slot test budget",
        "plan minor-fix constraint",
        "targeted-set-v1",
    ),
    "FN-11": ("reused read-only", "creates no second registry"),
    "FN-12": (
        "extended, never replaced",
        "ledger dispatch event carries the 067 fields",
    ),
    "FN-13": (
        "exec-quant feedback channel is unchanged",
        "no new runtime record type",
    ),
    "FN-14": (
        "Contract tests pin",
        "Unit tests cover the two scripts",
        "Fixture dry runs prove",
        "A non-regression file proves",
        "Mutation drills prove",
    ),
    "FN-15": (
        "New behavior is red before implementation",
        "command, exit code, pass/fail counts, changed paths, and an evidence pointer",
        "would not turn red",
    ),
    "FN-16": (
        "Delivery is confined to",
        "No runtime service",
        "persisted team directory is added",
    ),
}


@pytest.mark.parametrize("clause", sorted(FN_CONTRACT_PINS))
def test_fn_contract_clause_keeps_its_normative_content(clause):
    """One pin per FN clause; the contract file owns the clause text."""
    text = FN_CONTRACT.read_text(encoding="utf-8")
    for fragment in FN_CONTRACT_PINS[clause]:
        assert fragment in text, "%s lost its normative content: %s" % (
            clause,
            fragment,
        )


def test_fn_contract_file_covers_the_closed_clause_set():
    text = FN_CONTRACT.read_text(encoding="utf-8")
    ids = re.findall(r"^- \*\*(FN-\d{2})\b", text, re.MULTILINE)
    assert ids == ["FN-%02d" % index for index in range(1, 17)], (
        "the FN contract must carry FN-01…FN-16 once, in order; got %r" % ids
    )


def test_fn_model_doc_carries_the_runtime_projection():
    """T035: the runtime owner names the opt-out, fallback, and preserved rules."""
    text = _model_text()
    for token in (
        "## 20. Opt-out and fallback (FN-01…FN-08)",
        "## 21. Preserved behaviors, test matrix, and delivery surface (FN-09…FN-16)",
        "decomposition_stages",
        "decomposition_override",
        "decomposition_slot_cap",
        "hard opt-out",
        "`gate-reject`",
        "`decomposition-unavailable`",
        "`not-beneficial`",
        "`no-gate-run`",
        "canonical decision record",
        "partial package set",
        "adds pre-U4 steps only",
        "FN-09…FN-16",
        "mutation drills",
        "T036",
    ):
        assert token in text, "runtime projection missing: %s" % token


# ---------------------------------------------------------------- FN-01…FN-03


def test_fn_01_declaration_fields_carry_documented_defaults():
    resolved = wp_driver_sim.normalize_entry_declaration()
    assert resolved["decomposition"] == "auto"
    assert resolved["decomposition_slot_cap"] == 2
    assert resolved["decomposition_stages"] == {
        "plan": "auto",
        "implement": "auto",
        "review": "auto",
        "analyze": "off",
        "clarify": "off",
        "requirements": "off",
        "tasks": "off",
        "checklist": "off",
    }

    explicit = wp_driver_sim.normalize_entry_declaration(
        {
            "decomposition": "off",
            "decomposition_stages": {"plan": "on", "analyze": "off"},
            "decomposition_slot_cap": 3,
        }
    )
    assert explicit["decomposition"] == "off"
    assert explicit["decomposition_slot_cap"] == 3
    assert explicit["decomposition_stages"]["plan"] == "on"
    assert explicit["decomposition_stages"]["analyze"] == "off"


@pytest.mark.parametrize(
    "entry,override,stage,expected_mode,expected_source",
    [
        ({"decomposition": "off"}, "on", "plan", "off", "feature-off"),
        ({"decomposition": "off"}, None, "implement", "off", "feature-off"),
        (None, "off", "plan", "off", "stage-override"),
        (None, "on", "analyze", "on", "stage-override"),
        ({"decomposition_stages": {"implement": "on"}}, None, "implement", "on", "stage-map"),
        ({"decomposition_stages": {"clarify": "off"}}, "auto", "clarify", "auto", "stage-override"),
        ({}, None, "review", "auto", "builtin-default"),
        ({}, None, "tasks", "off", "builtin-default"),
    ],
)
def test_fn_02_precedence_is_feature_off_then_override_then_map_then_default(
    entry, override, stage, expected_mode, expected_source
):
    resolved = wp_driver_sim.resolve_decomposition_mode(
        stage, entry=entry, override=override
    )
    assert resolved == {"mode": expected_mode, "source": expected_source}


@pytest.mark.parametrize(
    "stage,expected",
    [
        ("plan", "auto"),
        ("implement", "auto"),
        ("review", "auto"),
        ("analyze", "off"),
        ("clarify", "off"),
        ("requirements", "off"),
        ("tasks", "off"),
        ("checklist", "off"),
    ],
)
def test_fn_03_builtin_defaults_are_the_closed_map(stage, expected):
    assert wp_driver_sim.BUILTIN_DECOMPOSITION_DEFAULTS[stage] == expected


# ---------------------------------------------------------------- FN-04…FN-08


def test_fn_04_auto_requires_admit_two_packages_and_the_benefit_test():
    two = wp_fixtures.make_two_package_plan()
    one = wp_fixtures.make_single_package_plan()

    admitted = wp_driver_sim.decide_stage_decomposition(
        two, gate_verdict="admit", beneficial=True
    )
    assert admitted["decision"] == "decomposed"
    assert admitted["gate_verdict"] == "admit"

    no_benefit = wp_driver_sim.decide_stage_decomposition(
        two, gate_verdict="admit", beneficial=False
    )
    assert no_benefit["decision"] == "single-package"
    assert no_benefit["reason"] == "not-beneficial"
    assert no_benefit["gate_verdict"] == "single-package"

    one_package = wp_driver_sim.decide_stage_decomposition(
        one, gate_verdict="admit", beneficial=True
    )
    assert one_package["decision"] == "single-package"
    assert one_package["reason"] == "not-beneficial"

    gate_single = wp_driver_sim.decide_stage_decomposition(
        two, gate_verdict="single-package", beneficial=True
    )
    assert gate_single["decision"] == "single-package"
    assert gate_single["gate_verdict"] == "single-package"

    # An explicit stage `on` is not gated by the auto benefit test (FN-02 wins).
    explicit_on = wp_driver_sim.decide_stage_decomposition(
        two, override="on", gate_verdict="admit", beneficial=False
    )
    assert explicit_on["decision"] == "decomposed"
    assert explicit_on["mode_source"] == "stage-override"


def test_fn_05_non_decomposed_decisions_run_the_standard_stage_path():
    plan = wp_fixtures.make_single_package_plan()
    cases = [
        ({"decomposition": "off"}, "admit", "disabled", "no-gate-run"),
        (None, "single-package", "single-package", "single-package"),
        (None, "admit", "single-package", "single-package"),
    ]
    for entry, verdict, expected_decision, expected_verdict in cases:
        outcome = wp_driver_sim.run_stage_attempt(
            plan, entry=entry, gate_verdict=verdict
        )
        record = outcome["decision"]
        assert record["decision"] == expected_decision
        assert record["gate_verdict"] == expected_verdict
        assert outcome["dispatch"] is None
        standard = outcome["standard_path"]
        assert standard["prompt"] == "unchanged"
        assert standard["dispatch"] == "runner-native"
        assert standard["sentinel"] == "PLAN-DONE"
        assert standard["u4"] == "unchanged"
        assert standard["integrator"] is False
        assert standard["packages_dispatched"] == []

    implement = wp_fixtures.make_single_package_plan(stage="implement")
    outcome = wp_driver_sim.run_stage_attempt(
        implement, entry={"decomposition": "off"}, gate_verdict="admit"
    )
    assert outcome["standard_path"]["sentinel"] == "IMPLEMENT-DONE"
    assert outcome["standard_path"]["part_discipline"] == "067-preserved"


def test_fn_06_fallback_causes_are_the_closed_named_set():
    plan = wp_fixtures.make_two_package_plan()

    unavailable = wp_driver_sim.decide_stage_decomposition(
        plan, gate_error="decomposition-unavailable"
    )
    assert unavailable["decision"] == "fallback"
    assert unavailable["reason"] == "decomposition-unavailable"
    assert unavailable["gate_verdict"] == "no-gate-run"
    assert unavailable["fallback"] is True

    rejected = wp_driver_sim.decide_stage_decomposition(
        plan, gate_verdict="reject"
    )
    assert rejected["decision"] == "fallback"
    assert rejected["reason"] == "gate-reject"
    assert rejected["gate_verdict"] == "no-gate-run"

    repaired = wp_driver_sim.decide_stage_decomposition(
        plan,
        gate_verdict="reject",
        repair=lambda candidate: {
            "verdict": "reject",
            "findings": [{"code": "cycle"}],
        },
    )
    assert repaired["repaired"] is True
    assert repaired["reason"] == "gate-reject"
    assert repaired["findings"] == [{"code": "cycle"}]

    repaired_ok = wp_driver_sim.decide_stage_decomposition(
        plan,
        gate_verdict="reject",
        repair=lambda candidate: {"verdict": "admit"},
        beneficial=True,
    )
    assert repaired_ok["repaired"] is True
    assert repaired_ok["decision"] == "decomposed"

    unrepresentable = wp_driver_sim.decide_stage_decomposition(
        plan, gate_verdict="admit", beneficial=True, representable=False
    )
    assert unrepresentable["decision"] == "fallback"
    assert unrepresentable["reason"] == "not-beneficial"
    assert unrepresentable["gate_verdict"] == "no-gate-run"

    reasons = {
        unavailable["reason"],
        rejected["reason"],
        repaired["reason"],
        unrepresentable["reason"],
    }
    assert reasons <= {
        "gate-reject",
        "decomposition-unavailable",
        "not-beneficial",
    }


def test_fn_07_fallback_never_runs_a_partial_package_set():
    plan = wp_fixtures.make_two_package_plan()
    outcome = wp_driver_sim.run_stage_attempt(
        plan,
        gate_verdict="reject",
        repair=lambda candidate: {"verdict": "reject"},
    )
    record = outcome["decision"]
    assert record["decision"] == "fallback"
    assert record["attempted_packages"] == ["plan-wp01", "plan-wp02"]
    assert record["dispatched_packages"] == []
    assert record["dispatch_packages"] == []
    assert outcome["dispatch"] is None
    assert outcome["standard_path"]["packages_dispatched"] == []
    assert outcome["standard_path"]["sentinel"] == "PLAN-DONE"

    stopped = wp_driver_sim.decide_stage_decomposition(
        plan, gate_verdict="reject", single_package_available=False
    )
    assert stopped["decision"] == "fallback"
    assert stopped["stopped"] is True
    assert stopped["single_package_available"] is False


def test_fn_08_every_stage_records_one_decision_with_the_mapped_verdict():
    two = wp_fixtures.make_two_package_plan()
    two["plan_hash"] = wp_fixtures.canonical_hash_of(two)
    one = wp_fixtures.make_single_package_plan()
    one["plan_hash"] = wp_fixtures.canonical_hash_of(one)

    cases = [
        (
            two,
            {"gate_verdict": "admit", "beneficial": True},
            "decomposed",
            "admit",
        ),
        (one, {"gate_verdict": "single-package"}, "single-package", "single-package"),
        (one, {"entry": {"decomposition": "off"}}, "disabled", "no-gate-run"),
        (two, {"gate_verdict": "reject"}, "fallback", "no-gate-run"),
    ]
    for plan, kwargs, expected_decision, expected_verdict in cases:
        record = wp_driver_sim.decide_stage_decomposition(plan, **kwargs)
        assert record["decision"] == expected_decision
        assert record["gate_verdict"] == expected_verdict
        assert record["reason"]
        fence = record["plan_fence"]
        assert fence["decision"] == expected_decision
        assert fence["gate_verdict"] == expected_verdict
        assert fence["reason"] == record["reason"]
        assert fence["plan_hash"] == plan["plan_hash"]
        event = record["ledger_plan_event"]
        assert event["event"] == "plan"
        assert event["plan_hash"] == plan["plan_hash"]
        assert event["decision"] == expected_decision
        assert event["verdict"] == expected_verdict


# ---------------------------------------------------------------- FN-09…FN-16


def test_fn_09_to_fn_13_preserved_behaviors_are_cited_not_redefined():
    text = _model_text()
    for token in (
        "FN-09",
        "FN-10",
        "FN-11",
        "FN-12",
        "FN-13",
        "stage sentinel",
        "U4",
        "stage chain",
        "fast lane",
        "two-slot test budget",
        "plan minor-fix constraint",
        "Feature 064",
        "Feature 067",
        "Feature 068",
    ):
        assert token in text, "preserved-behavior citation missing: %s" % token

    record = wp_driver_sim.decide_stage_decomposition(
        wp_fixtures.make_two_package_plan(), gate_verdict="admit", beneficial=True
    )
    assert record["adds_pre_u4_steps_only"] is True


def test_fn_14_the_declared_test_matrix_exists():
    matrix = [
        REPO_ROOT / "tests/contract/test_sdd_loop_driver_wp_model.py",
        REPO_ROOT / "tests/contract/test_sdd_loop_driver_wp_gate.py",
        REPO_ROOT / "tests/contract/test_sdd_loop_driver_wp_coordination.py",
        REPO_ROOT / "tests/contract/test_sdd_loop_driver_wp_preset.py",
        REPO_ROOT / "tests/unit/test_wp_gate.py",
        REPO_ROOT / "tests/unit/test_wp_report.py",
        REPO_ROOT / "tests/integration/test_wp_coordination_dry_runs.py",
        REPO_ROOT / "tests/contract/test_non_regression_070.py",
    ]
    for path in matrix:
        assert path.is_file(), "declared test surface missing: %s" % path

    dry_runs = (
        REPO_ROOT / "tests/integration/test_wp_coordination_dry_runs.py"
    ).read_text(encoding="utf-8")
    for name in (
        "test_concurrent_read_only_dispatch_overlaps_intervals",
        "test_ownership_path_rejection_blocks_dispatch",
        "test_fallback_never_dispatches_a_partial_package_set",
        "test_single_package_decision_runs_the_standard_stage_path",
        "test_nested_driver_prompt_is_blocked_and_not_dispatched",
        "test_no_team_directory_is_created",
    ):
        assert name in dry_runs, "dry-run matrix entry missing: %s" % name

    tasks = (
        REPO_ROOT
        / ".specify"
        / "specs"
        / "070-subagent-task-teams"
        / "tasks.md"
    ).read_text(encoding="utf-8")
    assert "tests/contract/test_wp_mutation_drills.py" in tasks, (
        "the mutation-drill obligation (T036) must remain in the task file"
    )
    assert "mutation drills" in _model_text()


def test_fn_15_red_first_evidence_records_the_required_fields():
    notes = RED_FIRST_NOTES.read_text(encoding="utf-8")
    assert "## T034" in notes, "T034 has no red-first evidence section"
    section = notes.split("## T034", 1)[1]
    for token in ("Command", "Real output", "Exit code", "Changed paths"):
        assert token in section, "T034 red-first record missing: %s" % token
    assert re.search(r"Exit code[^\n]*`[1-9]\d*`", section), (
        "the T034 record must carry a non-zero exit code"
    )


def test_fn_16_delivery_surface_adds_no_runtime_or_duplicate_surface():
    assert sorted(path.name for path in DRIVER_ROOT.iterdir()) == [
        "SKILL.md",
        "references",
        "scripts",
        "templates",
    ]
    assert not (DRIVER_ROOT / "teams").exists()
    assert (DRIVER_ROOT / "templates" / "stage-team-preset.md").is_file()
    assert not (
        REPO_ROOT
        / "skills"
        / "internal"
        / "create-team"
        / "templates"
        / "teams"
        / "sdd-stage-team.md"
    ).exists(), "the stage-team preset must not enter the create-team catalog"

    text = _model_text()
    for token in (
        "Delivery is confined to",
        "No runtime service",
        "second registry",
        "persisted team",
    ):
        assert token in text, "delivery boundary missing: %s" % token
