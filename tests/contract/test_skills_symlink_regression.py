"""Contract test: ensure_specify_symlink with 'skills' preserves existing behavior."""

import pytest
from pathlib import Path

from specify_cli import ensure_specify_symlink


@pytest.mark.contract
class TestSkillsSymlinkRegression:
    """Regression guard: skills symlinks work identically after refactor to ensure_specify_symlink."""

    def test_github_skills_symlink_resolves(self, tmp_path):
        (tmp_path / ".specify").mkdir()
        ensure_specify_symlink(tmp_path, ".github", "skills")

        link = tmp_path / ".github" / "skills"
        assert link.is_symlink()
        assert link.resolve() == (tmp_path / ".specify" / "skills").resolve()

    def test_qoder_skills_symlink_resolves(self, tmp_path):
        (tmp_path / ".specify").mkdir()
        ensure_specify_symlink(tmp_path, ".qoder", "skills")

        link = tmp_path / ".qoder" / "skills"
        assert link.is_symlink()
        assert link.resolve() == (tmp_path / ".specify" / "skills").resolve()

    def test_claude_skills_symlink_resolves(self, tmp_path):
        (tmp_path / ".specify").mkdir()
        ensure_specify_symlink(tmp_path, ".claude", "skills")

        link = tmp_path / ".claude" / "skills"
        assert link.is_symlink()
        assert link.resolve() == (tmp_path / ".specify" / "skills").resolve()

    def test_qwen_skills_symlink_resolves(self, tmp_path):
        (tmp_path / ".specify").mkdir()
        ensure_specify_symlink(tmp_path, ".qwen", "skills")

        link = tmp_path / ".qwen" / "skills"
        assert link.is_symlink()
        assert link.resolve() == (tmp_path / ".specify" / "skills").resolve()

    def test_opencode_skills_symlink_resolves(self, tmp_path):
        (tmp_path / ".specify").mkdir()
        ensure_specify_symlink(tmp_path, ".opencode", "skills")

        link = tmp_path / ".opencode" / "skills"
        assert link.is_symlink()
        assert link.resolve() == (tmp_path / ".specify" / "skills").resolve()

    def test_skills_content_preserved_after_migration(self, tmp_path):
        (tmp_path / ".specify").mkdir()
        skills_dir = tmp_path / ".github" / "skills"
        skills_dir.mkdir(parents=True)
        (skills_dir / "my-skill" / "SKILL.md").parent.mkdir()
        (skills_dir / "my-skill" / "SKILL.md").write_text("skill content")

        ensure_specify_symlink(tmp_path, ".github", "skills")

        assert (tmp_path / ".specify" / "skills" / "my-skill" / "SKILL.md").read_text() == "skill content"
        assert (tmp_path / ".github" / "skills").is_symlink()
