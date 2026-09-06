"""Unit tests: the accumulating move library (`moves-add` / `moves-list`).

Engine:   scripts/python/derive-utils.py
Contract: .specify/specs/048-derive-command/contracts/move-library.md
          (physical form §1, monotonic issuance §2, two-level dedup §3, the
          status state machine §4, projection §5, the small-file threshold §6)
Concept:  shared/definitions/derivation-definitions.md §Reasoning Move /
          §Move Library / §Projection, Not Copy

Covers monotonic project-wide identity issuance (max+1, never row-count+1, never
a reuse), two-level dedup (exact + slot-isomorphic) with its refuse-and-return-
existing-id success semantics, the four `intent` values, the qualified
`<topic-slug>.S-<nnn>` anchor form and its grow-only sorted union, hand-edit
detection through the sole writer, the two-value durable `status`, and the
projection-shaped read path with its `fullReadAllowed` threshold flip.
"""

from __future__ import annotations

import pytest

from tests.derive_fixtures import (
    MOVE_COLUMNS,
    SEED_MOVES,
    SLOT_VARIANT_FORM,
    TOPIC,
    library_ids,
    library_rows,
    library_text,
    load_engine_module,
    move,
    moves_spec_file,
    run,
    scaffold,
    triples,
)

ENGINE = load_engine_module("derive_utils_moves")

#: Qualified anchors used across the tests.
A1 = TOPIC + ".S-001"
A2 = TOPIC + ".S-002"

pytestmark = pytest.mark.unit


@pytest.fixture
def ws(tmp_path):
    code, env = scaffold(tmp_path)
    assert code == 0, env
    return tmp_path


def add(workspace, moves, name="moves.json"):
    spec = moves_spec_file(workspace, moves, name=name)
    return run(workspace, "--action", "moves-add", "--file", str(spec))


def seed(workspace, name="moves.json"):
    return add(workspace, [dict(m) for m in SEED_MOVES], name=name)


def dispositions(env):
    return {d["moveId"]: d["disposition"] for d in env["payload"]["dispositions"]}


def break_library(workspace, mutate):
    path = workspace / ".specify" / "derive" / "moves.md"
    path.write_text(mutate(library_text(workspace)), encoding="utf-8")


# --------------------------------------------------------------------------
# identity issuance — project-wide, monotonic at max+1, never reused
# --------------------------------------------------------------------------

def test_first_add_issues_m001_and_m002(ws):
    code, env = seed(ws)
    assert code == 0, env
    assert env["payload"]["issued"] == ["M-001", "M-002"]
    assert env["payload"]["appended"] == 2
    assert library_ids(ws) == ["M-001", "M-002"]


def test_ids_are_monotonic_across_sequential_adds(ws):
    seed(ws, name="a.json")
    code, env = add(ws, [move("Third-shape", "Given a queue `Q`, bound it with a budget `N`.")],
                    name="b.json")
    assert code == 0, env
    assert env["payload"]["issued"] == ["M-003"]
    assert library_ids(ws) == ["M-001", "M-002", "M-003"]


def test_add_after_a_manual_gap_issues_max_plus_one(ws):
    """Row-count+1 would re-issue M-003 here; max+1 issues M-004 (C-10)."""
    add(ws, [move("A", "Given `P` of `D`, exhibit a counter-instance.", A1),
             move("B", "Given forces `F`, derive structure `S`.", A2),
             move("C", "Given a boundary `B`, split `S` along it.", TOPIC + ".S-003")], name="a.json")
    assert library_ids(ws) == ["M-001", "M-002", "M-003"]

    path = ws / ".specify" / "derive" / "moves.md"
    kept = [line for line in library_text(ws).splitlines() if not line.startswith("| M-002 |")]
    path.write_text("\n".join(kept) + "\n", encoding="utf-8")
    assert library_ids(ws) == ["M-001", "M-003"]

    code, env = add(ws, [move("D", "Given a ledger `L`, append only entries `E`.", TOPIC + ".S-004")],
                    name="b.json")
    assert code == 0, env
    assert env["payload"]["issued"] == ["M-004"]
    assert "M-002" not in library_ids(ws), "a retired id must never be reused"
    assert library_ids(ws) == ["M-001", "M-003", "M-004"]


