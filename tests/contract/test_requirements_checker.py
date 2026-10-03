"""Contract tests for contracts/requirements-checker.md — all 29 clauses (Feature 053, T008).

Subject: ``scripts/python/validate-requirements.py``. The checker is exercised through its real
``main()`` / CLI, never by re-implementing its regexes here.

This file owns the canonical pin of the US1 checker's label set (``REQUIREMENTS_CHECKS``);
tests/contract/test_checker_form.py reads it from here rather than keeping a second copy.

Class labeling: [制品类] clauses are asserted mechanically; [行为类] clauses (C-6, C-10, C-18,
C-19, C-21, C-27) are asserted through the artifact-side proxy their own text names, and the
test name says which proxy. Nothing here claims a behavior-class clause is guard-covered.

Red-first: red until T009 (the checker), T011/T012 (command + guidelines wiring) and T013
(the FR-014 debt) land.
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts" / "python"
CHECKER = SCRIPTS / "validate-requirements.py"
SPEC = ROOT / ".specify" / "specs" / "053-machine-decidable-artifacts"
CONTRACT = SPEC / "contracts" / "requirements-checker.md"
TAXONOMY = ROOT / "shared" / "constants" / "clarify-taxonomy.md"
GUIDELINES = ROOT / "shared" / "guidelines" / "requirements-guidelines.md"
CMD_TEMPLATE = ROOT / "templates" / "commands" / "requirements.md"
CLARIFY_TESTS = ROOT / "tests" / "contract" / "test_clarify_semantic_completeness.py"

# C-2: the label set is the pin, never a count (checker-form C-22).
REQUIREMENTS_CHECKS = {
    "id-contiguous",
    "doc-order",
    "ref-resolvable",
    "marker-count",
    "dup-id",
}

STR_ORDER_BREAK = "ORDER BREAK: {} after {}"


def _load():
    if not CHECKER.is_file():
        raise AssertionError("validate-requirements.py is missing — T009 has not landed")
    spec = importlib.util.spec_from_file_location("validate_requirements", CHECKER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run(args, expect=None):
    r = subprocess.run(
        [sys.executable, str(CHECKER), *args], capture_output=True, text=True, cwd=str(ROOT)
    )
    if expect is not None:
        assert r.returncode == expect, f"exit {r.returncode}\n{r.stdout}\n{r.stderr}"
    return r


def _write(tmp_path, name, text):
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return p


def _findings(stdout, label=None):
    """Only `<lineno>: <label>: ` lines are findings. The human output ALSO prints a per-check
    summary line (`  [label] pass (0)`), so asserting that a label is absent from stdout is
    never a valid form — it fails on a clean run. Assert on finding lines instead."""
    out = [l for l in stdout.splitlines() if re.match(r"^\d+: [a-z-]+: ", l)]
    return [l for l in out if label is None or l.split(": ", 2)[1] == label]


GOOD = "# Spec\n\n## Requirements\n\n- **FR-001**: a\n- **FR-002**: b\n\n## Success Criteria\n\n- **SC-001**: c\n"


# --------------------------------------------------------------------------- #
# C-1 / C-2 / C-3 — the check surface and message form
# --------------------------------------------------------------------------- #

def test_c01_c02_docstring_enumerates_exactly_the_five_labels():
    mod = _load()
    extracted = set(re.findall(r"^  ([A-Za-z][A-Za-z-]*)\s{2,}", mod.__doc__ or "", re.M))
    assert extracted == REQUIREMENTS_CHECKS


def test_c03_every_message_starts_with_lineno_label(tmp_path):
    mod = _load()
    p = _write(tmp_path, "bad.md", "# S\n\n- **FR-001**: a\n- **FR-003**: b\n")
    r = _run([str(p)])
    assert r.returncode == 1
    msgs = [l for l in r.stdout.splitlines() if re.match(r"^\d+: [a-z-]+: ", l)]
    assert msgs, r.stdout
    for m in msgs:
        label = m.split(": ", 2)[1]
        assert label in REQUIREMENTS_CHECKS, m


# --------------------------------------------------------------------------- #
# C-4 / C-5 / C-6 — id contiguity
# --------------------------------------------------------------------------- #

def test_c04_sequences_are_independent_per_prefix(tmp_path):
    ok = _write(tmp_path, "ok.md",
                "# S\n\n- **FR-001**: a\n- **FR-002**: b\n- **FR-003**: c\n\n- **SC-001**: x\n- **SC-002**: y\n")
    assert _load().main([str(ok)]) == 0
    gap = _write(tmp_path, "gap.md", "# S\n\n- **FR-001**: a\n- **FR-003**: c\n")
    r = _run([str(gap)], expect=1)
    assert "id-contiguous" in r.stdout and "FR-002" in r.stdout


def test_c05_only_definition_lines_join_the_sequence(tmp_path):
    """A prose mention of FR-009 must not extend or break the sequence."""
    p = _write(tmp_path, "prose.md",
               "# S\n\n- **FR-001**: a\n\nSee FR-009 and SC-004 elsewhere.\n")
    r = _run([str(p)])
    assert not _findings(r.stdout, "id-contiguous")


def test_c06_proxy_zero_padding_and_letter_suffixes_are_format_violations(tmp_path):
    """C-6 is [行为类]; its proxy is that both spellings are named and NOT normalized away."""
    p = _write(tmp_path, "forms.md", "# S\n\n- **FR-7**: a\n- **FR-007**: b\n- **FR-003a**: c\n")
    r = _run([str(p)])
    assert r.returncode == 1
    assert "FR-7" in r.stdout and "FR-007" in r.stdout and "FR-003a" in r.stdout


# --------------------------------------------------------------------------- #
# C-7 … C-10 — document order
# --------------------------------------------------------------------------- #

def test_c07_doc_order_is_anchored_on_definition_lines():
    r = _run([str(SPEC / "requirements.md")], expect=0)
    assert not _findings(r.stdout, "doc-order"), "cross-references legitimately appear out of order"


def test_c08_clarifications_section_is_excluded():
    """This spec's own Clarifications history quotes pre-renumbering definition rows; counting
    them produces a sixth false violation."""
    text = (SPEC / "requirements.md").read_text(encoding="utf-8")
    assert "## Clarifications" in text
    r = _run([str(SPEC / "requirements.md")], expect=0)
    assert not _findings(r.stdout, "doc-order")


def test_c09_violation_uses_the_str002_literal(tmp_path):
    src = (SPEC / "requirements.md").read_text(encoding="utf-8").split("\n")
    row = next(l for l in src if l.startswith("- **SC-002**"))
    out = [l for l in src if not l.startswith("- **SC-002**")]
    i5 = next(i for i, l in enumerate(out) if l.startswith("- **SC-005**"))
    out.insert(i5 + 1, row)
    p = _write(tmp_path, "reordered.md", "\n".join(out))
    r = _run([str(p)], expect=1)
    assert STR_ORDER_BREAK.format("SC-002", "SC-005") in r.stdout


def test_c10_proxy_both_anchors_reasons_are_written_in_the_subject():
    """C-10 is [行为类]: the two anchors must be load-bearing in a truth source, or the next edit
    'simplifies' the extraction and re-introduces false violations. Proxy: the checker's own
    docstring states why each anchor exists."""
    doc = _load().__doc__ or ""
    assert "definition" in doc.lower() or "定义行" in doc
    assert "Clarifications" in doc


# --------------------------------------------------------------------------- #
# C-11 … C-15 — reference resolution
# --------------------------------------------------------------------------- #

def test_c11_all_three_reference_forms_are_checked(tmp_path):
    p = _write(tmp_path, "refs.md",
               "# S\n\n- **FR-001**: cites FR-099 and SC-099 and [[STR-099]]\n\n"
               "## Shared Strings\n\n- **STR-001**: x\n")
    r = _run([str(p)], expect=1)
    for needle in ("FR-099", "SC-099", "STR-099"):
        assert needle in r.stdout, needle
    assert re.search(r"^\d+: ref-resolvable", r.stdout, re.M), "the line number must be named"


def test_c12_backticked_forms_are_mentions(tmp_path):
    p = _write(tmp_path, "mentions.md",
               "# S\n\n- **FR-001**: a\n\nThe form `FR-7` and `[[STR-001]]` are mentions.\n")
    r = _run([str(p)], expect=0)
    # the per-check summary line always names the label; only a FINDING line is a violation
    assert not [l for l in r.stdout.splitlines() if re.match(r"^\d+: ref-resolvable", l)]


def test_c13_dup_id_is_an_error_and_is_not_merged_with_dangling(tmp_path):
    p = _write(tmp_path, "dup.md",
               "# S\n\n- **FR-001**: a\n- **FR-001**: again\n- **FR-002**: cites FR-077\n")
    r = _run([str(p)], expect=1)
    assert "dup-id" in r.stdout and "ref-resolvable" in r.stdout
    dup_lines = [l for l in r.stdout.splitlines() if "dup-id" in l]
    ref_lines = [l for l in r.stdout.splitlines() if "ref-resolvable" in l]
    assert dup_lines and ref_lines and not (set(dup_lines) & set(ref_lines))


def test_c14_str_reference_check_is_bidirectional_on_this_spec():
    r = _run([str(SPEC / "requirements.md"), "--json"], expect=0)
    payload = json.loads(r.stdout)
    check = next(c for c in payload["checks"] if c["label"] == "ref-resolvable")
    assert check["status"] in ("pass", "ok"), check
    text = (SPEC / "requirements.md").read_text(encoding="utf-8")
    defined = set(re.findall(r"(?m)^\|\s*`(STR-\d+)`\s*\|", text))
    referenced = set(re.findall(r"\[\[(STR-\d+)\]\]", text))
    assert defined and referenced
    assert referenced - defined == set() and defined - referenced == set()


def test_c15_consumed_by_column_is_reverse_consistent():
    """Every FR/SC named in a Shared Strings `Consumed by` cell must really cite that STR."""
    text = (SPEC / "requirements.md").read_text(encoding="utf-8")
    rows = re.findall(r"(?m)^\|\s*`(STR-\d+)`\s*\|(.*)$", text)
    assert rows
    bad = []
    for sid, rest in rows:
        for target in re.findall(r"(?:FR|SC)-\d{3}", rest):
            line = next((l for l in text.split("\n") if l.startswith("- **%s**" % target)), None)
            if line is None or "[[%s]]" % sid not in line:
                bad.append((sid, target))
    assert bad == [], f"Consumed-by rows whose target does not cite back: {bad}"


# --------------------------------------------------------------------------- #
# C-16 / C-17 — active marker count
# --------------------------------------------------------------------------- #

def test_c16_marker_count_ignores_backticked_instances(tmp_path):
    p = _write(tmp_path, "markers.md",
               "# S\n\n- **FR-001**: a\n\nThe marker `[NEEDS CLARIFICATION: x]` is quoted; "
               "[NEEDS CLARIFICATION: real one] is not.\n")
    r = _run([str(p)], expect=1)
    assert "marker-count" in r.stdout
    line = next(l for l in r.stdout.splitlines() if "marker-count" in l)
    assert re.search(r"\b1\b", line), f"the quoted instance must not be counted: {line}"


def test_c17_the_regex_uses_a_negative_lookbehind_and_an_inner_colon():
    src = CHECKER.read_text(encoding="utf-8")
    assert re.search(r"\(\?<!`\)\\\[NEEDS CLARIFICATION:", src), (
        "the marker pattern must exclude a backtick prefix and keep the colon inside the pattern"
    )


# --------------------------------------------------------------------------- #
# C-18 … C-21 — wiring
# --------------------------------------------------------------------------- #

def test_c18_the_command_template_invokes_the_checker_and_stops_on_error():
    text = CMD_TEMPLATE.read_text(encoding="utf-8")
    assert "validate-requirements.py" in text
    assert re.search(r"STOP|停止|do not proceed|MUST NOT proceed", text), "no stop obligation"


def test_c19_proxy_output_is_presented_verbatim_not_summarized():
    text = CMD_TEMPLATE.read_text(encoding="utf-8")
    assert re.search(r"verbatim|原样呈现", text)
    assert "summarize the findings" not in text


def test_c20_guidelines_validation_section_cites_the_checker_and_the_timing():
    text = GUIDELINES.read_text(encoding="utf-8")
    section = text[text.index("### Validation Process"):]
    section = section[: section.index("\n## ")] if "\n## " in section else section
    assert "validate-requirements.py" in section
    assert re.search(r"之后|after", section), "the checklist-update timing must be stated"


def test_c21_proxy_no_dangling_count_set_owner_is_claimed():
    """C-21 is [行为类]: this feature must state that counts derive from the checker and must NOT
    inherit the taxonomy's dangling 'full count set' owner claim (escalated as A-1)."""
    text = GUIDELINES.read_text(encoding="utf-8")
    section = text[text.index("### Validation Process"):]
    assert "full count set" not in section


