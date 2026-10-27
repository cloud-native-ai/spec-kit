"""Contract test: the `Implemented → Ready for Review` gate and its single owner (Feature 071).

Pins `contracts/status-gate-ownership.md` C-45…C-54 against the surfaces that
carry them:

* C-45/C-46 — `templates/feature-details-template.md` § Canonical Status State
  Machine owns the criteria; its row carries the three conjunctive conditions;
  the third one is an **existence** test over the current code-segment record
  (`code-review.md`) and is read in the six-level vocabulary directly.
* C-47/C-48 — the two initiating rows in `shared/workflow/feature-integration.md`
  converge to references: the `/speckit.review` row is an unconditional
  initiator, the `/speckit.checklist` row a **conditional** one, each naming the
  transition, the owner section, and stating that the criteria are not restated.
  The third mention of the transition (`templates/commands/checklist.md`) keeps
  its pointer and gains no criteria copy.
* C-49 — `important` allows the transition but must be answered; `suggestion`,
  `nitpick`, `question` and `praise` never block.
* C-50 — no numeric conversion, mapping matrix or unified score exists between
  the two severity families, and no artifact of this feature is a place to store
  one.
* C-51 — a waiver comes only from an explicit user ruling (a driver's or an
  orchestrator's confirmation is not one); the unattended disposition is
  halt-and-report with `blocking-unresolved` as the named refusal literal.
* C-52/C-53 — a non-conclusion and a refusal are disclosed on the two verifiable
  carriers; a refusal names the failed condition and leaves the status at
  `Implemented`.
* C-54 — the transition is judged once, after both segments finished and both
  artifacts are on disk.

Two layers are measured, deliberately:

* The **existence semantics** are driven against the real merge gate — the
  `report --summary --file <record>` subcommand of
  `skills/internal/code-review/scripts/git-delta-review.sh` — inside the
  disposable repository of the T003 fixture. The gate is what SC-004 reports, so
  the two runs of SC-004 are real invocations here, not a reading of prose. The
  archive case is driven too, because "reads only the record the run points at"
  is only measurable if a blocking heading sitting in an archived record is
  present during the run.
* The **normative wording** is measured against the four surfaces that carry it.
  This group does not pin the merge gate's exit alphabet (C-26/C-27 own it) nor
  the receipt's counts (C-31…C-44 own them): a second copy here would be the
  drift this feature exists to remove.

Red before the ownership statement lands (Tests Mode = ON, Constitution
Principle IV): at the time this file was written the owner row carried only two
of the three conditions ("deferred tasks resolved or waived, and review evidence
has been produced"), the integration protocol carried a **second** criteria
wording of its own, and none of the surfaces named an owner, a waiver rule, a
refusal literal or a checkpoint.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import List

import pytest

from fixtures.review_git_repo import ReviewGitRepo

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
FEATURE_DETAILS = ROOT / "templates" / "feature-details-template.md"
FEATURE_INTEGRATION = ROOT / "shared" / "workflow" / "feature-integration.md"
REVIEW_CMD = ROOT / "templates" / "commands" / "review.md"
CHECKLIST_CMD = ROOT / "templates" / "commands" / "checklist.md"

#: The owner the two initiating rows must name (C-45/C-47/C-48).
OWNER_PATH = "templates/feature-details-template.md"
OWNER_SECTION = "Canonical Status State Machine"
TRANSITION = "Implemented → Ready for Review"

#: The six-level code vocabulary, owned by `skills/internal/code-review/SKILL.md`.
#: Referenced here only to detect a relabel or a second enumeration, never to
#: define it.
CODE_SEVERITIES = ("blocking", "important", "suggestion", "nitpick", "question", "praise")
PROCESS_SEVERITIES = ("P0", "P1", "P2")

#: The three conjunctive conditions as the owner block states them. A second
#: wording elsewhere would have to reproduce these phrases, so their absence
#: outside the owner file is what makes "one owner, references only" mechanical.
CONDITION_MARKERS = (
    "resolved or explicitly waived",
    "review evidence has been produced",
    "contains no `blocking` entry",
)

#: The row-shaped summary of the same three conditions (C-46).
ROW_CONDITION_MARKERS = (
    "resolved or explicitly waived",
    "review evidence",
    "no `blocking` entry",
)

#: Anything a *second* criteria wording would carry. A row that names the
#: transition and points at the owner while carrying none of these is a
#: reference; a row carrying one of them is a copy (C-47/C-48).
CRITERIA_COPY_TOKENS = (
    "blocking",
    "deferred",
    "review evidence",
    "review.md committed",
    "resolved or waived",
)

#: The named refusal literal (FR-009, STR-010) and the spellings a typo or a
#: reworded literal would produce.
REFUSAL_LITERAL = "blocking-unresolved"
REFUSAL_VARIANTS = ("blocking_unresolved", "blocking unresolved", "blocked-unresolved")

#: The two verifiable carriers (C-52/C-53): the report's code subsection and the
#: feature detail's `## Latest Review` review-record entry.
CARRIER_REPORT = "### 2.1"
CARRIER_FEATURE = "## Latest Review"

#: Verbatim records for the driven gate cases. The gate counts severity headings
#: in the record, so the heading form is what matters (`### … [BLOCKING] …`).
BLOCKING_RECORD = (
    "# Code Review\n\n### ! [BLOCKING] src/fixture_demo.py\n\n"
    "- **Why**: a real defect in the reviewed slice\n"
)
CLEAN_RECORD = (
    "# Code Review\n\n### ~ [SUGGESTION] src/fixture_demo.py\n\n"
    "- **Why**: a style opinion, which never blocks\n"
)
IMPORTANT_ONLY_RECORD = (
    "# Code Review\n\n### i [IMPORTANT] src/fixture_demo.py\n\n"
    "- **Why**: an important item that must be answered\n"
)
ARCHIVE_NAME = "code-review-20260101T000000Z.md"


# --------------------------------------------------------------------------- #
# helpers — surfaces
# --------------------------------------------------------------------------- #

def _read(path: Path) -> str:
    assert path.is_file(), f"surface is missing: {path}"
    return path.read_text(encoding="utf-8")


def _flat(text: str) -> str:
    """Collapse whitespace so a phrase can be asserted across a line wrap."""
    return re.sub(r"\s+", " ", text)


def _has(text: str, phrase: str) -> bool:
    return phrase.lower() in _flat(text).lower()


def _section(text: str, start_re: str, end_re: str) -> str:
    start = re.search(start_re, text, re.M)
    assert start, f"section not found: {start_re!r}"
    tail = text[start.end():]
    end = re.search(end_re, tail, re.M)
    return tail[: end.start()] if end else tail


def _owner_section() -> str:
    """§ Canonical Status State Machine of the feature-details template."""
    return _section(
        _read(FEATURE_DETAILS),
        r"^### Canonical Status State Machine",
        r"^## ",
    )


def _owner_block() -> str:
    """The transition's own block inside the owner section (the criteria's body)."""
    return _section(
        _read(FEATURE_DETAILS),
        r"^\*\*The `Implemented → Ready for Review` gate",
        r"^## ",
    )


def _owner_row() -> str:
    rows = [
        line
        for line in _owner_section().splitlines()
        if line.startswith("| Implemented ") and "Ready for Review" in line
    ]
    assert len(rows) == 1, (
        f"the owner section MUST carry exactly one `{TRANSITION}` row, found {len(rows)}"
    )
    return rows[0]


def _integration_table() -> str:
    return _section(
        _read(FEATURE_INTEGRATION),
        r"^## Status State Machine",
        r"^## ",
    )


def _initiating_row(command: str) -> str:
    table = _integration_table()
    rows = [line for line in table.splitlines() if line.startswith(f"| `{command}`")]
    assert len(rows) == 1, (
        f"`{command}` MUST own exactly one transition row, found {len(rows)}"
    )
    return rows[0]


def _cmd_gate_section() -> str:
    """The command template's pointer section for the transition (T022)."""
    return _section(_read(REVIEW_CMD), r"^## Status Transition", r"^## ")


