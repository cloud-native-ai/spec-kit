"""Contract tests for wp-gate.py — WG-01…WG-05 (path, CLI, envelope, exits).

The behavioural checks live in tests/unit/test_wp_gate.py. This file pins the
script location, the stdlib-only constraint, the CLI grammar, the input
precedence, the JSON envelope, the exit-code taxonomy, deterministic finding
order, and the never-writes-the-spine guarantee.

Plan-check clause coverage (T010 unit cases, green at T011):

- WG-06 schema: `test_schema_missing_for_absent_required_field`,
  `test_schema_failures_skip_the_hash_check`
- WG-07 graph: `test_dup_wp_id_rejects`, `test_dangling_dep_rejects`,
  `test_dependency_cycle_rejects`
- WG-08 output coverage: `test_orphan_required_output_rejects`,
  `test_non_required_output_orphans`,
  `test_unconsumed_intermediate_output_rejects`,
  `test_duplicate_required_output_rejects`,
  `test_package_claiming_integrator_output_rejects`,
  `test_integrator_output_not_in_required_outputs_is_schema_missing`
- WG-09 boundedness: `test_bounded_by_caps`
- WG-10 kind: `test_kind_mismatch_cases`
- WG-11 pattern: `test_pattern_compatibility`
- WG-12 hash: `test_plan_hash_mismatch_is_a_reject`
- WG-13 benefit: `test_not_beneficial_returns_single_package_with_advisory`,
  `test_benefit_branch_b_admits_a_forked_graph`,
  `test_benefit_branch_c_admits_a_bounded_iteration`

Foundational clause coverage (T005 cases, green at T007):

- WG-01 path and responsibility: `test_script_path_and_stdlib_only`,
  `test_gate_never_writes_spine_or_plan`
- WG-02 CLI grammar: `test_cli_grammar_and_defaults`,
  `test_stage_attempt_defaults_to_highest_in_spine`,
  `test_retry_check_requires_wp_arguments`
- WG-03 input precedence: `test_plan_json_takes_precedence_over_spine`,
  `test_preflight_requires_manifest_when_owned_paths_exist`
- WG-04 JSON output: `test_json_envelope_shape`,
  `test_evidence_ptr_is_null_without_json_out`,
  `test_finding_order_is_stable_and_sorted`
- WG-05 exit codes: `test_exit_codes_cover_zero_one_two`

Preflight, retry, and fallback clause coverage (T016 cases, green at T017;
WG-18's fallback layer is green at T035):

- WG-14 manifest coverage: `test_preflight_manifest_uncovered_path_rejects`,
  `test_preflight_manifest_forbidden_read_path_rejects`,
  `test_preflight_normalizes_paths_before_coverage`
- WG-15 concurrency territories: `test_preflight_write_write_overlap_rejects`,
  `test_preflight_read_write_overlap_rejects`,
  `test_preflight_ordered_read_write_is_allowed`
- WG-16 slot cap and isolation: `test_preflight_slot_cap_above_ceiling_rejects`,
  `test_preflight_slot_cap_below_one_rejects`,
  `test_preflight_isolation_missing_rejects`,
  `test_preflight_shared_readonly_satisfies_isolation`
- WG-17 retry checks: `test_retry_attempt_one_is_admitted_without_a_delta`,
  `test_retry_second_attempt_without_a_delta_is_unchanged`,
  `test_retry_valid_budget_increase_is_admitted`,
  `test_retry_third_attempt_is_exhausted`
- WG-18 determinism, repair, and fallback: CLI-envelope layer
  `test_json_envelope_shape`, `test_finding_order_is_stable_and_sorted`,
  `test_exit_codes_cover_zero_one_two`; fallback/preflight layer
  `test_fn_06_fallback_causes_are_the_closed_named_set`,
  `test_fn_07_fallback_never_runs_a_partial_package_set`,
  `test_fn_08_every_stage_records_one_decision_with_the_mapped_verdict`
  (coordination contract) and `test_fallback_never_dispatches_a_partial_package_set`
  (integration dry run)
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from fixtures import wp_fixtures

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = (
    REPO_ROOT
    / "skills"
    / "external"
    / "sdd-loop-driver"
    / "scripts"
    / "wp-gate.py"
)

ENVELOPE_KEYS = {
    "schema_version",
    "check",
    "stage",
    "verdict",
    "findings",
    "plan_hash",
    "checked_at",
    "evidence_ptr",
}

ISO_8601 = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def _run(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args], capture_output=True, text=True
    )


def _spine(tmp_path: Path, plan=None, **kwargs) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    return wp_fixtures.make_spine(tmp_path / "state.md", plan=plan, **kwargs)


def _plan_json(tmp_path: Path, plan: dict) -> Path:
    return wp_fixtures.write_plan_json(tmp_path / "plan.json", plan)


@pytest.mark.contract
def test_script_path_and_stdlib_only():
    assert SCRIPT.is_file(), "missing gate script: %s" % SCRIPT
    source = SCRIPT.read_text(encoding="utf-8")
    stdlib = {
        "argparse",
        "copy",
        "hashlib",
        "json",
        "os",
        "pathlib",
        "re",
        "sys",
        "time",
    }
    for module in re.findall(
        r"^(?:import|from)\s+([A-Za-z_][\w.]*)", source, re.MULTILINE
    ):
        assert module.split(".", 1)[0] in stdlib, (
            "wp-gate.py imports non-stdlib module %s" % module
        )
    assert "specify_cli" not in source
    assert ".specify/scripts" not in source


@pytest.mark.contract
def test_cli_grammar_and_defaults():
    completed = _run("--help")
    assert completed.returncode == 0, completed.stderr
    for flag in (
        "--spine",
        "--stage",
        "--check",
        "--plan-json",
        "--manifest",
        "--repo",
        "--slot-cap-ceiling",
        "--stage-attempt",
        "--wp-id",
        "--wp-attempt",
        "--json-out",
    ):
        assert flag in completed.stdout, "wp-gate.py --help lacks %s" % flag


@pytest.mark.contract
def test_plan_json_takes_precedence_over_spine(tmp_path):
    broken = wp_fixtures.make_two_package_plan()
    del broken["packages"][0]["objective"]
    broken["plan_hash"] = wp_fixtures.canonical_hash_of(broken)
    spine = _spine(tmp_path, plan=broken)
    good = wp_fixtures.make_two_package_plan()
    plan_json = _plan_json(tmp_path, good)

    completed = _run(
        "--spine", str(spine), "--stage", "plan", "--stage-attempt", "1",
        "--check", "plan", "--plan-json", str(plan_json),
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert json.loads(completed.stdout)["verdict"] == "admit"


@pytest.mark.contract
def test_stage_attempt_defaults_to_highest_in_spine(tmp_path):
    first = wp_fixtures.make_plan(packages=[wp_fixtures.make_package("plan-wp01")])
    first["stage_attempt"] = 1
    first["plan_hash"] = wp_fixtures.canonical_hash_of(first)

    second_package = wp_fixtures.make_package("plan-wp02")
    del second_package["objective"]
    second = wp_fixtures.make_plan(packages=[second_package])
    second["stage_attempt"] = 2
    second["plan_hash"] = wp_fixtures.canonical_hash_of(second)

    spine = tmp_path / "state.md"
    spine.write_text(
        "\n\n".join(
            [wp_fixtures.plan_fence(first), wp_fixtures.plan_fence(second)]
        )
        + "\n",
        encoding="utf-8",
    )

    completed = _run(
        "--spine", str(spine), "--stage", "plan", "--check", "plan"
    )
    assert completed.returncode == 1, completed.stdout + completed.stderr
    record = json.loads(completed.stdout)
    assert record["verdict"] == "reject"
    assert any(
        finding["code"] == "schema-missing"
        and finding["wp_id"] == "plan-wp02"
        for finding in record["findings"]
    ), record["findings"]


@pytest.mark.contract
def test_preflight_requires_manifest_when_owned_paths_exist(tmp_path):
    plan = wp_fixtures.make_plan(packages=[wp_fixtures.make_write_package()])
    spine = _spine(tmp_path, plan=plan)

    completed = _run(
        "--spine", str(spine), "--stage", "plan", "--stage-attempt", "1",
        "--check", "preflight",
    )
    assert completed.returncode == 2, completed.stdout + completed.stderr
    assert "manifest" in completed.stderr.lower()


@pytest.mark.contract
def test_json_envelope_shape(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    spine = _spine(tmp_path, plan=plan)
    out = tmp_path / "wp" / "line-plan-a1-gate-plan.json"
    out.parent.mkdir(parents=True)

    completed = _run(
        "--spine", str(spine), "--stage", "plan", "--stage-attempt", "1",
        "--check", "plan", "--json-out", str(out),
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    record = json.loads(completed.stdout)
    assert ENVELOPE_KEYS <= set(record), sorted(record)
    assert record["schema_version"] == 1
    assert record["check"] == "plan"
    assert record["stage"] == "plan"
    assert record["verdict"] == "admit"
    assert record["findings"] == []
    assert re.match(r"^sha256:[0-9a-f]{64}$", record["plan_hash"])
    assert ISO_8601.match(record["checked_at"]), record["checked_at"]
    assert record["evidence_ptr"] == str(out)
    assert json.loads(out.read_text(encoding="utf-8")) == record


@pytest.mark.contract
def test_evidence_ptr_is_null_without_json_out(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    spine = _spine(tmp_path, plan=plan)
    completed = _run(
        "--spine", str(spine), "--stage", "plan", "--stage-attempt", "1",
        "--check", "plan",
    )
    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout)["evidence_ptr"] is None


@pytest.mark.contract
def test_exit_codes_cover_zero_one_two(tmp_path):
    good = wp_fixtures.make_two_package_plan()
    good_spine = _spine(tmp_path / "good", plan=good)
    admitted = _run(
        "--spine", str(good_spine), "--stage", "plan", "--stage-attempt", "1",
        "--check", "plan",
    )
    assert admitted.returncode == 0, admitted.stderr
    assert json.loads(admitted.stdout)["verdict"] == "admit"

    bad_hash = wp_fixtures.make_two_package_plan()
    bad_hash["plan_hash"] = "sha256:" + "0" * 64
    bad_spine = _spine(tmp_path / "bad", plan=bad_hash)
    rejected = _run(
        "--spine", str(bad_spine), "--stage", "plan", "--stage-attempt", "1",
        "--check", "plan",
    )
    assert rejected.returncode == 1, rejected.stdout + rejected.stderr
    record = json.loads(rejected.stdout)
    assert record["verdict"] == "reject"
    assert any(
        finding["code"] == "plan-hash-mismatch" for finding in record["findings"]
    )

    errored = _run("--stage", "plan", "--check", "plan")
    assert errored.returncode == 2, errored.stdout + errored.stderr
    assert errored.stderr.strip()


@pytest.mark.contract
def test_finding_order_is_stable_and_sorted(tmp_path):
    packages = [
        wp_fixtures.make_package("plan-wp02"),
        wp_fixtures.make_package("plan-wp01"),
    ]
    for package in packages:
        del package["objective"]
    plan = wp_fixtures.make_plan(packages=packages)
    plan["plan_hash"] = wp_fixtures.canonical_hash_of(plan)
    spine = _spine(tmp_path, plan=plan)

    args = (
        "--spine", str(spine), "--stage", "plan", "--stage-attempt", "1",
        "--check", "plan",
    )
    first = _run(*args)
    second = _run(*args)
    assert first.returncode == second.returncode == 1
    findings = json.loads(first.stdout)["findings"]
    assert json.loads(second.stdout)["findings"] == findings
    assert len(findings) >= 2
    assert findings == sorted(
        findings, key=lambda item: (item["code"], item["wp_id"] or "")
    )
    assert [item["wp_id"] for item in findings] == ["plan-wp01", "plan-wp02"]


@pytest.mark.contract
def test_gate_never_writes_spine_or_plan(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    spine = _spine(tmp_path, plan=plan)
    plan_json = _plan_json(tmp_path, plan)
    spine_before = spine.read_bytes()
    plan_before = plan_json.read_bytes()

    completed = _run(
        "--spine", str(spine), "--stage", "plan", "--stage-attempt", "1",
        "--check", "plan", "--plan-json", str(plan_json),
    )
    assert completed.returncode == 0, completed.stderr
    assert spine.read_bytes() == spine_before
    assert plan_json.read_bytes() == plan_before


@pytest.mark.contract
def test_retry_check_requires_wp_arguments(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    spine = _spine(tmp_path, plan=plan)
    completed = _run(
        "--spine", str(spine), "--stage", "plan", "--stage-attempt", "1",
        "--check", "retry", "--wp-attempt", "2",
    )
    assert completed.returncode == 2, completed.stdout + completed.stderr
    assert "--wp-id" in completed.stderr
