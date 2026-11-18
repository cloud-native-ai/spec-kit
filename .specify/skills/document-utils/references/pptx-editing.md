# Editing an Existing Presentation

Use this route when a template or a finished deck is the starting point. The
deck is unpacked into a directory of XML parts, the parts are edited directly,
and the directory is packed back into a `.pptx`. Nothing re-serializes a part you
did not touch, so the template's own formatting survives the round trip.

Creating a deck from code is a different job -- see
[pptx-creation.md](./pptx-creation.md).

## The loop

```bash
SKILL=${SKILL_HOME}/scripts

# 1. Look at what the template offers
python $SKILL/pptx/thumbnail.py template.pptx            # thumbnails.jpg, one cell per slide

# 2. Unpack
python $SKILL/office/unpack.py template.pptx unpacked/

# 3. Structural edits: slide list, new slides, reordering
python $SKILL/pptx/add_slide.py unpacked/ slideLayout3.xml
#    ... insert the printed <p:sldId> into ppt/presentation.xml ...

# 4. Content edits: text, pictures, shapes inside each ppt/slides/slideN.xml

# 5. Reclaim what the edits orphaned
python $SKILL/pptx/clean.py unpacked/

# 6. Pack
python $SKILL/office/pack.py unpacked/ output.pptx --original template.pptx
```

Finish every structural change (step 3) before starting content edits (step 4).
A slide's file name is assigned when it is created, so adding slides after
editing content means re-reading which file holds which slide.

Steps 3 and 4 are independent per slide once the structure is settled: each slide
is its own file, so several editors can work on different slides at the same
time without touching a shared part. The shared parts -- `presentation.xml`,
`[Content_Types].xml`, the relationship files -- belong to one editor at a time.

## Choosing layouts

The thumbnail grid labels every cell with the slide part that produced it
(`slide7.xml`), so a layout you like can be found again in the tree. Look for
variety before writing content: multi-column layouts, picture-plus-text,
full-bleed images, quote or callout slides, section dividers, big-number
callouts. A deck that uses one text layout for every slide reads as a document,
not a presentation.

To see the layouts a template carries:

```bash
ls unpacked/ppt/slideLayouts/
```

`add_slide.py unpacked/ slideLayoutN.xml` starts a new slide bound to that
layout. The new slide is empty apart from the layout's inheritance; it does not
copy the layout's decorative shapes, which stay on the layout and render through
it.

## The scripts

| Script | Operand | What it does |
|--------|---------|--------------|
| `office/unpack.py` | `file.pptx dir/` | extracts the package into a directory of parts |
| `pptx/add_slide.py` | `dir/ slideN.xml` or `dir/ slideLayoutN.xml` | writes the next slide part, its relationships, its content type and its presentation relationship |
| `pptx/clean.py` | `dir/` | removes parts nothing references any more |
| `office/pack.py` | `dir/ out.pptx [--original file]` | packs the tree back into a package, validating it on the way |
| `pptx/thumbnail.py` | `file.pptx [prefix] [--cols N]` | labelled thumbnail grids of a packaged deck |

### add_slide.py

```bash
python $SKILL/pptx/add_slide.py unpacked/ slide2.xml        # copy slide2
python $SKILL/pptx/add_slide.py unpacked/ slideLayout2.xml  # new slide from a layout
```

It prints two lines:

```
Created slide5.xml from slide2.xml
Add to presentation.xml <p:sldIdLst>: <p:sldId id="259" r:id="rId12"/>
```

The second line is the element to insert into `<p:sldIdLst>` in
`ppt/presentation.xml`, at the position where the slide belongs. The script
deliberately does not insert it: slide order is a decision, and the script cannot
know where in the deck the new slide goes.

Copying a slide copies its relationships too, except the speaker-notes
relationship -- notes belong to one slide, and two slides sharing a notes part
would show the same notes twice. The notes part itself is left in place for
`clean.py` to reclaim if nothing else names it.

Exit codes: 0 on success, 1 for a wrong operand count, a missing directory, or a
source part that does not exist. Errors go to stderr.

### clean.py

```bash
python $SKILL/pptx/clean.py unpacked/
```

Removes, in order: slides absent from `<p:sldIdLst>` and their relationships; the
`[trash]` directory; relationship files under `charts`, `diagrams` and `drawings`
whose own part is gone or unreferenced; unreferenced files under `media`,
`embeddings`, `charts`, `diagrams`, `tags`, `drawings` and `ink`; unreferenced
`theme/themeN.xml` parts; unreferenced notes slides; and the content-type
overrides of everything it removed.

Removal repeats until a pass removes nothing, because deleting a chart orphans
the picture the chart embedded. A part stays as long as *any* surviving
relationship names it -- including a relationship from another resource, not
only from a slide.

It prints `Removed N unreferenced files:` followed by one package-relative path
per line, or `No unreferenced files found`. Running it twice is safe: the second
run reports nothing.

## Slide order, deletion, addition

Order lives in `ppt/presentation.xml`, in `<p:sldIdLst>`:

