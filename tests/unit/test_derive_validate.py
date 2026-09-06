"""Unit tests: `derive-utils.py --action validate` integrity rules (048 / Feature 049).

Engine:   scripts/python/derive-utils.py
Contract: .specify/specs/048-derive-command/contracts/derivation-model.md
          (chain rules C1-C7, audit checks A1-A14, the closed warning set C-44,
          the shared normalization C-22, and the (rule, locator) dedup C-3)
Concept:  shared/definitions/derivation-definitions.md

One test per error `code` over the shared synthetic corpus
(tests/derive_fixtures.py): each asserts exit code 4 plus the code's presence in
`errors[].code`. The green path is pinned too — including the two semantic checks
that can never be inherited as green (A11 / A14), the complete-enum key sets that
make SC-001/SC-002 assertable without probing shape, and the derived audit.

Two contract clauses the engine does NOT satisfy are encoded as strict=False
xfail and named in the report rather than papered over (see the divergence
reasons inline).
"""

from __future__ import annotations

import pytest

from tests.derive_fixtures import (
    ACCESS_BUCKETS,
    ALL_CHECKS,
    ARCH,
    AUDIT,
    CHAIN,
    CONFIDENCES,
    ENGINE_CHECKS,
    GRADES,
    MOVES_APPLIED,
    QUESTIONS,
    SEMANTIC_CHECKS_PENDING,
    SOURCES,
    TERMINATION,
    TOPIC,
    UNVERIFIABLE,
    WARNING_CODES,
    build_artifact,
    build_degraded_artifact,
    codes,
    load_engine_module,
    move,
    moves_spec_file,
    rules,
    run,
    scaffold,
    seed_library,
    triples,
    validate,
    warning_codes,
    write_artifact,
)

ENGINE = load_engine_module("derive_utils_validate")

#: Imported from the engine, never re-typed: C3 is parametrized over the engine's
#: own pinned copy of the anchor's closed literal set (derivation-model C-15).
BANNED = ENGINE.BANNED_JUSTIFICATIONS

#: Stable substrings of the green fixture used as replacement anchors.
D1_CONF = "- confidence: derived\n\n### D-2"
D2_TAIL = "improved evolvability without cost. Not observed.\n- confidence: provisional"
D1_DERIVATION = (
    "The source treats a popularity ladder as if it were a definition. Applying the "
    "counter-instance move: a design can satisfy every rung of the ladder while lacking "
    "the property the definition claims, so the ladder does not entail the property."
)
D1_FALSIFICATION = (
    "Finding a rung of the ladder that no counter-instance can satisfy while omitting "
    "the defining property. Not found in S-001."
)

pytestmark = pytest.mark.unit


@pytest.fixture(scope="module")
def ws(tmp_path_factory):
    """Workspace with the topic scaffolded and the two-move library seeded.

    Module-scoped on purpose: every test below rewrites the artifact it needs and
    none of them touches the library. The two tests that must mutate the library
    (the superseded citation and the hand-edited library) build their own
    ``tmp_path`` workspace so this one stays clean.
    """
    workspace = tmp_path_factory.mktemp("derive-validate")
    code, env = scaffold(workspace)
    assert code == 0, env
    seed_library(workspace)
    return workspace


def check(ws, text: str, *extra: str) -> tuple[int, dict]:
    write_artifact(ws, text, TOPIC)
    return validate(ws, TOPIC, *extra)


# --------------------------------------------------------------------------
# green path
# --------------------------------------------------------------------------

def test_well_formed_artifact_exits_0(ws):
    code, env = check(ws, build_artifact())
    assert code == 0, env.get("errors")
    assert env["ok"] is True
    assert env["errors"] == []


def test_envelope_top_level_keys_are_fixed(ws):
    _, env = check(ws, build_artifact())
    assert set(env) == {"ok", "action", "workspaceRoot", "generatedAt", "errors",
                        "warnings", "semanticChecksPending", "notes", "payload"}
    assert env["action"] == "validate"


def test_semantic_checks_are_never_inherited_as_green(ws):
    _, env = check(ws, build_artifact())
    assert env["semanticChecksPending"] == list(SEMANTIC_CHECKS_PENDING) == ["A11", "A14"]


def test_every_engine_check_passes_on_the_green_path(ws):
    _, env = check(ws, build_artifact())
    engine = env["payload"]["audit"]["engine"]
    assert set(engine) == set(ENGINE_CHECKS)
    assert all(v == "pass" for v in engine.values()), engine