def test_a_superseded_row_is_never_deleted_or_renumbered(ws):
    seed(ws, name="a.json")
    code, env = add(ws, [move("Retired-shape", "Given a ladder `L`, rank items by `R`.",
                              TOPIC + ".S-003")], name="b.json")
    assert code == 0 and env["payload"]["issued"] == ["M-003"]
    before = library_rows(ws)

    code, env = add(ws, [move("x", "y", TOPIC + ".S-003", intent="supersede",
                              existingMoveId="M-003")], name="c.json")
    assert code == 0, env
    assert env["payload"]["superseded"] == 1
    # C-21: superseded is an in-place status change, never a deletion.
    assert env["payload"]["dispositions"] == [], "a persistent transition is not a disposition"

    after = library_rows(ws)
    assert len(after) == len(before), "superseding updates a row, it never removes one"
    assert [r["move_id"] for r in after] == ["M-001", "M-002", "M-003"]
    assert after[2]["status"] == "superseded"
    assert after[2]["inference_form"] == before[2]["inference_form"]


# --------------------------------------------------------------------------
# two-level dedup — refuse and return the existing id (exit 0)
# --------------------------------------------------------------------------

def test_slot_isomorphic_forms_share_a_dedup_key():
    """The dedup key is the shape, not the slot names (C-14 level 2)."""
    assert ENGINE.slot_isomorphic_key(SEED_MOVES[0]["inferenceForm"]) == \
        ENGINE.slot_isomorphic_key(SLOT_VARIANT_FORM)


def test_exact_duplicate_is_refused_and_returns_existing_id(ws):
    seed(ws, name="a.json")
    code, env = add(ws, [move("Demote-by-counterexample", SEED_MOVES[0]["inferenceForm"], A1)],
                    name="b.json")
    assert code == 0, env
    assert env["ok"] is True
    assert env["payload"]["deduped"] == 1 and env["payload"]["appended"] == 0
    assert env["payload"]["duplicates"][0]["existingMoveId"] == "M-001"
    assert library_ids(ws) == ["M-001", "M-002"], "no new row for a duplicate shape"


def test_slot_isomorphic_duplicate_is_refused_and_returns_existing_id(ws):
    seed(ws, name="a.json")
    form_before = library_rows(ws)[0]["inference_form"]
    code, env = add(ws, [move("A different name for the same shape", SLOT_VARIANT_FORM, A1)],
                    name="b.json")
    assert code == 0, env
    assert env["payload"]["deduped"] == 1 and env["payload"]["appended"] == 0
    assert env["payload"]["duplicates"][0]["existingMoveId"] == "M-001"
    assert library_ids(ws) == ["M-001", "M-002"]
    row = library_rows(ws)[0]
    assert row["name"] == SEED_MOVES[0]["name"], "the recorded move is reinforced, never forked"
    assert row["inference_form"] == form_before, "a refusal does not rewrite the library row"


def test_dedup_is_on_the_form_not_the_name(ws):
    """Same label, different shape: two good names for two shapes stay two rows (C-13)."""
    add(ws, [move("Shared-name", "Given `P` of `D`, exhibit a counter-instance.", A1)], name="a.json")
    code, env = add(ws, [move("Shared-name", "Given forces `F`, derive structure `S`.", A2)],
                    name="b.json")
    assert code == 0, env
    assert env["payload"]["appended"] == 1
    assert library_ids(ws) == ["M-001", "M-002"]


# --------------------------------------------------------------------------
# intent semantics — new / reuse / reinforce / supersede
# --------------------------------------------------------------------------

def test_intent_reuse_is_zero_write_and_reports_reused(ws):
    seed(ws, name="a.json")
    before = library_text(ws)
    code, env = add(ws, [move("x", "y", A1, intent="reuse", existingMoveId="M-001")], name="b.json")
    assert code == 0, env
    assert dispositions(env) == {"M-001": "reused"}
    assert env["payload"]["appended"] == 0
    assert library_text(ws) == before, "reuse never writes the library"


