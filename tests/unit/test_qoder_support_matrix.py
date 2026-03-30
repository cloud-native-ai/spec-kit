from pathlib import Path

from specify_cli import AGENT_CONFIG

ROOT = Path(__file__).resolve().parents[2]


def test_assistant_matrix_contains_qoder():
    assert set(AGENT_CONFIG) >= {"copilot", "qwen", "opencode", "qoder"}


def test_governance_and_templates_include_qoder():
    constitution = (ROOT / ".specify" / "memory" / "constitution.md").read_text(encoding="utf-8")
    plan_template = (ROOT / "templates" / "plan-template.md").read_text(encoding="utf-8")
    agents_template = (ROOT / "templates" / "commands" / "agents.md").read_text(encoding="utf-8")

    assert "Qoder" in constitution
    assert "Qoder" in plan_template
    assert "Qoder" in agents_template
