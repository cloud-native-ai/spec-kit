"""Contract tests for create-skills prompt assets.

Covers:
- Frontmatter existence and shape for skills/create-skills/SKILL.md
- Routing language in templates/commands/skills.md
- Duplication boundaries between command template and Skill
- Packaging assertion for pyproject.toml
"""
from pathlib import Path
import re

import yaml


ROOT = Path(__file__).resolve().parents[2]

SKILL_FILE = ROOT / "skills" / "create-skills" / "SKILL.md"
SKILL_WORKSPACE_FILE = ROOT / ".specify" / "skills" / "create-skills" / "SKILL.md"
SKILL_REF_FILE = ROOT / "skills" / "create-skills" / "references" / "skill-creation-quality-checklist.md"
ROOT = Path(__file__).resolve().parents[2]

SKILL_FILE = ROOT / "skills" / "create-skills" / "SKILL.md"
SKILL_WORKSPACE_FILE = ROOT / ".specify" / "skills" / "create-skills" / "SKILL.md"
SKILL_REF_FILE = ROOT / "skills" / "create-skills" / "references" / "skill-creation-quality-checklist.md"
SKILL_REF_WORKSPACE_FILE = (
    ROOT / ".specify" / "skills" / "create-skills" / "references" / "skill-creation-quality-checklist.md"
)
COMMAND_FILE = ROOT / "templates" / "commands" / "skills.md"
PYPROJECT_FILE = ROOT / "pyproject.toml"


def _read_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1]) or {}


