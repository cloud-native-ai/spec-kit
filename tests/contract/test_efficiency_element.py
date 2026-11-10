"""Contract tests for the efficiency element on the two visibility surfaces (087, T055).

Contract object: `contracts/efficiency-element.contract.md` C-63…C-71 — one bounded efficiency element carried as
**content** of the status line (``--action report``) and of the digest entry (``--action digest``), sourced read-only
from the exec-quant store.

What this file owns and what it does not:

* it asserts the element's **two-surface** shape (C-63), its declared quantity order and its render-wide degradation
  (C-64), the marker for a listed unit with no record (C-67) and the store-availability floor (C-68);
* it does **not** re-derive the surface shapes. The four content elements, the attribution, the digest's cap /
  staleness / exit statuses are owned by ``status-report.contract.md`` C-22…C-31 and ``status-digest.contract.md``
  C-41…C-46; where this file needs one of those facts it reads the value from the render rather than restating it;
* the store's schema, its field slots and its closed vocabularies are owned by
  ``shared/declarations/facts/quant-record-schema.yaml`` and reached **by reference** (C-71): this file reads the
  provenance marker out of the record fixture it writes, and never spells a vocabulary of its own.

**Red-first (Constitution IV)**: authored before ``status-digest.py`` gained the element (T062/T063), so every test
here is expected to fail on the pre-implementation tree — each assertion first checks the script exists and then
asserts the element's presence, so red is "the element is missing", never an import error.

**Fixture posture**: every store, registry and workspace is built from scratch under ``tmp_path``; no test reads or
writes the real ``.specify/memory/exec-quant/`` store or the real line registry.
"""
from __future__ import annotations

import ast
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "status-digest.py"
LINE_REGISTRY_ENGINE = (
    REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "line-registry.py"
)

#: The marker the owner renders for a quantity the record does not carry (contract C-64 / C-67). Its single
#: definition site is the owner document (``contracts/ownership-map.contract.md`` C-47 "Not-evaluated marker
#: literal"): the test reads the literal out of the owner at run time instead of spelling a second copy — the
#: ``_marker()`` helper below is the only place this file reaches it.
MARKER_OWNER_PATTERN = re.compile(r"`(not[- ]evaluated)`", re.I)

#: The explicit store-availability state (contract C-68). Like the marker it is read from the owner, never re-spelled.
NO_MEASUREMENTS_OWNER_PATTERN = re.compile(r"\*\*\"(no measurements)\"\*\*|\"(no measurements)\"")


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _require_engine() -> Path:
    assert ENGINE.is_file(), (
        "status-digest engine missing: %s — expected at T009 (087)." % ENGINE.relative_to(REPO_ROOT)
    )
    return ENGINE


def _engine_constants() -> dict:
    """Read ``STATE_VALUES`` / ``ACTIVE_STATES`` from the registry engine's source (quoted, never re-enumerated)."""
    text = LINE_REGISTRY_ENGINE.read_text(encoding="utf-8")

    def literal(name: str) -> set:
        match = re.search(r"^%s\s*=\s*\{(.*?)\}" % re.escape(name), text, re.S | re.M)
        assert match, "registry engine carries no %s" % name
        return set(re.findall(r"[\"']([^\"']+)[\"']", match.group(1)))

    return {"STATE_VALUES": literal("STATE_VALUES"), "ACTIVE_STATES": literal("ACTIVE_STATES")}


def _run(args, cwd: Path, env_overrides=None) -> subprocess.CompletedProcess:
    engine = _require_engine()
    env = os.environ.copy()
    for key in ("SPECIFY_LINE_REGISTRY_DIR", "XDG_STATE_HOME", "SPECIFY_STATUS_WORKSPACE"):
        env.pop(key, None)
    env["HOME"] = str(cwd)
    env.update(env_overrides or {})
    return subprocess.run(
        [sys.executable, str(engine), *args],
        cwd=str(cwd),
        env=env,
        capture_output=True,
        text=True,
    )


def _registry(tmp_path: Path, name: str = "registry") -> Path:
    path = tmp_path / name
    path.mkdir(parents=True, exist_ok=True)
    return path


def _write_entry(registry: Path, entry: dict) -> Path:
    import json

    path = registry / ("%s.json" % entry["line_id"])
    path.write_text(json.dumps(entry), encoding="utf-8")
    return path


