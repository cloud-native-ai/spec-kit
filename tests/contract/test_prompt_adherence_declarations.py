"""Contract tests for the five prompt-adherence declaration facts (109, C-010…C-016).

**Red-first (T004).** This module was authored before the five facts, the owner document and the engine
existed; the red run is recorded in `.specify/specs/109-prompt-adherence/notes/red-first-evidence.md`.
Every leg fails on a MISSING subject with an explicit assertion — never on an import error: the only
module this file imports is the declaration layer's own reader
(`scripts/python/declaration_reader.py`), which pre-exists this feature.

**Subjects.**

* the five facts under `shared/declarations/facts/prompt-adherence-*.yaml` — exactly five, `closed-set`,
  the declaration layer's required keys, membership equal to FR-018's set, no sixth fact for
  observation states (C-010, C-011, C-014);
* the owner document `shared/definitions/prompt-adherence-definitions.md` — its machine-parsed catalog
  table cells agree with the five sets in BOTH directions (C-012), and its two reason-taxonomy tables are
  the owner face of the pin (C-015);
* the engine `scripts/python/prompt-adherence.py` — the read points are locatable per slug (C-011), the
  engine carries the reason-taxonomy constants `ROW_REASON_CAUSES` / `INVALID_SOURCE_CAUSES` (C-015),
  and unknown declaration/owner tokens or an absent declaration layer exit 2 with no reading (C-013,
  C-026).

**Catalog shape (the owner document must carry it verbatim as one table).** The header row is exactly::

    | row_id | record_predicate | store | read_surface | identity_fields | timestamp_field | layer | strength | allowed_states | deviation_classes |

Row order equals the signals fact's declared order; `store` is a `runtime-store-layout` name or the
literal `registry` for the probe row (C-032); `deviation_classes` is `—` or a comma-separated list.

**Engine pin (the P2 implementation contract).** The engine carries, as module-level constant
sequences of string literals, `ROW_REASON_CAUSES = ("source-unavailable", "no-matching-records",
"invalid-source")` and `INVALID_SOURCE_CAUSES = ("unparsable", "schema-violation",
"unknown-schema-version", "invalid-timestamp")` — the tokens whose meanings this feature's owner
document owns (C-015). The pin compares tokens member-for-member in both directions.
"""
from __future__ import annotations

import ast
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
FACTS_DIR = REPO_ROOT / "shared" / "declarations" / "facts"
OWNER = REPO_ROOT / "shared" / "definitions" / "prompt-adherence-definitions.md"
ENGINE = REPO_ROOT / "scripts" / "python" / "prompt-adherence.py"
RUN_DETERMINATION = REPO_ROOT / "scripts" / "python" / "run-determination.py"

#: FR-018 — one fact per set; the signals order is the catalog declaration order.
EXPECTED_MEMBERS = {
    "prompt-adherence-layers": ["host-prompt", "project-rules"],
    "prompt-adherence-strengths": ["direct", "indirect"],
    "prompt-adherence-signals": [
        "run-determination-record",
        "exec-quant-record",
        "feedback-entry",
        "gate-observation-record",
        "evidence-finding",
        "probe-registry-declaration",
    ],
    "prompt-adherence-deviation-classes": ["axis-regression", "green-unproven", "evidence-missing"],
    "prompt-adherence-reading-status": ["complete", "partial", "no-data", "not-found"],
}

CATALOG_HEADER = [
    "row_id", "record_predicate", "store", "read_surface", "identity_fields",
    "timestamp_field", "layer", "strength", "allowed_states", "deviation_classes",
]
ROW_REASON_HEADER = ["cause", "meaning"]
INVALID_CAUSE_HEADER = ["invalid-source cause", "meaning"]

#: C-015 — the engine schema tokens the owner document gives meanings to.
ROW_REASON_CAUSES = ("source-unavailable", "no-matching-records", "invalid-source")
INVALID_SOURCE_CAUSES = (
    "unparsable", "schema-violation", "unknown-schema-version", "invalid-timestamp",
)
ENGINE_CONSUMER = "scripts/python/prompt-adherence.py"

