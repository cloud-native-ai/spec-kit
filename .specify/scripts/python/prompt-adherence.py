#!/usr/bin/env python3
"""``prompt-adherence.py`` — the read-only prompt-adherence reading engine (feature 109).

One deterministic, offline, stdlib-only script over records that already exist. It reads the
five declaration facts through ``scripts/python/declaration_reader.py``, the owner document
``shared/definitions/prompt-adherence-definitions.md`` (the machine-parsed catalog, blind-spot
register and reason tables), the runtime store layout fact, and the six sensor read surfaces
**through their owning engines, in process** — ``run-determination.py load_determinations``,
``exec-quant.py load_records``, ``feedback-utils.py scan_entries`` (metadata only),
``probe-utils.py load_probe_registry``, ``evidence-utils.py load_index`` plus the finding-item
projection pinned to the owning engines' constants. No second record parser exists here.

The reading is rebuilt on read: it writes nothing under any managed store root, keeps no cache
or lock, makes no network access, and carries no clock field — identical inputs reproduce a
byte-identical reading. It never emits an adherence verdict, composite score or ranking;
absence is ``not_evaluated`` / ``Unobserved`` with a reason, never clean and never breach.

This package delivers the per-run reading, the longitudinal window reading (``--since`` /
``--until``: half-open ``[since, until)`` on each record's own declared timestamp field, an
omitted bound printed as the literal ``open``, per-row state counts, the window-exempt
declaration-row note, and the bounded output lists), the interface surface and the
``--check-coverage`` action over the owner document's assumed-behavior coverage map.

Exit codes: 0 a reading was emitted (including status ``no-data`` / ``not-found``) or the
coverage check is clean; 1 the coverage check reported findings; 2 no reading can be produced —
an unusable declaration layer or owner document, an unknown token, or invalid arguments.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

_ENGINE_HOME = Path(__file__).resolve()
if str(_ENGINE_HOME.parent) not in sys.path:
    sys.path.insert(0, str(_ENGINE_HOME.parent))
import declaration_reader  # noqa: E402  (the one declaration-layer read entry)

try:  # the shared script-interface helper owns --version and undeclared-option rejection
    from script_interface_cli import configure_parser as _configure_parser
    from script_interface_cli import guard_argv as _guard_argv
    from script_interface_cli import resolve_version as _resolve_version
except ImportError:  # a sandbox copy carrying the engine but not the helper
    def _configure_parser(parser, **_kwargs):
        return parser

    def _guard_argv(_argv=None, declared=None, **_kwargs):
        return None

    def _resolve_version(_start=None):
        return "unknown"


#: Exit codes — the house table (0 emitted / 1 finding set / 2 no reading can be produced).
EXIT_OK = 0
EXIT_FINDINGS = 1
EXIT_INPUT = 2

READING_FORMAT = 1

#: The omitted-window-bound literal (FR-015): never resolved to a clock reading.
OPEN_BOUND = "open"

#: Output caps (owner document § Ordering, tie-breaks, duplicates and caps): bounds, never
#: judgement thresholds. Each truncation is disclosed with its total count.
SOURCES_CAP = 20
INVALID_SOURCES_CAP = 50
DUPLICATES_CAP = 20

#: The declaration-only row: it evaluates once against current state and is window-exempt.
WINDOW_EXEMPT_ROW = "probe-registry-declaration"

#: The engine's reason taxonomy (the tokens face of contract C-015; meanings owned by the owner
#: document's "Reason causes" / "Invalid-source causes" tables, pinned bidirectionally by the
#: declarations guard). Deliberately not a sixth declaration fact (FR-018).
ROW_REASON_CAUSES = ("source-unavailable", "no-matching-records", "invalid-source")
INVALID_SOURCE_CAUSES = (
    "unparsable",
    "schema-violation",
    "unknown-schema-version",
    "invalid-timestamp",
)

#: The five declaration facts this engine consumes (C-010/C-011; also the triple check's
#: read-point locator: each slug below is referenced where the fact is loaded).
FACT_SLUGS = (
    "prompt-adherence-layers",
    "prompt-adherence-strengths",
    "prompt-adherence-signals",
    "prompt-adherence-deviation-classes",
    "prompt-adherence-reading-status",
)

#: The runtime store layout fact: the one owner of the store roster. Each non-registry row's
#: root is the ``.specify/<store-name>/`` projection of its declared store name (FR-030); the
#: engine keeps no second root table.
STORE_LAYOUT_FACT = "runtime-store-layout"
STORE_ROOT_PREFIX = ".specify"

#: Owner document forms: framework-source first for a source-tree copy, installed form first
#: for a copy carrying a literal ``.specify`` component of its own resolved path (C-036).
OWNER_SOURCE_REL = "shared/definitions/prompt-adherence-definitions.md"
OWNER_INSTALLED_REL = ".specify/shared/definitions/prompt-adherence-definitions.md"

#: The gate-observation family prefix (declared by the confirmation-gates protocol; the
#: catalog's gate-row predicate cell must carry it — validated at read time).
GATE_FAMILY_PREFIX = "gate:"

#: Deviation-class tokens wired to their derivations (the schema face; membership in the
#: declaration set is validated at read time).
CLASS_AXIS_REGRESSION = "axis-regression"
CLASS_GREEN_UNPROVEN = "green-unproven"
CLASS_EVIDENCE_MISSING = "evidence-missing"

#: The evidence-state tokens the engine's derivation must name (schema face; membership in the
#: composed state domain is validated at read time). Every other state literal reaches the
#: output through a declaration: positive caps come from the catalog's "allowed_states" cells,
#: and the absence literal is read from the run-determination verdict domain.
UNOBSERVED_STATE = "Unobserved"
EVIDENCE_MISSING_STATE = "Missing"

#: Row -> read surface wiring. The row ids are the signals fact's declared tokens; a declared
#: member without wiring aborts the reading (unknown token, C-013). ``surface`` is the owning
#: engine's function the catalog's ``read_surface`` cell must name (C-032: a row bypasses no
#: owning read function).
ROW_WIRING = {
    "run-determination-record": ("run-determination", "run-determination.py::load_determinations"),
    "exec-quant-record": ("exec-quant", "exec-quant.py::load_records"),
    "feedback-entry": ("feedback-non-gate", "feedback-utils.py::scan_entries"),
    "gate-observation-record": ("feedback-gate", "feedback-utils.py::scan_entries"),
    "evidence-finding": ("evidence", "evidence-utils.py::load_index"),
    "probe-registry-declaration": ("probe-registry", "probe-utils.py::load_probe_registry"),
}

DECLARATION_ESTATE_ROOT = "registry"

EMPTY_CELLS = {"", "—", "-", "–", "none", "n/a"}

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
_SEPARATOR_RE = re.compile(r"^:?-{2,}:?$")
_TIMESTAMP_FORMATS = ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d")


class UsageError(Exception):
    """An input or declaration failure: exit 2, no reading is emitted."""


# --------------------------------------------------------------------------- #
# sibling engines (the measure.py in-process precedent)
# --------------------------------------------------------------------------- #
def _sibling(filename):
    """Import one sibling engine in process, or ``None`` when it cannot be loaded."""
    path = _ENGINE_HOME.parent / filename
    if not path.is_file():
        return None
    module_name = "_pa_" + filename.replace("-", "_").replace(".py", "")
    try:
        spec = importlib.util.spec_from_file_location(module_name, str(path))
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        sys.modules.setdefault(module_name, module)
        spec.loader.exec_module(module)
    except (OSError, ImportError, SyntaxError, ValueError):
        return None
    return module


# --------------------------------------------------------------------------- #
# declaration layer (C-010/C-011/C-013)
# --------------------------------------------------------------------------- #
def _install_dir_is_literal(path):
    """Copy-level self-location fires only on a literal ``.specify`` component (C-036)."""
    return any(part == ".specify" for part in Path(path).parts)


def _load_fact_members(repo):
    members = {}
    for slug in FACT_SLUGS:
        try:
            body = declaration_reader.load_fact(str(repo), slug)["body"]
        except declaration_reader.DeclarationError as error:
            raise UsageError("declaration layer unusable: %s" % error)
        values = body.get("statement")
        if not isinstance(values, list) or not values:
            raise UsageError("declaration %s carries no closed-set statement" % slug)
        members[slug] = [str(value) for value in values]
    return members


def _declaration_set_digest(repo):
    """SHA-256 over the five fact files: sorted repo-relative path plus bytes (FR-014)."""
    try:
        facts_dir = declaration_reader.layer_dir(str(repo)) / "facts"
    except declaration_reader.DeclarationError as error:
        raise UsageError("declaration layer unusable: %s" % error)
    digest = hashlib.sha256()
    paths = []
    for slug in sorted(FACT_SLUGS):
        path = facts_dir / (slug + ".yaml")
        if not path.is_file():
            raise UsageError("declaration fact file absent: %s.yaml" % slug)
        try:
            rel = declaration_reader.normalize_path(
                str(path.resolve().relative_to(Path(repo).resolve()))
            )
            payload = path.read_bytes()
        except (OSError, ValueError) as error:
            raise UsageError("declaration fact file unreadable: %s (%s)" % (path, error))
        paths.append(rel)
        digest.update(rel.encode("utf-8") + b"\0" + payload + b"\0")
    return digest.hexdigest(), paths


def _store_names(repo):
    """The declared runtime store roster, read through the declaration layer (FR-030)."""
    absent = declaration_reader.absent_label(STORE_LAYOUT_FACT)
    try:
        body = declaration_reader.load_fact(str(repo), STORE_LAYOUT_FACT)["body"]
    except declaration_reader.DeclarationError:
        raise UsageError("runtime store layout unusable: %s" % absent)
    statement = body.get("statement")
    stores = statement.get("stores") if isinstance(statement, dict) else None
    if not isinstance(stores, dict) or not stores:
        raise UsageError("runtime store layout carries no store roster: %s" % absent)
    return {str(name) for name in stores}


def _store_root(name):
    """The documented ``.specify/<store-name>/`` projection of one declared store name."""
    return STORE_ROOT_PREFIX + "/" + name


def _resolve_owner_document(repo):
    if _install_dir_is_literal(_ENGINE_HOME):
        candidates = (OWNER_INSTALLED_REL, OWNER_SOURCE_REL)
    else:
        candidates = (OWNER_SOURCE_REL, OWNER_INSTALLED_REL)
    for rel in candidates:
        candidate = Path(repo) / rel
        if candidate.is_file():
            return candidate
    raise UsageError("owner document absent: %s" % OWNER_SOURCE_REL)


# --------------------------------------------------------------------------- #
# the owner document's machine-parsed tables
# --------------------------------------------------------------------------- #
def _section(text, predicate):
    lines = text.splitlines()
    start = start_level = None
    for index, line in enumerate(lines):
        match = _HEADING_RE.match(line)
        if not match:
            continue
        level = len(match.group(1))
        label = match.group(2).strip()
        if start is None:
            if predicate(label):
                start, start_level = index + 1, level
        elif level <= start_level:
            return "\n".join(lines[start:index])
    if start is None:
        return None
    return "\n".join(lines[start:])


def _contains(fragment):
    return lambda label: fragment.lower() in label.lower()


def _cells(line):
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _tables(chunk):
    tables, current = [], []

    def flush():
        if len(current) >= 2:
            header = current[0]
            data = [
                row for row in current[1:]
                if not all(_SEPARATOR_RE.match(cell.replace(" ", "")) for cell in row if cell)
            ]
            tables.append((header, data))
        current.clear()

    for line in chunk.splitlines():
        stripped = line.strip()
        if len(stripped) > 2 and stripped.startswith("|") and stripped.endswith("|"):
            current.append(_cells(stripped))
        else:
            flush()
    flush()
    return tables


def _token(cell):
    return cell.replace("`", "").strip()


def _empty_cell(cell):
    """A cell that declares no value: the empty literals, or a dash-led annotation
    (``— (window-exempt)``) the owner document uses for the declaration row."""
    token = _token(cell)
    if token.lower() in EMPTY_CELLS:
        return True
    return token.startswith(("—", "–")) or (
        token.startswith("-") and (len(token) == 1 or token[1].isspace())
    )


def _split_tokens(cell):
    if _empty_cell(cell):
        return []
    return [_token(part) for part in _token(cell).split(",") if _token(part)]


def _column_exact(header, name):
    """The column whose label IS ``name`` (the owner document's headers are machine-parsed
    and pinned by the guard, so an absent column is an owner-document defect)."""
    for index, label in enumerate(header):
        if label.strip().lower() == name.lower():
            return index
    raise UsageError("owner-document table lacks the exact %r column (header: %r)" % (name, header))


def _column_ending(header, suffix):
    for index, label in enumerate(header):
        if label.strip().lower().endswith(suffix.lower()):
            return index
    raise UsageError("owner-document table lacks the %r column (header: %r)" % (suffix, header))


def _first_table(text, title):
    chunk = _section(text, _contains(title))
    if chunk is None:
        raise UsageError("owner document carries no %r section" % title)
    tables = _tables(chunk)
    if not tables:
        raise UsageError("owner document %r section carries no table" % title)
    return tables[0]


def _table_cause_members(text, title):
    header, rows = _first_table(text, title)
    cause_column = _column_ending(header, "cause")
    return [_token(row[cause_column]) for row in rows]


CATALOG_COLUMNS = (
    "row_id",
    "record_predicate",
    "store",
    "read_surface",
    "identity_fields",
    "timestamp_field",
    "layer",
    "strength",
    "allowed_states",
    "deviation_classes",
)


def _parse_catalog(text):
    chunk = _section(text, _contains("Signal Catalog"))
    if chunk is None:
        raise UsageError("owner document carries no 'Signal Catalog' section")
    for header, rows in _tables(chunk):
        if header and all(
            header[index].strip().lower() == name
            for index, name in enumerate(CATALOG_COLUMNS)
        ) and len(header) == len(CATALOG_COLUMNS):
            return _catalog_rows(header, rows)
    raise UsageError("owner document 'Signal Catalog' section carries no catalog table")


def _catalog_rows(header, rows):
    columns = {name: _column_exact(header, name) for name in CATALOG_COLUMNS}
    catalog = []
    for row in rows:
        row_id = _token(row[columns["row_id"]])
        if not row_id:
            continue
        catalog.append({
            "row": row_id,
            "predicate": row[columns["record_predicate"]],
            "store": _token(row[columns["store"]]),
            "read_surface": row[columns["read_surface"]],
            "identity_fields": _split_tokens(row[columns["identity_fields"]]),
            "timestamp_field": _token(row[columns["timestamp_field"]]),
            "layer": _token(row[columns["layer"]]),
            "strength": _token(row[columns["strength"]]),
            "allowed_states": _split_tokens(row[columns["allowed_states"]]),
            "deviation_classes": _split_tokens(row[columns["deviation_classes"]]),
        })
    if not catalog:
        raise UsageError("the catalog table carries no data rows")
    return catalog


def _parse_blind_spots(text):
    header, rows = _first_table(text, "Blind-Spot Register")
    class_column = _column_exact(header, "blind_spot")
    ids = [_token(row[class_column]) for row in rows]
    if not ids or not all(ids):
        raise UsageError("the blind-spot register carries an empty class id")
    if len(ids) != len(set(ids)):
        raise UsageError("the blind-spot register repeats a class id")
    return ids


# --------------------------------------------------------------------------- #
# the FR-003 coverage-map check (C-003)
# --------------------------------------------------------------------------- #
#: The two target kinds a coverage-map row may declare (data-model E-5).
COVERAGE_TARGET_KINDS = ("sensor", "blind-spot")


class CoverageResult:
    """The ``--check-coverage`` outcome: a sorted finding list, never a reading."""

    def __init__(self, findings):
        self.findings = list(findings)


def _parse_coverage_map(text):
    chunk = _section(text, _contains("coverage map"))
    if chunk is None:
        raise UsageError("owner document carries no machine-parsed coverage map")
    for header, rows in _tables(chunk):
        if header and header[0].strip().lower().startswith("assumed behavior"):
            return _coverage_rows(header, rows)
    raise UsageError("the coverage-map section carries no assumed-behavior table")


def _coverage_rows(header, rows):
    id_column = _column_exact(header, "Assumed behavior")
    kind_column = _column_exact(header, "Target kind")
    target_column = _column_exact(header, "Target")
    entries = []
    for row in rows:
        entry_id = _token(row[id_column])
        if not entry_id:
            continue
        entries.append({
            "id": entry_id,
            "kinds": _split_tokens(row[kind_column]),
            "targets": _split_tokens(row[target_column]),
        })
    if not entries:
        raise UsageError("the coverage map carries no assumed-behavior rows")
    return entries


def _coverage_findings(entries, catalog, blind_spots):
    """E-5's five checks; findings are plain sorted lines, the same text on every run."""
    row_ids = {row["row"] for row in catalog}
    spot_ids = set(blind_spots)
    findings = []
    occurrences = {}
    cited_rows, cited_spots = set(), set()
    for entry in entries:
        occurrences[entry["id"]] = occurrences.get(entry["id"], 0) + 1
        if len(entry["kinds"]) != 1 or len(entry["targets"]) != 1:
            findings.append(
                "coverage-map: multiple-targets: %s names %r target kind(s) and %r target(s); "
                "exactly one of each is required"
                % (entry["id"], entry["kinds"], entry["targets"])
            )
            continue
        kind, target = entry["kinds"][0], entry["targets"][0]
        if kind not in COVERAGE_TARGET_KINDS:
            findings.append(
                "coverage-map: unresolved-target: %s declares target kind %r; expected one of %r"
                % (entry["id"], kind, list(COVERAGE_TARGET_KINDS))
            )
        elif kind == "sensor":
            if target in row_ids:
                cited_rows.add(target)
            else:
                findings.append(
                    "coverage-map: unresolved-target: %s sensor target %r is not a catalog "
                    "row id" % (entry["id"], target)
                )
        elif target in spot_ids:
            cited_spots.add(target)
        else:
            findings.append(
                "coverage-map: unresolved-target: %s blind-spot target %r is not a register "
                "id" % (entry["id"], target)
            )
    for entry_id in sorted(occurrences):
        if occurrences[entry_id] > 1:
            findings.append(
                "coverage-map: duplicate-assumed-behavior: %s appears %d times"
                % (entry_id, occurrences[entry_id])
            )
    for row_id in sorted(row_ids - cited_rows):
        findings.append(
            "coverage-map: uncited-catalog-row: no assumed behavior cites %s" % row_id
        )
    for spot_id in sorted(spot_ids - cited_spots):
        findings.append(
            "coverage-map: uncited-blind-spot: no assumed behavior cites %s" % spot_id
        )
    return sorted(findings)


