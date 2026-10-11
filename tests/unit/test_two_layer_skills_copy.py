"""Smoke test for the install-time two-layer skills copy.

Source layout (framework resources):
    skills/external/<name>/...  -> <project>/.specify/skills/<name>/...        (flat)
    skills/internal/<name>/...  -> <project>/.specify/skills/internal/<name>/  (nested)

copy_tree_with_rewrite must also: rewrite source-form refs to runtime form,
copy binary files byte-identical, and preserve copytree(dirs_exist_ok=True)
additive semantics (never delete pre-existing destination files).
"""

from specify_cli import copy_tree_with_rewrite


def _build_fake_skills_source(root):
    """Create a minimal skills/{external,internal} resource tree."""
    ext = root / "skills" / "external" / "demo-ext"
    int_ = root / "skills" / "internal" / "demo-int"
    ext.mkdir(parents=True)
    int_.mkdir(parents=True)

    (ext / "SKILL.md").write_text(
        "# demo-ext\n"
        "See skills/internal/demo-int/SKILL.md and skills/external/demo-ext/scripts/run.py\n"
        "Memory lives at memory/constitution.md\n",
        encoding="utf-8",
    )
    (int_ / "SKILL.md").write_text(
        "# demo-int\nConsumes skills/external/demo-ext/SKILL.md\n",
        encoding="utf-8",
    )
    (ext / "scripts").mkdir()
    # Ref uses the contractual `<name>/` directory form (the landed regexes
    # require the trailing slash after the skill name).
    (ext / "scripts" / "run.py").write_text(
        "print('skills/internal/demo-int/SKILL.md')\n", encoding="utf-8"
    )
    # Junk that must never be copied
    (ext / "__pycache__").mkdir()
    (ext / "__pycache__" / "junk.pyc").write_bytes(b"\x00junk")
    (ext / ".DS_Store").write_bytes(b"\x00ds")
    # Binary payload that must survive byte-identical
    payload = bytes(range(256)) + b"\xff\xfe\x80not-utf8"
    (ext / "blob.bin").write_bytes(payload)
    return payload


def test_two_layer_layout_and_rewrite(tmp_path):
    src_root = tmp_path / "resource"
    dest_root = tmp_path / "project" / ".specify" / "skills"
    payload = _build_fake_skills_source(src_root)

    # Mirror copy_local_templates' two-layer invocation
    copy_tree_with_rewrite(src_root / "skills" / "external", dest_root)
    copy_tree_with_rewrite(src_root / "skills" / "internal", dest_root / "internal")

    # Flat external layer
    ext_skill = dest_root / "demo-ext" / "SKILL.md"
    assert ext_skill.is_file()
    text = ext_skill.read_text(encoding="utf-8")
    # Source-form refs (not preceded by `.specify/`) must be gone; the nested
    # runtime form legitimately contains `skills/internal/...` as a substring.
    assert "See skills/internal/" not in text
    assert "and skills/external/" not in text
    assert ".specify/skills/internal/demo-int/SKILL.md" in text
    assert ".specify/skills/demo-ext/scripts/run.py" in text
    assert ".specify/memory/constitution.md" in text
    assert ".specify/.specify/" not in text

    # Nested internal layer
    int_skill = dest_root / "internal" / "demo-int" / "SKILL.md"
    assert int_skill.is_file()
    assert (
        "Consumes .specify/skills/demo-ext/SKILL.md"
        in int_skill.read_text(encoding="utf-8")
    )

    # Code file refs rewritten too
    run_py = (dest_root / "demo-ext" / "scripts" / "run.py").read_text(
        encoding="utf-8"
    )
    assert run_py == "print('.specify/skills/internal/demo-int/SKILL.md')\n"

    # Binary copied byte-identical
    assert (dest_root / "demo-ext" / "blob.bin").read_bytes() == payload

    # Junk skipped
    assert not (dest_root / "demo-ext" / "__pycache__").exists()
    assert not (dest_root / "demo-ext" / ".DS_Store").exists()


def test_copy_is_additive_and_overwriting(tmp_path):
    src_root = tmp_path / "resource"
    dest_root = tmp_path / "project" / ".specify" / "skills"
    _build_fake_skills_source(src_root)

    # Pre-existing user skill + stale file in destination must survive
    (dest_root / "user-own-skill").mkdir(parents=True)
    (dest_root / "user-own-skill" / "SKILL.md").write_text("mine", encoding="utf-8")

    copy_tree_with_rewrite(src_root / "skills" / "external", dest_root)

    assert (dest_root / "user-own-skill" / "SKILL.md").read_text(
        encoding="utf-8"
    ) == "mine"
    assert (dest_root / "demo-ext" / "SKILL.md").is_file()

    # Second pass overwrites shipped files but is a content-level no-op
    before = (dest_root / "demo-ext" / "SKILL.md").read_text(encoding="utf-8")
    copy_tree_with_rewrite(src_root / "skills" / "external", dest_root)
    assert (dest_root / "demo-ext" / "SKILL.md").read_text(encoding="utf-8") == before


def test_missing_source_is_noop(tmp_path):
    dest = tmp_path / "out"
    copy_tree_with_rewrite(tmp_path / "does-not-exist", dest)
    assert not dest.exists()
