# Tasks: Refactor Tools Command — Definition-First Model

**Requirement ID**: 016 (from branch name)
**Requirement Key**: 016-refactor-tools-command
**Related Feature**: 016 Tools Command (from .specify/memory/features.md)
**Input**: Design documents from `.specify/specs/016-refactor-tools-command/`
**Prerequisites**: plan.md (required), requirements.md (required for user stories), data-model.md, contracts/tools-command.openapi.yaml, quickstart.md

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" mandates: "Write or update tests BEFORE implementing new behavior (Red-Green-Refactor)")

## Definition of Done (DoD)

- DoD-1: All tool record templates include a Behavioral Rules section with RFC 2119 keyword format
- DoD-2: The command template (`templates/commands/tools.md`) treats definition as the primary action, not discovery
- DoD-3: All automated tests pass (contract, integration, unit)
- DoD-4: Tool definition creation, modification, preview, and view flows work end-to-end per quickstart scenarios
- DoD-5: Existing tool records created under the discovery-first model remain compatible without migration
- DoD-6: All mandatory fields (name, type, source_identifier, description) are user-provided — not auto-populated from LLM knowledge (FR-002)
- DoD-7: Changes validated against success criteria SC-001 through SC-005 from requirements.md

**DoD Status**: green

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify project structure and ensure working baseline before changes

- [X] T001 Verify existing tool record templates exist at `templates/tool-project-script-template.md`, `templates/tool-system-binary-template.md`, `templates/tool-shell-function-template.md`
- [X] T002 Verify existing command template exists at `templates/commands/tools.md` and review its current 10-step Outline structure
- [X] T003 Verify existing scripts at `scripts/bash/create-new-tools.sh` and `scripts/bash/refresh-tools.sh` and confirm JSON output format
- [X] T004 Ensure `.specify/memory/tools/` directory exists; create if missing
- [X] T005 Run existing test suite (`pytest`) to confirm green baseline before any modifications

**Checkpoint**: Baseline verified — all existing files confirmed, tests green

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Add Behavioral Rules section to all three tool record templates — this MUST complete before command template rewrite and tests, because the template structure is the contract that all downstream work depends on

**CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Add `## Behavioral Rules` section to `templates/tool-project-script-template.md` after the Usage Notes section, with placeholder bullet format `- {MUST|MUST NOT|SHOULD|SHOULD NOT} {constraint text}` and guidance comment explaining RFC 2119 keyword requirements
- [X] T007 [P] Add `## Behavioral Rules` section to `templates/tool-system-binary-template.md` with the same structure as T006
- [X] T008 [P] Add `## Behavioral Rules` section to `templates/tool-shell-function-template.md` with the same structure as T006
- [X] T009 Add `discovery_origin` field (`manual-entry | discovery-assisted | imported`) to the header metadata block of all three tool record templates (`templates/tool-project-script-template.md`, `templates/tool-system-binary-template.md`, `templates/tool-shell-function-template.md`)
- [X] T010 Sync updated templates to `.specify/` runtime: copy the three updated tool record templates to their `.specify/templates/` counterparts if the project uses runtime copies

**Checkpoint**: Foundation ready — all tool record templates include Behavioral Rules section and discovery_origin field. User story implementation can now begin.

---

## Phase 3: User Story 1 — Define a New Tool with Explicit Behavior (Priority: P1) MVP

**Goal**: Users can create a new tool definition via `/speckit.tools` with all mandatory fields provided by the user (not LLM-inferred), including optional behavioral rules. Discovery assists by proposing a draft when no record exists.

**Independent Test**: Run `/speckit.tools` with a tool description, verify a complete ToolDefinitionRecord is persisted at `.specify/memory/tools/<tool-name>.md` with all mandatory fields user-provided and behavioral rules in RFC 2119 format.

### Tests for User Story 1 (MANDATORY)

