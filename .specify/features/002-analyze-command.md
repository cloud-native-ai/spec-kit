# Feature Detail: Analyze Command

**Feature ID**: 002  
**Name**: Analyze Command  
**Description**: Perform read-only cross-artifact consistency, coverage, and constitution-alignment analysis.
**Status**: Completed  
**Created**: 2026-02-10  
**Last Updated**: 2026-11-22

## Overview

`/speckit.analyze` evaluates requirements, plans, tasks, checklists, and feature metadata before implementation. It checks consistency and coverage, delegates independent validation of serious findings, and reports actionable gaps instead of modifying the artifacts it analyzes.

## Latest Review

2026-11-22 implementation audit: the current implementation is an artifact-analysis gate, not a generic project or code-structure analyzer. The previous description and duplicated-number specification links were stale.

## Key Changes

1. Delegate execution to `analyze-artifacts` for bounded, read-only consistency passes.
2. Measure clause and requirement coverage with deterministic programs.
3. Independently validate CRITICAL/HIGH findings and preserve rejected findings separately from confirmed ones.

## Implementation Notes

- Primary surfaces: `templates/commands/analyze.md`, `skills/internal/analyze-artifacts/SKILL.md`, and `scripts/python/account-clause-coverage.py`.
- Current behavior is pinned by clause-coverage and review contract tests.

## Future Evolution Suggestions

- Keep artifact checks aligned with newly introduced schema owners and lifecycle states.

## Related Files

- Feature Index: `.specify/features.md`
- Feature Detail: `.specify/features/002-analyze-command.md`
- Implementation: `templates/commands/analyze.md`, `skills/internal/analyze-artifacts/SKILL.md`
- Specification: none registered for this legacy command row.

## Status Tracking

- **Draft**: Concept defined.
- **Planned**: Specification and design approved.
- **Implemented**: Analysis behavior delivered and verified.
- **Blocked**: A final-path acceptance criterion fails.
- **Ready for Review**: Review evidence complete with no blocking code-review entry.
- **Sealed**: Canonical seal criteria met.
- **Completed** (legacy — current): Historical delivered status retained.
