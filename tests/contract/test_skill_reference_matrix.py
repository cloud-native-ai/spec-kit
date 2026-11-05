"""Contract tests for Feature 082 US5 — SC-006 matrix recomputation (T026).

Every row of ``tests/fixtures/skill-reference/normalization-matrix.json`` is
recomputed through ``tests/contract/skill_reference_matrix.py`` and compared with
the row's own expectation: both the **decision class** and the **paired
raw-plus-normalized shape** (FR-025 / FR-030 / GM-13).

* The denominator is the fixture's own row count and MUST be at least 12.
* A run prints one ``rows=N matched=N failed=0`` reading.
* Any single mismatch fails **with the row named** — never "the rest passed".
* Rows whose ``repo_root`` is ``none`` are recomputed without I/O; ``scratch`` rows
  are materialized under ``tmp_path`` from the row's own ``scratch`` block;
  ``live`` rows are read from the repository.

Readings (``repo_root == live``) depend on the layer distribution of the live
tree, so a row that names one layer is checked for that layer and a row that names
two is checked for two **distinct** layers (the criterion is the layer, never the
path literal — § Disambiguation rules (c)).

All comparison lives in :func:`recompute`, which the negative case re-runs against
a mutated ``tmp_path`` copy (GM-07).
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
MATRIX_REL = Path("tests/fixtures/skill-reference/normalization-matrix.json")
HELPER_REL = Path("tests/contract/skill_reference_matrix.py")

#: SC-006 — the fixture MUST carry at least this many rows.
MIN_ROWS = 12

#: GM-13 — the three disjoint segments a row may belong to.
SEGMENTS = ("surface", "normalize", "failure")


def _helper():
    """Import the test-only executable implementation (not a pytest module)."""
    path = REPO_ROOT / HELPER_REL
    assert path.is_file(), "artifact missing: %s" % path
    spec = importlib.util.spec_from_file_location("skill_reference_matrix", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_matrix(path: Path) -> dict:
    assert path.is_file(), "artifact missing: %s" % path
    return json.loads(path.read_text(encoding="utf-8"))


def _recompute_row(module, row: dict, tmp_root: Path) -> dict:
    """Recompute one row under its declared ``repo_root``."""
    form = row["form"]
    operation = row.get("operation", "invocation")
    where = row.get("repo_root", "live")
    select = form if form in module.OPERATIONS else "bare name"
    if where == "none":
        return module.normalize(row["raw"], form=select, operation=operation)
    if where == "scratch":
        scratch = tmp_root / row["id"]
        scratch.mkdir(parents=True, exist_ok=True)
        module.materialize_scratch(row.get("scratch") or {}, scratch)
        return module.normalize(row["raw"], form=select, operation=operation,
                                repo_root=scratch)
    return module.normalize(row["raw"], form=select, operation=operation,
                            repo_root=REPO_ROOT)


def _compare(module, row: dict, result: dict,
             command_surfaces: list[str] | None = None) -> list[str]:
    """Every difference between one row's expectation and its recomputation."""
    expect = row["expect"]
    problems: list[str] = []
    for field in ("raw", "normalized", "decision_class"):
        if field not in result:
            problems.append("%s: the report carries no %r" % (row["id"], field))
    if result.get("raw") != row["raw"]:
        problems.append("%s: report raw %r is not the row's raw %r"
                        % (row["id"], result.get("raw"), row["raw"]))
    if result.get("outcome") != expect["outcome"]:
        problems.append("%s: decision class %r, expected %r"
                        % (row["id"], result.get("outcome"), expect["outcome"]))
    if result.get("decision_class") != result.get("outcome"):
        problems.append("%s: decision_class %r disagrees with the outcome %r"
                        % (row["id"], result.get("decision_class"), result.get("outcome")))
    if result.get("normalized") != expect["normalized"]:
        problems.append("%s: normalized %r, expected %r"
                        % (row["id"], result.get("normalized"), expect["normalized"]))
    if "failure_class" in expect:
        if result.get("failure_class") != expect["failure_class"]:
            problems.append("%s: failure class %r, expected %r"
                            % (row["id"], result.get("failure_class"),
                               expect["failure_class"]))
        report = result.get("report_items") or {}
        for item in expect.get("report_items", []):
            if item not in report:
                problems.append("%s: the failure report omits %r" % (row["id"], item))
    if "layer" in expect and result.get("layer") != expect["layer"]:
        problems.append("%s: layer %r, expected %r"
                        % (row["id"], result.get("layer"), expect["layer"]))
    if "case_pass" in expect and result.get("case_pass") != expect["case_pass"]:
        problems.append("%s: case pass %r, expected %r"
                        % (row["id"], result.get("case_pass"), expect["case_pass"]))
    if "command_target" in expect:
        if result.get("command_target") != expect["command_target"]:
            problems.append("%s: command target %r, expected %r"
                            % (row["id"], result.get("command_target"),
                               expect["command_target"]))
        if result.get("enters_skill_resolution") is not False:
            problems.append("%s: a command-surface row entered Skill resolution" % row["id"])

    # Structural rules every row obeys, whatever its expectation says.
    if row["segment"] not in SEGMENTS:
        problems.append("%s: segment %r is outside %r" % (row["id"], row["segment"], SEGMENTS))
    if expect["outcome"] not in module.OUTCOMES:
        problems.append("%s: expected outcome %r is not one of the three"
                        % (row["id"], expect["outcome"]))
    if row["segment"] == "failure" and expect["outcome"] != "failure":
        problems.append("%s: a failure-segment row must close as 'failure'" % row["id"])
    if row["segment"] == "surface" and expect["outcome"] == "command-surface" \
            and "command_target" not in expect:
        problems.append("%s: a command-surface row names no command target" % row["id"])
    if row["segment"] == "failure":
        for item in ("raw", "normalized"):
            if item not in (result.get("report_items") or {}):
                problems.append("%s: the paired report omits the %r half" % (row["id"], item))
    # A command-surface row never enters Skill resolution, whatever its expectation.
    if result.get("outcome") == "command-surface":
        if result.get("enters_skill_resolution") is not False:
            problems.append("%s: a command-surface row entered Skill resolution" % row["id"])
        target = result.get("command_target")
        # The negative surface row (a command-shaped name that is not a command) names
        # a target that need not exist: the ruling follows the namespace, not the file.
        if target and command_surfaces is not None and (REPO_ROOT / target).is_file():
            command_surfaces.append(target)
    return problems


