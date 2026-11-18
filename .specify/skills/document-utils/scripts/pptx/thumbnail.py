"""Render a presentation as labelled thumbnail grids for a quick visual read.

Usage: python thumbnail.py <input.pptx> [output_prefix] [--cols N]

Each slide becomes one cell, labelled with the slide part's file name
(``slide3.xml``) so a reviewer can move from the picture to the XML without
guessing which part produced it.  A slide marked hidden is drawn as a crossed
placeholder when the converter skips it, and labelled ``(hidden)`` either way.

The deck is read with python-pptx, converted to PDF by LibreOffice headless, and
rasterized with PDFium; Pillow composes the grids.  Large decks are split across
``<prefix>-1.jpg``, ``<prefix>-2.jpg``, ... so one image never becomes too tall
to read.

This is the template-analysis view: small cells, whole deck, one look.  For
pixel-level QA render the slides full size instead -- see references/pptx-qa.md.

ai-engine project, MIT licensed -- see LICENSE.txt.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

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

_SIG_SCRIPT = 'skills/external/document-utils/scripts/pptx/thumbnail.py'
_SIG_DECLARED = ('--cols',)
_SIG_HELP = (
    'usage: thumbnail.py [options]\n'
    'options:\n'
    '  --cols\n'
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
SCRIPTS_DIR = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import ooxml_parts as op  # noqa: E402 -- beside this file, after the path bootstrap

#: Cell geometry, in pixels.  A cell is one thumbnail plus its label band.
THUMBNAIL_WIDTH = 300
LABEL_BAND_RATIO = 0.10
GRID_PADDING = 20
BORDER_WIDTH = 2
JPEG_QUALITY = 95

#: Rasterization resolution.  100 dpi keeps a 10-inch slide at 1000 px, which
#: downscales to a readable cell without carrying a full-size render around.
RENDER_DPI = 100
PDF_POINTS_PER_INCH = 72

DEFAULT_COLS = 3
MAX_COLS = 6

#: Fallback cell size when the converter produced nothing to measure.
FALLBACK_SIZE = (1920, 1080)


class ThumbnailError(Exception):
    """The deck could not be read, converted or composed."""


def _require(module: str, purpose: str, install: str | None = None):
    """Import a runtime dependency, naming it plainly when it is absent."""
    try:
        return __import__(module)
    except ImportError as exc:
        raise ThumbnailError(
            f"{module} is required to {purpose}; install it with "
            f"'python -m pip install {install or module}'"
        ) from exc


def _pil():
    """Pillow's imaging entry points, or a plain statement of what is missing."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError as exc:
        raise ThumbnailError(
            "Pillow is required to compose the grids; install it with "
            "'python -m pip install Pillow'"
        ) from exc
    return Image, ImageDraw, ImageFont


def _label_font(size: int):
    """A built-in font at the requested size, on any Pillow the skill may meet."""
    _, _, ImageFont = _pil()
    try:
        return ImageFont.load_default(size=size)
    except TypeError:  # Pillow before 10.1 has no sized default font
        return ImageFont.load_default()


def _soffice_env() -> dict:
    """The environment LibreOffice runs in, as the office wrapper defines it.

    ``office/soffice.py`` owns that decision (headless video plugin, and the
    socket shim some sandboxes need).  A tree without the wrapper still gets a
    usable environment rather than an import failure.
    """
    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        from office.soffice import get_soffice_env
    except ImportError:
        return os.environ.copy()
    return get_soffice_env()


