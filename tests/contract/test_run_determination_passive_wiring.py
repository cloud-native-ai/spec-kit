"""Contract tests for the S3 passive-trigger wiring (运行判定 → the Feedback step).

Landed surfaces under test:

* ``shared/workflow/feedback-step.md`` § *Run Determination* — the consumption point,
  the step-6 composition, the two ruled inputs (OI-2 persistence, OI-9 red state) and
  the passive non-exhaustiveness constraint (D9 detail 3).
* ``templates/instructions-template.md`` § ``## Run Determination`` — the ambient
  summary + pointer, and nothing more.

Design truth (dated record, never cited as current reality):
``.specify/teams/session-driven-self-improvement/runs/2026-10-06-S1-judgment-contract.md``
§ 10–12. After landing, ownership of the consumption point migrated to
``feedback-step.md`` and ownership of the schema / value domains / routing-bit
derivation migrated to **code** — ``scripts/python/run-determination.py``.

Three house disciplines shape this file:

* **One Source of Truth** (``shared/guidelines/one-source-of-truth.md``). Most guards
  below are *negatives*: they assert the landed prose reaches a fact by reference instead
  of copying it. Where the fact is code-owned the guard **executes the owner** rather
  than pinning a literal — ``derive_trigger_feedback`` is called, the memory engine's
  ``validate_source`` is called — so no guard copy of the formula or of the ``--source``
  grammar appears here.
* **反空真哨兵**. Every "the landed text does not carry X" assertion is paired with a
  positive control proving the probe can see X when X is there, so "absent because
  correct" stays distinguishable from "absent because the probe is blind".
* **Red-First 取证 / 变异演练** (owner: ``.specify/memory/glossary.md``). Evidence:
  ``.specify/teams/.work/session-driven-self-improvement/outputs/red-first-evidence-s3.md``.

``TestOwnerSurfaces`` deliberately passes **before** the wiring exists. That is the
discriminator: it proves the module imports, the owners resolve and the probes are
non-blind, so a red wiring test failed because the wiring is absent rather than because
this file is broken.
"""
from __future__ import annotations

import importlib.util
import inspect
import re
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]

FEEDBACK_STEP = REPO_ROOT / "shared" / "workflow" / "feedback-step.md"
INSTRUCTIONS = REPO_ROOT / "templates" / "instructions-template.md"
TODO_CMD = REPO_ROOT / "templates" / "commands" / "todo.md"
ENGINE = REPO_ROOT / "scripts" / "python" / "run-determination.py"
MEMORY_ENGINE = REPO_ROOT / "scripts" / "python" / "memory-utils.py"
SCANNER = REPO_ROOT / "scripts" / "python" / "scan-confirmation-gates.py"

WIRING_HEADING_PREFIX = "## Run Determination"
AMBIENT_HEADING = "## Run Determination"

#: The drift trap named by the S1 contract § 14.1 and by this team's ceiling note:
#: step 6's verb is ``run``. The scanner's pattern tuple carries a nearby form
#: differing only in verb and object, and the gate budget's margin is zero.
SAFE_STEP6_WORDING = "inviting the user to run the `/speckit.feedback` command"
UNSAFE_STEP6_WORDING = "inviting the user to submit collected feedback"

#: Characteristic literals of the four red lines. Each is owned by
#: § *Positioning & Red Lines* and MUST occur exactly once in the file — a second
#: occurrence means the wiring section restated a red line instead of referencing it.
RED_LINE_LITERALS = (
    "**Target = the Spec Kit framework itself.**",
    "**Feedback is user data and fully optional.**",
    "**Zero automated transmission.**",
    "**Local workaround value.**",
)

#: The memory-store directories that already have owners. The wiring section MUST NOT
#: introduce another one: "no new store" is a fact about paths, so it is guarded as a
#: path set rather than as a promise.
OWNED_MEMORY_DIRS = {"session", "knowledge", "feedback", "trigger", "todo"}


