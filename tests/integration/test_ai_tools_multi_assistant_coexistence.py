"""Integration tests for multi-assistant coexistence in one workspace.

Validates that three or more AI tools can coexist in one project without
interfering with each other's assets (US3).
"""

from pathlib import Path

import pytest

pytestmark = pytest.mark.integration

_THREE_ASSISTANTS = ["copilot", "claude", "qwen"]


class TestMultiAssistantCoexistence:
    def test_three_assistants_can_coexist(self, monkeypatch, tmp_path: Path):
        """Three assistants should be configurable in one workspace."""
        resource_root = tmp_path / "resource"
        from fixtures.ai_tools_support import make_resource_with_skills

        make_resource_with_skills(resource_root)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        from specify_cli import copy_local_templates

        project = tmp_path / "multi"
        copy_local_templates(project, "copilot", "sh")

        # Add second
        copy_local_templates(project, "claude", "sh", is_current_dir=True)
        # Add third
        copy_local_templates(project, "qwen", "sh", is_current_dir=True)

        # All three assistant roots must exist
        assert (project / ".github").is_dir(), ".github/ missing"
        assert (project / ".claude").is_dir(), ".claude/ missing"
        assert (project / ".qwen").is_dir(), ".qwen/ missing"

        # .specify must exist with full core
        assert (project / ".specify").is_dir()
        assert (project / ".specify" / "memory").is_dir()
        assert (project / ".specify" / "scripts").is_dir()
        assert (project / ".specify" / "skills").is_dir()
        assert (project / ".specify" / "templates").is_dir()

    def test_five_assistants_can_coexist(self, monkeypatch, tmp_path: Path):
        """All five official assistants should coexist in one workspace."""
        resource_root = tmp_path / "resource"
        from fixtures.ai_tools_support import make_resource_with_skills

        make_resource_with_skills(resource_root)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        from specify_cli import _OFFICIAL_ASSISTANT_KEYS, copy_local_templates

        project = tmp_path / "all5"
        first = _OFFICIAL_ASSISTANT_KEYS[0]
        copy_local_templates(project, first, "sh")

        for assistant in _OFFICIAL_ASSISTANT_KEYS[1:]:
            copy_local_templates(project, assistant, "sh", is_current_dir=True)

        # All five roots must exist
        for assistant in _OFFICIAL_ASSISTANT_KEYS:
            profile = {
                "copilot": ".github/",
                "claude": ".claude/",
                "qwen": ".qwen/",
                "opencode": ".opencode/",
                "qoder": ".qoder/",
            }
            root_dir = project / profile[assistant]
            assert root_dir.is_dir(), f"{assistant} root {profile[assistant]} missing"

    def test_adding_assistant_does_not_affect_other_roots(
        self, monkeypatch, tmp_path: Path
    ):
        """Adding a new assistant must not modify other assistant roots."""
        resource_root = tmp_path / "resource"
        from fixtures.ai_tools_support import make_resource_with_skills

        make_resource_with_skills(resource_root)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        from specify_cli import copy_local_templates

        project = tmp_path / "isolated"
        copy_local_templates(project, "copilot", "sh")
        copy_local_templates(project, "claude", "sh", is_current_dir=True)

        # Snapshot claude root
        claude_files_before = sorted(
            str(p.relative_to(project))
            for p in (project / ".claude").rglob("*")
            if p.is_file()
        )

        # Add qwen
        copy_local_templates(project, "qwen", "sh", is_current_dir=True)

        claude_files_after = sorted(
            str(p.relative_to(project))
            for p in (project / ".claude").rglob("*")
            if p.is_file()
        )

        # Claude files unchanged
        for f in claude_files_before:
            assert f in claude_files_after, f"Claude file {f} was removed"

        # No new unexpected files in claude root
        assert len(claude_files_before) == len(claude_files_after), (
            f"Claude root changed: {len(claude_files_before)} -> {len(claude_files_after)}"
        )
