"""Contract tests for the exec-quant engine (Feature 059).

Engine: ``scripts/python/exec-quant.py`` — behavior owner of
``.specify/specs/059-exec-quant-recording/contracts/exec-quant-cli.md``.
Subprocess CLI invocation form (the engine is a literal command line in the
compiled wrap-up faces, so the contract is tested the way it runs).

File partitions (one write-owner per contract section; append, never rewrite
another partition's tests):

* **US1 partition** (T003): ``contracts/exec-quant-cli.md`` 通用参数 + 动作一
  ``collect``, and ``data-model.md`` V1/V2/V3.
* **US2 partition** (T010): 动作二 ``list-records`` + 动作三 ``score``.
* **US3 partition** (T013): 交叉约束 + V4–V8.

Red-First 取证: the US1/US2 partitions were run RED before the engine existed
(evidence: ``.specify/specs/059-exec-quant-recording/notes/red-first-evidence.md``);
the US3 partition is a migration/regression net authored after its subjects
(tasks.md A-tasks-6).

Host-determination hermeticity: agent resolution walks the real parent chain,
which differs per host. Tests that need a DETERMINISTIC host identity spawn the
engine as a child of a process whose OS argv[0] basename impersonates a known
host CLI (``exec -a qodercli``); tests that only audit the field-binary law
tolerate any resolution value. One D7 branch is NOT hermetically testable on a
qoder-ancestored host (a foreign host name still finds the real qodercli further
up the chain), so the whole-group degrade is covered by the missing-config-face
test plus the real-host smoke (T009).
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

_HERE = Path(__file__).resolve()
REPO_ROOT = _HERE.parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "exec-quant.py"
RUN_DETERMINATION = REPO_ROOT / "scripts" / "python" / "run-determination.py"

#: Framework-repo store the two-hats guard protects (every test passes an
#: explicit --workspace-root, so nothing may land here as a side effect).
FRAMEWORK_STORE = REPO_ROOT / ".specify" / "memory" / "exec-quant"

# 063 C-22 (2026-10-20): args-manifest joins every wrap-up engine's closed set
# (same-batch amendment; the docstring below had already drifted at 059 —
# collect-dispatch landed without a write-back, per the 056 owner contract's
# historical note).
# 068 C-18 (2026-10-22, same-batch amendment): the explicit `aggregate` action
# joins the closed set (US3 summary leg; registered in ACTIONS + parser).
ACTIONS_CLOSED_SET = {"collect", "list-records", "score", "collect-dispatch", "args-manifest",
                      "aggregate"}
KIND = "speckit.exec-quant"  # [[STR-001]]
NOT_EVALUATED = "not_evaluated"  # [[STR-002]]
PROVENANCE_DOMAIN = {"measured", "carried", "user-given", "configured"}

#: Declared measurable fields (data-model §1.1): each is either the literal
#: ``not_evaluated`` or a ``{"value", "provenance"}`` object.
MEASURABLE_PATHS = (
    ("agent", "name"), ("agent", "version"), ("agent", "binary"),
    ("agent", "argv"), ("agent", "cwd"),
    ("llm", "model"), ("llm", "context_window"), ("llm", "reasoning_effort"),
    ("llm", "config_source"), ("llm", "connection_evidence"),
    ("quality", "elapsed_ms"), ("quality", "tokens"), ("quality", "satisfaction"),
    ("quality", "exit_code"),
    ("qualification",),
)


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _snapshot(store: Path):
    if not store.is_dir():
        return None
    return sorted((p.name, p.stat().st_size) for p in store.rglob("*") if p.is_file())


@pytest.fixture(autouse=True)
def framework_store_untouched():
    before = _snapshot(FRAMEWORK_STORE)
    yield
    after = _snapshot(FRAMEWORK_STORE)
    assert after == before, (
        f"a test wrote into the framework repository's exec-quant store: "
        f"added={sorted(set(after or []) - set(before or []))}"
    )


@pytest.fixture
def ws(tmp_path: Path) -> Path:
    root = tmp_path / "ws"
    (root / ".specify" / "memory" / "session").mkdir(parents=True)
    return root


@pytest.fixture
def fake_home(tmp_path: Path) -> Path:
    home = tmp_path / "home"
    home.mkdir()
    return home


def run_engine(args, env_home: Path | None = None, extra_env: dict | None = None):
    """Run the engine CLI in subprocess form."""
    env = dict(os.environ)
    if env_home is not None:
        env["HOME"] = str(env_home)
    if extra_env:
        env.update({k: str(v) for k, v in extra_env.items()})
    argv = [sys.executable, str(ENGINE)] + [str(a) for a in args]
    return subprocess.run(argv, capture_output=True, text=True, timeout=240, env=env)


def run_via_host_wrapper(args, env_home: Path, host_name: str = "qodercli",
                         extra_env: dict | None = None,
                         wrapper_args: tuple = ()) -> "subprocess.CompletedProcess":
    """Spawn the engine as a child of a process impersonating a host CLI.

    ``exec -a <host_name>`` keeps the OS-level argv[0] (visible in
    /proc/<pid>/cmdline) at ``<host_name>`` while the program itself is a tiny
    runner that execs the engine in subprocess form — so D8 agent resolution is
    deterministic on any Linux host.
    """
    runner = env_home.parent / "host_runner.py"
    engine_argv = [sys.executable, str(ENGINE)] + [str(a) for a in args]
    runner.write_text(
        "import json, subprocess, sys\n"
        f"argv = {json.dumps(engine_argv)}\n"
        "proc = subprocess.run(argv, capture_output=True, text=True)\n"
        "sys.stdout.write(proc.stdout)\n"
        "sys.stderr.write(proc.stderr)\n"
        "sys.exit(proc.returncode)\n",
        encoding="utf-8",
    )
    env = dict(os.environ)
    env["HOME"] = str(env_home)
    if extra_env:
        env.update({k: str(v) for k, v in extra_env.items()})
    extra = " ".join(f'"{a}"' for a in wrapper_args)
    cmd = ["bash", "-c",
           f'exec -a {host_name} "{sys.executable}" "{runner}" {extra}'.rstrip()]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=240, env=env)


def store_dir(ws: Path) -> Path:
    return ws / ".specify" / "memory" / "exec-quant"


def records_dir(ws: Path) -> Path:
    return store_dir(ws) / "records"


def scores_dir(ws: Path) -> Path:
    return store_dir(ws) / "scores"


def records_path(ws: Path) -> Path:
    """Legacy single-file store, readable but never written since the split."""
    return store_dir(ws) / "records.jsonl"


def scores_path(ws: Path) -> Path:
    return store_dir(ws) / "scores.jsonl"


def read_jsonl(path: Path) -> list:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


def read_records(ws: Path) -> list:
    entries = read_jsonl(records_path(ws)) if records_path(ws).is_file() else []
    if records_dir(ws).is_dir():
        entries += [json.loads(path.read_text(encoding="utf-8"))
                    for path in sorted(records_dir(ws).glob("*.json"))]
    return entries


def read_scores(ws: Path) -> list:
    entries = read_jsonl(scores_path(ws)) if scores_path(ws).is_file() else []
    if scores_dir(ws).is_dir():
        entries += [json.loads(path.read_text(encoding="utf-8"))
                    for path in sorted(scores_dir(ws).glob("*.json"))]
    return entries


def record_files(ws: Path) -> list:
    return sorted(records_dir(ws).glob("*.json")) if records_dir(ws).is_dir() else []


def store_snapshot(ws: Path) -> dict:
    root = store_dir(ws)
    if not root.is_dir():
        return {}
    return {p.relative_to(root).as_posix(): p.read_bytes()
            for p in root.rglob("*")
            if p.is_file() and p.name != ".write.lock"}


def records_snapshot(ws: Path) -> dict:
    return {name: payload for name, payload in store_snapshot(ws).items()
            if name == "records.jsonl" or name.startswith("records/")}


def scores_snapshot(ws: Path) -> dict:
    return {name: payload for name, payload in store_snapshot(ws).items()
            if name == "scores.jsonl" or name.startswith("scores/")}


def collect_args(ws: Path, unit_id="/speckit.plan", **over):
    args = ["--action", "collect", "--workspace-root", str(ws), "--unit-id", unit_id]
    for key, value in over.items():
        if value is None:
            continue
        args += ["--" + key.replace("_", "-"), str(value)]
    return args


def make_determination(ws: Path, unit_id: str, run_id: str, extra=()):
    """Create a real determination record for ``unit_id`` via the adjacent
    engine's own CLI (the honest upstream form — no fabricated store files)."""
    return subprocess.run(
        [sys.executable, str(RUN_DETERMINATION),
         "--action", "determine", "--workspace-root", str(ws),
         "--unit-id", unit_id, "--run-id", run_id,
         "--complexity", "complex", "--qualification", "qualified",
         "--elapsed-ms", "81234", *[str(e) for e in extra]],
        capture_output=True, text=True, timeout=120, check=False)


