# Code Review Report — 代码段 (code segment)

| 属性 | 值 |
|------|-----|
| **分支** | `110-context-management` |
| **基准** | `0419adae5e6e0e208ad6bcb443e45be8d266f04a` (`0419adae5`) |
| **目标** | `8ef781e2719a07eef8cefdc3290466b3b0a4cd38` (`8ef781e27`) |
| **基准来源** | `feature-first-commit` |
| **渲染模式** | `renderer: text` |
| **Reviewer** | `Qiming Liu (John)` |
| **日期** | `2026-11-27T10:25:55Z` |

## 变更概览

```
 .../records/20261127T072628355872Z-543c4294.json   |    1 +
 .../records/20261127T073308631166Z-92bd8cfd.json   |    1 +
 .../records/20261127T074850335988Z-00b03532.json   |    1 +
 .../records/20261127T080412159425Z-df5b2a99.json   |    1 +
 .../records/20261127T081307767461Z-17befc22.json   |    1 +
 .../records/20261127T082703321162Z-955f127b.json   |    1 +
 .../records/20261127T085800623850Z-9f6a62ee.json   |    1 +
 .specify/features.md                               |    5 +-
 .specify/features/110-context-management.md        |   30 +
 .../20261127T072628Z-skill-create-requirements.md  |   22 +
 .../20261127T073341Z-skill-clarify-artifact.md     |   22 +
 .../feedback/20261127T074856Z-skill-create-plan.md |   23 +
 .../20261127T080418Z-skill-create-tasks.md         |   20 +
 .../20261127T081312Z-skill-create-checklist.md     |   20 +
 .../20261127T082707Z-skill-analyze-artifacts.md    |   20 +
 .../20261127T085805Z-skill-implement-feature.md    |   20 +
 .specify/instructions.md                           |    4 +
 ...T072649Z-r20261127T070000Z-110a-requirements.md |   64 ++
 ...127T081406Z-r20261127T070000Z-110a-checklist.md |   56 +
 ...61127T082826Z-r20261127T070000Z-110a-analyze.md |   29 +
 ...27T084243Z-r20261127T070000Z-110a-analyze-r2.md |   29 +
 .specify/scripts/python/context-audit.py           |  725 +++++++++++++
 ...n-skill-create-requirements-r20261124t024654.md |   10 +-
 ...ion-skill-create-plan-r20261125t173500z-107c.md |   10 +-
 ...n-skill-create-requirements-r20261127t070000.md |  207 ++++
 ...n-skill-clarify-artifact-r20261127t070000z-1.md |  192 ++++
 ...ion-skill-create-plan-r20261127t070000z-110a.md |  207 ++++
 ...on-skill-create-tasks-r20261127t070000z-110a.md |  207 ++++
 ...n-skill-create-checklist-r20261127t070000z-1.md |  202 ++++
 ...on-skill-analyze-artifacts-r20261127t070000z.md |  207 ++++
 ...on-skill-implement-feature-r20261127t070000z.md |  191 ++++
 .specify/shared/declarations/contract.yaml         |    9 +
 .../declarations/facts/context-categories.yaml     |    9 +
 .../shared/declarations/facts/context-classes.yaml |   28 +
 .../shared/declarations/facts/context-forms.yaml   |   12 +
 .../shared/declarations/facts/context-layers.yaml  |   10 +
 .../definitions/context-management-definitions.md  |  212 ++++
 .specify/shared/definitions/framework-map.md       |    3 +
 .../110-context-management/baseline-failed.txt     |  223 ++++
 .../checklists/context-model-2026-11-27.md         |   83 ++
 .../checklists/requirements.md                     |   51 +
 .../checkpoints/01-requirements.md                 |   16 +
 .../checkpoints/02-clarify.md                      |    8 +
 .../110-context-management/checkpoints/03-plan.md  |    8 +
 .../110-context-management/checkpoints/04-tasks.md |    8 +
 .../checkpoints/05-checklist.md                    |    8 +
 .../checkpoints/06-analyze.md                      |    8 +
 .../checkpoints/07-implement.md                    |    7 +
 .../contracts/declarations-and-domains.contract.md |  126 +++
 .../contracts/engine-and-distribution.contract.md  |  149 +++
 .../contracts/guards-and-boundaries.contract.md    |  131 +++
 .../contracts/matrix-and-triggers.contract.md      |  163 +++
 .../contracts/owner-and-layout.contract.md         |  130 +++
 .../110-context-management/coverage-baseline.txt   |  788 ++++++++++++++
 .../specs/110-context-management/data-model.md     |  208 ++++
 .../specs/110-context-management/feature-ref.md    |   79 ++
 .../specs/110-context-management/notes/.gitkeep    |    0
 .../notes/pre-change-measurements.md               |  285 +++++
 .../110-context-management/notes/quickstart-run.md |  129 +++
 .../notes/red-first-evidence.md                    |   90 ++
 .specify/specs/110-context-management/plan.md      |  427 ++++++++
 .../specs/110-context-management/quickstart.md     |  160 +++
 .../specs/110-context-management/requirements.md   |  289 +++++
 .specify/specs/110-context-management/research.md  |  198 ++++
 .specify/specs/110-context-management/tasks.md     |  407 +++++++
 .../test-evidence/analyze-exec-quant.txt           |    4 +
 .../test-evidence/analyze-feedback-record.txt      |   12 +
 .../analyze-repair-pre-analyze-tasks.txt           |    5 +
 .../analyze-repair-requirements-validator.txt      |   13 +
 .../test-evidence/analyze-repair-round1.md         |   63 ++
 .../analyze-repair-tasks-validator.txt             |    4 +
 .../analyze-repair-workspace-check.txt             |   22 +
 .../test-evidence/analyze-round1-findings.jsonl    |   24 +
 .../test-evidence/analyze-round1-report.md         |  216 ++++
 .../analyze-round2-artifact-hashes.txt             |   19 +
 .../test-evidence/analyze-round2-exec-quant.txt    |    4 +
 .../analyze-round2-feedback-record.txt             |   12 +
 .../test-evidence/analyze-round2-findings.jsonl    |   27 +
 .../test-evidence/analyze-round2-mirror-check.txt  |   16 +
 .../analyze-round2-pre-analyze-tasks.txt           |    5 +
 .../test-evidence/analyze-round2-report.md         |  140 +++
 .../analyze-round2-requirements-validator.txt      |   13 +
 .../analyze-round2-residue-verify.txt              |  151 +++
 .../analyze-round2-run-determination.txt           |    4 +
 .../analyze-round2-tasks-validator.txt             |    4 +
 .../analyze-round2-workspace-check.txt             |   24 +
 .../analyze-round2-workspace-snapshot.txt          |    4 +
 .../test-evidence/analyze-run-determination.txt    |   11 +
 .../test-evidence/analyze.jsonl                    |    1 +
 .../test-evidence/audit-fixtures.txt               |   67 ++
 .../test-evidence/cap-scan.txt                     |   55 +
 .../test-evidence/changed-set.txt                  |   78 ++
 .../test-evidence/checklist-exec-quant.txt         |    4 +
 .../test-evidence/checklist-feedback-record.txt    |   12 +
 .../test-evidence/checklist-run-determination.txt  |   11 +
 .../test-evidence/checklist-self-check.txt         |   45 +
 .../test-evidence/checklist-stage-2026-11-27.md    |   23 +
 .../test-evidence/checklist.jsonl                  |    1 +
 .../test-evidence/clarify-exec-quant.txt           |    1 +
 .../test-evidence/clarify-feedback-record.txt      |    9 +
 .../test-evidence/clarify-run-determination.txt    |    9 +
 .../test-evidence/clarify-stage-2026-11-27.md      |   47 +
 .../test-evidence/clarify-validator.txt            |   10 +
 .../test-evidence/clarify-workspace-guard.txt      |    1 +
 .../closure-acceptance-2026-11-27.json             |   38 +
 .../test-evidence/concept-presence.txt             |   66 ++
 .../test-evidence/decomposition-plan.txt           |    4 +
 .../decomposition-requirements-postcommit.json     |   12 +
 .../decomposition-requirements-postcommit.txt      |    1 +
 .../test-evidence/decomposition-requirements.json  |   12 +
 .../test-evidence/decomposition-requirements.txt   |    1 +
 .../test-evidence/decomposition-tasks.json         |   12 +
 .../test-evidence/decomposition-tasks.txt          |    4 +
 .../test-evidence/determinism.txt                  |   76 ++
 .../test-evidence/doc-consistency-plan.txt         |   10 +
 .../test-evidence/doc-consistency-tasks.txt        |   10 +
 .../test-evidence/full-suite-current-failed.txt    |  223 ++++
 .../test-evidence/full-suite.txt                   |   99 ++
 .../test-evidence/guard-convergence.txt            |   60 ++
 .../test-evidence/implement-entry-readings.txt     |   79 ++
 .../test-evidence/implement-p1-exec-quant.txt      |    4 +
 .../test-evidence/implement-p1-feedback-record.txt |   12 +
 .../implement-p1-run-determination.txt             |   11 +
 .../test-evidence/implement-p2-exec-quant.txt      |    4 +
 .../test-evidence/implement-p2-feedback-record.txt |   12 +
 .../implement-p2-run-determination.txt             |    4 +
 .../test-evidence/implement-p3-exec-quant.txt      |    4 +
 .../test-evidence/implement-p3-feedback-record.txt |   12 +
 .../implement-p3-run-determination.txt             |    4 +
 .../test-evidence/implement-p4-exec-quant.txt      |    4 +
 .../test-evidence/implement-p4-feedback-record.txt |   12 +
 .../implement-p4-run-determination.txt             |    4 +
 .../test-evidence/mirror-baseline-plan.txt         |   16 +
 .../test-evidence/mirror-final.txt                 |   55 +
 .../test-evidence/mutation-drill.txt               |   51 +
 .../test-evidence/plan-exec-quant.txt              |    1 +
 .../test-evidence/plan-feedback-record.txt         |    9 +
 .../test-evidence/plan-run-determination.txt       |    9 +
 .../test-evidence/plan-stage-2026-11-27.md         |  113 ++
 .../test-evidence/plan-time-reads.txt              |   58 +
 .../test-evidence/pre-analyze-plan.json            |  885 +++++++++++++++
 .../test-evidence/pre-analyze-plan.txt             |    2 +
 .../pre-analyze-requirements-postcommit.json       |  115 ++
 .../pre-analyze-requirements-postcommit.txt        |    2 +
 .../test-evidence/pre-analyze-requirements.json    |  115 ++
 .../test-evidence/pre-analyze-requirements.txt     |    2 +
 .../test-evidence/pre-analyze-tasks.json           | 1130 ++++++++++++++++++++
 .../test-evidence/pre-analyze-tasks.txt            |   10 +
 .../test-evidence/red-declarations.txt             |  316 ++++++
 .../test-evidence/red-engine.txt                   |  698 ++++++++++++
 .../test-evidence/red-init.txt                     |   66 ++
 .../test-evidence/red-owner.txt                    |  367 +++++++
 .../test-evidence/red-readonly.txt                 |  125 +++
 .../test-evidence/requirements-exec-quant.txt      |    1 +
 .../test-evidence/requirements-feedback-record.txt |    9 +
 .../requirements-run-determination.txt             |    9 +
 .../test-evidence/requirements-stage-2026-11-27.md |   41 +
 .../requirements-validator-postcommit.txt          |   10 +
 .../test-evidence/requirements-validator.txt       |   10 +
 .../test-evidence/tasks-exec-quant.txt             |    4 +
 .../test-evidence/tasks-feedback-record.txt        |   12 +
 .../test-evidence/tasks-run-determination.txt      |   11 +
 .../test-evidence/tasks-validator.txt              |    1 +
 .../test-evidence/us1-green.txt                    |  107 ++
 .../test-evidence/us2-green.txt                    |   85 ++
 .../test-evidence/us3-green.txt                    |   55 +
 .../test-evidence/us4-green.txt                    |  167 +++
 .../test-evidence/verification-input.md            |  109 ++
 .../test-evidence/workspace-analyze-repair.json    |  314 ++++++
 .../test-evidence/workspace-analyze-round2.json    |  314 ++++++
 .../test-evidence/workspace-checklist-check.txt    |   29 +
 .../test-evidence/workspace-checklist.json         |  313 ++++++
 .../test-evidence/workspace-implement-p1-check.txt |   35 +
 .../test-evidence/workspace-implement-p1.json      |  314 ++++++
 .../test-evidence/workspace-implement-p2-check.txt |   41 +
 .../test-evidence/workspace-implement-p2.json      |  314 ++++++
 .../test-evidence/workspace-implement-p3-check.txt |   44 +
 .../test-evidence/workspace-implement-p3.json      |  313 ++++++
 .../test-evidence/workspace-implement-p4-check.txt |   30 +
 .../test-evidence/workspace-implement-p4.json      |  313 ++++++
 .../test-evidence/workspace-plan-check.txt         |   40 +
 .../test-evidence/workspace-plan.json              |  314 ++++++
 .../test-evidence/workspace-requirements-check.txt |    1 +
 .../workspace-requirements-postcommit.json         |  314 ++++++
 .../workspace-requirements-postcommit.txt          |    1 +
 .../test-evidence/workspace-requirements.json      |  314 ++++++
 .../test-evidence/workspace-tasks-check.txt        |   28 +
 .../test-evidence/workspace-tasks.json             |  314 ++++++
 .../specs/110-context-management/verification.md   |  102 ++
 .specify/templates/instructions-template.md        |    4 +
 scripts/python/context-audit.py                    |  725 +++++++++++++
 shared/declarations/contract.yaml                  |    9 +
 shared/declarations/facts/context-categories.yaml  |    9 +
 shared/declarations/facts/context-classes.yaml     |   28 +
 shared/declarations/facts/context-forms.yaml       |   12 +
 shared/declarations/facts/context-layers.yaml      |   10 +
 .../definitions/context-management-definitions.md  |  212 ++++
 shared/definitions/framework-map.md                |    3 +
 templates/instructions-template.md                 |    4 +
 .../test_context_management_declarations.py        |  384 +++++++
 tests/contract/test_context_management_engine.py   |  631 +++++++++++
 tests/contract/test_context_management_owner.py    |  632 +++++++++++
 tests/contract/test_context_management_readonly.py |  221 ++++
 tests/contract/test_declaration_facts.py           |   10 +-
 tests/contract/test_fast_fail_discipline.py        |    8 +-
 .../absence-mixed/.specify/constitution.md         |    3 +
 .../absence-mixed/.specify/glossary.md             |    3 +
 .../absence-mixed/.specify/instructions.md         |    3 +
 .../absence-mixed/.specify/knowledge/entry.md      |    1 +
 .../absence-mixed/.specify/session/entry.md        |    0
 .../shared/definitions/fixture-definitions.md      |    3 +
 .../shared/workflow/user-input-protocol.md         |    1 +
 .../absence-mixed/.specify/skills.md               |    3 +
 .../absence-mixed/.specify/specs                   |    1 +
 .../absence-mixed/.specify/tools.md                |    3 +
 .../declarations/facts/context-categories.yaml     |    9 +
 .../shared/declarations/facts/context-classes.yaml |   19 +
 .../shared/declarations/facts/context-forms.yaml   |   12 +
 .../shared/declarations/facts/context-layers.yaml  |   10 +
 .../definitions/context-management-definitions.md  |   31 +
 .../all-present/.specify/constitution.md           |    3 +
 .../all-present/.specify/glossary.md               |    3 +
 .../all-present/.specify/instructions.md           |    3 +
 .../all-present/.specify/knowledge/entry.md        |    1 +
 .../all-present/.specify/session/entry.md          |    1 +
 .../shared/definitions/fixture-definitions.md      |    3 +
 .../shared/workflow/user-input-protocol.md         |    1 +
 .../all-present/.specify/skills.md                 |    3 +
 .../specs/110-context-management/requirements.md   |    3 +
 .../all-present/.specify/tools.md                  |    3 +
 .../all-present/docs/constraints.md                |    3 +
 .../declarations/facts/context-categories.yaml     |    9 +
 .../shared/declarations/facts/context-classes.yaml |   19 +
 .../shared/declarations/facts/context-forms.yaml   |   12 +
 .../shared/declarations/facts/context-layers.yaml  |   10 +
 .../definitions/context-management-definitions.md  |   31 +
 .../concept-missing/.specify/constitution.md       |    3 +
 .../concept-missing/.specify/glossary.md           |    1 +
 .../concept-missing/.specify/instructions.md       |    3 +
 .../concept-missing/.specify/knowledge/entry.md    |    1 +
 .../concept-missing/.specify/session/entry.md      |    1 +
 .../shared/definitions/fixture-definitions.md      |    3 +
 .../shared/workflow/user-input-protocol.md         |    1 +
 .../concept-missing/.specify/skills.md             |    3 +
 .../specs/110-context-management/requirements.md   |    3 +
 .../concept-missing/.specify/tools.md              |    3 +
 .../concept-missing/docs/constraints.md            |    3 +
 .../declarations/facts/context-categories.yaml     |    9 +
 .../shared/declarations/facts/context-classes.yaml |   19 +
 .../shared/declarations/facts/context-forms.yaml   |   12 +
 .../shared/declarations/facts/context-layers.yaml  |   10 +
 .../definitions/context-management-definitions.md  |   30 +
 .../declaration-missing/.specify/constitution.md   |    3 +
 .../declaration-missing/.specify/glossary.md       |    3 +
 .../declaration-missing/.specify/instructions.md   |    3 +
 .../.specify/knowledge/entry.md                    |    1 +
 .../declaration-missing/.specify/session/entry.md  |    1 +
 .../shared/definitions/fixture-definitions.md      |    3 +
 .../shared/workflow/user-input-protocol.md         |    1 +
 .../declaration-missing/.specify/skills.md         |    3 +
 .../specs/110-context-management/requirements.md   |    3 +
 .../declaration-missing/.specify/tools.md          |    3 +
 .../declaration-missing/docs/constraints.md        |    3 +
 .../declarations/facts/context-categories.yaml     |    9 +
 .../shared/declarations/facts/context-classes.yaml |   19 +
 .../shared/declarations/facts/context-layers.yaml  |   10 +
 .../definitions/context-management-definitions.md  |   31 +
 .../.specify/constitution.md                       |    3 +
 .../.specify/glossary.md                           |    3 +
 .../.specify/instructions.md                       |    3 +
 .../.specify/knowledge/entry.md                    |    1 +
 .../.specify/session/entry.md                      |    1 +
 .../shared/definitions/fixture-definitions.md      |    3 +
 .../shared/workflow/user-input-protocol.md         |    1 +
 .../declaration-unknown-member/.specify/skills.md  |    3 +
 .../specs/110-context-management/requirements.md   |    3 +
 .../declaration-unknown-member/.specify/tools.md   |    3 +
 .../declaration-unknown-member/docs/constraints.md |    3 +
 .../declarations/facts/context-categories.yaml     |    9 +
 .../shared/declarations/facts/context-classes.yaml |   21 +
 .../shared/declarations/facts/context-forms.yaml   |   12 +
 .../shared/declarations/facts/context-layers.yaml  |   10 +
 .../definitions/context-management-definitions.md  |   31 +
 .../violation-cap-missing/.specify/constitution.md |    3 +
 .../violation-cap-missing/.specify/glossary.md     |    3 +
 .../violation-cap-missing/.specify/instructions.md |    3 +
 .../.specify/knowledge/entry.md                    |    1 +
 .../.specify/session/entry.md                      |    1 +
 .../shared/definitions/fixture-definitions.md      |    3 +
 .../shared/workflow/user-input-protocol.md         |    1 +
 .../violation-cap-missing/.specify/skills.md       |    3 +
 .../specs/110-context-management/requirements.md   |    3 +
 .../violation-cap-missing/.specify/tools.md        |    3 +
 .../violation-cap-missing/docs/constraints.md      |    3 +
 .../declarations/facts/context-categories.yaml     |    9 +
 .../shared/declarations/facts/context-classes.yaml |   19 +
 .../shared/declarations/facts/context-forms.yaml   |   12 +
 .../shared/declarations/facts/context-layers.yaml  |   10 +
 .../definitions/context-management-definitions.md  |   31 +
 .../.specify/constitution.md                       |    3 +
 .../violation-category-column/.specify/glossary.md |    3 +
 .../.specify/instructions.md                       |    3 +
 .../.specify/knowledge/entry.md                    |    1 +
 .../.specify/session/entry.md                      |    1 +
 .../shared/definitions/fixture-definitions.md      |    3 +
 .../shared/workflow/user-input-protocol.md         |    1 +
 .../violation-category-column/.specify/skills.md   |    3 +
 .../specs/110-context-management/requirements.md   |    3 +
 .../violation-category-column/.specify/tools.md    |    3 +
 .../violation-category-column/docs/constraints.md  |    3 +
 .../declarations/facts/context-categories.yaml     |    9 +
 .../shared/declarations/facts/context-classes.yaml |   19 +
 .../shared/declarations/facts/context-forms.yaml   |   12 +
 .../shared/declarations/facts/context-layers.yaml  |   10 +
 .../definitions/context-management-definitions.md  |   31 +
 .../.specify/constitution.md                       |    3 +
 .../violation-duplicate-class/.specify/glossary.md |    3 +
 .../.specify/instructions.md                       |    3 +
 .../.specify/knowledge/entry.md                    |    1 +
 .../.specify/session/entry.md                      |    1 +
 .../shared/definitions/fixture-definitions.md      |    3 +
 .../shared/workflow/user-input-protocol.md         |    1 +
 .../violation-duplicate-class/.specify/skills.md   |    3 +
 .../specs/110-context-management/requirements.md   |    3 +
 .../violation-duplicate-class/.specify/tools.md    |    3 +
 .../violation-duplicate-class/docs/constraints.md  |    3 +
 .../declarations/facts/context-categories.yaml     |    9 +
 .../shared/declarations/facts/context-classes.yaml |   19 +
 .../shared/declarations/facts/context-forms.yaml   |   12 +
 .../shared/declarations/facts/context-layers.yaml  |   10 +
 .../definitions/context-management-definitions.md  |   32 +
 .../violation-empty-layer/.specify/constitution.md |    3 +
 .../violation-empty-layer/.specify/glossary.md     |    3 +
 .../violation-empty-layer/.specify/instructions.md |    3 +
 .../.specify/knowledge/entry.md                    |    1 +
 .../.specify/session/entry.md                      |    1 +
 .../shared/definitions/fixture-definitions.md      |    3 +
 .../shared/workflow/user-input-protocol.md         |    1 +
 .../violation-empty-layer/.specify/skills.md       |    3 +
 .../specs/110-context-management/requirements.md   |    3 +
 .../violation-empty-layer/.specify/tools.md        |    3 +
 .../violation-empty-layer/docs/constraints.md      |    3 +
 .../declarations/facts/context-categories.yaml     |    9 +
 .../shared/declarations/facts/context-classes.yaml |   19 +
 .../shared/declarations/facts/context-forms.yaml   |   12 +
 .../shared/declarations/facts/context-layers.yaml  |   10 +
 .../definitions/context-management-definitions.md  |   28 +
 .../violation-layer-form/.specify/constitution.md  |    3 +
 .../violation-layer-form/.specify/glossary.md      |    3 +
 .../violation-layer-form/.specify/instructions.md  |    3 +
 .../.specify/knowledge/entry.md                    |    1 +
 .../violation-layer-form/.specify/session/entry.md |    1 +
 .../shared/definitions/fixture-definitions.md      |    3 +
 .../shared/workflow/user-input-protocol.md         |    1 +
 .../violation-layer-form/.specify/skills.md        |    3 +
 .../specs/110-context-management/requirements.md   |    3 +
 .../violation-layer-form/.specify/tools.md         |    3 +
 .../violation-layer-form/docs/constraints.md       |    3 +
 .../declarations/facts/context-categories.yaml     |    9 +
 .../shared/declarations/facts/context-classes.yaml |   19 +
 .../shared/declarations/facts/context-forms.yaml   |   12 +
 .../shared/declarations/facts/context-layers.yaml  |   10 +
 .../definitions/context-management-definitions.md  |   31 +
 .../.specify/constitution.md                       |    3 +
 .../violation-roster-mismatch/.specify/glossary.md |    3 +
 .../.specify/instructions.md                       |    3 +
 .../.specify/knowledge/entry.md                    |    1 +
 .../.specify/session/entry.md                      |    1 +
 .../shared/definitions/fixture-definitions.md      |    3 +
 .../shared/workflow/user-input-protocol.md         |    1 +
 .../violation-roster-mismatch/.specify/skills.md   |    3 +
 .../specs/110-context-management/requirements.md   |    3 +
 .../violation-roster-mismatch/.specify/tools.md    |    3 +
 .../violation-roster-mismatch/docs/constraints.md  |    3 +
 .../declarations/facts/context-categories.yaml     |    9 +
 .../shared/declarations/facts/context-classes.yaml |   19 +
 .../shared/declarations/facts/context-forms.yaml   |   12 +
 .../shared/declarations/facts/context-layers.yaml  |   10 +
 .../definitions/context-management-definitions.md  |   30 +
 .../.specify/constitution.md                       |    3 +
 .../violation-roster-order/.specify/glossary.md    |    3 +
 .../.specify/instructions.md                       |    3 +
 .../.specify/knowledge/entry.md                    |    1 +
 .../.specify/session/entry.md                      |    1 +
 .../shared/definitions/fixture-definitions.md      |    3 +
 .../shared/workflow/user-input-protocol.md         |    1 +
 .../violation-roster-order/.specify/skills.md      |    3 +
 .../specs/110-context-management/requirements.md   |    3 +
 .../violation-roster-order/.specify/tools.md       |    3 +
 .../violation-roster-order/docs/constraints.md     |    3 +
 .../declarations/facts/context-categories.yaml     |    9 +
 .../shared/declarations/facts/context-classes.yaml |   19 +
 .../shared/declarations/facts/context-forms.yaml   |   12 +
 .../shared/declarations/facts/context-layers.yaml  |   10 +
 .../definitions/context-management-definitions.md  |   31 +
 .../.specify/constitution.md                       |    3 +
 .../violation-unknown-form/.specify/glossary.md    |    3 +
 .../.specify/instructions.md                       |    3 +
 .../.specify/knowledge/entry.md                    |    1 +
 .../.specify/session/entry.md                      |    1 +
 .../shared/definitions/fixture-definitions.md      |    3 +
 .../shared/workflow/user-input-protocol.md         |    1 +
 .../violation-unknown-form/.specify/skills.md      |    3 +
 .../specs/110-context-management/requirements.md   |    3 +
 .../violation-unknown-form/.specify/tools.md       |    3 +
 .../violation-unknown-form/docs/constraints.md     |    3 +
 .../declarations/facts/context-categories.yaml     |    9 +
 .../shared/declarations/facts/context-classes.yaml |   19 +
 .../shared/declarations/facts/context-forms.yaml   |   12 +
 .../shared/declarations/facts/context-layers.yaml  |   10 +
 .../definitions/context-management-definitions.md  |   31 +
 .../.specify/constitution.md                       |    3 +
 .../violation-unknown-layer/.specify/glossary.md   |    3 +
 .../.specify/instructions.md                       |    3 +
 .../.specify/knowledge/entry.md                    |    1 +
 .../.specify/session/entry.md                      |    1 +
 .../shared/definitions/fixture-definitions.md      |    3 +
 .../shared/workflow/user-input-protocol.md         |    1 +
 .../violation-unknown-layer/.specify/skills.md     |    3 +
 .../specs/110-context-management/requirements.md   |    3 +
 .../violation-unknown-layer/.specify/tools.md      |    3 +
 .../violation-unknown-layer/docs/constraints.md    |    3 +
 .../declarations/facts/context-categories.yaml     |    9 +
 .../shared/declarations/facts/context-classes.yaml |   19 +
 .../shared/declarations/facts/context-forms.yaml   |   12 +
 .../shared/declarations/facts/context-layers.yaml  |   10 +
 .../definitions/context-management-definitions.md  |   32 +
 tests/fixtures/context_management_support.py       |  289 +++++
 tests/integration/test_context_management_init.py  |  142 +++
 429 files changed, 22343 insertions(+), 15 deletions(-)
```

