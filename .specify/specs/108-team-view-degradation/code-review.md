# Code Review Report — 代码段 (code segment)

| 属性 | 值 |
|------|-----|
| **分支** | `108-team-view-degradation` |
| **基准** | `54c6efa8c9a93a107400a0256504a5f3169f5c04` (`54c6efa8c`) |
| **目标** | `4262522f4e3eaeb4b0a8caac25f0e1c1211c5708` (`4262522f4`) |
| **基准来源** | `feature-first-commit` |
| **渲染模式** | `renderer: text` |
| **Reviewer** | `Qiming Liu (John)` |
| **日期** | `2026-11-26T13:10:16Z` |

## 变更概览

```
 .specify/agents/.render-manifest.json              |   2 +-
 .../anchoring/108-team-view-degradation/anchor.md  |  26 +
 .../records/20261126T072644224940Z-874b8c89.json   |   1 +
 .../records/20261126T081948513263Z-654bcce0.json   |   1 +
 .../records/20261126T083330495519Z-84b1aa89.json   |   1 +
 .../records/20261126T084427478702Z-bea2028a.json   |   1 +
 .../records/20261126T085258314890Z-0b6e405f.json   |   1 +
 .../records/20261126T090913272888Z-8c4b973c.json   |   1 +
 .../records/20261126T092410989193Z-8491c499.json   |   1 +
 .../records/20261126T094006906283Z-80e01547.json   |   1 +
 .../records/20261126T125523893293Z-3464cb2b.json   |   1 +
 .specify/features.md                               |   3 +-
 .specify/features/027-team-management.md           |   7 +-
 .../20261126T071944Z-skill-sdd-loop-driver.md      |  21 +
 .../20261126T071947Z-skill-analyze-artifacts.md    |  21 +
 .../20261126T071947Z-skill-create-requirements.md  |  21 +
 .../20261126T071947Z-skill-sdd-loop-driver.md      |  21 +
 .../feedback/20261126T071950Z-skill-create-team.md |  21 +
 .../20261126T071950Z-skill-manage-features.md      |  21 +
 .../20261126T071950Z-skill-sdd-loop-driver.md      |  21 +
 .../20261126T072656Z-speckit-requirements.md       |  22 +
 .../feedback/20261126T082001Z-speckit-clarify.md   |  23 +
 .specify/feedback/20261126T083347Z-speckit-plan.md |  24 +
 .../feedback/20261126T084451Z-speckit-tasks.md     |  25 +
 .../feedback/20261126T085303Z-speckit-checklist.md |  25 +
 .../20261126T090913Z-skill-analyze-artifacts.md    |  25 +
 .../20261126T092426Z-skill-analyze-artifacts.md    |  31 +
 .../20261126T094007Z-skill-analyze-artifacts.md    |  27 +
 .../20261126T125545Z-skill-implement-feature.md    |  26 +
 ...T072711Z-r20261126T071500Z-108a-requirements.md |  59 ++
 ...61126T082034Z-r20261126T071500Z-108a-clarify.md |  42 ++
 ...20261126T083410Z-r20261126T071500Z-108a-plan.md |  51 ++
 ...0261126T084501Z-r20261126T071500Z-108a-tasks.md |  51 ++
 ...126T085314Z-r20261126T071500Z-108a-checklist.md |  54 ++
 ...42Z-108-team-view-degradation-analyze-repair.md |  60 ++
 ...T125603Z-108-team-view-degradation-implement.md |  31 +
 .specify/scripts/python/team-view.py               | 375 ++++++++--
 ...ination-speckit-tasks-r20261125t022857z-06dd.md |  10 +-
 ...ation-speckit-clarify-r20261125t113505z-106a.md |  10 +-
 ...mination-speckit-plan-r20261125t113505z-106a.md |  10 +-
 ...ination-speckit-tasks-r20261125t113505z-106a.md |  10 +-
 ...ion-speckit-checklist-r20261125t113505z-106a.md |  10 +-
 ...n-speckit-requirements-r20261126t071500z-108.md | 208 ++++++
 ...ation-speckit-clarify-r20261126t071500z-108a.md | 203 ++++++
 ...mination-speckit-plan-r20261126t071500z-108a.md | 207 ++++++
 ...ination-speckit-tasks-r20261126t071500z-108a.md | 190 +++++
 ...ion-speckit-checklist-r20261126t071500z-108a.md | 207 ++++++
 ...on-skill-analyze-artifacts-r20261126t090814z.md | 209 ++++++
 ...on-skill-analyze-artifacts-r20261126t092355z.md | 215 ++++++
 ...on-skill-analyze-artifacts-r20261126t093658z.md | 202 ++++++
 ...on-skill-implement-feature-r20261126t071500z.md | 201 ++++++
 .specify/skills/internal/view-team/SKILL.md        |   3 +-
 .../108-team-view-degradation/baseline-failed.txt  | 221 ++++++
 .../checklists/requirements-quality-2026-11-26.md  |  94 +++
 .../checklists/requirements.md                     |  49 ++
 .../checkpoints/01-requirements.md                 |  23 +
 .../checkpoints/02-clarify.md                      |   5 +
 .../checkpoints/03-plan.md                         |   9 +
 .../checkpoints/04-tasks.md                        |   5 +
 .../checkpoints/05-goal-team-activation.md         |   7 +
 .../checkpoints/07-analyze.md                      |   5 +
 .../checkpoints/08-implement.md                    |   7 +
 .../contracts/presentation.contract.md             |  40 ++
 .../contracts/report-recognition.contract.md       |  36 +
 .../contracts/team-view-program.contract.md        |  42 ++
 .../contracts/view-labels.contract.md              |  51 ++
 .../coverage-baseline.txt                          | 787 +++++++++++++++++++++
 .../specs/108-team-view-degradation/data-model.md  | 166 +++++
 .../specs/108-team-view-degradation/feature-ref.md |  77 ++
 .../specs/108-team-view-degradation/handoff.md     |  47 ++
 .../specs/108-team-view-degradation/notes/.gitkeep |   0
 .../notes/pre-change-measurements.md               | 130 ++++
 .../notes/quickstart-run.md                        | 128 ++++
 .../notes/red-first-evidence.md                    | 237 +++++++
 .../108-team-view-degradation/notes/us1-green.txt  |  26 +
 .../108-team-view-degradation/notes/us2-green.txt  |  59 ++
 .../108-team-view-degradation/notes/us3-green.txt  | 113 +++
 .specify/specs/108-team-view-degradation/plan.md   | 155 ++++
 .../specs/108-team-view-degradation/quickstart.md  | 153 ++++
 .../108-team-view-degradation/requirements.md      | 238 +++++++
 .../specs/108-team-view-degradation/research.md    | 143 ++++
 .specify/specs/108-team-view-degradation/tasks.md  | 331 +++++++++
 .../test-evidence/analyze-domain-w1-r2.jsonl       |   6 +
 .../test-evidence/analyze-domain-w1-r3.jsonl       |   6 +
 .../test-evidence/analyze-domain-w1.jsonl          |   6 +
 .../test-evidence/analyze-domain-w2-r2.jsonl       |   6 +
 .../test-evidence/analyze-domain-w2-r3.jsonl       |   6 +
 .../test-evidence/analyze-domain-w2.jsonl          |   6 +
 .../test-evidence/analyze-domain-w3-r2.jsonl       |   6 +
 .../test-evidence/analyze-domain-w3-r3.jsonl       |   6 +
 .../test-evidence/analyze-domain-w3.jsonl          |   6 +
 .../analyze-final-report-r4-2026-11-26.md          |   6 +
 .../test-evidence/analyze-incremental-r4.jsonl     |   4 +
 .../test-evidence/analyze-repair-2026-11-26.md     |  78 ++
 .../analyze-repair-decomposition-plan.json         |  12 +
 .../analyze-repair-decomposition-plan.txt          |   1 +
 .../analyze-repair-decomposition-tasks.json        |  12 +
 .../analyze-repair-decomposition-tasks.txt         |   1 +
 .../test-evidence/analyze-repair-exec-quant.txt    |   1 +
 .../analyze-repair-feedback-record.txt             |   9 +
 .../analyze-repair-feedback-status.txt             |  10 +
 .../analyze-repair-pre-analyze-plan.json           | 507 +++++++++++++
 .../analyze-repair-pre-analyze-plan.txt            |   2 +
 .../analyze-repair-pre-analyze-requirements.json   | 507 +++++++++++++
 .../analyze-repair-pre-analyze-requirements.txt    |   2 +
 .../analyze-repair-pre-analyze-tasks.json          | 507 +++++++++++++
 .../analyze-repair-pre-analyze-tasks.txt           |   2 +
 .../analyze-repair-requirements-validator.txt      |  10 +
 .../analyze-repair-resolution-probe.txt            |  38 +
 .../analyze-repair-run-determination.txt           |   8 +
 .../analyze-repair-tasks-validator.txt             |   1 +
 .../analyze-repair-workspace-before.json           | 311 ++++++++
 .../analyze-repair-workspace-postcommit.json       | 311 ++++++++
 .../analyze-repair-workspace-postcommit.txt        |   1 +
 .../analyze-repair-workspace-precommit.txt         |   1 +
 .../test-evidence/analyze-repair2-2026-11-26.md    |  68 ++
 .../analyze-repair2-decomposition-plan.json        |  12 +
 .../analyze-repair2-decomposition-plan.txt         |   1 +
 .../analyze-repair2-decomposition-tasks.json       |  12 +
 .../analyze-repair2-decomposition-tasks.txt        |   1 +
 .../test-evidence/analyze-repair2-exec-quant.txt   |   1 +
 .../analyze-repair2-feedback-record.txt            |   9 +
 .../analyze-repair2-feedback-status.txt            |  10 +
 .../analyze-repair2-pre-analyze-plan.json          | 507 +++++++++++++
 .../analyze-repair2-pre-analyze-plan.txt           |   2 +
 .../analyze-repair2-pre-analyze-requirements.json  | 507 +++++++++++++
 .../analyze-repair2-pre-analyze-requirements.txt   |   2 +
 .../analyze-repair2-pre-analyze-tasks.json         | 507 +++++++++++++
 .../analyze-repair2-pre-analyze-tasks.txt          |   2 +
 .../analyze-repair2-requirements-validator.txt     |  10 +
 .../analyze-repair2-resolution-probe.txt           |  52 ++
 .../analyze-repair2-run-determination.txt          |   8 +
 .../analyze-repair2-tasks-validator.txt            |   1 +
 .../analyze-repair2-workspace-before.json          | 311 ++++++++
 .../analyze-repair2-workspace-postcommit.json      | 311 ++++++++
 .../analyze-repair2-workspace-postcommit.txt       |   1 +
 .../analyze-repair2-workspace-precommit.txt        |   1 +
 .../test-evidence/analyze-repair3-2026-11-26.md    |  62 ++
 .../analyze-repair3-decomposition-plan.json        |  12 +
 .../analyze-repair3-decomposition-plan.txt         |   1 +
 .../analyze-repair3-decomposition-tasks.json       |  12 +
 .../analyze-repair3-decomposition-tasks.txt        |   1 +
 .../test-evidence/analyze-repair3-exec-quant.txt   |   1 +
 .../analyze-repair3-feedback-record.txt            |   9 +
 .../analyze-repair3-feedback-status.txt            |  10 +
 .../analyze-repair3-pre-analyze-plan.json          | 507 +++++++++++++
 .../analyze-repair3-pre-analyze-plan.txt           |   2 +
 .../analyze-repair3-pre-analyze-requirements.json  | 507 +++++++++++++
 .../analyze-repair3-pre-analyze-requirements.txt   |   2 +
 .../analyze-repair3-pre-analyze-tasks.json         | 507 +++++++++++++
 .../analyze-repair3-pre-analyze-tasks.txt          |   2 +
 .../analyze-repair3-resolution-probe.txt           |  35 +
 .../analyze-repair3-run-determination.txt          |   8 +
 .../analyze-repair3-tasks-validator.txt            |   1 +
 .../analyze-repair3-workspace-before.json          | 311 ++++++++
 .../analyze-repair3-workspace-postcommit.json      | 311 ++++++++
 .../analyze-repair3-workspace-postcommit.txt       |   1 +
 .../analyze-repair3-workspace-precommit.txt        |   1 +
 .../test-evidence/analyze.jsonl                    |   1 +
 ...checklist-requirements-validator-postcommit.txt |  10 +
 .../checklist-requirements-validator.txt           |  10 +
 .../checklist-selfcheck-postcommit.txt             |   4 +
 .../test-evidence/checklist-selfcheck.txt          |  16 +
 .../test-evidence/checklist-spec-readings.txt      |  25 +
 .../test-evidence/checklist-stage-2026-11-26.md    |  65 ++
 .../checklist-stage-addendum-2026-11-26.md         |  13 +
 .../test-evidence/checklist.jsonl                  |   1 +
 .../test-evidence/clarify-stage-2026-11-26.md      |  53 ++
 .../test-evidence/clarify-validator-postcommit.txt |  11 +
 .../test-evidence/clarify-validator.txt            |  11 +
 .../test-evidence/clarify.jsonl                    |   1 +
 .../test-evidence/decomposition-plan.json          |  12 +
 .../test-evidence/decomposition-requirements.json  |   1 +
 .../test-evidence/decomposition-tasks.json         |   1 +
 .../test-evidence/goal-team-activation.txt         |   7 +
 .../test-evidence/implement-entry-readings.txt     |  59 ++
 .../test-evidence/implement-integration.md         | 169 +++++
 .../test-evidence/plan-decision-tensions.txt       |  11 +
 .../test-evidence/plan-gates.txt                   |  19 +
 .../test-evidence/plan-stage-2026-11-26.md         |  71 ++
 .../test-evidence/plan.jsonl                       |   1 +
 .../test-evidence/pre-analyze-checklist.txt        |   5 +
 .../pre-analyze-clarify-postcommit.json            |  16 +
 .../pre-analyze-clarify-postcommit.txt             |   3 +
 .../test-evidence/pre-analyze-clarify.json         |  16 +
 .../test-evidence/pre-analyze-clarify.txt          |   3 +
 .../test-evidence/pre-analyze-plan-postcommit.json | 353 +++++++++
 .../test-evidence/pre-analyze-plan-postcommit.txt  |   2 +
 .../test-evidence/pre-analyze-plan.json            | 353 +++++++++
 .../test-evidence/pre-analyze-plan.txt             |   2 +
 .../pre-analyze-requirements-postcommit.json       |   1 +
 .../pre-analyze-requirements-postcommit.txt        |   2 +
 .../test-evidence/pre-analyze-requirements.json    |   2 +
 .../pre-analyze-tasks-postcommit.json              |   1 +
 .../test-evidence/pre-analyze-tasks-postcommit.txt |   1 +
 .../test-evidence/pre-analyze-tasks.json           |   1 +
 .../test-evidence/pre-analyze-tasks.txt            |   1 +
 .../test-evidence/requirements-stage-2026-11-26.md |  42 ++
 .../requirements-validator-postcommit.txt          |  10 +
 .../test-evidence/requirements-validator.txt       |  10 +
 .../test-evidence/shape-change-guard.txt           |  36 +
 .../test-evidence/sync-mirrors-after.txt           |  13 +
 .../test-evidence/sync-mirrors-baseline.txt        |  19 +
 .../test-evidence/targeted-current-failed.txt      |   0
 .../test-evidence/targeted-set.txt                 |  44 ++
 .../test-evidence/tasks-stage-2026-11-26.md        |  71 ++
 .../test-evidence/tasks-validator-postcommit.txt   |   1 +
 .../test-evidence/tasks-validator.txt              |   1 +
 .../test-evidence/tasks.jsonl                      |   1 +
 .../test-evidence/us1-red-integration.txt          | 281 ++++++++
 .../test-evidence/us1-red-unit.txt                 | 135 ++++
 .../test-evidence/us2-red-degraded.txt             | 137 ++++
 .../test-evidence/us2-red-states.txt               |  95 +++
 .../test-evidence/us3-guards.txt                   |   8 +
 .../test-evidence/us3-red-contract.txt             |  36 +
 .../test-evidence/verification-input.md            |  63 ++
 .../workspace-checklist-check-vs-tasks.json        |   1 +
 .../workspace-checklist-postcommit.json            | 311 ++++++++
 .../workspace-checklist-postcommit.txt             |   1 +
 .../test-evidence/workspace-checklist-readings.txt |   1 +
 .../test-evidence/workspace-checklist.json         | 311 ++++++++
 .../workspace-clarify-postcommit.json              | 311 ++++++++
 .../test-evidence/workspace-clarify-postcommit.txt |   2 +
 .../test-evidence/workspace-clarify-readings.txt   |   8 +
 .../test-evidence/workspace-clarify.json           | 311 ++++++++
 .../test-evidence/workspace-plan-postcommit.json   |   1 +
 .../test-evidence/workspace-plan-postcommit.txt    |   1 +
 .../workspace-plan-poststage-driver.json           | 311 ++++++++
 .../test-evidence/workspace-plan-readings.txt      |   1 +
 .../test-evidence/workspace-plan.json              |   1 +
 .../workspace-requirements-postcommit.json         | 311 ++++++++
 .../workspace-requirements-postcommit.txt          |   9 +
 .../workspace-requirements-readings.txt            |  14 +
 .../test-evidence/workspace-requirements.json      | 311 ++++++++
 .../workspace-tasks-check-vs-plan.json             |   1 +
 .../test-evidence/workspace-tasks-postcommit.json  | 311 ++++++++
 .../test-evidence/workspace-tasks-postcommit.txt   |   1 +
 .../test-evidence/workspace-tasks-readings.txt     |   1 +
 .../test-evidence/workspace-tasks.json             | 311 ++++++++
 .../108-team-view-degradation/writeback/T001.yaml  |   5 +
 .../108-team-view-degradation/writeback/T002.yaml  |   5 +
 .../108-team-view-degradation/writeback/T003.yaml  |   5 +
 .../108-team-view-degradation/writeback/T004.yaml  |   5 +
 .../108-team-view-degradation/writeback/T005.yaml  |   5 +
 .../108-team-view-degradation/writeback/T006.yaml  |   5 +
 .../108-team-view-degradation/writeback/T007.yaml  |   5 +
 .../108-team-view-degradation/writeback/T008.yaml  |   5 +
 .../108-team-view-degradation/writeback/T009.yaml  |   5 +
 .../108-team-view-degradation/writeback/T010.yaml  |   5 +
 .../108-team-view-degradation/writeback/T011.yaml  |   5 +
 .../108-team-view-degradation/writeback/T012.yaml  |   5 +
 .../108-team-view-degradation/writeback/T013.yaml  |   5 +
 .../108-team-view-degradation/writeback/T014.yaml  |   5 +
 .../108-team-view-degradation/writeback/T015.yaml  |   5 +
 .../108-team-view-degradation/writeback/T016.yaml  |   5 +
 .../108-team-view-degradation/writeback/T017.yaml  |   5 +
 .../108-team-view-degradation/writeback/T018.yaml  |   5 +
 .specify/teams/108-team-view-degradation/team.md   | 149 ++++
 docs/reference/commands/team.md                    |  32 +
 scripts/python/team-view.py                        | 375 ++++++++--
 skills/internal/view-team/SKILL.md                 |   3 +-
 .../test_team_view_degradation_contract.py         | 519 ++++++++++++++
 tests/integration/test_team_view_degradation.py    | 754 ++++++++++++++++++++
 tests/unit/test_team_view_report_recognition.py    | 174 +++++
 264 files changed, 20562 insertions(+), 172 deletions(-)
```

