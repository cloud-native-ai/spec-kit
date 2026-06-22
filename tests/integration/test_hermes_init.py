"""Integration tests for specify init --ai hermes flow (Spec 019)."""

import hashlib
from pathlib import Path

import pytest

from specify_cli import AGENT_CONFIG, copy_local_templates

pytestmark = pytest.mark.integration


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_hermes_config_exposed_for_init_flow():
    assert AGENT_CONFIG["hermes"]["name"] == "Hermes Agent"


def test_copy_local_templates_creates_hermes_assets(
    monkeypatch, tmp_path: Path, ai_tools_resource_path: Path
):
    monkeypatch.setattr("specify_cli.get_resource_path", lambda: ai_tools_resource_path)

    project_path = tmp_path / "demo"
    copy_local_templates(project_path, "hermes", "sh")

    commands_dir = project_path / ".hermes" / "commands"
    assert commands_dir.exists()
    assert any(p.suffix == ".md" for p in commands_dir.iterdir() if p.is_file())


def test_copy_local_templates_creates_hermes_skills_symlink(
    monkeypatch, tmp_path: Path, ai_tools_resource_path: Path
):
    monkeypatch.setattr("specify_cli.get_resource_path", lambda: ai_tools_resource_path)

    project_path = tmp_path / "demo"
    copy_local_templates(project_path, "hermes", "sh")

    skills_link = project_path / ".hermes" / "skills"
    assert skills_link.exists()
    assert skills_link.is_symlink()
    assert skills_link.resolve() == (project_path / ".specify" / "skills").resolve()


def test_adding_hermes_preserves_existing_specify_core(
    monkeypatch, tmp_path: Path, ai_tools_resource_path: Path
):
    monkeypatch.setattr("specify_cli.get_resource_path", lambda: ai_tools_resource_path)

    project_path = tmp_path / "demo"
    copy_local_templates(project_path, "claude", "sh")

    core_files = [
        project_path / ".specify" / "memory" / "constitution.md",
        project_path / ".specify" / "memory" / "features.md",
    ]
    before = {str(path): _sha256(path) for path in core_files}

    copy_local_templates(project_path, "hermes", "sh", is_current_dir=True)

    after = {str(path): _sha256(path) for path in core_files}
    assert after == before
