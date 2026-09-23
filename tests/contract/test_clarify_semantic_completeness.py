"""Contract tests: clarify Mode A's semantic-completeness surface.

Subject: ``shared/constants/clarify-taxonomy.md`` § Mode A, driven by the confirmed
introspection finding F-07 (``.specify/memory/feedback/introspection/``). Mode A's
mechanical verification asserted an ID *set* and a ``- Q:`` row count; neither reads
the artifact's Assumptions, and neither notices that a renumbering falsified a derived
count in the quality checklist. Three obligations close that:

* **C-1…C-3** — a 12th taxonomy category, ``Deferred-by-assumption``, that separates a
  decision already taken from a choice still open. C-3 pins its *discriminability* with
  positive and negative sample wordings: a category that fires on everything, or on
  nothing, is not a category.
* **C-4** — a document-order invariant beside the append-only invariant, adjudicated by
  an ``ORDER BREAK`` line rather than by re-reading the artifact.
* **C-5** — a derived-count revisit of ``checklists/requirements.md`` after any FR/SC
  addition, removal, or renumbering.
* **C-6** — the four surfaces this change writes add no blocking-gate wording, against a
  confirmation-gate budget with zero integer headroom.

The machine implementation of C-4 is deliberately **not** built here: the report assigns
it to the deterministic requirements validator, a separately scheduled feature, so this
file pins the obligation text and the interim extraction the owner document carries.

Pin hygiene: every zero-hit assertion carries a non-empty companion, so a needle that
stopped matching fails loudly instead of passing vacuously.
"""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
TAXONOMY = ROOT / "shared" / "constants" / "clarify-taxonomy.md"
SCANNER = ROOT / "scripts" / "python" / "scan-confirmation-gates.py"

# The four framework sources this change writes. All four are inside the gate
# scanner's scope (SCAN_DIRS covers `shared` and `templates/commands`).
#
# Split into two rosters because the proposition differs per file — the same split
# test_fast_fail_discipline.py's G-4 makes: "the lines this change adds are zero-hit",
# not "every file it touches is hit-free". Three of the four carry no gate at all, so
# their guard is whole-file. glossary.md carries one pre-existing destructive gate
# (§4's user-entry overwrite, `--confirmed-resolution`), so demanding a hit-free file
# there would force "fixing" correct pre-existing work to satisfy a wrong assertion;
# its guard is scoped to the lines this change adds.
ZERO_HIT_SURFACES = (
    "shared/constants/clarify-taxonomy.md",
    "shared/workflow/user-input-protocol.md",
    "templates/commands/requirements.md",
)
GATE_CARRYING_SURFACE = "shared/workflow/glossary.md"
# Region anchors: this change adds one wrapped bullet to §1, so marker-line scoping would
# examine two physical lines out of fifteen. The region runs from the bullet's lead to the
# next numbered heading.
GATE_CARRYING_REGION = ("- **Constraint-side reading", "\n## 2.")
# The pre-existing gate that scoping keeps out of the proposition — pinned so the
# scoping cannot silently absorb a second one.
PREEXISTING_GATE_FRAGMENT = "explicit user confirmation"

NEW_CATEGORY = "Deferred-by-assumption"

# The eleven pre-existing Mode A categories, pinned by name so that "12 categories"
# cannot be reached by dropping one and adding two.
PREEXISTING_CATEGORIES = (
    "Feature Linkage",
    "Functional Scope & Behavior",
    "Domain & Data Model",
    "Interaction & UX Flow",
    "Non-Functional Quality Attributes",
    "Integration & External Dependencies",
    "Edge Cases & Failure Handling",
    "Constraints & Tradeoffs",
    "Terminology & Consistency",
    "Completion Signals",
    "Misc / Placeholders",
)

# The three hit conditions, by a literal fragment of each as the owner words them.
HIT_CONDITION_LITERALS = (
    "named alternatives",
    "names a later phase or artifact as the decision-maker",
    "conditional escalation clause",
)

