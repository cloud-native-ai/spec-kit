"""Contract test: self-explanatory constitution landing (Feature 082).

Implements ``.specify/specs/082-self-explanatory-integration/contracts/constitution-double-landing.contract.md``
(clauses C-1, C-2, C-3, C-4, C-6, C-7, C-8) and the two "reference, not copy" clauses of
``contracts/mirror-distribution.contract.md`` (C-20, C-21) that are decidable against the very
surfaces this module already reads.

This module is deliberately SEPARATE from ``test_constitution_double_landing.py``: that carrier
holds load-time count constants (C-5/C-7/C-8/C-9) that Feature 082 must bump in a later phase
(T016). Writing the new assertions into a new module keeps the whole US1 red-first capture out of
an existing file's import-time constants, so the red is attributable to the missing artifact and
not to a half-updated carrier.

Red-first provenance (`tasks.md` T006): this module was created and run BEFORE the principle
existed, and the run is recorded in
``.specify/specs/082-self-explanatory-integration/notes/red-first-evidence.md``. The red comes from
the assertion below — NOT from the two pre-existing suites, which pass and never reference
`[[STR-001]]`.

Term isolation: the headings' identity is `[[STR-001]]`; the owner location is `[[STR-002]]`
(framework source) / `[[STR-004]]` (runtime). The literal values live in
``requirements.md`` § Shared Strings and are NOT restated here beyond the one string this module
asserts.

C-7 is deliberately one-sided here (the template side only). Its mandate-side half lives in the
carrier file, which owns the generator skill's MUST-include set and the count that goes with it;
asserting it twice would create a second spelling of the same rule. Until T013 lands the mandate
entry, the carrier's C-7 is expected-red — that is `tasks.md`'s declared ordering, not a defect
this module may paper over.
"""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "templates" / "constitution-template.md"
INSTRUCTIONS_TEMPLATE = ROOT / "templates" / "instructions-template.md"
OWNER_SOURCE = ROOT / "shared" / "definitions" / "self-explanatory-definitions.md"
OWNER_MIRROR = ROOT / ".specify" / "shared" / "definitions" / "self-explanatory-definitions.md"
SCANNER = ROOT / "scripts" / "python" / "scan-confirmation-gates.py"

# C-3 / C-4: numeral-agnostic matcher, `re.M` load-bearing for the same reason as the carrier.
TEMPLATE_TITLE_RE = re.compile(r"^### ([IVXLC0-9]+)\. (.+)$", re.M)

# [[STR-001]] — the one literal this module asserts.
PRINCIPLE_TITLE = "Self-Explanatory Structure (不言自明)"
# [[STR-004]] — the client-facing runtime owner path the principle must point at.
RUNTIME_OWNER = ".specify/shared/definitions/self-explanatory-definitions.md"
# [[STR-002]] — the framework-source owner path. MAY appear only as the framework's own
# owner location, never as the path a downstream reader is told to open (requirements A11).
FRAMEWORK_OWNER = "shared/definitions/self-explanatory-definitions.md"

# C-6's five content obligations, each paired with a phrase that can only be its own.
# The pairing is what makes "each obligation is covered" decidable: a block that satisfied an
# obligation in a second form would have to carry a second phrase, which makes the assertion RED
# (fix the phrase table in the same change) instead of silently green.
#
# The rows are (name, marker, description) and the marker is a STRING, not a compiled pattern: the
# uniqueness search below is assignment-order dependent, and a compiled pattern is a C object whose
# identity C-free semantics can disturb (a generator-expression scope binding the row's second
# element to a stale match object, for one, makes a plain-string row still behave). Strings keep the
# search a value comparison, so the result cannot depend on which loop binding Python chose.
CONTENT_OBLIGATIONS = (
    ("user-view", "user", "user's view decides"),
    ("ceiling-floor", "ceiling", "ceiling / floor pair"),
    ("no-preventive-redesign", "preventive redesign", "the no-preventive-redesign scope limit"),
    ("one-dimension-per-task", "information dimension",
     "at most one information dimension per optimization task"),
    ("source-of-truth-projection", "projection",
     "an encoded attribute's original source of truth keeps ownership"),
)

# C-6 clause 2's three mechanical pieces (ceiling / floor / floor-sufficiency).
CEILING_PHRASE = "ceiling"
FLOOR_PHRASE = "floor"

HOUSE_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


