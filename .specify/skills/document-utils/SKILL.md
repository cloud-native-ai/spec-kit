---
name: document-utils
description: |
  Create, read, edit and check office documents — Word (.docx), PDF, PowerPoint (.pptx)
  and Excel (.xlsx) — with one permissively licensed Python stack, and apply a visual
  theme to any of them.
  Use when the user mentions "Word", "docx", "PDF", "PowerPoint", "pptx", "Excel", "xlsx",
  "spreadsheet", "presentation", "slides", "deck", "report", "memo", "letter", "template",
  "theme", "文档", "Word文档", "PDF文件", "表格", "电子表格", "幻灯片", "演示文稿",
  "主题", "财务模型", "报告", or any request to produce, read, edit, or analyze
  office document files.
skill_id: "<SKILL:.specify/skills/document-utils/SKILL.md>"
license: MIT
metadata:
  author: spec-kit project
  version: "3.0"
classification: external
---

# Document Utilities

> **Concurrency obligation（执行义务，按指针抵达）**: this skill is an execution body — before the first real action, run the one-shot assessment (class → carrier → partition), default to concurrent execution for two or more independent units, and when serial name a reason code and record the `requested` / `effective` / `effective_reason` reading. Authored text: `.specify/shared/definitions/subagent-definitions.md` § The Concurrency Obligation; class table: `.specify/shared/declarations/facts/concurrency-class.yaml`; reason codes: `.specify/shared/declarations/facts/serial-reason.yaml`; reading fields: `.specify/shared/declarations/facts/effective-concurrency.yaml`. This body restates none of their rules.

## Overview

This skill produces, reads, edits and checks office documents in four formats,
and styles any of them with a chosen theme. Everything it runs is Python on a
permissive licence set (`requirements.txt` lists it with licences); the only
external program is LibreOffice, invoked headless through
`${SKILL_HOME}/scripts/office/soffice.py` for conversion, thumbnails and formula
recalculation.

- **DOCX** — create with `python-docx`, edit by unpacking the package, editing the
  markup and packing it again, accept tracked changes and add comments with the
  skill's own scripts, and check the result structurally before handover.
- **PDF** — read text and tables, create, merge/split/rotate/watermark/encrypt,
  render pages to images, and fill forms whether or not the file has fields.
- **PPTX** — create with `python-pptx`, edit an existing deck through the same
  unpack/edit/pack road so the template's masters and theme survive, and check
  the finished deck by extraction and by looking at rendered slides.
- **XLSX** — create and edit workbooks with `openpyxl`, write formulas rather
  than results, and recalculate through LibreOffice to obtain cached values.
- **Themes** — ten original presets plus custom ones, applied by role across any
  artifact.

Two capabilities of the previous implementation are deliberately gone, each with
a replacement: the vendored XSD schema subsystem (schema validation is replaced
by structural checks plus a library round trip in `office/validate.py`), and the
JavaScript creation routes (`docx-js`, PptxGenJS, `pdf-lib`), replaced by
`python-docx`, `python-pptx` and `reportlab`. The command-line PDF toolchain
(poppler, qpdf, pdftk) is likewise replaced by `pypdf`, `pdfplumber` and
`pypdfium2`. No Node toolchain is required anywhere in this skill.

## Quick Reference

