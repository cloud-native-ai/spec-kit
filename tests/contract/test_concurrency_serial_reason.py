"""Serial-reason and default-concurrency contract (contracts/judgement-engine.contract.md C-027…C-030).

Rows pinned here (WP4): T042, T044, T046, T047, T048, T049, T050, T057.

- **T042** — a two-unit, dependency-free, disjoint-write, host-parallel fixture reads
  ``effective >= 2``; every serial record carries a non-empty ordered code list drawn from
  the closed vocabulary with no duplicates; the condition↔code bijection is asserted in
  both directions against the FR-005 clause ids carried by ``serial-reason.yaml``.
- **T044/C-030** — evidence is judged per code against its declared evidence form; ``.``
  is rejected for every code; ``pattern``/``codes`` inconsistency is caught in both
  directions (concurrent with codes, serial without).
- **T046** — the four condition-bound evidence forms: a resolvable dependency edge with its
  completion verdict pointer, an intersecting write path set, a host probe reading with its
  landing point, and before/after slot-and-budget readings.
- **T047** — a budget code is rejected when remaining budget was never measured.
- **T048** — a host code is never reusable; it carries a landing point recording that run.
- **T049** — simplicity/controllability/history are not codes; the vocabulary is named.
- **T050** — a two-condition serial records both codes in declared order; the list length is
  never reported as concurrency.

**Pinned record schema** (from C-027 and ``serial-reason.yaml``'s ``evidence_requirement``;
block-subset/v1 YAML, parsed by the engine through the same subset as the facts):

    pattern: serial
    codes:
      - <code>
    evidence:
      <code>: <per-code object>

Engine cases are red-first: ``scripts/python/concurrency-check.py`` lands in WP2.
"""
from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "concurrency-check.py"
READER = REPO_ROOT / "scripts" / "python" / "declaration_reader.py"

