<!-- Fixture case: acceptance-hardening/audit-history/901-audit-blocked — see requirements.md for
     the fixture notice. Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set. -->

# Implementation Plan: Acceptance Fixture — audit blocked

**Requirement Branch**: `901-acceptance-fixture-audit-blocked`

## Execution Premises

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | The fixture's runtime capability is available to it inside the fixture. | fixture-local: no external probe, no network | verified | — |

## Inherited Blockers

Dependency set: none — the fixture depends on no other feature, so nothing can be inherited. The table still
carries one `not-applicable` row, so the row shape is exercised instead of the section standing empty.

| # | Source row | Disposition | Carrier (MUST be filled when `inherited`) | Evidence / note |
|---|-----------|-------------|------------------------------------------|-----------------|
| IB-001 | (none) | not-applicable | — | the fixture has no dependency feature, so no inherited record exists to dispose |
