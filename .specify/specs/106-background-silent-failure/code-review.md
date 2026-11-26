# Code Review Report — 代码段 (code segment)

| 属性 | 值 |
|------|-----|
| **分支** | `106-background-silent-failure` |
| **基准** | `fbab7a45c4a57b596bc32437181ee9eb799ebe60` (`fbab7a45c`) |
| **目标** | `0a01f797a9f52d446c9069b029afda8ab8f65ea9` (`0a01f797a`) |
| **基准来源** | `feature-first-commit` |
| **渲染模式** | `renderer: text` |
| **Reviewer** | `Qiming Liu (John)` |
| **日期** | `2026-11-26T03:30:46Z` |

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
 .specify/agents/.render-manifest.json              |   12 +-
 .../templates/sdd-implement-coordinator.agent.md   |    1 +
 .../agents/templates/sdd-plan-coordinator.agent.md |    1 +
 .../templates/sdd-review-coordinator.agent.md      |    1 +
 .../agents/templates/sdd-task-coordinator.agent.md |    1 +
 .../106-background-silent-failure/anchor.md        |   26 +
 .../records/20261125T114538658383Z-0904f023.json   |    1 +
 .../records/20261125T115451874927Z-6db027b5.json   |    1 +
 .../records/20261125T121419791413Z-a4679bfb.json   |    1 +
 .../records/20261125T122810951835Z-56d6e538.json   |    1 +
 .../records/20261125T123555820029Z-80b8b9aa.json   |    1 +
 .../records/20261125T125153331787Z-46e5ff70.json   |    1 +
 .../records/20261125T125926616815Z-eb0837fb.json   |    1 +
 .../records/20261125T132404451045Z-ffd93788.json   |    1 +
 .../records/20261125T134020382137Z-dc4a1b7c.json   |    1 +
 .../records/20261125T173956791454Z-2e94960a.json   |    1 +
 .../records/20261126T032247826756Z-33524863.json   |    1 +
 .specify/features.md                               |    5 +-
 .specify/features/095-superagent-role.md           |   20 +-
 .../20261125T114609Z-speckit-requirements.md       |   22 +
 .../feedback/20261125T115512Z-speckit-clarify.md   |   23 +
 .specify/feedback/20261125T121425Z-speckit-plan.md |   23 +
 .../feedback/20261125T122816Z-speckit-tasks.md     |   22 +
 .../feedback/20261125T123559Z-speckit-checklist.md |   21 +
 .../20261125T125200Z-skill-analyze-artifacts.md    |   21 +
 .../20261125T125926Z-skill-analyze-artifacts.md    |   19 +
 .../20261125T132404Z-skill-analyze-artifacts.md    |   19 +
 .../20261125T134023Z-skill-analyze-artifacts.md    |   20 +
 .../20261125T174002Z-skill-analyze-artifacts.md    |   23 +
 .../20261126T032257Z-skill-implement-feature.md    |   22 +
 .specify/glossary.md                               |    1 +
 ...Z-106-background-silent-failure-requirements.md |   31 +
 ...15521Z-106-background-silent-failure-clarify.md |   31 +
 ...106-background-silent-failure-clarify-repair.md |   33 +
 ...5T121502Z-106-background-silent-failure-plan.md |   34 +
 ...T122912Z-106-background-silent-failure-tasks.md |   36 +
 ...605Z-106-background-silent-failure-checklist.md |   36 +
 ...25221Z-106-background-silent-failure-analyze.md |   56 +
 ...106-background-silent-failure-analyze-repair.md |   57 +
 ...06-background-silent-failure-analyze-repair2.md |   58 +
 ...315Z-106-background-silent-failure-implement.md |   33 +
 .specify/scripts/python/role-edge-check.py         |  990 ++-
 ...ation-speckit-clarify-r20261124t054500z-9b2d.md |   10 +-
 ...n-speckit-requirements-r20261125t022857z-06d.md |   10 +-
 ...on-skill-implement-feature-r20261125t022857z.md |   10 +-
 ...n-speckit-requirements-r20261125t113505z-106.md |  204 +
 ...ation-speckit-clarify-r20261125t113505z-106a.md |  204 +
 ...mination-speckit-plan-r20261125t113505z-106a.md |  202 +
 ...ination-speckit-tasks-r20261125t113505z-106a.md |  207 +
 ...ion-speckit-checklist-r20261125t113505z-106a.md |  202 +
 ...on-skill-analyze-artifacts-r20261125t113505z.md |  207 +
 ...on-skill-analyze-artifacts-r20261125t125827z.md |  208 +
 ...on-skill-analyze-artifacts-r20261125t132316z.md |  204 +
 ...on-skill-analyze-artifacts-r20261125t134017z.md |  204 +
 ...on-skill-analyze-artifacts-r20261125t173750z.md |  203 +
 ...on-skill-implement-feature-r20261125t113505z.md |  219 +
 .../shared/definitions/subagent-definitions.md     |    2 +
 .../shared/definitions/superagent-definitions.md   |   85 +-
 .../shared/workflow/external-dispatch-recipes.md   |    8 +-
 .specify/skills/internal/create-team/SKILL.md      |    6 +-
 .../internal/create-team/scripts/dispatch.sh       |  103 +-
 .specify/skills/internal/run-agent/SKILL.md        |   33 +
 .specify/skills/internal/run-team/SKILL.md         |    1 +
 .specify/skills/sdd-loop-driver/SKILL.md           |    1 +
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
 .../contracts/carrier-conformance.contract.md      |   54 +
 .../enforcement-and-migration.contract.md          |   46 +
 .../contracts/settlement-contract.contract.md      |   56 +
 .../coverage-baseline.txt                          |  787 +++
 .../106-background-silent-failure/data-model.md    |  163 +
 .../106-background-silent-failure/feature-ref.md   |  102 +
 .../specs/106-background-silent-failure/handoff.md |   54 +
 .../notes/pre-change-measurements.md               |   86 +
 .../notes/quickstart-run.md                        |  194 +
 .../notes/red-first-evidence.md                    |  437 ++
 .../specs/106-background-silent-failure/plan.md    |  217 +
 .../106-background-silent-failure/quickstart.md    |  171 +
 .../106-background-silent-failure/requirements.md  |  311 +
 .../106-background-silent-failure/research.md      |   33 +
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
 .../teams/106-background-silent-failure/team.md    |  183 +
 agents/sdd-implement-coordinator.agent.md          |    1 +
 agents/sdd-plan-coordinator.agent.md               |    1 +
 agents/sdd-review-coordinator.agent.md             |    1 +
 agents/sdd-task-coordinator.agent.md               |    1 +
 docs/reference/commands/agents.md                  |    9 +
 docs/reference/skills/sdd-loop-driver.md           |   10 +
 docs/reference/teams/orchestration.md              |   11 +
 scripts/python/role-edge-check.py                  |  990 ++-
 shared/definitions/subagent-definitions.md         |    2 +
 shared/definitions/superagent-definitions.md       |   85 +-
 shared/workflow/external-dispatch-recipes.md       |    8 +-
 skills/external/sdd-loop-driver/SKILL.md           |    1 +
 skills/internal/create-team/SKILL.md               |    6 +-
 skills/internal/create-team/scripts/dispatch.sh    |  103 +-
 skills/internal/run-agent/SKILL.md                 |   33 +
 skills/internal/run-team/SKILL.md                  |    1 +
 templates/commands/agents.md                       |    2 +
 templates/commands/team.md                         |    2 +
 tests/contract/test_settlement_carriers.py         |  887 +++
 .../test_settlement_contract_definitions.py        |  481 ++
 tests/contract/test_settlement_engine.py           |  614 ++
 tests/contract/test_settlement_migration.py        |  363 +
 tests/contract/test_settlement_preservation.py     |  305 +
 tests/contract/test_settlement_scope.py            |  293 +
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
 331 files changed, 34432 insertions(+), 80 deletions(-)
