"""Contract test for tier ordering (T029).

Asserts _OFFICIAL_ASSISTANT_KEYS lists Tier 1 CLI tools before Tier 2
tools, and README mentions tiers.
"""

from pathlib import Path

import pytest

from specify_cli import _ASSISTANT_TIERS, _OFFICIAL_ASSISTANT_KEYS

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]


def test_tier1_tools_before_tier2_in_keys():
    tier2_indexes = [
        i for i, key in enumerate(_OFFICIAL_ASSISTANT_KEYS) if _ASSISTANT_TIERS[key] == "tier2"
    ]
    assert tier2_indexes, "expected at least one tier2 tool"
    first_tier2 = min(tier2_indexes)
    for key in _OFFICIAL_ASSISTANT_KEYS[:first_tier2]:
        assert _ASSISTANT_TIERS[key] == "tier1", (
            f"{key} appears before tier2 tools but is not tier1"
        )


def test_official_keys_are_supported_tools_only():
    assert set(_OFFICIAL_ASSISTANT_KEYS) == set(_ASSISTANT_TIERS)


def test_official_assistant_count_is_six():
    assert len(_OFFICIAL_ASSISTANT_KEYS) == 6


def test_tier1_tools_are_cli_form():
    tier1 = [k for k in _OFFICIAL_ASSISTANT_KEYS if _ASSISTANT_TIERS[k] == "tier1"]
    assert tier1 == ["claude", "codex", "qoder", "opencode"]


def test_readme_mentions_tier():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Tier 1" in readme
    assert "Tier 2" in readme
    assert "Codex CLI" in readme
    assert "Hermes Agent" in readme
