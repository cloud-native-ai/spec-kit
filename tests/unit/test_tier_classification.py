"""Unit test for tier classification (T028).

Asserts _ASSISTANT_TIERS has exactly 6 entries, all Tier 1 keys are in
_OFFICIAL_ASSISTANT_KEYS, get_assistant_profile() returns valid tier field.
"""

from specify_cli import (
    _ASSISTANT_TIERS,
    _OFFICIAL_ASSISTANT_KEYS,
    get_assistant_profile,
)

TIER1_KEYS = {"claude", "codex", "qoder", "copilot", "opencode"}
TIER2_KEYS = {"qwen"}


def test_tiers_has_six_entries():
    assert len(_ASSISTANT_TIERS) == 6


def test_all_tier1_keys_in_official_list():
    for key in TIER1_KEYS:
        assert key in _OFFICIAL_ASSISTANT_KEYS, f"{key} not in official list"


def test_tier1_count_is_five():
    tier1 = [k for k, v in _ASSISTANT_TIERS.items() if v == "tier1"]
    assert len(tier1) == 5


def test_tier2_count_is_one():
    tier2 = [k for k, v in _ASSISTANT_TIERS.items() if v == "tier2"]
    assert len(tier2) == 1
    assert tier2[0] == "qwen"


def test_profile_tier_field_for_each_tool():
    for key in _OFFICIAL_ASSISTANT_KEYS:
        profile = get_assistant_profile(key)
        assert "tier" in profile, f"{key} missing tier field"
        assert profile["tier"] in ("tier1", "tier2"), f"{key} has invalid tier"


def test_tier1_tools_profile_tier():
    for key in TIER1_KEYS:
        profile = get_assistant_profile(key)
        assert profile["tier"] == "tier1", f"{key} should be tier1"


def test_qwen_is_tier2():
    profile = get_assistant_profile("qwen")
    assert profile["tier"] == "tier2"