---

## Review 意见


### 🟠 [IMPORTANT] scripts/python/context-audit.py (Line 539)

> FR-021 fixes the check JSON face: findings carry rule/file/line/message and summary carries total plus by_rule counts. The engine emits rule/file/row/line/detail and a summary with a third 'findings' count; tests/contract/test_context_management_engine.py:63 pins that drifted key set. A consumer written against FR-021 breaks on the first finding. Decide the owner: align the engine and tests to FR-021, or amend FR-021 (and the contract) to the shipped shape.

<sub>18:26:21</sub>


### 🟠 [IMPORTANT] tests/contract/test_context_management_engine.py (Line 593)

> C-027 says the audit reports the two decidable duplication shapes and is red when the audit silently passes one. _decidable_duplications is a test-local helper asserted only over copies of the all-present fixture; it never runs over shared/definitions/context-management-definitions.md and the engine's nine-rule check has no duplication rule. A decidable duplication in the repository's own layout now passes every shipped guard silently. Apply the reading to the repository owner document (and name the reporting surface in the requirement).

<sub>18:26:21</sub>


### 🟢 [SUGGESTION] scripts/python/context-audit.py (Line 441)

> A directory holding entries that are all 0-byte files reads 'empty' (zero_only branch). FR-020 judges a directory by entry count and defines 'empty' as a 0-byte file or an empty directory; data-model.md agrees, while the owner document line 78 widens the definition. Four surfaces state this one fact differently and the engine follows the owner document. Align the definitions (or record the widened reading in FR-020) so one reading is authoritative.

