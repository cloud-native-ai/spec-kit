# Review-repair r2 — dispositions (098-suite-speed-optimizations)

- Date: 2026-11-11
- Worktree: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/098-suite-speed-optimizations`
- Review object: `review.md` round 2 (run-start HEAD `c4f7c8bd1`; the refusal's sole root cause was
  T061 unexecuted → SC-003/SC-005 `partial` → `closure-acceptance-check` `block`).
- Repair target: execute T061 (closure stage slot 2 + same-tree serial validation), land its
  readings, close the two criteria, and clear `deferred_tasks=` so the checker reaches `accept`.
- Quadruple (this round): `flow_class=execution`; `source=declaration`; `marker=`; `error=-`

## Summary

| Item | Severity | Disposition | Evidence |
|------|----------|-------------|----------|
| T061 unexecuted → SC-003/SC-005 `partial` → checker `block` | P0 (refusal root cause) | **repaired** — slot 2 + same-tree `--full --serial` run executed; both criteria `pass`; checker `accept` | `test-evidence/closure.txt`; `test-evidence/review-repair-r2-closure-{payload.json,verdict.txt}` |
| Attempt-1 comparison: 5 parallel-only names (`test_trigger_tuning.py`) | defect found at closure | **repaired at the root** — explicit `--workspace` in two trigger test helpers (the r1 SC-002 precedent); re-measured, both `comm` directions empty | `test-evidence/closure.txt` §5; `test-evidence/closure-isolation-fix.txt` |
| A1 (P2) — verification readings did not name the measured tree | P2 | **repaired in passing** — `*_measured_tree=` fields added beside the baseline/post-change/closure counters | `verification.md` |
| A2 (P2) — index SC-005 row opened with the superseded slot-1 wall (70.99 s) | P2 | **repaired in passing** — the row now states the rebuilt-referent supersession and the closure reading | `test-evidence/index.md` SC-005 row |
| F2 (P2) — `checkpoints/02-clarify.md` duplicates `01-requirements.md` | P2 | **not repaired this round (carried)** — it is an untracked driver-side handoff record; reconstructing the clarify stage record would fabricate stage history at the closure stage; the finding does not block the verdict and its framework fix (REC-098-07) is already registered | `review.md` §3 F2; `checkpoints/02-clarify.md` |
| F3 / F1 (P2/P1 framework) | — | **carried unchanged** (REC-098-08 / REC-098-01); framework-targeted, not slice-repairable | `review.md` §5 |

## 1. T061 execution — slot 2 of 2 plus the same-tree serial validation run

- **Slot 2 (full parallel)** — `bash scripts/bash/run-tests.sh --full --names-out <scratch>/final-failed-repaired.txt`
  → exit `1`, wall **70.62 s**, `223 failed, 8363 passed, 2 skipped, 576 warnings in 46.99s`;
  serial-exception pass `1 passed, 8588 deselected in 17.89s`;
  `mode=parallel workers=auto dist=load passes=2 tier=full excluded_slow=0`.
  Names: `final-failed.txt` (223 entries, sha256 `1f85ac90…`).
- **Serial validation** — `bash scripts/bash/run-tests.sh --full --serial --names-out <scratch>/serial-failed-repaired.txt`
  → exit `1`, wall **708.13 s**, `223 failed, 8364 passed, 2 skipped, 3 warnings in 705.97s`;
  `mode=serial reason=explicit tier=full excluded_slow=0`.
  Names: `test-evidence/closure-serial-failed.txt` (223 entries, sha256 `1f85ac90…` — byte-identical
  to the parallel list).
- **Bidirectional comparison**: both `comm` directions **0**; `cmp` byte-identical (SC-003).
- **Slot-1 name comparison** (`comm -13 baseline-failed.txt final-failed.txt`): **0** new names;
  64 removals (GATE-1 empty).
- **Wall clause**: `70.62 / 76.52 = 92.3 % ≤ 110 %` (rebuilt pre-change referent, SC-005).
- **Budget statement**: slot 2 is the closure slot; the serial validation run consumes no budget
  slot and is not an SC-004/SC-005 wall reading (A14). The attempt-1 slot-2 reading (71.82 s,
  254 names) is superseded by the repaired-tree reading above and is retained only as the
  diagnostic in `closure.txt` §5 — no third measurement slot is added.

## 2. The isolation defect attempt 1 exposed, and its root-cause repair

- Attempt 1's comparison was `comm -13` = 0, `comm -23` = **5** — five names only in the parallel
  arm, all `tests/integration/test_trigger_tuning.py`. The promotion file additionally failed 18
  tests in **both** arms.
- **Root cause (measured)**: engine C-7 resolution gives engine self-location priority; this
  worktree is nested under the parent repo's `.specify/.tmp/`, so the engine resolves to the
  **parent repo**. Probe (`--action status`, read-only, scratch cwd): the envelope reports
  `workspaceRoot=/storage/project/cloud-native-ai/spec-kit`. The tuning/promotion helpers ran the
  engine without `--workspace`, so the tests shared the parent repo's trigger store — the 18
  promotion tests read a fixture `index.json` that was never written (`FileNotFoundError`), and
  the tuning tests raced on shared state under xdist.
- **Repair (C-004's isolation-defect path; r1's precedent in `tests/contract/test_trigger_engine.py`)**:
  forward `--workspace <cwd>` unless the call already names one. Exact change per file:
  `+    argv = list(args) if "--workspace" in args else ["--workspace", str(cwd), *args]`
  and the subprocess call uses `argv`. No assertion weakened, no test removed or narrowed, no
  skip/xfail/retry introduced, no parametrize removed, no worker-resolution change — the SC-010
  forbidden-means set is untouched.
- **Targeted green**: parallel `38 passed in 3.46s` exit 0; serial `38 passed in 16.74s` exit 0
  (`test-evidence/closure-isolation-fix.txt`).
- Slot 2 and the serial validation were then re-taken together on the repaired tree (both listed
  in §1); no edits occurred between the two runs.

## 3. Record updates

- `verification.md`:
  - `SC-003_status=pass` — full-tier same-tree comparison, both `comm` directions empty;
    `SC-005_status=pass` — wall ratio 92.3 %, both slots full-tier, 0 new names.
  - The five ladder fields on the two former `partial` rows were removed (they are only legal on
    blocked/deferred/partial rows).
  - Evidence records added for SC-003 and SC-005, both binding
    `test-evidence/closure.txt` (sha256 `7c504ef8…`).
  - `deferred_tasks=` and `deferred_reason_summary=` are now empty (61/61 rows closed).
  - The smoke triple is unchanged and valid (exit 0, evidence exists, exactly one record).
  - P2 A1: `baseline_measured_tree=`, `post_change_measured_tree=` and `closure_measured_tree=`
    now sit beside the counters; `closure_full_suite_{wall_s,failed_names}=` record the slot-2
    reading.
  - The closure verdict block is replaced by the `accept` record copied from the payload; the r1
    `block` record stays archived in its own files.
- `tasks.md`: T061 `[~]` → `[X]` with its execution reading; **DoD Status** now `met` (61/61);
  the Phase-7 checkpoint sentence and the `[~]` notes bullet updated; `validate-tasks.py` → PASS,
  0 errors / 3 known out-of-order warnings (unchanged).
- `test-evidence/index.md`: SC-003/SC-005 rows carry the closure readings and `pass`; the SC-005
  row marks the 70.99 s slot-1 wall superseded by the 76.52 s rebuilt referent (P2 A2); a
  review-repair r2 records table was added.
- `test-evidence/closure.txt` (new): the complete T061 record (commands, exits, walls, verbatim
  counting lines, both `comm` directions, the slot-1 comparison, the 3-name rebuilt-baseline
  disclosure, the budget statement, gate readings).
- Names/logs archived: `final-failed.txt`, `test-evidence/closure-serial-failed.txt`,
  `test-evidence/closure-prerepair-{parallel,serial}-failed.txt`,
  `test-evidence/run-logs/closure-{parallel,serial}-full.log.gz`,
  `test-evidence/run-logs/closure-prerepair-{parallel,serial}.log.gz`.
- Rebuilt-baseline name disclosure (not the slot-1 comparison): `comm -13` vs the rebuilt
  pre-change list = 3 names, all present in the recorded slot-1 list and all worktree-state
  artifacts — feedback records under `.specify/memory/feedback/` (flow_class lines), a generated
  skill `__pycache__/*.pyc`, and the stale `.specify/.tmp/wp9/before-tree/` scratch copy. They are
  disclosed in `closure.txt` §4 and are not new relative to the slot-1 baseline.

## 4. Closure judgement and gates (re-read on this tree)

- `closure-acceptance-check.py --spec-dir … --feature-detail .specify/features/086-efficient-test-execution.md --json --json-out test-evidence/review-repair-r2-closure-payload.json`
  → exit **0**, verdict **`accept`**, reasons `[]`; `final_path` pass 9 / total 9; tasks closed 61 ·
  deferred 0 · open 0 · in_progress 0; completion conditions all true; smoke present/exit 0/evidence
  exists. Transcript: `test-evidence/review-repair-r2-closure-verdict.txt`; payload:
  `test-evidence/review-repair-r2-closure-payload.json`. Bare invocation (no `--feature-detail`)
  still exits 2 with "no registry row" — the follow-up-spec binding's resolution fact.
- GATE-1: `comm -13 baseline-failed.txt final-failed.txt` empty → pass.
- GATE-2: `python3 scripts/python/sync-mirrors.py --check` → exit 0 (no mirror-pair file was edited
  by this repair).
- GATE-3: `grep -cE '^- \[[ >]\]' tasks.md` = 0; 61 `[X]`, 0 `[~]`.
- GATE-4: every final-path SC is `pass` and the smoke triple is valid.
- `validate-tasks.py` → PASS (0 errors; the same 3 declared out-of-order warnings).

## 5. Anomaly line

- One defect was found by the closure measurement itself (the attempt-1 five-name parallel-only
  difference) and repaired under C-004's explicit isolation-defect path — a correction consistent
  with the recorded intent and the r1 precedent, disclosed above, not a halt-level decision.
- No unresolved anomaly; no blocker remains in this repair's scope.
