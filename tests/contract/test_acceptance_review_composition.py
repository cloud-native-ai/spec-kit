"""Contract tests for ``contracts/review-composition.contract.md`` — RC-01…RC-19 (Feature 081, slice 081c, T004).

This is slice **081c**'s single test carrier (``plan.md`` § D10 names it), and the module
``plan.md`` § Inherited Blockers IB-004's carrier resolves to. Its subject is the **post-rewrite**
tree: four review segments in one fixed order plus one deterministic check that is not a segment,
the expected-artifact denominator the artifact segment is measured on, the Acceptance Reality
Check's copied seven-key record, the three report slots, the four-unit feedback census, the review
call site actually running, and the process skill's single judgment object.

=====  ==========================================================================================
leg    what it pins
=====  ==========================================================================================
(a)    ``templates/commands/review.md`` carries four ``### Segment <n> — …`` markers in the order
       process → artifact → implementation → code, each naming its own skill and its own carrier
       anchor (§ Segment A / § Segment B); the Acceptance Reality Check section exists, calls
       itself **not** a segment and delegates to nobody; the pre-change wording ``exactly two
       segments`` survives nowhere in the framework's markdown (RC-01, RC-02, RC-03, RC-16)
(b)    each of the four segments is described by the **same five fields** — `Skill`, `Judgment
       object`, `Severity vocabulary`, `Inputs`, `Outputs` — exactly once each, every `Skill`
       value is a runtime path, and the runtime paths and the anchors they cite resolve on disk
       (RC-05, RC-10, RC-11)
(c)    the per-segment boundary sentences exist **once**, in the content owner, and the middle two
       segments reach them by path + anchor instead of restating them; no line pairs a process
       severity with a code severity and no score field exists; ``code-review`` is still present
       and declares itself the fourth segment (RC-04, RC-08, RC-12)
(d)    the artifact segment's denominator is the **expected** set derived from the slice's stage
       rules plus ``plan.md`` § Project Structure, referenced by anchor and restated nowhere; and
       the leg **applies** that derivation to ``expected-artifact-missing`` — expected minus
       present names ``quickstart.md``, the coverage line reads ``6 / 7`` (strictly below 100 %)
       with one finding for the absent member, while the competing "the ones that exist" reading
       makes the same fixture read ``6 / 6`` = 100 % with nothing reported (RC-06, FR-013)
(e)    the implementation segment judges this slice's ``base..head``, names
       ``skills/internal/code-review/scripts/git-delta-review.sh`` as its only base-resolution
       route, requires the smoke command / exit code / evidence-path triple, and is neither
       answered by the code segment nor by ``review-sdd-process`` (RC-07, RC-08, RC-09)
(f)    the Acceptance Reality Check **copies** rather than counts: the slot carries all seven
       ``final_path`` keys on one line, names the checker as the source and says never recomputed;
       the refusal path names the fixed item ``F-ACCEPTANCE`` at ``P0`` and leaves the claimed
       status unchanged; the refusal is driven on ``review-implemented-blocked``, not on
       ``negative``, which claims ``Planned`` and never reaches RC-15's conjunction (RC-13…RC-15)
(g)    ``templates/review-template.md`` carries ``### 2.2`` / ``### 2.3`` / ``### 2.4`` after an
       un-renumbered ``### 2.1``, and every placeholder used in them is in the Placeholder
       Glossary (RC-17)
(h)    the command's feedback boundary declares **four** units sharing one ``run_id``, suppresses
       no skill's wrap-up, and carries no ``three units`` wording (RC-18)
(i)    the call site is **wired, not named**: the invocation is extracted verbatim from the
       command template and run against four fixtures — ``negative`` (exit 1, reason inside the
       closed set), ``positive`` (exit 0), ``review-implemented-clean`` (exit 0, claimed
       ``Implemented``, all four completion conditions true) and ``review-implemented-blocked``
       (exit 1, ``zero-final-path-pass``) (GW-02, GW-04)
(j)    the finding locator is a **MUST** with exactly one escape — ``severity`` + artifact/diff
       path + ``line``, with ``line`` required whenever the artifact is line-addressable and an
       omission carrying a named reason; no carrier of the field set marks ``line`` optional
       (RC-06, FR-013)
(k)    ``skills/internal/review-sdd-process/SKILL.md`` carries **exactly one** countable
       ``- **Judgment object**:`` marker, and the two dimension headings
       ``## Segment A — Artifact Review`` / ``## Segment B — Implementation Review`` appear only
       under ``skills/internal/review-feature-quality/`` (RC-10, RC-12)
=====  ==========================================================================================

**Every leg asserts a verdict or an absence, never a bare string presence.** That is the whole
reason the module is worth its cost: a segment that *names* the expected set but falls back to "the
ones that exist", or an ARC slot that *lists* three buckets and calls it the record, is exactly the
false green FR-013 and FR-015 were declared to close. Where a leg's subject can be shown to
discriminate, the module shows it: (d) computes the competing reading on the same fixture and
asserts the two readings differ, (f) computes the ARC conjunction over two fixtures and asserts it
fires on one and cannot fire on the other, and (i) runs four fixtures through the documented
command. The two-part closed-set membership test belongs to
``tests/contract/test_closure_acceptance_check.py``; this module reuses the reason set's **owner**
(``requirements.md`` § Shared Strings) for a prefix-membership check only, and re-implements no
parser.

**Red-first (``tasks.md`` DoD-2).** This module is authored before the rows that fill its subject —
T005 (the carrier skill), T006 (the report slots) and T007 (the command rewrite) — so most legs are
red when it lands. The measured run — command, real console tail, exit status and failing count —
is recorded in ``.specify/specs/081-acceptance-hardening/notes/red-first-evidence-081c.md`` § T004;
nothing here claims a red that was not run, and no leg is written to pass against the current
two-segment template.

What this file deliberately does NOT pin: the closure checker's internals (its own contract group
owns them), the carrier skill's dimension lists and the report slots' content (T005/T006 own them,
and ``§ Segment A`` / ``§ Segment B`` are the anchors this file checks *resolve*), the code
segment's six-level family (``skills/internal/code-review/SKILL.md`` owns it), the base-resolution
tiers (``git-delta-review.sh`` owns them) and the two census pins' own modules
(``test_review_feedback_boundary.py`` / ``test_client_guard_sweep.py``, re-pinned by T009).
"""
from __future__ import annotations

import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]

REVIEW_CMD = ROOT / "templates" / "commands" / "review.md"
REVIEW_TEMPLATE = ROOT / "templates" / "review-template.md"
OWNER_DOC = ROOT / "shared" / "workflow" / "acceptance-hardening.md"

CARRIER_SRC_DIR = ROOT / "skills" / "internal" / "review-feature-quality"
CARRIER_RUNTIME = ROOT / ".specify" / "skills" / "internal" / "review-feature-quality" / "SKILL.md"
PROCESS_SKILL = ROOT / "skills" / "internal" / "review-sdd-process" / "SKILL.md"
CODE_SKILL = ROOT / "skills" / "internal" / "code-review" / "SKILL.md"

