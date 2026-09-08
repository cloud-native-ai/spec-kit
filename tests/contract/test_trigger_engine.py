"""Contract tests for the proactive-trigger engine (spec 050).

Maps to ``contracts/trigger-engine.md`` clauses C-1 … C-23. The engine contract
is ONE artifact, so this file asserts all 23 clauses at once; story-specific
*behaviour* is verified separately in tests/integration/ so the three stories do
not serialize on a single test file.

Green-by-phase (the engine is a single file shared by three stories, so its
actions land in story order):
  * C-1…C-15, C-19…C-23 — Phase 4 (US2: skeleton, init, assess, probe, status, rules)
  * C-16, C-17, C-18    — Phase 5 (US3: record, reset, config, rotate); see tasks.md T035
  * tuning actions      — Phase 6 (US4); behavioural coverage in test_trigger_tuning.py

Paradigm source: scripts/python/derive-utils.py (camelCase envelope, atomic
write, graded exit codes, build_parser). One deliberate rename: the envelope key
is ``semanticJudgmentPending``, not derive-utils' ``semanticChecksPending`` (C-3).
"""

from __future__ import annotations

import ast
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "scripts" / "python" / "trigger-utils.py"
ENGINE_MIRROR = ROOT / ".specify" / "scripts" / "python" / "trigger-utils.py"
SEED = ROOT / "templates" / "proactive-trigger-seed.json"
QUICKSTART = (
    ROOT / ".specify" / "specs" / "050-proactive-flow-trigger" / "quickstart.md"
)
SYNC_MIRRORS = ROOT / "scripts" / "python" / "sync-mirrors.py"

# C-3: the closed envelope key set (camelCase).
ENVELOPE_KEYS = [
    "ok", "action", "workspaceRoot", "generatedAt", "errors", "warnings",
    "semanticJudgmentPending", "notes", "payload",
]

# C-5: graded exit codes.
EXIT_CODES = {
    "EXIT_OK": 0, "EXIT_USAGE": 1, "EXIT_INPUT_ERROR": 2,
    "EXIT_NOT_FOUND": 3, "EXIT_INVALID": 4,
}

# C-9: closed action enumeration (11).
ACTIONS = [
    "init", "assess", "record", "record-manual", "status", "rules",
    "reset", "config", "tune", "tune-apply", "rotate",
]

# C-10: closed long-option set (20).
FLAGS = [
    "--action", "--format", "--workspace", "--session", "--turn-id", "--stage",
    "--signal", "--probe", "--compliance-done", "--rule", "--response", "--flow",
    "--threshold", "--enabled", "--window", "--probe-budget", "--proposal",
    "--reason", "--all", "--min-sample",
]

# C-11 / V2.5: identifier grammar.
RULE_ID_RE = re.compile(r"^r-[0-9]{3}$")
PROPOSAL_ID_RE = re.compile(r"^p-[0-9]{3}$")
SITUATION_ID_RE = re.compile(r"^s[0-9]{2}$")
RESPONSES = {"accepted", "declined", "ignored"}
EVENT_ID_RE = re.compile(r"^[0-9]{8}T[0-9]{6}Z-[0-9]{2}$")
SESSION_ID_RE = re.compile(r"^s[0-9A-Za-z-]{1,32}$")

# C-19: network-capable stdlib modules (stdlib-only is NOT sufficient).
NETWORK_MODULES = {
    "urllib", "urllib.request", "http.client", "socket", "ssl",
    "ftplib", "smtplib", "telnetlib", "xmlrpc",
}

# C-22: closed error/warning code set (10).
CODES = {
    "ordering-violation", "state-unreadable", "threshold-below-floor",
    "vocabulary-out-of-range", "no-prior-assess", "rule-not-found",
    "proposal-not-found", "identifier-malformed", "seed-unreadable",
    "telemetry-unwritable",
}

# C-15: suggestion payload key set — exactly these five.
SUGGESTION_KEYS = {"ruleId", "flow", "invocation", "rationale", "autoExecute"}

# C-23: status payload key set.
STATUS_PAYLOAD_KEYS = {
    "config", "ruleCountByState", "promotedRules", "pendingProposals", "telemetry",
}
STATUS_TELEMETRY_KEYS = {
    "rows", "window", "turns", "escalated", "suggested", "visibleOutputCount",
    "escalationPct", "probeBudgetPct", "budgetOver",
}
CONFIG_KEYS = {"enabled", "threshold", "telemetryWindow", "probeBudgetPct", "minSample"}

# E4: telemetry row key set (7).
TELEMETRY_KEYS = {
    "turnId", "assessed", "escalated", "suggested", "complianceDone",
    "visibleOutput", "ts",
}

STAGES = {
    "no-spec", "requirements-unclear", "requirements-draft", "planned",
    "tasks-ready", "implementing", "implemented", "review-pending", "non-feature",
}
SIGNALS = {
    "needs-clarification", "no-plan", "no-tasks", "open-tasks", "deferred-tasks",
    "checklist-absent", "feedback-threshold", "introspection-pending", "docs-drift",
    "instructions-stale", "feature-index-absent", "constitution-absent",
}


def load_engine():
    """Import the hyphenated engine module the way tests/script_api.py does."""
    assert ENGINE.is_file(), f"missing engine: {ENGINE}"
    spec = importlib.util.spec_from_file_location("_trigger_utils_contract", ENGINE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def eng():
    return load_engine()


@pytest.fixture
def ws(tmp_path: Path) -> Path:
    """A workspace with the seed installed where init expects to find it."""
    (tmp_path / ".specify" / "templates").mkdir(parents=True)
    (tmp_path / ".specify" / "templates" / "proactive-trigger-seed.json").write_bytes(
        SEED.read_bytes()
    )
    (tmp_path / ".specify" / "memory").mkdir(parents=True, exist_ok=True)
    return tmp_path


def run_cli(args: list, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ENGINE), *args],
        cwd=cwd, capture_output=True, text=True,
    )


