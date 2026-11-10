# Code Review Report — 代码段 (code segment)

| 属性 | 值 |
|------|-----|
| **分支** | `095-superagent-role` |
| **基准** | `b3da3a26dfba209057f65c2b17962b9516812c39` (`b3da3a26d`) |
| **目标** | `2cf1e82ca513e3e265f781485e222834af3e9bbb` (`2cf1e82ca`) |
| **基准来源** | `feature-first-commit` |
| **渲染模式** | `renderer: text` |
| **Reviewer** | `Qiming Liu (John)` |
| **日期** | `2026-11-10T15:56:39Z` |

## 变更概览

```
 .specify/.gitignore                                |    4 +
 .specify/constitution.md                           |   16 +-
 .specify/features.md                               |    5 +-
 .specify/features/095-superagent-role.md           |   89 +
 .specify/glossary.md                               |    1 +
 .specify/instructions.md                           |    6 +
 .../20261110T065243Z-speckit-status/deviations.md  |   23 +
 .../20261110T065243Z-speckit-status/expectation.md |   55 +
 .../improvement-plan.md                            |   17 +
 .../20261110T065243Z-speckit-status/observation.md |   38 +
 .../records/20261110T060923194196Z-c9831663.json   |    1 +
 .../records/20261110T062049963005Z-0faa0f26.json   |    1 +
 .../records/20261110T064458279071Z-0eff0349.json   |    1 +
 .../records/20261110T065348449613Z-8451e579.json   |    1 +
 .../records/20261110T065627047158Z-76dd17eb.json   |    1 +
 .../records/20261110T070315544047Z-96c02c4f.json   |    1 +
 .../records/20261110T072029205343Z-96c5f7b3.json   |    1 +
 .../records/20261110T072037572826Z-4954ba31.json   |    1 +
 .../records/20261110T073148804873Z-a7b1966a.json   |    1 +
 .../records/20261110T073359116823Z-e43a701e.json   |    1 +
 .../records/20261110T073612212532Z-1c036aa8.json   |    1 +
 .../records/20261110T074701988907Z-f6b4edb9.json   |    1 +
 .../records/20261110T080443723487Z-d2dfa9c2.json   |    1 +
 .../records/20261110T080536949332Z-a3e82c5a.json   |    1 +
 .../records/20261110T080806145548Z-c33d7598.json   |    1 +
 .../records/20261110T081631561733Z-92d76c48.json   |    1 +
 .../records/20261110T123009978854Z-25394832.json   |    1 +
 .../records/20261110T124504821887Z-604fc7b3.json   |    1 +
 .../records/20261110T151913790212Z-31aa1b16.json   |    1 +
 .../records/20261110T151914121269Z-b8ad7403.json   |    1 +
 .../records/20261110T151914451830Z-cd1dedfb.json   |    1 +
 .../records/20261110T151914784483Z-43e68f87.json   |    1 +
 .../20261110T060933Z-speckit-requirements.md       |   22 +
 .../feedback/20261110T062057Z-speckit-clarify.md   |   22 +
 .../feedback/20261110T064500Z-speckit-plan.md      |   19 +
 .../feedback/20261110T065439Z-speckit-status.md    |   19 +
 .../20261110T065627Z-skill-coaching-skills.md      |   19 +
 .../feedback/20261110T070329Z-speckit-tasks.md     |   19 +
 .../feedback/20261110T072029Z-speckit-checklist.md |   23 +
 .../20261110T072037Z-skill-create-checklist.md     |   22 +
 .../feedback/20261110T073148Z-speckit-analyze.md   |   23 +
 .../feedback/20261110T073404Z-speckit-analyze.md   |   23 +
 .../feedback/20261110T073617Z-speckit-analyze.md   |   19 +
 .../feedback/20261110T074703Z-speckit-analyze.md   |   21 +
 .../feedback/20261110T080448Z-speckit-analyze.md   |   20 +
 .../feedback/20261110T080543Z-speckit-analyze.md   |   19 +
 .../feedback/20261110T080814Z-speckit-analyze.md   |   21 +
 .../feedback/20261110T081631Z-speckit-analyze.md   |   20 +
 .../feedback/20261110T123022Z-speckit-analyze.md   |   21 +
 .../feedback/20261110T124514Z-speckit-analyze.md   |   19 +
 .../feedback/20261110T151928Z-speckit-review.md    |   23 +
 .../20261110T151929Z-skill-review-sdd-process.md   |   23 +
 ...0261110T151935Z-skill-review-feature-quality.md |   23 +
 .../feedback/20261110T151937Z-skill-code-review.md |   23 +
 .../20261110T061120Z-r20261110T055657Z-b095.json   |   23 +
 .../20261110T062134Z-r20261110T055657Z-b095.json   |   23 +
 .../20261110T064605Z-r20261110T064443Z-b095.json   |   23 +
 .../20261110T070413Z-r20261110T065604Z-b095.json   |   23 +
 .../20261110T072115Z-r20261110T072013Z-b095.json   |   38 +
 .../20261110T074757Z-r20261110T055657Z-b095.json   |   68 +
 ...110T081653Z-r20261110T055657Z-b095-r2merge.json |   68 +
 ...20261110T123105Z-r20261110T055657Z-b095-r3.json |   23 +
 ...20261110T124538Z-r20261110T055657Z-b095-r4.json |   23 +
 ...1110T152047Z-r20261110T055657Z-b095-review.json |   68 +
 ...ination-speckit-tasks-r20261109t064500z-092a.md |   10 +-
 ...run-determination-speckit-tasks-093-tasks-a1.md |   10 +-
 ...n-speckit-requirements-r20261110t055657z-b09.md |  202 +
 ...ation-speckit-clarify-r20261110t055657z-b095.md |  200 +
 ...mination-speckit-plan-r20261110t064443z-b095.md |  202 +
 ...ination-speckit-tasks-r20261110t065604z-b095.md |  202 +
 ...ion-speckit-checklist-r20261110t072013z-b095.md |  220 +
 ...n-skill-create-checklist-r20261110t072013z-b.md |  220 +
 ...on-speckit-analyze-r20261110t055657z-b095-w1.md |  213 +
 ...ation-speckit-analyze-r20261110t073257z-b095.md |  208 +
 ...ation-speckit-analyze-r20261110t055657z-b095.md |  202 +
 ...n-speckit-analyze-r20261110t055657z-b095-mer.md |  213 +
 ...n-speckit-analyze-r20261110t080102z-b095-r2w.md |  202 +
 ...n-speckit-analyze-r20261110t055657z-b095-r2w.md |  202 +
 ...n-speckit-analyze-r20261110t055657z-b095-r2w.md |  202 +
 ...n-speckit-analyze-r20261110t055657z-b095-r2m.md |  200 +
 ...on-speckit-analyze-r20261110t055657z-b095-r3.md |  202 +
 ...on-speckit-analyze-r20261110t055657z-b095-r4.md |  202 +
 ...n-skill-code-review-r20261110t055657z-b095-r.md |  213 +
 ...n-skill-review-feature-quality-r20261110t055.md |  213 +
 ...n-skill-review-sdd-process-r20261110t055657z.md |  213 +
 ...n-speckit-review-r20261110t055657z-b095-revi.md |  213 +
 ...rview-blocked-stalled-lines-2026-11-10.dag.json |  128 +
 .../interview-blocked-stalled-lines-2026-11-10.md  |   20 +
 .specify/register.md                               |    9 +
 .specify/scripts/bash/run-tests-shards.sh          |    8 +-
 .specify/scripts/python/role-edge-check.py         | 1005 +++
 .specify/scripts/python/scan-temp-usage.py         |   12 +-
 .specify/scripts/python/status-digest.py           |  768 +-
 .specify/shared/definitions/agent-definitions.md   |    1 +
 .specify/shared/definitions/framework-map.md       |    1 +
 .../shared/definitions/subagent-definitions.md     |    2 +
 .../shared/definitions/superagent-definitions.md   |  124 +
 .specify/shared/guidelines/better-harness.md       |    4 +-
 .specify/shared/guidelines/confirmation-gates.md   |    6 +
 .../code-review/scripts/git-delta-review.sh        |   14 +-
 .specify/skills/internal/create-team/SKILL.md      |    2 +
 .../internal/create-team/references/patterns.md    |    1 +
 .specify/skills/internal/run-agent/SKILL.md        |   10 +
 .specify/skills/sdd-loop-driver/SKILL.md           |    1 +
 .../sdd-loop-driver/references/dispatch-recipes.md |    2 +-
 .../sdd-loop-driver/references/stage-prompts.md    |    2 +-
 .../checklists/requirements-quality-2026-11-10.md  |   83 +
 .../095-superagent-role/checklists/requirements.md |   55 +
 .specify/specs/095-superagent-role/code-review.md  | 1377 ++++
 .../contracts/harness-landing.contract.md          |   59 +
 .../contracts/role-edge-engine.contract.md         |   82 +
 .../contracts/role-transition-payload.contract.md  |   67 +
 .../contracts/status-digest-role-view.contract.md  |   47 +
 .../095-superagent-role/coverage-baseline.txt      |  642 ++
 .specify/specs/095-superagent-role/data-model.md   |  115 +
 .specify/specs/095-superagent-role/feature-ref.md  |   21 +
 .../notes/baseline-failed-names.txt                |  303 +
 .../notes/baseline-provenance.md                   |   48 +
 .../coverage-baseline-2026-11-10-tasks-frozen.txt  |  642 ++
 .../notes/pre-change-measurements.md               |  139 +
 .../095-superagent-role/notes/quickstart-run.md    |  138 +
 .../notes/red-first-evidence.md                    |  329 +
 .../095-superagent-role/observation-appendix.md    |   30 +
 .specify/specs/095-superagent-role/plan.md         |  247 +
 .specify/specs/095-superagent-role/quickstart.md   |   57 +
 .specify/specs/095-superagent-role/requirements.md |  287 +
 .specify/specs/095-superagent-role/review.md       |  404 +
 .specify/specs/095-superagent-role/tasks.md        |  341 +
 .../test-evidence/analyze-findings-W1.md           |  135 +
 .../test-evidence/analyze-findings-W2.md           |   82 +
 .../test-evidence/analyze-findings-W3.md           |   67 +
 .../test-evidence/analyze-findings-round2-W1.md    |  212 +
 .../test-evidence/analyze-findings-round2-W2.md    |  139 +
 .../test-evidence/analyze-findings-round2-W3.md    |   96 +
 .../test-evidence/analyze-merged-2026-11-10.md     |  315 +
 .../test-evidence/analyze-merged-r3-2026-11-10.md  |  254 +
 .../test-evidence/analyze-merged-r4-2026-11-10.md  |  245 +
 .../analyze-merged-round2-2026-11-10.md            |  258 +
 .../analyze-repair-dispositions-2026-11-10.md      |   64 +
 .../analyze-repair-dispositions-r3-2026-11-10.md   |   49 +
 .../analyze-repair-dispositions-r4-2026-11-10.md   |   66 +
 .../analyze-repair-gates-2026-11-10.txt            |   30 +
 .../analyze-repair-gates-r3-2026-11-10.txt         |   33 +
 .../analyze-repair-gates-r4-2026-11-10.txt         |   75 +
 .../test-evidence/analyze-wrapup-exec-quant.txt    |    1 +
 .../test-evidence/analyze-wrapup-feedback.txt      |    9 +
 .../analyze-wrapup-run-determination.txt           |    8 +
 .../checklist-readings-2026-11-10.txt              |  214 +
 .../checklist-wrapup-exec-quant-skill.txt          |    1 +
 .../test-evidence/checklist-wrapup-exec-quant.txt  |    1 +
 .../checklist-wrapup-feedback-skill.txt            |    9 +
 .../test-evidence/checklist-wrapup-feedback.txt    |    9 +
 .../checklist-wrapup-run-determination-skill.txt   |   10 +
 .../checklist-wrapup-run-determination.txt         |   10 +
 .../test-evidence/clarify-flow-class.txt           |    7 +
 .../test-evidence/clarify-overlap-check.json       |   10 +
 .../test-evidence/clarify-overlap-check.txt        |    2 +
 .../clarify-validate-requirements.txt              |   10 +
 .../test-evidence/clarify-wrapup-exec-quant.txt    |    1 +
 .../test-evidence/clarify-wrapup-feedback.txt      |    9 +
 .../clarify-wrapup-run-determination.txt           |    8 +
 .../test-evidence/closure-acceptance.txt           |   90 +
 .../test-evidence/closure-suite-comparison.txt     |   34 +
 .../test-evidence/closure-suite-names.txt          |  233 +
 .../test-evidence/closure-suite.txt                | 8368 ++++++++++++++++++++
 .../test-evidence/concurrency-invariants.txt       |   59 +
 .../test-evidence/concurrency-wave-readings.txt    |   48 +
 .../test-evidence/definitions-readings.txt         |  104 +
 .../test-evidence/gate-checks.txt                  |   47 +
 .../test-evidence/instructions-budget.txt          |   93 +
 .../test-evidence/mirror-obligations.txt           |   94 +
 .../test-evidence/observation-appendix-check.txt   |  109 +
 .../test-evidence/plan-gate.txt                    |    4 +
 .../test-evidence/plan-stage-evidence.md           |   65 +
 .../test-evidence/plan-wrapup-exec-quant.txt       |    1 +
 .../test-evidence/plan-wrapup-feedback.txt         |    9 +
 .../plan-wrapup-run-determination.txt              |    8 +
 .../test-evidence/requirements-flow-class.txt      |    7 +
 .../test-evidence/requirements-glossary-add.txt    |    5 +
 .../requirements-glossary-conflict.txt             |    5 +
 .../requirements-validator-initial.txt             |   13 +
 .../test-evidence/requirements-validator.txt       |   10 +
 .../review-repair-baseline-module-health.txt       |  700 ++
 .../review-repair-closure-acceptance.txt           |   43 +
 .../review-repair-closure-suite-comparison.txt     |   65 +
 .../review-repair-closure-suite-names.txt          |  215 +
 .../test-evidence/review-repair-closure-suite.txt  | 7692 ++++++++++++++++++
 .../review-repair-dispositions-r1-2026-11-10.md    |   37 +
 .../test-evidence/review-repair-guards.txt         |    8 +
 .../review-repair-mutation-drills.txt              |  114 +
 .../test-evidence/review-repair-suite.txt          |    7 +
 .../test-evidence/role-edge-engine-readings.txt    |  283 +
 .../test-evidence/role-transition-readings.txt     |  144 +
 .../test-evidence/smoke-six-modules.txt            |    9 +
 .../test-evidence/state-sync-recovery.txt          |   79 +
 .../test-evidence/status-digest-roles-readings.txt |  141 +
 .../test-evidence/tasks-decomposition-check.txt    |    4 +
 .../test-evidence/tasks-flow-class.txt             |    7 +
 .../test-evidence/tasks-pre-analyze-check.txt      |    5 +
 .../test-evidence/tasks-stage-evidence.md          |   48 +
 .../test-evidence/tasks-validate.txt               |    1 +
 .../test-evidence/tasks-wrapup-exec-quant.txt      |    1 +
 .../test-evidence/tasks-wrapup-feedback.txt        |    9 +
 .../tasks-wrapup-run-determination.txt             |    9 +
 .../test-evidence/three-forms-readings.txt         |   99 +
 .../test-evidence/validate-tasks.txt               |    7 +
 .../test-evidence/wrapup-exec-quant.txt            |    1 +
 .../test-evidence/wrapup-feedback.txt              |    9 +
 .../test-evidence/wrapup-run-determination.txt     |  206 +
 .../zero-mechanism-baseline-names.txt              |    1 +
 .../test-evidence/zero-mechanism-current-names.txt |    1 +
 .../test-evidence/zero-mechanism-readings.txt      |   84 +
 .specify/specs/095-superagent-role/verification.md |  135 +
 .specify/state/074-goal-team-sdd-unification.md    |  172 -
 .specify/state/074b-nested-governance.md           |   89 -
 .specify/state/076-decision-tension-contract.md    |  257 -
 .specify/state/077-doc-sdd-integration.md          |  214 -
 .specify/state/078-bilingual-expression.md         |  382 -
 .specify/state/078-coaching-skills.md              |  136 -
 .specify/state/079-humanize-run-output.md          |  121 -
 .specify/state/081-acceptance-hardening.md         |  453 --
 .specify/state/082-self-explanatory-integration.md |  739 --
 .specify/state/083-budget-calibration-tests.txt    |    6 -
 .specify/state/083-budget-calibration.md           |   88 -
 .specify/state/083-loop-state-self-test.txt        |   37 -
 .specify/state/083-mechanism-policy-separation.md  |  409 -
 .specify/state/084-harness-triple-structure.md     |  336 -
 .specify/state/086-efficient-test-execution.md     |  288 -
 .specify/state/087-arch-diagram-docs.md            |  126 -
 .specify/state/088-speckit-visualization.md        |  835 --
 .specify/state/089-script-interface-contract.md    |  124 -
 .specify/state/090-re-anchoring.md                 |   57 -
 .specify/state/091-auto-git-closeout.md            |  218 -
 .specify/state/092-non-disposable.md               |   69 -
 .specify/state/093-concurrency-by-default.md       |  119 -
 .specify/state/094-goal-team-parallel.md           |   70 -
 .specify/state/eval-baseline/README.md             |   99 -
 .specify/state/eval-baseline/instructions.md       |  140 -
 .specify/state/speckit-docs-expression.md          |   68 -
 ...eckit-visualization-implement-a1-gate-plan.json |    1 -
 ...eckit-visualization-implement-a2-gate-plan.json |    1 -
 ...88-speckit-visualization-plan-a1-gate-plan.json |    1 -
 ...88-speckit-visualization-plan-a2-gate-plan.json |    1 -
 .specify/templates/instructions-template.md        |    6 +
 scripts/bash/run-tests-shards.sh                   |    8 +-
 scripts/python/role-edge-check.py                  | 1005 +++
 scripts/python/scan-temp-usage.py                  |   12 +-
 scripts/python/status-digest.py                    |  768 +-
 shared/definitions/agent-definitions.md            |    1 +
 shared/definitions/framework-map.md                |    1 +
 shared/definitions/subagent-definitions.md         |    2 +
 shared/definitions/superagent-definitions.md       |  124 +
 shared/guidelines/better-harness.md                |    4 +-
 shared/guidelines/confirmation-gates.md            |    6 +
 skills/external/sdd-loop-driver/SKILL.md           |    1 +
 .../sdd-loop-driver/references/dispatch-recipes.md |    2 +-
 .../sdd-loop-driver/references/stage-prompts.md    |    2 +-
 .../code-review/scripts/git-delta-review.sh        |   14 +-
 skills/internal/create-team/SKILL.md               |    2 +
 skills/internal/create-team/references/patterns.md |    1 +
 skills/internal/run-agent/SKILL.md                 |   10 +
 templates/gitignore-specify-template               |    4 +
 templates/instructions-template.md                 |    6 +
 tests/contract/test_code_review_skill_contract.py  |   28 +-
 tests/contract/test_efficiency_element.py          |   33 +-
 tests/contract/test_fast_fail_discipline.py        |   25 +-
 .../test_instructions_budget_superagent_section.py |  175 +
 tests/contract/test_role_edge_engine.py            |  774 ++
 tests/contract/test_role_transition_payload.py     |  377 +
 tests/contract/test_specify_gitignore_template.py  |    2 +
 tests/contract/test_status_digest.py               |  102 +-
 tests/contract/test_status_digest_roles.py         |  604 ++
 tests/contract/test_superagent_definitions.py      |  222 +
 tests/contract/test_superagent_zero_mechanism.py   |  370 +
 .../superagent-role/conflict/logs/.gitkeep         |    0
 .../superagent-role/conflict/registry/.gitkeep     |    0
 .../superagent-role/conflict/state/.gitkeep        |    0
 .../conflict-team/runs/20261110T000000Z-report.md  |   11 +
 .../conflict-team/runs/20261110T010000Z-report.md  |   11 +
 tests/fixtures/superagent-role/empty/logs/.gitkeep |    0
 .../superagent-role/empty/registry/.gitkeep        |    0
 .../fixtures/superagent-role/empty/state/.gitkeep  |    0
 .../fixtures/superagent-role/empty/teams/.gitkeep  |    0
 .../superagent-role/fanout-10/logs/.gitkeep        |    0
 .../superagent-role/fanout-10/registry/.gitkeep    |    0
 .../superagent-role/fanout-10/state/.gitkeep       |    0
 .../fanout-team/runs/20261110T000000Z-report.md    |   22 +
 .../superagent-role/interrupted/logs/child-1.jsonl |    1 +
 .../interrupted/logs/child-1.status                |    1 +
 .../interrupted/registry/demo-line.json            |   14 +
 .../superagent-role/interrupted/state/demo-line.md |   14 +
 .../runs/20261110T000000Z-report.md                |   12 +
 .../superagent-role/local-team/logs/alice.jsonl    |    1 +
 .../superagent-role/local-team/logs/alice.status   |    1 +
 .../superagent-role/local-team/logs/bob.jsonl      |    1 +
 .../superagent-role/local-team/logs/bob.status     |    1 +
 .../superagent-role/local-team/logs/carol.jsonl    |    1 +
 .../superagent-role/local-team/logs/carol.status   |    1 +
 .../superagent-role/local-team/registry/.gitkeep   |    0
 .../superagent-role/local-team/state/.gitkeep      |    0
 .../local-team/runs/20261110T000000Z-report.md     |   13 +
 .../superagent-role/malformed/logs/.gitkeep        |    0
 .../superagent-role/malformed/registry/.gitkeep    |    0
 .../superagent-role/malformed/state/.gitkeep       |    0
 .../malformed-team/runs/20261110T000000Z-report.md |   11 +
 .../superagent-role/payload/role-fields.md         |   15 +
 .../payload/role-transition-complete.md            |   18 +
 .../payload/role-transition-missing-item.md        |   16 +
 .../payload/role-transition-skill-load.md          |   22 +
 .../logs/remote--20261110T000000Z--worker.jsonl    |    1 +
 .../logs/remote--20261110T000000Z--worker.status   |    1 +
 .../records/20261110T000000000000Z-fixture01.json  |   10 +
 .../remote-topology/registry/remote-builder.json   |    6 +
 .../superagent-role/remote-topology/state/.gitkeep |    0
 .../superagent-role/remote-topology/teams/.gitkeep |    0
 .../fixtures/superagent-role/root-a-b/logs/A.jsonl |    1 +
 .../superagent-role/root-a-b/logs/A.status         |    1 +
 .../fixtures/superagent-role/root-a-b/logs/B.jsonl |    1 +
 .../superagent-role/root-a-b/logs/B.status         |    1 +
 .../root-a-b/registry/demo-line.json               |    6 +
 .../superagent-role/root-a-b/state/demo-line.md    |   12 +
 .../root-a-b/state/prompt-B-s1.md.meta.json        |   13 +
 .../demo-team/runs/20261110T000000Z-report.md      |   11 +
 .../violations/dangling-parent/logs/.gitkeep       |    0
 .../violations/dangling-parent/registry/.gitkeep   |    0
 .../violations/dangling-parent/state/.gitkeep      |    0
 .../violations/dangling-parent/teams/.gitkeep      |    0
 .../dangling-team/runs/20261110T000000Z-report.md  |   11 +
 .../violations/depth-cycle/logs/.gitkeep           |    0
 .../violations/depth-cycle/registry/.gitkeep       |    0
 .../violations/depth-cycle/state/.gitkeep          |    0
 .../violations/depth-cycle/teams/.gitkeep          |    0
 .../cycle-team/runs/20261110T000000Z-report.md     |   13 +
 .../violations/self-dispatch/logs/.gitkeep         |    0
 .../violations/self-dispatch/registry/.gitkeep     |    0
 .../violations/self-dispatch/state/.gitkeep        |    0
 .../violations/self-dispatch/teams/.gitkeep        |    0
 .../self-team/runs/20261110T000000Z-report.md      |   11 +
 .../violations/unbacked-claim/logs/.gitkeep        |    0
 .../violations/unbacked-claim/registry/.gitkeep    |    0
 .../violations/unbacked-claim/state/.gitkeep       |    0
 .../violations/unbacked-claim/teams/.gitkeep       |    0
 .../claim-team/runs/20261110T000000Z-report.md     |   12 +
 tests/unit/test_status_digest_unit.py              |  185 +-
 344 files changed, 39570 insertions(+), 6185 deletions(-)
```

