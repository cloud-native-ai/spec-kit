"""Unit tests for the wp-gate.py foundational core.

Covers spine fence reading (plan, amendments, ledger), the required-field
schema checks, schema-before-later-check ordering, the canonical plan hash,
and exit-2 input handling. Graph, preflight, and retry behaviour is added by
later task rows in the same file.
"""
from __future__ import annotations

import copy
import importlib.util
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


def load_gate():
    assert SCRIPT.is_file(), "missing gate script: %s" % SCRIPT
    spec = importlib.util.spec_from_file_location("wp_gate_under_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args], capture_output=True, text=True
    )


def _write_spine(tmp_path: Path, plan=None, **kwargs) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    return wp_fixtures.make_spine(tmp_path / "state.md", plan=plan, **kwargs)


def test_read_spine_reads_plan_amendment_and_ledger(tmp_path):
    gate = load_gate()
    plan = wp_fixtures.make_two_package_plan()
    amendment = {
        "schema_version": 1,
        "stage": "plan",
        "stage_attempt": 1,
        "seq": 1,
        "supersedes_plan_hash": plan["plan_hash"],
        "reason": "fixture amendment",
        "packages": [wp_fixtures.make_package("plan-wp01", objective="changed")],
        "plan_hash": "sha256:" + "1" * 64,
    }
    spine = _write_spine(
        tmp_path,
        plan=plan,
        amendments=[amendment],
        ledger=wp_fixtures.ledger_sequence(),
    )

    document = gate.read_spine(spine)
    assert len(document["plan_fences"]) == 1
    assert document["plan_fences"][0]["stage"] == "plan"
    assert document["plan_fences"][0]["stage_attempt"] == 1
    assert document["plan_fences"][0]["plan"]["plan_hash"] == plan["plan_hash"]
    assert len(document["amendments"]) == 1
    assert document["amendments"][0]["seq"] == 1
    assert [event["event"] for event in document["ledger"]] == [
        "plan",
        "dispatch",
        "settle",
        "verdict",
    ]


def test_effective_plan_applies_amendments_in_seq_order(tmp_path):
    gate = load_gate()
    plan = wp_fixtures.make_two_package_plan()
    replacement = wp_fixtures.make_package("plan-wp01", objective="amended outcome")
    expected = json.loads(json.dumps(plan))
    expected["packages"] = [replacement, expected["packages"][1]]
    expected_hash = wp_fixtures.canonical_hash_of(expected)
    amendment = {
        "schema_version": 1,
        "stage": "plan",
        "stage_attempt": 1,
        "seq": 1,
        "supersedes_plan_hash": plan["plan_hash"],
        "reason": "fixture amendment",
        "packages": [replacement],
        "plan_hash": expected_hash,
    }

    effective = gate.effective_plan(plan, [amendment])
    assert effective["plan_hash"] == expected_hash
    assert effective["packages"][0]["objective"] == "amended outcome"
    assert effective["packages"][1]["wp_id"] == "plan-wp02"


def test_canonical_hash_excludes_hash_slot_keys_and_timestamps():
    gate = load_gate()
    plan = wp_fixtures.make_two_package_plan()
    baseline = gate.canonical_plan_hash(plan)

    mutated = json.loads(json.dumps(plan))
    mutated["plan_hash"] = "sha256:" + "9" * 64
    mutated["slot_cap_requested"] = 4
    mutated["slot_cap_ceiling"] = 4
    mutated["at"] = 1790000000
    mutated["checked_at"] = "2026-10-25T00:00:00Z"
    mutated["packages"][0]["verified_at"] = "2026-10-25T00:00:01Z"
    assert gate.canonical_plan_hash(mutated) == baseline

    mutated["packages"][0]["objective"] = "a different bounded outcome"
    assert gate.canonical_plan_hash(mutated) != baseline


def test_canonical_hash_is_sha256_hex():
    gate = load_gate()
    digest = gate.canonical_plan_hash(wp_fixtures.make_two_package_plan())
    assert re.match(r"^sha256:[0-9a-f]{64}$", digest), digest


def test_schema_missing_for_absent_required_field(tmp_path):
    package = wp_fixtures.make_package("plan-wp01")
    del package["objective"]
    plan = wp_fixtures.make_plan(packages=[package])
    plan["plan_hash"] = wp_fixtures.canonical_hash_of(plan)
    spine = _write_spine(tmp_path, plan=plan)

    completed = _run(
        "--spine", str(spine), "--stage", "plan", "--stage-attempt", "1",
        "--check", "plan",
    )
    assert completed.returncode == 1, completed.stdout + completed.stderr
    findings = json.loads(completed.stdout)["findings"]
    assert any(
        finding["code"] == "schema-missing"
        and finding["wp_id"] == "plan-wp01"
        for finding in findings
    ), findings


def test_schema_failures_skip_the_hash_check(tmp_path):
    package = wp_fixtures.make_package("plan-wp01")
    del package["objective"]
    plan = wp_fixtures.make_plan(packages=[package])
    plan["plan_hash"] = "sha256:" + "0" * 64
    spine = _write_spine(tmp_path, plan=plan)

    completed = _run(
        "--spine", str(spine), "--stage", "plan", "--stage-attempt", "1",
        "--check", "plan",
    )
    assert completed.returncode == 1
    codes = [finding["code"] for finding in json.loads(completed.stdout)["findings"]]
    assert "schema-missing" in codes
    assert "plan-hash-mismatch" not in codes