| Task | Format | Approach |
|------|--------|----------|
| Read/analyze content | DOCX | `python-docx` paragraph walk, or unpack for the markup — see [docx-editing.md](./references/docx-editing.md) |
| Create new document | DOCX | `python-docx` — see [docx-creation.md](./references/docx-creation.md) |
| Edit existing document | DOCX | Unpack → edit markup → pack → validate — see [docx-editing.md](./references/docx-editing.md) |
| Accept tracked changes / comment | DOCX | `.specify/scripts/docx/accept_changes.py`, `.specify/scripts/docx/comment.py` |
| Read/extract text | PDF | `pypdf` or `pdfplumber` — see [pdf-operations.md](./references/pdf-operations.md) |
| Pull tables out of a PDF | PDF | `pdfplumber` table extraction — see [pdf-operations.md](./references/pdf-operations.md) |
| Create new PDF | PDF | `reportlab` — see [pdf-operations.md](./references/pdf-operations.md) |
| Merge/split/rotate/encrypt | PDF | `pypdf` — see [pdf-operations.md](./references/pdf-operations.md) |
| Render pages to images | PDF | `pypdfium2` via `.specify/scripts/pdf/convert_pdf_to_images.py` |
| Fill PDF forms | PDF | Field and field-less routes in [pdf-forms.md](./references/pdf-forms.md) |
| Read/analyze slides | PPTX | `python-pptx` extraction — see [pptx-qa.md](./references/pptx-qa.md); visual overview via `.specify/scripts/pptx/thumbnail.py` |
| Edit existing presentation | PPTX | Unpack → `add_slide.py` / markup edits → `clean.py` → pack — see [pptx-editing.md](./references/pptx-editing.md) |
| Create from scratch | PPTX | `python-pptx` — see [pptx-creation.md](./references/pptx-creation.md) |
| Read/analyze spreadsheet | XLSX | `openpyxl` (`data_only=True` for cached values) — see [xlsx-creation.md](./references/xlsx-creation.md) |
| Create/edit spreadsheet | XLSX | `openpyxl` with formulas, then `.specify/scripts/xlsx/recalc.py` — see [xlsx-creation.md](./references/xlsx-creation.md) |
| Check any Office package | DOCX/PPTX | `.specify/scripts/office/validate.py` (structural checks + round trip; XSD validation is no longer shipped) |
| Apply visual theme | Any | Role-based application in [themes-guide.md](./references/themes-guide.md) |

## DOCX

A `.docx` file is a ZIP of XML parts. Creating one is a library job; editing one
is a markup job, because a round trip through a library re-serializes parts the
edit never touched.

- **Creating**: `python-docx` owns the package inventories, numbering and style
  table. Set section geometry first, restyle built-in styles rather than cloning
  them, and validate before handover — [docx-creation.md](./references/docx-creation.md).
- **Editing**: `office/unpack.py` → edit the parts → `office/pack.py` →
  `office/validate.py`. Curly quotes go in as numeric character references;
  whitespace-sensitive runs need `xml:space="preserve"` —
  [docx-editing.md](./references/docx-editing.md).
- **Markup patterns**: tracked insertions/deletions/moves, comments, images and
  identifier ranges — [docx-xml-reference.md](./references/docx-xml-reference.md).
- **Revisions**: `docx/accept_changes.py` applies every tracked change as a
  Python transformation (no LibreOffice macro); `docx/comment.py` adds comments
  from the templates in `docx/templates/`.

## PDF

Everyday reading, creation and rearranging:
[pdf-operations.md](./references/pdf-operations.md). Rendering internals,
extraction tuning, encryption and troubleshooting:
[pdf-reference.md](./references/pdf-reference.md). Form filling, with and without
fields: [pdf-forms.md](./references/pdf-forms.md). The eight scripts under
`.specify/scripts/pdf/` carry the form workflow end to end: describe fields, recover
geometry, audit boxes, fill, and draw a validation overlay to look at.

## PPTX

- **Reading**: extract text with `python-pptx` (recipe in
  [pptx-qa.md](./references/pptx-qa.md)); get a visual overview from
  `.specify/scripts/pptx/thumbnail.py`, which converts through LibreOffice and composes a
  labelled grid.
- **Editing**: the unpack/edit/pack road keeps the template's masters, layouts
  and theme. `pptx/add_slide.py` registers a new slide from a layout or a copy,
  `pptx/clean.py` prunes what the edits orphaned —
  [pptx-editing.md](./references/pptx-editing.md).
- **Creating**: `python-pptx` — canvas and EMU, layouts and placeholder `idx`,
  text frames, shapes, pictures, tables, charts, notes —
  [pptx-creation.md](./references/pptx-creation.md).
- **Design**: palette directions, type pairings, sizes and spacing —
  [pptx-design.md](./references/pptx-design.md).
- **QA**: content extraction, template-leftover search, rendered-slide review
  and the verify-fix-reverify loop — [pptx-qa.md](./references/pptx-qa.md).

## XLSX

Write formulas, never their results: a workbook of hardcoded values cannot
recalculate. `openpyxl` writes and reads; `.specify/scripts/xlsx/recalc.py` runs
LibreOffice headless to fill cached values and prints a JSON verdict (error
cells, formula count) — read the verdict, not the exit code. Financial-model
colour coding, number formats and formula construction:
[xlsx-financial-models.md](./references/xlsx-financial-models.md); creation,
editing, streaming reads and verification:
[xlsx-creation.md](./references/xlsx-creation.md).

## Themes