<sub>18:26:21</sub>


### 👍 [PRAISE] scripts/python/context-audit.py (Line 35)

> Read-only discipline is mechanically demonstrated, not asserted: AST scan for write-shaped calls and network imports, in-process socket monkeypatching, and before/after SHA-256 tree manifests on three fixture trees plus the repository tree. The digest carries metadata only and the text/JSON faces agree.

<sub>18:26:21</sub>


### 👍 [PRAISE] tests/contract/test_context_management_engine.py (Line 289)

> test-evidence/mutation-drill.txt shows each of the nine check rules going red when exactly that rule's emission is removed and green again after a byte-exact restore - the guard set is credible per rule, which is what FR-027 asks for.

<sub>18:26:21</sub>


### 👍 [PRAISE] shared/definitions/context-management-definitions.md (Line 103)

> The layout table is a real single home: the roster fact is the machine member list, the table is its projection, and the engine, guard suite and mirror check all agree. sync-mirrors.py --check reports all six pairs byte-identical.

<sub>18:26:21</sub>


> **未提交范围（未评审）**: 2 个未提交路径未计入本次评审对象（.specify/session/20261125T140702Z-run-determination-skill-clarify-artifact-r20261125t134500z-1.md, .specify/trigger/index.json）；本回执不对该范围给出任何结论。

