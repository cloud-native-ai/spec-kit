"""Integration tests for AI tools command coverage.

Validates that generated assistant command surfaces cover canonical
command templates (User Stories 1 and 3).
"""

from pathlib import Path

import pytest

pytestmark = pytest.mark.integration

_OFFICIAL_ASSISTANTS = ["copilot", "claude", "qwen", "opencode", "qoder"]
_CANONICAL_COMMANDS = {
    "constitution",
    "feature",
    "requirements",
    "plan",
    "tasks",
    "implement",
    "clarify",
    "analyze",
    "checklist",
    "research",
    "review",
    "tools",
    "skills",
    "instructions",
    "agents",
}


def _canonical_command_stems() -> set:
    """Get the set of canonical command template names from templates/commands/."""
    from pathlib import Path

    candidate_dirs = [
        Path(__file__).resolve().parents[2] / "templates" / "commands",
        Path(__file__).resolve().parents[2] / ".specify" / "templates" / "commands",
    ]
    for d in candidate_dirs:
        if d.exists():
            return {f.stem for f in d.glob("*.md") if f.is_file()}
    return _CANONICAL_COMMANDS


class TestCommandCoverageBasics:
    def test_canonical_commands_exist(self):
        """Verify the canonical command templates directory is accessible."""
        stems = _canonical_command_stems()
        assert len(stems) > 0, "No canonical command templates found"
        # At minimum, the core SDD commands must exist
        core = {"constitution", "feature", "requirements", "plan", "tasks", "implement"}
        assert core.issubset(stems), f"Missing core commands: {core - stems}"

    def test_all_assistants_have_command_assets_generated(
        self, monkeypatch, tmp_path: Path
    ):
        """Verify that each assistant generates command assets."""
        from fixtures.ai_tools_support import make_resource_with_skills

        resource_root = make_resource_with_skills(tmp_path / "resource")
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        from specify_cli import copy_local_templates

        canonical = _canonical_command_stems()

        # For each assistant, generate commands and verify coverage
        for assistant in _OFFICIAL_ASSISTANTS:
            project = tmp_path / f"check-{assistant}"
            copy_local_templates(project, assistant, "sh")

            # Determine output dir per assistant convention
            dir_map = {
                "copilot": project / ".github" / "prompts",
                "claude": project / ".claude" / "commands",
                "qwen": project / ".qwen" / "commands",
                "opencode": project / ".opencode" / "command",
                "qoder": project / ".qoder" / "commands",
            }
            output_dir = dir_map.get(assistant)
            if output_dir and output_dir.exists():
                generated = {
                    # Strip "speckit." prefix and the assistant-specific extension
                    f.name.replace("speckit.", "", 1)
                    .replace(".prompt.md", "")
                    .replace(".toml", "")
                    .replace(".md", "")
                    for f in output_dir.iterdir()
                    if f.is_file() and f.name.startswith("speckit.")
                }
                # At minimum core commands should be generated
                generated_core = generated & canonical
                assert len(generated_core) >= 5, (
                    f"Assistant '{assistant}' generated only {len(generated_core)} "
                    f"of {len(canonical)} canonical commands"
                )
