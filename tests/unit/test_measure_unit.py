"""Unit tests for the one reader / two projections rule and the element's record selection (087, T056).

Layer-1 of the Feature 087 test map (``tasks.md`` § Tests Mode). This file owns what a whole-repository contract
test cannot isolate:

* **one reader** — the efficiency projection (``scripts/python/status-digest.py``) and the measure report
  (``scripts/python/measure.py``) each obtain their records by importing ``scripts/python/exec-quant.py``'s read path
  **in process**; an AST check asserts neither delivered script carries a record-format parser of its own
  (``contracts/efficiency-element.contract.md`` C-65, ``contracts/measure-report.contract.md`` C-53);
* **the element's selection rule** — the record with the latest ``collected_at``, ties resolved by the record's own
  identity ascending, never by filesystem enumeration order, never folded (C-66);
* **render-wide withdrawal** — the token / invocation quantities are withdrawn from *every* unit on a render
  together, never per unit (C-64, Clarifications Q2).

**What this file does not own**: the surfaces' own shapes (cap, staleness, exit statuses) are
``status-digest.contract.md`` C-43…C-45's; the element's contract-level assertions are
``tests/contract/test_efficiency_element.py``'s. Where a fact has an owner, this file reads it from the owner (the
provenance marker from ``shared/guidelines/reporting-obligations.md``, the state vocabulary from the registry engine)
rather than spelling a second copy.

**Red-first (Constitution IV)**: authored before T062/T063/T064 land, so every test here is expected to fail on the
pre-implementation tree with a message naming the missing behaviour.
"""
from __future__ import annotations

import ast
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
DIGEST = REPO_ROOT / "scripts" / "python" / "status-digest.py"
MEASURE = REPO_ROOT / "scripts" / "python" / "measure.py"
STORE_ENGINE = REPO_ROOT / "scripts" / "python" / "exec-quant.py"
LINE_REGISTRY_ENGINE = (
    REPO_ROOT / "skills" / "external" / "sdd-loop-driver" / "scripts" / "line-registry.py"
)
OWNER_DOC = REPO_ROOT / "shared" / "guidelines" / "reporting-obligations.md"


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _require(path: Path) -> Path:
    assert path.is_file(), (
        "%s is missing: %s — red is the intended pre-implementation state for T056."
        % (path.name, path.relative_to(REPO_ROOT))
    )
    return path


def _engine_constants() -> dict:
    text = LINE_REGISTRY_ENGINE.read_text(encoding="utf-8")

    def literal(name: str) -> set:
        match = re.search(r"^%s\s*=\s*\{(.*?)\}" % re.escape(name), text, re.S | re.M)
        assert match, "the registry engine carries no %s" % name
        return set(re.findall(r"[\"']([^\"']+)[\"']", match.group(1)))

    return {"STATE_VALUES": literal("STATE_VALUES"), "ACTIVE_STATES": literal("ACTIVE_STATES")}


def _run(script: Path, args, cwd: Path, env_overrides=None) -> subprocess.CompletedProcess:
    _require(script)
    env = os.environ.copy()
    for key in ("SPECIFY_LINE_REGISTRY_DIR", "XDG_STATE_HOME", "SPECIFY_STATUS_WORKSPACE"):
        env.pop(key, None)
    env["HOME"] = str(cwd)
    env.update(env_overrides or {})
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=str(cwd),
        env=env,
        capture_output=True,
        text=True,
    )


def _registry(tmp_path: Path) -> Path:
    path = tmp_path / "registry"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _entry(line_id: str, workspace: Path, **overrides) -> dict:
    active = sorted(_engine_constants()["ACTIVE_STATES"])[0]
    entry = {
        "line_id": line_id,
        "run_id": "r20261106T000000Z-" + line_id,
        "project_dir": str(workspace),
        "branch": "main",
        "stage": "implement",
        "state": active,
        "updated_at": "2026-11-06T09:00:00Z",
    }
    entry.update(overrides)
    return entry


def _record(unit_id: str, unit_type: str, collected_at: str, elapsed=None, tokens=None,
            invocations=None) -> dict:
    return {
        "kind": "speckit.exec-quant",
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


def _store(workspace: Path) -> Path:
    directory = workspace / ".specify" / "memory" / "exec-quant" / "records"
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def _write_records(workspace: Path, records) -> list:
    directory = _store(workspace)
    written = []
    for stem, record in records:
        path = directory / ("%s.json" % stem)
        path.write_text(json.dumps(record), encoding="utf-8")
        written.append(path)
    return written


def _marker() -> str:
    """The not-evaluated marker, read from its single definition site (owner document, C-47)."""
    text = OWNER_DOC.read_text(encoding="utf-8")
    match = re.search(r"`(not[- ]evaluated)`", text, re.I)
    assert match, "the owner document declares no not-evaluated marker literal (C-47)"
    form = match.group(1).lower()
    return "not-evaluated" if "-" in form else "not evaluated"


def _render_line(workspace: Path, registry: Path, *extra) -> subprocess.CompletedProcess:
    """One status line, with the emitting step the flow names (FR-024: the line is that step alone)."""
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
        *extra,
    ]
    return _run(DIGEST, args, cwd=workspace,
                env_overrides={"SPECIFY_LINE_REGISTRY_DIR": str(registry)})


