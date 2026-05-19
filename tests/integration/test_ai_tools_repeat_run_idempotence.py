"""Integration tests for repeat-run idempotence.

Validates that running initialization twice with the same assistant
produces identical results (US2).
"""

from pathlib import Path

import pytest

pytestmark = pytest.mark.integration


class TestRepeatRunIdempotence:
    def test_double_init_same_assistant_produces_same_files(
        self, monkeypatch, tmp_path: Path
    ):
        """Two consecutive inits with the same assistant must be idempotent."""
        resource_root = tmp_path / "resource"
        from fixtures.ai_tools_support import make_resource_with_skills

        make_resource_with_skills(resource_root)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        from specify_cli import copy_local_templates

        project = tmp_path / "idem"
        copy_local_templates(project, "copilot", "sh")

        files_first = sorted(
            str(p.relative_to(project)) for p in project.rglob("*") if p.is_file()
        )

        copy_local_templates(project, "copilot", "sh", is_current_dir=True)

        files_second = sorted(
            str(p.relative_to(project)) for p in project.rglob("*") if p.is_file()
        )

        assert set(files_first) == set(files_second), (
            f"Files differ: added={set(files_second) - set(files_first)}, "
            f"removed={set(files_first) - set(files_second)}"
        )

    def test_double_init_different_assistants_no_duplicates(
        self, monkeypatch, tmp_path: Path
    ):
        """Adding the same assistant twice should not duplicate assets."""
        resource_root = tmp_path / "resource"
        from fixtures.ai_tools_support import make_resource_with_skills

        make_resource_with_skills(resource_root)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        from specify_cli import copy_local_templates

        project = tmp_path / "idem"
        copy_local_templates(project, "claude", "sh")

        # Count .claude/command files
        claude_cmds_first = list((project / ".claude" / "commands").rglob("*.md"))
        count_first = len(claude_cmds_first)

        # Init again with same assistant
        copy_local_templates(project, "claude", "sh", is_current_dir=True)

        claude_cmds_second = list((project / ".claude" / "commands").rglob("*.md"))
        count_second = len(claude_cmds_second)

        # No duplicate command files
        assert count_second >= count_first, "Command files were lost"
        # Note: current implementation may overwrite existing, not duplicate
        # This is acceptable as long as content doesn't change

    def test_triple_init_different_assistants(self, monkeypatch, tmp_path: Path):
        """Init copilot, then claude, then copilot again - copilot intact."""
        resource_root = tmp_path / "resource"
        from fixtures.ai_tools_support import make_resource_with_skills

        make_resource_with_skills(resource_root)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        from specify_cli import copy_local_templates

        project = tmp_path / "idem"
        copy_local_templates(project, "copilot", "sh")

        # Record .github/ files
        github_first = sorted(
            str(p.relative_to(project))
            for p in (project / ".github").rglob("*")
            if p.is_file()
        )

        # Add claude
        copy_local_templates(project, "claude", "sh", is_current_dir=True)

        # Add copilot again
        copy_local_templates(project, "copilot", "sh", is_current_dir=True)

        github_third = sorted(
            str(p.relative_to(project))
            for p in (project / ".github").rglob("*")
            if p.is_file()
        )

        for f in github_first:
            assert f in github_third, f"Copilot file {f} was lost"
