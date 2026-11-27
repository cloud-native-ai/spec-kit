"""Contract guard: the four context-management declaration facts (Feature 110, C-010…C-016, C-046).

Every fact is read through the declaration layer's one parser
(``scripts/python/declaration_reader.py``, ``parse_subset``) and every engine decision is
driven through the engine CLI a consumer actually calls — never through a helper only the
test can reach. The domain membership itself is never copied into this module: each
expected value is read from the fact that owns it, except the contract's closed ordinals
which are pinned literally here as a sanctioned test duplicate.

Authored red-first (C-040): the facts, the registration keys, the engine and the owner
document do not exist yet at this point of the run, so the whole module is expected to
fail before the implementation rows land.
"""
from __future__ import annotations

import ast
import re
import shutil
from pathlib import Path

import pytest

from fixtures.context_management_support import (
    CONTRACT,
    ENGINE,
    FORM_MATRIX,
    FORMS_COLUMNS,
    LAYOUT_COLUMNS,
    REPO_ROOT,
    copy_case_to,
    declaration_reader,
    fact_body,
    fact_path,
    fact_text,
    marker_list,
    owner_text,
    section_body,
    table_rows,
)

pytestmark = pytest.mark.contract

OWNER_DOC = REPO_ROOT / "shared" / "definitions" / "context-management-definitions.md"
CAP_OWNER_SUFFIX = "shared/guidelines/token-efficiency.md"
CAP_SECTION = "摘要优先(Summary-First)"
CAP_UNIT_RE = re.compile(r"\b\d+\s*(?:tokens?|bytes?|chars?|characters?|KB|KiB|B)\b")
CAP_CELL_RE = re.compile(r"^(?P<path>.+) § (?P<section>.+)$")

MANDATORY_FACT_KEYS = {"fact", "kind", "statement", "consumers", "former_carriers"}
EXPECTED_KINDS = {
    "context-categories": "closed-set",
    "context-layers": "closed-set",
    "context-forms": "closed-set",
    "context-classes": "mapping",
}
EXPECTED_DOMAINS = {
    "context-categories": ("invariant", "variable"),
    "context-layers": ("system", "project", "task"),
    "context-forms": ("pointer", "read-in-full", "bounded-index", "runtime-discovery", "inline-digest"),
}
NUMERIC_BOUND_KEYS = {
    "bound", "bounds", "limit", "limits", "cap", "caps",
    "max", "min", "threshold", "thresholds", "budget", "budgets",
}

PRE_EXISTING_CONTRACT_KEYS = {
    "schema", "yaml_subset", "fact_kinds", "completeness_states",
    "exclusion_reasons", "exit_codes", "required_fact_keys",
    "required_exclusion_keys", "gate_call_sites", "registered_facts",
}
POST_093_FACT_KEYS = {
    "concurrency-class", "concurrency-contract", "concurrency-slot-and-reserve",
    "coordinator-dispatch-verdict", "decomposition-coverage", "effective-concurrency",
    "executor-enumeration-roots", "serial-reason",
}
POST_105_FACT_KEYS = {"runtime-store-layout"}


def _fact(slug: str) -> dict:
    return fact_body(slug)


def _statement(slug: str):
    return _fact(slug)["statement"]


def _contract_body() -> dict:
    assert CONTRACT.is_file(), f"declaration contract missing: {CONTRACT}"
    body = declaration_reader().parse_subset(CONTRACT.read_text(encoding="utf-8"), str(CONTRACT))
    assert isinstance(body, dict), "shared/declarations/contract.yaml does not parse as a mapping"
    return body


def _owner_layout_rows():
    text = owner_text()
    header, rows = table_rows(text, "Layout")
    assert tuple(header) == LAYOUT_COLUMNS, f"layout header must be {LAYOUT_COLUMNS}, got {header}"
    return rows


def _owner_forms():
    text = owner_text()
    header, rows = table_rows(text, "Forms")
    assert tuple(header) == FORMS_COLUMNS, f"forms header must be {FORMS_COLUMNS}, got {header}"
    return {row[0]: tuple(part.strip() for part in row[1].split(",") if part.strip())
            for row in rows}


