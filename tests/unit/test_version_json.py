"""Regression: the CLI answers its own version, in text and as JSON.

Adapted-from: 8dfb15d9d8a2fb27343fe2e1140815e23f6ac718 — upstream stabilized a
``version --json`` payload. Master had no ``--version`` flag and no ``version``
command at all, so the surface is new here and the key names follow master's
own JSON envelopes (camelCase, like ``specify migrate``), not upstream's
artifact contract.

The values are not re-derived: ``version_payload`` delegates to
``migrate_target_record`` (distribution version + framework source commit), so
these cases pin the reuse as well as the surface. The git probe is stubbed to
keep the unit in-process and independent of the checkout it runs in.
"""

import json
import platform
import sys

import specify_cli

_KEYS = {
    "name",
    "cliVersion",
    "frameworkCommit",
    "commitOrigin",
    "python",
    "platform",
    "architecture",
}
_COMMIT = "a" * 40


def _invoke(args):
    from typer.testing import CliRunner

    return CliRunner().invoke(specify_cli.app, args)


def _stub_source(monkeypatch, commit=_COMMIT, origin="git"):
    monkeypatch.setattr(
        specify_cli,
        "resolve_source_commit",
        lambda: {"commit": commit, "origin": origin, "reason": None},
    )


def test_version_json_emits_one_closed_record_on_stdout(monkeypatch):
    _stub_source(monkeypatch)
    result = _invoke(["version", "--json"])

    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)  # whole stdout: no banner, no prefix
    assert set(payload) == _KEYS
    assert payload["name"] == "specify-cli"
    assert payload["cliVersion"] == specify_cli.migrate_cli_version()
    assert payload["frameworkCommit"] == _COMMIT
    assert payload["commitOrigin"] == "git"
    assert payload["python"] == platform.python_version()
    assert payload["platform"] == sys.platform
    assert payload["architecture"] == platform.machine()


def test_version_json_is_unstyled_and_banner_free(monkeypatch):
    _stub_source(monkeypatch)
    result = _invoke(["version", "--json"])

    assert result.output.startswith("{")
    assert "\x1b[" not in result.output
    assert "█" not in result.output


def test_version_json_reports_unavailable_without_fabricating(monkeypatch):
    _stub_source(monkeypatch, commit=None, origin="unavailable")
    monkeypatch.setattr(specify_cli, "migrate_cli_version", lambda: "unavailable")

    payload = json.loads(_invoke(["version", "--json"]).output)

    assert payload["frameworkCommit"] == "unavailable"
    assert payload["commitOrigin"] == "unavailable"
    assert payload["cliVersion"] == "unavailable"


def test_version_flag_and_subcommand_share_one_payload(monkeypatch):
    _stub_source(monkeypatch)
    expected = specify_cli.version_payload()

    for args in (["--version"], ["version"]):
        result = _invoke(args)
        assert result.exit_code == 0, result.output
        assert expected["cliVersion"] in result.output
        assert expected["frameworkCommit"] in result.output
        assert "█" not in result.output, "a version query must not print the banner"


def test_payload_reuses_the_migrate_record_owner(monkeypatch):
    sentinel = {
        "cliVersion": "9.9.9",
        "frameworkCommit": "b" * 40,
        "origin": "embedded",
    }
    monkeypatch.setattr(specify_cli, "migrate_target_record", lambda: sentinel)

    payload = specify_cli.version_payload()

    assert payload["cliVersion"] == sentinel["cliVersion"]
    assert payload["frameworkCommit"] == sentinel["frameworkCommit"]
    assert payload["commitOrigin"] == sentinel["origin"]


def test_version_help_declares_the_json_option():
    result = _invoke(["version", "--help"])

    assert result.exit_code == 0
    assert "--json" in result.output


def test_root_help_declares_the_version_flag():
    result = _invoke(["--help"])

    assert result.exit_code == 0
    assert "--version" in result.output