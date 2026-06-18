# Tasks: Consolidate Draft Skills into Formal Skills

**Requirement ID**: 017 (from branch name)
**Requirement Key**: 017-consolidate-draft-skills
**Related Feature**: 013 Skills Command (from .specify/memory/features.md)
**Input**: Design documents from `.specify/specs/017-consolidate-draft-skills/`
**Prerequisites**: plan.md (required), requirements.md (required), data-model.md, contracts/skill-format.md, quickstart.md

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" uses MUST language). However, per the justified Complexity Tracking exception in plan.md, skills are prompt/document artifacts — validation is manual coverage comparison and YAML frontmatter checks, not automated unit tests. Test tasks below are verification/validation tasks.

**Organization**: Tasks are grouped by user story. US1–US3 are all P1 and can proceed in parallel since each creates an independent skill. US4 (P2) depends on US1–US3 completion.

## Definition of Done (DoD)

- DoD-1: All 3 formal skills created in skills/ with complete SKILL.md files conforming to contracts/skill-format.md
- DoD-2: All supporting files (scripts, references, themes, examples, configs) copied and organized per data-model.md
- DoD-3: YAML frontmatter validated for each skill (name, description with EN/CN triggers, skill_id)
- DoD-4: Path conventions (${SKILL_HOME}, ${SKILL_WORKDIR}) adopted in all SKILL.md files
- DoD-5: All 3 skills mirrored to .specify/skills/ with byte-equivalence
- DoD-6: All 9 draft skill directories removed from draft/skills/
- DoD-7: Feature 013 detail updated with key change note for this iteration
- DoD-8: Success criteria SC-001 through SC-006 verified

**DoD Status**: green

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- Includes exact file paths in descriptions

## Phase 1: Setup

**Purpose**: Create target directory structures for all 3 formal skills

- [X] T001 Create directory structure for skills/document-utils/ per data-model.md: scripts/{office,docx,pdf,pptx,xlsx}/, references/, themes/
- [X] T002 [P] Create directory structure for skills/database-utils/ per data-model.md: scripts/, references/
- [X] T003 [P] Create directory structure for skills/browser-utils/ per data-model.md: scripts/{js,python}/, references/, examples/

---

## Phase 2: User Story 1 - Document Utilities Skill (Priority: P1) 🎯 MVP

**Goal**: Consolidate docx-utils, pdf-utils, pptx-utils, theme-creator, and xlsx-utils into a single document-utils skill with format-specific sections and all supporting files.

**Independent Test**: Invoke document-utils for each format (create .docx, extract from .pdf, edit .pptx, build .xlsx, apply theme) and verify format-specific guidance is surfaced correctly.

### Supporting Files for US1

