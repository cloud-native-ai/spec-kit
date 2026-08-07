"""Unit test for tier classification (T028).

Asserts _ASSISTANT_TIERS classifies 4 CLI tools as Tier 1 and 2 non-CLI
tools as Tier 2, all keys are in _OFFICIAL_ASSISTANT_KEYS, and
get_assistant_profile() returns a valid tier field.
"""

from specify_cli import (
    _ASSISTANT_TIERS,
    _OFFICIAL_ASSISTANT_KEYS,
    get_assistant_profile,
)

TIER1_KEYS = {"claude", "codex", "qoder", "opencode"}
TIER2_KEYS = {"hermes", "copilot"}


def test_tiers_has_six_entries():
    assert len(_ASSISTANT_TIERS) == 6


def test_all_tier_keys_in_official_list():
    for key in TIER1_KEYS | TIER2_KEYS:
        assert key in _OFFICIAL_ASSISTANT_KEYS, f"{key} not in official list"


def test_tier1_count_is_four():
    tier1 = [k for k, v in _ASSISTANT_TIERS.items() if v == "tier1"]
    assert len(tier1) == 4


def test_tier2_count_is_two():
    tier2 = [k for k, v in _ASSISTANT_TIERS.items() if v == "tier2"]
    assert len(tier2) == 2
    assert set(tier2) == TIER2_KEYS


def test_profile_tier_field_for_each_tool():
    for key in _OFFICIAL_ASSISTANT_KEYS:
        profile = get_assistant_profile(key)
        assert "tier" in profile, f"{key} missing tier field"
        assert profile["tier"] in ("tier1", "tier2"), f"{key} has invalid tier"


def test_tier1_tools_profile_tier():
    for key in TIER1_KEYS:
        profile = get_assistant_profile(key)
        assert profile["tier"] == "tier1", f"{key} should be tier1"


def test_copilot_is_tier2():
    profile = get_assistant_profile("copilot")
    assert profile["tier"] == "tier2"
