"""Deterministic dry-run simulator for the Feature 070 coordination algorithm.

Test-only: nothing here touches the repository or a real line state spine. The
scheduler models SD-01…SD-12 (readiness, write-alone, slot cap, deterministic
order, collection, verifier dispatch, failure isolation, re-entry) with a
logical clock. ``verify`` models VI-01…VI-06 (independent verifiers, verdict
records, fail-closed handling) and ``integrate`` models VI-06…VI-14
(aggregation, declared integration order, conflict stop, closing commit,
integrator seat, unchanged stage U4, driver-owned closure).
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from . import wp_fixtures

# Deterministic fixture graph: two independent read-only packages and one write
# package that depends on the first read-only package.
SIM_READ_A = "plan-wp01"
SIM_READ_B = "plan-wp02"
SIM_WRITE = "plan-wp03"

TERMINAL_OUTCOMES = (
    "failed",
    "stalled",
    "budget-exhausted",
    "missing-sentinel",
    "anomaly",
)
RUNNER_STATUS = {
    "done": "DONE",
    "failed": "FAILED",
    "stalled": "STALLED",
    "budget-exhausted": "BUDGET-EXHAUSTED",
}
LOAD_SKILL = re.compile(
    r"\b(load|use|invoke|read)\b[^.]{0,60}\bskill\b", re.IGNORECASE
)
LOOP_LOGIC = re.compile(
    r"\b(while|repeat\s+until|loop\s+until|for\s+each\s+package|"
    r"dispatch\s+the\s+next)\b",
    re.IGNORECASE,
)


def sim_packages() -> list:
    read_a = wp_fixtures.make_package(
        SIM_READ_A,
        outputs=["findings/read-a.md"],
        bounded_by={"unit": "tasks", "count": 2},
    )
    read_b = wp_fixtures.make_package(
        SIM_READ_B,
        source_refs=["contracts/scheduler-and-dispatch.md#SD-04"],
        inputs=["contracts/scheduler-and-dispatch.md"],
        outputs=["findings/read-b.md"],
        read_only_paths=["contracts/scheduler-and-dispatch.md"],
        bounded_by={"unit": "tasks", "count": 2},
    )
    write = wp_fixtures.make_write_package(
        SIM_WRITE,
        depends_on=[SIM_READ_A],
        outputs=["src/generated/sim.md"],
        bounded_by={"unit": "tasks", "count": 1},
    )
    return [read_a, read_b, write]


def sim_plan() -> dict:
    return wp_fixtures.make_plan(
        packages=sim_packages(),
        pattern="serial",
        slot_cap=2,
    )


def dispatch_layers(plan: dict) -> list:
    """WP-04 layers: roots at 0, sorted by wp_id within each layer."""
    packages = plan["packages"]
    ids = {package["wp_id"] for package in packages}
    graph = {
        package["wp_id"]: sorted(
            {dep for dep in package["depends_on"] if dep in ids}
        )
        for package in packages
    }
    indegree = {
        node: len(dependencies) for node, dependencies in graph.items()
    }
    ready = sorted(node for node, count in indegree.items() if count == 0)
    order = []
    while ready:
        node = ready.pop(0)
        order.append(node)
        for other, dependencies in graph.items():
            if node in dependencies:
                indegree[other] -= 1
                if indegree[other] == 0:
                    ready.append(other)
        ready.sort()
    if len(order) < len(graph):
        raise ValueError("plan contains a dependency cycle")
    depth = {}
    for node in order:
        dependencies = graph[node]
        depth[node] = (
            0
            if not dependencies
            else 1 + max(depth[dep] for dep in dependencies)
        )
    if not depth:
        return []
    return [
        sorted(node for node, value in depth.items() if value == level)
        for level in range(max(depth.values()) + 1)
    ]


def stage_team_pattern(plan: dict) -> str:
    """ST-06: graph-derived pattern; ``continuous`` is never selected."""
    packages = plan.get("packages") or []
    if plan.get("repair_loop"):
        return "iteration"
    independent = not any(package.get("depends_on") for package in packages)
    all_read_only = all(
        package.get("kind") == "read-only" for package in packages
    )
    if len(packages) >= 2 and independent and all_read_only:
        return "parallel"
    return "serial"


def adapt_stage_team(plan: dict) -> dict:
    """ST-08/ST-12: project the preset plus the graph into a run-scoped plan.

    Pure function: it writes no file, creates no team directory, and has no
    goal binding or run report. The graph-derived pattern, the resolved slot
    cap, and the per-package seat mapping take precedence over the preset's
    declared defaults.
    """
    topology = plan.get("topology", "native")
    execution_form = (
        "detached-runner" if topology == "detached" else "native"
    )
    seats = [
        {
            "wp_id": package["wp_id"],
            "role": "stage-worker",
            "stage": "executor",
            "type": "Worker",
            "execution_form": execution_form,
            "lifetime": "one-package",
        }
        for package in plan.get("packages", [])
    ]
    seats.extend(
        [
            {
                "wp_id": None,
                "role": "stage-planner",
                "stage": "executor",
                "type": "Worker",
                "execution_form": "driver",
                "lifetime": "stage",
            },
            {
                "wp_id": None,
                "role": "stage-verifier",
                "stage": "evaluator",
                "type": "Worker",
                "execution_form": "fresh-context",
                "lifetime": "one-verdict",
            },
            {
                "wp_id": None,
                "role": "stage-integrator",
                "stage": "executor",
                "type": "Worker",
                "execution_form": "integrator",
                "lifetime": "one-stage-attempt",
            },
        ]
    )
    return {
        "schema_version": 1,
        "preset_id": "sdd-stage-team",
        "stage": plan.get("stage"),
        "line_id": plan.get("line_id"),
        "plan_hash": plan.get("plan_hash"),
        "pattern": stage_team_pattern(plan),
        "slot_cap": plan.get("slot_cap", 1),
        "topology": topology,
        "seats": seats,
        "team_directory": None,
    }


def check_dispatch_prompt(prompt: str) -> dict:
    """SD-13's three prohibitions, applied before a package is dispatched."""
    text = prompt or ""
    findings = []
    if "sdd-loop-driver" in text.lower():
        findings.append(
            {
                "code": "prompt-names-driver",
                "detail": "the package prompt names sdd-loop-driver",
            }
        )
    if LOAD_SKILL.search(text) or "skill:" in text.lower():
        findings.append(
            {
                "code": "prompt-loads-skill",
                "detail": "the package prompt instructs a skill load",
            }
        )
    if LOOP_LOGIC.search(text):
        findings.append(
            {
                "code": "prompt-loop-logic",
                "detail": "the package prompt contains loop logic",
            }
        )
    return {"ok": not findings, "findings": findings}


