# 086 T054 — Two-slot accountability for every full-suite run

Owner of the proposition: `tasks.md` T054 / `contracts/dogfood-and-preservation.contract.md` C-047.
The slot model itself and its ceiling are **owned elsewhere and not restated here**:
`skills/external/sdd-loop-driver/references/efficiency-model.md` and
`.specify/specs/075-sdd-loop-efficiency/contracts/test-budget.md`.
This file only accounts for what this feature consumed against that model.

Rule applied when reading the table below: a full-suite invocation that is neither listed nor
exempted here is an unaccounted consumption and fails T054. A **targeted** re-run (a named subset of
files) is not a full-suite run and consumes no slot.

## The account

| # | slot | purpose | command | output evidence |
|---|---|---|---|---|
| 1 | `slot-1-baseline` | T050 — pre-change serial baseline, the comparison referent for C-045/C-047 | `env -u PYTHONPATH bash scripts/bash/run-tests.sh --names-out .specify/specs/086-efficient-test-execution/test-evidence/baseline-failed.txt -q` | `test-evidence/baseline.txt`; names in `test-evidence/baseline-failed.txt` |
| 2 | `out-of-slot-exception` | T014 — parallel-safety measurement (default-parallel run compared against slot 1) | `env -u PYTHONPATH SPECKIT_PYTHON=<venv>/python bash scripts/bash/run-tests.sh --names-out .specify/.tmp/086/us1-parallel.txt -q` | `test-evidence/parallel-safety.txt` |
| 3 | `out-of-slot-exception` | T016 arm 1 — A13 scheduling experiment, shipped default (`-n auto`, `--dist load`) | `env -u PYTHONPATH SPECKIT_PYTHON=<venv>/python bash scripts/bash/run-tests.sh --names-out .specify/.tmp/086/s5-auto-names.txt -q` | `test-evidence/scheduling-experiment.txt` § Arm 1 |
| 4 | `out-of-slot-exception` | T016 arm 2 — A13 scheduling experiment, the single most plausible alternative (`--workers 8`, `--dist loadfile`) | `env -u PYTHONPATH SPECKIT_PYTHON=<venv>/python bash scripts/bash/run-tests.sh --workers 8 --dist loadfile --names-out .specify/.tmp/086/s5-lf-names.txt -q` | `test-evidence/scheduling-experiment.txt` § Arm 2 |
| 5 | `out-of-slot-exception` | M-16 real-suite-load mutation leg, rep 1 — the GATE-5 hunk check must go RED when a non-carve-out `SC-010_*` line is doctored; loaded with the real suite so the reading is not a toy | full suite over a doctored copy of `verification.md` held **outside** the repo root | `test-evidence/parallel-safety-attribution.md` § Mutation legs → Leg M-16 |
| 6 | `out-of-slot-exception` | M-16 real-suite-load mutation leg, rep 2 — second completed rep of the same leg, to show the RED reading is stable and not a one-off | same, second rep | `test-evidence/parallel-safety-attribution.md` § Mutation legs → Leg M-16 |
| 7 | `slot-2-in-slot-rerun-attempt` | T047 first attempt — **contaminated, not the closure slot**; trigger was the package's own sandbox worktree *inside* the repo root, not a property of the feature tree | same command as #8 | `test-evidence/closure-diff.txt` § Run ledger |
| 8 | `slot-2-closure` | T047 — default-parallel closure run on the cleaned tree; the slot-2 record | `env -u PYTHONPATH SPECKIT_PYTHON=/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.venv/bin/python bash scripts/bash/run-tests.sh --names-out .specify/specs/086-efficient-test-execution/test-evidence/final-failed.txt -q` | `test-evidence/closure-diff.txt`; names in `test-evidence/final-failed.txt` |
| — | **no run** | T044 — worktree-pollution check **re-uses #8**: its before/after `git status --porcelain --untracked-files=all` snapshots bracket that run | (none of its own) | `test-evidence/worktree-clean.txt` |
| — | **no slot** | T040 — 085 preservation re-run is a **targeted** five-file set, not a full-suite run | targeted pytest over the five named files | `test-evidence/preservation-085.txt` § 8 |

