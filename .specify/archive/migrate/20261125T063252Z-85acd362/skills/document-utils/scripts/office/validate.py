"""Check an Office package before it is handed to a reader.

Original implementation, MIT licensed.

Usage:
    python validate.py <path> [--original <original_file>] [--auto-repair]
                       [--author NAME] [--verbose|-v]

``<path>`` is either an unpacked directory or a packed .docx/.pptx/.xlsx file,
which is extracted to a temporary directory for the duration of the check. The
format is taken from the suffix of ``--original`` when it is given, otherwise
from ``<path>`` itself.

What is checked: XML well-formedness, namespace declarations, identifier
uniqueness and ranges, relationship and content-type inventories, the format's
own markup rules, and — when the format's Python library is installed — a round
trip that re-packs the parts and opens them. Schema (XSD) validation is no
longer part of this skill; the round trip and the structural checks replace it.

``--auto-repair`` fixes what is mechanically fixable before checking: text runs
whose edge whitespace needs ``xml:space="preserve"``, and Word identifiers that
fall outside the ranges the format reserves. ``--author`` names whose tracked
changes are compared against ``--original`` (DOCX only).
"""

import argparse
import sys
import tempfile
from pathlib import Path

try:  # package-relative import, then the flat script directory
    from . import ooxml as ox
except ImportError:  # pragma: no cover - depends on how the caller set sys.path
    import ooxml as ox

try:
    from .validators import DOCXValidator, PPTXValidator, RedliningValidator
except ImportError:  # pragma: no cover - flat script directory
    from validators import DOCXValidator, PPTXValidator, RedliningValidator


def main():
    parser = argparse.ArgumentParser(
        description="Validate an unpacked Office directory or a packed Office file",
        add_help=False,
    )
    parser.add_argument(
        "path",
        help="Unpacked directory, or a packed .docx/.pptx/.xlsx file",
    )
    parser.add_argument(
        "--original",
        default=None,
        help="Original package; enables the tracked-change comparison and names the format",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Report each check that passes as well as each that fails",
    )
    parser.add_argument(
        "--auto-repair",
        action="store_true",
        help="Repair whitespace preservation and out-of-range identifiers before checking",
    )
    parser.add_argument(
        "--author",
        default="Claude",
        help="Author whose tracked changes are compared with the original (default: Claude)",
    )
    parser.add_argument("-h", "--help", action="store_true", help="print this help and exit")
    arguments = parser.parse_args()
    if arguments.help:
        parser.print_help()
        sys.exit(0)

    path = Path(arguments.path)
    if not path.exists():
        parser.error(f"{path} does not exist")

    original = None
    if arguments.original:
        original = Path(arguments.original)
        if not original.is_file():
            parser.error(f"{original} is not a file")
        if original.suffix.lower() not in ox.OFFICE_SUFFIXES:
            parser.error(f"{original} must be a .docx, .pptx, or .xlsx file")

    suffix = (original or path).suffix.lower()
    if suffix not in ox.OFFICE_SUFFIXES:
        parser.error(
            f"Cannot determine file type from {path}. "
            "Use --original or provide a .docx/.pptx/.xlsx file."
        )

    with tempfile.TemporaryDirectory() as scratch:
        if path.is_file():
            try:
                ox.extract_package(path, Path(scratch))
            except Exception as exc:
                print(f"Error: {path} is not a readable Office package: {exc}", file=sys.stderr)
                sys.exit(2)
            tree = Path(scratch)
        elif path.is_dir():
            tree = path
        else:
            parser.error(f"{path} is neither a directory nor an Office file")

        if suffix == ".docx":
            checks = [DOCXValidator(tree, original, verbose=arguments.verbose)]
            if original is not None:
                checks.append(
                    RedliningValidator(tree, original, verbose=arguments.verbose, author=arguments.author)
                )
        elif suffix == ".pptx":
            checks = [PPTXValidator(tree, original, verbose=arguments.verbose)]
        else:
            print(f"Error: Validation not supported for file type {suffix}")
            sys.exit(1)

        if arguments.auto_repair:
            repairs = sum(check.repair() for check in checks)
            if repairs:
                print(f"Auto-repaired {repairs} issue(s)")

        passed = all([check.validate() for check in checks])

    if passed:
        print("All validations PASSED!")
    sys.exit(0 if passed else 1)


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

_SIG_SCRIPT = '.specify/skills/document-utils/scripts/office/validate.py'
_SIG_DECLARED = ('--author', '--auto-repair', '--original', '--verbose', '-v')
_SIG_HELP = (
    'usage: validate.py [options]\n'
    'options:\n'
    '  --author\n  --auto-repair\n  --original\n  --verbose\n  -v\n'
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
    main()