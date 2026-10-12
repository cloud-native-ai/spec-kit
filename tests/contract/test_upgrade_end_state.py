"""Contract test: upgrade END STATE over a pre-layering (flat) install.

Red-first baseline: ``docs/notes/consumer-upgrade-migration-plan.md`` §1 — a
real 0.0.22 consumer upgraded with the post-layering wheel kept all 15 flat
framework-internal skill copies (``migrated 0 … kept 15``) because the
internal-layer skills copy ran BEFORE ``migrate_flat_internal_skills``, so the
migration always hit its "nested target exists → keep flat" branch.

This test drives the REAL ``copy_local_templates`` (monkeypatched
``get_resource_path``, same idiom as the shared-dir install tests) over a fake
OLD install and asserts the upgrade end state:

  * flat framework-internal skill ABSENT (relocated / reclaimed, not kept);
  * ``internal/<name>/SKILL.md`` present with the NEW resource content;
  * user-authored skill untouched and still FLAT (red line);
  * flat external skill refreshed with rewritten ``.specify/`` runtime-form refs.
"""

from pathlib import Path

import pytest

from specify_cli import copy_local_templates


def _build_fake_resource(root: Path) -> Path:
    """Framework resource tree: two-layer skills source layout + minimal scaffold."""
    r = root / "resource"
    # External layer (installs flat). Source-form refs must land rewritten.
    ext = r / "skills" / "external" / "demo-ext"
    ext.mkdir(parents=True)
    (ext / "SKILL.md").write_text(
        "# demo-ext (new)\n"
        "See skills/internal/demo-int/SKILL.md for the internal layer.\n"
        "Memory anchor: memory/constitution.md\n",
        encoding="utf-8",
    )
    # Internal layer (installs nested): demo-int plus a REAL framework name.
    for name, body in (
        ("demo-int", "# demo-int (new)\nConsumes skills/external/demo-ext/SKILL.md\n"),
        ("create-agent", "# create-agent (new)\n"),
    ):
        skill_dir = r / "skills" / "internal" / name
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(body, encoding="utf-8")
    # Minimal scaffold for the code path's other copy targets.
    (r / "templates" / "commands").mkdir(parents=True)
    (r / "templates" / "commands" / "requirements.md").write_text(
        "# requirements\nSee shared/workflow/user-input-protocol.md\n",
        encoding="utf-8",
    )
    (r / "memory").mkdir()
    (r / "memory" / "constitution.md").write_text("# C\n", encoding="utf-8")
    (r / "memory" / "features.md").write_text("# F\n", encoding="utf-8")
    (r / "scripts").mkdir()
    return r


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _build_old_install(project: Path) -> None:
    """Fake pre-layering install: framework skills FLAT, user skill present."""
    skills = project / ".specify" / "skills"
    # Framework-INTERNAL name, flat, OLD content (pre-layering copy).
    _write(skills / "create-agent" / "SKILL.md", "# create-agent (OLD flat copy)\n")
    # Framework-EXTERNAL name, flat, OLD content (gets refreshed by the copy).
    _write(skills / "demo-ext" / "SKILL.md", "# demo-ext (OLD)\n")
    # User-authored skill (red line: never touched, stays flat).
    _write(skills / "my-own-skill" / "SKILL.md", "# mine\n")
    # .specify skeleton the code path expects on an existing install.
    (project / ".specify" / "templates").mkdir(parents=True, exist_ok=True)


@pytest.mark.contract
def test_upgrade_end_state_over_flat_internal_install(monkeypatch, tmp_path: Path):
    """Old flat install → after init: no flat internal residue, nested present."""
    resource = _build_fake_resource(tmp_path)
    monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource)

    project = tmp_path / "proj"
    _build_old_install(project)

    # Real upgrade path: the engine's own copy order is exercised end-to-end.
    copy_local_templates(project, "claude", "sh")

    skills = project / ".specify" / "skills"

    # 1) Flat framework-internal copy ABSENT (the red-first baseline: the old
    #    engine "kept 15" here because the internal copy had already run).
    assert not (skills / "create-agent").exists()

    # 2) Nested internal skill present, refreshed to the NEW resource content.
    nested = skills / "internal" / "create-agent" / "SKILL.md"
    assert nested.is_file()
    assert nested.read_text(encoding="utf-8") == "# create-agent (new)\n"
    assert (skills / "internal" / "demo-int" / "SKILL.md").is_file()

    # 3) User skill untouched and still FLAT (never nested, content preserved).
    assert (skills / "my-own-skill" / "SKILL.md").read_text(
        encoding="utf-8"
    ) == "# mine\n"
    assert not (skills / "internal" / "my-own-skill").exists()

    # 4) Flat external skill refreshed with rewritten runtime-form refs.
    flat_ext = skills / "demo-ext" / "SKILL.md"
    text = flat_ext.read_text(encoding="utf-8")
    assert text.startswith("# demo-ext (new)\n")
    assert "See .specify/skills/internal/demo-int/SKILL.md" in text
    assert "See skills/internal/demo-int" not in text
    assert ".specify/memory/constitution.md" in text
