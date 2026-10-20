"""Unit tests for the line-registry engine (Feature 064).

Partitioned by story: foundational primitives first, then US1 (envelope /
ingress / state words), US2 (paths / queue / resources), US3 (lease /
reservation / identity). Each story appends its own cases in the same file.
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import pytest

from fixtures.line_fixtures import base_env, engine_path, make_line_id, make_run_id

REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_engine():
    path = engine_path()
    if not path.exists():
        raise AssertionError(f"engine missing: {path}")
    spec = importlib.util.spec_from_file_location("line_registry_engine", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["line_registry_engine"] = module
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------- foundational


def test_action_dispatch_table_covers_contract_actions():
    engine = _load_engine()
    expected = {
        "register", "update", "deregister", "list", "resolve-message",
        "verify-identity", "classify-remote", "reattach-brief",
        "lease-acquire", "lease-renew", "lease-release", "lease-break",
        "reserve", "reservation-status", "reservation-break",
        "orphan-check", "ownership-check", "release-ownership", "promote-waiting",
        "integration-enqueue", "integration-plan", "integration-record",
        "allocate-resources", "archive-runtime",
    }
    assert expected <= set(engine.ACTIONS)


def test_exit_code_taxonomy_constants():
    engine = _load_engine()
    assert engine.EXIT_OK == 0
    assert engine.EXIT_USAGE == 2
    assert engine.EXIT_HELD == 3
    assert engine.EXIT_NO_IDENTITY == 4
    assert engine.EXIT_IO == 6


def test_line_id_format_and_slug_normalization():
    engine = _load_engine()
    assert re.match(engine.LINE_ID_RE, "demo-20261020T120000Z-a1b2")
    assert engine.slugify("My_Project.v2") == "my-project-v2"
    generated = engine.generate_line_id(Path("/tmp/My Project.v2"), now=1792500000)
    assert re.match(engine.LINE_ID_RE, generated), generated
    assert generated.startswith("my-project-v2-")


def test_run_id_format():
    engine = _load_engine()
    assert re.match(engine.RUN_ID_RE, "r20261020T120000Z-a1b2")
    generated = engine.generate_run_id()
    assert re.match(engine.RUN_ID_RE, generated), generated


def test_registry_dir_resolution_override_xdg_and_home(tmp_path, monkeypatch):
    engine = _load_engine()
    override = tmp_path / "override"
    monkeypatch.setenv("SPECIFY_LINE_REGISTRY_DIR", str(override))
    assert engine.resolve_registry_dir() == override
    monkeypatch.delenv("SPECIFY_LINE_REGISTRY_DIR")
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "xdg"))
    assert engine.resolve_registry_dir() == tmp_path / "xdg" / "spec-kit" / "lines"
    monkeypatch.delenv("XDG_STATE_HOME")
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    assert engine.resolve_registry_dir() == tmp_path / "home" / ".local" / "state" / "spec-kit" / "lines"


def test_atomic_write_fsync_and_os_replace(tmp_path, monkeypatch):
    engine = _load_engine()
    target = tmp_path / "entry.json"
    calls = {"fsync": 0, "replace": 0}
    real_fsync, real_replace = os.fsync, os.replace

    def counting_fsync(fd):
        calls["fsync"] += 1
        return real_fsync(fd)

    def counting_replace(src, dst):
        calls["replace"] += 1
        return real_replace(src, dst)

    monkeypatch.setattr(os, "fsync", counting_fsync)
    monkeypatch.setattr(os, "replace", counting_replace)
    engine.atomic_write_json(target, {"line_id": "x", "n": 1})
    assert json.loads(target.read_text())["n"] == 1
    assert calls["replace"] == 1
    assert calls["fsync"] >= 2  # file + directory
    assert not list(tmp_path.glob("*.tmp*")), "temp file leaked"


def test_same_line_lock_blocks_second_writer(tmp_path):
    engine = _load_engine()
    lock_path = tmp_path / "line.lock"
    script = (
        "import fcntl, sys, time\n"
        f"fh = open({str(lock_path)!r}, 'w')\n"
        "fcntl.flock(fh, fcntl.LOCK_EX)\n"
        "print('held', flush=True)\n"
        "time.sleep(2)\n"
    )
    holder = subprocess.Popen(
        [sys.executable, "-c", script], stdout=subprocess.PIPE, text=True
    )
    try:
        assert holder.stdout.readline().strip() == "held"
        started = time.time()
        with pytest.raises(engine.LockTimeout):
            with engine.line_lock(lock_path, timeout=0.2):
                pass
        assert time.time() - started < 1.5
    finally:
        holder.kill()
        holder.wait(timeout=3)


def test_unknown_fields_preserved_on_update(tmp_path):
    engine = _load_engine()
    reg = tmp_path / "reg"
    reg.mkdir()
    entry = {
        "schema_version": 1,
        "line_id": make_line_id(),
        "run_id": make_run_id(),
        "project_dir": str(tmp_path),
        "repo_root": str(tmp_path),
        "driver_session": "s1",
        "cli": "qodercli",
        "state": "active",
        "last_event": "registered",
        "created_at": "2026-10-20T00:00:00Z",
        "updated_at": "2026-10-20T00:00:00Z",
        "x_extension": {"kept": True},
    }
    (reg / f"{entry['line_id']}.json").write_text(json.dumps(entry), encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(engine_path()), "--action", "update",
         "--line-id", entry["line_id"], "--last-event", "u2-dispatch"],
        capture_output=True, text=True, env=base_env(reg),
    )
    assert proc.returncode == 0, proc.stderr
    updated = json.loads((reg / f"{entry['line_id']}.json").read_text())
    assert updated["x_extension"] == {"kept": True}
    assert updated["last_event"] == "u2-dispatch"


def test_usage_error_exit_code(tmp_path):
    engine = _load_engine()
    proc = subprocess.run(
        [sys.executable, str(engine_path()), "--action", "no-such-action"],
        capture_output=True, text=True, env=base_env(tmp_path / "reg"),
    )
    assert proc.returncode == engine.EXIT_USAGE
    assert "error" in proc.stdout.lower() or "error" in proc.stderr.lower()


# ---------------------------------------------------------------- US1: envelope / ingress


def test_envelope_classification_five_values():
    engine = _load_engine()
    target_line, target_run = "demo-20261020T120000Z-a1b2", "r20261020T120000Z-a1b2"
    assert engine.classify_envelope(target_line, target_run, target_line, target_run) == "own"
    assert engine.classify_envelope("other-20261020T120000Z-a1b2", target_run, target_line, target_run) == "foreign"
    assert engine.classify_envelope(target_line, "r20261020T120000Z-dead", target_line, target_run) == "stale-run"
    assert engine.classify_envelope("", "", target_line, target_run) == "unattributed"
    assert engine.classify_envelope(target_line, target_run, "", "") == "legacy"


def test_ingress_decision_table():
    engine = _load_engine()
    assert engine.decide_ingress(0, 0, False, False) == "no-active"
    assert engine.decide_ingress(1, 0, False, False) == "route"
    assert engine.decide_ingress(1, 1, True, False) == "route"
    assert engine.decide_ingress(1, 0, True, False) == "no-match"
    assert engine.decide_ingress(2, 1, True, False) == "route"
    assert engine.decide_ingress(2, 0, False, False) == "clarify"
    assert engine.decide_ingress(2, 0, False, True) == "ambiguous-stop"
    assert engine.decide_ingress(2, 2, True, False) == "clarify"
    assert engine.decide_ingress(2, 2, True, True) == "ambiguous-stop"


def test_state_word_list_and_active_set():
    engine = _load_engine()
    assert engine.STATE_VALUES == {
        "active", "waiting", "stalled", "completed", "orphaned", "stale", "closed"
    }
    assert engine.ACTIVE_STATES == {"active", "waiting"}


def test_event_word_list_and_attribution_values():
    engine = _load_engine()
    assert engine.EVENT_VALUES == {
        "prompt", "pid", "heartbeat", "status", "log-start", "log-terminal",
        "watcher-verdict", "monitor", "registry-update", "integration",
    }
    assert engine.ATTRIBUTION_VALUES == {"own", "foreign", "stale-run", "unattributed", "legacy"}


# ---------------------------------------------------------------- US2: paths / queue / resources


def test_path_normalization_and_overlap(tmp_path):
    engine = _load_engine()
    repo = tmp_path / "repo"
    (repo / "src" / "lib").mkdir(parents=True)
    (repo / "link").symlink_to(repo / "src", target_is_directory=True)
    a = engine.normalize_path("src/lib", repo)
    b = engine.normalize_path(str(repo / "link" / "lib"), repo)
    assert a == b
    assert engine.paths_overlap(a, str(repo / "src"))
    assert not engine.paths_overlap(a, str(repo / "other"))


def test_topological_layers_and_cycle_refusal():
    engine = _load_engine()
    layers = engine.topological_layers(
        ["a", "b", "c"], {"a": set(), "b": set(), "c": {"a"}}
    )
    assert layers == [["a", "b"], ["c"]]
    with pytest.raises(engine.EngineError):
        engine.topological_layers(["a", "b"], {"a": {"b"}, "b": {"a"}})


def test_conflict_name_is_deterministic():
    engine = _load_engine()
    name, conflict = engine.conflict_name({"same.md"}, "same.md", "line-x")
    assert conflict is True and name == "same.md.line-x.1"
    name2, conflict2 = engine.conflict_name({"same.md", name}, "same.md", "line-x")
    assert conflict2 is True and name2 == "same.md.line-x.2"
    assert engine.conflict_name(set(), "same.md", "line-x") == ("same.md", False)


def test_port_block_allocation_skips_used_ranges():
    engine = _load_engine()
    block = engine.allocate_port_block([(39000, 39019), (39040, 39059)], 39000, 20)
    assert block == (39020, 39039)
    assert engine.allocate_port_block([], 39000, 20) == (39000, 39019)
