"""Integration test: ``specify check`` reports an installed CLI agent's surface.

Merged from ``test_claude_validation.py`` and ``test_qoder_init.py``, which were
byte-identical apart from the tool name; the tool is now the parameter.
"""

import pytest

from specify_cli import AGENT_CONFIG
from tests.script_api import run_specify_check

# Probes that are present regardless of which agent CLI is installed.
ALWAYS_PRESENT = {"git", "code", "code-insiders"}


@pytest.mark.parametrize("tool", ["claude", "qoder"])
def test_check_command_reports_cli_surface(tool, monkeypatch):
    monkeypatch.setattr("specify_cli.show_banner", lambda: None)
    monkeypatch.setattr(
        "specify_cli.check_tool",
        lambda candidate, tracker=None: candidate in ALWAYS_PRESENT | {tool},
    )

    result = run_specify_check()

    assert result.exit_code == 0
    assert AGENT_CONFIG[tool]["name"] in result.stdout
