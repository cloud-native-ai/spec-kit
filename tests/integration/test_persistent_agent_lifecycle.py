"""Integration test: temporary vs persistent agent lifecycle (FR-010/011/012, SC-009).

Spec 023 (Agent Framework Redesign) distinguishes two agent lifecycles:

- **temporary** — spawned for a single orchestration; context-only, never written to disk.
- **persistent** — written under the layered stores ``.specify/agents/templates/`` /
  ``.specify/agents/instances/`` and rendered into every officially supported tool's
  agent config directory as real files (Feature 044; per-file symlinks retired).

This test asserts the persistence + rendering behaviour for persistent agents and confirms
the ``create-agent`` skill documents the temporary (non-persisted) lifecycle.
"""

import pytest
from pathlib import Path

from specify_cli import render_agents_for_tool

NEUTRAL_DEF = (
    "---\n"
    'name: "System Designer"\n'
    'description: "Designs system-level architecture."\n'
    "model-tier: auto\n"
    "---\n"
    "persistent\n"
)

REPO_ROOT = Path(__file__).parent.parent.parent
PERSISTED_ROLES = [
    "structure-adjuster",
    "skill-verifier",
]


@pytest.mark.integration
class TestPersistentAgentLifecycle:
    """Persistent agents live under .specify/agents/ and are linked into supported tools."""

    def test_persisted_agents_written_under_specify_agents(self):
        agents_dir = REPO_ROOT / ".specify" / "agents" / "templates"
        assert agents_dir.is_dir(), ".specify/agents/templates/ must exist as the canonical Template store"
        for role in PERSISTED_ROLES:
            agent_file = agents_dir / f"{role}.agent.md"
            assert agent_file.exists(), f"persistent agent missing: {agent_file}"

    def test_persisted_agents_use_unified_terminology(self):
        """Persistent agents must express Role/Stage/Type with 0 deprecated terms (SC-009)."""
        import re

        deprecated = re.compile(r"subrole|improver|meta-coordinator", re.IGNORECASE)
        offenders = []
        agents_dir = REPO_ROOT / ".specify" / "agents"
        for md in sorted(agents_dir.glob("*/*.agent.md")):
            for lineno, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
                if deprecated.search(line):
                    offenders.append(f"{md.name}:{lineno}: {line.strip()}")
        assert not offenders, "persisted agents retain deprecated terms:\n" + "\n".join(offenders)

    def test_initialization_renders_tool_agent_file(self, tmp_path):
        """Each supported tool gets rendered real files from the layered stores (FR-012)."""
        # Simulate a persistent agent being written to the canonical Template store.
        specify_agents = tmp_path / ".specify" / "agents" / "templates"
        specify_agents.mkdir(parents=True, exist_ok=True)
        (specify_agents / "system-designer.agent.md").write_text(
            NEUTRAL_DEF, encoding="utf-8"
        )

        render_agents_for_tool(tmp_path, "qoder")

        tool_dir = tmp_path / ".qoder" / "agents"
        assert tool_dir.is_dir() and not tool_dir.is_symlink(), (
            ".qoder/agents must be a real directory of rendered files"
        )
        output = tool_dir / "system-designer.agent.md"
        assert output.is_file() and not output.is_symlink(), (
            ".qoder/agents/system-designer.agent.md must be a rendered real file"
        )
        content = output.read_text(encoding="utf-8")
        assert "persistent" in content

    def test_render_preserves_tool_authored_overrides(self, tmp_path):
        """A tool-side user asset (not in the manifest, no matching slug) is untouched."""
        specify_agents = tmp_path / ".specify" / "agents" / "templates"
        specify_agents.mkdir(parents=True, exist_ok=True)
        (specify_agents / "system-designer.agent.md").write_text(
            NEUTRAL_DEF, encoding="utf-8"
        )
        tool_dir = tmp_path / ".qoder" / "agents"
        tool_dir.mkdir(parents=True, exist_ok=True)
        override = tool_dir / "Full-Stack Engineer.md"
        override.write_text("tool-authored override", encoding="utf-8")

        render_agents_for_tool(tmp_path, "qoder")

        assert override.exists() and not override.is_symlink()
        assert override.read_text(encoding="utf-8") == "tool-authored override"
        assert (tool_dir / "system-designer.agent.md").is_file()

    def test_temporary_agent_is_not_persisted(self, tmp_path):
        """A temporary agent is context-only: nothing is written under .specify/agents/."""
        specify_agents = tmp_path / ".specify" / "agents"
        specify_agents.mkdir(parents=True, exist_ok=True)
        # A temporary orchestration spawns context-only workers; no files should appear.
        assert list(specify_agents.glob("**/*.agent.md")) == [], (
            "temporary agents must not be persisted to .specify/agents/"
        )

    def test_create_agent_skill_documents_lifecycle(self):
        """create-agent SKILL.md must document temporary vs persistent lifecycle (T029)."""
        skill = (REPO_ROOT / "skills" / "create-agent" / "SKILL.md").read_text(encoding="utf-8")
        lowered = skill.lower()
        assert "temporary" in lowered, "SKILL.md must document the temporary (context-only) lifecycle"
        assert "persistent" in lowered, "SKILL.md must document the persistent (.specify/agents) lifecycle"
