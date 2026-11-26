#!/usr/bin/env python3
"""validate-decisions.py — read-only deterministic checker for decision governance (Feature 107).

The propositions judged here are fixed, textual and decidable, so a program judges them and
prints a verdict. The vocabulary, the class presentation, the option-set contract, the record
field closure, the transmission obligations and the M/B boundary are owned by
``shared/definitions/decision-definitions.md`` — this checker consumes them and never
restates them.

Actions:
  records     judge decision records in their carriers: M-01 (layered field closure,
              class domain, phase-driven timepoints), M-02 (same-name locator), M-03
              (option-set closure and chosen-member membership), M-04 (id form, density,
              register), M-08 (registered glossary variant) and M-09 (evidence-pointer
              resolvability); legacy headings and legacy register rows are reported, never
              judged
  payload     judge dispatch payload snapshots: M-06 (a decision-backed dispatch carries
              the complete five-field ``decision_block``; a non-decision dispatch without
              a block is legal)
  chain       judge chain snapshots: M-05 (the implementation receipt exists and its
              ``decision_id`` resolves) and M-07 (record → dispatch attempt → receipt all
              present with consistent ids)
  inventory   judge the closed Decision Producer Inventory (FR-003; the leg lands with US5)

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

#: ``### D-NNN — <title>``; the title after the em dash carries the decision subject. The id
#: token is captured for any ``D-…`` heading so the legacy discriminator can tell the minimal
#: qualifying form (``^D-\d{3}`` plus at least one field line) from everything below it.
RECORD_HEADING_RE = re.compile(r"^###\s+(D-\S+)(?:\s+—\s+(.*))?$")
#: The declared id form (C-203): three digits, whole token.
ID_FORM_RE = re.compile(r"^D-\d{3}$")
#: One top-level field line ``- **<field>**: <value>`` (the C-201 serialization grammar).
FIELD_RE = re.compile(r"^- \*\*([A-Za-z_][A-Za-z0-9_]*)\*\*:\s*(.*)$")
ANY_HEADING_RE = re.compile(r"^#{1,3}\s")
#: One named dimension ``key=value`` inside ``resource_locator`` (``;``-separated).
DIMENSION_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+?)\s*$")

#: The same-name locator floor (C-103): business resource group + region id, as a pair.
LOCATOR_FLOOR = ("business_resource_group", "region_id")

#: The five option elements (C-106); ``path`` and ``forced`` are value-shape members of
#: ``options``, not additional elements.
OPTION_ELEMENTS = ("consequences", "reversibility", "default", "evidence")

#: The ten base-layer fields (C-202). ``decision_id`` is carried by the heading; the other
#: nine MUST appear as one field line each on every record.
BASE_FIELDS = (
    "decision_id", "decision_class", "context", "options", "chosen_option",
    "rationale", "evidence", "actor", "created_at", "transmission_status",
)
BASE_LINE_FIELDS = tuple(name for name in BASE_FIELDS if name != "decision_id")

#: The conditional-layer families (C-202); each field is required exactly when its trigger
#: holds. Together with the base layer these are the only admitted top-level field lines.
CONDITIONAL_FIELDS = (
    "same_name_conflict", "resource_locator", "superseded_by",
    "dispatched_at", "acknowledged_at", "implemented_at",
)
ADMITTED_FIELD_LINES = frozenset(BASE_LINE_FIELDS) | frozenset(CONDITIONAL_FIELDS)

CLASS_DOMAIN = ("human-interactive", "ai-autonomous")
STATUS_DOMAIN = (
    "not-transmitted", "dispatched", "acknowledged", "implemented", "diverged", "blocked",
)
TRANSMISSION_TIMEPOINTS = ("dispatched_at", "acknowledged_at", "implemented_at")
#: ISO-8601 UTC: ``Z`` or an explicit ``+00:00`` offset, optional fractional seconds.
TIMEPOINT_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|\+00:00)$")

#: A three-digit id token in a register cell; a suffixed id (``D-001-a``) is a distinct
#: legacy id and never resolves the base token.
REGISTER_ID_RE = re.compile(r"(?<![A-Za-z0-9-])D-\d{3}(?![A-Za-z0-9-])")
#: A grouped register row ``D-001–D-003`` / ``D-001…D-003`` / ``D-001-D-003``.
REGISTER_RANGE_RE = re.compile(r"D-(\d{3})\s*[–—…-]\s*(?:D-)?(\d{3})")

#: The rules this file's ``records`` action judges today. The remaining legs land with their
#: user stories — an unimplemented leg is never printed as a pass, because only listed rules
#: produce verdicts at all.
RECORDS_RULES = ("M-01", "M-02", "M-03", "M-04", "M-08", "M-09")

#: The five decision-block fields (C-301) a decision-backed dispatch must carry.
BLOCK_FIELDS = (
    "decision_id", "decision_class", "chosen_option",
    "implementation_constraints", "archive_pointer",
)

#: The rules the ``payload`` and ``chain`` actions judge (C-401 rows M-05…M-07).
PAYLOAD_RULES = ("M-06",)
CHAIN_RULES = ("M-05", "M-07")

#: The chain segments of an auditable transmission (C-306), in order.
CHAIN_SEGMENTS = ("Record", "Dispatch Attempt", "Receipt")
CHAIN_SECTION_RE = re.compile(r"^##\s+(?!##)(.+?)\s*$")
#: One indented ``- **<field>**: <value>`` sub-line (a decision block's members).
SUB_FIELD_RE = re.compile(r"^\s{2,}- \*\*([A-Za-z_][A-Za-z0-9_]*)\*\*:\s*(.*)$")


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
    """Split a carrier into ``### D-…`` record blocks (fenced code never counts).

    A block is *new-form* when its heading token matches the minimal qualifying form
    (``^D-\\d{3}``) and the block carries at least one top-level C-201 field line; anything
    below that threshold is legacy and is never judged (C-206).
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
                    "heading": line.strip(),
                    "fields": {},
                    "field_lines": {},
                    "lines": [],
                }
                records.append(current)
            elif ANY_HEADING_RE.match(line):
                current = None
            continue
        if current is not None:
            current["lines"].append((lineno, line))
            field = FIELD_RE.match(line)
            if field:
                name, value = field.group(1), field.group(2).strip()
                current["fields"][name] = value
                current["field_lines"][name] = lineno
    return records


