"""Contract tests for Codex CLI assistant profile (T016).

Validates that codex is registered in AGENT_CONFIG, _OFFICIAL_ASSISTANT_KEYS,
and that get_assistant_profile returns the expected profile shape.
"""

from pathlib import Path

from specify_cli import (
    AGENT_CONFIG,
    _OFFICIAL_ASSISTANT_KEYS,
    get_assistant_profile,
)

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = (
    ROOT
    / ".specify"
    / "specs"
    / "018-cli-priority-support"
    / "contracts"
    / "cli-priority-support.openapi.yaml"
)


def test_codex_in_agent_config():
    assert "codex" in AGENT_CONFIG


def test_codex_in_official_assistant_keys():
    assert "codex" in _OFFICIAL_ASSISTANT_KEYS


def test_codex_profile_folder():
    profile = get_assistant_profile("codex")
    assert profile["folder"] == ".codex/"


def test_codex_profile_command_directory():
    profile = get_assistant_profile("codex")
    assert profile["command_directory"] == ".codex/commands"


def test_codex_profile_command_format():
    profile = get_assistant_profile("codex")
    assert profile["command_format"] == "md"


def test_codex_profile_arg_format():
    profile = get_assistant_profile("codex")
    assert profile["arg_format"] == "$ARGUMENTS"


def test_codex_profile_requires_cli():
    profile = get_assistant_profile("codex")
    assert profile["requires_cli"] is True


def test_codex_profile_officially_supported():
    profile = get_assistant_profile("codex")
    assert profile["officially_supported"] is True


def test_codex_profile_tier():
    profile = get_assistant_profile("codex")
    assert profile["tier"] == "tier1"


def test_contract_file_lists_codex():
    content = CONTRACT.read_text(encoding="utf-8")
    assert "codex" in content
    assert "/projects/init:" in content
