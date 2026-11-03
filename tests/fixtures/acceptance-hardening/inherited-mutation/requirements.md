<!-- Fixture case: acceptance-hardening/inherited-mutation
     Declarative input for the ownership/premise findings landed by slice 081b. This is not a real feature: it
     describes no work performed in this repository and points at no real feature directory.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set (Slice column: 081b).
     THE MUTATION (two shapes, one reason class), both in plan.md § Inherited Blockers:
       (1) exactly one extracted dependency row is left **undisposed** — Feature 901's `partial` status row has no
           disposition row at all                    ⇒ `inherited-blocker-undisposed: 901:SC-004_status`
       (2) one `inherited` row names a `Carrier` (`SC-002`) that is a deferrable `supporting`-path criterion of
           *this* fixture, which is not an eligible carrier
                                                     ⇒ `inherited-blocker-undisposed: 901:SC-003_status`
     `inherited-clean` is the counter-example: the same dependency side, everything disposed, no reason. -->

# Requirements Specification: Acceptance Fixture — inherited-mutation

**Requirement Branch**: `900-acceptance-fixture-inherited-mutation`
**Created**: 2026-11-03
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -

## Related Feature *(mandatory)*

**Feature ID**: 900
**Feature Name**: Acceptance fixture — inherited-mutation

## Assumptions

**F-1**: This directory is a declarative fixture. Its dependency side (`dependency-feature-901.md` and
`dependency-verification-901.md`) is what the extraction reads; without it the green would prove only that a
judgement fires, never that extraction discovers rows. The defect lives in the dispositions, not in the
dependency.

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

`SC-002` is deliberately a `supporting`-path criterion: it is the criterion one `inherited` row offers as its
`Carrier`, and a deferrable criterion is not eligible, so that row is judged as an undisposed row.
