"""Declaration-driven acceptance fixtures for feature 097 (``specify migrate``).

Every constructed object name is taken from an owner declaration and asserted
present in that declaration **and** in the checker output at build time
(FR-023 / contracts/migrate-engine.md C-8): fixtures are generated from the
same declarations the command consumes, never from a historical release
snapshot. A construct that stops being recognised by its owner makes the
builder raise, not silently build a stale fixture.

Entry points:

* ``build_latest_project``  — the current installed assets projected through
  the init copy mechanism (``copy_local_templates``) plus ``.specify/source.json``.
* ``build_legacy_project``  — the latest project mutated back into the legacy
  layout (five anchors under ``.specify/memory/``, obsolete skill/command
  residue, a flat internal duplicate, a missing compat link, one edited
  template, one deleted script).
* ``build_mixed_project``   — the latest project plus a subset of those
  constructs (the "partially re-initialised" state).
"""

import importlib.util
import shutil
from pathlib import Path

from specify_cli import (
    _ASSISTANT_COMMAND_DIRS,
    _ASSISTANT_EXTENSIONS,
    _FRAMEWORK_INTERNAL_SKILLS,
    _OBSOLETE_COMMANDS,
    _OBSOLETE_SKILLS,
    copy_local_templates,
    get_resource_path,
    write_source_stamp,
)

DEFAULT_ASSISTANT = "qoder"
DEFAULT_SCRIPT_VARIANT = "sh"

# Anchors relocated to the legacy ``.specify/memory/`` location. The complete
# roster is owned by anchor-layout-migrate.py's ANCHORS (asserted below).
LEGACY_ANCHORS = ("constitution.md", "features.md")
# Flat legacy skill directories — owner: the CLI's _OBSOLETE_SKILLS registry.
LEGACY_SKILL_NAMES = ("agent-cli-setup", "docx-utils", "web-test")
# Obsolete command copies — owner: the CLI's _OBSOLETE_COMMANDS registry.
LEGACY_COMMAND_STEMS = ("converge", "taskstoissues")
# Flat duplicate of a nested framework-internal skill — owner: _FRAMEWORK_INTERNAL_SKILLS.
FLAT_INTERNAL_DUPLICATE = "create-agent"
# Missing (removed) compat link — owner: sanitize-utils.COMPAT_SYMLINKS.
MISSING_COMPAT_LINK = ".qoder/skills"
# Edited framework template (templates-generated / mirror-consistency difference).
EDITED_TEMPLATE = "templates/plan-template.md"
# Deleted framework script (mirror-consistency difference).
DELETED_SCRIPT = "scripts/python/flow-class-check.py"


def _engine_module(filename: str):
    """In-process load of a client engine from get_resource_path()/scripts/python/."""
    engine_dir = Path(get_resource_path()) / "scripts" / "python"
    path = engine_dir / filename
    if not path.is_file():
        raise FileNotFoundError(f"engine not found for fixture construction: {path}")
    module_name = "_migrate_097_" + path.stem.replace("-", "_")
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_latest_project(
    dest,
    assistant: str = DEFAULT_ASSISTANT,
    script_type: str = DEFAULT_SCRIPT_VARIANT,
) -> Path:
    """Project the current installed assets into ``dest`` via the init copy mechanism."""
    dest = Path(dest)
    copy_local_templates(dest, assistant, script_type, is_current_dir=False)
    if not write_source_stamp(dest):
        raise RuntimeError(f"source stamp write failed for fixture at {dest}")
    if not (dest / ".specify" / "source.json").is_file():
        raise AssertionError(".specify/source.json missing from the latest fixture")
    return dest