def _table_rows(text: str) -> List[str]:
    return [line for line in text.splitlines() if line.lstrip().startswith("|")]


def _cells(row: str) -> List[str]:
    return [cell.strip() for cell in row.strip().strip("|").split("|")]


def _is_separator(row: str) -> bool:
    parts = _cells(row)
    return bool(parts) and set(parts[0].replace(" ", "")) <= set("-:")


def _severity_hits(line: str) -> List[str]:
    return [sev for sev in CODE_SEVERITIES if re.search(rf"\b{sev}\b", line, re.I)]


def _process_hits(line: str) -> List[str]:
    return [sev for sev in PROCESS_SEVERITIES if re.search(rf"\b{sev}\b", line)]


def _is_prohibition(line: str) -> bool:
    """A sentence that *forbids* the pairing is not a mapping row.

    Without this exemption the prohibition itself would be read as the mapping it
    forbids; the exemption is narrow (an explicit prohibition marker) so a real
    mapping row cannot hide behind ordinary wording.
    """
    low = line.lower()
    return any(
        marker in low
        for marker in ("forbidden", "never", "no conversion", "must not", "not exist")
    )


# --------------------------------------------------------------------------- #
# helpers — the driven merge gate
# --------------------------------------------------------------------------- #

@pytest.fixture()
def repo(tmp_path: Path) -> ReviewGitRepo:
    """A disposable git repository rooted in the case's own `tmp_path`."""
    with ReviewGitRepo(root=tmp_path) as built:
        yield built