CONDITION_BOUND = ("dependency-edge", "write-conflict", "host-no-parallel", "budget-reserve")
FACTUAL = ("single-unit", "mechanism-not-yet-landed")


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _reader_module():
    spec = importlib.util.spec_from_file_location("declaration_reader", READER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _vocabulary():
    reader = _reader_module()
    return reader.load_fact(str(REPO_ROOT), "serial-reason")["body"]["statement"]


def _repo(tmp_path: Path) -> Path:
    shutil.copytree(REPO_ROOT / "shared" / "declarations", tmp_path / "shared" / "declarations")
    evidence = tmp_path / "evidence"
    evidence.mkdir()
    (evidence / "unit-a.verdict").write_text("verdict: pass\n", encoding="utf-8")
    (evidence / "host-probe.txt").write_text("nproc=1\n", encoding="utf-8")
    (tmp_path / "a.txt").write_text("a\n", encoding="utf-8")
    (tmp_path / "b.txt").write_text("b\n", encoding="utf-8")
    return tmp_path


def _record(repo: Path, name: str, lines) -> Path:
    path = repo / name
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _valid_record(repo: Path, code: str) -> Path:
    bodies = {
        "dependency-edge": [
            "evidence:",
            "  dependency-edge:",
            "    predecessor_id: unit-a",
            "    verdict_ptr: evidence/unit-a.verdict",
        ],
        "write-conflict": [
            "evidence:",
            "  write-conflict:",
            "    paths:",
            "      - a.txt",
            "      - b.txt",
        ],
        "host-no-parallel": [
            "evidence:",
            "  host-no-parallel:",
            "    probe: nproc=1",
            "    landing: evidence/host-probe.txt",
        ],
        "budget-reserve": [
            "evidence:",
            "  budget-reserve:",
            "    before:",
            "      slots: 3",
            "      budget: 120",
            "    after:",
            "      slots: 2",
            "      budget: 80",
        ],
        "single-unit": [
            "evidence:",
            "  single-unit:",
            "    units:",
            "      - only-unit",
        ],
        "mechanism-not-yet-landed": [
            "evidence:",
            "  mechanism-not-yet-landed:",
            "    units:",
            "      - unit-a",
            "    mechanism: fork-carrier-not-landed",
        ],
    }
    return _record(repo, "%s.yaml" % code, [
        "pattern: serial", "codes:", "  - %s" % code] + bodies[code])


def _run_engine(*args):
    assert ENGINE.is_file(), (
        "red-first: scripts/python/concurrency-check.py is the WP2 engine target and is "
        "not in this worktree yet")
    return subprocess.run(
        [sys.executable, str(ENGINE), *[str(arg) for arg in args]],
        capture_output=True, text=True, cwd=str(REPO_ROOT), timeout=120,
    )


def _judge(repo: Path, record: Path, out: Path):
    proc = _run_engine("serial-reason", "--repo", repo, "--record", record, "--json-out", out)
    envelope = json.loads(out.read_text(encoding="utf-8")) if out.is_file() else None
    return proc, envelope


def _reading(repo: Path, record: Path, out: Path):
    proc = _run_engine("reading", "--repo", repo, "--record", record, "--json-out", out)
    envelope = json.loads(out.read_text(encoding="utf-8")) if out.is_file() else None
    return proc, envelope


def _codes(envelope):
    return [finding.get("code") for finding in (envelope or {}).get("findings", [])]


def _mentions(envelope, needle: str) -> bool:
    for finding in (envelope or {}).get("findings", []):
        blob = " ".join(str(finding.get(key, "")) for key in ("subject", "message", "evidence_ptr"))
        if needle in blob:
            return True
    return False


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


# --------------------------------------------------------------------------- #
# T042 — default concurrency and the closed ordered list
# --------------------------------------------------------------------------- #
def test_default_concurrency_fixture_reads_effective_two(tmp_path):
    """Two dependency-free, disjoint-write units overlap: effective >= 2, not an estimate."""
    repo = _repo(tmp_path)
    record = _record(repo, "concurrent.yaml", [
        "requested: 2",
        "units:",
        "  - unit_id: unit-a",
        "    dispatched_at: 1000",
        "    settled_at: 1010",
        "    executor_id: exec-a",
        "    verifier_id: ver-a",
        "  - unit_id: unit-b",
        "    dispatched_at: 1005",
        "    settled_at: 1020",
        "    executor_id: exec-b",
        "    verifier_id: ver-b",
    ])
    proc, envelope = _reading(repo, record, tmp_path / "out.json")
    assert envelope is not None, proc.stdout + proc.stderr
    assert proc.returncode == 0, envelope.get("findings")
    assert _find(envelope.get("measured"), "effective") == 2


def test_every_serial_record_uses_the_closed_vocabulary_without_duplicates(tmp_path):
    statement = _vocabulary()
    vocabulary = {entry["code"] for entry in statement["codes"]}
    assert vocabulary == set(CONDITION_BOUND) | set(FACTUAL)
    repo = _repo(tmp_path)
    unknown = _record(repo, "unknown.yaml", [
        "pattern: serial", "codes:", "  - depends-on-things", "evidence:",
        "  depends-on-things: .",
    ])
    proc, envelope = _judge(repo, unknown, tmp_path / "unknown.json")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "code-unknown" in _codes(envelope), envelope.get("findings")
    assert _mentions(envelope, "depends-on-things")

    duplicated = _record(repo, "duplicated.yaml", [
        "pattern: serial", "codes:",
        "  - dependency-edge",
        "  - dependency-edge",
        "evidence:",
        "  dependency-edge:",
        "    predecessor_id: unit-a",
        "    verdict_ptr: evidence/unit-a.verdict",
    ])
    proc, envelope = _judge(repo, duplicated, tmp_path / "duplicated.json")
    assert proc.returncode == 1, "FR-006: a duplicated code must be reported"
    assert _mentions(envelope, "dependency-edge")


def test_condition_code_bijection_is_zero_gap_in_both_directions(tmp_path):
    statement = _vocabulary()
    index = statement["condition_index"]
    bound = [entry for entry in statement["codes"] if entry["group"] == "condition-bound"]
    factual = [entry for entry in statement["codes"] if entry["group"] == "factual"]
    # direction 1: every condition has exactly one code
    for condition in index:
        matching = [entry for entry in bound if entry.get("condition") == condition]
        assert len(matching) == 1, "condition %s has %d codes" % (condition, len(matching))
    # direction 2: every condition-bound code maps to exactly one indexed condition
    for entry in bound:
        assert entry.get("condition") in index, entry
    for entry in factual:
        assert "condition" not in entry, "factual %r must not carry a condition" % entry["code"]

    # the engine reports the gap when the fact is mutated (both directions of the fact)
    repo = _repo(tmp_path)
    fact = repo / "shared" / "declarations" / "facts" / "serial-reason.yaml"
    text = fact.read_text(encoding="utf-8")
    mutated = text.replace("    - FR-005(e)\n", "", 1)
    assert mutated != text, "fixture premise: the condition index must list FR-005(e)"
    fact.write_text(mutated, encoding="utf-8")
    record = _valid_record(repo, "budget-reserve")
    proc, envelope = _judge(repo, record, tmp_path / "bijection.json")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "bijection-gap" in _codes(envelope), envelope.get("findings")


# --------------------------------------------------------------------------- #
# T044 — evidence judged per code; "." rejected for every code
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("code", CONDITION_BOUND + FACTUAL)
def test_dot_evidence_is_rejected_for_every_code(tmp_path, code):
    repo = _repo(tmp_path)
    record = _record(repo, "dot.yaml", [
        "pattern: serial", "codes:", "  - %s" % code, "evidence:", "  %s: ." % code,
    ])
    proc, envelope = _judge(repo, record, tmp_path / "dot.json")
    assert proc.returncode == 1, "%s accepted a '.' as evidence" % code
    assert envelope is not None and envelope["decision"] != "pass"


def test_form_reason_inconsistency_both_directions(tmp_path):
    repo = _repo(tmp_path)
    concurrent_with_codes = _record(repo, "concurrent-codes.yaml", [
        "pattern: concurrent", "codes:", "  - single-unit", "evidence:",
        "  single-unit:", "    units:", "      - only-unit",
    ])
    proc, envelope = _judge(repo, concurrent_with_codes, tmp_path / "a.json")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "form-reason-inconsistent" in _codes(envelope), envelope.get("findings")

    serial_without_codes = _record(repo, "serial-empty.yaml", [
        "pattern: serial", "codes: []", "evidence: {}",
    ])
    proc, envelope = _judge(repo, serial_without_codes, tmp_path / "b.json")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "form-reason-inconsistent" in _codes(envelope), envelope.get("findings")


# --------------------------------------------------------------------------- #
# T046 — the four condition-bound evidence forms
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("code", CONDITION_BOUND)
def test_condition_bound_evidence_form_is_accepted_when_complete(tmp_path, code):
    repo = _repo(tmp_path)
    proc, envelope = _judge(repo, _valid_record(repo, code), tmp_path / "valid.json")
    assert envelope is not None, proc.stdout + proc.stderr
    assert proc.returncode == 0, (code, envelope.get("findings"))
    assert envelope["decision"] == "pass"


# --------------------------------------------------------------------------- #
# T047 — a budget code needs the before/after readings
# --------------------------------------------------------------------------- #
def test_budget_code_requires_measured_remaining_budget(tmp_path):
    repo = _repo(tmp_path)
    partial = _record(repo, "budget-partial.yaml", [
        "pattern: serial", "codes:", "  - budget-reserve", "evidence:",
        "  budget-reserve:", "    before:", "      slots: 3", "      budget: 120",
    ])
    proc, envelope = _judge(repo, partial, tmp_path / "partial.json")
    assert proc.returncode == 1, "a budget code without the after-reading must be red"
    assert envelope is not None and envelope["decision"] != "pass"


# --------------------------------------------------------------------------- #
# T048 — a host code needs that run's landing point
# --------------------------------------------------------------------------- #
def test_host_code_requires_a_resolving_landing_point(tmp_path):
    repo = _repo(tmp_path)
    no_landing = _record(repo, "host-no-landing.yaml", [
        "pattern: serial", "codes:", "  - host-no-parallel", "evidence:",
        "  host-no-parallel:", "    probe: nproc=1",
    ])
    proc, envelope = _judge(repo, no_landing, tmp_path / "a.json")
    assert proc.returncode == 1, "a host code without a landing point must be red"

    missing_landing = _record(repo, "host-missing-landing.yaml", [
        "pattern: serial", "codes:", "  - host-no-parallel", "evidence:",
        "  host-no-parallel:", "    probe: nproc=1",
        "    landing: evidence/no-such-probe.txt",
    ])
    proc, envelope = _judge(repo, missing_landing, tmp_path / "b.json")
    assert proc.returncode == 1, "a landing point that does not resolve must be red"


# --------------------------------------------------------------------------- #
# T049 — simplicity is not a code
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("phrase", ("simpler", "more controllable", "historically serial"))
def test_simplicity_controllability_history_are_not_codes(tmp_path, phrase):
    repo = _repo(tmp_path)
    record = _record(repo, "not-a-code.yaml", [
        "pattern: serial", "codes:", "  - %s" % phrase, "evidence:", "  %s: ." % phrase,
    ])
    proc, envelope = _judge(repo, record, tmp_path / "out.json")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "code-unknown" in _codes(envelope), envelope.get("findings")
    assert _mentions(envelope, phrase), "the offending string must be named"


# --------------------------------------------------------------------------- #
# T050 — ordered list, no loss, list length is not concurrency
# --------------------------------------------------------------------------- #
def test_two_condition_serial_records_both_codes_in_declared_order(tmp_path):
    repo = _repo(tmp_path)
    record = _record(repo, "two-conditions.yaml", [
        "pattern: serial",
        "codes:",
        "  - dependency-edge",
        "  - budget-reserve",
        "evidence:",
        "  dependency-edge:",
        "    predecessor_id: unit-a",
        "    verdict_ptr: evidence/unit-a.verdict",
        "  budget-reserve:",
        "    before:",
        "      slots: 3",
        "      budget: 120",
        "    after:",
        "      slots: 2",
        "      budget: 80",
    ])
    proc, envelope = _judge(repo, record, tmp_path / "out.json")
    assert envelope is not None, proc.stdout + proc.stderr
    assert proc.returncode == 0, envelope.get("findings")
    effective = _find(envelope.get("measured"), "effective")
    assert effective != 2, (
        "FR-006: the code-list length (2) must never be reported as concurrency: %r" % effective)
