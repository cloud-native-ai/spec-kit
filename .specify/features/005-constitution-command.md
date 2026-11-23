# Feature Detail: Constitution Command

**Feature ID**: 005  
**Name**: Constitution Command  
**Description**: Manage project governance and principles.  
**Status**: Completed  
**Created**: 2026-02-10  
**Last Updated**: 2026-11-22

## Overview

`/speckit.constitution` creates or updates the project constitution from interactive or supplied principles, resolves placeholders and version changes, propagates dependent template updates, and emits a Sync Impact Report.

## Latest Review

2026-11-22 implementation audit: the governance workflow is present in `manage-constitution`, including dependent-template synchronization and double-landing guards. The legacy duplicated-number specification links were removed.

## Key Changes

1. Bootstrap or revise `.specify/constitution.md` with concrete project values.
2. Apply the governed version bump and synchronize dependent templates and project guidance.
3. Report propagated changes and unresolved placeholders through a Sync Impact Report.

## Implementation Notes

- Primary surfaces: `templates/commands/constitution.md` and `skills/internal/manage-constitution/SKILL.md`.
- The 2026-11-22 audit found malformed handoff YAML in `templates/commands/constitution.md`; this is a current implementation residual.

## Future Evolution Suggestions

- Repair the handoff frontmatter defect without changing the constitution workflow's governance semantics.

## Related Files

- Feature Index: `.specify/features.md`
- Feature Detail: `.specify/features/005-constitution-command.md`
- Implementation: `templates/commands/constitution.md`, `skills/internal/manage-constitution/SKILL.md`
- Specification: none registered for this legacy command row.

## Status Tracking

- **Draft**: Concept defined.
- **Planned**: Specification and design approved.
- **Implemented**: Constitution workflow delivered and verified.
- **Blocked**: A final-path acceptance criterion fails.
- **Ready for Review**: Review evidence complete with no blocking code-review entry.
- **Sealed**: Canonical seal criteria met.
- **Completed** (legacy — current): Historical delivered status retained.
