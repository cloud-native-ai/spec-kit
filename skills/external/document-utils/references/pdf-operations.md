# Everyday PDF operations

Reading, creating and rearranging PDFs with the skill's Python stack. Form
filling has its own workflow: [pdf-forms.md](./pdf-forms.md). Rendering internals,
extraction tuning and troubleshooting: [pdf-reference.md](./pdf-reference.md).

## The stack

| Library | Licence | What it is for here |
|---------|---------|---------------------|
| `pypdf` | BSD-3-Clause | Page-level surgery: merge, split, rotate, crop, watermark, metadata, encryption, form fields, annotations |
| `pdfplumber` | MIT | Words, characters, rules and rectangles with coordinates; table extraction |
| `reportlab` | BSD | Creating PDFs: canvas drawing and flowing documents |
| `pypdfium2` | Apache-2.0 OR BSD-3-Clause | Rendering pages to images (PDFium), fast text access |
| `Pillow` | MIT-CMU | Image handling: crop, resize, overlay drawing |

Everything is importable Python. No Node package, no poppler, no qpdf, no pdftk
and no LibreOffice is needed for the operations on this page; the previous
toolchain's JavaScript and command-line routes were dropped in favour of these
five, and each recipe below states the Python equivalent.

## Reading

### Page count and plain text

```python
from pypdf import PdfReader

reader = PdfReader("report.pdf")
print(len(reader.pages))
text = "\n".join(page.extract_text() or "" for page in reader.pages)
```

`extract_text()` returns the page's text in content-stream order, which is not
always reading order: multi-column layouts and tables can interleave. When the
arrangement matters, use pdfplumber instead.

### Layout-aware text and tables

```python
import pdfplumber

with pdfplumber.open("report.pdf") as pdf:
    for number, page in enumerate(pdf.pages, start=1):
        print(f"--- page {number} ---")
        print(page.extract_text(layout=True))
        for table in page.extract_tables():
            for row in table:
                print(row)
```

`extract_tables()` returns a list of tables, each a list of rows, each row a list
of cell strings or `None`. Detection is driven by the page's rules and text
alignment; a table drawn without rules needs the settings described in
[pdf-reference.md](./pdf-reference.md).

To hand the rows to another tool, write CSV with the standard library — no
dataframe dependency is required:

```python
import csv

with pdfplumber.open("report.pdf") as pdf, open("tables.csv", "w", newline="", encoding="utf-8") as out:
    writer = csv.writer(out)
    for page in pdf.pages:
        for table in page.extract_tables():
            writer.writerows(table)
```

### Words and characters with coordinates

```python
import pdfplumber

with pdfplumber.open("report.pdf") as pdf:
    page = pdf.pages[0]
    for word in page.extract_words()[:5]:
        print(word["text"], word["x0"], word["top"], word["x1"], word["bottom"])
```

pdfplumber's coordinates are top-down: `top` is the distance from the page's top
edge. This is the same space `extract_form_structure.py` reports in.

## Creating

### Drawing on a canvas

```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

width, height = A4
sheet = canvas.Canvas("invoice.pdf", pagesize=A4)
sheet.setFont("Helvetica-Bold", 18)
sheet.drawString(50, height - 60, "Invoice 12345")
sheet.setFont("Helvetica", 11)
sheet.drawString(50, height - 90, "Due on receipt")
sheet.line(50, height - 100, width - 50, height - 100)
sheet.showPage()          # finish the page; omit it and the last page is lost
sheet.save()
```

Canvas coordinates are bottom-up PDF points, the same space `pypdf` uses. Call
`showPage()` before `save()` or the final page is discarded.

### Flowing documents

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

styles = getSampleStyleSheet()
story = [
    Paragraph("Quarterly report", styles["Title"]),
    Spacer(1, 12),
    Paragraph("Revenue grew across every region. " * 12, styles["BodyText"]),
    PageBreak(),
    Paragraph("Appendix", styles["Heading1"]),
]
SimpleDocTemplate("report.pdf", pagesize=A4).build(story)
```

Platypus handles wrapping, pagination and headings; the canvas does not. Use it
for anything longer than a page.

### Tables

```python
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle

rows = [["Product", "Q1", "Q2"], ["Widgets", "120", "135"], ["Gadgets", "85", "92"]]
table = Table(rows, hAlign="LEFT")
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DDDDDD")),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
]))
SimpleDocTemplate("table.pdf").build([Paragraph("Sales", getSampleStyleSheet()["Title"]), table])
```

### Subscripts, superscripts and other glyphs

The 14 standard PDF fonts carry a limited glyph set. Unicode subscript and
superscript characters (₂, ²) are **not** in it and render as black boxes. Use
Paragraph markup instead:

```python
from reportlab.platypus import Paragraph

Paragraph("H<sub>2</sub>O and x<super>2</super>", styles["BodyText"])
```

For canvas text, draw the smaller glyph yourself at a raised or lowered baseline.
For anything beyond Latin-1 — CJK, emoji, mathematical symbols — register a TrueType
font that has the glyphs:

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("NotoSans", "/path/to/NotoSans-Regular.ttf"))
sheet.setFont("NotoSans", 11)
```

## Rearranging

### Merge and split

```python
from pypdf import PdfReader, PdfWriter

writer = PdfWriter()
for name in ("first.pdf", "second.pdf"):
    writer.append(name)
with open("merged.pdf", "wb") as out:
    writer.write(out)

reader = PdfReader("merged.pdf")
for index, page in enumerate(reader.pages, start=1):
    single = PdfWriter()
    single.add_page(page)
    with open(f"page_{index}.pdf", "wb") as out:
        single.write(out)
```

