# Feature Detail: Instructions Command

**Feature ID**: 008  
**Name**: Instructions Command  
**Description**: Non-destructively reconcile project AI instructions and compatibility symlinks.
**Status**: Completed  
**Created**: 2026-02-10  
**Last Updated**: 2026-11-22

## Overview

`/speckit.instructions` generates or refreshes `.specify/instructions.md` while preserving existing project content, creates timestamped backups, restores missing template sections, and maintains compatibility symlinks for supported AI tools.

## Latest Review

2026-11-22 implementation audit: the current behavior is a non-destructive instructions reconcile engine with section recovery and symlink maintenance, not generic prompt generation. Duplicated-number specification links were removed.

## Key Changes

1. Merge required instruction sections without discarding preserved project content.
2. Create timestamped backups and report the reconciliation result.
3. Maintain canonical instructions and per-tool compatibility symlinks.

## Implementation Notes

- Primary surfaces: `templates/commands/instructions.md`, `skills/internal/manage-instructions/SKILL.md`, and `scripts/bash/generate-instructions.sh`.
- Preservation and section-propagation behavior is covered by integration and contract tests.

## Future Evolution Suggestions

- Keep newly mandatory ambient sections within the declared instructions byte budget.

## Related Files

- Feature Index: `.specify/features.md`
- Feature Detail: `.specify/features/008-instructions-command.md`
- Implementation: `templates/commands/instructions.md`, `scripts/bash/generate-instructions.sh`
- Specification: none registered for this legacy command row.

## Status Tracking

- **Draft**: Concept defined.
- **Planned**: Specification and design approved.
- **Implemented**: Instructions reconciliation delivered and verified.
- **Blocked**: A final-path acceptance criterion fails.
- **Ready for Review**: Review evidence complete with no blocking code-review entry.
- **Sealed**: Canonical seal criteria met.
- **Completed** (legacy — current): Historical delivered status retained.