def _validate_registry(catalog, blind_spots, reason_causes, invalid_causes, members,
                       state_domain, stores):
    signals = members["prompt-adherence-signals"]
    row_ids = [row["row"] for row in catalog]
    if len(row_ids) != len(set(row_ids)):
        raise UsageError("the catalog repeats a row id: %r" % row_ids)
    if set(row_ids) != set(signals):
        raise UsageError(
            "catalog row ids %r disagree with the signals fact %r"
            % (sorted(row_ids), sorted(signals))
        )
    if set(signals) != set(ROW_WIRING):
        raise UsageError(
            "the signals fact declares a row with no engine read point: %r"
            % sorted(set(signals) ^ set(ROW_WIRING))
        )
    layers = set(members["prompt-adherence-layers"])
    strengths = set(members["prompt-adherence-strengths"])
    classes = set(members["prompt-adherence-deviation-classes"])
    used_layers, used_strengths, used_classes = set(), set(), set()
    for row in catalog:
        if row["layer"] not in layers:
            raise UsageError("catalog layer token %r is outside the layers fact" % row["layer"])
        if row["strength"] not in strengths:
            raise UsageError(
                "catalog strength token %r is outside the strengths fact" % row["strength"]
            )
        used_layers.add(row["layer"])
        used_strengths.add(row["strength"])
        for token in row["deviation_classes"]:
            if token not in classes:
                raise UsageError(
                    "catalog deviation class %r is outside the classes fact" % token
                )
            used_classes.add(token)
        if not row["allowed_states"]:
            raise UsageError("catalog row %r declares no positive state cap" % row["row"])
        for state in row["allowed_states"]:
            if state not in state_domain:
                raise UsageError(
                    "catalog allowed state %r is outside the composed state domain" % state
                )
        expected_reader, expected_surface = ROW_WIRING[row["row"]]
        if expected_surface not in row["read_surface"]:
            raise UsageError(
                "catalog row %r names read surface %r; the engine reads it through %r"
                % (row["row"], row["read_surface"], expected_surface)
            )
        declaration_row = expected_reader == "probe-registry"
        if declaration_row:
            if row["identity_fields"] or not _empty_cell(row["timestamp_field"]):
                raise UsageError(
                    "the declaration row %r must declare no identity or timestamp field"
                    % row["row"]
                )
            if row["store"] != DECLARATION_ESTATE_ROOT:
                raise UsageError(
                    "the declaration row %r must name %r as its store"
                    % (row["row"], DECLARATION_ESTATE_ROOT)
                )
            continue
        if not row["identity_fields"]:
            raise UsageError("catalog row %r declares no identity field" % row["row"])
        if _empty_cell(row["timestamp_field"]):
            raise UsageError("catalog row %r declares no timestamp field" % row["row"])
        if row["store"] not in stores:
            raise UsageError(
                "catalog row %r names store %r, which the runtime store layout does not declare"
                % (row["row"], row["store"])
            )
        if row["row"] == "gate-observation-record" and GATE_FAMILY_PREFIX not in row["predicate"]:
            raise UsageError(
                "the gate-observation row's predicate does not carry the declared %r prefix"
                % GATE_FAMILY_PREFIX
            )
    if used_layers != layers:
        raise UsageError(
            "declared layer tokens unused by the catalog: %r" % sorted(layers - used_layers)
        )
    if used_strengths != strengths:
        raise UsageError(
            "declared strength tokens unused by the catalog: %r" % sorted(strengths - used_strengths)
        )
    if used_classes != classes:
        raise UsageError(
            "declared deviation classes unused by the catalog: %r" % sorted(classes - used_classes)
        )
    if set(reason_causes) != set(ROW_REASON_CAUSES):
        raise UsageError(
            "owner-document reason causes %r disagree with the engine schema %r"
            % (sorted(reason_causes), sorted(ROW_REASON_CAUSES))
        )
    if set(invalid_causes) != set(INVALID_SOURCE_CAUSES):
        raise UsageError(
            "owner-document invalid-source causes %r disagree with the engine schema %r"
            % (sorted(invalid_causes), sorted(INVALID_SOURCE_CAUSES))
        )
    if not blind_spots:
        raise UsageError("the blind-spot register is empty")