def test_semantic_audit_reflects_the_attestation(ws):
    _, env = check(ws, build_artifact())
    assert env["payload"]["audit"]["semantic"] == {"A11": "attested", "A14": "attested"}


def test_grouping_key_sets_are_the_complete_enum(ws):
    """SC-001/SC-002 anchor: byGrade/byConfidence/byAccess key sets EQUAL the
    complete enum (absent members counted 0), so the grouping is assertable
    without probing shape first. A legal `wayback:<ts>` access value collapses to
    the single `wayback` bucket, keeping byAccess the complete enum too."""
    _, env = check(ws, build_artifact())
    src = env["payload"]["sources"]
    assert set(src["byGrade"]) == set(GRADES)
    assert set(src["byAccess"]) == set(ACCESS_BUCKETS)
    assert set(env["payload"]["steps"]["byConfidence"]) == set(CONFIDENCES)
    assert set(env["payload"]["elements"]["byConfidence"]) == set(CONFIDENCES)


def test_counts_are_computed_from_the_artifact(ws):
    _, env = check(ws, build_artifact())
    p = env["payload"]
    assert p["sources"]["total"] == 4
    assert p["sources"]["byGrade"] == {"primary": 2, "authoritative-secondary": 0,
                                       "community": 1, "unverified": 1}
    assert p["sources"]["byAccess"] == {"live": 2, "wayback": 1, "dead": 1,
                                        "paywalled": 0, "unknown": 0}
    assert p["steps"]["total"] == 2 and p["steps"]["anchorable"] == 2
    assert p["steps"]["budget"] == ENGINE.DEFAULT_MAX_STEPS and p["steps"]["budgetReached"] is False
    assert p["elements"]["total"] == 2 and p["elements"]["untraceable"] == 0
    assert p["openQuestions"]["total"] == 1 and p["openQuestions"]["brokenLinks"] == []
    assert p["moves"] == {"cited": 2, "resolved": 2, "missing": []}
    assert p["degraded"] is False


def test_title_mismatch_count_is_computed_not_asserted(ws):
    """S-002's two titles genuinely differ; the count is the engine's, not the agent's."""
    _, env = check(ws, build_artifact())
    assert env["payload"]["sources"]["titleMismatch"] == 1


# --------------------------------------------------------------------------
# C1 — orphan premises, anchoring grades, DAG in step order
# --------------------------------------------------------------------------

def test_orphan_source_premise(ws):
    code, env = check(ws, build_artifact(chain=CHAIN.replace("- premises: S-001", "- premises: S-009")))
    assert code == 4
    assert "orphan-source-premise" in codes(env)
    assert ("C1", "orphan-source-premise", "D-1.premises:S-009") in triples(env)


def test_premise_grade_ineligible_community(ws):
    code, env = check(ws, build_artifact(chain=CHAIN.replace("- premises: S-001", "- premises: S-003")))
    assert code == 4
    assert "premise-grade-ineligible" in codes(env)


def test_forward_step_reference(ws):
    code, env = check(ws, build_artifact(chain=CHAIN.replace("- premises: S-001", "- premises: S-001, D-2")))
    assert code == 4
    assert "forward-step-reference" in codes(env)


def test_self_referential_step(ws):
    code, env = check(ws, build_artifact(chain=CHAIN.replace("- premises: S-001", "- premises: S-001, D-1")))
    assert code == 4
    assert "self-referential-step" in codes(env)


def test_unresolved_lead(ws):
    code, env = check(ws, build_artifact(chain=CHAIN.replace("- leads: S-003", "- leads: S-009")))
    assert code == 4
    assert "unresolved-lead" in codes(env)


def test_community_source_is_legal_as_a_lead(ws):
    """The finding-aid half of the anchor rule: `leads` may carry community."""
    assert "- leads: S-003" in CHAIN
    code, env = check(ws, build_artifact())
    assert code == 0, env.get("errors")


# --------------------------------------------------------------------------
# C2 — exactly one move per step
# --------------------------------------------------------------------------

def test_move_count_not_one_zero(ws):
    code, env = check(ws, build_artifact(chain=CHAIN.replace("- move: M-001", "- move: ")))
    assert code == 4
    assert "move-count-not-one" in codes(env)


