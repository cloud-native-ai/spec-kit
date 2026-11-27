# Code Review Report — 代码段 (code segment)

| 属性 | 值 |
|------|-----|
| **分支** | `111-general-best-practices` |
| **基准** | `0419adae5e6e0e208ad6bcb443e45be8d266f04a` (`0419adae5`) |
| **目标** | `aca4fb076e9e9ea28ef6516f9d0a935949545fa9` (`aca4fb076`) |
| **基准来源** | `explicit` |
| **渲染模式** | `renderer: text` |
| **Reviewer** | `Qiming Liu (John)` |
| **日期** | `2026-11-27T09:12:08Z` |

## 变更概览

```
 .../records/20261127T072256895807Z-b2ed5204.json   |    1 +
 .../records/20261127T073241883504Z-2aeff455.json   |    1 +
 .../records/20261127T074258844219Z-60fd971b.json   |    1 +
 .../records/20261127T075547662238Z-61e5bf4a.json   |    1 +
 .../records/20261127T080451648094Z-4a771e2b.json   |    1 +
 .../records/20261127T081331351003Z-14a31158.json   |    1 +
 .../records/20261127T084428666545Z-8f2106d0.json   |    1 +
 .specify/features.md                               |    5 +-
 .specify/features/111-general-best-practices.md    |   31 +
 .../20261127T072303Z-speckit-requirements.md       |   20 +
 .../feedback/20261127T073252Z-speckit-clarify.md   |   20 +
 .specify/feedback/20261127T074304Z-speckit-plan.md |   21 +
 .../feedback/20261127T075556Z-speckit-tasks.md     |   21 +
 .../feedback/20261127T080505Z-speckit-checklist.md |   22 +
 .../feedback/20261127T081350Z-speckit-analyze.md   |   21 +
 .../feedback/20261127T082900Z-speckit-analyze.md   |   21 +
 .../feedback/20261127T084443Z-speckit-implement.md |   20 +
 ...n-speckit-requirements-r20261127t071500z-111.md |  202 ++++
 ...ation-speckit-clarify-r20261127t071500z-111a.md |  202 ++++
 ...mination-speckit-plan-r20261127t071500z-111a.md |  202 ++++
 ...ination-speckit-tasks-r20261127t071500z-111a.md |  202 ++++
 ...ion-speckit-checklist-r20261127t071500z-111a.md |  202 ++++
 ...ation-speckit-analyze-r20261127t071500z-111a.md |  202 ++++
 ...n-speckit-analyze-r20261127t074400z-111a-ana.md |  202 ++++
 ...ion-speckit-implement-r20261127t071500z-111a.md |  218 ++++
 .specify/shared/best-practices/README.md           |   44 +
 .../best-practices/programming-frameworks.md       |    5 +
 .../shared/best-practices/programming-languages.md |    5 +
 .../shared/best-practices/programming-tools.md     |    9 +
 .../shared/best-practices/system-interfaces.md     |    5 +
 .specify/shared/definitions/framework-map.md       |    1 +
 .../111-general-best-practices/baseline-failed.txt |  223 ++++
 .../general-best-practices-2026-11-27.md           |   94 ++
 .../checklists/requirements.md                     |   48 +
 .../checkpoints/01-requirements.md                 |   38 +
 .../checkpoints/02-clarify.md                      |    9 +
 .../checkpoints/03-plan.md                         |    8 +
 .../checkpoints/04-tasks.md                        |    7 +
 .../checkpoints/05-checklist.md                    |    7 +
 .../checkpoints/06-analyze.md                      |    8 +
 .../checkpoints/07-implement.md                    |    7 +
 .../contracts/accumulation.contract.md             |   28 +
 .../contracts/distribution-guard.contract.md       |   40 +
 .../contracts/entry-shape.contract.md              |   24 +
 .../contracts/manifest.contract.md                 |   28 +
 .../coverage-baseline.txt                          |  787 +++++++++++++++
 .../specs/111-general-best-practices/data-model.md |  158 +++
 .../111-general-best-practices/feature-ref.md      |   65 ++
 .../111-general-best-practices/notes/.gitkeep      |    0
 .../notes/pre-change-measurements.md               |   21 +
 .../notes/quickstart-run.md                        |  193 ++++
 .../notes/red-first-evidence.md                    |   43 +
 .../111-general-best-practices/notes/us1-green.txt |   51 +
 .../111-general-best-practices/notes/us2-green.txt |   56 +
 .../111-general-best-practices/notes/us3-green.txt |   93 ++
 .specify/specs/111-general-best-practices/plan.md  |  152 +++
 .../specs/111-general-best-practices/quickstart.md |  154 +++
 .../111-general-best-practices/requirements.md     |  229 +++++
 .../specs/111-general-best-practices/research.md   |  115 +++
 .specify/specs/111-general-best-practices/tasks.md |  306 ++++++
 .../test-evidence/analyze-repair-pre-analyze.json  | 1067 ++++++++++++++++++++
 .../test-evidence/analyze-repair-pre-analyze.txt   |    5 +
 .../analyze-repair-requirements-validator.txt      |   13 +
 .../test-evidence/analyze-repair-round1.md         |   62 ++
 .../analyze-repair-tasks-validator.txt             |    4 +
 .../test-evidence/analyze-round1-findings.jsonl    |   12 +
 .../test-evidence/analyze-round1-report.md         |  143 +++
 .../test-evidence/analyze-round2-findings.jsonl    |   14 +
 .../test-evidence/analyze-round2-report.md         |  126 +++
 .../analyze-round2-requirements-validator.txt      |   10 +
 .../analyze-round2-tasks-validator.txt             |    1 +
 .../test-evidence/checklist-exec-quant.txt         |    1 +
 .../test-evidence/checklist-feedback-record.txt    |    9 +
 .../checklist-requirements-validator.txt           |   10 +
 .../test-evidence/checklist-run-determination.txt  |    8 +
 .../test-evidence/checklist-selfcheck.txt          |   17 +
 .../test-evidence/checklist-spec-readings.txt      |   32 +
 .../test-evidence/checklist-stage-2026-11-27.md    |   75 ++
 .../test-evidence/clarify-stage-2026-11-27.md      |  111 ++
 .../test-evidence/clarify-validator.txt            |   10 +
 .../test-evidence/closure-gates.txt                |   95 ++
 .../test-evidence/containment.txt                  |   97 ++
 .../test-evidence/decomposition-requirements.json  |   12 +
 .../test-evidence/decomposition-requirements.txt   |    1 +
 .../test-evidence/decomposition-tasks.json         |   12 +
 .../test-evidence/decomposition-tasks.txt          |    1 +
 .../test-evidence/full-names-run1.txt              |  225 +++++
 .../test-evidence/full-names.txt                   |  223 ++++
 .../test-evidence/full-suite.txt                   |   51 +
 .../test-evidence/implement-entry-baseline.txt     |   13 +
 .../test-evidence/init-distribution-proof.txt      |  112 ++
 .../test-evidence/mirror-parity-names.txt          |    0
 .../test-evidence/p1-parity-names.txt              |    1 +
 .../test-evidence/plan-decision-tensions.txt       |   11 +
 .../test-evidence/plan-exec-quant.txt              |    1 +
 .../test-evidence/plan-feedback-record.txt         |    9 +
 .../test-evidence/plan-mirror-check.txt            |   13 +
 .../test-evidence/plan-mirror-write.txt            |   13 +
 .../test-evidence/plan-pre-analyze.json            |  787 +++++++++++++++
 .../test-evidence/plan-pre-analyze.txt             |    2 +
 .../test-evidence/plan-probes.txt                  |  186 ++++
 .../test-evidence/plan-requirements-revalidate.txt |   10 +
 .../test-evidence/plan-run-determination.txt       |    8 +
 .../test-evidence/plan-stage-2026-11-27.md         |   58 ++
 .../test-evidence/pre-analyze-checklist.txt        |    5 +
 .../test-evidence/pre-analyze-requirements.json    |  213 ++++
 .../test-evidence/pre-analyze-requirements.txt     |    2 +
 .../test-evidence/requirements-stage-2026-11-27.md |   69 ++
 .../test-evidence/requirements-validator.txt       |   10 +
 .../test-evidence/targeted-names.txt               |    0
 .../test-evidence/targeted-set.txt                 |   36 +
 .../test-evidence/tasks-exec-quant.txt             |    1 +
 .../test-evidence/tasks-feedback-record.txt        |    9 +
 .../test-evidence/tasks-pre-analyze.json           |  990 ++++++++++++++++++
 .../test-evidence/tasks-pre-analyze.txt            |    2 +
 .../test-evidence/tasks-run-determination.txt      |    8 +
 .../test-evidence/tasks-stage-2026-11-27.md        |   56 +
 .../test-evidence/tasks-validator.txt              |    1 +
 .../test-evidence/us1-names.txt                    |    0
 .../test-evidence/us2-names.txt                    |    0
 .../test-evidence/us3-names.txt                    |    0
 .../test-evidence/verification-input.md            |   60 ++
 .../workspace-analyze-repair-check.json            |    1 +
 .../workspace-analyze-repair-vs-checklist.json     |    1 +
 .../test-evidence/workspace-analyze-repair.json    |  314 ++++++
 .../workspace-checklist-check-vs-plan.json         |    1 +
 .../test-evidence/workspace-checklist.json         |  314 ++++++
 .../test-evidence/workspace-implement-p1.json      |  314 ++++++
 .../test-evidence/workspace-implement-p2.json      |  314 ++++++
 .../test-evidence/workspace-plan.json              |  314 ++++++
 .../test-evidence/wrap-up-accounting.txt           |  116 +++
 shared/best-practices/README.md                    |   44 +
 shared/best-practices/programming-frameworks.md    |    5 +
 shared/best-practices/programming-languages.md     |    5 +
 shared/best-practices/programming-tools.md         |    9 +
 shared/best-practices/system-interfaces.md         |    5 +
 shared/definitions/framework-map.md                |    1 +
 tests/contract/test_general_best_practices.py      |  288 ++++++
 138 files changed, 12079 insertions(+), 2 deletions(-)
```