---

## Review 意见


### 🟠 [IMPORTANT] tests/unit/test_status_digest_unit.py (Line 657)

> Round-2 NEW finding (introduced by the r1 repair commit 2cf1e82ca): the C-43 determinism guard was rewritten from table-line comparison to full-JSON comparison and pops only generated_at. The JSON carries second-resolution age_seconds derived from the render clock, so two digest runs that straddle a one-second boundary differ and the guard goes red on a healthy tree. Measured by this review: 1 failure in 8 isolated runs (age_seconds 395291 vs 395292; test-evidence/review-r2-guards.txt); the repair single 41-passed reading could not see it. Answer: agreed, a real defect introduced by the repair — fix by popping age/age_seconds (or freezing the clock) in the comparison; it does not block because the product behaviour is correct and only the determinism claim is false.

<sub>23:56:48</sub>


### 🟠 [IMPORTANT] scripts/python/status-digest.py (Line 967)

> Carried from round 1 (still present at HEAD): merge_role_entries seeds activity[row-id] for every extra from row[state], and the synthetic root executor is an extra whose state is running (no artifacts), so a stale child under parent root can never be marked interrupted. The only fixture is line-rooted (stalled spine), so the gap is unmeasured. Answer: agreed, remains open — not repaired in r1 because it was outside the blocking scope. Fix: seed the root activity from an artifact-derived reading instead of state-by-absence before the interrupted pass.

