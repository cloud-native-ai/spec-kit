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

_SIG_SCRIPT = '.specify/skills/document-utils/scripts/docx/comment.py'
_SIG_DECLARED = ('--author', '--initials', '--parent')
_SIG_HELP = (
    'usage: comment.py [options]\n'
    'options:\n'
    '  --author\n  --initials\n  --parent\n'
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

"""Add a comment, or a reply to one, to an unpacked DOCX.

Original implementation, MIT licensed.

Usage:
    python comment.py <unpacked_dir> <comment_id> "text" [--author NAME]
                      [--initials X] [--parent PARENT_ID]

A Word comment is four parts that must agree: the comment text (comments.xml),
its threading and resolved state (commentsExtended.xml), its stable identifiers
(commentsIds.xml) and its date-stamped extension record
(commentsExtensible.xml). This script writes all four, creates the parts from
the templates beside it when they are absent, and registers them in the
package's relationship and content-type inventories.

It does not place the markers: ``commentRangeStart`` / ``commentRangeEnd`` /
``commentReference`` belong in document.xml around the text the comment covers,
and the script prints the exact markup to add. A reply is threaded by pointing
its ``w15:paraIdParent`` at the parent comment's paragraph id.
"""

import argparse
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

# The shared OOXML helpers live in the sibling office/ directory; see the note
# in accept_changes.py for why office/ and not .specify/scripts/ goes on sys.path.
_OFFICE_DIR = Path(__file__).resolve().parent.parent / "office"
if str(_OFFICE_DIR) not in sys.path:
    sys.path.insert(0, str(_OFFICE_DIR))

import ooxml as ox  # noqa: E402 - path bootstrap above must run first

TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"
ID_CEILING = 0x7FFFFFFE

COMMENT_PARTS = (
    ("comments.xml", "w:comments"),
    ("commentsExtended.xml", "w15:commentsEx"),
    ("commentsIds.xml", "w16cid:commentsIds"),
    ("commentsExtensible.xml", "w16cex:commentsExtensible"),
)

RELATIONSHIP_TYPES = {
    "comments.xml": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments",
    "commentsExtended.xml": "http://schemas.microsoft.com/office/2011/relationships/commentsExtended",
    "commentsIds.xml": "http://schemas.microsoft.com/office/2016/09/relationships/commentsIds",
    "commentsExtensible.xml": "http://schemas.microsoft.com/office/2018/08/relationships/commentsExtensible",
}

CONTENT_TYPES = {
    "/word/comments.xml": "application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml",
    "/word/commentsExtended.xml": "application/vnd.openxmlformats-officedocument.wordprocessingml.commentsExtended+xml",
    "/word/commentsIds.xml": "application/vnd.openxmlformats-officedocument.wordprocessingml.commentsIds+xml",
    "/word/commentsExtensible.xml": "application/vnd.openxmlformats-officedocument.wordprocessingml.commentsExtensible+xml",
}

MARKER_GUIDE = """
Add these markers to word/document.xml. They are direct children of w:p, never
children of w:r, and the range covers the runs the comment is about:
  <w:commentRangeStart w:id="{cid}"/>
  <w:r>...the commented runs...</w:r>
  <w:commentRangeEnd w:id="{cid}"/>
  <w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="{cid}"/></w:r>"""

REPLY_GUIDE = """
A reply shares its parent's range. Nest the markers inside the parent's, keeping
the parent's outermost, and reference both ids:
  <w:commentRangeStart w:id="{pid}"/><w:commentRangeStart w:id="{cid}"/>
  <w:r>...the commented runs...</w:r>
  <w:commentRangeEnd w:id="{cid}"/><w:commentRangeEnd w:id="{pid}"/>
  <w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="{pid}"/></w:r>
  <w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="{cid}"/></w:r>"""


def add_comment(
    unpacked_dir: str,
    comment_id: int,
    text: str,
    author: str = "Claude",
    initials: str = "C",
    parent_id: int | None = None,
) -> tuple[str, str]:
    """Write one comment into the four comment parts; return (para_id, message)."""
    root = Path(unpacked_dir)
    word = root / "word"
    if not word.is_dir():
        return "", f"Error: {word} not found"

    documents = {}
    for name, _ in COMMENT_PARTS:
        documents[name] = _part_document(word / name, name)

    taken = _existing_ids(documents["comments.xml"], documents["commentsIds.xml"])
    para_id = _fresh_id(taken)
    durable_id = _fresh_id(taken | {int(para_id, 16)})
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    parent_para = None
    if parent_id is not None:
        parent_para = _paragraph_id(documents["comments.xml"], parent_id)
        if parent_para is None:
            return "", f"Error: Parent comment {parent_id} not found"

    _append_comment(documents["comments.xml"], comment_id, text, author, initials, stamp, para_id)
    _append_extension(documents["commentsExtended.xml"], para_id, parent_para)
    _append_identifier(documents["commentsIds.xml"], para_id, durable_id)
    _append_extensible(documents["commentsExtensible.xml"], durable_id, stamp)

    _register_parts(root)
    for name, _ in COMMENT_PARTS:
        _save(word / name, documents[name])

    kind = "reply" if parent_id is not None else "comment"
    return para_id, f"Added {kind} {comment_id} (para_id={para_id})"


# --- part plumbing ---------------------------------------------------------- #
def _part_document(path: Path, template_name: str):
    if path.is_file():
        return ox.parse_file(path)
    template = TEMPLATE_DIR / template_name
    return ox.parse_string(template.read_text(encoding="utf-8"))


def _save(path: Path, doc) -> None:
    payload = ox.document_bytes(doc).decode("utf-8")
    path.write_text(ox.escape_smart_quotes(payload), encoding="utf-8")


def _existing_ids(comments_doc, ids_doc) -> set:
    taken = set()
    for element in ox.iter_elements(comments_doc.documentElement, "p"):
        value = ox.get_attr(element, "paraId")
        if value:
            try:
                taken.add(int(value, 16))
            except ValueError:
                pass
    for element in ox.iter_elements(ids_doc.documentElement, "commentId"):
        for attribute in ("paraId", "durableId"):
            value = ox.get_attr(element, attribute)
            if value:
                try:
                    taken.add(int(value, 16))
                except ValueError:
                    pass
    return taken


def _fresh_id(taken: set) -> str:
    number = random.randint(1, ID_CEILING)
    while number in taken:
        number = random.randint(1, ID_CEILING)
    return f"{number:08X}"


def _paragraph_id(comments_doc, comment_id: int):
    for comment in ox.iter_elements(comments_doc.documentElement, "comment"):
        if ox.get_attr(comment, "id") != str(comment_id):
            continue
        for paragraph in ox.iter_elements(comment, "p"):
            value = ox.get_attr(paragraph, "paraId")
            if value:
                return value
    return None


def _register_parts(root: Path) -> None:
    """Make the four comment parts known to the package inventories."""
    rels_path = root / "word" / "_rels" / "document.xml.rels"
    if rels_path.is_file():
        rels = ox.parse_file(rels_path)
        declared = {
            ox.get_attr(node, "Target")
            for node in ox.iter_elements(rels.documentElement, "Relationship")
        }
        next_number = _next_relationship_number(rels)
        for target, rel_type in RELATIONSHIP_TYPES.items():
            if target in declared:
                continue
            ox.append_element(
                rels,
                rels.documentElement,
                "Relationship",
                {"Id": f"rId{next_number}", "Type": rel_type, "Target": target},
            )
            next_number += 1
        _save(rels_path, rels)

    ct_path = root / ox.CONTENT_TYPES_PART
    if ct_path.is_file():
        content_types = ox.parse_file(ct_path)
        declared = {
            ox.get_attr(node, "PartName")
            for node in ox.iter_elements(content_types.documentElement, "Override")
        }
        for part_name, content_type in CONTENT_TYPES.items():
            if part_name in declared:
                continue
            ox.append_element(
                content_types,
                content_types.documentElement,
                "Override",
                {"PartName": part_name, "ContentType": content_type},
            )
        _save(ct_path, content_types)


def _next_relationship_number(rels) -> int:
    highest = 0
    for node in ox.iter_elements(rels.documentElement, "Relationship"):
        rid = ox.get_attr(node, "Id") or ""
        if rid.startswith("rId") and rid[3:].isdigit():
            highest = max(highest, int(rid[3:]))
    return highest + 1


# --- comment markup --------------------------------------------------------- #
def _append_comment(doc, comment_id, text, author, initials, stamp, para_id) -> None:
    comment = ox.append_element(
        doc,
        doc.documentElement,
        "w:comment",
        {"w:id": comment_id, "w:author": author, "w:date": stamp, "w:initials": initials},
    )
    paragraph = ox.append_element(
        doc, comment, "w:p", {"w14:paraId": para_id, "w14:textId": "77777777"}
    )
    anchor_run = ox.append_element(doc, paragraph, "w:r")
    anchor_properties = ox.append_element(doc, anchor_run, "w:rPr")
    ox.append_element(doc, anchor_properties, "w:rStyle", {"w:val": "CommentReference"})
    ox.append_element(doc, anchor_run, "w:annotationRef")

    text_run = ox.append_element(doc, paragraph, "w:r")
    text_properties = ox.append_element(doc, text_run, "w:rPr")
    ox.append_element(doc, text_properties, "w:color", {"w:val": "000000"})
    ox.append_element(doc, text_properties, "w:sz", {"w:val": "20"})
    ox.append_element(doc, text_properties, "w:szCs", {"w:val": "20"})
    text_element = ox.append_element(doc, text_run, "w:t")
    if text[:1] in (" ", "\t") or text[-1:] in (" ", "\t"):
        text_element.setAttribute("xml:space", "preserve")
    text_element.appendChild(doc.createTextNode(text))


def _append_extension(doc, para_id, parent_para) -> None:
    attributes = {"w15:paraId": para_id, "w15:done": "0"}
    if parent_para:
        attributes["w15:paraIdParent"] = parent_para
    ox.append_element(doc, doc.documentElement, "w15:commentEx", attributes)


def _append_identifier(doc, para_id, durable_id) -> None:
    ox.append_element(
        doc,
        doc.documentElement,
        "w16cid:commentId",
        {"w16cid:paraId": para_id, "w16cid:durableId": durable_id},
    )


def _append_extensible(doc, durable_id, stamp) -> None:
    ox.append_element(
        doc,
        doc.documentElement,
        "w16cex:commentExtensible",
        {"w16cex:durableId": durable_id, "w16cex:dateUtc": stamp},
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add comments to an unpacked DOCX")
    parser.add_argument("unpacked_dir", help="Unpacked DOCX directory")
    parser.add_argument("comment_id", type=int, help="Comment id, unique within the document")
    parser.add_argument("text", help="Comment text")
    parser.add_argument("--author", default="Claude", help="Author name (default: Claude)")
    parser.add_argument("--initials", default="C", help="Author initials (default: C)")
    parser.add_argument("--parent", type=int, help="Parent comment id, when this is a reply")
    arguments = parser.parse_args()

    paragraph_id, report = add_comment(
        arguments.unpacked_dir,
        arguments.comment_id,
        arguments.text,
        arguments.author,
        arguments.initials,
        arguments.parent,
    )
    print(report)
    if "Error" in report:
        sys.exit(1)
    if arguments.parent is not None:
        print(REPLY_GUIDE.format(pid=arguments.parent, cid=arguments.comment_id))
    else:
        print(MARKER_GUIDE.format(cid=arguments.comment_id))