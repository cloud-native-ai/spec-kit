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

_SIG_SCRIPT = 'skills/external/document-utils/scripts/office/unpack.py'
_SIG_DECLARED = ('--merge-runs', '--simplify-redlines')
_SIG_HELP = (
    'usage: unpack.py [options]\n'
    'options:\n'
    '  --merge-runs\n  --simplify-redlines\n'
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

"""Open an Office package for editing: unzip it, lay out the XML, tidy Word runs.

Original implementation, MIT licensed.

Usage:
    python unpack.py <office_file> <output_dir> [--merge-runs true|false]
                                                [--simplify-redlines true|false]

The parts are extracted under the destination directory (a member name that
would escape it is refused), every XML part is indented for reading, and a
DOCX additionally gets its revision wrappers and runs collapsed so an editor
sees one span per visual span. Curly quotes are written as numeric character
references on the way out, which keeps them stable across later re-saves.

``pack.py`` reverses this: it removes the layout whitespace again and zips the
tree back into a package.
"""

import argparse
import sys
import zipfile
from pathlib import Path

try:  # package-relative import, then the flat script directory
    from . import ooxml as ox
except ImportError:  # pragma: no cover - depends on how the caller set sys.path
    import ooxml as ox

try:
    from .helpers.merge_runs import merge_runs as collapse_runs
    from .helpers.simplify_redlines import simplify_redlines as collapse_revisions
except ImportError:  # pragma: no cover - flat script directory
    from helpers.merge_runs import merge_runs as collapse_runs
    from helpers.simplify_redlines import simplify_redlines as collapse_revisions


def unpack(
    input_file: str,
    output_directory: str,
    merge_runs: bool = True,
    simplify_redlines: bool = True,
) -> tuple[None, str]:
    """Extract one package; return (None, message) — the message carries errors."""
    source = Path(input_file)
    destination = Path(output_directory)

    if not source.exists():
        return None, f"Error: {input_file} does not exist"
    if source.suffix.lower() not in ox.OFFICE_SUFFIXES:
        return None, f"Error: {input_file} must be a .docx, .pptx, or .xlsx file"

    try:
        ox.extract_package(source, destination)
        parts = ox.xml_parts(destination)
        for part in parts:
            _lay_out(part)

        message = f"Unpacked {input_file} ({len(parts)} XML files)"
        if source.suffix.lower() == ".docx":
            if simplify_redlines:
                revisions, _ = collapse_revisions(str(destination))
                message += f", simplified {revisions} tracked changes"
            if merge_runs:
                runs, _ = collapse_runs(str(destination))
                message += f", merged {runs} runs"

        for part in parts:
            _reference_quotes(part)
        return None, message
    except zipfile.BadZipFile:
        return None, f"Error: {input_file} is not a valid Office file"
    except Exception as exc:
        return None, f"Error unpacking: {exc}"


def _lay_out(part: Path) -> None:
    """Indent one part; a part that cannot be parsed is left byte-identical."""
    try:
        doc = ox.parse_file(part)
    except Exception:
        return
    ox.indent_document(doc)
    ox.write_document(part, doc)


def _reference_quotes(part: Path) -> None:
    try:
        text = part.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return
    part.write_text(ox.escape_smart_quotes(text), encoding="utf-8")


def _boolean(value: str) -> bool:
    return value.strip().lower() == "true"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unpack an Office file (DOCX, PPTX, XLSX) for editing")
    parser.add_argument("input_file", help="Office file to unpack")
    parser.add_argument("output_directory", help="Directory the parts are extracted into")
    parser.add_argument(
        "--merge-runs",
        type=_boolean,
        default=True,
        metavar="true|false",
        help="Join adjacent runs with identical formatting (DOCX only, default: true)",
    )
    parser.add_argument(
        "--simplify-redlines",
        type=_boolean,
        default=True,
        metavar="true|false",
        help="Join adjacent tracked changes by one author (DOCX only, default: true)",
    )
    arguments = parser.parse_args()

    _, report = unpack(
        arguments.input_file,
        arguments.output_directory,
        merge_runs=arguments.merge_runs,
        simplify_redlines=arguments.simplify_redlines,
    )
    print(report)
    if "Error" in report:
        sys.exit(1)