---

## Review 意见


### 🔴 [BLOCKING] .specify/features/111-general-best-practices.md (Line 6)

> Status claim unsupported by its declared carrier: both the registry row (features.md:118) and this detail read `Implemented`, but the implement Pre-Status-Flip Gate requires `verification.md` (one status row per SC plus the smoke record). That file never landed; `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/111-general-best-practices` exits 2 with `required input not found: .../verification.md`. Until the carrier exists and the closure verdict reads `accept`, the `Implemented` claim must not be relied on and this branch must not be merged as a completed feature. Fix: derive `verification.md` from `test-evidence/verification-input.md` (the derive-then-recheck shape used by the 107/108 reviews) and re-run the closure gate.

<sub>17:12:55</sub>


### 🟠 [IMPORTANT] .specify/specs/111-general-best-practices/tasks.md (Line 23)

> DoD-7 reassigns an implement-stage deliverable to an unnamed "spec side" and forbids the crew to write it, while implement-feature SKILL.md § Step 9 (lines 322-329) assigns populating `REQUIREMENTS_DIR/verification.md` to the implement run. No stage in the driver sequence owns the derivation, so the file was never produced (the same defect surfaced in the 107 and 108 reviews). Fix: align DoD-7 with Step 9 (the implement run populates it) or name the deriving seat explicitly.