def _read(path: Path) -> str:
    """Read a file, letting a missing artifact surface as FileNotFoundError.

    Unguarded on purpose: at red-first time the failure must read as "artifact missing", not as
    an assertion written wrong.
    """
    return path.read_text(encoding="utf-8")


def _template_titles(text: str) -> set[str]:
    return {m.group(2).strip() for m in TEMPLATE_TITLE_RE.finditer(text)}


def _flat(text: str) -> str:
    """Collapse whitespace so a phrase split across hard-wrapped lines still matches.

    C-2(d) requires lines under 100 chars, which necessarily breaks fixed phrases across a
    newline. Phrase assertions run on the flattened form; structural ones on the raw text.
    """
    return re.sub(r"\s+", " ", text)


def _principle_block(text: str, title: str = PRINCIPLE_TITLE) -> str:
    """One principle's block: its heading line plus body up to the next `### ` or `## `."""
    m = re.search(
        rf"^### [IVXLC0-9]+\. {re.escape(title)}\s*$(.*?)(?=^### |^## |\Z)",
        text, re.M | re.S,
    )
    assert m, (
        f"principle {title!r} not found in the surface under test; this module cannot judge its "
        "shape until the principle lands"
    )
    return m.group(0)


def _logical_bullets(lines: list[str]) -> list[tuple[int, int, str]]:
    """Group hard-wrapped list items into logical bullets.

    Returns (first_line_index, last_line_index, joined_text) per bullet. C-2(c)'s "3–6 bullets,
    each containing MUST" is about logical bullets while C-2(d)'s line-length rule is about
    physical ones; checking a physical line for MUST reports a missing obligation whenever the
    wrap puts `- …` and `… MUST …` on different lines, which the <100-char rule makes normal.
    """
    out: list[tuple[int, int, str]] = []
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


