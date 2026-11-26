# Code Review Report — 代码段 (code segment)

| 属性 | 值 |
|------|-----|
| **分支** | `107-decision-governance` |
| **基准** | `fbab7a45c4a57b596bc32437181ee9eb799ebe60` (`fbab7a45c`) |
| **目标** | `3f0200b421bf284c176592afa34549e7a2c07706` (`3f0200b42`) |
| **基准来源** | `feature-first-commit` |
| **渲染模式** | `renderer: text` |
| **Reviewer** | `Qiming Liu (John)` |
| **日期** | `2026-11-26T06:24:15Z` |

## 变更概览

```
 .claude/commands/speckit.agents.md                 |    2 +
 .claude/commands/speckit.team.md                   |    2 +
 .github/prompts/speckit.agents.prompt.md           |    2 +
 .github/prompts/speckit.team.prompt.md             |    2 +
 .opencode/command/speckit.agents.md                |    2 +
 .opencode/command/speckit.team.md                  |    2 +
 .qoder/agents/sdd-debt-governor.agent.md           |    4 +-
 .qoder/agents/sdd-implement-coordinator.agent.md   |    1 +
 .qoder/agents/sdd-plan-coordinator.agent.md        |    1 +
 .qoder/agents/sdd-review-coordinator.agent.md      |    1 +
 .qoder/agents/sdd-task-coordinator.agent.md        |    1 +
 .qoder/commands/speckit.agents.md                  |    2 +
 .qoder/commands/speckit.team.md                    |    2 +
 .specify/agents/.render-manifest.json              |  312 +-
 .../templates/sdd-implement-coordinator.agent.md   |    1 +
 .../agents/templates/sdd-plan-coordinator.agent.md |    1 +
 .../templates/sdd-review-coordinator.agent.md      |    1 +
 .../agents/templates/sdd-task-coordinator.agent.md |    1 +
 .../106-background-silent-failure/anchor.md        |   26 +
 .../anchoring/107-decision-governance/anchor.md    |   26 +
 .../records/20261125T114538658383Z-0904f023.json   |    1 +
 .../records/20261125T115451874927Z-6db027b5.json   |    1 +
 .../records/20261125T121419791413Z-a4679bfb.json   |    1 +
 .../records/20261125T122810951835Z-56d6e538.json   |    1 +
 .../records/20261125T123555820029Z-80b8b9aa.json   |    1 +
 .../records/20261125T125153331787Z-46e5ff70.json   |    1 +
 .../records/20261125T125926616815Z-eb0837fb.json   |    1 +
 .../records/20261125T132404451045Z-ffd93788.json   |    1 +
 .../records/20261125T134020382137Z-dc4a1b7c.json   |    1 +
 .../records/20261125T135920685209Z-dd809ed0.json   |    1 +
 .../records/20261125T140707830920Z-97a6c8e4.json   |    1 +
 .../records/20261125T142034358066Z-f6b47bfc.json   |    1 +
 .../records/20261125T143217905096Z-b9e267ca.json   |    1 +
 .../records/20261125T160801888488Z-1fb91fea.json   |    1 +
 .../records/20261125T162322617249Z-b3955a58.json   |    1 +
 .../records/20261125T163755432720Z-371d39ee.json   |    1 +
 .../records/20261125T173627505479Z-5caa3c2f.json   |    1 +
 .../records/20261125T173956791454Z-2e94960a.json   |    1 +
 .../records/20261125T180105894081Z-3ac41486.json   |    1 +
 .../records/20261126T020852910406Z-e88542f4.json   |    1 +
 .../records/20261126T032247826756Z-33524863.json   |    1 +
 .../records/20261126T033532112186Z-c50e14d7.json   |    1 +
 .../records/20261126T061350897087Z-27ed0640.json   |    1 +
 .specify/features.md                               |    8 +-
 .specify/features/076-decision-tension-contract.md |    1 +
 .specify/features/095-superagent-role.md           |   28 +-
 .specify/features/107-decision-governance.md       |   68 +
 .../20261125T114609Z-speckit-requirements.md       |   22 +
 .../feedback/20261125T115512Z-speckit-clarify.md   |   23 +
 .specify/feedback/20261125T121425Z-speckit-plan.md |   23 +
 .../feedback/20261125T122816Z-speckit-tasks.md     |   22 +
 .../feedback/20261125T123559Z-speckit-checklist.md |   21 +
 .../20261125T125200Z-skill-analyze-artifacts.md    |   21 +
 .../20261125T125926Z-skill-analyze-artifacts.md    |   19 +
 .../20261125T132404Z-skill-analyze-artifacts.md    |   19 +
 .../20261125T134023Z-skill-analyze-artifacts.md    |   20 +
 .../20261125T135929Z-speckit-requirements.md       |   25 +
 .../20261125T140714Z-skill-clarify-artifact.md     |   22 +
 .../feedback/20261125T142034Z-skill-create-plan.md |   21 +
 .../20261125T143223Z-skill-create-tasks.md         |   21 +
 .../20261125T160807Z-skill-create-checklist.md     |   21 +
 .../20261125T162329Z-skill-analyze-artifacts.md    |   21 +
 .../20261125T163801Z-skill-analyze-artifacts.md    |   21 +
 .../feedback/20261125T173633Z-skill-create-plan.md |   22 +
 .../20261125T174002Z-skill-analyze-artifacts.md    |   23 +
 .../20261125T180117Z-skill-analyze-artifacts.md    |   22 +
 .../20261126T020919Z-skill-analyze-artifacts.md    |   23 +
 .../20261126T032257Z-skill-implement-feature.md    |   22 +
 .../20261126T033532Z-skill-review-sdd-process.md   |   21 +
 .../20261126T061400Z-skill-implement-feature.md    |   24 +
 .specify/glossary.md                               |    1 +
 .specify/instructions.md                           |   10 +
 .specify/register.md                               |   14 +
 ...Z-106-background-silent-failure-requirements.md |   31 +
 ...15521Z-106-background-silent-failure-clarify.md |   31 +
 ...106-background-silent-failure-clarify-repair.md |   33 +
 ...5T121502Z-106-background-silent-failure-plan.md |   34 +
 ...T122912Z-106-background-silent-failure-tasks.md |   36 +
 ...605Z-106-background-silent-failure-checklist.md |   36 +
 ...25221Z-106-background-silent-failure-analyze.md |   56 +
 ...106-background-silent-failure-analyze-repair.md |   57 +
 ...06-background-silent-failure-analyze-repair2.md |   58 +
 ...T140024Z-r20261125T134500Z-107a-requirements.md |   44 +
 ...61125T140844Z-r20261125T134500Z-107a-clarify.md |   46 +
 ...20261125T142103Z-r20261125T134500Z-107a-plan.md |   47 +
 ...0261125T143241Z-r20261125T134500Z-107a-tasks.md |   45 +
 ...125T160827Z-r20261125T134500Z-107a-checklist.md |   45 +
 ...173700Z-r20261125T173500Z-107c-plan-rereview.md |   45 +
 ...315Z-106-background-silent-failure-implement.md |   33 +
 ...033549Z-106-background-silent-failure-review.md |   38 +
 ...26T061407Z-107-decision-governance-implement.md |   30 +
 .specify/scripts/bash/generate-instructions.sh     |   14 +-
 .specify/scripts/python/role-edge-check.py         |  990 ++-
 .specify/scripts/python/validate-decisions.py      | 1209 ++++
 ...-determination-skill-create-plan-093-plan-a1.md |   10 +-
 ...ion-skill-create-plan-r20261110t081104z-b096.md |   10 +-
 ...on-skill-create-tasks-r20261110t081104z-b096.md |   10 +-
 ...ation-speckit-clarify-r20261124t054500z-9b2d.md |   10 +-
 ...n-speckit-requirements-r20261125t022857z-06d.md |   10 +-
 ...n-skill-clarify-artifact-r20261125t022857z-0.md |   10 +-
 ...n-skill-create-checklist-r20261125t022857z-0.md |   10 +-
 ...on-skill-implement-feature-r20261125t022857z.md |   10 +-
 ...n-skill-review-sdd-process-r20261125t022857z.md |   10 +-
 ...n-speckit-requirements-r20261125t113505z-106.md |  204 +
 ...ation-speckit-clarify-r20261125t113505z-106a.md |  204 +
 ...mination-speckit-plan-r20261125t113505z-106a.md |  202 +
 ...ination-speckit-tasks-r20261125t113505z-106a.md |  207 +
 ...ion-speckit-checklist-r20261125t113505z-106a.md |  202 +
 ...on-skill-analyze-artifacts-r20261125t113505z.md |  207 +
 ...on-skill-analyze-artifacts-r20261125t125827z.md |  208 +
 ...on-skill-analyze-artifacts-r20261125t132316z.md |  204 +
 ...on-skill-analyze-artifacts-r20261125t134017z.md |  204 +
 ...n-speckit-requirements-r20261125t134500z-107.md |  190 +
 ...n-skill-clarify-artifact-r20261125t134500z-1.md |  207 +
 ...ion-skill-create-plan-r20261125t134500z-107a.md |  207 +
 ...on-skill-create-tasks-r20261125t134500z-107a.md |  207 +
 ...n-skill-create-checklist-r20261125t134500z-1.md |  202 +
 ...on-skill-analyze-artifacts-r20261125t134500z.md |  225 +
 ...on-skill-analyze-artifacts-r20261125t162400z.md |  225 +
 ...ion-skill-create-plan-r20261125t173500z-107c.md |  213 +
 ...on-skill-analyze-artifacts-r20261125t173750z.md |  203 +
 ...on-skill-analyze-artifacts-r20261125t180013z.md |  224 +
 ...on-skill-analyze-artifacts-r20261126t020820z.md |  224 +
 ...on-skill-implement-feature-r20261125t113505z.md |  219 +
 ...n-skill-review-sdd-process-r20261126t033520z.md |  202 +
 ...on-skill-implement-feature-r20261125t134500z.md |  207 +
 .specify/shared/definitions/agent-definitions.md   |    2 +
 .specify/shared/definitions/anchor-definitions.md  |    2 +
 .../shared/definitions/decision-definitions.md     |  303 +
 .specify/shared/definitions/framework-map.md       |    1 +
 .specify/shared/definitions/goal-definitions.md    |    2 +
 .../shared/definitions/subagent-definitions.md     |    2 +
 .../shared/definitions/superagent-definitions.md   |   87 +-
 .specify/shared/guidelines/confirmation-gates.md   |    2 +
 .specify/shared/guidelines/decision-tension.md     |    3 +-
 .specify/shared/guidelines/fast-fail.md            |    2 +
 .../shared/workflow/external-dispatch-recipes.md   |    8 +-
 .../skills/internal/analyze-artifacts/SKILL.md     |    7 +
 .specify/skills/internal/create-team/SKILL.md      |    6 +-
 .../internal/create-team/scripts/dispatch.sh       |  103 +-
 .../internal/review-feature-quality/SKILL.md       |    7 +
 .../skills/internal/review-sdd-process/SKILL.md    |    6 +
 .specify/skills/internal/run-agent/SKILL.md        |   43 +
 .specify/skills/internal/run-team/SKILL.md         |    2 +
 .specify/skills/sdd-loop-driver/SKILL.md           |    1 +
 .../references/checkpoint-protocol.md              |    1 +
 .../sdd-loop-driver/references/dispatch-recipes.md |    1 +
 .../sdd-loop-driver/references/stage-prompts.md    |    2 +
 .../baseline-failed.txt                            |  218 +
 .../checklists/background-settlement-2026-11-25.md |   94 +
 .../checklists/requirements.md                     |   49 +
 .../checkpoints/01-requirements.md                 |   44 +
 .../checkpoints/02-clarify.md                      |   44 +
 .../checkpoints/03-plan.md                         |   43 +
 .../checkpoints/04-tasks.md                        |   43 +
 .../checkpoints/05-goal-team-activation.md         |   48 +
 .../checkpoints/06-checklist.md                    |   49 +
 .../checkpoints/07-analyze.md                      |   25 +
 .../checkpoints/08-implement.md                    |   25 +
 .../checkpoints/closure.md                         |   33 +
 .../106-background-silent-failure/code-review.md   | 1357 ++++
 .../contracts/carrier-conformance.contract.md      |   54 +
 .../enforcement-and-migration.contract.md          |   46 +
 .../contracts/settlement-contract.contract.md      |   56 +
 .../coverage-baseline.txt                          |  787 +++
 .../106-background-silent-failure/data-model.md    |  163 +
 .../106-background-silent-failure/feature-ref.md   |  102 +
 .../106-background-silent-failure/final-failed.txt |  217 +
 .../specs/106-background-silent-failure/handoff.md |   54 +
 .../notes/pre-change-measurements.md               |   86 +
 .../notes/quickstart-run.md                        |  194 +
 .../notes/red-first-evidence.md                    |  437 ++
 .../specs/106-background-silent-failure/plan.md    |  217 +
 .../106-background-silent-failure/quickstart.md    |  171 +
 .../106-background-silent-failure/requirements.md  |  311 +
 .../106-background-silent-failure/research.md      |   33 +
 .../specs/106-background-silent-failure/review.md  |  355 +
 .../specs/106-background-silent-failure/tasks.md   |  361 +
 .../test-evidence/acceptance-106.md                |  146 +
 .../test-evidence/analyze-domain-w1-r2.jsonl       |   10 +
 .../test-evidence/analyze-domain-w1-r3.jsonl       |    6 +
 .../test-evidence/analyze-domain-w1.jsonl          |   11 +
 .../test-evidence/analyze-domain-w2.jsonl          |   10 +
 .../test-evidence/analyze-domain-w2a-r2.jsonl      |    6 +
 .../test-evidence/analyze-domain-w2a-r3.jsonl      |    6 +
 .../test-evidence/analyze-domain-w2b-r2.jsonl      |    6 +
 .../test-evidence/analyze-domain-w2b-r3.jsonl      |    6 +
 .../test-evidence/analyze-domain-w2c-r2.jsonl      |    6 +
 .../test-evidence/analyze-domain-w2c-r3.jsonl      |    6 +
 .../test-evidence/analyze-domain-w3-r2.jsonl       |   10 +
 .../test-evidence/analyze-domain-w3-r3.jsonl       |    5 +
 .../test-evidence/analyze-domain-w3.jsonl          |   10 +
 .../test-evidence/analyze-incremental-r4.jsonl     |    5 +
 .../test-evidence/analyze-incremental-r5.jsonl     |    6 +
 .../analyze-r4-reused-domain-hashes.txt            |    4 +
 .../test-evidence/analyze-repair-2026-11-25.md     |  136 +
 .../analyze-repair-clause-coverage.txt             |  818 +++
 .../analyze-repair-clause-extract.json             |   37 +
 .../test-evidence/analyze-repair-decomposition.txt |    1 +
 .../test-evidence/analyze-repair-gate-scan.json    |  295 +
 .../analyze-repair-glossary-validate.txt           |    4 +
 .../analyze-repair-pre-analyze-plan.txt            |    2 +
 .../analyze-repair-pre-analyze-requirements.txt    |    2 +
 .../analyze-repair-pre-analyze-tasks.txt           |    2 +
 .../analyze-repair-requirements-validator.txt      |   10 +
 .../analyze-repair-tasks-validator.txt             |    1 +
 .../test-evidence/analyze-repair2-2026-11-25.md    |  110 +
 .../analyze-repair2-clause-coverage.txt            |  818 +++
 .../analyze-repair2-clause-extract.json            |   37 +
 .../analyze-repair2-decomposition.txt              |    1 +
 .../test-evidence/analyze-repair2-gate-scan.json   |  295 +
 .../analyze-repair2-glossary-validate.txt          |    4 +
 .../analyze-repair2-pre-analyze-plan.txt           |    2 +
 .../analyze-repair2-pre-analyze-requirements.txt   |    2 +
 .../analyze-repair2-pre-analyze-tasks.txt          |    2 +
 .../analyze-repair2-requirements-validator.txt     |   10 +
 .../analyze-repair2-tasks-validator.txt            |    1 +
 .../test-evidence/analyze-repair3-2026-11-25.md    |   98 +
 .../analyze-repair3-clause-coverage.txt            |  818 +++
 .../analyze-repair3-clause-extract.json            |   37 +
 .../analyze-repair3-decomposition.txt              |    1 +
 .../test-evidence/analyze-repair3-gate-scan.json   |  295 +
 .../analyze-repair3-glossary-validate.txt          |    4 +
 .../analyze-repair3-pre-analyze-plan.txt           |    2 +
 .../analyze-repair3-pre-analyze-requirements.txt   |    2 +
 .../analyze-repair3-pre-analyze-tasks.txt          |    2 +
 .../analyze-repair3-requirements-validator.txt     |   10 +
 .../test-evidence/analyze-repair3-run-id.txt       |    1 +
 .../analyze-repair3-tasks-validator.txt            |    1 +
 .../test-evidence/analyze-repair4-2026-11-26.md    |   80 +
 .../analyze-repair4-clause-coverage.txt            |  818 +++
 .../analyze-repair4-clause-extract.json            |   37 +
 .../analyze-repair4-decomposition.txt              |    1 +
 .../test-evidence/analyze-repair4-gate-scan.json   |  295 +
 .../analyze-repair4-glossary-validate.txt          |    4 +
 .../analyze-repair4-pre-analyze-plan.txt           |    2 +
 .../analyze-repair4-pre-analyze-requirements.txt   |    2 +
 .../analyze-repair4-pre-analyze-tasks.txt          |    2 +
 .../analyze-repair4-requirements-validator.txt     |   10 +
 .../test-evidence/analyze-repair4-run-id.txt       |    1 +
 .../analyze-repair4-tasks-validator.txt            |    1 +
 .../test-evidence/analyze-report-2026-11-25.md     |  465 ++
 .../test-evidence/analyze-report-r5-2026-11-26.md  |  204 +
 .../test-evidence/analyze.jsonl                    |    1 +
 .../test-evidence/checklist-artifact-counts.txt    |   17 +
 .../checklist-requirements-validator.txt           |   10 +
 .../test-evidence/checklist.jsonl                  |    1 +
 .../test-evidence/clarify.jsonl                    |    1 +
 .../test-evidence/clause-coverage-tasks.txt        |  818 +++
 .../test-evidence/closure-full-run-r2-summary.txt  |    1 +
 .../confirmation-total-red-at-base.txt             |   27 +
 .../test-evidence/decomposition-plan.json          |   12 +
 .../test-evidence/decomposition-plan.stdout.txt    |    1 +
 .../test-evidence/enforcement-honesty.md           |   62 +
 .../test-evidence/exec-quant-analyze-repair.txt    |    1 +
 .../test-evidence/exec-quant-analyze-repair2.txt   |    1 +
 .../test-evidence/exec-quant-analyze-repair3.txt   |    1 +
 .../test-evidence/exec-quant-analyze-repair4.txt   |    1 +
 .../test-evidence/exec-quant-analyze.txt           |    1 +
 .../test-evidence/exec-quant-checklist.txt         |    1 +
 .../test-evidence/exec-quant-clarify.txt           |    2 +
 .../test-evidence/exec-quant-plan.txt              |    1 +
 .../test-evidence/exec-quant-tasks.txt             |    1 +
 .../test-evidence/exec-quant.txt                   |    1 +
 .../feedback-record-analyze-repair.txt             |    9 +
 .../feedback-record-analyze-repair2.txt            |    9 +
 .../feedback-record-analyze-repair3.txt            |    9 +
 .../feedback-record-analyze-repair4.txt            |    9 +
 .../test-evidence/feedback-record-analyze.txt      |    9 +
 .../test-evidence/feedback-record-checklist.txt    |    9 +
 .../test-evidence/feedback-record-clarify.txt      |    9 +
 .../test-evidence/feedback-record-plan.txt         |    9 +
 .../test-evidence/feedback-record-tasks.txt        |    9 +
 .../test-evidence/feedback-record.txt              |    9 +
 .../test-evidence/final-gate.txt                   |   73 +
 .../test-evidence/flow-class-lookup-checklist.txt  |    7 +
 .../test-evidence/flow-class-lookup-clarify.txt    |    8 +
 .../test-evidence/flow-class-lookup-plan.txt       |    7 +
 .../test-evidence/flow-class-lookup.txt            |    7 +
 .../test-evidence/git-access-anomaly.txt           |   11 +
 .../test-evidence/git-commit-attempt-clarify.txt   |   12 +
 .../test-evidence/glossary-proposal-plan.txt       |    5 +
 .../test-evidence/goal-team-activation.txt         |   28 +
 .../test-evidence/implement-baseline-full.txt      | 7210 ++++++++++++++++++++
 .../test-evidence/implement-integration.md         |  106 +
 .../test-evidence/mirror-check-baseline.txt        |   13 +
 .../test-evidence/mutation-drill.md                |  123 +
 .../test-evidence/non-goals-audit.md               |  108 +
 .../test-evidence/plan-stage-2026-11-25.md         |   78 +
 .../test-evidence/plan.jsonl                       |    1 +
 .../test-evidence/pre-analyze-plan-before-fill.txt |    1 +
 .../test-evidence/pre-analyze-plan.json            |  157 +
 .../test-evidence/pre-analyze-plan.stdout.txt      |    2 +
 .../pre-analyze-requirements-clarify.json          |   16 +
 .../pre-analyze-requirements-clarify.stdout.txt    |    3 +
 .../test-evidence/pre-analyze-requirements.json    |   16 +
 .../pre-analyze-requirements.stdout.txt            |    2 +
 .../test-evidence/pre-analyze-tasks.json           |    1 +
 .../test-evidence/pre-analyze-tasks.stdout.txt     |    1 +
 .../quickstart-role-edge-empty-report.json         |   34 +
 .../test-evidence/quickstart-role-edge-help.txt    |   24 +
 .../test-evidence/reaction-drill.md                |   53 +
 .../test-evidence/review-evidence.txt              |   64 +
 .../review-workspace-before-commit.json            |  316 +
 .../test-evidence/review-workspace-postcommit.txt  |    1 +
 .../test-evidence/review.jsonl                     |    1 +
 .../role-edge-report-empty-fbab7a45c.json          |   34 +
 .../run-determination-analyze-repair.txt           |    8 +
 .../run-determination-analyze-repair2.txt          |    8 +
 .../run-determination-analyze-repair3.txt          |    9 +
 .../run-determination-analyze-repair4.txt          |    9 +
 .../test-evidence/run-determination-analyze.txt    |    8 +
 .../test-evidence/run-determination-checklist.txt  |    8 +
 .../test-evidence/run-determination-clarify.txt    |   10 +
 .../test-evidence/run-determination-plan.txt       |    8 +
 .../test-evidence/run-determination-tasks.txt      |    8 +
 .../test-evidence/run-determination.txt            |    9 +
 .../scan-confirmation-gates-baseline.json          |  295 +
 .../test-evidence/super-sub-protocol-fbab7a45c.txt |    8 +
 .../test-evidence/t033-smoke.txt                   |    7 +
 .../test-evidence/tasks-premises.txt               |  108 +
 .../test-evidence/tasks.jsonl                      |    1 +
 .../test-evidence/test-entry-smoke.txt             |    7 +
 .../test-evidence/validate-r4-01.verdicts.json     |   13 +
 .../test-evidence/validate-tasks.json              |  212 +
 .../test-evidence/validate-tasks.stdout.txt        |    1 +
 .../test-evidence/validate-wave1.verdicts.json     |  122 +
 .../test-evidence/validate-wave2.verdicts.json     |   62 +
 .../test-evidence/validate-wave3.verdicts.json     |   52 +
 .../validator-requirements-clarify.txt             |   11 +
 .../test-evidence/validator-requirements.txt       |   10 +
 .../test-evidence/verification-input.md            |   55 +
 .../test-evidence/watch-help-baseline.txt          |   70 +
 .../test-evidence/watch-self-test-baseline.txt     |   40 +
 .../test-evidence/watch-target-fbab7a45c.sh        | 1404 ++++
 ...orkspace-check-analyze-repair-before-commit.txt |    1 +
 .../workspace-check-analyze-repair-postcommit.txt  |    1 +
 ...rkspace-check-analyze-repair2-before-commit.txt |    1 +
 .../workspace-check-analyze-repair2-postcommit.txt |    1 +
 ...rkspace-check-analyze-repair3-before-commit.txt |    1 +
 .../workspace-check-analyze-repair3-postcommit.txt |    1 +
 ...rkspace-check-analyze-repair4-before-commit.txt |    1 +
 .../workspace-check-analyze-repair4-postcommit.txt |    1 +
 .../workspace-check-checklist-postcommit.txt       |    1 +
 .../test-evidence/workspace-check-checklist.txt    |    1 +
 .../workspace-check-clarify-repair.txt             |    4 +
 .../test-evidence/workspace-check-clarify.txt      |    4 +
 .../test-evidence/workspace-check.txt              |    1 +
 .../test-evidence/workspace-plan-after-driver.json |  304 +
 .../test-evidence/workspace-plan-after.json        |    1 +
 .../test-evidence/workspace-plan-before.json       |  304 +
 .../test-evidence/workspace-requirements.json      |  304 +
 .../workspace-snapshot-analyze-before-commit.json  |  304 +
 ...pace-snapshot-analyze-repair-before-commit.json |  304 +
 .../workspace-snapshot-analyze-repair2-before.json |  304 +
 .../workspace-snapshot-analyze-repair3-before.json |  304 +
 .../workspace-snapshot-analyze-repair4-before.json |  312 +
 .../workspace-snapshot-checklist-after.json        |  304 +
 .../workspace-snapshot-checklist-before.json       |  304 +
 .../test-evidence/workspace-tasks-after.json       |  304 +
 .../test-evidence/workspace-tasks-before.json      |  304 +
 .../106-background-silent-failure/verification.md  |   65 +
 .../107-decision-governance/baseline-failed.txt    |  221 +
 .../checklists/decision-governance-2026-11-26.md   |   94 +
 .../checklists/requirements.md                     |   50 +
 .../checkpoints/01-requirements.md                 |   40 +
 .../checkpoints/02-clarify.md                      |   31 +
 .../107-decision-governance/checkpoints/03-plan.md |   31 +
 .../checkpoints/04-tasks.md                        |   31 +
 .../checkpoints/05-goal-team-activation.md         |   34 +
 .../checkpoints/06-checklist.md                    |   26 +
 .../checkpoints/07-analyze.md                      |    6 +
 .../checkpoints/08-implement.md                    |   27 +
 .../contracts/archive-and-audit.contract.md        |   36 +
 .../contracts/enforcement-boundary.contract.md     |   48 +
 .../contracts/migration-and-compat.contract.md     |   32 +
 .../contracts/text-and-options.contract.md         |   38 +
 .../transmission-and-implementation.contract.md    |   36 +
 .../specs/107-decision-governance/data-model.md    |  134 +
 .../specs/107-decision-governance/feature-ref.md   |   73 +
 .specify/specs/107-decision-governance/handoff.md  |   54 +
 .../notes/pre-change-measurements.md               |   63 +
 .../notes/quickstart-run.md                        |  109 +
 .../notes/red-first-evidence.md                    |  549 ++
 .../107-decision-governance/notes/us1-green.txt    |   73 +
 .../107-decision-governance/notes/us2-green.txt    |   95 +
 .../107-decision-governance/notes/us3-green.txt    |  170 +
 .../notes/us4-green-slots.txt                      |    7 +
 .../107-decision-governance/notes/us4-green.txt    |  181 +
 .../notes/us5-green-slots.txt                      |    7 +
 .../107-decision-governance/notes/us5-green.txt    |  101 +
 .../notes/us6-green-slots.txt                      |    7 +
 .../107-decision-governance/notes/us6-green.txt    |   71 +
 .specify/specs/107-decision-governance/plan.md     |  217 +
 .../specs/107-decision-governance/quickstart.md    |   81 +
 .../specs/107-decision-governance/requirements.md  |  427 ++
 .specify/specs/107-decision-governance/research.md |   73 +
 .specify/specs/107-decision-governance/tasks.md    |  420 ++
 .../test-evidence/analyze-domain-w1-r2.jsonl       |    6 +
 .../test-evidence/analyze-domain-w1-r3.jsonl       |    5 +
 .../test-evidence/analyze-domain-w1.jsonl          |    6 +
 .../test-evidence/analyze-domain-w2-r2.jsonl       |    6 +
 .../test-evidence/analyze-domain-w2-r3.jsonl       |    6 +
 .../test-evidence/analyze-domain-w2.jsonl          |    6 +
 .../test-evidence/analyze-domain-w3-r2.jsonl       |    6 +
 .../test-evidence/analyze-domain-w3-r3.jsonl       |    6 +
 .../test-evidence/analyze-domain-w3.jsonl          |    6 +
 .../analyze-final-report-r5-2026-11-26.md          |    8 +
 .../test-evidence/analyze-incremental-r4.jsonl     |    5 +
 .../test-evidence/analyze-incremental-r5.jsonl     |    1 +
 .../test-evidence/analyze-repair-2026-11-26.md     |   63 +
 .../test-evidence/analyze-repair-decomposition.txt |    5 +
 .../analyze-repair-pre-analyze-plan.txt            |    5 +
 .../analyze-repair-pre-analyze-requirements.txt    |    5 +
 .../analyze-repair-pre-analyze-tasks.txt           |    5 +
 .../analyze-repair-readings-postcommit.txt         |   10 +
 .../test-evidence/analyze-repair-readings.txt      |   39 +
 .../analyze-repair-validate-requirements.txt       |   15 +
 .../analyze-repair-validate-tasks.txt              |    5 +
 .../test-evidence/analyze-repair2-2026-11-26.md    |   60 +
 .../analyze-repair2-decomposition.txt              |    3 +
 .../analyze-repair2-pre-analyze-plan.txt           |    4 +
 .../analyze-repair2-pre-analyze-requirements.txt   |    4 +
 .../analyze-repair2-pre-analyze-tasks.txt          |    4 +
 .../analyze-repair2-readings-postcommit.txt        |   35 +
 .../test-evidence/analyze-repair2-readings.txt     |   50 +
 .../analyze-repair2-validate-requirements.txt      |   12 +
 .../analyze-repair2-validate-tasks.txt             |    3 +
 .../test-evidence/analyze-repair3-2026-11-26.md    |   55 +
 .../analyze-repair3-decomposition.txt              |    3 +
 .../analyze-repair3-pre-analyze-plan.txt           |    4 +
 .../analyze-repair3-pre-analyze-requirements.txt   |    4 +
 .../analyze-repair3-pre-analyze-tasks.txt          |    4 +
 .../analyze-repair3-readings-postcommit.txt        |   37 +
 .../test-evidence/analyze-repair3-readings.txt     |   50 +
 .../analyze-repair3-validate-requirements.txt      |   12 +
 .../analyze-repair3-validate-tasks.txt             |    3 +
 .../test-evidence/analyze-repair4-2026-11-26.md    |   59 +
 .../analyze-repair4-decomposition.txt              |    3 +
 .../analyze-repair4-pre-analyze-plan.txt           |    4 +
 .../analyze-repair4-pre-analyze-requirements.txt   |    4 +
 .../analyze-repair4-pre-analyze-tasks.txt          |    4 +
 .../analyze-repair4-readings-postcommit.txt        |   37 +
 .../test-evidence/analyze-repair4-readings.txt     |   65 +
 .../analyze-repair4-validate-requirements.txt      |   12 +
 .../analyze-repair4-validate-tasks.txt             |    3 +
 .../test-evidence/analyze.jsonl                    |    1 +
 .../checklist-requirements-validator.txt           |   10 +
 .../test-evidence/checklist-spec-readings.txt      |   33 +
 .../test-evidence/checklist-stage-2026-11-26.md    |   60 +
 .../test-evidence/checklist-targeted-set.txt       |   64 +
 .../test-evidence/checklist-verification.txt       |   13 +
 .../test-evidence/checklist.jsonl                  |    1 +
 .../test-evidence/clarify-overlap.txt              |    5 +
 .../clarify-pre-analyze-requirements.txt           |    5 +
 .../test-evidence/clarify-stage-2026-11-25.md      |  128 +
 .../test-evidence/clarify-validator.txt            |   15 +
 .../test-evidence/clarify-workspace.json           |    4 +
 .../test-evidence/clarify.jsonl                    |    1 +
 .../closure-failed-names-preservation-sweep.txt    |    5 +
 .../test-evidence/decomposition-requirements.json  |    4 +
 .../test-evidence/gate-neutrality.txt              |   49 +
 .../test-evidence/glossary-discipline.txt          |   30 +
 .../glossary-proposal-plan-2026-11-25.md           |    7 +
 .../test-evidence/glossary-proposal.md             |   17 +
 .../test-evidence/goal-team-activation.txt         |   11 +
 .../implement-baseline-environment-deltas.md       |   11 +
 .../test-evidence/implement-baseline.txt           |   55 +
 .../test-evidence/implement-integration.md         |  128 +
 .../test-evidence/migration-closure.md             |  182 +
 .../test-evidence/mirror-foundational.txt          |   36 +
 .../test-evidence/mutation-drill.md                |   54 +
 .../test-evidence/overlap-post-plan.txt            |    2 +
 .../test-evidence/plan-integrity.txt               |    8 +
 .../test-evidence/plan-rereview-2026-11-26.md      |  129 +
 .../test-evidence/plan-rereview-integrity.txt      |   51 +
 .../plan-rereview-pre-analyze-plan.txt             |    5 +
 .../test-evidence/plan-rereview-targeted-set.txt   |   69 +
 .../plan-rereview-validate-decision-tensions.txt   |   14 +
 .../test-evidence/plan-rereview.jsonl              |    1 +
 .../test-evidence/plan-stage-2026-11-25.md         |   94 +
 .../test-evidence/plan-targeted-set.txt            |   31 +
 .../test-evidence/plan.jsonl                       |    1 +
 .../test-evidence/post-generation-quality-gate.txt |   10 +
 .../test-evidence/pre-analyze-plan.txt             |    2 +
 .../test-evidence/pre-analyze-requirements.json    |    5 +
 .../test-evidence/preservation-sweep.txt           |   64 +
 .../test-evidence/regen-copies-baseline.txt        |    1 +
 .../test-evidence/requirements-stage-2026-11-25.md |  115 +
 .../test-evidence/requirements-validator.txt       |   15 +
 .../scan-confirmation-gates-baseline.txt           |    6 +
 .../test-evidence/sync-mirrors-baseline.txt        |   16 +
 .../test-evidence/tasks-pre-analyze.txt            |    2 +
 .../test-evidence/tasks-stage-2026-11-25.md        |   60 +
 .../test-evidence/tasks-targeted-set.txt           |   19 +
 .../test-evidence/tasks-validator.txt              |    3 +
 .../test-evidence/tasks.jsonl                      |    1 +
 .../test-evidence/us1-green-slots.txt              |   15 +
 .../test-evidence/us1-mirror-check.txt             |   50 +
 .../test-evidence/us1-red-first.txt                |  116 +
 .../test-evidence/us2-green-slots.txt              |    7 +
 .../test-evidence/us2-red-first.txt                |   78 +
 .../test-evidence/us3-green-slots.txt              |    7 +
 .../test-evidence/us3-red-first.txt                |  246 +
 .../test-evidence/us4-mirror-check.txt             |   13 +
 .../test-evidence/us4-red-first.txt                |  279 +
 .../test-evidence/us5-mirror-check.txt             |   13 +
 .../test-evidence/us5-red-first.txt                |  190 +
 .../test-evidence/us6-migrate-dryrun.json          |  111 +
 .../test-evidence/us6-mirror-check.txt             |   67 +
 .../test-evidence/us6-red-first.txt                |   29 +
 .../test-evidence/validate-decision-tensions.txt   |   11 +
 .../test-evidence/verification-input.md            |   54 +
 .../test-evidence/workspace-analyze-repair.json    |  306 +
 .../test-evidence/workspace-analyze-repair2.json   |  306 +
 .../test-evidence/workspace-analyze-repair3.json   |  312 +
 .../test-evidence/workspace-analyze-repair4.json   |  316 +
 .../test-evidence/workspace-checklist.json         |  306 +
 .../test-evidence/workspace-plan-after.json        |    1 +
 .../test-evidence/workspace-plan-before.json       |  305 +
 .../workspace-plan-rereview-after.json             |  312 +
 .../workspace-plan-rereview-before.json            |  312 +
 .../test-evidence/workspace-requirements.json      |  305 +
 .../test-evidence/workspace-tasks.json             |  305 +
 .../teams/106-background-silent-failure/team.md    |  183 +
 .specify/teams/107-decision-governance/team.md     |  170 +
 .specify/templates/instructions-template.md        |   10 +
 agents/sdd-implement-coordinator.agent.md          |    1 +
 agents/sdd-plan-coordinator.agent.md               |    1 +
 agents/sdd-review-coordinator.agent.md             |    1 +
 agents/sdd-task-coordinator.agent.md               |    1 +
 docs/concepts/spec-driven.md                       |    2 +
 docs/reference/commands/agents.md                  |    9 +
 docs/reference/skills/sdd-loop-driver.md           |   10 +
 docs/reference/teams/orchestration.md              |   11 +
 scripts/bash/generate-instructions.sh              |   14 +-
 scripts/python/role-edge-check.py                  |  990 ++-
 scripts/python/validate-decisions.py               | 1209 ++++
 shared/definitions/agent-definitions.md            |    2 +
 shared/definitions/anchor-definitions.md           |    2 +
 shared/definitions/decision-definitions.md         |  303 +
 shared/definitions/framework-map.md                |    1 +
 shared/definitions/goal-definitions.md             |    2 +
 shared/definitions/subagent-definitions.md         |    2 +
 shared/definitions/superagent-definitions.md       |   87 +-
 shared/guidelines/confirmation-gates.md            |    2 +
 shared/guidelines/decision-tension.md              |    3 +-
 shared/guidelines/fast-fail.md                     |    2 +
 shared/workflow/external-dispatch-recipes.md       |    8 +-
 skills/external/sdd-loop-driver/SKILL.md           |    1 +
 .../references/checkpoint-protocol.md              |    1 +
 .../sdd-loop-driver/references/dispatch-recipes.md |    1 +
 .../sdd-loop-driver/references/stage-prompts.md    |    2 +
 skills/internal/analyze-artifacts/SKILL.md         |    7 +
 skills/internal/create-team/SKILL.md               |    6 +-
 skills/internal/create-team/scripts/dispatch.sh    |  103 +-
 skills/internal/review-feature-quality/SKILL.md    |    7 +
 skills/internal/review-sdd-process/SKILL.md        |    6 +
 skills/internal/run-agent/SKILL.md                 |   43 +
 skills/internal/run-team/SKILL.md                  |    2 +
 templates/commands/agents.md                       |    2 +
 templates/commands/team.md                         |    2 +
 templates/instructions-template.md                 |   10 +
 .../contract/test_decision_governance_contracts.py |  773 +++
 tests/contract/test_decision_governance_guards.py  |  878 +++
 .../test_decision_governance_migration_map.py      |  256 +
 tests/contract/test_fast_fail_discipline.py        |    8 +-
 tests/contract/test_non_regression_070.py          |    5 +-
 tests/contract/test_settlement_carriers.py         |  887 +++
 .../test_settlement_contract_definitions.py        |  481 ++
 tests/contract/test_settlement_engine.py           |  614 ++
 tests/contract/test_settlement_migration.py        |  363 +
 tests/contract/test_settlement_preservation.py     |  305 +
 tests/contract/test_settlement_scope.py            |  293 +
 tests/fixtures/decision-governance/chain/.gitkeep  |    0
 .../chain/carriers/redecision-lossy.md             |   48 +
 .../chain/carriers/redecision.md                   |   49 +
 .../decision-governance/chain/carriers/register.md |    6 +
 .../chain/carriers/round-trip.md                   |   26 +
 .../decision-governance/chain/green-complete.md    |   22 +
 .../decision-governance/chain/multi-hop-green.md   |   36 +
 .../decision-governance/chain/red-multi-hop-id.md  |   36 +
 .../chain/red-silent-redecision.md                 |   22 +
 tests/fixtures/decision-governance/legacy/.gitkeep |    0
 .../legacy/incomplete-new-form.md                  |    5 +
 .../fixtures/decision-governance/legacy/legacy.md  |   13 +
 .../decision-governance/legacy/register.md         |    7 +
 tests/fixtures/decision-governance/m01/.gitkeep    |    0
 .../decision-governance/m01/green-complete.md      |   23 +
 .../decision-governance/m01/green-tension-ref.md   |   23 +
 .../decision-governance/m01/red-class-outside.md   |   23 +
 .../m01/red-conditional-missing.md                 |   23 +
 .../m01/red-malformed-timepoint.md                 |   23 +
 .../decision-governance/m01/red-missing-actor.md   |   22 +
 .../decision-governance/m01/red-placeholder.md     |   24 +
 .../decision-governance/m01/red-tension-copy.md    |   25 +
 .../decision-governance/m01/red-timepoint-phase.md |   25 +
 tests/fixtures/decision-governance/m02/.gitkeep    |    0
 .../decision-governance/m02/green-complete.md      |   25 +
 .../decision-governance/m02/red-empty-locator.md   |   25 +
 .../m02/red-single-dimension.md                    |   25 +
 tests/fixtures/decision-governance/m03/.gitkeep    |    0
 .../decision-governance/m03/ai-replay-green.md     |   25 +
 .../decision-governance/m03/ai-replay-mismatch.md  |   25 +
 .../decision-governance/m03/green-complete.md      |   23 +
 .../decision-governance/m03/green-single-forced.md |   19 +
 .../m03/red-chosen-not-member.md                   |   23 +
 .../decision-governance/m03/red-count-mismatch.md  |   23 +
 .../decision-governance/m03/red-duplicate-label.md |   23 +
 .../decision-governance/m03/red-empty-set.md       |   13 +
 .../m03/red-missing-evidence.md                    |   22 +
 .../m03/red-missing-reversibility.md               |   22 +
 .../m03/red-other-without-path.md                  |   23 +
 .../m03/red-single-without-forced.md               |   18 +
 tests/fixtures/decision-governance/m04/.gitkeep    |    0
 .../decision-governance/m04/green-dense.md         |   45 +
 tests/fixtures/decision-governance/m04/red-form.md |   23 +
 .../decision-governance/m04/red-non-dense.md       |   45 +
 .../decision-governance/m04/red-unregistered.md    |   23 +
 .../decision-governance/m04/register-missing.md    |    5 +
 tests/fixtures/decision-governance/m04/register.md |    7 +
 tests/fixtures/decision-governance/m05/.gitkeep    |    0
 .../fixtures/decision-governance/m05/red-no-id.md  |   21 +
 .../decision-governance/m05/red-no-receipt.md      |   15 +
 .../decision-governance/m05/red-unresolvable.md    |   17 +
 tests/fixtures/decision-governance/m06/.gitkeep    |    0
 .../decision-governance/m06/red-missing-archive.md |   15 +
 .../decision-governance/m06/red-missing-chosen.md  |   15 +
 .../decision-governance/m06/red-missing-class.md   |   15 +
 .../m06/red-missing-constraints.md                 |   15 +
 .../decision-governance/m06/red-missing-id.md      |   15 +
 .../decision-governance/m06/red-no-block.md        |   10 +
 tests/fixtures/decision-governance/m07/.gitkeep    |    0
 .../decision-governance/m07/red-inconsistent-id.md |   22 +
 .../m07/red-missing-dispatch.md                    |   15 +
 .../decision-governance/m07/red-missing-receipt.md |   15 +
 .../decision-governance/m07/red-missing-record.md  |   17 +
 tests/fixtures/decision-governance/m08/.gitkeep    |    0
 tests/fixtures/decision-governance/m08/glossary.md |    5 +
 .../decision-governance/m08/green-full-name.md     |   23 +
 .../decision-governance/m08/green-unregistered.md  |   23 +
 .../decision-governance/m08/red-variant.md         |   23 +
 tests/fixtures/decision-governance/m09/.gitkeep    |    0
 .../decision-governance/m09/green-resolvable.md    |   23 +
 .../decision-governance/m09/red-broken-anchor.md   |   23 +
 .../fixtures/decision-governance/m09/red-broken.md |   23 +
 .../fixtures/decision-governance/payload/.gitkeep  |    0
 .../decision-governance/payload/complete.md        |   16 +
 .../decision-governance/payload/non-decision.md    |   10 +
 .../payload/returns/return-acknowledged.md         |   10 +
 .../payload/returns/return-escalated.md            |    6 +
 .../decision-governance/reconstruct/.gitkeep       |    0
 .../reconstruct/checkpoints/02-implement.md        |   23 +
 .../decision-governance/reconstruct/plan.md        |   23 +
 .../decision-governance/reconstruct/register.md    |    5 +
 .../reconstruct/requirements.md                    |   25 +
 .../decision-governance/reconstruct/run-report.md  |   23 +
 tests/fixtures/settlement/builders.py              |  497 ++
 tests/fixtures/settlement/c1-state/demo-line.md    |    9 +
 .../c1-state/heartbeat-demo-line-implement.log     |    1 +
 .../c1-state/log-demo-line-implement.log           |    3 +
 .../settlement/c1-state/pid-demo-line-implement    |    1 +
 .../prompt-demo-line-implement.md.meta.json        |   14 +
 .../settlement/c1-state/status-demo-line-implement |    1 +
 .../settlement/c3-report/logs/seat-legacy.attempt  |    8 +
 .../c3-report/logs/seat-missing-start.return.txt   |    1 +
 .../settlement/c3-report/logs/seat-ok.attempt      |    8 +
 .../settlement/c3-report/logs/seat-ok.return.txt   |    1 +
 .../demo-team/runs/20261120T000000Z-report.md      |   12 +
 .../legacy-team/runs/20261119T000000Z-report.md    |   11 +
 .../settlement/legacy/logs/legacy-run.attempt      |    9 +
 .../fixtures/settlement/legacy/logs/legacy-run.end |    6 +
 .../settlement/legacy/logs/legacy-run.live.log     |    2 +
 .../settlement/legacy/logs/legacy-run.return.txt   |    1 +
 .../settlement/legacy/logs/legacy-run.settlement   |   10 +
 .../settlement/legacy/logs/legacy-run.status       |    1 +
 .../versioned/logs/versioned-run.attempt           |    9 +
 .../settlement/versioned/logs/versioned-run.end    |    6 +
 .../versioned/logs/versioned-run.live.log          |    2 +
 .../versioned/logs/versioned-run.return.txt        |    1 +
 .../versioned/logs/versioned-run.settlement        |   11 +
 .../settlement/versioned/logs/versioned-run.status |    1 +
 .../test_decision_governance_migrate_dryrun.py     |  360 +
 tests/unit/test_validate_decisions.py              |  354 +
 684 files changed, 58052 insertions(+), 418 deletions(-)
```

