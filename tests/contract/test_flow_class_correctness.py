"""Classification-correctness contract test (069a, T005 / FR-006 / SC-001).

The ledger is only worth its bytes if ``flow-class-check.py --action lookup`` returns
the *right* class for a known population — a structural "the table has 78 rows" test
cannot tell a correct classification from a scrambled one. This file therefore:

* builds a self-contained fixture repository (owner document + command templates +
  skills) with at least ten flow units: both classes at least three times, at least
  one unregistered unit, at least one neutral carrier, and at least one
  ``mixed-oracle`` row;
* compares every ``lookup`` result (class key / ``source`` / ``basis`` / ``marker`` /
  ``neutral``) against an oracle read from
  ``tests/fixtures/flow_class/classification-oracle.md`` — a **separate artifact**
  written from the owner's *criteria text*, with a per-unit criterion-application
  row. The expectation is never inlined from the fixture's own class values: that
  would only prove lookup copies the ledger back (the defect this file closes);
* carries a mutation assertion: flipping one unit's class in a temporary copy of the
  fixture MUST turn the very same comparison red, and restoring it MUST turn it green.
  A second assertion flips the *oracle* instead, proving the expectation side drives
  the comparison too. That is what makes FR-006 / SC-001 machine-falsifiable rather
  than merely present.

The fixture owner embeds the **real** owner criteria (``shared/definitions/
flow-class-definitions.md`` § 判据), not a stub: a fixture whose criteria section is
a placeholder cannot claim to test a criteria-driven judgment.

Red-first (Constitution IV): the engine does not exist yet. ``_run`` asserts the
script path first, so a red is "artifact missing / behaviour wrong", never an import
or collection error.

Shared-string literals are pinned copies of ``requirements.md`` § Shared Strings.
"""
from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "flow-class-check.py"
OWNER_REL = Path("shared") / "definitions" / "flow-class-definitions.md"
REAL_OWNER = REPO_ROOT / OWNER_REL
ORACLE_FILE = (
    Path(__file__).resolve().parents[1]
    / "fixtures"
    / "flow_class"
    / "classification-oracle.md"
)

# requirements.md § Shared Strings (pinned copies).
STR_001 = "execution"
STR_002 = "expression"
STR_003 = "flow_class"
STR_004 = "未声明·按默认"

LEDGER_COLUMNS = ("unit_id", STR_003, "basis", "neutral", "notes")

# --------------------------------------------------------------------------- #
# Fixture input: ten ledger units. This is the *input* side only — the expected
# classes live in the oracle artifact below, never here.
# --------------------------------------------------------------------------- #
FIXTURE_ROWS = [
    {"unit_id": "/speckit.docs", STR_003: STR_002, "basis": "reader-oracle", "neutral": ""},
    {"unit_id": "/speckit.humanize", STR_003: STR_002, "basis": "reader-oracle", "neutral": ""},
    {"unit_id": "/speckit.requirements", STR_003: STR_001, "basis": "behavior-oracle", "neutral": ""},
    {"unit_id": "/speckit.plan", STR_003: STR_001, "basis": "behavior-oracle", "neutral": ""},
    {"unit_id": "/speckit.analyze", STR_003: STR_001, "basis": "behavior-oracle", "neutral": ""},
    {
        "unit_id": "/speckit.implement",
        STR_003: STR_001,
        "basis": "mixed-oracle",
        "neutral": "",
        "notes": "parent 069 §Edge Cases (mixed oracle resolves to execution in 069b)",
    },
    {"unit_id": "skill:create-docs", STR_003: STR_002, "basis": "reader-oracle", "neutral": ""},
    {"unit_id": "skill:humanize", STR_003: STR_002, "basis": "reader-oracle", "neutral": ""},
    {"unit_id": "skill:git-utils", STR_003: STR_001, "basis": "behavior-oracle", "neutral": ""},
    {"unit_id": "skill:memory-record", STR_003: STR_001, "basis": "behavior-oracle", "neutral": "yes"},
]

FIXTURE_NEUTRAL_ROWS = [
    ("skill:memory-record", "memory", "carries the caller's memory records; no deliverable of its own"),
]

# Well-formed but never registered: default class + fixed marker, not "decided".
# These carry no classification judgment, so they are not oracle table rows.
UNREGISTERED_PROBES = ("/speckit.ghost", "skill:ghost")