`append()` accepts a path, a reader or a file object, and a `pages` argument to
take a subset (a list of indices, or a half-open `(start, stop)` range).

### Rotate, crop, metadata

```python
from pypdf import PdfReader, PdfWriter

writer = PdfWriter(clone_from=PdfReader("input.pdf"))
page = writer.pages[0]
page.rotate(90)                       # clockwise, must be a multiple of 90
page.mediabox.left = 50               # crop by moving the box edges
page.mediabox.bottom = 50
page.mediabox.right = 550
page.mediabox.top = 750
writer.add_metadata({"/Title": "Cropped", "/Author": "ai-engine project"})
with open("output.pdf", "wb") as out:
    writer.write(out)
```

Cropping changes the visible box, not the content: the clipped material is still
in the file. Redaction needs the content removed, not hidden.

### Watermark

Attach the pages to a writer **before** merging onto them — pypdf 7 refuses to
rewrite the content stream of a page that has no writer:

```python
from pypdf import PdfReader, PdfWriter

stamp = PdfReader("stamp.pdf").pages[0]
writer = PdfWriter(clone_from=PdfReader("input.pdf"))
for page in writer.pages:
    page.merge_page(stamp)            # over=True by default; False puts it behind
with open("watermarked.pdf", "wb") as out:
    writer.write(out)
```

Build `stamp.pdf` with reportlab at the same page size, and use
`canvas.setFillAlpha(0.3)` for a translucent mark.

### Password protection

```python
from pypdf import PdfReader, PdfWriter

writer = PdfWriter(clone_from=PdfReader("input.pdf"))
writer.encrypt(user_password="read-only", owner_password="full-control", algorithm="AES-256")
with open("protected.pdf", "wb") as out:
    writer.write(out)

reader = PdfReader("protected.pdf")
if reader.is_encrypted:
    reader.decrypt("read-only")       # returns a PasswordType; 0 means failure
print(reader.pages[0].extract_text())
```

The user password opens the document; the owner password controls permissions.
An empty user password with a set owner password is the common "anyone may read,
only the owner may change" arrangement. Encryption is access control, not
redaction: anyone who can open the file can copy its content.

## Rendering to images

The skill's script renders every page, caps the long side at 1000 pixels and
reports each file it wrote:

```bash
python ${SKILL_HOME}/scripts/pdf/convert_pdf_to_images.py input.pdf images/
```

Directly, when you need a different resolution or a single page:

```python
import pypdfium2 as pdfium

document = pdfium.PdfDocument("input.pdf")
page = document[0]
bitmap = page.render(scale=300 / 72)      # 300 dpi; PDF user space is 72/inch
bitmap.to_pil().save("page_1.png")
bitmap.close()
page.close()
document.close()
```

Rendering needs no external binary: PDFium is bundled with `pypdfium2`.

### Scanned pages (OCR)

A scan has no text layer, so extraction returns nothing. OCR is optional and
needs the Tesseract binary plus its Python wrapper (both Apache-2.0):

```python
import pypdfium2 as pdfium
import pytesseract                     # pip install pytesseract; tesseract must be on PATH

document = pdfium.PdfDocument("scan.pdf")
pages = []
for page in document:
    bitmap = page.render(scale=300 / 72)
    pages.append(pytesseract.image_to_string(bitmap.to_pil()))
    bitmap.close()
document.close()
text = "\n\n".join(pages)
```

Render at 300 dpi or better before OCR; the skill's 1000-pixel cap is for visual
inspection and is too small for reliable recognition.

## Recipe index

| Task | Tool | Entry point |
|------|------|-------------|
| Page count, plain text | pypdf | `PdfReader(...).pages`, `page.extract_text()` |
| Layout text, tables, word boxes | pdfplumber | `extract_text(layout=True)`, `extract_tables()`, `extract_words()` |
| Create a PDF | reportlab | `canvas.Canvas`, `SimpleDocTemplate` |
| Merge / split / page subset | pypdf | `PdfWriter.append`, `add_page` |
| Rotate / crop / metadata | pypdf | `page.rotate`, `page.mediabox`, `add_metadata` |
| Watermark | pypdf + reportlab | writer first, then `page.merge_page` |
| Encrypt / decrypt | pypdf | `writer.encrypt`, `reader.decrypt` |
| Pages as PNG | script | `convert_pdf_to_images.py` |
| Render at a chosen dpi | pypdfium2 | `page.render(scale=dpi/72)` |
| Fill a form | scripts | [pdf-forms.md](./pdf-forms.md) |
| Recover a field-less form's geometry | script | `extract_form_structure.py` |
| OCR a scan | pytesseract (optional) | render, then `image_to_string` |

## Pitfalls worth remembering

* **Writer first.** `merge_page`, `replace_contents` and other content rewrites
  need the page attached to a `PdfWriter`; pypdf 7 raises `DeprecationError`
  otherwise. `PdfWriter(clone_from=reader)` is the shortest way to get there.
* **`showPage()` before `save()`** in reportlab, or the last page never lands.
* **Extraction order is not reading order.** Use pdfplumber's layout mode or its
  word boxes when column structure matters.
* **Two y directions.** pypdf and reportlab are bottom-up; pdfplumber and
  rendered images are top-down. Convert explicitly at every boundary.
* **Standard fonts are Latin-1.** Register a TTF for other scripts; never rely on
  Unicode sub/superscript glyphs.
* **Encrypted input.** `reader.is_encrypted` then `reader.decrypt(password)`
  before any page access; the skill's scripts try an empty password and report a
  clear error when that fails.
* **Close what you render.** PDFium bitmaps and pages hold native memory;
  `close()` them (or use the script, which does) when looping over many pages.