def new_form_records(records: list[dict]) -> list[dict]:
    """Records at or above the minimal qualifying form; incomplete blocks stay judged."""
    return [
        record for record in records
        if re.match(r"^D-\d{3}", record["id"]) and record["fields"]
    ]


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


def parse_options(record: dict) -> tuple[int | None, list[dict], str]:
    """(declared count, option entries, forced reason) of the record's ``options`` block.

    Option entries are indented ``- label: <value>`` sub-lines; the four remaining elements
    and the ``other`` path are further indented lines attributed to the current entry. A
    ``forced: <reason>`` line anywhere in the block (or inside the field value) is the
    single-viable-option declaration (C-106).
    """
    value = record["fields"].get("options", "")
    declared = None
    count_match = re.match(r"\s*(\d+)", value)
    if count_match:
        declared = int(count_match.group(1))
    forced = ""
    inline = re.search(r"forced\s*:\s*(.+)$", value)
    if inline:
        forced = inline.group(1).strip()

    entries: list[dict] = []
    start = record["field_lines"].get("options")
    if start is None:
        return declared, entries, forced
    for lineno, line in record["lines"]:
        if lineno <= start:
            continue
        if FIELD_RE.match(line):
            break
        entry = re.match(r"^\s{2,}-\s+label\s*:\s*(.*)$", line)
        if entry:
            entries.append({
                "label": entry.group(1).strip(),
                "line": lineno,
                "elements": {},
                "path": "",
            })
            continue
        element = re.match(
            r"^\s{2,}(consequences|reversibility|default|evidence)\s*:\s*(.*)$", line
        )
        if element:
            if entries:
                entries[-1]["elements"][element.group(1)] = element.group(2).strip()
            continue
        path_line = re.match(r"^\s{2,}path\s*:\s*(.*)$", line)
        if path_line:
            if entries:
                entries[-1]["path"] = path_line.group(1).strip()
            continue
        forced_line = re.match(r"^\s{2,}forced\s*:\s*(.*)$", line)
        if forced_line and forced_line.group(1).strip():
            forced = forced_line.group(1).strip()
    return declared, entries, forced