FIXTURES = ROOT / "tests" / "fixtures" / "acceptance-hardening"
REQUIREMENTS = ROOT / ".specify" / "specs" / "081-acceptance-hardening" / "requirements.md"

CHECKER_REL = "scripts/python/closure-acceptance-check.py"
CHECKER = ROOT / CHECKER_REL

#: The content owner's path, as the command template, the skills and this module must reach it.
OWNER_REL = "shared/workflow/acceptance-hardening.md"
OWNER_ANCHOR = "§ Review Composition"

#: The one base-resolution route (RC-09).
GIT_DELTA_REL = "skills/internal/code-review/scripts/git-delta-review.sh"

#: The four segments' skills, in the fixed order, with the carrier anchor each middle segment
#: must cite. `None` means "this segment has no carrier anchor of its own".
SEGMENT_PLAN = (
    ("1", "review-sdd-process", None),
    ("2", "review-feature-quality", "Segment A"),
    ("3", "review-feature-quality", "Segment B"),
    ("4", "code-review", None),
)

#: RC-05's five fields, as the marker each segment section must carry exactly once.
SEGMENT_FIELDS = (
    "Skill",
    "Judgment object",
    "Severity vocabulary",
    "Inputs",
    "Outputs",
)

#: The runtime path shape every `Skill` value must be (RC-05, RC-10).
SKILL_PATH = re.compile(r"\.specify/skills/internal/[a-z0-9-]+/SKILL\.md")

#: The three stable report slots, in slot order (RC-17).
REPORT_SLOTS = (
    "### 2.1",
    "### 2.2 Artifact Review Segment",
    "### 2.3 Implementation Review Segment",
    "### 2.4 Acceptance Reality Check",
)

#: The two slots that carry findings, by name (the `### 2.x` prefix is added for the heading).
FINDING_SLOTS = (
    "2.2 Artifact Review Segment",
    "2.3 Implementation Review Segment",
)

#: `final_path` is a closed count record — six status buckets plus the total (RC-14). A three-count
#: summary is a different shape and MUST fail leg (f).
FINAL_PATH_KEYS = ("pass", "blocked", "deferred", "partial", "fail", "unknown", "total")

#: The artifact segment's expected set — the derivation's product for this feature's stage (RC-06).
EXPECTED_MEMBERS = (
    "requirements.md",
    "plan.md",
    "tasks.md",
    "contracts/",
    "data-model.md",
    "quickstart.md",
    "verification.md",
)

#: The four units of one composed run, each with its own closing record (RC-18).
CENSUS_UNITS = (
    "/speckit.review",
    "skill:review-sdd-process",
    "skill:review-feature-quality",
    "skill:code-review",
)

#: The two dimension headings T005 lands; RC-10 puts them under the carrier and nowhere else.
SEGMENT_HEADINGS = (
    "## Segment A — Artifact Review",
    "## Segment B — Implementation Review",
)

#: The declaring ids of the closed reason set, in `## Shared Strings` table order.
REASON_IDS = ("STR-008", "STR-009", "STR-010", "STR-011", "STR-012", "STR-013", "STR-014")

#: The `completion_conditions` payload keys the clean case must satisfy 4/4 (FR-016's fourth
#: condition judged and passed, not skipped).
COMPLETION_CONDITIONS = (
    "every_final_path_pass",
    "no_open_rows",
    "smoke_record_pass",
    "status_row_per_criterion",
)

#: The six code severities, owned by `skills/internal/code-review/SKILL.md`. Referenced here only
#: to detect an enumeration that was inlined into a segment or merged with the process family.
CODE_SEVERITIES = ("blocking", "important", "suggestion", "nitpick", "question", "praise")
PROCESS_SEVERITIES = ("P0", "P1", "P2")


# --------------------------------------------------------------------------- #
# reading helpers — sections, phrases, fixtures
# --------------------------------------------------------------------------- #

def _read(path: Path) -> str:
    assert path.is_file(), "missing subject: %s" % path
    return path.read_text(encoding="utf-8")


def _flat(text: str) -> str:
    """Whitespace-collapsed, emphasis-stripped text — for phrases asserted across a line wrap."""
    return re.sub(r"\s+", " ", text.replace("*", "").replace("`", "")).strip()


def _has(text: str, phrase: str) -> bool:
    return phrase.lower() in _flat(text).lower()


def _sentences(text: str) -> list:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", _flat(text)) if s.strip()]


def _heading_section(text: str, pattern: str) -> str:
    """Body of the first heading matching ``pattern``, ending at the next same-or-higher heading."""
    match = re.search(rf"(?m)^(#{{1,6}})\s*(?:{pattern})\s*$", text)
    assert match, "no heading matching %r in the subject" % pattern
    tail = text[match.end():]
    stop = re.search(rf"(?m)^#{{1,{len(match.group(1))}}} ", tail)
    return tail[: stop.start()] if stop else tail


def _segment_sections() -> list:
    """``[(number, title, section_text)]`` for every ``### Segment <n> — …`` marker, in order."""
    body = _read(REVIEW_CMD)
    marks = list(re.finditer(r"(?m)^###\s+Segment\s+(\d+)\s*[—–-]\s*([^\n]+)$", body))
    out = []
    for mark in marks:
        tail = body[mark.end():]
        stop = re.search(r"(?m)^#{1,3} ", tail)
        out.append((mark.group(1), mark.group(2).strip(), tail[: stop.start()] if stop else tail))
    return out


def _segment(number: str) -> str:
    """The section of one segment position, rejecting a position that holds another segment.

    The skill check is not duplication of leg (a): it keeps every other leg's failure message
    honest. Without it, a two-segment template makes legs (c)/(d)/(e) report "the artifact segment
    does not do X" when the truth is "position 2 is still the code segment".
    """
    expected = {n: skill for n, skill, _anchor in SEGMENT_PLAN}
    for got, _title, section in _segment_sections():
        if got != number:
            continue
        line = _field_line(section, "Skill") or ""
        assert expected[number] in line, (
            "position %s is delegated to %r, not to %r — this leg's subject is the four-segment "
            "order (process → artifact → implementation → code), and it is not the tree's order "
            "yet (RC-01)" % (number, line.strip() or "<no Skill field>", expected[number])
        )
        return section
    known = [n for n, _t, _s in _segment_sections()]
    raise AssertionError(
        "templates/commands/review.md carries no `### Segment %s — …` section; the positions it "
        "does carry are %r, and this leg's subject is the post-rewrite four-segment order "
        "(RC-01)" % (number, known)
    )


def _field_line(section: str, field: str):
    lines = re.findall(rf"(?m)^\s*-\s*\*\*{re.escape(field)}\*\*:[^\n]*", section)
    return lines[0] if len(lines) == 1 else None


def _arc_section() -> str:
    """The Acceptance Reality Check section of the command template (RC-16 lives here)."""
    body = _read(REVIEW_CMD)
    marks = list(re.finditer(r"(?m)^(#{1,6})[^\n]*\bAcceptance Reality Check\b[^\n]*$", body))
    assert len(marks) == 1, (
        "templates/commands/review.md must carry exactly one heading for the Acceptance Reality "
        "Check; found %d — two headings leave the reader without one home for the check (RC-16)"
        % len(marks)
    )
    mark = marks[0]
    tail = body[mark.end():]
    stop = re.search(rf"(?m)^#{{1,{len(mark.group(1))}}} ", tail)
    return tail[: stop.start()] if stop else tail