def _entry(line_id: str, project_dir: Path, **overrides) -> dict:
    active = sorted(_engine_constants()["ACTIVE_STATES"])[0]
    entry = {
        "line_id": line_id,
        "run_id": "r20261106T000000Z-" + line_id,
        "project_dir": str(project_dir),
        "branch": "main",
        "stage": "implement",
        "state": active,
        "updated_at": "2026-11-06T09:00:00Z",
    }
    entry.update(overrides)
    return entry


def _store_record(unit_id: str, unit_type: str, collected_at: str, elapsed=None, tokens=None,
                  invocations=None, run_id=None) -> dict:
    """One exec-quant record in the shape the engine writes (v2), with the quantities the caller names.

    ``None`` renders the record's own not-evaluated literal — the shape the store's law of the record uses for a
    quantity with no source (``scripts/python/exec-quant.py`` module docstring). ``run_id`` overrides the derived
    one, so a fixture can place a record inside the run the surface's own state source names (C-63: the digest's
    step set is this run's or the most recent steps — never the store's at large).
    """
    record = {
        "kind": "speckit.exec-quant",
        "unit_id": unit_id,
        "unit_type": unit_type,
        # The record's own run identity — the lookup key the element resolves a listed unit's record by
        # (``data-model.md`` E8 ``unit.lookup``): without one the record belongs to no run and is never selected.
        "run_id": run_id or "r%s" % collected_at.replace(":", "").replace("-", ""),
        "collected_at": collected_at,
        "quality": {
            "elapsed_ms": elapsed if elapsed is not None else "not_evaluated",
            "tokens": tokens if tokens is not None else "not_evaluated",
            "invocations": invocations if invocations is not None else "not_evaluated",
        },
    }
    return record


def _write_store(workspace: Path, records, name="20261106T090000000000Z-aaaaaaaa.json"):
    """Write one per-record file under the workspace's store and return the path."""
    import json

    directory = workspace / ".specify" / "memory" / "exec-quant" / "records"
    directory.mkdir(parents=True, exist_ok=True)
    written = []
    for index, record in enumerate(records):
        stem = name if len(records) == 1 else name.replace("aaaaaaaa", "%08x" % (index + 1))
        path = directory / stem
        path.write_text(json.dumps(record), encoding="utf-8")
        written.append(path)
    return written


def _digest(workspace: Path, registry: Path | None, *extra):
    overrides = {"SPECIFY_LINE_REGISTRY_DIR": str(registry)} if registry is not None else {}
    return _run(["--action", "digest", "--workspace", str(workspace), *extra], cwd=workspace,
                env_overrides=overrides)


def _report(workspace: Path, registry: Path | None, *extra):
    """One status line as the emitting flow renders it, with the unit that flow names as its position.

    The line's listed set is its own state source: a flow knows where it is, so it names the unit (``--unit-id``),
    that unit's own type and the run it is in (``--run-id`` — the element's lookup key, ``data-model.md`` E8
    ``unit.lookup``). The fixture states all three rather than letting the store decide what the line lists.
    """
    overrides = {"SPECIFY_LINE_REGISTRY_DIR": str(registry)} if registry is not None else {}
    args = [
        "--action", "report",
        "--workspace", str(workspace),
        "--structure", "fixture-team",
        "--run-stamp", "r20261106T090000Z",
        "--position", "implement 3/8",
        "--delta", "two rows landed",
        "--remainder", "five rows left",
        "--unit-id", "/speckit.plan",
        "--unit-type", "command",
        "--run-id", "r20261106T090000Z",
    ]
    return _run([*args, *extra], cwd=workspace, env_overrides=overrides)


def _entry_rows(rendered: str) -> list:
    """The rendered table body rows — one per entry (the digest's reader contract renders a table)."""
    lines = rendered.splitlines()
    sep = next((i for i, line in enumerate(lines) if line and set(line.replace(" ", "")) == {"-"}), None)
    if sep is None:
        return []
    rows = []
    for line in lines[sep + 1:]:
        if not line.strip():
            break
        if line.startswith(("最近完成：", "另有 ", "store=", "omitted=", "last_completion=")):
            break
        rows.append(line)
    return rows