def _gate(repo: ReviewGitRepo):
    """Run the merge gate against the record the run itself points at."""
    return repo.run_script(
        "report", "--summary", "--file", str(repo.record_path)
    )


def _plain(text: str) -> str:
    return re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", text)


# --------------------------------------------------------------------------- #
# C-45 — one owner for the criteria, references everywhere else
# --------------------------------------------------------------------------- #

def test_c45_the_owner_section_declares_itself_the_authority_for_the_transition():
    section = _owner_section()
    assert _has(section, "authoritative transition table"), (
        "the owner section MUST still declare itself the authoritative transition "
        "table (C-45), or the section later rows point at is no longer the owner"
    )
    block = _owner_block()
    assert _has(block, "owns the transition's criteria") or _has(
        block, "owns the criteria"
    ), (
        "the transition's block MUST state that it owns the criteria; got:\n" + block[:400]
    )
    assert re.search(r"by reference", _flat(block), re.I), (
        "the owner block MUST state the shape the other surfaces take: they reach the "
        "criteria here by reference (C-45)"
    )
    assert re.search(r"no second wording", _flat(block), re.I), (
        "the owner block MUST forbid a second wording of the criteria elsewhere (C-45)"
    )


def test_c45_no_second_criteria_wording_survives_on_another_surface():
    block = _owner_block()
    for marker in CONDITION_MARKERS:
        assert _has(block, marker), (
            f"the owner block MUST carry the condition {marker!r} (C-46); "
            "it is the one place the criteria are stated"
        )
    for path in (FEATURE_INTEGRATION, REVIEW_CMD, CHECKLIST_CMD):
        text = _flat(_read(path))
        for marker in CONDITION_MARKERS:
            assert marker.lower() not in text.lower(), (
                f"{path.relative_to(ROOT)} carries a second wording of the criteria "
                f"({marker!r}); the owner states them and every other surface reaches "
                "them by reference (C-45/C-47)"
            )


# --------------------------------------------------------------------------- #
# C-46 — three conjunctive conditions, the third an existence test
# --------------------------------------------------------------------------- #

