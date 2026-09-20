"""Unit test for tier classification (T028).

Asserts that the tier assignment covers exactly the official assistants, that
``get_assistant_profile()`` exposes a valid ``tier`` for each of them, and that the
CLI-form tools are the ones classified Tier 1.

Deliberately free of count pins: ``len(_ASSISTANT_TIERS) == 6`` and
``len(tier1) == 4`` broke every time an assistant was legitimately added (see the
recorded failure of ``test_tiers_has_six_entries`` in
``.specify/memory/feedback/last-regression-failed.txt``), while catching nothing that
the derived set equalities below miss. ``test_ai_tools_support_matrix.py`` owns the
authoritative pin of the official assistant roster itself.
"""

from specify_cli import (
    _ASSISTANT_TIERS,
    _OFFICIAL_ASSISTANT_KEYS,
    get_assistant_profile,
)

TIER1_KEYS = {"claude", "codex", "qoder", "opencode"}
TIER2_KEYS = {"hermes", "copilot"}


def test_tier_assignment_covers_exactly_the_official_assistants():
    """Every official assistant has a tier entry, and no stray key does.

    Derived rather than counted, so a seventh official assistant does not break it —
    but a tier entry for a key that is not official (dead config), or a missing entry
    for one that is, does.
    """
    assert set(_ASSISTANT_TIERS) == set(_OFFICIAL_ASSISTANT_KEYS)
    tier2 = {k for k, v in _ASSISTANT_TIERS.items() if v == "tier2"}
    assert tier2 == TIER2_KEYS


def test_profile_tier_field_for_each_tool():
    for key in _OFFICIAL_ASSISTANT_KEYS:
        profile = get_assistant_profile(key)
        assert "tier" in profile, f"{key} missing tier field"
        assert profile["tier"] in ("tier1", "tier2"), f"{key} has invalid tier"


def test_tier1_tools_profile_tier():
    for key in TIER1_KEYS:
        profile = get_assistant_profile(key)
        assert profile["tier"] == "tier1", f"{key} should be tier1"
