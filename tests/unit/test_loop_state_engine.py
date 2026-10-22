"""Unit tests for the loop-state engine (Feature 065 / Slice 065a).

Red-first: written before the engine implementation (tasks.md T005..T007).

The file is a sequence of test groups that mirror the task split, so a red run
maps cleanly to a task:

- T005 — path / Registry / spine resolution, not-dispatched, single-line,
  determinism.
- T006 — four-piece + watchbeat + sentinel, stale signals, artifacts and
  commit evidence.
- T007 — FR-004 derived priority, the six detectors, watcher tri-state and
  attribution, the IA-14 action matrix, salvage/attempt gates, probe shapes,
  and the SC-001 accident replay.

Owner note: the derived mapping under test is owned by slice
`requirements.md` FR-004 (parent #FR-004). These tests mirror that table; they
never restate it as an authority. The reference `state-awareness.md`
(§Derived Mapping / §Stage Artifact Map) is only ever a mirror and is created
by T018, so tuple-equality tests against it live in the contract test file.
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

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "loop-state.py"

LINE = "demo-line"
NOW = int(time.time())

# Explicit thresholds keep every fixture independent of watch-target.sh
# defaults (C-16: the engine embeds no second set of numbers).
DEFAULT_THRESHOLDS = {
    "start-grace": 0,
    "deadline-grace": 0,
    "heartbeat-max-age": 3600,
}


def _load_engine():
    assert SCRIPT.exists(), f"engine missing: {SCRIPT}"
    spec = importlib.util.spec_from_file_location("loop_state_engine", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["loop_state_engine"] = module
    spec.loader.exec_module(module)
    return module


def _run(args, env=None, cwd=None, timeout=120, unset=None):
    merged = dict(os.environ)
    if env:
        merged.update(env)
    # `unset` removes inherited names (e.g. SPECIFY_LINE_RUNTIME_DIR) so the
    # R-02 fallback tail can be exercised instead of the host's own value.
    for name in unset or ():
        merged.pop(name, None)
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, env=merged, cwd=cwd, timeout=timeout,
    )


def _iso_utc(value):
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", value or ""))


def _dead_pid():
    """A pid that certainly belonged to a process which has already exited."""
    proc = subprocess.Popen([sys.executable, "-c", "pass"])
    proc.wait()
    return proc.pid


class Workspace:
    """One line's read-only evidence tree plus a git repo to derive commits."""

    def __init__(self, root: Path):
        self.root = Path(root)
        self.line = LINE
        self.stage = "tasks"
        self.state_dir = self.root / "state" / LINE
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.repo = self.root / "repo"
        self.spec_dir = self.repo / ".specify" / "specs" / "demo"
        self.spec_dir.mkdir(parents=True, exist_ok=True)
        self.spine = self.state_dir / "spine.md"
        self.registry_dir = self.root / "registry"
        self.registry_dir.mkdir(exist_ok=True)
        self.home = self.root / "home"
        self.home.mkdir(exist_ok=True)
        self.watch_script = self.root / "watch.sh"
        self.no_watch = self.root / "no-such-watch.sh"
        self.env = {
            "SPECIFY_LINE_REGISTRY_DIR": str(self.registry_dir),
            "SPECIFY_LINE_RUNTIME_DIR": str(self.state_dir),
            "HOME": str(self.home),
            "XDG_STATE_HOME": str(self.root / "xdg"),
        }

    # -- file names -------------------------------------------------------
    def path(self, kind, stage=None):
        stage = stage or self.stage
        names = {
            "pid": "pid-%s-%s" % (self.line, stage),
            "status": "status-%s-%s" % (self.line, stage),
            "log": "log-%s-%s.log" % (self.line, stage),
            "heartbeat": "heartbeat-%s-%s.log" % (self.line, stage),
            "watchbeat": "watchbeat-%s-%s" % (self.line, stage),
        }
        return self.state_dir / names[kind]

    # -- spine ------------------------------------------------------------
    def write_spine(self, *, state="running", started_at=NOW - 100, deadline=NOW + 3600,
                    base_commit="abc1234", attempt=1, retry_limit=2, run_id=None,
                    last_verdict=None, salvage=None, salvage_evidence=None,
                    salvage_at=None):
        lines = [
            "# Loop State Spine — %s" % self.line,
            "",
            "<!-- loop-state:begin -->",
            "spine_schema: v1",
            "spine_state: %s" % state,
        ]
        if started_at is not None:
            lines.append("stage_started_at: %d" % started_at)
        if deadline is not None:
            lines.append("stage_deadline_epoch: %d" % deadline)
        if base_commit is not None:
            lines.append("stage_base_commit: %s" % base_commit)
        if attempt is not None:
            lines.append("attempt: %d" % attempt)
        if retry_limit is not None:
            lines.append("retry_limit: %d" % retry_limit)
        if run_id is not None:
            lines.append("run_id: %s" % run_id)
        if last_verdict is not None:
            lines.append("last_verdict: %s" % last_verdict)
        if salvage is not None:
            lines.append("salvage: %s" % salvage)
        if salvage_evidence is not None:
            lines.append("salvage_evidence: %s" % salvage_evidence)
        if salvage_at is not None:
            lines.append("salvage_at: %s" % salvage_at)
        lines += ["<!-- loop-state:end -->", ""]
        self.spine.write_text("\n".join(lines), encoding="utf-8")

    def write_legacy_spine(self, state="running"):
        self.spine.write_text(
            "# Loop State Spine — %s\n\nstate: %s\n" % (self.line, state),
            encoding="utf-8",
        )

    # -- registry ---------------------------------------------------------
    def write_registry(self, *, stage=None, run_id="run-1", state="active",
                       spine_path=None, status_path=None):
        entry = {
            "schema_version": 1,
            "line_id": self.line,
            "run_id": run_id,
            "state": state,
            "project_dir": str(self.repo),
            "repo_root": str(self.repo),
            "driver_session": "pid:1",
            "cli": "qodercli",
            "updated_at": "2026-10-21T10:00:00Z",
            "spine_path": str(spine_path or self.spine),
            "status_path": str(status_path or self.path("status")),
        }
        if stage:
            entry["stage"] = stage
        (self.registry_dir / ("%s.json" % self.line)).write_text(
            json.dumps(entry), encoding="utf-8")

    # -- four-piece + watchbeat ------------------------------------------
    def write_pid(self, *, pid=None, start="424242", run=None, at=None,
                  line=True, stage=None):
        tokens = [
            "pid=%d" % (os.getpid() if pid is None else pid),
            "start=%s" % start,
            "at=%d" % (NOW if at is None else at),
        ]
        if line:
            tokens.append("line=%s" % self.line)
        if run is not None:
            tokens.append("run=%s" % run)
        tokens += ["stage=%s" % (stage or self.stage), "event=pid"]
        p = self.path("pid", stage)
        p.write_text(" ".join(tokens) + "\n", encoding="utf-8")
        return p

    def write_status(self, *, exit_code=0, sentinel=1, run=None, at=None,
                     line=True, stage=None, progress="stream"):
        tokens = [
            "exit=%s" % exit_code,
            "at=%d" % (NOW if at is None else at),
            "sentinel=%s" % sentinel,
        ]
        if line:
            tokens.append("line=%s" % self.line)
        if run is not None:
            tokens.append("run=%s" % run)
        tokens += ["stage=%s" % (stage or self.stage), "event=status",
                   "progress=%s" % progress]
        p = self.path("status", stage)
        p.write_text(" ".join(tokens) + "\n", encoding="utf-8")
        return p

    def write_log(self, lines, stage=None):
        p = self.path("log", stage)
        body = lines if isinstance(lines, str) else "\n".join(lines)
        p.write_text(body + "\n", encoding="utf-8")
        return p

    def write_heartbeat(self, *, at=None, run=None, line=True, stage=None):
        tokens = ["at=%d" % (NOW if at is None else at)]
        if line:
            tokens.append("line=%s" % self.line)
        if run is not None:
            tokens.append("run=%s" % run)
        tokens += ["stage=%s" % (stage or self.stage), "event=heartbeat"]
        p = self.path("heartbeat", stage)
        p.write_text(" ".join(tokens) + "\n", encoding="utf-8")
        return p

    def write_watchbeat(self, *, at=None, window=300, run="run-1",
                        event="watch-window", stage=None):
        tokens = []
        if run is not None:
            tokens.append("run=%s" % run)
        tokens.append("stage=%s" % (stage or self.stage))
        if window is not None:
            tokens.append("window=%d" % window)
        tokens.append("at=%d" % (NOW if at is None else at))
        tokens.append("event=%s" % event)
        p = self.path("watchbeat", stage)
        p.write_text(" ".join(tokens) + "\n", encoding="utf-8")
        return p

    def write_watch_script(self, line=None):
        line = line or (
            "WATCH label=demo-line verdict=STALLED pid=alive heartbeat=fresh "
            "hook=na anomaly=0 sentinel=0 rc=13 reason=stalled stream=na "
            "line=demo-line run=run-1 stage=tasks event=watcher-verdict at=1 "
            "attribution=legacy"
        )
        self.watch_script.write_text(
            "#!/usr/bin/env bash\ncat <<'WATCH_EOF'\n%s\nWATCH_EOF\n" % line,
            encoding="utf-8",
        )
        return self.watch_script

    # -- artifacts + git ---------------------------------------------------
    def write_artifact(self, name, text="content\n"):
        p = self.spec_dir / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        return p

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=str(self.repo),
                              capture_output=True, text=True)

    def git_commit(self, message):
        self.git("add", "-A")
        done = self.git("commit", "-q", "--allow-empty", "-m", message)
        assert done.returncode == 0, done.stderr
        return self.git("rev-parse", "HEAD").stdout.strip()

    def git_base(self):
        if not (self.repo / ".git").exists():
            for args in (("init", "-q"),
                         ("config", "user.email", "test@example.com"),
                         ("config", "user.name", "Test"),
                         ("config", "commit.gpgsign", "false")):
                done = self.git(*args)
                assert done.returncode == 0, done.stderr
        return self.git_commit("base")