# --------------------------------------------------------------------------- #
# C-22 … C-27 — the FR-014 debt
# --------------------------------------------------------------------------- #

def test_c22_the_transitional_awk_block_is_gone():
    text = TAXONOMY.read_text(encoding="utf-8")
    assert "```awk" not in text
    assert "ORDER BREAK: %s after %s" not in text


def test_c23_the_interim_sentence_is_gone():
    assert "Until that validator ships" not in TAXONOMY.read_text(encoding="utf-8")


def test_c24_the_invariant_now_points_at_the_checker():
    assert "validate-requirements.py" in TAXONOMY.read_text(encoding="utf-8")


def test_c25_anti_vacuity_the_section_survived_the_removal():
    """Zero hits must mean 'removed', not 'the whole section vanished'."""
    text = TAXONOMY.read_text(encoding="utf-8")
    assert len(text.splitlines()) > 50
    assert re.search(r"document.?order|文档序|文档出现序", text, re.I)


def test_c26_c27_the_two_pinning_tests_now_assert_the_new_state():
    src = CLARIFY_TESTS.read_text(encoding="utf-8")
    assert "def test_c4_extraction_is_definition_anchored_and_history_excluded" in src
    assert "def test_c4_shared_implementation_with_the_requirements_validator_is_declared" in src
    assert "the interim extraction block is gone" not in src, (
        "that assertion message still treats the transitional copy's presence as the pass condition"
    )
    assert "validate-requirements.py" in src, "the rewrite must name the checker that now owns the anchors"


