"""Regression: untrusted text reaching ``console.print`` keeps its brackets.

Adapted-from: 99dc915ae38a276ce6be542b97cf2fbd4efd048b — upstream escaped the
catalog fields it printed; master has no catalog, so the same rule lands on the
sinks that carry argv, process output, exception text, paths and user-supplied
names. Rich reads ``[...]`` as a style tag: unescaped, the text is swallowed or
raises while rendering.

The intentional markup (``[red]Error ...[/red]``) must stay *styled*: each case
asserts both that the dynamic brackets survive verbatim and that the label
still emits its colour, so over-escaping cannot pass either.
"""

import io
import subprocess

import pytest
from rich.console import Console

import specify_cli


def _color_console(monkeypatch) -> io.StringIO:
    buf = io.StringIO()
    monkeypatch.setattr(
        specify_cli,
        "console",
        Console(
            file=buf,
            force_terminal=True,
            color_system="standard",
            width=400,
            highlight=False,
        ),
    )
    return buf


def test_run_command_error_keeps_bracketed_argv_and_styles_the_label(monkeypatch):
    buf = _color_console(monkeypatch)
    argv = ["tool", "[red]not-a-tag[/red]", "C:\\dir\\[x]"]

    def _run(cmd, **kwargs):
        raise subprocess.CalledProcessError(3, cmd)

    monkeypatch.setattr(specify_cli.subprocess, "run", _run)

    with pytest.raises(subprocess.CalledProcessError):
        specify_cli.run_command(argv, capture=True)

    out = buf.getvalue()
    assert "[red]not-a-tag[/red]" in out, "argv brackets were swallowed"
    assert "C:\\dir\\[x]" in out
    assert "Error running command:" in out
    assert "\x1b[31m" in out, "the intentional red label lost its style"


def test_run_command_error_keeps_bracketed_stderr(monkeypatch):
    buf = _color_console(monkeypatch)

    def _run(cmd, **kwargs):
        raise subprocess.CalledProcessError(
            1, cmd, output="", stderr="[bold]boom[/bold] happened"
        )

    monkeypatch.setattr(specify_cli.subprocess, "run", _run)

    with pytest.raises(subprocess.CalledProcessError):
        specify_cli.run_command(["tool"], capture=True)

    out = buf.getvalue()
    assert "[bold]boom[/bold] happened" in out
    assert "Error output:" in out


def test_step_tracker_plain_log_keeps_bracketed_label_and_detail(monkeypatch):
    buf = _color_console(monkeypatch)
    tracker = specify_cli.StepTracker("Title", plain=True)
    tracker.add("step", "Label [blue]tag[/blue]")
    tracker.error("step", "failed on [red]path[/red]")

    out = buf.getvalue()
    assert "Label [blue]tag[/blue]" in out
    assert "failed on [red]path[/red]" in out


def test_step_tracker_tree_keeps_bracketed_detail(monkeypatch):
    buf = _color_console(monkeypatch)
    tracker = specify_cli.StepTracker("Title")
    tracker.add("step", "Label")
    tracker.error("step", "failed on [red]path[/red]")

    specify_cli.console.print(tracker.render())

    out = buf.getvalue()
    assert "failed on [red]path[/red]" in out
    assert "Label" in out


def test_source_stamp_warning_keeps_bracketed_oserror(monkeypatch, tmp_path):
    buf = _color_console(monkeypatch)

    def _boom():
        raise OSError("cannot stamp [red]runtime[/red] dir")

    monkeypatch.setattr(specify_cli, "resolve_source_commit", _boom)

    assert specify_cli.write_source_stamp(tmp_path) is False
    assert "cannot stamp [red]runtime[/red] dir" in buf.getvalue()
    assert not (tmp_path / ".specify" / "source.json").exists()