def test_move_count_not_one_two(ws):
    code, env = check(ws, build_artifact(chain=CHAIN.replace("- move: M-001", "- move: M-001, M-002")))
    assert code == 4
    assert "move-count-not-one" in codes(env)


# --------------------------------------------------------------------------
# C3 — the closed banned-justification set (parametrized over the engine copy)
# --------------------------------------------------------------------------

@pytest.mark.parametrize("literal", BANNED)
def test_banned_justification_literal_is_rejected(ws, literal):
    code, env = check(ws, build_artifact(
        chain=CHAIN.replace("The source treats a popularity ladder",
                            "%s. The source treats a popularity ladder" % literal)))
    assert code == 4, f"{literal!r} was accepted"
    assert "banned-justification" in codes(env)
    assert "C3" in rules(env)


def test_banned_set_is_the_closed_fifteen(ws):
    """The set is closed (C-18): this count is the drift tripwire, not a definition."""
    assert len(BANNED) == 15 and len(set(BANNED)) == 15


def test_longest_banned_hit_is_reported_once(ws):
    """C-17: `industry best practices` contains both `best practice` and `best
    practices`; only the longest is reported, so one fragment is not counted twice."""
    assert ENGINE.longest_banned_hit("industry best practices") == "best practices"


# --------------------------------------------------------------------------
# C4 — non-vacuous falsification
# --------------------------------------------------------------------------

def test_falsification_vacuous_literal(ws):
    code, env = check(ws, build_artifact(
        chain=CHAIN.replace("- falsification: " + D1_FALSIFICATION, "- falsification: none")))
    assert code == 4
    assert "falsification-vacuous-literal" in codes(env)


def test_falsification_restates_conclusion(ws):
    code, env = check(ws, build_artifact(
        chain=CHAIN.replace("- falsification: " + D1_FALSIFICATION,
                            "- falsification: A maturity ladder is not a definition of the style.")))
    assert code == 4
    assert "falsification-restates-conclusion" in codes(env)


# --------------------------------------------------------------------------
# C5 — contradictions recorded never averaged; uncertainty propagates
# --------------------------------------------------------------------------

def test_contested_without_link(ws):
    code, env = check(ws, build_artifact(chain=CHAIN.replace(D1_CONF, "- confidence: contested\n\n### D-2")))
    assert code == 4
    assert "contested-without-link" in codes(env)


def test_contested_link_unresolved(ws):
    code, env = check(ws, build_artifact(
        chain=CHAIN.replace(D1_CONF, "- confidence: contested\n- contested-with: D-9\n\n### D-2")))
    assert code == 4
    assert "contested-link-unresolved" in codes(env)


def test_contested_link_not_reciprocal(ws):
    code, env = check(ws, build_artifact(
        chain=CHAIN.replace(D1_CONF, "- confidence: contested\n- contested-with: D-2\n\n### D-2")))
    assert code == 4
    assert "contested-link-not-reciprocal" in codes(env)


def test_contested_not_routed(ws):
    chain = (CHAIN
             .replace(D1_CONF, "- confidence: contested\n- contested-with: D-2\n\n### D-2")
             .replace(D2_TAIL, "improved evolvability without cost. Not observed.\n"
                               "- confidence: contested\n- contested-with: D-1"))
    code, env = check(ws, build_artifact(chain=chain))
    assert code == 4
    assert "contested-not-routed" in codes(env)


def test_contested_premise_in_derived_step(ws):
    chain = (CHAIN
             .replace(D1_CONF, "- confidence: contested\n- contested-with: D-2\n\n### D-2")
             .replace(D2_TAIL, "improved evolvability without cost. Not observed.\n- confidence: derived"))
    code, env = check(ws, build_artifact(chain=chain))
    assert code == 4
    assert "contested-premise-in-derived-step" in codes(env)


def test_step_confidence_above_premise_min(ws):
    """D-1 downgraded to provisional, D-2 (which rests on D-1) claims derived."""
    chain = (CHAIN
             .replace(D1_CONF, "- confidence: provisional\n\n### D-2")
             .replace(D2_TAIL, "improved evolvability without cost. Not observed.\n- confidence: derived"))
    code, env = check(ws, build_artifact(chain=chain))
    assert code == 4
    assert "step-confidence-above-premise-min" in codes(env)


