<!-- Fixture case: acceptance-hardening/smoke-mutation
     Declarative input for scripts/python/closure-acceptance-check.py. This is not a real feature: it
     describes no work performed in this repository and points at no real feature directory.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set.
     The mutation, relative to `positive`: the smoke record is deleted AND the claimed status is
     `Implemented`. Every `final`-path SC still passes, so `zero-final-path-pass` cannot fire here — this is
     the one fixture that exercises the claimed-but-not-accepted reason. -->

# Requirements Specification: Acceptance Fixture — smoke mutation

**Requirement Branch**: `900-acceptance-fixture-smoke-mutation`
**Created**: 2026-11-03
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -

## Related Feature *(mandatory)*

**Feature ID**: 900
**Feature Name**: Acceptance fixture — smoke mutation

## Assumptions

**F-1**: This directory is a declarative fixture. Its single defect is completion condition ④: the feature
claims `Implemented` while its smoke record — the evidence that the main flow was ever driven — is gone.

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
- **SC-002**: The fixture's hygiene note is recorded alongside the run. **Path**: supporting