# ---------------------------------------------------------------------------
# loaders and readers
# ---------------------------------------------------------------------------


def _load(path: Path, name: str):
    assert path.is_file(), f"missing owner surface: {path}"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None, f"cannot load spec for {path}"
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def eng():
    return _load(ENGINE, "_rd_passive_wiring_engine")


@pytest.fixture(scope="module")
def mem():
    return _load(MEMORY_ENGINE, "_rd_passive_wiring_memory")


@pytest.fixture(scope="module")
def blocking_re():
    """The scanner's own compiled pattern set — never a second phrase list here."""
    module = _load(SCANNER, "_rd_passive_wiring_scanner")
    # Anti-vacuity sentinel: an empty pattern would make every zero-hit guard below
    # pass for nothing, and the trap form is the positive control for step 6.
    assert module.BLOCKING_RE.search("等待用户确认"), "scanner BLOCKING_RE loaded empty"
    assert module.BLOCKING_RE.search(UNSAFE_STEP6_WORDING), (
        "scanner BLOCKING_RE no longer matches the known trap form — the positive "
        "control for the step-6 verb guard is gone"
    )
    return module.BLOCKING_RE


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _flat(text: str) -> str:
    """Whitespace-collapsed view, so a prose assertion cannot be broken by a rewrap.

    Line structure is asserted separately and only where it carries meaning (the
    same-line prohibition below).
    """
    return re.sub(r"\s+", " ", text)


def _section(text: str, heading_prefix: str) -> str:
    """Body of the `## `-section whose heading starts with ``heading_prefix``.

    Stops at the next top-level heading that sits **outside** a fenced block, because
    this file's sibling section carries ```markdown examples whose inner ``## ``
    headings would otherwise truncate the slice — the same trap
    ``test_feedback_step_reference_form.py`` documents.
    """
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip().startswith(heading_prefix):
            start = i
            break
    assert start is not None, f"no section starting with {heading_prefix!r}"
    in_fence = False
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence and (lines[j].startswith("## ") or lines[j].startswith("# ")):
            return "\n".join(lines[start + 1 : j])
    return "\n".join(lines[start + 1 :])


@pytest.fixture(scope="module")
def wiring() -> str:
    return _section(_text(FEEDBACK_STEP), WIRING_HEADING_PREFIX)


@pytest.fixture(scope="module")
def wiring_flat(wiring) -> str:
    return _flat(wiring)


@pytest.fixture(scope="module")
def ambient() -> str:
    return _section(_text(INSTRUCTIONS), AMBIENT_HEADING)


def _reflection_procedure(text: str) -> str:
    """The Reflection procedure's own section.

    Scoping is load-bearing, not tidiness: ``## Positioning & Red Lines`` and
    ``## Threshold prompt protocol`` carry numbered lists of their own, so an unscoped
    ``^2\\.`` search binds to "2. **Feedback is user data…**" and every assertion about
    step 2 is then made about the wrong list — and passes or fails for a reason that has
    nothing to do with the step under test.
    """
    return _section(text, "## Reflection procedure")


def _numbered_step(text: str, n: int, end: str | None = None) -> str:
    """Step ``n`` of the Reflection procedure, sliced out of that section only.

    ``end`` bounds the last step, whose numbered sibling does not exist: without it the
    slice runs to the end of the section and an assertion about step 6 could be satisfied
    by prose that follows it.
    """
    body = _reflection_procedure(text)
    tail = rf"(?=^{n + 1}\.\s\*\*|\Z)" if end is None else rf"(?={end}|\Z)"
    match = re.search(rf"^{n}\.\s\*\*.*?{tail}", body, flags=re.M | re.S)
    assert match, f"sentinel: numbered step {n} was not parsed out of the procedure at all"
    return match.group(0)


# ===========================================================================
# Owner surfaces — these pass before the wiring lands. They are the discriminator
# that makes the red wiring tests meaningful, and they execute the code owners
# instead of pinning guard copies of their rules.
# ===========================================================================


