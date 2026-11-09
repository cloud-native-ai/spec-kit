# Efficiency diagnosis — 092 run (2026-11-09)

Sensor: commit timestamps (exec-quant records carry no elapsed_ms for these units — the run's own
measurement did not capture duration, so this table is derived from git, which is measured).

| stage | window | wall | output |
|---|---|---|---|
| requirements | 10:42–10:47 | 5m | 465 lines, 65 FR / 20 SC |
| clarify | 10:47–10:56 | 9m | 8 rulings, +24 FR |
| plan | 10:57–11:11 | 14m | 458-line plan, 7 contracts, 8 packages |
| tasks | 11:11–11:27 | 16m | 150 rows, 3 registry writes |
| checklist | 11:27–11:31 | 4m | 40 items |
| analyze | 11:32–11:43 | 11m | 25 findings (1 CRITICAL / 8 HIGH) |
| analyze repair | 11:43–12:04 | 21m | 8 contracts → 62 clauses, all 25 closed |
| implement | 12:05–13:15+ | 70m+ | P1 + P2 only; two 500-turn stalls |

## Bottlenecks, ranked

1. **Monolithic implement dispatch (≈70m, the largest cost).** One subagent was handed 150 rows /
   62 clauses and a 500-turn budget; it hit the cap twice, both inside P2. Each restart re-read
   the whole corpus, so roughly two-thirds of the spent work was re-done. P1 alone took 19m;
   P2 needed ~50m and still needed 2 driver minutes to finish (mirror + 81 tests + commit).
2. **Full-corpus re-read per stage (10–21m each).** Every stage agent re-opened the 465-line
   requirements, 458-line plan, 150-row task graph and 62 clauses; none received package slices
   or exact anchors. Bookkeeping stages (tasks 16m, repair 21m) cost more than design (plan 14m).
3. **Gate friction causing rework rounds.** Three deterministic-gate defects bit this run:
   `pre-analyze` skips any heading containing "history" (it hid FR-022…FR-028); `missing-path`
   advisories fire on the feature's own not-yet-created deliverables (48 rows); the clause
   accounting reports an FR lane that no contract can close (57/65). Together they produced one
   clarify round (9m) and one repair round (21m).
4. **Declared parallelism unused.** The team was created with max_parallel 4/8/4, but plan,
   tasks, repair and P1/P2 all ran serially; no two packages ever ran in the same window.
5. **Oversized stage returns.** Ten multi-thousand-word reports were consumed by the driver,
   costing context and slowing each next dispatch.

## Adjustments (applied from the next dispatch)

- Implement runs **one package per dispatch** (P3, P4‖P5, P6 sharded ×3, P7‖P8), each ≤40 rows,
  with the package slice and file anchors in the brief; the 500-turn cap stays, the scope shrinks.
- A machine work queue (`test-evidence/work-queue.json`, derived from tasks.md) carries package →
  rows → files, so executors stop re-deriving order.
- Corpus metrics are computed once and stored (`test-evidence/corpus-baseline.json`).
- Targeted pytest during implement; the full suite only at the implement start and after review
  (the two-slot budget). 092 has spent 80 s on the P2 suite so far.
- Parallel dispatch for disjoint packages (P4‖P5, P7‖P8); P6's 19 repairs shard by feature group.
- Stage returns are capped at ~30 lines plus evidence pointers.

## Measured proof of the fix

Finishing P2 driver-side (mirror sync + 81 contract tests + commit) took **≈2 minutes**, where a
third 500-turn dispatch would have re-read the corpus and risked a third stall.

## Script-level concurrency (2026-11-09, follow-up)

- No interpreter on this host has `pytest-xdist` (`/usr/bin/python3`, `/usr/local/bin/python3`: pytest 9.0.3, no xdist), so `run-tests.sh --workers` always degrades to serial; this is also why its `-n0` runs 25 tests red.
- Added `scripts/bash/run-tests-shards.sh`: shards by module (not node id, to stay under ARG_MAX), runs N concurrent pytest processes, merges the FAILED list, honours `--names-out`, and resolves the interpreter by the same ladder with an xdist-independent check.
- Measured: 8 heavy modules, 8 shards, 225 passed + 1 known mirror-drift failure, 82 s. The critical path is the 80 s `test_non_disposable_check.py` module — the next lever is splitting that module, not raising N.
- Budget interaction: 15 writer seats and 8 test shards on 32 CPUs contend; shards run at stage boundaries, never inside a writer wave. The engine already offers `--scope sNNN-of-N` shards for parallel review runs.
