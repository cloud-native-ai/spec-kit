"""High-order executor contract (contracts/high-order-executors.contract.md C-093/C-094, C-025).

Rows pinned here (WP4): T029, T091, T141, T143.

- **T029/C-025** — each class's obligation text is reachable from the body's own text or its
  declared ``owner_anchor``; an anchor that does not resolve is ``obligation-missing`` (red).
- **T091/SC-011** — anti-nesting is preserved: the permitted chain is depth 2, the stage
  executor still MUST NOT start or host any SDD run, and the existing subagent taxonomy keeps
  its shape (the obligation attaches, never replaces); a stage body made able to carry the
  driver turns the judgement red.
- **T141/C-093** — the ``analyze`` stage defaults to N >= 2 concurrent SDD Analysis Workers:
  pre-dispatch file-level read domains with an intersection red before dispatch, deterministic
  consolidation (read-domain order → finding id order → first declaration), and the reading
  triple plus executor/verifier ids recorded. Reverting the default to ``off`` turns the
  judgement red.
- **T143/C-094** — the fork carrier's invocation shape is asserted against
  ``stage-runner.sh --help`` (prompt through stdin, ``--output-format stream-json``, sentinel);
  the pool bound is the runtime ``nproc`` reading, never a frozen constant; an in-process
  fan-out record is rejected as the concurrency mechanism.

Engine cases are red-first (``scripts/python/concurrency-check.py`` lands in WP2); the
document-shape cases turn green when the FR-034/FR-035 rows land (WP3).
"""
from __future__ import annotations

import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from script_api import run_engine_in_process

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "concurrency-check.py"
READER = REPO_ROOT / "scripts" / "python" / "declaration_reader.py"
STAGE_RUNNER = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "stage-runner.sh"
DRIVER_SKILL = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "SKILL.md"
DRIVER_RECIPES = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "references" / "dispatch-recipes.md"
SUBAGENT_DEFS = REPO_ROOT / "shared" / "definitions" / "subagent-definitions.md"

#: The three prohibitions the depth-2 chain carries (owner: 074's governance section).
PROHIBITIONS = (
    "MUST NOT start or host any SDD run",
    "MUST NOT itself be an SDD invocation host",
    "SDD-within-SDD recursion is prohibited",
)


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _run_engine(*args):
    assert ENGINE.is_file(), (
        "red-first: scripts/python/concurrency-check.py is the WP2 engine target and is "
        "not in this worktree yet")
    return run_engine_in_process(ENGINE, [str(arg) for arg in args])


