"""Integration test: name-level regression discovery for Feature 063.

The runner's ``--names-out`` list must make the final full run comparable to
the implement-start baseline by name (``comm -13``), so an injected failure is
reported even when the pass counters look plausible. The audit script must
reject a closure record that only compares counts.

Feature 086 adds the nested-invocation case: the same ``--names-out`` surface
must survive a run that is already inside a parallel worker. The runner then
runs serially (``reason=nested``), derives no second worker pool, and still
writes exactly one list and one exit code — which is what keeps a nested
driver call comparable to a serial baseline by name.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RUNNER = REPO_ROOT / "scripts" / "bash" / "run-tests.sh"
AUDIT = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "audit-test-budget.py"

SLOT_SUMMARY = re.compile(r"slots=baseline:(\d+) closure:(\d+)")
STAGE_SUMMARY = re.compile(r"stages=(\d+) complete=(\d+)")
MODE_LINE = re.compile(r"^# test runner: mode=(?P<mode>\w+)(?P<rest>.*)$", re.M)
LIST_LINE = re.compile(
    r"^# failed-name list written: (?P<path>.+?) \((?P<n>\d+) entries\) passes=(?P<k>\d+)$", re.M
)
COMMAND_LINE = re.compile(r"^# test runner: .* -m pytest ", re.M)


def _write_suite(root, failing=False):
    suite = root / "suite"
    suite.mkdir(parents=True, exist_ok=True)
    (suite / "test_sample.py").write_text(
        "def test_one():\n"
        "    assert True\n"
        "\n"
        "def test_two():\n"
        "    assert %s\n" % ("False" if failing else "True"),
        encoding="utf-8",
    )
    return suite


def _run_names(suite, names_out, env_extra=None):
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    # The mode the runner must DECIDE is the subject here: an inherited
    # PYTEST_XDIST_WORKER (pytest exports it for every worker's own children) would make
    # every case observe the nested branch instead of the branch under test.
    env.pop("PYTEST_XDIST_WORKER", None)
    if env_extra is not None:
        env.update(env_extra)
    completed = subprocess.run(
        ["bash", str(RUNNER), "--names-out", str(names_out), str(suite), "-q"],
        capture_output=True, text=True, env=env,
    )
    return completed


def _names(path):
    return [line.strip() for line in Path(path).read_text(encoding="utf-8").splitlines()
            if line.strip()]


def test_injected_regression_found_by_name_diff(tmp_path):
    suite = _write_suite(tmp_path, failing=False)
    baseline = tmp_path / "baseline-failed.txt"
    first = _run_names(suite, baseline)
    assert first.returncode == 0, first.stdout + first.stderr
    assert _names(baseline) == []

    (suite / "test_sample.py").write_text(
        "def test_one():\n"
        "    assert True\n"
        "\n"
        "def test_two():\n"
        "    assert False\n",
        encoding="utf-8",
    )
    final = tmp_path / "final-failed.txt"
    second = _run_names(suite, final)
    assert second.returncode == 1
    new_failures = [name for name in _names(final) if name not in _names(baseline)]
    assert new_failures, "name-level diff found no injected failure"
    assert any("test_two" in name for name in new_failures)

    spine = tmp_path / "spine.md"
    spine.write_text(
        "# Spine\n\n<!-- test-budget:begin -->\n"
        + json.dumps({
            "seq": 1, "slot": "baseline", "stage": "implement", "purpose": "baseline",
            "trigger": "scheduled", "at": 1,
            "command": "bash scripts/bash/run-tests.sh --names-out baseline.txt",
            "selection_basis": "full-suite", "rc": 0, "passed": 2, "failed": 0,
            "failed_names_path": "baseline.txt", "baseline_compare": "na",
            "evidence_ptr": "baseline.log", "merge_source": "na", "merged_at": "na",
        }) + "\n" + json.dumps({
            "seq": 2, "slot": "closure", "stage": "review", "purpose": "closure",
            "trigger": "scheduled", "at": 2,
            "command": "bash scripts/bash/run-tests.sh --names-out final.txt",
            "selection_basis": "full-suite", "rc": 1, "passed": 1, "failed": 1,
            "failed_names_path": "final.txt",
            "baseline_compare": "failed count 0 vs 1",
            "evidence_ptr": "closure.log", "merge_source": "na", "merged_at": "na",
        }) + "\n<!-- test-budget:end -->\n",
        encoding="utf-8",
    )
    audited = subprocess.run(
        [sys.executable, str(AUDIT), "--spine", str(spine),
         "--spec-dir", str(tmp_path / "spec")],
        capture_output=True, text=True,
    )
    assert audited.returncode == 1, audited.stdout + audited.stderr
    assert "baseline_compare" in (audited.stdout + audited.stderr)
    assert SLOT_SUMMARY.search(audited.stdout)
    assert STAGE_SUMMARY.search(audited.stdout)


# ---------------------------------------------------------------- 086 nested runner
# C-005 / C-013 / C-014 / C-015 of
# `.specify/specs/086-efficient-test-execution/contracts/runner-contract-086.contract.md`:
# a runner invoked from inside an xdist worker must not fork a second pool, and the
# name-level comparison surface must be identical to the one a top-level run produces.


def test_nested_run_is_serial_and_writes_one_comparable_list(tmp_path):
    """`PYTEST_XDIST_WORKER` set → serial with `reason=nested`, exactly one list/exit code.

    The assertion that matters for this feature is the *comparability* one: the list a
    nested run writes is the same single sorted, de-duplicated `FAILED` name list a serial
    run writes, written by exactly one pass, so `comm -13` against a baseline stays
    meaningful no matter which topology produced the closure record.
    """
    suite = _write_suite(tmp_path, failing=True)
    names = tmp_path / "nested-failed.txt"
    nested = _run_names(suite, names, env_extra={"PYTEST_XDIST_WORKER": "gw0"})

    assert nested.returncode == 1, nested.stdout + nested.stderr
    match = MODE_LINE.search(nested.stderr)
    assert match is not None, f"no mode line on stderr:\n{nested.stderr}"
    assert match.group("mode") == "serial", nested.stderr
    assert "reason=nested" in match.group("rest"), match.group("rest")
    assert "PYTEST_XDIST_WORKER=gw0" in match.group("rest"), match.group("rest")

    # One command header, describing the command actually executed: serial, no pool.
    headers = COMMAND_LINE.findall(nested.stderr)
    assert len(headers) == 1, nested.stderr
    header_line = next(
        line for line in nested.stderr.splitlines() if COMMAND_LINE.match(line)
    )
    assert "-n0" in header_line, header_line
    assert "-n auto" not in header_line, header_line
    assert "--dist" not in header_line, header_line

    # Exactly one list, one pass, one failure name — not one per (non-existent) pool.
    lists = LIST_LINE.findall(nested.stderr)
    assert len(lists) == 1, nested.stderr
    written = LIST_LINE.search(nested.stderr)
    assert int(written.group("k")) == 1, written.group(0)
    assert int(written.group("n")) == 1, written.group(0)
    assert [name.rsplit("::", 1)[-1] for name in _names(names)] == ["test_two"], _names(names)

    # The same selection with no worker in the environment yields the same list, so the
    # nested run is comparable to a top-level one by name.
    top_names = tmp_path / "top-failed.txt"
    top = _run_names(suite, top_names)
    assert top.returncode == 1, top.stdout + top.stderr
    assert _names(top_names) == _names(names)
