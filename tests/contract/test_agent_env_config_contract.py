"""Contract test for the unified env-var agent configuration (024-agent-env-config).

Asserts that skills/agent-setup/SKILL.md documents:
  - the unified variables (AGENT_API_KEY, AGENT_MODEL, AGENT_BASE_URL,
    AGENT_ANTHROPIC_BASE_URL),
  - the config_agent_env_validate / config_agent_env_apply commands,
  - the six-tool scope (claude, codex, qwen, qoder, iflow, opencode).
Traces to contracts/unified-env-contract.md.
"""
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SKILL_MD = ROOT / "skills" / "agent-setup" / "SKILL.md"

UNIFIED_VARIABLES = [
    "AGENT_API_KEY",
    "AGENT_MODEL",
    "AGENT_BASE_URL",
    "AGENT_ANTHROPIC_BASE_URL",
]

COMMANDS = [
    "config_agent_env_validate",
    "config_agent_env_apply",
]

SIX_TOOLS = ["claude", "codex", "qwen", "qoder", "iflow", "opencode"]


@pytest.fixture(scope="module")
def skill_text() -> str:
    assert SKILL_MD.exists(), "skills/agent-setup/SKILL.md does not exist"
    return SKILL_MD.read_text(encoding="utf-8")


class TestUnifiedEnvContract:
    @pytest.mark.contract
    @pytest.mark.parametrize("var", UNIFIED_VARIABLES)
    def test_documents_unified_variable(self, skill_text: str, var: str):
        assert var in skill_text, f"SKILL.md must document unified variable {var}"

    @pytest.mark.contract
    @pytest.mark.parametrize("cmd", COMMANDS)
    def test_documents_command(self, skill_text: str, cmd: str):
        assert cmd in skill_text, f"SKILL.md must document command {cmd}"

    @pytest.mark.contract
    @pytest.mark.parametrize("tool", SIX_TOOLS)
    def test_documents_tool_scope(self, skill_text: str, tool: str):
        assert tool in skill_text, f"SKILL.md must document in-scope tool {tool}"

    @pytest.mark.contract
    def test_excludes_copilot_and_hermes_from_env_scope(self, skill_text: str):
        # The unified env-var flow explicitly excludes Copilot and Hermes.
        # They must be named as out-of-scope, not silently omitted.
        lowered = skill_text.lower()
        assert "copilot" in lowered and "hermes" in lowered, (
            "SKILL.md must state that Copilot and Hermes Agent are out of scope "
            "for the unified env-var flow"
        )
