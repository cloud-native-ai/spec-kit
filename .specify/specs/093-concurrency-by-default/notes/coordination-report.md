# Coordination report — Feature 093 implement run (T110, SC-006)

**Run kind**: `real` (the implement stage of `093-concurrency-by-default`, non-fixture)
**Date**: 2026-11-09 · **Branch**: `093-concurrency-by-default` / per-package branches · **Worktree**: `.specify/.tmp/sdd-loop/worktrees/093-*`
**Requirement**: FR-008 / SC-006 / T110 — a real run's coordination report, with every missing
quantity written `not_evaluated` and never a fabricated number.

## Reading

| Field | Value |
|-------|-------|
| `requested` | **6** (the stage plan's slot cap; `shared/declarations/facts/concurrency-slot-and-reserve.yaml`) |
| `effective` | `not_evaluated` |
| `effective_reason` | `mechanism-not-yet-landed` — the FR-035 fork carrier was authored *during* this run (WP3 T142) and the implement fold dispatched one package at a time in declared order; the run has no pair of overlapping unit intervals to measure |
| missing mechanism | the fold's package dispatches were serialized by the driver (WP1 → WP2 → WP3 → WP4 → enginefix → WP5); no two units were in flight together, so `effective` is not evaluated from interval overlap — it is **not** `0` and **not** an estimate |

There were six real dispatch units, each a separate fork worker, each resolving to its own record.
Five ran in their own per-package worktree/branch; **WP1 ran in the line worktree**
`.specify/.tmp/sdd-loop/worktrees/093-clarify` on branch `093-concurrency-by-default` — not a
per-package `093-wp1` worktree (`notes/implement-wp1.md`), corrected here per PF-3:

| Unit | Verdict | Evidence |
|------|---------|----------|
| WP1-facts | pass (15/16 rows; T098 open — the coordinator verdict is the owner's ruling, F-093-003) | `notes/implement-wp1.md`, commits `41900079…354145e2` |
| WP2-engine | pass (25/26 rows; T025's collect half waited on WP4) | `notes/implement-wp2.md`, commits `27ef0433…aac8834e` |
| WP3-owners | pass (30/30 rows) | `notes/implement-wp3.md`, commits `217342364…ce89e4e0e` |
| WP4-tests | pass (38/38 rows authored; engine-absent reds designed) | `notes/implement-wp4.md`, commit `5d92723f` |
| enginefix | pass (23/23 formerly red contract tests turned green) | `notes/engine-fix.md`, commit `cb34019a5` |
| WP5-release | this run (49 rows; release readings under `test-evidence/wp5-*`) | `notes/implement-wp5.md` |

**Integration order** (declared-order fold, never return order): `WP1 → WP2 → WP3 → WP4 → enginefix → WP5`,
recorded by the merge commits on the 093 branch (`6001c9ad1` opens WP5).

**Duration**: `not_evaluated` — the fold did not record per-unit dispatch/settle epochs, and this
report does not reconstruct them from commit timestamps (that would be an inference, not a measurement).

## Serial baseline comparison (T111)

`notes/serial-baseline.md` records the 091 comparison row: 62 tasks, 1 agent, 116 minutes, cited
from 091's recorded run — never re-measured here.

## Task-state and registry state at report time (measured)

`tasks.md` holds 159 `- [ ]` rows and the closure reading records `tasks: {closed: 0, open: 159}`;
`features.md` row 093 read `Planned` when this report was written. Flipping the sigils and landing the
status transition (`Planned → Blocked` on the closure verdict `block`) are the integration owner's
close-out acts, not this report's — this report makes no all-done claim. **T098 is open by design**
(F-093-003 — the coordinator-dispatch verdict value awaits its owner), not an unflipped done row.

## Why this is the honest reading

The feature's own rule forbids presenting a serial run as concurrent. The implement fold was real,
its units were real, and they ran one after another: the interval-overlap definition yields no
`>= 2` claim, so `effective` is `not_evaluated` and the reason is the missing mechanism at dispatch
time — not missing work. The mechanism itself (the facts, the engine, and the FR-035 fork runner
path) is this run's deliverable; its first exercised concurrent run is the next one.