def test_plan_hash_mismatch_is_a_reject(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    plan["plan_hash"] = "sha256:" + "0" * 64
    spine = _write_spine(tmp_path, plan=plan)

    completed = _run(
        "--spine", str(spine), "--stage", "plan", "--stage-attempt", "1",
        "--check", "plan",
    )
    assert completed.returncode == 1, completed.stdout + completed.stderr
    record = json.loads(completed.stdout)
    assert record["verdict"] == "reject"
    assert [finding["code"] for finding in record["findings"]] == [
        "plan-hash-mismatch"
    ]
    assert record["plan_hash"] == wp_fixtures.canonical_hash_of(plan)


def test_exit_two_when_neither_spine_nor_plan_json(tmp_path):
    completed = _run("--stage", "plan", "--check", "plan")
    assert completed.returncode == 2
    assert "--spine" in completed.stderr or "--plan-json" in completed.stderr


def test_exit_two_on_malformed_plan_json(tmp_path):
    plan_json = tmp_path / "plan.json"
    plan_json.write_text("{not json", encoding="utf-8")
    completed = _run(
        "--stage", "plan", "--stage-attempt", "1", "--check", "plan",
        "--plan-json", str(plan_json),
    )
    assert completed.returncode == 2
    assert completed.stderr.strip()


def test_exit_two_on_malformed_ledger_line(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    spine = tmp_path / "state.md"
    spine.write_text(
        "\n".join(
            [
                wp_fixtures.plan_fence(plan),
                "<!-- wp-ledger:begin -->",
                "this is not a JSON object",
                "<!-- wp-ledger:end -->",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    completed = _run(
        "--spine", str(spine), "--stage", "plan", "--stage-attempt", "1",
        "--check", "plan",
    )
    assert completed.returncode == 2
    assert "ledger" in completed.stderr.lower()


def test_exit_two_when_no_plan_fence_matches(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    spine = _write_spine(tmp_path, plan=plan)
    completed = _run(
        "--spine", str(spine), "--stage", "review", "--stage-attempt", "1",
        "--check", "plan",
    )
    assert completed.returncode == 2
    assert "review" in completed.stderr


def test_ledger_stage_attempt_contributes_to_the_default(tmp_path):
    gate = load_gate()
    plan = wp_fixtures.make_two_package_plan()
    spine = _write_spine(
        tmp_path,
        plan=plan,
        ledger=[wp_fixtures.plan_event(stage_attempt=2)],
    )
    document = gate.read_spine(spine)
    assert gate.highest_stage_attempt(document) == 2


# --- T010: --check plan (WG-06…WG-13) ---


def _rehash(plan: dict) -> dict:
    plan["plan_hash"] = wp_fixtures.canonical_hash_of(plan)
    return plan


def _run_plan(tmp_path: Path, plan: dict):
    spine = _write_spine(tmp_path, plan=plan)
    return _run(
        "--spine", str(spine), "--stage", plan["stage"],
        "--stage-attempt", str(plan["stage_attempt"]), "--check", "plan",
    )


def _record(completed) -> dict:
    assert completed.stdout.strip(), completed.stderr
    return json.loads(completed.stdout)


def _codes(completed) -> list:
    return [finding["code"] for finding in _record(completed)["findings"]]


def test_dup_wp_id_rejects(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    plan["packages"][1]["wp_id"] = "plan-wp01"
    _rehash(plan)

    completed = _run_plan(tmp_path, plan)
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert "dup-wp-id" in _codes(completed)


def test_dangling_dep_rejects(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    plan["packages"][1]["depends_on"] = ["plan-wp99"]
    _rehash(plan)

    completed = _run_plan(tmp_path, plan)
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert "dangling-dep" in _codes(completed)


def test_dependency_cycle_rejects(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    plan["packages"][0]["depends_on"] = ["plan-wp02"]
    plan["packages"][1]["depends_on"] = ["plan-wp01"]
    plan["pattern"] = "serial"
    _rehash(plan)

    completed = _run_plan(tmp_path, plan)
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert "cycle" in _codes(completed)


def test_orphan_required_output_rejects(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    plan["required_outputs"].append("findings/unowned.md")
    _rehash(plan)

    completed = _run_plan(tmp_path, plan)
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert "orphan-output" in _codes(completed)


def test_non_required_output_orphans(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    plan["packages"][0]["outputs"].append("findings/extra.md")
    _rehash(plan)

    completed = _run_plan(tmp_path, plan)
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert "orphan-output" in _codes(completed)


def test_unconsumed_intermediate_output_rejects(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    plan["packages"][0]["intermediate_outputs"] = ["findings/scratch.md"]
    plan["packages"][0]["outputs"].append("findings/scratch.md")
    plan["required_outputs"] = [
        "findings/plan-wp01.md",
        "findings/plan-wp02.md",
    ]
    _rehash(plan)

    completed = _run_plan(tmp_path, plan)
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert "orphan-output" in _codes(completed)


def test_consumed_intermediate_output_is_admitted(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    plan["packages"][0]["intermediate_outputs"] = ["findings/scratch.md"]
    plan["packages"][0]["outputs"].append("findings/scratch.md")
    plan["required_outputs"] = [
        "findings/plan-wp01.md",
        "findings/plan-wp02.md",
    ]
    plan["packages"][1]["depends_on"] = ["plan-wp01"]
    plan["packages"][1]["inputs"].append("findings/scratch.md")
    plan["pattern"] = "serial"
    _rehash(plan)

    completed = _run_plan(tmp_path, plan)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert _record(completed)["verdict"] in ("admit", "single-package")


def test_duplicate_required_output_rejects(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    plan["packages"][1]["outputs"] = ["findings/plan-wp01.md"]
    plan["required_outputs"] = ["findings/plan-wp01.md"]
    _rehash(plan)

    completed = _run_plan(tmp_path, plan)
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert "duplicate-output" in _codes(completed)


def test_package_claiming_integrator_output_rejects(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    plan["required_outputs"].append("clarification.md")
    plan["integrator_outputs"] = ["clarification.md"]
    plan["packages"][0]["outputs"].append("clarification.md")
    _rehash(plan)

    completed = _run_plan(tmp_path, plan)
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert "duplicate-output" in _codes(completed)


def test_integrator_output_not_in_required_outputs_is_schema_missing(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    plan["integrator_outputs"] = ["ghost.md"]
    _rehash(plan)

    completed = _run_plan(tmp_path, plan)
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert "schema-missing" in _codes(completed)


@pytest.mark.parametrize(
    "unit,count,blocked",
    [
        ("tasks", 8, False),
        ("tasks", 9, True),
        ("clauses", 40, False),
        ("clauses", 41, True),
        ("tasks", 0, True),
        ("artifacts", 999, False),
        ("acceptance", 1, False),
    ],
)
def test_bounded_by_caps(tmp_path, unit, count, blocked):
    plan = wp_fixtures.make_two_package_plan()
    plan["packages"][0]["bounded_by"] = {"unit": unit, "count": count}
    _rehash(plan)

    completed = _run_plan(tmp_path, plan)
    if blocked:
        assert completed.returncode == 1, completed.stdout + completed.stderr
        assert "unbounded" in _codes(completed)
    else:
        assert completed.returncode == 0, completed.stdout + completed.stderr
        assert "unbounded" not in _codes(completed)


def test_kind_mismatch_cases(tmp_path):
    cases = []

    read_only_with_territory = wp_fixtures.make_two_package_plan()
    read_only_with_territory["packages"][0]["owned_paths"] = ["src/generated/"]
    cases.append(read_only_with_territory)

    write_without_territory = wp_fixtures.make_two_package_plan()
    write_without_territory["packages"][0].update(
        kind="write", parallel_safe=False, owned_paths=[]
    )
    cases.append(write_without_territory)

    parallel_write = wp_fixtures.make_two_package_plan()
    parallel_write["packages"][0].update(
        kind="write", parallel_safe=True, owned_paths=["src/generated/"]
    )
    cases.append(parallel_write)

    for index, plan in enumerate(cases):
        _rehash(plan)
        completed = _run_plan(tmp_path / ("case-%d" % index), plan)
        assert completed.returncode == 1, completed.stdout + completed.stderr
        assert "kind-mismatch" in _codes(completed), _record(completed)["findings"]


@pytest.mark.parametrize(
    "mutate",
    [
        "parallel-with-write",
        "parallel-with-one-package",
        "parallel-with-unsafe-package",
        "serial-with-independent-read-only",
        "iteration-without-repair-loop",
        "continuous-pattern",
        "parallel-with-dependency-edge",
    ],
)
def test_pattern_compatibility(tmp_path, mutate):
    plan = wp_fixtures.make_two_package_plan()

    if mutate == "parallel-with-write":
        plan["packages"][1].update(
            kind="write", parallel_safe=False, owned_paths=["src/generated/"]
        )
    elif mutate == "parallel-with-one-package":
        plan = wp_fixtures.make_single_package_plan()
        plan["pattern"] = "parallel"
    elif mutate == "parallel-with-unsafe-package":
        plan["packages"][1]["parallel_safe"] = False
    elif mutate == "serial-with-independent-read-only":
        plan["pattern"] = "serial"
    elif mutate == "iteration-without-repair-loop":
        plan["pattern"] = "iteration"
    elif mutate == "continuous-pattern":
        plan["pattern"] = "continuous"
    elif mutate == "parallel-with-dependency-edge":
        plan["packages"][1]["depends_on"] = ["plan-wp01"]
    else:  # pragma: no cover - parametrization is closed above
        raise AssertionError(mutate)

    _rehash(plan)
    completed = _run_plan(tmp_path, plan)
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert "pattern-mismatch" in _codes(completed), _record(completed)["findings"]


def test_graph_checks_skip_when_schema_is_incomplete(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    plan["packages"][1]["wp_id"] = "plan-wp01"
    del plan["packages"][0]["objective"]
    _rehash(plan)

    completed = _run_plan(tmp_path, plan)
    assert completed.returncode == 1
    codes = _codes(completed)
    assert "schema-missing" in codes
    assert "dup-wp-id" not in codes


def test_not_beneficial_returns_single_package_with_advisory(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    plan["packages"][1].update(
        kind="write",
        parallel_safe=False,
        owned_paths=["src/generated/"],
        depends_on=["plan-wp01"],
    )
    plan["pattern"] = "serial"
    plan["slot_cap"] = 2
    _rehash(plan)

    completed = _run_plan(tmp_path, plan)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    record = _record(completed)
    assert record["verdict"] == "single-package"
    assert [finding["code"] for finding in record["findings"]] == ["not-beneficial"]
    assert "not-beneficial" in record["findings"][0]["detail"]


def test_benefit_branch_b_admits_a_forked_graph(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    plan["packages"][1].update(
        kind="write",
        parallel_safe=False,
        owned_paths=["src/generated/"],
    )
    third = wp_fixtures.make_write_package(
        "plan-wp03",
        depends_on=["plan-wp01", "plan-wp02"],
        owned_paths=["src/generated/"],
        outputs=["src/generated/integrated.md"],
    )
    plan["packages"].append(third)
    plan["required_outputs"].append("src/generated/integrated.md")
    plan["pattern"] = "serial"
    plan["slot_cap"] = 2
    _rehash(plan)

    completed = _run_plan(tmp_path, plan)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    record = _record(completed)
    assert record["verdict"] == "admit"
    assert "not-beneficial" not in [item["code"] for item in record["findings"]]


def test_benefit_branch_c_admits_a_bounded_iteration(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    plan["packages"][1].update(
        kind="write",
        parallel_safe=False,
        owned_paths=["src/generated/"],
        depends_on=["plan-wp01"],
    )
    plan["pattern"] = "iteration"
    plan["repair_loop"] = {
        "max_iterations": 3,
        "stop_condition": "zero open blockers",
        "findings_source": "findings/findings.json",
    }
    _rehash(plan)

    completed = _run_plan(tmp_path, plan)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    record = _record(completed)
    assert record["verdict"] == "admit"


# --- T016: --check preflight (WG-14…WG-16) ---


def _prepare_plan(plan: dict) -> dict:
    plan["plan_hash"] = wp_fixtures.canonical_hash_of(plan)
    return plan


def _isolate(plan: dict) -> dict:
    for package in plan["packages"]:
        package["resources"] = {
            "ports": "none",
            "tmp_dir": "tmp/%s" % package["wp_id"],
            "cache_dir": "none",
            "shared_readonly": [],
        }
    return plan


def _write_pair(overlap: bool = True) -> dict:
    first_owned = ["src/generated/"] if overlap else ["src/first/"]
    first_output = (
        "src/generated/a.md" if overlap else "src/first/a.md"
    )
    second_owned = ["src/generated/"] if overlap else ["src/second/"]
    second_output = (
        "src/generated/b.md" if overlap else "src/second/b.md"
    )
    first = wp_fixtures.make_write_package(
        "plan-wp01", owned_paths=first_owned, outputs=[first_output]
    )
    second = wp_fixtures.make_write_package(
        "plan-wp02", owned_paths=second_owned, outputs=[second_output]
    )
    return wp_fixtures.make_plan(
        packages=[first, second], pattern="serial", slot_cap=1
    )


def _write_read_plan(ordered: bool = False) -> dict:
    writer = wp_fixtures.make_write_package(
        "plan-wp01",
        owned_paths=["src/generated/"],
        outputs=["src/generated/out.md"],
    )
    reader = wp_fixtures.make_package(
        "plan-wp02",
        inputs=["src/generated/out.md"],
        outputs=["findings/read.md"],
        read_only_paths=["src/generated/out.md"],
        depends_on=["plan-wp01"] if ordered else [],
        resources={
            "ports": "none",
            "tmp_dir": "tmp/plan-wp02",
            "cache_dir": "none",
            "shared_readonly": [],
        },
    )
    return wp_fixtures.make_plan(
        packages=[writer, reader], pattern="serial", slot_cap=2
    )


def _run_preflight(
    tmp_path: Path,
    plan: dict,
    *,
    owned=(),
    read_only=(),
    forbidden=(),
    extra=(),
    manifest_path=None,
):
    _prepare_plan(plan)
    spine = _write_spine(tmp_path, plan=plan)
    if manifest_path is None:
        manifest_path = wp_fixtures.make_manifest(
            tmp_path / "manifest.json",
            owned=owned,
            read_only=read_only,
            forbidden=forbidden,
        )
    args = [
        "--spine", str(spine),
        "--stage", plan["stage"],
        "--stage-attempt", str(plan["stage_attempt"]),
        "--check", "preflight",
        "--manifest", str(manifest_path),
        "--repo", str(tmp_path),
    ]
    args.extend(extra)
    return _run(*args)


def test_preflight_admits_a_covered_plan(tmp_path):
    plan = _write_pair(overlap=False)
    completed = _run_preflight(
        tmp_path, plan, owned=["src/first/", "src/second/"]
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    record = json.loads(completed.stdout)
    assert record["check"] == "preflight"
    assert record["verdict"] == "admit"
    assert record["findings"] == []


def test_preflight_manifest_uncovered_path_rejects(tmp_path):
    plan = _write_pair(overlap=False)
    completed = _run_preflight(tmp_path, plan, owned=["src/first/"])
    assert completed.returncode == 1, completed.stdout + completed.stderr
    codes = [finding["code"] for finding in _record(completed)["findings"]]
    assert "manifest-uncovered" in codes


def test_preflight_manifest_forbidden_read_path_rejects(tmp_path):
    plan = _isolate(
        wp_fixtures.make_two_package_plan()
    )
    plan["packages"][1]["read_only_paths"].append("secrets/token.txt")
    completed = _run_preflight(
        tmp_path, plan, forbidden=["secrets/"]
    )
    assert completed.returncode == 1, completed.stdout + completed.stderr
    codes = [finding["code"] for finding in _record(completed)["findings"]]
    assert "manifest-forbidden" in codes


def test_preflight_normalizes_paths_before_coverage(tmp_path):
    package = wp_fixtures.make_write_package(
        "plan-wp01",
        owned_paths=["./src/generated/notes.md"],
        outputs=["./src/generated/notes.md"],
    )
    plan = wp_fixtures.make_plan(
        packages=[package], pattern="serial", slot_cap=1
    )
    completed = _run_preflight(
        tmp_path, plan, owned=["src//generated/"]
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    codes = [finding["code"] for finding in _record(completed)["findings"]]
    assert "manifest-uncovered" not in codes


def test_preflight_write_write_overlap_rejects(tmp_path):
    plan = _write_pair(overlap=True)
    completed = _run_preflight(
        tmp_path, plan, owned=["src/generated/"]
    )
    assert completed.returncode == 1, completed.stdout + completed.stderr
    codes = [finding["code"] for finding in _record(completed)["findings"]]
    assert "write-write-unordered" in codes
    assert "path-overlap" in codes


def test_preflight_read_write_overlap_rejects(tmp_path):
    plan = _write_read_plan(ordered=False)
    completed = _run_preflight(
        tmp_path, plan, owned=["src/generated/"]
    )
    assert completed.returncode == 1, completed.stdout + completed.stderr
    codes = [finding["code"] for finding in _record(completed)["findings"]]
    assert "read-write-unordered" in codes


def test_preflight_ordered_read_write_is_allowed(tmp_path):
    plan = _write_read_plan(ordered=True)
    completed = _run_preflight(
        tmp_path, plan, owned=["src/generated/"]
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    codes = [finding["code"] for finding in _record(completed)["findings"]]
    assert "read-write-unordered" not in codes
    assert "path-overlap" not in codes


def test_preflight_slot_cap_above_ceiling_rejects(tmp_path):
    plan = _isolate(wp_fixtures.make_two_package_plan(slot_cap=4))
    completed = _run_preflight(
        tmp_path, plan, extra=["--slot-cap-ceiling", "3"]
    )
    assert completed.returncode == 1, completed.stdout + completed.stderr
    codes = [finding["code"] for finding in _record(completed)["findings"]]
    assert "slot-cap-exceeded" in codes


def test_preflight_slot_cap_below_one_rejects(tmp_path):
    package = wp_fixtures.make_write_package("plan-wp01")
    plan = wp_fixtures.make_plan(
        packages=[package], pattern="serial", slot_cap=0
    )
    completed = _run_preflight(tmp_path, plan, owned=["src/generated/"])
    assert completed.returncode == 1, completed.stdout + completed.stderr
    codes = [finding["code"] for finding in _record(completed)["findings"]]
    assert "slot-cap-exceeded" in codes


def test_preflight_isolation_missing_rejects(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    for package in plan["packages"]:
        package["resources"] = {
            "ports": "none",
            "tmp_dir": "none",
            "cache_dir": "none",
            "shared_readonly": [],
        }
    completed = _run_preflight(tmp_path, plan)
    assert completed.returncode == 1, completed.stdout + completed.stderr
    codes = [finding["code"] for finding in _record(completed)["findings"]]
    assert "isolation-missing" in codes


def test_preflight_shared_readonly_satisfies_isolation(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    for package in plan["packages"]:
        package["resources"] = {
            "ports": "none",
            "tmp_dir": "none",
            "cache_dir": "none",
            "shared_readonly": ["plan.md"],
        }
    completed = _run_preflight(tmp_path, plan)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    codes = [finding["code"] for finding in _record(completed)["findings"]]
    assert "isolation-missing" not in codes


def test_preflight_includes_plan_checks(tmp_path):
    first = wp_fixtures.make_write_package(
        "plan-wp01",
        owned_paths=["src/generated/"],
        outputs=["src/generated/a.md"],
    )
    second = wp_fixtures.make_write_package(
        "plan-wp02",
        owned_paths=["src/generated/"],
        outputs=["src/generated/b.md"],
        depends_on=["plan-wp03"],
    )
    third = wp_fixtures.make_package(
        "plan-wp03",
        outputs=["findings/c.md"],
        depends_on=["plan-wp02"],
    )
    plan = wp_fixtures.make_plan(
        packages=[first, second, third], pattern="serial", slot_cap=1
    )
    plan["required_outputs"].append("ghost.md")
    completed = _run_preflight(
        tmp_path, plan, owned=["src/generated/"]
    )
    assert completed.returncode == 1, completed.stdout + completed.stderr
    codes = [finding["code"] for finding in _record(completed)["findings"]]
    assert "cycle" in codes
    assert "orphan-output" in codes
    assert "write-write-unordered" in codes
    assert "path-overlap" in codes


def test_preflight_exit_two_for_unreadable_manifest(tmp_path):
    plan = _write_pair(overlap=False)
    completed = _run_preflight(
        tmp_path,
        plan,
        owned=["src/first/", "src/second/"],
        manifest_path=tmp_path / "missing-manifest.json",
    )
    assert completed.returncode == 2, completed.stdout + completed.stderr
    assert completed.stderr.strip()


def test_preflight_exit_two_for_malformed_manifest(tmp_path):
    plan = _write_pair(overlap=False)
    bad = tmp_path / "bad-manifest.json"
    bad.write_text("{not json", encoding="utf-8")
    completed = _run_preflight(
        tmp_path,
        plan,
        owned=["src/first/", "src/second/"],
        manifest_path=bad,
    )
    assert completed.returncode == 2, completed.stdout + completed.stderr
    assert completed.stderr.strip()


# --- T016: --check retry (WG-17) ---


def _dispatch_for(wp_id="plan-wp01", wp_attempt=1, **overrides):
    event = wp_fixtures.dispatch_event(
        wp_id=wp_id,
        wp_attempt=wp_attempt,
        attempt_id="%s-a1-w%d" % (wp_id, wp_attempt),
    )
    event.update(overrides)
    return event


def _budget_evidence(tmp_path: Path, payload=None, name="budget.json") -> str:
    path = tmp_path / "wp" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            payload
            if payload is not None
            else {"turns": 120, "budget_exhausted": True}
        ),
        encoding="utf-8",
    )
    return "wp/%s" % name


def _delta(changed, reason="fixture delta", scope=None, budget=None, topology=None):
    delta = {"changed": list(changed), "reason": reason}
    if scope is not None:
        delta["scope"] = scope
    if budget is not None:
        delta["budget"] = budget
    if topology is not None:
        delta["topology"] = topology
    return delta


def _retry_amendment(plan, wp_id, wp_attempt, delta, packages=None, seq=1):
    return {
        "schema_version": 1,
        "stage": plan["stage"],
        "stage_attempt": plan["stage_attempt"],
        "seq": seq,
        "supersedes_plan_hash": plan["plan_hash"],
        "reason": "fixture retry amendment",
        "wp_id": wp_id,
        "wp_attempt": wp_attempt,
        "retry_delta": delta,
        "packages": packages or [],
        "plan_hash": "sha256:" + (str(seq % 10) * 64),
    }


def _run_retry(
    tmp_path: Path,
    plan: dict,
    wp_id: str,
    wp_attempt: int,
    *,
    ledger=(),
    amendments=(),
):
    spine = _write_spine(
        tmp_path,
        plan=_prepare_plan(plan),
        amendments=amendments,
        ledger=ledger,
    )
    return _run(
        "--spine", str(spine),
        "--stage", plan["stage"],
        "--stage-attempt", str(plan["stage_attempt"]),
        "--check", "retry",
        "--wp-id", wp_id,
        "--wp-attempt", str(wp_attempt),
    )


def _retry_codes(completed) -> list:
    return [finding["code"] for finding in _record(completed)["findings"]]


def _budget_delta(tmp_path, from_turns=120, to_turns=160, evidence=True):
    budget = {"from_max_turns": from_turns, "to_max_turns": to_turns}
    if evidence is True:
        budget["evidence_ref"] = _budget_evidence(tmp_path)
    elif evidence:
        budget["evidence_ref"] = evidence
    return _delta(["budget"], budget=budget)


def test_retry_attempt_one_is_admitted_without_a_delta(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    completed = _run_retry(
        tmp_path, plan, "plan-wp01", 1, ledger=[wp_fixtures.plan_event()]
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    record = _record(completed)
    assert record["check"] == "retry"
    assert record["verdict"] == "admit"
    assert record["findings"] == []
    assert record["dispatch_count"] == 0


def test_retry_second_attempt_without_a_delta_is_unchanged(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    completed = _run_retry(
        tmp_path,
        plan,
        "plan-wp01",
        2,
        ledger=[wp_fixtures.plan_event(), wp_fixtures.dispatch_event()],
    )
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert _retry_codes(completed) == ["retry-unchanged"]


def test_retry_identical_same_budget_rerun_is_unchanged(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    delta = _budget_delta(tmp_path, from_turns=120, to_turns=120)
    amendment = _retry_amendment(plan, "plan-wp01", 2, delta)
    completed = _run_retry(
        tmp_path,
        plan,
        "plan-wp01",
        2,
        ledger=[wp_fixtures.plan_event(), wp_fixtures.dispatch_event()],
        amendments=[amendment],
    )
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert _retry_codes(completed) == ["retry-unchanged"]


def test_retry_valid_budget_increase_is_admitted(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    delta = _budget_delta(tmp_path, from_turns=120, to_turns=160)
    amendment = _retry_amendment(plan, "plan-wp01", 2, delta)
    completed = _run_retry(
        tmp_path,
        plan,
        "plan-wp01",
        2,
        ledger=[wp_fixtures.plan_event(), wp_fixtures.dispatch_event()],
        amendments=[amendment],
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert _record(completed)["verdict"] == "admit"


def test_retry_budget_decrease_is_invalid(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    delta = _budget_delta(tmp_path, from_turns=160, to_turns=120)
    amendment = _retry_amendment(plan, "plan-wp01", 2, delta)
    completed = _run_retry(
        tmp_path,
        plan,
        "plan-wp01",
        2,
        ledger=[wp_fixtures.plan_event(), wp_fixtures.dispatch_event()],
        amendments=[amendment],
    )
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert "retry-delta-invalid" in _retry_codes(completed)


def test_retry_budget_without_evidence_is_invalid(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    delta = _budget_delta(
        tmp_path, from_turns=120, to_turns=160, evidence=False
    )
    amendment = _retry_amendment(plan, "plan-wp01", 2, delta)
    completed = _run_retry(
        tmp_path,
        plan,
        "plan-wp01",
        2,
        ledger=[wp_fixtures.plan_event(), wp_fixtures.dispatch_event()],
        amendments=[amendment],
    )
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert "retry-delta-invalid" in _retry_codes(completed)


def test_retry_budget_evidence_must_be_dispatch_level(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    evidence = _budget_evidence(
        tmp_path, payload={"note": "no dispatch measurement"}
    )
    delta = _budget_delta(
        tmp_path, from_turns=120, to_turns=160, evidence=evidence
    )
    amendment = _retry_amendment(plan, "plan-wp01", 2, delta)
    completed = _run_retry(
        tmp_path,
        plan,
        "plan-wp01",
        2,
        ledger=[wp_fixtures.plan_event(), wp_fixtures.dispatch_event()],
        amendments=[amendment],
    )
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert "retry-delta-invalid" in _retry_codes(completed)


def test_retry_scope_reduction_is_admitted(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    delta = _delta(
        ["scope"],
        scope={
            "from_unit": "tasks",
            "from_count": 8,
            "to_unit": "tasks",
            "to_count": 4,
        },
    )
    amendment = _retry_amendment(plan, "plan-wp01", 2, delta)
    completed = _run_retry(
        tmp_path,
        plan,
        "plan-wp01",
        2,
        ledger=[wp_fixtures.plan_event(), wp_fixtures.dispatch_event()],
        amendments=[amendment],
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert _record(completed)["verdict"] == "admit"


@pytest.mark.parametrize("to_count", [4, 6])
def test_retry_non_smaller_scope_is_invalid(tmp_path, to_count):
    plan = wp_fixtures.make_two_package_plan()
    delta = _delta(
        ["scope"],
        scope={
            "from_unit": "tasks",
            "from_count": 4,
            "to_unit": "tasks",
            "to_count": to_count,
        },
    )
    amendment = _retry_amendment(plan, "plan-wp01", 2, delta)
    completed = _run_retry(
        tmp_path,
        plan,
        "plan-wp01",
        2,
        ledger=[wp_fixtures.plan_event(), wp_fixtures.dispatch_event()],
        amendments=[amendment],
    )
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert "retry-delta-invalid" in _retry_codes(completed)


def test_retry_topology_change_is_admitted(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    delta = _delta(
        ["topology"],
        topology={"from": "parallel-native", "to": "serial-native"},
    )
    amendment = _retry_amendment(plan, "plan-wp01", 2, delta)
    completed = _run_retry(
        tmp_path,
        plan,
        "plan-wp01",
        2,
        ledger=[wp_fixtures.plan_event(), wp_fixtures.dispatch_event()],
        amendments=[amendment],
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert _record(completed)["verdict"] == "admit"


@pytest.mark.parametrize(
    "topology",
    [
        {"from": "parallel-native", "to": "parallel-native"},
        {"from": "parallel-native", "to": "magic-mode"},
    ],
)
def test_retry_fake_or_unknown_topology_is_invalid(tmp_path, topology):
    plan = wp_fixtures.make_two_package_plan()
    delta = _delta(["topology"], topology=topology)
    amendment = _retry_amendment(plan, "plan-wp01", 2, delta)
    completed = _run_retry(
        tmp_path,
        plan,
        "plan-wp01",
        2,
        ledger=[wp_fixtures.plan_event(), wp_fixtures.dispatch_event()],
        amendments=[amendment],
    )
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert "retry-delta-invalid" in _retry_codes(completed)


@pytest.mark.parametrize(
    "delta",
    [
        {"changed": ["nonsense"], "reason": "invalid key"},
        {"changed": [], "reason": "empty change set"},
        {"changed": ["budget"], "reason": ""},
    ],
)
def test_retry_malformed_delta_is_invalid(tmp_path, delta):
    plan = wp_fixtures.make_two_package_plan()
    amendment = _retry_amendment(plan, "plan-wp01", 2, delta)
    completed = _run_retry(
        tmp_path,
        plan,
        "plan-wp01",
        2,
        ledger=[wp_fixtures.plan_event(), wp_fixtures.dispatch_event()],
        amendments=[amendment],
    )
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert "retry-delta-invalid" in _retry_codes(completed)


def test_retry_third_attempt_is_exhausted(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    completed = _run_retry(
        tmp_path,
        plan,
        "plan-wp01",
        3,
        ledger=[wp_fixtures.plan_event(), wp_fixtures.dispatch_event()],
    )
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert _retry_codes(completed) == ["retry-exhausted"]


def test_retry_package_already_at_two_attempts_is_exhausted(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    completed = _run_retry(
        tmp_path,
        plan,
        "plan-wp01",
        2,
        ledger=[
            wp_fixtures.plan_event(),
            _dispatch_for(wp_attempt=1),
            _dispatch_for(wp_attempt=2),
        ],
    )
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert _retry_codes(completed) == ["retry-exhausted"]


def _split_packages(plan):
    parent = copy.deepcopy(plan["packages"][0])
    parent["superseded_by"] = ["plan-wp01-a", "plan-wp01-b"]
    child_a = wp_fixtures.make_package(
        "plan-wp01-a", outputs=["findings/split-a.md"]
    )
    child_b = wp_fixtures.make_package(
        "plan-wp01-b", outputs=["findings/split-b.md"]
    )
    return [parent, child_a, child_b]


def _split_delta(children=("plan-wp01-a", "plan-wp01-b")):
    return _delta(
        ["scope"],
        scope={
            "from_unit": "tasks",
            "from_count": 4,
            "to_unit": "tasks",
            "to_count": 2,
            "split_into": list(children),
        },
    )


def _split_amendment(plan, packages=None, seq=1):
    return _retry_amendment(
        plan,
        "plan-wp01",
        2,
        _split_delta(),
        packages=_split_packages(plan) if packages is None else packages,
        seq=seq,
    )


def test_retry_split_parent_admits_the_retry_attempt(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    completed = _run_retry(
        tmp_path,
        plan,
        "plan-wp01",
        2,
        ledger=[wp_fixtures.plan_event(), wp_fixtures.dispatch_event()],
        amendments=[_split_amendment(plan)],
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert _record(completed)["verdict"] == "admit"


def test_retry_split_child_inherits_the_parent_attempt(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    completed = _run_retry(
        tmp_path,
        plan,
        "plan-wp01-a",
        2,
        ledger=[wp_fixtures.plan_event(), wp_fixtures.dispatch_event()],
        amendments=[_split_amendment(plan)],
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert _record(completed)["verdict"] == "admit"


def test_retry_split_child_attempt_one_is_invalid(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    completed = _run_retry(
        tmp_path,
        plan,
        "plan-wp01-a",
        1,
        ledger=[wp_fixtures.plan_event(), wp_fixtures.dispatch_event()],
        amendments=[_split_amendment(plan)],
    )
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert "retry-delta-invalid" in _retry_codes(completed)


def test_retry_split_child_further_attempt_is_exhausted(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    completed = _run_retry(
        tmp_path,
        plan,
        "plan-wp01-a",
        2,
        ledger=[
            wp_fixtures.plan_event(),
            wp_fixtures.dispatch_event(),
            _dispatch_for("plan-wp01-a", 2),
        ],
        amendments=[_split_amendment(plan)],
    )
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert _retry_codes(completed) == ["retry-exhausted"]


def test_retry_split_of_a_child_is_exhausted(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    split = _split_amendment(plan)
    child_split_packages = _split_packages(plan)
    child_a = copy.deepcopy(child_split_packages[1])
    child_a["superseded_by"] = ["plan-wp01-a-a", "plan-wp01-a-b"]
    extra_children = [
        child_a,
        wp_fixtures.make_package(
            "plan-wp01-a-a", outputs=["findings/split-a-a.md"]
        ),
        wp_fixtures.make_package(
            "plan-wp01-a-b", outputs=["findings/split-a-b.md"]
        ),
    ]
    child_amendment = _retry_amendment(
        plan,
        "plan-wp01-a",
        2,
        _split_delta(("plan-wp01-a-a", "plan-wp01-a-b")),
        packages=extra_children,
        seq=2,
    )
    completed = _run_retry(
        tmp_path,
        plan,
        "plan-wp01-a",
        2,
        ledger=[wp_fixtures.plan_event(), wp_fixtures.dispatch_event()],
        amendments=[split, child_amendment],
    )
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert _retry_codes(completed) == ["retry-exhausted"]


def test_retry_split_requires_distinct_child_outputs(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    packages = _split_packages(plan)
    packages[2]["outputs"] = packages[1]["outputs"]
    completed = _run_retry(
        tmp_path,
        plan,
        "plan-wp01",
        2,
        ledger=[wp_fixtures.plan_event(), wp_fixtures.dispatch_event()],
        amendments=[_split_amendment(plan, packages=packages)],
    )
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert "retry-delta-invalid" in _retry_codes(completed)


def test_retry_split_without_child_records_is_invalid(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    completed = _run_retry(
        tmp_path,
        plan,
        "plan-wp01",
        2,
        ledger=[wp_fixtures.plan_event(), wp_fixtures.dispatch_event()],
        amendments=[_split_amendment(plan, packages=[])],
    )
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert "retry-delta-invalid" in _retry_codes(completed)


def test_retry_attempt_must_be_positive(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    completed = _run_retry(tmp_path, plan, "plan-wp01", 0)
    assert completed.returncode == 2, completed.stdout + completed.stderr
    assert completed.stderr.strip()


def test_retry_unknown_package_is_rejected(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    completed = _run_retry(tmp_path, plan, "plan-wp99", 1)
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert "schema-missing" in _retry_codes(completed)


def test_retry_never_writes_the_spine(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    spine = _write_spine(
        tmp_path,
        plan=_prepare_plan(plan),
        ledger=[wp_fixtures.plan_event(), wp_fixtures.dispatch_event()],
    )
    before = spine.read_bytes()
    completed = _run(
        "--spine", str(spine), "--stage", "plan", "--stage-attempt", "1",
        "--check", "retry", "--wp-id", "plan-wp01", "--wp-attempt", "2",
    )
    assert completed.returncode == 1, completed.stdout + completed.stderr
    assert spine.read_bytes() == before

