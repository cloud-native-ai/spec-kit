"""Contract test: the test-execution-efficiency principle lands on both sides, six times.

Implements ``.specify/specs/086-efficient-test-execution/contracts/
principle-landing.contract.md`` **C-039** (both-sides guard) and **C-040** (one in-memory
mutation leg per surface); the owner guideline's own content clauses (C-021…C-024) are
carried by that contract and measured here only through the pointers this guard reads.

The defect this file exists to prevent is the one
``tests/contract/test_constitution_double_landing.py`` was written for, one discipline
later: a rule landed on the surface its author was looking at and nowhere else.

* A principle added to the **live** constitution but not to
  ``templates/constitution-template.md`` never reaches a downstream project.
* An ambient section added to the **template** instructions but never reconciled into the
  **live** instructions leaves this repository running the old rule set.
* An owner guideline no surface points at is a definition point nobody can reach, and a
  surface whose pointer names a file that does not exist is a dangling reference.

Two deliberate design constraints, both inherited:

* **Both sides are asserted in ONE case per surface pair.** Splitting "template has it" and
  "live has it" into two tests lets a one-sided landing pass whenever one of the two is
  skipped, deselected or fails for an unrelated reason. One case, one verdict.
* **Nothing is pinned that an artifact already owns.** The title is matched by set
  membership against the roster and never by numeral (the template says XIX, the live
  constitution says XX, and either can be renumbered); the pointer path, the pointer
  filename and the MUST-include anchor are read from the owner file's own declarations
  where it is reachable, so renaming the discipline to a second name fails here instead of
  drifting quietly.

The mutation leg (C-040) runs on **in-memory doctored copies** — never on the tracked files
— and each leg re-runs the very predicate its case asserts, so a case that could not go red
is caught. Every leg is matched with the anti-vacuity claim that the real text *does* carry
what the mutation removed: a probe whose subject was already absent proves nothing.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]

# --- the six surfaces (C-039) ----------------------------------------------

OWNER = ROOT / "shared" / "guidelines" / "test-execution-efficiency.md"
CONSTITUTION_TEMPLATE = ROOT / "templates" / "constitution-template.md"
CONSTITUTION_LIVE = ROOT / ".specify" / "memory" / "constitution.md"
INSTRUCTIONS_TEMPLATE = ROOT / "templates" / "instructions-template.md"
INSTRUCTIONS_LIVE = ROOT / ".specify" / "instructions.md"
CONSTITUTION_SKILL = ROOT / "skills" / "internal" / "manage-constitution" / "SKILL.md"

# [[STR-001]] / [[STR-003]] — the literals every surface points with.
#
# Two forms of the same name, deliberately: the constitution rosters and the generator's
# MUST-include list carry the principle title, while the ambient instructions sections are
# headed `## Test Execution Efficiency (测试执行效率)` — the framework's own section-naming
# form, and the form C-030 fixes. A surface satisfies this guard by carrying EITHER form;
# requiring one of the two on every surface would be a pin the artifacts do not hold. What
# is asserted of every surface is the POINTER (the file it must name), which is the
# reachability property the one-source-of-truth discipline is actually about.
TITLE = "Efficient Test Execution (Concurrent by Default)"
AMBIENT_NAME = "Test Execution Efficiency (测试执行效率)"
TITLE_FORMS = (TITLE, AMBIENT_NAME)

# The runtime pointer the instructions surfaces carry (they are copied into client projects,
# which have no framework-source tree) and the framework pointer the constitution and the
# generator surfaces carry. Both name the same file; the owner is that file.
POINTER_PATH = "shared/guidelines/test-execution-efficiency.md"
RUNTIME_POINTER_PATH = ".specify/shared/guidelines/test-execution-efficiency.md"
POINTER_FILENAME = "test-execution-efficiency.md"   # [[STR-001]]

# The sibling section the ambient section MUST follow (C-030).
PRECEDING_SECTION = "## Single-Run Evidence Discipline"
AMBIENT_HEADING = f"## {AMBIENT_NAME}"
# The owner's `##` headings, which no pointer surface may reproduce (C-028/C-031/C-039's
# "pointer shape, not content shape"). Derived from the owner, never listed here.

ROSTER_HEADING_RE = re.compile(r"^### ([IVXLC0-9]+)\. (.+)$", re.M)
SKILL_ENTRY_RE = re.compile(r"^  - \*\*(.+?)\*\* —", re.M)

# --- the owner's normative content (what no other surface may reproduce) ----
#
# C-039's last conjunct: "no surface other than the owner contains the owner's decision
# table". The decision table is the owner's own `|`-table rows; a shared row between the
# owner and another surface is the content-copy shape C-028 and C-031 forbid. Rows are
# compared as normalized cell tuples so re-aligning the columns is not a difference.


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _flat(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def _roster_titles(text: str) -> set[str]:
    """Principle titles of a constitution roster. Numeral-agnostic by construction."""
    return {m.group(2).strip() for m in ROSTER_HEADING_RE.finditer(text)}


def _skill_entry_names(text: str) -> set[str]:
    """Titles in the generator's `- **MUST include**` block, extracted from the
    uniform `  - **<Title>** — …` sub-entry form (never by substring containment)."""
    lines = text.splitlines()
    start = next((i for i, ln in enumerate(lines) if ln.startswith("- **MUST include**")), None)
    assert start is not None, (
        "manage-constitution/SKILL.md lost its `- **MUST include**` mandatory-principles block"
    )
    block = [lines[start]]
    for ln in lines[start + 1:]:
        if ln.startswith("- "):
            break
        block.append(ln)
    return {m.group(1).strip() for m in SKILL_ENTRY_RE.finditer("\n".join(block))}


def _section_body(text: str, heading: str) -> str | None:
    """Body of a top-level `##` section, heading excluded; `None` when absent.

    Returning `None` rather than raising is load-bearing for the mutation legs: the leg has
    to observe the *absence* it manufactured, and an exception would be indistinguishable
    from a broken helper.
    """
    lines = text.splitlines()
    if heading not in lines:
        return None
    start = lines.index(heading)
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## ") or lines[j].startswith("# "):
            end = j
            break
    return "\n".join(lines[start + 1:end])


def _principle_block(text: str, title: str) -> str | None:
    """One principle's block: heading line plus body up to the next heading; `None` if absent."""
    m = re.search(
        rf"^### [IVXLC0-9]+\. {re.escape(title)}\s*$(.*?)(?=^### |^## |\Z)",
        text, re.M | re.S,
    )
    return m.group(0) if m else None


