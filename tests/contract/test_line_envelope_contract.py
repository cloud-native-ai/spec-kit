"""Contract tests for contracts/line-envelope-and-ingress.md (EN-01…EN-16)."""
from __future__ import annotations

import json
import os
import re
import subprocess
import time
from pathlib import Path

import pytest

from fixtures.line_fixtures import (
    append_meta,
    base_env,
    engine_json,
    engine_path,
    four_piece,
    install_process_stubs,
    make_line_id,
    make_project,
    make_run_id,
    run_engine,
    run_watcher,
    stub_calls,
    watcher_path,
    write_heartbeat,
    write_log,
    write_pid,
    write_status,
)

SKILL_DIR = Path(__file__).resolve().parents[2] / "skills" / "external" / "sdd-loop-driver"


def _register(reg: Path, project: Path, line: str, run: str, **kwargs) -> dict:
    args = [
        "--line-id", line, "--run-id", run,
        "--project-dir", str(project), "--repo-root", str(project),
        "--state", kwargs.pop("state", "active"),
    ]
    for flag, value in kwargs.items():
        args += [f"--{flag.replace('_', '-')}", str(value)]
    return engine_json("register", *args, reg=reg)


def _attribution(output: str) -> str:
    match = re.search(r"attribution=(\S+)", output)
    assert match, output
    return match.group(1)


def test_en_01_envelope_fields(tmp_path):
    line, run = make_line_id(), make_run_id()
    paths = four_piece(tmp_path, line, run, stage="plan", sentinel=True)
    records = [json.loads(row) for row in paths["meta"].read_text().splitlines()]
    for record in records:
        assert set(record) >= {"line_id", "run_id", "stage", "event", "at"}
        assert record["line_id"] == line and record["run_id"] == run
    terminal = records[-1]
    assert terminal["event"] == "log-terminal"
    assert terminal["sentinel_seen"] == 1 and terminal["exit"] == 0
    prompt = json.loads(paths["prompt_meta"].read_text())
    assert {"line_id", "run_id", "stage", "event", "at"} <= set(prompt)


def test_en_02_carriers(tmp_path):
    recipes = (SKILL_DIR / "references" / "dispatch-recipes.md").read_text(encoding="utf-8")
    for needle in [
        "line=", "run=", "stage=", "event=",
        ".meta.jsonl", ".meta.json", "prompt-<line>-<stage>.md",
    ]:
        assert needle in recipes, f"carrier literal missing from dispatch recipes: {needle}"
    line, run = make_line_id(), make_run_id()
    paths = four_piece(tmp_path, line, run, stage="plan", sentinel=True)
    log_before = paths["log"].read_text()
    assert f"line={line}" in paths["status"].read_text()
    assert f"line={line}" in paths["pid"].read_text()
    assert f"line={line}" in paths["heartbeat"].read_text()
    assert "line_id" in paths["meta"].read_text()
    assert paths["log"].read_text() == log_before
    watch = run_watcher(paths, line, run, "PLAN-DONE")
    assert "stage=plan" in watch.stdout
    assert "event=watcher-verdict" in watch.stdout
    assert " at=" in watch.stdout


def test_en_03_sentinel_untouched(tmp_path):
    line, run = make_line_id(), make_run_id()
    paths = four_piece(tmp_path, line, run, stage="plan", sentinel=True)
    before = paths["log"].read_bytes()
    proc = run_watcher(paths, line, run, "PLAN-DONE")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "verdict=DONE" in proc.stdout
    assert paths["log"].read_bytes() == before
    assert paths["log"].read_text().strip().splitlines()[-1] == "PLAN-DONE"


def test_en_04_classification(tmp_path):
    line, run = make_line_id(), make_run_id()
    other_line, other_run = make_line_id("other"), make_run_id()
    paths = four_piece(tmp_path, line, run, stage="plan", sentinel=True)
    own = run_watcher(paths, line, run, "PLAN-DONE")
    assert own.returncode == 0 and _attribution(own.stdout) == "own"

    legacy = subprocess.run(
        ["bash", str(watcher_path()), "--once", "--label", line,
         "--pid-file", str(paths["pid"]), "--status-file", str(paths["status"]),
         "--log", str(paths["log"]), "--sentinel", "PLAN-DONE",
         "--heartbeat", str(paths["heartbeat"]), "--meta", str(paths["meta"])],
        capture_output=True, text=True,
    )
    assert legacy.returncode == 0 and _attribution(legacy.stdout) == "legacy"

    # foreign: L1 carriers now say L2, and the sentinel is only in that foreign record.
    write_status(paths["status"], other_line, other_run, "plan", sentinel=1)
    write_log(paths["log"], "working", "PLAN-DONE")
    append_meta(paths["meta"], other_line, other_run, "plan", "log-terminal", sentinel_seen=1, exit_code=0)
    foreign = run_watcher(paths, line, run, "PLAN-DONE")
    assert _attribution(foreign.stdout) == "foreign"
    assert "verdict=DONE" not in foreign.stdout

    # stale-run: same line, different run.
    write_status(paths["status"], line, "r20260101T000000Z-dead", "plan", sentinel=1)
    stale = run_watcher(paths, line, run, "PLAN-DONE")
    assert _attribution(stale.stdout) == "stale-run"
    assert "verdict=DONE" not in stale.stdout

    # unattributed: no envelope at all.
    write_status(paths["status"], line, run, "plan", sentinel=1, envelope=False)
    paths["meta"].unlink()
    unattributed = run_watcher(paths, line, run, "PLAN-DONE")
    assert _attribution(unattributed.stdout) == "unattributed"
    assert "verdict=DONE" not in unattributed.stdout