def _text_of(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Frontmatter and required-section assertions (T006)
# ---------------------------------------------------------------------------

def test_create_skills_skill_file_exists():
    """skills/create-skills/SKILL.md exists."""
    assert SKILL_FILE.exists(), f"Expected {SKILL_FILE} to exist"


def test_create_skills_has_valid_frontmatter():
    """Frontmatter is valid YAML and contains required fields."""
    fm = _read_frontmatter(SKILL_FILE)
    assert fm, "Expected non-empty YAML frontmatter"
    assert "name" in fm, "Expected 'name' in frontmatter"
    assert fm["name"] == "create-skills", f"Expected name='create-skills', got {fm.get('name')}"
    assert "description" in fm, "Expected 'description' in frontmatter"
    desc = fm["description"]
    assert "create" in desc.lower() or "skill" in desc.lower(), (
        f"Expected description to mention skill creation, got: {desc}"
    )


def test_create_skills_has_required_sections():
    """Contains core creation workflow sections."""
    text = _text_of(SKILL_FILE)
    required = [
        "Goal",
        "Workflow",
        "input",
        "conversation",
        "SKILL.md",
        "frontmatter",
    ]
    for needle in required:
        assert needle.lower() in text.lower(), f"Expected section referencing '{needle}'"


# ---------------------------------------------------------------------------
# Routing language assertions (T007)
# ---------------------------------------------------------------------------

def test_command_routes_missing_to_create_skills():
    """templates/commands/skills.md explicitly routes missing targets to create-skills."""
    text = _text_of(COMMAND_FILE)
    assert "create-skills" in text, "Expected 'create-skills' reference in command template"


def test_command_routes_existing_to_improve_skills():
    """templates/commands/skills.md explicitly routes existing targets to improve-skills."""
    text = _text_of(COMMAND_FILE)
    assert "improve-skills" in text, "Expected 'improve-skills' reference in command template"


# ---------------------------------------------------------------------------
# Duplication-boundary assertions (T008)
# ---------------------------------------------------------------------------

def test_command_does_not_contain_full_creation_methodology():
    """templates/commands/skills.md should not duplicate the full creation playbook."""
    text = _text_of(COMMAND_FILE)
    # The command may still reference create-skills by name, but should not
    # inline the full creation workflow that now lives in the Skill.
    creation_only = [
        "Design Principles",
        "Execution Steps",
        "Slash Behavior Notes",
        "Continuous Improvement",
        "### Input Classification & Processing Strategy",
    ]
    for term in creation_only:
        assert term not in text, (
            f"Command template still contains creation-only section '{term}'"
        )


def test_skill_does_not_contain_command_routing_logic():
    """skills/create-skills/SKILL.md should not embed /speckit.skills routing."""
    text = _text_of(SKILL_FILE)
    routing_terms = ["/speckit.skills", "templates/commands/skills.md"]
    for term in routing_terms:
        occurrences = text.count(term)
        # Allow one contextual mention (relationship note) but not full routing
        assert occurrences <= 1, (
            f"Skill body contains '{term}' {occurrences} times; expected 0 or 1 contextual mentions"
        )


# ---------------------------------------------------------------------------
# Packaging assertion (T009)
# ---------------------------------------------------------------------------

def test_pyproject_toml_force_includes_skills():
    """pyproject.toml force-include still covers the root skills/ directory."""
    text = _text_of(PYPROJECT_FILE)
    assert '"skills" = "specify_cli/skills"' in text, (
        "Expected pyproject.toml to force-include skills/"
    )


# ---------------------------------------------------------------------------
# Progressive disclosure, registries, anti-patterns (T026-T028) - placeholder
# ---------------------------------------------------------------------------

def test_create_skills_references_directory_exists():
    """skills/create-skills/references/ exists when quality checklist is present."""
    if SKILL_REF_FILE.exists():
        assert SKILL_REF_FILE.parent.is_dir()


def test_create_skills_instructs_registry_update():
    """Skill mentions .specify/instructions.md for registry persistence."""
    text = _text_of(SKILL_FILE)
    registry_terms = [".specify/instructions.md", "registry", "Resource ID", "skill_id"]
    found = sum(1 for t in registry_terms if t.lower() in text.lower())
    assert found >= 2, f"Expected at least 2 registry-related terms in Skill body, found {found}"


def test_create_skills_mentions_quality_anti_patterns():
    """Skill warns against known anti-patterns."""
    text = _text_of(SKILL_FILE)
    anti_pattern_terms = [
        "vague description",
        "invalid",
        "oversized",
        "missing executable",
        "inconsistent",
    ]
    found = sum(1 for t in anti_pattern_terms if t.lower() in text.lower())
    assert found >= 2, (
        f"Expected at least 2 anti-pattern terms in Skill body, found {found}"
    )


# ---------------------------------------------------------------------------
# Explicit-input and conversation-history creation guidance (T012)
# ---------------------------------------------------------------------------

def test_create_skills_covers_explicit_input():
    """Skill describes creation from explicit user-provided input."""
    text = _text_of(SKILL_FILE)
    markers = ["explicit", "$ARGUMENTS", "user input", "user provided"]
    found = sum(1 for m in markers if m.lower() in text.lower())
    assert found >= 1, "Expected explicit-input creation guidance in Skill"


def test_create_skills_covers_conversation_history():
    """Skill describes creation from conversation history distillation."""
    text = _text_of(SKILL_FILE)
    markers = ["conversation", "distill", "empty", "history"]
    found = sum(1 for m in markers if m.lower() in text.lower())
    assert found >= 1, "Expected conversation-history creation guidance in Skill"


# ---------------------------------------------------------------------------
# Resource path and progressive-disclosure assertions (T026)
# ---------------------------------------------------------------------------

def test_create_skills_uses_relative_resource_paths():
    """Skill references resources with relative paths (./ prefix)."""
    text = _text_of(SKILL_FILE)
    rel_patterns = ["./references/", "./scripts/", "./assets/"]
    found = sum(1 for p in rel_patterns if p in text)
    assert found >= 1, f"Expected at least one relative resource path in Skill, found {found}"


def test_create_skills_instructs_progressive_disclosure():
    """Skill body mentions splitting large details into resource directories."""
    text = _text_of(SKILL_FILE)
    markers = ["progressive", "references/", "resource", "split", "size"]
    found = sum(1 for m in markers if m.lower() in text.lower())
    assert found >= 2, f"Expected progressive-disclosure guidance, found {found}"


# ---------------------------------------------------------------------------
# Mirror / workspace copy assertions
# ---------------------------------------------------------------------------

def test_workspace_skill_mirrors_source():
    """The .specify/skills/create-skills/SKILL.md mirrors skills/create-skills/SKILL.md."""
    if SKILL_WORKSPACE_FILE.exists():
        assert SKILL_WORKSPACE_FILE.read_text(encoding="utf-8") == SKILL_FILE.read_text(
            encoding="utf-8"
        ), "Workspace mirror differs from source Skill"
PYPROJECT_FILE = ROOT / "pyproject.toml"