def recompute(matrix: dict, tmp_root: Path,
              command_surfaces: list[str] | None = None) -> tuple[int, int, list[str]]:
    """Recompute every row; return ``(rows, matched, problems)``.

    ``matched`` counts rows with **zero** discrepancies. A row with any problem is
    not matched, so the count can never read as "the rest passed".
    """
    module = _helper()
    problems: list[str] = []
    matched = 0
    for row in matrix["rows"]:
        row_problems = _compare(module, row, _recompute_row(module, row, tmp_root),
                                command_surfaces)
        if row_problems:
            problems.extend(row_problems)
        else:
            matched += 1
    return len(matrix["rows"]), matched, problems


# --------------------------------------------------------------------------- #
# SC-006 — the matrix
# --------------------------------------------------------------------------- #
def test_sc006_fixture_is_three_disjoint_segments_of_at_least_twelve_rows():
    matrix = _load_matrix(REPO_ROOT / MATRIX_REL)
    rows = matrix["rows"]
    assert len(rows) >= MIN_ROWS, "the matrix carries %d rows, fewer than %d" % (
        len(rows), MIN_ROWS)
    seen: dict[str, str] = {}
    for row in rows:
        for key in ("segment", "id", "raw", "form", "expect"):
            assert key in row, "row %r carries no %r" % (row.get("id"), key)
        assert row["id"] not in seen, "row id %r is used twice" % row["id"]
        seen[row["id"]] = row["segment"]
    assert {row["segment"] for row in rows} == set(SEGMENTS), (
        "the segments present are %r, not the three disjoint ones"
        % sorted({row["segment"] for row in rows}))
    # SC-006 names the six accepted forms as coverage the matrix owns; a matrix that
    # lost a whole form's rows would still clear MIN_ROWS, so the form set is asserted.
    forms = {row["form"] for row in rows}
    missing_forms = set(_helper().FORMS) - forms
    assert not missing_forms, (
        "the matrix carries no row for accepted form(s) %r — SC-006 names the six forms"
        % sorted(missing_forms)
    )


def row_reading(module, row: dict, tmp_root: Path) -> str:
    """One matrix row's own reading: what the implementation said and what was expected."""
    result = _recompute_row(module, row, tmp_root)
    expect = row["expect"]
    verdict = "ok" if (
        result.get("outcome") == expect["outcome"]
        and result.get("normalized") == expect["normalized"]
    ) else "MISMATCH"
    return (
        "row %s segment=%s raw=%r outcome=%s normalized=%r expected=%s/%r %s"
        % (row["id"], row["segment"], row["raw"], result.get("outcome"),
           result.get("normalized"), expect["outcome"], expect["normalized"], verdict)
    )


def test_sc006_every_row_recomputes(tmp_path):
    matrix = _load_matrix(REPO_ROOT / MATRIX_REL)
    command_surfaces: list[str] = []
    rows, matched, problems = recompute(matrix, tmp_path, command_surfaces=command_surfaces)
    assert "templates/commands/skills.md" in command_surfaces, (
        "no command-surface row pointed at templates/commands/skills.md: %r"
        % command_surfaces)
    row_lines = [row_reading(_helper(), row, tmp_path) for row in matrix["rows"]]
    for line in row_lines:
        print(line)
    assert len(row_lines) == rows, (
        "the run printed %d per-row reading(s) for %d matrix row(s) — a total without "
        "its rows is not recomputable" % (len(row_lines), rows))
    printed_ids = [line.split()[1] for line in row_lines]
    assert printed_ids == [row["id"] for row in matrix["rows"]], (
        "the per-row readings name %r, not the matrix's own row order" % printed_ids)
    reading = "rows=%d matched=%d failed=%d" % (rows, matched, len(problems))
    print(reading)
    assert rows >= MIN_ROWS, reading
    assert not problems, reading + "\n" + "\n".join(problems)
    assert matched == rows, reading


def test_sc006_negative_case_one_changed_expectation_turns_red(tmp_path):
    matrix = _load_matrix(REPO_ROOT / MATRIX_REL)
    # A 'none' row is recomputed without I/O, so the drift lands on this row alone
    # (a live row's tier is read from the tree, which a copied matrix must not disturb).
    target = next(row for row in matrix["rows"] if row["segment"] == "normalize"
                  and row.get("repo_root") == "none")
    target["expect"]["normalized"] = target["expect"]["normalized"] + "-drifted"
    rows, matched, problems = recompute(matrix, tmp_path / "run")
    assert matched == rows - 1, "the negative case changed %d rows, not one" % (
        rows - matched)
    assert any(target["id"] in p for p in problems), (
        "the comparison did not turn red on the mutated row %r" % target["id"])
