# Designing Slides That Carry the Content

A deck is read at a distance, in seconds, by people who did not write it. Every
choice below serves that: one idea per slide, a visual anchor for it, and enough
contrast and space to read it from the back of a room.

The failure mode to avoid is the default deck -- white background, black bullets,
one layout repeated twenty times. It is not neutral; it reads as unfinished.

## Decide four things before the first slide

1. **A palette that belongs to this subject.** Test it by imagining the same
   colours on an unrelated deck. If they would work equally well there, the
   choice is generic. A talk about soil health and a talk about payment
   infrastructure should not share a palette.
2. **A hierarchy inside the palette.** One colour carries most of the surface
   (roughly two thirds), one or two support it, and a single accent is reserved
   for the thing you want looked at. Equal weights give the eye nowhere to land.
3. **A light/dark structure.** Dark opening and closing slides with light
   content between them gives the deck a shape; an all-dark deck reads as
   premium and continuous. Pick one and hold it.
4. **One repeated motif.** A corner radius, an icon inside a filled circle, a
   thick left edge on cards, a numbered chip. Repeat it on every slide so the
   deck looks like one object rather than a collection.

## Palette starting points

Use these as directions, not as a fixed list. Adjust to the subject and check
contrast against the background you will actually use.

| Direction | Base | Support | Accent |
|-----------|------|---------|--------|
| Deep water | `0B2545` | `8DA9C4` | `EEF4ED` |
| Kiln and clay | `8C3B2E` | `E4D5C3` | `5E7A6B` |
| Signal green | `14532D` | `A7C957` | `F2F0EB` |
| Graphite paper | `2B2D31` | `D8DADF` | `E4572E` |
| Plum and linen | `4A2545` | `C9ADA7` | `F5EBE0` |
| Cold steel | `1F3A5F` | `6E8CA0` | `F4A259` |
| Ink and citrus | `101418` | `BFC0C0` | `FFB627` |

Two checks before committing: body text against its background should reach at
least 4.5:1 contrast, and the accent should still be distinguishable for a
reader with red-green colour vision deficiency (vary lightness, not only hue).

## Every slide needs something to look at

An image, a chart, a diagram, an icon, or a deliberately composed shape. A slide
of only text is a paragraph with a title, and the audience reads ahead instead
of listening.

Compositions that work:

- **Split**: text on one side, a picture or diagram on the other.
- **Icon rows**: a filled circle with an icon, a bold label, one line of detail.
- **Card grid**: two by two, or three across, each card one claim.
- **Half-bleed picture**: the image runs to the slide edge, text sits on the
  calm half or on a scrim.
- **Number first**: one large figure with a short label under it.
- **Sequence**: numbered steps along a line, with the current step emphasised.
- **Before / after**: two columns with the same structure, so the difference is
  the only thing that changes.

Vary the composition across the deck. Three consecutive slides with the same
structure is where attention drops.

## Typography

Pair a header face with a body face that disagrees with it in a useful way -- a
serif header over a sans body, or a heavy grotesque over a light one. Two faces
are enough; a third is usually a mistake.

| Header | Body | Character |
|--------|------|-----------|
| Georgia | Calibri | editorial, warm |
| Cambria | Calibri | formal, report-like |
| Arial Black | Arial | blunt, high impact |
| Trebuchet MS | Calibri | friendly, informal |
| Consolas | Calibri | technical, product |
| Palatino Linotype | Garamond | literary, long-form |

Sizes for a projected deck:

| Element | Size | Weight |
|---------|------|--------|
| Slide title | 32-44 pt | bold |
| Section header inside a slide | 20-26 pt | bold |
| Body | 16-20 pt | regular |
| Caption, source, footnote | 10-13 pt | regular, muted |
| Big number callout | 60-96 pt | bold |

The gap between title and body matters more than the absolute sizes: a 20 pt
title over 18 pt body has no hierarchy at all. Below 14 pt, text stops being
readable from a distance -- if it does not fit, cut content rather than shrink.

## Space

- Keep at least half an inch between content and the slide edge.
- Use one gap value between blocks (0.3 in or 0.5 in) and repeat it. Mixed gaps
  read as misalignment even when nothing is actually misaligned.
- Leave a region deliberately empty. A slide filled edge to edge has no place
  for the eye to rest, and the important item loses its emphasis.
- Text boxes carry internal padding. When aligning a rule or a shape to the
  *text* edge, either zero the frame's margins or offset the shape by the
  padding; aligning to the box edge leaves a visible stagger.

## Mistakes worth naming

- **One layout for the whole deck.** Vary columns, cards and callouts.
- **Centred body text.** Left-align paragraphs and lists; centre titles and
  single-line callouts only.
- **A thin rule under every title.** It is decoration that adds no information
  and dates the deck. Separate with space or a background block instead.
- **Low contrast anywhere.** Light grey on cream, a dark icon on a dark panel,
  a coloured label on a same-tone card. Check icons as well as text.
- **Uneven emphasis.** Styling the opening slide carefully and leaving the rest
  plain is worse than a consistently plain deck.
- **Bullet characters typed into text.** Use the layout's list formatting; a
  pasted glyph will not align with the indent.
- **Content that overflows its box.** Longer text than the template slot was
  designed for wraps or spills. Render and look -- see
  [pptx-qa.md](./pptx-qa.md).
- **Decoration that survives its content.** When a template slot loses its
  item, delete the picture and the caption with the text, not just the text.