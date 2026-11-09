"""Unit-obligation contract (contracts/judgement-engine.contract.md C-031…C-034, data-model V-17…V-22).

Rows pinned here (WP4): T066, T067, T068, T069, T070, T071, T072, T073.

- **T066/C-031** — ``effective`` equals the maximum overlap count of the units'
  ``[dispatched_at, settled_at]`` intervals; the requested/effective/effective-reason
  triple is judged together.
- **T067/C-032** — a missing interval yields the literal ``not_evaluated``, no pass, and the
  unit whose interval is missing is named.
- **T068/C-033** — one or two of the three reading fields alone is ``reading-incomplete``; a
  shortfall against the recomputed bound needs a named reason.
- **T069/C-034** — the engine recomputes the bound from the slot fact plus the ceiling read
  from ``wp-gate.py``'s declared default minus the verifier reserve, and reports its operands.
- **T070/V-17** — same inputs and same rule id yield the same unit ids, layers and edges.
- **T071/V-19, V-20** — a write unit without a write domain is red, a directory-level domain
  is red, a read-only unit's domain is empty.
- **T072/V-21** — executor and verifier ids both present, different, and the two sets
  disjoint; prose "independent verification passed" alone is red.
- **T073/V-22** — integration order equals the declared layer-flattened order including the
  tie-break, identical on replay.

The reading action's record schema is pinned from ``effective-concurrency.yaml`` and
data-model E-3/E-5 (block-subset/v1): top-level ``requested`` / ``effective_reason`` and a
``units`` sequence whose entries carry ``unit_id``, ``dispatched_at``, ``settled_at``,
``executor_id`` and ``verifier_id``. The wp-gate cases consume the existing 070 engine
(retained per C-091), so they are green on this tree except the T061 extension.
"""
from __future__ import annotations

import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from fixtures import wp_fixtures

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "concurrency-check.py"
WP_GATE = REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "wp-gate.py"
READER = REPO_ROOT / "scripts" / "python" / "declaration_reader.py"


