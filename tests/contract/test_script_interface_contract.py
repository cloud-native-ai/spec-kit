"""Contract test: the script-interface rule's governance landings.

Implements ``.specify/specs/089-script-interface-contract/contracts/governance-landing.contract.md``
**C-23 … C-30**, plus the C-21 owner-page half that the page's own declaration makes checkable.
``test_cN_*`` maps one-to-one onto that file's ``## C-N``.

The defect this file exists to prevent is the *rule that reaches a reader as prose in five
places and as fact nowhere*: the four mandatory help-content labels and the classification step
list have exactly one owner (``shared/definitions/script-interface-definitions.md``), and every
other landing carries a summary plus that path. A landing that restates the labels does not
merely duplicate them — it forks them, and the fork is invisible until the two copies disagree.

Four deliberate design constraints:

* **The owner page is READ, never re-declared.** Every set this file compares against (the
  banned-literal list, the four label names, the exemption-table columns) is grepped back out of
  the page at assertion time. A second hand-typed list would be the very defect the file guards.
* **No numeral is ever pinned.** The template roster and the live roster are different sizes and
  either can grow; a matcher keyed to ``### XX.`` misfires the day a principle is inserted
  above it. Titles are matched by name.
* **Set membership, never substring containment.** ``Script Interface Contract`` and
  ``Script Interface Contract (Declared, Zero-Side-Effect)`` share a prefix; a containment test
  would silently merge them, so the title matchers extract whole heading texts.
* **The house shape is the sibling guard's, not a re-invention.** C-24 says "the house shape
  *already asserted* for every principle in that file"; the owner of that judgement is
  ``tests/contract/test_constitution_double_landing.py::_check_structure``, which this file
  imports and runs rather than copying.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from script_api import run_engine_in_process

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]

# --- the five landing surfaces (C-29's closed scan set) --------------------------------
OWNER = ROOT / "shared" / "definitions" / "script-interface-definitions.md"
OWNER_MIRROR = ROOT / ".specify" / "shared" / "definitions" / "script-interface-definitions.md"
TEMPLATE = ROOT / "templates" / "constitution-template.md"
LIVE = ROOT / ".specify" / "constitution.md"
INSTRUCTIONS_TEMPLATE = ROOT / "templates" / "instructions-template.md"
INSTRUCTIONS_LIVE = ROOT / ".specify" / "instructions.md"
SKILL = ROOT / "skills" / "internal" / "manage-constitution" / "SKILL.md"

# The five surfaces C-29 forbids from carrying the banned literals.
LANDING_SURFACES = (
    TEMPLATE,
    INSTRUCTIONS_TEMPLATE,
    LIVE,
    INSTRUCTIONS_LIVE,
    SKILL,
)

# --- the rule's own nouns (C-24 / C-25 / C-26 / C-27) ---------------------------------
PRINCIPLE_TITLE = "Script Interface Contract (Declared, Zero-Side-Effect)"
AMBIENT_HEADING = "Script Interface Contract"

# C-27: the forms an ambient section may never carry — they are invocation syntax, not
# documentation, and one of them turns an instruction file into a command.
INVOCATION_FORMS = ("--action", "$ARGUMENTS")

# C-24: the template's numbered-principle roster, numeral-agnostic.
TEMPLATE_TITLE_RE = re.compile(r"^### ([IVXLC0-9]+)\. (.+)$", re.M)
# C-26: the generator skill's uniform mandate sub-entry form.
SKILL_ENTRY_RE = re.compile(r"^  - \*\*(.+?)\*\* —", re.M)


# ======================================================================================
# helpers
# ======================================================================================


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _flat(text: str) -> str:
    """Collapse whitespace so a phrase hard-wrapped across lines still matches.

    The house shape requires lines under 100 chars, which necessarily breaks fixed phrases
    such as ``.specify/shared/definitions/...`` or a colon-ended claim across a newline.
    Phrase assertions run on the flattened form; structural ones (line length, blank-line
    placement) run on the raw one.
    """
    return re.sub(r"\s+", " ", text)


def _principle_block(text: str, title: str) -> str:
    """One principle's block: its heading line plus body up to the next `### ` or `## `."""
    m = re.search(
        rf"^### [IVXLC0-9]+\. {re.escape(title)}\s*$(.*?)(?=^### |^## |\Z)",
        text, re.M | re.S,
    )
    assert m, f"principle {title!r} not found on this surface"
    return m.group(0)


def _principle_titles(text: str) -> list[str]:
    return [m.group(2).strip() for m in TEMPLATE_TITLE_RE.finditer(text)]


def _section(text: str, heading: str) -> str:
    """One `## ` section's body: everything up to the next `## ` (or EOF)."""
    m = re.search(
        rf"^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S
    )
    assert m, f"section {heading!r} not found on this surface"
    return m.group(1)


def _sections_h2(text: str) -> list[str]:
    return re.findall(r"^## (.+)$", text, re.M)


def _sentences(body: str) -> list[str]:
    """Split a markdown body into sentences, ignoring hard-wrap newlines.

    A bulleted block is excluded from the count by the caller: C-27's ceiling is on the
    summary *prose*, and a section that carries no bullets has exactly the prose to measure.
    """
    flat = _flat(body)
    return [s for s in re.split(r"(?<=[.!?])\s+", flat) if s.strip()]


def _load_sibling_guard():
    """Import the double-landing guard, whose ``_check_structure`` owns C-24's house shape.

    Loaded by path (the ``tests/contract`` directory is not a package on ``sys.path``) so the
    import cannot resolve to a same-named module elsewhere, and so an import failure is a
    loud red rather than a silent skip.
    """
    import importlib.util

    path = ROOT / "tests" / "contract" / "test_constitution_double_landing.py"
    assert path.is_file(), f"the house-shape owner disappeared: {path}"
    spec = importlib.util.spec_from_file_location("_sibling_double_landing_086", path)
    assert spec is not None and spec.loader is not None, "cannot load the sibling guard"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --- C-23: the owner page declares itself and names the five things it owns --------------


OPENING_ITEM_COUNT = 5  # C-23: exactly five owned items, named in the page's opening block

OWNED_ITEM_ANCHORS = (
    # (label, regex over the page's opening block)
    ("candidate and classification rule", r"候选面如何派生|判定对象与分类"),
    ("mandatory flags and their content", r"必备标志及其必备内容|必备标志与必备内容"),
    ("zero-side-effect boundary", r"零副作用边界"),
    ("unrecognized-option rejection", r"未知选项的拒绝"),
    ("exemption criteria and register", r"豁免判据与已声明例外登记|Declared Exceptions"),
)


def test_c23_owner_page_declares_itself_the_single_source():
    assert OWNER.is_file(), (
        f"the owner page is missing: {OWNER.relative_to(ROOT)} — the whole pointer discipline "
        "has nothing to point at"
    )
    text = _text(OWNER)
    # The opening block, before the first `---` rule: the declaration must be the first thing
    # a reader meets, not a footnote at the bottom that happens to be greppable.
    opening = text.split("\n---\n", 1)[0]
    assert re.search(r"唯一真源|single source of truth|single owner", opening, re.I), (
        "the owner page must open by declaring itself the single source of truth"
    )
    assert len(OWNED_ITEM_ANCHORS) == OPENING_ITEM_COUNT, (
        "C-23 fixes exactly five owned items; this guard's own anchor list moved"
    )
    missing = [
        label for label, pattern in OWNED_ITEM_ANCHORS
        if not re.search(pattern, opening)
    ]
    assert not missing, (
        f"the owner page lists {OPENING_ITEM_COUNT - len(missing)} of {OPENING_ITEM_COUNT} owned "
        f"items at the top; missing: {missing}"
    )
    # C-23: the register is the page's LAST CORE section — "ends with `## Declared Exceptions`"
    # means nothing follows the five owned items, not that the file may carry no closing
    # apparatus. The owner page's own `## 本文档不拥有什么` after the register is that apparatus
    # (a scope disclaimer, not a sixth owned item), so the assertion is: the register is the
    # last of the five owned sections, and nothing else in the file introduces another one.
    sections = _sections_h2(text)
    assert sections.count("Declared Exceptions") == 1, (
        "the owner page carries `## Declared Exceptions` more than once"
    )
    register_idx = sections.index("Declared Exceptions")
    tail = sections[register_idx + 1:]
    # The apparatus after the register (projection declaration, consumer table, scope
    # disclaimer) is the page's own structure and C-23 does not forbid it. What C-23 forbids is
    # a sixth owned item after the register, so the assertion is scoped: the register sits among
    # the owned sections (index 5 of 7 today), never ahead of one, and no heading after it
    # introduces another owned item.
    assert register_idx == 4, (
        "C-23: `## Declared Exceptions` is the FIFTH of the page's five owned items, so it "
        f"closes the owned block; it sits at index {register_idx} of {sections}"
    )
    assert not [h for h in tail if h.startswith("Declared")], tail
    # And its mirror is byte-identical (C-23's second sentence).
    assert OWNER_MIRROR.is_file(), f"the mirror is missing: {OWNER_MIRROR.relative_to(ROOT)}"
    assert OWNER_MIRROR.read_bytes() == OWNER.read_bytes(), (
        "the owner page's mirror is not byte-identical — "
        "`.specify/shared/definitions/script-interface-definitions.md` is generated by "
        "`sync-mirrors.py` and must never be hand-edited"
    )


# --- C-24: the template principle ---------------------------------------------------------


def test_c24_template_carries_the_principle_with_the_house_shape():
    assert TEMPLATE.is_file(), f"missing: {TEMPLATE.relative_to(ROOT)}"
    text = _text(TEMPLATE)
    titles = _principle_titles(text)
    assert PRINCIPLE_TITLE in titles, (
        f"`templates/constitution-template.md` carries no principle titled {PRINCIPLE_TITLE!r}; "
        f"titles present: {titles[-3:]}"
    )
    assert titles.count(PRINCIPLE_TITLE) == 1, (
        f"{PRINCIPLE_TITLE!r} appears {titles.count(PRINCIPLE_TITLE)} times in the template roster"
    )
    block = _principle_block(text, PRINCIPLE_TITLE)

    # C-24: "the house shape already asserted for every principle in that file" — that
    # judgement's owner is the sibling guard, imported rather than re-implemented.
    _load_sibling_guard()._check_structure(block, PRINCIPLE_TITLE)

    # C-24's own two additional obligations, stated in the clause rather than in the house shape.
    assert not re.search(r"\[[A-Z_]{3,}\]", block), (
        f"{PRINCIPLE_TITLE}: an unresolved `[UPPER_SNAKE_CASE]` placeholder is left in the block"
    )
    long_lines = [ln for ln in block.splitlines() if len(ln) >= 100]
    assert not long_lines, (
        f"{PRINCIPLE_TITLE}: {len(long_lines)} line(s) reach 100 chars; the house shape hard-wraps"
    )


def test_c24_template_principle_points_at_the_owner_and_does_not_copy_its_steps():
    text = _text(TEMPLATE)
    block = _principle_block(text, PRINCIPLE_TITLE)
    flat = _flat(block)
    # The pointer. The template ships downstream, so it names the downstream-resolved path.
    assert ".specify/shared/definitions/script-interface-definitions.md" in flat, (
        f"{PRINCIPLE_TITLE}: the principle must name the owner page's path; a summary with no "
        "pointer leaves the reader nowhere to go"
    )
    # C-29's substance, asserted here as the C-24 limb that owns it for THIS surface: the
    # classification steps live on the owner page only.
    for literal in _owner_banned_forms():
        assert literal not in flat, (
            f"{PRINCIPLE_TITLE}: the template principle reproduces the owner page's "
            f"{literal!r} — C-24 requires a pointer, not a copy of the steps"
        )


# --- C-25: the live principle -------------------------------------------------------------


def test_c25_live_constitution_carries_the_principle():
    assert LIVE.is_file(), f"missing: {LIVE.relative_to(ROOT)}"
    text = _text(LIVE)
    titles = _principle_titles(text)
    assert PRINCIPLE_TITLE in titles, (
        f".specify/constitution.md carries no principle titled {PRINCIPLE_TITLE!r}; "
        f"titles present: {titles[-3:]}"
    )
    assert titles.count(PRINCIPLE_TITLE) == 1, (
        f"{PRINCIPLE_TITLE!r} appears {titles.count(PRINCIPLE_TITLE)} times in the live roster"
    )
    # Numeral-agnostic: the roster position is read, never pinned, and the two rosters are
    # allowed to differ (the live constitution numbers its own principles).
    assert not re.search(r"\b(XX|XIX|XVIII)\b", TEMPLATE_TITLE_RE.pattern), (
        f"the title matcher pins a numeral value: {TEMPLATE_TITLE_RE.pattern}"
    )
    assert re.search(r"\[IVXLC0-9\]\+", TEMPLATE_TITLE_RE.pattern), (
        "the title matcher must accept any numeral (roman or arabic), never a fixed set"
    )
    block = _principle_block(text, PRINCIPLE_TITLE)
    _load_sibling_guard()._check_structure(block, PRINCIPLE_TITLE)


def test_c25_amendment_carries_sync_report_minor_bump_and_last_amended():
    text = _text(LIVE)
    head = "\n".join(text.splitlines()[:40])
    assert "Sync Impact Report" in head, (
        "the amendment must prepend a Sync Impact Report block at the top of the file"
    )
    assert re.search(r"Version change:\s*\d+\.\d+\.\d+\s*(?:→|->)\s*\d+\.\d+\.\d+", head), (
        "the Sync Impact Report must state the version change"
    )
    # The report must name THIS amendment's principle; a fixed older title alone would let any
    # later amendment pass without naming its own subject. Stale-oracle repair (2026-11-10,
    # Feature 099 T014): the report history is append-only and later amendments prepend their own
    # blocks, so the 089 block no longer sits inside the fixed 40-line window (the same repair
    # `test_constitution_double_landing.py` C-12 already records for the 051 block). Locate the
    # 089 block by its own version change — the subject stays "this amendment's report names its
    # own principle", only the locator moves off a line count.
    reports = re.findall(r"<!--\s*\nSync Impact Report\n(.*?)-->", text, re.S)
    assert reports, "no Sync Impact Report block was found in the live constitution"
    own = [r for r in reports if re.search(r"1\.17\.0\s*(?:→|->)\s*1\.18\.0", r)]
    assert len(own) == 1, (
        "the 089 amendment's Sync Impact Report block (Version change: 1.17.0 → 1.18.0) is "
        "missing or duplicated"
    )
    assert AMBIENT_HEADING in own[0], (
        f"the Sync Impact Report must name the principle THIS amendment added "
        f"({PRINCIPLE_TITLE!r}); the 089 block names none of it"
    )

    m = re.search(r"^\*\*Version\*\*:\s*(\d+)\.(\d+)\.(\d+)", text, re.M)
    assert m, "no `**Version**:` line found in the live constitution"
    got = tuple(int(g) for g in m.groups())
    # A new principle is a MINOR bump: floor (1, 17, 0) — additive, never an equality pin, so a
    # later MAJOR amendment does not have to edit this guard.
    assert got >= (1, 17, 0), (
        f"constitution version {'.'.join(map(str, got))} is below (1, 17, 0): adding a principle "
        "is a MINOR bump, so the amendment must reach at least 1.17.0"
    )
    amended = re.search(r"\*\*Last Amended\*\*:\s*(\d{4}-\d{2}-\d{2})", text)
    assert amended, "no `**Last Amended**: YYYY-MM-DD` on the live constitution"
    assert amended.group(1) >= "2026-11-06", (
        f"`Last Amended` reads {amended.group(1)}; the amendment cannot predate the change"
    )


# --- C-26: the mandate-list entry ----------------------------------------------------------


def _must_include_block(text: str) -> str:
    """The generator skill's mandatory-principles block: the top-level `- **MUST include**`
    bullet plus its indented sub-entries, ending at the next top-level bullet."""
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.startswith("- **MUST include**"):
            start = i
            break
    assert start is not None, (
        "manage-constitution SKILL.md lost its `- **MUST include**` mandatory-principles block"
    )
    body = []
    for ln in lines[start + 1:]:
        if ln.startswith("- "):
            break
        body.append(ln)
    return "\n".join([lines[start]] + body)


def test_c26_generator_skill_carries_the_mandate_entry():
    assert SKILL.is_file(), f"missing: {SKILL.relative_to(ROOT)}"
    block = _must_include_block(_text(SKILL))
    names = [m.group(1).strip() for m in SKILL_ENTRY_RE.finditer(block)]
    assert PRINCIPLE_TITLE in names, (
        f"the `- **MUST include**` block carries no {PRINCIPLE_TITLE!r} sub-entry; entries: "
        f"{names[-3:]}"
    )
    assert len(names) == 14, (
        f"the mandate list holds {len(names)} entries after the landing; expected 14 "
        "(13 after 089 + 090's Re-Anchoring entry). A count that stays behind is how the "
        "guard goes red on nothing"
    )
    # The uniform sub-entry form C-26 fixes, plus its two content obligations.
    m = re.search(
        rf"^  - \*\*{re.escape(PRINCIPLE_TITLE)}\*\* —.*?(?=^  - \*\*|^- |\Z)", block, re.M | re.S
    )
    assert m, f"the entry for {PRINCIPLE_TITLE!r} is not in the mandate list's uniform form"
    entry = _flat(m.group(0))
    assert ".specify/shared/definitions/script-interface-definitions.md" in entry, (
        f"{PRINCIPLE_TITLE}: the mandate entry must name the owner path"
    )
    assert re.search(r"referenced, not restated|referenced, never restated", entry), (
        f"{PRINCIPLE_TITLE}: the mandate entry must carry the referenced-not-restated rule"
    )


# --- C-27: the ambient section -------------------------------------------------------------


def _ambient_body_problems(body: str) -> list[str]:
    """Every way one ambient section body can fail C-27, as human-readable reasons."""
    problems = []
    for form in INVOCATION_FORMS:
        if form in body:
            problems.append(f"carries the engine-invocation form {form!r}")
    if re.search(r"<[A-Za-z][A-Za-z0-9 _-]*>", body):
        problems.append("carries an `<placeholder>` form")
    if re.search(r"^[-*] ", body, re.M):
        problems.append("carries a bullet list; C-27 allows a summary of at most two sentences")
    sentences = _sentences(body)
    if len(sentences) > 2:
        problems.append(
            f"states {len(sentences)} sentences; the ceiling is 2 summary sentences"
        )
    if ".specify/shared/definitions/script-interface-definitions.md" not in _flat(body):
        problems.append("does not carry the owner path")
    return problems


@pytest.mark.parametrize(
    "path", [INSTRUCTIONS_TEMPLATE, INSTRUCTIONS_LIVE], ids=["template", "live"]
)
def test_c27_ambient_section_shape(path):
    assert path.is_file(), f"missing: {path.relative_to(ROOT)}"
    text = _text(path)
    headings = _sections_h2(text)
    assert headings.count(AMBIENT_HEADING) == 1, (
        f"{path.relative_to(ROOT)} carries the `## {AMBIENT_HEADING}` heading "
        f"{headings.count(AMBIENT_HEADING)} times; expected exactly one"
    )
    body = _section(text, AMBIENT_HEADING)
    problems = _ambient_body_problems(body)
    assert not problems, (
        f"{path.relative_to(ROOT)} `## {AMBIENT_HEADING}`: " + "; ".join(problems)
    )


def test_c27_template_and_live_ambient_bodies_agree():
    """C-27's second sentence: the live file carries "the same body, produced by the
    reconcile". Whitespace is normalised, because the reconcile may re-wrap."""
    tpl = _flat(_section(_text(INSTRUCTIONS_TEMPLATE), AMBIENT_HEADING)).strip()
    live = _flat(_section(_text(INSTRUCTIONS_LIVE), AMBIENT_HEADING)).strip()
    assert tpl == live, (
        "the ambient section's body differs between `templates/instructions-template.md` and "
        "`.specify/instructions.md`; the live file is produced by the instructions reconcile and "
        "must never be hand-written"
    )


# --- C-29: pointer discipline, the banned-literal list read OUT of the page ----------------


# The owner page publishes its four help-content labels as one parenthesised group: the
# sentence `必备内容标签的闭集是:…` introduces them and the four backticked tokens follow. The
# group is HARD-WRAPPED (the page keeps its lines under the house width), so the sentence's
# remainder lives on the following line; the guard therefore reads from the sentence to the
# next blank line — the end of that paragraph — and never types the four names.
LABEL_LINE_RE = re.compile(r"必备内容标签的闭集是[^\n]*(?:\n(?!\s*\n)[^\n]*)*")
CLASSIFICATION_STEPS_HEADING = "### 1.4 分类步骤"


# The page also fixes the scan's matching UNIT: a label is banned in its complete form (the
# label followed by its printed value), never as a bare ordinary word. The guard reads that
# form template out of the page instead of typing it, so the page stays the owner of what
# "restating a label" means. Measured cause (086 package 2b): the bare word collides with
# pre-existing downstream prose — `Presenting options that are incomplete or incorrect` in the
# constitution template and `token usage efficiency` in the instructions template — neither of
# which restates this page's list, so a bare-word scan reports leaks that are not leaks.
BANNED_FORM_TEMPLATE = "`{0}` 标签"


def _owner_label_line() -> str:
    text = _text(OWNER)
    matches = LABEL_LINE_RE.findall(text)
    assert len(matches) == 1, (
        f"the owner page must publish its four help-content labels in exactly one paragraph; "
        f"found {len(matches)} — the guard reads the list out of the page, so a page that "
        "stopped publishing it leaves the scan with nothing to compare against"
    )
    return matches[0]


def _owner_banned_forms() -> tuple[str, ...]:
    """C-29's banned-literal list, read out of the owner page.

    The unit of the scan is the **complete label form** the page publishes, never a bare
    ordinary word. The page states this itself (`## 2.` carries the rule: 匹配单位是完整标签,
    不是单词), because the bare word collides with ordinary prose on the surfaces that ship
    downstream — `Presenting options that are incomplete …` is a principle about decision
    quality, `token usage efficiency` is an efficiency discipline, and neither restates this
    page's label list. Scanning for the bare word therefore reports a leak that is not one, so
    a guard keyed to it goes red on prose it was never written to judge.

    Two things are read back and neither is typed: the four label forms (from the closed-set
    sentence's backticked tokens plus the page's published form template) and the
    classification rule's step heading. Nothing here has to be edited when the page's wording
    changes — but the page MUST keep publishing both, or the assertions below go red.
    """
    # The sentence's own follow-on clause names the JSON key `labels`; the four labels are the
    # names SHAPED like a help-content label, and the emitted-rule key is the datum excluded.
    emitted_rule_key = "labels"
    label_tokens = tuple(
        name for name in re.findall(r"`([a-z][a-z-]*)`", _owner_label_line())
        if name != emitted_rule_key
    )
    assert len(label_tokens) == 4, (
        f"the owner page's label sentence yields {len(label_tokens)} backticked labels, expected "
        f"4 ({label_tokens}) — the banned-literal list is read out of the page, so the page's "
        "own publishing form is a precondition of this guard"
    )
    page = _text(OWNER)
    assert BANNED_FORM_TEMPLATE in _flat(page), (
        f"the owner page no longer publishes its matching-unit template {BANNED_FORM_TEMPLATE!r} "
        "— the scan reads the form out of the page, so a page that stopped publishing it leaves "
        "this guard comparing against an invented form"
    )
    forms = tuple(
        BANNED_FORM_TEMPLATE.format(label) for label in label_tokens
    ) + (CLASSIFICATION_STEPS_HEADING,)
    steps = re.findall(rf"^{re.escape(CLASSIFICATION_STEPS_HEADING)}\s*$", page, re.M)
    assert steps, f"the owner page no longer carries {CLASSIFICATION_STEPS_HEADING!r}"
    return forms


def test_c29_banned_literal_list_is_read_out_of_the_owner_page():
    literals = _owner_banned_forms()
    assert len(literals) == 5, (
        f"the banned-literal list reads {len(literals)} items ({literals}); expected the four "
        "help-content label forms plus the classification steps heading"
    )
    # Anti-vacuity: the list is genuinely derived, not an empty tuple that makes the scan below
    # pass for every surface. Each form must carry a label the owner page really publishes.
    owner = _text(OWNER)
    for literal in literals:
        probe = literal if literal == CLASSIFICATION_STEPS_HEADING else literal.strip("`").split("`")[0]
        assert probe in owner, f"the derived literal {literal!r} is not on the owner page"


def test_c29_no_landing_surface_carries_the_banned_literals():
    literals = _owner_banned_forms()
    leaks = []
    for path in LANDING_SURFACES:
        assert path.is_file(), f"landing surface missing: {path.relative_to(ROOT)}"
        text = _text(path)
        hits = [lit for lit in literals if lit in text]
        if hits:
            leaks.append((path.relative_to(ROOT).as_posix(), hits))
    assert not leaks, (
        "C-29: these landings restate the owner page's own list instead of pointing at it: "
        + "; ".join(f"{p} -> {h}" for p, h in leaks)
    )


def test_c29_the_four_labels_appear_on_the_owner_page_and_nowhere_else():
    """The four labels are the page's closed set; a landing that loses its pointer while
    keeping a label would pass the scan above trivially, so the pointer is asserted too."""
    forms = _owner_banned_forms()[:4]
    labels = [f.strip("`").split("`")[0] for f in forms]
    owner = _text(OWNER)
    assert all(lit in owner for lit in labels), "the owner page lost one of its own labels"
    flat_refs = [
        p for p in LANDING_SURFACES
        if ".specify/shared/definitions/script-interface-definitions.md" in _flat(_text(p))
    ]
    # The two constitution surfaces reach the owner through the constitution's own pointer
    # discipline; the instructions surfaces and the generator skill name the path directly.
    assert len(flat_refs) >= 4, (
        "C-29: a landing that carries neither a label nor the owner path is not a pointer — "
        f"only {len(flat_refs)} of {len(LANDING_SURFACES)} landings name the owner path"
    )


# --- C-30: the exemption register agrees with the checker's payload, row for row ----------


EXCEPTION_COLUMNS = ("path", "skill", "unsatisfied clause", "handling")
CHECKER = ROOT / "scripts" / "python" / "script-interface-check.py"


def _owner_exception_rows() -> list[list[str]]:
    """The owner page's `## Declared Exceptions` table, as a list of cell lists."""
    body = _section(_text(OWNER), "Declared Exceptions")
    rows = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            continue  # the alignment row
        rows.append(cells)
    assert rows, "the `## Declared Exceptions` section carries no table"
    header, data = rows[0], rows[1:]
    assert tuple(header) == EXCEPTION_COLUMNS, (
        f"the exception table's columns are {header}; C-30 fixes {list(EXCEPTION_COLUMNS)}"
    )
    # The `none` placeholder is the table's way of saying "this register is empty"; it is not a
    # declared script and MUST NOT be compared against the checker's recomputation as though it
    # were one. `test_c30_exception_table_shape_and_empty_state` is where it is checked.
    if len(data) == 1 and data[0][0] == "none":
        return []
    return data


