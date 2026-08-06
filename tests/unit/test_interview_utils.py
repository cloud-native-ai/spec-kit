"""Unit tests for the interview decision-DAG engine (Feature 042).

Engine: scripts/python/interview-utils.py
Pattern: shared/patterns/interview-pattern.md

Covers the parts the pattern delegates to a program: dependency tracking, frontier
computation, cycle rejection, deep-premise-first ordering, retraction propagation
(the D3→D4 case), conflict candidate lookup, and exit-gate readiness.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "scripts/python/interview-utils.py"


def _load_engine():
    assert ENGINE.is_file(), f"engine missing: {ENGINE}"
    spec = importlib.util.spec_from_file_location("interview_utils", ENGINE)
    module = importlib.util.module_from_spec(spec)
    sys.modules["interview_utils"] = module
    spec.loader.exec_module(module)
    return module


iu = _load_engine()


@pytest.fixture()
def ledger(tmp_path: Path) -> Path:
    path = tmp_path / "interview-log.md"
    iu.act_init(path, target="plan.md", mode="special", branches=["storage"], force=False)
    return path


def _chain(ledger: Path) -> None:
    """D1 → D3 → D4, plus an isolated D2, all settled except D4."""
    iu.act_add(ledger, "D1", "backend?", [], "storage")
    iu.act_add(ledger, "D2", "unrelated?", [], "naming")
    iu.act_add(ledger, "D3", "which queue?", ["D1"], "storage")
    iu.act_add(ledger, "D4", "retry policy?", ["D3"], "storage")
    iu.act_answer(ledger, "D1", "queue", "## Storage", 1)
    iu.act_answer(ledger, "D3", "redis", "## Storage > Queue", 2)


# ---------------------------------------------------------------------------
# Store & identity
# ---------------------------------------------------------------------------

def test_store_is_a_sidecar_of_the_ledger(ledger: Path):
    assert iu.store_path(ledger).name == "interview-log.dag.json"
    assert iu.store_path(ledger).is_file()


def test_init_refuses_to_clobber_without_force(ledger: Path):
    with pytest.raises(iu.EngineError) as exc:
        iu.act_init(ledger, target="other.md", mode=None, branches=[], force=False)
    assert exc.value.code == iu.EXIT_INPUT_ERROR


def test_load_missing_store_is_not_found(tmp_path: Path):
    with pytest.raises(iu.EngineError) as exc:
        iu.load(tmp_path / "absent.md")
    assert exc.value.code == iu.EXIT_NOT_FOUND


@pytest.mark.parametrize("bad", ["4D", "-D1", "", "1", "#D"])
def test_invalid_ids_rejected(ledger: Path, bad: str):
    with pytest.raises(iu.EngineError):
        iu.act_add(ledger, bad, "q?", [], None)


def test_ids_are_never_reused(ledger: Path):
    iu.act_add(ledger, "D1", "q?", [], None)
    with pytest.raises(iu.EngineError) as exc:
        iu.act_add(ledger, "D1", "different q?", [], None)
    assert "never reused" in str(exc.value)


def test_unknown_premise_is_not_found(ledger: Path):
    with pytest.raises(iu.EngineError) as exc:
        iu.act_add(ledger, "D2", "q?", ["D99"], None)
    assert exc.value.code == iu.EXIT_NOT_FOUND


# ---------------------------------------------------------------------------
# Cycles — a retraction walk on a cyclic graph would not terminate
# ---------------------------------------------------------------------------

def test_self_dependency_rejected(ledger: Path):
    with pytest.raises(iu.EngineError) as exc:
        iu.act_add(ledger, "D1", "q?", ["D1"], None)
    assert exc.value.code in (iu.EXIT_INVALID, iu.EXIT_NOT_FOUND)


def test_indirect_cycle_rejected(ledger: Path, tmp_path: Path):
    iu.act_add(ledger, "D1", "a?", [], None)
    iu.act_add(ledger, "D2", "b?", ["D1"], None)
    iu.act_add(ledger, "D3", "c?", ["D2"], None)
    # D1 already reaches D3 transitively; making D1 rest on D3 closes the loop.
    data = iu.load(ledger)
    cycle = iu._would_cycle(data, "D1", ["D3"])
    assert cycle, "expected a cycle to be detected"


# ---------------------------------------------------------------------------
# Frontier & ordering
# ---------------------------------------------------------------------------

def test_frontier_excludes_blocked_questions(ledger: Path):
    _chain(ledger)
    # D4 is askable (D3 settled); D2 is open with no premises.
    assert set(iu.frontier(iu.load(ledger))) == {"D2", "D4"}


def test_frontier_blocks_on_unsettled_premise(ledger: Path):
    iu.act_add(ledger, "D1", "a?", [], None)
    iu.act_add(ledger, "D2", "b?", ["D1"], None)
    assert iu.frontier(iu.load(ledger)) == ["D1"], "D2 must wait for its premise"


def test_deferred_premise_does_not_unblock_dependents(ledger: Path):
    iu.act_add(ledger, "D1", "a?", [], None)
    iu.act_add(ledger, "D2", "b?", ["D1"], None)
    iu.act_defer(ledger, "D1", "out of scope")
    assert "D2" not in iu.frontier(iu.load(ledger))


def test_order_puts_most_depended_on_premises_first(ledger: Path):
    iu.act_add(ledger, "shallow", "no dependents?", [], None)
    iu.act_add(ledger, "deep", "many dependents?", [], None)
    for n in range(3):
        iu.act_add(ledger, f"leaf{n}", "q?", ["deep"], None)
    order = iu.topological_order(iu.load(ledger))
    assert order[0] == "deep", f"deep premise must be asked first, got {order}"
    assert order.index("deep") < order.index("shallow")


def test_answering_a_blocked_decision_is_rejected(ledger: Path):
    iu.act_add(ledger, "D1", "a?", [], None)
    iu.act_add(ledger, "D2", "b?", ["D1"], None)
    with pytest.raises(iu.EngineError) as exc:
        iu.act_answer(ledger, "D2", "answer", "## S", 1)
    assert exc.value.code == iu.EXIT_INVALID


# ---------------------------------------------------------------------------
# Dependency queries
# ---------------------------------------------------------------------------

def test_descendants_are_transitive(ledger: Path):
    _chain(ledger)
    assert iu.descendants(iu.load(ledger), "D1") == ["D3", "D4"]


def test_direct_descendants_stop_at_one_hop(ledger: Path):
    _chain(ledger)
    assert iu.descendants(iu.load(ledger), "D1", direct=True) == ["D3"]


def test_descendants_of_isolated_branch_are_empty(ledger: Path):
    _chain(ledger)
    assert iu.descendants(iu.load(ledger), "D2") == []


def test_descendants_of_unknown_id_is_not_found(ledger: Path):
    with pytest.raises(iu.EngineError) as exc:
        iu.descendants(iu.load(ledger), "D77")
    assert exc.value.code == iu.EXIT_NOT_FOUND


def test_diamond_dependency_reports_each_node_once(ledger: Path):
    iu.act_add(ledger, "root", "r?", [], None)
    iu.act_add(ledger, "left", "l?", ["root"], None)
    iu.act_add(ledger, "right", "r2?", ["root"], None)
    iu.act_add(ledger, "join", "j?", ["left", "right"], None)
    found = iu.descendants(iu.load(ledger), "root")
    assert sorted(found) == ["join", "left", "right"]
    assert len(found) == len(set(found)), "no duplicates in a diamond"


# ---------------------------------------------------------------------------
# Retraction — the D3→D4 case from the pattern
# ---------------------------------------------------------------------------

def test_retract_dry_run_writes_nothing(ledger: Path):
    _chain(ledger)
    before = iu.store_path(ledger).read_text(encoding="utf-8")
    plan = iu.act_retract(ledger, "D3", decision=None, apply=False)
    assert plan["applied"] is False
    assert iu.store_path(ledger).read_text(encoding="utf-8") == before


def test_retract_plan_lists_spans_to_roll_back(ledger: Path):
    _chain(ledger)
    iu.act_answer(ledger, "D4", "3 retries", "## Storage > Retry", 3)
    plan = iu.act_retract(ledger, "D3", decision=None, apply=False)
    assert plan["descendants"] == ["D4"]
    assert plan["invalidated"] == ["D4"]
    assert {"id": "D4", "span": "## Storage > Retry"} in plan["needs_rollback"]


def test_retract_apply_reopens_descendants(ledger: Path):
    _chain(ledger)
    iu.act_answer(ledger, "D4", "3 retries", "## Storage > Retry", 3)
    iu.act_retract(ledger, "D3", decision="sqs", apply=True)
    data = iu.load(ledger)
    index = {d["id"]: d for d in data["decisions"]}
    assert index["D3"]["decision"] == "sqs"
    assert index["D4"]["status"] == iu.OPEN, "D4 rested on D3 — it must be re-asked"
    assert index["D4"]["decision"] is None
    assert index["D4"]["span"] is None, "stale span must be cleared"
    assert "D4" in iu.frontier(data), "re-opened D4 returns to the frontier"


def test_retract_leaves_isolated_branch_untouched(ledger: Path):
    _chain(ledger)
    iu.act_answer(ledger, "D2", "kept", "## Naming", 2)
    iu.act_retract(ledger, "D3", decision="sqs", apply=True)
    index = {d["id"]: d for d in iu.load(ledger)["decisions"]}
    assert index["D2"]["status"] == iu.SETTLED, "isolation must limit the blast radius"
    assert index["D2"]["decision"] == "kept"


def test_retract_is_recorded(ledger: Path):
    _chain(ledger)
    iu.act_retract(ledger, "D3", decision="sqs", apply=True)
    data = iu.load(ledger)
    assert len(data["retractions"]) == 1
    assert data["retractions"][0]["invalidated"] == []


def test_retract_propagates_through_a_deep_chain(ledger: Path):
    iu.act_add(ledger, "A", "a?", [], None)
    iu.act_add(ledger, "B", "b?", ["A"], None)
    iu.act_add(ledger, "C", "c?", ["B"], None)
    for i, name in enumerate(("A", "B", "C"), start=1):
        iu.act_answer(ledger, name, f"ans{i}", f"## {name}", i)
    plan = iu.act_retract(ledger, "A", decision="new", apply=True)
    assert plan["invalidated"] == ["B", "C"], "transitive, not just the direct child"
    index = {d["id"]: d for d in iu.load(ledger)["decisions"]}
    assert index["B"]["status"] == iu.OPEN and index["C"]["status"] == iu.OPEN


def test_retract_without_replacement_reopens_itself(ledger: Path):
    _chain(ledger)
    iu.act_retract(ledger, "D3", decision=None, apply=True)
    index = {d["id"]: d for d in iu.load(ledger)["decisions"]}
    assert index["D3"]["status"] == iu.OPEN


def test_answer_on_retracted_decision_rejected(ledger: Path):
    iu.act_add(ledger, "D1", "a?", [], None)
    iu.act_answer(ledger, "D1", "x", "## S", 1)
    data = iu.load(ledger)
    data["decisions"][0]["status"] = iu.RETRACTED
    iu.save(ledger, data)
    with pytest.raises(iu.EngineError) as exc:
        iu.act_answer(ledger, "D1", "y", "## S", 2)
    assert exc.value.code == iu.EXIT_INVALID


# ---------------------------------------------------------------------------
# Conflicts & status
# ---------------------------------------------------------------------------

def test_conflicts_returns_candidates_not_verdicts(ledger: Path):
    _chain(ledger)
    out = iu.act_conflicts(ledger, "should the queue be redis or sqs")
    assert "candidates" in out and "model's call" in out["note"]
    assert any(c["id"] == "D3" for c in out["candidates"])


def test_conflicts_ignores_unsettled_rows(ledger: Path):
    iu.act_add(ledger, "D1", "queue backend?", [], None)
    out = iu.act_conflicts(ledger, "queue backend")
    assert out["candidates"] == []


def test_status_reports_frontier_and_gate(ledger: Path):
    _chain(ledger)
    st = iu.act_status(ledger)
    assert st["mode"] == "special" and st["target"] == "plan.md"
    assert st["exit_gate_ready"] is False
    assert set(st["frontier"]) == {"D2", "D4"}


def test_exit_gate_ready_only_when_nothing_open(ledger: Path):
    iu.act_add(ledger, "D1", "a?", [], None)
    iu.act_answer(ledger, "D1", "x", "## S", 1)
    assert iu.act_status(ledger)["exit_gate_ready"] is True


def test_status_flags_settled_without_span(ledger: Path):
    iu.act_add(ledger, "D1", "a?", [], None)
    iu.act_answer(ledger, "D1", "x", None, 1)
    assert iu.act_status(ledger)["settled_without_span"] == ["D1"]


# ---------------------------------------------------------------------------
# Render & resumability
# ---------------------------------------------------------------------------

def test_render_emits_the_pattern_ledger_columns(ledger: Path):
    _chain(ledger)
    table = iu.render(ledger)
    for column in ("ID", "dependsOn", "Status", "Artifact span", "Superseded by"):
        assert column in table
    assert "| D3 |" in table and "D1" in table
    assert "✅" in table and "⬜" in table


def test_store_survives_a_reload(ledger: Path):
    _chain(ledger)
    reloaded = json.loads(iu.store_path(ledger).read_text(encoding="utf-8"))
    assert reloaded["target"] == "plan.md"
    assert [d["id"] for d in reloaded["decisions"]] == ["D1", "D2", "D3", "D4"]


# ---------------------------------------------------------------------------
# CLI surface
# ---------------------------------------------------------------------------

def test_cli_end_to_end(tmp_path: Path, capsys):
    led = str(tmp_path / "log.md")
    assert iu.main(["init", "--ledger", led, "--target", "spec.md", "--mode", "informal"]) == 0
    assert iu.main(["add", "--ledger", led, "--id", "D1", "--question", "a?"]) == 0
    assert iu.main(["add", "--ledger", led, "--id", "D2", "--question", "b?",
                    "--depends-on", "D1"]) == 0
    assert iu.main(["answer", "--ledger", led, "D1", "--decision", "yes",
                    "--span", "## A"]) == 0
    capsys.readouterr()
    assert iu.main(["frontier", "--ledger", led, "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["frontier"] == ["D2"]


def test_cli_maps_errors_to_exit_codes(tmp_path: Path):
    led = str(tmp_path / "log.md")
    assert iu.main(["frontier", "--ledger", led]) == iu.EXIT_NOT_FOUND
    iu.main(["init", "--ledger", led, "--target", "t.md"])
    assert iu.main(["add", "--ledger", led, "--id", "D1", "--question", "q?",
                    "--depends-on", "NOPE"]) == iu.EXIT_NOT_FOUND
    assert iu.main(["descendants", "--ledger", led, "GHOST"]) == iu.EXIT_NOT_FOUND