def assert_no_blanks(node, path="$"):
    """Zero null / zero empty string anywhere (V2 global invariants)."""
    if node is None:
        raise AssertionError(f"null at {path}")
    if isinstance(node, str) and node == "":
        raise AssertionError(f"empty string at {path}")
    if isinstance(node, dict):
        for key, value in node.items():
            assert_no_blanks(value, f"{path}.{key}")
    elif isinstance(node, list):
        for i, value in enumerate(node):
            assert_no_blanks(value, f"{path}[{i}]")


def assert_field_binary_law(record):
    """V2: every declared measurable field is a value object or the literal
    ``not_evaluated``; provenance closed-domain; companion invariants."""
    for path in MEASURABLE_PATHS:
        node = record
        for key in path:
            assert isinstance(node, dict) and key in node, f"missing key {'.'.join(path)}"
            node = node[key]
        if node == NOT_EVALUATED:
            continue
        assert isinstance(node, dict), f"{'.'.join(path)} must be value-object or literal: {node!r}"
        assert set(node.keys()) == {"value", "provenance"}, f"{'.'.join(path)} keys {set(node.keys())}"
        assert node["provenance"] in PROVENANCE_DOMAIN, f"{'.'.join(path)} provenance {node['provenance']!r}"
        assert node["value"] is not None and node["value"] != "", f"{'.'.join(path)} blank value"

    ep = record["llm"]["endpoint_candidates"]
    assert ep == NOT_EVALUATED or (isinstance(ep, dict) and all(
        isinstance(k, str) and k and isinstance(v, str) and v for k, v in ep.items()))

    errors = record["quality"]["errors"]
    assert errors == NOT_EVALUATED or (isinstance(errors, list) and all(
        isinstance(e, dict) and set(e.keys()) == {"source", "count"}
        and isinstance(e["source"], str) and e["source"]
        and isinstance(e["count"], int) and e["count"] >= 0 for e in errors))

    assert isinstance(record["truncated"], list)

    assert_no_blanks(record)


def load_single_record(ws: Path) -> dict:
    records = read_records(ws)
    assert len(records) == 1, f"expected 1 record, found {len(records)}"
    return records[0]


