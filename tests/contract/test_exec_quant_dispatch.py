"""Contract tests for exec-quant v2 + collect-dispatch (Feature 061, US2).

Engine: ``scripts/python/exec-quant.py`` — behavior owner of
``.specify/specs/061-subagent-cli-config/contracts/exec-quant-v2.md``
(C-EQ-02..C-EQ-10).

Every test uses fixture dispatch artifacts (snapshot + ``<label>.jsonl`` +
``<label>.status``) under a temp workspace; snapshots are authored here with the
canonical JSON form, never by the engine. The framework repository's store is
never written.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

_HERE = Path(__file__).resolve()
REPO_ROOT = _HERE.parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "exec-quant.py"
NOT_EVALUATED = "not_evaluated"
CONFIG_FIELDS = {
    "config_id", "source_chain", "method_requested", "method_resolved", "mode",
    "cli", "model", "reasoning_effort", "context_window", "extra_flags", "snapshot"}
QODER_DEFAULT_LITERALS = ("DeepSeek-Flash", "max", "1000000", "qodercli")


@pytest.fixture(autouse=True)
def engine_v2_present():
    """Red-first attribution: no test may pass vacuously before the v2 extension."""
    source = ENGINE.read_text(encoding="utf-8")
    assert "collect-dispatch" in source, "collect-dispatch missing — engine not extended"
    assert "SCHEMA_VERSION = 2" in source, "exec-quant is not v2 yet"


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def make_ws(tmp_path: Path) -> Path:
    ws = tmp_path / "ws"
    (ws / ".specify" / "agents" / "execution" / "logs").mkdir(parents=True)
    (ws / ".specify" / "memory").mkdir(parents=True)
    return ws


def canonical_json(node) -> str:
    return json.dumps(node, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def config_id_of(effective) -> str:
    return hashlib.sha256(canonical_json(effective).encode("utf-8")).hexdigest()[:16]


def qoder_effective(resolved="qoder-settings") -> dict:
    return {
        "mode": "external", "cli": "qodercli", "model": "DeepSeek-Flash",
        "reasoning_effort": "max", "context_window": 1000000,
        "extra_flags": None, "log_dir": None,
        "quantification": {"requested": "auto", "resolved": resolved},
    }


def claude_none_effective() -> dict:
    return {
        "mode": "external", "cli": "claude", "model": None,
        "reasoning_effort": None, "context_window": None,
        "extra_flags": None, "log_dir": None,
        "quantification": {"requested": "none", "resolved": "none"},
    }


def source_chain_for(effective: dict) -> dict:
    chain = {}
    for field in ("mode", "cli", "model", "reasoning_effort", "context_window"):
        if effective.get(field) is not None:
            chain[field] = {"layer": "defaults", "path": ".specify/agents/execution/configs/_defaults.yaml"}
    chain["quantification.method"] = {
        "layer": "defaults", "path": ".specify/agents/execution/configs/_defaults.yaml"}
    return chain


def write_snapshot(ws: Path, effective: dict, agent: str = "sample-agent",
                   resolved_at: str = "2026-10-18T00:00:00Z",
                   config_id: str | None = None) -> tuple[Path, str]:
    cid = config_id_of(effective)
    snapshot = {
        "kind": "speckit.execution-config-snapshot",
        "schema_version": 1,
        "config_id": cid,
        "resolved_at": resolved_at,
        "agent": agent,
        "effective": effective,
        "source_chain": source_chain_for(effective),
        "skipped_layers": [],
        "requires_external": effective.get("mode") == "external",
        "cli_args": [],
        "log_dir": ".specify/agents/execution/logs",
    }
    directory = ws / ".specify" / "agents" / "execution" / "logs" / "config-snapshots"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{cid}.json"
    path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    return path, cid


def write_status(ws: Path, label: str, line: str) -> Path:
    path = ws / ".specify" / "agents" / "execution" / "logs" / f"{label}.status"
    path.write_text(line + "\n", encoding="utf-8")
    return path


def write_jsonl(ws: Path, label: str, events: list) -> Path:
    path = ws / ".specify" / "agents" / "execution" / "logs" / f"{label}.jsonl"
    path.write_text("\n".join(json.dumps(event) for event in events) + "\n",
                    encoding="utf-8")
    return path


def run_engine(args, fake_home: Path | None = None) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    if fake_home is not None:
        env["HOME"] = str(fake_home)
    argv = [sys.executable, str(ENGINE)] + [str(item) for item in args]
    return subprocess.run(argv, capture_output=True, text=True, timeout=120, env=env)


def dispatch_args(ws: Path, snapshot: Path, cid: str, label: str = "demo-label",
                  unit_id: str = "agent:sample-agent", omit=()):
    args = ["--action", "collect-dispatch", "--workspace-root", str(ws),
            "--unit-id", unit_id]
    for flag, value in (("--run-id", label), ("--snapshot", str(snapshot)),
                        ("--config-id", cid)):
        if flag not in omit:
            args += [flag, value]
    return args


def store_dir(ws: Path) -> Path:
    return ws / ".specify" / "memory" / "exec-quant"


def records_dir(ws: Path) -> Path:
    return store_dir(ws) / "records"


def scores_dir(ws: Path) -> Path:
    return store_dir(ws) / "scores"


def records_path(ws: Path) -> Path:
    """Legacy single-file store, readable but never written since the split."""
    return store_dir(ws) / "records.jsonl"


def record_files(ws: Path) -> list:
    return sorted(records_dir(ws).glob("*.json")) if records_dir(ws).is_dir() else []


def read_jsonl(path: Path) -> list:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


def read_records(ws: Path) -> list:
    entries = read_jsonl(records_path(ws))
    if records_dir(ws).is_dir():
        entries += [json.loads(path.read_text(encoding="utf-8"))
                    for path in sorted(records_dir(ws).glob("*.json"))]
    return entries


def read_scores(ws: Path) -> list:
    entries = read_jsonl(store_dir(ws) / "scores.jsonl")
    if scores_dir(ws).is_dir():
        entries += [json.loads(path.read_text(encoding="utf-8"))
                    for path in sorted(scores_dir(ws).glob("*.json"))]
    return entries


def records_snapshot(ws: Path) -> dict:
    root = store_dir(ws)
    if not root.is_dir():
        return {}
    return {p.relative_to(root).as_posix(): p.read_bytes()
            for p in root.rglob("*")
            if p.is_file() and (p.relative_to(root).as_posix() == "records.jsonl"
                                or p.relative_to(root).as_posix().startswith("records/"))}


def assert_no_blanks(node, path="$"):
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


# ===========================================================================
# C-EQ-01 / C-EQ-02 — schema v2, action set, collect under v2
# ===========================================================================

class TestSchemaV2:
    def test_action_set_includes_collect_dispatch(self):
        result = run_engine(["--action", "bogus"])
        assert result.returncode == 2
        assert "collect-dispatch" in result.stderr

    def test_collect_writes_schema_v2_and_config_group(self, tmp_path):
        ws = make_ws(tmp_path)
        result = run_engine(["--action", "collect", "--workspace-root", str(ws),
                             "--unit-id", "/speckit.plan", "--run-id", "r1"])
        assert result.returncode == 0, result.stderr
        record = read_records(ws)[0]
        assert record["schema_version"] == 2
        assert set(record["config"].keys()) == CONFIG_FIELDS
        assert all(value == NOT_EVALUATED for value in record["config"].values())
        assert record["quality"]["exit_code"] == NOT_EVALUATED
        assert_no_blanks(record)

    def test_collect_rejects_agent_unit(self, tmp_path):
        ws = make_ws(tmp_path)
        result = run_engine(["--action", "collect", "--workspace-root", str(ws),
                             "--unit-id", "agent:sample-agent", "--run-id", "r1"])
        assert result.returncode == 2
        assert "usage:" in result.stderr

    def test_collect_dispatch_rejects_non_agent_unit(self, tmp_path):
        ws = make_ws(tmp_path)
        snapshot, cid = write_snapshot(ws, qoder_effective())
        result = run_engine(dispatch_args(ws, snapshot, cid, unit_id="/speckit.plan"))
        assert result.returncode == 2
        assert not read_records(ws)


# ===========================================================================
# C-EQ-03 — collect-dispatch input contract
# ===========================================================================

class TestCollectDispatchInput:
    def test_writes_one_agent_record(self, tmp_path):
        ws = make_ws(tmp_path)
        snapshot, cid = write_snapshot(ws, qoder_effective())
        write_status(ws, "demo-label", "demo-label exit=0")
        result = run_engine(dispatch_args(ws, snapshot, cid))
        assert result.returncode == 0, result.stderr
        records = read_records(ws)
        assert len(records) == 1
        record = records[0]
        assert record["schema_version"] == 2
        assert record["unit_id"] == "agent:sample-agent"
        assert record["unit_type"] == "agent"
        assert record["run_id"] == "demo-label"
        assert record["run_id_resolution"] == "explicit"
        assert set(record["config"].keys()) == CONFIG_FIELDS
        assert record["config"]["config_id"] == cid
        assert record["config"]["method_requested"] == "auto"
        assert record["config"]["method_resolved"] == "qoder-settings"
        assert record["config"]["snapshot"].endswith(f"{cid}.json")
        assert_no_blanks(record)

    @pytest.mark.parametrize("missing", ["--run-id", "--snapshot", "--config-id"])
    def test_missing_required_argument_exits_2(self, tmp_path, missing):
        ws = make_ws(tmp_path)
        snapshot, cid = write_snapshot(ws, qoder_effective())
        result = run_engine(dispatch_args(ws, snapshot, cid, omit=(missing,)))
        assert result.returncode == 2
        assert "usage:" in result.stderr
        assert not read_records(ws)

    def test_missing_snapshot_exits_1_no_record(self, tmp_path):
        ws = make_ws(tmp_path)
        snapshot, cid = write_snapshot(ws, qoder_effective())
        snapshot.unlink()
        result = run_engine(dispatch_args(ws, snapshot, cid))
        assert result.returncode == 1
        assert not read_records(ws)

    def test_wrong_kind_exits_1(self, tmp_path):
        ws = make_ws(tmp_path)
        snapshot, cid = write_snapshot(ws, qoder_effective())
        document = json.loads(snapshot.read_text(encoding="utf-8"))
        document["kind"] = "not-a-snapshot"
        snapshot.write_text(json.dumps(document), encoding="utf-8")
        result = run_engine(dispatch_args(ws, snapshot, cid))
        assert result.returncode == 1
        assert not read_records(ws)

    def test_wrong_schema_version_exits_1(self, tmp_path):
        ws = make_ws(tmp_path)
        snapshot, cid = write_snapshot(ws, qoder_effective())
        document = json.loads(snapshot.read_text(encoding="utf-8"))
        document["schema_version"] = 2
        snapshot.write_text(json.dumps(document), encoding="utf-8")
        result = run_engine(dispatch_args(ws, snapshot, cid))
        assert result.returncode == 1
        assert not read_records(ws)

    def test_tampered_effective_exits_1(self, tmp_path):
        ws = make_ws(tmp_path)
        snapshot, cid = write_snapshot(ws, qoder_effective())
        document = json.loads(snapshot.read_text(encoding="utf-8"))
        document["effective"]["model"] = "tampered"
        snapshot.write_text(json.dumps(document), encoding="utf-8")
        result = run_engine(dispatch_args(ws, snapshot, cid))
        assert result.returncode == 1
        assert not read_records(ws)

    def test_config_id_mismatch_exits_1(self, tmp_path):
        ws = make_ws(tmp_path)
        snapshot, cid = write_snapshot(ws, qoder_effective())
        args = dispatch_args(ws, snapshot, cid)
        args[-1] = "0000000000000000"
        result = run_engine(args)
        assert result.returncode == 1
        assert not read_records(ws)

    def test_non_agent_unit_exits_2(self, tmp_path):
        ws = make_ws(tmp_path)
        snapshot, cid = write_snapshot(ws, qoder_effective())
        result = run_engine(dispatch_args(ws, snapshot, cid,
                                          unit_id="agent:bad/slug"))
        assert result.returncode == 2


class TestIdempotency:
    def test_duplicate_call_leaves_one_row_and_bytes_identical(self, tmp_path):
        ws = make_ws(tmp_path)
        snapshot, cid = write_snapshot(ws, qoder_effective())
        write_status(ws, "demo-label", "demo-label exit=0")
        first = run_engine(dispatch_args(ws, snapshot, cid))
        assert first.returncode == 0, first.stderr
        before = records_snapshot(ws)
        second = run_engine(dispatch_args(ws, snapshot, cid))
        assert second.returncode == 0, second.stderr
        assert "duplicate" in (second.stdout + second.stderr).lower()
        assert records_snapshot(ws) == before
        assert len(read_records(ws)) == 1


# ===========================================================================
# C-EQ-04 / C-EQ-05 — config group + llm by method
# ===========================================================================

class TestConfigGroup:
    def test_null_effective_values_become_explicit_markers(self, tmp_path):
        ws = make_ws(tmp_path)
        snapshot, cid = write_snapshot(ws, claude_none_effective())
        result = run_engine(dispatch_args(ws, snapshot, cid))
        assert result.returncode == 0, result.stderr
        config = read_records(ws)[0]["config"]
        for field in ("model", "reasoning_effort", "context_window", "extra_flags"):
            assert config[field] == NOT_EVALUATED, field
        assert config["mode"] == "external"
        assert config["cli"] == "claude"
        assert config["method_requested"] == "none"
        assert config["method_resolved"] == "none"

    def test_claude_none_config_group_has_zero_qoder_literals(self, tmp_path):
        """SC-006(a): the record's config group carries no qoder defaults."""
        ws = make_ws(tmp_path)
        snapshot, cid = write_snapshot(ws, claude_none_effective())
        result = run_engine(dispatch_args(ws, snapshot, cid))
        assert result.returncode == 0, result.stderr
        record = read_records(ws)[0]
        config_surface = json.dumps(record["config"])
        for literal in QODER_DEFAULT_LITERALS:
            assert literal not in config_surface, f"qoder default leaked: {literal}"
        # the agent group is host evidence and is out of the leak-count scope
        assert "agent" in record


