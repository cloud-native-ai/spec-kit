#!/usr/bin/env python3
"""Describe a PDF's interactive form fields as JSON, in reading order.

Operands: input PDF, output JSON path. The result is a list with one record per
fillable field, ordered by page and then top-to-bottom, left-to-right, so an
agent can walk it the way a person reads the form. Every record carries:

    field_id   qualified field name; a kid field is joined to its ancestors
               with dots ("address.street"), which is the name a value must
               be addressed by
    type       "text", "checkbox", "choice", "radio_group", or "unknown (/FT)"
    page       1-based page holding the field's widget
    rect       [left, bottom, right, top] in PDF user space -- y=0 is the
               BOTTOM of the page, unlike the top-down boxes of fields.json

Type-specific members:

    checkbox     checked_value / unchecked_value: the exact names to write,
                 taken from the widget's appearance states ("/Yes", "/Off")
    choice       choice_options: [{value, text}] -- value is what a filler
                 writes, text is what the form displays
    radio_group  radio_options: [{value, rect}] -- one entry per button, each
                 with its own rectangle, because the buttons of one group are
                 spread across the page

A radio group is reported once, from its parent field, with every button as an
option; a field whose widget cannot be found is reported on stdout and left out
of the JSON, because a value addressed to it could not be placed.

The sibling script fill_fillable_fields.py imports get_field_info() from this
module to validate a value file against the same description, so the two always
agree on names, pages and legal values.

Exit 1 means nothing was written: wrong operand count, unreadable PDF, or a
missing pypdf.

ai-engine project, MIT licensed -- see LICENSE.txt.
"""

import json
import sys

USAGE = "Usage: extract_form_field_info.py [input pdf] [output json]"

#: Ancestor walk limit: a malformed /Parent cycle must not hang the extraction.
MAX_FIELD_DEPTH = 64
OFF_STATE = "/Off"


def _resolve(value):
    """Follow an indirect reference; a direct object resolves to itself."""
    return value.get_object() if hasattr(value, "get_object") else value


def _open_reader(pdf_path):
    from pypdf import PdfReader

    reader = PdfReader(pdf_path)
    if reader.is_encrypted:
        reader.decrypt("")
    return reader


def get_full_annotation_field_id(annotation):
    """Qualified name of a widget: its own /T behind every ancestor /T."""
    parts = []
    node = _resolve(annotation)
    for _ in range(MAX_FIELD_DEPTH):
        if node is None:
            break
        name = node.get("/T")
        if name:
            parts.append(str(name))
        parent = node.get("/Parent")
        node = _resolve(parent) if parent is not None else None
    return ".".join(reversed(parts)) if parts else None


def _choice_option(state) -> dict:
    """One /Opt entry as {value, text}.

    ISO 32000-1 allows an option to be a plain string or an [export, display]
    pair. A plain string is both the value to write and the text shown.
    """
    if isinstance(state, (list, tuple)) and len(state) == 2:
        return {"value": str(state[0]), "text": str(state[1])}
    text = str(state)
    return {"value": text, "text": text}


def make_field_dict(field, field_id) -> dict:
    """Shape one terminal field (text, checkbox or choice) without its location."""
    record = {"field_id": field_id}
    kind = field.get("/FT")
    states = list(field.get("/_States_") or [])

    if kind == "/Tx":
        record["type"] = "text"
    elif kind == "/Btn":
        record["type"] = "checkbox"
        names = [str(state) for state in states]
        on = [name for name in names if name != OFF_STATE]
        if len(names) == 2 and len(on) == 1:
            record["checked_value"] = on[0]
            record["unchecked_value"] = OFF_STATE
        else:
            print(
                f"WARNING: checkbox `{field_id}` declares unexpected states {names}; "
                "its checked and unchecked values may be wrong -- verify the result visually."
            )
            record["checked_value"] = names[0] if names else OFF_STATE
            record["unchecked_value"] = names[1] if len(names) > 1 else OFF_STATE
    elif kind == "/Ch":
        record["type"] = "choice"
        record["choice_options"] = [_choice_option(state) for state in states]
    else:
        record["type"] = f"unknown ({kind})"
    return record