def test_c46_the_owner_row_carries_the_three_conjunctive_conditions():
    row = _owner_row()
    assert TRANSITION.split(" → ")[1] in row, "the row MUST name its target status"
    for marker in ROW_CONDITION_MARKERS:
        assert _has(row, marker), (
            f"the owner row MUST carry the condition {marker!r}; got:\n{row}"
        )
    assert "`code-review.md`" in row, (
        "the third condition MUST name the record it reads (`code-review.md`)"
    )
    assert re.search(r"\bthree\b|\b3 conditions\b|all required", _flat(row), re.I), (
        "the row MUST read as three conjunctive conditions, not as an optional list"
    )


def test_c46_the_third_condition_is_an_existence_test_over_the_current_record():
    block = _owner_block()
    assert _has(block, "existence test"), (
        "the third condition MUST be stated as an existence test over the current "
        "record (A-05), not as a resolution test"
    )
    assert re.search(r"\bat least one\b[^.]{0,80}blocking", _flat(block), re.I), (
        "the existence test MUST be stated on its positive side: at least one "
        "`blocking` entry blocks"
    )
    assert _has(block, "current code-segment record") or _has(
        block, "current record"
    ), "the test is over the CURRENT record only"


def test_c46_one_blocking_entry_blocks_and_a_fresh_record_allows(repo: ReviewGitRepo):
    repo.write_record(BLOCKING_RECORD)
    deny = _gate(repo)
    assert deny.returncode == 1, (
        "a current record carrying one `blocking` entry MUST refuse the transition "
        "(exit 1), as SC-004's first run reports:\n" + deny.describe()
    )
    assert "blocking_entries=1" in _plain(deny.stdout), (
        "the refusal MUST name the count of `blocking` entries:\n" + deny.describe()
    )

    # SC-004's second run: a later run rewrites the record. Nothing is "cleared" —
    # the new record simply contains no `blocking` heading, and the same command
    # then allows. No clearing action exists to be performed here.
    repo.write_record(CLEAN_RECORD)
    allow = _gate(repo)
    assert allow.returncode == 0, (
        "a later record with zero `blocking` entries MUST allow the same transition "
        "(SC-004's second run), with no clearing step in between:\n" + allow.describe()
    )
    assert "blocking_entries=0" in _plain(allow.stdout), (
        "the allow run MUST still report what it counted:\n" + allow.describe()
    )


def test_c46_an_archived_record_never_keeps_blocking(repo: ReviewGitRepo):
    archive = repo.spec_dir / ARCHIVE_NAME
    archive.parent.mkdir(parents=True, exist_ok=True)
    archive.write_text(BLOCKING_RECORD, encoding="utf-8")
    repo.write_record(CLEAN_RECORD)
    allow = _gate(repo)
    assert allow.returncode == 0, (
        "an archived record holding a `blocking` entry MUST NOT block: the condition "
        "reads only the record the run points at (C-46):\n" + allow.describe()
    )
    assert archive.is_file(), "the case is vacuous unless the archive really exists"


def test_c46_the_archive_does_not_dilute_a_blocking_current_record(repo: ReviewGitRepo):
    archive = repo.spec_dir / ARCHIVE_NAME
    archive.parent.mkdir(parents=True, exist_ok=True)
    archive.write_text(CLEAN_RECORD, encoding="utf-8")
    repo.write_record(BLOCKING_RECORD)
    deny = _gate(repo)
    assert deny.returncode == 1, (
        "the current record alone decides; a clean archive cannot offset it "
        "(C-46):\n" + deny.describe()
    )


def test_c46_no_clearing_action_and_no_cleared_state_are_defined():
    block = _owner_block()
    assert _has(block, "no clearing action"), (
        "the owner MUST state that no clearing action exists (A-05); without it the "
        "reader invents one"
    )
    assert _has(block, "no cleared state"), (
        "the owner MUST state that no cleared state exists (A-05)"
    )
    states = set()
    for row in _table_rows(_owner_section()):
        if _is_separator(row):
            continue
        parts = _cells(row)
        if len(parts) < 2 or parts[0].lower() in {"from", "command"}:
            continue
        states.update(part.strip("`*") for part in parts[:2])
    states.discard("(n/a)")
    assert states == {
        "Draft",
        "Planned",
        "Implemented",
        "Ready for Review",
        "Completed",
    }, (
        "the transition table's state set MUST stay the five published statuses; a "
        f"`cleared` (or any other) state is a second mechanism (C-46): {sorted(states)}"
    )
    for row in _table_rows(_integration_table()):
        assert "clear" not in row.lower(), (
            f"no initiating row may describe a clearing step: {row!r}"
        )


