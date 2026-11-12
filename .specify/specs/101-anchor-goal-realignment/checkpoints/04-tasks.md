# Checkpoint 04 — tasks

## 1. Artifact verification

- sentinel: `TASKS-DONE`
- U4: pass — `tasks.md` landed (81 rows, `T001`…`T081`) on the plan's six-work-package spine: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/101-anchor-goal-realignment/tasks.md` → `0 error(s), 0 warning(s)`; `pre-analyze-check.py --stage tasks` → `decision=pass errors=0 advisories=0`, summary `fr 71 / sc 10 / tasks 81`; `decomposition-check.py --mode tasks` → `decision=proceed`, measured `fr_count 71 ≤ 120`, `task_count 81 ≤ 160`; `audit-plan-changes.py --base 8f91310f7 --head HEAD` → `classification=declared`, `undeclared=false`, 4 plan-owned paths touched.
- coverage: every FR-001…FR-071 is cited on a task row and indexed in § FR → 行 trace; every SC-001…SC-010 is cited on its sensor row **and** indexed in § SC → 行 trace with its `**Path**` value (mechanical re-read: zero FR and zero SC ids missing from the rows); runtime `in-scope` rows (FR-047 / FR-048 / FR-049 / FR-054 / FR-057 / FR-070) are each quoted by name.
- wrap-up records: session `20261112T074632Z-run-determination-speckit-tasks-r20261112t064607z-b101.md`; exec-quant `20261112T074647737249Z-a3402305.json`; feedback `20261112T074654Z-speckit-tasks.md`.
- anomalies/corrections: (a) `PLAN-EDIT: 101-005` — the classification count was transcribed as "2 action-goal" in five copies (`plan.md` Technical Context, contract C-44 P2, `quickstart.md` S-5, `feature-ref.md` SC-003 row, `.specify/features.md` 101 row) against the machine-readable authority `classification.json` = 9 anchor / 3 action-goal / 2 obsolete; all five corrected, declaration `PLAN-EDIT: 101-005` in `tasks.md` § Notes N-1 and in the stage declarations file. (b) `PLAN-EDIT: 101-006` — the plan named two consumer scripts under `scripts/python/` that do not exist; real locations are `skills/external/sdd-project-setup/scripts/logical-framework.py`, `skills/external/sdd-house-keeping/scripts/logical-framework.py`, `skills/internal/create-team/scripts/build-summary-input.py` (matches contract C-32), corrected in the plan tree and WP-01 territory. (c) `PLAN-EDIT: 101-007` — the plan placed the four team-domain skills under `skills/external/`; they live under `skills/internal/`, corrected in the plan tree and WP-03 territory. All three are corrections consistent with the recorded intent, disclosed in `tasks.md` § Notes.
- rulings disclosed, not folded into green: `[green:]` clause tags omitted (claiming C-1…C-49 would force a row order contradicting the work-package spine and produce `green-cross-phase` warnings; FR-level traceability compensates — N-4); phases are work-package phases with no `[US]` labels, stories mapped through the SC trace (N-5); red-first under the plan's guard-late ordering is satisfied by plan-mandated injection checks recorded in `notes/red-first-evidence.md` (N-6); the docs-build limb is `not-evaluated` per EP-006, re-probed this stage with `hugo --renderToMemory` exit 1 (N-7).
- artifacts: `checkpoints/04-tasks.md`, `tasks.md`, the five corrected plan-owned / registry copies above.

## 2. Goal progress

- Direct driver run; no bound goal (`goal_slug` absent). `n/a — no goal to measure`.
- Brief-level objective: the decomposition that the next stage executes now exists and is mechanically checked; the semantic inversion itself is not yet applied to any store (correct by design — implement executes it).

## 3. Team configuration review

- No team exists for this direct run. `n/a — no team`.
- symptom: none; proposal: none; ratification: n/a; applied: no.

## 4. Next stage concurrency / roster

- requested: 24; effective: 24; reason: local fork carrier; the implement stage's worker partition follows this file's phases and write territories; verifier reserve: 1.
- stage max_parallel: bounded by the three serial chains named in `tasks.md` § Dependencies & Execution Order (engine chain, command-surface chain, cleanup chain); parallel-safe rows are only the `[P]` sets.
- next stage: `implement`; roster: SDD Implement Coordinator (workers per work package, verifier reserve 1).

## 5. Direction audit

- reload tier: T0 + T1.
- Q1 rules: unattended / no approval request / U4 → next stage / spine written before acting / workspace guard / fast-fail / gate discipline / budget / report discipline — all in force.
- Q2 process: `correction-applied` — three plan-owned factual slips corrected against their machine-readable authorities (`classification.json`, the real script paths, the real skill layer) and declared; the docs build stays a recorded falsified premise with a fallback, never a silent waiver.
- Q3 next action: pass — `implement` is the next stage in the U0 stage plan.
- Q4 spine freshness: pass — spine carries the tasks start, gates and last verdict; this file is the stage's own record.
- Q5 territory/workspace: pass — the stage commits contain only this spec's artifacts, the 101 registry row, and its wrap-up records; the pre-existing `smoke-081.txt` modification was neither staged nor reverted.
- verdict: `correction-applied`.
- 5b published-state: `n/a — no history correction` (new commits only).
