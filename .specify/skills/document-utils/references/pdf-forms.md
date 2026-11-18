# Filling a PDF form

Two kinds of PDF arrive with the word "form" on them. One carries interactive
fields that a viewer can edit; the other is a picture of a form, with nothing to
type into. The routes are different, the coordinate systems are different, and
mixing them is the usual cause of text landing in the wrong place. Work out
which kind you have first, then follow that route end to end.

Every script below lives in `${SKILL_HOME}/scripts/pdf/` and takes positional
operands only. Run them with the interpreter that has the skill's dependencies
installed (`pypdf`, `pdfplumber`, `pypdfium2`, `Pillow`). Each script answers
`-h` / `--help` and `--version` without touching a file.

## Step 0 — choose the route

```bash
python ${SKILL_HOME}/scripts/pdf/check_fillable_fields.py form.pdf
```

One line comes back, and it is the branch condition:

| Printed line | Route |
|--------------|-------|
| `This PDF has fillable form fields` | Route 1 — write into the document's own fields |
| `This PDF does not have fillable form fields; you will need to visually determine where to enter data` | Route 2 — place text annotations |

Do not skip this step and do not infer the answer from the file name. A form
that looks interactive in a viewer may be a flattened export, and a plain-looking
scan may still carry an invisible field layer.

---

## Route 1 — the PDF has fields

### 1.1 Describe the fields

```bash
python ${SKILL_HOME}/scripts/pdf/extract_form_field_info.py form.pdf field_info.json
```

`field_info.json` is a list in reading order: page ascending, then top to bottom,
then left to right. One record per fillable field:

| Key | Meaning |
|-----|---------|
| `field_id` | Qualified name. A nested field is joined with dots (`address.street`); this exact string addresses the value |
| `type` | `text`, `checkbox`, `choice`, `radio_group`, or `unknown (/FT)` for a type this toolset does not fill |
| `page` | 1-based page holding the widget |
| `rect` | `[left, bottom, right, top]` in PDF user space — **y=0 is the bottom of the page** |

Type-specific members:

```json
[
  {"field_id": "last_name", "type": "text", "page": 1, "rect": [150, 672, 350, 688]},
  {"field_id": "agree", "type": "checkbox", "page": 1, "rect": [72, 602, 84, 614],
   "checked_value": "/Yes", "unchecked_value": "/Off"},
  {"field_id": "country", "type": "choice", "page": 1, "rect": [150, 562, 310, 578],
   "choice_options": [{"value": "US", "text": "United States"},
                      {"value": "CA", "text": "Canada"}]},
  {"field_id": "plan", "type": "radio_group", "page": 1,
   "radio_options": [{"value": "/basic", "rect": [72, 522, 84, 534]},
                     {"value": "/pro", "rect": [140, 522, 152, 534]}]}
]
```

Write the `value` a record asks for, never the display text: `"/Yes"` for a
checkbox, one of `radio_options[].value` for a radio group, one of
`choice_options[].value` for a dropdown. The leading slash on button states is
part of the name.

A field the script could not locate is reported on stdout and omitted from the
JSON. If a field you can see in the viewer is missing, the document's field tree
is unusual — fall back to Route 2 for that page rather than guessing an id.

### 1.2 Learn what each field asks

The field id is a name, not a question. Render the pages and read them:

```bash
python ${SKILL_HOME}/scripts/pdf/convert_pdf_to_images.py form.pdf images/
```

One PNG per page (`images/page_1.png`, ...), rendered at 200 dpi and capped at
1000 pixels on the long side. Match each rendered widget to its `field_info.json`
record by position. The two coordinate spaces differ, so convert before
comparing:

```
scale        = image_width / pdf_page_width
image_x      = pdf_x * scale
image_y      = (pdf_page_height - pdf_y) * scale      # y flips
```