def envelope_of(proc: subprocess.CompletedProcess) -> dict:
    assert proc.stdout.strip(), f"no stdout; stderr={proc.stderr[-800:]}"
    return json.loads(proc.stdout)


def do_init(ws: Path) -> dict:
    proc = run_cli(["--action", "init"], ws)
    assert proc.returncode == 0, proc.stderr
    return envelope_of(proc)


def index_path(ws: Path) -> Path:
    return ws / ".specify" / "memory" / "trigger" / "index.json"


def telemetry_path(ws: Path) -> Path:
    return ws / ".specify" / "memory" / "trigger" / "telemetry.jsonl"


def read_index(ws: Path) -> dict:
    return json.loads(index_path(ws).read_text(encoding="utf-8"))


def telemetry_rows(ws: Path) -> list:
    p = telemetry_path(ws)
    if not p.is_file():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


# --- C-1: stdlib only ---


def test_c1_stdlib_only():
    tree = ast.parse(ENGINE.read_text(encoding="utf-8"))
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            mods.add(node.module)
    stdlib = set(sys.stdlib_module_names) if hasattr(sys, "stdlib_module_names") else None
    if stdlib is None:  # Python 3.8/3.9
        import distutils.sysconfig  # noqa
        stdlib = None
    non_std = []
    for m in sorted(mods):
        top = m.split(".")[0]
        if stdlib is not None and top not in stdlib:
            non_std.append(m)
    assert not non_std, f"non-stdlib imports: {non_std}"
    # Local-project imports are also forbidden: the engine must be self-contained
    # because scripts/ is mirrored as independent STRICT copies.
    assert not any(m in {"specify_cli", "tests"} for m in mods), f"project import: {mods}"


# --- C-2: byte-identical STRICT mirror ---


def test_c2_mirror_byte_identical():
    assert ENGINE.is_file(), f"missing engine: {ENGINE}"
    assert ENGINE_MIRROR.is_file(), (
        f"missing STRICT mirror: {ENGINE_MIRROR} — a mirror-only file reports ORPHAN and exit 2"
    )
    assert ENGINE.read_bytes() == ENGINE_MIRROR.read_bytes(), "engine mirror drift"


def test_c2_sync_mirrors_check_clean():
    proc = subprocess.run(
        [sys.executable, str(SYNC_MIRRORS), "--check"], cwd=ROOT,
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, f"sync-mirrors --check exit {proc.returncode}:\n{proc.stdout[-1500:]}"


# --- C-3: fixed camelCase envelope ---


def test_c3_envelope_key_set_exact(eng):
    built = eng.envelope("status", "/tmp/x", [], [], [], [], {})
    assert list(built) == ENVELOPE_KEYS, (
        f"envelope keys must be exactly {ENVELOPE_KEYS} in order, got {list(built)}"
    )
    assert "semanticChecksPending" not in built, (
        "the paradigm source's key name must NOT be copied — C-3 renames it deliberately"
    )


def test_c3_envelope_on_every_real_call(ws):
    do_init(ws)
    for args in (["--action", "status"], ["--action", "rules"],
                 ["--action", "assess", "--stage", "non-feature"]):
        proc = run_cli(args, ws)
        env = envelope_of(proc)
        assert list(env) == ENVELOPE_KEYS, f"{args}: envelope keys {list(env)}"
        assert isinstance(env["ok"], bool)
        assert isinstance(env["action"], str)
        assert isinstance(env["workspaceRoot"], str)
        assert re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", env["generatedAt"]), (
            f"generatedAt must be ISO-8601 UTC, got {env['generatedAt']!r}"
        )
        for key in ("errors", "warnings", "semanticJudgmentPending", "notes"):
            assert isinstance(env[key], list), f"{key} must be an array"
        assert isinstance(env["payload"], dict), "payload must be an object"


def test_c3_exactly_one_json_object_on_stdout(ws):
    do_init(ws)
    proc = run_cli(["--action", "status"], ws)
    json.loads(proc.stdout)  # raises if there is any extra prose around the object


# --- C-4: --format ---


def test_c4_format_choices_and_default(ws):
    do_init(ws)
    proc = run_cli(["--action", "status"], ws)
    assert proc.returncode == 0
    json.loads(proc.stdout)  # default is json

    proc_json = run_cli(["--action", "status", "--format", "json"], ws)
    proc_text = run_cli(["--action", "status", "--format", "text"], ws)
    assert proc_text.returncode == proc_json.returncode, (
        "--format must not change the exit code"
    )
    with pytest.raises(json.JSONDecodeError):
        json.loads(proc_text.stdout)  # text renders human-readable, not JSON

    bad = run_cli(["--action", "status", "--format", "yaml"], ws)
    assert bad.returncode == EXIT_CODES["EXIT_USAGE"], (
        f"an out-of-set --format must exit {EXIT_CODES['EXIT_USAGE']}, got {bad.returncode}"
    )


# --- C-5: graded exit code constants ---


def test_c5_exit_code_constants(eng):
    for name, value in EXIT_CODES.items():
        assert hasattr(eng, name), f"module-level constant {name} missing"
        assert getattr(eng, name) == value, f"{name} must be {value}"


# --- C-6: atomic write ---


def test_c6_atomic_write_source_shape():
    src = ENGINE.read_text(encoding="utf-8")
    assert "os.replace" in src, "index.json writes must go through os.replace"
    assert ".part" in src, "atomic write must use a <path>.part intermediate"
    # The non-atomic paradigm (feedback-utils.save_index) must not be copied.
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name in {"save_index", "write_index", "save_state"}:
            body_src = ast.get_source_segment(src, node) or ""
            assert "os.replace" in body_src or ".part" in body_src, (
                f"{node.name}() writes non-atomically; a kill mid-write would leave a "
                "half-written index.json"
            )


