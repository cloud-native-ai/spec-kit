"""Contract test: ambient-section — delivery of the User-Facing Comprehension section.

Implements ``.specify/specs/051-user-facing-comprehension/contracts/ambient-section.md``
clauses **C-1…C-11**. ``test_cN_*`` maps one-to-one onto that file's C-N.

Two deliberate design choices, both driven by Constitution Principle XIV (one owner per
fact):

* **C-6's forbidden list is derived, not pinned.** The seven section names the ambient body
  must not inline are owned by ``contracts/discipline-doc.md`` C-6 and asserted there.
  Restating the tuple here would create a second copy that silently goes vacuous the day a
  section is renamed — it would keep forbidding names that no longer exist. This file reads
  the truth document's own H2 headings instead, so the forbidden set always tracks reality.
* **C-3 asserts the heading only.** The live ``.specify/instructions.md`` may legitimately
  carry project-specific sections the template lacks, so the direction is template ⊆ live.
  The whole-of-template ⊆ live assertion already exists and is owned by
  ``test_instructions_section_propagation.py::test_c1_live_instructions_carry_all_template_sections``;
  duplicating it here would be a copy of another test's fact.

Reading C-11: the pointer-existence half is green before this feature lands (every pointer
that exists today resolves), and C-11(b)'s subset semantics keeps it green afterwards —
adding the new pointer shrinks nothing, deleting any existing pointer grows the remainder
past the three named files and fails. That is the point of subset rather than equality.

Pin hygiene: no file count is hard-coded as an expected population; the anti-vacuity guards
assert that named files exist rather than that a directory holds N entries.
"""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "templates" / "instructions-template.md"
MIRROR = ROOT / ".specify" / "templates" / "instructions-template.md"
LIVE = ROOT / ".specify" / "instructions.md"
GUIDELINES = ROOT / "shared" / "guidelines"
DOC = GUIDELINES / "user-facing-comprehension.md"
SCANNER = ROOT / "scripts" / "python" / "scan-confirmation-gates.py"

HEADING = "## User-Facing Comprehension"                             # STR-004
POINTER = ".specify/shared/guidelines/user-facing-comprehension.md"   # STR-001

# C-8: the new section's neighbours.
PREV_HEADING = "## Token Efficiency Discipline"
NEXT_HEADING = "## Dogfooding Practice"

# C-7: the window pinned by test_proactive_trigger_section.py:141-152 and
# test_ask_record_repeat.py:220-227. These three must stay consecutive and in this order.
PINNED_WINDOW = (
    "## Documentation Map",
    "## Proactive Flow Trigger",
    "## Fact, Correctness & Logic Checks (Input Sanity)",
)

# C-9: shipped surfaces stay project-neutral.
FORBIDDEN_NAMES = ("spec-kit", "specify-cli", "specify_cli", "cloud-native-ai")

# C-5: engine surface that must not leak into a reader-facing section.
PARAM_PATTERNS = (r"--[a-z][a-z0-9-]*", r"\$ARGUMENTS", r"<[a-z-]+>")

# C-11: every pointer to a guideline on either instruction surface.
GUIDELINE_POINTER_RE = re.compile(r"shared/guidelines/([A-Za-z0-9._-]+\.md)")

# C-11(b): the three guidelines no instruction surface points at, so no pointer to them can
# dangle. Subset semantics — a fourth name in the remainder means a pointer was removed.
UNPOINTED_BY_STRUCTURE = (
    "checklist-methodology.md",
    "requirements-guidelines.md",
    "self-improvement.md",
)


def _text(path: Path) -> str:
    """Read a file, letting a missing artifact surface as FileNotFoundError.

    Unguarded on purpose: at red-first time (T005) the failure reason must read as
    "artifact missing", not as an assertion that was written wrong.
    """
    return path.read_text(encoding="utf-8")


def _h2(text: str) -> list[str]:
    return re.findall(r"(?m)^## .+$", text)


