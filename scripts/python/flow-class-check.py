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
* ``--action isomorphism`` — parse the owner's isomorphism map (8 stages x 3
  faces) and its four non-isomorphism boundaries, then judge the 24 cells, the
  truthfulness of every enforcement annotation against the gate owner's
  ``(stage, face, blocking)`` rows, the boundary-to-face bindings, the closed
  medium-axis phrases and the code-type operator floor (069b contract
  ``contracts/isomorphism-map.md``).

All actions are read-only: no file is written or modified.

Exit codes (contracts ``flow-class-ledger.md`` C-13 and ``isomorphism-map.md``
C-13):

* ``check``:  0 = zero findings, 1 = at least one finding, 2 = input/parse error
  (owner document missing, ledger section or header unparsable);
* ``lookup``: 0 = resolved (including the default degradation), 2 = malformed unit
  id or unparsable owner. An unparsable owner keeps the default class semantics,
  reports ``owner-unavailable`` on stderr and leaves ``marker`` null — the two
  degradation labels are mutually exclusive (requirements FR-009 / FR-016);
* ``isomorphism``: 0 = zero findings, 1 = at least one finding, 2 = input error
  (owner/map missing, roster unparsable ``roster-unavailable``, gate owner
  unparsable ``gate-owner-unavailable``, or a payload root
  ``framework-source-required``). A payload root emits zero findings and never a
  green verdict.

Usage::

    python3 scripts/python/flow-class-check.py --action check [--repo <root>] [--format text|json]
    python3 scripts/python/flow-class-check.py --action lookup --unit-id <id> [--repo <root>] [--format text|json]
    python3 scripts/python/flow-class-check.py --action isomorphism [--repo <root>] [--format text|json]

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
# 069b: isomorphism map action (contract contracts/isomorphism-map.md)
# --------------------------------------------------------------------------- #
GATES_OWNER_REL = Path("shared") / "workflow" / "expression-gates.md"
ROSTER_REL = Path("skills") / "external" / "sdd-loop-driver" / "scripts" / "loop-state.py"
MAP_SECTION_KEYWORD = "同构映射"
BOUNDARY_SECTION_KEYWORD = "不可同构边界"
FACE_SECTION_KEYWORD = "六面（封闭集）"
OPERATOR_SECTION_KEYWORD = "阶段算子表"

# Contract C-2 / C-8: the table headers, verbatim.
MAP_HEADER = (
    "阶段",
    "结构（实体 / 关系 / 边界）",
    "流程（阶段与门禁角色）",
    "逻辑（证据 / 契约 / 验收 / 版本 / 所有权）",
    "强制门禁",
    "强制状态",
)
BOUNDARY_HEADER = ("边界", "不可互换的判定面", "为什么不能互换", "门禁处理")

# Contract C-4: the status column is a closed two-value set.
ENFORCED = "已强制"
DECLARED_UNENFORCED = "已声明未强制"
STATUS_VALUES = (ENFORCED, DECLARED_UNENFORCED)

# Contract C-11 / C-12: the closed phrase sets (case-insensitive).
CODE_OPERATORS = ("pytest", "--cov", "coverage", "go test", "mvn test", "npm test", "jest")
MEDIUM_PHRASES = ("按扩展名", "by extension", ".md 即", ".yaml 即")

ROSTER_START_RE = re.compile(r"^STAGE_ARTIFACTS\s*=\s*\{")
ROSTER_KEY_RE = re.compile(r'^ {4}"([a-z][a-z0-9_-]*)"\s*:\s*\{')
GATE_SPLIT_RE = re.compile(r"[、,，/+\s]+")
GATE_RESIDUAL_RE = re.compile(r"[\s`、,，。；;：:/+\-—（）()\[\]]+")


class RosterError(Exception):
    """The stage roster owner cannot be parsed (a C-13 exit-2 condition)."""


class GateOwnerError(Exception):
    """The gate owner cannot be parsed (a C-13 exit-2 condition)."""


def resolve_shared(repo: Path, rel: Path):
    """Resolve a ``shared/``-relative path in the framework source, then its mirror."""
    for root in (repo, repo / MIRROR_DIR_NAME):
        path = root / rel
        if path.is_file():
            return path
    return None