class TestLlmByMethod:
    def test_declared_echoes_config_values_as_configured(self, tmp_path):
        ws = make_ws(tmp_path)
        effective = qoder_effective(resolved="declared")
        effective["quantification"]["requested"] = "declared"
        snapshot, cid = write_snapshot(ws, effective)
        result = run_engine(dispatch_args(ws, snapshot, cid))
        assert result.returncode == 0, result.stderr
        llm = read_records(ws)[0]["llm"]
        assert llm["model"] == {"value": "DeepSeek-Flash", "provenance": "configured"}
        assert llm["reasoning_effort"] == {"value": "max", "provenance": "configured"}
        assert llm["context_window"] == {"value": 1000000, "provenance": "configured"}
        assert llm["config_source"] == {
            "value": f"execution-config:{cid}", "provenance": "configured"}
        assert llm["endpoint_candidates"] == NOT_EVALUATED
        assert llm["connection_evidence"] == NOT_EVALUATED

    def test_qoder_settings_reads_fake_home(self, tmp_path):
        ws = make_ws(tmp_path)
        fake_home = tmp_path / "home"
        settings = fake_home / ".qoder" / "settings.json"
        settings.parent.mkdir(parents=True)
        settings.write_text(json.dumps({
            "model": {"name": "gfmodel",
                      "preferences": {"gfmodel": {
                          "contextWindow": 1000000,
                          "reasoning": {"effort": "xhigh"}}}}}), encoding="utf-8")
        snapshot, cid = write_snapshot(ws, qoder_effective())
        result = run_engine(dispatch_args(ws, snapshot, cid), fake_home=fake_home)
        assert result.returncode == 0, result.stderr
        llm = read_records(ws)[0]["llm"]
        assert llm["model"] == {"value": "gfmodel", "provenance": "measured"}
        assert llm["context_window"] == {"value": 1000000, "provenance": "measured"}
        assert llm["reasoning_effort"] == {"value": "xhigh", "provenance": "measured"}
        assert llm["config_source"] == {"value": str(settings), "provenance": "measured"}

    def test_qoder_settings_missing_file_degrades(self, tmp_path):
        ws = make_ws(tmp_path)
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        snapshot, cid = write_snapshot(ws, qoder_effective())
        result = run_engine(dispatch_args(ws, snapshot, cid), fake_home=fake_home)
        assert result.returncode == 0, result.stderr
        llm = read_records(ws)[0]["llm"]
        for field in ("model", "reasoning_effort", "context_window", "config_source"):
            assert llm[field] == NOT_EVALUATED, field

    def test_none_marks_all_six_llm_fields(self, tmp_path):
        ws = make_ws(tmp_path)
        snapshot, cid = write_snapshot(ws, claude_none_effective())
        result = run_engine(dispatch_args(ws, snapshot, cid))
        assert result.returncode == 0, result.stderr
        llm = read_records(ws)[0]["llm"]
        for field in ("model", "reasoning_effort", "context_window",
                      "config_source", "endpoint_candidates",
                      "connection_evidence"):
            assert llm[field] == NOT_EVALUATED, field


