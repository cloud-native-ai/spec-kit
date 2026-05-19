"""Integration tests for core workspace preservation during assistant addition.

Validates that existing initialized .specify assets are preserved when
adding additional AI assistants to a workspace (User Story 2).
"""

from pathlib import Path

import pytest

pytestmark = pytest.mark.integration


def _mock_resource_path_with_commands(tmp_path: Path) -> Path:
    """Create a minimal resource root for test."""
    from fixtures.ai_tools_support import make_resource_with_skills

    return make_resource_with_skills(tmp_path / "resource")


class TestCorePreservationDuringAssistantAddition:
    """Tests that adding a second assistant preserves existing .specify content."""

    def test_modified_features_md_is_preserved(self, monkeypatch, tmp_path: Path):
        """Adding an assistant should not overwrite an already-modified features.md."""
        resource_root = _mock_resource_path_with_commands(tmp_path)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        from specify_cli import copy_local_templates

        project = tmp_path / "workspace"
        project.mkdir()

        # Initialize with copilot first
        copy_local_templates(project, "copilot", "sh")

        # Verify features.md exists
        features_path = project / ".specify" / "memory" / "features.md"
        assert features_path.exists()

        # Modify features.md with user content
        custom_content = "# Custom Features\n\nUser-modified content.\n"
        features_path.write_text(custom_content, encoding="utf-8")

        # Now add claude as second assistant
        copy_local_templates(project, "claude", "sh")

        # Verify features.md was preserved (not overwritten)
        preserved = features_path.read_text(encoding="utf-8")
        assert preserved == custom_content, (
            f"features.md was overwritten. Expected custom content, got: {preserved[:100]}"
        )

    def test_modified_instructions_md_is_preserved(self, monkeypatch, tmp_path: Path):
        """Adding an assistant should preserve user-modified instructions.md."""
        resource_root = _mock_resource_path_with_commands(tmp_path)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        from specify_cli import copy_local_templates

        project = tmp_path / "workspace"
        project.mkdir()

        # Initialize with copilot first
        copy_local_templates(project, "copilot", "sh")

        # instructions.md may need to be created during init - check common paths
        maybe_instructions = [
            project / ".specify" / "instructions.md",
            project / ".github" / "copilot-instructions.md",
            project / "CLAUDE.md",
        ]
        for p in maybe_instructions:
            if p.exists():
                p.write_text("# Custom Instructions", encoding="utf-8")
                break
        else:
            # Create one if none exists
            instr_path = project / ".specify" / "instructions.md"
            instr_path.parent.mkdir(parents=True, exist_ok=True)
            instr_path.write_text("# Custom Instructions", encoding="utf-8")

        # Now add claude
        copy_local_templates(project, "claude", "sh")

        # Verify custom instructions are still present
        for p in maybe_instructions:
            if p.exists():
                content = p.read_text(encoding="utf-8")
                assert "Custom Instructions" in content, (
                    f"Custom instructions were overwritten in {p.name}"
                )
                break

    def test_existing_assistant_assets_remain_after_second_init(
        self, monkeypatch, tmp_path: Path
    ):
        """Adding a second assistant must not remove the first assistant's assets."""
        resource_root = _mock_resource_path_with_commands(tmp_path)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        from specify_cli import copy_local_templates

        project = tmp_path / "workspace"
        project.mkdir()

        # Initialize with copilot
        copy_local_templates(project, "copilot", "sh")
        assert (project / ".github").exists()
        assert (project / ".specify").exists()

        # Record files present after first init
        first_run_files = sorted(
            str(p.relative_to(project)) for p in project.rglob("*") if p.is_file()
        )

        # Add claude as second assistant
        copy_local_templates(project, "claude", "sh")

        # Verify copilot assets still exist
        assert (project / ".github").exists(), "Copilot .github/ was removed"
        assert (project / ".specify").exists(), ".specify/ was removed"

        # Verify claude assets were added
        assert (project / ".claude").exists(), "Claude .claude/ was not created"