def _snapshot(ws, *extra, stage="tasks", spine=True, state_dir=True,
              spec_dir=True, repo=True, watch=None, thresholds=None, unset=None):
    th = dict(DEFAULT_THRESHOLDS)
    if thresholds:
        th.update(thresholds)
    args = ["--action", "snapshot", "--line-id", ws.line]
    if state_dir:
        args += ["--state-dir", str(ws.state_dir)]
    if spec_dir:
        args += ["--spec-dir", str(ws.spec_dir)]
    if repo:
        args += ["--repo", str(ws.repo)]
    if spine:
        args += ["--spine", str(ws.spine)]
    args += ["--watch-script", str(watch or ws.no_watch)]
    for flag, key in (("--start-grace", "start-grace"),
                      ("--deadline-grace", "deadline-grace"),
                      ("--heartbeat-max-age", "heartbeat-max-age")):
        if th.get(key) is not None:
            args += [flag, str(th[key])]
    if stage is not None:
        args += ["--stage", stage]
    args += [str(x) for x in extra]
    return _run(args, env=ws.env, unset=unset)


def _snap_json(ws, *extra, **kwargs):
    proc = _snapshot(ws, *extra, **kwargs)
    assert proc.returncode == 0, (
        "snapshot exit %d\nstderr: %s\nstdout: %s"
        % (proc.returncode, proc.stderr, proc.stdout)
    )
    return json.loads(proc.stdout)


def _forms(envelope):
    return [item["form"] for item in envelope["interruptions"]]


def _stale(envelope, signal):
    return [s for s in envelope["stale_signals"] if s["signal"] == signal]


# ---------------------------------------------------------------------------
# T005 — path resolution, Registry fallback, spine parse, not-dispatched
# ---------------------------------------------------------------------------

def test_explicit_paths_win_over_registry(tmp_path):
    ws = Workspace(tmp_path)
    ws.write_spine(state="running")
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    (elsewhere / "spine.md").write_text("# not this one\n", encoding="utf-8")
    ws.write_registry(stage="tasks", spine_path=elsewhere / "spine.md")

    env = _snap_json(ws)

    assert env["paths"]["spine"] == str(ws.spine)
    assert env["spine"]["path"] == str(ws.spine)
    assert env["spine"]["status"] == "present"
    assert env["spine"]["schema"] == "v1"
    assert env["spine"]["state"] == "running"
    assert env["spine"]["state_value_state"] == "known"


def test_v1_spine_fields_are_parsed_without_guessing(tmp_path):
    ws = Workspace(tmp_path)
    ws.write_spine(state="running", started_at=NOW - 100, deadline=NOW + 3600,
                   base_commit="deadbee", attempt=3, retry_limit=5,
                   run_id="run-9", last_verdict="RUNNING")
    env = _snap_json(ws)

    fields = env["spine"]["fields"]
    assert fields["stage_started_at"] == NOW - 100
    assert fields["stage_deadline_epoch"] == NOW + 3600
    assert fields["stage_base_commit"] == "deadbee"
    assert fields["attempt"] == 3
    assert fields["retry_limit"] == 5
    assert env["spine"]["missing_fields"] == []
    # No four-piece evidence in this fixture and the start grace has elapsed, so
    # FR-004 rule (6) derives NO_SIGNAL != last_verdict RUNNING; C-39 then
    # requires consistent=false (report, never silently pick a side).
    assert env["loop_state"] == "NO_SIGNAL"
    assert env["spine"]["consistent"] is False


def test_registry_fallback_resolves_paths_and_stage(tmp_path):
    ws = Workspace(tmp_path)
    ws.write_spine(state="running")
    ws.write_registry(stage="tasks")

    env = _snap_json(ws, spine=False, state_dir=False)

    assert env["registry"]["status"] == "present"
    assert env["registry"]["stage"] == "tasks"
    assert env["registry"]["run_id"] == "run-1"
    assert env["stage"] == "tasks"
    assert env["paths"]["spine"] == str(ws.spine)
    assert env["paths"]["state_dir"] == str(ws.state_dir)


def test_state_dir_falls_back_to_runtime_dir_env(tmp_path):
    """R-02 level 3: with no --state-dir and no Registry `status_path`, the
    `SPECIFY_LINE_RUNTIME_DIR` convention the runner writes to is used, so the
    four-piece evidence is still found instead of leaving `state_dir` null."""
    ws = Workspace(tmp_path)  # no registry entry -> level 2 cannot fire
    ws.write_spine(state="running")
    pid = ws.write_pid(pid=os.getpid())
    ws.write_heartbeat()

    env = _snap_json(ws, state_dir=False)  # --spine stays explicit

    assert env["registry"]["status"] == "missing"
    assert env["paths"]["state_dir"] == str(ws.state_dir)
    assert env["evidence"]["pid"]["status"] == "present"
    assert env["evidence"]["pid"]["path"] == str(pid)
    assert env["loop_state"] == "RUNNING"


def test_state_dir_falls_back_to_home_when_runtime_env_is_absent(tmp_path):
    """R-02 level 4: with no --state-dir, no Registry and no
    `SPECIFY_LINE_RUNTIME_DIR`, `$HOME` is the last resort. The fixture points
    HOME at a temp dir, so the real home is neither read nor written."""
    ws = Workspace(tmp_path)  # no registry entry
    ws.write_spine(state="running")
    home_pid = ws.home / ("pid-%s-%s" % (ws.line, ws.stage))
    home_pid.write_text(
        "pid=%d start=424242 at=%d line=%s stage=%s event=pid\n"
        % (os.getpid(), NOW, ws.line, ws.stage), encoding="utf-8")
    (ws.home / ("heartbeat-%s-%s.log" % (ws.line, ws.stage))).write_text(
        "at=%d line=%s stage=%s event=heartbeat\n" % (NOW, ws.line, ws.stage),
        encoding="utf-8")

    env = _snap_json(ws, state_dir=False, unset=["SPECIFY_LINE_RUNTIME_DIR"])

    assert env["paths"]["state_dir"] == str(ws.home)
    assert env["paths"]["state_dir"] != str(Path.home()), "real home must stay out"
    assert env["evidence"]["pid"]["status"] == "present"
    assert env["evidence"]["pid"]["path"] == str(home_pid)
    assert env["loop_state"] == "RUNNING"


