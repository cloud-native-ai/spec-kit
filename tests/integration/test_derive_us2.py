"""Integration test — User Story 2: extract reusable reasoning moves and accumulate
them into the project-level library (048 / Feature 049, Priority P1).

Driving contract: .specify/specs/048-derive-command/contracts/move-library.md
                  (§3 two-level dedup, §4 status) + derive-engine.md C-21/C-23
Success criterion: SC-003 (a second run on the same topic reports reused +
                  reinforced > 0; the library carries zero duplicate ids and zero
                  duplicate slot-isomorphic forms).

Two sequential `moves-add` runs: run 2 must reuse run 1's identities, append only
genuinely new shapes, and leave the library de-duplicated; `stats` then reports the
run-relative dispositions read back from the archive.
"""

from __future__ import annotations

import pytest

from tests.derive_fixtures import (
    SEED_MOVES,
    SLOT_VARIANT_FORM,
    TOPIC,
    build_artifact,
    library_ids,
    library_rows,
    move,
    moves_spec_file,
    run,
    scaffold,
    write_artifact,
)

pytestmark = pytest.mark.integration

#: Run 2's ## Reasoning Moves Applied disposition log — what `stats` reads for SC-003.
DISPOSITION_LOG = """Applied from `.specify/derive/moves.md`:

| move_id | disposition |
|---|---|
| M-001 | reinforced |
| M-002 | reused |
| M-003 | new |
"""


def _add(ws, moves, name):
    spec = moves_spec_file(ws, moves, name=name)
    return run(ws, "--action", "moves-add", "--file", str(spec))


@pytest.fixture(scope="module")
def two_runs(tmp_path_factory):
    ws = tmp_path_factory.mktemp("derive-us2")
    code, env = scaffold(ws)
    assert code == 0, env

    # Run 1 — two genuinely new shapes.
    code1, env1 = _add(ws, [dict(m) for m in SEED_MOVES], "run1.json")
    assert code1 == 0, env1

    # Run 2 — a slot-isomorphic variant of M-001 with a fresh anchor (reinforce),
    # one genuinely new shape (append), and a plain reuse of M-002.
    run2 = [
        move("Renamed variant of the counter-instance move", SLOT_VARIANT_FORM, TOPIC + ".S-007"),
        move("Append-only ledger", "Given a ledger `L`, append only entries `E` and never "
                                   "rewrite history.", TOPIC + ".S-003"),
        move("reuse the forces move", "irrelevant body", TOPIC + ".S-002",
             intent="reuse", existingMoveId="M-002"),
    ]
    code2, env2 = _add(ws, run2, "run2.json")
    assert code2 == 0, env2

    write_artifact(ws, build_artifact(moves=DISPOSITION_LOG), TOPIC)
    scode, senv = run(ws, "--action", "stats", "--slug", TOPIC)
    return {"ws": ws, "run1": env1, "run2": env2, "stats_code": scode, "stats": senv}


def test_run1_issues_the_first_two_identities(two_runs):
    env1 = two_runs["run1"]
    assert env1["payload"]["issued"] == ["M-001", "M-002"]
    assert env1["payload"]["appended"] == 2
    assert {d["disposition"] for d in env1["payload"]["dispositions"]} == {"new"}


def test_run2_reuses_run1_ids_and_appends_only_the_new_shape(two_runs):
    env2 = two_runs["run2"]
    p = env2["payload"]
    # only the genuinely new shape is issued; the slot-isomorphic variant is refused
    assert p["issued"] == ["M-003"]
    assert p["appended"] == 1 and p["deduped"] == 1
    assert p["duplicates"][0]["existingMoveId"] == "M-001"
    disp = {d["moveId"]: d["disposition"] for d in p["dispositions"]}
    assert disp == {"M-001": "reinforced", "M-002": "reused", "M-003": "new"}


def test_sc003_second_run_reports_reuse_and_reinforcement(two_runs):
    disp = {d["disposition"] for d in two_runs["run2"]["payload"]["dispositions"]}
    assert {"reused", "reinforced"} <= disp, "SC-003: run 2 must reuse/reinforce, not re-issue"


def test_the_library_accumulates_without_forking_or_renumbering(two_runs):
    ws = two_runs["ws"]
    assert library_ids(ws) == ["M-001", "M-002", "M-003"]
    rows = {r["move_id"]: r for r in library_rows(ws)}
    # the reinforced move grew its anchor union; the reused move is untouched
    assert TOPIC + ".S-001" in rows["M-001"]["anchor"]
    assert TOPIC + ".S-007" in rows["M-001"]["anchor"]
    assert rows["M-002"]["anchor"] == TOPIC + ".S-002"
    # the slot-isomorphic variant never forked into a second row under a new name
    assert rows["M-001"]["name"] == SEED_MOVES[0]["name"]
    assert all(r["status"] == "active" for r in library_rows(ws))


def test_sc003_stats_reports_zero_duplicates_and_the_dispositions(two_runs):
    assert two_runs["stats_code"] == 0, two_runs["stats"].get("errors")
    p = two_runs["stats"]["payload"]
    assert p["moves"]["total"] == 3
    assert p["moves"]["duplicateIds"] == 0
    assert p["moves"]["duplicateForms"] == 0
    assert p["moves"]["byStatus"] == {"active": 3, "superseded": 0}
    assert p["dispositions"] == {"new": 1, "reused": 1, "reinforced": 1}
    assert TOPIC in p["archives"]["topics"]
    assert p["lastRun"]["slug"] == TOPIC


def test_moves_list_projects_the_accumulated_library(two_runs):
    code, env = run(two_runs["ws"], "--action", "moves-list")
    assert code == 0
    assert env["payload"]["total"] == 3 and env["payload"]["projection"] is True
