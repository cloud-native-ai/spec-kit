# Code Review Report — 代码段 (code segment)

| 属性 | 值 |
|------|-----|
| **分支** | `112-decision-batch-panel` |
| **基准** | `c3489e52c597f7937824f728e104ea035a639baf` (`c3489e52c`) |
| **目标** | `838e7acb4650512bceefd689fec8e0da07c78f6d` (`838e7acb4`) |
| **基准来源** | `feature-first-commit` |
| **渲染模式** | `renderer: text` |
| **Reviewer** | `Qiming Liu (John)` |
| **日期** | `2026-11-27T11:20:06Z` |

## 段裁决

| 字段 | 值 |
|------|-----|
| Segment verdict | `blocked` |
| Gate verdict | `blocking-unresolved` (2 blocking entries; `report --summary --file` exits 1) |
| Reason | none — the refusal is the blocking set itself |
| Uncommitted scope | none beyond this run's own records (`review.md`, `code-review.md`) and the ignored scratch `.specify/.tmp/review-smoke-112.txt`; no product file is uncommitted |

## 变更概览

```
 .claude/commands/speckit.decide.md                 |   36 +
 .github/prompts/speckit.decide.prompt.md           |   36 +
 .opencode/command/speckit.decide.md                |   36 +
 .qoder/commands/speckit.decide.md                  |   39 +
 .../records/20261127T082913128534Z-ee9e2990.json   |    1 +
 .../records/20261127T084128423634Z-1badf7ac.json   |    1 +
 .../records/20261127T085643910002Z-e0a626d6.json   |    1 +
 .../records/20261127T090925309265Z-98aed753.json   |    1 +
 .../records/20261127T091728386412Z-1b103a03.json   |    1 +
 .../records/20261127T092900436577Z-71eaf093.json   |    1 +
 .../records/20261127T094641002616Z-09a39250.json   |    1 +
 .../records/20261127T100543484163Z-7125b0fa.json   |    1 +
 .specify/features.md                               |    3 +-
 .specify/features/112-decision-batch-panel.md      |   90 +
 .../20261127T082913Z-speckit-requirements.md       |   21 +
 .../feedback/20261127T084128Z-speckit-clarify.md   |   21 +
 .specify/feedback/20261127T085649Z-speckit-plan.md |   21 +
 .../feedback/20261127T090930Z-speckit-tasks.md     |   21 +
 .../feedback/20261127T091735Z-speckit-checklist.md |   21 +
 .../feedback/20261127T092907Z-speckit-analyze.md   |   26 +
 .../feedback/20261127T094647Z-speckit-analyze.md   |   25 +
 .../feedback/20261127T100546Z-speckit-implement.md |   21 +
 ...T082928Z-r20261127T081500Z-112a-requirements.md |   63 +
 ...61127T084136Z-r20261127T081500Z-112a-clarify.md |   57 +
 ...20261127T085702Z-r20261127T081500Z-112a-plan.md |   58 +
 ...0261127T091004Z-r20261127T081500Z-112a-tasks.md |   54 +
 ...127T091753Z-r20261127T081500Z-112a-checklist.md |   55 +
 ...61127T093023Z-r20261127T081500Z-112a-analyze.md |   56 +
 ...61127T094729Z-r20261127T094343Z-112a-analyze.md |   57 +
 .specify/scripts/python/decision-batch.py          | 2190 ++++++++++++++++++++
 .specify/scripts/python/validate-decisions.py      |   32 +
 ...mination-speckit-plan-r20261127t053750z-109a.md |   10 +-
 ...n-speckit-requirements-r20261127t081500z-112.md |  207 ++
 ...ation-speckit-clarify-r20261127t081500z-112a.md |  202 ++
 ...mination-speckit-plan-r20261127t081500z-112a.md |  207 ++
 ...ination-speckit-tasks-r20261127t081500z-112a.md |  202 ++
 ...ion-speckit-checklist-r20261127t081500z-112a.md |  202 ++
 ...ation-speckit-analyze-r20261127t081500z-112a.md |  202 ++
 ...ation-speckit-analyze-r20261127t094343z-112a.md |  202 ++
 ...ion-speckit-implement-r20261127t081500z-112a.md |  205 ++
 .../shared/definitions/decision-definitions.md     |  374 +++-
 .../shared/definitions/flow-class-definitions.md   |    4 +-
 .specify/shared/definitions/framework-map.md       |    2 +-
 .specify/shared/definitions/probe-definitions.md   |    1 +
 .specify/skills/internal/decide-batch/SKILL.md     |   64 +
 .../checklists/requirements-quality-2026-11-27.md  |  101 +
 .../checklists/requirements.md                     |   51 +
 .../checkpoints/01-requirements.md                 |    7 +
 .../checkpoints/02-clarify.md                      |    7 +
 .../checkpoints/03-plan.md                         |    7 +
 .../checkpoints/04-tasks.md                        |    7 +
 .../checkpoints/05-checklist.md                    |    7 +
 .../checkpoints/06-analyze.md                      |    7 +
 .../checkpoints/07-implement.md                    |    7 +
 .../contracts/completeness-refusal.contract.md     |   36 +
 .../contracts/default-derivation.contract.md       |   34 +
 .../contracts/objection-reply.contract.md          |   38 +
 .../contracts/presentation.contract.md             |   36 +
 .../contracts/record-replay.contract.md            |   44 +
 .../contracts/source-roster.contract.md            |   40 +
 .../112-decision-batch-panel/coverage-baseline.txt |  789 +++++++
 .../specs/112-decision-batch-panel/data-model.md   |  266 +++
 .../specs/112-decision-batch-panel/feature-ref.md  |  111 +
 .../notes/pre-change-measurements.md               |   24 +
 .../notes/quickstart-run.md                        |  178 ++
 .../notes/red-first-evidence.md                    |  332 +++
 .../notes/red-first-names-us2-contract.txt         |    1 +
 .../notes/red-first-names-us2.txt                  |   12 +
 .../notes/red-first-names-us3.txt                  |    6 +
 .../notes/red-first-names-us4.txt                  |    6 +
 .../notes/red-first-names-us5.txt                  |    6 +
 .../notes/red-first-names.txt                      |   23 +
 .../112-decision-batch-panel/notes/us1-green.txt   |   67 +
 .../112-decision-batch-panel/notes/us2-green.txt   |   91 +
 .../112-decision-batch-panel/notes/us3-green.txt   |   95 +
 .../112-decision-batch-panel/notes/us4-green.txt   |   81 +
 .../112-decision-batch-panel/notes/us5-green.txt   |  103 +
 .specify/specs/112-decision-batch-panel/plan.md    |  179 ++
 .../specs/112-decision-batch-panel/quickstart.md   |  124 ++
 .../specs/112-decision-batch-panel/requirements.md |  439 ++++
 .../specs/112-decision-batch-panel/research.md     |   62 +
 .specify/specs/112-decision-batch-panel/tasks.md   |  433 ++++
 .../test-evidence/analyze-exec-quant.txt           |    1 +
 .../test-evidence/analyze-feedback-record.txt      |    9 +
 .../analyze-repair-pre-analyze-tasks.json          |  556 +++++
 .../analyze-repair-pre-analyze-tasks.txt           |    2 +
 .../test-evidence/analyze-repair-round1.md         |   93 +
 .../analyze-repair-validate-requirements.txt       |   11 +
 .../analyze-repair-validate-tasks.txt              |    2 +
 .../test-evidence/analyze-round1-findings.jsonl    |   16 +
 .../test-evidence/analyze-round1-report.md         |  167 ++
 .../test-evidence/analyze-round2-exec-quant.txt    |    1 +
 .../analyze-round2-feedback-record.txt             |    9 +
 .../test-evidence/analyze-round2-findings.jsonl    |   20 +
 .../test-evidence/analyze-round2-gates.txt         | 1802 ++++++++++++++++
 .../test-evidence/analyze-round2-report.md         |  199 ++
 .../analyze-round2-run-determination.txt           |    8 +
 .../test-evidence/analyze-run-determination.txt    |    8 +
 .../test-evidence/checklist-exec-quant.txt         |    1 +
 .../test-evidence/checklist-feedback-record.txt    |    9 +
 .../checklist-requirements-validator.txt           |   10 +
 .../test-evidence/checklist-run-determination.txt  |    8 +
 .../test-evidence/checklist-selfcheck.txt          |  129 ++
 .../test-evidence/checklist-spec-readings.txt      |   53 +
 .../test-evidence/checklist-stage-2026-11-27.md    |   66 +
 .../test-evidence/clarify-exec-quant.txt           |    1 +
 .../test-evidence/clarify-feedback-record.txt      |    9 +
 .../test-evidence/clarify-roster-measure.txt       |   27 +
 .../test-evidence/clarify-run-determination.txt    |    8 +
 .../test-evidence/clarify-stage-2026-11-27.md      |   57 +
 .../test-evidence/clarify-validator-after.txt      |   10 +
 .../test-evidence/clarify-validator-before.txt     |   10 +
 .../test-evidence/clarify-validator-postcommit.txt |   10 +
 .../closure-acceptance-2026-11-27.json             |   38 +
 .../decomposition-requirements-postcommit.json     |   12 +
 .../decomposition-requirements-postcommit.txt      |    1 +
 .../test-evidence/decomposition-requirements.json  |   12 +
 .../test-evidence/decomposition-requirements.txt   |    1 +
 .../test-evidence/decomposition-tasks.json         |    1 +
 .../test-evidence/decomposition-tasks.txt          |    6 +
 .../test-evidence/implement-p1-baseline-failed.txt |    5 +
 .../test-evidence/implement-p1-exec-quant.txt      |    1 +
 .../test-evidence/implement-p1-feedback-record.txt |    9 +
 .../implement-p1-run-determination.txt             |    8 +
 .../test-evidence/implement-p1-stage-2026-11-27.md |   74 +
 .../test-evidence/implement-p2-exec-quant.txt      |    1 +
 .../test-evidence/implement-p2-feedback-record.txt |    9 +
 .../implement-p2-run-determination.txt             |    1 +
 .../test-evidence/implement-p2-stage-2026-11-27.md |   85 +
 .../test-evidence/implement-p3-exec-quant.txt      |    1 +
 .../test-evidence/implement-p3-feedback-record.txt |    9 +
 .../implement-p3-run-determination.txt             |    1 +
 .../test-evidence/implement-p3-stage-2026-11-27.md |   67 +
 .../test-evidence/implement-p4-exec-quant.txt      |    1 +
 .../test-evidence/implement-p4-feedback-record.txt |    9 +
 .../implement-p4-full-suite-baseline-names.txt     |  229 ++
 .../implement-p4-full-suite-names.txt              |  229 ++
 .../test-evidence/implement-p4-full-suite.txt      |   71 +
 .../test-evidence/implement-p4-gates.txt           |   14 +
 .../implement-p4-regression-names.txt              |    0
 .../implement-p4-run-determination.txt             |    1 +
 .../test-evidence/implement-p4-stage-2026-11-27.md |   70 +
 .../test-evidence/plan-exec-quant.txt              |    1 +
 .../test-evidence/plan-feedback-record.txt         |    9 +
 .../test-evidence/plan-integrity-postcommit.txt    |    4 +
 .../test-evidence/plan-integrity.txt               |    4 +
 .../test-evidence/plan-run-determination.txt       |    9 +
 .../test-evidence/plan-stage-2026-11-27.md         |   71 +
 .../test-evidence/plan-tensions.txt                |   11 +
 .../test-evidence/pre-analyze-checklist.txt        |    5 +
 .../test-evidence/pre-analyze-plan.json            |  290 +++
 .../test-evidence/pre-analyze-plan.txt             |    1 +
 .../pre-analyze-requirements-postcommit.json       |   73 +
 .../pre-analyze-requirements-postcommit.txt        |    1 +
 .../test-evidence/pre-analyze-requirements.json    |   73 +
 .../test-evidence/pre-analyze-requirements.txt     |    1 +
 .../test-evidence/pre-analyze-tasks-p4.txt         |    2 +
 .../test-evidence/pre-analyze-tasks.json           |  549 +++++
 .../test-evidence/pre-analyze-tasks.txt            |    1 +
 .../test-evidence/requirements-exec-quant.txt      |    1 +
 .../test-evidence/requirements-feedback-record.txt |    9 +
 .../requirements-run-determination.txt             |    8 +
 .../test-evidence/requirements-stage-2026-11-27.md |   64 +
 .../requirements-validator-postcommit.txt          |   10 +
 .../test-evidence/requirements-validator.txt       |   10 +
 .../scan-confirmation-gates-baseline.txt           |    6 +
 .../test-evidence/tasks-exec-quant.txt             |    1 +
 .../test-evidence/tasks-feedback-record.txt        |    9 +
 .../test-evidence/tasks-run-determination.txt      |    8 +
 .../test-evidence/tasks-stage-2026-11-27.md        |   66 +
 .../test-evidence/tasks-validator-p4.txt           |    1 +
 .../test-evidence/tasks-validator.txt              |    1 +
 .../test-evidence/verification-input.md            |   79 +
 .../test-evidence/workspace-analyze-readings.txt   |    7 +
 .../workspace-analyze-repair-readings.txt          |    7 +
 .../test-evidence/workspace-analyze-repair.json    |  314 +++
 .../test-evidence/workspace-analyze.json           |  314 +++
 .../workspace-checklist-postcommit.json            |  315 +++
 .../test-evidence/workspace-checklist-readings.txt |    6 +
 .../test-evidence/workspace-checklist.json         |  315 +++
 .../test-evidence/workspace-clarify-check.txt      |    1 +
 .../workspace-clarify-postcommit.json              |  315 +++
 .../test-evidence/workspace-clarify-postcommit.txt |    1 +
 .../test-evidence/workspace-clarify.json           |  315 +++
 .../test-evidence/workspace-implement-p1-check.txt |    1 +
 .../test-evidence/workspace-implement-p1.json      |  314 +++
 .../test-evidence/workspace-implement-p2-check.txt |    1 +
 .../test-evidence/workspace-implement-p2.json      |  314 +++
 .../test-evidence/workspace-implement-p3-check.txt |    1 +
 .../test-evidence/workspace-implement-p3.json      |  313 +++
 .../test-evidence/workspace-implement-p4-check.txt |    1 +
 .../test-evidence/workspace-implement-p4.json      |  313 +++
 .../test-evidence/workspace-plan-check.txt         |    1 +
 .../test-evidence/workspace-plan-postcommit.json   |  315 +++
 .../test-evidence/workspace-plan-postcommit.txt    |    1 +
 .../test-evidence/workspace-plan.json              |  315 +++
 .../test-evidence/workspace-requirements-check.txt |    1 +
 .../workspace-requirements-postcommit.json         |  315 +++
 .../workspace-requirements-postcommit.txt          |    1 +
 .../test-evidence/workspace-requirements.json      |  315 +++
 .../test-evidence/workspace-tasks-check.txt        |    1 +
 .../test-evidence/workspace-tasks-postcommit.json  |  315 +++
 .../test-evidence/workspace-tasks.json             |  315 +++
 .../specs/112-decision-batch-panel/verification.md |   97 +
 .specify/trigger/index.json                        |    2 +-
 docs/reference/commands/decide.md                  |   58 +
 scripts/python/decision-batch.py                   | 2190 ++++++++++++++++++++
 scripts/python/validate-decisions.py               |   32 +
 shared/definitions/decision-definitions.md         |  374 +++-
 shared/definitions/flow-class-definitions.md       |    4 +-
 shared/definitions/framework-map.md                |    2 +-
 shared/definitions/probe-definitions.md            |    1 +
 skills/internal/decide-batch/SKILL.md              |   64 +
 templates/commands/decide.md                       |   40 +
 tests/contract/test_decision_batch_contract.py     |  513 +++++
 .../contract/test_decision_governance_contracts.py |   34 +-
 tests/contract/test_decision_governance_guards.py  |  137 +-
 tests/contract/test_flow_class_ledger.py           |   32 +-
 tests/contract/test_humanize_command_surface.py    |    6 +-
 .../contract/test_migrate_distribution_assembly.py |    6 +-
 tests/contract/test_migration_distribution.py      |   12 +-
 tests/contract/test_probe_nonentity_catalog.py     |    7 +-
 tests/fixtures/decision-batch/absent-root/.gitkeep |    0
 .../absent-root/.specify/register.md               |    4 +
 .../absent-root/.specify/specs/demo/one.md         |   17 +
 .../absent-root/.specify/specs/demo/ref.md         |    3 +
 tests/fixtures/decision-batch/autonomous/.gitkeep  |    0
 .../decision-batch/autonomous/.specify/register.md |    4 +
 .../.specify/specs/demo/auto-evidence.md           |    3 +
 .../autonomous/.specify/specs/demo/auto.md         |   17 +
 .../fixtures/decision-batch/batch-family/.gitkeep  |    0
 .../batch-family/.specify/register.md              |    4 +
 .../batch-family/.specify/specs/demo/household.md  |   41 +
 .../batch-family/.specify/specs/demo/ref.md        |    3 +
 .../decision-batch/class-conflict/.gitkeep         |    0
 .../class-conflict/.specify/register.md            |    4 +
 .../.specify/specs/demo/conflict-a.md              |   17 +
 .../.specify/specs/demo/conflict-b.md              |   17 +
 .../class-conflict/.specify/specs/demo/ref.md      |    3 +
 .../concurrency/.specify/register.md               |    4 +
 .../concurrency/.specify/specs/demo/ref.md         |    3 +
 .../concurrency/.specify/specs/demo/two-batches.md |   41 +
 tests/fixtures/decision-batch/drift/.gitkeep       |    0
 .../decision-batch/drift/.specify/register.md      |    4 +
 .../drift/.specify/specs/demo/ref.md               |    3 +
 .../drift/.specify/specs/demo/two.md               |   41 +
 .../decision-batch/eligibility-matrix/.gitkeep     |    0
 .../eligibility-matrix/.specify/register.md        |    4 +
 .../.specify/specs/demo/matrix.md                  |  100 +
 .../.specify/specs/demo/prior.md                   |   23 +
 .../eligibility-matrix/.specify/specs/demo/ref.md  |    3 +
 .../fixtures/decision-batch/empty-project/.gitkeep |    0
 .../decision-batch/grounding-grounded/.gitkeep     |    0
 .../grounding-grounded/.specify/register.md        |    4 +
 .../.specify/specs/demo/grounded.md                |   21 +
 .../.specify/specs/demo/prior-records.md           |   23 +
 .../decision-batch/grounding-none/.gitkeep         |    0
 .../grounding-none/.specify/register.md            |    4 +
 .../.specify/specs/demo/no-evidence.md             |   21 +
 .../grounding-none/.specify/specs/demo/notes.md    |    3 +
 .../decision-batch/incomplete-block/.gitkeep       |    0
 .../incomplete-block/.specify/register.md          |    6 +
 .../.specify/specs/demo/ambiguous.md               |   33 +
 .../.specify/specs/demo/defects.md                 |   36 +
 .../.specify/specs/demo/incomplete.md              |   20 +
 .../.specify/specs/demo/no-default.md              |   21 +
 .../incomplete-block/.specify/specs/demo/ref.md    |    3 +
 tests/fixtures/decision-batch/m10/.gitkeep         |    0
 .../decision-batch/m10/.specify/register.md        |    3 +
 tests/fixtures/decision-batch/m11/.gitkeep         |    0
 .../decision-batch/m11/.specify/register.md        |    4 +
 .../m11/.specify/specs/demo/defect.md              |   22 +
 .../decision-batch/m11/.specify/specs/demo/ref.md  |    3 +
 tests/fixtures/decision-batch/m12/.gitkeep         |    0
 .../decision-batch/m12/.specify/register.md        |    4 +
 .../decision-batch/m12/.specify/specs/demo/mix.md  |   41 +
 .../decision-batch/m12/.specify/specs/demo/ref.md  |    3 +
 tests/fixtures/decision-batch/m13/.gitkeep         |    0
 .../decision-batch/m13/.specify/register.md        |    4 +
 .../decision-batch/m13/.specify/specs/demo/item.md |   21 +
 .../m13/.specify/specs/demo/prior.md               |   23 +
 tests/fixtures/decision-batch/m14/.gitkeep         |    0
 .../decision-batch/m14/.specify/register.md        |    4 +
 .../decision-batch/m14/.specify/specs/demo/item.md |   21 +
 .../decision-batch/m14/.specify/specs/demo/ref.md  |    3 +
 tests/fixtures/decision-batch/m14/reply.md         |    6 +
 tests/fixtures/decision-batch/m14/scan.json        |  113 +
 tests/fixtures/decision-batch/m15/.gitkeep         |    0
 .../decision-batch-b-20261127t105123z-752792b7.md  |   78 +
 .../decision-batch/m15/.specify/register.md        |    6 +
 .../decision-batch/m15/.specify/specs/demo/item.md |   22 +
 .../decision-batch/m15/.specify/specs/demo/ref.md  |    3 +
 tests/fixtures/decision-batch/m15/reply.md         |    3 +
 tests/fixtures/decision-batch/m15/scan.json        |  113 +
 tests/fixtures/decision-batch/m16/.gitkeep         |    0
 .../decision-batch-b-20261127t105123z-4bbb645d.md  |   78 +
 .../decision-batch/m16/.specify/register.md        |    6 +
 .../decision-batch/m16/.specify/specs/demo/item.md |   22 +
 .../decision-batch/m16/.specify/specs/demo/ref.md  |    3 +
 tests/fixtures/decision-batch/m16/reply.md         |    3 +
 tests/fixtures/decision-batch/m16/scan.json        |  113 +
 .../decision-batch/prior-conflict/.gitkeep         |    0
 .../prior-conflict/.specify/register.md            |    4 +
 .../prior-conflict/.specify/specs/demo/conflict.md |   21 +
 .../.specify/specs/demo/history-records.md         |   23 +
 .../register-absent/.specify/specs/demo/absent.md  |   21 +
 .../register-absent/.specify/specs/demo/ref.md     |    3 +
 .../register-updates/.specify/register.md          |    7 +
 .../register-updates/.specify/specs/demo/ledger.md |   41 +
 .../register-updates/.specify/specs/demo/ref.md    |    3 +
 .../replay-broken/.specify/register.md             |    4 +
 .../replay-broken/.specify/specs/demo/ref.md       |    3 +
 .../replay-broken/.specify/specs/demo/replay.md    |   21 +
 .../fixtures/decision-batch/reply-shapes/.gitkeep  |    0
 .../reply-shapes/.specify/register.md              |    4 +
 .../reply-shapes/.specify/specs/demo/one.md        |   41 +
 .../reply-shapes/.specify/specs/demo/ref.md        |    3 +
 .../decision-batch/resolution-join/.gitkeep        |    0
 .../decision-batch-b-20261101t000000z-bbbbbbbb.md  |   46 +
 .../resolution-join/.specify/register.md           |    4 +
 .../resolution-join/.specify/specs/demo/ref.md     |    3 +
 .../resolution-join/.specify/specs/demo/settled.md |   17 +
 .../resolution-join/.specify/specs/demo/source.md  |   18 +
 .../decision-batch/source-conflict/.gitkeep        |    0
 tests/fixtures/decision-batch/two-source/.gitkeep  |    0
 .../decision-batch/two-source/.specify/register.md |   10 +
 .../two-source/.specify/specs/demo/evidence-a.md   |    3 +
 .../two-source/.specify/specs/demo/fenced.md       |    7 +
 .../two-source/.specify/specs/demo/pending-a.md    |   21 +
 .../two-source/.specify/specs/demo/pending-b.md    |   21 +
 .../decision-batch/unreadable-register/.gitkeep    |    0
 .../unreadable-register/.specify/register.md       |    3 +
 .../unreadable-register/.specify/specs/demo/one.md |   17 +
 .../unreadable-register/.specify/specs/demo/ref.md |    3 +
 .../decision-batch/unwritable-old-record/.gitkeep  |    0
 .../unwritable-old-record/.specify/register.md     |    4 +
 .../.specify/specs/demo/item.md                    |   21 +
 .../.specify/specs/demo/old-record.md              |   23 +
 tests/unit/test_decision_batch_engine.py           | 1434 +++++++++++++
 339 files changed, 26392 insertions(+), 63 deletions(-)
```

