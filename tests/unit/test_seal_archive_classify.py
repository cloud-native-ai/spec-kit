"""Unit tests for the path-form classifier (Feature 100, P3).

Contract: ``.specify/specs/100-seal-slice-archive/contracts/reference-classification.contract.md``
C-301 (carrier roster), C-302 (F1/F2/F3 closed forms; bare slug is not a
reference), C-304 (H2 section predicate for the mixed feature-detail carrier).

Constitution Principle IV: the classifier is a pure function and carries its own
unit tests. Red-first reading: ``notes/red-first-evidence.md``.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.unit

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "seal-utils.py"

PARENT = "100-fixture-parent"
ALPHA = "100a-fixture-alpha"
BETA = "100b-fixture-beta"
SLUGS = (ALPHA, BETA)
PARENT_REL = ".specify/specs/%s" % PARENT


def _load_engine():
    spec = importlib.util.spec_from_file_location("seal_utils_archive_classify", ENGINE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def eng():
    return _load_engine()


def _hits(eng, line, *, carrier=PARENT_REL + "/plan.md", tests=False):
    return eng.find_reference_hits(
        line, SLUGS, parent_slug=PARENT, carrier_rel=carrier, tests_carrier=tests)


def test_f1_matches_the_spec_root_form_with_tail(eng):
    hits = _hits(eng, "Pointer: `.specify/specs/%s/plan.md`." % ALPHA)
    assert len(hits) == 1
    assert hits[0]["form"] == "F1"
    assert hits[0]["replacement"] == PARENT_REL + "/slices/" + ALPHA


def test_f1_left_boundary_excludes_absolute_and_dot_paths(eng):
    assert _hits(eng, "See /abs/.specify/specs/%s/plan.md" % ALPHA) == []
    assert _hits(eng, "See ../%s/plan.md" % ALPHA) == []


def test_f1_right_boundary_requires_a_segment_boundary(eng):
    hits = _hits(eng, "See .specify/specs/%s-extra/plan.md" % ALPHA)
    assert hits == [], "a longer slug is not a reference to the declared slug"


def test_f2_matches_the_parent_relative_form_only_inside_the_parent_subtree(eng):
    line = "Sibling shorthand: %s/tasks.md" % BETA
    hits = _hits(eng, line)
    assert len(hits) == 1 and hits[0]["form"] == "F2"
    assert hits[0]["replacement"] == "slices/%s/" % BETA
    assert eng.rewrite_line(line, hits) == "Sibling shorthand: slices/%s/tasks.md" % BETA
    assert _hits(eng, line, carrier="tests/contract/test_x.py", tests=True) == [], (
        "C-302: F2 is only recognized in the parent spec subtree"
    )


def test_f1_wins_over_f2_and_f3_on_overlapping_spans(eng):
    line = "Path .specify/specs/%s/tasks.md and raw %s/tasks.md" % (ALPHA, ALPHA)
    hits = _hits(eng, line)
    forms = [(hit["form"], hit["slug"]) for hit in hits]
    assert forms == [("F1", ALPHA), ("F2", ALPHA)]
    rewritten = eng.rewrite_line(line, hits)
    assert PARENT_REL + "/slices/" + ALPHA + "/tasks.md" in rewritten
    assert "slices/%s/tasks.md" % ALPHA in rewritten
    assert rewritten.count(".specify/specs/%s" % ALPHA) == 0


def test_f3_matches_a_slug_literal_on_a_path_construction_line(eng):
    line = ('SLICE_DIR = REPO_ROOT / ".specify" / "specs" / "%s"' % ALPHA)
    hits = _hits(eng, line, carrier="tests/contract/test_x.py", tests=True)
    assert len(hits) == 1 and hits[0]["form"] == "F3"
    assert hits[0]["replacement"] == "%s/slices/%s" % (PARENT, ALPHA)
    assert eng.rewrite_line(line, hits) == (
        'SLICE_DIR = REPO_ROOT / ".specify" / "specs" / "%s/slices/%s"'
        % (PARENT, ALPHA))


def test_f3_skips_the_identity_literal_on_the_right_of_equality(eng):
    line = ('assert make(".specify/specs/%s") == "%s"' % (BETA, BETA))
    hits = _hits(eng, line, carrier="tests/contract/test_x.py", tests=True)
    assert [(hit["form"], hit["slug"]) for hit in hits] == [("F1", BETA)]
    assert eng.rewrite_line(line, hits).endswith('== "%s"' % BETA), (
        "C-302/C-311: identity constants stay byte-identical"
    )


def test_bare_slug_is_never_a_reference(eng):
    for line in ('"slug": "%s"' % ALPHA,
                 "<!-- source: %s -->" % ALPHA,
                 "- %s：first slice" % ALPHA):
        assert _hits(eng, line) == [], line


def test_loose_source_forms_flag_absolute_dotdot_and_rewritten_shapes(eng):
    assert eng.loose_source_forms(
        "See /abs/.specify/specs/%s/plan.md" % ALPHA, SLUGS) == [
        ".specify/specs/%s" % ALPHA]
    assert eng.loose_source_forms("See ../%s/plan.md" % ALPHA, SLUGS) == [
        "../%s" % ALPHA]
    assert eng.loose_source_forms(
        "Archived .specify/specs/%s/slices/%s/plan.md" % (PARENT, ALPHA),
        SLUGS) == [], "the archived path is not a source-path form"


def test_loose_source_hits_carry_the_slice_they_attribute_to(eng):
    hits = eng.loose_source_hits(
        "See /abs/.specify/specs/%s/plan.md and ../%s/tasks.md" % (ALPHA, BETA),
        SLUGS)
    assert [(hit["slug"], hit["form"]) for hit in hits] == [
        (ALPHA, ".specify/specs/%s" % ALPHA), (BETA, "../%s" % BETA)]
    assert eng.loose_source_hits(
        "Archived .specify/specs/%s/slices/%s/plan.md" % (PARENT, ALPHA),
        SLUGS) == [], "the archived path is not a source-path form"


def test_carrier_kind_uses_the_closed_roster(eng):
    assert eng.archive_carrier_kind(PARENT_REL + "/plan.md", PARENT, SLUGS) == "live"
    assert eng.archive_carrier_kind(PARENT_REL + "/contracts/core.md", PARENT,
                                    SLUGS) == "live"
    assert eng.archive_carrier_kind(PARENT_REL + "/notes/note.md", PARENT,
                                    SLUGS) == "dated"
    assert eng.archive_carrier_kind(PARENT_REL + "/test-evidence/x.txt", PARENT,
                                    SLUGS) == "dated"
    assert eng.archive_carrier_kind(PARENT_REL + "/checklists/x.md", PARENT,
                                    SLUGS) == "dated"
    assert eng.archive_carrier_kind(PARENT_REL + "/merge-manifest.json", PARENT,
                                    SLUGS) == "merge-json"
    assert eng.archive_carrier_kind(PARENT_REL + "/seal.md", PARENT,
                                    SLUGS) == "excluded"
    assert eng.archive_carrier_kind(PARENT_REL + "/archive-manifest.json", PARENT,
                                    SLUGS) == "excluded"
    assert eng.archive_carrier_kind(PARENT_REL + "/unsorted/random.md", PARENT,
                                    SLUGS) == "unclassified"
    assert eng.archive_carrier_kind(".specify/specs/%s/notes.md" % ALPHA, PARENT,
                                    SLUGS) == "dated"
    assert eng.archive_carrier_kind(".specify/register.md", PARENT, SLUGS) == "live"
    assert eng.archive_carrier_kind(".specify/features.md", PARENT, SLUGS) == "dated"
    assert eng.archive_carrier_kind(
        ".specify/features/100-fixture-parent.md", PARENT, SLUGS) == "mixed"
    assert eng.archive_carrier_kind(".specify/memory/session/e.md", PARENT,
                                    SLUGS) == "dated"
    assert eng.archive_carrier_kind(".specify/history/t.md", PARENT, SLUGS) == "dated"
    assert eng.archive_carrier_kind("shared/definitions/x.md", PARENT, SLUGS) == "live"
    assert eng.archive_carrier_kind(".specify/shared/definitions/x.md", PARENT,
                                    SLUGS) == "live"
    assert eng.archive_carrier_kind("tests/contract/test_x.py", PARENT,
                                    SLUGS) == "live"


def test_mixed_carrier_uses_the_h2_section_predicate(eng):
    text = (
        "# Feature\n\n"
        "## Latest Review\n\n"
        "dated line\n\n"
        "## Related Specifications/Requirements\n\n"
        "live line\n\n"
        "## Key Changes\n\n"
        "dated again\n"
    )
    lines = text.splitlines()
    assert eng.mixed_section_kind(lines, 5) == "dated"
    assert eng.mixed_section_kind(lines, 9) == "live"
    assert eng.mixed_section_kind(lines, 13) == "dated"
    assert eng.mixed_section_kind(lines, 1) == "dated", (
        "C-304: everything outside the named H2 section is dated"
    )
