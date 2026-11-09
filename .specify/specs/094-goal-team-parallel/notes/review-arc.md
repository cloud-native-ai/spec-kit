# ARC review — 094-goal-team-parallel

**Role**: Acceptance Reality Check (read-only; this note is the only write) · **Tree**: MAIN
`/storage/project/cloud-native-ai/spec-kit` @ `19003b613` · **Date**: 2026-11-09 ·
**Mandate**: independently re-run the closure battery and spot-check three SC evidence chains,
then cross-check the registry claim against the closure verdict.

## 1. Closure verdict — measured vs claimed

**Measured (main tree, exit 0)** — `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/094-goal-team-parallel --feature-registry .specify/memory/features.md`:

```
verdict: accept
spec_dir: /storage/project/cloud-native-ai/spec-kit/.specify/specs/094-goal-team-parallel
flow_class: execution
claimed_status: Planned
final_path: pass=8 blocked=0 deferred=0 partial=0 fail=0 unknown=0 total=8
reason: none
```

**Claimed (notes/repairwave.md § 0, verbatim)**:

```
verdict: accept
spec_dir: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/094-repairwave/.specify/specs/094-goal-team-parallel
flow_class: execution
claimed_status: Planned
final_path: pass=8 blocked=0 deferred=0 partial=0 fail=0 unknown=0 total=8
reason: none
```

Agreement: identical except `spec_dir` (claimed was the repairwave worktree; measured is the
main tree — the expected difference). Machine-readable companion (`--json`):
`completion_conditions = {no_open_rows: true, status_row_per_criterion: true,
every_final_path_pass: true, smoke_record_pass: true}`; `tasks = {closed: 85, in_progress: 0,
open: 0, deferred: 0}`. The 8 final-path criteria are SC-002…SC-008 + SC-012 (SC-001 is
`supporting` under ruling R2; SC-009/010/011 are `supporting`).

## 2. Gate re-runs

| Gate | Command (main tree) | Measured | Claimed (repairwave) | Match |
|------|---------------------|----------|----------------------|-------|
| validate-requirements | `python3 .specify/scripts/python/validate-requirements.py .specify/specs/094-goal-team-parallel/requirements.md` | `status: ok`, 6/6 checks pass, `scanned: 331 lines, 55 definition rows, 6 shared strings`, 0 error / 0 warning, exit 0 | 331 / 55 / 6, 0/0 | yes |
| validate-tasks | `python3 .specify/scripts/python/validate-tasks.py .specify/specs/094-goal-team-parallel/tasks.md` | `PASS (with warnings)` — 0 errors, 1 warning: `240: blockedBy: T043 references later task T054 (forward dependency — verify this is intentional)`, exit 0 | 0 errors / 1 warning (same row) | yes |
| validate-decision-tensions | `python3 .specify/scripts/python/validate-decision-tensions.py --spec .specify/specs/094-goal-team-parallel` | `status: ok`, 6/6 checks pass, `scanned: 374 lines, 7 record(s)`, 0/0, exit 0 | 7 records, 0 findings | yes |
| pre-analyze — requirements | `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/094-goal-team-parallel --stage requirements --repo .` | `stage=requirements decision=pass errors=0 advisories=20 waived=0`; summary `fr 43 / sc 12 / tasks 85 / files 13`, exit 0 | pass, errors 0, advisories 20 | yes |
| pre-analyze — plan | same, `--stage plan` | `stage=plan decision=pass errors=0 advisories=20 waived=0`; fr 43 / sc 12 / tasks 85, exit 0 | same | yes |
| pre-analyze — tasks | same, `--stage tasks` | `stage=tasks decision=pass errors=0 advisories=20 waived=0`; fr 43 / sc 12 / tasks 85, exit 0 | same | yes |
| decomposition — plan | `python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode plan --requirements .specify/specs/094-goal-team-parallel/requirements.md` | `{"decision": "proceed", "measured": {"fr_count": 43, "task_count": null, "fr_ceiling": 120, "task_ceiling": 160}, "reasons": []}`, exit 0 | proceed (fr 43) | yes |
| decomposition — tasks | same, `--mode tasks --tasks .specify/specs/094-goal-team-parallel/tasks.md` | `{"decision": "proceed", "measured": {"fr_count": 43, "task_count": 85, ...}, "reasons": []}`, exit 0 | proceed (fr 43 / tasks 85) | yes |

