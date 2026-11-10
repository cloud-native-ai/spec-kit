# Code Review Report — 代码段 (code segment)

| 属性 | 值 |
|------|-----|
| **分支** | `095-superagent-role` |
| **基准** | `b3da3a26dfba209057f65c2b17962b9516812c39` (`b3da3a26d`) |
| **目标** | `6c48e9c253166a71ab8364dd818c7d4409471fb5` (`6c48e9c25`) |
| **基准来源** | `feature-first-commit` |
| **渲染模式** | `renderer: text` |
| **Reviewer** | `Qiming Liu (John)` |
| **日期** | `2026-11-10T15:14:02Z` |

## 变更概览

```
 .specify/.gitignore                                |    4 +
 .specify/constitution.md                           |   16 +-
 .specify/features.md                               |    5 +-
 .specify/features/095-superagent-role.md           |   71 +
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
 .../20261110T061120Z-r20261110T055657Z-b095.json   |   23 +
 .../20261110T062134Z-r20261110T055657Z-b095.json   |   23 +
 .../20261110T064605Z-r20261110T064443Z-b095.json   |   23 +
 .../20261110T070413Z-r20261110T065604Z-b095.json   |   23 +
 .../20261110T072115Z-r20261110T072013Z-b095.json   |   38 +
 .../20261110T074757Z-r20261110T055657Z-b095.json   |   68 +
 ...110T081653Z-r20261110T055657Z-b095-r2merge.json |   68 +
 ...20261110T123105Z-r20261110T055657Z-b095-r3.json |   23 +
 ...20261110T124538Z-r20261110T055657Z-b095-r4.json |   23 +
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
 ...rview-blocked-stalled-lines-2026-11-10.dag.json |  128 +
 .../interview-blocked-stalled-lines-2026-11-10.md  |   20 +
 .specify/scripts/bash/run-tests-shards.sh          |    8 +-
 .specify/scripts/python/role-edge-check.py         |  998 +++
 .specify/scripts/python/scan-temp-usage.py         |   12 +-
 .specify/scripts/python/status-digest.py           |  592 +-
 .specify/shared/definitions/agent-definitions.md   |    1 +
 .specify/shared/definitions/framework-map.md       |    1 +
 .../shared/definitions/subagent-definitions.md     |    2 +
 .../shared/definitions/superagent-definitions.md   |  124 +
 .specify/shared/guidelines/better-harness.md       |    4 +-
 .specify/shared/guidelines/confirmation-gates.md   |    6 +
 .specify/skills/internal/create-team/SKILL.md      |    2 +
 .../internal/create-team/references/patterns.md    |    1 +
 .specify/skills/internal/run-agent/SKILL.md        |   10 +
 .specify/skills/sdd-loop-driver/SKILL.md           |    1 +
 .../sdd-loop-driver/references/dispatch-recipes.md |    2 +-
 .../sdd-loop-driver/references/stage-prompts.md    |    2 +-
 .../checklists/requirements-quality-2026-11-10.md  |   83 +
 .../095-superagent-role/checklists/requirements.md |   55 +
 .../contracts/harness-landing.contract.md          |   59 +
 .../contracts/role-edge-engine.contract.md         |   82 +
 .../contracts/role-transition-payload.contract.md  |   67 +
 .../contracts/status-digest-role-view.contract.md  |   47 +
 .../095-superagent-role/coverage-baseline.txt      |  642 ++
 .specify/specs/095-superagent-role/data-model.md   |  115 +
 .specify/specs/095-superagent-role/feature-ref.md  |   21 +
 .../notes/baseline-failed-names.txt                |  303 +
 .../notes/baseline-provenance.md                   |   17 +
 .../notes/pre-change-measurements.md               |  139 +
 .../095-superagent-role/notes/quickstart-run.md    |  138 +
 .../notes/red-first-evidence.md                    |  329 +
 .../095-superagent-role/observation-appendix.md    |   30 +
 .specify/specs/095-superagent-role/plan.md         |  247 +
 .specify/specs/095-superagent-role/quickstart.md   |   57 +
 .specify/specs/095-superagent-role/requirements.md |  287 +
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
 .specify/specs/095-superagent-role/verification.md |  118 +
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
 scripts/python/role-edge-check.py                  |  998 +++
 scripts/python/scan-temp-usage.py                  |   12 +-
 scripts/python/status-digest.py                    |  592 +-
 shared/definitions/agent-definitions.md            |    1 +
 shared/definitions/framework-map.md                |    1 +
 shared/definitions/subagent-definitions.md         |    2 +
 shared/definitions/superagent-definitions.md       |  124 +
 shared/guidelines/better-harness.md                |    4 +-
 shared/guidelines/confirmation-gates.md            |    6 +
 skills/external/sdd-loop-driver/SKILL.md           |    1 +
 .../sdd-loop-driver/references/dispatch-recipes.md |    2 +-
 .../sdd-loop-driver/references/stage-prompts.md    |    2 +-
 skills/internal/create-team/SKILL.md               |    2 +
 skills/internal/create-team/references/patterns.md |    1 +
 skills/internal/run-agent/SKILL.md                 |   10 +
 templates/gitignore-specify-template               |    4 +
 templates/instructions-template.md                 |    6 +
 tests/contract/test_fast_fail_discipline.py        |   25 +-
 .../test_instructions_budget_superagent_section.py |  175 +
 tests/contract/test_role_edge_engine.py            |  774 ++
 tests/contract/test_role_transition_payload.py     |  377 +
 tests/contract/test_specify_gitignore_template.py  |    2 +
 tests/contract/test_status_digest.py               |  102 +-
 tests/contract/test_status_digest_roles.py         |  517 ++
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
 313 files changed, 26751 insertions(+), 5882 deletions(-)
```

---

## Review 意见


### 🔴 [BLOCKING] scripts/python/status-digest.py (Line 1174)

> 18 existing guards are RED at HEAD, caused by in-range commits dddd09773/c2f199955/48d78d1a5/9c39b8e06 (digest redesign, no 095 task row). c2f199955 removed last_completion from the only reachable table renderer (render_digest_table); render_digest with last_completion is now dead code (never called). Measured: bash scripts/bash/run-tests.sh tests/unit/test_status_digest_unit.py tests/contract/test_efficiency_element.py -q -> 18 failed, 23 passed (10 unit + 8 efficiency), all 18 names present in the reconstructed baseline at c671e168a, so the baseline absorbs them. Attribution: other-line commits, reviewed because they are inside base..head.

<sub>23:14:16</sub>


### 🔴 [BLOCKING] tests/contract/test_status_digest.py (Line 1476)

> C-68 (088 contracts/efficiency-element.contract.md) requires the explicit 'no measurements' state when the store is absent; the text renderer no longer emits it, and this range replaced the guarding assertion ('未找到运行记录存储' in stdout) with a weaker header-prefix check. test_c68_a_nonexistent_store_renders_no_measurements_and_changes_nothing_else is red. The weakening lands in the same range that removes the behaviour, so the guard cannot go red for its subject.

<sub>23:14:18</sub>


### 🟠 [IMPORTANT] scripts/python/status-digest.py (Line 1054)