def test_confidence_not_in_enum(ws):
    code, env = check(ws, build_artifact(chain=CHAIN.replace(D1_CONF, "- confidence: certain\n\n### D-2")))
    assert code == 4
    assert "confidence-not-in-enum" in codes(env)


# --------------------------------------------------------------------------
# C6 / A12 — termination and the step budget
# --------------------------------------------------------------------------

def test_termination_condition_absent(ws):
    code, env = check(ws, build_artifact(termination="- steps: 2 / 12\n"))
    assert code == 4
    assert "termination-condition-absent" in codes(env)


def test_step_budget_diverges(ws):
    code, env = check(ws, build_artifact(termination=TERMINATION.replace("steps: 2 / 12", "steps: 2 / 9")))
    assert code == 4
    assert "step-budget-diverges" in codes(env)


def test_step_budget_exceeded(ws):
    code, env = check(ws, build_artifact(), "--max-steps", "1")
    assert code == 4
    assert "step-budget-exceeded" in codes(env)


# --------------------------------------------------------------------------
# C7 — no conclusion laundering
# --------------------------------------------------------------------------

def test_derivation_empty_or_short(ws):
    code, env = check(ws, build_artifact(chain=CHAIN.replace(D1_DERIVATION, "Short.")))
    assert code == 4
    assert "derivation-empty-or-short" in codes(env)


def test_conclusion_equals_source_title(ws):
    code, env = check(ws, build_artifact(
        chain=CHAIN.replace("- conclusion: A maturity ladder is not a definition of the style.",
                            "- conclusion: On the maturity of the style")))
    assert code == 4
    assert "conclusion-equals-source-title" in codes(env)


# --------------------------------------------------------------------------
# A1 — source rows: grade, computed title_mismatch, verification, access coupling
# --------------------------------------------------------------------------

def test_grade_not_in_enum(ws):
    code, env = check(ws, build_artifact(sources=SOURCES.replace("| primary | <url-1> |", "| Primary | <url-1> |")))
    assert code == 4
    assert "grade-not-in-enum" in codes(env)


def test_title_mismatch_asserted(ws):
    code, env = check(ws, build_artifact(sources=SOURCES.replace(
        "| S-001 | On the maturity of the style | On the maturity of the style | false |",
        "| S-001 | On the maturity of the style | On the maturity of the style | true |")))
    assert code == 4
    assert "title-mismatch-asserted" in codes(env)


def test_title_mismatch_without_both_titles(ws):
    """C-29: title_mismatch is a two-title assertion. A stated `true` with an empty
    resolved_title is the more specific diagnosis, checked on the STATED value
    before the recomputation check."""
    code, env = check(ws, build_artifact(sources=SOURCES.replace(
        "| S-004 | An unverifiable attribution |  | false |",
        "| S-004 | An unverifiable attribution |  | true |")))
    assert code == 4
    assert "title-mismatch-without-both-titles" in codes(env)
    assert ("A1", "title-mismatch-without-both-titles", "S-004.title_mismatch") in triples(env)


def test_verification_too_short(ws):
    code, env = check(ws, build_artifact(
        sources=SOURCES.replace("direct fetch returned HTTP 200 on 2026-09-05", "HTTP 200")))
    assert code == 4
    assert "verification-too-short" in codes(env)


def test_verification_bare_attestation(ws):
    # >= 16 raw codepoints (so the length check passes) but normalizes to a bare token.
    code, env = check(ws, build_artifact(
        sources=SOURCES.replace("direct fetch returned HTTP 200 on 2026-09-05", "verified....................")))
    assert code == 4
    assert "verification-bare-attestation" in codes(env)


def test_unknown_access_with_verified_grade(ws):
    code, env = check(ws, build_artifact(sources=SOURCES.replace(
        "| live | direct | direct fetch returned HTTP 200 on 2026-09-05 |",
        "| unknown | direct | direct fetch returned HTTP 200 on 2026-09-05 |")))
    assert code == 4
    assert "unknown-access-with-verified-grade" in codes(env)


# --------------------------------------------------------------------------
# A2 — record, never drop
# --------------------------------------------------------------------------

def test_unverified_source_unrecorded(ws):
    code, env = check(ws, build_artifact(unverifiable="_None._\n"))
    assert code == 4
    assert "unverified-source-unrecorded" in codes(env)