# ===========================================================================
# US1 partition — contracts/exec-quant-cli.md 通用参数 + 动作一; V1/V2/V3
# ===========================================================================

class TestActionClosedSet:
    """argparse choices closed set == the engine's ACTIONS (4 domain actions from
    059/047 + args-manifest per 063 C-22; see ACTIONS_CLOSED_SET above)."""

    def test_choices_exact(self):
        result = run_engine(["--action", "totally-bogus"])
        assert result.returncode == 2, result.stderr
        assert "usage:" in result.stderr, f"not an argparse usage error: {result.stderr!r}"
        match = re.search(r"choose from (.+?)\)", result.stderr)
        assert match, f"no choices listing in stderr: {result.stderr!r}"
        choices = set(re.findall(r"'([^']+)'", match.group(1)))
        assert choices == ACTIONS_CLOSED_SET

    def test_missing_action_is_usage_error(self):
        result = run_engine([])
        assert result.returncode == 2
        assert "usage:" in result.stderr


class TestCollectContract:
    """动作一 collect: storage bootstrap, identity, run-id resolution."""

    def test_collect_writes_storage_and_record(self, ws, fake_home):
        result = run_engine(collect_args(ws), env_home=fake_home)
        assert result.returncode == 0, result.stderr
        assert records_dir(ws).is_dir()
        assert scores_dir(ws).is_dir()
        entry_files = record_files(ws)
        assert len(entry_files) == 1, f"expected one entry file, found {entry_files}"
        assert re.fullmatch(r"\d{8}T\d{12}Z-[0-9a-f]{8}\.json", entry_files[0].name), (
            f"entry filename must be timestamp-based: {entry_files[0].name}")
        record = load_single_record(ws)
        # V3: kind literal + schema_version (061 v2)
        assert record["kind"] == KIND
        assert record["schema_version"] == 2
        assert record["unit_id"] == "/speckit.plan"
        assert record["unit_type"] == "command"
        # 061 v2: config group + exit_code leaves are explicit markers
        assert set(record["config"].keys()) == {
            "config_id", "source_chain", "method_requested", "method_resolved",
            "mode", "cli", "model", "reasoning_effort", "context_window",
            "extra_flags", "snapshot"}
        assert all(value == NOT_EVALUATED for value in record["config"].values())
        assert record["quality"]["exit_code"] == NOT_EVALUATED
        # V1: run_id non-empty
        assert isinstance(record["run_id"], str) and record["run_id"]
        # collect text output names run_id and the landing path
        assert record["run_id"] in result.stdout
        assert str(records_dir(ws)) in result.stdout

    def test_collect_explicit_run_id(self, ws, fake_home):
        result = run_engine(collect_args(ws, run_id="run-x1"), env_home=fake_home)
        assert result.returncode == 0, result.stderr
        record = load_single_record(ws)
        assert record["run_id"] == "run-x1"
        assert record["run_id_resolution"] == "explicit"

    def test_collect_synthesized_without_determination(self, ws, fake_home):
        result = run_engine(collect_args(ws), env_home=fake_home)
        assert result.returncode == 0, result.stderr
        record = load_single_record(ws)
        assert record["run_id_resolution"] == "synthesized"
        for field in ("elapsed_ms", "tokens", "satisfaction"):
            assert record["quality"][field] == NOT_EVALUATED
        assert record["quality"]["errors"] == NOT_EVALUATED
        assert record["qualification"] == NOT_EVALUATED

    def test_collect_adopts_recent_determination_run_id(self, ws, fake_home):
        made = make_determination(ws, "/speckit.plan", "run-001")
        assert made.returncode == 0, made.stderr
        result = run_engine(collect_args(ws), env_home=fake_home)
        assert result.returncode == 0, result.stderr
        record = load_single_record(ws)
        assert record["run_id_resolution"] == "adopted"
        assert record["run_id"] == "run-001"
        # carried fields mirror the determination record exactly (V7 adopted)
        assert record["quality"]["elapsed_ms"] == {"value": 81234, "provenance": "carried"}
        assert record["qualification"] == {"value": "qualified", "provenance": "carried"}
        # token measurement absent in the determination record → explicit marker
        assert record["quality"]["tokens"] == NOT_EVALUATED

    def test_collect_explicit_run_id_carries_matching_record(self, ws, fake_home):
        made = make_determination(ws, "/speckit.plan", "run-001")
        assert made.returncode == 0, made.stderr
        result = run_engine(collect_args(ws, run_id="run-001"), env_home=fake_home)
        assert result.returncode == 0, result.stderr
        record = load_single_record(ws)
        assert record["run_id_resolution"] == "explicit"
        assert record["quality"]["elapsed_ms"] == {"value": 81234, "provenance": "carried"}

    def test_collect_ignores_determination_outside_recent_window(self, ws, fake_home):
        made = make_determination(ws, "/speckit.plan", "run-stale")
        assert made.returncode == 0, made.stderr
        entry = next((ws / ".specify" / "memory" / "session").glob("*run-determination*.md"))
        text = entry.read_text(encoding="utf-8")
        stamp = re.search(r'"determined_at": "([^"]+)"', text).group(1)
        stale = (datetime.now(timezone.utc) - timedelta(minutes=120)).strftime(
            "%Y-%m-%dT%H:%M:%SZ")
        # anchor on the KEY: frontmatter `created:` carries the same timestamp
        # and must stay untouched
        entry.write_text(
            text.replace(f'"determined_at": "{stamp}"', f'"determined_at": "{stale}"', 1),
            encoding="utf-8")
        result = run_engine(collect_args(ws), env_home=fake_home)
        assert result.returncode == 0, result.stderr
        record = load_single_record(ws)
        assert record["run_id_resolution"] == "synthesized"
        assert record["run_id"] != "run-stale"
        assert record["quality"]["elapsed_ms"] == NOT_EVALUATED

    def test_collect_counts_errors_from_declared_sources(self, ws, fake_home):
        (ws / "names-baseline.txt").write_text("", encoding="utf-8")
        (ws / "names-current.txt").write_text(
            "tests/contract/test_new_guard.py::test_red\n", encoding="utf-8")
        made = make_determination(
            ws, "/speckit.plan", "run-err",
            extra=("--declared-check", "pytest",
                   "--names-baseline", str(ws / "names-baseline.txt"),
                   "--names-current", str(ws / "names-current.txt"),
                   "--unresolved-red", "true", "--red-source", "engine_nonzero_exit"))
        assert made.returncode == 0, made.stderr
        result = run_engine(collect_args(ws, run_id="run-err"), env_home=fake_home)
        assert result.returncode == 0, result.stderr
        record = load_single_record(ws)
        errors = record["quality"]["errors"]
        assert isinstance(errors, list), f"errors must enumerate declared sources: {errors!r}"
        by_source = {e["source"]: e["count"] for e in errors}
        assert by_source.get("run-determination.failed_set_diff") == 1
        assert by_source.get("run-determination.unresolved_red") == 1

    def test_collect_idempotent_duplicate(self, ws, fake_home):
        first = run_engine(collect_args(ws, run_id="dup-1"), env_home=fake_home)
        assert first.returncode == 0, first.stderr
        second = run_engine(collect_args(ws, run_id="dup-1"), env_home=fake_home)
        assert second.returncode == 0, second.stderr
        assert "duplicate" in (second.stdout + second.stderr).lower()
        assert len(read_records(ws)) == 1
        assert len(record_files(ws)) == 1

    def test_collect_write_failure_exits_1_with_visible_stderr(self, ws, fake_home):
        records_dir(ws).parent.mkdir(parents=True, exist_ok=True)
        records_dir(ws).write_text("occupied", encoding="utf-8")  # a file where a dir must be
        result = run_engine(collect_args(ws), env_home=fake_home)
        assert result.returncode == 1
        assert result.stderr.strip(), "failure must be visible on stderr"


