# 086 Dogfood Record — 085 Temporary Goal/Team used by this run (T039)

Owner of the propositions this file carries:
`.specify/specs/086-efficient-test-execution/contracts/dogfood-and-preservation.contract.md`
C-048 (per-stage record shape), C-049 (`actual_concurrency_max > 1` from dispatch records),
C-050 (SC-010 status follows the evidence), C-051 (carrier downgrade is an observation).
The 085 mechanisms recorded here are owned by
`.specify/specs/085-sdd-temporary-goal-team/` and are not restated.

Provenance of every number below: the 086 checkpoints
(`.specify/specs/086-efficient-test-execution/checkpoints/01-…-10-…md`), the stage dispatch records, and
— for the implement stage — this executor's own dispatch and the driver briefs; **not** the declared
`agent_concurrency_requested: 24`. The distinction matters: C-049 fails a record that copies the
declared value into `effective`.

Recorded at: 2026-11-06, during WP-C1 (implement stage, integration slice C).

## 1. Stage table (C-048)

Terminology: `requested` = the value declared in
`team/086-efficient-test-execution/team.md` → `config.agent_concurrency.requested`;
`team_effective` = the team's configured `config.agent_concurrency.effective` (the ceiling after the
verifier reserve); `stage_effective` = what the next-stage decision in the preceding checkpoint set for
that stage; `actual_concurrency_max` = the largest number of agents actually observed running at one time
for that stage, read from the dispatch records.

