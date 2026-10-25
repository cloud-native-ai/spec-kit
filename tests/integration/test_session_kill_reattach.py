"""Integration S4: the delivered detached runner survives a driver kill and reattaches.

The survival case launches `scripts/run-stage.sh` with the documented
`nohup ... & disown` recipe and SIGHUPs the driver's process group; the
fixture-only shape remains for the done/dead/remote classification cases.
"""
from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

from fixtures.line_fixtures import (
    engine_json,
    kill_driver_group,
    make_line_id,
    make_project,
    make_run_id,
    pid_alive,
    process_token,
    run_engine,
    snapshot,
    start_fake_stage,
    teardown_stage,
    wait_until,
)

SKILL_DIR = Path(__file__).resolve().parents[2] / "skills" / "external" / "sdd-loop-driver"
RUNNER = SKILL_DIR / "scripts" / "run-stage.sh"


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
         "--registry", str(ctx["reg"]),
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


def test_delivered_runner_recipe_survives_driver_kill_and_reattaches(tmp_path):
    """FR-046/047/048: the documented detach recipe + delivered runner are the
    evidence, not a pytest-made process session."""
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    line, run = make_line_id("recipe"), make_run_id()
    engine_json(
        "register", "--line-id", line, "--run-id", run,
        "--project-dir", str(project), "--repo-root", str(project),
        "--state", "active", reg=reg,
    )
    stage_root = tmp_path / "stage"
    stage_root.mkdir()
    paths = {
        "pid": stage_root / f"pid-{line}-plan",
        "status": stage_root / f"status-{line}-plan",
        "log": stage_root / f"log-{line}-plan.log",
        "heartbeat": stage_root / f"heartbeat-{line}-plan.log",
        "meta": stage_root / f"log-{line}-plan.meta.jsonl",
        "prompt": stage_root / f"prompt-{line}-plan.md",
    }
    paths["prompt"].write_text("plan stage\n", encoding="utf-8")
    release = stage_root / "release-cli"
    cli = stage_root / "cli.sh"
    cli.write_text(
        "#!/usr/bin/env bash\n"
        f"while [ ! -f '{release}' ]; do sleep 0.2; done\n"
        "printf 'PLAN-DONE\\n'\n"
        "exit 0\n",
        encoding="utf-8",
    )
    cli.chmod(0o755)
    runner_log = stage_root / "runner.log"

    # The exact recipe from dispatch-recipes.md (macOS has no setsid).
    recipe = (
        f"nohup bash '{RUNNER}' --line-id '{line}' --run-id '{run}' --stage plan "
        f"--registry '{reg}' --worktree '{project}' --prompt '{paths['prompt']}' "
        f"--pid-file '{paths['pid']}' --status-file '{paths['status']}' "
        f"--log '{paths['log']}' --heartbeat '{paths['heartbeat']}' "
        f"--sentinel PLAN-DONE --engine '{SKILL_DIR / 'scripts' / 'line-registry.py'}' "
        f"--engine-python '{os.sys.executable}' "
        f"--command \"bash '{cli}'\" > '{runner_log}' 2>&1 < /dev/null & disown; "
        "sleep 60"
    )
    driver = subprocess.Popen(
        ["bash", "-c", recipe], cwd=str(project),
        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        start_new_session=True,
    )

    def entry() -> dict:
        path = reg / f"{line}.json"
        return json.loads(path.read_text()) if path.exists() else {}

    try:
        assert wait_until(
            lambda: entry().get("runner_pid") and entry().get("cli_pid"), timeout=10
        ), entry()
        launched = entry()
        runner_pid, cli_pid = launched["runner_pid"], launched["cli_pid"]
        assert pid_alive(runner_pid) and pid_alive(cli_pid)
        assert paths["pid"].read_text().split()[0] == f"pid={cli_pid}"

        engine_json(
            "reserve", "--line-id", line, "--stage", "plan",
            "--run-id", run, "--pid", str(runner_pid),
            "--start-token", process_token(runner_pid), reg=reg,
        )

        os.killpg(os.getpgid(driver.pid), signal.SIGHUP)
        try:
            driver.wait(timeout=10)
        except subprocess.TimeoutExpired:
            # SIGHUP delivery can be delayed under full-suite load; killing the
            # driver explicitly preserves the test's intent (the detached runner
            # must survive driver death and be reattachable).
            driver.kill()
            driver.wait(timeout=5)
        time.sleep(0.4)
        assert pid_alive(runner_pid), "detached runner must survive the driver group SIGHUP"
        assert pid_alive(cli_pid), "CLI child must survive the driver group SIGHUP"
        before = paths["heartbeat"].stat().st_mtime_ns
        assert wait_until(lambda: paths["heartbeat"].stat().st_mtime_ns > before, timeout=3), (
            "heartbeat stopped after the driver kill"
        )

        # New session reattaches through the registry + state spine only.
        engine_json(
            "lease-acquire", "--line-id", line, "--session", "new",
            "--pid", str(os.getpid()), reg=reg,
        )
        identity = engine_json("verify-identity", "--line-id", line, reg=reg)
        assert identity["identity"] == "ok", identity
        assert identity["branch_hint"] == "running"
        ctx = {"line": line, "run": run, "reg": reg, "stage": {"paths": paths}}
        running = _watch(ctx)
        assert running.returncode == 10 and "verdict=RUNNING" in running.stdout, running.stdout

        attach = engine_json(
            "reserve", "--line-id", line, "--stage", "plan",
            "--run-id", run, "--pid", str(runner_pid),
            "--start-token", process_token(runner_pid), reg=reg,
        )
        assert attach["action"] == "attach", "reattach must not launch a second stage"
        assert not paths["status"].exists() or "exit=" not in paths["status"].read_text()

        release.write_text("go", encoding="utf-8")
        assert wait_until(lambda: "exit=" in snapshot(paths["status"]), timeout=20)
        done = _watch(ctx)
        assert done.returncode == 0 and "verdict=DONE" in done.stdout, done.stdout
        after = entry()
        assert after["runner_pid"] == runner_pid and after["cli_pid"] == cli_pid, (
            "reattachment must not re-dispatch the stage"
        )
        assert paths["log"].read_text().splitlines()[-1] == "PLAN-DONE"
    finally:
        for pid in (locals().get("cli_pid"), locals().get("runner_pid")):
            if pid:
                try:
                    os.kill(pid, signal.SIGTERM)
                except OSError:
                    pass
        driver.kill()
        driver.wait(timeout=3)


