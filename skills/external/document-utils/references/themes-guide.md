# Applying a Theme

A theme is a small, fixed decision about colour and type: four colours with named
roles, and one header/body face pairing. Ten presets ship with this skill under
`${SKILL_HOME}/themes/`, one markdown file each. Once a preset is chosen, the same
four colours and the same two faces go on every artifact of the job — deck,
document, workbook or HTML page — so the pieces read as one set.

## What a preset declares

Every preset file carries the same four fields, and the role names are the
contract you apply:

| Role | What it paints |
|------|----------------|
| **Base** | Titles, section headers, table header bands |
| **Surface** | The page or slide background |
| **Body** | Running text, figures, captions |
| **Accent** | The one thing to notice: callouts, rules, highlights, links |

Plus a **Typography** pair (headers and body text) and a **Best Used For** line
that says which jobs the palette suits. Nothing else is introduced at apply
time: no fifth colour, no third face, no gradient the preset did not declare.

The preset file is the authority for its values. `theme-showcase.pdf` in the same
directory is a generated preview of those files — one page per preset, swatches
first and then the palette in use — and is never edited by hand. Its type samples
are drawn with the PDF base-14 faces standing in for the named Office faces, so
judge the colours from the preview and the faces from the preset's own names.

## Choosing a preset

1. **Show the preview.** Display `${SKILL_HOME}/themes/theme-showcase.pdf` so the
   choice is made by looking at the palettes, not by reading hex codes.
2. **Ask which one.** Name the presets by their titles and let the reader pick.
3. **Wait for the answer.** An explicit choice is required before anything is
   styled; a guess is not a choice.
4. **Apply it.** Read the chosen preset file and put its colours and faces on the
   artifact, consistently, from the first page to the last.

If none of the ten fits, write a custom preset (below) and run the same four
steps with it.

## Applying the colours and faces

- Read the chosen file from `${SKILL_HOME}/themes/` and take the hex values and
  face names from it verbatim; do not re-derive them from the preview image.
- Paint by role: background from **Surface**, headings from **Base**, running
  text from **Body**, emphasis from **Accent**. A dark preset such as Citrus
  Terminal simply has a dark Surface and a light Body — the roles do not change.
- Set the header face on titles and section heads and the body face everywhere
  else. Two faces, not three.
- Keep the accent rare. It marks what the reader must notice; used everywhere it
  marks nothing.
- Check readability on the surface you actually used. The contrast and type-size
  criteria for slides are owned by [pptx-design.md](./pptx-design.md)
  § Typography and § Palette starting points; apply them there rather than
  inventing a second threshold here.
- When the named face is missing on the host that renders the artifact (a PDF
  engine, a headless converter), substitute the closest available face and say
  so in the handover note; the named face remains what the document declares.

For a deck, the preset's colours reach the file through its theme part
(`ppt/theme/theme1.xml`) or through explicit shape and run formatting — see
[pptx-creation.md](./pptx-creation.md) § Masters, layouts and themes. For a
workbook, cell fills and font colours carry the same four roles; the
financial-model colour conventions in
[xlsx-financial-models.md](./xlsx-financial-models.md) still apply to input,
formula and link cells and are not replaced by a theme.

## The ten presets

| Preset | File | Character |
|--------|------|-----------|
| Harbour Graphite | `themes/harbour-graphite.md` | Cool slate and teal; settled, corporate |
| Terracotta Ledger | `themes/terracotta-ledger.md` | Clay and ink on cream; printed-report warmth |
| Meadow Signal | `themes/meadow-signal.md` | Hedge green on field white; growth subjects |
| Indigo Blueprint | `themes/indigo-blueprint.md` | Drafting indigo; plans and specifications |
| Citrus Terminal | `themes/citrus-terminal.md` | Dark surface, amber and mint; screens and demos |
| Glacier Mint | `themes/glacier-mint.md` | Ice white and deep teal; neutral, clinical |
| Copper Dusk | `themes/copper-dusk.md` | Copper on warm sand; brand and hospitality |
| Orchid Press | `themes/orchid-press.md` | Aubergine on bone; editorial and cultural |
| Sandstone Brief | `themes/sandstone-brief.md` | Olive stone on unbleached paper; procedural |
| Newsprint Ink | `themes/newsprint-ink.md` | Ink on newsprint with one red; fast reading |

## Writing a custom preset

When the ten do not fit the job, author an eleventh file in the same shape: a
title, one line of intent, the four role swatches with hex values and colour
names, the header/body pair, and a Best Used For line. Choose the colours so that
Body and Accent stay readable on the chosen Surface, name the file after what the
palette represents, and show it for review before applying it. A custom preset
lives with the job's artifacts, not in the skill directory; the shipped ten stay
as they are.