---

## Review 意见


### 🟠 [IMPORTANT] scripts/python/validate-decisions.py (Line 1064)

> INVENTORY OBSERVED-SET AUGMENTATION: lines 1064-1071 add every declared non-exempt producer whose owner path exists on disk to the observed set. The docstring says the observation set is the caller-supplied code-face scan; the documented scan maps only P-04/P-05/P-06/P-09, so 'observed == declared ± exempt' is reached largely by declaration-side existence, and a declared face that stops referencing the owner page while its file remains is still counted observed. Fix: make observed strictly the mapped scan hits (a non-observed declared row becomes missing), or state the augmented definition in the action docstring and the SC-001 source sentence.

<sub>14:24:39</sub>


### 🟢 [SUGGESTION] scripts/bash/generate-instructions.sh (Line 112)

> The raise record says the new '## Decision Items（决策项）' ambient section is '1,274 B'; the extracted section measures 1,276 B in both the template and the live file (review measurement 2026-11-26). Stale by 2 B; no threshold is affected (1,500 B cap; 40,170 B total < 40,960 B). Fix: correct the recorded figure.

<sub>14:24:39</sub>


### ❓ [QUESTION] shared/definitions/decision-definitions.md (Line 271)

> M-01's red condition reads '条件层字段在触发成立时缺失', but only the transmission family has a machine-detectable trigger (transmission_status); the supersession family's trigger ('记录被取代时') is not detectable from the record set, and tests/fixtures/decision-governance/m01/red-conditional-missing.md drills only the transmission family. Is the supersession leg intended to be machine-judged? If not, scope the M-01 row (or add a detection rule) so the table's claim matches the guard.

