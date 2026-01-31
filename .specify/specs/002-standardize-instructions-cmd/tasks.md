# Tasks: Standardize Instructions Command

**Feature**: Standardize Instructions Command
**Status**: In Progress
**Branch**: `002-standardize-instructions-cmd`

## Phase 1: Setup

- [x] T001 Verify project structure and ensuring `templates/` and `scripts/bash/` directories exist

## Phase 2: Foundational

- [x] T002 Create `templates/instructions-template.md` with standard sections (Overview, Doc Map, Tech Stack)
- [x] T003 Update `templates/commands/instructions.md` to match the command contract schema

## Phase 3: User Story 1 - Generate Standardized Instructions

**Goal**: Implement the robust instructions generation logic with smart fusion.
**Independent Test**: Run `specify instructions` and verify `.ai/instructions.md` is generated/merged correctly.

### Implementation Tasks

- [x] T004 [US1] Initialize `scripts/bash/generate-instructions.sh` with basics (logging, args parsing)
- [x] T005 [P] [US1] Implement "Hard Fail" check: Exit if `templates/instructions-template.md` is missing
- [x] T006 [P] [US1] Implement Variable Substitution logic (replacing `{{PROJECT_NAME}}`, `{{DATE}}`, etc.)
- [x] T007 [US1] Implement Backup Logic: Copy existing `.ai/instructions.md` to `.bak` before writing
- [x] T008 [US1] Implement Smart Fusion: Logic to parse existing Markdown file and extract content by headers
- [x] T009 [US1] Implement Smart Fusion: Logic to merge existing content into the new template structure
- [x] T010 [P] [US1] Implement Relative Symlink creation (e.g., `.clinerules/project_rules.md`)

## Phase 4: Polish

- [x] T011 Verify script execution permissions and error handling messages
- [x] T012 Update `QUICKSTART.md` or equivalent user docs if usage changed

## Dependencies

1. **Foundational** (T002, T003) must strictly precede script testing.
2. **Smart Fusion** (T008, T009) depends on basic script structure (T004).

## Parallel Execution Opportunities

- T005 (Hard Fail check), T006 (Variable Sub), and T010 (Symlinks) can be implemented in parallel after T004 is established.
