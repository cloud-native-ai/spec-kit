"""Preservation guard: the surfaces spec 106 must not move (US4 / T023).

Rule owner: ``shared/definitions/superagent-definitions.md`` § Termination. Pinning
clause: ``contracts/carrier-conformance.contract.md`` C-23 (all new surfaces are
additive; the preserved set has an empty allowed delta).

What this pins, each against a committed baseline under ``test-evidence/``

* watcher verdict-token set, exit-code set and sentinel-literal set — the same
  extractor over the live ``watch-target.sh`` and its ``fbab7a45c`` copy
  (``test-evidence/watch-target-fbab7a45c.sh``) must agree member-for-member;
* ``watch-target.sh --self-test`` still reports ``SELF-TEST: 39 passed, 0 failed`` and
  the same 39 case names as ``test-evidence/watch-self-test-baseline.txt``;
* the five-element uplink and seven-field downlink paragraphs are unchanged against
  ``test-evidence/super-sub-protocol-fbab7a45c.txt``;
* ``role-edge-check.py --action report`` is byte-identical to the pre-change engine's
  output recorded at ``test-evidence/role-edge-report-empty-fbab7a45c.json`` (read-only);
* ``scan-confirmation-gates.py`` adds no hit on any touched declaration file beyond the
  per-file baseline (EP-005 fallback: the frozen ``total == 27`` equality is a
  disclosed pre-existing red, so the metric is per-touched-file counts);
* the two-slot test budget keeps exactly one baseline slot and at most one closure slot
  — the rule is read from its owner engine ``audit-test-budget.py`` (``read_fence`` +
  ``check_ledger``), never restated here.

The baseline files are dated records, not regeneration targets: a difference here is a
preserved-surface drift, not a fixture refresh.
"""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = REPO_ROOT / ".specify" / "specs" / "106-background-silent-failure" / "test-evidence"
LIVE_WATCHER = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "watch-target.sh"
BASELINE_WATCHER = EVIDENCE / "watch-target-fbab7a45c.sh"
SELF_TEST_BASELINE = EVIDENCE / "watch-self-test-baseline.txt"
PROTOCOL_BASELINE = EVIDENCE / "super-sub-protocol-fbab7a45c.txt"
REPORT_BASELINE = EVIDENCE / "role-edge-report-empty-fbab7a45c.json"
GATE_BASELINE = EVIDENCE / "scan-confirmation-gates-baseline.json"
OWNER = REPO_ROOT / "shared" / "definitions" / "superagent-definitions.md"
ENGINE = REPO_ROOT / "scripts" / "python" / "role-edge-check.py"
GATE_SCAN = REPO_ROOT / "scripts" / "python" / "scan-confirmation-gates.py"
BUDGET_AUDIT = (
    REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "audit-test-budget.py"
)
SPINE = REPO_ROOT / ".specify" / "state" / "background-silent-failure.md"
SPEC_DIR = REPO_ROOT / ".specify" / "specs" / "106-background-silent-failure"
EMPTY_FIXTURE = "tests/fixtures/superagent-role/empty"

EXPECTED_VERDICTS = {
    "DONE",
    "RUNNING",
    "ANOMALY",
    "FAILED",
    "DEAD",
    "TIMEOUT",
    "INCOMPLETE",
    "NO_SIGNAL",
    "USAGE",
}
EXPECTED_CODES = {0, 10, 11, 12, 13, 14, 15, 16, 2}
SEVEN_FIELDS = (
    "parent_identity",
    "child_label",
    "role_declaration",
    "dispatch_duty",
    "depth_position",
    "authority_ref",
    "return_channel",
)
TOUCHED_DECLARATION_FILES = (
    "shared/definitions/superagent-definitions.md",
    "shared/definitions/subagent-definitions.md",
    "shared/workflow/external-dispatch-recipes.md",
    "skills/internal/run-agent/SKILL.md",
    "skills/internal/create-team/SKILL.md",
    "skills/internal/run-team/SKILL.md",
    "skills/external/sdd-loop-driver/SKILL.md",
    "templates/commands/agents.md",
    "templates/commands/team.md",
)


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _read(path: Path) -> str:
    assert path.is_file(), f"missing required file: {path}"
    return path.read_text(encoding="utf-8")


