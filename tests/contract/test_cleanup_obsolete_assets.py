"""Contract tests: init-time cleanup of obsolete framework structure.

When a workspace is re-initialised with a newer framework version, the additive
``copytree(dirs_exist_ok=True)`` copy never deletes skills, commands, or templates
that were renamed/removed in earlier versions. ``cleanup_obsolete_framework_assets``
prunes ONLY the enumerated, framework-owned artifacts and must never touch
user-authored content or current framework assets.
"""

from pathlib import Path

import pytest

from specify_cli import (
    _OBSOLETE_COMMANDS,
    _OBSOLETE_SKILL_FILES,
    _OBSOLETE_SKILLS,
    _OBSOLETE_TEMPLATES,
    cleanup_obsolete_framework_assets,
)


def _write(path: Path, content: str = "x\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _build_workspace(root: Path) -> None:
    """Seed a workspace mixing obsolete, current, and user-authored artifacts."""
    specify = root / ".specify"

    # Obsolete skills (must be removed)
    _write(specify / "skills" / "sdd-workflow" / "SKILL.md")
    _write(specify / "skills" / "organize-agents" / "SKILL.md")
    _write(specify / "skills" / "docx-utils" / "SKILL.md")
    _write(specify / "skills" / "extension-e2e-test" / "SKILL.md")
    _write(specify / "skills" / "agent-cli-setup" / "SKILL.md")
    # Current skill + user-authored skill (must survive)
    _write(specify / "skills" / "create-team" / "SKILL.md")
    _write(specify / "skills" / "my-custom-skill" / "SKILL.md")

    # Obsolete top-level templates (must be removed)
    _write(specify / "templates" / "agent-explore-template.md")
    _write(specify / "templates" / "consitution-template.md")
    _write(specify / "templates" / "mcptool-template.md")
    # Current template + user template (must survive)
    _write(specify / "templates" / "plan-template.md")
    _write(specify / "templates" / "my-team-template.md")

    # Obsolete commands in the active agent's dir (qoder → .qoder/commands, ext md)
    _write(root / ".qoder" / "commands" / "speckit.specify.md")
    _write(root / ".qoder" / "commands" / "speckit.mcpcall.md")
    _write(root / ".qoder" / "commands" / "speckit.taskstoissues.md")
    _write(root / ".qoder" / "commands" / "speckit.converge.md")
    # Current command + user command (must survive)
    _write(root / ".qoder" / "commands" / "speckit.requirements.md")
    _write(root / ".qoder" / "commands" / "my-custom.md")

    # Obsolete fallback command template (must be removed)
    _write(specify / "templates" / "commands" / "specify.md")
    _write(specify / "templates" / "commands" / "requirements.md")

    # Files a skill no longer owns — the Hugo layer moved create-docs → create-pages
    # (must be removed, leaving no empty scripts/references/assets dirs behind)
    _write(specify / "skills" / "create-docs" / "scripts" / "scaffold-hugo.py")
    _write(specify / "skills" / "create-docs" / "references" / "hugo-site.md")
    _write(specify / "skills" / "create-docs" / "assets" / "hugo" / "hugo.toml.tmpl")
    _write(specify / "skills" / "create-docs" / "assets" / "hugo" / "static" / "css" / "site.css")
    # The skill itself and anything the user added to it (must survive)
    _write(specify / "skills" / "create-docs" / "SKILL.md")
    _write(specify / "skills" / "create-docs" / "references" / "my-notes.md")

    # Retired create-team team presets — consolidated into capability-arena +
    # project-cluster (must be removed; the two new presets must survive)
    _write(specify / "skills" / "create-team" / "templates" / "teams" / "skills-arena.md")
    _write(specify / "skills" / "create-team" / "templates" / "teams" / "workspace-cluster.md")
    _write(specify / "skills" / "create-team" / "templates" / "teams" / "artifact-optimizer.md")
    _write(specify / "skills" / "create-team" / "templates" / "teams" / "process-monitor.md")
    _write(specify / "skills" / "create-team" / "templates" / "teams" / "capability-arena.md")
    _write(specify / "skills" / "create-team" / "templates" / "teams" / "project-cluster.md")


@pytest.mark.contract
def test_removes_obsolete_skills_commands_and_templates(tmp_path):
    _build_workspace(tmp_path)

    removed = cleanup_obsolete_framework_assets(tmp_path, "qoder")

    specify = tmp_path / ".specify"

    # Obsolete skills gone
    assert not (specify / "skills" / "sdd-workflow").exists()
    assert not (specify / "skills" / "organize-agents").exists()
    assert not (specify / "skills" / "docx-utils").exists()
    assert not (specify / "skills" / "extension-e2e-test").exists()
    assert not (specify / "skills" / "agent-cli-setup").exists()
    # Obsolete templates gone
    assert not (specify / "templates" / "agent-explore-template.md").exists()
    assert not (specify / "templates" / "consitution-template.md").exists()
    assert not (specify / "templates" / "mcptool-template.md").exists()
    # Obsolete commands gone (agent dir + fallback template)
    assert not (tmp_path / ".qoder" / "commands" / "speckit.specify.md").exists()
    assert not (tmp_path / ".qoder" / "commands" / "speckit.mcpcall.md").exists()
    assert not (tmp_path / ".qoder" / "commands" / "speckit.taskstoissues.md").exists()
    assert not (tmp_path / ".qoder" / "commands" / "speckit.converge.md").exists()
    assert not (specify / "templates" / "commands" / "specify.md").exists()

    # Files the skill no longer owns are reclaimed, and dirs they emptied are pruned
    create_docs = specify / "skills" / "create-docs"
    assert not (create_docs / "scripts" / "scaffold-hugo.py").exists()
    assert not (create_docs / "references" / "hugo-site.md").exists()
    assert not (create_docs / "assets" / "hugo" / "hugo.toml.tmpl").exists()
    assert not (create_docs / "scripts").exists(), "emptied scripts/ dir must be pruned"
    assert not (create_docs / "assets").exists(), "emptied assets/ tree must be pruned"

    # Retired create-team team presets are reclaimed
    create_team_presets = specify / "skills" / "create-team" / "templates" / "teams"
    assert not (create_team_presets / "skills-arena.md").exists()
    assert not (create_team_presets / "workspace-cluster.md").exists()
    assert not (create_team_presets / "artifact-optimizer.md").exists()
    assert not (create_team_presets / "process-monitor.md").exists()

    # Reported removals reference each removed path
    assert any("sdd-workflow" in r for r in removed)
    assert any("agent-explore-template.md" in r for r in removed)
    assert any("speckit.specify.md" in r for r in removed)
    assert any("scaffold-hugo.py" in r for r in removed)
    assert any("skills-arena.md" in r for r in removed)


@pytest.mark.contract
def test_preserves_current_and_user_assets(tmp_path):
    _build_workspace(tmp_path)

    cleanup_obsolete_framework_assets(tmp_path, "qoder")

    specify = tmp_path / ".specify"

    # Current framework assets preserved
    assert (specify / "skills" / "create-team" / "SKILL.md").exists()
    assert (specify / "templates" / "plan-template.md").exists()
    assert (tmp_path / ".qoder" / "commands" / "speckit.requirements.md").exists()
    assert (specify / "templates" / "commands" / "requirements.md").exists()
    # A skill losing files keeps itself and anything the user put inside it
    assert (specify / "skills" / "create-docs" / "SKILL.md").exists()
    assert (specify / "skills" / "create-docs" / "references" / "my-notes.md").exists()
    # The consolidated create-team presets survive
    create_team_presets = specify / "skills" / "create-team" / "templates" / "teams"
    assert (create_team_presets / "capability-arena.md").exists()
    assert (create_team_presets / "project-cluster.md").exists()
    # User-authored assets preserved
    assert (specify / "skills" / "my-custom-skill" / "SKILL.md").exists()
    assert (specify / "templates" / "my-team-template.md").exists()
    assert (tmp_path / ".qoder" / "commands" / "my-custom.md").exists()


@pytest.mark.contract
def test_cleanup_is_idempotent(tmp_path):
    _build_workspace(tmp_path)

    first = cleanup_obsolete_framework_assets(tmp_path, "qoder")
    second = cleanup_obsolete_framework_assets(tmp_path, "qoder")

    assert first  # removed something on first pass
    assert second == []  # nothing left to remove


@pytest.mark.contract
def test_symlinked_obsolete_skill_is_not_deleted(tmp_path):
    """A symlink named like an obsolete skill (e.g. user alias) must be left alone."""
    specify = tmp_path / ".specify"
    (specify / "skills").mkdir(parents=True)
    real = tmp_path / "external-skill"
    _write(real / "SKILL.md")
    link = specify / "skills" / "agent-setup"
    link.symlink_to(real, target_is_directory=True)

    removed = cleanup_obsolete_framework_assets(tmp_path, "qoder")

    assert link.is_symlink()
    assert real.exists()
    assert not any("agent-setup" in r for r in removed)


@pytest.mark.contract
def test_respects_agent_specific_command_extension(tmp_path):
    """copilot commands use the speckit.<stem>.prompt.md naming under .github/prompts."""
    prompts = tmp_path / ".github" / "prompts"
    _write(prompts / "speckit.specify.prompt.md")
    _write(prompts / "speckit.requirements.prompt.md")

    cleanup_obsolete_framework_assets(tmp_path, "copilot")

    assert not (prompts / "speckit.specify.prompt.md").exists()
    assert (prompts / "speckit.requirements.prompt.md").exists()


@pytest.mark.contract
def test_registries_are_nonempty_and_derived_from_history():
    """Guardrail: the obsolete registries must remain populated (framework-scoped)."""
    assert "sdd-workflow" in _OBSOLETE_SKILLS
    assert "agent-cli-setup" in _OBSOLETE_SKILLS
    assert "specify" in _OBSOLETE_COMMANDS
    assert "agent-explore-template.md" in _OBSOLETE_TEMPLATES
    assert "create-docs/scripts/scaffold-hugo.py" in _OBSOLETE_SKILL_FILES
    assert "create-team/templates/teams/skills-arena.md" in _OBSOLETE_SKILL_FILES
    assert "create-team/templates/teams/workspace-cluster.md" in _OBSOLETE_SKILL_FILES
    assert "create-team/templates/teams/artifact-optimizer.md" in _OBSOLETE_SKILL_FILES
    assert "create-team/templates/teams/process-monitor.md" in _OBSOLETE_SKILL_FILES
    # Current names must never be listed as obsolete.
    assert "create-team" not in _OBSOLETE_SKILLS
    assert "manage-agents" not in _OBSOLETE_SKILLS
    assert "requirements" not in _OBSOLETE_COMMANDS
    assert "plan-template.md" not in _OBSOLETE_TEMPLATES
    assert "create-pages/scripts/scaffold-hugo.py" not in _OBSOLETE_SKILL_FILES
    assert "create-team/templates/teams/capability-arena.md" not in _OBSOLETE_SKILL_FILES
    assert "create-team/templates/teams/project-cluster.md" not in _OBSOLETE_SKILL_FILES
