# Tasks: Agent-Specific Configuration for Commands and Skills

**Requirement ID**: 021 (from branch name)
**Requirement Key**: 021-agent-specific-config
**Related Feature**: 022 AI Tools Support (from .specify/memory/features.md)
**Input**: Design documents from `.specify/specs/021-agent-specific-config/`
**Prerequisites**: plan.md (required), requirements.md (required), data-model.md, contracts/, quickstart.md

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" states implementation MUST follow rigorous quality standards; contract tests validate template structure)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story. US1 and US2 are both P1 and can proceed in parallel after Foundational phase.

## Definition of Done (DoD)

- DoD-1: All 7 target files contain `## Agent-Specific Configuration` section with three-step workflow
- DoD-2: All 8 agent reference documents exist (2 per skill × 4 skills) with required sections
- DoD-3: `.specify/memory/feedback/` directory exists with `.gitkeep`
- DoD-4: All contract tests pass (C-001 through C-008)
- DoD-5: Command templates embed inline agent guidance for Claude Code and Copilot
- DoD-6: Agent-Specific Configuration sections are additive — removing them leaves core workflows intact
- DoD-7: Changes validated against SC-001 through SC-006

**DoD Status**: green

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup

**Purpose**: Create directories and scaffold infrastructure needed by all user stories

- [X] T001 Create feedback directory at `.specify/memory/feedback/` with `.gitkeep` file
- [X] T002 [P] Create `skills/create-agent/references/` directory (does not exist yet)
- [X] T003 [P] Create `skills/improve-agent/references/` directory (does not exist yet)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Define the canonical section templates and agent identification logic that all user story tasks will reuse

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Draft the canonical "Agent-Specific Configuration" section template with three steps (identify, load, capture) as a reference snippet to be used across all 7 target files. Store at `.specify/specs/021-agent-specific-config/snippets/agent-config-section.md`
- [X] T005 [P] Draft the canonical agent reference document template with four sections (Tool Mapping, Best Practices, Known Pitfalls, Capability Notes). Store at `.specify/specs/021-agent-specific-config/snippets/agent-reference-template.md`
- [X] T006 [P] Draft the canonical feedback document template with required fields (Source, Agent, Timestamp, Outcome, Obstacle, Workaround, Suggested Improvement). Store at `.specify/specs/021-agent-specific-config/snippets/feedback-template.md`

**Checkpoint**: Canonical templates ready — US1, US2, US3 implementation can begin

---

## Phase 3: User Story 1 — Agent-Aware Command Execution (Priority: P1) 🎯 MVP

**Goal**: Add Agent-Specific Configuration section with inline per-agent guidance to all 3 command templates

**Independent Test**: Run `/speckit.agents` from Claude Code and verify Claude Code-specific guidance appears; verify same command from Copilot shows Copilot guidance; verify unknown agent falls back to generic guidance

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T007 [P] [US1] Contract test for C-001 (command template section presence): verify `## Agent-Specific Configuration`, `### Step 1`, `### Step 2`, `### Step 3` headings exist in all 3 command templates. Write at `tests/contract/test_agent_specific_config_commands.py`
- [X] T008 [P] [US1] Contract test for C-007 (additive constraint): verify `## Agent-Specific Configuration` section appears after main workflow sections and before `## Handoffs` in each command template. Write at `tests/contract/test_agent_specific_config_commands.py`

### Implementation for User Story 1

- [X] T009 [P] [US1] Add Agent-Specific Configuration section to `templates/commands/agents.md` — include Step 1 (agent identification via system prompt, available tools, directory markers), Step 2 (inline Claude Code and Copilot guidance subsections for agent creation workflows), Step 3 (feedback capture instructions pointing to `.specify/memory/feedback/`)
- [X] T010 [P] [US1] Add Agent-Specific Configuration section to `templates/commands/skills.md` — include Step 1 (agent identification), Step 2 (inline Claude Code and Copilot guidance subsections for skill management workflows), Step 3 (feedback capture instructions)
- [X] T011 [P] [US1] Add Agent-Specific Configuration section to `templates/commands/tools.md` — include Step 1 (agent identification), Step 2 (inline Claude Code and Copilot guidance subsections for tool management workflows), Step 3 (feedback capture instructions)
- [X] T012 [US1] Run contract tests from T007–T008 and verify all pass