def check_m03(record: dict) -> list[dict]:
    """M-03: the option set is closed, enumerable and comparable (C-106, C-107 member)."""
    if "options" not in record["fields"]:
        return []  # a missing options field is M-01's missing base-layer field
    options_line = record["field_lines"].get("options", record["line"])
    declared, entries, forced = parse_options(record)
    found: list[dict] = []

    def verdict(line: int, message: str) -> None:
        found.append({"rule": "M-03", "line": line, "message": message})

    if declared is None:
        verdict(options_line,
                "the option count is not declared; a closed enumerable set MUST open its "
                "options field with the declared count (e.g. '- **options**: 2')")
    if declared == 0 or not entries:
        verdict(options_line,
                "empty option set; a decision item MUST carry at least one option "
                "(zero viable options is not a decision item)")
        return found
    if declared is not None and declared != len(entries):
        verdict(options_line,
                f"declared count {declared} does not match the {len(entries)} option "
                "entry(ies); the set is not closed as declared")

    seen: dict[str, int] = {}
    for entry in entries:
        label = entry["label"]
        if not label:
            verdict(entry["line"], "option entry carries no label")
        else:
            key = label.casefold()
            if key in seen:
                verdict(entry["line"],
                        f"duplicate option label {label!r}; labels MUST be unique")
            else:
                seen[key] = entry["line"]
        missing = [name for name in OPTION_ELEMENTS
                   if not entry["elements"].get(name, "").strip()]
        if missing:
            verdict(entry["line"],
                    f"option {label!r} is missing option element(s): {', '.join(missing)}")
        if label.strip().casefold() == "other" and not entry["path"]:
            verdict(entry["line"],
                    "an option named 'other' is legal only with a path declaring who/when/"
                    "how options may be added and the record written back")

    if len(entries) == 1 and not forced:
        verdict(options_line,
                "a single viable option MUST declare 'forced' with a reason; it MUST NOT "
                "masquerade as a multi-option decision")

    chosen = record["fields"].get("chosen_option", "").strip()
    if chosen:
        labels = {entry["label"].strip() for entry in entries}
        if chosen not in labels:
            verdict(record["field_lines"].get("chosen_option", record["line"]),
                    f"chosen_option {chosen!r} is not a named member of the option set")
    return found


