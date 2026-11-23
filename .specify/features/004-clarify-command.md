# Feature Detail: Clarify Command

**Feature ID**: 004  
**Name**: Clarify Command  
**Description**: Resolve ambiguities in specifications and design artifacts.
**Status**: Completed  
**Created**: 2026-02-10  
**Last Updated**: 2026-11-22

## Overview

`/speckit.clarify` selects the requirements, plan, or tasks target from the current artifact state, scans for underspecified areas, asks a bounded sequence of closed questions, and writes each ratified answer back to the same artifact with validation.

## Latest Review

2026-11-22 implementation audit: the command now delegates to `clarify-artifact` and includes fail-fast writability checks, bounded loops, and escalation to interview for open-ended exploration; only the duplicated-number links required removal.

## Key Changes

1. Resolve the clarification stage from existing requirements, plan, and tasks artifacts.
2. Run a bounded closed-question loop with per-answer writeback and validation.
3. Escalate unbounded or exploratory clarification to the interview flow.

## Implementation Notes

- Primary surfaces: `templates/commands/clarify.md` and `skills/internal/clarify-artifact/SKILL.md`.
- Semantic-completeness and clarification contract tests cover current behavior.

## Future Evolution Suggestions

- Preserve bounded clarification semantics as new artifact classes are introduced.

## Related Files

- Feature Index: `.specify/features.md`
- Feature Detail: `.specify/features/004-clarify-command.md`
- Implementation: `templates/commands/clarify.md`, `skills/internal/clarify-artifact/SKILL.md`
- Specification: none registered for this legacy command row.

## Status Tracking

- **Draft**: Concept defined.
- **Planned**: Specification and design approved.
- **Implemented**: Clarification behavior delivered and verified.
- **Blocked**: A final-path acceptance criterion fails.
- **Ready for Review**: Review evidence complete with no blocking code-review entry.
- **Sealed**: Canonical seal criteria met.
- **Completed** (legacy — current): Historical delivered status retained.