def test_intent_reinforce_needs_a_genuinely_new_anchor(ws):
    seed(ws, name="a.json")
    code, env = add(ws, [move("x", "y", A1, intent="reinforce", existingMoveId="M-001")], name="b.json")
    assert code == 2, env
    assert env["errors"][0]["code"] == "reinforce-without-new-anchor"


def test_intent_reinforce_with_a_new_anchor_grows_the_union(ws):
    seed(ws, name="a.json")
    code, env = add(ws, [move("x", "y", TOPIC + ".S-007", intent="reinforce",
                              existingMoveId="M-001")], name="b.json")
    assert code == 0, env
    assert dispositions(env) == {"M-001": "reinforced"}
    anchors = library_rows(ws)[0]["anchor"]
    assert A1 in anchors and TOPIC + ".S-007" in anchors
    assert library_ids(ws) == ["M-001", "M-002"], "reinforce updates in place, never appends"


def test_intent_supersede_is_terminal(ws):
    seed(ws, name="a.json")
    code, env = add(ws, [move("x", "y", A1, intent="supersede", existingMoveId="M-001")], name="b.json")
    assert code == 0 and env["payload"]["superseded"] == 1
    assert library_rows(ws)[0]["status"] == "superseded"
    # a second supersede is an illegal transition out of a terminal state (C-18)
    code, env = add(ws, [move("x", "y", A1, intent="supersede", existingMoveId="M-001")], name="c.json")
    assert code == 2, env
    assert env["errors"][0]["code"] == "illegal-status-transition"


def test_a_superseded_move_cannot_be_reused_or_reinforced(ws):
    seed(ws, name="a.json")
    add(ws, [move("x", "y", A1, intent="supersede", existingMoveId="M-001")], name="b.json")
    for intent in ("reuse", "reinforce"):
        code, env = add(ws, [move("x", "y", TOPIC + ".S-008", intent=intent,
                                  existingMoveId="M-001")], name="c-%s.json" % intent)
        assert code == 2, env
        assert env["errors"][0]["code"] == "illegal-status-transition"


@pytest.mark.parametrize("intent", ["reuse", "reinforce", "supersede"])
def test_non_new_intent_requires_existing_move_id(ws, intent):
    seed(ws, name="a.json")
    code, env = add(ws, [move("x", "y", A1, intent=intent)], name="b.json")
    assert code == 2, env
    assert env["errors"][0]["code"] == "input-schema"


def test_existing_move_id_without_a_library_row_is_rejected(ws):
    seed(ws, name="a.json")
    code, env = add(ws, [move("x", "y", A1, intent="reuse", existingMoveId="M-999")], name="b.json")
    assert code == 2, env
    assert env["errors"][0]["code"] == "move-not-in-library"


def test_a_superseded_shape_is_re_laid_as_a_new_row_not_revived(ws):
    """C-18: `superseded` is terminal. A shape that is needed again is re-laid as a
    NEW row — the dedup index is built from active rows only, so an intent:new
    candidate never dedups onto a dead id or grows a terminal row's anchors."""
    seed(ws, name="a.json")
    anchor_before = library_rows(ws)[0]["anchor"]
    add(ws, [move("x", "y", A1, intent="supersede", existingMoveId="M-001")], name="b.json")
    code, env = add(ws, [move("Revival attempt", SEED_MOVES[0]["inferenceForm"], TOPIC + ".S-008")],
                    name="c.json")
    assert code == 0, env
    assert env["payload"]["appended"] == 1, "a needed shape is re-laid as a new row"
    assert library_ids(ws) == ["M-001", "M-002", "M-003"]
    assert library_rows(ws)[0]["status"] == "superseded"
    assert library_rows(ws)[0]["anchor"] == anchor_before, "a terminal row is never reinforced"


# --------------------------------------------------------------------------
# anchors — qualified form, grow-only sorted union
# --------------------------------------------------------------------------

def test_bare_anchor_is_rejected_at_input(ws):
    code, env = add(ws, [move("Bare", "Given a cache `C`, invalidate by key `K`.", "S-004")])
    assert code == 2, env
    assert env["errors"][0]["code"] == "input-schema"
    assert library_ids(ws) == [], "a rejected candidate must not reach the library"


