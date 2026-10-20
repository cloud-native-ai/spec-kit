# Verification — Feature 063

Evidence class labels: **automated** (CI test), **recorded trace** (non-CI
recording), **driver closure** (owned by the driver after review).

## T002 — implement-start full-suite baseline (only slot consumed in implement)

- State spine: `/tmp/sdd-loop-efficiency/state.md` (`spine_write_mode=direct`)
- E2 ledger fence position: `<!-- test-budget:begin -->` line 1 (`seq=1`, `slot=baseline`)
- Command: `bash scripts/bash/run-tests.sh --names-out .specify/specs/063-sdd-loop-efficiency/notes/baseline-failed-tests.txt`
- Result: `68 failed, 4115 passed, 1 skipped, 4 warnings in 397.21s`; exit `1`
- Failed-name list: `notes/baseline-failed-tests.txt` (68 entries)
- Full log: `/tmp/t002-full-suite.log`
- Failure surface: all 68 are pre-existing mirror-drift / frozen-count contract
  failures; none is in `test_sdd_loop_driver_skill.py` or
  `test_sdd_loop_driver_cli_profiles.py`.
- `baseline_slot=consumed`; closure is driver-owned after review; implement ran
  no second full suite.
- E3 reference copy: `test-evidence/implement.jsonl` carries one legal row that
  references the E2 row; it is a transport/evidence copy, never the ledger.

## T001 — pre-change measurements and SC-010 baseline

- Measurements: `notes/pre-change-measurements.md` (+ raw outputs `notes/baseline-*.txt`)
- SC-010 baseline: `notes/stall-behavior-baseline.json`, `base_commit=a1aac7e5`,
  `initial_retries=0`, recorded before the first behavior-face commit; replay
  pre-check on the current tree: zero differences.

## US1 — fast lane (T008–T015)

### T008/T010 — admission-check unit suite (automated)

- Red: `notes/red-first-evidence.md` § T008 (23 failed, script absent).
- Green: `bash scripts/bash/run-tests.sh tests/unit/test_admission_check.py -q` → `23 passed`.
- Script: `skills/external/sdd-loop-driver/scripts/admission-check.py`; constants
  `FR_MIN=8 / FR_MAX=30 / TASK_MIN=10 / TASK_MAX=40`; exit codes 0/1/2; stdlib only.

### T009/T011 — FL clauses and owner document (automated)

- Red: `notes/red-first-evidence.md` § T009 (10 failed).
- Green (T013 combined run): `tests/unit/test_admission_check.py tests/contract/test_sdd_loop_driver_efficiency.py -q` → `33 passed`.
- Owner document: `skills/external/sdd-loop-driver/references/efficiency-model.md` §1.
- Downstream: `references/dispatch-recipes.md` Recipe 4 admission point + reversion;
  `references/stage-prompts.md` § Fast Lane Conditional Blocks.
- FR-042(a) script-side: S1/S2 show admission and refusal; the stage-sequence part
  is recorded in the S7 dry-run trace (T051).

### T012 — mirror parity (automated)

- `sync-mirrors.py --write --only skills/external/sdd-loop-driver` → 2 new + 2 updated.
- `diff -rq skills/external/sdd-loop-driver .specify/skills/sdd-loop-driver` → exit 0.
- `sync-mirrors.py --check --only skills/external/sdd-loop-driver` → `ok (17 files)`, exit 0.
- Existing C-12/C-18 (mirror drift) remain green; `test_sdd_loop_driver_skill.py` was
  23/23 green at T001.

### T013 — targeted green + quickstart S1/S2

- `bash scripts/bash/run-tests.sh tests/unit/test_admission_check.py tests/contract/test_sdd_loop_driver_efficiency.py -q` → `33 passed in 85.74s`, exit 0.
- Quickstart S1: exit 0, `fast-lane`, 12/25, seven pass. S2: exit 1, `full-chain`, 60 tasks, criterion a fail. Details in `notes/quickstart-run.md`.
- Narrow-mode admission: S1/S2 and `test_narrow_task_pattern_only_for_admission`; wide mode is repository bookkeeping only.
- SC-001/SC-002 automated evidence: unit + FL tests + S1/S2.

### T014 — mutation drill (5 applications, all restored)

| Mutation | Red test | Restore |
|----------|----------|---------|
| FR_MAX 30→31 | `test_task_count_boundary_edges[31-40-False]` | checksum equal |
| count SC rows as FR | `test_fr_count_excludes_sc_rows` | checksum equal |
| remove (c)/(d) scans | `test_sensitive_or_engine_path_rejected` | checksum equal |
| accept multi-record manifest | `test_lines_manifest_syntax_pinned[two records]` | checksum equal |
| use wide task mode for admission | `test_narrow_task_pattern_only_for_admission` | checksum equal |

### T015 — post-mutation re-run

- Mirror re-sync + `diff -rq` exit 0 + `--check` exit 0.
- `33 passed in 121.09s`, exit 0; quickstart S1/S2 re-run with the same expectations.
- `git diff` contains only the feature's expected paths (implementation + mirrors + tests + spec notes).
