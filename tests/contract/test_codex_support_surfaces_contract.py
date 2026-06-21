"""Contract test for Codex CLI support surfaces (T017).

Validates that all canonical command stems exist under .codex/commands/ after init.
"""

import pytest

from pathlib import Path

from specify_cli import (
    copy_local_templates,
    get_canonical_command_stems,
    get_assistant_generated_commands,
)

pytestmark = pytest.mark.contract


def test_codex_commands_cover_all_canonical_stems(
    monkeypatch, tmp_path: Path, codex_minimal_resource_path: Path
):
    monkeypatch.setattr(
        "specify_cli.get_resource_path", lambda: codex_minimal_resource_path
    )

    canonical = get_canonical_command_stems()
    if not canonical:
        pytest.skip("No canonical command templates found in resource path")

    project = tmp_path / "codex_project"
    copy_local_templates(project, "codex", "sh")

    generated = get_assistant_generated_commands(project, "codex")
    canonical_set = set(canonical)
    generated_set = set(generated)

    missing = canonical_set - generated_set
    assert not missing, f"Codex missing commands: {missing}"
