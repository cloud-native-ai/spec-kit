# Quickstart: Consolidate Draft Skills

**Spec**: `017-consolidate-draft-skills` | **Date**: 2026-06-18

## Prerequisites

- Branch `017-consolidate-draft-skills` checked out
- All 9 draft skills present in `draft/skills/`
- Existing formal skills in `skills/` are unmodified

## Step-by-Step Consolidation

### Step 1: Create document-utils

1. Create `skills/document-utils/` directory structure per data-model.md.
2. Write `SKILL.md` with YAML frontmatter (name, description with EN/CN triggers, skill_id) and format-specific sections (DOCX, PDF, PPTX, XLSX, Themes).
3. Copy shared `scripts/office/` from `draft/skills/docx-utils/scripts/office/` (one copy — identical across docx/pptx/xlsx).
4. Copy format-specific scripts:
   - `draft/skills/docx-utils/scripts/{accept_changes.py,comment.py,__init__.py,templates/}` → `scripts/docx/`
   - `draft/skills/pdf-utils/scripts/*.py` → `scripts/pdf/`
   - `draft/skills/pptx-utils/scripts/{add_slide.py,clean.py,__init__.py,thumbnail.py}` → `scripts/pptx/`
   - `draft/skills/xlsx-utils/scripts/recalc.py` → `scripts/xlsx/`
5. Copy reference docs:
   - `draft/skills/pdf-utils/{forms.md,reference.md}` → `references/{pdf-forms.md,pdf-reference.md}`
   - `draft/skills/pptx-utils/{editing.md,pptxgenjs.md}` → `references/{pptx-editing.md,pptx-creation.md}`
6. Copy themes: `draft/skills/theme-creator/{themes/,theme-showcase.pdf}` → `themes/`
7. Copy LICENSE.txt from any of the draft skills (identical across docx/pdf/pptx/xlsx).
8. Update all script path references in SKILL.md to use `${SKILL_HOME}/scripts/...`.

### Step 2: Create database-utils

1. Create `skills/database-utils/` directory structure per data-model.md.
2. Write `SKILL.md` with unified MySQL + PostgreSQL sections.
3. Copy `draft/skills/mysql-utils/scripts/query.py` → `scripts/query_mysql.py`.
4. Copy `draft/skills/postgres-utils/scripts/query.py` → `scripts/query_postgres.py`.
5. Create unified `scripts/query.py` that dispatches to the protocol-specific script.
6. Create unified `connections.example.json` with `protocol` field.
7. Merge `requirements.txt` (mysql-connector-python + psycopg2-binary).
8. Copy `.gitignore` from either source skill.
9. Create `references/README.md` merging setup guides from both sources.
10. Create `LICENSE.txt` with Apache-2.0 text.

### Step 3: Create browser-utils

1. Create `skills/browser-utils/` directory structure per data-model.md.
2. Write `SKILL.md` with Decision Tree, JS Automation, and Python Testing sections.
3. Copy `draft/skills/playwright-utils/{run.js,package.json}` → `scripts/js/`.
4. Copy `draft/skills/web-test/scripts/with_server.py` → `scripts/python/`.
5. Copy `draft/skills/playwright-utils/API_REFERENCE.md` → `references/playwright-api.md`.
6. Copy `draft/skills/web-test/examples/` → `examples/`.
7. Copy LICENSE.txt from `draft/skills/web-test/`.

### Step 4: Mirror to .specify/skills/

1. Copy each skill directory to `.specify/skills/<name>/`.
2. Verify byte-equivalence between `skills/<name>/` and `.specify/skills/<name>/`.

### Step 5: Validate

For each consolidated skill:
1. Verify YAML frontmatter has `name`, `description`, `skill_id`.
2. Verify all source skill workflows are represented in SKILL.md sections.
3. Verify all supporting files are present (scripts, references, themes, examples).
4. Verify `${SKILL_HOME}` and `${SKILL_WORKDIR}` path conventions are used.
5. Verify trigger keywords cover all constituent draft skills (EN + CN).

### Step 6: Remove Draft Skills

1. Remove the 9 directories from `draft/skills/`: docx-utils, pdf-utils, pptx-utils, theme-creator, xlsx-utils, mysql-utils, postgres-utils, playwright-utils, web-test.
2. Verify `draft/skills/` is empty or contains no skill-related content.

## Verification

After all steps:
- `ls skills/` includes `document-utils`, `database-utils`, `browser-utils`
- `ls .specify/skills/` includes the same three directories
- `ls draft/skills/` shows no remaining skill directories
- Each SKILL.md is parseable and follows the contract in `contracts/skill-format.md`
