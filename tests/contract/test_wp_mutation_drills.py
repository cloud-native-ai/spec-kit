"""Mutation drills for the Feature 070 guards (T036).

Each drill copies one implementation artifact to a temporary directory, applies
a single targeted source mutation, and runs a designated existing test against
the mutant copy. A generated pytest plugin redirects the test module's artifact
handle (``SCRIPT`` for the gate/report CLIs, ``wp_driver_sim`` for the
simulator) to the mutant copy at collection time.

A drill is only evidence when both halves hold:

- the control run (an unmutated copy) passes, proving the redirection is wired;
- the mutated run fails on an assertion, proving the named guard is load-bearing.

An anchor whose text no longer occurs exactly once fails the drill loudly; a
mutation that silently stops applying would otherwise produce a vacuous green.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
GATE = (
    REPO_ROOT
    / "skills"
    / "external"
    / "sdd-loop-driver"
    / "scripts"
    / "wp-gate.py"
)
REPORT = (
    REPO_ROOT
    / "skills"
    / "external"
    / "sdd-loop-driver"
    / "scripts"
    / "wp-report.py"
)
SIMULATOR = REPO_ROOT / "tests" / "fixtures" / "wp_driver_sim.py"

GATE_UNIT_TESTS = REPO_ROOT / "tests" / "unit" / "test_wp_gate.py"
REPORT_UNIT_TESTS = REPO_ROOT / "tests" / "unit" / "test_wp_report.py"
COORDINATION_CONTRACT_TESTS = (
    REPO_ROOT / "tests" / "contract" / "test_sdd_loop_driver_wp_coordination.py"
)

PLUGIN_TEMPLATE = '''\
import importlib
import importlib.util
import sys
from pathlib import Path

TARGET_FILE = Path({target_file!r}).resolve()
MUTANT_FILE = Path({mutant_file!r}).resolve()
ATTRIBUTE = {attribute!r}
MODE = {mode!r}


def _mutant():
    if MODE == "path":
        return MUTANT_FILE
    importlib.import_module("fixtures")
    name = "fixtures.wp_driver_sim_mutation_drill"
    spec = importlib.util.spec_from_file_location(name, MUTANT_FILE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def pytest_collection_modifyitems(config, items):
    for module in list(sys.modules.values()):
        file = getattr(module, "__file__", None)
        if file and Path(file).resolve() == TARGET_FILE:
            setattr(module, ATTRIBUTE, _mutant())
            return
    raise RuntimeError(
        "mutation target module was not collected: %s" % TARGET_FILE
    )
'''

GATE_CYCLE_ANCHOR = '''\
    if len(order) < len(graph):
        remaining = sorted(set(graph) - set(order))
        findings.append(
            _finding(
                "cycle",
                None,
                "dependency cycle among: %s" % ", ".join(remaining),
            )
        )
        return findings, []
'''

GATE_CYCLE_MUTATION = '''\
    if len(order) < len(graph):
        remaining = sorted(set(graph) - set(order))
        order.extend(remaining)
'''

SIM_WRITE_ANCHOR = '''\
        writes = [
            wp_id
            for wp_id in candidates
            if packages[wp_id]["kind"] == "write"
        ]
        if writes:
            if running:
                settle_due()
                continue
            dispatch(writes[0])
            settle_due()
            continue
'''

SIM_WRITE_MUTATION = '''\
        writes = []
'''

SIM_VERDICT_ANCHOR_ONE = '''\
        if override in VERDICT_FAILURE_CODES:
'''

SIM_VERDICT_MUTATION_ONE = '''\
        if override in VERDICT_FAILURE_CODES and override != "missing":
'''

SIM_VERDICT_ANCHOR_TWO = '''\
            value = "pass" if override == "pass" else "fail"
'''

SIM_VERDICT_MUTATION_TWO = '''\
            value = "pass" if override in ("pass", "missing") else "fail"
'''

REPORT_NOT_EVALUATED_ANCHOR = 'NOT_EVALUATED = "not_evaluated"\n'
REPORT_NOT_EVALUATED_MUTATION = "NOT_EVALUATED = 0\n"


def _write_copy(
    tmp_path: Path,
    source: Path,
    replacements,
    name: str,
) -> Path:
    """Copy ``source`` and apply exact-text replacements in order.

    Every anchor MUST occur exactly once in the current text. A refactor that
    moves the guarded code therefore turns the drill red instead of letting it
    pass without mutating anything.
    """
    text = source.read_text(encoding="utf-8")
    for old, new in replacements:
        occurrences = text.count(old)
        assert occurrences == 1, (
            "mutation anchor must occur exactly once in %s; found %d: %r"
            % (source, occurrences, old)
        )
        text = text.replace(old, new)
    destination = tmp_path / name
    destination.write_text(text, encoding="utf-8")
    return destination


def _run_node(
    tmp_path: Path,
    label: str,
    node: str,
    target_file: Path,
    mutant_file: Path,
    attribute: str,
    mode: str,
) -> subprocess.CompletedProcess:
    plugin_dir = tmp_path / ("plugin-%s" % label)
    plugin_dir.mkdir()
    (plugin_dir / "wp_mutation_drill_plugin.py").write_text(
        PLUGIN_TEMPLATE.format(
            target_file=str(target_file),
            mutant_file=str(mutant_file),
            attribute=attribute,
            mode=mode,
        ),
        encoding="utf-8",
    )
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        [str(plugin_dir)] + ([env["PYTHONPATH"]] if env.get("PYTHONPATH") else [])
    )
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "--tb=line",
            "-p",
            "wp_mutation_drill_plugin",
            node,
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        env=env,
    )


def _drill(
    tmp_path: Path,
    label: str,
    node: str,
    target_file: Path,
    source: Path,
    attribute: str,
    mode: str,
    replacements,
) -> subprocess.CompletedProcess:
    control_file = _write_copy(
        tmp_path, source, [], "%s-control.py" % label
    )
    control = _run_node(
        tmp_path, "%s-control" % label, node, target_file, control_file,
        attribute, mode,
    )
    assert control.returncode == 0, (
        "control run must pass before the mutation is evidence:\n%s\n%s"
        % (control.stdout, control.stderr)
    )
    assert "1 passed" in control.stdout, control.stdout

    mutant = _write_copy(
        tmp_path, source, replacements, "%s-mutant.py" % label
    )
    mutant_run = _run_node(
        tmp_path, "%s-mutant" % label, node, target_file, mutant, attribute, mode
    )
    assert mutant_run.returncode == 1, (
        "mutant must make the selected test fail:\n%s\n%s"
        % (mutant_run.stdout, mutant_run.stderr)
    )
    assert "1 failed" in mutant_run.stdout, mutant_run.stdout
    assert "AssertionError" in mutant_run.stdout, mutant_run.stdout
    failure_line = next(
        line
        for line in mutant_run.stdout.splitlines()
        if "AssertionError" in line
    )
    print(
        "DRILL %s: control rc=0 (1 passed); mutant rc=1 (1 failed) on %s"
        % (label, node)
    )
    print("  failure: %s" % failure_line)
    return mutant_run


@pytest.mark.contract
def test_removing_the_cycle_check_turns_the_cycle_case_red(tmp_path):
    """WG-07: deleting the cycle rejection makes the cyclic plan admissible."""
    _drill(
        tmp_path,
        "cycle-check-removed",
        "tests/unit/test_wp_gate.py::test_dependency_cycle_rejects",
        GATE_UNIT_TESTS,
        GATE,
        "SCRIPT",
        "path",
        [(GATE_CYCLE_ANCHOR, GATE_CYCLE_MUTATION)],
    )


@pytest.mark.contract
def test_allowing_write_concurrency_turns_the_write_alone_case_red(tmp_path):
    """SD-03/SD-06: letting a write share a slot with reads breaks write-alone."""
    _drill(
        tmp_path,
        "write-concurrency-allowed",
        "tests/contract/test_sdd_loop_driver_wp_coordination.py"
        "::test_sd_06_a_ready_write_is_not_starved_by_new_reads",
        COORDINATION_CONTRACT_TESTS,
        SIMULATOR,
        "wp_driver_sim",
        "module",
        [(SIM_WRITE_ANCHOR, SIM_WRITE_MUTATION)],
    )


@pytest.mark.contract
def test_treating_a_missing_verdict_as_pass_turns_the_verdict_case_red(tmp_path):
    """VI-04: a missing verdict is a fail, never an implicit pass."""
    _drill(
        tmp_path,
        "missing-verdict-treated-as-pass",
        "tests/contract/test_sdd_loop_driver_wp_coordination.py"
        "::test_vi_04_an_unusable_verdict_counts_as_fail"
        "[missing-verdict-missing]",
        COORDINATION_CONTRACT_TESTS,
        SIMULATOR,
        "wp_driver_sim",
        "module",
        [
            (SIM_VERDICT_ANCHOR_ONE, SIM_VERDICT_MUTATION_ONE),
            (SIM_VERDICT_ANCHOR_TWO, SIM_VERDICT_MUTATION_TWO),
        ],
    )


@pytest.mark.contract
def test_replacing_not_evaluated_with_zero_turns_the_report_case_red(tmp_path):
    """OR-10/FR-023: a missing metric is ``not_evaluated``, never zero."""
    _drill(
        tmp_path,
        "not-evaluated-replaced-by-zero",
        "tests/unit/test_wp_report.py"
        "::test_report_missing_timestamps_are_not_evaluated_not_zero",
        REPORT_UNIT_TESTS,
        REPORT,
        "SCRIPT",
        "path",
        [(REPORT_NOT_EVALUATED_ANCHOR, REPORT_NOT_EVALUATED_MUTATION)],
    )