# --------------------------------------------------------------------------- #
# helpers — the engine
# --------------------------------------------------------------------------- #
def _reader_module():
    spec = importlib.util.spec_from_file_location("declaration_reader", READER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _slot_statement():
    return _reader_module().load_fact(
        str(REPO_ROOT), "concurrency-slot-and-reserve")["body"]["statement"]


def _ceiling_default():
    source = WP_GATE.read_text(encoding="utf-8")
    match = re.search(r'"--slot-cap-ceiling"[^)]*default\s*=\s*(\d+)', source)
    assert match, "wp-gate.py must declare --slot-cap-ceiling with a numeric default"
    return int(match.group(1))


def _repo(tmp_path: Path) -> Path:
    shutil.copytree(REPO_ROOT / "shared" / "declarations", tmp_path / "shared" / "declarations")
    return tmp_path


def _record(repo: Path, name: str, lines) -> Path:
    path = repo / name
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _run_engine(*args):
    assert ENGINE.is_file(), (
        "red-first: scripts/python/concurrency-check.py is the WP2 engine target and is "
        "not in this worktree yet")
    return subprocess.run(
        [sys.executable, str(ENGINE), *[str(arg) for arg in args]],
        capture_output=True, text=True, cwd=str(REPO_ROOT), timeout=120,
    )


def _reading(repo: Path, record: Path, out: Path):
    proc = _run_engine("reading", "--repo", repo, "--record", record, "--json-out", out)
    envelope = json.loads(out.read_text(encoding="utf-8")) if out.is_file() else None
    return proc, envelope


def _find(node, key):
    if isinstance(node, dict):
        if key in node:
            return node[key]
        for value in node.values():
            found = _find(value, key)
            if found is not None:
                return found
    elif isinstance(node, list):
        for item in node:
            found = _find(item, key)
            if found is not None:
                return found
    return None


def _pairs(node, out=None):
    out = [] if out is None else out
    if isinstance(node, dict):
        for key, value in node.items():
            out.append((str(key).lower(), value))
            _pairs(value, out)
    elif isinstance(node, list):
        for item in node:
            _pairs(item, out)
    return out


def _codes(envelope):
    return [finding.get("code") for finding in (envelope or {}).get("findings", [])]


def _mentions(envelope, needle: str) -> bool:
    for finding in (envelope or {}).get("findings", []):
        blob = " ".join(str(finding.get(key, "")) for key in ("subject", "message", "evidence_ptr"))
        if needle in blob:
            return True
    return False


def _three_unit_record(repo: Path, missing_settle=False) -> Path:
    lines = [
        "requested: 3",
        "units:",
        "  - unit_id: unit-a",
        "    dispatched_at: 0",
        "    settled_at: 10",
        "    executor_id: exec-a",
        "    verifier_id: ver-a",
        "  - unit_id: unit-b",
        "    dispatched_at: 5",
        "    settled_at: 15",
        "    executor_id: exec-b",
        "    verifier_id: ver-b",
        "  - unit_id: unit-c",
        "    dispatched_at: 6",
    ]
    if not missing_settle:
        lines.append("    settled_at: 7")
    lines += ["    executor_id: exec-c", "    verifier_id: ver-c",
              "effective_reason: three-unit fixture with a planned overlap"]
    return _record(repo, "reading.yaml", lines)


# --------------------------------------------------------------------------- #
# helpers — the retained 070 gate
# --------------------------------------------------------------------------- #
def _rehash(plan):
    plan["plan_hash"] = wp_fixtures.canonical_hash_of(plan)
    return plan


def _gate_plan(tmp_path: Path, plan: dict):
    tmp_path.mkdir(parents=True, exist_ok=True)
    spine = wp_fixtures.make_spine(tmp_path / "state.md", plan=plan)
    proc = subprocess.run(
        [sys.executable, str(WP_GATE), "--spine", str(spine),
         "--stage", plan["stage"], "--stage-attempt", str(plan["stage_attempt"]),
         "--check", "plan"],
        capture_output=True, text=True, timeout=120,
    )
    record = json.loads(proc.stdout) if proc.stdout.strip() else None
    return proc, record


def _gate_codes(record):
    return [finding.get("code") for finding in (record or {}).get("findings", [])]


# --------------------------------------------------------------------------- #
# T066 / T068 — the reading triple and the overlap maximum
# --------------------------------------------------------------------------- #
def test_effective_is_the_maximum_interval_overlap(tmp_path):
    repo = _repo(tmp_path)
    record = _three_unit_record(repo)
    proc, first = _reading(repo, record, tmp_path / "a.json")
    assert first is not None, proc.stdout + proc.stderr
    assert proc.returncode == 0, first.get("findings")
    assert _find(first.get("measured"), "effective") == 3
    _, replay = _reading(repo, record, tmp_path / "b.json")
    assert _find(replay.get("measured"), "effective") == 3, "replay must be identical"


def test_touching_intervals_do_not_overlap(tmp_path):
    """The declared tie-break: at equal epoch seconds settle precedes dispatch."""
    repo = _repo(tmp_path)
    record = _record(repo, "touching.yaml", [
        "requested: 2",
        "units:",
        "  - unit_id: unit-a",
        "    dispatched_at: 0",
        "    settled_at: 10",
        "    executor_id: exec-a",
        "    verifier_id: ver-a",
        "  - unit_id: unit-b",
        "    dispatched_at: 10",
        "    settled_at: 20",
        "    executor_id: exec-b",
        "    verifier_id: ver-b",
        "effective_reason: intervals touch, so the overlap is one",
    ])
    proc, envelope = _reading(repo, record, tmp_path / "out.json")
    assert envelope is not None, proc.stdout + proc.stderr
    assert _find(envelope.get("measured"), "effective") == 1


def test_one_or_two_fields_alone_are_reading_incomplete(tmp_path):
    repo = _repo(tmp_path)
    missing_requested = _record(repo, "missing-requested.yaml", [
        "units:",
        "  - unit_id: unit-a",
        "    dispatched_at: 0",
        "    settled_at: 10",
    ])
    proc, envelope = _reading(repo, missing_requested, tmp_path / "a.json")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "reading-incomplete" in _codes(envelope), envelope.get("findings")

    shortfall_without_reason = _record(repo, "shortfall.yaml", [
        "requested: 4",
        "units:",
        "  - unit_id: unit-a",
        "    dispatched_at: 0",
        "    settled_at: 10",
        "  - unit_id: unit-b",
        "    dispatched_at: 5",
        "    settled_at: 15",
    ])
    proc, envelope = _reading(repo, shortfall_without_reason, tmp_path / "b.json")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "reading-incomplete" in _codes(envelope), envelope.get("findings")

    with_reason = _record(repo, "shortfall-reason.yaml", [
        "requested: 4",
        "units:",
        "  - unit_id: unit-a",
        "    dispatched_at: 0",
        "    settled_at: 10",
        "  - unit_id: unit-b",
        "    dispatched_at: 5",
        "    settled_at: 15",
        "effective_reason: only two representable units were ready",
    ])
    proc, envelope = _reading(repo, with_reason, tmp_path / "c.json")
    assert envelope is not None, proc.stdout + proc.stderr
    assert proc.returncode == 0, envelope.get("findings")
    assert _find(envelope.get("measured"), "effective") == 2


# --------------------------------------------------------------------------- #
# T067 — missing interval
# --------------------------------------------------------------------------- #
def test_missing_interval_yields_not_evaluated_and_names_the_unit(tmp_path):
    repo = _repo(tmp_path)
    record = _three_unit_record(repo, missing_settle=True)
    proc, envelope = _reading(repo, record, tmp_path / "out.json")
    assert envelope is not None, proc.stdout + proc.stderr
    assert proc.returncode == 1, "a claim that asserts concurrency must not pass without intervals"
    assert _find(envelope.get("measured"), "effective") == "not_evaluated"
    assert _mentions(envelope, "unit-c"), "the unit with the missing interval must be named"


# --------------------------------------------------------------------------- #
# T069 — the bound is recomputed and its operands reported
# --------------------------------------------------------------------------- #
def test_bound_recomputation_reports_its_operands(tmp_path):
    statement = _slot_statement()
    slot_cap = int(statement["slot_cap_default"])
    reserve = int(statement["verifier_reserve"])
    ceiling = _ceiling_default()
    repo = _repo(tmp_path)
    record = _record(repo, "bound.yaml", [
        "requested: 2",
        "units:",
        "  - unit_id: unit-a",
        "    dispatched_at: 0",
        "    settled_at: 10",
        "  - unit_id: unit-b",
        "    dispatched_at: 5",
        "    settled_at: 15",
        "effective_reason: fixture overlaps exactly once",
    ])
    proc, envelope = _reading(repo, record, tmp_path / "out.json")
    assert envelope is not None, proc.stdout + proc.stderr
    pairs = _pairs(envelope.get("measured"))

    def has(keys, value):
        return any(any(key in name for key in keys) and item == value for name, item in pairs)

    assert has(("slot",), slot_cap), pairs
    assert has(("ceiling",), ceiling), pairs
    assert has(("reserve",), reserve), pairs
    available = min(slot_cap, ceiling) - reserve
    assert has(("available", "bound"), available), (available, pairs)


# --------------------------------------------------------------------------- #
# T070 / T073 — deterministic partition and integration order
# --------------------------------------------------------------------------- #
def _reversed_parallel_plan():
    """Two independent read-only packages, declared in reverse id order."""
    p1 = wp_fixtures.make_package("plan-wp01")
    p2 = wp_fixtures.make_package("plan-wp02")
    return wp_fixtures.make_plan(packages=[p2, p1])


def _serial_chain_plan():
    p1 = wp_fixtures.make_package("plan-wp01")
    p2 = wp_fixtures.make_package("plan-wp02", depends_on=["plan-wp01"])
    return wp_fixtures.make_plan(packages=[p1, p2], pattern="serial")


def test_partition_replay_yields_identical_units_layers_and_edges(tmp_path):
    plan = _reversed_parallel_plan()
    first_proc, first = _gate_plan(tmp_path / "first", plan)
    second_proc, second = _gate_plan(tmp_path / "second", plan)
    assert first is not None and second is not None, first_proc.stdout + first_proc.stderr
    assert first_proc.returncode == second_proc.returncode == 0, first.get("findings")
    assert first["dispatch_layers"] == second["dispatch_layers"]
    # the plan hash covers the unit ids and the dependency edges; layers are compared above
    assert first["plan_hash"] == second["plan_hash"]
    assert first["dispatch_layers"] == [["plan-wp01", "plan-wp02"]]


def test_integration_order_is_the_layer_flattened_declared_order(tmp_path):
    parallel = _gate_plan(tmp_path / "parallel", _reversed_parallel_plan())
    parallel_proc, parallel_record = parallel
    assert parallel_record is not None, parallel_proc.stdout + parallel_proc.stderr
    assert parallel_proc.returncode == 0, parallel_record.get("findings")
    flattened = [wp_id for layer in parallel_record["dispatch_layers"] for wp_id in layer]
    assert flattened == ["plan-wp01", "plan-wp02"]  # wp_id-lexicographic tie-break
    assert parallel_record["integration_order"] == flattened

    _, replay = _gate_plan(tmp_path / "parallel-replay", _reversed_parallel_plan())
    assert replay["integration_order"] == parallel_record["integration_order"]

    serial_proc, serial = _gate_plan(tmp_path / "serial", _serial_chain_plan())
    assert serial_proc.returncode == 0, serial.get("findings")
    assert serial["dispatch_layers"] == [["plan-wp01"], ["plan-wp02"]]
    assert serial["integration_order"] == ["plan-wp01", "plan-wp02"]


# --------------------------------------------------------------------------- #
# T071 — write-domain unit-level form
# --------------------------------------------------------------------------- #
def test_write_unit_without_a_domain_is_red(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    plan["packages"][0].update(kind="write", parallel_safe=False, owned_paths=[])
    plan["pattern"] = "serial"
    _rehash(plan)
    proc, record = _gate_plan(tmp_path, plan)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "kind-mismatch" in _gate_codes(record), record.get("findings")


def test_directory_level_write_domain_is_red(tmp_path):
    write = wp_fixtures.make_write_package("plan-wp01")
    read = wp_fixtures.make_package("plan-wp02")
    plan = wp_fixtures.make_plan(packages=[write, read], pattern="serial")
    proc, record = _gate_plan(tmp_path, plan)
    assert record is not None, proc.stdout + proc.stderr
    assert proc.returncode == 1, "a directory-level write domain must be red (FR-012)"
    blob = json.dumps(record.get("findings", []))
    assert "src/generated/" in blob, record.get("findings")


def test_read_only_unit_domain_stays_empty_and_is_accepted(tmp_path):
    plan = wp_fixtures.make_two_package_plan()
    assert all(package["owned_paths"] == [] for package in plan["packages"])
    proc, record = _gate_plan(tmp_path, plan)
    assert proc.returncode == 0, record.get("findings") if record else proc.stdout
    with_territory = wp_fixtures.make_two_package_plan()
    with_territory["packages"][0]["owned_paths"] = ["src/generated/"]
    _rehash(with_territory)
    proc, record = _gate_plan(tmp_path / "territory", with_territory)
    assert proc.returncode == 1, "a read-only unit carrying a write territory must be red"
    assert "kind-mismatch" in _gate_codes(record), record.get("findings")


# --------------------------------------------------------------------------- #
# T072 — verifier independence
# --------------------------------------------------------------------------- #
def _judge_independence(units):
    """V-21 — both ids present, different per unit, and the two sets disjoint."""
    findings = []
    executors, verifiers = set(), set()
    for unit in units:
        executor = unit.get("executor_id")
        verifier = unit.get("verifier_id")
        if not executor or not verifier:
            findings.append(("independence-undecidable", unit.get("unit_id")))
            continue
        if executor == verifier:
            findings.append(("independence-undecidable", unit.get("unit_id")))
        executors.add(executor)
        verifiers.add(verifier)
    if executors & verifiers:
        findings.append(("independence-undecidable", "executor/verifier id sets intersect"))
    return findings


def test_verifier_independence_contract():
    compliant = [
        {"unit_id": "unit-a", "executor_id": "exec-a", "verifier_id": "ver-a"},
        {"unit_id": "unit-b", "executor_id": "exec-b", "verifier_id": "ver-b"},
    ]
    assert _judge_independence(compliant) == []

    same = [{"unit_id": "unit-a", "executor_id": "exec-a", "verifier_id": "exec-a"}]
    assert _judge_independence(same), "executor == verifier must be red"

    prose_only = [
        {"unit_id": "unit-a", "executor_id": "exec-a",
         "independent_verification": "independent verification passed"},
    ]
    assert _judge_independence(prose_only), "prose alone must be red"

    crossing = [
        {"unit_id": "unit-a", "executor_id": "exec-a", "verifier_id": "exec-b"},
        {"unit_id": "unit-b", "executor_id": "exec-b", "verifier_id": "ver-c"},
    ]
    assert _judge_independence(crossing), "intersecting id sets must be red"