---

## Review 意见


### 🔴 [BLOCKING] scripts/python/decision-batch.py (Line 806)

> FR-020 / C-204 violated in the user-facing body: batch_context renders the closed-roster source ids and the presence token verbatim ('register-open-decision-row 在场状态为 read；authored-pending-item ... read') into the completeness disclosure of every scan. Owner § 用户面标识边界 and C-204 forbid internal identifiers and status tokens in the user-facing body; the structured payload is the machine channel. Fix: map source ids to plain-language source names and presence to plain wording; keep the JSON payload unchanged.

<sub>19:20:19</sub>


### 🔴 [BLOCKING] scripts/python/decision-batch.py (Line 928)

> Same C-204 contract, second locus: state_sentence joins qualification.missing_fields raw, so an item missing a required field prints '缺少必填内容：decision_class' (and context/options/basis/origin/created_at) into the text body. C-202 requires the missing elements be named, C-204 forbids field names in the user-facing body; add a plain-language field-label map (mirroring REASON_TEXT) and render that. Reproduced on tests/fixtures/decision-batch/incomplete-block (items 6-7).

<sub>19:20:19</sub>


### 🟠 [IMPORTANT] tests/contract/test_decision_batch_contract.py (Line 216)

> The C-204 guard is blind to both violations above: INTERNAL_TOKENS omits the roster source ids and the presence token 'read', and the test scans only the two-source fixture, which never enters the missing-field rendering path. The test stays green while the user-facing body leaks machine tokens. Fix: add the source ids and presence words to the token set and scan the incomplete-block and autonomous fixtures as well.

