"""OOXML part plumbing shared by the PPTX entry points in this directory.

A .pptx file is an OPC package: a zip of XML parts joined by relationship files.
The scripts beside this one meet that package in two shapes -- still zipped
(``thumbnail.py``) or unpacked into a directory of parts (``add_slide.py``,
``clean.py``).  Both shapes need the same small amount of plumbing, and this
module owns it:

* the PresentationML, DrawingML and OPC namespace names, plus the relationship
  types and content types the PPTX scripts have to tell apart;
* parsing that refuses a DTD, because no OPC part carries one and an internal
  entity declaration is how a small part becomes an unbounded expansion;
* serialization through ``xml.dom.minidom``, which keeps every namespace
  declaration and every whitespace text node it read.  That fidelity is the
  point: an unpacked tree is hand-edited between script runs, so a rewrite of
  one relationship file must not renumber prefixes or reflow the rest of it.
  A prefix that a producer declared but never used still matters when an
  ``mc:Ignorable`` attribute names it, and a tree serializer that drops unused
  declarations would leave that attribute pointing at nothing;
* OPC target resolution.  A relationship target is relative to the directory of
  the part that owns the ``_rels`` file -- not to the ``_rels`` directory itself,
  which is the mistake that makes ``../media/image1.png`` resolve one level too
  high.

Pure library: no command line, no writes, nothing happens on import.

spec-kit project, MIT licensed -- see LICENSE.txt.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Iterable, Optional
from urllib.parse import unquote
from xml.dom import Node
from xml.dom.minidom import Document, Element, parseString

#: Prefixes used by PresentationML parts and by the two OPC documents every
#: package carries (``[Content_Types].xml`` and the ``.rels`` files).
NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
    "ct": "http://schemas.openxmlformats.org/package/2006/content-types",
}

RELATIONSHIPS_NS = NS["pr"]
CONTENT_TYPES_NS = NS["ct"]

#: Relationship types.  The suffix names the part kind; the prefix is the
#: officeDocument relationship namespace.  Matching the whole URI -- rather than
#: a substring such as "slide" -- is what keeps a slideLayout or slideMaster
#: relationship from being mistaken for a slide.
RT_SLIDE = NS["r"] + "/slide"
RT_SLIDE_LAYOUT = NS["r"] + "/slideLayout"
RT_SLIDE_MASTER = NS["r"] + "/slideMaster"
RT_NOTES_SLIDE = NS["r"] + "/notesSlide"
RT_OFFICE_DOCUMENT = NS["r"] + "/officeDocument"

#: Content type of a slide part, as registered in ``[Content_Types].xml``.
SLIDE_CONTENT_TYPE = (
    "application/vnd.openxmlformats-officedocument.presentationml.slide+xml"
)

#: The first slide id PowerPoint assigns.  Ids are ST_SlideId values (>= 256),
#: not ordinals, so a deck that starts at 256 continues at 257.
FIRST_SLIDE_ID = 256

#: A DTD -- or an entity declaration outside one -- is the only way an XML
#: document can ask the parser to expand something recursively.  expat never
#: fetches an external resource, so external-entity disclosure is out of reach;
#: internal expansion is not, and refusing the DTD closes it without pulling in
#: a third-party parser.
_DTD = re.compile(rb"<!\s*(?:DOCTYPE|ENTITY)", re.IGNORECASE)

_SLIDE_NAME = re.compile(r"slide(\d+)\.xml")
_LAYOUT_NAME = re.compile(r"slideLayout(\d+)\.xml")
_RID = re.compile(r"rId(\d+)")


class OoxmlError(Exception):
    """A part could not be read as XML, or is not shaped like an OPC part."""


# --------------------------------------------------------------------------- #
# Reading and writing parts
# --------------------------------------------------------------------------- #
def parse_bytes(data: bytes) -> Document:
    """Parse one XML part, refusing a DTD and reporting malformed XML plainly."""
    if _DTD.search(data):
        raise OoxmlError("XML part declares a DTD or an entity; refusing to parse it")
    try:
        return parseString(data)
    except Exception as exc:  # expat reports several distinct failure types
        raise OoxmlError(f"malformed XML part: {exc}") from exc


def parse_file(path: Path) -> Document:
    """Read and parse a part from an unpacked package directory."""
    return parse_bytes(Path(path).read_bytes())


def parse_member(container, name: str) -> Document:
    """Read and parse a part out of an open ``zipfile.ZipFile``."""
    return parse_bytes(container.read(name))


def serialize(doc: Document) -> bytes:
    """Render a document as UTF-8 XML with a declaration."""
    return doc.toxml(encoding="UTF-8")


def write_part(path: Path, doc: Document) -> None:
    """Serialize a document back to a part file."""
    Path(path).write_bytes(serialize(doc))


def new_document(namespace: str, qualified_root: str) -> Document:
    """Start a part whose root declares its own namespace.

    minidom writes exactly the attributes it is given, so the declaration is set
    here rather than assumed: a part without it is not namespace-well-formed.
    """
    doc = Document()
    root = doc.createElementNS(namespace, qualified_root)
    prefix = qualified_root.split(":")[0] if ":" in qualified_root else ""
    root.setAttribute("xmlns:" + prefix if prefix else "xmlns", namespace)
    doc.appendChild(root)
    return doc


# --------------------------------------------------------------------------- #
# Navigating a part
# --------------------------------------------------------------------------- #
def descendants(parent, namespace: str, local: str) -> list[Element]:
    """Every element with this namespace and local name, at any depth."""
    return list(parent.getElementsByTagNameNS(namespace, local))


def children(parent, namespace: str, local: str) -> list[Element]:
    """Direct children with this namespace and local name."""
    return [
        node
        for node in parent.childNodes
        if node.nodeType == Node.ELEMENT_NODE
        and node.namespaceURI == namespace
        and node.localName == local
    ]


def attr(node: Element, local: str, namespace: Optional[str] = None) -> str:
    """An attribute value by local name, optionally pinned to one namespace.

    Relationship ids are written ``r:id``.  Matching the local name keeps the
    reader working when a producer declares the same namespace under another
    prefix; pinning the namespace keeps ``id`` from matching ``r:id``.
    """
    for index in range(node.attributes.length):
        item = node.attributes.item(index)
        if item.localName != local:
            continue
        if namespace is None or item.namespaceURI == namespace:
            return item.value
    return ""


def set_attr(node: Element, local: str, value: str, namespace: Optional[str] = None,
             prefix: str = "") -> None:
    """Set an attribute, qualified when a namespace is given."""
    if namespace is None:
        node.setAttribute(local, value)
    else:
        node.setAttributeNS(namespace, f"{prefix}:{local}" if prefix else local, value)


def append_child(parent: Element, child: Element, indent: str = "  ") -> None:
    """Append a child and keep the surrounding pretty-printing readable."""
    doc = parent.ownerDocument
    tail = parent.lastChild
    if tail is not None and tail.nodeType == Node.TEXT_NODE and not tail.data.strip():
        parent.removeChild(tail)
    parent.appendChild(doc.createTextNode("\n" + indent))
    parent.appendChild(child)
    parent.appendChild(doc.createTextNode("\n"))


def remove_element(node: Element) -> None:
    """Detach a node together with the indentation that belonged to it."""
    parent = node.parentNode
    if parent is None:
        return
    previous = node.previousSibling
    parent.removeChild(node)
    if (
        previous is not None
        and previous.nodeType == Node.TEXT_NODE
        and not previous.data.strip()
    ):
        parent.removeChild(previous)


# --------------------------------------------------------------------------- #
# Relationships
# --------------------------------------------------------------------------- #
def relationships(doc) -> list[Element]:
    """The ``Relationship`` elements of a parsed ``.rels`` document."""
    return descendants(doc, RELATIONSHIPS_NS, "Relationship")


def relationship_type(rel: Element) -> str:
    return attr(rel, "Type")


def is_external(rel: Element) -> bool:
    """True when a relationship points outside the package."""
    return attr(rel, "TargetMode").lower() == "external"


def resolve_target(rels_file: Path, target: str, package_root: Path) -> Optional[Path]:
    """The package-relative path a relationship target names, or None.

    None means "not a part of this package": an external target, an empty one, a
    URL or fragment, or one that climbs out of the package directory.  ``..``
    segments are collapsed lexically, so a symlink inside the tree cannot
    redirect the answer outside the package.
    """
    if not target or "://" in target or target.startswith(("mailto:", "#")):
        return None
    target = unquote(target)
    root = Path(os.path.normpath(package_root))
    if target.startswith("/"):
        candidate = root / target.lstrip("/")
    else:
        candidate = Path(rels_file).parent.parent / target
    candidate = Path(os.path.normpath(candidate))
    try:
        return candidate.relative_to(root)
    except ValueError:
        return None


def referenced_parts(package_root: Path) -> set[Path]:
    """Every package-relative part named by any internal relationship.

    This is the flat union over all ``.rels`` files, not a walk from the package
    root: a part survives as long as some surviving relationship still names it.
    Callers prune relationships first, then ask again, until nothing changes.
    """
    root = Path(os.path.normpath(package_root))
    found: set[Path] = set()
    for rels_file in sorted(root.rglob("*.rels")):
        if not rels_file.is_file():
            continue
        for rel in relationships(parse_file(rels_file)):
            if is_external(rel):
                continue
            resolved = resolve_target(rels_file, attr(rel, "Target"), root)
            if resolved is not None:
                found.add(resolved)
    return found


def next_relationship_id(doc) -> str:
    """One past the highest ``rId<n>`` in a ``.rels`` document, or ``rId1``."""
    numbers = [
        int(match.group(1))
        for rel in relationships(doc)
        for match in [_RID.fullmatch(attr(rel, "Id"))]
        if match
    ]
    return f"rId{max(numbers) + 1 if numbers else 1}"


def add_relationship(doc, rid: str, rtype: str, target: str) -> Element:
    """Append an internal relationship to a ``.rels`` document."""
    root = doc.documentElement
    rel = doc.createElementNS(RELATIONSHIPS_NS, "Relationship")
    rel.setAttribute("Id", rid)
    rel.setAttribute("Type", rtype)
    rel.setAttribute("Target", target)
    append_child(root, rel)
    return rel


def find_relationship(doc, rtype: str, target: str) -> Optional[Element]:
    """The relationship with this type and target, if the document has one."""
    for rel in relationships(doc):
        if relationship_type(rel) == rtype and attr(rel, "Target") == target:
            return rel
    return None


# --------------------------------------------------------------------------- #
# Content types
# --------------------------------------------------------------------------- #
def add_override(doc, part_name: str, content_type: str) -> bool:
    """Register a part's content type.  True when an Override was added."""
    root = doc.documentElement
    wanted = "/" + part_name.lstrip("/")
    for override in descendants(doc, CONTENT_TYPES_NS, "Override"):
        if attr(override, "PartName") == wanted:
            return False
    node = doc.createElementNS(CONTENT_TYPES_NS, "Override")
    node.setAttribute("PartName", wanted)
    node.setAttribute("ContentType", content_type)
    append_child(root, node)
    return True


