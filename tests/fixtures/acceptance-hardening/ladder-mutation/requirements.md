<!-- Fixture case: acceptance-hardening/ladder-mutation
     Declarative input for scripts/python/closure-acceptance-check.py. This is not a real feature: it
     describes no work performed in this repository and points at no real feature directory.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set.
     The mutation: a `blocked` row carries all five ladder fields, but `SC-001_reduced_measurement` is
     non-empty while `SC-001_reduced_measurement_run=no` — the illegal row (data-model V-6). -->

# Requirements Specification: Acceptance Fixture — ladder mutation

**Requirement Branch**: `900-acceptance-fixture-ladder-mutation`
**Created**: 2026-11-03
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -

## Related Feature *(mandatory)*

**Feature ID**: 900
**Feature Name**: Acceptance fixture — ladder mutation

## Assumptions

**F-1**: This directory is a declarative fixture. Its single defect is the illegal measurement-ladder row:
a reduced measurement is written down but never run, and honesty is not an accepted substitute for running it.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The fixture delivers the runtime capability it consumes, so its runtime-stack row is `in-scope`.
- **FR-002**: The fixture records exactly one smoke command for its main flow.

### Runtime Stack & Dependency Ownership

| ID | Capability | Form | Owner | Pin | Joint acceptance | FR |
|----|------------|------|-------|-----|------------------|-----|
| RS-001 | fixture runtime capability | in-scope | this fixture | `900` fixture commit | `verification.md` carries the joint-acceptance row naming `RS-001` | FR-001 |

## Success Criteria *(mandatory)*

- **SC-001**: The fixture's main flow completes once, end to end. **Path**: final
