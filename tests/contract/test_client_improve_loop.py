"""Contract test: client-subject improvement loop — a client artifact runs the
existing SI-0…SI-9 loop with an honest why segment (Feature 072, User Story 4).

Pins `contracts/client-improvement-loop.md` C-33…C-39 against the surfaces that
own them:

* the **loop reuse and unrelaxed criteria** (C-33) — a `custom:` subject walks
  the existing self-improvement workflow's SI-0…SI-9; no client-specific flow,
  skill, or ledger exists; the five Execution Subject criteria stay owned (and
  un-restated) by `shared/definitions/self-improvement-definitions.md`;
* the **fail-closed disclosure** (C-34) — the run-determination engine has no
  legitimate persistence source for a `custom:` subject (its source contract
  accepts only command and skill unit forms), so the why segment states the
  disclosure 「运行判定历史未评估」 together with the engine's reason verbatim;
* the **observation source** (C-35) — for a `custom:` subject the why segment
  observes this unit's `kind: external` entries (the client channel) plus the
  existing evidence lanes; it invents no source string and never phrases "no
  history" as "past runs were fine";
* the **scope boundary** (C-36) — no parallel history store, no second
  observation engine, and the run-determination engine's source contract is
  not widened (that is the engine owner's action);
* the **how segment** (C-37) — routing keeps the existing dispatch table, the
  degrade-to-assisted path, no client improver, and the command never mutates
  a subject directly;
* the **preserved loop constraints** (C-38) — one executed falsification
  attempt before dispatch, exactly one intervention ledger, a hard attempt
  limit, and "outcome pending" until SI-8 comparison;
* the **SI-0 halt** (C-39) — a target with no unique editable definition stops
  at subject resolution, reports 「没有唯一所有者」, leaves the observation for
  a follow-up carrier, and mutates nothing.

Behavioural assertions execute inside the disposable client project built by
`tests/fixtures/client_project.py` — the run-determination engine's honest
fail-closed report is only observable end-to-end where the client branch
actually runs.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from fixtures.client_project import (
    FRAMEWORK_ROOT,
    make_client_project,
)

pytestmark = pytest.mark.contract

WORKFLOW = FRAMEWORK_ROOT / "shared" / "workflow" / "self-improvement-workflow.md"
WORKFLOW_MIRROR = (
    FRAMEWORK_ROOT / ".specify" / "shared" / "workflow" / "self-improvement-workflow.md"
)
SKILL = FRAMEWORK_ROOT / "skills" / "internal" / "self-improvement" / "SKILL.md"
SKILL_MIRROR = (
    FRAMEWORK_ROOT / ".specify" / "skills" / "internal" / "self-improvement" / "SKILL.md"
)
DEFINITIONS = (
    FRAMEWORK_ROOT / "shared" / "definitions" / "self-improvement-definitions.md"
)
EVIDENCE_STEP = FRAMEWORK_ROOT / "shared" / "workflow" / "evidence-step.md"
IMPROVE_TEMPLATE = FRAMEWORK_ROOT / "templates" / "commands" / "improve.md"
DOCS_IMPROVE = FRAMEWORK_ROOT / "docs" / "reference" / "commands" / "improve.md"
ENGINE = FRAMEWORK_ROOT / "scripts" / "python" / "run-determination.py"

#: Per-tool generated copies of templates/commands/improve.md (regen source of
#: truth: `scripts/python/regen-command-copies.py`).
TOOL_COPIES = (
    FRAMEWORK_ROOT / ".claude" / "commands" / "speckit.improve.md",
    FRAMEWORK_ROOT / ".github" / "prompts" / "speckit.improve.prompt.md",
    FRAMEWORK_ROOT / ".opencode" / "command" / "speckit.improve.md",
    FRAMEWORK_ROOT / ".qoder" / "commands" / "speckit.improve.md",
)

#: The disclosure literal a custom-subject why segment must state (C-34, FR-015).
DISCLOSURE = "运行判定历史未评估"

#: The engine fail-closed reason shape, verbatim from scripts/python/
#: run-determination.py `_persist_via_memory_utils` (the engine owns the
#: literal; these surfaces quote it, they do not paraphrase it).
ENGINE_REASON_HEAD = "the memory engine's --source contract does not accept"
ENGINE_REASON_TAIL = "the record is emitted but not landed"

#: The SI-0 halt report literal for a target with no unique editable
#: definition (C-39, FR-018).
NO_UNIQUE_OWNER = "没有唯一所有者"

#: Tokens that would constitute a second observation engine / a new client
#: improver / a parallel history store (C-36/C-37) — none may exist.
SECOND_ENGINE_TOKENS = ("client-history", "client_history", "parallel-history")
CLIENT_IMPROVER_TOKENS = ("improve-client", "improve_client")

UNIT = "custom:fixture/unit"


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def read(path: Path) -> str:
    assert path.is_file(), f"missing surface: {path}"
    return path.read_text(encoding="utf-8")


def all_surfaces() -> str:
    return "\n".join(
        read(p) for p in (WORKFLOW, SKILL, IMPROVE_TEMPLATE, DOCS_IMPROVE)
    )


# --------------------------------------------------------------------------- #
# C-33 — the loop is reused, not re-created; criteria stay owned and unrelaxed
# --------------------------------------------------------------------------- #

def test_c33_loop_reuses_si0_through_si9_with_no_client_specific_flow():
    text = read(WORKFLOW)
    for step in range(10):
        assert f"### SI-{step}" in text, (
            f"C-33: the standard flow MUST keep its SI-0…SI-9 steps; "
            f"SI-{step} heading missing"
        )
    skill_text = read(SKILL)
    # The carrier delegates the step bodies to the workflow (owner path) and
    # references the steps it annotates — it never redefines them. (SI-1's
    # body is executed as the skill's Segment 1/2, so only the load-bearing
    # step anchors are pinned here.)
    assert "self-improvement-workflow.md" in skill_text, (
        "C-33: the carrier skill must reach the workflow by its owner path"
    )
    for step in ("SI-0", "SI-2", "SI-3C", "SI-4", "SI-8", "SI-9"):
        assert step in skill_text, (
            f"C-33: the loop carrier references the workflow's steps, never "
            f"replaces them; {step} unreferenced"
        )
    # No client-specific improvement flow or skill was created: no skill
    # directory claims the client loop, and the carrier is the existing
    # self-improvement skill.
    client_skills = [
        p.parent.name
        for layer in ("internal", "external")
        for p in (FRAMEWORK_ROOT / "skills" / layer).glob("*/SKILL.md")
        if "client" in p.parent.name
    ]
    assert client_skills == [], (
        f"C-33: no client-specific improvement skill may exist; "
        f"found {client_skills!r}"
    )
    # The five Execution Subject criteria are owned by the definitions file and
    # cited, never restated, by the loop surfaces (One Source Of Truth).
    definition = read(DEFINITIONS)
    for criterion in (
        "1. can be invoked repeatedly;",
        "2. owns or references an execution contract;",
        "3. produces observable run evidence;",
        "4. has one canonical editable definition;",
        "5. can route a durable change to that definition",
    ):
        assert criterion in definition, (
            f"C-33: the Execution Subject definition MUST keep its five "
            f"criteria; missing {criterion!r}"
        )
    for name, text in (("workflow", text), ("skill", skill_text)):
        assert "can be invoked repeatedly" not in text, (
            f"C-33: the {name} restates the owned criteria instead of citing "
            "the definitions file"
        )


def test_c33_five_criteria_gain_no_relaxation_for_custom_subjects():
    combined = all_surfaces()
    # No surface relaxes the criteria or grants a client-side exemption: the
    # exemption/relaxation vocabulary must not appear on any loop surface.
    for token in ("放宽", "豁免", "client-side exemption", "criteria relaxation"):
        assert token not in combined, (
            f"C-33: {token!r} would relax the Execution Subject criteria or "
            "grant a client-side exemption"
        )
    # SI-0 still applies the criteria verbatim to every subject, custom
    # subjects included — no custom carve-out inside the SI-0 body.
    si0 = read(WORKFLOW).split("### SI-0")[1].split("### SI-1")[0]
    assert "Verify the target satisfies the Execution Subject definition." in si0, (
        "C-33: SI-0's criteria check must stay verbatim and universal"
    )
    assert "custom:" not in si0, (
        "C-33: SI-0 must not carve out a custom-subject branch — a client "
        "artifact passes (or fails) the same five criteria"
    )


# --------------------------------------------------------------------------- #
# C-34 — fail-closed disclosure with the engine's reason, verbatim
# --------------------------------------------------------------------------- #

def test_c34_why_discloses_run_determination_history_not_evaluated():
    workflow = read(WORKFLOW)
    skill = read(SKILL)
    template = read(IMPROVE_TEMPLATE)
    docs = read(DOCS_IMPROVE)
    for name, text in (
        ("workflow SI-1", workflow),
        ("self-improvement skill", skill),
        ("improve command template", template),
        ("improve docs page", docs),
    ):
        assert DISCLOSURE in text, (
            f"C-34: the {name} MUST carry the disclosure literal "
            f"{DISCLOSURE!r} for a custom-subject why segment"
        )
    # The engine's reason is quoted verbatim (head + tail), never paraphrased —
    # the engine owns the literal.
    for name, text in (
        ("workflow SI-1", workflow),
        ("improve docs page", docs),
    ):
        assert ENGINE_REASON_HEAD in text, (
            f"C-34: the {name} MUST quote the engine fail-closed reason "
            f"verbatim (head: {ENGINE_REASON_HEAD!r})"
        )
        assert ENGINE_REASON_TAIL in text, (
            f"C-34: the {name} MUST quote the engine fail-closed reason "
            f"verbatim (tail: {ENGINE_REASON_TAIL!r})"
        )
    assert ENGINE_REASON_HEAD in skill and ENGINE_REASON_HEAD in template, (
        "C-34: the skill and the command template MUST name the engine "
        "reason shape, not an invented paraphrase"
    )


def test_c34_engine_fail_closed_for_custom_subject_is_observable_in_client():
    """Behavioural: the fail-closed report the disclosure cites is real — the
    engine returns persisted:false plus its reason for a custom unit, and the
    record lands nowhere (pins the honesty boundary the why segment quotes)."""
    with make_client_project() as project:
        project.arm(UNIT)
        before = project.status_short()
        run = project.run_engine(
            "run-determination.py", "--action", "determine",
            "--unit-id", UNIT, "--unit-type", "custom-unit",
            "--run-id", "run-custom", "--complexity", "complex",
            "--workspace-root", str(project.path), "--json",
        )
        assert run.ok, run.describe()
        payload = run.json_stdout()
        assert payload["persistence"]["persisted"] is False, (
            f"C-34: a custom subject has no legitimate persistence source; "
            f"got {payload['persistence']!r}"
        )
        reason = payload["persistence"]["reason"]
        assert "--source contract does not accept" in reason, (
            f"C-34: the engine reason must name the source contract; "
            f"got {reason!r}"
        )
        assert payload["record"]["unit_type"] == "custom-unit"
        assert payload["record"]["unit_id"] == UNIT
        # Honest instead of dropping: the record is emitted (payload) but not
        # landed — the client store/session trees gain no file.
        assert project.status_short() == before, (
            "C-34: a fail-closed determination must not write into the "
            "client project"
        )
        session_dir = project.path / ".specify" / "memory" / "session"
        landed = list(session_dir.glob("*run-determination*")) if session_dir.is_dir() else []
        assert landed == [], (
            f"C-34: the fail-closed record must not land in the session "
            f"store; found {landed!r}"
        )


# --------------------------------------------------------------------------- #
# C-35 — observation source: client channel entries + existing evidence lanes
# --------------------------------------------------------------------------- #

def test_c35_observation_source_is_client_channel_plus_existing_lanes():
    workflow = read(WORKFLOW)
    skill = read(SKILL)
    template = read(IMPROVE_TEMPLATE)
    for name, text in (
        ("workflow SI-1", workflow),
        ("self-improvement skill", skill),
        ("improve command template", template),
    ):
        assert "kind: external" in text, (
            f"C-35: the {name} MUST name the client channel observation "
            "source — this unit's `kind: external` entries"
        )
        assert "evidence-step.md" in text, (
            f"C-35: the {name} MUST reach the existing evidence lanes by "
            "their owner path, never restate them"
        )
    # The existing evidence lanes owner is untouched and still owns its lanes.
    evidence = read(EVIDENCE_STEP)
    assert "Step A" in evidence and "Step B" in evidence, (
        "C-35: the existing evidence lanes stay owned by evidence-step.md"
    )
    # No invented source string: the custom-subject rule must not redirect the
    # why segment at the run-determination history action (the engine that has
    # no legitimate source for custom units) nor at any new store.
    si1 = workflow.split("### SI-1")[1].split("### SI-2")[0]
    custom_rule = si1.split("custom:")[-1]
    assert "--action history" not in custom_rule, (
        "C-35: the custom-subject observation rule must not cite the "
        "run-determination history action as its source"
    )
    for token in SECOND_ENGINE_TOKENS:
        for name, text in (
            ("workflow", workflow), ("skill", skill),
            ("template", template), ("docs", read(DOCS_IMPROVE)),
        ):
            assert token not in text, (
                f"C-35/C-36: {token!r} in the {name} would be an invented "
                "observation source"
            )
    # "No history" is never phrased as "past runs were fine" — the honesty
    # sentence is stated, not implied.
    for name, text in (
        ("workflow SI-1", si1),
        ("self-improvement skill", skill),
    ):
        assert '"past runs were fine"' in text or "past runs were fine" in text, (
            f"C-35: the {name} MUST state the rule that 'no history' is "
            "never phrased as 'past runs were fine'"
        )


# --------------------------------------------------------------------------- #
# C-36 — no parallel history store, no second observation engine
# --------------------------------------------------------------------------- #

def test_c36_engine_source_contract_not_widened_and_no_second_observer():
    source = read(ENGINE)
    # The fail-closed block is intact — the source contract was not widened
    # (widening is the engine owner's action, outside this feature).
    assert "the memory engine's --source contract does not accept" in source, (
        "C-36: the engine's fail-closed source contract must stay verbatim"
    )
    # Exactly one persistence adapter, the pre-existing memory-utils seam —
    # no client-side parallel history adapter was bolted on.
    m = re.search(r"PERSISTENCE_ADAPTERS = \{([^}]*)\}", source)
    assert m, "the engine keeps an explicit PERSISTENCE_ADAPTERS table"
    assert m.group(1).strip() == '"memory-utils-session": _persist_via_memory_utils', (
        f"C-36: exactly one persistence adapter may exist; found {m.group(1)!r}"
    )
    # No second observation engine was added under scripts/python/ by this
    # feature: the run-determination / history / observation engine roster is
    # the pre-existing one (roster size pinned by other contract families).
    new_engines = [
        p.name for p in (FRAMEWORK_ROOT / "scripts" / "python").glob("*.py")
        if re.search(r"client.*(history|loop|observe)|(history|observe).*client",
                     p.name, re.I)
    ]
    assert new_engines == [], (
        f"C-36: no client history/observation engine may be created; "
        f"found {new_engines!r}"
    )
    # No parallel history store directory materialised in the runtime memory.
    memory = FRAMEWORK_ROOT / ".specify" / "memory"
    parallel_stores = [
        d.name for d in memory.iterdir() if d.is_dir()
        and re.search(r"history|observ", d.name) and d.name != "history"
    ]
    assert parallel_stores == [], (
        f"C-36: no parallel history store may exist under .specify/memory/; "
        f"found {parallel_stores!r}"
    )
    # The skill keeps its "no second store" constraint verbatim.
    assert "No new machinery" in read(SKILL), (
        "C-36: the carrier skill's no-second-store constraint stays in force"
    )


# --------------------------------------------------------------------------- #
# C-37 — how segment: existing dispatch table, degrade path, no client improver
# --------------------------------------------------------------------------- #

def test_c37_how_routes_existing_dispatch_table_with_no_client_improver():
    template = read(IMPROVE_TEMPLATE)
    # The dispatch table still names exactly the four existing improvers plus
    # the pending command row — no client improver was added.
    for improver in ("improve-agent", "improve-skills", "improve-tools",
                     "improve-team"):
        assert improver in template, (
            f"C-37: the dispatch table MUST keep routing to {improver}"
        )
    combined = all_surfaces()
    for token in CLIENT_IMPROVER_TOKENS:
        assert token not in combined, (
            f"C-37: {token!r} would be a new improver for client subjects — "
            "the how segment adds no improver"
        )
    # A custom target routes by what the artifact actually is, and degrades to
    # Assisted Improvement when no route fits (existing closing sentence).
    assert "routes by what the artifact actually is" in template, (
        "C-37: a custom target keeps the route-by-identity rule"
    )
    assert "degrade to **Assisted Improvement**" in template, (
        "C-37: the degrade-to-assisted path stays in force for subjects "
        "without a matching improver"
    )
    # The command never mutates a subject directly.
    assert "The command does not mutate a subject itself" in template, (
        "C-37: the command's no-direct-mutation rule stays verbatim"
    )
    assert "The skill does not mutate a subject itself" in read(SKILL), (
        "C-37: the carrier skill's no-direct-mutation rule stays verbatim"
    )


# --------------------------------------------------------------------------- #
# C-38 — the four loop constraints preserved verbatim
# --------------------------------------------------------------------------- #

def test_c38_falsification_attempt_ledger_hard_limit_outcome_pending():
    workflow = read(WORKFLOW)
    skill = read(SKILL)
    # 1. One executed falsification attempt before every dispatch.
    assert "one falsification attempt, executed before routing" in workflow, (
        "C-38: the falsification-attempt-before-dispatch rule stays verbatim"
    )
    assert "one executed 证伪尝试 (falsification attempt)" in skill, (
        "C-38: the carrier skill keeps the executed-attempt gate"
    )
    # 2. Exactly one intervention ledger — the Step-E ledger, no second store.
    assert "do not create a parallel self-improvement database" in workflow, (
        "C-38: the workflow keeps its single-ledger rule"
    )
    assert "The ledger is the only intervention record" in skill, (
        "C-38: exactly one intervention ledger, kept beside the baseline "
        "evidence run"
    )
    # 3. The attempt limit remains a hard limit that stops the loop.
    assert "Attempt limit reached" in workflow, (
        "C-38: the failure table keeps the attempt-limit row"
    )
    assert "Attempt limit is hard" in skill, (
        "C-38: the attempt limit is a hard limit demanding human intervention"
    )
    # 4. Outcome reported pending until comparison completes — never "improved".
    assert "intervention applied; outcome pending" in workflow, (
        "C-38: a passing check supports only 'intervention applied; outcome "
        "pending'"
    )
    assert "outcome pending" in skill.lower() and "improved" in skill.lower(), (
        "C-38: the skill reports outcome pending until SI-8"
    )
    assert "no aggregate score over the axes" in skill, (
        "C-38: no aggregate score is added over the run-determination axes"
    )


# --------------------------------------------------------------------------- #
# C-39 — no unique editable definition: halt at SI-0, mutate nothing
# --------------------------------------------------------------------------- #

def test_c39_no_unique_editable_definition_halts_at_si0_with_named_report():
    workflow = read(WORKFLOW)
    template = read(IMPROVE_TEMPLATE)
    docs = read(DOCS_IMPROVE)
    # The halt lives at subject resolution (SI-0 / the Entry Contract).
    assert "No completed execution or no canonical owner means no Self-Improvement loop" in workflow, (
        "C-39: the Entry Contract keeps the no-canonical-owner halt"
    )
    assert "No canonical owner" in workflow and "Stop mutation; resolve ownership" in workflow, (
        "C-39: the failure table keeps 'No canonical owner → stop mutation'"
    )
    assert "record the observation for later" in workflow, (
        "C-39: the observation is left for a follow-up carrier"
    )
    # The report names the literal 「没有唯一所有者」 on the command face and
    # its docs page.
    for name, text in (("improve command template", template),
                       ("improve docs page", docs)):
        assert NO_UNIQUE_OWNER in text, (
            f"C-39: the {name} MUST report the halt with the literal "
            f"{NO_UNIQUE_OWNER!r}"
        )
    # No ownership assumption, no mutation.
    assert "stop without mutating anything" in template, (
        "C-39: the template keeps 'stop without mutating anything'"
    )
    assert "assumes no ownership" in docs or "never assumes ownership" in docs, (
        "C-39: the docs page states that no ownership is assumed"
    )


def test_c39_resolution_failure_mutates_nothing_in_the_client_project():
    """Behavioural: resolving a custom unit that has no probe object and no
    canonical owner produces observations only — every engine read is
    read-only and the working tree stays clean (the deterministic half of the
    SI-0 halt; the LLM-side halt wording is pinned structurally above)."""
    with make_client_project() as project:
        project.disarm_all()
        before = project.status_short()
        history = project.run_engine(
            "run-determination.py", "--action", "history",
            "--target", UNIT, "--json",
            "--workspace-root", str(project.path),
        )
        assert history.ok, history.describe()
        payload = history.json_stdout()
        assert int(payload["counts"]["total"]) == 0, (
            "C-39: a custom unit with no persistence source reads back an "
            f"empty history, never a fabricated one: {payload!r}"
        )
        probes = project.probe_registry_json()
        assert project.external_probe_count() == 0
        # The fixture's runtime files are installed uncommitted, so the tree
        # is not clean by construction — the pin is that resolution adds
        # nothing: the status snapshot is byte-identical before and after.
        assert project.status_short() == before, (
            "C-39: subject resolution mutates no file in the client project"
        )


# --------------------------------------------------------------------------- #
# T017/T018 — the edited surfaces stay mirrored and mutually consistent
# --------------------------------------------------------------------------- #

def test_t017_t018_mirror_isomorphism_for_the_edited_surfaces():
    assert WORKFLOW_MIRROR.read_bytes() == WORKFLOW.read_bytes(), (
        "T017: .specify/shared/workflow/self-improvement-workflow.md must be "
        "re-synced from the canonical source"
    )
    assert SKILL_MIRROR.read_bytes() == SKILL.read_bytes(), (
        "T018: .specify/skills/internal/self-improvement/SKILL.md must be "
        "re-synced from the canonical source"
    )


def test_t018_improve_docs_template_and_tool_copies_aligned():
    assert DOCS_IMPROVE.is_file(), (
        "T018: docs/reference/commands/improve.md is a plan-declared sync "
        "surface and must exist"
    )
    template = read(IMPROVE_TEMPLATE)
    docs = read(DOCS_IMPROVE)
    # The docs page and the template agree on the custom-subject why rule.
    for name, text in (("template", template), ("docs page", docs)):
        assert "kind: external" in text, (
            f"T018: the {name} names the client-channel observation source"
        )
        assert "evidence-step.md" in text or "evidence lanes" in text, (
            f"T018: the {name} points at the existing evidence lanes owner"
        )
    # The template's $ARGUMENTS target table still carries the custom: form.
    assert "custom:<owner>/<name>" in template, (
        "T018: the target table keeps the custom:<owner>/<name> form"
    )
    # Every generated per-tool copy carries the same client-observation
    # pointer (mirrors are generated, never hand-edited).
    for copy in TOOL_COPIES:
        text = read(copy)
        assert DISCLOSURE in text, (
            f"T018: generated copy {copy.name} drifted — missing the "
            f"disclosure literal {DISCLOSURE!r}; regenerate with "
            "regen-command-copies.py"
        )