# ===========================================================================
# C-EQ-06 — quality group
# ===========================================================================

class TestQuality:
    def test_exit_zero_and_measured_leaves(self, tmp_path):
        ws = make_ws(tmp_path)
        snapshot, cid = write_snapshot(ws, qoder_effective())
        write_status(ws, "demo-label", "demo-label exit=0")
        write_jsonl(ws, "demo-label", [
            {"type": "result", "duration_ms": 1234,
             "usage": {"input_tokens": 10, "output_tokens": 5}}])
        result = run_engine(dispatch_args(ws, snapshot, cid))
        assert result.returncode == 0, result.stderr
        quality = read_records(ws)[0]["quality"]
        assert quality["exit_code"] == {"value": 0, "provenance": "measured"}
        assert quality["errors"] == []
        assert quality["elapsed_ms"] == {"value": 1234, "provenance": "measured"}
        assert quality["tokens"] == {"value": 15, "provenance": "measured"}
        assert quality["satisfaction"] == NOT_EVALUATED

    def test_nonzero_exit_records_one_error(self, tmp_path):
        ws = make_ws(tmp_path)
        snapshot, cid = write_snapshot(ws, qoder_effective())
        write_status(ws, "demo-label", "demo-label exit=7")
        result = run_engine(dispatch_args(ws, snapshot, cid))
        assert result.returncode == 0, result.stderr
        quality = read_records(ws)[0]["quality"]
        assert quality["exit_code"] == {"value": 7, "provenance": "measured"}
        assert quality["errors"] == [{"source": "dispatch.exit_code", "count": 1}]

    def test_missing_status_marks_fields_not_evaluated(self, tmp_path):
        ws = make_ws(tmp_path)
        snapshot, cid = write_snapshot(ws, qoder_effective())
        result = run_engine(dispatch_args(ws, snapshot, cid))
        assert result.returncode == 0, result.stderr
        quality = read_records(ws)[0]["quality"]
        assert quality["exit_code"] == NOT_EVALUATED
        assert quality["errors"] == NOT_EVALUATED
        assert quality["elapsed_ms"] == NOT_EVALUATED

    def test_unparseable_status_degrades(self, tmp_path):
        ws = make_ws(tmp_path)
        snapshot, cid = write_snapshot(ws, qoder_effective())
        write_status(ws, "demo-label", "no exit code here")
        result = run_engine(dispatch_args(ws, snapshot, cid))
        assert result.returncode == 0, result.stderr
        quality = read_records(ws)[0]["quality"]
        assert quality["exit_code"] == NOT_EVALUATED
        assert quality["errors"] == NOT_EVALUATED

    def test_last_duration_wins(self, tmp_path):
        ws = make_ws(tmp_path)
        snapshot, cid = write_snapshot(ws, qoder_effective())
        write_status(ws, "demo-label", "demo-label exit=0")
        write_jsonl(ws, "demo-label", [
            {"duration_ms": 1000}, {"nested": {"duration_ms": 2000}}])
        result = run_engine(dispatch_args(ws, snapshot, cid))
        assert result.returncode == 0, result.stderr
        assert read_records(ws)[0]["quality"]["elapsed_ms"] == {
            "value": 2000, "provenance": "measured"}

    def test_elapsed_fallback_uses_status_mtime(self, tmp_path):
        from datetime import datetime, timezone
        ws = make_ws(tmp_path)
        snapshot, cid = write_snapshot(ws, qoder_effective(),
                                       resolved_at="2026-10-18T00:00:00Z")
        status = write_status(ws, "demo-label", "demo-label exit=0")
        stamp = datetime(2026, 10, 18, tzinfo=timezone.utc).timestamp() + 5
        os.utime(status, (stamp, stamp))
        result = run_engine(dispatch_args(ws, snapshot, cid))
        assert result.returncode == 0, result.stderr
        elapsed = read_records(ws)[0]["quality"]["elapsed_ms"]
        assert elapsed == {"value": 5000, "provenance": "measured"}

    def test_negative_elapsed_fallback_is_not_evaluated(self, tmp_path):
        ws = make_ws(tmp_path)
        snapshot, cid = write_snapshot(ws, qoder_effective(),
                                       resolved_at="2026-10-18T00:00:00Z")
        status = write_status(ws, "demo-label", "demo-label exit=0")
        os.utime(status, (1.0, 1.0))
        result = run_engine(dispatch_args(ws, snapshot, cid))
        assert result.returncode == 0, result.stderr
        assert read_records(ws)[0]["quality"]["elapsed_ms"] == NOT_EVALUATED

    def test_tokens_require_both_integers_in_one_object(self, tmp_path):
        ws = make_ws(tmp_path)
        snapshot, cid = write_snapshot(ws, qoder_effective())
        write_status(ws, "demo-label", "demo-label exit=0")
        write_jsonl(ws, "demo-label", [
            {"usage": {"input_tokens": 10}},
            {"usage": {"input_tokens": 10, "output_tokens": "5"}},
            {"usage": {"input_tokens": 7, "output_tokens": 3}}])
        result = run_engine(dispatch_args(ws, snapshot, cid))
        assert result.returncode == 0, result.stderr
        assert read_records(ws)[0]["quality"]["tokens"] == {
            "value": 10, "provenance": "measured"}

    def test_qualification_is_not_evaluated(self, tmp_path):
        ws = make_ws(tmp_path)
        snapshot, cid = write_snapshot(ws, qoder_effective())
        result = run_engine(dispatch_args(ws, snapshot, cid))
        assert result.returncode == 0, result.stderr
        assert read_records(ws)[0]["qualification"] == NOT_EVALUATED