<sub>17:12:55</sub>


### 🟢 [SUGGESTION] .specify/specs/111-general-best-practices/test-evidence/containment.txt (Line 81)

> The "final-tree re-read" label is premature: Reading 2 was taken at `0cbec5aa4` (135 paths) before the registry-repair commit (`39be9495a`, +2 registry paths) and the checkpoint commit (`aca4fb076`, +1 spec path). The HEAD re-derivation is 138 paths = 113 declared + 2 registry exception + 23 accounting residuals, 0 violations — the invariant holds; only the count and the "final" label are stale. Append a post-checkpoint reading or relabel Reading 2 as interim.

<sub>17:12:55</sub>


### 🟢 [SUGGESTION] shared/best-practices/README.md (Line 27)

> The manifest ships to every client project through `specify init`, but it points at `.specify/specs/111-general-best-practices/contracts/entry-shape.contract.md`, which init never copies — downstream readers hit a dead pointer. The guard cannot catch it because it resolves paths against the framework repo. This is the already-recorded analyze finding AR1-04 (deferred); recording it here for the delta. Fix: restate the entry-shape triple inline in the distributed text (it already lists the triple) and keep the spec contract as the framework-side design face, or point at a distributed file.

<sub>17:12:55</sub>


### ⚪ [NITPICK] .specify/features/111-general-best-practices.md (Line 24)

> Task-count phrasing drift: "Tasks T001–T019 closed" / "19/19 tasks" (also features.md:118 and checkpoints 04/07) versus the actual row set of 20 (T001–T019 + T007A; closure-gates.txt:24 reports tasks=20). Reconcile the count wording so closure counts are readable without recounting rows.

<sub>17:12:55</sub>