@pytest.mark.parametrize("bad", ["S-1", "S-0001x", "D-1", "url-1", TOPIC + "#S-001", TOPIC + "/S-001"])
def test_anchor_grammar_violation_is_rejected(ws, bad):
    code, env = add(ws, [move("Bad anchor", "Given a queue `Q`, bound it with budget `N`.", bad)])
    assert code == 2, env
    assert env["errors"][0]["code"] == "input-schema"
    assert library_ids(ws) == []


def test_an_already_qualified_cross_topic_anchor_is_left_alone(ws):
    qualified = "other-topic.S-009"
    code, env = add(ws, [move("Cross-topic", "Given a lease `L`, renew before expiry `E`.", qualified)])
    assert code == 0, env
    assert library_rows(ws)[0]["anchor"] == qualified


def test_anchor_union_is_sorted_and_never_shrinks(ws):
    """C-20: the anchor column is grow-only, sorted by slug then S- number."""
    add(ws, [move("Grow", "Given a queue `Q`, bound it with budget `N`.", TOPIC + ".S-005")], name="a.json")
    assert library_rows(ws)[0]["anchor"] == TOPIC + ".S-005"
    add(ws, [move("x", "y", TOPIC + ".S-001", intent="reinforce", existingMoveId="M-001")], name="b.json")
    add(ws, [move("x", "y", TOPIC + ".S-003", intent="reinforce", existingMoveId="M-001")], name="c.json")
    anchors = [a.strip() for a in library_rows(ws)[0]["anchor"].split(",")]
    assert anchors == [TOPIC + ".S-001", TOPIC + ".S-003", TOPIC + ".S-005"], anchors
    assert len(anchors) == len(set(anchors)), "the union never duplicates an anchor"


def test_sort_anchor_refs_orders_by_slug_then_number():
    refs = ["zeta.S-002", "alpha.S-010", "alpha.S-002", "zeta.S-001"]
    assert ENGINE.sort_anchor_refs(refs) == \
        ["alpha.S-002", "alpha.S-010", "zeta.S-001", "zeta.S-002"]


# --------------------------------------------------------------------------
# candidate schema — all-or-nothing, zero writes on any violation (C-28)
# --------------------------------------------------------------------------

@pytest.mark.parametrize("field", ["name", "inferenceForm", "prevents", "appliesWhen"])
def test_new_candidate_missing_a_required_field_is_rejected(ws, field):
    cand = move("No guard", "Given a queue `Q`, bound it with a budget `N`.", A1)
    cand[field] = ""
    code, env = add(ws, [cand])
    assert code == 2, env
    assert env["errors"][0]["code"] == "input-schema"
    assert library_ids(ws) == []


def test_empty_moves_list_is_an_input_error(ws):
    code, env = add(ws, [])
    assert code == 2 and env["ok"] is False


def test_schema_failure_is_all_or_nothing(ws):
    """One bad candidate => zero writes, even though a good one precedes it (C-28)."""
    unguarded = move("No guard", "Given a queue `Q`, bound it with a budget `N`.", A1)
    unguarded["appliesWhen"] = ""
    code, env = add(ws, [move("Fine", "Given a lease `L`, renew before expiry `E`.", A2), unguarded])
    assert code == 2, env
    assert library_ids(ws) == [], "schema validation is all-or-nothing: nothing is written"


# --------------------------------------------------------------------------
# hand edits are detected, never silently accepted, never auto-repaired
# --------------------------------------------------------------------------

def _refuses_with_hand_edited(ws, mutate):
    seed(ws, name="a.json")
    break_library(ws, mutate)
    broken = library_text(ws)
    code, env = add(ws, [move("After break", "Given a queue `Q`, bound it with budget `N`.",
                              TOPIC + ".S-005")], name="b.json")
    assert code == 2, env
    assert env["errors"][0]["code"] == "moves-library-hand-edited"
    assert library_text(ws) == broken, "the engine must not repair the library"
    return env