# Discriminability patterns: one per hit condition, keyed to the *wording shape* the
# owner names rather than to any single example. Derived from HIT_CONDITION_LITERALS
# one-for-one, in the same order.
HIT_PATTERNS = (
    # (a) named alternatives, one adopted tentatively rather than decided
    re.compile(
        r"(?:alternatives?|options?|candidates?)[^\n]{0,120}"
        r"(?:assum\w+|tentative|provisional|for now|interim)"
        r"|(?:assum\w+|tentative|provisional|for now|interim)[^\n]{0,120}"
        r"(?:alternatives?|options?|candidates?)",
        re.I,
    ),
    # (b) a later phase / artifact nominated as the decision-maker
    re.compile(
        r"(?:plan|tasks|implement\w*|design time|/speckit\.\w+)[^\n]{0,60}"
        r"(?:decid\w+|resolv\w+|settled?|determined|chosen)"
        r"|(?:decid\w+|resolv\w+|settled?)[^\n]{0,60}"
        r"\b(?:in|at|by|during)\s+(?:the\s+)?(?:plan|tasks|implement\w*|design)\b",
        re.I,
    ),
    # (c) an if-then escalation / re-open clause
    re.compile(
        r"\bif\b[^\n]{0,120}(?:revisit|re-open|reopen|escalat\w+)",
        re.I,
    ),
)

# Assumption wordings the category MUST mark Partial/Missing (a choice still open).
POSITIVE_SAMPLES = (
    "Assumption: the export format is JSON; YAML and CSV were the alternatives. "
    "Provisional until the plan phase decides.",
    "Assumption: the retry policy is 3 attempts; if the measured p99 turns out to "
    "exceed 2s, revisit this bound.",
    "Assumption: single-region deployment is assumed for now; the multi-region option "
    "stays open and is resolved at design time.",
)

# Assumption wordings the category MUST leave Clear (a value fixed, no competing
# alternative named, no later phase nominated, no escalation clause).
NEGATIVE_SAMPLES = (
    "Assumption: the deployment target is a single region.",
    "Assumption: all identifiers are UTF-8 encoded.",
    "Assumption: audit log retention is 90 days, matching the compliance baseline.",
)


def _text(path: Path) -> str:
    """Unguarded read: a missing artifact must surface as FileNotFoundError, not an assert."""
    return path.read_text(encoding="utf-8")


def _mode_a(text: str) -> str:
    m = re.search(r"^## Mode A:.*?$(.*?)(?=^## |\Z)", text, re.M | re.S)
    assert m, "Mode A section missing from clarify-taxonomy.md"
    return m.group(1)


def _scan_section(mode_a: str) -> str:
    m = re.search(r"^### Taxonomy Coverage Scan\s*$(.*?)(?=^### |\Z)", mode_a, re.M | re.S)
    assert m, "Mode A's Taxonomy Coverage Scan section is gone"
    return m.group(1)


def _rules_section(mode_a: str) -> str:
    m = re.search(r"^### Mode A Integration Rules\s*$(.*?)(?=^---|\Z)", mode_a, re.M | re.S)
    assert m, "Mode A's Integration Rules section is gone"
    return m.group(1)


def _categories(text: str) -> list[str]:
    return re.findall(r"^\*\*(.+?):\*\*\s*$", _scan_section(_mode_a(text)), re.M)


def _category_body(text: str, name: str) -> str:
    scan = _scan_section(_mode_a(text))
    m = re.search(rf"^\*\*{re.escape(name)}:\*\*\s*$(.*?)(?=^\*\*|^### |\Z)", scan, re.M | re.S)
    assert m, f"category {name!r} is not in Mode A's coverage scan"
    return m.group(1)