def _max_concurrent(dispatches: list) -> int:
    events = []
    for dispatch in dispatches:
        events.append((dispatch["started_at"], 1))
        events.append((dispatch["ended_at"], -1))
    events.sort(key=lambda item: (item[0], item[1]))
    current = 0
    maximum = 0
    for _, delta in events:
        current += delta
        maximum = max(maximum, current)
    return maximum


def schedule(
    plan: dict,
    *,
    outcomes=None,
    verdicts=None,
    slot_cap=None,
    host_parallel=True,
    topology="native",
    durations=None,
    prompts=None,
    completed=None,
    default_duration=10,
):
    """Simulate SD-01…SD-12 on a logical clock.

    ``outcomes`` maps wp_id to one of ``done`` (default), ``failed``,
    ``stalled``, ``budget-exhausted``, ``missing-sentinel`` or ``anomaly``.
    ``verdicts`` maps a completed wp_id to ``pass`` (default), ``fail`` or
    ``missing``. ``completed`` lists packages inherited as verified from the
    spine on re-entry. Every interval is logical time, never wall-clock.
    """
    packages = {
        package["wp_id"]: package for package in plan["packages"]
    }
    layers = dispatch_layers(plan)
    layer_index = {
        wp_id: index
        for index, layer in enumerate(layers)
        for wp_id in layer
    }
    if slot_cap is None:
        slot_cap = plan.get("slot_cap", 1)
    outcomes = dict(outcomes or {})
    verdict_map = dict(verdicts or {})
    durations = dict(durations or {})
    prompts = dict(prompts or {})
    completed_from_spine = sorted(set(completed or ()))
    stage_attempt = plan.get("stage_attempt", 1)
    stage = plan.get("stage", "stage")
    line_id = plan.get("line_id", "line")

    if topology == "detached":
        effective_topology = "detached-runner"
        topology_record = {
            "requested": "detached",
            "effective": "detached-runner",
            "reason": None,
        }
    elif not host_parallel:
        effective_topology = "serial-native"
        topology_record = {
            "requested": "native",
            "parallel_requested": "yes",
            "effective": "serial",
            "reason": "host-no-parallel-native",
        }
    else:
        effective_topology = "parallel-native"
        topology_record = {
            "requested": "native",
            "effective": "parallel-native",
            "reason": None,
        }

    verified = set(completed_from_spine)
    failed = set()
    unverified = set()
    blocked = set()
    running = {}
    dispatches = []
    settles = []
    verdict_records = []
    verifier_dispatches = []
    prompt_blocks = []
    anomalies = []
    dispatch_order = []
    clock = 0
    executor_seq = 0
    verifier_seq = 0

    def order_key(wp_id):
        return (layer_index.get(wp_id, 0), wp_id)

    def dependency_status(wp_id):
        dependencies = packages[wp_id]["depends_on"]
        if any(
            dep in failed or dep in unverified or dep in blocked
            for dep in dependencies
        ):
            return "bad"
        if all(dep in verified for dep in dependencies):
            return "ready"
        return "waiting"

    def propagate_blocked():
        changed = True
        while changed:
            changed = False
            for wp_id in packages:
                if (
                    wp_id in verified
                    or wp_id in failed
                    or wp_id in unverified
                    or wp_id in blocked
                    or wp_id in running
                ):
                    continue
                if dependency_status(wp_id) == "bad":
                    blocked.add(wp_id)
                    changed = True

    def startable():
        result = []
        for wp_id in packages:
            if (
                wp_id in verified
                or wp_id in failed
                or wp_id in unverified
                or wp_id in blocked
                or wp_id in running
            ):
                continue
            if packages[wp_id].get("superseded_by"):
                continue
            if dependency_status(wp_id) == "ready":
                result.append(wp_id)
        return sorted(result, key=order_key)

    def dispatch(wp_id):
        nonlocal executor_seq
        package = packages[wp_id]
        kind = package["kind"]
        end = clock + durations.get(wp_id, default_duration)
        executor_seq += 1
        record = {
            "wp_id": wp_id,
            "kind": kind,
            "stage": stage,
            "stage_attempt": stage_attempt,
            "attempt_id": "%s-a%d-w1" % (wp_id, stage_attempt),
            "dispatch_order": len(dispatches) + 1,
            "started_at": clock,
            "ended_at": end,
            "effective_concurrency": 1
            if kind == "write"
            else len(running) + 1,
            "topology": effective_topology,
            "layer": layer_index.get(wp_id, 0),
            "executor_execution": "executor-%d" % executor_seq,
        }
        if effective_topology == "detached-runner":
            label = "%s-%s" % (stage, wp_id)
            record.update(
                {
                    "runner_label": label,
                    "sentinel": package["sentinel"],
                    "pid_path": "wp/%s.pid" % label,
                    "status_path": "wp/%s.status" % label,
                    "log_path": "wp/%s.log" % label,
                    "heartbeat_path": "wp/%s.heartbeat" % label,
                }
            )
        dispatches.append(record)
        dispatch_order.append(wp_id)
        running[wp_id] = end

    def settle_due():
        nonlocal clock, verifier_seq
        if not running:
            return False
        end = min(running.values())
        clock = end
        due = sorted(
            wp_id for wp_id, finish in running.items() if finish == end
        )
        for wp_id in due:
            del running[wp_id]
            package = packages[wp_id]
            outcome = outcomes.get(wp_id, "done")
            base = "%s-%s-%s-a%dw1" % (
                line_id,
                stage,
                wp_id,
                stage_attempt,
            )
            result_ptr = "wp/%s.result.json" % base
            if outcome in ("missing-sentinel", "anomaly"):
                anomalies.append(
                    {"wp_id": wp_id, "reason": outcome, "at": clock}
                )
                failed.add(wp_id)
                continue
            runner_status = RUNNER_STATUS.get(outcome, "DONE")
            sentinel = package["sentinel"]
            log_last_line = (
                sentinel if runner_status == "DONE" else runner_status
            )
            settles.append(
                {
                    "wp_id": wp_id,
                    "ended_at": clock,
                    "runner_status": runner_status,
                    "result_ptr": result_ptr,
                    "outputs": package["outputs"]
                    if outcome == "done"
                    else [],
                    "sentinel": sentinel,
                    "log_last_line": log_last_line,
                    "result_status": outcome,
                }
            )
            if outcome != "done" or log_last_line != sentinel:
                failed.add(wp_id)
                continue
            verifier_seq += 1
            verifier_execution = "verifier-%d" % verifier_seq
            verifier_dispatches.append(
                {
                    "wp_id": wp_id,
                    "verifier_execution": verifier_execution,
                    "at": clock,
                    "fresh_context": True,
                }
            )
            verdict_value = verdict_map.get(wp_id, "pass")
            if verdict_value == "pass":
                verdict_records.append(
                    {
                        "wp_id": wp_id,
                        "verdict": "pass",
                        "verifier_execution": verifier_execution,
                        "evidence_ptr": "wp/%s.verdict.json" % base,
                        "at": clock,
                    }
                )
                verified.add(wp_id)
            elif verdict_value == "missing":
                anomalies.append(
                    {"wp_id": wp_id, "reason": "missing-verdict", "at": clock}
                )
                unverified.add(wp_id)
            else:
                verdict_records.append(
                    {
                        "wp_id": wp_id,
                        "verdict": "fail",
                        "verifier_execution": verifier_execution,
                        "evidence_ptr": "wp/%s.verdict.json" % base,
                        "at": clock,
                    }
                )
                unverified.add(wp_id)
        return True

    while True:
        propagate_blocked()
        candidates = startable()
        allowed = []
        for wp_id in candidates:
            if wp_id in prompts:
                checked = check_dispatch_prompt(prompts[wp_id])
                if not checked["ok"]:
                    prompt_blocks.append(
                        {
                            "wp_id": wp_id,
                            "findings": checked["findings"],
                            "at": clock,
                        }
                    )
                    anomalies.append(
                        {
                            "wp_id": wp_id,
                            "reason": "prompt-blocked",
                            "at": clock,
                        }
                    )
                    failed.add(wp_id)
                    continue
            allowed.append(wp_id)
        candidates = allowed
        if not candidates and not running:
            break
        writes = [
            wp_id
            for wp_id in candidates
            if packages[wp_id]["kind"] == "write"
        ]
        if writes:
            if running:
                settle_due()
                continue
            dispatch(writes[0])
            settle_due()
            continue
        capacity = 1 if effective_topology == "serial-native" else slot_cap
        launched = False
        for wp_id in candidates:
            if len(running) >= capacity:
                break
            dispatch(wp_id)
            launched = True
        if not running:
            if not launched:
                break
            continue
        settle_due()

    propagate_blocked()
    for wp_id in packages:
        if (
            wp_id in verified
            or wp_id in failed
            or wp_id in unverified
            or wp_id in blocked
        ):
            continue
        blocked.add(wp_id)

    considered = set(packages) - set(completed_from_spine)
    stage_ok = (
        all(wp_id in verified for wp_id in considered)
        and not failed
        and not unverified
        and not blocked
        and not anomalies
    )
    return {
        "coordinator": "driver",
        "plan_hash": plan.get("plan_hash"),
        "dispatch_layers": layers,
        "dispatch_order": dispatch_order,
        "dispatches": dispatches,
        "settles": settles,
        "verdicts": verdict_records,
        "verifier_dispatches": verifier_dispatches,
        "prompt_blocks": prompt_blocks,
        "anomalies": anomalies,
        "failed": sorted(failed),
        "unverified": sorted(unverified),
        "blocked": sorted(blocked),
        "completed_from_spine": completed_from_spine,
        "stage_gate": "pass" if stage_ok else "fail",
        "topology": topology_record,
        "max_concurrent": _max_concurrent(dispatches),
        "clock": clock,
    }


