"""Contract tests: pre-dispatch governance of nested SDD invocation (slice 074a, task T022).

What this pins
--------------
`contracts/hierarchy-and-authorization.md` C-9…C-16 — the anti-nesting obligation narrowed
**once**, at its existing owner site, into a decidable predicate, and the pre-dispatch probe
that enforces it without re-reading the definitions in prose.

Surface map (each clause is decided on the surface that actually carries it):

- **owner site** — `shared/definitions/subagent-definitions.md` § Dispatch-Time Governance
  Obligation: the three-condition predicate (C-9), the depth-2 chain and its three prohibitions
  (C-11), the virtual-mode prohibition (C-12), the per-member hard cap (C-13), the refusal
  record's required fields (C-14), the "blocked before dispatch" rule (C-15), and the
  no-gate / no-scheduler / no-second-registry statement (C-16).
- **probe** — `skills/internal/run-agent/SKILL.md`, anti-nesting paragraph: it calls the engine
  action `scripts/python/sdd-route.py --action authorize` and fails closed (C-10).
- **executable half** — the same engine action, exercised against the disposable target project
  of `tests/fixtures/nested_sdd.py`: the two declared halves resolve there, and a refusal carries
  the failing half, the recipient's resolved values, both source paths and the seat slug.

The four dispatch forms US3's independent test names land as: (1) an authorized SDD assignment
is allowed and its authorization basis is recorded (behavioural case below); (2) a prompt naming
a driver whose two halves do not both allow is blocked before dispatch with the failed condition
named (behavioural case + probe declaration); (3) a stage executor attempting to host a driver is
refused (owner declaration — a stage executor is a leaf); (4) an SDD attempt nested inside a
stage is refused (owner declaration — SDD-within-SDD recursion prohibited). Virtual-mode hosting
is refused on the same owner surface.

Red shape at T022 time: the owner site still carries the unqualified "loop depth is always 1"
sentence and the probe still restates the obligation in prose, so every declaration case below
fails as a **missing statement**, not as a contradictory assertion. The behavioural cases are
green at T022 time by construction — they consume the engine action task T011 landed, and they
sit here as the allowed-path anchor the narrowing must not disturb. The pre-existing-verdict case
(`test_the_pre_existing_probe_terms_still_hold`) is green at T022 time for the same reason: it is
the containment guard, not a new allowance.

Boundary: this module asserts nothing about the routing *outcome* reasoning
(`test_sdd_routing_engine.py`), nothing about the owner document's overall shape
(`test_sdd_routing_definitions.py`), and nothing about the nested run's handoff
(`test_nested_sdd_invocation.py`).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from fixtures.nested_sdd import ALLOWED, ENGINE, build

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[2]
SUBAGENT_DEFS = REPO_ROOT / "shared" / "definitions" / "subagent-definitions.md"
RUN_AGENT_SKILL = REPO_ROOT / "skills" / "internal" / "run-agent" / "SKILL.md"
ROUTING_OWNER = REPO_ROOT / "shared" / "definitions" / "sdd-routing-definitions.md"

GOV_SECTION = "Dispatch-Time Governance Obligation"

#: The probe region inside `run-agent/SKILL.md`: from the anti-nesting paragraph to the next
#: bold-lead paragraph (`**Scope boundary**`), so the region is the probe's own text and never
#: the whole skill.
PROBE_START = "Anti-nesting obligation"
PROBE_END = "**Scope boundary**"

#: C-9's first half — the three original prohibition clauses, verbatim. The narrowing may not
#: remove or reword any of them: it *adds* one allowance on top of an unchanged prohibition.
ORIGINAL_PROHIBITION = (
    "MUST NOT reference any driver/loop skill",
    "MUST NOT instruct the subagent to load any skill",
    "MUST NOT contain loop logic",
)

#: C-11's three prohibitions, verbatim from the contract. Each must appear on the owner site
#: exactly once across the framework sources (see the no-second-copy case below).
PROHIBITIONS = (
    "MUST NOT start or host any SDD run",
    "MUST NOT itself be an SDD invocation host",
    "SDD-within-SDD recursion is prohibited",
)

#: The four dispatch forms and the surface that must carry each one's decision. Form
#: ``authorized-sdd-assignment`` is decided behaviourally (the engine case below), so it is
#: named here without tokens — its presence in this table keeps the form set closed.
FORMS = (
    ("authorized-sdd-assignment", "behaviour", ()),
    ("prompt-names-a-driver", "probe", ("failed condition", "--action authorize")),
    ("stage-executor-hosts", "owner", ("stage executor", "MUST NOT start or host any SDD run")),
    ("nested-inside-a-stage", "owner", ("SDD-within-SDD",)),
)

#: Roots scanned by the no-second-copy case. Only the framework **sources**: the `.specify/`
#: projections are mirrors of them (sync is a later task in this slice), so counting there would
#: count the same sentence twice for a layout reason, not a duplication reason.
SOURCE_ROOTS = ("shared", "skills", "src")
SOURCE_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json"}


# ---------------------------------------------------------------------------
# Parsing helpers (deterministic; no prose reading)
# ---------------------------------------------------------------------------


def _read(path: Path) -> str:
    assert path.is_file(), f"missing document: {path.relative_to(REPO_ROOT)}"
    return path.read_text(encoding="utf-8")


def _heading_blocks(text: str) -> list:
    """`[(level, title, body)]` — body runs to the next heading of the same or higher level."""
    lines = text.splitlines()
    heads = [
        (index, len(line) - len(line.lstrip("#")), line.lstrip("#").strip())
        for index, line in enumerate(lines)
        if line.startswith("#")
    ]
    blocks = []
    for position, (index, level, title) in enumerate(heads):
        end = len(lines)
        for later_index, later_level, _later_title in heads[position + 1 :]:
            if later_level <= level:
                end = later_index
                break
        blocks.append((level, title, "\n".join(lines[index + 1 : end])))
    return blocks


def _governance() -> str:
    """The owner site's section body — the single place the predicate may be stated."""
    hits = [
        block
        for block in _heading_blocks(_read(SUBAGENT_DEFS))
        if block[1].startswith(GOV_SECTION)
    ]
    assert len(hits) == 1, (
        f"{SUBAGENT_DEFS.relative_to(REPO_ROOT)} must carry exactly one '{GOV_SECTION}' "
        f"section, found {[hit[1] for hit in hits]}"
    )
    return hits[0][2]


