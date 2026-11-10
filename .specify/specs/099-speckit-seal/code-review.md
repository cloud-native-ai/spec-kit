# Code Review Report — 代码段 (code segment)

| 属性 | 值 |
|------|-----|
| **分支** | `099-speckit-seal` |
| **基准** | `b3da3a26dfba209057f65c2b17962b9516812c39` (`b3da3a26d`) |
| **目标** | `55dd6d61dddd2ed529cbbd61dc3c3e966b470988` (`55dd6d61d`) |
| **基准来源** | `feature-first-commit` |
| **渲染模式** | `renderer: text` |
| **Reviewer** | `Qiming Liu (John)` |
| **日期** | `2026-11-10T19:05:04Z` |

## 变更概览

```
 .claude/commands/speckit.seal.md                   |   43 +
 .github/prompts/speckit.seal.prompt.md             |   43 +
 .opencode/command/speckit.seal.md                  |   43 +
 .qoder/commands/speckit.seal.md                    |   46 +
 .specify/constitution.md                           |   34 +-
 .specify/features.md                               |    5 +-
 .specify/features/099-speckit-seal.md              |   70 +
 .specify/glossary.md                               |    4 +
 .../records/20261110T122415340717Z-68288034.json   |    1 +
 .../records/20261110T123300407905Z-1fa74f99.json   |    1 +
 .../records/20261110T131540636283Z-d51fb7cb.json   |    1 +
 .../records/20261110T134514589152Z-7ddd0b1b.json   |    1 +
 .../records/20261110T135735902193Z-b8758b49.json   |    1 +
 .../records/20261110T140712289140Z-b5a8bb50.json   |    1 +
 .../records/20261110T142455961221Z-c5e27bc2.json   |    1 +
 .../records/20261110T150505512980Z-508bec9b.json   |    1 +
 .../records/20261110T183846975285Z-15becc33.json   |    1 +
 .../records/20261110T183847312664Z-060dbeab.json   |    1 +
 .../records/20261110T183847647164Z-cfe900b3.json   |    1 +
 .../records/20261110T183847980886Z-50cfe662.json   |    1 +
 .../20261110T122417Z-speckit-requirements.md       |   23 +
 .../feedback/20261110T123320Z-speckit-clarify.md   |   23 +
 .../feedback/20261110T131542Z-speckit-plan.md      |   23 +
 .../feedback/20261110T134640Z-speckit-tasks.md     |   22 +
 .../feedback/20261110T135746Z-speckit-checklist.md |   21 +
 .../feedback/20261110T140722Z-speckit-analyze.md   |   19 +
 .../feedback/20261110T142511Z-speckit-analyze.md   |   19 +
 .../feedback/20261110T150505Z-speckit-analyze.md   |   19 +
 .../feedback/20261110T183906Z-speckit-review.md    |   21 +
 .../feedback/20261110T183913Z-skill-code-review.md |   21 +
 ...0261110T183913Z-skill-review-feature-quality.md |   21 +
 .../20261110T183913Z-skill-review-sdd-process.md   |   21 +
 ...261110T122515Z-099-speckit-seal-requirements.md |   24 +
 .../20261110T123338Z-099-speckit-seal-clarify.md   |   25 +
 .../20261110T131622Z-099-speckit-seal-plan.md      |   31 +
 .../20261110T134741Z-099-speckit-seal-tasks.md     |   31 +
 .../20261110T135818Z-099-speckit-seal-checklist.md |   36 +
 .../20261110T140740Z-099-speckit-seal-analyze.md   |   37 +
 ...20261110T142547Z-099-speckit-seal-analyze-r2.md |   42 +
 ...20261110T150529Z-099-speckit-seal-analyze-r3.md |   44 +
 .../20261110T184022Z-099-speckit-seal-review.md    |   58 +
 ...nation-speckit-review-r20261106t040353z-087a.md |   34 +-
 ...n-skill-code-review-r20261106t105429z-087rev.md |   31 +-
 ...nation-speckit-review-r20261108t220214z-8647.md |   14 +-
 ...n-skill-review-feature-quality-r20261109t023.md |   31 +-
 ...n-skill-review-sdd-process-r20261109t023000z.md |   31 +-
 ...determination-speckit-clarify-093-clarify-a1.md |   10 +-
 ...on-speckit-analyze-r20261109t090000z-analyze.md |   10 +-
 ...n-speckit-requirements-r20261110t121314z-b09.md |  202 +
 ...ation-speckit-clarify-r20261110t121314z-b099.md |  202 +
 ...mination-speckit-plan-r20261110t121314z-b099.md |  209 +
 ...ination-speckit-tasks-r20261110t121314z-b099.md |  202 +
 ...ion-speckit-checklist-r20261110t121314z-b099.md |  200 +
 ...ation-speckit-analyze-r20261110t121314z-b099.md |  200 +
 ...n-speckit-analyze-r20261110t142432z-099-anal.md |  200 +
 ...n-speckit-analyze-r20261110t150457z-099-anal.md |  200 +
 ...n-speckit-review-r20261110t183510z-099-revie.md |  202 +
 ...n-skill-review-feature-quality-r20261110t183.md |  202 +
 ...n-skill-review-sdd-process-r20261110t183510z.md |  202 +
 ...n-skill-code-review-r20261110t183510z-099-re.md |  202 +
 .specify/register.md                               |    6 +
 .specify/scripts/python/account-clause-coverage.py |    5 +-
 .../scripts/python/closure-acceptance-check.py     |    6 +-
 .specify/scripts/python/non-disposable-check.py    |    7 +-
 .specify/scripts/python/seal-utils.py              | 3049 +++++++
 .specify/scripts/python/validate-tasks.py          |   49 +-
 .../shared/definitions/flow-class-definitions.md   |    4 +-
 .../definitions/non-disposable-definitions.md      |    5 +-
 .specify/shared/definitions/probe-definitions.md   |    2 +
 .../shared/definitions/sdd-routing-definitions.md  |    8 +-
 .../shared/definitions/subagent-definitions.md     |    2 +-
 .specify/shared/guidelines/better-harness.md       |    4 +-
 .specify/shared/workflow/acceptance-hardening.md   |   53 +-
 .specify/shared/workflow/expression-gates.md       |    2 +-
 .specify/shared/workflow/feature-integration.md    |    8 +-
 .specify/skills/internal/create-team/SKILL.md      |    4 +-
 .../skills/internal/create-team/references/goal.md |    2 +-
 .specify/skills/internal/manage-features/SKILL.md  |   25 +-
 .../skills/internal/sanitize-materials/SKILL.md    |   17 +
 .specify/skills/internal/seal-artifact/SKILL.md    |  104 +
 .specify/skills/sdd-loop-driver/SKILL.md           |    2 +-
 .../references/decomposition-model.md              |    2 +-
 .../references/nested-invocation.md                |    6 +-
 .../contracts/command-classification.md            |    6 +-
 .../checklists/readiness-2026-10-29.md             |  264 +
 .../recheck-2026-10-29-implement-start.md          |   54 +
 .../checklists/requirements.md                     |  166 +
 .../074-goal-team-sdd-unification/code-review.md   |    4 +
 .../contracts/bootstrap-and-maintenance.md         |   54 +
 .../contracts/compat-and-safety.md                 |  109 +
 .../contracts/diffusion.md                         |   81 +
 .../contracts/hierarchy-and-authorization.md       |  155 +
 .../contracts/nested-invocation.md                 |   14 +
 .../contracts/report-and-attribution.md            |   11 +
 .../contracts/routing-decision.md                  |  153 +
 .../074-goal-team-sdd-unification/feature-ref.md   |   18 +
 .../merge-manifest.json                            | 3774 ++++++++
 .../notes/closure-full-run-2.txt                   | 2039 +++++
 .../notes/closure-full-run-3.txt                   |  998 ++
 .../notes/closure-full-run.txt                     | 2243 +++++
 .../notes/full-baseline-run.txt                    | 1059 +++
 .../notes/golden-rows.txt                          |   17 +
 .../notes/golden-run1.json                         |  375 +
 .../notes/golden-run2.json                         |  375 +
 .../notes/green-t016-demo.txt                      |  101 +
 .../notes/green-t016.txt                           |    4 +
 .../notes/green-t017.txt                           |    5 +
 .../notes/green-t021.txt                           |    5 +
 .../notes/green-t025-targeted.txt                  |   31 +
 .../notes/green-t025.txt                           |    5 +
 .../notes/part5-failed.txt                         |    1 +
 .../notes/part5-regression.txt                     |   35 +
 .../notes/pre-change-file-sets.txt                 |  690 ++
 .../notes/pre-change-measurements.md               |  536 ++
 .../notes/quickstart-run.md                        | 1485 +++
 .../notes/red-first-evidence.md                    |  851 ++
 .../notes/red-t005.txt                             |  122 +
 .../notes/red-t007.txt                             |  228 +
 .../notes/red-t012.txt                             |  839 ++
 .../notes/red-t018.txt                             |  469 +
 .../notes/red-t022.txt                             |  204 +
 .../notes/targeted-set-v1-failed.txt               |    1 +
 .../specs/074-goal-team-sdd-unification/plan.md    |  258 +
 .../074-goal-team-sdd-unification/quickstart.md    |  324 +
 .../074-goal-team-sdd-unification/requirements.md  |   16 +-
 .../074-goal-team-sdd-unification/research.md      |  493 +
 .../specs/074-goal-team-sdd-unification/review.md  |    4 +
 .../specs/074-goal-team-sdd-unification/tasks.md   |  360 +-
 .../test-evidence/analyze-fix-checks.md            |  360 +
 .../test-evidence/analyze.jsonl                    |    7 +
 .../test-evidence/checklist-stage-checks.md        |  261 +
 .../test-evidence/checklist.jsonl                  |    7 +
 .../test-evidence/clarify.jsonl                    |    7 +
 .../test-evidence/compat-baseline-nodeids.txt      |  303 +
 .../containment-post-change-collect.txt            |  315 +
 .../test-evidence/containment-post-change-run.txt  |   36 +
 .../test-evidence/implement-baseline-run.txt       |  998 ++
 .../implement-targeted-part1-failed.txt            |    3 +
 .../test-evidence/implement-targeted-part1-run.txt |   65 +
 .../implement-targeted-part1-supp-failed.txt       |    3 +
 .../implement-targeted-part1-supp-run.txt          |   44 +
 .../implement-targeted-part2-failed.txt            |    3 +
 .../test-evidence/implement-targeted-part2-run.txt |   66 +
 .../implement-targeted-part2-supp-failed.txt       |    5 +
 .../implement-targeted-part2-supp-run.txt          |  102 +
 .../implement-targeted-part3-failed.txt            |    3 +
 .../test-evidence/implement-targeted-part3-run.txt |   70 +
 .../implement-targeted-part4-failed.txt            |    3 +
 .../test-evidence/implement-targeted-part4-run.txt |   75 +
 .../test-evidence/implement.jsonl                  |   21 +
 .../test-evidence/plan-stage-checks.md             |  472 +
 .../test-evidence/plan.jsonl                       |    7 +
 .../test-evidence/requirements-checks.txt          |   54 +
 .../test-evidence/review.jsonl                     |    7 +
 .../test-evidence/targeted-set-v1-baseline.txt     |  119 +
 .../test-evidence/tasks-stage-checks.md            |  399 +
 .../test-evidence/tasks.jsonl                      |    7 +
 .../074-goal-team-sdd-unification/verification.md  |   19 +
 .../specs/074a-authorized-routing/requirements.md  |    1 +
 .../specs/074b-nested-governance/requirements.md   |    1 +
 .../specs/099-speckit-seal/baseline-failed.txt     |  280 +
 .../checklists/2026-11-10-requirements-quality.md  |   72 +
 .../099-speckit-seal/checklists/requirements.md    |   43 +
 .specify/specs/099-speckit-seal/code-review.md     | 1841 ++++
 .../contracts/merge-back.contract.md               |  141 +
 .../contracts/records-and-boundaries.contract.md   |  140 +
 .../contracts/seal-engine.contract.md              |   87 +
 .../contracts/status-sealed.contract.md            |   80 +
 .../specs/099-speckit-seal/coverage-baseline.txt   |  642 ++
 .specify/specs/099-speckit-seal/data-model.md      |  216 +
 .specify/specs/099-speckit-seal/feature-ref.md     |  115 +
 .../notes/pre-change-measurements.md               |  126 +
 .../specs/099-speckit-seal/notes/quickstart-run.md |  215 +
 .../099-speckit-seal/notes/red-first-evidence.md   |  680 ++
 .specify/specs/099-speckit-seal/plan.md            |  333 +
 .specify/specs/099-speckit-seal/quickstart.md      |  196 +
 .specify/specs/099-speckit-seal/requirements.md    |  250 +
 .specify/specs/099-speckit-seal/research.md        |  228 +
 .specify/specs/099-speckit-seal/review.md          |  387 +
 .specify/specs/099-speckit-seal/tasks.md           |  374 +
 .../074-dated-record-hashes-before.txt             |   47 +
 .../074-dated-record-hashes-rerun-before.txt       |   49 +
 .../test-evidence/074-factory-resolutions.md       |   71 +
 .../074-merge-apply-rerun-20261111.txt             |   84 +
 .../test-evidence/074-merge-apply.txt              |    6 +
 .../074-merge-checks-rerun-20261111.txt            |   51 +
 .../test-evidence/074-merge-checks.txt             |   78 +
 .../test-evidence/074-merge-plan-after.json        | 2177 +++++
 .../test-evidence/074-merge-plan-after.txt         |   86 +
 .../test-evidence/074-merge-plan-before.json       | 3278 +++++++
 .../test-evidence/074-merge-plan-before.txt        |  194 +
 .../074-merge-plan-rerun-20261111.json             | 2717 ++++++
 .../074-merge-plan-rerun-20261111.txt              |   36 +
 .../test-evidence/074-pre-round-readings.txt       |   11 +
 .../074-rerun-before-snapshot-20261111.txt         |   12 +
 .../test-evidence/074-round-20261110.txt           |   52 +
 .../test-evidence/074-round-repair-r1-20261111.txt |   53 +
 .../test-evidence/074-round-rerun-20261111.txt     |   55 +
 .../test-evidence/analyze-coverage-2026-11-10.json | 1585 ++++
 .../analyze-coverage-r2-2026-11-10.json            | 1585 ++++
 .../analyze-coverage-r3-2026-11-10.json            | 1585 ++++
 .../test-evidence/analyze-gates-2026-11-10.txt     |  169 +
 .../test-evidence/analyze-merged-2026-11-10.md     |  202 +
 .../test-evidence/analyze-merged-r2-2026-11-10.md  |  233 +
 .../test-evidence/analyze-merged-r3-2026-11-10.md  |  240 +
 .../test-evidence/analyze-r2-gates-2026-11-10.txt  |  313 +
 .../test-evidence/analyze-r3-gates-2026-11-10.txt  |  489 +
 .../analyze-repair-dispositions-r1-2026-11-10.md   |  141 +
 .../analyze-repair-dispositions-r2-2026-11-10.md   |   85 +
 .../analyze-repair-gates-r1-2026-11-10.txt         |   73 +
 .../analyze-repair-gates-r2-2026-11-10.txt         |  160 +
 .../baseline-full-suite-20261110T150720Z.txt       | 9568 +++++++++++++++++++
 .../test-evidence/boundaries-audit.txt             |   25 +
 .../test-evidence/checklist-gates-2026-11-10.txt   |   19 +
 .../checklist-readings-2026-11-10.txt              |  162 +
 .../test-evidence/clarify-stage-checks.txt         |   29 +
 .../test-evidence/closure-rerun-20261111.txt       |   17 +
 .../test-evidence/closure-verdict-099-p9b.json     |   38 +
 .../test-evidence/closure-verdict-099-preflip.json |   38 +
 .../test-evidence/closure-verdict-099.json         |   38 +
 .../test-evidence/coverage-final.txt               |   29 +
 .../test-evidence/decomposition-plan.txt           |    2 +
 .../test-evidence/f1-red-first-20261111.txt        |  104 +
 .../test-evidence/f3-supersede-claims-20261111.txt |   17 +
 .../final-failed-parallel-sample-20261111.txt      |  286 +
 .../test-evidence/final-failed.txt                 |  268 +
 .../test-evidence/final-mirror-checks.txt          |   20 +
 .../test-evidence/final-suite-20261111.txt         | 9655 ++++++++++++++++++++
 .../test-evidence/final-suite-serial-20261111.txt  | 9455 +++++++++++++++++++
 .../099-speckit-seal/test-evidence/final-suite.txt |   35 +
 .../test-evidence/flow-class-lookup.txt            |    8 +
 .../test-evidence/merge-apply-checks.txt           |  178 +
 .../test-evidence/p1-status-domain-20261110.txt    |  183 +
 .../test-evidence/p2-engine-contract-20261110.txt  |  168 +
 .../test-evidence/p3-merge-plan-20261111.txt       |  137 +
 .../test-evidence/p5-red-first-20261111.txt        |  518 ++
 .../test-evidence/p5-seal-20261111.txt             |  127 +
 .../test-evidence/p6-archive-gate-20261111.txt     |  116 +
 .../test-evidence/p6-red-first-20261111.txt        |  246 +
 .../test-evidence/p7-adjacent-20261111.txt         |   73 +
 .../test-evidence/p7-adjacent2-20261111.txt        |    7 +
 .../test-evidence/p7-adjacent3-20261111.txt        |   80 +
 .../test-evidence/p7-adjacent4-20261111.txt        |    8 +
 .../test-evidence/p7-command-surface-20261111.txt  |   80 +
 .../test-evidence/p7-red-first-pins-20261111.txt   |   97 +
 .../p7-red-first-related-pins-20261111.txt         |  112 +
 .../p7-red-first-template-only-20261111.txt        |   32 +
 .../test-evidence/p7-seal-regression-20261111.txt  |    8 +
 .../test-evidence/p8b-dispositions-20261111.md     |   57 +
 .../test-evidence/p8b-red-first-20261111.txt       |  123 +
 .../test-evidence/p8b-suite-20261111.txt           |   15 +
 .../test-evidence/plan-stage-checks.txt            |   89 +
 .../test-evidence/post-flip-targeted.txt           |  346 +
 .../test-evidence/pre-analyze-requirements.txt     |    3 +
 .../review-repair-dispositions-r1-2026-11-11.md    |   86 +
 .../review-repair-r1-required-suites-20261111.txt  |   38 +
 .../review-repair-r1-suites-20261111.txt           |   80 +
 .../test-evidence/t041-rerun-20261111.txt          |   53 +
 .../t050-replay-repair-r1-20261111.json            |  852 ++
 .../t050-replay-repair-r1-20261111.txt             |   27 +
 .../test-evidence/t050-rerun-20261111.json         |  987 ++
 .../test-evidence/t050-rerun-20261111.txt          |   41 +
 .../test-evidence/tasks-stage-checks.txt           |   38 +
 .../test-evidence/validate-requirements.txt        |   11 +
 .specify/specs/099-speckit-seal/verification.md    |   76 +
 .specify/templates/feature-details-template.md     |   11 +-
 .specify/templates/feature-index-template.md       |    2 +-
 .specify/templates/plan-template.md                |    2 +-
 docs/reference/commands/seal.md                    |   62 +
 scripts/python/account-clause-coverage.py          |    5 +-
 scripts/python/closure-acceptance-check.py         |    6 +-
 scripts/python/non-disposable-check.py             |    7 +-
 scripts/python/seal-utils.py                       | 3049 +++++++
 scripts/python/validate-tasks.py                   |   49 +-
 shared/definitions/flow-class-definitions.md       |    4 +-
 shared/definitions/non-disposable-definitions.md   |    5 +-
 shared/definitions/probe-definitions.md            |    2 +
 shared/definitions/sdd-routing-definitions.md      |    8 +-
 shared/definitions/subagent-definitions.md         |    2 +-
 shared/guidelines/better-harness.md                |    4 +-
 shared/workflow/acceptance-hardening.md            |   53 +-
 shared/workflow/expression-gates.md                |    2 +-
 shared/workflow/feature-integration.md             |    8 +-
 skills/external/sdd-loop-driver/SKILL.md           |    2 +-
 .../references/decomposition-model.md              |    2 +-
 .../references/nested-invocation.md                |    6 +-
 skills/internal/create-team/SKILL.md               |    4 +-
 skills/internal/create-team/references/goal.md     |    2 +-
 skills/internal/manage-features/SKILL.md           |   25 +-
 skills/internal/sanitize-materials/SKILL.md        |   17 +
 skills/internal/seal-artifact/SKILL.md             |  104 +
 templates/commands/seal.md                         |   58 +
 templates/feature-details-template.md              |   11 +-
 templates/feature-index-template.md                |    2 +-
 templates/plan-template.md                         |    2 +-
 tests/contract/test_acceptance_state_machine.py    |   16 +-
 tests/contract/test_clause_coverage.py             |   30 +
 tests/contract/test_docs_step_injection.py         |    5 +
 tests/contract/test_expression_compatibility.py    |    8 +
 tests/contract/test_fast_fail_discipline.py        |    6 +-
 .../test_feedback_command_classification.py        |    6 +-
 tests/contract/test_flow_class_ledger.py           |   32 +-
 tests/contract/test_humanize_command_surface.py    |   13 +-
 tests/contract/test_migration_distribution.py      |   13 +-
 tests/contract/test_nested_run_report.py           |   14 +-
 tests/contract/test_nested_sdd_invocation.py       |   16 +-
 tests/contract/test_run_skills_wiring.py           |    7 +-
 tests/contract/test_script_interface_contract.py   |   23 +-
 tests/contract/test_sdd_routing_definitions.py     |    2 +-
 tests/contract/test_seal_archive_gate.py           |  547 ++
 tests/contract/test_seal_boundaries.py             |  497 +
 .../contract/test_seal_concurrency_and_readonly.py |  205 +
 tests/contract/test_seal_engine_contract.py        |  588 ++
 tests/contract/test_seal_merge_apply.py            |  592 ++
 tests/contract/test_seal_merge_plan.py             |  477 +
 tests/contract/test_seal_seal.py                   |  606 ++
 tests/contract/test_sealed_status_domain.py        |  350 +
 .../contract/test_skill_layer_visibility_guards.py |    6 +-
 tests/contract/test_status_gate_owner.py           |    7 +-
 .../099-fixture-parent/contracts/core.contract.md  |    3 +
 .../contracts/parent.contract.md                   |    3 +
 .../.specify/specs/099-fixture-parent/plan.md      |    5 +
 .../specs/099-fixture-parent/requirements.md       |   13 +
 .../.specify/specs/099-fixture-parent/tasks.md     |    4 +
 .../contracts/alpha.contract.md                    |    3 +
 .../contracts/core.contract.md                     |    3 +
 .../.specify/specs/099a-fixture-conflict/plan.md   |    5 +
 .../specs/099a-fixture-conflict/requirements.md    |   28 +
 .../specs/099b-fixture-conflict/requirements.md    |   14 +
 .../specs/099y-fixture-name-only/requirements.md   |    6 +
 .../specs/slice-099z-declared-only/requirements.md |    7 +
 .../.specify/state/099-fixture-parent.md           |    7 +
 .../skills/internal/demo-factory/SKILL.md          |    6 +
 .../specs/099-fixture-parent/requirements.md       |   13 +
 .../.specify/specs/099a-fixture-fd/requirements.md |   19 +
 .../.specify/state/099-fixture-parent.md           |    6 +
 .../skills/internal/demo-factory/SKILL.md          |    5 +
 .../specs/099-fixture-merged/code-review.md        |   20 +
 .../specs/099-fixture-merged/feature-detail.md     |   14 +
 .../specs/099-fixture-merged/feature-registry.md   |    9 +
 .../specs/099-fixture-merged/merge-manifest.json   |  303 +
 .../.specify/specs/099-fixture-merged/plan.md      |   21 +
 .../specs/099-fixture-merged/requirements.md       |   40 +
 .../.specify/specs/099-fixture-merged/review.md    |   27 +
 .../.specify/specs/099-fixture-merged/tasks.md     |   11 +
 .../test-evidence/run-2026-11-05.txt               |    3 +
 .../099-fixture-merged/test-evidence/smoke.txt     |    3 +
 .../specs/099-fixture-merged/verification.md       |   26 +
 .../specs/099a-fixture-slice/requirements.md       |   22 +
 .../.specify/specs/099a-fixture-slice/review.md    |   16 +
 .../test-evidence/run-2026-11-05.txt               |    3 +
 .../specs/099a-fixture-slice/verification.md       |    7 +
 .../specs/099-fixture-clean/code-review.md         |   16 +
 .../specs/099-fixture-clean/feature-detail.md      |   14 +
 .../specs/099-fixture-clean/feature-registry.md    |    9 +
 .../.specify/specs/099-fixture-clean/plan.md       |   21 +
 .../specs/099-fixture-clean/requirements.md        |   40 +
 .../.specify/specs/099-fixture-clean/review.md     |   23 +
 .../.specify/specs/099-fixture-clean/tasks.md      |   11 +
 .../099-fixture-clean/test-evidence/smoke.txt      |    3 +
 .../specs/099-fixture-clean/verification.md        |   21 +
 .../specs/099-fixture-clean/code-review.md         |   16 +
 .../specs/099-fixture-clean/feature-detail.md      |   14 +
 .../specs/099-fixture-clean/feature-registry.md    |    9 +
 .../.specify/specs/099-fixture-clean/plan.md       |   21 +
 .../specs/099-fixture-clean/requirements.md        |   40 +
 .../.specify/specs/099-fixture-clean/review.md     |   23 +
 .../.specify/specs/099-fixture-clean/tasks.md      |   11 +
 .../099-fixture-clean/test-evidence/smoke.txt      |    3 +
 .../specs/099-fixture-clean/verification.md        |   21 +
 .../specs/099-fixture-merged/code-review.md        |   20 +
 .../specs/099-fixture-merged/feature-detail.md     |   14 +
 .../specs/099-fixture-merged/feature-registry.md   |    9 +
 .../specs/099-fixture-merged/merge-manifest.json   |  324 +
 .../.specify/specs/099-fixture-merged/plan.md      |   21 +
 .../specs/099-fixture-merged/requirements.md       |   40 +
 .../.specify/specs/099-fixture-merged/review.md    |   27 +
 .../.specify/specs/099-fixture-merged/tasks.md     |   11 +
 .../test-evidence/run-2026-11-05.txt               |    3 +
 .../099-fixture-merged/test-evidence/smoke.txt     |    3 +
 .../specs/099-fixture-merged/verification.md       |   26 +
 .../specs/099a-fixture-slice/requirements.md       |   22 +
 .../.specify/specs/099a-fixture-slice/review.md    |   16 +
 .../test-evidence/run-2026-11-05.txt               |    3 +
 .../specs/099a-fixture-slice/verification.md       |    7 +
 .../specs/099-fixture-clean/code-review.md         |   16 +
 .../specs/099-fixture-clean/feature-detail.md      |   14 +
 .../specs/099-fixture-clean/feature-registry.md    |    9 +
 .../.specify/specs/099-fixture-clean/plan.md       |   21 +
 .../specs/099-fixture-clean/requirements.md        |   40 +
 .../.specify/specs/099-fixture-clean/review.md     |   23 +
 .../.specify/specs/099-fixture-clean/tasks.md      |   11 +
 .../099-fixture-clean/test-evidence/smoke.txt      |    3 +
 .../specs/099-fixture-clean/verification.md        |   21 +
 .../specs/099-fixture-clean/code-review.md         |   16 +
 .../specs/099-fixture-clean/feature-detail.md      |   14 +
 .../specs/099-fixture-clean/feature-registry.md    |    9 +
 .../.specify/specs/099-fixture-clean/plan.md       |   21 +
 .../specs/099-fixture-clean/requirements.md        |   40 +
 .../.specify/specs/099-fixture-clean/review.md     |   23 +
 .../.specify/specs/099-fixture-clean/tasks.md      |   11 +
 .../099-fixture-clean/test-evidence/smoke.txt      |    3 +
 .../specs/099-fixture-clean/verification.md        |   21 +
 .../specs/099-fixture-clean/code-review.md         |   16 +
 .../specs/099-fixture-clean/feature-detail.md      |   14 +
 .../specs/099-fixture-clean/feature-registry.md    |    9 +
 .../.specify/specs/099-fixture-clean/plan.md       |   21 +
 .../specs/099-fixture-clean/requirements.md        |   40 +
 .../.specify/specs/099-fixture-clean/review.md     |   29 +
 .../.specify/specs/099-fixture-clean/tasks.md      |   11 +
 .../099-fixture-clean/test-evidence/smoke.txt      |    3 +
 .../specs/099-fixture-clean/verification.md        |   21 +
 .../specs/099-fixture-clean/code-review.md         |   16 +
 .../specs/099-fixture-clean/feature-detail.md      |   14 +
 .../specs/099-fixture-clean/feature-registry.md    |    9 +
 .../.specify/specs/099-fixture-clean/plan.md       |   21 +
 .../specs/099-fixture-clean/requirements.md        |   40 +
 .../.specify/specs/099-fixture-clean/review.md     |   23 +
 .../.specify/specs/099-fixture-clean/tasks.md      |   11 +
 .../099-fixture-clean/test-evidence/smoke.txt      |    3 +
 .../specs/099-fixture-clean/verification.md        |   21 +
 .../specs/099a-fixture-open/requirements.md        |   15 +
 .../.specify/specs/099a-fixture-open/tasks.md      |    6 +
 .../specs/099-fixture-clean/code-review.md         |   16 +
 .../specs/099-fixture-clean/feature-detail.md      |   14 +
 .../specs/099-fixture-clean/feature-registry.md    |    9 +
 .../.specify/specs/099-fixture-clean/plan.md       |   21 +
 .../specs/099-fixture-clean/requirements.md        |   40 +
 .../.specify/specs/099-fixture-clean/review.md     |   23 +
 .../.specify/specs/099-fixture-clean/tasks.md      |   11 +
 .../099-fixture-clean/test-evidence/smoke.txt      |    3 +
 .../specs/099-fixture-clean/verification.md        |   21 +
 .../specs/099-fixture-clean/code-review.md         |   16 +
 .../specs/099-fixture-clean/feature-detail.md      |   14 +
 .../specs/099-fixture-clean/feature-registry.md    |    9 +
 .../.specify/specs/099-fixture-clean/plan.md       |   21 +
 .../specs/099-fixture-clean/requirements.md        |   40 +
 .../.specify/specs/099-fixture-clean/review.md     |   23 +
 .../.specify/specs/099-fixture-clean/tasks.md      |   11 +
 .../099-fixture-clean/test-evidence/smoke.txt      |    3 +
 .../specs/099-fixture-clean/verification.md        |   19 +
 .../specs/099-fixture-clean/code-review.md         |   16 +
 .../specs/099-fixture-clean/feature-detail.md      |   14 +
 .../specs/099-fixture-clean/feature-registry.md    |    9 +
 .../.specify/specs/099-fixture-clean/plan.md       |   21 +
 .../specs/099-fixture-clean/requirements.md        |   40 +
 .../.specify/specs/099-fixture-clean/review.md     |   23 +
 .../.specify/specs/099-fixture-clean/tasks.md      |   11 +
 .../099-fixture-clean/test-evidence/smoke.txt      |    3 +
 .../specs/099-fixture-clean/verification.md        |   21 +
 .../099-fixture-parent/checklists/requirements.md  |    1 +
 .../checkpoints/cp-2026-11-01.txt                  |    1 +
 .../099-fixture-parent/contracts/core.contract.md  |    5 +
 .../specs/099-fixture-parent/feature-ref.md        |    3 +
 .../.specify/specs/099-fixture-parent/plan.md      |    5 +
 .../specs/099-fixture-parent/requirements.md       |   22 +
 .../.specify/specs/099-fixture-parent/research.md  |    5 +
 .../.specify/specs/099-fixture-parent/tasks.md     |    4 +
 .../test-evidence/run-2026-11-01.txt               |    1 +
 .../099a-fixture-alpha/checklists/plan-review.md   |    1 +
 .../099a-fixture-alpha/checklists/requirements.md  |    1 +
 .../checkpoints/cp-2026-11-01.txt                  |    1 +
 .../specs/099a-fixture-alpha/code-review.md        |    5 +
 .../099a-fixture-alpha/contracts/core.contract.md  |    5 +
 .../099a-fixture-alpha/contracts/extra-alpha.md    |    3 +
 .../specs/099a-fixture-alpha/data-model.md         |    5 +
 .../.specify/specs/099a-fixture-alpha/plan.md      |    9 +
 .../specs/099a-fixture-alpha/requirements.md       |   31 +
 .../.specify/specs/099a-fixture-alpha/review.md    |    5 +
 .../.specify/specs/099a-fixture-alpha/tasks.md     |    4 +
 .../test-evidence/run-2026-11-01.txt               |    1 +
 .../specs/099a-fixture-alpha/verification.md       |    3 +
 .../checkpoints/cp-2026-11-05.txt                  |    1 +
 .../specs/099b-fixture-beta/code-review.md         |    5 +
 .../099b-fixture-beta/contracts/core.contract.md   |    3 +
 .../.specify/specs/099b-fixture-beta/plan.md       |    9 +
 .../specs/099b-fixture-beta/requirements.md        |   25 +
 .../.specify/specs/099b-fixture-beta/review.md     |    5 +
 .../.specify/specs/099b-fixture-beta/tasks.md      |    4 +
 .../test-evidence/run-2026-11-02.txt               |    1 +
 .../specs/099b-fixture-beta/verification.md        |    3 +
 .../.specify/state/099-fixture-parent.md           |   10 +
 tests/integration/test_docs_command_scenarios.py   |    7 +-
 tests/integration/test_seal_074_round.py           |  195 +
 tests/integration/test_seal_merge_determinism.py   |  187 +
 485 files changed, 97491 insertions(+), 319 deletions(-)
```