# --------------------------------------------------------------------------- #
# C-010 — the four facts carry the required keys and kinds
# --------------------------------------------------------------------------- #
def test_four_facts_carry_mandatory_keys_and_kinds():
    for slug, kind in EXPECTED_KINDS.items():
        path = fact_path(slug)
        assert path.is_file(), f"declaration fact missing: {path}"
        body = _fact(slug)
        missing = MANDATORY_FACT_KEYS - set(body)
        assert not missing, f"{slug}: mandatory key(s) missing: {sorted(missing)}"
        assert body["fact"] == slug, f"{slug}: fact slug drifted: {body['fact']!r}"
        assert body["kind"] == kind, f"{slug}: kind must be {kind!r}, got {body['kind']!r}"
        former = body["former_carriers"]
        assert former == [] or former == "", (
            f"{slug}: former_carriers must be empty (no earlier artifact carried this domain), got {former!r}")
        consumers = body["consumers"]
        assert isinstance(consumers, list), f"{slug}: consumers must be a list"
        assert "scripts/python/context-audit.py" in consumers, (
            f"{slug}: consumers must name the audit engine")
        assert "tests/contract/test_context_management_declarations.py" in consumers, (
            f"{slug}: consumers must name the declarations guard")


# --------------------------------------------------------------------------- #
# C-010 — append-only registration keys, before any consumer reads them
# --------------------------------------------------------------------------- #
def test_registration_keys_are_append_only_and_point_at_the_facts():
    body = _contract_body()
    keys = set(body)
    missing_pre_existing = (PRE_EXISTING_CONTRACT_KEYS | POST_093_FACT_KEYS | POST_105_FACT_KEYS) - keys
    assert not missing_pre_existing, (
        f"pre-existing declaration contract keys disappeared: {sorted(missing_pre_existing)}")
    for slug in EXPECTED_KINDS:
        assert slug in keys, f"registration key missing from contract.yaml: {slug}"
        expected = f"shared/declarations/facts/{slug}.yaml"
        assert body[slug] == expected, (
            f"{slug}: registration must point at {expected}, got {body[slug]!r}")
        assert (REPO_ROOT / expected).is_file(), f"{slug}: registered fact path does not resolve"
    registered = body.get("registered_facts")
    assert registered == [] or registered, "registered_facts section must survive the append"


# --------------------------------------------------------------------------- #
# C-011 — the domains are closed sets with one owner each
# --------------------------------------------------------------------------- #
def test_closed_sets_members_and_order():
    for slug, expected in EXPECTED_DOMAINS.items():
        statement = _statement(slug)
        assert isinstance(statement, list), f"{slug}: statement must be a block sequence"
        assert tuple(statement) == expected, (
            f"{slug}: members/order must be {expected}, got {tuple(statement)}")
        assert len(set(statement)) == len(statement), f"{slug}: duplicate member in the closed set"
    roster = _statement("context-classes")
    assert isinstance(roster, dict), "context-classes: statement must be a layer -> ids mapping"
    assert set(roster) == set(EXPECTED_DOMAINS["context-layers"]), (
        f"context-classes: mapping keys must be exactly the layer domain, got {sorted(roster)}")
    for layer, ids in roster.items():
        assert isinstance(ids, list) and ids, f"context-classes: layer {layer!r} must list its ids"
        assert len(set(ids)) == len(ids), f"context-classes: duplicate id inside layer {layer!r}"


# --------------------------------------------------------------------------- #
# C-015 — the roster matches the owner document row-for-row
# --------------------------------------------------------------------------- #
def test_classes_roster_matches_the_owner_layout_row_for_row():
    roster = _statement("context-classes")
    rows = _owner_layout_rows()
    for layer in EXPECTED_DOMAINS["context-layers"]:
        declared = list(roster[layer])
        in_layout = [row[0] for row in rows if row[1] == layer]
        assert in_layout == declared, (
            f"layer {layer!r}: layout rows must equal the roster in order; "
            f"layout={in_layout} roster={declared}")
    all_ids = [row[0] for row in rows]
    assert len(set(all_ids)) == len(all_ids), "layout carries a duplicate class id"
    for layer in EXPECTED_DOMAINS["context-layers"]:
        assert roster[layer], f"roster layer {layer!r} must be non-empty"


