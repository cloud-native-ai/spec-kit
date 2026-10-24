"""Contract tests for the WP model and ledger — WP-01…WP-18, OR-01…OR-16.

Layer under test
----------------
WP and OR clauses are design-owned by ``contracts/``. The executable model
surface is (a) ``wp-gate.py`` for the clauses it enforces (schema, kind,
fences, graph, canonical hash, layers) and (b) ``references/decomposition-model.md``
as the runtime-owner projection of the runtime rules (IDs, evidence paths,
067 projection, single-package, ledger/retry representation).

Metric *computation* (OR-04…OR-13) is behaviourally exercised by
``tests/unit/test_wp_report.py`` (T027/T028). This file pins the schema, field
sets, formulas, and runtime-owner citations so an owner edit cannot silently
drop them.
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

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
DRIVER_ROOT = REPO_ROOT / "skills" / "external" / "sdd-loop-driver"
GATE = DRIVER_ROOT / "scripts" / "wp-gate.py"
MODEL_DOC = DRIVER_ROOT / "references" / "decomposition-model.md"
CONTRACTS = REPO_ROOT / ".specify" / "specs" / "070-subagent-task-teams" / "contracts"
DATA_MODEL = (
    REPO_ROOT / ".specify" / "specs" / "070-subagent-task-teams" / "data-model.md"
)

ISO_8601 = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

EVENT_TYPES = (
    "plan",
    "dispatch",
    "settle",
    "verdict",
    "retry",
    "integrate",
    "stage-close",
    "wp_failed",
)

REQUIRED_PACKAGE_FIELDS = (
    "wp_id",
    "stage",
    "objective",
    "kind",
    "source_refs",
    "inputs",
    "outputs",
    "owned_paths",
    "read_only_paths",
    "depends_on",
    "parallel_safe",
    "max_turns",
    "bounded_by",
    "acceptance",
    "sentinel",
    "evidence",
    "seat",
    "resources",
)

EVENT_REQUIRED_FIELDS = {
    "plan": {
        "stage",
        "stage_attempt",
        "plan_hash",
        "decision",
        "pattern",
        "slot_cap",
        "verdict",
        "gate_evidence",
        "at",
    },
    "dispatch": {
        "wp_id",
        "stage_attempt",
        "wp_attempt",
        "dispatch_order",
        "started_at",
        "effective_concurrency",
        "attempt_id",
    },
    "settle": {"wp_id", "ended_at", "runner_status", "result_ptr", "outputs"},
    "verdict": {"wp_id", "verdict", "verifier_execution", "evidence_ptr", "at"},
    "retry": {"wp_id", "wp_attempt", "retry_delta", "gate_evidence", "at"},
    "integrate": {"stage_attempt", "order", "at", "conflict", "commit"},
    "stage-close": {
        "stage_attempt",
        "stage_u4_at",
        "wall_clock_seconds",
        "critical_path_seconds",
        "parallelism_efficiency",
        "retries_package",
        "retries_stage",
        "stage_attempts",
        "canonical_stages",
        "stage_executions_per_canonical",
        "manual_interventions",
        "sessions",
        "token_cost",
        "report_ptr",
    },
    "wp_failed": {"wp_id", "attempts", "verdict_evidence", "at"},
}

IMPLEMENT_DISPATCH_FIELDS = {
    "part_id",
    "task_ids",
    "turns",
    "test_delta",
    "commit",
    "outcome",
    "duration_seconds",
    "token_cost",
}


def load_gate():
    assert GATE.is_file(), "missing gate script: %s" % GATE
    spec = importlib.util.spec_from_file_location("wp_gate_model_under_test", GATE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run(*args):
    return subprocess.run(
        [sys.executable, str(GATE), *args], capture_output=True, text=True
    )


def _spine(tmp_path: Path, plan=None, **kwargs) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    return wp_fixtures.make_spine(tmp_path / "state.md", plan=plan, **kwargs)


def _rehash(plan: dict) -> dict:
    plan["plan_hash"] = wp_fixtures.canonical_hash_of(plan)
    return plan


def _run_plan(tmp_path: Path, plan: dict):
    spine = _spine(tmp_path, plan=plan)
    return _run(
        "--spine",
        str(spine),
        "--stage",
        plan.get("stage", wp_fixtures.STAGE),
        "--stage-attempt",
        str(plan.get("stage_attempt", 1)),
        "--check",
        "plan",
    )


def _record(completed) -> dict:
    assert completed.stdout.strip(), completed.stderr
    return json.loads(completed.stdout)


def _codes(completed) -> list:
    return [finding["code"] for finding in _record(completed)["findings"]]


def _model_text() -> str:
    assert MODEL_DOC.is_file(), "missing runtime owner: %s" % MODEL_DOC
    return MODEL_DOC.read_text(encoding="utf-8")


def _contract(name: str) -> str:
    return (CONTRACTS / name).read_text(encoding="utf-8")


def _apply_amendments(plan: dict, amendments: list) -> dict:
    """Fixture-local amendment application (replacement/add only)."""
    effective = copy.deepcopy(plan)
    for amendment in sorted(amendments, key=lambda body: body["seq"]):
        packages = effective["packages"]
        index_by_id = {
            package["wp_id"]: offset
            for offset, package in enumerate(packages)
        }
        for record in amendment["packages"]:
            copied = copy.deepcopy(record)
            if copied["wp_id"] in index_by_id:
                packages[index_by_id[copied["wp_id"]]] = copied
            else:
                packages.append(copied)
                index_by_id[copied["wp_id"]] = len(packages) - 1
        effective["packages"] = packages
        effective["plan_hash"] = amendment["plan_hash"]
    return effective


def _amendment(plan: dict, replacements: list, seq: int, supersedes: str) -> dict:
    amendment = {
        "schema_version": 1,
        "stage": plan["stage"],
        "stage_attempt": plan["stage_attempt"],
        "seq": seq,
        "supersedes_plan_hash": supersedes,
        "reason": "fixture amendment %d" % seq,
        "packages": [copy.deepcopy(record) for record in replacements],
        "plan_hash": "sha256:" + "0" * 64,
    }
    amendment["plan_hash"] = wp_fixtures.canonical_hash_of(
        _apply_amendments(plan, [amendment])
    )
    return amendment


@pytest.mark.parametrize("field", REQUIRED_PACKAGE_FIELDS)
def test_wp_01_required_package_field_is_schema_missing(tmp_path, field):
    """WP-01: a package missing any required field MUST NOT be dispatched."""
    plan = wp_fixtures.make_two_package_plan()
    del plan["packages"][0][field]
    _rehash(plan)

    completed = _run_plan(tmp_path, plan)
    assert completed.returncode == 1, completed.stdout + completed.stderr
    findings = _record(completed)["findings"]
    assert any(
        finding["code"] == "schema-missing" and field in finding["detail"]
        for finding in findings
    ), findings


def test_wp_01_intermediate_outputs_is_optional(tmp_path):
    """WP-01: the contract field is validated when present; E1 marks it optional."""
    plan = wp_fixtures.make_two_package_plan()
    for package in plan["packages"]:
        package.pop("intermediate_outputs", None)
    _rehash(plan)

    completed = _run_plan(tmp_path, plan)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert _record(completed)["verdict"] == "admit"


def test_wp_02_kind_and_territory_invariants(tmp_path):
    """WP-02: read-only has no owned paths; write owns paths; writes are never parallel-safe."""
    read_only_with_territory = wp_fixtures.make_two_package_plan()
    read_only_with_territory["packages"][0]["owned_paths"] = ["src/generated/"]
    _rehash(read_only_with_territory)

    write_without_territory = wp_fixtures.make_two_package_plan()
    write_without_territory["packages"][0].update(
        kind="write", parallel_safe=False, owned_paths=[]
    )
    _rehash(write_without_territory)

    parallel_write = wp_fixtures.make_two_package_plan()
    parallel_write["packages"][0].update(
        kind="write", parallel_safe=True, owned_paths=["src/generated/"]
    )
    _rehash(parallel_write)

    for index, plan in enumerate(
        (read_only_with_territory, write_without_territory, parallel_write)
    ):
        completed = _run_plan(tmp_path / ("case-%d" % index), plan)
        assert completed.returncode == 1, completed.stdout + completed.stderr
        assert "kind-mismatch" in _codes(completed), _record(completed)["findings"]


def test_wp_03_stable_ids_and_sentinels():
    """WP-03: ids derive from artifacts and the sentinel renders the id, not the dispatch time."""
    assert wp_fixtures.sentinel_for("plan-wp03") == "WP-PLAN-WP03-DONE"
    assert wp_fixtures.sentinel_for("plan-wp03-a") == "WP-PLAN-WP03-A-DONE"

    plan = wp_fixtures.make_two_package_plan()
    assert all(
        re.fullmatch(r"plan-wp\d{2}", package["wp_id"])
        for package in plan["packages"]
    )
    assert all(
        package["sentinel"] == wp_fixtures.sentinel_for(package["wp_id"])
        for package in plan["packages"]
    )

    text = _model_text()
    assert "WP-03" in text
    assert "WP-<WP_ID_UPPER>-DONE" in text
    assert _contract("work-package-model.md").count("WP-03") >= 1


def test_wp_04_deterministic_layers_and_tie_break(tmp_path):
    """WP-04: provisional keys, topological layers, lexicographic order, replay-stable ids."""
    plan = wp_fixtures.make_two_package_plan()
    first = _run_plan(tmp_path / "first", plan)
    second = _run_plan(tmp_path / "second", plan)
    assert first.returncode == second.returncode == 0, first.stdout + first.stderr
    record = _record(first)
    assert record["dispatch_layers"] == [["plan-wp01", "plan-wp02"]]
    assert record["integration_order"] == ["plan-wp01", "plan-wp02"]
    assert record["dispatch_layers"] == _record(second)["dispatch_layers"]
    assert record["integration_order"] == _record(second)["integration_order"]

    dependent = wp_fixtures.make_two_package_plan()
    dependent["packages"][1]["depends_on"] = ["plan-wp01"]
    dependent["pattern"] = "serial"
    _rehash(dependent)
    layered = _run_plan(tmp_path / "layered", dependent)
    assert layered.returncode == 0, layered.stdout + layered.stderr
    assert _record(layered)["dispatch_layers"] == [
        ["plan-wp01"],
        ["plan-wp02"],
    ]
    assert _record(layered)["integration_order"] == ["plan-wp01", "plan-wp02"]

    shuffled = wp_fixtures.make_two_package_plan()
    shuffled["packages"].reverse()
    _rehash(shuffled)
    shuffled_run = _run_plan(tmp_path / "shuffled", shuffled)
    assert shuffled_run.returncode == 0, shuffled_run.stdout + shuffled_run.stderr
    assert _record(shuffled_run)["dispatch_layers"] == [
        ["plan-wp01", "plan-wp02"]
    ]

    text = _model_text()
    assert "WP-04" in text
    assert "lexicographic" in text


def test_wp_05_plan_fence_and_sole_writer(tmp_path):
    """WP-05: the plan is one JSON fence in the spine; the gate never writes it."""
    plan = wp_fixtures.make_two_package_plan()
    spine = _spine(tmp_path, plan=plan)
    plan_json = wp_fixtures.write_plan_json(tmp_path / "plan.json", plan)
    spine_before = spine.read_bytes()
    plan_before = plan_json.read_bytes()

    completed = _run(
        "--spine",
        str(spine),
        "--stage",
        "plan",
        "--stage-attempt",
        "1",
        "--check",
        "plan",
        "--plan-json",
        str(plan_json),
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert spine.read_bytes() == spine_before
    assert plan_json.read_bytes() == plan_before

    text = _model_text()
    assert "WP-05" in text
    assert "wp-plan:begin" in text
    assert "wp-plan:end" in text


def test_wp_06_canonical_hash_exclusions_and_replay():
    """WP-06: the hash excludes the hash itself, slot-cap bookkeeping, and timestamps."""
    gate = load_gate()
    plan = wp_fixtures.make_two_package_plan()
    baseline = gate.canonical_plan_hash(plan)

    mutated = copy.deepcopy(plan)
    mutated["plan_hash"] = "sha256:" + "9" * 64
    mutated["slot_cap_requested"] = 4
    mutated["slot_cap_ceiling"] = 4
    mutated["at"] = 1790000000
    mutated["checked_at"] = "2026-10-25T00:00:00Z"
    mutated["packages"][0]["started_at"] = 1790000100
    mutated["packages"][0]["verified_at"] = "2026-10-25T00:00:01Z"
    assert gate.canonical_plan_hash(mutated) == baseline

    mutated["packages"][0]["objective"] = "a different bounded outcome"
    assert gate.canonical_plan_hash(mutated) != baseline
    assert gate.canonical_plan_hash(copy.deepcopy(plan)) == baseline

    assert "WP-06" in _model_text()


def test_wp_07_amendments_apply_in_seq_order(tmp_path):
    """WP-07: amendments are separate fences applied by seq; the latest effective hash wins."""
    plan = wp_fixtures.make_two_package_plan()
    first_replacement = wp_fixtures.make_package(
        "plan-wp01", objective="first amendment outcome"
    )
    first = _amendment(plan, [first_replacement], seq=1, supersedes=plan["plan_hash"])
    second_replacement = wp_fixtures.make_package(
        "plan-wp01", objective="second amendment outcome"
    )
    second = _amendment(
        plan, [second_replacement], seq=2, supersedes=first["plan_hash"]
    )

    gate = load_gate()
    effective = gate.effective_plan(plan, [second, first])
    assert effective["packages"][0]["objective"] == "second amendment outcome"
    assert effective["plan_hash"] == second["plan_hash"]

    spine = _spine(tmp_path, plan=plan, amendments=[second, first])
    completed = _run(
        "--spine", str(spine), "--stage", "plan", "--stage-attempt", "1",
        "--check", "plan",
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert _record(completed)["verdict"] == "admit"

    broken = copy.deepcopy(first)
    broken["supersedes_plan_hash"] = "sha256:" + "f" * 64
    broken_spine = _spine(tmp_path / "broken", plan=plan, amendments=[broken])
    rejected = _run(
        "--spine", str(broken_spine), "--stage", "plan", "--stage-attempt", "1",
        "--check", "plan",
    )
    assert rejected.returncode == 1, rejected.stdout + rejected.stderr
    assert "plan-hash-mismatch" in _codes(rejected)

    text = _model_text()
    assert "WP-07" in text
    assert "wp-plan-amendment" in text


def test_wp_08_split_retry_children_inherit_the_attempt():
    """WP-08: a split keeps the parent record, marks superseded_by, and the children inherit the attempt."""
    parent = wp_fixtures.make_package("plan-wp03", outputs=["findings/split.md"])
    child_a = wp_fixtures.make_package("plan-wp03-a", outputs=["findings/split-a.md"])
    child_b = wp_fixtures.make_package("plan-wp03-b", outputs=["findings/split-b.md"])
    parent["superseded_by"] = [child_a["wp_id"], child_b["wp_id"]]

    assert parent["superseded_by"] == ["plan-wp03-a", "plan-wp03-b"]
    assert child_a["outputs"] != child_b["outputs"]
    assert wp_fixtures.sentinel_for(child_a["wp_id"]) == "WP-PLAN-WP03-A-DONE"
    assert wp_fixtures.sentinel_for(child_b["wp_id"]) == "WP-PLAN-WP03-B-DONE"

    text = _model_text()
    for token in (
        "WP-08",
        "superseded_by",
        "split depth is one",
        "inherit",
    ):
        assert token in text, token

    contract = _contract("work-package-model.md")
    for token in ("superseded_by", "split depth is one", "inherit"):
        assert token in contract, token


def test_wp_09_ledger_fence_and_closed_event_set(tmp_path):
    """WP-09: one append-only JSONL fence; the eight event types are the closed set."""
    gate = load_gate()
    events = [
        wp_fixtures.plan_event(),
        wp_fixtures.dispatch_event(),
        wp_fixtures.settle_event(),
        wp_fixtures.verdict_event(),
        wp_fixtures.retry_event(),
        wp_fixtures.integrate_event(),
        wp_fixtures.stage_close_event(),
        wp_fixtures.wp_failed_event(),
    ]
    spine = _spine(tmp_path, plan=wp_fixtures.make_two_package_plan(), ledger=events)
    document = gate.read_spine(spine)
    assert [event["event"] for event in document["ledger"]] == list(EVENT_TYPES)

    contract = _contract("work-package-model.md")
    for event_name in EVENT_TYPES:
        assert event_name in contract, event_name

    text = _model_text()
    assert "WP-09" in text
    assert "wp-ledger:begin" in text
    assert "E4" in text


def test_wp_10_ledger_event_field_sets():
    """WP-10: each ledger event carries the E4 field set; unavailable values are not_evaluated."""
    builders = {
        "plan": wp_fixtures.plan_event(),
        "dispatch": wp_fixtures.dispatch_event(),
        "settle": wp_fixtures.settle_event(),
        "verdict": wp_fixtures.verdict_event(),
        "retry": wp_fixtures.retry_event(),
        "integrate": wp_fixtures.integrate_event(),
        "stage-close": wp_fixtures.stage_close_event(),
        "wp_failed": wp_fixtures.wp_failed_event(),
    }
    assert set(builders) == set(EVENT_TYPES)
    for event_name, event in builders.items():
        assert event["event"] == event_name
        assert EVENT_REQUIRED_FIELDS[event_name] <= set(event), event_name

    assert wp_fixtures.stage_close_event()["token_cost"] == "not_evaluated"

    implement_dispatch = wp_fixtures.implement_dispatch_event()
    assert IMPLEMENT_DISPATCH_FIELDS <= set(implement_dispatch)
    assert implement_dispatch["part_id"] == implement_dispatch["wp_id"]

    text = _model_text()
    assert "WP-10" in text
    assert "E4" in text


def test_wp_11_attempt_scoped_evidence_paths(tmp_path):
    """WP-11: evidence is per-entry and attempt-scoped under the state directory."""
    state_dir = tmp_path / "state"
    paths = wp_fixtures.attempt_scoped_evidence(state_dir)

    assert paths["result"] == (
        state_dir / "wp" / "line-demo-plan-plan-wp01-a1w1.result.json"
    )
    assert paths["verdict"] == (
        state_dir / "wp" / "line-demo-plan-plan-wp01-a1w1.verdict.json"
    )
    assert paths["gate"] == state_dir / "wp" / "line-demo-plan-a1-gate-plan.json"
    assert paths["report_md"] == (
        state_dir / "reports" / "line-demo-plan-a1-coordination.md"
    )
    assert paths["report_json"] == (
        state_dir / "reports" / "line-demo-plan-a1-coordination.json"
    )
    for path in paths.values():
        assert state_dir in path.parents

    text = _model_text()
    assert "WP-11" in text
    assert ".result.json" in text
    assert ".verdict.json" in text
    assert "coordination" in text


def test_wp_12_implement_projection_of_the_067_brief():
    """WP-12: the implement WP is the 067 part brief plus WP fields, in one dispatch log."""
    contract = _contract("work-package-model.md")
    for field in IMPLEMENT_DISPATCH_FIELDS:
        assert field in contract, field
    assert "one brief format and one dispatch log" in contract

    text = _model_text()
    assert "WP-12" in text
    assert "067" in text
    assert "part_id" in text
    assert "test_delta" in text


def test_wp_13_single_package_representation(tmp_path):
    """WP-13: one synthetic package, the stage sentinel, and no integrator outputs."""
    plan = wp_fixtures.make_single_package_plan()
    assert plan["decision"] == "single-package"
    assert plan["gate_verdict"] == "single-package"
    assert plan["rule"] is None
    assert plan["slot_cap"] == 1
    assert plan["integrator_outputs"] == []
    assert len(plan["packages"]) == 1

    package = plan["packages"][0]
    assert package["wp_id"] == "plan-wp01"
    assert package["kind"] == "write"
    assert package["parallel_safe"] is False
    assert package["bounded_by"] == {"unit": "acceptance", "count": 1}
    assert package["sentinel"] == "PLAN-DONE"

    completed = _run_plan(tmp_path, plan)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    record = _record(completed)
    assert record["verdict"] == "single-package"
    assert record["findings"] == []
    assert record["dispatch_layers"] == [["plan-wp01"]]
    assert record["integration_order"] == ["plan-wp01"]

    text = _model_text()
    assert "WP-13" in text
    assert "<STAGE>-DONE" in text
    assert "integrator_outputs" in text


def test_wp_14_canonical_location_and_no_second_ledger():
    """WP-14: the only WP ledgers are spine fences; no spec-local or side ledger exists."""
    assert list(DRIVER_ROOT.rglob("*.jsonl")) == []

    text = _model_text()
    assert "WP-14" in text
    assert "no second ledger" in text
    assert "line state spine" in text

    contract = _contract("work-package-model.md")
    assert "No spec-local plan file, no second JSONL stream" in contract


def test_wp_15_output_coverage_and_integrator_carve_out(tmp_path):
    """WP-15: required outputs are covered exactly once; integrator_outputs are excluded (WG-08)."""
    unowned = wp_fixtures.make_two_package_plan()
    unowned["required_outputs"].append("findings/unowned.md")
    _rehash(unowned)
    unowned_run = _run_plan(tmp_path / "unowned", unowned)
    assert unowned_run.returncode == 1, unowned_run.stdout + unowned_run.stderr
    assert "orphan-output" in _codes(unowned_run)

    duplicate = wp_fixtures.make_two_package_plan()
    duplicate["packages"][1]["outputs"] = ["findings/plan-wp01.md"]
    duplicate["required_outputs"] = ["findings/plan-wp01.md"]
    _rehash(duplicate)
    duplicate_run = _run_plan(tmp_path / "duplicate", duplicate)
    assert duplicate_run.returncode == 1, duplicate_run.stdout + duplicate_run.stderr
    assert "duplicate-output" in _codes(duplicate_run)

    non_required = wp_fixtures.make_two_package_plan()
    non_required["packages"][0]["outputs"].append("findings/extra.md")
    _rehash(non_required)
    non_required_run = _run_plan(tmp_path / "non-required", non_required)
    assert non_required_run.returncode == 1, (
        non_required_run.stdout + non_required_run.stderr
    )
    assert "orphan-output" in _codes(non_required_run)

    unconsumed = wp_fixtures.make_two_package_plan()
    unconsumed["packages"][0]["intermediate_outputs"] = ["findings/scratch.md"]
    unconsumed["packages"][0]["outputs"].append("findings/scratch.md")
    unconsumed["required_outputs"] = [
        "findings/plan-wp01.md",
        "findings/plan-wp02.md",
    ]
    _rehash(unconsumed)
    unconsumed_run = _run_plan(tmp_path / "unconsumed", unconsumed)
    assert unconsumed_run.returncode == 1, (
        unconsumed_run.stdout + unconsumed_run.stderr
    )
    assert "orphan-output" in _codes(unconsumed_run)

    carve_out = wp_fixtures.make_two_package_plan()
    carve_out["required_outputs"].append("clarification.md")
    carve_out["integrator_outputs"] = ["clarification.md"]
    _rehash(carve_out)
    carve_out_run = _run_plan(tmp_path / "carve-out", carve_out)
    assert carve_out_run.returncode == 0, (
        carve_out_run.stdout + carve_out_run.stderr
    )
    assert _record(carve_out_run)["verdict"] == "admit"

    package_claims_integrator = wp_fixtures.make_two_package_plan()
    package_claims_integrator["required_outputs"].append("clarification.md")
    package_claims_integrator["integrator_outputs"] = ["clarification.md"]
    package_claims_integrator["packages"][0]["outputs"].append("clarification.md")
    _rehash(package_claims_integrator)
    claimed_run = _run_plan(tmp_path / "claimed", package_claims_integrator)
    assert claimed_run.returncode == 1, claimed_run.stdout + claimed_run.stderr
    assert "duplicate-output" in _codes(claimed_run)

    ghost_integrator = wp_fixtures.make_two_package_plan()
    ghost_integrator["integrator_outputs"] = ["ghost.md"]
    _rehash(ghost_integrator)
    ghost_run = _run_plan(tmp_path / "ghost", ghost_integrator)
    assert ghost_run.returncode == 1, ghost_run.stdout + ghost_run.stderr
    assert "schema-missing" in _codes(ghost_run)

    text = _model_text()
    assert "WP-15" in text
    assert "E13" in text
    assert "Mirror Obligations" in text


def test_wp_16_replayability(tmp_path):
    """WP-16: the same artifacts and rule reproduce the same package set and hash."""
    first_plan = wp_fixtures.make_two_package_plan()
    second_plan = wp_fixtures.make_two_package_plan()
    assert first_plan["plan_hash"] == second_plan["plan_hash"]

    first_run = _run_plan(tmp_path / "first", first_plan)
    second_run = _run_plan(tmp_path / "second", second_plan)
    assert first_run.returncode == second_run.returncode == 0
    assert _record(first_run)["plan_hash"] == _record(second_run)["plan_hash"]
    assert (
        _record(first_run)["dispatch_layers"]
        == _record(second_run)["dispatch_layers"]
    )

    changed = copy.deepcopy(first_plan)
    changed["packages"][0]["source_refs"] = ["requirements.md#other"]
    _rehash(changed)
    assert changed["plan_hash"] != first_plan["plan_hash"]

    text = _model_text()
    assert "WP-16" in text
    assert "replay" in text


def test_wp_17_timestamp_units(tmp_path):
    """WP-17: ledger arithmetic uses epoch seconds; evidence uses ISO-8601."""
    dispatch = wp_fixtures.dispatch_event()
    settle = wp_fixtures.settle_event()
    close = wp_fixtures.stage_close_event()
    for value in (dispatch["started_at"], settle["ended_at"], close["stage_u4_at"]):
        assert isinstance(value, int) and not isinstance(value, bool)

    completed = _run_plan(tmp_path, wp_fixtures.make_two_package_plan())
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert ISO_8601.match(_record(completed)["checked_at"])

    text = _model_text()
    assert "WP-17" in text
    assert "epoch seconds" in text
    assert "ISO-8601" in text

    contract = _contract("work-package-model.md")
    assert "epoch seconds" in contract
    assert "ISO-8601" in contract


def test_wp_18_spine_write_authority(tmp_path):
    """WP-18: the driver owns the fences; package executors never write the spine."""
    plan = wp_fixtures.make_two_package_plan()
    spine = _spine(tmp_path, plan=plan)
    before = spine.read_bytes()
    completed = _run_plan(tmp_path, plan)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert spine.read_bytes() == before

    text = _model_text()
    assert "WP-18" in text
    assert "transport" in text
    assert "never write" in text.lower()

    contract = _contract("work-package-model.md")
    assert "package executors never write a fence" in contract


OR_CONTRACT_PINS = {
    "OR-01": (
        "`plan`, `dispatch`",
        "`wp_failed`",
        "only event types",
    ),
    "OR-02": (
        "attempt_id = <wp_id>-a<stage_attempt>-w<wp_attempt>",
        "Result and verdict evidence carry the same identity",
    ),
    "OR-03": (
        "`stage_u4_at`",
        "`wall_clock_seconds`",
        "`critical_path_seconds`",
        "`parallelism_efficiency`",
        "`retries_package`",
        "`retries_stage`",
        "`stage_attempts`",
        "`canonical_stages`",
        "`stage_executions_per_canonical`",
        "`manual_interventions`",
        "`sessions`",
        "`token_cost`",
        "`report_ptr`",
    ),
    "OR-04": (
        "stage_u4_at - first started_at",
        "not_evaluated",
        "never inferred from commit timestamps",
    ),
    "OR-05": (
        "duration-weighted longest path",
        "cp[node] = duration[node] + max(cp[dep])",
        "not_evaluated",
    ),
    "OR-06": (
        "sum(package durations) / (wall_clock_seconds × max_concurrent_package_count)",
        "with the product in the denominator",
        "excluded",
    ),
    "OR-07": (
        "stage_attempts / canonical_stages",
        "canonical_stages = 8",
        "never increments the numerator",
    ),
    "OR-08": (
        "retries_package",
        "retries_stage = stage_attempt - 1",
        "does not consume the stage retry budget",
    ),
    "OR-09": (
        "manual_interventions_per_session = manual_interventions / sessions",
        "--manual-interventions",
        "--sessions",
        "not_evaluated",
    ),
    "OR-10": (
        "literal string `not_evaluated`",
        "never `0`",
        "explicitly waives",
        "SC-001",
    ),
    "OR-11": (
        "wp-report.py --spine <path>",
        "--out-dir <state-dir>/reports",
        "<line>-<stage>-a<N>-coordination.md",
        "never writes the spine",
    ),
    "OR-12": (
        "decomposition decision",
        "parallel-overlap flag",
        "raw transcripts",
    ),
    "OR-13": (
        "At least three comparable samples",
        "plan 70 minutes, review 37 minutes",
        "56 minutes",
        "29.6 minutes",
    ),
    "OR-14": (
        "counting ledger `dispatch` events",
        "no separate counter file",
        "inherits the parent's attempt count",
        "fresh WP counter",
    ),
    "OR-15": (
        "{changed[], reason, scope?, budget?, topology?}",
        "strictly decreases",
        "strictly increases",
        "split depth is one",
        "identical same-budget rerun",
    ),
    "OR-16": (
        "Attempt 3 is rejected as `retry-exhausted`",
        "split child's further attempt",
        "`wp_failed`",
        "default two stage retries",
    ),
}


@pytest.mark.parametrize(
    "clause", sorted(OR_CONTRACT_PINS), ids=sorted(OR_CONTRACT_PINS)
)
def test_or_contract_clause_keeps_its_normative_content(clause):
    """Each OR clause keeps its formula, fields, or rule in the owner contract."""
    contract = _contract("observability-and-retry.md")
    for snippet in OR_CONTRACT_PINS[clause]:
        assert snippet in contract, (clause, snippet)


def test_or_02_attempt_identity_is_addressable():
    """OR-02: attempt identity is <wp_id>-a<stage_attempt>-w<wp_attempt>."""
    dispatch = wp_fixtures.dispatch_event()
    expected = "%s-a%d-w%d" % (
        dispatch["wp_id"],
        dispatch["stage_attempt"],
        dispatch["wp_attempt"],
    )
    assert dispatch["attempt_id"] == expected

    implement = wp_fixtures.implement_dispatch_event()
    assert implement["attempt_id"] == "%s-a1-w1" % implement["wp_id"]
    assert "OR-02" in _model_text()


def test_or_03_stage_close_field_set():
    """OR-03: the stage-close record carries every declared field."""
    event = wp_fixtures.stage_close_event()
    assert EVENT_REQUIRED_FIELDS["stage-close"] <= set(event)
    assert isinstance(event["stage_u4_at"], int)
    assert event["stage_attempts"] == 1
    assert event["canonical_stages"] == 8
    assert event["stage_executions_per_canonical"] == 0.125
    assert event["token_cost"] == "not_evaluated"
    assert event["report_ptr"].endswith("-coordination.json")


def test_or_14_retry_counter_is_ledger_derived():
    """OR-14: the counter comes from dispatch events; there is no counter file."""
    event = wp_fixtures.retry_event()
    assert event["wp_attempt"] == 2
    assert "retry_delta" in event
    assert "gate_evidence" in event

    contract = _contract("observability-and-retry.md")
    assert "no separate counter file" in contract
    assert "inherits the parent's attempt count" in contract


def test_or_15_retry_delta_schema():
    """OR-15: a delta names a change and makes it mechanically checkable."""
    delta = wp_fixtures.retry_event()["retry_delta"]
    assert delta["changed"]
    assert set(delta["changed"]) <= {"scope", "budget", "topology"}
    assert delta["budget"]["to_max_turns"] > delta["budget"]["from_max_turns"]
    assert delta["budget"]["evidence_ref"]

    contract = _contract("observability-and-retry.md")
    for topology in (
        "parallel-native",
        "serial-native",
        "detached-runner",
        "split-serial-children",
    ):
        assert topology in contract, topology


def test_or_16_escalation_record():
    """OR-16: a second package failure records wp_failed and enters the unchanged U5 path."""
    event = wp_fixtures.wp_failed_event()
    assert event["attempts"] == 2
    assert event["verdict_evidence"].endswith(".verdict.json")
    contract = _contract("observability-and-retry.md")
    assert "default two stage retries" in contract
    assert "never silently reuses the failed package set" in contract