Ten presets live in `${SKILL_HOME}/themes/`, each a markdown file declaring four
role colours (Base, Surface, Body, Accent) and a header/body face pair.
`theme-showcase.pdf` previews them one page each. Show the preview, ask which
preset to use, wait for an explicit choice, then apply its colours and faces by
role across the whole artifact. Usage, the preset list and custom-preset
authoring: [themes-guide.md](./references/themes-guide.md).

## Hard Constraints

Breaking any of these yields a file that is corrupt or wrong, not merely plain.

1. **DOCX page size**: set the section explicitly before adding content
   (`section.page_width` / `page_height`); US Letter is `Inches(8.5)` ×
   `Inches(11)`, A4 is `Mm(210)` × `Mm(297)`. A page break inherits the section it
   lands in.
2. **DOCX table widths**: set the width on every cell of a column, not only the
   first — Word derives a column's width from its cells, and one wide cell
   stretches the table past the margin.
3. **DOCX tracked changes**: the author defaults to "Claude" unless the user
   names another; write curly quotes as numeric character references in the
   markup.
4. **Excel formulas**: never hardcode calculated values; write formulas and run
   `${SKILL_HOME}/scripts/xlsx/recalc.py`, then read its JSON verdict.
5. **PPTX colours**: `RGBColor` takes three byte values or a six-digit hex string
   without `#`; a `#` prefix or an eight-digit ARGB value is rejected.
6. **PPTX bullets**: bullets come from the layout — set `paragraph.level`; never
   paste a bullet character into the text.
7. **Themes**: show `${SKILL_HOME}/themes/theme-showcase.pdf`, ask for the choice,
   and wait for explicit confirmation before applying.

## Path Conventions

- `${SKILL_HOME}/<relative-path>` — Skill-owned resources (scripts, references, themes, assets).
- `${SKILL_WORKDIR}/<relative-path>` — runtime/user-facing paths.
- Install paths of a particular agent never appear in this skill's text.

## Resources

### Scripts

| Directory | Contents |
|-----------|----------|
| `${SKILL_HOME}/scripts/office/` | Shared Office tools: `soffice.py`, `pack.py`, `unpack.py`, `validate.py`, `ooxml.py`, `helpers/`, `validators/` |
| `${SKILL_HOME}/scripts/docx/` | DOCX-specific: `accept_changes.py`, `comment.py`, `.specify/templates/` |
| `${SKILL_HOME}/scripts/pdf/` | PDF-specific: `check_bounding_boxes.py`, `check_fillable_fields.py`, `convert_pdf_to_images.py`, `create_validation_image.py`, `extract_form_field_info.py`, `extract_form_structure.py`, `fill_fillable_fields.py`, `fill_pdf_form_with_annotations.py` |
| `${SKILL_HOME}/scripts/pptx/` | PPTX-specific: `add_slide.py`, `clean.py`, `thumbnail.py`, `ooxml_parts.py` |
| `${SKILL_HOME}/scripts/xlsx/` | XLSX-specific: `recalc.py` |

`office/validate.py` checks well-formedness, namespace declarations, identifier
uniqueness and ranges, relationship and content-type inventories, the format's
markup rules, and — when the format's library is installed — a round trip that
re-opens the package. The vendored XSD schemas and the schema-validation
machinery are no longer part of this skill; those checks are the replacement.
`.xlsx` is detected but not validated, as before.

### References

| File | Description |
|------|-------------|
| `${SKILL_HOME}/references/docx-creation.md` | Creating new DOCX documents with `python-docx` |
| `${SKILL_HOME}/references/docx-editing.md` | Editing existing DOCX documents via the unpack/edit/pack road |
| `${SKILL_HOME}/references/docx-xml-reference.md` | WordprocessingML patterns for tracked changes, comments and images |
| `${SKILL_HOME}/references/pdf-operations.md` | Everyday PDF operations on the Python stack |
| `${SKILL_HOME}/references/pdf-forms.md` | PDF form filling, with and without fields |
| `${SKILL_HOME}/references/pdf-reference.md` | PDF internals: `pypdfium2`, `pdfplumber`, `pypdf`, `reportlab`; licences |
| `${SKILL_HOME}/references/pptx-creation.md` | `python-pptx` tutorial (creating presentations from scratch) |
| `${SKILL_HOME}/references/pptx-editing.md` | PPTX editing workflow (template-based, part surgery) |
| `${SKILL_HOME}/references/pptx-design.md` | Palette, type and spacing guidance for slides |
| `${SKILL_HOME}/references/pptx-qa.md` | Content and visual QA loop for a finished deck |
| `${SKILL_HOME}/references/xlsx-creation.md` | Creating, editing and checking workbooks with formulas |
| `${SKILL_HOME}/references/xlsx-financial-models.md` | Colour coding, number formats and formula standards for models |
| `${SKILL_HOME}/references/themes-guide.md` | Choosing, applying and authoring theme presets |