<sub>14:24:39</sub>


### 👍 [PRAISE] scripts/python/validate-decisions.py

> Clean read-only engine: closed tables as module constants, per-rule red conditions with rule-carrying verdict lines, legacy reported rather than judged, and the script-interface surface (--help/--version/undeclared-option refusal) behaves as declared; the 43-test battery with reverse samples shows the guard roster is alive.

<sub>14:24:39</sub>


## 回应与评审依据 (responses and review basis)

- **[important → agree, follow-up]** The augmentation is real: the documented scan observes four declared producers (P-04/P-05/P-06/P-09) plus three declared non-producer faces and the checker, while the action's `observed` set is completed by declaration-side path existence (lines 1064-1071). The two defensive properties the criterion needs still hold and are mutation-drilled — an unregistered face turns the guard red and a vanished owner face turns it red — so this does not block the slice; it is carried into `review.md` as implementation finding I1 (P1) and artifact finding A3 (P1) with the measured scan output as evidence. The fix choice (strict observation vs a documented augmented definition, plus the SC-001 Source sentence) is a follow-up ruling, not a review-stage repair.
- **[suggestion → agree, follow-up]** Accepted as a follow-up one-line correction; no threshold is affected.
- **[question → answered for this run]** The M-01 row is read as carrying the transmission family's machine leg (the only trigger a deterministic judge can detect); the supersession family's trigger is recorded in the record itself, so no machine leg exists for it. The wording/scope question is carried into `review.md` as artifact finding A5 (P2); no machine-coverage claim is made for a supersession detection this run.
- **Review basis (what "reviewed" means in the receipt):** the 27 judged files are the feature's code and test surfaces — the new engine read in full, the owner page read in full, every pointer/template/generator diff read, the five test modules and the section-count repair read — plus the pointer-shaped edits to adjacent owners. The 657 skipped files are: declared non-producer generated copies and `.specify/` mirrors (`generated`), non-code records and spec artifacts (`non-code-file`), and the line-106 merge scope plus its fixture/log data (`size-guard-focus-not-reviewed`). The 106 merge content is not this slice's work: its lines were reviewed by line 106's own code segment at `0a01f797a` (record `.specify/specs/106-background-silent-failure/code-review.md`), and this run verified the merge preserved those contents (`git diff 0a01f797a..HEAD` empty for 321 of the 322 line-106-only files; the one remaining file is 106's own review-record entry, read here). Skips earn no coverage credit, so the segment verdict is `not-evaluated` by rule, not a pass claim.
- **Client capture:** not run — this repository is the framework source (framework hat, `shared/definitions/dogfooding-definitions.md` § 2.1); no client feedback entry is written and the five-value disclosure set does not apply.
- **Merge gate:** `report --summary --file` → 0 blocking, gate `allow` (one important answered here, one suggestion and one question disclosed for follow-up).


> **未提交范围（未评审）**: 2 个未提交路径未计入本次评审对象（.specify/specs/107-decision-governance/test-evidence/review-evidence.txt, .specify/specs/107-decision-governance/verification.md）；本回执不对该范围给出任何结论。