```xml
<p:sldIdLst>
  <p:sldId id="256" r:id="rId7"/>
  <p:sldId id="257" r:id="rId8"/>
</p:sldIdLst>
```

- **Reorder**: move the `<p:sldId>` elements. The `id` is an identifier, not a
  position; the document order is the slide order.
- **Delete**: remove the `<p:sldId>` element, then run `clean.py`. The part, its
  relationships and its media go with it.
- **Add**: use `add_slide.py`, then insert the printed element.

Do not copy slide files by hand. A copied part needs a content-type override, a
presentation relationship with an unused `rId`, a unique slide id, and its own
relationship file with the notes reference removed. `add_slide.py` does all four;
a manual copy usually misses at least one, and PowerPoint reports the package as
corrupt rather than naming the missing piece.

## Editing content inside a slide

A slide part is PresentationML. The text of a shape lives in
`<p:sp>/<p:txBody>/<a:p>/<a:r>/<a:t>`:

```xml
<p:sp>
  <p:txBody>
    <a:bodyPr/>
    <a:p>
      <a:pPr algn="l"/>
      <a:r><a:rPr lang="en-US" sz="2400" b="1"/><a:t>Step 1</a:t></a:r>
    </a:p>
    <a:p>
      <a:r><a:rPr lang="en-US" sz="1800"/><a:t>Do the first thing.</a:t></a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

Work through every placeholder in the part -- text, pictures, charts, captions --
and replace each with final content. A template's placeholder text left behind
is the most common defect in a finished deck; search for it explicitly during QA
([pptx-qa.md](./pptx-qa.md)).

Edit the XML with a precise, targeted replacement rather than a bulk
substitution: the same string often appears in several shapes, and a global
replace silently rewrites the ones you did not mean.

### Formatting rules that keep a template intact

- **One paragraph per item.** A list of steps is several `<a:p>` elements, never
  one paragraph with the steps concatenated. Copy the `<a:pPr>` of the paragraph
  you are replacing so line spacing and indentation survive.
- **Bold is a run property.** Headers, subheadings and inline labels carry
  `b="1"` on `<a:rPr>`. Sizes are hundredths of a point: `sz="2400"` is 24 pt.
- **Bullets come from the layout.** Use `<a:buChar>` or `<a:buAutoNum>` when a
  paragraph must override them, and `<a:buNone/>` to suppress them. Never type a
  bullet character into `<a:t>`: it does not align with the list indent.
- **Whitespace is significant only when declared.** Add `xml:space="preserve"`
  to an `<a:t>` whose leading or trailing spaces matter.
- **Curly quotes are written as entities** (`&#x201C;`, `&#x201D;`, `&#x2018;`,
  `&#x2019;`) so an editor that normalizes Unicode cannot flatten them.

### Fewer items than the template has slots

Delete the whole element group -- picture, caption, text box -- not just the
text. A cleared text box leaves an empty frame and an orphaned picture beside it,
which renders as a hole in the layout. `clean.py` then reclaims the picture file
if no other slide names it.

### Longer content than the slot was designed for

Shorter replacements are safe. Longer ones wrap, overflow, or push a decorative
rule out of place. Either trim the content, split it across slides, or resize the
shape -- and render the slide afterwards to see which happened.

## Parsing and writing the parts

The part scripts (`add_slide.py`, `clean.py`, and the `ooxml_parts` module they
share) parse with `xml.dom.minidom` after refusing any part that declares a DTD.
Two reasons, both practical:

- No OPC part carries a DTD, and an internal entity declaration is how a small
  part becomes an unbounded expansion. Refusing the DTD closes that without a
  third-party parser.
- minidom keeps every namespace declaration and every whitespace node it read.
  A part whose producer declared a prefix it never used -- named, for example, by
  an `mc:Ignorable` attribute -- still needs that declaration after a rewrite.
  A serializer that drops unused declarations leaves the attribute pointing at
  nothing, and the package stops opening.

If you write your own tooling against these parts, keep both properties. Check
the result by packing and reopening the deck, not by reading the XML alone.

## Where things live

| Path | Holds |
|------|-------|
| `[Content_Types].xml` | one Override per part, plus Defaults by extension |
| `_rels/.rels` | the package root's relationship to `ppt/presentation.xml` |
| `ppt/presentation.xml` | slide order, slide size, masters list |
| `ppt/_rels/presentation.xml.rels` | presentation to slides, masters, theme, props |
| `ppt/slides/slideN.xml` | one slide's shapes and text |
| `ppt/slides/_rels/slideN.xml.rels` | that slide's layout, pictures, notes, charts |
| `ppt/slideLayouts/`, `ppt/slideMasters/` | inherited structure and decoration |
| `ppt/theme/themeN.xml` | colour scheme, font scheme, format scheme |
| `ppt/media/`, `ppt/notesSlides/` | embedded files and speaker notes |

A relationship target is relative to the directory of the part that owns the
`_rels` file. From `ppt/slides/_rels/slide1.xml.rels`, `../media/image1.png` is
`ppt/media/image1.png` -- not `ppt/slides/media/image1.png`.