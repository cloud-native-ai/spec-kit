"""Contract tests for the flow-class owner and ledger (069a, T004).

Owns the owner/ledger assertions of
``.specify/specs/069a-flow-classification-docs-gates/contracts/flow-class-ledger.md``
that ``tasks.md`` T004 names:

* C-1  the single owner exists, declares ownership up front, and carries the
       required sections (criteria / boundary examples / namespace / ledger /
       neutral list / change log); no second classification data file exists
       (Markdown ledger rows, YAML/JSON data, code constants).
* C-3  the binary values are the only two, keyed by the namespaced class key.
* C-4  the ledger is a Markdown table with 78 rows, the class key verbatim in the
       header, and only the two values in the class column.
* C-5  the ledger unit set equals the repository inventory in both directions
       (27 command templates + 51 skills).
* C-6  the ledger never repeats a unit id.
* C-7  ``lookup`` marks an unregistered unit as default + fixed marker, and a
       registered one as ledger-sourced with ``marker=null``.
* C-8  the closed neutral list is consistent with the ledger's ``neutral: yes``
       subset (both directions) and carries a rationale per entry.
* C-9  command templates and skills never assign the class key and never carry a
       ledger-style row.
* C-12 the change log keeps the ``date | unit_id | before → after | basis | 依据``
       row form.
* C-13 ``check`` reports 78 units and zero findings on this repository.

Red-first discipline (Constitution IV): the owner document and the engine do not
exist yet. Every engine call goes through ``_run``, which asserts the script path
first, so a red is "artifact missing / behaviour wrong", never an import or
collection error. Shared-string literals below are pinned copies of
``requirements.md`` § Shared Strings — a legitimate drift-detection duplicate under
``.specify/shared/guidelines/one-source-of-truth.md``.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OWNER = REPO_ROOT / "shared" / "definitions" / "flow-class-definitions.md"
ENGINE = REPO_ROOT / "scripts" / "python" / "flow-class-check.py"
COMMANDS_DIR = REPO_ROOT / "templates" / "commands"
SKILLS_DIR = REPO_ROOT / "skills"

# requirements.md § Shared Strings (pinned copies).
STR_001 = "execution"
STR_002 = "expression"
STR_003 = "flow_class"
STR_004 = "未声明·按默认"

CLASS_VALUES = (STR_001, STR_002)
BASIS_VALUES = ("behavior-oracle", "reader-oracle", "mixed-oracle")
NEUTRAL_CATEGORIES = ("memory", "feedback", "evidence", "session")
ISO_Z_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
UNIT_ID_RE = re.compile(r"^(?:/speckit\.[a-z0-9][a-z0-9-]*|skill:[a-z0-9][a-z0-9-]*)$")
# A Markdown row shaped like a ledger entry: unit id in the first cell, a class
# value in the next one. The second classification-data detector for prose docs.
LEDGER_SHAPED_ROW_RE = re.compile(
    r"^\s*\|\s*`?(?:/speckit\.[a-z0-9-]+|skill:[a-z0-9-]+)`?\s*\|\s*"
    r"(?:%s|%s)\s*\|" % (STR_001, STR_002)
)
# A code constant mapping the class key to one of the two values.
CODE_CLASS_CONST_RE = re.compile(
    r"""flow_class["']?\s*[:=]\s*["']?(?:%s|%s)\b""" % (STR_001, STR_002)
)


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _read_owner() -> str:
    assert OWNER.is_file(), (
        "flow-class owner missing: %s — expected at T007/T008 (069a). "
        "Red is the intended pre-implementation state for T004."
        % OWNER.relative_to(REPO_ROOT)
    )
    return OWNER.read_text(encoding="utf-8")


def _run(*args: str) -> subprocess.CompletedProcess:
    assert ENGINE.is_file(), (
        "flow-class engine missing: %s — expected at T009/T010 (069a). "
        "Red is the intended pre-implementation state for T004."
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
        "expected a JSON document on stdout, got empty output "
        "(stderr: %r)" % proc.stderr
    )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(
            "stdout is not JSON (%s); head=%r" % (exc, proc.stdout[:400])
        ) from exc


