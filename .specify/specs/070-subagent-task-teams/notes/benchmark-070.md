# Benchmark Record — Feature 070 (T038, OR-13 / FR-023)

**Record date**: 2026-10-25T07:52Z (segment impl-s7)
**Method owner**: OR-13; the runtime description is in
`skills/external/sdd-loop-driver/references/decomposition-model.md` §18.3.
**Result**: `not_evaluated` — no comparable benchmark run exists. Closure is
blocked pending a user waiver that names SC-001 and/or SC-002, or a later
comparable benchmark.

## Method applied

OR-13 requires all of the following before SC-001 or SC-002 may be marked met:

1. a feature comparable to the 2026-10-24 dated baseline (full chain, 8–30 FR
   definitions, 10–40 task rows);
2. at least three comparable samples per measured stage;
3. the same host class and topology for every sample;
4. stage wall-clock measured as the FR-022/OR-04 interval: first package
   `started_at` to stage U4 completion (`stage_u4_at`), taken from the line
   state spine;
5. the dated conservative anchor (plan 70 min, review 37 min) or a re-measured
   baseline using the same interval — sources are never mixed.

## Inputs available to this record

| Input | Value | Source |
|-------|-------|--------|
| Comparable benchmark runs | none | no Feature 070 driver run record or state spine exists in this worktree |
| Samples per measured stage | 0 | no real `plan`/`review` decomposed stage was executed |
| Host class / topology | `not_evaluated` | no benchmark run to classify |
| Driver sessions | `not_evaluated` | no run record supplies a session count |
| Manual interventions | `not_evaluated` | no run record supplies an intervention count |
| Stage wall-clock samples | `not_evaluated` | no real spine timestamps |
| Stage executions per canonical stage | `not_evaluated` | no run-level stage chain |

The Scenario E report (see `notes/quickstart-run.md`) reports
`wall_clock_seconds=200`, `manual_interventions=0`, and `sessions=1`, but its
timestamps are synthetic fixture epochs and its counts are caller-supplied
inputs for a derivation test. It is **not** a benchmark run, is not comparable
to the dated baseline, and is deliberately excluded from every median and rate
above. The logical-clock simulator runs are likewise not wall-clock samples.

## Criteria outcome

| Criterion | Outcome | Reason |
|-----------|---------|--------|
| SC-001 (median plan/review stage wall-clock ≤ 80% of the dated anchor) | `not_evaluated` | 0 comparable samples; no real spine interval; fewer than the three required samples |
| SC-002 (stage executions per canonical stage ≤ 1.5, ≥40% below 2.6×) | `not_evaluated` | no comparable benchmark run and no run-level `(stage, stage_attempt)` chain; package retries stay out of the numerator |
| SC-006 (manual interventions per session ≤ 30/29) | `not_evaluated` | no run record supplies either the intervention count or the driver-session count |

No absolute wall-clock promise is made, and no metric is inferred from
impressions, estimates, or the simulator's logical clock.

## Closure consequence (FR-023)

An all-`not_evaluated` benchmark MUST NOT close the feature. Closure is blocked
until either:

- a comparable benchmark exists (three samples per measured stage, same host
  class and topology, FR-022 interval), or
- the user records an explicit written decision that waives SC-001 and/or
  SC-002, names the waived criterion or criteria, and states the reason.

As of 2026-10-25T07:52Z **no such waiver is recorded** in this workspace.
`not_evaluated` alone never satisfies SC-001 or SC-002. The T039 verification
matrix therefore carries both criteria as `not_evaluated` with closure
`blocked`, and no implementation or review step may promote either criterion
to `met`.