---

## Review 意见


### 🟢 [SUGGESTION] scripts/python/team-view.py (Line 1104)

> The inventory's `unreadable` flag is computed with os.access() while the rendering's readability state comes from build_latest()'s actual read attempt — two mechanisms for one fact that can disagree (ACL/root edge cases). The envelope could carry a wrong readability fact while the human rendering is right. Derive the inventory flag from the same read attempt (or drop it and keep the build_latest record as the single readability source).

<sub>21:10:31</sub>


### 🟢 [SUGGESTION] scripts/python/team-view.py (Line 174)

> SLUG_FORM_RE re-implements the shared identity grammar whose executable owner is goal-utils.py's is_valid_identity (authored statement: shared/definitions/goal-definitions.md § Identity grammar). The regex matches the owner's statement today, but nothing pins the equivalence: if the owner grammar changes, the view's copy drifts silently. Add a parity assertion against the owner function on shared samples (and a few reverse samples), or derive the check from the owner.

<sub>21:10:31</sub>


### 🟢 [SUGGESTION] tests/contract/test_team_view_degradation_contract.py (Line 135)

> test_reason_set_is_closed pins the emitted degradation codes by regex over the program's source text ("code": "..."). A refactor that assembles the code from a constant or variable would escape the scan while the behaviour changes; the behavioural mapping test covers only the reasons that exist today, so the closure claim would weaken silently. Consider an AST-based scan or asserting an explicit reason-constant set.