class TestOwnerSurfaces:
    def test_engine_owns_the_routing_bit_and_it_is_asymmetric(self, eng):
        """Executes the owner of ``trigger_feedback`` rather than copying its formula.

        The asymmetry is the whole noise guard: one regressed comparison axis records,
        two fire. If the engine ever lost it, the wiring prose that promises it would be
        a lie — so the promise is checked against the code, not against a literal.
        """
        assert hasattr(eng, "derive_trigger_feedback"), "the routing-bit owner is gone"

        def axes(token, elapsed, correctness="ok", satisfaction="accepted"):
            return {
                "token_consumption": {"verdict": token},
                "elapsed": {"verdict": elapsed},
                "artifact_correctness": {"verdict": correctness},
                "satisfaction": {"verdict": satisfaction},
            }

        # Positive controls: the bit CAN be true, so the negatives below are not vacuous.
        assert eng.derive_trigger_feedback("qualified", axes("regressed", "regressed"))
        assert eng.derive_trigger_feedback(
            "qualified", axes("unchanged", "unchanged", correctness="regressed"))
        assert eng.derive_trigger_feedback(
            "qualified", axes("unchanged", "unchanged", satisfaction="rejected"))
        # The asymmetry itself.
        assert not eng.derive_trigger_feedback("qualified", axes("regressed", "unchanged"))
        assert not eng.derive_trigger_feedback("qualified", axes("unchanged", "regressed"))
        # An unqualified run never routes, whatever the axes say.
        assert not eng.derive_trigger_feedback(
            "aborted", axes("regressed", "regressed", correctness="regressed"))

    def test_memory_engine_source_grammar_accepts_exactly_two_forms(self, mem):
        """The fact S3 had to read out of the engine instead of out of the contract.

        ``custom:<owner>/<name>`` is a legal ``unit_id`` for the determination engine and
        for the feedback engine, and is **not** a legal ``--source`` here. That
        asymmetry is what makes the fail-closed rule below necessary.
        """
        assert mem.validate_source("/speckit.plan") is True
        assert mem.validate_source("skill:create-team") is True
        assert mem.validate_source("custom:team/reviewer") is False
        # Positive control on the negative: the grammar is not merely rejecting
        # everything, which would make the custom-unit refusal prove nothing.
        assert mem.validate_source("") is False
        assert mem.validate_source("/speckit.") is False

    def test_the_two_seams_are_present_and_single_sited(self, eng):
        source = _text(ENGINE)
        for symbol in ("OI2_PERSISTENCE_ADAPTER", "PERSISTENCE_ADAPTERS",
                       "OI9_RED_STATE_INPUT"):
            assert hasattr(eng, symbol), f"seam {symbol} is gone from the engine"
        assert callable(eng.read_red_state), "the OI-9 producer seam is gone"
        assert source.count("OI2_PERSISTENCE_ADAPTER = ") == 1
        assert source.count("OI9_RED_STATE_INPUT = ") == 1

    def test_park_mode_is_really_owned_by_the_todo_command(self):
        """D9 detail 3 names ``/speckit.todo`` Park Mode as the default carrier.

        Verified against the owner rather than taken from the contract: the flag, the
        store path and the promote route into the Requirement plane must all be there,
        or the wiring would point at a carrier that does not exist.
        """
        text = _text(TODO_CMD)
        assert "--park" in text, "todo.md no longer documents Park Mode's flag"
        assert "Park Mode" in text, "todo.md no longer names Park Mode"
        assert ".specify/memory/todo/" in text, "the park store path is gone"
        assert "/speckit.requirements" in text, "the promote route into a spec is gone"

    def test_step6_safe_wording_survives_and_the_trap_form_is_absent(self, blocking_re):
        text = _text(FEEDBACK_STEP)
        assert SAFE_STEP6_WORDING in text, (
            "step 6 lost the safe verb form; the scanner's pattern tuple carries a "
            "nearby form differing only in verb and object, and the gate budget's "
            "margin is zero"
        )
        assert UNSAFE_STEP6_WORDING not in text
        assert blocking_re.search(SAFE_STEP6_WORDING) is None, (
            "the safe form now matches the scanner — re-word it, do not raise the budget"
        )

    def test_owner_file_surfaces_resolve(self):
        for path in (FEEDBACK_STEP, INSTRUCTIONS, ENGINE, MEMORY_ENGINE, SCANNER, TODO_CMD):
            assert path.is_file(), f"missing surface: {path}"


