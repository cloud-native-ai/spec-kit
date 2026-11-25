"""Integration tests for partial .specify repair with missing core files.

Validates that when .specify/ exists but is missing required core
components, initialization adds only what's missing (US2).
"""

from pathlib import Path

import pytest

pytestmark = pytest.mark.integration


class TestPartialCoreRepair:
    def test_missing_templates_added(self, monkeypatch, tmp_path: Path):
        """When .specify/templates/ is missing, it should be added."""
        resource_root = tmp_path / "resource"
        from fixtures.ai_tools_support import make_resource_with_skills

        make_resource_with_skills(resource_root)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        from specify_cli import copy_local_templates

        project = tmp_path / "partial"
        project.mkdir()
        (project / ".specify" / "session").mkdir(parents=True)
        (project / ".specify" / "scripts").mkdir(parents=True)
        # templates/ is intentionally missing

        copy_local_templates(project, "copilot", "sh", is_current_dir=True)

        assert (project / ".specify" / "templates").is_dir(), "templates/ not created"

    def test_missing_scripts_added(self, monkeypatch, tmp_path: Path):
        """When .specify/scripts/ is missing, it should be added."""
        resource_root = tmp_path / "resource"
        from fixtures.ai_tools_support import make_resource_with_skills

        make_resource_with_skills(resource_root)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        from specify_cli import copy_local_templates

        project = tmp_path / "partial"
        project.mkdir()
        (project / ".specify" / "session").mkdir(parents=True)
        (project / ".specify" / "templates").mkdir(parents=True)

        copy_local_templates(project, "copilot", "sh", is_current_dir=True)

        assert (project / ".specify" / "scripts").is_dir(), "scripts/ not created"

    def test_missing_memory_added(self, monkeypatch, tmp_path: Path):
        """When .specify/session/ is missing, it should be added."""
        resource_root = tmp_path / "resource"
        from fixtures.ai_tools_support import make_resource_with_skills

        make_resource_with_skills(resource_root)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        from specify_cli import copy_local_templates

        project = tmp_path / "partial"
        project.mkdir()
        (project / ".specify" / "scripts").mkdir(parents=True)
        (project / ".specify" / "templates").mkdir(parents=True)

        copy_local_templates(project, "copilot", "sh", is_current_dir=True)

        assert (project / ".specify" / "session").is_dir(), "memory/ not created"

    def test_existing_memory_files_preserved_during_repair(
        self, monkeypatch, tmp_path: Path
    ):
        """Existing memory-tier entries must be preserved when repairing other directories."""
        resource_root = tmp_path / "resource"
        from fixtures.ai_tools_support import make_resource_with_skills

        make_resource_with_skills(resource_root)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        from specify_cli import copy_local_templates

        project = tmp_path / "partial"
        project.mkdir()
        (project / ".specify" / "session").mkdir(parents=True)
        (project / ".specify" / "session" / "notes.md").write_text(
            "# Our working notes\n\nCustom session entry.", encoding="utf-8"
        )

        # scripts and templates are missing
        copy_local_templates(project, "copilot", "sh", is_current_dir=True)

        const = (project / ".specify" / "session" / "notes.md").read_text(
            encoding="utf-8"
        )
        assert "Custom session entry" in const, "Custom session entry was overwritten"
