# Checking a Finished Deck

Start from the assumption that something is wrong. The first render of a
generated or edited deck almost always has at least one defect, and the person
who wrote the content is the worst-placed reader of it: you see what you meant,
not what is on the slide. A pass that finds nothing is a pass that did not look.

Two kinds of check, both required. Content QA reads the text; visual QA reads the
rendered page. Neither catches the other's defects.

## Content QA

Extract the text straight from the package with python-pptx -- no converter, no
extra service. Save this as `extract_text.py`:

```python
import sys

from pptx import Presentation

prs = Presentation(sys.argv[1])
for number, slide in enumerate(prs.slides, 1):
    print(f"--- slide {number} ---")
    for shape in slide.shapes:
        if shape.has_text_frame:
            for paragraph in shape.text_frame.paragraphs:
                text = "".join(run.text for run in paragraph.runs)
                if text.strip():
                    print(text)
        if shape.has_table:
            for row in shape.table.rows:
                print(" | ".join(cell.text for cell in row.cells))
    if slide.has_notes_slide:
        print("notes:", slide.notes_slide.notes_text_frame.text)
```

Read the output for missing content, wrong order, duplicated items and typos.
Then search it for the template's own leftovers, which are the most common
defect in a deck built from a template:

```bash
python extract_text.py output.pptx > deck.txt
grep -inE "lorem|ipsum|xxxx|placeholder|click to (add|edit)|sample text|your (title|text|company)" deck.txt
```

Any hit is a defect to fix before the deck is called finished. Add the terms your
own template uses -- a company name, a date, a job title -- to that pattern.

Also check the counts: if the source has three team members and the template had
four slots, the fourth slot's picture and caption must be gone, not emptied.

## Visual QA

Render every slide at full size and look at the pictures. The thumbnail grid is
for choosing layouts, not for this: its cells are too small to show a collision
or a clipped descender.

```bash
soffice --headless --convert-to pdf output.pptx
```

```python
import pypdfium2 as pdfium

document = pdfium.PdfDocument("output.pdf")
for index in range(len(document)):
    image = document[index].render(scale=150 / 72).to_pil()   # 150 dpi
    image.save(f"slide-{index + 1:02d}.jpg", quality=90)
document.close()
```

`scripts/pdf/convert_pdf_to_images.py` does the same rasterization if you prefer
a script to a snippet. In a sandbox where LibreOffice cannot open its socket,
`scripts/office/soffice.py` owns the environment that makes the conversion work.

To re-render one slide after a fix, convert again and render only that page
index -- the PDF page order follows the slide order, and hidden slides may be
skipped by the converter, so check the page count against the visible slide
count before trusting an index.

### Look for these, in this order

1. Text crossing a shape, a rule or another text block.
2. Text clipped at a box edge or at the slide edge.
3. A decorative line or rule positioned for one line of text while the title
   wrapped to two.
4. Footers, sources and page numbers colliding with the content above them.
5. Blocks nearly touching, or a large empty region beside a cramped one.
6. Columns and cards whose edges do not line up.
7. Contrast too low to read: text, icons and thin rules alike.
8. A box so narrow that every line wraps to two or three words.
9. Anything left over from the template.

### Use a fresh reader

Hand the rendered images to a reviewer that did not write the deck -- a
subagent with no prior context is ideal, and worth dispatching even for two or
three slides. Give it the images, what each slide is supposed to say, and the
list above. Ask for every issue including minor ones, per slide, and ask it to
assume there are issues rather than to confirm the deck is fine.

A reviewer that shares your context shares your blind spots.

## The loop

1. Render, inspect, write down every issue found.
2. Fix the issues.
3. Re-render the affected slides and inspect them again -- a fix moves something
   else more often than not.
4. Repeat until a full pass produces no new issue.

Do not call the deck finished before at least one fix-and-recheck cycle has
happened. "It looked right the first time" is not a result; it is an untested
claim.

## Quick check of the package itself

A deck can render and still be structurally wrong -- an orphaned part, a missing
content type, a relationship pointing at a deleted file. After editing an
unpacked tree, `scripts/pptx/clean.py` reclaims the orphans and
`scripts/office/pack.py` validates on the way out. Reopening the packed file with
python-pptx is a cheap final check that a reader accepts it:

```python
Presentation("output.pptx")   # raises if the package is not loadable
```