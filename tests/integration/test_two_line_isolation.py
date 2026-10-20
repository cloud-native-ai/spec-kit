"""Integration S2: two lines with identical sentinels never cross-attribute.

Same environment, same generic sentinel, same CLI name; the only difference is
the `(line_id, run_id)` envelope.  Also proves the unlabelled-message rule and
the zero-process-scan rule with PATH stubs.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from fixtures.line_fixtures import (
    append_meta,
    base_env,
    engine_json,
    four_piece,
    install_process_stubs,
    make_line_id,
    make_project,
    make_run_id,
    run_engine,
    run_watcher,
    stub_calls,
    write_log,
    write_status,
)


def _register(reg: Path, project: Path, line: str, run: str) -> dict:
    return engine_json(
        "register", "--line-id", line, "--run-id", run,
        "--project-dir", str(project), "--repo-root", str(project),
        "--state", "active", "--cli", "qodercli", reg=reg,
    )


def _attribution(output: str) -> str:
    return re.search(r"attribution=(\S+)", output).group(1)


def test_two_lines_same_sentinel_no_cross_attribution(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    l1, r1 = make_line_id("alpha"), make_run_id()
    l2, r2 = make_line_id("beta"), make_run_id()
    _register(reg, project, l1, r1)
    _register(reg, project, l2, r2)
    p1 = four_piece(tmp_path / "l1", l1, r1, stage="plan", sentinel=True)
    p2 = four_piece(tmp_path / "l2", l2, r2, stage="plan", sentinel=True)

    w1 = run_watcher(p1, l1, r1, "PLAN-DONE")
    w2 = run_watcher(p2, l2, r2, "PLAN-DONE")
    assert w1.returncode == 0 and w2.returncode == 0
    assert "verdict=DONE" in w1.stdout and "verdict=DONE" in w2.stdout
    assert _attribution(w1.stdout) == "own"
    assert _attribution(w2.stdout) == "own"
    assert l2 not in w1.stdout and l1 not in w2.stdout


def test_foreign_status_pid_and_meta_never_change_state(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    l1, r1 = make_line_id("alpha"), make_run_id()
    l2, r2 = make_line_id("beta"), make_run_id()
    _register(reg, project, l1, r1)
    _register(reg, project, l2, r2)
    p1 = four_piece(tmp_path / "l1", l1, r1, stage="plan", sentinel=False)
    p2 = four_piece(tmp_path / "l2", l2, r2, stage="plan", sentinel=True)
    before = json.loads((reg / f"{l1}.json").read_text())

    # Inject L2's terminal evidence into L1's carriers.
    write_status(p1["status"], l2, r2, "plan", sentinel=1)
    write_log(p1["log"], "working", "PLAN-DONE")
    append_meta(p1["meta"], l2, r2, "plan", "log-terminal", sentinel_seen=1, exit_code=0)
    p1["pid"].write_text(p2["pid"].read_text(), encoding="utf-8")

    proc = run_watcher(p1, l1, r1, "PLAN-DONE")
    assert proc.returncode == 10, proc.stdout
    assert "verdict=RUNNING" in proc.stdout
    assert "attribution=foreign" in proc.stdout
    after = json.loads((reg / f"{l1}.json").read_text())
    assert after["state"] == before["state"]
    assert after["updated_at"] == before["updated_at"]


def test_stale_run_and_pid_reuse_do_not_fake_completion(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    line, run = make_line_id("alpha"), make_run_id()
    _register(reg, project, line, run)
    paths = four_piece(tmp_path / "l", line, run, stage="plan", sentinel=False)
    # A previous attempt's sentinel arrives: stale-run, never DONE.
    write_status(paths["status"], line, "r20260101T000000Z-dead", "plan", sentinel=1)
    write_log(paths["log"], "working", "PLAN-DONE")
    stale = run_watcher(paths, line, run, "PLAN-DONE")
    assert stale.returncode == 10
    assert "attribution=stale-run" in stale.stdout
    # The registered PID is dead: DEAD, never DONE.
    paths["pid"].write_text("pid=999999 start=1 line=%s run=%s stage=plan event=pid\n" % (line, run))
    paths["status"].unlink()
    dead = run_watcher(paths, line, run, "PLAN-DONE")
    assert dead.returncode == 13
    assert "verdict=DEAD" in dead.stdout


def test_unlabelled_message_exactly_one_clarification_and_no_process_scan(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    _register(reg, project, make_line_id("alpha"), make_run_id())
    _register(reg, project, make_line_id("beta"), make_run_id())
    stubs = install_process_stubs(tmp_path)
    env = base_env(reg, extra={"PATH": stubs["env"]["PATH"], "STUB_LOG": str(stubs["log"])})
    proc = run_engine("resolve-message", "--message", "继续推进", reg=reg, env=env)
    assert proc.returncode == 0, proc.stderr
    first = json.loads(proc.stdout)
    assert first["decision"] == "clarify"
    question = first["question"]
    assert question.count("?") + question.count("？") == 1
    assert len(first["candidates"]) == 2
    assert stub_calls(stubs) == []


def test_clarified_answer_ambiguity_stops_without_second_question(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    _register(reg, project, make_line_id("alpha"), make_run_id())
    _register(reg, project, make_line_id("beta"), make_run_id())
    proc = run_engine("resolve-message", "--message", "还是不确定", "--clarified", reg=reg)
    assert proc.returncode == 0, proc.stderr
    decision = json.loads(proc.stdout)
    assert decision["decision"] == "ambiguous-stop"
    assert not decision.get("question")
    assert len(decision["candidates"]) == 2


def test_explicit_line_token_routes(tmp_path):
    project = make_project(tmp_path)
    reg = tmp_path / "reg"
    l1, r1 = make_line_id("alpha"), make_run_id()
    _register(reg, project, l1, r1)
    _register(reg, project, make_line_id("beta"), make_run_id())
    proc = run_engine("resolve-message", "--message", f"继续 {l1}", reg=reg)
    decision = json.loads(proc.stdout)
    assert decision["decision"] == "route"
    assert decision["target_line_id"] == l1