**Checkpoint**: All 3 command templates have Agent-Specific Configuration sections with inline Claude Code + Copilot guidance

---

## Phase 4: User Story 2 — Tool-Specific References for Skills (Priority: P1)

**Goal**: Add Agent-Specific Configuration section to all 4 skill SKILL.md files and create 8 agent reference documents (claude-code-guide.md + copilot-guide.md per skill)

**Independent Test**: Examine each skill's SKILL.md for Agent-Specific Configuration section that references `${SKILL_HOME}/references/<agent-slug>-guide.md`; verify the referenced files exist with all 4 required sections

### Tests for User Story 2 (MANDATORY) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T013 [P] [US2] Contract test for C-002 (skill SKILL.md section presence): verify `## Agent-Specific Configuration` heading and three-step subsections in all 4 skill SKILL.md files. Write at `tests/contract/test_agent_specific_config_skills.py`
- [X] T014 [P] [US2] Contract test for C-003 (reference document naming): verify `claude-code-guide.md` and `copilot-guide.md` exist in `references/` for all 4 targeted skills. Write at `tests/contract/test_agent_specific_config_skills.py`
- [X] T015 [P] [US2] Contract test for C-004 (reference document structure): verify each agent reference document contains `## Tool Mapping`, `## Best Practices`, `## Known Pitfalls`, `## Capability Notes` headings. Write at `tests/contract/test_agent_specific_config_skills.py`

### Implementation for User Story 2 — SKILL.md Sections

- [X] T016 [P] [US2] Add Agent-Specific Configuration section to `skills/browser-utils/SKILL.md` — Step 1 (identify agent), Step 2 (load `${SKILL_HOME}/references/<agent-slug>-guide.md`), Step 3 (feedback capture)
- [X] T017 [P] [US2] Add Agent-Specific Configuration section to `skills/create-agent/SKILL.md` — same three-step structure
- [X] T018 [P] [US2] Add Agent-Specific Configuration section to `skills/improve-agent/SKILL.md` — same three-step structure
- [X] T019 [P] [US2] Add Agent-Specific Configuration section to `skills/improve-skills/SKILL.md` — same three-step structure

### Implementation for User Story 2 — Claude Code Reference Documents