def _load_module(name: str, path: Path):
    assert path.is_file(), f"module missing: {path}"
    spec = importlib.util.spec_from_file_location(name, str(path))
    assert spec and spec.loader, f"module not loadable: {path}"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run(*args, timeout=600) -> subprocess.CompletedProcess:
    return subprocess.run(
        [str(item) for item in args],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=timeout,
    )


# --------------------------------------------------------------------------- #
# watcher: verdict tokens, exit codes, sentinel literals (same extractor)
# --------------------------------------------------------------------------- #
def _verdict_block(text: str) -> list:
    lines = text.splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if line.strip() == "Verdicts / exit codes:"
    ]
    assert starts, "the watcher usage lost its 'Verdicts / exit codes:' block"
    block = []
    for line in lines[starts[-1] + 1 :]:
        match = re.match(r"^\s{2,}(\d+)\s+([A-Z_]+)\s+\S", line)
        if match:
            block.append((int(match.group(1)), match.group(2)))
        elif block:
            break
    assert block, "the verdict block parsed empty"
    return block


def _watcher_facts(path: Path) -> dict:
    text = _read(path)
    block = _verdict_block(text)
    return {
        "block": block,
        "verdicts": {name for _code, name in block},
        "codes": {code for code, _name in block},
        "sentinels": set(re.findall(r"\b[A-Z][A-Z0-9]*-DONE\b", text)),
    }


def test_watcher_sets_equal_the_fbab7a45c_baseline_member_for_member():
    live = _watcher_facts(LIVE_WATCHER)
    base = _watcher_facts(BASELINE_WATCHER)
    assert live["block"] == base["block"], "verdict/exit-code pairs drifted"
    assert live["verdicts"] == base["verdicts"], "verdict token set drifted"
    assert live["codes"] == base["codes"], "watcher exit-code set drifted"
    assert live["sentinels"] == base["sentinels"], "sentinel literal set drifted"
    assert live["verdicts"] == EXPECTED_VERDICTS
    assert live["codes"] == EXPECTED_CODES


def test_watcher_self_test_still_reports_39_of_0():
    proc = _run("bash", LIVE_WATCHER, "--self-test", timeout=900)
    assert proc.returncode == 0, (proc.stdout[-2000:], proc.stderr[-2000:])
    lines = [line for line in proc.stdout.splitlines() if line.strip()]
    assert lines[-1] == "SELF-TEST: 39 passed, 0 failed", lines[-1]
    ok_names = {
        line[3:].strip() for line in proc.stdout.splitlines() if line.startswith("ok ")
    }
    baseline_names = {
        line[3:].strip()
        for line in _read(SELF_TEST_BASELINE).splitlines()
        if line.startswith("ok ")
    }
    assert len(baseline_names) == 39
    assert ok_names == baseline_names, (
        f"self-test case set drifted: added={sorted(ok_names - baseline_names)} "
        f"missing={sorted(baseline_names - ok_names)}"
    )


# --------------------------------------------------------------------------- #
# five-element uplink / seven-field downlink text
# --------------------------------------------------------------------------- #
def _baseline_paragraph(label: str) -> str:
    text = _read(PROTOCOL_BASELINE)
    match = re.search(
        r"<!-- %s-BEGIN -->\n(.*)\n<!-- %s-END -->" % (label, label), text, re.S
    )
    assert match, f"{label} baseline paragraph missing from {PROTOCOL_BASELINE}"
    return match.group(1)