def _md_files(*dirs: str) -> list:
    out = []
    for name in dirs:
        for path in (ROOT / name).rglob("*.md"):
            if ".venv" in path.parts:
                continue
            out.append(path)
    return sorted(out)


def _sweep(phrase: str, *dirs: str) -> list:
    """``[(repo-relative path, line number)]`` where ``phrase`` occurs in the framework markdown."""
    dirs = dirs or ("templates", "shared", "skills", "docs")
    hits = []
    for path in _md_files(*dirs):
        for lineno, line in enumerate(_read(path).splitlines(), 1):
            if phrase.lower() in _flat(line).lower():
                hits.append((path.relative_to(ROOT).as_posix(), lineno))
    return hits


def _severity_hits(line: str, family) -> list:
    return [s for s in family if re.search(rf"(?<![\w-]){s}(?![\w-])", line, re.IGNORECASE)]


def _fixture(name: str) -> Path:
    path = FIXTURES / name
    assert path.is_dir(), "fixture set %r is missing — T015/T016/T017 has not landed" % name
    return path


def _slot(name: str) -> str:
    """The body of one `### 2.x <name>` report slot."""
    return _heading_section(_read(REVIEW_TEMPLATE), re.escape(name))


# --------------------------------------------------------------------------- #
# (a) four segments, one fixed order, plus a check that is not a segment
# --------------------------------------------------------------------------- #

def test_a1_four_segments_in_the_fixed_order():
    """The order is content: process → artifact → implementation → code (RC-01, RC-02).

    Asserted through what each position *delegates to*, not through a title's wording: the
    middle two both hand off to the carrier skill, so the only thing distinguishing them is the
    carrier anchor they cite — ``§ Segment A`` (artifact) and ``§ Segment B`` (implementation).
    Swapping those two segments therefore fails this leg, which a title check would not catch.
    """
    segments = _segment_sections()
    assert [number for number, _t, _s in segments] == ["1", "2", "3", "4"], (
        "templates/commands/review.md must carry exactly the four `### Segment <n> — …` markers "
        "in one fixed order; found %r" % ([n for n, _t, _s in segments],)
    )
    for (number, _title, section), (_n, skill, anchor) in zip(segments, SEGMENT_PLAN):
        line = _field_line(section, "Skill")
        assert line is not None, (
            "segment %s must carry exactly one `- **Skill**:` row (RC-05)" % number
        )
        assert skill in line, (
            "segment %s must be delegated to %r, not to whatever %r names — the fixed order is "
            "the composition (RC-01)" % (number, skill, line.strip())
        )
        if anchor:
            assert anchor in section, (
                "segment %s must cite `§ %s` of the carrier skill — the two middle segments are "
                "told apart only by the anchor they point at (RC-10, RC-11)" % (number, anchor)
            )
            other = "Segment B" if anchor == "Segment A" else "Segment A"
            assert other not in section, (
                "segment %s cites `§ %s` as well as `§ %s`; one segment answers one question "
                "(RC-08)" % (number, other, anchor)
            )


def test_a2_the_acceptance_reality_check_is_present_and_is_not_a_segment():
    """ARC is a deterministic check, not a fifth entry in the order (RC-16)."""
    arc = _arc_section()
    assert re.search(r"(?i)\bnot\s+a(?:\s+fifth)?\s+segment\b", _flat(arc)), (
        "the Acceptance Reality Check section must say it is not a (fifth) segment — a check "
        "described as a segment becomes one the next time someone counts: %r" % arc[:400]
    )
    assert not re.search(r"(?m)^\s*-\s*\*\*Skill\*\*", arc), (
        "the Acceptance Reality Check carries a `Skill` field: it is delegated to a model "
        "judgement (RC-16): %r" % arc[:400]
    )
    assert ".specify/skills/" not in arc, (
        "the Acceptance Reality Check names a skill runtime path — it runs one deterministic "
        "program and delegates nothing (RC-16): %r" % arc[:400]
    )


def test_a3_the_two_segment_wording_survives_nowhere():
    """RC-03: the pre-change composition sentence MUST NOT survive anywhere in the tree.

    The sweep is `templates/`, `shared/`, `skills/` and `docs/` — the same four roots T007's own
    row declares. It therefore includes `docs/reference/commands/review.md`, which still carries
    the sentence at the time this module lands: RC-03 forbids the wording anywhere, so the docs
    page is inside the sweep rather than deferred with the CHANGELOG and instructions limbs
    (GW-14's other two limbs are 081d).
    """
    hits = _sweep("exactly two segments")
    assert not hits, (
        "the pre-change wording `exactly two segments` still lives at %r — the composition "
        "sentence must be rewritten in place, not shadowed by a second one (RC-03)" % (hits,)
    )


# --------------------------------------------------------------------------- #
# (b) five fields per segment, in the same order, resolving on disk
# --------------------------------------------------------------------------- #

def test_b1_each_segment_declares_the_same_five_fields_once_each():
    """RC-05: one field set, four times. A segment missing a field is not describable."""
    assert len(SEGMENT_FIELDS) == 5
    segments = _segment_sections()
    assert len(segments) == 4, (
        "the five-field rule is a rule about **four** segments; the template carries %d "
        "`### Segment <n> — …` markers (RC-01, RC-05)" % len(segments)
    )
    for number, _title, section in segments:
        for field in SEGMENT_FIELDS:
            count = len(re.findall(rf"(?m)^\s*-\s*\*\*{re.escape(field)}\*\*:", section))
            assert count == 1, (
                "segment %s declares `%s` %d times; every segment carries the same five fields "
                "exactly once (RC-05)" % (number, field, count)
            )


def test_b2_the_segment_skill_paths_and_their_anchors_resolve_on_disk():
    """RC-05/RC-10/RC-11: a runtime path is a claim until it resolves."""
    for number, _title, section in _segment_sections():
        line = _field_line(section, "Skill")
        assert line is not None, "segment %s carries no `Skill` row" % number
        match = SKILL_PATH.search(line)
        assert match, (
            "segment %s's `Skill` must be a runtime path of the form `.specify/skills/internal/"
            "<name>/SKILL.md` (its value reads %r) — a bare skill name is not runtime-reachable "
            "(RC-05, RC-10)" % (number, line.strip())
        )
        runtime = ROOT / match.group(0)
        source = ROOT / match.group(0).replace(".specify/", "", 1)
        assert runtime.is_file() or source.is_file(), (
            "segment %s points at %r, which resolves neither as the runtime path %s nor as its "
            "source %s — the carrier lands in T005 and its mirror via "
            "`python3 scripts/python/sync-mirrors.py` (RC-05, RC-10)"
            % (number, match.group(0), runtime.relative_to(ROOT), source.relative_to(ROOT))
        )
    # the two anchors the middle segments cite must exist in the carrier they cite
    carrier = _read(CARRIER_RUNTIME if CARRIER_RUNTIME.is_file() else CARRIER_SRC_DIR / "SKILL.md")
    for anchor in ("Segment A", "Segment B"):
        assert re.search(rf"(?m)^#{{1,6}}\s*{anchor}\b", carrier), (
            "the carrier skill must carry a `## %s — …` heading; a pointer to a section that "
            "does not exist is not a pointer (RC-10, RC-11)" % anchor
        )