class TestIdentityForms:
    """V1: unit_id closed forms and unit-type agreement."""

    def test_invalid_unit_id_is_usage_error(self, ws, fake_home):
        result = run_engine(collect_args(ws, unit_id="bogus"), env_home=fake_home)
        assert result.returncode == 2
        assert "usage:" in result.stderr

    def test_missing_unit_id_is_usage_error(self, ws, fake_home):
        result = run_engine(["--action", "collect", "--workspace-root", str(ws)],
                            env_home=fake_home)
        assert result.returncode == 2
        assert "usage:" in result.stderr

    def test_unit_type_mismatch_is_usage_error(self, ws, fake_home):
        result = run_engine(collect_args(ws, unit_type="skill"), env_home=fake_home)
        assert result.returncode == 2
        assert "usage:" in result.stderr

    def test_skill_form_infers_skill_type(self, ws, fake_home):
        result = run_engine(collect_args(ws, unit_id="skill:study-project"),
                            env_home=fake_home)
        assert result.returncode == 0, result.stderr
        assert load_single_record(ws)["unit_type"] == "skill"

    def test_custom_form_infers_custom_unit_type(self, ws, fake_home):
        result = run_engine(collect_args(ws, unit_id="custom:myowner/myunit"),
                            env_home=fake_home)
        assert result.returncode == 0, result.stderr
        assert load_single_record(ws)["unit_type"] == "custom-unit"

    def test_custom_form_accepts_explicit_custom_unit_type(self, ws, fake_home):
        result = run_engine(collect_args(ws, unit_id="custom:myowner/myunit",
                                         unit_type="custom-unit"), env_home=fake_home)
        assert result.returncode == 0, result.stderr

    def test_collect_rejects_agent_form(self, ws, fake_home):
        result = run_engine(collect_args(ws, unit_id="agent:qoder-guide"),
                            env_home=fake_home)
        assert result.returncode == 2
        assert "collect-dispatch" in result.stderr

    def test_agent_unit_type_is_a_valid_listing_choice(self, ws, fake_home):
        result = run_engine(["--action", "list-records", "--workspace-root", str(ws),
                             "--unit-type", "agent", "--format", "json"],
                            env_home=fake_home)
        assert result.returncode == 0, result.stderr
        assert json.loads(result.stdout) == []


class TestFieldBinaryLaw:
    """V2 over a degraded bare-workspace collect."""

    def test_degraded_record_holds_the_law(self, ws, fake_home):
        result = run_engine(collect_args(ws), env_home=fake_home)
        assert result.returncode == 0, result.stderr
        assert_field_binary_law(load_single_record(ws))


