from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_generate_instructions_scripts_cover_claude_project_rules():
    root_script = (ROOT / "scripts" / "bash" / "generate-instructions.sh").read_text(
        encoding="utf-8"
    )
    specify_script = (
        ROOT / ".specify" / "scripts" / "bash" / "generate-instructions.sh"
    ).read_text(encoding="utf-8")

    assert ".claude" in root_script
    assert ".claude" in specify_script
    assert "project_rules.md" in root_script
    assert "project_rules.md" in specify_script


def test_usage_doc_documents_claude_refresh_flow():
    usage = (ROOT / "docs" / "usage.md").read_text(encoding="utf-8")
    assert "Claude Code Maintenance Workflow" in usage
    assert "generate-instructions.sh" in usage