def check_m01(record: dict) -> list[dict]:
    """M-01: layered field closure, the class domain and phase-driven timepoints (C-202)."""
    fields = record["fields"]
    found: list[dict] = []

    def verdict(line: int, message: str) -> None:
        found.append({"rule": "M-01", "line": line, "message": message})

    missing = [name for name in BASE_LINE_FIELDS if not fields.get(name, "").strip()]
    if missing:
        verdict(record["line"], f"missing base-layer field(s): {', '.join(missing)}")

    if "decision_id" in fields:
        verdict(record["field_lines"]["decision_id"],
                "decision_id is carried by the heading; a second field line duplicates the id")

    unknown = [name for name in fields if name not in ADMITTED_FIELD_LINES
               and name != "decision_id"]
    for name in unknown:
        verdict(record["field_lines"][name],
                f"field {name!r} is outside the two admitted layers "
                "(layered field closure; revise the owner page before adding a field)")

    decision_class = fields.get("decision_class", "").strip()
    if decision_class and decision_class not in CLASS_DOMAIN:
        verdict(record["field_lines"].get("decision_class", record["line"]),
                f"decision_class {decision_class!r} is outside the closed set "
                f"{' / '.join(CLASS_DOMAIN)}")

    status = fields.get("transmission_status", "").strip()
    if status and status not in STATUS_DOMAIN:
        verdict(record["field_lines"].get("transmission_status", record["line"]),
                f"transmission_status {status!r} is outside its closed domain")

    created_at = fields.get("created_at", "").strip()
    if created_at and not TIMEPOINT_RE.match(created_at):
        verdict(record["field_lines"]["created_at"],
                "created_at is not an ISO-8601 UTC timepoint (e.g. 2026-11-26T00:00:00Z)")

    present = {name: fields.get(name, "").strip() for name in TRANSMISSION_TIMEPOINTS}
    for name, value in present.items():
        if value and not TIMEPOINT_RE.match(value):
            verdict(record["field_lines"][name],
                    f"{name} is not an ISO-8601 UTC timepoint (e.g. 2026-11-26T00:00:00Z)")

    if status in STATUS_DOMAIN:
        if status == "not-transmitted":
            for name, value in present.items():
                if value:
                    verdict(record["field_lines"][name],
                            f"{name} present on a not-transmitted record "
                            "(no placeholder before the event)")
        else:
            required = ["dispatched_at"]
            if status in ("acknowledged", "implemented", "diverged", "blocked"):
                required.append("acknowledged_at")
            if status in ("implemented", "diverged"):
                required.append("implemented_at")
            for name in required:
                if not present[name]:
                    verdict(record["line"],
                            f"{name} missing while transmission_status is {status}")
            if status == "dispatched":
                for name in ("acknowledged_at", "implemented_at"):
                    if present[name]:
                        verdict(record["field_lines"][name],
                                f"{name} present while transmission_status is still "
                                "dispatched (phase contradiction)")
            elif status == "acknowledged" and present["implemented_at"]:
                verdict(record["field_lines"]["implemented_at"],
                        "implemented_at present while transmission_status is still "
                        "acknowledged (phase contradiction)")
    return found


def check_m09(record: dict, carrier: Path) -> list[dict]:
    """M-09: every evidence pointer resolves to an existing carrier path/anchor (C-204)."""
    found: list[dict] = []
    pointers: list[tuple[str, int]] = []
    evidence_line = record["field_lines"].get("evidence", record["line"])
    for part in record["fields"].get("evidence", "").split(";"):
        if part.strip():
            pointers.append((part.strip(), evidence_line))
    _, entries, _ = parse_options(record)
    for entry in entries:
        for part in entry["elements"].get("evidence", "").split(";"):
            if part.strip():
                pointers.append((part.strip(), entry["line"]))
    for pointer, line in pointers:
        resolved, reason = resolve_pointer(pointer, carrier)
        if not resolved:
            found.append({"rule": "M-09", "line": line,
                          "message": f"evidence pointer {pointer!r} does not resolve: {reason}"})
    return found


def resolve_pointer(pointer: str, carrier: Path) -> tuple[bool, str]:
    """Resolve one evidence pointer: repository-relative or carrier-relative path (+anchor).

    Only resolvability is judged. A pointer whose path part is empty resolves inside the
    carrier itself; an external URL is unresolvable in a deterministic offline check.
    """
    if pointer.startswith(("http://", "https://")):
        return False, "an external URL cannot be resolved deterministically offline"
    path_part, _, anchor = pointer.partition("#")
    path_part = path_part.strip()
    if not path_part:
        target: Path | None = carrier
    else:
        raw = Path(path_part)
        candidates = [raw] if raw.is_absolute() else [
            REPO_ROOT / path_part, carrier.parent / path_part,
        ]
        target = next((candidate for candidate in candidates if candidate.is_file()), None)
        if target is None:
            return False, "the referenced carrier path does not exist"
    if anchor.strip():
        try:
            body = target.read_text(encoding="utf-8")
        except OSError as exc:
            return False, f"the referenced carrier is unreadable ({exc})"
        if anchor.strip().casefold() not in body.casefold():
            return False, "the anchor does not appear in the referenced carrier"
    return True, ""


def load_register_rows(path: Path) -> list[tuple[int, str]]:
    """``(line, id cell)`` rows of the register's id column; header/separator rows drop."""
    rows: list[tuple[int, str]] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells:
            continue
        first = cells[0].replace("*", "").replace("`", "").strip()
        if not first or first.casefold() in ("编号", "id"):
            continue
        if set(first) <= set("-: "):
            continue
        if not re.match(r"^D(?:-|\d)", first):
            continue
        rows.append((lineno, first))
    return rows


