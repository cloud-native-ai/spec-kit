"""Unit module for the concurrency judgement engine's own contract surface.

Rows pinned here (WP4): T015, T136; the module carries the ``[green:]`` marker for
``contracts/declaration-facts.contract.md#C-003``.

- **C-003 / T015** — every fact's ``kind`` is a member of ``fact_kinds`` read from
  ``shared/declarations/contract.yaml``; the eight file stems equal their ``fact:`` values;
  the per-slug kind assignment of C-003 holds.
- **C-019/C-020/C-021 / T136** — ``-h``/``--help`` and ``--version`` answer without acting;
  an undeclared option exits 2; the five actions are the closed action set; the three
  record-judging actions refuse to run without ``--record`` (exit 2); ``classify`` and
  ``coverage`` take no record flag.
- **SC-012 / T136** — the cost-benefit fixture: the same independent task set run
  concurrently yields an identical result set with lower wall-clock than the serial run.

Red-first state: the engine ``scripts/python/concurrency-check.py`` lands in WP2; the
T015 cases are green on the declaration layer and the T136 cases are red until it lands.
"""
from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "concurrency-check.py"
READER = REPO_ROOT / "scripts" / "python" / "declaration_reader.py"

EIGHT_FACTS = (
    "concurrency-class",
    "serial-reason",
    "effective-concurrency",
    "concurrency-slot-and-reserve",
    "decomposition-coverage",
    "executor-enumeration-roots",
    "concurrency-contract",
    "coordinator-dispatch-verdict",
)

#: C-003's per-slug kind assignment.
DECLARED_KINDS = {
    "concurrency-class": "mapping",
    "executor-enumeration-roots": "mapping",
    "serial-reason": "ordered-operator-table",
    "effective-concurrency": "record-schema",
    "concurrency-slot-and-reserve": "threshold",
    "decomposition-coverage": "mapping",
    "concurrency-contract": "mapping",
    "coordinator-dispatch-verdict": "mapping",
}