def _skill_entry_block(text: str, title: str) -> str | None:
    m = re.search(
        rf"^  - \*\*{re.escape(title)}\*\* —.*?(?=^  - \*\*|^- |\Z)", text, re.M | re.S
    )
    return m.group(0) if m else None


def _owner_decision_rows(text: str) -> set[tuple[str, ...]]:
    """The owner's decision-table rows as normalized cell tuples.

    The separator row (`|---|---|`) is excluded: cells that are all dashes carry no decision.
    The header row is kept — a copied table brings its header with it, and comparing cells
    (not prose) keeps the predicate decidable without judging wording.
    """
    rows: set[tuple[str, ...]] = set()
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = tuple(c.strip() for c in stripped.strip("|").split("|"))
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
            continue
        rows.add(cells)
    return rows


def _table_rows(text: str) -> set[tuple[str, ...]]:
    return _owner_decision_rows(text)


def _owner_h2_headings(text: str) -> set[str]:
    return {ln.strip() for ln in text.splitlines() if ln.startswith("## ")}


# --- per-surface predicates (the mutation legs reuse exactly these) ---------
#
# Each predicate answers one question for one surface and takes the surface TEXT (not a
# path) so the mutation leg can call it on a doctored copy. Each returns a list of
# violations; empty means the surface is clean.


def _owner_violations(text: str) -> list[str]:
    """The owner's own half: it must exist, declare itself, and name its title and file."""
    out = []
    if not any(form in text for form in TITLE_FORMS):
        out.append(f"the owner carries neither title form {TITLE_FORMS}")
    flat = _flat(text)
    # C-021: the owner declares itself the single definition point.
    if not re.search(r"唯一真源|唯一.*定义|single source of truth|single owner", flat, re.I):
        out.append("the owner does not declare itself the single definition point")
    # C-022: its six required sections, counted by `##` heading (six plus the boundary,
    # scope and evidence sections the contract also requires).
    h2 = _owner_h2_headings(text)
    if len(h2) < 6:
        out.append(f"the owner carries {len(h2)} `##` sections; the contract requires six")
    # C-023: the boundary with the pre-existing test-quality rules.
    if not any("边界" in h or "boundar" in h.lower() for h in h2):
        out.append("the owner carries no section stating its boundary with sibling disciplines")
    # C-024: no new machinery.
    if not re.search(r"MUST NOT", flat):
        out.append("the owner states no MUST NOT, so the no-new-machinery limit is unstated")
    return out


