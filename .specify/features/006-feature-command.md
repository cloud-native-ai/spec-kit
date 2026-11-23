# Feature Detail: Feature Command

**Feature ID**: 006  
**Name**: Feature Command  
**Description**: Manage feature lifecycle and metadata.  
**Status**: Completed  
**Created**: 2026-02-10  
**Last Updated**: 2026-11-22

## Overview

`/speckit.feature` reconciles the feature index, per-feature detail files, and the README feature summary against repository reality. It supports full-registry reconciliation, commit or branch context mining, and single-target convergence.

## Latest Review

2026-11-22 implementation audit: the command delegates all registry work to `manage-features`; its current reconcile model includes a tolerance band, archive-not-delete, status-regression protection, sequential identifier allocation, derived counts, and residual reporting.

## Key Changes

1. Reconcile functional and non-functional feature records with current implementation evidence.
2. Preserve unchanged rows and historical records while refusing unapproved status regressions.
3. Maintain detail files, the feature index, README summary, and derived feature count together.

## Implementation Notes

- Primary surfaces: `templates/commands/feature.md` and `skills/internal/manage-features/SKILL.md`.
- Registry count and acceptance-state behavior are covered by existing contract tests.

## Future Evolution Suggestions

- Keep implementation-evidence extraction deterministic and avoid using historical status prose as proof of delivery.

## Related Files

- Feature Index: `.specify/features.md`
- Feature Detail: `.specify/features/006-feature-command.md`
- Implementation: `templates/commands/feature.md`, `skills/internal/manage-features/SKILL.md`
- Specification: none registered for this legacy command row.

## Status Tracking

- **Draft**: Concept defined.
- **Planned**: Specification and design approved.
- **Implemented**: Registry workflow delivered and verified.
- **Blocked**: A final-path acceptance criterion fails.
- **Ready for Review**: Review evidence complete with no blocking code-review entry.
- **Sealed**: Canonical seal criteria met.
- **Completed** (legacy — current): Historical delivered status retained.
