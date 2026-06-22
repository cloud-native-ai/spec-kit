"""Contract tests for Hermes Agent Tier 2 onboarding (Spec 019)."""

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


def test_hermes_in_agent_config_with_required_fields():
    assert "hermes" in AGENT_CONFIG
    assert AGENT_CONFIG["hermes"]["name"] == "Hermes Agent"
    assert AGENT_CONFIG["hermes"]["folder"] == ".hermes/"
    assert AGENT_CONFIG["hermes"]["requires_cli"] is True


def test_hermes_in_official_assistant_keys():
    assert "hermes" in _OFFICIAL_ASSISTANT_KEYS


def test_hermes_is_tier2():
    assert _ASSISTANT_TIERS["hermes"] == "tier2"


def test_hermes_in_skills_symlink_assistants():
    assert "hermes" in _SKILLS_SYMLINK_ASSISTANTS


def test_hermes_instructions_file_mapping():
    assert _INSTRUCTIONS_FILE_MAP["hermes"] == "HERMES.md"


def test_hermes_profile_is_complete():
    profile = get_assistant_profile("hermes")
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

    assert profile["key"] == "hermes"
    assert profile["tier"] == "tier2"
    assert profile["officially_supported"] is True
    assert profile["skills_symlink"] is True


def test_summary_reports_hermes_tier2_label():
    summary = InitializationResultSummary()
    summary.set_configured_assistants(["hermes"])

    assert summary.assistant_tiers["hermes"] == "tier2"
    assert "(Tier 2)" in summary.render_rich()