COMPARED_FIELDS = (STR_003, "source", "basis", "marker", "neutral")


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _run(*args: str) -> subprocess.CompletedProcess:
    assert ENGINE.is_file(), (
        "flow-class engine missing: %s — expected at T009/T010 (069a). "
        "Red is the intended pre-implementation state for T005."
        % ENGINE.relative_to(REPO_ROOT)
    )
    return subprocess.run(
        [sys.executable, str(ENGINE), *args],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )


def _json(proc: subprocess.CompletedProcess) -> dict:
    assert proc.stdout.strip(), (
        "expected a JSON document on stdout, got empty output (stderr: %r)" % proc.stderr
    )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(
            "stdout is not JSON (%s); head=%r" % (exc, proc.stdout[:400])
        ) from exc


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


# --------------------------------------------------------------------------- #
# oracle artifact (expected side) — a separate file, never the fixture's values
# --------------------------------------------------------------------------- #
ORACLE_SECTION = "## 判定记录"
ORACLE_COLUMNS = (
    "unit_id",
    "主交付物（第一步）",
    "判定面（第二步）",
    "判据落点",
    STR_003,
    "basis",
    "neutral",
)


def _oracle_rows() -> dict[str, tuple]:
    """Parse ``tests/fixtures/flow_class/classification-oracle.md``.

    The workbook records, per unit, the two judging steps and the criteria anchor
    the class comes from. The test compares only the last three columns; the prose
    columns exist so a reader can falsify the judgment without re-running anything.
    """
    assert ORACLE_FILE.is_file(), (
        "independent oracle artifact missing: %s — the expectation must live in its "
        "own file, not inline in this test (FR-006 / SC-001)"
        % ORACLE_FILE.relative_to(REPO_ROOT)
    )
    lines = ORACLE_FILE.read_text(encoding="utf-8").splitlines()
    start = next(
        (i for i, line in enumerate(lines) if line.strip() == ORACLE_SECTION), None
    )
    assert start is not None, "oracle artifact lacks a %r section" % ORACLE_SECTION
    header = None
    rows: dict[str, tuple] = {}
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if header is None:
            header = cells
            assert tuple(header) == ORACLE_COLUMNS, (
                "oracle table header drifted: %r (expected %r)" % (header, ORACLE_COLUMNS)
            )
            continue
        if all(set(cell) <= set(":-") for cell in cells):
            continue
        record = dict(zip(header, cells))
        unit_id = record["unit_id"]
        rows[unit_id] = (
            record[STR_003],
            "ledger",
            record["basis"],
            None,
            record["neutral"].strip().lower() == "yes",
        )
    assert rows, "oracle artifact yielded no judgment rows"
    return rows


def _expectations() -> dict[str, tuple]:
    """The oracle plus the two unregistered probes (which carry no judgment)."""
    expected = dict(_oracle_rows())
    for unit_id in UNREGISTERED_PROBES:
        expected[unit_id] = (STR_001, "default", None, STR_004, False)
    return expected


def _owner_criteria_block() -> str:
    """The owner's real ``## 判据`` section, embedded verbatim into the fixture."""
    assert REAL_OWNER.is_file(), "owner missing: %s" % OWNER_REL
    lines = REAL_OWNER.read_text(encoding="utf-8").splitlines()
    start = next(
        (i for i, line in enumerate(lines) if line.strip() == "## 判据"), None
    )
    assert start is not None, "the owner carries no %r section" % "## 判据"
    end = next(
        (i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")),
        len(lines),
    )
    block = "\n".join(lines[start:end]).strip()
    assert "唯一问题" in block and "判定步骤" in block, (
        "the embedded criteria block does not look like the owner's § 判据"
    )
    return block


def _render_owner(rows: list[dict]) -> str:
    header = "| " + " | ".join(LEDGER_COLUMNS) + " |"
    separator = "| " + " | ".join("---" for _ in LEDGER_COLUMNS) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")) for column in LEDGER_COLUMNS) + " |"
        for row in rows
    ]
    neutral = [
        "| " + " | ".join(entry) + " |" for entry in FIXTURE_NEUTRAL_ROWS
    ]
    return "\n".join(
        [
            "# Flow Class Definitions (correctness fixture)",
            "",
            "本文件是 069a 正确性测试的临时夹具，不是仓库所有者；",
            "其中的判据段逐字来自真实所有者 `%s` § 判据。" % OWNER_REL.as_posix(),
            "",
            _owner_criteria_block(),
            "",
            "## 逐流程台账",
            "",
            header,
            separator,
            *body,
            "",
            "## 类中立清单",
            "",
            "| unit_id | category | rationale |",
            "| --- | --- | --- |",
            *neutral,
            "",
            "## 变更记录",
            "",
            "| date | unit_id | before → after | basis | 依据 |",
            "| --- | --- | --- | --- | --- |",
            "",
            "## 命名空间",
            "",
            "fixture.",
            "",
        ]
    )