<sub>23:56:48</sub>


### 🟠 [IMPORTANT] scripts/python/status-digest.py (Line 900)

> Carried: an executor with no artifact set at all is reported running forever (no exit record => running) and is never stale, so it sorts first and can never become interrupted; the fanout-10 fixture therefore renders 12 permanently running rows for a finished team run (test_status_digest_roles.py asserts only the row count). Answer: agreed, remains open. Fix: distinguish no artifacts at all from no exit record yet in the reader contract, or pin the fixture expectation.

<sub>23:56:48</sub>


### 🟠 [IMPORTANT] tests/contract/test_fast_fail_discipline.py (Line 61)

> Carried: CONST_LIVE points at .specify/memory/constitution.md, which does not exist in this repo (the live file is .specify/constitution.md), so test_x4/test_x5 (and x6/x7) fail with FileNotFoundError and the in-range constitution amendment dd7cbbab4 raises the pin to 1.19.1 without a readable guard. Answer: agreed, remains open — the amendment own templates-requiring-updates claim has no reading; fix the path so the pin is actually checked.

<sub>23:56:48</sub>


### 🟠 [IMPORTANT] shared/definitions/superagent-definitions.md (Line 74)

> Carried: the owner page attributes the extended pre-dispatch self-check to shared/guidelines/fast-fail.md § 派发前自检, but that file is untouched in the range and still judges only the fast-fail clause identifier; the extension lives only in skills/internal/run-agent/SKILL.md. Answer: agreed, remains open. Fix: correct the attribution to the run-agent surface, or extend the file the page names.

<sub>23:56:48</sub>


### 🟠 [IMPORTANT] tests/contract/test_superagent_zero_mechanism.py (Line 367)

> Carried: the C-3.6 seeded mutation appends a copied rule literal to the section text and then asserts the seeded string contains it; the detection path (the FORBIDDEN_RULE_LITERALS scan over section/owner) is never run on the seed, so the leg cannot go red for its subject. Answer: agreed, remains open. Fix: run the scan function against the seeded text and assert it reports the hit.

<sub>23:56:48</sub>


### 🟢 [SUGGESTION] tests/contract/test_role_transition_payload.py (Line 171)

> Carried: the delete-one -> blocks drill re-implements the self-check locally (_self_check) and runs it on a pre-mutated fixture; no wired surface or real check is exercised, so the leg stays green if run-agent loses the requirement. The pin is a model of the substring form, not the form carrier.

<sub>23:56:54</sub>


### 🟢 [SUGGESTION] tests/contract/test_role_edge_engine.py (Line 505)

> Carried: the conflict fixture places the disagreeing rows in two team reports with different run stamps (20261110T000000Z vs 20261110T010000Z) — the retry shape data-model §2 forbids for one label — not two different carrier families for the same recorded edge; team rows carry no attempt, so the pinned attempt 1 is the engine default rather than a recorded identity.

<sub>23:56:54</sub>


### 🟢 [SUGGESTION] tests/contract/test_role_edge_engine.py (Line 515)

> Carried: the C-2 error-names-the-offending-field assertion is a tautology: assert role in proc.stderr passes on the program name in every error prefix (role-edge-check.py: error: ...), so an error that never names the field stays green.

<sub>23:56:54</sub>


### 🟢 [SUGGESTION] .specify/.gitignore (Line 34)

> Carried: other-line commit 57d364074 adds state/ to .specify/.gitignore and de-indexes 30+ tracked state files, including .specify/state/074-goal-team-sdd-unification.md whose D-074 rulings 6d13938aa had written 11 minutes earlier. The rulings survive in the tracked interview ledger; the 095 state spine and other run ledgers are now disk-only. Reviewed as a declared runtime reclassification, not a defect; flagged for the non-disposable review obligation (shared/definitions/non-disposable-definitions.md).

<sub>23:56:54</sub>


### 🟢 [SUGGESTION] .specify/specs/095-superagent-role/test-evidence/observation-appendix-check.txt

> Carried: the FR-038/SC-010 mechanical check is an ad-hoc script kept at .specify/.tmp/095-appendix-check.py and reproduced only inside this evidence file; nothing guards it from rot, unlike the feature other claims which have contract modules, and the mutation drill recorded command shows an AssertionError traceback before the mutated-copy reading, which a reader can misread.

<sub>23:56:54</sub>


### 👍 [PRAISE] scripts/python/status-digest.py (Line 1420)

> Round-2 verification of the r1 blocking subjects: both are resolved at HEAD. last_completion is back in the only reachable renderer, render_digest was deleted, the C-68 explicit store=no measurements line is restored with a strengthened single-line guard, and the C-1 clause now derives the legacy rows from one registry read with a behavioural audit-hook guard (one root scan, one open per entry; the seeded second read turns it red). Measured at review: the two repaired modules read 40 of 41 green in this reviewer run — the one red is the new clock-sensitive C-43 guard noted above, not a product regression — plus 144 further contract tests green.

<sub>23:56:54</sub>