def test_c46_the_six_level_vocabulary_is_read_directly_not_relabelled():
    block = _owner_block()
    for level in CODE_SEVERITIES:
        assert f"`{level}`" in block, (
            f"the owner block MUST name the level `{level}` it reads; the vocabulary "
            "is cited, not defined elsewhere in this feature"
        )
    assert re.search(r"relabell?ing", _flat(block), re.I), (
        "the owner MUST forbid relabelling the vocabulary before judging"
    )
    for level in PROCESS_SEVERITIES:
        assert level in block, (
            f"the prohibition MUST name {level!r} as the family the relabel would "
            "borrow (C-50's rejected request)"
        )
    assert _has(block, "directly"), (
        "the condition is judged by reading the six levels directly (C-46)"
    )


# --------------------------------------------------------------------------- #
# C-47 — the `/speckit.review` row becomes a reference
# --------------------------------------------------------------------------- #

def test_c47_the_review_row_is_a_reference_to_the_owner():
    row = _initiating_row("/speckit.review")
    assert TRANSITION in row, "the row MUST still name the transition it initiates"
    assert OWNER_PATH in row, f"the row MUST name the owner path {OWNER_PATH!r}"
    assert OWNER_SECTION in row, f"the row MUST name the owner section {OWNER_SECTION!r}"
    assert re.search(r"not restated|不.*重述|不再重述", _flat(row)), (
        "the row MUST state that the criteria are not restated there (C-47); got:\n"
        + row
    )


def test_c47_the_duplicated_criteria_wording_is_removed_not_reworded():
    row = _initiating_row("/speckit.review")
    hits = [token for token in CRITERIA_COPY_TOKENS if token.lower() in row.lower()]
    assert not hits, (
        "the review row MUST NOT carry its own criteria wording; the duplicated "
        f"wording is removed rather than reworded (C-47). found: {hits} in:\n{row}"
    )
    assert "review.md committed" not in _integration_table(), (
        "the old duplicated wording (`review.md committed`) MUST be gone from the "
        "status table"
    )


def test_c47_the_owner_the_row_names_really_holds_the_criteria():
    assert FEATURE_DETAILS.is_file(), f"the owner path does not resolve: {OWNER_PATH}"
    assert OWNER_SECTION in _read(FEATURE_DETAILS), (
        f"the owner section {OWNER_SECTION!r} named by the rows does not exist in "
        f"{OWNER_PATH}"
    )


# --------------------------------------------------------------------------- #
# C-48 — the gate belongs to the transition, not to one command
# --------------------------------------------------------------------------- #

def test_c48_the_checklist_row_is_a_conditional_initiator():
    row = _initiating_row("/speckit.checklist")
    assert TRANSITION in row, "the checklist row MUST still name its transition"
    assert re.search(r"applies only when|after `/speckit.implement`|after implement", row), (
        "the checklist row MUST keep its 'only after implement' annotation — an "
        f"existing pin reads it: {row!r}"
    )
    assert re.search(r"conditional", row, re.I), (
        "the checklist row MUST declare itself a conditional initiator (A-18)"
    )
    after = re.search(r"after[^.;]*", _flat(row), re.I)
    assert after, "the row MUST state what happens after implement"
    assert re.search(r"cites? the same|same owner", _flat(row), re.I), (
        "after implement the checklist initiates the transition and cites the SAME "
        "owner criterion (C-48)"
    )
    assert re.search(r"before[^.;]*implement", _flat(row), re.I), (
        "the row MUST state what happens when it runs before implement: it initiates "
        "nothing (C-48)"
    )
    assert re.search(r"neither? errors?|must not error|manufactur", _flat(row), re.I), (
        "before implement the checklist MUST NOT error for a missing code-segment "
        "conclusion and MUST NOT manufacture one (C-48)"
    )


