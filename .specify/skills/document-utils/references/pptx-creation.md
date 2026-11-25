# Creating Presentations with python-pptx

Build a deck from code when there is no template to start from. When a template
exists, edit it instead -- the unpack/edit/pack route in
[pptx-editing.md](./pptx-editing.md) keeps the template's own masters, layouts and
theme, which a generated deck cannot reproduce.

Everything below runs on [python-pptx](https://python-pptx.readthedocs.io/) (MIT).
Lengths are English Metric Units (EMU): 914400 per inch, 12700 per point. The
`Inches`, `Pt` and `Emu` helpers convert for you, so never write a raw number
where a length belongs.

## Install and import

```bash
python -m pip install python-pptx
```

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE
```

## The deck and its canvas

```python
prs = Presentation()                      # built-in starter deck, 10 x 7.5 in (4:3)
prs.slide_width = Inches(13.333)          # 16:9
prs.slide_height = Inches(7.5)
```

Set the canvas before adding slides. Shapes are positioned in EMU from the
top-left corner, so a layout designed for 4:3 leaves a wide empty band on 16:9.

`Presentation("template.pptx")` opens an existing file instead of the starter
deck; its layouts and theme come with it.

## Slides and layouts

A slide is always created *from a layout*. The layout supplies the placeholders,
the background and the inherited fonts; the slide supplies the content.

```python
for index, layout in enumerate(prs.slide_layouts):
    print(index, layout.name)

slide = prs.slides.add_slide(prs.slide_layouts[1])   # "Title and Content"
```

The starter deck's layouts, by index:

| Index | Name | Use |
|-------|------|-----|
| 0 | Title Slide | opening, closing |
| 1 | Title and Content | one idea plus a body |
| 2 | Section Header | divider between parts |
| 3 | Two Content | side-by-side comparison |
| 4 | Comparison | two labelled columns |
| 5 | Title Only | a title over your own shapes |
| 6 | Blank | full manual composition |
| 7 | Content with Caption | picture plus explanation |
| 8 | Picture with Caption | picture-led slide |

A template's own layouts are different -- list them rather than assuming an
index. Vary the layouts across a deck; repeating one layout for every slide is
the most common way a generated deck looks generated.

### Placeholders are addressed by idx, not by position

```python
slide.shapes.title.text = "Quarterly review"

for ph in slide.placeholders:
    print(ph.placeholder_format.idx, ph.placeholder_format.type, ph.name)

body = slide.placeholders[1]              # idx 1 on "Title and Content"
body.text_frame.text = "First point"
```

`idx` is the placeholder's identity inside the layout and survives reordering;
the position in `slide.placeholders` does not. `slide.shapes.title` is the
shortcut for the title placeholder and is `None` on a layout without one.

## Text

A shape's `text_frame` holds paragraphs; a paragraph holds runs. A run is the
unit that carries formatting, so mixed formatting means multiple runs.

```python
tf = body.text_frame
tf.text = "First paragraph"               # replaces everything in the frame

p = tf.add_paragraph()
p.text = "Second paragraph"
p.level = 1                               # indent level, 0-8
p.alignment = PP_ALIGN.LEFT
p.space_after = Pt(6)
p.line_spacing = 1.2                      # a multiple, or Pt(...) for an exact height

run = p.add_run()
run.text = " with a bold tail"
run.font.bold = True
run.font.italic = True
run.font.size = Pt(16)
run.font.name = "Calibri"
run.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
```

Frame-level settings:

```python
tf.word_wrap = True
tf.vertical_anchor = MSO_ANCHOR.TOP       # TOP, MIDDLE, BOTTOM
tf.margin_left = Inches(0.1)
tf.margin_right = Inches(0.1)
tf.auto_size = MSO_AUTO_SIZE.NONE         # keep the box; let the text overflow visibly
```

`MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE` shrinks text to fit, which hides an overlong
slide until someone opens it. Prefer `NONE` and fix the content or the box.

Bullets come from the layout. Setting `p.level` moves a paragraph through the
layout's list levels; do not paste a bullet character into the text, because it
will not align with the list indent and will not survive a theme change.

## Shapes

```python
card = slide.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(1.5), Inches(3), Inches(1.2)
)
card.fill.solid()
card.fill.fore_color.rgb = RGBColor(0x02, 0x80, 0x90)
card.line.color.rgb = RGBColor(0x01, 0x50, 0x5A)
card.line.width = Pt(1.5)
card.shadow.inherit = False               # the starter theme adds a shadow otherwise
```

`MSO_SHAPE` names the preset geometry (RECTANGLE, OVAL, CHEVRON, RIGHT_ARROW,
CLOUD, ...). `card.text_frame` works exactly like a placeholder's, so a shape can
carry its own label. `fill.background()` makes the fill transparent.

For a free-form text box with no geometry:

```python
box = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(6), Inches(0.8))
box.text_frame.paragraphs[0].add_run().text = "A caption"
```

## Pictures

```python
pic = slide.shapes.add_picture("chart.png", Inches(7), Inches(1.5), width=Inches(4))
```

Give **one** of `width` or `height` and python-pptx keeps the aspect ratio; give
both and the picture is stretched. To fit a box without distortion, compute the
limiting dimension first:

```python
from PIL import Image

def fit(path, box_w, box_h):
    with Image.open(path) as im:
        scale = min(box_w / im.width, box_h / im.height)
    return int(im.width * scale), int(im.height * scale)
