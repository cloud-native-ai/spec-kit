# Code Review Report — 代码段 (code segment)

| 属性 | 值 |
|------|-----|
| **分支** | `084-harness-triple-structure` |
| **基准** | `3ffeb26e4880f134f7a5e220ecbffb869f165632` (`3ffeb26e`) |
| **目标** | `03a19487e4ceb668e27ef1a4554aff82e4dc8a4c` (`03a19487`) |
| **基准来源** | `feature-first-commit` |
| **渲染模式** | `renderer: text` |
| **Reviewer** | `Qiming Liu (John)` |
| **日期** | `2026-11-05T15:56:19Z` |

## 变更概览

```
 .claude/commands/speckit.history.md                |    3 +-
 .claude/commands/speckit.requirements.md           |    1 +
 .claude/commands/speckit.review.md                 |    2 +
 .github/prompts/speckit.history.prompt.md          |    3 +-
 .github/prompts/speckit.requirements.prompt.md     |    1 +
 .github/prompts/speckit.review.prompt.md           |    2 +
 .opencode/command/speckit.history.md               |    3 +-
 .opencode/command/speckit.requirements.md          |    1 +
 .opencode/command/speckit.review.md                |    2 +
 .qoder/commands/speckit.history.md                 |    3 +-
 .qoder/commands/speckit.requirements.md            |    1 +
 .qoder/commands/speckit.review.md                  |    2 +
 .specify/memory/features.md                        |    5 +-
 .specify/memory/features/081.md                    |    1 +
 .specify/memory/features/084.md                    |   92 +
 .../scripts/python/closure-acceptance-check.py     |  149 +-
 .specify/scripts/python/declaration_reader.py      |  469 ++++++
 .specify/scripts/python/evidence-utils.py          |   40 +-
 .specify/scripts/python/exec-quant.py              |  132 +-
 .specify/scripts/python/feedback-utils.py          |   82 +-
 .specify/scripts/python/flow-class-check.py        |  141 +-
 .specify/scripts/python/harness-triple-check.py    |  596 +++++++
 .specify/scripts/python/history-utils.py           |   76 +-
 .specify/scripts/python/memory-utils.py            |   31 +-
 .specify/scripts/python/probe-utils.py             |  100 +-
 .specify/scripts/python/record-retention.py        |   47 +-
 .specify/scripts/python/trigger-utils.py           |  105 +-
 .specify/scripts/python/validate-requirements.py   |   54 +-
 .specify/shared/declarations/contract.yaml         |   62 +
 .../declarations/exclusions/no-harness-asset.yaml  |  269 +++
 .../declarations/exclusions/no-machine-fact.yaml   |  313 ++++
 .../declarations/facts/arc-verdict-mapping.yaml    |   38 +
 .../facts/driver-completion-sentinels.yaml         |   26 +
 .../declarations/facts/driver-gate-roster.yaml     |   37 +
 .../declarations/facts/driver-stage-artifacts.yaml |   79 +
 .../declarations/facts/driver-stage-sequence.yaml  |   27 +
 .../shared/declarations/facts/evidence-lanes.yaml  |   23 +
 .../declarations/facts/evidence-seven-states.yaml  |   27 +
 .../declarations/facts/expression-gate-faces.yaml  |   19 +
 .../facts/expression-stage-operator-table.yaml     |   23 +
 .../facts/feedback-prompt-threshold.yaml           |   19 +
 .../declarations/facts/flow-class-basis.yaml       |   17 +
 .../declarations/facts/flow-class-classes.yaml     |   19 +
 .../facts/flow-class-document-types.yaml           |   19 +
 .../facts/flow-class-ledger-columns.yaml           |   18 +
 .../facts/flow-class-neutral-categories.yaml       |   18 +
 .../facts/history-manifest-schema.yaml             |   30 +
 .../facts/memory-retention-thresholds.yaml         |   31 +
 .../shared/declarations/facts/memory-types.yaml    |   21 +
 .../declarations/facts/probe-class-values.yaml     |   46 +
 .../facts/probe-object-binding-map.yaml            |   26 +
 .../declarations/facts/quant-record-schema.yaml    |   90 +
 .../facts/success-criterion-path-values.yaml       |   23 +
 .../declarations/facts/trigger-state-schema.yaml   |   47 +
 .../shared/definitions/flow-class-definitions.md   |   23 +-
 .specify/shared/definitions/framework-map.md       |    3 +
 .../definitions/harness-triple-definitions.md      |  154 ++
 .specify/shared/definitions/probe-definitions.md   |   15 +
 .specify/shared/guidelines/better-harness.md       |    2 +-
 .specify/shared/guidelines/proactive-trigger.md    |    1 +
 .specify/shared/workflow/acceptance-hardening.md   |    6 +
 .specify/shared/workflow/evidence-step.md          |    2 +-
 .specify/shared/workflow/expression-gates.md       |    8 +
 .specify/shared/workflow/feedback-step.md          |    7 +-
 .specify/skills/internal/collect-evidence/SKILL.md |    4 +-
 .../references/evidence-discipline.md              |   27 +-
 .specify/skills/internal/manage-history/SKILL.md   |    2 +
 .specify/skills/internal/memory-recall/SKILL.md    |   10 +-
 .specify/skills/internal/memory-record/SKILL.md    |   10 +-
 .../skills/internal/review-sdd-process/SKILL.md    |    5 +-
 .specify/skills/sdd-loop-driver/SKILL.md           |    3 +-
 .../sdd-loop-driver/references/efficiency-model.md |    2 +
 .../sdd-loop-driver/references/state-awareness.md  |    2 +
 .../skills/sdd-loop-driver/scripts/loop-state.py   |  224 ++-
 .../sdd-loop-driver/scripts/pre-analyze-check.py   |  236 ++-
 .../baseline-failed.txt                            |   25 +
 .../checklists/layer-criteria-2026-11-05.md        |   85 +
 .../checklists/requirements.md                     |   44 +
 .../contracts/declaration-schema.contract.md       |   66 +
 .../contracts/distribution-and-mirror.contract.md  |   79 +
 .../contracts/harness-triple-check.contract.md     |   69 +
 .../contracts/migration-batches.contract.md        |  162 ++
 .../contracts/shared-reader.contract.md            |   50 +
 .../coverage-baseline.txt                          |  515 ++++++
 .../084-harness-triple-structure/data-model.md     |  169 ++
 .../084-harness-triple-structure/feature-ref.md    |   42 +
 .../notes/pre-change-measurements.md               |  168 ++
 .../notes/red-first-evidence.md                    |   50 +
 .../specs/084-harness-triple-structure/plan.md     |  434 +++++
 .../084-harness-triple-structure/quickstart.md     |  152 ++
 .../084-harness-triple-structure/requirements.md   |  285 ++++
 .../specs/084-harness-triple-structure/research.md |  157 ++
 .../specs/084-harness-triple-structure/tasks.md    |  261 +++
 .../account-clause-coverage-tasks.txt              |  701 ++++++++
 .../test-evidence/account-clause-coverage.txt      | 1075 ++++++++++++
 .../test-evidence/analyze-report-2026-11-05.md     |  172 ++
 .../analyze-report-round2-2026-11-05.md            |  256 +++
 .../analyze-report-round3-2026-11-05.md            |  235 +++
 .../test-evidence/analyze-round2-targeted-run.txt  |  104 ++
 .../test-evidence/analyze-round2-targeted-set.txt  |   21 +
 .../analyze-round3-gates-2026-11-05.txt            |  179 ++
 .../test-evidence/analyze-round3-targeted-run.txt  |   77 +
 .../test-evidence/analyze-round3-targeted-set.txt  |   22 +
 .../baseline-full-suite-2026-11-05.txt             | 1172 +++++++++++++
 .../test-evidence/baseline-pre-existing-failed.txt |   23 +
 .../test-evidence/baseline-reading-2026-11-05.md   |   73 +
 .../test-evidence/checklist-self-check.txt         |  268 +++
 .../test-evidence/clarify-adjudication.txt         |  110 ++
 .../test-evidence/clause-extract-5-contracts.txt   |   66 +
 .../test-evidence/coverage-baseline-freeze.txt     |   32 +
 .../test-evidence/decomposition-plan-repair.txt    |    3 +
 .../test-evidence/decomposition-plan.txt           |    8 +
 .../test-evidence/decomposition-tasks-repair.txt   |   19 +
 .../test-evidence/decomposition-tasks.txt          |   25 +
 .../test-evidence/f07-test-file-readings.txt       |  128 ++
 .../test-evidence/final-contract-module.txt        |   15 +
 .../test-evidence/final-duplicate-face.txt         |    5 +
 .../test-evidence/flow-class-lookup-checklist.txt  |    8 +
 .../test-evidence/flow-class-lookup-clarify.txt    |    7 +
 .../test-evidence/flow-class-lookup.txt            |    9 +
 ...lement-part1-attempt1-targeted-failed-names.txt |   32 +
 .../implement-part1-t007-closeout-2026-11-05.txt   |  231 +++
 .../implement-part1-targeted-run-2026-11-05.txt    | 1002 +++++++++++
 .../test-evidence/implement-part1-targeted-set.txt |  226 +++
 ...ment-part2a-closure-targeted-run-2026-11-05.txt |  963 +++++++++++
 ...t-part2a-closure-targeted-run-r2-2026-11-05.txt |  629 +++++++
 ...art2a-mirror-parity-supplemental-2026-11-05.txt |  495 ++++++
 .../implement-part2a-targeted-run-2026-11-05.txt   | 1395 +++++++++++++++
 ...implement-part2a-targeted-run-r2-2026-11-05.txt | 1212 +++++++++++++
 .../implement-part2a-targeted-set.txt              |  235 +++
 .../implement-part2b-targeted-run-2026-11-05.txt   |  409 +++++
 .../implement-part2b-targeted-set.txt              |   29 +
 ...ment-part2c-declaration-readings-2026-11-05.txt |  109 ++
 .../implement-part2c-targeted-run-2026-11-05.txt   |  354 ++++
 ...plement-part2d-closure-brief-set-2026-11-05.txt |  295 ++++
 ...mplement-part2d-closure-readings-2026-11-05.txt |  144 ++
 ...ment-part2d-closure-targeted-set-2026-11-05.txt |  348 ++++
 ...ment-part2d-declaration-readings-2026-11-05.txt |  191 +++
 .../implement-part2d-targeted-run-2026-11-05.txt   |  323 ++++
 .../implement-part2d-targeted-set-2026-11-05.txt   |  348 ++++
 .../implement-part5-readings-2026-11-05.txt        |  163 ++
 .../test-evidence/plan-readings.txt                |   85 +
 .../plan-reopen-pathA-gates-2026-11-05.txt         |  793 +++++++++
 .../plan-reopen-pathA-targeted-run.txt             |   17 +
 .../test-evidence/pre-analyze-clarify.txt          |    2 +
 .../test-evidence/pre-analyze-plan-repair.txt      |    4 +
 .../pre-analyze-plan-tasks-repair.txt              |   22 +
 .../test-evidence/pre-analyze-plan.txt             |    9 +
 .../pre-analyze-requirements-repair.txt            |   22 +
 .../test-evidence/red-first-run-2026-11-05.txt     |  399 +++++
 .../test-evidence/smoke-run1-2026-11-05.txt        |  270 +++
 .../test-evidence/smoke-run2-2026-11-05.txt        |  270 +++
 .../test-evidence/specify-init-source-route.txt    |   44 +
 .../test-evidence/stage-status.md                  | 1780 ++++++++++++++++++++
 .../test-evidence/t004-structure-reading.txt       |   96 ++
 .../t018-coverage-run1-2026-11-05.txt              |  274 +++
 .../t018-coverage-run2-2026-11-05.txt              |  274 +++
 .../t026-mirror-projection-run1-2026-11-05.txt     |   89 +
 .../t026-mirror-projection-run2-2026-11-05.txt     |   47 +
 .../t032-classification-readings-2026-11-05.txt    | 1159 +++++++++++++
 .../test-evidence/tasks-readings.txt               |  193 +++
 .../test-evidence/us1-single-definition-point.txt  |  255 +++
 .../validate-decision-tensions-repair.txt          |   13 +
 .../test-evidence/validate-requirements-repair.txt |   12 +
 .../test-evidence/validate-requirements.txt        |   51 +
 .../test-evidence/validate-tasks-repair.txt        |   20 +
 .../test-evidence/validate-tasks.txt               |   25 +
 .../084-harness-triple-structure/verification.md   |  133 ++
 .specify/templates/review-template.md              |    6 +
 CHANGELOG.md                                       |   11 +
 docs/concepts/harness-triple-structure.md          |   47 +
 docs/reference/commands/sanitize.md                |    2 +-
 docs/reference/skills/feedback.md                  |   10 +-
 docs/reference/skills/memory.md                    |   10 +-
 scripts/python/closure-acceptance-check.py         |  149 +-
 scripts/python/declaration_reader.py               |  469 ++++++
 scripts/python/evidence-utils.py                   |   40 +-
 scripts/python/exec-quant.py                       |  132 +-
 scripts/python/feedback-utils.py                   |   82 +-
 scripts/python/flow-class-check.py                 |  141 +-
 scripts/python/harness-triple-check.py             |  596 +++++++
 scripts/python/history-utils.py                    |   76 +-
 scripts/python/memory-utils.py                     |   31 +-
 scripts/python/probe-utils.py                      |  100 +-
 scripts/python/record-retention.py                 |   47 +-
 scripts/python/trigger-utils.py                    |  105 +-
 scripts/python/validate-requirements.py            |   54 +-
 shared/declarations/contract.yaml                  |   62 +
 shared/declarations/exclusions/.gitkeep            |    0
 .../declarations/exclusions/no-harness-asset.yaml  |  269 +++
 .../declarations/exclusions/no-machine-fact.yaml   |  313 ++++
 shared/declarations/facts/.gitkeep                 |    0
 shared/declarations/facts/arc-verdict-mapping.yaml |   38 +
 .../facts/driver-completion-sentinels.yaml         |   26 +
 shared/declarations/facts/driver-gate-roster.yaml  |   37 +
 .../declarations/facts/driver-stage-artifacts.yaml |   79 +
 .../declarations/facts/driver-stage-sequence.yaml  |   27 +
 shared/declarations/facts/evidence-lanes.yaml      |   23 +
 .../declarations/facts/evidence-seven-states.yaml  |   27 +
 .../declarations/facts/expression-gate-faces.yaml  |   19 +
 .../facts/expression-stage-operator-table.yaml     |   23 +
 .../facts/feedback-prompt-threshold.yaml           |   19 +
 shared/declarations/facts/flow-class-basis.yaml    |   17 +
 shared/declarations/facts/flow-class-classes.yaml  |   19 +
 .../facts/flow-class-document-types.yaml           |   19 +
 .../facts/flow-class-ledger-columns.yaml           |   18 +
 .../facts/flow-class-neutral-categories.yaml       |   18 +
 .../facts/history-manifest-schema.yaml             |   30 +
 .../facts/memory-retention-thresholds.yaml         |   31 +
 shared/declarations/facts/memory-types.yaml        |   21 +
 shared/declarations/facts/probe-class-values.yaml  |   46 +
 .../facts/probe-object-binding-map.yaml            |   26 +
 shared/declarations/facts/quant-record-schema.yaml |   90 +
 .../facts/success-criterion-path-values.yaml       |   23 +
 .../declarations/facts/trigger-state-schema.yaml   |   47 +
 shared/definitions/flow-class-definitions.md       |   23 +-
 shared/definitions/framework-map.md                |    3 +
 shared/definitions/harness-triple-definitions.md   |  154 ++
 shared/definitions/probe-definitions.md            |   15 +
 shared/guidelines/better-harness.md                |    2 +-
 shared/guidelines/proactive-trigger.md             |    1 +
 shared/workflow/acceptance-hardening.md            |    6 +
 shared/workflow/evidence-step.md                   |    2 +-
 shared/workflow/expression-gates.md                |    8 +
 shared/workflow/feedback-step.md                   |    7 +-
 skills/external/sdd-loop-driver/SKILL.md           |    3 +-
 .../sdd-loop-driver/references/efficiency-model.md |    2 +
 .../sdd-loop-driver/references/state-awareness.md  |    2 +
 .../external/sdd-loop-driver/scripts/loop-state.py |  224 ++-
 .../sdd-loop-driver/scripts/pre-analyze-check.py   |  236 ++-
 skills/internal/collect-evidence/SKILL.md          |    4 +-
 .../references/evidence-discipline.md              |   27 +-
 skills/internal/manage-history/SKILL.md            |    2 +
 skills/internal/memory-recall/SKILL.md             |   10 +-
 skills/internal/memory-record/SKILL.md             |   10 +-
 skills/internal/review-sdd-process/SKILL.md        |    5 +-
 templates/commands/history.md                      |    3 +-
 templates/commands/requirements.md                 |    1 +
 templates/commands/review.md                       |    2 +
 templates/review-template.md                       |    6 +
 tests/contract/test_compile_embeds.py              |    5 +
 tests/contract/test_expression_compatibility.py    |   84 +-
 tests/contract/test_harness_triple_structure.py    |  680 ++++++++
 tests/contract/test_store_state_protocol.py        |    7 +
 .../branch-a/scripts/python/evidence-utils.py      |    6 +
 .../declarations/facts/evidence-seven-states.yaml  |   10 +
 .../branch-b/scripts/python/flow-class-check.py    |    6 +
 .../declarations/facts/flow-class-classes.yaml     |    9 +
 .../shared/workflow/feedback-step.md               |    4 +
 .../shared/declarations/facts/.gitkeep             |    0
 .../shared/workflow/feedback-step.md               |    4 +
 .../scripts/python/feedback-utils.py               |    6 +
 .../facts/feedback-prompt-threshold.yaml           |    8 +
 .../shared/workflow/feedback-step.md               |    5 +
 .../scripts/python/feedback-utils.py               |    6 +
 .../facts/feedback-prompt-threshold-copy.yaml      |    7 +
 .../facts/feedback-prompt-threshold.yaml           |    8 +
 .../shared/workflow/feedback-step.md               |    5 +
 .../declarations/exclusions/no-machine-fact.yaml   |    3 +
 .../skills/internal/humanize/SKILL.md              |    4 +
 .../skills/internal/humanize/scripts/rewrite.py    |    5 +
 .../scripts/python/feedback-utils.py               |    6 +
 .../facts/feedback-prompt-threshold.yaml           |    8 +
 .../shared/workflow/feedback-step.md               |    7 +
 .../scripts/python/flow-class-check.py             |    5 +
 .../shared/declarations/facts/.gitkeep             |    0
 .../shared/workflow/gate-roster.md                 |    4 +
 .../positive/scripts/python/feedback-utils.py      |    6 +
 .../declarations/exclusions/no-harness-asset.yaml  |    3 +
 .../facts/feedback-prompt-threshold.yaml           |    8 +
 .../positive/shared/workflow/feedback-step.md      |    8 +
 .../positive/skills/external/draw-diagram/SKILL.md |    7 +
 .../external/draw-diagram/scripts/render_asset.py  |    5 +
 .../declarations/exclusions/no-machine-fact.yaml   |    3 +
 .../skills/internal/summarize-project/SKILL.md     |    7 +
 .../summarize-project/scripts/summarize.py         |    5 +
 276 files changed, 32171 insertions(+), 390 deletions(-)
```