VERDICT_FAILURE_CODES = {
    "missing": "verdict-missing",
    "unreadable": "verdict-unreadable",
    "malformed": "verdict-malformed",
    "ambiguous": "verdict-ambiguous",
}


def _iso_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _verdict_path(plan: dict, wp_id: str, stage_attempt: int, wp_attempt: int) -> str:
    return "wp/%s-%s-%s-a%dw%d.verdict.json" % (
        plan.get("line_id", "line"),
        plan.get("stage", "stage"),
        wp_id,
        stage_attempt,
        wp_attempt,
    )


def _check_kind(text: str) -> str:
    lowered = (text or "").lower()
    for kind in ("adversarial", "ownership", "contract", "test"):
        if kind in lowered:
            return kind
    return "artifact"


def results_from_schedule(dispatch: dict) -> dict:
    """Project E5-style result records from a ``schedule()`` dry run."""
    by_id = {item["wp_id"]: item for item in dispatch["dispatches"]}
    results = {}
    for settle in dispatch["settles"]:
        record = by_id[settle["wp_id"]]
        match = re.search(r"-w(\d+)$", record["attempt_id"])
        results[settle["wp_id"]] = {
            "schema_version": 1,
            "wp_id": settle["wp_id"],
            "stage": record.get("stage", "stage"),
            "stage_attempt": record.get("stage_attempt", 1),
            "wp_attempt": int(match.group(1)) if match else 1,
            "attempt_id": record["attempt_id"],
            "status": settle["result_status"],
            "outputs": list(settle["outputs"]),
            "changed_paths": [],
            "tests": "not_evaluated",
            "commits": [],
            "result_ptr": settle["result_ptr"],
            "executor_execution": record["executor_execution"],
            "ended_at": settle["ended_at"],
        }
    return results