- [X] T020 [P] [US2] Create `skills/browser-utils/references/claude-code-guide.md` — Tool Mapping (Bash for Playwright, Read for screenshots, Agent for parallel tests), Best Practices (headless default, /tmp scripts, auto-detect dev servers), Known Pitfalls (WebFetch doesn't support file://, timeout needed for long renders), Capability Notes (background tasks, structured output)
- [X] T021 [P] [US2] Create `skills/create-agent/references/claude-code-guide.md` — Tool Mapping (Edit for .agent.md modifications, Agent for subagent testing, Bash for frontmatter validation), Best Practices (use Edit not Write for updates, verify symlinks via Bash), Known Pitfalls (Write overwrites without diff, Agent tool typing differences), Capability Notes (hooks, worktrees)
- [X] T022 [P] [US2] Create `skills/improve-agent/references/claude-code-guide.md` — Tool Mapping (Read for template analysis, Edit for targeted fixes, Bash for grep-based evidence), Best Practices (minimal diffs, read before edit), Known Pitfalls (context window limits on large templates), Capability Notes (auto-memory for feedback patterns)
- [X] T023 [P] [US2] Create `skills/improve-skills/references/claude-code-guide.md` — Tool Mapping (Read for SKILL.md analysis, Edit for targeted fixes, Bash for validation scripts, Agent for parallel analysis), Best Practices (re-read after edits, use grep for evidence), Known Pitfalls (symlink resolution differences, skill_id refresh), Capability Notes (background tasks for validation)

### Implementation for User Story 2 — Copilot Reference Documents

- [X] T024 [P] [US2] Create `skills/browser-utils/references/copilot-guide.md` — Tool Mapping (terminal panel for shell commands, workspace edit for file changes), Best Practices (use @terminal for Playwright, prefer headless mode in IDE context), Known Pitfalls (limited background task support, no direct screenshot viewing in chat), Capability Notes (VS Code integration, limited shell timeout)
- [X] T025 [P] [US2] Create `skills/create-agent/references/copilot-guide.md` — Tool Mapping (workspace edit for .agent.md, @terminal for validation), Best Practices (use Copilot-native frontmatter fields, test with agent picker), Known Pitfalls (.agent.md format differences from Claude Code), Capability Notes (agent picker integration, @agent invocation)
- [X] T026 [P] [US2] Create `skills/improve-agent/references/copilot-guide.md` — Tool Mapping (search for template analysis, workspace edit for fixes), Best Practices (use inline suggestions for small changes), Known Pitfalls (limited multi-file diff support), Capability Notes (IDE-integrated agent testing)
- [X] T027 [P] [US2] Create `skills/improve-skills/references/copilot-guide.md` — Tool Mapping (search for evidence, workspace edit for targeted fixes, @terminal for scripts), Best Practices (Copilot Chat for analysis, workspace edit for SKILL.md), Known Pitfalls (limited grep capabilities in chat mode, no background validation), Capability Notes (VS Code task integration)

- [X] T028 [US2] Run contract tests from T013–T015 and verify all pass

**Checkpoint**: All 4 skills have Agent-Specific Configuration sections; 8 reference documents created (claude-code-guide.md + copilot-guide.md per skill)

---

## Phase 5: User Story 3 — Execution Feedback Generation (Priority: P2)

**Goal**: Ensure the feedback capture step in all 7 target files correctly instructs agents to generate feedback documents at `.specify/memory/feedback/` when agent-specific obstacles are encountered

**Independent Test**: Trigger an agent-specific obstacle during skill execution and verify a feedback document is created with required structure at `.specify/memory/feedback/`

### Tests for User Story 3 (MANDATORY) ⚠️

- [X] T029 [P] [US3] Contract test for C-005 (feedback document structure): create a sample feedback document and verify it contains required fields (Source, Agent, Timestamp, Outcome, Obstacle, Suggested Improvement headings). Write at `tests/contract/test_agent_specific_config_feedback.py`
- [X] T030 [P] [US3] Contract test for C-008 (feedback directory existence): verify `.specify/memory/feedback/` directory exists and contains `.gitkeep`. Write at `tests/contract/test_agent_specific_config_feedback.py`

### Implementation for User Story 3

- [X] T031 [US3] Review all 7 target files and verify Step 3 (Capture Execution Feedback) sections are complete and consistent — each must instruct the agent to generate a feedback document at `.specify/memory/feedback/<source>-<agent-slug>-<timestamp>.md` with all required fields per the feedback template from T006
- [X] T032 [US3] Create a sample feedback document at `.specify/specs/021-agent-specific-config/snippets/sample-feedback.md` demonstrating the expected structure for documentation and test fixture purposes
- [X] T033 [US3] Run contract tests from T029–T030 and verify all pass

**Checkpoint**: Feedback generation workflow complete; centralized feedback directory ready for runtime use

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validation, documentation, and cross-artifact consistency

- [X] T034 [P] Run full contract test suite (`pytest tests/contract/ -v`) and verify all agent-specific-config tests pass
- [X] T035 [P] Verify additive constraint (C-007): for each of the 7 target files, confirm that removing the `## Agent-Specific Configuration` section leaves the file functional with no broken references
- [X] T036 Update Feature 022 detail at `.specify/memory/features/022.md` with implementation notes for spec 021
- [X] T037 Clean up snippet files from `.specify/specs/021-agent-specific-config/snippets/` — these were working drafts; canonical content now lives in the target files

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **US1 Commands (Phase 3)**: Depends on Foundational (Phase 2) — no dependency on US2 or US3
- **US2 Skills (Phase 4)**: Depends on Foundational (Phase 2) — no dependency on US1 or US3
- **US3 Feedback (Phase 5)**: Depends on US1 and US2 completion (Step 3 sections must exist in all 7 files before review)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational — independent of US2
- **User Story 2 (P1)**: Can start after Foundational — independent of US1
- **User Story 3 (P2)**: Depends on US1 and US2 (reviews Step 3 sections added by both)

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Section template (from Foundational) is applied first, then content is customized
- Reference documents are parallelizable (different files, no shared state)
- Contract test validation runs after all implementation tasks in that story

### Parallel Opportunities

- T002 + T003 can run in parallel (different directories)
- T004 + T005 + T006 can run in parallel (different snippet files)
- T007 + T008 can run in parallel (same test file, different test functions)
- T009 + T010 + T011 can run in parallel (different command template files)
- T013 + T014 + T015 can run in parallel (same test file, different test functions)
- T016 + T017 + T018 + T019 can run in parallel (different SKILL.md files)
- T020–T027 can ALL run in parallel (8 independent reference documents)
- T029 + T030 can run in parallel (same test file, different test functions)
- T034 + T035 can run in parallel (testing vs. manual verification)

---

## Parallel Example: User Story 2 (Skills)

```bash
# Launch all SKILL.md edits together (4 independent files):
Task T016: "Add Agent-Specific Configuration section to skills/browser-utils/SKILL.md"
Task T017: "Add Agent-Specific Configuration section to skills/create-agent/SKILL.md"
Task T018: "Add Agent-Specific Configuration section to skills/improve-agent/SKILL.md"
Task T019: "Add Agent-Specific Configuration section to skills/improve-skills/SKILL.md"

# Launch all reference documents together (8 independent files):
Task T020: "Create skills/browser-utils/references/claude-code-guide.md"
Task T021: "Create skills/create-agent/references/claude-code-guide.md"
Task T022: "Create skills/improve-agent/references/claude-code-guide.md"
Task T023: "Create skills/improve-skills/references/claude-code-guide.md"
Task T024: "Create skills/browser-utils/references/copilot-guide.md"
Task T025: "Create skills/create-agent/references/copilot-guide.md"
Task T026: "Create skills/improve-agent/references/copilot-guide.md"
Task T027: "Create skills/improve-skills/references/copilot-guide.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (create directories)
2. Complete Phase 2: Foundational (draft canonical templates)
3. Complete Phase 3: User Story 1 (3 command templates with inline guidance)
4. **STOP and VALIDATE**: Verify command templates have Agent-Specific Configuration sections; run contract tests
5. Commands are now agent-aware — MVP delivered

### Incremental Delivery

1. Setup + Foundational → Infrastructure ready
2. Add US1 (Commands) → 3 command templates agent-aware → Validate independently
3. Add US2 (Skills) → 4 skills + 8 reference docs → Validate independently
4. Add US3 (Feedback) → Feedback loop complete → Validate end-to-end
5. Polish → All contracts pass, feature complete

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (3 command templates)
   - Developer B: User Story 2 (4 skills + 8 references)
3. After US1 + US2 complete: User Story 3 (feedback review)
4. Polish phase

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- All changes are markdown template/document edits — no Python CLI code changes
- Reference documents should contain genuine agent-specific guidance, not generic boilerplate
- Snippet files in Phase 2 are working drafts; cleaned up in Phase 6
- Agent slugs for file naming: `claude-code` (not `claude`), `copilot`, `qoder`, `opencode`, `qwen`, `codex`, `hermes`, `iflow`
