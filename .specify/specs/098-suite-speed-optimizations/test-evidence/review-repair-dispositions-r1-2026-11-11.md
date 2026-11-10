# Review-repair r1 — dispositions (098-suite-speed-optimizations)

- Date: 2026-11-11
- Worktree: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/098-suite-speed-optimizations`
- Review object: `review.md` (2026-11-11, run-start HEAD `ea5962c87`; review commit `b9e5a35a2`)
- Repair target: the 5 P0 + 6 P1 findings, plus the P2 quick wins F5/F6/F7/F8 where the
  classification allowed an in-passing change. Code segment stays `allow` (unchanged).
- Quadruple (this round): `flow_class=execution`; `source=declaration`; `marker=`; `error=-`

## Summary

| Finding | Severity | Repair status | Evidence |
|---------|----------|---------------|----------|
| F1 / A1 / I1 — implement close-out skipped | P0 | **repaired** — `verification.md` populated; closure record produced | `verification.md`; `test-evidence/review-repair-r1-closure-verdict.txt` + `-payload.json` |
| A2 / I2 — SC-002 final-tree bidirectional diff non-empty | P0 | **repaired at the root** — fixture-isolation fix; both comm directions empty | `test-evidence/review-repair-r1-sc002-comm.txt`; `-trigger-fix.txt`; `notes/quickstart-run.md` § S-4 repair r1 |
| A3 / I3 — slot-1 baseline taken post-change | P1 | **repaired** — pre-change baseline rebuilt at the implement-entry commit; 92.4 % ≤ 110 % | `test-evidence/review-repair-r1-sc005-walls.txt`; `notes/pre-change-measurements.md` § 7 |
| F2 / F4 — stale state spine; checkpoints stop at plan | P1 | **repaired** — spine advanced to the live stage; checkpoints 04…08 written | state spine (`stage: review`, attempt 1, verdict recorded); `checkpoints/04-tasks.md`…`08-review.md` |
| A4 — T061 has no `deferred_tasks=` carrier | P1 | **repaired** — `deferred_tasks=T061 …` recorded | `verification.md` (record block) |
| F3 — baseline row scheduled last (structural) | P1 | **repaired for this slice** (rebuilt baseline); framework recommendation REC-098-01 registered, not applied here | `notes/pre-change-measurements.md` § 7; `review.md` § 5.1 |
| F5 — DoD status `pending` contradicted the rows | P2 | **repaired in passing** — DoD status names its remaining condition | `tasks.md` **DoD Status** line |
| F6 — receipt refuses a legal binary skip | P2 | **repaired** — skip selectors precede line measurement; mirror synced | `skills/internal/code-review/scripts/git-delta-review.sh` (+ `.specify` mirror); `test-evidence/review-repair-r1-f6-receipt.txt` |
| F7 — user-ruled constitution amendment unattributed | P2 | **repaired** — `D-098-01` registered | `.specify/register.md` |
| F8 — T012 scope says "obligations 1–11" | P2 | **repaired** — wording matches the row's evidence | `tasks.md` T012; `test-evidence/tier-contract-green.txt` § Scope note |

## 1. F1 / A1 / I1 (P0) — implement close-out

- **Defect**: `verification.md` absent; no SC rows, no smoke record, no `deferred_tasks=`;
  `closure-acceptance-check.py` exited 2; the `Planned → Implemented` four conditions had no
  evidence base.
- **Repair**: executed the implement Step 9 close-out on the current tree.
  `verification.md` now carries `SC-001…SC-011` `SC-NNN_status=` rows with value/note, the
  five ladder fields on the `partial` rows, exactly one smoke triple, `RS-004_joint_acceptance`,
  `deferred_tasks=T061 — driver closure stage after review; slot 2 of 2`, and the copied
  closure verdict. The smoke was re-executed for the record (exit 0, `86 passed in 34.74s`,
  transcript `test-evidence/verification-smoke-098.txt`).
- **Closure judgement (copied, not authored)**:
  - bare invocation exits 2: `no registry row for '098-suite-speed-optimizations'` — 098 is a
    follow-up spec bound to Feature 086 ("不新建、不改号"), so its claim lives in 086's detail
    file; the checker's declared `--feature-detail` input resolves it (calling surface C-02).
  - with `--feature-detail .specify/features/086-efficient-test-execution.md`: exit 1,
    verdict `block`; reasons `final-path-not-pass: SC-003`, `final-path-not-pass: SC-005`,
    `status-claims-implemented-but-blocked`; `final_path` pass 7 / partial 2 / total 9;
    conditions `no_open_rows=true`, `status_row_per_criterion=true`, `smoke_record_pass=true`,
    `every_final_path_pass=false`.
- **Status reading**: the record now exists and is honest. SC-003/SC-005 are `partial`
  because their readings are the closure stage's (T061, slot 2) by the task's own design —
  `tasks.md` GATE-4 states that the closure-stage rows supply those readings before the gate
  is re-read. No status was written to make the checker pass; the `block` verdict is copied
  verbatim.
- **Residual**: the transition still needs T061's closure legs — by design, not by defect.

## 2. A2 / I2 (P0) — SC-002 final-tree bidirectional comparison

- **Defect**: `comm -13` = 2 serial-only names in `tests/contract/test_trigger_engine.py`
  (`test_c20_new_session_is_not_suppressed`, `test_c21_auto_execute_is_only_a_flag`), a file
  the delta touched; the record substituted "0 new failure names", which is not SC-002.
- **Root cause (measured, not guessed)**: the engine's workspace resolution (contract C-7:
  explicit `--workspace` > engine self-location > nearest `.specify` CWD ancestor > CWD) lets
  **engine self-location win** when the engine's own path sits under a `.specify` directory —
  and this worktree lives inside the parent repository's `.specify/.tmp/`. Every
  `run_cli` call therefore wrote the parent repo's trigger store instead of the pytest
  fixture: shared telemetry accumulated session state and xdist workers raced on one
  `index.json`. The result was arm-dependent failures — the two serial-only names (and, in
  earlier observations, `test_c15_*`).
- **Repair (C-004's isolation-defect path)**: `run_cli` passes `--workspace <cwd>` unless the
  call already names one. C-7 keeps explicit `--workspace` first, so the engine contract is
  unchanged and the fixture resolves; on a normal checkout the CWD walk already resolved the
  fixture, so the change is behavior-neutral there. No assertion weakened, no test removed,
  no retry used.
- **Re-run (final tree, one run per arm, same tree, `tier=fast excluded_slow=5` both)**:
  parallel exit 1, wall 175.76 s, 137 names; serial exit 1, wall 557.04 s, 137 names;
  `comm -13` = **0**, `comm -23` = **0**.
- **Affected-file guard**: `bash scripts/bash/run-tests.sh tests/contract/test_trigger_engine.py -q`
  → exit 0, `145 passed in 7.46s`.
- **Residual**: none for SC-002; the failure-count drop (157/159 → 137/137) is disclosed as
  repair effect, and removals never violate a name-equality criterion.

## 3. A3 / I3 (P1) — pre-change baseline timing

- **Defect**: slot 1 (T003) executed at WP-9 on the post-WP-8 tree, so SC-005 compared
  post-change against post-change.
- **Repair**: rebuilt the baseline on a throwaway worktree at the **implement-entry commit**
  `af73f65f1` (parent of the first implement commit `0d1f7a1e4`;
  `git diff --stat b3da3a26d af73f65f1 -- tests/ scripts/ pyproject.toml` = the constitution
  version pin only). The old runner selects everything by construction (no `--full` flag at
  that tree). Run: exit 1, wall **76.52 s**, `279 failed, 8261 passed, 2 skipped in 42.21s`;
  names `test-evidence/review-repair-prechange-failed.txt` (279).
- **Final-tree leg**: `--full` run on the repaired tree: exit 1, wall **70.73 s**,
  `254 failed, 8332 passed, 2 skipped in 46.91s`; names
  `test-evidence/review-repair-final-failed.txt` (254).
- **SC-005 restated as pre-change baseline → final tree**: `70.73 / 76.52 = 92.4 %` ≤ 110 %.
  The two-slot-completeness half remains T061's, so SC-005 is `partial` (ladder recorded).
- **Name disclosure**: 1 new name vs the recorded slot-1 baseline
  (`test_tools_inventory_ownership.py::test_no_surface_claims_it_anywhere_in_the_repo`),
  isolated re-run green (`1 passed in 6.25s`) — load-induced, not a regression; 34 removals
  (27 trigger-file names from §2 plus load-variation reads).
- **Budget**: no third slot — slot 1 is re-constituted on its proper tree; the final-tree leg
  is this repair's authorized re-measurement; slot 2 (T061) untouched.
- **Teardown**: the throwaway worktree was removed after the run (`git worktree list` no
  longer lists it); its scratch output is gitignored.

## 4. F2 / F4 (P1) — state spine and checkpoints

- **Spine**: the loop-state machine block now reads `stage: review`,
  `stage_started_at: 1794333734` (review run start), `deadline: +10800 s`,
  `stage_base_commit: ea5962c87`, `attempt: 1`, `retry_limit: 3`, and a `last_verdict`
  describing the refusal + this repair. The human section's stale `stalled`/`requirements`
  lines were replaced with the live state. `loop-state.py --action snapshot --spine …`
  parses it: schema `v1`, state `running`, no missing required fields. (The engine's
  artifact-derived stage still reads `implement` — correct, because no `REVIEW-DONE` sentinel
  exists while the transition is refused.)
- **Checkpoints**: `04-tasks.md`, `05-checklist.md`, `06-analyze.md`, `07-implement.md`
  (with the four disclosed implement deviations), `08-review.md` (round 1 refusal + this
  repair's handoff). No stage completion is inferred from an executor's self-report.
- **Residual**: the driver's own runtime records (session / exec-quant / feedback) remain
  intentionally uncommitted per dispatch discipline.

## 5. A4 / F5 (P1/P2) — deferred-task carrier and DoD status

- `verification.md` now carries `deferred_tasks=T061 — driver closure stage after review;
  slot 2 of 2, not an implement-stage run` plus a one-line reason summary (DoD-1's carrier).
- `tasks.md` **DoD Status** is no longer a bare `pending`: it names the remaining condition
  (T061 + SC-003/SC-005 `partial`) and the close-out record. DoD is honestly **not met** —
  the DoD row itself requires every final SC `pass`.

## 6. F6 (P2) — receipt binary/skip ordering

- The `receipt` subcommand applied `--skip-with-reason` selectors only **after** summing
  `git diff --numstat`, so a legal `binary` skip exited 2 before the selector could apply.
- Repair: skip selectors are applied before the line-count loop; matched paths are excluded
  from `lines_added`/`lines_deleted` and never trigger the binary refusal; unmatched binary
  files still exit 2 (C-41 / V16 unchanged). Source
  `skills/internal/code-review/scripts/git-delta-review.sh`; mirror regenerated with
  `sync-mirrors.py --write --only skills/internal/code-review`; `--check` exit 0;
  files byte-identical.
- Drill (throwaway git fixture): with the selector → exit 0, `skipped_files=1`,
  `lines_added=3` (binary excluded); without it → exit 2 with the C-41 message (the
  pre-existing refusal preserved). Evidence `test-evidence/review-repair-r1-f6-receipt.txt`.
- Guards: `bash scripts/bash/run-tests.sh --workers 4 tests/contract/test_coverage_receipt.py
  tests/contract/test_code_review_skill_contract.py -q` → exit 0, `59 passed in 1.88s`.

## 7. F7 / F8 (P2) — register and task-scope wording

- F7: `.specify/register.md` gains `D-098-01` — the 2026-11-10 user ruling that amended
  constitution Principle VII's carrier (1.19.0 → 1.19.1), attributed to commit `af73f65f1`
  with the full statement path.
- F8: T012's scope now reads "obligations 1–10 plus the slow-membership guard cases as they
  exist at this row; obligation 11 lands with T021/T022" — matching
  `test-evidence/tier-contract-green.txt` § Scope note.

## Disclosures

- **Bare checker exit 2**: `closure-acceptance-check.py --spec-dir …` without a claim carrier
  is an input error for a follow-up spec with no registry row (098 is bound to 086). The
  record uses the checker's declared `--feature-detail` input; both invocations are archived.
- **Validator warnings**: `validate-tasks.py` on the repaired `tasks.md` = 0 errors /
  3 warnings (`green-cross-phase` on T017/T025/T040 rows this repair did not touch). The same
  three warnings exist on the pre-repair `tasks.md`; the tasks-stage gate record's "0 warnings"
  is a dated reading of an older validator state. No new warning was introduced.
- **Diagnostic side effect**: during root-cause diagnosis, two `trigger-utils.py init`
  invocations reconciled the **parent repository's** `.specify/memory/trigger/` store
  (idempotent seed reconcile + telemetry append, timestamp-only). The worktree's own
  `.specify/memory/trigger/index.json` was already dirty before this session; neither is part
  of the repair commit.
- **Design residue (by design, not defect)**: SC-003/SC-005 remain `partial` until T061's
  closure stage executes; `tasks.md` GATE-4 declares that the closure-stage rows supply those
  readings before the gate is re-read. The next review round judges a complete evidence base;
  the transition must not be forced ahead of the closure stage.
- **Framework recommendations**: REC-098-01…06 registered in `review.md` § 5 are framework-level
  changes (templates/skills) outside this slice's repair scope; they were not applied here.