def test_duplicate_move_id_is_detected(ws):
    env = _refuses_with_hand_edited(ws, lambda t: t.replace("| M-002 |", "| M-001 |", 1))
    assert any(e.get("value") == "duplicate-id" for e in env["errors"])


def test_broken_monotonicity_is_detected(ws):
    def swap(text):
        lines = text.splitlines()
        idx = [i for i, line in enumerate(lines) if line.startswith("| M-")]
        lines[idx[0]], lines[idx[1]] = lines[idx[1]], lines[idx[0]]
        return "\n".join(lines) + "\n"
    env = _refuses_with_hand_edited(ws, swap)
    assert any(e.get("value") == "id-not-monotonic" for e in env["errors"])


def test_duplicate_inference_form_is_detected(ws):
    def dup_form(text):
        row = [line for line in text.splitlines() if line.startswith("| M-001 |")][0]
        return text.rstrip("\n") + "\n" + row.replace("| M-001 |", "| M-009 |", 1) + "\n"
    env = _refuses_with_hand_edited(ws, dup_form)
    assert any(e.get("value") == "duplicate-form" for e in env["errors"])


def test_status_outside_the_enum_is_detected(ws):
    env = _refuses_with_hand_edited(ws, lambda t: t.replace("| active |", "| reused |", 1))
    assert any(e.get("value") == "status-not-in-enum" for e in env["errors"])


def test_missing_engine_written_marker_is_detected(ws):
    env = _refuses_with_hand_edited(ws, lambda t: t.replace(ENGINE.MOVES_MARKER, ""))
    assert any(e.get("value") == "header-marker-missing" for e in env["errors"])


def test_non_qualified_anchor_in_the_library_is_detected(ws):
    env = _refuses_with_hand_edited(ws, lambda t: t.replace(A1, "S-001", 1))
    assert any(e.get("value") == "anchor-form" for e in env["errors"])


def test_move_id_grammar_is_detected(ws):
    env = _refuses_with_hand_edited(ws, lambda t: t.replace("| M-001 |", "| M-1 |", 1))
    assert any(e.get("value") == "id-grammar" for e in env["errors"])


# --------------------------------------------------------------------------
# status column — two durable values, never a run-relative disposition
# --------------------------------------------------------------------------

def test_status_column_never_carries_a_run_relative_disposition(ws):
    seed(ws, name="a.json")
    add(ws, [move("x", "y", A1, intent="reuse", existingMoveId="M-001")], name="b.json")
    add(ws, [move("x", "y", TOPIC + ".S-007", intent="reinforce", existingMoveId="M-002")], name="c.json")
    add(ws, [move("New-shape", "Given a ledger `L`, append only entries `E`.", TOPIC + ".S-003")],
        name="d.json")
    statuses = {row["status"] for row in library_rows(ws)}
    assert statuses <= {"active", "superseded"}
    assert not (statuses & {"new", "reused", "reinforced"}), (
        "run-relative dispositions are payload output, never a library column (C-17)")


# --------------------------------------------------------------------------
# moves-list — filters and the projection read path
# --------------------------------------------------------------------------

def test_moves_list_filters_by_name_substring_case_insensitively(ws):
    seed(ws)
    code, env = run(ws, "--action", "moves-list", "--name-contains", "DEMOTE")
    assert code == 0
    assert env["payload"]["returned"] == 1
    assert env["payload"]["moves"][0]["moveId"] == "M-001"


def test_moves_list_filters_by_anchor(ws):
    seed(ws)
    code, env = run(ws, "--action", "moves-list", "--anchor", A2)
    assert code == 0
    assert [m["moveId"] for m in env["payload"]["moves"]] == ["M-002"]


def test_moves_list_filters_by_status(ws):
    seed(ws, name="a.json")
    add(ws, [move("x", "y", A1, intent="supersede", existingMoveId="M-001")], name="b.json")
    code, active = run(ws, "--action", "moves-list", "--status", "active")
    assert code == 0 and [m["moveId"] for m in active["payload"]["moves"]] == ["M-002"]
    code, retired = run(ws, "--action", "moves-list", "--status", "superseded")
    assert code == 0 and [m["moveId"] for m in retired["payload"]["moves"]] == ["M-001"]