`rect` is bottom-up; the image is top-down. A widget at `rect[1] = 672` on a
792-point page sits near the **top** of the image, at `y ≈ (792 - 688) * scale`.

### 1.3 Author the value file

`field_values.json` is a list. `field_id` and `page` must agree with
`field_info.json`; `description` is for the human reading the file and is not
written into the PDF. A record may omit `value` — it is then checked but left
blank, which is useful for validating a partly-decided form.

```json
[
  {"field_id": "last_name", "description": "Family name", "page": 1, "value": "Simpson"},
  {"field_id": "agree", "description": "Over 18", "page": 1, "value": "/Yes"},
  {"field_id": "country", "description": "Country of residence", "page": 1, "value": "CA"},
  {"field_id": "plan", "description": "Subscription tier", "page": 1, "value": "/pro"},
  {"field_id": "notes", "description": "Free text", "page": 2, "value": "None"}
]
```

### 1.4 Fill, and let the validator argue

```bash
python ${SKILL_HOME}/scripts/pdf/fill_fillable_fields.py form.pdf field_values.json filled.pdf
```

Nothing is written until every record passes three checks: the id exists, the
page matches the widget's page, and the value is legal for the type. Each failure
prints one line and the run exits 1 with no output file:

```
ERROR: `nope` is not a valid field ID
ERROR: Incorrect page number for `last_name` (got 2, expected 1)
ERROR: Invalid value "/Maybe" for checkbox field "agree". The checked value is "/Yes" and the unchecked value is "/Off"
ERROR: Invalid value "MX" for choice field "country". Valid values are: ['US', 'CA']
```

Fix the value file and run again; do not edit the PDF to make an error go away.

On success the document keeps its field layer — the result is still fillable —
and `NeedAppearances` is set so the viewer redraws each widget from its new
value. That flag is what makes checkboxes and radio buttons show up reliably
across viewers; a tool that strips it can leave a filled field looking empty.

### 1.5 Verify

```bash
python ${SKILL_HOME}/scripts/pdf/convert_pdf_to_images.py filled.pdf verify/
```

Read the images, and read the values back:

```python
from pypdf import PdfReader

for name, field in (PdfReader("filled.pdf").get_fields() or {}).items():
    print(name, field.get("/V"))
```

A value that reads back correctly but renders blank is an appearance problem,
not a data problem: confirm `/NeedAppearances` is true in the document's
`/AcroForm`, and open the file in a second viewer before concluding the fill
failed.

---

## Route 2 — the PDF has no fields

Text is placed as free-text annotations at coordinates you supply. Accuracy
comes from the document's own geometry where it exists, and from measured pixels
where it does not. Try the structure first; it is exact, and it is cheaper than
looking at pictures.

### 2.1 Recover the geometry

```bash
python ${SKILL_HOME}/scripts/pdf/extract_form_structure.py form.pdf structure.json
```

