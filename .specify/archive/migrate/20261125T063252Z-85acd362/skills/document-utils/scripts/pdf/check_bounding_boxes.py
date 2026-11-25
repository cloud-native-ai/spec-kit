#!/usr/bin/env python3
"""Audit the geometry of a hand-authored fields.json before anything is filled.

Operand: one fields.json path in the annotation-fill schema -- a top-level
"form_fields" list whose entries carry page_number, description,
label_bounding_box, entry_bounding_box and optionally entry_text.

Rectangles are [x0, y0, x1, y1] with y growing downward. The audit is purely
geometric, so it never needs to know whether the numbers are PDF points or
pixels; it only requires that one file stays in one coordinate space. Two rules
are enforced:

  * rectangles sharing a page must not overlap -- a label may not sit inside its
    own entry area, and no two fields may claim the same area;
  * an entry rectangle must be at least as tall as the font size its text will
    be drawn with, otherwise the text is clipped.

Findings go to stdout, one per line: the field count first, then either a single
SUCCESS line or FAILURE lines. The verdict lives in that text, not in the exit
status -- a completed audit exits 0 even when it reports failures, so a caller
reads the lines. Exit 1 means the audit could not run (wrong operand count,
unreadable or malformed input). At most 20 lines are emitted; the audit then
stops and says so, because a file with that many conflicts needs rewriting
rather than more diagnostics.

spec-kit project, MIT licensed -- see LICENSE.txt.
"""

import json
import sys
from dataclasses import dataclass

USAGE = "Usage: check_bounding_boxes.py [fields.json]"

#: Diagnostic budget: after this many lines the audit stops reporting.
MESSAGE_LIMIT = 20
STOP_LINE = "Aborting further checks; fix bounding boxes and try again"
SUCCESS_LINE = "SUCCESS: All bounding boxes are valid"
DEFAULT_FONT_SIZE = 14


@dataclass
class RectAndField:
    """One rectangle, the role it plays ("label" or "entry") and its owner."""

    rect: list
    rect_type: str
    field: dict


def _overlaps(first, second) -> bool:
    """True when two rectangles share interior area (touching edges do not)."""
    apart_horizontally = first[0] >= second[2] or first[2] <= second[0]
    apart_vertically = first[1] >= second[3] or first[3] <= second[1]
    return not (apart_horizontally or apart_vertically)


def _conflict_line(left: RectAndField, right: RectAndField) -> str:
    """Describe one overlap, naming both rectangles and their fields."""
    if left.field is right.field:
        return (
            "FAILURE: intersection between label and entry bounding boxes for "
            f"`{left.field['description']}` ({left.rect}, {right.rect})"
        )
    return (
        f"FAILURE: intersection between {left.rect_type} bounding box for "
        f"`{left.field['description']}` ({left.rect}) and {right.rect_type} "
        f"bounding box for `{right.field['description']}` ({right.rect})"
    )


def _height_line(rect: RectAndField, font_size, height) -> str:
    return (
        f"FAILURE: entry bounding box height ({height}) for "
        f"`{rect.field['description']}` is too short for the text content "
        f"(font size: {font_size}). Increase the box height or decrease the font size."
    )


def get_bounding_box_messages(fields_json_stream) -> list:
    """Return the audit lines for an open fields.json stream."""
    fields = json.load(fields_json_stream)["form_fields"]
    messages = [f"Read {len(fields)} fields"]

    rectangles = []
    for field in fields:
        rectangles.append(RectAndField(field["label_bounding_box"], "label", field))
        rectangles.append(RectAndField(field["entry_bounding_box"], "entry", field))

    def report(line: str):
        messages.append(line)
        if len(messages) >= MESSAGE_LIMIT:
            messages.append(STOP_LINE)
            return True
        return False

    found_problem = False
    for position, left in enumerate(rectangles):
        for right in rectangles[position + 1:]:
            if left.field["page_number"] != right.field["page_number"]:
                continue
            if not _overlaps(left.rect, right.rect):
                continue
            found_problem = True
            if report(_conflict_line(left, right)):
                return messages

        if left.rect_type != "entry":
            continue
        entry_text = left.field.get("entry_text") or {}
        font_size = entry_text.get("font_size", DEFAULT_FONT_SIZE)
        height = left.rect[3] - left.rect[1]
        if height < font_size:
            found_problem = True
            if report(_height_line(left, font_size, height)):
                return messages

    if not found_problem:
        messages.append(SUCCESS_LINE)
    return messages


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print(USAGE)
        return 1
    try:
        with open(args[0], encoding="utf-8") as stream:
            messages = get_bounding_box_messages(stream)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: cannot audit {args[0]}: {exc}", file=sys.stderr)
        return 1
    for line in messages:
        print(line)
    return 0

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

_SIG_SCRIPT = '.specify/skills/document-utils/scripts/pdf/check_bounding_boxes.py'
_SIG_DECLARED = ()
_SIG_HELP = (
    'usage: check_bounding_boxes.py [options]\n'
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
