from specify_cli import AGENT_CONFIG
from tests.script_api import run_specify_check


def test_check_command_reports_claude_cli_surface(monkeypatch):
    monkeypatch.setattr("specify_cli.show_banner", lambda: None)
    monkeypatch.setattr(
        "specify_cli.check_tool",
        lambda tool, tracker=None: tool in {"git", "code", "code-insiders", "claude"},
    )

    result = run_specify_check()

    assert result.exit_code == 0
    assert AGENT_CONFIG["claude"]["name"] in result.stdout