# --------------------------------------------------------------------------- #
# (c) boundaries owned once, never merged, code-review survives as the fourth
# --------------------------------------------------------------------------- #

#: The boundary sentences, quoted by the smallest fragment that is unique to the owner. Each is
#: owned by `shared/workflow/acceptance-hardening.md` § Review Composition and MUST occur **once**
#: in the framework's markdown: a second occurrence is a restatement (FR-013's layer split).
BOUNDARY_FRAGMENTS = (
    "substitute for the artifact or implementation segments",
    "MUST NOT substitute for one another",
    "answered by the code segment",
)

#: The owner's derivation rule, quoted by a fragment no consumer may repeat (RC-06).
DERIVATION_FRAGMENT = "declares it owns"


def test_c1_the_boundary_sentences_live_once_and_are_pointed_to():
    """The content layer is one place; the declaration layer points at it (FR-013)."""
    owner = _read(OWNER_DOC)
    for fragment in BOUNDARY_FRAGMENTS:
        assert _has(owner, fragment), (
            "the content owner no longer carries the boundary fragment %r — the boundary has "
            "lost its home" % fragment
        )
        hits = _sweep(fragment)
        assert len(hits) == 1 and hits[0][0] == OWNER_REL, (
            "the boundary fragment %r occurs in %r; it is owned once by %s and every consumer "
            "must point at it instead of restating it (FR-013)"
            % (fragment, hits, OWNER_REL)
        )
    for number in ("2", "3"):
        section = _segment(number)
        assert OWNER_REL in section and OWNER_ANCHOR in section, (
            "segment %s answers its own boundary question without reaching the owner; it must "
            "cite `%s` %s (RC-08, FR-013)" % (number, OWNER_REL, OWNER_ANCHOR)
        )


def test_c2_no_segment_conclusion_is_merged_into_one_severity_or_one_score():
    """RC-04: two vocabularies that convert into each other are one vocabulary."""
    subjects = (
        ("templates/commands/review.md", _read(REVIEW_CMD)),
        ("templates/review-template.md", _read(REVIEW_TEMPLATE)),
        (OWNER_REL, _read(OWNER_DOC)),
    )
    for name, body in subjects:
        for lineno, line in enumerate(body.splitlines(), 1):
            process = _severity_hits(line, PROCESS_SEVERITIES)
            code = _severity_hits(line, CODE_SEVERITIES)
            assert not (process and code), (
                "%s:%d carries a process severity %r and a code severity %r on one line — that "
                "is a mapping row, and the two families are never mapped (RC-04): %r"
                % (name, lineno, process, code, line.strip())
            )
            assert not re.search(
                r"(?i)^\s*(?:-\s*\*\*|\|\s*)(?:unified |combined |overall )?score\b", line
            ), (
                "%s:%d declares a score field; the run stores no combined value (RC-04): %r"
                % (name, lineno, line.strip())
            )


def test_c3_the_code_segment_survives_and_declares_its_position():
    """RC-03/RC-04: `code-review` is not replaced, and it now knows it is the fourth segment."""
    cmd = _read(REVIEW_CMD)
    assert "skills/internal/code-review/SKILL.md" in cmd, (
        "templates/commands/review.md no longer names the code skill — its replacement is "
        "forbidden (RC-03)"
    )
    assert CODE_SKILL.is_file(), "the code skill itself is missing: %s" % CODE_SKILL
    body = _read(CODE_SKILL)
    assert re.search(r"(?i)fourth\s+segment|第四段", _flat(body)), (
        "skills/internal/code-review/SKILL.md must declare its position as the fourth segment of "
        "the fixed order (RC-04): the composition is no longer two segments, and a skill that "
        "does not know where it sits invites a third re-derivation"
    )
    assert seg_is_last(), (
        "`### Segment 4 — …` is not the code segment; the code segment is last in the fixed "
        "order (RC-01)"
    )


def seg_is_last() -> bool:
    """`True` when the fourth segment is the code segment — the order's last position."""
    segments = _segment_sections()
    if not segments:
        return False
    line = _field_line(segments[-1][2], "Skill")
    return bool(line) and "code-review" in line


# --------------------------------------------------------------------------- #
# (d) the artifact denominator is the expected set — falsified, not described
# --------------------------------------------------------------------------- #

def test_d1_the_artifact_segment_declares_the_expected_denominator_by_pointer():
    """RC-06: the rule is stated once, in the owner; the segment states its consequence."""
    section = _segment("2")
    flat = _flat(section)
    assert re.search(r"(?i)expected", flat), (
        "the artifact segment's denominator is not stated as the expected set (RC-06): %r"
        % section[:400]
    )
    assert re.search(r"(?i)checked\s*/\s*expected", flat), (
        "the artifact segment does not state the coverage line shape `checked / expected`; a "
        "denominator whose line shape is unstated is a number without a meaning (RC-06)"
    )
    assert OWNER_REL in section and OWNER_ANCHOR in section, (
        "the artifact segment must reach the derivation by path + anchor (`%s` %s) instead of "
        "carrying a second copy of the rule (RC-06, FR-013)" % (OWNER_REL, OWNER_ANCHOR)
    )
    assert re.search(r"(?i)(restat|second definition)", flat), (
        "the artifact segment must state that restating the derivation there is a defect — "
        "otherwise the two-layer split is a hope, not a rule (FR-013)"
    )
    missing_sentence = [
        s for s in _sentences(section)
        if re.search(r"(?i)\b(missing|absent)\b", s) and re.search(r"(?i)\bfinding", s)
    ]
    assert missing_sentence, (
        "the artifact segment does not state that a required-but-missing artifact yields a "
        "finding (RC-06): %r" % section[:400]
    )
    assert any(re.search(r"(?i)uncovered", s) for s in missing_sentence), (
        "the artifact segment states the finding but not that the absent member counts as "
        "uncovered — reported-but-not-counted under-reports the gap (RC-06, FR-013)"
    )


def test_d2_the_derivation_rule_is_not_restated_outside_its_owner():
    """The rule has one statement. A second one is the copy FR-013 forbids."""
    owner = _read(OWNER_DOC)
    assert _has(owner, DERIVATION_FRAGMENT), (
        "the owner no longer carries the derivation fragment %r" % DERIVATION_FRAGMENT
    )
    hits = _sweep(DERIVATION_FRAGMENT, "templates", "skills", "docs")
    assert not hits, (
        "the derivation rule is restated at %r; it is stated once in %s %s and every consumer "
        "points at it (FR-013)" % (hits, OWNER_REL, OWNER_ANCHOR)
    )