def _probe() -> str:
    """The anti-nesting paragraph of the run-agent skill."""
    text = _read(RUN_AGENT_SKILL)
    assert PROBE_START in text, (
        f"{RUN_AGENT_SKILL.relative_to(REPO_ROOT)} no longer carries a {PROBE_START!r} "
        f"paragraph — the pre-dispatch probe is the operational enforcement (C-10)"
    )
    start = text.index(PROBE_START)
    tail = text[start:]
    assert PROBE_END in tail, (
        f"the {PROBE_START!r} paragraph in {RUN_AGENT_SKILL.relative_to(REPO_ROOT)} must be "
        f"closed by {PROBE_END!r}; without it the probe region cannot be delimited"
    )
    return tail[: tail.index(PROBE_END)]


def _safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return ""


def _framework_sources() -> list:
    paths = []
    for root in SOURCE_ROOTS:
        base = REPO_ROOT / root
        if not base.is_dir():
            continue
        paths.extend(
            path
            for path in sorted(base.rglob("*"))
            if path.is_file() and path.suffix in SOURCE_SUFFIXES
        )
    return paths


@pytest.fixture(autouse=True)
def _engine_present():
    """Fail on absence for the right reason: without the engine the behavioural cases would
    pass or fail for a reason unrelated to the governance predicate."""
    assert ENGINE.is_file(), (
        f"--action authorize engine is missing: {ENGINE} (delivered by task T011)"
    )


@pytest.fixture
def project(tmp_path: Path):
    """One disposable target project (block-style seats, one allowed and one refused seat)."""
    return build(tmp_path / "block", variant="block")


# ---------------------------------------------------------------------------
# C-9 — the predicate is narrowed to three conditions
# ---------------------------------------------------------------------------


