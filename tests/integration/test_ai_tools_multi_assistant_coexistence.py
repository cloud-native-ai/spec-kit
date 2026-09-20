"""Integration tests for multi-assistant coexistence in one workspace.

Validates that every official AI tool can coexist in one project without
interfering with the others' assets (US3).

One test, driven off ``_OFFICIAL_ASSISTANT_KEYS``: a hand-picked three-assistant
subset of it asserted nothing the full set does not, and the per-root isolation it
also checked is asserted strictly (full file-set equality) by
``test_ai_tools_refresh_isolation.py``.
"""

from pathlib import Path

import pytest

pytestmark = pytest.mark.integration


class TestMultiAssistantCoexistence:
    def test_all_official_assistants_can_coexist(self, monkeypatch, tmp_path: Path):
        """Every official assistant should coexist in one workspace."""
        resource_root = tmp_path / "resource"
        from fixtures.ai_tools_support import make_resource_with_skills

        make_resource_with_skills(resource_root)
        monkeypatch.setattr("specify_cli.get_resource_path", lambda: resource_root)

        from specify_cli import _OFFICIAL_ASSISTANT_KEYS, copy_local_templates

        project = tmp_path / "all6"
        first = _OFFICIAL_ASSISTANT_KEYS[0]
        copy_local_templates(project, first, "sh")

        for assistant in _OFFICIAL_ASSISTANT_KEYS[1:]:
            copy_local_templates(project, assistant, "sh", is_current_dir=True)

        # All assistant roots must exist
        profile = {
            "copilot": ".github/",
            "claude": ".claude/",
            "opencode": ".opencode/",
            "qoder": ".qoder/",
            "codex": ".codex/",
            "hermes": ".hermes/",
        }
        for assistant in _OFFICIAL_ASSISTANT_KEYS:
            root_dir = project / profile[assistant]
            assert root_dir.is_dir(), f"{assistant} root {profile[assistant]} missing"

        # Six inits into one workspace must leave the shared core complete —
        # `templates/` included, which the per-assistant init tests do not assert
        # on a fresh workspace.
        assert (project / ".specify").is_dir()
        for core in ("memory", "scripts", "skills", "templates"):
            assert (project / ".specify" / core).is_dir(), f".specify/{core} missing"
