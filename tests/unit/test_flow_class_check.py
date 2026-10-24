"""Unit tests for ``scripts/python/flow-class-check.py`` (069a, T006).

Owns the parser/behaviour details of
``.specify/specs/069a-flow-classification-docs-gates/contracts/flow-class-ledger.md``
that ``tasks.md`` T006 names — the parts a whole-repository contract test cannot
isolate:

* ledger row parsing: a wrong cell count, a missing required value, and a
  non-canonical unit id each report ``row-malformed`` (the parser never guesses a
  column; the same ledger with a permuted header still parses by header name);
* unit-id normalisation: commands are ``/speckit.<stem>``, skills are
  ``skill:<dir>``; nothing else is accepted;
* the anti-vacuous floor: commands 27 / skills 51 — a smaller inventory is
  ``inventory-truncated``, and a tree without ``skills/`` never reports "zero gaps";
* the eight finding kinds are reported independently (``missing`` / ``unknown`` /
  ``duplicate`` / ``dual-class`` / ``invalid-class`` / ``row-malformed`` /
  ``neutral-unlisted`` / ``inventory-truncated``);
* the exit-code ladder: ``check`` 0/1/2 and ``lookup`` 0/2;
* ``lookup`` degradation: an unregistered unit carries the fixed marker with
  ``source=default``; an unparsable owner keeps the default class with
  ``marker=null`` and reports the owner degradation label — the two labels are
  mutually exclusive (FR-009 / FR-016);
* both actions are read-only.

Fixtures are built from scratch in ``tmp_path``; no test touches the real owner or
the real ledger. Red-first (Constitution IV): the engine does not exist yet, so
``_run`` asserts the script path first — red is "artifact missing / behaviour
wrong", never an import or collection error.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "flow-class-check.py"
OWNER_REL = Path("shared") / "definitions" / "flow-class-definitions.md"

# requirements.md § Shared Strings (pinned copies).
STR_001 = "execution"
STR_002 = "expression"
STR_003 = "flow_class"
STR_004 = "未声明·按默认"

LEDGER_COLUMNS = ("unit_id", STR_003, "basis", "neutral", "notes")
EIGHT_KINDS = (
    "missing",
    "unknown",
    "duplicate",
    "dual-class",
    "invalid-class",
    "row-malformed",
    "neutral-unlisted",
    "inventory-truncated",
)
ISO_Z_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _run(*args: str) -> subprocess.CompletedProcess:
    assert ENGINE.is_file(), (
        "flow-class engine missing: %s — expected at T009/T010 (069a). "
        "Red is the intended pre-implementation state for T006."
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


def _render_owner(
    rows: list[dict],
    neutral_rows: list[tuple[str, str, str]],
    *,
    columns=LEDGER_COLUMNS,
    include_table: bool = True,
    extra_rows: tuple[str, ...] = (),
) -> str:
    lines = [
        "# Flow Class Definitions (unit-test fixture)",
        "",
        "本文件是 069a 单元测试的临时夹具，不是仓库所有者。",
        "",
        "## 判据",
        "",
        "fixture: 主交付物的验收由什么判定。",
        "",
        "## 逐流程台账",
        "",
    ]
    if include_table:
        lines.append("| " + " | ".join(columns) + " |")
        lines.append("| " + " | ".join("---" for _ in columns) + " |")
        for row in rows:
            lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
        lines.extend(extra_rows)
    lines.extend(
        [
            "",
            "## 类中立清单",
            "",
            "| unit_id | category | rationale |",
            "| --- | --- | --- |",
        ]
    )
    for unit, category, rationale in neutral_rows:
        lines.append("| %s | %s | %s |" % (unit, category, rationale))
    lines.extend(
        [
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
    return "\n".join(lines)


def _build_repo(
    root: Path,
    *,
    commands: int = 27,
    skills: int = 51,
    with_skills_dir: bool = True,
    columns=LEDGER_COLUMNS,
):
    """Materialise a fixture repo of the requested size; returns (rows, neutral_rows)."""
    stems = ["cmd-%02d" % number for number in range(1, commands + 1)]
    names = ["skill-%02d" % number for number in range(1, skills + 1)]
    for stem in stems:
        _write(
            root / "templates" / "commands" / ("%s.md" % stem),
            "# /speckit.%s\n\nfixture command template\n" % stem,
        )
    if with_skills_dir:
        (root / "skills" / "external").mkdir(parents=True, exist_ok=True)
        (root / "skills" / "internal").mkdir(parents=True, exist_ok=True)
    for index, name in enumerate(names):
        layer = "external" if index < 14 else "internal"
        _write(
            root / "skills" / layer / name / "SKILL.md",
            "---\nname: %s\ndescription: fixture skill\n---\n" % name,
        )

    rows: list[dict] = []
    for index, stem in enumerate(stems):
        rows.append(
            {
                "unit_id": "/speckit.%s" % stem,
                STR_003: STR_001 if index % 2 == 0 else STR_002,
                "basis": "behavior-oracle",
                "neutral": "",
                "notes": "",
            }
        )
    for index, name in enumerate(names):
        rows.append(
            {
                "unit_id": "skill:%s" % name,
                STR_003: STR_001 if index % 2 == 0 else STR_002,
                "basis": "reader-oracle",
                "neutral": "",
                "notes": "",
            }
        )
    neutral_rows: list[tuple[str, str, str]] = []
    if names:
        carrier = "skill:%s" % names[0]
        for row in rows:
            if row["unit_id"] == carrier:
                row["neutral"] = "yes"
        neutral_rows.append(
            (carrier, "memory", "carries the caller's memory records; no deliverable of its own")
        )
    _write_owner(root, rows, neutral_rows, columns=columns)
    return rows, neutral_rows


def _write_owner(root: Path, rows: list[dict], neutral_rows, **render_kwargs) -> None:
    _write(root / OWNER_REL, _render_owner(rows, neutral_rows, **render_kwargs))


def _check(root: Path):
    proc = _run("--action", "check", "--repo", str(root), "--format", "json")
    record = _json(proc) if proc.stdout.strip() else None
    return proc, record


def _lookup(root: Path, unit_id: str):
    return _run(
        "--action", "lookup", "--repo", str(root), "--unit-id", unit_id, "--format", "json"
    )


def _kinds(record: dict) -> list[str]:
    return [finding.get("kind") for finding in record.get("findings", [])]


def _assert_kind(record: dict, kind: str, unit: str | None = None) -> list[dict]:
    matches = [finding for finding in record.get("findings", []) if finding.get("kind") == kind]
    assert matches, "expected a %r finding; got %r" % (kind, record.get("findings"))
    if unit is not None:
        assert any(finding.get("unit_id") == unit for finding in matches), (
            "expected a %r finding for %r; got %r" % (kind, unit, matches)
        )
    return matches


def _digest(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


# --------------------------------------------------------------------------- #
# baseline: a complete fixture is gap-free
# --------------------------------------------------------------------------- #
def test_clean_full_fixture_exits_0_with_no_findings(tmp_path):
    _build_repo(tmp_path)
    proc, record = _check(tmp_path)
    assert proc.returncode == 0, (
        "a complete ledger over a 27/51 inventory must exit 0; findings=%r stderr=%r"
        % (None if record is None else record.get("findings"), proc.stderr)
    )
    assert record is not None, "check must print JSON on stdout"
    assert record.get("action") == "check"
    assert record.get("findings") == []
    assert record.get("units") == 78, "check must report 78 scanned units; got %r" % record.get("units")
    assert ISO_Z_RE.match(str(record.get("checked_at", ""))), (
        "checked_at must be ISO-8601 Z; got %r" % record.get("checked_at")
    )


# --------------------------------------------------------------------------- #
# the eight finding kinds, reported independently
# --------------------------------------------------------------------------- #
def test_missing_ledger_row_reports_missing(tmp_path):
    rows, neutral_rows = _build_repo(tmp_path)
    removed = rows.pop(0)
    _write_owner(tmp_path, rows, neutral_rows)
    proc, record = _check(tmp_path)
    assert proc.returncode == 1
    _assert_kind(record, "missing", unit=removed["unit_id"])
    kinds = set(_kinds(record))
    assert kinds <= set(EIGHT_KINDS), (
        "findings must stay inside the eight declared kinds; unexpected=%r"
        % sorted(kinds - set(EIGHT_KINDS))
    )
    assert "unknown" not in kinds, "a ledger gap is 'missing', not 'unknown': %r" % sorted(kinds)
    assert "inventory-truncated" not in kinds, (
        "the inventory is still 27/51; truncation must not be claimed: %r" % sorted(kinds)
    )


def test_ledger_row_absent_from_inventory_reports_unknown(tmp_path):
    rows, neutral_rows = _build_repo(tmp_path)
    rows.append(
        {
            "unit_id": "/speckit.ghost",
            STR_003: STR_001,
            "basis": "behavior-oracle",
            "neutral": "",
            "notes": "",
        }
    )
    _write_owner(tmp_path, rows, neutral_rows)
    proc, record = _check(tmp_path)
    assert proc.returncode == 1
    _assert_kind(record, "unknown", unit="/speckit.ghost")
    assert "missing" not in set(_kinds(record)), (
        "an extra ledger row is 'unknown', not 'missing'"
    )


def test_repeated_row_reports_duplicate(tmp_path):
    rows, neutral_rows = _build_repo(tmp_path)
    rows.append(dict(rows[0]))
    _write_owner(tmp_path, rows, neutral_rows)
    proc, record = _check(tmp_path)
    assert proc.returncode == 1
    _assert_kind(record, "duplicate", unit=rows[0]["unit_id"])
    assert "dual-class" not in set(_kinds(record)), (
        "two rows with the same value are a duplicate, not a dual class"
    )
    assert "invalid-class" not in set(_kinds(record)), (
        "both repeated values are in-domain; invalid-class must stay silent"
    )


def test_opposite_values_report_dual_class(tmp_path):
    rows, neutral_rows = _build_repo(tmp_path)
    flipped = dict(rows[0])
    flipped[STR_003] = STR_002 if rows[0][STR_003] == STR_001 else STR_001
    rows.append(flipped)
    _write_owner(tmp_path, rows, neutral_rows)
    proc, record = _check(tmp_path)
    assert proc.returncode == 1
    _assert_kind(record, "dual-class", unit=rows[0]["unit_id"])
    assert "invalid-class" not in set(_kinds(record)), (
        "both values are in-domain; the defect is the conflict, not the domain"
    )


def test_out_of_domain_value_reports_invalid_class(tmp_path):
    rows, neutral_rows = _build_repo(tmp_path)
    rows[0][STR_003] = "hybrid"
    _write_owner(tmp_path, rows, neutral_rows)
    proc, record = _check(tmp_path)
    assert proc.returncode == 1
    _assert_kind(record, "invalid-class", unit=rows[0]["unit_id"])
    assert "row-malformed" not in set(_kinds(record)), (
        "the row is structurally well formed; only the value is out of domain"
    )


def test_row_with_wrong_cell_count_reports_row_malformed(tmp_path):
    rows, neutral_rows = _build_repo(tmp_path)
    _write_owner(
        tmp_path,
        rows,
        neutral_rows,
        extra_rows=(
            "| /speckit.short | %s | behavior-oracle | |" % STR_001,  # 4 cells
            "| /speckit.long | %s | behavior-oracle | | | extra |" % STR_001,  # 6 cells
        ),
    )
    proc, record = _check(tmp_path)
    assert proc.returncode == 1
    matches = _assert_kind(record, "row-malformed")
    assert len(matches) >= 2, (
        "both the 4-cell and the 6-cell row must be reported: %r" % matches
    )
    assert "invalid-class" not in set(_kinds(record)), (
        "a column-count defect is not an out-of-domain value"
    )


def test_row_with_empty_required_value_reports_row_malformed(tmp_path):
    rows, neutral_rows = _build_repo(tmp_path)
    rows.append(
        {
            "unit_id": "/speckit.empty-basis",
            STR_003: STR_001,
            "basis": "",
            "neutral": "",
            "notes": "",
        }
    )
    _write_owner(tmp_path, rows, neutral_rows)
    proc, record = _check(tmp_path)
    assert proc.returncode == 1
    _assert_kind(record, "row-malformed", unit="/speckit.empty-basis")


def test_non_canonical_unit_ids_report_row_malformed(tmp_path):
    rows, neutral_rows = _build_repo(tmp_path)
    bad_ids = (
        "speckit.cmd-99",   # missing the leading slash
        "/speckit.",        # empty stem
        "skill:",           # empty skill name
        "skill:Bad Name",   # space / uppercase
        "skill:foo/bar",    # path, not a directory name
        "",                 # empty first cell
    )
    extra = tuple(
        "| %s | %s | behavior-oracle | | |" % (unit_id, STR_001) for unit_id in bad_ids
    )
    _write_owner(tmp_path, rows, neutral_rows, extra_rows=extra)
    proc, record = _check(tmp_path)
    assert proc.returncode == 1
    matches = _assert_kind(record, "row-malformed")
    assert len(matches) >= len(bad_ids), (
        "every non-canonical unit id must be reported; expected >= %d, got %r"
        % (len(bad_ids), matches)
    )
    assert set(_kinds(record)) == {"row-malformed"}, (
        "unparseable rows must not be re-classified as missing/unknown/invalid-class; "
        "kinds=%r" % sorted(set(_kinds(record)))
    )


def test_neutral_flag_outside_closed_list_reports_neutral_unlisted(tmp_path):
    rows, neutral_rows = _build_repo(tmp_path)
    rows[0]["neutral"] = "yes"  # not in the closed list
    _write_owner(tmp_path, rows, neutral_rows)
    proc, record = _check(tmp_path)
    assert proc.returncode == 1
    _assert_kind(record, "neutral-unlisted", unit=rows[0]["unit_id"])


# --------------------------------------------------------------------------- #
# anti-vacuous floors and the customer-project shape
# --------------------------------------------------------------------------- #
def test_inventory_truncated_below_command_floor(tmp_path):
    rows, neutral_rows = _build_repo(tmp_path, commands=26, skills=51)
    _write_owner(tmp_path, rows, neutral_rows)
    proc, record = _check(tmp_path)
    assert proc.returncode == 1
    _assert_kind(record, "inventory-truncated")
    kinds = set(_kinds(record))
    assert "missing" not in kinds and "unknown" not in kinds, (
        "the ledger matches the (truncated) inventory; the only defect is the floor: %r"
        % sorted(kinds)
    )


def test_inventory_truncated_below_skill_floor(tmp_path):
    rows, neutral_rows = _build_repo(tmp_path, commands=27, skills=50)
    _write_owner(tmp_path, rows, neutral_rows)
    proc, record = _check(tmp_path)
    assert proc.returncode == 1
    _assert_kind(record, "inventory-truncated")
    assert "missing" not in set(_kinds(record)) and "unknown" not in set(_kinds(record))


def test_repo_without_skills_directory_is_not_silently_green(tmp_path):
    rows, neutral_rows = _build_repo(tmp_path, commands=27, skills=0, with_skills_dir=False)
    _write_owner(tmp_path, rows, neutral_rows)
    proc, record = _check(tmp_path)
    assert proc.returncode != 0, (
        "a tree without skills/ must not report zero gaps (C-5 / C-14)"
    )
    assert record is not None
    assert record.get("findings"), "findings must be non-empty when the skill inventory is absent"
    _assert_kind(record, "inventory-truncated")
    if "units" in record:
        assert record["units"] < 78, "a missing skills/ tree has fewer than 78 units"


def test_repo_with_empty_skills_directory_is_not_silently_green(tmp_path):
    rows, neutral_rows = _build_repo(tmp_path, commands=27, skills=0, with_skills_dir=True)
    _write_owner(tmp_path, rows, neutral_rows)
    proc, record = _check(tmp_path)
    assert proc.returncode != 0
    _assert_kind(record, "inventory-truncated")


# --------------------------------------------------------------------------- #
# exit-code ladder
# --------------------------------------------------------------------------- #
def test_exit_code_ladder(tmp_path):
    clean = tmp_path / "clean"
    _build_repo(clean)
    clean_proc, _ = _check(clean)
    assert clean_proc.returncode == 0, "check with zero findings must exit 0"

    broken = tmp_path / "broken"
    broken_rows, broken_neutral = _build_repo(broken)
    broken_rows.pop(0)
    _write_owner(broken, broken_rows, broken_neutral)
    broken_proc, _ = _check(broken)
    assert broken_proc.returncode == 1, "check with a finding must exit 1"

    ownerless = tmp_path / "ownerless"
    _build_repo(ownerless)
    (ownerless / OWNER_REL).unlink()
    ownerless_proc, _ = _check(ownerless)
    assert ownerless_proc.returncode == 2, "check without an owner document must exit 2"

    registered = _lookup(clean, "/speckit.cmd-01")
    assert registered.returncode == 0, "lookup of a registered unit must exit 0"
    unregistered = _lookup(clean, "/speckit.never-registered")
    assert unregistered.returncode == 0, "lookup of an unregistered unit must exit 0 (no interruption)"
    malformed = _lookup(clean, "cmd-01")
    assert malformed.returncode == 2, "lookup of a malformed unit id must exit 2"


def test_check_exit_2_when_owner_missing(tmp_path):
    _build_repo(tmp_path)
    (tmp_path / OWNER_REL).unlink()
    proc, _ = _check(tmp_path)
    assert proc.returncode == 2
    assert proc.stderr.strip(), "exit 2 must explain itself on stderr"


def test_check_exit_2_when_ledger_header_missing(tmp_path):
    rows, neutral_rows = _build_repo(tmp_path)
    _write_owner(tmp_path, rows, neutral_rows, include_table=False)
    proc, _ = _check(tmp_path)
    assert proc.returncode == 2, (
        "an owner without a parseable ledger header is an input/parse error (C-13), not a finding"
    )
    assert proc.stderr.strip(), "exit 2 must explain itself on stderr"


# --------------------------------------------------------------------------- #
# parsing rules
# --------------------------------------------------------------------------- #
def test_parser_reads_columns_by_header_and_does_not_guess(tmp_path):
    # Same data, permuted header: a position-guessing parser would read the neutral
    # cell as the class value and report every row as malformed.
    permuted = ("neutral", "unit_id", "basis", STR_003, "notes")
    rows, neutral_rows = _build_repo(tmp_path, columns=permuted)
    proc, record = _check(tmp_path)
    assert proc.returncode == 0, (
        "the parser must bind columns by header name, not by position; findings=%r"
        % (None if record is None else record.get("findings"))
    )
    assert record is not None and record.get("findings") == []


def test_unit_ids_are_normalised_to_the_two_canonical_forms(tmp_path):
    rows, neutral_rows = _build_repo(tmp_path, commands=3, skills=2)
    _write_owner(tmp_path, rows, neutral_rows)

    command_record = _json(_lookup(tmp_path, "/speckit.cmd-01"))
    assert command_record.get("source") == "ledger"
    assert command_record.get(STR_003) == rows[0][STR_003]

    skill_record = _json(_lookup(tmp_path, "skill:skill-01"))
    assert skill_record.get("source") == "ledger"
    assert skill_record.get(STR_003) == rows[3][STR_003]

    for bad in ("cmd-01", "speckit.cmd-01", "/cmd-01", "skill:skill-01/extra", "", "skill:", "/speckit."):
        proc = _lookup(tmp_path, bad)
        assert proc.returncode == 2, (
            "non-canonical unit id %r must be rejected with exit 2; got %d"
            % (bad, proc.returncode)
        )


# --------------------------------------------------------------------------- #
# lookup degradation branches (FR-009 / FR-016)
# --------------------------------------------------------------------------- #
def test_lookup_unregistered_keeps_the_marker_non_empty(tmp_path):
    _build_repo(tmp_path)
    proc = _lookup(tmp_path, "/speckit.never-registered")
    assert proc.returncode == 0
    record = _json(proc)
    assert record.get(STR_003) == STR_001
    assert record.get("source") == "default"
    assert record.get("marker") == STR_004, (
        "the unregistered path must carry the fixed marker; got %r" % record.get("marker")
    )
    assert record.get("basis") is None
    assert "owner-unavailable" not in proc.stderr, (
        "the unregistered path must not emit the owner degradation label 'owner-unavailable'"
    )


def test_lookup_owner_missing_keeps_default_semantics(tmp_path):
    _build_repo(tmp_path)
    (tmp_path / OWNER_REL).unlink()
    proc = _lookup(tmp_path, "/speckit.cmd-01")
    assert proc.returncode == 2, "an unparsable owner must exit 2"
    record = _json(proc)
    assert record.get(STR_003) == STR_001, (
        "an unparsable owner must keep the default class semantics"
    )
    assert record.get("source") == "default"
    assert record.get("marker") is None, (
        "the owner-degradation path must NOT carry the unregistered marker (mutually exclusive)"
    )
    assert "owner-unavailable" in proc.stderr, (
        "the degradation must be visible on stderr as 'owner-unavailable' "
        "(single unified label, C-7 / data-model E9); stderr=%r" % proc.stderr
    )


def test_lookup_owner_without_ledger_table_keeps_default_semantics(tmp_path):
    rows, neutral_rows = _build_repo(tmp_path)
    _write_owner(tmp_path, rows, neutral_rows, include_table=False)
    proc = _lookup(tmp_path, "/speckit.cmd-01")
    assert proc.returncode == 2
    record = _json(proc)
    assert record.get(STR_003) == STR_001
    assert record.get("marker") is None
    assert "owner-unavailable" in proc.stderr


# --------------------------------------------------------------------------- #
# lookup must not hand back a corrupted or ambiguous value as decided (FR-016)
# --------------------------------------------------------------------------- #
def test_lookup_out_of_domain_class_degrades_with_a_visible_label(tmp_path):
    rows, neutral_rows = _build_repo(tmp_path)
    rows[0][STR_003] = "hybrid"          # outside the closed two-value domain
    _write_owner(tmp_path, rows, neutral_rows)
    proc = _lookup(tmp_path, rows[0]["unit_id"])
    assert proc.returncode == 2, (
        "an out-of-domain class must degrade (exit 2), never exit 0 as a decided value"
    )
    record = _json(proc)
    assert record.get(STR_003) == STR_001, (
        "a corrupted value must fall back to the default class; got %r"
        % record.get(STR_003)
    )
    assert record.get("source") == "default", (
        "source must not be 'ledger' when the ledger value is out of domain; got %r"
        % record.get("source")
    )
    assert record.get("marker") is None, (
        "the fixed undeclared marker is reserved for 'not registered' (C-7)"
    )
    assert "owner-unavailable" in proc.stderr, (
        "the degradation must carry the closed owner-degradation label"
    )
    assert "invalid-class" in proc.stderr, (
        "the stderr detail must name the defect (invalid-class), stderr=%r" % proc.stderr
    )


def test_lookup_duplicate_rows_never_silently_pick_the_first(tmp_path):
    rows, neutral_rows = _build_repo(tmp_path)
    rows.append(dict(rows[0]))           # same unit, same value
    _write_owner(tmp_path, rows, neutral_rows)
    proc = _lookup(tmp_path, rows[0]["unit_id"])
    assert proc.returncode == 2, "a duplicated ledger row is not a decided class"
    record = _json(proc)
    assert record.get("source") == "default"
    assert record.get(STR_003) == STR_001
    assert record.get("marker") is None
    assert "duplicate" in proc.stderr, (
        "the detail must name the duplicate defect, stderr=%r" % proc.stderr
    )


def test_lookup_conflicting_rows_report_dual_class(tmp_path):
    rows, neutral_rows = _build_repo(tmp_path)
    twin = dict(rows[0])
    twin[STR_003] = STR_002 if rows[0][STR_003] == STR_001 else STR_001
    rows.append(twin)
    _write_owner(tmp_path, rows, neutral_rows)
    proc = _lookup(tmp_path, rows[0]["unit_id"])
    assert proc.returncode == 2
    record = _json(proc)
    assert record.get("source") == "default"
    assert record.get(STR_003) == STR_001
    assert "dual-class" in proc.stderr, (
        "two rows that disagree must be reported as dual-class, stderr=%r" % proc.stderr
    )


def test_default_marker_and_owner_degradation_label_are_mutually_exclusive(tmp_path):
    parsed_owner = tmp_path / "parsed"
    _build_repo(parsed_owner)
    unregistered = _lookup(parsed_owner, "/speckit.never-registered")
    assert _json(unregistered).get("marker") == STR_004
    assert "owner-unavailable" not in unregistered.stderr

    unparsable_owner = tmp_path / "unparsable"
    _build_repo(unparsable_owner)
    (unparsable_owner / OWNER_REL).unlink()
    degraded = _lookup(unparsable_owner, "/speckit.cmd-01")
    degraded_record = _json(degraded)
    assert degraded.returncode == 2
    assert degraded_record.get("marker") is None
    assert degraded_record.get("source") == "default"
    assert "owner-unavailable" in degraded.stderr
    assert degraded_record.get("marker") != STR_004, (
        "the two degradation labels must never be presented together"
    )


# --------------------------------------------------------------------------- #
# read-only guarantee
# --------------------------------------------------------------------------- #
def test_check_and_lookup_are_read_only(tmp_path):
    _build_repo(tmp_path)
    before = _digest(tmp_path)
    _check(tmp_path)
    _lookup(tmp_path, "/speckit.cmd-01")
    _lookup(tmp_path, "/speckit.never-registered")
    after = _digest(tmp_path)
    assert after == before, (
        "check/lookup must not write or modify any file; changed=%r added=%r removed=%r"
        % (
            sorted(path for path in before if after.get(path) != before[path]),
            sorted(set(after) - set(before)),
            sorted(set(before) - set(after)),
        )
    )