def test_moves_list_filters_combine_as_and_and_zero_hits_is_ok(ws):
    seed(ws)
    code, env = run(ws, "--action", "moves-list", "--name-contains", "Demote", "--anchor", A2)
    assert code == 0
    assert env["payload"]["returned"] == 0 and env["payload"]["moves"] == []
    assert env["payload"]["total"] == 2


def test_moves_list_rejects_a_run_relative_status(ws):
    seed(ws)
    code, env = run(ws, "--action", "moves-list", "--status", "reinforced")
    assert code == 2 and env["errors"][0]["code"] == "input-enum"


def test_moves_list_rejects_a_malformed_anchor(ws):
    seed(ws)
    code, env = run(ws, "--action", "moves-list", "--anchor", "not-an-anchor")
    assert code == 2 and env["errors"][0]["code"] == "input-enum"


def test_moves_list_emits_a_projection_not_the_raw_file(ws):
    seed(ws)
    code, env = run(ws, "--action", "moves-list")
    assert code == 0 and env["ok"] is True
    p = env["payload"]
    assert p["projection"] is True and p["total"] == 2 and p["returned"] == 2
    assert p["filters"] == {"nameContains": None, "status": None, "anchor": None}
    assert set(p["librarySize"]) == {"lines", "bytes"}
    for row in p["moves"]:
        assert set(row) == {"moveId", "name", "inferenceForm", "prevents", "appliesWhen",
                            "anchor", "status"}
        assert row["status"] in ("active", "superseded")
    # the library's prose header must not be shipped in the projection
    assert library_text(ws).splitlines()[0] not in str(p["moves"])


def test_full_read_allowed_is_true_for_a_small_library(ws):
    seed(ws)
    code, env = run(ws, "--action", "moves-list")
    assert code == 0 and env["payload"]["fullReadAllowed"] is True


def test_full_read_allowed_flips_false_past_the_line_threshold(ws):
    rows = [{"move_id": "M-%03d" % (i + 1), "name": "shape-%d" % i,
             "inference_form": "Given a distinct slot `S%d`, derive outcome `O%d`." % (i, i),
             "prevents": "p", "applies_when": "w; NOT licensed when x",
             "anchor": A1, "status": "active"}
            for i in range(ENGINE.SMALL_FILE_MAX_LINES + 5)]
    (ws / ".specify" / "derive" / "moves.md").write_text(ENGINE.moves_file_text(rows),
                                                         encoding="utf-8")
    code, env = run(ws, "--action", "moves-list")
    assert code == 0
    assert env["payload"]["librarySize"]["lines"] > ENGINE.SMALL_FILE_MAX_LINES
    assert env["payload"]["fullReadAllowed"] is False


def test_full_read_allowed_flips_false_past_the_byte_threshold(ws):
    # few rows but each padded so the byte threshold trips first
    pad = "x" * 400
    rows = [{"move_id": "M-%03d" % (i + 1), "name": "shape-%d" % i,
             "inference_form": "Given a distinct slot `S%d`, derive outcome `O%d`." % (i, i),
             "prevents": pad, "applies_when": "w; NOT licensed when x",
             "anchor": A1, "status": "active"}
            for i in range(40)]
    (ws / ".specify" / "derive" / "moves.md").write_text(ENGINE.moves_file_text(rows),
                                                         encoding="utf-8")
    code, env = run(ws, "--action", "moves-list")
    assert code == 0
    assert env["payload"]["librarySize"]["bytes"] > ENGINE.SMALL_FILE_MAX_BYTES
    assert env["payload"]["fullReadAllowed"] is False


def test_init_creates_the_library_skeleton_once(ws):
    assert (ws / ".specify" / "derive" / "moves.md").is_file()
    code, env = run(ws, "--action", "init", "--slug", "second-topic")
    assert code == 0
    text = library_text(ws)
    assert ENGINE.MOVES_MARKER in text
    assert ENGINE.MOVES_HEADER in text and ENGINE.MOVES_SEPARATOR in text
    assert library_ids(ws) == [], "init scaffolds zero data rows"
    assert (ws / ".specify" / "derive" / "second-topic" / "derive.md").is_file()
