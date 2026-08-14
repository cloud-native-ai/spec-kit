"""Contract test: the shipped ``agents/`` resource carries the Meta Agent preset set (Feature 044).

``specify init`` copies the shipped ``agents/`` resource into ``.specify/agents/templates/``
(the Agent Template layer) and then pre-links each ``*.agent.md`` per file into every
supported tool directory. For that to work on a fresh install, the seven preset role agents
must exist in the shipped resource (not only in this repo's dogfooded
``.specify/agents/templates/``).
"""

import pytest
from pathlib import Path

SHIPPED_AGENTS_DIR = Path(__file__).resolve().parents[2] / "agents"

PRESET_ROLES = [
    "structure-adjuster",
    "skill-verifier",
]


@pytest.mark.contract
class TestShippedAgentPresets:
    @pytest.mark.parametrize("slug", PRESET_ROLES)
    def test_preset_shipped(self, slug):
        path = SHIPPED_AGENTS_DIR / f"{slug}.agent.md"
        assert path.exists(), f"shipped preset agent missing: {path}"

    @pytest.mark.parametrize("slug", PRESET_ROLES)
    def test_preset_has_neutral_frontmatter(self, slug):
        path = SHIPPED_AGENTS_DIR / f"{slug}.agent.md"
        content = path.read_text(encoding="utf-8")
        parts = content.split("---", 2)
        assert len(parts) >= 3, f"{slug}: malformed frontmatter"
        frontmatter = parts[1]
        for field in (
            "name:",
            "description:",
            "model-tier:",
            "capability-tools:",
            "run-turn-budget:",
        ):
            assert field in frontmatter, f"{slug}: shipped preset missing frontmatter '{field}'"

    def test_no_shared_files_shipped(self):
        """The removed shared files must not reappear in the shipped resource."""
        for removed in ("AGENTS.md", "MEMORY.md", "SOUL.md", "USER.md"):
            assert not (SHIPPED_AGENTS_DIR / removed).exists(), (
                f"{removed} should not be shipped in agents/"
            )
