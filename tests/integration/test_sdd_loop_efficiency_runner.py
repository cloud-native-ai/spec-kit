"""Integration tests for skills/external/sdd-loop-driver/scripts/stage-runner.sh.

Red-first: the runner does not exist yet. It runs the stage CLI under the
stream-json pipeline (raw + derived live log), keeps the four-piece evidence
set, records degradation without faking completion, and survives the parent
shell exit when launched under nohup.
"""

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RUNNER = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "stage-runner.sh"
WATCH = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "watch-target.sh"
STUB = REPO_ROOT / "tests" / "fixtures" / "sdd_loop_efficiency" / "stub-cli.sh"

DERIVED = re.compile(r"\[evt=(\d+) at=([0-9]+(?:\.[0-9]+)?)\]")


def _status(state_dir, line="demo", stage="plan"):
    path = Path(state_dir) / ("status-%s-%s" % (line, stage))
    values = {}
    if not path.exists():
        return values
    for field in path.read_text(encoding="utf-8").split():
        if "=" in field:
            key, value = field.split("=", 1)
            values[key] = value
    return values


def _runner(state_dir, cli_args="", mode="stream", detached="yes",
            line="demo", stage="plan", sentinel="PLAN-DONE", cli=STUB):
    args = ["bash", str(RUNNER),
            "--cli", str(cli), "--cli-args", cli_args,
            "--project-dir", str(state_dir), "--prompt-file", "/dev/null",
            "--sentinel", sentinel, "--line", line, "--stage", stage,
            "--state-dir", str(state_dir), "--mode", mode,
            "--detached", detached]
    completed = subprocess.run(args, capture_output=True, text=True, timeout=120)
    return completed, _status(state_dir, line, stage)


def _last_nonempty(path):
    p = Path(path)
    if not p.exists():
        return ""
    lines = [line for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]
    return lines[-1] if lines else ""


def test_stream_mode_writes_raw_and_live(tmp_path):
    completed, status = _runner(tmp_path)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    raw = tmp_path / "raw-demo-plan.jsonl"
    live = tmp_path / "log-demo-plan.log"
    assert raw.exists() and live.exists()
    assert len([line for line in raw.read_text(encoding="utf-8").splitlines() if line]) == 4
    assert _last_nonempty(live) == "PLAN-DONE"
    assert status.get("exit") == "0"
    assert status.get("sentinel") == "1"
    assert status.get("progress") == "stream"
    assert status.get("detached") == "yes"


def test_auto_selects_stream_when_cli_advertises_capability(tmp_path):
    shim = tmp_path / "stream-capable-cli.sh"
    shim.write_text(
        "#!/usr/bin/env bash\n"
        "if [ \"${1:-}\" = \"--help\" ]; then\n"
        "  printf 'Usage: cli [--output-format FORMAT]\\n'\n"
        "  exit 0\n"
        "fi\n"
        "exec bash %s \"$@\"\n" % STUB,
        encoding="utf-8")
    shim.chmod(0o755)
    completed, status = _runner(tmp_path, mode="auto", cli=shim)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert status.get("progress") == "stream"
    assert (tmp_path / "raw-demo-plan.jsonl").exists()
    assert status.get("sentinel") == "1"


def test_buffered_degradation_when_cli_lacks_stream(tmp_path):
    completed, status = _runner(tmp_path, cli_args="--mode no-stream", mode="auto")
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert status.get("progress") == "degraded"
    assert "cli-lacks-stream" in status.get("reason", "")
    assert status.get("sentinel") == "1"
    assert _last_nonempty(tmp_path / "log-demo-plan.log") == "PLAN-DONE"
    raw = tmp_path / "raw-demo-plan.jsonl"
    assert not raw.exists() or raw.read_text(encoding="utf-8").strip() == ""


def test_status_fields_and_exit_code_propagation(tmp_path):
    completed, status = _runner(tmp_path, cli_args="--mode fail")
    assert completed.returncode == 7, completed.stdout + completed.stderr
    assert status.get("exit") == "7"
    assert status.get("sentinel") == "0"
    assert status.get("progress") == "stream"
    assert status.get("detached") == "yes"


def test_local_nohup_survives_parent_exit(tmp_path):
    state = tmp_path / "state"
    state.mkdir()
    command = (
        "nohup bash %s --cli %s --cli-args \"--delay 2\" "
        "--project-dir %s --prompt-file /dev/null --sentinel PLAN-DONE "
        "--line demo --stage plan --state-dir %s --mode stream --detached yes "
        "</dev/null >%s 2>&1 & echo $! >%s"
    ) % (RUNNER, STUB, state, state, state / "runner-log-demo-plan.log",
         state / "runner.pid")
    parent = subprocess.run(["bash", "-c", command], capture_output=True, text=True,
                            timeout=30)
    assert parent.returncode == 0, parent.stderr
    status_path = state / "status-demo-plan"
    deadline = time.time() + 30
    while time.time() < deadline and not status_path.exists():
        time.sleep(0.2)
    assert status_path.exists(), "detached runner did not finish after parent exit"
    status = _status(state)
    assert status.get("exit") == "0"
    assert status.get("sentinel") == "1"
    assert _last_nonempty(state / "log-demo-plan.log") == "PLAN-DONE"


def test_once_snapshot_does_not_redispatch(tmp_path):
    completed, _ = _runner(tmp_path)
    assert completed.returncode == 0
    status_path = tmp_path / "status-demo-plan"
    before_mtime = status_path.stat().st_mtime_ns
    before_raw = (tmp_path / "raw-demo-plan.jsonl").read_text(encoding="utf-8")
    watch = subprocess.run(
        ["bash", str(WATCH), "--label", "demo",
         "--pid-file", str(tmp_path / "pid-demo-plan"),
         "--status-file", str(status_path),
         "--log", str(tmp_path / "log-demo-plan.log"),
         "--sentinel", "PLAN-DONE", "--once", "--start-grace", "0"],
        capture_output=True, text=True, timeout=30,
    )
    assert watch.returncode == 0, watch.stdout + watch.stderr
    assert "verdict=DONE" in watch.stdout
    assert status_path.stat().st_mtime_ns == before_mtime
    assert (tmp_path / "raw-demo-plan.jsonl").read_text(encoding="utf-8") == before_raw


def test_detached_no_marks_unprotected(tmp_path):
    completed, status = _runner(tmp_path, detached="no")
    assert completed.returncode == 0
    assert status.get("detached") == "no"
    assert status.get("unprotected") == "true"
    assert "unprotected_reason" in status


def test_raw_receive_timestamps_pair_with_live_lines(tmp_path):
    completed, _ = _runner(tmp_path)
    assert completed.returncode == 0
    sidecar = tmp_path / "raw-demo-plan.ts.jsonl"
    assert sidecar.exists(), "raw receive timestamps sidecar missing"
    stamps = {}
    for line in sidecar.read_text(encoding="utf-8").splitlines():
        if line.strip():
            item = json.loads(line)
            stamps[int(item["seq"])] = float(item["at"])
    assert stamps, "no receive timestamps recorded"
    live = (tmp_path / "log-demo-plan.log").read_text(encoding="utf-8")
    paired = 0
    for line in live.splitlines():
        match = DERIVED.search(line)
        if not match:
            continue
        seq = int(match.group(1))
        derived_at = float(match.group(2))
        assert seq in stamps, "live line has no raw receive timestamp: %s" % line
        assert derived_at >= stamps[seq] - 5
        assert derived_at - stamps[seq] <= 120
        paired += 1
    assert paired >= 3