```

---

## Review 意见


### 🟠 [IMPORTANT] scripts/python/role-edge-check.py (Line 1672)

> The --live-window option is declared (C-25) and echoed into inputs.live_window_s, but _derive_settlement (line 1514) never receives it: the owner's 'running' evidence row names 'a live log growing inside the --live-window window' (superagent-definitions.md line 74) and FR-005 lists the live-log window as one re-checked liveness leg, yet liveness today rests only on pid liveness or the open return channel. Operator answers: agree the option is inert; NOT blocking for this feature because FR-005's one-of liveness rule is satisfied by the pid leg and no requirement makes the window mandatory — implement the live-log-growth leg or drop the option in a follow-up.

<sub>11:31:53</sub>


### 🟠 [IMPORTANT] skills/internal/create-team/scripts/dispatch.sh (Line 211)

> The TERM/INT/HUP trap writes .end and .status and exits, but the async pipeline subshell (and the CLI it runs) is not signalled: the recorded .end exit=143 / signal=TERM describes the wrapper only, while the child can outlive it and keep appending to .live.log. The settlement value stays evidence-derived (failed from the signal terminal, honest), so this is not blocking; answer: agree it needs a follow-up — signal the pipeline's process group in the trap (or document the orphan) so the terminal record does not read as 'the work ended'.

<sub>11:31:53</sub>


### 🟢 [SUGGESTION] scripts/python/role-edge-check.py (Line 1645)

> silent-end evidence bundles append 'lack' pointers for <label>.end and <label>.status for every carrier; on C1/C3/C4 attempts those file names are never part of the carrier's artifact set, so the bundle points a reader at log-dir paths that were never expected. Scope the lack pointers to C2 or name the carrier-specific absent records.

<sub>11:31:53</sub>


### ⚪ [NITPICK] scripts/python/role-edge-check.py (Line 1337)

> The C1 status file's sentinel token is parsed into the terminal entry (line 1353) but never consulted by _derive_settlement; either use it in the derived detail or drop the parse so the field does not imply participation it does not have.

<sub>11:31:53</sub>


### 👍 [PRAISE] tests/contract/test_settlement_preservation.py (Line 253)

> Report/query byte-equality against a recorded fbab7a45c baseline plus the AST-level read-only/destructive-authority pins in test_settlement_scope.py are exactly the guards C-25/C-29 needed; the preserved surface is measured, not asserted.

<sub>11:31:53</sub>


### 👍 [PRAISE] tests/contract/test_settlement_carriers.py (Line 345)

> The C2 silent-death fixture drives the shipped dispatch.sh, SIGKILLs the real wrapper and polls for pid disappearance — the silent failure is proven on the real carrier, not on a mock; process-group cleanup is explicit.

<sub>11:31:53</sub>




> **未提交范围（未评审）**: 1 个未提交路径未计入本次评审对象（.specify/specs/106-background-silent-failure/verification.md）；本回执不对该范围给出任何结论。

<!-- coverage-receipt:begin -->
receipt_version=1
base=fbab7a45c4a57b596bc32437181ee9eb799ebe60
head=0a01f797a9f52d446c9069b029afda8ab8f65ea9
base_source=feature-first-commit
renderer=text
changed_files=331
judged_files=49
skipped_files=282
gap_files=0
lines_added=4809
lines_deleted=27
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
file.020.path=.specify/exec-quant/records/20261125T114538658383Z-0904f023.json
file.020.verdict=skipped
file.020.reason=non-code-file
file.021.path=.specify/exec-quant/records/20261125T115451874927Z-6db027b5.json
file.021.verdict=skipped
file.021.reason=non-code-file
file.022.path=.specify/exec-quant/records/20261125T121419791413Z-a4679bfb.json
file.022.verdict=skipped
file.022.reason=non-code-file
file.023.path=.specify/exec-quant/records/20261125T122810951835Z-56d6e538.json
file.023.verdict=skipped
file.023.reason=non-code-file
file.024.path=.specify/exec-quant/records/20261125T123555820029Z-80b8b9aa.json
file.024.verdict=skipped
file.024.reason=non-code-file
file.025.path=.specify/exec-quant/records/20261125T125153331787Z-46e5ff70.json
file.025.verdict=skipped
file.025.reason=non-code-file
file.026.path=.specify/exec-quant/records/20261125T125926616815Z-eb0837fb.json
file.026.verdict=skipped
file.026.reason=non-code-file
file.027.path=.specify/exec-quant/records/20261125T132404451045Z-ffd93788.json
file.027.verdict=skipped
file.027.reason=non-code-file
file.028.path=.specify/exec-quant/records/20261125T134020382137Z-dc4a1b7c.json
file.028.verdict=skipped
file.028.reason=non-code-file
file.029.path=.specify/exec-quant/records/20261125T173956791454Z-2e94960a.json
file.029.verdict=skipped
file.029.reason=non-code-file
file.030.path=.specify/exec-quant/records/20261126T032247826756Z-33524863.json
file.030.verdict=skipped
file.030.reason=non-code-file
file.031.path=.specify/features.md
file.031.verdict=skipped
file.031.reason=non-code-file
file.032.path=.specify/features/095-superagent-role.md
file.032.verdict=skipped
file.032.reason=non-code-file
file.033.path=.specify/feedback/20261125T114609Z-speckit-requirements.md
file.033.verdict=skipped
file.033.reason=non-code-file
file.034.path=.specify/feedback/20261125T115512Z-speckit-clarify.md
file.034.verdict=skipped
file.034.reason=non-code-file
file.035.path=.specify/feedback/20261125T121425Z-speckit-plan.md
file.035.verdict=skipped
file.035.reason=non-code-file
file.036.path=.specify/feedback/20261125T122816Z-speckit-tasks.md
file.036.verdict=skipped
file.036.reason=non-code-file
file.037.path=.specify/feedback/20261125T123559Z-speckit-checklist.md
file.037.verdict=skipped
file.037.reason=non-code-file
file.038.path=.specify/feedback/20261125T125200Z-skill-analyze-artifacts.md
file.038.verdict=skipped
file.038.reason=non-code-file
file.039.path=.specify/feedback/20261125T125926Z-skill-analyze-artifacts.md
file.039.verdict=skipped
file.039.reason=non-code-file
file.040.path=.specify/feedback/20261125T132404Z-skill-analyze-artifacts.md
file.040.verdict=skipped
file.040.reason=non-code-file
file.041.path=.specify/feedback/20261125T134023Z-skill-analyze-artifacts.md
file.041.verdict=skipped
file.041.reason=non-code-file
file.042.path=.specify/feedback/20261125T174002Z-skill-analyze-artifacts.md
file.042.verdict=skipped
file.042.reason=non-code-file
file.043.path=.specify/feedback/20261126T032257Z-skill-implement-feature.md
file.043.verdict=skipped
file.043.reason=non-code-file
file.044.path=.specify/glossary.md
file.044.verdict=skipped
file.044.reason=non-code-file
file.045.path=.specify/retention/closeout/20261125T114628Z-106-background-silent-failure-requirements.md
file.045.verdict=skipped
file.045.reason=non-code-file
file.046.path=.specify/retention/closeout/20261125T115521Z-106-background-silent-failure-clarify.md
file.046.verdict=skipped
file.046.reason=non-code-file
file.047.path=.specify/retention/closeout/20261125T115846Z-106-background-silent-failure-clarify-repair.md
file.047.verdict=skipped
file.047.reason=non-code-file
file.048.path=.specify/retention/closeout/20261125T121502Z-106-background-silent-failure-plan.md
file.048.verdict=skipped
file.048.reason=non-code-file
file.049.path=.specify/retention/closeout/20261125T122912Z-106-background-silent-failure-tasks.md
file.049.verdict=skipped
file.049.reason=non-code-file
file.050.path=.specify/retention/closeout/20261125T123605Z-106-background-silent-failure-checklist.md
file.050.verdict=skipped
file.050.reason=non-code-file
file.051.path=.specify/retention/closeout/20261125T125221Z-106-background-silent-failure-analyze.md
file.051.verdict=skipped
file.051.reason=non-code-file
file.052.path=.specify/retention/closeout/20261125T130200Z-106-background-silent-failure-analyze-repair.md
file.052.verdict=skipped
file.052.reason=non-code-file
file.053.path=.specify/retention/closeout/20261125T132427Z-106-background-silent-failure-analyze-repair2.md
file.053.verdict=skipped
file.053.reason=non-code-file
file.054.path=.specify/retention/closeout/20261126T032315Z-106-background-silent-failure-implement.md
file.054.verdict=skipped
file.054.reason=non-code-file
file.055.path=.specify/scripts/python/role-edge-check.py
file.055.verdict=skipped
file.055.reason=generated
file.056.path=.specify/session/20261124T055708Z-run-determination-speckit-clarify-r20261124t054500z-9b2d.md
file.056.verdict=skipped
file.056.reason=non-code-file
file.057.path=.specify/session/20261125T024118Z-run-determination-speckit-requirements-r20261125t022857z-06d.md
file.057.verdict=skipped
file.057.reason=non-code-file
file.058.path=.specify/session/20261125T055144Z-run-determination-skill-implement-feature-r20261125t022857z.md
file.058.verdict=skipped
file.058.reason=non-code-file
file.059.path=.specify/session/20261125T114533Z-run-determination-speckit-requirements-r20261125t113505z-106.md
file.059.verdict=skipped
file.059.reason=non-code-file
file.060.path=.specify/session/20261125T115445Z-run-determination-speckit-clarify-r20261125t113505z-106a.md
file.060.verdict=skipped
file.060.reason=non-code-file
file.061.path=.specify/session/20261125T121417Z-run-determination-speckit-plan-r20261125t113505z-106a.md
file.061.verdict=skipped
file.061.reason=non-code-file
file.062.path=.specify/session/20261125T122808Z-run-determination-speckit-tasks-r20261125t113505z-106a.md
file.062.verdict=skipped
file.062.reason=non-code-file
file.063.path=.specify/session/20261125T123550Z-run-determination-speckit-checklist-r20261125t113505z-106a.md
file.063.verdict=skipped
file.063.reason=non-code-file
file.064.path=.specify/session/20261125T125150Z-run-determination-skill-analyze-artifacts-r20261125t113505z.md
file.064.verdict=skipped
file.064.reason=non-code-file
file.065.path=.specify/session/20261125T125920Z-run-determination-skill-analyze-artifacts-r20261125t125827z.md
file.065.verdict=skipped
file.065.reason=non-code-file
file.066.path=.specify/session/20261125T132358Z-run-determination-skill-analyze-artifacts-r20261125t132316z.md
file.066.verdict=skipped
file.066.reason=non-code-file
file.067.path=.specify/session/20261125T134017Z-run-determination-skill-analyze-artifacts-r20261125t134017z.md
file.067.verdict=skipped
file.067.reason=non-code-file
file.068.path=.specify/session/20261125T173937Z-run-determination-skill-analyze-artifacts-r20261125t173750z.md
file.068.verdict=skipped
file.068.reason=non-code-file
file.069.path=.specify/session/20261126T032240Z-run-determination-skill-implement-feature-r20261125t113505z.md
file.069.verdict=skipped
file.069.reason=non-code-file
file.070.path=.specify/shared/definitions/subagent-definitions.md
file.070.verdict=skipped
file.070.reason=generated
file.071.path=.specify/shared/definitions/superagent-definitions.md
file.071.verdict=skipped
file.071.reason=generated
file.072.path=.specify/shared/workflow/external-dispatch-recipes.md
file.072.verdict=skipped
file.072.reason=generated
file.073.path=.specify/skills/internal/create-team/SKILL.md
file.073.verdict=skipped
file.073.reason=generated
file.074.path=.specify/skills/internal/create-team/scripts/dispatch.sh
file.074.verdict=skipped
file.074.reason=generated
file.075.path=.specify/skills/internal/run-agent/SKILL.md
file.075.verdict=skipped
file.075.reason=generated
file.076.path=.specify/skills/internal/run-team/SKILL.md
file.076.verdict=skipped
file.076.reason=generated
file.077.path=.specify/skills/sdd-loop-driver/SKILL.md
file.077.verdict=skipped
file.077.reason=generated
file.078.path=.specify/specs/106-background-silent-failure/baseline-failed.txt
file.078.verdict=skipped
file.078.reason=non-code-file
file.079.path=.specify/specs/106-background-silent-failure/checklists/background-settlement-2026-11-25.md
file.079.verdict=skipped
file.079.reason=non-code-file
file.080.path=.specify/specs/106-background-silent-failure/checklists/requirements.md
file.080.verdict=skipped
file.080.reason=non-code-file
file.081.path=.specify/specs/106-background-silent-failure/checkpoints/01-requirements.md
file.081.verdict=skipped
file.081.reason=non-code-file
file.082.path=.specify/specs/106-background-silent-failure/checkpoints/02-clarify.md
file.082.verdict=skipped
file.082.reason=non-code-file
file.083.path=.specify/specs/106-background-silent-failure/checkpoints/03-plan.md
file.083.verdict=skipped
file.083.reason=non-code-file
file.084.path=.specify/specs/106-background-silent-failure/checkpoints/04-tasks.md
file.084.verdict=skipped
file.084.reason=non-code-file
file.085.path=.specify/specs/106-background-silent-failure/checkpoints/05-goal-team-activation.md
file.085.verdict=skipped
file.085.reason=non-code-file
file.086.path=.specify/specs/106-background-silent-failure/checkpoints/06-checklist.md
file.086.verdict=skipped
file.086.reason=non-code-file
file.087.path=.specify/specs/106-background-silent-failure/checkpoints/07-analyze.md
file.087.verdict=skipped
file.087.reason=non-code-file
file.088.path=.specify/specs/106-background-silent-failure/checkpoints/08-implement.md
file.088.verdict=skipped
file.088.reason=non-code-file
file.089.path=.specify/specs/106-background-silent-failure/contracts/carrier-conformance.contract.md
file.089.verdict=skipped
file.089.reason=non-code-file
file.090.path=.specify/specs/106-background-silent-failure/contracts/enforcement-and-migration.contract.md
file.090.verdict=skipped
file.090.reason=non-code-file
file.091.path=.specify/specs/106-background-silent-failure/contracts/settlement-contract.contract.md
file.091.verdict=skipped
file.091.reason=non-code-file
file.092.path=.specify/specs/106-background-silent-failure/coverage-baseline.txt
file.092.verdict=skipped
file.092.reason=non-code-file
file.093.path=.specify/specs/106-background-silent-failure/data-model.md
file.093.verdict=skipped
file.093.reason=non-code-file
file.094.path=.specify/specs/106-background-silent-failure/feature-ref.md
file.094.verdict=skipped
file.094.reason=non-code-file
file.095.path=.specify/specs/106-background-silent-failure/handoff.md
file.095.verdict=skipped
file.095.reason=non-code-file
file.096.path=.specify/specs/106-background-silent-failure/notes/pre-change-measurements.md
file.096.verdict=skipped
file.096.reason=non-code-file
file.097.path=.specify/specs/106-background-silent-failure/notes/quickstart-run.md
file.097.verdict=skipped
file.097.reason=non-code-file
file.098.path=.specify/specs/106-background-silent-failure/notes/red-first-evidence.md
file.098.verdict=skipped
file.098.reason=non-code-file
file.099.path=.specify/specs/106-background-silent-failure/plan.md
file.099.verdict=skipped
file.099.reason=non-code-file
file.100.path=.specify/specs/106-background-silent-failure/quickstart.md
file.100.verdict=skipped
file.100.reason=non-code-file
file.101.path=.specify/specs/106-background-silent-failure/requirements.md
file.101.verdict=skipped
file.101.reason=non-code-file
file.102.path=.specify/specs/106-background-silent-failure/research.md
file.102.verdict=skipped
file.102.reason=non-code-file
file.103.path=.specify/specs/106-background-silent-failure/tasks.md
file.103.verdict=skipped
file.103.reason=non-code-file
file.104.path=.specify/specs/106-background-silent-failure/test-evidence/acceptance-106.md
file.104.verdict=skipped
file.104.reason=non-code-file
file.105.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-domain-w1-r2.jsonl
file.105.verdict=skipped
file.105.reason=non-code-file
file.106.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-domain-w1-r3.jsonl
file.106.verdict=skipped
file.106.reason=non-code-file
file.107.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-domain-w1.jsonl
file.107.verdict=skipped
file.107.reason=non-code-file
file.108.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-domain-w2.jsonl
file.108.verdict=skipped
file.108.reason=non-code-file
file.109.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-domain-w2a-r2.jsonl
file.109.verdict=skipped
file.109.reason=non-code-file
file.110.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-domain-w2a-r3.jsonl
file.110.verdict=skipped
file.110.reason=non-code-file
file.111.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-domain-w2b-r2.jsonl
file.111.verdict=skipped
file.111.reason=non-code-file
file.112.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-domain-w2b-r3.jsonl
file.112.verdict=skipped
file.112.reason=non-code-file
file.113.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-domain-w2c-r2.jsonl
file.113.verdict=skipped
file.113.reason=non-code-file
file.114.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-domain-w2c-r3.jsonl
file.114.verdict=skipped
file.114.reason=non-code-file
file.115.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-domain-w3-r2.jsonl
file.115.verdict=skipped
file.115.reason=non-code-file
file.116.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-domain-w3-r3.jsonl
file.116.verdict=skipped
file.116.reason=non-code-file
file.117.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-domain-w3.jsonl
file.117.verdict=skipped
file.117.reason=non-code-file
file.118.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-incremental-r4.jsonl
file.118.verdict=skipped
file.118.reason=non-code-file
file.119.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-incremental-r5.jsonl
file.119.verdict=skipped
file.119.reason=non-code-file
file.120.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-r4-reused-domain-hashes.txt
file.120.verdict=skipped
file.120.reason=non-code-file
file.121.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair-2026-11-25.md
file.121.verdict=skipped
file.121.reason=non-code-file
file.122.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair-clause-coverage.txt
file.122.verdict=skipped
file.122.reason=non-code-file
file.123.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair-clause-extract.json
file.123.verdict=skipped
file.123.reason=non-code-file
file.124.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair-decomposition.txt
file.124.verdict=skipped
file.124.reason=non-code-file
file.125.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair-gate-scan.json
file.125.verdict=skipped
file.125.reason=non-code-file
file.126.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair-glossary-validate.txt
file.126.verdict=skipped
file.126.reason=non-code-file
file.127.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair-pre-analyze-plan.txt
file.127.verdict=skipped
file.127.reason=non-code-file
file.128.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair-pre-analyze-requirements.txt
file.128.verdict=skipped
file.128.reason=non-code-file
file.129.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair-pre-analyze-tasks.txt
file.129.verdict=skipped
file.129.reason=non-code-file
file.130.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair-requirements-validator.txt
file.130.verdict=skipped
file.130.reason=non-code-file
file.131.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair-tasks-validator.txt
file.131.verdict=skipped
file.131.reason=non-code-file
file.132.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair2-2026-11-25.md
file.132.verdict=skipped
file.132.reason=non-code-file
file.133.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair2-clause-coverage.txt
file.133.verdict=skipped
file.133.reason=non-code-file
file.134.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair2-clause-extract.json
file.134.verdict=skipped
file.134.reason=non-code-file
file.135.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair2-decomposition.txt
file.135.verdict=skipped
file.135.reason=non-code-file
file.136.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair2-gate-scan.json
file.136.verdict=skipped
file.136.reason=non-code-file
file.137.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair2-glossary-validate.txt
file.137.verdict=skipped
file.137.reason=non-code-file
file.138.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair2-pre-analyze-plan.txt
file.138.verdict=skipped
file.138.reason=non-code-file
file.139.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair2-pre-analyze-requirements.txt
file.139.verdict=skipped
file.139.reason=non-code-file
file.140.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair2-pre-analyze-tasks.txt
file.140.verdict=skipped
file.140.reason=non-code-file
file.141.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair2-requirements-validator.txt
file.141.verdict=skipped
file.141.reason=non-code-file
file.142.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair2-tasks-validator.txt
file.142.verdict=skipped
file.142.reason=non-code-file
file.143.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair3-2026-11-25.md
file.143.verdict=skipped
file.143.reason=non-code-file
file.144.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair3-clause-coverage.txt
file.144.verdict=skipped
file.144.reason=non-code-file
file.145.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair3-clause-extract.json
file.145.verdict=skipped
file.145.reason=non-code-file
file.146.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair3-decomposition.txt
file.146.verdict=skipped
file.146.reason=non-code-file
file.147.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair3-gate-scan.json
file.147.verdict=skipped
file.147.reason=non-code-file
file.148.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair3-glossary-validate.txt
file.148.verdict=skipped
file.148.reason=non-code-file
file.149.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair3-pre-analyze-plan.txt
file.149.verdict=skipped
file.149.reason=non-code-file
file.150.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair3-pre-analyze-requirements.txt
file.150.verdict=skipped
file.150.reason=non-code-file
file.151.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair3-pre-analyze-tasks.txt
file.151.verdict=skipped
file.151.reason=non-code-file
file.152.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair3-requirements-validator.txt
file.152.verdict=skipped
file.152.reason=non-code-file
file.153.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair3-run-id.txt
file.153.verdict=skipped
file.153.reason=non-code-file
file.154.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair3-tasks-validator.txt
file.154.verdict=skipped
file.154.reason=non-code-file
file.155.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair4-2026-11-26.md
file.155.verdict=skipped
file.155.reason=non-code-file
file.156.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair4-clause-coverage.txt
file.156.verdict=skipped
file.156.reason=non-code-file
file.157.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair4-clause-extract.json
file.157.verdict=skipped
file.157.reason=non-code-file
file.158.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair4-decomposition.txt
file.158.verdict=skipped
file.158.reason=non-code-file
file.159.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair4-gate-scan.json
file.159.verdict=skipped
file.159.reason=non-code-file
file.160.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair4-glossary-validate.txt
file.160.verdict=skipped
file.160.reason=non-code-file
file.161.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair4-pre-analyze-plan.txt
file.161.verdict=skipped
file.161.reason=non-code-file
file.162.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair4-pre-analyze-requirements.txt
file.162.verdict=skipped
file.162.reason=non-code-file
file.163.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair4-pre-analyze-tasks.txt
file.163.verdict=skipped
file.163.reason=non-code-file
file.164.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair4-requirements-validator.txt
file.164.verdict=skipped
file.164.reason=non-code-file
file.165.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair4-run-id.txt
file.165.verdict=skipped
file.165.reason=non-code-file
file.166.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-repair4-tasks-validator.txt
file.166.verdict=skipped
file.166.reason=non-code-file
file.167.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-report-2026-11-25.md
file.167.verdict=skipped
file.167.reason=non-code-file
file.168.path=.specify/specs/106-background-silent-failure/test-evidence/analyze-report-r5-2026-11-26.md
file.168.verdict=skipped
file.168.reason=non-code-file
file.169.path=.specify/specs/106-background-silent-failure/test-evidence/analyze.jsonl
file.169.verdict=skipped
file.169.reason=non-code-file
file.170.path=.specify/specs/106-background-silent-failure/test-evidence/checklist-artifact-counts.txt
file.170.verdict=skipped
file.170.reason=non-code-file
file.171.path=.specify/specs/106-background-silent-failure/test-evidence/checklist-requirements-validator.txt
file.171.verdict=skipped
file.171.reason=non-code-file
file.172.path=.specify/specs/106-background-silent-failure/test-evidence/checklist.jsonl
file.172.verdict=skipped
file.172.reason=non-code-file
file.173.path=.specify/specs/106-background-silent-failure/test-evidence/clarify.jsonl
file.173.verdict=skipped
file.173.reason=non-code-file
file.174.path=.specify/specs/106-background-silent-failure/test-evidence/clause-coverage-tasks.txt
file.174.verdict=skipped
file.174.reason=non-code-file
file.175.path=.specify/specs/106-background-silent-failure/test-evidence/confirmation-total-red-at-base.txt
file.175.verdict=skipped
file.175.reason=non-code-file
file.176.path=.specify/specs/106-background-silent-failure/test-evidence/decomposition-plan.json
file.176.verdict=skipped
file.176.reason=non-code-file
file.177.path=.specify/specs/106-background-silent-failure/test-evidence/decomposition-plan.stdout.txt
file.177.verdict=skipped
file.177.reason=non-code-file
file.178.path=.specify/specs/106-background-silent-failure/test-evidence/enforcement-honesty.md
file.178.verdict=skipped
file.178.reason=non-code-file
file.179.path=.specify/specs/106-background-silent-failure/test-evidence/exec-quant-analyze-repair.txt
file.179.verdict=skipped
file.179.reason=non-code-file
file.180.path=.specify/specs/106-background-silent-failure/test-evidence/exec-quant-analyze-repair2.txt
file.180.verdict=skipped
file.180.reason=non-code-file
file.181.path=.specify/specs/106-background-silent-failure/test-evidence/exec-quant-analyze-repair3.txt
file.181.verdict=skipped
file.181.reason=non-code-file
file.182.path=.specify/specs/106-background-silent-failure/test-evidence/exec-quant-analyze-repair4.txt
file.182.verdict=skipped
file.182.reason=non-code-file
file.183.path=.specify/specs/106-background-silent-failure/test-evidence/exec-quant-analyze.txt
file.183.verdict=skipped
file.183.reason=non-code-file
file.184.path=.specify/specs/106-background-silent-failure/test-evidence/exec-quant-checklist.txt
file.184.verdict=skipped
file.184.reason=non-code-file
file.185.path=.specify/specs/106-background-silent-failure/test-evidence/exec-quant-clarify.txt
file.185.verdict=skipped
file.185.reason=non-code-file
file.186.path=.specify/specs/106-background-silent-failure/test-evidence/exec-quant-plan.txt
file.186.verdict=skipped
file.186.reason=non-code-file
file.187.path=.specify/specs/106-background-silent-failure/test-evidence/exec-quant-tasks.txt
file.187.verdict=skipped
file.187.reason=non-code-file
file.188.path=.specify/specs/106-background-silent-failure/test-evidence/exec-quant.txt
file.188.verdict=skipped
file.188.reason=non-code-file
file.189.path=.specify/specs/106-background-silent-failure/test-evidence/feedback-record-analyze-repair.txt
file.189.verdict=skipped
file.189.reason=non-code-file
file.190.path=.specify/specs/106-background-silent-failure/test-evidence/feedback-record-analyze-repair2.txt
file.190.verdict=skipped
file.190.reason=non-code-file
file.191.path=.specify/specs/106-background-silent-failure/test-evidence/feedback-record-analyze-repair3.txt
file.191.verdict=skipped
file.191.reason=non-code-file
file.192.path=.specify/specs/106-background-silent-failure/test-evidence/feedback-record-analyze-repair4.txt
file.192.verdict=skipped
file.192.reason=non-code-file
file.193.path=.specify/specs/106-background-silent-failure/test-evidence/feedback-record-analyze.txt
file.193.verdict=skipped
file.193.reason=non-code-file
file.194.path=.specify/specs/106-background-silent-failure/test-evidence/feedback-record-checklist.txt
file.194.verdict=skipped
file.194.reason=non-code-file
file.195.path=.specify/specs/106-background-silent-failure/test-evidence/feedback-record-clarify.txt
file.195.verdict=skipped
file.195.reason=non-code-file
file.196.path=.specify/specs/106-background-silent-failure/test-evidence/feedback-record-plan.txt
file.196.verdict=skipped
file.196.reason=non-code-file
file.197.path=.specify/specs/106-background-silent-failure/test-evidence/feedback-record-tasks.txt
file.197.verdict=skipped
file.197.reason=non-code-file
file.198.path=.specify/specs/106-background-silent-failure/test-evidence/feedback-record.txt
file.198.verdict=skipped
file.198.reason=non-code-file
file.199.path=.specify/specs/106-background-silent-failure/test-evidence/final-gate.txt
file.199.verdict=skipped
file.199.reason=non-code-file
file.200.path=.specify/specs/106-background-silent-failure/test-evidence/flow-class-lookup-checklist.txt
file.200.verdict=skipped
file.200.reason=non-code-file
file.201.path=.specify/specs/106-background-silent-failure/test-evidence/flow-class-lookup-clarify.txt
file.201.verdict=skipped
file.201.reason=non-code-file
file.202.path=.specify/specs/106-background-silent-failure/test-evidence/flow-class-lookup-plan.txt
file.202.verdict=skipped
file.202.reason=non-code-file
file.203.path=.specify/specs/106-background-silent-failure/test-evidence/flow-class-lookup.txt
file.203.verdict=skipped
file.203.reason=non-code-file
file.204.path=.specify/specs/106-background-silent-failure/test-evidence/git-access-anomaly.txt
file.204.verdict=skipped
file.204.reason=non-code-file
file.205.path=.specify/specs/106-background-silent-failure/test-evidence/git-commit-attempt-clarify.txt
file.205.verdict=skipped
file.205.reason=non-code-file
file.206.path=.specify/specs/106-background-silent-failure/test-evidence/glossary-proposal-plan.txt
file.206.verdict=skipped
file.206.reason=non-code-file
file.207.path=.specify/specs/106-background-silent-failure/test-evidence/goal-team-activation.txt
file.207.verdict=skipped
file.207.reason=non-code-file
file.208.path=.specify/specs/106-background-silent-failure/test-evidence/implement-baseline-full.txt
file.208.verdict=skipped
file.208.reason=non-code-file
file.209.path=.specify/specs/106-background-silent-failure/test-evidence/implement-integration.md
file.209.verdict=skipped
file.209.reason=non-code-file
file.210.path=.specify/specs/106-background-silent-failure/test-evidence/mirror-check-baseline.txt
file.210.verdict=skipped
file.210.reason=non-code-file
file.211.path=.specify/specs/106-background-silent-failure/test-evidence/mutation-drill.md
file.211.verdict=skipped
file.211.reason=non-code-file
file.212.path=.specify/specs/106-background-silent-failure/test-evidence/non-goals-audit.md
file.212.verdict=skipped
file.212.reason=non-code-file
file.213.path=.specify/specs/106-background-silent-failure/test-evidence/plan-stage-2026-11-25.md
file.213.verdict=skipped
file.213.reason=non-code-file
file.214.path=.specify/specs/106-background-silent-failure/test-evidence/plan.jsonl
file.214.verdict=skipped
file.214.reason=non-code-file
file.215.path=.specify/specs/106-background-silent-failure/test-evidence/pre-analyze-plan-before-fill.txt
file.215.verdict=skipped
file.215.reason=non-code-file
file.216.path=.specify/specs/106-background-silent-failure/test-evidence/pre-analyze-plan.json
file.216.verdict=skipped
file.216.reason=non-code-file
file.217.path=.specify/specs/106-background-silent-failure/test-evidence/pre-analyze-plan.stdout.txt
file.217.verdict=skipped
file.217.reason=non-code-file
file.218.path=.specify/specs/106-background-silent-failure/test-evidence/pre-analyze-requirements-clarify.json
file.218.verdict=skipped
file.218.reason=non-code-file
file.219.path=.specify/specs/106-background-silent-failure/test-evidence/pre-analyze-requirements-clarify.stdout.txt
file.219.verdict=skipped
file.219.reason=non-code-file
file.220.path=.specify/specs/106-background-silent-failure/test-evidence/pre-analyze-requirements.json
file.220.verdict=skipped
file.220.reason=non-code-file
file.221.path=.specify/specs/106-background-silent-failure/test-evidence/pre-analyze-requirements.stdout.txt
file.221.verdict=skipped
file.221.reason=non-code-file
file.222.path=.specify/specs/106-background-silent-failure/test-evidence/pre-analyze-tasks.json
file.222.verdict=skipped
file.222.reason=non-code-file
file.223.path=.specify/specs/106-background-silent-failure/test-evidence/pre-analyze-tasks.stdout.txt
file.223.verdict=skipped
file.223.reason=non-code-file
file.224.path=.specify/specs/106-background-silent-failure/test-evidence/quickstart-role-edge-empty-report.json
file.224.verdict=skipped
file.224.reason=non-code-file
file.225.path=.specify/specs/106-background-silent-failure/test-evidence/quickstart-role-edge-help.txt
file.225.verdict=skipped
file.225.reason=non-code-file
file.226.path=.specify/specs/106-background-silent-failure/test-evidence/reaction-drill.md
file.226.verdict=skipped
file.226.reason=non-code-file
file.227.path=.specify/specs/106-background-silent-failure/test-evidence/role-edge-report-empty-fbab7a45c.json
file.227.verdict=skipped
file.227.reason=non-code-file
file.228.path=.specify/specs/106-background-silent-failure/test-evidence/run-determination-analyze-repair.txt
file.228.verdict=skipped
file.228.reason=non-code-file
file.229.path=.specify/specs/106-background-silent-failure/test-evidence/run-determination-analyze-repair2.txt
file.229.verdict=skipped
file.229.reason=non-code-file
file.230.path=.specify/specs/106-background-silent-failure/test-evidence/run-determination-analyze-repair3.txt
file.230.verdict=skipped
file.230.reason=non-code-file
file.231.path=.specify/specs/106-background-silent-failure/test-evidence/run-determination-analyze-repair4.txt
file.231.verdict=skipped
file.231.reason=non-code-file
file.232.path=.specify/specs/106-background-silent-failure/test-evidence/run-determination-analyze.txt
file.232.verdict=skipped
file.232.reason=non-code-file
file.233.path=.specify/specs/106-background-silent-failure/test-evidence/run-determination-checklist.txt
file.233.verdict=skipped
file.233.reason=non-code-file
file.234.path=.specify/specs/106-background-silent-failure/test-evidence/run-determination-clarify.txt
file.234.verdict=skipped
file.234.reason=non-code-file
file.235.path=.specify/specs/106-background-silent-failure/test-evidence/run-determination-plan.txt
file.235.verdict=skipped
file.235.reason=non-code-file
file.236.path=.specify/specs/106-background-silent-failure/test-evidence/run-determination-tasks.txt
file.236.verdict=skipped
file.236.reason=non-code-file
file.237.path=.specify/specs/106-background-silent-failure/test-evidence/run-determination.txt
file.237.verdict=skipped
file.237.reason=non-code-file
file.238.path=.specify/specs/106-background-silent-failure/test-evidence/scan-confirmation-gates-baseline.json
file.238.verdict=skipped
file.238.reason=non-code-file
file.239.path=.specify/specs/106-background-silent-failure/test-evidence/super-sub-protocol-fbab7a45c.txt
file.239.verdict=skipped
file.239.reason=non-code-file
file.240.path=.specify/specs/106-background-silent-failure/test-evidence/t033-smoke.txt
file.240.verdict=skipped
file.240.reason=non-code-file
file.241.path=.specify/specs/106-background-silent-failure/test-evidence/tasks-premises.txt
file.241.verdict=skipped
file.241.reason=non-code-file
file.242.path=.specify/specs/106-background-silent-failure/test-evidence/tasks.jsonl
file.242.verdict=skipped
file.242.reason=non-code-file
file.243.path=.specify/specs/106-background-silent-failure/test-evidence/test-entry-smoke.txt
file.243.verdict=skipped
file.243.reason=non-code-file
file.244.path=.specify/specs/106-background-silent-failure/test-evidence/validate-r4-01.verdicts.json
file.244.verdict=skipped
file.244.reason=non-code-file
file.245.path=.specify/specs/106-background-silent-failure/test-evidence/validate-tasks.json
file.245.verdict=skipped
file.245.reason=non-code-file
file.246.path=.specify/specs/106-background-silent-failure/test-evidence/validate-tasks.stdout.txt
file.246.verdict=skipped
file.246.reason=non-code-file
file.247.path=.specify/specs/106-background-silent-failure/test-evidence/validate-wave1.verdicts.json
file.247.verdict=skipped
file.247.reason=non-code-file
file.248.path=.specify/specs/106-background-silent-failure/test-evidence/validate-wave2.verdicts.json
file.248.verdict=skipped
file.248.reason=non-code-file
file.249.path=.specify/specs/106-background-silent-failure/test-evidence/validate-wave3.verdicts.json
file.249.verdict=skipped
file.249.reason=non-code-file
file.250.path=.specify/specs/106-background-silent-failure/test-evidence/validator-requirements-clarify.txt
file.250.verdict=skipped
file.250.reason=non-code-file
file.251.path=.specify/specs/106-background-silent-failure/test-evidence/validator-requirements.txt
file.251.verdict=skipped
file.251.reason=non-code-file
file.252.path=.specify/specs/106-background-silent-failure/test-evidence/verification-input.md
file.252.verdict=skipped
file.252.reason=non-code-file
file.253.path=.specify/specs/106-background-silent-failure/test-evidence/watch-help-baseline.txt
file.253.verdict=skipped
file.253.reason=non-code-file
file.254.path=.specify/specs/106-background-silent-failure/test-evidence/watch-self-test-baseline.txt
file.254.verdict=skipped
file.254.reason=non-code-file
file.255.path=.specify/specs/106-background-silent-failure/test-evidence/watch-target-fbab7a45c.sh
file.255.verdict=skipped
file.255.reason=non-code-file
file.256.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-check-analyze-repair-before-commit.txt
file.256.verdict=skipped
file.256.reason=non-code-file
file.257.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-check-analyze-repair-postcommit.txt
file.257.verdict=skipped
file.257.reason=non-code-file
file.258.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-check-analyze-repair2-before-commit.txt
file.258.verdict=skipped
file.258.reason=non-code-file
file.259.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-check-analyze-repair2-postcommit.txt
file.259.verdict=skipped
file.259.reason=non-code-file
file.260.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-check-analyze-repair3-before-commit.txt
file.260.verdict=skipped
file.260.reason=non-code-file
file.261.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-check-analyze-repair3-postcommit.txt
file.261.verdict=skipped
file.261.reason=non-code-file
file.262.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-check-analyze-repair4-before-commit.txt
file.262.verdict=skipped
file.262.reason=non-code-file
file.263.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-check-analyze-repair4-postcommit.txt
file.263.verdict=skipped
file.263.reason=non-code-file
file.264.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-check-checklist-postcommit.txt
file.264.verdict=skipped
file.264.reason=non-code-file
file.265.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-check-checklist.txt
file.265.verdict=skipped
file.265.reason=non-code-file
file.266.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-check-clarify-repair.txt
file.266.verdict=skipped
file.266.reason=non-code-file
file.267.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-check-clarify.txt
file.267.verdict=skipped
file.267.reason=non-code-file
file.268.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-check.txt
file.268.verdict=skipped
file.268.reason=non-code-file
file.269.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-plan-after-driver.json
file.269.verdict=skipped
file.269.reason=non-code-file
file.270.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-plan-after.json
file.270.verdict=skipped
file.270.reason=non-code-file
file.271.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-plan-before.json
file.271.verdict=skipped
file.271.reason=non-code-file
file.272.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-requirements.json
file.272.verdict=skipped
file.272.reason=non-code-file
file.273.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-snapshot-analyze-before-commit.json
file.273.verdict=skipped
file.273.reason=non-code-file
file.274.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-snapshot-analyze-repair-before-commit.json
file.274.verdict=skipped
file.274.reason=non-code-file
file.275.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-snapshot-analyze-repair2-before.json
file.275.verdict=skipped
file.275.reason=non-code-file
file.276.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-snapshot-analyze-repair3-before.json
file.276.verdict=skipped
file.276.reason=non-code-file
file.277.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-snapshot-analyze-repair4-before.json
file.277.verdict=skipped
file.277.reason=non-code-file
file.278.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-snapshot-checklist-after.json
file.278.verdict=skipped
file.278.reason=non-code-file
file.279.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-snapshot-checklist-before.json
file.279.verdict=skipped
file.279.reason=non-code-file
file.280.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-tasks-after.json
file.280.verdict=skipped
file.280.reason=non-code-file
file.281.path=.specify/specs/106-background-silent-failure/test-evidence/workspace-tasks-before.json
file.281.verdict=skipped
file.281.reason=non-code-file
file.282.path=.specify/teams/106-background-silent-failure/team.md
file.282.verdict=skipped
file.282.reason=non-code-file
file.283.path=agents/sdd-implement-coordinator.agent.md
file.283.verdict=reviewed
file.284.path=agents/sdd-plan-coordinator.agent.md
file.284.verdict=reviewed
file.285.path=agents/sdd-review-coordinator.agent.md
file.285.verdict=reviewed
file.286.path=agents/sdd-task-coordinator.agent.md
file.286.verdict=reviewed
file.287.path=docs/reference/commands/agents.md
file.287.verdict=reviewed
file.288.path=docs/reference/skills/sdd-loop-driver.md
file.288.verdict=reviewed
file.289.path=docs/reference/teams/orchestration.md
file.289.verdict=reviewed
file.290.path=scripts/python/role-edge-check.py
file.290.verdict=reviewed
file.291.path=shared/definitions/subagent-definitions.md
file.291.verdict=reviewed
file.292.path=shared/definitions/superagent-definitions.md
file.292.verdict=reviewed
file.293.path=shared/workflow/external-dispatch-recipes.md
file.293.verdict=reviewed
file.294.path=skills/external/sdd-loop-driver/SKILL.md
file.294.verdict=reviewed
file.295.path=skills/internal/create-team/SKILL.md
file.295.verdict=reviewed
file.296.path=skills/internal/create-team/scripts/dispatch.sh
file.296.verdict=reviewed
file.297.path=skills/internal/run-agent/SKILL.md
file.297.verdict=reviewed
file.298.path=skills/internal/run-team/SKILL.md
file.298.verdict=reviewed
file.299.path=templates/commands/agents.md
file.299.verdict=reviewed
file.300.path=templates/commands/team.md
file.300.verdict=reviewed
file.301.path=tests/contract/test_settlement_carriers.py
file.301.verdict=reviewed
file.302.path=tests/contract/test_settlement_contract_definitions.py
file.302.verdict=reviewed
file.303.path=tests/contract/test_settlement_engine.py
file.303.verdict=reviewed
file.304.path=tests/contract/test_settlement_migration.py
file.304.verdict=reviewed
file.305.path=tests/contract/test_settlement_preservation.py
file.305.verdict=reviewed
file.306.path=tests/contract/test_settlement_scope.py
file.306.verdict=reviewed
file.307.path=tests/fixtures/settlement/builders.py
file.307.verdict=reviewed
file.308.path=tests/fixtures/settlement/c1-state/demo-line.md
file.308.verdict=reviewed
file.309.path=tests/fixtures/settlement/c1-state/heartbeat-demo-line-implement.log
file.309.verdict=reviewed
file.310.path=tests/fixtures/settlement/c1-state/log-demo-line-implement.log
file.310.verdict=reviewed
file.311.path=tests/fixtures/settlement/c1-state/pid-demo-line-implement
file.311.verdict=reviewed
file.312.path=tests/fixtures/settlement/c1-state/prompt-demo-line-implement.md.meta.json
file.312.verdict=reviewed
file.313.path=tests/fixtures/settlement/c1-state/status-demo-line-implement
file.313.verdict=reviewed
file.314.path=tests/fixtures/settlement/c3-report/logs/seat-legacy.attempt
file.314.verdict=reviewed
file.315.path=tests/fixtures/settlement/c3-report/logs/seat-missing-start.return.txt
file.315.verdict=reviewed
file.316.path=tests/fixtures/settlement/c3-report/logs/seat-ok.attempt
file.316.verdict=reviewed
file.317.path=tests/fixtures/settlement/c3-report/logs/seat-ok.return.txt
file.317.verdict=reviewed
file.318.path=tests/fixtures/settlement/c3-report/teams/demo-team/runs/20261120T000000Z-report.md
file.318.verdict=reviewed
file.319.path=tests/fixtures/settlement/c3-report/teams/legacy-team/runs/20261119T000000Z-report.md
file.319.verdict=reviewed
file.320.path=tests/fixtures/settlement/legacy/logs/legacy-run.attempt
file.320.verdict=reviewed
file.321.path=tests/fixtures/settlement/legacy/logs/legacy-run.end
file.321.verdict=reviewed
file.322.path=tests/fixtures/settlement/legacy/logs/legacy-run.live.log
file.322.verdict=reviewed
file.323.path=tests/fixtures/settlement/legacy/logs/legacy-run.return.txt
file.323.verdict=reviewed
file.324.path=tests/fixtures/settlement/legacy/logs/legacy-run.settlement
file.324.verdict=reviewed
file.325.path=tests/fixtures/settlement/legacy/logs/legacy-run.status
file.325.verdict=reviewed
file.326.path=tests/fixtures/settlement/versioned/logs/versioned-run.attempt
file.326.verdict=reviewed
file.327.path=tests/fixtures/settlement/versioned/logs/versioned-run.end
file.327.verdict=reviewed
file.328.path=tests/fixtures/settlement/versioned/logs/versioned-run.live.log
file.328.verdict=reviewed
file.329.path=tests/fixtures/settlement/versioned/logs/versioned-run.return.txt
file.329.verdict=reviewed
file.330.path=tests/fixtures/settlement/versioned/logs/versioned-run.settlement
file.330.verdict=reviewed
file.331.path=tests/fixtures/settlement/versioned/logs/versioned-run.status
file.331.verdict=reviewed
<!-- coverage-receipt:end -->