def _section(text: str, heading: str = HEADING) -> str:
    """Section body (heading excluded), up to the next ``## `` or ``# ``."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == heading:
            start = i
            break
    assert start is not None, f"section heading {heading!r} not found"
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## ") or lines[j].startswith("# "):
            end = j
            break
    return "\n".join(lines[start + 1 : end])


def _load_scanner():
    spec = importlib.util.spec_from_file_location("_scan_gates_ambient", SCANNER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --- uniqueness and mirrors ---


def test_c1_template_carries_the_section_exactly_once_with_its_pointer():
    text = _text(TEMPLATE)
    count = len(re.findall(rf"(?m)^{re.escape(HEADING)}\s*$", text))
    assert count == 1, f"{HEADING!r} must appear exactly once in the template, got {count}"
    assert POINTER in _section(text), (
        f"the section body must carry the STR-001 pointer {POINTER!r}"
    )


def test_c2_mirror_carries_the_section_and_is_byte_identical():
    mirror = _text(MIRROR)
    count = len(re.findall(rf"(?m)^{re.escape(HEADING)}\s*$", mirror))
    assert count == 1, f"{HEADING!r} must appear exactly once in the mirror, got {count}"
    assert POINTER in _section(mirror), (
        f"the mirrored section body must carry the STR-001 pointer {POINTER!r}"
    )
    assert TEMPLATE.read_bytes() == MIRROR.read_bytes(), (
        "templates/instructions-template.md and its .specify/ mirror diverged "
        "(run scripts/python/sync-mirrors.py --write templates)"
    )


def test_c3_live_instructions_carry_the_heading_verbatim():
    live = _text(LIVE)
    count = len(re.findall(rf"(?m)^{re.escape(HEADING)}\s*$", live))
    assert count == 1, (
        f"{HEADING!r} must appear exactly once in the live instructions file, got {count} "
        "(run scripts/bash/generate-instructions.sh to reconcile)"
    )


# --- the body constrains itself ---


def test_c4_body_within_25_lines_and_no_subheadings():
    lines = _section(_text(TEMPLATE)).splitlines()
    assert len(lines) <= 25, f"section body must be <= 25 lines, got {len(lines)}"
    assert not any(line.startswith("### ") for line in lines), (
        "no `### ` subheadings: additive reconcile does not propagate them, so content "
        "hidden in a subsection never reaches already-initialized projects"
    )


def test_c5_body_exposes_no_command_or_parameter_surface():
    body = _section(_text(TEMPLATE))
    assert body.count("/speckit.") == 0, (
        "the section must not name command forms — its own subject is not exposing the "
        "engine surface to readers, so it must comply first"
    )
    hits = []
    for pattern in PARAM_PATTERNS:
        hits.extend(m.group(0) for m in re.finditer(pattern, body))
    assert not hits, f"parameter forms must not appear in the section body: {hits}"


def test_c6_body_does_not_inline_the_truth_doc_section_names():
    doc_sections = _h2(_text(DOC))
    assert len(doc_sections) >= 7, (
        "the truth document's H2 roster is the source of this clause's forbidden set; "
        f"expected at least the seven names discipline-doc C-6 pins, got {doc_sections}"
    )
    body = _section(_text(TEMPLATE))
    inlined = [name.lstrip("# ").strip() for name in doc_sections
               if name.lstrip("# ").strip() in body]
    assert not inlined, (
        "the ambient body inlines section names owned by the truth document — a reader "
        "intending to act on it must still have to open the owner "
        f"(ask-record-repeat.md:97): {inlined}"
    )


# --- position window ---


def test_c7_pinned_position_window_is_undisturbed():
    headings = _h2(_text(TEMPLATE))
    for pinned in PINNED_WINDOW:
        assert pinned in headings, f"pinned window heading {pinned!r} gone from the template"
    idx = [headings.index(h) for h in PINNED_WINDOW]
    assert idx == [idx[0], idx[0] + 1, idx[0] + 2], (
        f"the three pinned sections must stay consecutive and in order; got {idx} in {headings}"
    )
    if HEADING in headings:
        assert not idx[0] <= headings.index(HEADING) <= idx[2], (
            f"{HEADING!r} must not be inserted inside the pinned window {PINNED_WINDOW}"
        )


def test_c8_section_sits_after_token_efficiency_and_before_dogfooding():
    headings = _h2(_text(TEMPLATE))
    for anchor in (PREV_HEADING, NEXT_HEADING):
        assert anchor in headings, f"anchor {anchor!r} gone from the template"
    assert HEADING in headings, f"{HEADING!r} missing"
    i_prev = headings.index(PREV_HEADING)
    i_new = headings.index(HEADING)
    i_next = headings.index(NEXT_HEADING)
    assert i_prev < i_new < i_next, (
        f"{HEADING!r} must sit between {PREV_HEADING!r} and {NEXT_HEADING!r}; "
        f"got indices {i_prev}, {i_new}, {i_next} in {headings}"
    )


# --- neutrality and budget ---


def test_c9_body_is_project_neutral():
    low = _section(_text(TEMPLATE)).lower()
    for token in FORBIDDEN_NAMES:
        assert token.lower() not in low, f"project token {token!r} leaked into the section body"


def test_c10_body_has_zero_blocking_pattern_hits():
    blocking_re = _load_scanner().BLOCKING_RE
    body = _section(_text(TEMPLATE))
    hits = []
    for lineno, line in enumerate(body.splitlines(), 1):
        hits.extend(f"L{lineno}:{m.group(0)!r}" for m in blocking_re.finditer(line))
    assert not hits, (
        "the section trips BLOCKING_PATTERNS and the gate-budget integer headroom is 0 "
        f"(scan total is pinned at 23 by equality): {hits}"
    )


# --- dangling-pointer guard (FR-038) ---


def test_c11_no_dangling_guideline_pointer_on_either_instruction_surface():
    surfaces = (("template", TEMPLATE), ("live", LIVE))
    pointed: set[str] = set()
    for label, path in surfaces:
        names = set(GUIDELINE_POINTER_RE.findall(_text(path)))
        assert names, f"the {label} instruction surface carries no guideline pointer at all"
        pointed |= names

    dangling = sorted(n for n in pointed if not (GUIDELINES / n).is_file())
    assert not dangling, (
        "instruction surfaces point at guidelines that do not exist — the delivery window "
        f"is open and nothing warns the reader (FR-038 / SC-017): {dangling}"
    )

    # C-11(b): the remainder must not grow past the three structurally unpointed files.
    # Anti-vacuity: name the three and require them to exist, so an empty guidelines
    # directory cannot make the subset assertion pass on nothing.
    for name in UNPOINTED_BY_STRUCTURE:
        assert (GUIDELINES / name).is_file(), (
            f"C-11(b) names {name} as unpointed-by-structure but it is not in shared/guidelines/"
        )
    full = {p.name for p in GUIDELINES.glob("*.md")}
    remainder = full - pointed
    unexpected = sorted(remainder - set(UNPOINTED_BY_STRUCTURE))
    assert not unexpected, (
        "a guideline lost its instruction-surface pointer, so it can no longer dangle "
        "loudly — coverage shrank silently. Either restore the pointer or amend "
        f"ambient-section.md C-11(b) with a recorded reason: {unexpected}"
    )
