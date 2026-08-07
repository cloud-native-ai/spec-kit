"""Unit test for command template variant generation (T044).

Assert each Tier 1 tool generates files with correct arg_format.
"""

from specify_cli import _ASSISTANT_TIERS, _ASSISTANT_ARG_FORMATS


def test_tier1_tools_use_dollar_arguments():
    tier1_keys = [k for k, v in _ASSISTANT_TIERS.items() if v == "tier1"]
    for key in tier1_keys:
        assert _ASSISTANT_ARG_FORMATS[key] == "$ARGUMENTS", (
            f"Tier 1 tool {key} should use $ARGUMENTS, got {_ASSISTANT_ARG_FORMATS[key]}"
        )


def test_all_tools_use_dollar_arguments():
    for key in _ASSISTANT_ARG_FORMATS:
        assert _ASSISTANT_ARG_FORMATS[key] == "$ARGUMENTS", (
            f"Tool {key} should use $ARGUMENTS, got {_ASSISTANT_ARG_FORMATS[key]}"
        )