def parse_roster(repo: Path) -> list[str]:
    """Return the ``STAGE_ARTIFACTS`` top-level keys, statically parsed.

    The roster is the *owner* of the stage set: this action MUST NOT fall back to
    a built-in eight-stage list, so an empty or missing assignment is an input
    error rather than a silent default.
    """
    path = repo / ROSTER_REL
    if not path.is_file():
        raise RosterError("stage roster owner missing: %s" % (repo / ROSTER_REL))
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        raise RosterError("stage roster owner unreadable: %s (%s)" % (path, exc))

    start = next((i for i, line in enumerate(lines) if ROSTER_START_RE.match(line)), None)
    if start is None:
        raise RosterError("STAGE_ARTIFACTS assignment not found in %s" % path)
    stages: list[str] = []
    for follow in lines[start + 1:]:
        if follow and not follow.startswith(" "):
            break
        match = ROSTER_KEY_RE.match(follow)
        if match:
            stages.append(match.group(1))
    if not stages:
        raise RosterError("STAGE_ARTIFACTS has no top-level stage keys in %s" % path)
    return stages


class GateOwner:
    def __init__(self, faces, operators):
        self.faces = faces          # list[str] in table order
        self.operators = operators  # list[dict] with stage / face / blocking / operator

    @property
    def blocking_pairs(self):
        return {
            (row["stage"], row["face"]) for row in self.operators if row["blocking"]
        }

    @property
    def blocking_stages(self):
        return {row["stage"] for row in self.operators if row["blocking"]}


def parse_gate_owner(repo: Path) -> GateOwner:
    path = resolve_shared(repo, GATES_OWNER_REL)
    if path is None:
        raise GateOwnerError("gate owner missing: %s" % (repo / GATES_OWNER_REL))
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        raise GateOwnerError("gate owner unreadable: %s (%s)" % (path, exc))

    face_body = section_body(lines, FACE_SECTION_KEYWORD)
    if face_body is None:
        raise GateOwnerError("gate owner has no %r section" % FACE_SECTION_KEYWORD)
    face_table = first_table(face_body)
    if face_table is None:
        raise GateOwnerError("gate owner § 六面 has no parseable table")
    face_header, face_rows = face_table
    if "face id" not in face_header:
        raise GateOwnerError("six-face table has no 'face id' column: %r" % (face_header,))
    face_index = face_header.index("face id")
    faces = [
        row[face_index].strip("` ")
        for _line, row in face_rows
        if len(row) == len(face_header) and row[face_index].strip("` ")
    ]
    if not faces:
        raise GateOwnerError("six-face table yielded no face ids")

    operator_body = section_body(lines, OPERATOR_SECTION_KEYWORD)
    if operator_body is None:
        raise GateOwnerError("gate owner has no %r section" % OPERATOR_SECTION_KEYWORD)
    operator_table = first_table(operator_body)
    if operator_table is None:
        raise GateOwnerError("gate owner § 阶段算子表 has no parseable table")
    op_header, op_rows = operator_table
    required = ("阶段", "执行算子", "对应面", "阻断级别")
    missing = [column for column in required if column not in op_header]
    if missing:
        raise GateOwnerError(
            "operator table lacks required column(s): %s (header=%r)"
            % (", ".join(missing), op_header)
        )
    operators = []
    for _line, row in op_rows:
        if len(row) != len(op_header):
            continue
        record = {column: row[op_header.index(column)] for column in required}
        operators.append(
            {
                "stage": record["阶段"].strip("` "),
                "face": record["对应面"].strip("` "),
                "blocking": record["阻断级别"].strip("` ").lower() == "blocking",
                "operator": record["执行算子"],
            }
        )
    return GateOwner(faces, operators)


