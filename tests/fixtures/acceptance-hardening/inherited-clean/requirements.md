<!-- Fixture case: acceptance-hardening/inherited-clean
     Declarative input for the ownership/premise findings landed by slice 081b. This is not a real feature: it
     describes no work performed in this repository and points at no real feature directory.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set (Slice column: 081b).
     THE COUNTER-EXAMPLE: the dependency side is the same as `inherited-mutation`'s, and every extracted row
     is disposed — so this fixture MUST be accepted with **no** inherited reason. That is what proves the
     extraction branch discovers rows instead of merely judging row sets it was handed.
     One row reads `inherited-later` (`Carrier slice` = `081c`, `Carrier` = `test:<path>` alone): disclosed,
     neither blocking nor resolved. The claimed status is `Blocked`, which is what makes that reading legal. -->

# Requirements Specification: Acceptance Fixture — inherited-clean

**Requirement Branch**: `900-acceptance-fixture-inherited-clean`
**Created**: 2026-11-03
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -

## Related Feature *(mandatory)*

**Feature ID**: 900
**Feature Name**: Acceptance fixture — inherited-clean

## Assumptions

**F-1**: This directory is a declarative fixture, and it is the counter-example to `inherited-mutation`: same
dependency side, every extracted row disposed. Without this half the extraction branch could pass by never being
fed. Its single non-blocking reading is one `inherited-later` row, which MUST NOT be counted as undisposed and
MUST NOT be counted as resolved.

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

`SC-002` is a `supporting`-path criterion, as in `inherited-mutation`; this fixture never offers it as a `Carrier`,
so the eligibility rule is proved on the other half of the pair.