```

Cropping is fractional, per edge, and does not change the frame:

```python
pic.crop_left = 0.1
pic.crop_right = 0.1
```

python-pptx embeds PNG, JPEG, GIF, BMP, TIFF and WMF. Convert anything else
first; an embedded SVG is not supported.

## Tables

```python
table = slide.shapes.add_table(
    rows=3, cols=3, left=Inches(0.5), top=Inches(3.2), width=Inches(6), height=Inches(1.5)
).table

table.columns[0].width = Inches(2.5)
table.cell(0, 0).text = "Region"
table.cell(1, 0).text = "EMEA"
```

Row heights and column widths are set individually; the `width`/`height` of the
frame are divided evenly at creation. Cell text is a text frame, so the same run
formatting applies. A table inherits its banding from the theme -- set
`table.first_row = True` for a header row, and style cells explicitly when the
theme's banding is not what you want.

## Charts

```python
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION

data = CategoryChartData()
data.categories = ["Q1", "Q2", "Q3"]
data.add_series("Revenue", (12.5, 15.0, 18.25))
data.add_series("Cost", (8.0, 9.5, 10.0))

chart = slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(7), Inches(3.2), Inches(5.5), Inches(3), data
).chart

chart.has_legend = True
chart.legend.position = XL_LEGEND_POSITION.BOTTOM
chart.legend.include_in_layout = False
```

The chart is a real embedded workbook, so it stays editable in PowerPoint.
`XL_CHART_TYPE` covers column, bar, line, pie, area, scatter and their stacked
variants. Axis titles, number formats and series colours are reachable through
`chart.category_axis`, `chart.value_axis` and `chart.series[i].format`.

## Backgrounds and speaker notes

```python
slide.background.fill.solid()
slide.background.fill.fore_color.rgb = RGBColor(0xF7, 0xF7, 0xF5)

slide.notes_slide.notes_text_frame.text = "Say the number, then the reason for it."
```

A slide background overrides the layout's. Setting it on every slide is how a
deck loses the theme's dark/light structure -- prefer changing the layout when
the whole section should change.

## Masters, layouts and themes

`prs.slide_masters[0]` is the master; `master.slide_layouts` are its layouts.
Editing a master or layout placeholder changes every slide that inherits it,
which is the cheap way to restyle a whole deck.

python-pptx does **not** create layouts or masters, and it does not edit a theme
part (`ppt/theme/theme1.xml`: colour scheme, font scheme, format scheme). For
those, use the XML route: unpack the deck, edit the part, clean, pack -- see
[pptx-editing.md](./pptx-editing.md). The palette and typography notes in
`../themes/` are starting points for that edit.

## What python-pptx cannot do

| Need | Route |
|------|-------|
| Delete or reorder slides | edit `<p:sldIdLst>` in `ppt/presentation.xml`, then `clean.py` |
| Add a slide to an unpacked tree | `.specify/scripts/pptx/add_slide.py` |
| Create a layout or master | copy an existing layout part and rewire its relationships |
| Change theme colours or fonts | edit `ppt/theme/theme1.xml` |
| Animations, transitions, SmartArt | not modelled; edit the XML or use PowerPoint |

`Slides` has no `remove()`. Deleting a slide means removing its `<p:sldId>` from
the slide list; the part, its relationships and its media are then orphaned, and
`.specify/scripts/pptx/clean.py` reclaims them.

## Save and verify

```python
prs.save("output.pptx")
```

Saving is not verification. Render the deck and look at it
([pptx-qa.md](./pptx-qa.md)): overflow, collisions and inherited formatting are
invisible in the object model.

## Pitfalls

- **Raw numbers as lengths.** `left=914400` works, `left=1` puts the shape one
  EMU from the edge. Always use `Inches()` or `Pt()`.
- **`tf.text = ...` after building runs.** Assigning `.text` replaces the whole
  frame, discarding the runs and their formatting.
- **Placeholder index assumptions.** `slide.placeholders[1]` raises `KeyError`
  on a layout whose body placeholder has a different idx. List them first.
- **Both width and height on a picture.** That stretches it; pass one.
- **Text that fits in code but not on the slide.** Font metrics differ between
  the renderer and PowerPoint. Leave headroom, and render to check.
- **Forgetting the canvas.** A 4:3 composition on a 16:9 canvas leaves a band.
- **Shadow inheritance.** The starter theme gives shapes a shadow; set
  `shape.shadow.inherit = False` for a flat look.

## Quick reference

| Task | Call |
|------|------|
| New deck | `Presentation()` |
| Open a deck | `Presentation("file.pptx")` |
| Canvas | `prs.slide_width`, `prs.slide_height` |
| Add slide | `prs.slides.add_slide(prs.slide_layouts[i])` |
| Title | `slide.shapes.title.text` |
| Body | `slide.placeholders[idx].text_frame` |
| Text box | `slide.shapes.add_textbox(l, t, w, h)` |
| Shape | `slide.shapes.add_shape(MSO_SHAPE.X, l, t, w, h)` |
| Picture | `slide.shapes.add_picture(path, l, t, width=...)` |
| Table | `slide.shapes.add_table(rows, cols, l, t, w, h).table` |
| Chart | `slide.shapes.add_chart(XL_CHART_TYPE.X, l, t, w, h, data).chart` |
| Notes | `slide.notes_slide.notes_text_frame.text` |
| Background | `slide.background.fill` |
| Save | `prs.save("out.pptx")` |