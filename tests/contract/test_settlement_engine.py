"""Contract tests: the read-only settlement judgment face (spec 106, US1 / T006).

Rule owner: ``shared/definitions/superagent-definitions.md`` § Termination. Pinning
clauses: ``contracts/enforcement-and-migration.contract.md`` C-25…C-29 plus
``carrier-conformance.contract.md`` C-13.

What this pins

* C-25 — ``scripts/python/role-edge-check.py --action settle`` exists, is read-only
  (zero writes, fixture tree byte-identical after a run), answers ``-h`` / ``--version``
  and rejects undeclared options before reading, and declares the boundary options
  ``--live-window`` / ``--wait-deadline`` / ``--start-grace`` as positive integers.
* C-26 — exit codes 0 (every attempt judged, a correctly derived ``silent-end``
  included) / 1 (settlement violations) / 2 (``unknown`` findings naming the unreadable
  pointer or the missing start slot); ``unknown`` is never exit 0.
* C-27 — only the three settlement violation kinds.
* C-28 — C1 four-piece + stage sidecar/spine, the C2 triplet + additive records, the C3
  seat start record + report mapping rows (5-column legacy and 7-column new), the C4
  native attempt record, inside the existing roots.
* C-29 — two consecutive runs on the same input are byte-identical.
* C-13 — the C1 verdict mapping DONE / FAILED / ANOMALY / INCOMPLETE / DEAD / NO_SIGNAL
  / TIMEOUT / RUNNING.

Red-first (Constitution IV): at T006 the ``settle`` action does not exist, so every leg
fails on its own named assertion (argparse rejects ``--action settle`` with exit 2 and
an empty stdout) — never on an import or collection error. The engine is loaded lazily
only where its importable mapping interface is the subject.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "role-edge-check.py"
FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "settlement"
BUILDERS_PATH = FIXTURE_ROOT / "builders.py"

CLOSED_VALUES = {
    "completed",
    "failed",
    "anomaly",
    "cancelled",
    "running",
    "silent-end",
    "unknown",
}
VALUE_CLASSES = {
    "completed": "terminal",
    "failed": "terminal",
    "anomaly": "terminal",
    "cancelled": "terminal",
    "running": "non-terminal",
    "silent-end": "terminal",
    "unknown": "detection-defect",
}
SETTLEMENT_KINDS = {
    "settlement-unrecorded",
    "settlement-out-of-set",
    "settlement-unbacked",
}
EVIDENCE_KINDS = {"start", "live", "terminal", "lack", "claim", "unreadable"}
C1_MAPPING = {
    "DONE": "completed",
    "FAILED": "failed",
    "ANOMALY": "anomaly",
    "INCOMPLETE": "failed",
    "DEAD": "silent-end",
    "NO_SIGNAL": "silent-end",
    "TIMEOUT": "running",
    "RUNNING": "running",
}


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


def _load_engine():
    assert ENGINE.is_file(), "engine missing: scripts/python/role-edge-check.py"
    spec = importlib.util.spec_from_file_location("role_edge_check_settle", str(ENGINE))
    assert spec and spec.loader, "engine not loadable via importlib file location"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_engine(*args) -> subprocess.CompletedProcess:
    assert ENGINE.is_file(), "engine missing: scripts/python/role-edge-check.py"
    return subprocess.run(
        [sys.executable, str(ENGINE)] + [str(item) for item in args],
        capture_output=True,
        text=True,
        timeout=180,
    )


def settle(state, teams, logs, *extra):
    proc = run_engine(
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
        *extra,
    )
    payload = None
    if proc.stdout.strip():
        try:
            payload = json.loads(proc.stdout)
        except json.JSONDecodeError:
            payload = None
    return proc, payload


def _finding(payload: dict, attempt_id: str) -> dict:
    assert payload is not None, "settle produced no JSON payload"
    for row in payload["findings"]:
        if row["attempt_id"] == attempt_id:
            return row
    raise AssertionError(f"finding missing for {attempt_id}: {payload['findings']}")


def _tree_hashes(root: Path) -> dict:
    hashes = {}
    for path in sorted(root.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            hashes[path.relative_to(root).as_posix()] = hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
    return hashes


def _empty_roots(tmp_path):
    builders = _load_builders()
    return builders.make_roots(tmp_path)


# --------------------------------------------------------------------------- #
# C-25 — presence, read-only surface, boundary options
# --------------------------------------------------------------------------- #
def test_action_settle_exists_with_own_schema(tmp_path):
    state, teams, logs = _empty_roots(tmp_path)
    proc, payload = settle(state, teams, logs)
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    assert payload is not None, "settle must emit JSON on stdout"
    assert payload["schema_version"] == 1
    assert payload["action"] == "settle"
    assert {"schema_version", "action", "inputs", "findings", "violations", "summary"} <= set(payload)
    assert payload["findings"] == []
    assert payload["violations"] == []
    assert payload["summary"]["attempts"] == 0
    assert payload["inputs"]["live_window_s"] == 120
    assert payload["inputs"]["wait_deadline_s"] == 1800
    assert payload["inputs"]["start_grace_s"] == 30


def test_help_version_and_undeclared_option_still_hold():
    help_proc = run_engine("--help")
    assert help_proc.returncode == 0, help_proc.stderr
    assert "settle" in help_proc.stdout, "help must list the new action"
    assert "Side effects:" in help_proc.stdout
    assert "Exit codes:" in help_proc.stdout

    version = run_engine("--version")
    assert version.returncode == 0
    assert len(version.stdout.strip().splitlines()) == 1

    bad = run_engine("--no-such-option")
    assert bad.returncode == 2
    assert bad.stdout == ""


def test_boundary_options_are_positive_integers(tmp_path):
    state, teams, logs = _empty_roots(tmp_path)
    for option in ("--live-window", "--wait-deadline", "--start-grace"):
        proc, payload = settle(state, teams, logs, option, "0")
        assert proc.returncode == 2, (option, proc.stdout, proc.stderr)
        assert payload is None, f"{option} 0 must be rejected before reading"
        proc, payload = settle(state, teams, logs, option, "abc")
        assert proc.returncode == 2, (option, proc.stdout, proc.stderr)

    proc, payload = settle(
        state, teams, logs, "--live-window", "7", "--wait-deadline", "9", "--start-grace", "3"
    )
    assert proc.returncode == 0, proc.stderr
    assert payload["inputs"]["live_window_s"] == 7
    assert payload["inputs"]["wait_deadline_s"] == 9
    assert payload["inputs"]["start_grace_s"] == 3


def test_engine_stays_read_only_over_the_fixture_tree():
    before = _tree_hashes(FIXTURE_ROOT)
    proc, payload = settle(
        FIXTURE_ROOT / "c1-state",
        FIXTURE_ROOT / "c3-report" / "teams",
        FIXTURE_ROOT / "c3-report" / "logs",
    )
    assert proc.returncode in (0, 1, 2), proc.stderr
    assert payload is not None and payload["action"] == "settle", proc.stderr
    after = _tree_hashes(FIXTURE_ROOT)
    assert before == after, "the settle action wrote into the fixture tree"


def test_two_runs_are_byte_identical():
    args = (
        FIXTURE_ROOT / "c1-state",
        FIXTURE_ROOT / "c3-report" / "teams",
        FIXTURE_ROOT / "c3-report" / "logs",
    )
    first, first_payload = settle(*args)
    second, second_payload = settle(*args)
    assert first_payload is not None and first_payload["action"] == "settle", first.stderr
    assert first.stdout == second.stdout
    assert first.returncode == second.returncode
    assert first_payload == second_payload


# --------------------------------------------------------------------------- #
# C-26 / C-27 — the six terminal classes, the unknown refusal, violations
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "builder_name,expected",
    [
        ("c2_completed", "completed"),
        ("c2_failed", "failed"),
        ("c2_anomaly", "anomaly"),
        ("c2_cancelled", "cancelled"),
        ("c2_silent_end", "silent-end"),
    ],
)
def test_terminal_classes_settle_with_evidence(tmp_path, builder_name, expected):
    builders = _load_builders()
    state, teams, logs = builders.make_roots(tmp_path)
    label = getattr(builders, builder_name)(logs)
    proc, payload = settle(state, teams, logs)
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    row = _finding(payload, label)
    assert set(row) >= {
        "attempt_id",
        "carrier",
        "verdict",
        "value",
        "class",
        "evidence",
        "claim",
        "consistent",
        "legacy",
        "violations",
    }
    assert row["verdict"] == expected
    assert row["value"] == expected
    assert row["class"] == VALUE_CLASSES[expected]
    assert row["evidence"], f"{expected} must carry evidence pointers"
    for item in row["evidence"]:
        assert set(item) >= {"pointer", "kind"}
        assert item["kind"] in EVIDENCE_KINDS
    assert payload["violations"] == []
    assert all(kind in SETTLEMENT_KINDS for kind in row["violations"]) or row["violations"] == []


def test_running_requires_a_live_check_and_is_reverse_safe(tmp_path):
    builders = _load_builders()
    state, teams, logs = builders.make_roots(tmp_path)
    child = builders.c2_running(logs)
    try:
        proc, payload = settle(state, teams, logs)
    finally:
        builders.stop_live_process(child)
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    row = _finding(payload, "running")
    assert row["verdict"] == "running"
    assert row["class"] == "non-terminal"
    assert any(item["kind"] == "live" for item in row["evidence"])


def test_pid_reuse_is_not_liveness(tmp_path):
    builders = _load_builders()
    state, teams, logs = builders.make_roots(tmp_path)
    child = builders.c2_pid_reuse(logs)
    try:
        proc, payload = settle(state, teams, logs)
    finally:
        builders.stop_live_process(child)
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    row = _finding(payload, "reused")
    assert row["verdict"] == "silent-end", row


def test_silent_end_is_a_judged_attempt_not_a_violation(tmp_path):
    builders = _load_builders()
    state, teams, logs = builders.make_roots(tmp_path)
    keyed = builders.c2_silent_end(logs)
    proc, payload = settle(state, teams, logs)
    assert proc.returncode == 0, "a correctly derived silent-end is exit 0"
    row = _finding(payload, keyed)
    assert row["verdict"] == "silent-end"
    kinds = {item["kind"] for item in row["evidence"]}
    assert "start" in kinds, row
    assert "lack" in kinds, row
    assert payload["summary"]["unknown"] == 0


def test_unreadable_evidence_is_unknown_exit_two(tmp_path):
    builders = _load_builders()
    state, teams, logs = builders.make_roots(tmp_path)
    label = builders.c2_unreadable(logs)
    proc, payload = settle(state, teams, logs)
    assert proc.returncode == 2, (proc.stdout, proc.stderr)
    row = _finding(payload, label)
    assert row["verdict"] == "unknown"
    assert row["unknown_cause"] == "unreadable"
    assert any(
        item["kind"] == "unreadable" and item["pointer"].endswith(".attempt")
        for item in row["evidence"]
    ), row
    assert payload["summary"]["unknown"] >= 1


def test_missing_start_record_is_unknown_exit_two(tmp_path):
    builders = _load_builders()
    state, teams, logs = builders.make_roots(tmp_path)
    label = builders.c2_missing_start(logs)
    proc, payload = settle(state, teams, logs)
    assert proc.returncode == 2, (proc.stdout, proc.stderr)
    row = _finding(payload, label)
    assert row["verdict"] == "unknown"
    assert row["unknown_cause"] == "start-record-missing"


def test_unknown_is_never_exit_zero(tmp_path):
    builders = _load_builders()
    state, teams, logs = builders.make_roots(tmp_path)
    builders.c2_unreadable(logs)
    builders.c2_missing_start(logs)
    proc, payload = settle(state, teams, logs)
    assert proc.returncode != 0
    assert proc.returncode == 2
    assert payload["summary"]["unknown"] == 2


def test_claim_disagreeing_with_evidence_is_unbacked_exit_one(tmp_path):
    builders = _load_builders()
    state, teams, logs = builders.make_roots(tmp_path)
    label = builders.c2_failed(logs)
    (logs / f"{label}.return.txt").write_text("artifact\n", encoding="utf-8")
    builders.write_claim(
        logs,
        label,
        value="completed",
        mechanism="return-record",
        evidence=[f"{label}.return.txt"],
    )
    proc, payload = settle(state, teams, logs)
    assert proc.returncode == 1, (proc.stdout, proc.stderr)
    row = _finding(payload, label)
    assert row["verdict"] == "failed"
    assert row["consistent"] is False
    kinds = {item["kind"] for item in row["violations"]}
    assert kinds == {"settlement-unbacked"}, row["violations"]
    assert {item["kind"] for item in payload["violations"]} <= SETTLEMENT_KINDS


def test_completed_without_verification_is_incomplete(tmp_path):
    builders = _load_builders()
    state, teams, logs = builders.make_roots(tmp_path)
    label = "no-claim"
    builders.write_attempt(logs, label)
    builders.write_end(logs, label, exit=0)
    builders.write_status(logs, label, 0)
    builders.write_live_log(logs, label, ["done"])
    proc, payload = settle(state, teams, logs)
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    row = _finding(payload, label)
    assert row["verdict"] == "failed", row
    assert row["detail"] == "incomplete", row
    assert row["claim"] is None


def test_completed_claim_without_evidence_is_unbacked(tmp_path):
    builders = _load_builders()
    state, teams, logs = builders.make_roots(tmp_path)
    label = "empty-evidence"
    builders.write_attempt(logs, label)
    builders.write_end(logs, label, exit=0)
    builders.write_status(logs, label, 0)
    builders.write_live_log(logs, label, ["done"])
    builders.write_claim(logs, label, value="completed", mechanism="return-record", evidence=[])
    proc, payload = settle(state, teams, logs)
    assert proc.returncode == 1, (proc.stdout, proc.stderr)
    row = _finding(payload, label)
    assert {item["kind"] for item in row["violations"]} == {"settlement-unbacked"}


# --------------------------------------------------------------------------- #
# C-13 — the C1 verdict mapping
# --------------------------------------------------------------------------- #
def test_c1_mapping_function_covers_all_eight_tokens():
    module = _load_engine()
    mapper = getattr(module, "C1_VERDICT_MAP", None)
    assert mapper is not None, "the engine must export the C1 verdict mapping"
    assert dict(mapper) == C1_MAPPING


def test_c1_done_without_u4_claim_is_incomplete(tmp_path):
    builders = _load_builders()
    state = tmp_path / "state"
    shutil.copytree(FIXTURE_ROOT / "c1-state", state)
    teams = tmp_path / "teams"
    logs = tmp_path / "logs"
    teams.mkdir()
    logs.mkdir()
    proc, payload = settle(state, teams, logs)
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    row = _finding(payload, "demo-line-implement")
    assert row["carrier"] == "c1-fork"
    assert row["verdict"] == "failed", row
    assert row["claim"] is None


def test_c1_done_with_u4_claim_is_completed(tmp_path):
    builders = _load_builders()
    state = tmp_path / "state"
    shutil.copytree(FIXTURE_ROOT / "c1-state", state)
    teams = tmp_path / "teams"
    logs = tmp_path / "logs"
    teams.mkdir()
    logs.mkdir()
    (logs / "u4-verification.txt").write_text("U4 pass\n", encoding="utf-8")
    builders.write_claim(
        logs,
        "demo-line-implement",
        value="completed",
        mechanism="u4",
        evidence=["u4-verification.txt"],
    )
    proc, payload = settle(state, teams, logs)
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    row = _finding(payload, "demo-line-implement")
    assert row["verdict"] == "completed", row
    assert row["claim"]["value"] == "completed"


# --------------------------------------------------------------------------- #
# C-28 — C3 report rows: 7-column new and 5-column legacy
# --------------------------------------------------------------------------- #
def test_team_report_rows_parse_in_both_shapes():
    proc, payload = settle(
        FIXTURE_ROOT / "c1-state",
        FIXTURE_ROOT / "c3-report" / "teams",
        FIXTURE_ROOT / "c3-report" / "logs",
    )
    assert proc.returncode == 2, "the missing-start seat is an unknown refusal"
    ok = _finding(payload, "seat-ok")
    assert ok["carrier"] == "c3-team-seat"
    assert ok["verdict"] == "completed", ok
    assert ok["claim"]["value"] == "completed"
    assert ok["legacy"] is False

    legacy = _finding(payload, "seat-legacy")
    assert legacy["legacy"] is True
    assert legacy["verdict"] in CLOSED_VALUES
    assert legacy["violations"] == []

    missing = _finding(payload, "seat-missing-start")
    assert missing["verdict"] == "unknown"
    assert missing["unknown_cause"] == "start-record-missing"