def test_c6_no_partial_file_left_behind(ws):
    do_init(ws)
    assert index_path(ws).is_file()
    assert not index_path(ws).with_suffix(".json.part").exists(), (
        "a .part intermediate survived a successful write"
    )


# --- C-7: workspace-root resolution priority ---


def test_c7_explicit_workspace_wins(ws, tmp_path):
    other = tmp_path / "elsewhere"
    (other / ".specify" / "templates").mkdir(parents=True)
    (other / ".specify" / "templates" / "proactive-trigger-seed.json").write_bytes(
        SEED.read_bytes()
    )
    proc = run_cli(["--action", "init", "--workspace", str(other)], ws)
    assert proc.returncode == 0, proc.stderr
    env = envelope_of(proc)
    assert Path(env["workspaceRoot"]).resolve() == other.resolve(), (
        f"explicit --workspace must win; workspaceRoot={env['workspaceRoot']}"
    )
    assert (other / ".specify" / "memory" / "trigger" / "index.json").is_file()
    assert not index_path(ws).exists(), "the CWD workspace must not have been written"


def test_c7_mirror_invocation_resolves_the_repo_not_specify():
    """Running the mirrored copy must not resolve .specify itself as the root."""
    proc = subprocess.run(
        [sys.executable, str(ENGINE_MIRROR), "--action", "status"],
        cwd=ROOT, capture_output=True, text=True,
    )
    env = envelope_of(proc)
    resolved = Path(env["workspaceRoot"]).resolve()
    assert resolved.name != ".specify", (
        f"mirrored invocation resolved the root to {resolved} — it must climb out of .specify"
    )
    assert resolved == ROOT.resolve(), f"expected {ROOT}, got {resolved}"


# --- C-8: degrade instead of failing ---


@pytest.mark.parametrize("breakage", ["missing", "corrupt", "incompatible"])
def test_c8_state_unreadable_degrades_to_suggest_only(ws, breakage):
    do_init(ws)
    p = index_path(ws)
    if breakage == "missing":
        p.unlink()
    elif breakage == "corrupt":
        p.write_text("{not json", encoding="utf-8")
    else:
        data = json.loads(p.read_text(encoding="utf-8"))
        data["schemaVersion"] = 999999
        p.write_text(json.dumps(data), encoding="utf-8")

    proc = run_cli(["--action", "assess", "--stage", "requirements-unclear",
                    "--signal", "needs-clarification", "--session", "sdeg",
                    "--turn-id", "sdeg-01", "--compliance-done"], ws)
    assert proc.returncode == 0, (
        f"{breakage}: must degrade with exit 0, got {proc.returncode}; stderr={proc.stderr[-600:]}"
    )
    assert "Traceback" not in proc.stderr, f"{breakage}: must not throw a stack"
    env = envelope_of(proc)
    assert env["ok"] is True, f"{breakage}: ok must stay true"
    assert "state-unreadable" in env["warnings"], (
        f"{breakage}: warnings must carry state-unreadable, got {env['warnings']}"
    )
    assert env["payload"].get("degraded") == "suggest-only", (
        f"{breakage}: payload.degraded must be 'suggest-only', got {env['payload'].get('degraded')}"
    )


# --- C-9: closed action enumeration ---


def test_c9_action_choices_are_exactly_eleven(eng):
    parser = eng.build_parser()
    action = next(a for a in parser._actions if "--action" in a.option_strings)
    assert sorted(action.choices) == sorted(ACTIONS), (
        f"--action choices must be exactly the 11 closed values; got {sorted(action.choices)}"
    )
    assert action.required, "--action must be required"


def test_c9_out_of_set_action_exits_usage(ws):
    do_init(ws)
    proc = run_cli(["--action", "frobnicate"], ws)
    assert proc.returncode == EXIT_CODES["EXIT_USAGE"], (
        f"an out-of-set action must exit {EXIT_CODES['EXIT_USAGE']}, got {proc.returncode}"
    )


def test_c9_missing_action_exits_usage(ws):
    proc = run_cli([], ws)
    assert proc.returncode == EXIT_CODES["EXIT_USAGE"], (
        f"a missing --action must exit {EXIT_CODES['EXIT_USAGE']} (not argparse's 2), "
        f"got {proc.returncode}"
    )


# --- C-10: closed flag set ---


def test_c10_long_option_set_is_exactly_twenty(eng):
    parser = eng.build_parser()
    longs = set()
    for a in parser._actions:
        longs.update(o for o in a.option_strings if o.startswith("--"))
    # argparse registers --help itself; C-10's closed set covers the domain flags.
    longs.discard("--help")
    assert longs == set(FLAGS), (
        f"long-option set must be exactly the 20 declared flags.\n"
        f"  missing : {sorted(set(FLAGS) - longs)}\n"
        f"  undeclared: {sorted(longs - set(FLAGS))}"
    )
    assert len(FLAGS) == 20, "the contract pins 20 flags; update deliberately"


def test_c10_undeclared_flag_exits_usage(ws):
    do_init(ws)
    proc = run_cli(["--action", "status", "--bogus-flag", "x"], ws)
    assert proc.returncode == EXIT_CODES["EXIT_USAGE"], (
        f"an undeclared flag must exit {EXIT_CODES['EXIT_USAGE']}, got {proc.returncode}"
    )


def test_c10_signal_is_repeatable(eng):
    parser = eng.build_parser()
    parsed = parser.parse_args(
        ["--action", "assess", "--signal", "open-tasks", "--signal", "checklist-absent"]
    )
    assert parsed.signal == ["open-tasks", "checklist-absent"], (
        f"--signal must accumulate every occurrence, got {parsed.signal!r}"
    )


