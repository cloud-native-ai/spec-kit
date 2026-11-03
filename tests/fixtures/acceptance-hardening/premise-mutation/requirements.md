<!-- Fixture case: acceptance-hardening/premise-mutation
     Declarative input for the ownership/premise findings landed by slice 081b. This is not a real feature: it
     describes no work performed in this repository and points at no real feature directory.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set (Slice column: 081b).
     Shape note: the runtime-stack table carries the nine-column set — `Contract` and `Premises` are their own
     cells — that the owner document's § Runtime Stack & Dependency Ownership defines; `positive`/`negative`
     predate those two cells, so this fixture repeats their content in the current shape. -->

# Requirements Specification: Acceptance Fixture — premise-mutation

**Requirement Branch**: `900-acceptance-fixture-premise-mutation`
**Created**: 2026-11-03
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -

## Related Feature *(mandatory)*

**Feature ID**: 900
**Feature Name**: Acceptance fixture — premise-mutation

## Assumptions

**F-1**: This directory is a declarative fixture. Its **single** defect lives in `plan.md`: `EP-001` carries
`Status` = `falsified` with its `Decision` **cell emptied**, and the row itself is left in place. "Emptied", not
"deleted", is deliberate — the emitted reason must be attributable to a missing decision, never to a missing
row. Every other artifact is a complete, otherwise-accepting shape, so the reason set can be attributed to that
one emptied cell.

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
- **SC-002**: The fixture's hygiene note is recorded alongside the run. **Path**: supporting
