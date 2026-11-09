"""Real-run evidence contract (requirements SC-006 / FR-030, quickstart S-6).

Rows pinned here (WP4): T106.

A coordination report is accepted only when it carries, for a **non-fixture** run:

- ``run_kind: real`` — a fixture run never satisfies SC-006;
- the units' intervals and per-unit verdicts with their evidence pointers;
- the deterministic integration order and the duration;
- the 091 serial-baseline comparison (62 tasks, one agent, 116 minutes, cited from 091's
  own record — never re-measured here);
- every quantity the run did not produce written as the literal ``not_evaluated`` — a ``0``
  or an estimate is a fabricated number and fails.

The engine half reuses the ``reading`` action: a report claiming concurrency without
intervals is red, and a missing interval reads ``not_evaluated``. Engine cases are
red-first (``scripts/python/concurrency-check.py`` lands in WP2); this feature's own
coordination report lands with T110 (WP5), so its live read records ``not_evaluated`` with
that reason instead of a silent skip.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "concurrency-check.py"
SPEC_DIR = REPO_ROOT / ".specify" / "specs" / "093-concurrency-by-default"

NOT_EVALUATED = "not_evaluated"


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _run_engine(*args):
    assert ENGINE.is_file(), (
        "red-first: scripts/python/concurrency-check.py is the WP2 engine target and is "
        "not in this worktree yet")
    return subprocess.run(
        [sys.executable, str(ENGINE), *[str(arg) for arg in args]],
        capture_output=True, text=True, cwd=str(REPO_ROOT), timeout=120,
    )


def _repo(tmp_path: Path) -> Path:
    shutil.copytree(REPO_ROOT / "shared" / "declarations", tmp_path / "shared" / "declarations")
    return tmp_path


def _record(repo: Path, name: str, lines) -> Path:
    path = repo / name
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _find(node, key):
    if isinstance(node, dict):
        if key in node:
            return node[key]
        for value in node.values():
            found = _find(value, key)
            if found is not None:
                return found
    elif isinstance(node, list):
        for item in node:
            found = _find(item, key)
            if found is not None:
                return found
    return None


def _reading(repo: Path, record: Path, out: Path):
    proc = _run_engine("reading", "--repo", repo, "--record", record, "--json-out", out)
    envelope = json.loads(out.read_text(encoding="utf-8")) if out.is_file() else None
    return proc, envelope


# --------------------------------------------------------------------------- #
# T106 — the report shape judge
# --------------------------------------------------------------------------- #
BASELINE = {"tasks": 62, "agents": 1, "minutes": 116}  # 091's own record, cited not measured


def _valid_quantity(value):
    return isinstance(value, int) and value > 0


def _judge_report(report: dict) -> list:
    findings = []
    if report.get("run_kind") != "real":
        findings.append(("fixture-run", "a fixture run cannot satisfy SC-006"))
    units = report.get("units", [])
    if not units:
        findings.append(("report-incomplete", "no units recorded"))
    intervals = all(
        unit.get("dispatched_at") is not None and unit.get("settled_at") is not None
        for unit in units)
    for unit in units:
        if unit.get("verdict") not in ("pass", "fail", "blocked"):
            findings.append(("report-incomplete", "unit %s has no verdict" % unit.get("unit_id")))
        if not unit.get("evidence_ptr"):
            findings.append(("report-incomplete", "unit %s has no evidence pointer" % unit.get("unit_id")))
    if not intervals:
        effective = report.get("effective")
        if effective != NOT_EVALUATED:
            findings.append(("fabricated-number",
                             "a report without intervals must read %r, not %r"
                             % (NOT_EVALUATED, effective)))
    elif int(report.get("effective", 0)) < 2:
        findings.append(("not-concurrent", "a real-run report must show effective >= 2"))
    if not report.get("integration_order"):
        findings.append(("report-incomplete", "the deterministic integration order is missing"))
    duration = report.get("duration_seconds")
    if duration is not None and not _valid_quantity(duration) and duration != NOT_EVALUATED:
        findings.append(("fabricated-number", "duration must be measured or %r" % NOT_EVALUATED))
    baseline = report.get("baseline_091")
    if not isinstance(baseline, dict) or not baseline:
        findings.append(("report-incomplete", "the 091 baseline comparison is missing"))
    else:
        for key in ("tasks", "agents", "minutes"):
            value = baseline.get(key)
            if value is not None and not _valid_quantity(value) and value != NOT_EVALUATED:
                findings.append(("fabricated-number", "baseline %s must be cited or %r"
                                 % (key, NOT_EVALUATED)))
    return findings


def _valid_report():
    return {
        "run_kind": "real",
        "effective": 2,
        "units": [
            {"unit_id": "unit-a", "dispatched_at": 0, "settled_at": 10,
             "verdict": "pass", "evidence_ptr": "test-evidence/a.txt"},
            {"unit_id": "unit-b", "dispatched_at": 5, "settled_at": 20,
             "verdict": "pass", "evidence_ptr": "test-evidence/b.txt"},
        ],
        "integration_order": ["unit-a", "unit-b"],
        "duration_seconds": 20,
        "baseline_091": dict(BASELINE),
    }


def test_valid_report_is_accepted():
    assert _judge_report(_valid_report()) == []


def test_fixture_run_is_rejected():
    report = _valid_report()
    report["run_kind"] = "fixture"
    assert ("fixture-run", "a fixture run cannot satisfy SC-006") in _judge_report(report)


def test_claim_without_intervals_is_red():
    report = _valid_report()
    for unit in report["units"]:
        unit.pop("dispatched_at")
        unit.pop("settled_at")
    report["effective"] = 2
    assert any(code == "fabricated-number" for code, _ in _judge_report(report))
    report["effective"] = NOT_EVALUATED
    assert not any(code == "fabricated-number" for code, _ in _judge_report(report))


def test_zero_and_estimates_are_fabricated_numbers():
    report = _valid_report()
    report["duration_seconds"] = 0
    assert any(code == "fabricated-number" for code, _ in _judge_report(report))
    report["duration_seconds"] = "~20"
    assert any(code == "fabricated-number" for code, _ in _judge_report(report))
    report["duration_seconds"] = NOT_EVALUATED
    assert not any(code == "fabricated-number" for code, _ in _judge_report(report))


def test_missing_baseline_is_incomplete():
    report = _valid_report()
    report.pop("baseline_091")
    assert any(code == "report-incomplete" for code, _ in _judge_report(report))


# --------------------------------------------------------------------------- #
# T106 — the engine half: intervals are the only concurrency evidence
# --------------------------------------------------------------------------- #
def test_engine_accepts_a_real_run_record_with_overlapping_intervals(tmp_path):
    repo = _repo(tmp_path)
    record = _record(repo, "real-run.yaml", [
        "run_kind: real",
        "requested: 2",
        "units:",
        "  - unit_id: unit-a",
        "    dispatched_at: 0",
        "    settled_at: 10",
        "    executor_id: exec-a",
        "    verifier_id: ver-a",
        "    verdict: pass",
        "    evidence_ptr: evidence/a.txt",
        "  - unit_id: unit-b",
        "    dispatched_at: 5",
        "    settled_at: 20",
        "    executor_id: exec-b",
        "    verifier_id: ver-b",
        "    verdict: pass",
        "    evidence_ptr: evidence/b.txt",
        "effective_reason: two independently dispatched units",
    ])
    proc, envelope = _reading(repo, record, tmp_path / "out.json")
    assert envelope is not None, proc.stdout + proc.stderr
    assert proc.returncode == 0, envelope.get("findings")
    assert _find(envelope.get("measured"), "effective") == 2


def test_engine_refuses_a_concurrency_claim_without_intervals(tmp_path):
    repo = _repo(tmp_path)
    record = _record(repo, "no-intervals.yaml", [
        "run_kind: real",
        "requested: 2",
        "units:",
        "  - unit_id: unit-a",
        "    executor_id: exec-a",
        "    verifier_id: ver-a",
        "  - unit_id: unit-b",
        "    executor_id: exec-b",
        "    verifier_id: ver-b",
    ])
    proc, envelope = _reading(repo, record, tmp_path / "out.json")
    assert envelope is not None, proc.stdout + proc.stderr
    assert proc.returncode == 1, "a claim without intervals must be red"
    assert _find(envelope.get("measured"), "effective") == NOT_EVALUATED


# --------------------------------------------------------------------------- #
# T106 — this feature's own report (lands with WP5 T110)
# --------------------------------------------------------------------------- #
def test_this_features_coordination_report_is_decidable_or_not_evaluated():
    candidates = [
        path for path in SPEC_DIR.rglob("*.md")
        if "coordination" in path.name.lower()
    ]
    if not candidates:
        pytest.skip("not_evaluated: this feature's own coordination report lands with "
                    "T110 (WP5); the report-shape judge is exercised on fixtures above")
    for path in candidates:
        text = path.read_text(encoding="utf-8")
        assert ("effective: 2" in text or "effective: 3" in text
                or "not_evaluated" in text), (
            "a coordination report states an interval-overlap reading or not_evaluated: %s" % path)