class TestLLMCollection:
    """D6 endpoint candidates (whitelist, origin-only) + D7 qoder adapter."""

    def test_endpoint_candidates_origin_only(self, ws, fake_home):
        # the whitelist is read from the HOST process environ, so the values
        # must be planted on the impersonated host (the wrapper), not the
        # engine's own env
        result = run_via_host_wrapper(
            collect_args(ws),
            env_home=fake_home,
            extra_env={"ANTHROPIC_BASE_URL": "https://user:pw@api.example.com/v1/path?k=1",
                       "DASHSCOPE_API_URL": "https://dashscope.example.com/compatible/v1"},
        )
        assert result.returncode == 0, result.stderr
        record = load_single_record(ws)
        endpoints = record["llm"]["endpoint_candidates"]
        assert isinstance(endpoints, dict), f"expected candidate mapping: {endpoints!r}"
        assert endpoints["ANTHROPIC_BASE_URL"] == "https://api.example.com"
        assert endpoints["DASHSCOPE_API_URL"] == "https://dashscope.example.com"
        serialized = json.dumps(record)
        assert "user:pw" not in serialized and "/v1/path" not in serialized

    def test_endpoint_candidates_absent_marker(self, ws, fake_home):
        env = {k: "" for k in ("ANTHROPIC_BASE_URL", "ANTHROPIC_URL", "OPENAI_BASE_URL",
                               "OPENAI_URL", "DASHSCOPE_API_URL",
                               "ALIYUN_ANTHROPIC_COMPATIBLE_URL",
                               "ALIYUN_OPENAI_COMPATIBLE_URL",
                               "CLAUDE_ALIBABA_BASE_URL", "CLAUDE_OFFICIAL_BASE_URL")}
        result = run_via_host_wrapper(collect_args(ws), env_home=fake_home, extra_env=env)
        assert result.returncode == 0, result.stderr
        assert load_single_record(ws)["llm"]["endpoint_candidates"] == NOT_EVALUATED

    def test_qoder_adapter_reads_config_face(self, ws, fake_home):
        settings = fake_home / ".qoder" / "settings.json"
        settings.parent.mkdir(parents=True)
        settings.write_text(json.dumps({
            "model": {"name": "gfmodel",
                      "preferences": {"gfmodel": {"contextWindow": 1000000}}}}),
            encoding="utf-8")
        result = run_via_host_wrapper(collect_args(ws), env_home=fake_home)
        assert result.returncode == 0, result.stderr
        record = load_single_record(ws)
        assert record["agent"]["resolution"] == "resolved"
        assert record["agent"]["name"] == {"value": "qodercli", "provenance": "measured"}
        llm = record["llm"]
        assert llm["model"] == {"value": "gfmodel", "provenance": "measured"}
        assert llm["context_window"] == {"value": 1000000, "provenance": "measured"}
        # effort unset on this model → explicit marker, NEVER the CLI default
        assert llm["reasoning_effort"] == NOT_EVALUATED
        assert llm["config_source"] == {"value": str(settings), "provenance": "measured"}

    def test_qoder_adapter_reads_per_model_effort_when_set(self, ws, fake_home):
        settings = fake_home / ".qoder" / "settings.json"
        settings.parent.mkdir(parents=True)
        settings.write_text(json.dumps({
            "model": {"name": "qmodel_38max",
                      "preferences": {"qmodel_38max": {
                          "contextWindow": 1000000,
                          "reasoning": {"enabled": True, "effort": "xhigh"}}}}}),
            encoding="utf-8")
        result = run_via_host_wrapper(collect_args(ws), env_home=fake_home)
        assert result.returncode == 0, result.stderr
        llm = load_single_record(ws)["llm"]
        assert llm["reasoning_effort"] == {"value": "xhigh", "provenance": "measured"}

    def test_missing_config_face_degrades_to_marker(self, ws, fake_home):
        # fake HOME has no .qoder/ at all — the adapter finds nothing
        result = run_via_host_wrapper(collect_args(ws), env_home=fake_home)
        assert result.returncode == 0, result.stderr
        record = load_single_record(ws)
        assert record["agent"]["resolution"] == "resolved"
        for field in ("model", "context_window", "reasoning_effort", "config_source"):
            assert record["llm"][field] == NOT_EVALUATED, field


class TestAgentCollection:
    """D8: agent attribution from the parent chain, never guessed."""

    def test_resolved_agent_fields_from_wrapper_host(self, ws, fake_home):
        result = run_via_host_wrapper(collect_args(ws), env_home=fake_home)
        assert result.returncode == 0, result.stderr
        record = load_single_record(ws)
        agent = record["agent"]
        assert agent["resolution"] == "resolved"
        assert agent["name"] == {"value": "qodercli", "provenance": "measured"}
        binary = agent["binary"]
        assert binary == NOT_EVALUATED or (
            isinstance(binary, dict) and binary["provenance"] == "measured")
        argv = agent["argv"]
        assert argv == NOT_EVALUATED or (
            isinstance(argv, dict) and isinstance(argv["value"], list))
        cwd = agent["cwd"]
        assert cwd == NOT_EVALUATED or (
            isinstance(cwd, dict) and isinstance(cwd["value"], str))
        version = agent["version"]
        assert version == NOT_EVALUATED or (
            isinstance(version, dict) and isinstance(version["value"], str)
            and version["value"])

    def test_version_measured_from_wrapper_host_binary(self, ws, fake_home):
        # the impersonated argv[0] name resolves through PATH on hosts that have
        # the real CLI; where absent, the probe degrades to the marker
        result = run_via_host_wrapper(collect_args(ws), env_home=fake_home)
        assert result.returncode == 0, result.stderr
        record = load_single_record(ws)
        agent = record["agent"]
        if agent["version"] != NOT_EVALUATED:
            assert re.match(r"^[0-9][0-9A-Za-z.\-]*$", agent["version"]["value"]), (
                f"version must be a probed value: {agent['version']!r}")
            assert agent["version"]["provenance"] == "measured"


# ===========================================================================
# US2 partition — contracts/exec-quant-cli.md 动作二 list-records + 动作三 score
# (T010; T003's US1 partition above is untouched)
# ===========================================================================

def _collect_two_units(ws: Path, fake_home: Path):
    run_engine(collect_args(ws), env_home=fake_home)
    run_engine(collect_args(ws, unit_id="skill:study-project"), env_home=fake_home)