---

## Review 意见


### 🔴 [BLOCKING] scripts/python/closure-acceptance-check.py (Line 223)

> The declared closed set `flow-class-classes` still has an inline copy in three engines the declaration does not name as consumers: `FLOW_CLASSES = ("execution", "expression")` here (223) and at skills/external/sdd-loop-driver/scripts/pre-analyze-check.py:332, plus `EXECUTION_CLASS = "execution"` at scripts/python/validate-requirements.py:99. The fact flow-class-classes.yaml lists one consumer (flow-class-check.py), so C-033 always-green cannot see them: it inspects candidate carriers only. Consequence is measurable, not stylistic -- add a third member to the declaration alone and flow-class-check accepts it while these two gates still reject it, which is exactly US2 acceptance scenario 2 (`只改声明文件 -> 门禁立刻接受新取值`) and the one-machine-read-copy property SC-002 claims. All three files are inside this slice delta (T012/T013/T024 edited them).

<sub>23:58:08</sub>


### 🟠 [IMPORTANT] scripts/python/closure-acceptance-check.py (Line 110)

> FR-012 as written cannot be satisfied by one shipped file, and the engines resolve it two opposite ways. FR-012 says `声明存在 ⇒ 该引擎的内联值 MUST 被删除（MUST NOT 双读）；声明缺席 ⇒ 允许沿用内联值`, but a single source file is what ships to both trees. The slice therefore contains both readings: feedback-utils.py / evidence-utils.py / flow-class-check.py delete the inline copy and degrade loudly (empty set + STR-014 label, or exit 2), while closure-acceptance-check.py (ARC_FALLBACK_* here and at 110-135), skills/external/sdd-loop-driver/scripts/loop-state.py and pre-analyze-check.py keep the pre-migration literals as a labelled fallback. Both are defensible; shipping both means the same rule has two implementations, and the retained fallback is a second copy a reader still has to keep in step (docs/concepts/harness-triple-structure.md states the engine carries no second copy). Decision needed at requirements level, not per engine.

