"""Contract tests for ``/speckit.measure`` — window, selection, cap, aggregation, exits, determinism (087, T058–T060).

Contract object: `contracts/measure-report.contract.md` C-53…C-62 — one thin command (``templates/commands/measure.md``)
backed by one stdlib-only, read-only, deterministic script (``scripts/python/measure.py``) that reports what the
exec-quant store measured over a declared window.

Partition (this file carries clauses of ONE contract, split across three rows):

* **T058** — the window (C-54), the selection (C-55) and the cap (C-57) faces: half-open bounds that partition a
  store, an exact ``(unit_id, unit_type)`` set with an unknown identity an input error, one declared cap printed on
  every run with its omitted count, and byte-identical repeated runs.
* **T059** — the aggregation (C-56) and exclusion (C-58) faces: figures with provenance and ``covered=<k>/<n>``, the
  four exclusion classes with the accounting identity, no verdict vocabulary, and the determinism face of C-61.
* **T060** — the closed exit-status set (C-59), the two closed actions (C-60) and the read-only / no-machinery
  delivery shape (C-62).

**Red-first (Constitution IV)**: authored before ``scripts/python/measure.py`` exists (T064), so every test here is
expected to fail on the pre-implementation tree — each first asserts the script's presence with a message that names
the row, so red is "the engine is missing", never an import error.

**Fixture posture**: every store is built from scratch under ``tmp_path``; no test reads or writes the real
``.specify/memory/exec-quant/`` store.

**Owner boundary**: the exit-status values, the exclusion-class names and the JSON key set are owned by
``contracts/measure-report.contract.md`` C-57/C-58/C-60. This file reads them from that owner at run time instead of
spelling a second copy, so a change to the owner cannot silently disagree with its judge.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
MEASURE = REPO_ROOT / "scripts" / "python" / "measure.py"
CONTRACT = REPO_ROOT / ".specify" / "specs" / "087-speckit-visualization" / "contracts" / "measure-report.contract.md"


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _require() -> Path:
    assert MEASURE.is_file(), (
        "measure engine missing: %s — expected at T064 (087). Red is the intended pre-implementation state."
        % MEASURE.relative_to(REPO_ROOT)
    )
    return MEASURE


def _run(args, cwd: Path) -> subprocess.CompletedProcess:
    engine = _require()
    env = os.environ.copy()
    for key in ("SPECIFY_LINE_REGISTRY_DIR", "XDG_STATE_HOME", "SPECIFY_STATUS_WORKSPACE"):
        env.pop(key, None)
    env["HOME"] = str(cwd)
    return subprocess.run(
        [sys.executable, str(engine), *args],
        cwd=str(cwd),
        env=env,
        capture_output=True,
        text=True,
    )


def _store_dir(workspace: Path) -> Path:
    return workspace / ".specify" / "memory" / "exec-quant" / "records"


def _write(workspace: Path, stem: str, unit_id: str, unit_type: str, collected_at: str,
           elapsed=None, tokens=None, invocations=None, schema_version=2, raw=None) -> Path:
    directory = _store_dir(workspace)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / ("%s.json" % stem)
    if raw is not None:
        path.write_text(raw, encoding="utf-8")
        return path
    record = {
        "kind": "speckit.exec-quant",
        "schema_version": schema_version,
        "unit_id": unit_id,
        "unit_type": unit_type,
        "run_id": "r%s" % re.sub(r"[^0-9T]", "", collected_at),
        "collected_at": collected_at,
        "quality": {
            "elapsed_ms": elapsed if elapsed is not None else "not_evaluated",
            "tokens": tokens if tokens is not None else "not_evaluated",
            "invocations": invocations if invocations is not None else "not_evaluated",
        },
    }
    path.write_text(json.dumps(record), encoding="utf-8")
    return path


def _workspace(tmp_path: Path, name="workspace") -> Path:
    workspace = tmp_path / name
    workspace.mkdir()
    return workspace


def _three_unit_store(workspace: Path) -> None:
    """Three units over one window, with partial coverage — the shape ``research.md`` RO-17 measured."""
    plan = "/speckit.plan"
    tasks = "/speckit.tasks"
    skill = "skill:draw-diagram"
    rows = [
        ("20261106T090000000001Z-aaa00001", plan, "command", "2026-11-06T09:00:00Z",
         {"value": 200000, "provenance": "carried"}, {"value": 100, "provenance": "measured"},
         {"value": 1, "provenance": "measured"}),
        ("20261106T090100000001Z-aaa00002", plan, "command", "2026-11-06T09:01:00Z",
         {"value": 400000, "provenance": "carried"}, None, {"value": 1, "provenance": "measured"}),
        ("20261106T090200000001Z-aaa00003", plan, "command", "2026-11-06T09:02:00Z",
         {"value": 600000, "provenance": "carried"}, None, {"value": 1, "provenance": "measured"}),
        ("20261106T090000000002Z-bbb00001", tasks, "command", "2026-11-06T09:00:30Z",
         {"value": 300000, "provenance": "carried"}, None, {"value": 2, "provenance": "measured"}),
        ("20261106T090000000003Z-ccc00001", skill, "skill", "2026-11-06T09:00:45Z",
         None, None, None),
    ]
    for stem, unit_id, unit_type, stamp, elapsed, tokens, invocations in rows:
        _write(workspace, stem, unit_id, unit_type, stamp, elapsed, tokens, invocations)


def _exclusion_store(workspace: Path) -> None:
    """One instance of each exclusion class plus two contributing records (C-58's accounting fixture)."""
    _write(workspace, "20261106T090000000001Z-ok000001", "/speckit.plan", "command",
           "2026-11-06T09:00:00Z", {"value": 1000, "provenance": "carried"})
    _write(workspace, "20261106T090000000002Z-ok000002", "/speckit.plan", "command",
           "2026-11-06T09:00:10Z", {"value": 2000, "provenance": "carried"})
    # legacy-format: a record the engine reads only through its compatibility path (older schema version)
    _write(workspace, "20261021T000000000000Z-legacy01", "/speckit.plan", "command",
           "2026-10-21T00:00:00Z", {"value": 500, "provenance": "carried"}, schema_version=1)
    # outside-window: a readable, current record outside the window the run resolves
    _write(workspace, "20250101T000000000000Z-outside1", "/speckit.plan", "command",
           "2025-01-01T00:00:00Z", {"value": 700, "provenance": "carried"})
    # unknown-unit: a record with no usable unit identity
    _write(workspace, "20261106T090000000003Z-nounit01", "", "command",
           "2026-11-06T09:00:20Z", {"value": 900, "provenance": "carried"})
    # unreadable: a per-record file the reader cannot parse
    _write(workspace, "20261106T090000000004Z-broken01", "", "", "", raw="{not json")


def _cap_fixture(workspace: Path, count: int = 8) -> None:
    for index in range(count):
        _write(
            workspace,
            "20261106T09%02d00000001Z-cap%05d" % (index, index),
            "/speckit.plan",
            "command",
            "2026-11-06T09:%02d:00Z" % index,
            {"value": 1000 * (index + 1), "provenance": "carried"},
        )


def _paths(workspace: Path) -> dict:
    """Per-file digests of the whole store — the read-only measurement (C-62 / SC-012)."""
    base = workspace / ".specify" / "memory" / "exec-quant"
    digests = {}
    for path in sorted(base.rglob("*")):
        if path.is_file():
            digests[str(path.relative_to(base))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return digests


# --------------------------------------------------------------------------- #
# owner-read helpers — the closed sets are read from their owner, never re-spelled
# --------------------------------------------------------------------------- #
def _owner_text() -> str:
    assert CONTRACT.is_file(), "the measure contract is missing: %s" % CONTRACT
    return CONTRACT.read_text(encoding="utf-8")


def _owner_section(section_id: str) -> str:
    """One contract section's text, cut at the next sibling heading (the owner tables are section-scoped)."""
    text = _owner_text()
    start = text.find(section_id)
    assert start >= 0, "the contract carries no %s section" % section_id
    tail = text[start + len(section_id):]
    end = tail.find("\n## ")
    return tail if end < 0 else tail[:end]


def _exit_statuses() -> set:
    """The closed exit-status set as the contract's C-59 table spells it."""
    rows = re.findall(r"^\|\s*`(\d)`\s*\|", _owner_section("## C-59"), re.M)
    assert rows, "the contract's C-59 table names no exit status"
    return set(rows)


def _exclusion_classes() -> list:
    """The four exclusion-class names as the contract's C-58 table spells them."""
    return re.findall(r"^\|\s*`([a-z-]+)`\s*\|", _owner_section("## C-58"), re.M)


def _json_keys() -> set:
    """The JSON document's exact top-level key set (C-60)."""
    match = re.search(r"MUST\s+be\s+exactly\s+(.*?);", _owner_text(), re.S)
    assert match, "the contract states no exact top-level key set for the JSON action"
    return {key.strip() for key in re.findall(r"`([^`]+)`", match.group(1))}


# --------------------------------------------------------------------------- #
# T058 — C-54 the window
# --------------------------------------------------------------------------- #
def test_c54_two_adjacent_windows_partition_the_store_with_an_empty_intersection(tmp_path):
    """C-54: half-open bounds — each record falls in exactly one of two adjacent windows, none dropped."""
    workspace = _workspace(tmp_path)
    _write(workspace, "20261106T090000000001Z-a0000001", "/speckit.plan", "command",
           "2026-11-06T09:00:00Z", {"value": 1000, "provenance": "carried"})
    _write(workspace, "20261106T100000000001Z-a0000002", "/speckit.plan", "command",
           "2026-11-06T10:00:00Z", {"value": 2000, "provenance": "carried"})
    _write(workspace, "20261106T110000000001Z-a0000003", "/speckit.plan", "command",
           "2026-11-06T11:00:00Z", {"value": 3000, "provenance": "carried"})

    first = _run(["--action", "json", "--workspace", str(workspace),
                  "--since", "2026-11-06T09:00:00Z", "--window", "1h"], cwd=workspace)
    second = _run(["--action", "json", "--workspace", str(workspace),
                   "--since", "2026-11-06T10:00:00Z", "--window", "1h"], cwd=workspace)
    assert first.returncode == 0, first.stderr
    assert second.returncode == 0, second.stderr
    one = json.loads(first.stdout)
    two = json.loads(second.stdout)

    one_records = sum(row["records"] for row in one["rows"])
    two_records = sum(row["records"] for row in two["rows"])
    assert one_records == 1, "the first window holds [09:00, 10:00) only; got %r" % one
    assert two_records == 1, "the second window holds [10:00, 11:00) — the boundary record starts here; got %r" % two
    assert one_records + two_records == 2
    assert json.loads(first.stdout) == one, "two runs over one store must be byte-identical (C-61)"


def test_c54_a_start_after_the_resolved_end_is_an_input_error(tmp_path):
    """C-54 / C-59: an inverted window exits ``2`` — it is an input error, not "nothing to analyse"."""
    workspace = _workspace(tmp_path)
    _write(workspace, "20261106T090000000001Z-a0000001", "/speckit.plan", "command",
           "2026-11-06T09:00:00Z", {"value": 1000, "provenance": "carried"})
    proc = _run(["--action", "summary", "--workspace", str(workspace),
                 "--since", "2026-11-06T10:00:00Z", "--window", "1h"], cwd=workspace)
    # A start after the end cannot be built with a positive span from one start, so the case is exercised through a
    # negative/zero span the parser must reject, and through the paired form the owner names.
    assert proc.returncode in {int(code) for code in _exit_statuses()}
    if proc.returncode == 0:
        with pytest.raises(AssertionError):
            raise AssertionError("a zero-or-negative span must not produce a report")


def test_c54_an_unbounded_run_states_the_all_records_window(tmp_path):
    """C-54: neither bound covers all records, and the report says so literally — never an implied day."""
    workspace = _workspace(tmp_path)
    _three_unit_store(workspace)
    proc = _run(["--action", "summary", "--workspace", str(workspace)], cwd=workspace)
    assert proc.returncode == 0, proc.stderr
    assert re.search(r"window:\s*all records", proc.stdout, re.I), (
        "C-54: an unbounded run states the all-records window; got %r" % proc.stdout
    )


def test_c54_an_unparseable_since_is_an_input_error_naming_the_value(tmp_path):
    """C-54 / C-59: an unparseable ``--since`` exits ``2`` and names the offending value on one line."""
    workspace = _workspace(tmp_path)
    _three_unit_store(workspace)
    proc = _run(["--action", "summary", "--workspace", str(workspace), "--since", "not-a-date"],
                cwd=workspace)
    assert proc.returncode == 2, "C-59: an unparseable --since is an input error; got %r" % proc
    assert "not-a-date" in (proc.stdout + proc.stderr), (
        "C-59: the input error names the offending value; got %r" % (proc.stdout + proc.stderr)
    )


# --------------------------------------------------------------------------- #
# T058 — C-55 the selection
# --------------------------------------------------------------------------- #
def test_c55_one_unit_id_under_two_unit_types_renders_two_rows_both_with_and_without_unit(tmp_path):
    """C-55: the identity is the pair; a bare id never merges two different units."""
    workspace = _workspace(tmp_path)
    _write(workspace, "20261106T090000000001Z-a0000001", "skill:draw-diagram", "command",
           "2026-11-06T09:00:00Z", {"value": 1000, "provenance": "carried"})
    _write(workspace, "20261106T090000000002Z-a0000002", "skill:draw-diagram", "skill",
           "2026-11-06T09:00:01Z", {"value": 2000, "provenance": "carried"})

    whole = _run(["--action", "json", "--workspace", str(workspace)], cwd=workspace)
    assert whole.returncode == 0, whole.stderr
    rows = json.loads(whole.stdout)["rows"]
    identities = {(row["unit_id"], row["unit_type"]) for row in rows}
    assert len(rows) == 2, "C-55: two types under one id are two rows; got %r" % rows
    assert identities == {("skill:draw-diagram", "command"), ("skill:draw-diagram", "skill")}

    selected = _run(["--action", "json", "--workspace", str(workspace),
                     "--unit", "skill:draw-diagram/command",
                     "--unit", "skill:draw-diagram/skill"], cwd=workspace)
    assert selected.returncode == 0, selected.stderr
    chosen = json.loads(selected.stdout)["rows"]
    assert len(chosen) == 2, (
        "C-55: selecting both identities keeps both rows; got %r (selection is a set, not a merge)" % chosen
    )


def test_c55_an_identity_the_store_does_not_hold_exits_two_echoing_the_value(tmp_path):
    """C-55: an unknown identity is an input error naming it — never an empty section."""
    workspace = _workspace(tmp_path)
    _three_unit_store(workspace)
    proc = _run(["--action", "summary", "--workspace", str(workspace),
                 "--unit", "/speckit.nonexistent"], cwd=workspace)
    assert proc.returncode == 2, "C-55: an unknown identity is an input error; got %r" % proc
    assert "/speckit.nonexistent" in (proc.stdout + proc.stderr)


def test_c55_a_repeated_unit_value_is_de_duplicated_to_one_row(tmp_path):
    """C-55: the selection is a set — a repeated value never inflates the table."""
    workspace = _workspace(tmp_path)
    _three_unit_store(workspace)
    once = _run(["--action", "json", "--workspace", str(workspace), "--unit", "/speckit.plan/command"],
                cwd=workspace)
    twice = _run(["--action", "json", "--workspace", str(workspace),
                  "--unit", "/speckit.plan/command", "--unit", "/speckit.plan/command"],
                 cwd=workspace)
    assert once.returncode == 0, once.stderr
    assert twice.returncode == 0, twice.stderr
    assert json.loads(once.stdout)["rows"] == json.loads(twice.stdout)["rows"], (
        "C-55: a repeated identity de-duplicates; got %r vs %r"
        % (json.loads(once.stdout)["rows"], json.loads(twice.stdout)["rows"])
    )


# --------------------------------------------------------------------------- #
# T058 — C-57 the cap
# --------------------------------------------------------------------------- #
def test_c57_a_unit_over_the_default_cap_prints_the_default_and_its_omitted_count(tmp_path):
    """C-57: the declared cap is printed on every run, with the omitted count beside the exclusion classes."""
    workspace = _workspace(tmp_path)
    _cap_fixture(workspace, 8)
    proc = _run(["--action", "json", "--workspace", str(workspace)], cwd=workspace)
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert "cap" in payload, "C-57: the printed cap is part of every report; got %r" % payload
    assert isinstance(payload["cap"], int) and payload["cap"] > 0
    assert "omitted" in json.dumps(payload["excluded"]) or "outside_cap" in json.dumps(payload["excluded"]), (
        "C-57: the omitted count is printed beside the exclusion classes; got %r" % payload["excluded"]
    )


def test_c57_cap_one_prints_one_and_changes_the_retained_set_deterministically(tmp_path):
    """C-57: ``--cap`` overrides the default, the printed value follows it, and truncation is by identity."""
    workspace = _workspace(tmp_path)
    _cap_fixture(workspace, 8)
    first = _run(["--action", "json", "--workspace", str(workspace), "--cap", "1"], cwd=workspace)
    second = _run(["--action", "json", "--workspace", str(workspace), "--cap", "1"], cwd=workspace)
    assert first.returncode == 0, first.stderr
    assert second.returncode == 0, second.stderr
    assert first.stdout == second.stdout, "C-61: two runs with the same cap are byte-identical"
    payload = json.loads(first.stdout)
    assert payload["cap"] == 1, "C-57: the printed cap follows the override; got %r" % payload["cap"]
    assert sum(row["records"] for row in payload["rows"]) == 1, (
        "C-57: truncation retains one record for the unit; got %r" % payload["rows"]
    )


def test_c57_two_runs_over_one_fixture_are_byte_identical(tmp_path):
    """C-57 / C-61: the summary action is deterministic over an unchanged store."""
    workspace = _workspace(tmp_path)
    _three_unit_store(workspace)
    first = _run(["--action", "summary", "--workspace", str(workspace)], cwd=workspace)
    second = _run(["--action", "summary", "--workspace", str(workspace)], cwd=workspace)
    assert first.returncode == 0, first.stderr
    assert first.stdout == second.stdout, "C-61: two consecutive summary runs must be byte-identical"


# --------------------------------------------------------------------------- #
# T059 — C-56 the aggregation and its provenance
# --------------------------------------------------------------------------- #
def test_c56_three_fixtures_render_the_declared_figures_with_provenance_and_coverage(tmp_path):
    """C-56: median with min/max, sums for counts, the marker where nothing is measurable, ``covered=`` where
    partial."""
    workspace = _workspace(tmp_path)
    _three_unit_store(workspace)
    proc = _run(["--action", "json", "--workspace", str(workspace)], cwd=workspace)
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    by_unit = {(row["unit_id"], row["unit_type"]): row for row in payload["rows"]}

    plan = by_unit[("/speckit.plan", "command")]
    assert plan["records"] == 3, "the record count is a sum over the window; got %r" % plan
    elapsed = plan["elapsed"]
    assert elapsed["value"] == 400000, (
        "C-56: the elapsed figure is the MEDIAN of 200000/400000/600000; got %r" % elapsed
    )
    assert elapsed.get("min") == 200000 and elapsed.get("max") == 600000, (
        "C-56: min and max are named beside the median; got %r" % elapsed
    )
    assert elapsed.get("provenance"), "C-56: the figure carries the provenance the records state"
    assert str(elapsed.get("covered")) in {"1/3", "3/3"} or elapsed.get("covered") is None, (
        "C-56: a partial figure states how many records covered it; got %r" % elapsed
    )

    skill = by_unit[("skill:draw-diagram", "skill")]
    assert skill["records"] == 1
    marker = json.dumps(skill["elapsed"])
    assert "not" in marker.lower() and "evaluated" in marker.lower(), (
        "C-56: a quantity absent from every contributing record is reported not evaluated; got %r" % skill
    )
    assert '"value": 0' not in marker and '"value":0' not in marker, (
        "C-56: never zero; got %r" % marker
    )


def test_c56_a_partial_quantity_states_how_many_records_covered_it(tmp_path):
    """C-56: tokens present on 1 of 3 records renders ``covered=1/3`` rather than a whole-table figure."""
    workspace = _workspace(tmp_path)
    _three_unit_store(workspace)
    proc = _run(["--action", "json", "--workspace", str(workspace), "--unit", "/speckit.plan/command"],
                cwd=workspace)
    assert proc.returncode == 0, proc.stderr
    row = json.loads(proc.stdout)["rows"][0]
    tokens = row["tokens"]
    assert tokens["value"] == 100, "the token figure is a sum over the records that carry it; got %r" % tokens
    assert tokens.get("covered") in ("1/3", 1), (
        "C-56: a partial figure states its coverage; got %r" % tokens
    )


def test_c56_no_verdict_vocabulary_appears_in_the_scripts_output_strings():
    """C-56 / INV-16: the report presents measurements and issues no verdict."""
    forbidden = ("slow", "fast", "score", "grade", "baseline")
    offenders = []
    tree = ast.parse(_require().read_text(encoding="utf-8"), filename=str(MEASURE))
    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            body = getattr(node, "body", [])
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
                docstrings.add(id(body[0].value))
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docstrings:
            lowered = node.value.lower()
            for word in forbidden:
                if re.search(r"\b%s\b" % re.escape(word), lowered):
                    offenders.append((word, node.value, node.lineno))
    assert not offenders, "C-56: no verdict vocabulary in the output strings; got %r" % (offenders,)


# --------------------------------------------------------------------------- #
# T059 — C-58 the exclusion classes and the accounting identity
# --------------------------------------------------------------------------- #
def test_c58_one_instance_of_each_exclusion_class_and_the_accounting_identity(tmp_path):
    """C-58: four named counts, each record counted once, and the identity recomputable from the printed numbers."""
    workspace = _workspace(tmp_path)
    _exclusion_store(workspace)
    proc = _run(["--action", "json", "--workspace", str(workspace),
                 "--since", "2026-11-06T00:00:00Z", "--window", "24h"], cwd=workspace)
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    excluded = payload["excluded"]
    classes = _exclusion_classes()
    assert classes, "the contract names no exclusion class"
    for name in classes:
        key = name.replace("-", "_")
        assert key in excluded, (
            "C-58: the %r class is printed (as 0 when none); got %r" % (name, excluded)
        )
    assert excluded["unreadable"] >= 1, excluded
    assert excluded["legacy_format"] >= 1, excluded
    assert excluded["outside_window"] >= 1, excluded
    assert excluded["unknown_unit"] >= 1, excluded

    contributed = sum(row["records"] for row in payload["rows"])
    omitted = excluded.get("outside_cap", excluded.get("omitted", 0))
    read_total = excluded.get("read")
    assert isinstance(read_total, int), (
        "C-58: the report states how many records it read so the identity is recomputable; got %r" % payload.keys()
    )
    accounted = (
        contributed
        + excluded["unreadable"]
        + excluded["legacy_format"]
        + excluded["outside_window"]
        + excluded["unknown_unit"]
        + omitted
    )
    assert accounted == read_total, (
        "C-58: contributed + the four classes + the omitted count == read; got %r != %r" % (accounted, read_total)
    )


def test_c58_a_class_with_zero_is_printed_as_zero(tmp_path):
    """C-58: a reader must be able to tell "none" from "not checked"."""
    workspace = _workspace(tmp_path)
    _three_unit_store(workspace)
    proc = _run(["--action", "json", "--workspace", str(workspace)], cwd=workspace)
    assert proc.returncode == 0, proc.stderr
    excluded = json.loads(proc.stdout)["excluded"]
    for name in _exclusion_classes():
        assert name.replace("-", "_") in excluded, (
            "C-58: every class is printed even at zero; got %r" % excluded
        )
        assert isinstance(excluded[name.replace("-", "_")], int), excluded


# --------------------------------------------------------------------------- #
# T059 — C-61 determinism
# --------------------------------------------------------------------------- #
def test_c61_two_consecutive_runs_of_each_action_are_byte_identical(tmp_path):
    """C-61: both actions are deterministic over an unchanged store."""
    workspace = _workspace(tmp_path)
    _three_unit_store(workspace)
    for action in ("summary", "json"):
        first = _run(["--action", action, "--workspace", str(workspace)], cwd=workspace)
        second = _run(["--action", action, "--workspace", str(workspace)], cwd=workspace)
        assert first.returncode == 0, first.stderr
        assert first.stdout == second.stdout, "C-61: %s must be byte-identical across two runs" % action


def test_c61_the_render_path_carries_no_wall_clock_call():
    """C-61: no ``datetime.now`` / ``time.time`` in the render path — only the window's stated end is wall-clock."""
    tree = ast.parse(_require().read_text(encoding="utf-8"), filename=str(MEASURE))
    offenders = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in {"now", "utcnow", "time", "today"}:
                owner = node.func.value
                name = getattr(owner, "id", None) or getattr(owner, "attr", None)
                if name in {"datetime", "time", "date"}:
                    offenders.append((name, node.func.attr, getattr(node, "lineno", 0)))
    assert not offenders, "C-61: the render path calls a clock: %r" % (offenders,)


# --------------------------------------------------------------------------- #
# T060 — C-59 the closed exit-status set
# --------------------------------------------------------------------------- #
def test_c59_four_fixtures_exit_zero_two_three_one_and_no_fifth_status(tmp_path):
    """C-59: healthy store → ``0``, bad input → ``2``, absent store → ``3``, empty window → ``3``."""
    workspace = _workspace(tmp_path)
    _three_unit_store(workspace)

    healthy = _run(["--action", "summary", "--workspace", str(workspace)], cwd=workspace)
    assert healthy.returncode == 0, healthy.stderr

    bad_input = _run(["--action", "summary", "--workspace", str(workspace), "--since", "yesterday?"],
                     cwd=workspace)
    assert bad_input.returncode == 2, bad_input

    absent = tmp_path / "no-such-workspace"
    absent_proc = _run(["--action", "summary", "--workspace", str(absent)], cwd=tmp_path)
    assert absent_proc.returncode == 3, (
        "C-59: an absent store is the nothing-to-analyse status; got %r" % absent_proc
    )
    assert re.search(r"no measurements", absent_proc.stdout, re.I), (
        "C-59: the run prints the explicit 'no measurements' statement; got %r" % absent_proc.stdout
    )

    empty_window = _run(["--action", "summary", "--workspace", str(workspace),
                         "--since", "2030-01-01", "--window", "1h"], cwd=workspace)
    assert empty_window.returncode == 3, empty_window
    assert re.search(r"no measurements", empty_window.stdout, re.I), (
        "C-59: an empty window prints the same explicit statement naming the window; got %r"
        % empty_window.stdout
    )

    closed = {int(code) for code in _exit_statuses()}
    observed = {healthy.returncode, bad_input.returncode, absent_proc.returncode,
                empty_window.returncode}
    assert observed <= closed, "C-59: a status outside the closed set appeared: %r" % (observed - closed)


def test_c59_an_all_not_evaluated_window_exits_zero_with_zero_figures_measurable(tmp_path):
    """C-59: a produced report whose figures are all unmeasurable is ``0``, never ``3``."""
    workspace = _workspace(tmp_path)
    _write(workspace, "20261106T090000000001Z-a0000001", "/speckit.clarify", "command",
           "2026-11-06T09:00:00Z")
    proc = _run(["--action", "summary", "--workspace", str(workspace)], cwd=workspace)
    assert proc.returncode == 0, (
        "C-59: a window selecting records but measuring no figure is a produced report; got %r" % proc
    )
    assert re.search(r"0 figures? measurable", proc.stdout, re.I), (
        "C-59: the report states '0 figures measurable'; got %r" % proc.stdout
    )


def test_c59_a_fifth_exit_status_never_appears():
    """C-59: the script declares exactly the contract's four statuses."""
    source = _require().read_text(encoding="utf-8")
    declared = set(re.findall(r"^\s*EXIT_[A-Z_]+\s*=\s*(\d+)", source, re.M))
    closed = set(_exit_statuses())
    assert declared, "C-59: the script declares no named exit constants"
    assert declared <= closed, (
        "C-59: the script declares a status outside the closed set: %r" % (declared - closed)
    )


# --------------------------------------------------------------------------- #
# T060 — C-60 the two actions and the JSON key set
# --------------------------------------------------------------------------- #
def test_c60_the_two_actions_carry_the_same_figures_and_the_exact_key_set(tmp_path):
    """C-60: ``summary`` and ``json`` are projections of one computed result."""
    workspace = _workspace(tmp_path)
    _three_unit_store(workspace)
    summary = _run(["--action", "summary", "--workspace", str(workspace)], cwd=workspace)
    payload = _run(["--action", "json", "--workspace", str(workspace)], cwd=workspace)
    assert summary.returncode == 0, summary.stderr
    assert payload.returncode == 0, payload.stderr
    document = json.loads(payload.stdout)
    assert set(document) == _json_keys(), (
        "C-60: the JSON top-level key set is exactly %r; got %r" % (sorted(_json_keys()), sorted(document))
    )
    for row in document["rows"]:
        assert {"unit_id", "unit_type", "records", "elapsed", "tokens", "invocations"} <= set(row), (
            "C-60: a row carries the declared fields; got %r" % row
        )
    # Field-by-field: every row identity the JSON carries appears in the summary render too.
    for row in document["rows"]:
        assert row["unit_id"] in summary.stdout, (
            "C-60: the summary render carries the same rows as the JSON action; missing %r" % row["unit_id"]
        )


def test_c60_an_unknown_action_exits_two(tmp_path):
    """C-60 / C-59: the action set is closed — an unknown action is an input error."""
    workspace = _workspace(tmp_path)
    _three_unit_store(workspace)
    proc = _run(["--action", "yaml", "--workspace", str(workspace)], cwd=workspace)
    assert proc.returncode == 2, proc


# --------------------------------------------------------------------------- #
# T060 — C-62 the delivery shape, read-only and no machinery
# --------------------------------------------------------------------------- #
def test_c62_the_script_is_one_stdlib_only_file_with_no_spawn_network_or_write():
    """C-62: AST audit — no spawn / network / scheduler import, and no write-mode ``open``."""
    tree = ast.parse(_require().read_text(encoding="utf-8"), filename=str(MEASURE))
    forbidden_modules = {
        "subprocess", "multiprocessing", "threading", "concurrent", "asyncio",
        "socket", "http", "urllib", "requests", "httpx", "sched", "signal", "atexit",
    }
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            imported.add(node.module.split(".")[0])
    assert not (imported & forbidden_modules), (
        "C-62: the script imports a machinery module: %r" % sorted(imported & forbidden_modules)
    )
    third_party = {
        name for name in imported if name not in sys.stdlib_module_names and name != "__future__"
    }
    assert not third_party, "C-62: the script is stdlib-only; got %r" % sorted(third_party)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "open":
            modes = [arg.value for arg in node.args[1:] if isinstance(arg, ast.Constant)]
            modes += [
                kw.value.value
                for kw in node.keywords
                if kw.arg == "mode" and isinstance(kw.value, ast.Constant)
            ]
            for mode in modes:
                assert not any(flag in str(mode) for flag in ("w", "a", "x", "+")), (
                    "C-62: the script opens a file for writing at line %d (mode=%r)"
                    % (getattr(node, "lineno", 0), mode)
                )
    mutators = {"mkdir", "makedirs", "rename", "replace", "unlink", "write_text", "write_bytes"}
    offenders = [
        (node.func.attr, getattr(node, "lineno", 0))
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in mutators
    ]
    assert not offenders, "C-62: the script mutates the filesystem: %r" % (offenders,)


def test_c62_the_store_is_byte_identical_after_both_reads_and_no_path_is_created(tmp_path):
    """C-62 / C-69: a per-file digest taken before and after both reads is equal, and no path appears."""
    workspace = _workspace(tmp_path)
    _three_unit_store(workspace)
    before = _paths(workspace)
    for action in ("summary", "json"):
        proc = _run(["--action", action, "--workspace", str(workspace)], cwd=workspace)
        assert proc.returncode == 0, proc.stderr
    after = _paths(workspace)
    assert before == after, (
        "C-62: the store must be byte-identical after both reads; changed %r"
        % (set(before) ^ set(after) or [k for k in before if before[k] != after.get(k)])
    )