# ===========================================================================
# The consumption point (S1 § 10)
# ===========================================================================


class TestConsumptionPoint:
    def test_the_wiring_section_exists(self, wiring):
        assert wiring.strip(), "the wiring section is empty"
        assert len(wiring.splitlines()) >= 20, (
            f"the wiring section is {len(wiring.splitlines())} lines — that is a stub, "
            "not a landing of nine normative clauses"
        )

    def test_the_section_declares_what_it_owns(self, wiring):
        """One Source of Truth: an owner says so in its opening lines and names what it
        owns — and disclaims what code owns, so nobody looks here for a value domain."""
        opening = "\n".join(wiring.splitlines()[:6])
        assert "owner" in opening.lower(), "the section does not declare ownership"
        assert "value domain" in opening, (
            "the section must disclaim the code-owned value domains in the same breath "
            "it claims the wiring"
        )

    def test_the_consumption_boundary_is_named(self, wiring):
        assert "step 1 → step 2 boundary" in wiring, (
            "the consumption point is not the boundary the design fixed; a reader "
            "cannot tell where the determination enters this step"
        )

    @pytest.mark.parametrize("n", [1, 2])
    def test_the_numbered_steps_carry_the_pointer_in_place(self, n):
        """The boundary is wired *inside* the procedure, not only in a distant section.

        A rule stated in exactly one place is effectively absent (Ask, Record, Repeat):
        an agent executing step 1 reads step 1, so step 1 must reach the wiring.
        """
        step = _numbered_step(_text(FEEDBACK_STEP), n)
        assert "运行判定" in step, f"step {n} does not name the mechanism it now consumes"
        assert "Run Determination" in step, (
            f"step {n} carries no pointer to the wiring section that owns the detail"
        )

    def test_step_2_keeps_its_own_three_questions(self):
        """The generalization reuses step 2's self-check; it does not absorb it."""
        step = _numbered_step(_text(FEEDBACK_STEP), 2)
        for probe in ("原文转储", "代做确定性工作", "重复读取"):
            assert probe in step, f"step 2 lost Token 三问 probe {probe!r}"

    def test_steps_3_4_5_are_declared_unchanged(self, wiring_flat):
        assert re.search(r"\*\*Steps 3, 4 and 5\*\* are unchanged", wiring_flat), (
            "the wiring must state that the scope guard, the dedup guard and the persist "
            "call are untouched — otherwise the record reads as a second feedback entry"
        )
        assert "never enters the step-5 call" in wiring_flat

    def test_step_6_composes_and_degrades_without_a_record(self, wiring, wiring_flat):
        """Both halves: the composition, and the honest behaviour when the sensor did not
        run. The second half is what keeps red line 2 true — an absent determination MUST
        NOT silently switch off a notification the user receives today."""
        assert "should_prompt" in wiring_flat and "trigger_feedback" in wiring_flat
        assert "neither replaces the other" in wiring_flat
        assert "Absent record" in wiring, "the missing-record clause is gone"
        assert "governs on `should_prompt` alone" in wiring_flat, (
            "without this, an absent determination would suppress an existing notification"
        )
        assert "not evaluated" in wiring_flat, "an absent record must be reported, not hidden"
        step6 = _numbered_step(_text(FEEDBACK_STEP), 6,
                               end=r"^\*\*Abort / partial-run rule")
        assert "composes" in step6 and "Run Determination" in step6, (
            "step 6 itself carries no pointer to the composition rule"
        )

    def test_the_routing_bit_owner_is_cited_by_symbol(self, wiring, eng):
        assert "derive_trigger_feedback" in wiring, (
            "the derivation must be reached by naming its code owner, so the pointer can "
            "be checked instead of trusted"
        )
        assert hasattr(eng, "derive_trigger_feedback"), "the cited symbol does not exist"

    def test_the_asymmetry_is_stated_in_prose_not_as_a_formula(self, wiring_flat):
        """The one property a reader must not miss, said in words — while the formula
        itself stays in code (guarded by the no-copy class below)."""
        assert "single** regressed comparison axis does not fire the passive path" in wiring_flat
        assert "recorded, and the active improve flow picks it up later" in wiring_flat
        assert "regressed on **both** comparison axes at once" in wiring_flat


