#!/usr/bin/env python3
"""validate-decisions.py — read-only deterministic checker for decision governance (Feature 107).

The propositions judged here are fixed, textual and decidable, so a program judges them and
prints a verdict. The vocabulary, the class presentation, the option-set contract, the record
field closure, the transmission obligations and the M/B boundary are owned by
``shared/definitions/decision-definitions.md`` — this checker consumes them and never
restates them.

Actions (the declared interface; judgement legs land with their user stories):
  records     judge decision records in their carriers (US1: M-02, M-08;
              M-01, M-03, M-04, M-09 land with their user stories)
  payload     judge decision-backed dispatch payloads (M-06)
  chain       judge the record → dispatch attempt → implementation-receipt chain (M-05, M-07)
  inventory   judge the closed Decision Producer Inventory (FR-003)

Options:
  --action {records,payload,chain,inventory}   required; the judgement to run
  --spec PATH          the spec directory holding the carrier files
  --carrier PATH       a decision-record carrier file; repeatable
  --fixture PATH       a fixture directory or file to judge
  --register PATH      the register file that indexes ``D-NNN`` ids
  --glossary PATH      the glossary file whose variant rows M-08 consults
  --json               machine-readable output
  -h / --help          this body (same body for both spellings), exit 0
  --version            one line ``<script-name> <framework-version>``, exit 0

Exit codes: 0 = every judged check passed / 1 = a documented check failed /
2 = input or argument error (including a declared action not implemented yet).

Read-only: no write point of any kind, no resident process, standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

EXIT_OK = 0
EXIT_CHECK_FAILED = 1
EXIT_INPUT = 2

#: The closed declared action set (C-404 / T007). A fifth value MUST NOT be accepted before
#: the owner page and this tuple are revised in the same change.
ACTIONS = ("records", "payload", "chain", "inventory")

#: Every option the parser accepts, for the pre-parse guard (an undeclared ``-*`` token is
#: refused before any action runs — ``shared/definitions/script-interface-definitions.md`` § 4).
DECLARED_OPTIONS = (
    "--action", "--spec", "--carrier", "--fixture", "--register", "--glossary", "--json",
)

#: ``### D-NNN — <title>``; the title after the em dash carries the decision subject.
RECORD_HEADING_RE = re.compile(r"^### (D-\d{3})(?:\s+—\s+(.*))?$")
#: One top-level field line ``- **<field>**: <value>`` (the C-201 serialization grammar).
FIELD_RE = re.compile(r"^- \*\*([A-Za-z_][A-Za-z0-9_]*)\*\*:\s*(.*)$")
ANY_HEADING_RE = re.compile(r"^#{1,3}\s")
#: One named dimension ``key=value`` inside ``resource_locator`` (``;``-separated).
DIMENSION_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+?)\s*$")

#: The same-name locator floor (C-103): business resource group + region id, as a pair.
LOCATOR_FLOOR = ("business_resource_group", "region_id")

#: The rules this file's ``records`` action judges today (US1 legs). The remaining legs
#: (M-01, M-03, M-04, M-09) land with their user stories — an unimplemented leg is never
#: printed as a pass, because only listed rules produce verdicts at all.
RECORDS_RULES = ("M-02", "M-08")


def repo_root(start=None) -> Path:
    """The enclosing repository root, resolved from this file's own path.

    ``scripts/python/validate-decisions.py`` → the repository root is two levels up. The
    ``.specify/scripts/python/`` mirror copy would resolve to ``.specify``; a directory
    named ``.specify`` is never a repository root, so the guard steps one level further.
    """
    here = Path(start) if start is not None else Path(__file__)
    root = here.resolve().parents[2]
    if root.name == ".specify":
        root = root.parent
    return root


REPO_ROOT = repo_root()

# --version and the undeclared-option refusal come from the one shared helper; a copy that
# lacks the helper still runs its actions (same pattern as validate-decision-tensions.py).
_SIG_DIR = str(Path(__file__).resolve().parent)
if _SIG_DIR not in sys.path:
    sys.path.insert(0, _SIG_DIR)
try:
    from script_interface_cli import configure_parser as _sig_configure
    from script_interface_cli import guard_argv as _sig_guard
except ImportError:
    def _sig_configure(parser, **_kwargs):
        return parser

    def _sig_guard(_argv=None, declared=None, **_kwargs):
        return None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="validate-decisions.py",
        description="Judge the deterministic propositions of decision items, decision "
                    "records, transmission payloads and the closed producer inventory.",
    )
    _sig_configure(
        parser,
        effects="none; the checker is read-only — every action writes no file",
        codes="0 all judged checks passed; 1 a documented check failed; "
              "2 input or argument error",
    )
    parser.add_argument("--action", required=True, choices=ACTIONS,
                        help="the judgement to run")
    parser.add_argument("--spec", metavar="PATH",
                        help="the spec directory holding the carrier files")
    parser.add_argument("--carrier", metavar="PATH", action="append", default=[],
                        help="a decision-record carrier file (repeatable)")
    parser.add_argument("--fixture", metavar="PATH",
                        help="a fixture directory or file to judge")
    parser.add_argument("--register", metavar="PATH",
                        help="the register file that indexes D-NNN ids")
    parser.add_argument("--glossary", metavar="PATH",
                        help="the glossary file whose variant rows the subject check consults")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    return parser


def display_path(path: Path) -> str:
    """Repository-relative path when possible, so verdicts are stable across checkouts."""
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def parse_records(text: str) -> list[dict]:
    """Split a carrier into ``### D-NNN`` record blocks (fenced code never counts).

    A block is *new-form* when it carries at least one top-level C-201 field line; a
    three-digit heading below that threshold is legacy and is never judged (I-13).
    """
    records: list[dict] = []
    current: dict | None = None
    in_fence = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith("#"):
            heading = RECORD_HEADING_RE.match(line)
            if heading:
                current = {
                    "id": heading.group(1),
                    "subject": (heading.group(2) or "").strip(),
                    "line": lineno,
                    "fields": {},
                    "field_lines": {},
                }
                records.append(current)
            elif ANY_HEADING_RE.match(line):
                current = None
            continue
        if current is not None:
            field = FIELD_RE.match(line)
            if field:
                name, value = field.group(1), field.group(2).strip()
                current["fields"][name] = value
                current["field_lines"][name] = lineno
    return records


def new_form_records(records: list[dict]) -> list[dict]:
    return [record for record in records if record["fields"]]


def parse_dimensions(value: str) -> dict[str, str]:
    """Named dimensions of a ``resource_locator`` as ``{key: value}``; empty entries drop."""
    dimensions: dict[str, str] = {}
    for part in value.split(";"):
        match = DIMENSION_RE.match(part)
        if match:
            dimensions[match.group(1).lower()] = match.group(2)
    return dimensions


def load_glossary(path: Path) -> list[tuple[str, list[str]]]:
    """(canonical, variants) rows of a glossary table; header and separator rows drop."""
    rows: list[tuple[str, list[str]]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 2:
            continue
        canonical, variants_cell = cells[0], cells[1]
        if not canonical or canonical.lower() == "canonical":
            continue
        if set(canonical) <= set("-: "):
            continue
        variants = [v.strip() for v in variants_cell.split(",") if v.strip() and v.strip() != "-"]
        rows.append((canonical, variants))
    return rows


def variant_regex(variant: str) -> re.Pattern:
    """A variant as a standalone token: ASCII letters/digits/underscore are boundaries."""
    return re.compile(
        r"(?<![A-Za-z0-9_])" + re.escape(variant) + r"(?![A-Za-z0-9_])",
        re.IGNORECASE,
    )


def check_m02(record: dict) -> list[dict]:
    """M-02: ``same_name_conflict: true`` needs the locator floor (C-103)."""
    if record["fields"].get("same_name_conflict", "").strip().lower() != "true":
        return []
    locator = record["fields"].get("resource_locator", "")
    line = record["field_lines"].get(
        "resource_locator", record["field_lines"].get("same_name_conflict", record["line"])
    )
    dimensions = parse_dimensions(locator)
    missing = [key for key in LOCATOR_FLOOR if not dimensions.get(key)]
    if locator.strip() and not missing:
        return []
    if not locator.strip():
        message = ("same_name_conflict: true requires a machine-parseable resource_locator "
                   "carrying at least the business resource group + region id pair "
                   "(the locator is empty)")
    else:
        message = ("same_name_conflict: true requires a machine-parseable resource_locator "
                   "carrying at least the business resource group + region id pair "
                   f"(missing named dimension(s): {', '.join(missing)})")
    return [{"rule": "M-02", "line": line, "message": message}]


def check_m08(record: dict, glossary_rows: list[tuple[str, list[str]]]) -> list[dict]:
    """M-08: a registered glossary variant in the structured subject turns red."""
    subject = record["subject"]
    if not subject:
        return []
    for canonical, variants in glossary_rows:
        for variant in variants:
            if variant.lower() == canonical.lower():
                # A variant that differs from its canonical only by letter case is the
                # canonical's own case-folded spelling; it cannot be told apart.
                continue
            if variant_regex(variant).search(subject):
                return [{
                    "rule": "M-08",
                    "line": record["line"],
                    "message": (f"decision subject uses the registered glossary variant "
                                f"{variant!r}; use the full name {canonical!r}"),
                }]
    return []


def collect_carriers(carriers: list[str], fixture: str | None, spec: str | None) -> list[Path]:
    """Every carrier file the run judges: explicit files, a fixture path, a spec directory."""
    paths: list[Path] = []
    for raw in carriers:
        paths.append(Path(raw))
    for raw in (fixture, spec):
        if not raw:
            continue
        base = Path(raw)
        if base.is_dir():
            paths.extend(sorted(base.rglob("*.md")))
        else:
            paths.append(base)
    return paths


def run_records(args) -> int:
    """Judge the landed ``records`` legs (M-02, M-08); the run mutates nothing."""
    carriers = collect_carriers(args.carrier, args.fixture, args.spec)
    if not carriers:
        print("error: --action records needs --carrier, --fixture or --spec input",
              file=sys.stderr)
        return EXIT_INPUT

    glossary_path = Path(args.glossary) if args.glossary else REPO_ROOT / ".specify" / "glossary.md"
    try:
        glossary_rows = load_glossary(glossary_path) if glossary_path.is_file() else []
    except OSError as exc:
        print(f"error: cannot read glossary {glossary_path}: {exc}", file=sys.stderr)
        return EXIT_INPUT
    if args.glossary and not glossary_path.is_file():
        print(f"error: glossary not found: {glossary_path}", file=sys.stderr)
        return EXIT_INPUT

    violations: list[dict] = []
    for carrier in carriers:
        try:
            text = carrier.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"error: cannot read carrier {carrier}: {exc}", file=sys.stderr)
            return EXIT_INPUT
        for record in new_form_records(parse_records(text)):
            found = check_m02(record) + check_m08(record, glossary_rows)
            for verdict in found:
                verdict["path"] = display_path(carrier)
                violations.append(verdict)
    violations.sort(key=lambda v: (v["path"], v["line"], v["rule"]))

    status = "fail" if violations else "pass"
    if args.json:
        print(json.dumps({
            "action": "records",
            "status": status,
            "rules": list(RECORDS_RULES),
            "violations": violations,
        }, ensure_ascii=False, indent=2))
    elif violations:
        for verdict in violations:
            print(f"{verdict['rule']} {verdict['path']}:{verdict['line']}: {verdict['message']}")
        print(f"FAIL: {len(violations)} violation(s)")
    else:
        print(f"PASS: 0 violation(s) (rules: {', '.join(RECORDS_RULES)})")
    return EXIT_CHECK_FAILED if violations else EXIT_OK


def main(argv=None) -> int:
    _sig_guard(argv, declared=DECLARED_OPTIONS)
    parser = build_parser()
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    if args.action == "records":
        return run_records(args)

    # Interface final, judgement legs pending: the remaining declared actions report
    # not-implemented and exit as an input error, so an unimplemented check can never be
    # mistaken for a pass. The legs land with US3–US5 of feature 107.
    if args.json:
        print(json.dumps({"action": args.action, "status": "not-implemented",
                          "root": str(REPO_ROOT)}, ensure_ascii=False))
    print("error: action %r is declared but not implemented yet (read-only skeleton)"
          % args.action, file=sys.stderr)
    return EXIT_INPUT


if __name__ == "__main__":
    sys.exit(main())
