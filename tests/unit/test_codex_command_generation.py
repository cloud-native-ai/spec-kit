"""Unit test for Codex CLI command generation (T020).

Verifies generate_commands produces correct file count and content for codex.
"""

from pathlib import Path

from specify_cli import generate_commands


def test_codex_generate_commands_produces_md_files(
    monkeypatch, tmp_path: Path, codex_minimal_resource_path: Path
):
    monkeypatch.setattr(
        "specify_cli.get_resource_path", lambda: codex_minimal_resource_path
    )

    output_dir = tmp_path / ".codex" / "commands"
    generate_commands("codex", "md", "$ARGUMENTS", output_dir, "sh")

    assert output_dir.exists()
    md_files = list(output_dir.glob("*.md"))
    assert len(md_files) >= 1, "No command files generated for codex"


def test_codex_command_files_use_dollar_arguments(
    monkeypatch, tmp_path: Path, codex_minimal_resource_path: Path
):
    monkeypatch.setattr(
        "specify_cli.get_resource_path", lambda: codex_minimal_resource_path
    )

    output_dir = tmp_path / ".codex" / "commands"
    generate_commands("codex", "md", "$ARGUMENTS", output_dir, "sh")

    for f in output_dir.glob("*.md"):
        content = f.read_text(encoding="utf-8")
        assert "{{args}}" not in content, f"{f.name} uses Qwen-style args"
