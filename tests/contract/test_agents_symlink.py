"""Contract tests: agent directory-level symlink creation and migration."""

import pytest
from pathlib import Path

from specify_cli import ensure_specify_symlink


@pytest.mark.contract
class TestAgentsSymlinkCreation:
    """Verify directory-level symlink creation for agents."""

    def test_github_agents_symlink_resolves(self, tmp_path):
        (tmp_path / ".specify").mkdir()
        ensure_specify_symlink(tmp_path, ".github", "agents")

        link = tmp_path / ".github" / "agents"
        assert link.is_symlink()
        assert link.resolve() == (tmp_path / ".specify" / "agents").resolve()

    def test_qoder_agents_symlink_resolves(self, tmp_path):
        (tmp_path / ".specify").mkdir()
        ensure_specify_symlink(tmp_path, ".qoder", "agents")

        link = tmp_path / ".qoder" / "agents"
        assert link.is_symlink()
        assert link.resolve() == (tmp_path / ".specify" / "agents").resolve()

    def test_qwen_agents_symlink_resolves(self, tmp_path):
        (tmp_path / ".specify").mkdir()
        ensure_specify_symlink(tmp_path, ".qwen", "agents")

        link = tmp_path / ".qwen" / "agents"
        assert link.is_symlink()
        assert link.resolve() == (tmp_path / ".specify" / "agents").resolve()

    def test_opencode_agents_symlink_resolves(self, tmp_path):
        (tmp_path / ".specify").mkdir()
        ensure_specify_symlink(tmp_path, ".opencode", "agents")

        link = tmp_path / ".opencode" / "agents"
        assert link.is_symlink()
        assert link.resolve() == (tmp_path / ".specify" / "agents").resolve()

    def test_agent_visible_through_symlink(self, tmp_path):
        (tmp_path / ".specify" / "agents").mkdir(parents=True)
        (tmp_path / ".specify" / "agents" / "my-agent.agent.md").write_text("agent content")

        ensure_specify_symlink(tmp_path, ".github", "agents")

        via_symlink = tmp_path / ".github" / "agents" / "my-agent.agent.md"
        assert via_symlink.exists()
        assert via_symlink.read_text() == "agent content"


@pytest.mark.contract
class TestAgentsSymlinkMigration:
    """Verify migration of existing regular directories to symlinks."""

    def test_regular_directory_migrated_to_symlink(self, tmp_path):
        (tmp_path / ".specify").mkdir()
        regular_dir = tmp_path / ".github" / "agents"
        regular_dir.mkdir(parents=True)
        (regular_dir / "legacy.agent.md").write_text("legacy agent")

        ensure_specify_symlink(tmp_path, ".github", "agents")

        link = tmp_path / ".github" / "agents"
        assert link.is_symlink()
        migrated = tmp_path / ".specify" / "agents" / "legacy.agent.md"
        assert migrated.exists()
        assert migrated.read_text() == "legacy agent"

    def test_multiple_files_migrated(self, tmp_path):
        (tmp_path / ".specify").mkdir()
        regular_dir = tmp_path / ".github" / "agents"
        regular_dir.mkdir(parents=True)
        (regular_dir / "agent-a.agent.md").write_text("a")
        (regular_dir / "agent-b.agent.md").write_text("b")
        refs = regular_dir / "references"
        refs.mkdir()
        (refs / "shared.md").write_text("shared")

        ensure_specify_symlink(tmp_path, ".github", "agents")

        assert (tmp_path / ".specify" / "agents" / "agent-a.agent.md").read_text() == "a"
        assert (tmp_path / ".specify" / "agents" / "agent-b.agent.md").read_text() == "b"
        assert (tmp_path / ".specify" / "agents" / "references" / "shared.md").read_text() == "shared"
        assert (tmp_path / ".github" / "agents").is_symlink()
