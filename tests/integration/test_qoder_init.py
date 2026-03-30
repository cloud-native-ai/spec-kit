from specify_cli import AGENT_CONFIG
from tests.script_api import run_specify_check


def test_check_command_reports_qoder_cli_surface(monkeypatch):
    monkeypatch.setattr("specify_cli.show_banner", lambda: None)
    monkeypatch.setattr(
        "specify_cli.check_tool",
        lambda tool, tracker=None: tool in {"git", "code", "code-insiders", "qoder"},
    )

    result = run_specify_check()

    assert result.exit_code == 0
    assert AGENT_CONFIG["qoder"]["name"] in result.stdout