def test_missing_registry_continues_evaluation(tmp_path):
    ws = Workspace(tmp_path)
    ws.write_spine(state="running")
    ws.write_pid(pid=os.getpid())
    ws.write_heartbeat()

    env = _snap_json(ws)

    assert env["registry"]["status"] == "missing"
    assert env["registry"]["stage"] is None
    assert env["spine"]["status"] == "present"
    assert env["loop_state"] == "RUNNING"
    assert env["verdict_source"] == "derived"


def test_legacy_spine_degrades_without_guessing(tmp_path):
    ws = Workspace(tmp_path)
    ws.write_legacy_spine(state="running")
    ws.write_pid(pid=os.getpid())
    ws.write_heartbeat()

    env = _snap_json(ws)

    spine = env["spine"]
    assert spine["schema"] == "legacy"
    assert spine["status"] == "present"
    assert spine["state"] == "running"
    assert spine["state_value_state"] == "known"
    for field in ("stage_started_at", "stage_base_commit", "attempt", "retry_limit"):
        assert field in spine["missing_fields"], field
        assert spine["fields"].get(field) is None, field


def test_stage_argument_alone_is_not_dispatch_evidence(tmp_path):
    ws = Workspace(tmp_path)  # no spine, no registry, no four-piece, no sentinel

    env = _snap_json(ws)  # --stage tasks is caller intent only

    assert env["loop_state"] == "UNKNOWN"
    assert env["loop_state_reason"] == "not-dispatched"
    assert env["recovery_action"] == "none"
    assert env["recovery_reason"] == "not-dispatched"
    assert env["spine"]["status"] == "missing"
    assert env["spine"]["schema"] == "missing"


def test_never_dispatched_marks_evidence_na(tmp_path):
    ws = Workspace(tmp_path)

    env = _snap_json(ws)

    for key in ("pid", "status", "log", "heartbeat", "watchbeat"):
        assert env["evidence"][key]["status"] == "na", key
        assert env["evidence"][key]["value_state"] == "na", key
    assert env["evidence"]["artifacts"]["status"] == "na"
    assert env["evidence"]["artifacts"]["value_state"] == "na"
    assert env["evidence"]["commits"]["status"] == "na"
    assert env["evidence"]["commits"]["value_state"] == "na"
    assert env["false_completion"] is False


def test_nonempty_spine_state_excludes_not_dispatched(tmp_path):
    ws = Workspace(tmp_path)
    ws.write_spine(state="running", started_at=None)  # no stage_started_at, no signals

    env = _snap_json(ws)

    assert env["loop_state_reason"] != "not-dispatched"
    assert env["recovery_reason"] != "not-dispatched"
    assert env["recovery_action"] != "none"
    assert env["evidence"]["pid"]["status"] != "na"


def test_dispatch_evidence_without_spine_is_an_evidence_gap(tmp_path):
    ws = Workspace(tmp_path)
    ws.write_registry(stage="tasks")  # dispatch evidence, spine file absent

    env = _snap_json(ws)

    assert env["spine"]["status"] == "missing"
    assert env["loop_state"] == "UNKNOWN"
    assert env["loop_state_reason"] == "evidence-gap"
    assert env["recovery_action"] == "stop"
    assert env["recovery_reason"] == "evidence-gap"


def test_single_line_evaluation_does_not_cross_lines(tmp_path):
    ws = Workspace(tmp_path)
    ws.state_dir.joinpath("pid-other-line-tasks").write_text(
        "pid=%d start=1 at=%d line=other-line stage=tasks event=pid\n"
        % (os.getpid(), NOW), encoding="utf-8")
    ws.state_dir.joinpath("log-other-line-tasks.log").write_text(
        "TASKS-DONE\n", encoding="utf-8")

    env = _snap_json(ws)

    assert env["line_id"] == "demo-line"
    assert env["loop_state_reason"] == "not-dispatched"
    assert env["interruptions"] == []
    assert env["evidence"]["pid"]["status"] == "na"


def test_two_runs_differ_only_in_evaluated_at(tmp_path):
    ws = Workspace(tmp_path)
    base = ws.git_base()
    ws.write_spine(base_commit=base)
    ws.write_status(exit_code=0, sentinel=1)
    ws.write_log(["TASKS-DONE"])
    ws.write_artifact("tasks.md")

    first = _snap_json(ws)
    second = _snap_json(ws)

    assert _iso_utc(first["evaluated_at"]), first["evaluated_at"]
    assert first["loop_state"] == "DONE"
    left = {k: v for k, v in first.items() if k != "evaluated_at"}
    right = {k: v for k, v in second.items() if k != "evaluated_at"}
    assert left == right


# ---------------------------------------------------------------------------
# T006 — four-piece envelopes, watchbeat marker, sentinel, stale signals
# ---------------------------------------------------------------------------

def test_four_piece_space_envelopes_are_parsed(tmp_path):
    ws = Workspace(tmp_path)
    ws.write_spine()
    ws.write_pid(pid=os.getpid())
    ws.write_status(exit_code=0, sentinel=1)
    ws.write_log(["working", "TASKS-DONE"])
    ws.write_heartbeat()

    env = _snap_json(ws)
    ev = env["evidence"]

    assert ev["pid"]["status"] == "present"
    assert ev["pid"]["value_state"] == "known"
    assert ev["pid"]["pid"] == os.getpid()
    assert ev["pid"]["alive"] is True
    assert ev["status"]["status"] == "present"
    assert ev["status"]["exit_code"] == 0
    assert ev["status"]["sentinel"] == 1
    assert ev["log"]["status"] == "present"
    assert ev["log"]["last_line"] == "TASKS-DONE"
    assert ev["log"]["sentinel_present"] is True
    assert ev["heartbeat"]["status"] == "present"
    assert ev["heartbeat"]["at"] == NOW
    assert ev["heartbeat"]["fresh"] is True


def test_watchbeat_marker_projection_and_freshness(tmp_path):
    ws = Workspace(tmp_path)
    ws.write_spine(run_id="run-1")
    ws.write_pid(pid=os.getpid())
    ws.write_heartbeat()
    ws.write_watchbeat(at=NOW, window=300, run="run-1")

    env = _snap_json(ws)
    wb = env["evidence"]["watchbeat"]

    assert wb["status"] == "present"
    assert wb["value_state"] == "known"
    assert wb["run_id"] == "run-1"
    assert wb["stage"] == "tasks"
    assert wb["window"] == 300
    assert wb["at"] == NOW
    assert wb["event"] == "watch-window"
    assert wb["fresh"] is True


def test_watchbeat_past_its_window_is_not_fresh(tmp_path):
    ws = Workspace(tmp_path)
    ws.write_spine(run_id="run-1")
    ws.write_pid(pid=os.getpid())
    ws.write_heartbeat()
    ws.write_watchbeat(at=NOW - 1000, window=300, run="run-1")

    env = _snap_json(ws)

    assert env["evidence"]["watchbeat"]["fresh"] is False


def test_sentinel_must_be_the_last_nonempty_line(tmp_path):
    ws = Workspace(tmp_path)
    ws.write_spine()
    ws.write_pid(pid=os.getpid())
    ws.write_heartbeat()
    ws.write_log(["TASKS-DONE", "", "still working"])

    env = _snap_json(ws)

    assert env["evidence"]["log"]["sentinel_present"] is False
    assert env["loop_state"] == "RUNNING"