### Themes

| Directory | Contents |
|-----------|----------|
| `${SKILL_HOME}/themes/` | 10 theme preset files (`.md`) and `theme-showcase.pdf`, a generated preview of them |

## Dependencies

The installable set, with licences, is `${SKILL_HOME}/requirements.txt`; every
package is permissive and no GPL/AGPL package is imported. Scripts import their
third-party libraries inside the functions that use them, so `-h`, `--help` and
`--version` answer even where none of them is installed.

- **DOCX**: `python-docx` (MIT) for creation and round-trip checks; the
  unpack/edit/pack road needs only the standard library. `defusedxml` (PSF-2.0)
  hardens XML parsing when present.
- **PDF**: `pypdf` (BSD-3-Clause), `pdfplumber` (MIT), `pypdfium2`
  (Apache-2.0 OR BSD-3-Clause, bundled PDFium BSD-3-Clause), `Pillow` (MIT-CMU),
  `reportlab` (BSD-3-Clause). Optional OCR: `pytesseract` + the Tesseract binary
  (Apache-2.0), imported by no script.
- **PPTX**: `python-pptx` (MIT), `Pillow` and `pypdfium2` for the thumbnail grid.
- **XLSX**: `openpyxl` (MIT).
- **External program**: LibreOffice (`soffice`, MPL-2.0), invoked only as a
  subprocess via `.specify/scripts/office/soffice.py` for conversion, PNG thumbnails and
  recalculation. It is not bundled and not imported. On hosts whose sandbox
  forbids the socket family LibreOffice needs, conversion is unavailable and
  `soffice.af_unix_available()` reports it; the Python routes above still work.

## Wrap-up

<!-- AUTO-GENERATED by probe-utils.py --action compile-embeds — truth source: .specify/shared/definitions/probe-definitions.md (## Handler / ## HandlerBinding) — fingerprint: 2845f5641171 — do not edit; edit the registry, then recompile -->

**Runtime-mode gate.** If `${SKILL_WORKDIR}/.specify/` does not exist, this skill is running in standalone mode (a non–Spec Kit deployment, e.g. a global agent skills directory) — skip this entire Wrap-up step: no engine call, no feedback entry.

1. Run Determination — `python3 .specify/scripts/python/run-determination.py --action determine --unit-id "skill:document-utils" --unit-type skill --run-id <RUN_ID> --complexity <COMPLEXITY>`；source args when available: `--session-file <SESSION_FILE> --session-rows <SESSION_ROWS> --tool <TOOL> --proxy-paths <PROXY_PATHS> --token-note <TOKEN_NOTE> --elapsed-ms <ELAPSED_MS> --elapsed-note <ELAPSED_NOTE> --names-current <NAMES_CURRENT> --names-baseline <NAMES_BASELINE> --declared-check <DECLARED_CHECK> --green-check <GREEN_CHECK> --red-first-refs <RED_FIRST_REFS> --collected <COLLECTED> --prev-user-turn-class <PREV_USER_TURN_CLASS> --unresolved-red <UNRESOLVED_RED> --red-source <RED_SOURCE>`
   尖括号为本轮运行时值——代入后照抄执行(占位 = 参数名去 --、转下划线、全大写;渲染集 = 引擎 manifest required + source,身份对已带实值)
2. Exec Quant — `python3 .specify/scripts/python/exec-quant.py --action collect --unit-id "skill:document-utils" --unit-type skill`；source args when available: `--run-id <RUN_ID>`
3. Feedback Record — `python3 .specify/scripts/python/feedback-utils.py --action record --unit-id "skill:document-utils" --unit-type skill --run-id <RUN_ID> --review <REVIEW> --points <POINTS>`
4. Threshold Notice — `.specify/shared/workflow/feedback-step.md` § "Threshold prompt protocol (canonical semantics for step 6)"
5. Token Reflection — `.specify/shared/workflow/feedback-step.md` § "Reflection procedure (the embedded step points here)"
6. Closeout — `.specify/shared/workflow/artifact-commit-step.md` § "The `## Close-out` step"
