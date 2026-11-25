"""Reduce revision-wrapper noise, and name the author who added revisions.

Original implementation, MIT licensed. Two jobs, both about ``w:ins`` / ``w:del``
wrappers in ``word/document.xml``:

* ``simplify_redlines`` joins neighbouring wrappers of the same kind written by
  the same author. Timestamps are deliberately ignored: one editing pass emits
  many wrappers seconds apart, and a reader cares about the pass, not the clock.
* ``infer_author`` compares revision counts with the original package and
  returns the single author whose count grew, so a caller can validate that
  author's redlining without being told the name.
"""
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

_SIG_SCRIPT = '.specify/skills/document-utils/scripts/office/helpers/simplify_redlines.py'
_SIG_DECLARED = ()
_SIG_HELP = (
    'usage: simplify_redlines.py [options]\n'
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


from pathlib import Path

try:  # package-relative import, then the flat script directory
    from .. import ooxml as ox
except ImportError:  # pragma: no cover - depends on how the caller set sys.path
    import ooxml as ox


def simplify_redlines(input_dir: str) -> tuple[int, str]:
    """Join adjacent same-author revisions; return (count, message)."""
    doc_xml = Path(input_dir) / "word" / "document.xml"
    if not doc_xml.exists():
        return 0, f"Error: {doc_xml} not found"

    try:
        doc = ox.parse_file(doc_xml)
        root = doc.documentElement
        containers = list(ox.iter_elements(root, "p")) + list(ox.iter_elements(root, "tc"))
        merged = 0
        for container in containers:
            for tag in ("ins", "del"):
                merged += _merge_adjacent(container, tag)
        ox.write_document(doc_xml, doc)
        return merged, f"Simplified {merged} tracked changes"
    except Exception as exc:
        return 0, f"Error: {exc}"


def _merge_adjacent(container, tag: str) -> int:
    wrappers = ox.element_children(container, tag)
    merged = 0
    index = 0
    while index < len(wrappers) - 1:
        first, second = wrappers[index], wrappers[index + 1]
        same_author = ox.get_attr(first, "author") == ox.get_attr(second, "author")
        if same_author and ox.adjacent(first, second):
            for kid in list(second.childNodes):
                first.appendChild(kid)
            container.removeChild(second)
            wrappers.pop(index + 1)
            merged += 1
        else:
            index += 1
    return merged


def get_tracked_change_authors(doc_xml_path: Path) -> dict:
    """Count revisions per author in one document part ({} when unreadable)."""
    doc_xml_path = Path(doc_xml_path)
    if not doc_xml_path.is_file():
        return {}
    try:
        doc = ox.parse_file(doc_xml_path)
    except Exception:
        return {}
    return _count_authors(doc.documentElement)


def _count_authors(root) -> dict:
    authors: dict = {}
    for tag in ("ins", "del"):
        for element in ox.iter_elements(root, tag):
            author = ox.get_attr(element, "author")
            if author:
                authors[author] = authors.get(author, 0) + 1
    return authors


def _authors_in_package(docx_path: Path) -> dict:
    try:
        payload = ox.read_part(docx_path, "word/document.xml")
        if payload is None:
            return {}
        return _count_authors(ox.parse_string(payload).documentElement)
    except Exception:
        return {}


def infer_author(modified_dir: Path, original_docx: Path, default: str = "Claude") -> str:
    """Name the author whose revision count grew, or fall back to ``default``.

    Raises ValueError when several authors added revisions: picking one of them
    would be a guess, and validating the wrong author reports the wrong verdict.
    """
    modified = get_tracked_change_authors(Path(modified_dir) / "word" / "document.xml")
    if not modified:
        return default
    before = _authors_in_package(Path(original_docx))
    growth = {
        author: count - before.get(author, 0)
        for author, count in modified.items()
        if count - before.get(author, 0) > 0
    }
    if not growth:
        return default
    if len(growth) == 1:
        return next(iter(growth))
    raise ValueError(
        f"Multiple authors added new changes: {growth}. Cannot infer which author to validate."
    )


if __name__ == "__main__":
    raise RuntimeError("This module is a library; run office/unpack.py or office/pack.py instead.")