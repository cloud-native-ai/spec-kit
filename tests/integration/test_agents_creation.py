"""Integration test: verify the agents command template targets .specify/agents/ as canonical path."""

import pytest
from pathlib import Path


@pytest.mark.integration
class TestAgentsCommandTemplate:
    """Verify the agents command template uses canonical .specify/agents/ paths."""

    @pytest.fixture
    def agents_template(self):
        template_path = Path(__file__).parent.parent.parent / "templates" / "commands" / "agents.md"
        if not template_path.exists():
            pytest.skip("agents.md template not found at expected path")
        return template_path.read_text()

    def test_canonical_path_is_specify_agents(self, agents_template):
        assert ".specify/agents/" in agents_template

    def test_no_direct_github_agents_target(self, agents_template):
        lines_with_target = [
            line for line in agents_template.splitlines()
            if "Target path:" in line or "target path:" in line.lower()
        ]
        for line in lines_with_target:
            assert ".github/agents/" not in line, (
                f"Template still targets .github/agents/ directly: {line}"
            )

    def test_workspace_files_documented(self, agents_template):
        for ws_file in ["AGENTS.md", "MEMORY.md", "SOUL.md", "USER.md"]:
            assert ws_file in agents_template, f"Workspace file {ws_file} not documented in template"

    def test_references_directory_documented(self, agents_template):
        assert ".specify/agents/references/" in agents_template

    def test_agent_id_uses_canonical_path(self, agents_template):
        assert ".specify/agents/" in agents_template
        id_lines = [
            line for line in agents_template.splitlines()
            if "Agent ID:" in line
        ]
        for line in id_lines:
            if ".github/agents/" in line:
                pytest.fail(f"agent_id still references .github/agents/: {line}")

    def test_valid_file_locations_updated(self, agents_template):
        assert "Canonical (workspace) scope:" in agents_template or "canonical location" in agents_template.lower()