<sub>21:10:31</sub>


### ⚪ [NITPICK] tests/unit/test_team_view_report_recognition.py (Line 129)

> test_residue_presentation_is_bounded injects residue names through the fixture builder's reports= argument, which reads as a contradiction at the call site (residue passed as reports). A names=/files= helper or a one-line comment would keep the fixture intent visible without reading classify_run_file first.

<sub>21:10:31</sub>


### 👍 [PRAISE] scripts/python/team-view.py

> The recognition core is compact and single-entry: one compiled grammar, strptime for calendar validation instead of hand-rolled date math, a fixed three-way classifier, and a stable name-ascending tie-break. The healthy-fidelity guard runs the materialized baseline program (not a hash) and the zero-write guard snapshots before/after — the right evidence shapes for the claims.

<sub>21:10:31</sub>


### 👍 [PRAISE] tests/integration/test_team_view_degradation.py

> Both healthy variants (goal absent / goal slug) are exercised against the baseline program with read-only sibling modules, and the degraded fixture asserts all six named states plus the zero-fabricated-value absence checks. Genuine red-first captures back the US1/US2/US3 slots.

<sub>21:10:31</sub>


> **未提交范围（未评审）**: 5 个未提交路径未计入本次评审对象（.specify/specs/108-team-view-degradation/test-evidence/review-quickstart.txt, .specify/specs/108-team-view-degradation/test-evidence/review-smoke.txt, .specify/specs/108-team-view-degradation/test-evidence/review-targeted-failed.txt, .specify/specs/108-team-view-degradation/test-evidence/review-targeted.txt, .specify/specs/108-team-view-degradation/verification.md）；本回执不对该范围给出任何结论。

