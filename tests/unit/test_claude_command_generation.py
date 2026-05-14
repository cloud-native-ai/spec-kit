from pathlib import Path

from specify_cli import copy_local_templates


def test_copy_local_templates_generates_claude_commands(
    monkeypatch, tmp_path: Path, claude_minimal_resource_path: Path
):
    monkeypatch.setattr(
        "specify_cli.get_resource_path", lambda: claude_minimal_resource_path
    )

    project_path = tmp_path / "demo"
    copy_local_templates(project_path, "claude", "sh")

    commands_dir = project_path / ".claude" / "commands"
    assert commands_dir.exists()
    assert any(commands_dir.glob("*.md"))


def test_generated_claude_command_keeps_arguments_placeholder(
    monkeypatch, tmp_path: Path, claude_minimal_resource_path: Path
):
    monkeypatch.setattr(
        "specify_cli.get_resource_path", lambda: claude_minimal_resource_path
    )

    project_path = tmp_path / "demo"
    copy_local_templates(project_path, "claude", "sh")

    command_files = list((project_path / ".claude" / "commands").glob("*.md"))
    assert command_files
    content = command_files[0].read_text(encoding="utf-8")
    assert "$ARGUMENTS" in content
