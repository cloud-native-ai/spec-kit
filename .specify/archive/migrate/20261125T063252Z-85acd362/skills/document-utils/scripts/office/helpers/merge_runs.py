"""Collapse neighbouring Word runs that carry the same formatting.

Original implementation, MIT licensed. A run (``w:r``) is a span of text with
one property set. Editors and generators emit many tiny runs for one visual
span, which makes a redlined document hard to read and hard to edit. This
helper joins runs that a reader would see as one span:

* adjacent siblings only, with nothing but whitespace between them,
* identical run properties (``w:rPr``), compared without layout whitespace,
* inside any container, so runs wrapped in ``w:ins`` / ``w:del`` join too.

Two kinds of noise are removed first because they block joining without
changing what the document shows: spell/grammar markers (``w:proofErr``) and
revision-save identifiers (``w:rsid*`` attributes) on runs.
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

_SIG_SCRIPT = '.specify/skills/document-utils/scripts/office/helpers/merge_runs.py'
_SIG_DECLARED = ()
_SIG_HELP = (
    'usage: merge_runs.py [options]\n'
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


def merge_runs(input_dir: str) -> tuple[int, str]:
    """Join same-format runs in ``word/document.xml``; return (count, message)."""
    doc_xml = Path(input_dir) / "word" / "document.xml"
    if not doc_xml.exists():
        return 0, f"Error: {doc_xml} not found"

    try:
        doc = ox.parse_file(doc_xml)
        root = doc.documentElement

        for marker in list(ox.iter_elements(root, "proofErr")):
            ox.remove_node(marker)
        for run in list(ox.iter_elements(root, "r")):
            for index in range(run.attributes.length - 1, -1, -1):
                attr = run.attributes.item(index)
                if "rsid" in ox.local_name(attr).lower():
                    run.removeAttribute(attr.name)

        containers = {run.parentNode for run in ox.iter_elements(root, "r")}
        merged = sum(_merge_within(container) for container in containers)

        ox.write_document(doc_xml, doc)
        return merged, f"Merged {merged} runs"
    except Exception as exc:
        return 0, f"Error: {exc}"


def _properties_signature(run):
    """A run's formatting, normalized so indentation cannot mask equality."""
    properties = ox.first_child(run, "rPr")
    if properties is None:
        return None
    clone = properties.cloneNode(deep=True)
    for element in ox.iter_elements(clone):
        for kid in list(element.childNodes):
            if kid.nodeType == kid.TEXT_NODE and not kid.data.strip():
                element.removeChild(kid)
    return clone.toxml()


def _joinable(first, second) -> bool:
    if not ox.is_element(second, "r"):
        return False
    if not ox.adjacent(first, second):
        return False
    return _properties_signature(first) == _properties_signature(second)


def _merge_within(container) -> int:
    merged = 0
    for run in ox.element_children(container, "r"):
        while True:
            sibling = _next_element(run)
            if sibling is None or not _joinable(run, sibling):
                break
            for kid in list(sibling.childNodes):
                if ox.is_element(kid, "rPr"):
                    continue
                run.appendChild(kid)
            container.removeChild(sibling)
            merged += 1
        _join_text_nodes(run)
    return merged


def _next_element(node):
    sibling = node.nextSibling
    while sibling is not None:
        if sibling.nodeType == sibling.ELEMENT_NODE:
            return sibling
        sibling = sibling.nextSibling
    return None


def _join_text_nodes(run) -> None:
    """Fold adjacent w:t siblings into one, keeping whitespace semantics."""
    while True:
        texts = ox.element_children(run, "t")
        folded = False
        for previous, current in zip(texts, texts[1:]):
            if not ox.adjacent(previous, current):
                continue
            combined = ox.text_of(previous) + ox.text_of(current)
            ox.set_text(previous, combined)
            if combined[:1] in (" ", "\t") or combined[-1:] in (" ", "\t"):
                previous.setAttribute("xml:space", "preserve")
            elif ox.has_attr(previous, "space"):
                previous.removeAttribute("xml:space")
            run.removeChild(current)
            folded = True
            break
        if not folded:
            return


if __name__ == "__main__":
    raise RuntimeError("This module is a library; run office/unpack.py instead.")