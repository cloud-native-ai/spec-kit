<!-- Fixture case: acceptance-hardening/review-implemented-clean
     Declarative input for scripts/python/closure-acceptance-check.py. This is not a real feature: it
     describes no work performed in this repository and points at no real feature directory.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set. -->

# Requirements Specification: Acceptance Fixture — review-implemented-clean

**Requirement Branch**: `900-acceptance-fixture-review-implemented-clean`
**Created**: 2026-11-03
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -

## Related Feature *(mandatory)*

**Feature ID**: 900
**Feature Name**: Acceptance fixture — review-implemented-clean

## Assumptions

**F-1**: This directory is a declarative fixture. Every `execution`-class shape rule holds here on purpose, so
the fixture is the counter-example to over-blocking: a feature whose `final`-path criteria pass and whose smoke
record is complete MUST NOT be refused.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The fixture delivers the runtime capability it consumes, so its runtime-stack row is `in-scope`.
- **FR-002**: The fixture records exactly one smoke command for its main flow.

### Runtime Stack & Dependency Ownership

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | fixture runtime capability | in-scope | this fixture | `900` fixture commit | — | `verification.md` carries the joint-acceptance row naming `RS-001` | FR-001 | EP-001 |

The fixture also mentions RS-004 inside narrative prose, deliberately without the declaration
marker: an id inside a sentence is not a declaration, so the prose rule MUST NOT fire on it. This
is the exclusion arm on the accepting side — `runtime-gap-mutation` proves the same arm beside a
real defect.

## Success Criteria *(mandatory)*

- **SC-001**: The fixture's main flow completes once, end to end. **Path**: final
- **SC-002**: The fixture's hygiene note is recorded alongside the run. **Path**: supporting