def _live_paragraph(label: str) -> str:
    lines = _read(OWNER).splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if line.startswith("## The super↔sub Protocol")
    ]
    assert starts, "the owner page lost § The super↔sub Protocol"
    for line in lines[starts[0] :]:
        if line.startswith("**%s.**" % label):
            return line
    raise AssertionError(f"{label} paragraph missing from the live owner page")


def test_five_element_uplink_and_seven_field_downlink_text_unchanged():
    assert _live_paragraph("Downlink") == _baseline_paragraph("DOWNLINK")
    assert _live_paragraph("Uplink") == _baseline_paragraph("UPLINK")
    downlink = _live_paragraph("Downlink")
    positions = [downlink.find(f"`{field}`") for field in SEVEN_FIELDS]
    assert all(position >= 0 for position in positions), (
        "a seven-field downlink name disappeared from the Downlink paragraph"
    )
    assert positions == sorted(positions), "the seven downlink fields lost their order"
    uplink = _live_paragraph("Uplink")
    for phrase in (
        "result or deliverable path",
        "evidence pointer(s)",
        "explicit anomaly line",
        "concurrency reading triple",
        "returning executor's identity",
    ):
        assert phrase in uplink, f"a five-element uplink phrase disappeared: {phrase!r}"


# --------------------------------------------------------------------------- #
# report byte equality against the recorded pre-change output
# --------------------------------------------------------------------------- #
def _report_stdout() -> str:
    proc = _run(
        sys.executable,
        ENGINE,
        "--action",
        "report",
        "--state-dir",
        EMPTY_FIXTURE + "/state",
        "--teams-dir",
        EMPTY_FIXTURE + "/teams",
        "--logs-dir",
        EMPTY_FIXTURE + "/logs",
        "--registry-dir",
        EMPTY_FIXTURE + "/registry",
    )
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    return proc.stdout


def test_report_action_is_byte_identical_to_the_recorded_baseline():
    baseline = _read(REPORT_BASELINE)
    first = _report_stdout()
    second = _report_stdout()
    assert first == baseline, "the report action output drifted from the fbab7a45c baseline"
    assert first == second, "two report runs are not byte-identical"
    payload = json.loads(first)
    assert payload["action"] == "report"
    assert payload["summary"] == {
        "edges": 0,
        "executors": 0,
        "violations": 0,
        "conflicts": 0,
    }


# --------------------------------------------------------------------------- #
# confirmation-gate scan: per-touched-file counts never above baseline
# --------------------------------------------------------------------------- #
def _gate_counts(document: dict) -> dict:
    counts = {}
    for gate in document.get("gates", []):
        counts[gate["file"]] = counts.get(gate["file"], 0) + 1
    return counts


def test_confirmation_gate_scan_adds_no_hits_on_touched_files():
    proc = _run(sys.executable, GATE_SCAN, "--root", ".", "--json")
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    live = _gate_counts(json.loads(proc.stdout))
    base = _gate_counts(json.loads(_read(GATE_BASELINE)))
    offenders = []
    for touched in TOUCHED_DECLARATION_FILES:
        if live.get(touched, 0) > base.get(touched, 0):
            offenders.append(
                (touched, "base=%d" % base.get(touched, 0), "live=%d" % live.get(touched, 0))
            )
    assert not offenders, f"a touched declaration file gained gate hits: {offenders}"


# --------------------------------------------------------------------------- #
# two-slot test budget — the rule read from its owner engine
# --------------------------------------------------------------------------- #
def test_test_budget_keeps_one_baseline_and_at_most_one_closure_slot():
    audit = _load_module("audit_test_budget", BUDGET_AUDIT)
    _text, rows = audit.read_fence(str(SPINE))
    violations = []
    unknown = [0]
    counts = audit.check_ledger(rows, "implement", violations, unknown)
    assert violations == [], f"the two-slot ledger is violated: {violations}"
    assert unknown[0] == 0
    assert counts["baseline"] == 1, counts
    assert counts["closure"] <= 1, counts