def _checker_exceptions_payload() -> list[dict]:
    """Run the checker with `--json --emit-rule` and read the `exceptions` payload.

    `--emit-rule` is the one mode that answers without probing 700+ candidates, and C-21 fixes
    its `exceptions` key; the register itself is the owner page's, so this is the checker's
    recomputation of it rather than a second copy.
    """
    import json
    import subprocess
    import sys

    assert CHECKER.is_file(), (
        f"the checker is missing: {CHECKER.relative_to(ROOT)} — T032/T045 have not landed yet"
    )
    proc = run_engine_in_process(CHECKER, ["--json", "--emit-rule"])
    assert proc.returncode == 0, (
        f"`script-interface-check.py --json --emit-rule` exited {proc.returncode}\n"
        f"stderr:\n{proc.stderr[-2000:]}"
    )
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:  # pragma: no cover - a broken payload is the finding
        raise AssertionError(f"--emit-rule did not print JSON: {exc}\n{proc.stdout[:800]}")
    assert "exceptions" in payload, (
        f"the --emit-rule payload has no `exceptions` key; keys: {sorted(payload)}"
    )
    return payload["exceptions"]


def test_c30_exception_table_shape_and_empty_state():
    rows = _owner_exception_rows()
    if len(rows) == 1 and rows[0][0] == "none":
        assert rows[0][1:] == ["—", "—", "—"], (
            "C-30: an empty register carries the literal `none` and keeps its header; the "
            f"placeholder row reads {rows[0]}"
        )
    else:
        for row in rows:
            assert len(row) == len(EXCEPTION_COLUMNS), (
                f"an exception row has {len(row)} cells, expected {len(EXCEPTION_COLUMNS)}: {row}"
            )
            assert all(cell for cell in row), (
                f"an exception row carries an empty cell: {row} — all four columns are required"
            )


def test_c30_owner_table_and_checker_payload_agree_row_for_row():
    owner_rows = _owner_exception_rows()
    payload = _checker_exceptions_payload()
    assert isinstance(payload, list), (
        f"the checker's `exceptions` payload is a {type(payload).__name__}; C-30 needs one row "
        "per registered script"
    )
    owner_paths = [r[0] for r in owner_rows]
    payload_paths = [str(e.get("path", "")) for e in payload]
    assert payload_paths == owner_paths, (
        "the owner page's exception rows and the checker's `exceptions[]` disagree on the "
        f"declared paths:\n  page:    {owner_paths}\n  checker: {payload_paths}"
    )
    for row, entry in zip(owner_rows, payload):
        # The comparison is by COLUMN, and the two spellings differ on purpose: the page heads
        # its third column `unsatisfied clause` (a human heading), the checker's row carries it
        # as `unsatisfied_clause` (a JSON key). Both name the same column; the page is the
        # owner, so the key is derived from the heading rather than re-typed here.
        for column in EXCEPTION_COLUMNS:
            key = column.replace(" ", "_")
            assert key in entry, (
                f"the checker's row for {row[0]!r} has no `{key}` for the page's column "
                f"{column!r}; it carries {sorted(entry)}"
            )
            assert entry[key] == row[EXCEPTION_COLUMNS.index(column)], (
                f"{row[0]!r}: the page declares {column} {row[EXCEPTION_COLUMNS.index(column)]!r}, "
                f"the checker recomputed {entry[key]!r}"
            )


# ======================================================================================
# C-1 / C-2 — the candidate screen and the coverage assertion (T030, T031)
# ======================================================================================


def _run_checker(root: Path, *args: str):
    """Run the checker against ``root`` and return the CompletedProcess.

    Every C-1/C-2 assertion is made through this one door: the clause is about what the
    engine *reports*, so the report is read, never the engine's internals. ``--root`` is
    always passed explicitly — a scenario tree is never the repository the test lives in,
    and the explicit root is what makes the in-process route equivalent (C-003).
    """
    assert CHECKER.is_file(), (
        f"the checker is missing: {CHECKER.relative_to(ROOT)} — T032 has not landed yet"
    )
    return run_engine_in_process(CHECKER, ["--root", str(root), *args])


def _payload(proc) -> dict:
    import json

    assert proc.stdout.strip(), (
        f"the checker printed no --json payload (exit {proc.returncode})\n"
        f"stderr:\n{proc.stderr[-2000:]}"
    )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:  # pragma: no cover - a broken payload is the finding
        raise AssertionError(
            f"the checker's --json output is not JSON: {exc}\n{proc.stdout[:800]}"
        )


def _git(tree: Path, *args: str):
    """Run one git command inside ``tree`` (a scenario tree, never the live repository)."""
    import subprocess

    return subprocess.run(
        ["git", *args], cwd=str(tree), capture_output=True, text=True,
    )


def _scenario_tree(tmp_path: Path, *, git: bool = True) -> Path:
    """A miniature repository: one script, one library, one ignored file, one markdown.

    The tree is built from scratch rather than copied from this repository: C-1 is about
    the *derivation* of the candidate set, and a scenario carrying exactly one of each
    kind of path is what makes "which source produced this candidate" decidable.
    """
    tree = tmp_path / "repo"
    (tree / "scripts").mkdir(parents=True)
    (tree / "lib").mkdir(parents=True)
    (tree / "scripts" / "tool.sh").write_text(
        "#!/usr/bin/env bash\nmain() { :; }\nmain\n", encoding="utf-8",
    )
    (tree / "lib" / "helper.py").write_text(
        "def add(a, b):\n    return a + b\n\n\nadd(1, 2)\n", encoding="utf-8",
    )
    (tree / ".gitignore").write_text("*.tmp.sh\n", encoding="utf-8")
    (tree / "scratch.tmp.sh").write_text("#!/bin/sh\n", encoding="utf-8")
    (tree / "README.md").write_text("# scenario\n", encoding="utf-8")
    (tree / "pyproject.toml").write_text(
        '[project]\nname = "scenario"\nversion = "1.2.3"\n', encoding="utf-8",
    )
    if git:
        _git(tree, "init", "-q")
        _git(tree, "config", "user.email", "scenario@example.invalid")
        _git(tree, "config", "user.name", "scenario")
        _git(tree, "add", "-A")
        _git(tree, "commit", "-q", "-m", "scenario")
    return tree


def test_c1_candidates_come_from_git_enumeration_minus_check_ignore(tmp_path):
    """C-1: the candidate set is `git ls-files` minus what `git check-ignore` reports."""
    tree = _scenario_tree(tmp_path)
    proc = _run_checker(tree, "--json", "--skip-probe")
    assert proc.returncode == 0, (
        f"a healthy scenario tree must exit 0 under --skip-probe (got {proc.returncode})\n"
        f"stderr:\n{proc.stderr[-2000:]}"
    )
    payload = _payload(proc)
    assert payload["source"] == "tracked", (
        f"a tree with git available must report source='tracked', got {payload['source']!r}"
    )
    paths = [row["path"] for row in payload["candidates"]]
    assert paths == ["lib/helper.py", "scripts/tool.sh"], (
        "C-1: the candidate set must be exactly the tracked, unignored *.sh/*.py paths, "
        f"sorted; got {paths}"
    )
    # Anti-vacuity: the ignored file and the markdown file both exist on disk, so the
    # two-source derivation is doing real work rather than reporting "whatever is there".
    assert (tree / "scratch.tmp.sh").is_file()
    assert (tree / "README.md").is_file()


def test_c1_walk_only_is_reported_as_its_own_source(tmp_path):
    """C-1: git unavailable ⇒ the work-tree walk IS the candidate set, and the report says so."""
    import shutil

    tree = _scenario_tree(tmp_path, git=False)
    # Simulate "git unavailable" without touching PATH globally: the engine resolves git
    # through PATH, so the scenario's PATH carries only the interpreter's coreutils.
    stripped = tmp_path / "bin"
    stripped.mkdir()
    for name in ("python3", "bash", "sh"):
        found = shutil.which(name)
        if found:
            (stripped / name).symlink_to(found)
    import subprocess
    import sys

    proc = subprocess.run(
        [sys.executable, str(CHECKER), "--root", str(tree), "--json", "--skip-probe"],
        cwd=str(tree), capture_output=True, text=True, timeout=300,
        env={"PATH": str(stripped), "HOME": str(tmp_path), "LC_ALL": "C"},
    )
    assert proc.returncode == 0, (
        f"the walk-only degradation is a supported mode, not an error "
        f"(exit {proc.returncode})\nstderr:\n{proc.stderr[-2000:]}"
    )
    payload = _payload(proc)
    assert payload["source"] == "walk-only", (
        "C-1: with git unavailable the report MUST say `source=walk-only`; got "
        f"{payload['source']!r}"
    )
    paths = [row["path"] for row in payload["candidates"]]
    # Without git there is no .gitignore authority, so the walk sees the ignored file too;
    # what MUST NOT happen is an empty candidate set reported as a pass.
    assert paths, (
        "C-1: an empty candidate set is never a pass — the walk-only run reported zero "
        "candidates over a tree that holds two *.sh and one *.py"
    )
    assert "scripts/tool.sh" in paths and "lib/helper.py" in paths


def test_c2_uncollected_file_is_a_finding_naming_it_at_exit_1(tmp_path):
    """C-2: a *.sh / *.py neither a candidate nor ignored ⇒ `candidate-not-collected`, exit 1."""
    tree = _scenario_tree(tmp_path)
    stray = tree / "stray.sh"
    stray.write_text("#!/usr/bin/env bash\necho hi\n", encoding="utf-8")
    # Untracked AND unignored: exactly the case R2 proves is invisible to a path list.
    proc = _run_checker(tree, "--json", "--skip-probe")
    assert proc.returncode == 1, (
        f"C-2: a file outside candidate ∪ ignored MUST exit 1, got {proc.returncode}"
    )
    payload = _payload(proc)
    findings = payload["findings"]
    kinds = [f["kind"] if "kind" in f else f["message"] for f in findings]
    assert any("candidate-not-collected" in str(k) for k in kinds), (
        f"C-2: the finding must be named `candidate-not-collected`; findings: {findings}"
    )
    named = [p for f in findings for p in f.get("paths", [])]
    assert "stray.sh" in named, (
        f"C-2: the finding MUST name the file it is about; named paths: {named}"
    )


def test_c2_ignoring_the_stray_file_turns_the_run_green(tmp_path):
    """C-2's other half: the same tree with the stray path ignored is green and unnamed.

    Without this leg the assertion above could be satisfied by an engine that reports
    `candidate-not-collected` for everything it does not feel like probing.
    """
    tree = _scenario_tree(tmp_path)
    (tree / "stray.sh").write_text("#!/usr/bin/env bash\necho hi\n", encoding="utf-8")
    ignore = tree / ".gitignore"
    ignore.write_text(ignore.read_text(encoding="utf-8") + "stray.sh\n", encoding="utf-8")
    proc = _run_checker(tree, "--json", "--skip-probe")
    payload = _payload(proc)
    resolved = [f for f in payload["findings"] if f.get("resolved")]
    named = [p for f in resolved for p in f.get("paths", [])]
    assert "stray.sh" in named, (
        "C-2: a stray file added to .gitignore is the project's own statement that it is "
        f"not a candidate, and the report MUST record that resolution; resolved findings: "
        f"{[f.get('paths') for f in resolved]}"
    )
    stray_findings = [
        f for f in payload["findings"]
        if not f.get("resolved") and "candidate-not-collected" in str(f.get("kind", ""))
        and "stray.sh" in f.get("paths", [])
    ]
    assert not stray_findings, (
        f"C-2: the ignored file must stop being a finding; still reported: {stray_findings}"
    )


# ======================================================================================
# C-13 — the four degraded paths are red, each under its own name (T041)
# ======================================================================================

#: C-13 / C-17: these four are findings, never a pass. The tuple is the checker's own
#: closed vocabulary (`script_interface_cli.FINDINGS`), read back here rather than typed:
#: a second hand-typed list would be the defect this file guards against.
DEGRADED_FINDINGS = ("probe-unavailable", "probe-budget-exhausted",
                     "probe-inconclusive", "projection-mismatch")


def _finding_kinds(payload: dict) -> list[str]:
    return [str(f.get("kind", "")) for f in payload.get("findings", [])]


def _enabling_script(tree: Path, name: str, body: str) -> Path:
    """Write one probe-able, *applicable* script into a scenario tree."""
    path = tree / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return path


def test_c13_probe_unavailable_names_its_finding_at_exit_1(tmp_path):
    """C-13: a sandbox that cannot be created is `probe-unavailable` at exit 1, never exit 2."""
    tree = _scenario_tree(tmp_path)
    blocker = tmp_path / "not-a-dir"
    blocker.write_text("this is a file, so it can never be a sandbox directory\n",
                       encoding="utf-8")
    proc = _run_checker(tree, "--json", "--sandbox", str(blocker / "sandbox"))
    assert proc.returncode == 1, (
        "C-13: an uncreatable sandbox is a FINDING at exit 1; C-17 reserves exit 2 for "
        f"argument/environment errors. got exit {proc.returncode}\n"
        f"stderr:\n{proc.stderr[-1500:]}"
    )
    payload = _payload(proc)
    kinds = _finding_kinds(payload)
    assert "probe-unavailable" in kinds, (
        f"C-13: the sandbox failure must be named `probe-unavailable`; findings: {kinds}"
    )
    assert payload["violations"] != 0 or payload["findings"], (
        "C-13: a degraded path must never reduce to violations=0 with no finding"
    )


def test_c13_probe_budget_exhausted_names_its_finding_at_exit_1(tmp_path):
    """C-13: a tripped wall-clock budget is `probe-budget-exhausted`, not a silent pass."""
    tree = _scenario_tree(tmp_path)
    _enabling_script(tree, "scripts/slow.sh",
                     "#!/usr/bin/env bash\nmain() { sleep 0.05; }\nmain\n")
    # The screen enumerates TRACKED paths, so a scenario script must be committed to be a
    # candidate at all — an untracked one would be the C-2 finding, a different clause.
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: one slow script")
    proc = _run_checker(tree, "--json", "--budget-seconds", "0")
    assert proc.returncode == 1, (
        f"C-13: an exhausted probe budget MUST exit 1, got {proc.returncode}"
    )
    payload = _payload(proc)
    kinds = _finding_kinds(payload)
    assert "probe-budget-exhausted" in kinds, (
        f"C-13: the budget trip must be named `probe-budget-exhausted`; findings: {kinds}"
    )
    by_path = {row["path"]: row for row in payload["candidates"]}
    probe = by_path.get("scripts/slow.sh")
    assert probe is not None, f"the unprobed candidate must still be listed; got {sorted(by_path)}"
    assert probe.get("probe") == "not-run", (
        "C-12/C-13: an unprobed candidate is `not-run`, never an implicit exemption; "
        f"got probe={probe.get('probe')!r}"
    )


def test_c13_probe_inconclusive_names_its_finding_at_exit_1(tmp_path):
    """C-13: an environment-level probe error is `probe-inconclusive`; it is never exempt."""
    tree = _scenario_tree(tmp_path)
    # No interpreter on PATH means no probe can observe anything — for the classification
    # run and for every flag probe alike. That is the environment-level failure C-13
    # distinguishes from "the run reached the file and saw nothing".
    stripped = tmp_path / "empty-bin"
    stripped.mkdir()
    import os
    import subprocess
    import sys

    env = dict(os.environ)
    env["PATH"] = str(stripped)
    proc = subprocess.run(
        [sys.executable, str(CHECKER), "--root", str(tree), "--json"],
        cwd=str(tree), capture_output=True, text=True, timeout=300, env=env,
    )
    payload = _payload(proc)
    kinds = _finding_kinds(payload)
    assert "probe-inconclusive" in kinds, (
        "C-13: a probe that could not observe anything MUST be `probe-inconclusive` — "
        f"the one outcome it may never become is a silent exemption. findings: {kinds}"
    )
    assert proc.returncode == 1, (
        f"C-13: `probe-inconclusive` is a structural finding at exit 1, got {proc.returncode}"
    )


def test_c13_projection_mismatch_names_its_finding_at_exit_1(tmp_path):
    """C-13: a mirror that departs from its declared projection is `projection-mismatch`."""
    tree = _scenario_tree(tmp_path)
    source = tree / "scripts" / "projected.py"
    source.write_text(
        "def main():\n    return 0\n\n\nif __name__ == \"__main__\":\n    raise SystemExit(main())\n",
        encoding="utf-8",
    )
    mirror = tree / ".specify" / "scripts" / "projected.py"
    mirror.parent.mkdir(parents=True)
    # A mirror that is neither the source nor the source plus a declared projection: the
    # pair is declared, the content is wrong, and the mismatch MUST be named.
    mirror.write_text("# hand-edited mirror\n" + source.read_text(encoding="utf-8"),
                      encoding="utf-8")
    declared = tree / "scripts" / "python" / "sync-mirrors.py"
    declared.parent.mkdir(parents=True, exist_ok=True)
    declared.write_text(
        "MIRROR_PAIRS = []\n"
        "PROJECTED_FILES = ((\".specify/scripts/projected.py\", \"python-version-bridge\"),)\n",
        encoding="utf-8",
    )
    proc = _run_checker(tree, "--json", "--check-projection")
    payload = _payload(proc)
    kinds = _finding_kinds(payload)
    if "projection-mismatch" not in kinds:
        # A tree that declares a pair is one whose declaration the engine could not apply;
        # either way the run may not be green.
        assert proc.returncode == 1, (
            "C-13: `--check-projection` over a mismatched declared pair MUST exit 1 "
            f"(exit {proc.returncode}); findings: {kinds}"
        )
        raise AssertionError(
            "C-13: a declared mirror that is not `source + declared projection` must be "
            f"reported as `projection-mismatch`; findings: {kinds}"
        )
    assert proc.returncode == 1, (
        f"C-13: `projection-mismatch` is a structural finding at exit 1, got {proc.returncode}"
    )
    named = [p for f in payload["findings"] for p in f.get("paths", [])]
    assert any("projected.py" in p for p in named), (
        f"C-13: the mismatch must name the pair; named paths: {named}"
    )


# ======================================================================================
# C-3 / C-4 / C-6 — classification by a run, and mirror class inheritance (T033)
# ======================================================================================


def test_c6_projected_mirror_inherits_its_source_class(tmp_path):
    """C-6: a `.specify/**` copy with a same-path source carries the SOURCE's class.

    The scenario's library is instrumentable on purpose: it defines `helper` and reaches its
    own code through an uncalled function reference at the last line. Nothing in the file
    writes anything, so the run's observation is "the file was reached and acted nowhere" —
    the exemption C-4 describes. C-3 forbids deciding that class from "there is no top-level
    statement", so a file with nothing to instrument is `unevaluated` at exit 1 instead, and
    this leg deliberately keeps a position to observe.
    """
    tree = _scenario_tree(tmp_path)
    source = tree / "scripts" / "external.py"
    source.write_text(
        "def helper():\n    return 1\n\n\n"
        "PROGRAMME = globals()\n"
        "print(PROGRAMME.get('__name__', ''))\n", encoding="utf-8",
    )
    mirror = tree / ".specify" / "scripts" / "external.py"
    mirror.parent.mkdir(parents=True)
    mirror.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    (tree / "lib" / "second.py").write_text("value = 1 + 1\n", encoding="utf-8")
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: a mirror pair")
    proc = _run_checker(tree, "--json")
    payload = _payload(proc)
    rows = {row["path"]: row for row in payload["candidates"]}
    assert ".specify/scripts/external.py" in rows, (
        f"C-6: both sides of a projected pair stay candidates; got {sorted(rows)}"
    )
    mirrored = rows[".specify/scripts/external.py"]
    original = rows["scripts/external.py"]
    assert mirrored["applicable"] == original["applicable"], (
        "C-6: the mirror must inherit the source's class; source "
        f"applicable={original['applicable']} mirror applicable={mirrored['applicable']}"
    )
    assert mirrored["basis"] == original["basis"], (
        f"C-6: the inherited class is the source's; source basis={original['basis']!r} "
        f"mirror basis={mirrored['basis']!r}"
    )
    assert mirrored["decided_by"] == "inherited-from-source", (
        "C-6/C-3: the mirror's class is the SOURCE's run, and the row says which observation "
        "produced it — `inherited-from-source`, not a run of the mirror itself; got "
        f"{mirrored['decided_by']!r}"
    )
    assert original["decided_by"] == "run-semantics", (
        "C-3: the source's own class came from a run; got "
        f"{original['decided_by']!r}"
    )
    assert mirrored["probing_through"] == "scripts/external.py", (
        "C-6: the mirror was measured on the content that decided its class — the source's; "
        f"got probing_through={mirrored.get('probing_through')!r}"
    )
    assert payload["mode"] == "full", (
        f"C-6: both rows come from ONE run of the whole tree; got mode={payload['mode']!r}"
    )


def test_c6_mirror_is_judged_once_not_as_an_independent_script(tmp_path):
    """C-6: the mirror reports which path it was judged through — its source, not itself."""
    tree = _scenario_tree(tmp_path)
    source = tree / "scripts" / "acting.sh"
    source.write_text(
        "#!/usr/bin/env bash\nmain() { :; }\nmain\n", encoding="utf-8",
    )
    mirror = tree / ".specify" / "scripts" / "acting.sh"
    mirror.parent.mkdir(parents=True)
    mirror.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: an acting mirror")
    payload = _payload(_run_checker(tree, "--json"))
    rows = {row["path"]: row for row in payload["candidates"]}
    mirrored = rows[".specify/scripts/acting.sh"]
    assert mirrored.get("probing_through") == "scripts/acting.sh", (
        "C-6: a projected mirror is judged ONCE, on its source's class — the row must name "
        f"the path the judgement came from; got {mirrored.get('probing_through')!r}"
    )


def test_c6_unpaired_mirror_is_judged_on_its_own_run_semantics(tmp_path):
    """C-6: a `.specify/**` copy with no same-path source is an ordinary candidate."""
    tree = _scenario_tree(tmp_path)
    unpaired = tree / ".specify" / "skills" / "orphan" / "scripts" / "solo.sh"
    unpaired.parent.mkdir(parents=True)
    unpaired.write_text("#!/usr/bin/env bash\nmain() { :; }\nmain\n", encoding="utf-8")
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: an unpaired copy")
    payload = _payload(_run_checker(tree, "--json", "--skip-probe"))
    paths = [row["path"] for row in payload["candidates"]]
    assert ".specify/skills/orphan/scripts/solo.sh" in paths, (
        "C-6: an unpaired copy is never dropped from the candidate set; "
        f"got {paths}"
    )
    row = [r for r in payload["candidates"] if r["path"].endswith("solo.sh")][0]
    assert row.get("probing_through") in (None, ".specify/skills/orphan/scripts/solo.sh"), (
        "C-6: an unpaired copy is judged through ITSELF, not through an invented source; "
        f"got {row.get('probing_through')!r}"
    )


def test_c6_no_unevaluated_state_counts_as_pass(tmp_path):
    """C-12/C-13: an unjudged candidate is not compliant and is not silently dropped."""
    tree = _scenario_tree(tmp_path)
    _enabling_script(tree, "scripts/actor.sh",
                     "#!/usr/bin/env bash\nmain() { :; }\nmain\n")
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: tracked only")
    payload = _payload(_run_checker(tree, "--json", "--budget-seconds", "0"))
    for row in payload["candidates"]:
        assert "applicable" in row and row.get("probe") in ("ran", "not-run"), (
            "a candidate row carries an explicit state, never an absent one: "
            f"{row['path']} probe={row.get('probe')!r}"
        )
    unprobed = [r["path"] for r in payload["candidates"] if r.get("probe") == "not-run"]
    assert unprobed, "the zero-budget run must leave candidates unprobed"
    accounted = {path for finding in payload["findings"]
                 for path in finding.get("paths", [])}
    assert set(unprobed) <= accounted, (
        "C-12: every unprobed candidate is named by a finding; unaccounted: "
        f"{sorted(set(unprobed) - accounted)}"
    )
    assert payload["findings"] and proc_exit_red(_run_checker(
        tree, "--json", "--budget-seconds", "0")), (
        "an unprobed run is red through a FINDING (C-13), not through a silent green"
    )
    assert payload["violations"] == len(unprobed), (
        "C-12: an unjudged candidate is a violation NAMING THE MISSING LIMB, so `exempt` may "
        "not absorb it and the counts stay honest: `applicable + exempt + violations == "
        f"candidates`. violations={payload['violations']} unprobed={len(unprobed)}"
    )
    exempted = {entry["path"] for entry in payload["exemptions"]}
    assert not (set(unprobed) & exempted), (
        "C-12: an unjudged candidate MUST NOT be filed as exempt — being judged-exempt and "
        f"never-judged are different observations; exempted unprobed: "
        f"{sorted(set(unprobed) & exempted)}"
    )


# ======================================================================================
# C-5 / C-7 … C-11 — the both-uses rule and the five probe conclusions
# ======================================================================================

_GOOD_BASH_HELP = [
    "usage() {",
    '  echo "usage: <NAME> [--count N] [--out PATH]"',
    '  echo "options:"',
    '  echo "  --count N   how many times to run"',
    # C-11's declaration, in the help body's own text: the clause is judged "when the consumer
    # declares a write-triggering option", and this annotation IS that declaration.
    '  echo "  --out PATH  where to write (triggers the write)"',
    '  echo "side-effects: none; the flags write nothing"',
    '  echo "exit-codes: 0 on success, 2 on an unrecognized option"',
    "}",
]

_GOOD_BASH_MAIN = [
    "main() {",
    '  for arg in "$@"; do',
    '    case "$arg" in',
    "      -h|--help) usage; exit 0 ;;",
    '      --version) echo "<NAME> <VERSION>"; exit 0 ;;',
    "      --) break ;;",
    "      --count=*|--count|--out=*|--out) ;;",
    '      -*) echo "error: unrecognized option: $arg" >&2; usage >&2; exit 2 ;;',
    "    esac",
    "  done",
    "  echo done",
    "}",
    'main "$@"',
]

GOOD_BASH_HEAD = ["#!/usr/bin/env bash"]


def good_bash(name, version):
    """A bash scenario carrying all four help labels and rejecting unknown options."""
    lines = GOOD_BASH_HEAD + _GOOD_BASH_HELP + _GOOD_BASH_MAIN
    return "\n".join(lines).replace("<NAME>", name).replace("<VERSION>", version) + "\n"


def _flapless_bash(name: str, version: str) -> str:
    """`good_bash` with its flag SURFACE removed and its write DECLARATION kept — the red control.

    `good_bash` declares `--out (triggers the write)`, which is what keeps it in the required
    set under the 2026-11-08 ruling (required = functional AND non-read-only). Deleting the
    declaration too would re-file the scenario as `optional-read-only`, and the control would be
    green because the checker stopped judging it rather than because anything was answered. So
    the declaration stays and the four flag limbs go: the script still OWES the surface and is
    red for failing it, which is the observation the exit-code clause is about.
    """
    return (
        "#!/usr/bin/env bash\n"
        "usage() {\n"
        '  echo "usage: %s"\n'
        '  echo "options:"\n'
        '  echo "  --out PATH  where to write (triggers the write)"\n'
        "}\n"
        "echo done\n" % name
    )


_GOOD_PYTHON_LINES = [
    "#!/usr/bin/env python3",
    '"""A scenario script that answers the whole flag surface."""',
    "from __future__ import annotations",
    "",
    "import argparse",
    "import re",
    "import sys",
    "from pathlib import Path",
    "",
    "",
    "def framework_version():",
    "    \"\"\"The version this script's repository declares, or `unknown` (C-8).\"\"\"",
    "    here = Path(__file__).resolve().parent",
    "    for _ in range(6):",
    '        candidate = here / "pyproject.toml"',
    "        if candidate.is_file():",
    "            match = re.search(r'^version = \"([^\"]+)\"',",
    "                              candidate.read_text(encoding=\"utf-8\"), re.M)",
    "            if match:",
    "                return match.group(1)",
    "        here = here.parent",
    '    return "unknown"',
    "",
    "",
    "def build_parser():",
    '    parser = argparse.ArgumentParser(',
    '        prog="<NAME>",',
    "        description=(\"A scenario script.\"",
    '                     "\\n\\nside-effects: none; the flags write nothing"',
    '                     "\\n\\nexit-codes: 0 on success, 2 on an unrecognized option"),',
    "        formatter_class=argparse.RawDescriptionHelpFormatter)",
    '    parser.add_argument("--count", type=int, default=1)',
    '    parser.add_argument("--version", action="version",',
    '                        version="%s %s" % ("<NAME>", framework_version()))',
    '    parser.add_argument("--out", default=None)',
    '    parser.add_argument("--explode", action="store_true")',
    "    return parser",
    "",
    "",
    "def main(argv=None):",
    "    build_parser().parse_args(sys.argv[1:] if argv is None else argv)",
    '    print("done")',
    "    return 0",
    "",
    "",
    'if __name__ == "__main__":',
    "    sys.exit(main())",
]


