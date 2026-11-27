"""Contract guard — the prompt-adherence owner document (C-001…C-007, C-033 framework-map leg).

Red-first (T017): authored before T018 adds the premise chain's assumed behaviors and the
machine-parsed coverage map. The coverage-map legs fail on the missing section with a named
red-first message; every other leg reads the delivered owner document, the five declaration
facts (through ``declaration_reader``) and ``shared/definitions/framework-map.md`` directly —
this module imports nothing from the mechanism and never fails on an import error.

Legs and their clauses:

- C-001 / FR-001 — the owner document exists and self-declares its single ownership of the six
  owned faces (premise chain and coverage map, two-layer model, signal catalog, reading
  contract, blind-spot register, red lines), with the meaning/value-domain/schema split.
- C-002 / FR-002 — the bilingual layer tokens ``host-prompt`` / 宿主提示层 and
  ``project-rules`` / 项目规则文件层, and the two by-reference reaches (the host-versus-project
  disambiguation and the instructions-surface owner).
- C-004 / C-005 / FR-004 / FR-028 — the catalog table's cells resolve against the five
  declaration sets and the runtime store layout; the admission criteria carry all five
  conditions and the no-new-capture-point boundary.
- C-006 / FR-029 — the blind-spot register carries exactly the six classes, each with a reason
  and a capture direction, and states the two named boundaries.
- C-003 / FR-003 / SC-004 — the coverage map: twelve assumed behaviors, dense in document
  order, each naming exactly one target kind and one target; sensor targets resolve to catalog
  row ids, blind-spot targets resolve to register ids, every catalog row is cited and every
  register id is cited.
- C-001 / C-033 — the two framework-map rows (owner document, reading entry) exist and name
  their installed paths.
- C-007 — the red lines are stated once, with the feedback red lines reached by path.
"""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
OWNER_DOC = REPO_ROOT / "shared" / "definitions" / "prompt-adherence-definitions.md"
FRAMEWORK_MAP = REPO_ROOT / "shared" / "definitions" / "framework-map.md"
READER = REPO_ROOT / "scripts" / "python" / "declaration_reader.py"

FACT_SLUGS = (
    "prompt-adherence-layers",
    "prompt-adherence-strengths",
    "prompt-adherence-signals",
    "prompt-adherence-deviation-classes",
    "prompt-adherence-reading-status",
)

EXPECTED_ROWS = (
    "run-determination-record",
    "exec-quant-record",
    "feedback-entry",
    "gate-observation-record",
    "evidence-finding",
    "probe-registry-declaration",
)

EXPECTED_BLIND_SPOTS = (
    "host-prompt-content",
    "host-rule-surfacing",
    "in-turn-rule-behavior",
    "anomaly-line-persistence",
    "gate-breach-and-silent-skip",
    "instruction-drift-between-reconciles",
)

#: The owning read surface each catalog row's ``read_surface`` cell must name (C-032).
READ_SURFACES = {
    "run-determination-record": "run-determination.py::load_determinations",
    "exec-quant-record": "exec-quant.py::load_records",
    "feedback-entry": "feedback-utils.py::scan_entries",
    "gate-observation-record": "feedback-utils.py::scan_entries",
    "evidence-finding": "evidence-utils.py::load_index",
    "probe-registry-declaration": "probe-utils.py::load_probe_registry",
}

EXPECTED_ASSUMED_BEHAVIORS = tuple("AB-%02d" % index for index in range(1, 13))
TARGET_KINDS = ("sensor", "blind-spot")

CATALOG_HEADER = (
    "row_id", "record_predicate", "store", "read_surface", "identity_fields",
    "timestamp_field", "layer", "strength", "allowed_states", "deviation_classes",
)
REGISTER_HEADER = ("blind_spot", "reason", "capture_direction")
COVERAGE_HEADER = ("Assumed behavior", "Statement", "Target kind", "Target")

EMPTY_CELLS = {"", "—", "-", "–", "none", "n/a"}


# --------------------------------------------------------------------------- #
# subject loaders (named failures, never import errors)
# --------------------------------------------------------------------------- #
def _owner_text():
    assert OWNER_DOC.is_file(), (
        "red-first: shared/definitions/prompt-adherence-definitions.md is absent "
        "(authored by T006/T007)"
    )
    return OWNER_DOC.read_text(encoding="utf-8")