def ids_in_cell(cell: str) -> set[str]:
    """``D-NNN`` ids (and ids covered by a grouped range) written in one register cell."""
    ids: set[str] = set()
    for match in REGISTER_RANGE_RE.finditer(cell):
        low, high = sorted((int(match.group(1)), int(match.group(2))))
        ids.update(f"D-{number:03d}" for number in range(low, high + 1))
    ids.update(match.group(0) for match in REGISTER_ID_RE.finditer(cell))
    return ids


def register_ids(rows: list[tuple[int, str]]) -> set[str]:
    ids: set[str] = set()
    for _, cell in rows:
        ids.update(ids_in_cell(cell))
    return ids


def check_m04(records: list[dict], resolvable_ids: set[str]) -> list[dict]:
    """M-04: id form, per-carrier density and register resolvability (C-203)."""
    found: list[dict] = []
    for record in records:
        if not ID_FORM_RE.match(record["id"]):
            found.append({
                "rule": "M-04", "line": record["line"],
                "message": (f"heading id {record['id']!r} does not match the D-NNN form "
                            "(exactly three digits)"),
            })
    well_formed = [record for record in records if ID_FORM_RE.match(record["id"])]
    seen: set[str] = set()
    for record in well_formed:
        if record["id"] in seen:
            found.append({"rule": "M-04", "line": record["line"],
                          "message": f"id {record['id']} appears more than once in the carrier"})
        seen.add(record["id"])
    numbers = sorted({int(record["id"][2:]) for record in well_formed})
    if numbers:
        expected = list(range(1, len(numbers) + 1))
        if numbers != expected:
            missing = [f"D-{number:03d}" for number in sorted(set(expected) - set(numbers))]
            found.append({"rule": "M-04", "line": well_formed[0]["line"],
                          "message": (f"ids in the carrier are not dense: missing "
                                      f"{', '.join(missing)}")})
    for record in well_formed:
        if record["id"] not in resolvable_ids:
            found.append({"rule": "M-04", "line": record["line"],
                          "message": f"id {record['id']} is not resolvable in the register"})
    return found