def test_d3_the_seven_members_are_the_derivations_product():
    section = _segment("2")
    named = set(re.findall(r"`([A-Za-z0-9._/-]+)`", section))
    absent = [m for m in EXPECTED_MEMBERS if m not in named]
    assert not absent, (
        "the artifact segment's judgment object is not the full expected set: %r missing from "
        "its own member list (RC-06)" % (absent,)
    )


def _fixture_project_structure(fixture: Path) -> list:
    """The members the fixture's own `plan.md` § Project Structure declares it owns."""
    section = _heading_section(_read(fixture / "plan.md"), r"Project Structure")
    block = re.search(r"(?ms)^```[a-z]*\n(.*?)^```", section)
    assert block, (
        "%s/plan.md § Project Structure carries no fenced member list — the derivation has "
        "nothing to read" % fixture.name
    )
    return [line.strip() for line in block.group(1).splitlines() if line.strip()]


def _present(fixture: Path, member: str) -> bool:
    return (fixture / member).is_dir() if member.endswith("/") else (fixture / member).is_file()


def _coverage(fixture: Path, expected) -> tuple:
    """``(coverage_line, findings, present)`` for one denominator.

    ``findings`` is one per expected-but-absent member — the derivation's own consequence, so the
    two denominators below are computed by the same function and can be compared.
    """
    present = [m for m in expected if _present(fixture, m)]
    missing = [m for m in expected if m not in present]
    return "%d / %d" % (len(present), len(expected)), missing, present


def test_d4_the_declared_derivation_applied_to_the_missing_artifact_case():
    """The rule is falsified on the one case where the two readings differ (FR-013).

    Expected set from the fixture's own ``plan.md`` § Project Structure; membership by an
    existence test on the directory. The absent member is named, and the coverage line is
    strictly below 100 %.
    """
    fixture = _fixture("expected-artifact-missing")
    expected = _fixture_project_structure(fixture)
    assert set(expected) == set(EXPECTED_MEMBERS), (
        "the fixture's declared expected set drifted from the segment's: %r vs %r"
        % (sorted(expected), sorted(EXPECTED_MEMBERS))
    )
    assert len(expected) == 7

    line, findings, present = _coverage(fixture, expected)
    assert findings == ["quickstart.md"], (
        "expected-set minus present-set must name exactly `quickstart.md`; measured %r (present "
        "%r) — the derivation's product is what the case is built to expose (FR-013)"
        % (findings, present)
    )
    assert line == "6 / 7", (
        "the coverage line must read `6 / 7` on this case; measured %r — a segment reading the "
        "directory instead of the expected set reads `6 / 6` (FR-013)" % line
    )
    assert len(present) / len(expected) < 1.0, (
        "the derived coverage must be strictly below 100 %%: %d / %d" % (len(present), len(expected))
    )


def test_d5_the_competing_reading_reads_full_coverage_on_the_same_fixture():
    """Anti-vacuity: unless "the ones that exist" reads differently, leg (d) proves nothing.

    The same fixture, the same membership test, a denominator taken from what is present: 6 / 6 =
    100 % coverage with zero findings — a missing required artifact rendered as a clean review.
    That is the false green FR-013 exists to forbid, and it is why the denominator's source is
    fixed in the owner rather than left to each run's taste.
    """
    fixture = _fixture("expected-artifact-missing")
    expected_line, expected_findings, present = _coverage(fixture, _fixture_project_structure(fixture))
    naive_line, naive_findings, _p = _coverage(fixture, present)

    assert naive_line == "6 / 6", naive_line
    assert naive_findings == [], (
        "the present-only reading must report nothing on this case; measured %r" % (naive_findings,)
    )
    assert expected_line != naive_line, (
        "the two readings agree on this fixture — then the case cannot distinguish them and leg "
        "(d) is not a falsification: %r" % (expected_line,)
    )
    assert expected_findings, "the expected-set reading must report the absent member"


# --------------------------------------------------------------------------- #
# (e) the implementation segment judges this slice's base..head
# --------------------------------------------------------------------------- #

def test_e1_the_implementation_segment_judges_base_to_head_through_the_one_route():
    """RC-07/RC-09: one diff, one base resolution, one smoke triple."""
    section = _segment("3")
    flat = _flat(section)
    assert re.search(r"base\s*\.\.\s*head", flat), (
        "the implementation segment must name its judgment object as this slice's `base..head` "
        "delta (RC-07): %r" % section[:400]
    )
    assert GIT_DELTA_REL in section, (
        "the implementation segment must name `%s` as its base-resolution route (RC-09)" % GIT_DELTA_REL
    )
    assert re.search(r"(?i)\b(no|MUST NOT|never)\b[^.]{0,48}\bsecond\b[^.]{0,48}\bbase\b", flat), (
        "the implementation segment must forbid a second base resolution — the code skill's "
        "ordered tiers are the only route (RC-09): %r" % flat[:400]
    )
    for token in ("smoke", "command", "exit code", "evidence path"):
        assert token in flat.lower(), (
            "the implementation segment does not require the smoke triple (%r missing) — "
            "command, exit code and evidence path are all of it (RC-07)" % token
        )


def test_e2_the_implementation_segment_is_answered_by_nobody_else():
    """RC-08: neither the code segment nor the process skill answers the implementation segment."""
    section = _segment("3")
    flat = _flat(section)
    inputs = _field_line(section, "Inputs")
    assert inputs is not None, "segment 3 carries no `Inputs` row (RC-05)"
    for substitute in ("review-sdd-process", "code-review"):
        assert substitute not in inputs, (
            "the implementation segment's Inputs name %r — a segment answered by a neighbour is "
            "not judged at all (RC-08): %r" % (substitute, inputs.strip())
        )
    assert not re.search(r"(?i)\bcode segment\b[^.]{0,48}\b(answers|substitutes|covers)\b", flat), (
        "the implementation segment hands its question to the code segment (RC-08): %r"
        % flat[:400]
    )
    assert OWNER_REL in section and OWNER_ANCHOR in section, (
        "the implementation segment must reach the no-substitution boundary by pointer "
        "(`%s` %s) instead of restating it (RC-08, FR-013)" % (OWNER_REL, OWNER_ANCHOR)
    )


# --------------------------------------------------------------------------- #
# (f) the Acceptance Reality Check copies; the refusal has a real input
# --------------------------------------------------------------------------- #

def _line_with_all_tokens(text: str, tokens) -> str:
    """The first line or sentence carrying every token — the record's shape, in one place."""
    candidates = list(text.splitlines()) + _sentences(text)
    for candidate in candidates:
        if all(re.search(rf"(?<![\w-]){t}(?![\w-])", candidate, re.IGNORECASE) for t in tokens):
            return candidate.strip()
    return ""


def _arc_item(payload: dict):
    """RC-15's conjunction, computed from a checker payload: the item ARC must emit, or ``None``."""
    claimed = payload.get("claimed_status")
    if claimed in ("Implemented", "Ready for Review") and payload["final_path"]["pass"] == 0:
        return "F-ACCEPTANCE"
    return None


