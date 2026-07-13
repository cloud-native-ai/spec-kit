"""Contract test: the seven shipped role agents are skill-enabled.

Enforces the Agent Skill Enablement contract
(``.specify/specs/025-agent-skill-enablement/contracts/agent-skill-enablement-contract.md``).

Assertions are grouped by contract clause / user story:
  US1 (C-5 T-1, T-2, T-5): each agent declares a non-empty ``skills:`` list and has a
      ``## Skill Enablement`` heading.
  US2 (C-5 T-3, T-4 / C-4): every declared slug resolves to an installed skill and no
      slug is a member of the non-declarable set.
  US3 (C-3): each ``agent-role-*-template.md`` mirrors the same additions.
"""

import re
import pytest
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SHIPPED_AGENTS_DIR = REPO_ROOT / "agents"
SKILLS_DIR = REPO_ROOT / "skills"
ROLE_TEMPLATES_DIR = REPO_ROOT / "skills" / "create-agent" / "templates"

PRESET_ROLES = [
    "requirements-analyst",
    "ux-analyst",
    "system-designer",
    "module-designer",
    "test-engineer",
    "qa-engineer",
    "knowledge-manager",
]

# Skills that MUST NOT be declared by any role agent (reference-only + meta), per C-1/C-4.
NON_DECLARABLE = {
    "sdd-workflow",
    "create-agent",
    "improve-agent",
    "create-skills",
    "improve-skills",
    "create-team",
    "improve-team",
}


def _split_frontmatter(content):
    """Return (frontmatter_dict, body_str) for a Markdown file with YAML frontmatter."""
    parts = content.split("---", 2)
    assert len(parts) >= 3, "malformed frontmatter (expected leading '---' fenced block)"
    frontmatter = yaml.safe_load(parts[1]) or {}
    body = parts[2]
    return frontmatter, body


def _agent_content(slug):
    path = SHIPPED_AGENTS_DIR / f"{slug}.agent.md"
    assert path.exists(), f"shipped preset agent missing: {path}"
    return path.read_text(encoding="utf-8")


def _installed_skill_slugs():
    return {p.parent.name for p in SKILLS_DIR.glob("*/SKILL.md")}


@pytest.mark.contract
class TestAgentSkillEnablement:
    # ---- US1: agents declare and prefer role-relevant skills (C-5 T-1, T-2, T-5) ----

    @pytest.mark.parametrize("slug", PRESET_ROLES)
    def test_frontmatter_has_skills_key(self, slug):
        """T-1: frontmatter contains a ``skills:`` key."""
        frontmatter, _ = _split_frontmatter(_agent_content(slug))
        assert "skills" in frontmatter, f"{slug}: frontmatter missing 'skills:' key"

    @pytest.mark.parametrize("slug", PRESET_ROLES)
    def test_skills_list_non_empty(self, slug):
        """T-2: the parsed ``skills`` value is a non-empty list of strings."""
        frontmatter, _ = _split_frontmatter(_agent_content(slug))
        skills = frontmatter.get("skills")
        assert isinstance(skills, list) and len(skills) >= 1, (
            f"{slug}: 'skills' must be a non-empty list, got {skills!r}"
        )
        assert all(isinstance(s, str) and s for s in skills), (
            f"{slug}: every skill slug must be a non-empty string"
        )

    @pytest.mark.parametrize("slug", PRESET_ROLES)
    def test_has_skill_enablement_section(self, slug):
        """T-5: the agent body contains exactly one ``## Skill Enablement`` heading."""
        _, body = _split_frontmatter(_agent_content(slug))
        headings = re.findall(r"^##\s+Skill Enablement\s*$", body, flags=re.MULTILINE)
        assert len(headings) == 1, (
            f"{slug}: expected exactly one '## Skill Enablement' heading, found {len(headings)}"
        )

    # ---- US2: declared skills are guaranteed invocable (C-5 T-3, T-4 / C-4) ----

    @pytest.mark.parametrize("slug", PRESET_ROLES)
    def test_declared_skills_resolve_to_installed(self, slug):
        """T-3: every declared slug resolves to an installed ``skills/<slug>/SKILL.md``."""
        frontmatter, _ = _split_frontmatter(_agent_content(slug))
        installed = _installed_skill_slugs()
        for skill in frontmatter.get("skills", []):
            assert skill in installed, (
                f"{slug}: declared skill '{skill}' has no installed skills/{skill}/SKILL.md "
                f"(dangling reference)"
            )

    @pytest.mark.parametrize("slug", PRESET_ROLES)
    def test_no_non_declarable_skill(self, slug):
        """T-4: no declared slug is a member of the non-declarable (reference-only/meta) set."""
        frontmatter, _ = _split_frontmatter(_agent_content(slug))
        offending = NON_DECLARABLE.intersection(frontmatter.get("skills", []))
        assert not offending, (
            f"{slug}: declares non-declarable skill(s) {sorted(offending)} "
            f"(reference-only or meta skills must not appear in a role agent's skills list)"
        )

    def test_union_is_subset_of_declarable_installed(self):
        """C-4: the union of all declared skills is a subset of installed-minus-non-declarable."""
        declarable = _installed_skill_slugs() - NON_DECLARABLE
        union = set()
        for slug in PRESET_ROLES:
            frontmatter, _ = _split_frontmatter(_agent_content(slug))
            union.update(frontmatter.get("skills", []))
        assert union, "no skills declared across any agent"
        assert union.issubset(declarable), (
            f"declared skills not in the declarable installed set: {sorted(union - declarable)}"
        )

    # ---- US3: generator templates mirror the additions (C-3 parity) ----

    @pytest.mark.parametrize("slug", PRESET_ROLES)
    def test_role_template_has_skills_and_section(self, slug):
        """C-3: each ``agent-role-<slug>-template.md`` declares a ``skills:`` list and a
        ``## Skill Enablement`` section, so a regenerated agent inherits skill enablement.

        Uses string checks (not YAML parse) because template frontmatter contains
        ``{{PLACEHOLDER}}`` tokens that are not valid YAML.
        """
        path = ROLE_TEMPLATES_DIR / f"agent-role-{slug}-template.md"
        assert path.exists(), f"role template missing: {path}"
        parts = path.read_text(encoding="utf-8").split("---", 2)
        assert len(parts) >= 3, f"{slug} template: malformed frontmatter"
        frontmatter, body = parts[1], parts[2]
        assert re.search(r"^skills:\s*\[", frontmatter, flags=re.MULTILINE), (
            f"{slug} template: frontmatter missing 'skills:' list"
        )
        assert re.search(r"^##\s+Skill Enablement\s*$", body, flags=re.MULTILINE), (
            f"{slug} template: body missing '## Skill Enablement' heading"
        )