def test_anomaly_last_line_disqualifies_earlier_sentinel(tmp_path):
    ws = Workspace(tmp_path)
    ws.write_spine()
    ws.write_status(exit_code=0, sentinel=0)
    ws.write_log(["TASKS-DONE", "ANOMALY: subagent returned malformed tasks"])

    env = _snap_json(ws)

    assert env["evidence"]["log"]["sentinel_present"] is False
    assert env["evidence"]["log"]["anomaly"] is True
    assert env["loop_state"] == "ANOMALY"


def test_stale_run_mismatch_is_listed_and_excluded(tmp_path):
    ws = Workspace(tmp_path)
    ws.write_spine(run_id="run-1")
    ws.write_pid(pid=os.getpid(), run="run-other")
    ws.write_heartbeat(run="run-other")

    env = _snap_json(ws)

    pid_entries = _stale(env, "pid")
    assert pid_entries, "pid with a foreign run= must be listed as stale"
    entry = pid_entries[0]
    for key in ("signal", "path", "reason", "run_id", "at", "mtime_ns"):
        assert key in entry, key
    assert entry["reason"] == "run-mismatch"
    assert entry["run_id"] == "run-other"
    assert entry["at"] == NOW
    assert env["loop_state"] != "RUNNING", "stale live-looking pid must not drive RUNNING"


def test_stale_signal_older_than_stage_start_is_listed(tmp_path):
    ws = Workspace(tmp_path)
    ws.write_spine(started_at=NOW)
    status = ws.write_status(exit_code=0, sentinel=0)
    os.utime(status, (NOW - 600, NOW - 600))

    env = _snap_json(ws)

    entries = _stale(env, "status")
    assert entries, "a status file older than stage_started_at must be stale"
    assert entries[0]["reason"] == "before-stage-start"
    assert entries[0]["mtime_ns"] is not None


def test_unattributed_legacy_file_is_stale(tmp_path):
    ws = Workspace(tmp_path)
    ws.write_spine()
    ws.write_heartbeat(line=False)  # at= only, no run= and no line=

    env = _snap_json(ws)

    entries = _stale(env, "heartbeat")
    assert entries, "an envelope without run=/line= and no meta is legacy-stale"
    assert entries[0]["reason"] == "legacy-stale"


def test_current_envelope_without_run_is_legacy_not_stale(tmp_path):
    ws = Workspace(tmp_path)
    ws.write_spine()
    ws.write_pid(pid=os.getpid())
    ws.write_heartbeat()
    ws.write_status(exit_code=0, sentinel=1)  # line=/stage= only, no run=

    env = _snap_json(ws)

    assert env["evidence"]["status"]["attribution"] == "legacy"
    assert _stale(env, "status") == [], (
        "a current envelope carrying line=/stage= must not be stale merely for "
        "lacking run="
    )


def test_unresolved_paths_stay_null_and_are_not_invented(tmp_path):
    """C-4 + R-02: only the R-02 chain may produce a path; every item the chain
    cannot produce stays null. `state_dir` is the single item with an env/HOME
    tail, so the fixture's env (level 3) decides it; spine/spec_dir/repo have no
    fallback at all and MUST stay null."""
    ws = Workspace(tmp_path)  # no registry entry, no explicit paths

    env = _snap_json(ws, spine=False, state_dir=False, spec_dir=False, repo=False)

    assert set(env["paths"]) == {"state_dir", "spec_dir", "repo", "spine", "probe"}
    assert env["paths"]["state_dir"] == str(ws.state_dir)
    for key in ("spec_dir", "repo", "spine", "probe"):
        assert env["paths"][key] is None, key
    assert env["registry"]["status"] == "missing"
    assert env["spine"]["status"] == "missing"
    assert env["spine"]["schema"] == "missing"


def test_state_dir_stays_null_when_every_r02_source_is_absent(tmp_path):
    """R-02 invents no default: with --state-dir, the Registry,
    `SPECIFY_LINE_RUNTIME_DIR` AND `$HOME` all absent, `state_dir` is null and
    the four-piece names cannot be built, so no evidence is claimed present."""
    ws = Workspace(tmp_path)  # no registry entry
    ws.write_spine(state="running")

    env = _snap_json(ws, state_dir=False,
                     unset=["SPECIFY_LINE_RUNTIME_DIR", "HOME"])

    assert env["paths"]["state_dir"] is None
    for key in ("pid", "status", "log", "heartbeat", "watchbeat"):
        assert env["evidence"][key]["status"] != "present", key


def test_unreadable_evidence_sources_report_missing_and_exit_zero(tmp_path):
    """C-6: evidence sources degrade to missing/na, never to exit 2."""
    ws = Workspace(tmp_path)
    missing_spine = tmp_path / "nope" / "spine.md"
    ws.write_registry(stage="tasks", spine_path=missing_spine)  # dispatch evidence
    gone = tmp_path / "gone"

    proc = _run(
        [
            "--action", "snapshot", "--line-id", ws.line,
            "--spine", str(missing_spine),
            "--state-dir", str(gone / "state"),
            "--spec-dir", str(gone / "spec"),
            "--repo", str(gone / "repo"),
            "--stage", "tasks",
            "--watch-script", str(ws.no_watch),
        ],
        env=ws.env,
    )

    assert proc.returncode == 0, proc.stderr
    env = json.loads(proc.stdout)
    assert env["spine"]["status"] == "missing"
    assert env["spine"]["schema"] == "missing"
    for key in ("pid", "status", "log", "heartbeat", "watchbeat"):
        assert env["evidence"][key]["status"] == "missing", key
        assert env["evidence"][key]["value_state"] == "na", key
    assert env["evidence"]["pid"].get("pid") is None
    assert env["evidence"]["status"].get("exit_code") is None
    assert "tasks.md" in env["missing_artifacts"]


def test_legacy_spine_marks_degraded_fields_unknown(tmp_path):
    """C-23: legacy degradation is value-level unknown, never a guess."""
    ws = Workspace(tmp_path)
    ws.write_legacy_spine(state="running")

    env = _snap_json(ws)

    spine = env["spine"]
    assert spine["schema"] == "legacy"
    assert spine["missing_fields"], "degraded spine must list what it could not read"
    assert spine["state_value_state"] == "known"
    assert spine["fields"].get("stage_started_at") is None
    assert spine["fields"].get("attempt") is None


# ---------------------------------------------------------------------------
# T006 (continued) — artifacts, checklists, commit evidence, exclusivity
# ---------------------------------------------------------------------------

def _write_plan_artifacts(ws, *, contracts_text="contract text\n"):
    ws.write_artifact("plan.md")
    ws.write_artifact("data-model.md")
    ws.write_artifact("quickstart.md")
    ws.write_artifact("feature-ref.md")
    (ws.spec_dir / "contracts").mkdir(exist_ok=True)
    (ws.spec_dir / "contracts" / "c.md").write_text(contracts_text, encoding="utf-8")


def test_directory_artifact_requires_one_nonempty_file(tmp_path):
    """C-54: a directory artifact needs the dir plus >=1 non-empty file."""
    ws = Workspace(tmp_path)
    ws.stage = "plan"
    base = ws.git_base()
    _write_plan_artifacts(ws)
    ws.write_spine(base_commit=base)
    ws.write_status(exit_code=0, sentinel=1)
    ws.write_log(["PLAN-DONE"])

    env = _snap_json(ws, stage="plan")
    assert env["evidence"]["artifacts"]["complete"] is True
    assert env["missing_artifacts"] == []

    (ws.spec_dir / "contracts" / "c.md").write_text("", encoding="utf-8")
    env = _snap_json(ws, stage="plan")
    assert env["evidence"]["artifacts"]["complete"] is False
    assert "contracts/" in env["missing_artifacts"]

    (ws.spec_dir / "contracts" / "c.md").unlink()
    env = _snap_json(ws, stage="plan")
    assert env["evidence"]["artifacts"]["complete"] is False
    assert "contracts/" in env["missing_artifacts"]


