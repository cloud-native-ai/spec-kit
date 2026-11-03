<!-- Fixture case: acceptance-hardening/runtime-gap-mutation
     Declarative input for the ownership/premise findings landed by slice 081b. This is not a real feature: it
     describes no work performed in this repository and points at no real feature directory.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set (Slice column: 081b).
     THE MUTATION — two shapes, one reason class:
       (1) one capability is declared **only as prose**, with the declaration marker and the id `RS-905`, and has
           no table row            ⇒ `runtime-dependency-not-owned: RS-905`
       (2) one `signed-contract` row leaves the `Pin` **and** the `Contract` cell empty
                                   ⇒ `runtime-dependency-not-owned: RS-001`
     THE EXCLUSION ARMS (both MUST NOT fire — they are what makes "prose" decidable instead of a judgement):
       (a) a narrative line that mentions `RS-904` without the declaration marker;
       (b) a marker-shaped line that lives inside a fenced code block, carrying `RS-906`. -->

# Requirements Specification: Acceptance Fixture — runtime-gap-mutation

**Requirement Branch**: `900-acceptance-fixture-runtime-gap-mutation`
**Created**: 2026-11-03
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -

## Related Feature *(mandatory)*

**Feature ID**: 900
**Feature Name**: Acceptance fixture — runtime-gap-mutation

## Assumptions

**F-1**: This directory is a declarative fixture carrying two runtime-row defects and two exclusion arms at once,
because both defects share one reason class and both exclusions share one marker rule. The declared-but-rowless
capability is `RS-905`; the incomplete `signed-contract` row is `RS-001`.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The fixture consumes a runtime capability supplied outside it, so its row is `signed-contract`.
- **FR-002**: The fixture records exactly one smoke command for its main flow.

### Runtime Stack & Dependency Ownership

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | an externally supplied runtime capability | signed-contract | a provider outside this fixture |  |  | the provider and this fixture accept it jointly | FR-001 | EP-001 |

- **Runtime dependency**: an external capability this fixture consumes — RS-905

The fixture also mentions RS-904 inside narrative prose, without the declaration marker, on purpose: the marker
is what makes the prose rule decidable, so an id inside a sentence is not a declaration and MUST NOT fire.

```text
- **Runtime dependency**: a marker-shaped line that lives inside a fenced code block — RS-906
```

The fenced block above is the code-block exclusion arm: fenced code blocks are removed before the marker rule is
applied, so `RS-906` MUST NOT fire either.

## Success Criteria *(mandatory)*

- **SC-001**: The fixture's main flow completes once, end to end. **Path**: final
- **SC-002**: The fixture's hygiene note is recorded alongside the run. **Path**: supporting
