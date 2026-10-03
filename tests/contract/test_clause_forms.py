"""Unit tests for scripts/python/clause_extract.py — the executable counterpart of
shared/definitions/contract-clause-definitions.md (Feature 053, US3 / Foundational).

Every assertion here pins a rule the owner document declares. The suite MUST be red
before the module exists (Tests Mode = ON, Constitution Principle IV).
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts" / "python"
SPECS = ROOT / ".specify" / "specs"

sys.path.insert(0, str(SCRIPTS))

import clause_extract as ce  # noqa: E402  (red until T005 lands)

SIX_FORMS = {
    "md-bold-closed",
    "md-bold-paren",
    "md-heading",
    "yaml-openapi",
    "yaml-assertions",
    "md-none",
}

# Real fixtures, existence-checked at authoring time (pin hygiene rule 2).
FIX_PAREN = SPECS / "031-task-complexity-rubric" / "contracts" / "rubric-section.md"
FIX_MISNOMER = (
    SPECS / "013-portable-skill-creation" / "contracts" / "portable-skill-creation.openapi.yaml"
)
FIX_HEADING = SPECS / "025-agent-skill-enablement" / "contracts" / "agent-skill-enablement-contract.md"
FIX_OPENAPI = SPECS / "018-cli-priority-support" / "contracts" / "cli-priority-support.openapi.yaml"


def _corpus():
    return sorted(p for p in SPECS.glob("*/contracts/*") if p.is_file())


# --------------------------------------------------------------------------- #
# form detection
# --------------------------------------------------------------------------- #

def test_form_names_are_exactly_the_owner_set():
    assert set(ce.FORMS) == SIX_FORMS


@pytest.mark.parametrize(
    "path,expected",
    [
        (FIX_PAREN, "md-bold-paren"),
        (FIX_MISNOMER, "yaml-assertions"),
        (FIX_HEADING, "md-heading"),
        (FIX_OPENAPI, "yaml-openapi"),
    ],
)
def test_real_fixtures_classify_to_the_expected_form(path, expected):
    assert path.is_file(), f"fixture vanished: {path}"
    assert ce.form_of(path) == expected


def test_md_bold_closed_is_detected_on_a_spec_own_contract():
    target = SPECS / "053-machine-decidable-artifacts" / "contracts" / "checker-form.md"
    assert target.is_file()
    assert ce.form_of(target) == "md-bold-closed"


def test_md_none_is_a_named_class_not_a_silent_zero(tmp_path):
    p = tmp_path / "no-clauses.md"
    p.write_text("# Contract\n\nSome prose with no clause markers at all.\n", encoding="utf-8")
    assert ce.form_of(p) == "md-none"
    assert ce.extract_clauses(p) == []
    # the disposition rule: it MUST be nameable, never silently counted as covered
    assert p.name in ce.unparseable_names([p])


def test_the_four_md_forms_never_co_occur_in_one_file():
    md = [p for p in _corpus() if p.suffix == ".md"]
    assert md, "corpus empty — wrong cwd?"
    co_occurring = [p for p in md if len(ce.md_forms_hit(p)) > 1]
    assert co_occurring == []


# --------------------------------------------------------------------------- #
# extraction
# --------------------------------------------------------------------------- #

def test_paren_form_yields_the_ids_the_closed_regex_would_drop():
    """The whole reason md-bold-paren exists: the canonical regex alone finds nothing here."""
    text = FIX_PAREN.read_text(encoding="utf-8")
    assert len(set(re.findall(r"\*\*(C-\d+(?:\.\d+)*)\*\*", text))) == 0
    ids = ce.extract_clauses(FIX_PAREN)
    assert len(ids) == 10
    assert ids[0].startswith("C-")


def test_openapi_clauses_are_path_method_keys_not_a_literal_key_name():
    text = FIX_OPENAPI.read_text(encoding="utf-8")
    assert "openapi:" in text and "paths:" in text
    assert "operations:" not in text, "the corpus has no literal operations: key to probe for"
    ids = ce.extract_clauses(FIX_OPENAPI)
    assert ids, "no method keys extracted"
    assert all(i in {"get", "post", "put", "delete", "patch", "head", "options"} for i in ids)


def test_assertions_form_uses_the_id_key_and_the_misnomer_is_content_judged():
    """013's file is NAMED .openapi.yaml but is not OpenAPI — extension MUST NOT decide."""
    text = FIX_MISNOMER.read_text(encoding="utf-8")
    assert "openapi:" not in text and "paths:" not in text
    assert len(re.findall(r"(?m)^\s+- id:", text)) == 6
    assert ce.form_of(FIX_MISNOMER) == "yaml-assertions"
    assert len(ce.extract_clauses(FIX_MISNOMER)) == 6


