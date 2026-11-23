# Feature Detail: Review Command

**Feature ID**: 012  
**Name**: Review Command  
**Description**: Review process, artifacts, implementation, and code with acceptance reality checks.
**Status**: Completed  
**Created**: 2026-02-10  
**Last Updated**: 2026-11-22

## Overview

`/speckit.review` runs four review segments—process, artifact, implementation, and code—then performs an Acceptance Reality Check against the feature's recorded success criteria. Code review produces non-interactive records, coverage receipts, and explicit applicability verdicts.

## Latest Review

2026-11-22 implementation audit: the current review flow combines the four segments with deterministic `accept` / `block` acceptance results and final-path counts. The previous generic rule-review text and duplicated-number links were stale.

## Key Changes

1. Review the SDD process and expected artifact set for completeness and traceability.
2. Verify implementation evidence and execute a non-interactive code-review segment.
3. Run the Acceptance Reality Check and report agreement or disagreement with the claimed status.
4. Apply the canonical review gate before any status transition.

## Implementation Notes

- Primary surfaces: `templates/commands/review.md`, `skills/internal/review-sdd-process/`, `skills/internal/code-review/`, and `scripts/python/closure-acceptance-check.py`.
- Related later extensions are registered as Features 071 and 081 rather than as this legacy row's specification.

## Future Evolution Suggestions

- Preserve explicit not-evaluated and not-applicable verdicts as review coverage evolves.

## Related Files

- Feature Index: `.specify/features.md`
- Feature Detail: `.specify/features/012-review-command.md`
- Implementation: `templates/commands/review.md`, `skills/internal/code-review/SKILL.md`
- Related Specifications: `.specify/specs/071-review-code-integration/requirements.md`, `.specify/specs/081-acceptance-hardening/requirements.md`

## Status Tracking

- **Draft**: Concept defined.
- **Planned**: Specification and design approved.
- **Implemented**: Review workflow delivered and verified.
- **Blocked**: A final-path acceptance criterion fails.
- **Ready for Review**: Review evidence complete with no blocking code-review entry.
- **Sealed**: Canonical seal criteria met.
- **Completed** (legacy — current): Historical delivered status retained.