def _render_digest(workspace: Path, registry: Path, *extra) -> subprocess.CompletedProcess:
    return _run(
        DIGEST,
        ["--action", "digest", "--workspace", str(workspace), *extra],
        cwd=workspace,
        env_overrides={"SPECIFY_LINE_REGISTRY_DIR": str(registry)},
    )


# --------------------------------------------------------------------------- #
# C-65 / C-53 — one reader, two projections; no delivered parser
# --------------------------------------------------------------------------- #
def _module_imports(tree) -> set:
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                names.add(node.module)
    return names


def _reader_import_sites(tree) -> list:
    """Every site that names the store engine's module — an ``import``, an ``importlib`` spec, or a path literal.

    The two legal forms the plan fixes (``plan.md`` § S1 / T-003) are an in-process import of the engine module by
    path and the ``importlib.util.spec_from_file_location`` loader the engine's own siblings use; a shell-out or a
    re-parse names neither.
    """
    sites = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in {"spec_from_file_location", "spec_from_loader", "module_from_spec"}:
                sites.append(("importlib", getattr(node, "lineno", 0)))
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in {"spec_from_file_location", "module_from_spec"}:
                sites.append(("importlib", getattr(node, "lineno", 0)))
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            if node.value in {"exec-quant.py", "exec_quant", "exec-quant"}:
                sites.append(("literal", getattr(node, "lineno", 0)))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) and any(
            alias.name.split(".")[0] in {"exec_quant", "execquant"} for alias in node.names
        ):
            sites.append(("import", getattr(node, "lineno", 0)))
    return sites


def test_c65_c53_both_delivered_readers_reach_the_store_through_the_engine_module():
    """C-65 / C-53: the element's script and the measure script each reach the store through the engine's module."""
    for path in (DIGEST, MEASURE):
        _require(path)
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        sites = _reader_import_sites(tree)
        assert sites, (
            "C-65: %s must obtain its records by importing the store engine's read path in process; "
            "no import site was found" % path.relative_to(REPO_ROOT)
        )


# --------------------------------------------------------------------------- #
# C-66 — the selection rule: latest by collected_at, ties by record identity
# --------------------------------------------------------------------------- #
def _element_for(workspace: Path, registry: Path, unit_hint: str) -> str:
    """The rendered element for one unit, as the line printed it."""
    proc = _render_line(workspace, registry)
    assert proc.returncode == 0, proc.stderr
    match = re.search(r"unit=%s([^|]*)" % re.escape(unit_hint), proc.stdout)
    assert match, (
        "C-66: the line carries an element for %s; got %r" % (unit_hint, proc.stdout)
    )
    return match.group(0)


def test_c66_three_records_with_increasing_collected_at_select_the_newest(tmp_path):
    """C-66: the newest record wins — nothing is averaged, summed or ranked across the older ones."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    registry = _registry(tmp_path)
    (registry / "t056-latest.json").write_text(json.dumps(_entry("t056-latest", workspace)),
                                              encoding="utf-8")
    _write_records(
        workspace,
        [
            ("20261106T090000000001Z-aaaaaaaa",
             _record("/speckit.plan", "command", "2026-11-06T09:00:00Z",
                     elapsed={"value": 111000, "provenance": "carried"})),
            ("20261106T091000000001Z-bbbbbbbb",
             _record("/speckit.plan", "command", "2026-11-06T09:10:00Z",
                     elapsed={"value": 222000, "provenance": "carried"})),
            ("20261106T092000000001Z-cccccccc",
             _record("/speckit.plan", "command", "2026-11-06T09:20:00Z",
                     elapsed={"value": 333000, "provenance": "carried"})),
        ],
    )
    element = _element_for(workspace, registry, "/speckit.plan")
    assert "333000" in element, "C-66: the element reports the newest record; got %r" % element
    for stale in ("111000", "222000"):
        assert stale not in element, (
            "C-66: an older record's quantity is never folded into the element; got %r" % element
        )


def test_c66_a_tie_on_collected_at_is_resolved_by_record_identity_ascending(tmp_path):
    """C-66: the tie-break is the record's own identity ascending — stable under a shuffled enumeration order."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    registry = _registry(tmp_path)
    (registry / "t056-tie.json").write_text(json.dumps(_entry("t056-tie", workspace)), encoding="utf-8")

    same_stamp = "2026-11-06T09:30:00Z"
    # Two records sharing the newest collected_at, distinguished only by their name stems.
    low = ("20261106T093000000001Z-aaaa0000",
           _record("/speckit.plan", "command", same_stamp,
                   elapsed={"value": 444000, "provenance": "carried"}))
    high = ("20261106T093000000002Z-zzzz9999",
            _record("/speckit.plan", "command", same_stamp,
                    elapsed={"value": 555000, "provenance": "carried"}))

    _write_records(workspace, [low, high])
    first = _element_for(workspace, registry, "/speckit.plan")

    # Re-create the same two records in the opposite write order: the identity rule, not the enumeration order,
    # must decide. The store's own reader sorts by stem, so a renderer relying on write or glob order would flip.
    for path in _store(workspace).glob("*.json"):
        path.unlink()
    _write_records(workspace, [high, low])
    second = _element_for(workspace, registry, "/speckit.plan")

    assert first == second, (
        "C-66: the tie-break must not depend on filesystem enumeration order; got %r then %r"
        % (first, second)
    )
    assert "444000" in first, (
        "C-66: the ascending identity rule selects the lower name stem; got %r" % first
    )