def test_f1_the_arc_copies_the_seven_key_record_and_never_recounts_it():
    """RC-13/RC-14: the record is copied verbatim; a three-count summary is a re-derivation."""
    arc = _arc_section()
    assert len(FINAL_PATH_KEYS) == 7
    carrier = _line_with_all_tokens(arc, FINAL_PATH_KEYS)
    assert carrier, (
        "no line of the Acceptance Reality Check carries all seven `final_path` keys (%r) — a "
        "record narrowed to a three-count summary is a re-derivation with extra steps (RC-14): "
        "%r" % (FINAL_PATH_KEYS, arc[:600])
    )
    assert CHECKER_REL in arc, (
        "the Acceptance Reality Check must name the closure checker as the record's source "
        "(RC-13): %r" % arc[:400]
    )
    assert re.search(r"(?i)(never\s+re-?comput|verbatim|copied)", _flat(arc)), (
        "the Acceptance Reality Check must state that the record is copied and never recomputed "
        "(RC-13): %r" % arc[:400]
    )


def test_f2_the_refusal_names_the_fixed_item_and_leaves_the_claimed_status():
    """RC-15: `F-ACCEPTANCE` at `P0`, the failed condition named, the claim unchanged."""
    arc = _arc_section()
    flat = _flat(arc)
    assert "F-ACCEPTANCE" in arc, (
        "the refusal path does not name the fixed item `F-ACCEPTANCE`; the literal is owned by "
        "the declaring feature's § Shared Strings and quoted verbatim (RC-15, STR-016)"
    )
    assert re.search(r"(?<![\w-])P0(?![\w-])", arc), (
        "`F-ACCEPTANCE` is emitted at `P0`; the severity is part of the fixed item (RC-15)"
    )
    assert re.search(r"(?i)refus", flat), (
        "the Acceptance Reality Check does not state that the transition is refused (RC-15)"
    )
    assert re.search(r"(?i)unchanged|stays|leaves", flat) and "Implemented" in arc, (
        "the refusal must leave the claimed status unchanged — a refusal is not a downgrade "
        "(RC-15): %r" % arc[:400]
    )


def test_f3_the_refusal_fires_on_the_blocked_case_and_cannot_fire_on_negative():
    """The input the refusal needs exists exactly once in the corpus.

    ``negative`` claims ``Planned``, so RC-15's conjunction is never reached there: driving the
    refusal on it would assert nothing. ``review-implemented-blocked`` claims ``Implemented`` with
    a zero ``pass`` bucket, which is the only shape that reaches the conjunction.
    """
    blocked, blocked_payload, _ = _payload("review-implemented-blocked")
    negative, negative_payload, _ = _payload("negative")

    assert blocked.returncode == 1, blocked.stdout + blocked.stderr
    assert blocked_payload["claimed_status"] == "Implemented", blocked_payload["claimed_status"]
    assert blocked_payload["final_path"]["pass"] == 0, blocked_payload["final_path"]
    assert [r["code"] for r in blocked_payload["reasons"]] == [
        "zero-final-path-pass",
        "status-claims-implemented-but-blocked",
    ], blocked_payload["reasons"]
    assert _arc_item(blocked_payload) == "F-ACCEPTANCE", (
        "the blocked case is the refusal's own input: claimed `Implemented` and a zero `pass` "
        "bucket must emit `F-ACCEPTANCE` (RC-15)"
    )

    assert negative_payload["claimed_status"] == "Planned", negative_payload["claimed_status"]
    assert _arc_item(negative_payload) is None, (
        "`negative` claims `Planned`, so RC-15's conjunction cannot be reached there — the "
        "refusal MUST NOT be measured on it (T004 leg (f))"
    )


def test_f4_the_refusal_never_downgrades_the_claimed_status():
    """Measured at the source: the checker reports, it does not edit the claim."""
    fixture = _fixture("review-implemented-blocked")
    detail = fixture / "feature-detail.md"
    before = re.search(r"(?m)^\*\*Status\*\*:\s*(\S+)", _read(detail))
    assert before and before.group(1) == "Implemented", before

    _proc, payload, _raw = _payload("review-implemented-blocked")
    assert payload["claimed_status"] == "Implemented"

    after = re.search(r"(?m)^\*\*Status\*\*:\s*(\S+)", _read(detail))
    assert after and after.group(1) == "Implemented", (
        "the blocked run changed the claim to %r; a refusal leaves `Implemented` at "
        "`Implemented` (RC-15)" % (after.group(1) if after else None,)
    )


# --------------------------------------------------------------------------- #
# (g) the three report slots
# --------------------------------------------------------------------------- #

def test_g1_the_three_slots_exist_after_2_1_and_2_1_is_not_renumbered():
    """RC-17: stable slots, in slot order, with `### 2.1` where it was."""
    body = _read(REVIEW_TEMPLATE)
    positions = {}
    for token in REPORT_SLOTS:
        match = re.search(rf"(?m)^{re.escape(token)}\b", body)
        assert match, (
            "templates/review-template.md no longer carries `%s` (RC-17); found slots %r"
            % (token, re.findall(r"(?m)^### 2\.\d+", body))
        )
        positions[token] = match.start()
    assert list(positions.values()) == sorted(positions.values()), (
        "the report slots are out of order: %r — the numbers are stable slots, not execution "
        "order, and the new ones land after `### 2.1` (RC-17)" % (positions,)
    )
    numbers = re.findall(r"(?m)^### (2\.\d+)", body)
    assert numbers == ["2.1", "2.2", "2.3", "2.4"], (
        "the § 2 subsections must read 2.1 → 2.4 with `### 2.1` neither renumbered nor "
        "duplicated; found %r (RC-17)" % (numbers,)
    )


def test_g2_the_two_review_slots_carry_the_finding_location_fields():
    """RC-17 placeholder-side: the slots are fillable, so the fields must be tokens."""
    for slot in FINDING_SLOTS:
        section = _slot(slot)
        used = set(re.findall(r"\[([A-Z][A-Z0-9_]+)\]", section))
        assert used, "`%s` carries no placeholder token at all" % slot
        flat = _flat(section).lower()
        assert "severity" in flat, (
            "the `%s` slot carries no severity field; a finding with no level is a complaint "
            "(RC-06, RC-17)" % slot
        )
        assert re.search(r"(?i)\bline\b", section), (
            "the `%s` slot carries no line field (RC-06, RC-17)" % slot
        )
        assert re.search(r"(?i)\b(artifact|diff)\b", section), (
            "the `%s` slot carries no artifact/diff path field (RC-06, RC-17)" % slot
        )


def test_g3_every_placeholder_in_the_new_slots_is_glossed():
    """RC-17: a token the glossary never defines is a value nobody can fill correctly."""
    body = _read(REVIEW_TEMPLATE)
    assert "## Placeholder Glossary" in body, "the report template lost its Placeholder Glossary"
    glossary = body[body.index("## Placeholder Glossary"):]
    for slot in FINDING_SLOTS + ("2.4 Acceptance Reality Check",):
        section = _slot(slot)
        used = sorted(set(re.findall(r"\[([A-Z][A-Z0-9_]+)\]", section)))
        missing = [token for token in used if token not in glossary]
        assert not missing, (
            "placeholder tokens used in `%s` but absent from the Placeholder Glossary: %r"
            % (slot, missing)
        )