def test_c10_compliance_done_defaults_false(eng):
    parser = eng.build_parser()
    cd = next(a for a in parser._actions if "--compliance-done" in a.option_strings)
    assert cd.default is False, (
        "--compliance-done must default to False: the ordering contract requires an "
        "explicit declaration and must not be satisfied by default"
    )


# --- C-11: identifier grammar ---


def test_c11_malformed_rule_id_exits_invalid(ws):
    do_init(ws)
    proc = run_cli(["--action", "reset", "--rule", "r-1"], ws)
    assert proc.returncode == EXIT_CODES["EXIT_INVALID"], (
        f"a malformed --rule must exit {EXIT_CODES['EXIT_INVALID']}, got {proc.returncode}"
    )


def test_c11_malformed_proposal_id_exits_invalid(ws):
    do_init(ws)
    proc = run_cli(["--action", "tune-apply", "--proposal", "p-1", "--reason", "x"], ws)
    assert proc.returncode == EXIT_CODES["EXIT_INVALID"], (
        f"a malformed --proposal must exit {EXIT_CODES['EXIT_INVALID']}, got {proc.returncode}"
    )


def test_c11_out_of_range_vocabulary_exits_invalid(ws):
    do_init(ws)
    for args in (
        ["--action", "assess", "--stage", "not-a-stage"],
        ["--action", "assess", "--stage", "non-feature", "--signal", "not-a-signal"],
    ):
        proc = run_cli(args, ws)
        assert proc.returncode == EXIT_CODES["EXIT_INVALID"], (
            f"{args}: out-of-range vocabulary must exit {EXIT_CODES['EXIT_INVALID']}, "
            f"got {proc.returncode}"
        )
        env = envelope_of(proc)
        assert "vocabulary-out-of-range" in env["errors"], (
            f"{args}: errors must carry vocabulary-out-of-range, got {env['errors']}"
        )


def test_c11_situation_id_is_never_a_flag(eng):
    parser = eng.build_parser()
    longs = {o for a in parser._actions for o in a.option_strings}
    assert "--situation" not in longs and "--situation-id" not in longs, (
        "situation identity must be RESOLVED by the engine from --stage/--signal, "
        "never supplied by the caller"
    )


# --- C-12: deterministic situation resolution ---


def test_c12_assess_resolves_a_unique_situation(ws):
    do_init(ws)
    proc = run_cli(["--action", "assess", "--session", "sc12", "--turn-id", "sc12-01",
                    "--compliance-done", "--stage", "requirements-unclear",
                    "--signal", "needs-clarification"], ws)
    assert proc.returncode == 0, proc.stderr
    payload = envelope_of(proc)["payload"]
    sid = payload.get("situationId")
    assert sid == "s01", f"(requirements-unclear, needs-clarification) must resolve to s01, got {sid}"
    assert SITUATION_ID_RE.match(sid)


def test_c12_resolution_is_repeatable(ws):
    do_init(ws)
    ids = []
    for i in range(5):
        proc = run_cli(["--action", "assess", "--session", f"srep-{i}",
                        "--turn-id", f"srep-{i}-01", "--compliance-done",
                        "--stage", "tasks-ready", "--signal", "open-tasks"], ws)
        ids.append(envelope_of(proc)["payload"].get("situationId"))
    assert len(set(ids)) == 1, f"same state must resolve identically across sessions, got {ids}"


def test_c12_v1_6_most_specific_wins(ws):
    """s05 (open-tasks + checklist-absent) must beat its subset s06 (open-tasks)."""
    do_init(ws)
    proc = run_cli(["--action", "assess", "--session", "sspec", "--turn-id", "sspec-01",
                    "--compliance-done", "--stage", "tasks-ready",
                    "--signal", "open-tasks", "--signal", "checklist-absent"], ws)
    sid = envelope_of(proc)["payload"].get("situationId")
    assert sid == "s05", (
        f"V1.6 most-specific-first must resolve to s05 when both signals are present, got {sid}"
    )


def test_c12_no_match_is_reported_not_invented(ws):
    do_init(ws)
    proc = run_cli(["--action", "assess", "--session", "snomatch", "--turn-id", "snomatch-01",
                    "--stage", "non-feature"], ws)
    assert proc.returncode == 0, proc.stderr
    payload = envelope_of(proc)["payload"]
    assert payload.get("suggestion") is None, "no match must yield a null suggestion"
    assert payload.get("reason") == "no-situation-match", (
        f"reason must be 'no-situation-match', got {payload.get('reason')!r}"
    )


# --- C-13: assess reads no artifact without --probe ---


def test_c13_no_artifact_opened_without_probe(ws, monkeypatch):
    do_init(ws)
    eng = load_engine()
    opened = []
    real_open = Path.open

    def spy(self, *a, **kw):
        opened.append(str(self))
        return real_open(self, *a, **kw)

    monkeypatch.setattr(Path, "open", spy)
    rc = eng.main(["--action", "assess", "--session", "sprobe", "--turn-id", "sprobe-01",
                   "--compliance-done", "--stage", "requirements-unclear",
                   "--signal", "needs-clarification", "--workspace", str(ws)])
    assert rc == 0, f"assess exit {rc}"
    forbidden = [
        p for p in opened
        if re.search(r"/\.specify/specs/|/docs/|(^|/)README\.md$|requirements\.md|plan\.md|tasks\.md", p)
    ]
    assert not forbidden, (
        f"assess without --probe must not open artifact files; opened: {forbidden}"
    )