def test_c48_the_checklist_row_is_a_reference_to_the_same_owner():
    row = _initiating_row("/speckit.checklist")
    assert OWNER_PATH in row and OWNER_SECTION in row, (
        "the checklist row MUST name the same owner section the review row names "
        f"(C-48); got:\n{row}"
    )
    assert re.search(r"not restated", _flat(row)), (
        "the checklist row MUST state that the criteria are not restated (C-48)"
    )


def test_c48_no_initiating_row_carries_its_own_copy_of_the_conditions():
    for command in ("/speckit.review", "/speckit.checklist"):
        row = _initiating_row(command)
        hits = [token for token in CRITERIA_COPY_TOKENS if token.lower() in row.lower()]
        assert not hits, (
            f"{command} MUST cite the owner criterion and MUST NOT carry its own copy "
            f"of the conditions (C-48): found {hits} in:\n{row}"
        )


def test_c48_the_checklist_command_keeps_its_pointer_and_gains_no_criteria():
    body = _read(CHECKLIST_CMD)
    mentions = [line for line in body.splitlines() if TRANSITION in line]
    assert len(mentions) == 1, (
        "the checklist command carries exactly one mention of the transition "
        f"(the third surface C-48 checks), found {len(mentions)}: {mentions}"
    )
    mention = mentions[0]
    assert "Feature Integration Protocol" in mention, (
        "the mention MUST keep its pointer at the integration protocol; got:\n" + mention
    )
    hits = [token for token in CRITERIA_COPY_TOKENS if token.lower() in mention.lower()]
    assert not hits, (
        "the checklist command's mention MUST NOT acquire a criteria copy of its own "
        f"(C-48): found {hits} in:\n{mention}"
    )


# --------------------------------------------------------------------------- #
# C-49 — `important` allows but must be answered; the four lower levels never block
# --------------------------------------------------------------------------- #

def test_c49_important_allows_the_transition_but_must_be_answered():
    block = _owner_block()
    assert re.search(
        r"`important`[^.]{0,200}(allowed|allows|does not block)", _flat(block), re.I
    ), "the owner MUST state that `important` does not block the transition (C-49)"
    assert re.search(
        r"each `important` item[^.]{0,120}answered", _flat(block), re.I
    ), "the owner MUST require each `important` item to be answered (C-49)"


def test_c49_important_only_allows_the_driven_gate(repo: ReviewGitRepo):
    repo.write_record(IMPORTANT_ONLY_RECORD)
    allow = _gate(repo)
    assert allow.returncode == 0, (
        "with only `important` items open and none of them `blocking`, the transition "
        "is allowed (C-49; US4 acceptance scenario 2):\n" + allow.describe()
    )
    assert "important_entries=1" in _plain(allow.stdout) or "1" in _plain(allow.stdout), (
        "the allow run MUST still disclose that an `important` item needs an answer:\n"
        + allow.describe()
    )


def test_c49_the_four_lower_levels_never_block():
    block = _owner_block()
    flat = _flat(block)
    assert re.search(
        r"`suggestion`[^.]{0,60}`nitpick`[^.]{0,60}`question`[^.]{0,60}`praise`[^.]{0,120}never block",
        flat,
    ), (
        "the owner MUST name all four remaining levels and state that none of them "
        "blocks the transition (C-49): the enumeration is closed, so a level cannot "
        "be dropped into the blocking side by omission"
    )


# --------------------------------------------------------------------------- #
# C-50 — no numeric conversion, mapping matrix or unified score
# --------------------------------------------------------------------------- #

