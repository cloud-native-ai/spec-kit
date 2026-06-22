"""Integration tests for new-project initialization across all official assistants.

Validates that every official AI tool can initialize a new Spec Kit workspace
with complete core assets and assistant-specific command/guidance assets (US1).
"""

from pathlib import Path

import pytest

from specify_cli import (
    _OFFICIAL_ASSISTANT_KEYS,
    copy_local_templates,
    get_assistant_profile,
)

pytestmark = pytest.mark.integration


def _extensions_for(assistant: str) -> list:
    """Return the expected file extensions for a given assistant."""
    ext_map = {
        "copilot": ".prompt.md",
        "claude": ".md",
        "qwen": ".toml",
        "opencode": ".md",
        "qoder": ".md",
        "codex": ".md",
        "hermes": ".md",
        "iflow": ".md",
    }
    return [ext_map.get(assistant, ".md")]


class TestAllAssistantsInit:
    def test_each_assistant_creates_core_specify(self, monkeypatch, tmp_path: Path):
        """Initialize a new project for each assistant and verify .specify exists."""

        resource_root = tmp_path / "resource"
        from fixtures.ai_tools_support import make_resource_with_skills

        make_resource_with_skills(resource_root)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        for assistant in _OFFICIAL_ASSISTANT_KEYS:
            project = tmp_path / f"init-{assistant}"
            copy_local_templates(project, assistant, "sh")

            # Core .specify must exist
            assert (project / ".specify").is_dir(), (
                f"[{assistant}] .specify/ not created"
            )

            # Core memory must exist
            assert (project / ".specify" / "memory").is_dir(), (
                f"[{assistant}] .specify/memory/ not created"
            )

            # Core scripts must exist
            assert (project / ".specify" / "scripts").is_dir(), (
                f"[{assistant}] .specify/scripts/ not created"
            )

            # Core skills must exist
            assert (project / ".specify" / "skills").is_dir(), (
                f"[{assistant}] .specify/skills/ not created"
            )

    def test_each_assistant_creates_its_own_command_dir(
        self, monkeypatch, tmp_path: Path
    ):
        """Each assistant should have its own command/directories created."""
        resource_root = tmp_path / "resource"
        from fixtures.ai_tools_support import make_resource_with_skills

        make_resource_with_skills(resource_root)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        for assistant in _OFFICIAL_ASSISTANT_KEYS:
            project = tmp_path / f"cmds-{assistant}"
            copy_local_templates(project, assistant, "sh")

            profile = get_assistant_profile(assistant)
            folder = profile["folder"]

            # The assistant root folder must exist
            assert (project / folder).is_dir(), (
                f"[{assistant}] assistant root {folder} not created"
            )

    def test_assistant_specific_command_files_are_generated(
        self, monkeypatch, tmp_path: Path
    ):
        """Generated command files should exist for each assistant."""
        resource_root = tmp_path / "resource"
        from fixtures.ai_tools_support import make_resource_with_skills

        make_resource_with_skills(resource_root)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        for assistant in _OFFICIAL_ASSISTANT_KEYS:
            project = tmp_path / f"gen-{assistant}"
            copy_local_templates(project, assistant, "sh")

            profile = get_assistant_profile(assistant)
            cmd_dir_rel = profile["command_directory"]
            cmd_dir = project / cmd_dir_rel

            assert cmd_dir.is_dir(), (
                f"[{assistant}] command directory {cmd_dir_rel} not created"
            )

            # At least a few command files should exist
            cmd_files = list(cmd_dir.iterdir())
            assert len(cmd_files) >= 3, (
                f"[{assistant}] only {len(cmd_files)} command files in {cmd_dir_rel}"
            )

            # Check they are speckit.* files
            speckit_files = [f for f in cmd_files if f.name.startswith("speckit.")]
            assert len(speckit_files) >= 3, (
                f"[{assistant}] only {len(speckit_files)} speckit.* files generated"
            )
