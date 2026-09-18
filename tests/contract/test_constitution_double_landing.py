"""Contract test: constitution-export — the double landing of two principles downstream.

Implements ``.specify/specs/051-user-facing-comprehension/contracts/constitution-export.md``
**C-1…C-13**. ``test_cN_*`` maps one-to-one onto that file's C-N.

The defect this file exists to prevent is a **single-sided landing**: a principle written into
this repository's live constitution but never into the two templates that downstream projects
are generated from, so no other project ever receives it. That happened for real — Principle
XIV (One Source of Truth) reached the live constitution and `grep -c "One Source"` returned 0
in *both* templates. C-7's watchlist plus C-10's mutation probe turn that accident into the
first tested sample of the guard that should have caught it.

Two deliberate design constraints:

* **No roman numerals are pinned** (C-8). The template roster and the live constitution roster
  are different sizes (13 vs 15) and either can grow; a matcher keyed to `### XIV.` would
  misfire the day a principle is inserted above it. Titles are matched by name, and the
  matcher's numeral-agnosticism is itself asserted.
* **Set membership, never substring containment** (C-7). `Code as the Single Source of Truth`
  and `One Source of Truth (Authority & Reference Discipline)` share the substring
  `Source of Truth`; a substring test would silently merge two distinct principles (C-9).
"""
from __future__ import annotations

import importlib.util
import re
import shutil
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "templates" / "constitution-template.md"
COMMAND = ROOT / "templates" / "commands" / "constitution.md"
LIVE = ROOT / ".specify" / "memory" / "constitution.md"
SCANNER = ROOT / "scripts" / "python" / "scan-confirmation-gates.py"

# C-1: the two titles, verbatim.
STR006_TITLE = "One Source of Truth (Authority & Reference Discipline)"
STR003_TITLE = "User-Facing Comprehension (No Jargon, With Context)"
NEW_TEMPLATE_TITLES = (STR006_TITLE, STR003_TITLE)

# C-7: the named double-landing watchlist. Membership is asserted on BOTH sides for every
# entry; adding a principle here is how a future landing gets guarded.
DOUBLE_LANDING_WATCHLIST = (
    "User-Facing Comprehension (No Jargon, With Context)",
    "One Source of Truth (Authority & Reference Discipline)",
)

# C-8: numeral-agnostic matchers. `[IVXLC0-9]+` accepts roman or arabic; nothing pins a value.
# `re.M` is load-bearing: without it `^`/`$` anchor to the whole string and the title set comes
# back empty, which reads as "the principles are missing" rather than "the matcher is broken".
TEMPLATE_TITLE_RE = re.compile(r"^### ([IVXLC0-9]+)\. (.+)$", re.M)
COMMAND_NAME_RE = re.compile(r'\*\*MUST include\*\* a principle for "([^"]+)"')
# The list entries are indented sub-bullets, so a form check must tolerate leading whitespace.
COMMAND_ENTRY_RE = re.compile(r'^\s*- \*\*MUST include\*\* a principle for "([^"]+)" that mandates:\s*$', re.M)
COMMAND_ENTRY_END_RE = r"^\s*(?:- \*\*MUST include\*\*|- Ensure )"
LIVE_TITLE_RE = TEMPLATE_TITLE_RE

# C-9: the pre-existing command-side entry that shares a substring with STR-006.
CODE_SSOT_NAME = "Code as the Single Source of Truth"

TEMPLATE_COUNT = 13     # 11 pre-existing + 2 landed here
LIVE_COUNT = 15         # 14 pre-existing + 1 (XIV already carries STR-006)
COMMAND_COUNT = 7       # 5 pre-existing + 2
MIN_VERSION = (1, 12)   # floor semantics, never an equality pin


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _flat(text: str) -> str:
    """Collapse whitespace so a phrase split across hard-wrapped lines still matches.

    C-2(d) requires lines under 100 chars, which necessarily breaks fixed phrases such as
    "reference it, do not restate it" across a newline. Matching against the raw text would
    report a missing obligation that is present, so phrase assertions run on the flattened
    form while structural assertions (line length, blank-line placement) run on the raw one.
    """
    return re.sub(r"\s+", " ", text)


