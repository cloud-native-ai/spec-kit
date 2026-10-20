"""Unit tests for pre-analyze-check.py (deterministic cross-artifact gate)."""

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "pre-analyze-check.py"


def _spec(tmp_path, plan_extra="", task_extra="", requirement_extra="",
          contract_text="- **AB-01**: local clause\n"):
    spec = tmp_path / "001-demo"
    (spec / "contracts").mkdir(parents=True)
    (spec / "requirements.md").write_text(
        "# Requirements\n\n- **FR-001**: first\n- **FR-002**: second\n"
        "- **SC-001**: criterion\n" + requirement_extra, encoding="utf-8")
    (spec / "plan.md").write_text(
        "# Plan\n\nCovers FR-001 and FR-002 against SC-001.\n" + plan_extra,
        encoding="utf-8")
    (spec / "tasks.md").write_text(
        "# Tasks\n\n- [ ] T001 first\n- [ ] T002 second [blockedBy: T001]\n"
        + task_extra, encoding="utf-8")
    if contract_text is not None:
        (spec / "contracts" / "core.md").write_text(
            "# Contracts\n\n" + contract_text, encoding="utf-8")
    return spec


def _run(spec, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--spec-dir", str(spec), "--stage", "tasks", *args],
        capture_output=True, text=True)


def _record(proc):
    return json.loads(proc.stdout)


def test_clean_spec_passes(tmp_path):
    proc = _run(_spec(tmp_path))
    assert proc.returncode == 0, proc.stdout + proc.stderr
    record = _record(proc)
    assert record["decision"] == "pass"
    assert record["summary"]["fr"] == 2
    assert record["summary"]["sc"] == 1
    assert record["summary"]["tasks"] == 2
    assert record["summary"]["clauses"] == 1


def test_dangling_fr_reference_fails(tmp_path):
    spec = _spec(tmp_path, plan_extra="\nAlso FR-009.\n")
    proc = _run(spec)
    assert proc.returncode == 1
    findings = _record(proc)["findings"]
    assert any(f["check"] == "dangling-id" and "FR-009" in f["message"]
               for f in findings)


def test_duplicate_fr_definition_fails(tmp_path):
    spec = _spec(tmp_path,
                 requirement_extra="- **FR-001**: duplicated\n")
    proc = _run(spec)
    assert proc.returncode == 1
    assert any(f["check"] == "duplicate-id" and "FR-001" in f["message"]
               for f in _record(proc)["findings"])


def test_duplicate_clause_across_contracts_fails(tmp_path):
    spec = _spec(tmp_path)
    (spec / "contracts" / "second.md").write_text(
        "# Second\n\n- **AB-01**: duplicated clause\n", encoding="utf-8")
    proc = _run(spec)
    assert proc.returncode == 1
    assert any(f["check"] == "duplicate-id" and "AB-01" in f["message"]
               for f in _record(proc)["findings"])


def test_count_claim_mismatch_fails(tmp_path):
    spec = _spec(tmp_path, plan_extra="\nCount check: 3 FR in total.\n")
    proc = _run(spec)
    assert proc.returncode == 1
    finding = [f for f in _record(proc)["findings"] if f["check"] == "count-claim"]
    assert finding and "claims 3 FR" in finding[0]["message"]


def test_ranges_and_examples_are_not_claims(tmp_path):
    spec = _spec(
        tmp_path,
        plan_extra="\nMedium band: 8–30 FR and 10–40 tasks.\n",
        requirement_extra="1. **Given** a feature with 12 FR, **When** planned.\n")
    proc = _run(spec)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert not [f for f in _record(proc)["findings"] if f["check"] == "count-claim"]


def test_historical_sections_are_ignored(tmp_path):
    spec = _spec(
        tmp_path,
        plan_extra=("\n## Plan Repair Record\n\n"
                    "Round 1 changed 5 FR → 3 FR and 9 tasks → 7 tasks.\n"))
    proc = _run(spec)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_blocked_by_missing_target_fails(tmp_path):
    spec = _spec(tmp_path, task_extra="- [ ] T003 third [blockedBy: T009]\n")
    proc = _run(spec)
    assert proc.returncode == 1
    assert any(f["check"] == "blocked-by" and "T009" in f["message"]
               for f in _record(proc)["findings"])


def test_non_concrete_blocked_by_is_advisory(tmp_path):
    spec = _spec(tmp_path, task_extra="- [ ] T003 third [blockedBy: Txxx]\n")
    proc = _run(spec)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    record = _record(proc)
    assert record["summary"]["advisories"] == 1
    assert record["findings"][0]["severity"] == "advisory"


def test_local_clause_dangling_fails(tmp_path):
    spec = _spec(tmp_path, plan_extra="\nSee AB-02 for the missing clause.\n")
    proc = _run(spec)
    assert proc.returncode == 1
    assert any(f["check"] == "dangling-id" and "AB-02" in f["message"]
               for f in _record(proc)["findings"])


def test_external_clause_namespace_is_advisory(tmp_path):
    spec = _spec(tmp_path, plan_extra="\nSee CLP-01 owned elsewhere.\n")
    proc = _run(spec)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    findings = _record(proc)["findings"]
    assert any(f["check"] == "external-clause" and "CLP-01" in f["message"]
               for f in findings)


def test_missing_path_is_advisory_and_strict_blocks(tmp_path):
    spec = _spec(tmp_path, plan_extra="\nSee `skills/demo/absent.md`.\n")
    lenient = _run(spec, "--repo", str(tmp_path))
    assert lenient.returncode == 0, lenient.stdout + lenient.stderr
    assert any(f["check"] == "missing-path"
               for f in _record(lenient)["findings"])
    strict = _run(spec, "--repo", str(tmp_path), "--strict")
    assert strict.returncode == 1


def test_waiver_clears_count_claim(tmp_path):
    spec = _spec(tmp_path, plan_extra="\nCount check: 3 FR in total.\n")
    line = (spec / "plan.md").read_text(encoding="utf-8").splitlines().index(
        "Count check: 3 FR in total.") + 1
    proc = _run(spec, "--waive", "count-claim:plan.md:%d" % line)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert _record(proc)["summary"]["waived"] == 1


def test_stage_requires_its_artifact(tmp_path):
    spec = _spec(tmp_path)
    (spec / "plan.md").unlink()
    proc = _run(spec)
    assert proc.returncode == 2
    assert "plan.md" in proc.stderr


def test_json_out_written(tmp_path):
    spec = _spec(tmp_path, plan_extra="\nAlso FR-009.\n")
    out = tmp_path / "gate.json"
    proc = _run(spec, "--json-out", str(out))
    assert proc.returncode == 1
    assert json.loads(out.read_text(encoding="utf-8"))["decision"] == "fail"
