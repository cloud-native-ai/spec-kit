<!-- Fixture case: acceptance-hardening/inherited-clean — see requirements.md for the fixture notice.
     Shape owner: .specify/specs/081-acceptance-hardening/data-model.md § Fixture set.
     Every extracted row is disposed: two `resolved`, one `not-applicable`, two `inherited` (one `task:…+test:…`
     carrier, one `gate:…` carrier) and one `inherited-later`. No reason may be emitted from this table. -->

# Implementation Plan: Acceptance Fixture — inherited-clean

**Requirement Branch**: `900-acceptance-fixture-inherited-clean`

## Execution Premises

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | The fixture's runtime capability is available to it inside the fixture. | fixture-local: no external probe, no network | verified | — |

## Inherited Blockers

**Dependency set (declared, never implied)** — in: Feature 901. Its detail is `dependency-feature-901.md` and its
verification log is `dependency-verification-901.md`, both inside this fixture directory. Out with reason: the
fixture depends on no other feature, so no further record can be inherited.

**Extraction reading**: Feature 901's closed three sources yield **six** rows — the two `## Deferred` bullets,
the three `verification.md` status rows in `blocked` / `deferred` / `partial`, and the non-empty `deferred_tasks=`
list. The `Source row` cell is the join key and is reproduced verbatim; all six are disposed below.

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|
| IB-001 | `901:deferred:warm-pool-sizing` | resolved | — | — | the dependency's fixed pool size was measured to carry this fixture's load; `verification.md` `SC-001` records the single-pool run at exit 0 |
| IB-002 | `901:deferred:retry-budget` | not-applicable | — | — | this fixture issues no retried call, so a tunable budget would measure nothing it consumes |
| IB-003 | `901:SC-002_status` | inherited | `task:T004+test:tests/contract/test_acceptance_premises.py` | `this-slice` | the dependency could not measure its own journey; this fixture inherits the measurement in T004 and asserts it in its test module |
| IB-004 | `901:SC-003_status` | inherited | `gate:GATE-1` | `this-slice` | the dependency's error path is re-judged by this fixture's completion gate, which runs the single test carrier |
| IB-005 | `901:SC-004_status` | resolved | — | — | the dependency's remaining matrix rows were measured under this fixture; nothing remains partial to inherit |
| IB-006 | `901:deferred_tasks` | inherited | `test:tests/contract/test_acceptance_review_composition.py` | `081c` | reads **`inherited-later`**: the carrier module belongs to slice `081c` (listed in § D10 below), so the task id MUST NOT be written yet — the row is disclosed, neither blocking nor resolved, and is re-read at `081c`'s closure |

## D10 — Slice decomposition

The declared slice table. A `Carrier slice` naming a later slice is legal only while the feature is `Blocked` and
the slice appears here; `inherited-clean` is the fixture that exercises it.

| Slice | Scope | Depends on |
|-------|-------|------------|
| `081b` | this fixture's own slice — the dispositions above are read here | — |
| `081c` | the fixture's later slice, named by an `inherited-later` row's `Carrier slice` | `081b` |
