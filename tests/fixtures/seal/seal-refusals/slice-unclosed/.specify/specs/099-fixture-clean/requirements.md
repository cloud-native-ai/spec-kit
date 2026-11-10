<!-- Fixture case: seal/seal-refusals/slice-unclosed — a clean single spec for the `seal` action.
     This is not a real feature: it describes no work performed in this repository and
     points at no real feature directory. Shape owner: `.specify/specs/099-speckit-seal/`
     data-model.md § 3 and the closure checker's accepted-input shape. -->

# Requirements Specification: Seal Fixture — clean single spec

**Requirement Branch**: `099-fixture-clean`
**Created**: 2026-11-11
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -

## Related Feature *(mandatory)*

**Feature ID**: 099
**Feature Name**: Seal fixture — clean single spec

## Assumptions

**F-1**: This directory is a declarative fixture. Every `execution`-class shape rule holds
here on purpose, so the fixture is the accepting side of the `seal` action.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The fixture delivers the runtime capability it consumes, so its runtime-stack row is `in-scope`.
- **FR-002**: The fixture records exactly one smoke command for its main flow.

### Runtime Stack & Dependency Ownership

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | fixture runtime capability | in-scope | this fixture | `099` fixture commit | — | `verification.md` carries the joint-acceptance row naming `RS-001` | FR-001 | EP-001 |

## Success Criteria *(mandatory)*

- **SC-001**: The fixture's main flow completes once, end to end. **Path**: final
- **SC-002**: The fixture's hygiene note is recorded alongside the run. **Path**: supporting