The JSON carries five inventories, all in **top-down PDF points** (origin at the
page's top-left, y growing downward, one decimal place):

| Key | Contents | How to use it |
|-----|----------|---------------|
| `pages` | `page_number`, `width`, `height` | Copy into `fields.json` as `pdf_width` / `pdf_height` |
| `labels` | Every extracted word with `x0`, `top`, `x1`, `bottom` | Find the label of each field; adjacent words form one label |
| `lines` | Horizontal rules spanning over half the page width: `y`, `x0`, `x1` | Row separators and the underline a value sits on |
| `checkboxes` | Near-square rectangles 5–15 pt a side, with `center_x` / `center_y` | Tick boxes, usable as an entry box directly |
| `row_boundaries` | Consecutive rule pairs: `row_top`, `row_bottom`, `row_height` | How tall an entry box may be |

If `labels` holds the form's own words, continue with 2.2. If the page is a scan
— no labels, or text like `(cid:12)` — go to 2.3.

The filters are conservative on purpose. Round boxes, faint rules, table cells
and anything drawn as part of an image are not reported. Missing elements are
normal; 2.4 covers the mixed case.

### 2.2 Boxes from the structure (preferred)

Derive each entry box from the geometry around it:

* **Text field** — `x0` a few points right of the label's `x1`; `x1` at the next
  label's `x0` or the row's right edge; `top` aligned with the label's `top`;
  `bottom` at the rule below, or `top + row_height`. Keep the box at least as
  tall as the font size you will write with.
* **Checkbox** — use the reported rectangle verbatim:
  `[x0, top, x1, bottom]`. Write `X` into it, or leave it empty.
* **Multi-line area** — span several `row_boundaries` entries; the text is drawn
  from the top of the box.

Declare the space with `pdf_width` / `pdf_height`. That pair is the switch the
filler reads: with it, boxes are treated as top-down PDF points and no scaling
happens.

```json
{
  "pages": [{"page_number": 1, "pdf_width": 612, "pdf_height": 792}],
  "form_fields": [
    {
      "page_number": 1,
      "description": "Family name entry",
      "field_label": "Last Name",
      "label_bounding_box": [72, 63, 128, 75],
      "entry_bounding_box": [140, 62, 290, 78],
      "entry_text": {"text": "Simpson", "font_size": 11}
    },
    {
      "page_number": 1,
      "description": "Consent tick box",
      "field_label": "Yes",
      "label_bounding_box": [90, 196, 110, 208],
      "entry_bounding_box": [72, 198, 82, 208],
      "entry_text": {"text": "X", "font_size": 10}
    }
  ]
}
```

`label_bounding_box` is not ink. It exists so the audit and the overlay can show
you which label each entry belongs to.

### 2.3 Boxes from measured pixels (scanned pages)

Render, estimate, then refine by cropping. Estimating on a full page is accurate
to about a centimetre; cropping is what turns that into a pixel-exact box.

```bash
python ${SKILL_HOME}/scripts/pdf/convert_pdf_to_images.py form.pdf images/
```

Look at `images/page_1.png` and note a rough region per field. Crop that region
with generous padding and measure inside the crop; keep the crops in their own
directory (`mkdir -p crops`):

```python
from PIL import Image

page = Image.open("images/page_1.png")
offset = (50, 120)                       # crop origin in full-page pixels
page.crop((offset[0], offset[1], offset[0] + 300, offset[1] + 90)).save("crops/name.png")
```

Read `crops/name.png`, find the exact edges of the entry area, then add the
offset back: a box starting at `(52, 18)` inside that crop is `(102, 138)` on the
full page. Group neighbouring fields into one crop when they fit; the offset
arithmetic is the same.

Record the **full-page pixel** size of the image you measured, not the PDF size:

```json
{
  "pages": [{"page_number": 1, "image_width": 1700, "image_height": 2200}],
  "form_fields": [
    {
      "page_number": 1,
      "description": "Family name entry",
      "field_label": "Last Name",
      "label_bounding_box": [200, 175, 355, 208],
      "entry_bounding_box": [390, 172, 800, 216],
      "entry_text": {"text": "Simpson", "font_size": 11}
    }
  ]
}
```

`image_width` / `image_height` tell the filler to scale by
`pdf_width / image_width` and `pdf_height / image_height` before flipping y. If
the numbers do not match the image you actually measured, every box on the page
shifts by the same ratio — the first thing to check when output is uniformly
misplaced.

### 2.4 Mixing the two sources

Use structure boxes for what the structure found and measured pixels for the
rest, but convert the pixel boxes into points before writing the file:

```
pdf_x = image_x * (pdf_width / image_width)
pdf_y = image_y * (pdf_height / image_height)
```

Then declare `pdf_width` / `pdf_height` for the page and keep every box in that
one space. A page record selects one space for the whole page; there is no
per-field override.

### 2.5 Audit the boxes

```bash
python ${SKILL_HOME}/scripts/pdf/check_bounding_boxes.py fields.json
```

Two rules are checked: rectangles on one page must not overlap (a label inside
its own entry area, or two fields claiming the same area), and an entry box must
be at least as tall as its `entry_text.font_size` (14 when omitted). The report
opens with `Read N fields` and ends with `SUCCESS: All bounding boxes are valid`
or one `FAILURE:` line per problem, each naming the fields and the numbers
involved. After 20 lines it stops and says so.

The verdict is in the text: a completed audit exits 0 even when it reports
failures. Read the lines, fix `fields.json`, and run it again until it prints
SUCCESS.

### 2.6 Look at the boxes

Arithmetic cannot tell you that a box sits over the wrong line. Draw the boxes
on the page image and look:

```bash
python ${SKILL_HOME}/scripts/pdf/create_validation_image.py 1 fields.json images/page_1.png review/page_1_boxes.png
```

Operands are the 1-based page number, the fields file, the input image and the
output image. Every field on that page contributes two outlines — **red** for
`entry_bounding_box`, **blue** for `label_bounding_box` — and the script reports
how many it drew. The input image must be in the same space as the boxes: for
pixel boxes use the rendered page at its rendered size; for point boxes render at
72 dpi so one point is one pixel.

### 2.7 Fill

```bash
python ${SKILL_HOME}/scripts/pdf/fill_pdf_form_with_annotations.py form.pdf fields.json filled.pdf
```

The filler picks the coordinate space from the page record, flips y into PDF
user space, and adds one borderless, background-free free-text annotation per
non-empty `entry_text.text`. A field with no text, or an empty string, is skipped
silently — that is how a blank is left blank. Defaults are font `Arial`, size 14,
colour `000000`; `font_color` is hex RGB without a leading `#`.

The output has no AcroForm: the values are page content, which survives merging,
printing and flattening, and cannot be edited by clicking on the form.

### 2.8 Verify, and what to check when it is wrong

```bash
python ${SKILL_HOME}/scripts/pdf/convert_pdf_to_images.py filled.pdf verify/
```

| Symptom | First thing to check |
|---------|----------------------|
| Everything on a page shifted by a constant ratio | `image_width` / `image_height` do not match the image you measured |
| Text mirrored vertically, or at the bottom of the page | Boxes were written bottom-up; this route needs top-down y |
| Text clipped at the box's bottom edge | Box shorter than the font size — the audit reports this |
| Text over a neighbouring field | Overlapping boxes — the audit reports this; the overlay shows it |
| Nothing drawn for one field | `entry_text.text` missing or empty, or `page_number` has no `pages` record |
| Values correct but invisible in one viewer | Font substitution: try `Helvetica`, or embed a font when creating the PDF |

Page rotation is not compensated by these scripts: a page with `/Rotate 90`
needs its boxes measured on the rendered (rotated) image, with the rendered
pixel size declared.

---

## Coordinate spaces at a glance

| Space | Origin | y direction | Where it appears |
|-------|--------|-------------|------------------|
| PDF user space | bottom-left | up | `field_info.json` `rect`, annotation rectangles, `mediabox` |
| Top-down points | top-left | down | `structure.json`, `fields.json` with `pdf_width`/`pdf_height` |
| Image pixels | top-left | down | rendered PNGs, `fields.json` with `image_width`/`image_height` |

Conversions: top-down points → user space is `y' = page_height - y`; pixels →
points is a scale by `page_size / image_size` on each axis, then the same flip.
One file, one space, one page record.

## Dependencies

`pypdf` reads and writes the field layer and the annotations; `pdfplumber`
recover the geometry of a field-less form; `pypdfium2` renders pages to images;
`Pillow` draws the review overlay and crops regions for measurement. Licences
and versions: [pdf-reference.md](./pdf-reference.md) § Dependencies and licences.
Everyday PDF work outside form filling: [pdf-operations.md](./pdf-operations.md).