def parse_isomorphism_map(repo: Path):
    """Return ``(map_rows, boundary_rows_or_None)``; raise ``OwnerError`` on shape loss.

    A missing/unparsable map *table* is an input error (the checker has no
    subject). A missing boundary table is a finding rather than an input error:
    C-8 names the defect (``boundary-missing``) and the checker can still report
    the map half.
    """
    owner_path = next((path for path in owner_candidates(repo) if path.is_file()), None)
    if owner_path is None:
        raise OwnerError(
            "owner document unreadable: none of %s exists"
            % ", ".join(str(path) for path in owner_candidates(repo))
        )
    try:
        lines = owner_path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        raise OwnerError("owner document unreadable: %s (%s)" % (owner_path, exc))

    map_body = section_body(lines, MAP_SECTION_KEYWORD)
    if map_body is None:
        raise OwnerError("owner document has no %r section" % MAP_SECTION_KEYWORD)
    map_table = first_table(map_body)
    if map_table is None:
        raise OwnerError("owner § 同构映射 has no parseable Markdown table")
    map_header, map_rows = map_table
    if tuple(map_header) != MAP_HEADER:
        raise OwnerError(
            "map header does not match contract C-2 verbatim: got %r" % (map_header,)
        )

    boundary_table = None
    boundary_body = section_body(lines, BOUNDARY_SECTION_KEYWORD)
    if boundary_body is not None:
        boundary_table = first_table(boundary_body)
    return map_rows, boundary_table


def iso_finding(kind: str, stage, message: str) -> dict:
    return {"kind": kind, "stage": stage, "message": message}


def gate_tokens(cell: str) -> list[str]:
    """Split a 强制门禁 cell into candidate tokens (backticks stripped)."""
    cleaned = cell.replace("`", " ")
    return [token for token in GATE_SPLIT_RE.split(cleaned) if token and token not in ("—", "-")]


def face_ids_in(text: str, faces) -> list[str]:
    found = []
    for face in sorted(faces, key=len, reverse=True):
        if re.search(r"(?<![a-z0-9-])%s(?![a-z0-9-])" % re.escape(face), text):
            found.append(face)
    return found


def cell_grammar_problem(cell: str):
    if cell.count("↔") != 1:
        return "expected exactly one '↔', found %d" % cell.count("↔")
    left, right = [part.strip() for part in cell.split("↔")]
    if not left.startswith("代码型："):
        return "left side does not start with '代码型：'"
    if not right.startswith("文档型："):
        return "right side does not start with '文档型：'"
    if len(left) < 8 or len(right) < 8:
        return "a side is shorter than 8 characters (left=%d, right=%d)" % (
            len(left),
            len(right),
        )
    return None


def medium_hits(cell: str) -> list[str]:
    normalized = re.sub(r"\s+", "", cell).lower()
    return [
        phrase
        for phrase in MEDIUM_PHRASES
        if re.sub(r"\s+", "", phrase).lower() in normalized
    ]


