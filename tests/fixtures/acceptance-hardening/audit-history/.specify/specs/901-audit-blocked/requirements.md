<!-- Fixture case: acceptance-hardening/audit-history/901-audit-blocked
     Declarative input for scripts/python/closure-acceptance-check.py --audit-existing. This is not
     a real feature: it describes no work performed in this repository and points at no real
     feature directory.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set.
     The 026 shape with the claim left standing: tasks closed, a status row per SC, every
     `final`-path criterion non-`pass`, no smoke record — the feature the audit reports as one that
     would become `Blocked` under the new rules. -->

# Requirements Specification: Acceptance Fixture — audit blocked

**Requirement Branch**: `901-acceptance-fixture-audit-blocked`
**Created**: 2026-11-03
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -

## Related Feature *(mandatory)*

**Feature ID**: 901
**Feature Name**: Acceptance fixture — audit blocked

## Assumptions

**F-1**: This directory is a declarative fixture and one of the audit-history case's two subjects.
It reproduces the shape the pre-081 bar accepted: the bookkeeping is complete and the main journey
never ran. Under the new rules its claim exceeds its evidence, so `--audit-existing` reports it.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The fixture delivers the runtime capability it consumes, so its runtime-stack row is `in-scope`.
- **FR-002**: The fixture records exactly one smoke command for its main flow.

### Runtime Stack & Dependency Ownership

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | fixture runtime capability | in-scope | this fixture | `901` fixture commit | — | `verification.md` carries the joint-acceptance row naming `RS-001` | FR-001 | EP-001 |

## Success Criteria *(mandatory)*

- **SC-001**: The fixture's main flow completes once, end to end. **Path**: final
- **SC-002**: The fixture's error path is exercised once. **Path**: final
