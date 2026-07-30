"""Contract test: `/speckit.tools` single-entry routing + the tool-domain skill pair.

Mirrors the team-domain contract (`test_team_command_routing.py`) for the tools
domain:
  - `templates/commands/tools.md` is the single entry point and exposes exactly
    the five modes define / modify / view / list / invoke.
  - define routes to `create-tools`, modify routes to `improve-tools`, and the
    command delegates rather than rendering templates inline.
  - invoke is gated by preview -> confirm -> execute.
  - both skills exist with correct identity, and the authoring templates live
    inside `create-tools` (not at the top-level `templates/`).
  - `skills/` and `.specify/skills/` copies stay in sync for both skills.
"""

import re
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLS_CMD = REPO_ROOT / "templates" / "commands" / "tools.md"
CREATE_TOOLS = REPO_ROOT / "skills" / "create-tools" / "SKILL.md"
IMPROVE_TOOLS = REPO_ROOT / "skills" / "improve-tools" / "SKILL.md"
TOOL_TEMPLATE_DIR = REPO_ROOT / "skills" / "create-tools" / "templates"
TOOL_TEMPLATES = (
    "tool-project-script-template.md",
    "tool-system-binary-template.md",
    "tool-shell-function-template.md",
    "tool-webhook-template.md",
)
MODES = ("define", "modify", "view", "list", "invoke")


@pytest.mark.contract
class TestToolsCommandRouting:
    def test_tools_command_exists(self):
        assert TOOLS_CMD.exists(), "templates/commands/tools.md must exist (source of /speckit.tools)"

    def test_tools_command_is_single_entry_point(self):
        content = TOOLS_CMD.read_text(encoding="utf-8").lower()
        assert "single entry point" in content, (
            "tools.md must declare itself the single entry point for tool operations"
        )
        assert "does **not** render templates inline" in content or "not render templates inline" in content, (
            "tools.md must delegate to skills rather than rendering templates inline"
        )

    def test_tools_command_exposes_five_modes(self):
        content = TOOLS_CMD.read_text(encoding="utf-8").lower()
        for mode in MODES:
            assert mode in content, f"tools.md must document the '{mode}' mode"

    def test_tools_command_routes_to_tool_skills(self):
        content = TOOLS_CMD.read_text(encoding="utf-8")
        assert "create-tools" in content, "tools.md must route define to create-tools"
        assert "improve-tools" in content, "tools.md must route modify to improve-tools"

    def test_tools_command_has_invoke_confirmation_gate(self):
        content = TOOLS_CMD.read_text(encoding="utf-8")
        assert "Proceed with execution? (yes/no)" in content, (
            "tools.md invoke mode must use the canonical confirmation prompt"
        )
        assert re.search(r"preview\s*→\s*confirm\s*→\s*execute", content, flags=re.IGNORECASE), (
            "tools.md invoke mode must document the preview → confirm → execute gate"
        )

    def test_tools_command_documents_default_and_ambiguous_behavior(self):
        content = TOOLS_CMD.read_text(encoding="utf-8")
        assert "Default Behavior (No Arguments)" in content, (
            "tools.md must define the no-arguments default behavior"
        )
        assert "Ambiguous or Unsupported Intent" in content, (
            "tools.md must define the ambiguous/unsupported intent branch"
        )

    def test_other_domain_commands_do_not_route_tool_ops(self):
        for stem in ("agents", "team", "skills"):
            content = (REPO_ROOT / "templates" / "commands" / f"{stem}.md").read_text(encoding="utf-8")
            assert "create-tools" not in content and "improve-tools" not in content, (
                f"{stem}.md must not route tool-domain operations (that is /speckit.tools)"
            )


@pytest.mark.contract
class TestToolSkillPairPresence:
    @pytest.mark.parametrize(
        "skill_path,slug",
        [(CREATE_TOOLS, "create-tools"), (IMPROVE_TOOLS, "improve-tools")],
    )
    def test_skill_exists_with_correct_identity(self, skill_path, slug):
        assert skill_path.exists(), f"skills/{slug}/SKILL.md must exist"
        content = skill_path.read_text(encoding="utf-8")
        assert f"name: {slug}" in content, f"{slug} frontmatter must declare name: {slug}"
        assert f'skill_id: "<SKILL:.specify/skills/{slug}/SKILL.md>"' in content, (
            f"{slug} must declare the canonical skill_id"
        )

    @pytest.mark.parametrize(
        "skill_path,slug",
        [(CREATE_TOOLS, "create-tools"), (IMPROVE_TOOLS, "improve-tools")],
    )
    def test_skill_mirror_in_sync(self, skill_path, slug):
        mirror = REPO_ROOT / ".specify" / "skills" / slug / "SKILL.md"
        assert mirror.exists(), f".specify/skills/{slug}/SKILL.md mirror must exist"
        assert mirror.read_text(encoding="utf-8") == skill_path.read_text(encoding="utf-8"), (
            f"skills/{slug}/ and .specify/skills/{slug}/ must stay byte-identical"
        )