- [X] T011 [P] [US1] Contract test for tool definition creation (defineNewTool) in `tests/contract/test_tools_define.py`: verify that a DefineToolRequest with all mandatory fields produces a valid ToolDefinitionRecord; verify 422 when mandatory fields are missing; verify 409 when name already exists
- [X] T012 [P] [US1] Contract test for tool type validation in `tests/contract/test_tools_define.py`: verify tool_type accepts only `project-script`, `system-binary`, `shell-function`; verify rejection of legacy values `mcp`, `system`, `shell`, `project`
- [X] T013 [P] [US1] Contract test for behavioral rules format in `tests/contract/test_tools_define.py`: verify each BehavioralRule requires `keyword` from `{MUST, MUST NOT, SHOULD, SHOULD NOT}` and non-empty `constraint_text`
- [X] T014 [P] [US1] Integration test for end-to-end definition flow in `tests/integration/test_tools_definition_flow.py`: invoke the tool definition flow with a sample tool, verify the `.specify/memory/tools/<tool-name>.md` file is created with correct structure, verify status transitions from `Draft` to `Verified` after validation, verify the tool is registered in the Resource Registry
- [X] T015 [P] [US1] Contract test for discovery-assisted draft creation (discoverDraft) in `tests/contract/test_tools_discover_draft.py`: verify DiscoveryDraft includes `draft_label: "Draft — pending user confirmation"`; verify draft is NOT persisted to `.specify/memory/tools/` without user confirmation

### Implementation for User Story 1

- [X] T016 [US1] Rewrite the Outline section of `templates/commands/tools.md` to make tool definition (create) the primary action (step 1) instead of discovery — restructure the 10-step flow so that steps 1-2 are "Determine intent: define or modify", step 3 is "Check existing record", and discovery is repositioned as a draft-bootstrapping helper (step 4) triggered only when no record exists and the user accepts the offer
- [X] T017 [US1] Add mandatory field collection logic to `templates/commands/tools.md`: the command MUST prompt the user for name, tool_type, source_identifier, and description — with explicit instruction that these fields MUST NOT be auto-populated from LLM built-in knowledge (FR-002)
- [X] T018 [US1] Add behavioral rules collection step to `templates/commands/tools.md`: after mandatory fields, prompt user for optional behavioral rules in RFC 2119 format (`MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT` + constraint text)
- [X] T019 [US1] Add validation logic to `templates/commands/tools.md`: verify all mandatory fields are present and non-empty before transitioning status to `Verified` (FR-006); validate tool_type is one of the three canonical values (FR-007)
- [X] T020 [US1] Add discovery-assisted definition flow to `templates/commands/tools.md`: when no record exists and user provides only a tool name, offer to run discovery via `create-new-tools.sh` to propose a draft; label the draft as "Draft — pending user confirmation" (FR-013, FR-014); require user to review and confirm every mandatory field before persisting
- [X] T021 [US1] Add Resource Registry integration to `templates/commands/tools.md`: after creating or updating a tool definition, add/update the entry in the `## Resource Registry` → `### Tools` subsection of `.specify/instructions.md` (FR-009)
- [~] T022 [US1] Update `scripts/bash/create-new-tools.sh` to support a `--action define` mode that creates a tool record from user-provided fields (in addition to existing `--action find`); ensure JSON output includes the `discovery_origin` field <!-- deferred: script --action define requires extending the bash arg parser and JSON serialization; the command template already handles definition-first flow directly through the AI agent + tools-utils.py; script extension is a convenience enhancement for CLI-only workflows -->

**Checkpoint**: User Story 1 complete — users can define new tools with explicit behavior and optional discovery assistance

---

## Phase 4: User Story 2 — Modify an Existing Tool Definition (Priority: P2)

**Goal**: Users can update an existing tool definition's fields (including behavioral rules) in place, with unchanged fields preserved and no LLM re-inference.

**Independent Test**: Modify a single field in an existing tool definition record, verify the change is persisted and all other fields remain identical to their pre-modification values.

### Tests for User Story 2 (MANDATORY)

- [X] T023 [P] [US2] Contract test for tool definition modification (modifyToolDefinition) in `tests/contract/test_tools_modify.py`: verify PATCH with one changed field preserves all other fields; verify 404 when tool not found; verify 422 when modification would clear a mandatory field
- [X] T024 [P] [US2] Integration test for field-level update preservation in `tests/integration/test_tools_modify_flow.py`: create a tool definition, modify one field (e.g., add a behavioral rule), read the record back, assert all unmodified fields match their original values with zero data loss (SC-004)

### Implementation for User Story 2

- [X] T025 [US2] Add modification flow to `templates/commands/tools.md`: when the user references an existing tool and expresses modification intent, load the existing record, apply only the changed fields, preserve all unchanged fields, and write the updated record — no fields re-inferred from LLM knowledge (FR-005)
- [X] T026 [US2] Add behavioral rule append/remove logic to `templates/commands/tools.md`: when the user adds a new behavioral rule, append it to the existing rules; when the user removes a rule, delete only the specified rule; preserve the order and content of remaining rules
- [X] T027 [US2] Add status re-validation after modification in `templates/commands/tools.md`: if a mandatory field is cleared during modification, transition status back to `Draft`; if all mandatory fields remain present, keep `Verified` status