# ===========================================================================
# Reference, not copy
# ===========================================================================


class TestReferenceNotCopy:
    def test_the_no_reason_literal_is_restated(self, wiring, eng):
        """The closed reason set is code-owned; a copy here would drift silently.

        Positive control first, so "zero hits" cannot mean "the probe is blind".
        """
        assert len(eng.REASONS) >= 10, "sentinel: the reason set looks empty"
        probe = eng.REASONS[0]
        assert probe in inspect.getsource(eng), "sentinel: reason literal not in its owner"
        leaked = [r for r in eng.REASONS if r in wiring]
        assert not leaked, f"wiring restates the code-owned reason set: {leaked}"

    def test_the_no_satisfaction_input_enumeration_is_restated(self, wiring, ambient, eng):
        """The decision table's input enumeration is the highest-drift copy of all."""
        assert len(eng.USER_TURN_CLASSES) == 5, "sentinel: the turn-class set changed shape"
        assert "topic_change" in inspect.getsource(eng), "sentinel: probe cannot see its owner"
        for surface, name in ((wiring, "wiring"), (ambient, "ambient section")):
            leaked = [c for c in eng.USER_TURN_CLASSES if c in surface]
            assert not leaked, f"{name} restates the user-turn-class enumeration: {leaked}"

    def test_the_no_verdict_domain_is_enumerated(self, wiring, ambient):
        """Naming one verdict while explaining the asymmetry is a reference; carrying the
        domain is a copy. ``not_evaluated`` is the code literal, so prose says "not
        evaluated" and leaves the literal to its owner."""
        for surface, name in ((wiring, "wiring"), (ambient, "ambient section")):
            assert "improved" not in surface, f"{name} enumerates the comparison domain"
            assert "not_evaluated" not in surface, (
                f"{name} carries the code literal `not_evaluated`"
            )

    def test_the_four_red_lines_are_referenced_not_copied(self, wiring_flat):
        text = _text(FEEDBACK_STEP)
        for literal in RED_LINE_LITERALS:
            assert text.count(literal) == 1, (
                f"red line {literal!r} occurs {text.count(literal)} times — the wiring "
                "section restated it instead of referencing the owner section"
            )
        assert "not restated here" in wiring_flat, (
            "the wiring must say the red lines govern it unchanged"
        )
        # Positive control: the single occurrence really is in the owner section.
        owner = _section(text, "## Positioning & Red Lines")
        for literal in RED_LINE_LITERALS:
            assert literal in owner, f"sentinel: {literal!r} is not in its owner section"

    def test_the_exit_code_table_is_not_copied(self, wiring):
        """STR-007's table has an owner; the wiring names the shared table, not its rows."""
        assert "exit-code table" in wiring
        assert not re.search(r"\b0\s*=\s*ok\b", wiring), "the exit-code table was copied"

    def test_the_wiring_carries_no_flag_list(self, wiring):
        """The CLI flag set is generated from the parser, so a prose copy could only
        drift. The section must name the authoritative flag surface instead."""
        flags = re.findall(r"(?<![\w`])--[a-z][a-z0-9-]{2,}", wiring)
        assert not flags, f"wiring restates the engine's flag set: {sorted(set(flags))}"
        assert "`--help`" in wiring, (
            "the section must name the engine's own help as the flag owner"
        )


