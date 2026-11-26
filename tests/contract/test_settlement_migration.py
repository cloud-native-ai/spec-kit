"""Contract tests: legacy annotation and additive versioning (spec 106, US5 / T028).

Rule owner: ``shared/definitions/superagent-definitions.md`` § Termination. Pinning
clause: ``contracts/enforcement-and-migration.contract.md`` C-33 (with the shape rule of
C-16 / INV08 and the exposure duty of the quickstart S-4 scenario).

What this pins

* the committed legacy / versioned fixture pair under
  ``tests/fixtures/settlement/{legacy,versioned}/logs``: a version-less claim is annotated
  ``legacy: true`` while a derived value is still produced, the exit code stays off 1
  (annotation is not a refusal) and no file on disk is rewritten; the versioned claim is
  audited under ``settlement_version: 1`` and stays clean;
* version-bearing is decided per claim shape — claim file by carrying
  ``settlement_version``, team-report row by its 7-column header (a 5-column row is
  version-less by schema) — and a legacy disagreement is annotated, never a violation;
* the single deterministic refusal (``unknown``, exit 2) still names the unreadable
  pointer regardless of the record's version shape;
* this feature's incompatible-change ledger is empty (exactly one declared settlement
  version in the framework sources; the owner page declares it as the first version) and
  the engine carries no pre-built version rejection: an unrecognized future version is
  audited under the ordinary predicates, never refused by a version gate.

Red-first note (declared exception, tasks.md § Tests Mode): T028 is the migration /
regression guard for behaviour US1 already delivered — ``--action settle`` landed with
the ``legacy`` / ``version_bearing`` fields at T007, so this module runs green on arrival
instead of reproducing the planned ``legacy``-is-absent red. The red capability of the
settlement guards is evidenced by the T021 reaction drill, the T025 mutation drills and
the T032 honesty record, per the declared exception; the reading is recorded in
``notes/red-first-evidence.md``.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "role-edge-check.py"
FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "settlement"
BUILDERS_PATH = FIXTURE_ROOT / "builders.py"
OWNER = REPO_ROOT / "shared" / "definitions" / "superagent-definitions.md"

LEGACY_LOGS = FIXTURE_ROOT / "legacy" / "logs"
VERSIONED_LOGS = FIXTURE_ROOT / "versioned" / "logs"

CLOSED_VALUES = {
    "completed",
    "failed",
    "anomaly",
    "cancelled",
    "running",
    "silent-end",
    "unknown",
}
SOURCE_ROOTS = ("shared", "skills", "templates", "agents", "scripts")
SOURCE_SUFFIXES = {".md", ".sh", ".py", ".yaml", ".yml"}


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


def _read(path: Path) -> str:
    assert path.is_file(), f"missing required file: {path}"
    return path.read_text(encoding="utf-8")


# --------------------------------------------------------------------------- #
# S-4 — the committed legacy / versioned fixture pair
# --------------------------------------------------------------------------- #
def test_legacy_annotated_not_compliant(tmp_path):
    """The legacy fixture settles with a derived value, is annotated, exits 0, stays unwritten."""
    state, teams = tmp_path / "state", tmp_path / "teams"
    state.mkdir()
    teams.mkdir()
    before = _tree_hashes(LEGACY_LOGS)
    proc, payload = settle(state, teams, LEGACY_LOGS)
    after = _tree_hashes(LEGACY_LOGS)

    assert proc.returncode == 0, (
        "a legacy record alone must not produce a failing exit code (annotation, not "
        "a refusal): %r %r" % (proc.stdout, proc.stderr)
    )
    row = _finding(payload, "legacy-run")
    assert row["legacy"] is True, row
    assert row["verdict"] == "completed", row
    assert row["verdict"] in CLOSED_VALUES
    assert row["violations"] == [], row["violations"]
    assert row["claim"]["value"] == "completed"
    assert row["claim"]["settlement_version"] is None
    assert before == after, "settle rewrote a legacy fixture file; dated records are never rewritten"


def test_versioned_claim_is_audited(tmp_path):
    """The versioned fixture carries settlement_version 1 and is judged as a full claim."""
    state, teams = tmp_path / "state", tmp_path / "teams"
    state.mkdir()
    teams.mkdir()
    before = _tree_hashes(VERSIONED_LOGS)
    proc, payload = settle(state, teams, VERSIONED_LOGS)
    after = _tree_hashes(VERSIONED_LOGS)

    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    row = _finding(payload, "versioned-run")
    assert row["legacy"] is False, row
    assert row["claim"]["settlement_version"] == 1
    assert row["verdict"] == "completed", row
    assert row["consistent"] is True
    assert row["violations"] == [], row["violations"]
    assert before == after, "settle rewrote a versioned fixture file"


def test_version_bearing_is_decided_by_claim_shape(tmp_path):
    """Claim file: presence of settlement_version; report row: the 7-column header."""
    builders = _load_builders()
    state, teams, logs = builders.make_roots(tmp_path)
    builders.write_attempt(logs, "shaped-legacy")
    builders.write_end(logs, "shaped-legacy", exit=0)
    builders.write_claim(
        logs, "shaped-legacy", value="completed", mechanism="return-record",
        evidence=[], version=None,
    )
    builders.write_attempt(logs, "shaped-versioned")
    builders.write_end(logs, "shaped-versioned", exit=0)
    (logs / "shaped-versioned.return.txt").write_text("artifact\n", encoding="utf-8")
    builders.write_claim(
        logs, "shaped-versioned", value="completed", mechanism="return-record",
        evidence=["shaped-versioned.return.txt"], version=1,
    )
    builders.write_report(teams, "shape-team", "20261126T000000Z", builders.C2_HEADER, [
        ("shaped-legacy", "subagent", "not-granted", "work/legacy", "root"),
    ])
    builders.write_report(teams, "shape-team", "20261126T000001Z", builders.C3_HEADER, [
        ("shaped-versioned", "subagent", "not-granted", "work/versioned", "root",
         "completed", "shaped-versioned.return.txt"),
    ])

    proc, payload = settle(state, teams, logs)
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    legacy = _finding(payload, "shaped-legacy")
    versioned = _finding(payload, "shaped-versioned")
    assert legacy["legacy"] is True, legacy
    assert versioned["legacy"] is False, versioned
    assert legacy["claim"]["surface"] == "attempt-file"
    assert legacy["claim"]["settlement_version"] is None
    assert versioned["claim"]["settlement_version"] == 1


def test_legacy_disagreement_is_annotated_not_a_violation(tmp_path):
    """A legacy claim judged by none of the three predicates never drives exit 1."""
    builders = _load_builders()
    state, teams, logs = builders.make_roots(tmp_path)
    builders.write_attempt(logs, "legacy-mismatch")
    builders.write_end(logs, "legacy-mismatch", exit=0)
    # No completion evidence, no version declaration: the claim disagrees with the
    # evidence-derived value, yet a legacy record carries no violation and no exit 1.
    builders.write_claim(
        logs, "legacy-mismatch", value="completed", mechanism="return-record",
        evidence=[], version=None,
    )
    proc, payload = settle(state, teams, logs)
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    row = _finding(payload, "legacy-mismatch")
    assert row["legacy"] is True
    assert row["verdict"] == "failed", row
    assert row["detail"] == "incomplete", row
    assert row["claim"]["value"] == "completed"
    assert row["consistent"] is False, "the audit still reports the disagreement"
    assert row["violations"] == [], (
        "a legacy record must be exempt from all three settlement predicates"
    )
    assert payload["summary"]["violations"] == 0


# --------------------------------------------------------------------------- #
# The single deterministic refusal applies regardless of version shape
# --------------------------------------------------------------------------- #
def test_unreadable_legacy_claim_is_unknown_exit_two_naming_the_pointer(tmp_path):
    builders = _load_builders()
    state, teams, logs = builders.make_roots(tmp_path)
    builders.write_attempt(logs, "broken-legacy")
    builders.write_end(logs, "broken-legacy", exit=0)
    (logs / "broken-legacy.settlement").write_text("{not valid json\n", encoding="utf-8")

    proc, payload = settle(state, teams, logs)
    assert proc.returncode == 2, (proc.stdout, proc.stderr)
    row = _finding(payload, "broken-legacy")
    assert row["verdict"] == "unknown"
    assert row["unknown_cause"] == "unreadable"
    named = [
        item["pointer"]
        for item in row["evidence"]
        if item.get("kind") == "unreadable"
    ]
    assert any(pointer.endswith("broken-legacy.settlement") for pointer in named), named


def test_unreadable_versioned_record_is_unknown_exit_two_naming_the_pointer(tmp_path):
    builders = _load_builders()
    state, teams, logs = builders.make_roots(tmp_path)
    builders.write_attempt(logs, "broken-versioned")
    (logs / "broken-versioned.end").write_text("{not valid json\n", encoding="utf-8")
    (logs / "broken-versioned.return.txt").write_text("artifact\n", encoding="utf-8")
    builders.write_claim(
        logs, "broken-versioned", value="completed", mechanism="return-record",
        evidence=["broken-versioned.return.txt"], version=1,
    )

    proc, payload = settle(state, teams, logs)
    assert proc.returncode == 2, (proc.stdout, proc.stderr)
    row = _finding(payload, "broken-versioned")
    assert row["verdict"] == "unknown"
    assert row["unknown_cause"] == "unreadable"
    named = [
        item["pointer"]
        for item in row["evidence"]
        if item.get("kind") == "unreadable"
    ]
    assert any(pointer.endswith("broken-versioned.end") for pointer in named), named


# --------------------------------------------------------------------------- #
# Empty incompatible-change ledger, no pre-built version rejection (C-33)
# --------------------------------------------------------------------------- #
def test_incompatible_change_ledger_is_empty():
    """Exactly one settlement version is declared in the framework sources."""
    literal = re.compile(r"""["']?settlement_version["']?\s*[:=]\s*(\d+)""")
    declared = {}
    for root_name in SOURCE_ROOTS:
        root = REPO_ROOT / root_name
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix not in SOURCE_SUFFIXES:
                continue
            for match in literal.finditer(_read(path)):
                declared.setdefault(match.group(1), []).append(
                    path.relative_to(REPO_ROOT).as_posix()
                )
    assert set(declared) == {"1"}, (
        "the ledger is empty: no settlement record shape beyond version 1 may ship "
        "without a migration path; declared versions: %r" % (declared,)
    )

    owner = _read(OWNER)
    assert "`settlement_version` (`1` in this page's first version)" in owner, (
        "the owner page must declare its first (and only) settlement version"
    )
    assert "No pre-built rejection mechanism is added beyond that single refusal." in owner


def test_engine_carries_no_prebuilt_version_rejection(tmp_path):
    """An unrecognized future version is audited, never refused by a version gate."""
    source = _read(ENGINE)
    lines = [line for line in source.splitlines() if "settlement_version" in line]
    assert lines, "the settle action stopped reading settlement_version"
    for line in lines:
        assert not re.search(r"settlement_version[^#\n]{0,40}(==|!=|<=|>=|<|>)", line), line
        assert not re.search(r"(==|!=|<=|>=|<|>)\s*[0-9]+\s*[^\n]{0,40}settlement_version", line), line
    assert "SUPPORTED_SETTLEMENT_VERSION" not in source

    builders = _load_builders()
    state, teams, logs = builders.make_roots(tmp_path)
    # A clean claim from a hypothetical future version is judged, not refused.
    builders.write_attempt(logs, "future-clean")
    builders.write_end(logs, "future-clean", exit=0)
    (logs / "future-clean.return.txt").write_text("artifact\n", encoding="utf-8")
    builders.write_claim(
        logs, "future-clean", value="completed", mechanism="return-record",
        evidence=["future-clean.return.txt"], version=2,
    )
    # A bad value on that version is caught by the ordinary out-of-set predicate.
    builders.write_attempt(logs, "future-bad")
    builders.write_end(logs, "future-bad", exit=0)
    builders.write_claim(
        logs, "future-bad", value="not-a-settlement-value", mechanism="return-record",
        evidence=[], version=2,
    )

    proc, payload = settle(state, teams, logs)
    assert proc.returncode == 1, (
        "the out-of-set predicate (exit 1), not a version gate, judges the bad value: "
        "%r %r" % (proc.stdout, proc.stderr)
    )
    clean = _finding(payload, "future-clean")
    assert clean["verdict"] == "completed", clean
    assert clean["legacy"] is False
    assert clean["claim"]["settlement_version"] == 2
    assert clean["violations"] == []
    bad = _finding(payload, "future-bad")
    kinds = {item["kind"] for item in bad["violations"]}
    assert "settlement-out-of-set" in kinds, bad["violations"]
