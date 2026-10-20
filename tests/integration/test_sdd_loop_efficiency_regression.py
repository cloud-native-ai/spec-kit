"""Integration test: name-level regression discovery for Feature 063.

The runner's ``--names-out`` list must make the final full run comparable to
the implement-start baseline by name (``comm -13``), so an injected failure is
reported even when the pass counters look plausible. The audit script must
reject a closure record that only compares counts.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RUNNER = REPO_ROOT / "scripts" / "bash" / "run-tests.sh"
AUDIT = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "audit-test-budget.py"

SLOT_SUMMARY = re.compile(r"slots=baseline:(\d+) closure:(\d+)")
STAGE_SUMMARY = re.compile(r"stages=(\d+) complete=(\d+)")


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


def _run_names(suite, names_out):
    completed = subprocess.run(
        ["bash", str(RUNNER), "--names-out", str(names_out), str(suite), "-q"],
        capture_output=True, text=True,
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
