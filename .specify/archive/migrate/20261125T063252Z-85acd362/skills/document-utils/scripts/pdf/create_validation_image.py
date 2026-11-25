#!/usr/bin/env python3
"""Draw the declared rectangles of one page onto that page's image for review.

Operands, in order: page number (1-based), fields.json path, input image path,
output image path. For every form_fields entry whose page_number matches, two
outlines are drawn on a copy of the input image:

    red   -- entry_bounding_box, where the value will be written
    blue  -- label_bounding_box, the text the entry belongs to

Both outlines are two pixels wide. The result is written to the output path in
the format its extension implies, and one line is printed:

    Created validation image at <output> with <n> bounding boxes

<n> counts rectangles, not fields: a matched field contributes two. Looking at
the overlay is how an author catches a box that drifted off its label or covers
a neighbouring field before any PDF is produced -- check_bounding_boxes.py
catches the arithmetic conflicts, this catches the ones only an eye can see.

This script is a registered entry in the script-interface contract: -h, --help
and --version answer before Pillow is imported, and an undeclared option is
refused. Its operands are positional; it declares no options of its own.

Exit 1 means no image was written: wrong operand count, a page number that is
not an integer, or unreadable input.

spec-kit project, MIT licensed -- see LICENSE.txt.
"""

import json
import sys

USAGE = (
    "Usage: create_validation_image.py [page number] [fields.json file] "
    "[input image path] [output image path]"
)

ENTRY_OUTLINE = "red"
LABEL_OUTLINE = "blue"
OUTLINE_WIDTH = 2


def create_validation_image(page_number, fields_json_path, input_path, output_path) -> int:
    """Overlay one page's rectangles; return the number of rectangles drawn."""
    from PIL import Image, ImageDraw

    with open(fields_json_path, encoding="utf-8") as stream:
        fields = json.load(stream)["form_fields"]

    image = Image.open(input_path)
    try:
        draw = ImageDraw.Draw(image)
        drawn = 0
        for field in fields:
            if field["page_number"] != page_number:
                continue
            draw.rectangle(field["entry_bounding_box"], outline=ENTRY_OUTLINE, width=OUTLINE_WIDTH)
            draw.rectangle(field["label_bounding_box"], outline=LABEL_OUTLINE, width=OUTLINE_WIDTH)
            drawn += 2
        image.save(output_path)
    finally:
        image.close()
    print(f"Created validation image at {output_path} with {drawn} bounding boxes")
    return drawn


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 4:
        print(USAGE)
        return 1
    try:
        page_number = int(args[0])
    except ValueError:
        print(USAGE)
        return 1
    try:
        create_validation_image(page_number, args[1], args[2], args[3])
    except ImportError as exc:
        print(
            f"ERROR: drawing the overlay needs Pillow ({exc}). "
            "Install it with: pip install Pillow",
            file=sys.stderr,
        )
        return 1
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: cannot create validation image: {exc}", file=sys.stderr)
        return 1
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

_SIG_SCRIPT = '.specify/skills/document-utils/scripts/pdf/create_validation_image.py'
_SIG_DECLARED = ()
_SIG_HELP = (
    'usage: create_validation_image.py [options]\n'
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
