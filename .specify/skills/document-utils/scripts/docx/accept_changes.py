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

_SIG_SCRIPT = '.specify/skills/document-utils/scripts/docx/accept_changes.py'
_SIG_DECLARED = ()
_SIG_HELP = (
    'usage: accept_changes.py [options]\n'
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

"""Accept every tracked change in a DOCX, in Python, without LibreOffice.

Original implementation, MIT licensed.

Usage:
    python accept_changes.py <input_file> <output_file>

Accepting a revision means applying it to the markup: an insertion keeps its
content and loses its wrapper, a deletion loses its content, a moved span is
treated as the insertion/deletion pair it is, and a formatting revision keeps
the new formatting and loses the record of the old one. A deleted paragraph
mark joins that paragraph to the one after it, which is what a reader sees when
the revision is accepted in an editor.

The input package is never modified: parts are read, the prose parts are
transformed, and a new package is written to the output path. Parts without
revisions are copied byte-for-byte.
"""

import argparse
import re
import sys
import zipfile
from pathlib import Path

# The shared OOXML helpers live in the sibling office/ directory. That directory
# (not .specify/scripts/) is what goes on sys.path: .specify/scripts/ also holds a package named
# docx, which would shadow the python-docx library.
_OFFICE_DIR = Path(__file__).resolve().parent.parent / "office"
if str(_OFFICE_DIR) not in sys.path:
    sys.path.insert(0, str(_OFFICE_DIR))

import ooxml as ox  # noqa: E402 - path bootstrap above must run first

INSERTIONS = {"ins", "moveTo"}
DELETIONS = {"del", "moveFrom"}
RANGE_MARKERS = {
    "moveFromRangeStart",
    "moveFromRangeEnd",
    "moveToRangeStart",
    "moveToRangeEnd",
    "customXmlInsRangeStart",
    "customXmlInsRangeEnd",
    "customXmlDelRangeStart",
    "customXmlDelRangeEnd",
}
PROPERTY_REVISIONS = {
    "pPrChange",
    "rPrChange",
    "sectPrChange",
    "tblPrChange",
    "tblGridChange",
    "trPrChange",
    "tcPrChange",
    "numberingChange",
}
CELL_MARKERS = {"cellIns", "cellMerge"}
PROSE_PART = re.compile(r"^word/(document|footnotes|endnotes|comments|header\d*|footer\d*)\.xml$")


def accept_changes(input_file: str, output_file: str) -> tuple[None, str]:
    """Write a revision-free copy of a DOCX; return (None, message)."""
    source = Path(input_file)
    target = Path(output_file)

    if not source.exists():
        return None, f"Error: Input file not found: {input_file}"
    if source.suffix.lower() != ".docx":
        return None, f"Error: Input file is not a DOCX file: {input_file}"

    try:
        with zipfile.ZipFile(source, "r") as archive:
            parts = {
                info.filename: archive.read(info.filename)
                for info in archive.infolist()
                if not info.is_dir()
            }
    except zipfile.BadZipFile:
        return None, f"Error: {input_file} is not a valid DOCX package"
    except OSError as exc:
        return None, f"Error: Failed to read input file: {exc}"

    accepted = 0
    for name in sorted(parts):
        if not PROSE_PART.match(name):
            continue
        try:
            doc = ox.parse_string(parts[name])
        except Exception:
            continue
        count = accept_all(doc.documentElement)
        if count:
            parts[name] = ox.document_bytes(doc)
            accepted += count

    try:
        ox.write_package(target, parts)
    except OSError as exc:
        return None, f"Error: Failed to write output file: {exc}"

    problem = _verify_readable(target)
    if problem:
        return None, f"Error: {problem}"

    return None, f"Successfully accepted all tracked changes: {input_file} -> {output_file}"


def accept_all(root) -> int:
    """Apply every revision under one element; return how many were applied."""
    applied = 0
    for marker in _live(root, RANGE_MARKERS):
        ox.remove_node(marker)
        applied += 1

    applied += _join_deleted_paragraph_marks(root)
    applied += _drop_deleted_cells(root)

    for element in _live(root, PROPERTY_REVISIONS | CELL_MARKERS):
        ox.remove_node(element)
        applied += 1

    for element in _live(root, DELETIONS):
        ox.remove_node(element)
        applied += 1

    for element in _live(root, INSERTIONS):
        ox.unwrap_node(element)
        applied += 1

    return applied


def _attached(root, node) -> bool:
    """Whether a node is still in the tree (an earlier phase may have dropped it)."""
    current = node
    while current is not None:
        if current is root:
            return True
        current = current.parentNode
    return False


def _live(root, names):
    """Elements with one of ``names`` that are still attached, in document order."""
    return [
        element
        for element in ox.iter_elements(root)
        if ox.local_name(element) in names and _attached(root, element)
    ]


def _paragraph_mark_deleted(paragraph) -> bool:
    properties = ox.first_child(paragraph, "pPr")
    if properties is None:
        return False
    run_properties = ox.first_child(properties, "rPr")
    if run_properties is None:
        return False
    return any(ox.is_element(kid, "del") for kid in run_properties.childNodes)


def _join_deleted_paragraph_marks(root) -> int:
    """A deleted paragraph mark merges its paragraph into the next one."""
    joined = 0
    for paragraph in reversed(list(ox.iter_elements(root, "p"))):
        if not _paragraph_mark_deleted(paragraph):
            continue
        following = paragraph.nextSibling
        while following is not None and not ox.is_element(following, "p"):
            following = following.nextSibling
        if following is None:
            continue
        anchor = next(
            (kid for kid in following.childNodes if ox.is_element(kid) and not ox.is_element(kid, "pPr")),
            None,
        )
        for kid in list(paragraph.childNodes):
            if ox.is_element(kid, "pPr"):
                continue
            if anchor is None:
                following.appendChild(kid)
            else:
                following.insertBefore(kid, anchor)
        ox.remove_node(paragraph)
        joined += 1
    return joined


def _drop_deleted_cells(root) -> int:
    dropped = 0
    for cell in list(ox.iter_elements(root, "tc")):
        properties = ox.first_child(cell, "tcPr")
        if properties is None:
            continue
        if any(ox.is_element(kid, "cellDel") for kid in properties.childNodes):
            ox.remove_node(cell)
            dropped += 1
    return dropped


def _verify_readable(target: Path):
    """Open the result with python-docx when it is installed; report why not."""
    try:
        import docx as python_docx
    except ImportError:
        return None
    if not hasattr(python_docx, "Document"):
        return None
    try:
        python_docx.Document(str(target))
    except Exception as exc:
        return f"the written package does not open: {exc}"
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Accept all tracked changes in a DOCX file")
    parser.add_argument("input_file", help="Input DOCX carrying tracked changes")
    parser.add_argument("output_file", help="Output DOCX with the changes applied")
    arguments = parser.parse_args()

    _, report = accept_changes(arguments.input_file, arguments.output_file)
    print(report)
    if "Error" in report:
        sys.exit(1)