_READER = None


def reader():
    """The declaration layer's one reader, loaded by path (it pre-exists this feature)."""
    global _READER
    if _READER is not None:
        return _READER
    path = REPO_ROOT / "scripts" / "python" / "declaration_reader.py"
    assert path.is_file(), "declaration reader absent: %s" % path
    spec = importlib.util.spec_from_file_location("_pa_declaration_reader", path)
    assert spec is not None and spec.loader is not None, "unable to load %s" % path
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _READER = module
    return module


def fact_files() -> list[Path]:
    return sorted(FACTS_DIR.glob("prompt-adherence-*.yaml"))


def fact_path(slug: str) -> Path:
    return FACTS_DIR / (slug + ".yaml")


def fact_body(slug: str) -> dict:
    path = fact_path(slug)
    assert path.is_file(), "declaration fact absent: %s" % path.relative_to(REPO_ROOT)
    try:
        fact = reader().load_fact(REPO_ROOT, slug)
    except reader().DeclarationError as error:
        pytest.fail("fact %r does not load: %s" % (slug, error))
    assert fact["stem"] == slug, "%s: `fact` key must equal the file stem" % path.name
    return fact["body"]


def statement(slug: str) -> list:
    body = fact_body(slug)
    value = body.get("statement")
    assert isinstance(value, list) and value, "%s: statement must be a non-empty sequence" % slug
    assert all(isinstance(item, str) and item for item in value), \
        "%s: every statement member must be a non-empty string" % slug
    return value


def owner_text() -> str:
    assert OWNER.is_file(), "owner document absent: %s" % OWNER.relative_to(REPO_ROOT)
    return OWNER.read_text(encoding="utf-8")


def engine_text() -> str:
    assert ENGINE.is_file(), "engine absent: %s" % ENGINE.relative_to(REPO_ROOT)
    return ENGINE.read_text(encoding="utf-8")


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def markdown_tables(text: str):
    """Every pipe table in the document as `(header_cells, [row_cells])`, in document order."""
    lines = text.splitlines()
    tables = []
    index = 0
    while index + 1 < len(lines):
        head, rule = lines[index].strip(), lines[index + 1].strip()
        if head.startswith("|") and rule.startswith("|") \
                and all(set(cell) <= set("-: ") and "-" in cell for cell in split_row(rule)):
            rows = []
            probe = index + 2
            while probe < len(lines) and lines[probe].strip().startswith("|"):
                rows.append(split_row(lines[probe]))
                probe += 1
            tables.append((split_row(head), rows))
            index = probe
            continue
        index += 1
    return tables


def table_with_header(text: str, header: list[str]):
    matches = [table for table in markdown_tables(text) if table[0] == header]
    assert len(matches) == 1, (
        "expected exactly one table with header %r, found %d" % (header, len(matches)))
    return matches[0]


def catalog_rows() -> list[dict]:
    _header, rows = table_with_header(owner_text(), CATALOG_HEADER)
    return [dict(zip(CATALOG_HEADER, row)) for row in rows]


def store_names() -> set[str]:
    body = reader().load_fact(REPO_ROOT, "runtime-store-layout")["body"]
    stores = body["statement"]["stores"]
    assert isinstance(stores, dict) and stores, "runtime-store-layout statement.stores must be a mapping"
    return {str(name) for name in stores}


def constant_sequence(tree: ast.AST, name: str):
    """The single module-wide constant sequence assigned to ``name``, or None."""
    found = []
    for node in ast.walk(tree):
        target = value = None
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name):
            target, value = node.targets[0].id, node.value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            target, value = node.target.id, node.value
        if target != name or not isinstance(value, (ast.Tuple, ast.List)):
            continue
        items = [item.value for item in value.elts
                 if isinstance(item, ast.Constant) and isinstance(item.value, str)]
        if len(items) == len(value.elts):
            found.append(items)
    assert len(found) <= 1, "engine defines %s more than once" % name
    return found[0] if found else None