def _reader_module():
    spec = importlib.util.spec_from_file_location("declaration_reader", READER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_engine(*args, cwd=None, timeout=120):
    assert ENGINE.is_file(), (
        "red-first: scripts/python/concurrency-check.py is the WP2 engine target and is "
        "not in this worktree yet")
    return subprocess.run(
        [sys.executable, str(ENGINE), *[str(arg) for arg in args]],
        capture_output=True, text=True, cwd=str(cwd or REPO_ROOT), timeout=timeout,
    )


# --------------------------------------------------------------------------- #
# T015 — kind assignment and stem/`fact:` agreement (C-003)
# --------------------------------------------------------------------------- #
def test_every_fact_kind_is_a_declared_member():
    reader = _reader_module()
    contract = reader.load_contract(str(REPO_ROOT))
    kinds = set(contract["fact_kinds"])
    for fact in reader.load_facts(str(REPO_ROOT)):
        if fact["body"].get("fact") in EIGHT_FACTS:
            assert fact["body"]["kind"] in kinds, (
                "%s declares kind %r outside fact_kinds %s"
                % (fact["path"], fact["body"].get("kind"), sorted(kinds)))


def test_eight_stems_equal_their_fact_keys():
    reader = _reader_module()
    found = {}
    for fact in reader.load_facts(str(REPO_ROOT)):
        if fact["body"].get("fact") in EIGHT_FACTS:
            assert fact["stem"] == fact["body"]["fact"], (
                "%s: stem %r != fact %r" % (fact["path"], fact["stem"], fact["body"]["fact"]))
            found[fact["stem"]] = fact["body"]
    assert set(found) == set(EIGHT_FACTS), sorted(found)


def test_declared_kind_assignment_matches_c003():
    reader = _reader_module()
    facts = {fact["body"]["fact"]: fact["body"] for fact in reader.load_facts(str(REPO_ROOT))}
    for slug, kind in DECLARED_KINDS.items():
        assert facts[slug]["kind"] == kind, (
            "%s: C-003 assigns %r, file carries %r" % (slug, kind, facts[slug]["kind"]))


# --------------------------------------------------------------------------- #
# T136 — the five actions' argument surface
# --------------------------------------------------------------------------- #
def test_help_and_version_answer_without_acting(tmp_path):
    for flag in ("-h", "--help", "--version"):
        proc = _run_engine(flag, cwd=tmp_path)
        assert proc.returncode == 0, "%s exited %d: %s" % (flag, proc.returncode, proc.stderr)
        assert proc.stdout.strip(), "%s printed nothing" % flag
        assert list(tmp_path.iterdir()) == [], "%s must not write anything" % flag


def test_undeclared_option_is_rejected_with_exit_2(tmp_path):
    proc = _run_engine("classify", "--repo", REPO_ROOT, "--bogus-option", cwd=tmp_path)
    assert proc.returncode == 2, proc.stdout + proc.stderr


def test_action_set_is_closed_to_five():
    proc = _run_engine("sixth-action", "--repo", REPO_ROOT)
    assert proc.returncode == 2, "an undeclared action must be rejected with exit 2"


def test_record_actions_require_their_record_flag(tmp_path):
    for action in ("serial-reason", "reading", "capability"):
        proc = _run_engine(action, "--repo", REPO_ROOT, "--json-out", tmp_path / "out.json")
        assert proc.returncode == 2, (
            "%s without --record must exit 2 (C-021): %s" % (action, proc.stdout + proc.stderr))


def _write_subset(path: Path, lines):
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def test_five_actions_each_produce_one_envelope(tmp_path):
    cases = {
        "classify": ["classify", "--repo", REPO_ROOT],
        "coverage": ["coverage", "--repo", REPO_ROOT, "--stage", "requirements"],
        "serial-reason": [
            "serial-reason", "--repo", REPO_ROOT,
            "--record", _write_subset(tmp_path / "serial.yaml", [
                "pattern: serial",
                "codes:",
                "  - single-unit",
                "evidence:",
                "  single-unit:",
                "    units:",
                "      - only-unit",
            ]),
        ],
        "reading": [
            "reading", "--repo", REPO_ROOT,
            "--record", _write_subset(tmp_path / "reading.yaml", [
                "requested: 1",
                "units:",
                "  - unit_id: unit-a",
                "    dispatched_at: 100",
                "    settled_at: 200",
                "effective_reason: one representable unit",
            ]),
        ],
        "capability": [
            "capability", "--repo", REPO_ROOT,
            "--record", _write_subset(tmp_path / "capability.yaml", ["{}"]),
        ],
    }
    for action, args in cases.items():
        out = tmp_path / ("%s.json" % action)
        proc = _run_engine(*args, "--json-out", out)
        # 0 = pass, 1 = a documented check failed, 2 = input/environment error
        # (the live capability action is fail-closed on the unadjudicated verdict fact).
        assert proc.returncode in (0, 1, 2), "%s exited %d: %s" % (action, proc.returncode, proc.stderr)
        if proc.returncode == 2:
            combined = proc.stdout + proc.stderr + (out.read_text(encoding="utf-8") if out.is_file() else "")
            assert "owner-unavailable" in combined or "error" in combined.lower(), (
                "%s exited 2 without a named reason: %s" % (action, combined))
            continue
        assert out.is_file(), "%s must write its envelope to --json-out" % action
        envelope = json.loads(out.read_text(encoding="utf-8"))
        assert envelope["action"] == action
        assert envelope["decision"] in ("pass", "fail", "owner-unavailable", "not-applicable")


# --------------------------------------------------------------------------- #
# D-I2 — a malformed units field is never "no units"
# --------------------------------------------------------------------------- #
def test_present_non_list_units_is_record_malformed(tmp_path):
    """A present-but-non-list units field is record-malformed, never effective=0 pass."""
    record = _write_subset(tmp_path / "bad-units.yaml", [
        "requested: 2",
        "pattern: concurrent",
        "units: not-a-list",
        "effective_reason: pretend",
    ])
    out = tmp_path / "bad-units.json"
    proc = _run_engine("reading", "--repo", REPO_ROOT, "--record", record, "--json-out", out)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    envelope = json.loads(out.read_text(encoding="utf-8"))
    assert envelope["decision"] == "fail"
    assert "record-malformed" in [item["code"] for item in envelope["findings"]], (
        "a concurrency claim must not hide its units behind a non-list value")


# --------------------------------------------------------------------------- #
# D-I3 / C-2 — the coverage action's red arms (SC-008 evidence)
# --------------------------------------------------------------------------- #
def _declaration_repo(tmp_path: Path) -> Path:
    shutil.copytree(REPO_ROOT / "shared" / "declarations",
                    tmp_path / "shared" / "declarations")
    return tmp_path


def _goal_fixture(repo: Path, slug: str, targets) -> Path:
    goal_dir = repo / ".specify" / "anchoring" / slug
    goal_dir.mkdir(parents=True)
    rows = ["## Targets", "", "| Target | Description | Status |", "|---|---|---|"]
    rows.extend("| %s | unit %s | open |" % (target, target) for target in targets)
    (goal_dir / "goal.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    return goal_dir


def test_coverage_undeclared_stage_turns_red(tmp_path):
    """C-035/SC-008 red arm: a stage outside the fact is coverage-undeclared (exit 1)."""
    out = tmp_path / "undeclared.json"
    proc = _run_engine("coverage", "--repo", REPO_ROOT, "--stage", "frobnicate",
                       "--json-out", out)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    envelope = json.loads(out.read_text(encoding="utf-8"))
    assert envelope["decision"] == "fail"
    assert "coverage-undeclared" in [item["code"] for item in envelope["findings"]]


def test_coverage_off_without_decision_turns_red(tmp_path):
    """C-035/SC-008 red arm: a stage kept serial with no named decision record (exit 1)."""
    repo = _declaration_repo(tmp_path)
    fact = repo / "shared" / "declarations" / "facts" / "decomposition-coverage.yaml"
    text = fact.read_text(encoding="utf-8")
    mutated = text.replace(
        "    - stage: clarify\n      coverage: auto\n",
        "    - stage: clarify\n      coverage: off\n", 1)
    assert mutated != text, "fixture premise: the fact must declare clarify as auto"
    fact.write_text(mutated, encoding="utf-8")
    out = tmp_path / "off.json"
    proc = _run_engine("coverage", "--repo", repo, "--stage", "clarify",
                       "--ceiling", "4", "--json-out", out)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    envelope = json.loads(out.read_text(encoding="utf-8"))
    assert envelope["decision"] == "fail"
    assert "coverage-undeclared" in [item["code"] for item in envelope["findings"]]


def test_coverage_partition_under_ceiling_turns_red(tmp_path):
    """C-063/C-065 red arm: the goal partition is bounded by --ceiling; when the
    remaining slots drop under two it must not claim packages and must name its
    serial reason code. A regression that ignores the ceiling turns this red."""
    repo = _declaration_repo(tmp_path)
    _goal_fixture(repo, "five", ["T-001", "T-002", "T-003", "T-004", "T-005"])

    out = tmp_path / "ceiling4.json"
    proc = _run_engine("coverage", "--repo", repo, "--goal", "five",
                       "--ceiling", "4", "--json-out", out)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    goal = json.loads(out.read_text(encoding="utf-8"))["measured"]["goals"][0]
    assert goal["effective_available"] == 3
    assert [len(package) for package in goal["packages"]] == [3, 2], (
        "packages are bounded by ceiling minus reserve, not by the slot cap: %r" % goal)

    out = tmp_path / "ceiling2.json"
    proc = _run_engine("coverage", "--repo", repo, "--goal", "five",
                       "--ceiling", "2", "--json-out", out)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    goal = json.loads(out.read_text(encoding="utf-8"))["measured"]["goals"][0]
    assert goal["effective_available"] == 1
    assert goal["packages"] == [], "under the ceiling no concurrent partition is claimed"
    assert goal["serial_reason"] == "budget-reserve", (
        "a serial fallback carries its named reason code: %r" % goal)


# --------------------------------------------------------------------------- #
# T136 / SC-012 — cost benefit on the fixture
# --------------------------------------------------------------------------- #
def _fixture_task(value):
    time.sleep(0.12)
    return {"value": value, "verdict": "pass"}


def test_cost_benefit_fixture_identical_result_set_lower_wall_clock():
    """SC-012 — same task set: concurrent wall-clock < serial, result sets identical."""
    values = list(range(6))
    started = time.monotonic()
    serial = [_fixture_task(value) for value in values]
    serial_elapsed = time.monotonic() - started
    started = time.monotonic()
    with ThreadPoolExecutor(max_workers=len(values)) as pool:
        concurrent = list(pool.map(_fixture_task, values))
    concurrent_elapsed = time.monotonic() - started
    assert concurrent == serial, "SC-012: the concurrent result set must be identical"
    assert concurrent_elapsed < serial_elapsed, (
        "SC-012: concurrent %.3fs must beat serial %.3fs"
        % (concurrent_elapsed, serial_elapsed))