def _build_fixture(root: Path) -> Path:
    """Materialise the fixture repository; returns the owner document path."""
    for row in FIXTURE_ROWS:
        unit = row["unit_id"]
        if unit.startswith("/speckit."):
            stem = unit.split(".", 1)[1]
            _write(root / "templates" / "commands" / ("%s.md" % stem), "# /speckit.%s\n" % stem)
        else:
            name = unit.split(":", 1)[1]
            layer = "internal" if name == "memory-record" else "external"
            _write(
                root / "skills" / layer / name / "SKILL.md",
                "---\nname: %s\ndescription: fixture skill\n---\n" % name,
            )
    owner = root / OWNER_REL
    _write(owner, _render_owner(FIXTURE_ROWS))
    return owner


def _lookup(root: Path, unit_id: str) -> dict:
    proc = _run(
        "--action", "lookup", "--repo", str(root), "--unit-id", unit_id, "--format", "json"
    )
    assert proc.returncode == 0, (
        "lookup of well-formed unit %r must exit 0; stderr=%r" % (unit_id, proc.stderr)
    )
    record = _json(proc)
    assert record.get("unit_id") == unit_id, (
        "lookup must echo the requested unit id; got %r" % record.get("unit_id")
    )
    return record


def _compare(root: Path, expected_map: dict[str, tuple] | None = None):
    """Return every (unit, field, expected, actual) mismatch against the oracle."""
    expected_map = expected_map if expected_map is not None else _expectations()
    mismatches: list[tuple[str, str, object, object]] = []
    for unit_id, expected in expected_map.items():
        record = _lookup(root, unit_id)
        for offset, field in enumerate(COMPARED_FIELDS):
            actual = record.get(field)
            if actual != expected[offset]:
                mismatches.append((unit_id, field, expected[offset], actual))
    return mismatches


# --------------------------------------------------------------------------- #
# fixture self-check — the population must be able to catch a wrong classifier
# --------------------------------------------------------------------------- #
def test_fixture_matrix_is_not_vacuous(tmp_path):
    _build_fixture(tmp_path)
    expected = _expectations()
    classes = [value[0] for value in expected.values()]
    sources = [value[1] for value in expected.values()]
    assert len(expected) >= 10, "the fixture must cover at least 10 flow units"
    assert classes.count(STR_001) >= 3, "at least three execution units are required"
    assert classes.count(STR_002) >= 3, "at least three expression units are required"
    assert sources.count("default") >= 1, "at least one unregistered unit is required"
    assert any(value[4] for value in expected.values()), "at least one neutral unit is required"
    assert any(
        value[2] == "mixed-oracle" for value in expected.values()
    ), "at least one mixed-oracle unit is required"
    owner_text = (tmp_path / OWNER_REL).read_text(encoding="utf-8")
    for unit_id, value in expected.items():
        if value[1] == "ledger":
            assert unit_id in owner_text, (
                "fixture ledger is missing the unit %r it claims to register" % unit_id
            )


def test_every_oracle_unit_has_a_fixture_row():
    """The oracle and the input must describe the same population.

    A unit in the oracle with no fixture row would be a "default" match by luck; a
    fixture row with no oracle row would be an unchecked judgment.
    """
    oracle_units = set(_oracle_rows())
    fixture_units = {row["unit_id"] for row in FIXTURE_ROWS}
    assert oracle_units == fixture_units, (
        "oracle and fixture describe different populations: only-oracle=%r only-fixture=%r"
        % (sorted(oracle_units - fixture_units), sorted(fixture_units - oracle_units))
    )


def test_fixture_owner_embeds_the_real_criteria():
    """A stub criteria section cannot support a criteria-driven judgment."""
    text = _render_owner(FIXTURE_ROWS)
    assert "唯一问题" in text and "判定步骤" in text, (
        "the fixture owner must carry the real § 判据 text, not a placeholder"
    )
    assert "其验收由什么判定" in text, (
        "the owner's single judging question must be present verbatim"
    )


# --------------------------------------------------------------------------- #
# the comparison itself
# --------------------------------------------------------------------------- #
def test_lookup_matches_independent_oracle(tmp_path):
    _build_fixture(tmp_path)
    mismatches = _compare(tmp_path)
    assert not mismatches, (
        "lookup disagrees with the independent oracle (unit, field, expected, actual):\n  "
        + "\n  ".join(repr(mismatch) for mismatch in mismatches)
    )


