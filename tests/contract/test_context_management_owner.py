"""Contract guard: the context-management owner document (Feature 110, C-001…C-007, C-020…C-029).

The owner document `shared/definitions/context-management-definitions.md` is the single
home of the model, the layout table, the triggers and the presence vocabulary. This file
pins the shapes the audit engine and every other surface read, and it pins the
protocol-boundary against the pre-change baseline captured at implement entry.

Machine conventions pinned here (the owner document MUST carry them; the audit engine
parses the same shapes):

* first pipe table under ``## Forms`` — header ``form | legal layers``;
* first pipe table under ``## Layout`` — header ``class id | layer | form | source |
  owner | cap reference``;
* marker lines inside their sections — ``owns:``, ``baseline_composition:``,
  ``baseline_refresh_triggers:``, ``task_composition_triggers:``, ``baseline_scope:``,
  ``role_fields:``, ``injections:``, ``red_lines:``, and the concept-pointer
  ``glossary:`` / ``definitions:`` / ``explanations:`` triple.

Authored red-first (C-040): every leg below reads a subject that does not exist yet at
this point of the run, so the whole module is expected to fail before the implementation
rows land.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from fixtures.context_management_support import (
    BOUNDARY_COLUMNS,
    CONCEPT_STRUCTURE_COLUMNS,
    FORM_MATRIX,
    FORMS_COLUMNS,
    LANDING_COLUMNS,
    LAYOUT_COLUMNS,
    LIVE_INSTRUCTIONS,
    PRE_CHANGE_NOTES,
    PRESENCE_COLUMNS,
    REPO_ROOT,
    TEMPLATE,
    TRIGGER_COLUMNS,
    marker_list,
    owner_text,
    section_body,
    split_layers,
    table_rows,
)

pytestmark = pytest.mark.contract

OWNER_DOC = REPO_ROOT / "shared" / "definitions" / "context-management-definitions.md"
DEFINITIONS_DIR = REPO_ROOT / "shared" / "definitions"
PROTOCOL_OWNER = REPO_ROOT / "shared" / "definitions" / "superagent-definitions.md"

AMBIENT_HEADING = "## Context Management(上下文管理)"
AMBIENT_OWNER_POINTER = ".specify/shared/definitions/context-management-definitions.md"
AMBIENT_AUDIT_ENTRY = ".specify/scripts/python/context-audit.py"

STR_LITERALS = (
    "Context Management(上下文管理)",
    "Invariant(不变)",
    "Variable(可变)",
    "System(系统级)",
    "Project(项目级)",
    "Task(任务级)",
)

OWNED_SURFACES = {
    "umbrella-term",
    "categories",
    "layers",
    "forms",
    "landing-contract",
    "layout-table",
    "composition-protocol",
    "trigger-set",
    "composer-roles",
    "concept-pointer-slot",
    "presence-vocabulary",
    "red-lines",
}

TRIGGER_ROWS = {
    "session-entry": ("root session", ("baseline",), ("manifest",)),
    "task-entry": ("composer of the current work", ("task",), ("manifest",)),
    "task-switch": ("composer of the current work", ("task",), ("manifest",)),
    "pre-dispatch": ("superagent", ("task",), ("dispatch brief",)),
    "stage-boundary": ("composer of the current work", ("task-delta",), ("manifest",)),
    "source-drift": ("root session", ("baseline",), ("source reading", "manifest")),
    "reentry": (
        "resumed session",
        ("baseline", "task-delta"),
        ("re-anchoring statement",),
    ),
}

FORBIDDEN_CELLS = ("invariant × task", "variable × system", "variable × project")
LEGAL_CELLS = ("invariant × system", "invariant × project", "variable × task")

CONCEPT_STRUCTURE_LABELS = (
    "root/superagent turn",
    "subagent dispatch payload",
    "memory-recall projection",
    "recovery/re-anchoring re-entry surface",
)

PRESENCE_TOKENS = ("present", "absent", "unreachable", "empty", "not-evaluated")

# FR-004's eighteen-class seed. A literal pinned in a guard is a sanctioned duplicate;
# membership stays owned by `context-classes.yaml`.
SEED_CLASS_IDS = (
    "runtime-environment",
    "available-commands",
    "operation-permissions",
    "reality-constraints",
    "governance-baseline",
    "project-vocabulary",
    "concept-definitions",
    "concept-explanations",
    "capability-inventories",
    "project-state-anchors",
    "workspace-map",
    "task-artifacts",
    "task-capabilities",
    "task-shared-docs",
    "task-docs",
    "task-memory",
    "task-statement",
    "task-delta",
)

CAP_UNIT_RE = re.compile(r"\b\d+\s*(?:tokens?|bytes?|chars?|characters?|KB|KiB|B)\b")
SNAKE_CASE_TOKEN_RE = re.compile(r"`([a-z][a-z0-9]*(?:_[a-z0-9]+)+)`")

PROTOCOL_ROLE_RE = re.compile(
    r"seven role fields in its existing payload channel: ((?:`[a-z_]+`(?:,\s*)?)+)\.")
INJECTIONS_RE = re.compile(
    r"The four pre-existing injections keep their owners and travel by pointer: (.*?)\.\s", re.S)
INJECTION_ITEM_RE = re.compile(r"(?:^|,\s*(?:and\s+)?|\s+and\s+)(the [a-z][^(),]*?)\s*\(`")


def _owner_text() -> str:
    return owner_text()


def _norm(cell: str) -> str:
    return " ".join(cell.replace("`", "").split()).lower()


def _layout_rows(text: str):
    header, rows = table_rows(text, "Layout")
    return tuple(header), rows


def _forms_matrix(text: str) -> dict:
    header, rows = table_rows(text, "Forms")
    assert tuple(header) == FORMS_COLUMNS, (
        f"## Forms table header must be {FORMS_COLUMNS}, got {header}")
    matrix = {}
    for row in rows:
        assert len(row) == 2, f"## Forms row malformed: {row}"
        matrix[row[0]] = split_layers(row[1])
    return matrix


def _protocol_items() -> tuple:
    """The super↔sub protocol owner's declared item set (role fields, injections)."""
    assert PROTOCOL_OWNER.is_file(), f"protocol owner missing: {PROTOCOL_OWNER}"
    text = PROTOCOL_OWNER.read_text(encoding="utf-8")
    roles_match = PROTOCOL_ROLE_RE.search(text)
    assert roles_match, "could not parse the seven role fields from the protocol owner"
    roles = tuple(re.findall(r"`([a-z_]+)`", roles_match.group(1)))
    injections_match = INJECTIONS_RE.search(text)
    assert injections_match, "could not parse the four injections from the protocol owner"
    items = INJECTION_ITEM_RE.findall(injections_match.group(1))
    injections = tuple(item[len("the "):] for item in items)
    return roles, injections