def _constitution_violations(text: str, owner_headings: set[str]) -> list[str]:
    """A roster must carry the principle, with a pointer — never the owner's own headings."""
    out = []
    if TITLE not in _roster_titles(text):
        return [f"the roster carries no principle titled {TITLE!r}"]
    block = _principle_block(text, TITLE)
    if block is None:
        return ["the title matched but its principle block could not be extracted"]
    if POINTER_PATH not in _flat(block):
        out.append(f"the principle block does not carry the pointer path {POINTER_PATH!r}")
    copied = sorted(h for h in owner_headings if h in block)
    if copied:
        out.append(f"the principle block reproduces the owner's heading(s) {copied}")
    return out


def _instructions_violations(text: str, owner_headings: set[str]) -> list[str]:
    """An instruction surface must carry the ambient section, with a runtime pointer."""
    out = []
    body = _section_body(text, AMBIENT_HEADING)
    if body is None:
        return [f"the surface carries no {AMBIENT_HEADING!r} section"]
    if RUNTIME_POINTER_PATH not in _flat(body):
        out.append(f"the section does not carry the runtime pointer {RUNTIME_POINTER_PATH!r}")
    copied = sorted(h for h in owner_headings if h in body.splitlines() or h in body)
    if copied:
        out.append(f"the section reproduces the owner's heading(s) {copied}")
    return out


def _skill_violations(text: str) -> list[str]:
    """The generator's MUST-include list must instruct the principle, by pointer."""
    out = []
    if TITLE not in _skill_entry_names(text):
        return [f"the MUST-include list carries no entry titled {TITLE!r}"]
    block = _skill_entry_block(text, TITLE)
    if block is None:
        return ["the entry name matched but its block could not be extracted"]
    flat = _flat(block)
    if POINTER_PATH not in flat:
        out.append(f"the entry does not carry the pointer path {POINTER_PATH!r}")
    if not re.search(r"MUST NOT justify|not machinery", flat):
        out.append("the entry does not carry the no-new-machinery obligation")
    return out


def _copy_violations(text: str, owner_rows: set[tuple[str, ...]]) -> list[str]:
    """A non-owner surface may not reproduce the owner's decision table (C-028/C-039)."""
    shared = _table_rows(text) & owner_rows
    return [f"reproduces the owner's decision-table row {row}" for row in sorted(shared)]


# --- the six surfaces, as (id, path, text, predicate) ---------------------


def _surfaces() -> list[tuple[str, Path, str, object]]:
    """The six surfaces C-039 enumerates, each with a predicate over that surface's text."""
    owner_text = _text(OWNER)
    owner_headings = _owner_h2_headings(owner_text)
    rows = _owner_decision_rows(owner_text)
    assert owner_headings, "the owner carries no `##` heading, so 'no copy' has no referent"

    def constitution(t: str) -> list[str]:
        return _constitution_violations(t, owner_headings) + _copy_violations(t, rows)

    def instructions(t: str) -> list[str]:
        return _instructions_violations(t, owner_headings) + _copy_violations(t, rows)

    def skill(t: str) -> list[str]:
        return _skill_violations(t) + _copy_violations(t, rows)

    return [
        ("owner", OWNER, owner_text, _owner_violations),
        ("constitution_template", CONSTITUTION_TEMPLATE, _text(CONSTITUTION_TEMPLATE),
         constitution),
        ("constitution_live", CONSTITUTION_LIVE, _text(CONSTITUTION_LIVE), constitution),
        ("instructions_template", INSTRUCTIONS_TEMPLATE, _text(INSTRUCTIONS_TEMPLATE),
         instructions),
        ("instructions_live", INSTRUCTIONS_LIVE, _text(INSTRUCTIONS_LIVE), instructions),
        ("generator_list", CONSTITUTION_SKILL, _text(CONSTITUTION_SKILL), skill),
    ]


# --- C-039: one case asserting all six surfaces ----------------------------


def test_c39_the_principle_lands_on_all_six_surfaces():
    """C-039: every surface carries the title/pointer, and the owner file exists.

    One case, not six: a one-sided landing has to be impossible to miss, and "skip the
    template half and keep the live half" is exactly how a single-sided landing survives.
    """
    assert OWNER.is_file(), (
        f"the owner guideline {OWNER.relative_to(ROOT)} does not exist; every pointer this "
        "guard accepts would be dangling"
    )
    assert POINTER_PATH == str(OWNER.relative_to(ROOT)), (
        "this guard's pointer literal no longer names the owner file: the pin and the artifact "
        f"diverged ({POINTER_PATH!r} vs {str(OWNER.relative_to(ROOT))!r})"
    )
    failures = {}
    for surface, path, body, predicate in _surfaces():
        violations = predicate(body)
        if violations:
            failures[surface] = (str(path.relative_to(ROOT)), violations)
    assert not failures, (
        "the principle did not land on every surface, or landed one-sidedly: "
        + "; ".join(f"{s} ({w}): {v}" for s, (w, v) in sorted(failures.items()))
    )


