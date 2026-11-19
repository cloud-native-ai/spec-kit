"""Unit tests: the 1 MiB standard-input ceiling (memory + write-path gate).

Port family: upstream ``f8b3d604e`` ("fix: cap stdin read at 1 MiB to prevent
DoS"). Upstream capped one CLI call site; this port applies the same bound to
the two unbounded stdin reads the framework actually has:

* ``scripts/python/memory-utils.py::read_content`` — ``sys.stdin.read()``;
* ``scripts/python/gate-check.py --stdin`` — line-by-line iteration, unbounded
  in both the line count and the length of a single line.

Over-limit behaviour is REFUSAL, never truncation, and each engine reports it
through its own existing error ladder (memory: ``MemoryError`` → exit 2; gate:
exit 2, the code its help already reserves for an unusable invocation). A
truncated memory body would be stored as if complete; a truncated path list
would make the gate print ``allow`` for paths it never saw.

Subjects are the framework sources under ``scripts/python/`` (never the
``.specify/`` mirror — two-hats rule). The ceiling is exercised both at its real
declared value (subprocess, true byte semantics) and with the module constant
monkeypatched small, so no test has to pipe megabytes to prove the bound.

Red-first evidence: /tmp/speckit-p1/redfirst-d-before.txt (an 8 MiB payload was
accepted by both engines before this port).
"""
from __future__ import annotations

import io
import subprocess
import sys
import types
from pathlib import Path

import pytest

from tests.script_api import ROOT, load_engine_module, memory_utils as mu
from tests.script_api import run_engine_in_process

GATE_SCRIPT = ROOT / "scripts" / "python" / "gate-check.py"
MEMORY_SCRIPT = ROOT / "scripts" / "python" / "memory-utils.py"
gate = load_engine_module(GATE_SCRIPT)

ONE_MIB = 1024 * 1024


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _pipe(monkeypatch, data: bytes, encoding: str = "utf-8", errors: str = "strict"):
    """A real text stream over bytes: exposes .buffer, .encoding and .errors."""
    stream = io.TextIOWrapper(io.BytesIO(data), encoding=encoding, errors=errors)
    monkeypatch.setattr(sys, "stdin", stream)
    return stream


class _ShortReadStream:
    """A stream that never returns more than *granularity* units per request."""

    def __init__(self, data: bytes, granularity: int = 3):
        self._stream = io.BytesIO(data)
        self._granularity = granularity
        self.requests: list[int] = []

    def read(self, size=-1):
        self.requests.append(size)
        return self._stream.read(min(size, self._granularity))

    @property
    def consumed(self) -> int:
        return self._stream.tell()


class _UntouchableStdin:
    """Fails the test if anything reads it (help must not act)."""

    isatty = staticmethod(lambda: False)

    def read(self, *args, **kwargs):
        raise AssertionError("stdin was read on a path that must not act")

    def __iter__(self):
        raise AssertionError("stdin was iterated on a path that must not act")


def _run(script: Path, args, payload: bytes, cwd: Path = ROOT):
    return subprocess.run([sys.executable, str(script), *args], input=payload,
                          capture_output=True, cwd=str(cwd), timeout=180)


def _record_args(workspace: Path):
    return ["--action", "record", "--source", "/speckit.plan",
            "--title", "bounded stdin probe", "--workspace-root", str(workspace),
            "--format", "json"]


# --------------------------------------------------------------------------- #
# subjects + the shared bound
# --------------------------------------------------------------------------- #
def test_subjects_are_framework_source_engines():
    assert Path(mu.__file__).resolve() == MEMORY_SCRIPT.resolve()
    assert Path(gate.__file__).resolve() == GATE_SCRIPT.resolve()


def test_both_engines_declare_the_same_one_mib_ceiling():
    # drift pin: two engines, one bound (a literal in a test is a sanctioned
    # duplicate of the owner constants)
    assert mu.MAX_STDIN_BYTES == ONE_MIB
    assert gate.MAX_STDIN_BYTES == ONE_MIB
    assert mu.STDIN_READ_CHUNK_BYTES == gate.STDIN_READ_CHUNK_BYTES == 64 * 1024