def test_c50_no_conversion_matrix_or_unified_score_exists():
    block = _owner_block()
    assert re.search(
        r"(no conversion|never converted|not converted)[^.]{0,160}(mapping|score)", _flat(block), re.I
    ) or (
        _has(block, "no conversion") and _has(block, "unified score")
    ), (
        "the owner MUST forbid a conversion, a mapping matrix and a unified score "
        "between the two families (C-50)"
    )
    surfaces = [FEATURE_DETAILS, FEATURE_INTEGRATION, REVIEW_CMD]
    for path in surfaces:
        for line in _table_rows(_read(path)):
            if _is_separator(line) or _is_prohibition(line):
                continue
            code = _severity_hits(line)
            process = _process_hits(line)
            assert not (code and process), (
                f"{path.relative_to(ROOT)} has a row pairing a process severity with a "
                f"code severity — that row is the mapping matrix C-50 forbids: {line!r}"
            )


def test_c50_no_artifact_of_this_feature_stores_a_mapping():
    body = _read(REVIEW_CMD)
    assert _has(body, "mapping") or _has(body, "conversion"), (
        "the command template MUST state the prohibition in the same place it states "
        "the gate, so the two vocabularies cannot be quietly combined there"
    )
    for line in _table_rows(body):
        if _is_separator(line) or _is_prohibition(line):
            continue
        assert not (_severity_hits(line) and _process_hits(line)), (
            f"the command template may not carry a mapping row: {line!r}"
        )


# --------------------------------------------------------------------------- #
# C-51 — waiver from an explicit user ruling only; halt-and-report when there is none
# --------------------------------------------------------------------------- #

def test_c51_a_waiver_requires_an_explicit_user_ruling():
    block = _owner_block()
    assert _has(block, "explicit user ruling"), (
        "the owner MUST name an explicit user ruling as the only waiver source (C-51)"
    )
    assert re.search(
        r"driver[^.]{0,200}(never|not)[^.]{0,60}user ruling", _flat(block), re.I
    ), (
        "the owner MUST state that a driver's or an orchestrator's confirmation is "
        "never a user ruling (FR-009, A-19)"
    )


def test_c51_the_agent_never_downgrades_merges_or_excludes_a_blocking_entry():
    block = _owner_block()
    assert re.search(
        r"never downgrades?[^.]{0,120}(merges?|exclud)", _flat(block), re.I
    ), (
        "the owner MUST forbid downgrading, merging or excluding a `blocking` entry "
        "inside the gate judgement (C-51)"
    )
    assert re.search(r"absence of objection", _flat(block), re.I), (
        "the owner MUST state that the absence of objection is not a waiver (C-51)"
    )


def test_c51_the_unattended_disposition_is_halt_and_report_with_the_named_literal():
    block = _owner_block()
    assert _has(block, "halt-and-report"), (
        "the unattended disposition MUST be halt-and-report (C-51, A-19)"
    )
    assert REFUSAL_LITERAL in block, (
        f"the owner MUST record the named refusal literal {REFUSAL_LITERAL!r}"
    )
    assert re.search(r"stops? before the transition", _flat(block), re.I), (
        "halt-and-report means the run stops BEFORE the transition (C-51)"
    )
    assert REFUSAL_LITERAL in _cmd_gate_section(), (
        f"the command template's pointer MUST carry the same refusal literal "
        f"{REFUSAL_LITERAL!r}, or the two surfaces disagree on the literal"
    )


def test_c51_the_refusal_literal_has_one_spelling():
    for path in (FEATURE_DETAILS, REVIEW_CMD, FEATURE_INTEGRATION):
        text = _read(path)
        for variant in REFUSAL_VARIANTS:
            assert variant not in text, (
                f"{path.relative_to(ROOT)} carries a variant spelling {variant!r} of "
                f"the refusal literal; the single literal is {REFUSAL_LITERAL!r}"
            )


# --------------------------------------------------------------------------- #
# C-52 — a non-conclusion does not block but is disclosed on both carriers
# --------------------------------------------------------------------------- #