def verify(
    plan: dict,
    results: dict,
    *,
    verdicts=None,
    host_can_spawn: bool = True,
    topology: str = "native",
    state_dir=None,
):
    """VI-01…VI-06: one independent verifier per settled package, fail-closed.

    ``verdicts`` maps a ``done`` package to ``pass`` (default), ``fail``, or
    one of ``missing``/``unreadable``/``malformed``/``ambiguous``. The last
    four model unusable verdict artifacts and MUST resolve to a fail event
    (VI-04). ``host_can_spawn=False`` models the recorded ``driver-u4``
    capability fallback (VI-01).
    """
    results = dict(results or {})
    overrides = dict(verdicts or {})
    packages = {item["wp_id"]: item for item in plan.get("packages", [])}
    stage = plan.get("stage", "stage")
    stage_attempt = plan.get("stage_attempt", 1)
    detached = topology in ("detached", "detached-runner")

    ordered = sorted(
        packages,
        key=lambda wp_id: (
            results.get(wp_id, {}).get("ended_at", 0),
            wp_id,
        ),
    )
    verifier_executions = []
    verdict_records = []
    verdict_events = []
    findings = []
    verified = []
    failed = []
    unverified = []
    state_dir_writes = []
    verifier_seq = 0

    for wp_id in ordered:
        result = results.get(wp_id)
        if result is None:
            unverified.append(wp_id)
            findings.append(
                {
                    "code": "result-missing",
                    "wp_id": wp_id,
                    "evidence_refs": [plan.get("plan_hash") or "plan"],
                }
            )
            continue
        if result.get("status") != "done":
            failed.append(wp_id)
            findings.append(
                {
                    "code": "result-%s" % result.get("status", "unknown"),
                    "wp_id": wp_id,
                    "evidence_refs": [
                        result.get("result_ptr") or "wp/%s" % wp_id
                    ],
                }
            )
            continue

        verifier_seq += 1
        kind = (
            "driver-u4"
            if not host_can_spawn
            else ("runner" if detached else "native")
        )
        if kind == "native":
            execution_id = "verifier-%d" % verifier_seq
        elif kind == "runner":
            execution_id = "%s-%s-verify" % (stage, wp_id)
        else:
            execution_id = "driver-u4-%d" % verifier_seq
        executor_execution = result.get(
            "executor_execution", "executor-unknown"
        )
        started_at = result.get("ended_at", 0)
        ended_at = started_at + 1
        verifier_executions.append(
            {
                "execution_id": execution_id,
                "kind": kind,
                "wp_id": wp_id,
                "started_at": started_at,
                "ended_at": ended_at,
                "fresh_context": kind != "driver-u4",
                "read_only": True,
                "independent": execution_id != executor_execution,
                "fallback_reason": (
                    "host-no-subagent" if kind == "driver-u4" else None
                ),
            }
        )

        attempt = result.get("stage_attempt", stage_attempt)
        wp_attempt = result.get("wp_attempt", 1)
        path = _verdict_path(plan, wp_id, attempt, wp_attempt)
        override = overrides.get(wp_id, "pass")

        if override in VERDICT_FAILURE_CODES:
            value = "fail"
            unverified.append(wp_id)
            findings.append(
                {
                    "code": VERDICT_FAILURE_CODES[override],
                    "wp_id": wp_id,
                    "evidence_refs": [path],
                }
            )
        else:
            value = "pass" if override == "pass" else "fail"
            package = packages[wp_id]
            checks = [
                {
                    "id": item.get("id"),
                    "kind": _check_kind(item.get("check", "")),
                    "command": None,
                    "result": value,
                    "evidence_ref": item.get("evidence"),
                }
                for item in package.get("acceptance", [])
            ]
            evidence_refs = sorted(
                {
                    item.get("evidence")
                    for item in package.get("acceptance", [])
                    if item.get("evidence")
                }
                | {result.get("result_ptr") or path}
            )
            record = {
                "schema_version": 1,
                "wp_id": wp_id,
                "stage": stage,
                "stage_attempt": attempt,
                "wp_attempt": wp_attempt,
                "verdict": value,
                "checks": checks,
                "evidence_refs": evidence_refs,
                "execution_id": execution_id,
                "verified_at": _iso_now(),
                "path": path,
                "read_only": True,
                "full_suite_run": False,
            }
            verdict_records.append(record)
            if value == "pass":
                verified.append(wp_id)
            else:
                unverified.append(wp_id)
                findings.append(
                    {
                        "code": "verdict-fail",
                        "wp_id": wp_id,
                        "evidence_refs": [path],
                    }
                )
            if state_dir is not None:
                destination = Path(state_dir) / path
                destination.parent.mkdir(parents=True, exist_ok=True)
                payload = {
                    key: item
                    for key, item in record.items()
                    if key != "path"
                }
                destination.write_text(
                    json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )
                state_dir_writes.append(path)

        event = {
            "event": "verdict",
            "wp_id": wp_id,
            "verdict": value,
            "verifier_execution": execution_id,
            "evidence_ptr": path,
            "at": ended_at,
        }
        if kind == "driver-u4":
            event["verification_fallback"] = "host-no-subagent"
        verdict_events.append(event)

    all_verified = (
        len(verified) == len(packages) and not failed and not unverified
    )
    return {
        "verifier_executions": verifier_executions,
        "verdicts": verdict_records,
        "verdict_events": verdict_events,
        "verified": sorted(verified),
        "failed": sorted(failed),
        "unverified": sorted(unverified),
        "findings": findings,
        "state_dir_writes": state_dir_writes,
        "repository_writes": [],
        "full_suite_runs": 0,
        "targeted_tests_only": True,
        "stage_gate": "pass" if all_verified else "fail",
    }