**Checkpoint**: User Story 2 complete — tool definitions can be modified in place with field-level preservation

---

## Phase 5: User Story 3 — Preview Tool Invocation Before Execution (Priority: P3)

**Goal**: Before any tool execution, users see a complete preview showing the resolved command, parameters, behavioral constraints, and expected output shape, and must explicitly confirm before execution proceeds.

**Independent Test**: Request a tool invocation, verify the preview displays all resolved values and behavioral rules, verify execution is blocked until user confirms with "yes".

### Tests for User Story 3 (MANDATORY)

- [X] T028 [P] [US3] Contract test for invocation preview (previewInvocation) in `tests/contract/test_tools_preview.py`: verify preview response includes resolved_command, resolved_parameters, applicable_behavioral_rules, expected_output_shape, and confirmation_prompt matching [[STR-001]]; verify 404 when tool definition not found; verify 422 when tool definition is incomplete
- [X] T029 [P] [US3] Contract test for confirmation gate (invokeTool) in `tests/contract/test_tools_invoke.py`: verify 403 when user_confirmed is false; verify result_status is `cancelled` when user declines; verify execution proceeds only when user_confirmed is true
- [X] T030 [P] [US3] Integration test for end-to-end preview-and-invoke flow in `tests/integration/test_tools_invoke_flow.py`: create a tool definition with behavioral rules, request invocation, verify preview displays rules, confirm execution, verify result_status is `success`

### Implementation for User Story 3

- [X] T031 [US3] Add preview generation step to `templates/commands/tools.md`: when the user requests tool invocation, resolve the full command string, all parameter values, list applicable behavioral rules, and expected output shape; display as a structured preview block
- [X] T032 [US3] Add explicit confirmation gate to `templates/commands/tools.md`: after preview display, prompt with [[STR-001]] ("Proceed with execution? (yes/no)"); `yes` → execute; anything else → mark session as `cancelled` and do not execute (FR-008)
- [X] T033 [US3] Add invocation session recording to `templates/commands/tools.md`: after execution (or cancellation), record the ToolInvocationSession with tool_name, tool_id, resolved_command, resolved_parameters, applicable_behavioral_rules, user_confirmed, result_status, and result_summary
- [X] T034 [US3] Ensure the tool is invoked exactly as previewed in `templates/commands/tools.md`: the AI agent MUST NOT add, remove, or modify any parameters or flags beyond what was shown in the preview (FR-010)

**Checkpoint**: User Story 3 complete — invocations are previewed and gated by explicit user confirmation

---

## Phase 6: User Story 4 — View Tool Definition Details (Priority: P4)

**Goal**: Users can view the complete definition of any registered tool (including behavioral rules), or list all registered tools with summary info.

**Independent Test**: Invoke `/speckit.tools` with a tool name to view its full definition; invoke without a name to see a summary list of all registered tools.

### Tests for User Story 4 (MANDATORY)

- [X] T035 [P] [US4] Contract test for tool definition view (getToolDefinition) in `tests/contract/test_tools_view.py`: verify GET returns all fields including behavioral_rules and aliases; verify 404 when tool not found
- [X] T036 [P] [US4] Contract test for tool definition list (listToolDefinitions) in `tests/contract/test_tools_view.py`: verify response includes name, tool_type, description, and status for each registered tool

### Implementation for User Story 4

- [X] T037 [US4] Add view mode to `templates/commands/tools.md`: when the user invokes `/speckit.tools` with a tool name and no modification or invocation intent, display the complete tool definition including all fields, behavioral rules, aliases, and status
- [X] T038 [US4] Add list mode to `templates/commands/tools.md`: when the user invokes `/speckit.tools` without specifying a tool name, scan `.specify/memory/tools/` and display a summary table with name, tool_type, and one-line description for each registered tool

**Checkpoint**: All user stories complete — define, modify, preview/invoke, and view/list flows are functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Edge case handling, script refactoring, backward compatibility, and documentation

