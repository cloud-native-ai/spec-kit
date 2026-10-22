# Failure Triage — 067-loop-efficiency-hardening (baseline 2026-10-22)

**Owner of triage rows**: this file (schema: `data-model.md` E5; mechanics: `contracts/failure-baseline.md` FB-01…FB-09).

**Scope**: the authoritative 83-name baseline failure set (`test-evidence/baseline-failures-2026-10-22.txt`,
FB-01). Every name appears exactly once (V-E5-1). Rows are appended during implement triage
(W1 Class 1 sync at T023; Class 2 per-name triage at T025–T027; closure check at T029).

**Field vocabulary (closed)**:

- class: `mirror-sync` / `stale-pin` / `regression` / `pre-existing-debt`
- disposition: `synced` / `pin-updated+rationale` / `mechanism-fixed` / `debt-registered`
- `debt-registered` rows MUST point at a dated debt record explicitly marked "not introduced
  by this scope" (V-E5-2). `mirror-sync` rows MUST name the sync command and pair scope (V-E5-3).
- Deleting or merging away a failing test is never a disposition (FB-07). Debt records never
  claim green (FB-06).

## Rows

<!-- append rows below; one row per baseline failure name -->

| original node id | class | disposition | evidence pointer | date | commit |
|---|---|---|---|---|---|

## FB-06 debt record index

<!-- dated debt records under test-evidence/ (one file per debt, 一文一件); each MUST state
     the failing pinned test, that it predates this scope, and fix-before-close vs registered -->

| debt record | failing pinned test | predates scope (yes + evidence) | chosen path | date | commit |
|---|---|---|---|---|---|
