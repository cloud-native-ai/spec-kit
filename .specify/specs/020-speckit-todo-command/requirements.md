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

### User Story 1 - Discover actionable TODO blocks (Priority: P1)

A Spec Kit user runs the todo command in a workspace and receives a consolidated list of every marked TODO block found in text files, with enough source context to understand what each block refers to.

**Why this priority**: Discovery is the core value of the command; without reliable extraction, no later planning or execution can be trusted.

**Independent Test**: Add marked TODO blocks to multiple text files, run the command, and verify that each block appears exactly once with its originating file and surrounding context.

**Acceptance Scenarios**:

1. **Given** a workspace containing multiple text files with marked TODO blocks, **When** the user runs `/speckit.todo`, **Then** the command reports every block with the source file, block text, and contextual excerpt.
2. **Given** a workspace containing ordinary TODO comments that are not inside the special marker block, **When** the user runs `/speckit.todo`, **Then** those ordinary comments are ignored.
3. **Given** a workspace with binary, dependency, generated, or ignored files, **When** the user runs `/speckit.todo`, **Then** those files are excluded from TODO extraction.

---

### User Story 2 - Generate an execution-ready todo plan (Priority: P2)

A Spec Kit user wants the extracted TODO blocks to be transformed into a clear plan that can be reviewed and then carried out through the normal agent workflow.

**Why this priority**: The feature is intended to turn embedded project notes into actionable work, not only search results.

**Independent Test**: Create a TODO block that describes a specific change, run the command, and verify that the produced plan contains ordered tasks, affected context, validation expectations, and execution boundaries.

**Acceptance Scenarios**:

1. **Given** one or more extracted TODO blocks with source context, **When** the command prepares the prompt for the agent, **Then** the resulting plan groups related TODOs, preserves source references, and states what will be changed or verified.
2. **Given** multiple TODO blocks that reference the same file or topic, **When** the plan is generated, **Then** related work is consolidated to avoid duplicate or conflicting execution steps.
3. **Given** a TODO block with insufficient context to choose a safe action, **When** the plan is generated, **Then** the plan marks that item for human review instead of silently guessing a risky change.

---

### User Story 3 - Handle scan outcomes safely (Priority: P3)

A Spec Kit user needs predictable behavior when no TODO blocks are present, markers are malformed, or planned work could exceed the current command scope.

**Why this priority**: Safe handling prevents noisy output, accidental overreach, and confusing failures.

**Independent Test**: Run the command against empty, malformed, and oversized TODO examples and verify that the command gives clear status messages and bounded next steps.

**Acceptance Scenarios**:

1. **Given** no marked TODO blocks exist in eligible files, **When** the user runs `/speckit.todo`, **Then** the command reports that no actionable blocks were found and performs no planning work.
2. **Given** a marked TODO block has no closing delimiter, **When** the user runs `/speckit.todo`, **Then** the command reports the file and approximate location of the malformed block and excludes it from automatic execution planning.
3. **Given** the extracted TODO set is too large for one safe execution pass, **When** the plan is generated, **Then** the command divides work into reviewable batches and starts with the highest-priority safe batch.

### Edge Cases

- Marked blocks may appear more than once in the same file and MUST retain their file order.
- Marked blocks may contain backticks, quotes, non-English text, or multiline instructions and MUST preserve their original text.
- A TODO block may sit near headings, comments, or code; the captured context MUST be sufficient to identify the user intent without including excessive unrelated content.
- Files may be renamed or changed while the command is running; the command MUST either use a consistent scan snapshot or report that the affected item should be retried.
- The command MUST avoid automatically acting on TODO content that appears to request destructive, secret-exposing, or out-of-scope operations.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a user-invocable `/speckit.todo` command that initiates TODO discovery and planning for the current workspace.
- **FR-002**: The command MUST use the repository-provided TODO search script identified by `[[STR-003]]` as the discovery source for marked blocks.
- **FR-003**: The search behavior MUST scan eligible text files in the workspace and exclude binary files, dependency directories, generated outputs, and files ignored by normal project ignore rules.
- **FR-004**: The marker format MUST identify fenced multiline blocks whose opening fence contains the marker string `[[STR-002]]` (anywhere on the opening fence line) and whose content continues until the next matching closing fence.
- **FR-005**: For each valid marked block, the system MUST capture the source file path, block order within the file, exact block content, and nearby contextual text bounded by the nearest blank lines or section headings above and below the block (paragraph-boundary context).
- **FR-006**: The command MUST ignore unmarked TODO comments and TODO-like text outside the special marker block format.
- **FR-007**: The command MUST report malformed marker blocks with source location context and MUST exclude malformed blocks from automatic execution planning.
- **FR-008**: The command MUST combine extracted TODO content and source context into a prompt suitable for generating an ordered todo plan.
- **FR-009**: The generated todo plan MUST include grouped work items, source references, intended outcomes, safety notes, and validation expectations for each actionable group.
- **FR-010**: The command MUST present the todo plan in a reviewable form before any workspace-modifying execution begins, and upon user confirmation MUST proceed to execute the plan tasks automatically.
- **FR-011**: The command MUST batch TODO groups when the total number of valid blocks exceeds 10, with each batch containing at most 5 blocks, and MUST present batches sequentially for review and execution.
- **FR-012**: The command MUST provide a clear no-op result when no valid marked TODO blocks are found.

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
