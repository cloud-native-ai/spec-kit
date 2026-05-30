"""Structural contract test for the 012-skill-home-workdir iteration.

Asserts the structural requirements encoded in
.specify/specs/012-skill-home-workdir/contracts/skill-home-workdir-template.openapi.yaml
against the four in-scope documentation files (plus consistency checks on
CLAUDE.md and .specify/instructions.md).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


SKILL_HOME_IDIOM = (
    'SKILL_HOME="${SKILL_HOME:-$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." '
    '&& pwd -P)}"'
)
SKILL_WORKDIR_IDIOM = 'SKILL_WORKDIR="${SKILL_WORKDIR:-$(pwd -P)}"'

TEMPLATE_PATH = "templates/commands/skills.md"
CREATE_SKILLS_PATH = "skills/create-skills/SKILL.md"
IMPROVE_SKILLS_PATH = "skills/improve-skills/SKILL.md"
CREATE_SKILLS_MIRROR = ".specify/skills/create-skills/SKILL.md"
IMPROVE_SKILLS_MIRROR = ".specify/skills/improve-skills/SKILL.md"
CLAUDE_MD_PATH = "CLAUDE.md"
INSTRUCTIONS_MD_PATH = ".specify/instructions.md"

REQUIRED_TEMPLATE_SECTIONS = (
    "Path Conventions",
    "Computation Idioms",
    "Paired Example",
    "Migration Mapping",
    "Non-shell Agents",
    "Nested Invocations",
)

# Each row: (legacy_pattern_substring, new_pattern_substring) the migration
# mapping table in templates/commands/skills.md MUST contain. Covers FR-011 /
# SC-005 / data-model.md entity 3 cardinality (>=3 rows over the three idiom
# kinds: bare relative, SKILL_ROOT, agent-specific install).
REQUIRED_MIGRATION_ROWS = (
    ("./scripts", "${SKILL_HOME}/scripts"),
    ("${SKILL_ROOT}", "${SKILL_HOME}"),
    ("~/.copilot/skills", "${SKILL_HOME}"),
)


def _read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


@pytest.mark.contract
def test_placeholder_until_assertions_added():
    """Sentinel test so the file is discoverable before story-specific tests land."""
    assert SKILL_HOME_IDIOM.startswith('SKILL_HOME=')
    assert SKILL_WORKDIR_IDIOM.startswith('SKILL_WORKDIR=')


# ---------------------------------------------------------------------------
# US1 — ${SKILL_HOME} in templates/commands/skills.md and skills/create-skills/
# ---------------------------------------------------------------------------


@pytest.mark.contract
def test_us1_template_defines_skill_home():
    """TemplateAssertions.definesSkillHome — Path Conventions section names ${SKILL_HOME}."""
    body = _read(TEMPLATE_PATH)
    assert "${SKILL_HOME}" in body, (
        f"{TEMPLATE_PATH} must reference ${{SKILL_HOME}} as a first-class variable (FR-001)"
    )


@pytest.mark.contract
def test_us1_template_has_path_conventions_section():
    """TemplateAssertions.hasPathConventionsSection."""
    body = _read(TEMPLATE_PATH)
    assert re.search(r"^##\s+Path Conventions\s*$", body, re.MULTILINE), (
        f"{TEMPLATE_PATH} must contain a top-level '## Path Conventions' heading"
    )


@pytest.mark.contract
def test_us1_template_has_computation_idioms_section():
    """TemplateAssertions.hasComputationIdiomsSection — SKILL_HOME idiom substring present."""
    body = _read(TEMPLATE_PATH)
    assert re.search(r"^###\s+Computation Idioms\s*$", body, re.MULTILINE), (
        f"{TEMPLATE_PATH} must contain a '### Computation Idioms' subsection"
    )
    assert SKILL_HOME_IDIOM in body, (
        f"{TEMPLATE_PATH} must contain the FR-016 SKILL_HOME script idiom verbatim:\n  {SKILL_HOME_IDIOM}"
    )


@pytest.mark.contract
def test_us1_template_contains_normative_skill_home_fallback():
    """TemplateAssertions.containsNormativeScriptIdiom.skillHomeFallback."""
    body = _read(TEMPLATE_PATH)
    assert SKILL_HOME_IDIOM in body, (
        f"{TEMPLATE_PATH} must contain SKILL_HOME_IDIOM (FR-016 normative recipe)"
    )


@pytest.mark.contract
def test_us1_template_has_non_shell_agents_clause():
    """TemplateAssertions.hasNonShellAgentsClause (FR-013)."""
    body = _read(TEMPLATE_PATH)
    assert re.search(r"^###\s+Non-shell Agents\s*$", body, re.MULTILINE), (
        f"{TEMPLATE_PATH} must contain a '### Non-shell Agents' subsection"
    )


@pytest.mark.contract
def test_us1_template_has_nested_invocations_clause():
    """TemplateAssertions.hasNestedInvocationsClause (F2 remediation; resolves Nested Invocations edge case)."""
    body = _read(TEMPLATE_PATH)
    assert re.search(r"^###\s+Nested Invocations\s*$", body, re.MULTILINE), (
        f"{TEMPLATE_PATH} must contain a '### Nested Invocations' subsection"
    )
    # Both anchors must appear within ~10 lines of each other.
    lines = body.splitlines()
    unset_home_idx = next(
        (i for i, ln in enumerate(lines) if "unset SKILL_HOME" in ln), None
    )
    must_not_unset_idx = next(
        (i for i, ln in enumerate(lines) if "MUST NOT unset" in ln and "SKILL_WORKDIR" in ln),
        None,
    )
    assert unset_home_idx is not None, (
        f"{TEMPLATE_PATH} must instruct callers to 'unset SKILL_HOME' before nested calls"
    )
    assert must_not_unset_idx is not None, (
        f"{TEMPLATE_PATH} must state callers 'MUST NOT unset SKILL_WORKDIR' across nested calls"
    )
    assert abs(unset_home_idx - must_not_unset_idx) <= 10, (
        "The unset-SKILL_HOME and MUST-NOT-unset-SKILL_WORKDIR statements must appear "
        "within ~10 lines of each other (they are paired rules)."
    )


@pytest.mark.contract
def test_us1_create_skills_has_zero_skill_root_occurrences():
    """CreateSkillsAssertions.skillRootOccurrences == 0 (SC-006)."""
    body = _read(CREATE_SKILLS_PATH)
    assert "SKILL_ROOT" not in body, (
        f"{CREATE_SKILLS_PATH} must contain zero SKILL_ROOT references after rename to SKILL_HOME (SC-006)"
    )


@pytest.mark.contract
def test_us1_create_skills_uses_skill_home():
    """CreateSkillsAssertions.skillHomeOccurrences >= 1."""
    body = _read(CREATE_SKILLS_PATH)
    assert body.count("SKILL_HOME") >= 1, (
        f"{CREATE_SKILLS_PATH} must reference SKILL_HOME at least once (FR-008/FR-009)"
    )


@pytest.mark.contract
def test_us1_create_skills_has_skill_home_adoption_guidance():
    """CreateSkillsAssertions.hasSkillHomeAdoptionGuidance — new Skills told to use ${SKILL_HOME}/..."""
    body = _read(CREATE_SKILLS_PATH)
    assert re.search(r"\$\{SKILL_HOME\}/[A-Za-z<]", body), (
        f"{CREATE_SKILLS_PATH} must instruct new Skills to write Skill-owned resources as "
        "${SKILL_HOME}/<relative-path> (FR-009)"
    )


@pytest.mark.contract
def test_us1_create_skills_has_skill_workdir_adoption_guidance():
    """CreateSkillsAssertions.hasSkillWorkdirAdoptionGuidance — F1 remediation."""
    body = _read(CREATE_SKILLS_PATH)
    assert re.search(r"\$\{SKILL_WORKDIR\}/[A-Za-z<]", body), (
        f"{CREATE_SKILLS_PATH} must also instruct new Skills to write user-facing paths as "
        "${SKILL_WORKDIR}/<relative-path> (FR-009 full coverage, F1 remediation)"
    )


# ---------------------------------------------------------------------------
# US2 — ${SKILL_WORKDIR} and Paired Example
# ---------------------------------------------------------------------------


@pytest.mark.contract
def test_us2_template_defines_skill_workdir():
    """TemplateAssertions.definesSkillWorkdir."""
    body = _read(TEMPLATE_PATH)
    assert "${SKILL_WORKDIR}" in body, (
        f"{TEMPLATE_PATH} must reference ${{SKILL_WORKDIR}} as a first-class variable (FR-002)"
    )


@pytest.mark.contract
def test_us2_template_contains_normative_skill_workdir_fallback():
    """TemplateAssertions.containsNormativeScriptIdiom.skillWorkdirFallback."""
    body = _read(TEMPLATE_PATH)
    assert SKILL_WORKDIR_IDIOM in body, (
        f"{TEMPLATE_PATH} must contain the FR-016 SKILL_WORKDIR script idiom verbatim:\n  {SKILL_WORKDIR_IDIOM}"
    )


@pytest.mark.contract
def test_us2_template_has_paired_example():
    """TemplateAssertions.hasPairedExample (FR-006)."""
    body = _read(TEMPLATE_PATH)
    assert re.search(r"^###\s+Paired Example\s*$", body, re.MULTILINE), (
        f"{TEMPLATE_PATH} must contain a '### Paired Example' subsection"
    )
    # Locate the Paired Example fenced code block and verify it uses both vars.
    pe_match = re.search(
        r"^###\s+Paired Example\s*$(?P<body>.*?)(?=^##\s|^###\s|\Z)",
        body,
        re.MULTILINE | re.DOTALL,
    )
    assert pe_match, "Could not extract Paired Example section body"
    pe_body = pe_match.group("body")
    code_blocks = re.findall(r"```(?:bash|sh)?\n(.*?)```", pe_body, re.DOTALL)
    assert code_blocks, (
        "Paired Example section must contain at least one fenced bash code block"
    )
    combined = "\n".join(code_blocks)
    assert "${SKILL_HOME}/" in combined and "${SKILL_WORKDIR}/" in combined, (
        "Paired Example must use BOTH ${SKILL_HOME}/ and ${SKILL_WORKDIR}/ in the same snippet (FR-006)"
    )


# ---------------------------------------------------------------------------
# US3 — Migration Mapping + improve-skills legacy detection + mirror consistency
# ---------------------------------------------------------------------------


@pytest.mark.contract
def test_us3_template_has_migration_mapping_present():
    """TemplateAssertions.hasMigrationMapping.present."""
    body = _read(TEMPLATE_PATH)
    assert re.search(r"^##\s+Migration Mapping\s*$", body, re.MULTILINE), (
        f"{TEMPLATE_PATH} must contain a '## Migration Mapping' section (FR-011)"
    )


def _migration_table_rows() -> list[str]:
    """Return the body rows of the Migration Mapping markdown table."""
    body = _read(TEMPLATE_PATH)
    section = re.search(
        r"^##\s+Migration Mapping\s*$(?P<body>.*?)(?=^##\s|\Z)",
        body,
        re.MULTILINE | re.DOTALL,
    )
    assert section, "Migration Mapping section not found"
    # Markdown table rows look like "| col | col | col |" — drop header + separator.
    rows = [
        ln for ln in section.group("body").splitlines()
        if ln.strip().startswith("|") and not re.match(r"^\s*\|\s*-+", ln)
    ]
    # Drop the header (first remaining row).
    return rows[1:] if rows else []


@pytest.mark.contract
def test_us3_template_migration_mapping_has_at_least_three_rows():
    """TemplateAssertions.hasMigrationMapping.rowCount >= 3 (SC-005, data-model.md entity 3)."""
    rows = _migration_table_rows()
    assert len(rows) >= 3, (
        f"Migration Mapping table must contain at least 3 rows (got {len(rows)}); "
        "covers bare relative, SKILL_ROOT, and agent-specific install path idioms (FR-011)"
    )


@pytest.mark.contract
def test_us3_template_migration_mapping_covers_required_idioms():
    """TemplateAssertions.hasMigrationMapping.covers{BareRelative,SkillRoot,AgentSpecificPaths}."""
    table_text = "\n".join(_migration_table_rows())
    for legacy_anchor, new_anchor in REQUIRED_MIGRATION_ROWS:
        assert legacy_anchor in table_text, (
            f"Migration Mapping must include a row with legacy anchor `{legacy_anchor}`"
        )
        assert new_anchor in table_text, (
            f"Migration Mapping must include a row with new anchor `{new_anchor}`"
        )


@pytest.mark.contract
def test_us3_improve_skills_has_legacy_idiom_detection_clause():
    """ImproveSkillsAssertions.hasLegacyIdiomDetectionClause (FR-010)."""
    body = _read(IMPROVE_SKILLS_PATH)
    # Must reference all three legacy idioms as detection candidates.
    assert "./scripts" in body or "bare relative" in body.lower() or "./X" in body, (
        f"{IMPROVE_SKILLS_PATH} must list bare relative paths as a legacy idiom (FR-010)"
    )
    assert "${SKILL_ROOT}" in body or "SKILL_ROOT" in body, (
        f"{IMPROVE_SKILLS_PATH} must list ${{SKILL_ROOT}} references as a legacy idiom (FR-010)"
    )
    assert ".copilot/skills" in body or "agent-specific install" in body.lower(), (
        f"{IMPROVE_SKILLS_PATH} must list agent-specific install paths as a legacy idiom (FR-010)"
    )


@pytest.mark.contract
def test_us3_mirror_create_skills_in_sync():
    """MirrorConsistency.createSkillsInSync — byte-equality."""
    canonical = _read(CREATE_SKILLS_PATH)
    mirror = _read(CREATE_SKILLS_MIRROR)
    assert canonical == mirror, (
        f"{CREATE_SKILLS_MIRROR} must be byte-equivalent to {CREATE_SKILLS_PATH}"
    )


@pytest.mark.contract
def test_us3_mirror_improve_skills_in_sync():
    """MirrorConsistency.improveSkillsInSync — byte-equality."""
    canonical = _read(IMPROVE_SKILLS_PATH)
    mirror = _read(IMPROVE_SKILLS_MIRROR)
    assert canonical == mirror, (
        f"{IMPROVE_SKILLS_MIRROR} must be byte-equivalent to {IMPROVE_SKILLS_PATH}"
    )


# ---------------------------------------------------------------------------
# Polish — Residual SKILL_ROOT consistency check (FR-015)
# ---------------------------------------------------------------------------


@pytest.mark.contract
def test_polish_claude_md_has_zero_skill_root_references():
    """ResidualSkillRootCheck.claudeMdReferences == 0 (FR-015)."""
    body = _read(CLAUDE_MD_PATH)
    assert "SKILL_ROOT" not in body, (
        f"{CLAUDE_MD_PATH} must contain zero SKILL_ROOT references (FR-015)"
    )


@pytest.mark.contract
def test_polish_instructions_md_has_zero_skill_root_references():
    """ResidualSkillRootCheck.instructionsMdReferences == 0 (FR-015)."""
    body = _read(INSTRUCTIONS_MD_PATH)
    assert "SKILL_ROOT" not in body, (
        f"{INSTRUCTIONS_MD_PATH} must contain zero SKILL_ROOT references (FR-015)"
    )