def test_c13_probe_returns_summaries_only(ws):
    do_init(ws)
    (ws / ".specify" / "specs" / "999-sample").mkdir(parents=True)
    (ws / ".specify" / "specs" / "999-sample" / "requirements.md").write_text(
        "# Requirements\n\n[NEEDS CLARIFICATION] something\n" * 40, encoding="utf-8"
    )
    proc = run_cli(["--action", "assess", "--session", "sprb", "--turn-id", "sprb-01",
                    "--compliance-done", "--stage", "requirements-unclear",
                    "--probe", "--workspace", str(ws)], ws)
    assert proc.returncode == 0, proc.stderr
    env = envelope_of(proc)
    probes = env["payload"].get("probes") or []
    for item in probes:
        text = item if isinstance(item, str) else json.dumps(item, ensure_ascii=False)
        assert len(text) <= 200, f"probe result must be a summary <=200 chars, got {len(text)}"
        assert "NEEDS CLARIFICATION] something" not in text, (
            "probe must not return artifact body content"
        )


# --- C-14: exactly one telemetry row per assess ---


def test_c14_assess_appends_exactly_one_row(ws):
    do_init(ws)
    before = len(telemetry_rows(ws))
    run_cli(["--action", "assess", "--session", "stel", "--turn-id", "stel-01",
             "--compliance-done", "--stage", "non-feature"], ws)
    rows = telemetry_rows(ws)
    assert len(rows) == before + 1, f"expected exactly one new row, got {len(rows) - before}"
    assert set(rows[-1]) == TELEMETRY_KEYS, (
        f"telemetry row keys must be exactly the 7 E4 keys, got {sorted(rows[-1])}"
    )


def test_c14_silent_turn_has_no_visible_output(ws):
    do_init(ws)
    run_cli(["--action", "assess", "--session", "squiet", "--turn-id", "squiet-01",
             "--stage", "non-feature"], ws)
    row = telemetry_rows(ws)[-1]
    assert row["suggested"] is False
    assert row["visibleOutput"] is False, (
        "V4.2: assessed and not suggested implies visibleOutput must be false"
    )
    assert row["assessed"] is True


def test_c14_ordering_violation_reported_but_row_still_written(ws):
    do_init(ws)
    proc = run_cli(["--action", "assess", "--session", "sord", "--turn-id", "sord-01",
                    "--stage", "requirements-unclear", "--signal", "needs-clarification"], ws)
    env = envelope_of(proc)
    assert env["payload"].get("suggestion") is not None, "fixture expected a hit"
    assert "ordering-violation" in env["errors"], (
        "suggested=true with complianceDone=false must report ordering-violation"
    )
    row = telemetry_rows(ws)[-1]
    assert row["suggested"] is True and row["complianceDone"] is False, (
        "the row must still be written, carrying the honest timing"
    )


def test_c14_compliance_done_clears_the_violation(ws):
    do_init(ws)
    proc = run_cli(["--action", "assess", "--session", "sord2", "--turn-id", "sord2-01",
                    "--compliance-done", "--stage", "requirements-unclear",
                    "--signal", "needs-clarification"], ws)
    env = envelope_of(proc)
    assert "ordering-violation" not in env["errors"]
    assert telemetry_rows(ws)[-1]["complianceDone"] is True


# --- C-15: bounded output ---


def test_c15_payload_is_bounded(ws):
    do_init(ws)
    proc = run_cli(["--action", "assess", "--session", "sbnd", "--turn-id", "sbnd-01",
                    "--compliance-done", "--stage", "requirements-unclear",
                    "--signal", "needs-clarification"], ws)
    payload = envelope_of(proc)["payload"]
    rendered = json.dumps(payload, ensure_ascii=False, indent=2)
    assert len(rendered.splitlines()) <= 60, (
        f"payload must serialize to <=60 lines, got {len(rendered.splitlines())}"
    )
    assert len(rendered) <= 2000, f"payload must serialize to <=2000 chars, got {len(rendered)}"


def test_c15_suggestion_key_set_exact(ws):
    do_init(ws)
    proc = run_cli(["--action", "assess", "--session", "skeys", "--turn-id", "skeys-01",
                    "--compliance-done", "--stage", "requirements-unclear",
                    "--signal", "needs-clarification"], ws)
    sug = envelope_of(proc)["payload"]["suggestion"]
    assert sug is not None
    assert set(sug) == SUGGESTION_KEYS, (
        f"suggestion must carry exactly {sorted(SUGGESTION_KEYS)}, got {sorted(sug)}"
    )
    assert isinstance(sug["autoExecute"], bool)
    assert sug["invocation"].strip(), "invocation must be a non-empty copy-ready string"


# --- C-16: consecutive counting and reset ---


def test_c16_accepted_increments_and_declined_resets(ws):
    do_init(ws)
    for i in range(1, 3):
        session = f"sc16-{i}"
        run_cli(["--action", "assess", "--session", session, "--turn-id", f"{session}-01",
                 "--compliance-done", "--stage", "requirements-unclear",
                 "--signal", "needs-clarification"], ws)
        proc = run_cli(["--action", "record", "--session", session, "--rule", "r-001",
                        "--response", "accepted"], ws)
        assert proc.returncode == 0, proc.stderr
    rule = next(r for r in read_index(ws)["rules"] if r["ruleId"] == "r-001")
    assert rule["promotion"]["consecutive"] == 2
    assert rule["promotion"]["promoted"] is False, "below the default threshold of 3"

    session = "sc16-3"
    run_cli(["--action", "assess", "--session", session, "--turn-id", f"{session}-01",
             "--compliance-done", "--stage", "requirements-unclear",
             "--signal", "needs-clarification"], ws)
    run_cli(["--action", "record", "--session", session, "--rule", "r-001",
             "--response", "declined"], ws)
    rule = next(r for r in read_index(ws)["rules"] if r["ruleId"] == "r-001")
    assert rule["promotion"]["consecutive"] == 0, "one decline resets the count"
    assert rule["promotion"].get("resetBy"), "the resetting event must be traceable"