# ===========================================================================
# C-EQ-07 / C-EQ-08 — list-records, score, v1 normalization
# ===========================================================================

class TestListAndScore:
    def test_filter_by_unit_type_and_config_id(self, tmp_path):
        ws = make_ws(tmp_path)
        snapshot, cid = write_snapshot(ws, qoder_effective())
        write_status(ws, "demo-label", "demo-label exit=0")
        run_engine(dispatch_args(ws, snapshot, cid))
        result = run_engine(["--action", "list-records", "--workspace-root", str(ws),
                             "--unit-type", "agent", "--config-id", cid,
                             "--format", "json"])
        assert result.returncode == 0, result.stderr
        entries = json.loads(result.stdout)
        assert len(entries) == 1
        assert entries[0]["unit_id"] == "agent:sample-agent"

    def test_config_id_filter_excludes_other_configs(self, tmp_path):
        ws = make_ws(tmp_path)
        snapshot, cid = write_snapshot(ws, qoder_effective())
        write_status(ws, "demo-label", "demo-label exit=0")
        run_engine(dispatch_args(ws, snapshot, cid))
        result = run_engine(["--action", "list-records", "--workspace-root", str(ws),
                             "--config-id", "ffffffffffffffff", "--format", "json"])
        assert result.returncode == 0, result.stderr
        assert json.loads(result.stdout) == []

    def test_v1_record_read_only_normalization(self, tmp_path):
        ws = make_ws(tmp_path)
        store = ws / ".specify" / "memory" / "exec-quant"
        store.mkdir(parents=True, exist_ok=True)
        v1 = {
            "kind": "speckit.exec-quant", "schema_version": 1,
            "unit_id": "/speckit.plan", "unit_type": "command",
            "run_id": "old-run", "run_id_resolution": "explicit",
            "collected_at": "2026-10-18T00:00:00Z",
            "agent": {"resolution": "unresolved"},
            "llm": {}, "quality": {"errors": NOT_EVALUATED},
            "qualification": NOT_EVALUATED, "truncated": [],
        }
        path = store / "records.jsonl"
        path.write_text(json.dumps(v1) + "\n", encoding="utf-8")
        before = path.read_bytes()
        result = run_engine(["--action", "list-records", "--workspace-root", str(ws),
                             "--format", "json"])
        assert result.returncode == 0, result.stderr
        entries = json.loads(result.stdout)
        assert entries[0]["schema_version"] == 1
        assert set(entries[0]["config"].keys()) == CONFIG_FIELDS
        assert entries[0]["quality"]["exit_code"] == NOT_EVALUATED
        assert path.read_bytes() == before, "v1 store must not be rewritten"

    def test_score_agent_record(self, tmp_path):
        ws = make_ws(tmp_path)
        snapshot, cid = write_snapshot(ws, qoder_effective())
        write_status(ws, "demo-label", "demo-label exit=0")
        run_engine(dispatch_args(ws, snapshot, cid))
        result = run_engine(["--action", "score", "--workspace-root", str(ws),
                             "--unit-id", "agent:sample-agent", "--run-id",
                             "demo-label", "--score", "5", "--note", "ok"])
        assert result.returncode == 0, result.stderr
        scores = read_scores(ws)
        assert len(scores) == 1
        assert scores[0]["provenance"] == "user-given"
        assert scores[0]["unit_type"] == "agent"