def check_map(rows, roster: list[str], gates: GateOwner) -> list[dict]:
    findings: list[dict] = []
    face_columns = MAP_HEADER[1:4]
    blocking_pairs = gates.blocking_pairs
    blocking_stages = gates.blocking_stages

    stages: list[str] = []
    for line_no, row in rows:
        if len(row) != len(MAP_HEADER):
            findings.append(
                iso_finding(
                    "cell-malformed",
                    row[0].strip("` ") if row else None,
                    "map row on line %d has %d cell(s), expected %d"
                    % (line_no, len(row), len(MAP_HEADER)),
                )
            )
            continue
        stage = row[0].strip("` ")
        stages.append(stage)

        for column in face_columns:
            cell = row[MAP_HEADER.index(column)]
            problem = cell_grammar_problem(cell)
            if problem:
                findings.append(
                    iso_finding(
                        "cell-malformed",
                        stage,
                        "%s cell on line %d: %s" % (column, line_no, problem),
                    )
                )

        status = row[MAP_HEADER.index("强制状态")].strip("` ")
        gate_cell = row[MAP_HEADER.index("强制门禁")]
        named = face_ids_in(gate_cell, gates.faces)
        candidates = gate_tokens(gate_cell)
        unknown = [token for token in candidates if token not in gates.faces]

        if status == ENFORCED:
            if not named:
                findings.append(
                    iso_finding(
                        "slogan-row",
                        stage,
                        "row claims enforcement but names no closed face id",
                    )
                )
            for face in unknown:
                findings.append(
                    iso_finding(
                        "gate-unknown",
                        stage,
                        "face id %r is outside the closed six-face set" % face,
                    )
                )
            for face in named:
                if (stage, face) not in blocking_pairs:
                    findings.append(
                        iso_finding(
                            "annotation-false-enforced",
                            stage,
                            "%r is claimed enforced but has no blocking operator at %r"
                            % (face, stage),
                        )
                    )
        elif status == DECLARED_UNENFORCED:
            if candidates:
                findings.append(
                    iso_finding(
                        "status-invalid",
                        stage,
                        "已声明未强制 must leave 强制门禁 empty, found %r" % (candidates,),
                    )
                )
            if stage in blocking_stages:
                findings.append(
                    iso_finding(
                        "annotation-false-unenforced",
                        stage,
                        "stage %r has blocking operator(s) but is declared unenforced" % stage,
                    )
                )
        elif status:
            findings.append(
                iso_finding(
                    "status-invalid",
                    stage,
                    "强制状态 %r is outside the closed set %r" % (status, STATUS_VALUES),
                )
            )
        else:
            findings.append(
                iso_finding(
                    "slogan-row",
                    stage,
                    "row carries neither a closed face id nor the 已声明未强制 annotation",
                )
            )

    if len(rows) != len(roster):
        findings.append(
            iso_finding(
                "stage-set-mismatch",
                None,
                "map has %d data row(s), the roster has %d stage(s)" % (len(rows), len(roster)),
            )
        )
    if len(stages) != len(set(stages)) or set(stages) != set(roster):
        findings.append(
            iso_finding(
                "stage-set-mismatch",
                None,
                "map stage set %r does not equal the roster keys %r"
                % (sorted(set(stages)), sorted(roster)),
            )
        )

    for _line_no, row in rows:
        if len(row) != len(MAP_HEADER):
            continue
        for column in face_columns:
            hits = medium_hits(row[MAP_HEADER.index(column)])
            if hits:
                findings.append(
                    iso_finding(
                        "medium-axis-in-map",
                        row[0].strip("` "),
                        "%s cell uses a medium-axis phrase as the classification reason: %r"
                        % (column, hits),
                    )
                )
    return findings


def check_boundaries(boundary_table, gates: GateOwner) -> list[dict]:
    findings: list[dict] = []
    if boundary_table is None:
        return [
            iso_finding(
                "boundary-missing",
                None,
                "owner has no § %s table; all four boundaries are absent"
                % BOUNDARY_SECTION_KEYWORD,
            )
        ]
    header, rows = boundary_table
    if tuple(header) != BOUNDARY_HEADER:
        findings.append(
            iso_finding(
                "boundary-malformed",
                None,
                "boundary header does not match contract C-8 verbatim: got %r" % (header,),
            )
        )

    def column(name: str) -> int:
        return header.index(name) if name in header else BOUNDARY_HEADER.index(name)

    seen: list[str] = []
    for line_no, row in rows:
        if len(row) != len(BOUNDARY_HEADER):
            findings.append(
                iso_finding(
                    "boundary-malformed",
                    None,
                    "boundary row on line %d has %d cell(s), expected %d"
                    % (line_no, len(row), len(BOUNDARY_HEADER)),
                )
            )
            continue
        boundary = row[0].strip("` ")
        if boundary not in ("a", "b", "c", "d"):
            findings.append(
                iso_finding(
                    "boundary-missing",
                    None,
                    "unknown boundary id %r on line %d" % (boundary, line_no),
                )
            )
            continue
        seen.append(boundary)

        reason = row[column("为什么不能互换")].strip()
        if not reason:
            findings.append(
                iso_finding(
                    "boundary-malformed",
                    None,
                    "boundary %r has an empty 为什么不能互换 cell" % boundary,
                )
            )

        handling = row[column("门禁处理")].strip()
        named = face_ids_in(handling, gates.faces)
        if not named:
            findings.append(
                iso_finding(
                    "boundary-unbound",
                    None,
                    "boundary %r names no closed face id in 门禁处理" % boundary,
                )
            )
        else:
            residual = handling
            for face in named:
                residual = residual.replace(face, "")
            if len(GATE_RESIDUAL_RE.sub("", residual)) < 4:
                findings.append(
                    iso_finding(
                        "boundary-malformed",
                        None,
                        "boundary %r lists face id(s) but no handling explanation" % boundary,
                    )
                )

    for boundary in ("a", "b", "c", "d"):
        count = seen.count(boundary)
        if count == 0:
            findings.append(
                iso_finding("boundary-missing", None, "boundary %r is missing" % boundary)
            )
        elif count > 1:
            findings.append(
                iso_finding(
                    "boundary-missing",
                    None,
                    "boundary %r appears %d times" % (boundary, count),
                )
            )
    return findings