def test_c39_the_six_surfaces_are_distinct_files():
    """Anti-vacuity for C-039: six surfaces, six paths.

    A mapping that accidentally named one file twice would make the six assertions above
    two assertions repeated six times.
    """
    paths = [str(p.relative_to(ROOT)) for p in (
        OWNER, CONSTITUTION_TEMPLATE, CONSTITUTION_LIVE,
        INSTRUCTIONS_TEMPLATE, INSTRUCTIONS_LIVE, CONSTITUTION_SKILL,
    )]
    assert len(set(paths)) == 6, f"the guard's surface list repeats a file: {paths}"
    missing = [p for p in paths if not (ROOT / p).is_file()]
    assert not missing, f"surface file(s) missing: {missing}"


def test_c39_no_non_owner_surface_reproduces_the_owner_decision_table():
    """C-039's last conjunct, stated once on its own so a copy is read as a copy.

    The sweep covers every non-owner surface: a single shared decision row is a second
    definition point, and the copy-vs-pointer distinction is the whole point of the owner.
    """
    owner_rows = _owner_decision_rows(_text(OWNER))
    assert len(owner_rows) >= 4, (
        f"the owner's decision table holds {len(owner_rows)} rows; a table this guard cannot "
        "see makes every copy assertion below vacuously true"
    )
    offenders = {}
    for surface, path, body, _predicate in _surfaces()[1:]:
        shared = _table_rows(body) & owner_rows
        if shared:
            offenders[surface] = (str(path.relative_to(ROOT)), sorted(shared))
    assert not offenders, (
        "a non-owner surface reproduces the owner's decision table instead of pointing at it: "
        f"{offenders}"
    )


def test_c39_ambient_section_sits_immediately_after_its_sibling():
    """C-030's positional half, on both instruction surfaces.

    The section's *content* is the section-propagation guard's business; what is asserted
    here is the placement the contract fixes, on both surfaces, because the template alone
    being right is a one-sided landing.
    """
    for path in (INSTRUCTIONS_TEMPLATE, INSTRUCTIONS_LIVE):
        lines = _text(path).splitlines()
        rel = path.relative_to(ROOT)
        assert AMBIENT_HEADING in lines, f"{rel} carries no {AMBIENT_HEADING!r} section"
        assert PRECEDING_SECTION in lines, f"{rel} lost its {PRECEDING_SECTION!r} section"
        i = lines.index(PRECEDING_SECTION)
        nxt = next((ln for ln in lines[i + 1:] if ln.startswith("## ")), None)
        assert nxt == AMBIENT_HEADING, (
            f"{rel}: the section immediately after {PRECEDING_SECTION!r} is {nxt!r}, not "
            f"{AMBIENT_HEADING!r} — the placement C-030 fixes must hold on both surfaces"
        )


def test_c39_the_pointer_forms_are_the_sibling_forms():
    """The runtime-pointer form is not invented for this section.

    Each instruction surface already carries the `.specify/shared/guidelines/<name>` form
    for its sibling disciplines; a section that reaches its owner by a form no sibling uses
    is a pointer a future reader cannot pattern-match.
    """
    for path in (INSTRUCTIONS_TEMPLATE, INSTRUCTIONS_LIVE):
        body = _section_body(_text(path), AMBIENT_HEADING)
        rel = path.relative_to(ROOT)
        assert body is not None, f"{rel}: no {AMBIENT_HEADING!r} section"
        assert RUNTIME_POINTER_PATH in _flat(body), (
            f"{rel}: the section does not carry {RUNTIME_POINTER_PATH!r}"
        )
        sibling = _section_body(_text(path), PRECEDING_SECTION) or ""
        sibling_pointers = set(re.findall(r"\.specify/shared/guidelines/[\w.-]+\.md", sibling))
        assert sibling_pointers, (
            f"{rel}: the sibling section {PRECEDING_SECTION!r} carries no runtime pointer, so "
            "there is no form to compare against"
        )
        mine = set(re.findall(r"\.specify/shared/guidelines/[\w.-]+\.md", body))
        assert mine, f"{rel}: the new section carries no runtime pointer at all"
        prefix = {p.rsplit("/", 1)[0] for p in sibling_pointers}
        assert {p.rsplit("/", 1)[0] for p in mine} <= prefix, (
            f"{rel}: the new section points through a different root than its siblings "
            f"({sorted(mine)} vs {sorted(sibling_pointers)})"
        )


# --- C-040: one mutation leg per surface, in memory, never on disk ---------

