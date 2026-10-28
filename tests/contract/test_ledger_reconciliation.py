"""Contract tests for ledger reconciliation (069b, T014).

Owns the assertions of
``.specify/specs/069b-isomorphism-migration-metrics/contracts/ledger-reconciler.md``
C-1…C-7 that ``tasks.md`` T014 names:

* C-1  the anti-vacuous floor: a ledger parsed below the inventory-derived floor
  is ``ledger-truncated``; parsing zero rows over a non-empty inventory can never
  end green. The floor is derived from the inventory-side constants
  (``⌊(27 + 51) / 2⌋ = 39``), never from the ledger under inspection — deleting a
  single row (78 → 77) must stay a ``gap``, not become a parse failure.
* C-2  the ``coverage`` block carries the six declared integers and the declared
  arithmetic: ``gaps == missing + unknown`` and
  ``parse_errors == row-malformed + ledger-truncated`` (the inventory-side
  ``inventory-truncated`` is deliberately *not* counted). ``clean`` additionally
  requires ``findings == []`` — the four coverage conditions are necessary, not
  sufficient, which an ``inventory-truncated`` tree proves.
* C-3  ``red_kind`` is a two-bucket partition with a fixed priority
  (``owner-unavailable`` > ``framework-source-required`` > ``parse-failure`` >
  ``gap`` > ``clean``): the same deletion and a broken row must be
  distinguishable, and ``red_kind == clean`` ⟺ zero findings.
* C-5  the ledger version is declared exactly once inside § 逐流程台账; a missing
  declaration is ``ledger-version-missing`` (gap bucket), a duplicated one is
  ``row-malformed`` (parse bucket).
* C-7  a ``basis = mixed-oracle`` row is ``execution``; the ``expression``
  counter-injection is ``mixed-oracle-class`` and lands in the gap bucket.
* the closed neutral list keeps its flag check (``neutral-unlisted`` is a gap).

Every fixture is a framework-source tree (27 command templates + 51 skill
directories, owner under ``shared/``) built from scratch in ``tmp_path``; the real
owner is never written. Red-first (Constitution IV): 069a's engine has no
``coverage`` block, no ``red_kind``, no ``ledger-truncated`` /
``ledger-version-missing`` / ``mixed-oracle-class`` kind and no payload-root
branch, so every call here reds as "field / action missing" — never as an import
or collection error. ``_run`` asserts the script path first.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "flow-class-check.py"
OWNER_REL = Path("shared") / "definitions" / "flow-class-definitions.md"

# requirements.md § Shared Strings (pinned copies).
EXECUTION = "execution"
EXPRESSION = "expression"

LEDGER_COLUMNS = ("unit_id", "flow_class", "basis", "neutral", "notes")
COVERAGE_KEYS = (
    "ledger_rows",
    "inventory_units",
    "matched",
    "gaps",
    "parse_errors",
    "floor",
)
GAP_KINDS = frozenset(
    {
        "missing",
        "unknown",
        "duplicate",
        "dual-class",
        "invalid-class",
        "neutral-unlisted",
        "mixed-oracle-class",
        "ledger-version-missing",
    }
)
FLOOR_COMMANDS = 27
FLOOR_SKILLS = 51
LEDGER_FLOOR = (FLOOR_COMMANDS + FLOOR_SKILLS) // 2  # 39
VERSION_LINE = "**台账版本**: 1（2026-10-25）"


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _run(*args: str) -> subprocess.CompletedProcess:
    assert ENGINE.is_file(), (
        "flow-class engine missing: %s — expected from 069a. "
        "Red is the intended pre-implementation state for 069b T014."
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
    version: str | None = VERSION_LINE,
    duplicate_version: bool = False,
    extra_row_lines: tuple[str, ...] = (),
) -> str:
    lines = [
        "# Flow Class Definitions (069b contract fixture)",
        "",
        "fixture: not the repository owner.",
        "",
        "## 判据",
        "",
        "fixture: 主交付物的验收由什么判定。",
        "",
        "## 逐流程台账",
        "",
    ]
    if version is not None:
        lines.append(version)
        lines.append("")
    if duplicate_version and version is not None:
        lines.append(version)
        lines.append("")
    lines.append("| " + " | ".join(LEDGER_COLUMNS) + " |")
    lines.append("| " + " | ".join("---" for _ in LEDGER_COLUMNS) + " |")
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(c, "")) for c in LEDGER_COLUMNS) + " |")
    lines.extend(extra_row_lines)
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
    lines.extend(["", "## 变更记录", "", "| date | unit_id | before → after | basis | 依据 |", "| --- | --- | --- | --- | --- |", ""])
    return "\n".join(lines)


def _inventory_names(commands: int, skills: int) -> tuple[list[str], list[str]]:
    stems = ["cmd-%02d" % number for number in range(1, commands + 1)]
    names = ["skill-%02d" % number for number in range(1, skills + 1)]
    return stems, names


def _default_rows(commands: int = FLOOR_COMMANDS, skills: int = FLOOR_SKILLS) -> list[dict]:
    stems, names = _inventory_names(commands, skills)
    rows: list[dict] = []
    for index, stem in enumerate(stems):
        rows.append(
            {
                "unit_id": "/speckit.%s" % stem,
                "flow_class": EXECUTION if index % 2 == 0 else EXPRESSION,
                "basis": "behavior-oracle",
                "neutral": "",
                "notes": "",
            }
        )
    for index, name in enumerate(names):
        rows.append(
            {
                "unit_id": "skill:%s" % name,
                "flow_class": EXECUTION if index % 2 == 0 else EXPRESSION,
                "basis": "reader-oracle",
                "neutral": "",
                "notes": "",
            }
        )
    return rows


def _build_repo(
    root: Path,
    *,
    commands: int = FLOOR_COMMANDS,
    skills: int = FLOOR_SKILLS,
    rows: list[dict] | None = None,
    neutral_rows: list[tuple[str, str, str]] | None = None,
    owner_text: str | None = None,
) -> list[dict]:
    stems, names = _inventory_names(commands, skills)
    for stem in stems:
        _write(
            root / "templates" / "commands" / ("%s.md" % stem),
            "# /speckit.%s\n\nfixture command template\n" % stem,
        )
    for index, name in enumerate(names):
        layer = "external" if index < 14 else "internal"
        _write(
            root / "skills" / layer / name / "SKILL.md",
            "---\nname: %s\ndescription: fixture skill\n---\n" % name,
        )
    used_rows = list(rows) if rows is not None else _default_rows(commands, skills)
    used_neutral = list(neutral_rows) if neutral_rows is not None else []
    _write(
        root / OWNER_REL,
        owner_text if owner_text is not None else _render_owner(used_rows, used_neutral),
    )
    return used_rows


def _check(root: Path):
    proc = _run("--action", "check", "--repo", str(root), "--format", "json")
    record = _json(proc) if proc.stdout.strip() else None
    return proc, record


def _kinds(record: dict) -> list[str]:
    return [finding.get("kind") for finding in record.get("findings", [])]


def _coverage(record: dict) -> dict:
    assert record is not None, "check must print JSON on stdout"
    assert isinstance(record.get("coverage"), dict), (
        "check JSON must carry a `coverage` block (contract C-2); got %r"
        % (record.get("coverage"),)
    )
    return record["coverage"]


def _assert_coverage_shape(coverage: dict) -> None:
    missing = [key for key in COVERAGE_KEYS if key not in coverage]
    assert not missing, "coverage block lacks %r (contract C-2); got %r" % (
        missing,
        coverage,
    )
    for key in COVERAGE_KEYS:
        assert isinstance(coverage[key], int) and not isinstance(coverage[key], bool), (
            "coverage.%s must be an integer; got %r" % (key, coverage[key])
        )


def _assert_gap_arithmetic(record: dict) -> None:
    coverage = _coverage(record)
    kinds = _kinds(record)
    assert coverage["gaps"] == kinds.count("missing") + kinds.count("unknown"), (
        "gaps MUST equal missing + unknown (C-2); coverage=%r kinds=%r"
        % (coverage, kinds)
    )
    assert coverage["parse_errors"] == kinds.count("row-malformed") + kinds.count(
        "ledger-truncated"
    ), (
        "parse_errors MUST equal row-malformed + ledger-truncated (C-2); coverage=%r kinds=%r"
        % (coverage, kinds)
    )


# --------------------------------------------------------------------------- #
# real tree: the version declaration and the clean baseline
# --------------------------------------------------------------------------- #
def test_real_owner_declares_the_ledger_version_exactly_once():
    owner = REPO_ROOT / OWNER_REL
    assert owner.is_file(), "owner document missing: %s" % OWNER_REL
    body = _ledger_section(owner.read_text(encoding="utf-8"))
    declarations = [line for line in body if line.strip().startswith("**台账版本**")]
    assert len(declarations) == 1, (
        "§ 逐流程台账 MUST declare `**台账版本**: <int>（<YYYY-MM-DD>）` exactly once "
        "(C-5); found %d: %r" % (len(declarations), declarations)
    )
    assert "（" in declarations[0] and "）" in declarations[0], (
        "the version declaration must carry its date in full-width parentheses (C-5); got %r"
        % declarations[0]
    )


def test_real_tree_reconciles_clean_with_the_declared_coverage_numbers():
    proc, record = _check(REPO_ROOT)
    assert proc.returncode == 0, (
        "the real 79-row ledger must reconcile clean; findings=%r stderr=%r"
        % (None if record is None else record.get("findings"), proc.stderr)
    )
    assert record is not None and record.get("findings") == []
    assert record.get("red_kind") == "clean", (
        "red_kind must be `clean` on a zero-finding tree (C-3); got %r"
        % record.get("red_kind")
    )
    coverage = _coverage(record)
    _assert_coverage_shape(coverage)
    assert coverage["inventory_units"] == record["units"] == 79
    assert coverage["ledger_rows"] == 79
    assert coverage["matched"] == 79
    assert coverage["gaps"] == 0
    assert coverage["parse_errors"] == 0
    assert coverage["floor"] == LEDGER_FLOOR == 39


def _ledger_section(text: str) -> list[str]:
    lines = text.splitlines()
    body: list[str] = []
    inside = False
    for line in lines:
        if line.startswith("## "):
            if inside:
                break
            inside = "逐流程台账" in line
            continue
        if inside:
            body.append(line)
    return body


# --------------------------------------------------------------------------- #
# C-1: the anti-vacuous floor
# --------------------------------------------------------------------------- #
def test_clean_fixture_reports_the_full_coverage_block(tmp_path):
    _build_repo(tmp_path)
    proc, record = _check(tmp_path)
    assert proc.returncode == 0, "clean fixture must exit 0; findings=%r stderr=%r" % (
        None if record is None else record.get("findings"),
        proc.stderr,
    )
    coverage = _coverage(record)
    _assert_coverage_shape(coverage)
    assert coverage == {
        "ledger_rows": 78,
        "inventory_units": 78,
        "matched": 78,
        "gaps": 0,
        "parse_errors": 0,
        "floor": 39,
    }, "unexpected clean coverage: %r" % (coverage,)
    assert record.get("red_kind") == "clean"
    _assert_gap_arithmetic(record)


def test_zero_parsed_rows_never_end_green(tmp_path):
    _build_repo(tmp_path, rows=[])
    proc, record = _check(tmp_path)
    assert record is not None
    kinds = _kinds(record)
    assert "ledger-truncated" in kinds, (
        "zero parsed rows over a non-empty inventory MUST report `ledger-truncated` "
        "(C-1); got %r" % kinds
    )
    assert record.get("red_kind") == "parse-failure", (
        "a truncated ledger is a parse failure, not a gap (C-3); got %r"
        % record.get("red_kind")
    )
    assert proc.returncode == 1
    coverage = _coverage(record)
    _assert_coverage_shape(coverage)
    assert coverage["ledger_rows"] == 0
    assert coverage["inventory_units"] == 78
    assert coverage["matched"] == 0
    assert coverage["parse_errors"] >= 1
    _assert_gap_arithmetic(record)


def test_deleting_one_row_stays_a_gap_and_never_truncates(tmp_path):
    rows = _default_rows()
    _build_repo(tmp_path, rows=rows[:-1])
    proc, record = _check(tmp_path)
    assert record is not None
    kinds = _kinds(record)
    assert "missing" in kinds, "one deleted row must be `missing` (C-1); got %r" % kinds
    assert "ledger-truncated" not in kinds, (
        "77 parsed rows are above the floor of 39 — `ledger-truncated` MUST NOT "
        "fire (C-1 / C-4); got %r" % kinds
    )
    assert record.get("red_kind") == "gap", (
        "a single deleted row is a gap, not a parse failure (C-3); got %r"
        % record.get("red_kind")
    )
    assert proc.returncode == 1
    coverage = _coverage(record)
    assert coverage["ledger_rows"] == 77
    assert coverage["matched"] == 77
    assert coverage["gaps"] == 1
    assert coverage["parse_errors"] == 0
    assert coverage["floor"] == 39
    _assert_gap_arithmetic(record)


def test_floor_is_inventory_derived_and_not_the_expected_row_count(tmp_path):
    rows = _default_rows()
    _build_repo(tmp_path, rows=rows[:38])
    proc, record = _check(tmp_path)
    assert record is not None
    assert "ledger-truncated" in _kinds(record), (
        "38 parsed rows are below the floor of 39; got %r" % _kinds(record)
    )
    _build_repo(tmp_path, rows=rows[:39])
    proc, record = _check(tmp_path)
    assert record is not None
    assert "ledger-truncated" not in _kinds(record), (
        "39 parsed rows meet the floor — the floor is 39, not the 78 expected rows "
        "(C-1); got %r" % _kinds(record)
    )


# --------------------------------------------------------------------------- #
# C-2: coverage arithmetic and the closed-inventory boundary
# --------------------------------------------------------------------------- #
def test_gaps_are_missing_plus_unknown(tmp_path):
    rows = _default_rows()
    _build_repo(tmp_path, rows=rows[2:] + [_unknown_row("ghost")])
    proc, record = _check(tmp_path)
    assert record is not None
    kinds = _kinds(record)
    assert kinds.count("missing") == 2 and kinds.count("unknown") == 1, (
        "fixture must yield 2 missing + 1 unknown; got %r" % kinds
    )
    coverage = _coverage(record)
    assert coverage["gaps"] == 3
    assert coverage["ledger_rows"] == 77
    assert coverage["matched"] == 76
    _assert_gap_arithmetic(record)


def test_parse_errors_count_only_ledger_side_parse_defects(tmp_path):
    rows = _default_rows()
    malformed = "| not-a-unit-id | execution |"
    _build_repo(tmp_path, rows=rows, owner_text=_render_owner(rows, [], extra_row_lines=(malformed,)))
    proc, record = _check(tmp_path)
    assert record is not None
    assert "row-malformed" in _kinds(record), "expected a row-malformed finding"
    coverage = _coverage(record)
    assert coverage["ledger_rows"] == 78
    assert coverage["gaps"] == 0
    assert coverage["parse_errors"] == 1
    _assert_gap_arithmetic(record)


def test_inventory_truncation_is_a_parse_failure_but_not_a_parse_error(tmp_path):
    rows = _default_rows(commands=26, skills=50)
    _build_repo(tmp_path, commands=26, skills=50, rows=rows)
    proc, record = _check(tmp_path)
    assert record is not None
    kinds = _kinds(record)
    assert kinds.count("inventory-truncated") == 2, (
        "a 26/50 inventory must report two inventory-truncated findings; got %r" % kinds
    )
    coverage = _coverage(record)
    _assert_coverage_shape(coverage)
    # Necessary-but-not-sufficient: all four C-2 conditions hold here, yet the
    # tree is red because an inventory-side defect sits outside the gap bucket.
    assert coverage["matched"] == coverage["inventory_units"] == 76
    assert coverage["gaps"] == 0
    assert coverage["parse_errors"] == 0
    assert coverage["ledger_rows"] >= coverage["floor"]
    assert record.get("red_kind") == "parse-failure", (
        "inventory-truncated is outside the gap bucket (C-3); got %r"
        % record.get("red_kind")
    )
    assert proc.returncode == 1


# --------------------------------------------------------------------------- #
# C-3: red_kind is a two-bucket partition
# --------------------------------------------------------------------------- #
def test_red_kind_is_clean_exactly_when_findings_are_empty(tmp_path):
    _build_repo(tmp_path)
    proc, record = _check(tmp_path)
    assert record is not None and record.get("findings") == []
    assert record.get("red_kind") == "clean"
    assert (proc.returncode, record.get("red_kind")) == (0, "clean"), (
        "clean must be the only zero-finding red_kind and must exit 0 (C-3)"
    )

    rows = _default_rows()
    _build_repo(tmp_path, rows=rows[:-1])
    proc, record = _check(tmp_path)
    assert record is not None and record.get("findings")
    assert record.get("red_kind") != "clean"


def test_deleted_row_and_broken_row_are_distinguishable(tmp_path):
    rows = _default_rows()
    _build_repo(tmp_path, rows=rows[:-1])
    proc_gap, record_gap = _check(tmp_path)
    assert record_gap is not None
    assert record_gap.get("red_kind") == "gap"
    assert proc_gap.returncode == 1

    _build_repo(
        tmp_path,
        rows=rows,
        owner_text=_render_owner(
            rows, [], extra_row_lines=("| not-a-unit-id | execution |",)
        ),
    )
    proc_parse, record_parse = _check(tmp_path)
    assert record_parse is not None
    assert record_parse.get("red_kind") == "parse-failure"
    assert proc_parse.returncode == 1
    assert record_gap.get("red_kind") != record_parse.get("red_kind"), (
        "the two injections MUST differ on red_kind (C-3)"
    )


def test_gap_bucket_is_the_declared_closed_set(tmp_path):
    rows = _default_rows()
    # One gap-bucket kind at a time, all on the same complete inventory.
    injections = {
        "missing": rows[:-1],
        "unknown": rows + [_unknown_row("ghost")],
        "invalid-class": _mutate(rows, 0, flow_class="neither"),
        "duplicate": rows + [dict(rows[0])],
    }
    for label, injected in injections.items():
        _build_repo(tmp_path, rows=injected)
        proc, record = _check(tmp_path)
        assert record is not None, label
        observed = set(_kinds(record))
        assert observed, "injection %r produced no finding" % label
        assert observed <= GAP_KINDS, (
            "injection %r produced kinds outside the gap bucket: %r" % (label, observed)
        )
        assert record.get("red_kind") == "gap", (
            "injection %r must be a gap (C-3); got %r" % (label, record.get("red_kind"))
        )


def test_neutral_flag_outside_the_closed_list_lands_in_the_gap_bucket(tmp_path):
    rows = _default_rows()
    rows[-1]["neutral"] = "yes"
    _build_repo(tmp_path, rows=rows)
    proc, record = _check(tmp_path)
    assert record is not None
    assert "neutral-unlisted" in _kinds(record)
    assert record.get("red_kind") == "gap"
    _assert_gap_arithmetic(record)


# --------------------------------------------------------------------------- #
# C-5: the ledger version declaration
# --------------------------------------------------------------------------- #
def test_missing_version_declaration_is_a_gap_bucket_defect(tmp_path):
    rows = _default_rows()
    _build_repo(tmp_path, rows=rows, owner_text=_render_owner(rows, [], version=None))
    proc, record = _check(tmp_path)
    assert record is not None
    kinds = _kinds(record)
    assert "ledger-version-missing" in kinds, (
        "a missing `**台账版本**` declaration MUST be `ledger-version-missing` (C-5); "
        "got %r" % kinds
    )
    assert record.get("red_kind") == "gap", (
        "ledger-version-missing sits in the gap bucket (C-3); got %r"
        % record.get("red_kind")
    )
    coverage = _coverage(record)
    assert coverage["parse_errors"] == 0, (
        "a missing declaration is not a parse error (C-2 / C-5); got %r" % coverage
    )
    _assert_gap_arithmetic(record)


def test_duplicate_version_declaration_is_row_malformed(tmp_path):
    rows = _default_rows()
    _build_repo(
        tmp_path,
        rows=rows,
        owner_text=_render_owner(rows, [], duplicate_version=True),
    )
    proc, record = _check(tmp_path)
    assert record is not None
    kinds = _kinds(record)
    assert "row-malformed" in kinds, (
        "a duplicated declaration MUST reuse `row-malformed` (C-5); got %r" % kinds
    )
    assert "ledger-version-missing" not in kinds, (
        "a duplicated declaration is not a missing one; got %r" % kinds
    )
    assert record.get("red_kind") == "parse-failure"
    coverage = _coverage(record)
    assert coverage["parse_errors"] >= 1
    _assert_gap_arithmetic(record)


# --------------------------------------------------------------------------- #
# C-7: mixed oracle
# --------------------------------------------------------------------------- #
def test_mixed_oracle_execution_row_is_accepted(tmp_path):
    rows = _default_rows()
    rows[0]["basis"] = "mixed-oracle"
    rows[0]["flow_class"] = EXECUTION
    _build_repo(tmp_path, rows=rows)
    proc, record = _check(tmp_path)
    assert proc.returncode == 0, (
        "a mixed-oracle command row with flow_class=execution is valid (C-7); "
        "findings=%r" % (None if record is None else record.get("findings"))
    )
    assert record is not None and record.get("findings") == []


def test_mixed_oracle_expression_row_is_rejected(tmp_path):
    rows = _default_rows()
    rows[0]["basis"] = "mixed-oracle"
    rows[0]["flow_class"] = EXPRESSION
    _build_repo(tmp_path, rows=rows)
    proc, record = _check(tmp_path)
    assert record is not None
    matches = [
        finding
        for finding in record.get("findings", [])
        if finding.get("kind") == "mixed-oracle-class"
    ]
    assert matches, (
        "basis=mixed-oracle + flow_class=expression MUST be `mixed-oracle-class` (C-7); "
        "got %r" % _kinds(record)
    )
    assert any(finding.get("unit_id") == rows[0]["unit_id"] for finding in matches)
    assert record.get("red_kind") == "gap"
    _assert_gap_arithmetic(record)


# --------------------------------------------------------------------------- #
# C-2: the text face keeps the anti-vacuous companion numbers
# --------------------------------------------------------------------------- #
def test_text_output_prints_matched_and_inventory_units_next_to_the_empty_set(tmp_path):
    _build_repo(tmp_path)
    proc = _run("--action", "check", "--repo", str(tmp_path), "--format", "text")
    assert proc.returncode == 0, "clean fixture must exit 0; stderr=%r" % proc.stderr
    lowered = proc.stdout.lower()
    assert "matched" in lowered, (
        "text output MUST print `matched` beside the empty set (C-2); got %r"
        % proc.stdout
    )
    assert "inventory_units" in lowered, (
        "text output MUST print `inventory_units` beside the empty set (C-2); got %r"
        % proc.stdout
    )
    assert "78" in proc.stdout, (
        "both companion numbers are 78 on a clean fixture; got %r" % proc.stdout
    )


# --------------------------------------------------------------------------- #
# C-3 / C-14: the named non-green states
# --------------------------------------------------------------------------- #
def test_owner_unavailable_outranks_framework_source_required(tmp_path):
    payload = tmp_path / "payload"
    (payload / ".specify").mkdir(parents=True)
    proc, record = _check(payload)
    assert proc.returncode == 2
    assert record is not None
    assert record.get("findings") == []
    assert (record.get("error") or {}).get("label") == "owner-unavailable", (
        "a missing owner is `owner-unavailable` even on a payload root (C-3 / C-14); "
        "got %r" % (record.get("error"),)
    )
    assert record.get("red_kind") == "owner-unavailable", (
        "red_kind MUST name the highest-priority state (C-3); got %r"
        % record.get("red_kind")
    )


def test_payload_root_is_framework_source_required_for_check(tmp_path):
    payload = tmp_path / "project"
    _write(
        payload / ".specify" / OWNER_REL,
        _render_owner(_default_rows(2, 2), []),
    )
    proc, record = _check(payload)
    assert proc.returncode == 2, (
        "check on a payload root MUST exit 2 (C-14); got %d (findings=%r)"
        % (proc.returncode, None if record is None else record.get("findings"))
    )
    assert record is not None
    assert record.get("findings") == [], "a payload root must not produce findings (C-14)"
    assert (record.get("error") or {}).get("label") == "framework-source-required"
    assert record.get("red_kind") == "framework-source-required"

    # The same tree addressed through the payload directory itself.
    proc_direct, record_direct = _check(payload / ".specify")
    assert proc_direct.returncode == 2
    assert record_direct is not None
    assert record_direct.get("findings") == []


def test_payload_root_never_lands_in_the_parse_bucket(tmp_path):
    payload = tmp_path / "project"
    parseable_owner = _render_owner(_default_rows(2, 2), [])
    _write(payload / ".specify" / OWNER_REL, parseable_owner)
    proc, record = _check(payload)
    assert proc.returncode == 2
    assert record is not None
    assert (record.get("error") or {}).get("label") == "framework-source-required", (
        "a payload root is a named non-green state, not a parse failure or a gap "
        "(C-3 / C-14); got %r" % (record.get("error"),)
    )
    assert record.get("red_kind") == "framework-source-required"
    assert record.get("findings") == [], (
        "without the framework-source branch this tree would report unknown / "
        "inventory-truncated — the named state must replace them, not join them"
    )


def test_inventory_truncated_alone_never_lands_on_clean(tmp_path):
    rows = _default_rows(commands=26, skills=50)
    _build_repo(tmp_path, commands=26, skills=50, rows=rows)
    proc, record = _check(tmp_path)
    assert record is not None
    kinds = _kinds(record)
    assert kinds and set(kinds) == {"inventory-truncated"}, (
        "expected only inventory-truncated findings; got %r" % kinds
    )
    assert record.get("red_kind") == "parse-failure"
    assert proc.returncode == 1


# --------------------------------------------------------------------------- #
# fixture helpers that only this file needs
# --------------------------------------------------------------------------- #
def _unknown_row(name: str) -> dict:
    return {
        "unit_id": "skill:%s" % name,
        "flow_class": EXECUTION,
        "basis": "behavior-oracle",
        "neutral": "",
        "notes": "",
    }


def _mutate(rows: list[dict], index: int, **changes) -> list[dict]:
    mutated = [dict(row) for row in rows]
    mutated[index].update(changes)
    return mutated
