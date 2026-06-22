"""Contract tests for iFlow Tier 2 onboarding (Spec 019)."""

import pytest

from specify_cli import (
    _ASSISTANT_TIERS,
    _INSTRUCTIONS_FILE_MAP,
    _OFFICIAL_ASSISTANT_KEYS,
    _SKILLS_SYMLINK_ASSISTANTS,
    AGENT_CONFIG,
    InitializationResultSummary,
    get_assistant_profile,
)

pytestmark = pytest.mark.contract


def test_iflow_in_agent_config_with_required_fields():
    assert "iflow" in AGENT_CONFIG
    assert AGENT_CONFIG["iflow"]["name"] == "iFlow"
    assert AGENT_CONFIG["iflow"]["folder"] == ".iflow/"
    assert AGENT_CONFIG["iflow"]["requires_cli"] is True


def test_iflow_in_official_assistant_keys():
    assert "iflow" in _OFFICIAL_ASSISTANT_KEYS


def test_iflow_is_tier2():
    assert _ASSISTANT_TIERS["iflow"] == "tier2"


def test_iflow_in_skills_symlink_assistants():
    assert "iflow" in _SKILLS_SYMLINK_ASSISTANTS


def test_iflow_instructions_file_mapping():
    assert _INSTRUCTIONS_FILE_MAP["iflow"] == "IFLOW.md"


def test_iflow_profile_is_complete():
    profile = get_assistant_profile("iflow")
    for field in [
        "key",
        "name",
        "folder",
        "install_url",
        "requires_cli",
        "command_directory",
        "command_format",
        "arg_format",
        "officially_supported",
        "tier",
        "skills_symlink",
    ]:
        assert field in profile

    assert profile["key"] == "iflow"
    assert profile["tier"] == "tier2"
    assert profile["officially_supported"] is True
    assert profile["skills_symlink"] is True


def test_summary_reports_iflow_tier2_label():
    summary = InitializationResultSummary()
    summary.set_configured_assistants(["iflow"])

    assert summary.assistant_tiers["iflow"] == "tier2"
    assert "(Tier 2)" in summary.render_rich()