def slide_inventory(path: Path) -> list[tuple[str, bool]]:
    """(slide part file name, hidden) for every slide, in presentation order.

    The name has to be the one on disk: it is how a reviewer moves from a cell to
    the part that produced it.  python-pptx renumbers slide partnames in memory
    the first time ``.slides`` is read, so the real names are captured from the
    presentation's relationships before that happens and matched back by part
    identity afterwards.
    """
    pptx = _require("pptx", "read the slide deck", install="python-pptx")
    from pptx.opc.constants import RELATIONSHIP_TYPE as RT

    presentation = pptx.Presentation(str(path))
    part = presentation.part
    on_disk = {
        id(rel.target_part): Path(str(rel.target_part.partname)).name
        for rel in part.rels.values()
        if rel.reltype == RT.SLIDE and not rel.is_external
    }

    inventory = []
    for slide in presentation.slides:
        name = on_disk.get(id(slide.part), Path(str(slide.part.partname)).name)
        inventory.append((name, op.hidden_flag(slide.element.get("show"))))
    return inventory


def render_slide_images(path: Path, work_dir: Path) -> list[Path]:
    """Convert the deck to PDF, then rasterize one JPEG per exported page."""
    pdf_path = work_dir / f"{path.stem}.pdf"
    converted = subprocess.run(
        [
            "soffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(work_dir),
            str(path),
        ],
        capture_output=True,
        text=True,
        env=_soffice_env(),
        check=False,
    )
    if converted.returncode != 0 or not pdf_path.is_file():
        detail = (converted.stderr or converted.stdout or "").strip()
        raise ThumbnailError(
            "LibreOffice did not produce a PDF" + (f": {detail}" if detail else "")
        )

    pdfium = _require("pypdfium2", "rasterize the converted PDF")
    document = pdfium.PdfDocument(str(pdf_path))
    images = []
    try:
        for index in range(len(document)):
            bitmap = document[index].render(scale=RENDER_DPI / PDF_POINTS_PER_INCH)
            image = bitmap.to_pil().convert("RGB")
            target = work_dir / f"slide-{index + 1:03d}.jpg"
            image.save(target, "JPEG", quality=JPEG_QUALITY)
            images.append(target)
    finally:
        document.close()
    return images


