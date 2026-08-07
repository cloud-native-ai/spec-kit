"""US3 integration tests — configure a single named tool (T016).

Covers FR-009, FR-015 and success criteria SC-002 for 024-agent-env-config.

  (a) single-tool apply writes only that tool's file; others untouched
  (b) an unknown tool → exit 3 and lists the four supported tools
  (c) `--all` without AGENT_ANTHROPIC_BASE_URL skips claude, configures the rest
"""
import json
from pathlib import Path

import pytest

from .agent_env_helpers import SECRET_VALUE, run_config_agent, valid_env

SUPPORTED = ["claude", "codex", "qoder", "opencode"]


@pytest.mark.integration
class TestUS3SingleTool:
    def test_single_tool_writes_only_its_file(self, tmp_path: Path):
        result = run_config_agent("config_agent_env_apply opencode", tmp_path, valid_env(tmp_path))
        assert result.returncode == 0, result.combined
        assert (tmp_path / ".config" / "opencode" / "config.json").exists()
        # No other tool's config directory should have been created.
        for other in [".claude", ".codex", ".qoder", ".hermes"]:
            assert not (tmp_path / other).exists(), f"{other} should be untouched"

    def test_single_qoder_only(self, tmp_path: Path):
        result = run_config_agent("config_agent_env_apply qoder", tmp_path, valid_env(tmp_path))
        assert result.returncode == 0, result.combined
        qoder = json.loads((tmp_path / ".qoder" / "config.json").read_text(encoding="utf-8"))
        assert qoder["apiKey"] == SECRET_VALUE
        assert not (tmp_path / ".config").exists()


@pytest.mark.integration
class TestUS3UnknownTool:
    def test_unknown_tool_exit_3_lists_supported(self, tmp_path: Path):
        result = run_config_agent("config_agent_env_apply bogus", tmp_path, valid_env(tmp_path))
        assert result.returncode == 3, result.combined
        for tool in SUPPORTED:
            assert tool in result.combined, f"supported tool {tool} must be listed"
        # Rejected before any write.
        assert [p for p in tmp_path.rglob("*") if p.is_file()] == []

    def test_unknown_tool_rejected_by_validate_too(self, tmp_path: Path):
        result = run_config_agent("config_agent_env_validate bogus", tmp_path, valid_env(tmp_path))
        assert result.returncode == 3, result.combined


@pytest.mark.integration
class TestUS3AllSkipsClaudeWithoutAnthropic:
    def test_all_without_anthropic_skips_claude_configures_rest(self, tmp_path: Path):
        env = valid_env(tmp_path, with_anthropic=False)
        result = run_config_agent("config_agent_env_apply --all", tmp_path, env)
        # claude skipped (not failed) → run still succeeds.
        assert result.returncode == 0, result.combined
        assert "claude" in result.combined
        assert "skip" in result.combined.lower()
        # claude config not written; the other three are.
        assert not (tmp_path / ".claude" / "settings.json").exists()
        assert (tmp_path / ".qoder" / "config.json").exists()
        assert (tmp_path / ".codex" / "config.toml").exists()
        assert (tmp_path / ".config" / "opencode" / "config.json").exists()
