# Efficiency Case Study — 2026-10-20

**Status**: dated record, not a normative rule. Input to Feature 063's review/verification and
to the framework feedback store. This note records the efficiency of developing Features
063/064 and the `sdd-project-setup` improvement on 2026-10-19/20, using this run itself as the
real-world case.

## Measured facts

- 063 wall-clock: 2026-10-19 16:33Z (requirements feedback) → 2026-10-20 13:04Z (review
  feedback) ≈ **20.5 h**.
- 063 stage durations (from the state spine/logs): requirements ≈10 min; clarify ≈6 min;
  plan ≈26.6 min; tasks ≈10.7 min; checklist ≈7.6 min; analyze + repairs multiple hours;
  implement attempt 1 ≈42.6 min (stopped/restarted); implement-retry-1 ≈63.8 min;
  review ≈16.7 min.
- 063: **3 analyze runs + 3 tasks/spec repair passes**. 064: 2 analyze runs + 1 repair +
  ≈2 h post-review repair. `sdd-project-setup` improvement: ≈1 h.
- Human decision points: second repair authorization, P0 repair decision, implement restart.
- Non-blocking `.r2c` hook timeouts (5 s) produced false-failure-looking output while the
  Write/Bash operations succeeded.
- Monitoring race: the watcher returned `TIMEOUT` at the stage deadline while the process was
  still alive; the process completed ~11 min later. Deadline grace is now implemented.

## Test evidence observed

- 063 targeted set: 144 passed; watcher self-test 33/0; full-suite baseline: 68 failed /
  4115 passed (existing failures, zero new); review independently found a P0 in the test-budget
  audit denominator.
- Full-suite executions and long subagent stages dominated wall-clock time; the two-slot test
  budget was only partially dogfooded.

## Root causes

1. **Feature size**: 063 (43 FR / 52 tasks) and 064 (68 FR / 82 tasks) exceeded the medium
   fast-lane interval (8–30 FR / 10–40 tasks), forcing the full chain and repeated repairs.
2. **Over-specified, cross-layer duplicated specs**: requirements/data-model/contracts/tasks
   drifted on counts, state sets, and paths; analyze found textual/arithmetic inconsistencies.
3. **Late cross-feature overlap**: CLI capability profiles were provisionally added to 063 and
   then implemented in 064; tasks-repair-2/3 and analyze rework followed.
4. **Long subagent stages without early commit boundaries**: post-review repair ran ≈2 h before
   committing; the TIMEOUT/restart episode added overhead.
5. **Test-budget mechanism not dogfooded**: the review P0 showed missing evidence was silently
   removed from the `stages=N` denominator; `SC-005` was not trustworthy yet.
6. **Monitoring and hook noise**: `TIMEOUT` was treated as a stop/kill signal although the
   process was alive; hook timeouts were non-blocking but looked like failures.
7. **Human decision overhead**: the second repair, P0 disposition, and implement restart were
   necessary but added latency.

## What the 063 optimizations did / did not do

- **Fast lane**: correctly excluded these large features, but there is no large-feature
  decomposition path.
- **Two-slot test budget**: partially used; the audit denominator P0 must be fixed before its
  success criterion is trusted.
- **Plan minor-fix constraint**: used, but plan/tasks were still traversed repeatedly; earlier
  machine checks and overlap checks are needed.
- **stream-json + nohup**: implemented; deadline grace fixed the late-completion race; hook
  timeouts remain a reporting gap.
- **064 worktree/line registry**: manual worktrees were the right direction; same-repo
  concurrency still needs the 064 registry/worktree design.

## Recommendations (input to the flow)

1. Add a **large-feature decomposition gate** before plan: >30 FR or >40 tasks must split into
   subfeatures instead of driving the full chain in one line.
2. Add a **cross-feature overlap pre-check** at requirements/clarify for shared skill assets,
   CLI profiles, and probe objects.
3. Enforce **per-task-group commits** and stream-json/grace; treat `TIMEOUT` as a budget verdict,
   not a kill signal; treat hook timeouts as non-blocking warnings.
4. Move deterministic checks (counts, references, clause/task mapping) earlier into
   requirements/plan/tasks to reduce analyze repair loops.
5. Dogfood the two-slot test budget with targeted sets between the two full runs, and pin the
   audit denominator with missing-evidence cases.
6. Keep independent review: it found a real P0; do not merge with P0 open.
7. Record this case in review/verification and the feedback store with markers
   `sdd-loop-efficiency` and `token-efficiency`.

## Evidence pointers

- `review.md` (P0/P1/P2)
- analyze logs under `/tmp/sdd-loop-efficiency/`
- state spine `/tmp/sdd-loop-efficiency/state.md`
- 064 overlap adjudication: `.specify/specs/064-subagent-concurrency/notes/063-overlap-adjudication.md`
- git history: 063 commits `a2279cc5` → `afca82f7` → `a108ff11`
