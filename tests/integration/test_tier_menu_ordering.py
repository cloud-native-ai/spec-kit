"""Integration test for init menu ordering (T031).

Verifies that the interactive menu displays Tier 1 tools first.
"""

import pytest

from specify_cli import _OFFICIAL_ASSISTANT_KEYS, _ASSISTANT_TIERS, AGENT_CONFIG

pytestmark = pytest.mark.integration


def test_menu_displays_tier1_first():
    """Tier 1 tools should appear before Tier 2 in _OFFICIAL_ASSISTANT_KEYS."""
    seen_tier2 = False
    for key in _OFFICIAL_ASSISTANT_KEYS:
        tier = _ASSISTANT_TIERS.get(key, "tier2")
        if tier == "tier2":
            seen_tier2 = True
        elif seen_tier2:
            pytest.fail(
                f"Tier 1 tool '{key}' appears after Tier 2 tool in menu order"
            )


def test_all_official_keys_in_agent_config():
    for key in _OFFICIAL_ASSISTANT_KEYS:
        assert key in AGENT_CONFIG, f"{key} missing from AGENT_CONFIG"


def test_ai_choices_dict_has_all_tools():
    ai_choices = {key: config["name"] for key, config in AGENT_CONFIG.items()}
    for key in _OFFICIAL_ASSISTANT_KEYS:
        assert key in ai_choices
