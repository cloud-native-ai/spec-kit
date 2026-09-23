"""Contract tests: `/speckit.requirements`' convention entry points.

Subject: ``templates/commands/requirements.md``, ``shared/workflow/glossary.md`` §1, and
``shared/workflow/user-input-protocol.md`` § Mid-Run Addendum Input — driven by the
confirmed introspection finding F-10. The command told the agent to "write to the house
conventions" without naming where any of them lives, so paths were guessed and the error
surfaced only downstream. Four entry points close that:

* **D-1** — the convention-sampling step names the artifact file it samples and writes.
* **D-2** — a concept-owner check that locates the owning document under
  ``shared/definitions/`` *before* drafting.
* **D-3** — the command's ``## Glossary`` section is a pointer; the protocol's conditions
  live only in ``shared/workflow/glossary.md``.
* **D-4** — that owner carries the constraint-side reading obligation the pointer names.
* **D-5** — the user-input protocol disposes of input that arrives *after* wrap-up.

No gate-budget guard lives here: the sibling
``test_clarify_semantic_completeness.py`` C-6 already pins all four surfaces this change
writes (including ``shared/constants/clarify-taxonomy.md``) as zero-hit against the
confirmation-gate scanner, whose budget has zero integer headroom. Duplicating the
proposition here would give it two owners.

Pin hygiene: every zero-hit assertion carries a non-empty companion, so a needle that
stopped matching fails loudly instead of passing vacuously.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]
REQUIREMENTS = ROOT / "templates" / "commands" / "requirements.md"
GLOSSARY_PROTOCOL = ROOT / "shared" / "workflow" / "glossary.md"
USER_INPUT = ROOT / "shared" / "workflow" / "user-input-protocol.md"

# Characteristic literals of the protocol owner's own rule text. Their presence in a
# command's `## Glossary` section is the copy D-3 exists to prevent. Labels may stay
# beside a pointer (the C-9 precedent in test_user_facing_comprehension_pointers.py);
# condition sets may not.
OWNER_ONLY_LITERALS = (
    "homophone",
    "origin=auto",
    "status=proposed",
    "mechanical ceiling",
    "established disposition",
    "named anti-pattern",
    "Common everyday words MUST NOT be recorded",
    "--confirmed-resolution",
)

# The same bound the sibling `## Feedback` / `## Documentation` reference steps are held
# to (test_feedback_step_reference_form.py MAX_SECTION_BYTES): a pointer section that
# grows past it has started restating the owner.
MAX_GLOSSARY_SECTION_BYTES = 1500

GLOSSARY_POINTER = ".specify/shared/workflow/glossary.md"

WRAP_UP_OWNERS = (
    "shared/workflow/artifact-commit-step.md",
    "shared/workflow/feedback-step.md",
    "shared/workflow/docs-step.md",
)


def _text(path: Path) -> str:
    """Unguarded read: a missing artifact must surface as FileNotFoundError, not an assert."""
    return path.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    m = re.search(rf"^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    assert m, f"missing H2 section: ## {heading}"
    return m.group(1)


def _outline_step(text: str, lead: str) -> str:
    """The numbered Outline sub-step (three-space indent) whose text carries `lead`."""
    steps = re.findall(r"^   \d+\..*?(?=^   \d+\.|\Z)", text, re.M | re.S)
    assert steps, "sentinel: no indented Outline sub-steps were parsed at all"
    match = [s for s in steps if lead in s]
    assert match, f"no Outline sub-step carries {lead!r}"
    return match[0]


# --- D-1: the convention-sampling step names the artifact file ---


def test_d1_convention_step_names_the_artifact_file():
    text = _text(REQUIREMENTS)
    step = _outline_step(text, "**Peek at house conventions")
    assert "`requirements.md`" in step, (
        "the convention-sampling step does not name the artifact file it samples, so the "
        "agent guesses a path and the ENOENT surfaces in a later phase"
    )
    assert "templates/requirements-template.md" in step, (
        "the step does not name the template the same artifact is scaffolded from — the "
        "other half of 'derive the filename rather than recall it'"
    )
    assert "SPEC_FILE" in step, (
        "the step does not tie the sampled filename back to the SPEC_FILE the run script "
        "returned, so the two could still diverge"
    )
    # Companion: the step really is the bounded/summary-first one, not some other text
    # that happens to mention the filename.
    assert "token-efficiency" in step, "sentinel: the sampled step is not the bounded peek"


# --- D-2: the concept-owner check ---


def test_d2_concept_owner_check_present_and_precedes_drafting():
    text = _text(REQUIREMENTS)
    assert "**Concept-owner check**" in text, "the concept-owner check step is gone"
    assert "shared/definitions/" in text, (
        "the concept-owner check names no directory to look in, which is the gap D-2 closes"
    )
    assert "before drafting" in text, (
        "the check is not ordered before drafting, so it can be discharged after the "
        "requirement is already written to recall"
    )
    assert text.index("**Concept-owner check**") < text.index("Fill User Scenarios"), (
        "the concept-owner check sits after the drafting steps it is supposed to gate"
    )


def test_d2_unlocatable_owner_is_declared_a_new_concept():
    text = _text(REQUIREMENTS)
    step = _outline_step(text, "**Concept-owner check**")
    assert "new** concept" in step, (
        "the step does not say what to do when no owner can be located, so the fallback is "
        "an inline definition — a second owner for the same concept"
    )
    assert "recall" in step, (
        "the step does not rule out writing from recall, which is the failure mode F-10 names"
    )
    assert "constraint-side reading" in step, (
        "the step does not hand concept *names* to the glossary's constraint-side reading, "
        "so the two entry points stay unconnected"
    )


# --- D-3: the command's `## Glossary` section is a pointer, not a copy ---


def test_d3_glossary_section_restates_none_of_the_owner_conditions():
    section = _section(_text(REQUIREMENTS), "Glossary")
    owner = _text(GLOSSARY_PROTOCOL)
    # Anti-vacuity companion first: the needles must be live owner text, otherwise their
    # absence from the command proves nothing.
    stale = [lit for lit in OWNER_ONLY_LITERALS if lit not in owner]
    assert not stale, (
        f"needles no longer present in the protocol owner, so D-3 would pass vacuously: {stale}"
    )
    copied = [lit for lit in OWNER_ONLY_LITERALS if lit in section]
    assert not copied, (
        f"the command's `## Glossary` section restates the owner's conditions: {copied}. "
        "F-10③ leaves the conditions in the owner and keeps only a pointer here."
    )


def test_d3_glossary_section_is_a_real_pointer_within_the_house_bound():
    section = _section(_text(REQUIREMENTS), "Glossary")
    size = len(section.encode("utf-8"))
    assert size <= MAX_GLOSSARY_SECTION_BYTES, (
        f"the `## Glossary` pointer section is {size} B, over the {MAX_GLOSSARY_SECTION_BYTES} B "
        "bound the sibling `## Feedback` / `## Documentation` steps are held to — it has "
        "started restating the owner"
    )
    # Companions: a section shrunk to nothing would also satisfy the bound and D-3.
    assert size > 100, f"sentinel: the `## Glossary` section is only {size} B — it was deleted, not converged"
    assert GLOSSARY_POINTER in section, "the section no longer points at the protocol owner"
    for marker in ("§1", "§2", "§3", "§4"):
        assert marker in section, (
            f"the pointer does not name {marker}, so a reader cannot reach the rule that "
            "applies to them without reading the whole owner"
        )
    assert "constraint-side reading" in section, (
        "the pointer does not name the constraint-side reading obligation — the one rule "
        "F-10③ adds to the owner, and the one a command reader would otherwise miss"
    )


# --- D-4: the owner carries the constraint-side reading obligation ---


def test_d4_owner_owns_the_constraint_side_reading():
    text = _text(GLOSSARY_PROTOCOL)
    section = _section(text, "1. Input correction & anchoring (voice-first)")
    assert "Constraint-side reading" in section and "约束侧读取" in section, (
        "§1 no longer carries the constraint-side reading obligation under both names"
    )
    for kind in ("mechanical ceiling", "established disposition", "named anti-pattern"):
        assert kind in section, (
            f"§1 does not enumerate the registered constraint kind {kind!r}; a reader "
            "cannot tell what to look for in an entry"
        )
    assert "by topic domain" in section, (
        "§1 does not bound the reading to a topic domain, so the obligation reads as "
        "'load the whole table' — the summary-first violation F-10's sibling findings name"
    )
    assert "MUST NOT restate" in section, (
        "§1 does not forbid command-side restatement, so the obligation can be copied back "
        "into a command template and drift there"
    )


# --- D-5: input arriving after wrap-up ---


def test_d5_post_wrap_up_addendum_is_disposed_of():
    text = _text(USER_INPUT)
    section = _section(text, "Mid-Run Addendum Input")
    assert "Arriving after wrap-up" in section, (
        "§ Mid-Run Addendum Input does not cover input that arrives after the run has "
        "reported completion — the case F-10④ names"
    )
    assert "second invocation" in section, (
        "the rule does not name the alternative it rules out, so 'start a new run' stays "
        "available and re-derives numbering against the same artifact"
    )
    assert "validation gate **once**" in section, "the upstream gate is not re-run exactly once"
    assert "incrementally" in section, (
        "the wrap-up side effects are not scoped to what the addendum changed"
    )
    assert "delta against the first wrap-up" in section, (
        "the rule does not say what the second report looks like, so the user gets two "
        "full reports for one run"
    )


def test_d5_wrap_up_side_effects_are_reached_by_owner_path():
    section = _section(_text(USER_INPUT), "Mid-Run Addendum Input")
    missing = [p for p in WRAP_UP_OWNERS if p not in section]
    assert not missing, (
        f"the post-wrap-up rule names no owner for {missing}; it would have to restate "
        "their rules to be actionable"
    )
    # Companions: the three paths resolve, and the section still owns the four earlier rules.
    for rel in WRAP_UP_OWNERS:
        assert (ROOT / rel).is_file(), f"referenced wrap-up owner does not exist: {rel}"
    for rule in ("Batch, do not interleave", "Upstream artifact first", "Record verbatim"):
        assert rule in section, f"sentinel: the pre-existing addendum rule {rule!r} was displaced"
