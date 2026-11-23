# Feature Detail: Checklist Command

**Feature ID**: 003  
**Name**: Checklist Command  
**Description**: Generate traceable requirements-quality checklists with append-only rechecks.
**Status**: Completed  
**Created**: 2026-02-10  
**Last Updated**: 2026-11-22

## Overview

`/speckit.checklist` authors requirement-quality checks rather than implementation tests or a dedicated constitution-compliance report. Each run creates a dated checklist, traces items to requirement gaps, and supports append-only rechecks that preserve earlier outcomes.

## Latest Review

2026-11-22 implementation audit: the current behavior is requirements-quality authoring and recheck; the former constitution-alignment description and nonexistent duplicated-number links were incorrect.

## Key Changes

1. Delegate checklist creation to `create-checklist` with explicit traceability and quality-focus rules.
2. Write a new dated checklist instead of overwriting prior review history.
3. Support append-only rechecks and explicit waiver records.

## Implementation Notes

- Primary surfaces: `templates/commands/checklist.md` and `skills/internal/create-checklist/SKILL.md`.
- Recheck and waiver behavior is covered by current review contract tests.

## Future Evolution Suggestions

- Continue aligning checklist quality dimensions with new artifact types and acceptance gates.

## Related Files

- Feature Index: `.specify/features.md`
- Feature Detail: `.specify/features/003-checklist-command.md`
- Implementation: `templates/commands/checklist.md`, `skills/internal/create-checklist/SKILL.md`
- Specification: none registered for this legacy command row.

## Status Tracking

- **Draft**: Concept defined.
- **Planned**: Specification and design approved.
- **Implemented**: Checklist behavior delivered and verified.
- **Blocked**: A final-path acceptance criterion fails.
- **Ready for Review**: Review evidence complete with no blocking code-review entry.
- **Sealed**: Canonical seal criteria met.
- **Completed** (legacy — current): Historical delivered status retained.