def test_c9_the_predicate_narrows_to_exactly_three_conditions():
    """Only a dispatch satisfying all three conditions may name a driver (C-9).

    The three conditions are asserted by their distinguishing tokens rather than by one
    sentence: (1) the recipient Agent definition declares the capability key, (2) its seat
    policy declares the same key, (3) the assigned task is an SDD assignment. The third
    condition's definition (and its exclusion set) must be stated, because a term nobody
    defines is not decidable.
    """
    gov = _governance()
    assert "sdd-invocation" in gov, (
        "owner site must name the capability key the recipient Agent definition declares (C-9/1)"
    )
    assert "seat policy" in gov, (
        "owner site must name the seat-policy half of the predicate (C-9/2)"
    )
    assert "SDD assignment" in gov, (
        "owner site must name the third condition as a term (C-9/3)"
    )
    for excluded in ("absent", "direct", "adjudicate"):
        assert excluded in gov, (
            f"an SDD assignment's definition must exclude the {excluded!r} case, or the term "
            f"degenerates to 'any duty' (C-9)"
        )
    assert "routing" in gov and ROUTING_OWNER.name in gov, (
        "the verdict vocabulary behind 'SDD assignment' must be reached by path "
        f"(C-9): expected a reference to {ROUTING_OWNER.name} on the owner site"
    )


def test_c9_the_original_prohibition_survives_word_for_word():
    """The narrowing adds an allowance and removes no prohibition (C-9, C-15).

    The three original clauses are pinned verbatim: a rewrite that softens any of them would
    widen the allowance past the three conditioned cases.
    """
    gov = _governance()
    for clause in ORIGINAL_PROHIBITION:
        assert clause in gov, (
            f"the original prohibition clause {clause!r} is no longer stated verbatim on the "
            f"owner site — the narrowing must not remove or reword it (C-9)"
        )


def test_c9_the_exclusivity_sentence_is_replaced_by_the_predicate():
    """The unqualified "loop depth is always 1" claim is the sentence the narrowing replaces.

    Leaving it in place would state a contradiction: an unconditioned depth-1 rule beside a
    predicate that permits depth 2.
    """
    gov = _governance()
    assert "loop depth is always 1" not in gov, (
        "the owner site still carries the unqualified 'loop depth is always 1' sentence beside "
        "the narrowed predicate — the two cannot both hold (C-11)"
    )
    probe = _probe()
    assert "恒为 1" not in probe, (
        "the probe still states the unqualified '循环层级恒为 1' rule (C-11)"
    )


def test_c9_no_second_copy_of_the_prohibition_set():
    """The narrowed prohibitions are stated once, on the owner site (C-9).

    "The amendment states the predicate without moving the obligation, and no second copy of
    the predicate is created elsewhere": a second landing place is exactly what this counts.
    """
    for literal in PROHIBITIONS:
        hits = [path for path in _framework_sources() if literal in _safe_read(path)]
        assert hits == [SUBAGENT_DEFS], (
            f"the prohibition {literal!r} must be declared on exactly one source surface "
            f"({SUBAGENT_DEFS.relative_to(REPO_ROOT)}), found on "
            f"{[str(path.relative_to(REPO_ROOT)) for path in hits]} (C-9)"
        )


# ---------------------------------------------------------------------------
# C-10 — the probe calls the engine and fails closed
# ---------------------------------------------------------------------------


def test_c10_the_probe_calls_the_engine_and_fails_closed():
    """C-10: the pre-dispatch probe calls the C-8 action, refuses before dispatch, and names
    the failed condition; a caller cannot repair a refusal by rewording the prompt."""
    probe = _probe()
    assert "sdd-route.py" in probe and "--action authorize" in probe, (
        "the probe must call the engine action of C-8 rather than re-reading the definitions in "
        "prose (C-10)"
    )
    assert "fails closed" in probe or "fail-closed" in probe or "fail closed" in probe, (
        "the probe must be declared fail-closed: an unresolved or refused verdict blocks the "
        "dispatch (C-10)"
    )
    assert "failed condition" in probe, (
        "a refusal must name the condition that failed (C-10 / C-14)"
    )
    assert "cannot repair" in probe, (
        "the probe must state that rewording the prompt cannot repair a refusal, which is the "
        "property that makes the check (rather than the prompt text) authoritative (C-10)"
    )
    assert "subagent-definitions.md" in probe, (
        "the probe must reach the predicate by path instead of restating it (C-9 / C-10)"
    )


