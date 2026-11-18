# PDF processing in depth

Internals, tuning and failure modes behind the recipes in
[pdf-operations.md](./pdf-operations.md) and the form workflow in
[pdf-forms.md](./pdf-forms.md). Read this page when a recipe is not enough: the
extraction is wrong, the rendering is slow, the file is damaged, or you need to
know what a library is actually doing to the document.

The whole stack is Python. The JavaScript routes (`pdf-lib`, `pdfjs-dist`) and
the command-line routes (`pdftotext`, `pdftoppm`, `pdfimages`, `qpdf`, `pdftk`)
that earlier versions of this skill documented are no longer part of it: every
capability they covered has a Python equivalent below, and nothing here needs a
system binary except optional OCR.

## pypdfium2 — rendering and fast text

PDFium is the PDF engine Chromium ships; `pypdfium2` binds it and bundles the
compiled library, so rendering works on a host with no poppler and no
Ghostscript.

### Document and page lifecycle

```python
import pypdfium2 as pdfium

document = pdfium.PdfDocument("input.pdf")     # path, bytes, or file object
try:
    print(len(document))                       # page count
    page = document[0]
    try:
        print(page.get_size())                 # (width, height) in PDF points
        print(page.get_rotation())             # 0 / 90 / 180 / 270
        bitmap = page.render(scale=200 / 72)
        try:
            image = bitmap.to_pil()            # PIL.Image, RGB
            image.save("page_1.png")
        finally:
            bitmap.close()
    finally:
        page.close()
finally:
    document.close()
```

Pages, bitmaps and text pages hold native memory that Python's garbage collector
does not account for. Close them in loops over long documents; the skill's
`convert_pdf_to_images.py` does exactly this.

### Render options

`page.render(...)` accepts:

| Argument | Effect |
|----------|--------|
| `scale` | Multiplier on PDF points. `dpi / 72` gives that dpi: 200 dpi → `200/72 ≈ 2.78` |
| `rotation` | Extra rotation in degrees, applied on top of the page's own `/Rotate` |
| `crop` | `(left, bottom, right, top)` margins removed from the page before rendering |
| `may_draw_forms` | Draw widget appearances (default `True`); `False` renders the page without form ink |
| `color_scheme` | Optional colour override, e.g. for dark-mode or high-contrast proofing |
| `fill_to_stroke` | Convert filled text to stroked text; useful for some print pipelines |

```python
bitmap = page.render(scale=300 / 72, rotation=90, crop=(20, 20, 20, 20))
```

`bitmap.to_pil()` yields an RGB image; pass it straight to Pillow for cropping,
resizing or OCR. For JPEG output use `image.save("page.jpg", quality=90)`.

### Text without a full parse

```python
textpage = page.get_textpage()
try:
    print(textpage.count_chars())
    print(textpage.get_text_range())           # whole page
    print(textpage.get_text_bounded(left=50, bottom=700, right=300, top=760))
    print(textpage.get_charbox(0))             # (left, bottom, right, top) of char 0
finally:
    textpage.close()
```

Character boxes are in **PDF user space** (bottom-up), unlike pdfplumber's
top-down boxes. `get_text_range()` is fast because PDFium already parsed the
page for rendering; it is a good first pass when you only need the words.

## pdfplumber — geometry and tables

pdfplumber parses the content stream into typed objects and exposes them as
lists of dictionaries. It is the tool for "where is this on the page", which is
what form geometry recovery needs.

### The object inventory

| Attribute | Contents |
|-----------|----------|
| `page.chars` | One dict per character: `text`, `x0`, `x1`, `top`, `bottom`, `y0`, `y1`, `size`, `fontname`, `adv`, `upright`, `non_stroking_color` |
| `page.extract_words()` | Characters grouped into words, same box keys plus `text` |
| `page.lines` | Straight line segments: `x0`, `x1`, `top`, `bottom`, `width`, `height` |
| `page.rects` | Rectangles (a filled box, a cell border, a tick box) |
| `page.curves` | Bézier paths — circles, rounded boxes, signatures |
| `page.images` | Raster images placed on the page |

Two coordinate conventions coexist: `top`/`bottom` are measured **downward from
the page's top edge**, while `y0`/`y1` are PDF user space (upward from the
bottom). Mixing them is the most common source of mirrored geometry.