# --------------------------------------------------------------------------- #
# (h) the feedback unit census is four
# --------------------------------------------------------------------------- #

def test_h_the_census_is_four_units_sharing_one_run_id():
    """RC-18: the count moves with the carrier, not the other way round."""
    section = _heading_section(_read(REVIEW_CMD), r"Feedback boundary[^\n]*")
    flat = _flat(section)
    for unit in CENSUS_UNITS:
        assert unit in section, (
            "the feedback boundary does not name the unit %r; the census of one composed run is "
            "%r (RC-18)" % (unit, CENSUS_UNITS)
        )
    assert re.search(r"(?i)\bfour\b[^.]{0,60}\bunits?\b", flat), (
        "the feedback boundary does not state the census as four units (RC-18): %r" % flat[:400]
    )
    assert re.search(r"(?i)run[ _]id", section), (
        "the census must state that the four units share one `run_id` — that is the key the "
        "feedback engine already uses, and without it the count is a coincidence (RC-18)"
    )
    assert re.search(r"(?i)MUST NOT suppress|suppress(?:es|ed)? no", flat), (
        "the command must state that it suppresses no skill's wrap-up (RC-18): %r" % flat[:400]
    )
    assert not re.search(r"(?i)\bthree units\b|三个单元", flat), (
        "the pre-change `three units` wording survives in the feedback boundary — the census "
        "moves with the carrier (RC-18, RC-19)"
    )


# --------------------------------------------------------------------------- #
# (i) the call site is wired, not named
# --------------------------------------------------------------------------- #

#: The documented invocation, extracted rather than retyped (GW-02).
INVOCATION = re.compile(r"python3\s+%s[^\n`]*" % re.escape(CHECKER_REL))


def _invocation() -> str:
    match = INVOCATION.search(_read(REVIEW_CMD))
    assert match, (
        "templates/commands/review.md names no runnable closure-checker invocation "
        "(`python3 %s --spec-dir <dir>`) — a review site that only mentions the checker leaves "
        "the judgement to whoever reads it (GW-02)" % CHECKER_REL
    )
    return match.group(0).strip()


def _run_invocation(spec_dir: Path):
    argv = shlex.split(_invocation())
    assert argv and argv[0].startswith("python3"), argv
    if "--spec-dir" in argv:
        argv[argv.index("--spec-dir") + 1] = str(spec_dir)
    else:
        argv += ["--spec-dir", str(spec_dir)]
    if "--json" not in argv:
        argv.append("--json")
    return subprocess.run([sys.executable] + argv[1:], capture_output=True, text=True,
                          cwd=str(ROOT))


def _json_from(proc, where: str) -> dict:
    assert proc.stdout.strip(), (
        "the documented invocation produced no payload on %s:\nstdout:\n%s\nstderr:\n%s"
        % (where, proc.stdout, proc.stderr)
    )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:  # pragma: no cover - a malformed payload is the failure
        raise AssertionError(
            "the documented invocation did not emit JSON on %s (%s):\n%s" % (where, exc, proc.stdout)
        )