# ---------------------------------------------------------------------------
# C-11 / C-12 / C-13 — chain depth, virtual prohibition, hard cap
# ---------------------------------------------------------------------------


def test_c11_the_permitted_chain_is_depth_two_with_its_three_prohibitions():
    """C-11: team orchestrator → invoking member (driver host) → stage executor (leaf), in
    place of the unqualified depth-1 sentence, with the three prohibitions stated."""
    gov = _governance()
    assert "depth 2" in gov, "the permitted chain's depth must be stated as depth 2 (C-11)"
    for layer in ("team orchestrator", "driver host", "stage executor", "leaf"):
        assert layer in gov, f"the depth-2 chain layer {layer!r} is missing (C-11)"
    for prohibition in PROHIBITIONS:
        assert prohibition in gov, (
            f"the prohibition {prohibition!r} is missing from the owner site (C-11)"
        )


def test_c12_virtual_mode_must_not_host_a_run():
    """C-12: virtual execution occupies the orchestrating session, so it can never host."""
    gov = _governance()
    assert "virtual mode" in gov, "the virtual-mode exclusion must be stated on the owner site"
    assert "MUST NOT host an SDD run" in gov, (
        "the model must refuse virtual-mode hosting as a rule, not as a preference (C-12)"
    )
    assert "orchestrating session" in gov, (
        "the reason must be stated: virtual execution occupies the orchestrating session, so "
        "hosting a driver there collapses the outer layer into the driver (C-12)"
    )
    assert "before" in gov and "dispatch" in gov, (
        "the refusal must happen before the dispatch leaves (C-12)"
    )


def test_c13_the_per_member_cap_is_hard_and_cites_the_existing_line_mechanism():
    """C-13: one run per member, no escape, and the second-duty case resolved by the existing
    line regime rather than by a new concurrency primitive."""
    gov = _governance()
    assert "at most one SDD run at a time" in gov, (
        "the per-member cap must be stated as a hard rule (C-13)"
    )
    assert "no higher per-member cap is declarable" in gov, (
        "the cap must have no declarable escape, or it is a default rather than a cap (C-13)"
    )
    assert "existing line registry and worktree-per-write-line ownership mechanism" in gov, (
        "the second-duty case must cite the existing line registry / ownership mechanism "
        "(C-13), not an invented gate"
    )
    assert "no second concurrency primitive" in gov, (
        "the decision must state that no second concurrency primitive is introduced (C-13)"
    )


# ---------------------------------------------------------------------------
# C-14 / C-15 / C-16 — refusal record, blocking rule, no new machinery
# ---------------------------------------------------------------------------


def test_c14_a_refusal_record_names_the_condition_and_the_resolved_values():
    """C-14: a record stating only "not authorized" is non-conforming — the two halves exist
    precisely so a reader can tell a policy decision from a missing declaration."""
    gov = _governance()
    for token in ("failed condition", "resolved values", "source paths", "seat slug"):
        assert token in gov, (
            f"the refusal record's required field {token!r} is not stated (C-14)"
        )
    assert "not authorized" in gov and "non-conforming" in gov, (
        'the owner site must state that a record carrying only "not authorized" is '
        "non-conforming (C-14)"
    )


def test_c15_stage_executors_and_unqualified_prompts_are_blocked_before_dispatch():
    """C-15: stage executors cannot start a run, and every prompt naming a driver without the
    three conditions is blocked before dispatch."""
    gov = _governance()
    assert "stage executor" in gov, (
        "the stage-executor refusal must be stated on the owner site (C-15)"
    )
    assert "MUST NOT start or host any SDD run" in gov, (
        "the stage executor is a leaf: it must be stated as a rule, not as guidance (C-15)"
    )
    assert "before dispatch" in gov or "before it leaves" in gov, (
        "the blocking must be stated as happening before the dispatch leaves (C-15)"
    )