class TestListRecords:
    """动作二 list-records: filters, machine-readable form, score join."""

    def test_json_full_schema_with_provenance(self, ws, fake_home):
        _collect_two_units(ws, fake_home)
        result = run_engine(["--action", "list-records", "--workspace-root", str(ws),
                             "--format", "json"], env_home=fake_home)
        assert result.returncode == 0, result.stderr
        entries = json.loads(result.stdout)
        assert len(entries) == 2
        for entry in entries:
            for key in ("kind", "schema_version", "unit_id", "unit_type", "run_id",
                        "run_id_resolution", "collected_at", "agent", "config", "llm",
                        "quality", "qualification", "truncated", "scores"):
                assert key in entry, f"json form missing key {key}"
            assert entry["kind"] == KIND
            assert entry["scores"] == []
            assert_field_binary_law(entry)

    def test_text_is_the_default_form(self, ws, fake_home):
        _collect_two_units(ws, fake_home)
        result = run_engine(["--action", "list-records", "--workspace-root", str(ws)],
                            env_home=fake_home)
        assert result.returncode == 0, result.stderr
        assert result.stdout.count("type=") == 2

    def test_filter_by_unit_id(self, ws, fake_home):
        _collect_two_units(ws, fake_home)
        result = run_engine(["--action", "list-records", "--workspace-root", str(ws),
                             "--unit-id", "skill:study-project", "--format", "json"],
                            env_home=fake_home)
        entries = json.loads(result.stdout)
        assert [e["unit_id"] for e in entries] == ["skill:study-project"]

    def test_filter_by_unit_type(self, ws, fake_home):
        _collect_two_units(ws, fake_home)
        result = run_engine(["--action", "list-records", "--workspace-root", str(ws),
                             "--unit-type", "command", "--format", "json"],
                            env_home=fake_home)
        entries = json.loads(result.stdout)
        assert [e["unit_id"] for e in entries] == ["/speckit.plan"]

    def test_filter_by_run_id(self, ws, fake_home):
        _collect_two_units(ws, fake_home)
        records = read_records(ws)
        run_id = records[0]["run_id"]
        result = run_engine(["--action", "list-records", "--workspace-root", str(ws),
                             "--run-id", run_id, "--format", "json"],
                            env_home=fake_home)
        entries = json.loads(result.stdout)
        assert [e["run_id"] for e in entries] == [run_id]

    def test_filter_since_includes_and_excludes(self, ws, fake_home):
        _collect_two_units(ws, fake_home)
        old = run_engine(["--action", "list-records", "--workspace-root", str(ws),
                          "--since", "2000-01-01", "--format", "json"],
                         env_home=fake_home)
        assert old.returncode == 0, old.stderr
        assert len(json.loads(old.stdout)) == 2
        new = run_engine(["--action", "list-records", "--workspace-root", str(ws),
                          "--since", "2999-01-01", "--format", "json"],
                         env_home=fake_home)
        assert new.returncode == 0, new.stderr
        assert json.loads(new.stdout) == []

    def test_zero_hits_exit_0(self, ws, fake_home):
        result = run_engine(["--action", "list-records", "--workspace-root", str(ws),
                             "--unit-id", "skill:no-such-unit", "--format", "json"],
                            env_home=fake_home)
        assert result.returncode == 0, result.stderr
        assert json.loads(result.stdout) == []

    def test_scores_joined_latest_scored_at_wins(self, ws, fake_home):
        _collect_two_units(ws, fake_home)
        record = read_records(ws)[0]
        run_engine(["--action", "score", "--workspace-root", str(ws),
                    "--unit-id", record["unit_id"], "--run-id", record["run_id"],
                    "--score", "3"], env_home=fake_home)
        run_engine(["--action", "score", "--workspace-root", str(ws),
                    "--unit-id", record["unit_id"], "--run-id", record["run_id"],
                    "--score", "5", "--note", "later"], env_home=fake_home)
        result = run_engine(["--action", "list-records", "--workspace-root", str(ws),
                             "--unit-id", record["unit_id"], "--format", "json"],
                            env_home=fake_home)
        entry = json.loads(result.stdout)[0]
        assert len(entry["scores"]) == 2
        assert entry["scores"][-1]["score"] == 5
        assert entry["scores"][-1]["note"] == "later"
        assert all(s["provenance"] == "user-given" for s in entry["scores"])