def _template_titles(text: str) -> set[str]:
    return {m.group(2).strip() for m in TEMPLATE_TITLE_RE.finditer(text)}


def _template_numerals(text: str) -> list[str]:
    return [m.group(1) for m in TEMPLATE_TITLE_RE.finditer(text)]


def _command_names(text: str) -> set[str]:
    return {m.group(1).strip() for m in COMMAND_NAME_RE.finditer(text)}


def _principle_block(text: str, title: str) -> str:
    """One principle's block: its heading line plus body up to the next `### ` or `## `."""
    m = re.search(
        rf"^### [IVXLC0-9]+\. {re.escape(title)}\s*$(.*?)(?=^### |^## |\Z)",
        text, re.M | re.S,
    )
    assert m, f"principle {title!r} not found"
    return m.group(0)


def _load_scanner():
    spec = importlib.util.spec_from_file_location("_scan_gates_constitution", SCANNER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _logical_bullets(lines: list[str]) -> list[tuple[int, int, str]]:
    """Group hard-wrapped list items into logical bullets.

    Returns (first_line_index, last_line_index, joined_text) per bullet. C-2(c)'s "3–6 bullets,
    each containing MUST" is about logical bullets; C-2(d)'s line-length rule is about physical
    ones. Checking a physical line for MUST reports a missing obligation whenever the wrap puts
    `- …` and `… MUST …` on different lines, which the <100-char rule makes the normal case.
    """
    out = []
    start = None
    for i, ln in enumerate(lines):
        if re.match(r"^\s*-\s+", ln):
            if start is not None:
                out.append((start, i - 1, " ".join(x.strip() for x in lines[start:i])))
            start = i
        elif start is not None and ln.strip() and not ln.startswith("Rationale:"):
            continue
        elif start is not None:
            out.append((start, i - 1, " ".join(x.strip() for x in lines[start:i])))
            start = None
    if start is not None:
        out.append((start, len(lines) - 1, " ".join(x.strip() for x in lines[start:])))
    return out


def _check_structure(block: str, title: str) -> None:
    """C-2's (a)–(g), applied to one principle block."""
    lines = block.splitlines()
    heading = lines[0]
    assert re.match(r"^### [IVXLC]+\. .+$", heading), f"(a) bad heading form: {heading!r}"

    bullets = _logical_bullets(lines)
    assert bullets, f"(c) {title}: no bullets"
    first_bullet = bullets[0][0]

    # (b) The claim is one sentence ending in a colon, but (d) hard-wraps it, so it is read as
    # the joined text between the heading and the first bullet — not as `lines[1]` alone.
    claim = " ".join(ln.strip() for ln in lines[1:first_bullet] if ln.strip())
    assert claim.endswith(":"), (
        f"(b) {title}: the sentence between the heading and the first bullet must end with a "
        f"colon; got …{claim[-70:]!r}"
    )

    assert 3 <= len(bullets) <= 6, (
        f"(c) {title}: expected 3-6 MUST bullets, got {len(bullets)}"
    )
    for _, _, text in bullets:
        assert "MUST" in text, f"(c) {title}: bullet carries no MUST/MUST NOT: {text[:70]!r}"

    long_lines = [ln for ln in lines if len(ln) >= 100]
    assert not long_lines, (
        f"(d) {title}: lines must hard-wrap under 100 chars; {len(long_lines)} do not, "
        f"longest {max(len(x) for x in long_lines)}"
    )

    rat_idx = next((i for i, ln in enumerate(lines) if ln.startswith("Rationale:")), None)
    assert rat_idx is not None, f"(f) {title}: no paragraph starting with the literal `Rationale:`"
    last_bullet_line = bullets[-1][1]
    between = [i for i in range(last_bullet_line + 1, rat_idx) if lines[i].strip()]
    assert not between, (
        f"(e) {title}: expected exactly one blank line between the bullets and Rationale:, "
        f"found content on lines {between}"
    )
    assert rat_idx == last_bullet_line + 2, (
        f"(e) {title}: Rationale: must follow the bullets after exactly one blank line "
        f"(bullets end at {last_bullet_line}, Rationale: at {rat_idx})"
    )
    rationale = " ".join(ln.strip() for ln in lines[rat_idx:] if ln.strip())
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", rationale) if s.strip()]
    assert 1 <= len(sentences) <= 4, (
        f"(f) {title}: Rationale: must be 1-4 sentences, got {len(sentences)}"
    )
    assert not re.search(r"\[[A-Z_]{3,}\]", block), (
        f"(g) {title}: unresolved bracket placeholder left in the principle"
    )


# --- C-1: both titles land in the template ---


def test_c1_template_carries_both_new_principles():
    text = _text(TEMPLATE)
    titles = _template_titles(text)
    missing = [t for t in NEW_TEMPLATE_TITLES if t not in titles]
    assert not missing, f"template is missing principle titles: {missing}"
    numerals = _template_numerals(text)
    assert len(numerals) == TEMPLATE_COUNT, (
        f"template has {len(numerals)} principles, expected {TEMPLATE_COUNT}"
    )
    # Order: the two new ones sit after the pre-existing XI and before the next H2 section.
    order = [m.group(2).strip() for m in TEMPLATE_TITLE_RE.finditer(text)]
    assert order.index(STR006_TITLE) < order.index(STR003_TITLE), (
        "STR-006 (XII) must precede STR-003 (XIII)"
    )


# --- C-2 / C-3 / C-4: structure, anchoring, scope limit ---


@pytest.mark.parametrize("title", NEW_TEMPLATE_TITLES)
def test_c2_new_principle_structure_is_compliant(title):
    _check_structure(_principle_block(_text(TEMPLATE), title), title)


@pytest.mark.parametrize("title", NEW_TEMPLATE_TITLES)
def test_c3_new_principle_anchors_its_truth_document(title):
    block = _principle_block(_text(TEMPLATE), title)
    assert ".specify/shared/guidelines/" in block, (
        f"{title}: no anchor into .specify/shared/guidelines/ — a principle whose detail lives "
        "in an owner document must name it"
    )
    assert re.search(r"reference it, do not restate it|never restate", _flat(block), re.I), (
        f"{title}: the anchoring bullet must state reference-not-restate semantics"
    )


@pytest.mark.parametrize("title", NEW_TEMPLATE_TITLES)
def test_c4_new_principle_declares_no_new_machinery(title):
    block = _flat(_principle_block(_text(TEMPLATE), title))
    assert re.search(r"MUST NOT (be used to )?justify", block), (
        f"{title}: missing the scope-limit bullet — the principle must not become a licence "
        "for new machinery"
    )
    assert re.search(r"scoring|maturity report|tracking", block, re.I), (
        f"{title}: the scope limit must name the machinery it refuses"
    )


# --- C-5 / C-6: the command-side landing ---


def test_c5_command_must_include_list_has_both_entries():
    text = _text(COMMAND)
    names = _command_names(text)
    missing = [t for t in NEW_TEMPLATE_TITLES if t not in names]
    assert not missing, f"command MUST-include list is missing: {missing}"
    # The list total counts *entries*, not entries in one particular phrasing: the
    # pre-existing "Documentation-First" entry reads `… that is ordered ABOVE any …` rather
    # than `… that mandates:`, so a form-strict count returns 6 and hides the seventh.
    assert len(names) == COMMAND_COUNT, (
        f"command MUST-include list has {len(names)} entries, expected {COMMAND_COUNT}: "
        f"{sorted(names)}"
    )
    # The verbatim form C-5 requires applies to the two entries this feature adds.
    verbatim = set(COMMAND_ENTRY_RE.findall(text))
    for title in NEW_TEMPLATE_TITLES:
        assert title in verbatim, (
            f"the new entry for {title!r} is not in the required verbatim form "
            "`- **MUST include** a principle for \"<title>\" that mandates:`"
        )


def _command_entry_body(text: str, title: str) -> str:
    m = re.search(
        rf'^\s*- \*\*MUST include\*\* a principle for "{re.escape(title)}"[^\n]*$'
        rf'(.*?)(?={COMMAND_ENTRY_END_RE}|\Z)',
        text, re.M | re.S,
    )
    assert m, f"command entry for {title!r} not found"
    return m.group(1)


@pytest.mark.parametrize("title", NEW_TEMPLATE_TITLES)
def test_c6_command_entry_has_anchor_and_scope_sub_bullets(title):
    body = _flat(_command_entry_body(_text(COMMAND), title))
    assert ".specify/shared/guidelines/" in body, f"{title}: no truth-document anchor"
    assert "MUST be referenced, not restated" in body, (
        f"{title}: the anchor sub-bullet must carry the referenced-not-restated rule"
    )
    assert re.search(r"not machinery|MUST NOT justify", body), (
        f"{title}: missing the no-new-machinery sub-bullet"
    )


# --- C-7: the watchlist lands on both sides, by set membership ---


def test_c7_watchlist_principles_land_on_both_sides():
    template_titles = _template_titles(_text(TEMPLATE))
    command_names = _command_names(_text(COMMAND))
    for title in DOUBLE_LANDING_WATCHLIST:
        assert title in template_titles, (
            f"watchlist principle {title!r} is absent from templates/constitution-template.md — "
            "a single-sided landing: the live constitution may carry it, but no downstream "
            "project generated from the template ever will"
        )
        assert title in command_names, (
            f"watchlist principle {title!r} is absent from templates/commands/constitution.md's "
            "MUST-include list — the generator is never told to emit it"
        )


# --- C-8: the matcher must not depend on a numeral ---


def test_c8_matcher_is_numeral_agnostic():
    # A self-check on this test's own matching logic: the same regexes must resolve a title
    # under a numeral this repo has never used. Pinning `### XIV.` is the defect C-8 forbids
    # (and one an existing sibling test still carries).
    #
    # The probe numerals stay inside the contract's `[IVXLC0-9]` class on purpose — C-7(a)
    # specifies that class, and widening it here would test a matcher the contract does not
    # define. What C-8 forbids is pinning a *value*, not covering every roman digit.
    synthetic = (
        "### VII. Alpha Principle\nclaim:\n- MUST do x\n\nRationale: because.\n\n"
        "### XLII. User-Facing Comprehension (No Jargon, With Context)\n"
        "claim:\n- MUST do y\n\nRationale: because.\n\n"
        "### 9. One Source of Truth (Authority & Reference Discipline)\n"
        "claim:\n- MUST do z\n\nRationale: because.\n"
    )
    parsed = _template_titles(synthetic)
    assert STR003_TITLE in parsed, "the title matcher depends on a familiar roman numeral"
    assert STR006_TITLE in parsed, "the title matcher does not accept arabic numerals"
    assert "Alpha Principle" in parsed
    assert _template_numerals(synthetic) == ["VII", "XLII", "9"]
    for literal in (TEMPLATE_TITLE_RE.pattern, COMMAND_NAME_RE.pattern):
        assert not re.search(r"\b(XIV|XV|XII|XIII)\b", literal), (
            f"a roman numeral is pinned in a matcher: {literal}"
        )


# --- C-9: two principles sharing a substring stay distinct ---


def test_c9_code_ssot_and_str006_are_not_merged():
    names = _command_names(_text(COMMAND))
    assert CODE_SSOT_NAME in names, (
        f"the pre-existing command entry {CODE_SSOT_NAME!r} disappeared"
    )
    assert STR006_TITLE in names, f"{STR006_TITLE!r} missing from the command name set"
    assert CODE_SSOT_NAME != STR006_TITLE
    # They share a substring, which is exactly why containment matching is forbidden.
    assert "Source of Truth" in CODE_SSOT_NAME and "Source of Truth" in STR006_TITLE
    watchlist_hits = [t for t in DOUBLE_LANDING_WATCHLIST if t in names]
    assert CODE_SSOT_NAME not in watchlist_hits, (
        "the watchlist must not capture Code as the Single Source of Truth; if it does, the "
        "matcher has degraded to substring containment"
    )


# --- C-10: mutation probe — the guard must actually fail ---


@pytest.mark.parametrize("side", ["template", "command"])
def test_c10_removing_a_watchlist_principle_breaks_c7(side, tmp_path):
    """Delete one watchlist title from a *copy*; C-7's condition must then be false.

    Operates on temp copies — never on the repository's real files.
    """
    victim = DOUBLE_LANDING_WATCHLIST[0]
    if side == "template":
        mutant = tmp_path / "constitution-template.md"
        text = _text(TEMPLATE)
        # Drop the whole principle block, which is how a real regression would look.
        mutant.write_text(
            re.sub(rf"^### [IVXLC0-9]+\. {re.escape(victim)}\s*$.*?(?=^### |^## |\Z)",
                   "", text, flags=re.M | re.S),
            encoding="utf-8",
        )
        assert victim not in _template_titles(mutant.read_text(encoding="utf-8")), (
            "the mutation did not take effect — this probe would pass vacuously"
        )
        assert victim in _template_titles(text), "anti-vacuity: the real template must carry it"
    else:
        mutant = tmp_path / "constitution.md"
        text = _text(COMMAND)
        mutant.write_text(
            re.sub(
                rf'^\s*- \*\*MUST include\*\* a principle for "{re.escape(victim)}" that mandates:\s*$.*?(?={COMMAND_ENTRY_END_RE}|\Z)',
                "", text, flags=re.M | re.S,
            ),
            encoding="utf-8",
        )
        assert victim not in _command_names(mutant.read_text(encoding="utf-8")), (
            "the mutation did not take effect — this probe would pass vacuously"
        )
        assert victim in _command_names(text), "anti-vacuity: the real command must carry it"
    # The mutant is a temp copy; the repository files are untouched.
    assert victim in _template_titles(_text(TEMPLATE))
    assert victim in _command_names(_text(COMMAND))


# --- C-11 / C-12: this repository's own constitution ---


def test_c11_live_constitution_carries_the_comprehension_principle():
    text = _text(LIVE)
    titles = {m.group(2).strip() for m in LIVE_TITLE_RE.finditer(text)}
    assert STR003_TITLE in titles, (
        f".specify/memory/constitution.md carries no principle titled {STR003_TITLE!r}"
    )
    numerals = [m.group(1) for m in LIVE_TITLE_RE.finditer(text)]
    assert len(numerals) == LIVE_COUNT, (
        f"live constitution has {len(numerals)} principles, expected {LIVE_COUNT}"
    )
    block = _principle_block(text, STR003_TITLE)
    _check_structure(block, STR003_TITLE)
    flat = _flat(block)
    assert ".specify/shared/guidelines/" in flat, "C-11 via C-3: no truth-document anchor"
    assert re.search(r"MUST NOT (be used to )?justify", flat), "C-11 via C-4: no scope limit"


def test_c12_live_constitution_version_and_sync_impact_report():
    text = _text(LIVE)
    m = re.search(r"^\*\*Version\*\*:\s*(\d+)\.(\d+)", text, re.M)
    assert m, "no `**Version**:` line found"
    got = (int(m.group(1)), int(m.group(2)))
    assert got >= MIN_VERSION, (
        f"constitution version {got} is below the floor {MIN_VERSION} — adding a principle is a "
        "MINOR bump per the constitution command's versioning policy"
    )
    head = "\n".join(text.splitlines()[:40])
    assert "Sync Impact Report" in head, (
        "the Sync Impact Report must be prepended as an HTML comment at the top of the file"
    )
    assert re.search(r"Version change:.*→", head), "the report must state the version change"
    assert STR003_TITLE.split(" (")[0] in head, (
        "the report must name the principle this amendment added"
    )


# --- C-13: gate-budget neutrality of the two new template blocks ---


@pytest.mark.parametrize("title", NEW_TEMPLATE_TITLES)
def test_c13_new_principle_blocks_have_zero_blocking_hits(title):
    blocking_re = _load_scanner().BLOCKING_RE
    block = _principle_block(_text(TEMPLATE), title)
    hits = []
    for lineno, line in enumerate(block.splitlines(), 1):
        hits.extend(f"L{lineno}:{m.group(0)!r}" for m in blocking_re.finditer(line))
    assert not hits, (
        f"principle {title!r} trips BLOCKING_RE: {hits}. `constitution-template.md` matches the "
        "scanner's governance-path patterns so a hit is classified governance_kept — but "
        "governance_kept still counts toward `total`, which is pinned at 23 by equality, so any "
        "hit here breaks two existing contract tests."
    )