def test_parse_doubt_yaml_is_named_never_guessed_zero(tmp_path):
    """Flow-style YAML: it matches the openapi judge but yields no method-key clauses, so it
    MUST be named as parse-doubt rather than reported as '0 clauses, covered' (C-13)."""
    p = tmp_path / "stream.openapi.yaml"
    p.write_text(
        "openapi: 3.0.0\npaths: {/a: {get: {summary: x}}}\n", encoding="utf-8"
    )
    assert ce.extract_clauses(p) == []
    assert p.name in ce.unparseable_names([p])


def test_resolvable_matches_membership(tmp_path):
    p = tmp_path / "c.md"
    p.write_text("**C-1** first\n\n**C-2** second\n", encoding="utf-8")
    assert ce.resolvable(p, "C-1") is True
    assert ce.resolvable(p, "C-2") is True
    assert ce.resolvable(p, "C-3") is False


# --------------------------------------------------------------------------- #
# block extent (owner doc § 4.1)
# --------------------------------------------------------------------------- #

def test_a_section_heading_terminates_a_clause_block(tmp_path):
    p = tmp_path / "extent.md"
    p.write_text(
        "**C-1** body line\n\n## Next Section\n\nFR-002 lives in the heading, not in C-1.\n",
        encoding="utf-8",
    )
    blocks = dict(ce.clause_blocks(p))
    assert "C-1" in blocks
    assert "FR-002" not in blocks["C-1"], "a heading's text MUST NOT join the preceding clause"


def test_the_next_clause_marker_terminates_a_block(tmp_path):
    p = tmp_path / "extent2.md"
    p.write_text("**C-1** aaa\n\n**C-2** bbb\n", encoding="utf-8")
    blocks = dict(ce.clause_blocks(p))
    assert "aaa" in blocks["C-1"] and "bbb" not in blocks["C-1"]
    assert "bbb" in blocks["C-2"]


def test_fenced_code_inside_a_clause_is_not_body(tmp_path):
    p = tmp_path / "fence.md"
    p.write_text("**C-1** text\n\n```\nFR-009 inside a fence\n```\n\n(FR-001)\n", encoding="utf-8")
    blocks = dict(ce.clause_blocks(p))
    assert "FR-009" not in blocks["C-1"]


# --------------------------------------------------------------------------- #
# citation group (owner doc § 4.2) and code spans (§ 4.3)
# --------------------------------------------------------------------------- #

def test_only_the_last_fr_bearing_parenthetical_is_the_citation_group(tmp_path):
    p = tmp_path / "cite.md"
    p.write_text(
        "**C-1** prose mentioning FR-005 in the middle, authority (FR-006), tail (FR-007、D-2)\n",
        encoding="utf-8",
    )
    cites = ce.clause_citations(p)
    assert cites["C-1"] == {"FR-007"}


def test_a_clause_with_no_fr_bearing_group_cites_nothing(tmp_path):
    p = tmp_path / "nocite.md"
    p.write_text("**C-1** text (D-10、A-3)\n\n**C-2** other (FR-011)\n", encoding="utf-8")
    cites = ce.clause_citations(p)
    assert cites["C-1"] == set()
    assert cites["C-2"] == {"FR-011"}


def test_nested_sub_item_suffixes_survive(tmp_path):
    p = tmp_path / "nested.md"
    p.write_text("**C-1** rule (FR-018(a))\n\n**C-2** rule (FR-018(b)、US2 验收场景 6)\n", encoding="utf-8")
    cites = ce.clause_citations(p)
    assert cites["C-1"] == {"FR-018"}
    assert cites["C-2"] == {"FR-018"}


def test_ranges_expand(tmp_path):
    p = tmp_path / "range.md"
    p.write_text("**C-1** covers the block (FR-006…FR-009、D-5)\n", encoding="utf-8")
    assert ce.clause_citations(p)["C-1"] == {"FR-006", "FR-007", "FR-008", "FR-009"}