def test_mutating_one_class_turns_the_same_comparison_red(tmp_path):
    original = tmp_path / "original"
    _build_fixture(original)
    assert _compare(original) == [], "the clean fixture must start green before mutating"

    mutated = tmp_path / "mutated"
    shutil.copytree(original, mutated)
    rows = copy.deepcopy(FIXTURE_ROWS)
    target = "/speckit.docs"
    changed = False
    for row in rows:
        if row["unit_id"] == target:
            assert row[STR_003] == STR_002, "fixture precondition: %s starts as expression" % target
            row[STR_003] = STR_001
            changed = True
    assert changed, "fixture precondition: %s exists in the ledger" % target
    (mutated / OWNER_REL).write_text(_render_owner(rows), encoding="utf-8")

    mismatches = _compare(mutated)
    assert mismatches, (
        "flipping one ledger class MUST turn the oracle comparison red — otherwise the "
        "test cannot falsify a wrong classification (FR-006 / SC-001)"
    )
    reddened_units = {mismatch[0] for mismatch in mismatches}
    assert reddened_units == {target}, (
        "only the mutated unit may disagree; mismatching units=%r" % sorted(reddened_units)
    )
    assert {mismatch[1] for mismatch in mismatches} == {STR_003}, (
        "the mutation changes the class field only; mismatching fields=%r"
        % sorted({mismatch[1] for mismatch in mismatches})
    )

    # Restore the ledger inside the same copy: the comparison must go green again,
    # which proves the red above was caused by the mutation and not by the copy.
    (mutated / OWNER_REL).write_text(_render_owner(copy.deepcopy(FIXTURE_ROWS)), encoding="utf-8")
    assert _compare(mutated) == [], "restoring the correct class must return the comparison to green"


def test_mutating_the_oracle_turns_the_same_comparison_red(tmp_path):
    """The expectation side must drive the comparison, not the other way round.

    If the oracle were a copy of the fixture values, flipping the *oracle* alone
    would still leave every row agreeing with itself; this leg proves it does not.
    """
    _build_fixture(tmp_path)
    assert _compare(tmp_path) == [], "fixture precondition: the clean run is green"

    flipped = _expectations()
    target = "/speckit.requirements"
    class_value, source, basis, marker, neutral = flipped[target]
    assert class_value == STR_001, "fixture precondition: %s is execution" % target
    flipped[target] = (STR_002, source, basis, marker, neutral)

    mismatches = _compare(tmp_path, flipped)
    assert mismatches, (
        "an oracle row that disagrees with the engine MUST turn the comparison red"
    )
    assert {mismatch[0] for mismatch in mismatches} == {target}, (
        "only the flipped oracle row may disagree; mismatching units=%r"
        % sorted({mismatch[0] for mismatch in mismatches})
    )
    assert {mismatch[1] for mismatch in mismatches} == {STR_003}, (
        "the flip changes the class field only; mismatching fields=%r"
        % sorted({mismatch[1] for mismatch in mismatches})
    )


# --------------------------------------------------------------------------- #
# C-7 / FR-016 — the two degradation labels never coexist
# --------------------------------------------------------------------------- #
def test_source_and_marker_invariants_hold_for_every_unit(tmp_path):
    _build_fixture(tmp_path)
    for unit_id, expected in _expectations().items():
        record = _lookup(tmp_path, unit_id)
        source = record.get("source")
        marker = record.get("marker")
        assert source in ("ledger", "default"), (
            "%s: source must be 'ledger' or 'default'; got %r" % (unit_id, source)
        )
        if source == "ledger":
            assert marker is None, (
                "%s: a ledger-sourced result must not carry the default marker; got %r"
                % (unit_id, marker)
            )
            assert record.get("basis") in ("behavior-oracle", "reader-oracle", "mixed-oracle"), (
                "%s: a ledger-sourced result must expose a known basis; got %r"
                % (unit_id, record.get("basis"))
            )
            assert record.get(STR_003) in (STR_001, STR_002)
        else:
            assert marker == STR_004, (
                "%s: source='default' with a parsable owner MUST carry the fixed marker %r; "
                "got %r" % (unit_id, STR_004, marker)
            )
            assert record.get("basis") is None, (
                "%s: a default result has no oracle basis; got %r"
                % (unit_id, record.get("basis"))
            )
