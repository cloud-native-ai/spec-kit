# Contract: Glossary File Format

**Artifact**: `.specify/memory/glossary.md` (one per project) — seeded from `templates/glossary-template.md`.

## C-1 Location & cardinality

- The glossary MUST live at exactly `.specify/memory/glossary.md`.
- There MUST be exactly one glossary per project. Per-feature glossaries MUST NOT be created.

## C-2 File structure

The file MUST contain, in order:

1. A `# Project Glossary (项目词汇表)` H1 title.
2. A preamble block stating the authoring rules verbatim (seeded from the template):
   - Common everyday words MUST NOT be recorded.
   - User edits are authoritative; automatic proposals MUST NOT overwrite user-authored entries.
   - Conflicts MUST be confirmed by the user before writing.
3. A single Markdown table of entries with this exact header row:

   ```
   | Canonical | Variants | Meaning | Origin | Status |
   |-----------|----------|---------|--------|--------|
   ```

## C-3 Row rules

- `Canonical`: non-empty; unique case-insensitively across all rows; not a common everyday word.
- `Variants`: comma-separated list of homophone/confusable forms, or `-` when none.
- `Meaning`: non-empty one-line domain definition.
- `Origin`: exactly one of `auto` | `user`.
- `Status`: exactly one of `proposed` | `confirmed`.
- An empty glossary (zero data rows) is valid.

## C-4 Empty-state contract

On a project with no seedable terms, the file MUST still be created with the title, preamble, and the table header (zero data rows). A single placeholder row with `None yet.` in the first column and `-` elsewhere MAY be used, matching the project's Resource Registry convention.

## C-5 Non-destructive contract

- Re-running instruction generation MUST NOT discard or reorder existing rows.
- User-authored rows (`Origin = user`) MUST be preserved byte-for-byte across regenerations unless the user explicitly confirmed a change.

## C-6 Validation

`glossary-utils.py --action validate` MUST return success only when C-2 and C-3 hold, and non-zero with a specific message otherwise (see `glossary-utils-cli.md`).