def test_checklist_stage_needs_a_checklist_added_since_base(tmp_path):
    """C-54: pre-existing checklist files alone are not completeness."""
    ws = Workspace(tmp_path)
    ws.stage = "checklist"
    checklist_dir = ws.spec_dir / "checklists"
    checklist_dir.mkdir(parents=True)
    (checklist_dir / "pre-existing.md").write_text("pre\n", encoding="utf-8")
    base = ws.git_base()
    ws.write_spine(base_commit=base)
    ws.write_status(exit_code=0, sentinel=1)
    ws.write_log(["CHECKLIST-DONE"])

    env = _snap_json(ws, stage="checklist")
    assert env["evidence"]["artifacts"]["complete"] is False, (
        "only pre-existing checklist files must not count as complete"
    )

    (checklist_dir / "new.md").write_text("new\n", encoding="utf-8")
    ws.git_commit("checklist: add new item")
    env = _snap_json(ws, stage="checklist")
    assert env["evidence"]["artifacts"]["complete"] is True


def test_commit_evidence_uses_stage_base_commit(tmp_path):
    """C-57/C-58/C-59: baseline, pathspec and uncommitted projection."""
    ws = Workspace(tmp_path)
    base = ws.git_base()
    ws.write_artifact("tasks.md")
    ws.write_spine(base_commit=base)
    ws.write_status(exit_code=0, sentinel=1)
    ws.write_log(["TASKS-DONE"])

    env = _snap_json(ws)
    commits = env["evidence"]["commits"]
    assert commits["status"] == "present"
    assert commits["base"] == base
    assert commits["pathspec"], "pathspec must list the stage artifact paths"
    assert commits["touching"] is False
    assert "tasks.md" in env["uncommitted_artifacts"]
    assert env["recovery_action"] != "verify"

    ws.git_commit("tasks: complete task list")
    env = _snap_json(ws)
    assert env["evidence"]["commits"]["touching"] is True
    assert env["uncommitted_artifacts"] == []
    assert env["recovery_action"] == "verify"


def test_unknown_base_commit_marks_value_unknown_not_head_guess(tmp_path):
    """C-57/C-59: missing baseline never falls back to HEAD or recent commit."""
    ws = Workspace(tmp_path)
    ws.git_base()
    ws.write_artifact("tasks.md")
    ws.write_spine(base_commit=None)  # no stage_base_commit
    ws.write_status(exit_code=0, sentinel=1)
    ws.write_log(["TASKS-DONE"])

    env = _snap_json(ws)

    commits = env["evidence"]["commits"]
    assert commits["value_state"] == "unknown"
    assert commits["base"] is None
    assert env["uncommitted_artifacts"] == [], (
        "an unknown baseline must not be reported as 'everything committed'"
    )


def test_analyze_artifacts_are_vacuously_complete(tmp_path):
    """C-53: analyze has no required file artifacts -> complete=true."""
    ws = Workspace(tmp_path)
    ws.stage = "analyze"  # four-piece names follow the stage under test
    base = ws.git_base()
    ws.write_spine(base_commit=base)
    ws.write_status(exit_code=0, sentinel=1)
    ws.write_log(["ANALYZE-DONE"])

    env = _snap_json(ws, stage="analyze")

    artifacts = env["evidence"]["artifacts"]
    assert artifacts["complete"] is True
    assert artifacts["commit_required"] is False
    assert env["evidence"]["commits"]["status"] == "na"
    assert env["missing_artifacts"] == []
    assert env["recovery_action"] == "verify"


def test_implement_document_only_commit_is_not_complete(tmp_path):
    """C-60: implement completeness is code/test commit evidence only."""
    ws = Workspace(tmp_path)
    ws.stage = "implement"  # four-piece names follow the stage under test
    base = ws.git_base()
    ws.write_spine(base_commit=base)
    ws.write_status(exit_code=0, sentinel=1)
    ws.write_log(["IMPLEMENT-DONE"])
    ws.write_artifact("requirements.md")           # a doc path under .specify/
    ws.git_commit("docs: requirements touch")

    env = _snap_json(ws, stage="implement")
    assert env["evidence"]["artifacts"]["complete"] is False
    assert env["evidence"]["artifacts"]["status"] == "na"
    assert env["recovery_action"] != "verify"

    (ws.repo / "tests").mkdir(exist_ok=True)
    (ws.repo / "tests" / "demo_test.py").write_text("def test_x():\n    pass\n",
                                                    encoding="utf-8")
    ws.git_commit("test: add coverage")
    env = _snap_json(ws, stage="implement")
    assert env["evidence"]["artifacts"]["complete"] is True
    assert env["recovery_action"] == "verify"


def test_false_completion_and_artifacts_without_completion_are_exclusive(tmp_path):
    """C-31/C-42: the two sides can never both hold."""
    ws = Workspace(tmp_path)
    base = ws.git_base()
    ws.write_spine(base_commit=base)
    ws.write_status(exit_code=0, sentinel=1)
    ws.write_log(["TASKS-DONE"])  # sentinel, artifacts missing

    env = _snap_json(ws)
    assert env["false_completion"] is True
    assert "artifacts-without-completion" not in _forms(env)
    assert env["recovery_action"] == "retry"

    ws.write_artifact("tasks.md")
    ws.write_log(["working"])  # artifacts present, no sentinel
    env = _snap_json(ws)
    assert env["false_completion"] is False
    assert "artifacts-without-completion" in _forms(env)
    assert env["recovery_action"] != "resume"


# ---------------------------------------------------------------------------
# T007 — FR-004 derived ladder (owner: slice requirements FR-004)
# ---------------------------------------------------------------------------

def _find(env, form):
    return [i for i in env["interruptions"] if i["form"] == form]


def _done_fixture(ws):
    base = ws.git_base()
    ws.write_artifact("tasks.md")
    ws.write_spine(base_commit=base)
    ws.write_status(exit_code=0, sentinel=1)
    ws.write_log(["working", "TASKS-DONE"])
    ws.write_heartbeat()
    ws.write_pid(pid=os.getpid())
    ws.git_commit("tasks: complete")
    return base


def test_derived_spine_state_wins_over_terminal_evidence(tmp_path):
    """FR-004 rule (1): spine_state short-circuits everything else."""
    ws = Workspace(tmp_path)
    _done_fixture(ws)
    ws.write_spine(state="stalled", base_commit=ws.git("rev-parse", "HEAD").stdout.strip())

    env = _snap_json(ws)
    assert env["loop_state"] == "STALLED"
    assert env["loop_state_reason"] == "spine-stalled"
    assert env["verdict_source"] == "derived"
    assert env["recovery_action"] == "stop"

    ws.write_spine(state="reentry-required",
                   base_commit=ws.git("rev-parse", "HEAD").stdout.strip())
    env = _snap_json(ws)
    assert env["loop_state"] == "REENTRY_REQUIRED"
    assert env["loop_state_reason"] == "spine-reentry-required"
    assert env["recovery_action"] == "stop"


def test_derived_anomaly_and_failed_precede_done(tmp_path):
    """FR-004 rule (2): ANOMALY line, then exit≠0, then DONE, then INCOMPLETE."""
    ws = Workspace(tmp_path)
    ws.write_artifact("tasks.md")
    ws.write_spine()
    ws.write_status(exit_code=1, sentinel=0)
    ws.write_log(["TASKS-DONE", "ANOMALY: malformed return"])

    env = _snap_json(ws)
    assert env["loop_state"] == "ANOMALY"
    assert env["loop_state_reason"] == "anomaly-line"
    assert env["recovery_action"] == "retry"

    ws.write_log(["working"])
    env = _snap_json(ws)
    assert env["loop_state"] == "FAILED"
    assert env["loop_state_reason"] == "exit-nonzero"


def test_derived_exit_zero_done_and_incomplete(tmp_path):
    """FR-004 rule (2): exit=0 splits on sentinel x artifacts."""
    ws = Workspace(tmp_path)
    ws.write_artifact("tasks.md")
    ws.write_spine()
    ws.write_status(exit_code=0, sentinel=1)
    ws.write_log(["TASKS-DONE"])

    env = _snap_json(ws)
    assert env["loop_state"] == "DONE"
    assert env["loop_state_reason"] == "sentinel-and-artifacts"
    assert env["false_completion"] is False

    ws.write_log(["working"])  # no sentinel
    env = _snap_json(ws)
    assert env["loop_state"] == "INCOMPLETE"
    assert env["loop_state_reason"] == "exit-zero-incomplete"


