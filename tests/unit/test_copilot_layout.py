from pathlib import Path

from specify_cli import AGENT_CONFIG, copy_local_templates


def test_copilot_folder_is_github():
    copilot = AGENT_CONFIG["copilot"]
    assert copilot["folder"] == ".github/"


def test_copy_local_templates_copilot_uses_github_prompts_and_symlinked_skills(
    monkeypatch, tmp_path: Path, qoder_minimal_resource_path: Path
):
    monkeypatch.setattr(
        "specify_cli.get_resource_path", lambda: qoder_minimal_resource_path
    )

    project_path = tmp_path / "demo"
    copy_local_templates(project_path, "copilot", "sh")

    assert (project_path / ".github" / "prompts").exists()
    assert any((project_path / ".github" / "prompts").glob("*.prompt.md"))
    assert (project_path / ".specify" / "skills").exists()

    github_skills = project_path / ".github" / "skills"
    assert github_skills.exists()
    assert github_skills.is_symlink()
    assert github_skills.readlink() == Path("../.specify/skills")
    assert github_skills.resolve() == (project_path / ".specify" / "skills").resolve()


def test_copy_local_templates_non_copilot_does_not_create_github(
    monkeypatch, tmp_path: Path, qoder_minimal_resource_path: Path
):
    monkeypatch.setattr(
        "specify_cli.get_resource_path", lambda: qoder_minimal_resource_path
    )

    project_path = tmp_path / "demo"
    copy_local_templates(project_path, "qoder", "sh")

    assert (project_path / ".specify" / "skills").exists()
    assert not (project_path / ".github").exists()


def test_copy_local_templates_copilot_migrates_existing_github_skills(
    monkeypatch, tmp_path: Path, qoder_minimal_resource_path: Path
):
    monkeypatch.setattr(
        "specify_cli.get_resource_path", lambda: qoder_minimal_resource_path
    )

    project_path = tmp_path / "demo"
    (project_path / ".github" / "skills" / "legacy").mkdir(parents=True)
    (project_path / ".github" / "skills" / "legacy" / "note.txt").write_text(
        "legacy", encoding="utf-8"
    )

    copy_local_templates(project_path, "copilot", "sh", is_current_dir=True)

    assert (project_path / ".specify" / "skills" / "legacy" / "note.txt").exists()
    github_skills = project_path / ".github" / "skills"
    assert github_skills.is_symlink()
    assert github_skills.readlink() == Path("../.specify/skills")
