# Feature Specification: Remove GitHub API Integration

**Feature Branch**: `004-remove-github-api`  
**Created**: 2025-12-11  
**Status**: Draft  
**Input**: User description: "在项目中删除和github api进行交互的代码，包括taskstoissues命令，调用github api的逻辑等。"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Remove taskstoissues Command (Priority: P1)

Remove the `taskstoissues` command from the CLI to stop supporting the creation of GitHub issues from tasks.

**Why this priority**: This is the primary user-facing change requested.

**Independent Test**: Verify the command is gone from the help menu and cannot be executed.

**Acceptance Scenarios**:

1. **Given** the CLI is installed, **When** I run `speckit --help`, **Then** `taskstoissues` should NOT be listed in the available commands.
2. **Given** the CLI is installed, **When** I try to run `speckit taskstoissues`, **Then** it should return an error indicating the command does not exist.

---

### User Story 2 - Remove GitHub API Logic (Priority: P1)

Remove the underlying Python code and prompt files that interact with the GitHub API.

**Why this priority**: To clean up the codebase and remove unused dependencies/logic.

**Independent Test**: Code search for GitHub API usage returns no results (excluding documentation/comments).

**Acceptance Scenarios**:

1. **Given** the codebase, **When** I search for the `taskstoissues` command implementation, **Then** it should not exist.
2. **Given** the codebase, **When** I search for the `speckit.taskstoissues.prompt.md` file, **Then** it should not exist.
3. **Given** the codebase, **When** I search for GitHub API client initialization logic used by this feature, **Then** it should not exist.

### Edge Cases

- What happens if a user has `taskstoissues` in their history or scripts?
  - They will get a "command not found" error. This is expected.
- What happens to existing configuration for GitHub tokens?
  - If the token is only used for this feature, it becomes irrelevant. If used for other things (unlikely based on request), it stays but is unused here.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The `taskstoissues` command MUST be removed from the CLI registration.
- **FR-002**: The `speckit.taskstoissues.prompt.md` file MUST be deleted.
- **FR-003**: The Python implementation file for `taskstoissues` (e.g., `src/specify_cli/commands/taskstoissues.py` or similar) MUST be deleted.
- **FR-004**: Any shared utilities specifically and ONLY used for GitHub API interaction in this context MUST be removed.
- **FR-005**: Documentation referencing `taskstoissues` (e.g., `templates/commands/taskstoissues.md`) MUST be removed or updated.

### Key Entities *(include if feature involves data)*

- N/A

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `speckit --help` does not list `taskstoissues`.
- **SC-002**: The file `.github/prompts/speckit.taskstoissues.prompt.md` is deleted.
- **SC-003**: The project builds successfully without the removed code.
- **SC-004**: No "ImportError" or runtime errors occur due to missing modules when running other commands.

## Clarifications