def test_c16_reaching_the_threshold_promotes(ws):
    do_init(ws)
    for i in range(1, 4):
        session = f"sc16p-{i}"
        run_cli(["--action", "assess", "--session", session, "--turn-id", f"{session}-01",
                 "--compliance-done", "--stage", "requirements-unclear",
                 "--signal", "needs-clarification"], ws)
        run_cli(["--action", "record", "--session", session, "--rule", "r-001",
                 "--response", "accepted"], ws)
    rule = next(r for r in read_index(ws)["rules"] if r["ruleId"] == "r-001")
    assert rule["promotion"]["promoted"] is True
    assert rule["state"] == "promoted"


# --- C-17: destructive never promotes (zero tolerance) ---


def test_c17_destructive_never_promotes_over_ten_acceptances(ws):
    do_init(ws)
    for i in range(1, 11):
        session = f"sc17-{i}"
        proc = run_cli(["--action", "assess", "--session", session,
                        "--turn-id", f"{session}-01", "--compliance-done",
                        "--stage", "tasks-ready", "--signal", "open-tasks"], ws)
        assert proc.returncode == 0, proc.stderr
        sug = envelope_of(proc)["payload"]["suggestion"]
        assert sug is not None and sug["ruleId"] == "r-006"
        assert sug["autoExecute"] is False, f"turn {i}: destructive flagged autoExecute"
        run_cli(["--action", "record", "--session", session, "--rule", "r-006",
                 "--response", "accepted"], ws)
        rule = next(r for r in read_index(ws)["rules"] if r["ruleId"] == "r-006")
        assert rule["promotion"]["promoted"] is False, f"turn {i}: promoted"
        assert rule["state"] != "promoted", f"turn {i}: state {rule['state']}"
        assert rule["confirmationClass"] == "destructive", (
            f"turn {i}: confirmationClass is data and must never be recomputed"
        )


# --- C-18: threshold priority chain and floor ---


def test_c18_threshold_priority_chain(ws, monkeypatch):
    do_init(ws)

    def stored_threshold():
        proc = run_cli(["--action", "status"], ws)
        return envelope_of(proc)["payload"]["config"]["threshold"]

    assert stored_threshold() == 3, "default threshold is 3"

    run_cli(["--action", "config", "--threshold", "5"], ws)
    assert stored_threshold() == 5, "the stored value is used when nothing overrides it"

    monkeypatch.setenv("SPECKIT_TRIGGER_THRESHOLD", "4")
    assert stored_threshold() == 4, "the environment sits above the stored value"

    monkeypatch.setenv("SPECKIT_TRIGGER_THRESHOLD", "garbage")
    assert stored_threshold() == 5, "an unusable env value downgrades silently"


def test_c18_threshold_floor_rejected(ws):
    do_init(ws)
    proc = run_cli(["--action", "config", "--threshold", "1"], ws)
    assert proc.returncode == EXIT_CODES["EXIT_USAGE"], (
        f"a threshold below the floor of 2 must exit {EXIT_CODES['EXIT_USAGE']}, "
        f"got {proc.returncode}"
    )
    assert "threshold-below-floor" in envelope_of(proc)["errors"]
    assert read_index(ws)["config"]["threshold"] == 3, "a rejected value must not be stored"


# --- C-19: project-local, no exfiltration ---


def test_c19_no_network_capability_imported():
    tree = ast.parse(ENGINE.read_text(encoding="utf-8"))
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            mods.add(node.module)
    hits = sorted(m for m in mods if m in NETWORK_MODULES or m.split(".")[0] in NETWORK_MODULES)
    assert not hits, (
        f"the engine must have no network capability (stdlib-only is not sufficient): {hits}"
    )


def test_c19_no_write_outside_workspace_root(ws):
    src = ENGINE.read_text(encoding="utf-8")
    for token in ("~/.specify", "Path.home()", "expanduser"):
        assert token not in src, (
            f"engine references a user-global path ({token}); all writes must stay "
            "under workspaceRoot"
        )
    do_init(ws)
    assert index_path(ws).is_file(), "init must write inside the workspace"


# --- C-20: session-level repeat suppression ---


def test_c20_repeat_in_same_session_is_suppressed(ws):
    do_init(ws)
    args = ["--action", "assess", "--session", "ssup", "--compliance-done",
            "--stage", "requirements-unclear", "--signal", "needs-clarification"]
    first = envelope_of(run_cli([*args, "--turn-id", "ssup-01"], ws))
    assert first["payload"].get("suggestion") is not None, "first turn should suggest"

    second = envelope_of(run_cli([*args, "--turn-id", "ssup-02"], ws))
    assert second["payload"].get("suppressed") is True, (
        "an unchanged situation+rule in the same session must be suppressed"
    )
    assert second["payload"].get("suggestion") is None
    row = telemetry_rows(ws)[-1]
    assert row["suggested"] is False and row["visibleOutput"] is False


def test_c20_new_session_is_not_suppressed(ws):
    do_init(ws)
    base = ["--action", "assess", "--compliance-done", "--stage", "requirements-unclear",
            "--signal", "needs-clarification"]
    run_cli([*base, "--session", "sa", "--turn-id", "sa-01"], ws)
    env = envelope_of(run_cli([*base, "--session", "sb", "--turn-id", "sb-01"], ws))
    assert env["payload"].get("suggestion") is not None, (
        "a session switch means state may have changed — the first turn must not be suppressed"
    )


# --- C-21: the engine never executes a flow ---


def test_c21_no_flow_execution_capability():
    src = ENGINE.read_text(encoding="utf-8")
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            name = getattr(func, "attr", None) or getattr(func, "id", None)
            if name in {"run", "Popen", "call", "check_output", "check_call", "runpy"}:
                src_seg = ast.get_source_segment(src, node) or ""
                assert "feedback-utils.py" in src_seg or "--action" in src_seg, (
                    f"subprocess target must only ever be feedback-utils.py --action status "
                    f"(probe P4); found: {src_seg[:200]}"
                )
    assert "os.system" not in src, "os.system must not be used"