# --------------------------------------------------------------------------- #
# C-010 / C-011 — five facts, required keys, one kind, exact membership
# --------------------------------------------------------------------------- #
def test_exactly_five_facts_with_required_keys_and_closed_set_kind():
    expected_files = sorted(path.name for path in map(fact_path, EXPECTED_MEMBERS))
    assert [path.name for path in fact_files()] == expected_files, (
        "exactly the five prompt-adherence facts must exist; found %s"
        % [path.name for path in fact_files()])

    contract = reader().load_contract(REPO_ROOT)
    required_keys = contract["required_fact_keys"]
    kinds = contract["fact_kinds"]
    for slug in EXPECTED_MEMBERS:
        body = fact_body(slug)
        missing = [key for key in required_keys if key not in body]
        assert not missing, "%s: missing required key(s) %s" % (slug, missing)
        assert set(body) <= set(required_keys) | {"note"}, \
            "%s: unknown top-level key(s) %s" % (
                slug, sorted(set(body) - set(required_keys) - {"note"}))
        assert body.get("kind") == "closed-set", "%s: kind must be closed-set" % slug
        assert body.get("kind") in kinds, "%s: kind outside the declaration contract" % slug
        consumers = body.get("consumers")
        assert isinstance(consumers, list) and ENGINE_CONSUMER in consumers, \
            "%s: consumers must name %s" % (slug, ENGINE_CONSUMER)
        assert isinstance(body.get("former_carriers"), list), \
            "%s: former_carriers must be a sequence" % slug


def test_membership_equality_per_fr018():
    for slug, expected in EXPECTED_MEMBERS.items():
        declared = statement(slug)
        assert declared == expected, (
            "%s statement drifted from FR-018: declared=%r expected=%r"
            % (slug, declared, expected))
        assert len(set(declared)) == len(declared), "%s: duplicate member" % slug


# --------------------------------------------------------------------------- #
# C-014 — observation states get no sixth fact
# --------------------------------------------------------------------------- #
def test_no_sixth_fact_for_observation_states():
    seven = statement("evidence-seven-states")
    assert len(seven) == 7, "the composed state domain must be the seven-state fact"
    assert "Unobserved" in seven, "the seven-state fact lost `Unobserved`"
    source = RUN_DETERMINATION.read_text(encoding="utf-8")
    assert "not_evaluated" in source, \
        "run-determination.py no longer carries the `not_evaluated` literal"
    assert not fact_path("prompt-adherence-observation-states").exists(), \
        "observation states MUST NOT become a sixth prompt-adherence fact"