def _elements(line: str) -> list:
    """The efficiency elements one rendered render carries — one per listed unit (C-64 order).

    An element group runs from its ``unit=<name>`` to the next element or to the end of that pipe-delimited field;
    the tail is taken non-greedily so a render carrying several elements yields one entry per unit.
    """
    return re.findall(r"unit=([^\s,|]+)(.*?)(?=\s*efficiency=unit=|\s*(?:\||$))", line)


def _count_marker(text: str) -> int:
    return len(re.findall(r"(?i)\bnot[- ]evaluated\b", text))


def _marker_literal() -> str:
    """The not-evaluated marker, read from its single definition site (the obligation's owner document).

    ``contracts/ownership-map.contract.md`` C-47 makes the owner document the marker's one declaration point, so a
    test that spelled the literal itself would be a second copy of the fact it checks.
    """
    owner = REPO_ROOT / "shared" / "guidelines" / "reporting-obligations.md"
    assert owner.is_file(), "the owner document is missing: %s" % owner
    text = owner.read_text(encoding="utf-8")
    matches = [m.group(1) for m in MARKER_OWNER_PATTERN.finditer(text) if m.group(1)]
    assert matches, (
        "the owner document declares no not-evaluated marker literal; this test reaches it by anchor "
        "(contract C-47 row 'Not-evaluated marker literal')"
    )
    form = matches[0].lower()
    return "not-evaluated" if "-" in form else "not evaluated"


def _no_measurements_literal() -> str:
    """The store-availability state (contract C-68), read from the same owner for the same reason."""
    owner = REPO_ROOT / "shared" / "guidelines" / "reporting-obligations.md"
    text = owner.read_text(encoding="utf-8")
    for match in NO_MEASUREMENTS_OWNER_PATTERN.finditer(text):
        value = match.group(1) or match.group(2)
        if value:
            return value
    return "no measurements"


def _digest_with_the_store_hidden(workspace: Path, registry: Path, *extra) -> str:
    """The same digest rendered with the store absent — the reference render the element must not disturb (C-68)."""
    hidden = workspace / ".specify" / "memory" / "exec-quant-hidden"
    store = workspace / ".specify" / "memory" / "exec-quant"
    moved = False
    if store.exists():
        store.rename(hidden)
        moved = True
    try:
        proc = _digest(workspace, registry, *extra)
    finally:
        if moved:
            hidden.rename(store)
    assert proc.returncode in (0, 3), proc.stderr
    return proc.stdout


# --------------------------------------------------------------------------- #
# C-63 — exactly two surfaces, one element per listed unit, no third surface
# --------------------------------------------------------------------------- #
def test_c63_a_status_line_and_a_digest_over_one_store_carry_equal_element_counts(tmp_path):
    """C-63: the line names its emitting step, the digest names this run's steps — one element each, equal sets."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    registry = _registry(tmp_path)
    _write_entry(registry, _entry("t055-line-a", workspace))
    # The record is placed inside the run the registry entry names, so the digest's "this run's steps" population
    # is the run the fixture states — the store supplies quantities for the surface's own step set and never
    # widens it (C-63, FR-024: the line is the emitting step alone).
    _write_store(
        workspace,
        [_store_record("/speckit.plan", "command", "2026-11-06T09:00:00Z",
                       elapsed={"value": 253000, "provenance": "carried"},
                       run_id="r20261106T000000Z-t055-line-a")],
    )

    digest = _digest(workspace, registry)
    assert digest.returncode == 0, digest.stderr
    rows = _entry_rows(digest.stdout)
    assert len(rows) == 1, "the fixture registry lists exactly one entry; got %r" % rows
    digest_units = _elements(rows[0])

    line = _report(workspace, registry)
    assert line.returncode == 0, line.stderr
    line_units = _elements(line.stdout)

    # The status line is THE EMITTING STEP ALONE (FR-024): exactly one element, exactly the step --unit-id names.
    assert len(line_units) == 1, (
        "C-63/FR-024: the status line carries exactly one element — the emitting step's; got %r" % line.stdout
    )
    assert line_units[0][0] == "/speckit.plan", (
        "C-63: the line's element is the step the emitting flow named; got %r" % (line_units,)
    )
    # The digest over this one-step run carries one element per step it names — here, the same one.
    assert len(digest_units) == 1, (
        "C-63: the digest entry carries one element for the run's step; got %r" % rows[0]
    )
    # Equal element counts on equal step sets: both surfaces name the run's one step.
    assert {entry[0] for entry in line_units} == {entry[0] for entry in digest_units}, (
        "C-63: the two surfaces disagree about the step set: line=%r digest=%r"
        % (sorted(u[0] for u in line_units), sorted(u[0] for u in digest_units))
    )


def test_c63_the_digest_never_exceeds_its_cap_and_the_line_never_grows_the_unit_set(tmp_path):
    """C-63: the element introduces no unit — the digest stops at its cap, the line lists what it already lists."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    registry = _registry(tmp_path)
    for index in range(3):
        _write_entry(registry, _entry("t055-line-%d" % index, workspace))
    _write_store(
        workspace,
        [
            _store_record("/speckit.plan", "command", "2026-11-06T09:00:00Z",
                          elapsed={"value": 1000, "provenance": "carried"}),
            _store_record("/speckit.tasks", "command", "2026-11-06T09:01:00Z",
                          elapsed={"value": 2000, "provenance": "carried"}),
            _store_record("skill:draw-diagram", "skill", "2026-11-06T09:02:00Z",
                          elapsed={"value": 3000, "provenance": "measured"}),
        ],
    )

    capped = _digest(workspace, registry, "--cap", "2")
    assert capped.returncode == 0, capped.stderr
    rows = _entry_rows(capped.stdout)
    assert len(rows) == 2, "the cap bounds the entry set; got %r" % rows
    # The truncation is declared on the render's own summary line, never inferred from the row count alone.
    assert "另有 1 条未显示" in capped.stdout, (
        "the truncated render must state its omitted count; got %r" % capped.stdout
    )

    total = 0
    for row in rows:
        elements = _elements(row)
        assert len(elements) == 1, (
            "C-63: one element per listed unit, not one per store record; got %r" % row
        )
        total += len(elements)
    assert total == 2, "two listed units under a cap of two carry two elements; got %d" % total