class TestScoreAction:
    """动作三 score: append-only score entries, precondition, bounds."""

    def test_score_appends_only_to_scores(self, ws, fake_home):
        run_engine(collect_args(ws), env_home=fake_home)
        before = records_snapshot(ws)
        result = run_engine(["--action", "score", "--workspace-root", str(ws),
                             "--unit-id", "/speckit.plan", "--run-id",
                             read_records(ws)[0]["run_id"],
                             "--score", "4", "--note", "手测通过"],
                            env_home=fake_home)
        assert result.returncode == 0, result.stderr
        assert records_snapshot(ws) == before, "record entries must stay untouched"
        assert not scores_path(ws).exists(), "new scores land in scores/, not the legacy file"
        scores = read_scores(ws)
        assert len(scores) == 1
        entry = scores[0]
        assert entry["entry_type"] == "score"
        assert entry["kind"] == KIND
        assert entry["provenance"] == "user-given"
        assert entry["score"] == 4
        assert entry["note"] == "手测通过"
        assert entry["unit_type"] == "command"

    def test_score_requires_existing_record(self, ws, fake_home):
        result = run_engine(["--action", "score", "--workspace-root", str(ws),
                             "--unit-id", "/speckit.plan", "--run-id", "no-such-run",
                             "--score", "4"], env_home=fake_home)
        assert result.returncode == 2
        assert "usage:" in result.stderr

    def test_score_bounds(self, ws, fake_home):
        run_engine(collect_args(ws), env_home=fake_home)
        run_id = read_records(ws)[0]["run_id"]
        for bad in ("0", "6"):
            result = run_engine(["--action", "score", "--workspace-root", str(ws),
                                 "--unit-id", "/speckit.plan", "--run-id", run_id,
                                 "--score", bad], env_home=fake_home)
            assert result.returncode == 2, bad
            assert "usage:" in result.stderr
        result = run_engine(["--action", "score", "--workspace-root", str(ws),
                             "--unit-id", "/speckit.plan", "--run-id", run_id,
                             "--score", "abc"], env_home=fake_home)
        assert result.returncode == 2

    def test_score_missing_params(self, ws, fake_home):
        for args in (["--action", "score", "--workspace-root", str(ws),
                      "--unit-id", "/speckit.plan", "--score", "4"],
                     ["--action", "score", "--workspace-root", str(ws),
                      "--unit-id", "/speckit.plan", "--run-id", "r1"],
                     ["--action", "score", "--workspace-root", str(ws),
                      "--run-id", "r1", "--score", "4"]):
            result = run_engine(args, env_home=fake_home)
            assert result.returncode == 2
            assert "usage:" in result.stderr

    def test_user_given_vs_carried_distinguishable(self, ws, fake_home):
        made = make_determination(ws, "/speckit.plan", "run-001")
        assert made.returncode == 0, made.stderr
        run_engine(collect_args(ws, run_id="run-001"), env_home=fake_home)
        result = run_engine(["--action", "score", "--workspace-root", str(ws),
                             "--unit-id", "/speckit.plan", "--run-id", "run-001",
                             "--score", "4"], env_home=fake_home)
        assert result.returncode == 0, result.stderr
        listed = run_engine(["--action", "list-records", "--workspace-root", str(ws),
                             "--unit-id", "/speckit.plan", "--format", "json"],
                            env_home=fake_home)
        entry = json.loads(listed.stdout)[0]
        # FR-014: the joined user score and the derived satisfaction live in
        # separate fields with separate provenance — one never overwrites the other
        assert entry["scores"][0]["provenance"] == "user-given"
        assert entry["quality"]["satisfaction"] == NOT_EVALUATED
        assert entry["qualification"] == {"value": "qualified", "provenance": "carried"}


# ===========================================================================
# US3 partition — contracts/exec-quant-cli.md 交叉约束 + data-model.md V4–V8
# (T013; migration/regression net authored AFTER its subjects per tasks.md
# A-tasks-6 — no red-first evidence owed. T003/T010 partitions untouched.)
# ===========================================================================

class TestAppendOnly:
    """V4: no action rewrites or reorders existing store entries."""

    def test_actions_never_rewrite_existing_entries(self, ws, fake_home):
        run_engine(collect_args(ws, run_id="v4-a"), env_home=fake_home)
        run_engine(collect_args(ws, unit_id="skill:study-project", run_id="v4-b"),
                   env_home=fake_home)
        records_before = records_snapshot(ws)
        scores_before = scores_snapshot(ws)
        run_engine(["--action", "list-records", "--workspace-root", str(ws)],
                   env_home=fake_home)
        run_engine(["--action", "score", "--workspace-root", str(ws),
                    "--unit-id", "/speckit.plan", "--run-id", "v4-a", "--score", "3"],
                   env_home=fake_home)
        run_engine(collect_args(ws, run_id="v4-a"), env_home=fake_home)  # duplicate
        assert records_snapshot(ws) == records_before, \
            "list/score/duplicate-collect must leave every record entry byte-identical"
        scores_after = scores_snapshot(ws)
        new_scores = set(scores_after) - set(scores_before)
        assert len(new_scores) == 1, "exactly one score entry file is added"
        for name, payload in scores_before.items():
            assert scores_after[name] == payload, "existing score entries stay byte-identical"


class TestSizeCap:
    """V5: 64 KiB cap with per-field truncation; truncated non-empty iff truncated."""

    def test_normal_record_is_not_truncated(self, ws, fake_home):
        run_engine(collect_args(ws), env_home=fake_home)
        assert load_single_record(ws)["truncated"] == []

    def test_oversized_record_is_field_truncated_and_capped(self, ws, fake_home):
        result = run_via_host_wrapper(collect_args(ws), env_home=fake_home,
                                      wrapper_args=("x" * 70000,))
        assert result.returncode == 0, result.stderr
        entry_files = record_files(ws)
        assert len(entry_files) == 1, f"expected one entry file, found {entry_files}"
        line = entry_files[0].read_text(encoding="utf-8").splitlines()[0]
        assert len(line.encode("utf-8")) <= 64 * 1024 + 1, "record must fit the cap"
        record = json.loads(line)
        assert record["truncated"], "truncation must be annotated in the record"
        assert any("agent.argv" in p for p in record["truncated"]), record["truncated"]
        assert all(isinstance(p, str) and p for p in record["truncated"])


