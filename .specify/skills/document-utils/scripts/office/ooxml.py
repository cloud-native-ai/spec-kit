"""Shared OOXML plumbing for the document-utils Office scripts.

Original implementation, MIT licensed. It owns three things the sibling modules
would otherwise each re-invent:

* the namespace names and package conventions an OPC package is built from,
* XML reading and writing that keeps namespace prefixes exactly as authored
  (minidom, not ElementTree, because ElementTree rewrites prefixes and an
  ``mc:Ignorable`` list points at prefixes by name),
* ZIP access that refuses to write outside the directory it was handed.

The standard library is sufficient. ``defusedxml`` (PSF-2.0) is used when it is
importable; without it the stdlib parser is still guarded, because every entry
point rejects DTD and entity declarations before parsing. No OOXML part needs a
DTD, so refusing one costs nothing and closes entity-expansion attacks.
"""

from __future__ import annotations

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

_SIG_SCRIPT = 'skills/external/document-utils/scripts/office/ooxml.py'
_SIG_DECLARED = ()
_SIG_HELP = (
    'usage: ooxml.py [options]\n'
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


import re
import shutil
import zipfile
from pathlib import Path
from xml.dom import Node, minidom

# --- namespace names (ECMA-376 / ISO-IEC 29500 part identifiers) ------------- #
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
S_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PR_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
MC_NS = "http://schemas.openxmlformats.org/markup-compatibility/2006"
XML_NS = "http://www.w3.org/XML/1998/namespace"
W14_NS = "http://schemas.microsoft.com/office/word/2010/wordml"
W15_NS = "http://schemas.microsoft.com/office/word/2012/wordml"
W16CID_NS = "http://schemas.microsoft.com/office/word/2016/wordml/cid"
W16CEX_NS = "http://schemas.microsoft.com/office/word/2018/wordml/cex"

#: The package suffixes these tools accept, and the folder each keeps its parts in.
OFFICE_SUFFIXES = (".docx", ".pptx", ".xlsx")
MAIN_PART_DIRS = {"word", "ppt", "xl"}
CONTENT_TYPES_PART = "[Content_Types].xml"

#: Curly quotes are written as numeric character references so that an editor
#: which re-saves the part as a different encoding cannot change them.
SMART_QUOTES = {
    "\u201c": "&#x201C;",
    "\u201d": "&#x201D;",
    "\u2018": "&#x2018;",
    "\u2019": "&#x2019;",
}

_DTD_PATTERN = re.compile(r"<!\s*(DOCTYPE|ENTITY)", re.IGNORECASE)


class PackageError(ValueError):
    """A package or part is unsafe or unusable; the message says which and why."""


# --- XML input and output --------------------------------------------------- #
def parse_string(text) -> minidom.Document:
    """Parse XML text into a minidom document, refusing DTD/entity declarations."""
    if isinstance(text, bytes):
        text = text.decode("utf-8")
    if _DTD_PATTERN.search(text):
        raise PackageError("DTD or entity declaration in an OOXML part; refusing to parse")
    try:
        from defusedxml import minidom as hardened
    except ImportError:
        return minidom.parseString(text)
    return hardened.parseString(text)


def parse_file(path) -> minidom.Document:
    """Parse one part from disk. Raises PackageError or an XML syntax error."""
    return parse_string(Path(path).read_text(encoding="utf-8"))


def document_bytes(doc: minidom.Document) -> bytes:
    """Serialize a document as UTF-8 with an XML declaration."""
    return doc.toxml(encoding="UTF-8")


def write_document(path, doc: minidom.Document) -> None:
    Path(path).write_bytes(document_bytes(doc))


def escape_smart_quotes(text: str) -> str:
    for char, reference in SMART_QUOTES.items():
        text = text.replace(char, reference)
    return text


# --- node helpers (prefix based: minidom keeps tags as authored) ------------- #
def local_name(node) -> str:
    """The name without its prefix: ``w:t`` -> ``t``."""
    name = getattr(node, "tagName", None) or getattr(node, "name", "")
    return name.rsplit(":", 1)[-1]


def is_element(node, name: str | None = None) -> bool:
    if node.nodeType != Node.ELEMENT_NODE:
        return False
    return name is None or local_name(node) == name


def element_children(node, name: str | None = None) -> list:
    return [kid for kid in node.childNodes if is_element(kid, name)]


def iter_elements(root, name: str | None = None):
    """Yield elements in document order, root included."""
    stack = [root]
    while stack:
        node = stack.pop()
        if node.nodeType != Node.ELEMENT_NODE:
            continue
        if name is None or local_name(node) == name:
            yield node
        stack.extend(reversed(node.childNodes))


def get_attr(node, name: str):
    """Read an attribute by local name, whatever prefix carries it."""
    if not node.attributes:
        return None
    for index in range(node.attributes.length):
        attr = node.attributes.item(index)
        if local_name(attr) == name:
            return attr.value
    return None


def has_attr(node, name: str) -> bool:
    return get_attr(node, name) is not None


def set_attr(node, name: str, value: str) -> None:
    node.setAttribute(name, value)


def text_of(node) -> str:
    """The concatenated text and CDATA children of one element."""
    parts = []
    for kid in node.childNodes:
        if kid.nodeType in (Node.TEXT_NODE, Node.CDATA_SECTION_NODE):
            parts.append(kid.data)
    return "".join(parts)


def set_text(node, text: str) -> None:
    for kid in list(node.childNodes):
        if kid.nodeType in (Node.TEXT_NODE, Node.CDATA_SECTION_NODE):
            node.removeChild(kid)
    node.appendChild(node.ownerDocument.createTextNode(text))


def first_child(node, name: str):
    for kid in node.childNodes:
        if is_element(kid, name):
            return kid
    return None


def ns_prefixes(node, namespace: str) -> set:
    """Prefixes bound to a namespace URI, collected from the node up to the root.

    minidom keeps prefixes as authored and does not resolve namespaces, so a
    namespace-aware lookup has to read the declarations itself.
    """
    prefixes = set()
    current = node
    while current is not None and current.nodeType == Node.ELEMENT_NODE:
        for index in range(current.attributes.length):
            attr = current.attributes.item(index)
            if attr.value != namespace:
                continue
            if attr.name == "xmlns":
                prefixes.add("")
            elif attr.name.startswith("xmlns:"):
                prefixes.add(attr.name.split(":", 1)[1])
        current = current.parentNode
    return prefixes


def get_attr_ns(node, prefixes, name: str):
    """Read an attribute by local name restricted to the given prefixes."""
    if not node.attributes:
        return None
    for index in range(node.attributes.length):
        attr = node.attributes.item(index)
        prefix, _, local = attr.name.rpartition(":")
        if local == name and prefix in prefixes:
            return attr.value
    return None


def remove_node(node) -> None:
    if node.parentNode is not None:
        node.parentNode.removeChild(node)


def unwrap_node(node) -> None:
    """Replace an element with its children, keeping their order and position."""
    parent = node.parentNode
    if parent is None:
        return
    for kid in list(node.childNodes):
        parent.insertBefore(kid, node)
    parent.removeChild(node)


def append_element(doc: minidom.Document, parent, tag: str, attrs=None):
    """Create ``tag`` (a prefixed name the root already declares) under parent."""
    element = doc.createElement(tag)
    for key, value in (attrs or {}).items():
        element.setAttribute(key, str(value))
    parent.appendChild(element)
    return element


def adjacent(elem1, elem2) -> bool:
    """True when only whitespace text or comments sit between two siblings."""
    node = elem1.nextSibling
    while node is not None and node is not elem2:
        if node.nodeType == Node.ELEMENT_NODE:
            return False
        if node.nodeType == Node.TEXT_NODE and node.data.strip():
            return False
        node = node.nextSibling
    return node is elem2


# --- layout whitespace ------------------------------------------------------ #
def strip_layout_whitespace(doc: minidom.Document) -> None:
    """Drop indentation and comments between elements, never inside text runs.

    ``*:t`` elements and anything marked ``xml:space="preserve"`` keep their
    children untouched: that whitespace is document content, not layout.
    """
    for element in iter_elements(doc.documentElement):
        if local_name(element) == "t" or get_attr(element, "space") == "preserve":
            continue
        for kid in list(element.childNodes):
            if kid.nodeType == Node.COMMENT_NODE:
                element.removeChild(kid)
            elif kid.nodeType == Node.TEXT_NODE and not kid.data.strip():
                element.removeChild(kid)


def indent_document(doc: minidom.Document, indent: str = "  ") -> None:
    """Pretty-print element-only content, leaving mixed content byte-stable.

    An element that carries any text of its own is skipped, so a run's text and
    the spaces inside ``w:t`` survive the round trip unchanged.
    """

    def layout(element, depth):
        if get_attr(element, "space") == "preserve":
            return
        kids = list(element.childNodes)
        elements = [kid for kid in kids if kid.nodeType == Node.ELEMENT_NODE]
        if not elements:
            return
        for kid in kids:
            if kid.nodeType in (Node.TEXT_NODE, Node.CDATA_SECTION_NODE) and kid.data.strip():
                return
        for kid in kids:
            if kid.nodeType == Node.TEXT_NODE:
                element.removeChild(kid)
        pad = indent * (depth + 1)
        for kid in elements:
            element.insertBefore(doc.createTextNode("\n" + pad), kid)
            layout(kid, depth + 1)
        element.appendChild(doc.createTextNode("\n" + indent * depth))

    layout(doc.documentElement, 0)


# --- package (ZIP) access --------------------------------------------------- #
def xml_parts(directory) -> list:
    """Every ``*.xml`` and ``*.rels`` part under a directory, in stable order.

    Matching is by name, not by ``Path.suffix``: the package-root relationship
    part is called ``.rels``, which has no suffix at all.
    """
    root = Path(directory)
    found = [
        path
        for path in root.rglob("*")
        if path.is_file() and path.name.endswith((".xml", ".rels"))
    ]
    return sorted(found)


def _safe_target(destination: Path, member: str) -> Path:
    if member.startswith("/") or member.startswith("\\") or re.match(r"^[A-Za-z]:", member):
        raise PackageError(f"absolute path in package: {member}")
    target = (destination / member).resolve()
    try:
        target.relative_to(destination.resolve())
    except ValueError:
        raise PackageError(f"package member escapes the destination: {member}") from None
    return target


def extract_package(zip_path, destination) -> list:
    """Extract every file member, refusing absolute or traversing names."""
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    written = []
    with zipfile.ZipFile(zip_path, "r") as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            target = _safe_target(destination, info.filename)
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(info) as source, open(target, "wb") as sink:
                shutil.copyfileobj(source, sink)
            written.append(info.filename)
    return written


def package_names(zip_path) -> list:
    with zipfile.ZipFile(zip_path, "r") as archive:
        return [info.filename for info in archive.infolist() if not info.is_dir()]


def read_part(zip_path, name: str):
    """Return one part's bytes, or None when the package does not carry it."""
    with zipfile.ZipFile(zip_path, "r") as archive:
        try:
            return archive.read(name)
        except KeyError:
            return None


def write_package(zip_path, parts: dict) -> None:
    """Write a package: content types first, then the remaining parts by name."""
    zip_path = Path(zip_path)
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    order = [CONTENT_TYPES_PART] if CONTENT_TYPES_PART in parts else []
    order += sorted(name for name in parts if name != CONTENT_TYPES_PART)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for name in order:
            archive.writestr(name, parts[name])


def directory_parts(directory) -> dict:
    """Read an unpacked tree into the ``{member name: bytes}`` shape write_package takes."""
    root = Path(directory)
    parts = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            parts[path.relative_to(root).as_posix()] = path.read_bytes()
    return parts


def relationship_parts(directory) -> list:
    return sorted(path for path in Path(directory).rglob("*.rels") if path.is_file())


def resolve_target(unpacked_dir: Path, rels_file: Path, target: str) -> Path:
    """Resolve a relationship Target the way OPC defines it.

    A leading ``/`` is package-absolute; otherwise the base is the folder that
    owns the ``_rels`` directory (the package root for ``_rels/.rels``).
    """
    if target.startswith("/"):
        return (unpacked_dir / target.lstrip("/")).resolve()
    if rels_file.name == ".rels" and rels_file.parent.name == "_rels" and rels_file.parent.parent == unpacked_dir:
        return (unpacked_dir / target).resolve()
    return (rels_file.parent.parent / target).resolve()


def is_external_target(target: str) -> bool:
    return target.startswith(("http:", "https:", "mailto:", "ftp:")) or "://" in target

if __name__ == "__main__":
    raise RuntimeError("This module is a library; run office/validate.py, pack.py or unpack.py instead.")