# ===========================================================================
# OI-9 — the unresolved-red input, narrowed to engine exit codes
# ===========================================================================


class TestRedStateNarrowing:
    def test_engine_exit_codes_are_named_as_the_only_producer(self, wiring):
        assert "engine exit codes only" in wiring
        assert "non-zero exit" in wiring
        assert "exactly one producer" in wiring

    def test_the_telemetry_store_is_forbidden_on_the_same_line(self, wiring):
        """The forbidden read and its prohibition must share a line, so a rewrite that
        keeps the path but drops the MUST NOT cannot pass."""
        lines = [ln for ln in wiring.splitlines() if "telemetry.jsonl" in ln]
        assert lines, "the wiring no longer names the store it forbids reading"
        assert any("MUST NOT" in ln for ln in lines), (
            "the telemetry path is named without its prohibition on the same line"
        )
        schema_lines = [ln for ln in wiring.splitlines() if "row schema" in ln]
        assert schema_lines and any("closed set" in ln for ln in schema_lines), (
            "the reason (a closed row schema owned elsewhere) must be stated, or the "
            "prohibition reads as arbitrary and gets undone later"
        )

    def test_the_dropped_producer_is_named_as_dropped(self, wiring):
        assert "surfaced_anomaly_unanswered" in wiring, (
            "the dropped producer must be named — an unnamed drop is indistinguishable "
            "from a producer nobody implemented"
        )
        para = next(p for p in wiring.split("\n\n") if "surfaced_anomaly_unanswered" in p)
        assert "dropped" in para and "MUST NOT be declared" in _flat(para), (
            "the drop must be normative, not a footnote"
        )

    def test_the_producer_seam_is_cited(self, wiring):
        assert "OI9_RED_STATE_INPUT" in wiring and "read_red_state" in wiring


# ===========================================================================
# OI-2 — where the record lands, and the custom-unit fail-closed rule
# ===========================================================================


class TestPersistenceLanding:
    def test_the_landing_goes_through_the_existing_memory_engine(self, wiring):
        assert "memory-utils.py" in wiring, "the landing point must name its engine"
        assert "`session` scope" in wiring
        assert "run-determination" in wiring, "the separating tag must be named"
        assert "No new store" in wiring

    def test_no_new_memory_directory_is_introduced(self, wiring):
        """"No new store" is a fact about paths, so it is guarded as a path set.

        Positive control: the probe does see a directory literal when one is present.
        """
        found = set(re.findall(r"\.specify/memory/([a-z0-9_-]+)/", wiring))
        assert found, "sentinel: the probe found no memory path at all"
        assert found <= OWNED_MEMORY_DIRS, (
            f"the wiring introduces a memory directory with no owner: "
            f"{sorted(found - OWNED_MEMORY_DIRS)}"
        )

    def test_custom_units_fail_closed_and_no_source_is_invented(self, wiring_flat, mem):
        """The verified fact: the memory engine accepts two source forms, so a ``custom:``
        unit has none. The honest behaviours are fail-closed or widen the owner's
        contract — and widening is not this flow's act."""
        assert "custom:<owner>/<name>" in wiring_flat
        assert "**no** accepted source form" in wiring_flat
        assert "fails closed" in wiring_flat
        assert "`persisted: false`" in wiring_flat
        assert "MUST NOT invent a source string" in wiring_flat
        assert mem.validate_source("custom:team/reviewer") is False

    def test_the_persistence_seam_is_cited(self, wiring):
        assert "OI2_PERSISTENCE_ADAPTER" in wiring and "PERSISTENCE_ADAPTERS" in wiring

    def test_the_read_side_is_a_projection(self, wiring_flat):
        """Summary-First: the read side returns a projection, never record bodies."""
        assert "`history` action is the read side" in wiring_flat
        assert "never record bodies" in wiring_flat


# ===========================================================================
# D9 detail 3 — the passive path is not exhaustive
# ===========================================================================


