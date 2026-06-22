"""Unit tests for assistant profile uniqueness and official assistant list.

Validates that the assistant support matrix is complete, consistent, and
that each official assistant has a well-defined profile (Feature 022).
"""

import pytest

from specify_cli import (
    _OFFICIAL_ASSISTANT_KEYS,
    AGENT_CONFIG,
    get_assistant_profile,
    get_official_assistants,
)


class TestAssistantProfileUniqueness:
    def test_all_official_keys_are_in_agent_config(self):
        """Every official assistant key must have an AGENT_CONFIG entry."""
        for key in _OFFICIAL_ASSISTANT_KEYS:
            assert key in AGENT_CONFIG, (
                f"Official assistant '{key}' missing from AGENT_CONFIG"
            )

    def test_agent_config_folder_uniqueness(self):
        """Each assistant folder must be unique."""
        folders = [AGENT_CONFIG[k]["folder"] for k in _OFFICIAL_ASSISTANT_KEYS]
        assert len(folders) == len(set(folders)), (
            f"Duplicate folders detected: {folders}"
        )

    def test_agent_config_name_uniqueness(self):
        """Each assistant display name must be unique."""
        names = [AGENT_CONFIG[k]["name"] for k in _OFFICIAL_ASSISTANT_KEYS]
        assert len(names) == len(set(names)), (
            f"Duplicate display names detected: {names}"
        )

    def test_eight_official_assistants(self):
        """The official list must contain exactly 8 assistants."""
        assert len(_OFFICIAL_ASSISTANT_KEYS) == 8
        assert set(_OFFICIAL_ASSISTANT_KEYS) == {
            "copilot",
            "claude",
            "qwen",
            "opencode",
            "qoder",
            "codex",
            "hermes",
            "iflow",
        }

    def test_get_official_assistants_returns_correct_list(self):
        """get_official_assistants() returns the canonical ordered list."""
        result = get_official_assistants()
        assert result == _OFFICIAL_ASSISTANT_KEYS
        assert len(result) == 8


class TestAssistantProfile:
    def test_profile_has_required_fields(self):
        """Each profile must contain key metadata fields."""
        for key in _OFFICIAL_ASSISTANT_KEYS:
            profile = get_assistant_profile(key)
            assert "key" in profile
            assert profile["key"] == key
            assert "name" in profile or "display_name" in profile
            assert "folder" in profile
            assert "officially_supported" in profile
            assert profile["officially_supported"] is True

    def test_copilot_does_not_require_cli(self):
        profile = get_assistant_profile("copilot")
        assert profile.get("requires_cli") is False

    def test_claude_requires_cli(self):
        profile = get_assistant_profile("claude")
        assert profile.get("requires_cli") is True

    def test_unknown_key_raises_keyerror(self):
        with pytest.raises(KeyError):
            get_assistant_profile("nonexistent")

    def test_each_profile_has_command_directory(self):
        for key in _OFFICIAL_ASSISTANT_KEYS:
            profile = get_assistant_profile(key)
            assert profile.get("command_directory"), (
                f"Assistant '{key}' missing command_directory"
            )

    def test_each_profile_has_extension(self):
        for key in _OFFICIAL_ASSISTANT_KEYS:
            profile = get_assistant_profile(key)
            assert profile.get("command_format"), (
                f"Assistant '{key}' missing command_format"
            )
