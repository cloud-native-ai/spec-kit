"""Regression: ``run_command`` never invokes a shell.

Adapted-from: 8e76ff3d5cd4796c4515bac84ed5c4479b2ab199 — upstream forwarded
``shell=`` straight to ``subprocess.run``; master's copy was word-for-word the
same pre-fix shape. The parameter stays for keyword compatibility, but
``shell=True`` now fails loudly instead of running with a different meaning.

Every case stubs ``subprocess.run``: the guard is about what reaches the process
boundary, so no real process is spawned and the unit stays in the fast tier.
"""

import io
import subprocess

import pytest
from rich.console import Console

import specify_cli


def _capture_console(monkeypatch) -> io.StringIO:
    buf = io.StringIO()
    monkeypatch.setattr(
        specify_cli,
        "console",
        Console(file=buf, width=400, no_color=True, highlight=False),
    )
    return buf


@pytest.mark.parametrize("capture", [False, True])
@pytest.mark.parametrize("check_return", [False, True])
def test_shell_true_is_rejected_before_any_spawn(
    monkeypatch, capture, check_return
):
    def _forbidden(*args, **kwargs):
        raise AssertionError("subprocess.run reached despite shell=True")

    monkeypatch.setattr(specify_cli.subprocess, "run", _forbidden)

    with pytest.raises(ValueError, match="shell=True"):
        specify_cli.run_command(
            ["echo", "hi"],
            check_return=check_return,
            capture=capture,
            shell=True,
        )


def test_shell_true_with_a_string_command_is_rejected(monkeypatch):
    """The injection shape: one string plus a shell metacharacter."""

    def _forbidden(*args, **kwargs):
        raise AssertionError("subprocess.run reached despite shell=True")

    monkeypatch.setattr(specify_cli.subprocess, "run", _forbidden)

    with pytest.raises(ValueError, match="argv as a list"):
        specify_cli.run_command("echo hi && touch /tmp/pwned", shell=True)


@pytest.mark.parametrize("capture", [False, True])
@pytest.mark.parametrize("extra", [{}, {"shell": False}])
def test_shell_kwarg_is_never_forwarded(monkeypatch, capture, extra):
    seen = {}

    class _Result:
        stdout = "  ok  "

    def _run(cmd, **kwargs):
        seen["cmd"] = cmd
        seen.update(kwargs)
        return _Result()

    monkeypatch.setattr(specify_cli.subprocess, "run", _run)

    out = specify_cli.run_command(["tool", "arg"], capture=capture, **extra)

    assert seen["cmd"] == ["tool", "arg"], "argv must reach subprocess unchanged"
    assert "shell" not in seen, "shell= must not be forwarded at all"
    assert out == ("ok" if capture else None)


def test_failure_without_check_return_stays_silent(monkeypatch):
    buf = _capture_console(monkeypatch)

    def _run(cmd, **kwargs):
        raise subprocess.CalledProcessError(2, cmd)

    monkeypatch.setattr(specify_cli.subprocess, "run", _run)

    assert specify_cli.run_command(["tool"], check_return=False) is None
    assert buf.getvalue() == ""


def test_failure_with_check_return_reraises(monkeypatch):
    _capture_console(monkeypatch)

    def _run(cmd, **kwargs):
        raise subprocess.CalledProcessError(3, cmd)

    monkeypatch.setattr(specify_cli.subprocess, "run", _run)

    with pytest.raises(subprocess.CalledProcessError) as excinfo:
        specify_cli.run_command(["tool"], capture=True)
    assert excinfo.value.returncode == 3