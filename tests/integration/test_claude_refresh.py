from pathlib import Path

from specify_cli import copy_local_templates


def test_claude_refresh_like_copy_does_not_remove_other_assistant_roots(
    monkeypatch, tmp_path: Path, claude_minimal_resource_path: Path
):
    monkeypatch.setattr(
        "specify_cli.get_resource_path", lambda: claude_minimal_resource_path
    )

    project_path = tmp_path / "demo"
    (project_path / ".qoder").mkdir(parents=True)
    (project_path / ".github").mkdir(parents=True)

    copy_local_templates(project_path, "claude", "sh", is_current_dir=True)

    assert (project_path / ".qoder").exists()
    assert (project_path / ".github").exists()
    assert (project_path / ".claude" / "commands").exists()


def test_claude_skills_are_linked_to_specify(
    monkeypatch, tmp_path: Path, claude_minimal_resource_path: Path
):
    monkeypatch.setattr(
        "specify_cli.get_resource_path", lambda: claude_minimal_resource_path
    )

    project_path = tmp_path / "demo"
    copy_local_templates(project_path, "claude", "sh")

    claude_skills = project_path / ".claude" / "skills"
    assert claude_skills.exists()
    assert claude_skills.is_symlink()
