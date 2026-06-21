"""Integration test for instructions sync (T047).

Verifies that _INSTRUCTIONS_FILE_MAP has entries for all Tier 1 tools.
"""

import pytest

from specify_cli import _OFFICIAL_ASSISTANT_KEYS, _ASSISTANT_TIERS

pytestmark = pytest.mark.integration


def test_instructions_file_map_has_tier1_tools():
    from specify_cli import _INSTRUCTIONS_FILE_MAP

    tier1_keys = [k for k, v in _ASSISTANT_TIERS.items() if v == "tier1"]
    for key in tier1_keys:
        assert key in _INSTRUCTIONS_FILE_MAP, (
            f"Tier 1 tool '{key}' missing from _INSTRUCTIONS_FILE_MAP"
        )
