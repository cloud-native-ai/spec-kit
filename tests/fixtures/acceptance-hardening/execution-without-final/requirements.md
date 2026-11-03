<!-- Fixture case: acceptance-hardening/execution-without-final
     Declarative input for scripts/python/closure-acceptance-check.py. This is not a real feature: it
     describes no work performed in this repository and points at no real feature directory.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set.
     An `execution`-class feature whose criteria are all `supporting`: the `final >= 1` floor is violated, so
     `final_path.total = 0` and the zero-pass verdict applies. The same shape MUST fail the requirements
     validator's `path-marker` check. -->

# Requirements Specification: Acceptance Fixture — execution without a final path

**Requirement Branch**: `900-acceptance-fixture-execution-without-final`
**Created**: 2026-11-03
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -

## Related Feature *(mandatory)*

**Feature ID**: 900
**Feature Name**: Acceptance fixture — execution without a final path

## Assumptions

**F-1**: This directory is a declarative fixture. Its single defect is structural: an `execution` feature
declares no `final`-path criterion, so it has no criterion that can make it acceptable however honest its
`supporting` rows are.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The fixture delivers the runtime capability it consumes, so its runtime-stack row is `in-scope`.
- **FR-002**: The fixture records exactly one smoke command for its main flow.

### Runtime Stack & Dependency Ownership

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | fixture runtime capability | in-scope | this fixture | `900` fixture commit | — | `verification.md` carries the joint-acceptance row naming `RS-001` | FR-001 | EP-001 |

## Success Criteria *(mandatory)*

- **SC-001**: The fixture's helper script parses its own arguments. **Path**: supporting
- **SC-002**: The fixture's helper script is covered by a unit test. **Path**: supporting