def _reader_module():
    assert READER.is_file(), "declaration reader absent: %s" % READER
    spec = importlib.util.spec_from_file_location("pa_owner_guard_reader", READER)
    assert spec is not None and spec.loader is not None, "unable to load %s" % READER
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _fact_body(slug):
    try:
        return _reader_module().load_fact(str(REPO_ROOT), slug)["body"]
    except Exception as exc:  # DeclarationError / OSError
        pytest.fail(
            "red-first: shared/declarations/facts/%s.yaml is not readable through "
            "declaration_reader (%s)" % (slug, exc)
        )


def _fact_members(slug):
    return [str(member) for member in _fact_body(slug).get("statement") or []]


def _store_names():
    statement = _fact_body("runtime-store-layout").get("statement")
    assert isinstance(statement, dict) and statement.get("stores"), (
        "runtime-store-layout carries no stores mapping"
    )
    return {str(name) for name in statement["stores"]}


# --------------------------------------------------------------------------- #
# Markdown table helpers (the machine-parsed owner-document registry, PA4)
# --------------------------------------------------------------------------- #
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
_SEPARATOR_RE = re.compile(r"^:?-{2,}:?$")


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


def _section_fragment(text, fragment):
    return _section(text, lambda label: fragment.lower() in label.lower())


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


def _split_tokens(cell):
    token = _token(cell)
    if token.lower() in EMPTY_CELLS:
        return []
    return [_token(part) for part in token.split(",") if _token(part)]


def _column_exact(header, name):
    for index, label in enumerate(header):
        if label.strip().lower() == name.lower():
            return index
    pytest.fail("table lacks the exact '%s' column (header: %r)" % (name, header))


def _table_with_header(text, section_fragment, header, where):
    chunk = _section_fragment(text, section_fragment)
    assert chunk is not None, "owner document has no %r section (%s)" % (
        section_fragment, where)
    expected = [cell.lower() for cell in header]
    for found_header, rows in _tables(chunk):
        if [cell.strip().lower() for cell in found_header] == expected:
            return found_header, rows
    pytest.fail(
        "the %r section carries no table with header %r (%s)" % (
            section_fragment, list(header), where)
    )


def _catalog_table(text):
    return _table_with_header(text, "Signal Catalog", CATALOG_HEADER, "C-005")


def _register_table(text):
    return _table_with_header(text, "Blind-Spot Register", REGISTER_HEADER, "C-006")


def _coverage_table(text):
    chunk = _section_fragment(text, "Coverage Map")
    assert chunk is not None, (
        "red-first: the owner document carries no assumed-behavior coverage-map section "
        "(authored by T018 — twelve AB-NN rows mapping each assumed behavior to exactly one "
        "catalog row or exactly one blind-spot id; FR-003)"
    )
    expected = [cell.lower() for cell in COVERAGE_HEADER]
    for header, rows in _tables(chunk):
        if [cell.strip().lower() for cell in header] == expected:
            return header, rows
    pytest.fail(
        "the coverage-map section carries no assumed-behavior table with header %r (C-003)"
        % (list(COVERAGE_HEADER),)
    )


def _coverage_entries(text):
    header, rows = _coverage_table(text)
    id_column = _column_exact(header, "Assumed behavior")
    statement_column = _column_exact(header, "Statement")
    kind_column = _column_exact(header, "Target kind")
    target_column = _column_exact(header, "Target")
    entries = []
    for row in rows:
        entry_id = _token(row[id_column])
        if not entry_id:
            continue
        entries.append({
            "id": entry_id,
            "statement": row[statement_column].strip(),
            "kinds": _split_tokens(row[kind_column]),
            "targets": _split_tokens(row[target_column]),
        })
    return entries


