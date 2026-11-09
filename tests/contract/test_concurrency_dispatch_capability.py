"""Dispatch-capability contract (contracts/judgement-engine.contract.md C-037…C-040).

Rows pinned here (WP4): T086, T087, T089.

- **T086/C-037/C-038** — each agent definition's **existing** ``capability-tools`` list is
  read and judged; the verdict names the reading it used; the engine introduces no new
  frontmatter key (a new key is not the reading and must not change the verdict).
- **T087/C-039** — the coordinator verdict is read from its fact; absent ⇒ exit 2 with
  ``owner-unavailable``, never a default; the unadjudicated fact (``decision_state`` without
  a value from ``allowed_values``) reads the same way (the fact's fail-closed window).
- **T089/C-040** — the statement-by-statement shape is reported as a finding, never
  repaired silently: a run record whose units all share one ``executor_id`` with zero
  interval overlap is ``declaration-execution-mismatch``; the verdict fact's own decided
  value is carried in the report.

Engine cases are red-first (``scripts/python/concurrency-check.py`` lands in WP2).
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "concurrency-check.py"

VERDICT_LITERALS = ("dispatch-capable", "handoff-declared", "external-process", "incapable")


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


def _agent(repo: Path, name: str, tools: str = "[]", extra_keys=(), body: str = "Never dispatch another agent.") -> Path:
    path = repo / "agents" / ("%s.agent.md" % name)
    path.parent.mkdir(parents=True, exist_ok=True)
    keys = ["name: \"%s\"" % name, "description: \"fixture agent\""]
    keys.append("capability-tools: %s" % tools)
    keys.extend(extra_keys)
    path.write_text("---\n%s\n---\n# %s\n\n%s\n" % ("\n".join(keys), name, body),
                    encoding="utf-8")
    return path


def _coordinator_fact(repo: Path, verdict=None) -> Path:
    path = repo / "shared" / "declarations" / "facts" / "coordinator-dispatch-verdict.yaml"
    text = path.read_text(encoding="utf-8")
    if verdict is not None:
        text = text.replace("  decision_state: unadjudicated\n",
                            "  decision_state: adjudicated\n  verdict: %s\n" % verdict, 1)
    path.write_text(text, encoding="utf-8")
    return path


def _repo(tmp_path: Path, verdict="forbid") -> Path:
    shutil.copytree(REPO_ROOT / "shared" / "declarations", tmp_path / "shared" / "declarations")
    if verdict is not None:
        _coordinator_fact(tmp_path, verdict)
    return tmp_path


def _record(repo: Path, name: str, lines) -> Path:
    path = repo / name
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _single_unit_record(repo: Path) -> Path:
    return _record(repo, "run.yaml", [
        "requested: 1",
        "units:",
        "  - unit_id: unit-a",
        "    executor_id: exec-a",
        "    verifier_id: ver-a",
    ])


def _capability(repo: Path, record: Path, out: Path):
    proc = _run_engine("capability", "--repo", repo, "--record", record, "--json-out", out)
    envelope = json.loads(out.read_text(encoding="utf-8")) if out.is_file() else None
    return proc, envelope


def _codes(envelope):
    return [finding.get("code") for finding in (envelope or {}).get("findings", [])]


# --------------------------------------------------------------------------- #
# T086 — the existing field is the reading; no new frontmatter key
# --------------------------------------------------------------------------- #
def test_capability_reads_the_existing_capability_tools_field(tmp_path):
    repo = _repo(tmp_path)
    _agent(repo, "fixture-worker-a", tools="[]")
    _agent(repo, "fixture-worker-b", tools="[Read, Grep]")
    record = _single_unit_record(repo)
    proc, envelope = _capability(repo, record, tmp_path / "out.json")
    assert envelope is not None, proc.stdout + proc.stderr
    assert proc.returncode in (0, 1), proc.returncode
    blob = json.dumps(envelope)
    assert "fixture-worker-a" in blob and "fixture-worker-b" in blob, (
        "each agent definition must be judged and named in the report")
    assert "capability-tools" in blob, "the verdict must name the reading it used"
    assert "incapable" in blob


def test_a_new_frontmatter_key_is_not_the_reading(tmp_path):
    repo = _repo(tmp_path)
    _agent(repo, "fixture-worker", tools="[]",
           extra_keys=("dispatch-capable: true", "concurrency-class: concurrent-by-default"))
    record = _single_unit_record(repo)
    proc, envelope = _capability(repo, record, tmp_path / "out.json")
    assert envelope is not None, proc.stdout + proc.stderr
    blob = json.dumps(envelope)
    upgraded = re.search(r"fixture-worker[\s\S]{0,400}dispatch-capable", blob) or re.search(
        r"dispatch-capable[\s\S]{0,400}fixture-worker", blob)
    assert upgraded is None, (
        "a new frontmatter key must not upgrade the verdict to dispatch-capable (C-038)")
    assert "incapable" in blob


# --------------------------------------------------------------------------- #
# T087 — the coordinator verdict is read from its fact, fail-closed
# --------------------------------------------------------------------------- #
def test_absent_coordinator_verdict_fact_is_owner_unavailable(tmp_path):
    repo = _repo(tmp_path, verdict=None)
    fact = repo / "shared" / "declarations" / "facts" / "coordinator-dispatch-verdict.yaml"
    fact.unlink()
    _agent(repo, "fixture-worker")
    record = _single_unit_record(repo)
    proc, envelope = _capability(repo, record, tmp_path / "out.json")
    combined = proc.stdout + proc.stderr + json.dumps(envelope or {})
    assert proc.returncode == 2, combined
    assert "owner-unavailable" in combined


def test_unadjudicated_verdict_fact_reads_owner_unavailable(tmp_path):
    """The live shape: decision_state without a value from allowed_values (C-039, SM-5)."""
    repo = _repo(tmp_path, verdict=None)
    _agent(repo, "fixture-worker")
    record = _single_unit_record(repo)
    proc, envelope = _capability(repo, record, tmp_path / "out.json")
    combined = proc.stdout + proc.stderr + json.dumps(envelope or {})
    assert proc.returncode == 2, combined
    assert "owner-unavailable" in combined


def test_adjudicated_verdict_is_reported_verbatim(tmp_path):
    repo = _repo(tmp_path, verdict="forbid")
    _agent(repo, "fixture-worker")
    record = _single_unit_record(repo)
    proc, envelope = _capability(repo, record, tmp_path / "out.json")
    assert envelope is not None, proc.stdout + proc.stderr
    assert "forbid" in json.dumps(envelope), "the decided value must be carried in the report"


# --------------------------------------------------------------------------- #
# T089 — statement-by-statement inconsistency is reported, never repaired
# --------------------------------------------------------------------------- #
def test_same_executor_zero_overlap_is_declaration_execution_mismatch(tmp_path):
    repo = _repo(tmp_path, verdict="forbid")
    _agent(repo, "fixture-worker")
    record = _record(repo, "mismatch.yaml", [
        "requested: 2",
        "units:",
        "  - unit_id: unit-a",
        "    executor_id: exec-a",
        "    dispatched_at: 0",
        "    settled_at: 10",
        "  - unit_id: unit-b",
        "    executor_id: exec-a",
        "    dispatched_at: 10",
        "    settled_at: 20",
    ])
    proc, envelope = _capability(repo, record, tmp_path / "out.json")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "declaration-execution-mismatch" in _codes(envelope), envelope.get("findings")
    assert "forbid" in json.dumps(envelope), "the verdict value travels with the finding"


DECLARES_UNITS = re.compile(r"declares?\s+(\d+)\s+(?:concurrent\s+)?(?:packages|units)", re.I)


def _judge_declared_units(agent_text: str, tools: list) -> list:
    """C-040 static half: a declared N>=2 with no dispatch tool and no handoff is a mismatch."""
    match = DECLARES_UNITS.search(agent_text)
    if not match or int(match.group(1)) < 2:
        return []
    if tools:
        return []
    if re.search(r"handoff|hand off|移交", agent_text, re.I):
        return []
    return [("declaration-execution-mismatch", "declared %s units, no dispatch tool" % match.group(1))]


def test_static_declaration_without_capability_is_a_mismatch():
    declaring = "This coordinator declares 6 packages and runs them."
    assert _judge_declared_units(declaring, []) == [
        ("declaration-execution-mismatch", "declared 6 units, no dispatch tool")]
    assert _judge_declared_units(declaring, ["Task"]) == []
    assert _judge_declared_units(declaring + " Handoff to the driver.", []) == []
    assert _judge_declared_units("This coordinator declares 1 package.", []) == []
