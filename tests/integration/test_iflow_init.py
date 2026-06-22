"""Integration tests for specify init --ai iflow flow (Spec 019)."""

import hashlib
from pathlib import Path

import pytest

from specify_cli import AGENT_CONFIG, copy_local_templates

pytestmark = pytest.mark.integration


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_iflow_config_exposed_for_init_flow():
    assert AGENT_CONFIG["iflow"]["name"] == "iFlow"


def test_copy_local_templates_creates_iflow_assets(
    monkeypatch, tmp_path: Path, ai_tools_resource_path: Path
):
    monkeypatch.setattr("specify_cli.get_resource_path", lambda: ai_tools_resource_path)

    project_path = tmp_path / "demo"
    copy_local_templates(project_path, "iflow", "sh")

    commands_dir = project_path / ".iflow" / "commands"
    assert commands_dir.exists()
    assert any(p.suffix == ".md" for p in commands_dir.iterdir() if p.is_file())


def test_copy_local_templates_creates_iflow_skills_symlink(
    monkeypatch, tmp_path: Path, ai_tools_resource_path: Path
):
    monkeypatch.setattr("specify_cli.get_resource_path", lambda: ai_tools_resource_path)

    project_path = tmp_path / "demo"
    copy_local_templates(project_path, "iflow", "sh")

    skills_link = project_path / ".iflow" / "skills"
    assert skills_link.exists()
    assert skills_link.is_symlink()
    assert skills_link.resolve() == (project_path / ".specify" / "skills").resolve()


def test_adding_iflow_preserves_existing_specify_core(
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

    copy_local_templates(project_path, "iflow", "sh", is_current_dir=True)

    after = {str(path): _sha256(path) for path in core_files}
    assert after == before
