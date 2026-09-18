"""Contract test: surface-pointers — pointer wiring, content moves, and criteria freeze.

Implements ``.specify/specs/051-user-facing-comprehension/contracts/surface-pointers.md``
**C-1…C-14**. ``test_cN_*`` maps one-to-one onto that file's C-N.

CLAUSE → PHASE PARTITION
------------------------
This file is claimed by three stories' verification rows, which is why the partition is
recorded here rather than left implicit — without it the same file would be required
all-green at two different times, an unsatisfiable pair:

===========  ==========================  =========================================
Story        Turn-green task             Clauses
===========  ==========================  =========================================
US2          T021                        C-2, C-4, C-5
US4          T038                        C-10
US5          T052                        C-1, C-3, C-6…C-9, C-11…C-14
===========  ==========================  =========================================

Green at authoring (freeze assertions — true before any edit, and that is their point):
**C-3, C-4, C-5, C-7, C-14**.

PENDING-PARTITION MECHANISM
---------------------------
A clause whose subject is not built yet carries ``pytest.mark.xfail(strict=True, reason=…)``
naming the task that turns it green, rather than being left to fail outright. Two reasons,
both mechanical:

* ``strict=True`` means that the moment its story lands and the clause passes, pytest
  reports **XPASS as a failure** — so a marker cannot be forgotten, and each story's
  turn-green task is forced to remove it.
* An xfailed case is not a ``FAILED`` line, so GATE-1 ("zero new test failures versus the
  frozen baseline") stays satisfiable at *every* phase boundary from US2 through US5. The
  alternative — letting nine clauses fail and re-freezing the baseline to include them —
  would be undetectable decay: ``comm -13`` only reports *additions*, so a clause absorbed
  into the baseline could stay red forever and no gate would notice.

Pin hygiene: multi-line frozen text is pinned by SHA-256 (C-4's five criteria sections),
single preserved lines by exact literal (C-7, C-10), and derived needle sets carry an
anti-vacuity sentinel so a changed owner document fails loudly instead of silently making
the assertion match nothing (C-12, C-13).
"""
from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
TRUTH_DOC = ROOT / "shared" / "guidelines" / "user-facing-comprehension.md"
POINTER = "shared/guidelines/user-facing-comprehension.md"   # STR-002; STR-001 is its .specify/ twin

CG = ROOT / "shared" / "guidelines" / "confirmation-gates.md"
FEEDBACK = ROOT / "shared" / "workflow" / "feedback-step.md"
INTERVIEW = ROOT / "shared" / "patterns" / "interview-pattern.md"
CLARIFY_CMD = ROOT / "templates" / "commands" / "clarify.md"
REQ_GUIDELINES = ROOT / "shared" / "guidelines" / "requirements-guidelines.md"
PROACTIVE = ROOT / "shared" / "guidelines" / "proactive-trigger.md"
PLAYBOOK = ROOT / "skills" / "summarize-project" / "references" / "reporting-playbook.md"
GLOSSARY = ROOT / "shared" / "workflow" / "glossary.md"
REGEN = ROOT / "scripts" / "python" / "regen-command-copies.py"

# C-1's table: the eight rule sources and the surface classes each covers.
RULE_SOURCES = (
    ("shared/guidelines/confirmation-gates.md", "①②⑩⑪"),
    ("shared/workflow/feedback-step.md", "③"),
    ("shared/patterns/interview-pattern.md", "④"),
    ("templates/commands/clarify.md", "⑤"),
    ("shared/guidelines/requirements-guidelines.md", "⑤⑦"),
    ("shared/guidelines/proactive-trigger.md", "⑥"),
    ("skills/summarize-project/references/reporting-playbook.md", "⑧"),
    ("shared/workflow/glossary.md", "⑨"),
)

# C-4: the five criteria sections of confirmation-gates.md, frozen by hash. Extracted by
# HEADING, not by the contract's pre-change line numbers — T017 inserts a header line above
# them, which shifts every cited line by one, so a line-range extraction would silently
# start hashing the wrong text.
FROZEN_SECTIONS = {
    "两级判据": "089071c2c24bc8e4d8dd2ba10f4f24765f43a34b1fdb70a0d466543e17b2c5bf",
    "破坏性动作清单": "3eda7d3bbae14a675bbe1c39f413cc53c153557544a88003708c3ef88d8391a6",
    "治理保留清单": "92c1c367428a34d038de9c0e85ef37c346dee00d49e7653421e5a64aae91d703",
    "存疑从严": "c1f18db4b9eedf55036cdcb77ef7fd9b41791c4bc292b2d57de346e1744facea",
    "回流约束": "ae1711acd3a325334150051f1193f47631eb043ad336e156b02fa4eca6583af7",
}
GOVERNANCE_KEPT_ROWS = 13   # data rows in 治理保留清单, pinned by C-4

