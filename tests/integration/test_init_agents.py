"""Integration tests: specify init copies bundled agents and preserves user agents.

Current install contract (see ``shared/definitions/agent-definitions.md``):
bundled agents land in ``.specify/agents/templates/`` (Agent Template layer),
agent definitions are self-contained (no shared-assets ``references/`` directory),
and tool directories receive **rendered real files** translated from the neutral
metadata of ``templates/`` + ``instances/`` (Feature 044; symlinks retired).
"""

import shutil
import pytest
from pathlib import Path

from specify_cli import ensure_agent_layer_dirs, render_agents_for_tool

RENDER_MATRIX = {
    "qoder": (".qoder/agents", ".agent.md"),
    "claude": (".claude/agents", ".md"),
    "copilot": (".github/agents", ".agent.md"),
    "opencode": (".opencode/agents", ".md"),
}


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

    @pytest.mark.parametrize("tool", sorted(RENDER_MATRIX))
    def test_rendered_files_created_after_copy(self, tmp_path, agents_source, tool):
        dest = ensure_agent_layer_dirs(tmp_path) / "templates"
        shutil.copytree(agents_source, dest, dirs_exist_ok=True)

        stats = render_agents_for_tool(tmp_path, tool)

        rel_dir, suffix = RENDER_MATRIX[tool]
        tool_dir = tmp_path / Path(rel_dir)
        assert tool_dir.is_dir() and not tool_dir.is_symlink()
        outputs = sorted(tool_dir.glob(f"*{suffix}"))
        expected_count = len(list(dest.glob("*.agent.md")))
        assert stats["rendered"] == expected_count
        assert len(outputs) == expected_count
        assert not any(p.is_symlink() for p in tool_dir.iterdir()), (
            "rendered agents must be real files, never symlinks (SC-002)"
        )


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