def _reader_module():
    spec = importlib.util.spec_from_file_location("declaration_reader", READER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _codes(envelope):
    return [finding.get("code") for finding in (envelope or {}).get("findings", [])]


# --------------------------------------------------------------------------- #
# T029 — obligation presence through the body or its owner anchor
# --------------------------------------------------------------------------- #
def _mini_repo(tmp_path: Path, broken_anchor: bool) -> Path:
    repo = tmp_path / "repo"
    shutil.copytree(REPO_ROOT / "shared" / "declarations", repo / "shared" / "declarations")
    if broken_anchor:
        fact = repo / "shared" / "declarations" / "facts" / "concurrency-class.yaml"
        text = fact.read_text(encoding="utf-8")
        mutated = text.replace(
            "owner_anchor: shared/definitions/subagent-definitions.md#class-concurrent-by-default",
            "owner_anchor: shared/definitions/no-such-owner.md#class-concurrent-by-default", 1)
        assert mutated != text, "fixture premise: the concurrent-by-default anchor must exist"
        fact.write_text(mutated, encoding="utf-8")
    bodies = {
        "skills/internal/fixture-skill/SKILL.md":
            "---\nname: fixture-skill\n---\n# Fixture Skill\n\nNo obligation text here.\n",
        "templates/commands/fixture.md": "# Fixture command\n\nNo obligation text here.\n",
        "agents/fixture.agent.md":
            "---\nname: fixture\ncapability-tools: []\n---\n# Fixture agent\n\nNo obligation.\n",
        ".specify/teams/fixture/team.md": "# Fixture team\n",
        ".specify/anchoring/fixture/goal.md": "# Fixture goal\n",
    }
    for rel, text in bodies.items():
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return repo


def test_unresolvable_owner_anchor_is_obligation_missing(tmp_path):
    repo = _mini_repo(tmp_path, broken_anchor=True)
    proc = _run_engine("classify", "--repo", repo, "--json-out", tmp_path / "out.json")
    envelope = None
    if (tmp_path / "out.json").is_file():
        envelope = json.loads((tmp_path / "out.json").read_text(encoding="utf-8"))
    assert proc.returncode != 0, "a bare body with an unresolvable anchor must be red"
    if envelope is not None:
        assert "obligation-missing" in _codes(envelope) or envelope["decision"] == "fail", (
            envelope.get("findings"))


def test_live_tree_has_no_obligation_missing_finding(tmp_path):
    proc = _run_engine("classify", "--repo", REPO_ROOT, "--json-out", tmp_path / "out.json")
    envelope = json.loads((tmp_path / "out.json").read_text(encoding="utf-8"))
    assert "obligation-missing" not in _codes(envelope), envelope.get("findings")
    assert envelope["decision"] == "pass", envelope.get("findings")


# --------------------------------------------------------------------------- #
# T091 — anti-nesting preservation and the taxonomy shape
# --------------------------------------------------------------------------- #
def _judge_anti_nesting(text: str) -> list:
    findings = []
    if "depth 2" not in text:
        findings.append(("anti-nesting", "the permitted chain must state depth 2"))
    for prohibition in PROHIBITIONS:
        if prohibition not in text:
            findings.append(("anti-nesting", "missing prohibition: %s" % prohibition))
    return findings


def test_anti_nesting_chain_is_depth_two_with_its_three_prohibitions():
    assert _judge_anti_nesting(SUBAGENT_DEFS.read_text(encoding="utf-8")) == []
    tampered = SUBAGENT_DEFS.read_text(encoding="utf-8").replace(
        "MUST NOT start or host any SDD run", "MAY carry the driver", 1)
    assert _judge_anti_nesting(tampered), (
        "a stage body made able to carry the driver must turn the judgement red")


def test_subagent_taxonomy_keeps_its_shape():
    text = SUBAGENT_DEFS.read_text(encoding="utf-8")
    for heading in ("## What a Subagent Is", "## Three Execution Modes", "## Mode Selection"):
        assert heading in text, "taxonomy section lost: %s" % heading
    agents = sorted((REPO_ROOT / "agents").glob("*.agent.md"))
    assert agents, "the agent definitions must exist"
    for path in agents:
        frontmatter = path.read_text(encoding="utf-8").split("\n---", 1)[0]
        assert "name:" in frontmatter and "capability-tools:" in frontmatter, path
        assert "dispatch-carrier:" not in frontmatter, (
            "the obligation attaches to the existing taxonomy; no new carrier key: %s" % path)


# --------------------------------------------------------------------------- #
# T141 — the analyze wave
# --------------------------------------------------------------------------- #
def _analyze_text(root: Path):
    return "\n".join([
        (root / "skills" / "external" / "sdd-loop-driver" / "SKILL.md").read_text(encoding="utf-8"),
        (root / "skills" / "external" / "sdd-loop-driver" / "references"
         / "dispatch-recipes.md").read_text(encoding="utf-8"),
    ])


def _analyze_stage(root: Path):
    fact = _reader_module().load_fact(
        str(root), "decomposition-coverage")["body"]["statement"]
    for stage in fact["stages"]:
        if stage["stage"] == "analyze":
            return stage
    raise AssertionError("decomposition-coverage.yaml must declare the analyze stage")


def _judge_analyze(root: Path) -> list:
    findings = []
    stage = _analyze_stage(root)
    if stage.get("coverage") != "on":
        findings.append(("analyze-default", "analyze must default to concurrent coverage 'on'"))
    if not stage.get("concurrency_source"):
        findings.append(("analyze-default", "N must resolve from the stage team configuration / spine"))
    text = _analyze_text(root)
    required = (
        ("sdd-analysis-worker|SDD Analysis Worker", "the analyze Worker definition must be named"),
        ("并发|concurrent", "the N-way concurrency must be stated"),
        ("读域|read domain|read-domain", "each Worker's read domain must be declared"),
        ("相交|intersect", "a read-domain intersection must be red before dispatch"),
        ("确定性|deterministic", "consolidation must be deterministic"),
        ("finding id", "consolidation orders by finding id"),
        ("first declaration|先声明", "duplicate ids break by first declaration"),
        ("requested", "the reading triple records requested concurrency"),
        ("effective_reason|effective reason|effective-reason", "the reading triple records the effective reason"),
        ("executor_id|executor id", "each Worker's executor id is recorded"),
        ("verifier_id|verifier id", "each verdict's verifier id is recorded"),
    )
    for pattern, message in required:
        if not re.search(pattern, text):
            findings.append(("analyze-wave", message))
    return findings


def test_analyze_wave_contract_on_the_live_tree():
    assert _judge_analyze(REPO_ROOT) == []


def test_reverting_analyze_to_off_turns_the_judgement_red(tmp_path):
    root = tmp_path / "tree"
    for rel in (
        "shared/declarations",
        "skills/external/sdd-loop-driver/SKILL.md",
        "skills/external/sdd-loop-driver/references/dispatch-recipes.md",
    ):
        source = REPO_ROOT / rel
        target = root / rel
        if source.is_dir():
            shutil.copytree(source, target)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    fact = root / "shared" / "declarations" / "facts" / "decomposition-coverage.yaml"
    text = fact.read_text(encoding="utf-8")
    mutated = text.replace("    - stage: analyze\n      coverage: on\n",
                           "    - stage: analyze\n      coverage: off\n", 1)
    assert mutated != text, "fixture premise: the analyze stage must default to on"
    fact.write_text(mutated, encoding="utf-8")
    findings = _judge_analyze(root)
    assert any(code == "analyze-default" for code, _ in findings), findings


# --------------------------------------------------------------------------- #
# T143 — the fork mechanism
# --------------------------------------------------------------------------- #
def test_stage_runner_help_carries_the_invocation_shape():
    proc = subprocess.run(["bash", str(STAGE_RUNNER), "--help"],
                          capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, proc.stderr
    help_text = proc.stdout
    for token in ("--prompt-file", "--sentinel", "--mode", "stdin"):
        assert token in help_text, "the runner --help must document %r" % token
    source = STAGE_RUNNER.read_text(encoding="utf-8")
    assert "--output-format stream-json" in source, (
        "the runner invocation shape is --output-format stream-json")
    assert re.search(r'<\s*"\$PROMPT_FILE"', source), (
        "the prompt must be fed through stdin, not interpolated into argv")


def _judge_pool_bound(text: str) -> list:
    findings = []
    if "nproc" not in text:
        findings.append(("pool-bound", "the pool bound must be the host nproc reading"))
        return findings
    window = re.search(r".{0,160}nproc.{0,160}", text)
    near = window.group(0) if window else ""
    if not re.search(r"运行期|runtime|at dispatch|派发时|派发时读取", near):
        findings.append(("pool-bound", "nproc must be read at runtime, never frozen"))
    if re.search(r"nproc\s*[=:]\s*\d+|固化|frozen", near):
        findings.append(("pool-bound", "a frozen nproc value is a defect"))
    return findings


def test_pool_bound_is_a_runtime_reading():
    text = DRIVER_SKILL.read_text(encoding="utf-8") + DRIVER_RECIPES.read_text(encoding="utf-8")
    assert _judge_pool_bound(text) == []
    frozen = "The pool bound is nproc = 8, fixed in the configuration."
    assert _judge_pool_bound(frozen), "freezing nproc into a file must turn the judgement red"


def _judge_mechanism(record: dict) -> list:
    allowed = {"fork", "subprocess"}
    mechanism = str(record.get("mechanism", "")).strip().lower()
    if mechanism in allowed:
        return []
    return [("mechanism-not-allowed",
             "the concurrency mechanism %r is not one of the two legal carriers" % mechanism)]


def test_in_process_fanout_is_not_a_concurrency_mechanism():
    assert _judge_mechanism({"mechanism": "fork"}) == []
    assert _judge_mechanism({"mechanism": "subprocess"}) == []
    assert _judge_mechanism({"mechanism": "in-process"}), (
        "the host-internal in-process fan-out is BANNED as a concurrency carrier")