def _on_states(widget) -> list:
    """Selectable appearance states of one button widget, without /Off.

    A radio button keeps one appearance per state in /AP/N; a widget with a
    single appearance stream carries no state names at all and is skipped.
    """
    from pypdf.generic import StreamObject

    appearance = widget.get("/AP")
    if appearance is None:
        return []
    normal = _resolve(appearance).get("/N")
    if normal is None:
        return []
    normal = _resolve(normal)
    if isinstance(normal, StreamObject):
        return []
    return [str(key) for key in normal.keys() if str(key) != OFF_STATE]


def _rect(value):
    """A /Rect as a plain list, keeping the document's own numeric types."""
    return list(value) if value is not None else None


def _anchor_rect(record) -> list:
    options = record.get("radio_options")
    if options:
        return options[0].get("rect") or [0, 0, 0, 0]
    return record.get("rect") or [0, 0, 0, 0]


def _reading_order(record):
    """Page first, then top-to-bottom (PDF y grows upward), then left-to-right."""
    rect = _anchor_rect(record)
    return (record.get("page"), -rect[1], rect[0])


def get_field_info(reader) -> list:
    """Return every locatable field of an open PdfReader, in reading order."""
    fields = reader.get_fields() or {}
    records = {}
    radio_parents = set()

    for field_id, field in fields.items():
        if field.get("/Kids"):
            # A parent is not fillable itself. A button parent with kids is a
            # radio group, whose options are the kids' widgets.
            if field.get("/FT") == "/Btn":
                radio_parents.add(field_id)
            continue
        records[field_id] = make_field_dict(field, field_id)

    groups = {}
    for page_index, page in enumerate(reader.pages):
        for reference in page.get("/Annots") or []:
            widget = _resolve(reference)
            subtype = widget.get("/Subtype")
            if subtype is not None and str(subtype) != "/Widget":
                continue
            field_id = get_full_annotation_field_id(widget)
            if field_id in records:
                records[field_id]["page"] = page_index + 1
                records[field_id]["rect"] = _rect(widget.get("/Rect"))
            elif field_id in radio_parents:
                on = _on_states(widget)
                if len(on) != 1:
                    continue
                group = groups.get(field_id)
                if group is None:
                    group = {
                        "field_id": field_id,
                        "type": "radio_group",
                        "page": page_index + 1,
                        "radio_options": [],
                    }
                    groups[field_id] = group
                group["radio_options"].append({"value": on[0], "rect": _rect(widget.get("/Rect"))})

    located = []
    for record in records.values():
        if "page" not in record:
            print(f"Unable to determine location for field id: {record['field_id']}, ignoring")
            continue
        located.append(record)

    combined = located + list(groups.values())
    combined.sort(key=_reading_order)
    return combined


def write_field_info(pdf_path: str, json_output_path: str) -> list:
    """Extract one PDF's fields to JSON; return the records that were written."""
    records = get_field_info(_open_reader(pdf_path))
    with open(json_output_path, "w", encoding="utf-8") as stream:
        json.dump(records, stream, indent=2)
    print(f"Wrote {len(records)} fields to {json_output_path}")
    return records


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 2:
        print(USAGE)
        return 1
    try:
        write_field_info(args[0], args[1])
    except ImportError as exc:
        print(
            f"ERROR: field extraction needs pypdf ({exc}). "
            "Install it with: pip install pypdf",
            file=sys.stderr,
        )
        return 1
    except Exception as exc:  # unreadable PDF, unwritable output
        print(f"ERROR: cannot extract fields from {args[0]}: {exc}", file=sys.stderr)
        return 1
    return 0

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

_SIG_SCRIPT = 'skills/external/document-utils/scripts/pdf/extract_form_field_info.py'
_SIG_DECLARED = ()
_SIG_HELP = (
    'usage: extract_form_field_info.py [options]\n'
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

if __name__ == "__main__":
    sys.exit(main())