# --------------------------------------------------------------------------- #
# C-001 / FR-001 — one owner, self-declared
# --------------------------------------------------------------------------- #
def test_owner_document_declares_its_single_ownership():
    text = _owner_text()
    declaration = _section_fragment(text, "Owner Declaration")
    assert declaration is not None, (
        "the owner document carries no 'Owner Declaration' section (C-001/FR-001)"
    )
    assert "本文件自声明拥有" in declaration, (
        "the owner declaration does not declare the document's own ownership (C-001)"
    )
    for owned in (
        "前提链与假定行为覆盖图",
        "双层模型",
        "信号目录",
        "读取契约的字段含义",
        "盲区登记",
        "本特性红线",
    ):
        assert owned in declaration, (
            "the owner declaration does not name %r among the faces it owns (FR-001)" % owned
        )
    assert "MUST NOT 复述" in text, (
        "the owner document does not close the second-location door (pointer-only consumers, "
        "FR-001/FR-019)"
    )
    assert "唯一 owner" in text and "shared/declarations/facts/prompt-adherence-*.yaml" in text, (
        "the owner document does not declare the single-owner split (meaning here, value "
        "domains in the five facts; FR-019)"
    )
    assert "scripts/python/prompt-adherence.py" in text, (
        "the owner document does not reach the engine by path (the schema-and-behavior face, "
        "FR-019)"
    )


# --------------------------------------------------------------------------- #
# C-002 / FR-002 — the bilingual layer tokens and their references
# --------------------------------------------------------------------------- #
def test_layer_tokens_are_bilingual_and_reference_their_owners():
    text = _owner_text()
    layers = _section_fragment(text, "Two-Layer Model")
    assert layers is not None, "owner document has no 'Two-Layer Model' section (C-002/FR-002)"
    flattened = " ".join(layers.split())

    host = flattened.find("宿主提示层(Host Prompt Layer")
    project = flattened.find("项目规则文件层(Project Rule File Layer")
    assert host >= 0, "the host layer line loses its bilingual form 宿主提示层(Host Prompt Layer) (C-002)"
    assert project >= 0, (
        "the project layer line loses its bilingual form 项目规则文件层(Project Rule File Layer) "
        "(C-002)"
    )
    assert "`host-prompt`" in flattened, (
        "the host layer line does not tie the bilingual form to the 'host-prompt' token (C-002)"
    )
    assert "`project-rules`" in flattened, (
        "the project layer line does not tie the bilingual form to the 'project-rules' token "
        "(C-002)"
    )
    assert "better-harness.md" in layers, (
        "the two-layer section does not reach the host-versus-project disambiguation by "
        "reference (shared/guidelines/better-harness.md)"
    )
    assert "symlink-model.md" in layers, (
        "the two-layer section does not reach the instructions-surface owner by reference "
        "(.specify/shared/workflow/symlink-model.md)"
    )


# --------------------------------------------------------------------------- #
# C-004 / C-005 / FR-004 / FR-028 — catalog cells and admission criteria
# --------------------------------------------------------------------------- #
def test_catalog_rows_resolve_against_the_declaration_sets_and_store_layout():
    text = _owner_text()
    header, rows = _catalog_table(text)
    row_column = _column_exact(header, "row_id")
    store_column = _column_exact(header, "store")
    surface_column = _column_exact(header, "read_surface")
    layer_column = _column_exact(header, "layer")
    strength_column = _column_exact(header, "strength")
    states_column = _column_exact(header, "allowed_states")
    class_column = _column_exact(header, "deviation_classes")
    predicate_column = _column_exact(header, "record_predicate")

    row_ids = [_token(row[row_column]) for row in rows]
    assert row_ids == list(EXPECTED_ROWS), (
        "the catalog rows are %r, expected exactly the six of FR-028 in order" % row_ids
    )

    layers = set(_fact_members("prompt-adherence-layers"))
    strengths = set(_fact_members("prompt-adherence-strengths"))
    classes = set(_fact_members("prompt-adherence-deviation-classes"))
    states = set(_fact_members("evidence-seven-states")) | {"not_evaluated"}
    stores = _store_names()

    used_classes = set()
    for row in rows:
        row_id = _token(row[row_column])
        assert row[predicate_column].strip(), (
            "catalog row %r carries no record predicate (FR-028)" % row_id
        )
        assert _token(row[layer_column]) in layers, (
            "catalog row %r carries an undeclared layer token %r" % (row_id, row[layer_column])
        )
        assert _token(row[strength_column]) in strengths, (
            "catalog row %r carries an undeclared strength token %r"
            % (row_id, row[strength_column])
        )
        for state in _split_tokens(row[states_column]):
            assert state in states, (
                "catalog row %r carries an allowed state %r outside the composed state domain"
                % (row_id, state)
            )
        used_classes.update(_split_tokens(row[class_column]))
        assert READ_SURFACES[row_id] in row[surface_column], (
            "catalog row %r does not name its owning read surface %r (C-032)"
            % (row_id, READ_SURFACES[row_id])
        )
        store = _token(row[store_column])
        if row_id == "probe-registry-declaration":
            assert store == "registry", (
                "the probe row reads the registry, not a declared store (FR-030)"
            )
        else:
            assert store in stores, (
                "catalog row %r names store %r, which the runtime store layout does not "
                "declare (FR-030)" % (row_id, store)
            )
    assert used_classes <= classes, (
        "catalog deviation-class cells outside the classes fact: %r"
        % sorted(used_classes - classes)
    )
    assert used_classes == classes, (
        "not every declared deviation class is exercised by a catalog row: %r"
        % sorted(classes - used_classes)
    )


