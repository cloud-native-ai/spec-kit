"""The 092 reproduction fixture (SC-005, C-040; row T090).

**What "092" means here**: Feature **092-goal-team-parallel** (the 6-package plan), not
the 092-non-disposable row absorbed into 090 by the 2026-11-09 merge — the numbering
collision is recorded as F-093-019 and this filename is kept because renaming it would
break every reference (tasks.md T090).

**The defect being reproduced**: a coordinator declared six packages, the executing
body's ``capability-tools`` list carried no dispatch tool, no handoff was declared, and
all six units returned through one executor in sequence. Before Feature 093 landed the
capability judgement this shape was silently accepted; after it, the shape is refused
with ``declaration-execution-mismatch`` on both readings — the static declaration and
the run record. The red-first reading (engine absent → the module could not run; the
092 run itself accepted the shape) is recorded in
``test-evidence/wp4-red-first-modules.txt``; the post-repair reading is this module
green plus ``test-evidence/wp5-t090-reproduction-092.txt``.

The verdict value used in these fixtures (``forbid``) is a **test input** that exercises
the reader; it does not decide the owner's ruling, which stays unadjudicated in the
live ``coordinator-dispatch-verdict.yaml`` (C-016, F-093-003).
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

from script_api import run_engine_in_process

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "concurrency-check.py"

PACKAGES = ("wp01", "wp02", "wp03", "wp04", "wp05", "wp06")


# --------------------------------------------------------------------------- #
# fixtures
# --------------------------------------------------------------------------- #
def _repo(tmp_path: Path, verdict: str = "forbid") -> Path:
    shutil.copytree(REPO_ROOT / "shared" / "declarations", tmp_path / "shared" / "declarations")
    fact = tmp_path / "shared" / "declarations" / "facts" / "coordinator-dispatch-verdict.yaml"
    text = fact.read_text(encoding="utf-8")
    text = text.replace(
        "  decision_state: unadjudicated\n",
        "  decision_state: adjudicated\n  verdict: %s\n" % verdict, 1)
    fact.write_text(text, encoding="utf-8")
    return tmp_path


def _agent(repo: Path, name: str, tools: str, body: str) -> Path:
    path = repo / "agents" / ("%s.agent.md" % name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\nname: \"%s\"\ndescription: \"092 reproduction fixture\"\n"
        "capability-tools: %s\n---\n# %s\n\n%s\n" % (name, tools, name, body),
        encoding="utf-8")
    return path


def _six_package_record(repo: Path, executor: str = "exec-one") -> Path:
    """The 092 run shape: six units, one executor, sequential (non-overlapping) intervals."""
    lines = ["declared_body: agents/coordinator.agent.md", "declared_units: 6", "units:"]
    for index, package in enumerate(PACKAGES):
        lines.extend([
            "  - unit_id: %s" % package,
            "    executor_id: %s" % executor,
            "    verifier_id: ver-%s" % package,
            "    dispatched_at: %d" % (index * 10),
            "    settled_at: %d" % (index * 10 + 8),
            "    verdict: pass",
            "    evidence_ptr: evidence/%s.txt" % package,
        ])
    path = repo / "run-092.yaml"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _capability(repo: Path, record: Path, out: Path):
    proc = run_engine_in_process(
        ENGINE,
        ["capability", "--repo", str(repo), "--record", str(record), "--json-out", str(out)],
    )
    envelope = json.loads(out.read_text(encoding="utf-8")) if out.is_file() else None
    return proc, envelope


def _codes(envelope) -> list:
    return [finding.get("code") for finding in (envelope or {}).get("findings", [])]


# --------------------------------------------------------------------------- #
# T090 — the 092 shape is red before the repair, green after
# --------------------------------------------------------------------------- #
def test_the_092_shape_is_refused_on_both_readings(tmp_path):
    """The six-package declaration by an incapable coordinator is a mismatch, not a silent serial run."""
    repo = _repo(tmp_path)
    _agent(repo, "coordinator", tools="[Read, Grep, Glob, Bash, Write, Edit]",
           body="Never dispatch another agent. Plans six packages and returns them serially.")
    record = _six_package_record(repo)
    proc, envelope = _capability(repo, record, tmp_path / "cap.json")

    assert proc.returncode == 1, "the 092 shape must be red: %s" % (proc.stdout + proc.stderr)
    mismatch = [code for code in _codes(envelope) if code == "declaration-execution-mismatch"]
    assert len(mismatch) >= 2, (
        "both statements must be judged: the static declaration AND the run record "
        "(findings: %r)" % envelope.get("findings"))
    combined = json.dumps(envelope)
    assert "capability-tools" in combined, "the finding names the field it read"
    assert "exec-one" in combined, "the record finding names the single executor"
    assert "forbid" in combined, "the verdict value travels with the finding"


def test_a_dispatch_capable_coordinator_passes_the_same_record_shape(tmp_path):
    """The repaired form: a dispatch tool in the existing key — the static half is clean."""
    repo = _repo(tmp_path)
    _agent(repo, "coordinator", tools="[Agent, Read, Grep]",
           body="Dispatches one child per package through the fork carrier.")
    record = _six_package_record(repo)
    proc, envelope = _capability(repo, record, tmp_path / "cap.json")

    # The run record still shows one executor in sequence — that half stays red by design.
    assert proc.returncode == 1, proc.stdout + proc.stderr
    findings = envelope.get("findings", [])
    static = [finding for finding in findings
              if finding.get("subject") == "agents/coordinator.agent.md"]
    assert not static, (
        "a dispatch-capable coordinator must not carry the static mismatch: %r" % static)
    assert any(finding.get("code") == "declaration-execution-mismatch"
               and finding.get("subject") != "agents/coordinator.agent.md"
               for finding in findings), findings


def test_a_handoff_declaration_is_the_second_legal_form(tmp_path):
    """A body that hands dispatch to a capable superior is not a static mismatch."""
    repo = _repo(tmp_path)
    _agent(repo, "coordinator", tools="[Read, Grep, Glob]",
           body="Handoff: dispatch of the six packages is delegated to the driver.")
    record = _six_package_record(repo)
    proc, envelope = _capability(repo, record, tmp_path / "cap.json")
    static = [finding for finding in envelope.get("findings", [])
              if finding.get("subject") == "agents/coordinator.agent.md"]
    assert not static, "a declared handoff is a legal form (C-037): %r" % static


def test_an_honestly_concurrent_record_has_no_mismatch(tmp_path):
    """The repaired execution: two executors with overlapping intervals is not a mismatch."""
    repo = _repo(tmp_path)
    _agent(repo, "coordinator", tools="[Agent]", body="Dispatches siblings through the fork carrier.")
    record = repo / "run-repaired.yaml"
    record.write_text(
        "declared_body: agents/coordinator.agent.md\n"
        "declared_units: 2\n"
        "units:\n"
        "  - unit_id: wp01\n    executor_id: exec-a\n    verifier_id: ver-1\n"
        "    dispatched_at: 0\n    settled_at: 10\n    verdict: pass\n"
        "    evidence_ptr: evidence/wp01.txt\n"
        "  - unit_id: wp02\n    executor_id: exec-b\n    verifier_id: ver-2\n"
        "    dispatched_at: 5\n    settled_at: 15\n    verdict: pass\n"
        "    evidence_ptr: evidence/wp02.txt\n",
        encoding="utf-8")
    proc, envelope = _capability(repo, record, tmp_path / "cap.json")
    assert proc.returncode == 0, envelope.get("findings")
    assert "declaration-execution-mismatch" not in _codes(envelope)