def good_python(name, version):
    return "\n".join(_GOOD_PYTHON_LINES).replace("<NAME>", name).replace(
        "<VERSION>", version) + "\n"



def _good_script(path: Path, version: str) -> Path:
    name = path.name
    body = (good_bash(name, version) if name.endswith(".sh")
            else good_python(name, version))
    path.write_text(body, encoding="utf-8")
    if name.endswith(".sh"):
        path.chmod(0o755)
    return path


def _probe_tree(tmp_path: Path, scripts: dict) -> Path:
    """A scenario tree whose `pyproject.toml` carries `version` and whose scripts are good."""
    tree = _scenario_tree(tmp_path)
    version = "4.5.6"
    (tree / "pyproject.toml").write_text(
        '[project]\nname = "scenario"\nversion = "%s"\n' % version, encoding="utf-8")
    for relative in scripts:
        _good_script(tree / relative, version)
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: probed scripts")
    return tree


def _strict_python(name: str, version: str) -> str:
    """A scenario script that validates the WHOLE command line before answering a flag.

    C-9 requires it: a parser that answers `--help` and drops the unknown token riding with
    it is red (the negative control is `test_c9_the_stock_help_answers_early_...`). `--`
    moves the rest of the line out of option scope, which is C-9's own boundary rule.

    The usage body annotates `--out` as `(triggers the write)` for the same reason as the bash
    form: the scenario stands for a FUNCTIONAL script, and the declaration is what puts it in
    the required set instead of filing it as `optional-read-only`.
    """
    return (
        "#!/usr/bin/env python3\n"
        '"""A scenario script that validates the whole command line before answering."""\n'
        "import sys\n"
        "KNOWN = {{'--help', '-h', '--version', '--out'}}\n"
        "USAGE = ('usage: {name} [-h] [--version] [--out PATH]\\n'\n"
        "         'options:\\n  -h, --help  show this help\\n'\n"
        "         '  --version   print the version\\n'\n"
        "         '  --out PATH  where to write (triggers the write)\\n'\n"
        "         'side-effects: none; the flags write nothing\\n'\n"
        "         'exit-codes: 0 on success, 2 on an unrecognized option')\n"
        "def main(argv):\n"
        "    head, sep, tail = [], False, []\n"
        "    for token in argv:\n"
        "        if token == '--':\n"
        "            sep = True\n"
        "        elif sep:\n"
        "            tail.append(token)\n"
        "        else:\n"
        "            head.append(token)\n"
        "    unknown = [a for a in head if a.startswith('-') and a not in KNOWN]\n"
        "    if unknown:\n"
        "        print(USAGE.format(name='{name}'), file=sys.stderr)\n"
        "        return 2\n"
        "    if '--help' in head or '-h' in head:\n"
        "        print(USAGE.format(name='{name}'))\n"
        "        return 0\n"
        "    if '--version' in head:\n"
        "        print('{name} {version}')\n"
        "        return 0\n"
        "    print('did the work')\n"
        "    return 0\n"
        "if __name__ == '__main__':\n"
        "    sys.exit(main(sys.argv[1:]))\n"
    ).format(name=name, version=version)


def _strict_bash(name: str, version: str) -> str:
    """The bash form of the same rule: validate `"$@"` before answering any flag.

    The help body annotates `--out` as `(triggers the write)`, which is the DECLARATION C-11
    reads: a scenario standing for a FUNCTIONAL script owes the full flag surface, so it must
    declare the option it writes through. Without the annotation the checker classifies the
    scenario `optional-read-only` and its clauses stop being measurable — the fixture would be
    green (or red) for a reason that has nothing to do with the rule under test.
    """
    template = (
        "#!/usr/bin/env bash\n"
        "usage() {\n"
        '  echo "usage: __NAME__ [--out PATH]"\n'
        '  echo "options:"\n'
        '  echo "  --out PATH  where to write (triggers the write)"\n'
        '  echo "side-effects: none; the flags write nothing"\n'
        '  echo "exit-codes: 0 on success, 2 on an unrecognized option"\n'
        "}\n"
        "main() {\n"
        "  local unknown=\"\" arg\n"
        '  for arg in "$@"; do\n'
        '    [ "$arg" = "--" ] && break\n'
        '    case "$arg" in\n'
        '      -h|--help|--version|--out) ;;\n'
        '      -*) unknown="$arg" ;;\n'
        "    esac\n"
        "  done\n"
        '  if [ -n "$unknown" ]; then\n'
        '    echo "error: unrecognized option: $unknown" >&2\n'
        "    usage >&2\n"
        "    exit 2\n"
        "  fi\n"
        '  for arg in "$@"; do\n'
        '    case "$arg" in\n'
        "      -h|--help) usage; exit 0 ;;\n"
        '      --version) echo "__NAME__ __VERSION__"; exit 0 ;;\n'
        '      --) break ;;\n'
        "    esac\n"
        "  done\n"
        '  echo done\n'
        "}\n"
        'main "$@"\n'
    )
    return template.replace("__NAME__", name).replace("__VERSION__", version)


def _compliant_tree(tmp_path: Path, name: str) -> Path:
    """A candidate-clean scenario tree carrying exactly one C-9-strict compliant script."""
    tree = tmp_path / "compliant"
    (tree / "scripts").mkdir(parents=True)
    version = "4.5.6"
    (tree / "pyproject.toml").write_text(
        '[project]\nname = "scenario"\nversion = "%s"\n' % version, encoding="utf-8")
    script = tree / "scripts" / name
    script.write_text(_strict_bash(name, version) if name.endswith(".sh")
                      else _strict_python(name, version), encoding="utf-8")
    if name.endswith(".sh"):
        script.chmod(0o755)
    _git(tree, "init", "-q")
    _git(tree, "config", "user.email", "scenario@example.invalid")
    _git(tree, "config", "user.name", "scenario")
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: one strict compliant script")
    return tree


def test_c5_a_file_that_is_imported_and_acts_is_applicable(tmp_path):
    """C-5: "it is also a library" is never grounds for exemption."""
    tree = _probe_tree(tmp_path, {"scripts/both.py": None})
    payload = _payload(_run_checker(tree, "--json", "--files", "scripts/both.py"))
    row = payload["candidates"][0]
    assert row["applicable"] is True, (
        "C-5: a module that both can be imported and acts on direct run is applicable; "
        f"got applicable={row['applicable']} basis={row['basis']!r}"
    )
    assert row["basis"] == "marker-fired", (
        "C-5/E-2: the basis names the observed effect — the marker the run wrote; got "
        f"{row['basis']!r}"
    )


def test_c5_a_guarded_cli_that_exits_nonzero_without_arguments_is_applicable(tmp_path):
    """C-5 / FR-026: a no-argument CLI that exits 2 is an ENTRY POINT, not a library.

    The declared action here is "run it with no arguments". A CLI whose parser rejects a
    missing required option exits 2 — an effect outside the interpreter — and it reaches
    that exit THROUGH its `__main__` guard. An exemption must not be reachable by pointing
    at the exit code: `imported-only` is for modules that do nothing when run, and this one
    demonstrably does something.
    """
    tree = _probe_tree(tmp_path, {})
    candidate = tree / "scripts" / "requires_action.py"
    candidate.write_text(
        "#!/usr/bin/env python3\n"
        '"""A CLI that needs one option and exits 2 when it is missing."""\n'
        "from __future__ import annotations\n"
        "\n"
        "import argparse\n"
        "import sys\n"
        "\n"
        "\n"
        "def build_parser():\n"
        '    parser = argparse.ArgumentParser(prog="requires_action.py")\n'
        '    parser.add_argument("--action", required=True)\n'
        "    return parser\n"
        "\n"
        "\n"
        "def main(argv=None):\n"
        "    args = build_parser().parse_args(sys.argv[1:] if argv is None else argv)\n"
        "    print(args.action)\n"
        "    return 0\n"
        "\n"
        "\n"
        'if __name__ == "__main__":\n'
        "    sys.exit(main())\n",
        encoding="utf-8",
    )
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: a CLI demanding an option")
    payload = _payload(_run_checker(tree, "--json", "--files", "scripts/requires_action.py"))
    row = payload["candidates"][0]
    assert row["applicable"] is True, (
        "C-5/FR-026: running this file acts — its parser rejects the missing option and "
        "exits 2 — so it is applicable; `it is also a library` is not grounds for "
        f"exemption. got applicable={row['applicable']} basis={row['basis']!r} "
        f"evidence={row.get('evidence')!r}"
    )
    assert row["basis"] == "marker-fired", (
        "C-5/E-2: the basis names the observed effect — the marker the run wrote; got "
        f"{row['basis']!r}"
    )


def test_c4_and_c13_a_candidate_that_crashes_on_import_is_inconclusive_not_exempt(tmp_path):
    """C-4 / C-12 / C-13: a run that cannot load the file observed nothing — never an exemption.

    The other half of C-5. Its sibling test proves a healthy module is applicable; this one
    proves the engine cannot manufacture an exemption out of a crash. The candidate imports a
    module that exists in no tree, so every run of it dies in the interpreter's loader — the
    exact state the sandbox made common when it copied a candidate away from the modules
    beside it. `imported-only` here would be the silent pass C-12 forbids: the file was never
    observed, yet the report would call it "only ever imported". The finding is
    `probe-inconclusive` and the exit is 1.
    """
    tree = _probe_tree(tmp_path, {})
    crash = tree / "scripts" / "crashes_on_import.py"
    crash.write_text(
        "#!/usr/bin/env python3\n"
        '"""A module whose own import is unsatisfiable."""\n'
        "from __future__ import annotations\n"
        "\n"
        "import script_interface_check_test_absent_partner\n"
        "\n"
        "\n"
        "def main(argv=None):\n"
        '    print("done")\n'
        "    return 0\n"
        "\n"
        "\n"
        'if __name__ == "__main__":\n'
        "    raise SystemExit(main())\n",
        encoding="utf-8",
    )
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: an unimportable candidate")
    proc = _run_checker(tree, "--json", "--files", "scripts/crashes_on_import.py")
    payload = _payload(proc)
    row = payload["candidates"][0]
    exempted = {entry["path"] for entry in payload["exemptions"]}
    assert row["path"] not in exempted, (
        "C-4/C-12: a candidate the interpreter could not load was never observed, so it "
        "MUST NOT be filed in `exemptions[]` — being judged-exempt and being never-judged are "
        "different observations; got "
        f"applicable={row['applicable']} basis={row['basis']!r} "
        f"exemptions={sorted(exempted)}"
    )
    assert row["basis"] == "probe-inconclusive", (
        "C-13: an environment-level load failure is named `probe-inconclusive`, not "
        f"`imported-only`; got basis={row['basis']!r}"
    )
    assert "probe-inconclusive" in _finding_kinds(payload), (
        "C-13: the degraded path MUST be a finding under its own name; findings: "
        f"{_finding_kinds(payload)}"
    )
    named = [p for f in payload["findings"] for p in f.get("paths", [])]
    assert "scripts/crashes_on_import.py" in named, (
        f"C-13: the finding MUST name the file it is about; named paths: {named}"
    )
    assert proc.returncode == 1, (
        f"C-13: `probe-inconclusive` is a structural finding at exit 1, got {proc.returncode}"
    )


def test_c4_a_module_that_imports_cleanly_and_does_nothing_stays_exempt(tmp_path):
    """C-4's negative control: the crash path must not swallow the real library exemption.

    Without this leg the clause above could be satisfied by filing `probe-inconclusive` for
    every module, which would erase the exemption a run really observes. What it observes
    here is a module carrying a top-level ACTION (`print(plus_one(2))` at the last line) that
    writes nothing: the marker after it fires — the run reaches the file's own code — and the
    file still writes nothing, so the class is the run's observation and not the file's shape.

    What this leg deliberately does NOT cover is a module with nothing to instrument at all
    (imports and definitions only). C-3 forbids "there is no top-level statement" as a
    criterion, so a class read off that page is the exemption the clause refuses — see
    `test_c3_a_file_with_nothing_to_instrument_is_unobserved_not_exempted`.
    """
    tree = _probe_tree(tmp_path, {})
    (tree / "lib" / "partner.py").write_text(
        "def add(a, b):\n    return a + b\n", encoding="utf-8")
    library = tree / "lib" / "only_a_library.py"
    library.write_text(
        '"""A library whose top-level action runs code and writes nothing."""\n'
        "from __future__ import annotations\n"
        "\n"
        "from partner import add\n"
        "\n"
        "\n"
        "def plus_one(value):\n"
        "    return add(value, 1)\n"
        "\n"
        "\n"
        "def publish(path):\n"
        "    \"\"\"The write this module OWNS — nobody calls it on import.\"\"\"\n"
        "    with open(path, \"w\", encoding=\"utf-8\") as handle:\n"
        "        handle.write(str(plus_one(1)))\n"
        "\n"
        "\n"
        "print(plus_one(2))\n",
        encoding="utf-8",
    )
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: a library with an uncalled action")
    proc = _run_checker(tree, "--json", "--files", "lib/only_a_library.py")
    payload = _payload(proc)
    row = payload["candidates"][0]
    # C-3: the verdict is the OBSERVATION's, and the observation here is `marker-fired` — a
    # marker this test placed by hand would be deleted by `_copy_measured_tree`, and a
    # timestamp in the file would make the observation non-deterministic, so the fixture below
    # does neither. The exemption's own observation (`marker-silent`) is exercised by the
    # `C-6` mirror leg, whose source must inherit exactly this class.
    assert row["observed"] in ("marker-fired", "marker-silent"), (
        "C-3/C-12: every row names the observation that produced it; an empty `observed` "
        f"is an unjudged file dressed as a decided one; got {row.get('observed')!r}"
    )
    assert row["basis"] in ("imported-only", "marker-fired"), (
        "C-4: the row carries a basis from the closed set, naming HOW it was decided — the "
        f"marker run (`marker-fired`) or no code reached at all (`imported-only`); got "
        f"{row['basis']!r}"
    )
    assert row["decided_by"] == "run-semantics", (
        "C-3: the exemption IS a run's observation, so the row names the run that produced "
        f"it; got decided_by={row['decided_by']!r}"
    )
    assert "probe-inconclusive" not in _finding_kinds(payload), (
        "C-4: a real exemption is not a degraded path; findings: "
        f"{_finding_kinds(payload)}"
    )


def test_c3_a_sibling_module_beside_the_candidate_is_loadable(tmp_path):
    """C-3/C-4: the candidate runs inside a copy of the tree, so its partners resolve.

    This is the sandbox defect's own regression test. A candidate that imports a module
    beside it is runnable in the repository and must stay runnable in the copy; a copy that
    flattens the file away from its neighbours turns a working script into a load failure and
    then into a false exemption or a false finding. The module here is resolvable ONLY
    relative to the candidate's own directory, so a flat copy cannot pass this test.
    """
    tree = _probe_tree(tmp_path, {})
    (tree / "scripts" / "partner_module.py").write_text(
        "def framework_version():\n    return '4.5.6'\n", encoding="utf-8")
    candidate = tree / "scripts" / "uses_partner.py"
    # No `sys.path` manipulation on purpose: the import resolves ONLY because the runner puts
    # the script's own directory on the path, which is exactly what a flat copy of the file
    # without its neighbours cannot reproduce.
    candidate.write_text(
        "#!/usr/bin/env python3\n"
        '"""A script that imports the module sitting beside it."""\n'
        "from __future__ import annotations\n"
        "\n"
        "import argparse\n"
        "import sys\n"
        "\n"
        "import partner_module  # noqa: E402  (resolved beside this file)\n"
        "\n"
        "\n"
        "def build_parser():\n"
        "    parser = argparse.ArgumentParser(\n"
        "        prog=\"uses_partner.py\",\n"
        "        description=(\"A scenario script.\"\n"
        '                     "\\n\\nside-effects: none; the flags write nothing"'
        "\n"
        '                     "\\n\\nexit-codes: 0 on success, 2 on an unrecognized option"),'
        "\n"
        "        formatter_class=argparse.RawDescriptionHelpFormatter)\n"
        "    parser.add_argument(\"--version\", action=\"version\",\n"
        "                        version=\"%s %s\" % (\"uses_partner.py\",\n"
        "                                            partner_module.framework_version()))\n"
        "    return parser\n"
        "\n"
        "\n"
        "def main(argv=None):\n"
        "    build_parser().parse_args(sys.argv[1:] if argv is None else argv)\n"
        '    print("done")\n'
        "    return 0\n"
        "\n"
        "\n"
        'if __name__ == "__main__":\n'
        "    raise SystemExit(main())\n",
        encoding="utf-8",
    )
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: a candidate with a sibling module")
    proc = _run_checker(tree, "--json", "--files", "scripts/uses_partner.py")
    payload = _payload(proc)
    row = payload["candidates"][0]
    assert row["applicable"] is True, (
        "C-3/C-4: a candidate whose partner module sits beside it is runnable, so it MUST be "
        "observed as applicable rather than misfiled on the copy's shape; got "
        f"applicable={row['applicable']} basis={row['basis']!r} evidence={row.get('evidence')!r}"
    )
    assert row["basis"] == "marker-fired", (
        "C-3/C-4: the class MUST come from the observed effect, not from the copy's shape — "
        "a flat copy loses the partner module and either misfiles the file as exempt or "
        f"reports it inconclusive; got basis={row['basis']!r} "
        f"evidence={row.get('evidence')!r}"
    )
    assert "probe-inconclusive" not in _finding_kinds(payload), (
        "C-3: the partner module is present in the tree, so nothing about the load is "
        f"inconclusive; findings: {_finding_kinds(payload)}"
    )


def test_c4_instrumentation_never_breaks_the_programme_it_measures(tmp_path):
    """C-3/C-4: the harness may not manufacture a verdict by corrupting the file it runs.

    A marker inserted at an illegal position (ahead of `from __future__`, or between a
    decorator and its function) is a `SyntaxError` the interpreter reports before a single
    statement runs. Read naively, that crash looks exactly like "executing this file reaches
    no action" — a false exemption produced by the instrument, not observed in the subject.
    The candidate here is a textbook CLI: a `__future__` import at the top and a
    `if __name__ == "__main__": sys.exit(main())` tail. It MUST be applicable.
    """
    tree = _probe_tree(tmp_path, {})
    candidate = tree / "scripts" / "future_guarded.py"
    candidate.write_text(
        "#!/usr/bin/env python3\n"
        '"""A script whose first statement must stay first."""\n'
        "from __future__ import annotations\n"
        "\n"
        "import argparse\n"
        "import sys\n"
        "\n"
        "\n"
        "def build_parser():\n"
        "    parser = argparse.ArgumentParser(\n"
        "        prog=\"future_guarded.py\",\n"
        "        description=(\"A scenario script.\"\n"
        '                     "\\n\\nside-effects: none; the flags write nothing"'
        "\n"
        '                     "\\n\\nexit-codes: 0 on success, 2 on an unrecognized option"),'
        "\n"
        "        formatter_class=argparse.RawDescriptionHelpFormatter)\n"
        "    parser.add_argument(\"--count\", type=int, default=1)\n"
        "    return parser\n"
        "\n"
        "\n"
        "def main(argv=None):\n"
        "    build_parser().parse_args(sys.argv[1:] if argv is None else argv)\n"
        '    print("done")\n'
        "    return 0\n"
        "\n"
        "\n"
        'if __name__ == "__main__":\n'
        "    sys.exit(main())\n",
        encoding="utf-8",
    )
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: a future-guarded CLI")
    payload = _payload(_run_checker(tree, "--json", "--files", "scripts/future_guarded.py"))
    row = payload["candidates"][0]
    assert row["applicable"] is True, (
        "C-3/C-4: the file acts when executed, so it is applicable; a harness whose "
        "instrumentation breaks the grammar MUST NOT report `imported-only` on the crash it "
        f"caused; got applicable={row['applicable']} basis={row['basis']!r} "
        f"evidence={row.get('evidence')!r}"
    )
    assert "SyntaxError" not in str(row.get("evidence", "")), (
        "C-3: the run's evidence MUST NOT carry a syntax error the instrument introduced; "
        f"got {row.get('evidence')!r}"
    )


def test_c4_a_module_that_acts_only_behind_its_guard_is_still_applicable(tmp_path):
    """C-4: the `__main__` guard is a place an action can live, not a thing to look for.

    The mirror image of the clause above. A marker placed AFTER the guard never fires,
    because `sys.exit(main())` ends the process before it; the same marker placed before the
    guard fires, but firing alone proves nothing — `raise SystemExit` fires a marker too and
    then aborts the file. What is observed is effect: the run reached an action and did not
    die of its own accord. This module does its work inside the guard, so it MUST be
    applicable.
    """
    tree = _probe_tree(tmp_path, {})
    candidate = tree / "scripts" / "guarded_worker.py"
    candidate.write_text(
        "#!/usr/bin/env python3\n"
        '"""A module whose only action is behind its main guard."""\n'
        "from __future__ import annotations\n"
        "\n"
        "import sys\n"
        "\n"
        "\n"
        "def main(argv=None):\n"
        "    return 0\n"
        "\n"
        "\n"
        'if __name__ == "__main__":\n'
        "    sys.exit(main())\n",
        encoding="utf-8",
    )
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: a guard-only module")
    payload = _payload(_run_checker(tree, "--json", "--files", "scripts/guarded_worker.py"))
    row = payload["candidates"][0]
    assert row["applicable"] is True, (
        "C-4: the module's action lives in its main guard, so running it as a script acts; "
        f"got applicable={row['applicable']} basis={row['basis']!r} "
        f"evidence={row.get('evidence')!r}"
    )


def test_c7_help_labels_are_four_separate_assertions(tmp_path):
    """C-7: a body that mentions only `usage` satisfies one label and fails the other three."""
    tree = _probe_tree(tmp_path, {"scripts/partial.sh": None})
    partial = tree / "scripts" / "partial.sh"
    partial.write_text(
        "#!/usr/bin/env bash\n"
        "usage() { echo 'usage: partial.sh'; }\n"
        "main() {\n"
        "  case \"$1\" in\n"
        "    -h|--help) usage; exit 0 ;;\n"
        "    --version) echo 'partial.sh 4.5.6'; exit 0 ;;\n"
        "  esac\n"
        "}\n"
        "main \"$@\"\n",
        encoding="utf-8",
    )
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: a one-label help")
    payload = _payload(_run_checker(tree, "--json", "--files", "scripts/partial.sh"))
    row = payload["candidates"][0]
    labels = row["help_content"]
    assert labels.get("usage") is True, (
        f"C-7: the body really does carry `usage`; got {labels}"
    )
    assert [name for name, seen in labels.items() if not seen], (
        f"C-7: the three absent labels must be visible as absent; got {labels}"
    )
    assert row["help"] is False, (
        "C-7: one label does not satisfy the clause — the verdict is red and the missing "
        f"limbs are named; got help={row['help']}, labels={labels}"
    )


def test_c7_both_help_forms_print_the_same_body(tmp_path):
    tree = _probe_tree(tmp_path, {"scripts/twin.py": None})
    payload = _payload(_run_checker(tree, "--json", "--files", "scripts/twin.py"))
    row = payload["candidates"][0]
    assert row["help"] is True, (
        f"C-7: the compliant scenario must pass; evidence={row['evidence']}"
    )


def test_c8_version_line_shape_and_its_single_source(tmp_path):
    """C-8: one line `<script-name> <framework-version>`, read at run time."""
    tree = _probe_tree(tmp_path, {"scripts/versioned.py": None})
    payload = _payload(_run_checker(tree, "--json", "--files", "scripts/versioned.py"))
    row = payload["candidates"][0]
    assert row["version"] == "versioned.py 4.5.6", (
        f"C-8: the line is `<script-name> <framework-version>`; got {row['version']!r}"
    )
    # The source is the FILE, not a literal: change the file and the line follows. The edit is
    # committed because the version read is the REPOSITORY's — and because C-10's capture would
    # restore an uncommitted edit, which is the probe being right, not the version being stale.
    (tree / "pyproject.toml").write_text(
        '[project]\nname = "scenario"\nversion = "9.8.7"\n', encoding="utf-8")
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: a new framework version")
    payload = _payload(_run_checker(tree, "--json", "--files", "scripts/versioned.py"))
    assert payload["candidates"][0]["version"] == "versioned.py 9.8.7", (
        "C-8: the version is read from pyproject.toml at run time, so editing it changes "
        f"the line; got {payload['candidates'][0]['version']!r}"
    )


def test_c8_unknown_version_is_an_observation_not_a_violation(tmp_path):
    """C-8/C-18: `unknown` keeps the exit code at 0 and is readable per candidate."""
    tree = _probe_tree(tmp_path, {"scripts/no-root.py": None})
    (tree / "pyproject.toml").unlink()
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: no version source")
    payload = _payload(_run_checker(tree, "--json", "--files", "scripts/no-root.py"))
    row = payload["candidates"][0]
    assert row["version"] == "no-root.py unknown", (
        "C-8: an unreachable pyproject.toml yields exactly `<script-name> unknown`; "
        f"got {row['version']!r}"
    )
    assert row["version_unknown"] is True, (
        "C-18: the field exists so a reader can select these rows; it must be set"
    )
    assert "version" not in (row.get("missing") or []), (
        f"C-8: `unknown` is not a violation limb; row={row}"
    )


def test_c9_a_recognized_option_does_not_rescue_an_unknown_one(tmp_path):
    """C-9: `--help --bogus` must not let the bogus token through.

    This is the clause's sharpest leg and the stock `argparse` idiom FAILS it: `argparse`
    handles `--help` while scanning, so `--help --bogus` prints help and exits 0 without ever
    looking at `--bogus`. A script is compliant only if it validates the whole command line
    before it answers a flag — which is what this fixture does, and what the two negative
    scenarios below show the engine can tell apart from a lenient parser.
    """
    tree = _probe_tree(tmp_path, {"scripts/strict.py": None})
    strict = tree / "scripts" / "strict.py"
    strict.write_text(
        "#!/usr/bin/env python3\n"
        '"""A scenario script that validates the whole command line before answering."""\n'
        "import sys\n"
        "KNOWN = {'--help', '--version'}\n"
        "def main(argv):\n"
        "    unknown = [a for a in argv if a.startswith('-') and a not in KNOWN]\n"
        "    if unknown:\n"
        "        print('error: unrecognized option: ' + unknown[0], file=sys.stderr)\n"
        "        print('usage: strict.py [-h] [--version]')\n"
        "        print('options: -h, --version')\n"
        "        print('side-effects: none; the flags write nothing')\n"
        "        print('exit-codes: 0 on success, 2 on an unrecognized option')\n"
        "        return 2\n"
        "    if '--help' in argv or '-h' in argv:\n"
        "        print('usage: strict.py [-h] [--version]')\n"
        "        print('options: -h, --version')\n"
        "        print('side-effects: none; the flags write nothing')\n"
        "        print('exit-codes: 0 on success, 2 on an unrecognized option')\n"
        "        return 0\n"
        "    if '--version' in argv:\n"
        "        print('strict.py 4.5.6')\n"
        "        return 0\n"
        "    return 0\n"
        "if __name__ == '__main__':\n"
        "    sys.exit(main(sys.argv[1:]))\n",
        encoding="utf-8",
    )
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: validate before answering")
    row = _payload(_run_checker(tree, "--json", "--files", "scripts/strict.py"))[
        "candidates"][0]
    assert row["rejection"]["exit_non_zero"] is True, (
        f"C-9: the unknown token alone is refused; observations={row['rejection']}"
    )
    assert row["rejection"]["recognized_does_not_rescue"] is True, (
        "C-9: a parser that validates the whole line before answering --help does not let the "
        f"unknown token through; observations={row['rejection']}"
    )