class TestPassiveNonExhaustiveness:
    def test_the_constraint_is_stated_with_its_reason(self, wiring, wiring_flat):
        assert "MUST NOT be exhaustive" in wiring_flat
        assert "disturb the very run it is measuring" in wiring_flat, (
            "the constraint without its reason gets undone the first time someone decides "
            "more thoroughness would be better"
        )

    def test_in_scope_is_narrowly_defined(self, wiring_flat):
        assert "whose unit is this unit" in wiring_flat
        assert "actually evaluated in this run" in wiring_flat
        assert "only those, feed the routing bit" in wiring_flat

    def test_both_carry_forward_carriers_are_named_with_their_owner(self, wiring_flat):
        assert "/speckit.todo" in wiring_flat and "Park Mode" in wiring_flat
        assert "templates/commands/todo.md" in wiring_flat, (
            "the park carrier must cite the file that owns the mode and its store path"
        )
        assert "/speckit.requirements" in wiring_flat
        assert "Requirement" in wiring_flat, (
            "the spec carrier's boundary (which plane owns the finding) must be stated"
        )

    def test_no_carrier_is_assigned_on_the_passive_turn(self, wiring_flat, eng):
        """Assignment is the active flow's act. The engine's own carrier set is checked so
        the prose cannot promise a behaviour the code contradicts."""
        assert "`parked_via: none`" in wiring_flat
        assert "no carrier assigned" in wiring_flat
        assert "**active** improve flow" in wiring_flat
        assert "none" in eng.PARKED_VIA, "sentinel: the engine dropped the none carrier"

    def test_the_passive_turn_opens_no_second_flow(self, wiring_flat):
        assert "MUST NOT open either flow" in wiring_flat
        assert "widen the current turn" in wiring_flat
        assert "single non-blocking notification" in wiring_flat, (
            "the budget of user-visible output must stay at the one notification step 6 "
            "already owns"
        )


# ===========================================================================
# 改点 is a sensor, not a ledger
# ===========================================================================


class TestSensorNotLedger:
    def test_the_record_carries_no_mutation_authority(self, wiring_flat):
        assert "no disposition, no threshold and no mutation authority" in wiring_flat
        assert "never written under `.specify/memory/feedback/`" in wiring_flat

    def test_the_ledger_is_fed_not_duplicated(self, wiring_flat):
        assert "intervention.json" in wiring_flat
        assert "baseline evidence run directory" in wiring_flat
        assert "one-way" in wiring_flat, "the join direction must be stated"
        assert "never replaces or duplicates that ledger" in wiring_flat
        assert "self-improvement-workflow.md" in wiring_flat

    def test_the_glossary_owns_the_term(self, wiring):
        assert "`.specify/memory/glossary.md`" in wiring, (
            "改点 has a term owner; the wiring must reach it by path"
        )


# ===========================================================================
# The never-solicit line (the reason this wiring is passive at all)
# ===========================================================================


class TestNeverSolicit:
    def test_the_passive_path_infers(self, wiring, wiring_flat):
        assert "The passive path **infers**" in wiring
        assert "already happened" in wiring_flat
        assert "never raw user text" in wiring_flat

    def test_no_question_is_put_to_the_user(self, wiring_flat):
        assert "No question is put to the user" in wiring_flat
        assert "no new user-facing surface class" in wiring_flat

    def test_the_wiring_adds_no_transmission_verb(self, wiring):
        """Red line 3: zero automated transmission, and the wiring gains no path."""
        lowered = wiring.lower()
        for verb in ("upload", "http", "webhook", "curl", " post ", " push ", "request"):
            assert verb not in lowered, (
                f"the wiring section carries a transmission verb {verb!r}"
            )


# ===========================================================================
# The ambient instructions section — summary + pointer, nothing more
# ===========================================================================