<!-- coverage-receipt:begin -->
receipt_version=1
base=0419adae5e6e0e208ad6bcb443e45be8d266f04a
head=8ef781e2719a07eef8cefdc3290466b3b0a4cd38
base_source=feature-first-commit
renderer=text
changed_files=429
judged_files=29
skipped_files=400
gap_files=0
lines_added=4375
lines_deleted=5
file.001.path=.specify/exec-quant/records/20261127T072628355872Z-543c4294.json
file.001.verdict=skipped
file.001.reason=generated
file.002.path=.specify/exec-quant/records/20261127T073308631166Z-92bd8cfd.json
file.002.verdict=skipped
file.002.reason=generated
file.003.path=.specify/exec-quant/records/20261127T074850335988Z-00b03532.json
file.003.verdict=skipped
file.003.reason=generated
file.004.path=.specify/exec-quant/records/20261127T080412159425Z-df5b2a99.json
file.004.verdict=skipped
file.004.reason=generated
file.005.path=.specify/exec-quant/records/20261127T081307767461Z-17befc22.json
file.005.verdict=skipped
file.005.reason=generated
file.006.path=.specify/exec-quant/records/20261127T082703321162Z-955f127b.json
file.006.verdict=skipped
file.006.reason=generated
file.007.path=.specify/exec-quant/records/20261127T085800623850Z-9f6a62ee.json
file.007.verdict=skipped
file.007.reason=generated
file.008.path=.specify/features.md
file.008.verdict=reviewed
file.009.path=.specify/features/110-context-management.md
file.009.verdict=reviewed
file.010.path=.specify/feedback/20261127T072628Z-skill-create-requirements.md
file.010.verdict=skipped
file.010.reason=generated
file.011.path=.specify/feedback/20261127T073341Z-skill-clarify-artifact.md
file.011.verdict=skipped
file.011.reason=generated
file.012.path=.specify/feedback/20261127T074856Z-skill-create-plan.md
file.012.verdict=skipped
file.012.reason=generated
file.013.path=.specify/feedback/20261127T080418Z-skill-create-tasks.md
file.013.verdict=skipped
file.013.reason=generated
file.014.path=.specify/feedback/20261127T081312Z-skill-create-checklist.md
file.014.verdict=skipped
file.014.reason=generated
file.015.path=.specify/feedback/20261127T082707Z-skill-analyze-artifacts.md
file.015.verdict=skipped
file.015.reason=generated
file.016.path=.specify/feedback/20261127T085805Z-skill-implement-feature.md
file.016.verdict=skipped
file.016.reason=generated
file.017.path=.specify/instructions.md
file.017.verdict=reviewed
file.018.path=.specify/retention/closeout/20261127T072649Z-r20261127T070000Z-110a-requirements.md
file.018.verdict=skipped
file.018.reason=generated
file.019.path=.specify/retention/closeout/20261127T081406Z-r20261127T070000Z-110a-checklist.md
file.019.verdict=skipped
file.019.reason=generated
file.020.path=.specify/retention/closeout/20261127T082826Z-r20261127T070000Z-110a-analyze.md
file.020.verdict=skipped
file.020.reason=generated
file.021.path=.specify/retention/closeout/20261127T084243Z-r20261127T070000Z-110a-analyze-r2.md
file.021.verdict=skipped
file.021.reason=generated
file.022.path=.specify/scripts/python/context-audit.py
file.022.verdict=reviewed
file.023.path=.specify/session/20261124T025604Z-run-determination-skill-create-requirements-r20261124t024654.md
file.023.verdict=skipped
file.023.reason=generated
file.024.path=.specify/session/20261125T173624Z-run-determination-skill-create-plan-r20261125t173500z-107c.md
file.024.verdict=skipped
file.024.reason=generated
file.025.path=.specify/session/20261127T072618Z-run-determination-skill-create-requirements-r20261127t070000.md
file.025.verdict=skipped
file.025.reason=generated
file.026.path=.specify/session/20261127T073329Z-run-determination-skill-clarify-artifact-r20261127t070000z-1.md
file.026.verdict=skipped
file.026.reason=generated
file.027.path=.specify/session/20261127T074847Z-run-determination-skill-create-plan-r20261127t070000z-110a.md
file.027.verdict=skipped
file.027.reason=generated
file.028.path=.specify/session/20261127T080408Z-run-determination-skill-create-tasks-r20261127t070000z-110a.md
file.028.verdict=skipped
file.028.reason=generated
file.029.path=.specify/session/20261127T081302Z-run-determination-skill-create-checklist-r20261127t070000z-1.md
file.029.verdict=skipped
file.029.reason=generated
file.030.path=.specify/session/20261127T082658Z-run-determination-skill-analyze-artifacts-r20261127t070000z.md
file.030.verdict=skipped
file.030.reason=generated
file.031.path=.specify/session/20261127T085746Z-run-determination-skill-implement-feature-r20261127t070000z.md
file.031.verdict=skipped
file.031.reason=generated
file.032.path=.specify/shared/declarations/contract.yaml
file.032.verdict=reviewed
file.033.path=.specify/shared/declarations/facts/context-categories.yaml
file.033.verdict=reviewed
file.034.path=.specify/shared/declarations/facts/context-classes.yaml
file.034.verdict=reviewed
file.035.path=.specify/shared/declarations/facts/context-forms.yaml
file.035.verdict=reviewed
file.036.path=.specify/shared/declarations/facts/context-layers.yaml
file.036.verdict=reviewed
file.037.path=.specify/shared/definitions/context-management-definitions.md
file.037.verdict=reviewed
file.038.path=.specify/shared/definitions/framework-map.md
file.038.verdict=reviewed
file.039.path=.specify/specs/110-context-management/baseline-failed.txt
file.039.verdict=skipped
file.039.reason=non-code-file
file.040.path=.specify/specs/110-context-management/checklists/context-model-2026-11-27.md
file.040.verdict=skipped
file.040.reason=non-code-file
file.041.path=.specify/specs/110-context-management/checklists/requirements.md
file.041.verdict=skipped
file.041.reason=non-code-file
file.042.path=.specify/specs/110-context-management/checkpoints/01-requirements.md
file.042.verdict=skipped
file.042.reason=non-code-file
file.043.path=.specify/specs/110-context-management/checkpoints/02-clarify.md
file.043.verdict=skipped
file.043.reason=non-code-file
file.044.path=.specify/specs/110-context-management/checkpoints/03-plan.md
file.044.verdict=skipped
file.044.reason=non-code-file
file.045.path=.specify/specs/110-context-management/checkpoints/04-tasks.md
file.045.verdict=skipped
file.045.reason=non-code-file
file.046.path=.specify/specs/110-context-management/checkpoints/05-checklist.md
file.046.verdict=skipped
file.046.reason=non-code-file
file.047.path=.specify/specs/110-context-management/checkpoints/06-analyze.md
file.047.verdict=skipped
file.047.reason=non-code-file
file.048.path=.specify/specs/110-context-management/checkpoints/07-implement.md
file.048.verdict=skipped
file.048.reason=non-code-file
file.049.path=.specify/specs/110-context-management/contracts/declarations-and-domains.contract.md
file.049.verdict=skipped
file.049.reason=non-code-file
file.050.path=.specify/specs/110-context-management/contracts/engine-and-distribution.contract.md
file.050.verdict=skipped
file.050.reason=non-code-file
file.051.path=.specify/specs/110-context-management/contracts/guards-and-boundaries.contract.md
file.051.verdict=skipped
file.051.reason=non-code-file
file.052.path=.specify/specs/110-context-management/contracts/matrix-and-triggers.contract.md
file.052.verdict=skipped
file.052.reason=non-code-file
file.053.path=.specify/specs/110-context-management/contracts/owner-and-layout.contract.md
file.053.verdict=skipped
file.053.reason=non-code-file
file.054.path=.specify/specs/110-context-management/coverage-baseline.txt
file.054.verdict=skipped
file.054.reason=non-code-file
file.055.path=.specify/specs/110-context-management/data-model.md
file.055.verdict=skipped
file.055.reason=non-code-file
file.056.path=.specify/specs/110-context-management/feature-ref.md
file.056.verdict=skipped
file.056.reason=non-code-file
file.057.path=.specify/specs/110-context-management/notes/.gitkeep
file.057.verdict=skipped
file.057.reason=non-code-file
file.058.path=.specify/specs/110-context-management/notes/pre-change-measurements.md
file.058.verdict=skipped
file.058.reason=non-code-file
file.059.path=.specify/specs/110-context-management/notes/quickstart-run.md
file.059.verdict=skipped
file.059.reason=non-code-file
file.060.path=.specify/specs/110-context-management/notes/red-first-evidence.md
file.060.verdict=skipped
file.060.reason=non-code-file
file.061.path=.specify/specs/110-context-management/plan.md
file.061.verdict=skipped
file.061.reason=non-code-file
file.062.path=.specify/specs/110-context-management/quickstart.md
file.062.verdict=skipped
file.062.reason=non-code-file
file.063.path=.specify/specs/110-context-management/requirements.md
file.063.verdict=skipped
file.063.reason=non-code-file
file.064.path=.specify/specs/110-context-management/research.md
file.064.verdict=skipped
file.064.reason=non-code-file
file.065.path=.specify/specs/110-context-management/tasks.md
file.065.verdict=skipped
file.065.reason=non-code-file
file.066.path=.specify/specs/110-context-management/test-evidence/analyze-exec-quant.txt
file.066.verdict=skipped
file.066.reason=non-code-file
file.067.path=.specify/specs/110-context-management/test-evidence/analyze-feedback-record.txt
file.067.verdict=skipped
file.067.reason=non-code-file
file.068.path=.specify/specs/110-context-management/test-evidence/analyze-repair-pre-analyze-tasks.txt
file.068.verdict=skipped
file.068.reason=non-code-file
file.069.path=.specify/specs/110-context-management/test-evidence/analyze-repair-requirements-validator.txt
file.069.verdict=skipped
file.069.reason=non-code-file
file.070.path=.specify/specs/110-context-management/test-evidence/analyze-repair-round1.md
file.070.verdict=skipped
file.070.reason=non-code-file
file.071.path=.specify/specs/110-context-management/test-evidence/analyze-repair-tasks-validator.txt
file.071.verdict=skipped
file.071.reason=non-code-file
file.072.path=.specify/specs/110-context-management/test-evidence/analyze-repair-workspace-check.txt
file.072.verdict=skipped
file.072.reason=non-code-file
file.073.path=.specify/specs/110-context-management/test-evidence/analyze-round1-findings.jsonl
file.073.verdict=skipped
file.073.reason=non-code-file
file.074.path=.specify/specs/110-context-management/test-evidence/analyze-round1-report.md
file.074.verdict=skipped
file.074.reason=non-code-file
file.075.path=.specify/specs/110-context-management/test-evidence/analyze-round2-artifact-hashes.txt
file.075.verdict=skipped
file.075.reason=non-code-file
file.076.path=.specify/specs/110-context-management/test-evidence/analyze-round2-exec-quant.txt
file.076.verdict=skipped
file.076.reason=non-code-file
file.077.path=.specify/specs/110-context-management/test-evidence/analyze-round2-feedback-record.txt
file.077.verdict=skipped
file.077.reason=non-code-file
file.078.path=.specify/specs/110-context-management/test-evidence/analyze-round2-findings.jsonl
file.078.verdict=skipped
file.078.reason=non-code-file
file.079.path=.specify/specs/110-context-management/test-evidence/analyze-round2-mirror-check.txt
file.079.verdict=skipped
file.079.reason=non-code-file
file.080.path=.specify/specs/110-context-management/test-evidence/analyze-round2-pre-analyze-tasks.txt
file.080.verdict=skipped
file.080.reason=non-code-file
file.081.path=.specify/specs/110-context-management/test-evidence/analyze-round2-report.md
file.081.verdict=skipped
file.081.reason=non-code-file
file.082.path=.specify/specs/110-context-management/test-evidence/analyze-round2-requirements-validator.txt
file.082.verdict=skipped
file.082.reason=non-code-file
file.083.path=.specify/specs/110-context-management/test-evidence/analyze-round2-residue-verify.txt
file.083.verdict=skipped
file.083.reason=non-code-file
file.084.path=.specify/specs/110-context-management/test-evidence/analyze-round2-run-determination.txt
file.084.verdict=skipped
file.084.reason=non-code-file
file.085.path=.specify/specs/110-context-management/test-evidence/analyze-round2-tasks-validator.txt
file.085.verdict=skipped
file.085.reason=non-code-file
file.086.path=.specify/specs/110-context-management/test-evidence/analyze-round2-workspace-check.txt
file.086.verdict=skipped
file.086.reason=non-code-file
file.087.path=.specify/specs/110-context-management/test-evidence/analyze-round2-workspace-snapshot.txt
file.087.verdict=skipped
file.087.reason=non-code-file
file.088.path=.specify/specs/110-context-management/test-evidence/analyze-run-determination.txt
file.088.verdict=skipped
file.088.reason=non-code-file
file.089.path=.specify/specs/110-context-management/test-evidence/analyze.jsonl
file.089.verdict=skipped
file.089.reason=non-code-file
file.090.path=.specify/specs/110-context-management/test-evidence/audit-fixtures.txt
file.090.verdict=skipped
file.090.reason=non-code-file
file.091.path=.specify/specs/110-context-management/test-evidence/cap-scan.txt
file.091.verdict=skipped
file.091.reason=non-code-file
file.092.path=.specify/specs/110-context-management/test-evidence/changed-set.txt
file.092.verdict=skipped
file.092.reason=non-code-file
file.093.path=.specify/specs/110-context-management/test-evidence/checklist-exec-quant.txt
file.093.verdict=skipped
file.093.reason=non-code-file
file.094.path=.specify/specs/110-context-management/test-evidence/checklist-feedback-record.txt
file.094.verdict=skipped
file.094.reason=non-code-file
file.095.path=.specify/specs/110-context-management/test-evidence/checklist-run-determination.txt
file.095.verdict=skipped
file.095.reason=non-code-file
file.096.path=.specify/specs/110-context-management/test-evidence/checklist-self-check.txt
file.096.verdict=skipped
file.096.reason=non-code-file
file.097.path=.specify/specs/110-context-management/test-evidence/checklist-stage-2026-11-27.md
file.097.verdict=skipped
file.097.reason=non-code-file
file.098.path=.specify/specs/110-context-management/test-evidence/checklist.jsonl
file.098.verdict=skipped
file.098.reason=non-code-file
file.099.path=.specify/specs/110-context-management/test-evidence/clarify-exec-quant.txt
file.099.verdict=skipped
file.099.reason=non-code-file
file.100.path=.specify/specs/110-context-management/test-evidence/clarify-feedback-record.txt
file.100.verdict=skipped
file.100.reason=non-code-file
file.101.path=.specify/specs/110-context-management/test-evidence/clarify-run-determination.txt
file.101.verdict=skipped
file.101.reason=non-code-file
file.102.path=.specify/specs/110-context-management/test-evidence/clarify-stage-2026-11-27.md
file.102.verdict=skipped
file.102.reason=non-code-file
file.103.path=.specify/specs/110-context-management/test-evidence/clarify-validator.txt
file.103.verdict=skipped
file.103.reason=non-code-file
file.104.path=.specify/specs/110-context-management/test-evidence/clarify-workspace-guard.txt
file.104.verdict=skipped
file.104.reason=non-code-file
file.105.path=.specify/specs/110-context-management/test-evidence/closure-acceptance-2026-11-27.json
file.105.verdict=skipped
file.105.reason=non-code-file
file.106.path=.specify/specs/110-context-management/test-evidence/concept-presence.txt
file.106.verdict=skipped
file.106.reason=non-code-file
file.107.path=.specify/specs/110-context-management/test-evidence/decomposition-plan.txt
file.107.verdict=skipped
file.107.reason=non-code-file
file.108.path=.specify/specs/110-context-management/test-evidence/decomposition-requirements-postcommit.json
file.108.verdict=skipped
file.108.reason=non-code-file
file.109.path=.specify/specs/110-context-management/test-evidence/decomposition-requirements-postcommit.txt
file.109.verdict=skipped
file.109.reason=non-code-file
file.110.path=.specify/specs/110-context-management/test-evidence/decomposition-requirements.json
file.110.verdict=skipped
file.110.reason=non-code-file
file.111.path=.specify/specs/110-context-management/test-evidence/decomposition-requirements.txt
file.111.verdict=skipped
file.111.reason=non-code-file
file.112.path=.specify/specs/110-context-management/test-evidence/decomposition-tasks.json
file.112.verdict=skipped
file.112.reason=non-code-file
file.113.path=.specify/specs/110-context-management/test-evidence/decomposition-tasks.txt
file.113.verdict=skipped
file.113.reason=non-code-file
file.114.path=.specify/specs/110-context-management/test-evidence/determinism.txt
file.114.verdict=skipped
file.114.reason=non-code-file
file.115.path=.specify/specs/110-context-management/test-evidence/doc-consistency-plan.txt
file.115.verdict=skipped
file.115.reason=non-code-file
file.116.path=.specify/specs/110-context-management/test-evidence/doc-consistency-tasks.txt
file.116.verdict=skipped
file.116.reason=non-code-file
file.117.path=.specify/specs/110-context-management/test-evidence/full-suite-current-failed.txt
file.117.verdict=skipped
file.117.reason=non-code-file
file.118.path=.specify/specs/110-context-management/test-evidence/full-suite.txt
file.118.verdict=skipped
file.118.reason=non-code-file
file.119.path=.specify/specs/110-context-management/test-evidence/guard-convergence.txt
file.119.verdict=skipped
file.119.reason=non-code-file
file.120.path=.specify/specs/110-context-management/test-evidence/implement-entry-readings.txt
file.120.verdict=skipped
file.120.reason=non-code-file
file.121.path=.specify/specs/110-context-management/test-evidence/implement-p1-exec-quant.txt
file.121.verdict=skipped
file.121.reason=non-code-file
file.122.path=.specify/specs/110-context-management/test-evidence/implement-p1-feedback-record.txt
file.122.verdict=skipped
file.122.reason=non-code-file
file.123.path=.specify/specs/110-context-management/test-evidence/implement-p1-run-determination.txt
file.123.verdict=skipped
file.123.reason=non-code-file
file.124.path=.specify/specs/110-context-management/test-evidence/implement-p2-exec-quant.txt
file.124.verdict=skipped
file.124.reason=non-code-file
file.125.path=.specify/specs/110-context-management/test-evidence/implement-p2-feedback-record.txt
file.125.verdict=skipped
file.125.reason=non-code-file
file.126.path=.specify/specs/110-context-management/test-evidence/implement-p2-run-determination.txt
file.126.verdict=skipped
file.126.reason=non-code-file
file.127.path=.specify/specs/110-context-management/test-evidence/implement-p3-exec-quant.txt
file.127.verdict=skipped
file.127.reason=non-code-file
file.128.path=.specify/specs/110-context-management/test-evidence/implement-p3-feedback-record.txt
file.128.verdict=skipped
file.128.reason=non-code-file
file.129.path=.specify/specs/110-context-management/test-evidence/implement-p3-run-determination.txt
file.129.verdict=skipped
file.129.reason=non-code-file
file.130.path=.specify/specs/110-context-management/test-evidence/implement-p4-exec-quant.txt
file.130.verdict=skipped
file.130.reason=non-code-file
file.131.path=.specify/specs/110-context-management/test-evidence/implement-p4-feedback-record.txt
file.131.verdict=skipped
file.131.reason=non-code-file
file.132.path=.specify/specs/110-context-management/test-evidence/implement-p4-run-determination.txt
file.132.verdict=skipped
file.132.reason=non-code-file
file.133.path=.specify/specs/110-context-management/test-evidence/mirror-baseline-plan.txt
file.133.verdict=skipped
file.133.reason=non-code-file
file.134.path=.specify/specs/110-context-management/test-evidence/mirror-final.txt
file.134.verdict=skipped
file.134.reason=non-code-file
file.135.path=.specify/specs/110-context-management/test-evidence/mutation-drill.txt
file.135.verdict=skipped
file.135.reason=non-code-file
file.136.path=.specify/specs/110-context-management/test-evidence/plan-exec-quant.txt
file.136.verdict=skipped
file.136.reason=non-code-file
file.137.path=.specify/specs/110-context-management/test-evidence/plan-feedback-record.txt
file.137.verdict=skipped
file.137.reason=non-code-file
file.138.path=.specify/specs/110-context-management/test-evidence/plan-run-determination.txt
file.138.verdict=skipped
file.138.reason=non-code-file
file.139.path=.specify/specs/110-context-management/test-evidence/plan-stage-2026-11-27.md
file.139.verdict=skipped
file.139.reason=non-code-file
file.140.path=.specify/specs/110-context-management/test-evidence/plan-time-reads.txt
file.140.verdict=skipped
file.140.reason=non-code-file
file.141.path=.specify/specs/110-context-management/test-evidence/pre-analyze-plan.json
file.141.verdict=skipped
file.141.reason=non-code-file
file.142.path=.specify/specs/110-context-management/test-evidence/pre-analyze-plan.txt
file.142.verdict=skipped
file.142.reason=non-code-file
file.143.path=.specify/specs/110-context-management/test-evidence/pre-analyze-requirements-postcommit.json
file.143.verdict=skipped
file.143.reason=non-code-file
file.144.path=.specify/specs/110-context-management/test-evidence/pre-analyze-requirements-postcommit.txt
file.144.verdict=skipped
file.144.reason=non-code-file
file.145.path=.specify/specs/110-context-management/test-evidence/pre-analyze-requirements.json
file.145.verdict=skipped
file.145.reason=non-code-file
file.146.path=.specify/specs/110-context-management/test-evidence/pre-analyze-requirements.txt
file.146.verdict=skipped
file.146.reason=non-code-file
file.147.path=.specify/specs/110-context-management/test-evidence/pre-analyze-tasks.json
file.147.verdict=skipped
file.147.reason=non-code-file
file.148.path=.specify/specs/110-context-management/test-evidence/pre-analyze-tasks.txt
file.148.verdict=skipped
file.148.reason=non-code-file
file.149.path=.specify/specs/110-context-management/test-evidence/red-declarations.txt
file.149.verdict=skipped
file.149.reason=non-code-file
file.150.path=.specify/specs/110-context-management/test-evidence/red-engine.txt
file.150.verdict=skipped
file.150.reason=non-code-file
file.151.path=.specify/specs/110-context-management/test-evidence/red-init.txt
file.151.verdict=skipped
file.151.reason=non-code-file
file.152.path=.specify/specs/110-context-management/test-evidence/red-owner.txt
file.152.verdict=skipped
file.152.reason=non-code-file
file.153.path=.specify/specs/110-context-management/test-evidence/red-readonly.txt
file.153.verdict=skipped
file.153.reason=non-code-file
file.154.path=.specify/specs/110-context-management/test-evidence/requirements-exec-quant.txt
file.154.verdict=skipped
file.154.reason=non-code-file
file.155.path=.specify/specs/110-context-management/test-evidence/requirements-feedback-record.txt
file.155.verdict=skipped
file.155.reason=non-code-file
file.156.path=.specify/specs/110-context-management/test-evidence/requirements-run-determination.txt
file.156.verdict=skipped
file.156.reason=non-code-file
file.157.path=.specify/specs/110-context-management/test-evidence/requirements-stage-2026-11-27.md
file.157.verdict=skipped
file.157.reason=non-code-file
file.158.path=.specify/specs/110-context-management/test-evidence/requirements-validator-postcommit.txt
file.158.verdict=skipped
file.158.reason=non-code-file
file.159.path=.specify/specs/110-context-management/test-evidence/requirements-validator.txt
file.159.verdict=skipped
file.159.reason=non-code-file
file.160.path=.specify/specs/110-context-management/test-evidence/tasks-exec-quant.txt
file.160.verdict=skipped
file.160.reason=non-code-file
file.161.path=.specify/specs/110-context-management/test-evidence/tasks-feedback-record.txt
file.161.verdict=skipped
file.161.reason=non-code-file
file.162.path=.specify/specs/110-context-management/test-evidence/tasks-run-determination.txt
file.162.verdict=skipped
file.162.reason=non-code-file
file.163.path=.specify/specs/110-context-management/test-evidence/tasks-validator.txt
file.163.verdict=skipped
file.163.reason=non-code-file
file.164.path=.specify/specs/110-context-management/test-evidence/us1-green.txt
file.164.verdict=skipped
file.164.reason=non-code-file
file.165.path=.specify/specs/110-context-management/test-evidence/us2-green.txt
file.165.verdict=skipped
file.165.reason=non-code-file
file.166.path=.specify/specs/110-context-management/test-evidence/us3-green.txt
file.166.verdict=skipped
file.166.reason=non-code-file
file.167.path=.specify/specs/110-context-management/test-evidence/us4-green.txt
file.167.verdict=skipped
file.167.reason=non-code-file
file.168.path=.specify/specs/110-context-management/test-evidence/verification-input.md
file.168.verdict=skipped
file.168.reason=non-code-file
file.169.path=.specify/specs/110-context-management/test-evidence/workspace-analyze-repair.json
file.169.verdict=skipped
file.169.reason=non-code-file
file.170.path=.specify/specs/110-context-management/test-evidence/workspace-analyze-round2.json
file.170.verdict=skipped
file.170.reason=non-code-file
file.171.path=.specify/specs/110-context-management/test-evidence/workspace-checklist-check.txt
file.171.verdict=skipped
file.171.reason=non-code-file
file.172.path=.specify/specs/110-context-management/test-evidence/workspace-checklist.json
file.172.verdict=skipped
file.172.reason=non-code-file
file.173.path=.specify/specs/110-context-management/test-evidence/workspace-implement-p1-check.txt
file.173.verdict=skipped
file.173.reason=non-code-file
file.174.path=.specify/specs/110-context-management/test-evidence/workspace-implement-p1.json
file.174.verdict=skipped
file.174.reason=non-code-file
file.175.path=.specify/specs/110-context-management/test-evidence/workspace-implement-p2-check.txt
file.175.verdict=skipped
file.175.reason=non-code-file
file.176.path=.specify/specs/110-context-management/test-evidence/workspace-implement-p2.json
file.176.verdict=skipped
file.176.reason=non-code-file
file.177.path=.specify/specs/110-context-management/test-evidence/workspace-implement-p3-check.txt
file.177.verdict=skipped
file.177.reason=non-code-file
file.178.path=.specify/specs/110-context-management/test-evidence/workspace-implement-p3.json
file.178.verdict=skipped
file.178.reason=non-code-file
file.179.path=.specify/specs/110-context-management/test-evidence/workspace-implement-p4-check.txt
file.179.verdict=skipped
file.179.reason=non-code-file
file.180.path=.specify/specs/110-context-management/test-evidence/workspace-implement-p4.json
file.180.verdict=skipped
file.180.reason=non-code-file
file.181.path=.specify/specs/110-context-management/test-evidence/workspace-plan-check.txt
file.181.verdict=skipped
file.181.reason=non-code-file
file.182.path=.specify/specs/110-context-management/test-evidence/workspace-plan.json
file.182.verdict=skipped
file.182.reason=non-code-file
file.183.path=.specify/specs/110-context-management/test-evidence/workspace-requirements-check.txt
file.183.verdict=skipped
file.183.reason=non-code-file
file.184.path=.specify/specs/110-context-management/test-evidence/workspace-requirements-postcommit.json
file.184.verdict=skipped
file.184.reason=non-code-file
file.185.path=.specify/specs/110-context-management/test-evidence/workspace-requirements-postcommit.txt
file.185.verdict=skipped
file.185.reason=non-code-file
file.186.path=.specify/specs/110-context-management/test-evidence/workspace-requirements.json
file.186.verdict=skipped
file.186.reason=non-code-file
file.187.path=.specify/specs/110-context-management/test-evidence/workspace-tasks-check.txt
file.187.verdict=skipped
file.187.reason=non-code-file
file.188.path=.specify/specs/110-context-management/test-evidence/workspace-tasks.json
file.188.verdict=skipped
file.188.reason=non-code-file
file.189.path=.specify/specs/110-context-management/verification.md
file.189.verdict=skipped
file.189.reason=non-code-file
file.190.path=.specify/templates/instructions-template.md
file.190.verdict=reviewed
file.191.path=scripts/python/context-audit.py
file.191.verdict=reviewed
file.192.path=shared/declarations/contract.yaml
file.192.verdict=reviewed
file.193.path=shared/declarations/facts/context-categories.yaml
file.193.verdict=reviewed
file.194.path=shared/declarations/facts/context-classes.yaml
file.194.verdict=reviewed
file.195.path=shared/declarations/facts/context-forms.yaml
file.195.verdict=reviewed
file.196.path=shared/declarations/facts/context-layers.yaml
file.196.verdict=reviewed
file.197.path=shared/definitions/context-management-definitions.md
file.197.verdict=reviewed
file.198.path=shared/definitions/framework-map.md
file.198.verdict=reviewed
file.199.path=templates/instructions-template.md
file.199.verdict=reviewed
file.200.path=tests/contract/test_context_management_declarations.py
file.200.verdict=reviewed
file.201.path=tests/contract/test_context_management_engine.py
file.201.verdict=reviewed
file.202.path=tests/contract/test_context_management_owner.py
file.202.verdict=reviewed
file.203.path=tests/contract/test_context_management_readonly.py
file.203.verdict=reviewed
file.204.path=tests/contract/test_declaration_facts.py
file.204.verdict=reviewed
file.205.path=tests/contract/test_fast_fail_discipline.py
file.205.verdict=reviewed
file.206.path=tests/fixtures/context-management/absence-mixed/.specify/constitution.md
file.206.verdict=skipped
file.206.reason=non-code-file
file.207.path=tests/fixtures/context-management/absence-mixed/.specify/glossary.md
file.207.verdict=skipped
file.207.reason=non-code-file
file.208.path=tests/fixtures/context-management/absence-mixed/.specify/instructions.md
file.208.verdict=skipped
file.208.reason=non-code-file
file.209.path=tests/fixtures/context-management/absence-mixed/.specify/knowledge/entry.md
file.209.verdict=skipped
file.209.reason=non-code-file
file.210.path=tests/fixtures/context-management/absence-mixed/.specify/session/entry.md
file.210.verdict=skipped
file.210.reason=non-code-file
file.211.path=tests/fixtures/context-management/absence-mixed/.specify/shared/definitions/fixture-definitions.md
file.211.verdict=skipped
file.211.reason=non-code-file
file.212.path=tests/fixtures/context-management/absence-mixed/.specify/shared/workflow/user-input-protocol.md
file.212.verdict=skipped
file.212.reason=non-code-file
file.213.path=tests/fixtures/context-management/absence-mixed/.specify/skills.md
file.213.verdict=skipped
file.213.reason=non-code-file
file.214.path=tests/fixtures/context-management/absence-mixed/.specify/specs
file.214.verdict=skipped
file.214.reason=non-code-file
file.215.path=tests/fixtures/context-management/absence-mixed/.specify/tools.md
file.215.verdict=skipped
file.215.reason=non-code-file
file.216.path=tests/fixtures/context-management/absence-mixed/shared/declarations/facts/context-categories.yaml
file.216.verdict=skipped
file.216.reason=non-code-file
file.217.path=tests/fixtures/context-management/absence-mixed/shared/declarations/facts/context-classes.yaml
file.217.verdict=skipped
file.217.reason=non-code-file
file.218.path=tests/fixtures/context-management/absence-mixed/shared/declarations/facts/context-forms.yaml
file.218.verdict=skipped
file.218.reason=non-code-file
file.219.path=tests/fixtures/context-management/absence-mixed/shared/declarations/facts/context-layers.yaml
file.219.verdict=skipped
file.219.reason=non-code-file
file.220.path=tests/fixtures/context-management/absence-mixed/shared/definitions/context-management-definitions.md
file.220.verdict=skipped
file.220.reason=non-code-file
file.221.path=tests/fixtures/context-management/all-present/.specify/constitution.md
file.221.verdict=skipped
file.221.reason=non-code-file
file.222.path=tests/fixtures/context-management/all-present/.specify/glossary.md
file.222.verdict=skipped
file.222.reason=non-code-file
file.223.path=tests/fixtures/context-management/all-present/.specify/instructions.md
file.223.verdict=skipped
file.223.reason=non-code-file
file.224.path=tests/fixtures/context-management/all-present/.specify/knowledge/entry.md
file.224.verdict=skipped
file.224.reason=non-code-file
file.225.path=tests/fixtures/context-management/all-present/.specify/session/entry.md
file.225.verdict=skipped
file.225.reason=non-code-file
file.226.path=tests/fixtures/context-management/all-present/.specify/shared/definitions/fixture-definitions.md
file.226.verdict=skipped
file.226.reason=non-code-file
file.227.path=tests/fixtures/context-management/all-present/.specify/shared/workflow/user-input-protocol.md
file.227.verdict=skipped
file.227.reason=non-code-file
file.228.path=tests/fixtures/context-management/all-present/.specify/skills.md
file.228.verdict=skipped
file.228.reason=non-code-file
file.229.path=tests/fixtures/context-management/all-present/.specify/specs/110-context-management/requirements.md
file.229.verdict=skipped
file.229.reason=non-code-file
file.230.path=tests/fixtures/context-management/all-present/.specify/tools.md
file.230.verdict=skipped
file.230.reason=non-code-file
file.231.path=tests/fixtures/context-management/all-present/docs/constraints.md
file.231.verdict=skipped
file.231.reason=non-code-file
file.232.path=tests/fixtures/context-management/all-present/shared/declarations/facts/context-categories.yaml
file.232.verdict=skipped
file.232.reason=non-code-file
file.233.path=tests/fixtures/context-management/all-present/shared/declarations/facts/context-classes.yaml
file.233.verdict=skipped
file.233.reason=non-code-file
file.234.path=tests/fixtures/context-management/all-present/shared/declarations/facts/context-forms.yaml
file.234.verdict=skipped
file.234.reason=non-code-file
file.235.path=tests/fixtures/context-management/all-present/shared/declarations/facts/context-layers.yaml
file.235.verdict=skipped
file.235.reason=non-code-file
file.236.path=tests/fixtures/context-management/all-present/shared/definitions/context-management-definitions.md
file.236.verdict=skipped
file.236.reason=non-code-file
file.237.path=tests/fixtures/context-management/concept-missing/.specify/constitution.md
file.237.verdict=skipped
file.237.reason=non-code-file
file.238.path=tests/fixtures/context-management/concept-missing/.specify/glossary.md
file.238.verdict=skipped
file.238.reason=non-code-file
file.239.path=tests/fixtures/context-management/concept-missing/.specify/instructions.md
file.239.verdict=skipped
file.239.reason=non-code-file
file.240.path=tests/fixtures/context-management/concept-missing/.specify/knowledge/entry.md
file.240.verdict=skipped
file.240.reason=non-code-file
file.241.path=tests/fixtures/context-management/concept-missing/.specify/session/entry.md
file.241.verdict=skipped
file.241.reason=non-code-file
file.242.path=tests/fixtures/context-management/concept-missing/.specify/shared/definitions/fixture-definitions.md
file.242.verdict=skipped
file.242.reason=non-code-file
file.243.path=tests/fixtures/context-management/concept-missing/.specify/shared/workflow/user-input-protocol.md
file.243.verdict=skipped
file.243.reason=non-code-file
file.244.path=tests/fixtures/context-management/concept-missing/.specify/skills.md
file.244.verdict=skipped
file.244.reason=non-code-file
file.245.path=tests/fixtures/context-management/concept-missing/.specify/specs/110-context-management/requirements.md
file.245.verdict=skipped
file.245.reason=non-code-file
file.246.path=tests/fixtures/context-management/concept-missing/.specify/tools.md
file.246.verdict=skipped
file.246.reason=non-code-file
file.247.path=tests/fixtures/context-management/concept-missing/docs/constraints.md
file.247.verdict=skipped
file.247.reason=non-code-file
file.248.path=tests/fixtures/context-management/concept-missing/shared/declarations/facts/context-categories.yaml
file.248.verdict=skipped
file.248.reason=non-code-file
file.249.path=tests/fixtures/context-management/concept-missing/shared/declarations/facts/context-classes.yaml
file.249.verdict=skipped
file.249.reason=non-code-file
file.250.path=tests/fixtures/context-management/concept-missing/shared/declarations/facts/context-forms.yaml
file.250.verdict=skipped
file.250.reason=non-code-file
file.251.path=tests/fixtures/context-management/concept-missing/shared/declarations/facts/context-layers.yaml
file.251.verdict=skipped
file.251.reason=non-code-file
file.252.path=tests/fixtures/context-management/concept-missing/shared/definitions/context-management-definitions.md
file.252.verdict=skipped
file.252.reason=non-code-file
file.253.path=tests/fixtures/context-management/declaration-missing/.specify/constitution.md
file.253.verdict=skipped
file.253.reason=non-code-file
file.254.path=tests/fixtures/context-management/declaration-missing/.specify/glossary.md
file.254.verdict=skipped
file.254.reason=non-code-file
file.255.path=tests/fixtures/context-management/declaration-missing/.specify/instructions.md
file.255.verdict=skipped
file.255.reason=non-code-file
file.256.path=tests/fixtures/context-management/declaration-missing/.specify/knowledge/entry.md
file.256.verdict=skipped
file.256.reason=non-code-file
file.257.path=tests/fixtures/context-management/declaration-missing/.specify/session/entry.md
file.257.verdict=skipped
file.257.reason=non-code-file
file.258.path=tests/fixtures/context-management/declaration-missing/.specify/shared/definitions/fixture-definitions.md
file.258.verdict=skipped
file.258.reason=non-code-file
file.259.path=tests/fixtures/context-management/declaration-missing/.specify/shared/workflow/user-input-protocol.md
file.259.verdict=skipped
file.259.reason=non-code-file
file.260.path=tests/fixtures/context-management/declaration-missing/.specify/skills.md
file.260.verdict=skipped
file.260.reason=non-code-file
file.261.path=tests/fixtures/context-management/declaration-missing/.specify/specs/110-context-management/requirements.md
file.261.verdict=skipped
file.261.reason=non-code-file
file.262.path=tests/fixtures/context-management/declaration-missing/.specify/tools.md
file.262.verdict=skipped
file.262.reason=non-code-file
file.263.path=tests/fixtures/context-management/declaration-missing/docs/constraints.md
file.263.verdict=skipped
file.263.reason=non-code-file
file.264.path=tests/fixtures/context-management/declaration-missing/shared/declarations/facts/context-categories.yaml
file.264.verdict=skipped
file.264.reason=non-code-file
file.265.path=tests/fixtures/context-management/declaration-missing/shared/declarations/facts/context-classes.yaml
file.265.verdict=skipped
file.265.reason=non-code-file
file.266.path=tests/fixtures/context-management/declaration-missing/shared/declarations/facts/context-layers.yaml
file.266.verdict=skipped
file.266.reason=non-code-file
file.267.path=tests/fixtures/context-management/declaration-missing/shared/definitions/context-management-definitions.md
file.267.verdict=skipped
file.267.reason=non-code-file
file.268.path=tests/fixtures/context-management/declaration-unknown-member/.specify/constitution.md
file.268.verdict=skipped
file.268.reason=non-code-file
file.269.path=tests/fixtures/context-management/declaration-unknown-member/.specify/glossary.md
file.269.verdict=skipped
file.269.reason=non-code-file
file.270.path=tests/fixtures/context-management/declaration-unknown-member/.specify/instructions.md
file.270.verdict=skipped
file.270.reason=non-code-file
file.271.path=tests/fixtures/context-management/declaration-unknown-member/.specify/knowledge/entry.md
file.271.verdict=skipped
file.271.reason=non-code-file
file.272.path=tests/fixtures/context-management/declaration-unknown-member/.specify/session/entry.md
file.272.verdict=skipped
file.272.reason=non-code-file
file.273.path=tests/fixtures/context-management/declaration-unknown-member/.specify/shared/definitions/fixture-definitions.md
file.273.verdict=skipped
file.273.reason=non-code-file
file.274.path=tests/fixtures/context-management/declaration-unknown-member/.specify/shared/workflow/user-input-protocol.md
file.274.verdict=skipped
file.274.reason=non-code-file
file.275.path=tests/fixtures/context-management/declaration-unknown-member/.specify/skills.md
file.275.verdict=skipped
file.275.reason=non-code-file
file.276.path=tests/fixtures/context-management/declaration-unknown-member/.specify/specs/110-context-management/requirements.md
file.276.verdict=skipped
file.276.reason=non-code-file
file.277.path=tests/fixtures/context-management/declaration-unknown-member/.specify/tools.md
file.277.verdict=skipped
file.277.reason=non-code-file
file.278.path=tests/fixtures/context-management/declaration-unknown-member/docs/constraints.md
file.278.verdict=skipped
file.278.reason=non-code-file
file.279.path=tests/fixtures/context-management/declaration-unknown-member/shared/declarations/facts/context-categories.yaml
file.279.verdict=skipped
file.279.reason=non-code-file
file.280.path=tests/fixtures/context-management/declaration-unknown-member/shared/declarations/facts/context-classes.yaml
file.280.verdict=skipped
file.280.reason=non-code-file
file.281.path=tests/fixtures/context-management/declaration-unknown-member/shared/declarations/facts/context-forms.yaml
file.281.verdict=skipped
file.281.reason=non-code-file
file.282.path=tests/fixtures/context-management/declaration-unknown-member/shared/declarations/facts/context-layers.yaml
file.282.verdict=skipped
file.282.reason=non-code-file
file.283.path=tests/fixtures/context-management/declaration-unknown-member/shared/definitions/context-management-definitions.md
file.283.verdict=skipped
file.283.reason=non-code-file
file.284.path=tests/fixtures/context-management/violation-cap-missing/.specify/constitution.md
file.284.verdict=skipped
file.284.reason=non-code-file
file.285.path=tests/fixtures/context-management/violation-cap-missing/.specify/glossary.md
file.285.verdict=skipped
file.285.reason=non-code-file
file.286.path=tests/fixtures/context-management/violation-cap-missing/.specify/instructions.md
file.286.verdict=skipped
file.286.reason=non-code-file
file.287.path=tests/fixtures/context-management/violation-cap-missing/.specify/knowledge/entry.md
file.287.verdict=skipped
file.287.reason=non-code-file
file.288.path=tests/fixtures/context-management/violation-cap-missing/.specify/session/entry.md
file.288.verdict=skipped
file.288.reason=non-code-file
file.289.path=tests/fixtures/context-management/violation-cap-missing/.specify/shared/definitions/fixture-definitions.md
file.289.verdict=skipped
file.289.reason=non-code-file
file.290.path=tests/fixtures/context-management/violation-cap-missing/.specify/shared/workflow/user-input-protocol.md
file.290.verdict=skipped
file.290.reason=non-code-file
file.291.path=tests/fixtures/context-management/violation-cap-missing/.specify/skills.md
file.291.verdict=skipped
file.291.reason=non-code-file
file.292.path=tests/fixtures/context-management/violation-cap-missing/.specify/specs/110-context-management/requirements.md
file.292.verdict=skipped
file.292.reason=non-code-file
file.293.path=tests/fixtures/context-management/violation-cap-missing/.specify/tools.md
file.293.verdict=skipped
file.293.reason=non-code-file
file.294.path=tests/fixtures/context-management/violation-cap-missing/docs/constraints.md
file.294.verdict=skipped
file.294.reason=non-code-file
file.295.path=tests/fixtures/context-management/violation-cap-missing/shared/declarations/facts/context-categories.yaml
file.295.verdict=skipped
file.295.reason=non-code-file
file.296.path=tests/fixtures/context-management/violation-cap-missing/shared/declarations/facts/context-classes.yaml
file.296.verdict=skipped
file.296.reason=non-code-file
file.297.path=tests/fixtures/context-management/violation-cap-missing/shared/declarations/facts/context-forms.yaml
file.297.verdict=skipped
file.297.reason=non-code-file
file.298.path=tests/fixtures/context-management/violation-cap-missing/shared/declarations/facts/context-layers.yaml
file.298.verdict=skipped
file.298.reason=non-code-file
file.299.path=tests/fixtures/context-management/violation-cap-missing/shared/definitions/context-management-definitions.md
file.299.verdict=skipped
file.299.reason=non-code-file
file.300.path=tests/fixtures/context-management/violation-category-column/.specify/constitution.md
file.300.verdict=skipped
file.300.reason=non-code-file
file.301.path=tests/fixtures/context-management/violation-category-column/.specify/glossary.md
file.301.verdict=skipped
file.301.reason=non-code-file
file.302.path=tests/fixtures/context-management/violation-category-column/.specify/instructions.md
file.302.verdict=skipped
file.302.reason=non-code-file
file.303.path=tests/fixtures/context-management/violation-category-column/.specify/knowledge/entry.md
file.303.verdict=skipped
file.303.reason=non-code-file
file.304.path=tests/fixtures/context-management/violation-category-column/.specify/session/entry.md
file.304.verdict=skipped
file.304.reason=non-code-file
file.305.path=tests/fixtures/context-management/violation-category-column/.specify/shared/definitions/fixture-definitions.md
file.305.verdict=skipped
file.305.reason=non-code-file
file.306.path=tests/fixtures/context-management/violation-category-column/.specify/shared/workflow/user-input-protocol.md
file.306.verdict=skipped
file.306.reason=non-code-file
file.307.path=tests/fixtures/context-management/violation-category-column/.specify/skills.md
file.307.verdict=skipped
file.307.reason=non-code-file
file.308.path=tests/fixtures/context-management/violation-category-column/.specify/specs/110-context-management/requirements.md
file.308.verdict=skipped
file.308.reason=non-code-file
file.309.path=tests/fixtures/context-management/violation-category-column/.specify/tools.md
file.309.verdict=skipped
file.309.reason=non-code-file
file.310.path=tests/fixtures/context-management/violation-category-column/docs/constraints.md
file.310.verdict=skipped
file.310.reason=non-code-file
file.311.path=tests/fixtures/context-management/violation-category-column/shared/declarations/facts/context-categories.yaml
file.311.verdict=skipped
file.311.reason=non-code-file
file.312.path=tests/fixtures/context-management/violation-category-column/shared/declarations/facts/context-classes.yaml
file.312.verdict=skipped
file.312.reason=non-code-file
file.313.path=tests/fixtures/context-management/violation-category-column/shared/declarations/facts/context-forms.yaml
file.313.verdict=skipped
file.313.reason=non-code-file
file.314.path=tests/fixtures/context-management/violation-category-column/shared/declarations/facts/context-layers.yaml
file.314.verdict=skipped
file.314.reason=non-code-file
file.315.path=tests/fixtures/context-management/violation-category-column/shared/definitions/context-management-definitions.md
file.315.verdict=skipped
file.315.reason=non-code-file
file.316.path=tests/fixtures/context-management/violation-duplicate-class/.specify/constitution.md
file.316.verdict=skipped
file.316.reason=non-code-file
file.317.path=tests/fixtures/context-management/violation-duplicate-class/.specify/glossary.md
file.317.verdict=skipped
file.317.reason=non-code-file
file.318.path=tests/fixtures/context-management/violation-duplicate-class/.specify/instructions.md
file.318.verdict=skipped
file.318.reason=non-code-file
file.319.path=tests/fixtures/context-management/violation-duplicate-class/.specify/knowledge/entry.md
file.319.verdict=skipped
file.319.reason=non-code-file
file.320.path=tests/fixtures/context-management/violation-duplicate-class/.specify/session/entry.md
file.320.verdict=skipped
file.320.reason=non-code-file
file.321.path=tests/fixtures/context-management/violation-duplicate-class/.specify/shared/definitions/fixture-definitions.md
file.321.verdict=skipped
file.321.reason=non-code-file
file.322.path=tests/fixtures/context-management/violation-duplicate-class/.specify/shared/workflow/user-input-protocol.md
file.322.verdict=skipped
file.322.reason=non-code-file
file.323.path=tests/fixtures/context-management/violation-duplicate-class/.specify/skills.md
file.323.verdict=skipped
file.323.reason=non-code-file
file.324.path=tests/fixtures/context-management/violation-duplicate-class/.specify/specs/110-context-management/requirements.md
file.324.verdict=skipped
file.324.reason=non-code-file
file.325.path=tests/fixtures/context-management/violation-duplicate-class/.specify/tools.md
file.325.verdict=skipped
file.325.reason=non-code-file
file.326.path=tests/fixtures/context-management/violation-duplicate-class/docs/constraints.md
file.326.verdict=skipped
file.326.reason=non-code-file
file.327.path=tests/fixtures/context-management/violation-duplicate-class/shared/declarations/facts/context-categories.yaml
file.327.verdict=skipped
file.327.reason=non-code-file
file.328.path=tests/fixtures/context-management/violation-duplicate-class/shared/declarations/facts/context-classes.yaml
file.328.verdict=skipped
file.328.reason=non-code-file
file.329.path=tests/fixtures/context-management/violation-duplicate-class/shared/declarations/facts/context-forms.yaml
file.329.verdict=skipped
file.329.reason=non-code-file
file.330.path=tests/fixtures/context-management/violation-duplicate-class/shared/declarations/facts/context-layers.yaml
file.330.verdict=skipped
file.330.reason=non-code-file
file.331.path=tests/fixtures/context-management/violation-duplicate-class/shared/definitions/context-management-definitions.md
file.331.verdict=skipped
file.331.reason=non-code-file
file.332.path=tests/fixtures/context-management/violation-empty-layer/.specify/constitution.md
file.332.verdict=skipped
file.332.reason=non-code-file
file.333.path=tests/fixtures/context-management/violation-empty-layer/.specify/glossary.md
file.333.verdict=skipped
file.333.reason=non-code-file
file.334.path=tests/fixtures/context-management/violation-empty-layer/.specify/instructions.md
file.334.verdict=skipped
file.334.reason=non-code-file
file.335.path=tests/fixtures/context-management/violation-empty-layer/.specify/knowledge/entry.md
file.335.verdict=skipped
file.335.reason=non-code-file
file.336.path=tests/fixtures/context-management/violation-empty-layer/.specify/session/entry.md
file.336.verdict=skipped
file.336.reason=non-code-file
file.337.path=tests/fixtures/context-management/violation-empty-layer/.specify/shared/definitions/fixture-definitions.md
file.337.verdict=skipped
file.337.reason=non-code-file
file.338.path=tests/fixtures/context-management/violation-empty-layer/.specify/shared/workflow/user-input-protocol.md
file.338.verdict=skipped
file.338.reason=non-code-file
file.339.path=tests/fixtures/context-management/violation-empty-layer/.specify/skills.md
file.339.verdict=skipped
file.339.reason=non-code-file
file.340.path=tests/fixtures/context-management/violation-empty-layer/.specify/specs/110-context-management/requirements.md
file.340.verdict=skipped
file.340.reason=non-code-file
file.341.path=tests/fixtures/context-management/violation-empty-layer/.specify/tools.md
file.341.verdict=skipped
file.341.reason=non-code-file
file.342.path=tests/fixtures/context-management/violation-empty-layer/docs/constraints.md
file.342.verdict=skipped
file.342.reason=non-code-file
file.343.path=tests/fixtures/context-management/violation-empty-layer/shared/declarations/facts/context-categories.yaml
file.343.verdict=skipped
file.343.reason=non-code-file
file.344.path=tests/fixtures/context-management/violation-empty-layer/shared/declarations/facts/context-classes.yaml
file.344.verdict=skipped
file.344.reason=non-code-file
file.345.path=tests/fixtures/context-management/violation-empty-layer/shared/declarations/facts/context-forms.yaml
file.345.verdict=skipped
file.345.reason=non-code-file
file.346.path=tests/fixtures/context-management/violation-empty-layer/shared/declarations/facts/context-layers.yaml
file.346.verdict=skipped
file.346.reason=non-code-file
file.347.path=tests/fixtures/context-management/violation-empty-layer/shared/definitions/context-management-definitions.md
file.347.verdict=skipped
file.347.reason=non-code-file
file.348.path=tests/fixtures/context-management/violation-layer-form/.specify/constitution.md
file.348.verdict=skipped
file.348.reason=non-code-file
file.349.path=tests/fixtures/context-management/violation-layer-form/.specify/glossary.md
file.349.verdict=skipped
file.349.reason=non-code-file
file.350.path=tests/fixtures/context-management/violation-layer-form/.specify/instructions.md
file.350.verdict=skipped
file.350.reason=non-code-file
file.351.path=tests/fixtures/context-management/violation-layer-form/.specify/knowledge/entry.md
file.351.verdict=skipped
file.351.reason=non-code-file
file.352.path=tests/fixtures/context-management/violation-layer-form/.specify/session/entry.md
file.352.verdict=skipped
file.352.reason=non-code-file
file.353.path=tests/fixtures/context-management/violation-layer-form/.specify/shared/definitions/fixture-definitions.md
file.353.verdict=skipped
file.353.reason=non-code-file
file.354.path=tests/fixtures/context-management/violation-layer-form/.specify/shared/workflow/user-input-protocol.md
file.354.verdict=skipped
file.354.reason=non-code-file
file.355.path=tests/fixtures/context-management/violation-layer-form/.specify/skills.md
file.355.verdict=skipped
file.355.reason=non-code-file
file.356.path=tests/fixtures/context-management/violation-layer-form/.specify/specs/110-context-management/requirements.md
file.356.verdict=skipped
file.356.reason=non-code-file
file.357.path=tests/fixtures/context-management/violation-layer-form/.specify/tools.md
file.357.verdict=skipped
file.357.reason=non-code-file
file.358.path=tests/fixtures/context-management/violation-layer-form/docs/constraints.md
file.358.verdict=skipped
file.358.reason=non-code-file
file.359.path=tests/fixtures/context-management/violation-layer-form/shared/declarations/facts/context-categories.yaml
file.359.verdict=skipped
file.359.reason=non-code-file
file.360.path=tests/fixtures/context-management/violation-layer-form/shared/declarations/facts/context-classes.yaml
file.360.verdict=skipped
file.360.reason=non-code-file
file.361.path=tests/fixtures/context-management/violation-layer-form/shared/declarations/facts/context-forms.yaml
file.361.verdict=skipped
file.361.reason=non-code-file
file.362.path=tests/fixtures/context-management/violation-layer-form/shared/declarations/facts/context-layers.yaml
file.362.verdict=skipped
file.362.reason=non-code-file
file.363.path=tests/fixtures/context-management/violation-layer-form/shared/definitions/context-management-definitions.md
file.363.verdict=skipped
file.363.reason=non-code-file
file.364.path=tests/fixtures/context-management/violation-roster-mismatch/.specify/constitution.md
file.364.verdict=skipped
file.364.reason=non-code-file
file.365.path=tests/fixtures/context-management/violation-roster-mismatch/.specify/glossary.md
file.365.verdict=skipped
file.365.reason=non-code-file
file.366.path=tests/fixtures/context-management/violation-roster-mismatch/.specify/instructions.md
file.366.verdict=skipped
file.366.reason=non-code-file
file.367.path=tests/fixtures/context-management/violation-roster-mismatch/.specify/knowledge/entry.md
file.367.verdict=skipped
file.367.reason=non-code-file
file.368.path=tests/fixtures/context-management/violation-roster-mismatch/.specify/session/entry.md
file.368.verdict=skipped
file.368.reason=non-code-file
file.369.path=tests/fixtures/context-management/violation-roster-mismatch/.specify/shared/definitions/fixture-definitions.md
file.369.verdict=skipped
file.369.reason=non-code-file
file.370.path=tests/fixtures/context-management/violation-roster-mismatch/.specify/shared/workflow/user-input-protocol.md
file.370.verdict=skipped
file.370.reason=non-code-file
file.371.path=tests/fixtures/context-management/violation-roster-mismatch/.specify/skills.md
file.371.verdict=skipped
file.371.reason=non-code-file
file.372.path=tests/fixtures/context-management/violation-roster-mismatch/.specify/specs/110-context-management/requirements.md
file.372.verdict=skipped
file.372.reason=non-code-file
file.373.path=tests/fixtures/context-management/violation-roster-mismatch/.specify/tools.md
file.373.verdict=skipped
file.373.reason=non-code-file
file.374.path=tests/fixtures/context-management/violation-roster-mismatch/docs/constraints.md
file.374.verdict=skipped
file.374.reason=non-code-file
file.375.path=tests/fixtures/context-management/violation-roster-mismatch/shared/declarations/facts/context-categories.yaml
file.375.verdict=skipped
file.375.reason=non-code-file
file.376.path=tests/fixtures/context-management/violation-roster-mismatch/shared/declarations/facts/context-classes.yaml
file.376.verdict=skipped
file.376.reason=non-code-file
file.377.path=tests/fixtures/context-management/violation-roster-mismatch/shared/declarations/facts/context-forms.yaml
file.377.verdict=skipped
file.377.reason=non-code-file
file.378.path=tests/fixtures/context-management/violation-roster-mismatch/shared/declarations/facts/context-layers.yaml
file.378.verdict=skipped
file.378.reason=non-code-file
file.379.path=tests/fixtures/context-management/violation-roster-mismatch/shared/definitions/context-management-definitions.md
file.379.verdict=skipped
file.379.reason=non-code-file
file.380.path=tests/fixtures/context-management/violation-roster-order/.specify/constitution.md
file.380.verdict=skipped
file.380.reason=non-code-file
file.381.path=tests/fixtures/context-management/violation-roster-order/.specify/glossary.md
file.381.verdict=skipped
file.381.reason=non-code-file
file.382.path=tests/fixtures/context-management/violation-roster-order/.specify/instructions.md
file.382.verdict=skipped
file.382.reason=non-code-file
file.383.path=tests/fixtures/context-management/violation-roster-order/.specify/knowledge/entry.md
file.383.verdict=skipped
file.383.reason=non-code-file
file.384.path=tests/fixtures/context-management/violation-roster-order/.specify/session/entry.md
file.384.verdict=skipped
file.384.reason=non-code-file
file.385.path=tests/fixtures/context-management/violation-roster-order/.specify/shared/definitions/fixture-definitions.md
file.385.verdict=skipped
file.385.reason=non-code-file
file.386.path=tests/fixtures/context-management/violation-roster-order/.specify/shared/workflow/user-input-protocol.md
file.386.verdict=skipped
file.386.reason=non-code-file
file.387.path=tests/fixtures/context-management/violation-roster-order/.specify/skills.md
file.387.verdict=skipped
file.387.reason=non-code-file
file.388.path=tests/fixtures/context-management/violation-roster-order/.specify/specs/110-context-management/requirements.md
file.388.verdict=skipped
file.388.reason=non-code-file
file.389.path=tests/fixtures/context-management/violation-roster-order/.specify/tools.md
file.389.verdict=skipped
file.389.reason=non-code-file
file.390.path=tests/fixtures/context-management/violation-roster-order/docs/constraints.md
file.390.verdict=skipped
file.390.reason=non-code-file
file.391.path=tests/fixtures/context-management/violation-roster-order/shared/declarations/facts/context-categories.yaml
file.391.verdict=skipped
file.391.reason=non-code-file
file.392.path=tests/fixtures/context-management/violation-roster-order/shared/declarations/facts/context-classes.yaml
file.392.verdict=skipped
file.392.reason=non-code-file
file.393.path=tests/fixtures/context-management/violation-roster-order/shared/declarations/facts/context-forms.yaml
file.393.verdict=skipped
file.393.reason=non-code-file
file.394.path=tests/fixtures/context-management/violation-roster-order/shared/declarations/facts/context-layers.yaml
file.394.verdict=skipped
file.394.reason=non-code-file
file.395.path=tests/fixtures/context-management/violation-roster-order/shared/definitions/context-management-definitions.md
file.395.verdict=skipped
file.395.reason=non-code-file
file.396.path=tests/fixtures/context-management/violation-unknown-form/.specify/constitution.md
file.396.verdict=skipped
file.396.reason=non-code-file
file.397.path=tests/fixtures/context-management/violation-unknown-form/.specify/glossary.md
file.397.verdict=skipped
file.397.reason=non-code-file
file.398.path=tests/fixtures/context-management/violation-unknown-form/.specify/instructions.md
file.398.verdict=skipped
file.398.reason=non-code-file
file.399.path=tests/fixtures/context-management/violation-unknown-form/.specify/knowledge/entry.md
file.399.verdict=skipped
file.399.reason=non-code-file
file.400.path=tests/fixtures/context-management/violation-unknown-form/.specify/session/entry.md
file.400.verdict=skipped
file.400.reason=non-code-file
file.401.path=tests/fixtures/context-management/violation-unknown-form/.specify/shared/definitions/fixture-definitions.md
file.401.verdict=skipped
file.401.reason=non-code-file
file.402.path=tests/fixtures/context-management/violation-unknown-form/.specify/shared/workflow/user-input-protocol.md
file.402.verdict=skipped
file.402.reason=non-code-file
file.403.path=tests/fixtures/context-management/violation-unknown-form/.specify/skills.md
file.403.verdict=skipped
file.403.reason=non-code-file
file.404.path=tests/fixtures/context-management/violation-unknown-form/.specify/specs/110-context-management/requirements.md
file.404.verdict=skipped
file.404.reason=non-code-file
file.405.path=tests/fixtures/context-management/violation-unknown-form/.specify/tools.md
file.405.verdict=skipped
file.405.reason=non-code-file
file.406.path=tests/fixtures/context-management/violation-unknown-form/docs/constraints.md
file.406.verdict=skipped
file.406.reason=non-code-file
file.407.path=tests/fixtures/context-management/violation-unknown-form/shared/declarations/facts/context-categories.yaml
file.407.verdict=skipped
file.407.reason=non-code-file
file.408.path=tests/fixtures/context-management/violation-unknown-form/shared/declarations/facts/context-classes.yaml
file.408.verdict=skipped
file.408.reason=non-code-file
file.409.path=tests/fixtures/context-management/violation-unknown-form/shared/declarations/facts/context-forms.yaml
file.409.verdict=skipped
file.409.reason=non-code-file
file.410.path=tests/fixtures/context-management/violation-unknown-form/shared/declarations/facts/context-layers.yaml
file.410.verdict=skipped
file.410.reason=non-code-file
file.411.path=tests/fixtures/context-management/violation-unknown-form/shared/definitions/context-management-definitions.md
file.411.verdict=skipped
file.411.reason=non-code-file
file.412.path=tests/fixtures/context-management/violation-unknown-layer/.specify/constitution.md
file.412.verdict=skipped
file.412.reason=non-code-file
file.413.path=tests/fixtures/context-management/violation-unknown-layer/.specify/glossary.md
file.413.verdict=skipped
file.413.reason=non-code-file
file.414.path=tests/fixtures/context-management/violation-unknown-layer/.specify/instructions.md
file.414.verdict=skipped
file.414.reason=non-code-file
file.415.path=tests/fixtures/context-management/violation-unknown-layer/.specify/knowledge/entry.md
file.415.verdict=skipped
file.415.reason=non-code-file
file.416.path=tests/fixtures/context-management/violation-unknown-layer/.specify/session/entry.md
file.416.verdict=skipped
file.416.reason=non-code-file
file.417.path=tests/fixtures/context-management/violation-unknown-layer/.specify/shared/definitions/fixture-definitions.md
file.417.verdict=skipped
file.417.reason=non-code-file
file.418.path=tests/fixtures/context-management/violation-unknown-layer/.specify/shared/workflow/user-input-protocol.md
file.418.verdict=skipped
file.418.reason=non-code-file
file.419.path=tests/fixtures/context-management/violation-unknown-layer/.specify/skills.md
file.419.verdict=skipped
file.419.reason=non-code-file
file.420.path=tests/fixtures/context-management/violation-unknown-layer/.specify/specs/110-context-management/requirements.md
file.420.verdict=skipped
file.420.reason=non-code-file
file.421.path=tests/fixtures/context-management/violation-unknown-layer/.specify/tools.md
file.421.verdict=skipped
file.421.reason=non-code-file
file.422.path=tests/fixtures/context-management/violation-unknown-layer/docs/constraints.md
file.422.verdict=skipped
file.422.reason=non-code-file
file.423.path=tests/fixtures/context-management/violation-unknown-layer/shared/declarations/facts/context-categories.yaml
file.423.verdict=skipped
file.423.reason=non-code-file
file.424.path=tests/fixtures/context-management/violation-unknown-layer/shared/declarations/facts/context-classes.yaml
file.424.verdict=skipped
file.424.reason=non-code-file
file.425.path=tests/fixtures/context-management/violation-unknown-layer/shared/declarations/facts/context-forms.yaml
file.425.verdict=skipped
file.425.reason=non-code-file
file.426.path=tests/fixtures/context-management/violation-unknown-layer/shared/declarations/facts/context-layers.yaml
file.426.verdict=skipped
file.426.reason=non-code-file
file.427.path=tests/fixtures/context-management/violation-unknown-layer/shared/definitions/context-management-definitions.md
file.427.verdict=skipped
file.427.reason=non-code-file
file.428.path=tests/fixtures/context_management_support.py
file.428.verdict=reviewed
file.429.path=tests/integration/test_context_management_init.py
file.429.verdict=reviewed
<!-- coverage-receipt:end -->