def legacy_register_rows(
    rows: list[tuple[int, str]], new_form_ids: set[str]
) -> list[tuple[int, str]]:
    """Register rows that are not the birth registration of a new-form record (C-206)."""
    return [
        (lineno, cell) for lineno, cell in rows
        if not (ids_in_cell(cell) & new_form_ids)
    ]


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
    """Judge the ``records`` legs (M-01…M-04, M-08, M-09); the run mutates nothing."""
    carriers = collect_carriers(args.carrier, args.fixture, args.spec)
    if not carriers:
        print("error: --action records needs --carrier, --fixture or --spec input",
              file=sys.stderr)
        return EXIT_INPUT

    register_path = Path(args.register) if args.register else REPO_ROOT / ".specify" / "register.md"
    if not register_path.is_file():
        print(f"error: register not found: {register_path}", file=sys.stderr)
        return EXIT_INPUT
    try:
        register_rows = load_register_rows(register_path)
    except OSError as exc:
        print(f"error: cannot read register {register_path}: {exc}", file=sys.stderr)
        return EXIT_INPUT
    resolvable_ids = register_ids(register_rows)

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
    legacy: list[dict] = []
    records_out: list[dict] = []
    new_form_ids: set[str] = set()

    for carrier in carriers:
        try:
            text = carrier.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"error: cannot read carrier {carrier}: {exc}", file=sys.stderr)
            return EXIT_INPUT
        parsed = parse_records(text)
        new_form = new_form_records(parsed)
        new_form_ids.update(record["id"] for record in new_form)
        judged = {id(record) for record in new_form}
        for record in parsed:
            if id(record) in judged:
                continue
            legacy.append({
                "kind": "heading",
                "path": display_path(carrier),
                "line": record["line"],
                "text": record["heading"],
            })
        for record in new_form:
            found = (check_m01(record) + check_m02(record) + check_m03(record)
                     + check_m08(record, glossary_rows) + check_m09(record, carrier))
            for verdict in found:
                verdict["path"] = display_path(carrier)
                violations.append(verdict)
            records_out.append({
                "id": record["id"],
                "path": display_path(carrier),
                "line": record["line"],
                "class": record["fields"].get("decision_class", ""),
                "fields": dict(record["fields"]),
            })
        for verdict in check_m04(new_form, resolvable_ids):
            verdict["path"] = display_path(carrier)
            violations.append(verdict)

    for lineno, cell in legacy_register_rows(register_rows, new_form_ids):
        legacy.append({
            "kind": "register-row",
            "path": display_path(register_path),
            "line": lineno,
            "id": cell,
        })

    violations.sort(key=lambda v: (v["path"], v["line"], v["rule"]))
    legacy.sort(key=lambda e: (e["path"], e["line"]))

    status = "fail" if violations else "pass"
    if args.json:
        print(json.dumps({
            "action": "records",
            "status": status,
            "rules": list(RECORDS_RULES),
            "records": records_out,
            "legacy": legacy,
            "violations": violations,
        }, ensure_ascii=False, indent=2))
    else:
        for verdict in violations:
            print(f"{verdict['rule']} {verdict['path']}:{verdict['line']}: {verdict['message']}")
        for entry in legacy:
            if entry["kind"] == "heading":
                print(f"LEGACY {entry['path']}:{entry['line']}: {entry['text']} "
                      "(legacy record — reported, not judged)")
            else:
                print(f"LEGACY {entry['path']}:{entry['line']}: {entry['id']} "
                      "(legacy register row — reported, not judged)")
        if violations:
            print(f"FAIL: {len(violations)} violation(s)")
        else:
            print(f"PASS: 0 violation(s) (rules: {', '.join(RECORDS_RULES)})")
    return EXIT_CHECK_FAILED if violations else EXIT_OK


def collect_snapshots(carriers: list[str], fixture: str | None) -> list[Path]:
    """Snapshot files the ``payload`` and ``chain`` actions judge.

    A fixture directory contributes its top-level ``*.md`` files only; return snapshots and
    record carriers live in subdirectories and are reached by an explicit path, so a
    directory judgement never silently widens to them.
    """
    paths: list[Path] = [Path(raw) for raw in carriers]
    if fixture:
        base = Path(fixture)
        if base.is_dir():
            paths.extend(sorted(base.glob("*.md")))
        else:
            paths.append(base)
    return paths


def parse_payload(text: str) -> dict:
    """Top-level fields plus the ``decision_block`` sub-fields of one dispatch snapshot."""
    fields: dict[str, str] = {}
    field_lines: dict[str, int] = {}
    block: dict[str, str] = {}
    block_lines: dict[str, int] = {}
    in_block = False
    in_fence = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith("#"):
            in_block = False
            continue
        sub = SUB_FIELD_RE.match(line)
        if sub and in_block:
            block[sub.group(1)] = sub.group(2).strip()
            block_lines[sub.group(1)] = lineno
            continue
        top = FIELD_RE.match(line)
        if top:
            name, value = top.group(1), top.group(2).strip()
            fields[name] = value
            field_lines[name] = lineno
            in_block = name == "decision_block"
            continue
        if line.strip():
            in_block = False
    return {"fields": fields, "field_lines": field_lines,
            "block": block, "block_lines": block_lines}


def check_m06(snapshot: dict) -> list[dict]:
    """M-06: a decision-backed dispatch carries the complete five-field block (C-301/C-302)."""
    backed = snapshot["fields"].get("decision_backed", "").strip().lower()
    block_line = snapshot["field_lines"].get("decision_block", 1)
    if backed == "false":
        return []
    declared = "decision_block" in snapshot["fields"]
    if not declared and not snapshot["block"]:
        return [{
            "rule": "M-06",
            "line": block_line,
            "message": ("a decision-backed dispatch MUST carry a decision_block with "
                        "decision_id, decision_class, chosen_option, implementation_constraints "
                        "and archive_pointer; it is refused at payload construction "
                        "(the decision_block is absent)"),
        }]
    found: list[dict] = []
    for name in BLOCK_FIELDS:
        if not snapshot["block"].get(name, "").strip():
            found.append({
                "rule": "M-06",
                "line": block_line,
                "message": f"the decision_block is missing the required field `{name}`",
            })
    return found