@pytest.mark.contract
class TestToolConceptDefinition:
    """The Tool concept — what it is and why it exists — is defined once, canonically."""

    def test_definition_file_states_what_a_tool_is(self):
        content = (REPO_ROOT / "shared" / "definitions" / "tool-definitions.md").read_text(encoding="utf-8")
        assert "## What a Tool Is" in content, (
            "tool-definitions.md must define the Tool concept, not only its schema"
        )

    def test_definition_file_states_both_rationales(self):
        content = (REPO_ROOT / "shared" / "definitions" / "tool-definitions.md").read_text(encoding="utf-8").lower()
        # Rationale 1: absorbing environment variance.
        for token in ("environment variance", "version", "architecture"):
            assert token in content, f"tool-definitions.md must explain environment variance ({token})"
        # Rationale 2: replacing throwaway LLM-generated scripts.
        assert "throwaway" in content or "ad-hoc script" in content, (
            "tool-definitions.md must explain that Tools replace throwaway generated scripts"
        )
        assert "inference overhead" in content, (
            "tool-definitions.md must state the efficiency rationale (inference overhead)"
        )

    def test_definition_file_disambiguates_terminology(self):
        content = (REPO_ROOT / "shared" / "definitions" / "tool-definitions.md").read_text(encoding="utf-8")
        assert "three different things called" in content.lower(), (
            "tool-definitions.md must disambiguate Tool record vs AI agent CLI vs tool-call list"
        )

    def test_definition_file_documents_environment_applicability(self):
        content = (REPO_ROOT / "shared" / "definitions" / "tool-definitions.md").read_text(encoding="utf-8")
        assert "## Environment Applicability" in content
        for label in ("Verified Version", "Version Differences", "Platform", "Architecture", "Fallback", "Preflight Check"):
            assert label in content, f"Environment Applicability must document the '{label}' field"

    @pytest.mark.parametrize("root", ["shared", ".specify/shared"])
    def test_reuse_gate_convention_exists(self, root):
        gate = REPO_ROOT / root / "workflow" / "tool-reuse-gate.md"
        assert gate.exists(), f"{root}/workflow/tool-reuse-gate.md must exist"
        content = gate.read_text(encoding="utf-8")
        assert "Reuse when found" in content or "reuse it" in content.lower()
        assert "Draft" in content, "the gate must state that a Draft record does not satisfy it"

    def test_constitution_codifies_tool_reuse(self):
        content = (REPO_ROOT / ".specify" / "memory" / "constitution.md").read_text(encoding="utf-8")
        assert "### XII. Tool Reuse Over Ad-Hoc Generation" in content, (
            "the constitution must codify the tool-reuse discipline as a principle"
        )

    @pytest.mark.parametrize("template", TOOL_TEMPLATES)
    def test_templates_carry_environment_applicability(self, template):
        content = (TOOL_TEMPLATE_DIR / template).read_text(encoding="utf-8")
        assert "## Environment Applicability" in content, (
            f"{template} must let a record express environment variance"
        )

    def test_engine_round_trips_environment_fields(self, tmp_path):
        from tests.script_api import tools_utils as mod

        record = mod.ToolRecord(
            name="probe",
            tool_type="system-binary",
            source_identifier="/usr/bin/probe",
            description="probe",
            environment=mod.EnvironmentApplicability(
                verified_version="1.2.3",
                version_differences="flag renamed in 2.x",
                platform="linux",
                architecture="x86_64",
                fallback="use probe-legacy",
                preflight_check="probe --version",
            ),
        )
        mod.save_record(tmp_path, record)
        loaded = mod.load_record(tmp_path, "probe")
        assert loaded.environment == record.environment, (
            "environment applicability must survive a save/load round-trip"
        )

    def test_empty_environment_omits_section(self, tmp_path):
        from tests.script_api import tools_utils as mod

        mod.save_record(
            tmp_path,
            mod.ToolRecord(
                name="plain",
                tool_type="system-binary",
                source_identifier="/usr/bin/plain",
                description="plain",
            ),
        )
        content = (tmp_path / "plain.md").read_text(encoding="utf-8")
        assert "## Environment Applicability" not in content, (
            "a record with no known variance must not emit an empty environment section"
        )


@pytest.mark.contract
class TestToolTemplatesLiveInsideSkill:
    @pytest.mark.parametrize("template", TOOL_TEMPLATES)
    def test_template_moved_into_create_tools(self, template):
        assert (TOOL_TEMPLATE_DIR / template).exists(), (
            f"{template} must live in skills/create-tools/templates/"
        )

    @pytest.mark.parametrize("template", TOOL_TEMPLATES)
    def test_template_no_longer_at_top_level(self, template):
        assert not (REPO_ROOT / "templates" / template).exists(), (
            f"{template} must no longer live at the top-level templates/ directory"
        )

    @pytest.mark.parametrize("template", TOOL_TEMPLATES)
    def test_template_registered_as_obsolete_top_level_asset(self, template):
        src = (REPO_ROOT / "src" / "specify_cli" / "__init__.py").read_text(encoding="utf-8")
        assert f'"{template}"' in src, (
            f"{template} must be listed in _OBSOLETE_TEMPLATES so stale installs are cleaned up"
        )

    def test_create_tools_skill_references_its_own_templates(self):
        content = CREATE_TOOLS.read_text(encoding="utf-8")
        assert "${SKILL_HOME}/templates/" in content, (
            "create-tools must reference its templates via the ${SKILL_HOME} idiom"
        )

    def test_record_creation_script_resolves_skill_templates(self):
        script = (REPO_ROOT / "scripts" / "bash" / "create-new-tools.sh").read_text(encoding="utf-8")
        assert ".specify/skills/create-tools/templates/" in script, (
            "create-new-tools.sh must resolve templates from the create-tools skill"
        )
        assert "tool-webhook-template.md" in script, (
            "create-new-tools.sh must support the webhook tool type"
        )
