# Implementation Plan: Consolidate Draft Skills into Formal Skills

**Branch**: `017-consolidate-draft-skills` | **Date**: 2026-06-18 | **Spec**: [requirements.md](requirements.md)
**Input**: Specification from `.specify/specs/017-consolidate-draft-skills/requirements.md`

## Summary

Consolidate 9 draft skills from `draft/skills/` into 3 formal skills (`document-utils`, `database-utils`, `browser-utils`) following the established Spec Kit skill format. Each formal skill merges related draft skills into a unified SKILL.md with format-specific sections, preserves all supporting files (scripts, references, examples, configuration), and follows the `${SKILL_HOME}` / `${SKILL_WORKDIR}` path conventions. After validation, the 9 source draft skill directories are removed.

No standalone research.md — findings inlined below. All technical decisions are derived from existing draft skill content and the established skill format in `templates/skills-template.md`.

## Technical Context

**Language/Version**: N/A — Skills are prompt/document artifacts (SKILL.md + supporting files), not compiled code. Supporting scripts are Python 3.8+ and Node.js (inherited from drafts).
**Primary Dependencies**: N/A — No new runtime dependencies. Each skill inherits its draft dependencies (docx-js, pypdf, pdfplumber, reportlab, openpyxl, markitdown, pptxgenjs, mysql-connector-python, psycopg2-binary, playwright).
**Storage**: N/A — File-based skill definitions under `skills/` and `.specify/skills/`.
**Testing**: Manual verification — compare consolidated SKILL.md coverage against source drafts; validate YAML frontmatter; confirm AI agent discoverability.
**Target Platform**: Cross-platform (skill files are consumed by AI agents on any OS).
**Project Type**: Code generator / framework — extends `skills/` directory with new skill packages.
**Performance Goals**: N/A — No runtime performance targets for document artifacts.
**Constraints**: Must follow established skill format (YAML frontmatter + markdown body); must use `${SKILL_HOME}` / `${SKILL_WORKDIR}` path conventions; must not break existing skill resolution.
**Scale/Scope**: 3 new skills created, 9 draft skills removed, ~15 supporting files reorganized.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | This plan is driven by `017-consolidate-draft-skills/requirements.md` with 15 FRs and 6 SCs |
| II | Feature-Centric Development | ✅ Pass | Spec bound to Feature 013 (Skills Command); feature index updated with new spec path |
| III | Intent-Driven Development | ✅ Pass | Requirements specify "what" (3 consolidated skills) and "why" (reduce cognitive overhead); plan specifies "how" |
| IV | Test-First & Contract-Driven Implementation | ⚠ Partial — see Complexity Tracking | Skills are prompt artifacts, not executable code; validation is manual coverage comparison, not automated tests |
| V | AI Agent Integration Standards | ✅ Pass | Skills follow established format discoverable by all supported AI agents (Claude Code, Copilot, Qwen, opencode, Qoder) |
| VI | Continuous Quality & Observability | ✅ Pass | Skills use semantic structure; changes tracked in feature index and git history |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Following full SDD workflow: requirements → plan → tasks → implement |

**Gates Status**: ⚠ Principle IV partial — justified in Complexity Tracking below. All other gates pass.

**Re-check after Phase 1**: 2026-06-18 — Post-design check confirms no additional violations. The data model and contracts are structural (file layout and format specifications), not API/database schemas, consistent with the nature of prompt-artifact work.

## Project Structure

### Documentation (this spec)

```text
.specify/specs/017-consolidate-draft-skills/
├── plan.md              # This file
├── data-model.md        # Phase 1: skill directory layout and file structure model
├── quickstart.md        # Phase 1: step-by-step consolidation walkthrough
├── contracts/           # Phase 1: skill format specification contracts
│   └── skill-format.md  # YAML frontmatter and SKILL.md structural contract
├── checklists/
│   └── requirements.md  # Specification quality checklist
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
skills/document-utils/   # NEW: consolidated document skill (docx, pdf, pptx, xlsx, themes)
skills/database-utils/   # NEW: consolidated database skill (MySQL + PostgreSQL ecosystems)
skills/browser-utils/    # NEW: consolidated browser skill (automation + web testing)
draft/skills/            # MODIFIED: 9 subdirectories removed after consolidation
```