def test_admission_criteria_carry_all_five_conditions():
    text = _owner_text()
    chunk = _section_fragment(text, "Admission Criteria")
    assert chunk is not None, (
        "the owner document carries no 'Admission Criteria' section (C-004/FR-004)"
    )
    for label in ("(a)", "(b)", "(c)", "(d)", "(e)"):
        assert label in chunk, (
            "the admission criteria lack condition %s (C-004 requires all five)" % label
        )
    assert "MUST NOT 通过新采集点合成" in chunk, (
        "the admission criteria do not carry the no-new-capture-point boundary (FR-004)"
    )


# --------------------------------------------------------------------------- #
# C-006 / FR-029 — the blind-spot register
# --------------------------------------------------------------------------- #
def test_blind_spot_register_carries_the_six_classes_with_reason_and_direction():
    text = _owner_text()
    header, rows = _register_table(text)
    class_column = _column_exact(header, "blind_spot")
    reason_column = _column_exact(header, "reason")
    direction_column = _column_exact(header, "capture_direction")
    ids = [_token(row[class_column]) for row in rows]
    assert ids == list(EXPECTED_BLIND_SPOTS), (
        "the blind-spot register classes are %r, expected exactly the six of FR-029" % ids
    )
    for row in rows:
        class_id = _token(row[class_column])
        assert row[reason_column].strip(), (
            "blind-spot %r carries no reason why no persisted sensor observes it (C-006)"
            % class_id
        )
        assert row[direction_column].strip(), (
            "blind-spot %r carries no capture direction an owner-sanctioned change would take "
            "(C-006)" % class_id
        )
    by_id = {_token(row[class_column]): " | ".join(row) for row in rows}
    assert "隐私红线" in by_id["host-prompt-content"], (
        "the host-prompt-content entry does not state its privacy red line (C-006)"
    )
    anomaly = by_id["anomaly-line-persistence"]
    assert "MUST NOT 在此重新引入" in anomaly and "shared/guidelines/fast-fail.md" in anomaly, (
        "the anomaly-line-persistence entry does not state the dropped-producer boundary and "
        "its owner path (C-006)"
    )
    assert "缺席 MUST NOT 读成违规" in by_id["gate-breach-and-silent-skip"], (
        "the gate-breach-and-silent-skip entry does not state the absence-is-not-breach rule "
        "(FR-012)"
    )


# --------------------------------------------------------------------------- #
# C-003 / FR-003 / SC-004 — the coverage map, machine-checked in both directions
# --------------------------------------------------------------------------- #
def test_coverage_map_names_twelve_dense_assumed_behaviors():
    entries = _coverage_entries(_owner_text())
    ids = [entry["id"] for entry in entries]
    assert ids == list(EXPECTED_ASSUMED_BEHAVIORS), (
        "the coverage map's assumed behaviors are %r; expected twelve ids dense in document "
        "order (%r) — FR-003 / data-model E-3" % (ids, list(EXPECTED_ASSUMED_BEHAVIORS))
    )
    for entry in entries:
        assert entry["statement"], (
            "assumed behavior %r carries no statement sentence (data-model E-3)" % entry["id"]
        )


def test_every_assumed_behavior_names_exactly_one_target_kind_and_one_target():
    for entry in _coverage_entries(_owner_text()):
        assert len(entry["kinds"]) == 1, (
            "assumed behavior %r names %r target kinds; exactly one is allowed (C-003)"
            % (entry["id"], entry["kinds"])
        )
        assert entry["kinds"][0] in TARGET_KINDS, (
            "assumed behavior %r declares target kind %r; expected one of %r"
            % (entry["id"], entry["kinds"][0], list(TARGET_KINDS))
        )
        assert len(entry["targets"]) == 1, (
            "assumed behavior %r names %r targets; exactly one is allowed (C-003)"
            % (entry["id"], entry["targets"])
        )


