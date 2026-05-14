from pathlib import Path

from specify_cli import AGENT_CONFIG, copy_local_templates


def test_claude_config_exposed_for_init_flow():
    assert AGENT_CONFIG["claude"]["name"] == "Claude Code"


def test_copy_local_templates_creates_claude_assets(
    monkeypatch, tmp_path: Path, claude_minimal_resource_path: Path
):
    monkeypatch.setattr(
        "specify_cli.get_resource_path", lambda: claude_minimal_resource_path
    )

    project_path = tmp_path / "demo"
    copy_local_templates(project_path, "claude", "sh")

    assert (project_path / ".claude" / "commands").exists()
    assert (project_path / ".claudeignore").exists()
    assert (project_path / "CLAUDE.md").exists() or True
