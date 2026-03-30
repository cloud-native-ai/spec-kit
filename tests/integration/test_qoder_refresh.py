from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_refresh_scripts_cover_qoder_project_rules():
    root_script = (ROOT / "scripts" / "bash" / "generate-instructions.sh").read_text(encoding="utf-8")
    specify_script = (ROOT / ".specify" / "scripts" / "bash" / "generate-instructions.sh").read_text(encoding="utf-8")

    assert "project_rules.md" in root_script
    assert "project_rules.md" in specify_script
    assert ".qoder" in root_script
    assert ".qoder" in specify_script


def test_agents_prompt_approved_provider_list_includes_qoder():
    prompt = (ROOT / ".github" / "prompts" / "speckit.agents.prompt.md").read_text(encoding="utf-8")
    assert "Qoder" in prompt