That is two slots spent, five named `out-of-slot-exception` runs, one documented in-slot rerun
attempt, and two rows that add no run. Nothing outside this table was a full-suite invocation.

## Readings per row

### #1 `slot-1-baseline` (T050)

```
19 failed, 7475 passed, 7 skipped, 4 warnings in 687.41s (0:11:27)
```

19 names in `baseline-failed.txt`. Serial entry point (`run-tests.sh` default = serial before 086),
so this is the pre-change reference the parallel runs are held against.

### #2 `out-of-slot-exception` (T014)

Justification: the parallel-safety measurement necessarily compares a **default-parallel** run
against the **serial** slot-1 baseline; the serial side is not re-run because slot 1 already holds it.
19 failed / 7533 passed / 7 skipped, 206.12 s + 35.08 s serial exception pass.

### #3, #4 `out-of-slot-exception` (T016, two arms)

Justification: A13 asks whether the shipped default is the right scheduler. The adjudicated
allocation reduces the experiment to the **representative pair** rather than four arms — the two-arm
pair already decides the hypothesis, and the four-arm sweep would multiply full-suite consumption to
answer a question the pair answers. Both arms produce the identical 19 failure names
(`comm -3` empty), 0 new names against slot 1, and the alternative is not faster
(204.99 / 201.34 = 1.02×) — the default stays.

### #5, #6 `out-of-slot-exception` (M-16 real-suite-load, 2 completed reps)

Justification: a mutation leg that asserts a check goes red is only meaningful if the check is
exercised under the real suite load, not a toy fixture; the sandbox tree is a **doctored copy**, not
the feature tree, and contributes to **no** name diff (it is not in `final-failed.txt` and appears in
neither `comm`). Two completed reps, both reading RED on the mutated line and GREEN on the tracked
tree. Same `out-of-slot-exception` label the brief assigns to the sandbox accounting.

### #7 `slot-2-in-slot-rerun-attempt` (T047 first attempt — contaminated)

Recorded here so the account is complete, and deliberately **not** labelled `slot-2-closure`.

- Trigger: this package's own sandbox was a `git worktree` at
  `.specify/.tmp/086/mutations/sandbox/` — **inside the repo root**. `git status` could not see it
  (a nested worktree is not untracked content of the parent), but the contract tests' `_md_files()`
  walks could, so three extra contract-spec documents entered the walk.
- Reading: `21 failed, 7533 passed, 7 skipped in 271.72s` — two names above the baseline.
- Disproof that the extra names are sandbox artifacts and not feature behaviour:
  `tests/contract/test_isomorphism_map.py` → `27 passed` once the sandbox was removed.
- Correction: all further doctored copies were relocated **outside** the repo root, to
  `/Users/liuqiming.lqm/tmp/spec-kit/086/mutations-c2/`. Nothing sat under the repo while #8 ran.

### #8 `slot-2-closure` (T047)

```
19 failed, 7535 passed, 7 skipped, 55 warnings in 284.12s (0:04:44)   <- parallel pass
1 passed, 7561 deselected, 3 warnings in 35.22s                       <- serial exception pass
```

Exit code **1**; `final-failed.txt` holds exactly **19** names;
`comm -13` and `comm -23` against `baseline-failed.txt` both empty.
Unit wall clock 284.12 s = **0.41×** slot 1 (687.41 s), and 284.12 s = **69%** of SC-001's 412.59 s
ceiling. Full detail: `test-evidence/closure-diff.txt`.

### Two rows that add no run

- **T044** brackets #8: `git status --porcelain --untracked-files=all` was captured immediately
  before and immediately after that run; the delta is the run's own tracked `--names-out` target
  (`final-failed.txt`) changing from clean to modified, plus the permitted pre-existing
  `.specify/memory/trigger/index.json` residue. No run of its own — see `test-evidence/worktree-clean.txt`.
- **T040** re-ran five named 085 preservation files, not the suite (`20 passed in 6.22s`); a targeted
  set consumes no slot — see `test-evidence/preservation-085.txt` § 8.

## Verdict for T054

Every full-suite invocation this feature made is in the table above with a slot label, a purpose, a
command and an evidence file. Two slots spent (#1, #8); the rest are named exemptions; nothing is
unaccounted.
