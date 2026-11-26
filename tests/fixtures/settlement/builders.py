"""Deterministic settlement fixtures for spec 106 (T005).

Rule owner: ``shared/definitions/superagent-definitions.md`` § Termination. Record
shapes: ``.specify/specs/106-background-silent-failure/data-model.md`` E2 (attempt),
E3 (termination record), E5 (settlement claim) and E8 (carrier evidence map).

Design rules for every fixture here:

* Deterministic — fixed timestamps and pids; no fixed ``sleep`` anywhere. Liveness
  fixtures hold a child process alive on an open stdin pipe and the caller polls
  ``/proc`` facts, never wall-clock waits.
* One attempt per label, one file per record — matching the feature's per-entry
  file layout (Concurrent Development Safety).
* ``tmp_path`` builders for the six terminal classes and the live / half-dead
  variants; the static directories named by tasks.md (``c1-state/``,
  ``c3-report/``, ``legacy/logs/``, ``versioned/logs/``) carry committed samples.

Entry points used by the contract tests are listed in ``__all__``.
"""

from __future__ import annotations

import datetime
import json
import os
import subprocess
import sys
import time
from pathlib import Path

FIXTURE_ROOT = Path(__file__).resolve().parent

DEAD_PID = 99999999
STARTED_AT = "2026-01-01T00:00:00Z"
ENDED_AT = "2026-01-01T00:01:00Z"
CONTRACT_POINTER = "shared/definitions/superagent-definitions.md § Termination"

C2_HEADER = ("label", "role", "dispatch_duty", "workspace", "parent")
C3_HEADER = C2_HEADER + ("end_state", "evidence")

__all__ = [
    "C2_HEADER",
    "C3_HEADER",
    "CONTRACT_POINTER",
    "DEAD_PID",
    "ENDED_AT",
    "FIXTURE_ROOT",
    "STARTED_AT",
    "attempt_payload",
    "c1_live",
    "c2_anomaly",
    "c2_cancelled",
    "c2_completed",
    "c2_failed",
    "c2_live",
    "c2_missing_start",
    "c2_pid_reuse",
    "c2_running",
    "c2_silent_end",
    "c2_unreadable",
    "c2_zombie",
    "c3_live",
    "c4_live",
    "make_roots",
    "now_iso",
    "pid_start_ticks",
    "spawn_live_process",
    "spawn_zombie_holder",
    "stop_live_process",
    "write_attempt",
    "write_c1_stage",
    "write_claim",
    "write_end",
    "write_live_log",
    "write_report",
    "write_status",
]


# --------------------------------------------------------------------------- #
# primitives
# --------------------------------------------------------------------------- #
def make_roots(tmp_path: Path):
    """Create the three required roots and return ``(state, teams, logs)``."""
    state = tmp_path / "state"
    teams = tmp_path / "teams"
    logs = tmp_path / "logs"
    for path in (state, teams, logs):
        path.mkdir(parents=True, exist_ok=True)
    return state, teams, logs


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _write_json(path: Path, payload: dict) -> Path:
    return _write(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def attempt_payload(label: str, **overrides) -> dict:
    payload = {
        "settlement_version": 1,
        "attempt_id": label,
        "carrier": "c2-subprocess",
        "parent_identity": "root",
        "started_at": STARTED_AT,
        "contract": CONTRACT_POINTER,
    }
    payload.update(overrides)
    return payload


def write_attempt(logs: Path, label: str, **overrides) -> Path:
    return _write_json(logs / f"{label}.attempt", attempt_payload(label, **overrides))


def write_end(logs: Path, label: str, **fields) -> Path:
    payload = {
        "settlement_version": 1,
        "attempt_id": label,
        "exit": 0,
        "ended_at": ENDED_AT,
    }
    payload.update(fields)
    return _write_json(logs / f"{label}.end", payload)


def write_claim(
    logs: Path,
    label: str,
    *,
    value: str,
    evidence=(),
    mechanism=None,
    version=1,
    claimed_at=ENDED_AT,
    **extra,
) -> Path:
    payload = {
        "attempt_id": label,
        "surface": "attempt-file",
        "value": value,
        "evidence": list(evidence),
        "claimed_at": claimed_at,
    }
    if version is not None:
        payload["settlement_version"] = version
    if mechanism is not None:
        payload["mechanism"] = mechanism
    payload.update(extra)
    return _write_json(logs / f"{label}.settlement", payload)


def write_status(logs: Path, label: str, exit_code: int) -> Path:
    return _write(logs / f"{label}.status", f"{label} exit={exit_code}\n")


def write_live_log(logs: Path, label: str, lines) -> Path:
    return _write(logs / f"{label}.live.log", "\n".join(lines) + "\n")


def write_report(teams: Path, slug: str, stamp: str, header, rows) -> Path:
    body = [
        "# Team Run Report: %s" % slug,
        "",
        "## Execution Detail",
        "",
        "| " + " | ".join(header) + " |",
        "|" + "|".join("---" for _ in header) + "|",
    ]
    for row in rows:
        body.append("| " + " | ".join(str(cell) for cell in row) + " |")
    body += ["", "## Verification", "", "Settlement coverage: see the settlement owner.", ""]
    return _write(teams / slug / "runs" / f"{stamp}-report.md", "\n".join(body))


# --------------------------------------------------------------------------- #
# process / liveness helpers (event-based; no fixed sleep)
# --------------------------------------------------------------------------- #
def spawn_live_process() -> subprocess.Popen:
    """A child that stays alive while its stdin pipe is open (no sleep involved)."""
    return subprocess.Popen(
        [sys.executable, "-c", "import sys\nsys.stdin.read()"],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
    )


def stop_live_process(proc: subprocess.Popen) -> None:
    if proc.poll() is not None:
        return
    try:
        if proc.stdin is not None:
            proc.stdin.close()
    except OSError:
        pass
    proc.terminate()
    try:
        proc.wait(timeout=15)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=15)