def _baseline_items() -> tuple:
    assert PRE_CHANGE_NOTES.is_file(), f"pre-change notes missing: {PRE_CHANGE_NOTES}"
    text = PRE_CHANGE_NOTES.read_text(encoding="utf-8")
    block = re.search(
        r"<!-- protocol-baseline:begin -->(.*?)<!-- protocol-baseline:end -->", text, re.S)
    assert block, "notes/pre-change-measurements.md carries no protocol-baseline block"
    return marker_list(block.group(1), "role_fields"), marker_list(block.group(1), "injections")


# --------------------------------------------------------------------------- #
# C-001 — one owner document, one declared ownership set
# --------------------------------------------------------------------------- #
def test_owner_document_is_the_single_model_home():
    assert OWNER_DOC.is_file(), f"owner document missing: {OWNER_DOC}"
    text = _owner_text()
    headings = [line for line in text.splitlines() if line.startswith("# ")]
    assert headings == ["# Context Management(上下文管理)"], (
        f"the owner document must carry exactly the one H1 `# Context Management(上下文管理)`, got {headings}")
    owned = set(marker_list(text, "owns"))
    assert owned == OWNED_SURFACES, (
        f"the `owns:` set must be exactly the twelve owned surfaces; missing={sorted(OWNED_SURFACES - owned)} extra={sorted(owned - OWNED_SURFACES)}")
    for surface in OWNED_SURFACES:
        assert surface, "empty owns token"