def test_en_05_foreign_not_consumed(tmp_path):
    line, run = make_line_id(), make_run_id()
    other_line, other_run = make_line_id("other"), make_run_id()
    paths = four_piece(tmp_path, line, run, stage="plan", sentinel=False)
    write_status(paths["status"], other_line, other_run, "plan", sentinel=1)
    append_meta(paths["meta"], other_line, other_run, "plan", "log-terminal", sentinel_seen=1, exit_code=0)
    proc = run_watcher(paths, line, run, "PLAN-DONE")
    assert proc.returncode == 10, proc.stdout
    assert "verdict=RUNNING" in proc.stdout
    assert _attribution(proc.stdout) == "foreign"


def test_en_06_watcher_flags_and_exit_codes(tmp_path):
    source = watcher_path().read_text(encoding="utf-8")
    for literal in [
        "EXIT_DONE=0", "EXIT_RUNNING=10", "EXIT_ANOMALY=11", "EXIT_FAILED=12",
        "EXIT_DEAD=13", "EXIT_TIMEOUT=14", "EXIT_INCOMPLETE=15", "EXIT_NO_SIGNAL=16",
    ]:
        assert literal in source
    line, run = make_line_id(), make_run_id()
    root = tmp_path / "cases"
    cases = {}

    done = four_piece(root / "done", line, run, stage="plan", sentinel=True)
    cases["done"] = (run_watcher(done, line, run, "PLAN-DONE").returncode, 0)

    failed = four_piece(root / "failed", line, run, stage="plan", sentinel=False)
    write_status(failed["status"], line, run, "plan", rc=2, sentinel=0)
    cases["failed"] = (run_watcher(failed, line, run, "PLAN-DONE").returncode, 12)

    incomplete = four_piece(root / "incomplete", line, run, stage="plan", sentinel=False)
    write_status(incomplete["status"], line, run, "plan", rc=0, sentinel=0)
    cases["incomplete"] = (run_watcher(incomplete, line, run, "PLAN-DONE").returncode, 15)

    dead = four_piece(root / "dead", line, run, stage="plan", sentinel=False, pid=999999)
    cases["dead"] = (run_watcher(dead, line, run, "PLAN-DONE").returncode, 13)

    running = four_piece(root / "running", line, run, stage="plan", sentinel=False)
    cases["running"] = (
        run_watcher(running, line, run, "PLAN-DONE", "--start-grace", "0").returncode, 10
    )

    no_signal = four_piece(root / "no_signal", line, run, stage="plan", sentinel=False)
    for key in ("pid", "status", "heartbeat", "meta"):
        no_signal[key].unlink(missing_ok=True)
    cases["no_signal"] = (
        run_watcher(no_signal, line, run, "PLAN-DONE", "--start-grace", "0").returncode, 16
    )

    for name, (actual, expected) in cases.items():
        assert actual == expected, f"{name}: {actual} != {expected}"


def test_en_07_targeted_pid_only(tmp_path):
    line, run = make_line_id(), make_run_id()
    paths = four_piece(tmp_path, line, run, stage="plan", sentinel=False)
    stubs = install_process_stubs(tmp_path)
    proc = run_watcher(paths, line, run, "PLAN-DONE", env=stubs["env"])
    assert proc.returncode == 10
    assert stub_calls(stubs) == [], "watcher invoked a broad process scan"
    source = watcher_path().read_text(encoding="utf-8")
    runtime = source[: source.find("# ---------------------------------------------------------------- self-test")]
    runtime = "\n".join(
        line for line in runtime.splitlines() if not line.lstrip().startswith("#")
    )
    assert not re.search(r"\b(pgrep|pidof)\b", runtime)
    assert not re.search(r"\bps\b", runtime)