# --------------------------------------------------------------------------- #
# memory-utils: the piped entry body
# --------------------------------------------------------------------------- #
def test_memory_stdin_at_the_ceiling_is_accepted(monkeypatch):
    monkeypatch.setattr(mu, "MAX_STDIN_BYTES", 64)
    _pipe(monkeypatch, b"x" * 64)
    assert mu.read_stdin_limited() == "x" * 64


def test_memory_stdin_one_byte_over_the_ceiling_is_refused(monkeypatch):
    monkeypatch.setattr(mu, "MAX_STDIN_BYTES", 64)
    _pipe(monkeypatch, b"x" * 65)
    with pytest.raises(mu.MemoryError) as excinfo:
        mu.read_stdin_limited()
    assert "64-byte limit" in str(excinfo.value)
    assert "truncate" in str(excinfo.value)


def test_memory_over_limit_stdin_records_nothing(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mu, "MAX_STDIN_BYTES", 64)
    _pipe(monkeypatch, b"x" * 4096)
    rc = mu.main(_record_args(tmp_path))
    err = capsys.readouterr().err
    assert rc == 2
    assert "stdin payload exceeds" in err
    session = tmp_path / ".specify" / "memory" / "session"
    assert not session.exists() or not list(session.glob("*.md"))


def test_memory_small_stdin_records_the_whole_body(tmp_path, monkeypatch, capsys):
    body = "第一行 memory body\nsecond line\n"
    _pipe(monkeypatch, body.encode("utf-8"))
    rc = mu.main(_record_args(tmp_path))
    captured = capsys.readouterr()
    assert rc == 0, captured.err
    entries = list((tmp_path / ".specify" / "memory" / "session").glob("*.md"))
    assert len(entries) == 1
    assert body.strip() in entries[0].read_text(encoding="utf-8")