- [X] T004 [US1] Copy shared scripts/office/ from draft/skills/docx-utils/scripts/office/ to skills/document-utils/scripts/office/ (ONE copy — identical across docx/pptx/xlsx)
- [X] T005 [P] [US1] Copy docx-specific scripts from draft/skills/docx-utils/scripts/{accept_changes.py,comment.py,__init__.py,templates/} to skills/document-utils/scripts/docx/
- [X] T006 [P] [US1] Copy pdf-specific scripts from draft/skills/pdf-utils/scripts/*.py to skills/document-utils/scripts/pdf/
- [X] T007 [P] [US1] Copy pptx-specific scripts from draft/skills/pptx-utils/scripts/{add_slide.py,clean.py,__init__.py,thumbnail.py} to skills/document-utils/scripts/pptx/
- [X] T008 [P] [US1] Copy xlsx-specific script from draft/skills/xlsx-utils/scripts/recalc.py to skills/document-utils/scripts/xlsx/recalc.py
- [X] T009 [P] [US1] Copy reference docs: draft/skills/pdf-utils/{forms.md,reference.md} → skills/document-utils/references/{pdf-forms.md,pdf-reference.md}; draft/skills/pptx-utils/{editing.md,pptxgenjs.md} → skills/document-utils/references/{pptx-editing.md,pptx-creation.md}
- [X] T010 [P] [US1] Copy themes: draft/skills/theme-creator/{themes/,theme-showcase.pdf} → skills/document-utils/themes/
- [X] T011 [P] [US1] Copy LICENSE.txt from draft/skills/docx-utils/LICENSE.txt to skills/document-utils/LICENSE.txt

### SKILL.md Authoring for US1

- [X] T012 [US1] Write skills/document-utils/SKILL.md: YAML frontmatter (name: document-utils, description with EN/CN trigger keywords covering Word/docx/PDF/PowerPoint/pptx/Excel/xlsx/spreadsheet/presentation/slides/deck/theme/文档/表格/幻灯片/演示文稿/主题, skill_id), Overview, Quick Reference table
- [X] T013 [US1] Write DOCX section in skills/document-utils/SKILL.md: merge all content from draft/skills/docx-utils/SKILL.md (creation with docx-js, editing with XML unpack/edit/repack, reading, converting, tracked changes, comments, critical rules, dependencies). Update script paths to use ${SKILL_HOME}/scripts/office/ and ${SKILL_HOME}/scripts/docx/
- [X] T014 [US1] Write PDF section in skills/document-utils/SKILL.md: merge all content from draft/skills/pdf-utils/SKILL.md (reading, text/table extraction, PDF creation with reportlab, merging/splitting, rotation, watermarks, OCR, password protection, form filling reference). Update script paths to use ${SKILL_HOME}/scripts/pdf/. Reference ${SKILL_HOME}/references/pdf-forms.md and ${SKILL_HOME}/references/pdf-reference.md
- [X] T015 [US1] Write PPTX section in skills/document-utils/SKILL.md: merge all content from draft/skills/pptx-utils/SKILL.md (reading, editing workflow, creating from scratch, design ideas, color palettes, typography, QA process, converting to images, dependencies). Update script paths to use ${SKILL_HOME}/scripts/pptx/. Reference ${SKILL_HOME}/references/pptx-editing.md and ${SKILL_HOME}/references/pptx-creation.md
- [X] T016 [US1] Write XLSX section in skills/document-utils/SKILL.md: merge all content from draft/skills/xlsx-utils/SKILL.md (output requirements, financial model standards, reading/analyzing, creating/editing, formula rules, recalculation, verification checklist). Update script paths to use ${SKILL_HOME}/scripts/xlsx/
- [X] T017 [US1] Write Themes section in skills/document-utils/SKILL.md: merge all content from draft/skills/theme-creator/SKILL.md (10 pre-set themes, usage instructions, application process, custom theme creation). Reference ${SKILL_HOME}/themes/
- [X] T018 [US1] Add Path Conventions, Resources, and Dependencies sections to skills/document-utils/SKILL.md per contracts/skill-format.md C-002

### Verification for US1

- [X] T019 [US1] Verify document-utils: compare SKILL.md section headings and workflow coverage against all 5 source draft SKILL.md files (SC-001). Check YAML frontmatter (C-001). Confirm all scripts, references, and themes are present in the directory structure (FR-015). Validate ${SKILL_HOME} path usage (C-002)

**Checkpoint**: document-utils is fully functional and independently testable

---

## Phase 3: User Story 2 - Database Utilities Skill (Priority: P1)

**Goal**: Consolidate mysql-utils and postgres-utils into a single database-utils skill supporting MySQL and PostgreSQL protocol families, including ClickHouse and Apache Doris/SelectDB.

**Independent Test**: Configure connections for MySQL-protocol and PostgreSQL-protocol databases, run --list, --tables, --schema, --query against each, verify correct protocol routing and safety features.

### Supporting Files for US2

- [X] T020 [P] [US2] Copy draft/skills/mysql-utils/scripts/query.py to skills/database-utils/scripts/query_mysql.py
- [X] T021 [P] [US2] Copy draft/skills/postgres-utils/scripts/query.py to skills/database-utils/scripts/query_postgres.py
- [X] T022 [US2] Create unified skills/database-utils/scripts/query.py: dispatcher that reads protocol from connection config (or infers from port), imports and delegates to query_mysql.py or query_postgres.py. Preserve the same CLI interface (--list, --tables, --schema, --query, --db, --limit)
- [X] T023 [P] [US2] Create skills/database-utils/connections.example.json with protocol field: include MySQL example (protocol: "mysql", port: 3306), PostgreSQL example (protocol: "postgres", port: 5432), ClickHouse example (protocol: "postgres", port: 9005), Apache Doris example (protocol: "mysql", port: 9030)
- [X] T024 [P] [US2] Create skills/database-utils/requirements.txt combining mysql-connector-python and psycopg2-binary
- [X] T025 [P] [US2] Copy .gitignore from draft/skills/mysql-utils/.gitignore to skills/database-utils/.gitignore
- [X] T026 [P] [US2] Create skills/database-utils/references/README.md merging setup and usage guides from draft/skills/mysql-utils/README.md and draft/skills/postgres-utils/README.md
- [X] T027 [P] [US2] Create skills/database-utils/LICENSE.txt with Apache-2.0 license text (same as source skills)

### SKILL.md Authoring for US2

- [X] T028 [US2] Write skills/database-utils/SKILL.md: YAML frontmatter (name: database-utils, description with EN/CN trigger keywords covering MySQL/PostgreSQL/database/SQL/query/ClickHouse/Doris/SelectDB/数据库/查询, skill_id), Overview, Quick Reference table with supported databases
- [X] T029 [US2] Write Setup, Usage, Database Selection, Supported Databases sections in skills/database-utils/SKILL.md: merge content from both source SKILL.md files. Add protocol field documentation. Include supported databases table (MySQL, PostgreSQL, ClickHouse, Doris/SelectDB with protocols and ports). Update script paths to use ${SKILL_HOME}/scripts/
- [X] T030 [US2] Write Safety Features and Troubleshooting sections in skills/database-utils/SKILL.md: merge safety features from both sources (read-only sessions, query validation, single-statement enforcement, timeout, row limits, column width caps, credential sanitization). Combine troubleshooting tables
- [X] T031 [US2] Add Path Conventions, Resources, and Dependencies sections to skills/database-utils/SKILL.md per contracts/skill-format.md C-002

### Verification for US2

- [X] T032 [US2] Verify database-utils: validate YAML frontmatter (C-001). Check unified connections.example.json has all 4 database types (FR-005). Verify query.py dispatcher logic handles both protocols (FR-006). Confirm all safety features documented (FR-007, SC-002). Validate ${SKILL_HOME} path usage

**Checkpoint**: database-utils is fully functional and independently testable

---

## Phase 4: User Story 3 - Browser Utilities Skill (Priority: P1)

**Goal**: Consolidate playwright-utils and web-test into a single browser-utils skill covering both JavaScript browser automation and Python web application testing with server lifecycle management.

**Independent Test**: Run a screenshot task through JS automation and a server-lifecycle test through Python testing, verify both patterns are documented and supporting files present.

### Supporting Files for US3

- [X] T033 [P] [US3] Copy draft/skills/playwright-utils/{run.js,package.json} to skills/browser-utils/scripts/js/
- [X] T034 [P] [US3] Copy draft/skills/web-test/scripts/with_server.py to skills/browser-utils/scripts/python/with_server.py
- [X] T035 [P] [US3] Copy draft/skills/playwright-utils/API_REFERENCE.md to skills/browser-utils/references/playwright-api.md
- [X] T036 [P] [US3] Copy draft/skills/web-test/examples/{console_logging.py,element_discovery.py,static_html_automation.py} to skills/browser-utils/examples/
- [X] T037 [P] [US3] Copy draft/skills/web-test/LICENSE.txt to skills/browser-utils/LICENSE.txt

### SKILL.md Authoring for US3

- [X] T038 [US3] Write skills/browser-utils/SKILL.md: YAML frontmatter (name: browser-utils, description with EN/CN trigger keywords covering browser/Playwright/web test/screenshot/automation/responsive/浏览器/网页测试/截图/自动化, skill_id), Overview, Decision Tree (choosing between JS and Python approaches)
- [X] T039 [US3] Write JavaScript Automation section in skills/browser-utils/SKILL.md: merge content from draft/skills/playwright-utils/SKILL.md (setup, dev server detection, script execution via run.js, common patterns — responsive testing, login flows, form filling, link checking, screenshots, custom HTTP headers, helper utilities, inline execution). Update paths to use ${SKILL_HOME}/scripts/js/
- [X] T040 [US3] Write Python Testing section in skills/browser-utils/SKILL.md: merge content from draft/skills/web-test/SKILL.md (with_server.py usage, single/multi-server setup, reconnaissance-then-action pattern, sync_playwright API, best practices). Update paths to use ${SKILL_HOME}/scripts/python/. Reference ${SKILL_HOME}/examples/
- [X] T041 [US3] Write Common Patterns, Troubleshooting sections and add Path Conventions, Resources, Dependencies sections to skills/browser-utils/SKILL.md per contracts/skill-format.md C-002. Reference ${SKILL_HOME}/references/playwright-api.md

### Verification for US3

- [X] T042 [US3] Verify browser-utils: validate YAML frontmatter (C-001). Confirm both JS and Python patterns are documented (FR-009). Check server lifecycle management present (FR-010). Verify dev server detection and run.js references (FR-011). Validate all supporting files present (SC-003)

**Checkpoint**: browser-utils is fully functional and independently testable

---

## Phase 5: User Story 4 - Remove Draft Skills (Priority: P2)

**Goal**: Remove all 9 original draft skill directories from draft/skills/ after successful consolidation.

**Independent Test**: Verify draft/skills/ contains none of the 9 original skill subdirectories.

- [X] T043 [US4] Remove 9 draft skill directories: draft/skills/{docx-utils,pdf-utils,pptx-utils,theme-creator,xlsx-utils,mysql-utils,postgres-utils,playwright-utils,web-test}
- [X] T044 [US4] Verify draft/skills/ is empty or contains no skill-related content (SC-004)

**Checkpoint**: Draft skills removed, no duplicate skill content exists

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Mirror skills, update feature tracking, final validation

- [X] T045 [P] Mirror skills/document-utils/ to .specify/skills/document-utils/ (full directory copy)
- [X] T046 [P] Mirror skills/database-utils/ to .specify/skills/database-utils/ (full directory copy)
- [X] T047 [P] Mirror skills/browser-utils/ to .specify/skills/browser-utils/ (full directory copy)
- [X] T048 Verify byte-equivalence between skills/<name>/ and .specify/skills/<name>/ for all 3 skills (C-006)
- [X] T049 Update .specify/memory/features/013.md: add key change note for 017-consolidate-draft-skills iteration
- [X] T050 Final validation: verify all success criteria SC-001 through SC-006 pass — document-utils covers all 5 source skills, database-utils handles both protocols, browser-utils covers both JS and Python, drafts removed, format compliant, 3 new skills in skills/

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **US1 (Phase 2)**: Depends on T001 (document-utils directory creation)
- **US2 (Phase 3)**: Depends on T002 (database-utils directory creation) — can run in parallel with US1
- **US3 (Phase 4)**: Depends on T003 (browser-utils directory creation) — can run in parallel with US1 and US2
- **US4 (Phase 5)**: Depends on US1, US2, and US3 completion (T019, T032, T042 all done)
- **Polish (Phase 6)**: Depends on US4 completion (T044 done)

### User Story Dependencies

- **User Story 1 (P1)**: Can start after T001 — No dependencies on other stories
- **User Story 2 (P1)**: Can start after T002 — No dependencies on other stories
- **User Story 3 (P1)**: Can start after T003 — No dependencies on other stories
- **User Story 4 (P2)**: Depends on US1 + US2 + US3 all verified (T019, T032, T042)

### Within Each User Story

- Copy supporting files BEFORE writing SKILL.md (need to know exact file layout)
- Parallel file copies within a story (different source/target directories)
- SKILL.md authoring is sequential (single file, sections build on each other)
- Verification AFTER all files and SKILL.md are complete

### Parallel Opportunities

- All 3 setup tasks (T001, T002, T003) can run in parallel
- US1, US2, US3 can all run in parallel (independent skills, different directories)
- Within each story: all file-copy tasks marked [P] can run in parallel
- All 3 mirror tasks (T045, T046, T047) can run in parallel

---

## Parallel Example: All User Stories

```text
# After setup, launch all 3 skills in parallel:
Stream A (US1): T004–T019 (document-utils)
Stream B (US2): T020–T032 (database-utils)
Stream C (US3): T033–T042 (browser-utils)

# Within US1, launch file copies in parallel:
T005, T006, T007, T008, T009, T010, T011 (all [P], different source/target dirs)

# After all 3 verified, proceed to cleanup and polish:
T043–T050 (sequential)
```

---

## Implementation Strategy

### MVP First (Any Single User Story)

1. Complete Phase 1: Setup (T001–T003)
2. Complete Phase 2: User Story 1 — document-utils (T004–T019)
3. **STOP and VALIDATE**: Test document-utils independently with each format
4. Proceed to remaining stories

### Parallel Delivery (Recommended)

1. Complete Setup (T001–T003)
2. Launch US1, US2, US3 in parallel — each creates an independent skill
3. After all 3 verified → US4: Remove drafts (T043–T044)
4. Polish: Mirror + final validation (T045–T050)

### Incremental Delivery

1. Setup → US1 (document-utils) → Validate → Demo
2. US2 (database-utils) → Validate → Demo
3. US3 (browser-utils) → Validate → Demo
4. US4 (cleanup) → Polish → Done

---

## Notes

- [P] tasks = different files/directories, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story (US1, US2, US3) is independently completable and testable
- US4 depends on all 3 other stories
- All SKILL.md authoring tasks involve reading source draft SKILL.md and merging content — not copying verbatim
- Script path references in SKILL.md must be updated from relative paths to ${SKILL_HOME}/ convention
- Mirror to .specify/skills/ must include ALL files (SKILL.md + supporting directories)
