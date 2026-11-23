# Feature Detail: Requirements Command

**Feature ID**: 010  
**Name**: Requirements Command  
**Description**: Define and validate requirements specifications.
**Status**: Completed  
**Created**: 2026-02-10  
**Last Updated**: 2026-11-22

## Overview

`/speckit.requirements` derives a short name and globally next specification number, creates the requirement branch and `requirements.md`, and validates the result with deterministic checks for numbering, structure, references, clarification markers, and success-criterion paths.

## Latest Review

2026-11-22 implementation audit: current scaffolding handles portable branch names, Unicode descriptions, and safe JSON output. The previous generic text and nonexistent duplicated-number links did not describe these delivered behaviors.

## Key Changes

1. Resolve the next specification identifier without colliding with archived or slash-namespaced branches.
2. Scaffold the requirements artifact and create the corresponding branch with portable name handling.
3. Validate requirement structure, references, clarification markers, and final/supporting success-criterion paths.
4. Emit Unicode-safe, correctly escaped JSON for automation.

## Implementation Notes

- Primary surfaces: `templates/commands/requirements.md`, `skills/internal/create-requirements/SKILL.md`, `scripts/bash/create-new-requirements.sh`, and `scripts/python/validate-requirements.py`.
- Current unit and contract tests cover JSON escaping, branch handling, and checker behavior.

## Future Evolution Suggestions

- Keep global number allocation and branch handling aligned with archive and namespace conventions.

## Related Files

- Feature Index: `.specify/features.md`
- Feature Detail: `.specify/features/010-requirements-command.md`
- Implementation: `templates/commands/requirements.md`, `skills/internal/create-requirements/SKILL.md`
- Specification: none registered for this legacy command row.

## Status Tracking

- **Draft**: Concept defined.
- **Planned**: Specification and design approved.
- **Implemented**: Requirements workflow delivered and verified.
- **Blocked**: A final-path acceptance criterion fails.
- **Ready for Review**: Review evidence complete with no blocking code-review entry.
- **Sealed**: Canonical seal criteria met.
- **Completed** (legacy — current): Historical delivered status retained.