def parse_chain(text: str) -> dict[str, list[dict]]:
    """The Record / Dispatch Attempt / Receipt segments of one chain snapshot.

    A segment is one ``## <name>`` section with its top-level field lines; repeated
    Dispatch Attempt / Receipt sections model a multi-hop chain.
    """
    segments: dict[str, list[dict]] = {name: [] for name in CHAIN_SEGMENTS}
    current: dict | None = None
    in_fence = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith("## "):
            heading = CHAIN_SECTION_RE.match(line)
            name = heading.group(1).strip() if heading else ""
            current = ({"line": lineno, "fields": {}, "field_lines": {}}
                       if name in segments else None)
            if current is not None:
                segments[name].append(current)
            continue
        if line.startswith("#"):
            current = None
            continue
        if current is not None:
            field = FIELD_RE.match(line)
            if field:
                current["fields"][field.group(1)] = field.group(2).strip()
                current["field_lines"][field.group(1)] = lineno
    return segments


def chain_verdicts(segments: dict[str, list[dict]]) -> list[dict]:
    """M-05 (receipt presence/resolvability) and M-07 (segments and id consistency)."""
    found: list[dict] = []
    records = [seg for seg in segments["Record"] if seg["fields"]]
    dispatches = [seg for seg in segments["Dispatch Attempt"] if seg["fields"]]
    receipts = [seg for seg in segments["Receipt"] if seg["fields"]]
    record_ids = [seg["fields"].get("decision_id", "").strip() for seg in records]
    record_ids = [rid for rid in record_ids if rid]
    record_id = record_ids[0] if record_ids else ""

    anchor = records[0]["line"] if records else 1

    if not receipts:
        found.append({
            "rule": "M-05", "line": anchor,
            "message": ("the implementation_receipt is missing; a transmitted decision MUST "
                        "return a receipt and an incomplete return is never consumed"),
        })
    for receipt in receipts:
        rid = receipt["fields"].get("decision_id", "").strip()
        line = receipt["field_lines"].get("decision_id", receipt["line"])
        if not rid:
            found.append({"rule": "M-05", "line": line,
                          "message": "the implementation_receipt carries no decision_id"})
        elif not ID_FORM_RE.match(rid):
            found.append({"rule": "M-05", "line": line,
                          "message": (f"the receipt decision_id {rid!r} is not a resolvable "
                                      "D-NNN id")})
        elif not record_id or rid != record_id:
            found.append({"rule": "M-05", "line": line,
                          "message": (f"the receipt decision_id {rid!r} does not resolve to a "
                                      "record in this chain")})

    if not records:
        found.append({"rule": "M-07", "line": anchor,
                      "message": ("the record segment is missing; an auditable chain MUST "
                                  "carry the decision record, the dispatch attempt and the "
                                  "implementation receipt")})
    elif not record_id:
        found.append({"rule": "M-07", "line": records[0]["line"],
                      "message": "the record segment carries no decision_id"})
    if not dispatches:
        found.append({"rule": "M-07", "line": anchor,
                      "message": ("the dispatch attempt segment is missing "
                                  "(decision record → dispatch attempt → receipt)")})
    if not receipts:
        found.append({"rule": "M-07", "line": anchor,
                      "message": ("the receipt segment is missing "
                                  "(decision record → dispatch attempt → receipt)")})
    if record_id:
        for dispatch in dispatches:
            did = dispatch["fields"].get("decision_id", "").strip()
            line = dispatch["field_lines"].get("decision_id", dispatch["line"])
            if not did:
                found.append({"rule": "M-07", "line": line,
                              "message": "the dispatch attempt carries no decision_id "
                                         "(the chain link is missing)"})
            elif did != record_id:
                found.append({"rule": "M-07", "line": line,
                              "message": (f"the dispatch attempt decision_id {did!r} is "
                                          f"inconsistent with the record id {record_id!r}")})
        for receipt in receipts:
            rid = receipt["fields"].get("decision_id", "").strip()
            if rid and rid != record_id:
                found.append({
                    "rule": "M-07",
                    "line": receipt["field_lines"].get("decision_id", receipt["line"]),
                    "message": (f"the receipt decision_id {rid!r} is inconsistent with the "
                                f"record id {record_id!r}"),
                })
    return found


