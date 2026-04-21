from pathlib import Path

from specify_cli import AGENT_CONFIG, copy_local_templates


def test_qoder_is_registered_in_agent_config():
    qoder = AGENT_CONFIG["qoder"]
    assert qoder["name"] == "Qoder CLI"
    assert qoder["folder"] == ".qoder/"
    assert qoder["install_url"] == "https://qoder.com/cli"
    assert qoder["requires_cli"] is True


def test_copy_local_templates_generates_qoder_commands(
    monkeypatch, tmp_path: Path, qoder_minimal_resource_path: Path
):
    monkeypatch.setattr(
        "specify_cli.get_resource_path", lambda: qoder_minimal_resource_path
    )

    project_path = tmp_path / "demo"
    copy_local_templates(project_path, "qoder", "sh")

    commands_dir = project_path / ".qoder" / "commands"
    assert commands_dir.exists()
    assert any(commands_dir.glob("*.md"))


def test_copy_local_templates_qoder_symlinks_skills_to_specify(
    monkeypatch, tmp_path: Path, qoder_minimal_resource_path: Path
):
    monkeypatch.setattr(
        "specify_cli.get_resource_path", lambda: qoder_minimal_resource_path
    )

    project_path = tmp_path / "demo"
    copy_local_templates(project_path, "qoder", "sh")

    assert (project_path / ".specify" / "skills").exists()

    qoder_skills = project_path / ".qoder" / "skills"
    assert qoder_skills.exists()
    assert qoder_skills.is_symlink()
    assert qoder_skills.resolve() == (project_path / ".specify" / "skills").resolve()