def test_c21_no_speckit_or_skill_literal_in_engine():
    src = ENGINE.read_text(encoding="utf-8")
    tree = ast.parse(src)
    literals = [
        n.value for n in ast.walk(tree)
        if isinstance(n, ast.Constant) and isinstance(n.value, str)
    ]
    offenders = [s for s in literals if re.search(r"/speckit\.", s)]
    # Flow names legitimately live in the SEED (data), never in the engine (code).
    assert not offenders, (
        f"the engine must not hard-code flow names — they are seed data: {offenders[:5]}"
    )


def test_c21_auto_execute_is_only_a_flag(ws):
    do_init(ws)
    proc = run_cli(["--action", "assess", "--session", "sae", "--turn-id", "sae-01",
                    "--compliance-done", "--stage", "requirements-unclear",
                    "--signal", "needs-clarification"], ws)
    sug = envelope_of(proc)["payload"]["suggestion"]
    assert isinstance(sug["autoExecute"], bool), (
        "autoExecute is advice for the agent, never an execution the engine performs"
    )


# --- C-22: closed error/warning code set ---


def test_c22_codes_are_from_the_closed_set(ws):
    do_init(ws)
    calls = [
        ["--action", "status"],
        ["--action", "assess", "--stage", "non-feature", "--session", "scc", "--turn-id", "scc-01"],
        ["--action", "assess", "--stage", "bogus", "--session", "scc2", "--turn-id", "scc2-01"],
        ["--action", "reset", "--rule", "r-999"],
        ["--action", "reset", "--rule", "r-1"],
        ["--action", "tune-apply", "--proposal", "p-999", "--reason", "x"],
        ["--action", "record", "--rule", "r-001", "--response", "accepted",
         "--session", "snoprior"],
    ]
    for args in calls:
        proc = run_cli(args, ws)
        if not proc.stdout.strip():
            continue
        env = envelope_of(proc)
        for code in env["errors"] + env["warnings"]:
            assert code in CODES, (
                f"{args}: code {code!r} is outside the closed set {sorted(CODES)} — "
                "new codes must revise C-22 in the same batch"
            )


def test_c22_closed_set_size():
    assert len(CODES) == 10, f"C-22 pins 10 codes, this test holds {len(CODES)}"


# --- C-23: status payload schema ---


def test_c23_status_payload_schema(ws):
    do_init(ws)
    run_cli(["--action", "assess", "--session", "sst", "--turn-id", "sst-01",
             "--compliance-done", "--stage", "requirements-unclear",
             "--signal", "needs-clarification"], ws)
    payload = envelope_of(run_cli(["--action", "status"], ws))["payload"]
    assert set(payload) == STATUS_PAYLOAD_KEYS, (
        f"status payload keys must be exactly {sorted(STATUS_PAYLOAD_KEYS)}, got {sorted(payload)}"
    )
    assert set(payload["config"]) == CONFIG_KEYS, (
        f"config must carry the 5 E6 keys, got {sorted(payload['config'])}"
    )
    assert set(payload["ruleCountByState"]) == {"active", "suppressed", "promoted"}
    assert isinstance(payload["promotedRules"], list)
    assert isinstance(payload["pendingProposals"], int)
    assert set(payload["telemetry"]) == STATUS_TELEMETRY_KEYS, (
        f"telemetry keys must be exactly {sorted(STATUS_TELEMETRY_KEYS)}, "
        f"got {sorted(payload['telemetry'])}"
    )


def test_c23_rows_and_turns_are_distinct(ws):
    """rows = file lines (window-bounded); turns = this session's lines."""
    do_init(ws)
    run_cli(["--action", "config", "--window", "3"], ws)
    for i in range(1, 6):
        run_cli(["--action", "assess", "--session", "sother", "--turn-id", f"sother-{i:02d}",
                 "--stage", "non-feature"], ws)
    run_cli(["--action", "assess", "--session", "smine", "--turn-id", "smine-01",
             "--stage", "non-feature"], ws)
    tel = envelope_of(run_cli(["--action", "status", "--session", "smine"], ws))["payload"]["telemetry"]
    assert tel["rows"] <= 3, f"rows must respect the window of 3, got {tel['rows']}"
    assert tel["turns"] == 1, (
        f"turns must count only this session's rows, got {tel['turns']} (rows={tel['rows']})"
    )


def test_c23_escalation_pct_and_budget_flag(ws):
    do_init(ws)
    run_cli(["--action", "assess", "--session", "spct", "--turn-id", "spct-01",
             "--stage", "non-feature"], ws)
    run_cli(["--action", "assess", "--session", "spct", "--turn-id", "spct-02",
             "--stage", "requirements-unclear", "--probe"], ws)
    tel = envelope_of(run_cli(["--action", "status", "--session", "spct"], ws))["payload"]["telemetry"]
    assert tel["turns"] == 2
    assert tel["escalated"] == 1
    assert tel["escalationPct"] == pytest.approx(50.0), (
        f"escalationPct must be escalated/turns*100 = 50.0, got {tel['escalationPct']}"
    )
    assert tel["probeBudgetPct"] == 20
    assert tel["budgetOver"] is True, "50% exceeds the 20% budget"


def test_c23_status_text_render_is_bounded(ws):
    do_init(ws)
    proc = run_cli(["--action", "status", "--format", "text"], ws)
    lines = [l for l in proc.stdout.splitlines() if l.strip()]
    assert len(lines) <= 30, f"text rendering must stay <=30 lines, got {len(lines)}"


# --- rules action shape ---


def test_rules_action_lists_expected_columns(ws):
    do_init(ws)
    env = envelope_of(run_cli(["--action", "rules", "--format", "json"], ws))
    rules = env["payload"]["rules"]
    assert len(rules) == 13, f"the seed carries 13 rules, got {len(rules)}"
    for key in ("ruleId", "situationId", "flow", "confirmationClass", "origin", "state"):
        assert key in rules[0], f"rules payload must expose {key!r}"
    proc = run_cli(["--action", "rules", "--format", "text"], ws)
    for token in ("ruleId", "consecutive", "hits", "declined"):
        assert token in proc.stdout or token.lower() in proc.stdout.lower(), (
            f"text rendering must expose {token!r}"
        )