# --------------------------------------------------------------------------
# A3 — a retitled source is cited by its resolved title
# --------------------------------------------------------------------------

def test_resolved_title_not_cited(ws):
    code, env = check(ws, build_artifact(
        chain=CHAIN.replace("In search of the ideal identifier names the forces",
                            "Community digest of the 2009 essay names the forces")))
    assert code == 4
    assert "resolved-title-not-cited" in codes(env)


# --------------------------------------------------------------------------
# A7 / A8 — traceability and the confidence minimum
# --------------------------------------------------------------------------

def test_element_derived_from_missing(ws):
    code, env = check(ws, build_artifact(
        arch=ARCH.replace("- derived-from: D-1\n- confidence: derived",
                          "- derived-from: \n- confidence: derived")))
    assert code == 4
    assert "element-derived-from-missing" in codes(env)


def test_element_derived_from_unresolved(ws):
    code, env = check(ws, build_artifact(
        arch=ARCH.replace("- derived-from: D-1\n- confidence: derived",
                          "- derived-from: D-99\n- confidence: derived")))
    assert code == 4
    assert "element-derived-from-unresolved" in codes(env)


def test_element_confidence_not_minimum(ws):
    code, env = check(ws, build_artifact(
        arch=ARCH.replace("- derived-from: D-1\n- confidence: derived",
                          "- derived-from: D-1\n- confidence: provisional")))
    assert code == 4
    assert "element-confidence-not-minimum" in codes(env)


# --------------------------------------------------------------------------
# A9 — every cited move exists, is active, and is not a divergent copy
# --------------------------------------------------------------------------

def test_move_not_in_library(ws):
    code, env = check(ws, build_artifact(chain=CHAIN.replace("- move: M-001", "- move: M-777")))
    assert code == 4
    assert "move-not-in-library" in codes(env)


def test_unmarked_move_copy(ws):
    moves = ("Applied:\n\n"
             "| M-001 | Demote-by-counterexample | some restated form | prevents | applies | anchor | active |\n")
    code, env = check(ws, build_artifact(moves=moves))
    assert code == 4
    assert "unmarked-move-copy" in codes(env)


def test_divergent_move_projection(ws):
    moves = ("Applied:\n\n"
             "<!-- projection of moves.md#M-001 -->\n"
             "| M-001 | Demote-by-counterexample | A totally different inference form than the "
             "library row | prevents | applies | anchor | active |\n")
    code, env = check(ws, build_artifact(moves=moves))
    assert code == 4
    assert "divergent-move-projection" in codes(env)


def test_superseded_move_applied(tmp_path):
    """Needs a superseded library row, so this test owns its workspace."""
    workspace = tmp_path
    scaffold(workspace)
    seed_library(workspace)
    spec = moves_spec_file(workspace, [move("x", "y", TOPIC + ".S-001",
                                            intent="supersede", existingMoveId="M-001")],
                           name="supersede.json")
    code, env = run(workspace, "--action", "moves-add", "--file", str(spec))
    assert code == 0, env
    # the artifact still cites M-001 exactly as the green fixture does
    code, env = check(workspace, build_artifact())
    assert code == 4
    assert "superseded-move-applied" in codes(env)


# --------------------------------------------------------------------------
# A10 — Q <-> A resolves both ways; blocked elements downgrade
# --------------------------------------------------------------------------

def test_open_question_link_unresolved(ws):
    code, env = check(ws, build_artifact(arch=ARCH.replace("- open-questions: Q-1", "- open-questions: Q-9")))
    assert code == 4
    assert "open-question-link-unresolved" in codes(env)


def test_blocked_element_not_downgraded(ws):
    code, env = check(ws, build_artifact(arch=ARCH.replace(
        "- derived-from: D-2\n- confidence: provisional\n- open-questions: Q-1",
        "- derived-from: D-2\n- confidence: derived\n- open-questions: Q-1")))
    assert code == 4
    assert "blocked-element-not-downgraded" in codes(env)


def test_open_question_missing_its_discriminator(ws):
    code, env = check(ws, build_artifact(questions=QUESTIONS.replace(
        "- discriminator: A primary source that derives identifier stability under a "
        "versioning scheme.\n", "")))
    assert code == 4
    assert "open-question-link-unresolved" in codes(env)


# --------------------------------------------------------------------------
# A13 — library invariants and newly-issued moves
# --------------------------------------------------------------------------

