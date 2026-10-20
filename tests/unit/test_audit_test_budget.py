"""Unit tests for skills/external/sdd-loop-driver/scripts/audit-test-budget.py.

Red-first: the script does not exist yet; every audit invocation fails.
The ledger authority is the ``<!-- test-budget:begin/end -->`` JSONL fence in
the line state spine; ``<spec-dir>/test-evidence/`` only carries E3 rows.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "audit-test-budget.py"

SLOT_SUMMARY = re.compile(
    r"slots=baseline:(\d+) closure:(\d+) reruns=(\d+) exceptions=(\d+) "
    r"unknown=(\d+)(?: environment_failures=(\d+))?")
STAGE_SUMMARY = re.compile(r"stages=(\d+) complete=(\d+)")

FULL_COMMAND = "bash scripts/bash/run-tests.sh --names-out names.txt"
CLOSURE_COMPARE = "comm -13 baseline.txt final.txt -> 0 new failures"

ADMISSION = [
    "decision=fast-lane",
    "entry_evidence=fast-lane=opt-in",
    "decided_at=2026-10-20T00:00:00Z",
    "measured.fr_count=12",
    "measured.task_count=25",
    "checklist=skipped(fast-lane)",
]


def _row(seq, slot, **overrides):
    base = {
        "seq": seq,
        "slot": slot,
        "stage": "implement" if slot == "baseline" else "review",
        "purpose": "fixture",
        "trigger": "scheduled",
        "at": "2026-10-20T00:00:00Z",
        "command": FULL_COMMAND,
        "selection_basis": "full-suite",
        "rc": 0,
        "passed": 10,
        "failed": 0,
        "failed_names_path": "names.txt",
        "baseline_compare": "na",
        "evidence_ptr": "logs/run.log",
        "merge_source": "na",
        "merged_at": "na",
    }
    if slot == "closure":
        base["baseline_compare"] = CLOSURE_COMPARE
    base.update(overrides)
    return base


def _write_spine(tmp_path, rows, admission=None, name="spine.md", raw_tail=""):
    lines = ["# Line State Spine", ""]
    if admission is not None:
        lines.append("## Admission (E1)")
        lines.append("")
        lines.append("```text")
        lines.extend(admission)
        lines.append("```")
        lines.append("")
    lines.append("<!-- test-budget:begin -->")
    for row in rows:
        lines.append(json.dumps(row, ensure_ascii=False))
    lines.append("<!-- test-budget:end -->")
    if raw_tail:
        lines.append("")
        lines.append(raw_tail)
    path = tmp_path / name
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _evidence(spec_dir, stage, rows):
    target = Path(spec_dir) / "test-evidence"
    target.mkdir(parents=True, exist_ok=True)
    (target / ("%s.jsonl" % stage)).write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8")


def _stage_status(stage, status="ran", **overrides):
    row = {
        "stage": stage,
        "row_type": "stage-status",
        "status": status,
        "command": "bash scripts/bash/run-tests.sh tests/unit/test_x.py -q",
        "selection_basis": "targeted-set-v1 (a) changed-path coverage",
        "selected_paths": ["tests/unit/test_x.py"],
        "sufficiency": "the selected test covers the changed surface",
        "rc": 0,
        "passed": 1,
        "failed": 0,
        "new_failures": [],
        "baseline": "na",
        "changed_paths": [],
        "evidence_ptr": "logs/stage.log",
    }
    if status == "not-run-docs-only":
        row = {
            "stage": stage,
            "row_type": "stage-status",
            "status": status,
            "selection_basis": "targeted-set-v1: documentation-only change",
            "changed_paths": ["docs/notes.md"],
            "evidence_ptr": "logs/stage.log",
        }
    if status == "not-applicable-skipped-stage":
        row = {
            "stage": stage,
            "row_type": "stage-status",
            "status": status,
            "selection_basis": "E1 fast-lane admission + checklist=skipped(fast-lane)",
            "selected_paths": [],
            "sufficiency": "stage skipped by the ratified fast lane",
            "evidence_ptr": "spine.md#admission",
        }
    if status == "empty-selection-escalated":
        row = {
            "stage": stage,
            "row_type": "stage-status",
            "status": status,
            "selection_basis": "targeted-set-v1 produced an empty set",
            "selected_paths": [],
            "sufficiency": "expanded to the contract family per FR-013",
            "evidence_ptr": "logs/stage.log",
        }
    row.update(overrides)
    return row


def _write_all_stage_evidence(spec_dir, checklist="ran", overrides=None):
    overrides = overrides or {}
    for stage in ("clarify", "plan", "tasks", "checklist", "analyze", "review"):
        if stage == "checklist" and checklist == "skipped":
            rows = [_stage_status(stage, "not-applicable-skipped-stage")]
        else:
            rows = [_stage_status(stage, **overrides.get(stage, {}))]
        _evidence(spec_dir, stage, rows)


def _run(spine, spec_dir, logs_dir=None, stage_check=None):
    cmd = [sys.executable, str(SCRIPT), "--spine", str(spine), "--spec-dir", str(spec_dir)]
    if logs_dir is not None:
        cmd += ["--logs-dir", str(logs_dir)]
    if stage_check is not None:
        cmd += ["--stage-check", stage_check]
    return subprocess.run(cmd, capture_output=True, text=True)


def _slots(completed):
    match = SLOT_SUMMARY.search(completed.stdout)
    assert match, "summary line missing; stdout=%r stderr=%r" % (
        completed.stdout, completed.stderr)
    return {
        "baseline": int(match.group(1)),
        "closure": int(match.group(2)),
        "reruns": int(match.group(3)),
        "exceptions": int(match.group(4)),
        "unknown": int(match.group(5)),
        "environment_failures": int(match.group(6) or 0),
    }


def _stages(completed):
    match = STAGE_SUMMARY.search(completed.stdout)
    assert match, "stage summary missing; stdout=%r" % completed.stdout
    return int(match.group(1)), int(match.group(2))


def test_valid_two_slot_ledger(tmp_path):
    spec = tmp_path / "spec"
    _write_all_stage_evidence(spec)
    spine = _write_spine(tmp_path, [_row(1, "baseline"), _row(2, "closure")])
    completed = _run(spine, spec)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert _slots(completed)["baseline"] == 1
    assert _slots(completed)["closure"] == 1
    assert _slots(completed)["unknown"] == 0
    assert _stages(completed) == (6, 6)


def test_summary_shape(tmp_path):
    spec = tmp_path / "spec"
    _write_all_stage_evidence(spec)
    spine = _write_spine(tmp_path, [_row(1, "baseline"), _row(2, "closure")])
    completed = _run(spine, spec)
    assert completed.returncode == 0
    assert SLOT_SUMMARY.search(completed.stdout)
    assert STAGE_SUMMARY.search(completed.stdout)


def test_out_of_slot_without_exception_fails(tmp_path):
    spec = tmp_path / "spec"
    _write_all_stage_evidence(spec)
    row = _row(2, "out-of-slot-exception", stage="analyze",
               exception_reason="", evidence_ptr="")
    spine = _write_spine(tmp_path, [_row(1, "baseline"), _row(2, "closure"), row])
    completed = _run(spine, spec)
    assert completed.returncode == 1
    assert "exception_reason" in (completed.stdout + completed.stderr)


def test_out_of_slot_with_exception_passes(tmp_path):
    spec = tmp_path / "spec"
    _write_all_stage_evidence(spec)
    row = _row(3, "out-of-slot-exception", stage="analyze",
               exception_reason="shared engine changed", evidence_ptr="logs/analyze.log")
    spine = _write_spine(tmp_path, [_row(1, "baseline"), _row(2, "closure"), row])
    completed = _run(spine, spec)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert _slots(completed)["exceptions"] == 1


def test_rerun_only_after_closure(tmp_path):
    spec = tmp_path / "spec"
    _write_all_stage_evidence(spec)
    before_rerun = _row(2, "in-slot-rerun", stage="review", trigger="closure-fix")
    before = _write_spine(tmp_path, [_row(1, "baseline"), before_rerun], name="before.md")
    completed = _run(before, spec)
    assert completed.returncode == 1

    after_rerun = _row(3, "in-slot-rerun", stage="review", trigger="closure-fix")
    after = _write_spine(tmp_path, [_row(1, "baseline"), _row(2, "closure"), after_rerun],
                         name="after.md")
    completed = _run(after, spec)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert _slots(completed)["reruns"] == 1


def test_third_slot_rejected(tmp_path):
    spec = tmp_path / "spec"
    _write_all_stage_evidence(spec)
    spine = _write_spine(tmp_path, [
        _row(1, "baseline"),
        _row(2, "baseline", stage="implement"),
        _row(3, "closure"),
    ])
    completed = _run(spine, spec)
    assert completed.returncode == 1

    spine2 = _write_spine(tmp_path, [
        _row(1, "baseline"), _row(2, "closure"), _row(3, "closure"),
    ], name="two-closure.md")
    completed2 = _run(spine2, spec)
    assert completed2.returncode == 1


def test_environment_failure_no_slot(tmp_path):
    spec = tmp_path / "spec"
    _write_all_stage_evidence(spec)
    env_row = _row(2, "environment-failure", stage="plan",
                   environment_evidence="interpreter missing: python3.8 not found")
    spine = _write_spine(tmp_path, [_row(1, "baseline"), env_row, _row(3, "closure")])
    completed = _run(spine, spec)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert _slots(completed)["environment_failures"] == 1
    assert _slots(completed)["baseline"] == 1
    assert _slots(completed)["closure"] == 1

    bad = _write_spine(tmp_path, [
        _row(1, "baseline"),
        _row(2, "environment-failure", stage="plan", environment_evidence=""),
        _row(3, "closure"),
    ], name="bad-env.md")
    completed2 = _run(bad, spec)
    assert completed2.returncode == 1


def test_missing_counts_unknown(tmp_path):
    spec = tmp_path / "spec"
    _write_all_stage_evidence(spec)
    row = _row(1, "baseline")
    del row["passed"]
    del row["failed"]
    spine = _write_spine(tmp_path, [row, _row(2, "closure")])
    completed = _run(spine, spec)
    assert completed.returncode == 1
    assert _slots(completed)["unknown"] >= 1


def test_closure_requires_name_level_diff(tmp_path):
    spec = tmp_path / "spec"
    _write_all_stage_evidence(spec)
    count_only = _row(2, "closure", baseline_compare="passed: 10 vs 10; failed: 0 vs 1")
    spine = _write_spine(tmp_path, [_row(1, "baseline"), count_only])
    completed = _run(spine, spec)
    assert completed.returncode == 1

    missing = _row(2, "closure", baseline_compare="na")
    spine2 = _write_spine(tmp_path, [_row(1, "baseline"), missing], name="missing.md")
    completed2 = _run(spine2, spec)
    assert completed2.returncode == 1


def test_unaccounted_log_full_run_rejected(tmp_path):
    spec = tmp_path / "spec"
    _write_all_stage_evidence(spec)
    logs = tmp_path / "logs"
    logs.mkdir()
    (logs / "analyze.log").write_text(
        "$ bash scripts/bash/run-tests.sh -q\n# targeted run done\n", encoding="utf-8")
    spine = _write_spine(tmp_path, [_row(1, "baseline"), _row(2, "closure")])
    completed = _run(spine, spec, logs_dir=logs)
    assert completed.returncode == 1
    assert "unaccounted" in (completed.stdout + completed.stderr)


def test_accounted_log_full_run_passes(tmp_path):
    spec = tmp_path / "spec"
    _write_all_stage_evidence(spec)
    logs = tmp_path / "logs"
    logs.mkdir()
    (logs / "baseline.log").write_text(
        "# test runner: python -m pytest\n$ %s\n" % FULL_COMMAND, encoding="utf-8")
    spine = _write_spine(tmp_path, [_row(1, "baseline"), _row(2, "closure")])
    completed = _run(spine, spec, logs_dir=logs)
    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_missing_logs_reports_unknown(tmp_path):
    spec = tmp_path / "spec"
    _write_all_stage_evidence(spec)
    empty = tmp_path / "logs"
    empty.mkdir()
    spine = _write_spine(tmp_path, [_row(1, "baseline"), _row(2, "closure")])
    completed = _run(spine, spec, logs_dir=empty)
    assert completed.returncode == 1
    assert _slots(completed)["unknown"] >= 1


def test_ledger_reads_state_spine_fence(tmp_path):
    spec = tmp_path / "spec"
    _write_all_stage_evidence(spec)
    _evidence(spec, "implement", [
        {"seq": 1, "slot": "baseline", "stage": "implement", "purpose": "copy",
         "trigger": "scheduled", "at": 1, "command": FULL_COMMAND,
         "selection_basis": "full-suite", "rc": 0, "passed": 1, "failed": 0,
         "failed_names_path": "implement.txt", "baseline_compare": "na",
         "evidence_ptr": "implement.jsonl"},
    ])
    spine = _write_spine(tmp_path, [_row(1, "baseline")])
    completed = _run(spine, spec, stage_check="implement")
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert _slots(completed)["baseline"] == 1

    no_fence = tmp_path / "no-fence.md"
    no_fence.write_text("# Line State Spine\n\nno fence here\n", encoding="utf-8")
    completed2 = _run(no_fence, spec)
    assert completed2.returncode == 2


def test_not_applicable_skipped_stage_not_unknown(tmp_path):
    spec = tmp_path / "spec"
    _write_all_stage_evidence(spec, checklist="skipped")
    spine = _write_spine(tmp_path, [_row(1, "baseline"), _row(2, "closure")],
                         admission=ADMISSION)
    completed = _run(spine, spec)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert _slots(completed)["unknown"] == 0
    stages, complete = _stages(completed)
    assert stages == 5 and complete == 5


def test_missing_or_incomplete_admission_record_fails_closed(tmp_path):
    spec = tmp_path / "spec"
    _write_all_stage_evidence(spec, checklist="skipped")
    no_admission = _write_spine(tmp_path, [_row(1, "baseline"), _row(2, "closure")],
                                name="no-admission.md")
    completed = _run(no_admission, spec)
    assert completed.returncode == 1
    stages, complete = _stages(completed)
    assert stages == 6 and complete == 5

    incomplete = [line for line in ADMISSION if not line.startswith("decided_at")]
    partial = _write_spine(tmp_path, [_row(1, "baseline"), _row(2, "closure")],
                           admission=incomplete, name="partial.md")
    completed2 = _run(partial, spec)
    assert completed2.returncode == 1
    stages2, complete2 = _stages(completed2)
    assert stages2 == 6 and complete2 == 5


def test_empty_selection_escalated_status(tmp_path):
    spec = tmp_path / "spec"
    _write_all_stage_evidence(
        spec, overrides={"analyze": {"status": "empty-selection-escalated"}})
    spine = _write_spine(tmp_path, [_row(1, "baseline"), _row(2, "closure")])
    completed = _run(spine, spec)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert _slots(completed)["unknown"] == 0
    assert _stages(completed) == (6, 6)


def test_multiline_ledger_isolation(tmp_path):
    spec_a = tmp_path / "spec-a"
    spec_b = tmp_path / "spec-b"
    _write_all_stage_evidence(spec_a)
    _write_all_stage_evidence(spec_b)
    spine_a = _write_spine(tmp_path, [_row(1, "baseline"), _row(2, "closure")],
                           name="line-a.md")
    spine_b = _write_spine(tmp_path, [_row(1, "baseline")], name="line-b.md")
    completed_a = _run(spine_a, spec_a)
    completed_b = _run(spine_b, spec_b, stage_check="implement")
    assert completed_a.returncode == 0
    assert completed_b.returncode == 0
    assert _slots(completed_a)["closure"] == 1
    assert _slots(completed_b)["closure"] == 0


def test_implement_open_allows_zero_closure(tmp_path):
    spec = tmp_path / "spec"
    _write_all_stage_evidence(spec)
    spine = _write_spine(tmp_path, [_row(1, "baseline")])
    completed = _run(spine, spec, stage_check="implement")
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert _slots(completed)["baseline"] == 1
    assert _slots(completed)["closure"] == 0


def test_closure_requires_two_slots(tmp_path):
    spec = tmp_path / "spec"
    _write_all_stage_evidence(spec)
    spine = _write_spine(tmp_path, [_row(1, "baseline")])
    completed = _run(spine, spec, stage_check="closure")
    assert completed.returncode == 1


def test_docs_only_reduced_field_set(tmp_path):
    spec = tmp_path / "spec"
    _write_all_stage_evidence(
        spec, overrides={"plan": {"status": "not-run-docs-only"}})
    spine = _write_spine(tmp_path, [_row(1, "baseline"), _row(2, "closure")])
    completed = _run(spine, spec)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert _stages(completed) == (6, 6)
    assert _slots(completed)["unknown"] == 0

    broken = _stage_status("plan", "not-run-docs-only")
    del broken["changed_paths"]
    spec2 = tmp_path / "spec2"
    _write_all_stage_evidence(
        spec2, overrides={"plan": {"status": "not-run-docs-only"}})
    _evidence(spec2, "plan", [broken])
    spine2 = _write_spine(tmp_path, [_row(1, "baseline"), _row(2, "closure")],
                          name="docs-broken.md")
    completed2 = _run(spine2, spec2)
    assert completed2.returncode == 1
    stages, complete = _stages(completed2)
    assert stages == 6 and complete == 5


def test_stage_status_row_uniqueness(tmp_path):
    spec = tmp_path / "spec"
    _write_all_stage_evidence(spec)
    _evidence(spec, "analyze", [
        _stage_status("analyze"),
        _stage_status("analyze"),
    ])
    spine = _write_spine(tmp_path, [_row(1, "baseline"), _row(2, "closure")])
    completed = _run(spine, spec)
    assert completed.returncode == 1
    stages, complete = _stages(completed)
    assert stages == 6 and complete == 5

    spec2 = tmp_path / "spec2"
    _write_all_stage_evidence(spec2)
    run_only = _stage_status("review")
    run_only["row_type"] = "run"
    _evidence(spec2, "review", [run_only])
    spine2 = _write_spine(tmp_path, [_row(1, "baseline"), _row(2, "closure")],
                          name="run-only.md")
    completed2 = _run(spine2, spec2)
    assert completed2.returncode == 1
    stages2, complete2 = _stages(completed2)
    assert stages2 == 6 and complete2 == 5


def test_stages_complete_summary(tmp_path):
    spec = tmp_path / "spec"
    _write_all_stage_evidence(
        spec, checklist="skipped",
        overrides={"plan": {"status": "not-run-docs-only"}})
    spine = _write_spine(tmp_path, [_row(1, "baseline"), _row(2, "closure")],
                         admission=ADMISSION)
    completed = _run(spine, spec)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert _stages(completed) == (5, 5)
    assert _slots(completed)["unknown"] == 0


def test_missing_stage_evidence_fails(tmp_path):
    spec = tmp_path / "spec"
    _write_all_stage_evidence(spec)
    (spec / "test-evidence" / "analyze.jsonl").unlink()
    spine = _write_spine(tmp_path, [_row(1, "baseline"), _row(2, "closure")])
    completed = _run(spine, spec)
    assert completed.returncode == 1
    stages, complete = _stages(completed)
    assert stages == 6 and complete == 5
    assert "analyze" in completed.stdout
    assert "missing" in completed.stdout


def test_empty_stage_evidence_fails(tmp_path):
    spec = tmp_path / "spec"
    _write_all_stage_evidence(spec)
    (spec / "test-evidence" / "review.jsonl").write_text("", encoding="utf-8")
    spine = _write_spine(tmp_path, [_row(1, "baseline"), _row(2, "closure")])
    completed = _run(spine, spec)
    assert completed.returncode == 1
    stages, complete = _stages(completed)
    assert stages == 6 and complete == 5
    assert "review" in completed.stdout
    assert "expected exactly one stage-status row, found 0" in completed.stdout


def test_missing_evidence_directory_fails(tmp_path):
    spine = _write_spine(tmp_path, [_row(1, "baseline"), _row(2, "closure")])
    completed = _run(spine, tmp_path / "absent-spec")
    assert completed.returncode == 1
    assert _stages(completed) == (6, 0)
    assert completed.stdout.count("stage evidence file missing") == 6