# C-5: the execution-report triad confirmation-gates.md must keep owning.
TRIAD = ("执行内容", "产出/变更工件", "修改途径")

# C-6: the four comprehension rules that must be converged away (matched by their bold lead).
CONVERGED_RULES = (
    "Plain language first",
    "No unexplained abbreviations or jargon",
    "Annotate special terms inline",
    "Never assume shared context",
)
COMPREHENSION_MOUNT = "**Comprehension rules (可理解性规则)**"

# C-7: the two pattern-specific rules preserved verbatim — they are NOT comprehension
# discipline, so the truth document must not swallow them.
PRESERVED_INTERVIEW_RULES = (
    '- **One decision per question.** A question containing "and" usually holds two decisions — split them, and let the dependency edges order them.',
    '- **Ask what, not whether.** "What should happen when X?" invites the user\'s actual model; "Should we do X?" narrows it to yes/no and smuggles in a proposal.',
)

# C-9: the two anti-patterns converged to one short reference.
CONVERGED_ANTIPATTERNS = ("Context-free questions", "Jargon and bare abbreviations")

# C-10: three preserved passages in feedback-step.md (exact literals), and the one line
# that MUST be rewritten. `:115` is deliberately NOT in the preserve set — see the contract's
# B-09 correction: preserving it would contradict its own rewrite obligation.
PRESERVED_FEEDBACK = (
    "`/speckit.feedback package` command — the user-facing path; never paste the raw",
    "Present the choices in user-facing terms: the notification references the",
    "`/speckit.feedback package` command, never the raw `feedback-utils.py` engine path.",
    "(engine detail — do not paste the bare flag into the user-facing line).",
)
REWRITTEN_FEEDBACK_LINE = '(Embedded copies that still say only "invite the user to submit" defer to this section):'

# C-13: content-form restatement needles. These are characteristic literals of the
# **pre-existing dispersed wordings** that US4/US5 converge — NOT literals of the truth
# document's own text. That distinction is load-bearing and was found the hard way: a needle
# set keyed to the owner matched nothing anywhere (the owner's phrasing is brand new), so the
# clause passed vacuously and reported XPASS. Keyed to the dispersed sites it matches 2 files
# before convergence and 0 after.
#
# Deliberately EXCLUDED, because other clauses require them to survive — including them would
# make C-13 contradict C-12 and discipline-doc C-18:
#   * `无内部黑话` / `外部读者不读代码也能看懂` — project-overview.md's landing check (C-12)
#     and class ⑧'s registered reader-baseline override site (C-18(b))
#   * `Written for … stakeholders` — requirements-guidelines.md:24,101, class ⑦'s registered
#     override sites (C-18(b))
#   * the four triad element names — confirmation-gates.md keeps owning them (C-5)
#
# SCOPE LIMIT, stated rather than hidden: this is a **literal** scan. Research measured 38
# dispersed *wordings*, most of which are paraphrases no literal needle can match, and
# FR-033 forbids building a wording scorer to find them. So C-13 pins the
# literally-identifiable restatements to zero; the remaining sites are converged and verified
# individually by C-6/C-9/C-10/C-11 and by T047–T049's own rows.
RESTATED_NEEDLES = (
    # ④ interview-pattern.md — T041 converges the four comprehension rules (C-6) and the two
    # anti-patterns (C-9)
    "Plain language first",
    "No unexplained abbreviations or jargon",
    "Annotate special terms inline",
    "Never assume shared context",
    "Context-free questions",
    "Jargon and bare abbreviations",
    # ③ feedback-step.md — T036 moves the coexistence authority up to the truth source (C-10)
    "defer to this section",
)
SCAN_DIRS = ("shared", "templates", "skills")
# Mechanical copies and generated trees are regenerated, never authored, so they are exempt.
SCAN_EXEMPT = (".specify/", ".claude/", ".github/", ".qoder/", ".opencode/", "docs/public/")


def _text(path: Path) -> str:
    """Unguarded read: a missing artifact must surface as FileNotFoundError, not as an assert."""
    return path.read_text(encoding="utf-8")