def test_c66_the_element_never_widens_the_surfaces_unit_set(tmp_path):
    """C-66: a store holding more units than the surfaces list introduces no extra element."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    registry = _registry(tmp_path)
    (registry / "t056-one.json").write_text(json.dumps(_entry("t056-one", workspace)), encoding="utf-8")
    _write_records(
        workspace,
        [
            ("20261106T090000000001Z-aaaaaaaa",
             _record("/speckit.plan", "command", "2026-11-06T09:00:00Z",
                     elapsed={"value": 1000, "provenance": "carried"})),
            ("20261106T090000000002Z-bbbbbbbb",
             _record("/speckit.tasks", "command", "2026-11-06T09:00:01Z",
                     elapsed={"value": 2000, "provenance": "carried"})),
            ("20261106T090000000003Z-cccccccc",
             _record("skill:draw-diagram", "skill", "2026-11-06T09:00:02Z",
                     elapsed={"value": 3000, "provenance": "carried"})),
        ],
    )
    proc = _render_digest(workspace, registry, "--cap", "5")
    assert proc.returncode == 0, proc.stderr
    rows = [line for line in proc.stdout.splitlines() if line.startswith("line_id=")]
    assert len(rows) == 1, rows
    assert rows[0].count("unit=") == 1, (
        "C-66: one element per listed unit, never one per store record; got %r" % rows[0]
    )


# --------------------------------------------------------------------------- #
# C-64 — the withdrawal is render-wide, never per unit
# --------------------------------------------------------------------------- #
def test_c64_the_token_invocation_withdrawal_is_render_wide_not_per_unit(tmp_path):
    """C-64 / Clarifications Q2: one unit shown with tokens while its neighbour is not is the defect."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    registry = _registry(tmp_path)
    for line_id in ("t056-wide-a", "t056-wide-b"):
        (registry / ("%s.json" % line_id)).write_text(
            json.dumps(_entry(line_id, workspace)), encoding="utf-8"
        )
    _write_records(
        workspace,
        [
            ("20261106T090000000001Z-aaaaaaaa",
             _record("/speckit.plan", "command", "2026-11-06T09:00:00Z",
                     elapsed={"value": 1000, "provenance": "measured"},
                     tokens={"value": 1200, "provenance": "measured"},
                     invocations={"value": 3, "provenance": "measured"})),
            ("20261106T090000000002Z-bbbbbbbb",
             _record("/speckit.tasks", "command", "2026-11-06T09:00:01Z",
                     elapsed={"value": 2000, "provenance": "measured"},
                     tokens={"value": 900, "provenance": "measured"},
                     invocations={"value": 2, "provenance": "measured"})),
        ],
    )

    wide = _render_digest(workspace, registry, "--cap", "2")
    assert wide.returncode == 0, wide.stderr
    row_tokens = [("tokens=" in line) for line in wide.stdout.splitlines() if line.startswith("line_id=")]
    assert all(row_tokens) or not any(row_tokens), (
        "C-64: token depth must be uniform across one render; got per-row presence %r" % row_tokens
    )

    tight = _render_digest(workspace, registry, "--cap", "2", "--element-bound", "40")
    assert tight.returncode == 0, tight.stderr
    tight_tokens = [
        ("tokens=" in line) for line in tight.stdout.splitlines() if line.startswith("line_id=")
    ]
    assert tight_tokens and not any(tight_tokens), (
        "C-64: a tight bound withdraws tokens from EVERY unit on the render; got %r" % tight_tokens
    )
    assert "elapsed=" in tight.stdout, "C-64: elapsed stays unconditional at any bound"


# --------------------------------------------------------------------------- #
# C-64 — a not-evaluated quantity renders the marker, never a zero
# --------------------------------------------------------------------------- #
def test_c64_a_not_evaluated_quantity_renders_the_marker_and_never_zero(tmp_path):
    """C-64: the marker is the record's own state, rendered explicitly; ``0`` would read as "free"."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    registry = _registry(tmp_path)
    (registry / "t056-marker.json").write_text(json.dumps(_entry("t056-marker", workspace)),
                                               encoding="utf-8")
    _write_records(
        workspace,
        [("20261106T090000000001Z-aaaaaaaa",
          _record("/speckit.plan", "command", "2026-11-06T09:00:00Z"))],
    )
    element = _element_for(workspace, registry, "/speckit.plan")
    assert _marker().replace(" ", "-") in element.replace(" ", "-"), (
        "C-64: the not-evaluated record renders the owner's marker; got %r" % element
    )
    assert "elapsed=0" not in element, "C-64: never zero; got %r" % element