### ⚪ [NITPICK] shared/best-practices/README.md (Line 44)

> All five ported module documents end without a trailing newline (README.md, programming-tools.md and the three placeholder files), while their ai-harness source files end with one; the mirrors inherit the same bytes so parity is unaffected. A-8 asks for a port "in substance"; restoring the final newline keeps the docs POSIX-clean and makes future diffs stable.

<sub>17:12:55</sub>


### 👍 [PRAISE] tests/contract/test_general_best_practices.py (Line 220)

> The placeholder leg pins the equivalence (one italic placeholder ⇔ zero `## ` entries) without freezing the delivery count of 3, and the shared prelude (lines 145-164) adds the residue scan plus cited-path existence so all six legs share one read of the module — exactly the C-203/C-205 boundary between structural pinning and semantic judgement.

<sub>17:12:55</sub>


<!-- coverage-receipt:begin -->
receipt_version=1
base=0419adae5e6e0e208ad6bcb443e45be8d266f04a
head=aca4fb076e9e9ea28ef6516f9d0a935949545fa9
base_source=explicit
renderer=text
changed_files=138
judged_files=15
skipped_files=123
gap_files=0
lines_added=460
lines_deleted=2
file.001.path=.specify/exec-quant/records/20261127T072256895807Z-b2ed5204.json
file.001.verdict=skipped
file.001.reason=generated
file.002.path=.specify/exec-quant/records/20261127T073241883504Z-2aeff455.json
file.002.verdict=skipped
file.002.reason=generated
file.003.path=.specify/exec-quant/records/20261127T074258844219Z-60fd971b.json
file.003.verdict=skipped
file.003.reason=generated
file.004.path=.specify/exec-quant/records/20261127T075547662238Z-61e5bf4a.json
file.004.verdict=skipped
file.004.reason=generated
file.005.path=.specify/exec-quant/records/20261127T080451648094Z-4a771e2b.json
file.005.verdict=skipped
file.005.reason=generated
file.006.path=.specify/exec-quant/records/20261127T081331351003Z-14a31158.json
file.006.verdict=skipped
file.006.reason=generated
file.007.path=.specify/exec-quant/records/20261127T084428666545Z-8f2106d0.json
file.007.verdict=skipped
file.007.reason=generated
file.008.path=.specify/features.md
file.008.verdict=reviewed
file.009.path=.specify/features/111-general-best-practices.md
file.009.verdict=reviewed
file.010.path=.specify/feedback/20261127T072303Z-speckit-requirements.md
file.010.verdict=skipped
file.010.reason=generated
file.011.path=.specify/feedback/20261127T073252Z-speckit-clarify.md
file.011.verdict=skipped
file.011.reason=generated
file.012.path=.specify/feedback/20261127T074304Z-speckit-plan.md
file.012.verdict=skipped
file.012.reason=generated
file.013.path=.specify/feedback/20261127T075556Z-speckit-tasks.md
file.013.verdict=skipped
file.013.reason=generated
file.014.path=.specify/feedback/20261127T080505Z-speckit-checklist.md
file.014.verdict=skipped
file.014.reason=generated
file.015.path=.specify/feedback/20261127T081350Z-speckit-analyze.md
file.015.verdict=skipped
file.015.reason=generated
file.016.path=.specify/feedback/20261127T082900Z-speckit-analyze.md
file.016.verdict=skipped
file.016.reason=generated
file.017.path=.specify/feedback/20261127T084443Z-speckit-implement.md
file.017.verdict=skipped
file.017.reason=generated
file.018.path=.specify/session/20261127T072252Z-run-determination-speckit-requirements-r20261127t071500z-111.md
file.018.verdict=skipped
file.018.reason=generated
file.019.path=.specify/session/20261127T073236Z-run-determination-speckit-clarify-r20261127t071500z-111a.md
file.019.verdict=skipped
file.019.reason=generated
file.020.path=.specify/session/20261127T074258Z-run-determination-speckit-plan-r20261127t071500z-111a.md
file.020.verdict=skipped
file.020.reason=generated
file.021.path=.specify/session/20261127T075541Z-run-determination-speckit-tasks-r20261127t071500z-111a.md
file.021.verdict=skipped
file.021.reason=generated
file.022.path=.specify/session/20261127T080445Z-run-determination-speckit-checklist-r20261127t071500z-111a.md
file.022.verdict=skipped
file.022.reason=generated
file.023.path=.specify/session/20261127T081331Z-run-determination-speckit-analyze-r20261127t071500z-111a.md
file.023.verdict=skipped
file.023.reason=generated
file.024.path=.specify/session/20261127T082842Z-run-determination-speckit-analyze-r20261127t074400z-111a-ana.md
file.024.verdict=skipped
file.024.reason=generated
file.025.path=.specify/session/20261127T084422Z-run-determination-speckit-implement-r20261127t071500z-111a.md
file.025.verdict=skipped
file.025.reason=generated
file.026.path=.specify/shared/best-practices/README.md
file.026.verdict=reviewed
file.027.path=.specify/shared/best-practices/programming-frameworks.md
file.027.verdict=reviewed
file.028.path=.specify/shared/best-practices/programming-languages.md
file.028.verdict=reviewed
file.029.path=.specify/shared/best-practices/programming-tools.md
file.029.verdict=reviewed
file.030.path=.specify/shared/best-practices/system-interfaces.md
file.030.verdict=reviewed
file.031.path=.specify/shared/definitions/framework-map.md
file.031.verdict=reviewed
file.032.path=.specify/specs/111-general-best-practices/baseline-failed.txt
file.032.verdict=skipped
file.032.reason=non-code-file
file.033.path=.specify/specs/111-general-best-practices/checklists/general-best-practices-2026-11-27.md
file.033.verdict=skipped
file.033.reason=non-code-file
file.034.path=.specify/specs/111-general-best-practices/checklists/requirements.md
file.034.verdict=skipped
file.034.reason=non-code-file
file.035.path=.specify/specs/111-general-best-practices/checkpoints/01-requirements.md
file.035.verdict=skipped
file.035.reason=non-code-file
file.036.path=.specify/specs/111-general-best-practices/checkpoints/02-clarify.md
file.036.verdict=skipped
file.036.reason=non-code-file
file.037.path=.specify/specs/111-general-best-practices/checkpoints/03-plan.md
file.037.verdict=skipped
file.037.reason=non-code-file
file.038.path=.specify/specs/111-general-best-practices/checkpoints/04-tasks.md
file.038.verdict=skipped
file.038.reason=non-code-file
file.039.path=.specify/specs/111-general-best-practices/checkpoints/05-checklist.md
file.039.verdict=skipped
file.039.reason=non-code-file
file.040.path=.specify/specs/111-general-best-practices/checkpoints/06-analyze.md
file.040.verdict=skipped
file.040.reason=non-code-file
file.041.path=.specify/specs/111-general-best-practices/checkpoints/07-implement.md
file.041.verdict=skipped
file.041.reason=non-code-file
file.042.path=.specify/specs/111-general-best-practices/contracts/accumulation.contract.md
file.042.verdict=skipped
file.042.reason=non-code-file
file.043.path=.specify/specs/111-general-best-practices/contracts/distribution-guard.contract.md
file.043.verdict=skipped
file.043.reason=non-code-file
file.044.path=.specify/specs/111-general-best-practices/contracts/entry-shape.contract.md
file.044.verdict=skipped
file.044.reason=non-code-file
file.045.path=.specify/specs/111-general-best-practices/contracts/manifest.contract.md
file.045.verdict=skipped
file.045.reason=non-code-file
file.046.path=.specify/specs/111-general-best-practices/coverage-baseline.txt
file.046.verdict=skipped
file.046.reason=non-code-file
file.047.path=.specify/specs/111-general-best-practices/data-model.md
file.047.verdict=skipped
file.047.reason=non-code-file
file.048.path=.specify/specs/111-general-best-practices/feature-ref.md
file.048.verdict=skipped
file.048.reason=non-code-file
file.049.path=.specify/specs/111-general-best-practices/notes/.gitkeep
file.049.verdict=skipped
file.049.reason=non-code-file
file.050.path=.specify/specs/111-general-best-practices/notes/pre-change-measurements.md
file.050.verdict=skipped
file.050.reason=non-code-file
file.051.path=.specify/specs/111-general-best-practices/notes/quickstart-run.md
file.051.verdict=skipped
file.051.reason=non-code-file
file.052.path=.specify/specs/111-general-best-practices/notes/red-first-evidence.md
file.052.verdict=skipped
file.052.reason=non-code-file
file.053.path=.specify/specs/111-general-best-practices/notes/us1-green.txt
file.053.verdict=skipped
file.053.reason=non-code-file
file.054.path=.specify/specs/111-general-best-practices/notes/us2-green.txt
file.054.verdict=skipped
file.054.reason=non-code-file
file.055.path=.specify/specs/111-general-best-practices/notes/us3-green.txt
file.055.verdict=skipped
file.055.reason=non-code-file
file.056.path=.specify/specs/111-general-best-practices/plan.md
file.056.verdict=skipped
file.056.reason=non-code-file
file.057.path=.specify/specs/111-general-best-practices/quickstart.md
file.057.verdict=skipped
file.057.reason=non-code-file
file.058.path=.specify/specs/111-general-best-practices/requirements.md
file.058.verdict=skipped
file.058.reason=non-code-file
file.059.path=.specify/specs/111-general-best-practices/research.md
file.059.verdict=skipped
file.059.reason=non-code-file
file.060.path=.specify/specs/111-general-best-practices/tasks.md
file.060.verdict=skipped
file.060.reason=non-code-file
file.061.path=.specify/specs/111-general-best-practices/test-evidence/analyze-repair-pre-analyze.json
file.061.verdict=skipped
file.061.reason=non-code-file
file.062.path=.specify/specs/111-general-best-practices/test-evidence/analyze-repair-pre-analyze.txt
file.062.verdict=skipped
file.062.reason=non-code-file
file.063.path=.specify/specs/111-general-best-practices/test-evidence/analyze-repair-requirements-validator.txt
file.063.verdict=skipped
file.063.reason=non-code-file
file.064.path=.specify/specs/111-general-best-practices/test-evidence/analyze-repair-round1.md
file.064.verdict=skipped
file.064.reason=non-code-file
file.065.path=.specify/specs/111-general-best-practices/test-evidence/analyze-repair-tasks-validator.txt
file.065.verdict=skipped
file.065.reason=non-code-file
file.066.path=.specify/specs/111-general-best-practices/test-evidence/analyze-round1-findings.jsonl
file.066.verdict=skipped
file.066.reason=non-code-file
file.067.path=.specify/specs/111-general-best-practices/test-evidence/analyze-round1-report.md
file.067.verdict=skipped
file.067.reason=non-code-file
file.068.path=.specify/specs/111-general-best-practices/test-evidence/analyze-round2-findings.jsonl
file.068.verdict=skipped
file.068.reason=non-code-file
file.069.path=.specify/specs/111-general-best-practices/test-evidence/analyze-round2-report.md
file.069.verdict=skipped
file.069.reason=non-code-file
file.070.path=.specify/specs/111-general-best-practices/test-evidence/analyze-round2-requirements-validator.txt
file.070.verdict=skipped
file.070.reason=non-code-file
file.071.path=.specify/specs/111-general-best-practices/test-evidence/analyze-round2-tasks-validator.txt
file.071.verdict=skipped
file.071.reason=non-code-file
file.072.path=.specify/specs/111-general-best-practices/test-evidence/checklist-exec-quant.txt
file.072.verdict=skipped
file.072.reason=non-code-file
file.073.path=.specify/specs/111-general-best-practices/test-evidence/checklist-feedback-record.txt
file.073.verdict=skipped
file.073.reason=non-code-file
file.074.path=.specify/specs/111-general-best-practices/test-evidence/checklist-requirements-validator.txt
file.074.verdict=skipped
file.074.reason=non-code-file
file.075.path=.specify/specs/111-general-best-practices/test-evidence/checklist-run-determination.txt
file.075.verdict=skipped
file.075.reason=non-code-file
file.076.path=.specify/specs/111-general-best-practices/test-evidence/checklist-selfcheck.txt
file.076.verdict=skipped
file.076.reason=non-code-file
file.077.path=.specify/specs/111-general-best-practices/test-evidence/checklist-spec-readings.txt
file.077.verdict=skipped
file.077.reason=non-code-file
file.078.path=.specify/specs/111-general-best-practices/test-evidence/checklist-stage-2026-11-27.md
file.078.verdict=skipped
file.078.reason=non-code-file
file.079.path=.specify/specs/111-general-best-practices/test-evidence/clarify-stage-2026-11-27.md
file.079.verdict=skipped
file.079.reason=non-code-file
file.080.path=.specify/specs/111-general-best-practices/test-evidence/clarify-validator.txt
file.080.verdict=skipped
file.080.reason=non-code-file
file.081.path=.specify/specs/111-general-best-practices/test-evidence/closure-gates.txt
file.081.verdict=skipped
file.081.reason=non-code-file
file.082.path=.specify/specs/111-general-best-practices/test-evidence/containment.txt
file.082.verdict=skipped
file.082.reason=non-code-file
file.083.path=.specify/specs/111-general-best-practices/test-evidence/decomposition-requirements.json
file.083.verdict=skipped
file.083.reason=non-code-file
file.084.path=.specify/specs/111-general-best-practices/test-evidence/decomposition-requirements.txt
file.084.verdict=skipped
file.084.reason=non-code-file
file.085.path=.specify/specs/111-general-best-practices/test-evidence/decomposition-tasks.json
file.085.verdict=skipped
file.085.reason=non-code-file
file.086.path=.specify/specs/111-general-best-practices/test-evidence/decomposition-tasks.txt
file.086.verdict=skipped
file.086.reason=non-code-file
file.087.path=.specify/specs/111-general-best-practices/test-evidence/full-names-run1.txt
file.087.verdict=skipped
file.087.reason=non-code-file
file.088.path=.specify/specs/111-general-best-practices/test-evidence/full-names.txt
file.088.verdict=skipped
file.088.reason=non-code-file
file.089.path=.specify/specs/111-general-best-practices/test-evidence/full-suite.txt
file.089.verdict=skipped
file.089.reason=non-code-file
file.090.path=.specify/specs/111-general-best-practices/test-evidence/implement-entry-baseline.txt
file.090.verdict=skipped
file.090.reason=non-code-file
file.091.path=.specify/specs/111-general-best-practices/test-evidence/init-distribution-proof.txt
file.091.verdict=skipped
file.091.reason=non-code-file
file.092.path=.specify/specs/111-general-best-practices/test-evidence/mirror-parity-names.txt
file.092.verdict=skipped
file.092.reason=non-code-file
file.093.path=.specify/specs/111-general-best-practices/test-evidence/p1-parity-names.txt
file.093.verdict=skipped
file.093.reason=non-code-file
file.094.path=.specify/specs/111-general-best-practices/test-evidence/plan-decision-tensions.txt
file.094.verdict=skipped
file.094.reason=non-code-file
file.095.path=.specify/specs/111-general-best-practices/test-evidence/plan-exec-quant.txt
file.095.verdict=skipped
file.095.reason=non-code-file
file.096.path=.specify/specs/111-general-best-practices/test-evidence/plan-feedback-record.txt
file.096.verdict=skipped
file.096.reason=non-code-file
file.097.path=.specify/specs/111-general-best-practices/test-evidence/plan-mirror-check.txt
file.097.verdict=skipped
file.097.reason=non-code-file
file.098.path=.specify/specs/111-general-best-practices/test-evidence/plan-mirror-write.txt
file.098.verdict=skipped
file.098.reason=non-code-file
file.099.path=.specify/specs/111-general-best-practices/test-evidence/plan-pre-analyze.json
file.099.verdict=skipped
file.099.reason=non-code-file
file.100.path=.specify/specs/111-general-best-practices/test-evidence/plan-pre-analyze.txt
file.100.verdict=skipped
file.100.reason=non-code-file
file.101.path=.specify/specs/111-general-best-practices/test-evidence/plan-probes.txt
file.101.verdict=skipped
file.101.reason=non-code-file
file.102.path=.specify/specs/111-general-best-practices/test-evidence/plan-requirements-revalidate.txt
file.102.verdict=skipped
file.102.reason=non-code-file
file.103.path=.specify/specs/111-general-best-practices/test-evidence/plan-run-determination.txt
file.103.verdict=skipped
file.103.reason=non-code-file
file.104.path=.specify/specs/111-general-best-practices/test-evidence/plan-stage-2026-11-27.md
file.104.verdict=skipped
file.104.reason=non-code-file
file.105.path=.specify/specs/111-general-best-practices/test-evidence/pre-analyze-checklist.txt
file.105.verdict=skipped
file.105.reason=non-code-file
file.106.path=.specify/specs/111-general-best-practices/test-evidence/pre-analyze-requirements.json
file.106.verdict=skipped
file.106.reason=non-code-file
file.107.path=.specify/specs/111-general-best-practices/test-evidence/pre-analyze-requirements.txt
file.107.verdict=skipped
file.107.reason=non-code-file
file.108.path=.specify/specs/111-general-best-practices/test-evidence/requirements-stage-2026-11-27.md
file.108.verdict=skipped
file.108.reason=non-code-file
file.109.path=.specify/specs/111-general-best-practices/test-evidence/requirements-validator.txt
file.109.verdict=skipped
file.109.reason=non-code-file
file.110.path=.specify/specs/111-general-best-practices/test-evidence/targeted-names.txt
file.110.verdict=skipped
file.110.reason=non-code-file
file.111.path=.specify/specs/111-general-best-practices/test-evidence/targeted-set.txt
file.111.verdict=skipped
file.111.reason=non-code-file
file.112.path=.specify/specs/111-general-best-practices/test-evidence/tasks-exec-quant.txt
file.112.verdict=skipped
file.112.reason=non-code-file
file.113.path=.specify/specs/111-general-best-practices/test-evidence/tasks-feedback-record.txt
file.113.verdict=skipped
file.113.reason=non-code-file
file.114.path=.specify/specs/111-general-best-practices/test-evidence/tasks-pre-analyze.json
file.114.verdict=skipped
file.114.reason=non-code-file
file.115.path=.specify/specs/111-general-best-practices/test-evidence/tasks-pre-analyze.txt
file.115.verdict=skipped
file.115.reason=non-code-file
file.116.path=.specify/specs/111-general-best-practices/test-evidence/tasks-run-determination.txt
file.116.verdict=skipped
file.116.reason=non-code-file
file.117.path=.specify/specs/111-general-best-practices/test-evidence/tasks-stage-2026-11-27.md
file.117.verdict=skipped
file.117.reason=non-code-file
file.118.path=.specify/specs/111-general-best-practices/test-evidence/tasks-validator.txt
file.118.verdict=skipped
file.118.reason=non-code-file
file.119.path=.specify/specs/111-general-best-practices/test-evidence/us1-names.txt
file.119.verdict=skipped
file.119.reason=non-code-file
file.120.path=.specify/specs/111-general-best-practices/test-evidence/us2-names.txt
file.120.verdict=skipped
file.120.reason=non-code-file
file.121.path=.specify/specs/111-general-best-practices/test-evidence/us3-names.txt
file.121.verdict=skipped
file.121.reason=non-code-file
file.122.path=.specify/specs/111-general-best-practices/test-evidence/verification-input.md
file.122.verdict=skipped
file.122.reason=non-code-file
file.123.path=.specify/specs/111-general-best-practices/test-evidence/workspace-analyze-repair-check.json
file.123.verdict=skipped
file.123.reason=non-code-file
file.124.path=.specify/specs/111-general-best-practices/test-evidence/workspace-analyze-repair-vs-checklist.json
file.124.verdict=skipped
file.124.reason=non-code-file
file.125.path=.specify/specs/111-general-best-practices/test-evidence/workspace-analyze-repair.json
file.125.verdict=skipped
file.125.reason=non-code-file
file.126.path=.specify/specs/111-general-best-practices/test-evidence/workspace-checklist-check-vs-plan.json
file.126.verdict=skipped
file.126.reason=non-code-file
file.127.path=.specify/specs/111-general-best-practices/test-evidence/workspace-checklist.json
file.127.verdict=skipped
file.127.reason=non-code-file
file.128.path=.specify/specs/111-general-best-practices/test-evidence/workspace-implement-p1.json
file.128.verdict=skipped
file.128.reason=non-code-file
file.129.path=.specify/specs/111-general-best-practices/test-evidence/workspace-implement-p2.json
file.129.verdict=skipped
file.129.reason=non-code-file
file.130.path=.specify/specs/111-general-best-practices/test-evidence/workspace-plan.json
file.130.verdict=skipped
file.130.reason=non-code-file
file.131.path=.specify/specs/111-general-best-practices/test-evidence/wrap-up-accounting.txt
file.131.verdict=skipped
file.131.reason=non-code-file
file.132.path=shared/best-practices/README.md
file.132.verdict=reviewed
file.133.path=shared/best-practices/programming-frameworks.md
file.133.verdict=reviewed
file.134.path=shared/best-practices/programming-languages.md
file.134.verdict=reviewed
file.135.path=shared/best-practices/programming-tools.md
file.135.verdict=reviewed
file.136.path=shared/best-practices/system-interfaces.md
file.136.verdict=reviewed
file.137.path=shared/definitions/framework-map.md
file.137.verdict=reviewed
file.138.path=tests/contract/test_general_best_practices.py
file.138.verdict=reviewed
<!-- coverage-receipt:end -->