<!-- coverage-receipt:begin -->
receipt_version=1
base=fbab7a45c4a57b596bc32437181ee9eb799ebe60
head=3f0200b421bf284c176592afa34549e7a2c07706
base_source=feature-first-commit
renderer=text
changed_files=684
judged_files=27
skipped_files=657
gap_files=0
lines_added=4330
lines_deleted=7
file.001.path=.claude/commands/speckit.agents.md
file.001.verdict=skipped
file.001.reason=generated
file.002.path=.claude/commands/speckit.team.md
file.002.verdict=skipped
file.002.reason=generated
file.003.path=.github/prompts/speckit.agents.prompt.md
file.003.verdict=skipped
file.003.reason=generated
file.004.path=.github/prompts/speckit.team.prompt.md
file.004.verdict=skipped
file.004.reason=generated
file.005.path=.opencode/command/speckit.agents.md
file.005.verdict=skipped
file.005.reason=generated
file.006.path=.opencode/command/speckit.team.md
file.006.verdict=skipped
file.006.reason=generated
file.007.path=.qoder/agents/sdd-debt-governor.agent.md
file.007.verdict=skipped
file.007.reason=generated
file.008.path=.qoder/agents/sdd-implement-coordinator.agent.md
file.008.verdict=skipped
file.008.reason=generated
file.009.path=.qoder/agents/sdd-plan-coordinator.agent.md
file.009.verdict=skipped
file.009.reason=generated
file.010.path=.qoder/agents/sdd-review-coordinator.agent.md
file.010.verdict=skipped
file.010.reason=generated
file.011.path=.qoder/agents/sdd-task-coordinator.agent.md
file.011.verdict=skipped
file.011.reason=generated
file.012.path=.qoder/commands/speckit.agents.md
file.012.verdict=skipped
file.012.reason=generated
file.013.path=.qoder/commands/speckit.team.md
file.013.verdict=skipped
file.013.reason=generated
file.014.path=.specify/agents/.render-manifest.json
file.014.verdict=skipped
file.014.reason=generated
file.015.path=.specify/agents/templates/sdd-implement-coordinator.agent.md
file.015.verdict=skipped
file.015.reason=generated
file.016.path=.specify/agents/templates/sdd-plan-coordinator.agent.md
file.016.verdict=skipped
file.016.reason=generated
file.017.path=.specify/agents/templates/sdd-review-coordinator.agent.md
file.017.verdict=skipped
file.017.reason=generated
file.018.path=.specify/agents/templates/sdd-task-coordinator.agent.md
file.018.verdict=skipped
file.018.reason=generated
file.019.path=.specify/anchoring/106-background-silent-failure/anchor.md
file.019.verdict=skipped
file.019.reason=non-code-file
file.020.path=.specify/anchoring/107-decision-governance/anchor.md
file.020.verdict=skipped
file.020.reason=non-code-file
file.021.path=.specify/exec-quant/records/20261125T114538658383Z-0904f023.json
file.021.verdict=skipped
file.021.reason=non-code-file
file.022.path=.specify/exec-quant/records/20261125T115451874927Z-6db027b5.json
file.022.verdict=skipped
file.022.reason=non-code-file
file.023.path=.specify/exec-quant/records/20261125T121419791413Z-a4679bfb.json
file.023.verdict=skipped
file.023.reason=non-code-file
file.024.path=.specify/exec-quant/records/20261125T122810951835Z-56d6e538.json
file.024.verdict=skipped
file.024.reason=non-code-file
file.025.path=.specify/exec-quant/records/20261125T123555820029Z-80b8b9aa.json
file.025.verdict=skipped
file.025.reason=non-code-file
file.026.path=.specify/exec-quant/records/20261125T125153331787Z-46e5ff70.json
file.026.verdict=skipped
file.026.reason=non-code-file
file.027.path=.specify/exec-quant/records/20261125T125926616815Z-eb0837fb.json
file.027.verdict=skipped
file.027.reason=non-code-file
file.028.path=.specify/exec-quant/records/20261125T132404451045Z-ffd93788.json
file.028.verdict=skipped
file.028.reason=non-code-file
file.029.path=.specify/exec-quant/records/20261125T134020382137Z-dc4a1b7c.json
file.029.verdict=skipped
file.029.reason=non-code-file
file.030.path=.specify/exec-quant/records/20261125T135920685209Z-dd809ed0.json
file.030.verdict=skipped
file.030.reason=non-code-file
file.031.path=.specify/exec-quant/records/20261125T140707830920Z-97a6c8e4.json
file.031.verdict=skipped
file.031.reason=non-code-file
file.032.path=.specify/exec-quant/records/20261125T142034358066Z-f6b47bfc.json
file.032.verdict=skipped
file.032.reason=non-code-file
file.033.path=.specify/exec-quant/records/20261125T143217905096Z-b9e267ca.json
file.033.verdict=skipped
file.033.reason=non-code-file
file.034.path=.specify/exec-quant/records/20261125T160801888488Z-1fb91fea.json
file.034.verdict=skipped
file.034.reason=non-code-file
file.035.path=.specify/exec-quant/records/20261125T162322617249Z-b3955a58.json
file.035.verdict=skipped
file.035.reason=non-code-file
file.036.path=.specify/exec-quant/records/20261125T163755432720Z-371d39ee.json
file.036.verdict=skipped
file.036.reason=non-code-file
file.037.path=.specify/exec-quant/records/20261125T173627505479Z-5caa3c2f.json
file.037.verdict=skipped
file.037.reason=non-code-file
file.038.path=.specify/exec-quant/records/20261125T173956791454Z-2e94960a.json
file.038.verdict=skipped
file.038.reason=non-code-file
file.039.path=.specify/exec-quant/records/20261125T180105894081Z-3ac41486.json
file.039.verdict=skipped
file.039.reason=non-code-file
file.040.path=.specify/exec-quant/records/20261126T020852910406Z-e88542f4.json
file.040.verdict=skipped
file.040.reason=non-code-file
file.041.path=.specify/exec-quant/records/20261126T032247826756Z-33524863.json
file.041.verdict=skipped
file.041.reason=non-code-file
file.042.path=.specify/exec-quant/records/20261126T033532112186Z-c50e14d7.json
file.042.verdict=skipped
file.042.reason=non-code-file
file.043.path=.specify/exec-quant/records/20261126T061350897087Z-27ed0640.json
file.043.verdict=skipped
file.043.reason=non-code-file
file.044.path=.specify/features.md
file.044.verdict=skipped
file.044.reason=non-code-file
file.045.path=.specify/features/076-decision-tension-contract.md
file.045.verdict=skipped
file.045.reason=non-code-file
file.046.path=.specify/features/095-superagent-role.md
file.046.verdict=skipped
file.046.reason=non-code-file
file.047.path=.specify/features/107-decision-governance.md
file.047.verdict=skipped
file.047.reason=non-code-file
file.048.path=.specify/feedback/20261125T114609Z-speckit-requirements.md
file.048.verdict=skipped
file.048.reason=non-code-file
file.049.path=.specify/feedback/20261125T115512Z-speckit-clarify.md
file.049.verdict=skipped
file.049.reason=non-code-file
file.050.path=.specify/feedback/20261125T121425Z-speckit-plan.md
file.050.verdict=skipped
file.050.reason=non-code-file
file.051.path=.specify/feedback/20261125T122816Z-speckit-tasks.md
file.051.verdict=skipped
file.051.reason=non-code-file
file.052.path=.specify/feedback/20261125T123559Z-speckit-checklist.md
file.052.verdict=skipped
file.052.reason=non-code-file
file.053.path=.specify/feedback/20261125T125200Z-skill-analyze-artifacts.md
file.053.verdict=skipped
file.053.reason=non-code-file
file.054.path=.specify/feedback/20261125T125926Z-skill-analyze-artifacts.md
file.054.verdict=skipped
file.054.reason=non-code-file
file.055.path=.specify/feedback/20261125T132404Z-skill-analyze-artifacts.md
file.055.verdict=skipped
file.055.reason=non-code-file
file.056.path=.specify/feedback/20261125T134023Z-skill-analyze-artifacts.md
file.056.verdict=skipped
file.056.reason=non-code-file
file.057.path=.specify/feedback/20261125T135929Z-speckit-requirements.md
file.057.verdict=skipped
file.057.reason=non-code-file
file.058.path=.specify/feedback/20261125T140714Z-skill-clarify-artifact.md
file.058.verdict=skipped
file.058.reason=non-code-file
file.059.path=.specify/feedback/20261125T142034Z-skill-create-plan.md
file.059.verdict=skipped
file.059.reason=non-code-file
file.060.path=.specify/feedback/20261125T143223Z-skill-create-tasks.md
file.060.verdict=skipped
file.060.reason=non-code-file
file.061.path=.specify/feedback/20261125T160807Z-skill-create-checklist.md
file.061.verdict=skipped
file.061.reason=non-code-file
file.062.path=.specify/feedback/20261125T162329Z-skill-analyze-artifacts.md
file.062.verdict=skipped
file.062.reason=non-code-file
file.063.path=.specify/feedback/20261125T163801Z-skill-analyze-artifacts.md
file.063.verdict=skipped
file.063.reason=non-code-file
file.064.path=.specify/feedback/20261125T173633Z-skill-create-plan.md
file.064.verdict=skipped
file.064.reason=non-code-file
file.065.path=.specify/feedback/20261125T174002Z-skill-analyze-artifacts.md
file.065.verdict=skipped
file.065.reason=non-code-file
file.066.path=.specify/feedback/20261125T180117Z-skill-analyze-artifacts.md
file.066.verdict=skipped
file.066.reason=non-code-file
file.067.path=.specify/feedback/20261126T020919Z-skill-analyze-artifacts.md
file.067.verdict=skipped
file.067.reason=non-code-file
file.068.path=.specify/feedback/20261126T032257Z-skill-implement-feature.md
file.068.verdict=skipped
file.068.reason=non-code-file
file.069.path=.specify/feedback/20261126T033532Z-skill-review-sdd-process.md
file.069.verdict=skipped
file.069.reason=non-code-file
file.070.path=.specify/feedback/20261126T061400Z-skill-implement-feature.md
file.070.verdict=skipped
file.070.reason=non-code-file
file.071.path=.specify/glossary.md
file.071.verdict=skipped
file.071.reason=non-code-file
file.072.path=.specify/instructions.md
file.072.verdict=skipped
file.072.reason=generated
file.073.path=.specify/register.md
file.073.verdict=skipped
file.073.reason=non-code-file
file.074.path=.specify/retention/closeout/20261125T114628Z-106-background-silent-failure-requirements.md
file.074.verdict=skipped
file.074.reason=non-code-file
file.075.path=.specify/retention/closeout/20261125T115521Z-106-background-silent-failure-clarify.md
file.075.verdict=skipped
file.075.reason=non-code-file
file.076.path=.specify/retention/closeout/20261125T115846Z-106-background-silent-failure-clarify-repair.md
file.076.verdict=skipped
file.076.reason=non-code-file
file.077.path=.specify/retention/closeout/20261125T121502Z-106-background-silent-failure-plan.md
file.077.verdict=skipped
file.077.reason=non-code-file
file.078.path=.specify/retention/closeout/20261125T122912Z-106-background-silent-failure-tasks.md
file.078.verdict=skipped
file.078.reason=non-code-file
file.079.path=.specify/retention/closeout/20261125T123605Z-106-background-silent-failure-checklist.md
file.079.verdict=skipped
file.079.reason=non-code-file
file.080.path=.specify/retention/closeout/20261125T125221Z-106-background-silent-failure-analyze.md
file.080.verdict=skipped
file.080.reason=non-code-file
file.081.path=.specify/retention/closeout/20261125T130200Z-106-background-silent-failure-analyze-repair.md
file.081.verdict=skipped
file.081.reason=non-code-file
file.082.path=.specify/retention/closeout/20261125T132427Z-106-background-silent-failure-analyze-repair2.md
file.082.verdict=skipped
file.082.reason=non-code-file
file.083.path=.specify/retention/closeout/20261125T140024Z-r20261125T134500Z-107a-requirements.md
file.083.verdict=skipped
file.083.reason=non-code-file
file.084.path=.specify/retention/closeout/20261125T140844Z-r20261125T134500Z-107a-clarify.md
file.084.verdict=skipped
file.084.reason=non-code-file
file.085.path=.specify/retention/closeout/20261125T142103Z-r20261125T134500Z-107a-plan.md
file.085.verdict=skipped
file.085.reason=non-code-file
file.086.path=.specify/retention/closeout/20261125T143241Z-r20261125T134500Z-107a-tasks.md
file.086.verdict=skipped
file.086.reason=non-code-file
file.087.path=.specify/retention/closeout/20261125T160827Z-r20261125T134500Z-107a-checklist.md
file.087.verdict=skipped
file.087.reason=non-code-file
file.088.path=.specify/retention/closeout/20261125T173700Z-r20261125T173500Z-107c-plan-rereview.md
file.088.verdict=skipped
file.088.reason=non-code-file
file.089.path=.specify/retention/closeout/20261126T032315Z-106-background-silent-failure-implement.md
file.089.verdict=skipped
file.089.reason=non-code-file
file.090.path=.specify/retention/closeout/20261126T033549Z-106-background-silent-failure-review.md
file.090.verdict=skipped
file.090.reason=non-code-file
file.091.path=.specify/retention/closeout/20261126T061407Z-107-decision-governance-implement.md
file.091.verdict=skipped
file.091.reason=non-code-file
file.092.path=.specify/scripts/bash/generate-instructions.sh
file.092.verdict=skipped
file.092.reason=generated
file.093.path=.specify/scripts/python/role-edge-check.py
file.093.verdict=skipped
file.093.reason=generated
file.094.path=.specify/scripts/python/validate-decisions.py
file.094.verdict=skipped
file.094.reason=generated
file.095.path=.specify/session/20261109T081108Z-run-determination-skill-create-plan-093-plan-a1.md
file.095.verdict=skipped
file.095.reason=non-code-file
file.096.path=.specify/session/20261110T085343Z-run-determination-skill-create-plan-r20261110t081104z-b096.md
file.096.verdict=skipped
file.096.reason=non-code-file
file.097.path=.specify/session/20261110T091102Z-run-determination-skill-create-tasks-r20261110t081104z-b096.md
file.097.verdict=skipped
file.097.reason=non-code-file
file.098.path=.specify/session/20261124T055708Z-run-determination-speckit-clarify-r20261124t054500z-9b2d.md
file.098.verdict=skipped
file.098.reason=non-code-file
file.099.path=.specify/session/20261125T024118Z-run-determination-speckit-requirements-r20261125t022857z-06d.md
file.099.verdict=skipped
file.099.reason=non-code-file
file.100.path=.specify/session/20261125T024939Z-run-determination-skill-clarify-artifact-r20261125t022857z-0.md
file.100.verdict=skipped
file.100.reason=non-code-file
file.101.path=.specify/session/20261125T035109Z-run-determination-skill-create-checklist-r20261125t022857z-0.md
file.101.verdict=skipped
file.101.reason=non-code-file
file.102.path=.specify/session/20261125T055144Z-run-determination-skill-implement-feature-r20261125t022857z.md
file.102.verdict=skipped
file.102.reason=non-code-file
file.103.path=.specify/session/20261125T074156Z-run-determination-skill-review-sdd-process-r20261125t022857z.md
file.103.verdict=skipped
file.103.reason=non-code-file
file.104.path=.specify/session/20261125T114533Z-run-determination-speckit-requirements-r20261125t113505z-106.md
file.104.verdict=skipped
file.104.reason=non-code-file
file.105.path=.specify/session/20261125T115445Z-run-determination-speckit-clarify-r20261125t113505z-106a.md
file.105.verdict=skipped
file.105.reason=non-code-file
file.106.path=.specify/session/20261125T121417Z-run-determination-speckit-plan-r20261125t113505z-106a.md
file.106.verdict=skipped
file.106.reason=non-code-file
file.107.path=.specify/session/20261125T122808Z-run-determination-speckit-tasks-r20261125t113505z-106a.md
file.107.verdict=skipped
file.107.reason=non-code-file
file.108.path=.specify/session/20261125T123550Z-run-determination-speckit-checklist-r20261125t113505z-106a.md
file.108.verdict=skipped
file.108.reason=non-code-file
file.109.path=.specify/session/20261125T125150Z-run-determination-skill-analyze-artifacts-r20261125t113505z.md
file.109.verdict=skipped
file.109.reason=non-code-file
file.110.path=.specify/session/20261125T125920Z-run-determination-skill-analyze-artifacts-r20261125t125827z.md
file.110.verdict=skipped
file.110.reason=non-code-file
file.111.path=.specify/session/20261125T132358Z-run-determination-skill-analyze-artifacts-r20261125t132316z.md
file.111.verdict=skipped
file.111.reason=non-code-file
file.112.path=.specify/session/20261125T134017Z-run-determination-skill-analyze-artifacts-r20261125t134017z.md
file.112.verdict=skipped
file.112.reason=non-code-file
file.113.path=.specify/session/20261125T135914Z-run-determination-speckit-requirements-r20261125t134500z-107.md
file.113.verdict=skipped
file.113.reason=non-code-file
file.114.path=.specify/session/20261125T140702Z-run-determination-skill-clarify-artifact-r20261125t134500z-1.md
file.114.verdict=skipped
file.114.reason=non-code-file
file.115.path=.specify/session/20261125T142028Z-run-determination-skill-create-plan-r20261125t134500z-107a.md
file.115.verdict=skipped
file.115.reason=non-code-file
file.116.path=.specify/session/20261125T143214Z-run-determination-skill-create-tasks-r20261125t134500z-107a.md
file.116.verdict=skipped
file.116.reason=non-code-file
file.117.path=.specify/session/20261125T160757Z-run-determination-skill-create-checklist-r20261125t134500z-1.md
file.117.verdict=skipped
file.117.reason=non-code-file
file.118.path=.specify/session/20261125T162319Z-run-determination-skill-analyze-artifacts-r20261125t134500z.md
file.118.verdict=skipped
file.118.reason=non-code-file
file.119.path=.specify/session/20261125T163748Z-run-determination-skill-analyze-artifacts-r20261125t162400z.md
file.119.verdict=skipped
file.119.reason=non-code-file
file.120.path=.specify/session/20261125T173624Z-run-determination-skill-create-plan-r20261125t173500z-107c.md
file.120.verdict=skipped
file.120.reason=non-code-file
file.121.path=.specify/session/20261125T173937Z-run-determination-skill-analyze-artifacts-r20261125t173750z.md
file.121.verdict=skipped
file.121.reason=non-code-file
file.122.path=.specify/session/20261125T180034Z-run-determination-skill-analyze-artifacts-r20261125t180013z.md
file.122.verdict=skipped
file.122.reason=non-code-file
file.123.path=.specify/session/20261126T020850Z-run-determination-skill-analyze-artifacts-r20261126t020820z.md
file.123.verdict=skipped
file.123.reason=non-code-file
file.124.path=.specify/session/20261126T032240Z-run-determination-skill-implement-feature-r20261125t113505z.md
file.124.verdict=skipped
file.124.reason=non-code-file
file.125.path=.specify/session/20261126T033527Z-run-determination-skill-review-sdd-process-r20261126t033520z.md
file.125.verdict=skipped
file.125.reason=non-code-file
file.126.path=.specify/session/20261126T061344Z-run-determination-skill-implement-feature-r20261125t134500z.md
file.126.verdict=skipped
file.126.reason=non-code-file
file.127.path=.specify/shared/definitions/agent-definitions.md
file.127.verdict=skipped
file.127.reason=generated
file.128.path=.specify/shared/definitions/anchor-definitions.md
file.128.verdict=skipped
file.128.reason=generated
file.129.path=.specify/shared/definitions/decision-definitions.md
file.129.verdict=skipped
file.129.reason=generated
file.130.path=.specify/shared/definitions/framework-map.md
file.130.verdict=skipped
file.130.reason=generated
file.131.path=.specify/shared/definitions/goal-definitions.md
file.131.verdict=skipped
file.131.reason=generated
file.132.path=.specify/shared/definitions/subagent-definitions.md
file.132.verdict=skipped
file.132.reason=generated
file.133.path=.specify/shared/definitions/superagent-definitions.md
file.133.verdict=skipped
file.133.reason=generated
file.134.path=.specify/shared/guidelines/confirmation-gates.md
file.134.verdict=skipped
file.134.reason=generated
file.135.path=.specify/shared/guidelines/decision-tension.md
file.135.verdict=skipped
file.135.reason=generated
file.136.path=.specify/shared/guidelines/fast-fail.md
file.136.verdict=skipped
file.136.reason=generated
file.137.path=.specify/shared/workflow/external-dispatch-recipes.md
file.137.verdict=skipped
file.137.reason=generated
file.138.path=.specify/skills/internal/analyze-artifacts/SKILL.md
file.138.verdict=skipped
file.138.reason=generated
file.139.path=.specify/skills/internal/create-team/SKILL.md
file.139.verdict=skipped
file.139.reason=generated
file.140.path=.specify/skills/internal/create-team/scripts/dispatch.sh
file.140.verdict=skipped
file.140.reason=generated
file.141.path=.specify/skills/internal/review-feature-quality/SKILL.md
file.141.verdict=skipped
file.141.reason=generated
file.142.path=.specify/skills/internal/review-sdd-process/SKILL.md
file.142.verdict=skipped
file.142.reason=generated
file.143.path=.specify/skills/internal/run-agent/SKILL.md
file.143.verdict=skipped
file.143.reason=generated
file.144.path=.specify/skills/internal/run-team/SKILL.md
file.144.verdict=skipped
file.144.reason=generated
file.145.path=.specify/skills/sdd-loop-driver/SKILL.md
file.145.verdict=skipped
file.145.reason=generated
file.146.path=.specify/skills/sdd-loop-driver/references/checkpoint-protocol.md
file.146.verdict=skipped
file.146.reason=generated
file.147.path=.specify/skills/sdd-loop-driver/references/dispatch-recipes.md
file.147.verdict=skipped
file.147.reason=generated
file.148.path=.specify/skills/sdd-loop-driver/references/stage-prompts.md
file.148.verdict=skipped
file.148.reason=generated
file.149.path=.specify/specs/106-background-silent-failure/baseline-failed.txt
file.149.verdict=skipped
file.149.reason=non-code-file
file.150.path=.specify/specs/106-background-silent-failure/checklists/background-settlement-2026-11-25.md
file.150.verdict=skipped
file.150.reason=non-code-file
file.151.path=.specify/specs/106-background-silent-failure/checklists/requirements.md
file.151.verdict=skipped
file.151.reason=non-code-file
file.152.path=.specify/specs/106-background-silent-failure/checkpoints/01-requirements.md
file.152.verdict=skipped
file.152.reason=non-code-file
file.153.path=.specify/specs/106-background-silent-failure/checkpoints/02-clarify.md
file.153.verdict=skipped
file.153.reason=non-code-file
file.154.path=.specify/specs/106-background-silent-failure/checkpoints/03-plan.md
file.154.verdict=skipped
file.154.reason=non-code-file
file.155.path=.specify/specs/106-background-silent-failure/checkpoints/04-tasks.md
file.155.verdict=skipped
file.155.reason=non-code-file
file.156.path=.specify/specs/106-background-silent-failure/checkpoints/05-goal-team-activation.md
file.156.verdict=skipped
file.156.reason=non-code-file
file.157.path=.specify/specs/106-background-silent-failure/checkpoints/06-checklist.md
file.157.verdict=skipped
file.157.reason=non-code-file
file.158.path=.specify/specs/106-background-silent-failure/checkpoints/07-analyze.md
file.158.verdict=skipped
file.158.reason=non-code-file
file.159.path=.specify/specs/106-background-silent-failure/checkpoints/08-implement.md
file.159.verdict=skipped
file.159.reason=non-code-file
file.160.path=.specify/specs/106-background-silent-failure/checkpoints/closure.md
file.160.verdict=skipped
file.160.reason=non-code-file
file.161.path=.specify/specs/106-background-silent-failure/code-review.md
file.161.verdict=skipped
file.161.reason=non-code-file
file.162.path=.specify/specs/106-background-silent-failure/contracts/carrier-conformance.contract.md
file.162.verdict=skipped
file.162.reason=non-code-file
file.163.path=.specify/specs/106-background-silent-failure/contracts/enforcement-and-migration.contract.md
file.163.verdict=skipped
file.163.reason=non-code-file
file.164.path=.specify/specs/106-background-silent-failure/contracts/settlement-contract.contract.md
file.164.verdict=skipped
file.164.reason=non-code-file
file.165.path=.specify/specs/106-background-silent-failure/coverage-baseline.txt
file.165.verdict=skipped
file.165.reason=non-code-file
file.166.path=.specify/specs/106-background-silent-failure/data-model.md
file.166.verdict=skipped
file.166.reason=non-code-file
file.167.path=.specify/specs/106-background-silent-failure/feature-ref.md
file.167.verdict=skipped
file.167.reason=non-code-file
file.168.path=.specify/specs/106-background-silent-failure/final-failed.txt
file.168.verdict=skipped
file.168.reason=non-code-file
file.169.path=.specify/specs/106-background-silent-failure/handoff.md
file.169.verdict=skipped
file.169.reason=non-code-file
file.170.path=.specify/specs/106-background-silent-failure/notes/pre-change-measurements.md
file.170.verdict=skipped
file.170.reason=non-code-file
file.171.path=.specify/specs/106-background-silent-failure/notes/quickstart-run.md
file.171.verdict=skipped
file.171.reason=non-code-file
file.172.path=.specify/specs/106-background-silent-failure/notes/red-first-evidence.md
file.172.verdict=skipped
file.172.reason=non-code-file
file.173.path=.specify/specs/106-background-silent-failure/plan.md
file.173.verdict=skipped
file.173.reason=non-code-file
file.174.path=.specify/specs/106-background-silent-failure/quickstart.md
file.174.verdict=skipped
file.174.reason=non-code-file
file.175.path=.specify/specs/106-background-silent-failure/requirements.md
file.175.verdict=skipped
file.175.reason=non-code-file
file.176.path=.specify/specs/106-background-silent-failure/research.md
file.176.verdict=skipped
file.176.reason=non-code-file
file.177.path=.specify/specs/106-background-silent-failure/review.md
file.177.verdict=skipped
file.177.reason=non-code-file
file.178.path=.specify/specs/106-background-silent-failure/tasks.md
file.178.verdict=skipped
file.178.reason=non-code-file
file.179.path=.specify/specs/106-background-silent-failure/test-evidence/acceptance-106.md
file.179.verdict=skipped
file.179.reason=non-code-file
file.180.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-domain-w1-r2.jsonl
file.180.verdict=skipped
file.180.reason=non-code-file
file.181.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-domain-w1-r3.jsonl
file.181.verdict=skipped
file.181.reason=non-code-file
file.182.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-domain-w1.jsonl
file.182.verdict=skipped
file.182.reason=non-code-file
file.183.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-domain-w2.jsonl
file.183.verdict=skipped
file.183.reason=non-code-file
file.184.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-domain-w2a-r2.jsonl
file.184.verdict=skipped
file.184.reason=non-code-file
file.185.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-domain-w2a-r3.jsonl
file.185.verdict=skipped
file.185.reason=non-code-file
file.186.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-domain-w2b-r2.jsonl
file.186.verdict=skipped
file.186.reason=non-code-file
file.187.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-domain-w2b-r3.jsonl
file.187.verdict=skipped
file.187.reason=non-code-file
file.188.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-domain-w2c-r2.jsonl
file.188.verdict=skipped
file.188.reason=non-code-file
file.189.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-domain-w2c-r3.jsonl
file.189.verdict=skipped
file.189.reason=non-code-file
file.190.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-domain-w3-r2.jsonl
file.190.verdict=skipped
file.190.reason=non-code-file
file.191.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-domain-w3-r3.jsonl
file.191.verdict=skipped
file.191.reason=non-code-file
file.192.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-domain-w3.jsonl
file.192.verdict=skipped
file.192.reason=non-code-file
file.193.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-incremental-r4.jsonl
file.193.verdict=skipped
file.193.reason=non-code-file
file.194.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-incremental-r5.jsonl
file.194.verdict=skipped
file.194.reason=non-code-file
file.195.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-r4-reused-domain-hashes.txt
file.195.verdict=skipped
file.195.reason=non-code-file
file.196.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair-2026-11-25.md
file.196.verdict=skipped
file.196.reason=non-code-file
file.197.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair-clause-coverage.txt
file.197.verdict=skipped
file.197.reason=non-code-file
file.198.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair-clause-extract.json
file.198.verdict=skipped
file.198.reason=non-code-file
file.199.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair-decomposition.txt
file.199.verdict=skipped
file.199.reason=non-code-file
file.200.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair-gate-scan.json
file.200.verdict=skipped
file.200.reason=non-code-file
file.201.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair-glossary-validate.txt
file.201.verdict=skipped
file.201.reason=non-code-file
file.202.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair-pre-analyze-plan.txt
file.202.verdict=skipped
file.202.reason=non-code-file
file.203.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair-pre-analyze-requirements.txt
file.203.verdict=skipped
file.203.reason=non-code-file
file.204.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair-pre-analyze-tasks.txt
file.204.verdict=skipped
file.204.reason=non-code-file
file.205.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair-requirements-validator.txt
file.205.verdict=skipped
file.205.reason=non-code-file
file.206.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair-tasks-validator.txt
file.206.verdict=skipped
file.206.reason=non-code-file
file.207.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair2-2026-11-25.md
file.207.verdict=skipped
file.207.reason=non-code-file
file.208.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair2-clause-coverage.txt
file.208.verdict=skipped
file.208.reason=non-code-file
file.209.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair2-clause-extract.json
file.209.verdict=skipped
file.209.reason=non-code-file
file.210.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair2-decomposition.txt
file.210.verdict=skipped
file.210.reason=non-code-file
file.211.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair2-gate-scan.json
file.211.verdict=skipped
file.211.reason=non-code-file
file.212.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair2-glossary-validate.txt
file.212.verdict=skipped
file.212.reason=non-code-file
file.213.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair2-pre-analyze-plan.txt
file.213.verdict=skipped
file.213.reason=non-code-file
file.214.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair2-pre-analyze-requirements.txt
file.214.verdict=skipped
file.214.reason=non-code-file
file.215.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair2-pre-analyze-tasks.txt
file.215.verdict=skipped
file.215.reason=non-code-file
file.216.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair2-requirements-validator.txt
file.216.verdict=skipped
file.216.reason=non-code-file
file.217.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair2-tasks-validator.txt
file.217.verdict=skipped
file.217.reason=non-code-file
file.218.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair3-2026-11-25.md
file.218.verdict=skipped
file.218.reason=non-code-file
file.219.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair3-clause-coverage.txt
file.219.verdict=skipped
file.219.reason=non-code-file
file.220.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair3-clause-extract.json
file.220.verdict=skipped
file.220.reason=non-code-file
file.221.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair3-decomposition.txt
file.221.verdict=skipped
file.221.reason=non-code-file
file.222.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair3-gate-scan.json
file.222.verdict=skipped
file.222.reason=non-code-file
file.223.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair3-glossary-validate.txt
file.223.verdict=skipped
file.223.reason=non-code-file
file.224.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair3-pre-analyze-plan.txt
file.224.verdict=skipped
file.224.reason=non-code-file
file.225.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair3-pre-analyze-requirements.txt
file.225.verdict=skipped
file.225.reason=non-code-file
file.226.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair3-pre-analyze-tasks.txt
file.226.verdict=skipped
file.226.reason=non-code-file
file.227.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair3-requirements-validator.txt
file.227.verdict=skipped
file.227.reason=non-code-file
file.228.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair3-run-id.txt
file.228.verdict=skipped
file.228.reason=non-code-file
file.229.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair3-tasks-validator.txt
file.229.verdict=skipped
file.229.reason=non-code-file
file.230.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair4-2026-11-26.md
file.230.verdict=skipped
file.230.reason=non-code-file
file.231.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair4-clause-coverage.txt
file.231.verdict=skipped
file.231.reason=non-code-file
file.232.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair4-clause-extract.json
file.232.verdict=skipped
file.232.reason=non-code-file
file.233.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair4-decomposition.txt
file.233.verdict=skipped
file.233.reason=non-code-file
file.234.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair4-gate-scan.json
file.234.verdict=skipped
file.234.reason=non-code-file
file.235.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair4-glossary-validate.txt
file.235.verdict=skipped
file.235.reason=non-code-file
file.236.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair4-pre-analyze-plan.txt
file.236.verdict=skipped
file.236.reason=non-code-file
file.237.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair4-pre-analyze-requirements.txt
file.237.verdict=skipped
file.237.reason=non-code-file
file.238.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair4-pre-analyze-tasks.txt
file.238.verdict=skipped
file.238.reason=non-code-file
file.239.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair4-requirements-validator.txt
file.239.verdict=skipped
file.239.reason=non-code-file
file.240.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair4-run-id.txt
file.240.verdict=skipped
file.240.reason=non-code-file
file.241.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair4-tasks-validator.txt
file.241.verdict=skipped
file.241.reason=non-code-file
file.242.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-report-2026-11-25.md
file.242.verdict=skipped
file.242.reason=non-code-file
file.243.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-report-r5-2026-11-26.md
file.243.verdict=skipped
file.243.reason=non-code-file
file.244.path=.specify/specs/106-background-silent-failure/test-evidence/analyze.jsonl
file.244.verdict=skipped
file.244.reason=non-code-file
file.245.path=.specify/specs/106-background-silent-failure/test-evidence/checklist-artifact-counts.txt
file.245.verdict=skipped
file.245.reason=non-code-file
file.246.path=.specify/specs/106-background-silent-failure/test-evidence/checklist-requirements-validator.txt
file.246.verdict=skipped
file.246.reason=non-code-file
file.247.path=.specify/specs/106-background-silent-failure/test-evidence/checklist.jsonl
file.247.verdict=skipped
file.247.reason=non-code-file
file.248.path=.specify/specs/106-background-silent-failure/test-evidence/clarify.jsonl
file.248.verdict=skipped
file.248.reason=non-code-file
file.249.path=.specify/specs/106-background-silent-failure/test-evidence/clause-coverage-tasks.txt
file.249.verdict=skipped
file.249.reason=non-code-file
file.250.path=.specify/specs/106-background-silent-failure/test-evidence/closure-full-run-r2-summary.txt
file.250.verdict=skipped
file.250.reason=non-code-file
file.251.path=.specify/specs/106-background-silent-failure/test-evidence/confirmation-total-red-at-base.txt
file.251.verdict=skipped
file.251.reason=non-code-file
file.252.path=.specify/specs/106-background-silent-failure/test-evidence/decomposition-plan.json
file.252.verdict=skipped
file.252.reason=non-code-file
file.253.path=.specify/specs/106-background-silent-failure/test-evidence/decomposition-plan.stdout.txt
file.253.verdict=skipped
file.253.reason=non-code-file
file.254.path=.specify/specs/106-background-silent-failure/test-evidence/enforcement-honesty.md
file.254.verdict=skipped
file.254.reason=non-code-file
file.255.path=.specify/specs/106-background-silent-failure/test-evidence/exec-quant-analyze-repair.txt
file.255.verdict=skipped
file.255.reason=non-code-file
file.256.path=.specify/specs/106-background-silent-failure/test-evidence/exec-quant-analyze-repair2.txt
file.256.verdict=skipped
file.256.reason=non-code-file
file.257.path=.specify/specs/106-background-silent-failure/test-evidence/exec-quant-analyze-repair3.txt
file.257.verdict=skipped
file.257.reason=non-code-file
file.258.path=.specify/specs/106-background-silent-failure/test-evidence/exec-quant-analyze-repair4.txt
file.258.verdict=skipped
file.258.reason=non-code-file
file.259.path=.specify/specs/106-background-silent-failure/test-evidence/exec-quant-analyze.txt
file.259.verdict=skipped
file.259.reason=non-code-file
file.260.path=.specify/specs/106-background-silent-failure/test-evidence/exec-quant-checklist.txt
file.260.verdict=skipped
file.260.reason=non-code-file
file.261.path=.specify/specs/106-background-silent-failure/test-evidence/exec-quant-clarify.txt
file.261.verdict=skipped
file.261.reason=non-code-file
file.262.path=.specify/specs/106-background-silent-failure/test-evidence/exec-quant-plan.txt
file.262.verdict=skipped
file.262.reason=non-code-file
file.263.path=.specify/specs/106-background-silent-failure/test-evidence/exec-quant-tasks.txt
file.263.verdict=skipped
file.263.reason=non-code-file
file.264.path=.specify/specs/106-background-silent-failure/test-evidence/exec-quant.txt
file.264.verdict=skipped
file.264.reason=non-code-file
file.265.path=.specify/specs/106-background-silent-failure/test-evidence/feedback-record-analyze-repair.txt
file.265.verdict=skipped
file.265.reason=non-code-file
file.266.path=.specify/specs/106-background-silent-failure/test-evidence/feedback-record-analyze-repair2.txt
file.266.verdict=skipped
file.266.reason=non-code-file
file.267.path=.specify/specs/106-background-silent-failure/test-evidence/feedback-record-analyze-repair3.txt
file.267.verdict=skipped
file.267.reason=non-code-file
file.268.path=.specify/specs/106-background-silent-failure/test-evidence/feedback-record-analyze-repair4.txt
file.268.verdict=skipped
file.268.reason=non-code-file
file.269.path=.specify/specs/106-background-silent-failure/test-evidence/feedback-record-analyze.txt
file.269.verdict=skipped
file.269.reason=non-code-file
file.270.path=.specify/specs/106-background-silent-failure/test-evidence/feedback-record-checklist.txt
file.270.verdict=skipped
file.270.reason=non-code-file
file.271.path=.specify/specs/106-background-silent-failure/test-evidence/feedback-record-clarify.txt
file.271.verdict=skipped
file.271.reason=non-code-file
file.272.path=.specify/specs/106-background-silent-failure/test-evidence/feedback-record-plan.txt
file.272.verdict=skipped
file.272.reason=non-code-file
file.273.path=.specify/specs/106-background-silent-failure/test-evidence/feedback-record-tasks.txt
file.273.verdict=skipped
file.273.reason=non-code-file
file.274.path=.specify/specs/106-background-silent-failure/test-evidence/feedback-record.txt
file.274.verdict=skipped
file.274.reason=non-code-file
file.275.path=.specify/specs/106-background-silent-failure/test-evidence/final-gate.txt
file.275.verdict=skipped
file.275.reason=non-code-file
file.276.path=.specify/specs/106-background-silent-failure/test-evidence/flow-class-lookup-checklist.txt
file.276.verdict=skipped
file.276.reason=non-code-file
file.277.path=.specify/specs/106-background-silent-failure/test-evidence/flow-class-lookup-clarify.txt
file.277.verdict=skipped
file.277.reason=non-code-file
file.278.path=.specify/specs/106-background-silent-failure/test-evidence/flow-class-lookup-plan.txt
file.278.verdict=skipped
file.278.reason=non-code-file
file.279.path=.specify/specs/106-background-silent-failure/test-evidence/flow-class-lookup.txt
file.279.verdict=skipped
file.279.reason=non-code-file
file.280.path=.specify/specs/106-background-silent-failure/test-evidence/git-access-anomaly.txt
file.280.verdict=skipped
file.280.reason=non-code-file
file.281.path=.specify/specs/106-background-silent-failure/test-evidence/git-commit-attempt-clarify.txt
file.281.verdict=skipped
file.281.reason=non-code-file
file.282.path=.specify/specs/106-background-silent-failure/test-evidence/glossary-proposal-plan.txt
file.282.verdict=skipped
file.282.reason=non-code-file
file.283.path=.specify/specs/106-background-silent-failure/test-evidence/goal-team-activation.txt
file.283.verdict=skipped
file.283.reason=non-code-file
file.284.path=.specify/specs/106-background-silent-failure/test-evidence/implement-baseline-full.txt
file.284.verdict=skipped
file.284.reason=non-code-file
file.285.path=.specify/specs/106-background-silent-failure/test-evidence/implement-integration.md
file.285.verdict=skipped
file.285.reason=non-code-file
file.286.path=.specify/specs/106-background-silent-failure/test-evidence/mirror-check-baseline.txt
file.286.verdict=skipped
file.286.reason=non-code-file
file.287.path=.specify/specs/106-background-silent-failure/test-evidence/mutation-drill.md
file.287.verdict=skipped
file.287.reason=non-code-file
file.288.path=.specify/specs/106-background-silent-failure/test-evidence/non-goals-audit.md
file.288.verdict=skipped
file.288.reason=non-code-file
file.289.path=.specify/specs/106-background-silent-failure/test-evidence/plan-stage-2026-11-25.md
file.289.verdict=skipped
file.289.reason=non-code-file
file.290.path=.specify/specs/106-background-silent-failure/test-evidence/plan.jsonl
file.290.verdict=skipped
file.290.reason=non-code-file
file.291.path=.specify/specs/106-background-silent-failure/test-evidence/pre-analyze-plan-before-fill.txt
file.291.verdict=skipped
file.291.reason=non-code-file
file.292.path=.specify/specs/106-background-silent-failure/test-evidence/pre-analyze-plan.json
file.292.verdict=skipped
file.292.reason=non-code-file
file.293.path=.specify/specs/106-background-silent-failure/test-evidence/pre-analyze-plan.stdout.txt
file.293.verdict=skipped
file.293.reason=non-code-file
file.294.path=.specify/specs/106-background-silent-failure/test-evidence/pre-analyze-requirements-clarify.json
file.294.verdict=skipped
file.294.reason=non-code-file
file.295.path=.specify/specs/106-background-silent-failure/test-evidence/pre-analyze-requirements-clarify.stdout.txt
file.295.verdict=skipped
file.295.reason=non-code-file
file.296.path=.specify/specs/106-background-silent-failure/test-evidence/pre-analyze-requirements.json
file.296.verdict=skipped
file.296.reason=non-code-file
file.297.path=.specify/specs/106-background-silent-failure/test-evidence/pre-analyze-requirements.stdout.txt
file.297.verdict=skipped
file.297.reason=non-code-file
file.298.path=.specify/specs/106-background-silent-failure/test-evidence/pre-analyze-tasks.json
file.298.verdict=skipped
file.298.reason=non-code-file
file.299.path=.specify/specs/106-background-silent-failure/test-evidence/pre-analyze-tasks.stdout.txt
file.299.verdict=skipped
file.299.reason=non-code-file
file.300.path=.specify/specs/106-background-silent-failure/test-evidence/quickstart-role-edge-empty-report.json
file.300.verdict=skipped
file.300.reason=non-code-file
file.301.path=.specify/specs/106-background-silent-failure/test-evidence/quickstart-role-edge-help.txt
file.301.verdict=skipped
file.301.reason=non-code-file
file.302.path=.specify/specs/106-background-silent-failure/test-evidence/reaction-drill.md
file.302.verdict=skipped
file.302.reason=non-code-file
file.303.path=.specify/specs/106-background-silent-failure/test-evidence/review-evidence.txt
file.303.verdict=skipped
file.303.reason=non-code-file
file.304.path=.specify/specs/106-background-silent-failure/test-evidence/review-workspace-before-commit.json
file.304.verdict=skipped
file.304.reason=non-code-file
file.305.path=.specify/specs/106-background-silent-failure/test-evidence/review-workspace-postcommit.txt
file.305.verdict=skipped
file.305.reason=non-code-file
file.306.path=.specify/specs/106-background-silent-failure/test-evidence/review.jsonl
file.306.verdict=skipped
file.306.reason=non-code-file
file.307.path=.specify/specs/106-background-silent-failure/test-evidence/role-edge-report-empty-fbab7a45c.json
file.307.verdict=skipped
file.307.reason=non-code-file
file.308.path=.specify/specs/106-background-silent-failure/test-evidence/run-determination-analyze-repair.txt
file.308.verdict=skipped
file.308.reason=non-code-file
file.309.path=.specify/specs/106-background-silent-failure/test-evidence/run-determination-analyze-repair2.txt
file.309.verdict=skipped
file.309.reason=non-code-file
file.310.path=.specify/specs/106-background-silent-failure/test-evidence/run-determination-analyze-repair3.txt
file.310.verdict=skipped
file.310.reason=non-code-file
file.311.path=.specify/specs/106-background-silent-failure/test-evidence/run-determination-analyze-repair4.txt
file.311.verdict=skipped
file.311.reason=non-code-file
file.312.path=.specify/specs/106-background-silent-failure/test-evidence/run-determination-analyze.txt
file.312.verdict=skipped
file.312.reason=non-code-file
file.313.path=.specify/specs/106-background-silent-failure/test-evidence/run-determination-checklist.txt
file.313.verdict=skipped
file.313.reason=non-code-file
file.314.path=.specify/specs/106-background-silent-failure/test-evidence/run-determination-clarify.txt
file.314.verdict=skipped
file.314.reason=non-code-file
file.315.path=.specify/specs/106-background-silent-failure/test-evidence/run-determination-plan.txt
file.315.verdict=skipped
file.315.reason=non-code-file
file.316.path=.specify/specs/106-background-silent-failure/test-evidence/run-determination-tasks.txt
file.316.verdict=skipped
file.316.reason=non-code-file
file.317.path=.specify/specs/106-background-silent-failure/test-evidence/run-determination.txt
file.317.verdict=skipped
file.317.reason=non-code-file
file.318.path=.specify/specs/106-background-silent-failure/test-evidence/scan-confirmation-gates-baseline.json
file.318.verdict=skipped
file.318.reason=non-code-file
file.319.path=.specify/specs/106-background-silent-failure/test-evidence/super-sub-protocol-fbab7a45c.txt
file.319.verdict=skipped
file.319.reason=non-code-file
file.320.path=.specify/specs/106-background-silent-failure/test-evidence/t033-smoke.txt
file.320.verdict=skipped
file.320.reason=non-code-file
file.321.path=.specify/specs/106-background-silent-failure/test-evidence/tasks-premises.txt
file.321.verdict=skipped
file.321.reason=non-code-file
file.322.path=.specify/specs/106-background-silent-failure/test-evidence/tasks.jsonl
file.322.verdict=skipped
file.322.reason=non-code-file
file.323.path=.specify/specs/106-background-silent-failure/test-evidence/test-entry-smoke.txt
file.323.verdict=skipped
file.323.reason=non-code-file
file.324.path=.specify/specs/106-background-silent-failure/test-evidence/validate-r4-01.verdicts.json
file.324.verdict=skipped
file.324.reason=non-code-file
file.325.path=.specify/specs/106-background-silent-failure/test-evidence/validate-tasks.json
file.325.verdict=skipped
file.325.reason=non-code-file
file.326.path=.specify/specs/106-background-silent-failure/test-evidence/validate-tasks.stdout.txt
file.326.verdict=skipped
file.326.reason=non-code-file
file.327.path=.specify/specs/106-background-silent-failure/test-evidence/validate-wave1.verdicts.json
file.327.verdict=skipped
file.327.reason=non-code-file
file.328.path=.specify/specs/106-background-silent-failure/test-evidence/validate-wave2.verdicts.json
file.328.verdict=skipped
file.328.reason=non-code-file
file.329.path=.specify/specs/106-background-silent-failure/test-evidence/validate-wave3.verdicts.json
file.329.verdict=skipped
file.329.reason=non-code-file
file.330.path=.specify/specs/106-background-silent-failure/test-evidence/validator-requirements-clarify.txt
file.330.verdict=skipped
file.330.reason=non-code-file
file.331.path=.specify/specs/106-background-silent-failure/test-evidence/validator-requirements.txt
file.331.verdict=skipped
file.331.reason=non-code-file
file.332.path=.specify/specs/106-background-silent-failure/test-evidence/verification-input.md
file.332.verdict=skipped
file.332.reason=non-code-file
file.333.path=.specify/specs/106-background-silent-failure/test-evidence/watch-help-baseline.txt
file.333.verdict=skipped
file.333.reason=non-code-file
file.334.path=.specify/specs/106-background-silent-failure/test-evidence/watch-self-test-baseline.txt
file.334.verdict=skipped
file.334.reason=non-code-file
file.335.path=.specify/specs/106-background-silent-failure/test-evidence/watch-target-fbab7a45c.sh
file.335.verdict=skipped
file.335.reason=non-code-file
file.336.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-check-analyze-repair-before-commit.txt
file.336.verdict=skipped
file.336.reason=non-code-file
file.337.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-check-analyze-repair-postcommit.txt
file.337.verdict=skipped
file.337.reason=non-code-file
file.338.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-check-analyze-repair2-before-commit.txt
file.338.verdict=skipped
file.338.reason=non-code-file
file.339.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-check-analyze-repair2-postcommit.txt
file.339.verdict=skipped
file.339.reason=non-code-file
file.340.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-check-analyze-repair3-before-commit.txt
file.340.verdict=skipped
file.340.reason=non-code-file
file.341.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-check-analyze-repair3-postcommit.txt
file.341.verdict=skipped
file.341.reason=non-code-file
file.342.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-check-analyze-repair4-before-commit.txt
file.342.verdict=skipped
file.342.reason=non-code-file
file.343.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-check-analyze-repair4-postcommit.txt
file.343.verdict=skipped
file.343.reason=non-code-file
file.344.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-check-checklist-postcommit.txt
file.344.verdict=skipped
file.344.reason=non-code-file
file.345.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-check-checklist.txt
file.345.verdict=skipped
file.345.reason=non-code-file
file.346.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-check-clarify-repair.txt
file.346.verdict=skipped
file.346.reason=non-code-file
file.347.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-check-clarify.txt
file.347.verdict=skipped
file.347.reason=non-code-file
file.348.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-check.txt
file.348.verdict=skipped
file.348.reason=non-code-file
file.349.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-plan-after-driver.json
file.349.verdict=skipped
file.349.reason=non-code-file
file.350.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-plan-after.json
file.350.verdict=skipped
file.350.reason=non-code-file
file.351.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-plan-before.json
file.351.verdict=skipped
file.351.reason=non-code-file
file.352.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-requirements.json
file.352.verdict=skipped
file.352.reason=non-code-file
file.353.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-snapshot-analyze-before-commit.json
file.353.verdict=skipped
file.353.reason=non-code-file
file.354.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-snapshot-analyze-repair-before-commit.json
file.354.verdict=skipped
file.354.reason=non-code-file
file.355.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-snapshot-analyze-repair2-before.json
file.355.verdict=skipped
file.355.reason=non-code-file
file.356.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-snapshot-analyze-repair3-before.json
file.356.verdict=skipped
file.356.reason=non-code-file
file.357.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-snapshot-analyze-repair4-before.json
file.357.verdict=skipped
file.357.reason=non-code-file
file.358.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-snapshot-checklist-after.json
file.358.verdict=skipped
file.358.reason=non-code-file
file.359.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-snapshot-checklist-before.json
file.359.verdict=skipped
file.359.reason=non-code-file
file.360.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-tasks-after.json
file.360.verdict=skipped
file.360.reason=non-code-file
file.361.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-tasks-before.json
file.361.verdict=skipped
file.361.reason=non-code-file
file.362.path=.specify/specs/106-background-silent-failure/verification.md
file.362.verdict=skipped
file.362.reason=non-code-file
file.363.path=.specify/specs/107-decision-governance/baseline-failed.txt
file.363.verdict=skipped
file.363.reason=non-code-file
file.364.path=.specify/specs/107-decision-governance/checklists/decision-governance-2026-11-26.md
file.364.verdict=skipped
file.364.reason=non-code-file
file.365.path=.specify/specs/107-decision-governance/checklists/requirements.md
file.365.verdict=skipped
file.365.reason=non-code-file
file.366.path=.specify/specs/107-decision-governance/checkpoints/01-requirements.md
file.366.verdict=skipped
file.366.reason=non-code-file
file.367.path=.specify/specs/107-decision-governance/checkpoints/02-clarify.md
file.367.verdict=skipped
file.367.reason=non-code-file
file.368.path=.specify/specs/107-decision-governance/checkpoints/03-plan.md
file.368.verdict=skipped
file.368.reason=non-code-file
file.369.path=.specify/specs/107-decision-governance/checkpoints/04-tasks.md
file.369.verdict=skipped
file.369.reason=non-code-file
file.370.path=.specify/specs/107-decision-governance/checkpoints/05-goal-team-activation.md
file.370.verdict=skipped
file.370.reason=non-code-file
file.371.path=.specify/specs/107-decision-governance/checkpoints/06-checklist.md
file.371.verdict=skipped
file.371.reason=non-code-file
file.372.path=.specify/specs/107-decision-governance/checkpoints/07-analyze.md
file.372.verdict=skipped
file.372.reason=non-code-file
file.373.path=.specify/specs/107-decision-governance/checkpoints/08-implement.md
file.373.verdict=skipped
file.373.reason=non-code-file
file.374.path=.specify/specs/107-decision-governance/contracts/archive-and-audit.contract.md
file.374.verdict=skipped
file.374.reason=non-code-file
file.375.path=.specify/specs/107-decision-governance/contracts/enforcement-boundary.contract.md
file.375.verdict=skipped
file.375.reason=non-code-file
file.376.path=.specify/specs/107-decision-governance/contracts/migration-and-compat.contract.md
file.376.verdict=skipped
file.376.reason=non-code-file
file.377.path=.specify/specs/107-decision-governance/contracts/text-and-options.contract.md
file.377.verdict=skipped
file.377.reason=non-code-file
file.378.path=.specify/specs/107-decision-governance/contracts/transmission-and-implementation.contract.md
file.378.verdict=skipped
file.378.reason=non-code-file
file.379.path=.specify/specs/107-decision-governance/data-model.md
file.379.verdict=skipped
file.379.reason=non-code-file
file.380.path=.specify/specs/107-decision-governance/feature-ref.md
file.380.verdict=skipped
file.380.reason=non-code-file
file.381.path=.specify/specs/107-decision-governance/handoff.md
file.381.verdict=skipped
file.381.reason=non-code-file
file.382.path=.specify/specs/107-decision-governance/notes/pre-change-measurements.md
file.382.verdict=skipped
file.382.reason=non-code-file
file.383.path=.specify/specs/107-decision-governance/notes/quickstart-run.md
file.383.verdict=skipped
file.383.reason=non-code-file
file.384.path=.specify/specs/107-decision-governance/notes/red-first-evidence.md
file.384.verdict=skipped
file.384.reason=non-code-file
file.385.path=.specify/specs/107-decision-governance/notes/us1-green.txt
file.385.verdict=skipped
file.385.reason=non-code-file
file.386.path=.specify/specs/107-decision-governance/notes/us2-green.txt
file.386.verdict=skipped
file.386.reason=non-code-file
file.387.path=.specify/specs/107-decision-governance/notes/us3-green.txt
file.387.verdict=skipped
file.387.reason=non-code-file
file.388.path=.specify/specs/107-decision-governance/notes/us4-green-slots.txt
file.388.verdict=skipped
file.388.reason=non-code-file
file.389.path=.specify/specs/107-decision-governance/notes/us4-green.txt
file.389.verdict=skipped
file.389.reason=non-code-file
file.390.path=.specify/specs/107-decision-governance/notes/us5-green-slots.txt
file.390.verdict=skipped
file.390.reason=non-code-file
file.391.path=.specify/specs/107-decision-governance/notes/us5-green.txt
file.391.verdict=skipped
file.391.reason=non-code-file
file.392.path=.specify/specs/107-decision-governance/notes/us6-green-slots.txt
file.392.verdict=skipped
file.392.reason=non-code-file
file.393.path=.specify/specs/107-decision-governance/notes/us6-green.txt
file.393.verdict=skipped
file.393.reason=non-code-file
file.394.path=.specify/specs/107-decision-governance/plan.md
file.394.verdict=skipped
file.394.reason=non-code-file
file.395.path=.specify/specs/107-decision-governance/quickstart.md
file.395.verdict=skipped
file.395.reason=non-code-file
file.396.path=.specify/specs/107-decision-governance/requirements.md
file.396.verdict=skipped
file.396.reason=non-code-file
file.397.path=.specify/specs/107-decision-governance/research.md
file.397.verdict=skipped
file.397.reason=non-code-file
file.398.path=.specify/specs/107-decision-governance/tasks.md
file.398.verdict=skipped
file.398.reason=non-code-file
file.399.path=.specify/specs/107-decision-governance/test-evidence/analyze-domain-w1-r2.jsonl
file.399.verdict=skipped
file.399.reason=non-code-file
file.400.path=.specify/specs/107-decision-governance/test-evidence/analyze-domain-w1-r3.jsonl
file.400.verdict=skipped
file.400.reason=non-code-file
file.401.path=.specify/specs/107-decision-governance/test-evidence/analyze-domain-w1.jsonl
file.401.verdict=skipped
file.401.reason=non-code-file
file.402.path=.specify/specs/107-decision-governance/test-evidence/analyze-domain-w2-r2.jsonl
file.402.verdict=skipped
file.402.reason=non-code-file
file.403.path=.specify/specs/107-decision-governance/test-evidence/analyze-domain-w2-r3.jsonl
file.403.verdict=skipped
file.403.reason=non-code-file
file.404.path=.specify/specs/107-decision-governance/test-evidence/analyze-domain-w2.jsonl
file.404.verdict=skipped
file.404.reason=non-code-file
file.405.path=.specify/specs/107-decision-governance/test-evidence/analyze-domain-w3-r2.jsonl
file.405.verdict=skipped
file.405.reason=non-code-file
file.406.path=.specify/specs/107-decision-governance/test-evidence/analyze-domain-w3-r3.jsonl
file.406.verdict=skipped
file.406.reason=non-code-file
file.407.path=.specify/specs/107-decision-governance/test-evidence/analyze-domain-w3.jsonl
file.407.verdict=skipped
file.407.reason=non-code-file
file.408.path=.specify/specs/107-decision-governance/test-evidence/analyze-final-report-r5-2026-11-26.md
file.408.verdict=skipped
file.408.reason=non-code-file
file.409.path=.specify/specs/107-decision-governance/test-evidence/analyze-incremental-r4.jsonl
file.409.verdict=skipped
file.409.reason=non-code-file
file.410.path=.specify/specs/107-decision-governance/test-evidence/analyze-incremental-r5.jsonl
file.410.verdict=skipped
file.410.reason=non-code-file
file.411.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair-2026-11-26.md
file.411.verdict=skipped
file.411.reason=non-code-file
file.412.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair-decomposition.txt
file.412.verdict=skipped
file.412.reason=non-code-file
file.413.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair-pre-analyze-plan.txt
file.413.verdict=skipped
file.413.reason=non-code-file
file.414.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair-pre-analyze-requirements.txt
file.414.verdict=skipped
file.414.reason=non-code-file
file.415.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair-pre-analyze-tasks.txt
file.415.verdict=skipped
file.415.reason=non-code-file
file.416.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair-readings-postcommit.txt
file.416.verdict=skipped
file.416.reason=non-code-file
file.417.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair-readings.txt
file.417.verdict=skipped
file.417.reason=non-code-file
file.418.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair-validate-requirements.txt
file.418.verdict=skipped
file.418.reason=non-code-file
file.419.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair-validate-tasks.txt
file.419.verdict=skipped
file.419.reason=non-code-file
file.420.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair2-2026-11-26.md
file.420.verdict=skipped
file.420.reason=non-code-file
file.421.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair2-decomposition.txt
file.421.verdict=skipped
file.421.reason=non-code-file
file.422.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair2-pre-analyze-plan.txt
file.422.verdict=skipped
file.422.reason=non-code-file
file.423.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair2-pre-analyze-requirements.txt
file.423.verdict=skipped
file.423.reason=non-code-file
file.424.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair2-pre-analyze-tasks.txt
file.424.verdict=skipped
file.424.reason=non-code-file
file.425.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair2-readings-postcommit.txt
file.425.verdict=skipped
file.425.reason=non-code-file
file.426.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair2-readings.txt
file.426.verdict=skipped
file.426.reason=non-code-file
file.427.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair2-validate-requirements.txt
file.427.verdict=skipped
file.427.reason=non-code-file
file.428.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair2-validate-tasks.txt
file.428.verdict=skipped
file.428.reason=non-code-file
file.429.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair3-2026-11-26.md
file.429.verdict=skipped
file.429.reason=non-code-file
file.430.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair3-decomposition.txt
file.430.verdict=skipped
file.430.reason=non-code-file
file.431.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair3-pre-analyze-plan.txt
file.431.verdict=skipped
file.431.reason=non-code-file
file.432.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair3-pre-analyze-requirements.txt
file.432.verdict=skipped
file.432.reason=non-code-file
file.433.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair3-pre-analyze-tasks.txt
file.433.verdict=skipped
file.433.reason=non-code-file
file.434.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair3-readings-postcommit.txt
file.434.verdict=skipped
file.434.reason=non-code-file
file.435.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair3-readings.txt
file.435.verdict=skipped
file.435.reason=non-code-file
file.436.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair3-validate-requirements.txt
file.436.verdict=skipped
file.436.reason=non-code-file
file.437.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair3-validate-tasks.txt
file.437.verdict=skipped
file.437.reason=non-code-file
file.438.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair4-2026-11-26.md
file.438.verdict=skipped
file.438.reason=non-code-file
file.439.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair4-decomposition.txt
file.439.verdict=skipped
file.439.reason=non-code-file
file.440.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair4-pre-analyze-plan.txt
file.440.verdict=skipped
file.440.reason=non-code-file
file.441.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair4-pre-analyze-requirements.txt
file.441.verdict=skipped
file.441.reason=non-code-file
file.442.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair4-pre-analyze-tasks.txt
file.442.verdict=skipped
file.442.reason=non-code-file
file.443.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair4-readings-postcommit.txt
file.443.verdict=skipped
file.443.reason=non-code-file
file.444.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair4-readings.txt
file.444.verdict=skipped
file.444.reason=non-code-file
file.445.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair4-validate-requirements.txt
file.445.verdict=skipped
file.445.reason=non-code-file
file.446.path=.specify/specs/107-decision-governance/test-evidence/analyze-repair4-validate-tasks.txt
file.446.verdict=skipped
file.446.reason=non-code-file
file.447.path=.specify/specs/107-decision-governance/test-evidence/analyze.jsonl
file.447.verdict=skipped
file.447.reason=non-code-file
file.448.path=.specify/specs/107-decision-governance/test-evidence/checklist-requirements-validator.txt
file.448.verdict=skipped
file.448.reason=non-code-file
file.449.path=.specify/specs/107-decision-governance/test-evidence/checklist-spec-readings.txt
file.449.verdict=skipped
file.449.reason=non-code-file
file.450.path=.specify/specs/107-decision-governance/test-evidence/checklist-stage-2026-11-26.md
file.450.verdict=skipped
file.450.reason=non-code-file
file.451.path=.specify/specs/107-decision-governance/test-evidence/checklist-targeted-set.txt
file.451.verdict=skipped
file.451.reason=non-code-file
file.452.path=.specify/specs/107-decision-governance/test-evidence/checklist-verification.txt
file.452.verdict=skipped
file.452.reason=non-code-file
file.453.path=.specify/specs/107-decision-governance/test-evidence/checklist.jsonl
file.453.verdict=skipped
file.453.reason=non-code-file
file.454.path=.specify/specs/107-decision-governance/test-evidence/clarify-overlap.txt
file.454.verdict=skipped
file.454.reason=non-code-file
file.455.path=.specify/specs/107-decision-governance/test-evidence/clarify-pre-analyze-requirements.txt
file.455.verdict=skipped
file.455.reason=non-code-file
file.456.path=.specify/specs/107-decision-governance/test-evidence/clarify-stage-2026-11-25.md
file.456.verdict=skipped
file.456.reason=non-code-file
file.457.path=.specify/specs/107-decision-governance/test-evidence/clarify-validator.txt
file.457.verdict=skipped
file.457.reason=non-code-file
file.458.path=.specify/specs/107-decision-governance/test-evidence/clarify-workspace.json
file.458.verdict=skipped
file.458.reason=non-code-file
file.459.path=.specify/specs/107-decision-governance/test-evidence/clarify.jsonl
file.459.verdict=skipped
file.459.reason=non-code-file
file.460.path=.specify/specs/107-decision-governance/test-evidence/closure-failed-names-preservation-sweep.txt
file.460.verdict=skipped
file.460.reason=non-code-file
file.461.path=.specify/specs/107-decision-governance/test-evidence/decomposition-requirements.json
file.461.verdict=skipped
file.461.reason=non-code-file
file.462.path=.specify/specs/107-decision-governance/test-evidence/gate-neutrality.txt
file.462.verdict=skipped
file.462.reason=non-code-file
file.463.path=.specify/specs/107-decision-governance/test-evidence/glossary-discipline.txt
file.463.verdict=skipped
file.463.reason=non-code-file
file.464.path=.specify/specs/107-decision-governance/test-evidence/glossary-proposal-plan-2026-11-25.md
file.464.verdict=skipped
file.464.reason=non-code-file
file.465.path=.specify/specs/107-decision-governance/test-evidence/glossary-proposal.md
file.465.verdict=skipped
file.465.reason=non-code-file
file.466.path=.specify/specs/107-decision-governance/test-evidence/goal-team-activation.txt
file.466.verdict=skipped
file.466.reason=non-code-file
file.467.path=.specify/specs/107-decision-governance/test-evidence/implement-baseline-environment-deltas.md
file.467.verdict=skipped
file.467.reason=non-code-file
file.468.path=.specify/specs/107-decision-governance/test-evidence/implement-baseline.txt
file.468.verdict=skipped
file.468.reason=non-code-file
file.469.path=.specify/specs/107-decision-governance/test-evidence/implement-integration.md
file.469.verdict=skipped
file.469.reason=non-code-file
file.470.path=.specify/specs/107-decision-governance/test-evidence/migration-closure.md
file.470.verdict=skipped
file.470.reason=non-code-file
file.471.path=.specify/specs/107-decision-governance/test-evidence/mirror-foundational.txt
file.471.verdict=skipped
file.471.reason=non-code-file
file.472.path=.specify/specs/107-decision-governance/test-evidence/mutation-drill.md
file.472.verdict=skipped
file.472.reason=non-code-file
file.473.path=.specify/specs/107-decision-governance/test-evidence/overlap-post-plan.txt
file.473.verdict=skipped
file.473.reason=non-code-file
file.474.path=.specify/specs/107-decision-governance/test-evidence/plan-integrity.txt
file.474.verdict=skipped
file.474.reason=non-code-file
file.475.path=.specify/specs/107-decision-governance/test-evidence/plan-rereview-2026-11-26.md
file.475.verdict=skipped
file.475.reason=non-code-file
file.476.path=.specify/specs/107-decision-governance/test-evidence/plan-rereview-integrity.txt
file.476.verdict=skipped
file.476.reason=non-code-file
file.477.path=.specify/specs/107-decision-governance/test-evidence/plan-rereview-pre-analyze-plan.txt
file.477.verdict=skipped
file.477.reason=non-code-file
file.478.path=.specify/specs/107-decision-governance/test-evidence/plan-rereview-targeted-set.txt
file.478.verdict=skipped
file.478.reason=non-code-file
file.479.path=.specify/specs/107-decision-governance/test-evidence/plan-rereview-validate-decision-tensions.txt
file.479.verdict=skipped
file.479.reason=non-code-file
file.480.path=.specify/specs/107-decision-governance/test-evidence/plan-rereview.jsonl
file.480.verdict=skipped
file.480.reason=non-code-file
file.481.path=.specify/specs/107-decision-governance/test-evidence/plan-stage-2026-11-25.md
file.481.verdict=skipped
file.481.reason=non-code-file
file.482.path=.specify/specs/107-decision-governance/test-evidence/plan-targeted-set.txt
file.482.verdict=skipped
file.482.reason=non-code-file
file.483.path=.specify/specs/107-decision-governance/test-evidence/plan.jsonl
file.483.verdict=skipped
file.483.reason=non-code-file
file.484.path=.specify/specs/107-decision-governance/test-evidence/post-generation-quality-gate.txt
file.484.verdict=skipped
file.484.reason=non-code-file
file.485.path=.specify/specs/107-decision-governance/test-evidence/pre-analyze-plan.txt
file.485.verdict=skipped
file.485.reason=non-code-file
file.486.path=.specify/specs/107-decision-governance/test-evidence/pre-analyze-requirements.json
file.486.verdict=skipped
file.486.reason=non-code-file
file.487.path=.specify/specs/107-decision-governance/test-evidence/preservation-sweep.txt
file.487.verdict=skipped
file.487.reason=non-code-file
file.488.path=.specify/specs/107-decision-governance/test-evidence/regen-copies-baseline.txt
file.488.verdict=skipped
file.488.reason=non-code-file
file.489.path=.specify/specs/107-decision-governance/test-evidence/requirements-stage-2026-11-25.md
file.489.verdict=skipped
file.489.reason=non-code-file
file.490.path=.specify/specs/107-decision-governance/test-evidence/requirements-validator.txt
file.490.verdict=skipped
file.490.reason=non-code-file
file.491.path=.specify/specs/107-decision-governance/test-evidence/scan-confirmation-gates-baseline.txt
file.491.verdict=skipped
file.491.reason=non-code-file
file.492.path=.specify/specs/107-decision-governance/test-evidence/sync-mirrors-baseline.txt
file.492.verdict=skipped
file.492.reason=non-code-file
file.493.path=.specify/specs/107-decision-governance/test-evidence/tasks-pre-analyze.txt
file.493.verdict=skipped
file.493.reason=non-code-file
file.494.path=.specify/specs/107-decision-governance/test-evidence/tasks-stage-2026-11-25.md
file.494.verdict=skipped
file.494.reason=non-code-file
file.495.path=.specify/specs/107-decision-governance/test-evidence/tasks-targeted-set.txt
file.495.verdict=skipped
file.495.reason=non-code-file
file.496.path=.specify/specs/107-decision-governance/test-evidence/tasks-validator.txt
file.496.verdict=skipped
file.496.reason=non-code-file
file.497.path=.specify/specs/107-decision-governance/test-evidence/tasks.jsonl
file.497.verdict=skipped
file.497.reason=non-code-file
file.498.path=.specify/specs/107-decision-governance/test-evidence/us1-green-slots.txt
file.498.verdict=skipped
file.498.reason=non-code-file
file.499.path=.specify/specs/107-decision-governance/test-evidence/us1-mirror-check.txt
file.499.verdict=skipped
file.499.reason=non-code-file
file.500.path=.specify/specs/107-decision-governance/test-evidence/us1-red-first.txt
file.500.verdict=skipped
file.500.reason=non-code-file
file.501.path=.specify/specs/107-decision-governance/test-evidence/us2-green-slots.txt
file.501.verdict=skipped
file.501.reason=non-code-file
file.502.path=.specify/specs/107-decision-governance/test-evidence/us2-red-first.txt
file.502.verdict=skipped
file.502.reason=non-code-file
file.503.path=.specify/specs/107-decision-governance/test-evidence/us3-green-slots.txt
file.503.verdict=skipped
file.503.reason=non-code-file
file.504.path=.specify/specs/107-decision-governance/test-evidence/us3-red-first.txt
file.504.verdict=skipped
file.504.reason=non-code-file
file.505.path=.specify/specs/107-decision-governance/test-evidence/us4-mirror-check.txt
file.505.verdict=skipped
file.505.reason=non-code-file
file.506.path=.specify/specs/107-decision-governance/test-evidence/us4-red-first.txt
file.506.verdict=skipped
file.506.reason=non-code-file
file.507.path=.specify/specs/107-decision-governance/test-evidence/us5-mirror-check.txt
file.507.verdict=skipped
file.507.reason=non-code-file
file.508.path=.specify/specs/107-decision-governance/test-evidence/us5-red-first.txt
file.508.verdict=skipped
file.508.reason=non-code-file
file.509.path=.specify/specs/107-decision-governance/test-evidence/us6-migrate-dryrun.json
file.509.verdict=skipped
file.509.reason=non-code-file
file.510.path=.specify/specs/107-decision-governance/test-evidence/us6-mirror-check.txt
file.510.verdict=skipped
file.510.reason=non-code-file
file.511.path=.specify/specs/107-decision-governance/test-evidence/us6-red-first.txt
file.511.verdict=skipped
file.511.reason=non-code-file
file.512.path=.specify/specs/107-decision-governance/test-evidence/validate-decision-tensions.txt
file.512.verdict=skipped
file.512.reason=non-code-file
file.513.path=.specify/specs/107-decision-governance/test-evidence/verification-input.md
file.513.verdict=skipped
file.513.reason=non-code-file
file.514.path=.specify/specs/107-decision-governance/test-evidence/workspace-analyze-repair.json
file.514.verdict=skipped
file.514.reason=non-code-file
file.515.path=.specify/specs/107-decision-governance/test-evidence/workspace-analyze-repair2.json
file.515.verdict=skipped
file.515.reason=non-code-file
file.516.path=.specify/specs/107-decision-governance/test-evidence/workspace-analyze-repair3.json
file.516.verdict=skipped
file.516.reason=non-code-file
file.517.path=.specify/specs/107-decision-governance/test-evidence/workspace-analyze-repair4.json
file.517.verdict=skipped
file.517.reason=non-code-file
file.518.path=.specify/specs/107-decision-governance/test-evidence/workspace-checklist.json
file.518.verdict=skipped
file.518.reason=non-code-file
file.519.path=.specify/specs/107-decision-governance/test-evidence/workspace-plan-after.json
file.519.verdict=skipped
file.519.reason=non-code-file
file.520.path=.specify/specs/107-decision-governance/test-evidence/workspace-plan-before.json
file.520.verdict=skipped
file.520.reason=non-code-file
file.521.path=.specify/specs/107-decision-governance/test-evidence/workspace-plan-rereview-after.json
file.521.verdict=skipped
file.521.reason=non-code-file
file.522.path=.specify/specs/107-decision-governance/test-evidence/workspace-plan-rereview-before.json
file.522.verdict=skipped
file.522.reason=non-code-file
file.523.path=.specify/specs/107-decision-governance/test-evidence/workspace-requirements.json
file.523.verdict=skipped
file.523.reason=non-code-file
file.524.path=.specify/specs/107-decision-governance/test-evidence/workspace-tasks.json
file.524.verdict=skipped
file.524.reason=non-code-file
file.525.path=.specify/teams/106-background-silent-failure/team.md
file.525.verdict=skipped
file.525.reason=non-code-file
file.526.path=.specify/teams/107-decision-governance/team.md
file.526.verdict=skipped
file.526.reason=non-code-file
file.527.path=.specify/templates/instructions-template.md
file.527.verdict=skipped
file.527.reason=generated
file.528.path=agents/sdd-implement-coordinator.agent.md
file.528.verdict=skipped
file.528.reason=size-guard-focus-not-reviewed
file.529.path=agents/sdd-plan-coordinator.agent.md
file.529.verdict=skipped
file.529.reason=size-guard-focus-not-reviewed
file.530.path=agents/sdd-review-coordinator.agent.md
file.530.verdict=skipped
file.530.reason=size-guard-focus-not-reviewed
file.531.path=agents/sdd-task-coordinator.agent.md
file.531.verdict=skipped
file.531.reason=size-guard-focus-not-reviewed
file.532.path=docs/concepts/spec-driven.md
file.532.verdict=reviewed
file.533.path=docs/reference/commands/agents.md
file.533.verdict=skipped
file.533.reason=size-guard-focus-not-reviewed
file.534.path=docs/reference/skills/sdd-loop-driver.md
file.534.verdict=skipped
file.534.reason=size-guard-focus-not-reviewed
file.535.path=docs/reference/teams/orchestration.md
file.535.verdict=skipped
file.535.reason=size-guard-focus-not-reviewed
file.536.path=scripts/bash/generate-instructions.sh
file.536.verdict=reviewed
file.537.path=scripts/python/role-edge-check.py
file.537.verdict=skipped
file.537.reason=size-guard-focus-not-reviewed
file.538.path=scripts/python/validate-decisions.py
file.538.verdict=reviewed
file.539.path=shared/definitions/agent-definitions.md
file.539.verdict=reviewed
file.540.path=shared/definitions/anchor-definitions.md
file.540.verdict=reviewed
file.541.path=shared/definitions/decision-definitions.md
file.541.verdict=reviewed
file.542.path=shared/definitions/framework-map.md
file.542.verdict=reviewed
file.543.path=shared/definitions/goal-definitions.md
file.543.verdict=reviewed
file.544.path=shared/definitions/subagent-definitions.md
file.544.verdict=skipped
file.544.reason=size-guard-focus-not-reviewed
file.545.path=shared/definitions/superagent-definitions.md
file.545.verdict=reviewed
file.546.path=shared/guidelines/confirmation-gates.md
file.546.verdict=reviewed
file.547.path=shared/guidelines/decision-tension.md
file.547.verdict=reviewed
file.548.path=shared/guidelines/fast-fail.md
file.548.verdict=reviewed
file.549.path=shared/workflow/external-dispatch-recipes.md
file.549.verdict=skipped
file.549.reason=size-guard-focus-not-reviewed
file.550.path=skills/external/sdd-loop-driver/SKILL.md
file.550.verdict=skipped
file.550.reason=size-guard-focus-not-reviewed
file.551.path=skills/external/sdd-loop-driver/references/checkpoint-protocol.md
file.551.verdict=reviewed
file.552.path=skills/external/sdd-loop-driver/references/dispatch-recipes.md
file.552.verdict=reviewed
file.553.path=skills/external/sdd-loop-driver/references/stage-prompts.md
file.553.verdict=reviewed
file.554.path=skills/internal/analyze-artifacts/SKILL.md
file.554.verdict=reviewed
file.555.path=skills/internal/create-team/SKILL.md
file.555.verdict=skipped
file.555.reason=size-guard-focus-not-reviewed
file.556.path=skills/internal/create-team/scripts/dispatch.sh
file.556.verdict=skipped
file.556.reason=size-guard-focus-not-reviewed
file.557.path=skills/internal/review-feature-quality/SKILL.md
file.557.verdict=reviewed
file.558.path=skills/internal/review-sdd-process/SKILL.md
file.558.verdict=reviewed
file.559.path=skills/internal/run-agent/SKILL.md
file.559.verdict=reviewed
file.560.path=skills/internal/run-team/SKILL.md
file.560.verdict=reviewed
file.561.path=templates/commands/agents.md
file.561.verdict=skipped
file.561.reason=size-guard-focus-not-reviewed
file.562.path=templates/commands/team.md
file.562.verdict=skipped
file.562.reason=size-guard-focus-not-reviewed
file.563.path=templates/instructions-template.md
file.563.verdict=reviewed
file.564.path=tests/contract/test_decision_governance_contracts.py
file.564.verdict=reviewed
file.565.path=tests/contract/test_decision_governance_guards.py
file.565.verdict=reviewed
file.566.path=tests/contract/test_decision_governance_migration_map.py
file.566.verdict=reviewed
file.567.path=tests/contract/test_fast_fail_discipline.py
file.567.verdict=reviewed
file.568.path=tests/contract/test_non_regression_070.py
file.568.verdict=skipped
file.568.reason=size-guard-focus-not-reviewed
file.569.path=tests/contract/test_settlement_carriers.py
file.569.verdict=skipped
file.569.reason=size-guard-focus-not-reviewed
file.570.path=tests/contract/test_settlement_contract_definitions.py
file.570.verdict=skipped
file.570.reason=size-guard-focus-not-reviewed
file.571.path=tests/contract/test_settlement_engine.py
file.571.verdict=skipped
file.571.reason=size-guard-focus-not-reviewed
file.572.path=tests/contract/test_settlement_migration.py
file.572.verdict=skipped
file.572.reason=size-guard-focus-not-reviewed
file.573.path=tests/contract/test_settlement_preservation.py
file.573.verdict=skipped
file.573.reason=size-guard-focus-not-reviewed
file.574.path=tests/contract/test_settlement_scope.py
file.574.verdict=skipped
file.574.reason=size-guard-focus-not-reviewed
file.575.path=tests/fixtures/decision-governance/chain/.gitkeep
file.575.verdict=skipped
file.575.reason=non-code-file
file.576.path=tests/fixtures/decision-governance/chain/carriers/redecision-lossy.md
file.576.verdict=skipped
file.576.reason=non-code-file
file.577.path=tests/fixtures/decision-governance/chain/carriers/redecision.md
file.577.verdict=skipped
file.577.reason=non-code-file
file.578.path=tests/fixtures/decision-governance/chain/carriers/register.md
file.578.verdict=skipped
file.578.reason=non-code-file
file.579.path=tests/fixtures/decision-governance/chain/carriers/round-trip.md
file.579.verdict=skipped
file.579.reason=non-code-file
file.580.path=tests/fixtures/decision-governance/chain/green-complete.md
file.580.verdict=skipped
file.580.reason=non-code-file
file.581.path=tests/fixtures/decision-governance/chain/multi-hop-green.md
file.581.verdict=skipped
file.581.reason=non-code-file
file.582.path=tests/fixtures/decision-governance/chain/red-multi-hop-id.md
file.582.verdict=skipped
file.582.reason=non-code-file
file.583.path=tests/fixtures/decision-governance/chain/red-silent-redecision.md
file.583.verdict=skipped
file.583.reason=non-code-file
file.584.path=tests/fixtures/decision-governance/legacy/.gitkeep
file.584.verdict=skipped
file.584.reason=non-code-file
file.585.path=tests/fixtures/decision-governance/legacy/incomplete-new-form.md
file.585.verdict=skipped
file.585.reason=non-code-file
file.586.path=tests/fixtures/decision-governance/legacy/legacy.md
file.586.verdict=skipped
file.586.reason=non-code-file
file.587.path=tests/fixtures/decision-governance/legacy/register.md
file.587.verdict=skipped
file.587.reason=non-code-file
file.588.path=tests/fixtures/decision-governance/m01/.gitkeep
file.588.verdict=skipped
file.588.reason=non-code-file
file.589.path=tests/fixtures/decision-governance/m01/green-complete.md
file.589.verdict=skipped
file.589.reason=non-code-file
file.590.path=tests/fixtures/decision-governance/m01/green-tension-ref.md
file.590.verdict=skipped
file.590.reason=non-code-file
file.591.path=tests/fixtures/decision-governance/m01/red-class-outside.md
file.591.verdict=skipped
file.591.reason=non-code-file
file.592.path=tests/fixtures/decision-governance/m01/red-conditional-missing.md
file.592.verdict=skipped
file.592.reason=non-code-file
file.593.path=tests/fixtures/decision-governance/m01/red-malformed-timepoint.md
file.593.verdict=skipped
file.593.reason=non-code-file
file.594.path=tests/fixtures/decision-governance/m01/red-missing-actor.md
file.594.verdict=skipped
file.594.reason=non-code-file
file.595.path=tests/fixtures/decision-governance/m01/red-placeholder.md
file.595.verdict=skipped
file.595.reason=non-code-file
file.596.path=tests/fixtures/decision-governance/m01/red-tension-copy.md
file.596.verdict=skipped
file.596.reason=non-code-file
file.597.path=tests/fixtures/decision-governance/m01/red-timepoint-phase.md
file.597.verdict=skipped
file.597.reason=non-code-file
file.598.path=tests/fixtures/decision-governance/m02/.gitkeep
file.598.verdict=skipped
file.598.reason=non-code-file
file.599.path=tests/fixtures/decision-governance/m02/green-complete.md
file.599.verdict=skipped
file.599.reason=non-code-file
file.600.path=tests/fixtures/decision-governance/m02/red-empty-locator.md
file.600.verdict=skipped
file.600.reason=non-code-file
file.601.path=tests/fixtures/decision-governance/m02/red-single-dimension.md
file.601.verdict=skipped
file.601.reason=non-code-file
file.602.path=tests/fixtures/decision-governance/m03/.gitkeep
file.602.verdict=skipped
file.602.reason=non-code-file
file.603.path=tests/fixtures/decision-governance/m03/ai-replay-green.md
file.603.verdict=skipped
file.603.reason=non-code-file
file.604.path=tests/fixtures/decision-governance/m03/ai-replay-mismatch.md
file.604.verdict=skipped
file.604.reason=non-code-file
file.605.path=tests/fixtures/decision-governance/m03/green-complete.md
file.605.verdict=skipped
file.605.reason=non-code-file
file.606.path=tests/fixtures/decision-governance/m03/green-single-forced.md
file.606.verdict=skipped
file.606.reason=non-code-file
file.607.path=tests/fixtures/decision-governance/m03/red-chosen-not-member.md
file.607.verdict=skipped
file.607.reason=non-code-file
file.608.path=tests/fixtures/decision-governance/m03/red-count-mismatch.md
file.608.verdict=skipped
file.608.reason=non-code-file
file.609.path=tests/fixtures/decision-governance/m03/red-duplicate-label.md
file.609.verdict=skipped
file.609.reason=non-code-file
file.610.path=tests/fixtures/decision-governance/m03/red-empty-set.md
file.610.verdict=skipped
file.610.reason=non-code-file
file.611.path=tests/fixtures/decision-governance/m03/red-missing-evidence.md
file.611.verdict=skipped
file.611.reason=non-code-file
file.612.path=tests/fixtures/decision-governance/m03/red-missing-reversibility.md
file.612.verdict=skipped
file.612.reason=non-code-file
file.613.path=tests/fixtures/decision-governance/m03/red-other-without-path.md
file.613.verdict=skipped
file.613.reason=non-code-file
file.614.path=tests/fixtures/decision-governance/m03/red-single-without-forced.md
file.614.verdict=skipped
file.614.reason=non-code-file
file.615.path=tests/fixtures/decision-governance/m04/.gitkeep
file.615.verdict=skipped
file.615.reason=non-code-file
file.616.path=tests/fixtures/decision-governance/m04/green-dense.md
file.616.verdict=skipped
file.616.reason=non-code-file
file.617.path=tests/fixtures/decision-governance/m04/red-form.md
file.617.verdict=skipped
file.617.reason=non-code-file
file.618.path=tests/fixtures/decision-governance/m04/red-non-dense.md
file.618.verdict=skipped
file.618.reason=non-code-file
file.619.path=tests/fixtures/decision-governance/m04/red-unregistered.md
file.619.verdict=skipped
file.619.reason=non-code-file
file.620.path=tests/fixtures/decision-governance/m04/register-missing.md
file.620.verdict=skipped
file.620.reason=non-code-file
file.621.path=tests/fixtures/decision-governance/m04/register.md
file.621.verdict=skipped
file.621.reason=non-code-file
file.622.path=tests/fixtures/decision-governance/m05/.gitkeep
file.622.verdict=skipped
file.622.reason=non-code-file
file.623.path=tests/fixtures/decision-governance/m05/red-no-id.md
file.623.verdict=skipped
file.623.reason=non-code-file
file.624.path=tests/fixtures/decision-governance/m05/red-no-receipt.md
file.624.verdict=skipped
file.624.reason=non-code-file
file.625.path=tests/fixtures/decision-governance/m05/red-unresolvable.md
file.625.verdict=skipped
file.625.reason=non-code-file
file.626.path=tests/fixtures/decision-governance/m06/.gitkeep
file.626.verdict=skipped
file.626.reason=non-code-file
file.627.path=tests/fixtures/decision-governance/m06/red-missing-archive.md
file.627.verdict=skipped
file.627.reason=non-code-file
file.628.path=tests/fixtures/decision-governance/m06/red-missing-chosen.md
file.628.verdict=skipped
file.628.reason=non-code-file
file.629.path=tests/fixtures/decision-governance/m06/red-missing-class.md
file.629.verdict=skipped
file.629.reason=non-code-file
file.630.path=tests/fixtures/decision-governance/m06/red-missing-constraints.md
file.630.verdict=skipped
file.630.reason=non-code-file
file.631.path=tests/fixtures/decision-governance/m06/red-missing-id.md
file.631.verdict=skipped
file.631.reason=non-code-file
file.632.path=tests/fixtures/decision-governance/m06/red-no-block.md
file.632.verdict=skipped
file.632.reason=non-code-file
file.633.path=tests/fixtures/decision-governance/m07/.gitkeep
file.633.verdict=skipped
file.633.reason=non-code-file
file.634.path=tests/fixtures/decision-governance/m07/red-inconsistent-id.md
file.634.verdict=skipped
file.634.reason=non-code-file
file.635.path=tests/fixtures/decision-governance/m07/red-missing-dispatch.md
file.635.verdict=skipped
file.635.reason=non-code-file
file.636.path=tests/fixtures/decision-governance/m07/red-missing-receipt.md
file.636.verdict=skipped
file.636.reason=non-code-file
file.637.path=tests/fixtures/decision-governance/m07/red-missing-record.md
file.637.verdict=skipped
file.637.reason=non-code-file
file.638.path=tests/fixtures/decision-governance/m08/.gitkeep
file.638.verdict=skipped
file.638.reason=non-code-file
file.639.path=tests/fixtures/decision-governance/m08/glossary.md
file.639.verdict=skipped
file.639.reason=non-code-file
file.640.path=tests/fixtures/decision-governance/m08/green-full-name.md
file.640.verdict=skipped
file.640.reason=non-code-file
file.641.path=tests/fixtures/decision-governance/m08/green-unregistered.md
file.641.verdict=skipped
file.641.reason=non-code-file
file.642.path=tests/fixtures/decision-governance/m08/red-variant.md
file.642.verdict=skipped
file.642.reason=non-code-file
file.643.path=tests/fixtures/decision-governance/m09/.gitkeep
file.643.verdict=skipped
file.643.reason=non-code-file
file.644.path=tests/fixtures/decision-governance/m09/green-resolvable.md
file.644.verdict=skipped
file.644.reason=non-code-file
file.645.path=tests/fixtures/decision-governance/m09/red-broken-anchor.md
file.645.verdict=skipped
file.645.reason=non-code-file
file.646.path=tests/fixtures/decision-governance/m09/red-broken.md
file.646.verdict=skipped
file.646.reason=non-code-file
file.647.path=tests/fixtures/decision-governance/payload/.gitkeep
file.647.verdict=skipped
file.647.reason=non-code-file
file.648.path=tests/fixtures/decision-governance/payload/complete.md
file.648.verdict=skipped
file.648.reason=non-code-file
file.649.path=tests/fixtures/decision-governance/payload/non-decision.md
file.649.verdict=skipped
file.649.reason=non-code-file
file.650.path=tests/fixtures/decision-governance/payload/returns/return-acknowledged.md
file.650.verdict=skipped
file.650.reason=non-code-file
file.651.path=tests/fixtures/decision-governance/payload/returns/return-escalated.md
file.651.verdict=skipped
file.651.reason=non-code-file
file.652.path=tests/fixtures/decision-governance/reconstruct/.gitkeep
file.652.verdict=skipped
file.652.reason=non-code-file
file.653.path=tests/fixtures/decision-governance/reconstruct/checkpoints/02-implement.md
file.653.verdict=skipped
file.653.reason=non-code-file
file.654.path=tests/fixtures/decision-governance/reconstruct/plan.md
file.654.verdict=skipped
file.654.reason=non-code-file
file.655.path=tests/fixtures/decision-governance/reconstruct/register.md
file.655.verdict=skipped
file.655.reason=non-code-file
file.656.path=tests/fixtures/decision-governance/reconstruct/requirements.md
file.656.verdict=skipped
file.656.reason=non-code-file
file.657.path=tests/fixtures/decision-governance/reconstruct/run-report.md
file.657.verdict=skipped
file.657.reason=non-code-file
file.658.path=tests/fixtures/settlement/builders.py
file.658.verdict=skipped
file.658.reason=size-guard-focus-not-reviewed
file.659.path=tests/fixtures/settlement/c1-state/demo-line.md
file.659.verdict=skipped
file.659.reason=size-guard-focus-not-reviewed
file.660.path=tests/fixtures/settlement/c1-state/heartbeat-demo-line-implement.log
file.660.verdict=skipped
file.660.reason=size-guard-focus-not-reviewed
file.661.path=tests/fixtures/settlement/c1-state/log-demo-line-implement.log
file.661.verdict=skipped
file.661.reason=size-guard-focus-not-reviewed
file.662.path=tests/fixtures/settlement/c1-state/pid-demo-line-implement
file.662.verdict=skipped
file.662.reason=size-guard-focus-not-reviewed
file.663.path=tests/fixtures/settlement/c1-state/prompt-demo-line-implement.md.meta.json
file.663.verdict=skipped
file.663.reason=size-guard-focus-not-reviewed
file.664.path=tests/fixtures/settlement/c1-state/status-demo-line-implement
file.664.verdict=skipped
file.664.reason=size-guard-focus-not-reviewed
file.665.path=tests/fixtures/settlement/c3-report/logs/seat-legacy.attempt
file.665.verdict=skipped
file.665.reason=size-guard-focus-not-reviewed
file.666.path=tests/fixtures/settlement/c3-report/logs/seat-missing-start.return.txt
file.666.verdict=skipped
file.666.reason=size-guard-focus-not-reviewed
file.667.path=tests/fixtures/settlement/c3-report/logs/seat-ok.attempt
file.667.verdict=skipped
file.667.reason=size-guard-focus-not-reviewed
file.668.path=tests/fixtures/settlement/c3-report/logs/seat-ok.return.txt
file.668.verdict=skipped
file.668.reason=size-guard-focus-not-reviewed
file.669.path=tests/fixtures/settlement/c3-report/teams/demo-team/runs/20261120T000000Z-report.md
file.669.verdict=skipped
file.669.reason=size-guard-focus-not-reviewed
file.670.path=tests/fixtures/settlement/c3-report/teams/legacy-team/runs/20261119T000000Z-report.md
file.670.verdict=skipped
file.670.reason=size-guard-focus-not-reviewed
file.671.path=tests/fixtures/settlement/legacy/logs/legacy-run.attempt
file.671.verdict=skipped
file.671.reason=size-guard-focus-not-reviewed
file.672.path=tests/fixtures/settlement/legacy/logs/legacy-run.end
file.672.verdict=skipped
file.672.reason=size-guard-focus-not-reviewed
file.673.path=tests/fixtures/settlement/legacy/logs/legacy-run.live.log
file.673.verdict=skipped
file.673.reason=size-guard-focus-not-reviewed
file.674.path=tests/fixtures/settlement/legacy/logs/legacy-run.return.txt
file.674.verdict=skipped
file.674.reason=size-guard-focus-not-reviewed
file.675.path=tests/fixtures/settlement/legacy/logs/legacy-run.settlement
file.675.verdict=skipped
file.675.reason=size-guard-focus-not-reviewed
file.676.path=tests/fixtures/settlement/legacy/logs/legacy-run.status
file.676.verdict=skipped
file.676.reason=size-guard-focus-not-reviewed
file.677.path=tests/fixtures/settlement/versioned/logs/versioned-run.attempt
file.677.verdict=skipped
file.677.reason=size-guard-focus-not-reviewed
file.678.path=tests/fixtures/settlement/versioned/logs/versioned-run.end
file.678.verdict=skipped
file.678.reason=size-guard-focus-not-reviewed
file.679.path=tests/fixtures/settlement/versioned/logs/versioned-run.live.log
file.679.verdict=skipped
file.679.reason=size-guard-focus-not-reviewed
file.680.path=tests/fixtures/settlement/versioned/logs/versioned-run.return.txt
file.680.verdict=skipped
file.680.reason=size-guard-focus-not-reviewed
file.681.path=tests/fixtures/settlement/versioned/logs/versioned-run.settlement
file.681.verdict=skipped
file.681.reason=size-guard-focus-not-reviewed
file.682.path=tests/fixtures/settlement/versioned/logs/versioned-run.status
file.682.verdict=skipped
file.682.reason=size-guard-focus-not-reviewed
file.683.path=tests/integration/test_decision_governance_migrate_dryrun.py
file.683.verdict=reviewed
file.684.path=tests/unit/test_validate_decisions.py
file.684.verdict=reviewed
<!-- coverage-receipt:end -->