# --------------------------------------------------------------------------- #
# small deterministic helpers
# --------------------------------------------------------------------------- #
def _parse_timestamp(value):
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    for fmt in _TIMESTAMP_FORMATS:
        try:
            return datetime.strptime(text, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    try:
        stamp = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    return stamp if stamp.tzinfo else stamp.replace(tzinfo=timezone.utc)


def _relative(workspace, path):
    try:
        return Path(path).resolve().relative_to(Path(workspace).resolve()).as_posix()
    except ValueError:
        return Path(path).as_posix()


def _record(identity, timestamp, store, path, record, field, classes):
    return {
        "identity": identity,
        "timestamp": timestamp,
        "stamp": _parse_timestamp(timestamp),
        "store": store,
        "path": path,
        "record": record,
        "field": field,
        "classes": list(classes),
    }


def _read_result(available=True, records=None, invalid=None):
    return {
        "available": available,
        "records": records or [],
        "invalid": invalid or [],
    }


def _unavailable():
    return _read_result(available=False)


# --------------------------------------------------------------------------- #
# the six sensor reads — each through its owning engine's read surface
# --------------------------------------------------------------------------- #
def _negative_verdicts(run_determination):
    """The source engine's own *negative* axis verdicts, read from its declared domains."""
    good = set(run_determination.GOOD_VERDICTS)
    domains = set(run_determination.COMPARISON_VERDICTS) | set(
        run_determination.CORRECTNESS_VERDICTS
    )
    absent = run_determination.GREEN_UNPROVEN_VERDICT[0]
    return domains - good - {absent}


def _read_run_determination(workspace, row, sensors):
    root = Path(workspace) / _store_root(row["store"])
    if not root.is_dir():
        return _unavailable()
    engine = sensors.get("run-determination")
    if engine is None:
        return _unavailable()
    try:
        determinations = engine.load_determinations(Path(workspace))
    except (OSError, ValueError):
        return _unavailable()
    identity_field = row["identity_fields"][0]
    timestamp_field = row["timestamp_field"]
    negative = _negative_verdicts(engine)
    green_pair = tuple(engine.GREEN_UNPROVEN_VERDICT)
    records, invalid = [], []
    for item in determinations:
        path = _relative(workspace, item["path"])
        body = item["record"]
        if body.get("schema_version") != engine.SCHEMA_VERSION:
            invalid.append((path, "unknown-schema-version"))
            continue
        stamp = _parse_timestamp(body.get(timestamp_field))
        if stamp is None:
            invalid.append((path, "invalid-timestamp"))
            continue
        identity = body.get(identity_field)
        if not isinstance(identity, str) or not identity.strip():
            invalid.append((path, "schema-violation"))
            continue
        classes = []
        axes = body.get("axes") if isinstance(body.get("axes"), dict) else {}
        verdicts = [axis for axis in axes.values() if isinstance(axis, dict)]
        if any(axis.get("verdict") in negative for axis in verdicts):
            classes.append(CLASS_AXIS_REGRESSION)
        if any((axis.get("verdict"), axis.get("reason")) == green_pair for axis in verdicts):
            classes.append(CLASS_GREEN_UNPROVEN)
        records.append(
            _record(identity, body.get(timestamp_field), row["store"], path, identity,
                    identity_field, classes)
        )
    return _read_result(records=records, invalid=invalid)


def _exec_quant_surfaces(root):
    """Every record surface under the exec-quant store, parsed once to bind paths and to name
    the files the owning reader could not hand back (measure.py's identity-binding precedent).
    """
    surfaces = []
    legacy = root / "records.jsonl"
    if legacy.is_file():
        try:
            lines = legacy.read_text(encoding="utf-8").splitlines()
        except OSError:
            lines = []
        parsed = []
        bad = 0
        for line in lines:
            if not line.strip():
                continue
            try:
                node = json.loads(line)
            except ValueError:
                bad += 1
                continue
            if isinstance(node, dict):
                parsed.append(node)
            else:
                bad += 1
        surfaces.append((legacy, parsed, bad))
    records_dir = root / "records"
    if records_dir.is_dir():
        for path in sorted(records_dir.glob("*.json")):
            try:
                node = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                surfaces.append((path, [], 1))
                continue
            if isinstance(node, dict):
                surfaces.append((path, [node], 0))
            else:
                surfaces.append((path, [], 1))
    return surfaces


def _read_exec_quant(workspace, row, sensors):
    root = Path(workspace) / _store_root(row["store"])
    if not root.is_dir():
        return _unavailable()
    engine = sensors.get("exec-quant")
    if engine is None:
        return _unavailable()
    try:
        records_in_store = engine.load_records(Path(workspace))
    except (OSError, ValueError):
        return _unavailable()
    surfaces = _exec_quant_surfaces(root)
    invalid = []
    entry_nodes = []
    for path, nodes, bad in surfaces:
        rel = _relative(workspace, path)
        invalid.extend((rel, "unparsable") for _ in range(bad))
        entry_nodes.extend((rel, node) for node in nodes)
    identity_field = row["identity_fields"][0]
    timestamp_field = row["timestamp_field"]
    records = []
    for body in records_in_store:
        path = next((rel for rel, node in entry_nodes if node == body), None)
        if path is None:
            path = row["store"]
        if body.get("kind") != engine.KIND:
            invalid.append((path, "schema-violation"))
            continue
        if body.get("schema_version") != engine.SCHEMA_VERSION:
            invalid.append((path, "unknown-schema-version"))
            continue
        stamp = _parse_timestamp(body.get(timestamp_field))
        if stamp is None:
            invalid.append((path, "invalid-timestamp"))
            continue
        identity = body.get(identity_field)
        if not isinstance(identity, str) or not identity.strip():
            invalid.append((path, "schema-violation"))
            continue
        records.append(
            _record(identity, body.get(timestamp_field), row["store"], path, identity,
                    identity_field, [])
        )
    return _read_result(records=records, invalid=invalid)


def _read_feedback(workspace, row, sensors, gate_family):
    root = Path(workspace) / _store_root(row["store"])
    if not root.is_dir():
        return _unavailable()
    engine = sensors.get("feedback-utils")
    if engine is None:
        return _unavailable()
    try:
        entries = engine.scan_entries(Path(workspace))
    except (OSError, ValueError):
        return _unavailable()
    identity_field = row["identity_fields"][0]
    timestamp_field = row["timestamp_field"]
    records, invalid = [], []
    for entry in entries:
        run_id = str(entry.get("run_id") or "")
        if run_id.startswith(GATE_FAMILY_PREFIX) != gate_family:
            continue
        path = _store_root(row["store"]) + "/" + str(entry.get("file") or "")
        stamp = _parse_timestamp(entry.get(timestamp_field))
        if stamp is None:
            invalid.append((path, "invalid-timestamp"))
            continue
        if not run_id:
            invalid.append((path, "schema-violation"))
            continue
        record_id = str(entry.get("id") or Path(str(entry.get("file") or "entry")).stem)
        records.append(
            _record(run_id, entry.get(timestamp_field), row["store"], path, record_id,
                    identity_field, [])
        )
    return _read_result(records=records, invalid=invalid)


def _read_feedback_non_gate(workspace, row, sensors):
    return _read_feedback(workspace, row, sensors, gate_family=False)


def _read_feedback_gate(workspace, row, sensors):
    return _read_feedback(workspace, row, sensors, gate_family=True)


def _read_evidence(workspace, row, sensors):
    root = Path(workspace) / _store_root(row["store"])
    if not root.is_dir():
        return _unavailable()
    engine = sensors.get("evidence-utils")
    projector = sensors.get("run-determination")
    if engine is None or projector is None:
        return _unavailable()
    try:
        index = engine.load_index(Path(workspace))
    except (OSError, ValueError):
        return _unavailable()
    by_file = {str(entry.get("file") or ""): entry for entry in index.get("entries") or []}
    states_domain = set(getattr(engine, "SEVEN_STATES", ()))
    projection_fields = tuple(getattr(projector, "FINDINGS_PROJECTION_FIELDS", ()))
    identity_field = row["identity_fields"][0]
    timestamp_field = row["timestamp_field"]
    records, invalid = [], []
    try:
        run_dirs = sorted(path for path in root.iterdir() if path.is_dir())
    except OSError:
        return _unavailable()
    for run_dir in run_dirs:
        findings_path = run_dir / "findings.json"
        if not findings_path.is_file():
            continue
        rel = _relative(workspace, findings_path)
        try:
            findings = json.loads(findings_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            invalid.append((rel, "unparsable"))
            continue
        if not isinstance(findings, dict):
            invalid.append((rel, "unparsable"))
            continue
        if findings.get("kind") != engine.FINDINGS_KIND:
            invalid.append((rel, "schema-violation"))
            continue
        if findings.get("schemaVersion") != engine.SCHEMA_VERSION:
            invalid.append((rel, "unknown-schema-version"))
            continue
        entry = by_file.get((Path(run_dir.name) / "findings.json").as_posix(), {})
        stamp = _parse_timestamp(entry.get(timestamp_field))
        if stamp is None:
            invalid.append((rel, "invalid-timestamp"))
            continue
        identity = findings.get(identity_field) or entry.get(identity_field)
        if not isinstance(identity, str) or not identity.strip():
            invalid.append((rel, "schema-violation"))
            continue
        items = findings.get("evidence") if isinstance(findings.get("evidence"), list) else []
        projection = [
            {field: item.get(field) for field in projection_fields}
            for item in items if isinstance(item, dict)
        ]
        item_states = [str(item.get("evidenceState")) for item in projection]
        if any(state not in states_domain for state in item_states):
            invalid.append((rel, "schema-violation"))
            continue
        classes = [CLASS_EVIDENCE_MISSING] if EVIDENCE_MISSING_STATE in item_states else []
        records.append(
            _record(identity, entry.get(timestamp_field), row["store"], rel, identity,
                    identity_field, classes)
        )
    return _read_result(records=records, invalid=invalid)


def _read_probe_registry(workspace, row, sensors):
    engine = sensors.get("probe-utils")
    if engine is None:
        return _unavailable()
    registry_rel = Path(engine.PROBE_DEFS_REL).as_posix()
    if not (Path(workspace) / registry_rel).is_file():
        return _unavailable()
    try:
        registry = engine.load_probe_registry(Path(workspace))
    except (OSError, ValueError):
        return _unavailable()
    if not registry.get("available"):
        return _unavailable()
    objects = list(registry.get("objects") or []) + list(registry.get("external") or [])
    if registry.get("errors"):
        return _read_result(records=[], invalid=[(registry_rel, "schema-violation")])
    if not objects:
        return _read_result(records=[], invalid=[])
    records = [
        _record(DECLARATION_ESTATE_ROOT, None, DECLARATION_ESTATE_ROOT, registry_rel,
                DECLARATION_ESTATE_ROOT, "objects", [])
    ]
    return _read_result(records=records, invalid=[])


READERS = {
    "run-determination": _read_run_determination,
    "exec-quant": _read_exec_quant,
    "feedback-non-gate": _read_feedback_non_gate,
    "feedback-gate": _read_feedback_gate,
    "evidence": _read_evidence,
    "probe-registry": _read_probe_registry,
}


# --------------------------------------------------------------------------- #
# scope resolution and observation derivation (C-021, E-6, I-4)
# --------------------------------------------------------------------------- #
def _resolve_scope(catalog_reads, explicit_run):
    if explicit_run is not None:
        return {
            "kind": "run",
            "run": explicit_run,
            "window": None,
            "resolution": "explicit",
            "basis": None,
        }
    candidates = []
    for row, read in catalog_reads:
        if ROW_WIRING[row["row"]][0] == "probe-registry":
            continue
        for record in read["records"]:
            if record["stamp"] is None:
                continue
            candidates.append((record, row))
    if not candidates:
        return {
            "kind": "run",
            "run": None,
            "window": None,
            "resolution": "none",
            "basis": None,
        }
    winner, _row = min(
        candidates,
        key=lambda pair: (
            -pair[0]["stamp"].timestamp(),
            pair[0]["store"],
            pair[0]["path"],
            pair[0]["identity"],
        ),
    )
    return {
        "kind": "run",
        "run": winner["identity"],
        "window": None,
        "resolution": "most-recent",
        "basis": {
            "store": winner["store"],
            "path": winner["path"],
            "timestamp": winner["timestamp"],
        },
    }


def _absence(row, state, cause, source):
    return {
        "row": row["row"],
        "layer": row["layer"],
        "strength": row["strength"],
        "state": state,
        "deviation_classes": [],
        "reason": {"cause": cause, "source": source},
        "sources": [],
    }


def _positive(row, read, state_domain):
    state = row["allowed_states"][0]
    if state not in state_domain:
        raise UsageError("row %r reaches an undeclared positive state %r" % (row["row"], state))
    derived = {token for record_item in read["records"] for token in record_item["classes"]}
    classes = [token for token in row["deviation_classes"] if token in derived]
    sources = [
        {
            "store": item["store"],
            "path": item["path"],
            "record": item["record"],
            "field": item["field"],
        }
        for item in sorted(read["records"], key=lambda item: (item["path"], item["record"]))
    ]
    return {
        "row": row["row"],
        "layer": row["layer"],
        "strength": row["strength"],
        "state": state,
        "deviation_classes": classes,
        "reason": None,
        "sources": sources,
    }


def _derive_observation(row, read, scope, state_domain, absent_literal):
    """E-6's four-way derivation for a per-run scope. Returns ``(observation, matched)``
    where ``matched`` is the list of records the observation was derived from.
    """
    store_label = _store_root(row["store"])
    declaration_row = ROW_WIRING[row["row"]][0] == "probe-registry"
    explicit_run = scope["resolution"] == "explicit"
    if not read["available"]:
        return _absence(row, absent_literal, "source-unavailable", store_label), []
    if declaration_row:
        if explicit_run and read["records"]:
            return _absence(row, absent_literal, "no-matching-records", store_label), []
        if read["records"]:
            return _positive(row, read, state_domain), []
        if read["invalid"]:
            return _absence(row, absent_literal, "invalid-source", store_label), []
        state = absent_literal if explicit_run else UNOBSERVED_STATE
        return _absence(row, state, "no-matching-records", store_label), []
    matched = [
        record
        for record in read["records"]
        if scope["run"] is not None and record["identity"] == scope["run"]
    ]
    if matched:
        scoped = dict(read)
        scoped["records"] = matched
        return _positive(row, scoped, state_domain), matched
    if not read["records"] and read["invalid"]:
        return _absence(row, absent_literal, "invalid-source", store_label), []
    if explicit_run:
        return _absence(row, absent_literal, "no-matching-records", store_label), []
    return _absence(row, UNOBSERVED_STATE, "no-matching-records", store_label), []


def _in_window(stamp, window):
    if stamp is None:
        return False
    if window["since"] is not None and stamp < window["since"]:
        return False
    if window["until"] is not None and stamp >= window["until"]:
        return False
    return True


def _derive_window_observation(row, read, window, state_domain, absent_literal):
    """E-6's derivation under a window scope: each record's own timestamp decides membership
    in the half-open interval. Returns ``(observation, matched)``; the observation carries
    the per-state counts (``state_counts``) — longitudinal readings only.
    """
    store_label = _store_root(row["store"])
    declaration_row = ROW_WIRING[row["row"]][0] == "probe-registry"
    if not read["available"]:
        observation = _absence(row, absent_literal, "source-unavailable", store_label)
        observation["state_counts"] = {}
        return observation, []
    if declaration_row:
        if read["records"]:
            observation = _positive(row, read, state_domain)
        elif read["invalid"]:
            observation = _absence(row, absent_literal, "invalid-source", store_label)
        else:
            observation = _absence(row, UNOBSERVED_STATE, "no-matching-records", store_label)
        observation["state_counts"] = {}
        return observation, []
    matched = [record for record in read["records"] if _in_window(record["stamp"], window)]
    if matched:
        scoped = dict(read)
        scoped["records"] = matched
        observation = _positive(row, scoped, state_domain)
        observation["state_counts"] = {row["allowed_states"][0]: len(matched)}
        return observation, matched
    if not read["records"] and read["invalid"]:
        observation = _absence(row, absent_literal, "invalid-source", store_label)
    else:
        observation = _absence(row, UNOBSERVED_STATE, "no-matching-records", store_label)
    observation["state_counts"] = {}
    return observation, []


def _status(explicit_run, records_in_scope, observations, status_members, absent_literal):
    if records_in_scope == 0:
        status = "not-found" if explicit_run else "no-data"
    elif any(obs["state"] == absent_literal for obs in observations):
        status = "partial"
    else:
        status = "complete"
    if status not in status_members:
        raise UsageError(
            "derived reading status %r is outside the declared reading-status fact" % status
        )
    return status


def _duplicates(matched_by_row):
    duplicates = []
    for row_id, records in matched_by_row.items():
        groups = {}
        for record in records:
            key = (record["identity"], record["timestamp"])
            groups.setdefault(key, []).append(record)
        for (identity, timestamp), members in sorted(groups.items()):
            if len(members) < 2:
                continue
            duplicates.append({
                "row": row_id,
                "identity": "%s@%s" % (identity, timestamp),
                "count": len(members) - 1,
                "paths": sorted(record["path"] for record in members),
            })
    duplicates.sort(key=lambda item: (item["row"], item["identity"]))
    return duplicates


def _window_scope(window):
    """E-9's window scope; the declaration row is marked window-exempt in the scope notes
    (C-022), so a declaration-only row is never faked into a timestamped series.
    """
    return {
        "kind": "window",
        "run": None,
        "window": {"since": window["since_text"], "until": window["until_text"]},
        "resolution": "explicit",
        "basis": None,
        "notes": [
            "%s is window-exempt: it evaluates once against current state" % WINDOW_EXEMPT_ROW
        ],
    }


def _apply_output_caps(observations, invalid_list, duplicates):
    """The owner document's output caps (20 / 50 / 20): each truncation carries its
    shown/total disclosure. Caps are output bounds by construction, never thresholds.
    """
    truncations = []
    for observation in observations:
        sources = observation["sources"]
        if len(sources) > SOURCES_CAP:
            observation["sources"] = sources[:SOURCES_CAP]
            truncations.append({
                "list": "sources",
                "row": observation["row"],
                "shown": SOURCES_CAP,
                "total": len(sources),
            })
    if len(invalid_list) > INVALID_SOURCES_CAP:
        truncations.append({
            "list": "invalid_sources",
            "row": None,
            "shown": INVALID_SOURCES_CAP,
            "total": len(invalid_list),
        })
        invalid_list = invalid_list[:INVALID_SOURCES_CAP]
    if len(duplicates) > DUPLICATES_CAP:
        truncations.append({
            "list": "duplicates",
            "row": None,
            "shown": DUPLICATES_CAP,
            "total": len(duplicates),
        })
        duplicates = duplicates[:DUPLICATES_CAP]
    truncations.sort(key=lambda item: (item["list"], item["row"] or "", item["total"]))
    return invalid_list, duplicates, truncations


# --------------------------------------------------------------------------- #
# the reading assembly (C-020/C-023/C-025/C-026/C-027)
# --------------------------------------------------------------------------- #
def _build_reading(args, engine_home, repo, window=None):
    members = _load_fact_members(repo)
    declaration_version, fact_paths = _declaration_set_digest(repo)
    sensors = {
        name: _sibling(filename)
        for name, filename in (
            ("run-determination", "run-determination.py"),
            ("exec-quant", "exec-quant.py"),
            ("feedback-utils", "feedback-utils.py"),
            ("probe-utils", "probe-utils.py"),
            ("evidence-utils", "evidence-utils.py"),
        )
    }
    run_determination = sensors.get("run-determination")
    evidence_utils = sensors.get("evidence-utils")
    if run_determination is None:
        raise UsageError("sibling engine unavailable: scripts/python/run-determination.py")
    if evidence_utils is None:
        raise UsageError("sibling engine unavailable: scripts/python/evidence-utils.py")
    seven_states = [str(state) for state in getattr(evidence_utils, "SEVEN_STATES", ())]
    if not seven_states:
        raise UsageError("the evidence seven-state composition is unavailable (evidence-seven-states)")
    absent_literal = run_determination.GREEN_UNPROVEN_VERDICT[0]
    state_domain = set(seven_states) | {absent_literal}
    for token in (EVIDENCE_MISSING_STATE, UNOBSERVED_STATE):
        if token not in state_domain:
            raise UsageError(
                "engine state token %r is outside the composed state domain" % token
            )
    class_members = set(members["prompt-adherence-deviation-classes"])
    for token in (CLASS_AXIS_REGRESSION, CLASS_GREEN_UNPROVEN, CLASS_EVIDENCE_MISSING):
        if token not in class_members:
            raise UsageError("engine deviation-class token %r is outside the classes fact" % token)

    owner_path = _resolve_owner_document(repo)
    try:
        owner_text = owner_path.read_text(encoding="utf-8")
    except OSError as error:
        raise UsageError("owner document unreadable: %s (%s)" % (owner_path, error))
    catalog = _parse_catalog(owner_text)
    blind_spots = _parse_blind_spots(owner_text)
    reason_causes = _table_cause_members(owner_text, "Reason causes")
    invalid_causes = _table_cause_members(owner_text, "Invalid-source causes")
    stores = _store_names(repo)
    _validate_registry(
        catalog, blind_spots, reason_causes, invalid_causes, members, state_domain, stores
    )
    for row in catalog:
        if ROW_WIRING[row["row"]][0] != "probe-registry":
            row["store_root"] = _store_root(row["store"])
        else:
            row["store_root"] = DECLARATION_ESTATE_ROOT

    if args.check_coverage:
        return CoverageResult(
            _coverage_findings(_parse_coverage_map(owner_text), catalog, blind_spots)
        )

    workspace = Path(args.workspace_root).expanduser().resolve() if args.workspace_root \
        else _workspace_from_cwd()
    catalog_reads = []
    invalid_sources = []
    for row in catalog:
        reader = READERS[ROW_WIRING[row["row"]][0]]
        read = reader(workspace, row, sensors)
        catalog_reads.append((row, read))
        invalid_sources.extend(read["invalid"])
    invalid_sources = sorted(invalid_sources, key=lambda pair: (pair[0], pair[1]))
    invalid_list = [{"path": path, "cause": cause} for path, cause in invalid_sources]
    invalid_total = len(invalid_list)

    scope = _window_scope(window) if window is not None else _resolve_scope(catalog_reads, args.run)
    observations = []
    matched_by_row = {}
    records_in_scope = 0
    for row, read in catalog_reads:
        if window is not None:
            observation, matched = _derive_window_observation(
                row, read, window, state_domain, absent_literal
            )
        else:
            observation, matched = _derive_observation(
                row, read, scope, state_domain, absent_literal
            )
        observations.append(observation)
        records_in_scope += len(matched)
        if matched and ROW_WIRING[row["row"]][0] != "probe-registry":
            matched_by_row[row["row"]] = matched
    for observation in observations:
        if observation["state"] not in state_domain:
            raise UsageError(
                "emitted observation state %r is outside the composed state domain"
                % observation["state"]
            )

    status_members = set(members["prompt-adherence-reading-status"])
    status = _status(
        window is None and scope["resolution"] == "explicit", records_in_scope,
        observations, status_members, absent_literal,
    )
    duplicates = _duplicates(matched_by_row)
    invalid_list, duplicates, truncations = _apply_output_caps(
        observations, invalid_list, duplicates
    )
    observable = [
        observation["row"]
        for observation, row in zip(observations, catalog)
        if observation["state"] in row["allowed_states"]
    ]
    not_observable = [
        observation["row"]
        for observation, row in zip(observations, catalog)
        if observation["state"] not in row["allowed_states"]
    ]
    coverage = {
        "observable": observable,
        "not_observable": not_observable,
        "blind_spots": blind_spots,
        "records_in_scope": records_in_scope,
        "invalid_records": invalid_total,
    }
    engine_relative = _relative(repo, engine_home)
    reading = {
        "reading_format": READING_FORMAT,
        "engine": {
            "path": engine_relative,
            "version": _resolve_version(engine_home),
        },
        "declaration_set": {
            "version": declaration_version,
            "facts": sorted(fact_paths),
        },
        "scope": scope,
        "status": status,
        "observations": observations,
        "coverage": coverage,
        "invalid_sources": invalid_list,
        "duplicates": duplicates,
    }
    if truncations:
        reading["truncations"] = truncations
    return reading


def _workspace_from_cwd():
    current = Path.cwd().resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".specify").is_dir():
            return candidate
    return current


# --------------------------------------------------------------------------- #
# the two projections of ONE computed structure (C-023)
# --------------------------------------------------------------------------- #
def _render_json(reading):
    return json.dumps(reading, indent=2, sort_keys=True, ensure_ascii=False)


def _render_human(reading):
    lines = [
        "prompt-adherence reading",
        "reading-format: %d" % reading["reading_format"],
        "engine: %s %s" % (reading["engine"]["path"], reading["engine"]["version"]),
        "declaration-set: %s" % reading["declaration_set"]["version"],
        "facts: %s" % ", ".join(reading["declaration_set"]["facts"]),
    ]
    scope = reading["scope"]
    if scope["kind"] == "window":
        window = scope["window"]
        lines.append("scope: window [%s, %s)" % (window["since"], window["until"]))
        lines.append("scope-resolution: %s" % scope["resolution"])
        lines.append("window-since: %s" % window["since"])
        lines.append("window-until: %s" % window["until"])
        for note in scope.get("notes") or []:
            lines.append("scope-note: %s" % note)
    else:
        lines.append("scope: run %s" % (scope["run"] if scope["run"] is not None else "none"))
        lines.append("scope-resolution: %s" % scope["resolution"])
        if scope["basis"]:
            lines.append(
                "scope-basis: store=%s path=%s timestamp=%s"
                % (scope["basis"]["store"], scope["basis"]["path"], scope["basis"]["timestamp"])
            )
    lines.append("status: %s" % reading["status"])
    longitudinal = scope["kind"] == "window"
    for observation in reading["observations"]:
        line = "row %s layer=%s strength=%s state=%s" % (
            observation["row"],
            observation["layer"],
            observation["strength"],
            observation["state"],
        )
        if observation["deviation_classes"]:
            line += " classes=%s" % ",".join(observation["deviation_classes"])
        if observation["reason"]:
            line += " reason=%s source=%s" % (
                observation["reason"]["cause"],
                observation["reason"]["source"],
            )
        if longitudinal and observation["row"] == WINDOW_EXEMPT_ROW:
            line += " window-exempt"
        lines.append(line)
        if "state_counts" in observation:
            counts = observation["state_counts"]
            body = ",".join("%s=%d" % (state, counts[state]) for state in sorted(counts))
            lines.append("state-counts %s %s" % (observation["row"], body or "none"))
        for source in observation["sources"]:
            lines.append(
                "source %s store=%s path=%s record=%s field=%s"
                % (
                    observation["row"],
                    source["store"],
                    source["path"],
                    source["record"],
                    source["field"],
                )
            )
    coverage = reading["coverage"]
    lines.append(
        "coverage-observable: %s" % (", ".join(coverage["observable"]) or "none")
    )
    lines.append(
        "coverage-not-observable: %s" % (", ".join(coverage["not_observable"]) or "none")
    )
    lines.append("coverage-blind-spots: %s" % ", ".join(coverage["blind_spots"]))
    lines.append("coverage-records-in-scope: %d" % coverage["records_in_scope"])
    lines.append("coverage-invalid-records: %d" % coverage["invalid_records"])
    for entry in reading["invalid_sources"]:
        lines.append("invalid-source %s %s" % (entry["path"], entry["cause"]))
    for duplicate in reading["duplicates"]:
        lines.append(
            "duplicate %s %s count=%d paths=%s"
            % (
                duplicate["row"],
                duplicate["identity"],
                duplicate["count"],
                ",".join(duplicate["paths"]),
            )
        )
    for truncation in reading.get("truncations") or []:
        prefix = "truncated %s" % truncation["list"]
        if truncation["row"] is not None:
            prefix += " row=%s" % truncation["row"]
        lines.append(
            "%s shown=%d total=%d" % (prefix, truncation["shown"], truncation["total"])
        )
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# interface (C-030/C-031)
# --------------------------------------------------------------------------- #
_DECLARED_FLAGS = [
    "--run",
    "--since",
    "--until",
    "--json",
    "--workspace-root",
    "--check-coverage",
]


def build_parser():
    parser = argparse.ArgumentParser(
        prog="prompt-adherence.py",
        description=(
            "Read-only prompt-adherence reading over the existing runtime stores "
            "(feature 109). One documented invocation prints the human-readable per-run "
            "reading for the default scope; --run pins one run identity; --since / --until "
            "request the longitudinal window reading; --json emits the machine-readable form."
        ),
    )
    _configure_parser(
        parser,
        effects=(
            "none — a reading reads the declaration layer, the owner document and the six "
            "existing sensor stores; it writes nothing, keeps no cache or lock, and makes no "
            "network access"
        ),
        codes=(
            "0 a reading was emitted (including status no-data / not-found); 1 the coverage "
            "check reported findings; 2 no reading can be produced (unusable declaration "
            "layer or owner document, unknown token, invalid arguments)"
        ),
    )
    parser.add_argument(
        "--run", default=None, metavar="RUN_ID", help="pin one run identity"
    )
    parser.add_argument(
        "--since", default=None, metavar="BOUND",
        help="window start, inclusive (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ, UTC); requests "
             "the longitudinal reading; omitted for an --until-only window",
    )
    parser.add_argument(
        "--until", default=None, metavar="BOUND",
        help="window end, exclusive (same forms as --since); omitted prints as the literal "
             "open",
    )
    parser.add_argument(
        "--json", action="store_true", help="emit the machine-readable reading form"
    )
    parser.add_argument(
        "--workspace-root", default=None, metavar="PATH",
        help="the project whose stores are read (default: walk up to the nearest .specify/)",
    )
    parser.add_argument(
        "--check-coverage", action="store_true",
        help="run the FR-003 coverage-map check over the owner document",
    )
    return parser


def _bound(value, flag):
    """One window bound: the two declared forms only (PA-13); an omitted bound is ``open``."""
    if value is None:
        return None, OPEN_BOUND
    text = value.strip()
    for fmt in _TIMESTAMP_FORMATS:
        try:
            stamp = datetime.strptime(text, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
        return stamp, stamp.strftime("%Y-%m-%dT%H:%M:%SZ")
    raise UsageError(
        "invalid %s value: %r (expected YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)" % (flag, value)
    )


def _window_request(args):
    """The window scope request, or None for the per-run path: half-open [since, until) on
    each record's own timestamp field; an omitted bound is the literal ``open``; --run
    combined with either bound is an input error (C-021/C-022).
    """
    if args.since is None and args.until is None:
        return None
    if args.run is not None:
        raise UsageError("--run cannot be combined with --since/--until (input error)")
    since, since_text = _bound(args.since, "--since")
    until, until_text = _bound(args.until, "--until")
    return {
        "since": since,
        "until": until,
        "since_text": since_text,
        "until_text": until_text,
    }


def main(argv=None):
    _guard_argv(argv, declared=_DECLARED_FLAGS)
    args = build_parser().parse_args(argv)
    try:
        window = _window_request(args)
        repo = Path(declaration_reader.find_repo(_ENGINE_HOME))
        reading = _build_reading(args, _ENGINE_HOME, repo, window)
    except UsageError as error:
        print("prompt-adherence: %s" % error, file=sys.stderr)
        return EXIT_INPUT
    except declaration_reader.DeclarationError as error:
        print("prompt-adherence: declaration layer unusable: %s" % error, file=sys.stderr)
        return EXIT_INPUT
    if isinstance(reading, CoverageResult):
        for line in reading.findings:
            print(line)
        if reading.findings:
            return EXIT_FINDINGS
        print("coverage-map: ok (0 findings)")
        return EXIT_OK
    if args.json:
        print(_render_json(reading))
    else:
        print(_render_human(reading))
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())