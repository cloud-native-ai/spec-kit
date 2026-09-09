"""US3 integration tests — choice recording and threshold promotion (spec 050).

Covers trigger-engine.md C-16 (consecutive count and reset), C-17 (destructive
flows never promote — zero tolerance) and C-18 (threshold priority chain and
floor), plus FR-012 (user reset) and FR-018 (global switch).

Written RED before the record/reset/config actions exist, per the dependency
graph in tasks.md (T029/T030 are parallel-eligible with the US2 implementation).
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
GENERATOR = ROOT / "scripts" / "bash" / "generate-instructions.sh"

EXIT_OK, EXIT_USAGE, EXIT_INVALID = 0, 1, 4

REVERSIBLE_RULE = "r-001"      # s01 -> /speckit.clarify
DESTRUCTIVE_RULE = "r-006"     # s06 -> /speckit.implement
CLARIFY_ARGS = ["--stage", "requirements-unclear", "--signal", "needs-clarification"]
IMPLEMENT_ARGS = ["--stage", "tasks-ready", "--signal", "open-tasks"]


@pytest.fixture
def ws(tmp_path: Path) -> Path:
    (tmp_path / ".specify" / "templates").mkdir(parents=True)
    (tmp_path / ".specify" / "templates" / "proactive-trigger-seed.json").write_bytes(
        SEED.read_bytes()
    )
    (tmp_path / ".specify" / "memory").mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q", "."], cwd=tmp_path, check=True)
    run(["--action", "init"], tmp_path)
    return tmp_path


def run(args, cwd) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(ENGINE), *args], cwd=cwd,
                          capture_output=True, text=True)


def env_of(proc) -> dict:
    assert proc.stdout.strip(), f"no stdout; stderr={proc.stderr[-800:]}"
    return json.loads(proc.stdout)


def index(ws: Path) -> dict:
    return json.loads((ws / ".specify" / "memory" / "trigger" / "index.json")
                      .read_text(encoding="utf-8"))


def rule(ws: Path, rid: str) -> dict:
    return next(r for r in index(ws)["rules"] if r["ruleId"] == rid)


def assess(ws, session, turn, stage_args, compliance=True, extra=()):
    args = ["--action", "assess", "--session", session, "--turn-id", turn, *stage_args]
    if compliance:
        args.append("--compliance-done")
    proc = run([*args, *extra], ws)
    assert proc.returncode == EXIT_OK, proc.stderr
    return env_of(proc)


def record(ws, session, rid, response):
    return run(["--action", "record", "--session", session, "--rule", rid,
                "--response", response], ws)


# --- C-16: consecutive acceptance promotes ---


def test_three_acceptances_promote_a_reversible_rule(ws):
    for i in range(1, 4):
        session = f"spromo-{i}"
        env = assess(ws, session, f"{session}-01", CLARIFY_ARGS)
        assert env["payload"]["suggestion"] is not None
        assert env["payload"]["suggestion"]["autoExecute"] is False, (
            f"turn {i}: must not auto-execute before the threshold is reached"
        )
        proc = record(ws, session, REVERSIBLE_RULE, "accepted")
        assert proc.returncode == EXIT_OK, proc.stderr

    r = rule(ws, REVERSIBLE_RULE)
    assert r["promotion"]["consecutive"] == 3
    assert r["promotion"]["promoted"] is True
    assert r["state"] == "promoted", f"state must become promoted, got {r['state']}"

    session = "spromo-4"
    env = assess(ws, session, f"{session}-01", CLARIFY_ARGS)
    assert env["payload"]["suggestion"]["autoExecute"] is True, (
        "SC-005: after promotion the next hit must carry autoExecute=true"
    )


def test_single_decline_resets_the_count(ws):
    for i in range(1, 3):
        session = f"sdec-{i}"
        assess(ws, session, f"{session}-01", CLARIFY_ARGS)
        record(ws, session, REVERSIBLE_RULE, "accepted")
    assert rule(ws, REVERSIBLE_RULE)["promotion"]["consecutive"] == 2

    session = "sdec-3"
    assess(ws, session, f"{session}-01", CLARIFY_ARGS)
    proc = record(ws, session, REVERSIBLE_RULE, "declined")
    assert proc.returncode == EXIT_OK, proc.stderr

    r = rule(ws, REVERSIBLE_RULE)
    assert r["promotion"]["consecutive"] == 0, "one decline must zero the counter"
    assert r["promotion"]["promoted"] is False
    assert r["state"] == "active", f"state must fall back to active, got {r['state']}"
    assert r["promotion"].get("resetBy"), "resetBy must name the event that reset it"


def test_decline_after_promotion_demotes(ws):
    for i in range(1, 4):
        session = f"sdem-{i}"
        assess(ws, session, f"{session}-01", CLARIFY_ARGS)
        record(ws, session, REVERSIBLE_RULE, "accepted")
    assert rule(ws, REVERSIBLE_RULE)["state"] == "promoted"

    session = "sdem-4"
    assess(ws, session, f"{session}-01", CLARIFY_ARGS)
    record(ws, session, REVERSIBLE_RULE, "declined")
    r = rule(ws, REVERSIBLE_RULE)
    assert r["state"] == "active" and r["promotion"]["promoted"] is False
    assert r["promotion"]["resetBy"]


def test_ignored_resets_but_is_counted_separately(ws):
    for i in range(1, 3):
        session = f"sign-{i}"
        assess(ws, session, f"{session}-01", CLARIFY_ARGS)
        record(ws, session, REVERSIBLE_RULE, "accepted")

    session = "sign-3"
    assess(ws, session, f"{session}-01", CLARIFY_ARGS)
    record(ws, session, REVERSIBLE_RULE, "ignored")

    r = rule(ws, REVERSIBLE_RULE)
    assert r["promotion"]["consecutive"] == 0, "ignored resets like declined"
    stats = r["stats"]
    assert stats["declined"] == 0 and stats["ignored"] == 1, (
        f"declined and ignored must be tallied separately for tuning evidence, got {stats}"
    )
    assert stats["accepted"] == 2
    assert stats["hits"] >= 3


def test_reset_by_points_at_a_real_event(ws):
    session = "srev-1"
    assess(ws, session, f"{session}-01", CLARIFY_ARGS)
    record(ws, session, REVERSIBLE_RULE, "accepted")
    session = "srev-2"
    assess(ws, session, f"{session}-01", CLARIFY_ARGS)
    record(ws, session, REVERSIBLE_RULE, "declined")

    reset_by = rule(ws, REVERSIBLE_RULE)["promotion"]["resetBy"]
    events = index(ws)["events"]
    assert reset_by in {e["eventId"] for e in events}, (
        f"resetBy {reset_by!r} must reference a stored event"
    )


# --- C-17: destructive never promotes (zero tolerance) ---


def test_destructive_rule_never_promotes_over_ten_acceptances(ws):
    """SC-005 hard safety criterion, measured at 10 (stronger than its >=5 floor)."""
    for i in range(1, 11):
        session = f"sdest-{i}"
        env = assess(ws, session, f"{session}-01", IMPLEMENT_ARGS)
        sug = env["payload"]["suggestion"]
        assert sug is not None, f"turn {i}: expected a hit on the destructive rule"
        assert sug["autoExecute"] is False, (
            f"turn {i}: a destructive flow must never be flagged for auto-execution"
        )
        proc = record(ws, session, DESTRUCTIVE_RULE, "accepted")
        assert proc.returncode == EXIT_OK, proc.stderr

        r = rule(ws, DESTRUCTIVE_RULE)
        assert r["promotion"]["promoted"] is False, f"turn {i}: promoted became true"
        assert r["state"] != "promoted", f"turn {i}: state became {r['state']}"

    r = rule(ws, DESTRUCTIVE_RULE)
    assert r["confirmationClass"] == "destructive", (
        "confirmationClass is data; the engine must not rewrite it"
    )
    assert r["promotion"]["destructiveExempt"] is True
    assert r["stats"]["accepted"] == 10


def test_destructive_class_is_never_recomputed(ws):
    before = rule(ws, DESTRUCTIVE_RULE)["confirmationClass"]
    for i in range(1, 6):
        session = f"scls-{i}"
        assess(ws, session, f"{session}-01", IMPLEMENT_ARGS)
        record(ws, session, DESTRUCTIVE_RULE, "accepted")
    assert rule(ws, DESTRUCTIVE_RULE)["confirmationClass"] == before


# --- FR-012: user reset ---


def test_reset_single_rule_records_user_reset_at(ws):
    for i in range(1, 4):
        session = f"srst-{i}"
        assess(ws, session, f"{session}-01", CLARIFY_ARGS)
        record(ws, session, REVERSIBLE_RULE, "accepted")
    assert rule(ws, REVERSIBLE_RULE)["state"] == "promoted"

    proc = run(["--action", "reset", "--rule", REVERSIBLE_RULE], ws)
    assert proc.returncode == EXIT_OK, proc.stderr
    r = rule(ws, REVERSIBLE_RULE)
    assert r["promotion"]["consecutive"] == 0
    assert r["promotion"]["promoted"] is False
    assert r["promotion"].get("userResetAt"), "V5.3: a reset must leave a timestamp"
    # The other rule is untouched.
    assert rule(ws, DESTRUCTIVE_RULE)["promotion"].get("userResetAt") in (None, "")


def test_reset_all_clears_every_rule_and_session_suppression(ws):
    session = "sall-1"
    assess(ws, session, f"{session}-01", CLARIFY_ARGS)
    record(ws, session, REVERSIBLE_RULE, "accepted")

    proc = run(["--action", "reset", "--all"], ws)
    assert proc.returncode == EXIT_OK, proc.stderr
    data = index(ws)
    for r in data["rules"]:
        assert r["promotion"]["consecutive"] == 0, f"{r['ruleId']} kept its count"
        assert r["promotion"]["promoted"] is False
    assert not data.get("lastSuggestion"), (
        "V6.8: reset --all must clear session suppression, else the first turn "
        "after a reset stays silent and the user sees no effect"
    )

    # Same session, same situation: must suggest again because suppression was cleared.
    env = assess(ws, session, f"{session}-02", CLARIFY_ARGS)
    assert env["payload"]["suggestion"] is not None, (
        "after reset --all the same session must not stay suppressed"
    )


def test_reset_unknown_rule_reports_rule_not_found(ws):
    proc = run(["--action", "reset", "--rule", "r-999"], ws)
    assert "rule-not-found" in env_of(proc)["errors"]


# --- FR-018: global switch ---


def test_disabled_produces_no_suggestion_and_no_auto_execution(ws):
    for i in range(1, 4):
        session = f"sdis-pre-{i}"
        assess(ws, session, f"{session}-01", CLARIFY_ARGS)
        record(ws, session, REVERSIBLE_RULE, "accepted")
    assert rule(ws, REVERSIBLE_RULE)["state"] == "promoted"

    proc = run(["--action", "config", "--enabled", "false"], ws)
    assert proc.returncode == EXIT_OK, proc.stderr

    suggestions = autoexec = 0
    for i in range(1, 6):
        session = f"sdis-{i}"
        env = assess(ws, session, f"{session}-01", CLARIFY_ARGS)
        sug = env["payload"].get("suggestion")
        if sug:
            suggestions += 1
            autoexec += bool(sug.get("autoExecute"))
    assert suggestions == 0, "SC-009: a disabled mechanism must produce no suggestions"
    assert autoexec == 0, "SC-009: promotion must not keep auto-executing while disabled"
    assert index(ws)["config"]["enabled"] is False


def test_disabled_state_survives_instructions_regeneration(ws):
    run(["--action", "config", "--enabled", "false"], ws)
    # A real installed project keeps its template so the generator can run.
    (ws / ".specify" / "templates" / "instructions-template.md").write_bytes(
        (ROOT / "templates" / "instructions-template.md").read_bytes()
    )
    specify_py = ws / ".specify" / "scripts" / "python"
    specify_py.mkdir(parents=True, exist_ok=True)
    (specify_py / "tools-utils.py").symlink_to(ROOT / "scripts" / "python" / "tools-utils.py")

    proc = subprocess.run(["bash", str(GENERATOR)], cwd=ws, capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr

    assert index(ws)["config"]["enabled"] is False, (
        "SC-009: regeneration rewrites instructions, never the trigger state store"
    )
    env = assess(ws, "safterregen", "safterregen-01", CLARIFY_ARGS)
    assert env["payload"].get("suggestion") is None


def test_reenabling_clears_session_suppression(ws):
    session = "sre-1"
    assess(ws, session, f"{session}-01", CLARIFY_ARGS)
    assess(ws, session, f"{session}-02", CLARIFY_ARGS)  # suppressed
    run(["--action", "config", "--enabled", "false"], ws)
    proc = run(["--action", "config", "--enabled", "true"], ws)
    assert proc.returncode == EXIT_OK, proc.stderr
    assert not index(ws).get("lastSuggestion"), (
        "V6.8: false->true must clear suppression, else the mechanism looks dead"
    )
    env = assess(ws, session, f"{session}-03", CLARIFY_ARGS)
    assert env["payload"]["suggestion"] is not None


# --- C-18: threshold priority chain and floor ---


def test_threshold_below_floor_is_rejected(ws):
    for bad in ("1", "0", "-2"):
        proc = run(["--action", "config", "--threshold", bad], ws)
        assert proc.returncode == EXIT_USAGE, (
            f"--threshold {bad} must exit {EXIT_USAGE}, got {proc.returncode}"
        )
        assert "threshold-below-floor" in env_of(proc)["errors"]
    assert index(ws)["config"]["threshold"] == 3, "a rejected threshold must not be stored"


def test_threshold_floor_of_two_is_accepted(ws):
    proc = run(["--action", "config", "--threshold", "2"], ws)
    assert proc.returncode == EXIT_OK, proc.stderr
    assert index(ws)["config"]["threshold"] == 2


def test_environment_threshold_beats_stored_value(ws, monkeypatch):
    run(["--action", "config", "--threshold", "5"], ws)
    monkeypatch.setenv("SPECKIT_TRIGGER_THRESHOLD", "2")
    proc = run(["--action", "status"], ws)
    assert proc.returncode == EXIT_OK, proc.stderr
    assert env_of(proc)["payload"]["config"]["threshold"] == 2, (
        "V6.2: the environment sits above the stored value"
    )


def test_invalid_environment_threshold_is_ignored(ws, monkeypatch):
    run(["--action", "config", "--threshold", "5"], ws)
    monkeypatch.setenv("SPECKIT_TRIGGER_THRESHOLD", "not-a-number")
    proc = run(["--action", "status"], ws)
    assert proc.returncode == EXIT_OK, proc.stderr
    assert env_of(proc)["payload"]["config"]["threshold"] == 5, (
        "an unusable env value must downgrade silently, not fail the call"
    )


def test_raising_the_threshold_demotes_existing_promotions(ws):
    for i in range(1, 4):
        session = f"sth-{i}"
        assess(ws, session, f"{session}-01", CLARIFY_ARGS)
        record(ws, session, REVERSIBLE_RULE, "accepted")
    assert rule(ws, REVERSIBLE_RULE)["state"] == "promoted"

    proc = run(["--action", "config", "--threshold", "5"], ws)
    assert proc.returncode == EXIT_OK, proc.stderr
    r = rule(ws, REVERSIBLE_RULE)
    assert r["promotion"]["promoted"] is False, (
        "V5.4: a promotion earned under the old threshold must not survive a raise"
    )
    assert r["state"] != "promoted"


# --- record's association rules (V3.4) ---


def test_record_without_a_prior_assess_is_refused(ws):
    proc = record(ws, "snoprior", REVERSIBLE_RULE, "accepted")
    assert proc.returncode == 2, f"expected EXIT_INPUT_ERROR(2), got {proc.returncode}"
    assert "no-prior-assess" in env_of(proc)["errors"]
    assert index(ws)["events"] == [], "V3.4: no half-written event may be stored"


def test_event_ids_follow_the_grammar(ws):
    session = "sevid-1"
    assess(ws, session, f"{session}-01", CLARIFY_ARGS)
    record(ws, session, REVERSIBLE_RULE, "accepted")
    events = index(ws)["events"]
    assert events, "the accepted response must be stored as an event"
    import re
    for e in events:
        assert re.match(r"^[0-9]{8}T[0-9]{6}Z-[0-9]{2}$", e["eventId"]), (
            f"eventId {e['eventId']!r} violates V2.5"
        )
        assert set(e) >= {"eventId", "ruleId", "situationId", "snapshot",
                          "response", "escalated", "created"}


def test_snapshot_over_200_chars_is_rejected(ws):
    session = "ssnap-1"
    assess(ws, session, f"{session}-01", CLARIFY_ARGS)
    # The engine derives the snapshot itself; assert the stored one respects V3.3.
    record(ws, session, REVERSIBLE_RULE, "accepted")
    for e in index(ws)["events"]:
        assert len(e["snapshot"]) <= 200, (
            f"V3.3: snapshot must stay summary-sized, got {len(e['snapshot'])} chars"
        )
