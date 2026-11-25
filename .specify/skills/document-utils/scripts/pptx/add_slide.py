"""Add one slide to an unpacked PPTX directory.

Usage: python add_slide.py <unpacked_dir> <source>

``<source>`` is either a slide part to copy (``slide2.xml``) or a layout part to
start from (``slideLayout2.xml``).  Both forms write the next free
``ppt/slides/slide<n>.xml``, give it a relationship file, register its content
type, and add a relationship to ``ppt/_rels/presentation.xml.rels``.

The presentation part itself is left alone: slide order belongs to
``<p:sldIdLst>``, and where the new slide belongs in that order is the caller's
decision, not this script's.  The element to insert is printed on stdout.

Nothing else in the tree is rewritten, so a hand-edited part keeps its own
formatting, namespace prefixes and comments.

spec-kit project, MIT licensed -- see LICENSE.txt.
"""

from __future__ import annotations

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

_SIG_SCRIPT = '.specify/skills/document-utils/scripts/pptx/add_slide.py'
_SIG_DECLARED = ()
_SIG_HELP = (
    'usage: add_slide.py [options]\n'
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
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import ooxml_parts as op  # noqa: E402 -- beside this file, after the path bootstrap


class AddSlideError(Exception):
    """The operand names something this directory does not contain."""


def _slides_dir(root: Path) -> Path:
    return root / "ppt" / "slides"


def _next_slide_name(root: Path) -> str:
    slides = _slides_dir(root)
    names = [p.name for p in slides.glob("slide*.xml")] if slides.is_dir() else []
    return f"slide{op.next_slide_number(names)}.xml"


def _group_shape(doc, sp_tree):
    """The mandatory ``<p:nvGrpSpPr>`` / ``<p:grpSpPr>`` pair of a shape tree."""
    p, a = op.NS["p"], op.NS["a"]
    nv = doc.createElementNS(p, "p:nvGrpSpPr")
    identifier = doc.createElementNS(p, "p:cNvPr")
    identifier.setAttribute("id", "1")
    identifier.setAttribute("name", "")
    nv.appendChild(identifier)
    nv.appendChild(doc.createElementNS(p, "p:cNvGrpSpPr"))
    nv.appendChild(doc.createElementNS(p, "p:nvPr"))
    sp_tree.appendChild(nv)

    props = doc.createElementNS(p, "p:grpSpPr")
    xfrm = doc.createElementNS(a, "a:xfrm")
    for tag in ("off", "chOff"):
        node = doc.createElementNS(a, "a:" + tag)
        node.setAttribute("x", "0")
        node.setAttribute("y", "0")
        xfrm.appendChild(node)
    for tag in ("ext", "chExt"):
        node = doc.createElementNS(a, "a:" + tag)
        node.setAttribute("cx", "0")
        node.setAttribute("cy", "0")
        xfrm.appendChild(node)
    props.appendChild(xfrm)
    sp_tree.appendChild(props)


def _blank_slide() -> "op.Document":
    """A slide part with an empty shape tree, ready for the caller's content.

    The shape tree still needs its group entry: a ``<p:spTree>`` without one is
    not a valid PresentationML slide, and PowerPoint refuses the package.
    """
    doc = op.new_document(op.NS["p"], "p:sld")
    root = doc.documentElement
    root.setAttribute("xmlns:a", op.NS["a"])
    root.setAttribute("xmlns:r", op.NS["r"])

    common = doc.createElementNS(op.NS["p"], "p:cSld")
    sp_tree = doc.createElementNS(op.NS["p"], "p:spTree")
    _group_shape(doc, sp_tree)
    common.appendChild(sp_tree)
    root.appendChild(common)

    override = doc.createElementNS(op.NS["p"], "p:clrMapOvr")
    override.appendChild(doc.createElementNS(op.NS["a"], "a:masterClrMapping"))
    root.appendChild(override)
    return doc


def _layout_relationships(layout_name: str) -> "op.Document":
    doc = op.new_document(op.RELATIONSHIPS_NS, "Relationships")
    op.add_relationship(doc, "rId1", op.RT_SLIDE_LAYOUT, f"../slideLayouts/{layout_name}")
    return doc


def create_from_layout(root: Path, layout_name: str) -> str:
    """Write a new slide bound to ``layout_name``; return the new part's name."""
    layout = root / "ppt" / "slideLayouts" / layout_name
    if not layout.is_file():
        raise AddSlideError(f"{layout} not found")

    dest = _next_slide_name(root)
    slides = _slides_dir(root)
    rels = slides / "_rels"
    rels.mkdir(parents=True, exist_ok=True)
    op.write_part(slides / dest, _blank_slide())
    op.write_part(rels / f"{dest}.rels", _layout_relationships(layout_name))
    return dest


def duplicate_slide(root: Path, source: str) -> str:
    """Copy a slide part and its relationships; return the new part's name.

    Speaker notes are not copied.  A notes slide belongs to one slide, and a
    second slide pointing at the same notes part would make the notes show up
    under both -- so the notes relationship is dropped and the notes part is
    left for ``clean.py`` to reclaim if nothing else references it.
    """
    slides = _slides_dir(root)
    src = slides / source
    if not src.is_file():
        raise AddSlideError(f"{src} not found")

    dest = _next_slide_name(root)
    (slides / dest).write_bytes(src.read_bytes())

    src_rels = slides / "_rels" / f"{source}.rels"
    if src_rels.is_file():
        doc = op.parse_file(src_rels)
        for rel in op.relationships(doc):
            if op.relationship_type(rel) == op.RT_NOTES_SLIDE:
                op.remove_element(rel)
        rels_dir = slides / "_rels"
        rels_dir.mkdir(parents=True, exist_ok=True)
        op.write_part(rels_dir / f"{dest}.rels", doc)
    return dest


def register_part(root: Path, dest: str) -> str:
    """Declare the new part's content type and relationship; return the rId."""
    content_types = root / "[Content_Types].xml"
    doc = op.parse_file(content_types)
    if op.add_override(doc, f"ppt/slides/{dest}", op.SLIDE_CONTENT_TYPE):
        op.write_part(content_types, doc)

    pres_rels = root / "ppt" / "_rels" / "presentation.xml.rels"
    doc = op.parse_file(pres_rels)
    target = f"slides/{dest}"
    existing = op.find_relationship(doc, op.RT_SLIDE, target)
    if existing is not None:
        return op.attr(existing, "Id")
    rid = op.next_relationship_id(doc)
    op.add_relationship(doc, rid, op.RT_SLIDE, target)
    op.write_part(pres_rels, doc)
    return rid


def suggested_slide_id(root: Path) -> int:
    """The id the printed ``<p:sldId>`` should carry."""
    pres = root / "ppt" / "presentation.xml"
    if not pres.is_file():
        return op.FIRST_SLIDE_ID
    return op.next_slide_id(op.parse_file(pres))


def add_slide(root: Path, source: str) -> tuple[str, str, int]:
    """Create the slide; return (new part name, relationship id, suggested id)."""
    if op.is_layout_name(source):
        dest = create_from_layout(root, source)
    else:
        dest = duplicate_slide(root, source)
    rid = register_part(root, dest)
    return dest, rid, suggested_slide_id(root)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        sys.stderr.write(
            "Usage: python add_slide.py <unpacked_dir> <source>\n"
            "\n"
            "<source> is one of:\n"
            "  slide2.xml        copy an existing slide\n"
            "  slideLayout2.xml  start a new slide from a layout\n"
            "\n"
            "List the layouts with: ls <unpacked_dir>/ppt/slideLayouts/\n"
        )
        return 1

    root = Path(argv[0])
    if not root.is_dir():
        sys.stderr.write(f"Error: {root} not found\n")
        return 1

    try:
        dest, rid, slide_id = add_slide(root, argv[1])
    except (AddSlideError, op.OoxmlError) as exc:
        sys.stderr.write(f"Error: {exc}\n")
        return 1
    except OSError as exc:
        sys.stderr.write(f"Error: {exc}\n")
        return 1

    print(f"Created {dest} from {argv[1]}")
    print(
        'Add to presentation.xml <p:sldIdLst>: '
        f'<p:sldId id="{slide_id}" r:id="{rid}"/>'
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))