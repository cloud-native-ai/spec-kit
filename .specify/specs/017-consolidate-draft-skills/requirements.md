# Feature Specification: Consolidate Draft Skills into Formal Skills

**Feature Branch**: `017-consolidate-draft-skills`  
**Created**: 2026-06-18  
**Status**: Draft  
**Input**: User description: "Consolidate 9 draft skills from draft/skills/ into 3 formal skills (document-utils, database-utils, browser-utils) and remove the drafts."

## Related Feature

**Feature ID**: 013  
**Feature Name**: Skills Command

## User Scenarios & Testing

### User Story 1 - Create and Use Document Utilities Skill (Priority: P1)

A user wants to create, edit, or analyze office documents (Word, PDF, PowerPoint, Excel) using a single unified skill rather than switching between separate skills for each document format. The user also wants to apply professional visual themes to any document type.

**Why this priority**: Document operations cover 5 of the 9 draft skills (docx-utils, pdf-utils, pptx-utils, theme-creator, xlsx-utils), making this the largest consolidation. A unified entry point reduces cognitive overhead for both users and AI agents.

**Independent Test**: Can be fully tested by invoking the document-utils skill for each supported format (create a .docx, extract text from a .pdf, edit a .pptx, build an .xlsx, apply a theme) and verifying that format-specific guidance, scripts, and workflows are correctly surfaced.

**Acceptance Scenarios**:

1. **Given** a user asks to create a Word document, **When** the document-utils skill is invoked, **Then** the skill provides docx-specific creation guidance including docx-js patterns, validation scripts, and XML editing workflows.
2. **Given** a user asks to extract tables from a PDF, **When** the document-utils skill is invoked, **Then** the skill provides PDF-specific extraction guidance using pdfplumber and pypdf.
3. **Given** a user asks to build a slide deck, **When** the document-utils skill is invoked, **Then** the skill provides PPTX-specific guidance including pptxgenjs creation, editing workflows, and visual QA processes.
4. **Given** a user asks to create a financial model in Excel, **When** the document-utils skill is invoked, **Then** the skill provides XLSX-specific guidance including formula construction rules, openpyxl patterns, and recalculation workflows.
5. **Given** a user asks to apply a visual theme to a document, **When** the document-utils skill is invoked, **Then** the skill provides theme selection (10 pre-set themes) and application guidance, or custom theme creation.

---

### User Story 2 - Create and Use Database Utilities Skill (Priority: P1)

A user wants to query and explore databases across both MySQL and PostgreSQL protocol ecosystems using a single unified skill. This includes MySQL-native databases, Apache Doris/SelectDB (MySQL protocol), PostgreSQL-native databases, and ClickHouse (PostgreSQL wire protocol).

**Why this priority**: Database access is a core operational need. Unifying the two protocol-based skills into one eliminates the need for users to know which protocol a specific database uses; the skill routes based on connection configuration.

**Independent Test**: Can be fully tested by configuring connections to MySQL-protocol and PostgreSQL-protocol databases, then running list, schema, tables, and query operations against each, verifying correct protocol routing and safety enforcement.

**Acceptance Scenarios**:

1. **Given** a user wants to query a MySQL database, **When** the database-utils skill is invoked, **Then** the skill uses the MySQL protocol driver to execute read-only queries with all safety features (read-only session, query validation, timeout, row limits).
2. **Given** a user wants to query a PostgreSQL database, **When** the database-utils skill is invoked, **Then** the skill uses the PostgreSQL protocol driver to execute read-only queries with all safety features.
3. **Given** a user wants to query a ClickHouse database via its PostgreSQL wire protocol, **When** the database-utils skill is invoked with a ClickHouse connection configured as PostgreSQL-protocol, **Then** the skill routes the query through the PostgreSQL driver and returns results correctly.
4. **Given** a user wants to query an Apache Doris/SelectDB database via its MySQL protocol, **When** the database-utils skill is invoked with a Doris/SelectDB connection configured as MySQL-protocol, **Then** the skill routes the query through the MySQL driver and returns results correctly.
5. **Given** a user lists configured databases, **When** the skill shows available connections, **Then** each connection displays its name, description, protocol type (MySQL or PostgreSQL), and target database system.

---

### User Story 3 - Create and Use Browser Utilities Skill (Priority: P1)

A user wants to automate browser interactions, test web applications, take screenshots, and validate UI behavior using a single unified skill that combines rich browser automation and web application testing with server lifecycle management.