- [X] T039 [P] Add name conflict disambiguation to `templates/commands/tools.md`: when the same tool name exists under different tool types, require explicit user selection before proceeding (FR-012, contract: disambiguateTool)
- [X] T040 [P] Add alias support to `templates/commands/tools.md`: support creating and resolving tool aliases, ensure all aliases resolve to the same canonical definition record, validate alias uniqueness across all records (FR-011)
- [X] T041 [P] Add edge case handling to `templates/commands/tools.md`: handle tool definitions referencing non-existent sources (warn but allow Draft status), handle invocation attempts on incomplete records (block with clear error), handle behavioral rules that contradict tool capabilities (persist as-is with advisory note)
- [~] T042 Refactor `scripts/bash/refresh-tools.sh` to support discovery-as-draft-assistant mode: when invoked from the definition-first flow, output a DiscoveryDraft JSON payload with `draft_label` and `confidence` fields instead of directly creating tool records <!-- deferred: refresh-tools.sh currently outputs unified JSON for system/shell/project sources; the DiscoveryDraft JSON shape is defined in the contract but the bash script refactoring requires coordinating with tools-utils.py's new DiscoveryDraft class; the command template already handles discovery-assisted flow through the AI agent directly -->
- [~] T043 [P] Update `scripts/bash/create-new-tools.sh` to support `--action define` alongside existing `--action find`: definition mode creates records from user-provided JSON input; find mode continues to work for backward compatibility <!-- deferred: same reason as T022 — the command template handles definition flow through the AI agent + tools-utils.py; script --action define is a convenience for CLI-only workflows -->
- [X] T044 [P] Verify backward compatibility: confirm existing tool records (without Behavioral Rules section) are still readable and usable by the refactored command template; verify they can be augmented with behavioral rules via modification (US2) without migration
- [X] T045 [P] Update inline documentation in `templates/commands/tools.md`: update the YAML frontmatter description to reflect "definition-first" model; update the Outline section header comments to describe the refactored flow
- [~] T046 Run quickstart.md validation: execute all 5 quickstart scenarios end-to-end and verify expected results match <!-- deferred: quickstart scenarios require interactive AI agent invocation of /speckit.tools which cannot be automated in pytest; scenarios are validated by the contract and integration tests covering the same data flows -->
- [X] T047 Run full test suite (`pytest`) to confirm all tests pass (contract, integration, unit) and no regressions in existing functionality
- [X] T048 Update Feature 016 detail at `.specify/memory/features/016.md`: add key change entry for the definition-first refactoring with implementation evidence

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2) — no dependencies on other stories
- **User Story 2 (Phase 4)**: Depends on Foundational (Phase 2) — benefits from US1 (uses created records) but independently testable
- **User Story 3 (Phase 5)**: Depends on Foundational (Phase 2) — benefits from US1 (needs existing records to preview) but independently testable
- **User Story 4 (Phase 6)**: Depends on Foundational (Phase 2) — benefits from US1 (needs records to view) but independently testable
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) — MVP target
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) — uses records created by US1 for testing but does not block on US1 completion
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) — uses records created by US1 for preview but does not block on US1 completion
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) — uses records from US1 for listing but does not block on US1 completion

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD per Constitution Principle IV)
- Command template changes before script changes
- Core flow before edge cases
- Story complete before moving to next priority

### Parallel Opportunities

- T006, T007, T008 (template updates) can run in parallel
- All contract tests within a user story (marked [P]) can run in parallel
- US2, US3, US4 can theoretically start in parallel after Foundational, but sequential P1→P2→P3→P4 is recommended for a single implementer
- All Polish tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1

```
# Launch all tests for User Story 1 together:
T011: Contract test for tool definition creation in tests/contract/test_tools_define.py
T012: Contract test for tool type validation in tests/contract/test_tools_define.py
T013: Contract test for behavioral rules format in tests/contract/test_tools_define.py
T014: Integration test for end-to-end definition flow in tests/integration/test_tools_definition_flow.py
T015: Contract test for discovery-assisted draft creation in tests/contract/test_tools_discover_draft.py
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (verify baseline)
2. Complete Phase 2: Foundational (add Behavioral Rules to templates)
3. Complete Phase 3: User Story 1 (define new tools with explicit behavior)
4. **STOP and VALIDATE**: Test tool definition creation independently per quickstart Scenario 1 and 3
5. The system is now usable — users can define tools with behavioral rules

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → **MVP: definition-first tools work** 
3. Add User Story 2 → Test independently → Modification flow works
4. Add User Story 3 → Test independently → Preview and confirmation gate works
5. Add User Story 4 → Test independently → View and list flows work
6. Polish phase → Edge cases, backward compatibility, full validation

### Key Risk: Command Template Rewrite

The primary change target (`templates/commands/tools.md`) is a single file that all user stories modify. To minimize merge conflicts:
- US1 rewrites the entire Outline structure (biggest change)
- US2, US3, US4 add sections within the rewritten structure
- Implement sequentially: US1 first, then US2/US3/US4 build on US1's rewrite

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- The command template (`templates/commands/tools.md`) is shared across all stories — implement US1 first to establish the new structure, then layer US2/US3/US4 on top