def integrate(
    plan: dict,
    verification: dict,
    *,
    results=None,
    outputs=None,
    contents=None,
    part_commits=None,
    u4=None,
    integrator_last_line=None,
):
    """VI-06…VI-14: aggregate, integrate in declared order, then run stage U4.

    ``contents`` maps an output path to a source->content mapping (or a single
    content shared by every source). Differing content for one path from two
    sources is a contradiction and stops integration (VI-06, VI-08).
    ``outputs`` overrides a package's produced outputs; without it the E5 result
    record is authoritative. A verified package with no result record is
    represented by its declared outputs, which is a dry-run convenience only.
    """
    packages = {item["wp_id"]: item for item in plan.get("packages", [])}
    order = [wp_id for layer in dispatch_layers(plan) for wp_id in layer]
    verified = set(verification.get("verified") or [])
    failed = set(verification.get("failed") or [])
    unverified = set(verification.get("unverified") or [])
    verification_gate = verification.get("stage_gate", "pass")

    results = dict(results or {})
    outputs = dict(outputs or {})
    contents = dict(contents or {})
    u4 = dict(u4 or {})
    stage = plan.get("stage", "stage")
    stage_attempt = plan.get("stage_attempt", 1)
    implement = stage == "implement"

    def evidence_for(wp_id: str) -> str:
        result = results.get(wp_id) or {}
        return result.get("result_ptr") or _verdict_path(
            plan, wp_id, stage_attempt, 1
        )

    package_outputs = {}
    for wp_id in order:
        if wp_id not in verified:
            continue
        if wp_id in outputs:
            claimed = list(outputs[wp_id])
        elif wp_id in results:
            claimed = list(results[wp_id].get("outputs") or [])
        else:
            claimed = list(packages[wp_id].get("outputs") or [])
        package_outputs[wp_id] = claimed

    required = list(dict.fromkeys(plan.get("required_outputs") or []))
    integrator_expected = list(
        dict.fromkeys(plan.get("integrator_outputs") or [])
    )
    required_packages = [
        item for item in required if item not in integrator_expected
    ]
    produced = {
        output
        for claimed in package_outputs.values()
        for output in claimed
    }
    missing = [item for item in required_packages if item not in produced]
    extra = sorted(produced - set(required_packages))
    findings = []

    for wp_id in sorted(unverified | failed):
        findings.append(
            {
                "code": "verification-incomplete",
                "wp_id": wp_id,
                "evidence_refs": [evidence_for(wp_id)],
            }
        )

    for output in missing:
        producers = [
            wp_id
            for wp_id in order
            if output in (packages[wp_id].get("outputs") or [])
        ]
        findings.append(
            {
                "code": "output-missing",
                "wp_id": producers[0] if producers else None,
                "output": output,
                "evidence_refs": [
                    evidence_for(producers[0])
                    if producers
                    else "wp/%s" % output,
                    "plan:%s#required_outputs"
                    % (plan.get("plan_hash") or "unhashed"),
                ],
            }
        )

    for output in extra:
        producer = next(
            (
                wp_id
                for wp_id, claimed in package_outputs.items()
                if output in claimed
            ),
            None,
        )
        findings.append(
            {
                "code": "output-coverage-extra",
                "wp_id": producer,
                "output": output,
                "evidence_refs": [
                    evidence_for(producer) if producer else "wp/%s" % output,
                    "plan:%s#required_outputs"
                    % (plan.get("plan_hash") or "unhashed"),
                ],
            }
        )

    sources_by_path = {}
    for wp_id, claimed in package_outputs.items():
        for output in claimed:
            sources_by_path.setdefault(output, []).append(wp_id)
    for output in integrator_expected:
        sources_by_path.setdefault(output, []).append("integrator")

    contradictions = []
    for output, sources in sources_by_path.items():
        mapping = contents.get(output)
        if isinstance(mapping, dict):
            values = [
                mapping[source] for source in sources if source in mapping
            ]
        elif mapping is not None:
            values = [mapping]
        else:
            continue
        if len(set(values)) > 1:
            contradictions.append(output)
            refs = [
                "integrator:%s-a%d" % (stage, stage_attempt)
                if source == "integrator"
                else evidence_for(source)
                for source in sources
            ]
            findings.append(
                {
                    "code": "output-contradiction",
                    "output": output,
                    "evidence_refs": refs,
                }
            )

    package_commits = []
    collected_part_commits = []
    for wp_id in order:
        commits = list((results.get(wp_id) or {}).get("commits") or [])
        if implement:
            collected_part_commits.extend(commits)
        else:
            package_commits.extend(commits)
            if commits:
                findings.append(
                    {
                        "code": "package-commit-forbidden",
                        "wp_id": wp_id,
                        "evidence_refs": [evidence_for(wp_id)],
                    }
                )
    if part_commits is not None:
        collected_part_commits = list(part_commits)
    elif not implement:
        collected_part_commits = []

    conflict = bool(findings) or verification_gate != "pass"

    ticks = [0]
    ticks.extend(
        event.get("at", 0)
        for event in verification.get("verdict_events") or []
    )
    ticks.extend(result.get("ended_at", 0) for result in results.values())
    start_tick = max(ticks) + 1
    end_tick = start_tick + 1

    stage_sentinel = "%s-DONE" % stage.upper()
    if integrator_last_line is not None:
        last_line = integrator_last_line
    elif conflict:
        last_line = "ANOMALY: integration-stopped"
    else:
        last_line = stage_sentinel

    integrator = {
        "execution_id": "integrator-%s-a%d" % (stage, stage_attempt),
        "seat": "stage-integrator",
        "stage": stage,
        "stage_attempt": stage_attempt,
        "started_at": start_tick,
        "ended_at": end_tick,
        "inputs": {
            "plan": plan.get("plan_hash"),
            "verified_outputs": {
                wp_id: list(claimed)
                for wp_id, claimed in package_outputs.items()
            },
            "stage_authority": list(plan.get("source_artifacts") or []),
        },
        "integrator_outputs": list(integrator_expected),
        "committed": not conflict,
        "last_non_empty_line": last_line,
        "dispatched_packages": [],
        "replanned": False,
        "loaded_driver": False,
        "fresh_context": True,
    }
    closing = (
        None
        if conflict
        else "integrated-%s-a%d" % (stage, stage_attempt)
    )

    sentinel_ok = last_line == stage_sentinel
    artifacts_ok = u4.get("artifact_verification", "pass") == "pass"
    discipline_ok = u4.get("discipline_checks", "pass") == "pass"
    u4_gate = (
        "pass"
        if (
            sentinel_ok
            and artifacts_ok
            and discipline_ok
            and not conflict
        )
        else "fail"
    )
    stage_u4 = {
        "sentinel": last_line,
        "sentinel_ok": sentinel_ok,
        "artifact_verification": "pass" if artifacts_ok else "fail",
        "artifacts_ok": artifacts_ok,
        "discipline_checks": "pass" if discipline_ok else "fail",
        "discipline_ok": discipline_ok,
        "package_verdicts_substitute": False,
        "at": end_tick + 1,
        "gate": u4_gate,
    }
    integrate_event = {
        "event": "integrate",
        "stage_attempt": stage_attempt,
        "order": list(order),
        "at": end_tick,
        "conflict": conflict,
        "commit": closing,
    }
    stage_gate = (
        "pass"
        if (
            not conflict
            and verification_gate == "pass"
            and u4_gate == "pass"
        )
        else "fail"
    )
    return {
        "integration_order": list(order),
        "at": end_tick,
        "aggregate": {
            "required_package_outputs": required_packages,
            "integrator_outputs_expected": integrator_expected,
            "package_outputs": package_outputs,
            "missing_outputs": missing,
            "extra_outputs": extra,
            "contradictions": contradictions,
            "coverage_ok": not missing and not extra,
        },
        "integrator_outputs": list(integrator_expected),
        "integrator": integrator,
        "conflict": conflict,
        "commit": closing,
        "commits": {
            "closing": closing,
            "package_commits": package_commits,
            "part_commits": collected_part_commits,
            "rewritten": [],
            "squashed": False,
        },
        "integrate_event": integrate_event,
        "stage_u4": stage_u4,
        "stage_gate": stage_gate,
        "findings": findings,
        "closure": {
            "owner": "driver",
            "push": False,
            "force_merge": False,
            "auto_merge": False,
            "confirmation_gates": "preserved",
        },
    }


def run_stage(
    plan: dict,
    *,
    outcomes=None,
    verdicts=None,
    outputs=None,
    contents=None,
    host_can_spawn: bool = True,
    u4=None,
    part_commits=None,
    integrator_last_line=None,
    **schedule_kwargs,
):
    """Schedule, verify, and integrate one decomposed stage attempt."""
    dispatch = schedule(
        plan, outcomes=outcomes, verdicts=verdicts, **schedule_kwargs
    )
    results = results_from_schedule(dispatch)
    verification = verify(
        plan,
        results,
        verdicts=verdicts,
        host_can_spawn=host_can_spawn,
        topology=dispatch.get("topology", {}).get("effective", "native"),
    )
    integration = integrate(
        plan,
        verification,
        results=results,
        outputs=outputs,
        contents=contents,
        part_commits=part_commits,
        u4=u4,
        integrator_last_line=integrator_last_line,
    )
    return {
        "dispatch": dispatch,
        "results": results,
        "verification": verification,
        "integration": integration,
    }