def test_backticked_examples_are_mentions_not_citations(tmp_path):
    """FR-009's mention-vs-reference rule, at clause granularity."""
    p = tmp_path / "mention.md"
    p.write_text(
        "**C-1** an example `FR-7` and another `FR-007` are mentions; the real tail is (FR-020)\n",
        encoding="utf-8",
    )
    assert ce.clause_citations(p)["C-1"] == {"FR-020"}


def test_code_spans_parse_by_backtick_run_length_not_parity(tmp_path):
    """The planted self-test string from requirements-checker C-28: an inline fence marker
    must not invert the parity of everything after it."""
    p = tmp_path / "runs.md"
    p.write_text(
        "**C-1** 写在 ```` ``` ```` 围栏内的 (FR-020) 与 `FR-9` 提及,真实引用在尾部 (FR-021)\n",
        encoding="utf-8",
    )
    assert ce.clause_citations(p)["C-1"] == {"FR-021"}


# --------------------------------------------------------------------------- #
# table-declared clauses (the shape five real corpus contracts use)
# --------------------------------------------------------------------------- #

FIX_TABLE = SPECS / "050-proactive-flow-trigger" / "contracts" / "trigger-engine.md"


def test_first_cell_table_rows_are_clause_declarations():
    assert FIX_TABLE.is_file(), f"fixture vanished: {FIX_TABLE}"
    assert ce.form_of(FIX_TABLE) == "md-bold-closed"
    assert len(ce.extract_clauses(FIX_TABLE)) == 23


def test_an_id_in_a_non_first_cell_is_a_cross_reference_not_a_clause(tmp_path):
    p = tmp_path / "xref.md"
    p.write_text(
        "**C-1** real clause\n\n"
        "| subject | note |\n|---|---|\n| thing | 即另一契约的 **C-13** |\n",
        encoding="utf-8",
    )
    assert ce.extract_clauses(p) == ["C-1"], "a cross-reference must not join the clause set"


def test_a_table_row_clause_body_is_the_row_itself(tmp_path):
    p = tmp_path / "tablecite.md"
    p.write_text(
        "| id | rule |\n|---|---|\n"
        "| **C-1** | 项目本地 + 禁外传 (FR-020) |\n"
        "| **C-2** | 会话级抑制 (FR-008) |\n",
        encoding="utf-8",
    )
    blocks = dict(ce.clause_blocks(p))
    assert set(blocks) == {"C-1", "C-2"}
    assert "FR-008" not in blocks["C-1"], "a table row must not swallow the next row"
    cites = ce.clause_citations(p)
    assert cites["C-1"] == {"FR-020"} and cites["C-2"] == {"FR-008"}


# --------------------------------------------------------------------------- #
# module hygiene
# --------------------------------------------------------------------------- #

def test_module_is_stdlib_only_no_yaml_dependency():
    """D-2: PyYAML is not a declared dependency; the house precedent is hand parsing."""
    src = (SCRIPTS / "clause_extract.py").read_text(encoding="utf-8")
    assert not re.search(r"(?m)^\s*import yaml\b", src)
    assert not re.search(r"(?m)^\s*from yaml\b", src)


def test_module_docstring_carries_the_program_first_attribution():
    src = (SCRIPTS / "clause_extract.py").read_text(encoding="utf-8")
    doc = ce.__doc__ or ""
    assert "Program-First" in doc or "程序优先" in doc
    assert "contract-clause-definitions.md" in doc or "contract-clause-definitions" in src


def test_module_has_no_write_points():
    """FR-005: every checker in this feature is read-only."""
    src = (SCRIPTS / "clause_extract.py").read_text(encoding="utf-8")
    write_calls = re.findall(r"\b(open\([^)]*['\"][wa]|\.(?:write_text|write_bytes|mkdir|unlink|rmtree)\()", src)
    assert write_calls == [], f"write point found: {write_calls}"


def test_the_extractor_runs_as_a_script_and_exits_zero(tmp_path):
    """An artifact whose contract is to be usable MUST actually be run once."""
    p = tmp_path / "c.md"
    p.write_text("**C-1** only\n", encoding="utf-8")
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / "clause_extract.py"), str(p)],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert r.returncode == 0, r.stderr
    assert "C-1" in r.stdout