def test_memory_explicit_content_never_reads_stdin(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(sys, "stdin", _UntouchableStdin())
    rc = mu.main([*_record_args(tmp_path), "--content", "explicit body"])
    assert rc == 0, capsys.readouterr().err


def test_memory_text_only_stream_fallback_is_bounded_too(monkeypatch):
    monkeypatch.setattr(mu, "MAX_STDIN_BYTES", 8)
    monkeypatch.setattr(sys, "stdin", io.StringIO("x" * 8))  # no .buffer
    assert mu.read_stdin_limited() == "x" * 8
    monkeypatch.setattr(sys, "stdin", io.StringIO("x" * 9))
    with pytest.raises(mu.MemoryError):
        mu.read_stdin_limited()


def test_memory_short_reads_cannot_slip_past_the_ceiling(monkeypatch):
    monkeypatch.setattr(mu, "MAX_STDIN_BYTES", 10)
    stream = _ShortReadStream(b"x" * 1000)
    monkeypatch.setattr(sys, "stdin", types.SimpleNamespace(
        buffer=stream, encoding="utf-8", errors="strict"))
    with pytest.raises(mu.MemoryError):
        mu.read_stdin_limited()
    assert stream.consumed == 11  # ceiling + 1, never the whole payload
    assert max(stream.requests) <= mu.STDIN_READ_CHUNK_BYTES


def test_memory_crlf_body_keeps_text_mode_newline_translation(monkeypatch):
    # reading the binary buffer bypasses the text layer, so its universal-newline
    # translation must be reproduced: a CRLF-piped body lands as it always did
    _pipe(monkeypatch, b"first line\r\nsecond line\rthird line\r\n")
    assert mu.read_stdin_limited() == "first line\nsecond line\nthird line\n"


def test_memory_decoding_is_the_streams_own(monkeypatch):
    text = "记忆 body with 中文 and emoji-free punctuation"
    _pipe(monkeypatch, text.encode("utf-8"))
    assert mu.read_stdin_limited() == text
    # a non-UTF-8 stream keeps its own error handler, exactly as read() did
    _pipe(monkeypatch, b"\xff", encoding="ascii", errors="surrogateescape")
    assert mu.read_stdin_limited() == "\udcff"


def test_memory_real_ceiling_boundary_in_a_subprocess(tmp_path):
    at = _run(MEMORY_SCRIPT, _record_args(tmp_path / "at"), b"x" * ONE_MIB)
    assert at.returncode == 0, at.stderr.decode()[:400]
    over = _run(MEMORY_SCRIPT, _record_args(tmp_path / "over"), b"x" * (ONE_MIB + 1))
    assert over.returncode == 2
    assert b"stdin payload exceeds" in over.stderr
    assert not list((tmp_path / "over").rglob("*.md"))


# --------------------------------------------------------------------------- #
# gate-check: the candidate path list
# --------------------------------------------------------------------------- #
def test_gate_stdin_paths_at_the_ceiling_are_accepted(monkeypatch):
    monkeypatch.setattr(gate, "MAX_STDIN_BYTES", 64)
    _pipe(monkeypatch, b"a.md\nb.md\n")
    assert gate.read_stdin_paths() == ["a.md", "b.md"]


def test_gate_over_ceiling_refuses_and_emits_no_verdict(monkeypatch):
    monkeypatch.setattr(gate, "MAX_STDIN_BYTES", 64)
    _pipe(monkeypatch, b"docs/a.md\n" * 100)
    result = run_engine_in_process(GATE_SCRIPT, ["--stdin"])
    assert result.returncode == 2
    assert result.stdout == ""  # never an invented "allow" for an unseen path
    assert "stdin payload exceeds" in result.stderr


def test_gate_single_unbroken_line_is_bounded(monkeypatch):
    # the old line iterator buffered a newline-free payload as ONE line
    monkeypatch.setattr(gate, "MAX_STDIN_BYTES", 64)
    _pipe(monkeypatch, b"x" * 5000)
    with pytest.raises(ValueError):
        gate.read_stdin_paths()


def test_gate_newline_forms_match_text_mode(monkeypatch):
    _pipe(monkeypatch, b"a.md\r\nb.md\rc.md\n")
    assert gate.read_stdin_paths() == ["a.md", "b.md", "c.md"]


def test_gate_blank_lines_are_dropped(monkeypatch):
    _pipe(monkeypatch, b"\n   \na.md\n\n")
    assert gate.read_stdin_paths() == ["a.md"]


def test_gate_text_only_stream_fallback(monkeypatch):
    monkeypatch.setattr(gate, "MAX_STDIN_BYTES", 8)
    monkeypatch.setattr(sys, "stdin", io.StringIO("a.md\n"))
    assert gate.read_stdin_paths() == ["a.md"]
    monkeypatch.setattr(sys, "stdin", io.StringIO("a.md\n" * 4))
    with pytest.raises(ValueError):
        gate.read_stdin_paths()


def test_gate_undecodable_payload_is_not_relabelled_as_over_limit(monkeypatch):
    # The ceiling refusal is its own condition. A payload the stream cannot
    # decode keeps failing as its own decode error (the pre-port behaviour under
    # a strict locale), never as "stdin payload exceeds" — the port bounds the
    # read, it does not redefine the engine's other input errors.
    _pipe(monkeypatch, b"docs/caf\xe9.md\n", encoding="utf-8", errors="strict")
    with pytest.raises(UnicodeDecodeError):
        gate.read_stdin_paths()


def test_gate_help_never_reads_stdin(monkeypatch):
    monkeypatch.setattr(sys, "stdin", _UntouchableStdin())
    result = run_engine_in_process(GATE_SCRIPT, ["--help"])
    assert result.returncode == 0
    for label in ("usage:", "options:", "side-effects:", "exit-codes:"):
        assert label in result.stdout


def test_gate_help_documents_the_ceiling_and_the_refusal():
    assert str(gate.MAX_STDIN_BYTES) in gate._HELP
    assert "over its ceiling" in gate._HELP
    assert "never truncated" in gate._HELP


def test_gate_real_ceiling_refuses_in_a_subprocess():
    line = b"some/path/" + b"p" * 60 + b"\n"
    result = _run(GATE_SCRIPT, ["--stdin"], line * (2 * ONE_MIB // len(line)))
    assert result.returncode == 2
    assert result.stdout == b""
    assert b"stdin payload exceeds" in result.stderr


def test_gate_small_stdin_still_gates():
    result = _run(GATE_SCRIPT, ["--stdin"], b"docs/x.md\n")
    assert result.returncode == 0, result.stderr.decode()[:400]
    assert b"allow   docs/x.md" in result.stdout


def test_gate_undeclared_option_is_still_rejected():
    result = _run(GATE_SCRIPT, ["--not-an-option"], b"")
    assert result.returncode == 2