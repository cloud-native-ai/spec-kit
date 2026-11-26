"""Contract tests: carrier surfaces settle from evidence (spec 106, US2 / T009).

Rule owner: ``shared/definitions/superagent-definitions.md`` § Termination. Pinning
clauses: ``contracts/carrier-conformance.contract.md`` C-14…C-22.

What this pins

* C-14 (T010) — ``dispatch.sh`` writes the additive ``<label>.attempt`` before the CLI
  launches and ``<label>.end`` on normal exit and on TERM/INT/HUP traps; the ``.status``
  line stays byte-compatible with its baseline reader.
* C-15 (T011) — C2 settles from evidence: SIGKILL silent death → ``silent-end`` (exit 0),
  a trapped signal → ``failed``, exit 0 without a declaration → ``failed`` (incomplete),
  a live pid → ``running`` (never ``silent-end``), unreadable evidence → ``unknown`` (exit 2).
* C-16 (T012) — the report contract's 7-column header with ``end_state`` / ``evidence``,
  the 5-column legacy carve-out, ``settlement-unrecorded`` / ``settlement-unbacked`` and
  the seat start record before hand-off.
* C-17 (T013) — the C4 native attempt-record / five-element / wait-deadline /
  foreground-terminal / virtual-pointer obligations.
* C-18 (T014) — the written virtual exclusion in § Three Execution Modes.
* C-19 / C-20 (T015) — per-value dispositions in the recipes and the Recipe 7 result
  contract (each validator settled; a missing status/verdict is ``failed`` (incomplete)
  and re-asked; it never disappears from the wave).
* C-21 (T016) — the observer stays optional and is never the only settlement carrier.
* C-22 (T017) — every dispatch entry and dispatch-duty definition references the same
  settlement owner, and no dispatch surface carries a second value table.

Red-first (Constitution IV): at T009 the dispatch.sh settlement records and every pinned
owner sentence are absent, so the carrier legs fail on their own named assertions — never
on an import or collection error. The engine legs (C2/C3 settlement) already pass because
US1 delivered the judgment face.

Real-process tests drive the shipped ``dispatch.sh`` with a deterministic fake CLI and a
passthrough stream filter; synchronization is fact-based polling (an event appears or a pid
disappears), never a fixed ``sleep``.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import signal
import subprocess
import sys
import time
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "role-edge-check.py"
DISPATCH = REPO_ROOT / "skills" / "internal" / "create-team" / "scripts" / "dispatch.sh"
BUILDERS_PATH = REPO_ROOT / "tests" / "fixtures" / "settlement" / "builders.py"

OWNER = REPO_ROOT / "shared" / "definitions" / "superagent-definitions.md"
SUBAGENT_DEFS = REPO_ROOT / "shared" / "definitions" / "subagent-definitions.md"
RECIPES = REPO_ROOT / "shared" / "workflow" / "external-dispatch-recipes.md"
RUN_AGENT = REPO_ROOT / "skills" / "internal" / "run-agent" / "SKILL.md"
CREATE_TEAM = REPO_ROOT / "skills" / "internal" / "create-team" / "SKILL.md"
RUN_TEAM = REPO_ROOT / "skills" / "internal" / "run-team" / "SKILL.md"
DRIVER_SKILL = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "SKILL.md"
AGENTS_CMD = REPO_ROOT / "templates" / "commands" / "agents.md"
TEAM_CMD = REPO_ROOT / "templates" / "commands" / "team.md"
COORDINATORS = tuple(
    REPO_ROOT / "agents" / ("sdd-%s-coordinator.agent.md" % stage)
    for stage in ("plan", "task", "implement", "review")
)

SETTLEMENT_VALUES = (
    "completed",
    "failed",
    "anomaly",
    "cancelled",
    "running",
    "silent-end",
    "unknown",
)
OWNER_PATH = "superagent-definitions.md"
OWNER_SECTION = "§ Termination"

FAKE_CLI = '''#!/usr/bin/env python3
import os
import pathlib
import sys

mode = os.environ.get("FAKE_CLI_MODE", "done")
state = pathlib.Path(os.environ["FAKE_CLI_STATE"])
(state / "cli.pid").write_text(str(os.getpid()), encoding="utf-8")
print("step one", flush=True)
if mode == "done":
    print("all done", flush=True)
    sys.exit(0)
if mode == "fail":
    print("boom", flush=True)
    sys.exit(int(os.environ.get("FAKE_CLI_RC", "2")))
if mode == "block":
    sys.stdin.read()
    sys.exit(0)
sys.exit(9)
'''

PASSTHROUGH_FILTER = '''import sys

for line in sys.stdin:
    sys.stdout.write(line)
    sys.stdout.flush()
'''


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _load_builders():
    assert BUILDERS_PATH.is_file(), (
        "fixture builders missing: tests/fixtures/settlement/builders.py (T005)"
    )
    spec = importlib.util.spec_from_file_location("settlement_builders", str(BUILDERS_PATH))
    assert spec and spec.loader, "builders module not loadable"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_module(name: str, path: Path):
    assert path.is_file(), f"module missing: {path.relative_to(REPO_ROOT)}"
    spec = importlib.util.spec_from_file_location(name, str(path))
    assert spec and spec.loader, f"module not loadable: {path}"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _read(path: Path) -> str:
    assert path.is_file(), f"missing required file: {path.relative_to(REPO_ROOT)}"
    return path.read_text(encoding="utf-8")


def _norm(text: str) -> str:
    return " ".join(text.split())


def _sections(text: str) -> dict:
    sections = {}
    current = None
    body = []
    for line in text.splitlines():
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(body)
            current = line.strip()
            body = []
            continue
        if current is not None:
            body.append(line)
    if current is not None:
        sections[current] = "\n".join(body)
    return sections


def run_settle(state, teams, logs, *extra):
    proc = subprocess.run(
        [
            sys.executable,
            str(ENGINE),
            "--action",
            "settle",
            "--state-dir",
            str(state),
            "--teams-dir",
            str(teams),
            "--logs-dir",
            str(logs),
            "--registry-dir",
            str(Path(state).parent / "no-such-registry"),
            *[str(item) for item in extra],
        ],
        capture_output=True,
        text=True,
        timeout=180,
    )
    payload = None
    if proc.stdout.strip():
        try:
            payload = json.loads(proc.stdout)
        except json.JSONDecodeError:
            payload = None
    return proc, payload


def _finding(payload, attempt_id):
    assert payload is not None, "settle produced no JSON payload"
    for row in payload["findings"]:
        if row["attempt_id"] == attempt_id:
            return row
    raise AssertionError(f"finding missing for {attempt_id}: {payload['findings']}")


def _poll_until(predicate, timeout=60.0):
    """Fact-based event polling — observe an artifact / pid fact, never a fixed sleep."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.02)
    return False


