# Research: Remove GitHub API Integration

**Status**: Completed
**Date**: 2025-12-11

## Decision: Remove `taskstoissues` and related artifacts

**Rationale**:
The user explicitly requested the removal of the `taskstoissues` command and all GitHub API interaction logic. This feature is no longer supported or desired.

**Alternatives Considered**:
- **Deprecation**: Mark the command as deprecated but keep the code. Rejected because the user asked for removal.
- **Hide**: Hide the command from help but keep the code. Rejected because the user asked for removal of logic and code.

## Impact Analysis

- **CLI**: `taskstoissues` command will be removed.
- **Dependencies**: `PyGithub` or similar libraries might be removable if not used elsewhere. (Need to check `pyproject.toml`)
- **Configuration**: `speckit.taskstoissues` setting in `vscode-settings.json` should be removed.
- **Prompts**: `.github/prompts/speckit.taskstoissues.prompt.md` will be deleted.
- **Templates**: `templates/commands/taskstoissues.md` will be deleted.

## Verification Plan

- Run `speckit --help` to ensure `taskstoissues` is gone.
- Run `grep` to ensure no references remain in the codebase.
- Run tests to ensure no regressions in other commands.
