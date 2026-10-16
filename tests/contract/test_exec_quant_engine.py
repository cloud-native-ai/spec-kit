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

ACTIONS_CLOSED_SET = {"collect", "list-records", "score"}
KIND = "speckit.exec-quant"  # [[STR-001]]
NOT_EVALUATED = "not_evaluated"  # [[STR-002]]
PROVENANCE_DOMAIN = {"measured", "carried", "user-given"}

#: Declared measurable fields (data-model §1.1): each is either the literal
#: ``not_evaluated`` or a ``{"value", "provenance"}`` object.
MEASURABLE_PATHS = (
    ("agent", "name"), ("agent", "version"), ("agent", "binary"),
    ("agent", "argv"), ("agent", "cwd"),
    ("llm", "model"), ("llm", "context_window"), ("llm", "reasoning_effort"),
    ("llm", "config_source"), ("llm", "connection_evidence"),
    ("quality", "elapsed_ms"), ("quality", "tokens"), ("quality", "satisfaction"),
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
                         extra_env: dict | None = None):
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
    cmd = ["bash", "-c", f'exec -a {host_name} "{sys.executable}" "{runner}"']
    return subprocess.run(cmd, capture_output=True, text=True, timeout=240, env=env)


def records_path(ws: Path) -> Path:
    return ws / ".specify" / "memory" / "exec-quant" / "records.jsonl"


def scores_path(ws: Path) -> Path:
    return ws / ".specify" / "memory" / "exec-quant" / "scores.jsonl"


def read_jsonl(path: Path) -> list:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


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
    records = read_jsonl(records_path(ws))
    assert len(records) == 1, f"expected 1 record, found {len(records)}"
    return records[0]


# ===========================================================================
# US1 partition — contracts/exec-quant-cli.md 通用参数 + 动作一; V1/V2/V3
# ===========================================================================

class TestActionClosedSet:
    """argparse choices closed set == {collect, list-records, score}."""

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
        assert records_path(ws).is_file()
        assert scores_path(ws).is_file()
        record = load_single_record(ws)
        # V3: kind literal + schema_version
        assert record["kind"] == KIND
        assert record["schema_version"] == 1
        assert record["unit_id"] == "/speckit.plan"
        assert record["unit_type"] == "command"
        # V1: run_id non-empty
        assert isinstance(record["run_id"], str) and record["run_id"]
        # collect text output names run_id and the landing path
        assert record["run_id"] in result.stdout
        assert str(records_path(ws)) in result.stdout

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
        assert len(read_jsonl(records_path(ws))) == 1

    def test_collect_write_failure_exits_1_with_visible_stderr(self, ws, fake_home):
        records_path(ws).parent.mkdir(parents=True, exist_ok=True)
        records_path(ws).mkdir()  # a directory where the append-only file must be
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