```python
import pdfplumber

with pdfplumber.open("input.pdf") as pdf:
    page = pdf.pages[0]
    print(page.width, page.height)
    for char in page.chars[:3]:
        print(char["text"], char["x0"], char["top"], char["size"], char["fontname"])
```

### Restricting to a region

```python
region = page.crop((50, 100, 400, 220))        # (x0, top, x1, bottom), top-down
print(region.extract_text())
print(page.within_bbox((50, 100, 400, 220)).extract_words())
```

`crop` returns a page-like object whose coordinates stay in the original page's
space; `within_bbox` filters objects without changing the origin. Use them to
read one cell of a form, or to check what sits inside a proposed entry box.

`page.filter(predicate)` keeps only objects matching a test — for example
`page.filter(lambda obj: obj["object_type"] == "rect")` — which is how you drop
decorative graphics before looking for tick boxes.

### Table extraction settings

`extract_tables()` and `extract_table()` accept a settings dict. The defaults
look for ruling lines; a table without rules needs a text-based strategy:

```python
settings = {
    "vertical_strategy": "lines",       # or "text" when there are no rules
    "horizontal_strategy": "lines",     # or "text"
    "snap_tolerance": 3,                # join nearly-collinear lines
    "intersection_tolerance": 15,       # how close two lines must cross to count
    "join_tolerance": 3,
    "edge_min_length": 3,
    "text_tolerance": 3,
}
tables = page.extract_tables(settings)
```

Diagnose a bad extraction visually before changing settings — the debug image
draws the detected edges over the page:

```python
page.to_image(resolution=150).save("debug.png")
page.to_image(resolution=150).debug_tablefinder(settings).save("debug_edges.png")
```

`to_image` renders through pypdfium2, so it needs no external binary either.

## pypdf — document structure

### Objects and references

A PDF is a graph of numbered objects. pypdf hands you `IndirectObject` proxies
for anything reached through a reference; call `.get_object()` to reach the real
dictionary before reading its keys. `DictionaryObject.get_inherited(key)` walks
`/Parent` chains, which is how a widget finds the field type declared above it.

### The form field tree

| Key | Meaning |
|-----|---------|
| `/AcroForm` | Catalog entry holding `/Fields` and `/NeedAppearances` |
| `/FT` | Field type: `/Tx` text, `/Btn` button, `/Ch` choice, `/Sig` signature |
| `/T` | Partial name; the qualified name joins ancestors with dots |
| `/V` | Value. A name (`/Yes`) for buttons, a string for text and choice |
| `/Kids`, `/Parent` | Tree edges. A `/Btn` parent with kids is a radio group |
| `/Opt` | Choice options: strings, or `[export, display]` pairs |
| `/Ff` | Flag bits: `1 << 15` radio, `1 << 16` pushbutton, `1 << 17` combo (choice), `1 << 21` multi-select, `1 << 12` multiline (text) |
| `/AP`, `/AS` | Widget appearance dictionary and the currently selected state |

`reader.get_fields()` flattens the tree into `{qualified_name: Field}` and adds a
synthesized `/_States_` entry: the appearance state names for a button, the
`/Opt` array for a choice. `extract_form_field_info.py` builds its JSON from that
mapping plus each page's `/Annots`, which is where a field's rectangle and page
actually live.

### Writing values

`writer.update_page_form_field_values(page, {name: value}, auto_regenerate=False)`
sets `/V`, updates `/AS` for buttons and builds a text appearance for text and
choice fields. `auto_regenerate=False` leaves `/NeedAppearances` alone; the
skill's filler then sets it explicitly with `writer.set_need_appearances_writer(True)`.

Two details worth knowing:

* **Paired `/Opt`.** A list box appearance is built by joining `/Opt` entries as
  text, which raises `TypeError` when the document stores `[export, display]
  pairs`. `fill_fillable_fields.py` hands pypdf a string-only view of those
  options for the duration of the update and restores the document's own pairs
  immediately afterwards — no library global is patched, and the written file
  keeps its display text.
* **Radio kids.** Each button of a group is its own widget with its own `/AP/N`
  states. Writing the group's value selects one kid's state and turns the others
  `/Off`; the group's rectangle is not a single box, which is why the extractor
  reports one `radio_options` entry per button.

### Annotations

`pypdf.annotations.FreeText(text=..., rect=(left, bottom, right, top), font=...,
font_size="14pt", font_color="000000", border_color=None, background_color=None)`
builds a free-text annotation; `writer.add_annotation(page_number=n, annotation=a)`
attaches it to page `n` (0-based). `rect` is PDF user space, bottom-up. This is
the mechanism Route 2 of the form workflow uses, and it is also how you add a
margin note or a review comment to any PDF.

