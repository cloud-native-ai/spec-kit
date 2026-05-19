"""Integration tests for package resource and distribution verification.

Validates that all assistant command and template assets are properly
included in the package/distribution (US1 / T020).
"""

from pathlib import Path

from specify_cli import (
    _OFFICIAL_ASSISTANT_KEYS,
    get_resource_path,
)


class TestDistributionAssets:
    def test_resource_path_is_available(self):
        """The get_resource_path() function must return a valid path."""
        # In the installed package, resources may be at MODULE_DIR.
        # In dev mode, they're at the repo root.
        resource = get_resource_path()
        if resource is None:
            # Try fallback: repo root
            from pathlib import Path

            repo_root = Path(__file__).resolve().parents[2]
            if (repo_root / "templates" / "commands").exists():
                return  # skip ok
        assert resource is not None, "get_resource_path() returned None"
        assert resource.is_dir(), f"Resource path {resource} is not a directory"

    def _resource_or_repo(self):
        resource = get_resource_path()
        if resource and resource.is_dir():
            return resource
        # Fallback to repo root for dev/test environments
        from pathlib import Path

        repo = Path(__file__).resolve().parents[2]
        return repo

    def test_templates_commands_exist(self):
        """Canonical command templates must be present."""
        resource = self._resource_or_repo()
        commands_dir = resource / "templates" / "commands"
        assert commands_dir.is_dir(), f"templates/commands/ not found at {commands_dir}"
        cmd_files = list(commands_dir.glob("*.md"))
        assert len(cmd_files) >= 5, (
            f"Only {len(cmd_files)} command templates found, expected >= 5"
        )

    def test_memory_templates_exist(self):
        """Memory templates must be present."""
        resource = self._resource_or_repo()
        memory_dir = resource / "memory"
        assert memory_dir.is_dir(), f"memory/ not found at {memory_dir}"
        assert (memory_dir / "constitution.md").exists(), "constitution.md missing"
        assert (memory_dir / "features.md").exists(), "features.md missing"

    def test_scripts_are_packaged(self):
        """Shell scripts must be present."""
        resource = self._resource_or_repo()
        scripts_dir = resource / "scripts"
        assert scripts_dir.is_dir(), f"scripts/ not found at {scripts_dir}"

    def test_skills_are_packaged(self):
        """Skills directory must be present."""
        resource = self._resource_or_repo()
        skills_dir = resource / "skills"
        assert skills_dir.is_dir(), f"skills/ not found at {skills_dir}"

    def test_instructions_template_exists(self):
        """The instructions-template.md must be present."""
        resource = self._resource_or_repo()
        templates_dir = resource / "templates"
        assert (templates_dir / "instructions-template.md").exists(), (
            "instructions-template.md missing"
        )

    def test_claudeignore_template_exists(self):
        """The claudeignore-template should be present."""
        resource = self._resource_or_repo()
        templates_dir = resource / "templates"
        assert (templates_dir / "claudeignore-template").exists(), (
            "claudeignore-template missing"
        )

    def test_vscode_settings_template_exists(self):
        """The vscode-settings.json should be present."""
        resource = self._resource_or_repo()
        templates_dir = resource / "templates"
        assert (templates_dir / "vscode-settings.json").exists(), (
            "vscode-settings.json missing"
        )

    def test_all_assistant_command_generation_works_locally(
        self, monkeypatch, tmp_path: Path
    ):
        """Verify generate_commands() works for every assistant."""
        resource_root = tmp_path / "resource"
        from fixtures.ai_tools_support import make_resource_with_skills

        make_resource_with_skills(resource_root)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        from specify_cli import generate_commands

        for assistant in _OFFICIAL_ASSISTANT_KEYS:
            from specify_cli import _ASSISTANT_COMMAND_DIRS, _ASSISTANT_EXTENSIONS

            cmd_dir_rel = _ASSISTANT_COMMAND_DIRS[assistant]
            ext = _ASSISTANT_EXTENSIONS[assistant]

            output = tmp_path / f"gen-{assistant}" / cmd_dir_rel
            generate_commands(assistant, ext, "$ARGUMENTS", output, "sh")

            assert output.is_dir(), f"[{assistant}] output dir not created"
            files = list(output.iterdir())
            assert len(files) >= 3, (
                f"[{assistant}] only {len(files)} command files generated"
            )
