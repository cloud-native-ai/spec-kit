# Requirements Specification: Speckit Todo Command

**Requirement Branch**: `020-speckit-todo-command`  
**Created**: 2026-06-22  
**Status**: Draft  
**Input**: User description: "创建一个新的命令/speckit.todo 这个命令用来搜索文本文件中的所有特殊的TODO标记，暂定“```SPECKIT TODO ```”, 这个命令调用一个search-todo.sh脚本，这个脚本扫描所有的文本文件，提取其中的SPECKIT TODO文本块，这是个多行文本块， 然后将文本块结合当前文本文件上下文作为prompt，生成todo plan进行执行"

## Related Feature *(mandatory)*

<!--
  ACTION REQUIRED: Keep the default values as "Need clarification" in the initial draft.
  /speckit.clarify must resolve this section to the final Feature binding before planning.
-->

**Feature ID**: 025  
**Feature Name**: Todo Command

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Collect TODO markers (Priority: P1)

A Spec Kit user runs the todo command without arguments and receives a consolidated list of every marked TODO block found in text files, with enough source context to understand what each block refers to.

**Why this priority**: Discovery is the core value of the command; without reliable extraction, users cannot understand what work needs to be done.

**Independent Test**: Add marked TODO blocks to multiple text files, run the command, and verify that each block appears exactly once with its originating file and surrounding context.

**Acceptance Scenarios**:

1. **Given** a workspace containing multiple text files with marked TODO blocks, **When** the user runs `/speckit.todo` without arguments, **Then** the command reports every block with the source file, block text, and contextual excerpt.
2. **Given** a workspace containing ordinary TODO comments that are not inside the special marker block, **When** the user runs `/speckit.todo`, **Then** those ordinary comments are ignored.
3. **Given** a workspace with binary, dependency, generated, or ignored files, **When** the user runs `/speckit.todo`, **Then** those files are excluded from TODO extraction.

---

### User Story 2 - Insert TODO at specified location (Priority: P1)

A Spec Kit user provides a description argument to the todo command, specifying where and what TODO content should be inserted into a file.

**Why this priority**: This is the primary action of the command - creating well-formed TODO blocks that conform to the project's TODO marker specification.

**Independent Test**: Run the command with a description pointing to a specific file and providing TODO content, then verify that a conforming SPECKIT TODO block is inserted at the specified location.

**Acceptance Scenarios**:

1. **Given** a user runs `/speckit.todo` with a description specifying a target file and TODO content, **When** the command executes, **Then** a conforming SPECKIT TODO block is inserted at the specified location in the file.
2. **Given** the target file exists, **When** the TODO is inserted, **Then** the block uses the correct marker format (triple backticks with SPECKIT TODO) and preserves any surrounding context.
3. **Given** the target file does not exist, **When** the user attempts to insert a TODO, **Then** the command reports an error and does not create the file.

---

### User Story 3 - Handle scan and insertion safely (Priority: P2)

A Spec Kit user needs predictable behavior when no TODO blocks are present during collection, markers are malformed, or insertion targets are invalid.

**Why this priority**: Safe handling prevents noisy output, accidental overreach, and confusing failures.

**Independent Test**: Run the command against empty, malformed, and invalid targets and verify that the command gives clear status messages.

**Acceptance Scenarios**:

1. **Given** no marked TODO blocks exist in eligible files, **When** the user runs `/speckit.todo` without arguments, **Then** the command reports that no actionable blocks were found.
2. **Given** a marked TODO block has no closing delimiter, **When** the user runs `/speckit.todo`, **Then** the command reports the file and approximate location of the malformed block.
3. **Given** the insertion target file does not exist or is not writable, **When** the user attempts to insert a TODO, **Then** the command reports the error and does not modify any files.

### Edge Cases