def test_run_stage_requires_the_engine(tmp_path):
    """Without --engine the runner could start an untracked stage; refuse."""
    project = make_project(tmp_path)
    proc = subprocess.run(
        ["bash", str(RUNNER), "--line-id", make_line_id("noengine"), "--run-id", make_run_id(),
         "--stage", "plan", "--registry", str(tmp_path / "reg"), "--worktree", str(project),
         "--pid-file", str(tmp_path / "pid"), "--status-file", str(tmp_path / "status"),
         "--log", str(tmp_path / "log"), "--heartbeat", str(tmp_path / "hb"),
         "--command", "true"],
        capture_output=True, text=True, timeout=10,
    )
    assert proc.returncode == 2
    assert "--engine" in proc.stderr


def test_run_stage_fails_loud_when_registry_update_fails(tmp_path):
    """An untracked stage is never left running: registry projection failure
    writes ANOMALY + exit=4 and terminates the CLI child."""
    project = make_project(tmp_path)
    stage_root = tmp_path / "stage-fail"
    stage_root.mkdir()
    paths = {
        "pid": stage_root / "pid",
        "status": stage_root / "status",
        "log": stage_root / "log",
        "heartbeat": stage_root / "hb",
    }
    broken_engine = stage_root / "broken-engine.py"
    broken_engine.write_text("import sys; sys.exit(1)\n", encoding="utf-8")
    cli = stage_root / "cli.sh"
    cli.write_text("#!/usr/bin/env bash\nsleep 30\n", encoding="utf-8")
    cli.chmod(0o755)
    proc = subprocess.run(
        ["bash", str(RUNNER), "--line-id", make_line_id("failing"), "--run-id", make_run_id(),
         "--stage", "plan", "--registry", str(tmp_path / "reg"), "--worktree", str(project),
         "--pid-file", str(paths["pid"]), "--status-file", str(paths["status"]),
         "--log", str(paths["log"]), "--heartbeat", str(paths["heartbeat"]),
         "--engine", str(broken_engine), "--engine-python", sys.executable,
         "--command", f"bash '{cli}'"],
        capture_output=True, text=True, timeout=30,
    )
    assert proc.returncode == 4, proc.stderr
    status = paths["status"].read_text()
    assert "exit=4" in status and "sentinel=0" in status
    assert "ANOMALY: registry-update-failed" in paths["log"].read_text()
    cli_pid = int(paths["pid"].read_text().split()[0].split("=")[1])
    assert wait_until(lambda: not pid_alive(cli_pid), timeout=3), "CLI must not outlive a failed projection"


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
