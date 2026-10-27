"""Contract test: documentation ↔ template isomorphism for `/speckit.review` (Feature 071).

Pins `contracts/tests-and-docs-sync.md` C-71 (and C-68's documentation-sync
surface): the command reference page `docs/reference/commands/review.md` declares
the same surface as `templates/commands/review.md`.

**What "the same surface" means here** — the four things a reader must be able to
learn from either file, and nothing about prose:

1. the two segments (`process segment` / `code segment`, each accepted under one
   documented spelling variant so a cosmetic reword does not red this file),
2. the two artifacts (`review.md` / `code-review.md`),
3. the three applicability values (`run` / `not-applicable` / `not-evaluated` —
   these are shared string literals, so they are compared exactly),
4. the two severity vocabularies (`P0`/`P1`/`P2` and the code skill's six levels),
   declared on both sides and never paired into a mapping.

The comparison is set-based: a **deleted** segment, artifact or value reds it
because the set difference is non-empty; a reworded sentence does not, because
prose is never compared. `test_the_comparison_tolerates_a_cosmetic_reword` proves
that non-brittleness rather than asserting it.

Red by construction while the page still describes a process-only review: FR-028
puts the page in the same change as the template (C-68), and this group stays red
until the documentation row lands.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
DOCS_PAGE = ROOT / "docs" / "reference" / "commands" / "review.md"
COMMAND_TEMPLATE = ROOT / "templates" / "commands" / "review.md"

#: Concept → the spellings either side MAY use. A concept counts as declared when
#: any one spelling is present, so re-wording is tolerated and deletion is not.
SEGMENTS = {
    "process segment": ("process segment", "process review segment", "process review pass"),
    "code segment": ("code segment", "code-review segment", "code review segment"),
}

#: Shared string literals: compared exactly, on both sides (requirements.md STR-004/005/001/002).
ARTIFACTS = ("review.md", "code-review.md")
APPLICABILITY_VALUES = ("run", "not-applicable", "not-evaluated")

#: The process vocabulary is `P0`/`P1`/`P2`; the code vocabulary is the six-level
#: set owned by `skills/internal/code-review/SKILL.md`. Both sides must declare each
#: family, and at least two of the six code levels are enough — the endpoints carry
#: the family, and a page is free to list all six.
PROCESS_SEVERITIES = ("P0", "P1", "P2")
CODE_SEVERITIES = ("blocking", "important", "suggestion", "nitpick", "question", "praise")


# --------------------------------------------------------------------------- #
# declared-surface extraction
# --------------------------------------------------------------------------- #

def _flat(text: str) -> str:
    return re.sub(r"\s+", " ", text).lower()


def _declared_segments(text: str) -> set:
    flat = _flat(text)
    return {name for name, spellings in SEGMENTS.items() if any(s in flat for s in spellings)}


def _declared_artifacts(text: str) -> set:
    return {a for a in ARTIFACTS if a in text}


def _declared_applicability(text: str) -> set:
    # Backticks are the canonical declaration form; a bare word is ambiguous
    # ("run" is an English verb), so only the marked form counts as declared.
    return {v for v in APPLICABILITY_VALUES if f"`{v}`" in text}


def _declared_code_severities(text: str) -> set:
    return {
        s for s in CODE_SEVERITIES if re.search(rf"(?<![\w-]){s}(?![\w-])", text, re.IGNORECASE)
    }


def _declared_process_severities(text: str) -> set:
    return {s for s in PROCESS_SEVERITIES if re.search(rf"\b{s}\b", text)}


def declared_surface(text: str) -> dict:
    return {
        "segments": _declared_segments(text),
        "artifacts": _declared_artifacts(text),
        "applicability": _declared_applicability(text),
        "process_severities": _declared_process_severities(text),
        "code_severities": _declared_code_severities(text),
    }


def _mapping_rows(text: str) -> list:
    """Lines that pair a process severity with a code severity.

    Such a line is a mapping table row (or its prose equivalent) — the one thing
    C-2 forbids both files to declare, because a mapping collapses the two
    vocabularies into the single severity system this feature keeps apart.
    """
    offenders = []
    for line in text.splitlines():
        process = [s for s in PROCESS_SEVERITIES if re.search(rf"\b{s}\b", line)]
        code = [
            s
            for s in CODE_SEVERITIES
            if re.search(rf"(?<![\w-]){s}(?![\w-])", line, re.IGNORECASE)
        ]
        if process and code:
            offenders.append(line.strip())
    return offenders


# --------------------------------------------------------------------------- #
# the isomorphism, one axis per test so a red run says which axis broke
# --------------------------------------------------------------------------- #

def test_the_two_segments_are_declared_on_both_sides():
    template = COMMAND_TEMPLATE.read_text(encoding="utf-8")
    page = DOCS_PAGE.read_text(encoding="utf-8")
    missing_from_template = set(SEGMENTS) - _declared_segments(template)
    missing_from_page = set(SEGMENTS) - _declared_segments(page)
    assert not missing_from_template, (
        f"the command template does not declare: {sorted(missing_from_template)!r}"
    )
    assert not missing_from_page, (
        "the documentation page still describes a process-only review; it does not "
        f"declare: {sorted(missing_from_page)!r} (C-68, C-71)"
    )


def test_the_two_artifacts_are_declared_on_both_sides():
    template = COMMAND_TEMPLATE.read_text(encoding="utf-8")
    page = DOCS_PAGE.read_text(encoding="utf-8")
    assert set(ARTIFACTS) - _declared_artifacts(template) == set(), (
        "the command template MUST name both artifacts"
    )
    assert set(ARTIFACTS) - _declared_artifacts(page) == set(), (
        "the documentation page MUST name both artifacts; missing: "
        f"{sorted(set(ARTIFACTS) - _declared_artifacts(page))!r}"
    )


def test_the_three_applicability_values_are_declared_on_both_sides():
    template = COMMAND_TEMPLATE.read_text(encoding="utf-8")
    page = DOCS_PAGE.read_text(encoding="utf-8")
    assert set(APPLICABILITY_VALUES) - _declared_applicability(template) == set(), (
        "the command template MUST declare the closed three-value triage"
    )
    assert set(APPLICABILITY_VALUES) - _declared_applicability(page) == set(), (
        "the documentation page MUST declare the closed three-value triage; missing: "
        f"{sorted(set(APPLICABILITY_VALUES) - _declared_applicability(page))!r}"
    )


def test_the_process_severity_family_is_declared_on_both_sides():
    for path in (COMMAND_TEMPLATE, DOCS_PAGE):
        text = path.read_text(encoding="utf-8")
        missing = set(PROCESS_SEVERITIES) - _declared_process_severities(text)
        assert not missing, (
            f"{path.relative_to(ROOT)} does not declare the process vocabulary: "
            f"{sorted(missing)!r}"
        )


def test_the_code_severity_family_is_declared_on_both_sides():
    for path in (COMMAND_TEMPLATE, DOCS_PAGE):
        text = path.read_text(encoding="utf-8")
        declared = _declared_code_severities(text)
        assert len(declared) >= 2, (
            f"{path.relative_to(ROOT)} does not declare the code severity family "
            f"(at least its endpoints); found {sorted(declared)!r}"
        )


def test_neither_side_maps_one_vocabulary_onto_the_other():
    for path in (COMMAND_TEMPLATE, DOCS_PAGE):
        offenders = _mapping_rows(path.read_text(encoding="utf-8"))
        assert not offenders, (
            f"{path.relative_to(ROOT)} pairs the two vocabularies, which is a mapping "
            f"(C-2): {offenders!r}"
        )


def test_the_declared_surfaces_are_equal():
    template = declared_surface(COMMAND_TEMPLATE.read_text(encoding="utf-8"))
    page = declared_surface(DOCS_PAGE.read_text(encoding="utf-8"))
    differing = {k: (template[k], page[k]) for k in template if template[k] != page[k]}
    assert not differing, (
        "the page and the template MUST declare the same surface "
        f"(template, page): {differing!r}"
    )


# --------------------------------------------------------------------------- #
# the comparison itself: a reword must survive, a deletion must not
# --------------------------------------------------------------------------- #

def test_the_comparison_tolerates_a_cosmetic_reword():
    page = DOCS_PAGE.read_text(encoding="utf-8")
    reworded = page.replace("process segment", "process review pass")
    reworded = reworded.replace("code segment", "code-review segment")
    reworded = reworded.replace("## Execution Flow", "## Execution sequence")
    assert declared_surface(reworded) == declared_surface(page), (
        "a reworded sentence MUST NOT change the declared surface — otherwise this "
        "group reds for cosmetics and stops being a signal"
    )


def test_the_comparison_detects_a_deleted_segment():
    page = DOCS_PAGE.read_text(encoding="utf-8")
    # Start from a page that *does* declare both segments (the post-C-68 shape),
    # then delete one — the extractor has to notice.
    updated = page + "\n## Segments\n\nThe process segment runs first; the code segment runs second.\n"
    assert _declared_segments(updated) == set(SEGMENTS)
    gutted = re.sub(r"(?i)code[ -]review segment|code segment", "", updated)
    assert _declared_segments(gutted) == {"process segment"}, (
        "removing a segment from the page MUST change the declared surface; a group "
        "that stays green here would not be coverage (C-65)"
    )