def _load_scanner():
    spec = importlib.util.spec_from_file_location("_scan_gates_self_explanatory", SCANNER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --- C-1: the template carries the principle ---


def test_c1_template_carries_the_principle() -> None:
    """C-1: the title is a MEMBER of the template's title set (set membership, never substring)."""
    titles = _template_titles(_read(TEMPLATE))
    assert PRINCIPLE_TITLE in titles, (
        f"templates/constitution-template.md is missing the principle titled {PRINCIPLE_TITLE!r}; "
        f"present titles: {sorted(titles)}"
    )


# --- C-3 / C-4: the matcher covers the new title and pins no numeral ---


def test_c3_matcher_resolves_the_principle_under_an_unused_numeral() -> None:
    """C-3/C-4: a synthetic roster using a numeral this repository never used still resolves.

    The probe numeral (`XCI`) is purpose-chosen, not decorative: the real rosters use I–XVII
    (template) and I–XVIII (live), so no repository numeral collides with it, and a matcher keyed
    to any real value fails here while the real files keep passing.
    """
    synthetic = (
        "### XCI. Self-Explanatory Structure (不言自明)\n"
        "claim:\n- MUST do x\n\nRationale: because.\n"
    )
    assert PRINCIPLE_TITLE in _template_titles(synthetic), (
        "the title matcher cannot resolve the principle under an unused numeral — it is pinned"
    )
    source = TEMPLATE_TITLE_RE.pattern
    assert not re.search(r"\b(I|II|III|XVII|XVIII)\b", source), (
        f"a roman numeral is pinned in the title matcher: {source}"
    )


def test_c4_no_pinned_numeral_where_this_principle_lands() -> None:
    """C-3: the numerals are per-surface, so neither side may be pinned in this module's matchers.

    Decided against the module's compiled patterns rather than against a search of its own source
    text: a source scan matches the probe literal C-3 itself requires (an unused numeral written
    into a test), so it would forbid the very assertion that proves the matcher is agnostic — a
    check that cannot go green without deleting the thing it is guarding. The patterns are the
    thing that could actually pin a numeral, so they are what is inspected.
    """
    template_titles = _template_titles(_read(TEMPLATE))
    assert PRINCIPLE_TITLE in template_titles, (
        "precondition: C-1 must hold before the numeral discipline can be judged"
    )
    numerals = dict(
        (m.group(2).strip(), m.group(1)) for m in TEMPLATE_TITLE_RE.finditer(_read(TEMPLATE))
    )
    assert numerals[PRINCIPLE_TITLE], "the principle must carry a numeral on the template surface"
    assert not re.search(r"\b(XCI|XVIII|XVII)\b", TEMPLATE_TITLE_RE.pattern), (
        f"the title matcher pins a numeral value: {TEMPLATE_TITLE_RE.pattern}"
    )
    assert re.search(r"\[IVXLC0-9\]\+", TEMPLATE_TITLE_RE.pattern), (
        "the title matcher must accept any numeral (roman or arabic), not a fixed set of values"
    )


# --- C-2: the house shape of the principle block ---


def _check_structure(block: str) -> list[str]:
    """C-2's (a)–(g), applied to one principle block; returns nothing, raises on violation."""
    lines = block.splitlines()
    heading = lines[0]
    assert re.match(r"^### [IVXLC0-9]+\. .+$", heading), f"(a) bad heading form: {heading!r}"

    bullets = _logical_bullets(lines)
    assert bullets, "(c) the principle carries no bullets"
    first_bullet = bullets[0][0]

    claim = " ".join(ln.strip() for ln in lines[1:first_bullet] if ln.strip())
    assert claim.endswith(":"), (
        "(b) the sentence between the heading and the first bullet must end with a colon; "
        f"got …{claim[-70:]!r}"
    )

    assert 3 <= len(bullets) <= 6, (
        f"(c) expected 3-6 MUST bullets, got {len(bullets)}"
    )
    for _, _, text in bullets:
        assert "MUST" in text, f"(c) a bullet carries no MUST / MUST NOT: {text[:70]!r}"

    long_lines = [ln for ln in lines if len(ln) >= 100]
    assert not long_lines, (
        f"(d) every physical line must stay under 100 chars; {len(long_lines)} do not, "
        f"longest {max(len(x) for x in long_lines)}"
    )

    rat_idx = next((i for i, ln in enumerate(lines) if ln.startswith("Rationale:")), None)
    assert rat_idx is not None, "(f) no paragraph starting with the literal `Rationale:`"
    last_bullet_line = bullets[-1][1]
    between = [i for i in range(last_bullet_line + 1, rat_idx) if lines[i].strip()]
    assert not between, (
        "(e) expected exactly one blank line between the bullets and Rationale:, "
        f"found content on lines {between}"
    )
    assert rat_idx == last_bullet_line + 2, (
        "(e) Rationale: must follow the last bullet after exactly one blank line "
        f"(bullets end at {last_bullet_line}, Rationale: at {rat_idx})"
    )
    rationale = " ".join(ln.strip() for ln in lines[rat_idx:] if ln.strip())
    sentences = [s for s in HOUSE_SENTENCE_SPLIT.split(rationale) if s.strip()]
    assert 1 <= len(sentences) <= 4, (
        f"(f) Rationale: must be 1-4 sentences, got {len(sentences)}"
    )
    assert not re.search(r"\[[A-Z_]{3,}\]", block), (
        "(g) an unresolved bracket placeholder is left in the principle block"
    )


def test_c2_the_principle_block_satisfies_the_house_shape() -> None:
    _check_structure(_principle_block(_read(TEMPLATE)))


# --- C-6: the five content obligations, plus the reference-not-restate pair ---


def test_c6_all_five_content_obligations_are_each_carried_by_their_own_bullet() -> None:
    """C-6: each of the five obligations is covered by a DISTINCT bullet.

    Per-obligation presence is the weaker claim, and a single catch-all bullet could satisfy all
    five at once while the principle still failed to speak about any one of them as a rule. The
    pairing asserted here is obligation-to-bullet, so the check cannot pass by accident.

    An obligation whose marker matches no remaining bullet is reported as UNPLACED and the search
    continues: stopping at the first collision would report the symptom (a later obligation looks
    uncovered) instead of the cause (an earlier marker that is not distinctive).
    """
    block = _principle_block(_read(TEMPLATE))
    bullets = [text for _, _, text in _logical_bullets(block.splitlines())]
    flat_bullets = [_flat(b).lower() for b in bullets]
    remaining = list(range(len(bullets)))
    unplaced = []
    for name, marker, description in CONTENT_OBLIGATIONS:
        hits = [i for i in remaining if _flat(marker).lower() in flat_bullets[i]]
        if not hits:
            unplaced.append(f"{name} ({description}) — marker {marker!r} matches no remaining bullet")
            continue
        remaining.remove(hits[0])
    assert not unplaced, (
        "C-6: the principle does not place each obligation on its own bullet:\n  "
        + "\n  ".join(unplaced)
        + "\nbullets seen: "
        + " | ".join(b[:60] for b in bullets)
    )
    for token in (CEILING_PHRASE, FLOOR_PHRASE):
        assert re.search(rf"\b{token}s?\b", _flat(block), re.I), (
            f"C-6 clause 2: the block never names the {token!r} bound"
        )
    assert re.search(r"suffic", _flat(block), re.I), (
        "C-6 clause 2: the block must state that a satisfied floor is enough to support a change"
    )


def test_c6_points_at_the_runtime_owner_and_states_reference_not_restate() -> None:
    block = _principle_block(_read(TEMPLATE))
    flat = _flat(block)
    assert RUNTIME_OWNER in flat, (
        f"C-6: the block must name the client-facing owner path {RUNTIME_OWNER!r} — a downstream "
        "project has no framework-source tree, so a framework-only pointer is unopenable there"
    )
    assert re.search(r"referenced?,? not restated|reference it, do not restate it|"
                     r"never restate", flat, re.I), (
        "C-6: the block must state that the owner is referenced, not restated"
    )


def test_c6_framework_owner_path_appears_only_as_the_framework_owner() -> None:
    """C-6: [[STR-002]] MAY appear only as the framework's own owner location.

    The decidable form: the framework path must never be the path a reader is sent to, so every
    occurrence has to sit in a logical bullet that also names the framework. A bare "Full
    definition: shared/…" is the downstream-breaking shape this catches.

    The unit is the LOGICAL bullet, not the physical line: every sibling principle in this template
    hard-wraps its bullets, so a line-level check would fail a bullet that is both correct and
    shape-compliant — a false red that teaches the author to reword for the test.
    """
    block = _principle_block(_read(TEMPLATE))
    for index, (_, _, text) in enumerate(_logical_bullets(block.splitlines()), 1):
        if FRAMEWORK_OWNER not in text:
            continue
        assert re.search(r"framework", text, re.I), (
            f"C-6: bullet {index} names the framework-source path {FRAMEWORK_OWNER!r} without "
            f"marking it as the framework's owner location: {text.strip()!r}. A client project "
            "cannot resolve a `shared/` path."
        )
    assert RUNTIME_OWNER in _flat(block), (
        "precondition: the runtime owner path must be present as the reader-facing pointer"
    )


# --- C-7 (template side): every watchlist title is a template title ---


def _carrier_watchlist() -> tuple[str, ...]:
    """Read the watchlist from its owner (the carrier module), never a second copy.

    The carrier owns the enumeration and its counts; this module only reaches the value. Importing
    it keeps a feature from having to edit two lists in step, and keeps a watchlist entry added
    there automatically guarded by C-7's template-side membership here.
    """
    carrier = Path(__file__).resolve().with_name("test_constitution_double_landing.py")
    spec = importlib.util.spec_from_file_location(
        "_constitution_double_landing_carrier", carrier
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return tuple(module.DOUBLE_LANDING_WATCHLIST)


def test_c7_template_side_membership_of_every_watchlist_title() -> None:
    titles = _template_titles(_read(TEMPLATE))
    watchlist = _carrier_watchlist()
    assert watchlist, "the carrier's watchlist is empty — there is nothing to guard"
    absent = [t for t in watchlist if t not in titles]
    assert not absent, (
        f"C-7: watchlist principle(s) {absent} are not template titles. A principle that exists "
        "only in the live constitution is a single-sided landing: no downstream project generated "
        "from the template ever receives it"
    )


def test_c7_mutation_leg_m1_removing_the_block_breaks_membership(tmp_path: Path) -> None:
    """M-1: delete the principle block from a temp COPY; membership must go false.

    The copy is the subject, and the anti-vacuity companion proves the mutation actually took
    effect. The real repository file is asserted untouched afterwards.
    """
    original = _read(TEMPLATE)
    mutant_path = tmp_path / "constitution-template.md"
    mutant_path.write_text(
        re.sub(
            rf"^### [IVXLC0-9]+\. {re.escape(PRINCIPLE_TITLE)}\s*$.*?(?=^### |^## |\Z)",
            "", original, flags=re.M | re.S,
        ),
        encoding="utf-8",
    )
    mutated = _read(mutant_path)
    assert mutated != original, "the mutation did not take effect — this probe would pass vacuously"
    assert PRINCIPLE_TITLE not in _template_titles(mutated), (
        "C-7: deleting the principle block left the title in the title set"
    )
    assert PRINCIPLE_TITLE in _template_titles(_read(TEMPLATE)), (
        "anti-vacuity: the real template must carry the principle"
    )


# --- C-8: gate-budget neutrality ---


def test_c8_principle_block_has_zero_blocking_pattern_hits() -> None:
    blocking_re = _load_scanner().BLOCKING_RE
    hits = []
    for lineno, line in enumerate(_principle_block(_read(TEMPLATE)).splitlines(), 1):
        hits.extend(f"L{lineno}:{m.group(0)!r}" for m in blocking_re.finditer(line))
    assert not hits, (
        f"the principle block trips BLOCKING_RE: {hits}. `constitution-template.md` matches the "
        "scanner's governance-path patterns, so a hit is classified governance_kept — but "
        "governance_kept still counts toward the scan total, and this feature's obligation is zero "
        "NEW hits (T012, T049)"
    )


# --- C-20: the owner's own level-2 headings never appear on a projected surface ---


def _owner_h2_headings() -> tuple[str, ...]:
    """The owner's `##` heading lines, read from the framework source and its mirror.

    C-20 is a "reference, not copy" claim made decidable: copying the owner's body necessarily
    copies its headings, so their absence is the mechanical form of "this surface points rather
    than restates". No prose wording is judged, and no list of forbidden phrases is maintained.
    """
    source = _read(OWNER_SOURCE)
    mirror = _read(OWNER_MIRROR)
    headings = [ln for ln in source.splitlines() if ln.startswith("## ")]
    assert headings, f"the owner {OWNER_SOURCE.relative_to(ROOT)} carries no `##` heading"
    assert source == mirror, (
        "the owner and its runtime mirror must be byte-identical before C-20 can be judged "
        "against both; run `python3 scripts/python/sync-mirrors.py --write`"
    )
    assert [ln for ln in mirror.splitlines() if ln.startswith("## ")] == headings
    return tuple(headings)


@pytest.mark.parametrize("surface", ["constitution-template", "instructions-template"])
def test_c20_no_owner_heading_is_copied_onto_a_projected_surface(surface: str) -> None:
    headings = _owner_h2_headings()
    path = TEMPLATE if surface == "constitution-template" else INSTRUCTIONS_TEMPLATE
    text = _read(path)
    copied = [h for h in headings if h in text]
    assert not copied, (
        f"C-20: {path.relative_to(ROOT)} reproduces the owner's own heading(s) {copied}. The "
        "surface must reference the owner, not carry its body"
    )


# --- C-21: the instructions summary stays within two sentences ---


INSTRUCTIONS_HEADING = f"## {PRINCIPLE_TITLE}"


def _instructions_section() -> str:
    """The instructions section body, heading excluded, up to the next `## ` / `# `."""
    lines = _read(INSTRUCTIONS_TEMPLATE).splitlines()
    try:
        start = lines.index(INSTRUCTIONS_HEADING)
    except ValueError:
        pytest.fail(
            f"{INSTRUCTIONS_TEMPLATE.relative_to(ROOT)} has no {INSTRUCTIONS_HEADING!r} section; "
            "C-21's summary bound cannot be judged until T022 lands it"
        )
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## ") or lines[j].startswith("# "):
            end = j
            break
    return "\n".join(lines[start + 1:end])


def _pointer_lines(body: str) -> list[str]:
    """Lines that are pointers rather than summary prose.

    The bound is on the SUMMARY, so the pointer is removed before counting; otherwise a long path
    would be counted as prose and a correct section would fail. Two shapes count as a pointer:
    the path stands alone on its line, or the line introduces the same path the principle already
    names as the owner location.
    """
    return [
        ln for ln in body.splitlines()
        if RUNTIME_OWNER in ln or FRAMEWORK_OWNER in ln
    ]


def test_c21_instructions_summary_is_at_most_two_sentences() -> None:
    body = _instructions_section()
    summary_lines = [ln for ln in body.splitlines() if ln not in _pointer_lines(body)]
    summary = _flat(" ".join(summary_lines))
    sentences = [s for s in HOUSE_SENTENCE_SPLIT.split(summary) if s.strip()]
    assert len(sentences) <= 2, (
        f"C-21: the summary must be at most two sentences before the pointer, got "
        f"{len(sentences)}: {sentences}"
    )
    assert sentences, "C-21: the section carries no summary at all — a pointer alone is not a summary"
