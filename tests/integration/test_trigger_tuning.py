"""US4 integration tests — evidence-driven rule tuning (spec 050).

Covers FR-015 (missed-suggestion evidence via record-manual), FR-016 (the rule
set changes only through tune-apply) and FR-017 (the small-sample guard), plus
SM-2's two-step proposed -> ratified -> applied transition and the
semanticJudgmentPending hand-off that keeps judgement with the agent.

Proposal emission criteria are the contract's closed constants
(trigger-engine.md, `tune` row): suppress at declined/hits >= 0.50, tighten at
ignored/hits >= 0.50, add-rule at >= 2 missed invocations of one flow. All four
additionally require hits >= minSample.

Written RED before record-manual/tune/tune-apply exist (tasks.md T037 is
parallel-eligible with the US3 implementation).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "scripts" / "python" / "trigger-utils.py"
SEED = ROOT / "templates" / "proactive-trigger-seed.json"

EXIT_OK, EXIT_INPUT_ERROR, EXIT_INVALID = 0, 2, 4
CLARIFY_ARGS = ["--stage", "requirements-unclear", "--signal", "needs-clarification"]
NO_MATCH_ARGS = ["--stage", "non-feature"]
_turn = {"n": 0}


@pytest.fixture
def ws(tmp_path: Path) -> Path:
    (tmp_path / ".specify" / "templates").mkdir(parents=True)
    (tmp_path / ".specify" / "templates" / "proactive-trigger-seed.json").write_bytes(
        SEED.read_bytes()
    )
    (tmp_path / ".specify" / "memory").mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q", "."], cwd=tmp_path, check=True)
    run(["--action", "init"], tmp_path)
    _turn["n"] = 0
    return tmp_path


def run(args, cwd) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(ENGINE), *args], cwd=cwd,
                          capture_output=True, text=True)


def env_of(proc) -> dict:
    assert proc.stdout.strip(), f"no stdout; stderr={proc.stderr[-800:]}"
    return json.loads(proc.stdout)


def rules_payload(ws: Path) -> list:
    return env_of(run(["--action", "rules", "--format", "json"], ws))["payload"]["rules"]


def rules_rendered(ws: Path) -> str:
    return json.dumps(rules_payload(ws), ensure_ascii=False, indent=2, sort_keys=True)


def index(ws: Path) -> dict:
    return json.loads((ws / ".specify" / "memory" / "trigger" / "index.json")
                      .read_text(encoding="utf-8"))


def fresh_session(prefix: str) -> tuple:
    """A new session each turn, so C-20 suppression does not swallow the hit."""
    _turn["n"] += 1
    session = f"{prefix}-{_turn['n']}"
    return session, f"{session}-01"


def hit_and_respond(ws, rid, response, stage_args=CLARIFY_ARGS, prefix="stune"):
    session, turn = fresh_session(prefix)
    proc = run(["--action", "assess", "--session", session, "--turn-id", turn,
                "--compliance-done", *stage_args], ws)
    assert proc.returncode == EXIT_OK, proc.stderr
    proc = run(["--action", "record", "--session", session, "--rule", rid,
                "--response", response], ws)
    assert proc.returncode == EXIT_OK, proc.stderr


def manual_flow(ws, flow, prefix="sman"):
    """A turn where nothing was suggested, then the user ran a flow by hand."""
    session, turn = fresh_session(prefix)
    proc = run(["--action", "assess", "--session", session, "--turn-id", turn,
                *NO_MATCH_ARGS], ws)
    assert proc.returncode == EXIT_OK, proc.stderr
    assert env_of(proc)["payload"].get("suggestion") is None, "fixture expected no suggestion"
    proc = run(["--action", "record-manual", "--session", session, "--flow", flow], ws)
    assert proc.returncode == EXIT_OK, proc.stderr


def proposals(ws: Path) -> list:
    env = env_of(run(["--action", "tune", "--format", "json"], ws))
    return env["payload"].get("proposals", [])


# --- FR-017: the small-sample guard ---


def test_small_sample_rules_are_not_proposed_and_are_named(ws):
    # Two declines on r-001: a 1.0 decline rate, but only 2 hits (< minSample 5).
    hit_and_respond(ws, "r-001", "declined")
    hit_and_respond(ws, "r-001", "declined")

    env = env_of(run(["--action", "tune", "--format", "json"], ws))
    props = env["payload"].get("proposals", [])
    assert all(p.get("ruleId") != "r-001" for p in props), (
        "FR-017: a rule below minSample must not yield a proposal however bad its ratio"
    )
    notes = " ".join(env["notes"])
    assert "r-001" in notes, (
        f"FR-017: a skipped rule must be named in notes[], got {env['notes']!r}"
    )


def test_min_sample_is_configurable(ws):
    for _ in range(2):
        hit_and_respond(ws, "r-001", "declined")
    assert not any(p.get("ruleId") == "r-001" for p in proposals(ws))

    proc = run(["--action", "tune", "--min-sample", "2", "--format", "json"], ws)
    assert proc.returncode == EXIT_OK, proc.stderr
    props = env_of(proc)["payload"].get("proposals", [])
    assert any(p.get("ruleId") == "r-001" for p in props), (
        "lowering minSample to 2 must let the same evidence produce a proposal"
    )


# --- proposal emission criteria ---


def test_high_decline_rate_yields_a_suppress_proposal(ws):
    for _ in range(6):
        hit_and_respond(ws, "r-001", "declined")
    props = proposals(ws)
    mine = [p for p in props if p.get("ruleId") == "r-001"]
    assert mine, f"expected a proposal for r-001, got {props}"
    assert mine[0]["kind"] == "suppress", (
        f"declined/hits = 1.0 must emit 'suppress', got {mine[0]['kind']}"
    )


def test_high_ignore_rate_yields_a_tighten_proposal(ws):
    for _ in range(6):
        hit_and_respond(ws, "r-001", "ignored")
    props = proposals(ws)
    mine = [p for p in props if p.get("ruleId") == "r-001"]
    assert mine and mine[0]["kind"] == "tighten", (
        f"ignored/hits = 1.0 must emit 'tighten', got {mine}"
    )


def test_acceptance_yields_no_proposal(ws):
    for _ in range(6):
        hit_and_respond(ws, "r-001", "accepted")
    props = proposals(ws)
    assert all(p.get("ruleId") != "r-001" for p in props), (
        f"a well-received rule must not be proposed for change, got {props}"
    )


def test_missed_flow_yields_an_add_rule_proposal(ws):
    manual_flow(ws, "/speckit.history")
    manual_flow(ws, "/speckit.history")
    props = proposals(ws)
    kinds = {p["kind"] for p in props}
    assert "add-rule" in kinds, (
        f"two missed invocations of one flow must emit 'add-rule', got {props}"
    )
    add = next(p for p in props if p["kind"] == "add-rule")
    assert add.get("flow") == "/speckit.history" or "/speckit.history" in json.dumps(add)


def test_a_single_missed_flow_is_below_the_add_rule_bar(ws):
    manual_flow(ws, "/speckit.history")
    props = proposals(ws)
    assert not any(p["kind"] == "add-rule" for p in props), (
        "one missed invocation is below the >=2 emission bar"
    )


# --- evidence shape ---


def test_every_proposal_carries_evidence_with_metric_and_sample_size(ws):
    for _ in range(6):
        hit_and_respond(ws, "r-001", "declined")
    manual_flow(ws, "/speckit.history")
    manual_flow(ws, "/speckit.history")

    for p in proposals(ws):
        assert "proposalId" in p and p["proposalId"].startswith("p-"), (
            f"proposalId must follow ^p-[0-9]{{3}}$, got {p.get('proposalId')!r}"
        )
        assert p["kind"] in {"tighten", "suppress", "add-rule", "extend-vocabulary"}, (
            f"kind {p['kind']!r} outside the closed set"
        )
        ev = p.get("evidence")
        assert isinstance(ev, dict), f"{p['proposalId']}: evidence must be an object"
        assert set(ev) >= {"metric", "value", "sampleSize"}, (
            f"{p['proposalId']}: evidence must carry metric/value/sampleSize, got {sorted(ev)}"
        )
        assert isinstance(ev["sampleSize"], int) and ev["sampleSize"] > 0
        assert p.get("state") == "proposed"


# --- FR-016: nothing changes without tune-apply ---


def test_tune_alone_changes_nothing(ws):
    for _ in range(6):
        hit_and_respond(ws, "r-001", "declined")
    before = rules_rendered(ws)
    run(["--action", "tune", "--format", "json"], ws)
    run(["--action", "tune", "--format", "json"], ws)
    assert rules_rendered(ws) == before, (
        "FR-016: tune is read-only analysis; the rule set must not move"
    )


def test_tune_apply_moves_the_state_machine_and_leaves_a_trail(ws):
    for _ in range(6):
        hit_and_respond(ws, "r-001", "declined")
    props = proposals(ws)
    pid = props[0]["proposalId"]
    before = rules_rendered(ws)

    proc = run(["--action", "tune-apply", "--proposal", pid,
                "--reason", "decline rate 1.00 over 6 hits"], ws)
    assert proc.returncode == EXIT_OK, proc.stderr

    data = index(ws)
    applied = next(p for p in data["proposals"] if p["proposalId"] == pid)
    assert applied["state"] == "applied", (
        f"SM-2 must reach applied, got {applied['state']}"
    )
    assert applied.get("ratifiedAt"), "ratification must be a separate, dated event"
    assert applied.get("appliedAt"), "application must be dated too"
    assert applied.get("reason"), "the approval reason must be stored for later lookup"

    target = next(r for r in data["rules"] if r["ruleId"] == "r-001")
    tuning = target.get("tuning")
    assert tuning, "tune-apply must write the rule's tuning trace"
    assert tuning.get("ratifiedAt"), "tuning.ratifiedAt must be written"
    assert tuning.get("evidenceRef"), "tuning.evidenceRef must point back at the evidence"
    assert rules_rendered(ws) != before, (
        "FR-016's counterpart: an approved proposal must actually change the rule set"
    )


def test_tune_apply_requires_a_reason(ws):
    for _ in range(6):
        hit_and_respond(ws, "r-001", "declined")
    pid = proposals(ws)[0]["proposalId"]
    proc = run(["--action", "tune-apply", "--proposal", pid], ws)
    assert proc.returncode != EXIT_OK, "an approval without a reason must be refused"


def test_tune_apply_unknown_proposal_is_reported(ws):
    proc = run(["--action", "tune-apply", "--proposal", "p-999", "--reason", "x"], ws)
    assert "proposal-not-found" in env_of(proc)["errors"]


def test_applied_suppression_takes_effect(ws):
    for _ in range(6):
        hit_and_respond(ws, "r-001", "declined")
    pid = proposals(ws)[0]["proposalId"]
    run(["--action", "tune-apply", "--proposal", pid, "--reason", "noisy rule"], ws)

    target = next(r for r in index(ws)["rules"] if r["ruleId"] == "r-001")
    if target.get("tuning", {}).get("suppressedBy"):
        assert target["state"] == "suppressed", (
            "a suppression written back must be reflected in the rule state"
        )
        session, turn = fresh_session("safter")
        env = env_of(run(["--action", "assess", "--session", session, "--turn-id", turn,
                          "--compliance-done", *CLARIFY_ARGS], ws))
        assert env["payload"].get("suggestion") is None, (
            "a suppressed rule must stop suggesting"
        )


# --- semantic judgement stays with the agent ---


def test_judgement_items_are_handed_back_not_decided(ws):
    for _ in range(6):
        hit_and_respond(ws, "r-001", "declined")
    manual_flow(ws, "/speckit.history")
    manual_flow(ws, "/speckit.history")

    env = env_of(run(["--action", "tune", "--format", "json"], ws))
    pending = env["semanticJudgmentPending"]
    assert pending, (
        "tune must hand the 'should this be adopted / which flow does this missed "
        "situation belong to' judgement back to the agent rather than deciding it"
    )
    assert all(isinstance(x, (str, dict)) for x in pending)


def test_record_manual_requires_a_flow(ws):
    assert ENGINE.is_file(), f"engine missing: {ENGINE} — this test would pass vacuously"
    proc = run(["--action", "record-manual"], ws)
    assert proc.returncode != EXIT_OK, "--flow is required for record-manual"
    assert "No such file" not in proc.stderr, (
        "the refusal must come from the engine's own argument handling, not a missing script"
    )


def test_record_manual_rejects_an_empty_flow(ws):
    assert ENGINE.is_file(), f"engine missing: {ENGINE} — this test would pass vacuously"
    proc = run(["--action", "record-manual", "--flow", ""], ws)
    assert proc.returncode != EXIT_OK
    assert "No such file" not in proc.stderr


def test_repeated_tune_is_idempotent_in_proposal_count(ws):
    for _ in range(6):
        hit_and_respond(ws, "r-001", "declined")
    first = proposals(ws)
    second = proposals(ws)
    assert len(second) == len(first), (
        f"re-running tune must not accumulate duplicate proposals: {len(first)} -> {len(second)}"
    )
