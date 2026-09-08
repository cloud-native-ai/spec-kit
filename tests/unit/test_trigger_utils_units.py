"""Unit tests for the proactive-trigger engine's pure functions (spec 050).

Constitution Principle IV: "Pure functions/utilities MUST have unit tests."
The engine is executable runtime code, so the template-only exemption does not
apply to it (tasks.md Tests Mode note).

These cover the deterministic core that must never be delegated to an LLM
(Program-First): situation identity resolution, vocabulary range checks, the
threshold priority chain, telemetry row shaping, the snapshot length guard,
consecutive-count arithmetic and the destructive-promotion exemption.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "scripts" / "python" / "trigger-utils.py"


def load_engine():
    assert ENGINE.is_file(), f"missing engine: {ENGINE}"
    spec = importlib.util.spec_from_file_location("_trigger_utils_units", ENGINE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def eng():
    return load_engine()


@pytest.fixture(scope="module")
def situations(eng):
    """The 13 named situations, taken from the shipped seed (not restated here)."""
    import json
    seed = json.loads(
        (ROOT / "templates" / "proactive-trigger-seed.json").read_text(encoding="utf-8")
    )
    return seed["situations"]


# --- situation identity resolution (E1 V1.5 / V1.6) ---


def test_resolve_situation_exact_match(eng, situations):
    assert eng.resolve_situation(situations, "requirements-unclear",
                                 {"needs-clarification"}) == "s01"
    assert eng.resolve_situation(situations, "requirements-draft", {"no-plan"}) == "s02"
    assert eng.resolve_situation(situations, "no-spec", {"feature-index-absent"}) == "s03"
    assert eng.resolve_situation(situations, "no-spec", {"constitution-absent"}) == "s13"


def test_resolve_situation_requires_the_stage_to_match(eng, situations):
    """V1.5: match.stage must equal --stage; signals alone never suffice."""
    assert eng.resolve_situation(situations, "planned", {"needs-clarification"}) is None
    assert eng.resolve_situation(situations, "non-feature", {"open-tasks"}) is None


def test_resolve_situation_requires_every_signals_all_member(eng, situations):
    """s05 needs both open-tasks and checklist-absent."""
    assert eng.resolve_situation(situations, "tasks-ready",
                                 {"open-tasks", "checklist-absent"}) == "s05"
    # Only one of the two -> s05 must not match; the subset situation s06 does.
    assert eng.resolve_situation(situations, "tasks-ready", {"open-tasks"}) == "s06"


def test_resolve_situation_v1_6_most_specific_wins(eng, situations):
    """Extra signals beyond the predicate must not defeat the most specific match."""
    assert eng.resolve_situation(
        situations, "tasks-ready", {"open-tasks", "checklist-absent", "no-plan"}
    ) == "s05", "the largest signalsAll cardinality must win"


def test_resolve_situation_no_match_returns_none(eng, situations):
    assert eng.resolve_situation(situations, "non-feature", set()) is None
    assert eng.resolve_situation(situations, "implementing", {"needs-clarification"}) is None


def test_resolve_situation_tie_breaks_on_lexicographic_id(eng):
    """V1.6: equal cardinality resolves to the lexicographically smallest id."""
    synthetic = [
        {"id": "s92", "name": "b", "stage": "planned", "signals": ["no-tasks"],
         "match": {"stage": "planned", "signalsAll": ["no-tasks"], "signalsAny": []}},
        {"id": "s91", "name": "a", "stage": "planned", "signals": ["no-tasks"],
         "match": {"stage": "planned", "signalsAll": ["no-tasks"], "signalsAny": []}},
    ]
    assert eng.resolve_situation(synthetic, "planned", {"no-tasks"}) == "s91"


def test_resolve_situation_signals_any_semantics(eng):
    """V1.5: a non-empty signalsAny requires at least one member present."""
    synthetic = [{
        "id": "s90", "name": "any", "stage": "planned", "signals": [],
        "match": {"stage": "planned", "signalsAll": [], "signalsAny": ["no-tasks", "no-plan"]},
    }]
    assert eng.resolve_situation(synthetic, "planned", {"no-plan"}) == "s90"
    assert eng.resolve_situation(synthetic, "planned", {"no-tasks"}) == "s90"
    assert eng.resolve_situation(synthetic, "planned", {"open-tasks"}) is None


def test_resolve_situation_is_deterministic(eng, situations):
    """Ordering of the input signal set must not change the outcome."""
    a = eng.resolve_situation(situations, "tasks-ready", {"checklist-absent", "open-tasks"})
    b = eng.resolve_situation(situations, "tasks-ready", {"open-tasks", "checklist-absent"})
    assert a == b == "s05"


# --- vocabulary range (V1.2 -> EXIT_INVALID) ---


def test_vocabulary_out_of_range_detected(eng):
    assert eng.vocabulary_violations("not-a-stage", []) == ["stage:not-a-stage"] or \
        eng.vocabulary_violations("not-a-stage", []) != []
    assert eng.vocabulary_violations("planned", ["not-a-signal"]) != []
    assert eng.vocabulary_violations("planned", ["no-tasks", "bogus"]) != []


def test_vocabulary_in_range_is_clean(eng):
    assert eng.vocabulary_violations("planned", ["no-tasks"]) == []
    assert eng.vocabulary_violations("non-feature", []) == []
    assert eng.vocabulary_violations("tasks-ready", ["open-tasks", "checklist-absent"]) == []


def test_vocabulary_covers_the_whole_enumeration(eng):
    for stage in sorted(eng.STAGES):
        assert eng.vocabulary_violations(stage, []) == [], f"{stage} wrongly rejected"
    for signal in sorted(eng.SIGNALS):
        assert eng.vocabulary_violations("non-feature", [signal]) == [], (
            f"{signal} wrongly rejected"
        )


def test_vocabulary_enumeration_sizes_are_pinned(eng):
    assert len(eng.STAGES) == 9, f"9 lifecycle stages expected, got {len(eng.STAGES)}"
    assert len(eng.SIGNALS) == 12, f"12 signals expected, got {len(eng.SIGNALS)}"


# --- threshold priority chain (V6.2 / C-18) ---


def test_threshold_explicit_wins_over_everything(eng):
    assert eng.resolve_threshold(explicit=7, env_value="9", stored=5) == 7


def test_threshold_env_beats_stored(eng):
    assert eng.resolve_threshold(explicit=None, env_value="9", stored=5) == 9


def test_threshold_stored_beats_default(eng):
    assert eng.resolve_threshold(explicit=None, env_value=None, stored=5) == 5


def test_threshold_default_is_three(eng):
    assert eng.resolve_threshold(explicit=None, env_value=None, stored=None) == 3


def test_threshold_invalid_env_is_ignored_not_fatal(eng):
    """An unusable env value downgrades to the next level instead of raising."""
    for bad in ("abc", "", "3.5", "none", "  "):
        assert eng.resolve_threshold(explicit=None, env_value=bad, stored=5) == 5, (
            f"env value {bad!r} must be ignored, falling through to the stored value"
        )
    assert eng.resolve_threshold(explicit=None, env_value="abc", stored=None) == 3


def test_threshold_env_zero_and_negative_parse_but_fail_the_floor(eng):
    assert eng.resolve_threshold(explicit=None, env_value="0", stored=5) == 0
    assert eng.resolve_threshold(explicit=None, env_value="-3", stored=5) == -3


def test_threshold_floor_is_two(eng):
    """V6.3: 0 or 1 would mean auto-executing on first sight."""
    for value in (-1, 0, 1):
        assert eng.threshold_below_floor(value) is True, f"{value} must be below the floor"
    for value in (2, 3, 10):
        assert eng.threshold_below_floor(value) is False, f"{value} must be acceptable"
    assert eng.THRESHOLD_FLOOR == 2


# --- telemetry row shaping (E4 / C-14) ---


def test_telemetry_row_has_exactly_seven_keys(eng):
    row = eng.shape_telemetry_row(
        turn_id="s1-01", escalated=False, suggested=True,
        compliance_done=True, visible_output=True, ts="2026-09-08T00:00:00Z",
    )
    assert set(row) == {
        "turnId", "assessed", "escalated", "suggested", "complianceDone",
        "visibleOutput", "ts",
    }, f"row keys: {sorted(row)}"


def test_telemetry_assessed_is_structurally_true(eng):
    """V4.5: only assess writes rows, so this records an invariant, not evidence."""
    for suggested in (True, False):
        row = eng.shape_telemetry_row(
            turn_id="s1-01", escalated=False, suggested=suggested,
            compliance_done=True, visible_output=suggested, ts="2026-09-08T00:00:00Z",
        )
        assert row["assessed"] is True


def test_telemetry_v4_2_silence_forces_no_visible_output(eng):
    """assessed and not suggested implies visibleOutput is false."""
    row = eng.shape_telemetry_row(
        turn_id="s1-01", escalated=False, suggested=False,
        compliance_done=False, visible_output=True, ts="2026-09-08T00:00:00Z",
    )
    assert row["visibleOutput"] is False, (
        "V4.2 must be enforced by the shaper, not left to the caller"
    )


def test_telemrow_types_are_json_native(eng):
    row = eng.shape_telemetry_row(
        turn_id="s1-01", escalated=True, suggested=True,
        compliance_done=True, visible_output=True, ts="2026-09-08T00:00:00Z",
    )
    assert isinstance(row["turnId"], str) and isinstance(row["ts"], str)
    for key in ("assessed", "escalated", "suggested", "complianceDone", "visibleOutput"):
        assert isinstance(row[key], bool), f"{key} must be a bool"


# --- snapshot guard (E3 V3.3) ---


def test_snapshot_within_limit_accepted(eng):
    assert eng.snapshot_ok("x" * 200) is True
    assert eng.snapshot_ok("") is True
    assert eng.snapshot_ok("short summary") is True


def test_snapshot_over_limit_rejected(eng):
    assert eng.snapshot_ok("x" * 201) is False
    assert eng.snapshot_ok("y" * 5000) is False
    assert eng.SNAPSHOT_MAX_CHARS == 200


# --- consecutive-count arithmetic (E5 V3.1 / V3.2) ---


def test_consecutive_increments_on_accepted(eng):
    assert eng.next_consecutive(0, "accepted") == 1
    assert eng.next_consecutive(1, "accepted") == 2
    assert eng.next_consecutive(2, "accepted") == 3


def test_consecutive_resets_on_declined_and_ignored(eng):
    """R2-Q3: one decline resets, and ignored behaves the same on the counter."""
    for response in ("declined", "ignored"):
        assert eng.next_consecutive(5, response) == 0
        assert eng.next_consecutive(1, response) == 0
        assert eng.next_consecutive(0, response) == 0


def test_consecutive_never_goes_negative(eng):
    for response in ("accepted", "declined", "ignored"):
        assert eng.next_consecutive(0, response) >= 0


def test_consecutive_rejects_unknown_response(eng):
    with pytest.raises((ValueError, KeyError)):
        eng.next_consecutive(0, "maybe")


# --- promotion decision and destructive exemption (V2.1 / V5.1 / V5.2 / C-17) ---


def test_promotion_requires_threshold_and_reversible(eng):
    assert eng.should_promote(consecutive=3, threshold=3, confirmation_class="reversible") is True
    assert eng.should_promote(consecutive=4, threshold=3, confirmation_class="reversible") is True


def test_promotion_below_threshold_is_false(eng):
    """V5.2: consecutive < threshold implies promoted is false."""
    for consecutive in (0, 1, 2):
        assert eng.should_promote(consecutive=consecutive, threshold=3,
                                  confirmation_class="reversible") is False


def test_destructive_is_never_promoted(eng):
    """C-17 zero tolerance: no acceptance count promotes a destructive flow."""
    for consecutive in range(0, 51):
        assert eng.should_promote(consecutive=consecutive, threshold=3,
                                  confirmation_class="destructive") is False, (
            f"destructive promoted at consecutive={consecutive}"
        )


def test_destructive_exemption_is_derived_from_the_class_only(eng):
    assert eng.is_destructive_exempt("destructive") is True
    assert eng.is_destructive_exempt("reversible") is False


def test_promotion_recomputed_after_threshold_change(eng):
    """V5.4: raising the threshold must demote what it no longer justifies."""
    assert eng.should_promote(consecutive=3, threshold=3, confirmation_class="reversible") is True
    assert eng.should_promote(consecutive=3, threshold=5, confirmation_class="reversible") is False


# --- identifier grammar (V2.5) ---


def test_identifier_regexes(eng):
    assert eng.RULE_ID_RE.match("r-001") and not eng.RULE_ID_RE.match("r-1")
    assert eng.RULE_ID_RE.match("r-013") and not eng.RULE_ID_RE.match("r-0001")
    assert eng.SITUATION_ID_RE.match("s01") and not eng.SITUATION_ID_RE.match("s1")
    assert eng.PROPOSAL_ID_RE.match("p-001") and not eng.PROPOSAL_ID_RE.match("p-1")
    assert eng.EVENT_ID_RE.match("20260908T142530Z-01")
    assert not eng.EVENT_ID_RE.match("20260908-01")
    assert eng.SESSION_ID_RE.match("s1") and eng.SESSION_ID_RE.match("s4-4")
    assert not eng.SESSION_ID_RE.match("session$")


def test_turn_id_grammar(eng):
    assert eng.turn_id_ok("s1", "s1-01") is True
    assert eng.turn_id_ok("s4-4", "s4-4-01") is True
    assert eng.turn_id_ok("s1", "s2-01") is False, "turnId must carry its session prefix"
    assert eng.turn_id_ok("s1", "s1-x") is False


# --- session suppression comparison (V6.7 / C-20) ---


def test_suppression_only_when_both_identity_and_rule_unchanged(eng):
    last = {"sessionId": "s1", "situationId": "s01", "ruleId": "r-001"}
    assert eng.is_suppressed(last, "s1", "s01", "r-001") is True
    assert eng.is_suppressed(last, "s1", "s01", "r-002") is False
    assert eng.is_suppressed(last, "s1", "s02", "r-001") is False
    assert eng.is_suppressed(last, "s2", "s01", "r-001") is False


def test_suppression_with_no_prior_suggestion(eng):
    assert eng.is_suppressed(None, "s1", "s01", "r-001") is False
    assert eng.is_suppressed({}, "s1", "s01", "r-001") is False