def pid_start_ticks(pid: int):
    """Field 22 of /proc/<pid>/stat (starttime); ``None`` where /proc is unavailable."""
    try:
        stat = Path("/proc/%d/stat" % pid).read_text(encoding="utf-8")
    except OSError:
        return None
    close = stat.rfind(")")
    if close < 0:
        return None
    fields = stat[close + 2 :].split()
    if len(fields) < 20:
        return None
    try:
        return int(fields[19])
    except ValueError:
        return None


def now_iso() -> str:
    """Current UTC time in the attempt-record stamp shape (live pid-less fixtures)."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


ZOMBIE_HOLDER = (
    "import os, sys\n"
    "marker = sys.argv[1]\n"
    "pid = os.fork()\n"
    "if pid == 0:\n"
    "    os._exit(0)\n"
    "with open(marker, 'w') as handle:\n"
    "    handle.write(str(pid))\n"
    "sys.stdin.read()\n"
)


def _poll(predicate, timeout=60.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.02)
    return False


def spawn_zombie_holder(workdir: Path):
    """Hold an unreaped zombie child alive; returns ``(holder_proc, zombie_pid)``.

    The child exits immediately; the holder never waits, so the pid stays a zombie
    (state ``Z``) until the holder is stopped. Readiness is polled from ``/proc`` —
    a fact, never a fixed sleep.
    """
    workdir.mkdir(parents=True, exist_ok=True)
    marker = workdir / "zombie.pid"
    proc = subprocess.Popen(
        [sys.executable, "-c", ZOMBIE_HOLDER, str(marker)],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    assert _poll(lambda: marker.exists() and marker.stat().st_size > 0), (
        "zombie holder never wrote its pid"
    )

    def is_zombie() -> bool:
        try:
            text = Path("/proc/%s/stat" % marker.read_text(encoding="utf-8").strip()).read_text(
                encoding="utf-8"
            )
        except OSError:
            return False
        close = text.rfind(")")
        return close >= 0 and text[close + 2 : close + 3] == "Z"

    assert _poll(is_zombie), "the forked child never reached the zombie state"
    return proc, int(marker.read_text(encoding="utf-8").strip())


# --------------------------------------------------------------------------- #
# C1 — driver stage four-piece
# --------------------------------------------------------------------------- #
def _spine(state: Path, line: str, run_id: str, stage: str) -> Path:
    body = [
        "# Line State — %s" % line,
        "",
        "<!-- loop-state:begin -->",
        "spine_state: running",
        "run_id: %s" % run_id,
        "slice: %s" % line,
        "stage: %s" % stage,
        "attempt: 1",
        "<!-- loop-state:end -->",
        "",
    ]
    return _write(state / f"{line}.md", "\n".join(body))


def write_c1_stage(
    state: Path,
    *,
    line: str = "demo-line",
    stage: str = "implement",
    run_id: str = "r-fixture-c1",
    exit_code=0,
    sentinel=1,
    pid=DEAD_PID,
    sidecar: bool = True,
    started_at: str = STARTED_AT,
    log_lines=("STAGE-DONE",),
    heartbeat: bool = True,
) -> str:
    stem = f"{line}-{stage}"
    _spine(state, line, run_id, stage)
    if sidecar:
        _write_json(
            state / ("prompt-%s.md.meta.json" % stem),
            {
                "line_id": line,
                "stage": stage,
                "started_at": started_at,
                "role_edge": {
                    "parent_identity": run_id,
                    "child_label": stem,
                    "role_declaration": "subagent",
                    "dispatch_duty": "not-granted",
                    "depth_position": 1,
                    "authority_ref": "none",
                    "return_channel": "structured return + evidence pointer",
                },
            },
        )
    if pid is not None:
        _write(state / f"pid-{stem}", f"{pid}\n")
    if exit_code is not None:
        _write(
            state / f"status-{stem}",
            "exit=%d at=1 sentinel=%d line=%s stage=%s event=status progress=stream detached=0\n"
            % (exit_code, sentinel, line, stage),
        )
    _write(state / f"log-{stem}.log", "\n".join(log_lines) + "\n")
    if heartbeat:
        _write(state / f"heartbeat-{stem}.log", "1\n")
    return stem


# --------------------------------------------------------------------------- #
# C2 — the six terminal classes and the half-dead / unreadable variants
# --------------------------------------------------------------------------- #
def c2_completed(logs: Path, label: str = "done", *, mechanism="return-record", version=1) -> str:
    write_attempt(logs, label)
    write_end(logs, label, exit=0)
    write_status(logs, label, 0)
    write_live_log(logs, label, ["step one", "step two", "done"])
    _write(logs / f"{label}.return.txt", "returned artifact\n")
    write_claim(
        logs,
        label,
        value="completed",
        mechanism=mechanism,
        evidence=[f"{label}.return.txt"],
        version=version,
    )
    return label


def c2_failed(logs: Path, label: str = "failed") -> str:
    write_attempt(logs, label)
    write_end(logs, label, exit=2, signal=None)
    write_status(logs, label, 2)
    write_live_log(logs, label, ["step one", "boom"])
    return label


def c2_anomaly(logs: Path, label: str = "anomaly") -> str:
    write_attempt(logs, label)
    write_end(logs, label, exit=0)
    write_status(logs, label, 0)
    write_live_log(logs, label, ["step one", "ANOMALY: demo anomaly line"])
    return label


def c2_cancelled(logs: Path, label: str = "cancelled") -> str:
    write_attempt(logs, label)
    write_live_log(logs, label, ["step one"])
    write_claim(logs, label, value="cancelled", evidence=[])
    return label


def c2_running(logs: Path, label: str = "running"):
    proc = spawn_live_process()
    ticks = pid_start_ticks(proc.pid)
    overrides = {"pid": proc.pid}
    if ticks is not None:
        overrides["pid_start_ticks"] = ticks
    write_attempt(logs, label, **overrides)
    write_live_log(logs, label, ["step one"])
    return proc


def c2_silent_end(logs: Path, label: str = "silent") -> str:
    write_attempt(logs, label, pid=DEAD_PID)
    write_live_log(logs, label, ["step one", "step two"])
    return label


def c2_pid_reuse(logs: Path, label: str = "reused"):
    """A live pid whose recorded start ticks differ — pid reuse, not liveness."""
    proc = spawn_live_process()
    ticks = pid_start_ticks(proc.pid)
    overrides = {"pid": proc.pid}
    if ticks is not None:
        overrides["pid_start_ticks"] = ticks + 1
    write_attempt(logs, label, **overrides)
    write_live_log(logs, label, ["step one"])
    return proc


def c2_unreadable(logs: Path, label: str = "broken") -> str:
    _write(logs / f"{label}.attempt", "{not valid json\n")
    return label


def c2_missing_start(logs: Path, label: str = "claim-only") -> str:
    """A claimed attempt with no start record — the ``start-record-missing`` case."""
    write_claim(logs, label, value="completed", mechanism="return-record", evidence=[])
    return label


# --------------------------------------------------------------------------- #
# Live / zombie reverse fixtures (T024) — a live subject is never silent-end
# --------------------------------------------------------------------------- #
def c1_live(state: Path, *, line: str = "live-line", stage: str = "implement"):
    """C1 four-piece with a live child pid and no status record → ``running``."""
    proc = spawn_live_process()
    write_c1_stage(
        state,
        line=line,
        stage=stage,
        pid=proc.pid,
        exit_code=None,
        log_lines=("step one",),
    )
    return proc


def c2_live(logs: Path, label: str = "live"):
    """A long-silent C2 attempt whose recorded pid stays alive → ``running``."""
    proc = spawn_live_process()
    overrides = {"pid": proc.pid}
    ticks = pid_start_ticks(proc.pid)
    if ticks is not None:
        overrides["pid_start_ticks"] = ticks
    write_attempt(logs, label, **overrides)
    write_live_log(logs, label, ["step one"])
    return proc


def c2_zombie(logs: Path, label: str = "zombie", *, workdir=None):
    """A recorded pid that is a zombie — the subject is gone, so ``silent-end``."""
    base = Path(workdir) if workdir is not None else logs.parent / "zombie-holder"
    holder, zombie_pid = spawn_zombie_holder(base)
    write_attempt(logs, label, pid=zombie_pid)
    write_live_log(logs, label, ["step one"])
    return holder


def c3_live(logs: Path, label: str = "live-seat", *, wait_deadline_s: int = 3600) -> str:
    """A pid-less C3 seat inside its declared wait deadline → ``running``."""
    write_attempt(
        logs,
        label,
        carrier="c3-team-seat",
        started_at=now_iso(),
        wait_deadline_s=wait_deadline_s,
    )
    return label


def c4_live(logs: Path, label: str = "live-native", *, wait_deadline_s: int = 3600) -> str:
    """A pid-less C4 native attempt inside its declared wait deadline → ``running``."""
    write_attempt(
        logs,
        label,
        carrier="c4-native",
        started_at=now_iso(),
        wait_deadline_s=wait_deadline_s,
    )
    return label