def check_code_operators(gates: GateOwner) -> list[dict]:
    findings: list[dict] = []
    for row in gates.operators:
        lowered = row["operator"].lower()
        for token in CODE_OPERATORS:
            if token in lowered:
                findings.append(
                    iso_finding(
                        "code-operator-in-expression-gates",
                        row["stage"],
                        "执行算子 carries the code-type operator %r: %r"
                        % (token, row["operator"]),
                    )
                )
                break
    return findings


def render_isomorphism_text(record: dict) -> str:
    lines = [
        "flow-class isomorphism: %d stage row(s), %d gate face(s), %d finding(s)"
        % (record["stages"], record["gates"], len(record["findings"]))
    ]
    for item in record["findings"]:
        location = item.get("stage") or "-"
        lines.append("  [%s] %s — %s" % (item["kind"], location, item["message"]))
    return "\n".join(lines)


def emit_isomorphism(record: dict, output_format: str, code: int) -> int:
    if output_format == "json":
        print(json.dumps(record, ensure_ascii=False, indent=2))
    else:
        if record["error"]:
            print("%s: %s" % (record["error"]["label"], record["error"]["detail"]))
        else:
            print(render_isomorphism_text(record))
    return code


def isomorphism_input_error(record: dict, label: str, detail: str, output_format: str) -> int:
    record["error"] = {"label": label, "detail": detail}
    print("%s: %s" % (label, detail), file=sys.stderr)
    return emit_isomorphism(record, output_format, 2)


def action_isomorphism(repo: Path, output_format: str) -> int:
    record = {
        "action": "isomorphism",
        "checked_at": checked_at(),
        "repo": str(repo),
        "stages": 0,
        "gates": 0,
        "findings": [],
        "error": None,
    }

    # C-13: this action only runs in a framework source tree. A payload root
    # (client `.specify/` shape) is an input error, never a green verdict.
    if not is_framework_source(repo):
        return isomorphism_input_error(
            record,
            "framework-source-required",
            "neither templates/commands/ nor a parseable skills/{external,internal}/ is present in %s"
            % repo,
            output_format,
        )

    try:
        roster = parse_roster(repo)
    except RosterError as exc:
        return isomorphism_input_error(record, "roster-unavailable", str(exc), output_format)

    try:
        gates = parse_gate_owner(repo)
    except GateOwnerError as exc:
        return isomorphism_input_error(
            record, "gate-owner-unavailable", str(exc), output_format
        )

    try:
        map_rows, boundary_table = parse_isomorphism_map(repo)
    except OwnerError as exc:
        return isomorphism_input_error(record, DEGRADATION_LABEL, str(exc), output_format)

    record["stages"] = len(map_rows)
    record["gates"] = len(gates.faces)

    findings: list[dict] = []
    findings.extend(check_map(map_rows, roster, gates))
    findings.extend(check_boundaries(boundary_table, gates))
    findings.extend(check_code_operators(gates))
    record["findings"] = findings
    return emit_isomorphism(record, output_format, 1 if findings else 0)


def is_framework_source(repo: Path) -> bool:
    if (repo / COMMANDS_REL).is_dir():
        return True
    for layer in SKILL_LAYERS:
        layer_dir = repo / SKILLS_REL / layer
        if layer_dir.is_dir() and any(layer_dir.glob("*/SKILL.md")):
            return True
    return False


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
    parser.add_argument(
        "--action", required=True, choices=("check", "lookup", "isomorphism")
    )
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
    if args.action == "isomorphism":
        return action_isomorphism(repo, args.format)
    return action_check(repo, args.format)


if __name__ == "__main__":
    sys.exit(main())