class TestCredentialDefense:
    """V6 / SC-004: zero credential-shaped values in any record (value level,
    independent shape list — a second opinion beside the engine's own scan)."""

    INDEPENDENT_SHAPES = tuple(re.compile(p, re.I) for p in (
        r"\b(?:sk|pk)-[A-Za-z0-9]{16,}\b",
        r"\bAKIA[0-9A-Z]{16}\b",
        r"\bBearer\s+\S{12,}",
        r"(?:api[_-]?key|secret|token|authorization|password)\s*[:=]\s*\S{8,}",
        r"[A-Za-z][A-Za-z0-9+.\-]*://[^\s/:@]+:[^\s/@]+@",
    ))

    def test_engine_masks_credential_shaped_config_values(self, ws, fake_home):
        settings = fake_home / ".qoder" / "settings.json"
        settings.parent.mkdir(parents=True)
        settings.write_text(json.dumps({
            "model": {"name": "sk-0123456789abcdef0123",
                      "preferences": {"sk-0123456789abcdef0123": {
                          "contextWindow": 1000000}}}}), encoding="utf-8")
        result = run_via_host_wrapper(collect_args(ws), env_home=fake_home)
        assert result.returncode == 0, result.stderr
        record = load_single_record(ws)
        serialized = json.dumps(record)
        assert "sk-0123456789abcdef0123" not in serialized, \
            "credential-shaped value must be masked before write"
        assert "[masked-credential:" in serialized, "mask must be annotated in place"
        assert record["llm"]["context_window"] == {"value": 1000000,
                                                   "provenance": "measured"}

    def test_zero_credential_shapes_across_the_store(self, ws, fake_home):
        run_engine(collect_args(ws), env_home=fake_home)
        for path in record_files(ws):
            for line in path.read_text(encoding="utf-8").splitlines():
                for pattern in self.INDEPENDENT_SHAPES:
                    assert not pattern.search(line), (
                        f"credential shape in store: {pattern.pattern}")


class TestCarriedConsistency:
    """V7: carried values mirror the determination record exactly; synthesized
    records carry no values at all."""

    def _store_record(self, ws: Path) -> dict:
        entry = next((ws / ".specify" / "memory" / "session").glob("*run-determination*.md"))
        body = re.search(r"```json\n(.*?)\n```", entry.read_text(encoding="utf-8"), re.S)
        return json.loads(body.group(1))

    def test_carried_values_match_the_determination_record(self, ws, fake_home):
        made = make_determination(ws, "/speckit.plan", "run-v7")
        assert made.returncode == 0, made.stderr
        result = run_engine(collect_args(ws, run_id="run-v7"), env_home=fake_home)
        assert result.returncode == 0, result.stderr
        det = self._store_record(ws)
        record = load_single_record(ws)
        axes = det["axes"]
        expected_elapsed = (axes.get("elapsed") or {}).get("measurement") or {}
        expected_elapsed = expected_elapsed.get("ms")
        assert record["quality"]["elapsed_ms"] == (
            {"value": expected_elapsed, "provenance": "carried"}
            if isinstance(expected_elapsed, int) else NOT_EVALUATED)
        assert record["qualification"] == (
            {"value": det["qualification"], "provenance": "carried"}
            if det.get("qualification") else NOT_EVALUATED)
        verdict = (axes.get("satisfaction") or {}).get("verdict")
        assert record["quality"]["satisfaction"] == (
            {"value": verdict, "provenance": "carried"}
            if verdict and verdict != NOT_EVALUATED else NOT_EVALUATED)

    def test_synthesized_record_carries_nothing(self, ws, fake_home):
        run_engine(collect_args(ws), env_home=fake_home)
        record = load_single_record(ws)
        assert record["run_id_resolution"] == "synthesized"
        for field in ("elapsed_ms", "tokens", "errors", "satisfaction"):
            assert record["quality"][field] == NOT_EVALUATED, field
        assert record["qualification"] == NOT_EVALUATED


class TestNonBlocking:
    """V8: failure paths exit 1 with a clean stderr message — no traceback
    propagates into the caller's run."""

    def test_hostile_workspace_root_exits_1_cleanly(self, ws, fake_home):
        blocker = fake_home / "not-a-directory"
        blocker.write_text("occupied", encoding="utf-8")
        result = run_engine(collect_args(blocker), env_home=fake_home)
        assert result.returncode == 1
        assert result.stderr.strip()
        assert "Traceback" not in result.stderr, \
            f"exceptions must not propagate: {result.stderr!r}"

    def test_write_failure_exits_1_cleanly(self, ws, fake_home):
        records_dir(ws).parent.mkdir(parents=True, exist_ok=True)
        records_dir(ws).write_text("occupied", encoding="utf-8")
        result = run_engine(collect_args(ws), env_home=fake_home)
        assert result.returncode == 1
        assert result.stderr.strip()
        assert "Traceback" not in result.stderr

    def test_packaging_quant_coupling_is_read_only(self):
        """068 revision of the former 059 structural exclusion (requirements
        § 对 059 的变更关系 + FR-019; clarify A5 keeps the zero-auto-transmit
        clause intact): the feedback package now READS the quant store for a
        first-class payload, so the old "zero exec-quant references" pin is
        superseded by its revised boundary — the feedback engine stays
        engine-decoupled (no import or spawn of the quant engine) and
        reaches the quant store only through its single read-only locator;
        behavioral read-only assurance rides
        tests/contract/test_feedback_exec_quant_payload.py::
        test_source_stores_read_only_after_package (068 T005)."""
        feedback_src = (REPO_ROOT / "scripts" / "python" / "feedback-utils.py").read_text(
            encoding="utf-8")
        assert "exec-quant.py" not in feedback_src, \
            "feedback engine must not import or spawn the quant engine"
        locator_uses = [line.strip() for line in feedback_src.splitlines()
                        if "exec_quant_dir(" in line]
        assert locator_uses, "payload sweep locator must exist (068 C-1)"
        assert all("def exec_quant_dir" in use or "store = exec_quant_dir("
                   in use for use in locator_uses), \
            f"quant store must be reached only via the read-only locator: {locator_uses}"