<sub>23:58:12</sub>


### 🟠 [IMPORTANT] scripts/python/harness-triple-check.py (Line 440)

> `verify` prints `residual_literals: "delegated: ..."` -- a constant string, not a reading -- while C-032 enumerates `residual literals via the reused duplicate-fact reading` as one of the things verify judges. The two clauses cannot both hold: C-038 forbids a subprocess and FR-010 forbids a second scanner, so the only way to run that reading from inside this engine is to import a script whose file name is not importable (doc-consistency-check.py). The implementation picked the clause that yields a green and documented the choice in the module docstring, which is honest, but the contract now has an unsatisfiable conjunct and `verify` exit 0 reads as if residual literals were checked. Fix on the contract side (drop the clause from C-032 and name the separate run as the evidence carrier) or add an explicit `residual-literals: not-evaluated` state so a green cannot be over-read.

<sub>23:58:16</sub>


### 🟢 [SUGGESTION] scripts/python/closure-acceptance-check.py (Line 173)

> `FINAL_PATH_PASS_BUCKET = "pass"` re-spells a member of the declared bucket set (arc-verdict-mapping.yaml#/statement/final_path_buckets) in the same file that reads that declaration, and it is used as a bucket key (`counts[FINAL_PATH_PASS_BUCKET]`, 934) as well as a status comparison (939). The docstring argues it names the value from the status-vocabulary side, which is true of the comparison but not of the dict key: if the declared buckets ever lose `pass`, that line raises KeyError instead of reporting a finding. Deriving it once from FINAL_PATH_BUCKETS (or declaring the pass bucket explicitly in the fact) removes the coupling.

<sub>23:58:19</sub>


### 🔴 [BLOCKING] scripts/python/closure-acceptance-check.py (Line 916)

> Same defect class at a migration that WAS performed as specified, so it is not only a roster gap. `success-criterion-path-values.yaml` names this engine as a consumer and the engine does read it (PATH_VALUES at 121, membership test at 610) -- yet three comparison sites still spell the member: `if path != "final"` (916), `criteria[sc_id] == "final"` (939), `path == "final"` (1347); scripts/python/validate-requirements.py:395 does the same. This is the FR-012 `MUST NOT 双读` shape: the declaration is read for the membership verdict and the same member is re-spelled for every branch, so renaming or extending the declared set leaves the branches comparing against a stale literal while the membership test says green. Fix: derive the pass-path member once from PATH_VALUES (or carry it in the fact) and compare against that value. No test in the slice would have caught it -- the contract module asserts the membership rejection, not that no member literal survives.

<sub>23:58:31</sub>


### ⚪ [NITPICK] scripts/python/declaration_reader.py (Line 220)

> Dead branch: `if value[:2] in ("|-", ">-", "|+", ">+")` can never be reached because the preceding `if value[0] in _FORBIDDEN_MARKERS` already refuses any value starting with `|` or `>`. Harmless (the refusal still happens, with the shorter message) but it reads as if block scalars had a second, more specific guard, so a later editor may "fix" one and believe the other still covers it.

<sub>23:58:40</sub>


### 🟢 [SUGGESTION] scripts/python/declaration_reader.py (Line 171)

> A nested inline sequence is silently parsed as a string instead of being refused. `_tokens` splits `- key: value` into a marker plus a mapping, but for `- - name` `_looks_like_mapping("- name")` is False, so the item becomes the scalar `"- name"` rather than a nested sequence. The subset explicitly excludes flow collections and block scalars and refuses everything else it does not model, so accepting a construct it cannot represent is the one shape the module docstring forbids (no best-effort parse). Low blast radius today because no declaration uses it; add an explicit refusal if the subset is meant to be closed.

<sub>23:58:40</sub>


### 👍 [PRAISE] scripts/python/flow-class-check.py (Line 2735)

> The refusal here is what the feature asks for and is easy to get wrong: when any declared closed set is unreadable the engine exits 2 with the STR-014 labels and says it will not judge against an absent set, instead of running with `CLASS_VALUES = ()`. loop-state.py and pre-analyze-check.py make the opposite (also defensible) choice, so the two styles differ -- but this one cannot silently misclassify, and it names the fact it could not read.

<sub>23:58:40</sub>




> **未提交范围（未评审）**: 30 个未提交路径未计入本次评审对象（.specify/memory/session/20261102T231648Z-run-determination-speckit-clarify-r20261102t225758z-081a.md, .specify/memory/exec-quant/records/20261105T075132768628Z-cf37e921.json, .specify/memory/exec-quant/records/20261105T080159336037Z-7f8a3419.json, .specify/memory/exec-quant/records/20261105T082009374970Z-a1347a99.json, .specify/memory/exec-quant/records/20261105T083525969720Z-0c4b8437.json, .specify/memory/exec-quant/records/20261105T084309278446Z-6ee2f63f.json, .specify/memory/exec-quant/records/20261105T085419852858Z-eb6daa1e.json, .specify/memory/exec-quant/records/20261105T094511658251Z-1d71de8a.json, .specify/memory/exec-quant/records/20261105T094750637884Z-90e0cae3.json, .specify/memory/exec-quant/records/20261105T111724911488Z-17c66632.json, .specify/memory/feedback/20261105T075137Z-speckit-requirements.md, .specify/memory/feedback/20261105T080203Z-speckit-clarify.md, .specify/memory/feedback/20261105T082017Z-speckit-plan.md, .specify/memory/feedback/20261105T083530Z-speckit-tasks.md, .specify/memory/feedback/20261105T084312Z-speckit-checklist.md, .specify/memory/feedback/20261105T085423Z-speckit-analyze.md, .specify/memory/feedback/20261105T094516Z-speckit-analyze.md, .specify/memory/feedback/20261105T094753Z-skill-sdd-loop-driver.md, .specify/memory/feedback/20261105T111730Z-speckit-analyze.md, .specify/memory/session/20261105T075127Z-run-determination-speckit-requirements-r20261105t074027z-084.md, .specify/memory/session/20261105T080146Z-run-determination-speckit-clarify-r20261105t074027z-084a.md, .specify/memory/session/20261105T082004Z-run-determination-speckit-plan-r20261105t074027z-084a.md, .specify/memory/session/20261105T083523Z-run-determination-speckit-tasks-r20261105t074027z-084a.md, .specify/memory/session/20261105T084306Z-run-determination-speckit-checklist-r20261105t074027z-084a.md, .specify/memory/session/20261105T085413Z-run-determination-speckit-analyze-r20261105t074027z-084a.md, .specify/memory/session/20261105T094508Z-run-determination-speckit-analyze-r20261105t074027z-084a-r2.md, .specify/memory/session/20261105T094745Z-run-determination-skill-sdd-loop-driver-r20261105t074027z-08.md, .specify/memory/session/20261105T111722Z-run-determination-speckit-analyze-r20261105t074027z-084a-r3.md, .specify/specs/084-harness-triple-structure/test-evidence/review-smoke-2026-11-05.txt, .specify/state/084-harness-triple-structure.md）；本回执不对该范围给出任何结论。

<!-- coverage-receipt:begin -->
receipt_version=1
base=3ffeb26e4880f134f7a5e220ecbffb869f165632
head=03a19487e4ceb668e27ef1a4554aff82e4dc8a4c
base_source=feature-first-commit
renderer=text
changed_files=276
judged_files=39
skipped_files=237
gap_files=0
lines_added=32171
lines_deleted=390
file.001.path=.claude/commands/speckit.history.md
file.001.verdict=skipped
file.001.reason=generated
file.002.path=.claude/commands/speckit.requirements.md
file.002.verdict=skipped
file.002.reason=generated
file.003.path=.claude/commands/speckit.review.md
file.003.verdict=skipped
file.003.reason=generated
file.004.path=.github/prompts/speckit.history.prompt.md
file.004.verdict=skipped
file.004.reason=generated
file.005.path=.github/prompts/speckit.requirements.prompt.md
file.005.verdict=skipped
file.005.reason=generated
file.006.path=.github/prompts/speckit.review.prompt.md
file.006.verdict=skipped
file.006.reason=generated
file.007.path=.opencode/command/speckit.history.md
file.007.verdict=skipped
file.007.reason=generated
file.008.path=.opencode/command/speckit.requirements.md
file.008.verdict=skipped
file.008.reason=generated
file.009.path=.opencode/command/speckit.review.md
file.009.verdict=skipped
file.009.reason=generated
file.010.path=.qoder/commands/speckit.history.md
file.010.verdict=skipped
file.010.reason=generated
file.011.path=.qoder/commands/speckit.requirements.md
file.011.verdict=skipped
file.011.reason=generated
file.012.path=.qoder/commands/speckit.review.md
file.012.verdict=skipped
file.012.reason=generated
file.013.path=.specify/memory/features.md
file.013.verdict=skipped
file.013.reason=generated
file.014.path=.specify/memory/features/081.md
file.014.verdict=skipped
file.014.reason=generated
file.015.path=.specify/memory/features/084.md
file.015.verdict=skipped
file.015.reason=generated
file.016.path=.specify/scripts/python/closure-acceptance-check.py
file.016.verdict=skipped
file.016.reason=generated
file.017.path=.specify/scripts/python/declaration_reader.py
file.017.verdict=skipped
file.017.reason=generated
file.018.path=.specify/scripts/python/evidence-utils.py
file.018.verdict=skipped
file.018.reason=generated
file.019.path=.specify/scripts/python/exec-quant.py
file.019.verdict=skipped
file.019.reason=generated
file.020.path=.specify/scripts/python/feedback-utils.py
file.020.verdict=skipped
file.020.reason=generated
file.021.path=.specify/scripts/python/flow-class-check.py
file.021.verdict=skipped
file.021.reason=generated
file.022.path=.specify/scripts/python/harness-triple-check.py
file.022.verdict=skipped
file.022.reason=generated
file.023.path=.specify/scripts/python/history-utils.py
file.023.verdict=skipped
file.023.reason=generated
file.024.path=.specify/scripts/python/memory-utils.py
file.024.verdict=skipped
file.024.reason=generated
file.025.path=.specify/scripts/python/probe-utils.py
file.025.verdict=skipped
file.025.reason=generated
file.026.path=.specify/scripts/python/record-retention.py
file.026.verdict=skipped
file.026.reason=generated
file.027.path=.specify/scripts/python/trigger-utils.py
file.027.verdict=skipped
file.027.reason=generated
file.028.path=.specify/scripts/python/validate-requirements.py
file.028.verdict=skipped
file.028.reason=generated
file.029.path=.specify/shared/declarations/contract.yaml
file.029.verdict=skipped
file.029.reason=generated
file.030.path=.specify/shared/declarations/exclusions/no-harness-asset.yaml
file.030.verdict=skipped
file.030.reason=generated
file.031.path=.specify/shared/declarations/exclusions/no-machine-fact.yaml
file.031.verdict=skipped
file.031.reason=generated
file.032.path=.specify/shared/declarations/facts/arc-verdict-mapping.yaml
file.032.verdict=skipped
file.032.reason=generated
file.033.path=.specify/shared/declarations/facts/driver-completion-sentinels.yaml
file.033.verdict=skipped
file.033.reason=generated
file.034.path=.specify/shared/declarations/facts/driver-gate-roster.yaml
file.034.verdict=skipped
file.034.reason=generated
file.035.path=.specify/shared/declarations/facts/driver-stage-artifacts.yaml
file.035.verdict=skipped
file.035.reason=generated
file.036.path=.specify/shared/declarations/facts/driver-stage-sequence.yaml
file.036.verdict=skipped
file.036.reason=generated
file.037.path=.specify/shared/declarations/facts/evidence-lanes.yaml
file.037.verdict=skipped
file.037.reason=generated
file.038.path=.specify/shared/declarations/facts/evidence-seven-states.yaml
file.038.verdict=skipped
file.038.reason=generated
file.039.path=.specify/shared/declarations/facts/expression-gate-faces.yaml
file.039.verdict=skipped
file.039.reason=generated
file.040.path=.specify/shared/declarations/facts/expression-stage-operator-table.yaml
file.040.verdict=skipped
file.040.reason=generated
file.041.path=.specify/shared/declarations/facts/feedback-prompt-threshold.yaml
file.041.verdict=skipped
file.041.reason=generated
file.042.path=.specify/shared/declarations/facts/flow-class-basis.yaml
file.042.verdict=skipped
file.042.reason=generated
file.043.path=.specify/shared/declarations/facts/flow-class-classes.yaml
file.043.verdict=skipped
file.043.reason=generated
file.044.path=.specify/shared/declarations/facts/flow-class-document-types.yaml
file.044.verdict=skipped
file.044.reason=generated
file.045.path=.specify/shared/declarations/facts/flow-class-ledger-columns.yaml
file.045.verdict=skipped
file.045.reason=generated
file.046.path=.specify/shared/declarations/facts/flow-class-neutral-categories.yaml
file.046.verdict=skipped
file.046.reason=generated
file.047.path=.specify/shared/declarations/facts/history-manifest-schema.yaml
file.047.verdict=skipped
file.047.reason=generated
file.048.path=.specify/shared/declarations/facts/memory-retention-thresholds.yaml
file.048.verdict=skipped
file.048.reason=generated
file.049.path=.specify/shared/declarations/facts/memory-types.yaml
file.049.verdict=skipped
file.049.reason=generated
file.050.path=.specify/shared/declarations/facts/probe-class-values.yaml
file.050.verdict=skipped
file.050.reason=generated
file.051.path=.specify/shared/declarations/facts/probe-object-binding-map.yaml
file.051.verdict=skipped
file.051.reason=generated
file.052.path=.specify/shared/declarations/facts/quant-record-schema.yaml
file.052.verdict=skipped
file.052.reason=generated
file.053.path=.specify/shared/declarations/facts/success-criterion-path-values.yaml
file.053.verdict=skipped
file.053.reason=generated
file.054.path=.specify/shared/declarations/facts/trigger-state-schema.yaml
file.054.verdict=skipped
file.054.reason=generated
file.055.path=.specify/shared/definitions/flow-class-definitions.md
file.055.verdict=skipped
file.055.reason=generated
file.056.path=.specify/shared/definitions/framework-map.md
file.056.verdict=skipped
file.056.reason=generated
file.057.path=.specify/shared/definitions/harness-triple-definitions.md
file.057.verdict=skipped
file.057.reason=generated
file.058.path=.specify/shared/definitions/probe-definitions.md
file.058.verdict=skipped
file.058.reason=generated
file.059.path=.specify/shared/guidelines/better-harness.md
file.059.verdict=skipped
file.059.reason=generated
file.060.path=.specify/shared/guidelines/proactive-trigger.md
file.060.verdict=skipped
file.060.reason=generated
file.061.path=.specify/shared/workflow/acceptance-hardening.md
file.061.verdict=skipped
file.061.reason=generated
file.062.path=.specify/shared/workflow/evidence-step.md
file.062.verdict=skipped
file.062.reason=generated
file.063.path=.specify/shared/workflow/expression-gates.md
file.063.verdict=skipped
file.063.reason=generated
file.064.path=.specify/shared/workflow/feedback-step.md
file.064.verdict=skipped
file.064.reason=generated
file.065.path=.specify/skills/internal/collect-evidence/SKILL.md
file.065.verdict=skipped
file.065.reason=generated
file.066.path=.specify/skills/internal/collect-evidence/references/evidence-discipline.md
file.066.verdict=skipped
file.066.reason=generated
file.067.path=.specify/skills/internal/manage-history/SKILL.md
file.067.verdict=skipped
file.067.reason=generated
file.068.path=.specify/skills/internal/memory-recall/SKILL.md
file.068.verdict=skipped
file.068.reason=generated
file.069.path=.specify/skills/internal/memory-record/SKILL.md
file.069.verdict=skipped
file.069.reason=generated
file.070.path=.specify/skills/internal/review-sdd-process/SKILL.md
file.070.verdict=skipped
file.070.reason=generated
file.071.path=.specify/skills/sdd-loop-driver/SKILL.md
file.071.verdict=skipped
file.071.reason=generated
file.072.path=.specify/skills/sdd-loop-driver/references/efficiency-model.md
file.072.verdict=skipped
file.072.reason=generated
file.073.path=.specify/skills/sdd-loop-driver/references/state-awareness.md
file.073.verdict=skipped
file.073.reason=generated
file.074.path=.specify/skills/sdd-loop-driver/scripts/loop-state.py
file.074.verdict=skipped
file.074.reason=generated
file.075.path=.specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py
file.075.verdict=skipped
file.075.reason=generated
file.076.path=.specify/specs/084-harness-triple-structure/baseline-failed.txt
file.076.verdict=skipped
file.076.reason=non-code-file
file.077.path=.specify/specs/084-harness-triple-structure/checklists/layer-criteria-2026-11-05.md
file.077.verdict=skipped
file.077.reason=non-code-file
file.078.path=.specify/specs/084-harness-triple-structure/checklists/requirements.md
file.078.verdict=skipped
file.078.reason=non-code-file
file.079.path=.specify/specs/084-harness-triple-structure/contracts/declaration-schema.contract.md
file.079.verdict=skipped
file.079.reason=non-code-file
file.080.path=.specify/specs/084-harness-triple-structure/contracts/distribution-and-mirror.contract.md
file.080.verdict=skipped
file.080.reason=non-code-file
file.081.path=.specify/specs/084-harness-triple-structure/contracts/harness-triple-check.contract.md
file.081.verdict=skipped
file.081.reason=non-code-file
file.082.path=.specify/specs/084-harness-triple-structure/contracts/migration-batches.contract.md
file.082.verdict=skipped
file.082.reason=non-code-file
file.083.path=.specify/specs/084-harness-triple-structure/contracts/shared-reader.contract.md
file.083.verdict=skipped
file.083.reason=non-code-file
file.084.path=.specify/specs/084-harness-triple-structure/coverage-baseline.txt
file.084.verdict=skipped
file.084.reason=non-code-file
file.085.path=.specify/specs/084-harness-triple-structure/data-model.md
file.085.verdict=skipped
file.085.reason=non-code-file
file.086.path=.specify/specs/084-harness-triple-structure/feature-ref.md
file.086.verdict=skipped
file.086.reason=non-code-file
file.087.path=.specify/specs/084-harness-triple-structure/notes/pre-change-measurements.md
file.087.verdict=skipped
file.087.reason=non-code-file
file.088.path=.specify/specs/084-harness-triple-structure/notes/red-first-evidence.md
file.088.verdict=skipped
file.088.reason=non-code-file
file.089.path=.specify/specs/084-harness-triple-structure/plan.md
file.089.verdict=skipped
file.089.reason=non-code-file
file.090.path=.specify/specs/084-harness-triple-structure/quickstart.md
file.090.verdict=skipped
file.090.reason=non-code-file
file.091.path=.specify/specs/084-harness-triple-structure/requirements.md
file.091.verdict=skipped
file.091.reason=non-code-file
file.092.path=.specify/specs/084-harness-triple-structure/research.md
file.092.verdict=skipped
file.092.reason=non-code-file
file.093.path=.specify/specs/084-harness-triple-structure/tasks.md
file.093.verdict=skipped
file.093.reason=non-code-file
file.094.path=.specify/specs/084-harness-triple-structure/test-evidence/account-clause-coverage-tasks.txt
file.094.verdict=skipped
file.094.reason=non-code-file
file.095.path=.specify/specs/084-harness-triple-structure/test-evidence/account-clause-coverage.txt
file.095.verdict=skipped
file.095.reason=non-code-file
file.096.path=.specify/specs/084-harness-triple-structure/test-evidence/analyze-report-2026-11-05.md
file.096.verdict=skipped
file.096.reason=non-code-file
file.097.path=.specify/specs/084-harness-triple-structure/test-evidence/analyze-report-round2-2026-11-05.md
file.097.verdict=skipped
file.097.reason=non-code-file
file.098.path=.specify/specs/084-harness-triple-structure/test-evidence/analyze-report-round3-2026-11-05.md
file.098.verdict=skipped
file.098.reason=non-code-file
file.099.path=.specify/specs/084-harness-triple-structure/test-evidence/analyze-round2-targeted-run.txt
file.099.verdict=skipped
file.099.reason=non-code-file
file.100.path=.specify/specs/084-harness-triple-structure/test-evidence/analyze-round2-targeted-set.txt
file.100.verdict=skipped
file.100.reason=non-code-file
file.101.path=.specify/specs/084-harness-triple-structure/test-evidence/analyze-round3-gates-2026-11-05.txt
file.101.verdict=skipped
file.101.reason=non-code-file
file.102.path=.specify/specs/084-harness-triple-structure/test-evidence/analyze-round3-targeted-run.txt
file.102.verdict=skipped
file.102.reason=non-code-file
file.103.path=.specify/specs/084-harness-triple-structure/test-evidence/analyze-round3-targeted-set.txt
file.103.verdict=skipped
file.103.reason=non-code-file
file.104.path=.specify/specs/084-harness-triple-structure/test-evidence/baseline-full-suite-2026-11-05.txt
file.104.verdict=skipped
file.104.reason=non-code-file
file.105.path=.specify/specs/084-harness-triple-structure/test-evidence/baseline-pre-existing-failed.txt
file.105.verdict=skipped
file.105.reason=non-code-file
file.106.path=.specify/specs/084-harness-triple-structure/test-evidence/baseline-reading-2026-11-05.md
file.106.verdict=skipped
file.106.reason=non-code-file
file.107.path=.specify/specs/084-harness-triple-structure/test-evidence/checklist-self-check.txt
file.107.verdict=skipped
file.107.reason=non-code-file
file.108.path=.specify/specs/084-harness-triple-structure/test-evidence/clarify-adjudication.txt
file.108.verdict=skipped
file.108.reason=non-code-file
file.109.path=.specify/specs/084-harness-triple-structure/test-evidence/clause-extract-5-contracts.txt
file.109.verdict=skipped
file.109.reason=non-code-file
file.110.path=.specify/specs/084-harness-triple-structure/test-evidence/coverage-baseline-freeze.txt
file.110.verdict=skipped
file.110.reason=non-code-file
file.111.path=.specify/specs/084-harness-triple-structure/test-evidence/decomposition-plan-repair.txt
file.111.verdict=skipped
file.111.reason=non-code-file
file.112.path=.specify/specs/084-harness-triple-structure/test-evidence/decomposition-plan.txt
file.112.verdict=skipped
file.112.reason=non-code-file
file.113.path=.specify/specs/084-harness-triple-structure/test-evidence/decomposition-tasks-repair.txt
file.113.verdict=skipped
file.113.reason=non-code-file
file.114.path=.specify/specs/084-harness-triple-structure/test-evidence/decomposition-tasks.txt
file.114.verdict=skipped
file.114.reason=non-code-file
file.115.path=.specify/specs/084-harness-triple-structure/test-evidence/f07-test-file-readings.txt
file.115.verdict=skipped
file.115.reason=non-code-file
file.116.path=.specify/specs/084-harness-triple-structure/test-evidence/final-contract-module.txt
file.116.verdict=skipped
file.116.reason=non-code-file
file.117.path=.specify/specs/084-harness-triple-structure/test-evidence/final-duplicate-face.txt
file.117.verdict=skipped
file.117.reason=non-code-file
file.118.path=.specify/specs/084-harness-triple-structure/test-evidence/flow-class-lookup-checklist.txt
file.118.verdict=skipped
file.118.reason=non-code-file
file.119.path=.specify/specs/084-harness-triple-structure/test-evidence/flow-class-lookup-clarify.txt
file.119.verdict=skipped
file.119.reason=non-code-file
file.120.path=.specify/specs/084-harness-triple-structure/test-evidence/flow-class-lookup.txt
file.120.verdict=skipped
file.120.reason=non-code-file
file.121.path=.specify/specs/084-harness-triple-structure/test-evidence/implement-part1-attempt1-targeted-failed-names.txt
file.121.verdict=skipped
file.121.reason=non-code-file
file.122.path=.specify/specs/084-harness-triple-structure/test-evidence/implement-part1-t007-closeout-2026-11-05.txt
file.122.verdict=skipped
file.122.reason=non-code-file
file.123.path=.specify/specs/084-harness-triple-structure/test-evidence/implement-part1-targeted-run-2026-11-05.txt
file.123.verdict=skipped
file.123.reason=non-code-file
file.124.path=.specify/specs/084-harness-triple-structure/test-evidence/implement-part1-targeted-set.txt
file.124.verdict=skipped
file.124.reason=non-code-file
file.125.path=.specify/specs/084-harness-triple-structure/test-evidence/implement-part2a-closure-targeted-run-2026-11-05.txt
file.125.verdict=skipped
file.125.reason=non-code-file
file.126.path=.specify/specs/084-harness-triple-structure/test-evidence/implement-part2a-closure-targeted-run-r2-2026-11-05.txt
file.126.verdict=skipped
file.126.reason=non-code-file
file.127.path=.specify/specs/084-harness-triple-structure/test-evidence/implement-part2a-mirror-parity-supplemental-2026-11-05.txt
file.127.verdict=skipped
file.127.reason=non-code-file
file.128.path=.specify/specs/084-harness-triple-structure/test-evidence/implement-part2a-targeted-run-2026-11-05.txt
file.128.verdict=skipped
file.128.reason=non-code-file
file.129.path=.specify/specs/084-harness-triple-structure/test-evidence/implement-part2a-targeted-run-r2-2026-11-05.txt
file.129.verdict=skipped
file.129.reason=non-code-file
file.130.path=.specify/specs/084-harness-triple-structure/test-evidence/implement-part2a-targeted-set.txt
file.130.verdict=skipped
file.130.reason=non-code-file
file.131.path=.specify/specs/084-harness-triple-structure/test-evidence/implement-part2b-targeted-run-2026-11-05.txt
file.131.verdict=skipped
file.131.reason=non-code-file
file.132.path=.specify/specs/084-harness-triple-structure/test-evidence/implement-part2b-targeted-set.txt
file.132.verdict=skipped
file.132.reason=non-code-file
file.133.path=.specify/specs/084-harness-triple-structure/test-evidence/implement-part2c-declaration-readings-2026-11-05.txt
file.133.verdict=skipped
file.133.reason=non-code-file
file.134.path=.specify/specs/084-harness-triple-structure/test-evidence/implement-part2c-targeted-run-2026-11-05.txt
file.134.verdict=skipped
file.134.reason=non-code-file
file.135.path=.specify/specs/084-harness-triple-structure/test-evidence/implement-part2d-closure-brief-set-2026-11-05.txt
file.135.verdict=skipped
file.135.reason=non-code-file
file.136.path=.specify/specs/084-harness-triple-structure/test-evidence/implement-part2d-closure-readings-2026-11-05.txt
file.136.verdict=skipped
file.136.reason=non-code-file
file.137.path=.specify/specs/084-harness-triple-structure/test-evidence/implement-part2d-closure-targeted-set-2026-11-05.txt
file.137.verdict=skipped
file.137.reason=non-code-file
file.138.path=.specify/specs/084-harness-triple-structure/test-evidence/implement-part2d-declaration-readings-2026-11-05.txt
file.138.verdict=skipped
file.138.reason=non-code-file
file.139.path=.specify/specs/084-harness-triple-structure/test-evidence/implement-part2d-targeted-run-2026-11-05.txt
file.139.verdict=skipped
file.139.reason=non-code-file
file.140.path=.specify/specs/084-harness-triple-structure/test-evidence/implement-part2d-targeted-set-2026-11-05.txt
file.140.verdict=skipped
file.140.reason=non-code-file
file.141.path=.specify/specs/084-harness-triple-structure/test-evidence/implement-part5-readings-2026-11-05.txt
file.141.verdict=skipped
file.141.reason=non-code-file
file.142.path=.specify/specs/084-harness-triple-structure/test-evidence/plan-readings.txt
file.142.verdict=skipped
file.142.reason=non-code-file
file.143.path=.specify/specs/084-harness-triple-structure/test-evidence/plan-reopen-pathA-gates-2026-11-05.txt
file.143.verdict=skipped
file.143.reason=non-code-file
file.144.path=.specify/specs/084-harness-triple-structure/test-evidence/plan-reopen-pathA-targeted-run.txt
file.144.verdict=skipped
file.144.reason=non-code-file
file.145.path=.specify/specs/084-harness-triple-structure/test-evidence/pre-analyze-clarify.txt
file.145.verdict=skipped
file.145.reason=non-code-file
file.146.path=.specify/specs/084-harness-triple-structure/test-evidence/pre-analyze-plan-repair.txt
file.146.verdict=skipped
file.146.reason=non-code-file
file.147.path=.specify/specs/084-harness-triple-structure/test-evidence/pre-analyze-plan-tasks-repair.txt
file.147.verdict=skipped
file.147.reason=non-code-file
file.148.path=.specify/specs/084-harness-triple-structure/test-evidence/pre-analyze-plan.txt
file.148.verdict=skipped
file.148.reason=non-code-file
file.149.path=.specify/specs/084-harness-triple-structure/test-evidence/pre-analyze-requirements-repair.txt
file.149.verdict=skipped
file.149.reason=non-code-file
file.150.path=.specify/specs/084-harness-triple-structure/test-evidence/red-first-run-2026-11-05.txt
file.150.verdict=skipped
file.150.reason=non-code-file
file.151.path=.specify/specs/084-harness-triple-structure/test-evidence/smoke-run1-2026-11-05.txt
file.151.verdict=skipped
file.151.reason=non-code-file
file.152.path=.specify/specs/084-harness-triple-structure/test-evidence/smoke-run2-2026-11-05.txt
file.152.verdict=skipped
file.152.reason=non-code-file
file.153.path=.specify/specs/084-harness-triple-structure/test-evidence/specify-init-source-route.txt
file.153.verdict=skipped
file.153.reason=non-code-file
file.154.path=.specify/specs/084-harness-triple-structure/test-evidence/stage-status.md
file.154.verdict=skipped
file.154.reason=non-code-file
file.155.path=.specify/specs/084-harness-triple-structure/test-evidence/t004-structure-reading.txt
file.155.verdict=skipped
file.155.reason=non-code-file
file.156.path=.specify/specs/084-harness-triple-structure/test-evidence/t018-coverage-run1-2026-11-05.txt
file.156.verdict=skipped
file.156.reason=non-code-file
file.157.path=.specify/specs/084-harness-triple-structure/test-evidence/t018-coverage-run2-2026-11-05.txt
file.157.verdict=skipped
file.157.reason=non-code-file
file.158.path=.specify/specs/084-harness-triple-structure/test-evidence/t026-mirror-projection-run1-2026-11-05.txt
file.158.verdict=skipped
file.158.reason=non-code-file
file.159.path=.specify/specs/084-harness-triple-structure/test-evidence/t026-mirror-projection-run2-2026-11-05.txt
file.159.verdict=skipped
file.159.reason=non-code-file
file.160.path=.specify/specs/084-harness-triple-structure/test-evidence/t032-classification-readings-2026-11-05.txt
file.160.verdict=skipped
file.160.reason=non-code-file
file.161.path=.specify/specs/084-harness-triple-structure/test-evidence/tasks-readings.txt
file.161.verdict=skipped
file.161.reason=non-code-file
file.162.path=.specify/specs/084-harness-triple-structure/test-evidence/us1-single-definition-point.txt
file.162.verdict=skipped
file.162.reason=non-code-file
file.163.path=.specify/specs/084-harness-triple-structure/test-evidence/validate-decision-tensions-repair.txt
file.163.verdict=skipped
file.163.reason=non-code-file
file.164.path=.specify/specs/084-harness-triple-structure/test-evidence/validate-requirements-repair.txt
file.164.verdict=skipped
file.164.reason=non-code-file
file.165.path=.specify/specs/084-harness-triple-structure/test-evidence/validate-requirements.txt
file.165.verdict=skipped
file.165.reason=non-code-file
file.166.path=.specify/specs/084-harness-triple-structure/test-evidence/validate-tasks-repair.txt
file.166.verdict=skipped
file.166.reason=non-code-file
file.167.path=.specify/specs/084-harness-triple-structure/test-evidence/validate-tasks.txt
file.167.verdict=skipped
file.167.reason=non-code-file
file.168.path=.specify/specs/084-harness-triple-structure/verification.md
file.168.verdict=skipped
file.168.reason=non-code-file
file.169.path=.specify/templates/review-template.md
file.169.verdict=skipped
file.169.reason=generated
file.170.path=CHANGELOG.md
file.170.verdict=skipped
file.170.reason=non-code-file
file.171.path=docs/concepts/harness-triple-structure.md
file.171.verdict=skipped
file.171.reason=non-code-file
file.172.path=docs/reference/commands/sanitize.md
file.172.verdict=skipped
file.172.reason=non-code-file
file.173.path=docs/reference/skills/feedback.md
file.173.verdict=skipped
file.173.reason=non-code-file
file.174.path=docs/reference/skills/memory.md
file.174.verdict=skipped
file.174.reason=non-code-file
file.175.path=scripts/python/closure-acceptance-check.py
file.175.verdict=reviewed
file.176.path=scripts/python/declaration_reader.py
file.176.verdict=reviewed
file.177.path=scripts/python/evidence-utils.py
file.177.verdict=reviewed
file.178.path=scripts/python/exec-quant.py
file.178.verdict=skipped
file.178.reason=size-guard-focus-not-reviewed
file.179.path=scripts/python/feedback-utils.py
file.179.verdict=reviewed
file.180.path=scripts/python/flow-class-check.py
file.180.verdict=reviewed
file.181.path=scripts/python/harness-triple-check.py
file.181.verdict=reviewed
file.182.path=scripts/python/history-utils.py
file.182.verdict=reviewed
file.183.path=scripts/python/memory-utils.py
file.183.verdict=reviewed
file.184.path=scripts/python/probe-utils.py
file.184.verdict=skipped
file.184.reason=size-guard-focus-not-reviewed
file.185.path=scripts/python/record-retention.py
file.185.verdict=skipped
file.185.reason=size-guard-focus-not-reviewed
file.186.path=scripts/python/trigger-utils.py
file.186.verdict=skipped
file.186.reason=size-guard-focus-not-reviewed
file.187.path=scripts/python/validate-requirements.py
file.187.verdict=reviewed
file.188.path=shared/declarations/contract.yaml
file.188.verdict=reviewed
file.189.path=shared/declarations/exclusions/.gitkeep
file.189.verdict=reviewed
file.190.path=shared/declarations/exclusions/no-harness-asset.yaml
file.190.verdict=reviewed
file.191.path=shared/declarations/exclusions/no-machine-fact.yaml
file.191.verdict=reviewed
file.192.path=shared/declarations/facts/.gitkeep
file.192.verdict=reviewed
file.193.path=shared/declarations/facts/arc-verdict-mapping.yaml
file.193.verdict=reviewed
file.194.path=shared/declarations/facts/driver-completion-sentinels.yaml
file.194.verdict=reviewed
file.195.path=shared/declarations/facts/driver-gate-roster.yaml
file.195.verdict=reviewed
file.196.path=shared/declarations/facts/driver-stage-artifacts.yaml
file.196.verdict=reviewed
file.197.path=shared/declarations/facts/driver-stage-sequence.yaml
file.197.verdict=reviewed
file.198.path=shared/declarations/facts/evidence-lanes.yaml
file.198.verdict=reviewed
file.199.path=shared/declarations/facts/evidence-seven-states.yaml
file.199.verdict=reviewed
file.200.path=shared/declarations/facts/expression-gate-faces.yaml
file.200.verdict=reviewed
file.201.path=shared/declarations/facts/expression-stage-operator-table.yaml
file.201.verdict=reviewed
file.202.path=shared/declarations/facts/feedback-prompt-threshold.yaml
file.202.verdict=reviewed
file.203.path=shared/declarations/facts/flow-class-basis.yaml
file.203.verdict=reviewed
file.204.path=shared/declarations/facts/flow-class-classes.yaml
file.204.verdict=reviewed
file.205.path=shared/declarations/facts/flow-class-document-types.yaml
file.205.verdict=reviewed
file.206.path=shared/declarations/facts/flow-class-ledger-columns.yaml
file.206.verdict=reviewed
file.207.path=shared/declarations/facts/flow-class-neutral-categories.yaml
file.207.verdict=reviewed
file.208.path=shared/declarations/facts/history-manifest-schema.yaml
file.208.verdict=reviewed
file.209.path=shared/declarations/facts/memory-retention-thresholds.yaml
file.209.verdict=reviewed
file.210.path=shared/declarations/facts/memory-types.yaml
file.210.verdict=reviewed
file.211.path=shared/declarations/facts/probe-class-values.yaml
file.211.verdict=reviewed
file.212.path=shared/declarations/facts/probe-object-binding-map.yaml
file.212.verdict=reviewed
file.213.path=shared/declarations/facts/quant-record-schema.yaml
file.213.verdict=reviewed
file.214.path=shared/declarations/facts/success-criterion-path-values.yaml
file.214.verdict=reviewed
file.215.path=shared/declarations/facts/trigger-state-schema.yaml
file.215.verdict=reviewed
file.216.path=shared/definitions/flow-class-definitions.md
file.216.verdict=skipped
file.216.reason=non-code-file
file.217.path=shared/definitions/framework-map.md
file.217.verdict=skipped
file.217.reason=non-code-file
file.218.path=shared/definitions/harness-triple-definitions.md
file.218.verdict=skipped
file.218.reason=non-code-file
file.219.path=shared/definitions/probe-definitions.md
file.219.verdict=skipped
file.219.reason=non-code-file
file.220.path=shared/guidelines/better-harness.md
file.220.verdict=skipped
file.220.reason=non-code-file
file.221.path=shared/guidelines/proactive-trigger.md
file.221.verdict=skipped
file.221.reason=non-code-file
file.222.path=shared/workflow/acceptance-hardening.md
file.222.verdict=skipped
file.222.reason=non-code-file
file.223.path=shared/workflow/evidence-step.md
file.223.verdict=skipped
file.223.reason=non-code-file
file.224.path=shared/workflow/expression-gates.md
file.224.verdict=skipped
file.224.reason=non-code-file
file.225.path=shared/workflow/feedback-step.md
file.225.verdict=skipped
file.225.reason=non-code-file
file.226.path=skills/external/sdd-loop-driver/SKILL.md
file.226.verdict=skipped
file.226.reason=non-code-file
file.227.path=skills/external/sdd-loop-driver/references/efficiency-model.md
file.227.verdict=skipped
file.227.reason=non-code-file
file.228.path=skills/external/sdd-loop-driver/references/state-awareness.md
file.228.verdict=skipped
file.228.reason=non-code-file
file.229.path=skills/external/sdd-loop-driver/scripts/loop-state.py
file.229.verdict=reviewed
file.230.path=skills/external/sdd-loop-driver/scripts/pre-analyze-check.py
file.230.verdict=reviewed
file.231.path=skills/internal/collect-evidence/SKILL.md
file.231.verdict=skipped
file.231.reason=non-code-file
file.232.path=skills/internal/collect-evidence/references/evidence-discipline.md
file.232.verdict=skipped
file.232.reason=non-code-file
file.233.path=skills/internal/manage-history/SKILL.md
file.233.verdict=skipped
file.233.reason=non-code-file
file.234.path=skills/internal/memory-recall/SKILL.md
file.234.verdict=skipped
file.234.reason=non-code-file
file.235.path=skills/internal/memory-record/SKILL.md
file.235.verdict=skipped
file.235.reason=non-code-file
file.236.path=skills/internal/review-sdd-process/SKILL.md
file.236.verdict=skipped
file.236.reason=non-code-file
file.237.path=templates/commands/history.md
file.237.verdict=skipped
file.237.reason=non-code-file
file.238.path=templates/commands/requirements.md
file.238.verdict=skipped
file.238.reason=non-code-file
file.239.path=templates/commands/review.md
file.239.verdict=skipped
file.239.reason=non-code-file
file.240.path=templates/review-template.md
file.240.verdict=skipped
file.240.reason=non-code-file
file.241.path=tests/contract/test_compile_embeds.py
file.241.verdict=skipped
file.241.reason=size-guard-focus-not-reviewed
file.242.path=tests/contract/test_expression_compatibility.py
file.242.verdict=skipped
file.242.reason=size-guard-focus-not-reviewed
file.243.path=tests/contract/test_harness_triple_structure.py
file.243.verdict=skipped
file.243.reason=size-guard-focus-not-reviewed
file.244.path=tests/contract/test_store_state_protocol.py
file.244.verdict=skipped
file.244.reason=size-guard-focus-not-reviewed
file.245.path=tests/fixtures/harness-triple-structure/dual-writer/branch-a/scripts/python/evidence-utils.py
file.245.verdict=skipped
file.245.reason=size-guard-focus-not-reviewed
file.246.path=tests/fixtures/harness-triple-structure/dual-writer/branch-a/shared/declarations/facts/evidence-seven-states.yaml
file.246.verdict=skipped
file.246.reason=size-guard-focus-not-reviewed
file.247.path=tests/fixtures/harness-triple-structure/dual-writer/branch-b/scripts/python/flow-class-check.py
file.247.verdict=skipped
file.247.reason=size-guard-focus-not-reviewed
file.248.path=tests/fixtures/harness-triple-structure/dual-writer/branch-b/shared/declarations/facts/flow-class-classes.yaml
file.248.verdict=skipped
file.248.reason=size-guard-focus-not-reviewed
file.249.path=tests/fixtures/harness-triple-structure/legacy-project/shared/workflow/feedback-step.md
file.249.verdict=skipped
file.249.reason=size-guard-focus-not-reviewed
file.250.path=tests/fixtures/harness-triple-structure/negative-declaration-absent/shared/declarations/facts/.gitkeep
file.250.verdict=skipped
file.250.reason=size-guard-focus-not-reviewed
file.251.path=tests/fixtures/harness-triple-structure/negative-declaration-absent/shared/workflow/feedback-step.md
file.251.verdict=skipped
file.251.reason=size-guard-focus-not-reviewed
file.252.path=tests/fixtures/harness-triple-structure/negative-declaration-outside-subset/scripts/python/feedback-utils.py
file.252.verdict=skipped
file.252.reason=size-guard-focus-not-reviewed
file.253.path=tests/fixtures/harness-triple-structure/negative-declaration-outside-subset/shared/declarations/facts/feedback-prompt-threshold.yaml
file.253.verdict=skipped
file.253.reason=size-guard-focus-not-reviewed
file.254.path=tests/fixtures/harness-triple-structure/negative-declaration-outside-subset/shared/workflow/feedback-step.md
file.254.verdict=skipped
file.254.reason=size-guard-focus-not-reviewed
file.255.path=tests/fixtures/harness-triple-structure/negative-duplicated-fact-literal/scripts/python/feedback-utils.py
file.255.verdict=skipped
file.255.reason=size-guard-focus-not-reviewed
file.256.path=tests/fixtures/harness-triple-structure/negative-duplicated-fact-literal/shared/declarations/facts/feedback-prompt-threshold-copy.yaml
file.256.verdict=skipped
file.256.reason=size-guard-focus-not-reviewed
file.257.path=tests/fixtures/harness-triple-structure/negative-duplicated-fact-literal/shared/declarations/facts/feedback-prompt-threshold.yaml
file.257.verdict=skipped
file.257.reason=size-guard-focus-not-reviewed
file.258.path=tests/fixtures/harness-triple-structure/negative-duplicated-fact-literal/shared/workflow/feedback-step.md
file.258.verdict=skipped
file.258.reason=size-guard-focus-not-reviewed
file.259.path=tests/fixtures/harness-triple-structure/negative-exclusion-anchor-unresolvable/shared/declarations/exclusions/no-machine-fact.yaml
file.259.verdict=skipped
file.259.reason=size-guard-focus-not-reviewed
file.260.path=tests/fixtures/harness-triple-structure/negative-exclusion-anchor-unresolvable/skills/internal/humanize/SKILL.md
file.260.verdict=skipped
file.260.reason=size-guard-focus-not-reviewed
file.261.path=tests/fixtures/harness-triple-structure/negative-exclusion-anchor-unresolvable/skills/internal/humanize/scripts/rewrite.py
file.261.verdict=skipped
file.261.reason=size-guard-focus-not-reviewed
file.262.path=tests/fixtures/harness-triple-structure/negative-third-layer-missing/scripts/python/feedback-utils.py
file.262.verdict=skipped
file.262.reason=size-guard-focus-not-reviewed
file.263.path=tests/fixtures/harness-triple-structure/negative-third-layer-missing/shared/declarations/facts/feedback-prompt-threshold.yaml
file.263.verdict=skipped
file.263.reason=size-guard-focus-not-reviewed
file.264.path=tests/fixtures/harness-triple-structure/negative-third-layer-missing/shared/workflow/feedback-step.md
file.264.verdict=skipped
file.264.reason=size-guard-focus-not-reviewed
file.265.path=tests/fixtures/harness-triple-structure/negative-unclassified-candidate/scripts/python/flow-class-check.py
file.265.verdict=skipped
file.265.reason=size-guard-focus-not-reviewed
file.266.path=tests/fixtures/harness-triple-structure/negative-unclassified-candidate/shared/declarations/facts/.gitkeep
file.266.verdict=skipped
file.266.reason=size-guard-focus-not-reviewed
file.267.path=tests/fixtures/harness-triple-structure/negative-unclassified-candidate/shared/workflow/gate-roster.md
file.267.verdict=skipped
file.267.reason=size-guard-focus-not-reviewed
file.268.path=tests/fixtures/harness-triple-structure/positive/scripts/python/feedback-utils.py
file.268.verdict=skipped
file.268.reason=size-guard-focus-not-reviewed
file.269.path=tests/fixtures/harness-triple-structure/positive/shared/declarations/exclusions/no-harness-asset.yaml
file.269.verdict=skipped
file.269.reason=size-guard-focus-not-reviewed
file.270.path=tests/fixtures/harness-triple-structure/positive/shared/declarations/facts/feedback-prompt-threshold.yaml
file.270.verdict=skipped
file.270.reason=size-guard-focus-not-reviewed
file.271.path=tests/fixtures/harness-triple-structure/positive/shared/workflow/feedback-step.md
file.271.verdict=skipped
file.271.reason=size-guard-focus-not-reviewed
file.272.path=tests/fixtures/harness-triple-structure/positive/skills/external/draw-diagram/SKILL.md
file.272.verdict=skipped
file.272.reason=size-guard-focus-not-reviewed
file.273.path=tests/fixtures/harness-triple-structure/positive/skills/external/draw-diagram/scripts/render_asset.py
file.273.verdict=skipped
file.273.reason=size-guard-focus-not-reviewed
file.274.path=tests/fixtures/harness-triple-structure/screen-boundary/shared/declarations/exclusions/no-machine-fact.yaml
file.274.verdict=skipped
file.274.reason=size-guard-focus-not-reviewed
file.275.path=tests/fixtures/harness-triple-structure/screen-boundary/skills/internal/summarize-project/SKILL.md
file.275.verdict=skipped
file.275.reason=size-guard-focus-not-reviewed
file.276.path=tests/fixtures/harness-triple-structure/screen-boundary/skills/internal/summarize-project/scripts/summarize.py
file.276.verdict=skipped
file.276.reason=size-guard-focus-not-reviewed
<!-- coverage-receipt:end -->
