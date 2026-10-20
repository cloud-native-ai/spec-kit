"""Integration S4: detached stage survives a driver kill and reattaches.

`SDD_RUNNER_MODE=foreground` forces the non-detached shape, which makes the
survival assertion red (mutation drill 2).
"""
from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path

from fixtures.line_fixtures import (
    engine_json,
    kill_driver_group,
    make_line_id,
    make_project,
    make_run_id,
    pid_alive,
    run_engine,
    snapshot,
    start_fake_stage,
    teardown_stage,
    wait_until,
)


def _token(pid: int) -> str:
    proc_path = Path(f"/proc/{pid}/stat")
    if proc_path.exists():
        return proc_path.read_text().split()[21]
    proc = subprocess.run(["ps", "-p", str(pid), "-o", "lstart="], capture_output=True, text=True)
    return " ".join(proc.stdout.split())


def _prepare(tmp_path, duration: float, finish: str = "done"):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    line, run = make_line_id("life"), make_run_id()
    engine_json(
        "register", "--line-id", line, "--run-id", run,
        "--project-dir", str(project), "--repo-root", str(project),
        "--state", "active", reg=reg,
    )
    stage = start_fake_stage(tmp_path, line, run, "plan", duration=duration, finish=finish)
    pid_file = stage["paths"]["pid"]
    assert wait_until(lambda: f"pid={stage['runner'].pid}" in snapshot(pid_file), timeout=5), snapshot(pid_file)
    token = _token(stage["runner"].pid)
    engine_json(
        "update", "--line-id", line, "--stage", "plan",
        "--runner-pid", str(stage["runner"].pid), "--runner-start-token", token,
        "--cli-pid", str(stage["runner"].pid), "--cli-start-token", token,
        "--prompt-path", str(stage["paths"]["prompt_meta"]),
        "--status-path", str(stage["paths"]["status"]),
        "--log-path", str(stage["paths"]["log"]),
        "--heartbeat-path", str(stage["paths"]["heartbeat"]),
        "--last-event", "u2-dispatch", reg=reg,
    )
    return {
        "project": project, "reg": reg, "line": line, "run": run,
        "stage": stage, "token": token,
    }


def _watch(ctx, *extra):
    proc = subprocess.run(
        ["bash", str(Path(__file__).resolve().parents[2] / "skills" / "external" /
                   "sdd-loop-driver" / "scripts" / "watch-target.sh"), "--once",
         "--line-id", ctx["line"], "--run-id", ctx["run"], "--label", ctx["line"],
         "--pid-file", str(ctx["stage"]["paths"]["pid"]),
         "--status-file", str(ctx["stage"]["paths"]["status"]),
         "--log", str(ctx["stage"]["paths"]["log"]),
         "--sentinel", "PLAN-DONE",
         "--heartbeat", str(ctx["stage"]["paths"]["heartbeat"]),
         "--meta", str(ctx["stage"]["paths"]["meta"]),
         "--start-grace", "0", *extra],
        capture_output=True, text=True,
    )
    return proc