**Why this priority**: Browser automation and web testing are closely related capabilities that users need together. Merging playwright-utils (JS-focused, feature-rich automation) with web-test (Python-focused, server lifecycle management) provides comprehensive coverage.

**Independent Test**: Can be fully tested by running browser automation tasks (screenshot, form fill, responsive test) and web testing tasks (server lifecycle, DOM inspection, console logging) through the unified skill.

**Acceptance Scenarios**:

1. **Given** a user wants to test a running web application, **When** the browser-utils skill is invoked, **Then** the skill auto-detects running dev servers and provides automation capabilities for the detected URLs.
2. **Given** a user wants to test a web application that is not yet running, **When** the browser-utils skill is invoked, **Then** the skill provides server lifecycle management to start the server, wait for readiness, execute tests, and clean up.
3. **Given** a user wants to take responsive screenshots across viewports, **When** the browser-utils skill is invoked, **Then** the skill provides multi-viewport screenshot capabilities (desktop, tablet, mobile).
4. **Given** a user wants to automate a login flow, **When** the browser-utils skill is invoked, **Then** the skill provides form-filling, navigation, and assertion patterns for end-to-end flow testing.

---

### User Story 4 - Remove Draft Skills After Consolidation (Priority: P2)

After the three formal skills are created and validated, the original 9 draft skill directories in draft/skills/ must be removed to avoid confusion and duplication.

**Why this priority**: Cleanup depends on successful creation of the formal skills and prevents users or AI agents from referencing outdated draft versions.

**Independent Test**: Can be tested by verifying that the draft/skills/ directory no longer contains the 9 original skill subdirectories after consolidation is complete.

**Acceptance Scenarios**:

1. **Given** all three formal skills (document-utils, database-utils, browser-utils) have been created and validated, **When** the consolidation process completes, **Then** the following directories are removed from draft/skills/: docx-utils, pdf-utils, pptx-utils, theme-creator, xlsx-utils, mysql-utils, postgres-utils, playwright-utils, web-test.
2. **Given** the draft skills are removed, **When** a user or AI agent searches for skill files, **Then** only the formal skills in skills/ are discoverable.

---

### Edge Cases

- What happens when a user query spans multiple document formats (e.g., "convert this Word doc to PDF")? The document-utils skill must handle cross-format workflows within a single invocation.
- How does the database-utils skill handle a connection configured with the wrong protocol for the target database? The skill must surface clear error messages from the underlying driver without masking the protocol mismatch.
- What happens when both JavaScript and Python Playwright environments are available for browser-utils? The skill must provide guidance for both approaches and let the user or context determine which to use.
- How does the database-utils skill handle databases that support multiple protocols (e.g., ClickHouse supports both native and PostgreSQL)? The connection configuration determines the protocol; the skill does not auto-detect.

## Requirements

### Functional Requirements

- **FR-001**: The system MUST create a `document-utils` skill that consolidates the capabilities of docx-utils, pdf-utils, pptx-utils, theme-creator, and xlsx-utils into a single skill with format-specific sections.
- **FR-002**: The `document-utils` skill MUST preserve all format-specific guidance, scripts, dependencies, and workflow patterns from each source draft skill without loss of functionality.
- **FR-003**: The `document-utils` skill MUST include theme creation and application capabilities from theme-creator as a cross-cutting concern applicable to all document types.
- **FR-004**: The system MUST create a `database-utils` skill that consolidates mysql-utils and postgres-utils into a single skill supporting both MySQL and PostgreSQL protocol families.
- **FR-005**: The `database-utils` skill MUST document support for the following database systems: MySQL (MySQL protocol), PostgreSQL (PostgreSQL protocol), ClickHouse (PostgreSQL wire protocol), Apache Doris/SelectDB (MySQL protocol).
- **FR-006**: The `database-utils` skill MUST use a unified connection configuration format that includes a protocol indicator to distinguish MySQL-protocol from PostgreSQL-protocol connections.
- **FR-007**: The `database-utils` skill MUST preserve all safety features from both source skills: read-only sessions, query validation, single-statement enforcement, query timeout, row limits, column width caps, and credential sanitization.
- **FR-008**: The system MUST create a `browser-utils` skill that consolidates playwright-utils and web-test into a single skill covering both browser automation and web application testing.
- **FR-009**: The `browser-utils` skill MUST support both JavaScript (Node.js Playwright) and Python (Playwright sync API) execution patterns.
- **FR-010**: The `browser-utils` skill MUST include server lifecycle management (starting, readying, and stopping dev servers) from the web-test skill.
- **FR-011**: The `browser-utils` skill MUST include dev server auto-detection, custom HTTP headers, helper utilities, and the run.js execution wrapper from playwright-utils.
- **FR-012**: All three formal skills MUST follow the established Spec Kit skill format (YAML frontmatter with name, description; markdown body with structured sections).
- **FR-013**: After successful creation of all three formal skills, the system MUST remove the 9 original draft skill directories from draft/skills/.
- **FR-014**: Each formal skill's YAML `description` field MUST include trigger keywords in both English and Chinese to match the existing skill convention.
- **FR-015**: Each formal skill MUST include all supporting files (scripts, reference docs, configuration examples, license files) from its constituent draft skills, organized under the skill's directory.