def build_legacy_project(
    dest,
    assistant: str = DEFAULT_ASSISTANT,
    script_type: str = DEFAULT_SCRIPT_VARIANT,
) -> Path:
    """The latest project mutated into the legacy mixed state, declaration-driven."""
    dest = build_latest_project(dest, assistant, script_type)
    specify = dest / ".specify"
    anchor_engine = _engine_module("anchor-layout-migrate.py")
    sanitize = _engine_module("sanitize-utils.py")

    memory = specify / "memory"
    memory.mkdir(parents=True, exist_ok=True)

    # 1) Anchor layout — move anchors to their legacy .specify/memory/ location.
    for anchor in LEGACY_ANCHORS:
        assert anchor in anchor_engine.ANCHORS, (
            f"fixture anchor {anchor!r} is not in the anchor engine's declared roster"
        )
        source = specify / anchor
        if not source.is_file():
            raise FileNotFoundError(f"anchor missing from the latest projection: {source}")
        source.replace(memory / anchor)
    steps = anchor_engine.plan(dest)
    moved_anchors = {
        Path(step["from"]).name for step in steps if step["kind"] == "move"
    }
    for anchor in LEGACY_ANCHORS:
        assert anchor in moved_anchors, (
            f"anchor-layout-migrate check does not report the constructed {anchor!r}"
        )

    # 2) Obsolete skill residue — flat directories owned by the removal registry.
    for name in LEGACY_SKILL_NAMES:
        assert name in _OBSOLETE_SKILLS, (
            f"fixture skill {name!r} is not in _OBSOLETE_SKILLS"
        )
        skill_dir = specify / "skills" / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(
            f"# {name} (legacy fixture residue)\n", encoding="utf-8"
        )
    residue_targets = {
        finding["target"] for finding in sanitize.check_legacy_install_residue(dest)
    }
    for name in LEGACY_SKILL_NAMES:
        assert f".specify/skills/{name}" in residue_targets, (
            f"check_legacy_install_residue does not report .specify/skills/{name}"
        )

    # 3) Obsolete command copies — in the active tool's command directory.
    command_rel = _ASSISTANT_COMMAND_DIRS[assistant]
    command_ext = _ASSISTANT_EXTENSIONS[assistant]
    for stem in LEGACY_COMMAND_STEMS:
        assert stem in _OBSOLETE_COMMANDS, (
            f"fixture command stem {stem!r} is not in _OBSOLETE_COMMANDS"
        )
        command_path = dest / command_rel / f"speckit.{stem}.{command_ext}"
        command_path.parent.mkdir(parents=True, exist_ok=True)
        command_path.write_text(f"# obsolete command: {stem}\n", encoding="utf-8")
        assert command_path.is_file()

    # 4) Flat internal duplicate — nested framework-internal skill copied flat.
    assert FLAT_INTERNAL_DUPLICATE in _FRAMEWORK_INTERNAL_SKILLS, (
        f"fixture internal skill {FLAT_INTERNAL_DUPLICATE!r} is not in "
        "_FRAMEWORK_INTERNAL_SKILLS"
    )
    nested = specify / "skills" / "internal" / FLAT_INTERNAL_DUPLICATE
    flat = specify / "skills" / FLAT_INTERNAL_DUPLICATE
    if not nested.is_dir():
        raise FileNotFoundError(f"nested internal skill missing: {nested}")
    shutil.copytree(nested, flat)
    duplicate_targets = {
        finding["target"] for finding in sanitize.check_flat_internal_duplicates(dest)
    }
    assert f".specify/skills/{FLAT_INTERNAL_DUPLICATE}" in duplicate_targets, (
        "check_flat_internal_duplicates does not report the constructed flat duplicate"
    )

    # 5) Missing compat link — removed after the projection created it.
    assert MISSING_COMPAT_LINK in sanitize.COMPAT_SYMLINKS, (
        f"fixture link {MISSING_COMPAT_LINK!r} is not in COMPAT_SYMLINKS"
    )
    link = dest / MISSING_COMPAT_LINK
    if not link.is_symlink():
        raise FileNotFoundError(f"expected projected compat link missing: {link}")
    link.unlink()
    link_targets = {
        finding["target"] for finding in sanitize.check_broken_symlinks(dest)
    }
    assert MISSING_COMPAT_LINK in link_targets, (
        "check_broken_symlinks does not report the removed compat link"
    )

    # 6) Edited template + deleted script — the template/command projection and
    #    the scripts mirror each lose one file relative to the reference tree.
    template = specify / EDITED_TEMPLATE
    if not template.is_file():
        raise FileNotFoundError(f"projected template missing: {template}")
    template.write_text(
        template.read_text(encoding="utf-8") + "\n<!-- fixture edit -->\n",
        encoding="utf-8",
    )
    script = specify / DELETED_SCRIPT
    if not script.is_file():
        raise FileNotFoundError(f"projected script missing: {script}")
    script.unlink()
    assert not script.exists()

    return dest


def build_mixed_project(
    dest,
    assistant: str = DEFAULT_ASSISTANT,
    script_type: str = DEFAULT_SCRIPT_VARIANT,
) -> Path:
    """The latest project plus a subset of legacy constructs (partial re-init)."""
    dest = build_latest_project(dest, assistant, script_type)
    specify = dest / ".specify"
    sanitize = _engine_module("sanitize-utils.py")

    name = LEGACY_SKILL_NAMES[0]
    assert name in _OBSOLETE_SKILLS
    skill_dir = specify / "skills" / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        f"# {name} (mixed fixture residue)\n", encoding="utf-8"
    )
    residue_targets = {
        finding["target"] for finding in sanitize.check_legacy_install_residue(dest)
    }
    assert f".specify/skills/{name}" in residue_targets

    assert MISSING_COMPAT_LINK in sanitize.COMPAT_SYMLINKS
    link = dest / MISSING_COMPAT_LINK
    if not link.is_symlink():
        raise FileNotFoundError(f"expected projected compat link missing: {link}")
    link.unlink()
    link_targets = {
        finding["target"] for finding in sanitize.check_broken_symlinks(dest)
    }
    assert MISSING_COMPAT_LINK in link_targets

    template = specify / EDITED_TEMPLATE
    if not template.is_file():
        raise FileNotFoundError(f"projected template missing: {template}")
    template.write_text(
        template.read_text(encoding="utf-8") + "\n<!-- mixed fixture edit -->\n",
        encoding="utf-8",
    )
    return dest
