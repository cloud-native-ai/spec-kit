"""Integration tests for refresh isolation.

Validates that refreshing one assistant does not damage other assistant
roots in a multi-assistant workspace (US3).
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