def test_no_second_layout_home_exists():
    """C-004: the layout table lives only in the owner document."""
    declaring = []
    for path in sorted(DEFINITIONS_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        header, rows = table_rows(text, "Layout")
        if header:
            declaring.append((path.name, header))
    assert declaring == [("context-management-definitions.md", LAYOUT_COLUMNS)], (
        f"exactly one file may declare the six-column layout table, got {declaring}")


# --------------------------------------------------------------------------- #
# C-002 — bilingual definition sites carry the fixed literals
# --------------------------------------------------------------------------- #
def test_bilingual_definition_sites_carry_the_fixed_literals():
    text = _owner_text()
    for literal in STR_LITERALS:
        assert literal in text, f"definition-site literal missing verbatim: {literal!r}"
    for token in ("invariant", "variable", "system", "project", "task"):
        assert token in text, f"machine token missing from the owner document: {token}"


# --------------------------------------------------------------------------- #
# C-003 — the terminology boundary names four neighbours by pointer
# --------------------------------------------------------------------------- #
def test_terminology_boundary_table_names_four_neighbours_by_pointer():
    text = _owner_text()
    header, rows = table_rows(text, "Terminology Boundary")
    assert tuple(header) == BOUNDARY_COLUMNS, f"boundary header must be {BOUNDARY_COLUMNS}"
    assert len(rows) == 4, f"the boundary table must carry four neighbour rows, got {len(rows)}"
    for row in rows:
        assert len(row) == 3 and all(cell.strip() for cell in row), f"boundary row malformed: {row}"
    by_neighbour = {_norm(row[0]): row for row in rows}

    project_context = next((row for key, row in by_neighbour.items() if "project context" in key), None)
    assert project_context, "the `## Project Context` neighbour row is missing"
    assert "src/specify_cli/__init__.py" in project_context[1], (
        f"the Project Context row must point at the render path; got {project_context[1]!r}")
    assert "render_agents_for_tool" in project_context[1]

    dispatch = next((row for key, row in by_neighbour.items()
                     if "super" in key and "dispatch" in key), None)
    assert dispatch, "the super<->sub dispatch payload neighbour row is missing"
    assert "shared/definitions/superagent-definitions.md" in dispatch[1], (
        f"the dispatch row must point at the protocol owner; got {dispatch[1]!r}")

    ambient = next((row for key, row in by_neighbour.items() if "ambient" in key), None)
    assert ambient, "the ambient instructions neighbour row is missing"
    assert "templates/instructions-template.md" in ambient[1]
    assert "scripts/bash/generate-instructions.sh" in ambient[1]

    window = next((row for key, row in by_neighbour.items() if "context window" in key), None)
    assert window, "the model context window neighbour row is missing"
    assert "not a framework artifact" in window[1].lower(), (
        f"the context-window row must say it is not a framework artifact; got {window[1]!r}")

    for path in ("src/specify_cli/__init__.py",
                 "shared/definitions/superagent-definitions.md",
                 "templates/instructions-template.md",
                 "scripts/bash/generate-instructions.sh"):
        assert (REPO_ROOT / path).exists(), f"boundary pointer does not resolve: {path}"


# --------------------------------------------------------------------------- #
# C-005 — the five forms and their legality matrix
# --------------------------------------------------------------------------- #
def test_forms_matrix_matches_the_contract():
    matrix = _forms_matrix(_owner_text())
    assert set(matrix) == set(FORM_MATRIX), (
        f"form domain drifted: missing={sorted(set(FORM_MATRIX) - set(matrix))} extra={sorted(set(matrix) - set(FORM_MATRIX))}")
    for form, layers in FORM_MATRIX.items():
        assert set(matrix[form]) == set(layers), (
            f"form {form!r} legal layers must be {layers}, got {matrix[form]}")
    for layer in ("system", "project", "task"):
        assert any(layer in layers for layers in matrix.values()), (
            f"layer {layer!r} never appears in the matrix")


# --------------------------------------------------------------------------- #
# C-004 — the layout table is the single home of the row data
# --------------------------------------------------------------------------- #
def test_layout_table_is_the_single_row_data_home():
    text = _owner_text()
    header, rows = _layout_rows(text)
    assert tuple(header) == LAYOUT_COLUMNS, (
        f"the layout header must be exactly {LAYOUT_COLUMNS}, got {header}")
    assert "category" not in {cell.lower() for cell in header}, (
        "the layout table must carry no category column")
    assert len(rows) == 18, f"the layout must carry the eighteen seed rows, got {len(rows)}"
    for row in rows:
        assert len(row) == 6, f"layout row malformed: {row}"
        assert all(cell.strip() for cell in row), f"layout row carries an empty cell: {row}"
    class_ids = [row[0] for row in rows]
    assert len(set(class_ids)) == len(class_ids), f"duplicate class id in the layout: {class_ids}"
    layers = [row[1] for row in rows]
    order = {"system": 0, "project": 1, "task": 2}
    assert all(layer in order for layer in layers), f"unknown layer in the layout: {layers}"
    ranks = [order[layer] for layer in layers]
    assert ranks == sorted(ranks), "layout rows must be grouped in composition order system -> project -> task"
    counts = {layer: layers.count(layer) for layer in order}
    assert counts == {"system": 4, "project": 7, "task": 7}, (
        f"the seed roster must be 4/7/7, got {counts}")
    for concept_id in ("project-vocabulary", "concept-definitions", "concept-explanations"):
        assert concept_id in class_ids, f"concept-pointer row missing from the layout: {concept_id}"
        row = rows[class_ids.index(concept_id)]
        assert row[1] == "project", f"concept-pointer row must sit on the project layer: {row}"
    forms = {row[2] for row in rows}
    assert forms == set(FORM_MATRIX), f"the layout must exercise every form, got {sorted(forms)}"


# --------------------------------------------------------------------------- #
# C-006 / C-043 — the layer landing contract
# --------------------------------------------------------------------------- #
def test_landing_contract_declares_three_cells_and_three_forbidden_pairs():
    text = _owner_text()
    header, rows = table_rows(text, "Landing Contract")
    assert tuple(header) == LANDING_COLUMNS, f"landing contract header must be {LANDING_COLUMNS}, got {header}"
    assert len(rows) == 3, f"the landing contract must declare exactly three legal cells, got {len(rows)}"
    cells = [row[0] for row in rows]
    assert set(cells) == set(LEGAL_CELLS), (
        f"legal cells must be exactly {LEGAL_CELLS}, got {cells}")
    body = section_body(text, "Landing Contract")
    for forbidden in FORBIDDEN_CELLS:
        assert forbidden in body, f"forbidden combination missing from the landing contract: {forbidden}"
        assert forbidden not in cells, f"forbidden combination appears as a legal row: {forbidden}"
    matrix = _forms_matrix(text)
    form_tokens = set(FORM_MATRIX)
    for row in rows:
        assert len(row) == 5 and all(cell.strip() for cell in row), f"landing row malformed: {row}"
        allowed = row[3].lower()
        assert ("§ forms" in allowed) or ("c-005" in allowed), (
            f"allowed forms must reference § Forms (C-005), never restate a value list; got {row[3]!r}")
        restated = [token for token in form_tokens if token in allowed]
        assert not restated, (
            f"allowed-forms cell restates form tokens {restated} instead of referencing the matrix")
    _, layout_rows = _layout_rows(text)
    for row in layout_rows:
        layer, form = row[1], row[2]
        assert form in matrix, f"layout form outside the matrix: {row}"
        assert layer in matrix[form], (
            f"layout row ({row[0]}) escapes its cell: form {form!r} is not legal on layer {layer!r}")


# --------------------------------------------------------------------------- #
# C-014 — presence vocabulary defined once; Unobserved reached by pointer
# --------------------------------------------------------------------------- #
def test_presence_vocabulary_defined_once_with_unobserved_pointer():
    text = _owner_text()
    header, rows = table_rows(text, "Presence Vocabulary")
    assert tuple(header) == PRESENCE_COLUMNS, f"presence table header must be {PRESENCE_COLUMNS}"
    tokens = [row[0] for row in rows]
    assert len(rows) == 5, f"the presence vocabulary must define exactly five tokens, got {tokens}"
    assert set(tokens) == set(PRESENCE_TOKENS), (
        f"presence token domain drifted: missing={sorted(set(PRESENCE_TOKENS) - set(tokens))} extra={sorted(set(tokens) - set(PRESENCE_TOKENS))}")
    for row in rows:
        assert len(row) == 2 and row[1].strip(), f"presence row carries no meaning: {row}"
    body = section_body(text, "Presence Vocabulary")
    assert "Unobserved" in body, "the presence section must reach Unobserved by pointer"
    assert "shared/declarations/facts/evidence-seven-states.yaml#/statement" in body, (
        "the Unobserved pointer must name its evidence-state owner")


# --------------------------------------------------------------------------- #
# C-007 / C-026 — the concept-pointer slot
# --------------------------------------------------------------------------- #
def test_concept_pointer_slot_carries_the_triple_and_four_structures():
    text = _owner_text()
    body = section_body(text, "Concept Pointer")
    assert body, "the `## Concept Pointer` section is missing"
    assert marker_value(body, "glossary") == ".specify/glossary.md", (
        "the glossary pointer must target .specify/glossary.md")
    assert marker_value(body, "definitions") == ".specify/shared/definitions/", (
        "the definitions pointer must target the installed definitions tree")
    explanations = marker_value(body, "explanations")
    assert ".specify/skills.md" in explanations and ".specify/tools.md" in explanations, (
        "the explanations pointer must target both .specify/skills.md and .specify/tools.md")
    header, rows = table_rows(text, "Concept Pointer")
    assert tuple(header) == tuple(CONCEPT_STRUCTURE_COLUMNS), (
        f"structure table header must be {CONCEPT_STRUCTURE_COLUMNS}, got {header}")
    labels = [_norm(row[0]) for row in rows]
    for expected in CONCEPT_STRUCTURE_LABELS:
        assert expected in labels, f"governed structure missing from the slot table: {expected}"
    assert len(rows) == 4, f"the slot table must carry exactly four structures, got {len(rows)}"
    surfaces = ("manifest", "documentation map", "reading list", "re-anchoring statement")
    for row in rows:
        assert len(row) == 4 and all(cell.strip() for cell in row), f"structure row malformed: {row}"
        presence = row[3].lower()
        assert any(surface in presence for surface in surfaces), (
            f"structure row {row[0]!r} names no readable presence surface: {row[3]!r}")
    assert "Unobserved" in body, "the slot section must declare the Unobserved absence reading"
    assert "not-evaluated" in body, "the slot section must name the missing-layout-row reading"


def marker_value(text: str, marker: str) -> str:
    """The value of a ``<marker>: <value>`` line inside a section body."""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(f"{marker}:"):
            return stripped[len(marker) + 1:].strip()
    return ""


# --------------------------------------------------------------------------- #
# C-022 — the closed seven-trigger set
# --------------------------------------------------------------------------- #
def test_trigger_set_is_closed_at_seven_with_composer_scope_and_evidence():
    text = _owner_text()
    header, rows = table_rows(text, "Triggers")
    assert tuple(header) == TRIGGER_COLUMNS, f"trigger table header must be {TRIGGER_COLUMNS}, got {header}"
    triggers = [row[0] for row in rows]
    assert len(rows) == 7, f"the trigger set is closed at seven, got {triggers}"
    assert set(triggers) == set(TRIGGER_ROWS), (
        f"trigger set drifted: missing={sorted(set(TRIGGER_ROWS) - set(triggers))} extra={sorted(set(triggers) - set(TRIGGER_ROWS))}")
    for row in rows:
        assert len(row) == 4 and all(cell.strip() for cell in row), f"trigger row malformed: {row}"
        trigger = row[0]
        composer, scope_tokens, evidence_tokens = TRIGGER_ROWS[trigger]
        composer_cell = _norm(row[1])
        assert composer in composer_cell, (
            f"{trigger}: composer must resolve to {composer!r}, got {row[1]!r}")
        scope_cell = _norm(row[2])
        assert any(token in scope_cell for token in scope_tokens), (
            f"{trigger}: scope must name one of {scope_tokens}, got {row[2]!r}")
        evidence_cell = _norm(row[3])
        assert any(token in evidence_cell for token in evidence_tokens), (
            f"{trigger}: evidence must name one of {evidence_tokens}, got {row[3]!r}")


# --------------------------------------------------------------------------- #
# C-023 — composer roles resolve through the existing relative role model
# --------------------------------------------------------------------------- #
def test_composer_roles_resolve_through_the_existing_model():
    text = _owner_text()
    body = section_body(text, "Composer Roles")
    assert body, "the `## Composer Roles` section is missing"
    assert "shared/definitions/superagent-definitions.md" in body, (
        "the composer roles must reach the relative role model by pointer")
    lowered = body.lower()
    for phrase in ("root session", "superagent", "composer of the current work", "dispatched executor"):
        assert phrase in lowered, f"composer role missing from the section: {phrase}"
    assert "re-gather" in lowered, (
        "the dispatched-executor boundary must state that it MUST NOT re-gather context")
    assert "holder" in lowered, (
        "the task-scope composer must be declared as a holder resolution, not a new role value")


# --------------------------------------------------------------------------- #
# C-020 / C-021 — baseline once, task per selection
# --------------------------------------------------------------------------- #
def test_composition_protocol_declares_baseline_once_and_task_selection():
    text = _owner_text()
    body = section_body(text, "Composition Protocol")
    assert body, "the `## Composition Protocol` section is missing"
    baseline = marker_value(body, "baseline_composition").lower()
    assert "once" in baseline and "session-entry" in baseline, (
        f"baseline_composition must state once-per-session-or-line at session-entry; got {baseline!r}")
    assert marker_list(body, "baseline_refresh_triggers") == ("session-entry", "source-drift"), (
        "baseline refresh is allowed exactly at session-entry and source-drift")
    assert marker_list(body, "task_composition_triggers") == (
        "task-entry", "task-switch", "stage-boundary"), (
        "task composition fires exactly at task-entry, task-switch and stage-boundary")
    assert marker_list(body, "baseline_scope") == ("session", "line"), (
        "the baseline scope must name the session and the line")
    lowered = body.lower()
    assert "compaction" in lowered, "the session definition must distinguish a compaction (reentry)"
    assert "state spine" in lowered, "the line definition must name the state spine"
    assert "discard" in lowered, "task content must be discarded at task end"
    assert "cap" in lowered, "task composition must stay within the owner-declared cap"
    assert "pointer" in lowered, "invariant sources must be cited by pointer only"


# --------------------------------------------------------------------------- #
# C-024 / C-028 — source drift and reentry semantics
# --------------------------------------------------------------------------- #
def test_source_drift_and_reentry_semantics():
    text = _owner_text()
    body = section_body(text, "Composition Protocol")
    lowered = body.lower()
    assert "source-drift" in lowered, "the source-drift trigger must be declared"
    assert "no watcher" in lowered and "poll" in lowered, (
        "source drift must be an observed record change, never a poll, watcher or daemon")
    assert "reentry" in lowered, "the reentry trigger must be declared"
    assert "re-cite" in lowered, "reentry must re-cite the baseline by pointer"
    assert "task-delta" in lowered, "reentry must refresh task-delta"
    assert "re-anchoring statement" in lowered, "reentry must record the re-anchoring statement"
    assert "shared/definitions/re-anchoring-definitions.md" in body, (
        "the re-anchoring tiers must be reached by pointer, never restated")


# --------------------------------------------------------------------------- #
# C-025 / C-042 — dispatch mapping adds nothing; protocol boundary unchanged
# --------------------------------------------------------------------------- #
def test_dispatch_mapping_adds_nothing_and_matches_the_protocol_baseline():
    text = _owner_text()
    body = section_body(text, "Dispatch Mapping")
    assert body, "the `## Dispatch Mapping` section is missing"
    doc_roles = marker_list(body, "role_fields")
    doc_injections = marker_list(body, "injections")
    live_roles, live_injections = _protocol_items()
    baseline_roles, baseline_injections = _baseline_items()
    assert live_roles == baseline_roles, (
        f"the protocol's declared role-field set changed since the pre-change baseline: {live_roles} != {baseline_roles}")
    assert live_injections == baseline_injections, (
        f"the protocol's declared injection set changed since the pre-change baseline: {live_injections} != {baseline_injections}")
    assert doc_roles == baseline_roles, (
        f"the owner document's role-field mapping drifted from the baseline: {doc_roles} != {baseline_roles}")
    assert doc_injections == baseline_injections, (
        f"the owner document's injection mapping drifted from the baseline: {doc_injections} != {baseline_injections}")
    field_tokens = set(SNAKE_CASE_TOKEN_RE.findall(body))
    assert field_tokens == set(baseline_roles), (
        f"the dispatch mapping section may name only the seven role fields; got {sorted(field_tokens)}")
    assert "shared/definitions/superagent-definitions.md" in body, (
        "the mapping must cite the protocol owner, never restate it")
    negated = " ".join(
        line.lower() for line in body.splitlines()
        if "add no" in line.lower() or "adds no" in line.lower())
    for token in ("field", "injection", "cap", "identifier", "self-check"):
        assert token in negated, (
            f"the mapping must declare that it adds no new {token}")
    assert "return_channel" in body, "the uplink return channel must be named"
    assert not CAP_UNIT_RE.search(body), "the dispatch mapping must carry no numeric cap literal"


# --------------------------------------------------------------------------- #
# C-037 — the ambient section: presence, pointer shape, template-side mutation
# --------------------------------------------------------------------------- #
def _ambient_section(text: str) -> str:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == AMBIENT_HEADING:
            start = index + 1
            break
    if start is None:
        return ""
    out = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        out.append(line)
    return "\n".join(out)


def _ambient_violations(text: str) -> list:
    problems = []
    body = _ambient_section(text)
    if not body:
        return ["section missing"]
    if AMBIENT_OWNER_POINTER not in body:
        problems.append("owner pointer missing")
    if AMBIENT_AUDIT_ENTRY not in body:
        problems.append("audit entry missing")
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("|"):
            problems.append("table line present")
            break
    for class_id in SEED_CLASS_IDS:
        if class_id in body:
            problems.append(f"class roster leaks: {class_id}")
            break
    if CAP_UNIT_RE.search(body):
        problems.append("cap literal present")
    return problems


def test_ambient_section_is_present_in_template_and_live_and_pointer_shaped():
    assert TEMPLATE.is_file(), f"instructions template missing: {TEMPLATE}"
    assert LIVE_INSTRUCTIONS.is_file(), f"live instructions missing: {LIVE_INSTRUCTIONS}"
    for path in (TEMPLATE, LIVE_INSTRUCTIONS):
        text = path.read_text(encoding="utf-8")
        assert AMBIENT_HEADING in text.splitlines(), (
            f"the ambient section heading is missing verbatim from {path}")
        assert _ambient_violations(text) == [], (
            f"the ambient section in {path} is not pointer-shaped: {_ambient_violations(text)}")


def test_ambient_section_mutation_leg_fires_on_the_template_side():
    assert TEMPLATE.is_file(), f"instructions template missing: {TEMPLATE}"
    pristine = TEMPLATE.read_text(encoding="utf-8")
    assert _ambient_violations(pristine) == [], (
        f"the pristine template must be clean: {_ambient_violations(pristine)}")

    without_section = pristine.split(AMBIENT_HEADING)[0]
    assert _ambient_violations(without_section), (
        "a template that drops the ambient section must trip the checker")

    table_injected = pristine + "\n## Probe Table\n\n| a | b |\n|---|---|\n| 1 | 2 |\n"
    assert _ambient_violations(table_injected) == [], (
        "a table outside the ambient section must not trip the checker")

    section_tampered = pristine.replace(
        AMBIENT_AUDIT_ENTRY, "the audit entry", 1)
    assert "audit entry missing" in _ambient_violations(section_tampered)


def test_ambient_section_cap_literal_and_roster_mutations_trip_the_checker():
    assert TEMPLATE.is_file(), f"instructions template missing: {TEMPLATE}"
    pristine = TEMPLATE.read_text(encoding="utf-8")
    body = _ambient_section(pristine)
    assert body, "the ambient section is missing from the template"

    cap_mutated = pristine.replace(body, body + "\nKeep it under 40 tokens.\n", 1)
    assert "cap literal present" in _ambient_violations(cap_mutated)

    roster_mutated = pristine.replace(body, body + "\n- runtime-environment\n", 1)
    assert any(violation.startswith("class roster leaks") for violation in _ambient_violations(roster_mutated))

    table_mutated = pristine.replace(body, body + "\n| class id | layer |\n|---|---|\n", 1)
    assert "table line present" in _ambient_violations(table_mutated)


# --------------------------------------------------------------------------- #
# C-029 / C-045 — red lines: no persistence, no replacement, no new surface
# --------------------------------------------------------------------------- #
def test_red_lines_declare_no_new_surface():
    text = _owner_text()
    body = section_body(text, "Red Lines")
    assert body, "the `## Red Lines` section is missing"
    red_lines = set(marker_list(body, "red_lines"))
    expected = {"no-persistence", "no-owner-replacement", "no-new-command", "no-new-gate", "no-watcher"}
    assert red_lines == expected, (
        f"red-line set drifted: missing={sorted(expected - red_lines)} extra={sorted(red_lines - expected)}")
    lowered = body.lower()
    for token in ("persist", "store", "command", "watcher"):
        assert token in lowered, f"the red lines must name {token!r}"