def test_derived_sentinel_without_exit_record(tmp_path):
    """FR-004 rule (3): sentinel alone is completion evidence."""
    ws = Workspace(tmp_path)
    ws.write_artifact("tasks.md")
    ws.write_spine()
    ws.write_log(["TASKS-DONE"])

    env = _snap_json(ws)
    assert env["loop_state"] == "DONE"
    assert env["loop_state_reason"] == "sentinel-no-exit"

    (ws.spec_dir / "tasks.md").unlink()
    env = _snap_json(ws)
    assert env["loop_state"] == "INCOMPLETE"
    assert env["false_completion"] is True


def test_derived_dead_no_signal_and_running(tmp_path):
    """FR-004 rules (4), (6), (7)."""
    ws = Workspace(tmp_path)
    ws.write_spine(started_at=NOW - 100)
    ws.write_pid(pid=_dead_pid())

    env = _snap_json(ws)
    assert env["loop_state"] == "DEAD"
    assert env["loop_state_reason"] == "dead-no-exit-record"
    assert env["recovery_action"] == "retry"

    (ws.state_dir / ("pid-%s-%s" % (ws.line, ws.stage))).unlink()
    env = _snap_json(ws)
    assert env["loop_state"] == "NO_SIGNAL"
    assert env["loop_state_reason"] == "no-signal"

    ws.write_pid(pid=os.getpid())
    ws.write_heartbeat()
    env = _snap_json(ws)
    assert env["loop_state"] == "RUNNING"
    assert env["recovery_action"] == "watch"


def test_derived_deadline_overrun_with_live_process_is_timeout_watch(tmp_path):
    """FR-004 rule (5) + IA-17: a live TIMEOUT is watched, never killed."""
    ws = Workspace(tmp_path)
    ws.write_spine(started_at=NOW - 900, deadline=NOW - 100)
    ws.write_pid(pid=os.getpid())
    ws.write_heartbeat()

    env = _snap_json(ws)

    assert env["loop_state"] == "TIMEOUT"
    assert env["loop_state_reason"] == "deadline-overrun"
    assert env["watch_verdict"]["present"] is False
    assert env["recovery_action"] == "watch"
    assert _find(env, "deadline-overrun-live"), "live deadline overrun must be reported"

    ws.write_spine(started_at=NOW - 100, deadline=NOW + 3600)  # deadline ahead
    env = _snap_json(ws)
    assert env["loop_state"] == "RUNNING"
    assert _find(env, "deadline-overrun-live") == [], (
        "a deadline that has not passed must not be reported"
    )


def test_unwatched_detector_positive_expired_and_negative(tmp_path):
    """C-40: watchbeat missing/expired reports unwatched; fresh or sentinel does not."""
    ws = Workspace(tmp_path)
    ws.write_spine(started_at=NOW - 100)
    ws.write_pid(pid=os.getpid())
    ws.write_heartbeat()

    env = _snap_json(ws)
    assert env["loop_state"] == "RUNNING"
    assert _find(env, "unwatched"), "a running stage without a watchbeat is unwatched"
    assert env["recovery_action"] == "watch"

    ws.write_watchbeat(at=NOW, window=300)  # inside its own window
    env = _snap_json(ws)
    assert _find(env, "unwatched") == [], "fresh window must not be reported unwatched"

    ws.write_watchbeat(at=NOW - 1000, window=300)  # past window + grace(0)
    env = _snap_json(ws)
    assert _find(env, "unwatched"), "an expired watchbeat is the expired branch"

    ws.write_log(["TASKS-DONE"])  # sentinel: never unwatched
    env = _snap_json(ws)
    assert _find(env, "unwatched") == []


def test_dead_no_exit_record_is_never_done(tmp_path):
    """C-41: dead pid without an exit record is never DONE; live adds no stop."""
    ws = Workspace(tmp_path)
    ws.write_artifact("tasks.md")
    ws.write_spine(started_at=NOW - 100)
    ws.write_pid(pid=_dead_pid())

    env = _snap_json(ws)
    assert env["loop_state"] == "DEAD"
    assert _find(env, "dead-no-exit-record")
    assert env["recovery_action"] != "verify"

    ws.write_pid(pid=os.getpid())
    ws.write_heartbeat()
    env = _snap_json(ws)
    assert _find(env, "dead-no-exit-record") == [], (
        "a live process must not be reported as dead-no-exit-record"
    )
    assert env["loop_state"] != "DEAD"


def test_artifacts_without_completion_never_suggests_resume(tmp_path):
    """C-42: complete artifacts without a sentinel cannot be 'resume'."""
    ws = Workspace(tmp_path)
    ws.write_artifact("tasks.md")
    ws.write_spine()
    ws.write_status(exit_code=0, sentinel=0)
    ws.write_log(["working"])

    env = _snap_json(ws)
    assert _find(env, "artifacts-without-completion")
    assert env["false_completion"] is False
    assert env["recovery_action"] == "retry"

    ws.write_log(["TASKS-DONE"])          # sentinel + artifacts complete
    (ws.spec_dir / "tasks.md").unlink()   # but the artifact is gone
    env = _snap_json(ws)
    assert env["false_completion"] is True
    assert env["recovery_action"] != "resume"


def test_clarify_legitimate_no_change_is_verify(tmp_path):
    """C-46: no_change_allowed + no artifact change since base is commit-ready."""
    ws = Workspace(tmp_path)
    ws.stage = "clarify"  # four-piece names follow the stage under test
    ws.write_artifact("requirements.md")   # the clarify artifact, unchanged
    base = ws.git_base()                   # committed at / before the baseline
    ws.write_spine(base_commit=base)
    ws.write_status(exit_code=0, sentinel=1)
    ws.write_log(["CLARIFY-DONE"])

    env = _snap_json(ws, stage="clarify")

    assert env["loop_state"] == "DONE"
    assert env["evidence"]["artifacts"]["no_change_allowed"] is True
    assert env["uncommitted_artifacts"] == []
    assert env["recovery_action"] == "verify", (
        "a legitimate no-change stage is commit-ready, never resumed"
    )


def test_terminal_states_with_unknown_commit_baseline_never_verify(tmp_path):
    """C-46 rows 11/12: only DONE may use the row-6 verify exception."""
    ws = Workspace(tmp_path)
    ws.write_artifact("tasks.md")
    ws.write_spine(base_commit=None, started_at=NOW - 100)  # baseline unknown
    ws.write_pid(pid=_dead_pid())
    ws.write_log(["working"])

    env = _snap_json(ws)
    assert env["loop_state"] == "DEAD"
    assert env["recovery_action"] == "retry", "DEAD + unknown baseline must not verify"

    ws.write_spine(state="stalled", base_commit=None, started_at=NOW - 100)
    env = _snap_json(ws)
    assert env["loop_state"] == "STALLED"
    assert env["recovery_action"] == "stop"

    ws.write_pid(pid=os.getpid())
    ws.write_heartbeat()
    ws.write_status(exit_code=1, sentinel=0)
    ws.write_log(["ANOMALY: malformed return"])
    env = _snap_json(ws)
    assert env["loop_state"] == "ANOMALY"
    assert env["recovery_action"] == "retry", (
        "ANOMALY + unknown baseline must not fall into the row-6 verify branch"
    )


# ---------------------------------------------------------------------------
# T007 — watcher verdict tri-state and attribution (C-14/C-15/C-25)
# ---------------------------------------------------------------------------