- Marked blocks may appear more than once in the same file and MUST retain their file order.
- Marked blocks may contain backticks, quotes, non-English text, or multiline instructions and MUST preserve their original text.
- A TODO block may sit near headings, comments, or code; the captured context MUST be sufficient to identify the user intent without including excessive unrelated content.
- Files may be renamed or changed while the command is running; the command MUST either use a consistent scan snapshot or report that the affected item should be retried.
- The command MUST avoid automatically acting on TODO content that appears to request destructive, secret-exposing, or out-of-scope operations.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a user-invocable `/speckit.todo` command that operates in two modes: collection mode (no arguments) and insertion mode (with description argument).
- **FR-002**: In collection mode (no arguments), the command MUST use the repository-provided TODO search script identified by `[[STR-003]]` to discover all marked TODO blocks in eligible text files.
- **FR-003**: The search behavior in collection mode MUST scan eligible text files in the workspace and exclude binary files, dependency directories, generated outputs, and files ignored by normal project ignore rules.
- **FR-004**: The marker format MUST identify fenced multiline blocks whose opening fence contains the marker string `[[STR-002]]` (anywhere on the opening fence line) and whose content continues until the next matching closing fence.
- **FR-005**: In collection mode, for each valid marked block, the system MUST capture the source file path, block order within the file, exact block content, and nearby contextual text bounded by the nearest blank lines or section headings above and below the block (paragraph-boundary context).
- **FR-006**: The command MUST ignore unmarked TODO comments and TODO-like text outside the special marker block format.
- **FR-007**: In collection mode, the command MUST report malformed marker blocks with source location context.
- **FR-008**: In insertion mode (with description argument), the command MUST parse the description to identify the target file, insertion location, and TODO content to insert.
- **FR-009**: In insertion mode, the command MUST verify that the target file exists and is writable before attempting insertion; if the file does not exist, the command MUST report an error and MUST NOT create the file.
- **FR-010**: In insertion mode, the command MUST insert a conforming SPECKIT TODO block at the specified location using the format specified in FR-004.
- **FR-011**: In insertion mode, the command MUST preserve surrounding file content and MUST NOT modify any content other than inserting the new TODO block.
- **FR-012**: In collection mode, the command MUST provide a clear no-op result when no valid marked TODO blocks are found.
- **FR-013**: When more than 10 valid TODO blocks are discovered in a single scan, the command MUST split the resulting groups into batches of at most 5 groups per batch and present each batch sequentially for review and confirmation before execution.

### Key Entities

- **TODO Marker Block**: A fenced multiline TODO section embedded in an eligible text file, including delimiter, content, order, and source location.
- **Source Context**: Nearby file information that helps interpret a TODO block, such as file path, surrounding headings, adjacent lines, and relevant section boundaries.
- **Todo Plan**: A reviewable set of ordered work groups derived from one or more TODO marker blocks, including intended outcomes, source references, risk notes, and validation expectations.
- **Execution Batch**: A bounded subset of the todo plan that can be reviewed and executed safely without mixing unrelated or conflicting work.

### Assumptions

- The provisional marker is a fenced block whose opening fence line contains the string `SPECKIT TODO` (anywhere on that line), and the block ends at the next matching closing triple-backtick fence. The exact position of the marker string on the opening fence line is not prescribed.
- Contextual text for each block extends upward to the nearest blank line or section heading and downward to the next blank line or section heading (paragraph-boundary).
- The command operates on the current workspace by default.
- “Text files” means files that can be safely read as text after honoring project ignore rules and common generated/dependency exclusions.
- Execution follows existing Spec Kit agent safety expectations: reviewable plans first, bounded changes, and validation evidence after changes.
- When more than 10 valid TODO blocks are found, the command splits them into batches of at most 5 blocks each and presents them one batch at a time.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In a workspace fixture with 25 valid marked TODO blocks across at least 10 text files, the command identifies 100% of valid blocks and reports zero duplicate blocks.
- **SC-002**: In a workspace fixture containing ordinary TODO comments, binary files, ignored files, and generated outputs, 100% of ineligible TODO-like content is excluded from the generated plan.
- **SC-003**: For each extracted block, users can trace the generated plan item back to its source file and context in under 10 seconds during review.
- **SC-004**: For malformed marker fixtures, the command reports every malformed block location and excludes 100% of malformed content from automatic execution planning.
- **SC-005**: At least 90% of users reviewing a generated plan for a representative fixture can correctly identify the next safe action without opening the original source files.

### Measurement Sources & Collection Methods

- **SC-001 Source**: Curated workspace fixtures with known valid block counts; compare command output against the expected block inventory on every validation run.
- **SC-002 Source**: Negative-case workspace fixtures; compare excluded files and comments against the expected ignore inventory on every validation run.
- **SC-003 Source**: Reviewer task timing during acceptance review; record time from plan item selection to source/context identification.
- **SC-004 Source**: Malformed-marker fixtures; compare reported malformed locations and excluded items against expected results.
- **SC-005 Source**: User review exercise or stakeholder acceptance session; aggregate correct next-action identification rates across representative TODO plans.

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `/speckit.todo` | FR-001, user documentation, command template, acceptance tests |
| `STR-002` | `SPECKIT TODO` | FR-004, search behavior, fixtures, acceptance tests |
| `STR-003` | `search-todo.sh` | FR-002, command template, script lookup tests |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

### Session 2026-06-23

- Q: Which Feature should this specification bind to? → A: Feature 025 "Todo Command"
- Q: Exact marker format parsing rules? → A: Loose mode — match any fenced block whose opening fence line contains `SPECKIT TODO`
- Q: How much surrounding context should be captured per TODO block? → A: Paragraph-boundary — upward to nearest blank line/heading, downward to next blank line/heading
- Q: Should the command only generate a plan, or also execute it? → A: Generate plan, present for review, then auto-execute after user confirmation
- Q: What threshold triggers batching of TODO blocks? → A: More than 10 blocks triggers batching; max 5 blocks per batch
