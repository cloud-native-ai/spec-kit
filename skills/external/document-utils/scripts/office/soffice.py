"""Run LibreOffice headless, and the three jobs this skill asks of it.

Original implementation, MIT licensed. LibreOffice is an external program
(LGPL/MPL, invoked as a subprocess, never imported); this module is the thin
wrapper that makes an invocation reproducible:

* ``get_soffice_env()`` — the environment a headless run needs. Side-effect
  free, so a caller may build its own ``subprocess`` command line with it.
* ``run_soffice(args)`` — run ``soffice`` with that environment and an isolated
  user profile, so two conversions at the same time do not fight over one
  profile directory.
* ``convert()`` / ``thumbnail()`` / ``recalc()`` — the three entry points the
  DOCX, PPTX and XLSX helpers use.

Sandbox note: LibreOffice needs AF_UNIX sockets for its own IPC. Where a
sandbox forbids them, ``af_unix_available()`` reports False and a conversion
will fail with LibreOffice's own error; run the conversion in an environment
that permits AF_UNIX. This wrapper no longer injects an LD_PRELOAD socket shim.

Usage:
    from office.soffice import run_soffice, get_soffice_env, convert
    convert("report.docx", "pdf", outdir="out/")
"""

from __future__ import annotations

import os
import shutil
import socket
import subprocess
import tempfile
from contextlib import contextmanager
from pathlib import Path

#: Where a LibreOffice install hides when it is not on PATH.
KNOWN_BINARIES = (
    "/usr/bin/soffice",
    "/usr/local/bin/soffice",
    "/opt/libreoffice/program/soffice",
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
)


def get_soffice_env() -> dict:
    """A copy of the environment with the headless VCL plugin selected."""
    env = os.environ.copy()
    env["SAL_USE_VCLPLUGIN"] = "svp"
    env["SAL_DISABLE_OPENCL"] = "1"
    return env


def find_soffice() -> str | None:
    """The soffice executable, or None when LibreOffice is not installed."""
    for name in ("soffice", "libreoffice"):
        found = shutil.which(name)
        if found:
            return found
    for candidate in KNOWN_BINARIES:
        if Path(candidate).is_file() and os.access(candidate, os.X_OK):
            return candidate
    return None


def af_unix_available() -> bool:
    """Whether this host lets a process open an AF_UNIX socket."""
    try:
        probe = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    except OSError:
        return False
    probe.close()
    return True


@contextmanager
def isolated_profile():
    """A throwaway user profile directory, removed when the block exits."""
    with tempfile.TemporaryDirectory(prefix="document-utils-lo-") as scratch:
        yield Path(scratch) / "profile"


def run_soffice(args, **kwargs) -> subprocess.CompletedProcess:
    """Run soffice with the headless environment and a private user profile."""
    executable = find_soffice()
    if executable is None:
        raise FileNotFoundError(
            "LibreOffice (soffice) was not found on PATH or in a known install location"
        )
    args = list(args)
    if any(str(arg).startswith("-env:UserInstallation") for arg in args):
        return subprocess.run([executable] + args, env=get_soffice_env(), **kwargs)
    with isolated_profile() as profile:
        command = [executable, f"-env:UserInstallation=file://{profile}"] + args
        return subprocess.run(command, env=get_soffice_env(), **kwargs)