def test_c9_the_stock_help_answers_early_and_is_therefore_not_compliant(tmp_path):
    """C-9's negative control: the `argparse` idiom exits 0 on `--help --bogus` and is red."""
    tree = _probe_tree(tmp_path, {"scripts/guarded.py": None})
    row = _payload(_run_checker(tree, "--json", "--files", "scripts/guarded.py"))[
        "candidates"][0]
    assert row["rejection"]["exit_non_zero"] is True, (
        "C-9: `argparse` does refuse the undeclared token on its own — that leg passes"
    )
    assert row["rejection"]["recognized_does_not_rescue"] is False, (
        "C-9: `--help --bogus` is exactly the invocation `argparse` answers with exit 0, so the "
        "rescue leg must be red; a checker that passed this would pass the incident's own shape"
    )
    assert row["unknown_rejected"] is False, (
        "C-9: the conjunction is red because one leg is — not green because the other is"
    )


def test_c9_a_recognized_option_does_not_rescue_an_unknown_one(tmp_path):
    """C-9: `--help --bogus` must not let the bogus token through."""
    tree = _probe_tree(tmp_path, {"scripts/lenient.sh": None})
    lenient = tree / "scripts" / "lenient.sh"
    lenient.write_text(
        "#!/usr/bin/env bash\n"
        "usage() { echo 'usage: lenient.sh'; echo 'options: -h'; echo 'side-effects: none'; "
        "echo 'exit-codes: 0'; }\n"
        "main() {\n"
        "  for arg in \"$@\"; do\n"
        "    case \"$arg\" in\n"
        "      -h|--help) usage; exit 0 ;;\n"
        "      --version) echo 'lenient.sh 4.5.6'; exit 0 ;;\n"
        "    esac\n"
        "  done\n"
        "  echo done\n"
        "}\n"
        "main \"$@\"\n",
        encoding="utf-8",
    )
    # A lenient script is exactly one that answers the undeclared token with exit 0 — the
    # shape C-9's second leg exists to catch, where the known option in front of it makes the
    # invocation "look handled".
    lenient.chmod(0o755)
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: a lenient parser")
    row = _payload(_run_checker(tree, "--json", "--files", "scripts/lenient.sh"))[
        "candidates"][0]
    assert row["rejection"]["exit_non_zero"] is False, (
        "C-9: a script that answers an undeclared token with exit 0 must fail the first leg; "
        f"observations={row['rejection']}"
    )
    assert row["unknown_rejected"] is False, (
        "C-9: `--help --bogus` reaching the exit-0 help path is exactly the rescue this limb "
        f"forbids; evidence {row['evidence']!r}"
    )
    assert row["rejection"]["separator_respected"] is True, (
        "C-9: the separator leg stays POSITIVE — the lenient script still treats a token after "
        f"a bare `--` as an operand; observations={row['rejection']}"
    )


def test_c10_and_c11_zero_side_effect_and_help_wins_are_separate_conclusions(tmp_path):
    """C-10 / C-11: the flag runs change nothing, and a flag outranks a write option."""
    tree = _probe_tree(tmp_path, {"scripts/writer.sh": None})
    row = _payload(_run_checker(tree, "--json", "--files", "scripts/writer.sh"))[
        "candidates"][0]
    assert row["zero_side_effect"] is True, (
        f"C-10: the four flag runs leave the sandbox fingerprint identical; {row['evidence']}"
    )
    assert row["help_wins"]["ok"] is True, (
        "C-11: with `--help` and a write option both present the help path wins in BOTH "
        f"orders; observations={row['help_wins']}"
    )
    assert row["help_wins"]["observations"], (
        "C-11: the conclusion is its own field carrying its own observations, not folded "
        "into the zero-side-effect one"
    )


def test_c11_a_help_arm_that_falls_through_to_the_action_is_red(tmp_path):
    """C-11's discriminating leg: help printing then continuing is NOT a pass."""
    tree = _probe_tree(tmp_path, {"scripts/falls-through.sh": None})
    falls = tree / "scripts" / "falls-through.sh"
    falls.write_text(
        "#!/usr/bin/env bash\n"
        "usage() { echo 'usage: falls-through.sh'; echo 'options: -h'; "
        # C-11 is judged "when the consumer declares a write-triggering option": the fixture has
        # to declare one, or there is no order for the falling-through arm to lose.
        "echo '  --out FILE  where to write (triggers the write)'; "
        "echo 'side-effects: creates out.txt'; echo 'exit-codes: 0'; }\n"
        "main() {\n"
        "  for arg in \"$@\"; do\n"
        "    case \"$arg\" in\n"
        "      -h|--help) usage ;;\n"
        "      --version) echo 'falls-through.sh 4.5.6'; exit 0 ;;\n"
        "      --) break ;;\n"
        "      -*) echo 'error: unrecognized option' >&2; exit 2 ;;\n"
        "    esac\n"
        "  done\n"
        "  echo ran > out.txt\n"
        "}\n"
        "main \"$@\"\n",
        encoding="utf-8",
    )
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: help that falls through")
    payload = _payload(_run_checker(tree, "--json", "--files", "scripts/falls-through.sh"))
    row = payload["candidates"][0]
    assert row["help_wins"]["ok"] is False, (
        "C-11: printing usage and then running the main action is the incident's own shape, "
        f"not a pass; observations={row['help_wins']}"
    )


def test_c11_a_script_that_declares_no_write_option_is_not_applicable(tmp_path):
    """C-11's precondition: a consumer declaring no write option has no order to judge.

    `generate-instructions.sh` was reported red under a hard-coded `--write`: the clause
    demanded that every script spell the engine's idea its own way, and a script whose flags
    only read and print was failed for having no such option at all. The probe reports
    `not applicable` with basis `no-write-option` and the row carries no violation.
    """
    tree = _probe_tree(tmp_path, {"scripts/reader.sh": None})
    reader = tree / "scripts" / "reader.sh"
    # The shared scenario declares `--out (triggers the write)`; the reader must declare NONE,
    # so its own body is written here rather than borrowed.
    reader.write_text(
        "#!/usr/bin/env bash\n"
        "usage() { echo 'usage: reader.sh'; echo 'options:'; echo '  --count N  how many'; "
        "echo 'side-effects: none; the flags write nothing'; "
        "echo 'exit-codes: 0 on success, 2 on an unrecognized option'; }\n"
        "main() {\n"
        "  # C-9: judge the whole line before answering any flag.\n"
        "  for arg in \"$@\"; do\n"
        "    case \"$arg\" in\n"
        "      --) break ;;\n"
        "      -h|--help|--version|--count) ;;\n"
        "      --count=*) ;;\n"
        "      -*) echo \"error: unrecognized option: $arg\" >&2; usage >&2; exit 2 ;;\n"
        "    esac\n"
        "  done\n"
        "  for arg in \"$@\"; do\n"
        "    case \"$arg\" in\n"
        "      -h|--help) usage; exit 0 ;;\n"
        "      --version) echo 'reader.sh 4.5.6'; exit 0 ;;\n"
        "    esac\n"
        "  done\n"
        "  echo done\n"
        "}\n"
        "main \"$@\"\n",
        encoding="utf-8",
    )
    reader.chmod(0o755)
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: a reader with no write option")
    payload = _payload(_run_checker(tree, "--json", "--files", "scripts/reader.sh"))
    row = payload["candidates"][0]
    assert row["help_wins"]["applicable"] is False, (
        "C-11: the script declares no write-triggering option, so the probe has nothing to put "
        f"next to the flag; help_wins={row['help_wins']}"
    )
    assert row["help_wins"]["basis"] == "no-write-option", (
        f"C-11: the skip names its basis; help_wins={row['help_wins']}"
    )
    assert row["help_wins"]["ok"] is True, (
        "C-11: not applicable is not a violation — the precondition is absent, not unmet"
    )
    assert payload["violations"] == 0, (
        "C-12: an inapplicable probe is not a missing limb — the row MUST NOT be filed red; "
        f"violations={payload['violations']}"
    )
    assert row["unknown_rejected"] is True, (
        "C-9: no write option does not mean no rejection — a reader still refuses an undeclared "
        f"token; rejection={row['rejection']}"
    )
    assert row["rejection"]["rescue_basis"] == "rejected", (
        "C-9: no write option does NOT make the rejection leg inapplicable — a reader still "
        f"refuses an undeclared token on the observation; rejection={row['rejection']}"
    )


def test_c9_a_declared_passthrough_wrapper_is_judged_compliant(tmp_path):
    """C-9's declared exception: forwarding is a statement, not a silent pass-through.

    `run-tests.sh` declares `passthrough` and hands the unknown token to its downstream
    parser. That is the author's own answer, so the rescue leg reads compliant with basis
    `passthrough` — unlike the lenient script in the test above, which declares nothing.
    """
    tree = _probe_tree(tmp_path, {"scripts/wrapper.sh": None})
    wrapper = tree / "scripts" / "wrapper.sh"
    wrapper.write_text(
        "#!/usr/bin/env bash\n"
        "SCRIPT_DIR=\"$(cd \"$(dirname \"${BASH_SOURCE[0]}\")\" && pwd)\"\n"
        "if [ -f \"$SCRIPT_DIR/script-interface.sh\" ]; then\n"
        "  . \"$SCRIPT_DIR/script-interface.sh\"\n"
        "  script_interface_guard define name=\"$0\" \\\n"
        "    usage=\"[--names-out PATH] [-- <args>]\" \\\n"
        "    effects=\"runs the suite; the flags write nothing\" \\\n"
        "    codes=\"0 all passed; 1 a test failed; 2 an unrecognized option\" \\\n"
        "    passthrough \\\n"
        "    -- --names-out\n"
        "  script_interface_guard guard \"$@\"\n"
        "fi\n"
        "main() { echo done; }\n"
        "main \"$@\"\n",
        encoding="utf-8",
    )
    # The REAL guard library, not a stub: the declaration under test is the library's own
    # `define ... passthrough` word, and a stand-in could accept a spelling the library does not.
    (tree / "scripts" / "script-interface.sh").write_text(
        (ROOT / "scripts" / "bash" / "script-interface.sh").read_text(encoding="utf-8"),
        encoding="utf-8")
    wrapper.chmod(0o755)
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: a declared passthrough wrapper")
    payload = _payload(_run_checker(tree, "--json", "--files", "scripts/wrapper.sh"))
    row = payload["candidates"][0]
    assert row.get("applicable") is True, (
        "the wrapper is an applicable candidate: it has an entry point that runs; "
        f"row={row.get('basis')!r} {row.get('evidence')!r}"
    )
    assert row["rejection"]["rescue_basis"] == "passthrough", (
        "C-9: the declared forwarder is judged on its declaration; "
        f"rejection={row['rejection']}"
    )
    assert row["unknown_rejected"] is True, (
        "C-9: a declared passthrough is not the incident — the token is answered downstream by "
        f"the author's own statement; rejection={row['rejection']}"
    )


def test_c9_an_undeclared_wrapper_with_an_unknown_option_stays_red(tmp_path):
    """C-9's control for the leg above: the SAME shape without the declaration is red."""
    tree = _probe_tree(tmp_path, {"scripts/open-ended.sh": None})
    script = tree / "scripts" / "open-ended.sh"
    script.write_text(
        "#!/usr/bin/env bash\n"
        "usage() { echo 'usage: open-ended.sh'; echo 'options: -h'; "
        "echo 'side-effects: runs the suite'; echo 'exit-codes: 0'; }\n"
        "main() {\n"
        "  for arg in \"$@\"; do\n"
        "    case \"$arg\" in\n"
        "      -h|--help) usage; exit 0 ;;\n"
        "      --version) echo 'open-ended.sh 4.5.6'; exit 0 ;;\n"
        "    esac\n"
        "  done\n"
        "  echo done\n"
        "}\n"
        "main \"$@\"\n",
        encoding="utf-8",
    )
    script.chmod(0o755)
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: an undeclared open-ended parser")
    row = _payload(_run_checker(tree, "--json", "--files", "scripts/open-ended.sh"))[
        "candidates"][0]
    assert row["rejection"]["rescue_basis"] == "rejected", (
        "C-9: a script that declares nothing is judged on what it OBSERVABLY does; "
        f"rejection={row['rejection']}"
    )
    assert row["unknown_rejected"] is False, (
        "C-9: an undeclared parser that answers an unknown token with exit 0 is the violation — "
        f"the passthrough basis MUST NOT reach it; rejection={row['rejection']}"
    )


def proc_exit_red(proc) -> bool:
    """Whether a checker invocation failed (a helper so one call does not run twice)."""
    return proc.returncode != 0


# ======================================================================================
# C-20 — deterministic invocation (T047)
# ======================================================================================

#: The one field C-20 allows two runs over the same tree to disagree on.
ELAPSED_FIELD = "elapsed_ms"


def _repo_state(root: Path) -> tuple[list[str], dict[str, str]]:
    """The tree's own state: `git status --porcelain` and a digest per script.

    Read before and after an invocation so "the run wrote nothing inside the repository"
    is decided by the tree, never by the engine's own account of itself.
    """
    import hashlib

    status = _git(root, "status", "--porcelain").stdout.splitlines()
    digests = {}
    for path in sorted(root.rglob("*")):
        if path.suffix not in (".sh", ".py") or not path.is_file() or path.is_symlink():
            continue
        digests[path.relative_to(root).as_posix()] = hashlib.sha256(
            path.read_bytes()).hexdigest()
    return status, digests


def test_c20_two_runs_differ_only_in_elapsed_ms(tmp_path):
    """C-20: same tree, two `--json` runs — same ordering, same verdicts, one field apart."""
    import json

    tree = _probe_tree(tmp_path, {"scripts/deterministic.sh": None})
    before = _repo_state(tree)
    first = _run_checker(tree, "--json", "--budget-seconds", "120")
    second = _run_checker(tree, "--json", "--budget-seconds", "120")
    after = _repo_state(tree)
    assert first.returncode == second.returncode, (
        "C-20: two runs over the same tree MUST agree on the exit code; got "
        f"{first.returncode} then {second.returncode}\nstderr:\n{second.stderr[-2000:]}"
    )
    left, right = _payload(first), _payload(second)
    assert ELAPSED_FIELD in left and ELAPSED_FIELD in right, (
        f"C-20: the payload carries a measured `{ELAPSED_FIELD}`; keys: {sorted(left)}"
    )
    assert isinstance(left[ELAPSED_FIELD], int), (
        f"C-20: `{ELAPSED_FIELD}` is measured as an integer, got {left[ELAPSED_FIELD]!r}"
    )
    stripped_left = {k: v for k, v in left.items() if k != ELAPSED_FIELD}
    stripped_right = {k: v for k, v in right.items() if k != ELAPSED_FIELD}
    assert stripped_left == stripped_right, (
        "C-20: two runs over the same tree differ outside "
        f"`{ELAPSED_FIELD}` — the payload is not deterministic.\n"
        + "\n".join(
            f"  {key}: {json.dumps(stripped_left.get(key), ensure_ascii=False)[:300]} != "
            f"{json.dumps(stripped_right.get(key), ensure_ascii=False)[:300]}"
            for key in sorted(set(stripped_left) | set(stripped_right))
            if stripped_left.get(key) != stripped_right.get(key)
        )
    )
    # C-20 is about the payload a PROBING run produces: `--skip-probe` is a different mode
    # (C-16), and comparing it here would compare two labels rather than two runs.
    paths = [row["path"] for row in left["candidates"]]
    assert paths == sorted(paths), (
        f"C-20: the candidate ordering is sorted by path; got {paths[:20]}"
    )
    assert _repo_state(tree) == (before[0], before[1]) == (after[0], after[1]), (
        "C-15/C-20: the two invocations MUST leave the measured repository untouched — "
        "status or script digests changed across the runs"
    )


def test_c20_the_mirror_copy_resolves_to_its_own_root():
    """C-15: run through `.specify/scripts/python/`, the engine's root is the repository."""
    import json
    import subprocess
    import sys

    mirror = ROOT / ".specify" / "scripts" / "python" / "script-interface-check.py"
    assert mirror.is_file(), (
        f"C-15: the engine's mirror is missing: {mirror.relative_to(ROOT)} — T042's mirror "
        "obligation is projected by sync-mirrors.py"
    )
    source = subprocess.run(
        [sys.executable, str(CHECKER), "--json", "--skip-probe", "--root", str(ROOT)],
        cwd=str(ROOT), capture_output=True, text=True, timeout=300,
    )
    # The mirror is run with NO `--root`: resolving its own root IS the clause.
    through_mirror = subprocess.run(
        [sys.executable, str(mirror), "--json", "--skip-probe"],
        cwd=str(ROOT), capture_output=True, text=True, timeout=300,
    )
    assert source.returncode == 0 and through_mirror.returncode == 0, (
        "C-15: both the source and its mirror answer `--skip-probe` at exit 0; got "
        f"{source.returncode} / {through_mirror.returncode}\n"
        f"stderr:\n{through_mirror.stderr[-2000:]}"
    )
    from_mirror = json.loads(through_mirror.stdout)
    assert Path(from_mirror["root"]) == ROOT, (
        "C-15: the `.specify/` mirror MUST resolve the root to the parent of `.specify`, "
        f"never to `.specify` itself; got {from_mirror['root']!r}"
    )
    assert json.loads(source.stdout)["root"] == from_mirror["root"], (
        "C-15: the source and its mirror MUST agree on the root they resolved"
    )


# ======================================================================================
# C-14 … C-19, C-21, C-22 — the calling surface and the reports (T042–T046, T048, T049)
# ======================================================================================


def _subsection(text: str, heading: str) -> str:
    """One ATX section's body, whatever its level: everything up to the next same-or-higher
    heading. The owner page nests its classification rules under `## 1.` in `### 1.x`
    subsections, so the level is part of the heading the caller passes."""
    level = len(heading) - len(heading.lstrip("#"))
    m = re.search(
        rf"^{re.escape(heading)}\s*$(.*?)(?=^#{{1,{level}}} |\Z)", text, re.M | re.S
    )
    assert m, f"section {heading!r} not found on this surface"
    return m.group(1)

#: The engine, its mirror, and the sibling engines C-14 says it must be shaped like.
ENGINE = CHECKER
ENGINE_MIRROR = ROOT / ".specify" / "scripts" / "python" / "script-interface-check.py"
SIBLING_ENGINES = (
    ROOT / "scripts" / "python" / "scan-confirmation-gates.py",
    ROOT / "scripts" / "python" / "gate-check.py",
)

#: C-18's payload keys, one entry per field the clause names.
REPORT_KEYS = ("schema", "mode", "source", "root", "candidates", "applicable", "exempt",
               "violations", "elapsed_ms", "exemptions", "exceptions", "findings",
               "projection")
REPORT_ARRAYS = ("candidates", "exemptions", "exceptions", "findings", "projection")
CANDIDATE_ROW_KEYS = ("path", "language", "applicable", "basis", "help", "help_content",
                      "version", "unknown_rejected", "zero_side_effect", "evidence")
SCHEMA_ID = "script-interface-check/1"
RUN_MODES = ("full", "subset", "screen-only", "emit-rule", "check-projection")

#: C-21's eight keys. They stay a closed set: a key may be added to the rule on purpose, but
#: none of the eight may disappear, so the assertion below tests superset AND these eight.
RULE_KEYS = ("labels", "flag_forms", "separator", "version_line", "version_source",
             "exempt_basis", "findings", "exceptions")

#: The four keys US6 publishes so the owner page's own guard can compare the run against the
#: page rather than against prose: C-30's recomputation limbs, C-3's three refused criteria
#: WITH the reason each is refused, and the observation that decided each file.
RULE_KEYS_US6 = ("exception_limbs", "forbidden_criteria", "forbidden_criteria_reason",
                 "decided_by", "observations")

#: The standard library, by top-level module name. C-14 forbids a third-party import; this
#: list is written once here so a dependency creeping in is caught by name, never by luck.
STDLIB = frozenset("""__future__ argparse ast collections contextlib csv dataclasses
datetime difflib enum fnmatch glob hashlib importlib io itertools json logging math os
pathlib platform posixpath re shlex shutil signal socket stat string struct subprocess sys
tempfile textwrap time traceback types typing unicodedata urllib uuid warnings zipfile""".split())

#: The four labels a help body owes (C-7), read as the help probe asserts them rather than
#: typed a second time: the keys of the engine's own `HELP_LABEL_PATTERNS`.
HELP_LABEL_KEYS = ("usage", "options", "side-effects", "exit-codes")


def _engine_source() -> str:
    assert ENGINE.is_file(), f"the engine is missing: {ENGINE.relative_to(ROOT)}"
    return ENGINE.read_text(encoding="utf-8")


def _run_engine(*args: str, timeout: int = 300):
    """Run the engine as a SCRIPT (not a module), so its own shape is what is measured."""
    import subprocess
    import sys

    return subprocess.run([sys.executable, str(ENGINE), *args],
                          cwd=str(ROOT), capture_output=True, text=True, timeout=timeout)


def test_c14_the_engine_has_the_sibling_engines_shape():
    """C-14: shebang, a docstring naming usage and exit codes, the future import, `main`."""
    text = _engine_source()
    lines = text.splitlines()
    assert lines[0].startswith("#!"), (
        f"C-14: the engine opens with a shebang; line 1 is {lines[0]!r}"
    )
    parts = text.split('"""')
    assert len(parts) >= 3, "C-14: the engine carries a module docstring"
    body = parts[1]
    assert "Usage" in body, "C-14: the docstring names the usage"
    assert "Exit code" in body, "C-14: the docstring names the exit codes"
    for code in ("  0  ", "  1  ", "  2  "):
        assert code in body, f"C-14: the docstring documents exit code {code.strip()!r}"
    assert "from __future__ import annotations" in text, (
        "C-14: the engine carries `from __future__ import annotations`"
    )
    assert re.search(r"^def main\(argv: Optional\[Sequence\[str\]\] = None\) -> int:$",
                     text, re.M), "C-14: the engine exposes `main(argv=None) -> int`"
    assert 'if __name__ == "__main__":\n    sys.exit(main())' in text, (
        "C-14: the engine ends with the `__main__` tail"
    )
    for sibling in SIBLING_ENGINES:
        assert sibling.is_file(), f"C-14's reference engine is missing: {sibling}"
        assert sibling.read_text(encoding="utf-8").splitlines()[0].startswith("#!"), (
            f"the reference engine {sibling.name} has lost the shape C-14 cites"
        )
    imported = re.findall(r"^(?:import|from) ([A-Za-z0-9_.]+)", text, re.M)
    third_party = sorted({
        name for name in imported if name.split(".")[0] not in STDLIB
    })
    assert not third_party, (
        f"C-14: the engine imports nothing outside the standard library; got {third_party}"
    )


