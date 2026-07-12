"""US1 integration tests — one-shot configuration of all six tools (T008).

Covers requirements FR-002, FR-005..FR-008, FR-012..FR-014 and success criteria
SC-001, SC-002, SC-004, SC-005, SC-006 for 024-agent-env-config.

  (a) `apply --all` writes all 6 config files with fields per
      contracts/tool-config-targets.md
  (b) idempotency — two runs produce identical managed fields
  (c) unrelated pre-existing keys are preserved
  (d) the API key value never appears in stdout/stderr
"""
import json
from pathlib import Path

import pytest

from .agent_env_helpers import SECRET_VALUE, run_config_agent, valid_env

MODEL = "glm-5.2"
BASE_URL = "https://example.test/compatible-mode/v1"
ANTHRO_URL = "https://example.test/apps/anthropic"


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.integration
class TestUS1ApplyAllWritesFiles:
    def test_apply_all_writes_all_six_files_with_fields(self, tmp_path: Path):
        result = run_config_agent("config_agent_env_apply --all", tmp_path, valid_env(tmp_path))
        assert result.returncode == 0, result.combined

        # claude → ~/.claude/settings.json (Anthropic mapping)
        claude = _read_json(tmp_path / ".claude" / "settings.json")
        env = claude["env"]
        assert env["ANTHROPIC_BASE_URL"] == ANTHRO_URL
        assert env["ANTHROPIC_AUTH_TOKEN"] == SECRET_VALUE
        assert env["ANTHROPIC_MODEL"] == MODEL
        assert env["ANTHROPIC_SMALL_FAST_MODEL"] == MODEL

        # codex → config.toml + auth.json
        toml_text = (tmp_path / ".codex" / "config.toml").read_text(encoding="utf-8")
        assert f'model = "{MODEL}"' in toml_text
        assert f'base_url = "{BASE_URL}"' in toml_text
        auth = _read_json(tmp_path / ".codex" / "auth.json")
        assert auth["OPENAI_API_KEY"] == SECRET_VALUE

        # qwen → ~/.qwen/.env
        qwen = (tmp_path / ".qwen" / ".env").read_text(encoding="utf-8")
        assert f"OPENAI_API_KEY={SECRET_VALUE}" in qwen
        assert f"OPENAI_BASE_URL={BASE_URL}" in qwen
        assert f"OPENAI_MODEL={MODEL}" in qwen

        # qoder → ~/.qoder/config.json
        qoder = _read_json(tmp_path / ".qoder" / "config.json")
        assert qoder["apiKey"] == SECRET_VALUE
        assert qoder["baseURL"] == BASE_URL
        assert qoder["model"] == MODEL

        # iflow → ~/.iflow/settings.json
        iflow = _read_json(tmp_path / ".iflow" / "settings.json")
        assert iflow["apiKey"] == SECRET_VALUE
        assert iflow["baseUrl"] == BASE_URL
        assert iflow["modelName"] == MODEL

        # opencode → ~/.config/opencode/config.json
        oc = _read_json(tmp_path / ".config" / "opencode" / "config.json")
        agent = oc["provider"]["agent"]
        assert agent["options"]["baseURL"] == BASE_URL
        assert agent["options"]["apiKey"] == SECRET_VALUE
        assert MODEL in agent["models"]

    def test_missing_directories_are_created(self, tmp_path: Path):
        # tmp_path starts empty — no tool dirs exist yet.
        result = run_config_agent("config_agent_env_apply --all", tmp_path, valid_env(tmp_path))
        assert result.returncode == 0, result.combined
        assert (tmp_path / ".config" / "opencode" / "config.json").exists()
        assert (tmp_path / ".qwen" / ".env").exists()


@pytest.mark.integration
class TestUS1Idempotency:
    def test_two_runs_produce_identical_files(self, tmp_path: Path):
        env = valid_env(tmp_path)
        first = run_config_agent("config_agent_env_apply --all", tmp_path, env)
        assert first.returncode == 0, first.combined
        snapshot = {
            p: p.read_bytes()
            for p in sorted(tmp_path.rglob("*"))
            if p.is_file()
        }
        second = run_config_agent("config_agent_env_apply --all", tmp_path, env)
        assert second.returncode == 0, second.combined
        after = {
            p: p.read_bytes()
            for p in sorted(tmp_path.rglob("*"))
            if p.is_file()
        }
        assert after == snapshot, "re-running with identical inputs must be byte-identical"


@pytest.mark.integration
class TestUS1PreservesUnrelatedKeys:
    def test_unrelated_json_keys_survive(self, tmp_path: Path):
        # Seed qoder + claude + opencode + iflow with unrelated content.
        (tmp_path / ".qoder").mkdir(parents=True)
        (tmp_path / ".qoder" / "config.json").write_text(
            json.dumps({"general": {"enableAutoUpdate": True}, "keepMe": 42}),
            encoding="utf-8",
        )
        (tmp_path / ".claude").mkdir(parents=True)
        (tmp_path / ".claude" / "settings.json").write_text(
            json.dumps({"env": {"UNRELATED": "x"}, "theme": "dark"}),
            encoding="utf-8",
        )
        (tmp_path / ".config" / "opencode").mkdir(parents=True)
        (tmp_path / ".config" / "opencode" / "config.json").write_text(
            json.dumps({"provider": {"other": {"name": "other"}}, "topLevel": 1}),
            encoding="utf-8",
        )
        (tmp_path / ".qwen").mkdir(parents=True)
        (tmp_path / ".qwen" / ".env").write_text("EXISTING_LINE=keep\n", encoding="utf-8")

        result = run_config_agent("config_agent_env_apply --all", tmp_path, valid_env(tmp_path))
        assert result.returncode == 0, result.combined

        qoder = _read_json(tmp_path / ".qoder" / "config.json")
        assert qoder["keepMe"] == 42
        assert qoder["general"] == {"enableAutoUpdate": True}
        assert qoder["apiKey"] == SECRET_VALUE

        claude = _read_json(tmp_path / ".claude" / "settings.json")
        assert claude["theme"] == "dark"
        assert claude["env"]["UNRELATED"] == "x"
        assert claude["env"]["ANTHROPIC_AUTH_TOKEN"] == SECRET_VALUE

        oc = _read_json(tmp_path / ".config" / "opencode" / "config.json")
        assert oc["topLevel"] == 1
        assert oc["provider"]["other"] == {"name": "other"}
        assert "agent" in oc["provider"]

        qwen = (tmp_path / ".qwen" / ".env").read_text(encoding="utf-8")
        assert "EXISTING_LINE=keep" in qwen
        assert f"OPENAI_API_KEY={SECRET_VALUE}" in qwen


@pytest.mark.integration
class TestUS1SecretRedaction:
    def test_api_key_never_printed(self, tmp_path: Path):
        result = run_config_agent("config_agent_env_apply --all", tmp_path, valid_env(tmp_path))
        assert result.returncode == 0, result.combined
        assert SECRET_VALUE not in result.stdout
        assert SECRET_VALUE not in result.stderr