def test_coverage_map_resolves_targets_and_cites_every_row_and_register_entry():
    text = _owner_text()
    entries = _coverage_entries(text)
    header, catalog_rows = _catalog_table(text)
    row_ids = {_token(row[_column_exact(header, "row_id")]) for row in catalog_rows}
    register_header, register_rows = _register_table(text)
    spot_ids = {
        _token(row[_column_exact(register_header, "blind_spot")]) for row in register_rows
    }

    cited_rows, cited_spots = set(), set()
    for entry in entries:
        if len(entry["kinds"]) != 1 or len(entry["targets"]) != 1:
            continue
        kind, target = entry["kinds"][0], entry["targets"][0]
        if kind == "sensor":
            assert target in row_ids, (
                "assumed behavior %r maps to sensor target %r, which is not a catalog row id "
                "(C-003)" % (entry["id"], target)
            )
            cited_rows.add(target)
        elif kind == "blind-spot":
            assert target in spot_ids, (
                "assumed behavior %r maps to blind-spot target %r, which is not a register id "
                "(C-003)" % (entry["id"], target)
            )
            cited_spots.add(target)

    assert row_ids <= cited_rows, (
        "catalog rows cited by no assumed behavior: %r (FR-003 two-way check)"
        % sorted(row_ids - cited_rows)
    )
    assert spot_ids <= cited_spots, (
        "blind spots cited by no assumed behavior: %r (C-003 register coverage)"
        % sorted(spot_ids - cited_spots)
    )
    assert cited_rows == row_ids and cited_spots == spot_ids, (
        "the coverage map cites a target outside the catalog or register: rows=%r spots=%r"
        % (sorted(cited_rows - row_ids), sorted(cited_spots - spot_ids))
    )


# --------------------------------------------------------------------------- #
# C-001 / C-033 — the framework-map rows
# --------------------------------------------------------------------------- #
def test_framework_map_registers_the_owner_document_and_the_reading_entry():
    assert FRAMEWORK_MAP.is_file(), "shared/definitions/framework-map.md is absent"
    text = FRAMEWORK_MAP.read_text(encoding="utf-8")
    assert ".specify/shared/definitions/prompt-adherence-definitions.md" in text, (
        "the framework map carries no row for the owner document's installed path (C-033)"
    )
    assert ".specify/scripts/python/prompt-adherence.py" in text, (
        "the framework map carries no row for the reading entry's installed path (C-033)"
    )
    rows = [
        line for line in text.splitlines()
        if "prompt-adherence" in line and line.strip().startswith("|")
    ]
    assert len(rows) >= 2, (
        "the framework map carries %d prompt-adherence row(s); expected the owner-document row "
        "and the reading-entry row" % len(rows)
    )
    for line in rows:
        assert "prompt-adherence-definitions.md" in line or "prompt-adherence.py" in line, (
            "a prompt-adherence framework-map row names neither mechanism path: %r" % line
        )


# --------------------------------------------------------------------------- #
# C-007 — the red lines, stated once
# --------------------------------------------------------------------------- #
def test_red_lines_are_stated_and_the_feedback_lines_are_reached_by_path():
    text = _owner_text()
    chunk = _section_fragment(text, "Red Lines")
    assert chunk is not None, "owner document has no 'Red Lines' section (C-007)"
    lowered = " ".join(chunk.lower().split())
    for phrase in (
        "复合遵从分",
        "成熟度指数",
        "排名",
        "跨项目比较",
        "不新增 store、采集点或记录 schema 变更",
        "不读取原始宿主系统提示或原始用户对话文本",
        "不访问网络、不执行自动传输",
        "绝不包装成关于宿主产品的反馈",
    ):
        assert phrase.lower() in lowered, (
            "the Red Lines section does not state %r (C-007/FR-025/FR-027)" % phrase
        )
    assert "shared/workflow/feedback-step.md" in chunk, (
        "the Red Lines section does not reach the feedback red lines by their owner path "
        "(shared/workflow/feedback-step.md, C-007)"
    )
    assert "MUST NOT 复述" in chunk, (
        "the Red Lines section does not declare that the feedback red lines are referenced, "
        "not restated (C-007)"
    )