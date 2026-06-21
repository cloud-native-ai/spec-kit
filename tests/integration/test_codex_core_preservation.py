"""Integration test for Codex CLI core preservation (T019).

Verifies re-init with --ai codex on existing project preserves .specify/ core files.
"""

import pytest

from pathlib import Path

from specify_cli import copy_local_templates

pytestmark = pytest.mark.integration


def test_reinit_codex_preserves_core_files(
    monkeypatch, tmp_path: Path, codex_minimal_resource_path: Path
):
    monkeypatch.setattr(
        "specify_cli.get_resource_path", lambda: codex_minimal_resource_path
    )

    project = tmp_path / "preserve"
    copy_local_templates(project, "codex", "sh")

    marker = project / ".specify" / "memory" / "user-data.md"
    marker.write_text("# User data", encoding="utf-8")

    copy_local_templates(project, "codex", "sh", is_current_dir=True)

    assert marker.exists(), ".specify/memory/user-data.md was overwritten"
    assert marker.read_text(encoding="utf-8") == "# User data"
