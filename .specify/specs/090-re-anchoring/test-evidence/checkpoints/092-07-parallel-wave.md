# Checkpoint 07 — the parallel implement wave

## 1. Artifact verification

- Wave 1: 15 concurrent writers (u01–u15), disjoint territories, no commits by writers; driver integrated `76b4ec60` (mirrors, command copies, registry, live instructions).
- Gates re-measured after integration: 080 requirements 0 error; 089 tasks PASS (68 warnings); 085 tensions ok; harness-triple coverage exit 0 (A2 closed); closure 089 **accept**, 090 **accept**.
- Deviation (disclosed): the 15 writers were dispatched as `general-purpose` subagents. The 092 roster names seat agents (`sdd-implement-executor`, `sdd-stage-verifier`, `sdd-stage-integrator`, …) and 085 C-001 fixes the stage role grammar; a worker dispatch MUST resolve to its seat, not a generic agent. The deviation is corrected from wave 2 onward: every dispatch names its seat type.
- Clarification of the model: 15 concurrency is **15 instances of the executor seat** (085 C-002: count is dynamic), not 15 roster rows; the roster keeps one row per role plus the reporter, and `stage_seats.implement.max_parallel` is raised 8 → 15 (this checkpoint's single configuration change, per the protocol).

## 2. Temporary Goal progress

| criterion | degree | evidence_ptr |
|---|---|---|
| A–H classes reproducible | 100% (engine 81 tests; A2/A3/A5/A6 readings) | `p2-*.txt`, `u04/u06/u08-report.txt` |
| Repairs drive the corpus down | 80% (档 I wave done; P7/P8 pending) | `work-queue.json`, closure 089/090 accept |
| Repair lane after confirmation | not_evaluated | P8 |

## 3. Team configuration review

- evidence: wave 1 ran 15 writers concurrently
- symptom: dispatch identity was generic, not seat-bound
- proposal: bind every dispatch to its roster seat; keep 15 executor instances
- applied: yes — wave 2 uses seat agent types

## 4. Next stage concurrency / roster

- requested 24; effective 15; implement executor instances 15; verifier reserve 1; reporter seat present

## 5. Direction audit

- reload tier: T0+T1
- Q1 rules: in force; the 15-way wave respected file territories and the no-commit rule
- Q2 process: the generic-dispatch deviation was caught by the user and is recorded, not hidden
- Q3 next action: P5 via the `sdd-implement-executor` seat, then P7/P8
- Q4 spine freshness: updated with the concurrency change
- Q5 territory/workspace: 76 files integrated; no other feature's body beyond the declared carve-outs
- verdict: correction-applied

## 6. Path-assembly correction (2026-11-09, user-reported)

- Symptom: `.specify/specs/092-non-disposable/team/092-non-disposable/team.md` — the spec slug appears twice.
- Root cause: `goal-utils.py` assembled every team as `<team-root>/<slug>/team.md` with no default-single-team case, so a slug equal to the spec slug doubled the path segment.
- Fix: the default team now lives at `<team-root>/team.md` and is resolved first (`Scope.team_definition`, `_has_team`, `resolve_team_goal_identity`, `run_checks`); only an additional named team nests under `<team-slug>/`. 092's own team moved to `team/team.md`; 085 C-007 states the rule; T157 migrates the siblings.
- Verified: `goal-utils.py run-checks 092-non-disposable --scope spec` resolves the default file.