# ===========================================================================
# C-EQ-09 / C-EQ-10 — errors & defenses
# ===========================================================================

class TestDefenses:
    def test_non_blocking_failure_has_no_traceback(self, tmp_path):
        ws = make_ws(tmp_path)
        snapshot, cid = write_snapshot(ws, qoder_effective())
        snapshot.write_text("{not json", encoding="utf-8")
        result = run_engine(dispatch_args(ws, snapshot, cid))
        assert result.returncode == 1
        assert result.stderr.strip()
        assert "Traceback" not in result.stderr

    def test_append_only_after_second_collect(self, tmp_path):
        ws = make_ws(tmp_path)
        snapshot, cid = write_snapshot(ws, qoder_effective())
        write_status(ws, "demo-label", "demo-label exit=0")
        run_engine(dispatch_args(ws, snapshot, cid))
        before = records_snapshot(ws)
        other = qoder_effective()
        other["mode"] = "external"
        other["model"] = "other-model"
        snapshot2, cid2 = write_snapshot(ws, other)
        run_engine(dispatch_args(ws, snapshot2, cid2, label="demo-label-2"))
        after = records_snapshot(ws)
        for name, payload in before.items():
            assert after.get(name) == payload, "existing record entries stay byte-identical"
        assert len(after) == len(before) + 1, "the second dispatch adds exactly one entry"

    def test_credential_values_are_masked(self, tmp_path):
        ws = make_ws(tmp_path)
        effective = qoder_effective()
        effective["model"] = "sk-0123456789abcdef0123"
        snapshot, cid = write_snapshot(ws, effective)
        result = run_engine(dispatch_args(ws, snapshot, cid))
        assert result.returncode == 0, result.stderr
        serialized = "\n".join(path.read_text(encoding="utf-8")
                               for path in record_files(ws))
        assert "sk-0123456789abcdef0123" not in serialized
        assert "[masked-credential:" in serialized

    def test_oversized_record_is_capped_identity_survives(self, tmp_path):
        ws = make_ws(tmp_path)
        effective = qoder_effective()
        effective["extra_flags"] = "x" * 70000
        snapshot, cid = write_snapshot(ws, effective)
        result = run_engine(dispatch_args(ws, snapshot, cid))
        assert result.returncode == 0, result.stderr
        entry_files = record_files(ws)
        assert len(entry_files) == 1, f"expected one entry file, found {entry_files}"
        line = entry_files[0].read_text(encoding="utf-8").splitlines()[0]
        assert len(line.encode("utf-8")) <= 64 * 1024 + 1
        record = json.loads(line)
        assert record["truncated"]
        assert record["config"]["config_id"] == cid