# --------------------------------------------------------------------------- #
# C-28 / C-29 — code spans and pair dedup
# --------------------------------------------------------------------------- #

def test_c28_code_spans_parse_by_run_length_not_parity(tmp_path):
    planted = "写在 ```` ``` ```` 围栏内的 (FR-020) 与 `FR-9` 提及"
    p = _write(tmp_path, "spans.md",
               "# S\n\n- **FR-001**: a\n- **FR-020**: b\n\n%s\n" % planted)
    r = _run([str(p)])
    assert "FR-020" not in "".join(_findings(r.stdout, "ref-resolvable")), (
        "the real trailing reference was swallowed by an inline fence marker"
    )


def test_c29_mentions_are_judged_before_spans_and_pairs_are_deduped(tmp_path):
    """`FR-7` and `FR-007` in backticks are one mention each, never two citations of FR-007."""
    p = _write(tmp_path, "dedup.md",
               "# S\n\n- **FR-001**: a\n- **FR-002**: b\n\n"
               "Example forms `FR-1` and `FR-001` are mentions, not citations.\n")
    r = _run([str(p)], expect=0)
    assert not _findings(r.stdout, "ref-resolvable")
    assert not _findings(r.stdout, "dup-id")


# --------------------------------------------------------------------------- #
# SC-001 — the four broken copies, 4/4 with zero cross-masking
# --------------------------------------------------------------------------- #

