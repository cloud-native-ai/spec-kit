"""Contract tests for contracts/lifecycle-detach-reattach.md (LC-01…LC-18)."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pytest

from fixtures.line_fixtures import (
    engine_path,
    four_piece,
    make_line_id,
    make_project,
    make_run_id,
    run_engine,
    engine_json,
    write_status,
)

SKILL_DIR = Path(__file__).resolve().parents[2] / "skills" / "external" / "sdd-loop-driver"


def _token(pid: int) -> str:
    proc_path = Path(f"/proc/{pid}/stat")
    if proc_path.exists():
        return proc_path.read_text().split()[21]
    proc = subprocess.run(["ps", "-p", str(pid), "-o", "lstart="], capture_output=True, text=True)
    return " ".join(proc.stdout.split())


def _register(reg: Path, project: Path, line: str | None = None, run: str | None = None, **extra) -> dict:
    line = line or make_line_id()
    run = run or make_run_id()
    args = [
        "--line-id", line, "--run-id", run,
        "--project-dir", str(project), "--repo-root", str(project), "--state", "active",
    ]
    for flag, value in extra.items():
        args += [f"--{flag.replace('_', '-')}", str(value)]
    return engine_json("register", *args, reg=reg)


def _old_iso(seconds: int = 7200) -> str:
    return datetime.fromtimestamp(time.time() - seconds, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _write_lease(reg: Path, line: str, holder_pid: int, token: str, heartbeat_age: int, ttl: int = 600) -> Path:
    path = reg / f"{line}.driver.lock"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "line_id": line,
        "holder_session": "old-session",
        "holder_pid": holder_pid,
        "holder_start_token": token,
        "host": os.uname().nodename,
        "acquired_at": _old_iso(heartbeat_age + 60),
        "heartbeat_at": _old_iso(heartbeat_age),
        "ttl_seconds": ttl,
    }), encoding="utf-8")
    return path


def _docs() -> str:
    return "\n".join(
        (SKILL_DIR / rel).read_text(encoding="utf-8")
        for rel in [
            "SKILL.md",
            "references/dispatch-recipes.md",
            "references/stage-prompts.md",
            "references/watch-model.md",
        ]
    )


def test_lc_01_02_detached_process_group_documented(tmp_path):
    text = _docs()
    for needle in ["setsid", "nohup", "disown", "stdio", "/dev/null"]:
        assert needle in text, f"detach literal missing: {needle}"
    assert "主会话" in text and ("MUST NOT" in text or "不得" in text)


def test_lc_03_four_piece_and_cli_pid(tmp_path):
    text = _docs()
    assert "cli_pid" in text
    assert "start token" in text or "start_token" in text or "start ticks" in text
    assert "wait" in text
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    entry = _register(reg, project)
    four = four_piece(tmp_path / "rt", entry["line_id"], entry["run_id"], stage="plan")
    updated = engine_json(
        "update", "--line-id", entry["line_id"], "--stage", "plan",
        "--runner-pid", str(os.getpid()), "--runner-start-token", _token(os.getpid()),
        "--cli-pid", str(os.getpid()), "--cli-start-token", _token(os.getpid()),
        "--prompt-path", str(four["prompt_meta"]),
        "--status-path", str(four["status"]), "--log-path", str(four["log"]),
        "--heartbeat-path", str(four["heartbeat"]),
        "--last-event", "u2-dispatch", reg=reg,
    )
    assert updated["runner_pid"] == os.getpid()
    assert updated["cli_pid"] == os.getpid()


def test_lc_04_reservation_exclusive(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    entry = _register(reg, project)
    first = engine_json(
        "reserve", "--line-id", entry["line_id"], "--stage", "plan",
        "--run-id", entry["run_id"], "--pid", str(os.getpid()),
        "--start-token", _token(os.getpid()), reg=reg,
    )
    assert first["action"] == "created"
    same = engine_json(
        "reserve", "--line-id", entry["line_id"], "--stage", "plan",
        "--run-id", entry["run_id"], "--pid", str(os.getpid()),
        "--start-token", _token(os.getpid()), reg=reg,
    )
    assert same["action"] == "attach"
    refused = run_engine(
        "reserve", "--line-id", entry["line_id"], "--stage", "plan",
        "--run-id", make_run_id(), "--pid", str(os.getpid()),
        "--start-token", _token(os.getpid()), reg=reg,
    )
    assert refused.returncode == 3


def test_lc_04_reservation_concurrent_single_winner(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    entry = _register(reg, project)
    token = _token(os.getpid())
    env = dict(os.environ, SPECIFY_LINE_REGISTRY_DIR=str(reg))
    procs = []
    for index in range(6):
        procs.append(subprocess.Popen(
            [sys.executable, str(engine_path()), "--action", "reserve",
             "--line-id", entry["line_id"], "--stage", "plan",
             "--run-id", make_run_id(f"{index:04x}"),
             "--pid", str(os.getpid()), "--start-token", token],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env,
        ))
    results = []
    for proc in procs:
        out, err = proc.communicate(timeout=20)
        results.append((proc.returncode, out, err))
    winners = [row for row in results if row[0] == 0]
    refused = [row for row in results if row[0] == 3]
    assert len(winners) == 1, results
    assert len(refused) == 5, results
    stored = json.loads((reg / "reservations" / f"{entry['line_id']}.plan.json").read_text())
    assert stored["line_id"] == entry["line_id"]


def test_lc_05_live_lease_refused_and_cadence(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    entry = _register(reg, project)
    lease = engine_json(
        "lease-acquire", "--line-id", entry["line_id"], "--session", "s1",
        "--pid", str(os.getpid()), "--ttl", "600", reg=reg,
    )
    assert lease["holder_session"] == "s1"
    assert lease["ttl_seconds"] == 600
    refused = run_engine(
        "lease-acquire", "--line-id", entry["line_id"], "--session", "s2",
        "--pid", str(os.getpid()), reg=reg,
    )
    assert refused.returncode == 3
    payload = json.loads(refused.stdout)
    assert payload["holder_state"] == "live"
    renew = engine_json(
        "lease-renew", "--line-id", entry["line_id"], "--session", "s1", reg=reg
    )
    assert renew["max_interval_seconds"] == 200
    assert renew["cadence_ok"] is True
    wrong = run_engine(
        "lease-renew", "--line-id", entry["line_id"], "--session", "s2", reg=reg
    )
    assert wrong.returncode == 3


def test_lc_06_expired_and_suspected_alive_break(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    dead = _register(reg, project)
    _write_lease(reg, dead["line_id"], 999999, "0", heartbeat_age=7200)
    refused = run_engine(
        "lease-acquire", "--line-id", dead["line_id"], "--session", "s2",
        "--pid", str(os.getpid()), reg=reg,
    )
    assert refused.returncode == 3
    assert json.loads(refused.stdout)["holder_state"] == "expired"
    broken = engine_json(
        "lease-break", "--line-id", dead["line_id"], "--reason", "holder-dead",
        "--evidence-ref", "notes/evidence.md", reg=reg,
    )
    assert broken["broken"] is True
    assert (reg / f"{dead['line_id']}.lease-history.jsonl").exists()

    alive = _register(reg, project)
    _write_lease(reg, alive["line_id"], os.getpid(), _token(os.getpid()), heartbeat_age=7200)
    suspected = run_engine(
        "lease-acquire", "--line-id", alive["line_id"], "--session", "s2",
        "--pid", str(os.getpid()), reg=reg,
    )
    assert suspected.returncode == 3
    assert json.loads(suspected.stdout)["holder_state"] == "suspected-alive"
    without = run_engine(
        "lease-break", "--line-id", alive["line_id"], "--reason", "stale",
        "--evidence-ref", "notes/evidence.md", reg=reg,
    )
    assert without.returncode == 3
    forced = engine_json(
        "lease-break", "--line-id", alive["line_id"], "--reason", "stale",
        "--evidence-ref", "notes/evidence.md", "--override", reg=reg,
    )
    assert forced["override"] is True
    history = (reg / f"{alive['line_id']}.lease-history.jsonl").read_text().splitlines()
    assert any("suspected-alive" in row for row in history)


def test_lc_07_identity_ok_mismatch_dead(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    entry = _register(reg, project)
    four = four_piece(tmp_path / "rt", entry["line_id"], entry["run_id"], stage="plan")
    engine_json(
        "update", "--line-id", entry["line_id"], "--stage", "plan",
        "--runner-pid", str(os.getpid()), "--runner-start-token", _token(os.getpid()),
        "--cli-pid", str(os.getpid()), "--cli-start-token", _token(os.getpid()),
        "--prompt-path", str(four["prompt_meta"]), "--status-path", str(four["status"]),
        "--log-path", str(four["log"]), "--heartbeat-path", str(four["heartbeat"]), reg=reg,
    )
    ok = engine_json("verify-identity", "--line-id", entry["line_id"], reg=reg)
    assert ok["identity"] == "ok"
    assert ok["cwd_check"] in {"ok", "unsupported"}
    engine_json(
        "update", "--line-id", entry["line_id"], "--runner-start-token", "wrong", reg=reg
    )
    mismatch = engine_json("verify-identity", "--line-id", entry["line_id"], reg=reg)
    assert mismatch["identity"] == "mismatch"
    engine_json(
        "update", "--line-id", entry["line_id"], "--runner-pid", "999999",
        "--runner-start-token", "0", reg=reg,
    )
    dead = engine_json("verify-identity", "--line-id", entry["line_id"], reg=reg)
    assert dead["identity"] == "dead"


def test_lc_08_snapshot_before_decision(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    entry = _register(reg, project)
    four = four_piece(tmp_path / "rt", entry["line_id"], entry["run_id"], stage="plan", sentinel=True)
    engine_json(
        "update", "--line-id", entry["line_id"], "--stage", "plan",
        "--runner-pid", "999999", "--runner-start-token", "0",
        "--cli-pid", "999999", "--cli-start-token", "0",
        "--prompt-path", str(four["prompt_meta"]), "--status-path", str(four["status"]),
        "--log-path", str(four["log"]), "--heartbeat-path", str(four["heartbeat"]), reg=reg,
    )
    brief = engine_json("reattach-brief", "--line-id", entry["line_id"], reg=reg)
    assert brief["snapshot_required"] is True
    assert brief["evidence"]["status"]["sentinel"] == 1
    assert brief["branch_hint"] in {"done", "dead"}
    text = _docs()
    assert "--once" in text and "先" in text


def test_lc_09_remote_unreachable_not_dead(tmp_path):
    probe = tmp_path / "probe.json"
    probe.write_text(json.dumps({"unreachable": True, "reason": "ssh 255"}), encoding="utf-8")
    classified = engine_json("classify-remote", "--probe-json", str(probe), reg=tmp_path / "reg")
    assert classified["identity"] == "remote-unreachable"
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    entry = _register(reg, project)
    identity = engine_json(
        "verify-identity", "--line-id", entry["line_id"], "--probe-json", str(probe), reg=reg
    )
    assert identity["identity"] == "remote-unreachable"


def test_lc_10_11_12_snapshot_branches(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    line = _register(reg, project)
    four = four_piece(tmp_path / "rt", line["line_id"], line["run_id"], stage="plan", sentinel=True)
    engine_json(
        "update", "--line-id", line["line_id"], "--stage", "plan",
        "--runner-pid", "999999", "--runner-start-token", "0",
        "--cli-pid", "999999", "--cli-start-token", "0",
        "--prompt-path", str(four["prompt_meta"]), "--status-path", str(four["status"]),
        "--log-path", str(four["log"]), "--heartbeat-path", str(four["heartbeat"]), reg=reg,
    )
    done = engine_json("verify-identity", "--line-id", line["line_id"], reg=reg)
    assert done["branch_hint"] == "done"

    running_line = _register(reg, project)
    four2 = four_piece(tmp_path / "rt2", running_line["line_id"], running_line["run_id"], stage="plan")
    engine_json(
        "update", "--line-id", running_line["line_id"], "--stage", "plan",
        "--runner-pid", str(os.getpid()), "--runner-start-token", _token(os.getpid()),
        "--cli-pid", str(os.getpid()), "--cli-start-token", _token(os.getpid()),
        "--prompt-path", str(four2["prompt_meta"]), "--status-path", str(four2["status"]),
        "--log-path", str(four2["log"]), "--heartbeat-path", str(four2["heartbeat"]), reg=reg,
    )
    running = engine_json("verify-identity", "--line-id", running_line["line_id"], reg=reg)
    assert running["identity"] == "ok"
    assert running["branch_hint"] == "running"


def test_lc_13_orphan_check_uses_line_evidence(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    entry = _register(reg, project)
    orphan = engine_json("orphan-check", "--line-id", make_line_id("ghost"), reg=reg)
    assert orphan["orphaned"] is True
    healthy = engine_json("orphan-check", "--line-id", entry["line_id"], reg=reg)
    assert healthy["orphaned"] is False
    source = (SKILL_DIR / "scripts" / "line-registry.py").read_text(encoding="utf-8")
    start = source.find("def action_orphan_check")
    body = source[start:source.find("\ndef ", start + 10)]
    assert "pgrep" not in body and "ps -" not in body


def test_lc_14_stale_explicit(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    entry = _register(reg, project)
    engine_json("update", "--line-id", entry["line_id"], "--runner-pid", "999999",
                "--runner-start-token", "0", reg=reg)
    identity = engine_json("verify-identity", "--line-id", entry["line_id"], reg=reg)
    assert identity["identity"] == "dead"
    closed = engine_json("deregister", "--line-id", entry["line_id"], "--reason", "stale-cleanup", reg=reg)
    assert closed["state"] == "closed"


def test_lc_15_second_start_attach_or_refuse(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    entry = _register(reg, project)
    engine_json(
        "reserve", "--line-id", entry["line_id"], "--stage", "plan",
        "--run-id", entry["run_id"], "--pid", str(os.getpid()),
        "--start-token", _token(os.getpid()), reg=reg,
    )
    attach = engine_json(
        "reserve", "--line-id", entry["line_id"], "--stage", "plan",
        "--run-id", entry["run_id"], "--pid", str(os.getpid()),
        "--start-token", _token(os.getpid()), reg=reg,
    )
    assert attach["action"] == "attach"
    refused = run_engine(
        "reserve", "--line-id", entry["line_id"], "--stage", "plan",
        "--run-id", make_run_id(), "--pid", str(os.getpid()),
        "--start-token", _token(os.getpid()), reg=reg,
    )
    assert refused.returncode == 3


def test_lc_16_u6_no_active_residue(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    entry = _register(reg, project)
    engine_json(
        "reserve", "--line-id", entry["line_id"], "--stage", "plan",
        "--run-id", entry["run_id"], "--pid", str(os.getpid()),
        "--start-token", _token(os.getpid()), reg=reg,
    )
    engine_json(
        "lease-acquire", "--line-id", entry["line_id"], "--session", "s1",
        "--pid", str(os.getpid()), reg=reg,
    )
    engine_json("update", "--line-id", entry["line_id"], "--state", "completed", reg=reg)
    engine_json(
        "integration-record", "--line-id", entry["line_id"], "--result", "merged",
        "--commit", "deadbeef", reg=reg,
    )
    closed = engine_json("deregister", "--line-id", entry["line_id"], "--reason", "merged", reg=reg)
    assert closed["state"] == "closed" and closed["closed_at"]
    assert not (reg / f"{entry['line_id']}.driver.lock").exists()
    assert not list((reg / "reservations").glob(f"{entry['line_id']}.*.json"))
    active = engine_json("list", "--active", reg=reg)
    assert active == []


def test_lc_17_remote_fields_isomorphic(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    remote = {"alias": "host", "run_user": "dev", "remote_root": "/srv/p"}
    entry = _register(reg, project, remote=json.dumps(remote))
    assert entry["remote"] == remote
    lease = engine_json(
        "lease-acquire", "--line-id", entry["line_id"], "--session", "s1",
        "--pid", str(os.getpid()), reg=reg,
    )
    assert lease["host"] == os.uname().nodename
    reserve = engine_json(
        "reserve", "--line-id", entry["line_id"], "--stage", "plan",
        "--run-id", entry["run_id"], "--pid", str(os.getpid()),
        "--start-token", _token(os.getpid()), reg=reg,
    )
    assert reserve["reservation"]["host"] == os.uname().nodename


def test_lc_18_kill_reattach_delegate():
    integration = (
        Path(__file__).resolve().parents[1] / "integration" / "test_session_kill_reattach.py"
    )
    text = integration.read_text(encoding="utf-8")
    for needle in ["SIGHUP", "survive", "reattach", "reservation", "remote-unreachable"]:
        assert needle in text