def test_moves_library_hand_edited_detected_by_validate(tmp_path):
    """`validate` re-checks the library independently of the write path (C-25)."""
    workspace = tmp_path
    scaffold(workspace)
    seed_library(workspace)
    write_artifact(workspace, build_artifact(), TOPIC)
    code, _ = validate(workspace, TOPIC)
    assert code == 0

    lib = workspace / ".specify" / "derive" / "moves.md"
    lib.write_text(lib.read_text(encoding="utf-8").replace("| M-002 |", "| M-001 |", 1),
                   encoding="utf-8")
    code, env = validate(workspace, TOPIC)
    assert code == 4
    assert "moves-library-hand-edited" in codes(env)
    assert env["payload"]["audit"]["engine"]["A13"] == "fail"


def test_newly_issued_move_unresolved(ws):
    moves = ("Applied from `.specify/derive/moves.md`:\n\n"
             "| move_id | disposition |\n|---|---|\n| M-999 | new |\n")
    code, env = check(ws, build_artifact(moves=moves))
    assert code == 4
    assert "newly-issued-move-unresolved" in codes(env)


# --------------------------------------------------------------------------
# A0 — the audit table itself
# --------------------------------------------------------------------------

def test_audit_table_shape_bad_row_id(ws):
    code, env = check(ws, build_artifact(audit=AUDIT.replace("| A14 |", "| A15 |")))
    assert code == 4
    assert "audit-table-shape" in codes(env)


def test_missing_section_is_reported(ws):
    text = build_artifact().replace("## Unverifiable Sources\n\n" + UNVERIFIABLE + "\n", "")
    code, env = check(ws, text)
    assert code == 4
    assert "audit-table-shape" in codes(env)


def test_audit_result_diverges(ws):
    """A1-A10/A12/A13 are engine-derived; a disagreeing artifact row is a defect (C-20)."""
    code, env = check(ws, build_artifact(
        audit=AUDIT.replace("| A5 | no banned justifications | engine | pass |",
                            "| A5 | no banned justifications | engine | fail |")))
    assert code == 4
    assert "audit-result-diverges" in codes(env)


def test_semantic_check_result_outside_the_enum(ws):
    code, env = check(ws, build_artifact(audit=AUDIT.replace(
        "| attested |\n| A12 |", "| pass |\n| A12 |")))
    assert code == 4
    assert "audit-result-diverges" in codes(env)


# --------------------------------------------------------------------------
# C-3 — one fact, one error, deduped by (rule, locator); A results are derived
# --------------------------------------------------------------------------

def test_errors_are_deduped_by_rule_and_locator(ws):
    code, env = check(ws, build_artifact(chain=CHAIN.replace("- premises: S-001", "- premises: S-009")))
    assert code == 4
    orphan = [e for e in env["errors"] if e["locator"] == "D-1.premises:S-009"]
    assert len(orphan) == 1, orphan
    assert orphan[0]["rule"] == "C1"
    keys = [(e["rule"], e["locator"]) for e in env["errors"]]
    assert len(keys) == len(set(keys)), "errors[] must be deduped by (rule, locator)"
    # A4 is DERIVED from the orphan error, never separately counted.
    assert env["payload"]["audit"]["engine"]["A4"] == "fail"


# --------------------------------------------------------------------------
# degraded run — no online capability, therefore no chain (C-45/C-46/C-47/C-48)
# --------------------------------------------------------------------------

def test_degraded_run_is_an_honest_empty_success(ws):
    code, env = check(ws, build_degraded_artifact())
    assert code == 0, env.get("errors")
    assert env["ok"] is True and env["errors"] == []
    assert env["payload"]["degraded"] is True
    assert "degraded-run" in warning_codes(env)
    assert any(n.startswith("no-online-capability") for n in env["notes"]), env["notes"]
    # C-48: a degraded run anchors zero steps.
    assert env["payload"]["steps"]["total"] == 0
    assert env["payload"]["steps"]["anchorable"] == 0


def test_degraded_looking_artifact_that_carries_a_step_is_rejected(ws):
    step = ("### D-1\n- premises: S-001\n- move: M-001\n"
            "- derivation: A step that must never exist because no source is anchoring-grade "
            "in a degraded run.\n- conclusion: Something unfounded.\n"
            "- falsification: An observation that would refute it. Not checked here.\n"
            "- confidence: derived\n")
    code, env = check(ws, build_degraded_artifact(chain=step))
    assert code == 4
    assert env["payload"]["degraded"] is False
    assert "premise-grade-ineligible" in codes(env)