MUTATIONS = {
    "owner": (_owner_violations),
    "constitution_template": None,   # bound in _predicates() once the owner is read
    "constitution_live": None,
    "instructions_template": None,
    "instructions_live": None,
    "generator_list": (_skill_violations),
}


def _predicates() -> dict:
    """The {surface: predicate} map the mutation legs run, built from one owner read."""
    owner_text = _text(OWNER)
    headings = _owner_h2_headings(owner_text)
    rows = _owner_decision_rows(owner_text)

    def constitution(t: str) -> list[str]:
        return _constitution_violations(t, headings) + _copy_violations(t, rows)

    def instructions(t: str) -> list[str]:
        return _instructions_violations(t, headings) + _copy_violations(t, rows)

    return {
        "owner": _owner_violations,
        "constitution_template": constitution,
        "constitution_live": constitution,
        "instructions_template": instructions,
        "instructions_live": instructions,
        "generator_list": _skill_violations,
    }


def _doctored_copy(surface: str, text: str) -> str:
    """Remove this surface's carrier of the discipline, in memory.

    Deliberately blunt — the whole section / principle block / entry block is dropped, the
    shape a one-sided landing takes when a surface is regenerated from an older source. The
    leg's job is to prove the predicate notices, not to model one edit style.
    """
    if surface == "owner":
        doctored = text
        for form in TITLE_FORMS:
            doctored = doctored.replace(form, "")
        return doctored
    if surface in ("constitution_template", "constitution_live"):
        block = _principle_block(text, TITLE)
        assert block is not None, f"{surface}: nothing to mutate"
        return text.replace(block, "")
    if surface in ("instructions_template", "instructions_live"):
        lines = text.splitlines()
        start = lines.index(AMBIENT_HEADING)
        end = len(lines)
        for j in range(start + 1, len(lines)):
            if lines[j].startswith("## ") or lines[j].startswith("# "):
                end = j
                break
        return "\n".join(lines[:start] + lines[end:])
    block = _skill_entry_block(text, TITLE)
    assert block is not None, f"{surface}: nothing to mutate"
    return text.replace(block, "")


@pytest.mark.parametrize("surface", sorted(MUTATIONS))
def test_c40_each_surface_goes_red_when_its_carrier_is_removed(surface):
    """C-040: deleting the carrier from one surface fails that surface's case.

    The mutation is exercised on an in-memory copy; the tracked files are read, never
    written. Both halves of the matched pair are asserted: the doctored copy MUST produce
    violations **and** the real text MUST be clean — a probe whose real half was already
    red would prove nothing about the guard.
    """
    path = {
        "owner": OWNER,
        "constitution_template": CONSTITUTION_TEMPLATE,
        "constitution_live": CONSTITUTION_LIVE,
        "instructions_template": INSTRUCTIONS_TEMPLATE,
        "instructions_live": INSTRUCTIONS_LIVE,
        "generator_list": CONSTITUTION_SKILL,
    }[surface]
    predicate = _predicates()[surface]
    real = _text(path)
    assert predicate(real) == [], (
        f"{surface}: the real surface is already non-compliant, so the mutation leg proves "
        f"nothing: {predicate(real)}"
    )

    doctored = _doctored_copy(surface, real)
    assert doctored != real, f"{surface}: the mutation changed nothing"
    violations = predicate(doctored)
    assert violations, (
        f"{surface}: removing the carrier left the predicate green — this surface's case could "
        "not go red, which is exactly the blind check C-040 forbids"
    )
    # The copy is in memory only: re-read the tracked file and confirm it is still clean.
    assert predicate(_text(path)) == [], (
        f"{surface}: the mutation leg wrote to the tracked file instead of a copy"
    )


def test_c40_no_mutation_leg_touches_the_tracked_files():
    """C-040's boundary, asserted once: the guard reads six files and writes none.

    A mutation leg that edited the real surface would turn this suite into a test that
    repairs the defect it is meant to report.
    """
    paths = {
        "owner": OWNER,
        "constitution_template": CONSTITUTION_TEMPLATE,
        "constitution_live": CONSTITUTION_LIVE,
        "instructions_template": INSTRUCTIONS_TEMPLATE,
        "instructions_live": INSTRUCTIONS_LIVE,
        "generator_list": CONSTITUTION_SKILL,
    }
    before = {name: _text(path) for name, path in paths.items()}
    for surface in sorted(paths):
        _doctored_copy(surface, before[surface])
    after = {name: _text(path) for name, path in paths.items()}
    assert after == before, (
        "a mutation leg modified a tracked surface: "
        f"{[n for n in before if before[n] != after[n]]}"
    )
