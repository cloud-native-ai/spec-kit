"""Contract tests: per-file agent symlink creation and migration."""

import pytest
from pathlib import Path

from specify_cli import ensure_per_file_agent_links


def _seed_agent(root: Path, name: str = "my-agent.agent.md", content: str = "agent content"):
    agents = root / ".specify" / "agents"
    agents.mkdir(parents=True, exist_ok=True)
    (agents / name).write_text(content, encoding="utf-8")
    return agents / name


@pytest.mark.contract
class TestPerFileAgentLinkCreation:
    """Each tool's agents/ is a real directory of per-file symlinks."""

    @pytest.mark.parametrize("tool", [".github", ".qoder", ".qwen", ".opencode", ".hermes", ".iflow"])
    def test_tool_agents_is_real_dir_with_per_file_links(self, tmp_path, tool):
        source = _seed_agent(tmp_path)
        ensure_per_file_agent_links(tmp_path, tool)

        tool_dir = tmp_path / tool / "agents"
        assert tool_dir.is_dir() and not tool_dir.is_symlink(), (
            f"{tool}/agents must be a real directory, not a whole-dir symlink"
        )
        link = tool_dir / "my-agent.agent.md"
        assert link.is_symlink()
        assert link.resolve() == source.resolve()

    def test_agent_visible_through_link(self, tmp_path):
        _seed_agent(tmp_path, content="hello")
        ensure_per_file_agent_links(tmp_path, ".github")
        via_link = tmp_path / ".github" / "agents" / "my-agent.agent.md"
        assert via_link.exists()
        assert via_link.read_text(encoding="utf-8") == "hello"

    def test_only_agent_md_files_linked(self, tmp_path):
        _seed_agent(tmp_path)
        # A non-agent file in the canonical store must not be linked.
        (tmp_path / ".specify" / "agents" / "references").mkdir()
        (tmp_path / ".specify" / "agents" / "references" / "shared.md").write_text("x")
        ensure_per_file_agent_links(tmp_path, ".qoder")

        tool_dir = tmp_path / ".qoder" / "agents"
        assert (tool_dir / "my-agent.agent.md").is_symlink()
        assert not (tool_dir / "references").exists()


@pytest.mark.contract
class TestPerFileAgentLinkMigration:
    """Migration from the legacy whole-directory symlink model."""

    def test_legacy_whole_dir_symlink_replaced(self, tmp_path):
        source = _seed_agent(tmp_path)
        # Simulate the old model: .qoder/agents is a symlink to .specify/agents.
        (tmp_path / ".qoder").mkdir()
        legacy = tmp_path / ".qoder" / "agents"
        legacy.symlink_to(Path("../.specify/agents"), target_is_directory=True)
        assert legacy.is_symlink()

        ensure_per_file_agent_links(tmp_path, ".qoder")

        tool_dir = tmp_path / ".qoder" / "agents"
        assert tool_dir.is_dir() and not tool_dir.is_symlink()
        assert (tool_dir / "my-agent.agent.md").resolve() == source.resolve()

    def test_stale_links_pruned(self, tmp_path):
        _seed_agent(tmp_path, name="keep.agent.md")
        ensure_per_file_agent_links(tmp_path, ".github")
        tool_dir = tmp_path / ".github" / "agents"
        assert (tool_dir / "keep.agent.md").is_symlink()

        # Remove the canonical source and re-link: stale link must be pruned.
        (tmp_path / ".specify" / "agents" / "keep.agent.md").unlink()
        ensure_per_file_agent_links(tmp_path, ".github")
        assert not (tool_dir / "keep.agent.md").exists()

    def test_tool_authored_override_preserved(self, tmp_path):
        _seed_agent(tmp_path)
        tool_dir = tmp_path / ".qoder" / "agents"
        tool_dir.mkdir(parents=True)
        override = tool_dir / "Full-Stack Engineer.md"
        override.write_text("override", encoding="utf-8")

        ensure_per_file_agent_links(tmp_path, ".qoder")

        assert override.exists() and not override.is_symlink()
        assert override.read_text(encoding="utf-8") == "override"
        assert (tool_dir / "my-agent.agent.md").is_symlink()
