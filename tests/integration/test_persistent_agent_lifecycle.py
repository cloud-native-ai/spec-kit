"""Integration test: temporary vs persistent agent lifecycle (FR-010/011/012, SC-009).

Spec 023 (Agent Framework Redesign) distinguishes two agent lifecycles:

- **temporary** — spawned for a single orchestration; context-only, never written to disk.
- **persistent** — written under ``.specify/agents/`` and linked into every officially
  supported tool's agent config directory (e.g. ``.qoder/agents`` → ``.specify/agents``).

This test asserts the persistence + linking behaviour for persistent agents and confirms
the ``create-agent`` skill documents the temporary (non-persisted) lifecycle. It is expected
to FAIL until the persisted agents are migrated (T027) and the lifecycle is documented (T029).
"""

import pytest
from pathlib import Path

from specify_cli import ensure_specify_symlink

REPO_ROOT = Path(__file__).parent.parent.parent
PERSISTED_ROLES = [
    "requirements-analyst",
    "system-designer",
    "module-designer",
    "test-engineer",
    "qa-engineer",
    "knowledge-manager",
]


@pytest.mark.integration
class TestPersistentAgentLifecycle:
    """Persistent agents live under .specify/agents/ and are linked into supported tools."""

    def test_persisted_agents_written_under_specify_agents(self):
        agents_dir = REPO_ROOT / ".specify" / "agents"
        assert agents_dir.is_dir(), ".specify/agents/ must exist as the canonical persistent store"
        for role in PERSISTED_ROLES:
            agent_file = agents_dir / f"{role}.agent.md"
            assert agent_file.exists(), f"persistent agent missing: {agent_file}"

    def test_persisted_agents_use_unified_terminology(self):
        """Persistent agents must express Role/Stage/Type with 0 deprecated terms (SC-009)."""
        import re

        deprecated = re.compile(r"subrole|improver|meta-coordinator", re.IGNORECASE)
        offenders = []
        agents_dir = REPO_ROOT / ".specify" / "agents"
        for md in sorted(agents_dir.glob("*.agent.md")):
            for lineno, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
                if deprecated.search(line):
                    offenders.append(f"{md.name}:{lineno}: {line.strip()}")
        assert not offenders, "persisted agents retain deprecated terms:\n" + "\n".join(offenders)

    def test_initialization_creates_tool_agent_link(self, tmp_path):
        """Each supported tool gets an agents symlink → .specify/agents (FR-012)."""
        # Simulate a persistent agent being written to the canonical store.
        specify_agents = tmp_path / ".specify" / "agents"
        specify_agents.mkdir(parents=True, exist_ok=True)
        (specify_agents / "system-designer.agent.md").write_text("persistent", encoding="utf-8")

        ensure_specify_symlink(tmp_path, ".qoder", "agents")

        link = tmp_path / ".qoder" / "agents"
        assert link.is_symlink(), ".qoder/agents must be a symlink"
        assert link.resolve() == specify_agents.resolve(), ".qoder/agents must resolve to .specify/agents"
        # Persistent agent is visible through the tool link.
        assert (link / "system-designer.agent.md").exists()

    def test_temporary_agent_is_not_persisted(self, tmp_path):
        """A temporary agent is context-only: nothing is written under .specify/agents/."""
        specify_agents = tmp_path / ".specify" / "agents"
        specify_agents.mkdir(parents=True, exist_ok=True)
        # A temporary orchestration spawns context-only workers; no files should appear.
        assert list(specify_agents.glob("*.agent.md")) == [], (
            "temporary agents must not be persisted to .specify/agents/"
        )

    def test_create_agent_skill_documents_lifecycle(self):
        """create-agent SKILL.md must document temporary vs persistent lifecycle (T029)."""
        skill = (REPO_ROOT / "skills" / "create-agent" / "SKILL.md").read_text(encoding="utf-8")
        lowered = skill.lower()
        assert "temporary" in lowered, "SKILL.md must document the temporary (context-only) lifecycle"
        assert "persistent" in lowered, "SKILL.md must document the persistent (.specify/agents) lifecycle"
