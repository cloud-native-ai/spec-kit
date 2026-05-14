from pathlib import Path

from specify_cli import copy_local_templates


def test_copy_local_templates_generates_claudeignore(
    monkeypatch, tmp_path: Path, claude_minimal_resource_path: Path
):
    monkeypatch.setattr(
        "specify_cli.get_resource_path", lambda: claude_minimal_resource_path
    )

    project_path = tmp_path / "demo"
    copy_local_templates(project_path, "claude", "sh")

    ignore_file = project_path / ".claudeignore"
    assert ignore_file.exists()


def test_claudeignore_template_keeps_specify_paths_visible():
    root = Path(__file__).resolve().parents[2]
    template = (root / "templates" / "claudeignore-template").read_text(
        encoding="utf-8"
    )

    assert "!.specify/instructions.md" in template
    assert "!.specify/specs/" in template
    assert "!.claude/commands/" in template