> C-1 of contracts/status-digest-role-view.contract.md says the materialization is the digest's SINGLE state-read pass, that the legacy line entries and the role view both derive from it, and that no carrier root may be read twice. In the implementation read_state() first calls read_registry() on the registry root and then read_role_materialization() parses the same registry through the engine (_parse_registry); the legacy entries are not derived from the materialization. The guarding test (test_status_digest_roles.py:205) only counts AST call sites in the digest, so it cannot see the second read. Plan D-8 (plan.md:36) repeats the unimplemented clause.

<sub>23:14:25</sub>


### 🟠 [IMPORTANT] scripts/python/status-digest.py (Line 963)

> FR-027/SC-005 interrupted semantics are unreachable for top-level team children. merge_role_entries seeds activity[] with every extra's own running state; the synthetic 'root' executor is an extra with no artifacts, so _executor_state reports it 'running' and activity['root'] is True. A stale child whose parent is 'root' can therefore never be marked interrupted. The only fixture (interrupted/) uses a line-rooted (stalled spine) parent, so the gap is not measured.

<sub>23:14:25</sub>


### 🟠 [IMPORTANT] scripts/python/status-digest.py (Line 897)

> An executor with no artifact set at all is reported state=running / is_active=True forever (no exit record => 'running'), and is never stale, so it sorts first and can never become interrupted. The fanout-10 fixture therefore renders 12 permanently '运行中' rows for a finished team run (test_status_digest_roles.py:328 asserts only the row count). The digest's reader contract ('every row is one live agent execution') is not supported for such rows.

<sub>23:14:25</sub>


### 🟠 [IMPORTANT] tests/contract/test_fast_fail_discipline.py (Line 61)

> CONST_LIVE points at .specify/memory/constitution.md, which does not exist in this repo (the live file is .specify/constitution.md), so test_x4/test_x5 (and x6/x7) fail with FileNotFoundError and are baseline reds. The in-range constitution amendment dd7cbbab4 raises the pin to 1.19.1 but its guard cannot read the file; the amendment's own 'templates requiring updates: check' claim is therefore unverified. Measured: run-tests.sh tests/contract/test_fast_fail_discipline.py -k 'x4 or x5' -> 2 failed (FileNotFoundError).

<sub>23:14:25</sub>


### 🟠 [IMPORTANT] shared/definitions/superagent-definitions.md (Line 74)

