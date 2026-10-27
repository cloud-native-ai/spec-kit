"""Contract test: the composed `/speckit.review` surface (Feature 071).

Pins `contracts/command-orchestration.md` C-1…C-16 against the two source
templates it governs — `templates/commands/review.md` (the orchestration) and
`templates/review-template.md` (the report's code-segment subsection):

* C-1/C-2 — exactly two segments in a fixed order, no selector parameter, no
  third mode and no merged severity vocabulary.
* C-3/C-4 — the process segment is unconditional; both segments are delegated by
  runtime path and neither skill's methodology is inlined.
* C-5 — failure propagation, including the command-authored minimal report that
  is written when the process skill aborted before `review.md` existed.
* C-6/C-7 — the three applicability values, each with its mandatory basis or
  reason; the code-path predicate cited from its single script owner; the
  empty-delta-first rule.
* C-8 — the review object is the committed delta; uncommitted scope is excluded
  and disclosed.
* C-9/C-10 — the report's `### 2.1` subsection and its closed content list, with
  no opinion bodies and no per-item counts copied.
* C-11/C-12 — two artifacts that never overwrite each other, record existence
  tied to the triage value, and the rotation with its timestamp form.
* C-13/C-14 — the two verifiable carriers, the closing summary demoted to
  presentation, and the record's exclusion from downstream document lists.
* C-15/C-16 — the code finding's locating form, and the untouched non-segment
  surfaces (frontmatter `scripts:`, the compiled `## Wrap-up` face, `## Handoffs`).

Red before the composition lands (Tests Mode = ON, Constitution Principle IV): at
the time this file was written, `templates/commands/review.md` declared one
delegation (`review-sdd-process`) and no triage at all, and
`templates/review-template.md` had no `### 2.1` subsection.

What this file deliberately does NOT pin: the base-resolution tiers, the receipt
grammar, the renderer-selection rule and the gate criteria. Those have their own
owners and their own contract groups; a second copy here would be the drift this
feature exists to prevent.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
REVIEW_CMD = ROOT / "templates" / "commands" / "review.md"
REVIEW_TEMPLATE = ROOT / "templates" / "review-template.md"

#: The six-level code vocabulary, owned by `skills/internal/code-review/SKILL.md`.
#: Referenced here only to detect an enumeration that was inlined into the command
#: template (C-4) or copied into the report subsection (C-10) — never to define it.
CODE_SEVERITIES = ("blocking", "important", "suggestion", "nitpick", "question", "praise")
PROCESS_SEVERITIES = ("P0", "P1", "P2")

#: The frontmatter prerequisite block as published (C-16: unchanged by this feature).
PUBLISHED_SCRIPTS_LINE = (
    "  sh: scripts/bash/check-prerequisites.sh --json --require-spec "
    "--include-spec --include-plan --include-tasks"
)


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #

def _flat(text: str) -> str:
    """Collapse whitespace so a phrase can be asserted across a line wrap."""
    return re.sub(r"\s+", " ", text)


def _has(text: str, phrase: str) -> bool:
    return phrase.lower() in _flat(text).lower()


def _sentences(text: str) -> list:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", _flat(text)) if s.strip()]


def _sentences_with(text: str, token: str) -> list:
    return [s for s in _sentences(text) if token.lower() in s.lower()]


def _section(text: str, start: str, end: str) -> str:
    m = re.search(rf"(?ms)^{re.escape(start)}.*?(?=^{re.escape(end)})", text)
    assert m, f"section {start!r} not found (or no {end!r} after it)"
    return m.group(0)


def _severity_hits(line: str) -> list:
    """Code-vocabulary literals in one line.

    The lookarounds keep the hyphenated gate literal `blocking-unresolved` from
    being read as a `blocking` severity heading — one is a refusal code, the other
    is an opinion level, and conflating them is exactly the merged-vocabulary bug
    C-2 forbids.
    """
    return [
        s
        for s in CODE_SEVERITIES
        if re.search(rf"(?<![\w-]){s}(?![\w-])", line, re.IGNORECASE)
    ]


def _cmd() -> str:
    return REVIEW_CMD.read_text(encoding="utf-8")


def _report_subsection() -> str:
    return _section(REVIEW_TEMPLATE.read_text(encoding="utf-8"), "### 2.1", "## ")


# --------------------------------------------------------------------------- #
# C-1 / C-2 — two segments, one order, two vocabularies
# --------------------------------------------------------------------------- #

def test_c01_exactly_two_segments_in_a_fixed_order():
    body = _cmd()
    assert _has(body, "exactly two segments"), (
        "the template MUST declare the composition as exactly two segments"
    )
    assert _has(body, "fixed order"), "the order MUST be stated as fixed"

    markers = re.findall(
        r"(?m)^### Segment (\d+) — (process segment|code segment)\b", body
    )
    assert markers == [("1", "process segment"), ("2", "code segment")], (
        "the template MUST declare exactly two segments — process first, code "
        f"second — and declare no third; found {markers!r}"
    )


def test_c01_no_parameter_selects_one_segment_over_the_other():
    body = _cmd()
    assert _has(body, "no parallel mode"), "a parallel mode MUST be excluded"
    assert _has(body, "no single merged report"), "a merged report MUST be excluded"
    for selector in (
        "--segment",
        "--process-only",
        "--code-only",
        "--skip-process",
        "--no-code",
        "review_mode",
    ):
        assert selector not in body, f"{selector!r} would create a segment selector"


def test_c02_the_two_severity_vocabularies_are_never_merged():
    body = _cmd()
    assert _has(body, "never merged"), (
        "the template MUST state that the two conclusions are never merged"
    )
    for line in body.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        process = [s for s in PROCESS_SEVERITIES if re.search(rf"\b{s}\b", line)]
        code = _severity_hits(line)
        assert not (process and code), (
            "no table row may pair a process severity with a code severity — that "
            f"row would be a mapping table (C-2): {line!r}"
        )


# --------------------------------------------------------------------------- #
# C-3 / C-4 — the process segment runs always; delegation, not inlining
# --------------------------------------------------------------------------- #

def test_c03_process_segment_runs_on_every_invocation():
    body = _cmd()
    assert _has(body, "every invocation"), (
        "the template MUST state that the process segment runs on every invocation"
    )
    exempt = " ".join(_sentences_with(body, "exempt"))
    assert exempt, "the template MUST state that the process segment cannot be exempted"
    for source in ("class", "$ARGUMENTS", "code delta"):
        assert source in exempt, (
            "the no-exemption rule MUST name the exemption it forbids; "
            f"{source!r} is missing from: {exempt!r}"
        )


def test_c04_both_segments_are_delegated_by_named_runtime_path():
    body = _cmd()
    assert ".specify/skills/internal/review-sdd-process/SKILL.md" in body, (
        "the process segment MUST be delegated by its runtime path"
    )
    assert ".specify/skills/internal/code-review/SKILL.md" in body, (
        "the code segment MUST be delegated by its runtime path"
    )
    assert body.count(".specify/skills/internal/") >= 2


def test_c04_no_skill_methodology_is_inlined():
    body = _cmd()
    for line in body.splitlines():
        assert len(_severity_hits(line)) < 3, (
            "the command template MUST NOT inline a code-review severity "
            f"enumeration (C-4): {line!r}"
        )
    distinct = {s for s in CODE_SEVERITIES if _severity_hits(body) and s in _severity_hits(body)}
    assert len(distinct) <= 3, (
        "the command template may name at most a mention of the code vocabulary, "
        f"never enumerate it; found {sorted(distinct)!r}"
    )
    for receipt_field in (
        "receipt_version",
        "changed_files",
        "judged_files",
        "skipped_files",
        "gap_files",
        "file.<NN>.path",
    ):
        assert receipt_field not in body, (
            "the receipt's field list belongs to the skill's script; the command "
            f"template MUST NOT carry it ({receipt_field!r})"
        )
    for dimension in ("cargo-cult", "friction:", "ambiguity/contradiction"):
        assert dimension not in body.lower(), (
            f"the process skill's dimension list MUST NOT be inlined ({dimension!r})"
        )


# --------------------------------------------------------------------------- #
# C-5 — failure propagation
# --------------------------------------------------------------------------- #

def test_c05_process_abort_does_not_suppress_the_code_segment():
    failure = _section(_cmd(), "## Failure propagation", "## ")
    assert _has(failure, "does not suppress the code segment"), (
        "the code segment's preconditions MUST NOT include the process segment's success"
    )
    assert _has(failure, "not-evaluated"), (
        "an aborted process segment MUST be recorded as `not-evaluated`"
    )
    assert _has(failure, "reason"), "that record MUST carry its reason"
    assert _has(failure, "not presented as a completed review"), (
        "the run MUST NOT be presented as a completed review"
    )


def test_c05_the_command_authors_a_minimal_report_when_none_exists():
    failure = _section(_cmd(), "## Failure propagation", "## ")
    assert _has(failure, "minimal process report"), (
        "an abort before `review.md` exists MUST make the command author a minimal report"
    )
    assert "### 2.1" in failure, (
        "the minimal report carries only the code-segment subsection"
    )
    assert _has(failure, "templates/review-template.md"), (
        "the minimal report MUST be authored from the report template"
    )
    assert _has(failure, "abort reason")


# --------------------------------------------------------------------------- #
# C-6 / C-7 — applicability triage
# --------------------------------------------------------------------------- #

def test_c06_triage_is_a_closed_three_value_set():
    triage = _section(_cmd(), "## Applicability triage", "## ")
    rows = [l for l in triage.splitlines() if l.lstrip().startswith("|")]
    value_rows = [
        r for r in rows if re.search(r"`(run|not-applicable|not-evaluated)`", r)
    ]
    assert len(value_rows) == 3, (
        "the triage MUST be presented as exactly three values; "
        f"found {len(value_rows)} row(s): {value_rows!r}"
    )
    assert _has(triage, "no fourth state"), (
        "an unspecified, empty or silently skipped value MUST be declared a violation"
    )
    assert _has(triage, "before the code segment starts"), (
        "the triage MUST resolve before the code segment starts"
    )


def test_c06_not_applicable_needs_a_basis_and_not_evaluated_a_reason():
    triage = _section(_cmd(), "## Applicability triage", "## ")
    rows = [l for l in triage.splitlines() if l.lstrip().startswith("|")]
    na = next(r for r in rows if "`not-applicable`" in r)
    ne = next(r for r in rows if "`not-evaluated`" in r)
    assert "basis" in na.lower(), (
        "the bare `not-applicable` literal without a basis does not satisfy C-7"
    )
    assert "reason" in ne.lower(), (
        "the bare `not-evaluated` literal without a reason does not satisfy C-6"
    )


def test_c07_the_code_path_predicate_has_exactly_one_owner():
    body = _cmd()
    assert "skills/internal/code-review/scripts/git-delta-review.sh" in body, (
        "the template MUST cite the predicate's owner by path"
    )
    assert "--code-paths" in body, (
        "the owner's explicit override MUST be named, so nobody re-derives the set"
    )
    assert _has(body, "no second path list"), (
        "the template MUST state why it carries no list of its own"
    )
    for glob in (
        "*.py", "*.js", "*.ts", "*.tsx", "*.go", "*.rs", "*.java",
        "*.rb", "*.sh", "*.c", "*.cpp", "*.swift", "*.kt",
    ):
        assert glob not in body, (
            f"a second code-path list would drift from its owner ({glob!r})"
        )


def test_c07_an_empty_delta_is_triaged_before_the_receipt_runs():
    body = _cmd()
    empty = " ".join(_sentences_with(body, "empty"))
    assert empty, "the template MUST carry the empty-delta rule"
    assert "not-applicable" in empty, "an empty delta MUST be `not-applicable`"
    assert "before" in empty.lower(), (
        "the triage MUST happen before the coverage receipt runs"
    )
    assert "no committed code delta" in empty, "the basis literal is mandatory"


# --------------------------------------------------------------------------- #
# C-8 — the review object
# --------------------------------------------------------------------------- #

def test_c08_review_object_is_the_committed_delta():
    body = _cmd()
    assert "base..head" in body, "the reviewed range MUST be recorded as `base..head`"
    assert _has(body, "committed code delta"), (
        "the object MUST be this feature slice's committed code delta"
    )
    assert _has(body, "git diff base..head"), (
        "the range MUST be recomputable from the report alone"
    )


def test_c08_uncommitted_changes_are_excluded_and_disclosed():
    body = _cmd()
    sentences = " ".join(_sentences_with(body, "uncommitted"))
    assert sentences, "the template MUST say what happens to uncommitted changes"
    low = sentences.lower()
    assert "not part of that object" in low or "not counted" in low, (
        "working-tree changes MUST be excluded from the default object"
    )
    assert "disclos" in low, (
        "when they exist the unreviewed scope MUST be disclosed"
    )


# --------------------------------------------------------------------------- #
# C-11 / C-12 — two artifacts, record existence, rotation
# --------------------------------------------------------------------------- #

def test_c11_two_artifacts_that_never_overwrite_each_other():
    body = _cmd()
    assert "review.md" in body and "code-review.md" in body, (
        "both artifacts MUST be named"
    )
    assert _has(body, "neither file overwrites the other"), (
        "the two artifacts MUST NOT overwrite each other"
    )
    assert _has(body, "never share one severity summary table"), (
        "the two artifacts MUST NOT share one severity summary table"
    )


def test_c11_record_existence_follows_the_triage_value():
    body = _cmd()
    assert _has(body, "only `run` writes `code-review.md`"), (
        "only the `run` triage value writes a record"
    )
    assert _has(body, "not even an empty one"), (
        "`not-applicable` and `not-evaluated` MUST create no record file at all"
    )
    assert _has(body, "record existence"), (
        "the rule MUST be stated as a rule, not implied by an example"
    )


def test_c12_rotation_uses_the_utc_second_timestamp_form():
    body = _cmd()
    assert "code-review-<YYYYMMDDTHHMMSSZ>.md" in body, (
        "the archive name form MUST be the literal one, not a description of it"
    )
    assert _has(body, "second resolution"), "the timestamp is UTC, second resolution"
    assert _has(body, "exit `2`"), (
        "a same-second collision waits or exits `2`; it never overwrites"
    )
    assert _has(body, "`none` on a first run"), (
        "a first run records `none` rather than an empty field"
    )
    assert _has(body, "never overwritten"), (
        "an existing archive path MUST NOT be overwritten"
    )


# --------------------------------------------------------------------------- #
# C-13 / C-14 — carriers and placement
# --------------------------------------------------------------------------- #

def test_c13_the_record_is_reachable_from_the_feature_side():
    body = _cmd()
    assert "## Latest Review" in body, (
        "the record MUST be referenced from the feature detail's `## Latest Review` entry"
    )
    assert "AVAILABLE_DOCS" in body, (
        "the record's exclusion from downstream available-documents lists MUST be stated"
    )
    assert _has(body, "no new structured field"), (
        "that existing entry is the carrier; no new field is added"
    )
    assert _has(body, "not read as plan or tasks input")


def test_c14_two_verifiable_carriers_and_a_presentational_closing_summary():
    body = _cmd()
    assert _has(body, "two verifiable carriers"), (
        "the conclusions land on exactly two verifiable carriers"
    )
    assert _has(body, "not a third verifiable carrier"), (
        "the closing summary MUST NOT be promoted to a carrier"
    )
    assert _has(body, "it is a presentation"), (
        "the closing summary is a presentation, not an artifact"
    )
    assert _has(body, "the carriers govern"), (
        "on disagreement, the carriers govern — that is what makes the demotion real"
    )


# --------------------------------------------------------------------------- #
# C-15 / C-16 — finding form and untouched surfaces
# --------------------------------------------------------------------------- #

def test_c15_a_code_finding_keeps_severity_plus_location():
    body = _cmd()
    assert _has(body, "severity plus file and optional line"), (
        "a code finding's locating form is severity plus file and optional line"
    )
    assert _has(body, "never coined as a `REC-"), (
        "a code finding MUST NOT be coined as a `REC-…` identifier"
    )


def test_c16_frontmatter_scripts_block_is_unchanged():
    body = _cmd()
    assert PUBLISHED_SCRIPTS_LINE in body, (
        "the frontmatter `scripts:` prerequisite block stays as published"
    )


def test_c16_the_compiled_wrap_up_face_is_untouched():
    body = _cmd()
    wrap = _section(body, "## Wrap-up", "## ")
    assert "AUTO-GENERATED by probe-utils.py --action compile-embeds" in wrap, (
        "the compiled face keeps its compilation marker"
    )
    steps = re.findall(r"(?m)^\d+\. ", wrap)
    assert len(steps) == 6, (
        "the compiled `## Wrap-up` face keeps its six steps; found "
        f"{len(steps)}: {steps!r}"
    )


def test_c16_handoffs_keeps_its_registration_obligation():
    body = _cmd()
    handoffs = body.split("\n## Handoffs", 1)[1]
    assert "register.md" in handoffs, "the handoff MUST name the register"
    assert "same commit" in handoffs, "registration stays in the same commit"
    assert "REC-" in handoffs, "the handoff names the identifier family it registers"


def test_c16_user_input_section_survives():
    body = _cmd()
    user_input = _section(body, "## User Input", "## ")
    assert "$ARGUMENTS" in user_input
    assert "shared/workflow/user-input-protocol.md" in user_input


# --------------------------------------------------------------------------- #
# C-9 / C-10 — the report's code-segment subsection
# --------------------------------------------------------------------------- #

def test_c09_the_report_carries_a_code_segment_subsection():
    subsection = _report_subsection()
    assert subsection.strip(), "`templates/review-template.md` MUST carry `### 2.1`"


def test_c09_subsection_content_list_is_closed():
    subsection = _report_subsection()
    required = {
        "base commit id": "base",
        "head commit id": "head",
        "base source": "base source",
        "renderer mode": "renderer",
        "changed count": "changed",
        "judged count": "judged",
        "skipped count": "skipped",
        "gap count": "gap",
        "segment verdict": "segment verdict",
        "gate verdict": "gate verdict",
        "gate refusal literal": "blocking-unresolved",
        "not-applicable / not-evaluated reason": "not-evaluated",
        "uncommitted-scope disclosure": "uncommitted",
        "record path": "record",
        "archive path": "archive",
    }
    missing = [name for name, token in required.items() if not _has(subsection, token)]
    assert not missing, f"the subsection's closed content list is missing: {missing!r}"


def test_c09_the_four_counts_are_copied_from_the_receipt_block():
    subsection = _report_subsection()
    assert _has(subsection, "receipt block"), (
        "the receipt block MUST be named as the source of the four counts"
    )
    assert _has(subsection, "never recomputed"), (
        "the subsection MUST NOT recompute, re-aggregate or derive the counts"
    )
    assert _has(subsection, "copied"), "the counts are copied field by field"


def test_c10_no_opinion_bodies_and_no_per_item_counts_are_copied():
    subsection = _report_subsection()
    assert _severity_hits(subsection) == [], (
        "the subsection copies no opinion bodies; a code severity literal here "
        "means opinions moved in (C-10)"
    )
    assert _has(subsection, "no opinion body"), (
        "the exclusion MUST be stated, not merely respected"
    )
    assert _has(subsection, "no per-severity item count"), (
        "a per-item count list is exactly what the subsection must not carry"
    )


def test_c05_the_subsection_is_fillable_as_the_whole_minimal_report():
    subsection = _report_subsection()
    for foreign in ("F[N]", "### F", "§ 3", "§ 5", "Section 3", "[QUOTED_EXCERPT"):
        assert foreign not in subsection, (
            "the subsection must be fillable with no other section present "
            f"(a process-segment abort produces exactly this); found {foreign!r}"
        )
    assert _has(subsection, "whole report") or _has(subsection, "nothing else present"), (
        "the subsection MUST state that it is fillable alone"
    )


def test_c09_every_placeholder_in_the_subsection_is_glossed():
    body = REVIEW_TEMPLATE.read_text(encoding="utf-8")
    subsection = _report_subsection()
    used = sorted(set(re.findall(r"\[([A-Z][A-Z0-9_]+)\]", subsection)))
    assert used, "the subsection MUST use placeholder tokens rather than prose values"
    glossary = body[body.index("## Placeholder Glossary"):]
    missing = [t for t in used if t not in glossary]
    assert not missing, (
        f"placeholder tokens used in `### 2.1` but absent from the glossary: {missing!r}"
    )


def test_c09_existing_top_level_section_numbers_are_stable():
    body = REVIEW_TEMPLATE.read_text(encoding="utf-8")
    numbers = re.findall(r"(?m)^## (\d+)\. ", body)
    assert numbers == [str(i) for i in range(9)], (
        "the subsection lands under § 2 so every existing top-level number stays "
        f"put; found {numbers!r}"
    )
