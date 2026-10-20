"""Contract tests for contracts/line-registry.md (LR-01…LR-13)."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

from fixtures.line_fixtures import (
    base_env,
    engine_json,
    engine_path,
    make_git_repo,
    make_line_id,
    make_project,
    make_run_id,
    run_engine,
)


def _register(reg: Path, project: Path, **overrides) -> dict:
    args = [
        "--line-id", overrides.pop("line_id", make_line_id()),
        "--run-id", overrides.pop("run_id", make_run_id()),
        "--project-dir", str(overrides.pop("project_dir", project)),
        "--repo-root", str(overrides.pop("repo_root", project)),
        "--state", overrides.pop("state", "active"),
    ]
    for flag, value in overrides.items():
        args += [f"--{flag.replace('_', '-')}", str(value)]
    return engine_json("register", *args, reg=reg)


def test_lr_01_location_override(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "line-registry"
    entry = _register(reg, project)
    assert (reg / f"{entry['line_id']}.json").exists()
    assert reg.resolve() != project.resolve()
    assert str(reg) not in entry["project_dir"]


def test_lr_02_register_deregister(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    entry = _register(reg, project)
    assert entry["state"] == "active"
    closed = engine_json("deregister", "--line-id", entry["line_id"], "--reason", "u6-closed", reg=reg)
    assert closed["state"] == "closed"
    assert closed["closed_at"]
    active = engine_json("list", "--active", reg=reg)
    assert entry["line_id"] not in [row["line_id"] for row in active]
    everything = engine_json("list", "--all", reg=reg)
    assert [row["line_id"] for row in everything] == [entry["line_id"]]


def test_lr_03_atomic_replace(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    entry = _register(reg, project)
    for i in range(10):
        proc = run_engine(
            "update", "--line-id", entry["line_id"], "--last-event", f"event-{i}", reg=reg
        )
        assert proc.returncode == 0, proc.stderr
    stored = json.loads((reg / f"{entry['line_id']}.json").read_text())
    assert stored["last_event"] == "event-9"
    assert not list(reg.glob("*.tmp*")), "atomic write left a temp file"


def test_lr_04_same_line_lock_serializes_updates(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    entry = _register(reg, project)
    env = base_env(reg)
    procs = []
    for i in range(8):
        procs.append(subprocess.Popen(
            [sys.executable, str(engine_path()), "--action", "update",
             "--line-id", entry["line_id"], "--last-event", f"parallel-{i}"],
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, env=env,
        ))
    for proc in procs:
        proc.wait(timeout=20)
        assert proc.returncode == 0, proc.stderr.read()
    stored = json.loads((reg / f"{entry['line_id']}.json").read_text())
    assert stored["line_id"] == entry["line_id"]
    assert stored["last_event"].startswith("parallel-")


def test_lr_05_list_active_and_all(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    active = _register(reg, project)
    waiting = _register(
        reg, project, state="waiting", waiting_reason="concurrency-cap", queued_at="2026-10-20T00:00:00Z"
    )
    closed = _register(reg, project)
    engine_json("deregister", "--line-id", closed["line_id"], "--reason", "done", reg=reg)
    rows = engine_json("list", "--active", reg=reg)
    ids = [row["line_id"] for row in rows]
    assert active["line_id"] in ids and waiting["line_id"] in ids
    assert closed["line_id"] not in ids
    for row in rows:
        assert set(row) >= {"line_id", "run_id", "project_dir", "branch", "stage", "state", "updated_at"}


def test_lr_06_id_formats_and_run_history(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    bad = run_engine(
        "register", "--line-id", "Bad_ID", "--run-id", make_run_id(),
        "--project-dir", str(project), "--repo-root", str(project), reg=reg,
    )
    assert bad.returncode == 2
    entry = _register(reg, project)
    new_run = make_run_id("ffff", offset=5)
    updated = engine_json("update", "--line-id", entry["line_id"], "--run-id", new_run, reg=reg)
    assert updated["run_id"] == new_run
    assert updated["run_history"][0]["run_id"] == entry["run_id"]
    assert updated["run_history"][0]["outcome"] == "superseded"


def test_lr_07_required_fields(tmp_path):
    reg = tmp_path / "reg"
    missing = run_engine("register", "--line-id", make_line_id(), "--run-id", make_run_id(), reg=reg)
    assert missing.returncode == 2
    project = make_project(tmp_path)
    waiting = run_engine(
        "register", "--line-id", make_line_id("wait", "b2c3"), "--run-id", make_run_id("b2c3"),
        "--project-dir", str(project), "--repo-root", str(project), "--state", "waiting", reg=reg,
    )
    assert waiting.returncode == 2
    entry = _register(reg, project)
    pid_only = run_engine(
        "update", "--line-id", entry["line_id"], "--runner-pid", str(os.getpid()), reg=reg,
        env=dict(base_env(reg), SPECIFY_LINE_RUNTIME_DIR=str(tmp_path / "nope")),
    )
    # Without a token the engine derives one from the live PID; with no stage the
    # entry stays valid. The token must nevertheless be present.
    stored = json.loads((reg / f"{entry['line_id']}.json").read_text())
    assert stored.get("runner_start_token")


def test_lr_08_remote_minimal_fields(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    bad = run_engine(
        "register", "--line-id", make_line_id("rem", "c1d2"), "--run-id", make_run_id("c1d2"),
        "--project-dir", str(project), "--repo-root", str(project),
        "--remote", json.dumps({"alias": "host"}), reg=reg,
    )
    assert bad.returncode == 2
    entry = engine_json(
        "register", "--line-id", make_line_id("rem", "c1d2"), "--run-id", make_run_id("c1d2"),
        "--project-dir", str(project), "--repo-root", str(project),
        "--remote", json.dumps({"alias": "host", "run_user": "dev", "remote_root": "/srv/p"}),
        reg=reg,
    )
    assert entry["remote"]["run_user"] == "dev"


def test_lr_09_state_enum_and_spine_consistency(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    entry = _register(reg, project)
    bad = run_engine("update", "--line-id", entry["line_id"], "--state", "sleeping", reg=reg)
    assert bad.returncode == 2
    spine = tmp_path / "spine.md"
    spine.write_text("state: done\n", encoding="utf-8")
    ok = run_engine(
        "update", "--line-id", entry["line_id"], "--state", "completed", "--spine", str(spine), reg=reg
    )
    assert ok.returncode == 0, ok.stderr
    spine.write_text("state: running\n", encoding="utf-8")
    conflict = run_engine(
        "update", "--line-id", entry["line_id"], "--last-event", "u4", "--spine", str(spine), reg=reg
    )
    assert conflict.returncode == 2


def test_lr_10_stale_detection_explicit_cleanup(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    entry = _register(reg, project)
    other = _register(reg, project)
    dead = 999999
    engine_json(
        "update", "--line-id", entry["line_id"], "--runner-pid", str(dead),
        "--runner-start-token", "0", "--last-event", "u2-dispatch", reg=reg,
    )
    identity = engine_json("verify-identity", "--line-id", entry["line_id"], reg=reg)
    assert identity["identity"] == "dead"
    closed = engine_json(
        "deregister", "--line-id", entry["line_id"], "--reason", "stale-cleanup", reg=reg
    )
    assert closed["state"] == "closed"
    assert closed["last_event"] == "stale-cleanup"
    survivor = json.loads((reg / f"{other['line_id']}.json").read_text())
    assert survivor["state"] == "active"
    assert survivor["line_id"] == other["line_id"]


def test_lr_11_unwritable_fails_start(tmp_path):
    project = make_project(tmp_path)
    blocker = tmp_path / "not-a-dir"
    blocker.write_text("x", encoding="utf-8")
    proc = run_engine(
        "register", "--line-id", make_line_id("bad", "e5f6"), "--run-id", make_run_id("e5f6"),
        "--project-dir", str(project), "--repo-root", str(project),
        env=dict(os.environ, SPECIFY_LINE_REGISTRY_DIR=str(blocker)),
    )
    assert proc.returncode == 6
    assert "registry" in proc.stdout.lower() or "registry" in proc.stderr.lower()


def test_lr_12_concurrent_registration(tmp_path):
    """N=12 writers with an interleaved reader (SC-009: no half-write/missing entry)."""
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    env = base_env(reg)
    count = 12
    read_errors = []
    stop = threading.Event()

    def reader():
        while not stop.is_set():
            proc = run_engine("list", "--all", reg=reg)
            if proc.returncode != 0:
                read_errors.append(proc.stderr)
                continue
            try:
                json.loads(proc.stdout)
            except json.JSONDecodeError:
                read_errors.append(proc.stdout)

    reader_thread = threading.Thread(target=reader, daemon=True)
    reader_thread.start()
    procs = []
    for i in range(count):
        line = make_line_id("conc", f"{i:04x}")
        run = make_run_id(f"{i:04x}")
        procs.append(subprocess.Popen(
            [sys.executable, str(engine_path()), "--action", "register",
             "--line-id", line, "--run-id", run,
             "--project-dir", str(project), "--repo-root", str(project)],
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, env=env,
        ))
    for proc in procs:
        proc.wait(timeout=30)
        assert proc.returncode == 0, proc.stderr.read()
    stop.set()
    reader_thread.join(timeout=10)
    assert read_errors == [], read_errors
    rows = engine_json("list", "--all", reg=reg)
    ids = [row["line_id"] for row in rows]
    assert len(ids) == count
    assert len(set(ids)) == count
    parsed = 0
    for path in reg.glob("*.json"):
        json.loads(path.read_text())
        parsed += 1
    assert parsed == count


def test_lr_13_single_line_compat(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    entry = _register(reg, project)
    rows = engine_json("list", "--active", reg=reg)
    assert len(rows) == 1
    assert rows[0]["line_id"] == entry["line_id"]
    assert rows[0]["state"] == "active"