def _scanner_module():
    spec = importlib.util.spec_from_file_location("_scg_clarify_semantic", SCANNER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --- C-1: the category count is twelve, reached by addition and not by substitution ---


def test_c1_mode_a_carries_twelve_categories():
    text = _text(TAXONOMY)
    cats = _categories(text)
    assert len(cats) == 12, (
        f"Mode A carries {len(cats)} taxonomy categories, expected 12 (the eleven "
        f"pre-existing ones plus {NEW_CATEGORY!r}): {cats}"
    )
    # Companion: the count is not reached by swapping names.
    missing = [c for c in PREEXISTING_CATEGORIES if c not in cats]
    assert not missing, f"pre-existing Mode A categories dropped: {missing}"
    assert len(PREEXISTING_CATEGORIES) == 11, "sentinel: the pinned pre-existing roster moved"


def test_c1_category_is_named_deferred_by_assumption():
    cats = _categories(_text(TAXONOMY))
    assert NEW_CATEGORY in cats, (
        f"Mode A has no {NEW_CATEGORY!r} category; found: {cats}"
    )


# --- C-2: the category states its three hit conditions and its Clear boundary ---


def test_c2_three_hit_conditions_are_named():
    body = _category_body(_text(TAXONOMY), NEW_CATEGORY)
    missing = [lit for lit in HIT_CONDITION_LITERALS if lit not in body]
    assert not missing, (
        f"{NEW_CATEGORY} lost hit conditions {missing}. Without all three the category "
        "collapses back into `Misc / Placeholders`, which scans markers and unquantified "
        "adjectives only — the exact blind spot F-07 names."
    )
    assert len(HIT_CONDITION_LITERALS) == len(HIT_PATTERNS), (
        "sentinel: the condition literals and the discriminability patterns drifted apart"
    )


def test_c2_category_states_a_clear_boundary():
    """A category with no negative boundary fires on everything and decides nothing."""
    body = _category_body(_text(TAXONOMY), NEW_CATEGORY)
    assert "Stays Clear" in body, (
        f"{NEW_CATEGORY} states no Clear boundary — an entry that fixes a value with no "
        "competing alternative and no nominated later phase would be flagged too"
    )
    assert "Constraints & Tradeoffs" in body, (
        f"{NEW_CATEGORY} does not hand a *rejected* alternative to Constraints & Tradeoffs; "
        "rejected and postponed are different states and the two categories would overlap"
    )
    assert "materiality" in body, (
        f"{NEW_CATEGORY} does not route its hits through /speckit.clarify's materiality "
        "filter, so every unfinished-sounding entry would become a question"
    )


# --- C-3: discriminability — positive samples fire, negative samples do not ---


def test_c3_every_positive_sample_fires_at_least_one_condition():
    dead = []
    for sample in POSITIVE_SAMPLES:
        fired = [i for i, p in enumerate(HIT_PATTERNS) if p.search(sample)]
        if not fired:
            dead.append(sample[:70])
    assert not dead, (
        f"wordings that must be marked Partial/Missing fire on nothing: {dead}"
    )
    assert len(POSITIVE_SAMPLES) >= 3, "sentinel: the positive sample set was thinned"


def test_c3_no_negative_sample_fires():
    false_positives = []
    for sample in NEGATIVE_SAMPLES:
        fired = [i for i, p in enumerate(HIT_PATTERNS) if p.search(sample)]
        if fired:
            false_positives.append((sample[:60], fired))
    assert not false_positives, (
        f"wordings that must stay Clear were flagged: {false_positives}. A category that "
        "fires on a plain recorded fact has no discriminative power."
    )
    # Anti-vacuity companions: the zero above is only meaningful because (1) the same
    # patterns do fire in this run, and (2) the negatives are shaped like real entries
    # rather than being trivially unlike them.
    fired_total = sum(1 for s in POSITIVE_SAMPLES for p in HIT_PATTERNS if p.search(s))
    assert fired_total >= len(POSITIVE_SAMPLES), (
        "sentinel: HIT_PATTERNS fired on nothing at all, so 'no negative sample fires' "
        "would pass vacuously"
    )
    assert len(NEGATIVE_SAMPLES) >= 3, "sentinel: the negative sample set was thinned"
    assert all(s.startswith("Assumption:") for s in NEGATIVE_SAMPLES), (
        "sentinel: the negative samples stopped looking like Assumption entries"
    )


def test_c3_each_condition_pattern_is_independently_live():
    """No dead condition: each of the three fires on at least one positive sample."""
    fired_per_pattern = [[s for s in POSITIVE_SAMPLES if p.search(s)] for p in HIT_PATTERNS]
    dead = [HIT_CONDITION_LITERALS[i] for i, fired in enumerate(fired_per_pattern) if not fired]
    assert not dead, (
        f"hit conditions no positive sample exercises, so they could be deleted undetected: {dead}"
    )
    # Companion: the conditions are not all collapsed onto one sample.
    assert len({s for fired in fired_per_pattern for s in fired}) >= 2, (
        "sentinel: every condition fires on the same single sample"
    )


# --- C-4: the document-order invariant ---


def test_c4_document_order_invariant_beside_append_only():
    rules = _rules_section(_mode_a(_text(TAXONOMY)))
    assert "Document-order invariant" in rules, "the document-order invariant is gone"
    assert "ORDER BREAK" in rules, (
        "the invariant names no ORDER BREAK verdict, so there is no machine-readable "
        "output to adjudicate against"
    )
    # Position: the report requires it *beside* the append-only invariant, not folded
    # into the ID-set check it complements. Measured gap is 387 chars — the length of the
    # append-only bullet itself, i.e. the two are adjacent; 1500 allows that bullet to grow
    # without letting the invariant be relocated across the section.
    append_at = rules.index("Append-only invariant")
    order_at = rules.index("Document-order invariant")
    assert 0 < order_at - append_at < 1500, (
        f"the document-order invariant sits {order_at - append_at} chars from the "
        "append-only invariant it complements; the report requires them adjacent"
    )
    assert "empty output means ordered" in rules.lower().replace("**", ""), (
        "the invariant does not say what a clean verdict looks like, so an agent cannot "
        "tell 'no breaks' from 'the check never ran'"
    )


def test_c4_extraction_is_definition_anchored_and_history_excluded():
    """Both anchors are load-bearing; the owner text must say why.

    Measured, not assumed. On a clean spec, comparing every ``FR-\\d+`` *occurrence*
    instead of every *definition* reports five false breaks (cross-references are
    legitimately out of order); including ``## Clarifications`` turns append-only history
    that quotes pre-renumbering definition lines into a sixth. Dropping either anchor
    makes the assertion fire on correct artifacts, which trains the next agent to ignore
    it.
    """
    rules = _rules_section(_mode_a(_text(TAXONOMY)))
    region = rules[rules.index("Document-order invariant"):]
    block = re.search(r"```bash\n(.*?)```", region, re.S)
    assert block, "the interim extraction block is gone from the document-order invariant"
    cmd = block.group(1)
    assert r"^- \*\*(FR|SC)-[0-9]+\*\*" in cmd, (
        "the extraction stopped anchoring on definition lines"
    )
    assert "## Clarifications" in cmd, "the extraction stopped excluding the history section"
    assert "load-bearing" in rules, (
        "the two anchors are no longer documented as load-bearing, so the next edit "
        "'simplifies' the extraction and reintroduces the false breaks"
    )


def test_c4_shared_implementation_with_the_requirements_validator_is_declared():
    rules = _rules_section(_mode_a(_text(TAXONOMY)))
    assert "shares one implementation" in rules, (
        "the invariant no longer declares a shared implementation with /speckit.requirements' "
        "validator, so the two commands are free to drift about what 'in order' means"
    )
    assert "/speckit.requirements" in rules, "the sharing partner is unnamed"


# --- C-5: the derived-count revisit ---


def test_c5_derived_count_revisit_follows_renumbering():
    rules = _rules_section(_mode_a(_text(TAXONOMY)))
    assert "Derived-count revisit" in rules, "the derived-count revisit obligation is gone"
    assert "checklists/requirements.md" in rules, (
        "the revisit names no artifact, so the obligation points nowhere"
    )
    # Position: the report requires it *after* the Removal & renumbering obligation.
    assert rules.index("Removal & renumbering") < rules.index("Derived-count revisit"), (
        "the derived-count revisit must follow the Removal & renumbering obligation it "
        "extends"
    )


def test_c5_revisit_covers_both_file_states_and_the_zero_residual_grep():
    rules = _rules_section(_mode_a(_text(TAXONOMY)))
    revisit = rules[rules.index("Derived-count revisit"):]
    revisit = revisit[: revisit.index("Append-only invariant")]
    for state in ("file exists", "file absent", "pending generation"):
        assert state in revisit, f"the revisit does not cover the {state!r} state"
    assert "zero residual stale counts" in revisit, (
        "the revisit does not require a zero-residual grep, so a refreshed checklist can "
        "keep a second, stale count elsewhere in the same file"
    )
    assert "requirements-guidelines.md" in revisit, (
        "the revisit restates the checklist's structure instead of reaching its owner "
        "(`shared/guidelines/requirements-guidelines.md`) by reference"
    )


# --- C-6: the confirmation-gate budget stays untouched ---


def test_c6_written_surfaces_add_no_blocking_gate_wording():
    """Scoped zero-hit guard: the budget is 23 with zero integer headroom.

    The repo-wide total is pinned elsewhere; this guard names *which* file entered the
    count, and it also catches the case where a hit added here is masked by a hit removed
    elsewhere in the same run. Loads the scanner's own compiled pattern rather than a
    copy of it (precedent: test_feedback_two_path_routing.py).
    """
    blocking = _scanner_module().BLOCKING_RE
    hits = []
    examined = 0
    for rel in ZERO_HIT_SURFACES:
        path = ROOT / rel
        assert path.is_file(), f"written surface missing: {rel}"
        lines = _text(path).splitlines()
        examined += len(lines)
        hits += [(rel, i + 1, m.group(0))
                 for i, ln in enumerate(lines) if (m := blocking.search(ln))]
    assert not hits, (
        f"surfaces this change writes gained blocking-gate wording {hits}; the scanner's "
        "total is pinned at exactly 23 with zero integer headroom"
    )

    gate_carrying = ROOT / GATE_CARRYING_SURFACE
    assert gate_carrying.is_file(), f"written surface missing: {GATE_CARRYING_SURFACE}"
    text = _text(gate_carrying)
    lines = text.splitlines()
    head, tail = GATE_CARRYING_REGION
    assert head in text, f"the added bullet's lead is gone from {GATE_CARRYING_SURFACE}"
    start = text.index(head)
    end = text.index(tail, start)
    ours = text[start:end].splitlines()
    ours_hits = [(i + 1, m.group(0))
                 for i, ln in enumerate(ours) if (m := blocking.search(ln))]
    assert not ours_hits, (
        f"the constraint-side-reading bullet added to {GATE_CARRYING_SURFACE} hits "
        f"BLOCKING_RE: {ours_hits}"
    )
    # Anti-vacuity companions: the region scoping really found this change's lines, and
    # it is not absorbing more than the one pre-existing gate it declares.
    assert len(ours) >= 10, (
        f"sentinel: the scoped region holds only {len(ours)} lines, so 'zero hits' would "
        "mean 'we barely looked'"
    )
    all_hits = [ln for ln in lines if blocking.search(ln)]
    assert len(all_hits) == 1 and PREEXISTING_GATE_FRAGMENT in all_hits[0], (
        f"sentinel: {GATE_CARRYING_SURFACE} carries {len(all_hits)} gate hits; the scoping "
        f"above is justified only by the single pre-existing one ({PREEXISTING_GATE_FRAGMENT!r})"
    )
    assert examined > 200, f"sentinel: only {examined} lines examined across the whole-file surfaces"
    assert len(ZERO_HIT_SURFACES) == 3, "sentinel: the written-surface roster moved"
