"""US3 integration tests — telemetry bounding and rotation (spec 050).

Covers FR-009 (one row per turn), FR-009a / V4.3 (append-then-truncate as an
always-true invariant) and SC-015 (rotation loses no learning: the promotion
counters are aggregate state on the rule, never recomputed from raw rows), plus
SC-011's silence and escalation-rate readings.

Written RED before the rotate/config actions exist (tasks.md T030 is
parallel-eligible with the US2 implementation).

Mechanism (067 T013, FR-016/FR-020): engine actions are called **in-process** —
``scripts/python/trigger-utils.py`` is importlib-loaded once and its
``main(argv)`` entry point invoked directly — so the sixty-turn loops no longer
pay 60+ interpreter cold starts. Two contract faces are kept intact:

* **workspace equivalence**: every in-process call passes ``--workspace``
  explicitly (an in-process call has no subprocess CWD to resolve from, and the
  pytest CWD must never leak into root resolution);
* **the CLI face stays real**: ``test_cli_subprocess_smoke_pins_payload_and_
  exit_semantics`` runs true subprocess invocations and pins envelope shape /
  exit codes, asserting subprocess ↔ in-process agreement on identical argv.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "scripts" / "python" / "trigger-utils.py"
SEED = ROOT / "templates" / "proactive-trigger-seed.json"

EXIT_OK = 0
CLARIFY_ARGS = ["--stage", "requirements-unclear", "--signal", "needs-clarification"]

# --- in-process engine (067 T013) -------------------------------------------
#
# The engine keeps ALL mutable state in workspace files (`.specify/memory/
# trigger/`); its module level declares immutable constants only, and the
# parser is rebuilt on every `main()` call. A fresh re-exec of the module under
# a new namespace is therefore a complete state reset — `reset_engine_state`
# runs it whenever the runner switches workspace (i.e. at every test case
# boundary), so no module-level state can carry across cases (FR-016).

_RESET_SEQ = iter(range(1 << 30))
_ACTIVE_WS: list[Path | None] = [None]


def _load_engine():
    spec = importlib.util.spec_from_file_location(
        f"_trigger_utils_telemetry_{next(_RESET_SEQ)}", ENGINE
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ENGINE_MOD = _load_engine()


def reset_engine_state() -> None:
    """Explicit module-state reset between workspaces/actions (FR-016, T013).

    Re-executes the engine module in a fresh namespace so any state a future
    engine revision adds at module level starts pristine for the next case.
    """
    global ENGINE_MOD
    ENGINE_MOD = _load_engine()
    _ACTIVE_WS[0] = None


def run(args, cwd) -> subprocess.CompletedProcess:
    """Call one engine action in-process with CLI argv semantics.

    ``cwd`` is the workspace; it is forwarded as ``--workspace`` because the
    in-process call has no subprocess CWD (and the pytest CWD must not be
    consulted). Switching workspace triggers an explicit engine-state reset.
    """
    if _ACTIVE_WS[0] != cwd:
        reset_engine_state()
        _ACTIVE_WS[0] = cwd
    argv = ["--workspace", str(cwd), *args]
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = ENGINE_MOD.main(argv)
    return subprocess.CompletedProcess(argv, code, out.getvalue(), err.getvalue())


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


def env_of(proc) -> dict:
    assert proc.stdout.strip(), f"no stdout; stderr={proc.stderr[-800:]}"
    return json.loads(proc.stdout)


def telemetry_file(ws: Path) -> Path:
    return ws / ".specify" / "memory" / "trigger" / "telemetry.jsonl"


def rows(ws: Path) -> list:
    p = telemetry_file(ws)
    if not p.is_file():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def rules_json(ws: Path) -> str:
    """Byte-level rendering of the rule set — the SC-015 zero-loss comparator."""
    proc = run(["--action", "rules", "--format", "json"], ws)
    assert proc.returncode == EXIT_OK, proc.stderr
    return json.dumps(env_of(proc)["payload"]["rules"], ensure_ascii=False,
                      indent=2, sort_keys=True)


def assess(ws, session, turn, stage_args, compliance=True, probe=False):
    args = ["--action", "assess", "--session", session, "--turn-id", turn, *stage_args]
    if compliance:
        args.append("--compliance-done")
    if probe:
        args.append("--probe")
    proc = run(args, ws)
    assert proc.returncode == EXIT_OK, proc.stderr
    return env_of(proc)


def cli_run(args, cwd: Path) -> subprocess.CompletedProcess:
    """The real CLI face: a true engine subprocess (067 T013 smoke)."""
    return subprocess.run([sys.executable, str(ENGINE), *args], cwd=cwd,
                          capture_output=True, text=True)


def normalized_envelope(raw: str) -> dict:
    """Envelope minus the two fields that legitimately differ between twin
    workspaces (run timestamp) or between root spellings (absolute path)."""
    env = json.loads(raw)
    env.pop("generatedAt")
    env["workspaceRoot"] = "<ws>"
    return env


# --- 067 T013 (FR-020): the CLI subprocess face, pinned ---------------------


def test_cli_subprocess_smoke_pins_payload_and_exit_semantics(tmp_path: Path):
    """≥1 true CLI subprocess run stays in this file (FR-020).

    Pins the engine's CLI contract on a real interpreter subprocess — fixed
    9-key envelope, ok/errors shape, graded exit codes — and asserts the
    in-process runner used by every other test in this file produces the
    *same* payload and exit code for identical argv on a twin workspace. If a
    future engine change makes the two faces diverge, this pin fires.
    """
    ws_cli = tmp_path / "cli"
    ws_ipc = tmp_path / "ipc"
    for d in (ws_cli, ws_ipc):
        (d / ".specify" / "templates").mkdir(parents=True)
        (d / ".specify" / "templates" / "proactive-trigger-seed.json").write_bytes(
            SEED.read_bytes()
        )
        (d / ".specify" / "memory").mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "init", "-q", "."], cwd=d, check=True)

    # init: envelope shape + ok flag, pinned on the subprocess face.
    proc_cli = cli_run(["--action", "init"], ws_cli)
    assert proc_cli.returncode == EXIT_OK, proc_cli.stderr
    init_env = json.loads(proc_cli.stdout)
    assert init_env["ok"] is True
    assert init_env["action"] == "init"
    assert init_env["errors"] == [] and init_env["warnings"] == []
    assert set(init_env) == {
        "ok", "action", "workspaceRoot", "generatedAt", "errors",
        "warnings", "semanticJudgmentPending", "notes", "payload",
    }, "the fixed 9-key envelope shape drifted"

    # Same argv through the in-process entry point: identical envelope.
    proc_ipc = run(["--action", "init"], ws_ipc)
    assert proc_ipc.returncode == proc_cli.returncode
    assert normalized_envelope(proc_ipc.stdout) == normalized_envelope(proc_cli.stdout)

    # assess: silent unrelated turn — payload and exit agree across the faces.
    assess_args = ["--action", "assess", "--session", "ssmoke",
                   "--turn-id", "ssmoke-01", "--stage", "non-feature",
                   "--compliance-done"]
    smoke_cli = cli_run(assess_args, ws_cli)
    assert smoke_cli.returncode == EXIT_OK, smoke_cli.stderr
    assert json.loads(smoke_cli.stdout)["payload"].get("suggestion") is None
    smoke_ipc = run(assess_args, ws_ipc)
    assert smoke_ipc.returncode == smoke_cli.returncode
    assert normalized_envelope(smoke_ipc.stdout) == normalized_envelope(smoke_cli.stdout)

    # Usage-error path: graded exit code 1 with ok=false on both faces.
    bad_cli = cli_run(["--action", "bogus"], ws_cli)
    assert bad_cli.returncode == 1
    assert json.loads(bad_cli.stdout)["ok"] is False
    bad_ipc = run(["--action", "bogus"], ws_ipc)
    assert bad_ipc.returncode == bad_cli.returncode
    assert normalized_envelope(bad_ipc.stdout) == normalized_envelope(bad_cli.stdout)


# --- V4.3: append-then-truncate is an always-true invariant ---


def test_row_count_never_exceeds_the_window(ws):
    proc = run(["--action", "config", "--window", "50"], ws)
    assert proc.returncode == EXIT_OK, proc.stderr
    for i in range(1, 61):
        session = f"swin-{i}"
        assess(ws, session, f"{session}-01", ["--stage", "non-feature"])
        n = len(rows(ws))
        assert n <= 50, (
            f"V4.3 violated after turn {i}: telemetry holds {n} rows, window is 50. "
            "Bounding must hold after EVERY append, not only after an explicit rotate."
        )
    assert len(rows(ws)) == 50, "the window should be exactly filled"


def test_sixty_turns_then_rotate_keeps_at_most_the_window(ws):
    run(["--action", "config", "--window", "50"], ws)
    for i in range(1, 61):
        session = f"srot-{i}"
        assess(ws, session, f"{session}-01", ["--stage", "non-feature"])
    proc = run(["--action", "rotate"], ws)
    assert proc.returncode == EXIT_OK, proc.stderr
    assert len(rows(ws)) <= 50, f"SC-015: expected <=50 rows, got {len(rows(ws))}"


def test_rotate_keeps_the_most_recent_rows(ws):
    run(["--action", "config", "--window", "5"], ws)
    for i in range(1, 11):
        session = f"srec-{i}"
        assess(ws, session, f"{session}-01", ["--stage", "non-feature"])
    run(["--action", "rotate"], ws)
    kept = [r["turnId"] for r in rows(ws)]
    assert kept == [f"srec-{i}-01" for i in range(6, 11)], (
        f"rotation must keep the most recent window, got {kept}"
    )


# --- SC-015: rotation loses no learning ---


def test_rotation_loses_no_rule_state(ws):
    """The discriminator for the 'recompute counters from raw rows' defect."""
    # Build real learning state: two acceptances on a reversible rule.
    for i in range(1, 3):
        session = f"slearn-{i}"
        assess(ws, session, f"{session}-01", CLARIFY_ARGS)
        proc = run(["--action", "record", "--session", session, "--rule", "r-001",
                    "--response", "accepted"], ws)
        assert proc.returncode == EXIT_OK, proc.stderr

    before = rules_json(ws)
    run(["--action", "config", "--window", "50"], ws)
    for i in range(1, 61):
        session = f"sfill-{i}"
        assess(ws, session, f"{session}-01", ["--stage", "non-feature"])
    run(["--action", "rotate"], ws)
    after = rules_json(ws)

    assert before == after, (
        "SC-015: the rule set must be byte-identical across rotation. A difference "
        "means promotion counters were recomputed from telemetry rows instead of "
        "being carried as aggregate state on the rule (V4.4)."
    )


def test_rotate_does_not_touch_index_file(ws):
    for i in range(1, 4):
        session = f"sidx-{i}"
        assess(ws, session, f"{session}-01", CLARIFY_ARGS)
        run(["--action", "record", "--session", session, "--rule", "r-001",
            "--response", "accepted"], ws)

    index_path = ws / ".specify" / "memory" / "trigger" / "index.json"
    before = json.loads(index_path.read_text(encoding="utf-8"))
    before_rules = before["rules"]
    before_events = before["events"]

    run(["--action", "config", "--window", "2"], ws)
    run(["--action", "rotate"], ws)

    after = json.loads(index_path.read_text(encoding="utf-8"))
    assert after["rules"] == before_rules, "V4.4: rotate must not alter rules"
    assert after["events"] == before_events, "V4.4: rotate must not alter events"


def test_consecutive_survives_window_shrink(ws):
    for i in range(1, 4):
        session = f"sshk-{i}"
        assess(ws, session, f"{session}-01", CLARIFY_ARGS)
        run(["--action", "record", "--session", session, "--rule", "r-001",
            "--response", "accepted"], ws)
    data = json.loads((ws / ".specify" / "memory" / "trigger" / "index.json")
                      .read_text(encoding="utf-8"))
    promoted = next(r for r in data["rules"] if r["ruleId"] == "r-001")
    assert promoted["promotion"]["consecutive"] == 3

    run(["--action", "config", "--window", "1"], ws)
    run(["--action", "rotate"], ws)
    assert len(rows(ws)) <= 1

    data = json.loads((ws / ".specify" / "memory" / "trigger" / "index.json")
                      .read_text(encoding="utf-8"))
    after = next(r for r in data["rules"] if r["ruleId"] == "r-001")
    assert after["promotion"]["consecutive"] == 3, (
        "shrinking the telemetry window must not erase the promotion counter"
    )
    assert after["state"] == "promoted"


# --- SC-011: silence and escalation rate ---


def test_unrelated_turns_produce_no_visible_output(ws):
    """quickstart scenario 3: 20 unrelated turns stay silent."""
    for i in range(1, 21):
        session = f"squiet-{i}"
        env = assess(ws, session, f"{session}-01", ["--stage", "non-feature"])
        assert env["payload"].get("suggestion") is None, (
            f"turn {i}: an unrelated turn must not produce a suggestion"
        )

    tel = rows(ws)
    assert len(tel) == 20, f"expected one row per turn, got {len(tel)}"
    assert all(r["suggested"] is False for r in tel)
    assert all(r["visibleOutput"] is False for r in tel), (
        "SC-011: turns with no applicable flow must have zero user-visible output"
    )
    assert all(r["escalated"] is False for r in tel), (
        "SC-011: without --probe nothing may escalate"
    )

    proc = run(["--action", "status", "--session", "squiet-20"], ws)
    payload = env_of(proc)["payload"]["telemetry"]
    assert payload["visibleOutputCount"] == 0
    assert payload["escalationPct"] == pytest.approx(0.0)
    assert payload["budgetOver"] is False


def test_escalation_rate_is_computed_over_session_turns(ws):
    session = "sesc"
    for i in range(1, 11):
        probe = i <= 2  # 2 of 10 escalate
        assess(ws, session, f"{session}-{i:02d}", ["--stage", "non-feature"], probe=probe)

    proc = run(["--action", "status", "--session", session], ws)
    tel = env_of(proc)["payload"]["telemetry"]
    assert tel["turns"] == 10, f"expected 10 session turns, got {tel['turns']}"
    assert tel["escalated"] == 2
    assert tel["escalationPct"] == pytest.approx(20.0)
    assert tel["probeBudgetPct"] == 20
    assert tel["budgetOver"] is False, "20% is at the budget, not over it"


def test_escalation_over_budget_is_flagged(ws):
    session = "sover"
    for i in range(1, 5):
        assess(ws, session, f"{session}-{i:02d}", ["--stage", "non-feature"],
               probe=(i <= 3))
    tel = env_of(run(["--action", "status", "--session", session], ws))["payload"]["telemetry"]
    assert tel["escalationPct"] == pytest.approx(75.0)
    assert tel["budgetOver"] is True


def test_probe_budget_is_configurable(ws):
    proc = run(["--action", "config", "--probe-budget", "50"], ws)
    assert proc.returncode == EXIT_OK, proc.stderr
    data = json.loads((ws / ".specify" / "memory" / "trigger" / "index.json")
                      .read_text(encoding="utf-8"))
    assert data["config"]["probeBudgetPct"] == 50


def test_every_assess_writes_exactly_one_row(ws):
    for i in range(1, 8):
        session = f"sone-{i}"
        before = len(rows(ws))
        assess(ws, session, f"{session}-01", CLARIFY_ARGS)
        assert len(rows(ws)) == before + 1, f"turn {i} did not append exactly one row"


def test_telemetry_is_git_ignored_but_index_is_not(ws):
    gi = ws / ".gitignore"
    assert gi.is_file(), "init must maintain the project ignore file"
    text = gi.read_text(encoding="utf-8")
    assert ".specify/memory/trigger/telemetry.jsonl" in text, (
        "V6.9: per-turn telemetry churns and must be ignored"
    )
    proc = subprocess.run(
        ["git", "check-ignore", "-q", ".specify/memory/trigger/index.json"],
        cwd=ws, capture_output=True, text=True,
    )
    assert proc.returncode != 0, (
        "V6.9: index.json carries user tuning across clones and must stay tracked"
    )