def test_detached_stage_survives_driver_kill_and_reattaches(tmp_path):
    ctx = _prepare(tmp_path, duration=6)
    stage = ctx["stage"]
    try:
        lease = engine_json(
            "lease-acquire", "--line-id", ctx["line"], "--session", "old",
            "--pid", str(stage["driver"].pid), reg=ctx["reg"],
        )
        assert lease["holder_session"] == "old"
        engine_json(
            "reserve", "--line-id", ctx["line"], "--stage", "plan",
            "--run-id", ctx["run"], "--pid", str(stage["runner"].pid),
            "--start-token", ctx["token"], reg=ctx["reg"],
        )
        kill_driver_group(stage)  # SIGHUP to the driver process group
        stage["driver"].wait(timeout=3)
        time.sleep(0.4)
        assert pid_alive(stage["runner"].pid), "detached runner must survive the driver kill"
        heartbeat = ctx["stage"]["paths"]["heartbeat"]
        before = heartbeat.stat().st_mtime_ns
        assert wait_until(lambda: heartbeat.stat().st_mtime_ns > before, timeout=3), "heartbeat stopped"

        # New session: stale lease must be broken with evidence, then acquired.
        refused = run_engine(
            "lease-acquire", "--line-id", ctx["line"], "--session", "new",
            "--pid", str(os.getpid()), reg=ctx["reg"],
        )
        assert refused.returncode == 3
        engine_json(
            "lease-break", "--line-id", ctx["line"], "--reason", "driver-killed",
            "--evidence-ref", "notes/kill.md", reg=ctx["reg"],
        )
        engine_json(
            "lease-acquire", "--line-id", ctx["line"], "--session", "new",
            "--pid", str(os.getpid()), reg=ctx["reg"],
        )

        identity = engine_json("verify-identity", "--line-id", ctx["line"], reg=ctx["reg"])
        assert identity["identity"] == "ok"
        assert identity["branch_hint"] == "running"
        running = _watch(ctx)
        assert running.returncode == 10 and "verdict=RUNNING" in running.stdout

        attach = engine_json(
            "reserve", "--line-id", ctx["line"], "--stage", "plan",
            "--run-id", ctx["run"], "--pid", str(stage["runner"].pid),
            "--start-token", ctx["token"], reg=ctx["reg"],
        )
        assert attach["action"] == "attach", "reattach must not launch a second stage"

        assert wait_until(lambda: "exit=" in snapshot(ctx["stage"]["paths"]["status"]), timeout=10)
        done = _watch(ctx)
        assert done.returncode == 0 and "verdict=DONE" in done.stdout
        assert identity["identity"] == "ok"
    finally:
        teardown_stage(stage)


def test_done_branch_skips_redispatch(tmp_path):
    ctx = _prepare(tmp_path, duration=0.5)
    stage = ctx["stage"]
    try:
        assert wait_until(lambda: "exit=" in snapshot(ctx["stage"]["paths"]["status"]), timeout=10)
        stage["runner"].wait(timeout=5)
        identity = engine_json("verify-identity", "--line-id", ctx["line"], reg=ctx["reg"])
        assert identity["branch_hint"] == "done"
        done = _watch(ctx)
        assert done.returncode == 0 and "verdict=DONE" in done.stdout
        reservations = list((ctx["reg"] / "reservations").glob(f"{ctx['line']}.*.json"))
        assert len(reservations) <= 1
    finally:
        teardown_stage(stage)


def test_dead_branch_retains_registry_evidence(tmp_path):
    ctx = _prepare(tmp_path, duration=0.3, finish="fail")
    stage = ctx["stage"]
    try:
        stage["runner"].wait(timeout=10)
        time.sleep(0.2)
        identity = engine_json("verify-identity", "--line-id", ctx["line"], reg=ctx["reg"])
        assert identity["identity"] == "dead"
        dead = _watch(ctx)
        assert dead.returncode == 13 and "verdict=DEAD" in dead.stdout
        entry = json.loads((ctx["reg"] / f"{ctx['line']}.json").read_text())
        assert entry["state"] == "active", "dead branch must not auto-clean the registry"
    finally:
        teardown_stage(stage)


def test_remote_unreachable_is_stalled_not_dead(tmp_path):
    ctx = _prepare(tmp_path, duration=2)
    stage = ctx["stage"]
    try:
        probe = tmp_path / "probe.json"
        probe.write_text(json.dumps({"unreachable": True, "reason": "ssh 255"}), encoding="utf-8")
        classified = engine_json("classify-remote", "--probe-json", str(probe), reg=ctx["reg"])
        assert classified["identity"] == "remote-unreachable"
        identity = engine_json(
            "verify-identity", "--line-id", ctx["line"], "--probe-json", str(probe), reg=ctx["reg"]
        )
        assert identity["identity"] == "remote-unreachable"
        assert identity.get("branch_hint") == "stalled"
    finally:
        teardown_stage(stage)
