"""Recalculate every formula in a workbook, then report the errors it produced.

Usage: python recalc.py <excel_file> [timeout_seconds]

openpyxl writes a formula as text and leaves the cached value empty, so a
workbook built by a script shows blanks until something evaluates it.  This
script asks LibreOffice to do that evaluation in place: a short StarBasic macro
calls ``calculateAll()`` and stores the document, run headless against the
caller's file.  The workbook keeps its formulas -- only the cached values change.

Afterwards the saved file is read twice with openpyxl: once for values, to find
cells that evaluated to an Excel error, and once for formulas, to count them.
The result is a JSON object on stdout:

    status          "success" or "errors_found"
    total_errors    number of cells holding an error value
    total_formulas  number of formula cells in the workbook
    error_summary   per error type: count and up to 20 "Sheet!Cell" locations

A run that could not start reports {"error": "..."} instead.  The exit status is
0 for both shapes: the JSON is the result, and a caller reads the verdict there.

spec-kit project, MIT licensed -- see LICENSE.txt.
"""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
from pathlib import Path

#
# Emitted by `.specify/scripts/python/sync-mirrors.py`; the authority for this block is
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
# `.specify/shared/definitions/script-interface-definitions.md`, its executable form by
# `.specify/scripts/python/script_interface_cli.py`. This block owns no rule of its own.)
import sys as _sig_sys
import pathlib as _sig_pathlib

_SIG_OWNER = _sig_pathlib.Path(__file__).resolve().parent
while not ((_SIG_OWNER / 'pyproject.toml').is_file()
           and (_SIG_OWNER / '.git').exists()) and _SIG_OWNER.parent != _SIG_OWNER:
    _SIG_OWNER = _SIG_OWNER.parent
_SIG_OWNER = str(_SIG_OWNER / 'scripts' / 'python')
if _SIG_OWNER not in _sig_sys.path:
    _sig_sys.path.insert(0, _SIG_OWNER)

_SIG_SCRIPT = '.specify/skills/document-utils/scripts/xlsx/recalc.py'
_SIG_DECLARED = ()
_SIG_HELP = (
    'usage: recalc.py [options]\n'
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

SCRIPT_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = SCRIPT_DIR.parent

#: Where a LibreOffice user profile keeps its Standard Basic library.
PROFILE_BASIC = {
    "Darwin": "~/Library/Application Support/LibreOffice/4/user/basic/Standard",
    "Linux": "~/.config/libreoffice/4/user/basic/Standard",
}
DEFAULT_BASIC = "~/.config/libreoffice/4/user/basic/Standard"

MODULE_NAME = "Module1"
SUB_NAME = "RecalculateAndSave"

#: The macro itself.  ``calculateAll`` forces a full recalculation regardless of
#: the document's own recalc-on-load setting; ``store`` writes the cached values
#: back to the same file; ``close`` releases it so the process can exit.
MACRO_BODY = (
    f"Sub {SUB_NAME}\n"
    "  Dim document As Object\n"
    "  document = ThisComponent\n"
    "  document.calculateAll()\n"
    "  document.store()\n"
    "  document.close(True)\n"
    "End Sub\n"
)

MODULE_TEMPLATE = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<!DOCTYPE script:module PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" '
    '"module.dtd">\n'
    '<script:module xmlns:script="http://openoffice.org/2000/script" '
    f'script:name="{MODULE_NAME}" script:language="StarBasic">\n'
    "{body}"
    "</script:module>\n"
)

#: The macro URL LibreOffice resolves against the application's Basic libraries.
MACRO_URL = (
    f"vnd.sun.star.script:Standard.{MODULE_NAME}.{SUB_NAME}"
    "?language=Basic&location=application"
)

#: Excel's error values.  A cell is counted once, under the first token it holds.
ERROR_TOKENS = (
    "#VALUE!",
    "#DIV/0!",
    "#REF!",
    "#NAME?",
    "#NULL!",
    "#NUM!",
    "#N/A",
)

#: Locations reported per error type; the count stays complete.
LOCATION_CAP = 20

DEFAULT_TIMEOUT = 30


def _soffice_env() -> dict:
    """The environment LibreOffice runs in, as the office wrapper defines it."""
    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        from office.soffice import get_soffice_env
    except ImportError:
        return os.environ.copy()
    return get_soffice_env()


def macro_directory() -> Path:
    """The Standard Basic library directory of this user's LibreOffice profile."""
    template = PROFILE_BASIC.get(platform.system(), DEFAULT_BASIC)
    return Path(os.path.expanduser(template))