<!-- coverage-receipt:begin -->
receipt_version=1
base=54c6efa8c9a93a107400a0256504a5f3169f5c04
head=4262522f4e3eaeb4b0a8caac25f0e1c1211c5708
base_source=feature-first-commit
renderer=text
changed_files=264
judged_files=6
skipped_files=258
gap_files=0
lines_added=1785
lines_deleted=72
file.001.path=.specify/agents/.render-manifest.json
file.001.verdict=skipped
file.001.reason=generated
file.002.path=.specify/anchoring/108-team-view-degradation/anchor.md
file.002.verdict=skipped
file.002.reason=non-code-file
file.003.path=.specify/exec-quant/records/20261126T072644224940Z-874b8c89.json
file.003.verdict=skipped
file.003.reason=non-code-file
file.004.path=.specify/exec-quant/records/20261126T081948513263Z-654bcce0.json
file.004.verdict=skipped
file.004.reason=non-code-file
file.005.path=.specify/exec-quant/records/20261126T083330495519Z-84b1aa89.json
file.005.verdict=skipped
file.005.reason=non-code-file
file.006.path=.specify/exec-quant/records/20261126T084427478702Z-bea2028a.json
file.006.verdict=skipped
file.006.reason=non-code-file
file.007.path=.specify/exec-quant/records/20261126T085258314890Z-0b6e405f.json
file.007.verdict=skipped
file.007.reason=non-code-file
file.008.path=.specify/exec-quant/records/20261126T090913272888Z-8c4b973c.json
file.008.verdict=skipped
file.008.reason=non-code-file
file.009.path=.specify/exec-quant/records/20261126T092410989193Z-8491c499.json
file.009.verdict=skipped
file.009.reason=non-code-file
file.010.path=.specify/exec-quant/records/20261126T094006906283Z-80e01547.json
file.010.verdict=skipped
file.010.reason=non-code-file
file.011.path=.specify/exec-quant/records/20261126T125523893293Z-3464cb2b.json
file.011.verdict=skipped
file.011.reason=non-code-file
file.012.path=.specify/features.md
file.012.verdict=skipped
file.012.reason=non-code-file
file.013.path=.specify/features/027-team-management.md
file.013.verdict=skipped
file.013.reason=non-code-file
file.014.path=.specify/feedback/20261126T071944Z-skill-sdd-loop-driver.md
file.014.verdict=skipped
file.014.reason=non-code-file
file.015.path=.specify/feedback/20261126T071947Z-skill-analyze-artifacts.md
file.015.verdict=skipped
file.015.reason=non-code-file
file.016.path=.specify/feedback/20261126T071947Z-skill-create-requirements.md
file.016.verdict=skipped
file.016.reason=non-code-file
file.017.path=.specify/feedback/20261126T071947Z-skill-sdd-loop-driver.md
file.017.verdict=skipped
file.017.reason=non-code-file
file.018.path=.specify/feedback/20261126T071950Z-skill-create-team.md
file.018.verdict=skipped
file.018.reason=non-code-file
file.019.path=.specify/feedback/20261126T071950Z-skill-manage-features.md
file.019.verdict=skipped
file.019.reason=non-code-file
file.020.path=.specify/feedback/20261126T071950Z-skill-sdd-loop-driver.md
file.020.verdict=skipped
file.020.reason=non-code-file
file.021.path=.specify/feedback/20261126T072656Z-speckit-requirements.md
file.021.verdict=skipped
file.021.reason=non-code-file
file.022.path=.specify/feedback/20261126T082001Z-speckit-clarify.md
file.022.verdict=skipped
file.022.reason=non-code-file
file.023.path=.specify/feedback/20261126T083347Z-speckit-plan.md
file.023.verdict=skipped
file.023.reason=non-code-file
file.024.path=.specify/feedback/20261126T084451Z-speckit-tasks.md
file.024.verdict=skipped
file.024.reason=non-code-file
file.025.path=.specify/feedback/20261126T085303Z-speckit-checklist.md
file.025.verdict=skipped
file.025.reason=non-code-file
file.026.path=.specify/feedback/20261126T090913Z-skill-analyze-artifacts.md
file.026.verdict=skipped
file.026.reason=non-code-file
file.027.path=.specify/feedback/20261126T092426Z-skill-analyze-artifacts.md
file.027.verdict=skipped
file.027.reason=non-code-file
file.028.path=.specify/feedback/20261126T094007Z-skill-analyze-artifacts.md
file.028.verdict=skipped
file.028.reason=non-code-file
file.029.path=.specify/feedback/20261126T125545Z-skill-implement-feature.md
file.029.verdict=skipped
file.029.reason=non-code-file
file.030.path=.specify/retention/closeout/20261126T072711Z-r20261126T071500Z-108a-requirements.md
file.030.verdict=skipped
file.030.reason=non-code-file
file.031.path=.specify/retention/closeout/20261126T082034Z-r20261126T071500Z-108a-clarify.md
file.031.verdict=skipped
file.031.reason=non-code-file
file.032.path=.specify/retention/closeout/20261126T083410Z-r20261126T071500Z-108a-plan.md
file.032.verdict=skipped
file.032.reason=non-code-file
file.033.path=.specify/retention/closeout/20261126T084501Z-r20261126T071500Z-108a-tasks.md
file.033.verdict=skipped
file.033.reason=non-code-file
file.034.path=.specify/retention/closeout/20261126T085314Z-r20261126T071500Z-108a-checklist.md
file.034.verdict=skipped
file.034.reason=non-code-file
file.035.path=.specify/retention/closeout/20261126T090942Z-108-team-view-degradation-analyze-repair.md
file.035.verdict=skipped
file.035.reason=non-code-file
file.036.path=.specify/retention/closeout/20261126T125603Z-108-team-view-degradation-implement.md
file.036.verdict=skipped
file.036.reason=non-code-file
file.037.path=.specify/scripts/python/team-view.py
file.037.verdict=skipped
file.037.reason=generated
file.038.path=.specify/session/20261125T032803Z-run-determination-speckit-tasks-r20261125t022857z-06dd.md
file.038.verdict=skipped
file.038.reason=non-code-file
file.039.path=.specify/session/20261125T115445Z-run-determination-speckit-clarify-r20261125t113505z-106a.md
file.039.verdict=skipped
file.039.reason=non-code-file
file.040.path=.specify/session/20261125T121417Z-run-determination-speckit-plan-r20261125t113505z-106a.md
file.040.verdict=skipped
file.040.reason=non-code-file
file.041.path=.specify/session/20261125T122808Z-run-determination-speckit-tasks-r20261125t113505z-106a.md
file.041.verdict=skipped
file.041.reason=non-code-file
file.042.path=.specify/session/20261125T123550Z-run-determination-speckit-checklist-r20261125t113505z-106a.md
file.042.verdict=skipped
file.042.reason=non-code-file
file.043.path=.specify/session/20261126T072639Z-run-determination-speckit-requirements-r20261126t071500z-108.md
file.043.verdict=skipped
file.043.reason=non-code-file
file.044.path=.specify/session/20261126T081931Z-run-determination-speckit-clarify-r20261126t071500z-108a.md
file.044.verdict=skipped
file.044.reason=non-code-file
file.045.path=.specify/session/20261126T083327Z-run-determination-speckit-plan-r20261126t071500z-108a.md
file.045.verdict=skipped
file.045.reason=non-code-file
file.046.path=.specify/session/20261126T084427Z-run-determination-speckit-tasks-r20261126t071500z-108a.md
file.046.verdict=skipped
file.046.reason=non-code-file
file.047.path=.specify/session/20261126T085243Z-run-determination-speckit-checklist-r20261126t071500z-108a.md
file.047.verdict=skipped
file.047.reason=non-code-file
file.048.path=.specify/session/20261126T090909Z-run-determination-skill-analyze-artifacts-r20261126t090814z.md
file.048.verdict=skipped
file.048.reason=non-code-file
file.049.path=.specify/session/20261126T092407Z-run-determination-skill-analyze-artifacts-r20261126t092355z.md
file.049.verdict=skipped
file.049.reason=non-code-file
file.050.path=.specify/session/20261126T094004Z-run-determination-skill-analyze-artifacts-r20261126t093658z.md
file.050.verdict=skipped
file.050.reason=non-code-file
file.051.path=.specify/session/20261126T125520Z-run-determination-skill-implement-feature-r20261126t071500z.md
file.051.verdict=skipped
file.051.reason=non-code-file
file.052.path=.specify/skills/internal/view-team/SKILL.md
file.052.verdict=skipped
file.052.reason=generated
file.053.path=.specify/specs/108-team-view-degradation/baseline-failed.txt
file.053.verdict=skipped
file.053.reason=non-code-file
file.054.path=.specify/specs/108-team-view-degradation/checklists/requirements-quality-2026-11-26.md
file.054.verdict=skipped
file.054.reason=non-code-file
file.055.path=.specify/specs/108-team-view-degradation/checklists/requirements.md
file.055.verdict=skipped
file.055.reason=non-code-file
file.056.path=.specify/specs/108-team-view-degradation/checkpoints/01-requirements.md
file.056.verdict=skipped
file.056.reason=non-code-file
file.057.path=.specify/specs/108-team-view-degradation/checkpoints/02-clarify.md
file.057.verdict=skipped
file.057.reason=non-code-file
file.058.path=.specify/specs/108-team-view-degradation/checkpoints/03-plan.md
file.058.verdict=skipped
file.058.reason=non-code-file
file.059.path=.specify/specs/108-team-view-degradation/checkpoints/04-tasks.md
file.059.verdict=skipped
file.059.reason=non-code-file
file.060.path=.specify/specs/108-team-view-degradation/checkpoints/05-goal-team-activation.md
file.060.verdict=skipped
file.060.reason=non-code-file
file.061.path=.specify/specs/108-team-view-degradation/checkpoints/07-analyze.md
file.061.verdict=skipped
file.061.reason=non-code-file
file.062.path=.specify/specs/108-team-view-degradation/checkpoints/08-implement.md
file.062.verdict=skipped
file.062.reason=non-code-file
file.063.path=.specify/specs/108-team-view-degradation/contracts/presentation.contract.md
file.063.verdict=skipped
file.063.reason=non-code-file
file.064.path=.specify/specs/108-team-view-degradation/contracts/report-recognition.contract.md
file.064.verdict=skipped
file.064.reason=non-code-file
file.065.path=.specify/specs/108-team-view-degradation/contracts/team-view-program.contract.md
file.065.verdict=skipped
file.065.reason=non-code-file
file.066.path=.specify/specs/108-team-view-degradation/contracts/view-labels.contract.md
file.066.verdict=skipped
file.066.reason=non-code-file
file.067.path=.specify/specs/108-team-view-degradation/coverage-baseline.txt
file.067.verdict=skipped
file.067.reason=non-code-file
file.068.path=.specify/specs/108-team-view-degradation/data-model.md
file.068.verdict=skipped
file.068.reason=non-code-file
file.069.path=.specify/specs/108-team-view-degradation/feature-ref.md
file.069.verdict=skipped
file.069.reason=non-code-file
file.070.path=.specify/specs/108-team-view-degradation/handoff.md
file.070.verdict=skipped
file.070.reason=non-code-file
file.071.path=.specify/specs/108-team-view-degradation/notes/.gitkeep
file.071.verdict=skipped
file.071.reason=non-code-file
file.072.path=.specify/specs/108-team-view-degradation/notes/pre-change-measurements.md
file.072.verdict=skipped
file.072.reason=non-code-file
file.073.path=.specify/specs/108-team-view-degradation/notes/quickstart-run.md
file.073.verdict=skipped
file.073.reason=non-code-file
file.074.path=.specify/specs/108-team-view-degradation/notes/red-first-evidence.md
file.074.verdict=skipped
file.074.reason=non-code-file
file.075.path=.specify/specs/108-team-view-degradation/notes/us1-green.txt
file.075.verdict=skipped
file.075.reason=non-code-file
file.076.path=.specify/specs/108-team-view-degradation/notes/us2-green.txt
file.076.verdict=skipped
file.076.reason=non-code-file
file.077.path=.specify/specs/108-team-view-degradation/notes/us3-green.txt
file.077.verdict=skipped
file.077.reason=non-code-file
file.078.path=.specify/specs/108-team-view-degradation/plan.md
file.078.verdict=skipped
file.078.reason=non-code-file
file.079.path=.specify/specs/108-team-view-degradation/quickstart.md
file.079.verdict=skipped
file.079.reason=non-code-file
file.080.path=.specify/specs/108-team-view-degradation/requirements.md
file.080.verdict=skipped
file.080.reason=non-code-file
file.081.path=.specify/specs/108-team-view-degradation/research.md
file.081.verdict=skipped
file.081.reason=non-code-file
file.082.path=.specify/specs/108-team-view-degradation/tasks.md
file.082.verdict=skipped
file.082.reason=non-code-file
file.083.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-domain-w1-r2.jsonl
file.083.verdict=skipped
file.083.reason=non-code-file
file.084.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-domain-w1-r3.jsonl
file.084.verdict=skipped
file.084.reason=non-code-file
file.085.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-domain-w1.jsonl
file.085.verdict=skipped
file.085.reason=non-code-file
file.086.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-domain-w2-r2.jsonl
file.086.verdict=skipped
file.086.reason=non-code-file
file.087.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-domain-w2-r3.jsonl
file.087.verdict=skipped
file.087.reason=non-code-file
file.088.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-domain-w2.jsonl
file.088.verdict=skipped
file.088.reason=non-code-file
file.089.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-domain-w3-r2.jsonl
file.089.verdict=skipped
file.089.reason=non-code-file
file.090.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-domain-w3-r3.jsonl
file.090.verdict=skipped
file.090.reason=non-code-file
file.091.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-domain-w3.jsonl
file.091.verdict=skipped
file.091.reason=non-code-file
file.092.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-final-report-r4-2026-11-26.md
file.092.verdict=skipped
file.092.reason=non-code-file
file.093.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-incremental-r4.jsonl
file.093.verdict=skipped
file.093.reason=non-code-file
file.094.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair-2026-11-26.md
file.094.verdict=skipped
file.094.reason=non-code-file
file.095.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair-decomposition-plan.json
file.095.verdict=skipped
file.095.reason=non-code-file
file.096.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair-decomposition-plan.txt
file.096.verdict=skipped
file.096.reason=non-code-file
file.097.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair-decomposition-tasks.json
file.097.verdict=skipped
file.097.reason=non-code-file
file.098.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair-decomposition-tasks.txt
file.098.verdict=skipped
file.098.reason=non-code-file
file.099.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair-exec-quant.txt
file.099.verdict=skipped
file.099.reason=non-code-file
file.100.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair-feedback-record.txt
file.100.verdict=skipped
file.100.reason=non-code-file
file.101.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair-feedback-status.txt
file.101.verdict=skipped
file.101.reason=non-code-file
file.102.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair-pre-analyze-plan.json
file.102.verdict=skipped
file.102.reason=non-code-file
file.103.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair-pre-analyze-plan.txt
file.103.verdict=skipped
file.103.reason=non-code-file
file.104.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair-pre-analyze-requirements.json
file.104.verdict=skipped
file.104.reason=non-code-file
file.105.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair-pre-analyze-requirements.txt
file.105.verdict=skipped
file.105.reason=non-code-file
file.106.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair-pre-analyze-tasks.json
file.106.verdict=skipped
file.106.reason=non-code-file
file.107.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair-pre-analyze-tasks.txt
file.107.verdict=skipped
file.107.reason=non-code-file
file.108.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair-requirements-validator.txt
file.108.verdict=skipped
file.108.reason=non-code-file
file.109.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair-resolution-probe.txt
file.109.verdict=skipped
file.109.reason=non-code-file
file.110.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair-run-determination.txt
file.110.verdict=skipped
file.110.reason=non-code-file
file.111.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair-tasks-validator.txt
file.111.verdict=skipped
file.111.reason=non-code-file
file.112.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair-workspace-before.json
file.112.verdict=skipped
file.112.reason=non-code-file
file.113.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair-workspace-postcommit.json
file.113.verdict=skipped
file.113.reason=non-code-file
file.114.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair-workspace-postcommit.txt
file.114.verdict=skipped
file.114.reason=non-code-file
file.115.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair-workspace-precommit.txt
file.115.verdict=skipped
file.115.reason=non-code-file
file.116.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair2-2026-11-26.md
file.116.verdict=skipped
file.116.reason=non-code-file
file.117.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair2-decomposition-plan.json
file.117.verdict=skipped
file.117.reason=non-code-file
file.118.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair2-decomposition-plan.txt
file.118.verdict=skipped
file.118.reason=non-code-file
file.119.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair2-decomposition-tasks.json
file.119.verdict=skipped
file.119.reason=non-code-file
file.120.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair2-decomposition-tasks.txt
file.120.verdict=skipped
file.120.reason=non-code-file
file.121.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair2-exec-quant.txt
file.121.verdict=skipped
file.121.reason=non-code-file
file.122.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair2-feedback-record.txt
file.122.verdict=skipped
file.122.reason=non-code-file
file.123.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair2-feedback-status.txt
file.123.verdict=skipped
file.123.reason=non-code-file
file.124.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair2-pre-analyze-plan.json
file.124.verdict=skipped
file.124.reason=non-code-file
file.125.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair2-pre-analyze-plan.txt
file.125.verdict=skipped
file.125.reason=non-code-file
file.126.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair2-pre-analyze-requirements.json
file.126.verdict=skipped
file.126.reason=non-code-file
file.127.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair2-pre-analyze-requirements.txt
file.127.verdict=skipped
file.127.reason=non-code-file
file.128.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair2-pre-analyze-tasks.json
file.128.verdict=skipped
file.128.reason=non-code-file
file.129.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair2-pre-analyze-tasks.txt
file.129.verdict=skipped
file.129.reason=non-code-file
file.130.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair2-requirements-validator.txt
file.130.verdict=skipped
file.130.reason=non-code-file
file.131.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair2-resolution-probe.txt
file.131.verdict=skipped
file.131.reason=non-code-file
file.132.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair2-run-determination.txt
file.132.verdict=skipped
file.132.reason=non-code-file
file.133.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair2-tasks-validator.txt
file.133.verdict=skipped
file.133.reason=non-code-file
file.134.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair2-workspace-before.json
file.134.verdict=skipped
file.134.reason=non-code-file
file.135.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair2-workspace-postcommit.json
file.135.verdict=skipped
file.135.reason=non-code-file
file.136.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair2-workspace-postcommit.txt
file.136.verdict=skipped
file.136.reason=non-code-file
file.137.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair2-workspace-precommit.txt
file.137.verdict=skipped
file.137.reason=non-code-file
file.138.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair3-2026-11-26.md
file.138.verdict=skipped
file.138.reason=non-code-file
file.139.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair3-decomposition-plan.json
file.139.verdict=skipped
file.139.reason=non-code-file
file.140.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair3-decomposition-plan.txt
file.140.verdict=skipped
file.140.reason=non-code-file
file.141.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair3-decomposition-tasks.json
file.141.verdict=skipped
file.141.reason=non-code-file
file.142.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair3-decomposition-tasks.txt
file.142.verdict=skipped
file.142.reason=non-code-file
file.143.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair3-exec-quant.txt
file.143.verdict=skipped
file.143.reason=non-code-file
file.144.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair3-feedback-record.txt
file.144.verdict=skipped
file.144.reason=non-code-file
file.145.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair3-feedback-status.txt
file.145.verdict=skipped
file.145.reason=non-code-file
file.146.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair3-pre-analyze-plan.json
file.146.verdict=skipped
file.146.reason=non-code-file
file.147.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair3-pre-analyze-plan.txt
file.147.verdict=skipped
file.147.reason=non-code-file
file.148.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair3-pre-analyze-requirements.json
file.148.verdict=skipped
file.148.reason=non-code-file
file.149.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair3-pre-analyze-requirements.txt
file.149.verdict=skipped
file.149.reason=non-code-file
file.150.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair3-pre-analyze-tasks.json
file.150.verdict=skipped
file.150.reason=non-code-file
file.151.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair3-pre-analyze-tasks.txt
file.151.verdict=skipped
file.151.reason=non-code-file
file.152.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair3-resolution-probe.txt
file.152.verdict=skipped
file.152.reason=non-code-file
file.153.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair3-run-determination.txt
file.153.verdict=skipped
file.153.reason=non-code-file
file.154.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair3-tasks-validator.txt
file.154.verdict=skipped
file.154.reason=non-code-file
file.155.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair3-workspace-before.json
file.155.verdict=skipped
file.155.reason=non-code-file
file.156.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair3-workspace-postcommit.json
file.156.verdict=skipped
file.156.reason=non-code-file
file.157.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair3-workspace-postcommit.txt
file.157.verdict=skipped
file.157.reason=non-code-file
file.158.path=.specify/specs/108-team-view-degradation/test-evidence/analyze-repair3-workspace-precommit.txt
file.158.verdict=skipped
file.158.reason=non-code-file
file.159.path=.specify/specs/108-team-view-degradation/test-evidence/analyze.jsonl
file.159.verdict=skipped
file.159.reason=non-code-file
file.160.path=.specify/specs/108-team-view-degradation/test-evidence/checklist-requirements-validator-postcommit.txt
file.160.verdict=skipped
file.160.reason=non-code-file
file.161.path=.specify/specs/108-team-view-degradation/test-evidence/checklist-requirements-validator.txt
file.161.verdict=skipped
file.161.reason=non-code-file
file.162.path=.specify/specs/108-team-view-degradation/test-evidence/checklist-selfcheck-postcommit.txt
file.162.verdict=skipped
file.162.reason=non-code-file
file.163.path=.specify/specs/108-team-view-degradation/test-evidence/checklist-selfcheck.txt
file.163.verdict=skipped
file.163.reason=non-code-file
file.164.path=.specify/specs/108-team-view-degradation/test-evidence/checklist-spec-readings.txt
file.164.verdict=skipped
file.164.reason=non-code-file
file.165.path=.specify/specs/108-team-view-degradation/test-evidence/checklist-stage-2026-11-26.md
file.165.verdict=skipped
file.165.reason=non-code-file
file.166.path=.specify/specs/108-team-view-degradation/test-evidence/checklist-stage-addendum-2026-11-26.md
file.166.verdict=skipped
file.166.reason=non-code-file
file.167.path=.specify/specs/108-team-view-degradation/test-evidence/checklist.jsonl
file.167.verdict=skipped
file.167.reason=non-code-file
file.168.path=.specify/specs/108-team-view-degradation/test-evidence/clarify-stage-2026-11-26.md
file.168.verdict=skipped
file.168.reason=non-code-file
file.169.path=.specify/specs/108-team-view-degradation/test-evidence/clarify-validator-postcommit.txt
file.169.verdict=skipped
file.169.reason=non-code-file
file.170.path=.specify/specs/108-team-view-degradation/test-evidence/clarify-validator.txt
file.170.verdict=skipped
file.170.reason=non-code-file
file.171.path=.specify/specs/108-team-view-degradation/test-evidence/clarify.jsonl
file.171.verdict=skipped
file.171.reason=non-code-file
file.172.path=.specify/specs/108-team-view-degradation/test-evidence/decomposition-plan.json
file.172.verdict=skipped
file.172.reason=non-code-file
file.173.path=.specify/specs/108-team-view-degradation/test-evidence/decomposition-requirements.json
file.173.verdict=skipped
file.173.reason=non-code-file
file.174.path=.specify/specs/108-team-view-degradation/test-evidence/decomposition-tasks.json
file.174.verdict=skipped
file.174.reason=non-code-file
file.175.path=.specify/specs/108-team-view-degradation/test-evidence/goal-team-activation.txt
file.175.verdict=skipped
file.175.reason=non-code-file
file.176.path=.specify/specs/108-team-view-degradation/test-evidence/implement-entry-readings.txt
file.176.verdict=skipped
file.176.reason=non-code-file
file.177.path=.specify/specs/108-team-view-degradation/test-evidence/implement-integration.md
file.177.verdict=skipped
file.177.reason=non-code-file
file.178.path=.specify/specs/108-team-view-degradation/test-evidence/plan-decision-tensions.txt
file.178.verdict=skipped
file.178.reason=non-code-file
file.179.path=.specify/specs/108-team-view-degradation/test-evidence/plan-gates.txt
file.179.verdict=skipped
file.179.reason=non-code-file
file.180.path=.specify/specs/108-team-view-degradation/test-evidence/plan-stage-2026-11-26.md
file.180.verdict=skipped
file.180.reason=non-code-file
file.181.path=.specify/specs/108-team-view-degradation/test-evidence/plan.jsonl
file.181.verdict=skipped
file.181.reason=non-code-file
file.182.path=.specify/specs/108-team-view-degradation/test-evidence/pre-analyze-checklist.txt
file.182.verdict=skipped
file.182.reason=non-code-file
file.183.path=.specify/specs/108-team-view-degradation/test-evidence/pre-analyze-clarify-postcommit.json
file.183.verdict=skipped
file.183.reason=non-code-file
file.184.path=.specify/specs/108-team-view-degradation/test-evidence/pre-analyze-clarify-postcommit.txt
file.184.verdict=skipped
file.184.reason=non-code-file
file.185.path=.specify/specs/108-team-view-degradation/test-evidence/pre-analyze-clarify.json
file.185.verdict=skipped
file.185.reason=non-code-file
file.186.path=.specify/specs/108-team-view-degradation/test-evidence/pre-analyze-clarify.txt
file.186.verdict=skipped
file.186.reason=non-code-file
file.187.path=.specify/specs/108-team-view-degradation/test-evidence/pre-analyze-plan-postcommit.json
file.187.verdict=skipped
file.187.reason=non-code-file
file.188.path=.specify/specs/108-team-view-degradation/test-evidence/pre-analyze-plan-postcommit.txt
file.188.verdict=skipped
file.188.reason=non-code-file
file.189.path=.specify/specs/108-team-view-degradation/test-evidence/pre-analyze-plan.json
file.189.verdict=skipped
file.189.reason=non-code-file
file.190.path=.specify/specs/108-team-view-degradation/test-evidence/pre-analyze-plan.txt
file.190.verdict=skipped
file.190.reason=non-code-file
file.191.path=.specify/specs/108-team-view-degradation/test-evidence/pre-analyze-requirements-postcommit.json
file.191.verdict=skipped
file.191.reason=non-code-file
file.192.path=.specify/specs/108-team-view-degradation/test-evidence/pre-analyze-requirements-postcommit.txt
file.192.verdict=skipped
file.192.reason=non-code-file
file.193.path=.specify/specs/108-team-view-degradation/test-evidence/pre-analyze-requirements.json
file.193.verdict=skipped
file.193.reason=non-code-file
file.194.path=.specify/specs/108-team-view-degradation/test-evidence/pre-analyze-tasks-postcommit.json
file.194.verdict=skipped
file.194.reason=non-code-file
file.195.path=.specify/specs/108-team-view-degradation/test-evidence/pre-analyze-tasks-postcommit.txt
file.195.verdict=skipped
file.195.reason=non-code-file
file.196.path=.specify/specs/108-team-view-degradation/test-evidence/pre-analyze-tasks.json
file.196.verdict=skipped
file.196.reason=non-code-file
file.197.path=.specify/specs/108-team-view-degradation/test-evidence/pre-analyze-tasks.txt
file.197.verdict=skipped
file.197.reason=non-code-file
file.198.path=.specify/specs/108-team-view-degradation/test-evidence/requirements-stage-2026-11-26.md
file.198.verdict=skipped
file.198.reason=non-code-file
file.199.path=.specify/specs/108-team-view-degradation/test-evidence/requirements-validator-postcommit.txt
file.199.verdict=skipped
file.199.reason=non-code-file
file.200.path=.specify/specs/108-team-view-degradation/test-evidence/requirements-validator.txt
file.200.verdict=skipped
file.200.reason=non-code-file
file.201.path=.specify/specs/108-team-view-degradation/test-evidence/shape-change-guard.txt
file.201.verdict=skipped
file.201.reason=non-code-file
file.202.path=.specify/specs/108-team-view-degradation/test-evidence/sync-mirrors-after.txt
file.202.verdict=skipped
file.202.reason=non-code-file
file.203.path=.specify/specs/108-team-view-degradation/test-evidence/sync-mirrors-baseline.txt
file.203.verdict=skipped
file.203.reason=non-code-file
file.204.path=.specify/specs/108-team-view-degradation/test-evidence/targeted-current-failed.txt
file.204.verdict=skipped
file.204.reason=non-code-file
file.205.path=.specify/specs/108-team-view-degradation/test-evidence/targeted-set.txt
file.205.verdict=skipped
file.205.reason=non-code-file
file.206.path=.specify/specs/108-team-view-degradation/test-evidence/tasks-stage-2026-11-26.md
file.206.verdict=skipped
file.206.reason=non-code-file
file.207.path=.specify/specs/108-team-view-degradation/test-evidence/tasks-validator-postcommit.txt
file.207.verdict=skipped
file.207.reason=non-code-file
file.208.path=.specify/specs/108-team-view-degradation/test-evidence/tasks-validator.txt
file.208.verdict=skipped
file.208.reason=non-code-file
file.209.path=.specify/specs/108-team-view-degradation/test-evidence/tasks.jsonl
file.209.verdict=skipped
file.209.reason=non-code-file
file.210.path=.specify/specs/108-team-view-degradation/test-evidence/us1-red-integration.txt
file.210.verdict=skipped
file.210.reason=non-code-file
file.211.path=.specify/specs/108-team-view-degradation/test-evidence/us1-red-unit.txt
file.211.verdict=skipped
file.211.reason=non-code-file
file.212.path=.specify/specs/108-team-view-degradation/test-evidence/us2-red-degraded.txt
file.212.verdict=skipped
file.212.reason=non-code-file
file.213.path=.specify/specs/108-team-view-degradation/test-evidence/us2-red-states.txt
file.213.verdict=skipped
file.213.reason=non-code-file
file.214.path=.specify/specs/108-team-view-degradation/test-evidence/us3-guards.txt
file.214.verdict=skipped
file.214.reason=non-code-file
file.215.path=.specify/specs/108-team-view-degradation/test-evidence/us3-red-contract.txt
file.215.verdict=skipped
file.215.reason=non-code-file
file.216.path=.specify/specs/108-team-view-degradation/test-evidence/verification-input.md
file.216.verdict=skipped
file.216.reason=non-code-file
file.217.path=.specify/specs/108-team-view-degradation/test-evidence/workspace-checklist-check-vs-tasks.json
file.217.verdict=skipped
file.217.reason=non-code-file
file.218.path=.specify/specs/108-team-view-degradation/test-evidence/workspace-checklist-postcommit.json
file.218.verdict=skipped
file.218.reason=non-code-file
file.219.path=.specify/specs/108-team-view-degradation/test-evidence/workspace-checklist-postcommit.txt
file.219.verdict=skipped
file.219.reason=non-code-file
file.220.path=.specify/specs/108-team-view-degradation/test-evidence/workspace-checklist-readings.txt
file.220.verdict=skipped
file.220.reason=non-code-file
file.221.path=.specify/specs/108-team-view-degradation/test-evidence/workspace-checklist.json
file.221.verdict=skipped
file.221.reason=non-code-file
file.222.path=.specify/specs/108-team-view-degradation/test-evidence/workspace-clarify-postcommit.json
file.222.verdict=skipped
file.222.reason=non-code-file
file.223.path=.specify/specs/108-team-view-degradation/test-evidence/workspace-clarify-postcommit.txt
file.223.verdict=skipped
file.223.reason=non-code-file
file.224.path=.specify/specs/108-team-view-degradation/test-evidence/workspace-clarify-readings.txt
file.224.verdict=skipped
file.224.reason=non-code-file
file.225.path=.specify/specs/108-team-view-degradation/test-evidence/workspace-clarify.json
file.225.verdict=skipped
file.225.reason=non-code-file
file.226.path=.specify/specs/108-team-view-degradation/test-evidence/workspace-plan-postcommit.json
file.226.verdict=skipped
file.226.reason=non-code-file
file.227.path=.specify/specs/108-team-view-degradation/test-evidence/workspace-plan-postcommit.txt
file.227.verdict=skipped
file.227.reason=non-code-file
file.228.path=.specify/specs/108-team-view-degradation/test-evidence/workspace-plan-poststage-driver.json
file.228.verdict=skipped
file.228.reason=non-code-file
file.229.path=.specify/specs/108-team-view-degradation/test-evidence/workspace-plan-readings.txt
file.229.verdict=skipped
file.229.reason=non-code-file
file.230.path=.specify/specs/108-team-view-degradation/test-evidence/workspace-plan.json
file.230.verdict=skipped
file.230.reason=non-code-file
file.231.path=.specify/specs/108-team-view-degradation/test-evidence/workspace-requirements-postcommit.json
file.231.verdict=skipped
file.231.reason=non-code-file
file.232.path=.specify/specs/108-team-view-degradation/test-evidence/workspace-requirements-postcommit.txt
file.232.verdict=skipped
file.232.reason=non-code-file
file.233.path=.specify/specs/108-team-view-degradation/test-evidence/workspace-requirements-readings.txt
file.233.verdict=skipped
file.233.reason=non-code-file
file.234.path=.specify/specs/108-team-view-degradation/test-evidence/workspace-requirements.json
file.234.verdict=skipped
file.234.reason=non-code-file
file.235.path=.specify/specs/108-team-view-degradation/test-evidence/workspace-tasks-check-vs-plan.json
file.235.verdict=skipped
file.235.reason=non-code-file
file.236.path=.specify/specs/108-team-view-degradation/test-evidence/workspace-tasks-postcommit.json
file.236.verdict=skipped
file.236.reason=non-code-file
file.237.path=.specify/specs/108-team-view-degradation/test-evidence/workspace-tasks-postcommit.txt
file.237.verdict=skipped
file.237.reason=non-code-file
file.238.path=.specify/specs/108-team-view-degradation/test-evidence/workspace-tasks-readings.txt
file.238.verdict=skipped
file.238.reason=non-code-file
file.239.path=.specify/specs/108-team-view-degradation/test-evidence/workspace-tasks.json
file.239.verdict=skipped
file.239.reason=non-code-file
file.240.path=.specify/specs/108-team-view-degradation/writeback/T001.yaml
file.240.verdict=skipped
file.240.reason=non-code-file
file.241.path=.specify/specs/108-team-view-degradation/writeback/T002.yaml
file.241.verdict=skipped
file.241.reason=non-code-file
file.242.path=.specify/specs/108-team-view-degradation/writeback/T003.yaml
file.242.verdict=skipped
file.242.reason=non-code-file
file.243.path=.specify/specs/108-team-view-degradation/writeback/T004.yaml
file.243.verdict=skipped
file.243.reason=non-code-file
file.244.path=.specify/specs/108-team-view-degradation/writeback/T005.yaml
file.244.verdict=skipped
file.244.reason=non-code-file
file.245.path=.specify/specs/108-team-view-degradation/writeback/T006.yaml
file.245.verdict=skipped
file.245.reason=non-code-file
file.246.path=.specify/specs/108-team-view-degradation/writeback/T007.yaml
file.246.verdict=skipped
file.246.reason=non-code-file
file.247.path=.specify/specs/108-team-view-degradation/writeback/T008.yaml
file.247.verdict=skipped
file.247.reason=non-code-file
file.248.path=.specify/specs/108-team-view-degradation/writeback/T009.yaml
file.248.verdict=skipped
file.248.reason=non-code-file
file.249.path=.specify/specs/108-team-view-degradation/writeback/T010.yaml
file.249.verdict=skipped
file.249.reason=non-code-file
file.250.path=.specify/specs/108-team-view-degradation/writeback/T011.yaml
file.250.verdict=skipped
file.250.reason=non-code-file
file.251.path=.specify/specs/108-team-view-degradation/writeback/T012.yaml
file.251.verdict=skipped
file.251.reason=non-code-file
file.252.path=.specify/specs/108-team-view-degradation/writeback/T013.yaml
file.252.verdict=skipped
file.252.reason=non-code-file
file.253.path=.specify/specs/108-team-view-degradation/writeback/T014.yaml
file.253.verdict=skipped
file.253.reason=non-code-file
file.254.path=.specify/specs/108-team-view-degradation/writeback/T015.yaml
file.254.verdict=skipped
file.254.reason=non-code-file
file.255.path=.specify/specs/108-team-view-degradation/writeback/T016.yaml
file.255.verdict=skipped
file.255.reason=non-code-file
file.256.path=.specify/specs/108-team-view-degradation/writeback/T017.yaml
file.256.verdict=skipped
file.256.reason=non-code-file
file.257.path=.specify/specs/108-team-view-degradation/writeback/T018.yaml
file.257.verdict=skipped
file.257.reason=non-code-file
file.258.path=.specify/teams/108-team-view-degradation/team.md
file.258.verdict=skipped
file.258.reason=non-code-file
file.259.path=docs/reference/commands/team.md
file.259.verdict=reviewed
file.260.path=scripts/python/team-view.py
file.260.verdict=reviewed
file.261.path=skills/internal/view-team/SKILL.md
file.261.verdict=reviewed
file.262.path=tests/contract/test_team_view_degradation_contract.py
file.262.verdict=reviewed
file.263.path=tests/integration/test_team_view_degradation.py
file.263.verdict=reviewed
file.264.path=tests/unit/test_team_view_report_recognition.py
file.264.verdict=reviewed
<!-- coverage-receipt:end -->
