# Feature Detail: Unify Command Handoffs

**Feature ID**: 001  
**Name**: Unify Command Handoffs  
**Description**: Declare command prerequisites and next steps through template handoffs.
**Status**: Completed
**Created**: 2026-02-10  
**Last Updated**: 2026-11-22

## Overview

The command templates carry handoff metadata and, for most commands, a `## Handoffs` body that names prerequisites and follow-up commands. Generated per-tool copies inherit this structure, and the quickstart documents part of the command relationship graph.

## Latest Review

2026-11-22 implementation audit: coverage is partial, not uniform. Thirty of 32 command templates have a `## Handoffs` body (`measure.md` and `status.md` do not), 21 have frontmatter `handoffs`, and the quickstart relationship table covers 15 of 32 commands. The legacy `Completed` status is retained because a status regression requires an explicit user decision; the measured coverage gap is recorded here and in the index.

## Key Changes

1. Add structured handoff metadata and body sections to command templates.
2. Propagate handoffs through generated per-tool command copies.
3. Document command sequencing in the quickstart and link the feature to its actual specification.

## Implementation Notes

- Primary surfaces: `templates/commands/`, `docs/tutorials/quickstart.md`, and generated host command directories.
- The audit also found malformed handoff YAML in several templates and a `plan.md` handoff missing `send`; these are implementation residuals, not hidden by the legacy status.

## Future Evolution Suggestions

- Close the `measure` / `status` body gap and the remaining quickstart relationships.
- Repair malformed handoff metadata and decide explicitly whether the legacy status should change.

## Related Files

- Feature Index: `.specify/features.md`
- Feature Detail: `.specify/features/001-unify-command-handoffs.md`
- Specification: `.specify/specs/001-unify-command-handoffs/requirements.md`
- Quality Checklist: `.specify/specs/001-unify-command-handoffs/checklists/requirements.md`

## Status Tracking

- **Draft**: Concept defined.
- **Planned**: Specification and design approved.
- **Implemented**: Handoff behavior delivered and verified.
- **Blocked**: A final-path acceptance criterion fails.
- **Ready for Review**: Review evidence complete with no blocking code-review entry.
- **Sealed**: Canonical seal criteria met.
- **Completed** (legacy — current): Historical delivered status retained while the 2026-11-22 partial-coverage audit awaits an explicit status decision.