def hidden_placeholder(size: tuple[int, int]):
    """A crossed light cell standing in for a slide the converter skipped."""
    Image, ImageDraw, _ = _pil()
    image = Image.new("RGB", size, "#F0F0F0")
    draw = ImageDraw.Draw(image)
    width = max(5, min(size) // 100)
    draw.line([(0, 0), (size[0] - 1, size[1] - 1)], fill="#CCCCCC", width=width)
    draw.line([(size[0] - 1, 0), (0, size[1] - 1)], fill="#CCCCCC", width=width)
    return image


def pair_slides(
    inventory: list[tuple[str, bool]], images: list[Path], work_dir: Path
) -> list[tuple[Path, str]]:
    """Match each slide to the picture that shows it, in presentation order.

    LibreOffice may or may not export hidden slides.  When the page count equals
    the slide count every slide has its own picture; when it equals the visible
    count the hidden ones get a placeholder.  Anything else is paired as far as
    the pictures reach, which is the honest reading of a partial export.
    """
    Image, _, _ = _pil()

    if images:
        with Image.open(images[0]) as first:
            size = first.size
    else:
        size = FALLBACK_SIZE

    positional = len(images) == len(inventory)
    pairs: list[tuple[Path, str]] = []
    cursor = 0
    for index, (name, hidden) in enumerate(inventory):
        label = f"{name} (hidden)" if hidden else name
        if positional:
            pairs.append((images[index], label))
            continue
        if hidden:
            placeholder = work_dir / f"hidden-{name}.jpg"
            hidden_placeholder(size).save(placeholder, "JPEG", quality=JPEG_QUALITY)
            pairs.append((placeholder, label))
        elif cursor < len(images):
            pairs.append((images[cursor], label))
            cursor += 1
    return pairs


def compose_grid(pairs: list[tuple[Path, str]], cols: int, width: int):
    """Lay the cells out in rows, each thumbnail above its own file-name label."""
    Image, ImageDraw, _ = _pil()

    label_band = max(12, int(width * LABEL_BAND_RATIO))
    font = _label_font(max(10, int(label_band * 0.6)))

    cells = []
    for image_path, label in pairs:
        with Image.open(image_path) as source:
            height = max(1, round(width * source.height / source.width))
            cell = source.convert("RGB").resize((width, height), Image.LANCZOS)
        cells.append((cell, label))

    rows = [cells[start : start + cols] for start in range(0, len(cells), cols)]
    row_heights = [max(cell.height for cell, _ in row) + label_band for row in rows]
    canvas_width = GRID_PADDING * (cols + 1) + width * cols
    canvas_height = GRID_PADDING * (len(rows) + 1) + sum(row_heights)
    canvas = Image.new("RGB", (canvas_width, canvas_height), "white")
    draw = ImageDraw.Draw(canvas)

    top = GRID_PADDING
    for row, row_height in zip(rows, row_heights):
        left = GRID_PADDING
        for cell, label in row:
            draw.rectangle(
                [
                    (left - BORDER_WIDTH, top - BORDER_WIDTH),
                    (left + width + BORDER_WIDTH - 1, top + cell.height + BORDER_WIDTH - 1),
                ],
                outline="gray",
                width=BORDER_WIDTH,
            )
            canvas.paste(cell, (left, top))
            draw.text(
                (left + width / 2, top + cell.height + label_band / 2),
                label,
                fill="black",
                font=font,
                anchor="mm",
            )
            left += width + GRID_PADDING
        top += row_height + GRID_PADDING
    return canvas


def write_grids(
    pairs: list[tuple[Path, str]], cols: int, width: int, output: Path
) -> list[str]:
    """Save one grid, or numbered grids when the deck outgrows a single image."""
    per_grid = cols * (cols + 1)
    written = []
    chunks = [pairs[start : start + per_grid] for start in range(0, len(pairs), per_grid)]
    for index, chunk in enumerate(chunks):
        if len(chunks) == 1:
            target = output
        else:
            target = output.parent / f"{output.stem}-{index + 1}{output.suffix}"
        target.parent.mkdir(parents=True, exist_ok=True)
        compose_grid(chunk, cols, width).save(target, "JPEG", quality=JPEG_QUALITY)
        written.append(str(target))
    return written


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render labelled thumbnail grids of a presentation's slides."
    )
    parser.add_argument("input", help="presentation to render (.pptx)")
    parser.add_argument(
        "output_prefix",
        nargs="?",
        default="thumbnails",
        help="file name stem for the grids (default: thumbnails)",
    )
    parser.add_argument(
        "--cols",
        type=int,
        default=DEFAULT_COLS,
        help=f"cells per row (default: {DEFAULT_COLS}, maximum: {MAX_COLS})",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    cols = args.cols
    if cols > MAX_COLS:
        print(f"Warning: Columns limited to {MAX_COLS}")
        cols = MAX_COLS
    if cols < 1:
        sys.stderr.write("Error: --cols must be at least 1\n")
        return 1

    path = Path(args.input)
    if not path.is_file() or path.suffix.lower() != ".pptx":
        sys.stderr.write(f"Error: Invalid PowerPoint file: {args.input}\n")
        return 1

    output = Path(f"{args.output_prefix}.jpg")
    try:
        inventory = slide_inventory(path)
        if not inventory:
            raise ThumbnailError("No slides found")
        with tempfile.TemporaryDirectory(prefix="pptx-thumbnails-") as work:
            work_dir = Path(work)
            images = render_slide_images(path, work_dir)
            pairs = pair_slides(inventory, images, work_dir)
            if not pairs:
                raise ThumbnailError("No slides found")
            written = write_grids(pairs, cols, THUMBNAIL_WIDTH, output)
    except ThumbnailError as exc:
        sys.stderr.write(f"Error: {exc}\n")
        return 1
    except Exception as exc:  # a converter, decoder or filesystem failure
        sys.stderr.write(f"Error: {exc}\n")
        return 1

    print(f"Created {len(written)} grid(s):")
    for name in written:
        print(f"  {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())