from pathlib import Path

from specify_cli import AGENT_CONFIG

ROOT = Path(__file__).resolve().parents[2]


def test_assistant_matrix_contains_claude():
    assert set(AGENT_CONFIG) >= {"claude", "copilot", "qwen", "opencode", "qoder"}


def test_claude_agent_config_values():
    claude = AGENT_CONFIG["claude"]
    assert claude["name"] == "Claude Code"
    assert claude["folder"] == ".claude/"
    assert claude["install_url"] == "https://www.anthropic.com/claude-code"
    assert claude["requires_cli"] is True


def test_governance_and_templates_include_claude():
    constitution = (ROOT / ".specify" / "memory" / "constitution.md").read_text(
        encoding="utf-8"
    )
    plan_template = (ROOT / "templates" / "plan-template.md").read_text(
        encoding="utf-8"
    )
    instructions_template = (ROOT / "templates" / "instructions-template.md").read_text(
        encoding="utf-8"
    )
    agents_template = (ROOT / "templates" / "commands" / "agents.md").read_text(
        encoding="utf-8"
    )

    assert "Claude Code" in constitution
    assert "Claude Code" in plan_template
    assert "Claude Code" in instructions_template
    assert "Claude Code" in agents_template
