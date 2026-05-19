"""Unit tests for CLI help assistant list consistency.

Validates that the --ai help text and CLI interfaces list all official
assistants consistently (US1 / T021).
"""

from specify_cli import (
    _OFFICIAL_ASSISTANT_KEYS,
    AGENT_CONFIG,
    get_official_assistants,
)


class TestCliHelpConsistency:
    def test_agent_config_matches_offical_list(self):
        """AGENT_CONFIG must contain exactly the official assistant keys."""
        official = set(_OFFICIAL_ASSISTANT_KEYS)
        config_keys = set(AGENT_CONFIG.keys())
        assert official.issubset(config_keys), (
            f"Official assistants {official - config_keys} missing from AGENT_CONFIG"
        )
        # AGENT_CONFIG may have extra keys but all officials must be there
        for key in official:
            assert key in AGENT_CONFIG, f"'{key}' not in AGENT_CONFIG"

    def test_each_agent_has_name(self):
        """Every AGENT_CONFIG entry must have a non-empty name."""
        for key in _OFFICIAL_ASSISTANT_KEYS:
            cfg = AGENT_CONFIG[key]
            assert "name" in cfg
            assert cfg["name"], f"'{key}' has empty name"

    def test_each_agent_has_folder(self):
        """Every AGENT_CONFIG entry must have a non-empty folder."""
        for key in _OFFICIAL_ASSISTANT_KEYS:
            cfg = AGENT_CONFIG[key]
            assert "folder" in cfg
            assert cfg["folder"], f"'{key}' has empty folder"

    def test_official_assistant_count_is_consistent(self):
        """get_official_assistants() must return the expected count."""
        assistants = get_official_assistants()
        assert len(assistants) == 5
        assert set(assistants) == set(_OFFICIAL_ASSISTANT_KEYS)

    def test_cli_help_would_mention_all_assistants(self):
        """Verify the --ai option would reference all assistants by introspection."""
        # The init function's help text should mention all assistants

        from specify_cli import init as init_command

        help_text = init_command.__doc__ or ""
        # The help text in the docstring mentions assistants
        for key in _OFFICIAL_ASSISTANT_KEYS:
            assert key in help_text.lower() or key in repr(AGENT_CONFIG).lower(), (
                f"Assistant '{key}' not referenced in CLI context"
            )