def convert(source, target_format: str = "pdf", outdir=None, timeout: int = 180):
    """Convert one document; the result lands in ``outdir`` (default: beside it)."""
    source = Path(source)
    destination = Path(outdir) if outdir else source.parent
    destination.mkdir(parents=True, exist_ok=True)
    return run_soffice(
        [
            "--headless",
            "--norestore",
            "--convert-to",
            target_format,
            "--outdir",
            str(destination),
            str(source),
        ],
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def thumbnail(source, outdir=None, timeout: int = 180):
    """Render the first page/slide of a document as a PNG image."""
    return convert(source, "png", outdir=outdir, timeout=timeout)


def recalc(workbook, outdir=None, timeout: int = 180):
    """Re-save a workbook through Calc so its formula results are written out.

    Calc evaluates formulas while loading, subject to its own recalculation
    setting; this entry point re-saves the file in the Excel 2007 XML format so
    the cached values a reader sees come from Calc rather than from the writer.
    """
    return convert(workbook, 'xlsx:"Calc MS Excel 2007 XML"', outdir=outdir, timeout=timeout)


#
# Emitted by `scripts/python/sync-mirrors.py`; the authority for this block is
# `contracts/mirror-projection.contract.md` C-34 / C-36. It depends on nothing
# that exists only in the source tree: it re-derives its own version line (C-36).
_VERSION_SOURCE = "pyproject.toml"
_VERSION_QUOTES = chr(39) + chr(34)
_MAX_UPWARD_LEVELS = 12


def _bridge_version(start):
    _here = start.resolve()
    for _ in range(_MAX_UPWARD_LEVELS + 1):
        if (_here / _VERSION_SOURCE).is_file() and (_here / ".git").exists():
            try:
                _text = (_here / _VERSION_SOURCE).read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                return "unknown"
            _in_project = False
            for _raw in _text.splitlines():
                _line = _raw.strip()
                if not _line or _line.startswith("#"):
                    continue
                if _line.startswith("[") and _line.endswith("]"):
                    _in_project = _line == "[project]"
                    continue
                if not _in_project:
                    continue
                _key, _sep, _value = _line.partition("=")
                if _sep and _key.strip() == "version":
                    _value = _value.strip()
                    if len(_value) >= 2 and _value[0] == _value[-1] and _value[0] in _VERSION_QUOTES:
                        _value = _value[1:-1]
                    return _value or "unknown"
            return "unknown"
        if _here.parent == _here:
            return "unknown"
        _here = _here.parent
    return "unknown"

def _bridge_main():
    import sys as _bridge_sys
    from pathlib import Path as _bridge_path

    _argv = list(_bridge_sys.argv[1:])
    if "--version" not in _argv:
        return
    if "--" in _argv and _argv.index("--version") > _argv.index("--"):
        return
    _invoked = _bridge_sys.argv[0] if _bridge_sys.argv[0] else "."
    _name = _bridge_path(_invoked).name or "script"
    print("%s %s" % (_name, _bridge_version(_bridge_path(_invoked).resolve().parent)))
    raise SystemExit(0)


_bridge_main()
del _bridge_main
# script-interface:86:begin (feature 086 -- generated; the rule is owned by
# `shared/definitions/script-interface-definitions.md`, its executable form by
# `scripts/python/script_interface_cli.py`. This block owns no rule of its own.)
import sys as _sig_sys
import pathlib as _sig_pathlib

_SIG_OWNER = _sig_pathlib.Path(__file__).resolve().parent
while not ((_SIG_OWNER / 'pyproject.toml').is_file()
           and (_SIG_OWNER / '.git').exists()) and _SIG_OWNER.parent != _SIG_OWNER:
    _SIG_OWNER = _SIG_OWNER.parent
_SIG_OWNER = str(_SIG_OWNER / 'scripts' / 'python')
if _SIG_OWNER not in _sig_sys.path:
    _sig_sys.path.insert(0, _SIG_OWNER)

_SIG_SCRIPT = 'skills/external/document-utils/scripts/office/soffice.py'
_SIG_DECLARED = ()
_SIG_HELP = (
    'usage: soffice.py [options]\n'
    'options:\n'
    '  (none of its own; the arguments it takes are operands)\n'
    '  -h, --help    print this help and exit\n'
    '  --version     print the script name and the framework version, then exit\n'
    +
    'side-effects:' + ' ' + 'writes only through the options it documents; a flag-only invocation writes nothing' + '\n'
    +
    'exit-codes:' + ' ' + '0 success; 1 a documented check failed; 2 argument or environment error' + '\n'
)


def _sig_guard(argv):
    # Answer the flags and reject an undeclared option before any parsing or write.
    # RULES are asked of the owner (script_interface_cli.guard_argv), never restated:
    # the declared vocabulary and the flag forms are its, and C-9 (a recognized option
    # never rescues an unrecognized one) is its judgement. What stays local is the help
    # BODY, because its operand sentence is this script's own.
    try:
        import script_interface_cli as _sig  # noqa: E402 -- deferred: a copied script may lack it
    except ImportError:  # skill-local or sandbox copy: the module's own parser still runs
        return list(argv)
    line = list(argv)
    try:
        _sig.guard_argv(line, declared=_SIG_DECLARED)
    except SystemExit as answered:  # what guard_argv raises; _sig_sys.exit IS SystemExit
        if answered.code == 0:
            raise
        # The owner prints the rejection line and this script's help body is appended after
        # it, so the reader sees the vocabulary and not only the refusal.
        _sig_sys.stderr.write(_SIG_HELP)
        raise _sig_sys.exit(answered.code)
    stop = line.index('--') if '--' in line else len(line)
    if '-h' in line[:stop] or '--help' in line[:stop]:
        _sig_sys.stdout.write(_SIG_HELP)
        raise _sig_sys.exit(0)
    return line

if __name__ == "__main__":
    _sig_sys.argv = [_sig_sys.argv[0]] + _sig_guard(_sig_sys.argv[1:])
# script-interface:86:end

if __name__ == "__main__":
    import sys

    completed = run_soffice(sys.argv[1:])
    sys.exit(completed.returncode)