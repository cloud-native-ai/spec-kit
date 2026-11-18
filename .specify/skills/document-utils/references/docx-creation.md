# Creating a New Word Document

This guide covers building a `.docx` from nothing. The stack is Python:
**python-docx** (MIT) writes the package, and the skill's own `office/` scripts
check it afterwards. The JavaScript route this skill used before (`docx-js`) is
no longer part of it — every example here runs in the same interpreter as the
rest of the workflow, with no Node toolchain and no second language to install.

## Setup

```bash
python3 -m pip install python-docx        # pulls lxml (BSD-3-Clause) with it
```

Python 3.10 or newer. `python-docx` is optional for *editing* an existing file
(the unpack/edit/pack road needs only the standard library), but it is the
recommended way to create one: it owns the package inventories, the numbering
definitions and the style table, which are tedious to write by hand.

## Validate what you wrote

```bash
python3 "${SKILL_HOME}/scripts/office/validate.py" report.docx --verbose
```

The check is structural: well-formed parts, declared namespaces, unique and
in-range identifiers, relationship and content-type inventories that agree with
the parts on disk, plus a round trip that re-opens the file with python-docx.
XSD schema validation is no longer shipped with this skill; the round trip and
the structural checks are what replace it. A file that passes them opens in
Word and in LibreOffice.

## Page size and margins

```python
from docx import Document
from docx.shared import Mm

document = Document()
section = document.sections[0]
section.page_width, section.page_height = Mm(210), Mm(297)   # A4 portrait
section.left_margin = section.right_margin = Mm(25)
section.top_margin = section.bottom_margin = Mm(20)
```

For US Letter use `Inches(8.5)` by `Inches(11)`. Set the section before adding
content: a page break inherits the section it lands in.

## Styles, including the built-in headings

Restyle the built-in names rather than inventing parallel ones, so the navigation
pane and a table of contents still recognise the hierarchy.

```python
from docx.shared import Pt, RGBColor

styles = document.styles
normal = styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(11)

for name, size in (("Heading 1", 18), ("Heading 2", 14), ("Heading 3", 12)):
    style = styles[name]
    style.font.size = Pt(size)
    style.font.bold = True
    style.font.color.rgb = RGBColor(0x1F, 0x3B, 0x57)

document.add_heading("Quarterly report", level=1)
document.add_paragraph("Summary of the period.", style="Normal")
```

East Asian text needs the east-Asian font attribute as well; set it on the
style's element when the document is bilingual:

```python
from docx.oxml.ns import qn

normal.element.rPr.rFonts.set(qn("w:eastAsia"), "SimSun")
```

## Lists

Use real numbering, never a typed bullet character. A bullet glyph in the text
cannot be re-leveled, cannot continue across paragraphs, and reads aloud as
punctuation.

```python
document.add_paragraph("First point", style="List Bullet")
document.add_paragraph("Second point", style="List Bullet")
document.add_paragraph("Step one", style="List Number")
document.add_paragraph("Step two", style="List Number")
```

For a nested level, use `List Bullet 2` / `List Number 2`. When a document needs
several independent numbered sequences, define a new abstract numbering in
`word/numbering.xml` (see `docx-xml-reference.md`) instead of restarting one
shared list.

## Tables

```python
table = document.add_table(rows=1, cols=3)
table.style = "Table Grid"
header = table.rows[0].cells
for cell, title in zip(header, ("Region", "Revenue", "Change")):
    cell.text = title

for region, revenue, change in (("North", "1.2M", "+4%"), ("South", "0.9M", "-2%")):
    row = table.add_row().cells
    row[0].text, row[1].text, row[2].text = region, revenue, change
```

Set column widths on every cell of a column, not only the first: Word derives a
column's width from its cells, and a single wide cell can stretch the table past
the margin.

```python
from docx.shared import Cm

for row in table.rows:
    row.cells[0].width = Cm(6)
    row.cells[1].width = Cm(4)
    row.cells[2].width = Cm(4)
```

## Images

```python
from docx.shared import Inches

document.add_picture("chart.png", width=Inches(5.5))
```

Give one dimension and let the other follow, so the aspect ratio survives.
python-docx registers the image part, its relationship and its content type; if
you add an image by editing XML instead, all three must be added by hand or the
document reports itself corrupt.

## Page breaks

```python
document.add_page_break()
```

A break is a run containing `<w:br w:type="page"/>`. Prefer it over empty
paragraphs used as spacing: empty paragraphs move when the text above them
reflows.

## Table of contents

Word builds the contents from the heading styles when it updates fields, so the
document carries a field rather than a frozen list.

```python
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

paragraph = document.add_paragraph()
field = OxmlElement("w:fldSimple")
field.set(qn("w:instr"), r'TOC \o "1-3" \h \z \u')
paragraph._p.append(field)
```

The field shows its result after an update in Word, or after a LibreOffice
round trip (`office/soffice.py convert`). State in the document that the contents
update on open if the reader may see an empty field first.

## Headers and footers

```python
section = document.sections[0]
section.header.paragraphs[0].text = "Internal draft"
footer = section.footer.paragraphs[0]
footer.text = "Page "
```

A page-number field goes into the footer as a field, not as a literal:

```python
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

run = footer.add_run()
field = OxmlElement("w:fldSimple")
field.set(qn("w:instr"), "PAGE")
run._r.append(field)
```

## Saving, then checking

```python
document.save("report.docx")
```

```bash
python3 "${SKILL_HOME}/scripts/office/validate.py" report.docx --verbose
```

When the document must carry tracked changes or comments, create it here first
and then add the revisions through the unpack/edit/pack road described in
`docx-editing.md`: python-docx writes clean content, and the revision markup is
easier to place deliberately than to generate.

## Rules that keep a generated document readable

- Restyle built-in style names; do not clone them under new names.
- Real numbering for lists, real fields for page numbers and contents.
- One dimension for an image, explicit widths for every cell of a table column.
- Section geometry first, content second.
- Validate before handing the file over; a package that fails its inventories
  opens as "corrupt" even when every paragraph is correct.