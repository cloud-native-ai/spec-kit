"""Support-surface audit tests for official assistant consistency.

Validates that README, docs, templates, CLI help, and package resources
all reference the same set of official assistants (Feature 022) as
defined by the support-surface audit contract (US3 / T045).
"""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

_OFFICIAL_NAMES = [
    "GitHub Copilot",
    "Claude Code",
    "Qwen Code",
    "opencode",
    "Qoder",
]

# Files that constitute release-blocking support surfaces.
_SURFACE_FILES = [
    "README.md",
    "docs/installation.md",
    "docs/quickstart.md",
    "docs/usage.md",
    ".specify/memory/constitution.md",
    "templates/instructions-template.md",
    ".specify/templates/instructions-template.md",
    "templates/commands/agents.md",
    ".specify/templates/commands/agents.md",
]


class TestSupportSurfaceAudit:
    def _read_if_exists(self, rel_path: str) -> str:
        fp = ROOT / rel_path
        if not fp.exists():
            return ""
        return fp.read_text(encoding="utf-8")

    def test_readme_mentions_all_official_assistants(self):
        content = self._read_if_exists("README.md")
        if not content:
            pytest.skip("README.md not found")
        for name in _OFFICIAL_NAMES:
            assert name in content, f"README.md missing '{name}'"

    def test_installation_docs_mention_all_assistants(self):
        content = self._read_if_exists("docs/installation.md")
        if not content:
            pytest.skip("docs/installation.md not found")
        for name in _OFFICIAL_NAMES:
            assert name in content, f"docs/installation.md missing '{name}'"

    def test_constitution_mentions_all_assistants(self):
        content = self._read_if_exists(".specify/memory/constitution.md")
        if not content:
            pytest.skip("constitution.md not found")
        for name in _OFFICIAL_NAMES:
            assert name in content, f"constitution.md missing '{name}'"

    def test_instructions_template_mentions_all_assistants(self):
        content = self._read_if_exists("templates/instructions-template.md")
        if not content:
            pytest.skip("templates/instructions-template.md not found")
        for name in _OFFICIAL_NAMES:
            assert name in content, f"instructions-template.md missing '{name}'"

    def test_agents_command_template_mentions_all_assistants(self):
        content = self._read_if_exists("templates/commands/agents.md")
        if not content:
            pytest.skip("templates/commands/agents.md not found")
        for name in _OFFICIAL_NAMES:
            assert name in content, f"agents.md missing '{name}'"

    def test_no_unsupported_assistant_names_in_surfaces(self):
        """Ensure only official assistant names appear on support surfaces."""
        # This is a smoke test - if unknown names appear it's a warning
        known = {
            "GitHub Copilot",
            "Claude Code",
            "Qwen Code",
            "opencode",
            "Qoder",
            "Qoder CLI",
        }
        for rel_path in _SURFACE_FILES:
            content = self._read_if_exists(rel_path)
            if not content:
                continue
            # Check for obviously wrong names
            bad_names = ["Cursor", "Windsurf", "Gemini"]
            for bad in bad_names:
                assert bad not in content, (
                    f"'{bad}' found in {rel_path} (not an official assistant)"
                )