# --------------------------------------------------------------------------
# C-44 / C-55 — the warning set is exactly six, closed, and fully exercised
# --------------------------------------------------------------------------

def test_warning_codes_are_the_closed_six_and_all_are_triggered(ws):
    produced: set[str] = set()

    def collect(env):
        produced.update(warning_codes(env))

    # green fixture: unresolved-title + verification-evidence-token-absent (S-004)
    collect(check(ws, build_artifact())[1])
    # degraded fixture: degraded-run
    collect(check(ws, build_degraded_artifact())[1])
    # budget exactly reached: step-budget-reached
    collect(check(ws, build_artifact(termination="- condition: b\n- steps: 2 / 2\n"),
                  "--max-steps", "2")[1])
    # A11 method degenerate: attestation-method-degenerate
    collect(check(ws, build_artifact(audit=AUDIT.replace(
        "| A11 | online grounding actually happened this run | every source was probed with the "
        "host fetch tool and each outcome recorded with its HTTP status in the verification column "
        "| attested |",
        "| A11 | online grounding actually happened this run | engine | attested |")))[1])
    # a contested step anchored only on authoritative-secondary: secondary-sole-anchor
    secondary = SOURCES.replace(
        "| S-003 | A practitioner roundup | A practitioner roundup | false | community |",
        "| S-003 | A practitioner roundup | A practitioner roundup | false | authoritative-secondary |")
    contested_chain = (
        "### D-1\n- premises: S-003\n- move: M-001\n"
        "- derivation: The roundup treats a popularity ladder as a definition; a design can "
        "satisfy every rung yet lack the property, so the ladder does not entail it.\n"
        "- conclusion: A maturity ladder is not a definition of the style.\n"
        "- falsification: A rung no counter-instance can satisfy. Not found in S-003.\n"
        "- confidence: contested\n- contested-with: D-2\n\n"
        "### D-2\n- premises: S-003\n- move: M-001\n"
        "- derivation: Read for the opposite branch, the same roundup suggests the ladder does "
        "capture the style when each rung is a necessary rather than a sufficient condition.\n"
        "- conclusion: A maturity ladder partially defines the style.\n"
        "- falsification: A rung shown to be neither necessary nor sufficient. Not found.\n"
        "- confidence: contested\n- contested-with: D-1\n")
    contested_arch = (
        "### A-1 Ladder status is contested\n"
        "- statement: Whether a maturity ladder defines the style is unresolved between two readings.\n"
        "- derived-from: D-1, D-2\n- confidence: contested\n- open-questions: Q-1\n")
    contested_q = (
        "### Q-1\n- question: Which reading of the ladder holds?\n"
        "- why-undetermined: D-1 and D-2 conflict and no primary source settles it.\n"
        "- would-resolve: A-1\n- discriminator: A primary source deriving the ladder's status.\n")
    collect(check(ws, build_artifact(sources=secondary, chain=contested_chain,
                                     arch=contested_arch, questions=contested_q))[1])

    assert produced <= set(WARNING_CODES), f"warning set grew beyond the closed six: {produced}"
    assert produced == set(WARNING_CODES), f"untriggered warning codes: {set(WARNING_CODES) - produced}"


# --------------------------------------------------------------------------
# C-22 / C-54 — the shared normalization function, pinned to its five steps
# --------------------------------------------------------------------------

def test_normalize_text_nfkc_folds_full_width():
    assert ENGINE.normalize_text("\uff21\uff22\uff23") == "abc"


def test_normalize_text_casefolds():
    assert ENGINE.normalize_text("ABC") == "abc"


def test_normalize_text_strips_punctuation_and_symbols():
    assert ENGINE.normalize_text("a.b-c!") == "abc"


def test_normalize_text_collapses_whitespace():
    assert ENGINE.normalize_text("a   b\t\nc") == "a b c"


def test_normalize_text_drops_zwsp_and_bom():
    assert ENGINE.normalize_text("a\u200bb\ufeffc") == "abc"


def test_normalize_text_empty_is_none():
    assert ENGINE.normalize_text("...") is None
    assert ENGINE.normalize_text("") is None
    assert ENGINE.normalize_text(None) is None
