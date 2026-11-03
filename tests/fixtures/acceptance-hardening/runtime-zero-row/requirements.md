<!-- Fixture case: acceptance-hardening/runtime-zero-row
     Declarative input for the ownership/premise findings landed by slice 081b. This is not a real feature: it
     describes no work performed in this repository and points at no real feature directory.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set (Slice column: 081b).
     THE MUTATION: § Runtime Stack & Dependency Ownership is present with a header row and a separator and
     **zero data rows**. That is V-27's middle shape and it MUST read as `runtime-dependency-not-owned:
     runtime-stack` — not as "this feature has no runtime dependency" (silence), and not as an input error
     (which is the absent-section shape). Everything else is `positive`'s content, in the nine-column shape. -->

# Requirements Specification: Acceptance Fixture — runtime-zero-row

**Requirement Branch**: `900-acceptance-fixture-runtime-zero-row`
**Created**: 2026-11-03
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -

## Related Feature *(mandatory)*

**Feature ID**: 900
**Feature Name**: Acceptance fixture — runtime-zero-row

## Assumptions

**F-1**: This directory is a declarative fixture. Its single defect is the runtime-stack section carrying **zero
data rows**: zero rows is the most complete form of "no table row", so it is a blocking finding and never a
silent pass. The fixture exists because that shape was measured to produce no reason at all before this slice.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The fixture would deliver the runtime capability it consumes, had the table kept the row it drops.
- **FR-002**: The fixture records exactly one smoke command for its main flow.

### Runtime Stack & Dependency Ownership

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|

Zero data rows, header and separator only. The reserved argument `runtime-stack` exists for exactly this shape:
there is no `RS-NNN` to name, and emitting nothing would be the false green the finding was introduced to catch.

## Success Criteria *(mandatory)*

- **SC-001**: The fixture's main flow completes once, end to end. **Path**: final
- **SC-002**: The fixture's hygiene note is recorded alongside the run. **Path**: supporting
