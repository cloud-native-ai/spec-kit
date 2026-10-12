"""Contract tests: init-time migration of flat framework-INTERNAL skills.

The runtime layering contract (layer introduced 2026-10) nests framework-internal
skills at ``.specify/skills/internal/<name>/`` so they stay invisible to the client's
flat discovery surface while ``/speckit.*`` workflows consume them by explicit path.
Installs that predate the layer carry these same skills FLAT at
``.specify/skills/<name>/``.

``migrate_flat_internal_skills`` is the upgrade-time relocation step. It must:
  * move ONLY the enumerated framework-owned internal names (flat -> nested);
  * never touch external framework skills (they stay flat);
  * never touch user-authored skills (red line);
  * when the nested target already exists, the flat copy is a stale framework
    duplicate: it is REMOVED and counted as ``removed_stale`` (the nested copy
    is never overwritten; an OSError degrades to the legacy ``kept`` counter).
"""

from pathlib import Path

import pytest

from specify_cli import (
    _FRAMEWORK_INTERNAL_SKILLS,
    migrate_flat_internal_skills,
)


def _write(path: Path, content: str = "x\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


@pytest.mark.contract
def test_moves_flat_internal_leaves_external_and_user(tmp_path):
    """Flat internal -> nested; external + user-authored stay flat and untouched."""
    skills = tmp_path / ".specify" / "skills"
    # Framework-INTERNAL, flat, no nested target -> must move
    _write(skills / "create-agent" / "SKILL.md", "# create-agent\n")
    # Framework-EXTERNAL, flat -> must be left exactly as-is
    _write(skills / "draw-mermaid" / "SKILL.md", "# draw-mermaid\n")
    # User-authored, flat -> must be left exactly as-is
    _write(skills / "my-own-skill" / "SKILL.md", "# mine\n")

    result = migrate_flat_internal_skills(tmp_path)

    # create-agent relocated to the nested runtime location, content preserved
    assert not (skills / "create-agent").exists()
    assert (skills / "internal" / "create-agent" / "SKILL.md").read_text(
        encoding="utf-8"
    ) == "# create-agent\n"
    # External + user skills untouched, still flat, never nested
    assert (skills / "draw-mermaid" / "SKILL.md").exists()
    assert not (skills / "internal" / "draw-mermaid").exists()
    assert (skills / "my-own-skill" / "SKILL.md").exists()
    assert not (skills / "internal" / "my-own-skill").exists()
    # Counters: exactly the internal name moved; nothing kept
    assert any("create-agent" in p for p in result["moved"])
    assert len(result["moved"]) == 1
    assert result["kept"] == []
    assert not any("draw-mermaid" in p for p in result["moved"])
    assert not any("my-own-skill" in p for p in result["moved"])


@pytest.mark.contract
def test_removes_stale_flat_when_nested_target_exists(tmp_path):
    """Flat internal duplicate of an existing nested target is REMOVED, not kept."""
    skills = tmp_path / ".specify" / "skills"
    # Flat pre-layering copy ...
    _write(skills / "create-team" / "SKILL.md", "# flat create-team\n")
    # ... and the nested target already present (e.g. a prior layered install
    # left one behind)
    _write(skills / "internal" / "create-team" / "SKILL.md", "# nested create-team\n")

    result = migrate_flat_internal_skills(tmp_path)

    # Stale flat duplicate removed; nested copy intact (never overwritten)
    assert not (skills / "create-team").exists()
    assert (skills / "internal" / "create-team" / "SKILL.md").read_text(
        encoding="utf-8"
    ) == "# nested create-team\n"
    # Counted as removed_stale, not moved
    assert any("create-team" in p for p in result["removed_stale"])
    assert len(result["removed_stale"]) == 1
    assert result["moved"] == []
    assert result["kept"] == []


@pytest.mark.contract
def test_migration_is_idempotent(tmp_path):
    """A second pass finds nothing flat to move (already nested)."""
    skills = tmp_path / ".specify" / "skills"
    _write(skills / "memory-record" / "SKILL.md", "# mr\n")

    first = migrate_flat_internal_skills(tmp_path)
    second = migrate_flat_internal_skills(tmp_path)

    assert any("memory-record" in p for p in first["moved"])
    assert second["moved"] == []
    assert second["kept"] == []
    assert (skills / "internal" / "memory-record" / "SKILL.md").exists()
    assert not (skills / "memory-record").exists()


@pytest.mark.contract
def test_symlinked_internal_name_is_not_moved(tmp_path):
    """A symlink named like an internal skill (user alias) must be left alone."""
    skills = tmp_path / ".specify" / "skills"
    skills.mkdir(parents=True)
    real = tmp_path / "external-target"
    _write(real / "SKILL.md", "# real\n")
    link = skills / "code-review"
    link.symlink_to(real, target_is_directory=True)

    result = migrate_flat_internal_skills(tmp_path)

    assert link.is_symlink()
    assert real.exists()
    assert not (skills / "internal" / "code-review").exists()
    assert result["moved"] == []
    assert result["kept"] == []


@pytest.mark.contract
def test_no_skills_dir_is_noop(tmp_path):
    """A project without .specify/skills/ must not error or create empty dirs."""
    result = migrate_flat_internal_skills(tmp_path)

    assert result == {"moved": [], "kept": [], "removed_stale": []}
    # Nothing to migrate -> no empty nested dir is conjured into existence
    assert not (tmp_path / ".specify" / "skills" / "internal").exists()


@pytest.mark.contract
def test_internal_roster_is_populated_and_scoped():
    """Guardrail: the migration manifest lists framework-internal names only."""
    # A representative sample of the 15 internal names is present
    for name in (
        "create-agent",
        "create-team",
        "memory-record",
        "self-improvement",
        "study-project",
    ):
        assert name in _FRAMEWORK_INTERNAL_SKILLS
    # External framework names and user-authored names must NEVER be listed
    assert "draw-mermaid" not in _FRAMEWORK_INTERNAL_SKILLS
    assert "create-docs" not in _FRAMEWORK_INTERNAL_SKILLS
    # Legacy/obsolete names belong to the removal manifest, not the migration one
    assert "organize-agents" not in _FRAMEWORK_INTERNAL_SKILLS
    assert "sdd-workflow" not in _FRAMEWORK_INTERNAL_SKILLS
