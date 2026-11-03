<!-- Fixture case: acceptance-hardening/mixed-path
     Declarative input for scripts/python/closure-acceptance-check.py. This is not a real feature: it
     describes no work performed in this repository and points at no real feature directory.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set.
     The `final` / `supporting` boundary rule: one `final` SC passes and one `final` SC fails, so the reason is
     a named failing criterion rather than a zero-pass verdict; the lone non-`pass` `supporting` SC produces no
     blocking reason of its own. -->

# Requirements Specification: Acceptance Fixture — mixed path

**Requirement Branch**: `900-acceptance-fixture-mixed-path`
**Created**: 2026-11-03
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -

## Related Feature *(mandatory)*

**Feature ID**: 900
**Feature Name**: Acceptance fixture — mixed path

## Assumptions

**F-1**: This directory is a declarative fixture. It mixes the two path kinds on purpose: the accepting side
must not be read as "all criteria pass", and the supporting side must not be promoted into a blocker.

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
- **SC-002**: The fixture's error path returns the documented failure code. **Path**: final
- **SC-003**: The fixture's hygiene note is recorded alongside the run. **Path**: supporting