class TestInstructionsAmbientSection:
    def test_heading_and_pointer_present(self, ambient):
        assert ambient.strip()
        assert ".specify/shared/workflow/feedback-step.md" in ambient, (
            "the ambient section must reach the wiring owner by path"
        )
        assert ".specify/scripts/python/run-determination.py" in ambient, (
            "the ambient section must name the engine that owns the code-side facts"
        )
        assert "do NOT copy its rules" in ambient, (
            "the house pointer form states the reference obligation explicitly"
        )

    def test_summary_shape_only(self, ambient, eng):
        lines = ambient.splitlines()
        assert len(lines) <= 25, f"ambient section is {len(lines)} lines; the cap is 25"
        assert not any(ln.startswith("### ") for ln in lines), (
            "no `### ` subheadings: additive reconcile propagates whole `## ` sections "
            "only, so content hidden in a subsection never reaches initialized projects"
        )
        leaked_reasons = [r for r in eng.REASONS if r in ambient]
        assert not leaked_reasons, f"ambient restates the reason set: {leaked_reasons}"
        leaked_classes = [c for c in eng.USER_TURN_CLASSES if c in ambient]
        assert not leaked_classes, f"ambient restates the turn classes: {leaked_classes}"
        assert ambient.count("/speckit.") == 0, (
            "the ambient section must not enumerate command names; the owner does"
        )

    def test_position_leaves_the_pinned_window_alone(self):
        """``test_proactive_trigger_section.py`` C-3 pins Documentation Map → Proactive
        Flow Trigger → Fact/Correctness as an exact adjacency. Inserting there would
        break a guard this team does not own."""
        headings = re.findall(r"(?m)^## .+$", _text(INSTRUCTIONS))
        i_doc = headings.index("## Documentation Map")
        i_pro = headings.index("## Proactive Flow Trigger")
        i_sanity = headings.index("## Fact, Correctness & Logic Checks (Input Sanity)")
        assert (i_pro, i_sanity) == (i_doc + 1, i_doc + 2), (
            f"the pinned adjacency moved: {headings[i_doc:i_doc + 4]}"
        )
        assert AMBIENT_HEADING in headings, "the ambient section is missing"
        assert headings.index(AMBIENT_HEADING) > i_sanity, (
            "the new section must not be inserted inside the pinned window"
        )

    def test_project_neutral(self, ambient):
        low = ambient.lower()
        for token in ("spec-kit", "specify-cli", "specify_cli", "cloud-native-ai",
                      "feature 0", ".specify/specs/0"):
            assert token not in low, f"project-specific token {token!r} leaked"

    def test_the_mechanism_name_is_the_ratified_one(self, ambient, wiring):
        for surface, name in ((ambient, "ambient"), (wiring, "wiring")):
            assert "运行判定" in surface, f"{name} section does not use the ratified name"
        assert "Run Determination" in ambient


# ===========================================================================
# Gate budget and retired naming on both landed surfaces
# ===========================================================================


class TestGateBudgetAndNaming:
    @pytest.mark.parametrize("path", [FEEDBACK_STEP, INSTRUCTIONS],
                             ids=lambda p: p.name)
    def test_surface_contributes_zero_blocking_hits(self, path, blocking_re):
        """Both surfaces sit inside the scanner's reach and the budget's margin is zero,
        so this is the local form of the ceiling note: one hit here moves the total and
        breaks every pin that freezes it."""
        text = _text(path)
        hits = [(i + 1, m.group(0))
                for i, line in enumerate(text.splitlines())
                if (m := blocking_re.search(line))]
        assert not hits, f"{path.name} entered the gate count: {hits}"

    @pytest.mark.parametrize("path", [FEEDBACK_STEP, INSTRUCTIONS],
                             ids=lambda p: p.name)
    def test_retired_names_do_not_appear(self, path):
        """Drift guard for the two retired forms named by ``.specify/memory/glossary.md``
        → `运行判定`. The literals below are guard copies in the sense
        ``one-source-of-truth.md`` § Legitimate duplicates allows."""
        text = _text(path)
        for retired in ("断言", "判断逻辑"):
            assert retired not in text, f"{path.name} carries the retired form {retired!r}"