> **未提交范围（未评审）**: 53 个未提交路径未计入本次评审对象（.claude/agents/reporter.md, .claude/agents/sdd-implement-coordinator.md, .claude/agents/sdd-implement-executor.md, .github/agents/reporter.agent.md, .github/agents/sdd-implement-coordinator.agent.md, .github/agents/sdd-implement-executor.agent.md, .opencode/agents/reporter.md, .opencode/agents/sdd-implement-coordinator.md, .opencode/agents/sdd-implement-executor.md, .qoder/agents/reporter.agent.md, .qoder/agents/sdd-implement-coordinator.agent.md, .qoder/agents/sdd-implement-executor.agent.md, .specify/agents/.render-manifest.json, .specify/memory/session/20261109T084106Z-run-determination-speckit-checklist-093-checklist-a1.md, .specify/memory/session/20261109T084110Z-run-determination-skill-create-checklist-093-checklist-skill.md, .specify/memory/session/interview-blocked-stalled-lines-2026-11-10.dag.json, .specify/memory/session/interview-blocked-stalled-lines-2026-11-10.md, .specify/memory/todo/20261030-suite-speed-optimizations.md, .specify/memory/trigger/index.json, .specify/scripts/bash/check-prerequisites.sh, .specify/scripts/bash/generate-instructions.sh, .specify/scripts/bash/run-tests.sh, .specify/scripts/python/git-workflow-observe.py, .specify/scripts/python/script-interface-check.py, .specify/scripts/python/script_interface_cli.py, .specify/scripts/python/sync-mirrors.py, .specify/source.json, .specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt, .specify/specs/095-superagent-role/review.md, .specify/templates/gitignore-specify-template, .specify/workflow/git.md, .specify/memory/exec-quant/records/20261110T024300521548Z-bd97a17c.json, .specify/memory/exec-quant/records/20261110T083604281128Z-1427346f.json, .specify/memory/exec-quant/records/20261110T104159254077Z-6add98fe.json, .specify/memory/exec-quant/records/20261110T121646540994Z-e130beb4.json, .specify/memory/exec-quant/records/20261110T135434742719Z-b232a3d0.json, .specify/memory/feedback/20261110T024300Z-speckit-status.md, .specify/memory/feedback/20261110T083604Z-speckit-status.md, .specify/memory/feedback/20261110T104158Z-skill-sdd-loop-driver.md, .specify/memory/feedback/20261110T121646Z-speckit-status.md, .specify/memory/feedback/20261110T135434Z-speckit-status.md, .specify/memory/session/20261110T104203Z-run-determination-skill-sdd-loop-driver-20261110t092500z-sdd.md, .specify/memory/todo/20261110-sdd-observer-agent.md, .specify/memory/todo/20261110-speckit-migrate-command.md, .specify/specs/095-superagent-role/checkpoints/, .specify/specs/095-superagent-role/code-review-r1.md, .specify/specs/095-superagent-role/review-r1.md, .specify/specs/095-superagent-role/test-evidence/review-r2-closure-acceptance.err, .specify/specs/095-superagent-role/test-evidence/review-r2-closure-acceptance.json, .specify/specs/095-superagent-role/test-evidence/review-r2-closure-suite-names.txt, .specify/specs/095-superagent-role/test-evidence/review-r2-closure-suite.txt, .specify/specs/095-superagent-role/test-evidence/review-r2-guards.txt, .specify/specs/095-superagent-role/test-evidence/review-r2-smoke.txt）；本回执不对该范围给出任何结论。