def test_c16_no_confirmation_gate_no_scheduler_no_second_registry():
    """C-16: the authorization surface's only stored state is the two declared values."""
    gov = _governance()
    for token in (
        "no additional user-confirmation step",
        "no scheduler",
        "no second registry",
        "two declared values",
    ):
        assert token in gov, f"the owner site must state {token!r} (C-16)"


# ---------------------------------------------------------------------------
# US3's independent test — the four dispatch forms
# ---------------------------------------------------------------------------


def test_the_authorized_form_is_allowed_and_its_basis_is_recorded(project):
    """Form 1 (control half): an authorized SDD assignment resolves allowed, and the record
    carries the basis a reader needs to recheck it (C-8 / C-14)."""
    rc, out, err = project.run_authorize(project.seat_allowed)
    assert rc == 0, f"--action authorize must exit 0 on a produced verdict, stderr={err!r}"
    record = json.loads(out)
    assert record["effective"] == ALLOWED and record["verdict"] == ALLOWED
    assert record["failed_half"] is None
    assert record["agent_capability"] == ALLOWED and record["seat_policy"] == ALLOWED
    assert Path(record["sources"]["agent"]).is_file(), "the agent source path must resolve"
    assert Path(record["sources"]["team"]).is_file(), "the roster source path must resolve"
    assert record["seat_slug"] == project.seat_allowed
    assert record["team_slug"] == project.team_slug


@pytest.mark.parametrize(
    "seat_attr, agent_attr, expected_half",
    [
        ("seat_forbidden", "agent_allowed", "seat"),
        ("seat_allowed", "agent_forbidden", "agent"),
        ("seat_forbidden", "agent_forbidden", "both"),
    ],
)
def test_the_prompt_forms_without_both_halves_are_refused_naming_the_half(
    project, seat_attr, agent_attr, expected_half
):
    """Form 2: a prompt naming a driver whose halves do not both allow is refused, and the
    refusal names which half failed — never a bare "not authorized" (C-9 / C-14)."""
    seat = getattr(project, seat_attr)
    agent = getattr(project, agent_attr)
    rc, out, err = project.run_authorize(seat, agent=agent)
    assert rc == 0, (
        f"a refusal is a produced verdict, not an error status (C-8 / C-28); stderr={err!r}"
    )
    record = json.loads(out)
    assert record["effective"] != ALLOWED
    assert record["failed_half"] == expected_half, (
        f"expected the {expected_half!r} half to be named, got {record['failed_half']!r}"
    )
    assert record["seat_slug"] == seat and record["team_slug"] == project.team_slug
    assert Path(record["sources"]["team"]).is_file()


def test_the_four_dispatch_forms_each_carry_their_rule():
    """US3's independent test: only the authorized SDD assignment is dispatched; the other
    three forms are refused on a surface that names the blocking rule.

    Form 1 is decided behaviourally by the two cases above, so it contributes no token here;
    it stays in the table so the form set is closed and a dropped form is visible.
    """
    surfaces = {"owner": _governance(), "probe": _probe()}
    for form, surface, tokens in FORMS:
        if surface == "behaviour":
            continue
        body = surfaces[surface]
        for token in tokens:
            assert token in body, (
                f"dispatch form {form!r} is not decidable: the {surface} surface does not "
                f"name {token!r}"
            )


# ---------------------------------------------------------------------------
# SC-004's containment half — the pre-existing verdicts must not move
# ---------------------------------------------------------------------------


def test_the_pre_existing_probe_terms_still_hold():
    """The pre-existing anti-nesting cases assert *presence* of these terms
    (`test_agent_dispatch_mechanism.py` C-6 / C-20, `test_sdd_loop_driver_skill.py` C-20).

    Re-asserting them here keeps a wording change from silently invalidating that set: the
    name-level re-run of those modules is task T025's, this case is the local guard.
    """
    gov = _governance()
    assert "反嵌套" in gov or "嵌套" in gov, "anti-nesting reference missing in the gov section"
    assert "run-agent" in gov, "the gov section must keep naming its enforcement surface"
    probe = _probe()
    assert "反嵌套" in probe or "嵌套" in probe, "anti-nesting obligation missing from the probe"
    assert "循环层级" in probe or "层级" in probe, "the hierarchy-layer statement is missing"
    assert "派发前" in probe, "pre-dispatch interception must be named"
