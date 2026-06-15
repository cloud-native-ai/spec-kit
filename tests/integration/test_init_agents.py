"""Integration tests: specify init copies bundled agents and preserves user agents."""

import shutil
import pytest
from pathlib import Path

from specify_cli import ensure_specify_symlink


@pytest.mark.integration
class TestInitAgentsCopy:
    """Verify that bundled agents are copied to .specify/agents/ during init."""

    @pytest.fixture
    def agents_source(self):
        """Path to the bundled agents directory in the package."""
        src = Path(__file__).parent.parent.parent / "agents"
        if not src.exists() or not any(src.glob("*.agent.md")):
            pytest.skip("No bundled agents found in agents/ directory")
        return src

    def test_bundled_agents_copied_to_specify(self, tmp_path, agents_source):
        dest = tmp_path / ".specify" / "agents"
        dest.mkdir(parents=True, exist_ok=True)

        shutil.copytree(agents_source, dest, dirs_exist_ok=True)

        assert (dest / "code-reviewer.agent.md").exists()
        assert (dest / "references").is_dir()

    def test_references_directory_preserved(self, tmp_path, agents_source):
        dest = tmp_path / ".specify" / "agents"
        dest.mkdir(parents=True, exist_ok=True)

        shutil.copytree(agents_source, dest, dirs_exist_ok=True)

        assert (dest / "references").is_dir()
        assert (dest / "references" / ".gitkeep").exists()

    def test_symlink_created_after_copy(self, tmp_path, agents_source):
        dest = tmp_path / ".specify" / "agents"
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copytree(agents_source, dest, dirs_exist_ok=True)

        ensure_specify_symlink(tmp_path, ".github", "agents")

        assert (tmp_path / ".github" / "agents").is_symlink()
        assert (tmp_path / ".github" / "agents" / "code-reviewer.agent.md").exists()


@pytest.mark.integration
class TestInitAgentsPreservation:
    """Verify that user agents are preserved during re-init."""

    @pytest.fixture
    def agents_source(self):
        src = Path(__file__).parent.parent.parent / "agents"
        if not src.exists():
            pytest.skip("No bundled agents found")
        return src

    def test_user_agent_not_overwritten(self, tmp_path, agents_source):
        dest = tmp_path / ".specify" / "agents"
        dest.mkdir(parents=True, exist_ok=True)

        (dest / "my-custom-agent.agent.md").write_text("user content")

        shutil.copytree(agents_source, dest, dirs_exist_ok=True)

        assert (dest / "my-custom-agent.agent.md").read_text() == "user content"
        assert (dest / "code-reviewer.agent.md").exists()

    def test_bundled_and_user_agents_coexist(self, tmp_path, agents_source):
        dest = tmp_path / ".specify" / "agents"
        dest.mkdir(parents=True, exist_ok=True)

        (dest / "user-agent.agent.md").write_text("custom agent")
        shutil.copytree(agents_source, dest, dirs_exist_ok=True)

        agent_files = list(dest.glob("*.agent.md"))
        names = {f.name for f in agent_files}
        assert "user-agent.agent.md" in names
        assert "code-reviewer.agent.md" in names