| Stage | Carrier identity (host-native) | requested | team_effective | stage_effective | actual_concurrency_max | checkpoint | completion state |
|-------|-------------------------------|-----------|----------------|-----------------|------------------------|------------|------------------|
| requirements | `SDD Requirements Executor` | 24 | 18 | 2 | 1 (one analyzer; the driver's U4 verified afterwards) | `checkpoints/01-requirements.md` | complete (`REQUIREMENTS-DONE`) |
| clarify | `general-purpose` | 24 | 18 | 2 | 1 | `checkpoints/02-clarify.md` | complete (`CLARIFY-DONE`) |
| plan | `SDD Executor` | 24 | 18 | 2 | 1 | `checkpoints/03-plan.md` | complete (`PLAN-DONE`) |
| tasks | `SDD Executor` | 24 | 18 | 2 | 1 | `checkpoints/04-tasks.md` | complete (`TASKS-DONE`) |
| checklist | `general-purpose` / `SDD Executor` | 24 | 18 | 2 | 1 | `checkpoints/05-checklist.md` | complete (`CHECKLIST-DONE`) |
| analyze | `general-purpose` / `SDD Executor` | 24 | 18 | 2 | 1 | `checkpoints/06-analyze.md` | complete (`ANALYZE-DONE`) |
| implement (preflight + wave 1) | `sdd-implement-executor` (host-native `SDD Executor`) | 24 | 18 | 3 (wave 1: A1+B1+verifier) | **2** (A1 ∥ B1) | `checkpoints/07-implement-preflight.md`, `checkpoints/08-implement-wave1.md` | complete |
| implement (wave 2) | `sdd-implement-executor` (host-native `SDD Executor`) | 24 | 18 | 4 (A2+A3+B2+verifier) | **3** (A2 ∥ A3 ∥ B2) | `checkpoints/09-implement-wave2.md` | complete |
| implement (wave 3) | `sdd-implement-executor` (host-native `SDD Executor`) | 24 | 18 | 3 (A4+B3+verifier) | **2** (A4 ∥ B3) | `checkpoints/10-implement-wave3.md` | complete |
| implement (wave 4) | `sdd-implement-executor` (host-native `SDD Executor`) | 24 | 18 | 2 (C1 + verifier reserve) | 1 (C1 alone; the stage is measured against the whole tree) | `checkpoints/11-implement-wave4.md` | complete (`C1-DONE`; the driver's `--dist` guard repair followed) |
| implement (wave 5 — closure) | `sdd-implement-executor` (host-native `SDD Executor`) | 24 | 18 | 2 (C2 + verifier reserve) | 1 (C2 alone; one integration slice) | `checkpoints/12-implement-closure.md` | complete (`C2-DONE`; nine gates pass, `closure-acceptance-check.py` accept) |
| review | `SDD Executor` (host-native) | 24 | 18 | 2 (review seat + verifier reserve) | 1 (one review seat; the driver's U4 verified afterwards) | `checkpoints/13-review.md` | complete (`REVIEW-DONE`; four segments pass, ARC `agree`, `Ready for Review`) |

## 2. `agent_concurrency_effective` and the named reason (C-048)

Three distinct numbers are in play and only one of them is evidence of concurrency:

1. `requested: 24` — declared in the team file. **Not** used anywhere in this record as an observation.
2. `effective: 18`, `reason: verifier-reserve` — the team's configured ceiling
   (`team.md` → `config.agent_concurrency`). It is a budget, not an observation: it was never binding,
   because no stage had 18 ready packages.
3. The **stage's** effective value, decided in the preceding checkpoint's § 4 and named with its reason
   when it is lower than the team ceiling:

| Stage | stage_effective | named reason it is lower than 18 |
|-------|-----------------|-----------------------------------|
| requirements | 2 | one ready analyzer package + 1 verifier reserve |
| clarify | 2 | one ready clarify package + 1 verifier reserve |
| plan | 2 | one plan coordinator + 1 verifier reserve |
| tasks | 2 | one ready tasks work package + 1 verifier reserve |
| checklist | 2 | one ready checklist work package + 1 verifier reserve |
| analyze | 2 | one ready analyze work package + 1 verifier reserve |
| implement wave 1 | 3 | two file-disjoint build packages (A1 ∥ B1) + 1 verifier reserve |
| implement wave 2 | 4 | three file-disjoint packages (A2 ∥ A3 ∥ B2) + 1 verifier reserve |
| implement wave 3 | 3 | two file-disjoint packages (A4 ∥ B3) + 1 verifier reserve |
| implement wave 4 (C1) | 2 | one integration slice (C1) + 1 verifier reserve; C runs alone because it measures the whole tree |

The plan's dependency graph — not a host limit — is what caps every stage below 18: A and B are
file-disjoint and run together, C integrates after both.

## 3. Actual concurrency from dispatch records (C-049)

- **Maximum observed: 3** (implement wave 2 — A2, A3 and B2 in flight simultaneously; recorded in
  `checkpoints/09-implement-wave2.md` § 1 "actual concurrency 3").
- Wave 1: **2** (A1 ∥ B1) — `checkpoints/08-implement-wave1.md` § 1.
- Wave 3: **2** (A4 ∥ B3) — `checkpoints/10-implement-wave3.md` § 1 "actual concurrency 2".
- Stages 01–06: **1** each (one package ready at a time; the driver's U4 verification follows the
  stage, so it is not concurrent with the executor).
- Wave 4 (this record's stage): **1** — the C1 executor runs alone by design.

`actual_concurrency_max > 1` therefore holds for **three** stages (wave 1, wave 2, wave 3), which
satisfies C-049 on the wave-1/2/3 evidence independently of this file's own stage.

Child lines opened and closed by this run (085 line registry): `086-wp-a1`, `086-wp-b1` (wave 1);
`086-wp-a2`, `086-wp-a3`, `086-wp-b2` (wave 2); `086-wp-a4`, `086-wp-b3` (wave 3); `086-wp-c1` (wave 4,
this one). Each ran in its own worktree under `~/tmp/spec-kit/086/worktrees/<child_line_id>` and merged
through the 085 integration queue — data recorded per wave in the checkpoint files.

## 4. Branch / worktree / integration / checkpoint observations (C-042)

- **Worktrees**: one per child line, outside `repo_root`. Observation: 085 C-008 names
  `.specify/.tmp/` as the child-worktree root, but the line registry rejects a worktree path inside
  `repo_root`, so the driver uses `~/tmp/spec-kit/086/worktrees/`. Recorded as a 085 dogfood observation;
  **no 085 file was edited** (C-041).
- **Integration**: base `ac8d5dcf`; waves fast-forwarded (A1, A2, A4) or rebased then fast-forwarded
  (A3, B2, B3) through the queue; worktrees removed and child lines closed after each merge.
- **Checkpoints**: `01-requirements` … `10-implement-wave3` exist before this slice; this slice's
  checkpoint is the driver's `11-implement-wave4`. Every stage that completed in this run has one.
- **Team-stale-line observation**: the 081 line (feature already `Completed`) was still registered as
  active and was released with `--evidence-ref features/081.md` before A2 could register. An observation
  about the registry's staleness, not a 085 defect repaired here.

## 5. Carrier downgrade (C-051) — observation, not a 085 failure, not repaired

The host running this SDD line does not expose Feature 085's stage-agent types. Each stage was therefore
executed by a **host-native carrier** (named per stage in § 1): `SDD Requirements Executor` (requirements),
`general-purpose` (clarify, checklist, analyze), `SDD Executor` (plan, tasks, implement). The mechanisms
085 owns — spec-local temporary Goal and Team, `agent_concurrency_*`, worktree write isolation, the
integration queue, per-stage checkpoints — were all created and used.

This is a **carrier downgrade**: only the agent *identity* is supplied by the host. Per `plan.md`
§ 085 Carrier Observation (A19b) and C-051 it is recorded here as an observation. It is **not** recorded as
a 085 failure, and the host's agent roster is **not** repaired in this feature (FR-027, FR-017).

## 6. 085 preservation re-run (C-043)

The five 085 contract/integration files were re-run unchanged (zero edits), under the default-parallel
runner:

```
env -u PYTHONPATH SPECKIT_PYTHON=/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.venv/bin/python \
  bash scripts/bash/run-tests.sh --names-out .specify/.tmp/086/c1-preservation-085.txt -q \
  tests/contract/test_temp_goal_contract.py tests/contract/test_temp_team_schema.py \
  tests/contract/test_checkpoint_protocol.py tests/integration/test_temp_team_worktree_queue.py \
  tests/integration/test_checkpoint_rollback.py
```

Result: `# test runner: mode=parallel workers=auto dist=load passes=1`, **20 passed**, exit 0,
failed-name list **0 entries**. New failure names against `test-evidence/baseline-failed.txt`: **0** (the
baseline's 19 names are all in `tests/contract/` outside these five files). Full logs and the byte-identity
half of C-041 are owned by `.specify/specs/086-efficient-test-execution/test-evidence/preservation-085.txt`
(WP-C2); this section records only the re-run result that C-043 asks for.

## 7. 085 SC-010 status (C-050)

The dogfood chain C-050 requires: every stage has a record (§ 1), a checkpoint each (§ 1 + § 4), and
C-049 satisfied (§ 3, max actual concurrency 3). Per C-050, on that chain **085 SC-010 qualifies for
`pass`**, with the carrier downgrade recorded as an observation rather than a failure (§ 5). The
status line is flipped at feature closure on this record: the chain now covers all eight stages
(requirements → review), each with a checkpoint (`01-requirements` … `13-review`), and the concurrency
observation comes from dispatch records (maximum 3, implement wave 2).

## 8. Not claimed by this record

- No 085 file was modified, moved or deleted by this work package.
- No concurrency number here was taken from `requested: 24`; every `actual_concurrency_max` cites the
  wave it was observed in.
- The reviewer stage has run (checkpoint `13-review.md`, `review.md`, `code-review.md`); its verdict is
  `Ready for Review`, code `blocking 0`, and its P1 findings are framework-improvement material
  recorded in `review.md` § 3.
