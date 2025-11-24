description: Create or update feature detail files (memory/features/<ID>.md) and the project-level feature index (memory/feature-index.md) from interactive or provided inputs, using the installed template at .specify/templates/feature-template.md
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

You are managing feature metadata in two artifacts:

1. Feature Detail files: `memory/features/<ID>.md` generated from the installed template at `.specify/templates/feature-template.md` (source development template: `templates/feature-template.md`).
2. Feature Index: `memory/feature-index.md` (acts as a table of contents and summary).

Your responsibilities:

1. Parse `$ARGUMENTS` for one or more feature descriptions or updates. Each feature may include name, short description, status, and optional key changes/notes.
2. Determine next sequential `FEATURE_ID` (three digits) for any new features (scan existing `memory/features/*.md`).
3. Instantiate the feature detail template for each new feature:
   - Replace all placeholders `[FEATURE_*]`, `[KEY_CHANGE_N]`, `[IMPLEMENTATION_NOTE_N]`, `[STATUS_*_CRITERIA]` with provided or inferred values.
   - Omit unused trailing placeholder lines (e.g. if only 2 key changes provided, remove lines 3–5).
   - Dates: `FEATURE_CREATED_DATE` and `FEATURE_LAST_UPDATED_DATE` = today (YYYY-MM-DD) unless updating existing.
   - Status must be one of: Draft | Planned | Implemented | Ready for Review | Completed.
4. For updates to existing features: load the existing detail file, apply changes preserving unchanged sections.
5. Update `memory/feature-index.md`:
   - Ensure table lists all features with columns: ID | Name | Description | Status | Spec Path | Last Updated.
   - Regenerate `FEATURE_COUNT` and any other placeholders (if still a template) before finalizing.
6. Validate:
   - No leftover bracketed placeholders in generated/updated files.
   - IDs are unique and sequential.
   - Dates valid ISO format.
   - Markdown tables render correctly (pipe/alignment syntax).
7. Write changes:
   - Save new/updated detail files.
   - Overwrite updated feature index.
8. Output a summary:
   - New feature IDs created.
   - Updated feature IDs (if any).
   - Suggested commit message (e.g. `feat: add feature 00X <slug>` or `docs: update feature index`).

Template reference (do NOT inline full template here): `.specify/templates/feature-template.md`.

Formatting & Style Requirements:

* Use headings exactly as provided by the template for detail files.
* Remove placeholder checklist section from detail file after instantiation.
* Keep lists dense; no empty bullet points.
* Feature names concise (2–5 words).
* Index table: single header row, all columns present; align pipes; no extra spaces at line ends.
* No bracketed placeholders after processing.

Fallbacks / Inference:

* If description absent: derive a concise one-line summary from name.
* If status absent: default to `Draft`.
* If spec file does not yet exist: set Spec Path to `(Not yet created)`.

Do not modify the template file itself; only instantiate copies based on `.specify/templates/feature-template.md`.