Task sigils measured directly: `^- [ ]` = 0, `^- [>]` = 0, `^- [x]` = 85. Smoke record:
`test-evidence/wp07-smoke.out` exists (99 B; `54 passed in 7.15s`).

## 3. SC evidence chains — end to end

### SC-003 (migration receipts) — claim supported

- Claim: apply = 16 decisions (8 goal + 8 teams), migrated 16 / conflict 0 / interrupted 0,
  exit 0; post `probe-residual` goal 0 / teams 0; existence 16/16; idempotent second apply =
  16 noop / 0 migrated / exit 0 / byte-identical.
- Recorded chain (read): `test-evidence/repairwave-T079-apply.txt` (counts block matches),
  `repairwave-T079-probe-after.json` (0/0), `repairwave-T079-existence.txt`
  (`pass=16 fail=0 total=16`), `repairwave-T079-idempotent.txt` (`second-exit=0`,
  `{"migrated": 0, "noop": 16, "conflict": 0, "interrupted": 0}`, `byte-diff ... NONE`).
- Independent re-verification: `goal-utils.py probe-residual --json` → goal 0 / teams 0
  (exit 0); 16 receipts on disk (8 `goal-*`, 8 `teams-*`), all 16 `target_path` files and
  all 16 `archived_path` directories exist; none of the 16 `source_path` values from the
  apply reading still exists; every receipt carries `delete_policy: archive-not-delete` and
  `result: migrated`; `git ls-files` tracks 16 receipts. The second `--apply` was read from
  its record, not re-executed (a write outside the ARC mandate); its noop precondition
  (16 targets present + 16 receipts) is measured true.
- Verdict: SC-003 `pass` is supported.

### SC-002 (stale pin) — claim supported

- Claim: `tests/contract/test_no_spec_local_writes.py` 4 passed; action sets agree at 10
  actions incl. `handoff-ref`; both mutation arms red-on-revert.
- Independent: `EXPECTED_WRITE_ACTIONS` (test file lines 41–44) = 10 members incl.
  `handoff-ref`; `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest ... -q -p no:cacheprovider` →
  `4 passed`, exit 0, including `test_the_guard_goes_red_when_one_surface_is_reverted` and
  `test_the_vocabulary_scan_goes_red_when_one_old_phrase_is_re_injected`.
- Verdict: SC-002 `pass` is supported.

### SC-010 (disposal wave) — guard green, criterion overclaimed

- Claim: 12-row disposal table complete; no module outside table + `FEATURE_MODULES`;
  wp06's `test_framework_map_archive_row.py` + `test_goal_command_template.py` admitted;
  rows 1/2/3/6/9/11 rewritten; 17 disposal-family ids + guard green; `SC-010_status=pass`.
- Independent: table at tasks.md § 085 disposal table has 12 rows;
  `FEATURE_MODULES` (test_085_disposal_table.py lines 53–72) contains both wp06 modules;
  targeted run of the guard + the six rewritten modules = **44 passed**, exit 0
  (`test_085_disposal_table` 2, `test_scope_resolution` 9, `test_temp_goal_contract` 8,
  `test_temp_team_schema` 9, `test_goal_scope_engine` 9, `test_checkpoint_protocol` 6,
  `test_checkpoint_rollback` 1).