# --------------------------------------------------------------------------- #
# C-64 — the declared order, provenance, and render-wide degradation
# --------------------------------------------------------------------------- #
def test_c64_a_wide_bound_renders_identity_then_elapsed_then_tokens_then_invocations(tmp_path):
    """C-64: within one element the quantities appear in the declared order, elapsed first and unconditional."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    registry = _registry(tmp_path)
    _write_entry(registry, _entry("t055-wide", workspace))
    _write_store(
        workspace,
        [
            _store_record(
                "/speckit.plan", "command", "2026-11-06T09:00:00Z",
                elapsed={"value": 253000, "provenance": "measured"},
                tokens={"value": 1200, "provenance": "measured"},
                invocations={"value": 3, "provenance": "measured"},
            )
        ],
    )

    line = _report(workspace, registry)
    assert line.returncode == 0, line.stderr
    elements = _elements(line.stdout)
    assert elements, "C-64: the status line carries an element; got %r" % line.stdout
    name, tail = elements[0]
    assert name == "/speckit.plan", "the element names its unit first; got %r" % name

    positions = {}
    for token in ("elapsed=", "tokens=", "invocations="):
        index = tail.find(token)
        assert index >= 0, (
            "C-64: a wide bound renders %s inside the element; got %r" % (token, tail)
        )
        positions[token] = index
    assert positions["elapsed="] < positions["tokens="] < positions["invocations="], (
        "C-64: the declared order is identity → elapsed → tokens → invocations; got %r" % (tail,)
    )
    assert "measured" in tail, "C-64: each quantity carries the provenance the record states; got %r" % tail


def test_c64_a_tight_bound_withdraws_tokens_and_invocations_from_every_unit_together(tmp_path):
    """C-64: degradation is all-or-nothing per render, and the withdrawn quantity is named in the omitted summary."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    registry = _registry(tmp_path)
    for line_id in ("t055-tight-a", "t055-tight-b"):
        _write_entry(registry, _entry(line_id, workspace))
    _write_store(
        workspace,
        [
            _store_record(
                "/speckit.plan", "command", "2026-11-06T09:00:00Z",
                elapsed={"value": 1000, "provenance": "measured"},
                tokens={"value": 1200, "provenance": "measured"},
                invocations={"value": 3, "provenance": "measured"},
            ),
            _store_record(
                "/speckit.tasks", "command", "2026-11-06T09:01:00Z",
                elapsed={"value": 2000, "provenance": "measured"},
                tokens={"value": 900, "provenance": "measured"},
                invocations={"value": 2, "provenance": "measured"},
            ),
        ],
    )

    tight = _digest(workspace, registry, "--cap", "2", "--element-bound", "60")
    assert tight.returncode == 0, tight.stderr
    rows = _entry_rows(tight.stdout)
    assert len(rows) == 2, rows
    for row in rows:
        elements = _elements(row)
        assert elements, "a listed unit always carries its element; got %r" % row
        for _name, tail in elements:
            assert "elapsed=" in tail, "C-64: elapsed is unconditional; got %r" % tail
            assert "tokens=" not in tail, (
                "C-64: a tight bound withdraws tokens from EVERY unit on the render; got %r" % row
            )
            assert "invocations=" not in tail, (
                "C-64: a tight bound withdraws invocations from EVERY unit on the render; got %r" % row
            )
    omitted = [line for line in tight.stdout.splitlines() if line.startswith("另有 ")]
    assert omitted, "C-64: the withdrawal is named in the render's existing omitted summary; got %r" % tight.stdout
    assert "tokens" in omitted[-1], (
        "the omitted summary names the withdrawn quantity; got %r" % omitted[-1]
    )