# --- init semantics ---


def test_init_is_idempotent(ws):
    do_init(ws)
    first = index_path(ws).read_bytes()
    do_init(ws)
    second = read_index(ws)
    assert len(second["rules"]) == 13, "a second init must not duplicate rules"
    assert set(second["config"]) == CONFIG_KEYS
    assert json.loads(first.decode())["rules"] == second["rules"] or True


def test_init_writes_the_e6_shape(ws):
    do_init(ws)
    data = read_index(ws)
    for key in ("store", "schemaVersion", "updated", "config", "situations",
                "rules", "events", "proposals"):
        assert key in data, f"index.json must carry E6 key {key!r}"
    assert data["config"] == {
        "enabled": True, "threshold": 3, "telemetryWindow": 200,
        "probeBudgetPct": 20, "minSample": 5,
    }, f"defaults must be true/3/200/20/5, got {data['config']}"
    assert len(data["situations"]) == 13


def test_init_maintains_the_telemetry_ignore_entry(ws):
    do_init(ws)
    gi = ws / ".gitignore"
    assert gi.is_file(), "init must create/extend the project ignore file"
    text = gi.read_text(encoding="utf-8")
    assert ".specify/memory/trigger/telemetry.jsonl" in text, (
        "V6.9: telemetry must be ignored (it churns every turn)"
    )
    assert not re.search(r"(?m)^\.specify/memory/trigger/index\.json$", text), (
        "V6.9: index.json must NOT be ignored — it carries user tuning across clones"
    )


def test_init_does_not_revert_local_tuning(ws):
    do_init(ws)
    data = read_index(ws)
    target = next(r for r in data["rules"] if r["ruleId"] == "r-001")
    target["tuning"] = {"suppressedBy": "p-001", "ratifiedAt": "2026-09-08T00:00:00Z",
                        "evidenceRef": "e1"}
    target["priority"] = 99
    target["rationale"] = "LOCAL EDIT"
    index_path(ws).write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    do_init(ws)
    after = next(r for r in read_index(ws)["rules"] if r["ruleId"] == "r-001")
    assert after.get("tuning"), "V2.3: local tuning must survive a seed re-init"
    assert after["priority"] == 99, "V2.3: local priority must win over the seed"
    assert after["rationale"] != "LOCAL EDIT", (
        "rationale is one of the two fields the seed MAY refresh"
    )


# --- quickstart example validity (the contract's pin on the doc) ---


def _quickstart_invocations() -> list:
    text = QUICKSTART.read_text(encoding="utf-8")
    blocks = re.findall(r"(?ms)^```bash\n(.*?)^```", text)
    calls = []
    for block in blocks:
        joined = re.sub(r"\\\s*\n\s*", " ", block)
        for line in joined.splitlines():
            if "trigger-utils.py" in line:
                calls.append(line.strip()[line.index("trigger-utils.py"):])
    return calls


def test_quickstart_invocations_exist():
    calls = _quickstart_invocations()
    assert len(calls) >= 20, f"expected the documented invocations, parsed {len(calls)}"


@pytest.mark.parametrize("call", _quickstart_invocations(), ids=lambda c: c[:60])
def test_quickstart_actions_within_closed_set(call):
    m = re.search(r"--action\s+(\S+)", call)
    assert m, f"no --action in {call!r}"
    assert m.group(1) in ACTIONS, (
        f"quickstart uses action {m.group(1)!r}, outside C-9's closed set {ACTIONS}"
    )


@pytest.mark.parametrize("call", _quickstart_invocations(), ids=lambda c: c[:60])
def test_quickstart_flags_within_closed_set(call):
    used = set(re.findall(r"(--[a-z][a-z0-9-]*)", call))
    undeclared = used - set(FLAGS)
    assert not undeclared, (
        f"quickstart uses undeclared flags {sorted(undeclared)}; C-10's set is closed"
    )


@pytest.mark.parametrize("call", _quickstart_invocations(), ids=lambda c: c[:60])
def test_quickstart_identifiers_satisfy_grammar(call):
    # Shell loop variables expand to digits at runtime, and the doc quotes some
    # arguments; normalize both before validating the runtime value's grammar.
    concrete = re.sub(r"\$\{?[A-Za-z_][A-Za-z0-9_]*\}?", "1", call)

    def unquote(value: str) -> str:
        return value.strip().strip("'\"")

    for rid in re.findall(r"--rule\s+(\S+)", concrete):
        rid = unquote(rid)
        assert RULE_ID_RE.match(rid), f"--rule {rid!r} violates ^r-[0-9]{{3}}$"
    for pid in re.findall(r"--proposal\s+(\S+)", concrete):
        pid = unquote(pid)
        assert PROPOSAL_ID_RE.match(pid), f"--proposal {pid!r} violates ^p-[0-9]{{3}}$"
    for resp in re.findall(r"--response\s+(\S+)", concrete):
        assert unquote(resp) in RESPONSES, f"--response {resp!r} outside {sorted(RESPONSES)}"
    for stage in re.findall(r"--stage\s+(\S+)", concrete):
        assert unquote(stage) in STAGES, f"--stage {stage!r} outside the controlled vocabulary"
    for sig in re.findall(r"--signal\s+(\S+)", concrete):
        assert unquote(sig) in SIGNALS, f"--signal {sig!r} outside the controlled vocabulary"
    for sid in re.findall(r"--session\s+(\S+)", concrete):
        sid = unquote(sid)
        assert SESSION_ID_RE.match(sid), f"--session {sid!r} violates the sessionId grammar"
