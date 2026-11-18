# WordprocessingML Markup Reference

The markup patterns an edit needs, and the rules the checker enforces. Element
names are the standard ones from ECMA-376 / ISO-IEC 29500; the examples are
minimal on purpose, so each one shows only the part being discussed.

Prefixes used below: `w` = wordprocessingml, `w14`/`w15`/`w16cid`/`w16cex` = the
Word extension namespaces, `r` = officeDocument relationships, `a` = drawingml,
`wp` = wordprocessingDrawing. Declare a prefix on the root before using it, and
list any extension prefix in `mc:Ignorable` so an older consumer can skip it.

## What "valid" means here

This skill no longer ships XSD schemas. `office/validate.py` checks instead:

- every part is well-formed XML, and every `mc:Ignorable` prefix is declared,
- identifiers that must be unique are unique, and Word's identifier ranges hold,
- every relationship target exists and every part is reachable,
- `[Content_Types].xml` declares the main parts and the media extensions,
- revision markup is internally consistent (no live text inside a deletion),
- comment markers pair up and name a comment that exists,
- and, when python-docx is installed, the re-packed file opens.

Hand-written markup that satisfies these opens in Word. Markup that satisfies a
schema but breaks an inventory does not.

## Tracked changes

A revision records three things: what kind of change it is, who made it, and
when. The `w:id` is unique among revisions in the part.

### Insertion

```xml
<w:ins w:id="101" w:author="Claude" w:date="2026-01-01T09:00:00Z">
  <w:r><w:t>the added words</w:t></w:r>
</w:ins>
```

The wrapper sits where a run would sit — a child of `w:p`, or of `w:tc` content
inside a table cell. It may contain several runs, and whole paragraphs when the
insertion spans them.

### Deletion

```xml
<w:del w:id="102" w:author="Claude" w:date="2026-01-01T09:05:00Z">
  <w:r><w:delText>the removed words</w:delText></w:r>
</w:del>
```

Inside a deletion the text element is `w:delText` (and `w:delInstrText` for field
instructions). A `w:t` there is reported as a violation: it would render as live
text while being marked deleted.

### The smallest edit

Change one word by deleting the old run and inserting the new one, leaving the
surrounding runs untouched:

```xml
<w:p>
  <w:r><w:t xml:space="preserve">Revenue grew </w:t></w:r>
  <w:del w:id="103" w:author="Claude" w:date="2026-01-01T09:10:00Z">
    <w:r><w:delText>slowly</w:delText></w:r>
  </w:del>
  <w:ins w:id="104" w:author="Claude" w:date="2026-01-01T09:10:00Z">
    <w:r><w:t>sharply</w:t></w:r>
  </w:ins>
  <w:r><w:t xml:space="preserve"> last quarter.</w:t></w:r>
</w:p>
```

Note the preserved spaces on the untouched runs: they carry the spacing that
the deleted and inserted words used to sit between.

### Deleting a whole paragraph or list item

Two statements are needed: the content is deleted, and the paragraph mark is
deleted. Without the second, an empty paragraph survives the acceptance.

```xml
<w:p>
  <w:pPr>
    <w:numPr><w:ilvl w:val="0"/><w:numId w:val="3"/></w:numPr>
    <w:rPr><w:del w:id="105" w:author="Claude" w:date="2026-01-01T09:20:00Z"/></w:rPr>
  </w:pPr>
  <w:del w:id="106" w:author="Claude" w:date="2026-01-01T09:20:00Z">
    <w:r><w:delText>Item to remove</w:delText></w:r>
  </w:del>
</w:p>
```

Accepting this joins the paragraph to the following one, which is exactly what
`docx/accept_changes.py` does.

### Inserting a whole paragraph

The new paragraph's own mark is an insertion too:

```xml
<w:p>
  <w:pPr><w:rPr><w:ins w:id="107" w:author="Claude" w:date="2026-01-01T09:30:00Z"/></w:rPr></w:pPr>
  <w:ins w:id="108" w:author="Claude" w:date="2026-01-01T09:30:00Z">
    <w:r><w:t>A new paragraph.</w:t></w:r>
  </w:ins>
</w:p>
```

### Rejecting another author's insertion

Do not delete their `w:ins`. Nest your deletion inside it, so both statements
remain readable:

```xml
<w:ins w:id="200" w:author="Reviewer" w:date="2025-12-20T10:00:00Z">
  <w:del w:id="201" w:author="Claude" w:date="2026-01-01T09:40:00Z">
    <w:r><w:delText>their added words</w:delText></w:r>
  </w:del>
</w:ins>
```

### Restoring another author's deletion

Their `w:del` stays as it is; your insertion follows it with the text they
removed:

```xml
<w:del w:id="202" w:author="Reviewer" w:date="2025-12-20T10:05:00Z">
  <w:r><w:delText>words they removed</w:delText></w:r>
</w:del>
<w:ins w:id="203" w:author="Claude" w:date="2026-01-01T09:45:00Z">
  <w:r><w:t>words they removed</w:t></w:r>
</w:ins>
```

### Moves

A move is a paired `w:moveFrom` / `w:moveTo` with range markers naming the span:

```xml
<w:moveFromRangeStart w:id="204" w:name="move1"/>
<w:moveFrom w:id="205" w:author="Claude" w:date="2026-01-01T09:50:00Z">
  <w:r><w:delText>the travelling text</w:delText></w:r>
</w:moveFrom>
<w:moveFromRangeEnd w:id="204"/>
```

The destination carries `moveToRangeStart` / `moveTo` / `moveToRangeEnd` with the
same `w:name`. Accepting a move keeps the destination and drops the source.

### Formatting revisions

A formatting change records the previous properties in a `*Change` element
(`w:rPrChange`, `w:pPrChange`, `w:tblPrChange`, `w:trPrChange`, `w:tcPrChange`,
`w:sectPrChange`, `w:numberingChange`). The current properties stay where they
always were; accepting the revision removes the record.

## Comments

A comment is four parts that must agree, plus markers in the document.

| Part | Root | Carries |
|------|------|---------|
| `word/comments.xml` | `w:comments` | the text, author, date, initials |
| `word/commentsExtended.xml` | `w15:commentsEx` | threading (`paraIdParent`) and resolved state (`done`) |
| `word/commentsIds.xml` | `w16cid:commentsIds` | `paraId` ↔ `durableId` |
| `word/commentsExtensible.xml` | `w16cex:commentsExtensible` | `durableId` with a UTC date |

`docx/comment.py` writes all four from the templates beside it and registers
them in `word/_rels/document.xml.rels` and `[Content_Types].xml`. The identifiers
it generates are eight hexadecimal digits below `0x80000000`.

One comment:

```xml
<w:comment w:id="0" w:author="Claude" w:date="2026-01-01T10:00:00Z" w:initials="C">
  <w:p w14:paraId="1A2B3C4D" w14:textId="77777777">
    <w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:annotationRef/></w:r>
    <w:r><w:t>Is this figure final?</w:t></w:r>
  </w:p>
</w:comment>
```

Its markers in `document.xml`, as children of `w:p`:

```xml
<w:commentRangeStart w:id="0"/>
<w:r><w:t>the commented text</w:t></w:r>
<w:commentRangeEnd w:id="0"/>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="0"/></w:r>
```

A reply nests its range inside the parent's and points at the parent's paragraph
id in `commentsExtended.xml`:

```xml
<w15:commentEx w15:paraId="5E6F7A8B" w15:paraIdParent="1A2B3C4D" w15:done="0"/>
```

Every `commentRangeStart` needs a matching `commentRangeEnd`, and every marker
id needs a comment with that id — the checker reports orphans in both directions.

`word/people.xml` (`w15:people`) is the optional directory of comment authors;
`docx/templates/people.xml` is a starting point when a document needs it.

## Images

An image is three registrations and one drawing:

1. the media part, e.g. `word/media/image1.png`,
2. a relationship in `word/_rels/document.xml.rels` with type
   `.../relationships/image` and target `media/image1.png`,
3. a content-type default for the extension (`png` → `image/png`),
4. the drawing in the run:

```xml
<w:r>
  <w:drawing>
    <wp:inline distT="0" distB="0" distL="0" distR="0">
      <wp:extent cx="5029200" cy="2857500"/>
      <wp:docPr id="1" name="Picture 1"/>
      <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
          <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:nvPicPr><pic:cNvPr id="1" name="image1.png"/><pic:cNvPicPr/></pic:nvPicPr>
            <pic:blipFill><a:blip r:embed="rId7"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
            <pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="5029200" cy="2857500"/></a:xfrm>
              <a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
          </pic:pic>
        </a:graphicData>
      </a:graphic>
    </wp:inline>
  </w:drawing>
</w:r>
```

Extents are English Metric Units: 914400 per inch, 360000 per centimetre.
`r:embed` must name the image relationship; a dangling id is reported before the
file is ever opened.

## Whitespace and identifiers

- A `w:t` whose text begins or ends with whitespace carries
  `xml:space="preserve"`. Without it the space is dropped on load.
- Layout whitespace between elements is cosmetic; `pack.py` removes it and never
  touches the inside of a text element.
- `w14:paraId` and `w14:textId` are eight hexadecimal digits; `paraId` must be
  below `0x80000000` and unique within the part.
- `w16cid:durableId` is below `0x7FFFFFFF`; in `word/numbering.xml` it is written
  in decimal, elsewhere in hexadecimal.
- `validate.py --auto-repair` rewrites identifiers that break these limits and
  adds missing `xml:space` attributes; it reports each edit it makes.