def _poll_json(path: Path, timeout=60.0):
    """Poll until ``path`` holds a complete JSON object (never a half-written record)."""
    seen = {}

    def ready():
        try:
            seen["payload"] = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return False
        return True

    assert _poll_until(ready, timeout), f"{path.name} was never written as a complete record"
    return seen["payload"]


def _pid_gone(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return True
    except PermissionError:
        return False
    stat = Path("/proc/%d/stat" % pid)
    try:
        text = stat.read_text(encoding="utf-8")
    except OSError:
        return True
    close = text.rfind(")")
    return close >= 0 and text[close + 2 : close + 3] == "Z"


def _tree_hashes(root: Path) -> dict:
    hashes = {}
    for path in sorted(root.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            hashes[path.relative_to(root).as_posix()] = hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
    return hashes


# --------------------------------------------------------------------------- #
# C2 — real dispatch.sh runs with a deterministic fake CLI
# --------------------------------------------------------------------------- #
class DispatchRun:
    def __init__(self, tmp_path: Path, label: str, mode: str):
        self.tmp_path = tmp_path
        self.label = label
        self.fake_state = tmp_path / "fake-cli"
        self.fake_state.mkdir(exist_ok=True)
        self.logs = tmp_path / "dispatch-logs"
        self.state = tmp_path / "engine-state"
        self.teams = tmp_path / "teams"
        self.work = tmp_path / "work"
        for path in (self.logs, self.state, self.teams, self.work):
            path.mkdir(parents=True, exist_ok=True)

        cli = tmp_path / "fake_cli.py"
        cli.write_text(FAKE_CLI, encoding="utf-8")
        cli.chmod(0o755)
        stream_filter = tmp_path / "passthrough_filter.py"
        stream_filter.write_text(PASSTHROUGH_FILTER, encoding="utf-8")
        prompt = tmp_path / "prompt.md"
        prompt.write_text("do the task\n", encoding="utf-8")

        env = dict(os.environ)
        env.update(
            {
                "DISPATCH_CLI": str(cli),
                "DISPATCH_CLI_FLAGS": "",
                "DISPATCH_FILTER": str(stream_filter),
                "DISPATCH_LOG_DIR": str(self.logs),
                "DISPATCH_PARENT": "root",
                "FAKE_CLI_MODE": mode,
                "FAKE_CLI_STATE": str(self.fake_state),
            }
        )
        self.proc = subprocess.Popen(
            ["bash", str(DISPATCH), label, str(self.work), str(prompt)],
            env=env,
            cwd=str(tmp_path),
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True,
        )

    @property
    def attempt_path(self) -> Path:
        return self.logs / f"{self.label}.attempt"

    @property
    def end_path(self) -> Path:
        return self.logs / f"{self.label}.end"

    @property
    def status_path(self) -> Path:
        return self.logs / f"{self.label}.status"

    def wait_attempt(self) -> dict:
        """C-14: the attempt record must exist (complete) before the CLI launches."""
        return _poll_json(self.attempt_path)

    def wait_cli_pid(self) -> int:
        marker = self.fake_state / "cli.pid"
        assert _poll_until(marker.exists), "fake CLI never started"
        return int(marker.read_text(encoding="utf-8").strip())

    def settle(self):
        return run_settle(self.state, self.teams, self.logs)

    def cleanup(self) -> None:
        if self.proc.poll() is None:
            try:
                if self.proc.stdin is not None:
                    self.proc.stdin.close()
            except OSError:
                pass
            try:
                os.kill(self.proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            self.proc.wait(timeout=30)
        marker = self.fake_state / "cli.pid"
        if marker.exists():
            cli_pid = int(marker.read_text(encoding="utf-8").strip())
            try:
                os.kill(cli_pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            _poll_until(lambda: _pid_gone(cli_pid), timeout=30)


def test_c2_sigkill_silent_death_settles_silent_end(tmp_path):
    run = DispatchRun(tmp_path, "kill-seat", "block")
    try:
        attempt = run.wait_attempt()
        assert attempt["settlement_version"] == 1
        assert attempt["attempt_id"] == "kill-seat"
        assert attempt["carrier"] == "c2-subprocess"
        assert attempt["parent_identity"] == "root"
        assert isinstance(attempt["pid"], int) and attempt["pid"] > 0
        assert attempt["started_at"]
        if Path("/proc").is_dir():
            assert isinstance(attempt.get("pid_start_ticks"), int)
        run.wait_cli_pid()
        os.kill(attempt["pid"], signal.SIGKILL)
        run.proc.wait(timeout=30)
        assert _poll_until(lambda: _pid_gone(attempt["pid"])), "recorded pid never disappeared"
        assert not run.end_path.exists(), "SIGKILL is untrappable: no .end may appear"
        assert not run.status_path.exists(), "SIGKILL is untrappable: no .status may appear"
        proc, payload = run.settle()
        assert proc.returncode == 0, (proc.stdout, proc.stderr)
        row = _finding(payload, "kill-seat")
        assert row["verdict"] == "silent-end", row
        kinds = {item["kind"] for item in row["evidence"]}
        assert "start" in kinds and "lack" in kinds, row
    finally:
        run.cleanup()


@pytest.mark.parametrize(
    "sig,signame,signum",
    [
        (signal.SIGTERM, "TERM", 15),
        (signal.SIGINT, "INT", 2),
        (signal.SIGHUP, "HUP", 1),
    ],
)
def test_c2_signal_traps_write_termination_records(tmp_path, sig, signame, signum):
    run = DispatchRun(tmp_path, "signal-seat", "block")
    try:
        attempt = run.wait_attempt()
        run.wait_cli_pid()
        os.kill(attempt["pid"], sig)
        end = _poll_json(run.end_path)
        assert end["settlement_version"] == 1
        assert end["attempt_id"] == "signal-seat"
        assert end["signal"] == signame
        assert end["exit"] == 128 + signum
        assert end["ended_at"]
        expected_status = f"signal-seat exit={128 + signum}\n"
        assert _poll_until(
            lambda: run.status_path.exists()
            and run.status_path.read_text(encoding="utf-8") == expected_status
        ), f"{signame}: the .status exit line was not written as {expected_status!r}"
        run.proc.wait(timeout=30)
        assert run.proc.returncode == 128 + signum
        proc, payload = run.settle()
        assert proc.returncode == 0, (proc.stdout, proc.stderr)
        row = _finding(payload, "signal-seat")
        assert row["verdict"] == "failed", row
    finally:
        run.cleanup()


def test_c2_live_attempt_is_running_not_silent_end(tmp_path):
    run = DispatchRun(tmp_path, "live-seat", "block")
    try:
        run.wait_attempt()
        run.wait_cli_pid()
        proc, payload = run.settle()
        assert proc.returncode == 0, (proc.stdout, proc.stderr)
        row = _finding(payload, "live-seat")
        assert row["verdict"] == "running", row
        assert row["class"] == "non-terminal"
        assert any(item["kind"] == "live" for item in row["evidence"]), row
    finally:
        run.cleanup()


def test_c2_exit_zero_without_declaration_is_failed_incomplete(tmp_path):
    run = DispatchRun(tmp_path, "quiet-seat", "done")
    try:
        run.proc.wait(timeout=120)
        assert run.proc.returncode == 0
        attempt = run.wait_attempt()
        end = _poll_json(run.end_path)
        assert end["settlement_version"] == 1
        assert end["exit"] == 0
        assert "signal" not in end
        assert run.status_path.read_text(encoding="utf-8") == "quiet-seat exit=0\n"
        assert not (run.logs / "quiet-seat.settlement").exists()
        proc, payload = run.settle()
        assert proc.returncode == 0, (proc.stdout, proc.stderr)
        row = _finding(payload, "quiet-seat")
        assert row["verdict"] == "failed", row
        assert row["detail"] == "incomplete", row
        assert row["claim"] is None
        assert row["carrier"] == "c2-subprocess"
        assert attempt["carrier"] == row["carrier"]
    finally:
        run.cleanup()


def test_c2_unreadable_evidence_is_unknown_exit_two(tmp_path):
    builders = _load_builders()
    state, teams, logs = builders.make_roots(tmp_path)
    label = builders.c2_unreadable(logs)
    proc, payload = run_settle(state, teams, logs)
    assert proc.returncode == 2, (proc.stdout, proc.stderr)
    row = _finding(payload, label)
    assert row["verdict"] == "unknown"
    assert row["unknown_cause"] == "unreadable"


def test_status_line_shape_is_read_by_the_baseline_reader(tmp_path):
    run = DispatchRun(tmp_path, "reader-seat", "done")
    try:
        run.proc.wait(timeout=120)
        assert _poll_until(run.status_path.exists), "the .status exit line was not written"
        text = run.status_path.read_text(encoding="utf-8")
        assert text == "reader-seat exit=0\n", f".status line shape changed: {text!r}"
        assert re.fullmatch(r"reader-seat exit=\d+\n", text)

        journal_utils = _load_module(
            "journal_utils_carriers", REPO_ROOT / "scripts" / "python" / "journal-utils.py"
        )
        assert journal_utils._field(text, "exit") == "0", (
            "journal-utils' existing field reader must read the new .status identically"
        )

        engine = _load_module("role_edge_settle_carriers", ENGINE)
        attempt = engine._blank_attempt("reader-seat", engine.CARRIER_C2, run.logs)
        engine._apply_status_record(attempt, run.status_path)
        assert [entry.get("exit") for entry in attempt["terminal"]] == [0]
        assert not attempt["unreadable"]
    finally:
        run.cleanup()


# --------------------------------------------------------------------------- #
# C3 — team-seat report rows and start records
# --------------------------------------------------------------------------- #
def _c3_seat(logs, label, **overrides):
    builders = _load_builders()
    fields = {"carrier": "c3-team-seat", "pid": builders.DEAD_PID}
    fields.update(overrides)
    return builders.write_attempt(logs, label, **fields)


def _c3_report(teams, header, rows, slug="demo-team"):
    builders = _load_builders()
    return builders.write_report(teams, slug, "20261126T000000Z", header, rows)


def test_c3_legacy_five_column_row_is_annotated_not_judged(tmp_path):
    builders = _load_builders()
    state, teams, logs = builders.make_roots(tmp_path)
    _c3_seat(logs, "seat-legacy")
    _c3_report(teams, builders.C2_HEADER, [
        ("seat-legacy", "subagent", "not-granted", "work/seat-legacy", "root"),
    ])
    proc, payload = run_settle(state, teams, logs)
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    row = _finding(payload, "seat-legacy")
    assert row["legacy"] is True
    assert row["violations"] == []
    assert row["verdict"] in SETTLEMENT_VALUES


def test_c3_seven_column_row_completes_with_evidence(tmp_path):
    builders = _load_builders()
    state, teams, logs = builders.make_roots(tmp_path)
    _c3_seat(logs, "seat-ok")
    (logs / "seat-ok.return.txt").write_text("returned artifact\n", encoding="utf-8")
    _c3_report(teams, builders.C3_HEADER, [
        (
            "seat-ok",
            "subagent",
            "not-granted",
            "work/seat-ok",
            "root",
            "completed",
            "seat-ok.return.txt",
        ),
    ])
    proc, payload = run_settle(state, teams, logs)
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    row = _finding(payload, "seat-ok")
    assert row["verdict"] == "completed", row
    assert row["legacy"] is False
    assert row["claim"]["value"] == "completed"


def test_c3_missing_end_state_is_settlement_unrecorded(tmp_path):
    builders = _load_builders()
    state, teams, logs = builders.make_roots(tmp_path)
    _c3_seat(logs, "seat-empty")
    _c3_report(teams, builders.C3_HEADER, [
        ("seat-empty", "subagent", "not-granted", "work/seat-empty", "root", "", ""),
    ])
    proc, payload = run_settle(state, teams, logs)
    assert proc.returncode == 1, (proc.stdout, proc.stderr)
    row = _finding(payload, "seat-empty")
    kinds = {item["kind"] for item in row["violations"]}
    assert "settlement-unrecorded" in kinds, row["violations"]


def test_c3_completed_without_resolvable_evidence_is_settlement_unbacked(tmp_path):
    builders = _load_builders()
    state, teams, logs = builders.make_roots(tmp_path)
    _c3_seat(logs, "seat-unbacked")
    _c3_report(teams, builders.C3_HEADER, [
        (
            "seat-unbacked",
            "subagent",
            "not-granted",
            "work/seat-unbacked",
            "root",
            "completed",
            "missing-proof.txt",
        ),
    ])
    proc, payload = run_settle(state, teams, logs)
    assert proc.returncode == 1, (proc.stdout, proc.stderr)
    row = _finding(payload, "seat-unbacked")
    kinds = {item["kind"] for item in row["violations"]}
    assert "settlement-unbacked" in kinds, row["violations"]
    assert row["consistent"] is False


def test_c3_seat_with_start_record_and_no_report_row_settles_silent_end(tmp_path):
    builders = _load_builders()
    state, teams, logs = builders.make_roots(tmp_path)
    _c3_seat(logs, "seat-silent")
    proc, payload = run_settle(state, teams, logs)
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    row = _finding(payload, "seat-silent")
    assert row["carrier"] == "c3-team-seat"
    assert row["verdict"] == "silent-end", row


def test_c3_report_row_without_start_record_is_unknown(tmp_path):
    builders = _load_builders()
    state, teams, logs = builders.make_roots(tmp_path)
    (logs / "seat-lost.return.txt").write_text("claimed\n", encoding="utf-8")
    _c3_report(teams, builders.C3_HEADER, [
        (
            "seat-lost",
            "subagent",
            "not-granted",
            "work/seat-lost",
            "root",
            "completed",
            "seat-lost.return.txt",
        ),
    ])
    proc, payload = run_settle(state, teams, logs)
    assert proc.returncode == 2, (proc.stdout, proc.stderr)
    row = _finding(payload, "seat-lost")
    assert row["verdict"] == "unknown"
    assert row["unknown_cause"] == "start-record-missing"


# --------------------------------------------------------------------------- #
# C4 / C5 / C6 — the owner-sentence pins on the declaration surfaces
# --------------------------------------------------------------------------- #
def test_c4_run_agent_native_settlement_obligations():
    body = _norm(_read(RUN_AGENT))
    for phrase in (
        "`c4-native`",
        "existing dispatch log directory",
        "`<label>.attempt`",
        "five-element",
        "`failed` (incomplete)",
        "MUST NOT be consumed",
        "host error",
        "`--wait-deadline`",
        "`wait_deadline_s`",
        "no return and no live signal",
        "`silent-end`",
        "foreground-terminal",
        "no settlement edge",
        "virtual dispatch is not background settlement",
        "no second mode table",
        OWNER_PATH,
        OWNER_SECTION,
    ):
        assert phrase in body, f"run-agent C4 obligation missing phrase: {phrase!r}"


def test_c5_virtual_exclusion_is_written_in_three_execution_modes():
    sections = _sections(_read(SUBAGENT_DEFS))
    hits = [heading for heading in sections if heading.startswith("## Three Execution Modes")]
    assert hits, "§ Three Execution Modes section missing from subagent-definitions.md"
    body = _norm(sections[hits[0]]).lower()
    for phrase in (
        "cannot detach from the session",
        "the parent is the executor",
        "no orphan edge",
        "excluded from background settlement",
        "unfinished virtual work must not be reported `completed`",
    ):
        assert phrase in body, f"virtual exclusion missing phrase: {phrase!r}"
    raw = _norm(sections[hits[0]])
    assert OWNER_PATH in raw and OWNER_SECTION in raw, (
        "the virtual exclusion must point at the settlement owner"
    )


def test_c6_recipes_carry_per_value_dispositions():
    body = _norm(_read(RECIPES))
    for phrase in (
        "`silent-end`",
        "`unknown`",
        "`running`",
        "compliant runner or wrapper",
        "foreground-terminal",
        "`failed` (incomplete)",
        "re-asked",
        "MUST NOT disappear",
        OWNER_PATH,
        OWNER_SECTION,
    ):
        assert phrase in body, f"recipes settlement disposition missing phrase: {phrase!r}"
    assert "treat it as a stall, not a silence" not in body, (
        "the single ambiguous stall sentence must be replaced by per-value dispositions"
    )


def test_c16_report_contract_declares_the_settlement_columns():
    body = _norm(_read(CREATE_TEAM))
    for phrase in (
        "`end_state`",
        "`evidence`",
        "7 列",
        "5 列旧头",
        "legacy",
        "settlement-unrecorded",
        "settlement-unbacked",
        "结算覆盖",
        "carrier `c3-team-seat`",
        "`<label>.attempt`",
        "同 label 的既有载体起点证据",
        OWNER_PATH,
        OWNER_SECTION,
    ):
        assert phrase in body, f"report contract missing phrase: {phrase!r}"


def test_c21_observer_remains_optional():
    sections = _sections(_read(OWNER))
    hits = [heading for heading in sections if heading.startswith("## Termination")]
    assert hits, "§ Termination section missing from the owner page"
    body = _norm(sections[hits[0]])
    for phrase in (
        "MUST NOT be the only settlement carrier",
        "a line without an observer still settles",
        "No probe class",
        "handler binding",
        "observer dependency",
    ):
        assert phrase in body, f"observer-optional sentence missing phrase: {phrase!r}"


def test_c22_dispatch_entries_reference_the_same_owner():
    entries = (RUN_TEAM, DRIVER_SKILL, AGENTS_CMD, TEAM_CMD) + COORDINATORS
    offenders = []
    for path in entries:
        body = _norm(_read(path))
        if OWNER_PATH not in body or OWNER_SECTION not in body:
            offenders.append(path.relative_to(REPO_ROOT).as_posix())
    assert not offenders, (
        "dispatch entry / dispatch-duty definitions must reference the same settlement "
        f"owner: {offenders}"
    )
    run_team_body = _norm(_read(RUN_TEAM))
    for phrase in ("c3-team-seat", "`<label>.attempt`", "同 label 的既有载体起点证据"):
        assert phrase in run_team_body, (
            f"run-team must declare the seat start-record obligation: {phrase!r}"
        )


def test_no_dispatch_surface_carries_a_second_value_table():
    offenders = []
    surfaces = (
        RUN_AGENT,
        CREATE_TEAM,
        RUN_TEAM,
        DRIVER_SKILL,
        AGENTS_CMD,
        TEAM_CMD,
        RECIPES,
        SUBAGENT_DEFS,
    ) + COORDINATORS
    for path in surfaces:
        text = _read(path)
        present = {value for value in SETTLEMENT_VALUES if f"`{value}`" in text}
        if len(present) >= 5:
            offenders.append((path.relative_to(REPO_ROOT).as_posix(), sorted(present)))
    assert not offenders, (
        f"a second settlement value table exists on a dispatch surface: {offenders}"
    )


# --------------------------------------------------------------------------- #
# Reaction obligations (T020) — the run-agent text carries its own side
# --------------------------------------------------------------------------- #
def test_run_agent_reports_every_attempt_before_the_outward_report():
    body = _norm(_read(RUN_AGENT))
    for phrase in (
        "settle every attempt",
        "before the outward completion report",
        "settlement value with its evidence pointers",
        "「未结算」(unsettled)",
        "never silently omitted",
        "reported item by item",
        "aggregate success voice",
        "leaves an attempt unaccounted is incomplete",
    ):
        assert phrase in body, f"run-agent reaction reporting missing phrase: {phrase!r}"


def test_run_agent_retry_and_stop_rules_forbid_silent_repair():
    body = _norm(_read(RUN_AGENT))
    for phrase in (
        "new attempt with a new label",
        "never rewritten, never deleted",
        "late return is never consumed as the current result",
        "named diagnosis or the user's ruling",
        "`running` + live evidence + the stop reason",
        "never `silent-end`",
        "never fabricate a terminal record",
        "never backfill a missing return element",
        "never rewrite a `.status` line",
        "never delete evidence",
        "never consume a stale return",
    ):
        assert phrase in body, f"run-agent reaction discipline missing phrase: {phrase!r}"