# --------------------------------------------------------------------------- #
# C-012 — one reader, no second parser, no hard-coded domain member
# --------------------------------------------------------------------------- #
def _domain_members() -> set:
    members = set()
    for slug in ("context-categories", "context-layers", "context-forms"):
        members.update(_statement(slug))
    roster = _statement("context-classes")
    for ids in roster.values():
        members.update(ids)
    return members


def _engine_ast():
    assert ENGINE.is_file(), f"audit engine missing: {ENGINE}"
    source = ENGINE.read_text(encoding="utf-8")
    return source, ast.parse(source)


def test_engine_is_a_single_reader_with_no_hard_coded_members():
    source, tree = _engine_ast()
    assert "declaration_reader" in source, (
        "the engine must read the four facts through scripts/python/declaration_reader.py")
    assert "load_fact" in source, "the engine must read each fact through load_fact"
    imported = set()
    defined_functions = set()
    string_constants = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            defined_functions.add(node.name)
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            string_constants.add(node.value)
    assert "yaml" not in imported, "the engine must implement no second YAML parser"
    assert "ruamel" not in imported, "the engine must implement no second YAML parser"
    for name in ("parse_subset", "parse_yaml", "load_fact", "load_facts"):
        assert name not in defined_functions, (
            f"the engine must not reimplement the reader: {name}")
    hard_coded = sorted(_domain_members() & string_constants)
    assert not hard_coded, (
        f"the engine carries hard-coded declaration members: {hard_coded}")


