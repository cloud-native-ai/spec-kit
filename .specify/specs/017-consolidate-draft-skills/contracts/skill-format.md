# Contract: Skill Format Specification

**Spec**: `017-consolidate-draft-skills` | **Date**: 2026-06-18

This contract defines the structural requirements for each consolidated skill's SKILL.md file. All three skills (document-utils, database-utils, browser-utils) MUST conform to this specification.

## C-001: YAML Frontmatter

Each SKILL.md MUST begin with a YAML frontmatter block containing:

```yaml
---
name: <skill-name>           # Required. Kebab-case identifier matching directory name.
description: |                # Required. Multi-line trigger description.
  <description text>          # MUST include English AND Chinese trigger keywords.
skill_id: "<SKILL:path>"     # Required. Canonical path-based ID.
---
```

### Validation Rules

- `name` MUST match the directory name (e.g., `document-utils` for `skills/document-utils/SKILL.md`).
- `description` MUST be a YAML block scalar (`|`) with trigger keywords for AI agent matching.
- `description` MUST include both English and Chinese trigger terms.
- `skill_id` MUST follow the pattern `<SKILL:.specify/skills/<name>/SKILL.md>`.

## C-002: Markdown Body Structure

The SKILL.md body MUST contain the following sections in order:

1. `# <Skill Title>` — Top-level heading.
2. `## Overview` — Brief description and trigger conditions.
3. Content sections — Skill-specific workflow, instructions, and reference material.
4. `## Path Conventions` — MUST include `${SKILL_HOME}` and `${SKILL_WORKDIR}` convention declarations per `templates/commands/skills.md`.
5. `## Resources` — MUST list scripts, references, and assets subdirectories.
6. `## Dependencies` — MUST list all required external tools and libraries.

### Path Convention Section

MUST contain the following declarations:

```markdown
## Path Conventions

This Skill follows the canonical path conventions:

- Use `${SKILL_HOME}/<relative-path>` for every Skill-owned resource reference.
- Use `${SKILL_WORKDIR}/<relative-path>` for every runtime/user-facing path.
- Never embed agent-specific install paths.
```

### Shell Script Preamble

Every shell script under `${SKILL_HOME}/scripts/` MUST begin with:

```bash
SKILL_HOME="${SKILL_HOME:-$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd -P)}"
SKILL_WORKDIR="${SKILL_WORKDIR:-$(pwd -P)}"
```

## C-003: document-utils Content Sections

The document-utils SKILL.md MUST contain format-specific sections:

1. `## Quick Reference` — Table routing users to the correct format section.
2. `## DOCX` — Word document creation, editing (XML), and analysis workflows.
3. `## PDF` — PDF reading, creation, manipulation, forms, and OCR workflows.
4. `## PPTX` — Presentation creation, editing, and visual QA workflows.
5. `## XLSX` — Spreadsheet creation, editing, formulas, and recalculation workflows.
6. `## Themes` — Cross-cutting theme selection and application (10 pre-set + custom).

Each format section MUST preserve the key workflows from its source draft skill without content loss.

## C-004: database-utils Content Sections

The database-utils SKILL.md MUST contain:

1. `## Quick Reference` — Supported databases and protocols table.
2. `## Setup` — Unified connection configuration with protocol field.
3. `## Usage` — Command interface (--list, --tables, --schema, --query, --limit).
4. `## Database Selection` — Intent-to-database matching guidance.
5. `## Supported Databases` — MySQL, PostgreSQL, ClickHouse, Apache Doris/SelectDB with protocol and port info.
6. `## Safety Features` — All safety features from both source skills.
7. `## Troubleshooting` — Combined troubleshooting table.

## C-005: browser-utils Content Sections

The browser-utils SKILL.md MUST contain:

1. `## Overview` — Combined automation + testing capabilities.
2. `## Decision Tree` — Choosing between JS automation and Python testing approaches.
3. `## Setup` — Installation for both Node.js Playwright and Python Playwright.
4. `## JavaScript Automation` — Dev server detection, script execution via run.js, common patterns (from playwright-utils).
5. `## Python Testing` — Server lifecycle management, sync API patterns, examples (from web-test).
6. `## Common Patterns` — Cross-language patterns (screenshots, responsive testing, form filling, link checking).
7. `## Troubleshooting` — Combined troubleshooting guidance.

## C-006: Mirror Requirement

After creation in `skills/<name>/`, each skill MUST be mirrored to `.specify/skills/<name>/` following the established Spec Kit installation layout. The mirror MUST be byte-equivalent to the source.

## C-007: Trigger Keyword Coverage

Each skill's `description` field MUST cover the trigger keywords from ALL constituent draft skills. Specifically:

- **document-utils**: MUST trigger on mentions of Word/docx, PDF, PowerPoint/pptx, Excel/xlsx, spreadsheet, presentation, slides, deck, theme, 文档, 表格, 幻灯片, 演示文稿, 主题.
- **database-utils**: MUST trigger on mentions of MySQL, PostgreSQL, database, SQL, query, ClickHouse, Doris, SelectDB, 数据库, 查询.
- **browser-utils**: MUST trigger on mentions of browser, Playwright, web test, screenshot, automation, responsive, 浏览器, 网页测试, 截图, 自动化.