def test_c52_not_applicable_and_not_evaluated_are_disclosed_on_both_carriers():
    block = _owner_block()
    flat = _flat(block)
    for value in ("`not-applicable`", "`not-evaluated`"):
        assert value in flat, (
            f"the owner MUST name {value} as a non-blocking, disclosed verdict (C-52)"
        )
    assert re.search(
        r"`not-applicable`[^.]{0,200}(not block|does not block|never block)", flat, re.I
    ), "neither segment verdict blocks the transition (C-52)"
    for carrier in (CARRIER_REPORT, CARRIER_FEATURE):
        assert carrier in flat, (
            f"the disclosure MUST name the verifiable carrier {carrier!r} (C-52); the "
            "two carriers are the report's code subsection and the review-record entry"
        )


def test_c52_the_closing_summary_carries_no_obligation_of_its_own():
    for surface in (_owner_block(), _cmd_gate_section()):
        assert re.search(
            r"closing summary[^.]{0,200}(no obligation|not an? (third )?carrier)",
            _flat(surface),
            re.I,
        ), (
            "the closing summary is a presentation and carries no obligation of its "
            "own (C-52); a surface that presents it as a third carrier contradicts the "
            "two-carrier rule"
        )


# --------------------------------------------------------------------------- #
# C-53 — a refusal names the failed condition and leaves the status at Implemented
# --------------------------------------------------------------------------- #

def test_c53_a_refusal_names_the_failed_condition():
    block = _flat(_owner_block())
    assert re.search(r"which of the three conditions failed", block, re.I) or re.search(
        r"names the (failed )?condition", block, re.I
    ), "a refusal MUST name the condition that failed, not merely that it refused (C-53)"
    for reason in (
        "blocking` entry in the current",
        "missing review evidence",
        "deferred tasks",
    ):
        assert reason in block, (
            f"the refusal reason MUST enumerate the failing conditions, including "
            f"{reason!r} (C-53)"
        )


def test_c53_the_refused_transition_leaves_the_status_at_implemented():
    block = _flat(_owner_block())
    assert re.search(r"leaves the status at `Implemented`", block, re.I) or re.search(
        r"status[^.]{0,80}(stays|remains|left) at `Implemented`", block, re.I
    ), "a refused transition MUST leave the status at `Implemented` (C-53)"
    assert re.search(
        r"never[^.]{0,120}completed review", block, re.I
    ), (
        "a run that refused MUST NOT present itself as a completed review (C-51/C-53)"
    )


# --------------------------------------------------------------------------- #
# C-54 — one checkpoint, after both segments and both artifacts
# --------------------------------------------------------------------------- #

def test_c54_the_transition_is_judged_once_after_both_segments():
    for name, surface in (
        ("the owner block", _owner_block()),
        ("the command template", _cmd_gate_section()),
    ):
        flat = _flat(surface)
        assert re.search(r"judged once", flat, re.I), (
            f"{name} MUST state that the transition is judged once (C-54)"
        )
        assert re.search(r"after (the )?(process|both)[^.]{0,120}code segment", flat, re.I), (
            f"{name} MUST place the single checkpoint after both segments finished (C-54)"
        )
        assert "must not flip before" in flat.lower() or re.search(
            r"not flip before", flat, re.I
        ), (
            f"{name} MUST forbid an early flip, which C-54 names a violation even when "
            "the process segment already passed"
        )


def test_c54_both_artifacts_are_on_disk_before_the_judgement():
    flat = _flat(_cmd_gate_section()) + " " + _flat(_owner_block())
    for artifact in ("review.md", "code-review.md"):
        assert artifact in flat, (
            f"the checkpoint's inputs include {artifact!r}: the judgement happens after "
            "both artifacts are on disk (C-54)"
        )


def test_c54_the_command_states_no_criterion_of_its_own():
    section = _flat(_cmd_gate_section())
    assert OWNER_PATH in section and OWNER_SECTION in section, (
        "the command template's transition section MUST point at the owner section "
        "rather than stating the criteria (C-45/C-54)"
    )
    for marker in CONDITION_MARKERS:
        assert marker.lower() not in section.lower(), (
            f"the command template MUST NOT restate the condition {marker!r}: it "
            "orchestrates and points (C-45)"
        )