# --------------------------------------------------------------------------- #
# C-012 — owner catalog cells agree with the five sets in both directions
# --------------------------------------------------------------------------- #
def test_owner_catalog_agrees_with_declaration_sets_both_directions():
    rows = catalog_rows()
    signals = statement("prompt-adherence-signals")
    assert len(rows) == len(signals), \
        "catalog must carry exactly the six signal rows, found %d" % len(rows)
    assert [row["row_id"] for row in rows] == signals, \
        "catalog row order must equal the signals fact's declared order"

    layers = statement("prompt-adherence-layers")
    strengths = statement("prompt-adherence-strengths")
    classes = statement("prompt-adherence-deviation-classes")
    states = statement("evidence-seven-states")
    stores = store_names()

    layer_cells = [row["layer"] for row in rows]
    strength_cells = [row["strength"] for row in rows]
    assert set(layer_cells) <= set(layers), \
        "catalog names a layer outside the layers fact: %s" % sorted(set(layer_cells) - set(layers))
    assert set(layers) <= set(layer_cells), \
        "a layers-fact member is never used by the catalog: %s" % sorted(set(layers) - set(layer_cells))
    assert set(strength_cells) <= set(strengths), \
        "catalog names a strength outside the strengths fact: %s" % (
            sorted(set(strength_cells) - set(strengths)))
    assert set(strengths) <= set(strength_cells), \
        "a strengths-fact member is never used by the catalog: %s" % (
            sorted(set(strengths) - set(strength_cells)))

    used_classes = set()
    for row in rows:
        cell = row["deviation_classes"]
        tokens = [] if cell in ("—", "-", "") else [part.strip() for part in cell.split(",")]
        assert set(tokens) <= set(classes), (
            "%s: deviation classes %s outside the classes fact" % (row["row_id"], tokens))
        assert row["allowed_states"] in states, (
            "%s: allowed state %r outside the composed state domain"
            % (row["row_id"], row["allowed_states"]))
        if row["row_id"] == "probe-registry-declaration":
            assert row["store"] == "registry", "the probe row reads the registry, not a store"
            assert row["identity_fields"] in ("—", "-"), "the probe row is run-identity-exempt"
            assert row["timestamp_field"] in ("—", "-"), "the probe row is window-exempt"
            assert row["allowed_states"] == "Wired", "the probe row's positive cap is Wired"
        else:
            assert row["store"] in stores, (
                "%s: store %r is not declared by runtime-store-layout" % (row["row_id"], row["store"]))
            assert row["identity_fields"] not in ("", "—", "-"), \
                "%s: identity fields must be declared" % row["row_id"]
            assert row["timestamp_field"] not in ("", "—", "-"), \
                "%s: timestamp field must be declared" % row["row_id"]
            assert row["allowed_states"] == "Exercised", \
                "%s: positive cap must be Exercised" % row["row_id"]
        for column in ("record_predicate", "read_surface"):
            assert row[column], "%s: empty %s cell" % (row["row_id"], column)
        used_classes |= set(tokens)
    assert used_classes == set(classes), (
        "every deviation class must be declared by some row; missing %s"
        % sorted(set(classes) - used_classes))


# --------------------------------------------------------------------------- #
# C-015 — the owner↔engine reason-taxonomy pin
# --------------------------------------------------------------------------- #
def test_owner_and_engine_reason_taxonomy_pin():
    text = owner_text()
    reason_rows = table_with_header(text, ROW_REASON_HEADER)[1]
    assert [row[0] for row in reason_rows] == list(ROW_REASON_CAUSES), (
        "owner row-reason table must carry exactly %s, found %s"
        % (list(ROW_REASON_CAUSES), [row[0] for row in reason_rows]))
    assert all(len(row) >= 2 and row[1] for row in reason_rows), \
        "every row-reason cause needs its meaning in the owner document"

    invalid_rows = table_with_header(text, INVALID_CAUSE_HEADER)[1]
    assert [row[0] for row in invalid_rows] == list(INVALID_SOURCE_CAUSES), (
        "owner invalid-source table must carry exactly %s, found %s"
        % (list(INVALID_SOURCE_CAUSES), [row[0] for row in invalid_rows]))
    assert all(len(row) >= 2 and row[1] for row in invalid_rows), \
        "every invalid-source cause needs its meaning in the owner document"

    tree = ast.parse(engine_text())
    engine_reasons = constant_sequence(tree, "ROW_REASON_CAUSES")
    assert engine_reasons is not None, "engine does not carry ROW_REASON_CAUSES"
    assert set(engine_reasons) == set(ROW_REASON_CAUSES) and \
        len(engine_reasons) == len(ROW_REASON_CAUSES), (
            "engine ROW_REASON_CAUSES disagrees with the owner document: %r" % engine_reasons)
    engine_invalid = constant_sequence(tree, "INVALID_SOURCE_CAUSES")
    assert engine_invalid is not None, "engine does not carry INVALID_SOURCE_CAUSES"
    assert set(engine_invalid) == set(INVALID_SOURCE_CAUSES) and \
        len(engine_invalid) == len(INVALID_SOURCE_CAUSES), (
            "engine INVALID_SOURCE_CAUSES disagrees with the owner document: %r" % engine_invalid)


