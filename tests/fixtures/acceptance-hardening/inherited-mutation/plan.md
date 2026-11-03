<!-- Fixture case: acceptance-hardening/inherited-mutation — see requirements.md for the fixture notice.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set.
     THE MUTATION lives in the table below: one extracted row carries no disposition row (numbered `IB-005` is
     absent on purpose, so the gap is legible), and one `inherited` row's `Carrier` names a deferrable
     `supporting`-path criterion. Every other row is disposed cleanly, so the two reasons are attributable. -->

# Implementation Plan: Acceptance Fixture — inherited-mutation

**Requirement Branch**: `900-acceptance-fixture-inherited-mutation`

## Execution Premises

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | The fixture's runtime capability is available to it inside the fixture. | fixture-local: no external probe, no network | verified | — |

## Inherited Blockers

**Dependency set** — in: Feature 901, inside this fixture directory. Out with reason: the fixture depends on no
other feature, so no further record can be inherited.

**Dependency artifacts (declared, never implied)** — the checker reads only the paths in this block:
- `dependency-feature-901.md` — Feature 901's detail
- `dependency-verification-901.md` — Feature 901's verification log

**Extraction reading**: Feature 901's closed three sources yield **six** rows — the two `## Deferred` bullets,
the three `verification.md` status rows in `blocked` / `deferred` / `partial`, and the non-empty `deferred_tasks=`
list. The `Source row` cell is the join key and is reproduced verbatim.

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|
| IB-001 | `901:deferred:warm-pool-sizing` | resolved | — | — | the dependency's fixed pool size was measured to carry this fixture's load; `verification.md` `SC-001` records the single-pool run at exit 0 |
| IB-002 | `901:deferred:retry-budget` | not-applicable | — | — | this fixture issues no retried call, so a tunable budget would measure nothing it consumes |
| IB-003 | `901:SC-002_status` | inherited | `task:T004+test:tests/contract/test_acceptance_premises.py` | `this-slice` | the dependency could not measure its own journey; this fixture inherits the measurement in T004 and asserts it in its test module |
| IB-004 | `901:SC-003_status` | inherited | `SC-002` | `this-slice` | **ineligible carrier**: `SC-002` is a `supporting`-path criterion and can be `deferred`, so it is not a carrier — judged exactly as an undisposed row, under the same reason |
| IB-006 | `901:deferred_tasks` | resolved | — | — | the dependency's two deferred task rows were re-run under this fixture and both closed; no work remains to inherit |

**Disclosure of the omission**: the sixth extracted row — Feature 901's `partial` status row — has **no
disposition row at all**. That is the "undisposed" shape this mutation proves, so it is deliberately absent rather
than written with an empty `Disposition` cell (which would be a different defect).

## D10 — Slice decomposition

The declared slice table. A `Carrier slice` naming a later slice is legal only while the feature is `Blocked` and
the slice appears here; `inherited-clean` is the fixture that exercises it.

| Slice | Scope | Depends on |
|-------|-------|------------|
| `081b` | this fixture's own slice — the dispositions above are read here | — |
| `081c` | the fixture's later slice, named by an `inherited-later` row's `Carrier slice` | `081b` |