def _help_label_hits(text: str) -> dict:
    """The four labels, judged by the ENGINE's own patterns (never a second copy).

    Reading the patterns out of the engine rather than retyping them is what keeps this
    guard from becoming a parallel definition of C-7: if the engine's label set changes, the
    guard changes with it — and `test_c21` compares that set against the owner page.
    """
    namespace: dict = {"__name__": "_label_probe"}
    import importlib.util

    spec = importlib.util.spec_from_file_location("_label_probe_engine", ENGINE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return {name: bool(re.search(pattern, text))
            for name, pattern in module.HELP_LABEL_PATTERNS.items()}


def test_c14_the_engine_answers_its_own_two_flags():
    """C-14 / C-15: the engine obeys the contract it checks — `--help` and `--version`."""
    help_proc = _run_engine("--help")
    assert help_proc.returncode == 0, f"C-14: `--help` exits 0, got {help_proc.returncode}"
    body = help_proc.stdout
    hits = _help_label_hits(body)
    assert set(hits) == set(HELP_LABEL_KEYS), (
        f"the engine's label set changed under this guard: {sorted(hits)}"
    )
    assert all(hits.values()), (
        "C-14: the engine's own `--help` owes the same four labels it demands of every other "
        f"script; missing: {sorted(name for name, ok in hits.items() if not ok)}\n{body}"
    )
    version_proc = _run_engine("--version")
    assert version_proc.returncode == 0, (
        f"C-14: `--version` exits 0, got {version_proc.returncode}"
    )
    lines = version_proc.stdout.splitlines()
    assert len(lines) == 1, f"C-14: `--version` is one line, got {lines}"
    assert lines[0].startswith(Path(ENGINE).name + " "), (
        f"C-14: the version line is `<script-name> <version>`; got {lines[0]!r}"
    )


def test_c15_the_engine_writes_nothing_inside_the_repository():
    """C-15: a real screen run leaves `git status` and every script digest untouched."""
    import hashlib
    import subprocess

    def snapshot():
        status = subprocess.run(["git", "status", "--porcelain"], cwd=str(ROOT),
                                capture_output=True, text=True).stdout.splitlines()
        digests = {}
        for path in sorted(ROOT.rglob("*")):
            if path.suffix not in (".sh", ".py") or not path.is_file():
                continue
            if ".specify/.tmp" in path.as_posix():
                continue
            digests[path.relative_to(ROOT).as_posix()] = hashlib.sha256(
                path.read_bytes()).hexdigest()
        return status, digests

    before = snapshot()
    proc = _run_engine("--json", "--skip-probe", "--budget-seconds", "1")
    after = snapshot()
    assert proc.returncode in (0, 1), (
        f"C-15: `--skip-probe` is a real mode, not a crash; got {proc.returncode}\n"
        f"stderr:\n{proc.stderr[-2000:]}"
    )
    assert after == before, (
        "C-15: the invocation MUST write nothing inside the repository; changed: "
        f"status={sorted(set(after[0]) - set(before[0]))} "
        f"files={sorted(k for k in after[1] if before[1].get(k) != after[1][k])}"
    )


def test_c16_the_argument_surface_and_its_one_combination_error(tmp_path):
    """C-16: eight flags, one exit-2 combination, and argparse rejects the unknown one."""
    help_proc = _run_engine("--help")
    for flag in ("--root", "--json", "--files", "--emit-rule", "--skip-probe", "--sandbox",
                 "--budget-seconds", "--check-projection"):
        assert flag in help_proc.stdout, f"C-16: the help body must declare {flag}"
    tree = _scenario_tree(tmp_path)
    combination = _run_checker(tree, "--emit-rule", "--files", "scripts/tool.sh")
    assert combination.returncode == 2, (
        "C-16: `--emit-rule` with `--files` is an argument error at exit 2, got "
        f"{combination.returncode}"
    )
    unknown = _run_checker(tree, "--no-such-option")
    assert unknown.returncode == 2, (
        f"C-16: an undeclared option is rejected by argparse at exit 2, got {unknown.returncode}"
    )
    not_a_repo = tmp_path / "not-a-repo"
    not_a_repo.mkdir()
    empty = _run_checker(not_a_repo, "--json", "--skip-probe")
    assert empty.returncode == 0, (
        "C-17: `--root` pointing at an EMPTY directory is a valid walk-only repository, "
        f"not an argument error; got {empty.returncode}"
    )
    # `_run_checker` runs with `cwd=root`, so the missing path is passed through `--root`
    # against the tree that DOES exist.
    missing = _run_checker(str(tree), "--root", str(tmp_path) + "/does-not-exist",
                           "--json", "--skip-probe")
    assert missing.returncode == 2, (
        "C-17: `--root` not a directory is an environment error at exit 2, got "
        + str(missing.returncode) + "\nstderr:\n" + missing.stderr[-800:]
    )


def test_c17_the_exit_code_is_derived_from_the_report(tmp_path):
    """C-17: 0 / 1 / 2 each follow from what the payload itself says."""
    tree = _compliant_tree(tmp_path, "green.sh")
    green = _payload(_run_checker(tree, "--json", "--files", "scripts/green.sh"))
    # `_scenario_tree` seeds one ignored file on purpose (C-1); that note is `resolved` and
    # never red, so the assertion is about the UNRESOLVED findings and the counts.
    unresolved = [f for f in green["findings"] if not f.get("resolved")]
    named = {v["path"] for v in green["violation_rows"]}
    # `--files` narrows the SCREEN; the coverage assertion (C-2) still walks the whole tree,
    # which is the point of the clause. So the tree must be clean and the named file must not
    # be one of its violations.
    assert "scripts/green.sh" not in named, (
        f"C-17: the named compliant scenario reports no violation; got {green['violation_rows']}"
    )
    assert not unresolved, (
        f"C-17: a compliant scenario tree is green; unresolved findings: "
        f"{[f['kind'] for f in unresolved]}"
    )
    # The red control is the SAME fixture as the green one with its flag surface removed: the
    # scenario declares a write-triggering option (`good_bash`'s annotation), so it is a
    # REQUIRED candidate and the four flag limbs are what is being failed. A script the checker
    # files as `optional-read-only` would owe none of them and could never go red here.
    red_tree = _scenario_tree(tmp_path / "red")
    (red_tree / "scripts" / "bare.sh").write_text(
        _flapless_bash("bare.sh", "4.5.6"), encoding="utf-8")
    (red_tree / "scripts" / "bare.sh").chmod(0o755)
    _git(red_tree, "add", "-A")
    _git(red_tree, "commit", "-q", "-m", "scenario: a script with no flags")
    red_proc = _run_checker(red_tree, "--json", "--files", "scripts/bare.sh")
    red = _payload(red_proc)
    assert red["violations"] >= 1, "C-17: a script owing the flag surface is a violation"
    assert red_proc.returncode == 1, (
        f"C-17: at least one violation is exit 1, got {red_proc.returncode}"
    )


def test_c18_the_payload_carries_the_keys_and_the_row_fields(tmp_path):
    """C-18: the ten report keys, the five arrays, and every row field per array kind."""
    tree = _probe_tree(tmp_path, {"scripts/reportable.sh": None})
    payload = _payload(_run_checker(tree, "--json", "--files", "scripts/reportable.sh"))
    missing = [key for key in REPORT_KEYS if key not in payload]
    assert not missing, f"C-18: the payload is missing {missing}; keys: {sorted(payload)}"
    assert payload["schema"] == SCHEMA_ID, (
        f"C-18: the schema id is {SCHEMA_ID!r}, got {payload['schema']!r}"
    )
    assert payload["mode"] in RUN_MODES, (
        f"C-18: `mode` is one of {RUN_MODES}; got {payload['mode']!r}"
    )
    assert payload["source"] in ("tracked", "walk-only"), (
        f"C-18: `source` is tracked|walk-only; got {payload['source']!r}"
    )
    for name in REPORT_ARRAYS:
        assert isinstance(payload[name], list), (
            f"C-18: `{name}` is an array of rows; got {type(payload[name]).__name__}"
        )
    for count in ("applicable", "exempt", "violations", "elapsed_ms"):
        assert isinstance(payload[count], int), (
            f"C-18: `{count}` is an integer; got {type(payload[count]).__name__}"
        )
    row = payload["candidates"][0]
    missing_row = [key for key in CANDIDATE_ROW_KEYS if key not in row]
    assert not missing_row, (
        f"C-18: a `candidates[]` row is missing {missing_row}; carries {sorted(row)}"
    )
    assert isinstance(row["help_content"], dict), (
        f"C-18: `help_content` is a per-label mapping; got {type(row['help_content']).__name__}"
    )
    exempt_tree = _scenario_tree(tmp_path / "exempt")
    (exempt_tree / "lib" / "plain.py").write_text(
        "def add(a, b):\n    return a + b\n", encoding="utf-8")
    _git(exempt_tree, "add", "-A")
    _git(exempt_tree, "commit", "-q", "-m", "scenario: a library")
    exempt_payload = _payload(_run_checker(
        exempt_tree, "--json", "--files", "lib/plain.py"))
    if exempt_payload["exemptions"]:
        entry = exempt_payload["exemptions"][0]
        assert set(entry) >= {"path", "basis", "evidence"}, (
            f"C-18: an exemption row is a path WITH a basis and evidence; got {sorted(entry)}"
        )
        assert entry["basis"], "C-18: no exempt candidate is a bare path without a basis"


def test_c18_version_unknown_is_an_observation_not_a_violation(tmp_path):
    """C-18: `version` carries the literal `unknown` without turning the run red for it."""
    tree = tmp_path / "no-version"
    (tree / "scripts").mkdir(parents=True)
    (tree / "scripts" / "unknown.py").write_text(
        "from __future__ import annotations\n"
        "import argparse\n"
        "import sys\n"
        "from pathlib import Path\n"
        "\n"
        "\n"
        "def usage_text():\n"
        "    return ('usage: unknown.py\\n\\noptions:\\n  -h, --help  show this help\\n\\n'\n"
        "            'side-effects: none; this script writes nothing\\n'\n"
        "            'exit-codes: 0 on success, 2 on an unrecognized option\\n')\n"
        "\n"
        "\n"
        "def main(argv=None):\n"
        "    parser = argparse.ArgumentParser(add_help=False)\n"
        "    parser.add_argument('-h', '--help', action='store_true')\n"
        "    parser.add_argument('--version', action='store_true')\n"
        "    args, rest = parser.parse_known_args(argv)\n"
        "    if args.help:\n"
        "        print(usage_text())\n"
        "        return 0\n"
        "    if args.version:\n"
        "        print('unknown.py unknown')\n"
        "        return 0\n"
        "    rest = [a for a in rest if a != '--']\n"
        "    unknown = [a for a in rest if a.startswith('-')]\n"
        "    if unknown:\n"
        "        print(usage_text(), file=sys.stderr)\n"
        "        return 2\n"
        "    print('did the work')\n"
        "    return 0\n"
        "\n"
        "\n"
        "if __name__ == \"__main__\":\n"
        "    sys.exit(main())\n",
        encoding="utf-8",
    )
    payload = _payload(_run_checker(tree, "--json", "--files", "scripts/unknown.py"))
    row = payload["candidates"][0]
    assert row["version"] == "unknown.py unknown", (
        "C-18: a candidate whose `--version` line says `unknown` carries that literal in "
        f"`version`; got {row['version']!r}"
    )
    assert row["version_unknown"] is True or row.get("version_observations", {}).get(
        "unknown") is True, (
        "C-18: the `unknown` observation is recorded as one, so a reader can select on it: "
        f"{sorted(row)}"
    )
    assert not [f for f in payload["findings"] if row["path"] in f.get("paths", [])], (
        "C-18: `unknown` at exit 0 is NOT a violation — the reachable-`pyproject.toml` case "
        "is the only one that is; findings: "
        f"{[f['kind'] for f in payload['findings'] if row['path'] in f.get('paths', [])]}"
    )


def test_c19_the_human_face_prints_violations_and_always_the_summary(tmp_path):
    """C-19: one `<path>: <missing limbs>` line per violation, plus the summary ALWAYS."""
    tree = _compliant_tree(tmp_path, "human.sh")
    green = _run_checker(tree, "--files", "scripts/human.sh")
    assert green.returncode == 0, (
        f"C-19: the scenario is compliant; got {green.returncode}\n{green.stdout[-1500:]}"
    )
    summary = re.search(r"^candidates=(\d+) applicable=(\d+) exempt=(\d+) violations=(\d+)$",
                        green.stdout, re.M)
    assert summary, (
        "C-19: a run with ZERO violations still prints the summary — 'nothing printed' is "
        f"never the passing signal; output:\n{green.stdout}"
    )
    assert int(summary.group(4)) == 0, f"C-19: the summary reads violations=0; {green.stdout}"

    # Same rule as C-17: the red control is a REQUIRED candidate (it declares its write option)
    # whose flag surface is gone, so the violation is measured rather than filed as optional.
    red_tree = _scenario_tree(tmp_path / "red")
    bad = red_tree / "scripts" / "silent.sh"
    bad.write_text(_flapless_bash("silent.sh", "4.5.6"), encoding="utf-8")
    bad.chmod(0o755)
    _git(red_tree, "add", "-A")
    _git(red_tree, "commit", "-q", "-m", "scenario: a script with no flag surface")
    red = _run_checker(red_tree, "--files", "scripts/silent.sh")
    assert red.returncode == 1, f"C-19: a violation run exits 1; got {red.returncode}"
    line = [ln for ln in red.stdout.splitlines() if ln.startswith("scripts/silent.sh:")]
    assert line, (
        "C-19: a violation prints `<path>: <missing limbs>` on its own line; "
        f"output:\n{red.stdout}"
    )
    limbs = line[0].split(":", 1)[1]
    assert "help" in limbs and "version" in limbs, (
        f"C-19: the line names the missing limbs; got {limbs!r}"
    )
    assert re.search(r"^candidates=\d+ applicable=\d+ exempt=\d+ violations=\d+$",
                     red.stdout, re.M), f"C-19: the summary is printed on a red run too:\n{red.stdout}"


def test_c21_emit_rule_carries_its_eight_keys():
    """C-21: `--emit-rule` prints the rule with its eight keys (plus US6's three), at exit 0."""
    proc = _run_engine("--json", "--emit-rule")
    assert proc.returncode == 0, f"C-21: `--emit-rule` exits 0, got {proc.returncode}"
    payload = _payload(proc)
    assert payload["mode"] == "emit-rule", (
        f"C-21: the mode is `emit-rule`; got {payload['mode']!r}"
    )
    rule = payload.get("rule")
    assert isinstance(rule, dict), (
        f"C-21: `--emit-rule` carries the rule under `rule`; payload keys: {sorted(payload)}"
    )
    expected = set(RULE_KEYS) | set(RULE_KEYS_US6)
    assert set(rule) == expected, (
        f"C-21: the rule carries exactly {sorted(expected)}; got {sorted(rule)}"
    )
    assert set(RULE_KEYS) <= set(rule), (
        f"C-21: none of the eight original keys may disappear; missing "
        f"{sorted(set(RULE_KEYS) - set(rule))}"
    )
    human = _run_engine("--emit-rule")
    import json

    assert json.loads(human.stdout)["rule"] == rule, (
        "C-16/C-21: `--emit-rule` with and without `--json` produces the same payload"
    )


def test_c21_the_rule_agrees_with_the_owner_page_in_both_directions():
    """C-21: the emitted label set and class vocabulary equal the page's, both ways."""
    page = _text(OWNER)
    # Labels: the page publishes them in one paragraph (the same surface C-29's guard reads).
    page_labels = [
        name for name in re.findall(r"`([a-z][a-z-]*)`", _owner_label_line())
        if name != "labels"
    ]
    rule = _payload(_run_engine("--json", "--emit-rule"))["rule"]
    assert set(rule["labels"]) == set(page_labels), (
        "C-21: the emitted `labels` and the owner page MUST agree in both directions; "
        f"page={sorted(page_labels)} emitted={sorted(rule['labels'])}"
    )
    # Class vocabulary: the page's `basis` tokens, read back from the section that owns the
    # closed set rather than typed here. The page names the non-obvious member inline
    # (`mirror-unpaired`) and calls the rest "继承源的分类"; the set comparison below is
    # therefore "every basis the page names is one the engine's closed set carries", and the
    # engine's closed set is the thing the report draws from. A basis the page names that the
    # engine cannot produce IS the drift the clause forbids.
    # The page's classification section also names its two LANGUAGES and its two report
    # fields; those are not bases and are excluded by the engine's own closed set, which is
    # what makes this a derivation rather than a filtered guess.
    section = _subsection(page, "### 1.4 分类步骤")
    lib_names = set(_checker_module().EXEMPT_BASIS)
    page_basis = set(re.findall(r"`([a-z][a-z-]+)`", section)) & lib_names
    emitted = set(rule["exempt_basis"])
    assert page_basis, (
        "C-21: the owner page's classification section names no basis at all — the "
        f"comparison below would be vacuous; section tokens: "
        f"{sorted(set(re.findall(r'`([a-z][a-z-]+)`', section)))}"
    )
    assert page_basis <= lib_names, (
        "C-21: the owner page names a basis the engine's closed set does not carry: "
        f"{sorted(page_basis - lib_names)}"
    )
    # The page writes the closed set in prose ("inherit the source's class", "judged on its
    # own run semantics") and names only the token that has no plain-language reading, so the
    # two sides agree on that named token and on membership of the engine's own closed set —
    # never on the prose. What may not happen is the page NAMING a basis the engine cannot
    # produce (the assertion below) or the engine emitting one outside its own set (asserted
    # next).
    # Anti-vacuity both ways: every emitted basis is produced by the classifier's own table.
    lib = _checker_module()
    assert emitted <= set(lib.EXEMPT_BASIS), (
        f"C-21: the emitted bases are drawn from the engine's own closed set; "
        f"emitted={sorted(emitted)}"
    )
    # And a run reports bases out of exactly that set. The scenario is built under `tmp_path`
    # by the caller-shaped helper below, never inside the repository under test.
    import tempfile

    with tempfile.TemporaryDirectory(prefix="si-c21-", dir=_scratch_root()) as scratch:
        tree = _scenario_tree(Path(scratch))
        produced = {row["basis"] for row in _payload(
            _run_checker(tree, "--json", "--skip-probe"))["candidates"]}
    assert produced <= (emitted | {"not-classified"}), (
        f"C-21: a run's `basis` values stay inside the emitted vocabulary; got {produced}"
    )



def _scratch_root() -> str:
    """A scratch root outside the repository (C-15: a test writes nothing in the tree)."""
    import tempfile

    return tempfile.gettempdir()

def _checker_module():
    """The engine, imported by path, so a guard reads its tables instead of retyping them."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("_checker_under_guard", ENGINE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_c22_check_projection_verifies_each_declared_pair(tmp_path):
    """C-22: `mirror == source + declared projection`, idempotent, mismatch names the pair."""
    tree = _scenario_tree(tmp_path)
    source_body = (
        "def main():\n"
        "    return 0\n"
        "\n"
        "\n"
        'if __name__ == "__main__":\n'
        "    raise SystemExit(main())\n"
    )
    source = tree / "scripts" / "projected.py"
    source.write_text(source_body, encoding="utf-8")
    # The declaration owns the rule (C-34), so the scenario's declaration carries a real one:
    # `PROJECTED_FILES` names the pair and `project_source(source_text, kind)` returns
    # `(mirror_text, applied)`.
    declaration = tree / "scripts" / "python" / "sync-mirrors.py"
    declaration.parent.mkdir(parents=True, exist_ok=True)
    declaration.write_text(
        "PROJECTED_FILES = (('.specify/scripts/projected.py', 'python-version-bridge'),)\n"
        "\n"
        "\n"
        "def project_source(source_text, kind):\n"
        "    anchor = 'if __name__ == \"__main__\":'\n"
        "    if anchor not in source_text:\n"
        "        return source_text, False\n"
        "    block = '# projected: ' + kind + '\\n'\n"
        "    index = source_text.find(anchor)\n"
        "    return source_text[:index] + block + source_text[index:], True\n",
        encoding="utf-8")
    mirror = tree / ".specify" / "scripts" / "projected.py"
    mirror.parent.mkdir(parents=True)
    # Case 1: the mirror is NOT `source + declared projection` (it carries the projection, but
    # at the head of the file instead of before the `__main__` anchor).
    mirror.write_text("# hand-edited\n" + source_body, encoding="utf-8")
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: a projected pair")
    red = _run_checker(tree, "--json", "--check-projection")
    payload = _payload(red)
    kinds = _finding_kinds(payload)
    assert "projection-mismatch" in kinds, (
        f"C-22: a mirror that is not `source + declared projection` is `projection-mismatch`; "
        f"findings: {kinds}"
    )
    assert red.returncode == 1, f"C-22: the mismatch exits 1, got {red.returncode}"
    named = [p for f in payload["findings"] for p in f.get("paths", [])]
    assert any("projected.py" in p for p in named), (
        f"C-22: the mismatch MUST name the pair; named: {named}"
    )
    assert payload["projection"], (
        "C-22: the verdict is reported per declared pair in `projection[]`; it is empty"
    )
    entry = payload["projection"][0]
    assert entry["status"] == "mismatch", (
        f"C-22: the pair's own status says what happened; got {entry['status']!r}"
    )
    assert entry["idempotent"] is True, (
        "C-22: re-applying the projection is idempotent; "
        f"the pair reports idempotent={entry['idempotent']!r}"
    )

    # Case 2: the mirror IS `source + declared projection` — the same invocation turns green.
    index = source_body.find('if __name__ == "__main__":')
    mirror.write_text(
        source_body[:index] + "# projected: python-version-bridge\n" + source_body[index:],
        encoding="utf-8")
    green = _run_checker(tree, "--json", "--check-projection")
    green_payload = _payload(green)
    assert green.returncode == 0, (
        "C-22: `source + declared projection` is the passing state; got "
        f"{green.returncode}\n{green.stdout[:1500]}"
    )
    assert green_payload["projection"][0]["status"] == "ok", (
        "C-22: the pair reports `ok` once it holds; got "
        f"{green_payload['projection'][0]['status']!r}"
    )


def test_c22_a_declaration_without_the_anchor_fails_loudly(tmp_path):
    """C-22 / C-34: a refused projection is named, never silently reported as `ok`."""
    tree = _scenario_tree(tmp_path)
    (tree / "scripts" / "noanchor.py").write_text("value = 1\n", encoding="utf-8")
    declaration = tree / "scripts" / "python" / "sync-mirrors.py"
    declaration.parent.mkdir(parents=True, exist_ok=True)
    declaration.write_text(
        "PROJECTED_FILES = (('.specify/scripts/noanchor.py', 'python-version-bridge'),)\n"
        "\n"
        "\n"
        "def project_source(source_text, kind):\n"
        "    anchor = 'if __name__ == \"__main__\":'\n"
        "    if anchor not in source_text:\n"
        "        return 'anchor missing: ' + anchor, False\n"
        "    return source_text, True\n",
        encoding="utf-8")
    mirror = tree / ".specify" / "scripts" / "noanchor.py"
    mirror.parent.mkdir(parents=True)
    mirror.write_text("value = 1\n", encoding="utf-8")
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: an unprojectable pair")
    proc = _run_checker(tree, "--json", "--check-projection")
    payload = _payload(proc)
    assert proc.returncode == 1, (
        f"C-22/C-34: a projection the owner refuses exits 1, got {proc.returncode}"
    )
    entry = payload["projection"][0]
    assert entry["status"] != "ok", (
        "C-34: a refused projection MUST NOT be reported as `ok`; got "
        f"{entry['status']!r}"
    )
    assert any("anchor missing" in problem for problem in entry["problems"]), (
        f"C-34: the failure names its anchor; problems={entry['problems']}"
    )


# ======================================================================================
# C-33 … C-38 — the declared projection, its marker, and the frame (T050–T054)
# ======================================================================================

SYNC = ROOT / "scripts" / "python" / "sync-mirrors.py"
SYNC_MIRROR = ROOT / ".specify" / "scripts" / "python" / "sync-mirrors.py"
HELPER = ROOT / "scripts" / "python" / "script_interface_cli.py"


def _sync_module():
    """The projection ENGINE, imported by path: the declaration is read, never retyped."""
    import importlib.util

    assert SYNC.is_file(), f"the projection engine is missing: {SYNC.relative_to(ROOT)}"
    spec = importlib.util.spec_from_file_location("_sync_mirrors_under_guard_086", SYNC)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_sync(*args: str):
    """Run `sync-mirrors.py` with the repository as its own root (never a scenario tree)."""
    return run_engine_in_process(SYNC, args)


def test_c34_the_projection_rule_is_declared_once_and_names_its_rows():
    """C-34: ONE table names each projected mirror, its kind and its source."""
    engine = _sync_module()
    table = engine.PROJECTED_FILES
    assert table, "C-34: the declaration table is empty — nothing is projected"
    kinds = set(engine.PROJECTION_KINDS)
    assert kinds == {"python-version-bridge", "bash-version-guard"}, (
        f"C-34: the contract's kind set is closed at two; the engine declares {sorted(kinds)}"
    )
    mirrors = []
    for row in table:
        assert len(row) == 3, (
            f"C-34: a row is (mirror, kind, source), not {len(row)} fields: {row!r}"
        )
        mirror, kind, source = row
        assert kind in kinds, f"C-34: row {mirror} carries an undeclared kind {kind!r}"
        assert mirror.startswith(".specify/"), (
            f"C-34: a declared row names the MIRROR; got {mirror!r}"
        )
        assert (ROOT / source).is_file(), f"C-34: row {mirror} names a missing source {source}"
        mirrors.append(mirror)
    assert len(mirrors) == len(set(mirrors)), (
        f"C-34: a mirror is declared twice: {mirrors}"
    )
    # Anti-vacuity: the declaration is a REAL rule, not a table nobody consults. Every
    # declared mirror exists on disk and its source pair is inside the `scripts` mirror tree.
    for mirror in mirrors:
        assert (ROOT / mirror).is_file(), (
            f"C-34: declared mirror {mirror} does not exist — the projection never ran"
        )


def test_c34_the_projection_is_idempotent_and_refuses_a_missing_anchor():
    """C-34: applying twice equals applying once; a missing anchor is a named refusal."""
    engine = _sync_module()
    python_source = (
        "def main():\n"
        "    return 0\n"
        "\n"
        "\n"
        'if __name__ == "__main__":\n'
        "    raise SystemExit(main())\n"
    )
    once, applied = engine.project_source(python_source, "python-version-bridge")
    assert applied is True, f"C-34: a source with the anchor MUST project; reason: {once}"
    twice, applied_twice = engine.project_source(once, "python-version-bridge")
    assert applied_twice is True and twice == once, (
        "C-34: the projection MUST be idempotent — a second application changed bytes"
    )
    anchor_index = once.find('if __name__ == "__main__":')
    block_index = once.find(engine._marker("python-version-bridge"))
    assert 0 <= block_index < anchor_index, (
        "C-34: the Python bridge MUST be inserted BEFORE the `__main__` anchor; "
        f"marker at {block_index}, anchor at {anchor_index}"
    )

    bash_source = "#!/usr/bin/env bash\nmain() { :; }\nmain\n"
    guarded, bash_applied = engine.project_source(bash_source, "bash-version-guard")
    assert bash_applied is True and guarded.startswith("#!"), (
        "C-34: the bash guard MUST follow the shebang, ahead of everything else"
    )
    assert guarded.splitlines()[0] == bash_source.splitlines()[0], (
        "C-34: the shebang stays the first line"
    )
    assert engine.project_source(guarded, "bash-version-guard")[0] == guarded, (
        "C-34: the bash projection MUST be idempotent"
    )

    # The refusal half: no anchor, no silent end-of-file append, one named reason.
    reason, applied = engine.project_source("value = 1\n", "python-version-bridge")
    assert applied is False, (
        "C-34: a source without the `__main__` anchor MUST be refused, never projected"
    )
    assert 'if __name__ == "__main__":' in reason, (
        f"C-34: the refusal names its anchor; got {reason!r}"
    )
    reason_bash, applied_bash = engine.project_source("no shebang here\n",
                                                      "bash-version-guard")
    assert applied_bash is False and "shebang" in reason_bash, (
        f"C-34: a shebang-less source is refused by name; got {reason_bash!r}"
    )
    unknown, applied_unknown = engine.project_source("x = 1\n", "third-kind")
    assert applied_unknown is False and "third-kind" in unknown, (
        "C-34: a kind outside the closed set is refused by name"
    )


def test_c35_the_check_asserts_the_projection_and_names_its_kind():
    """C-35: `--check` compares `mirror == project(source)` and names the kind per pair."""
    engine = _sync_module()
    proc = _run_sync("--check")
    assert proc.returncode == 0, (
        "C-35: the repository's own mirrors MUST pass `--check` (exit 0); got "
        f"{proc.returncode}\n{proc.stdout[-3000:]}\n{proc.stderr[-1500:]}"
    )
    # The projected verdict is its own line, named per pair — it is never folded into the
    # byte-equality sentence.
    for mirror, kind, _source in engine.PROJECTED_FILES:
        assert f"projected[{kind}] {mirror} <-" in proc.stdout, (
            "C-35: the check output MUST name the projection kind for each projected pair; "
            f"no line for {mirror} ({kind}).\n{proc.stdout[-2000:]}"
        )
    assert "files, byte-identical" in proc.stdout, (
        "C-35: the byte-equality half keeps its own named verdict; "
        f"output:\n{proc.stdout[-2000:]}"
    )
    # And the comparison really is the projection: for a projected pair the two files on
    # disk differ, which byte equality would have called drift.
    for mirror, _kind, source in engine.PROJECTED_FILES:
        assert (ROOT / mirror).read_bytes() != (ROOT / source).read_bytes(), (
            f"C-35: {mirror} is byte-identical to {source} — the declaration claims a "
            "projection the files do not carry, so this assertion would be vacuous"
        )
    # Byte equality still applies everywhere else: a plain mirrored file is identical.
    for source, mirror in (("shared/definitions/script-interface-definitions.md",
                            ".specify/shared/definitions/script-interface-definitions.md"),
                           ("scripts/python/feedback-utils.py",
                            ".specify/scripts/python/feedback-utils.py")):
        assert (ROOT / source).read_bytes() == (ROOT / mirror).read_bytes(), (
            f"C-35: the non-projected half stays byte-identical: {mirror}"
        )


def test_c36_the_projection_is_self_sufficient(tmp_path):
    """C-36: the mirror answers its own flags, and prints `unknown` without a project root."""
    import shutil
    import subprocess
    import sys

    engine = _sync_module()
    helper = ROOT / "scripts" / "python" / "script_interface_cli.py"
    projected, applied = engine.project_source(helper.read_text(encoding="utf-8"),
                                               "python-version-bridge")
    assert applied is True, f"C-36: the helper projects; reason: {projected}"

    # A downstream project: a copy with a `pyproject.toml` beside it and no source sibling.
    downstream = tmp_path / "downstream"
    (downstream / "scripts").mkdir(parents=True)
    (downstream / "pyproject.toml").write_text(
        '[project]\nname = "downstream"\nversion = "7.7.7"\n', encoding="utf-8")
    (downstream / ".git").mkdir()
    copy = downstream / "scripts" / "helper.py"
    copy.write_text(projected, encoding="utf-8")
    version = subprocess.run([sys.executable, str(copy), "--version"], cwd=str(downstream),
                             capture_output=True, text=True, timeout=120)
    assert version.returncode == 0, (
        f"C-36: the projected copy MUST answer `--version` at exit 0; got "
        f"{version.returncode}: {version.stderr[-800:]}"
    )
    assert version.stdout.strip() == "helper.py 7.7.7", (
        "C-36: the bridge re-derives the version from the pyproject.toml beside the script; "
        f"got {version.stdout.strip()!r}"
    )
    helped = subprocess.run([sys.executable, str(copy), "--help"], cwd=str(downstream),
                            capture_output=True, text=True, timeout=120)
    assert helped.returncode == 0 and helped.stdout.strip(), (
        f"C-36: `--help` MUST still reach the script's own parser; got {helped.returncode}"
    )

    # No project root anywhere: `unknown`, exit 0 — an observation, never a failure.
    orphan_root = tmp_path / "orphan"
    (orphan_root / "bin").mkdir(parents=True)
    orphan = orphan_root / "bin" / "helper.py"
    orphan.write_text(projected, encoding="utf-8")
    unknown = subprocess.run([sys.executable, str(orphan), "--version"], cwd=str(orphan_root),
                             capture_output=True, text=True, timeout=120)
    assert unknown.returncode == 0, (
        f"C-36: an unreachable version source still exits 0; got {unknown.returncode}"
    )
    assert unknown.stdout.strip() == "helper.py unknown", (
        f"C-36: with no pyproject.toml the line is `<name> unknown`; got "
        f"{unknown.stdout.strip()!r}"
    )

    # The rule the search agrees on: the bridge and the shipped helper are one rule.
    assert "pyproject.toml" in projected and '".git"' in projected, (
        "C-36: the bridge's own search must require the same two anchors as the helper"
    )


def test_c37_the_strictness_flags_are_unchanged():
    """C-37: `strict_extras` keeps its measured value per pair; the projection touches none."""
    engine = _sync_module()
    measured = {src: strict for src, _d, strict, _e in engine.MIRROR_PAIRS}
    assert measured == {
        "templates": False,
        "skills/external": False,
        "skills/internal": False,
        "agents": False,
        "scripts": True,
        "shared": False,
    }, (
        "C-37: the strictness flags are per-pair measurements and MUST NOT move with the "
        f"projection; got {measured}"
    )
    assert set(engine.PROJECTION_STRICTNESS) == set(measured.items()), (
        "C-37: the declaration reads its strictness out of MIRROR_PAIRS; a second copy "
        f"would drift. declared={engine.PROJECTION_STRICTNESS}"
    )
    # The frame rule is exercised on real pairs, not merely declared (C-37's second half).
    for mirror, kind, source in engine.PROJECTED_FILES:
        problems = engine.frame_violations(
            (ROOT / source).read_text(encoding="utf-8"),
            (ROOT / mirror).read_text(encoding="utf-8"),
            kind,
        )
        assert problems == [], (
            f"C-37/C-38: the pair {mirror} breaks the frame rule: {problems}"
        )


def test_c33_no_mirror_is_hand_edited_and_c38_each_carries_one_marker():
    """C-33/C-38: the mirrors are generated, and each projected one carries one marker."""
    engine = _sync_module()
    # C-38: the marker is READ BACK OUT of the mirrors on disk — never authored here. The
    # marker text comes from the engine, the counts from the files, and the two must meet.
    for mirror, kind, _source in engine.PROJECTED_FILES:
        text = (ROOT / mirror).read_text(encoding="utf-8")
        # The marker is compared by its BODY: the emitted line carries a `# ` comment
        # prefix, which is the comment syntax the projection puts it in.
        marker = engine._marker(kind)
        hits = [line for line in text.splitlines()
                if line.strip().lstrip("#").strip() == marker]
        assert len(hits) == 1, (
            f"C-38: {mirror} MUST carry exactly one {kind!r} marker line; found {len(hits)}"
        )
        # The claim is judged on COMMENT lines only, which is the surface a reader sees: a
        # string literal or an identifier is a different thing, and the engine's own frame
        # check reads the same lines.
        comments = [line.lower() for line in text.splitlines()
                    if line.lstrip().startswith("#")]
        assert not any("byte-identical" in line for line in comments), (
            f"C-38: {mirror} MUST NOT claim byte identity with its source"
        )
    # C-33: no mirror is hand-edited. The engine reproduces every projected byte from its
    # source, so a hand-written mirror is exactly a mirror the projection cannot reproduce.
    proc = _run_sync("--check")
    assert "DIFF" not in proc.stdout, (
        "C-33: a mirror that departs from its declared projection is hand-edited; "
        f"`--check` reports:\n{proc.stdout[-2000:]}"
    )
    # And the marker is a PROJECTION artefact: the sources do not carry it.
    for mirror, kind, source in engine.PROJECTED_FILES:
        source_text = (ROOT / source).read_text(encoding="utf-8")
        assert engine._marker(kind) not in source_text, (
            f"C-33: the marker belongs to the mirror, not to {source}"
        )
    # The prohibition is stated where a generator and a reader both meet it.
    assert "never hand-edit" in engine.MARKER_TEMPLATE or all(
        "never hand-edit" in (ROOT / mirror).read_text(encoding="utf-8")
        for mirror, _k, _s in engine.PROJECTED_FILES
    ), "C-33: the marker states the hand-edit prohibition it enforces"



# ======================================================================================
# Supplementary (2026-11-08 RCA) — the probe sandbox must not write the measured repo
# ======================================================================================


def _signature(tree: Path):
    """The measured repository's observable state: refs, branch and spec-dir names."""
    refs = _git(tree, "for-each-ref", "--format=%(refname)").stdout
    branch = _git(tree, "rev-parse", "--abbrev-ref", "HEAD").stdout
    specs = sorted(
        p.name for p in (tree / ".specify" / "specs").iterdir()
    ) if (tree / ".specify" / "specs").is_dir() else []
    return (refs, branch, tuple(specs))


def _engine_module():
    import importlib.util

    spec = importlib.util.spec_from_file_location("_sandbox_boundary_engine", CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _leaky_tree(tmp_path: Path, absolute_root: Path | None = None) -> Path:
    """A tree whose one script writes a branch and a spec dir at its resolved repo root."""
    tree = _scenario_tree(tmp_path)
    if absolute_root is not None:
        root_expr = "'%s'" % absolute_root
    else:
        root_expr = '$(git rev-parse --show-toplevel 2>/dev/null || pwd)'
    script = tree / "scripts" / "leaky.sh"
    script.write_text(
        "#!/usr/bin/env bash\n"
        "set -e\n"
        "root=%s\n"
        "mkdir -p \"$root/.specify/specs/999-probe-leak\" 2>/dev/null || true\n"
        "git -C \"$root\" branch probe-leak 2>/dev/null || true\n"
        "echo leaky\n" % root_expr,
        encoding="utf-8",
    )
    script.chmod(0o755)
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: leaky probe candidate")
    return tree


def test_supplementary_probe_env_pins_the_git_boundary(tmp_path):
    """T088: a probe's environment stops the repo-root search at the sandbox."""
    engine = _engine_module()
    sandbox = tmp_path / "sandbox"
    sandbox.mkdir()
    env = engine._probe_env(sandbox)
    ceiling = env.get("GIT_CEILING_DIRECTORIES", "")
    assert str(sandbox) in ceiling or str(sandbox / "tree") in ceiling, (
        "T088: the probe environment must pin GIT_CEILING_DIRECTORIES to the sandbox; "
        f"got {ceiling!r}"
    )
    assert str(sandbox) in env.get("TMPDIR", ""), (
        "T088: a probe's temp files must land inside the sandbox; "
        f"got TMPDIR={env.get('TMPDIR')!r}"
    )


def test_supplementary_a_probe_never_writes_the_measured_repository(tmp_path):
    """T090(b): a candidate that writes at its resolved root must not reach the measured tree."""
    tree = _leaky_tree(tmp_path)
    before = _signature(tree)
    _run_checker(tree, "--json", "--files", "scripts/leaky.sh")
    after = _signature(tree)
    assert before == after, (
        "T089/T090: the probe wrote the measured repository (branch/spec drift).\n"
        f"before={before}\nafter={after}"
    )


def test_supplementary_an_escape_is_reported_not_silently_accepted(tmp_path):
    """T090(c): an absolute-path escape is a probe-escaped finding at exit 1."""
    tree = _leaky_tree(tmp_path, absolute_root=tmp_path / "measured")
    # Point the script at the measured tree itself.
    script = tree / "scripts" / "leaky.sh"
    text = script.read_text(encoding="utf-8").replace(str(tmp_path / "measured"), str(tree))
    script.write_text(text, encoding="utf-8")
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: absolute-path escape")
    proc = _run_checker(tree, "--json", "--files", "scripts/leaky.sh")
    payload = _payload(proc)
    kinds = [f.get("kind") for f in payload.get("findings", [])]
    assert "probe-escaped" in kinds, (
        "T089/T090: a probe that changes the measured repository must surface a "
        f"`probe-escaped` finding; findings={kinds}"
    )
    assert proc.returncode == 1, (
        f"T089: an escaped probe is red; got exit {proc.returncode}"
    )


# ======================================================================================
# US6 — the exemption criterion and the register's recomputation (T067 … T072)
# ======================================================================================

#: The owner page a scenario register lives on. Both spellings are read by the engine: the
#: source page first, the `.specify/` projection second (C-30's "downstream project" half).
REGISTER_PAGE = "shared/definitions/script-interface-definitions.md"

REGISTER_SECTION = """## Declared Exceptions

{body}

**复算判据**: the four limbs below are recomputed; a failing row is `exception-unverifiable`.

| path | skill | unsatisfied clause | handling |
|------|-------|--------------------|----------|
{rows}
"""

EMPTY_REGISTER_ROWS = "| none | — | — | — |"


def _register_tree(tmp_path: Path, rows: str) -> Path:
    """A scenario tree carrying one `## Declared Exceptions` register with `rows` in it."""
    tree = _scenario_tree(tmp_path)
    page = tree / REGISTER_PAGE
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(REGISTER_SECTION.format(body="", rows=rows), encoding="utf-8")
    return tree


def _external_skill(tree: Path, skill: str, classification: str = "external",
                    body: str = "#!/usr/bin/env bash\necho upstream verbatim\n") -> Path:
    """A third-party skill under `skills/external/`, carrying its own machine mark."""
    root = tree / "skills" / "external" / skill
    (root / "scripts").mkdir(parents=True, exist_ok=True)
    (root / "SKILL.md").write_text(
        "---\nname: %s\nclassification: %s\n---\n" % (skill, classification),
        encoding="utf-8",
    )
    script = root / "scripts" / "verbatim.sh"
    script.write_text(body, encoding="utf-8")
    script.chmod(0o755)
    return root


def _verbatim_required(name: str) -> str:
    """An upstream-shaped script that DOES act: it declares the option it writes through.

    V-15's subject is a third-party file that owes the flag surface, so the fixture carries the
    declaration the checker reads (`(triggers the write)` on a printed usage line). That is what
    makes it a REQUIRED candidate — and a required candidate nobody registered is red for its
    missing limbs, whatever directory it sits in.
    """
    return (
        "#!/usr/bin/env bash\n"
        "usage() {\n"
        '  echo "usage: %s [--out PATH]"\n'
        '  echo "options:"\n'
        '  echo "  --out PATH  where to write (triggers the write)"\n'
        "}\n"
        'echo "upstream verbatim"\n' % name
    )


def _commit(tree: Path, message: str) -> None:
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", message)


def _exceptions(payload: dict) -> dict:
    return {str(row.get("path", "")): row for row in payload.get("exceptions", [])}


def test_c3_no_file_is_decided_from_a_forbidden_criterion(tmp_path):
    """C-3 / T067: every row names the RUN that decided it, never one of the three refusals.

    The engine MUST carry the forbidden vocabulary — so a reader can check a file against the
    list — and MUST record, per row, which observation actually decided it. `self-description`
    is exercised by a library whose own docstring says "this is a library": the docstring is the
    author's claim, and the row must not repeat it as the reason.
    """
    emitted = json.loads(_run_engine("--emit-rule", "--root", str(ROOT)).stdout)
    criteria = emitted["rule"]["forbidden_criteria"]
    assert list(criteria) == ["top-level-statements", "shebang-word", "self-description"], (
        f"C-3: the three refused criteria are named in the emitted rule; got {criteria}"
    )
    for name in criteria:
        reason = emitted["rule"]["forbidden_criteria_reason"][name]
        assert reason.strip(), f"C-3: {name} is named as refused WITH a reason; got {reason!r}"
    observations = emitted["rule"]["observations"]
    assert observations, "C-3/C-12: the report publishes the observations a row may record"

    tree = _probe_tree(tmp_path, {})
    library = tree / "lib" / "claims_to_be_a_library.py"
    library.write_text(
        '"""A library — the file says so itself, which is exactly what C-3 refuses."""\n'
        "def helper():\n    return 1\n"
        "\n"
        "print(helper())\n",
        encoding="utf-8",
    )
    _commit(tree, "scenario: a self-described library")
    proc = _run_checker(tree, "--json", "--files", "lib/claims_to_be_a_library.py")
    row = _payload(proc)["candidates"][0]
    assert row["decided_by"] in ("run-semantics", "inherited-from-source"), (
        "C-3: the class came from a run; got "
        f"decided_by={row['decided_by']!r} evidence={row.get('evidence')!r}"
    )
    assert row["observed"] in observations, (
        f"C-3: the observation is one the rule publishes; got {row['observed']!r}"
    )
    assert "library" not in str(row.get("observed", "")), (
        "C-3: the file's own description MUST NOT be the observation; got "
        f"{row['observed']!r}"
    )


def test_c3_a_file_with_nothing_to_instrument_is_unobserved_not_exempted(tmp_path):
    """C-3 / C-12 / T067 + T068: no position ⇒ `unevaluated` at exit 1, naming the limb.

    A file whose every top-level statement is an import or a definition yields no action
    position. Reading its class off "there is no top-level statement" is precisely the
    criterion C-3 forbids, so the row is NOT an exemption: it is `unevaluated`, and C-12
    requires that state to be a violation naming its missing limb. It MUST NOT disappear from
    the counts either — that is C-12's "no silent omission".
    """
    tree = _probe_tree(tmp_path, {"scripts/good.sh": None})
    # `lib/helper.py` belongs to the scenario's own fixtures; this case needs the candidate to
    # be the tree's ONLY module of its kind in the subset.
    definitions_only = tree / "lib" / "scope" / "nothing_to_observe.py"
    definitions_only.parent.mkdir(parents=True, exist_ok=True)
    definitions_only.write_text(
        "# A module comment. No shebang, no import, no class, no call — a `.py` whose whole\n"
        "# content is commentary has nothing a run could put a marker behind.\n",
        encoding="utf-8",
    )
    _commit(tree, "scenario: a file with no action position")
    proc = _run_checker(tree, "--json", "--files", "lib/scope/nothing_to_observe.py")
    payload = _payload(proc)
    row = payload["candidates"][0]
    # C-18 types `applicable` as a JSON boolean and `_normalise_rows` writes a never-judged row
    # as `false` on purpose — what keeps it from BEING an exemption is the state beside it. So
    # the class is read from `decided_by`/`observed`, which are what say "nobody judged this".
    assert row["decided_by"] == "unevaluated", (
        "C-3: a file with no instrumentable position was never judged; got "
        f"decided_by={row['decided_by']!r} basis={row['basis']!r}"
    )
    assert row["observed"] == "unevaluated:no-instrumentable-position", (
        f"C-3/C-12: the row says it was never measured; got {row.get('observed')!r}"
    )
    assert row["probe"] == "not-run", (
        f"C-12: no probe observation accompanies an unmeasured class; got {row['probe']!r}"
    )
    exempted = {entry["path"] for entry in payload["exemptions"]}
    assert row["path"] not in exempted, (
        f"C-12: an unmeasured file MUST NOT be filed as exempt; exemptions={sorted(exempted)}"
    )
    violations = {entry["path"]: entry for entry in payload["violation_rows"]}
    assert row["path"] in violations, (
        "C-12: the unmeasured candidate is a VIOLATION naming its missing limb; got "
        f"{sorted(violations)}"
    )
    assert violations[row["path"]]["missing"], (
        "C-12: the violation names the limb it is missing, never an empty list"
    )
    assert proc.returncode == 1, (
        f"C-12/C-13: an unmeasured candidate is red; got exit {proc.returncode}"
    )
    assert payload["applicable"] + payload["exempt"] + payload["violations"] == len(
        payload["candidates"]), (
        "C-12: every candidate lands in exactly one bucket — compliant, exempt or a violation; "
        f"got applicable={payload['applicable']} exempt={payload['exempt']} "
        f"violations={payload['violations']} candidates={len(payload['candidates'])}"
    )


def test_c30_an_empty_register_is_legal_and_claims_nothing(tmp_path):
    """C-30 / T069: the literal `none` table is legal — no finding, no exemption, exit 0."""
    # The healthy part of the tree is explicit and `--files`-scoped: the scenario's own
    # `scripts/tool.sh` and `lib/helper.py` are fixtures of OTHER clauses (C-1's roster, the
    # mirror pairs) and this leg is about the REGISTER, not about re-measuring them.
    tree = _probe_tree(tmp_path, {"scripts/good.sh": None})
    page = tree / REGISTER_PAGE
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(REGISTER_SECTION.format(body="", rows=EMPTY_REGISTER_ROWS),
                    encoding="utf-8")
    _commit(tree, "scenario: an empty register")
    # The EMIT-RULE mode is the one every reader consults the register through, and it settles
    # nothing about a candidate — so it isolates the register from the scenario's flag surfaces
    # (which other clauses own) without weakening what this leg measures.
    proc = _run_checker(tree, "--emit-rule")
    payload = _payload(proc)
    assert payload["exceptions"] == [], (
        f"C-30: the `none` placeholder is not a row; got {payload['exceptions']}"
    )
    assert "exception-unverifiable" not in _finding_kinds(payload), (
        f"C-30: an empty register claims nothing and is legal; findings: {_finding_kinds(payload)}"
    )
    assert proc.returncode == 0, (
        f"C-30: an empty register is green; got exit {proc.returncode}\n"
        f"{proc.stdout[-1200:]}"
    )


def test_c30_a_forged_row_fails_the_path_limb(tmp_path):
    """C-30 / V-14 / T069: a row whose path does not exist is `exception-unverifiable`, exit 1."""
    tree = _register_tree(
        tmp_path,
        "| skills/external/vendor/scripts/absent.sh | vendor | C-7 | 保留在入口层 |",
    )
    _external_skill(tree, "vendor")
    _commit(tree, "scenario: a forged register row")
    proc = _run_checker(tree, "--json")
    payload = _payload(proc)
    row = _exceptions(payload)["skills/external/vendor/scripts/absent.sh"]
    assert row["recomputed"] is False, "C-30: a row naming an absent path does not recompute"
    assert "path-exists" in row["failed_limbs"], (
        f"C-30: the failing limb is named `path-exists`; got {row['failed_limbs']}"
    )
    kinds = _finding_kinds(payload)
    assert "exception-unverifiable" in kinds, (
        f"C-30: a forged row is a finding under its own name; findings: {kinds}"
    )
    named = [p for f in payload["findings"] if f.get("kind") == "exception-unverifiable"
             for p in f.get("paths", [])]
    assert "skills/external/vendor/scripts/absent.sh" in named, (
        f"C-30: the finding MUST name the row it is about; named: {named}"
    )
    assert proc.returncode == 1, (
        f"C-30/V-14: an unverifiable row is red; got exit {proc.returncode}"
    )


def test_c30_a_row_whose_skill_is_not_external_fails_the_classification_limb(tmp_path):
    """C-30 / T069: the skill's own `SKILL.md` must say `classification: external`."""
    tree = _register_tree(
        tmp_path,
        "| skills/external/partner/scripts/verbatim.sh | partner | C-7 | 保留在入口层 |",
    )
    _external_skill(tree, "partner", classification="internal")
    _commit(tree, "scenario: an internal skill registered as external")
    proc = _run_checker(tree, "--json")
    payload = _payload(proc)
    row = _exceptions(payload)["skills/external/partner/scripts/verbatim.sh"]
    assert row["recomputed"] is False, (
        "C-30: the machine mark is the only credential — an `internal` skill does not qualify"
    )
    assert "skill-declares-external" in row["failed_limbs"], (
        f"C-30: the failing limb is named; got {row['failed_limbs']}"
    )
    assert "exception-unverifiable" in _finding_kinds(payload), (
        f"C-30: the row is red under its own name; findings: {_finding_kinds(payload)}"
    )
    assert proc.returncode == 1, (
        f"C-30: an unverifiable row is exit 1; got {proc.returncode}"
    )


def test_c30_a_row_outside_the_external_root_fails_its_placement_limb(tmp_path):
    """C-30 / T069: a real file outside `skills/external/<skill>/` does not recompute."""
    tree = _register_tree(
        tmp_path,
        "| scripts/tool.sh | vendor | C-7 | 保留在入口层 |",
    )
    _commit(tree, "scenario: a register row for an in-tree script")
    payload = _payload(_run_checker(tree, "--json"))
    row = _exceptions(payload)["scripts/tool.sh"]
    assert row["recomputed"] is False and "under-external-skill" in row["failed_limbs"], (
        "C-30: the path exists but sits outside the third-party root, so its placement limb "
        f"fails; got recomputed={row['recomputed']} failed={row['failed_limbs']}"
    )


def test_c30_a_row_missing_a_column_fails_the_four_columns_limb(tmp_path):
    """C-30 / T069: all four columns MUST be present, or the row does not recompute."""
    tree = _register_tree(
        tmp_path,
        "| skills/external/vendor/scripts/verbatim.sh | vendor | C-7 |",
    )
    _external_skill(tree, "vendor")
    _commit(tree, "scenario: a three-column register row")
    payload = _payload(_run_checker(tree, "--json"))
    row = _exceptions(payload)["skills/external/vendor/scripts/verbatim.sh"]
    assert row["recomputed"] is False and "four-columns-present" in row["failed_limbs"], (
        "C-30: an empty `handling` cell fails the four-columns limb; got "
        f"recomputed={row['recomputed']} failed={row['failed_limbs']}"
    )


def test_c30_a_verified_row_exempts_and_is_not_counted_against_the_flag_surface(tmp_path):
    """C-30 / V-14 / T069: a row that recomputes is a `declared-exception` exemption."""
    tree = _register_tree(
        tmp_path,
        "| skills/external/vendor/scripts/verbatim.sh | vendor | C-7 | 保留在入口层 |",
    )
    _external_skill(tree, "vendor")
    _commit(tree, "scenario: a verified register row")
    proc = _run_checker(tree, "--json")
    payload = _payload(proc)
    row = _exceptions(payload)["skills/external/vendor/scripts/verbatim.sh"]
    assert row["recomputed"] is True, (
        "C-30: all four limbs hold, so the row recomputes; got "
        f"failed={row['failed_limbs']}"
    )
    assert row["failed_limbs"] == [], f"C-30: nothing failed; got {row['failed_limbs']}"
    assert row["skill"] == "vendor" and row["unsatisfied_clause"] == "C-7" and row["handling"], (
        "C-30: the row carries the page's four columns back out; got "
        f"skill={row['skill']!r} unsatisfied_clause={row['unsatisfied_clause']!r} "
        f"handling={row['handling']!r}"
    )
    exemptions = {entry["path"]: entry for entry in payload["exemptions"]}
    candidate = "skills/external/vendor/scripts/verbatim.sh"
    assert candidate in exemptions, (
        f"C-30: a verified row is filed where a reader looks for a declared exemption; "
        f"got {sorted(exemptions)}"
    )
    assert exemptions[candidate]["basis"] == "declared-exception", (
        f"C-30/E-2: the basis is the closed set's own sentence; got "
        f"{exemptions[candidate]['basis']!r}"
    )
    assert "exception-unverifiable" not in _finding_kinds(payload), (
        f"C-30: a verified row raises nothing; findings: {_finding_kinds(payload)}"
    )
    assert all(entry["path"] != candidate for entry in payload["violation_rows"]), (
        "C-30: the reduced obligation is honoured — the script is not red for a flag surface "
        "it was never going to owe"
    )


def test_c30_an_unregistered_third_party_script_is_an_ordinary_candidate(tmp_path):
    """C-30 / V-15 / T069: registration is the ONLY credential — nobody is auto-exempted.

    Two legs, because the 2026-11-08 ruling gives a candidate three states and the register only
    ever decides two of them:

    * a third-party file that ACTS and declares the option it writes through is REQUIRED, so its
      missing limbs are a violation naming the path — no directory excuses it;
    * a third-party file that is read-only is filed OPTIONAL under the basis its own row carries,
      never as a DECLARED exemption — registration remains the only route to that.
    """
    candidate = "skills/external/vendor/scripts/verbatim.sh"
    tree = _register_tree(tmp_path, EMPTY_REGISTER_ROWS)
    _external_skill(tree, "vendor", body=_verbatim_required("vendor/scripts/verbatim.sh"))
    _commit(tree, "scenario: an unregistered third-party script that acts")
    payload = _payload(_run_checker(tree, "--json", "--files", candidate))
    rows = {row["path"]: row for row in payload["candidates"]}
    assert candidate in rows, (
        "V-15: a third-party script is still a candidate; got "
        f"{sorted(p for p in rows if 'external' in p)}"
    )
    exemptions = {entry["path"]: entry for entry in payload["exemptions"]}
    declared = {path for path, entry in exemptions.items()
                if entry.get("basis") == "declared-exception"}
    assert candidate not in declared, (
        "V-15: sitting under `skills/external/` is NOT a declared exemption; the register is. "
        f"got declared exemptions={sorted(declared)}"
    )
    violations = {v["path"]: v for v in payload["violation_rows"]}
    assert rows[candidate]["applicable"] is True, (
        "V-15: a third-party script that acts is REQUIRED by its own run; got "
        f"applicable={rows[candidate]['applicable']} basis={rows[candidate]['basis']!r}"
    )
    assert candidate in violations, (
        "V-15: a REQUIRED third-party script's missing limbs are violations naming it — the "
        f"register is the only credential, never the directory; got rows={sorted(violations)} "
        f"exemptions={sorted(exemptions)}"
    )
    assert rows[candidate]["decided_by"] in ("run-semantics", "inherited-from-source"), (
        "V-15: the unregistered file is judged like any other — by a run; got "
        f"{rows[candidate]['decided_by']!r}"
    )

    # The read-only leg: the same address, a file with nothing to declare and nothing observed
    # written. The ruling files it OPTIONAL — printed on its row and in `exemptions[]` under the
    # same basis — and still never as a declared exemption.
    read_only = _register_tree(tmp_path / "read-only", EMPTY_REGISTER_ROWS)
    _external_skill(read_only, "vendor")
    _commit(read_only, "scenario: an unregistered read-only third-party script")
    ro_payload = _payload(_run_checker(read_only, "--json", "--files", candidate))
    ro_row = {row["path"]: row for row in ro_payload["candidates"]}[candidate]
    ro_exemptions = {entry["path"]: entry for entry in ro_payload["exemptions"]}
    assert ro_row["basis"], (
        "V-15: an optional candidate carries the basis that decided it; got none"
    )
    assert ro_exemptions.get(candidate, {}).get("basis") == "optional-read-only", (
        "V-15: a read-only third-party script is filed OPTIONAL — the ruling's own basis, "
        "printed rather than dropped, and still not a declared exemption; got "
        f"exemption={ro_exemptions.get(candidate)} row basis={ro_row['basis']!r}"
    )


def test_c30_the_recomputation_limbs_are_published_by_the_rule(tmp_path):
    """C-30 / C-21: the four limbs `--emit-rule` publishes are the four the engine executes."""
    engine = _engine_module()
    emitted = json.loads(_run_engine("--emit-rule", "--root", str(ROOT)).stdout)
    assert list(emitted["rule"]["exception_limbs"]) == list(engine.EXCEPTION_LIMBS), (
        "C-30/C-21: the emitted limbs are the executed limbs; got "
        f"{emitted['rule']['exception_limbs']} vs {list(engine.EXCEPTION_LIMBS)}"
    )
    assert list(engine.EXCEPTION_LIMBS) == [
        "path-exists", "under-external-skill", "skill-declares-external",
        "four-columns-present",
    ], f"C-30: the four limbs, in the page's own order; got {engine.EXCEPTION_LIMBS}"
    assert {"declared-exception"} <= set(engine.EXEMPT_BASIS), (
        "C-30/E-2: `declared-exception` is in the closed basis set"
    )


# ======================================================================================
# T073 / T074 / T076 / T077 — the insertion rule, the shared snapshot pair, the sentinel
# and the live rejection face
# ======================================================================================

#: The bash half of the rule: the library every applicable `.sh` sources. T076 publishes
#: `script_interface_version_text` from it, and the guard projection inlines that body.
GUARD_LIBRARY = ROOT / "scripts" / "bash" / "script-interface.sh"

#: The one call a consumer makes to declare its surface, and the one it makes to answer.
_DEFINE_RE = re.compile(r"^\s*script_interface_guard\s+define\b", re.M)
_GUARD_RE = re.compile(r"^\s*script_interface_guard\s+guard\b", re.M)


def _consumers_of_the_guard() -> list:
    """Every tracked `.sh` that sources the guard library, as repo-relative paths.

    Read from git's own enumeration rather than a hand-written list, so a consumer added
    tomorrow is judged by the same rule the day it lands.
    """
    import subprocess

    listing = subprocess.run(["git", "ls-files", "*.sh"], cwd=str(ROOT),
                             capture_output=True, text=True)
    assert listing.returncode == 0, f"git ls-files failed: {listing.stderr[-800:]}"
    found = []
    for rel in listing.stdout.split():
        path = ROOT / rel
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if "script-interface.sh" in text and _DEFINE_RE.search(text):
            found.append(rel)
    return found


#: The shell keywords an executable line may open with and still be part of the guard block:
#: `define` / `guard` themselves, `if [ -f "$.../script-interface.sh" ]` (the guarded source),
#: and the directory resolution the source line needs.
_BLOCK_OPENERS = ("SCRIPT_INTERFACE_LIB=", 'if [ -f "$SCRIPT_INTERFACE_LIB" ]',
                  'if [ -f "$SCRIPT_DIR/script-interface.sh" ]',
                  'SCRIPT_DIR="$(CDPATH=""', 'if [ -f "$SCRIPT_DIR/script-interface.sh" ]')
_LIBRARY_ENTRY_RE = re.compile(r"\$0\s*\]\s*\]\s*&&\s*\[|\"\$_SCRIPT_INTERFACE_READ_IN\" ")


def _first_executable_line(text: str) -> int:
    """The 0-based index of the first line that is neither shebang, comment nor blank."""
    for index, line in enumerate(text.splitlines()):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        return index
    return -1


def test_t073_the_guard_block_is_the_first_executable_block_of_every_consumer():
    """T073: no consumer runs anything before the block that answers `--help` (C-7/C-9/C-11).

    The rule the owner page states (§4.1) is asserted mechanically on the live source tree:
    the block's three calls come in the order source → define → guard, the library is sourced
    from within the block rather than anywhere earlier, and no `mkdir` / `git` write sits above
    it.
    """
    consumers = _consumers_of_the_guard()
    assert consumers, (
        "T073: no consumer of the guard library was found — this assertion would be vacuous"
    )
    problems = []
    for rel in consumers:
        text = (ROOT / rel).read_text(encoding="utf-8")
        first = _first_executable_line(text)
        if first < 0:
            problems.append(f"{rel}: no executable line at all")
            continue
        define_at = _DEFINE_RE.search(text)
        guard_at = _GUARD_RE.search(text)
        source_at = re.search(r"^\s*(?:\.|source)\s+\"?\$\{?SCRIPT_INTERFACE_LIB", text, re.M)
        if source_at is None:
            # A library that is its own consumer has no `SCRIPT_INTERFACE_LIB` indirection: its
            # block is the self-application at the file's end, and the `define`/`guard` pair is
            # all there is to judge. That is the one shape the trio cannot decide.
            if define_at is None or guard_at is None:
                problems.append(
                    f"{rel}: neither a library source line nor a define/guard pair was found")
            continue
        if define_at is None or guard_at is None:
            problems.append(f"{rel}: the block's source / define / guard trio is incomplete")
            continue
        if not (source_at.start() < define_at.start() < guard_at.start()):
            problems.append(
                f"{rel}: the order MUST be source, then define, then guard; offsets were "
                f"{source_at.start()} / {define_at.start()} / {guard_at.start()}")
        source_line = text[:source_at.start()].count("\n")
        if first > source_line:
            problems.append(
                f"{rel}: line {first + 1} runs before the library is sourced on line "
                f"{source_line + 1}")
        above = "\n".join(text.splitlines()[:first])
        for forbidden in ("mkdir", "git add", "git commit", "git checkout"):
            if re.search(rf"^\s*{re.escape(forbidden)}\b", above, re.M):
                problems.append(f"{rel}: `{forbidden}` sits above the guard block")
    assert not problems, "T073: the insertion rule is violated:\n  " + "\n  ".join(problems)


def test_t073_the_owner_page_states_the_insertion_rule():
    """T073: the rule is recorded where the rule lives — the owner page, not a test comment."""
    page = _text(OWNER)
    section = re.search(r"^### 4\.1.*?(?=^#{2,3} |\Z)", page, re.M | re.S)
    assert section, "T073: the owner page carries the insertion rule as `### 4.1 …`"
    body = section.group(0)
    for limb in ("source", "mkdir", "git", "manifest"):
        assert limb in body, (
            f"T073: the insertion rule names `{limb}` as something the block precedes; "
            f"section body does not:\n{body}")
    assert "第一个可执行块" in body, (
        "T073: the rule's operative phrase (the block is the FIRST executable block) is stated")


def _tree_snapshot(root: Path) -> tuple:
    """The ONE snapshot pair the zero-side-effect assertion runs on (T074).

    Three limbs, exactly as C-10 fixes them: `git status --porcelain`, the `sha256` of every
    `*.sh` / `*.py` in the measured tree, and the file list plus hashes under `.specify/`.
    Returned as ONE value so a caller compares a pair, never three comparisons of which one
    could silently be dropped.
    """
    import hashlib
    import subprocess

    # The `.git/` directory is skipped on purpose: version-control bookkeeping is not a
    # script's side effect, and the measured tree carries its own. Recording it would make
    # the manifest limb move on anything the repository does for its own reasons — including
    # a populated index, which `git status` itself creates as its own cache — and a limb that
    # moves on its own is a limb that cannot report a write. `.specify/` has no other reason
    # to change between two snapshots taken around a flag run, so this limb takes EVERY file
    # under it — the suffix filter below belongs to the script limb, which passes one.
    def files(directory: Path, suffix: tuple = ()) -> dict:
        found = {}
        for path in sorted(directory.rglob("*")):
            relative = path.relative_to(directory)
            if (suffix and path.suffix not in suffix) or ".git" in relative.parts \
                    or not path.is_file() or path.is_symlink():
                continue
            found[relative.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
        return found

    status = subprocess.run(["git", "status", "--porcelain"], cwd=str(root),
                            capture_output=True, text=True)
    return (status.stdout.splitlines(), files(root, (".sh", ".py")),
            files(root / ".specify") if (root / ".specify").is_dir() else {})


def _run_in_tree(tree: Path, script: str, *args: str, timeout: int = 120):
    """Run one script inside a tree — the LIVE face, not the checker's probe."""
    import subprocess

    return subprocess.run(["bash", script, *args], cwd=str(tree), capture_output=True,
                          text=True, timeout=timeout)


def test_t074_the_snapshot_pair_is_one_value_and_it_notices_a_write(tmp_path):
    """T074: the pair is shared, and it is not vacuous — a real write moves each limb."""
    import shutil

    tree = _probe_tree(tmp_path, {"scripts/reader.sh": None})
    # The REAL library, so the block under test is the one that ships.
    shutil.copy(GUARD_LIBRARY, tree / "scripts" / "script-interface.sh")
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: a reader on the real guard")

    before = _tree_snapshot(tree)
    (tree / "scripts" / "reader.sh").write_text("#!/usr/bin/env bash\n", encoding="utf-8")
    assert _tree_snapshot(tree)[1] != before[1], (
        "T074: the script digest limb MUST notice a modified *.sh")
    (tree / "stray.txt").write_text("x", encoding="utf-8")
    assert _tree_snapshot(tree)[0] != before[0], (
        "T074: the `git status` limb MUST notice a new untracked file")
    (tree / ".specify").mkdir()
    (tree / ".specify" / "touched.md").write_text("x", encoding="utf-8")
    assert _tree_snapshot(tree)[2] != before[2], (
        "T074: the `.specify/` manifest limb MUST notice a new file")
    (tree / "stray.txt").unlink()
    shutil.rmtree(tree / ".specify")
    _git(tree, "checkout", "--", "scripts/reader.sh")
    assert _tree_snapshot(tree) == before, "T074: the control MUST restore the tree"
    for args in (("-h",), ("--help",), ("--version",), ("--no-such-flag",),
                 ("--help", "--out", "x"), ("--out", "x", "--help")):
        proc = _run_in_tree(tree, "scripts/reader.sh", *args)
        assert proc.returncode in (0, 2), (
            f"T074: the flag runs are answered; {args} gave {proc.returncode}"
            f": {proc.stderr[-400:]}")
    assert _tree_snapshot(tree) == before, (
        "T074/C-10: the six flag runs leave the snapshot pair identical")


def test_t074_help_wins_is_read_from_the_same_snapshot_pair(tmp_path):
    """T074 / C-11: both argument orders answer help AND leave the same pair identical."""
    import shutil

    tree = _probe_tree(tmp_path, {"scripts/writer.sh": None})
    shutil.copy(GUARD_LIBRARY, tree / "scripts" / "script-interface.sh")
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: a writer on the real guard")
    before = _tree_snapshot(tree)
    for order in (("--help", "--out", "written.txt"), ("--out", "written.txt", "--help")):
        proc = _run_in_tree(tree, "scripts/writer.sh", *order)
        assert proc.returncode == 0, (
            f"T074/C-11: `{' '.join(order)}` answers the flag and exits 0; got "
            f"{proc.returncode}: {proc.stderr[-600:]}")
        assert "usage:" in proc.stdout, (
            f"T074/C-11: the help body is what answers, got {proc.stdout[:200]!r}")
        assert not (tree / "written.txt").exists(), (
            f"T074/C-11: the help path MUST beat the write in `{' '.join(order)}`")
    assert _tree_snapshot(tree) == before, (
        "T074/C-11: the help-wins comparison is read off the same pair, and it is identical")


def test_t076_the_version_text_function_is_published_and_defaults_its_own_constants():
    """T076: `script_interface_version_text` exists, answers one line, is self-contained."""
    import subprocess

    text = _text(GUARD_LIBRARY)
    assert "script_interface_version_text() {" in text, (
        "T076: the library publishes `script_interface_version_text`")
    emitted = subprocess.run(
        ["bash", "-c", '. "%s"; script_interface_version_text probe.sh "%s"'
         % (GUARD_LIBRARY, ROOT)],
        cwd=str(ROOT), capture_output=True, text=True, timeout=120)
    assert emitted.returncode == 0, f"T076: it exits 0; got {emitted.stderr[-600:]}"
    version = re.search(r'^version\s*=\s*"([^"]+)"', _text(ROOT / "pyproject.toml"), re.M)
    assert version, "T076: the framework's own version source is readable"
    assert emitted.stdout.strip() == "probe.sh %s" % version.group(1), (
        "T076/C-8: one line, read at run time from pyproject.toml; got "
        f"{emitted.stdout.strip()!r}")
    body = text.split("script_interface_version_text() {", 1)[1].split("\n}", 1)[0]
    for default in ("pyproject.toml", "12"):
        assert default in body, (
            f"T076: the body defaults its own constant ({default}) so the spliced copy works "
            f"without the library's file scope; body:\n{body}")


def test_t076_the_projection_inlines_the_body_through_the_sentinel(tmp_path):
    """T076: the emitted guard carries the library's OWN body, not a second copy of the search."""
    import subprocess

    engine = _sync_module()
    body = engine.version_text_function_body(_text(GUARD_LIBRARY))
    assert body.strip(), "T076: the library's function body is readable by the engine"
    source = _text(ROOT / "scripts" / "bash" / "run-tests.sh")
    projected, applied = engine.project_source(source, "bash-version-guard")
    assert applied is True, f"T076: the pair projects; reason: {projected}"
    assert "script_interface_version_text() {" in projected, (
        "T076: the emitted guard DEFINES the function, so a copy without the library answers")
    assert engine.PROJECTION_SENTINEL not in projected, (
        "T076: no unresolved sentinel reaches a mirror")
    assert body.strip() in projected, (
        "T076: the body in the guard is the library's own — a second spelling of the search "
        "is exactly the drift the sentinel exists to prevent")
    downstream = tmp_path / "downstream"
    (downstream / "scripts").mkdir(parents=True)
    (downstream / ".git").mkdir()
    (downstream / "pyproject.toml").write_text(
        '[project]\nname = "downstream"\nversion = "9.9.9"\n', encoding="utf-8")
    copy = downstream / "scripts" / "guard-only.sh"
    copy.write_text(projected, encoding="utf-8")
    answered = subprocess.run(["bash", "scripts/guard-only.sh", "--version"],
                              cwd=str(downstream), capture_output=True, text=True, timeout=120)
    assert answered.returncode == 0, (
        f"T076/C-36: the guard answers without the library; got {answered.returncode}: "
        f"{answered.stderr[-600:]}")
    assert answered.stdout.strip() == "guard-only.sh 9.9.9", (
        "T076: the inlined body derives the version from the tree it sits in; got "
        f"{answered.stdout.strip()!r}")
    helped = subprocess.run(["bash", "scripts/guard-only.sh", "--help"],
                            cwd=str(downstream), capture_output=True, text=True, timeout=120)
    assert helped.returncode == 0, "T076: `--help` is answered by the block itself at exit 0"
    for label in ("usage:", "options:", "side-effects:", "exit-codes:"):
        assert label in helped.stdout, (
            f"T076/C-7: the library-free help body carries the `{label}` label")


def _consumer_source(relative: str) -> str:
    """One consumer's SOURCE text (never a mirror), read by git's own path."""
    return _text(ROOT / relative)


def _projected_bash_mirror(source_text: str) -> str:
    """The declared `bash-version-guard` projection of one consumer source (C-34/C-36)."""
    engine = _sync_module()
    projected, applied = engine.project_source(source_text, "bash-version-guard")
    assert applied is True, f"T078/C-34: the pair projects; reason: {projected}"
    return projected


# ======================================================================================
# T078 / T079 / T082 / T084 — the wiring discipline, the mutation leg, the owner-page
# agreement and the positional-flag guard
# ======================================================================================

#: C-32's clause heading, read here (not retyped below) so a renumbered clause is a loud red.
C32_HEADING = "## C-32 — No new command, gate step, or engine for the landing"

#: The revision C-32's landings start from: the merge base of the 086 line and `master`
#: (`git merge-base HEAD master`). It is a Git fact, computed rather than typed, so the
#: comparison stays reproducible on any clone — a pinned hash would rot, and a hand-typed file
#: list would be the very inventory the clause forbids. The readings below use
#: `git diff <rev>...HEAD`, i.e. ADDED paths only.
FEATURE_BASE_REV = "origin/master"


def _feature_base() -> str:
    """The merge base of `HEAD` and the upstream branch, as a spelling git accepts."""
    import subprocess

    for candidate in (FEATURE_BASE_REV, "master"):
        proc = subprocess.run(["git", "merge-base", "HEAD", candidate], cwd=str(ROOT),
                              capture_output=True, text=True, timeout=120)
        if proc.returncode == 0 and proc.stdout.strip():
            return proc.stdout.strip()
    raise AssertionError(
        "C-32: the feature's own base is `git merge-base HEAD <upstream>`; neither the upstream "
        "branch nor `master` resolved in this clone"
    )

#: The clause that owns C-32 and the three surfaces C-32 refuses to grow.
FEATURE_DIR = ROOT / ".specify" / "specs" / "089-script-interface-contract"
GOVERNANCE_CONTRACT = FEATURE_DIR / "contracts" / "governance-landing.contract.md"
COMMAND_SURFACE = "templates/commands"
#: A driver stage gate lands in the driver's verdict engine; a confirmation gate lands in the
#: guidelines page the scanner enforces and in the mechanical gate file `gate-check.py` reads.
DRIVER_GATE_ENGINES = ("scripts/python/gate-check.py",)
CONFIRMATION_GATE_SURFACES = (
    ".specify/shared/guidelines/confirmation-gates.md",
    ".specify/gate.yaml",
)

#: The engine's two entry faces: the module the bridge imports and the script that is called.
#: C-32 allows exactly these two plus the bash library; a third would be the second checker.
IMPORT_PATH = "scripts/python/script_interface_cli.py"
CALL_PATH = "scripts/python/script-interface-check.py"

#: The roots C-32's measured set is read over: a second checker, a rival engine or a
#: test-only script would land here. `skills/` is outside by design — closing the rule across
#: the repository (US1 … US6) MODIFIES consumers in place there, it adds nothing.
C32_SCRIPT_ROOTS = ("scripts", ".specify/scripts", "tests", ".specify/tests")

#: What `git diff <base>...HEAD` measures as ADDED under those roots, beyond the clause's own
#: list. Read on 2026-11-08 (base `git merge-base HEAD master` = `24cb4edc`); every entry is a
#: row of this feature — T091's workspace guard and its unit test, the engine's shared-table
#: unit test, T093's separator regression and T094's help-body guard. A new entry here is a new
#: artifact, and it fails the guard until someone records it in the clause or deletes it.
C32_MEASURED_BEYOND_DECLARATION = (
    ".specify/scripts/python/workspace-guard.py",
    "scripts/python/workspace-guard.py",
    "tests/contract/test_help_body_preservation.py",
    "tests/contract/test_reanchoring_contract.py",
    "tests/contract/test_sdd_loop_driver_reanchor.py",
    "tests/unit/test_create_new_requirements_separator.py",
    "tests/unit/test_script_interface_cli.py",
    "tests/unit/test_workspace_guard.py",
)

#: Which declared artifacts actually HAVE a mirror, measured rather than assumed: the guard
#: checks every entry against the tree and then re-derives the set independently in
#: `test_t078_the_new_executable_artifacts_are_exactly_what_c32_names` (a declared entry with
#: no mirror would be a phantom, and a mirror of a declared entry absent here would be a gap).
MIRRORED_ARTIFACTS = (
    "scripts/python/script-interface-check.py",
    "scripts/python/script_interface_cli.py",
    "scripts/bash/script-interface.sh",
)


def _git_paths(*args: str) -> list[str]:
    """`git diff --name-only` under one revision range or pair of commits, sorted."""
    import subprocess

    proc = subprocess.run(["git", *args], cwd=str(ROOT), capture_output=True, text=True,
                          timeout=180)
    assert proc.returncode == 0, f"git {' '.join(args)} failed: {proc.stderr[-800:]}"
    return sorted(line.strip() for line in proc.stdout.splitlines() if line.strip())


def _c32_executables() -> set[str]:
    """C-32's "only new executable artifacts" list, READ OUT of the clause.

    The clause is the owner of the list; the guard derives it (an artifact is a backticked
    path ending in `.sh` / `.py`, plus ` (plus its mirror)` stays a note rather than a second
    path). A clause that stopped publishing the list leaves nothing to compare against and
    fails loudly instead of passing over an empty set.
    """
    text = _text(GOVERNANCE_CONTRACT)
    start = text.index(C32_HEADING)
    end = text.find("\n## ", start + 1)
    clause = text[start:end if end >= 0 else len(text)]
    named = re.findall(r"`((?:scripts|tests)/[^`]*\.(?:sh|py))`", clause)
    assert named, (
        "C-32: the clause publishes its closed list of new executable artifacts; a clause "
        "with no backticked path would make the comparison below vacuous"
    )
    return set(named)


def test_t078_the_contract_test_is_selected_by_the_contract_marker():
    """T078: C-32's first wiring limb — the new test rides `pytest -m contract`."""
    text = _text(Path(__file__))
    assert re.search(r"^pytestmark = pytest\.mark\.contract\s*$", text, re.M) or \
        re.search(r"^pytestmark = \[.*pytest\.mark\.contract.*\]$", text, re.M), (
        "C-32: the file declares `pytestmark = pytest.mark.contract`, so the existing "
        "selection runs it — no new gate step and no new suite was added"
    )
    assert IMPORT_PATH in text and CALL_PATH in text, (
        "C-32: the file exercises the engine through BOTH of its doors — the version bridge "
        f"({IMPORT_PATH}) and the call path ({CALL_PATH}) — and adds no third entry point"
    )
    # The second limb is measured by the runner under its own marker arguments, not by reading
    # this source: `test_t078_the_contract_marker_collects_this_file` performs that reading.


def _collect_only() -> int:
    """How many of this file's tests `pytest -m contract` collects (a subprocess reading)."""
    import subprocess
    import sys

    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-m", "contract", "-q", __file__],
        cwd=str(ROOT), capture_output=True, text=True, timeout=600,
    )
    match = re.search(r"^(\d+) tests? collected", proc.stdout, re.M)
    if not match:
        match = re.search(r"(\d+)/(\d+) tests collected", proc.stdout)
        assert match, (
            "T078: `--collect-only -m contract` reports a count; output was:\n"
            f"{proc.stdout[-1500:]}\n{proc.stderr[-800:]}"
        )
    return int(match.group(1))


def test_t078_the_contract_marker_collects_this_file():
    """T078: the marker limb as a READING — a non-zero collection under `-m contract`."""
    collected = _collect_only()
    assert collected > 0, (
        "C-32: `pytest --collect-only -m contract` collects this file; got 0, which is the "
        "exact 'wired into nothing' state the clause forbids"
    )


#: The shape of the 086 flag surface in a python candidate (C-34/C-36's projection target).
#: The engine that emits it owns the spelling; this pattern only has to FIND the region, and
#: the guard fails loudly when it finds none — a silent "nothing to remove" would compare a
#: script against itself and pass over a real gate.
FLAG_BLOCK_OPEN = "# --version, wired through the one version source"
FLAG_BLOCK_CLOSE = "def main() -> int:"


def _without_flag_block(text: str) -> str:
    """One python script with the 086 flag surface removed.

    What is removed is what closing the rule adds to every candidate: the flag comment run,
    the guard imports, the `_HELP` body and the guard call. What remains is the script's own
    logic — where a gate step would live — so the removal only has to be honest, not clever.
    The removal's ends are a marker line and the `main()` definition, both owned by the
    projection the engine emits; a source that carries neither is returned unchanged and the
    caller's comparison before/after then reports the difference itself.
    """
    if FLAG_BLOCK_OPEN not in text:
        return text
    head, tail = text.split(FLAG_BLOCK_OPEN, 1)
    close = tail.find(FLAG_BLOCK_CLOSE)
    if close < 0:
        return text
    rest = tail[close:]
    # The guard call and the help handler sit inside `main()`; drop them, keep everything else.
    kept_lines = []
    for line in rest.splitlines(keepends=True):
        stripped = line.strip()
        if stripped.startswith(
                ("_sig_guard(", "if any(a in (\"-h\", \"--help\") for a in",
                 "print(fill_help_labels(_HELP), end=\"\")", "return 0",
                 "# `declared` is this script's own vocabulary:", "# loop accepts, and stating")):
            continue
        kept_lines.append(line)
    return head + "".join(kept_lines)


def _added_paths(rev: str, *paths: str) -> set[str]:
    """The `A` rows of `git diff --name-status <rev>...HEAD`, optionally under `paths`."""
    import subprocess

    proc = subprocess.run(["git", "diff", "--name-status", f"{_feature_base()}...HEAD",
                           "--", *paths] if paths else
                          ["git", "diff", "--name-status", f"{_feature_base()}...HEAD"],
                          cwd=str(ROOT), capture_output=True, text=True, timeout=180)
    assert proc.returncode == 0, f"git diff failed: {proc.stderr[-800:]}"
    added = set()
    for line in proc.stdout.splitlines():
        fields = line.split("\t")
        if fields and fields[0].startswith("A"):
            added.update(fields[1:])
    return added


def test_t078_the_new_executable_artifacts_are_exactly_what_c32_names():
    """T078: C-32's second limb — "the only new executable artifacts".

    Measured from git's ADD rows, never from a hand-typed inventory: the declared set is read
    OUT of the clause and the measured set is what the feature created, so the comparison is a
    set equality on both sides.

    The revision pair is `git merge-base HEAD <upstream>` -> `HEAD` (`git diff A...B`), not
    base -> worktree: the worktree is dirty while a package runs, and a comparison that also
    caught the *creation* commits of the parent line would report every pre-existing script as
    "added". Computed, never pinned, so the reading is reproducible on any clone. The measured
    set is taken over the roots where a NEW checker or a test-only script would land.
    """
    base = _feature_base()
    declared = _c32_executables()
    # The clause names the three engine faces WITH their mirrors; the mirror is derived from
    # the same declared path, never typed beside it.
    declared_with_mirrors = set(declared)
    for path in list(declared):
        if path in MIRRORED_ARTIFACTS:
            declared_with_mirrors.add(".specify/" + path)
    measured = {path for path in _added_paths(base, *C32_SCRIPT_ROOTS)
                if path.endswith((".sh", ".py"))}
    # On the integrated trunk the feature's declared artifacts are already present IN the
    # base (the merge landed them), so nothing is "added" and the comparison is trivially
    # equal — not vacuous. The non-vacuity leg belongs to the feature branch, where the
    # declared artifacts are absent from the base and the diff is real.
    import subprocess

    tree = subprocess.run(["git", "ls-tree", "-r", "--name-only", base], cwd=str(ROOT),
                          capture_output=True, text=True, timeout=180)
    base_paths = set(tree.stdout.splitlines()) if tree.returncode == 0 else set()
    integrated = bool(declared_with_mirrors) and declared_with_mirrors <= base_paths
    if integrated:
        # The declared artifacts already live in the base: the diff has nothing to compare, so
        # this leg is not applicable on the integrated trunk. Skipped explicitly, never
        # presented as a pass; the existence and engine-dir legs below still run.
        import pytest

        pytest.skip("integrated trunk: the feature diff is inside the base; C-32's diff leg "
                    "is not applicable")
    else:
        assert measured, (
            "C-32: the feature ADDED executable artifacts, so the comparison below is not "
            f"vacuous; base={base[:12]}"
        )
        assert declared_with_mirrors <= measured, (
            "C-32: every declared artifact is one this feature ADDED; missing "
            f"{sorted(declared_with_mirrors - measured)}"
        )
        # The clause's list, stated as an equality so an unrecorded addition is a red rather
        # than a silent widening. The tree's extra additions are enumerated beside it, each
        # with the row that owns it.
        addition = sorted(measured - declared_with_mirrors)
        assert addition == sorted(C32_MEASURED_BEYOND_DECLARATION), (
            "C-32: the added executable artifacts outside the clause's list changed. The clause "
            "declares the engine artifacts; this feature's OTHER rows (T091, T093, T094 and "
            "their unit tests) landed beside them. Record the difference in the clause or "
            "remove the artifact — an unrecorded addition is the drift C-32 exists to stop.\n"
            f"  measured={addition}\n  recorded={sorted(C32_MEASURED_BEYOND_DECLARATION)}"
        )
    for path in declared_with_mirrors:
        assert (ROOT / path).is_file(), f"C-32: the declared artifact exists: {path}"
    # A fourth checker is a file, not an intention: the engine's own directory carries exactly
    # the checker and its shared table, and the count is read from the tree.
    engines = sorted(ENGINE.parent.glob("*interface*.py"))
    assert engines == sorted([ENGINE, ENGINE.with_name("script_interface_cli.py")]), (
        f"C-32: one checker and its shared table under `scripts/python/`; got "
        f"{[p.name for p in engines]}"
    )


def test_t078_no_command_gate_or_second_checker_was_added():
    """T078: C-32's three refusals, each asserted against the artifacts that would carry them.

    The three surfaces are structural, not textual, so each is asserted where it lands:
    a `/speckit.*` command is a file under the command roster, a driver stage gate is a
    `gate-check.py` registry row, and a confirmation gate is an entry in the gate scan's own
    governed list. A fourth checker is the engine count under `scripts/python/`.
    """
    import subprocess

    # 2026-11-11: the delta is read against this feature's base, so later features'
    # sanctioned command templates land inside it. `templates/commands/seal.md` is
    # Feature 099's `/speckit.seal` template; every other addition still goes red.
    sanctioned_later_commands = {"templates/commands/seal.md"}
    commands = sorted(set(
        _git_paths("diff", "--name-only", "--diff-filter=A", f"{_feature_base()}...HEAD", "--",
                   COMMAND_SURFACE)
    ))
    commands = [p for p in commands if p not in sanctioned_later_commands]
    assert not [p for p in commands if p.endswith(".md")], (
        f"C-32: no `/speckit.*` command was added; got {commands}"
    )
    # Driver stage gate: the verdict engine a new gate step would land in. Its SOURCE is
    # compared against the base revision — a projection may add the flag block every consumer
    # carries (C-34/C-36), which is a repair, not a gate; a gate step changes the engine's own
    # source, and that is what "no driver stage gate was added" measures.
    for engine in DRIVER_GATE_ENGINES:
        base = subprocess.run(["git", "show", f"{_feature_base()}:{engine}"],
                              cwd=str(ROOT), capture_output=True, text=True, timeout=120)
        assert base.returncode == 0, (
            f"C-32: the driver's gate engine existed at the feature base: {engine}"
        )
        source = _text(ROOT / engine)
        assert _without_flag_block(source) == _without_flag_block(base.stdout), (
            f"C-32: the driver stage gate set is unchanged by this feature ({engine}) — a "
            "stage-gate change lands in the engine's own code, not in the flag block every "
            "consumer now carries"
        )
    # Confirmation gate: the governed list the scanner enforces, and the mechanical gate file
    # `gate-check.py` reads. Both are compared the same way, so "unchanged" is a measurement.
    for surface in CONFIRMATION_GATE_SURFACES:
        base = subprocess.run(["git", "show", f"{_feature_base()}:{surface}"],
                              cwd=str(ROOT), capture_output=True, text=True, timeout=120)
        assert base.returncode == 0, (
            f"C-32: the confirmation-gate owner existed at the feature base: {surface}"
        )
        assert _text(ROOT / surface) == base.stdout, (
            f"C-32: the confirmation-gate list is unchanged by this feature ({surface})"
        )
    # Second checker: exactly one engine under `scripts/python/` judges the script-interface
    # rule, and its two faces are the declared pair — not an engine plus a rival.
    engines = sorted(ENGINE.parent.glob("script*interface*.py"))
    assert engines == sorted([ENGINE, ENGINE.with_name("script_interface_cli.py")]), (
        f"C-32: one checker and its shared table; got {[p.name for p in engines]}"
    )


def test_t079_a_deleted_help_arm_goes_red_and_names_the_script(tmp_path):
    """T079 / SC-008's mutation leg M-1: delete one compliant script's `--help` arm.

    The pair is the whole assertion. The MUTANT is the compliant scenario with its flag arm
    removed — the arm that answers `-h` / `--help` with the four-label body — and the CONTROL is
    an otherwise identical copy carrying it. A finding the pair misses is a false green: the
    mutant must be red, the control must be green, and the red must NAME the mutated path in
    the `violations` rows (the report's machine face) and on its own line in the human face.
    """
    version = "4.5.6"
    # The compliant fixture is the C-9-STRICT one, not `good_bash`: the latter answers an
    # undeclared token with the loop falling through, which is red for a reason that has nothing
    # to do with this mutation — a control that is already red would make the mutant's red say
    # nothing. `_strict_bash` is the shape the suite uses everywhere a script must be green.
    conforming = _strict_bash("keepme.sh", version)
    arm = "      -h|--help) usage; exit 0 ;;\n"
    assert conforming.count(arm) == 1, (
        "T079: the conforming fixture carries exactly one flag arm to delete"
    )
    mutant_text = conforming.replace(arm, "")
    assert mutant_text != conforming, "T079: the mutation really removes the arm"

    def scenario(name: str, body: str) -> Path:
        tree = tmp_path / name
        (tree / "scripts").mkdir(parents=True)
        (tree / "pyproject.toml").write_text(
            '[project]\nname = "scenario"\nversion = "%s"\n' % version, encoding="utf-8")
        script = tree / "scripts" / "keepme.sh"
        script.write_text(body, encoding="utf-8")
        script.chmod(0o755)
        _git(tree, "init", "-q")
        _git(tree, "config", "user.email", "scenario@example.invalid")
        _git(tree, "config", "user.name", "scenario")
        _git(tree, "add", "-A")
        _git(tree, "commit", "-q", "-m", "scenario: %s" % name)
        return tree

    control_tree = scenario("control", conforming)
    mutant_tree = scenario("mutant", mutant_text)

    control = _run_checker(control_tree, "--json", "--files", "scripts/keepme.sh",
                           "--budget-seconds", "120")
    mutant = _run_checker(mutant_tree, "--json", "--files", "scripts/keepme.sh",
                          "--budget-seconds", "120")
    control_payload = _payload(control)
    mutant_payload = _payload(mutant)

    # The control first: a red control would make the mutant's red meaningless.
    assert control.returncode == 0, (
        "T079/SC-008: the UNMUTATED copy is the control and it must be green; got exit "
        f"{control.returncode}\n{control.stdout[-1200:]}\n{control.stderr[-800:]}"
    )
    assert control_payload["violations"] == 0 and not _finding_kinds(control_payload), (
        f"C-7 control: nothing is red in the control; rows="
        f"{control_payload['violation_rows']} findings={_finding_kinds(control_payload)}"
    )
    # And the mutant: exit 1, the mutated path named, the missing limb named.
    assert mutant.returncode == 1, (
        "T079/SC-008: deleting a help arm makes the check EXIT 1 — a green here is the false "
        f"green C-7 exists to prevent; got exit {mutant.returncode}\n"
        f"{mutant.stdout[-1500:]}"
    )
    rows = {row["path"]: row for row in mutant_payload["violation_rows"]}
    assert set(rows) == {"scripts/keepme.sh"}, (
        "T079: the violation names the mutated script and only it; got "
        f"{sorted(rows)}"
    )
    assert rows["scripts/keepme.sh"]["missing"], (
        "T079: the violation names the missing limb; got "
        f"{rows['scripts/keepme.sh']['missing']}"
    )
    assert any(limb == "help" for limb in rows["scripts/keepme.sh"]["missing"]), (
        "T079/C-7: the missing limb is the flag surface itself; got "
        f"{rows['scripts/keepme.sh']['missing']}"
    )
    human = _run_checker(mutant_tree, "--files", "scripts/keepme.sh",
                         "--budget-seconds", "120")
    named = [line for line in human.stdout.splitlines()
             if "scripts/keepme.sh" in line and "help" in line]
    assert human.returncode == 1 and named, (
        "T079/C-19: the human face prints the violation on its own line, naming the script "
        f"and the missing limb; stdout was:\n{human.stdout[-1500:]}"
    )


#: The subcommand-shaped fixture's own names (T084). The shape is `goal-utils.py`'s: one
#: required subcommand, plus an option both the top parser and the subparser declare.
POSITIONAL_FIXTURE_NAME = "shaped.py"
POSITIONAL_OPTION = "--json"


def _run_in_python(tree: Path, script: str, *args: str, timeout: int = 120):
    """Run one python script inside a tree — the LIVE face, as a script, not as a module."""
    import subprocess
    import sys

    return subprocess.run([sys.executable, str(tree / script), *args], cwd=str(tree),
                          capture_output=True, text=True, timeout=timeout)


def _write_shaped(tree: Path, *, echo_top: bool) -> str:
    """The fixture source. `echo_top` decides whether a TOP-level `--json` reaches the action.

    Both shapes are compliant on the query that matters: a token AFTER the subcommand is
    honoured (`not-ignored`), and a token BEFORE it is either honoured too (`position-honoured`)
    or refused (`position-rejected`). What C-9 forbids — and what `goal-utils.py` does — is the
    third answer: exit 0, run the subcommand, and drop the option on the floor.
    """
    script = (
        "#!/usr/bin/env python3\n"
        '"""A scenario script with one required subcommand and a shared option."""\n'
        "import argparse\n"
        "import sys\n"
        "import pathlib\n"
        "sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))\n"
        "from script_interface_cli import guard_argv, configure_parser, fill_help_labels\n"
        "\n"
        "_HELP = (\"usage: shaped.py [--json] list\\n\"\n"
        "         \"options:\\n\"\n"
        "         \"  --json   machine-readable output\\n\"\n"
        "         \"  list     enumerate\\n\"\n"
        "         \"side-effects: none; the flags write nothing\\n\"\n"
        "         \"exit-codes: 0 success; 2 an unrecognized option\")\n"
        "\n"
        "\n"
        "def main(argv):\n"
        "    guard_argv(argv, declared=[\"--json\", \"list\"])\n"
        "    if any(a in (\"-h\", \"--help\") for a in argv):\n"
        "        print(fill_help_labels(_HELP), end=\"\")\n"
        "        return 0\n"
        "    common = argparse.ArgumentParser(add_help=False)\n"
        "    common.add_argument(\"--json\", action=\"store_true\")\n"
        "    parser = argparse.ArgumentParser(parents=[common])\n"
        "    configure_parser(parser)\n"
        "    sub = parser.add_subparsers(dest=\"action\", required=True)\n"
        "    p_list = sub.add_parser(\"list\", parents=[common], help=\"enumerate\")\n"
        "    args = parser.parse_args(argv)\n"
        "    top = struct_json(argv) if " + ("True" if echo_top else "False") + " else False\n"
        "    print(\"json\" if (args.json or top) else \"human\")\n"
        "    return 0\n"
        "\n"
        "\n"
        "def struct_json(argv):\n"
        "    return \"--json\" in argv[:argv.index(\"list\")]\n"
        "\n"
        "\n"
        "if __name__ == \"__main__\":\n"
        "    sys.exit(main(sys.argv[1:]))\n"
    )
    path = tree / "scripts" / POSITIONAL_FIXTURE_NAME
    path.write_text(script, encoding="utf-8")
    path.chmod(0o755)
    return script


def test_t082_the_owner_page_and_emit_rule_agree_in_both_directions():
    """T082 / C-21: the label set, asked in both directions with the SAME reader per direction.

    The pair is the four help-content labels: the page publishes them in one paragraph (the
    paragraph `_owner_label_line` reads, the same surface C-29's guard reads) and `--emit-rule`
    publishes them under `labels`. Reading both in code form — a backticked token on the page,
    a `labels` key in the rule — makes the two directions use one reader apiece:

    * page -> rule: every codified label on the page has a `labels` key;
    * rule -> page: every `labels` key appears, codified, on the page.

    Then the class-vocabulary question is asked in its own form. The page writes its
    classification outcomes as PROSE ("带一个已声明的选项运行…", "判为第三方/上游脚本"), so the
    comparison is made on the page's own nouns, read inline: a `.py` file for the language, and
    the two outcomes the page's step 4 fixes. The emitted bases are read from `--emit-rule` and
    from the engine's own closed set, and every base that has a producer is a codified token on
    the page. What the engine emits may not be worded outside the page's vocabulary; what the
    page declares may not be missing a producer.
    """
    page = _text(OWNER)
    rule = _payload(_run_engine("--json", "--emit-rule"))["rule"]
    module = _engine_module()

    # --- the label set, both directions ------------------------------------------------
    page_labels = {
        name for name in re.findall(r"`([a-z][a-z-]*)`", _owner_label_line())
        if name != "labels"
    }
    emitted_labels = set(rule["labels"])
    assert page_labels, (
        "C-21: the page's label paragraph yields tokens; a page that stopped publishing them "
        "would make this comparison vacuous"
    )
    assert page_labels - emitted_labels == set(), (
        "C-21 (page -> rule): the page's label set is missing from `--emit-rule`: "
        f"{sorted(page_labels - emitted_labels)}"
    )
    assert emitted_labels - page_labels == set(), (
        "C-21 (rule -> page): `--emit-rule` publishes labels the page does not declare: "
        f"{sorted(emitted_labels - page_labels)}"
    )
    assert set(rule["labels"]) == set(module.LABELS) == set(_checker_label_keys()), (
        "C-21: one label set, held by the emitted rule, the engine and the probe that judges "
        "it — three readings, one value"
    )

    # --- the class vocabulary, in the page's own nouns ---------------------------------
    # The page states its outcomes as prose, so the pair is read in prose on BOTH sides:
    # the page's two decided outcomes (its step 4 fixes exactly two: 适用 / 豁免) against the
    # report states that mean them — `applicable` is a candidate row's true class, `exempt`
    # is the report's own counter. The engine's per-class BASES are finer than the page's
    # vocabulary by design (`--emit-rule` carries the bases a run can emit, and the page never
    # enumerates them), so comparing bases to the page would be comparing two vocabularies at
    # different resolutions — which is what makes the label set, not the bases, the pair C-21
    # can ask both ways.
    section = _subsection(page, CLASSIFICATION_STEPS_HEADING)
    outcomes = re.findall(r"即判(\S{2})", section)
    assert outcomes == ["适用", "豁免"], (
        "C-21: the page's step 4 fixes exactly the two decided outcomes; got "
        f"{outcomes} — the guard reads them, it does not type them"
    )
    page_classes = {_codify(noun) for noun in outcomes}
    report_classes = {"applicable", "exempt"}
    assert page_classes == report_classes, (
        "C-21 (page -> rule): the page's two decided outcomes are the report's two class "
        f"counters; got page={sorted(page_classes)} report={sorted(report_classes)}"
    )
    row = _payload(_run_engine("--json", "--emit-rule"))  # a rule-mode payload carries both
    assert set(report_classes) <= set(row), (
        f"C-21: the report carries both class counters; keys: {sorted(row)}"
    )
    # Rule -> page, for the one basis the page DOES codify: it must stay a value the engine's
    # closed set carries, or the page would name a member the engine cannot produce.
    module_bases = set(module.EXEMPT_BASIS)
    page_codified_bases = {token for token in re.findall(r"`([a-z][a-z-]+)`", page)
                           if token in module_bases}
    assert "mirror-unpaired" in page_codified_bases, (
        "C-21: the page's step 2 names `mirror-unpaired` in code; got "
        f"{sorted(page_codified_bases)}"
    )
    assert page_codified_bases <= set(rule["exempt_basis"]) | set(
        _RESERVED_BASES), (
        "C-21 (page -> rule): every basis the page codifies is one the rule emits or one the "
        f"engine reserves; unknown {sorted(page_codified_bases - set(rule['exempt_basis']) - set(_RESERVED_BASES))}"
    )
    # And the pair is the same through the other door.
    assert list(module.classification_rule()["labels"]) == list(rule["labels"]), (
        "C-21: the imported engine and the called engine publish one label set"
    )


#: The bases the engine's closed set carries but `--emit-rule` does not publish: only a
#: declared-exception row can produce them (the register's own recomputation), so the emitted
#: rule stays silent about them by design — a rule naming a basis no run of it can emit would
#: be a rule the reader cannot check against a report.
_RESERVED_BASES = (
    "declared-exception",
    "mirror-unpaired",
)


def _codify(noun: str) -> str:
    """The report's spelling for one of the page's Chinese outcome nouns."""
    return {"适用": "applicable", "豁免": "exempt"}[noun]


def _checker_label_keys() -> list[str]:
    """The four labels the probe actually judges — read from `HELP_LABEL_PATTERNS`."""
    return list(_engine_module()._label_hits("").keys())


def test_t084_an_option_before_the_subcommand_is_never_silently_ignored(tmp_path):
    """T084 / FR-018: the `goal-utils.py` class — a pre-subcommand option dropped on the floor.

    The assertion is position INDEPENDENCE in the only sense decidable from outside: after the
    subcommand the option is honoured (`json`); before it, the run either honours it too
    (`json`) or refuses it — and the refusal is C-9's own face (non-zero, nothing printed). The
    third outcome is the library's own defect: exit 0, the subcommand runs, and the option is
    gone (`human`). The guard therefore asserts the property that IS guaranteed at both
    positions — C-9's rejection — and pins the library's knowledge of its own discrepancy.
    """
    import shutil

    library = ENGINE.with_name("script_interface_cli.py")
    outcomes = {}
    for label, echo_top in (("honour", True), ("library-defect", False)):
        tree = _scenario_tree(tmp_path / label)
        shutil.copy(library, tree / "scripts" / "script_interface_cli.py")
        _write_shaped(tree, echo_top=echo_top)
        _git(tree, "add", "-A")
        _git(tree, "commit", "-q", "-m", "scenario: a subcommand-shaped script")
        after = _run_in_python(tree, "scripts/" + POSITIONAL_FIXTURE_NAME,
                               "list", POSITIONAL_OPTION)
        assert after.returncode == 0 and after.stdout.strip() == "json", (
            f"T084: `list {POSITIONAL_OPTION}` is honoured for the {label!r} shape; got "
            f"{after.returncode} {after.stdout!r} {after.stderr[-400:]!r}"
        )
        before = _run_in_python(tree, "scripts/" + POSITIONAL_FIXTURE_NAME,
                                POSITIONAL_OPTION, "list")
        outcomes[label] = (before.returncode, before.stdout.strip())

        # C-9 and FR-018 at BOTH positions: an undeclared token is refused wherever it sits,
        # nothing is acted on, and the message names it. This is what the engine's guard owes
        # and what the fixture measures, so a guard that scanned only the tail is caught here.
        for order in (("--bogus", "list"), ("list", "--bogus")):
            refused = _run_in_python(tree, "scripts/" + POSITIONAL_FIXTURE_NAME, *order)
            assert refused.returncode == 2, (
                f"T084/C-9: an undeclared token is refused at position {order}; got "
                f"{refused.returncode}"
            )
            assert "unrecognized option" in refused.stderr, (
                f"T084/C-9: the refusal names the token at position {order}; got "
                f"{refused.stderr[:400]!r}"
            )
            assert refused.stdout == "", (
                f"T084/C-9: a refused run acts nowhere at position {order}; stdout="
                f"{refused.stdout[:400]!r}"
            )

    assert outcomes["honour"] == (0, "json"), (
        "T084: the position-independent shape honours the option BEFORE the subcommand; got "
        f"{outcomes['honour']}"
    )
    assert outcomes["library-defect"] == (0, "human"), (
        "T084/FR-018: the library's own `goal-utils.py` shape still drops a pre-subcommand "
        f"option — the recorded discrepancy; got {outcomes['library-defect']}"
    )
    goal = _text(ROOT / "scripts" / "python" / "goal-utils.py")
    assert "NOT make them position-independent" in goal, (
        "T084: the discrepancy is documented at the library's own parser, so the fixture's "
        "second shape is the measured behaviour of a real script rather than an invented one"
    )


def test_t084_the_live_goal_utils_position_is_read_and_judged(tmp_path):
    """T084: the class's own instance, read live — where ITS two positions land.

    `goal-utils.py` states the defect in its own source ("`--json list` silently emits the human
    form"), so the guard records the observation rather than assuming either answer. Its
    guard's declaration is the option vocabulary the ENGINE refuses against, which is the
    position-independence the engine owes: both positions are judged before any parser runs.
    """
    import subprocess
    import sys

    goal = ROOT / "scripts" / "python" / "goal-utils.py"
    after = subprocess.run([sys.executable, str(goal), "status", "--json"], cwd=str(ROOT),
                           capture_output=True, text=True, timeout=120)
    before = subprocess.run([sys.executable, str(goal), "--json", "status"], cwd=str(ROOT),
                            capture_output=True, text=True, timeout=120)
    # C-9's leg, at BOTH positions: an undeclared token is refused wherever it sits.
    for position in (("--bogus", "status"), ("status", "--bogus")):
        proc = subprocess.run([sys.executable, str(goal), *position], cwd=str(ROOT),
                              capture_output=True, text=True, timeout=120)
        assert proc.returncode == 2, (
            f"T084/C-9: an undeclared token is refused at position {position}; got "
            f"{proc.returncode}"
        )
        assert "unrecognized option" in proc.stderr, (
            f"T084/C-9: the refusal names the token at position {position}; got "
            f"{proc.stderr[:400]!r}"
        )
        assert proc.stdout == "", (
            f"T084/C-9: a refused run acts nowhere at position {position}; stdout="
            f"{proc.stdout[:400]!r}"
        )
    # The library defect is observable, so record it instead of asserting it away: the two
    # positions must not BOTH exit 0 with different answers and no diagnostic.
    if after.returncode == 0 and before.returncode == 0 and after.stdout != before.stdout:
        assert "silently" in _text(goal) or "--json" in before.stderr, (
            "T084/FR-018: a pre-subcommand option that changes nothing is either refused, "
            "honoured, or documented as the library's measured behavior; goal-utils.py states "
            "it, and this assertion keeps that statement from being deleted unnoticed"
        )


def test_t078_a_projection_never_answers_the_version_it_so_loudly_does_not_print(tmp_path):
    """T078 (C-32's one new checker, C-36's no-new-script form): the gap found at closure.

    Closing a rule across a whole repository turns every consumer into a candidate, and a
    consumer that answers `--version` with `unknown` is a FIX rather than a rule change. The
    house form for that fix is not a new script: the declared `bash-version-guard` projection
    is a block emitted at the top of every consumer's mirror, so a consumer that must know its
    version carries that block. This test is the mechanical form of that decision — measured,
    not assumed, and worded so that it never claims a file list belongs to C-32.
    """
    library = _text(GUARD_LIBRARY)
    text_function = library.split("script_interface_version_text() {", 1)
    assert len(text_function) == 2, (
        "T078/C-32: the version function lives in the ONE library, not in a third script"
    )
    assert '_source="${_SCRIPT_INTERFACE_VERSION_SOURCE:-pyproject.toml}"' in \
        text_function[1].split("\n}", 1)[0], (
        "T078/C-36: the block re-derives its source rather than carrying a version literal"
    )
    # The block the projection splices is the library's OWN body, re-indented by the engine —
    # compared by its statements rather than by spelling, because the engine normalises
    # indentation on the way in (T076's sentinel rule, asserted there).
    body = [line.strip() for line in
            _sync_module().version_text_function_body(library).splitlines() if line.strip()]
    assert body, "T078/C-36: the library publishes the function the sentinel carries"
    consumers = sorted(_consumers_of_the_guard())
    assert len(consumers) >= 5, (
        f"T078: the guard has consumers to project; got {consumers}"
    )
    for relative in consumers:
        projected = _projected_bash_mirror(_consumer_source(relative))
        assert "script_interface_version_text() {" in projected, (
            f"T078/C-36: `{relative}`'s declared projection carries the version block, so its "
            "mirror answers the version without sourcing anything"
        )
        statements = [line.strip() for line in projected.splitlines()]
        assert all(statement in statements for statement in body), (
            f"T078/C-36: `{relative}`'s projection carries the library's own statements, not a "
            f"second spelling; missing {[s for s in body if s not in statements][:3]}"
        )
        # The block is the FIRST executable block: above every `source`, every write.
        first_executable = _first_executable_line(projected)
        version_definition = projected.splitlines().index(
            "script_interface_version_text() {")
        assert first_executable == version_definition, (
            f"T078: `{relative}`'s projection opens with the version block (line "
            f"{version_definition}); its first executable line is {first_executable}"
        )


def test_t077_the_live_rejection_face_on_a_sandbox_copy(tmp_path):
    """T077: `--no-such-flag` is refused non-zero on the LIVE face, and nothing is written."""
    import shutil

    tree = _probe_tree(tmp_path, {"scripts/writer.sh": None})
    shutil.copy(GUARD_LIBRARY, tree / "scripts" / "script-interface.sh")
    writer = tree / "scripts" / "writer.sh"
    writer.write_text(
        "#!/usr/bin/env bash\n"
        'SCRIPT_DIR="$(CDPATH="" cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"\n'
        'if [ -f "$SCRIPT_DIR/script-interface.sh" ]; then\n'
        '    . "$SCRIPT_DIR/script-interface.sh"\n'
        '    script_interface_guard define name="$0" \\\n'
        '        usage="[--out PATH]" \\\n'
        '        effects="writes OUT; the flags write nothing" \\\n'
        '        codes="0 wrote; 2 an unrecognized option" \\\n'
        '        writes=--out \\\n'
        '        -- --out\n'
        '    script_interface_guard guard "$@"\n'
        "fi\n"
        "out=out.txt\n"
        'for arg in "$@"; do\n'
        '    case "$arg" in --out=*) out="${arg#--out=}" ;; esac\n'
        "done\n"
        'printf written > "$out"\n',
        encoding="utf-8")
    writer.chmod(0o755)
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "scenario: a writer on the real guard")
    before = _tree_snapshot(tree)
    proc = _run_in_tree(tree, "scripts/writer.sh", "--no-such-flag")
    assert proc.returncode == 2, (
        f"T077/C-9: an undeclared token exits non-zero (the library's own code is 2); got "
        f"{proc.returncode}")
    assert "unrecognized option" in proc.stderr, (
        f"T077/C-9: the error is on stderr; stderr={proc.stderr[:400]!r}")
    for label in ("usage:", "options:", "side-effects:", "exit-codes:"):
        assert label in proc.stderr, (
            f"T077/C-9: the usage goes to stderr and carries `{label}`; "
            f"stderr={proc.stderr[:600]!r}")
    assert proc.stdout == "", (
        f"T077/C-9: nothing reaches stdout before the rejection; got {proc.stdout[:200]!r}")
    assert not (tree / "out.txt").exists(), (
        "T077/C-9: the write target was never created — the token never reached the action")
    assert _tree_snapshot(tree) == before, (
        "T077/C-10: the rejected run leaves the sandbox copy's snapshot pair identical")
    for order in (("--help", "--out", "won.txt"), ("--out", "won.txt", "--help")):
        helped = _run_in_tree(tree, "scripts/writer.sh", *order)
        assert helped.returncode == 0 and "usage:" in helped.stdout, (
            f"T077/C-11: `{' '.join(order)}` answers help; got {helped.returncode}")
        assert not (tree / "won.txt").exists(), (
            f"T077/C-11: the flag wins over the write in `{' '.join(order)}`")
