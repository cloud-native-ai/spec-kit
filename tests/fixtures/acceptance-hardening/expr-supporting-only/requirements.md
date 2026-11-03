<!-- Fixture case: acceptance-hardening/expr-supporting-only
     Declarative input for scripts/python/closure-acceptance-check.py. This is not a real feature: it
     describes no work performed in this repository and points at no real feature directory.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set.
     An `expression`-class feature whose criteria are all `supporting`: the `final`-path rule is vacuous here,
     so the fixture MUST NOT be forced to invent a `final` SC and MUST NOT be permanently refused because of
     the absence of one. -->

# Requirements Specification: Acceptance Fixture — expression, supporting only

**Requirement Branch**: `900-acceptance-fixture-expr-supporting-only`
**Created**: 2026-11-03
**Status**: Draft
**Flow Class**: expression
**Flow Type**: document

## Related Feature *(mandatory)*

**Feature ID**: 900
**Feature Name**: Acceptance fixture — expression, supporting only

## Assumptions

**F-1**: This directory is a declarative fixture. The class is declared, not inferred: `expression` features
are exempt from the `final ≥ 1` floor, and the exemption is mechanical — it is read from the declared class.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The fixture's only deliverable is a written note, so it consumes no runtime capability.

### Runtime Stack & Dependency Ownership

An `expression`-class feature may record `not-required` with a stated reason instead of an owned capability.

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | runtime capability | not-required | — | — | — | — | — | — |

Reason: the fixture delivers prose only; it runs nothing and therefore owns no runtime capability.

## Success Criteria *(mandatory)*

- **SC-001**: The fixture's note states the rule it illustrates. **Path**: supporting
- **SC-002**: The fixture's note is cross-checked against its own examples. **Path**: supporting
