"""Integration tests for instruction preservation during assistant addition/refresh.

Validates that user-modified .specify/instructions.md and compatibility
instruction files are preserved when adding/refreshing assistants (US2).
"""

from pathlib import Path

import pytest

pytestmark = pytest.mark.integration


class TestInstructionPreservation:
    def test_specify_instructions_preserved_on_second_assistant(
        self, monkeypatch, tmp_path: Path
    ):
        """Adding a second assistant must not overwrite .specify/instructions.md."""
        resource_root = tmp_path / "resource"
        from fixtures.ai_tools_support import make_resource_with_skills

        make_resource_with_skills(resource_root)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        from specify_cli import copy_local_templates

        project = tmp_path / "workspace"
        copy_local_templates(project, "copilot", "sh")

        # Create user-customized instructions
        instr_path = project / ".specify" / "instructions.md"
        instr_path.parent.mkdir(parents=True, exist_ok=True)
        instr_path.write_text(
            "# Custom AI Instructions\n\nUser specific content.", encoding="utf-8"
        )

        # Add claude assistant
        copy_local_templates(project, "claude", "sh", is_current_dir=True)

        # Verify instructions preserved
        content = instr_path.read_text(encoding="utf-8")
        assert "Custom AI Instructions" in content
        assert "User specific content" in content

    def test_copilot_instructions_preserved_on_assistant_add(
        self, monkeypatch, tmp_path: Path
    ):
        """Adding a second assistant must not overwrite .github/copilot-instructions.md."""
        resource_root = tmp_path / "resource"
        from fixtures.ai_tools_support import make_resource_with_skills

        make_resource_with_skills(resource_root)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        from specify_cli import copy_local_templates

        project = tmp_path / "workspace"
        copy_local_templates(project, "copilot", "sh")

        # Create user-customized copilot instructions
        instr_path = project / ".github" / "copilot-instructions.md"
        instr_path.parent.mkdir(parents=True, exist_ok=True)
        instr_path.write_text(
            "# Custom Copilot Instructions\n\nDo not override.", encoding="utf-8"
        )

        # Add qoder
        copy_local_templates(project, "qoder", "sh", is_current_dir=True)

        # Verify copilot instructions preserved
        assert instr_path.exists()
        content = instr_path.read_text(encoding="utf-8")
        assert "Do not override" in content

    def test_multiple_compatibility_files_preserved(self, monkeypatch, tmp_path: Path):
        """When multiple compatibility instruction files exist, all must survive."""
        resource_root = tmp_path / "resource"
        from fixtures.ai_tools_support import make_resource_with_skills

        make_resource_with_skills(resource_root)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        from specify_cli import copy_local_templates

        project = tmp_path / "workspace"
        copy_local_templates(project, "copilot", "sh")

        # Create several compatibility instruction files
        files = {
            ".github/copilot-instructions.md": "# Copilot rules",
            "CLAUDE.md": "# Claude rules",
        }
        for path, content in files.items():
            f = project / path
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(content, encoding="utf-8")

        # Add claude - should not overwrite CLAUDE.md
        copy_local_templates(project, "claude", "sh", is_current_dir=True)

        # Verify all files preserved
        for path, expected in files.items():
            f = project / path
            actual = f.read_text(encoding="utf-8") if f.exists() else ""
            assert expected in actual, f"{path} was not preserved"
