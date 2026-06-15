"""Unit tests for ensure_specify_symlink — the generalized directory symlink helper."""

import os
import pytest
from pathlib import Path

from specify_cli import ensure_specify_symlink


@pytest.fixture
def workspace(tmp_path):
    """Create a minimal workspace with .specify/ directory."""
    (tmp_path / ".specify").mkdir()
    return tmp_path


def test_fresh_create(workspace):
    """Symlink is created when nothing exists at the target path."""
    ensure_specify_symlink(workspace, ".github", "skills")

    link = workspace / ".github" / "skills"
    assert link.is_symlink()
    assert link.resolve() == (workspace / ".specify" / "skills").resolve()


def test_fresh_create_agents(workspace):
    """Works for agents subdir too, not just skills."""
    ensure_specify_symlink(workspace, ".qoder", "agents")

    link = workspace / ".qoder" / "agents"
    assert link.is_symlink()
    assert link.resolve() == (workspace / ".specify" / "agents").resolve()


def test_existing_correct_symlink_is_noop(workspace):
    """When the symlink already points to the right target, do nothing."""
    ensure_specify_symlink(workspace, ".github", "skills")
    link = workspace / ".github" / "skills"
    first_stat = os.lstat(link)

    ensure_specify_symlink(workspace, ".github", "skills")
    second_stat = os.lstat(link)

    assert link.is_symlink()
    assert first_stat.st_ino == second_stat.st_ino


def test_existing_stale_symlink_is_relinked(workspace):
    """When symlink points to wrong target, replace it."""
    agent_dir = workspace / ".github"
    agent_dir.mkdir(parents=True, exist_ok=True)
    stale_target = workspace / "elsewhere"
    stale_target.mkdir()
    (agent_dir / "skills").symlink_to(stale_target)

    ensure_specify_symlink(workspace, ".github", "skills")

    link = agent_dir / "skills"
    assert link.is_symlink()
    assert link.resolve() == (workspace / ".specify" / "skills").resolve()


def test_existing_regular_directory_is_migrated(workspace):
    """When a regular directory exists, its content is migrated to .specify/ and replaced with a symlink."""
    agent_dir = workspace / ".github"
    regular_dir = agent_dir / "agents"
    regular_dir.mkdir(parents=True)
    (regular_dir / "legacy-agent.agent.md").write_text("legacy content")

    ensure_specify_symlink(workspace, ".github", "agents")

    link = agent_dir / "agents"
    assert link.is_symlink()
    assert link.resolve() == (workspace / ".specify" / "agents").resolve()
    migrated = workspace / ".specify" / "agents" / "legacy-agent.agent.md"
    assert migrated.exists()
    assert migrated.read_text() == "legacy content"


def test_creates_parent_directories(workspace):
    """Tool directory and .specify/ subdirectory are auto-created."""
    ensure_specify_symlink(workspace, ".opencode", "agents")

    assert (workspace / ".opencode").is_dir()
    assert (workspace / ".specify" / "agents").is_dir()
    assert (workspace / ".opencode" / "agents").is_symlink()


def test_relative_symlink_path(workspace):
    """Symlink uses a relative path, not absolute."""
    ensure_specify_symlink(workspace, ".github", "skills")

    link = workspace / ".github" / "skills"
    raw_target = os.readlink(link)
    assert not os.path.isabs(raw_target)