### Encryption and damage

```python
reader = PdfReader("input.pdf", password="secret")   # or reader.decrypt("secret")
```

`PdfReader(..., strict=False)` (the default) tolerates many malformed structures
and repairs cross-reference tables on the fly. It cannot invent missing content:
a truncated file still raises `PdfStreamError` ("EOF marker not found"). Recovery
for that case means re-exporting from the source application, not a library flag.

`writer.encrypt(user_password=..., owner_password=..., algorithm="AES-256")`
supports AES-256 (default), AES-128 and RC4-128; the older algorithms are for
compatibility with legacy viewers only.

## reportlab — generation internals

* **Flowables.** Platypus lays out `Paragraph`, `Table`, `Image`, `Spacer`,
  `PageBreak` and friends into frames. A `SimpleDocTemplate` owns one frame per
  page; `BaseDocTemplate` with `PageTemplate` and `Frame` gives you columns,
  margins and per-page furniture.
* **Page furniture.** `canvas.Canvas(..., onPage=callback)` or
  `doc.build(story, onFirstPage=..., onLaterPages=...)` draws headers, footers and
  page numbers on every page. Draw them in the callback, not in the story.
* **TableStyle commands** are `(command, (col_start, row_start), (col_end,
  row_end), value)` tuples; negative indices count from the end, so `(-1, -1)` is
  the last cell. Common commands: `BACKGROUND`, `TEXTCOLOR`, `FONTNAME`,
  `FONTSIZE`, `ALIGN`, `VALIGN`, `GRID`, `BOX`, `LINEBELOW`, `LEFTPADDING`,
  `SPAN`.
* **Paragraph markup** is a small XML subset: `<b>`, `<i>`, `<sub>`, `<super>`,
  `<br/>`, `<font face=... size=... color=...>`, `<a href=...>`. Escape `&`, `<`
  and `>` in data-derived text or the parser raises.
* **Fonts.** The 14 standard fonts need no embedding and cover Latin-1.
  Everything else needs `pdfmetrics.registerFont(TTFont(name, path))`; register
  before drawing, and register a bold/italic face separately if you use them.
* **Transparency.** `canvas.setFillAlpha(0.3)` / `setStrokeAlpha` affect
  subsequent drawing; a watermark drawn this way stays translucent in viewers
  that support PDF 1.4 transparency.

## Batch processing

Isolate failures per file so one damaged document cannot stop a run, and log
enough to find the offender afterwards:

```python
import logging
from pathlib import Path

from pypdf import PdfReader, PdfWriter

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger("pdf-batch")

merged = PdfWriter()
for path in sorted(Path("incoming").glob("*.pdf")):
    try:
        reader = PdfReader(str(path))
        if reader.is_encrypted and not reader.decrypt(""):
            log.error("skipping %s: needs a password", path.name)
            continue
        for page in reader.pages:
            merged.add_page(page)
        log.info("merged %s (%d pages)", path.name, len(reader.pages))
    except Exception as exc:
        log.error("skipping %s: %s", path.name, exc)

with open("merged.pdf", "wb") as out:
    merged.write(out)
```

The same shape works for extraction and rendering: one try/except per file, one
log line per outcome, no silent `pass`.

## Performance and memory

* **Render per page, close per page.** A 500-page document rendered into a list
  of PIL images holds gigabytes; render, save, close, move on.
* **Choose the dpi for the job.** 150–200 dpi for visual inspection, 300 dpi or
  more for OCR, 72 dpi when one point must equal one pixel (the overlay review in
  the form workflow).
* **Cap the long side for inspection.** The skill's converter caps at 1000 px so
  a whole page fits one image; raise `max_dim` only when small print must survive.
* **Parse once.** `pdfplumber.open` parses lazily per page; keep the context
  manager open across all pages of one document instead of reopening per page.
* **Split before heavy work.** For very large inputs, write page-range chunks
  with `PdfWriter.append(path, pages=(start, stop))` and process each chunk.
* **Text extraction cost.** `pypdf` is cheapest for a plain text dump,
  `pdfplumber` for coordinates and tables, PDFium for a fast read of an already
  rendered page. Pick by what you need, not by habit.

## Troubleshooting