**Structure Decision**: Extends the existing `skills/` directory with 3 new skill packages. Each package follows the established pattern (SKILL.md + scripts/ + references/ subdirectories). The `draft/skills/` directory loses its 9 subdirectories. No new top-level directories are created.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Principle IV partial: no automated tests for skill content | Skills are prompt/document artifacts consumed by AI agents, not executable modules. There is no unit-testable interface — validation requires comparing SKILL.md content coverage against source drafts and verifying YAML frontmatter structure. | Automated tests would require parsing and semantically comparing markdown content, which adds fragile test infrastructure for document artifacts that are validated by human review and AI agent invocation. Manual verification checklist (SC-001 through SC-006) provides equivalent confidence. |

## Phase 0: Research Review

### Key Findings from Internal Analysis

1. **Shared `scripts/office/` directory**: docx-utils, pptx-utils, and xlsx-utils all contain identical `scripts/office/` subdirectories (soffice.py, pack.py, unpack.py, validate.py, helpers/, validators/). The consolidated document-utils skill needs only ONE copy.

2. **Format-specific scripts**: Each document skill has unique scripts beyond the shared office/ directory:
   - docx-utils: `accept_changes.py`, `comment.py`, `scripts/templates/` (XML templates)
   - pdf-utils: 8 PDF-specific scripts (form filling, field extraction, bounding boxes, image conversion)
   - pptx-utils: `add_slide.py`, `clean.py`, `thumbnail.py`
   - xlsx-utils: `recalc.py`

3. **Database skills have parallel structure**: Both mysql-utils and postgres-utils share the same interface pattern (`query.py --list/--tables/--schema/--query/--limit`). Consolidation means a single `query.py` that accepts a `--protocol` flag or auto-detects from connection config.

4. **Browser skills are complementary, not overlapping**: playwright-utils is JS-based (run.js wrapper, Node.js Playwright, API_REFERENCE.md) while web-test is Python-based (with_server.py, sync Playwright, examples/). No conflicting patterns — the SKILL.md can present both as language-specific sections.

5. **License handling**: docx-utils, pdf-utils, pptx-utils, xlsx-utils, and web-test share the same LICENSE.txt. theme-creator has a different license. mysql-utils and postgres-utils use Apache-2.0. Each consolidated skill should include appropriate license files.

6. **Path convention compliance**: Existing draft skills do NOT use `${SKILL_HOME}` / `${SKILL_WORKDIR}`. The formal skills must adopt these conventions per `templates/commands/skills.md`.

### Design Decisions

1. **document-utils SKILL.md structure**: A hub document with a Quick Reference table routing to format-specific sections. Each format (DOCX, PDF, PPTX, XLSX) gets its own `## Format` section. Theme capabilities get a cross-cutting `## Themes` section. Reference docs (forms.md, reference.md, editing.md, pptxgenjs.md) move to `references/`.

2. **database-utils unified config**: Add a `protocol` field to `connections.json` with values `"mysql"` or `"postgres"`. The query script dispatches to the appropriate driver based on this field. Backward-compatible: if `protocol` is absent, infer from port (3306→mysql, 5432→postgres).

3. **browser-utils dual-language sections**: SKILL.md organized as: Overview → Decision Tree → JavaScript Automation (from playwright-utils) → Python Testing (from web-test) → Common Patterns → Troubleshooting. Supporting files kept in their original language subdirectories.

4. **Shared office scripts deduplication**: The `scripts/office/` directory appears once in `document-utils/scripts/office/`. Format-specific scripts are placed alongside at `scripts/<format>/` (e.g., `scripts/docx/`, `scripts/pdf/`, `scripts/pptx/`, `scripts/xlsx/`).

---

## Phase 1 Design Artifacts

Generated as separate files:
- `data-model.md` — Skill directory layout and file structure
- `contracts/skill-format.md` — SKILL.md format contract
- `quickstart.md` — Step-by-step consolidation walkthrough