<sub>19:20:24</sub>


### 🟠 [IMPORTANT] scripts/python/decision-batch.py (Line 540)

> Path containment: explicit_repo_path accepts '..' segments after the .specify/ prefix (e.g. '.specify/../../outside/doc.md'), and resolve_pointer likewise accepts '..'. A register row's authority cell can therefore resolve to a carrier outside the workspace and record's build_block_updates/apply_text_update would append a resolution line there, outside the declared write surface. Owner § register↔block linkage requires an explicit repository-relative path. Fix: reject '..' segments and assert the resolved path stays under the workspace root (read side too). Probe: explicit_repo_path('.specify/../../outside/doc.md') is accepted and (root/rel).resolve() lands at /outside/doc.md.

<sub>19:20:24</sub>


### 🟢 [SUGGESTION] scripts/python/decision-batch.py (Line 2042)

> The register reflection is read-modify-write with no locking: two concurrent record calls read the pre-batch register and the later write replaces the earlier batch/decision rows and status cells (lost update). The owner A-26 guarantees only distinct batch-record paths, and test_two_batches_distinct_paths checks only those; the register claim in SC-005 can silently lose one batch under concurrency. Document the single-writer assumption or make the register append atomic before claiming concurrent batch recording.

<sub>19:20:24</sub>


### ❓ [QUESTION] scripts/python/decision-batch.py (Line 490)

> detect_prior_conflict does not skip records already carrying superseded_by, so an old overturned choice can still raise prior-decision-conflict after the superseding record agrees with the current default. The owner § 前例冲突 text says '一条既往决策记录' without excluding superseded records; is the intended reading the latest unsuperseded record, or the literal full history? Please rule; if the former, skip superseded records in both detect_prior_conflict and build_supersession_updates' target scan.

<sub>19:20:24</sub>


### 👍 [PRAISE] scripts/python/decision-batch.py (Line 2004)

> The create-only precondition is judged before the write surface (the candidate id is derived as a pure string and adopted only after every record precondition), and the suite backs it with zero-write snapshots across refusal paths (drift, unattended, membership, duplicate, unwritable prior carrier). This is the refusal discipline SC-001/SC-004/SC-010 needed.

<sub>19:20:24</sub>