---

## Review 意见


### 👍 [PRAISE] scripts/python/seal-utils.py (Line 2594)

> F1 repaired and re-verified in this run. The seal P0/blocking gate now reads each slice's original review.md / code-review.md alongside the parent pointer view (record collection at :2587-:2600), qualifies finding ids as <slice>:F1, aggregates the summary per source, and computes unaccounted per source (:2601-:2630). The C-044 waiver carrier for a slice finding is that slice record's code section plus the feature detail; the receipt references every record read and names the slice carrier in waivers[].source. Evidence measured this run: 4 new slice-P0/blocking tests pass (pre-fix all 4 failed, test-evidence/f1-red-first-20261111.txt); the real 074 replay (twice, read-only) now emits p0-unresolved 074b-nested-governance:F1 at .specify/specs/074b-nested-governance/review.md:115, exit 2, writes 0, byte-identical reruns, 074a/074b/parent hash sets unchanged, seal.md absent. This closes the previous record's blocking entry without a waiver.

<sub>03:05:18</sub>


### 🟠 [IMPORTANT] scripts/python/seal-utils.py (Line 2472)

> Carried and still open: C-005 atomic-batch gap. _write_seal_batch records originals before write_text (line 2471) but appends the path to 'written' only after the write returns (line 2473). If write_text raises mid-stream after truncation (e.g. ENOSPC), the in-flight file is not restored by the exception loop (:2475-:2480), so a half-written registry row or detail can survive. C-005 (contracts/seal-engine.contract.md) requires every written file restored on any failure; the guard test only exercises an open() permission failure. Fix: register the path as written before the write (or restore the current path in the handler) and add a fault-injection test. Answer in this run: agreed; it is real, remains open as REC-099-5, and does not block the transition under the gate's severity rules.

