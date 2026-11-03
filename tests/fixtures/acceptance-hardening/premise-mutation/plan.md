<!-- Fixture case: acceptance-hardening/premise-mutation — see requirements.md for the fixture notice.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set.
     THE MUTATION: `EP-001` is `falsified` and its `Decision` cell is empty. The expected finding is
     `falsified-premise-undecided: EP-001`. The row is present, so a finding about a missing row is NOT the
     defect being proved here. -->

# Implementation Plan: Acceptance Fixture — premise-mutation

**Requirement Branch**: `900-acceptance-fixture-premise-mutation`

## Execution Premises

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | The fixture's runtime capability is available to it inside the fixture. | fixture-local: no external probe, no network | falsified |  |

## Inherited Blockers

Dependency set: none — the fixture depends on no other feature, so nothing can be inherited. The table still
carries one `not-applicable` row, so the row shape is exercised instead of the section standing empty.

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|
| IB-001 | (none) | not-applicable | — | — | the fixture has no dependency feature, so no inherited record exists to dispose |