### Key Entities

- **Skill**: A self-contained capability package with a SKILL.md definition file, optional scripts, references, and configuration files, installed under skills/ and mirrored to .specify/skills/.
- **Draft Skill**: A preliminary skill definition stored in draft/skills/ that has not yet been promoted to a formal skill.
- **Connection Configuration**: A JSON structure defining database access parameters including host, port, credentials, SSL settings, and protocol type (MySQL or PostgreSQL).
- **Document Format**: One of the supported office document types (docx, pdf, pptx, xlsx) each with format-specific creation, editing, and analysis workflows.

## Success Criteria

### Measurable Outcomes

- **SC-001**: All document-related operations previously available across 5 separate draft skills are accessible through the single document-utils skill with no loss of guidance quality or supported workflows.
- **SC-002**: Users can query MySQL-protocol databases (MySQL, Apache Doris/SelectDB) and PostgreSQL-protocol databases (PostgreSQL, ClickHouse) through the single database-utils skill using the same command interface.
- **SC-003**: Browser automation tasks (screenshots, form filling, responsive testing) and web application testing tasks (server lifecycle, DOM inspection) are available through the single browser-utils skill.
- **SC-004**: The 9 original draft skill directories are removed from draft/skills/ after consolidation, reducing draft skill count from 9 to 0.
- **SC-005**: Each formal skill follows the established Spec Kit skill format and is discoverable by AI agents through standard skill resolution mechanisms.
- **SC-006**: The skills/ directory gains 3 new formal skills (document-utils, database-utils, browser-utils) after consolidation.

### Measurement Sources & Collection Methods

- **SC-001 Source**: Manual verification by comparing the table of contents and workflow coverage of the new document-utils SKILL.md against the combined content of the 5 source draft skills. Every section heading and script reference in the source skills must have a corresponding entry in the consolidated skill.
- **SC-002 Source**: Functional test with connections.json entries for MySQL and PostgreSQL protocol databases; run --list, --tables, --schema, and --query against each to verify correct routing.
- **SC-003 Source**: Functional test executing a screenshot task and a server-lifecycle test through the browser-utils skill; verify both JS and Python patterns are documented.
- **SC-004 Source**: File system inspection: `ls draft/skills/` returns empty or the directory is removed entirely.
- **SC-005 Source**: YAML frontmatter validation: each SKILL.md has name, description fields; markdown body follows established section conventions. AI agent can discover and invoke the skill.
- **SC-006 Source**: File system inspection: `ls skills/` includes document-utils, database-utils, browser-utils directories each containing SKILL.md.

## Assumptions

- The draft skills in draft/skills/ contain the complete and current versions of their respective SKILL.md files and supporting assets.
- The established Spec Kit skill format (as exemplified by existing skills like draw-d3js, create-skills) is the target format for the new formal skills.
- Supporting files (scripts/, references/, configuration examples) from draft skills will be copied into the formal skill directories with appropriate organization.
- The database-utils skill inherits the read-only safety model from both source skills; no write capabilities will be added.
- ClickHouse's PostgreSQL wire protocol compatibility and Apache Doris/SelectDB's MySQL protocol compatibility are mature enough for production read-only query use cases.
- The browser-utils skill does not require reconciling conflicting patterns between playwright-utils and web-test; both are complementary (JS-focused automation vs. Python-focused testing with server management).

## Clarifications

### Session 2026-06-18

- Q: Which existing Feature should this spec be bound to? → A: Feature 013 — Skills Command ("Manage extensible skills/tools"). This spec is a natural iteration of the same feature that covers skill creation, installation layout, and portability.
