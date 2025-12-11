# Tasks: Remove GitHub API Integration

**Feature**: Remove GitHub API Integration
**Status**: Planned
**Spec**: [.specify/specs/004-remove-github-api/spec.md](../spec.md)

## Phase 1: Setup & Verification

**Goal**: Verify current state and prepare for removal.

- [x] T001 Verify `taskstoissues` command exists and is registered in `src/specify_cli/commands/`
- [x] T002 Verify `speckit.taskstoissues.prompt.md` exists in `.github/prompts/`
- [x] T003 Verify `taskstoissues.md` exists in `templates/commands/`

## Phase 2: Foundational (Blocking)

**Goal**: Remove core dependencies and configuration to prevent accidental usage during cleanup.

- [x] T004 Remove `speckit.taskstoissues` configuration from `templates/vscode-settings.json`
- [x] T005 Remove `speckit.taskstoissues` configuration from `.specify/templates/vscode-settings.json`

## Phase 3: User Story 1 - Remove taskstoissues Command (P1)

**Goal**: Remove the `taskstoissues` command from the CLI to stop supporting the creation of GitHub issues from tasks.
**Independent Test**: `speckit --help` should not list `taskstoissues`.

- [x] T006 [US1] Delete `src/specify_cli/commands/taskstoissues.py` (or equivalent implementation file)
- [x] T007 [US1] Remove `taskstoissues` command registration from `src/specify_cli/__init__.py` or main entry point (if applicable)
- [x] T008 [US1] Delete `templates/commands/taskstoissues.md`
- [x] T009 [US1] Delete `.github/prompts/speckit.taskstoissues.prompt.md`

## Phase 4: User Story 2 - Remove GitHub API Logic (P1)

**Goal**: Remove the underlying Python code and prompt files that interact with the GitHub API.
**Independent Test**: Code search for GitHub API usage returns no results.

- [x] T010 [US2] Search for and remove any shared GitHub API client utilities in `src/specify_cli/` (if any exist and are ONLY used by this feature)
- [x] T011 [US2] Check `pyproject.toml` for `PyGithub` or similar dependencies and remove if no longer needed by other features

## Phase 5: Polish & Cleanup

**Goal**: Ensure no regressions and clean up any remaining references.

- [x] T012 Run `grep -r "taskstoissues" .` to find any remaining references in comments or documentation and remove them
- [x] T013 Run full test suite to ensure no regressions in other commands
- [x] T014 Verify `speckit --help` output is clean

## Dependencies

- T001, T002, T003 -> T004, T005
- T004, T005 -> T006, T007, T008, T009
- T006, T007 -> T010, T011
- T010, T011 -> T012, T013, T014

## Parallel Execution Examples

- T008 (Delete template) and T009 (Delete prompt) can be done in parallel with T006 (Delete code).

## Implementation Strategy

1. **Verify**: Confirm existence of files to be deleted.
2. **Config**: Remove configuration first.
3. **Code**: Remove the command implementation and registration.
4. **Assets**: Remove templates and prompts.
5. **Cleanup**: Remove dependencies and verify.
