<!-- Fixture case: acceptance-hardening/audit-history/902-audit-clean
     Declarative input for scripts/python/closure-acceptance-check.py --audit-existing. This is not
     a real feature: it describes no work performed in this repository and points at no real
     feature directory.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set.
     The complete shape with the claim already earned: every `final`-path criterion `pass`, a
     complete smoke record — the audit's unaffected subject, judged `accept` and reported as not
     affected. -->

# Requirements Specification: Acceptance Fixture — audit clean

**Requirement Branch**: `902-acceptance-fixture-audit-clean`
**Created**: 2026-11-03
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -

## Related Feature *(mandatory)*

**Feature ID**: 902
**Feature Name**: Acceptance fixture — audit clean

## Assumptions

**F-1**: This directory is a declarative fixture and one of the audit-history case's two subjects.
It carries the evidence the 081 rules demand, so the audit judges it `accept` — proving the mode
reports only the features whose claim exceeds their evidence, not every `Implemented` row it
enumerates.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The fixture delivers the runtime capability it consumes, so its runtime-stack row is `in-scope`.
- **FR-002**: The fixture records exactly one smoke command for its main flow.

### Runtime Stack & Dependency Ownership

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | fixture runtime capability | in-scope | this fixture | `902` fixture commit | — | `verification.md` carries the joint-acceptance row naming `RS-001` | FR-001 | EP-001 |

## Success Criteria *(mandatory)*

- **SC-001**: The fixture's main flow completes once, end to end. **Path**: final
- **SC-002**: The fixture's hygiene note is recorded alongside the run. **Path**: supporting