def _rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _section(text: str, heading: str) -> str:
    m = re.search(rf"^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    assert m, f"missing H2 section: ## {heading}"
    return m.group(1)


def _pointer_line_count(path: Path) -> int:
    return sum(1 for ln in _text(path).splitlines() if POINTER in ln)


def _scan(needles) -> list[str]:
    """Files under SCAN_DIRS carrying any needle, minus the exempt generated trees."""
    hits = []
    for d in SCAN_DIRS:
        for path in sorted((ROOT / d).rglob("*.md")):
            rel = _rel(path)
            if any(part in rel for part in SCAN_EXEMPT):
                continue
            if path == TRUTH_DOC:
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except OSError:
                continue
            if any(n in content for n in needles):
                hits.append(rel)
    return sorted(set(hits))


# --- C-1: pointer wiring across all eight rule sources (US5 / T052) ---


@pytest.mark.xfail(strict=True, reason="US5/T052 green point — T017/T036/T041-T049 have not inserted the pointers yet")
def test_c1_each_rule_source_carries_exactly_one_pointer_line():
    counts = {rel: _pointer_line_count(ROOT / rel) for rel, _ in RULE_SOURCES}
    wrong = {k: v for k, v in counts.items() if v != 1}
    assert not wrong, (
        f"rule sources whose count of lines containing {POINTER!r} is not exactly 1: {wrong}. "
        "Zero means the pointer is missing; two or more means a second path reference was "
        "added where a path-free reference was required (C-12(b))."
    )


# --- C-2: the confirmation-gates pointer sits in the header ownership area (US2 / T021) ---


def test_c2_confirmation_gates_pointer_is_in_the_header_ownership_area():
    lines = _text(CG).splitlines()
    hits = [i for i, ln in enumerate(lines) if POINTER in ln]
    assert len(hits) == 1, f"expected exactly one pointer line in confirmation-gates.md, got {len(hits)}"
    first_h2 = next((i for i, ln in enumerate(lines) if ln.startswith("## ")), len(lines))
    assert hits[0] < first_h2, (
        f"the pointer is at line {hits[0] + 1}, inside the criteria sections (first H2 at "
        f"line {first_h2 + 1}). It belongs in the header ownership area so that a host "
        "narrowing a criteria section cannot drop it, and one header line must cover all "
        "four classes ①②⑩⑪ rather than four per-section pointers."
    )


# --- C-3: mirror parity for the seven sources that have a .specify/ twin ---


def test_c3_mirrors_are_byte_identical():
    # `templates/commands/` has NO `.specify/` mirror — sync-mirrors.py's templates pair
    # excludes `commands` (retired), and C-14 forbids recreating it. So C-3 covers the seven
    # sources under the `shared` and `skills` pairs; clarify.md's copies are C-14's subject.
    drifted = []
    for rel, _ in RULE_SOURCES:
        if not rel.startswith(("shared/", "skills/")):
            continue
        src, mirror = ROOT / rel, ROOT / ".specify" / rel
        if not mirror.is_file():
            drifted.append(f"{rel}: mirror missing")
        elif src.read_bytes() != mirror.read_bytes():
            drifted.append(f"{rel}: source and mirror differ")
    assert not drifted, f"mirror drift (run sync-mirrors.py --write): {drifted}"


# --- C-4: the five criteria sections are frozen verbatim (US2 / T021) ---


def test_c4_criteria_sections_are_verbatim_frozen():
    text = _text(CG)
    changed = []
    for name, frozen in FROZEN_SECTIONS.items():
        body = _section(text, name)
        digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
        if digest != frozen:
            changed.append(name)
    assert not changed, (
        f"criteria sections were rewritten: {changed}. FR-017 freezes them — this feature "
        "adds a wording obligation beside them, it does not edit the gate criteria. If a "
        "change is genuinely intended, it belongs in a separate constitution-level edit and "
        "these hashes must be re-frozen deliberately, not silently."
    )
    rows = [r for r in _section(text, "治理保留清单").splitlines() if r.strip().startswith("|")]
    data = [r for r in rows if not re.fullmatch(r"[\s|:-]+", r)]
    assert len(data) - 1 == GOVERNANCE_KEPT_ROWS, (
        f"治理保留清单 has {len(data) - 1} data rows, frozen at {GOVERNANCE_KEPT_ROWS}"
    )


# --- C-5: the execution-report triad stays owned by confirmation-gates.md ---


def test_c5_execution_report_triad_still_owned_here():
    body = _section(_text(CG), "执行报告")
    missing = [item for item in TRIAD if item not in body]
    assert not missing, f"execution-report triad elements no longer owned here: {missing}"
    # The other side (the truth document reaches this by path, never by restatement) is
    # discipline-doc C-11's assertion; here we only pin that the triad's home did not move.
    assert "confirmation-gates.md" in _text(TRUTH_DOC), (
        "the truth document must reach the triad by path reference"
    )
    for item in TRIAD:
        assert item not in _section(_text(TRUTH_DOC), "上下文下限"), (
            f"the truth document restates triad element {item!r} instead of referencing it"
        )


# --- C-6…C-9: move A, interview-pattern.md (US5) ---


@pytest.mark.xfail(strict=True, reason="US5/T052 green point — T041 has not converged the four comprehension rules yet")
def test_c6_four_comprehension_rules_converged_to_a_pointer():
    text = _text(INTERVIEW)
    assert COMPREHENSION_MOUNT in text, (
        "the `Comprehension rules` heading MAY be kept as the pointer's mount point; it is gone"
    )
    region = text.split(COMPREHENSION_MOUNT, 1)[1]
    region = region.split("\n## ", 1)[0]
    still = [r for r in CONVERGED_RULES if r in region]
    assert not still, (
        f"comprehension rules still restated in interview-pattern.md: {still}. They belong to "
        "the truth document; this file keeps only the pointer."
    )


def test_c7_two_pattern_specific_rules_preserved_verbatim():
    text = _text(INTERVIEW)
    missing = [r for r in PRESERVED_INTERVIEW_RULES if r not in text]
    assert not missing, (
        f"pattern-specific rules were dropped or reworded: {[m[:60] for m in missing]}. "
        "One-decision-per-question and ask-what-not-whether are interview *pattern* rules, "
        "not comprehension discipline — C-7 forbids the truth document swallowing them."
    )


@pytest.mark.xfail(strict=True, reason="US5/T052 green point — T041 has not extended the non-droppable list yet")
def test_c8_embed_contract_nondroppable_list_includes_the_pointer():
    text = _text(INTERVIEW)
    m = re.search(r"A host may \*\*narrow\*\* the pattern[^\n]*", text)
    assert m, "the host-narrowing clause (the embed contract's non-droppable list) is gone"
    clause = m.group(0)
    assert re.search(r"comprehension|可理解性|pointer|指针", clause, re.I), (
        "the non-droppable list does not name the comprehension pointer. Measured at authoring "
        "time it lists write-through, persisted decision records, retraction propagation, the "
        "open-question format, the fact/decision split and the user-exit gate — but not this "
        "pointer, so a host narrowing the pattern could drop it legitimately."
    )


@pytest.mark.xfail(strict=True, reason="US5/T052 green point — T041 has not converged the two anti-patterns yet")
def test_c9_two_anti_patterns_converged_to_one_short_reference():
    text = _text(INTERVIEW)
    present = [a for a in CONVERGED_ANTIPATTERNS if a in text]
    assert len(present) <= 0, (
        f"anti-patterns still carrying their original condition restatement: {present}. "
        "C-9 requires one short reference to the truth document's blacklist/floor instead."
    )


# --- C-10: move B, feedback-step.md (US4 / T038) ---


def test_c10_feedback_step_preserves_three_and_rewrites_one():
    text = _text(FEEDBACK)
    # Preserve half: three passages (four literals) must survive verbatim.
    dropped = [p for p in PRESERVED_FEEDBACK if p not in text]
    assert not dropped, (
        f"passages that MUST be preserved verbatim were dropped or reworded: "
        f"{[d[:60] for d in dropped]}. FR-019 keeps them as class ③ instances of the "
        "discipline, not as a second rule set."
    )
    # Rewrite half: the coexistence authority must have moved up to the discipline's truth
    # source. The original line asserted this section wins; that claim is what C-10 removes.
    assert REWRITTEN_FEEDBACK_LINE not in text, (
        "the coexistence-authority line still says embedded copies defer to *this section*. "
        "C-10's rewrite obligation moves that authority to the discipline's truth source; the "
        "line is deliberately NOT in the preserve set (contract B-09 correction) — preserving "
        "it would contradict the rewrite."
    )
    assert _pointer_line_count(FEEDBACK) == 1, (
        "feedback-step.md must carry exactly one pointer line covering surface class ③"
    )


# --- C-11…C-12: move C, summarize-project (US5) ---


@pytest.mark.xfail(strict=True, reason="US5/T052 green point — T046 has not converged §1.7 nor promoted the blacklist yet")
def test_c11_playbook_section_converged_and_blacklist_promoted():
    text = _text(PLAYBOOK)
    m = re.search(r"^### 1\.7 .*$", text, re.M)
    assert m, "§1.7's heading is gone — C-11 converges its body to a pointer, it does not delete the section"
    body = text.split(m.group(0), 1)[1].split("\n### ", 1)[0].split("\n## ", 1)[0]
    identifiers = re.findall(r"`(?:T1|E1|RC-\d|RC-\*|CG-[A-Z0-9]|CG-\*|M-\*)[^`]*`", body)
    assert not identifiers, (
        f"§1.7 still enumerates internal identifiers: {identifiers[:6]}. The enumeration MUST be "
        "promoted into the truth document's blacklist section and left here as a pointer."
    )
    # The promoted half: the truth document's blacklist must now carry the identifier classes.
    bl = _section(_text(TRUTH_DOC), "禁用行话(黑名单)")
    assert re.search(r"RC-|CG-|T1|E1", bl), (
        "the truth document's blacklist does not carry the promoted identifier classes — "
        "C-11 is a two-sided obligation (converge here, promote there)."
    )


def _blacklist_identifier_needles() -> list[str]:
    """Identifier literals derived from the truth document's blacklist section.

    Derived rather than hard-coded: C-12(c) requires the needle to come from the truth
    document's own category literals, and T046 is what puts them there. Deriving means the
    needle strengthens automatically when the promotion lands.
    """
    bl = _section(_text(TRUTH_DOC), "禁用行话(黑名单)")
    return sorted(set(re.findall(r"`(?:T1|E1|RC-\d|RC-\*|CG-[A-Z0-9]|CG-\*|M-\*)[^`]*`", bl)))


@pytest.mark.xfail(strict=True, reason="US5/T052 green point — T046's promotion has not landed, so the derived needle set is still empty")
def test_c12_no_independent_blacklist_copy():
    needles = _blacklist_identifier_needles()
    # Anti-vacuity sentinel: an empty needle set would make the count below trivially zero
    # and prove nothing. This is what makes the clause falsifiable per C-12(c).
    assert needles, (
        "the truth document's blacklist carries no identifier literals yet, so there is no "
        "needle to scan with — T046's promotion must land first"
    )
    hits = _scan(needles)
    assert not hits, (
        f"independent blacklist copies outside the truth document: {hits}. C-12(a): a text MAY "
        "name the blacklist for a landing check but MUST NOT restate its category enumeration; "
        "C-12(b): that reference MUST be path-free so the file keeps exactly one pointer line."
    )
    # The two landing checks C-12 requires to survive (they are checks, not definitions).
    pb = _text(PLAYBOOK).splitlines()
    assert any("读者用语纪律已过" in ln for ln in pb), (
        "reporting-playbook.md's landing-gate checklist item was deleted — C-12 requires it kept"
    )
    po = _text(ROOT / "skills" / "summarize-project" / "references" / "project-overview.md")
    assert "无内部黑话" in po and "外部读者不读代码也能看懂" in po, (
        "project-overview.md's landing check was deleted — C-12 requires it kept"
    )


# --- C-13: single-source scan (US5) ---


@pytest.mark.xfail(strict=True, reason="US5/T052 green point — T036/T041 have not converged the dispersed wordings yet (2 files match today)")
def test_c13_no_content_form_restatement():
    # Anti-vacuity: the needle set must not have been emptied. A runtime "needle must match
    # something" sentinel is impossible here — after convergence matching nothing IS the pass
    # condition. The falsifiability proof is the recorded pre-conversion measurement instead
    # (notes/red-first-evidence.md, US2 section: 2 files / 7 needles), per C-12(c)'s rule that
    # a needle's effectiveness is proven by its hit count before the rewrite, not after.
    assert RESTATED_NEEDLES, "the needle set was emptied — this clause would pass vacuously"
    hits = _scan(RESTATED_NEEDLES)
    assert not hits, (
        f"content-form restatements of the discipline's rules: {hits}. A summary pointer is "
        "fine; restating the condition set is a copy (FR-031 / SC-003)."
    )


# --- C-14: per-tool copy trees regenerated, retired mirror not recreated ---


def test_c14_per_tool_copies_regenerated_and_retired_mirror_absent():
    proc = subprocess.run(
        ["python3", str(REGEN), "--check"], cwd=ROOT, capture_output=True, text=True
    )
    assert proc.returncode == 0, (
        f"regen-command-copies.py --check exited {proc.returncode} — the four per-tool trees "
        f"are out of sync with templates/commands/: {proc.stdout[-400:]}"
    )
    retired = ROOT / ".specify" / "templates" / "commands"
    assert not retired.exists(), (
        ".specify/templates/commands/ was recreated. That mirror is retired (sync-mirrors.py's "
        "templates pair excludes `commands`); C-14 forbids resurrecting it."
    )
