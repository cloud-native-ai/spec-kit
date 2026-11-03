<!-- Fixture case: acceptance-hardening/negative
     Declarative input for scripts/python/closure-acceptance-check.py. This is not a real feature: it
     describes no work performed in this repository and points at no real feature directory.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set.
     The 026 shape: tasks are all closed, every SC has a status row, and every `final`-path SC is
     `blocked` or `deferred` — the state that used to be readable as `Implemented`. -->

# Requirements Specification: Acceptance Fixture — negative

**Requirement Branch**: `900-acceptance-fixture-negative`
**Created**: 2026-11-03
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -

## Related Feature *(mandatory)*

**Feature ID**: 900
**Feature Name**: Acceptance fixture — negative

## Assumptions

**F-1**: This directory is a declarative fixture. It reproduces the 026 shape so the checker has a
counter-example: the honest-looking state (zero open tasks, a status row per SC) that nevertheless never drove
the feature's main journey. The `final`-path rule MUST refuse it.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The fixture delivers the runtime capability it consumes, so its runtime-stack row is `in-scope`.
- **FR-002**: The fixture records exactly one smoke command for its main flow.

### Runtime Stack & Dependency Ownership

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | fixture runtime capability | in-scope | this fixture | `900` fixture commit | — | `verification.md` carries the joint-acceptance row naming `RS-001` | FR-001 | EP-001 |

## Success Criteria *(mandatory)*

- **SC-001**: The fixture's main flow completes once, end to end. **Path**: final
- **SC-002**: The fixture's error path is exercised once. **Path**: final
