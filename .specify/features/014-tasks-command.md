# Feature Detail: Tasks Command

**Feature ID**: 014  
**Name**: Tasks Command  
**Description**: Break down plans into dependency-ordered executable tasks.
**Status**: Completed  
**Created**: 2026-02-10  
**Last Updated**: 2026-11-22

## Overview

`/speckit.tasks` delegates to `create-tasks` to organize immediately executable tasks by user story, dependency, test mode, and MVP order. Existing task files can be validated and amended while preserving stable task identities.

## Latest Review

2026-11-22 implementation audit: the current command includes deterministic validation for task IDs, `blockedBy` edges, parallel write conflicts, story labels, and green-point attribution. Duplicated-number specification links were removed.

## Key Changes

1. Generate dependency-ordered tasks from requirements and design artifacts.
2. Select the Constitution-driven test mode and preserve user-story execution order.
3. Validate and amend existing task files without silently rewriting stable IDs.
4. Check parallel safety, green-point coverage, and dependency integrity mechanically.

## Implementation Notes

- Primary surfaces: `templates/commands/tasks.md`, `skills/internal/create-tasks/SKILL.md`, and `scripts/python/validate-tasks.py`.
- Current contract tests cover parallel-write conflicts and task structure.

## Future Evolution Suggestions

- Keep task grammar and coverage attribution aligned with new acceptance artifact types.

## Related Files

- Feature Index: `.specify/features.md`
- Feature Detail: `.specify/features/014-tasks-command.md`
- Implementation: `templates/commands/tasks.md`, `skills/internal/create-tasks/SKILL.md`
- Specification: none registered for this legacy command row.

## Status Tracking

- **Draft**: Concept defined.
- **Planned**: Specification and design approved.
- **Implemented**: Task workflow delivered and verified.
- **Blocked**: A final-path acceptance criterion fails.
- **Ready for Review**: Review evidence complete with no blocking code-review entry.
- **Sealed**: Canonical seal criteria met.
- **Completed** (legacy — current): Historical delivered status retained.
