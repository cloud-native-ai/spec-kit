"""Contract test for tier ordering (T029).

Asserts _OFFICIAL_ASSISTANT_KEYS lists Tier 1 tools before qwen,
and README mentions tiers.
"""

from pathlib import Path

import pytest

from specify_cli import _ASSISTANT_TIERS, _OFFICIAL_ASSISTANT_KEYS

pytestmark = pytest.mark.contract

ROOT = Path(__file__).resolve().parents[2]


def test_tier1_tools_before_qwen_in_keys():
    qwen_index = _OFFICIAL_ASSISTANT_KEYS.index("qwen")
    for key in _OFFICIAL_ASSISTANT_KEYS[:qwen_index]:
        assert _ASSISTANT_TIERS[key] == "tier1", (
            f"{key} appears before qwen but is not tier1"
        )


def test_qwen_is_last_in_official_keys():
    assert _OFFICIAL_ASSISTANT_KEYS == [
        "claude",
        "codex",
        "qoder",
        "copilot",
        "opencode",
        "qwen",
        "hermes",
        "iflow",
    ]


def test_official_assistant_count_is_eight():
    assert len(_OFFICIAL_ASSISTANT_KEYS) == 8


def test_readme_mentions_tier():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Tier 1" in readme
    assert "Tier 2" in readme
    assert "Codex CLI" in readme
    assert "Hermes Agent" in readme
    assert "iFlow" in readme