def _cells(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def _is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", cell) for cell in cells)


def _first_table(lines: list[str]) -> tuple[list[str], list[tuple[int, list[str]]]]:
    for index, line in enumerate(lines):
        if not line.lstrip().startswith("|"):
            continue
        if index + 1 >= len(lines) or not lines[index + 1].lstrip().startswith("|"):
            continue
        header = _cells(line)
        if not _is_separator(_cells(lines[index + 1])):
            continue
        rows: list[tuple[int, list[str]]] = []
        cursor = index + 2
        while cursor < len(lines) and lines[cursor].lstrip().startswith("|"):
            cells = _cells(lines[cursor])
            if not _is_separator(cells):
                rows.append((cursor + 1, cells))
            cursor += 1
        return header, rows
    raise AssertionError("no Markdown table found where one is required")


def _table_under(text: str, heading_keyword: str):
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if re.match(r"^#{1,6}\s", line) and heading_keyword in line:
            try:
                return _first_table(lines[index + 1:])
            except AssertionError as exc:
                raise AssertionError(
                    "section %r has no parseable Markdown table" % heading_keyword
                ) from exc
    raise AssertionError(
        "owner document has no heading containing %r; headings are: %r"
        % (heading_keyword, [ln for ln in lines if re.match(r"^#{1,6}\s", ln)])
    )


def _ledger_rows() -> list[dict]:
    header, rows = _table_under(_read_owner(), "逐流程台账")
    names = [cell.strip() for cell in header]
    for required in ("unit_id", STR_003, "basis", "neutral"):
        assert required in names, (
            "ledger header must carry %r verbatim; header=%r" % (required, names)
        )
    index = {name: names.index(name) for name in names}
    parsed: list[dict] = []
    for line_no, cells in rows:
        assert len(cells) == len(names), (
            "ledger row %d has %d cells but the header has %d: %r"
            % (line_no, len(cells), len(names), cells)
        )
        record = {name: cells[index[name]] for name in names}
        record["_line"] = line_no
        parsed.append(record)
    return parsed


def _inventory() -> tuple[set[str], set[str]]:
    commands = {
        "/speckit.%s" % path.stem for path in COMMANDS_DIR.glob("*.md") if path.is_file()
    }
    skills = {
        "skill:%s" % path.parent.name
        for layer in ("external", "internal")
        for path in (SKILLS_DIR / layer).glob("*/SKILL.md")
        if path.is_file()
    }
    return commands, skills


def _tracked_files() -> list[str]:
    proc = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, "git ls-files failed: %r" % proc.stderr
    return [entry for entry in proc.stdout.split("\0") if entry]


def _diff(actual: set[str], expected: set[str]) -> str:
    return "only-in-ledger=%r only-in-inventory=%r" % (
        sorted(actual - expected),
        sorted(expected - actual),
    )


# --------------------------------------------------------------------------- #
# C-1 — the single owner, its declared sections, and no second data file
# --------------------------------------------------------------------------- #
def test_owner_exists_and_declares_required_sections():
    text = _read_owner()
    head = "\n".join(text.splitlines()[:40])
    assert "唯一所有者" in head, (
        "owner must declare itself the single owner in its opening lines; head=%r"
        % head[:400]
    )
    for keyword in ("判据", "边界例", "命名空间", "逐流程台账", "类中立", "变更记录"):
        assert any(
            re.match(r"^#{1,6}\s", line) and keyword in line
            for line in text.splitlines()
        ), "owner lacks a section heading containing %r" % keyword


def test_no_second_classification_data_file():
    owner_rel = OWNER.relative_to(REPO_ROOT).as_posix()
    engine_rel = ENGINE.relative_to(REPO_ROOT).as_posix()
    problems: list[str] = []
    for rel in _tracked_files():
        if rel in (owner_rel, engine_rel):
            continue
        if rel.startswith(".specify/") or rel.startswith("tests/"):
            # .specify/ = generated mirrors + spec artifacts; tests/ holds the
            # pinned literal copies this repository deliberately keeps.
            continue
        path = REPO_ROOT / rel
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix not in (".md", ".json", ".yaml", ".yml", ".py", ".js", ".mjs", ".cjs", ".ts"):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if suffix in (".json", ".yaml", ".yml"):
            if STR_003 in text:
                problems.append("%s: data file mentions the class key %r" % (rel, STR_003))
            continue
        if suffix in (".py", ".js", ".mjs", ".cjs", ".ts"):
            if CODE_CLASS_CONST_RE.search(text):
                problems.append("%s: code constant maps %r to a class value" % (rel, STR_003))
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            if LEDGER_SHAPED_ROW_RE.match(line):
                problems.append(
                    "%s:%d: ledger-shaped row outside the owner (%r)"
                    % (rel, line_no, line.strip()[:120])
                )
    assert not problems, (
        "a second classification data source exists — the owner must stay the only "
        "place declaring unit -> class:\n  " + "\n  ".join(problems)
    )


# --------------------------------------------------------------------------- #
# C-4 / C-5 / C-6 — ledger shape, cardinality, and bidirectional coverage
# --------------------------------------------------------------------------- #
def test_ledger_has_78_rows_covering_inventory_bidirectionally():
    rows = _ledger_rows()
    assert len(rows) == 78, (
        "ledger must carry exactly 78 rows (27 commands + 51 skills); got %d" % len(rows)
    )
    ids = [row["unit_id"] for row in rows]
    assert len(set(ids)) == len(ids), (
        "ledger repeats a unit id (C-6 duplicate): %r"
        % sorted({unit for unit in ids if ids.count(unit) > 1})
    )
    for row in rows:
        assert UNIT_ID_RE.fullmatch(row["unit_id"]), (
            "ledger row %d has a non-canonical unit id %r"
            % (row["_line"], row["unit_id"])
        )
    commands = {unit for unit in ids if unit.startswith("/speckit.")}
    skills = {unit for unit in ids if unit.startswith("skill:")}
    assert len(commands) == 27, "expected 27 command units, got %d" % len(commands)
    assert len(skills) == 51, "expected 51 skill units, got %d" % len(skills)
    inventory_commands, inventory_skills = _inventory()
    assert len(inventory_commands) == 27, (
        "inventory self-check: expected 27 templates/commands/*.md, got %d"
        % len(inventory_commands)
    )
    assert len(inventory_skills) == 51, (
        "inventory self-check: expected 51 skills/{external,internal}/*/SKILL.md, got %d"
        % len(inventory_skills)
    )
    expected = inventory_commands | inventory_skills
    assert set(ids) == expected, (
        "ledger unit set and repository inventory must be equal: " + _diff(set(ids), expected)
    )


def test_ledger_values_are_binary_and_basis_is_closed():
    rows = _ledger_rows()
    for row in rows:
        assert row[STR_003] in CLASS_VALUES, (
            "ledger row %d (%s) has an out-of-domain class %r; allowed=%r"
            % (row["_line"], row["unit_id"], row[STR_003], CLASS_VALUES)
        )
        assert row["basis"] in BASIS_VALUES, (
            "ledger row %d (%s) has an out-of-domain basis %r; allowed=%r"
            % (row["_line"], row["unit_id"], row["basis"], BASIS_VALUES)
        )
        assert row["neutral"].lower() in ("", "yes"), (
            "ledger row %d (%s) has an out-of-domain neutral cell %r; allowed='' or 'yes'"
            % (row["_line"], row["unit_id"], row["neutral"])
        )
    observed = {row[STR_003] for row in rows}
    assert observed == set(CLASS_VALUES), (
        "the ledger must exercise exactly the two class values; observed=%r" % sorted(observed)
    )


def test_first_batch_members_are_registered_as_expression():
    by_id = {row["unit_id"]: row for row in _ledger_rows()}
    for unit in ("/speckit.docs", "/speckit.humanize"):
        assert unit in by_id, "first-batch member %r is not registered in the ledger" % unit
        assert by_id[unit][STR_003] == STR_002, (
            "first-batch member %r must be registered as %r; got %r"
            % (unit, STR_002, by_id[unit][STR_003])
        )


def test_check_reports_78_units_and_zero_gaps():
    # No --repo: C-5 requires the engine to resolve the repository root itself.
    proc = _run("--action", "check", "--format", "json")
    record = _json(proc)
    assert proc.returncode == 0, (
        "check must exit 0 on a gap-free ledger; findings=%r stderr=%r"
        % (record.get("findings"), proc.stderr)
    )
    assert record.get("action") == "check"
    assert record.get("findings") == []
    assert record.get("units") == 78, (
        "check must report 78 scanned units; got %r" % record.get("units")
    )
    assert ISO_Z_RE.match(str(record.get("checked_at", ""))), (
        "checked_at must be ISO-8601 Z; got %r" % record.get("checked_at")
    )


# --------------------------------------------------------------------------- #
# C-7 — lookup: default + marker vs ledger + null marker
# --------------------------------------------------------------------------- #
def test_lookup_unregistered_unit_returns_default_with_marker():
    for unit in ("/speckit.no-such-flow", "skill:no-such-flow"):
        proc = _run("--action", "lookup", "--unit-id", unit, "--format", "json")
        assert proc.returncode == 0, (
            "lookup of a well-formed but unregistered unit must exit 0 (it must not "
            "interrupt a flow); unit=%r stderr=%r" % (unit, proc.stderr)
        )
        record = _json(proc)
        assert record.get("unit_id") == unit
        assert record.get(STR_003) == STR_001, (
            "an unregistered unit must fall back to %r; got %r"
            % (STR_001, record.get(STR_003))
        )
        assert record.get("source") == "default", (
            "an unregistered unit must report source='default'; got %r"
            % record.get("source")
        )
        assert record.get("marker") == STR_004, (
            "an unregistered unit must carry the fixed default marker %r; got %r"
            % (STR_004, record.get("marker"))
        )
        assert record.get("basis") is None, (
            "an unregistered unit has no oracle basis; got %r" % record.get("basis")
        )
        assert record.get("neutral") is False
        for label in ("owner-unavailable", "owner-unparsable"):
            assert label not in proc.stderr, (
                "the unregistered path must not emit the owner-degradation label %r "
                "(the two labels are mutually exclusive)" % label
            )


def test_lookup_registered_unit_returns_ledger_source_without_marker():
    proc = _run("--action", "lookup", "--unit-id", "/speckit.docs", "--format", "json")
    assert proc.returncode == 0, proc.stderr
    record = _json(proc)
    assert record.get("unit_id") == "/speckit.docs"
    assert record.get(STR_003) == STR_002
    assert record.get("source") == "ledger", (
        "a registered unit must not be presented as default; got %r"
        % record.get("source")
    )
    assert record.get("marker") is None, (
        "a registered unit must not carry the default marker; got %r"
        % record.get("marker")
    )
    assert record.get("basis") in BASIS_VALUES, (
        "a registered unit must expose its oracle basis; got %r" % record.get("basis")
    )
    assert record.get("neutral") is False


# --------------------------------------------------------------------------- #
# C-8 — the neutral list is a closed subset of the ledger
# --------------------------------------------------------------------------- #
def test_neutral_list_is_closed_against_ledger():
    header, table_rows = _table_under(_read_owner(), "类中立清单")
    names = [cell.strip() for cell in header]
    for required in ("unit_id", "category", "rationale"):
        assert required in names, (
            "neutral-list header must carry %r; header=%r" % (required, names)
        )
    index = {name: names.index(name) for name in names}
    listed: list[str] = []
    for line_no, cells in table_rows:
        assert len(cells) == len(names), (
            "neutral-list row %d has %d cells, header has %d" % (line_no, len(cells), len(names))
        )
        record = {name: cells[index[name]] for name in names}
        assert record["category"] in NEUTRAL_CATEGORIES, (
            "neutral-list row %d has an out-of-domain category %r; allowed=%r"
            % (line_no, record["category"], NEUTRAL_CATEGORIES)
        )
        assert record["rationale"].strip(), (
            "neutral-list row %d (%s) lacks a rationale" % (line_no, record["unit_id"])
        )
        listed.append(record["unit_id"])
    assert listed, "the neutral list must register at least one carrier skill"
    assert len(set(listed)) == len(listed), "the neutral list repeats an entry: %r" % listed
    ledger = {row["unit_id"]: row for row in _ledger_rows()}
    for unit in listed:
        assert unit in ledger, (
            "neutral-list unit %r is absent from the ledger (list must be a subset)" % unit
        )
        assert ledger[unit]["neutral"].lower() == "yes", (
            "neutral-list unit %r is not flagged neutral: yes in the ledger" % unit
        )
    flagged = {unit for unit, row in ledger.items() if row["neutral"].lower() == "yes"}
    assert flagged <= set(listed), (
        "ledger rows flagged neutral: yes must all be listed (closed set); unlisted=%r"
        % sorted(flagged - set(listed))
    )
    _, inventory_skills = _inventory()
    assert set(listed) <= inventory_skills, (
        "neutral-list units must exist in the skill inventory; missing=%r"
        % sorted(set(listed) - inventory_skills)
    )


# --------------------------------------------------------------------------- #
# C-12 — change-log row form
# --------------------------------------------------------------------------- #
def test_change_log_row_form():
    header, table_rows = _table_under(_read_owner(), "变更记录")
    normalized = [
        re.sub(r"\s*->\s*", " → ", " ".join(cell.split())) for cell in header
    ]
    assert normalized == ["date", "unit_id", "before → after", "basis", "依据"], (
        "change-log header must be 'date | unit_id | before → after | basis | 依据'; got %r"
        % normalized
    )
    for line_no, cells in table_rows:
        assert len(cells) == 5, (
            "change-log row %d must have 5 cells; got %r" % (line_no, cells)
        )
        date, unit, change, basis, authority = cells
        assert DATE_RE.match(date), "change-log row %d has a malformed date %r" % (line_no, date)
        assert UNIT_ID_RE.match(unit), (
            "change-log row %d has a non-canonical unit id %r" % (line_no, unit)
        )
        transition = re.fullmatch(r"\s*(\S+)\s*(?:→|->)\s*(\S+)\s*", change)
        assert transition, (
            "change-log row %d must read 'before → after'; got %r" % (line_no, change)
        )
        assert transition.group(1) in CLASS_VALUES and transition.group(2) in CLASS_VALUES, (
            "change-log row %d transitions outside the two class values: %r" % (line_no, change)
        )
        assert basis in BASIS_VALUES, (
            "change-log row %d has an out-of-domain basis %r" % (line_no, basis)
        )
        assert authority.strip(), (
            "change-log row %d lacks the 依据 (evidence) cell" % line_no
        )


# --------------------------------------------------------------------------- #
# C-9 — no class-key assignment in templates or skills (wiring reads the owner)
# --------------------------------------------------------------------------- #
def test_templates_and_skills_never_assign_class_key():
    paths = sorted(COMMANDS_DIR.glob("*.md")) + sorted(SKILLS_DIR.glob("*/*/SKILL.md"))
    assert len(paths) == 78, (
        "expected 27 templates + 51 skills, got %d files" % len(paths)
    )
    problems: list[str] = []
    for path in paths:
        rel = path.relative_to(REPO_ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        for match in CODE_CLASS_CONST_RE.finditer(text):
            line_no = text.count("\n", 0, match.start()) + 1
            problems.append(
                "%s:%d: class-key assignment %r" % (rel, line_no, match.group(0))
            )
        for line_no, line in enumerate(text.splitlines(), start=1):
            if LEDGER_SHAPED_ROW_RE.match(line):
                problems.append(
                    "%s:%d: ledger-shaped row %r" % (rel, line_no, line.strip()[:120])
                )
    assert not problems, (
        "templates/skills must read the class from the owner at runtime, never "
        "carry a class-key assignment or a ledger row:\n  " + "\n  ".join(problems)
    )