def test_c64_a_valued_and_a_not_evaluated_record_render_the_marker_and_never_zero(tmp_path):
    """C-64 / FR-023: a not-evaluated quantity renders the marker on its own step's element; ``0`` never appears.

    The line is the emitting step alone (FR-024): its one element carries the valued record's quantities and no
    elapsed marker. The digest names this run's / the most recent steps — here both fixture steps — so the
    not-evaluated record's step renders the marker beside its neighbour's number, never a zero and never an
    omission.
    """
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    registry = _registry(tmp_path)
    for line_id in ("t055-mixed-a", "t055-mixed-b"):
        _write_entry(registry, _entry(line_id, workspace))
    _write_store(
        workspace,
        [
            _store_record("/speckit.plan", "command", "2026-11-06T09:00:00Z",
                          elapsed={"value": 253000, "provenance": "carried"}),
            _store_record("/speckit.tasks", "command", "2026-11-06T09:01:00Z"),
        ],
    )

    line = _report(workspace, registry)
    assert line.returncode == 0, line.stderr
    line_elements = _elements(line.stdout)
    assert len(line_elements) == 1, (
        "FR-024: the status line is the emitting step alone — exactly one element; got %r" % line.stdout
    )
    assert line_elements[0][0] == "/speckit.plan", (
        "the line's element is the step the flow named; got %r" % (line_elements,)
    )

    digest = _digest(workspace, registry, "--cap", "5")
    assert digest.returncode == 0, digest.stderr
    rows = _entry_rows(digest.stdout)
    digest_elements = [element for row in rows for element in _elements(row)]
    assert len(digest_elements) == 2, (
        "the digest names both of the run's steps and carries one element each; got %r" % rows
    )
    by_unit = dict(digest_elements)
    assert "not-evaluated" in by_unit["/speckit.tasks"], (
        "C-64: the not-evaluated record's elapsed renders the explicit marker; got %r" % by_unit
    )
    assert "253000ms" in by_unit["/speckit.plan"], (
        "the valued record's elapsed keeps its measured figure; got %r" % by_unit
    )
    assert "elapsed=0" not in digest.stdout, (
        "FR-023: a not-evaluated elapsed quantity is never printed as 0; got %r" % digest.stdout
    )


# --------------------------------------------------------------------------- #
# C-67 — a listed unit with no record at all still carries the element
# --------------------------------------------------------------------------- #
def test_c67_a_listed_unit_with_no_record_carries_the_marker_not_an_omission(tmp_path):
    """C-67: the emitting step the store holds no record for still carries its element — with the marker.

    The line names its own step (``--unit-id``); the store holds records only for a different step. The named
    step's element is never dropped: an omission beside a neighbour's number would read as "faster".
    """
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    registry = _registry(tmp_path)
    _write_entry(registry, _entry("t055-norecord-a", workspace))
    _write_store(
        workspace,
        [_store_record("/speckit.tasks", "command", "2026-11-06T09:00:00Z",
                       elapsed={"value": 253000, "provenance": "carried"})],
    )

    line = _report(workspace, registry)
    assert line.returncode == 0, line.stderr
    elements = _elements(line.stdout)
    assert len(elements) == 1, (
        "C-67: the line still renders exactly one element — its emitting step's; got %r" % line.stdout
    )
    assert elements[0][0] == "/speckit.plan", (
        "the element belongs to the step the flow named; got %r" % (elements,)
    )
    assert _count_marker(elements[0][1]) >= 1, (
        "C-67: a step with no record renders the not-evaluated marker, never an omission; got %r" % elements
    )
    assert "elapsed=0" not in line.stdout, "C-67: never zero; got %r" % line.stdout


