"""Integration tests for refresh isolation.

Validates that refreshing or adding one assistant does not damage other assistant
roots in a multi-assistant workspace (US3).

Absorbs ``test_ai_tools_custom_asset_conflicts.py``: same proposition (nothing in a
neighbouring root is lost), same ``copy_local_templates`` driver, so the two files
only differed in which assistant pair they happened to pick.
"""

from pathlib import Path

import pytest

pytestmark = pytest.mark.integration


class TestRefreshIsolation:
    def test_refresh_claude_does_not_affect_copilot(self, monkeypatch, tmp_path: Path):
        """Refreshing one assistant must leave other assistant roots untouched."""
        resource_root = tmp_path / "resource"
        from fixtures.ai_tools_support import make_resource_with_skills

        make_resource_with_skills(resource_root)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        from specify_cli import copy_local_templates

        project = tmp_path / "refresh-test"
        copy_local_templates(project, "copilot", "sh")
        copy_local_templates(project, "claude", "sh", is_current_dir=True)

        # Snapshot copilot root
        copilot_files_before = sorted(
            str(p.relative_to(project))
            for p in (project / ".github").rglob("*")
            if p.is_file()
        )

        # Refresh claude
        copy_local_templates(project, "claude", "sh", is_current_dir=True)

        copilot_files_after = sorted(
            str(p.relative_to(project))
            for p in (project / ".github").rglob("*")
            if p.is_file()
        )

        # Copilot files must be exactly the same
        assert copilot_files_before == copilot_files_after, (
            f"Copilot root changed after claude refresh:\n"
            f"before={copilot_files_before}\nafter={copilot_files_after}"
        )

    def test_refresh_does_not_remove_unrelated_assistant_root(
        self, monkeypatch, tmp_path: Path
    ):
        """Refreshing one assistant must not delete another assistant's root dir."""
        resource_root = tmp_path / "resource"
        from fixtures.ai_tools_support import make_resource_with_skills

        make_resource_with_skills(resource_root)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        from specify_cli import copy_local_templates

        project = tmp_path / "keep-test"
        copy_local_templates(project, "qoder", "sh")
        copy_local_templates(project, "opencode", "sh", is_current_dir=True)

        assert (project / ".qoder").is_dir()
        assert (project / ".opencode").is_dir()

        # Refresh qoder
        copy_local_templates(project, "qoder", "sh", is_current_dir=True)

        # Both roots still present
        assert (project / ".qoder").is_dir(), "qoder root removed after refresh"
        assert (project / ".opencode").is_dir(), (
            "opencode root removed after qoder refresh"
        )

    def test_custom_command_file_is_not_deleted_by_refresh(
        self, monkeypatch, tmp_path: Path
    ):
        """A user-modified assistant command file must survive a refresh.

        Scope note: refresh regenerates command files from the templates, so the
        *content* is overwritten by design and is deliberately not asserted here.
        What is load-bearing is that the refresh does not remove the file (or the
        user's customization with it) — a deletion would be silent data loss.
        """
        resource_root = tmp_path / "resource"
        from fixtures.ai_tools_support import make_resource_with_skills

        make_resource_with_skills(resource_root)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        from specify_cli import copy_local_templates

        project = tmp_path / "workspace"
        copy_local_templates(project, "claude", "sh")

        cmd_path = project / ".claude" / "commands" / "speckit.requirements.md"
        assert cmd_path.exists(), "Command file not generated"
        cmd_path.write_text(
            "# Custom requirements command\n\nUser customization.", encoding="utf-8"
        )

        # Re-run init (refresh)
        copy_local_templates(project, "claude", "sh", is_current_dir=True)

        assert cmd_path.exists(), "Custom command was deleted"

    def test_user_file_in_other_assistant_dir_survives(
        self, monkeypatch, tmp_path: Path
    ):
        """A file the *user* placed in an assistant directory is not a generated
        asset, so no init for a different assistant may remove it."""
        resource_root = tmp_path / "resource"
        from fixtures.ai_tools_support import make_resource_with_skills

        make_resource_with_skills(resource_root)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        from specify_cli import copy_local_templates

        project = tmp_path / "workspace"
        copy_local_templates(project, "hermes", "sh")

        # Add a user file
        user_file = project / ".hermes" / "user-config.md"
        user_file.write_text('# custom\n', encoding="utf-8")

        # Add another assistant - user file in original assistant dir should survive
        copy_local_templates(project, "claude", "sh", is_current_dir=True)

        assert user_file.exists(), (
            "User file was deleted from other assistant directory"
        )

    def test_adding_assistant_preserves_other_root_files(
        self, monkeypatch, tmp_path: Path
    ):
        """The file set of one assistant's directory must survive another assistant's
        first init — the add path, as opposed to the refresh path covered above."""
        resource_root = tmp_path / "resource"
        from fixtures.ai_tools_support import make_resource_with_skills

        make_resource_with_skills(resource_root)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        from specify_cli import copy_local_templates

        project = tmp_path / "workspace"
        copy_local_templates(project, "copilot", "sh")

        # Count files in .github/
        github_files_before = sorted(
            str(p.relative_to(project))
            for p in (project / ".github").rglob("*")
            if p.is_file()
        )

        # Add qoder
        copy_local_templates(project, "qoder", "sh", is_current_dir=True)

        github_files_after = sorted(
            str(p.relative_to(project))
            for p in (project / ".github").rglob("*")
            if p.is_file()
        )

        # All original .github/ files should still exist
        for f in github_files_before:
            assert f in github_files_after, f"File {f} was removed from .github/"