# --------------------------------------------------------------------------- #
# C-011 — the engine's declaration read points are locatable per slug
# --------------------------------------------------------------------------- #
def test_engine_declaration_read_points_locatable():
    text = engine_text()
    assert "declaration_reader" in text, \
        "engine source must reference the declaration layer's reader"
    for slug in EXPECTED_MEMBERS:
        assert slug in text, "engine source has no read point for %r" % slug


# --------------------------------------------------------------------------- #
# C-013 / C-026 — unknown tokens and a degraded layer exit 2 with no reading
# --------------------------------------------------------------------------- #
def _scratch_tree(tmp_path: Path, *, doctor_signals=False, doctor_owner=False,
                  omit_shared=False) -> Path:
    tree = tmp_path / "scratch"
    shutil.copytree(REPO_ROOT / "scripts" / "python", tree / "scripts" / "python",
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    (tree / ".specify").mkdir()
    if omit_shared:
        return tree
    shutil.copytree(REPO_ROOT / "shared", tree / "shared")
    if doctor_signals:
        path = tree / "shared" / "declarations" / "facts" / "prompt-adherence-signals.yaml"
        assert path.is_file(), "cannot doctor an absent signals fact"
        text = path.read_text(encoding="utf-8")
        assert "\nconsumers:" in text, "signals fact shape changed; update the doctor"
        path.write_text(
            text.replace("\nconsumers:", "\n  - unknown-signal-row\nconsumers:", 1),
            encoding="utf-8")
    if doctor_owner:
        path = tree / "shared" / "definitions" / "prompt-adherence-definitions.md"
        assert path.is_file(), "cannot doctor an absent owner document"
        lines = path.read_text(encoding="utf-8").splitlines()
        hits = [i for i, line in enumerate(lines) if line.startswith("| run-determination-record ")]
        assert len(hits) == 1, "owner catalog shape changed; update the doctor"
        lines[hits[0]] = lines[hits[0]].replace("| host-prompt |", "| host-layer |", 1)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return tree


def _run_scratch_engine(tree: Path) -> subprocess.CompletedProcess:
    engine = tree / "scripts" / "python" / "prompt-adherence.py"
    assert engine.is_file(), "engine absent: %s" % ENGINE.relative_to(REPO_ROOT)
    return subprocess.run(
        [sys.executable, str(engine), "--workspace-root", str(tree)],
        capture_output=True, text=True, cwd=str(tree))


def test_unknown_declaration_token_is_exit_2_with_no_reading(tmp_path):
    proc = _run_scratch_engine(_scratch_tree(tmp_path, doctor_signals=True))
    assert proc.returncode == 2, (
        "an unknown token in a declaration set must exit 2 (got %d); stderr=%r"
        % (proc.returncode, proc.stderr[-400:]))
    assert proc.stdout.strip() == "", "no reading may be emitted after an unknown token"
    assert proc.stderr.strip(), "a recognizable message must land on stderr"


def test_unknown_owner_catalog_token_is_exit_2_with_no_reading(tmp_path):
    proc = _run_scratch_engine(_scratch_tree(tmp_path, doctor_owner=True))
    assert proc.returncode == 2, (
        "an unknown token in the owner catalog must exit 2 (got %d); stderr=%r"
        % (proc.returncode, proc.stderr[-400:]))
    assert proc.stdout.strip() == "", "no reading may be emitted after an unknown token"


def test_absent_declaration_layer_degrades_with_exit_2(tmp_path):
    proc = _run_scratch_engine(_scratch_tree(tmp_path, omit_shared=True))
    assert proc.returncode == 2, (
        "an unusable declaration layer must exit 2 (got %d)" % proc.returncode)
    assert proc.stdout.strip() == "", "no reading may be emitted from a degraded layer"
    assert proc.stderr.strip(), "the degradation must name a documented reason"