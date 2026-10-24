"""Deterministic dry-run simulator for the Feature 070 coordination algorithm.

Test-only: nothing here touches the repository or a real line state spine. The
scheduler models SD-01…SD-12 (readiness, write-alone, slot cap, deterministic
order, collection, verifier dispatch, failure isolation, re-entry) with a
logical clock. Independent verification (VI-01…VI-06) and integration
(VI-07…VI-13) remain explicit stubs until T022, so a dry run cannot silently
pass on unimplemented verification logic.
"""
from __future__ import annotations

import re

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


def verify(plan: dict, results: dict, **kwargs):
    """VI-01…VI-06 independent verification (implemented in T022)."""
    raise NotImplementedError(
        "wp_driver_sim.verify lands with T022 (VI-01…VI-06)"
    )


def integrate(plan: dict, verdicts: dict, **kwargs):
    """VI-07…VI-13 deterministic integration (implemented in T022)."""
    raise NotImplementedError(
        "wp_driver_sim.integrate lands with T022 (VI-07…VI-13)"
    )