# --------------------------------------------------------------------------- #
# C-013 — no numeric bound anywhere in the facts
# --------------------------------------------------------------------------- #
def _walk_keys(value):
    if isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from _walk_keys(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk_keys(item)


def test_facts_carry_no_numeric_bound():
    for slug in EXPECTED_KINDS:
        body = _fact(slug)
        offending = sorted(key for key in _walk_keys(body) if str(key).lower() in NUMERIC_BOUND_KEYS)
        assert not offending, f"{slug}: numeric bound field(s) declared: {offending}"
        assert not CAP_UNIT_RE.search(fact_text(slug)), (
            f"{slug}: a numeric cap literal sits beside a cap unit")


# --------------------------------------------------------------------------- #
# C-013 / FR-019 — cap references are one form resolving to the cap owner
# --------------------------------------------------------------------------- #
def test_cap_references_use_one_form_and_resolve_to_the_cap_owner():
    rows = _owner_layout_rows()
    for row in rows:
        class_id, layer, form, source, owner, cap = row
        if form in ("bounded-index", "read-in-full", "inline-digest"):
            match = CAP_CELL_RE.match(cap)
            assert match, (
                f"{class_id}: a capped/content-bearing row must cite `<path> § <section>`, got {cap!r}")
            path = match.group("path").strip()
            section = match.group("section").strip()
            assert path.endswith(CAP_OWNER_SUFFIX), (
                f"{class_id}: cap owner path must end with {CAP_OWNER_SUFFIX}, got {path!r}")
            assert section == CAP_SECTION, (
                f"{class_id}: cap section must be {CAP_SECTION!r}, got {section!r}")
            resolved = REPO_ROOT / path[len(".specify/"):] if path.startswith(".specify/") else REPO_ROOT / path
            assert resolved.is_file(), f"{class_id}: cap owner path does not resolve: {path}"
        else:
            assert cap in ("—", "-", ""), (
                f"{class_id}: an uncapped row carries a cap reference: {cap!r}")
        assert not CAP_UNIT_RE.search(cap), f"{class_id}: numeric cap literal in the cap cell"


# --------------------------------------------------------------------------- #
# C-011 / C-001 — the three faces agree member-for-member
# --------------------------------------------------------------------------- #
def test_value_domains_agree_with_the_owner_document():
    forms = _owner_forms()
    assert set(forms) == set(_statement("context-forms")), (
        "the owner document's form tokens and context-forms.yaml disagree")
    for form, layers in forms.items():
        assert set(layers) == set(FORM_MATRIX[form]), (
            f"form {form!r}: owner-document matrix drifted from C-005")
    text = owner_text()
    layers_in_layout = {row[1] for row in _owner_layout_rows()}
    assert layers_in_layout == set(_statement("context-layers")), (
        "the layout's layer tokens and context-layers.yaml disagree")
    categories_section = section_body(text, "Categories")
    assert categories_section, "the `## Categories` section is missing"
    for category in _statement("context-categories"):
        assert category in categories_section, (
            f"category token {category!r} missing from the categories section")


# --------------------------------------------------------------------------- #
# C-016 / C-046 — unknown or missing declaration members are refused, exit 2
# --------------------------------------------------------------------------- #
def _assert_refused(workspace_root: Path):
    from fixtures.context_management_support import run_engine_json

    for args in (("--action", "check"), ("--action", "manifest", "--layer", "project")):
        completed, payload = run_engine_json(workspace_root, *args)
        assert completed.returncode == 2, (
            f"declaration error must exit 2 for {args}, got {completed.returncode}\n"
            f"stdout={completed.stdout}\nstderr={completed.stderr}")
        assert '"findings"' not in completed.stdout and '"rows"' not in completed.stdout, (
            f"a partial verdict leaked for {args}: {completed.stdout}")


def test_unknown_declaration_member_is_refused_both_actions(tmp_path: Path):
    root = copy_case_to(tmp_path, "declaration-unknown-member")
    _assert_refused(root)


def test_missing_declaration_fact_is_refused_both_actions(tmp_path: Path):
    root = copy_case_to(tmp_path, "declaration-missing")
    _assert_refused(root)


# --------------------------------------------------------------------------- #
# C-046 / SC-007 — every declared member is exercised
# --------------------------------------------------------------------------- #
def _mutate_statement_member(slug: str, member: str) -> dict:
    text = fact_text(slug)
    old = f"  - {member}\n"
    assert text.count(old) == 1, f"{slug}: member {member!r} not found exactly once"
    mutated = text.replace(old, f"  - {member}-x\n")
    body = declaration_reader().parse_subset(mutated, f"{slug}-mutated")
    assert isinstance(body, dict)
    return body


def test_every_declared_member_is_exercised():
    for slug in ("context-categories", "context-layers", "context-forms"):
        for member in _statement(slug):
            mutated = _mutate_statement_member(slug, member)
            statement = mutated["statement"]
            assert member not in statement, (
                f"{slug}: mutating member {member!r} left it declared — member not exercised")
            assert f"{member}-x" in statement, (
                f"{slug}: the mutated member does not surface in the reading")

    rows = _owner_layout_rows()
    layout_layers = {row[1] for row in rows}
    layout_forms = {row[2] for row in rows}
    derived_categories = {("invariant" if layer in ("system", "project") else "variable")
                          for layer in layout_layers}
    assert layout_layers == set(_statement("context-layers")), (
        "some declared layer never appears in the layout")
    assert layout_forms == set(_statement("context-forms")), (
        "some declared form never appears in the layout")
    assert derived_categories == set(_statement("context-categories")), (
        "some declared category is never derived by a layout row")


def test_layer_and_form_mutations_change_the_engine_output(tmp_path: Path):
    from fixtures.context_management_support import run_engine_json

    clean_root = copy_case_to(tmp_path / "clean", "all-present")
    clean, _ = run_engine_json(clean_root, "--action", "check")
    assert clean.returncode == 0, (
        f"the clean fixture must pass before mutation:\n{clean.stdout}\n{clean.stderr}")

    for slug, member in (("context-layers", "task"), ("context-forms", "pointer")):
        case_dir = tmp_path / f"mutated-{slug}"
        case_dir.mkdir()
        root = copy_case_to(case_dir, "all-present")
        path = root / "shared" / "declarations" / "facts" / f"{slug}.yaml"
        text = path.read_text(encoding="utf-8")
        old = f"  - {member}\n"
        assert text.count(old) == 1
        path.write_text(text.replace(old, f"  - {member}-x\n"), encoding="utf-8")
        mutated, _ = run_engine_json(root, "--action", "check")
        assert mutated.returncode != 0, (
            f"mutating {slug}:{member} produced no engine-level difference")
        assert mutated.stdout != clean.stdout, (
            f"mutating {slug}:{member} left the engine output byte-identical")