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

_SIG_SCRIPT = 'skills/external/document-utils/scripts/office/pack.py'
_SIG_DECLARED = ('--original', '--validate')
_SIG_HELP = (
    'usage: pack.py [options]\n'
    'options:\n'
    '  --original\n  --validate\n'
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

"""Close an edited tree back into an Office package.

Original implementation, MIT licensed.

Usage:
    python pack.py <input_directory> <output_file> [--original <file>] [--validate true|false]

With ``--original`` the tree is checked first (and common defects repaired in
place) before anything is written; without it the tree is packed as it stands.
Packing removes the layout whitespace ``unpack.py`` added, keeps text runs
byte-exact, and writes ``[Content_Types].xml`` as the first member so a consumer
can identify the package without scanning it.
"""

import argparse
import sys
from pathlib import Path

try:  # package-relative import, then the flat script directory
    from . import ooxml as ox
except ImportError:  # pragma: no cover - depends on how the caller set sys.path
    import ooxml as ox

try:
    from .validators import DOCXValidator, PPTXValidator, RedliningValidator
except ImportError:  # pragma: no cover - flat script directory
    from validators import DOCXValidator, PPTXValidator, RedliningValidator

DEFAULT_AUTHOR = "Claude"


def pack(
    input_directory: str,
    output_file: str,
    original_file: str | None = None,
    validate: bool = True,
    infer_author_func=None,
) -> tuple[None, str]:
    """Pack one tree; return (None, message) — the message carries errors."""
    tree = Path(input_directory)
    package = Path(output_file)

    if not tree.is_dir():
        return None, f"Error: {tree} is not a directory"
    if package.suffix.lower() not in ox.OFFICE_SUFFIXES:
        return None, f"Error: {output_file} must be a .docx, .pptx, or .xlsx file"

    if validate and original_file:
        original = Path(original_file)
        if original.exists():
            passed, report = _check_tree(tree, original, package.suffix.lower(), infer_author_func)
            if report:
                print(report)
            if not passed:
                return None, f"Error: Validation failed for {tree}"

    parts = {}
    for member, payload in ox.directory_parts(tree).items():
        if member.endswith((".xml", ".rels")):
            try:
                doc = ox.parse_string(payload)
            except Exception as exc:
                return None, f"Error: {member} is not well-formed: {exc}"
            ox.strip_layout_whitespace(doc)
            payload = ox.document_bytes(doc)
        parts[member] = payload

    ox.write_package(package, parts)
    return None, f"Successfully packed {tree} to {output_file}"


def _check_tree(tree: Path, original: Path, suffix: str, infer_author_func=None) -> tuple[bool, str | None]:
    """Run the format's checks, repairing what is mechanically repairable."""
    lines = []
    if suffix == ".docx":
        author = DEFAULT_AUTHOR
        if infer_author_func is not None:
            try:
                author = infer_author_func(tree, original)
            except ValueError as exc:
                print(f"Warning: {exc} Using default author '{DEFAULT_AUTHOR}'.", file=sys.stderr)
        checks = [DOCXValidator(tree, original), RedliningValidator(tree, original, author=author)]
    elif suffix == ".pptx":
        checks = [PPTXValidator(tree, original)]
    else:
        return True, None

    repairs = sum(check.repair() for check in checks)
    if repairs:
        lines.append(f"Auto-repaired {repairs} issue(s)")
    passed = all([check.validate() for check in checks])
    if passed:
        lines.append("All validations PASSED!")
    return passed, "\n".join(lines) if lines else None


def _boolean(value: str) -> bool:
    return value.strip().lower() == "true"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pack a directory into a DOCX, PPTX, or XLSX file")
    parser.add_argument("input_directory", help="Unpacked Office document directory")
    parser.add_argument("output_file", help="Output Office file (.docx/.pptx/.xlsx)")
    parser.add_argument("--original", help="Original package the tree is validated against")
    parser.add_argument(
        "--validate",
        type=_boolean,
        default=True,
        metavar="true|false",
        help="Check and repair the tree before packing (default: true)",
    )
    arguments = parser.parse_args()

    _, report = pack(
        arguments.input_directory,
        arguments.output_file,
        original_file=arguments.original,
        validate=arguments.validate,
    )
    print(report)
    if "Error" in report:
        sys.exit(1)