def print_action_report(action: str, rules: tuple[str, ...], checked: int,
                        violations: list[dict], as_json: bool) -> int:
    """Shared verdict rendering for the snapshot-shaped actions."""
    violations.sort(key=lambda v: (v["path"], v["line"], v["rule"]))
    status = "fail" if violations else "pass"
    if as_json:
        print(json.dumps({
            "action": action,
            "status": status,
            "rules": list(rules),
            "checked": checked,
            "violations": violations,
        }, ensure_ascii=False, indent=2))
    else:
        for verdict in violations:
            print(f"{verdict['rule']} {verdict['path']}:{verdict['line']}: {verdict['message']}")
        if violations:
            print(f"FAIL: {len(violations)} violation(s)")
        else:
            print(f"PASS: 0 violation(s) (rules: {', '.join(rules)})")
    return EXIT_CHECK_FAILED if violations else EXIT_OK


def run_payload(args) -> int:
    """M-06: decision-backed dispatch snapshots carry the complete decision block."""
    snapshots = collect_snapshots(args.carrier, args.fixture)
    if not snapshots:
        print("error: --action payload needs --carrier or --fixture input", file=sys.stderr)
        return EXIT_INPUT
    violations: list[dict] = []
    checked = 0
    for path in snapshots:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"error: cannot read snapshot {path}: {exc}", file=sys.stderr)
            return EXIT_INPUT
        snapshot = parse_payload(text)
        backed = snapshot["fields"].get("decision_backed", "").strip().lower()
        if backed not in ("true", "false"):
            print(f"error: snapshot {display_path(path)} does not declare "
                  "`decision_backed: true|false`; the dispatch classification is mandatory",
                  file=sys.stderr)
            return EXIT_INPUT
        checked += 1
        for verdict in check_m06(snapshot):
            verdict["path"] = display_path(path)
            violations.append(verdict)
    return print_action_report("payload", PAYLOAD_RULES, checked, violations, args.json)


def run_chain(args) -> int:
    """M-05/M-07: chain snapshots carry the three segments with consistent ids."""
    snapshots = collect_snapshots(args.carrier, args.fixture)
    if not snapshots:
        print("error: --action chain needs --carrier or --fixture input", file=sys.stderr)
        return EXIT_INPUT
    violations: list[dict] = []
    checked = 0
    for path in snapshots:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"error: cannot read snapshot {path}: {exc}", file=sys.stderr)
            return EXIT_INPUT
        checked += 1
        for verdict in chain_verdicts(parse_chain(text)):
            verdict["path"] = display_path(path)
            violations.append(verdict)
    return print_action_report("chain", CHAIN_RULES, checked, violations, args.json)


def main(argv=None) -> int:
    _sig_guard(argv, declared=DECLARED_OPTIONS)
    parser = build_parser()
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    if args.action == "records":
        return run_records(args)
    if args.action == "payload":
        return run_payload(args)
    if args.action == "chain":
        return run_chain(args)

    # Interface final, judgement leg pending: the remaining declared action reports
    # not-implemented and exits as an input error, so an unimplemented check can never be
    # mistaken for a pass. The leg lands with US5 of feature 107.
    if args.json:
        print(json.dumps({"action": args.action, "status": "not-implemented",
                          "root": str(REPO_ROOT)}, ensure_ascii=False))
    print("error: action %r is declared but not implemented yet (read-only skeleton)"
          % args.action, file=sys.stderr)
    return EXIT_INPUT


if __name__ == "__main__":
    sys.exit(main())