- **Disagreement**: requirements.md SC-010 line 207 demands “处置后全套契约测试在 `>=3.8`
  上全绿” and its Source (line 222) names “处置后的 `pytest -m contract` 读数”. The
  criterion's own implementation reading, `test-evidence/wp05-contract-post-disposal.txt`,
  records `# exit status: 1` with 86 failing ids (93 lines; `new-vs-baseline: 51`); the
  post-wave full-suite reading is `186 failed / 8199 passed / 2 skipped`. The contract
  suite is therefore not literally all green on this tree. `verification.md` SC-010_note
  discloses that the limb is “decided by its own implementation (T065's guard)” as
  zero-new-failing-ids on the disposal surface; no ratified SC-010 clarification exists in
  requirements.md § Clarifications (R1 covers SC-003/T079, R2 covers SC-001). The guard's
  zero-new-failing-ids property is measured green; the literal all-green limb is measured
  false. Since SC-010 is `supporting`, the closure verdict is unaffected, but the recorded
  `pass` overclaims the criterion as written — `partial` is the honest status, or the SC
  needs an explicit user ruling narrowing it (the R2 pattern).
- Verdict: SC-010 `pass` not sustained against its own criterion text; supporting path, so
  no verdict change.

## 4. Registry row vs closure verdict

- `.specify/memory/features.md` row 094: Status cell = `Planned` (header:
  `ID | Name | Description | Status | Feature Details | Spec Path | Last Updated`). The
  closure check's `claimed_status: Planned` is read from that file
  (`claimed_status_source` = features.md).
- Verdict = `accept`, and all four `Planned → Implemented` conjunctive conditions are
  measured true (`no_open_rows`, `status_row_per_criterion`, `every_final_path_pass`,
  `smoke_record_pass`), with 85/85 task rows closed.
- Ownership: `.specify/shared/workflow/feature-integration.md` § Status State Machine —
  `/speckit.implement` owns `Planned → Implemented` (after its § Pre-Status-Flip Gate);
  `/speckit.review` owns `Implemented → Ready for Review`; there is **no**
  `Planned → Ready for Review` transition. The closure check does not block a claim lower
  than the evidence (its claimed-status reason fires only when an Implemented-family claim
  exceeds evidence).
- Judgement: the mismatch is **acceptable only as a transient pre-transition state**. It is
  a lower claim, not an overclaim, and the verdict is the implement-stage gate; the
  registry flip (status + `Last Updated` in the same pass) is owed by the
  review/integration transition and MUST land before review records `Ready for Review`.
  It is not acceptable as the terminal state.

Secondary record readings:

- `verification.md` human view (line 120) labels SC-012 `supporting`; requirements.md
  SC-012 `Path` is `final`, and the closure check counts it in `final_path` total 8. The
  record block is correct; the rendered table row is wrong (presentation only).
- `.specify/memory/features/094.md` Plan Notes still says `tasks.md 83 行（T001–T083）`;
  measured is 85 rows (T084/T085 landed with wp05). Stale detail line, not a closure input.

## 5. Carried residuals (disclosed; not independently re-measured here)

- Final GATE-1 main-tree reading “after every `.specify/.tmp` fixture and worktree is
  removed” remains owed: `.specify/.tmp` still holds `sdd-loop/worktrees/093-*` and
  `tmp/gate1-094-*` files (notes/repairwave.md § 5 item 1).
- Worktree suite runs mutated the MAIN repo's `.specify/memory/trigger/index.json`
  (repairwave § 5 item 2; wp07 ANOMALY 1).
- `.specify/specs/088-speckit-visualization/team/team.md` (one-level non-conforming) sits
  outside the probe glob and the migration (repairwave § 5 item 4).
- Pre-existing red families outside this feature's causal surface stay on the recorded
  baseline (repairwave § 5 item 3); they are not claimed by any 094 criterion.

## 6. ARC verdict

**ACCEPT sustained.** The closure verdict reproduces byte-for-byte in the main tree except
`spec_dir`; every stage gate matches its recorded reading; SC-003 and SC-002 chains verify
end to end; SC-010's guard surface is green. One status-level disagreement (SC-010 `pass`
against its literal all-green limb) and two record-hygiene items are recorded above; none
changes the final-path verdict. The registry `Planned` row is a legal pre-transition claim
that the review/integration transition must flip before `Ready for Review`.

**ANOMALY: `SC-010_status=pass` overclaims its criterion — the recorded post-disposal contract reading is exit 1 with 86 failing ids, while SC-010 requires the whole contract suite all green; supporting path, so the 8/8 closure verdict stands, but the status should be `partial` or the SC narrowed by an explicit user ruling (R2 pattern).**