def remove_overrides(doc, part_names: Iterable[str]) -> bool:
    """Drop the Overrides of deleted parts.  True when anything was removed."""
    wanted = {"/" + name.lstrip("/") for name in part_names}
    changed = False
    for override in descendants(doc, CONTENT_TYPES_NS, "Override"):
        if attr(override, "PartName") in wanted:
            remove_element(override)
            changed = True
    return changed


# --------------------------------------------------------------------------- #
# Presentation-level facts
# --------------------------------------------------------------------------- #
def slide_id_elements(pres_doc) -> list[Element]:
    """The ``<p:sldId>`` entries, in the order the presentation shows them."""
    return descendants(pres_doc, NS["p"], "sldId")


def next_slide_id(pres_doc) -> int:
    """One past the highest slide id in use, or the first id PowerPoint assigns."""
    ids = [
        int(value)
        for value in (attr(node, "id") for node in slide_id_elements(pres_doc))
        if value.isdigit()
    ]
    return max(ids) + 1 if ids else FIRST_SLIDE_ID


def slide_relationships(pres_rels_doc) -> dict[str, str]:
    """Relationship id -> slide file name, for the presentation's own slides."""
    mapping: dict[str, str] = {}
    for rel in relationships(pres_rels_doc):
        target = attr(rel, "Target")
        if relationship_type(rel) == RT_SLIDE and target.startswith("slides/"):
            mapping[attr(rel, "Id")] = target[len("slides/"):]
    return mapping