<!-- coverage-receipt:begin -->
receipt_version=1
base=c3489e52c597f7937824f728e104ea035a639baf
head=838e7acb4650512bceefd689fec8e0da07c78f6d
base_source=feature-first-commit
renderer=text
changed_files=339
judged_files=19
skipped_files=320
gap_files=0
lines_added=4930
lines_deleted=51
file.001.path=.claude/commands/speckit.decide.md
file.001.verdict=skipped
file.001.reason=generated
file.002.path=.github/prompts/speckit.decide.prompt.md
file.002.verdict=skipped
file.002.reason=generated
file.003.path=.opencode/command/speckit.decide.md
file.003.verdict=skipped
file.003.reason=generated
file.004.path=.qoder/commands/speckit.decide.md
file.004.verdict=skipped
file.004.reason=generated
file.005.path=.specify/exec-quant/records/20261127T082913128534Z-ee9e2990.json
file.005.verdict=skipped
file.005.reason=non-code-file
file.006.path=.specify/exec-quant/records/20261127T084128423634Z-1badf7ac.json
file.006.verdict=skipped
file.006.reason=non-code-file
file.007.path=.specify/exec-quant/records/20261127T085643910002Z-e0a626d6.json
file.007.verdict=skipped
file.007.reason=non-code-file
file.008.path=.specify/exec-quant/records/20261127T090925309265Z-98aed753.json
file.008.verdict=skipped
file.008.reason=non-code-file
file.009.path=.specify/exec-quant/records/20261127T091728386412Z-1b103a03.json
file.009.verdict=skipped
file.009.reason=non-code-file
file.010.path=.specify/exec-quant/records/20261127T092900436577Z-71eaf093.json
file.010.verdict=skipped
file.010.reason=non-code-file
file.011.path=.specify/exec-quant/records/20261127T094641002616Z-09a39250.json
file.011.verdict=skipped
file.011.reason=non-code-file
file.012.path=.specify/exec-quant/records/20261127T100543484163Z-7125b0fa.json
file.012.verdict=skipped
file.012.reason=non-code-file
file.013.path=.specify/features.md
file.013.verdict=reviewed
file.014.path=.specify/features/112-decision-batch-panel.md
file.014.verdict=reviewed
file.015.path=.specify/feedback/20261127T082913Z-speckit-requirements.md
file.015.verdict=skipped
file.015.reason=non-code-file
file.016.path=.specify/feedback/20261127T084128Z-speckit-clarify.md
file.016.verdict=skipped
file.016.reason=non-code-file
file.017.path=.specify/feedback/20261127T085649Z-speckit-plan.md
file.017.verdict=skipped
file.017.reason=non-code-file
file.018.path=.specify/feedback/20261127T090930Z-speckit-tasks.md
file.018.verdict=skipped
file.018.reason=non-code-file
file.019.path=.specify/feedback/20261127T091735Z-speckit-checklist.md
file.019.verdict=skipped
file.019.reason=non-code-file
file.020.path=.specify/feedback/20261127T092907Z-speckit-analyze.md
file.020.verdict=skipped
file.020.reason=non-code-file
file.021.path=.specify/feedback/20261127T094647Z-speckit-analyze.md
file.021.verdict=skipped
file.021.reason=non-code-file
file.022.path=.specify/feedback/20261127T100546Z-speckit-implement.md
file.022.verdict=skipped
file.022.reason=non-code-file
file.023.path=.specify/retention/closeout/20261127T082928Z-r20261127T081500Z-112a-requirements.md
file.023.verdict=skipped
file.023.reason=non-code-file
file.024.path=.specify/retention/closeout/20261127T084136Z-r20261127T081500Z-112a-clarify.md
file.024.verdict=skipped
file.024.reason=non-code-file
file.025.path=.specify/retention/closeout/20261127T085702Z-r20261127T081500Z-112a-plan.md
file.025.verdict=skipped
file.025.reason=non-code-file
file.026.path=.specify/retention/closeout/20261127T091004Z-r20261127T081500Z-112a-tasks.md
file.026.verdict=skipped
file.026.reason=non-code-file
file.027.path=.specify/retention/closeout/20261127T091753Z-r20261127T081500Z-112a-checklist.md
file.027.verdict=skipped
file.027.reason=non-code-file
file.028.path=.specify/retention/closeout/20261127T093023Z-r20261127T081500Z-112a-analyze.md
file.028.verdict=skipped
file.028.reason=non-code-file
file.029.path=.specify/retention/closeout/20261127T094729Z-r20261127T094343Z-112a-analyze.md
file.029.verdict=skipped
file.029.reason=non-code-file
file.030.path=.specify/scripts/python/decision-batch.py
file.030.verdict=skipped
file.030.reason=generated
file.031.path=.specify/scripts/python/validate-decisions.py
file.031.verdict=skipped
file.031.reason=generated
file.032.path=.specify/session/20261127T060910Z-run-determination-speckit-plan-r20261127t053750z-109a.md
file.032.verdict=skipped
file.032.reason=non-code-file
file.033.path=.specify/session/20261127T082907Z-run-determination-speckit-requirements-r20261127t081500z-112.md
file.033.verdict=skipped
file.033.reason=non-code-file
file.034.path=.specify/session/20261127T084111Z-run-determination-speckit-clarify-r20261127t081500z-112a.md
file.034.verdict=skipped
file.034.reason=non-code-file
file.035.path=.specify/session/20261127T085626Z-run-determination-speckit-plan-r20261127t081500z-112a.md
file.035.verdict=skipped
file.035.reason=non-code-file
file.036.path=.specify/session/20261127T090922Z-run-determination-speckit-tasks-r20261127t081500z-112a.md
file.036.verdict=skipped
file.036.reason=non-code-file
file.037.path=.specify/session/20261127T091725Z-run-determination-speckit-checklist-r20261127t081500z-112a.md
file.037.verdict=skipped
file.037.reason=non-code-file
file.038.path=.specify/session/20261127T092849Z-run-determination-speckit-analyze-r20261127t081500z-112a.md
file.038.verdict=skipped
file.038.reason=non-code-file
file.039.path=.specify/session/20261127T094640Z-run-determination-speckit-analyze-r20261127t094343z-112a.md
file.039.verdict=skipped
file.039.reason=non-code-file
file.040.path=.specify/session/20261127T100532Z-run-determination-speckit-implement-r20261127t081500z-112a.md
file.040.verdict=skipped
file.040.reason=non-code-file
file.041.path=.specify/shared/definitions/decision-definitions.md
file.041.verdict=skipped
file.041.reason=generated
file.042.path=.specify/shared/definitions/flow-class-definitions.md
file.042.verdict=skipped
file.042.reason=generated
file.043.path=.specify/shared/definitions/framework-map.md
file.043.verdict=skipped
file.043.reason=generated
file.044.path=.specify/shared/definitions/probe-definitions.md
file.044.verdict=skipped
file.044.reason=generated
file.045.path=.specify/skills/internal/decide-batch/SKILL.md
file.045.verdict=skipped
file.045.reason=generated
file.046.path=.specify/specs/112-decision-batch-panel/checklists/requirements-quality-2026-11-27.md
file.046.verdict=skipped
file.046.reason=non-code-file
file.047.path=.specify/specs/112-decision-batch-panel/checklists/requirements.md
file.047.verdict=skipped
file.047.reason=non-code-file
file.048.path=.specify/specs/112-decision-batch-panel/checkpoints/01-requirements.md
file.048.verdict=skipped
file.048.reason=non-code-file
file.049.path=.specify/specs/112-decision-batch-panel/checkpoints/02-clarify.md
file.049.verdict=skipped
file.049.reason=non-code-file
file.050.path=.specify/specs/112-decision-batch-panel/checkpoints/03-plan.md
file.050.verdict=skipped
file.050.reason=non-code-file
file.051.path=.specify/specs/112-decision-batch-panel/checkpoints/04-tasks.md
file.051.verdict=skipped
file.051.reason=non-code-file
file.052.path=.specify/specs/112-decision-batch-panel/checkpoints/05-checklist.md
file.052.verdict=skipped
file.052.reason=non-code-file
file.053.path=.specify/specs/112-decision-batch-panel/checkpoints/06-analyze.md
file.053.verdict=skipped
file.053.reason=non-code-file
file.054.path=.specify/specs/112-decision-batch-panel/checkpoints/07-implement.md
file.054.verdict=skipped
file.054.reason=non-code-file
file.055.path=.specify/specs/112-decision-batch-panel/contracts/completeness-refusal.contract.md
file.055.verdict=skipped
file.055.reason=non-code-file
file.056.path=.specify/specs/112-decision-batch-panel/contracts/default-derivation.contract.md
file.056.verdict=skipped
file.056.reason=non-code-file
file.057.path=.specify/specs/112-decision-batch-panel/contracts/objection-reply.contract.md
file.057.verdict=skipped
file.057.reason=non-code-file
file.058.path=.specify/specs/112-decision-batch-panel/contracts/presentation.contract.md
file.058.verdict=skipped
file.058.reason=non-code-file
file.059.path=.specify/specs/112-decision-batch-panel/contracts/record-replay.contract.md
file.059.verdict=skipped
file.059.reason=non-code-file
file.060.path=.specify/specs/112-decision-batch-panel/contracts/source-roster.contract.md
file.060.verdict=skipped
file.060.reason=non-code-file
file.061.path=.specify/specs/112-decision-batch-panel/coverage-baseline.txt
file.061.verdict=skipped
file.061.reason=non-code-file
file.062.path=.specify/specs/112-decision-batch-panel/data-model.md
file.062.verdict=skipped
file.062.reason=non-code-file
file.063.path=.specify/specs/112-decision-batch-panel/feature-ref.md
file.063.verdict=skipped
file.063.reason=non-code-file
file.064.path=.specify/specs/112-decision-batch-panel/notes/pre-change-measurements.md
file.064.verdict=skipped
file.064.reason=non-code-file
file.065.path=.specify/specs/112-decision-batch-panel/notes/quickstart-run.md
file.065.verdict=skipped
file.065.reason=non-code-file
file.066.path=.specify/specs/112-decision-batch-panel/notes/red-first-evidence.md
file.066.verdict=skipped
file.066.reason=non-code-file
file.067.path=.specify/specs/112-decision-batch-panel/notes/red-first-names-us2-contract.txt
file.067.verdict=skipped
file.067.reason=non-code-file
file.068.path=.specify/specs/112-decision-batch-panel/notes/red-first-names-us2.txt
file.068.verdict=skipped
file.068.reason=non-code-file
file.069.path=.specify/specs/112-decision-batch-panel/notes/red-first-names-us3.txt
file.069.verdict=skipped
file.069.reason=non-code-file
file.070.path=.specify/specs/112-decision-batch-panel/notes/red-first-names-us4.txt
file.070.verdict=skipped
file.070.reason=non-code-file
file.071.path=.specify/specs/112-decision-batch-panel/notes/red-first-names-us5.txt
file.071.verdict=skipped
file.071.reason=non-code-file
file.072.path=.specify/specs/112-decision-batch-panel/notes/red-first-names.txt
file.072.verdict=skipped
file.072.reason=non-code-file
file.073.path=.specify/specs/112-decision-batch-panel/notes/us1-green.txt
file.073.verdict=skipped
file.073.reason=non-code-file
file.074.path=.specify/specs/112-decision-batch-panel/notes/us2-green.txt
file.074.verdict=skipped
file.074.reason=non-code-file
file.075.path=.specify/specs/112-decision-batch-panel/notes/us3-green.txt
file.075.verdict=skipped
file.075.reason=non-code-file
file.076.path=.specify/specs/112-decision-batch-panel/notes/us4-green.txt
file.076.verdict=skipped
file.076.reason=non-code-file
file.077.path=.specify/specs/112-decision-batch-panel/notes/us5-green.txt
file.077.verdict=skipped
file.077.reason=non-code-file
file.078.path=.specify/specs/112-decision-batch-panel/plan.md
file.078.verdict=skipped
file.078.reason=non-code-file
file.079.path=.specify/specs/112-decision-batch-panel/quickstart.md
file.079.verdict=skipped
file.079.reason=non-code-file
file.080.path=.specify/specs/112-decision-batch-panel/requirements.md
file.080.verdict=skipped
file.080.reason=non-code-file
file.081.path=.specify/specs/112-decision-batch-panel/research.md
file.081.verdict=skipped
file.081.reason=non-code-file
file.082.path=.specify/specs/112-decision-batch-panel/tasks.md
file.082.verdict=skipped
file.082.reason=non-code-file
file.083.path=.specify/specs/112-decision-batch-panel/test-evidence/analyze-exec-quant.txt
file.083.verdict=skipped
file.083.reason=non-code-file
file.084.path=.specify/specs/112-decision-batch-panel/test-evidence/analyze-feedback-record.txt
file.084.verdict=skipped
file.084.reason=non-code-file
file.085.path=.specify/specs/112-decision-batch-panel/test-evidence/analyze-repair-pre-analyze-tasks.json
file.085.verdict=skipped
file.085.reason=non-code-file
file.086.path=.specify/specs/112-decision-batch-panel/test-evidence/analyze-repair-pre-analyze-tasks.txt
file.086.verdict=skipped
file.086.reason=non-code-file
file.087.path=.specify/specs/112-decision-batch-panel/test-evidence/analyze-repair-round1.md
file.087.verdict=skipped
file.087.reason=non-code-file
file.088.path=.specify/specs/112-decision-batch-panel/test-evidence/analyze-repair-validate-requirements.txt
file.088.verdict=skipped
file.088.reason=non-code-file
file.089.path=.specify/specs/112-decision-batch-panel/test-evidence/analyze-repair-validate-tasks.txt
file.089.verdict=skipped
file.089.reason=non-code-file
file.090.path=.specify/specs/112-decision-batch-panel/test-evidence/analyze-round1-findings.jsonl
file.090.verdict=skipped
file.090.reason=non-code-file
file.091.path=.specify/specs/112-decision-batch-panel/test-evidence/analyze-round1-report.md
file.091.verdict=skipped
file.091.reason=non-code-file
file.092.path=.specify/specs/112-decision-batch-panel/test-evidence/analyze-round2-exec-quant.txt
file.092.verdict=skipped
file.092.reason=non-code-file
file.093.path=.specify/specs/112-decision-batch-panel/test-evidence/analyze-round2-feedback-record.txt
file.093.verdict=skipped
file.093.reason=non-code-file
file.094.path=.specify/specs/112-decision-batch-panel/test-evidence/analyze-round2-findings.jsonl
file.094.verdict=skipped
file.094.reason=non-code-file
file.095.path=.specify/specs/112-decision-batch-panel/test-evidence/analyze-round2-gates.txt
file.095.verdict=skipped
file.095.reason=non-code-file
file.096.path=.specify/specs/112-decision-batch-panel/test-evidence/analyze-round2-report.md
file.096.verdict=skipped
file.096.reason=non-code-file
file.097.path=.specify/specs/112-decision-batch-panel/test-evidence/analyze-round2-run-determination.txt
file.097.verdict=skipped
file.097.reason=non-code-file
file.098.path=.specify/specs/112-decision-batch-panel/test-evidence/analyze-run-determination.txt
file.098.verdict=skipped
file.098.reason=non-code-file
file.099.path=.specify/specs/112-decision-batch-panel/test-evidence/checklist-exec-quant.txt
file.099.verdict=skipped
file.099.reason=non-code-file
file.100.path=.specify/specs/112-decision-batch-panel/test-evidence/checklist-feedback-record.txt
file.100.verdict=skipped
file.100.reason=non-code-file
file.101.path=.specify/specs/112-decision-batch-panel/test-evidence/checklist-requirements-validator.txt
file.101.verdict=skipped
file.101.reason=non-code-file
file.102.path=.specify/specs/112-decision-batch-panel/test-evidence/checklist-run-determination.txt
file.102.verdict=skipped
file.102.reason=non-code-file
file.103.path=.specify/specs/112-decision-batch-panel/test-evidence/checklist-selfcheck.txt
file.103.verdict=skipped
file.103.reason=non-code-file
file.104.path=.specify/specs/112-decision-batch-panel/test-evidence/checklist-spec-readings.txt
file.104.verdict=skipped
file.104.reason=non-code-file
file.105.path=.specify/specs/112-decision-batch-panel/test-evidence/checklist-stage-2026-11-27.md
file.105.verdict=skipped
file.105.reason=non-code-file
file.106.path=.specify/specs/112-decision-batch-panel/test-evidence/clarify-exec-quant.txt
file.106.verdict=skipped
file.106.reason=non-code-file
file.107.path=.specify/specs/112-decision-batch-panel/test-evidence/clarify-feedback-record.txt
file.107.verdict=skipped
file.107.reason=non-code-file
file.108.path=.specify/specs/112-decision-batch-panel/test-evidence/clarify-roster-measure.txt
file.108.verdict=skipped
file.108.reason=non-code-file
file.109.path=.specify/specs/112-decision-batch-panel/test-evidence/clarify-run-determination.txt
file.109.verdict=skipped
file.109.reason=non-code-file
file.110.path=.specify/specs/112-decision-batch-panel/test-evidence/clarify-stage-2026-11-27.md
file.110.verdict=skipped
file.110.reason=non-code-file
file.111.path=.specify/specs/112-decision-batch-panel/test-evidence/clarify-validator-after.txt
file.111.verdict=skipped
file.111.reason=non-code-file
file.112.path=.specify/specs/112-decision-batch-panel/test-evidence/clarify-validator-before.txt
file.112.verdict=skipped
file.112.reason=non-code-file
file.113.path=.specify/specs/112-decision-batch-panel/test-evidence/clarify-validator-postcommit.txt
file.113.verdict=skipped
file.113.reason=non-code-file
file.114.path=.specify/specs/112-decision-batch-panel/test-evidence/closure-acceptance-2026-11-27.json
file.114.verdict=skipped
file.114.reason=non-code-file
file.115.path=.specify/specs/112-decision-batch-panel/test-evidence/decomposition-requirements-postcommit.json
file.115.verdict=skipped
file.115.reason=non-code-file
file.116.path=.specify/specs/112-decision-batch-panel/test-evidence/decomposition-requirements-postcommit.txt
file.116.verdict=skipped
file.116.reason=non-code-file
file.117.path=.specify/specs/112-decision-batch-panel/test-evidence/decomposition-requirements.json
file.117.verdict=skipped
file.117.reason=non-code-file
file.118.path=.specify/specs/112-decision-batch-panel/test-evidence/decomposition-requirements.txt
file.118.verdict=skipped
file.118.reason=non-code-file
file.119.path=.specify/specs/112-decision-batch-panel/test-evidence/decomposition-tasks.json
file.119.verdict=skipped
file.119.reason=non-code-file
file.120.path=.specify/specs/112-decision-batch-panel/test-evidence/decomposition-tasks.txt
file.120.verdict=skipped
file.120.reason=non-code-file
file.121.path=.specify/specs/112-decision-batch-panel/test-evidence/implement-p1-baseline-failed.txt
file.121.verdict=skipped
file.121.reason=non-code-file
file.122.path=.specify/specs/112-decision-batch-panel/test-evidence/implement-p1-exec-quant.txt
file.122.verdict=skipped
file.122.reason=non-code-file
file.123.path=.specify/specs/112-decision-batch-panel/test-evidence/implement-p1-feedback-record.txt
file.123.verdict=skipped
file.123.reason=non-code-file
file.124.path=.specify/specs/112-decision-batch-panel/test-evidence/implement-p1-run-determination.txt
file.124.verdict=skipped
file.124.reason=non-code-file
file.125.path=.specify/specs/112-decision-batch-panel/test-evidence/implement-p1-stage-2026-11-27.md
file.125.verdict=skipped
file.125.reason=non-code-file
file.126.path=.specify/specs/112-decision-batch-panel/test-evidence/implement-p2-exec-quant.txt
file.126.verdict=skipped
file.126.reason=non-code-file
file.127.path=.specify/specs/112-decision-batch-panel/test-evidence/implement-p2-feedback-record.txt
file.127.verdict=skipped
file.127.reason=non-code-file
file.128.path=.specify/specs/112-decision-batch-panel/test-evidence/implement-p2-run-determination.txt
file.128.verdict=skipped
file.128.reason=non-code-file
file.129.path=.specify/specs/112-decision-batch-panel/test-evidence/implement-p2-stage-2026-11-27.md
file.129.verdict=skipped
file.129.reason=non-code-file
file.130.path=.specify/specs/112-decision-batch-panel/test-evidence/implement-p3-exec-quant.txt
file.130.verdict=skipped
file.130.reason=non-code-file
file.131.path=.specify/specs/112-decision-batch-panel/test-evidence/implement-p3-feedback-record.txt
file.131.verdict=skipped
file.131.reason=non-code-file
file.132.path=.specify/specs/112-decision-batch-panel/test-evidence/implement-p3-run-determination.txt
file.132.verdict=skipped
file.132.reason=non-code-file
file.133.path=.specify/specs/112-decision-batch-panel/test-evidence/implement-p3-stage-2026-11-27.md
file.133.verdict=skipped
file.133.reason=non-code-file
file.134.path=.specify/specs/112-decision-batch-panel/test-evidence/implement-p4-exec-quant.txt
file.134.verdict=skipped
file.134.reason=non-code-file
file.135.path=.specify/specs/112-decision-batch-panel/test-evidence/implement-p4-feedback-record.txt
file.135.verdict=skipped
file.135.reason=non-code-file
file.136.path=.specify/specs/112-decision-batch-panel/test-evidence/implement-p4-full-suite-baseline-names.txt
file.136.verdict=skipped
file.136.reason=non-code-file
file.137.path=.specify/specs/112-decision-batch-panel/test-evidence/implement-p4-full-suite-names.txt
file.137.verdict=skipped
file.137.reason=non-code-file
file.138.path=.specify/specs/112-decision-batch-panel/test-evidence/implement-p4-full-suite.txt
file.138.verdict=skipped
file.138.reason=non-code-file
file.139.path=.specify/specs/112-decision-batch-panel/test-evidence/implement-p4-gates.txt
file.139.verdict=skipped
file.139.reason=non-code-file
file.140.path=.specify/specs/112-decision-batch-panel/test-evidence/implement-p4-regression-names.txt
file.140.verdict=skipped
file.140.reason=non-code-file
file.141.path=.specify/specs/112-decision-batch-panel/test-evidence/implement-p4-run-determination.txt
file.141.verdict=skipped
file.141.reason=non-code-file
file.142.path=.specify/specs/112-decision-batch-panel/test-evidence/implement-p4-stage-2026-11-27.md
file.142.verdict=skipped
file.142.reason=non-code-file
file.143.path=.specify/specs/112-decision-batch-panel/test-evidence/plan-exec-quant.txt
file.143.verdict=skipped
file.143.reason=non-code-file
file.144.path=.specify/specs/112-decision-batch-panel/test-evidence/plan-feedback-record.txt
file.144.verdict=skipped
file.144.reason=non-code-file
file.145.path=.specify/specs/112-decision-batch-panel/test-evidence/plan-integrity-postcommit.txt
file.145.verdict=skipped
file.145.reason=non-code-file
file.146.path=.specify/specs/112-decision-batch-panel/test-evidence/plan-integrity.txt
file.146.verdict=skipped
file.146.reason=non-code-file
file.147.path=.specify/specs/112-decision-batch-panel/test-evidence/plan-run-determination.txt
file.147.verdict=skipped
file.147.reason=non-code-file
file.148.path=.specify/specs/112-decision-batch-panel/test-evidence/plan-stage-2026-11-27.md
file.148.verdict=skipped
file.148.reason=non-code-file
file.149.path=.specify/specs/112-decision-batch-panel/test-evidence/plan-tensions.txt
file.149.verdict=skipped
file.149.reason=non-code-file
file.150.path=.specify/specs/112-decision-batch-panel/test-evidence/pre-analyze-checklist.txt
file.150.verdict=skipped
file.150.reason=non-code-file
file.151.path=.specify/specs/112-decision-batch-panel/test-evidence/pre-analyze-plan.json
file.151.verdict=skipped
file.151.reason=non-code-file
file.152.path=.specify/specs/112-decision-batch-panel/test-evidence/pre-analyze-plan.txt
file.152.verdict=skipped
file.152.reason=non-code-file
file.153.path=.specify/specs/112-decision-batch-panel/test-evidence/pre-analyze-requirements-postcommit.json
file.153.verdict=skipped
file.153.reason=non-code-file
file.154.path=.specify/specs/112-decision-batch-panel/test-evidence/pre-analyze-requirements-postcommit.txt
file.154.verdict=skipped
file.154.reason=non-code-file
file.155.path=.specify/specs/112-decision-batch-panel/test-evidence/pre-analyze-requirements.json
file.155.verdict=skipped
file.155.reason=non-code-file
file.156.path=.specify/specs/112-decision-batch-panel/test-evidence/pre-analyze-requirements.txt
file.156.verdict=skipped
file.156.reason=non-code-file
file.157.path=.specify/specs/112-decision-batch-panel/test-evidence/pre-analyze-tasks-p4.txt
file.157.verdict=skipped
file.157.reason=non-code-file
file.158.path=.specify/specs/112-decision-batch-panel/test-evidence/pre-analyze-tasks.json
file.158.verdict=skipped
file.158.reason=non-code-file
file.159.path=.specify/specs/112-decision-batch-panel/test-evidence/pre-analyze-tasks.txt
file.159.verdict=skipped
file.159.reason=non-code-file
file.160.path=.specify/specs/112-decision-batch-panel/test-evidence/requirements-exec-quant.txt
file.160.verdict=skipped
file.160.reason=non-code-file
file.161.path=.specify/specs/112-decision-batch-panel/test-evidence/requirements-feedback-record.txt
file.161.verdict=skipped
file.161.reason=non-code-file
file.162.path=.specify/specs/112-decision-batch-panel/test-evidence/requirements-run-determination.txt
file.162.verdict=skipped
file.162.reason=non-code-file
file.163.path=.specify/specs/112-decision-batch-panel/test-evidence/requirements-stage-2026-11-27.md
file.163.verdict=skipped
file.163.reason=non-code-file
file.164.path=.specify/specs/112-decision-batch-panel/test-evidence/requirements-validator-postcommit.txt
file.164.verdict=skipped
file.164.reason=non-code-file
file.165.path=.specify/specs/112-decision-batch-panel/test-evidence/requirements-validator.txt
file.165.verdict=skipped
file.165.reason=non-code-file
file.166.path=.specify/specs/112-decision-batch-panel/test-evidence/scan-confirmation-gates-baseline.txt
file.166.verdict=skipped
file.166.reason=non-code-file
file.167.path=.specify/specs/112-decision-batch-panel/test-evidence/tasks-exec-quant.txt
file.167.verdict=skipped
file.167.reason=non-code-file
file.168.path=.specify/specs/112-decision-batch-panel/test-evidence/tasks-feedback-record.txt
file.168.verdict=skipped
file.168.reason=non-code-file
file.169.path=.specify/specs/112-decision-batch-panel/test-evidence/tasks-run-determination.txt
file.169.verdict=skipped
file.169.reason=non-code-file
file.170.path=.specify/specs/112-decision-batch-panel/test-evidence/tasks-stage-2026-11-27.md
file.170.verdict=skipped
file.170.reason=non-code-file
file.171.path=.specify/specs/112-decision-batch-panel/test-evidence/tasks-validator-p4.txt
file.171.verdict=skipped
file.171.reason=non-code-file
file.172.path=.specify/specs/112-decision-batch-panel/test-evidence/tasks-validator.txt
file.172.verdict=skipped
file.172.reason=non-code-file
file.173.path=.specify/specs/112-decision-batch-panel/test-evidence/verification-input.md
file.173.verdict=skipped
file.173.reason=non-code-file
file.174.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-analyze-readings.txt
file.174.verdict=skipped
file.174.reason=non-code-file
file.175.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-analyze-repair-readings.txt
file.175.verdict=skipped
file.175.reason=non-code-file
file.176.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-analyze-repair.json
file.176.verdict=skipped
file.176.reason=non-code-file
file.177.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-analyze.json
file.177.verdict=skipped
file.177.reason=non-code-file
file.178.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-checklist-postcommit.json
file.178.verdict=skipped
file.178.reason=non-code-file
file.179.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-checklist-readings.txt
file.179.verdict=skipped
file.179.reason=non-code-file
file.180.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-checklist.json
file.180.verdict=skipped
file.180.reason=non-code-file
file.181.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-clarify-check.txt
file.181.verdict=skipped
file.181.reason=non-code-file
file.182.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-clarify-postcommit.json
file.182.verdict=skipped
file.182.reason=non-code-file
file.183.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-clarify-postcommit.txt
file.183.verdict=skipped
file.183.reason=non-code-file
file.184.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-clarify.json
file.184.verdict=skipped
file.184.reason=non-code-file
file.185.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-implement-p1-check.txt
file.185.verdict=skipped
file.185.reason=non-code-file
file.186.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-implement-p1.json
file.186.verdict=skipped
file.186.reason=non-code-file
file.187.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-implement-p2-check.txt
file.187.verdict=skipped
file.187.reason=non-code-file
file.188.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-implement-p2.json
file.188.verdict=skipped
file.188.reason=non-code-file
file.189.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-implement-p3-check.txt
file.189.verdict=skipped
file.189.reason=non-code-file
file.190.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-implement-p3.json
file.190.verdict=skipped
file.190.reason=non-code-file
file.191.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-implement-p4-check.txt
file.191.verdict=skipped
file.191.reason=non-code-file
file.192.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-implement-p4.json
file.192.verdict=skipped
file.192.reason=non-code-file
file.193.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-plan-check.txt
file.193.verdict=skipped
file.193.reason=non-code-file
file.194.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-plan-postcommit.json
file.194.verdict=skipped
file.194.reason=non-code-file
file.195.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-plan-postcommit.txt
file.195.verdict=skipped
file.195.reason=non-code-file
file.196.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-plan.json
file.196.verdict=skipped
file.196.reason=non-code-file
file.197.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-requirements-check.txt
file.197.verdict=skipped
file.197.reason=non-code-file
file.198.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-requirements-postcommit.json
file.198.verdict=skipped
file.198.reason=non-code-file
file.199.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-requirements-postcommit.txt
file.199.verdict=skipped
file.199.reason=non-code-file
file.200.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-requirements.json
file.200.verdict=skipped
file.200.reason=non-code-file
file.201.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-tasks-check.txt
file.201.verdict=skipped
file.201.reason=non-code-file
file.202.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-tasks-postcommit.json
file.202.verdict=skipped
file.202.reason=non-code-file
file.203.path=.specify/specs/112-decision-batch-panel/test-evidence/workspace-tasks.json
file.203.verdict=skipped
file.203.reason=non-code-file
file.204.path=.specify/specs/112-decision-batch-panel/verification.md
file.204.verdict=skipped
file.204.reason=non-code-file
file.205.path=.specify/trigger/index.json
file.205.verdict=skipped
file.205.reason=generated
file.206.path=docs/reference/commands/decide.md
file.206.verdict=skipped
file.206.reason=non-code-file
file.207.path=scripts/python/decision-batch.py
file.207.verdict=reviewed
file.208.path=scripts/python/validate-decisions.py
file.208.verdict=reviewed
file.209.path=shared/definitions/decision-definitions.md
file.209.verdict=reviewed
file.210.path=shared/definitions/flow-class-definitions.md
file.210.verdict=reviewed
file.211.path=shared/definitions/framework-map.md
file.211.verdict=reviewed
file.212.path=shared/definitions/probe-definitions.md
file.212.verdict=reviewed
file.213.path=skills/internal/decide-batch/SKILL.md
file.213.verdict=reviewed
file.214.path=templates/commands/decide.md
file.214.verdict=reviewed
file.215.path=tests/contract/test_decision_batch_contract.py
file.215.verdict=reviewed
file.216.path=tests/contract/test_decision_governance_contracts.py
file.216.verdict=reviewed
file.217.path=tests/contract/test_decision_governance_guards.py
file.217.verdict=reviewed
file.218.path=tests/contract/test_flow_class_ledger.py
file.218.verdict=reviewed
file.219.path=tests/contract/test_humanize_command_surface.py
file.219.verdict=reviewed
file.220.path=tests/contract/test_migrate_distribution_assembly.py
file.220.verdict=reviewed
file.221.path=tests/contract/test_migration_distribution.py
file.221.verdict=reviewed
file.222.path=tests/contract/test_probe_nonentity_catalog.py
file.222.verdict=reviewed
file.223.path=tests/fixtures/decision-batch/absent-root/.gitkeep
file.223.verdict=skipped
file.223.reason=non-code-file
file.224.path=tests/fixtures/decision-batch/absent-root/.specify/register.md
file.224.verdict=skipped
file.224.reason=non-code-file
file.225.path=tests/fixtures/decision-batch/absent-root/.specify/specs/demo/one.md
file.225.verdict=skipped
file.225.reason=non-code-file
file.226.path=tests/fixtures/decision-batch/absent-root/.specify/specs/demo/ref.md
file.226.verdict=skipped
file.226.reason=non-code-file
file.227.path=tests/fixtures/decision-batch/autonomous/.gitkeep
file.227.verdict=skipped
file.227.reason=non-code-file
file.228.path=tests/fixtures/decision-batch/autonomous/.specify/register.md
file.228.verdict=skipped
file.228.reason=non-code-file
file.229.path=tests/fixtures/decision-batch/autonomous/.specify/specs/demo/auto-evidence.md
file.229.verdict=skipped
file.229.reason=non-code-file
file.230.path=tests/fixtures/decision-batch/autonomous/.specify/specs/demo/auto.md
file.230.verdict=skipped
file.230.reason=non-code-file
file.231.path=tests/fixtures/decision-batch/batch-family/.gitkeep
file.231.verdict=skipped
file.231.reason=non-code-file
file.232.path=tests/fixtures/decision-batch/batch-family/.specify/register.md
file.232.verdict=skipped
file.232.reason=non-code-file
file.233.path=tests/fixtures/decision-batch/batch-family/.specify/specs/demo/household.md
file.233.verdict=skipped
file.233.reason=non-code-file
file.234.path=tests/fixtures/decision-batch/batch-family/.specify/specs/demo/ref.md
file.234.verdict=skipped
file.234.reason=non-code-file
file.235.path=tests/fixtures/decision-batch/class-conflict/.gitkeep
file.235.verdict=skipped
file.235.reason=non-code-file
file.236.path=tests/fixtures/decision-batch/class-conflict/.specify/register.md
file.236.verdict=skipped
file.236.reason=non-code-file
file.237.path=tests/fixtures/decision-batch/class-conflict/.specify/specs/demo/conflict-a.md
file.237.verdict=skipped
file.237.reason=non-code-file
file.238.path=tests/fixtures/decision-batch/class-conflict/.specify/specs/demo/conflict-b.md
file.238.verdict=skipped
file.238.reason=non-code-file
file.239.path=tests/fixtures/decision-batch/class-conflict/.specify/specs/demo/ref.md
file.239.verdict=skipped
file.239.reason=non-code-file
file.240.path=tests/fixtures/decision-batch/concurrency/.specify/register.md
file.240.verdict=skipped
file.240.reason=non-code-file
file.241.path=tests/fixtures/decision-batch/concurrency/.specify/specs/demo/ref.md
file.241.verdict=skipped
file.241.reason=non-code-file
file.242.path=tests/fixtures/decision-batch/concurrency/.specify/specs/demo/two-batches.md
file.242.verdict=skipped
file.242.reason=non-code-file
file.243.path=tests/fixtures/decision-batch/drift/.gitkeep
file.243.verdict=skipped
file.243.reason=non-code-file
file.244.path=tests/fixtures/decision-batch/drift/.specify/register.md
file.244.verdict=skipped
file.244.reason=non-code-file
file.245.path=tests/fixtures/decision-batch/drift/.specify/specs/demo/ref.md
file.245.verdict=skipped
file.245.reason=non-code-file
file.246.path=tests/fixtures/decision-batch/drift/.specify/specs/demo/two.md
file.246.verdict=skipped
file.246.reason=non-code-file
file.247.path=tests/fixtures/decision-batch/eligibility-matrix/.gitkeep
file.247.verdict=skipped
file.247.reason=non-code-file
file.248.path=tests/fixtures/decision-batch/eligibility-matrix/.specify/register.md
file.248.verdict=skipped
file.248.reason=non-code-file
file.249.path=tests/fixtures/decision-batch/eligibility-matrix/.specify/specs/demo/matrix.md
file.249.verdict=skipped
file.249.reason=non-code-file
file.250.path=tests/fixtures/decision-batch/eligibility-matrix/.specify/specs/demo/prior.md
file.250.verdict=skipped
file.250.reason=non-code-file
file.251.path=tests/fixtures/decision-batch/eligibility-matrix/.specify/specs/demo/ref.md
file.251.verdict=skipped
file.251.reason=non-code-file
file.252.path=tests/fixtures/decision-batch/empty-project/.gitkeep
file.252.verdict=skipped
file.252.reason=non-code-file
file.253.path=tests/fixtures/decision-batch/grounding-grounded/.gitkeep
file.253.verdict=skipped
file.253.reason=non-code-file
file.254.path=tests/fixtures/decision-batch/grounding-grounded/.specify/register.md
file.254.verdict=skipped
file.254.reason=non-code-file
file.255.path=tests/fixtures/decision-batch/grounding-grounded/.specify/specs/demo/grounded.md
file.255.verdict=skipped
file.255.reason=non-code-file
file.256.path=tests/fixtures/decision-batch/grounding-grounded/.specify/specs/demo/prior-records.md
file.256.verdict=skipped
file.256.reason=non-code-file
file.257.path=tests/fixtures/decision-batch/grounding-none/.gitkeep
file.257.verdict=skipped
file.257.reason=non-code-file
file.258.path=tests/fixtures/decision-batch/grounding-none/.specify/register.md
file.258.verdict=skipped
file.258.reason=non-code-file
file.259.path=tests/fixtures/decision-batch/grounding-none/.specify/specs/demo/no-evidence.md
file.259.verdict=skipped
file.259.reason=non-code-file
file.260.path=tests/fixtures/decision-batch/grounding-none/.specify/specs/demo/notes.md
file.260.verdict=skipped
file.260.reason=non-code-file
file.261.path=tests/fixtures/decision-batch/incomplete-block/.gitkeep
file.261.verdict=skipped
file.261.reason=non-code-file
file.262.path=tests/fixtures/decision-batch/incomplete-block/.specify/register.md
file.262.verdict=skipped
file.262.reason=non-code-file
file.263.path=tests/fixtures/decision-batch/incomplete-block/.specify/specs/demo/ambiguous.md
file.263.verdict=skipped
file.263.reason=non-code-file
file.264.path=tests/fixtures/decision-batch/incomplete-block/.specify/specs/demo/defects.md
file.264.verdict=skipped
file.264.reason=non-code-file
file.265.path=tests/fixtures/decision-batch/incomplete-block/.specify/specs/demo/incomplete.md
file.265.verdict=skipped
file.265.reason=non-code-file
file.266.path=tests/fixtures/decision-batch/incomplete-block/.specify/specs/demo/no-default.md
file.266.verdict=skipped
file.266.reason=non-code-file
file.267.path=tests/fixtures/decision-batch/incomplete-block/.specify/specs/demo/ref.md
file.267.verdict=skipped
file.267.reason=non-code-file
file.268.path=tests/fixtures/decision-batch/m10/.gitkeep
file.268.verdict=skipped
file.268.reason=non-code-file
file.269.path=tests/fixtures/decision-batch/m10/.specify/register.md
file.269.verdict=skipped
file.269.reason=non-code-file
file.270.path=tests/fixtures/decision-batch/m11/.gitkeep
file.270.verdict=skipped
file.270.reason=non-code-file
file.271.path=tests/fixtures/decision-batch/m11/.specify/register.md
file.271.verdict=skipped
file.271.reason=non-code-file
file.272.path=tests/fixtures/decision-batch/m11/.specify/specs/demo/defect.md
file.272.verdict=skipped
file.272.reason=non-code-file
file.273.path=tests/fixtures/decision-batch/m11/.specify/specs/demo/ref.md
file.273.verdict=skipped
file.273.reason=non-code-file
file.274.path=tests/fixtures/decision-batch/m12/.gitkeep
file.274.verdict=skipped
file.274.reason=non-code-file
file.275.path=tests/fixtures/decision-batch/m12/.specify/register.md
file.275.verdict=skipped
file.275.reason=non-code-file
file.276.path=tests/fixtures/decision-batch/m12/.specify/specs/demo/mix.md
file.276.verdict=skipped
file.276.reason=non-code-file
file.277.path=tests/fixtures/decision-batch/m12/.specify/specs/demo/ref.md
file.277.verdict=skipped
file.277.reason=non-code-file
file.278.path=tests/fixtures/decision-batch/m13/.gitkeep
file.278.verdict=skipped
file.278.reason=non-code-file
file.279.path=tests/fixtures/decision-batch/m13/.specify/register.md
file.279.verdict=skipped
file.279.reason=non-code-file
file.280.path=tests/fixtures/decision-batch/m13/.specify/specs/demo/item.md
file.280.verdict=skipped
file.280.reason=non-code-file
file.281.path=tests/fixtures/decision-batch/m13/.specify/specs/demo/prior.md
file.281.verdict=skipped
file.281.reason=non-code-file
file.282.path=tests/fixtures/decision-batch/m14/.gitkeep
file.282.verdict=skipped
file.282.reason=non-code-file
file.283.path=tests/fixtures/decision-batch/m14/.specify/register.md
file.283.verdict=skipped
file.283.reason=non-code-file
file.284.path=tests/fixtures/decision-batch/m14/.specify/specs/demo/item.md
file.284.verdict=skipped
file.284.reason=non-code-file
file.285.path=tests/fixtures/decision-batch/m14/.specify/specs/demo/ref.md
file.285.verdict=skipped
file.285.reason=non-code-file
file.286.path=tests/fixtures/decision-batch/m14/reply.md
file.286.verdict=skipped
file.286.reason=non-code-file
file.287.path=tests/fixtures/decision-batch/m14/scan.json
file.287.verdict=skipped
file.287.reason=non-code-file
file.288.path=tests/fixtures/decision-batch/m15/.gitkeep
file.288.verdict=skipped
file.288.reason=non-code-file
file.289.path=tests/fixtures/decision-batch/m15/.specify/knowledge/decision-batch-b-20261127t105123z-752792b7.md
file.289.verdict=skipped
file.289.reason=non-code-file
file.290.path=tests/fixtures/decision-batch/m15/.specify/register.md
file.290.verdict=skipped
file.290.reason=non-code-file
file.291.path=tests/fixtures/decision-batch/m15/.specify/specs/demo/item.md
file.291.verdict=skipped
file.291.reason=non-code-file
file.292.path=tests/fixtures/decision-batch/m15/.specify/specs/demo/ref.md
file.292.verdict=skipped
file.292.reason=non-code-file
file.293.path=tests/fixtures/decision-batch/m15/reply.md
file.293.verdict=skipped
file.293.reason=non-code-file
file.294.path=tests/fixtures/decision-batch/m15/scan.json
file.294.verdict=skipped
file.294.reason=non-code-file
file.295.path=tests/fixtures/decision-batch/m16/.gitkeep
file.295.verdict=skipped
file.295.reason=non-code-file
file.296.path=tests/fixtures/decision-batch/m16/.specify/knowledge/decision-batch-b-20261127t105123z-4bbb645d.md
file.296.verdict=skipped
file.296.reason=non-code-file
file.297.path=tests/fixtures/decision-batch/m16/.specify/register.md
file.297.verdict=skipped
file.297.reason=non-code-file
file.298.path=tests/fixtures/decision-batch/m16/.specify/specs/demo/item.md
file.298.verdict=skipped
file.298.reason=non-code-file
file.299.path=tests/fixtures/decision-batch/m16/.specify/specs/demo/ref.md
file.299.verdict=skipped
file.299.reason=non-code-file
file.300.path=tests/fixtures/decision-batch/m16/reply.md
file.300.verdict=skipped
file.300.reason=non-code-file
file.301.path=tests/fixtures/decision-batch/m16/scan.json
file.301.verdict=skipped
file.301.reason=non-code-file
file.302.path=tests/fixtures/decision-batch/prior-conflict/.gitkeep
file.302.verdict=skipped
file.302.reason=non-code-file
file.303.path=tests/fixtures/decision-batch/prior-conflict/.specify/register.md
file.303.verdict=skipped
file.303.reason=non-code-file
file.304.path=tests/fixtures/decision-batch/prior-conflict/.specify/specs/demo/conflict.md
file.304.verdict=skipped
file.304.reason=non-code-file
file.305.path=tests/fixtures/decision-batch/prior-conflict/.specify/specs/demo/history-records.md
file.305.verdict=skipped
file.305.reason=non-code-file
file.306.path=tests/fixtures/decision-batch/register-absent/.specify/specs/demo/absent.md
file.306.verdict=skipped
file.306.reason=non-code-file
file.307.path=tests/fixtures/decision-batch/register-absent/.specify/specs/demo/ref.md
file.307.verdict=skipped
file.307.reason=non-code-file
file.308.path=tests/fixtures/decision-batch/register-updates/.specify/register.md
file.308.verdict=skipped
file.308.reason=non-code-file
file.309.path=tests/fixtures/decision-batch/register-updates/.specify/specs/demo/ledger.md
file.309.verdict=skipped
file.309.reason=non-code-file
file.310.path=tests/fixtures/decision-batch/register-updates/.specify/specs/demo/ref.md
file.310.verdict=skipped
file.310.reason=non-code-file
file.311.path=tests/fixtures/decision-batch/replay-broken/.specify/register.md
file.311.verdict=skipped
file.311.reason=non-code-file
file.312.path=tests/fixtures/decision-batch/replay-broken/.specify/specs/demo/ref.md
file.312.verdict=skipped
file.312.reason=non-code-file
file.313.path=tests/fixtures/decision-batch/replay-broken/.specify/specs/demo/replay.md
file.313.verdict=skipped
file.313.reason=non-code-file
file.314.path=tests/fixtures/decision-batch/reply-shapes/.gitkeep
file.314.verdict=skipped
file.314.reason=non-code-file
file.315.path=tests/fixtures/decision-batch/reply-shapes/.specify/register.md
file.315.verdict=skipped
file.315.reason=non-code-file
file.316.path=tests/fixtures/decision-batch/reply-shapes/.specify/specs/demo/one.md
file.316.verdict=skipped
file.316.reason=non-code-file
file.317.path=tests/fixtures/decision-batch/reply-shapes/.specify/specs/demo/ref.md
file.317.verdict=skipped
file.317.reason=non-code-file
file.318.path=tests/fixtures/decision-batch/resolution-join/.gitkeep
file.318.verdict=skipped
file.318.reason=non-code-file
file.319.path=tests/fixtures/decision-batch/resolution-join/.specify/knowledge/decision-batch-b-20261101t000000z-bbbbbbbb.md
file.319.verdict=skipped
file.319.reason=non-code-file
file.320.path=tests/fixtures/decision-batch/resolution-join/.specify/register.md
file.320.verdict=skipped
file.320.reason=non-code-file
file.321.path=tests/fixtures/decision-batch/resolution-join/.specify/specs/demo/ref.md
file.321.verdict=skipped
file.321.reason=non-code-file
file.322.path=tests/fixtures/decision-batch/resolution-join/.specify/specs/demo/settled.md
file.322.verdict=skipped
file.322.reason=non-code-file
file.323.path=tests/fixtures/decision-batch/resolution-join/.specify/specs/demo/source.md
file.323.verdict=skipped
file.323.reason=non-code-file
file.324.path=tests/fixtures/decision-batch/source-conflict/.gitkeep
file.324.verdict=skipped
file.324.reason=non-code-file
file.325.path=tests/fixtures/decision-batch/two-source/.gitkeep
file.325.verdict=skipped
file.325.reason=non-code-file
file.326.path=tests/fixtures/decision-batch/two-source/.specify/register.md
file.326.verdict=skipped
file.326.reason=non-code-file
file.327.path=tests/fixtures/decision-batch/two-source/.specify/specs/demo/evidence-a.md
file.327.verdict=skipped
file.327.reason=non-code-file
file.328.path=tests/fixtures/decision-batch/two-source/.specify/specs/demo/fenced.md
file.328.verdict=skipped
file.328.reason=non-code-file
file.329.path=tests/fixtures/decision-batch/two-source/.specify/specs/demo/pending-a.md
file.329.verdict=skipped
file.329.reason=non-code-file
file.330.path=tests/fixtures/decision-batch/two-source/.specify/specs/demo/pending-b.md
file.330.verdict=skipped
file.330.reason=non-code-file
file.331.path=tests/fixtures/decision-batch/unreadable-register/.gitkeep
file.331.verdict=skipped
file.331.reason=non-code-file
file.332.path=tests/fixtures/decision-batch/unreadable-register/.specify/register.md
file.332.verdict=skipped
file.332.reason=non-code-file
file.333.path=tests/fixtures/decision-batch/unreadable-register/.specify/specs/demo/one.md
file.333.verdict=skipped
file.333.reason=non-code-file
file.334.path=tests/fixtures/decision-batch/unreadable-register/.specify/specs/demo/ref.md
file.334.verdict=skipped
file.334.reason=non-code-file
file.335.path=tests/fixtures/decision-batch/unwritable-old-record/.gitkeep
file.335.verdict=skipped
file.335.reason=non-code-file
file.336.path=tests/fixtures/decision-batch/unwritable-old-record/.specify/register.md
file.336.verdict=skipped
file.336.reason=non-code-file
file.337.path=tests/fixtures/decision-batch/unwritable-old-record/.specify/specs/demo/item.md
file.337.verdict=skipped
file.337.reason=non-code-file
file.338.path=tests/fixtures/decision-batch/unwritable-old-record/.specify/specs/demo/old-record.md
file.338.verdict=skipped
file.338.reason=non-code-file
file.339.path=tests/unit/test_decision_batch_engine.py
file.339.verdict=reviewed
<!-- coverage-receipt:end -->