def _payload(fixture_name: str):
    """Run the checker directly on a fixture — for the ARC rule, not for the call site."""
    assert CHECKER.is_file(), "closure-acceptance-check.py is missing"
    fixture = _fixture(fixture_name)
    proc = subprocess.run(
        [sys.executable, str(CHECKER), "--spec-dir", str(fixture), "--json"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    return proc, _json_from(proc, fixture_name), proc.stdout


def _closed_reason_prefixes() -> set:
    """The closed set's prefixes, read out of their owner (`requirements.md` § Shared Strings)."""
    text = _read(REQUIREMENTS)
    rows = dict(re.findall(r"(?m)^\| `(STR-0\d\d)` \| `([^`]+)` \|", text))
    absent = [sid for sid in REASON_IDS if sid not in rows]
    assert not absent, "requirements.md no longer declares %r — the closed set moved" % (absent,)
    return {rows[sid].partition(": ")[0] for sid in REASON_IDS}


def test_i1_the_documented_invocation_blocks_the_negative_fixture():
    """GW-02: the extracted command, run, refuses — with a reason inside the closed set."""
    fixture = _fixture("negative")
    proc = _run_invocation(fixture)
    payload = _json_from(proc, "negative")
    assert proc.returncode == 1, (
        "the review site's own invocation, run against the 026-shape fixture, must refuse "
        "(exit 1):\nstdout:\n%s\nstderr:\n%s" % (proc.stdout, proc.stderr)
    )
    prefixes = _closed_reason_prefixes()
    codes = [r.get("code", "") for r in payload.get("reasons", [])]
    assert codes, "a refused review MUST carry at least one named reason (RC-15)"
    outside = [code for code in codes if code not in prefixes]
    assert not outside, (
        "the refusal reasons %r are outside the closed set %r — a refusal that invents a reason "
        "is not the verdict the owner defines" % (outside, sorted(prefixes))
    )


def test_i2_the_documented_invocation_accepts_the_positive_fixture():
    proc = _run_invocation(_fixture("positive"))
    assert proc.returncode == 0, (
        "a complete feature must not be refused by the wired review site:\nstdout:\n%s\n"
        "stderr:\n%s" % (proc.stdout, proc.stderr)
    )


def test_i3_the_clean_case_is_claimed_implemented_and_passes_all_four_conditions():
    """SC-002's measurement: the fourth condition is **judged and passed**, not skipped.

    A `positive`-on-`Planned` drive passes by inapplicability, so it is not this measurement.
    """
    proc = _run_invocation(_fixture("review-implemented-clean"))
    payload = _json_from(proc, "review-implemented-clean")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert payload["claimed_status"] == "Implemented", (
        "the clean case must be claimed `Implemented`; measured %r — a `Planned` claim makes "
        "the fourth condition inapplicable rather than measured" % payload["claimed_status"]
    )
    conditions = payload["completion_conditions"]
    assert set(conditions) == set(COMPLETION_CONDITIONS), (
        "the payload's completion conditions moved: %r" % (sorted(conditions),)
    )
    unmet = [key for key, value in conditions.items() if not value]
    assert not unmet, "the clean case must satisfy 4/4 completion conditions; unmet %r" % (unmet,)
    assert payload["final_path"]["pass"] >= 1, payload["final_path"]


def test_i4_the_blocked_case_refuses_with_zero_final_path_pass():
    proc = _run_invocation(_fixture("review-implemented-blocked"))
    payload = _json_from(proc, "review-implemented-blocked")
    assert proc.returncode == 1, (
        "claimed `Implemented` with a zero `pass` bucket must be refused (exit 1):\n%s%s"
        % (proc.stdout, proc.stderr)
    )
    codes = [r.get("code", "") for r in payload.get("reasons", [])]
    assert "zero-final-path-pass" in codes, (
        "the refusal must carry `zero-final-path-pass`; measured %r" % (codes,)
    )


# --------------------------------------------------------------------------- #
# (j) the finding locator is a MUST with exactly one escape
# --------------------------------------------------------------------------- #

#: The one escape RC-06 admits: a **stated reason**, in the finding's own text.
LOCATOR_REQUIRED = re.compile(r"(?i)\brequired\b")
LOCATOR_ADDRESSABLE = re.compile(r"(?i)line[- ]addressable")
LOCATOR_REASON = re.compile(r"(?i)\b(reason|why)\b")


def _marks_line_optional(text: str) -> list:
    """Every place that pairs ``line`` with ``optional`` **without** negating it.

    Written this way because "`line` is never optional" and "`line` (optional)" are one token
    apart and opposite obligations; a plain `in` test cannot tell them apart.
    """
    hits = []
    for match in re.finditer(r"(?i)\bline\b([^.\n]{0,32})\boptional\b", text):
        window = text[max(0, match.start() - 24):match.end()]
        if re.search(r"(?i)\b(never|not|no|MUST NOT)\b", window):
            continue
        hits.append(match.group(0).strip())
    return hits


def test_j1_both_report_slots_require_the_line_and_state_the_one_escape():
    for slot in FINDING_SLOTS:
        section = _slot(slot)
        assert LOCATOR_ADDRESSABLE.search(section), (
            "`%s` does not state that `line` is required whenever the artifact is line-addressable "
            "— that conditional IS the MUST (RC-06)" % slot
        )
        assert LOCATOR_REQUIRED.search(section), (
            "`%s` does not state the requirement at all (RC-06)" % slot
        )
        assert LOCATOR_REASON.search(section), (
            "`%s` states no escape: an omission MUST name why, in the finding itself (RC-06)"
            % slot
        )
        assert not _marks_line_optional(section), (
            "`%s` marks `line` optional (%r); `line` is required whenever the artifact is "
            "line-addressable and the single escape is a stated reason (RC-06)"
            % (slot, _marks_line_optional(section))
        )


def test_j2_the_method_doc_owns_the_rule_and_no_carrier_makes_line_optional():
    files = sorted(CARRIER_SRC_DIR.rglob("*.md")) if CARRIER_SRC_DIR.is_dir() else []
    assert files, (
        "no method doc under %s — the finding field set has no owner to state the rule "
        "(RC-10, RC-06)" % CARRIER_SRC_DIR.relative_to(ROOT)
    )
    body = "\n".join(_read(path) for path in files)
    assert LOCATOR_ADDRESSABLE.search(body), (
        "the method doc does not state that `line` is required whenever the artifact is "
        "line-addressable (RC-06)"
    )
    assert LOCATOR_REQUIRED.search(body), "the method doc states no requirement on `line` (RC-06)"
    assert LOCATOR_REASON.search(body), (
        "the method doc states no escape — the one allowed omission is a named reason (RC-06)"
    )
    for path in files:
        offenders = _marks_line_optional(_read(path))
        assert not offenders, (
            "%s marks `line` optional (%r) — no carrier of the field set may (RC-06)"
            % (path.relative_to(ROOT).as_posix(), offenders)
        )


# --------------------------------------------------------------------------- #
# (k) the process skill keeps exactly one judgment object
# --------------------------------------------------------------------------- #

JUDGMENT_MARKER = re.compile(r"(?m)^\s*-\s*\*\*Judgment object\*\*:")


def test_k1_the_process_skill_carries_exactly_one_judgment_object():
    """RC-12: counted, not sampled — a second judgment object is the rejected antithesis."""
    text = _read(PROCESS_SKILL)
    markers = JUDGMENT_MARKER.findall(text)
    assert len(markers) == 1, (
        "skills/internal/review-sdd-process/SKILL.md carries %d `- **Judgment object**:` markers; "
        "exactly one is required — an uncountable declaration is what let the carrier decision go "
        "unasserted (RC-12)" % len(markers)
    )
    contract = _heading_section(text, r"Input Contract")
    assert JUDGMENT_MARKER.search(contract), (
        "the single judgment object is not declared in `## Input Contract`, immediately after "
        "`- **Subject**:`, where RC-12's leg counts it"
    )


def test_k2_the_two_dimension_headings_live_only_in_the_carrier():
    """RC-10: the method has one home. The rejected antithesis puts it under the process skill."""
    for heading in SEGMENT_HEADINGS:
        offenders = []
        carriers = []
        for path in sorted((ROOT / "skills").rglob("*.md")):
            lines = {line.strip() for line in _read(path).splitlines()}
            if heading not in lines:
                continue
            rel = path.relative_to(ROOT).as_posix()
            (carriers if "internal/review-feature-quality/" in rel else offenders).append(rel)
        process_hits = [p for p in offenders if "internal/review-sdd-process/" in p]
        assert not process_hits, (
            "%r appears under the process skill (%r) — a second judgment object in that body is "
            "the rejected antithesis (RC-10, RC-12)" % (heading, process_hits)
        )
        assert not offenders, (
            "%r appears outside the carrier skill (%r); the method has one home "
            "(RC-10)" % (heading, offenders)
        )
        assert carriers, (
            "%r appears nowhere under skills/internal/review-feature-quality/ — the carrier "
            "T005 lands must declare both segments (RC-10)" % heading
        )


# --------------------------------------------------------------------------- #
# Anti-vacuity for the judges the other legs lean on
# --------------------------------------------------------------------------- #

def test_the_judges_reject_near_misses_so_no_leg_is_a_bare_string_test():
    """Each judge below is used by a leg that must be able to go red; prove it can reject.

    Without this, `_marks_line_optional`, `_line_with_all_tokens` and the merged-family scan
    could each be an `assert True` in disguise, and every assertion built on them would pass on
    any text — the failure mode this module exists to avoid, one level down.
    """
    # The locator judge: "(optional)" is the pre-change reading, "never optional" is the rule.
    assert _marks_line_optional("`line` (optional) — fill it in when you can")
    assert _marks_line_optional("line: optional")
    assert not _marks_line_optional("`line` is required; it is never optional")
    assert not _marks_line_optional("no field of this set is optional")

    # The record judge: the seven-key record passes, a three-count summary does not.
    record = ("final_path = {pass: 1, blocked: 0, deferred: 0, partial: 0, fail: 0, "
              "unknown: 0, total: 1}")
    assert _line_with_all_tokens(record, FINAL_PATH_KEYS)
    assert not _line_with_all_tokens("pass / blocked / deferred", FINAL_PATH_KEYS)
    assert not _line_with_all_tokens("pass: 1, blocked: 0, deferred: 0, total: 1", FINAL_PATH_KEYS)

    # The merge judge: both families are detected where present, and one is never the other.
    merged = "`P0` blocks, and `blocking` blocks too"
    assert _severity_hits(merged, PROCESS_SEVERITIES)
    assert _severity_hits(merged, CODE_SEVERITIES)
    assert not _severity_hits("`blocking-unresolved` is a refusal literal", CODE_SEVERITIES)

    # The closed reason set is read from its owner and holds exactly seven.
    assert len(_closed_reason_prefixes()) == 7
