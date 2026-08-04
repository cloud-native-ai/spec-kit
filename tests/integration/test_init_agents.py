"""Integration tests: specify init copies bundled agents and preserves user agents.

Current install contract (see ``shared/definitions/agent-definitions.md``):
bundled agents land in ``.specify/agents/templates/`` (Agent Template layer),
agent definitions are self-contained (no shared-assets ``references/`` directory),
and tool directories receive **per-file** symlinks aggregated from
``templates/`` + ``instances/``.
"""

import shutil
import pytest
from pathlib import Path

from specify_cli import ensure_agent_layer_dirs, ensure_per_file_agent_links


@pytest.mark.integration
class TestInitAgentsCopy:
    """Verify that bundled agents are copied to .specify/agents/templates/ during init."""

    @pytest.fixture
    def agents_source(self):
        """Path to the bundled agents directory in the package."""
        src = Path(__file__).parent.parent.parent / "agents"
        if not src.exists() or not any(src.glob("*.agent.md")):
            pytest.skip("No bundled agents found in agents/ directory")
        return src

    def test_bundled_agents_copied_to_templates_layer(self, tmp_path, agents_source):
        dest = ensure_agent_layer_dirs(tmp_path) / "templates"

        shutil.copytree(agents_source, dest, dirs_exist_ok=True)

        copied = {f.name for f in dest.glob("*.agent.md")}
        expected = {f.name for f in agents_source.glob("*.agent.md")}
        assert expected and expected <= copied

    def test_no_shared_assets_directory_shipped(self, tmp_path, agents_source):
        # Agent definitions are self-contained: the retired references/ dir
        # must neither ship in the bundle nor appear after the copy.
        assert not (agents_source / "references").exists()

        dest = ensure_agent_layer_dirs(tmp_path) / "templates"
        shutil.copytree(agents_source, dest, dirs_exist_ok=True)
        assert not (dest / "references").exists()

    def test_per_file_links_created_after_copy(self, tmp_path, agents_source):
        dest = ensure_agent_layer_dirs(tmp_path) / "templates"
        shutil.copytree(agents_source, dest, dirs_exist_ok=True)

        ensure_per_file_agent_links(tmp_path, ".github")

        tool_dir = tmp_path / ".github" / "agents"
        assert tool_dir.is_dir() and not tool_dir.is_symlink()
        for source in dest.glob("*.agent.md"):
            assert (tool_dir / source.name).is_symlink()


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
        dest = ensure_agent_layer_dirs(tmp_path) / "templates"

        (dest / "my-custom-agent.agent.md").write_text("user content")

        shutil.copytree(agents_source, dest, dirs_exist_ok=True)

        assert (dest / "my-custom-agent.agent.md").read_text() == "user content"

    def test_bundled_and_user_agents_coexist(self, tmp_path, agents_source):
        dest = ensure_agent_layer_dirs(tmp_path) / "templates"

        (dest / "user-agent.agent.md").write_text("custom agent")
        shutil.copytree(agents_source, dest, dirs_exist_ok=True)

        names = {f.name for f in dest.glob("*.agent.md")}
        assert "user-agent.agent.md" in names

    def test_project_instance_survives_reinstall(self, tmp_path, agents_source):
        # Instances live in their own layer; re-copying templates never touches them.
        agents_root = ensure_agent_layer_dirs(tmp_path)
        instance = agents_root / "instances" / "repo-analyst.agent.md"
        instance.write_text("instance content")

        shutil.copytree(agents_source, agents_root / "templates", dirs_exist_ok=True)

        assert instance.read_text() == "instance content"
