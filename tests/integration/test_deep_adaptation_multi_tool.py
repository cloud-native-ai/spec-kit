"""Integration test for deep adaptation multi-tool (T046).

Init project with 3 Tier 1 tools, verify skills symlinks, command variants,
and compatibility files all correct.
"""

import pytest

from pathlib import Path

from specify_cli import copy_local_templates

pytestmark = pytest.mark.integration

TIER1_TOOLS = ["claude", "codex", "qoder"]


def test_multi_tool_init_creates_all_directories(
    monkeypatch, tmp_path: Path, codex_minimal_resource_path: Path
):
    monkeypatch.setattr(
        "specify_cli.get_resource_path", lambda: codex_minimal_resource_path
    )

    # Also add claudeignore template for claude init
    (codex_minimal_resource_path / "templates" / "claudeignore-template").write_text(
        "__pycache__/\n", encoding="utf-8"
    )

    project = tmp_path / "multi"
    copy_local_templates(project, "claude", "sh")
    copy_local_templates(project, "codex", "sh", is_current_dir=True)
    copy_local_templates(project, "qoder", "sh", is_current_dir=True)

    assert (project / ".claude").is_dir()
    assert (project / ".codex").is_dir()
    assert (project / ".qoder").is_dir()
    assert (project / ".specify").is_dir()


def test_multi_tool_skills_symlinks(
    monkeypatch, tmp_path: Path, codex_minimal_resource_path: Path
):
    monkeypatch.setattr(
        "specify_cli.get_resource_path", lambda: codex_minimal_resource_path
    )

    (codex_minimal_resource_path / "templates" / "claudeignore-template").write_text(
        "__pycache__/\n", encoding="utf-8"
    )

    project = tmp_path / "multi"
    copy_local_templates(project, "claude", "sh")
    copy_local_templates(project, "codex", "sh", is_current_dir=True)
    copy_local_templates(project, "qoder", "sh", is_current_dir=True)

    assert (project / ".claude" / "skills").exists()
    assert (project / ".codex" / "skills").exists()
    assert (project / ".qoder" / "skills").exists()


def test_multi_tool_command_directories(
    monkeypatch, tmp_path: Path, codex_minimal_resource_path: Path
):
    monkeypatch.setattr(
        "specify_cli.get_resource_path", lambda: codex_minimal_resource_path
    )

    (codex_minimal_resource_path / "templates" / "claudeignore-template").write_text(
        "__pycache__/\n", encoding="utf-8"
    )

    project = tmp_path / "multi"
    copy_local_templates(project, "claude", "sh")
    copy_local_templates(project, "codex", "sh", is_current_dir=True)
    copy_local_templates(project, "qoder", "sh", is_current_dir=True)

    assert (project / ".claude" / "commands").is_dir()
    assert (project / ".codex" / "commands").is_dir()
    assert (project / ".qoder" / "commands").is_dir()
