#!/usr/bin/env python3
"""Context-management audit engine (Feature 110): one read-only entry, two actions.

Owner of the meanings: `shared/definitions/context-management-definitions.md`.
Owner of the machine value domains: the four `shared/declarations/facts/context-*.yaml`
facts, read through `scripts/python/declaration_reader.py` (`load_fact`) — this engine
carries no second YAML parser and no hard-coded domain member.

Actions
-------
`--action manifest --layer <layer>` prints one layer's rows in roster order: class id,
layer, form, resolved source(s), presence token and reason (on absence) and the cap
reference. The row set is `context-classes.yaml` (the roster), never the current layout
rows: a roster class whose layout row is missing still prints, its form / source(s) / cap
fields reading `—` and its token `not-evaluated` with the reason naming the missing row.
The JSON face carries the ordered keys `action`, `layer`, `rows` (each `class`, `layer`,
`form`, `sources`, `token`, `reason`, `cap`), `counts`, `source_reading`. The text face
prints one line per row and ends with one `source-reading: <digest>` line over the
`(class id, declared source, presence token, size-or-entry-count, mtime_ns)` tuples of the
printed layer (content bytes never enter it; unresolved sources use the -1/-2 sentinels,
runtime-discovery rows the 0/0 pair, a missing-layout row the -3/-3 pair).

`--action check` is the layout-integrity reading; its closed nine-rule set lands with its
own task row. Until then the action refuses loudly (exit 2) instead of reporting a green
it cannot support.

Read-only: no file, directory or cache is written and no socket is opened. The only
content reads are the declared inputs (the owner document and the four facts) and the
`--version` identity source; audited sources are consumed as paths and metadata only.

Usage:
  python3 scripts/python/context-audit.py --action check [--workspace-root PATH] [--json]
  python3 scripts/python/context-audit.py --action manifest --layer <layer> [--workspace-root PATH] [--json]

Exit codes: 0 clean or manifest emitted; 1 integrity findings; 2 usage, unreadable input
or an unknown or missing declaration member.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import sys
from pathlib import Path

OWNER_DOC_PARTS = ("shared", "definitions", "context-management-definitions.md")
MIRROR_DIR = ".specify"
FACT_SLUGS = ("context-categories", "context-layers", "context-forms", "context-classes")
LAYOUT_COLUMNS = ("class id", "layer", "form", "source", "owner", "cap reference")
FORMS_COLUMNS = ("form", "legal layers")
PROBE_PREFIX = "runtime-discovery:"
ACTION_NAMES = ("check", "manifest")
PRESENCE_TOKENS = ("present", "absent", "unreachable", "empty", "not-evaluated")
PRESENT_TOKEN = "present"
ABSENT_TOKEN = "absent"
UNREACHABLE_TOKEN = "unreachable"
EMPTY_TOKEN = "empty"
NOT_EVALUATED_TOKEN = "not-evaluated"
UNDECLARED_CELL = "—"
SENTINEL_MISSING_SIZE = -1
SENTINEL_UNREADABLE_SIZE = -2
SENTINEL_MISSING_ROW_SIZE = -3
EXIT_OK = 0
EXIT_FINDINGS = 1
EXIT_INPUT = 2

_ENGINE_DIR = Path(__file__).resolve().parent
if str(_ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(_ENGINE_DIR))

try:  # the shared reader owns the declaration layer's one parser
    import declaration_reader
except Exception:  # a sandbox copy may carry the engine without the helper
    declaration_reader = None

try:  # the house script-interface helper owns the version source and the help labels
    from script_interface_cli import VersionAction, configure_parser, guard_argv
except Exception:  # same sandbox case: the engine still runs its actions
    VersionAction = None

    def configure_parser(parser, **_kwargs):
        return parser

    def guard_argv(_argv=None, declared=None, **_kwargs):
        return None


class InputError(Exception):
    """An unreadable input: rendered to stderr and mapped to exit 2, never a partial verdict."""


# --------------------------------------------------------------------------- #
# small helpers
# --------------------------------------------------------------------------- #
def _normalize_cell(cell: str) -> str:
    value = cell.strip()
    while len(value) >= 2 and value.startswith("`") and value.endswith("`"):
        value = value[1:-1].strip()
    return value


def _split_row(line: str) -> list:
    inner = line.strip()[1:-1]
    return [_normalize_cell(cell) for cell in inner.split("|")]


def _is_separator(cells: list) -> bool:
    return bool(cells) and all(set(cell) <= set("-: ") for cell in cells)


def _first_table(text: str, heading: str):
    """The first pipe table under ``## <heading>`` as (header, rows, line numbers).

    Returns ``(None, [], [])`` when the heading or its table is absent. A non-table line
    after the table starts ends it.
    """
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == "## %s" % heading:
            start = index + 1
            break
    if start is None:
        return None, [], []
    header = None
    rows, line_numbers = [], []
    for index in range(start, len(lines)):
        line = lines[index]
        if line.startswith("## "):
            break
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = _split_row(stripped)
            if header is None:
                header = cells
                continue
            if _is_separator(cells):
                continue
            rows.append(cells)
            line_numbers.append(index + 1)
        elif header is not None:
            break
    return header, rows, line_numbers


def _split_sources(cell: str) -> list:
    return [part.strip() for part in cell.split(",") if part.strip()]


# --------------------------------------------------------------------------- #
# workspace and declaration layer
# --------------------------------------------------------------------------- #
def resolve_workspace(explicit):
    """`--workspace-root` when given (a directory), else the nearest `.specify/` ancestor."""
    if explicit:
        path = Path(explicit).expanduser()
        return path.resolve() if path.is_dir() else None
    current = Path.cwd().resolve()
    for candidate in (current, *current.parents):
        if (candidate / MIRROR_DIR).is_dir():
            return candidate
    return None


def _layer_root(workspace: Path):
    """The audited tree's own declaration layer: `shared/` first, then `.specify/shared/`.

    The reader root returned beside it is the directory `declaration_reader.layer_dir`
    resolves against (`<workspace>` for the framework-source shape, `<workspace>/.specify`
    for the installed shape), so the owner document and the facts always pair.
    """
    for base in (workspace, workspace / MIRROR_DIR):
        owner = base.joinpath(*OWNER_DOC_PARTS)
        if owner.is_file():
            return base, owner
    return None, None


def _validate_facts(facts: dict) -> None:
    def closed_set(slug):
        statement = facts[slug].get("statement")
        if not isinstance(statement, list) or not statement:
            raise InputError("%s: statement must be a non-empty block sequence" % slug)
        if any(not isinstance(member, str) or not member.strip() for member in statement):
            raise InputError("%s: every member must be a non-empty string" % slug)
        if len(set(statement)) != len(statement):
            raise InputError("%s: the closed set carries a duplicate member" % slug)
        return list(statement)

    layers = closed_set("context-layers")
    forms = closed_set("context-forms")
    closed_set("context-categories")
    roster = facts["context-classes"].get("statement")
    if not isinstance(roster, dict):
        raise InputError("context-classes: statement must be a layer -> ids mapping")
    if list(roster) != layers:
        raise InputError(
            "context-classes: mapping keys must equal the declared layer domain in order, got %s"
            % list(roster))
    seen = set()
    for layer in layers:
        ids = roster[layer]
        if not isinstance(ids, list) or not ids:
            raise InputError("context-classes: layer %r must list its class ids" % layer)
        for class_id in ids:
            if not isinstance(class_id, str) or not class_id.strip():
                raise InputError("context-classes: every class id must be a non-empty string")
            if class_id in seen:
                raise InputError("context-classes: duplicate class id %r" % class_id)
            seen.add(class_id)
    if not set(forms):
        raise InputError("context-forms: the closed set is empty")


def _parse_forms(text: str, facts: dict) -> dict:
    layers = list(facts["context-layers"]["statement"])
    forms = list(facts["context-forms"]["statement"])
    header, rows, _lines = _first_table(text, "Forms")
    if header is None:
        raise InputError("owner document: the ## Forms table is missing")
    if tuple(header) != FORMS_COLUMNS:
        raise InputError(
            "owner document: the ## Forms header must be %s, got %s" % (FORMS_COLUMNS, header))
    matrix = {}
    for row in rows:
        if len(row) != 2:
            raise InputError("owner document: a ## Forms row must carry two cells: %s" % row)
        form = row[0]
        if form not in forms:
            raise InputError(
                "owner document: the form token %r is outside the declared form domain" % form)
        legal = [part.strip() for part in row[1].split(",") if part.strip()]
        for layer in legal:
            if layer not in layers:
                raise InputError(
                    "owner document: the legal-layer token %r is outside the declared layer domain"
                    % layer)
        matrix[form] = tuple(legal)
    if set(matrix) != set(forms):
        missing = sorted(set(forms) - set(matrix))
        extra = sorted(set(matrix) - set(forms))
        raise InputError(
            "owner document: the ## Forms matrix must cover every declared form "
            "(missing=%s extra=%s)" % (missing, extra))
    for layer in layers:
        if not any(layer in legal for legal in matrix.values()):
            raise InputError(
                "owner document: layer %r never appears in the ## Forms matrix" % layer)
    return matrix


def _parse_layout(text: str) -> list:
    header, rows, line_numbers = _first_table(text, "Layout")
    if header is None:
        raise InputError("owner document: the ## Layout table is missing")
    if tuple(header) != LAYOUT_COLUMNS:
        raise InputError(
            "owner document: the ## Layout header must be %s, got %s" % (LAYOUT_COLUMNS, header))
    parsed = []
    for ordinal, (row, line_number) in enumerate(zip(rows, line_numbers), start=1):
        if len(row) != 6:
            raise InputError(
                "owner document: line %d carries %d layout cells, expected 6"
                % (line_number, len(row)))
        if not all(cell.strip() for cell in row):
            raise InputError("owner document: line %d carries an empty layout cell" % line_number)
        parsed.append({
            "class": row[0],
            "layer": row[1],
            "form": row[2],
            "sources": _split_sources(row[3]),
            "owner": row[4],
            "cap": row[5],
            "line": line_number,
            "row": ordinal,
        })
    return parsed


def load_context(workspace: Path) -> dict:
    base, owner_path = _layer_root(workspace)
    if base is None:
        raise InputError(
            "declaration layer absent: no shared/definitions/context-management-definitions.md "
            "under %s or its %s/ install" % (workspace, MIRROR_DIR))
    if declaration_reader is None:
        raise InputError(
            "declaration reader unavailable: scripts/python/declaration_reader.py is not "
            "importable beside this engine")
    facts = {}
    for slug in FACT_SLUGS:
        try:
            facts[slug] = declaration_reader.load_fact(base, slug)["body"]
        except declaration_reader.DeclarationError as error:
            raise InputError(str(error))
    _validate_facts(facts)
    try:
        text = owner_path.read_text(encoding="utf-8")
    except OSError as error:
        raise InputError("owner document unreadable: %s (%s)" % (owner_path, error))
    matrix = _parse_forms(text, facts)
    layout = _parse_layout(text)
    return {
        "facts": facts,
        "layers": list(facts["context-layers"]["statement"]),
        "roster": facts["context-classes"]["statement"],
        "matrix": matrix,
        "layout": layout,
        "layout_by_class": {row["class"]: row for row in layout},
    }


# --------------------------------------------------------------------------- #
# presence reading (paths and metadata only)
# --------------------------------------------------------------------------- #
def _probe_succeeds(name: str, workspace: Path):
    if name == "platform":
        return bool(platform.system() and platform.machine()), (
            "runtime-discovery probe failed: platform identity unavailable")
    if name == "path-tools":
        found = shutil.which("git") or shutil.which("bash")
        return bool(found), (
            "runtime-discovery probe failed: no shell tool found on PATH")
    if name == "fs-access":
        return os.access(str(workspace), os.R_OK | os.X_OK), (
            "runtime-discovery probe failed: workspace root not readable")
    return False, "runtime-discovery probe failed: unknown probe %r" % name


def _reading(token: str, reason, size: int, mtime: int) -> dict:
    return {"token": token, "reason": reason, "size": size, "mtime": mtime}


def _read_source(workspace: Path, source: str) -> dict:
    if source.startswith(PROBE_PREFIX):
        name = source[len(PROBE_PREFIX):]
        ok, reason = _probe_succeeds(name, workspace)
        if ok:
            return _reading(PRESENT_TOKEN, None, 0, 0)
        return _reading(NOT_EVALUATED_TOKEN, reason, 0, 0)
    path = workspace / source
    try:
        stat = path.lstat()
    except FileNotFoundError:
        return _reading(ABSENT_TOKEN, "absent: %s does not exist" % source,
                        SENTINEL_MISSING_SIZE, SENTINEL_MISSING_SIZE)
    except OSError:
        return _reading(UNREACHABLE_TOKEN, "unreachable: %s cannot be examined" % source,
                        SENTINEL_UNREADABLE_SIZE, SENTINEL_UNREADABLE_SIZE)
    if path.is_symlink() and not path.exists():
        return _reading(UNREACHABLE_TOKEN, "unreachable: %s is a dangling symlink" % source,
                        SENTINEL_UNREADABLE_SIZE, SENTINEL_UNREADABLE_SIZE)
    try:
        if path.is_dir():
            entries = list(path.iterdir())
            count = len(entries)
            if count == 0:
                return _reading(EMPTY_TOKEN, "empty: %s holds no entry" % source,
                                count, stat.st_mtime_ns)
            zero_only = all(
                entry.is_file() and not entry.is_symlink() and entry.stat().st_size == 0
                for entry in entries)
            if zero_only:
                return _reading(EMPTY_TOKEN, "empty: %s holds only 0-byte files" % source,
                                count, stat.st_mtime_ns)
            return _reading(PRESENT_TOKEN, None, count, stat.st_mtime_ns)
        if path.is_file():
            if stat.st_size == 0:
                return _reading(EMPTY_TOKEN, "empty: %s is a 0-byte file" % source,
                                stat.st_size, stat.st_mtime_ns)
            return _reading(PRESENT_TOKEN, None, stat.st_size, stat.st_mtime_ns)
    except OSError:
        return _reading(UNREACHABLE_TOKEN, "unreachable: %s cannot be read" % source,
                        SENTINEL_UNREADABLE_SIZE, SENTINEL_UNREADABLE_SIZE)
    return _reading(UNREACHABLE_TOKEN,
                    "unreachable: %s is neither a regular file nor a directory" % source,
                    SENTINEL_UNREADABLE_SIZE, SENTINEL_UNREADABLE_SIZE)


def _row_presence(readings: list):
    for reading in readings:
        if reading["token"] != PRESENT_TOKEN:
            return reading["token"], reading["reason"]
    return PRESENT_TOKEN, None


def _source_reading(entries: list) -> str:
    digest = hashlib.sha256()
    for class_id, source, token, size, mtime in entries:
        digest.update(("%s\x00%s\x00%s\x00%d\x00%d\n" % (class_id, source, token, size, mtime))
                      .encode("utf-8"))
    return digest.hexdigest()


# --------------------------------------------------------------------------- #
# actions
# --------------------------------------------------------------------------- #
def action_manifest(context: dict, workspace: Path, layer: str, as_json: bool) -> int:
    rows = []
    entries = []
    for class_id in context["roster"][layer]:
        row = context["layout_by_class"].get(class_id)
        if row is None:
            rows.append({
                "class": class_id,
                "layer": layer,
                "form": UNDECLARED_CELL,
                "sources": [],
                "token": NOT_EVALUATED_TOKEN,
                "reason": "missing layout row: %s" % class_id,
                "cap": UNDECLARED_CELL,
            })
            entries.append((class_id, "-", NOT_EVALUATED_TOKEN,
                            SENTINEL_MISSING_ROW_SIZE, SENTINEL_MISSING_ROW_SIZE))
            continue
        readings = [_read_source(workspace, source) for source in row["sources"]]
        token, reason = _row_presence(readings)
        rows.append({
            "class": class_id,
            "layer": layer,
            "form": row["form"],
            "sources": list(row["sources"]),
            "token": token,
            "reason": reason,
            "cap": row["cap"],
        })
        for source, reading in zip(row["sources"], readings):
            entries.append((class_id, source, reading["token"], reading["size"], reading["mtime"]))
    counts = {token: sum(1 for row in rows if row["token"] == token)
              for token in PRESENCE_TOKENS}
    digest = _source_reading(entries)
    if as_json:
        payload = {
            "action": "manifest",
            "layer": layer,
            "rows": rows,
            "counts": counts,
            "source_reading": digest,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return EXIT_OK
    lines = []
    for row in rows:
        source_cell = ", ".join(row["sources"]) if row["sources"] else UNDECLARED_CELL
        line = ("row: %s | layer=%s | form=%s | source=%s | token=%s"
                % (row["class"], row["layer"], row["form"], source_cell, row["token"]))
        if row["reason"]:
            line += " | reason=%s" % row["reason"]
        line += " | cap=%s" % row["cap"]
        lines.append(line)
    lines.append("counts: " + " ".join("%s=%d" % (token, counts[token])
                                        for token in PRESENCE_TOKENS))
    lines.append("source-reading: " + digest)
    print("\n".join(lines))
    return EXIT_OK


def action_check(context: dict, as_json: bool) -> int:
    """The layout-integrity reading. The closed nine-rule set lands with its own row.

    A green it cannot support is worse than a refusal: the action exits 2 and writes no
    verdict until the rule set exists.
    """
    del context, as_json
    print("check: the closed nine-rule set is not implemented in this build; "
          "the audit refuses to report a verdict it cannot support", file=sys.stderr)
    return EXIT_INPUT


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="context-audit.py",
        description=("Read-only context-management audit. The layout table and the four "
                     "context facts are the declared inputs; audited sources are read as "
                     "paths and metadata only."),
        allow_abbrev=False,
    )
    configure_parser(
        parser,
        effects="none (read-only: no file, directory, cache or socket is written or opened)",
        codes=("0 clean or manifest emitted; 1 integrity findings; 2 usage, unreadable "
               "input or an unknown or missing declaration member"),
    )
    parser.add_argument(
        "--action", required=True,
        help="check (layout integrity reading) or manifest (print one layer's rows)")
    parser.add_argument(
        "--layer", default=None,
        help="layer to manifest; must be a member of the declared layer domain")
    parser.add_argument(
        "--workspace-root", default=None,
        help="workspace root to audit (default: the nearest ancestor holding .specify/)")
    parser.add_argument(
        "--json", action="store_true",
        help="machine-readable output for either action")
    if VersionAction is not None:
        VersionAction.attach(parser)
    return parser


def _usage(message: str) -> int:
    print(message, file=sys.stderr)
    return EXIT_INPUT


def main(argv=None) -> int:
    guard_argv(argv, declared=["--action", "--layer", "--workspace-root", "--json"])
    args = build_parser().parse_args(argv)

    if args.action not in ACTION_NAMES:
        return _usage("context-audit: --action must be one of check, manifest")
    if args.action == "manifest" and not args.layer:
        return _usage("context-audit: --action manifest requires --layer <layer>")
    if args.action == "check" and args.layer is not None:
        return _usage("context-audit: --layer applies to --action manifest only")

    workspace = resolve_workspace(args.workspace_root)
    if workspace is None:
        return _usage("context-audit: the workspace root cannot be resolved "
                      "(--workspace-root must name an existing directory)")
    try:
        context = load_context(workspace)
    except InputError as error:
        print("context-audit: %s" % error, file=sys.stderr)
        return EXIT_INPUT

    if args.action == "manifest":
        if args.layer not in context["layers"]:
            return _usage(
                "context-audit: --layer %r is outside the declared layer domain" % args.layer)
        return action_manifest(context, workspace, args.layer, args.json)
    return action_check(context, args.json)


if __name__ == "__main__":
    sys.exit(main())