<sub>03:05:18</sub>


### 🟢 [SUGGESTION] scripts/python/seal-utils.py (Line 2210)

> Waiver matching on the feature-detail carrier uses the unqualified finding id (block["id"], e.g. F1) even when the finding is reported as <slice>:F1. When two slices both raise F1 and each slice review's code section carries its own literal waiver line, one blanket '- **User waiver**: ... F1 ...' line in the parent feature detail disposes both slice findings. Consider matching the qualified token (<slice>:F1) on the detail carrier when the finding came from a slice record. Low likelihood today (no current split has two P0 F1s), but the qualified id already exists in the receipt, so the fix is local to _p0_findings.

<sub>03:05:18</sub>


### 🟢 [SUGGESTION] scripts/python/seal-utils.py (Line 1682)

> Carried from the archived record: the P8b continuity fix anchors _continuous at each sequence's own minimum for every ID family. That is correct for per-file contract clauses (074 files start at C-47), but it also relaxes FR/SC/STR/T/E, which are feature-global and expected to start at 1. A merged requirements.md or tasks.md that loses its leading identifiers (FR-001 absent, FR-002 present) now reads as continuous. Consider keeping the 1-anchor for those four families or adding a leading-id regression fixture.

<sub>03:05:18</sub>


### 👍 [PRAISE] scripts/python/validate-tasks.py (Line 603)

> F3 repaired at the right owner: the superseded pre-split block is parsed by the same _strip_claims implementation as active rows (SUPERSEDED_HEADING/SUPERSEDED_ROW at :89-:90, retained-claim collection at :295-:325) and only feeds claims_out, so retained claims never re-enter the current-plan checks. The owner rule lives in shared/workflow/acceptance-hardening.md § 'Superseded pre-split records retain their claims'. Measured this run: the hermetic red/green fixture reads claimed 0 -> 3 (f3-supersede-claims-20261111.txt), test_superseded_pre_split_rows_retain_their_claims passes, 099 coverage is ok / 45 claimed / 0 beyond baseline, and the 074 lane reports claimed=144 with zero 074-* names beyond its baseline.

<sub>03:05:18</sub>


> **未提交范围（未评审）**: 2 个未提交路径未计入本次评审对象（.specify/memory/trigger/index.json, .specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt）；本回执不对该范围给出任何结论。

