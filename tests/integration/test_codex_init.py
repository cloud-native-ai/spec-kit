"""Integration test for specify init --ai codex flow (T018).

Verifies .codex/ directory created, command files generated, and init
produces the expected assets.
"""

import pytest

from pathlib import Path

from specify_cli import AGENT_CONFIG, copy_local_templates

pytestmark = pytest.mark.integration


def test_codex_config_exposed_for_init_flow():
    assert AGENT_CONFIG["codex"]["name"] == "Codex CLI"


def test_copy_local_templates_creates_codex_assets(
    monkeypatch, tmp_path: Path, codex_minimal_resource_path: Path
):
    monkeypatch.setattr(
        "specify_cli.get_resource_path", lambda: codex_minimal_resource_path
    )

    project_path = tmp_path / "demo"
    copy_local_templates(project_path, "codex", "sh")

    assert (project_path / ".codex" / "commands").exists()
    assert (project_path / ".codexignore").exists()


def test_copy_local_templates_creates_specify_core(
    monkeypatch, tmp_path: Path, codex_minimal_resource_path: Path
):
    monkeypatch.setattr(
        "specify_cli.get_resource_path", lambda: codex_minimal_resource_path
    )

    project_path = tmp_path / "demo"
    copy_local_templates(project_path, "codex", "sh")

    assert (project_path / ".specify").is_dir()
    assert (project_path / ".specify" / "memory").is_dir()
    assert (project_path / ".specify" / "scripts").is_dir()
    assert (project_path / ".specify" / "skills").is_dir()