<!-- coverage-receipt:begin -->
receipt_version=1
base=b3da3a26dfba209057f65c2b17962b9516812c39
head=2cf1e82ca513e3e265f781485e222834af3e9bbb
base_source=feature-first-commit
renderer=text
changed_files=344
judged_files=17
skipped_files=327
gap_files=0
lines_added=39570
lines_deleted=6185
file.001.path=.specify/.gitignore
file.001.verdict=skipped
file.001.reason=non-code-file
file.002.path=.specify/constitution.md
file.002.verdict=skipped
file.002.reason=non-code-file
file.003.path=.specify/features.md
file.003.verdict=skipped
file.003.reason=non-code-file
file.004.path=.specify/features/095-superagent-role.md
file.004.verdict=skipped
file.004.reason=non-code-file
file.005.path=.specify/glossary.md
file.005.verdict=skipped
file.005.reason=non-code-file
file.006.path=.specify/instructions.md
file.006.verdict=skipped
file.006.reason=generated
file.007.path=.specify/memory/coaching/20261110T065243Z-speckit-status/deviations.md
file.007.verdict=skipped
file.007.reason=generated
file.008.path=.specify/memory/coaching/20261110T065243Z-speckit-status/expectation.md
file.008.verdict=skipped
file.008.reason=generated
file.009.path=.specify/memory/coaching/20261110T065243Z-speckit-status/improvement-plan.md
file.009.verdict=skipped
file.009.reason=generated
file.010.path=.specify/memory/coaching/20261110T065243Z-speckit-status/observation.md
file.010.verdict=skipped
file.010.reason=generated
file.011.path=.specify/memory/exec-quant/records/20261110T060923194196Z-c9831663.json
file.011.verdict=skipped
file.011.reason=generated
file.012.path=.specify/memory/exec-quant/records/20261110T062049963005Z-0faa0f26.json
file.012.verdict=skipped
file.012.reason=generated
file.013.path=.specify/memory/exec-quant/records/20261110T064458279071Z-0eff0349.json
file.013.verdict=skipped
file.013.reason=generated
file.014.path=.specify/memory/exec-quant/records/20261110T065348449613Z-8451e579.json
file.014.verdict=skipped
file.014.reason=generated
file.015.path=.specify/memory/exec-quant/records/20261110T065627047158Z-76dd17eb.json
file.015.verdict=skipped
file.015.reason=generated
file.016.path=.specify/memory/exec-quant/records/20261110T070315544047Z-96c02c4f.json
file.016.verdict=skipped
file.016.reason=generated
file.017.path=.specify/memory/exec-quant/records/20261110T072029205343Z-96c5f7b3.json
file.017.verdict=skipped
file.017.reason=generated
file.018.path=.specify/memory/exec-quant/records/20261110T072037572826Z-4954ba31.json
file.018.verdict=skipped
file.018.reason=generated
file.019.path=.specify/memory/exec-quant/records/20261110T073148804873Z-a7b1966a.json
file.019.verdict=skipped
file.019.reason=generated
file.020.path=.specify/memory/exec-quant/records/20261110T073359116823Z-e43a701e.json
file.020.verdict=skipped
file.020.reason=generated
file.021.path=.specify/memory/exec-quant/records/20261110T073612212532Z-1c036aa8.json
file.021.verdict=skipped
file.021.reason=generated
file.022.path=.specify/memory/exec-quant/records/20261110T074701988907Z-f6b4edb9.json
file.022.verdict=skipped
file.022.reason=generated
file.023.path=.specify/memory/exec-quant/records/20261110T080443723487Z-d2dfa9c2.json
file.023.verdict=skipped
file.023.reason=generated
file.024.path=.specify/memory/exec-quant/records/20261110T080536949332Z-a3e82c5a.json
file.024.verdict=skipped
file.024.reason=generated
file.025.path=.specify/memory/exec-quant/records/20261110T080806145548Z-c33d7598.json
file.025.verdict=skipped
file.025.reason=generated
file.026.path=.specify/memory/exec-quant/records/20261110T081631561733Z-92d76c48.json
file.026.verdict=skipped
file.026.reason=generated
file.027.path=.specify/memory/exec-quant/records/20261110T123009978854Z-25394832.json
file.027.verdict=skipped
file.027.reason=generated
file.028.path=.specify/memory/exec-quant/records/20261110T124504821887Z-604fc7b3.json
file.028.verdict=skipped
file.028.reason=generated
file.029.path=.specify/memory/exec-quant/records/20261110T151913790212Z-31aa1b16.json
file.029.verdict=skipped
file.029.reason=generated
file.030.path=.specify/memory/exec-quant/records/20261110T151914121269Z-b8ad7403.json
file.030.verdict=skipped
file.030.reason=generated
file.031.path=.specify/memory/exec-quant/records/20261110T151914451830Z-cd1dedfb.json
file.031.verdict=skipped
file.031.reason=generated
file.032.path=.specify/memory/exec-quant/records/20261110T151914784483Z-43e68f87.json
file.032.verdict=skipped
file.032.reason=generated
file.033.path=.specify/memory/feedback/20261110T060933Z-speckit-requirements.md
file.033.verdict=skipped
file.033.reason=generated
file.034.path=.specify/memory/feedback/20261110T062057Z-speckit-clarify.md
file.034.verdict=skipped
file.034.reason=generated
file.035.path=.specify/memory/feedback/20261110T064500Z-speckit-plan.md
file.035.verdict=skipped
file.035.reason=generated
file.036.path=.specify/memory/feedback/20261110T065439Z-speckit-status.md
file.036.verdict=skipped
file.036.reason=generated
file.037.path=.specify/memory/feedback/20261110T065627Z-skill-coaching-skills.md
file.037.verdict=skipped
file.037.reason=generated
file.038.path=.specify/memory/feedback/20261110T070329Z-speckit-tasks.md
file.038.verdict=skipped
file.038.reason=generated
file.039.path=.specify/memory/feedback/20261110T072029Z-speckit-checklist.md
file.039.verdict=skipped
file.039.reason=generated
file.040.path=.specify/memory/feedback/20261110T072037Z-skill-create-checklist.md
file.040.verdict=skipped
file.040.reason=generated
file.041.path=.specify/memory/feedback/20261110T073148Z-speckit-analyze.md
file.041.verdict=skipped
file.041.reason=generated
file.042.path=.specify/memory/feedback/20261110T073404Z-speckit-analyze.md
file.042.verdict=skipped
file.042.reason=generated
file.043.path=.specify/memory/feedback/20261110T073617Z-speckit-analyze.md
file.043.verdict=skipped
file.043.reason=generated
file.044.path=.specify/memory/feedback/20261110T074703Z-speckit-analyze.md
file.044.verdict=skipped
file.044.reason=generated
file.045.path=.specify/memory/feedback/20261110T080448Z-speckit-analyze.md
file.045.verdict=skipped
file.045.reason=generated
file.046.path=.specify/memory/feedback/20261110T080543Z-speckit-analyze.md
file.046.verdict=skipped
file.046.reason=generated
file.047.path=.specify/memory/feedback/20261110T080814Z-speckit-analyze.md
file.047.verdict=skipped
file.047.reason=generated
file.048.path=.specify/memory/feedback/20261110T081631Z-speckit-analyze.md
file.048.verdict=skipped
file.048.reason=generated
file.049.path=.specify/memory/feedback/20261110T123022Z-speckit-analyze.md
file.049.verdict=skipped
file.049.reason=generated
file.050.path=.specify/memory/feedback/20261110T124514Z-speckit-analyze.md
file.050.verdict=skipped
file.050.reason=generated
file.051.path=.specify/memory/feedback/20261110T151928Z-speckit-review.md
file.051.verdict=skipped
file.051.reason=generated
file.052.path=.specify/memory/feedback/20261110T151929Z-skill-review-sdd-process.md
file.052.verdict=skipped
file.052.reason=generated
file.053.path=.specify/memory/feedback/20261110T151935Z-skill-review-feature-quality.md
file.053.verdict=skipped
file.053.reason=generated
file.054.path=.specify/memory/feedback/20261110T151937Z-skill-code-review.md
file.054.verdict=skipped
file.054.reason=generated
file.055.path=.specify/memory/retention/closeout/20261110T061120Z-r20261110T055657Z-b095.json
file.055.verdict=skipped
file.055.reason=generated
file.056.path=.specify/memory/retention/closeout/20261110T062134Z-r20261110T055657Z-b095.json
file.056.verdict=skipped
file.056.reason=generated
file.057.path=.specify/memory/retention/closeout/20261110T064605Z-r20261110T064443Z-b095.json
file.057.verdict=skipped
file.057.reason=generated
file.058.path=.specify/memory/retention/closeout/20261110T070413Z-r20261110T065604Z-b095.json
file.058.verdict=skipped
file.058.reason=generated
file.059.path=.specify/memory/retention/closeout/20261110T072115Z-r20261110T072013Z-b095.json
file.059.verdict=skipped
file.059.reason=generated
file.060.path=.specify/memory/retention/closeout/20261110T074757Z-r20261110T055657Z-b095.json
file.060.verdict=skipped
file.060.reason=generated
file.061.path=.specify/memory/retention/closeout/20261110T081653Z-r20261110T055657Z-b095-r2merge.json
file.061.verdict=skipped
file.061.reason=generated
file.062.path=.specify/memory/retention/closeout/20261110T123105Z-r20261110T055657Z-b095-r3.json
file.062.verdict=skipped
file.062.reason=generated
file.063.path=.specify/memory/retention/closeout/20261110T124538Z-r20261110T055657Z-b095-r4.json
file.063.verdict=skipped
file.063.reason=generated
file.064.path=.specify/memory/retention/closeout/20261110T152047Z-r20261110T055657Z-b095-review.json
file.064.verdict=skipped
file.064.reason=generated
file.065.path=.specify/memory/session/20261109T074036Z-run-determination-speckit-tasks-r20261109t064500z-092a.md
file.065.verdict=skipped
file.065.reason=generated
file.066.path=.specify/memory/session/20261109T082732Z-run-determination-speckit-tasks-093-tasks-a1.md
file.066.verdict=skipped
file.066.reason=generated
file.067.path=.specify/memory/session/20261110T060918Z-run-determination-speckit-requirements-r20261110t055657z-b09.md
file.067.verdict=skipped
file.067.reason=generated
file.068.path=.specify/memory/session/20261110T062041Z-run-determination-speckit-clarify-r20261110t055657z-b095.md
file.068.verdict=skipped
file.068.reason=generated
file.069.path=.specify/memory/session/20261110T064451Z-run-determination-speckit-plan-r20261110t064443z-b095.md
file.069.verdict=skipped
file.069.reason=generated
file.070.path=.specify/memory/session/20261110T070310Z-run-determination-speckit-tasks-r20261110t065604z-b095.md
file.070.verdict=skipped
file.070.reason=generated
file.071.path=.specify/memory/session/20261110T072013Z-run-determination-speckit-checklist-r20261110t072013z-b095.md
file.071.verdict=skipped
file.071.reason=generated
file.072.path=.specify/memory/session/20261110T072037Z-run-determination-skill-create-checklist-r20261110t072013z-b.md
file.072.verdict=skipped
file.072.reason=generated
file.073.path=.specify/memory/session/20261110T073136Z-run-determination-speckit-analyze-r20261110t055657z-b095-w1.md
file.073.verdict=skipped
file.073.reason=generated
file.074.path=.specify/memory/session/20261110T073354Z-run-determination-speckit-analyze-r20261110t073257z-b095.md
file.074.verdict=skipped
file.074.reason=generated
file.075.path=.specify/memory/session/20261110T073607Z-run-determination-speckit-analyze-r20261110t055657z-b095.md
file.075.verdict=skipped
file.075.reason=generated
file.076.path=.specify/memory/session/20261110T074653Z-run-determination-speckit-analyze-r20261110t055657z-b095-mer.md
file.076.verdict=skipped
file.076.reason=generated
file.077.path=.specify/memory/session/20261110T080438Z-run-determination-speckit-analyze-r20261110t080102z-b095-r2w.md
file.077.verdict=skipped
file.077.reason=generated
file.078.path=.specify/memory/session/20261110T080529Z-run-determination-speckit-analyze-r20261110t055657z-b095-r2w.md
file.078.verdict=skipped
file.078.reason=generated
file.079.path=.specify/memory/session/20261110T080800Z-run-determination-speckit-analyze-r20261110t055657z-b095-r2w.md
file.079.verdict=skipped
file.079.reason=generated
file.080.path=.specify/memory/session/20261110T081631Z-run-determination-speckit-analyze-r20261110t055657z-b095-r2m.md
file.080.verdict=skipped
file.080.reason=generated
file.081.path=.specify/memory/session/20261110T123009Z-run-determination-speckit-analyze-r20261110t055657z-b095-r3.md
file.081.verdict=skipped
file.081.reason=generated
file.082.path=.specify/memory/session/20261110T124504Z-run-determination-speckit-analyze-r20261110t055657z-b095-r4.md
file.082.verdict=skipped
file.082.reason=generated
file.083.path=.specify/memory/session/20261110T151908Z-run-determination-skill-code-review-r20261110t055657z-b095-r.md
file.083.verdict=skipped
file.083.reason=generated
file.084.path=.specify/memory/session/20261110T151908Z-run-determination-skill-review-feature-quality-r20261110t055.md
file.084.verdict=skipped
file.084.reason=generated
file.085.path=.specify/memory/session/20261110T151908Z-run-determination-skill-review-sdd-process-r20261110t055657z.md
file.085.verdict=skipped
file.085.reason=generated
file.086.path=.specify/memory/session/20261110T151908Z-run-determination-speckit-review-r20261110t055657z-b095-revi.md
file.086.verdict=skipped
file.086.reason=generated
file.087.path=.specify/memory/session/interview-blocked-stalled-lines-2026-11-10.dag.json
file.087.verdict=skipped
file.087.reason=generated
file.088.path=.specify/memory/session/interview-blocked-stalled-lines-2026-11-10.md
file.088.verdict=skipped
file.088.reason=generated
file.089.path=.specify/register.md
file.089.verdict=skipped
file.089.reason=non-code-file
file.090.path=.specify/scripts/bash/run-tests-shards.sh
file.090.verdict=skipped
file.090.reason=generated
file.091.path=.specify/scripts/python/role-edge-check.py
file.091.verdict=skipped
file.091.reason=generated
file.092.path=.specify/scripts/python/scan-temp-usage.py
file.092.verdict=skipped
file.092.reason=generated
file.093.path=.specify/scripts/python/status-digest.py
file.093.verdict=skipped
file.093.reason=generated
file.094.path=.specify/shared/definitions/agent-definitions.md
file.094.verdict=skipped
file.094.reason=generated
file.095.path=.specify/shared/definitions/framework-map.md
file.095.verdict=skipped
file.095.reason=generated
file.096.path=.specify/shared/definitions/subagent-definitions.md
file.096.verdict=skipped
file.096.reason=generated
file.097.path=.specify/shared/definitions/superagent-definitions.md
file.097.verdict=skipped
file.097.reason=generated
file.098.path=.specify/shared/guidelines/better-harness.md
file.098.verdict=skipped
file.098.reason=generated
file.099.path=.specify/shared/guidelines/confirmation-gates.md
file.099.verdict=skipped
file.099.reason=generated
file.100.path=.specify/skills/internal/code-review/scripts/git-delta-review.sh
file.100.verdict=skipped
file.100.reason=generated
file.101.path=.specify/skills/internal/create-team/SKILL.md
file.101.verdict=skipped
file.101.reason=generated
file.102.path=.specify/skills/internal/create-team/references/patterns.md
file.102.verdict=skipped
file.102.reason=generated
file.103.path=.specify/skills/internal/run-agent/SKILL.md
file.103.verdict=skipped
file.103.reason=generated
file.104.path=.specify/skills/sdd-loop-driver/SKILL.md
file.104.verdict=skipped
file.104.reason=generated
file.105.path=.specify/skills/sdd-loop-driver/references/dispatch-recipes.md
file.105.verdict=skipped
file.105.reason=generated
file.106.path=.specify/skills/sdd-loop-driver/references/stage-prompts.md
file.106.verdict=skipped
file.106.reason=generated
file.107.path=.specify/specs/095-superagent-role/checklists/requirements-quality-2026-11-10.md
file.107.verdict=skipped
file.107.reason=non-code-file
file.108.path=.specify/specs/095-superagent-role/checklists/requirements.md
file.108.verdict=skipped
file.108.reason=non-code-file
file.109.path=.specify/specs/095-superagent-role/code-review.md
file.109.verdict=skipped
file.109.reason=non-code-file
file.110.path=.specify/specs/095-superagent-role/contracts/harness-landing.contract.md
file.110.verdict=skipped
file.110.reason=non-code-file
file.111.path=.specify/specs/095-superagent-role/contracts/role-edge-engine.contract.md
file.111.verdict=skipped
file.111.reason=non-code-file
file.112.path=.specify/specs/095-superagent-role/contracts/role-transition-payload.contract.md
file.112.verdict=skipped
file.112.reason=non-code-file
file.113.path=.specify/specs/095-superagent-role/contracts/status-digest-role-view.contract.md
file.113.verdict=skipped
file.113.reason=non-code-file
file.114.path=.specify/specs/095-superagent-role/coverage-baseline.txt
file.114.verdict=skipped
file.114.reason=non-code-file
file.115.path=.specify/specs/095-superagent-role/data-model.md
file.115.verdict=skipped
file.115.reason=non-code-file
file.116.path=.specify/specs/095-superagent-role/feature-ref.md
file.116.verdict=skipped
file.116.reason=non-code-file
file.117.path=.specify/specs/095-superagent-role/notes/baseline-failed-names.txt
file.117.verdict=skipped
file.117.reason=non-code-file
file.118.path=.specify/specs/095-superagent-role/notes/baseline-provenance.md
file.118.verdict=skipped
file.118.reason=non-code-file
file.119.path=.specify/specs/095-superagent-role/notes/coverage-baseline-2026-11-10-tasks-frozen.txt
file.119.verdict=skipped
file.119.reason=non-code-file
file.120.path=.specify/specs/095-superagent-role/notes/pre-change-measurements.md
file.120.verdict=skipped
file.120.reason=non-code-file
file.121.path=.specify/specs/095-superagent-role/notes/quickstart-run.md
file.121.verdict=skipped
file.121.reason=non-code-file
file.122.path=.specify/specs/095-superagent-role/notes/red-first-evidence.md
file.122.verdict=skipped
file.122.reason=non-code-file
file.123.path=.specify/specs/095-superagent-role/observation-appendix.md
file.123.verdict=skipped
file.123.reason=non-code-file
file.124.path=.specify/specs/095-superagent-role/plan.md
file.124.verdict=skipped
file.124.reason=non-code-file
file.125.path=.specify/specs/095-superagent-role/quickstart.md
file.125.verdict=skipped
file.125.reason=non-code-file
file.126.path=.specify/specs/095-superagent-role/requirements.md
file.126.verdict=skipped
file.126.reason=non-code-file
file.127.path=.specify/specs/095-superagent-role/review.md
file.127.verdict=skipped
file.127.reason=non-code-file
file.128.path=.specify/specs/095-superagent-role/tasks.md
file.128.verdict=skipped
file.128.reason=non-code-file
file.129.path=.specify/specs/095-superagent-role/test-evidence/analyze-findings-W1.md
file.129.verdict=skipped
file.129.reason=non-code-file
file.130.path=.specify/specs/095-superagent-role/test-evidence/analyze-findings-W2.md
file.130.verdict=skipped
file.130.reason=non-code-file
file.131.path=.specify/specs/095-superagent-role/test-evidence/analyze-findings-W3.md
file.131.verdict=skipped
file.131.reason=non-code-file
file.132.path=.specify/specs/095-superagent-role/test-evidence/analyze-findings-round2-W1.md
file.132.verdict=skipped
file.132.reason=non-code-file
file.133.path=.specify/specs/095-superagent-role/test-evidence/analyze-findings-round2-W2.md
file.133.verdict=skipped
file.133.reason=non-code-file
file.134.path=.specify/specs/095-superagent-role/test-evidence/analyze-findings-round2-W3.md
file.134.verdict=skipped
file.134.reason=non-code-file
file.135.path=.specify/specs/095-superagent-role/test-evidence/analyze-merged-2026-11-10.md
file.135.verdict=skipped
file.135.reason=non-code-file
file.136.path=.specify/specs/095-superagent-role/test-evidence/analyze-merged-r3-2026-11-10.md
file.136.verdict=skipped
file.136.reason=non-code-file
file.137.path=.specify/specs/095-superagent-role/test-evidence/analyze-merged-r4-2026-11-10.md
file.137.verdict=skipped
file.137.reason=non-code-file
file.138.path=.specify/specs/095-superagent-role/test-evidence/analyze-merged-round2-2026-11-10.md
file.138.verdict=skipped
file.138.reason=non-code-file
file.139.path=.specify/specs/095-superagent-role/test-evidence/analyze-repair-dispositions-2026-11-10.md
file.139.verdict=skipped
file.139.reason=non-code-file
file.140.path=.specify/specs/095-superagent-role/test-evidence/analyze-repair-dispositions-r3-2026-11-10.md
file.140.verdict=skipped
file.140.reason=non-code-file
file.141.path=.specify/specs/095-superagent-role/test-evidence/analyze-repair-dispositions-r4-2026-11-10.md
file.141.verdict=skipped
file.141.reason=non-code-file
file.142.path=.specify/specs/095-superagent-role/test-evidence/analyze-repair-gates-2026-11-10.txt
file.142.verdict=skipped
file.142.reason=non-code-file
file.143.path=.specify/specs/095-superagent-role/test-evidence/analyze-repair-gates-r3-2026-11-10.txt
file.143.verdict=skipped
file.143.reason=non-code-file
file.144.path=.specify/specs/095-superagent-role/test-evidence/analyze-repair-gates-r4-2026-11-10.txt
file.144.verdict=skipped
file.144.reason=non-code-file
file.145.path=.specify/specs/095-superagent-role/test-evidence/analyze-wrapup-exec-quant.txt
file.145.verdict=skipped
file.145.reason=non-code-file
file.146.path=.specify/specs/095-superagent-role/test-evidence/analyze-wrapup-feedback.txt
file.146.verdict=skipped
file.146.reason=non-code-file
file.147.path=.specify/specs/095-superagent-role/test-evidence/analyze-wrapup-run-determination.txt
file.147.verdict=skipped
file.147.reason=non-code-file
file.148.path=.specify/specs/095-superagent-role/test-evidence/checklist-readings-2026-11-10.txt
file.148.verdict=skipped
file.148.reason=non-code-file
file.149.path=.specify/specs/095-superagent-role/test-evidence/checklist-wrapup-exec-quant-skill.txt
file.149.verdict=skipped
file.149.reason=non-code-file
file.150.path=.specify/specs/095-superagent-role/test-evidence/checklist-wrapup-exec-quant.txt
file.150.verdict=skipped
file.150.reason=non-code-file
file.151.path=.specify/specs/095-superagent-role/test-evidence/checklist-wrapup-feedback-skill.txt
file.151.verdict=skipped
file.151.reason=non-code-file
file.152.path=.specify/specs/095-superagent-role/test-evidence/checklist-wrapup-feedback.txt
file.152.verdict=skipped
file.152.reason=non-code-file
file.153.path=.specify/specs/095-superagent-role/test-evidence/checklist-wrapup-run-determination-skill.txt
file.153.verdict=skipped
file.153.reason=non-code-file
file.154.path=.specify/specs/095-superagent-role/test-evidence/checklist-wrapup-run-determination.txt
file.154.verdict=skipped
file.154.reason=non-code-file
file.155.path=.specify/specs/095-superagent-role/test-evidence/clarify-flow-class.txt
file.155.verdict=skipped
file.155.reason=non-code-file
file.156.path=.specify/specs/095-superagent-role/test-evidence/clarify-overlap-check.json
file.156.verdict=skipped
file.156.reason=non-code-file
file.157.path=.specify/specs/095-superagent-role/test-evidence/clarify-overlap-check.txt
file.157.verdict=skipped
file.157.reason=non-code-file
file.158.path=.specify/specs/095-superagent-role/test-evidence/clarify-validate-requirements.txt
file.158.verdict=skipped
file.158.reason=non-code-file
file.159.path=.specify/specs/095-superagent-role/test-evidence/clarify-wrapup-exec-quant.txt
file.159.verdict=skipped
file.159.reason=non-code-file
file.160.path=.specify/specs/095-superagent-role/test-evidence/clarify-wrapup-feedback.txt
file.160.verdict=skipped
file.160.reason=non-code-file
file.161.path=.specify/specs/095-superagent-role/test-evidence/clarify-wrapup-run-determination.txt
file.161.verdict=skipped
file.161.reason=non-code-file
file.162.path=.specify/specs/095-superagent-role/test-evidence/closure-acceptance.txt
file.162.verdict=skipped
file.162.reason=non-code-file
file.163.path=.specify/specs/095-superagent-role/test-evidence/closure-suite-comparison.txt
file.163.verdict=skipped
file.163.reason=non-code-file
file.164.path=.specify/specs/095-superagent-role/test-evidence/closure-suite-names.txt
file.164.verdict=skipped
file.164.reason=non-code-file
file.165.path=.specify/specs/095-superagent-role/test-evidence/closure-suite.txt
file.165.verdict=skipped
file.165.reason=non-code-file
file.166.path=.specify/specs/095-superagent-role/test-evidence/concurrency-invariants.txt
file.166.verdict=skipped
file.166.reason=non-code-file
file.167.path=.specify/specs/095-superagent-role/test-evidence/concurrency-wave-readings.txt
file.167.verdict=skipped
file.167.reason=non-code-file
file.168.path=.specify/specs/095-superagent-role/test-evidence/definitions-readings.txt
file.168.verdict=skipped
file.168.reason=non-code-file
file.169.path=.specify/specs/095-superagent-role/test-evidence/gate-checks.txt
file.169.verdict=skipped
file.169.reason=non-code-file
file.170.path=.specify/specs/095-superagent-role/test-evidence/instructions-budget.txt
file.170.verdict=skipped
file.170.reason=non-code-file
file.171.path=.specify/specs/095-superagent-role/test-evidence/mirror-obligations.txt
file.171.verdict=skipped
file.171.reason=non-code-file
file.172.path=.specify/specs/095-superagent-role/test-evidence/observation-appendix-check.txt
file.172.verdict=skipped
file.172.reason=non-code-file
file.173.path=.specify/specs/095-superagent-role/test-evidence/plan-gate.txt
file.173.verdict=skipped
file.173.reason=non-code-file
file.174.path=.specify/specs/095-superagent-role/test-evidence/plan-stage-evidence.md
file.174.verdict=skipped
file.174.reason=non-code-file
file.175.path=.specify/specs/095-superagent-role/test-evidence/plan-wrapup-exec-quant.txt
file.175.verdict=skipped
file.175.reason=non-code-file
file.176.path=.specify/specs/095-superagent-role/test-evidence/plan-wrapup-feedback.txt
file.176.verdict=skipped
file.176.reason=non-code-file
file.177.path=.specify/specs/095-superagent-role/test-evidence/plan-wrapup-run-determination.txt
file.177.verdict=skipped
file.177.reason=non-code-file
file.178.path=.specify/specs/095-superagent-role/test-evidence/requirements-flow-class.txt
file.178.verdict=skipped
file.178.reason=non-code-file
file.179.path=.specify/specs/095-superagent-role/test-evidence/requirements-glossary-add.txt
file.179.verdict=skipped
file.179.reason=non-code-file
file.180.path=.specify/specs/095-superagent-role/test-evidence/requirements-glossary-conflict.txt
file.180.verdict=skipped
file.180.reason=non-code-file
file.181.path=.specify/specs/095-superagent-role/test-evidence/requirements-validator-initial.txt
file.181.verdict=skipped
file.181.reason=non-code-file
file.182.path=.specify/specs/095-superagent-role/test-evidence/requirements-validator.txt
file.182.verdict=skipped
file.182.reason=non-code-file
file.183.path=.specify/specs/095-superagent-role/test-evidence/review-repair-baseline-module-health.txt
file.183.verdict=skipped
file.183.reason=non-code-file
file.184.path=.specify/specs/095-superagent-role/test-evidence/review-repair-closure-acceptance.txt
file.184.verdict=skipped
file.184.reason=non-code-file
file.185.path=.specify/specs/095-superagent-role/test-evidence/review-repair-closure-suite-comparison.txt
file.185.verdict=skipped
file.185.reason=non-code-file
file.186.path=.specify/specs/095-superagent-role/test-evidence/review-repair-closure-suite-names.txt
file.186.verdict=skipped
file.186.reason=non-code-file
file.187.path=.specify/specs/095-superagent-role/test-evidence/review-repair-closure-suite.txt
file.187.verdict=skipped
file.187.reason=non-code-file
file.188.path=.specify/specs/095-superagent-role/test-evidence/review-repair-dispositions-r1-2026-11-10.md
file.188.verdict=skipped
file.188.reason=non-code-file
file.189.path=.specify/specs/095-superagent-role/test-evidence/review-repair-guards.txt
file.189.verdict=skipped
file.189.reason=non-code-file
file.190.path=.specify/specs/095-superagent-role/test-evidence/review-repair-mutation-drills.txt
file.190.verdict=skipped
file.190.reason=non-code-file
file.191.path=.specify/specs/095-superagent-role/test-evidence/review-repair-suite.txt
file.191.verdict=skipped
file.191.reason=non-code-file
file.192.path=.specify/specs/095-superagent-role/test-evidence/role-edge-engine-readings.txt
file.192.verdict=skipped
file.192.reason=non-code-file
file.193.path=.specify/specs/095-superagent-role/test-evidence/role-transition-readings.txt
file.193.verdict=skipped
file.193.reason=non-code-file
file.194.path=.specify/specs/095-superagent-role/test-evidence/smoke-six-modules.txt
file.194.verdict=skipped
file.194.reason=non-code-file
file.195.path=.specify/specs/095-superagent-role/test-evidence/state-sync-recovery.txt
file.195.verdict=skipped
file.195.reason=non-code-file
file.196.path=.specify/specs/095-superagent-role/test-evidence/status-digest-roles-readings.txt
file.196.verdict=skipped
file.196.reason=non-code-file
file.197.path=.specify/specs/095-superagent-role/test-evidence/tasks-decomposition-check.txt
file.197.verdict=skipped
file.197.reason=non-code-file
file.198.path=.specify/specs/095-superagent-role/test-evidence/tasks-flow-class.txt
file.198.verdict=skipped
file.198.reason=non-code-file
file.199.path=.specify/specs/095-superagent-role/test-evidence/tasks-pre-analyze-check.txt
file.199.verdict=skipped
file.199.reason=non-code-file
file.200.path=.specify/specs/095-superagent-role/test-evidence/tasks-stage-evidence.md
file.200.verdict=skipped
file.200.reason=non-code-file
file.201.path=.specify/specs/095-superagent-role/test-evidence/tasks-validate.txt
file.201.verdict=skipped
file.201.reason=non-code-file
file.202.path=.specify/specs/095-superagent-role/test-evidence/tasks-wrapup-exec-quant.txt
file.202.verdict=skipped
file.202.reason=non-code-file
file.203.path=.specify/specs/095-superagent-role/test-evidence/tasks-wrapup-feedback.txt
file.203.verdict=skipped
file.203.reason=non-code-file
file.204.path=.specify/specs/095-superagent-role/test-evidence/tasks-wrapup-run-determination.txt
file.204.verdict=skipped
file.204.reason=non-code-file
file.205.path=.specify/specs/095-superagent-role/test-evidence/three-forms-readings.txt
file.205.verdict=skipped
file.205.reason=non-code-file
file.206.path=.specify/specs/095-superagent-role/test-evidence/validate-tasks.txt
file.206.verdict=skipped
file.206.reason=non-code-file
file.207.path=.specify/specs/095-superagent-role/test-evidence/wrapup-exec-quant.txt
file.207.verdict=skipped
file.207.reason=non-code-file
file.208.path=.specify/specs/095-superagent-role/test-evidence/wrapup-feedback.txt
file.208.verdict=skipped
file.208.reason=non-code-file
file.209.path=.specify/specs/095-superagent-role/test-evidence/wrapup-run-determination.txt
file.209.verdict=skipped
file.209.reason=non-code-file
file.210.path=.specify/specs/095-superagent-role/test-evidence/zero-mechanism-baseline-names.txt
file.210.verdict=skipped
file.210.reason=non-code-file
file.211.path=.specify/specs/095-superagent-role/test-evidence/zero-mechanism-current-names.txt
file.211.verdict=skipped
file.211.reason=non-code-file
file.212.path=.specify/specs/095-superagent-role/test-evidence/zero-mechanism-readings.txt
file.212.verdict=skipped
file.212.reason=non-code-file
file.213.path=.specify/specs/095-superagent-role/verification.md
file.213.verdict=skipped
file.213.reason=non-code-file
file.214.path=.specify/state/074-goal-team-sdd-unification.md
file.214.verdict=skipped
file.214.reason=non-code-file
file.215.path=.specify/state/074b-nested-governance.md
file.215.verdict=skipped
file.215.reason=non-code-file
file.216.path=.specify/state/076-decision-tension-contract.md
file.216.verdict=skipped
file.216.reason=non-code-file
file.217.path=.specify/state/077-doc-sdd-integration.md
file.217.verdict=skipped
file.217.reason=non-code-file
file.218.path=.specify/state/078-bilingual-expression.md
file.218.verdict=skipped
file.218.reason=non-code-file
file.219.path=.specify/state/078-coaching-skills.md
file.219.verdict=skipped
file.219.reason=non-code-file
file.220.path=.specify/state/079-humanize-run-output.md
file.220.verdict=skipped
file.220.reason=non-code-file
file.221.path=.specify/state/081-acceptance-hardening.md
file.221.verdict=skipped
file.221.reason=non-code-file
file.222.path=.specify/state/082-self-explanatory-integration.md
file.222.verdict=skipped
file.222.reason=non-code-file
file.223.path=.specify/state/083-budget-calibration-tests.txt
file.223.verdict=skipped
file.223.reason=non-code-file
file.224.path=.specify/state/083-budget-calibration.md
file.224.verdict=skipped
file.224.reason=non-code-file
file.225.path=.specify/state/083-loop-state-self-test.txt
file.225.verdict=skipped
file.225.reason=non-code-file
file.226.path=.specify/state/083-mechanism-policy-separation.md
file.226.verdict=skipped
file.226.reason=non-code-file
file.227.path=.specify/state/084-harness-triple-structure.md
file.227.verdict=skipped
file.227.reason=non-code-file
file.228.path=.specify/state/086-efficient-test-execution.md
file.228.verdict=skipped
file.228.reason=non-code-file
file.229.path=.specify/state/087-arch-diagram-docs.md
file.229.verdict=skipped
file.229.reason=non-code-file
file.230.path=.specify/state/088-speckit-visualization.md
file.230.verdict=skipped
file.230.reason=non-code-file
file.231.path=.specify/state/089-script-interface-contract.md
file.231.verdict=skipped
file.231.reason=non-code-file
file.232.path=.specify/state/090-re-anchoring.md
file.232.verdict=skipped
file.232.reason=non-code-file
file.233.path=.specify/state/091-auto-git-closeout.md
file.233.verdict=skipped
file.233.reason=non-code-file
file.234.path=.specify/state/092-non-disposable.md
file.234.verdict=skipped
file.234.reason=non-code-file
file.235.path=.specify/state/093-concurrency-by-default.md
file.235.verdict=skipped
file.235.reason=non-code-file
file.236.path=.specify/state/094-goal-team-parallel.md
file.236.verdict=skipped
file.236.reason=non-code-file
file.237.path=.specify/state/eval-baseline/README.md
file.237.verdict=skipped
file.237.reason=non-code-file
file.238.path=.specify/state/eval-baseline/instructions.md
file.238.verdict=skipped
file.238.reason=non-code-file
file.239.path=.specify/state/speckit-docs-expression.md
file.239.verdict=skipped
file.239.reason=non-code-file
file.240.path=.specify/state/wp/088-speckit-visualization-implement-a1-gate-plan.json
file.240.verdict=skipped
file.240.reason=non-code-file
file.241.path=.specify/state/wp/088-speckit-visualization-implement-a2-gate-plan.json
file.241.verdict=skipped
file.241.reason=non-code-file
file.242.path=.specify/state/wp/088-speckit-visualization-plan-a1-gate-plan.json
file.242.verdict=skipped
file.242.reason=non-code-file
file.243.path=.specify/state/wp/088-speckit-visualization-plan-a2-gate-plan.json
file.243.verdict=skipped
file.243.reason=non-code-file
file.244.path=.specify/templates/instructions-template.md
file.244.verdict=skipped
file.244.reason=generated
file.245.path=scripts/bash/run-tests-shards.sh
file.245.verdict=reviewed
file.246.path=scripts/python/role-edge-check.py
file.246.verdict=reviewed
file.247.path=scripts/python/scan-temp-usage.py
file.247.verdict=reviewed
file.248.path=scripts/python/status-digest.py
file.248.verdict=reviewed
file.249.path=shared/definitions/agent-definitions.md
file.249.verdict=skipped
file.249.reason=non-code-file
file.250.path=shared/definitions/framework-map.md
file.250.verdict=skipped
file.250.reason=non-code-file
file.251.path=shared/definitions/subagent-definitions.md
file.251.verdict=skipped
file.251.reason=non-code-file
file.252.path=shared/definitions/superagent-definitions.md
file.252.verdict=skipped
file.252.reason=non-code-file
file.253.path=shared/guidelines/better-harness.md
file.253.verdict=skipped
file.253.reason=non-code-file
file.254.path=shared/guidelines/confirmation-gates.md
file.254.verdict=skipped
file.254.reason=non-code-file
file.255.path=skills/external/sdd-loop-driver/SKILL.md
file.255.verdict=skipped
file.255.reason=non-code-file
file.256.path=skills/external/sdd-loop-driver/references/dispatch-recipes.md
file.256.verdict=skipped
file.256.reason=non-code-file
file.257.path=skills/external/sdd-loop-driver/references/stage-prompts.md
file.257.verdict=skipped
file.257.reason=non-code-file
file.258.path=skills/internal/code-review/scripts/git-delta-review.sh
file.258.verdict=reviewed
file.259.path=skills/internal/create-team/SKILL.md
file.259.verdict=skipped
file.259.reason=non-code-file
file.260.path=skills/internal/create-team/references/patterns.md
file.260.verdict=skipped
file.260.reason=non-code-file
file.261.path=skills/internal/run-agent/SKILL.md
file.261.verdict=skipped
file.261.reason=non-code-file
file.262.path=templates/gitignore-specify-template
file.262.verdict=skipped
file.262.reason=non-code-file
file.263.path=templates/instructions-template.md
file.263.verdict=skipped
file.263.reason=non-code-file
file.264.path=tests/contract/test_code_review_skill_contract.py
file.264.verdict=reviewed
file.265.path=tests/contract/test_efficiency_element.py
file.265.verdict=reviewed
file.266.path=tests/contract/test_fast_fail_discipline.py
file.266.verdict=reviewed
file.267.path=tests/contract/test_instructions_budget_superagent_section.py
file.267.verdict=reviewed
file.268.path=tests/contract/test_role_edge_engine.py
file.268.verdict=reviewed
file.269.path=tests/contract/test_role_transition_payload.py
file.269.verdict=reviewed
file.270.path=tests/contract/test_specify_gitignore_template.py
file.270.verdict=reviewed
file.271.path=tests/contract/test_status_digest.py
file.271.verdict=reviewed
file.272.path=tests/contract/test_status_digest_roles.py
file.272.verdict=reviewed
file.273.path=tests/contract/test_superagent_definitions.py
file.273.verdict=reviewed
file.274.path=tests/contract/test_superagent_zero_mechanism.py
file.274.verdict=reviewed
file.275.path=tests/fixtures/superagent-role/conflict/logs/.gitkeep
file.275.verdict=skipped
file.275.reason=non-code-file
file.276.path=tests/fixtures/superagent-role/conflict/registry/.gitkeep
file.276.verdict=skipped
file.276.reason=non-code-file
file.277.path=tests/fixtures/superagent-role/conflict/state/.gitkeep
file.277.verdict=skipped
file.277.reason=non-code-file
file.278.path=tests/fixtures/superagent-role/conflict/teams/conflict-team/runs/20261110T000000Z-report.md
file.278.verdict=skipped
file.278.reason=non-code-file
file.279.path=tests/fixtures/superagent-role/conflict/teams/conflict-team/runs/20261110T010000Z-report.md
file.279.verdict=skipped
file.279.reason=non-code-file
file.280.path=tests/fixtures/superagent-role/empty/logs/.gitkeep
file.280.verdict=skipped
file.280.reason=non-code-file
file.281.path=tests/fixtures/superagent-role/empty/registry/.gitkeep
file.281.verdict=skipped
file.281.reason=non-code-file
file.282.path=tests/fixtures/superagent-role/empty/state/.gitkeep
file.282.verdict=skipped
file.282.reason=non-code-file
file.283.path=tests/fixtures/superagent-role/empty/teams/.gitkeep
file.283.verdict=skipped
file.283.reason=non-code-file
file.284.path=tests/fixtures/superagent-role/fanout-10/logs/.gitkeep
file.284.verdict=skipped
file.284.reason=non-code-file
file.285.path=tests/fixtures/superagent-role/fanout-10/registry/.gitkeep
file.285.verdict=skipped
file.285.reason=non-code-file
file.286.path=tests/fixtures/superagent-role/fanout-10/state/.gitkeep
file.286.verdict=skipped
file.286.reason=non-code-file
file.287.path=tests/fixtures/superagent-role/fanout-10/teams/fanout-team/runs/20261110T000000Z-report.md
file.287.verdict=skipped
file.287.reason=non-code-file
file.288.path=tests/fixtures/superagent-role/interrupted/logs/child-1.jsonl
file.288.verdict=skipped
file.288.reason=non-code-file
file.289.path=tests/fixtures/superagent-role/interrupted/logs/child-1.status
file.289.verdict=skipped
file.289.reason=non-code-file
file.290.path=tests/fixtures/superagent-role/interrupted/registry/demo-line.json
file.290.verdict=skipped
file.290.reason=non-code-file
file.291.path=tests/fixtures/superagent-role/interrupted/state/demo-line.md
file.291.verdict=skipped
file.291.reason=non-code-file
file.292.path=tests/fixtures/superagent-role/interrupted/teams/interrupted-team/runs/20261110T000000Z-report.md
file.292.verdict=skipped
file.292.reason=non-code-file
file.293.path=tests/fixtures/superagent-role/local-team/logs/alice.jsonl
file.293.verdict=skipped
file.293.reason=non-code-file
file.294.path=tests/fixtures/superagent-role/local-team/logs/alice.status
file.294.verdict=skipped
file.294.reason=non-code-file
file.295.path=tests/fixtures/superagent-role/local-team/logs/bob.jsonl
file.295.verdict=skipped
file.295.reason=non-code-file
file.296.path=tests/fixtures/superagent-role/local-team/logs/bob.status
file.296.verdict=skipped
file.296.reason=non-code-file
file.297.path=tests/fixtures/superagent-role/local-team/logs/carol.jsonl
file.297.verdict=skipped
file.297.reason=non-code-file
file.298.path=tests/fixtures/superagent-role/local-team/logs/carol.status
file.298.verdict=skipped
file.298.reason=non-code-file
file.299.path=tests/fixtures/superagent-role/local-team/registry/.gitkeep
file.299.verdict=skipped
file.299.reason=non-code-file
file.300.path=tests/fixtures/superagent-role/local-team/state/.gitkeep
file.300.verdict=skipped
file.300.reason=non-code-file
file.301.path=tests/fixtures/superagent-role/local-team/teams/local-team/runs/20261110T000000Z-report.md
file.301.verdict=skipped
file.301.reason=non-code-file
file.302.path=tests/fixtures/superagent-role/malformed/logs/.gitkeep
file.302.verdict=skipped
file.302.reason=non-code-file
file.303.path=tests/fixtures/superagent-role/malformed/registry/.gitkeep
file.303.verdict=skipped
file.303.reason=non-code-file
file.304.path=tests/fixtures/superagent-role/malformed/state/.gitkeep
file.304.verdict=skipped
file.304.reason=non-code-file
file.305.path=tests/fixtures/superagent-role/malformed/teams/malformed-team/runs/20261110T000000Z-report.md
file.305.verdict=skipped
file.305.reason=non-code-file
file.306.path=tests/fixtures/superagent-role/payload/role-fields.md
file.306.verdict=skipped
file.306.reason=non-code-file
file.307.path=tests/fixtures/superagent-role/payload/role-transition-complete.md
file.307.verdict=skipped
file.307.reason=non-code-file
file.308.path=tests/fixtures/superagent-role/payload/role-transition-missing-item.md
file.308.verdict=skipped
file.308.reason=non-code-file
file.309.path=tests/fixtures/superagent-role/payload/role-transition-skill-load.md
file.309.verdict=skipped
file.309.reason=non-code-file
file.310.path=tests/fixtures/superagent-role/remote-topology/logs/remote--20261110T000000Z--worker.jsonl
file.310.verdict=skipped
file.310.reason=non-code-file
file.311.path=tests/fixtures/superagent-role/remote-topology/logs/remote--20261110T000000Z--worker.status
file.311.verdict=skipped
file.311.reason=non-code-file
file.312.path=tests/fixtures/superagent-role/remote-topology/memory/exec-quant/records/20261110T000000000000Z-fixture01.json
file.312.verdict=skipped
file.312.reason=non-code-file
file.313.path=tests/fixtures/superagent-role/remote-topology/registry/remote-builder.json
file.313.verdict=skipped
file.313.reason=non-code-file
file.314.path=tests/fixtures/superagent-role/remote-topology/state/.gitkeep
file.314.verdict=skipped
file.314.reason=non-code-file
file.315.path=tests/fixtures/superagent-role/remote-topology/teams/.gitkeep
file.315.verdict=skipped
file.315.reason=non-code-file
file.316.path=tests/fixtures/superagent-role/root-a-b/logs/A.jsonl
file.316.verdict=skipped
file.316.reason=non-code-file
file.317.path=tests/fixtures/superagent-role/root-a-b/logs/A.status
file.317.verdict=skipped
file.317.reason=non-code-file
file.318.path=tests/fixtures/superagent-role/root-a-b/logs/B.jsonl
file.318.verdict=skipped
file.318.reason=non-code-file
file.319.path=tests/fixtures/superagent-role/root-a-b/logs/B.status
file.319.verdict=skipped
file.319.reason=non-code-file
file.320.path=tests/fixtures/superagent-role/root-a-b/registry/demo-line.json
file.320.verdict=skipped
file.320.reason=non-code-file
file.321.path=tests/fixtures/superagent-role/root-a-b/state/demo-line.md
file.321.verdict=skipped
file.321.reason=non-code-file
file.322.path=tests/fixtures/superagent-role/root-a-b/state/prompt-B-s1.md.meta.json
file.322.verdict=skipped
file.322.reason=non-code-file
file.323.path=tests/fixtures/superagent-role/root-a-b/teams/demo-team/runs/20261110T000000Z-report.md
file.323.verdict=skipped
file.323.reason=non-code-file
file.324.path=tests/fixtures/superagent-role/violations/dangling-parent/logs/.gitkeep
file.324.verdict=skipped
file.324.reason=non-code-file
file.325.path=tests/fixtures/superagent-role/violations/dangling-parent/registry/.gitkeep
file.325.verdict=skipped
file.325.reason=non-code-file
file.326.path=tests/fixtures/superagent-role/violations/dangling-parent/state/.gitkeep
file.326.verdict=skipped
file.326.reason=non-code-file
file.327.path=tests/fixtures/superagent-role/violations/dangling-parent/teams/.gitkeep
file.327.verdict=skipped
file.327.reason=non-code-file
file.328.path=tests/fixtures/superagent-role/violations/dangling-parent/teams/dangling-team/runs/20261110T000000Z-report.md
file.328.verdict=skipped
file.328.reason=non-code-file
file.329.path=tests/fixtures/superagent-role/violations/depth-cycle/logs/.gitkeep
file.329.verdict=skipped
file.329.reason=non-code-file
file.330.path=tests/fixtures/superagent-role/violations/depth-cycle/registry/.gitkeep
file.330.verdict=skipped
file.330.reason=non-code-file
file.331.path=tests/fixtures/superagent-role/violations/depth-cycle/state/.gitkeep
file.331.verdict=skipped
file.331.reason=non-code-file
file.332.path=tests/fixtures/superagent-role/violations/depth-cycle/teams/.gitkeep
file.332.verdict=skipped
file.332.reason=non-code-file
file.333.path=tests/fixtures/superagent-role/violations/depth-cycle/teams/cycle-team/runs/20261110T000000Z-report.md
file.333.verdict=skipped
file.333.reason=non-code-file
file.334.path=tests/fixtures/superagent-role/violations/self-dispatch/logs/.gitkeep
file.334.verdict=skipped
file.334.reason=non-code-file
file.335.path=tests/fixtures/superagent-role/violations/self-dispatch/registry/.gitkeep
file.335.verdict=skipped
file.335.reason=non-code-file
file.336.path=tests/fixtures/superagent-role/violations/self-dispatch/state/.gitkeep
file.336.verdict=skipped
file.336.reason=non-code-file
file.337.path=tests/fixtures/superagent-role/violations/self-dispatch/teams/.gitkeep
file.337.verdict=skipped
file.337.reason=non-code-file
file.338.path=tests/fixtures/superagent-role/violations/self-dispatch/teams/self-team/runs/20261110T000000Z-report.md
file.338.verdict=skipped
file.338.reason=non-code-file
file.339.path=tests/fixtures/superagent-role/violations/unbacked-claim/logs/.gitkeep
file.339.verdict=skipped
file.339.reason=non-code-file
file.340.path=tests/fixtures/superagent-role/violations/unbacked-claim/registry/.gitkeep
file.340.verdict=skipped
file.340.reason=non-code-file
file.341.path=tests/fixtures/superagent-role/violations/unbacked-claim/state/.gitkeep
file.341.verdict=skipped
file.341.reason=non-code-file
file.342.path=tests/fixtures/superagent-role/violations/unbacked-claim/teams/.gitkeep
file.342.verdict=skipped
file.342.reason=non-code-file
file.343.path=tests/fixtures/superagent-role/violations/unbacked-claim/teams/claim-team/runs/20261110T000000Z-report.md
file.343.verdict=skipped
file.343.reason=non-code-file
file.344.path=tests/unit/test_status_digest_unit.py
file.344.verdict=reviewed
<!-- coverage-receipt:end -->
