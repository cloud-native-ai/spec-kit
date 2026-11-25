# Editing an Existing Word Document

Two roads lead through an existing `.docx`. Pick by the size of the change:

| Change | Road |
|--------|------|
| Read text, append paragraphs, restyle, add a table | python-docx directly on the file |
| Tracked changes, comments, surgical markup edits | unpack → edit the XML → pack |

The second road exists because a revision is a statement about *who changed
what*, and that statement lives in markup python-docx does not model. Everything
below runs on Python 3.10+; only the optional round-trip check needs python-docx.

## Getting the file into a usable shape

A legacy `.doc` is not an OPC package. Convert it first:

```bash
python3 "${SKILL_HOME}/scripts/office/soffice.py" --headless --convert-to docx legacy.doc
```

`soffice.py` is the LibreOffice wrapper: it selects the headless VCL plugin and
gives each run its own user profile, so two conversions at once do not collide.
As a Python API it also offers `convert()`, `thumbnail()` and `recalc()`.
LibreOffice must be installed; where a sandbox forbids AF_UNIX sockets,
`af_unix_available()` reports False and the conversion cannot run there.

## Reading content

```python
from docx import Document

document = Document("report.docx")
for paragraph in document.paragraphs:
    print(paragraph.style.name, paragraph.text)
```

`paragraph.text` shows the accepted view: it includes inserted text and omits
deleted text. To see the revisions themselves, read the markup:

```bash
python3 "${SKILL_HOME}/scripts/office/unpack.py" report.docx unpacked/
```

## Rendering for a visual check

```bash
python3 "${SKILL_HOME}/scripts/office/soffice.py" --headless --convert-to pdf report.docx
```

Then use the PDF tools in `.specify/scripts/pdf/` to rasterise pages. For a single
first-page image, `soffice.thumbnail("report.docx", outdir="preview/")` converts
straight to PNG.

## Accepting every tracked change

```bash
python3 "${SKILL_HOME}/scripts/docx/accept_changes.py" redlined.docx clean.docx
```

This is a Python transformation, not a LibreOffice macro: insertions keep their
content and lose their wrapper, deletions lose their content, moves are applied
as the insertion/deletion pair they are, formatting revisions keep the new
formatting, and a deleted paragraph mark joins its paragraph to the next one.
The input file is never modified; parts without revisions are copied unchanged.

## The unpack → edit → pack road

### 1. Unpack

```bash
python3 "${SKILL_HOME}/scripts/office/unpack.py" report.docx unpacked/
```

The parts are extracted, every XML part is indented for reading, and two
tidying passes run on a DOCX:

- adjacent revision wrappers by one author are joined (`--simplify-redlines false` to keep them),
- adjacent runs with identical formatting are joined (`--merge-runs false` to keep them).

Both passes are cosmetic: they change how many elements carry a change, never
what the document says. Curly quotes are written as numeric character references
so a later re-save cannot alter them.

### 2. Edit the markup

Work in `unpacked/word/document.xml`. The rules that matter:

- Wrap every edit in a revision. An unwrapped edit is invisible to a reviewer
  and fails the comparison against the original.
- Use one author name consistently — the default is `Claude`, or the name the
  user asks for. Pass the same name to `validate.py --author`.
- Deleted text goes in `w:delText`, never `w:t`, inside `w:del`.
- A run's text that begins or ends with a space needs `xml:space="preserve"`.
- Comment markers are children of `w:p`, never of `w:r`.

`docx-xml-reference.md` carries the markup patterns, including how to reject
another author's insertion and how to restore another author's deletion.

To add a comment, let the script write the four comment parts and their
registrations, then place the markers it prints:

```bash
python3 "${SKILL_HOME}/scripts/docx/comment.py" unpacked/ 0 "Check this figure" --author "Claude"
python3 "${SKILL_HOME}/scripts/docx/comment.py" unpacked/ 1 "Agreed" --parent 0
```

### 3. Pack

```bash
python3 "${SKILL_HOME}/scripts/office/pack.py" unpacked/ report-edited.docx --original report.docx
```

With `--original`, the tree is checked and mechanically repairable defects are
fixed before anything is written; a failed check means no output file. Packing
removes the indentation unpack added, keeps text runs byte-exact, and writes
`[Content_Types].xml` as the first member. Use `--validate false` only when the
tree is knowingly incomplete.

### 4. Check the result on its own

```bash
python3 "${SKILL_HOME}/scripts/office/validate.py" report-edited.docx --original report.docx --verbose
```

`--auto-repair` fixes whitespace preservation and out-of-range identifiers in an
unpacked tree. The paragraph census at the end (`Paragraphs: 12 -> 14 (+2)`) is
informational: a surprising delta is worth a look, not a failure by itself.

## Pitfalls that cost the most time

- **Editing inside someone else's revision.** Their insertion is their
  statement; to remove it, nest your `w:del` inside their `w:ins`.
- **`w:t` inside `w:del`.** Word shows the deleted text as live text. Use
  `w:delText`.
- **Lost spaces.** Merging runs or re-indenting a part can drop a leading space
  unless the run carries `xml:space="preserve"`.
- **Identifiers out of range.** `w14:paraId` must stay below `0x80000000` and
  `w16cid:durableId` below `0x7FFFFFFF`; `--auto-repair` rewrites offenders.
- **Unreferenced parts.** Adding a part without a relationship, or leaving a
  part behind after deleting its relationship, makes the package look corrupt.
- **Skipping the comparison.** Packing without `--original` writes whatever the
  tree says, including edits nobody tracked.