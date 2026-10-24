#!/usr/bin/env python3
"""Flow-class ledger engine (069a): reconcile the ledger and resolve a unit's class.

The single owner of the execution/expression classification is
``shared/definitions/flow-class-definitions.md``; this engine never restates the
criteria or the values' meaning. It only:

* ``--action check`` — scan the repository inventory (``templates/commands/*.md``
  and ``skills/{external,internal}/*/SKILL.md``), parse the owner's per-unit
  ledger, and report every defect as one of the eight contracted finding kinds
  (``missing`` / ``unknown`` / ``duplicate`` / ``dual-class`` / ``invalid-class`` /
  ``row-malformed`` / ``neutral-unlisted`` / ``inventory-truncated``);
* ``--action lookup --unit-id <id>`` — return the registered class for a unit, or
  the default class plus the fixed "undeclared, running on the default" marker for
  a well-formed but unregistered unit.

Both actions are read-only: no file is written or modified.

Exit codes (contract ``contracts/flow-class-ledger.md`` C-13):

* ``check``:  0 = zero findings, 1 = at least one finding, 2 = input/parse error
  (owner document missing, ledger section or header unparsable);
* ``lookup``: 0 = resolved (including the default degradation), 2 = malformed unit
  id or unparsable owner. An unparsable owner keeps the default class semantics,
  reports ``owner-unavailable`` on stderr and leaves ``marker`` null — the two
  degradation labels are mutually exclusive (requirements FR-009 / FR-016).

Usage::

    python3 scripts/python/flow-class-check.py --action check [--repo <root>] [--format text|json]
    python3 scripts/python/flow-class-check.py --action lookup --unit-id <id> [--repo <root>] [--format text|json]

The ledger is parsed by header name, never by column position; a row whose cell
count or required values do not fit the declared grammar is reported as
``row-malformed`` and excluded from the unit set (it is not re-classified as
missing/unknown/invalid-class).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# --------------------------------------------------------------------------- #
# Contract constants (literals are pinned copies of requirements.md § Shared Strings)
# --------------------------------------------------------------------------- #
CLASS_KEY = "flow_class"            # [[STR-003]]
EXECUTION = "execution"             # [[STR-001]]
EXPRESSION = "expression"           # [[STR-002]]
DEFAULT_CLASS = EXECUTION
DEFAULT_MARKER = "未声明·按默认"    # [[STR-004]]

CLASS_VALUES = (EXECUTION, EXPRESSION)
BASIS_VALUES = ("behavior-oracle", "reader-oracle", "mixed-oracle")
NEUTRAL_CATEGORIES = ("memory", "feedback", "evidence", "session")

# Anti-vacuous floors: measured constants (2026-10-24), never derived at runtime.
FLOOR_COMMANDS = 27
FLOOR_SKILLS = 51

OWNER_REL = Path("shared") / "definitions" / "flow-class-definitions.md"
MIRROR_DIR_NAME = ".specify"
COMMANDS_REL = Path("templates") / "commands"
SKILLS_REL = Path("skills")
SKILL_LAYERS = ("external", "internal")

LEDGER_SECTION_KEYWORD = "逐流程台账"
NEUTRAL_SECTION_KEYWORD = "类中立清单"
REQUIRED_LEDGER_COLUMNS = ("unit_id", CLASS_KEY, "basis", "neutral")
REQUIRED_NEUTRAL_COLUMNS = ("unit_id", "category", "rationale")

UNIT_ID_RE = re.compile(r"^(?:/speckit\.[a-z0-9][a-z0-9-]*|skill:[a-z0-9][a-z0-9-]*)$")
HEADING_RE = re.compile(r"^(#{1,6})\s")
SEPARATOR_CELL_RE = re.compile(r":?-{2,}:?")

FINDING_KINDS = (
    "missing",
    "unknown",
    "duplicate",
    "dual-class",
    "invalid-class",
    "row-malformed",
    "neutral-unlisted",
    "inventory-truncated",
)

DEGRADATION_LABEL = "owner-unavailable"


# --------------------------------------------------------------------------- #
# small helpers
# --------------------------------------------------------------------------- #
def find_repo_root() -> Path:
    """Resolve the repository root from this script's own location.

    The canonical copy lives at ``<root>/scripts/python/flow-class-check.py`` and
    its runtime mirror at ``<root>/.specify/scripts/python/flow-class-check.py``;
    walking up to the nearest ancestor that contains ``.specify/`` (skipping a
    parent that *is* ``.specify``) resolves both to the same root. A directory
    named ``.specify`` is never the project root — it is the payload mirror.
    """
    here = Path(__file__).resolve()
    parents = list(here.parents)
    for parent in parents:
        if parent.name != MIRROR_DIR_NAME and (parent / MIRROR_DIR_NAME).is_dir():
            return parent
    for parent in parents:
        if parent.name == MIRROR_DIR_NAME:
            return parent.parent
    return parents[2] if len(parents) > 2 else here.parent


def owner_candidates(repo: Path) -> list[Path]:
    """Every place the owner document may live, in resolution order.

    Two hats: the framework source keeps the owner at ``<root>/shared/…``, while a
    client project receives the same payload at ``<proj>/.specify/shared/…``
    (distribution contract C-3 row 1). ``--repo`` may name either the source root
    or the payload root itself, so both shapes are tried and the first hit wins;
    only when neither exists is the owner genuinely unavailable.
    """
    roots = [repo]
    if repo.name != MIRROR_DIR_NAME:
        roots.append(repo / MIRROR_DIR_NAME)
    return [root / OWNER_REL for root in roots]


def checked_at() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def cells(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def is_separator(row: list[str]) -> bool:
    return bool(row) and all(SEPARATOR_CELL_RE.fullmatch(cell) for cell in row)


def section_body(lines: list[str], keyword: str):
    """Return the body lines of the first heading containing ``keyword``.

    The body stops at the next heading of the same or a higher level, so a later
    section's table can never be mistaken for this section's table.
    """
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if not match or keyword not in line:
            continue
        level = len(match.group(1))
        body: list[str] = []
        for follow in lines[index + 1:]:
            follow_match = HEADING_RE.match(follow)
            if follow_match and len(follow_match.group(1)) <= level:
                break
            body.append(follow)
        return body
    return None


def first_table(lines: list[str]):
    """Return ``(header_cells, [(line_no, cells), ...])`` for the first table."""
    for index, line in enumerate(lines):
        if not line.lstrip().startswith("|"):
            continue
        if index + 1 >= len(lines) or not lines[index + 1].lstrip().startswith("|"):
            continue
        header = cells(line)
        if not is_separator(cells(lines[index + 1])):
            continue
        rows: list[tuple[int, list[str]]] = []
        cursor = index + 2
        while cursor < len(lines) and lines[cursor].lstrip().startswith("|"):
            row = cells(lines[cursor])
            if not is_separator(row):
                rows.append((cursor + 1, row))
            cursor += 1
        return header, rows
    return None


class OwnerError(Exception):
    """The owner document itself cannot be parsed (a C-13 exit-2 condition)."""


class OwnerLedger:
    def __init__(self, rows, malformed, neutral_units):
        self.rows = rows                  # list[dict] with a "_line" key
        self.malformed = malformed        # list[dict] {line, unit_id, message}
        self.neutral_units = neutral_units  # set[str]


# --------------------------------------------------------------------------- #
# owner parsing
# --------------------------------------------------------------------------- #
def parse_neutral_list(lines: list[str]) -> set[str]:
    """Parse the closed neutral list; a missing section/table yields an empty list.

    An unparsable neutral list is not an exit-2 condition — the checker then
    reports every ``neutral: yes`` row as ``neutral-unlisted`` rather than
    silently accepting the flag.
    """
    body = section_body(lines, NEUTRAL_SECTION_KEYWORD)
    if body is None:
        return set()
    table = first_table(body)
    if table is None:
        return set()
    header, rows = table
    names = [name for name in header]
    if any(column not in names for column in REQUIRED_NEUTRAL_COLUMNS):
        return set()
    index = {name: names.index(name) for name in names}
    units: set[str] = set()
    for _line_no, row in rows:
        if len(row) != len(names):
            continue
        record = {name: row[index[name]] for name in names}
        unit_id = record.get("unit_id", "")
        if not UNIT_ID_RE.fullmatch(unit_id):
            continue
        if record.get("category", "") not in NEUTRAL_CATEGORIES:
            continue
        if not record.get("rationale", "").strip():
            continue
        units.add(unit_id)
    return units


def parse_owner(repo: Path) -> OwnerLedger:
    candidates = owner_candidates(repo)
    owner_path = next((path for path in candidates if path.is_file()), None)
    if owner_path is None:
        raise OwnerError(
            "owner document unreadable: none of %s exists"
            % ", ".join(str(path) for path in candidates)
        )
    try:
        text = owner_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise OwnerError("owner document unreadable: %s (%s)" % (owner_path, exc))

    lines = text.splitlines()
    body = section_body(lines, LEDGER_SECTION_KEYWORD)
    if body is None:
        raise OwnerError(
            "owner document has no %r section" % LEDGER_SECTION_KEYWORD
        )
    table = first_table(body)
    if table is None:
        raise OwnerError(
            "owner section %r has no parseable Markdown table" % LEDGER_SECTION_KEYWORD
        )
    header, raw_rows = table
    names = [name for name in header]
    missing_columns = [c for c in REQUIRED_LEDGER_COLUMNS if c not in names]
    if missing_columns:
        raise OwnerError(
            "ledger header lacks required column(s): %s (header=%r)"
            % (", ".join(missing_columns), names)
        )
    index = {name: names.index(name) for name in names}

    rows: list[dict] = []
    malformed: list[dict] = []
    for line_no, row in raw_rows:
        if len(row) != len(names):
            malformed.append(
                {
                    "line": line_no,
                    "unit_id": _canonical_or_none(row[0] if row else ""),
                    "message": "row has %d cell(s) but the header declares %d"
                    % (len(row), len(names)),
                }
            )
            continue
        record = {name: row[index[name]] for name in names}
        problem = _row_problem(record)
        if problem:
            malformed.append(
                {
                    "line": line_no,
                    "unit_id": _canonical_or_none(record.get("unit_id", "")),
                    "message": problem,
                }
            )
            continue
        record["_line"] = line_no
        rows.append(record)

    return OwnerLedger(rows, malformed, parse_neutral_list(lines))


def _canonical_or_none(unit_id: str):
    unit_id = (unit_id or "").strip()
    return unit_id if UNIT_ID_RE.fullmatch(unit_id) else None


def _row_problem(record: dict):
    """Return a structural problem for one row, or ``None`` when it parses.

    Structural, not semantic: an out-of-domain class value is well formed (it is
    reported as ``invalid-class``), while an empty required value or a
    non-canonical unit id is ``row-malformed``.
    """
    unit_id = record.get("unit_id", "").strip()
    if not UNIT_ID_RE.fullmatch(unit_id):
        return "non-canonical unit id %r" % unit_id
    if not record.get(CLASS_KEY, "").strip():
        return "empty %s value" % CLASS_KEY
    if not record.get("basis", "").strip():
        return "empty basis value"
    if record.get("basis", "").strip() not in BASIS_VALUES:
        return "basis %r is outside the closed set %r" % (
            record.get("basis", "").strip(),
            BASIS_VALUES,
        )
    neutral = record.get("neutral", "").strip().lower()
    if neutral not in ("", "yes"):
        return "neutral %r is outside the closed set ''/yes" % record.get("neutral", "")
    return None


# --------------------------------------------------------------------------- #
# inventory
# --------------------------------------------------------------------------- #
class Inventory:
    def __init__(self, commands: set[str], skills: set[str]):
        self.commands = commands
        self.skills = skills

    @property
    def units(self) -> set[str]:
        return self.commands | self.skills


def scan_inventory(repo: Path) -> Inventory:
    commands: set[str] = set()
    commands_dir = repo / COMMANDS_REL
    if commands_dir.is_dir():
        for path in commands_dir.glob("*.md"):
            if path.is_file():
                commands.add("/speckit.%s" % path.stem)

    skills: set[str] = set()
    for layer in SKILL_LAYERS:
        layer_dir = repo / SKILLS_REL / layer
        if not layer_dir.is_dir():
            continue
        for path in layer_dir.glob("*/SKILL.md"):
            if path.is_file():
                skills.add("skill:%s" % path.parent.name)
    return Inventory(commands, skills)


# --------------------------------------------------------------------------- #
# findings
# --------------------------------------------------------------------------- #
def finding(kind: str, unit_id=None, message: str = "", line=None) -> dict:
    record = {"kind": kind, "unit_id": unit_id, "message": message}
    if line is not None:
        record["line"] = line
    return record


def reconcile(repo: Path, inventory: Inventory, ledger: OwnerLedger) -> list[dict]:
    findings: list[dict] = []

    for item in ledger.malformed:
        findings.append(
            finding(
                "row-malformed",
                item["unit_id"],
                message=item["message"],
                line=item["line"],
            )
        )

    grouped: dict[str, list[dict]] = {}
    for row in ledger.rows:
        unit_id = row["unit_id"]
        grouped.setdefault(unit_id, []).append(row)
        if row[CLASS_KEY] not in CLASS_VALUES:
            findings.append(
                finding(
                    "invalid-class",
                    unit_id,
                    message="%s value %r is outside the closed set %r"
                    % (CLASS_KEY, row[CLASS_KEY], CLASS_VALUES),
                    line=row["_line"],
                )
            )

    for unit_id, group in grouped.items():
        if len(group) < 2:
            continue
        values = {row[CLASS_KEY] for row in group if row[CLASS_KEY] in CLASS_VALUES}
        lines = [row["_line"] for row in group]
        if len(values) > 1:
            findings.append(
                finding(
                    "dual-class",
                    unit_id,
                    message="conflicting %s values %r on lines %r"
                    % (CLASS_KEY, sorted(values), lines),
                    line=lines[0],
                )
            )
        else:
            findings.append(
                finding(
                    "duplicate",
                    unit_id,
                    message="unit id appears on lines %r" % lines,
                    line=lines[0],
                )
            )

    reported_neutral: set[str] = set()
    for row in ledger.rows:
        unit_id = row["unit_id"]
        if row.get("neutral", "").strip().lower() != "yes":
            continue
        if unit_id in ledger.neutral_units or unit_id in reported_neutral:
            continue
        reported_neutral.add(unit_id)
        findings.append(
            finding(
                "neutral-unlisted",
                unit_id,
                message="neutral: yes outside the closed neutral list",
                line=row["_line"],
            )
        )

    ledger_units = set(grouped)
    inventory_units = inventory.units
    for unit_id in sorted(inventory_units - ledger_units):
        findings.append(
            finding("missing", unit_id, message="inventory unit has no ledger row")
        )
    for unit_id in sorted(ledger_units - inventory_units):
        findings.append(
            finding("unknown", unit_id, message="ledger unit is absent from the inventory")
        )

    if len(inventory.commands) < FLOOR_COMMANDS:
        findings.append(
            finding(
                "inventory-truncated",
                None,
                message="command inventory has %d unit(s), below the floor of %d"
                % (len(inventory.commands), FLOOR_COMMANDS),
            )
        )
    if len(inventory.skills) < FLOOR_SKILLS:
        findings.append(
            finding(
                "inventory-truncated",
                None,
                message="skill inventory has %d unit(s), below the floor of %d"
                % (len(inventory.skills), FLOOR_SKILLS),
            )
        )

    kinds_order = {kind: position for position, kind in enumerate(FINDING_KINDS)}
    findings.sort(
        key=lambda item: (
            kinds_order.get(item["kind"], len(FINDING_KINDS)),
            item.get("unit_id") or "",
            item.get("line") or 0,
        )
    )
    return findings


# --------------------------------------------------------------------------- #
# actions
# --------------------------------------------------------------------------- #
def render_check_text(record: dict) -> str:
    lines = [
        "flow-class check: %d unit(s) scanned, %d finding(s)"
        % (record["units"], len(record["findings"]))
    ]
    for item in record["findings"]:
        location = item.get("unit_id") or "-"
        if item.get("line"):
            location = "%s (line %d)" % (location, item["line"])
        lines.append("  [%s] %s — %s" % (item["kind"], location, item["message"]))
    return "\n".join(lines)


def action_check(repo: Path, output_format: str) -> int:
    stamp = checked_at()
    inventory = scan_inventory(repo)
    record = {
        "action": "check",
        "checked_at": stamp,
        "repo": str(repo),
        "units": len(inventory.units),
        "inventory": {
            "commands": len(inventory.commands),
            "skills": len(inventory.skills),
            "floors": {"commands": FLOOR_COMMANDS, "skills": FLOOR_SKILLS},
        },
        "findings": [],
        "error": None,
    }
    try:
        ledger = parse_owner(repo)
    except OwnerError as exc:
        record["error"] = {"label": DEGRADATION_LABEL, "detail": str(exc)}
        print("%s: %s" % (DEGRADATION_LABEL, exc), file=sys.stderr)
        if output_format == "json":
            print(json.dumps(record, ensure_ascii=False, indent=2))
        return 2

    record["findings"] = reconcile(repo, inventory, ledger)
    if output_format == "json":
        print(json.dumps(record, ensure_ascii=False, indent=2))
    else:
        print(render_check_text(record))
    return 1 if record["findings"] else 0


def render_lookup_text(record: dict) -> str:
    lines = [
        "unit_id: %s" % record["unit_id"],
        "%s: %s" % (CLASS_KEY, record[CLASS_KEY]),
        "source: %s" % record["source"],
        "marker: %s" % (record["marker"] if record["marker"] is not None else "null"),
        "basis: %s" % (record["basis"] if record["basis"] is not None else "null"),
        "neutral: %s" % ("true" if record["neutral"] else "false"),
    ]
    return "\n".join(lines)


def emit_lookup(record: dict, output_format: str) -> None:
    if output_format == "json":
        print(json.dumps(record, ensure_ascii=False, indent=2))
    else:
        print(render_lookup_text(record))


def owner_degradation(unit_id: str, stamp: str, detail: str, output_format: str) -> int:
    """Degrade to the default class with the one closed label, exit 2.

    Used when the owner parses but cannot yield a *decided* class for this unit: a
    value outside ``CLASS_VALUES``, a duplicated row, or two rows that disagree.
    The payload therefore never presents a corrupted or ambiguous value as
    ``source: ledger``; ``marker`` stays null because the fixed undeclared marker
    is reserved for "owner parsed, unit simply not registered" (C-7), and the two
    degradation labels stay mutually exclusive.
    """
    record = default_lookup_record(unit_id, stamp)
    record["error"] = {"label": DEGRADATION_LABEL, "detail": detail}
    print("%s: %s" % (DEGRADATION_LABEL, detail), file=sys.stderr)
    emit_lookup(record, output_format)
    return 2


def default_lookup_record(unit_id: str, stamp: str) -> dict:
    return {
        "action": "lookup",
        "checked_at": stamp,
        "unit_id": unit_id,
        CLASS_KEY: DEFAULT_CLASS,
        "source": "default",
        "marker": None,
        "basis": None,
        "neutral": False,
        "error": None,
    }


def action_lookup(repo: Path, unit_id: str, output_format: str) -> int:
    stamp = checked_at()
    if not UNIT_ID_RE.fullmatch(unit_id or ""):
        record = default_lookup_record(unit_id, stamp)
        record["error"] = {
            "label": "invalid-unit-id",
            "detail": "expected /speckit.<stem> or skill:<dir>",
        }
        print(
            "invalid unit id %r: expected /speckit.<stem> or skill:<dir>" % unit_id,
            file=sys.stderr,
        )
        emit_lookup(record, output_format)
        return 2

    try:
        ledger = parse_owner(repo)
    except OwnerError as exc:
        record = default_lookup_record(unit_id, stamp)
        record["error"] = {"label": DEGRADATION_LABEL, "detail": str(exc)}
        print("%s: %s" % (DEGRADATION_LABEL, exc), file=sys.stderr)
        emit_lookup(record, output_format)
        return 2

    matches = [row for row in ledger.rows if row["unit_id"] == unit_id]
    if not matches:
        record = default_lookup_record(unit_id, stamp)
        record["marker"] = DEFAULT_MARKER
        emit_lookup(record, output_format)
        return 0

    if len(matches) > 1:
        values = {row[CLASS_KEY] for row in matches}
        kind = "dual-class" if len(values) > 1 else "duplicate"
        return owner_degradation(
            unit_id,
            stamp,
            "%s: unit %r has %d ledger rows (lines %r, values %r) — a decided class "
            "is unavailable"
            % (kind, unit_id, len(matches), [row["_line"] for row in matches],
               sorted(values)),
            output_format,
        )

    row = matches[0]
    if row[CLASS_KEY] not in CLASS_VALUES:
        return owner_degradation(
            unit_id,
            stamp,
            "invalid-class: unit %r carries %r, outside the closed set %r"
            % (unit_id, row[CLASS_KEY], CLASS_VALUES),
            output_format,
        )

    record = {
        "action": "lookup",
        "checked_at": stamp,
        "unit_id": unit_id,
        CLASS_KEY: row[CLASS_KEY],
        "source": "ledger",
        "marker": None,
        "basis": row["basis"],
        "neutral": unit_id in ledger.neutral_units,
        "error": None,
    }
    emit_lookup(record, output_format)
    return 0


# --------------------------------------------------------------------------- #
# entry point
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="flow-class-check.py",
        description=(
            "Reconcile the flow-class ledger and resolve a unit's class "
            "(owner: shared/definitions/flow-class-definitions.md)."
        ),
    )
    parser.add_argument("--action", required=True, choices=("check", "lookup"))
    parser.add_argument(
        "--repo",
        default=None,
        help="repository root to inspect (default: resolved from this script)",
    )
    parser.add_argument("--unit-id", default=None, help="unit id for --action lookup")
    parser.add_argument("--format", default="text", choices=("text", "json"))
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    repo = Path(args.repo).expanduser().resolve() if args.repo else find_repo_root()
    if not repo.is_dir():
        print("repository root is not a directory: %s" % repo, file=sys.stderr)
        return 2

    if args.action == "lookup":
        if not args.unit_id:
            print("--action lookup requires --unit-id <id>", file=sys.stderr)
            return 2
        return action_lookup(repo, args.unit_id, args.format)
    return action_check(repo, args.format)


if __name__ == "__main__":
    sys.exit(main())
