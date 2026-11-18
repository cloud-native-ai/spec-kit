#!/usr/bin/env python3
"""Fill a form that has no interactive fields by adding free-text annotations.

Operands: input PDF, fields.json, output PDF. fields.json declares the geometry
of every page and the text to place on it:

    pages        one record per page: page_number plus EITHER pdf_width and
                 pdf_height (boxes are top-down PDF points) OR image_width and
                 image_height (boxes are pixels of a rendered page image).
                 The presence of pdf_width is what selects the coordinate
                 space; a file must not mix the two.
    form_fields  page_number, description, label_bounding_box,
                 entry_bounding_box and entry_text {text, font, font_size,
                 font_color}. Only entry_text.text is written -- the label box
                 is documentation and review material, not ink.

Boxes are [x0, y0, x1, y1] with y growing downward. The PDF's own user space
grows upward from the bottom-left corner, so every box is flipped on the way in:
the annotation rectangle becomes (left, pdf_height - y1, right, pdf_height - y0).
Pixel boxes are additionally scaled by pdf_width / image_width and
pdf_height / image_height. A field with no text, or an empty string, is skipped
without error -- that is how an author leaves a field blank.

Each value becomes a FreeText annotation with no border and no background, so
the result reads as text printed on the form rather than as a sticky note. The
annotations are ordinary PDF content: they survive merging and printing, and the
document stays a plain PDF with no AcroForm.

Defaults when entry_text omits them: font "Arial", font_size 14, font_color
"000000" (hex RGB, no leading #).

Exit 1 means the output was not written: wrong operand count, unreadable input,
a page_number with no matching page record, or a missing pypdf.

ai-engine project, MIT licensed -- see LICENSE.txt.
"""

import json
import sys

USAGE = "Usage: fill_pdf_form_with_annotations.py [input pdf] [fields.json] [output pdf]"

DEFAULT_FONT = "Arial"
DEFAULT_FONT_SIZE = 14
DEFAULT_FONT_COLOR = "000000"


def transform_from_image_coords(bbox, image_width, image_height, pdf_width, pdf_height):
    """Pixel box -> PDF rectangle (left, bottom, right, top), flipping y."""
    x_scale = pdf_width / image_width
    y_scale = pdf_height / image_height
    left = bbox[0] * x_scale
    right = bbox[2] * x_scale
    top = pdf_height - bbox[1] * y_scale
    bottom = pdf_height - bbox[3] * y_scale
    return left, bottom, right, top


def transform_from_pdf_coords(bbox, pdf_height):
    """Top-down PDF point box -> PDF rectangle (left, bottom, right, top)."""
    return bbox[0], pdf_height - bbox[3], bbox[2], pdf_height - bbox[1]


def _page_record(pages, page_number):
    for record in pages:
        if record["page_number"] == page_number:
            return record
    return None


def _entry_rectangle(field, page_info, pdf_width, pdf_height):
    box = field["entry_bounding_box"]
    if "pdf_width" in page_info:
        return transform_from_pdf_coords(box, pdf_height)
    return transform_from_image_coords(
        box, page_info["image_width"], page_info["image_height"], pdf_width, pdf_height
    )


def fill_pdf_form(input_pdf_path, fields_json_path, output_pdf_path) -> int:
    """Place every non-empty entry text as an annotation; return how many."""
    from pypdf import PdfReader, PdfWriter
    from pypdf.annotations import FreeText

    with open(fields_json_path, encoding="utf-8") as stream:
        data = json.load(stream)

    reader = PdfReader(input_pdf_path)
    if reader.is_encrypted:
        reader.decrypt("")
    writer = PdfWriter(clone_from=reader)
    dimensions = {
        number: (float(page.mediabox.width), float(page.mediabox.height))
        for number, page in enumerate(reader.pages, start=1)
    }

    added = 0
    for field in data["form_fields"]:
        entry_text = field.get("entry_text") or {}
        text = entry_text.get("text")
        if not text:
            continue

        page_number = field["page_number"]
        if page_number not in dimensions:
            raise ValueError(
                f"page_number {page_number} is outside the document (1-{len(dimensions)})"
            )
        page_info = _page_record(data["pages"], page_number)
        if page_info is None:
            raise ValueError(f"no pages record for page_number {page_number}")
        pdf_width, pdf_height = dimensions[page_number]

        annotation = FreeText(
            text=text,
            rect=_entry_rectangle(field, page_info, pdf_width, pdf_height),
            font=entry_text.get("font", DEFAULT_FONT),
            font_size=f"{entry_text.get('font_size', DEFAULT_FONT_SIZE)}pt",
            font_color=entry_text.get("font_color", DEFAULT_FONT_COLOR),
            border_color=None,
            background_color=None,
        )
        writer.add_annotation(page_number=page_number - 1, annotation=annotation)
        added += 1

    with open(output_pdf_path, "wb") as stream:
        writer.write(stream)
    print(f"Successfully filled PDF form and saved to {output_pdf_path}")
    print(f"Added {added} text annotations")
    return added


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 3:
        print(USAGE)
        return 1
    try:
        fill_pdf_form(args[0], args[1], args[2])
    except ImportError as exc:
        print(
            f"ERROR: annotation filling needs pypdf ({exc}). "
            "Install it with: pip install pypdf",
            file=sys.stderr,
        )
        return 1
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: cannot fill {args[0]}: {exc}", file=sys.stderr)
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

_SIG_SCRIPT = 'skills/external/document-utils/scripts/pdf/fill_pdf_form_with_annotations.py'
_SIG_DECLARED = ()
_SIG_HELP = (
    'usage: fill_pdf_form_with_annotations.py [options]\n'
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