def _write_recording_watch(ws, *, verdict="STALLED", rc=13, attribution="legacy",
                           record=None):
    body = [
        "#!/usr/bin/env bash",
    ]
    if record is not None:
        body.append('printf "%%s\\n" "$@" > %s' % json.dumps(str(record)))
    body += [
        "cat <<'WATCH_EOF'",
        "WATCH label=%s verdict=%s pid=alive heartbeat=fresh hook=na anomaly=0 "
        "sentinel=0 rc=%s reason=stalled stream=na line=%s run=run-1 stage=%s "
        "event=watcher-verdict at=1 attribution=%s"
        % (ws.line, verdict, rc, ws.line, ws.stage, attribution),
        "WATCH_EOF",
        "exit %s" % rc,
    ]
    ws.watch_script.write_text("\n".join(body) + "\n", encoding="utf-8")
    return ws.watch_script


def test_watcher_verdict_tristate(tmp_path):
    """C-25: obtained / unavailable / no active target."""
    ws = Workspace(tmp_path)
    ws.write_spine(started_at=NOW - 100, run_id="run-1")
    ws.write_pid(pid=os.getpid(), run="run-1")
    ws.write_heartbeat(run="run-1")
    script = _write_recording_watch(ws, verdict="STALLED", rc=13, attribution="own")

    env = _snap_json(ws, watch=script)
    wv = env["watch_verdict"]
    assert (wv["present"], wv["status"], wv["value_state"]) == (True, "present", "known")
    assert wv["verdict"] == "STALLED"
    assert wv["attribution"] == "own"
    assert wv["exit_code"] == 13
    assert env["loop_state"] == "STALLED"
    assert env["verdict_source"] == "watcher"

    env = _snap_json(ws)  # nonexistent watch script
    wv = env["watch_verdict"]
    assert (wv["present"], wv["status"], wv["value_state"]) == (False, "missing", "na")
    assert wv["verdict"] is None
    assert wv["reason"] == "unavailable"
    assert wv["detail"] in {
        "script-missing", "invocation-failed", "timeout", "unparseable", "usage",
        "stale-evidence", "probe-unreachable",
    }
    assert env["verdict_source"] == "derived"

    bare = Workspace(tmp_path / "bare")  # no target at all
    env = _snap_json(bare)
    wv = env["watch_verdict"]
    assert (wv["present"], wv["status"], wv["value_state"]) == (False, "na", "na")
    assert wv["verdict"] is None
    assert wv["reason"] is None


def test_watcher_attribution_forms(tmp_path):
    """C-14: provable attribution / legacy compatibility / stale never calls."""
    ws = Workspace(tmp_path)
    args_file = tmp_path / "argv.txt"
    ws.write_spine(started_at=NOW - 100, run_id="run-1")
    ws.write_pid(pid=os.getpid(), run="run-1")
    ws.write_status(run="run-1")
    ws.write_heartbeat(run="run-1")
    ws.write_registry(stage="tasks", run_id="run-1")
    script = _write_recording_watch(ws, attribution="own", record=args_file)

    env = _snap_json(ws, watch=script)
    recorded = args_file.read_text(encoding="utf-8").split()
    assert "--run-id" in recorded and "run-1" in recorded, (
        "provable attribution must pass --line-id/--run-id"
    )
    assert "--line-id" in recorded
    assert env["watch_verdict"]["attribution"] == "own"

    args_file.unlink()
    ws.spine.unlink()
    ws.registry_dir.joinpath("%s.json" % ws.line).unlink()
    ws.write_spine(started_at=NOW - 100)  # run_id unknown, no stale signals
    _write_recording_watch(ws, attribution="legacy", record=args_file)
    env = _snap_json(ws, watch=script)
    recorded = args_file.read_text(encoding="utf-8").split()
    assert "--run-id" not in recorded, "unprovable attribution uses the legacy form"
    assert env["watch_verdict"]["attribution"] == "legacy"

    args_file.unlink()
    ws.write_pid(pid=os.getpid(), run="run-other")  # stale run mismatch
    ws.write_spine(started_at=NOW - 100, run_id="run-1")
    env = _snap_json(ws, watch=script)
    assert not args_file.exists(), "stale evidence must prevent the watcher call"
    wv = env["watch_verdict"]
    assert (wv["present"], wv["reason"], wv["detail"]) == (False, "unavailable", "stale-evidence")
    assert _stale(env, "pid"), "the foreign-run pid must be listed as stale"


# ---------------------------------------------------------------------------
# T007 — IA-14 candidate order, attempt/salvage gates (C-46..C-49)
# ---------------------------------------------------------------------------

def test_done_with_unknown_commit_baseline_goes_verify(tmp_path):
    """C-46 row 6 / C-57: DONE + unknown baseline -> verify, never a HEAD guess."""
    ws = Workspace(tmp_path)
    ws.write_artifact("tasks.md")
    ws.write_spine(base_commit=None)
    ws.write_status(exit_code=0, sentinel=1)
    ws.write_log(["TASKS-DONE"])

    env = _snap_json(ws)

    assert env["evidence"]["commits"]["value_state"] == "unknown"
    assert env["loop_state"] == "DONE"
    assert env["recovery_action"] == "verify"
    assert env["recovery_reason"] == "commit-baseline-unknown"


def test_resume_needs_sentinel_complete_artifacts_and_known_attempt(tmp_path):
    """C-46 row 8 + C-47: uncommitted DONE resumes; unknown attempt may not."""
    ws = Workspace(tmp_path)
    base = ws.git_base()
    ws.write_artifact("tasks.md")
    ws.write_spine(base_commit=base, attempt=1, retry_limit=2)
    ws.write_log(["TASKS-DONE"])  # sentinel, no commit -> not commit-ready

    env = _snap_json(ws)
    assert env["loop_state"] == "DONE"
    assert env["uncommitted_artifacts"] == ["tasks.md"]
    assert env["recovery_action"] == "resume"

    ws.write_spine(base_commit=base, attempt=None, retry_limit=2)
    env = _snap_json(ws)
    assert env["recovery_action"] != "resume", "unknown attempt must not resume"
    assert "attempt-unknown" in env["recovery_decision"]["blocked_by"]


def test_attempt_limit_turns_retry_into_stop(tmp_path):
    """C-47: attempt >= retry_limit forces stop for retry/resume/stop candidates."""
    ws = Workspace(tmp_path)
    base = ws.git_base()
    ws.write_artifact("tasks.md")
    ws.write_spine(base_commit=base, attempt=2, retry_limit=2)
    ws.write_status(exit_code=0, sentinel=0)
    ws.write_log(["working"])  # complete artifacts, no sentinel -> row 9 retry

    env = _snap_json(ws)
    assert env["recovery_action"] == "stop"
    assert env["recovery_reason"] == "attempts-exhausted"


def test_salvage_gate_requires_a_complete_record(tmp_path):
    """C-48: incomplete salvage never resumes; a complete record does."""
    ws = Workspace(tmp_path)
    base = ws.git_base()
    ws.write_artifact("tasks.md")
    ws.write_spine(base_commit=base, attempt=1, retry_limit=2,
                   salvage="accepted")  # no evidence, no at -> incomplete
    ws.write_log(["working"])

    env = _snap_json(ws)
    assert env["recovery_action"] != "resume"
    assert env["recovery_action"] == "retry"

    ws.write_spine(base_commit=base, attempt=1, retry_limit=2,
                   salvage="accepted", salvage_evidence="notes/salvage.md",
                   salvage_at="2026-10-21T10:00:00Z")
    env = _snap_json(ws)
    assert env["recovery_action"] == "resume"


def test_stalled_with_complete_artifacts_stays_stop(tmp_path):
    """C-46 rows 8-10 MUST NOT re-judge STALLED/REENTRY_REQUIRED (row 11)."""
    ws = Workspace(tmp_path)
    base = _done_fixture(ws)
    ws.write_spine(state="stalled", base_commit=base)

    env = _snap_json(ws)
    assert env["evidence"]["artifacts"]["complete"] is True
    assert env["loop_state"] == "STALLED"
    assert env["recovery_action"] == "stop"

    ws.write_spine(state="reentry-required", base_commit=base)
    env = _snap_json(ws)
    assert env["loop_state"] == "REENTRY_REQUIRED"
    assert env["recovery_action"] == "stop"