def test_en_08_active_definition(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    line, run = make_line_id(), make_run_id()
    _register(reg, project, line, run)
    engine_json("update", "--line-id", line, "--state", "completed", reg=reg)
    decision = engine_json("resolve-message", "--message", "继续推进", reg=reg)
    assert decision["decision"] == "no-active"


def test_en_09_identifiable_tokens(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    l1, r1 = make_line_id("alpha"), make_run_id()
    l2, r2 = make_line_id("beta"), make_run_id()
    _register(reg, project, l1, r1)
    _register(reg, project, l2, r2)
    by_id = engine_json("resolve-message", "--message", f"继续 {l1}", reg=reg)
    assert by_id["decision"] == "route" and by_id["target_line_id"] == l1
    own_boundary = engine_json("resolve-message", "--message", f"继续 x{l1}x", reg=reg)
    assert own_boundary["decision"] == "clarify"
    by_path = engine_json("resolve-message", "--message", f"在 {project} 继续", reg=reg)
    assert by_path["decision"] == "clarify"  # both lines share the project -> not unique


def test_en_10_exactly_one_clarification(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    _register(reg, project, make_line_id("alpha"), make_run_id())
    _register(reg, project, make_line_id("beta"), make_run_id())
    decision = engine_json("resolve-message", "--message", "继续推进", reg=reg)
    assert decision["decision"] == "clarify"
    question = decision["question"]
    assert question.count("?") <= 1 and question.count("？") <= 1
    assert len(decision["candidates"]) == 2
    for candidate in decision["candidates"]:
        for key in ("line_id", "project_dir", "branch", "stage", "state"):
            assert key in candidate
    for candidate in decision["candidates"]:
        assert candidate["line_id"] in question


def test_en_11_ambiguous_stop(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    _register(reg, project, make_line_id("alpha"), make_run_id())
    _register(reg, project, make_line_id("beta"), make_run_id())
    decision = engine_json("resolve-message", "--message", "继续推进", "--clarified", reg=reg)
    assert decision["decision"] == "ambiguous-stop"
    assert "question" not in decision or decision.get("question") in (None, "")
    assert len(decision["candidates"]) == 2


def test_en_12_single_zero_active(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    single = _register(reg, project, make_line_id("solo"), make_run_id())
    routed = engine_json("resolve-message", "--message", "继续", reg=reg)
    assert routed["decision"] == "route"
    assert routed["target_line_id"] == single["line_id"]
    mismatch = engine_json("resolve-message", "--message", "继续 ghost-00000000T000000Z-0000", reg=reg)
    assert mismatch["decision"] == "no-match"
    engine_json("deregister", "--line-id", single["line_id"], "--reason", "done", reg=reg)
    empty = engine_json("resolve-message", "--message", "继续", reg=reg)
    assert empty["decision"] == "no-active"


def test_en_13_clarification_non_blocking(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    l1, r1 = make_line_id("alpha"), make_run_id()
    l2, r2 = make_line_id("beta"), make_run_id()
    _register(reg, project, l1, r1)
    entry2 = _register(reg, project, l2, r2)
    heartbeat = tmp_path / "heartbeat-l2.log"
    write_heartbeat(heartbeat, line=l2, run=r2, stage="plan")
    before_mtime = heartbeat.stat().st_mtime_ns
    decision = engine_json("resolve-message", "--message", "继续推进", reg=reg)
    assert decision["decision"] == "clarify"
    time.sleep(0.02)
    write_heartbeat(heartbeat, line=l2, run=r2, stage="plan")
    updated = engine_json("update", "--line-id", l2, "--last-event", "still-advancing", reg=reg)
    assert heartbeat.stat().st_mtime_ns >= before_mtime
    assert updated["updated_at"] >= entry2["updated_at"]
    assert updated["state"] == "active"
    l1_entry = json.loads((reg / f"{l1}.json").read_text())
    assert l1_entry["state"] == "active"


def test_en_14_no_process_scan(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    _register(reg, project, make_line_id("alpha"), make_run_id())
    _register(reg, project, make_line_id("beta"), make_run_id())
    stubs = install_process_stubs(tmp_path)
    env = base_env(reg, extra={"PATH": stubs["env"]["PATH"], "STUB_LOG": str(stubs["log"])})
    proc = run_engine("resolve-message", "--message", "继续推进", reg=reg, env=env)
    assert proc.returncode == 0, proc.stderr
    assert stub_calls(stubs) == []
    source = engine_path().read_text(encoding="utf-8")
    start = source.find("def action_resolve_message")
    assert start != -1
    end = source.find("\ndef ", start + 10)
    body = source[start:end if end != -1 else len(source)]
    assert "subprocess" not in body
    assert not re.search(r"\b(ps|pgrep|pidof)\b", body)
    assert "cwd" not in body.lower()


def test_en_15_integration_delegate():
    integration = (
        Path(__file__).resolve().parents[1] / "integration" / "test_two_line_isolation.py"
    )
    text = integration.read_text(encoding="utf-8")
    for needle in ["PLAN-DONE", "foreign", "clarify", "attribution"]:
        assert needle in text


def test_en_16_single_line_envelope_compat(tmp_path):
    line, run = make_line_id(), make_run_id()
    paths = four_piece(tmp_path, line, run, stage="plan", sentinel=True)
    flagged = run_watcher(paths, line, run, "PLAN-DONE")
    assert flagged.returncode == 0
    assert _attribution(flagged.stdout) == "own"
    legacy = subprocess.run(
        ["bash", str(watcher_path()), "--once", "--label", line,
         "--pid-file", str(paths["pid"]), "--status-file", str(paths["status"]),
         "--log", str(paths["log"]), "--sentinel", "PLAN-DONE",
         "--heartbeat", str(paths["heartbeat"]), "--meta", str(paths["meta"])],
        capture_output=True, text=True,
    )
    assert legacy.returncode == 0
    assert _attribution(legacy.stdout) == "legacy"
