"""US2 integration tests — pre-flight validation of environment variables (T013).

Covers FR-003, FR-004 and success criterion SC-003 for 024-agent-env-config.

  (a) missing + malformed vars are all reported (grouped), exit 1, zero files
  (b) `config_agent_env_apply` aborts on invalid input with no partial writes
  (c) an explicit `claude` target requires AGENT_ANTHROPIC_BASE_URL
"""
from pathlib import Path

import pytest

from .agent_env_helpers import SECRET_VALUE, run_config_agent, valid_env


def _files_written(home: Path) -> list[Path]:
    return [p for p in home.rglob("*") if p.is_file()]


@pytest.mark.integration
class TestUS2Validate:
    def test_missing_and_malformed_all_reported_no_files(self, tmp_path: Path):
        # AGENT_API_KEY missing, AGENT_MODEL whitespace-only (missing),
        # AGENT_BASE_URL malformed (no scheme).
        env = {
            "AGENT_MODEL": "   ",
            "AGENT_BASE_URL": "example.test/v1",
            "AGENT_ANTHROPIC_BASE_URL": "https://example.test/apps/anthropic",
        }
        result = run_config_agent("config_agent_env_validate --all", tmp_path, env)
        assert result.returncode == 1, result.combined
        out = result.combined
        assert "AGENT_API_KEY" in out
        assert "AGENT_MODEL" in out
        assert "AGENT_BASE_URL" in out
        # grouped reporting
        assert "Missing" in out
        assert "Malformed" in out
        # nothing written
        assert _files_written(tmp_path) == []

    def test_valid_input_passes_and_writes_nothing(self, tmp_path: Path):
        result = run_config_agent("config_agent_env_validate --all", tmp_path, valid_env(tmp_path))
        assert result.returncode == 0, result.combined
        assert _files_written(tmp_path) == []


@pytest.mark.integration
class TestUS2ApplyAbortsOnInvalid:
    def test_apply_aborts_no_partial_writes(self, tmp_path: Path):
        env = {
            # AGENT_API_KEY missing
            "AGENT_MODEL": "glm-5.2",
            "AGENT_BASE_URL": "https://example.test/v1",
            "AGENT_ANTHROPIC_BASE_URL": "https://example.test/apps/anthropic",
        }
        result = run_config_agent("config_agent_env_apply --all", tmp_path, env)
        assert result.returncode == 1, result.combined
        assert "AGENT_API_KEY" in result.combined
        assert _files_written(tmp_path) == [], "no config files may be written on validation failure"

    def test_secret_absent_when_partially_invalid(self, tmp_path: Path):
        env = valid_env(tmp_path)
        env.pop("AGENT_MODEL")  # force validation failure
        result = run_config_agent("config_agent_env_apply --all", tmp_path, env)
        assert result.returncode == 1, result.combined
        assert SECRET_VALUE not in result.combined


@pytest.mark.integration
class TestUS2ClaudeRequiresAnthropicUrl:
    def test_explicit_claude_requires_anthropic_url(self, tmp_path: Path):
        env = valid_env(tmp_path, with_anthropic=False)
        result = run_config_agent("config_agent_env_validate claude", tmp_path, env)
        assert result.returncode == 1, result.combined
        assert "AGENT_ANTHROPIC_BASE_URL" in result.combined
        assert _files_written(tmp_path) == []

    def test_all_without_anthropic_passes_validation(self, tmp_path: Path):
        # Under --all, a missing AGENT_ANTHROPIC_BASE_URL is not a validation
        # offender: claude will simply be skipped during apply.
        env = valid_env(tmp_path, with_anthropic=False)
        result = run_config_agent("config_agent_env_validate --all", tmp_path, env)
        assert result.returncode == 0, result.combined