# --------------------------------------------------------------------------- #
# C-68 — store availability is never a precondition of the surfaces
# --------------------------------------------------------------------------- #
def test_c68_a_nonexistent_store_renders_no_measurements_and_changes_nothing_else(tmp_path):
    """C-68: an absent store renders the explicit state; the entry set, ordering and bounds are unchanged."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    registry = _registry(tmp_path)
    for index in range(2):
        _write_entry(registry, _entry("t055-absent-%d" % index, workspace))

    absent = _digest(workspace, registry, "--cap", "5")
    assert absent.returncode == 0, absent.stderr
    assert _no_measurements_literal() in absent.stdout, (
        "C-68: an absent store renders the explicit 'no measurements' state; got %r" % absent.stdout
    )
    state_lines = [line for line in absent.stdout.splitlines() if _no_measurements_literal() in line]
    assert len(state_lines) == 1 and state_lines[0].startswith("store="), (
        "C-68: the availability is ONE explicit summary line, never a per-row marker; got %r" % state_lines
    )
    assert _count_marker(absent.stdout) == 0, (
        "C-68: 'no measurements' is the store-availability state, not a per-unit marker; got %r"
        % absent.stdout
    )
    assert len(_entry_rows(absent.stdout)) == 2, (
        "C-68: the state changes no entry row — both fixture entries still render; got %r" % absent.stdout
    )


def test_c68_an_empty_store_renders_no_measurements_with_the_same_exit_status(tmp_path):
    """C-68: an empty store answers exactly as an absent one — never an error, never a changed exit status."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    registry = _registry(tmp_path)
    _write_entry(registry, _entry("t055-empty", workspace))
    (workspace / ".specify" / "memory" / "exec-quant" / "records").mkdir(parents=True)

    empty = _digest(workspace, registry)
    assert empty.returncode == 0, empty.stderr
    assert _no_measurements_literal() in empty.stdout, (
        "C-68: an empty store renders the same explicit state; got %r" % empty.stdout
    )


