#!/usr/bin/env python3
"""Render every page of a PDF to a PNG that an agent can read in one look.

Operands: input PDF, output directory. The directory is created when it does not
exist. Pages are written in document order as page_1.png, page_2.png, ... and
each write is reported on stdout, followed by a total:

    Saved page 1 as <dir>/page_1.png (size: (850, 1100))
    Converted 2 pages to PNG images

Rendering runs at 200 dpi through pypdfium2, the PDFium binding, so no external
binary (poppler, Ghostscript, LibreOffice) has to be installed. A page whose
longer side exceeds max_dim -- 1000 pixels by default -- is scaled down
proportionally before it is saved; smaller pages keep their rendered size. The
cap keeps a full page inside one image an agent can inspect without tiling,
while 200 dpi keeps small print legible before the downscale.

Exit 1 means nothing was rendered: wrong operand count, unreadable PDF, or a
missing renderer. The renderer is imported inside the function so that -h,
--help and --version still answer on a host without pypdfium2.

ai-engine project, MIT licensed -- see LICENSE.txt.
"""

import os
import sys

USAGE = "Usage: convert_pdf_to_images.py [input pdf] [output directory]"

#: Rendering resolution. PDF user space is 72 units per inch, so the scale
#: handed to PDFium is dpi / 72.
RENDER_DPI = 200
PDF_UNITS_PER_INCH = 72.0
DEFAULT_MAX_DIM = 1000


def _fit_within(image, max_dim):
    """Shrink proportionally so neither side exceeds max_dim; never enlarge."""
    width, height = image.size
    if width <= max_dim and height <= max_dim:
        return image
    from PIL import Image

    factor = min(max_dim / width, max_dim / height)
    size = (max(1, int(width * factor)), max(1, int(height * factor)))
    return image.resize(size, Image.LANCZOS)


def convert(pdf_path, output_dir, max_dim=DEFAULT_MAX_DIM) -> int:
    """Write one PNG per page; return the number of pages written."""
    import pypdfium2 as pdfium

    os.makedirs(output_dir, exist_ok=True)
    document = pdfium.PdfDocument(pdf_path)
    written = 0
    try:
        for index in range(len(document)):
            page = document[index]
            bitmap = page.render(scale=RENDER_DPI / PDF_UNITS_PER_INCH)
            try:
                image = _fit_within(bitmap.to_pil(), max_dim)
            finally:
                bitmap.close()
                page.close()
            target = os.path.join(output_dir, f"page_{index + 1}.png")
            image.save(target)
            written += 1
            print(f"Saved page {index + 1} as {target} (size: {image.size})")
    finally:
        document.close()
    print(f"Converted {written} pages to PNG images")
    return written


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 2:
        print(USAGE)
        return 1
    try:
        convert(args[0], args[1])
    except ImportError as exc:
        print(
            f"ERROR: PDF rendering needs pypdfium2 ({exc}). "
            "Install it with: pip install pypdfium2",
            file=sys.stderr,
        )
        return 1
    except Exception as exc:  # unreadable PDF, unwritable directory, bad render
        print(f"ERROR: cannot convert {args[0]}: {exc}", file=sys.stderr)
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

_SIG_SCRIPT = 'skills/external/document-utils/scripts/pdf/convert_pdf_to_images.py'
_SIG_DECLARED = ()
_SIG_HELP = (
    'usage: convert_pdf_to_images.py [options]\n'
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