| Symptom | Cause | Remedy |
|---------|-------|--------|
| `EOF marker not found` / `PdfStreamError` | Truncated or non-PDF file | Re-export from the source; `strict=False` cannot rebuild missing content |
| `FileNotDecryptedError` | Encrypted, no password supplied | `PdfReader(path, password=...)` or `reader.decrypt(...)`; the scripts try an empty password only |
| Extraction returns `""` on a scan | No text layer | OCR: render at 300 dpi, then `pytesseract.image_to_string` |
| Text reads `(cid:12)` | Embedded font without a usable encoding map | OCR the rendered page, or ask for a re-export with embedded fonts |
| Black boxes instead of sub/superscripts | Standard font lacks the glyph | Paragraph `<sub>` / `<super>` markup, or register a TTF |
| Columns interleave in extracted text | Content-stream order is not reading order | `extract_text(layout=True)`, or sort `extract_words()` by `top` then `x0` |
| `DeprecationError` on `merge_page` | Page not attached to a writer | `PdfWriter(clone_from=reader)` first, then merge onto `writer.pages` |
| Filled checkbox looks empty in one viewer | Appearance not regenerated | Keep `/NeedAppearances` true; verify in a second viewer |
| `TypeError: sequence item 0: expected str` while filling a list box | Paired `/Opt` reaching pypdf's appearance builder | Use `fill_fillable_fields.py`, which flattens the view locally and restores the pairs |
| Annotation text lands mirrored or offset | Wrong coordinate space or wrong image size declared | See the coordinate table in [pdf-forms.md](./pdf-forms.md); check `image_width`/`image_height` against the actual PNG |
| Table extraction returns `[]` | No ruling lines, or lines not detected | `vertical_strategy`/`horizontal_strategy` = `"text"`, then `debug_tablefinder` |

## Dependencies and licences

The pdf family imports only the packages below. Versions are what this
implementation was verified against; licences were read from the installed
distributions' licence texts and metadata, not assumed.

| Package | Version verified | Licence (SPDX) | Role in this family |
|---------|------------------|----------------|---------------------|
| `pypdf` | 7.1.0 | BSD-3-Clause | Field extraction, value filling, free-text annotations, page surgery |
| `pdfplumber` | 0.11.10 | MIT | Word/line/rectangle inventory for `extract_form_structure.py` |
| `pdfminer.six` | 20260107 | MIT | pdfplumber's parser (transitive) |
| `Pillow` | 13.0.0 | MIT-CMU | Validation overlay, crop refinement, image resizing |
| `pypdfium2` | 5.15.2 | Apache-2.0 OR BSD-3-Clause | Page rendering in `convert_pdf_to_images.py`; also pdfplumber's renderer |
| `reportlab` | 5.1.0 | BSD-3-Clause | PDF creation recipes; builds the test fixtures |
| `charset-normalizer` | 3.4.7 | MIT | Encoding detection (transitive via pdfminer.six, reportlab) |
| `cryptography` | 44.0.3 | Apache-2.0 OR BSD-3-Clause | Encrypted-PDF support (transitive via pdfminer.six) |

Bundled native components:

* `pypdfium2` wheels ship the PDFium binary (BSD-3-Clause) together with its
  third-party components — FreeType (FTL), libjpeg-turbo (IJG/BSD-style),
  libpng, zlib, Little CMS (MIT), ICU (Unicode License v3), Abseil
  (Apache-2.0), AGG (BSD-style). The bundled licence texts mention the GPL in
  three places, none of which puts a GPL component in the import face: the LLVM
  exception's GPLv2 compatibility clause, ICU's optional GPL alternative, and
  the GCC runtime library exception carried by musl builds.
* `Pillow` wheels bundle image codecs under their own permissive licences (for
  example AOM under BSD-3-Clause); the Pillow licence text enumerates them.

Optional, not imported by any script in this family:

| Component | Licence | Why optional |
|-----------|---------|--------------|
| `pytesseract` 0.3.13 | Apache-2.0 | OCR of scanned pages; documented in pdf-operations.md |
| Tesseract binary | Apache-2.0 (upstream declaration) | The engine `pytesseract` drives; must be on `PATH` |

Install the working set with:

```bash
pip install pypdf pdfplumber pypdfium2 Pillow reportlab
```

No GPL-licensed package is imported, and no external binary is required for
reading, creating, rearranging, rendering or form filling. Each script imports
its third-party libraries inside the functions that use them, so `-h`, `--help`
and `--version` answer even on a host where none of them is installed.