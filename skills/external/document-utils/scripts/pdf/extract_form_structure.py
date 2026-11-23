#!/usr/bin/env python3
"""Recover the geometry of a form that has no interactive fields of its own.

Operands: input PDF, output JSON path. A scanned or flattened form still has
structure -- printed labels, ruled lines, small square boxes -- and that
structure is enough to place text accurately without guessing from a picture.
pdfplumber exposes the page's word, line and rectangle inventory; this script
filters that inventory into the four things a form filler needs and writes them
as JSON, alongside one record per page:

    pages          page_number, width, height (PDF points)
    labels         every extracted word: page, text, x0, top, x1, bottom
    lines          horizontal rules spanning more than half the page width:
                   page, y, x0, x1
    checkboxes     near-square rectangles 5-15 points a side: page, x0, top,
                   x1, bottom, center_x, center_y
    row_boundaries consecutive rule pairs per page: page, row_top, row_bottom,
                   row_height

Coordinates are top-down: the origin is the page's top-left corner and y grows
downward, which is the opposite of the PDF's own bottom-up user space. Every
number is rounded to one decimal. That convention is what lets the values be
used directly as the bounding boxes of fields.json with pdf_width/pdf_height
declared -- see references/pdf-forms.md.

The filters are deliberately conservative. A rule shorter than half the page
width is usually a cell divider or an underline, not a row boundary; a rectangle
outside the 5-15 point square window is usually a table cell or a decoration.
Round boxes, faint graphics and anything drawn as an image are not detected at
all, so a page can need visual estimation for some fields even when this script
succeeds -- the workflow's hybrid route covers that case.

Exit 1 means nothing was written: wrong operand count, unreadable PDF, or a
missing pdfplumber.

spec-kit project, MIT licensed -- see LICENSE.txt.
"""

import json
import sys

USAGE = "Usage: extract_form_structure.py <input.pdf> <output.json>"

#: A horizontal rule must span more than this fraction of the page width.
MIN_LINE_SPAN = 0.5
#: Side window for a rectangle to be read as a checkbox, in PDF points.
BOX_MIN_SIDE = 5.0
BOX_MAX_SIDE = 15.0
#: How far from square a checkbox may be and still count.
BOX_SQUARE_TOLERANCE = 2.0
#: Decimal places kept for every coordinate.
PRECISION = 1


def _coord(value) -> float:
    return round(float(value), PRECISION)


def _is_row_rule(line, page_width) -> bool:
    span = abs(float(line["x1"]) - float(line["x0"]))
    return span > page_width * MIN_LINE_SPAN


def _is_checkbox(rect) -> bool:
    width = float(rect["x1"]) - float(rect["x0"])
    height = float(rect["bottom"]) - float(rect["top"])
    return (
        BOX_MIN_SIDE <= width <= BOX_MAX_SIDE
        and BOX_MIN_SIDE <= height <= BOX_MAX_SIDE
        and abs(width - height) < BOX_SQUARE_TOLERANCE
    )


def _row_boundaries(lines) -> list:
    """Pair consecutive distinct rule heights into rows, page by page."""
    heights = {}
    for line in lines:
        heights.setdefault(line["page"], set()).add(line["y"])
    rows = []
    for page in sorted(heights):
        ordered = sorted(heights[page])
        for top, bottom in zip(ordered, ordered[1:]):
            rows.append({
                "page": page,
                "row_top": top,
                "row_bottom": bottom,
                "row_height": round(bottom - top, PRECISION),
            })
    return rows


def extract_form_structure(pdf_path) -> dict:
    """Return the page/label/line/checkbox/row inventory of a PDF."""
    import pdfplumber

    structure = {"pages": [], "labels": [], "lines": [], "checkboxes": [], "row_boundaries": []}
    with pdfplumber.open(pdf_path) as document:
        for number, page in enumerate(document.pages, start=1):
            structure["pages"].append({
                "page_number": number,
                "width": float(page.width),
                "height": float(page.height),
            })

            for word in page.extract_words():
                structure["labels"].append({
                    "page": number,
                    "text": word["text"],
                    "x0": _coord(word["x0"]),
                    "top": _coord(word["top"]),
                    "x1": _coord(word["x1"]),
                    "bottom": _coord(word["bottom"]),
                })

            for line in page.lines:
                if not _is_row_rule(line, float(page.width)):
                    continue
                structure["lines"].append({
                    "page": number,
                    "y": _coord(line["top"]),
                    "x0": _coord(line["x0"]),
                    "x1": _coord(line["x1"]),
                })

            for rect in page.rects:
                if not _is_checkbox(rect):
                    continue
                x0, x1 = float(rect["x0"]), float(rect["x1"])
                top, bottom = float(rect["top"]), float(rect["bottom"])
                structure["checkboxes"].append({
                    "page": number,
                    "x0": _coord(x0),
                    "top": _coord(top),
                    "x1": _coord(x1),
                    "bottom": _coord(bottom),
                    "center_x": _coord((x0 + x1) / 2),
                    "center_y": _coord((top + bottom) / 2),
                })

    structure["row_boundaries"] = _row_boundaries(structure["lines"])
    return structure


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 2:
        print(USAGE)
        return 1
    pdf_path, output_path = args
    print(f"Extracting structure from {pdf_path}...")
    try:
        structure = extract_form_structure(pdf_path)
        with open(output_path, "w", encoding="utf-8") as stream:
            json.dump(structure, stream, indent=2)
    except ImportError as exc:
        print(
            f"ERROR: structure extraction needs pdfplumber ({exc}). "
            "Install it with: pip install pdfplumber",
            file=sys.stderr,
        )
        return 1
    except Exception as exc:  # unreadable PDF, unwritable output
        print(f"ERROR: cannot extract structure from {pdf_path}: {exc}", file=sys.stderr)
        return 1
    print("Found:")
    print(f"  - {len(structure['pages'])} pages")
    print(f"  - {len(structure['labels'])} text labels")
    print(f"  - {len(structure['lines'])} horizontal lines")
    print(f"  - {len(structure['checkboxes'])} checkboxes")
    print(f"  - {len(structure['row_boundaries'])} row boundaries")
    print(f"Saved to {output_path}")
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

_SIG_SCRIPT = 'skills/external/document-utils/scripts/pdf/extract_form_structure.py'
_SIG_DECLARED = ()
_SIG_HELP = (
    'usage: extract_form_structure.py [options]\n'
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
