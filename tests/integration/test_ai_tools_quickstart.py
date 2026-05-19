"""Integration tests for quickstart scenario validation.

Covers new-project initialization, existing-project addition, coexistence,
and audit scenarios from quickstart.md (US1, US2, US3).
"""

from pathlib import Path

import pytest

from specify_cli import (
    _OFFICIAL_ASSISTANT_KEYS,
    copy_local_templates,
    get_assistant_profile,
)

pytestmark = pytest.mark.integration


class TestQuickstartScenario1NewProject:
    """Scenario 1: New project initialization for every official assistant."""

    def test_new_project_scenario(self, monkeypatch, tmp_path: Path):
        resource_root = tmp_path / "resource"
        from fixtures.ai_tools_support import make_resource_with_skills

        make_resource_with_skills(resource_root)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        for assistant in _OFFICIAL_ASSISTANT_KEYS:
            project = tmp_path / f"qs-{assistant}"
            copy_local_templates(project, assistant, "sh")

            # Expected Result checks from quickstart
            assert (project / ".specify").is_dir()
            assert (project / ".specify" / "memory").is_dir()
            assert (project / ".specify" / "scripts").is_dir()
            assert (project / ".specify" / "skills").is_dir()

            # Assistant-specific directory must exist
            profile = get_assistant_profile(assistant)
            folder = profile["folder"]
            assert (project / folder).is_dir(), (
                f"[{assistant}] Missing assistant root {folder}"
            )

            # Command directory must exist with files
            cmd_dir = project / profile["command_directory"]
            assert cmd_dir.is_dir() or (project / folder / "prompts").is_dir(), (
                f"[{assistant}] Missing command directory"
            )


class TestQuickstartScenario2AddSecondAssistant:
    """Scenario 2: Existing project adds a second assistant."""

    def test_core_modified_file_preserved(self, monkeypatch, tmp_path: Path):
        resource_root = tmp_path / "resource"
        from fixtures.ai_tools_support import make_resource_with_skills

        make_resource_with_skills(resource_root)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        project = tmp_path / "workspace"
        # Init with copilot (copy_local_templates creates the dir)
        copy_local_templates(project, "copilot", "sh")

        # Modify a core file
        features_md = project / ".specify" / "memory" / "features.md"
        features_md.write_text(
            "# Modified Features\nCustom content\n", encoding="utf-8"
        )

        # Add claude (use is_current_dir since project already exists)
        copy_local_templates(project, "claude", "sh", is_current_dir=True)

        # Verify preservation
        assert "Custom content" in features_md.read_text(encoding="utf-8")
        assert (project / ".claude").is_dir()
        assert (project / ".github").is_dir()


class TestQuickstartScenario4PartialCoreRepair:
    """Scenario 4: Incomplete .specify core is repaired safely."""

    def test_missing_core_files_are_created(self, monkeypatch, tmp_path: Path):
        resource_root = tmp_path / "resource"
        from fixtures.ai_tools_support import make_resource_with_skills

        make_resource_with_skills(resource_root)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        project = tmp_path / "partial"

        # Create only memory, no scripts/skills
        project.mkdir()
        (project / ".specify" / "memory").mkdir(parents=True)
        (project / ".specify" / "memory" / "features.md").write_text(
            "# Features", encoding="utf-8"
        )

        # Init with an assistant (use is_current_dir since project dir already exists)
        copy_local_templates(project, "qoder", "sh", is_current_dir=True)

        # Scripts and skills should now exist
        assert (project / ".specify" / "scripts").is_dir()
        assert (project / ".specify" / "skills").is_dir()
        # Memory should still contain original content
        features_content = (project / ".specify" / "memory" / "features.md").read_text(
            encoding="utf-8"
        )
        assert "# Features" in features_content


class TestQuickstartScenario6Idempotence:
    """Scenario 6: Repeat-run idempotence."""

    def test_double_init_does_not_create_duplicates(self, monkeypatch, tmp_path: Path):
        resource_root = tmp_path / "resource"
        from fixtures.ai_tools_support import make_resource_with_skills

        make_resource_with_skills(resource_root)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        project = tmp_path / "idem"

        # First init (copy_local_templates creates the dir)
        copy_local_templates(project, "copilot", "sh")

        # Record files
        first_files = sorted(
            str(p.relative_to(project)) for p in project.rglob("*") if p.is_file()
        )

        # Second init with same assistant (use is_current_dir=True for repeat run)
        copy_local_templates(project, "copilot", "sh", is_current_dir=True)

        second_files = sorted(
            str(p.relative_to(project)) for p in project.rglob("*") if p.is_file()
        )

        # The set of generated files should be the same (idempotent)
        assert set(first_files) == set(second_files), (
            f"File sets differ: added={set(second_files) - set(first_files)}"
        )