def test_false_completion_with_stalled_is_stop_not_retry(tmp_path):
    """C-31/C-42: row 11 also outranks the false_completion retry default."""
    ws = Workspace(tmp_path)
    ws.write_spine(state="stalled")
    ws.write_status(exit_code=0, sentinel=1)
    ws.write_log(["TASKS-DONE"])  # sentinel, no artifact

    env = _snap_json(ws)

    assert env["false_completion"] is True
    assert env["loop_state"] == "STALLED"
    assert env["recovery_action"] == "stop"
    assert env["recovery_reason"] != "false-completion"


def test_trailing_anomaly_line_with_live_process_is_watch_not_done(tmp_path):
    """FR-004 sentinel rule: an earlier sentinel followed by ANOMALY: is not DONE."""
    ws = Workspace(tmp_path)
    ws.write_artifact("tasks.md")
    ws.write_spine(started_at=NOW - 100)
    ws.write_pid(pid=os.getpid())
    ws.write_heartbeat()
    ws.write_log(["TASKS-DONE", "ANOMALY: subagent returned malformed tasks"])

    env = _snap_json(ws)

    assert env["evidence"]["log"]["sentinel_present"] is False
    assert env["evidence"]["log"]["anomaly"] is True
    assert env["loop_state"] == "RUNNING"
    assert env["recovery_action"] == "watch"
    assert env["false_completion"] is False


def test_stale_signals_are_excluded_without_changing_the_action(tmp_path):
    """C-43: stale is listed and excluded, never a reason to change the action."""
    ws = Workspace(tmp_path)
    _done_fixture(ws)

    baseline = _snap_json(ws)
    assert baseline["recovery_action"] == "verify"
    assert baseline["stale_signals"] == []

    ws.write_heartbeat(run="run-other")  # foreign run -> stale
    after = _snap_json(ws)

    assert _stale(after, "heartbeat"), "the foreign-run heartbeat must be listed"
    assert after["recovery_action"] == baseline["recovery_action"], (
        "mere staleness must not change the suggested action (isolation is 065c)"
    )
    assert after["loop_state"] == baseline["loop_state"]


# ---------------------------------------------------------------------------
# T007 — probe shapes and local-evidence isolation (C-11/C-44)
# ---------------------------------------------------------------------------

def _sig(**over):
    base = {"status": "missing", "value_state": "na", "path": None}
    base.update(over)
    return base


def _probe_evidence(**over):
    block = {
        "evidence_source": "probe",
        "pid": _sig(), "status": _sig(), "log": _sig(), "heartbeat": _sig(),
        "watchbeat": _sig(),
        "hook": {"status": "na", "value_state": "na", "path": None,
                 "observed_at": None},
        "artifacts": {"status": "missing", "value_state": "na", "stage": None,
                      "complete": None, "commit_required": None,
                      "no_change_allowed": None, "items": []},
        "commits": {"status": "missing", "value_state": "na", "base": None,
                    "pathspec": [], "commits": [], "touching": None},
    }
    block.update(over)
    return block


def _probe_watch(**over):
    base = {"present": False, "status": "na", "value_state": "na",
            "verdict": None, "reason": None, "exit_code": None,
            "attribution": None, "detail": None}
    base.update(over)
    return base


def _probe_payload(watch=None, evidence=None, **over):
    payload = {
        "schema_version": 1,
        "line_id": LINE,
        "watch_verdict": watch or _probe_watch(),
        "evidence": evidence or _probe_evidence(),
    }
    payload.update(over)
    return payload


def _probe_snapshot(ws, payload, *extra):
    path = ws.root / "probe.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    proc = _run(
        ["--action", "snapshot", "--line-id", ws.line, "--probe", str(path)]
        + [str(x) for x in extra],
        env=ws.env,
    )
    return path, proc


def _done_probe_evidence():
    return _probe_evidence(
        pid=_sig(status="present", value_state="known", pid=os.getpid(),
                 start="1", at=NOW, alive=True, identity="ok", attribution="own"),
        status=_sig(status="present", value_state="known", exit_code=0, at=NOW,
                    sentinel=1, run_id="run-1", stage="tasks", event="status",
                    legacy=None, attribution="own"),
        log=_sig(status="present", value_state="known", last_line="TASKS-DONE",
                 sentinel_present=True, sentinel="TASKS-DONE", anomaly=False),
        heartbeat=_sig(status="present", value_state="known", at=NOW,
                       mtime_ns=NOW * 10 ** 9, fresh=True, attribution="own"),
        artifacts={"status": "present", "value_state": "known", "stage": "tasks",
                   "complete": True, "commit_required": True,
                   "no_change_allowed": False,
                   "items": [{"path": "tasks.md", "required": True,
                              "status": "present", "size": 12}]},
        commits={"status": "present", "value_state": "known", "base": "abc1234",
                 "pathspec": ["tasks.md"], "commits": [], "touching": True},
    )


def test_probe_shape_a_consumes_verdict_verbatim(tmp_path):
    """C-11(a): probe evidence is consumed verbatim; a watcher verdict is literal."""
    ws = Workspace(tmp_path)
    payload = _probe_payload(watch=_probe_watch(
        present=True, status="present", value_state="known", verdict="STALLED",
        reason="stalled", exit_code=13, attribution="own"))

    path, proc = _probe_snapshot(ws, payload)

    assert proc.returncode == 0, proc.stderr
    env = json.loads(proc.stdout)
    assert env["paths"]["probe"] == str(path)
    assert env["evidence"]["evidence_source"] == "probe"
    assert env["verdict_source"] == "watcher"
    assert env["loop_state"] == "STALLED"
    assert env["watch_verdict"]["verdict"] == "STALLED"
    assert env["recovery_action"] == "stop"


def test_probe_evidence_isolated_from_local_signals(tmp_path):
    """C-11(a)/C-13: probe evidence wins; local evidence is never mixed in."""
    ws = Workspace(tmp_path)
    ws.write_log(["ANOMALY: local evidence must not leak"])
    ws.write_status(exit_code=1, sentinel=0)

    path, proc = _probe_snapshot(ws, _probe_payload(evidence=_done_probe_evidence()))

    assert proc.returncode == 0, proc.stderr
    env = json.loads(proc.stdout)
    assert env["evidence"]["evidence_source"] == "probe"
    assert env["evidence"]["log"]["last_line"] == "TASKS-DONE"
    assert env["loop_state"] == "DONE"
    assert env["verdict_source"] == "derived"
    assert env["recovery_action"] == "verify"


def test_probe_shape_b_unreachable_is_stalled_stop(tmp_path):
    """C-11(b)/C-44: reachable=false proves unreachability only."""
    ws = Workspace(tmp_path)
    payload = {"schema_version": 1, "reachable": False, "reason": "ssh-255"}

    path, proc = _probe_snapshot(ws, payload)

    assert proc.returncode == 0, proc.stderr
    env = json.loads(proc.stdout)
    assert env["loop_state"] == "STALLED"
    assert env["loop_state_reason"] == "remote-unreachable"
    assert env["recovery_action"] == "stop"
    assert _find(env, "remote-unreachable"), "the form must be reported"
    for key in ("pid", "status", "log", "heartbeat", "watchbeat",
                "artifacts", "commits"):
        assert env["evidence"][key]["status"] == "missing", key
    assert env["paths"]["probe"] == str(path)


def test_sc001_accident_replay_suggests_resume_or_retry(tmp_path):
    """SC-001: complete-but-uncommitted, exit=1, no sentinel, no watcher."""
    ws = Workspace(tmp_path)
    base = ws.git_base()
    ws.write_artifact("tasks.md")           # artifacts complete
    ws.write_spine(base_commit=base)
    ws.write_status(exit_code=1, sentinel=0)  # failed, uncommitted
    ws.write_log(["working"])               # no sentinel

    env = _snap_json(ws)

    assert env["loop_state"] == "FAILED"
    assert env["interruptions"], "the replay must surface at least one interruption"
    assert env["recovery_action"] in {"resume", "retry"}
    assert env["missing_artifacts"] == []


# ==== END OF FILE ====
