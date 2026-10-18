"""Contract tests for the execution-config resolver engine (Feature 061, US1).

Engine: ``scripts/python/execution-config.py`` — behavior owner of
``.specify/specs/061-subagent-cli-config/contracts/execution-config-cli.md``.

One test class per clause group (C-EC-01..C-EC-15). Every test uses a temp
workspace with an explicit ``--workspace-root``; the framework repository's
``.specify/`` tree is never written.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.contract

_HERE = Path(__file__).resolve()
REPO_ROOT = _HERE.parents[2]
ENGINE = REPO_ROOT / "scripts" / "python" / "execution-config.py"
TEMPLATE = REPO_ROOT / "templates" / "execution-config-defaults.yaml"

STR_013 = ["--model", "DeepSeek-Flash", "--reasoning-effort", "max",
           "--context-window", "1000000"]
QODER_DEFAULT_LITERALS = ("DeepSeek-Flash", "max", "1000000", "qodercli")


@pytest.fixture(autouse=True)
def engine_present():
    """Red-first attribution: no test may pass vacuously while the engine is absent."""
    assert ENGINE.is_file(), "execution-config.py missing — engine not implemented"


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def defaults_text() -> str:
    return TEMPLATE.read_text(encoding="utf-8")


def make_ws(tmp_path: Path, defaults_extra: str = "", agent_yaml: str | None = None,
            agent: str = "sample-agent", defaults_text_override: str | None = None) -> Path:
    ws = tmp_path / "ws"
    configs = ws / ".specify" / "agents" / "execution" / "configs"
    configs.mkdir(parents=True, exist_ok=True)
    body = defaults_text_override if defaults_text_override is not None else defaults_text()
    (configs / "_defaults.yaml").write_text(body + defaults_extra, encoding="utf-8")
    if agent_yaml is not None:
        (configs / f"{agent}.yaml").write_text(agent_yaml, encoding="utf-8")
    return ws


def run_engine(ws: Path, action: str = "resolve", agent: str | None = "sample-agent",
               extra: tuple = (), fmt: str | None = "json",
               extra_env: dict | None = None) -> subprocess.CompletedProcess:
    args = [sys.executable, str(ENGINE), "--action", action,
            "--workspace-root", str(ws)]
    if agent is not None:
        args += ["--agent", agent]
    args += [str(item) for item in extra]
    if fmt:
        args += ["--format", fmt]
    env = dict(os.environ)
    if extra_env:
        env.update({k: str(v) for k, v in extra_env.items()})
    return subprocess.run(args, capture_output=True, text=True, timeout=120, env=env)


def payload(result: subprocess.CompletedProcess) -> dict:
    assert result.returncode == 0, f"engine failed: {result.stderr}\n{result.stdout}"
    return json.loads(result.stdout)


def assert_exit2(result: subprocess.CompletedProcess, *needles: str) -> str:
    assert result.returncode == 2, (
        f"expected exit 2, got {result.returncode}: {result.stderr}")
    combined = result.stderr + result.stdout
    for needle in needles:
        assert needle in combined, f"missing {needle!r} in error surface: {combined!r}"
    return combined


# ===========================================================================
# C-EC-01 — engine identity & actions
# ===========================================================================

class TestEngineIdentity:
    def test_engine_exists_at_locked_path(self):
        assert ENGINE.is_file(), "execution-config.py missing — engine not implemented"

    def test_unknown_action_is_usage_error(self, tmp_path):
        ws = make_ws(tmp_path)
        result = run_engine(ws, action="bogus")
        assert result.returncode == 2
        assert "usage:" in result.stderr

    def test_missing_action_is_usage_error(self, tmp_path):
        ws = make_ws(tmp_path)
        result = subprocess.run(
            [sys.executable, str(ENGINE), "--workspace-root", str(ws)],
            capture_output=True, text=True, timeout=60)
        assert result.returncode == 2
        assert "usage:" in result.stderr

    def test_text_is_the_default_form(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n")
        result = run_engine(ws, fmt=None)
        assert result.returncode == 0, result.stderr
        assert result.stdout.strip()
        with pytest.raises(ValueError):
            json.loads(result.stdout)


# ===========================================================================
# C-EC-02 — paths & defaults layer
# ===========================================================================

class TestPathsAndDefaults:
    def test_missing_defaults_fails_with_path_and_repair(self, tmp_path):
        ws = tmp_path / "ws"
        (ws / ".specify" / "agents" / "execution" / "configs").mkdir(parents=True)
        result = run_engine(ws)
        combined = assert_exit2(result, "_defaults.yaml", "specify init")
        assert "templates/execution-config-defaults.yaml" in combined

    def test_agent_config_absence_is_not_an_error(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n")
        result = run_engine(ws)
        assert result.returncode == 0, result.stderr

    def test_workspace_root_flag_is_honoured(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n")
        result = run_engine(ws)
        data = payload(result)
        assert data["snapshot"].startswith(".specify/agents/execution/logs/")


# ===========================================================================
# C-EC-03 — YAML subset
# ===========================================================================

class TestYamlSubset:
    def test_full_line_comments_and_quotes_are_accepted(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n",
                     agent_yaml='# comment\ncli: qodercli\nmodel: "quoted-model"\n')
        data = payload(run_engine(ws))
        assert data["effective"]["model"] == "quoted-model"

    def test_tab_is_rejected_naming_file(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode:\texternal\n")
        combined = assert_exit2(run_engine(ws), "_defaults.yaml")
        assert "tab" in combined.lower()

    def test_list_item_is_rejected(self, tmp_path):
        ws = make_ws(tmp_path, agent_yaml="- model\n")
        assert_exit2(run_engine(ws), "list")

    def test_inline_list_value_is_rejected(self, tmp_path):
        ws = make_ws(tmp_path, agent_yaml="model: [a, b]\n")
        assert_exit2(run_engine(ws), "list")

    def test_deeper_nesting_is_rejected(self, tmp_path):
        ws = make_ws(tmp_path, agent_yaml="quantification:\n  method:\n    x: y\n")
        assert_exit2(run_engine(ws), "nest")

    def test_orphan_nested_line_is_rejected(self, tmp_path):
        ws = make_ws(tmp_path, agent_yaml="  method: auto\n")
        assert_exit2(run_engine(ws))

    def test_duplicate_key_is_rejected(self, tmp_path):
        ws = make_ws(tmp_path, agent_yaml="model: a\nmodel: b\n")
        assert_exit2(run_engine(ws), "duplicate")

    def test_line_without_colon_is_rejected(self, tmp_path):
        ws = make_ws(tmp_path, agent_yaml="model a\n")
        assert_exit2(run_engine(ws))

    def test_duplicate_quantification_section_is_rejected(self, tmp_path):
        ws = make_ws(tmp_path,
                     agent_yaml="quantification:\n  method: none\nquantification:\n  method: auto\n")
        assert_exit2(run_engine(ws), "quantification")

    def test_inline_hash_stays_part_of_the_value(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n",
                     agent_yaml="model: foo#bar\n")
        data = payload(run_engine(ws))
        assert data["effective"]["model"] == "foo#bar"


# ===========================================================================
# C-EC-04 — schema keys & types
# ===========================================================================

class TestSchemaValidation:
    def test_unknown_key_is_rejected(self, tmp_path):
        ws = make_ws(tmp_path, agent_yaml="bogus: value\n")
        assert_exit2(run_engine(ws), "bogus")

    def test_agent_key_in_defaults_is_rejected(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="agent: sample-agent\n")
        assert_exit2(run_engine(ws), "agent")

    def test_agent_key_mismatch_is_rejected(self, tmp_path):
        ws = make_ws(tmp_path, agent_yaml="agent: other-agent\n")
        assert_exit2(run_engine(ws), "agent")

    def test_quantification_only_allows_method(self, tmp_path):
        ws = make_ws(tmp_path, agent_yaml="quantification:\n  other: x\n")
        assert_exit2(run_engine(ws), "other")

    @pytest.mark.parametrize("value", ["0", "-3", "abc", "True", "1.5"])
    def test_context_window_must_be_positive_int(self, tmp_path, value):
        ws = make_ws(tmp_path, agent_yaml=f"context_window: {value}\n")
        assert_exit2(run_engine(ws), "context_window")

    def test_log_dir_outside_logs_is_rejected(self, tmp_path):
        ws = make_ws(tmp_path, agent_yaml="log_dir: ../../outside\n")
        assert_exit2(run_engine(ws), "log_dir")

    def test_log_dir_inside_logs_is_accepted(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n",
                     agent_yaml="log_dir: .specify/agents/execution/logs/sub\n")
        data = payload(run_engine(ws))
        assert data["effective"]["log_dir"] == ".specify/agents/execution/logs/sub"

    def test_extra_flags_managed_flag_is_rejected(self, tmp_path):
        for flags in ("-m x", "--model=x", "--reasoning-effort high",
                      "--context-window 5"):
            ws = make_ws(tmp_path, agent_yaml=f'extra_flags: "{flags}"\n')
            assert_exit2(run_engine(ws), "extra_flags")

    def test_extra_flags_newline_is_rejected(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n")
        assert_exit2(run_engine(ws, extra=("--extra-flags", "a\n--model b")),
                     "extra_flags")

    def test_extra_flags_custom_tokens_are_accepted(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n",
                     agent_yaml='extra_flags: "--allowed-tools Bash"\n')
        data = payload(run_engine(ws))
        assert data["cli_args"][-2:] == ["--allowed-tools", "Bash"]

    def test_invalid_low_layer_value_is_rejected_even_when_overridden(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="context_window: 0\n",
                     agent_yaml="context_window: 42\n")
        assert_exit2(run_engine(ws), "context_window")


# ===========================================================================
# C-EC-05 — merge & clear sentinels
# ===========================================================================

class TestResolveMerge:
    def test_defaults_only_str_013_and_source_chain(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n")
        data = payload(run_engine(ws))
        assert data["cli_args"] == STR_013
        assert data["requires_external"] is True
        effective = data["effective"]
        assert effective["mode"] == "external"
        assert effective["cli"] == "qodercli"
        assert effective["extra_flags"] is None
        assert effective["log_dir"] is None
        chain = data["source_chain"]
        for field in ("mode", "cli", "model", "reasoning_effort",
                      "context_window", "quantification.method"):
            assert field in chain, field
            assert chain[field]["layer"] == "defaults", field
            assert chain[field]["path"].endswith("_defaults.yaml"), field
        assert "extra_flags" not in chain
        assert "log_dir" not in chain

    def test_config_id_is_stable_across_repeated_runs(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n")
        first = payload(run_engine(ws, extra=("--host-cli", "qodercli")))
        second = payload(run_engine(ws, extra=("--host-cli", "qodercli")))
        assert first["config_id"] == second["config_id"]
        assert len(first["config_id"]) == 16
        int(first["config_id"], 16)

    def test_layer_override_and_inline_chain(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n",
                     agent_yaml="model: override-model\n")
        data = payload(run_engine(ws, extra=("--reasoning-effort", "high")))
        assert data["effective"]["model"] == "override-model"
        assert data["effective"]["reasoning_effort"] == "high"
        chain = data["source_chain"]
        assert chain["model"]["layer"] == "agent-config"
        assert chain["model"]["path"].endswith("sample-agent.yaml")
        assert chain["reasoning_effort"]["layer"] == "inline"
        assert "path" not in chain["reasoning_effort"]

    def test_clear_sentinel_removes_lower_value(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n",
                     agent_yaml='model: ""\n')
        data = payload(run_engine(ws))
        assert data["effective"]["model"] is None
        assert "model" not in data["source_chain"]
        assert "--model" not in data["cli_args"]
        assert data["cli_args"] == ["--reasoning-effort", "max",
                                    "--context-window", "1000000"]

    def test_auto_clears_value_fields(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n",
                     agent_yaml="reasoning_effort: auto\n")
        data = payload(run_engine(ws))
        assert data["effective"]["reasoning_effort"] is None
        assert "--reasoning-effort" not in data["cli_args"]

    def test_effective_always_has_eight_keys(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n")
        effective = payload(run_engine(ws))["effective"]
        assert set(effective.keys()) == {
            "mode", "cli", "model", "reasoning_effort", "context_window",
            "extra_flags", "log_dir", "quantification"}
        assert set(effective["quantification"].keys()) == {"requested", "resolved"}

    def test_cleared_value_changes_config_id(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n")
        with_value = payload(run_engine(ws))["config_id"]
        (ws / ".specify/agents/execution/configs/sample-agent.yaml").write_text(
            "model: auto\n", encoding="utf-8")
        without_value = payload(run_engine(ws))["config_id"]
        assert with_value != without_value

    def test_defaults_layer_skip_on_other_cli(self, tmp_path):
        ws = make_ws(tmp_path, agent_yaml="mode: external\ncli: claude\n"
                                          "quantification:\n  method: none\n")
        data = payload(run_engine(ws))
        assert data["skipped_layers"] == ["defaults"]
        effective = data["effective"]
        assert effective["model"] is None
        assert effective["reasoning_effort"] is None
        assert effective["context_window"] is None
        assert effective["quantification"] == {"requested": "none", "resolved": "none"}
        assert data["cli_args"] == []
        assert "defaults" not in json.dumps(data["source_chain"])

    def test_defaults_participate_when_cli_matches(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n",
                     agent_yaml="cli: qodercli\n")
        data = payload(run_engine(ws))
        assert data["skipped_layers"] == []
        assert data["effective"]["model"] == "DeepSeek-Flash"


# ===========================================================================
# C-EC-06 / C-EC-07 — topology identity & requires_external
# ===========================================================================

class TestIdentityConflict:
    def test_cli_cross_layer_conflict_lists_field(self, tmp_path):
        ws = make_ws(tmp_path, agent_yaml="cli: claude\n")
        assert_exit2(run_engine(ws, extra=("--cli", "qodercli")), "cli")

    def test_mode_cross_layer_conflict_lists_field(self, tmp_path):
        ws = make_ws(tmp_path, agent_yaml="mode: native\n")
        assert_exit2(run_engine(ws, extra=("--mode", "external")), "mode")

    def test_defaults_mode_does_not_trigger_conflict(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: native\n",
                     agent_yaml="mode: external\ncli: qodercli\n")
        data = payload(run_engine(ws))
        assert data["effective"]["mode"] == "external"

    def test_explicit_cli_with_native_is_rejected(self, tmp_path):
        ws = make_ws(tmp_path, agent_yaml="mode: native\ncli: qodercli\n")
        assert_exit2(run_engine(ws), "cli")

    def test_explicit_mode_native_with_override_is_rejected(self, tmp_path):
        ws = make_ws(tmp_path, agent_yaml="mode: virtual\nmodel: m\n")
        combined = assert_exit2(run_engine(ws), "external")
        assert "model" in combined or "mode" in combined

    def test_override_takes_priority_over_defaults_native(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: native\n",
                     agent_yaml="model: override-model\n")
        data = payload(run_engine(ws))
        assert data["effective"]["mode"] == "external"
        assert data["requires_external"] is True
        assert data["source_chain"]["mode"]["layer"] == "derived"
        assert "--model" in data["cli_args"]

    def test_external_without_cli_is_rejected(self, tmp_path):
        body = ("mode: external\nmodel: m\nreasoning_effort: max\n"
                "context_window: 1000\nquantification:\n  method: none\n")
        ws = make_ws(tmp_path, defaults_text_override=body)
        assert_exit2(run_engine(ws), "cli")

    def test_requires_external_false_for_native(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: native\n")
        data = payload(run_engine(ws, extra=("--host-cli", "qodercli")))
        assert data["requires_external"] is False
        assert data["cli_args"] == []

    def test_native_first_when_no_mode_declared(self, tmp_path):
        ws = make_ws(tmp_path)
        data = payload(run_engine(ws, extra=("--host-cli", "qodercli")))
        assert data["effective"]["mode"] == "native"
        assert data["requires_external"] is False
        assert data["cli_args"] == []


# ===========================================================================
# C-EC-08 — CLI capability matrix (single owner in code)
# ===========================================================================

class TestCapabilityMatrix:
    def test_claude_explicit_model_is_rejected_with_supported_set(self, tmp_path):
        ws = make_ws(tmp_path, agent_yaml="mode: external\ncli: claude\nmodel: some-model\n")
        combined = assert_exit2(run_engine(ws), "model", "claude")
        assert "qodercli" in combined, "rejection must name the supported set"

    @pytest.mark.parametrize("field,flag", [
        ("reasoning_effort", "--reasoning-effort"),
        ("context_window", "--context-window"),
    ])
    def test_claude_explicit_other_flags_are_rejected(self, tmp_path, field, flag):
        ws = make_ws(tmp_path, agent_yaml=f"mode: external\ncli: claude\n{field}: 5\n")
        assert_exit2(run_engine(ws), field)

    def test_codex_external_is_rejected(self, tmp_path):
        ws = make_ws(tmp_path, agent_yaml="mode: external\ncli: codex\n")
        assert_exit2(run_engine(ws), "codex")

    def test_opencode_external_is_rejected(self, tmp_path):
        ws = make_ws(tmp_path, agent_yaml="mode: external\ncli: opencode\n")
        assert_exit2(run_engine(ws), "opencode")

    def test_unknown_cli_is_rejected(self, tmp_path):
        ws = make_ws(tmp_path, agent_yaml="mode: external\ncli: mysterycli\n")
        assert_exit2(run_engine(ws), "mysterycli")

    def test_qodercli_full_flags_generate_exact_args(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n")
        data = payload(run_engine(ws))
        assert data["cli_args"] == STR_013

    def test_claude_none_positive_zero_qoder_leak(self, tmp_path):
        """SC-006(a): claude + none positive fixture declares mode: external."""
        ws = make_ws(tmp_path, agent_yaml="mode: external\ncli: claude\n"
                                          "quantification:\n  method: none\n")
        data = payload(run_engine(ws))
        assert data["effective"]["cli"] == "claude"
        assert data["effective"]["quantification"] == {
            "requested": "none", "resolved": "none"}
        telemetry = json.dumps({"effective": data["effective"],
                                "cli_args": data["cli_args"],
                                "source_chain": data["source_chain"]})
        for literal in QODER_DEFAULT_LITERALS:
            assert literal not in telemetry, f"qoder default leaked: {literal}"

    def test_claude_declared_rejection_zero_qoder_leak(self, tmp_path):
        """SC-006(b): claude + declared rejection surface contains no qoder defaults."""
        ws = make_ws(tmp_path, agent_yaml="mode: external\ncli: claude\n"
                                          "quantification:\n  method: declared\n")
        result = run_engine(ws)
        assert result.returncode == 2
        surface = result.stderr + result.stdout
        assert "model" in surface and "reasoning_effort" in surface
        for literal in QODER_DEFAULT_LITERALS:
            assert literal not in surface, f"qoder default leaked: {literal}"

    def test_qodercli_auto_is_resolved_not_matrix_rejected(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n")
        data = payload(run_engine(ws))
        assert data["quantification"] == {"requested": "auto",
                                          "resolved": "qoder-settings"}

    def test_claude_auto_resolves_to_none_with_warning(self, tmp_path):
        ws = make_ws(tmp_path, agent_yaml="mode: external\ncli: claude\n")
        result = run_engine(ws)
        data = payload(result)
        assert data["quantification"] == {"requested": "auto", "resolved": "none"}
        assert data["warnings"], "auto→none must warn"
        assert "warning" in result.stderr.lower()


# ===========================================================================
# C-EC-09 — quantification resolution
# ===========================================================================

class TestQuantification:
    def test_declared_with_all_three_values(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n",
                     agent_yaml="quantification:\n  method: declared\n")
        data = payload(run_engine(ws))
        assert data["quantification"] == {"requested": "declared",
                                          "resolved": "declared"}

    def test_declared_missing_values_exits_2(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n",
                     agent_yaml='model: ""\nquantification:\n  method: declared\n')
        assert_exit2(run_engine(ws), "model")

    def test_auto_declared_from_extra_flags_only_missing_values_exits_2(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n",
                     agent_yaml='model: ""\nreasoning_effort: ""\n'
                                'context_window: ""\nextra_flags: "--verbose"\n')
        assert_exit2(run_engine(ws), "declared")

    def test_explicit_qoder_settings_requires_qoder(self, tmp_path):
        ws = make_ws(tmp_path, agent_yaml="mode: external\ncli: claude\n"
                                          "quantification:\n  method: qoder-settings\n")
        assert_exit2(run_engine(ws), "qoder-settings")

    def test_native_qoder_host_resolves_qoder_settings(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: native\n")
        data = payload(run_engine(ws, extra=("--host-cli", "qodercli")))
        assert data["quantification"] == {"requested": "auto",
                                          "resolved": "qoder-settings"}

    def test_native_non_qoder_host_resolves_none_with_warning(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: native\n")
        data = payload(run_engine(ws, extra=("--host-cli", "claude")))
        assert data["quantification"] == {"requested": "auto", "resolved": "none"}
        assert data["warnings"]

    def test_explicit_none_wins_over_qoder_settings_rule(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n",
                     agent_yaml="quantification:\n  method: none\n")
        data = payload(run_engine(ws))
        assert data["quantification"] == {"requested": "none", "resolved": "none"}
        assert data["warnings"] == []

    def test_method_clear_sentinel_is_invalid_enum(self, tmp_path):
        ws = make_ws(tmp_path, agent_yaml='quantification:\n  method: ""\n')
        assert_exit2(run_engine(ws), "quantification")


# ===========================================================================
# C-EC-10 — cli_args
# ===========================================================================

class TestCliArgs:
    def test_exact_order_and_values(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n",
                     agent_yaml='extra_flags: "--verbose --foo bar"\n')
        data = payload(run_engine(ws))
        assert data["cli_args"] == STR_013 + ["--verbose", "--foo", "bar"]

    def test_native_args_are_empty(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: native\n")
        data = payload(run_engine(ws, extra=("--host-cli", "qodercli")))
        assert data["cli_args"] == []


# ===========================================================================
# C-EC-11 / C-EC-12 — config_id & snapshot
# ===========================================================================

class TestConfigIdAndSnapshot:
    def test_snapshot_written_and_self_consistent(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n")
        data = payload(run_engine(ws))
        snapshot_path = ws / data["snapshot"]
        assert snapshot_path.is_file()
        snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
        assert snapshot["kind"] == "speckit.execution-config-snapshot"
        assert snapshot["schema_version"] == 1
        assert snapshot["config_id"] == data["config_id"]
        assert snapshot["agent"] == "sample-agent"
        assert snapshot["effective"] == data["effective"]
        assert snapshot["cli_args"] == data["cli_args"]
        assert snapshot["log_dir"] == ".specify/agents/execution/logs"
        canonical = json.dumps(snapshot["effective"], sort_keys=True,
                               separators=(",", ":"), ensure_ascii=False)
        import hashlib
        recomputed = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]
        assert recomputed == snapshot["config_id"]

    def test_effective_field_change_changes_id(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n")
        before = payload(run_engine(ws))["config_id"]
        (ws / ".specify/agents/execution/configs/sample-agent.yaml").write_text(
            "model: other\n", encoding="utf-8")
        after = payload(run_engine(ws))["config_id"]
        assert before != after

    def test_snapshot_io_failure_exits_1(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n")
        blocker = ws / ".specify/agents/execution/logs"
        blocker.parent.mkdir(parents=True, exist_ok=True)
        blocker.write_text("occupied", encoding="utf-8")
        result = run_engine(ws)
        assert result.returncode == 1, result.stderr
        assert "Traceback" not in result.stderr


# ===========================================================================
# C-EC-13 — validate
# ===========================================================================

class TestValidate:
    def test_valid_config_no_snapshot(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n",
                     agent_yaml="model: some-model\n")
        data = payload(run_engine(ws, action="validate"))
        assert data["target"] == "sample-agent"
        assert data["valid"] is True
        assert data["errors"] == []
        snapshots = ws / ".specify/agents/execution/logs/config-snapshots"
        assert not snapshots.exists() or not any(snapshots.iterdir())

    def test_invalid_config_reports_fields(self, tmp_path):
        ws = make_ws(tmp_path, agent_yaml="context_window: 0\n")
        result = run_engine(ws, action="validate")
        assert result.returncode == 2
        data = json.loads(result.stdout)
        assert data["valid"] is False
        assert data["errors"]
        assert any("context_window" in error for error in data["errors"])

    def test_missing_defaults_is_an_error(self, tmp_path):
        ws = tmp_path / "ws"
        (ws / ".specify/agents/execution/configs").mkdir(parents=True)
        result = run_engine(ws, action="validate")
        assert result.returncode == 2
        combined = result.stderr + result.stdout
        assert "specify init" in combined


# ===========================================================================
# C-EC-14 — list-configs
# ===========================================================================

class TestListConfigs:
    def test_lists_sorted_excluding_defaults(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n",
                     agent_yaml="cli: qodercli\n")
        configs = ws / ".specify/agents/execution/configs"
        (configs / "zeta-agent.yaml").write_text("cli: qodercli\n", encoding="utf-8")
        data = payload(run_engine(ws, action="list-configs", agent=None))
        files = [entry["file"] for entry in data["configs"]]
        assert files == ["sample-agent.yaml", "zeta-agent.yaml"]
        assert all(entry["valid"] for entry in data["configs"])

    def test_invalid_entry_reported_without_abort(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n",
                     agent_yaml="context_window: 0\n")
        configs = ws / ".specify/agents/execution/configs"
        (configs / "good-agent.yaml").write_text("cli: qodercli\n", encoding="utf-8")
        result = run_engine(ws, action="list-configs", agent=None)
        assert result.returncode == 0, result.stderr
        data = json.loads(result.stdout)
        by_file = {entry["file"]: entry for entry in data["configs"]}
        assert by_file["sample-agent.yaml"]["valid"] is False
        assert by_file["good-agent.yaml"]["valid"] is True

    def test_missing_defaults_is_top_level_error(self, tmp_path):
        ws = tmp_path / "ws"
        (ws / ".specify/agents/execution/configs").mkdir(parents=True)
        result = run_engine(ws, action="list-configs", agent=None)
        assert result.returncode == 2
        assert "specify init" in result.stderr + result.stdout


# ===========================================================================
# C-EC-15 — errors & warnings
# ===========================================================================

class TestErrorsAndWarnings:
    def test_no_code_path_silently_drops_unsupported_combination(self, tmp_path):
        ws = make_ws(tmp_path, agent_yaml="mode: external\ncli: claude\n"
                                          "context_window: 100\n")
        result = run_engine(ws)
        assert result.returncode == 2
        assert "context_window" in result.stderr

    def test_warning_surface_is_json_and_stderr(self, tmp_path):
        ws = make_ws(tmp_path, defaults_extra="mode: external\n",
                     agent_yaml="cli: claude\n")
        result = run_engine(ws)
        data = payload(result)
        assert data["warnings"]
        assert "warning" in result.stderr.lower()

    def test_missing_defaults_does_not_use_builtin_values(self, tmp_path):
        ws = tmp_path / "ws"
        (ws / ".specify/agents/execution/configs").mkdir(parents=True)
        result = run_engine(ws)
        assert result.returncode == 2
        assert "DeepSeek-Flash" not in result.stdout + result.stderr
