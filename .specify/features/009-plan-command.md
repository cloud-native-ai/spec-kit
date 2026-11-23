# Feature Detail: Plan Command

**Feature ID**: 009  
**Name**: Plan Command  
**Description**: Create implementation plans and design artifacts from requirements.
**Status**: Completed  
**Created**: 2026-02-10  
**Last Updated**: 2026-11-22

## Overview

`/speckit.plan` turns a validated requirements specification into `plan.md` and the Phase 1 design set: research, data model, contracts, quickstart, and feature-reference mapping. Planning includes a dynamic Constitution Check and artifact-completeness gates.

## Latest Review

2026-11-22 implementation audit: the current `create-plan` flow includes decision-tension records, execution-premise checks, and scaffold safeguards. `create-new-plan.sh` now refuses a missing or empty plan template instead of touching `plan.md`.

## Key Changes

1. Fill the plan template from validated requirements and project governance.
2. Generate the Phase 1 design artifacts and requirement-to-delivery mapping.
3. Enforce dynamic Constitution Check, decomposition, and artifact-completeness gates.
4. Fail before modification when the source plan template is missing or empty.

## Implementation Notes

- Primary surfaces: `templates/commands/plan.md`, `skills/internal/create-plan/SKILL.md`, and `scripts/bash/create-new-plan.sh`.
- The audit found one `plan.md` handoff entry missing `send`; this is a current metadata residual.

## Future Evolution Suggestions

- Repair the incomplete handoff entry while preserving the planning workflow contract.

## Related Files

- Feature Index: `.specify/features.md`
- Feature Detail: `.specify/features/009-plan-command.md`
- Implementation: `templates/commands/plan.md`, `skills/internal/create-plan/SKILL.md`
- Specification: none registered for this legacy command row.

## Status Tracking

- **Draft**: Concept defined.
- **Planned**: Specification and design approved.
- **Implemented**: Planning workflow delivered and verified.
- **Blocked**: A final-path acceptance criterion fails.
- **Ready for Review**: Review evidence complete with no blocking code-review entry.
- **Sealed**: Canonical seal criteria met.
- **Completed** (legacy — current): Historical delivered status retained.
