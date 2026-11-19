"""Regression: the CLI entry point forces UTF-8 stdout/stderr on Windows.

Adapted-from: 9e05195d246f94f867a13864836353d756074a30 — a legacy Windows code
page cannot encode the banner glyphs, so piped/redirected output raised
UnicodeEncodeError instead of printing. The reconfiguration is a POSIX no-op,
tolerates streams that cannot be reconfigured, and lives at the entry point
only: importing the module as a library must not touch global streams.
"""

import sys

import pytest

import specify_cli

_UTF8 = {"encoding": "utf-8", "errors": "replace"}


class _Stream:
    def __init__(self, error=None):
        self.calls = []
        self._error = error

    def reconfigure(self, **kwargs):
        self.calls.append(kwargs)
        if self._error is not None:
            raise self._error


def _install(monkeypatch, platform_name, out, err):
    monkeypatch.setattr(sys, "platform", platform_name)
    monkeypatch.setattr(sys, "stdout", out)
    monkeypatch.setattr(sys, "stderr", err)


@pytest.mark.parametrize("platform_name", ["linux", "darwin"])
def test_posix_leaves_the_streams_untouched(monkeypatch, platform_name):
    out, err = _Stream(), _Stream()
    _install(monkeypatch, platform_name, out, err)

    specify_cli._force_utf8_output_streams()

    assert out.calls == []
    assert err.calls == []


def test_win32_reconfigures_both_streams(monkeypatch):
    out, err = _Stream(), _Stream()
    _install(monkeypatch, "win32", out, err)

    specify_cli._force_utf8_output_streams()

    assert out.calls == [_UTF8]
    assert err.calls == [_UTF8]


@pytest.mark.parametrize("error", [ValueError("closed"), OSError("detached")])
def test_win32_stream_errors_never_escape(monkeypatch, error):
    out, err = _Stream(error), _Stream(error)
    _install(monkeypatch, "win32", out, err)

    specify_cli._force_utf8_output_streams()  # must not raise

    assert out.calls == [_UTF8]
    assert err.calls == [_UTF8], "one failing stream must not skip the other"


def test_win32_stream_without_reconfigure_does_not_stop_the_other(monkeypatch):
    out, err = object(), _Stream()
    _install(monkeypatch, "win32", out, err)

    specify_cli._force_utf8_output_streams()

    assert err.calls == [_UTF8]


def test_main_configures_streams_before_running_the_app(monkeypatch):
    order = []
    monkeypatch.setattr(
        specify_cli, "_force_utf8_output_streams", lambda: order.append("streams")
    )
    monkeypatch.setattr(specify_cli, "app", lambda: order.append("app"))

    specify_cli.main()

    assert order == ["streams", "app"]