> The owner page says the existing pre-dispatch self-check (shared/guidelines/fast-fail.md § 派发前自检) 'requires the role-transition identifier and each item-id slug'. fast-fail.md is untouched in this range and still judges only the fast-fail clause identifier (measured: git log b3da3a26d..HEAD -- shared/guidelines/fast-fail.md -> empty; the file's § 派发前自检 says '自检 outgoing 提示是否已含子句标识'). The extension lives only in skills/internal/run-agent/SKILL.md, so the owner-page attribution names the wrong owner surface.

<sub>23:14:31</sub>


### 🟠 [IMPORTANT] tests/contract/test_superagent_zero_mechanism.py (Line 367)

> The C-3.6 'seeded mutation' is tautological: it appends a copied rule literal to the section text and then asserts the seeded string contains it and the literal. The detection logic (the FORBIDDEN_RULE_LITERALS scan over section/owner) is never run on the seed, so this leg cannot turn red for its subject; the module docstring's 'each leg carries a seeded mutation proving the check is not blind' is not true for this leg.

<sub>23:14:31</sub>


### 🟢 [SUGGESTION] tests/contract/test_role_transition_payload.py (Line 171)

> The delete-one -> blocks drill re-implements the self-check locally (_self_check) and runs it on a pre-mutated fixture; no wired surface or real check is exercised, so the leg stays green if run-agent loses the requirement. The pin is a model of the substring form, not the form's carrier.

<sub>23:14:31</sub>


### 🟢 [SUGGESTION] tests/contract/test_role_edge_engine.py (Line 505)

> The conflict fixture places the disagreeing rows in two team reports with different run stamps (20261110T000000Z vs 20261110T010000Z) — the retry shape data-model §2 forbids for one label — not two different carrier families for the same recorded edge; team rows carry no attempt, so the pinned attempt '1' is the engine default rather than a recorded identity.

<sub>23:14:31</sub>


### 🟢 [SUGGESTION] tests/contract/test_role_edge_engine.py (Line 515)

> The C-2 'error names the offending field' assertion is a tautology: assert 'role' in proc.stderr passes on the program name in every error prefix ('role-edge-check.py: error: ...'), so an error that never names the field stays green.

<sub>23:14:37</sub>


### 🟢 [SUGGESTION] .specify/.gitignore (Line 34)

> Other-line commit 57d364074 adds 'state/' to .specify/.gitignore and de-indexes 30+ tracked state files (5,880 lines), including .specify/state/074-goal-team-sdd-unification.md whose D-074 rulings 6d13938aa had written 11 minutes earlier. The rulings survive in the tracked interview ledger (.specify/memory/session/interview-blocked-stalled-lines-2026-11-10.md), but the 095 state spine and other run ledgers are now disk-only. Reviewed as declared runtime reclassification, not a defect; flagged for the non-disposable review obligation.

<sub>23:14:38</sub>


### 🟢 [SUGGESTION] .specify/specs/095-superagent-role/test-evidence/observation-appendix-check.txt

> The FR-038/SC-010 mechanical check is an ad-hoc script kept at .specify/.tmp/095-appendix-check.py and reproduced only inside this evidence file; nothing guards it from rot, unlike the feature's other claims which have contract modules. The mutation drill's recorded command shows an AssertionError traceback before the mutated-copy reading, which a reader can misread.

<sub>23:14:38</sub>


### 👍 [PRAISE] scripts/python/role-edge-check.py (Line 1)

> The new engine genuinely holds its read-only contract: zero write points (source scan), --help/--version answered before reads, undeclared option exits 2, empty set exits 0 with an explicit summary, four violation fixtures each exit 1, conflict/malformed drills behave per C-2..C-9. Mirror parity, the digest's both-channel role fields and the honest budget leg are likewise well pinned.

<sub>23:14:38</sub>




> **未提交范围（未评审）**: 44 个未提交路径未计入本次评审对象（.claude/agents/reporter.md, .claude/agents/sdd-implement-coordinator.md, .claude/agents/sdd-implement-executor.md, .github/agents/reporter.agent.md, .github/agents/sdd-implement-coordinator.agent.md, .github/agents/sdd-implement-executor.agent.md, .opencode/agents/reporter.md, .opencode/agents/sdd-implement-coordinator.md, .opencode/agents/sdd-implement-executor.md, .qoder/agents/reporter.agent.md, .qoder/agents/sdd-implement-coordinator.agent.md, .qoder/agents/sdd-implement-executor.agent.md, .specify/agents/.render-manifest.json, .specify/memory/session/20261109T084106Z-run-determination-speckit-checklist-093-checklist-a1.md, .specify/memory/session/20261109T084110Z-run-determination-skill-create-checklist-093-checklist-skill.md, .specify/memory/session/interview-blocked-stalled-lines-2026-11-10.dag.json, .specify/memory/session/interview-blocked-stalled-lines-2026-11-10.md, .specify/memory/todo/20261030-suite-speed-optimizations.md, .specify/memory/trigger/index.json, .specify/scripts/bash/check-prerequisites.sh, .specify/scripts/bash/generate-instructions.sh, .specify/scripts/bash/run-tests.sh, .specify/scripts/python/git-workflow-observe.py, .specify/scripts/python/script-interface-check.py, .specify/scripts/python/script_interface_cli.py, .specify/scripts/python/sync-mirrors.py, .specify/source.json, .specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt, .specify/templates/gitignore-specify-template, .specify/workflow/git.md, .specify/memory/exec-quant/records/20261110T024300521548Z-bd97a17c.json, .specify/memory/exec-quant/records/20261110T083604281128Z-1427346f.json, .specify/memory/exec-quant/records/20261110T104159254077Z-6add98fe.json, .specify/memory/exec-quant/records/20261110T121646540994Z-e130beb4.json, .specify/memory/exec-quant/records/20261110T135434742719Z-b232a3d0.json, .specify/memory/feedback/20261110T024300Z-speckit-status.md, .specify/memory/feedback/20261110T083604Z-speckit-status.md, .specify/memory/feedback/20261110T104158Z-skill-sdd-loop-driver.md, .specify/memory/feedback/20261110T121646Z-speckit-status.md, .specify/memory/feedback/20261110T135434Z-speckit-status.md, .specify/memory/session/20261110T104203Z-run-determination-skill-sdd-loop-driver-20261110t092500z-sdd.md, .specify/memory/todo/20261110-sdd-observer-agent.md, .specify/memory/todo/20261110-speckit-migrate-command.md, .specify/specs/095-superagent-role/checkpoints/）；本回执不对该范围给出任何结论。

<!-- coverage-receipt:begin -->
receipt_version=1
base=b3da3a26dfba209057f65c2b17962b9516812c39
head=6c48e9c253166a71ab8364dd818c7d4409471fb5
base_source=feature-first-commit
renderer=text
changed_files=313
judged_files=13
skipped_files=300
gap_files=0
lines_added=26751
lines_deleted=5882
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
file.029.path=.specify/memory/feedback/20261110T060933Z-speckit-requirements.md
file.029.verdict=skipped
file.029.reason=generated
file.030.path=.specify/memory/feedback/20261110T062057Z-speckit-clarify.md
file.030.verdict=skipped
file.030.reason=generated
file.031.path=.specify/memory/feedback/20261110T064500Z-speckit-plan.md
file.031.verdict=skipped
file.031.reason=generated
file.032.path=.specify/memory/feedback/20261110T065439Z-speckit-status.md
file.032.verdict=skipped
file.032.reason=generated
file.033.path=.specify/memory/feedback/20261110T065627Z-skill-coaching-skills.md
file.033.verdict=skipped
file.033.reason=generated
file.034.path=.specify/memory/feedback/20261110T070329Z-speckit-tasks.md
file.034.verdict=skipped
file.034.reason=generated
file.035.path=.specify/memory/feedback/20261110T072029Z-speckit-checklist.md
file.035.verdict=skipped
file.035.reason=generated
file.036.path=.specify/memory/feedback/20261110T072037Z-skill-create-checklist.md
file.036.verdict=skipped
file.036.reason=generated
file.037.path=.specify/memory/feedback/20261110T073148Z-speckit-analyze.md
file.037.verdict=skipped
file.037.reason=generated
file.038.path=.specify/memory/feedback/20261110T073404Z-speckit-analyze.md
file.038.verdict=skipped
file.038.reason=generated
file.039.path=.specify/memory/feedback/20261110T073617Z-speckit-analyze.md
file.039.verdict=skipped
file.039.reason=generated
file.040.path=.specify/memory/feedback/20261110T074703Z-speckit-analyze.md
file.040.verdict=skipped
file.040.reason=generated
file.041.path=.specify/memory/feedback/20261110T080448Z-speckit-analyze.md
file.041.verdict=skipped
file.041.reason=generated
file.042.path=.specify/memory/feedback/20261110T080543Z-speckit-analyze.md
file.042.verdict=skipped
file.042.reason=generated
file.043.path=.specify/memory/feedback/20261110T080814Z-speckit-analyze.md
file.043.verdict=skipped
file.043.reason=generated
file.044.path=.specify/memory/feedback/20261110T081631Z-speckit-analyze.md
file.044.verdict=skipped
file.044.reason=generated
file.045.path=.specify/memory/feedback/20261110T123022Z-speckit-analyze.md
file.045.verdict=skipped
file.045.reason=generated
file.046.path=.specify/memory/feedback/20261110T124514Z-speckit-analyze.md
file.046.verdict=skipped
file.046.reason=generated
file.047.path=.specify/memory/retention/closeout/20261110T061120Z-r20261110T055657Z-b095.json
file.047.verdict=skipped
file.047.reason=generated
file.048.path=.specify/memory/retention/closeout/20261110T062134Z-r20261110T055657Z-b095.json
file.048.verdict=skipped
file.048.reason=generated
file.049.path=.specify/memory/retention/closeout/20261110T064605Z-r20261110T064443Z-b095.json
file.049.verdict=skipped
file.049.reason=generated
file.050.path=.specify/memory/retention/closeout/20261110T070413Z-r20261110T065604Z-b095.json
file.050.verdict=skipped
file.050.reason=generated
file.051.path=.specify/memory/retention/closeout/20261110T072115Z-r20261110T072013Z-b095.json
file.051.verdict=skipped
file.051.reason=generated
file.052.path=.specify/memory/retention/closeout/20261110T074757Z-r20261110T055657Z-b095.json
file.052.verdict=skipped
file.052.reason=generated
file.053.path=.specify/memory/retention/closeout/20261110T081653Z-r20261110T055657Z-b095-r2merge.json
file.053.verdict=skipped
file.053.reason=generated
file.054.path=.specify/memory/retention/closeout/20261110T123105Z-r20261110T055657Z-b095-r3.json
file.054.verdict=skipped
file.054.reason=generated
file.055.path=.specify/memory/retention/closeout/20261110T124538Z-r20261110T055657Z-b095-r4.json
file.055.verdict=skipped
file.055.reason=generated
file.056.path=.specify/memory/session/20261109T074036Z-run-determination-speckit-tasks-r20261109t064500z-092a.md
file.056.verdict=skipped
file.056.reason=generated
file.057.path=.specify/memory/session/20261109T082732Z-run-determination-speckit-tasks-093-tasks-a1.md
file.057.verdict=skipped
file.057.reason=generated
file.058.path=.specify/memory/session/20261110T060918Z-run-determination-speckit-requirements-r20261110t055657z-b09.md
file.058.verdict=skipped
file.058.reason=generated
file.059.path=.specify/memory/session/20261110T062041Z-run-determination-speckit-clarify-r20261110t055657z-b095.md
file.059.verdict=skipped
file.059.reason=generated
file.060.path=.specify/memory/session/20261110T064451Z-run-determination-speckit-plan-r20261110t064443z-b095.md
file.060.verdict=skipped
file.060.reason=generated
file.061.path=.specify/memory/session/20261110T070310Z-run-determination-speckit-tasks-r20261110t065604z-b095.md
file.061.verdict=skipped
file.061.reason=generated
file.062.path=.specify/memory/session/20261110T072013Z-run-determination-speckit-checklist-r20261110t072013z-b095.md
file.062.verdict=skipped
file.062.reason=generated
file.063.path=.specify/memory/session/20261110T072037Z-run-determination-skill-create-checklist-r20261110t072013z-b.md
file.063.verdict=skipped
file.063.reason=generated
file.064.path=.specify/memory/session/20261110T073136Z-run-determination-speckit-analyze-r20261110t055657z-b095-w1.md
file.064.verdict=skipped
file.064.reason=generated
file.065.path=.specify/memory/session/20261110T073354Z-run-determination-speckit-analyze-r20261110t073257z-b095.md
file.065.verdict=skipped
file.065.reason=generated
file.066.path=.specify/memory/session/20261110T073607Z-run-determination-speckit-analyze-r20261110t055657z-b095.md
file.066.verdict=skipped
file.066.reason=generated
file.067.path=.specify/memory/session/20261110T074653Z-run-determination-speckit-analyze-r20261110t055657z-b095-mer.md
file.067.verdict=skipped
file.067.reason=generated
file.068.path=.specify/memory/session/20261110T080438Z-run-determination-speckit-analyze-r20261110t080102z-b095-r2w.md
file.068.verdict=skipped
file.068.reason=generated
file.069.path=.specify/memory/session/20261110T080529Z-run-determination-speckit-analyze-r20261110t055657z-b095-r2w.md
file.069.verdict=skipped
file.069.reason=generated
file.070.path=.specify/memory/session/20261110T080800Z-run-determination-speckit-analyze-r20261110t055657z-b095-r2w.md
file.070.verdict=skipped
file.070.reason=generated
file.071.path=.specify/memory/session/20261110T081631Z-run-determination-speckit-analyze-r20261110t055657z-b095-r2m.md
file.071.verdict=skipped
file.071.reason=generated
file.072.path=.specify/memory/session/20261110T123009Z-run-determination-speckit-analyze-r20261110t055657z-b095-r3.md
file.072.verdict=skipped
file.072.reason=generated
file.073.path=.specify/memory/session/20261110T124504Z-run-determination-speckit-analyze-r20261110t055657z-b095-r4.md
file.073.verdict=skipped
file.073.reason=generated
file.074.path=.specify/memory/session/interview-blocked-stalled-lines-2026-11-10.dag.json
file.074.verdict=skipped
file.074.reason=generated
file.075.path=.specify/memory/session/interview-blocked-stalled-lines-2026-11-10.md
file.075.verdict=skipped
file.075.reason=generated
file.076.path=.specify/scripts/bash/run-tests-shards.sh
file.076.verdict=skipped
file.076.reason=generated
file.077.path=.specify/scripts/python/role-edge-check.py
file.077.verdict=skipped
file.077.reason=generated
file.078.path=.specify/scripts/python/scan-temp-usage.py
file.078.verdict=skipped
file.078.reason=generated
file.079.path=.specify/scripts/python/status-digest.py
file.079.verdict=skipped
file.079.reason=generated
file.080.path=.specify/shared/definitions/agent-definitions.md
file.080.verdict=skipped
file.080.reason=generated
file.081.path=.specify/shared/definitions/framework-map.md
file.081.verdict=skipped
file.081.reason=generated
file.082.path=.specify/shared/definitions/subagent-definitions.md
file.082.verdict=skipped
file.082.reason=generated
file.083.path=.specify/shared/definitions/superagent-definitions.md
file.083.verdict=skipped
file.083.reason=generated
file.084.path=.specify/shared/guidelines/better-harness.md
file.084.verdict=skipped
file.084.reason=generated
file.085.path=.specify/shared/guidelines/confirmation-gates.md
file.085.verdict=skipped
file.085.reason=generated
file.086.path=.specify/skills/internal/create-team/SKILL.md
file.086.verdict=skipped
file.086.reason=generated
file.087.path=.specify/skills/internal/create-team/references/patterns.md
file.087.verdict=skipped
file.087.reason=generated
file.088.path=.specify/skills/internal/run-agent/SKILL.md
file.088.verdict=skipped
file.088.reason=generated
file.089.path=.specify/skills/sdd-loop-driver/SKILL.md
file.089.verdict=skipped
file.089.reason=generated
file.090.path=.specify/skills/sdd-loop-driver/references/dispatch-recipes.md
file.090.verdict=skipped
file.090.reason=generated
file.091.path=.specify/skills/sdd-loop-driver/references/stage-prompts.md
file.091.verdict=skipped
file.091.reason=generated
file.092.path=.specify/specs/095-superagent-role/checklists/requirements-quality-2026-11-10.md
file.092.verdict=skipped
file.092.reason=non-code-file
file.093.path=.specify/specs/095-superagent-role/checklists/requirements.md
file.093.verdict=skipped
file.093.reason=non-code-file
file.094.path=.specify/specs/095-superagent-role/contracts/harness-landing.contract.md
file.094.verdict=skipped
file.094.reason=non-code-file
file.095.path=.specify/specs/095-superagent-role/contracts/role-edge-engine.contract.md
file.095.verdict=skipped
file.095.reason=non-code-file
file.096.path=.specify/specs/095-superagent-role/contracts/role-transition-payload.contract.md
file.096.verdict=skipped
file.096.reason=non-code-file
file.097.path=.specify/specs/095-superagent-role/contracts/status-digest-role-view.contract.md
file.097.verdict=skipped
file.097.reason=non-code-file
file.098.path=.specify/specs/095-superagent-role/coverage-baseline.txt
file.098.verdict=skipped
file.098.reason=non-code-file
file.099.path=.specify/specs/095-superagent-role/data-model.md
file.099.verdict=skipped
file.099.reason=non-code-file
file.100.path=.specify/specs/095-superagent-role/feature-ref.md
file.100.verdict=skipped
file.100.reason=non-code-file
file.101.path=.specify/specs/095-superagent-role/notes/baseline-failed-names.txt
file.101.verdict=skipped
file.101.reason=non-code-file
file.102.path=.specify/specs/095-superagent-role/notes/baseline-provenance.md
file.102.verdict=skipped
file.102.reason=non-code-file
file.103.path=.specify/specs/095-superagent-role/notes/pre-change-measurements.md
file.103.verdict=skipped
file.103.reason=non-code-file
file.104.path=.specify/specs/095-superagent-role/notes/quickstart-run.md
file.104.verdict=skipped
file.104.reason=non-code-file
file.105.path=.specify/specs/095-superagent-role/notes/red-first-evidence.md
file.105.verdict=skipped
file.105.reason=non-code-file
file.106.path=.specify/specs/095-superagent-role/observation-appendix.md
file.106.verdict=skipped
file.106.reason=non-code-file
file.107.path=.specify/specs/095-superagent-role/plan.md
file.107.verdict=skipped
file.107.reason=non-code-file
file.108.path=.specify/specs/095-superagent-role/quickstart.md
file.108.verdict=skipped
file.108.reason=non-code-file
file.109.path=.specify/specs/095-superagent-role/requirements.md
file.109.verdict=skipped
file.109.reason=non-code-file
file.110.path=.specify/specs/095-superagent-role/tasks.md
file.110.verdict=skipped
file.110.reason=non-code-file
file.111.path=.specify/specs/095-superagent-role/test-evidence/analyze-findings-W1.md
file.111.verdict=skipped
file.111.reason=non-code-file
file.112.path=.specify/specs/095-superagent-role/test-evidence/analyze-findings-W2.md
file.112.verdict=skipped
file.112.reason=non-code-file
file.113.path=.specify/specs/095-superagent-role/test-evidence/analyze-findings-W3.md
file.113.verdict=skipped
file.113.reason=non-code-file
file.114.path=.specify/specs/095-superagent-role/test-evidence/analyze-findings-round2-W1.md
file.114.verdict=skipped
file.114.reason=non-code-file
file.115.path=.specify/specs/095-superagent-role/test-evidence/analyze-findings-round2-W2.md
file.115.verdict=skipped
file.115.reason=non-code-file
file.116.path=.specify/specs/095-superagent-role/test-evidence/analyze-findings-round2-W3.md
file.116.verdict=skipped
file.116.reason=non-code-file
file.117.path=.specify/specs/095-superagent-role/test-evidence/analyze-merged-2026-11-10.md
file.117.verdict=skipped
file.117.reason=non-code-file
file.118.path=.specify/specs/095-superagent-role/test-evidence/analyze-merged-r3-2026-11-10.md
file.118.verdict=skipped
file.118.reason=non-code-file
file.119.path=.specify/specs/095-superagent-role/test-evidence/analyze-merged-r4-2026-11-10.md
file.119.verdict=skipped
file.119.reason=non-code-file
file.120.path=.specify/specs/095-superagent-role/test-evidence/analyze-merged-round2-2026-11-10.md
file.120.verdict=skipped
file.120.reason=non-code-file
file.121.path=.specify/specs/095-superagent-role/test-evidence/analyze-repair-dispositions-2026-11-10.md
file.121.verdict=skipped
file.121.reason=non-code-file
file.122.path=.specify/specs/095-superagent-role/test-evidence/analyze-repair-dispositions-r3-2026-11-10.md
file.122.verdict=skipped
file.122.reason=non-code-file
file.123.path=.specify/specs/095-superagent-role/test-evidence/analyze-repair-dispositions-r4-2026-11-10.md
file.123.verdict=skipped
file.123.reason=non-code-file
file.124.path=.specify/specs/095-superagent-role/test-evidence/analyze-repair-gates-2026-11-10.txt
file.124.verdict=skipped
file.124.reason=non-code-file
file.125.path=.specify/specs/095-superagent-role/test-evidence/analyze-repair-gates-r3-2026-11-10.txt
file.125.verdict=skipped
file.125.reason=non-code-file
file.126.path=.specify/specs/095-superagent-role/test-evidence/analyze-repair-gates-r4-2026-11-10.txt
file.126.verdict=skipped
file.126.reason=non-code-file
file.127.path=.specify/specs/095-superagent-role/test-evidence/analyze-wrapup-exec-quant.txt
file.127.verdict=skipped
file.127.reason=non-code-file
file.128.path=.specify/specs/095-superagent-role/test-evidence/analyze-wrapup-feedback.txt
file.128.verdict=skipped
file.128.reason=non-code-file
file.129.path=.specify/specs/095-superagent-role/test-evidence/analyze-wrapup-run-determination.txt
file.129.verdict=skipped
file.129.reason=non-code-file
file.130.path=.specify/specs/095-superagent-role/test-evidence/checklist-readings-2026-11-10.txt
file.130.verdict=skipped
file.130.reason=non-code-file
file.131.path=.specify/specs/095-superagent-role/test-evidence/checklist-wrapup-exec-quant-skill.txt
file.131.verdict=skipped
file.131.reason=non-code-file
file.132.path=.specify/specs/095-superagent-role/test-evidence/checklist-wrapup-exec-quant.txt
file.132.verdict=skipped
file.132.reason=non-code-file
file.133.path=.specify/specs/095-superagent-role/test-evidence/checklist-wrapup-feedback-skill.txt
file.133.verdict=skipped
file.133.reason=non-code-file
file.134.path=.specify/specs/095-superagent-role/test-evidence/checklist-wrapup-feedback.txt
file.134.verdict=skipped
file.134.reason=non-code-file
file.135.path=.specify/specs/095-superagent-role/test-evidence/checklist-wrapup-run-determination-skill.txt
file.135.verdict=skipped
file.135.reason=non-code-file
file.136.path=.specify/specs/095-superagent-role/test-evidence/checklist-wrapup-run-determination.txt
file.136.verdict=skipped
file.136.reason=non-code-file
file.137.path=.specify/specs/095-superagent-role/test-evidence/clarify-flow-class.txt
file.137.verdict=skipped
file.137.reason=non-code-file
file.138.path=.specify/specs/095-superagent-role/test-evidence/clarify-overlap-check.json
file.138.verdict=skipped
file.138.reason=non-code-file
file.139.path=.specify/specs/095-superagent-role/test-evidence/clarify-overlap-check.txt
file.139.verdict=skipped
file.139.reason=non-code-file
file.140.path=.specify/specs/095-superagent-role/test-evidence/clarify-validate-requirements.txt
file.140.verdict=skipped
file.140.reason=non-code-file
file.141.path=.specify/specs/095-superagent-role/test-evidence/clarify-wrapup-exec-quant.txt
file.141.verdict=skipped
file.141.reason=non-code-file
file.142.path=.specify/specs/095-superagent-role/test-evidence/clarify-wrapup-feedback.txt
file.142.verdict=skipped
file.142.reason=non-code-file
file.143.path=.specify/specs/095-superagent-role/test-evidence/clarify-wrapup-run-determination.txt
file.143.verdict=skipped
file.143.reason=non-code-file
file.144.path=.specify/specs/095-superagent-role/test-evidence/closure-acceptance.txt
file.144.verdict=skipped
file.144.reason=non-code-file
file.145.path=.specify/specs/095-superagent-role/test-evidence/closure-suite-comparison.txt
file.145.verdict=skipped
file.145.reason=non-code-file
file.146.path=.specify/specs/095-superagent-role/test-evidence/closure-suite-names.txt
file.146.verdict=skipped
file.146.reason=non-code-file
file.147.path=.specify/specs/095-superagent-role/test-evidence/closure-suite.txt
file.147.verdict=skipped
file.147.reason=non-code-file
file.148.path=.specify/specs/095-superagent-role/test-evidence/concurrency-invariants.txt
file.148.verdict=skipped
file.148.reason=non-code-file
file.149.path=.specify/specs/095-superagent-role/test-evidence/concurrency-wave-readings.txt
file.149.verdict=skipped
file.149.reason=non-code-file
file.150.path=.specify/specs/095-superagent-role/test-evidence/definitions-readings.txt
file.150.verdict=skipped
file.150.reason=non-code-file
file.151.path=.specify/specs/095-superagent-role/test-evidence/gate-checks.txt
file.151.verdict=skipped
file.151.reason=non-code-file
file.152.path=.specify/specs/095-superagent-role/test-evidence/instructions-budget.txt
file.152.verdict=skipped
file.152.reason=non-code-file
file.153.path=.specify/specs/095-superagent-role/test-evidence/mirror-obligations.txt
file.153.verdict=skipped
file.153.reason=non-code-file
file.154.path=.specify/specs/095-superagent-role/test-evidence/observation-appendix-check.txt
file.154.verdict=skipped
file.154.reason=non-code-file
file.155.path=.specify/specs/095-superagent-role/test-evidence/plan-gate.txt
file.155.verdict=skipped
file.155.reason=non-code-file
file.156.path=.specify/specs/095-superagent-role/test-evidence/plan-stage-evidence.md
file.156.verdict=skipped
file.156.reason=non-code-file
file.157.path=.specify/specs/095-superagent-role/test-evidence/plan-wrapup-exec-quant.txt
file.157.verdict=skipped
file.157.reason=non-code-file
file.158.path=.specify/specs/095-superagent-role/test-evidence/plan-wrapup-feedback.txt
file.158.verdict=skipped
file.158.reason=non-code-file
file.159.path=.specify/specs/095-superagent-role/test-evidence/plan-wrapup-run-determination.txt
file.159.verdict=skipped
file.159.reason=non-code-file
file.160.path=.specify/specs/095-superagent-role/test-evidence/requirements-flow-class.txt
file.160.verdict=skipped
file.160.reason=non-code-file
file.161.path=.specify/specs/095-superagent-role/test-evidence/requirements-glossary-add.txt
file.161.verdict=skipped
file.161.reason=non-code-file
file.162.path=.specify/specs/095-superagent-role/test-evidence/requirements-glossary-conflict.txt
file.162.verdict=skipped
file.162.reason=non-code-file
file.163.path=.specify/specs/095-superagent-role/test-evidence/requirements-validator-initial.txt
file.163.verdict=skipped
file.163.reason=non-code-file
file.164.path=.specify/specs/095-superagent-role/test-evidence/requirements-validator.txt
file.164.verdict=skipped
file.164.reason=non-code-file
file.165.path=.specify/specs/095-superagent-role/test-evidence/role-edge-engine-readings.txt
file.165.verdict=skipped
file.165.reason=non-code-file
file.166.path=.specify/specs/095-superagent-role/test-evidence/role-transition-readings.txt
file.166.verdict=skipped
file.166.reason=non-code-file
file.167.path=.specify/specs/095-superagent-role/test-evidence/smoke-six-modules.txt
file.167.verdict=skipped
file.167.reason=non-code-file
file.168.path=.specify/specs/095-superagent-role/test-evidence/state-sync-recovery.txt
file.168.verdict=skipped
file.168.reason=non-code-file
file.169.path=.specify/specs/095-superagent-role/test-evidence/status-digest-roles-readings.txt
file.169.verdict=skipped
file.169.reason=non-code-file
file.170.path=.specify/specs/095-superagent-role/test-evidence/tasks-decomposition-check.txt
file.170.verdict=skipped
file.170.reason=non-code-file
file.171.path=.specify/specs/095-superagent-role/test-evidence/tasks-flow-class.txt
file.171.verdict=skipped
file.171.reason=non-code-file
file.172.path=.specify/specs/095-superagent-role/test-evidence/tasks-pre-analyze-check.txt
file.172.verdict=skipped
file.172.reason=non-code-file
file.173.path=.specify/specs/095-superagent-role/test-evidence/tasks-stage-evidence.md
file.173.verdict=skipped
file.173.reason=non-code-file
file.174.path=.specify/specs/095-superagent-role/test-evidence/tasks-validate.txt
file.174.verdict=skipped
file.174.reason=non-code-file
file.175.path=.specify/specs/095-superagent-role/test-evidence/tasks-wrapup-exec-quant.txt
file.175.verdict=skipped
file.175.reason=non-code-file
file.176.path=.specify/specs/095-superagent-role/test-evidence/tasks-wrapup-feedback.txt
file.176.verdict=skipped
file.176.reason=non-code-file
file.177.path=.specify/specs/095-superagent-role/test-evidence/tasks-wrapup-run-determination.txt
file.177.verdict=skipped
file.177.reason=non-code-file
file.178.path=.specify/specs/095-superagent-role/test-evidence/three-forms-readings.txt
file.178.verdict=skipped
file.178.reason=non-code-file
file.179.path=.specify/specs/095-superagent-role/test-evidence/validate-tasks.txt
file.179.verdict=skipped
file.179.reason=non-code-file
file.180.path=.specify/specs/095-superagent-role/test-evidence/wrapup-exec-quant.txt
file.180.verdict=skipped
file.180.reason=non-code-file
file.181.path=.specify/specs/095-superagent-role/test-evidence/wrapup-feedback.txt
file.181.verdict=skipped
file.181.reason=non-code-file
file.182.path=.specify/specs/095-superagent-role/test-evidence/wrapup-run-determination.txt
file.182.verdict=skipped
file.182.reason=non-code-file
file.183.path=.specify/specs/095-superagent-role/test-evidence/zero-mechanism-baseline-names.txt
file.183.verdict=skipped
file.183.reason=non-code-file
file.184.path=.specify/specs/095-superagent-role/test-evidence/zero-mechanism-current-names.txt
file.184.verdict=skipped
file.184.reason=non-code-file
file.185.path=.specify/specs/095-superagent-role/test-evidence/zero-mechanism-readings.txt
file.185.verdict=skipped
file.185.reason=non-code-file
file.186.path=.specify/specs/095-superagent-role/verification.md
file.186.verdict=skipped
file.186.reason=non-code-file
file.187.path=.specify/state/074-goal-team-sdd-unification.md
file.187.verdict=skipped
file.187.reason=generated
file.188.path=.specify/state/074b-nested-governance.md
file.188.verdict=skipped
file.188.reason=generated
file.189.path=.specify/state/076-decision-tension-contract.md
file.189.verdict=skipped
file.189.reason=generated
file.190.path=.specify/state/077-doc-sdd-integration.md
file.190.verdict=skipped
file.190.reason=generated
file.191.path=.specify/state/078-bilingual-expression.md
file.191.verdict=skipped
file.191.reason=generated
file.192.path=.specify/state/078-coaching-skills.md
file.192.verdict=skipped
file.192.reason=generated
file.193.path=.specify/state/079-humanize-run-output.md
file.193.verdict=skipped
file.193.reason=generated
file.194.path=.specify/state/081-acceptance-hardening.md
file.194.verdict=skipped
file.194.reason=generated
file.195.path=.specify/state/082-self-explanatory-integration.md
file.195.verdict=skipped
file.195.reason=generated
file.196.path=.specify/state/083-budget-calibration-tests.txt
file.196.verdict=skipped
file.196.reason=generated
file.197.path=.specify/state/083-budget-calibration.md
file.197.verdict=skipped
file.197.reason=generated
file.198.path=.specify/state/083-loop-state-self-test.txt
file.198.verdict=skipped
file.198.reason=generated
file.199.path=.specify/state/083-mechanism-policy-separation.md
file.199.verdict=skipped
file.199.reason=generated
file.200.path=.specify/state/084-harness-triple-structure.md
file.200.verdict=skipped
file.200.reason=generated
file.201.path=.specify/state/086-efficient-test-execution.md
file.201.verdict=skipped
file.201.reason=generated
file.202.path=.specify/state/087-arch-diagram-docs.md
file.202.verdict=skipped
file.202.reason=generated
file.203.path=.specify/state/088-speckit-visualization.md
file.203.verdict=skipped
file.203.reason=generated
file.204.path=.specify/state/089-script-interface-contract.md
file.204.verdict=skipped
file.204.reason=generated
file.205.path=.specify/state/090-re-anchoring.md
file.205.verdict=skipped
file.205.reason=generated
file.206.path=.specify/state/091-auto-git-closeout.md
file.206.verdict=skipped
file.206.reason=generated
file.207.path=.specify/state/092-non-disposable.md
file.207.verdict=skipped
file.207.reason=generated
file.208.path=.specify/state/093-concurrency-by-default.md
file.208.verdict=skipped
file.208.reason=generated
file.209.path=.specify/state/094-goal-team-parallel.md
file.209.verdict=skipped
file.209.reason=generated
file.210.path=.specify/state/eval-baseline/README.md
file.210.verdict=skipped
file.210.reason=generated
file.211.path=.specify/state/eval-baseline/instructions.md
file.211.verdict=skipped
file.211.reason=generated
file.212.path=.specify/state/speckit-docs-expression.md
file.212.verdict=skipped
file.212.reason=generated
file.213.path=.specify/state/wp/088-speckit-visualization-implement-a1-gate-plan.json
file.213.verdict=skipped
file.213.reason=generated
file.214.path=.specify/state/wp/088-speckit-visualization-implement-a2-gate-plan.json
file.214.verdict=skipped
file.214.reason=generated
file.215.path=.specify/state/wp/088-speckit-visualization-plan-a1-gate-plan.json
file.215.verdict=skipped
file.215.reason=generated
file.216.path=.specify/state/wp/088-speckit-visualization-plan-a2-gate-plan.json
file.216.verdict=skipped
file.216.reason=generated
file.217.path=.specify/templates/instructions-template.md
file.217.verdict=skipped
file.217.reason=generated
file.218.path=scripts/bash/run-tests-shards.sh
file.218.verdict=reviewed
file.219.path=scripts/python/role-edge-check.py
file.219.verdict=reviewed
file.220.path=scripts/python/scan-temp-usage.py
file.220.verdict=reviewed
file.221.path=scripts/python/status-digest.py
file.221.verdict=reviewed
file.222.path=shared/definitions/agent-definitions.md
file.222.verdict=skipped
file.222.reason=non-code-file
file.223.path=shared/definitions/framework-map.md
file.223.verdict=skipped
file.223.reason=non-code-file
file.224.path=shared/definitions/subagent-definitions.md
file.224.verdict=skipped
file.224.reason=non-code-file
file.225.path=shared/definitions/superagent-definitions.md
file.225.verdict=skipped
file.225.reason=non-code-file
file.226.path=shared/guidelines/better-harness.md
file.226.verdict=skipped
file.226.reason=non-code-file
file.227.path=shared/guidelines/confirmation-gates.md
file.227.verdict=skipped
file.227.reason=non-code-file
file.228.path=skills/external/sdd-loop-driver/SKILL.md
file.228.verdict=skipped
file.228.reason=non-code-file
file.229.path=skills/external/sdd-loop-driver/references/dispatch-recipes.md
file.229.verdict=skipped
file.229.reason=non-code-file
file.230.path=skills/external/sdd-loop-driver/references/stage-prompts.md
file.230.verdict=skipped
file.230.reason=non-code-file
file.231.path=skills/internal/create-team/SKILL.md
file.231.verdict=skipped
file.231.reason=non-code-file
file.232.path=skills/internal/create-team/references/patterns.md
file.232.verdict=skipped
file.232.reason=non-code-file
file.233.path=skills/internal/run-agent/SKILL.md
file.233.verdict=skipped
file.233.reason=non-code-file
file.234.path=templates/gitignore-specify-template
file.234.verdict=skipped
file.234.reason=non-code-file
file.235.path=templates/instructions-template.md
file.235.verdict=skipped
file.235.reason=non-code-file
file.236.path=tests/contract/test_fast_fail_discipline.py
file.236.verdict=reviewed
file.237.path=tests/contract/test_instructions_budget_superagent_section.py
file.237.verdict=reviewed
file.238.path=tests/contract/test_role_edge_engine.py
file.238.verdict=reviewed
file.239.path=tests/contract/test_role_transition_payload.py
file.239.verdict=reviewed
file.240.path=tests/contract/test_specify_gitignore_template.py
file.240.verdict=reviewed
file.241.path=tests/contract/test_status_digest.py
file.241.verdict=reviewed
file.242.path=tests/contract/test_status_digest_roles.py
file.242.verdict=reviewed
file.243.path=tests/contract/test_superagent_definitions.py
file.243.verdict=reviewed
file.244.path=tests/contract/test_superagent_zero_mechanism.py
file.244.verdict=reviewed
file.245.path=tests/fixtures/superagent-role/conflict/logs/.gitkeep
file.245.verdict=skipped
file.245.reason=non-code-file
file.246.path=tests/fixtures/superagent-role/conflict/registry/.gitkeep
file.246.verdict=skipped
file.246.reason=non-code-file
file.247.path=tests/fixtures/superagent-role/conflict/state/.gitkeep
file.247.verdict=skipped
file.247.reason=non-code-file
file.248.path=tests/fixtures/superagent-role/conflict/teams/conflict-team/runs/20261110T000000Z-report.md
file.248.verdict=skipped
file.248.reason=non-code-file
file.249.path=tests/fixtures/superagent-role/conflict/teams/conflict-team/runs/20261110T010000Z-report.md
file.249.verdict=skipped
file.249.reason=non-code-file
file.250.path=tests/fixtures/superagent-role/empty/logs/.gitkeep
file.250.verdict=skipped
file.250.reason=non-code-file
file.251.path=tests/fixtures/superagent-role/empty/registry/.gitkeep
file.251.verdict=skipped
file.251.reason=non-code-file
file.252.path=tests/fixtures/superagent-role/empty/state/.gitkeep
file.252.verdict=skipped
file.252.reason=non-code-file
file.253.path=tests/fixtures/superagent-role/empty/teams/.gitkeep
file.253.verdict=skipped
file.253.reason=non-code-file
file.254.path=tests/fixtures/superagent-role/fanout-10/logs/.gitkeep
file.254.verdict=skipped
file.254.reason=non-code-file
file.255.path=tests/fixtures/superagent-role/fanout-10/registry/.gitkeep
file.255.verdict=skipped
file.255.reason=non-code-file
file.256.path=tests/fixtures/superagent-role/fanout-10/state/.gitkeep
file.256.verdict=skipped
file.256.reason=non-code-file
file.257.path=tests/fixtures/superagent-role/fanout-10/teams/fanout-team/runs/20261110T000000Z-report.md
file.257.verdict=skipped
file.257.reason=non-code-file
file.258.path=tests/fixtures/superagent-role/interrupted/logs/child-1.jsonl
file.258.verdict=skipped
file.258.reason=non-code-file
file.259.path=tests/fixtures/superagent-role/interrupted/logs/child-1.status
file.259.verdict=skipped
file.259.reason=non-code-file
file.260.path=tests/fixtures/superagent-role/interrupted/registry/demo-line.json
file.260.verdict=skipped
file.260.reason=non-code-file
file.261.path=tests/fixtures/superagent-role/interrupted/state/demo-line.md
file.261.verdict=skipped
file.261.reason=non-code-file
file.262.path=tests/fixtures/superagent-role/interrupted/teams/interrupted-team/runs/20261110T000000Z-report.md
file.262.verdict=skipped
file.262.reason=non-code-file
file.263.path=tests/fixtures/superagent-role/local-team/logs/alice.jsonl
file.263.verdict=skipped
file.263.reason=non-code-file
file.264.path=tests/fixtures/superagent-role/local-team/logs/alice.status
file.264.verdict=skipped
file.264.reason=non-code-file
file.265.path=tests/fixtures/superagent-role/local-team/logs/bob.jsonl
file.265.verdict=skipped
file.265.reason=non-code-file
file.266.path=tests/fixtures/superagent-role/local-team/logs/bob.status
file.266.verdict=skipped
file.266.reason=non-code-file
file.267.path=tests/fixtures/superagent-role/local-team/logs/carol.jsonl
file.267.verdict=skipped
file.267.reason=non-code-file
file.268.path=tests/fixtures/superagent-role/local-team/logs/carol.status
file.268.verdict=skipped
file.268.reason=non-code-file
file.269.path=tests/fixtures/superagent-role/local-team/registry/.gitkeep
file.269.verdict=skipped
file.269.reason=non-code-file
file.270.path=tests/fixtures/superagent-role/local-team/state/.gitkeep
file.270.verdict=skipped
file.270.reason=non-code-file
file.271.path=tests/fixtures/superagent-role/local-team/teams/local-team/runs/20261110T000000Z-report.md
file.271.verdict=skipped
file.271.reason=non-code-file
file.272.path=tests/fixtures/superagent-role/malformed/logs/.gitkeep
file.272.verdict=skipped
file.272.reason=non-code-file
file.273.path=tests/fixtures/superagent-role/malformed/registry/.gitkeep
file.273.verdict=skipped
file.273.reason=non-code-file
file.274.path=tests/fixtures/superagent-role/malformed/state/.gitkeep
file.274.verdict=skipped
file.274.reason=non-code-file
file.275.path=tests/fixtures/superagent-role/malformed/teams/malformed-team/runs/20261110T000000Z-report.md
file.275.verdict=skipped
file.275.reason=non-code-file
file.276.path=tests/fixtures/superagent-role/payload/role-fields.md
file.276.verdict=skipped
file.276.reason=non-code-file
file.277.path=tests/fixtures/superagent-role/payload/role-transition-complete.md
file.277.verdict=skipped
file.277.reason=non-code-file
file.278.path=tests/fixtures/superagent-role/payload/role-transition-missing-item.md
file.278.verdict=skipped
file.278.reason=non-code-file
file.279.path=tests/fixtures/superagent-role/payload/role-transition-skill-load.md
file.279.verdict=skipped
file.279.reason=non-code-file
file.280.path=tests/fixtures/superagent-role/remote-topology/logs/remote--20261110T000000Z--worker.jsonl
file.280.verdict=skipped
file.280.reason=non-code-file
file.281.path=tests/fixtures/superagent-role/remote-topology/logs/remote--20261110T000000Z--worker.status
file.281.verdict=skipped
file.281.reason=non-code-file
file.282.path=tests/fixtures/superagent-role/remote-topology/memory/exec-quant/records/20261110T000000000000Z-fixture01.json
file.282.verdict=skipped
file.282.reason=non-code-file
file.283.path=tests/fixtures/superagent-role/remote-topology/registry/remote-builder.json
file.283.verdict=skipped
file.283.reason=non-code-file
file.284.path=tests/fixtures/superagent-role/remote-topology/state/.gitkeep
file.284.verdict=skipped
file.284.reason=non-code-file
file.285.path=tests/fixtures/superagent-role/remote-topology/teams/.gitkeep
file.285.verdict=skipped
file.285.reason=non-code-file
file.286.path=tests/fixtures/superagent-role/root-a-b/logs/A.jsonl
file.286.verdict=skipped
file.286.reason=non-code-file
file.287.path=tests/fixtures/superagent-role/root-a-b/logs/A.status
file.287.verdict=skipped
file.287.reason=non-code-file
file.288.path=tests/fixtures/superagent-role/root-a-b/logs/B.jsonl
file.288.verdict=skipped
file.288.reason=non-code-file
file.289.path=tests/fixtures/superagent-role/root-a-b/logs/B.status
file.289.verdict=skipped
file.289.reason=non-code-file
file.290.path=tests/fixtures/superagent-role/root-a-b/registry/demo-line.json
file.290.verdict=skipped
file.290.reason=non-code-file
file.291.path=tests/fixtures/superagent-role/root-a-b/state/demo-line.md
file.291.verdict=skipped
file.291.reason=non-code-file
file.292.path=tests/fixtures/superagent-role/root-a-b/state/prompt-B-s1.md.meta.json
file.292.verdict=skipped
file.292.reason=non-code-file
file.293.path=tests/fixtures/superagent-role/root-a-b/teams/demo-team/runs/20261110T000000Z-report.md
file.293.verdict=skipped
file.293.reason=non-code-file
file.294.path=tests/fixtures/superagent-role/violations/dangling-parent/logs/.gitkeep
file.294.verdict=skipped
file.294.reason=non-code-file
file.295.path=tests/fixtures/superagent-role/violations/dangling-parent/registry/.gitkeep
file.295.verdict=skipped
file.295.reason=non-code-file
file.296.path=tests/fixtures/superagent-role/violations/dangling-parent/state/.gitkeep
file.296.verdict=skipped
file.296.reason=non-code-file
file.297.path=tests/fixtures/superagent-role/violations/dangling-parent/teams/.gitkeep
file.297.verdict=skipped
file.297.reason=non-code-file
file.298.path=tests/fixtures/superagent-role/violations/dangling-parent/teams/dangling-team/runs/20261110T000000Z-report.md
file.298.verdict=skipped
file.298.reason=non-code-file
file.299.path=tests/fixtures/superagent-role/violations/depth-cycle/logs/.gitkeep
file.299.verdict=skipped
file.299.reason=non-code-file
file.300.path=tests/fixtures/superagent-role/violations/depth-cycle/registry/.gitkeep
file.300.verdict=skipped
file.300.reason=non-code-file
file.301.path=tests/fixtures/superagent-role/violations/depth-cycle/state/.gitkeep
file.301.verdict=skipped
file.301.reason=non-code-file
file.302.path=tests/fixtures/superagent-role/violations/depth-cycle/teams/.gitkeep
file.302.verdict=skipped
file.302.reason=non-code-file
file.303.path=tests/fixtures/superagent-role/violations/depth-cycle/teams/cycle-team/runs/20261110T000000Z-report.md
file.303.verdict=skipped
file.303.reason=non-code-file
file.304.path=tests/fixtures/superagent-role/violations/self-dispatch/logs/.gitkeep
file.304.verdict=skipped
file.304.reason=non-code-file
file.305.path=tests/fixtures/superagent-role/violations/self-dispatch/registry/.gitkeep
file.305.verdict=skipped
file.305.reason=non-code-file
file.306.path=tests/fixtures/superagent-role/violations/self-dispatch/state/.gitkeep
file.306.verdict=skipped
file.306.reason=non-code-file
file.307.path=tests/fixtures/superagent-role/violations/self-dispatch/teams/.gitkeep
file.307.verdict=skipped
file.307.reason=non-code-file
file.308.path=tests/fixtures/superagent-role/violations/self-dispatch/teams/self-team/runs/20261110T000000Z-report.md
file.308.verdict=skipped
file.308.reason=non-code-file
file.309.path=tests/fixtures/superagent-role/violations/unbacked-claim/logs/.gitkeep
file.309.verdict=skipped
file.309.reason=non-code-file
file.310.path=tests/fixtures/superagent-role/violations/unbacked-claim/registry/.gitkeep
file.310.verdict=skipped
file.310.reason=non-code-file
file.311.path=tests/fixtures/superagent-role/violations/unbacked-claim/state/.gitkeep
file.311.verdict=skipped
file.311.reason=non-code-file
file.312.path=tests/fixtures/superagent-role/violations/unbacked-claim/teams/.gitkeep
file.312.verdict=skipped
file.312.reason=non-code-file
file.313.path=tests/fixtures/superagent-role/violations/unbacked-claim/teams/claim-team/runs/20261110T000000Z-report.md
file.313.verdict=skipped
file.313.reason=non-code-file
<!-- coverage-receipt:end -->