def test_sc001_four_broken_copies_each_name_exactly_their_own_class(tmp_path):
    src_text = (SPEC / "requirements.md").read_text(encoding="utf-8")
    src_lines = src_text.split("\n")

    # FR-030, not FR-023: FR-023 is cited in prose by two other rows, so deleting its
    # definition would fire ref-resolvable as well and mask the id-contiguous class.
    # Isolation measured 2026-10-03 (20 FR ids have zero non-definition mentions).
    b1 = [l for l in src_lines if not l.startswith("- **FR-030**")]

    row = next(l for l in src_lines if l.startswith("- **SC-002**"))
    b2 = [l for l in src_lines if not l.startswith("- **SC-002**")]
    i5 = next(i for i, l in enumerate(b2) if l.startswith("- **SC-005**"))
    b2.insert(i5 + 1, row)

    b3 = src_text.replace("[[STR-005]]", "[[STR-999]]", 1)
    b4 = src_text.replace("## Overview", "## Overview\n\n[NEEDS CLARIFICATION: probe]", 1)

    cases = {
        "b1": ("\n".join(b1), {"id-contiguous"}),
        "b2": ("\n".join(b2), {"doc-order"}),
        "b3": (b3, {"ref-resolvable"}),
        "b4": (b4, {"marker-count"}),
    }
    for name, (text, expected) in cases.items():
        p = _write(tmp_path, name + ".md", text)
        r = _run([str(p)], expect=1)
        labels = {m.split(": ", 2)[1] for m in r.stdout.splitlines() if re.match(r"^\d+: [a-z-]+: ", m)}
        assert labels == expected, f"{name}: reported {labels}, expected exactly {expected}"


# --------------------------------------------------------------------------- #
# the contract artifact itself
# --------------------------------------------------------------------------- #

def test_the_contract_still_has_the_clause_count_this_suite_pins():
    ids = re.findall(r"(?m)^\*\*C-(\d+)\*\*", CONTRACT.read_text(encoding="utf-8"))
    assert len(ids) == 29, f"clause count moved: {len(ids)}"
    assert [int(i) for i in ids] == list(range(1, 30))