<!-- coverage-receipt:begin -->
receipt_version=1
base=b3da3a26dfba209057f65c2b17962b9516812c39
head=55dd6d61dddd2ed529cbbd61dc3c3e966b470988
base_source=feature-first-commit
renderer=text
changed_files=485
judged_files=5
skipped_files=480
gap_files=0
lines_added=97491
lines_deleted=319
file.001.path=.claude/commands/speckit.seal.md
file.001.verdict=skipped
file.001.reason=generated
file.002.path=.github/prompts/speckit.seal.prompt.md
file.002.verdict=skipped
file.002.reason=generated
file.003.path=.opencode/command/speckit.seal.md
file.003.verdict=skipped
file.003.reason=generated
file.004.path=.qoder/commands/speckit.seal.md
file.004.verdict=skipped
file.004.reason=generated
file.005.path=.specify/constitution.md
file.005.verdict=skipped
file.005.reason=non-code-file
file.006.path=.specify/features.md
file.006.verdict=skipped
file.006.reason=non-code-file
file.007.path=.specify/features/099-speckit-seal.md
file.007.verdict=skipped
file.007.reason=non-code-file
file.008.path=.specify/glossary.md
file.008.verdict=skipped
file.008.reason=non-code-file
file.009.path=.specify/memory/exec-quant/records/20261110T122415340717Z-68288034.json
file.009.verdict=skipped
file.009.reason=non-code-file
file.010.path=.specify/memory/exec-quant/records/20261110T123300407905Z-1fa74f99.json
file.010.verdict=skipped
file.010.reason=non-code-file
file.011.path=.specify/memory/exec-quant/records/20261110T131540636283Z-d51fb7cb.json
file.011.verdict=skipped
file.011.reason=non-code-file
file.012.path=.specify/memory/exec-quant/records/20261110T134514589152Z-7ddd0b1b.json
file.012.verdict=skipped
file.012.reason=non-code-file
file.013.path=.specify/memory/exec-quant/records/20261110T135735902193Z-b8758b49.json
file.013.verdict=skipped
file.013.reason=non-code-file
file.014.path=.specify/memory/exec-quant/records/20261110T140712289140Z-b5a8bb50.json
file.014.verdict=skipped
file.014.reason=non-code-file
file.015.path=.specify/memory/exec-quant/records/20261110T142455961221Z-c5e27bc2.json
file.015.verdict=skipped
file.015.reason=non-code-file
file.016.path=.specify/memory/exec-quant/records/20261110T150505512980Z-508bec9b.json
file.016.verdict=skipped
file.016.reason=non-code-file
file.017.path=.specify/memory/exec-quant/records/20261110T183846975285Z-15becc33.json
file.017.verdict=skipped
file.017.reason=non-code-file
file.018.path=.specify/memory/exec-quant/records/20261110T183847312664Z-060dbeab.json
file.018.verdict=skipped
file.018.reason=non-code-file
file.019.path=.specify/memory/exec-quant/records/20261110T183847647164Z-cfe900b3.json
file.019.verdict=skipped
file.019.reason=non-code-file
file.020.path=.specify/memory/exec-quant/records/20261110T183847980886Z-50cfe662.json
file.020.verdict=skipped
file.020.reason=non-code-file
file.021.path=.specify/memory/feedback/20261110T122417Z-speckit-requirements.md
file.021.verdict=skipped
file.021.reason=non-code-file
file.022.path=.specify/memory/feedback/20261110T123320Z-speckit-clarify.md
file.022.verdict=skipped
file.022.reason=non-code-file
file.023.path=.specify/memory/feedback/20261110T131542Z-speckit-plan.md
file.023.verdict=skipped
file.023.reason=non-code-file
file.024.path=.specify/memory/feedback/20261110T134640Z-speckit-tasks.md
file.024.verdict=skipped
file.024.reason=non-code-file
file.025.path=.specify/memory/feedback/20261110T135746Z-speckit-checklist.md
file.025.verdict=skipped
file.025.reason=non-code-file
file.026.path=.specify/memory/feedback/20261110T140722Z-speckit-analyze.md
file.026.verdict=skipped
file.026.reason=non-code-file
file.027.path=.specify/memory/feedback/20261110T142511Z-speckit-analyze.md
file.027.verdict=skipped
file.027.reason=non-code-file
file.028.path=.specify/memory/feedback/20261110T150505Z-speckit-analyze.md
file.028.verdict=skipped
file.028.reason=non-code-file
file.029.path=.specify/memory/feedback/20261110T183906Z-speckit-review.md
file.029.verdict=skipped
file.029.reason=non-code-file
file.030.path=.specify/memory/feedback/20261110T183913Z-skill-code-review.md
file.030.verdict=skipped
file.030.reason=non-code-file
file.031.path=.specify/memory/feedback/20261110T183913Z-skill-review-feature-quality.md
file.031.verdict=skipped
file.031.reason=non-code-file
file.032.path=.specify/memory/feedback/20261110T183913Z-skill-review-sdd-process.md
file.032.verdict=skipped
file.032.reason=non-code-file
file.033.path=.specify/memory/retention/closeout/20261110T122515Z-099-speckit-seal-requirements.md
file.033.verdict=skipped
file.033.reason=non-code-file
file.034.path=.specify/memory/retention/closeout/20261110T123338Z-099-speckit-seal-clarify.md
file.034.verdict=skipped
file.034.reason=non-code-file
file.035.path=.specify/memory/retention/closeout/20261110T131622Z-099-speckit-seal-plan.md
file.035.verdict=skipped
file.035.reason=non-code-file
file.036.path=.specify/memory/retention/closeout/20261110T134741Z-099-speckit-seal-tasks.md
file.036.verdict=skipped
file.036.reason=non-code-file
file.037.path=.specify/memory/retention/closeout/20261110T135818Z-099-speckit-seal-checklist.md
file.037.verdict=skipped
file.037.reason=non-code-file
file.038.path=.specify/memory/retention/closeout/20261110T140740Z-099-speckit-seal-analyze.md
file.038.verdict=skipped
file.038.reason=non-code-file
file.039.path=.specify/memory/retention/closeout/20261110T142547Z-099-speckit-seal-analyze-r2.md
file.039.verdict=skipped
file.039.reason=non-code-file
file.040.path=.specify/memory/retention/closeout/20261110T150529Z-099-speckit-seal-analyze-r3.md
file.040.verdict=skipped
file.040.reason=non-code-file
file.041.path=.specify/memory/retention/closeout/20261110T184022Z-099-speckit-seal-review.md
file.041.verdict=skipped
file.041.reason=non-code-file
file.042.path=.specify/memory/session/20261106T080226Z-run-determination-speckit-review-r20261106t040353z-087a.md
file.042.verdict=skipped
file.042.reason=non-code-file
file.043.path=.specify/memory/session/20261106T105438Z-run-determination-skill-code-review-r20261106t105429z-087rev.md
file.043.verdict=skipped
file.043.reason=non-code-file
file.044.path=.specify/memory/session/20261109T003341Z-run-determination-speckit-review-r20261108t220214z-8647.md
file.044.verdict=skipped
file.044.reason=non-code-file
file.045.path=.specify/memory/session/20261109T053527Z-run-determination-skill-review-feature-quality-r20261109t023.md
file.045.verdict=skipped
file.045.reason=non-code-file
file.046.path=.specify/memory/session/20261109T053545Z-run-determination-skill-review-sdd-process-r20261109t023000z.md
file.046.verdict=skipped
file.046.reason=non-code-file
file.047.path=.specify/memory/session/20261109T075428Z-run-determination-speckit-clarify-093-clarify-a1.md
file.047.verdict=skipped
file.047.reason=non-code-file
file.048.path=.specify/memory/session/20261109T085721Z-run-determination-speckit-analyze-r20261109t090000z-analyze.md
file.048.verdict=skipped
file.048.reason=non-code-file
file.049.path=.specify/memory/session/20261110T122409Z-run-determination-speckit-requirements-r20261110t121314z-b09.md
file.049.verdict=skipped
file.049.reason=non-code-file
file.050.path=.specify/memory/session/20261110T123255Z-run-determination-speckit-clarify-r20261110t121314z-b099.md
file.050.verdict=skipped
file.050.reason=non-code-file
file.051.path=.specify/memory/session/20261110T131533Z-run-determination-speckit-plan-r20261110t121314z-b099.md
file.051.verdict=skipped
file.051.reason=non-code-file
file.052.path=.specify/memory/session/20261110T134453Z-run-determination-speckit-tasks-r20261110t121314z-b099.md
file.052.verdict=skipped
file.052.reason=non-code-file
file.053.path=.specify/memory/session/20261110T135729Z-run-determination-speckit-checklist-r20261110t121314z-b099.md
file.053.verdict=skipped
file.053.reason=non-code-file
file.054.path=.specify/memory/session/20261110T140706Z-run-determination-speckit-analyze-r20261110t121314z-b099.md
file.054.verdict=skipped
file.054.reason=non-code-file
file.055.path=.specify/memory/session/20261110T142438Z-run-determination-speckit-analyze-r20261110t142432z-099-anal.md
file.055.verdict=skipped
file.055.reason=non-code-file
file.056.path=.specify/memory/session/20261110T150457Z-run-determination-speckit-analyze-r20261110t150457z-099-anal.md
file.056.verdict=skipped
file.056.reason=non-code-file
file.057.path=.specify/memory/session/20261110T183838Z-run-determination-speckit-review-r20261110t183510z-099-revie.md
file.057.verdict=skipped
file.057.reason=non-code-file
file.058.path=.specify/memory/session/20261110T183842Z-run-determination-skill-review-feature-quality-r20261110t183.md
file.058.verdict=skipped
file.058.reason=non-code-file
file.059.path=.specify/memory/session/20261110T183842Z-run-determination-skill-review-sdd-process-r20261110t183510z.md
file.059.verdict=skipped
file.059.reason=non-code-file
file.060.path=.specify/memory/session/20261110T183843Z-run-determination-skill-code-review-r20261110t183510z-099-re.md
file.060.verdict=skipped
file.060.reason=non-code-file
file.061.path=.specify/register.md
file.061.verdict=skipped
file.061.reason=non-code-file
file.062.path=.specify/scripts/python/account-clause-coverage.py
file.062.verdict=skipped
file.062.reason=generated
file.063.path=.specify/scripts/python/closure-acceptance-check.py
file.063.verdict=skipped
file.063.reason=generated
file.064.path=.specify/scripts/python/non-disposable-check.py
file.064.verdict=skipped
file.064.reason=generated
file.065.path=.specify/scripts/python/seal-utils.py
file.065.verdict=skipped
file.065.reason=generated
file.066.path=.specify/scripts/python/validate-tasks.py
file.066.verdict=skipped
file.066.reason=generated
file.067.path=.specify/shared/definitions/flow-class-definitions.md
file.067.verdict=skipped
file.067.reason=generated
file.068.path=.specify/shared/definitions/non-disposable-definitions.md
file.068.verdict=skipped
file.068.reason=generated
file.069.path=.specify/shared/definitions/probe-definitions.md
file.069.verdict=skipped
file.069.reason=generated
file.070.path=.specify/shared/definitions/sdd-routing-definitions.md
file.070.verdict=skipped
file.070.reason=generated
file.071.path=.specify/shared/definitions/subagent-definitions.md
file.071.verdict=skipped
file.071.reason=generated
file.072.path=.specify/shared/guidelines/better-harness.md
file.072.verdict=skipped
file.072.reason=generated
file.073.path=.specify/shared/workflow/acceptance-hardening.md
file.073.verdict=skipped
file.073.reason=generated
file.074.path=.specify/shared/workflow/expression-gates.md
file.074.verdict=skipped
file.074.reason=generated
file.075.path=.specify/shared/workflow/feature-integration.md
file.075.verdict=skipped
file.075.reason=generated
file.076.path=.specify/skills/internal/create-team/SKILL.md
file.076.verdict=skipped
file.076.reason=generated
file.077.path=.specify/skills/internal/create-team/references/goal.md
file.077.verdict=skipped
file.077.reason=generated
file.078.path=.specify/skills/internal/manage-features/SKILL.md
file.078.verdict=skipped
file.078.reason=generated
file.079.path=.specify/skills/internal/sanitize-materials/SKILL.md
file.079.verdict=skipped
file.079.reason=generated
file.080.path=.specify/skills/internal/seal-artifact/SKILL.md
file.080.verdict=skipped
file.080.reason=generated
file.081.path=.specify/skills/sdd-loop-driver/SKILL.md
file.081.verdict=skipped
file.081.reason=generated
file.082.path=.specify/skills/sdd-loop-driver/references/decomposition-model.md
file.082.verdict=skipped
file.082.reason=generated
file.083.path=.specify/skills/sdd-loop-driver/references/nested-invocation.md
file.083.verdict=skipped
file.083.reason=generated
file.084.path=.specify/specs/027-feedback-mechanism/contracts/command-classification.md
file.084.verdict=skipped
file.084.reason=non-code-file
file.085.path=.specify/specs/074-goal-team-sdd-unification/checklists/readiness-2026-10-29.md
file.085.verdict=skipped
file.085.reason=non-code-file
file.086.path=.specify/specs/074-goal-team-sdd-unification/checklists/recheck-2026-10-29-implement-start.md
file.086.verdict=skipped
file.086.reason=non-code-file
file.087.path=.specify/specs/074-goal-team-sdd-unification/checklists/requirements.md
file.087.verdict=skipped
file.087.reason=non-code-file
file.088.path=.specify/specs/074-goal-team-sdd-unification/code-review.md
file.088.verdict=skipped
file.088.reason=non-code-file
file.089.path=.specify/specs/074-goal-team-sdd-unification/contracts/bootstrap-and-maintenance.md
file.089.verdict=skipped
file.089.reason=non-code-file
file.090.path=.specify/specs/074-goal-team-sdd-unification/contracts/compat-and-safety.md
file.090.verdict=skipped
file.090.reason=non-code-file
file.091.path=.specify/specs/074-goal-team-sdd-unification/contracts/diffusion.md
file.091.verdict=skipped
file.091.reason=non-code-file
file.092.path=.specify/specs/074-goal-team-sdd-unification/contracts/hierarchy-and-authorization.md
file.092.verdict=skipped
file.092.reason=non-code-file
file.093.path=.specify/specs/074-goal-team-sdd-unification/contracts/nested-invocation.md
file.093.verdict=skipped
file.093.reason=non-code-file
file.094.path=.specify/specs/074-goal-team-sdd-unification/contracts/report-and-attribution.md
file.094.verdict=skipped
file.094.reason=non-code-file
file.095.path=.specify/specs/074-goal-team-sdd-unification/contracts/routing-decision.md
file.095.verdict=skipped
file.095.reason=non-code-file
file.096.path=.specify/specs/074-goal-team-sdd-unification/feature-ref.md
file.096.verdict=skipped
file.096.reason=non-code-file
file.097.path=.specify/specs/074-goal-team-sdd-unification/merge-manifest.json
file.097.verdict=skipped
file.097.reason=non-code-file
file.098.path=.specify/specs/074-goal-team-sdd-unification/notes/closure-full-run-2.txt
file.098.verdict=skipped
file.098.reason=non-code-file
file.099.path=.specify/specs/074-goal-team-sdd-unification/notes/closure-full-run-3.txt
file.099.verdict=skipped
file.099.reason=non-code-file
file.100.path=.specify/specs/074-goal-team-sdd-unification/notes/closure-full-run.txt
file.100.verdict=skipped
file.100.reason=non-code-file
file.101.path=.specify/specs/074-goal-team-sdd-unification/notes/full-baseline-run.txt
file.101.verdict=skipped
file.101.reason=non-code-file
file.102.path=.specify/specs/074-goal-team-sdd-unification/notes/golden-rows.txt
file.102.verdict=skipped
file.102.reason=non-code-file
file.103.path=.specify/specs/074-goal-team-sdd-unification/notes/golden-run1.json
file.103.verdict=skipped
file.103.reason=non-code-file
file.104.path=.specify/specs/074-goal-team-sdd-unification/notes/golden-run2.json
file.104.verdict=skipped
file.104.reason=non-code-file
file.105.path=.specify/specs/074-goal-team-sdd-unification/notes/green-t016-demo.txt
file.105.verdict=skipped
file.105.reason=non-code-file
file.106.path=.specify/specs/074-goal-team-sdd-unification/notes/green-t016.txt
file.106.verdict=skipped
file.106.reason=non-code-file
file.107.path=.specify/specs/074-goal-team-sdd-unification/notes/green-t017.txt
file.107.verdict=skipped
file.107.reason=non-code-file
file.108.path=.specify/specs/074-goal-team-sdd-unification/notes/green-t021.txt
file.108.verdict=skipped
file.108.reason=non-code-file
file.109.path=.specify/specs/074-goal-team-sdd-unification/notes/green-t025-targeted.txt
file.109.verdict=skipped
file.109.reason=non-code-file
file.110.path=.specify/specs/074-goal-team-sdd-unification/notes/green-t025.txt
file.110.verdict=skipped
file.110.reason=non-code-file
file.111.path=.specify/specs/074-goal-team-sdd-unification/notes/part5-failed.txt
file.111.verdict=skipped
file.111.reason=non-code-file
file.112.path=.specify/specs/074-goal-team-sdd-unification/notes/part5-regression.txt
file.112.verdict=skipped
file.112.reason=non-code-file
file.113.path=.specify/specs/074-goal-team-sdd-unification/notes/pre-change-file-sets.txt
file.113.verdict=skipped
file.113.reason=non-code-file
file.114.path=.specify/specs/074-goal-team-sdd-unification/notes/pre-change-measurements.md
file.114.verdict=skipped
file.114.reason=non-code-file
file.115.path=.specify/specs/074-goal-team-sdd-unification/notes/quickstart-run.md
file.115.verdict=skipped
file.115.reason=non-code-file
file.116.path=.specify/specs/074-goal-team-sdd-unification/notes/red-first-evidence.md
file.116.verdict=skipped
file.116.reason=non-code-file
file.117.path=.specify/specs/074-goal-team-sdd-unification/notes/red-t005.txt
file.117.verdict=skipped
file.117.reason=non-code-file
file.118.path=.specify/specs/074-goal-team-sdd-unification/notes/red-t007.txt
file.118.verdict=skipped
file.118.reason=non-code-file
file.119.path=.specify/specs/074-goal-team-sdd-unification/notes/red-t012.txt
file.119.verdict=skipped
file.119.reason=non-code-file
file.120.path=.specify/specs/074-goal-team-sdd-unification/notes/red-t018.txt
file.120.verdict=skipped
file.120.reason=non-code-file
file.121.path=.specify/specs/074-goal-team-sdd-unification/notes/red-t022.txt
file.121.verdict=skipped
file.121.reason=non-code-file
file.122.path=.specify/specs/074-goal-team-sdd-unification/notes/targeted-set-v1-failed.txt
file.122.verdict=skipped
file.122.reason=non-code-file
file.123.path=.specify/specs/074-goal-team-sdd-unification/plan.md
file.123.verdict=skipped
file.123.reason=non-code-file
file.124.path=.specify/specs/074-goal-team-sdd-unification/quickstart.md
file.124.verdict=skipped
file.124.reason=non-code-file
file.125.path=.specify/specs/074-goal-team-sdd-unification/requirements.md
file.125.verdict=skipped
file.125.reason=non-code-file
file.126.path=.specify/specs/074-goal-team-sdd-unification/research.md
file.126.verdict=skipped
file.126.reason=non-code-file
file.127.path=.specify/specs/074-goal-team-sdd-unification/review.md
file.127.verdict=skipped
file.127.reason=non-code-file
file.128.path=.specify/specs/074-goal-team-sdd-unification/tasks.md
file.128.verdict=skipped
file.128.reason=non-code-file
file.129.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/analyze-fix-checks.md
file.129.verdict=skipped
file.129.reason=non-code-file
file.130.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/analyze.jsonl
file.130.verdict=skipped
file.130.reason=non-code-file
file.131.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/checklist-stage-checks.md
file.131.verdict=skipped
file.131.reason=non-code-file
file.132.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/checklist.jsonl
file.132.verdict=skipped
file.132.reason=non-code-file
file.133.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/clarify.jsonl
file.133.verdict=skipped
file.133.reason=non-code-file
file.134.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/compat-baseline-nodeids.txt
file.134.verdict=skipped
file.134.reason=non-code-file
file.135.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/containment-post-change-collect.txt
file.135.verdict=skipped
file.135.reason=non-code-file
file.136.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/containment-post-change-run.txt
file.136.verdict=skipped
file.136.reason=non-code-file
file.137.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/implement-baseline-run.txt
file.137.verdict=skipped
file.137.reason=non-code-file
file.138.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/implement-targeted-part1-failed.txt
file.138.verdict=skipped
file.138.reason=non-code-file
file.139.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/implement-targeted-part1-run.txt
file.139.verdict=skipped
file.139.reason=non-code-file
file.140.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/implement-targeted-part1-supp-failed.txt
file.140.verdict=skipped
file.140.reason=non-code-file
file.141.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/implement-targeted-part1-supp-run.txt
file.141.verdict=skipped
file.141.reason=non-code-file
file.142.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/implement-targeted-part2-failed.txt
file.142.verdict=skipped
file.142.reason=non-code-file
file.143.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/implement-targeted-part2-run.txt
file.143.verdict=skipped
file.143.reason=non-code-file
file.144.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/implement-targeted-part2-supp-failed.txt
file.144.verdict=skipped
file.144.reason=non-code-file
file.145.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/implement-targeted-part2-supp-run.txt
file.145.verdict=skipped
file.145.reason=non-code-file
file.146.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/implement-targeted-part3-failed.txt
file.146.verdict=skipped
file.146.reason=non-code-file
file.147.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/implement-targeted-part3-run.txt
file.147.verdict=skipped
file.147.reason=non-code-file
file.148.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/implement-targeted-part4-failed.txt
file.148.verdict=skipped
file.148.reason=non-code-file
file.149.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/implement-targeted-part4-run.txt
file.149.verdict=skipped
file.149.reason=non-code-file
file.150.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/implement.jsonl
file.150.verdict=skipped
file.150.reason=non-code-file
file.151.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/plan-stage-checks.md
file.151.verdict=skipped
file.151.reason=non-code-file
file.152.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/plan.jsonl
file.152.verdict=skipped
file.152.reason=non-code-file
file.153.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/requirements-checks.txt
file.153.verdict=skipped
file.153.reason=non-code-file
file.154.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/review.jsonl
file.154.verdict=skipped
file.154.reason=non-code-file
file.155.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/targeted-set-v1-baseline.txt
file.155.verdict=skipped
file.155.reason=non-code-file
file.156.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/tasks-stage-checks.md
file.156.verdict=skipped
file.156.reason=non-code-file
file.157.path=.specify/specs/074-goal-team-sdd-unification/test-evidence/tasks.jsonl
file.157.verdict=skipped
file.157.reason=non-code-file
file.158.path=.specify/specs/074-goal-team-sdd-unification/verification.md
file.158.verdict=skipped
file.158.reason=non-code-file
file.159.path=.specify/specs/074a-authorized-routing/requirements.md
file.159.verdict=skipped
file.159.reason=non-code-file
file.160.path=.specify/specs/074b-nested-governance/requirements.md
file.160.verdict=skipped
file.160.reason=non-code-file
file.161.path=.specify/specs/099-speckit-seal/baseline-failed.txt
file.161.verdict=skipped
file.161.reason=non-code-file
file.162.path=.specify/specs/099-speckit-seal/checklists/2026-11-10-requirements-quality.md
file.162.verdict=skipped
file.162.reason=non-code-file
file.163.path=.specify/specs/099-speckit-seal/checklists/requirements.md
file.163.verdict=skipped
file.163.reason=non-code-file
file.164.path=.specify/specs/099-speckit-seal/code-review.md
file.164.verdict=skipped
file.164.reason=non-code-file
file.165.path=.specify/specs/099-speckit-seal/contracts/merge-back.contract.md
file.165.verdict=skipped
file.165.reason=non-code-file
file.166.path=.specify/specs/099-speckit-seal/contracts/records-and-boundaries.contract.md
file.166.verdict=skipped
file.166.reason=non-code-file
file.167.path=.specify/specs/099-speckit-seal/contracts/seal-engine.contract.md
file.167.verdict=skipped
file.167.reason=non-code-file
file.168.path=.specify/specs/099-speckit-seal/contracts/status-sealed.contract.md
file.168.verdict=skipped
file.168.reason=non-code-file
file.169.path=.specify/specs/099-speckit-seal/coverage-baseline.txt
file.169.verdict=skipped
file.169.reason=non-code-file
file.170.path=.specify/specs/099-speckit-seal/data-model.md
file.170.verdict=skipped
file.170.reason=non-code-file
file.171.path=.specify/specs/099-speckit-seal/feature-ref.md
file.171.verdict=skipped
file.171.reason=non-code-file
file.172.path=.specify/specs/099-speckit-seal/notes/pre-change-measurements.md
file.172.verdict=skipped
file.172.reason=non-code-file
file.173.path=.specify/specs/099-speckit-seal/notes/quickstart-run.md
file.173.verdict=skipped
file.173.reason=non-code-file
file.174.path=.specify/specs/099-speckit-seal/notes/red-first-evidence.md
file.174.verdict=skipped
file.174.reason=non-code-file
file.175.path=.specify/specs/099-speckit-seal/plan.md
file.175.verdict=skipped
file.175.reason=non-code-file
file.176.path=.specify/specs/099-speckit-seal/quickstart.md
file.176.verdict=skipped
file.176.reason=non-code-file
file.177.path=.specify/specs/099-speckit-seal/requirements.md
file.177.verdict=skipped
file.177.reason=non-code-file
file.178.path=.specify/specs/099-speckit-seal/research.md
file.178.verdict=skipped
file.178.reason=non-code-file
file.179.path=.specify/specs/099-speckit-seal/review.md
file.179.verdict=skipped
file.179.reason=non-code-file
file.180.path=.specify/specs/099-speckit-seal/tasks.md
file.180.verdict=skipped
file.180.reason=non-code-file
file.181.path=.specify/specs/099-speckit-seal/test-evidence/074-dated-record-hashes-before.txt
file.181.verdict=skipped
file.181.reason=non-code-file
file.182.path=.specify/specs/099-speckit-seal/test-evidence/074-dated-record-hashes-rerun-before.txt
file.182.verdict=skipped
file.182.reason=non-code-file
file.183.path=.specify/specs/099-speckit-seal/test-evidence/074-factory-resolutions.md
file.183.verdict=skipped
file.183.reason=non-code-file
file.184.path=.specify/specs/099-speckit-seal/test-evidence/074-merge-apply-rerun-20261111.txt
file.184.verdict=skipped
file.184.reason=non-code-file
file.185.path=.specify/specs/099-speckit-seal/test-evidence/074-merge-apply.txt
file.185.verdict=skipped
file.185.reason=non-code-file
file.186.path=.specify/specs/099-speckit-seal/test-evidence/074-merge-checks-rerun-20261111.txt
file.186.verdict=skipped
file.186.reason=non-code-file
file.187.path=.specify/specs/099-speckit-seal/test-evidence/074-merge-checks.txt
file.187.verdict=skipped
file.187.reason=non-code-file
file.188.path=.specify/specs/099-speckit-seal/test-evidence/074-merge-plan-after.json
file.188.verdict=skipped
file.188.reason=non-code-file
file.189.path=.specify/specs/099-speckit-seal/test-evidence/074-merge-plan-after.txt
file.189.verdict=skipped
file.189.reason=non-code-file
file.190.path=.specify/specs/099-speckit-seal/test-evidence/074-merge-plan-before.json
file.190.verdict=skipped
file.190.reason=non-code-file
file.191.path=.specify/specs/099-speckit-seal/test-evidence/074-merge-plan-before.txt
file.191.verdict=skipped
file.191.reason=non-code-file
file.192.path=.specify/specs/099-speckit-seal/test-evidence/074-merge-plan-rerun-20261111.json
file.192.verdict=skipped
file.192.reason=non-code-file
file.193.path=.specify/specs/099-speckit-seal/test-evidence/074-merge-plan-rerun-20261111.txt
file.193.verdict=skipped
file.193.reason=non-code-file
file.194.path=.specify/specs/099-speckit-seal/test-evidence/074-pre-round-readings.txt
file.194.verdict=skipped
file.194.reason=non-code-file
file.195.path=.specify/specs/099-speckit-seal/test-evidence/074-rerun-before-snapshot-20261111.txt
file.195.verdict=skipped
file.195.reason=non-code-file
file.196.path=.specify/specs/099-speckit-seal/test-evidence/074-round-20261110.txt
file.196.verdict=skipped
file.196.reason=non-code-file
file.197.path=.specify/specs/099-speckit-seal/test-evidence/074-round-repair-r1-20261111.txt
file.197.verdict=skipped
file.197.reason=non-code-file
file.198.path=.specify/specs/099-speckit-seal/test-evidence/074-round-rerun-20261111.txt
file.198.verdict=skipped
file.198.reason=non-code-file
file.199.path=.specify/specs/099-speckit-seal/test-evidence/analyze-coverage-2026-11-10.json
file.199.verdict=skipped
file.199.reason=non-code-file
file.200.path=.specify/specs/099-speckit-seal/test-evidence/analyze-coverage-r2-2026-11-10.json
file.200.verdict=skipped
file.200.reason=non-code-file
file.201.path=.specify/specs/099-speckit-seal/test-evidence/analyze-coverage-r3-2026-11-10.json
file.201.verdict=skipped
file.201.reason=non-code-file
file.202.path=.specify/specs/099-speckit-seal/test-evidence/analyze-gates-2026-11-10.txt
file.202.verdict=skipped
file.202.reason=non-code-file
file.203.path=.specify/specs/099-speckit-seal/test-evidence/analyze-merged-2026-11-10.md
file.203.verdict=skipped
file.203.reason=non-code-file
file.204.path=.specify/specs/099-speckit-seal/test-evidence/analyze-merged-r2-2026-11-10.md
file.204.verdict=skipped
file.204.reason=non-code-file
file.205.path=.specify/specs/099-speckit-seal/test-evidence/analyze-merged-r3-2026-11-10.md
file.205.verdict=skipped
file.205.reason=non-code-file
file.206.path=.specify/specs/099-speckit-seal/test-evidence/analyze-r2-gates-2026-11-10.txt
file.206.verdict=skipped
file.206.reason=non-code-file
file.207.path=.specify/specs/099-speckit-seal/test-evidence/analyze-r3-gates-2026-11-10.txt
file.207.verdict=skipped
file.207.reason=non-code-file
file.208.path=.specify/specs/099-speckit-seal/test-evidence/analyze-repair-dispositions-r1-2026-11-10.md
file.208.verdict=skipped
file.208.reason=non-code-file
file.209.path=.specify/specs/099-speckit-seal/test-evidence/analyze-repair-dispositions-r2-2026-11-10.md
file.209.verdict=skipped
file.209.reason=non-code-file
file.210.path=.specify/specs/099-speckit-seal/test-evidence/analyze-repair-gates-r1-2026-11-10.txt
file.210.verdict=skipped
file.210.reason=non-code-file
file.211.path=.specify/specs/099-speckit-seal/test-evidence/analyze-repair-gates-r2-2026-11-10.txt
file.211.verdict=skipped
file.211.reason=non-code-file
file.212.path=.specify/specs/099-speckit-seal/test-evidence/baseline-full-suite-20261110T150720Z.txt
file.212.verdict=skipped
file.212.reason=non-code-file
file.213.path=.specify/specs/099-speckit-seal/test-evidence/boundaries-audit.txt
file.213.verdict=skipped
file.213.reason=non-code-file
file.214.path=.specify/specs/099-speckit-seal/test-evidence/checklist-gates-2026-11-10.txt
file.214.verdict=skipped
file.214.reason=non-code-file
file.215.path=.specify/specs/099-speckit-seal/test-evidence/checklist-readings-2026-11-10.txt
file.215.verdict=skipped
file.215.reason=non-code-file
file.216.path=.specify/specs/099-speckit-seal/test-evidence/clarify-stage-checks.txt
file.216.verdict=skipped
file.216.reason=non-code-file
file.217.path=.specify/specs/099-speckit-seal/test-evidence/closure-rerun-20261111.txt
file.217.verdict=skipped
file.217.reason=non-code-file
file.218.path=.specify/specs/099-speckit-seal/test-evidence/closure-verdict-099-p9b.json
file.218.verdict=skipped
file.218.reason=non-code-file
file.219.path=.specify/specs/099-speckit-seal/test-evidence/closure-verdict-099-preflip.json
file.219.verdict=skipped
file.219.reason=non-code-file
file.220.path=.specify/specs/099-speckit-seal/test-evidence/closure-verdict-099.json
file.220.verdict=skipped
file.220.reason=non-code-file
file.221.path=.specify/specs/099-speckit-seal/test-evidence/coverage-final.txt
file.221.verdict=skipped
file.221.reason=non-code-file
file.222.path=.specify/specs/099-speckit-seal/test-evidence/decomposition-plan.txt
file.222.verdict=skipped
file.222.reason=non-code-file
file.223.path=.specify/specs/099-speckit-seal/test-evidence/f1-red-first-20261111.txt
file.223.verdict=skipped
file.223.reason=non-code-file
file.224.path=.specify/specs/099-speckit-seal/test-evidence/f3-supersede-claims-20261111.txt
file.224.verdict=skipped
file.224.reason=non-code-file
file.225.path=.specify/specs/099-speckit-seal/test-evidence/final-failed-parallel-sample-20261111.txt
file.225.verdict=skipped
file.225.reason=non-code-file
file.226.path=.specify/specs/099-speckit-seal/test-evidence/final-failed.txt
file.226.verdict=skipped
file.226.reason=non-code-file
file.227.path=.specify/specs/099-speckit-seal/test-evidence/final-mirror-checks.txt
file.227.verdict=skipped
file.227.reason=non-code-file
file.228.path=.specify/specs/099-speckit-seal/test-evidence/final-suite-20261111.txt
file.228.verdict=skipped
file.228.reason=non-code-file
file.229.path=.specify/specs/099-speckit-seal/test-evidence/final-suite-serial-20261111.txt
file.229.verdict=skipped
file.229.reason=non-code-file
file.230.path=.specify/specs/099-speckit-seal/test-evidence/final-suite.txt
file.230.verdict=skipped
file.230.reason=non-code-file
file.231.path=.specify/specs/099-speckit-seal/test-evidence/flow-class-lookup.txt
file.231.verdict=skipped
file.231.reason=non-code-file
file.232.path=.specify/specs/099-speckit-seal/test-evidence/merge-apply-checks.txt
file.232.verdict=skipped
file.232.reason=non-code-file
file.233.path=.specify/specs/099-speckit-seal/test-evidence/p1-status-domain-20261110.txt
file.233.verdict=skipped
file.233.reason=non-code-file
file.234.path=.specify/specs/099-speckit-seal/test-evidence/p2-engine-contract-20261110.txt
file.234.verdict=skipped
file.234.reason=non-code-file
file.235.path=.specify/specs/099-speckit-seal/test-evidence/p3-merge-plan-20261111.txt
file.235.verdict=skipped
file.235.reason=non-code-file
file.236.path=.specify/specs/099-speckit-seal/test-evidence/p5-red-first-20261111.txt
file.236.verdict=skipped
file.236.reason=non-code-file
file.237.path=.specify/specs/099-speckit-seal/test-evidence/p5-seal-20261111.txt
file.237.verdict=skipped
file.237.reason=non-code-file
file.238.path=.specify/specs/099-speckit-seal/test-evidence/p6-archive-gate-20261111.txt
file.238.verdict=skipped
file.238.reason=non-code-file
file.239.path=.specify/specs/099-speckit-seal/test-evidence/p6-red-first-20261111.txt
file.239.verdict=skipped
file.239.reason=non-code-file
file.240.path=.specify/specs/099-speckit-seal/test-evidence/p7-adjacent-20261111.txt
file.240.verdict=skipped
file.240.reason=non-code-file
file.241.path=.specify/specs/099-speckit-seal/test-evidence/p7-adjacent2-20261111.txt
file.241.verdict=skipped
file.241.reason=non-code-file
file.242.path=.specify/specs/099-speckit-seal/test-evidence/p7-adjacent3-20261111.txt
file.242.verdict=skipped
file.242.reason=non-code-file
file.243.path=.specify/specs/099-speckit-seal/test-evidence/p7-adjacent4-20261111.txt
file.243.verdict=skipped
file.243.reason=non-code-file
file.244.path=.specify/specs/099-speckit-seal/test-evidence/p7-command-surface-20261111.txt
file.244.verdict=skipped
file.244.reason=non-code-file
file.245.path=.specify/specs/099-speckit-seal/test-evidence/p7-red-first-pins-20261111.txt
file.245.verdict=skipped
file.245.reason=non-code-file
file.246.path=.specify/specs/099-speckit-seal/test-evidence/p7-red-first-related-pins-20261111.txt
file.246.verdict=skipped
file.246.reason=non-code-file
file.247.path=.specify/specs/099-speckit-seal/test-evidence/p7-red-first-template-only-20261111.txt
file.247.verdict=skipped
file.247.reason=non-code-file
file.248.path=.specify/specs/099-speckit-seal/test-evidence/p7-seal-regression-20261111.txt
file.248.verdict=skipped
file.248.reason=non-code-file
file.249.path=.specify/specs/099-speckit-seal/test-evidence/p8b-dispositions-20261111.md
file.249.verdict=skipped
file.249.reason=non-code-file
file.250.path=.specify/specs/099-speckit-seal/test-evidence/p8b-red-first-20261111.txt
file.250.verdict=skipped
file.250.reason=non-code-file
file.251.path=.specify/specs/099-speckit-seal/test-evidence/p8b-suite-20261111.txt
file.251.verdict=skipped
file.251.reason=non-code-file
file.252.path=.specify/specs/099-speckit-seal/test-evidence/plan-stage-checks.txt
file.252.verdict=skipped
file.252.reason=non-code-file
file.253.path=.specify/specs/099-speckit-seal/test-evidence/post-flip-targeted.txt
file.253.verdict=skipped
file.253.reason=non-code-file
file.254.path=.specify/specs/099-speckit-seal/test-evidence/pre-analyze-requirements.txt
file.254.verdict=skipped
file.254.reason=non-code-file
file.255.path=.specify/specs/099-speckit-seal/test-evidence/review-repair-dispositions-r1-2026-11-11.md
file.255.verdict=skipped
file.255.reason=non-code-file
file.256.path=.specify/specs/099-speckit-seal/test-evidence/review-repair-r1-required-suites-20261111.txt
file.256.verdict=skipped
file.256.reason=non-code-file
file.257.path=.specify/specs/099-speckit-seal/test-evidence/review-repair-r1-suites-20261111.txt
file.257.verdict=skipped
file.257.reason=non-code-file
file.258.path=.specify/specs/099-speckit-seal/test-evidence/t041-rerun-20261111.txt
file.258.verdict=skipped
file.258.reason=non-code-file
file.259.path=.specify/specs/099-speckit-seal/test-evidence/t050-replay-repair-r1-20261111.json
file.259.verdict=skipped
file.259.reason=non-code-file
file.260.path=.specify/specs/099-speckit-seal/test-evidence/t050-replay-repair-r1-20261111.txt
file.260.verdict=skipped
file.260.reason=non-code-file
file.261.path=.specify/specs/099-speckit-seal/test-evidence/t050-rerun-20261111.json
file.261.verdict=skipped
file.261.reason=non-code-file
file.262.path=.specify/specs/099-speckit-seal/test-evidence/t050-rerun-20261111.txt
file.262.verdict=skipped
file.262.reason=non-code-file
file.263.path=.specify/specs/099-speckit-seal/test-evidence/tasks-stage-checks.txt
file.263.verdict=skipped
file.263.reason=non-code-file
file.264.path=.specify/specs/099-speckit-seal/test-evidence/validate-requirements.txt
file.264.verdict=skipped
file.264.reason=non-code-file
file.265.path=.specify/specs/099-speckit-seal/verification.md
file.265.verdict=skipped
file.265.reason=non-code-file
file.266.path=.specify/templates/feature-details-template.md
file.266.verdict=skipped
file.266.reason=generated
file.267.path=.specify/templates/feature-index-template.md
file.267.verdict=skipped
file.267.reason=generated
file.268.path=.specify/templates/plan-template.md
file.268.verdict=skipped
file.268.reason=generated
file.269.path=docs/reference/commands/seal.md
file.269.verdict=skipped
file.269.reason=non-code-file
file.270.path=scripts/python/account-clause-coverage.py
file.270.verdict=reviewed
file.271.path=scripts/python/closure-acceptance-check.py
file.271.verdict=skipped
file.271.reason=size-guard-focus-not-reviewed
file.272.path=scripts/python/non-disposable-check.py
file.272.verdict=skipped
file.272.reason=size-guard-focus-not-reviewed
file.273.path=scripts/python/seal-utils.py
file.273.verdict=reviewed
file.274.path=scripts/python/validate-tasks.py
file.274.verdict=reviewed
file.275.path=shared/definitions/flow-class-definitions.md
file.275.verdict=skipped
file.275.reason=non-code-file
file.276.path=shared/definitions/non-disposable-definitions.md
file.276.verdict=skipped
file.276.reason=non-code-file
file.277.path=shared/definitions/probe-definitions.md
file.277.verdict=skipped
file.277.reason=non-code-file
file.278.path=shared/definitions/sdd-routing-definitions.md
file.278.verdict=skipped
file.278.reason=non-code-file
file.279.path=shared/definitions/subagent-definitions.md
file.279.verdict=skipped
file.279.reason=non-code-file
file.280.path=shared/guidelines/better-harness.md
file.280.verdict=skipped
file.280.reason=non-code-file
file.281.path=shared/workflow/acceptance-hardening.md
file.281.verdict=skipped
file.281.reason=non-code-file
file.282.path=shared/workflow/expression-gates.md
file.282.verdict=skipped
file.282.reason=non-code-file
file.283.path=shared/workflow/feature-integration.md
file.283.verdict=skipped
file.283.reason=non-code-file
file.284.path=skills/external/sdd-loop-driver/SKILL.md
file.284.verdict=skipped
file.284.reason=non-code-file
file.285.path=skills/external/sdd-loop-driver/references/decomposition-model.md
file.285.verdict=skipped
file.285.reason=non-code-file
file.286.path=skills/external/sdd-loop-driver/references/nested-invocation.md
file.286.verdict=skipped
file.286.reason=non-code-file
file.287.path=skills/internal/create-team/SKILL.md
file.287.verdict=skipped
file.287.reason=non-code-file
file.288.path=skills/internal/create-team/references/goal.md
file.288.verdict=skipped
file.288.reason=non-code-file
file.289.path=skills/internal/manage-features/SKILL.md
file.289.verdict=skipped
file.289.reason=non-code-file
file.290.path=skills/internal/sanitize-materials/SKILL.md
file.290.verdict=skipped
file.290.reason=non-code-file
file.291.path=skills/internal/seal-artifact/SKILL.md
file.291.verdict=skipped
file.291.reason=non-code-file
file.292.path=templates/commands/seal.md
file.292.verdict=skipped
file.292.reason=non-code-file
file.293.path=templates/feature-details-template.md
file.293.verdict=skipped
file.293.reason=non-code-file
file.294.path=templates/feature-index-template.md
file.294.verdict=skipped
file.294.reason=non-code-file
file.295.path=templates/plan-template.md
file.295.verdict=skipped
file.295.reason=non-code-file
file.296.path=tests/contract/test_acceptance_state_machine.py
file.296.verdict=skipped
file.296.reason=size-guard-focus-not-reviewed
file.297.path=tests/contract/test_clause_coverage.py
file.297.verdict=reviewed
file.298.path=tests/contract/test_docs_step_injection.py
file.298.verdict=skipped
file.298.reason=size-guard-focus-not-reviewed
file.299.path=tests/contract/test_expression_compatibility.py
file.299.verdict=skipped
file.299.reason=size-guard-focus-not-reviewed
file.300.path=tests/contract/test_fast_fail_discipline.py
file.300.verdict=skipped
file.300.reason=size-guard-focus-not-reviewed
file.301.path=tests/contract/test_feedback_command_classification.py
file.301.verdict=skipped
file.301.reason=size-guard-focus-not-reviewed
file.302.path=tests/contract/test_flow_class_ledger.py
file.302.verdict=skipped
file.302.reason=size-guard-focus-not-reviewed
file.303.path=tests/contract/test_humanize_command_surface.py
file.303.verdict=skipped
file.303.reason=size-guard-focus-not-reviewed
file.304.path=tests/contract/test_migration_distribution.py
file.304.verdict=skipped
file.304.reason=size-guard-focus-not-reviewed
file.305.path=tests/contract/test_nested_run_report.py
file.305.verdict=skipped
file.305.reason=size-guard-focus-not-reviewed
file.306.path=tests/contract/test_nested_sdd_invocation.py
file.306.verdict=skipped
file.306.reason=size-guard-focus-not-reviewed
file.307.path=tests/contract/test_run_skills_wiring.py
file.307.verdict=skipped
file.307.reason=size-guard-focus-not-reviewed
file.308.path=tests/contract/test_script_interface_contract.py
file.308.verdict=skipped
file.308.reason=size-guard-focus-not-reviewed
file.309.path=tests/contract/test_sdd_routing_definitions.py
file.309.verdict=skipped
file.309.reason=size-guard-focus-not-reviewed
file.310.path=tests/contract/test_seal_archive_gate.py
file.310.verdict=skipped
file.310.reason=size-guard-focus-not-reviewed
file.311.path=tests/contract/test_seal_boundaries.py
file.311.verdict=skipped
file.311.reason=size-guard-focus-not-reviewed
file.312.path=tests/contract/test_seal_concurrency_and_readonly.py
file.312.verdict=skipped
file.312.reason=size-guard-focus-not-reviewed
file.313.path=tests/contract/test_seal_engine_contract.py
file.313.verdict=skipped
file.313.reason=size-guard-focus-not-reviewed
file.314.path=tests/contract/test_seal_merge_apply.py
file.314.verdict=skipped
file.314.reason=size-guard-focus-not-reviewed
file.315.path=tests/contract/test_seal_merge_plan.py
file.315.verdict=skipped
file.315.reason=size-guard-focus-not-reviewed
file.316.path=tests/contract/test_seal_seal.py
file.316.verdict=reviewed
file.317.path=tests/contract/test_sealed_status_domain.py
file.317.verdict=skipped
file.317.reason=size-guard-focus-not-reviewed
file.318.path=tests/contract/test_skill_layer_visibility_guards.py
file.318.verdict=skipped
file.318.reason=size-guard-focus-not-reviewed
file.319.path=tests/contract/test_status_gate_owner.py
file.319.verdict=skipped
file.319.reason=size-guard-focus-not-reviewed
file.320.path=tests/fixtures/seal/conflict-injections/.specify/specs/099-fixture-parent/contracts/core.contract.md
file.320.verdict=skipped
file.320.reason=non-code-file
file.321.path=tests/fixtures/seal/conflict-injections/.specify/specs/099-fixture-parent/contracts/parent.contract.md
file.321.verdict=skipped
file.321.reason=non-code-file
file.322.path=tests/fixtures/seal/conflict-injections/.specify/specs/099-fixture-parent/plan.md
file.322.verdict=skipped
file.322.reason=non-code-file
file.323.path=tests/fixtures/seal/conflict-injections/.specify/specs/099-fixture-parent/requirements.md
file.323.verdict=skipped
file.323.reason=non-code-file
file.324.path=tests/fixtures/seal/conflict-injections/.specify/specs/099-fixture-parent/tasks.md
file.324.verdict=skipped
file.324.reason=non-code-file
file.325.path=tests/fixtures/seal/conflict-injections/.specify/specs/099a-fixture-conflict/contracts/alpha.contract.md
file.325.verdict=skipped
file.325.reason=non-code-file
file.326.path=tests/fixtures/seal/conflict-injections/.specify/specs/099a-fixture-conflict/contracts/core.contract.md
file.326.verdict=skipped
file.326.reason=non-code-file
file.327.path=tests/fixtures/seal/conflict-injections/.specify/specs/099a-fixture-conflict/plan.md
file.327.verdict=skipped
file.327.reason=non-code-file
file.328.path=tests/fixtures/seal/conflict-injections/.specify/specs/099a-fixture-conflict/requirements.md
file.328.verdict=skipped
file.328.reason=non-code-file
file.329.path=tests/fixtures/seal/conflict-injections/.specify/specs/099b-fixture-conflict/requirements.md
file.329.verdict=skipped
file.329.reason=non-code-file
file.330.path=tests/fixtures/seal/conflict-injections/.specify/specs/099y-fixture-name-only/requirements.md
file.330.verdict=skipped
file.330.reason=non-code-file
file.331.path=tests/fixtures/seal/conflict-injections/.specify/specs/slice-099z-declared-only/requirements.md
file.331.verdict=skipped
file.331.reason=non-code-file
file.332.path=tests/fixtures/seal/conflict-injections/.specify/state/099-fixture-parent.md
file.332.verdict=skipped
file.332.reason=non-code-file
file.333.path=tests/fixtures/seal/conflict-injections/skills/internal/demo-factory/SKILL.md
file.333.verdict=skipped
file.333.reason=non-code-file
file.334.path=tests/fixtures/seal/factory-doc/.specify/specs/099-fixture-parent/requirements.md
file.334.verdict=skipped
file.334.reason=non-code-file
file.335.path=tests/fixtures/seal/factory-doc/.specify/specs/099a-fixture-fd/requirements.md
file.335.verdict=skipped
file.335.reason=non-code-file
file.336.path=tests/fixtures/seal/factory-doc/.specify/state/099-fixture-parent.md
file.336.verdict=skipped
file.336.reason=non-code-file
file.337.path=tests/fixtures/seal/factory-doc/skills/internal/demo-factory/SKILL.md
file.337.verdict=skipped
file.337.reason=non-code-file
file.338.path=tests/fixtures/seal/merged-clean/.specify/specs/099-fixture-merged/code-review.md
file.338.verdict=skipped
file.338.reason=non-code-file
file.339.path=tests/fixtures/seal/merged-clean/.specify/specs/099-fixture-merged/feature-detail.md
file.339.verdict=skipped
file.339.reason=non-code-file
file.340.path=tests/fixtures/seal/merged-clean/.specify/specs/099-fixture-merged/feature-registry.md
file.340.verdict=skipped
file.340.reason=non-code-file
file.341.path=tests/fixtures/seal/merged-clean/.specify/specs/099-fixture-merged/merge-manifest.json
file.341.verdict=skipped
file.341.reason=non-code-file
file.342.path=tests/fixtures/seal/merged-clean/.specify/specs/099-fixture-merged/plan.md
file.342.verdict=skipped
file.342.reason=non-code-file
file.343.path=tests/fixtures/seal/merged-clean/.specify/specs/099-fixture-merged/requirements.md
file.343.verdict=skipped
file.343.reason=non-code-file
file.344.path=tests/fixtures/seal/merged-clean/.specify/specs/099-fixture-merged/review.md
file.344.verdict=skipped
file.344.reason=non-code-file
file.345.path=tests/fixtures/seal/merged-clean/.specify/specs/099-fixture-merged/tasks.md
file.345.verdict=skipped
file.345.reason=non-code-file
file.346.path=tests/fixtures/seal/merged-clean/.specify/specs/099-fixture-merged/test-evidence/run-2026-11-05.txt
file.346.verdict=skipped
file.346.reason=non-code-file
file.347.path=tests/fixtures/seal/merged-clean/.specify/specs/099-fixture-merged/test-evidence/smoke.txt
file.347.verdict=skipped
file.347.reason=non-code-file
file.348.path=tests/fixtures/seal/merged-clean/.specify/specs/099-fixture-merged/verification.md
file.348.verdict=skipped
file.348.reason=non-code-file
file.349.path=tests/fixtures/seal/merged-clean/.specify/specs/099a-fixture-slice/requirements.md
file.349.verdict=skipped
file.349.reason=non-code-file
file.350.path=tests/fixtures/seal/merged-clean/.specify/specs/099a-fixture-slice/review.md
file.350.verdict=skipped
file.350.reason=non-code-file
file.351.path=tests/fixtures/seal/merged-clean/.specify/specs/099a-fixture-slice/test-evidence/run-2026-11-05.txt
file.351.verdict=skipped
file.351.reason=non-code-file
file.352.path=tests/fixtures/seal/merged-clean/.specify/specs/099a-fixture-slice/verification.md
file.352.verdict=skipped
file.352.reason=non-code-file
file.353.path=tests/fixtures/seal/seal-refusals/closure-input-defect/.specify/specs/099-fixture-clean/code-review.md
file.353.verdict=skipped
file.353.reason=non-code-file
file.354.path=tests/fixtures/seal/seal-refusals/closure-input-defect/.specify/specs/099-fixture-clean/feature-detail.md
file.354.verdict=skipped
file.354.reason=non-code-file
file.355.path=tests/fixtures/seal/seal-refusals/closure-input-defect/.specify/specs/099-fixture-clean/feature-registry.md
file.355.verdict=skipped
file.355.reason=non-code-file
file.356.path=tests/fixtures/seal/seal-refusals/closure-input-defect/.specify/specs/099-fixture-clean/plan.md
file.356.verdict=skipped
file.356.reason=non-code-file
file.357.path=tests/fixtures/seal/seal-refusals/closure-input-defect/.specify/specs/099-fixture-clean/requirements.md
file.357.verdict=skipped
file.357.reason=non-code-file
file.358.path=tests/fixtures/seal/seal-refusals/closure-input-defect/.specify/specs/099-fixture-clean/review.md
file.358.verdict=skipped
file.358.reason=non-code-file
file.359.path=tests/fixtures/seal/seal-refusals/closure-input-defect/.specify/specs/099-fixture-clean/tasks.md
file.359.verdict=skipped
file.359.reason=non-code-file
file.360.path=tests/fixtures/seal/seal-refusals/closure-input-defect/.specify/specs/099-fixture-clean/test-evidence/smoke.txt
file.360.verdict=skipped
file.360.reason=non-code-file
file.361.path=tests/fixtures/seal/seal-refusals/closure-input-defect/.specify/specs/099-fixture-clean/verification.md
file.361.verdict=skipped
file.361.reason=non-code-file
file.362.path=tests/fixtures/seal/seal-refusals/closure-refused/.specify/specs/099-fixture-clean/code-review.md
file.362.verdict=skipped
file.362.reason=non-code-file
file.363.path=tests/fixtures/seal/seal-refusals/closure-refused/.specify/specs/099-fixture-clean/feature-detail.md
file.363.verdict=skipped
file.363.reason=non-code-file
file.364.path=tests/fixtures/seal/seal-refusals/closure-refused/.specify/specs/099-fixture-clean/feature-registry.md
file.364.verdict=skipped
file.364.reason=non-code-file
file.365.path=tests/fixtures/seal/seal-refusals/closure-refused/.specify/specs/099-fixture-clean/plan.md
file.365.verdict=skipped
file.365.reason=non-code-file
file.366.path=tests/fixtures/seal/seal-refusals/closure-refused/.specify/specs/099-fixture-clean/requirements.md
file.366.verdict=skipped
file.366.reason=non-code-file
file.367.path=tests/fixtures/seal/seal-refusals/closure-refused/.specify/specs/099-fixture-clean/review.md
file.367.verdict=skipped
file.367.reason=non-code-file
file.368.path=tests/fixtures/seal/seal-refusals/closure-refused/.specify/specs/099-fixture-clean/tasks.md
file.368.verdict=skipped
file.368.reason=non-code-file
file.369.path=tests/fixtures/seal/seal-refusals/closure-refused/.specify/specs/099-fixture-clean/test-evidence/smoke.txt
file.369.verdict=skipped
file.369.reason=non-code-file
file.370.path=tests/fixtures/seal/seal-refusals/closure-refused/.specify/specs/099-fixture-clean/verification.md
file.370.verdict=skipped
file.370.reason=non-code-file
file.371.path=tests/fixtures/seal/seal-refusals/conflict-open/.specify/specs/099-fixture-merged/code-review.md
file.371.verdict=skipped
file.371.reason=non-code-file
file.372.path=tests/fixtures/seal/seal-refusals/conflict-open/.specify/specs/099-fixture-merged/feature-detail.md
file.372.verdict=skipped
file.372.reason=non-code-file
file.373.path=tests/fixtures/seal/seal-refusals/conflict-open/.specify/specs/099-fixture-merged/feature-registry.md
file.373.verdict=skipped
file.373.reason=non-code-file
file.374.path=tests/fixtures/seal/seal-refusals/conflict-open/.specify/specs/099-fixture-merged/merge-manifest.json
file.374.verdict=skipped
file.374.reason=non-code-file
file.375.path=tests/fixtures/seal/seal-refusals/conflict-open/.specify/specs/099-fixture-merged/plan.md
file.375.verdict=skipped
file.375.reason=non-code-file
file.376.path=tests/fixtures/seal/seal-refusals/conflict-open/.specify/specs/099-fixture-merged/requirements.md
file.376.verdict=skipped
file.376.reason=non-code-file
file.377.path=tests/fixtures/seal/seal-refusals/conflict-open/.specify/specs/099-fixture-merged/review.md
file.377.verdict=skipped
file.377.reason=non-code-file
file.378.path=tests/fixtures/seal/seal-refusals/conflict-open/.specify/specs/099-fixture-merged/tasks.md
file.378.verdict=skipped
file.378.reason=non-code-file
file.379.path=tests/fixtures/seal/seal-refusals/conflict-open/.specify/specs/099-fixture-merged/test-evidence/run-2026-11-05.txt
file.379.verdict=skipped
file.379.reason=non-code-file
file.380.path=tests/fixtures/seal/seal-refusals/conflict-open/.specify/specs/099-fixture-merged/test-evidence/smoke.txt
file.380.verdict=skipped
file.380.reason=non-code-file
file.381.path=tests/fixtures/seal/seal-refusals/conflict-open/.specify/specs/099-fixture-merged/verification.md
file.381.verdict=skipped
file.381.reason=non-code-file
file.382.path=tests/fixtures/seal/seal-refusals/conflict-open/.specify/specs/099a-fixture-slice/requirements.md
file.382.verdict=skipped
file.382.reason=non-code-file
file.383.path=tests/fixtures/seal/seal-refusals/conflict-open/.specify/specs/099a-fixture-slice/review.md
file.383.verdict=skipped
file.383.reason=non-code-file
file.384.path=tests/fixtures/seal/seal-refusals/conflict-open/.specify/specs/099a-fixture-slice/test-evidence/run-2026-11-05.txt
file.384.verdict=skipped
file.384.reason=non-code-file
file.385.path=tests/fixtures/seal/seal-refusals/conflict-open/.specify/specs/099a-fixture-slice/verification.md
file.385.verdict=skipped
file.385.reason=non-code-file
file.386.path=tests/fixtures/seal/seal-refusals/dirty-spec-tree/.specify/specs/099-fixture-clean/code-review.md
file.386.verdict=skipped
file.386.reason=non-code-file
file.387.path=tests/fixtures/seal/seal-refusals/dirty-spec-tree/.specify/specs/099-fixture-clean/feature-detail.md
file.387.verdict=skipped
file.387.reason=non-code-file
file.388.path=tests/fixtures/seal/seal-refusals/dirty-spec-tree/.specify/specs/099-fixture-clean/feature-registry.md
file.388.verdict=skipped
file.388.reason=non-code-file
file.389.path=tests/fixtures/seal/seal-refusals/dirty-spec-tree/.specify/specs/099-fixture-clean/plan.md
file.389.verdict=skipped
file.389.reason=non-code-file
file.390.path=tests/fixtures/seal/seal-refusals/dirty-spec-tree/.specify/specs/099-fixture-clean/requirements.md
file.390.verdict=skipped
file.390.reason=non-code-file
file.391.path=tests/fixtures/seal/seal-refusals/dirty-spec-tree/.specify/specs/099-fixture-clean/review.md
file.391.verdict=skipped
file.391.reason=non-code-file
file.392.path=tests/fixtures/seal/seal-refusals/dirty-spec-tree/.specify/specs/099-fixture-clean/tasks.md
file.392.verdict=skipped
file.392.reason=non-code-file
file.393.path=tests/fixtures/seal/seal-refusals/dirty-spec-tree/.specify/specs/099-fixture-clean/test-evidence/smoke.txt
file.393.verdict=skipped
file.393.reason=non-code-file
file.394.path=tests/fixtures/seal/seal-refusals/dirty-spec-tree/.specify/specs/099-fixture-clean/verification.md
file.394.verdict=skipped
file.394.reason=non-code-file
file.395.path=tests/fixtures/seal/seal-refusals/from-status-invalid/.specify/specs/099-fixture-clean/code-review.md
file.395.verdict=skipped
file.395.reason=non-code-file
file.396.path=tests/fixtures/seal/seal-refusals/from-status-invalid/.specify/specs/099-fixture-clean/feature-detail.md
file.396.verdict=skipped
file.396.reason=non-code-file
file.397.path=tests/fixtures/seal/seal-refusals/from-status-invalid/.specify/specs/099-fixture-clean/feature-registry.md
file.397.verdict=skipped
file.397.reason=non-code-file
file.398.path=tests/fixtures/seal/seal-refusals/from-status-invalid/.specify/specs/099-fixture-clean/plan.md
file.398.verdict=skipped
file.398.reason=non-code-file
file.399.path=tests/fixtures/seal/seal-refusals/from-status-invalid/.specify/specs/099-fixture-clean/requirements.md
file.399.verdict=skipped
file.399.reason=non-code-file
file.400.path=tests/fixtures/seal/seal-refusals/from-status-invalid/.specify/specs/099-fixture-clean/review.md
file.400.verdict=skipped
file.400.reason=non-code-file
file.401.path=tests/fixtures/seal/seal-refusals/from-status-invalid/.specify/specs/099-fixture-clean/tasks.md
file.401.verdict=skipped
file.401.reason=non-code-file
file.402.path=tests/fixtures/seal/seal-refusals/from-status-invalid/.specify/specs/099-fixture-clean/test-evidence/smoke.txt
file.402.verdict=skipped
file.402.reason=non-code-file
file.403.path=tests/fixtures/seal/seal-refusals/from-status-invalid/.specify/specs/099-fixture-clean/verification.md
file.403.verdict=skipped
file.403.reason=non-code-file
file.404.path=tests/fixtures/seal/seal-refusals/p0-unresolved/.specify/specs/099-fixture-clean/code-review.md
file.404.verdict=skipped
file.404.reason=non-code-file
file.405.path=tests/fixtures/seal/seal-refusals/p0-unresolved/.specify/specs/099-fixture-clean/feature-detail.md
file.405.verdict=skipped
file.405.reason=non-code-file
file.406.path=tests/fixtures/seal/seal-refusals/p0-unresolved/.specify/specs/099-fixture-clean/feature-registry.md
file.406.verdict=skipped
file.406.reason=non-code-file
file.407.path=tests/fixtures/seal/seal-refusals/p0-unresolved/.specify/specs/099-fixture-clean/plan.md
file.407.verdict=skipped
file.407.reason=non-code-file
file.408.path=tests/fixtures/seal/seal-refusals/p0-unresolved/.specify/specs/099-fixture-clean/requirements.md
file.408.verdict=skipped
file.408.reason=non-code-file
file.409.path=tests/fixtures/seal/seal-refusals/p0-unresolved/.specify/specs/099-fixture-clean/review.md
file.409.verdict=skipped
file.409.reason=non-code-file
file.410.path=tests/fixtures/seal/seal-refusals/p0-unresolved/.specify/specs/099-fixture-clean/tasks.md
file.410.verdict=skipped
file.410.reason=non-code-file
file.411.path=tests/fixtures/seal/seal-refusals/p0-unresolved/.specify/specs/099-fixture-clean/test-evidence/smoke.txt
file.411.verdict=skipped
file.411.reason=non-code-file
file.412.path=tests/fixtures/seal/seal-refusals/p0-unresolved/.specify/specs/099-fixture-clean/verification.md
file.412.verdict=skipped
file.412.reason=non-code-file
file.413.path=tests/fixtures/seal/seal-refusals/slice-unclosed/.specify/specs/099-fixture-clean/code-review.md
file.413.verdict=skipped
file.413.reason=non-code-file
file.414.path=tests/fixtures/seal/seal-refusals/slice-unclosed/.specify/specs/099-fixture-clean/feature-detail.md
file.414.verdict=skipped
file.414.reason=non-code-file
file.415.path=tests/fixtures/seal/seal-refusals/slice-unclosed/.specify/specs/099-fixture-clean/feature-registry.md
file.415.verdict=skipped
file.415.reason=non-code-file
file.416.path=tests/fixtures/seal/seal-refusals/slice-unclosed/.specify/specs/099-fixture-clean/plan.md
file.416.verdict=skipped
file.416.reason=non-code-file
file.417.path=tests/fixtures/seal/seal-refusals/slice-unclosed/.specify/specs/099-fixture-clean/requirements.md
file.417.verdict=skipped
file.417.reason=non-code-file
file.418.path=tests/fixtures/seal/seal-refusals/slice-unclosed/.specify/specs/099-fixture-clean/review.md
file.418.verdict=skipped
file.418.reason=non-code-file
file.419.path=tests/fixtures/seal/seal-refusals/slice-unclosed/.specify/specs/099-fixture-clean/tasks.md
file.419.verdict=skipped
file.419.reason=non-code-file
file.420.path=tests/fixtures/seal/seal-refusals/slice-unclosed/.specify/specs/099-fixture-clean/test-evidence/smoke.txt
file.420.verdict=skipped
file.420.reason=non-code-file
file.421.path=tests/fixtures/seal/seal-refusals/slice-unclosed/.specify/specs/099-fixture-clean/verification.md
file.421.verdict=skipped
file.421.reason=non-code-file
file.422.path=tests/fixtures/seal/seal-refusals/slice-unclosed/.specify/specs/099a-fixture-open/requirements.md
file.422.verdict=skipped
file.422.reason=non-code-file
file.423.path=tests/fixtures/seal/seal-refusals/slice-unclosed/.specify/specs/099a-fixture-open/tasks.md
file.423.verdict=skipped
file.423.reason=non-code-file
file.424.path=tests/fixtures/seal/seal-refusals/state-drift/.specify/specs/099-fixture-clean/code-review.md
file.424.verdict=skipped
file.424.reason=non-code-file
file.425.path=tests/fixtures/seal/seal-refusals/state-drift/.specify/specs/099-fixture-clean/feature-detail.md
file.425.verdict=skipped
file.425.reason=non-code-file
file.426.path=tests/fixtures/seal/seal-refusals/state-drift/.specify/specs/099-fixture-clean/feature-registry.md
file.426.verdict=skipped
file.426.reason=non-code-file
file.427.path=tests/fixtures/seal/seal-refusals/state-drift/.specify/specs/099-fixture-clean/plan.md
file.427.verdict=skipped
file.427.reason=non-code-file
file.428.path=tests/fixtures/seal/seal-refusals/state-drift/.specify/specs/099-fixture-clean/requirements.md
file.428.verdict=skipped
file.428.reason=non-code-file
file.429.path=tests/fixtures/seal/seal-refusals/state-drift/.specify/specs/099-fixture-clean/review.md
file.429.verdict=skipped
file.429.reason=non-code-file
file.430.path=tests/fixtures/seal/seal-refusals/state-drift/.specify/specs/099-fixture-clean/tasks.md
file.430.verdict=skipped
file.430.reason=non-code-file
file.431.path=tests/fixtures/seal/seal-refusals/state-drift/.specify/specs/099-fixture-clean/test-evidence/smoke.txt
file.431.verdict=skipped
file.431.reason=non-code-file
file.432.path=tests/fixtures/seal/seal-refusals/state-drift/.specify/specs/099-fixture-clean/verification.md
file.432.verdict=skipped
file.432.reason=non-code-file
file.433.path=tests/fixtures/seal/seal-refusals/three-minus-one/.specify/specs/099-fixture-clean/code-review.md
file.433.verdict=skipped
file.433.reason=non-code-file
file.434.path=tests/fixtures/seal/seal-refusals/three-minus-one/.specify/specs/099-fixture-clean/feature-detail.md
file.434.verdict=skipped
file.434.reason=non-code-file
file.435.path=tests/fixtures/seal/seal-refusals/three-minus-one/.specify/specs/099-fixture-clean/feature-registry.md
file.435.verdict=skipped
file.435.reason=non-code-file
file.436.path=tests/fixtures/seal/seal-refusals/three-minus-one/.specify/specs/099-fixture-clean/plan.md
file.436.verdict=skipped
file.436.reason=non-code-file
file.437.path=tests/fixtures/seal/seal-refusals/three-minus-one/.specify/specs/099-fixture-clean/requirements.md
file.437.verdict=skipped
file.437.reason=non-code-file
file.438.path=tests/fixtures/seal/seal-refusals/three-minus-one/.specify/specs/099-fixture-clean/review.md
file.438.verdict=skipped
file.438.reason=non-code-file
file.439.path=tests/fixtures/seal/seal-refusals/three-minus-one/.specify/specs/099-fixture-clean/tasks.md
file.439.verdict=skipped
file.439.reason=non-code-file
file.440.path=tests/fixtures/seal/seal-refusals/three-minus-one/.specify/specs/099-fixture-clean/test-evidence/smoke.txt
file.440.verdict=skipped
file.440.reason=non-code-file
file.441.path=tests/fixtures/seal/seal-refusals/three-minus-one/.specify/specs/099-fixture-clean/verification.md
file.441.verdict=skipped
file.441.reason=non-code-file
file.442.path=tests/fixtures/seal/single-spec/.specify/specs/099-fixture-clean/code-review.md
file.442.verdict=skipped
file.442.reason=non-code-file
file.443.path=tests/fixtures/seal/single-spec/.specify/specs/099-fixture-clean/feature-detail.md
file.443.verdict=skipped
file.443.reason=non-code-file
file.444.path=tests/fixtures/seal/single-spec/.specify/specs/099-fixture-clean/feature-registry.md
file.444.verdict=skipped
file.444.reason=non-code-file
file.445.path=tests/fixtures/seal/single-spec/.specify/specs/099-fixture-clean/plan.md
file.445.verdict=skipped
file.445.reason=non-code-file
file.446.path=tests/fixtures/seal/single-spec/.specify/specs/099-fixture-clean/requirements.md
file.446.verdict=skipped
file.446.reason=non-code-file
file.447.path=tests/fixtures/seal/single-spec/.specify/specs/099-fixture-clean/review.md
file.447.verdict=skipped
file.447.reason=non-code-file
file.448.path=tests/fixtures/seal/single-spec/.specify/specs/099-fixture-clean/tasks.md
file.448.verdict=skipped
file.448.reason=non-code-file
file.449.path=tests/fixtures/seal/single-spec/.specify/specs/099-fixture-clean/test-evidence/smoke.txt
file.449.verdict=skipped
file.449.reason=non-code-file
file.450.path=tests/fixtures/seal/single-spec/.specify/specs/099-fixture-clean/verification.md
file.450.verdict=skipped
file.450.reason=non-code-file
file.451.path=tests/fixtures/seal/split-pair/.specify/specs/099-fixture-parent/checklists/requirements.md
file.451.verdict=skipped
file.451.reason=non-code-file
file.452.path=tests/fixtures/seal/split-pair/.specify/specs/099-fixture-parent/checkpoints/cp-2026-11-01.txt
file.452.verdict=skipped
file.452.reason=non-code-file
file.453.path=tests/fixtures/seal/split-pair/.specify/specs/099-fixture-parent/contracts/core.contract.md
file.453.verdict=skipped
file.453.reason=non-code-file
file.454.path=tests/fixtures/seal/split-pair/.specify/specs/099-fixture-parent/feature-ref.md
file.454.verdict=skipped
file.454.reason=non-code-file
file.455.path=tests/fixtures/seal/split-pair/.specify/specs/099-fixture-parent/plan.md
file.455.verdict=skipped
file.455.reason=non-code-file
file.456.path=tests/fixtures/seal/split-pair/.specify/specs/099-fixture-parent/requirements.md
file.456.verdict=skipped
file.456.reason=non-code-file
file.457.path=tests/fixtures/seal/split-pair/.specify/specs/099-fixture-parent/research.md
file.457.verdict=skipped
file.457.reason=non-code-file
file.458.path=tests/fixtures/seal/split-pair/.specify/specs/099-fixture-parent/tasks.md
file.458.verdict=skipped
file.458.reason=non-code-file
file.459.path=tests/fixtures/seal/split-pair/.specify/specs/099-fixture-parent/test-evidence/run-2026-11-01.txt
file.459.verdict=skipped
file.459.reason=non-code-file
file.460.path=tests/fixtures/seal/split-pair/.specify/specs/099a-fixture-alpha/checklists/plan-review.md
file.460.verdict=skipped
file.460.reason=non-code-file
file.461.path=tests/fixtures/seal/split-pair/.specify/specs/099a-fixture-alpha/checklists/requirements.md
file.461.verdict=skipped
file.461.reason=non-code-file
file.462.path=tests/fixtures/seal/split-pair/.specify/specs/099a-fixture-alpha/checkpoints/cp-2026-11-01.txt
file.462.verdict=skipped
file.462.reason=non-code-file
file.463.path=tests/fixtures/seal/split-pair/.specify/specs/099a-fixture-alpha/code-review.md
file.463.verdict=skipped
file.463.reason=non-code-file
file.464.path=tests/fixtures/seal/split-pair/.specify/specs/099a-fixture-alpha/contracts/core.contract.md
file.464.verdict=skipped
file.464.reason=non-code-file
file.465.path=tests/fixtures/seal/split-pair/.specify/specs/099a-fixture-alpha/contracts/extra-alpha.md
file.465.verdict=skipped
file.465.reason=non-code-file
file.466.path=tests/fixtures/seal/split-pair/.specify/specs/099a-fixture-alpha/data-model.md
file.466.verdict=skipped
file.466.reason=non-code-file
file.467.path=tests/fixtures/seal/split-pair/.specify/specs/099a-fixture-alpha/plan.md
file.467.verdict=skipped
file.467.reason=non-code-file
file.468.path=tests/fixtures/seal/split-pair/.specify/specs/099a-fixture-alpha/requirements.md
file.468.verdict=skipped
file.468.reason=non-code-file
file.469.path=tests/fixtures/seal/split-pair/.specify/specs/099a-fixture-alpha/review.md
file.469.verdict=skipped
file.469.reason=non-code-file
file.470.path=tests/fixtures/seal/split-pair/.specify/specs/099a-fixture-alpha/tasks.md
file.470.verdict=skipped
file.470.reason=non-code-file
file.471.path=tests/fixtures/seal/split-pair/.specify/specs/099a-fixture-alpha/test-evidence/run-2026-11-01.txt
file.471.verdict=skipped
file.471.reason=non-code-file
file.472.path=tests/fixtures/seal/split-pair/.specify/specs/099a-fixture-alpha/verification.md
file.472.verdict=skipped
file.472.reason=non-code-file
file.473.path=tests/fixtures/seal/split-pair/.specify/specs/099b-fixture-beta/checkpoints/cp-2026-11-05.txt
file.473.verdict=skipped
file.473.reason=non-code-file
file.474.path=tests/fixtures/seal/split-pair/.specify/specs/099b-fixture-beta/code-review.md
file.474.verdict=skipped
file.474.reason=non-code-file
file.475.path=tests/fixtures/seal/split-pair/.specify/specs/099b-fixture-beta/contracts/core.contract.md
file.475.verdict=skipped
file.475.reason=non-code-file
file.476.path=tests/fixtures/seal/split-pair/.specify/specs/099b-fixture-beta/plan.md
file.476.verdict=skipped
file.476.reason=non-code-file
file.477.path=tests/fixtures/seal/split-pair/.specify/specs/099b-fixture-beta/requirements.md
file.477.verdict=skipped
file.477.reason=non-code-file
file.478.path=tests/fixtures/seal/split-pair/.specify/specs/099b-fixture-beta/review.md
file.478.verdict=skipped
file.478.reason=non-code-file
file.479.path=tests/fixtures/seal/split-pair/.specify/specs/099b-fixture-beta/tasks.md
file.479.verdict=skipped
file.479.reason=non-code-file
file.480.path=tests/fixtures/seal/split-pair/.specify/specs/099b-fixture-beta/test-evidence/run-2026-11-02.txt
file.480.verdict=skipped
file.480.reason=non-code-file
file.481.path=tests/fixtures/seal/split-pair/.specify/specs/099b-fixture-beta/verification.md
file.481.verdict=skipped
file.481.reason=non-code-file
file.482.path=tests/fixtures/seal/split-pair/.specify/state/099-fixture-parent.md
file.482.verdict=skipped
file.482.reason=non-code-file
file.483.path=tests/integration/test_docs_command_scenarios.py
file.483.verdict=skipped
file.483.reason=size-guard-focus-not-reviewed
file.484.path=tests/integration/test_seal_074_round.py
file.484.verdict=skipped
file.484.reason=size-guard-focus-not-reviewed
file.485.path=tests/integration/test_seal_merge_determinism.py
file.485.verdict=skipped
file.485.reason=size-guard-focus-not-reviewed
<!-- coverage-receipt:end -->
