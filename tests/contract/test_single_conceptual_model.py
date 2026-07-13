"""Contract test: the multi-agent Conceptual Model is defined exactly once (SC-006).

Enforces migration contract M2:
  - The Conceptual Model lives in `skills/create-team/references/conceptual-model.md`
    (the team domain, single source of truth).
  - It is NOT embedded in `skills/create-agent/SKILL.md` — that skill may only carry
    a one-line pointer to the team-domain reference, never a re-definition.
"""

import re
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CONCEPTUAL_MODEL = REPO_ROOT / "skills" / "create-team" / "references" / "conceptual-model.md"
CREATE_AGENT = REPO_ROOT / "skills" / "create-agent" / "SKILL.md"


@pytest.mark.contract
class TestSingleConceptualModel:
    def test_model_defined_in_team_domain(self):
        assert CONCEPTUAL_MODEL.exists(), (
            "the Conceptual Model must live in skills/create-team/references/conceptual-model.md"
        )
        content = CONCEPTUAL_MODEL.read_text(encoding="utf-8")
        assert "Role" in content and "Stage" in content and "Type" in content, (
            "conceptual-model.md must define the Role × Stage × Type model"
        )

    def test_model_not_embedded_in_create_agent(self):
        content = CREATE_AGENT.read_text(encoding="utf-8")
        # No '## Conceptual Model ...' section heading may remain in create-agent.
        assert not re.search(r"^##\s+Conceptual Model", content, flags=re.MULTILINE), (
            "create-agent/SKILL.md must not embed a '## Conceptual Model' section; "
            "it may only point to the team-domain reference"
        )

    def test_create_agent_points_to_reference(self):
        content = CREATE_AGENT.read_text(encoding="utf-8")
        assert "create-team/references/conceptual-model.md" in content, (
            "create-agent/SKILL.md must point to the team-domain Conceptual Model reference"
        )