def install_macro() -> bool:
    """Make the recalculation macro available to LibreOffice.  True on success.

    An existing module is never clobbered: when it already defines the sub it is
    reused, and when it defines something else the sub is appended to it.  A
    profile that does not exist yet is initialized first, because LibreOffice
    creates the Standard library itself and a hand-made directory would not be
    registered in it.
    """
    directory = macro_directory()
    module = directory / f"{MODULE_NAME}.xba"

    if module.is_file():
        try:
            text = module.read_text(encoding="utf-8")
        except OSError:
            return False
        if SUB_NAME in text:
            return True
        closing = "</script:module>"
        if closing not in text:
            return False
        try:
            module.write_text(text.replace(closing, MACRO_BODY + closing), encoding="utf-8")
        except OSError:
            return False
        return True

    if not directory.is_dir():
        try:
            subprocess.run(
                ["soffice", "--headless", "--terminate_after_init"],
                capture_output=True,
                timeout=60,
                env=_soffice_env(),
                check=False,
            )
            directory.mkdir(parents=True, exist_ok=True)
        except (OSError, subprocess.SubprocessError):
            return False

    try:
        module.write_text(MODULE_TEMPLATE.format(body=MACRO_BODY), encoding="utf-8")
    except OSError:
        return False
    return True


def run_recalculation(path: Path, timeout: int) -> dict | None:
    """Ask LibreOffice to recalculate and store ``path``.  None when it ran.

    A timeout is not treated as failure: the macro stores the document before it
    closes it, so a process that outlived the budget may already have written the
    values.  The scan that follows reads whatever is on disk.
    """
    command = ["soffice", "--headless", "--norestore", MACRO_URL, str(path)]
    try:
        finished = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=_soffice_env(),
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None
    except OSError as exc:
        return {"error": f"LibreOffice could not be started: {exc}"}

    if finished.returncode != 0:
        detail = (finished.stderr or finished.stdout or "").strip()
        return {"error": detail or "Unknown error during recalculation"}
    return None


def _openpyxl():
    """The workbook reader, or a plain statement of what is missing."""
    try:
        import openpyxl
    except ImportError as exc:
        raise RuntimeError(
            "openpyxl is required to read the recalculated workbook; install it "
            "with 'python -m pip install openpyxl'"
        ) from exc
    return openpyxl


def scan_workbook(path: Path) -> dict:
    """Read the saved workbook for error values and for the formula count."""
    openpyxl = _openpyxl()
    values = openpyxl.load_workbook(path, data_only=True)
    locations: dict[str, list[str]] = {token: [] for token in ERROR_TOKENS}
    try:
        for sheet in values.worksheets:
            for row in sheet.iter_rows():
                for cell in row:
                    if not isinstance(cell.value, str):
                        continue
                    for token in ERROR_TOKENS:
                        if token in cell.value:
                            locations[token].append(f"{sheet.title}!{cell.coordinate}")
                            break
    finally:
        values.close()

    total_errors = sum(len(items) for items in locations.values())
    summary = {
        token: {"count": len(items), "locations": items[:LOCATION_CAP]}
        for token, items in locations.items()
        if items
    }

    formulas = openpyxl.load_workbook(path, data_only=False)
    try:
        total_formulas = sum(
            1
            for sheet in formulas.worksheets
            for row in sheet.iter_rows()
            for cell in row
            if cell.data_type == "f"
        )
    finally:
        formulas.close()

    return {
        "status": "success" if total_errors == 0 else "errors_found",
        "total_errors": total_errors,
        "error_summary": summary,
        "total_formulas": total_formulas,
    }


def recalc(filename, timeout: int = DEFAULT_TIMEOUT) -> dict:
    """Recalculate one workbook and report what its formulas evaluated to."""
    path = Path(filename)
    if not path.is_file():
        return {"error": f"File {filename} does not exist"}

    if not install_macro():
        return {"error": "Failed to setup LibreOffice macro"}

    failure = run_recalculation(path.resolve(), timeout)
    if failure is not None:
        return failure

    try:
        return scan_workbook(path)
    except Exception as exc:  # a workbook LibreOffice wrote but openpyxl cannot read
        return {"error": str(exc)}


def main(argv: list[str]) -> int:
    if not argv:
        print("Usage: python recalc.py <excel_file> [timeout_seconds]")
        print("\nRecalculates every formula in a workbook with LibreOffice, in place.")
        print("\nPrints a JSON result:")
        print("  status          'success' or 'errors_found'")
        print("  total_errors    cells holding an Excel error value")
        print("  total_formulas  formula cells in the workbook")
        print("  error_summary   per error type: count and up to 20 locations")
        print("    " + ", ".join(ERROR_TOKENS))
        return 1

    try:
        timeout = int(argv[1]) if len(argv) > 1 else DEFAULT_TIMEOUT
    except ValueError:
        sys.stderr.write("Error: timeout_seconds must be an integer\n")
        return 1

    print(json.dumps(recalc(argv[0], timeout), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))