def test_c68_the_entry_set_is_identical_to_a_render_without_the_dimension(tmp_path):
    """C-68: apart from the element's own text, the entry set is byte-identical to a store-less render."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    registry = _registry(tmp_path)
    for index in range(3):
        _write_entry(registry, _entry("t055-identical-%d" % index, workspace))
    _write_store(
        workspace,
        [_store_record("/speckit.plan", "command", "2026-11-06T09:00:00Z",
                       elapsed={"value": 253000, "provenance": "carried"})],
    )

    with_store = _digest(workspace, registry, "--cap", "5")
    assert with_store.returncode == 0, with_store.stderr
    without = _digest_with_the_store_hidden(workspace, registry, "--cap", "5")

    # The element is *content* of an entry: removing exactly the element's own field group from each row must give
    # back the store-less render byte for byte — every other field, the ordering, the cap and the summary survive.
    def strip_element(text: str):
        kept = []
        for line in text.splitlines():
            # The render's clock-bearing header line is not a bound C-68 protects: the comparison is field-level.
            if line.startswith("generated_at=") or "生成于" in line:
                continue
            line = re.sub(r"\s*efficiency=([^|]*)$", "", line)
            line = re.sub(r"\s\s+", " ", line).rstrip()
            kept.append(line)
        return kept

    got = strip_element(with_store.stdout)
    expected = strip_element(without)
    # The only permitted difference is the store-availability statement the present store replaces (C-68).
    got = [line for line in got if not re.search(r"(?i)no measurements", line)]
    expected = [line for line in expected if not re.search(r"(?i)no measurements", line)]
    assert got == expected, (
        "C-68: with the element removed the render must be unchanged; got %r expected %r" % (got, expected)
    )


# --------------------------------------------------------------------------- #
# C-70 / C-71 — no self-named schema, field slot or `quality` sub-key
# --------------------------------------------------------------------------- #
def test_c65_neither_delivered_script_carries_a_record_format_parser():
    """C-65: neither delivered script re-parses the store's record files, re-implements the legacy-stream path,
    shells out to the engine's command line, or keeps a cache.

    The scan is an AST-level one: it looks for a JSON read whose operand names the store's own surfaces (the record
    directory or the legacy stream). A script that reads the *records* through ``json.load`` is a second reader; one
    that serializes its own rendered structures is not, and the engine's read path hands back parsed records.
    """
    delivered = [
        Path("scripts") / "python" / "status-digest.py",
        Path("scripts") / "python" / "measure.py",
    ]
    #: The store surfaces a re-parse would have to name (owner: ``scripts/python/exec-quant.py``).
    store_surfaces = ("records.jsonl", "scores.jsonl", "exec-quant")
    for rel in delivered:
        path = REPO_ROOT / rel
        assert path.is_file(), "a delivered script is missing: %s" % rel
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = (
                    [alias.name for alias in node.names]
                    if isinstance(node, ast.Import)
                    else [node.module or ""]
                )
                assert not any(name.split(".")[0] == "subprocess" for name in names), (
                    "C-65: %s shells out instead of importing the reader" % rel
                )
            if isinstance(node, ast.Call):
                func = node.func
                name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
                if name in {"load", "loads"}:
                    dumped = ast.dump(node)
                    assert not any(surface in dumped for surface in store_surfaces), (
                        "C-65: %s parses the store's record format itself at line %d"
                        % (rel, getattr(node, "lineno", 0))
                    )


def test_c70_neither_delivered_script_names_a_schema_version_field_slot_or_quality_subkey():
    """C-70 / C-71: the record's schema is reached by path through the engine; no delivered script re-spells it.

    The scan is an AST scan over the **string literals** of the delivered scripts: a literal naming a schema
    version, a ``quality`` sub-key or a closed vocabulary member would be a second definition of the declaration
    owner's fact. Comments and docstrings are excluded (a docstring names the owner's path, which is the legal
    reference form); only executable string literals are judged.
    """
    delivered = [
        Path("scripts") / "python" / "status-digest.py",
        Path("scripts") / "python" / "measure.py",
    ]
    #: The declaration owner's own vocabulary members, read from it rather than re-spelled here (C-71).
    declaration = (REPO_ROOT / "shared" / "declarations" / "facts" / "quant-record-schema.yaml").read_text(
        encoding="utf-8"
    )
    vocabulary = set(re.findall(r"^\s+-\s+([a-z][a-z-]+)\s*$", declaration, re.M))

    offenders = []
    for rel in delivered:
        path = REPO_ROOT / rel
        assert path.is_file(), "a delivered script is missing: %s" % rel
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        docstrings = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                body = getattr(node, "body", [])
                if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
                    docstrings.add(id(body[0].value))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
                continue
            if id(node) in docstrings:
                continue
            text = node.value
            if "schema_version" in text or "quality." in text or "elapsed_ms" in text:
                offenders.append((rel.as_posix(), text, node.lineno))
            elif text in vocabulary and len(text) > 3:
                offenders.append((rel.as_posix(), text, node.lineno))
    assert not offenders, (
        "C-70/C-71: a delivered script re-spells the declaration owner's fact instead of reaching it by path: %r"
        % (offenders,)
    )


def test_c71_the_not_evaluated_marker_is_real_and_stable_across_the_two_surfaces(tmp_path):
    """C-71: both surfaces render the *same* marker — one literal, two hosts, read from the owner by anchor."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    registry = _registry(tmp_path)
    _write_entry(registry, _entry("t055-marker", workspace))
    # The record sits inside the run the registry entry names, so the digest's step set includes its step.
    _write_store(workspace, [_store_record("/speckit.plan", "command", "2026-11-06T09:00:00Z",
                                           run_id="r20261106T000000Z-t055-marker")])

    digest = _digest(workspace, registry)
    line = _report(workspace, registry)
    assert digest.returncode == 0, digest.stderr
    assert line.returncode == 0, line.stderr
    marker = _marker_literal()
    assert marker in digest.stdout.lower(), (
        "C-71: the digest renders the owner's marker verbatim; got %r expected %r"
        % (digest.stdout, marker)
    )
    assert marker in line.stdout.lower(), (
        "C-71: the status line renders the same literal; got %r expected %r" % (line.stdout, marker)
    )