def shown_slide_names(pres_doc, pres_rels_doc) -> list[str]:
    """Slide file names in presentation order, following ``<p:sldIdLst>``."""
    mapping = slide_relationships(pres_rels_doc)
    names = []
    for node in slide_id_elements(pres_doc):
        name = mapping.get(attr(node, "id", NS["r"]))
        if name is not None:
            names.append(name)
    return names


def slide_numbers(names: Iterable[str]) -> list[int]:
    """The numbers carried by ``slide<n>.xml`` names."""
    return [
        int(match.group(1))
        for match in (_SLIDE_NAME.fullmatch(name) for name in names)
        if match
    ]


def next_slide_number(names: Iterable[str]) -> int:
    numbers = slide_numbers(names)
    return max(numbers) + 1 if numbers else 1


def is_layout_name(name: str) -> bool:
    """True for a ``slideLayout<n>.xml`` operand (the create-from-layout form)."""
    return bool(_LAYOUT_NAME.fullmatch(name))


def hidden_flag(show: Optional[str]) -> bool:
    """Whether a slide's ``show`` attribute marks it hidden.

    The flag lives on the ``<p:sld>`` root (CT_Slide, ``show``, default true);
    ``<p:sldId>`` carries only an id and a relationship id, so reading it there
    would report every slide as visible.  Both spellings of false are accepted
    because the attribute is an xsd:boolean.
    """
    return (show or "").strip().lower() in ("0", "false")