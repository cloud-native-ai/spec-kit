# Code Review Report — 代码段 (code segment)

| 属性 | 值 |
|------|-----|
| **分支** | `082-mechanism-policy-separation` |
| **基准** | `3ffeb26e4880f134f7a5e220ecbffb869f165632` (`3ffeb26e`) |
| **目标** | `875be2c7f73679a0d1ec108afed1df4e32c8a766` (`875be2c7`) |
| **基准来源** | `feature-first-commit` |
| **渲染模式** | `renderer: text` |
| **Reviewer** | `Qiming, Liu` |
| **日期** | `2026-11-05T11:08:14Z` |

## 变更概览

```
 .opencode/agents/dogfood-executor.md               |   2 +-
 .opencode/agents/framework-engineer.md             |   2 +-
 .opencode/agents/sdd-executor.md                   |   2 +-
 .opencode/agents/sdd-requirements-executor.md      |   2 +-
 .opencode/agents/sdd-setup-executor.md             |   2 +-
 .opencode/agents/skill-verifier.md                 |   2 +-
 .opencode/agents/structure-adjuster.md             |   2 +-
 .qoder/agents/dogfood-executor.agent.md            |   2 +-
 .qoder/agents/framework-engineer.agent.md          |   2 +-
 .qoder/agents/sdd-executor.agent.md                |   2 +-
 .qoder/agents/sdd-requirements-executor.agent.md   |   2 +-
 .qoder/agents/sdd-setup-executor.agent.md          |   2 +-
 .qoder/agents/skill-verifier.agent.md              |   2 +-
 .qoder/agents/structure-adjuster.agent.md          |   2 +-
 .specify/agents/.render-manifest.json              |  30 +-
 .../agents/instances/dogfood-executor.agent.md     |   2 +-
 .../agents/instances/framework-engineer.agent.md   |   2 +-
 .../instances/sdd-requirements-executor.agent.md   |   2 +-
 .../agents/instances/sdd-setup-executor.agent.md   |   2 +-
 .specify/agents/templates/sdd-executor.agent.md    |   2 +-
 .specify/agents/templates/skill-verifier.agent.md  |   2 +-
 .../agents/templates/structure-adjuster.agent.md   |   2 +-
 .specify/memory/features.md                        |   5 +-
 .specify/memory/features/082.md                    |  88 ++
 .specify/memory/glossary.md                        |   1 +
 .../shared/definitions/flow-class-definitions.md   |   1 +
 .specify/shared/definitions/framework-map.md       |   2 +-
 .../definitions/mechanism-policy-definitions.md    | 351 ++++++++
 .specify/shared/definitions/probe-definitions.md   |   1 +
 .../definitions/skill-reference-definitions.md     | 133 +++
 .specify/shared/workflow/execution-topology.md     |   1 +
 .../shared/workflow/external-dispatch-recipes.md   |   6 +-
 .specify/skills/coaching-skills/SKILL.md           |  56 +-
 .specify/skills/coaching-skills/data-model.md      |  45 +-
 .../coaching-skills/references/prompt-templates.md |  14 +-
 .specify/skills/create-skills/SKILL.md             |   9 +-
 .../references/mechanism-policy-check.md           |  28 +
 .specify/skills/improve-skills/SKILL.md            |   7 +-
 .../improve-skills/references/loop-playbook.md     |   6 +
 .../agent-capacity-knowledge-manager-template.md   |   2 +-
 .../agent-capacity-module-designer-template.md     |   2 +-
 .../agent-capacity-qa-engineer-template.md         |   2 +-
 ...agent-capacity-requirements-analyst-template.md |   2 +-
 .../agent-capacity-system-designer-template.md     |   2 +-
 .../agent-capacity-test-engineer-template.md       |   2 +-
 .../agent-capacity-ux-analyst-template.md          |   2 +-
 .../templates/agent-project-custom-template.md     |   2 +-
 .../agents/agent-team-supervisor-template.md       |   2 +-
 .specify/skills/internal/run-agent/SKILL.md        |   2 +-
 .specify/skills/internal/run-skills/SKILL.md       |   4 +-
 .specify/skills/merge-skills/SKILL.md              |   9 +-
 .../merge-skills/references/provenance-record.md   |  10 +-
 .specify/skills/sdd-loop-driver/SKILL.md           |   6 +-
 .../sdd-loop-driver/references/dispatch-recipes.md |   4 +-
 .../sdd-loop-driver/references/efficiency-model.md |   6 +-
 .../sdd-loop-driver/references/stage-prompts.md    |   4 +-
 .../sdd-loop-driver/references/watch-model.md      |   2 +-
 .../sdd-loop-driver/scripts/admission-check.py     |   4 +-
 .../sdd-loop-driver/scripts/decomposition-check.py |   4 +-
 .../skills/sdd-loop-driver/scripts/loop-state.py   |  15 +-
 .specify/skills/sdd-project-setup/SKILL.md         |   6 +-
 .../sdd-project-setup/references/setup-recipes.md  |  18 +-
 .specify/skills/ssh-utils/SKILL.md                 | 131 +++
 .specify/skills/ssh-utils/references/pitfalls.md   |  77 ++
 .specify/skills/ssh-utils/references/recipes.md    |  98 +++
 .specify/skills/ssh-utils/scripts/ssh-exec.py      | 349 ++++++++
 .../baseline-failed.txt                            |  24 +
 .../checklists/quality-scope-update.md             | 153 ++++
 .../checklists/requirements.md                     |  89 ++
 .../contracts/guard-and-measurement.contract.md    | 172 ++++
 .../contracts/owner-document.contract.md           | 101 +++
 .../contracts/skill-reference.contract.md          | 148 ++++
 .../contracts/skill-wiring.contract.md             |  81 ++
 .../coverage-baseline.txt                          | 515 ++++++++++++
 .../082-mechanism-policy-separation/data-model.md  | 307 +++++++
 .../082-mechanism-policy-separation/feature-ref.md |  49 ++
 .../notes/pre-change-measurements.md               | 265 ++++++
 .../specs/082-mechanism-policy-separation/plan.md  | 527 ++++++++++++
 .../082-mechanism-policy-separation/quickstart.md  | 282 +++++++
 .../requirements.md                                | 318 +++++++
 .../082-mechanism-policy-separation/research.md    | 216 +++++
 .../specs/082-mechanism-policy-separation/tasks.md | 331 ++++++++
 .../test-evidence/analyze-repair-gates.txt         |  55 ++
 .../analyze-repair-stage-status.jsonl              |   1 +
 .../test-evidence/checklist-scope-update-gates.txt |  95 +++
 .../checklist-scope-update-stage-status.jsonl      |   1 +
 .../test-evidence/clarify-gates.txt                |  43 +
 .../clarify-scope-update-fixture-probe.txt         |  42 +
 .../clarify-scope-update-fixture.json              |  36 +
 .../test-evidence/clarify-scope-update-gates.txt   | 124 +++
 .../clarify-scope-update-stage-status.jsonl        |   1 +
 .../test-evidence/final-gates.txt                  | 350 ++++++++
 .../test-evidence/flow-class-lookup.txt            |   7 +
 .../fr-027-starting-point-verification.txt         |  70 ++
 .../test-evidence/implement-part1-baseline.txt     | 676 +++++++++++++++
 .../implement-part1-stage-status.jsonl             |   1 +
 .../test-evidence/implement-part2-green.txt        |   3 +
 .../test-evidence/implement-part2-red.txt          | 186 +++++
 .../implement-part2-stage-status.jsonl             |   1 +
 .../test-evidence/implement-part2-stage-status.txt |  39 +
 .../test-evidence/implement-part2-targeted.txt     |  14 +
 .../test-evidence/implement-part3-t017-red.txt     | 162 ++++
 .../test-evidence/implement-part3-t020-red.txt     |  52 ++
 .../implement-part3a-stage-status.jsonl            |   1 +
 .../test-evidence/implement-part3a-t017-green.txt  |  14 +
 .../implement-part3a-t018-consumption-wiring.txt   |  34 +
 .../test-evidence/implement-part3a-t019-green.txt  |  19 +
 .../test-evidence/implement-part3a-t020-green.txt  |  25 +
 .../implement-part3a-targeted-green.txt            |   3 +
 .../test-evidence/implement-part3a-targeted.txt    |  52 ++
 .../test-evidence/implement-part3b-t022.txt        |  12 +
 .../test-evidence/implement-part3b-t023-red.txt    |  10 +
 .../test-evidence/implement-part3b-t024-green.txt  |  35 +
 .../test-evidence/implement-part3b-targeted.txt    |  14 +
 .../test-evidence/implement-part4-red.txt          |  10 +
 .../implement-part4a-gm12-predicate-check.txt      |  73 ++
 .../implement-part4a-stage-status.jsonl            |   1 +
 .../test-evidence/implement-part4a-targeted.txt    | 107 +++
 .../test-evidence/implement-part4b-mirrors.txt     |  13 +
 .../implement-part4b-stage-status.jsonl            |   1 +
 .../test-evidence/implement-part4b-t029-green.txt  |   3 +
 .../test-evidence/implement-part4b-t029-red.txt    |  31 +
 .../implement-part4b-targeted-pre.txt              | 105 +++
 .../test-evidence/implement-part4b-targeted.txt    | 105 +++
 .../test-evidence/implement-part4b-wiring.txt      |  25 +
 .../test-evidence/implement-part5-red.txt          |   8 +
 .../implement-part5-stage-status.jsonl             |   1 +
 .../test-evidence/implement-part5-t035-green.txt   |  23 +
 .../test-evidence/implement-part5-t035-pre.txt     |  24 +
 .../test-evidence/implement-part5-t036-t037.txt    |  99 +++
 .../test-evidence/implement-part5-t038.txt         |  62 ++
 .../test-evidence/implement-part5-t039.txt         |  59 ++
 .../test-evidence/implement-part5-targeted.txt     |  69 ++
 .../implement-part6-stage-status.jsonl             |   1 +
 .../implement-part6-t041-t045-red.txt              | 117 +++
 .../test-evidence/implement-part6-targeted.txt     |   3 +
 .../implement-part7-stage-status.jsonl             |   1 +
 .../test-evidence/plan-scope-update-gates.txt      | 288 +++++++
 .../plan-scope-update-stage-status.jsonl           |   1 +
 .../test-evidence/plan2026-11-05-baseline.txt      |  68 ++
 .../test-evidence/plan2026-11-05-plan-gates.txt    | 399 +++++++++
 .../plan2026-11-05-stage-status.jsonl              |   1 +
 ...ements-scope-update-concurrent-impl-readout.txt |  59 ++
 .../requirements-scope-update-gates.txt            | 130 +++
 ...equirements-scope-update-mirror-observation.txt |  18 +
 .../requirements-scope-update-probe-tests.txt      |  20 +
 .../requirements-scope-update-stage-status.jsonl   |   1 +
 .../test-evidence/requirements-stage-status.jsonl  |   2 +
 .../test-evidence/requirements-u4-gates.txt        |  34 +
 .../review-078-coaching-regression.txt             |  12 +
 .../review-mirror-and-command-copies.txt           |  20 +
 .../test-evidence/review-sc-006-sc-009.txt         |  49 ++
 .../test-evidence/review-smoke-and-targeted.txt    |  14 +
 .../test-evidence/sc-001-2026-11-05.txt            | 224 +++++
 .../test-evidence/sc-002-2026-11-05.txt            | 185 +++++
 .../test-evidence/sc-003-2026-11-05.txt            | 300 +++++++
 .../test-evidence/sc-004-2026-11-05.txt            | 254 ++++++
 .../test-evidence/sc-005-2026-11-05.txt            | 200 +++++
 .../test-evidence/sc-006-2026-11-05.txt            | 107 +++
 .../test-evidence/sc-007-2026-11-05.txt            | 106 +++
 .../test-evidence/sc-008-2026-11-05.txt            | 103 +++
 .../test-evidence/sc-009-2026-11-05.txt            |  90 ++
 .../test-evidence/skill-shape-before-after.txt     |  71 ++
 .../test-evidence/tasks-scope-update-gates.txt     | 111 +++
 .../tasks-scope-update-stage-status.jsonl          |   1 +
 .../validate-requirements-scope-update.txt         |  13 +
 .../test-evidence/validate-requirements.txt        |  10 +
 .../verification.md                                | 229 +++++
 CHANGELOG.md                                       |  11 +
 agents/sdd-executor.agent.md                       |   2 +-
 agents/skill-verifier.agent.md                     |   2 +-
 agents/structure-adjuster.agent.md                 |   2 +-
 docs/reference/skills/sdd-loop-driver.md           |   2 +-
 docs/reference/skills/sdd-project-setup.md         |   1 +
 shared/definitions/flow-class-definitions.md       |   1 +
 shared/definitions/framework-map.md                |   2 +-
 shared/definitions/mechanism-policy-definitions.md | 351 ++++++++
 shared/definitions/probe-definitions.md            |   1 +
 shared/definitions/skill-reference-definitions.md  | 133 +++
 shared/workflow/execution-topology.md              |   1 +
 shared/workflow/external-dispatch-recipes.md       |   6 +-
 skills/external/coaching-skills/SKILL.md           |  56 +-
 skills/external/coaching-skills/data-model.md      |  45 +-
 .../coaching-skills/references/prompt-templates.md |  14 +-
 skills/external/create-skills/SKILL.md             |   9 +-
 .../references/mechanism-policy-check.md           |  28 +
 skills/external/improve-skills/SKILL.md            |   7 +-
 .../improve-skills/references/loop-playbook.md     |   6 +
 skills/external/merge-skills/SKILL.md              |   9 +-
 .../merge-skills/references/provenance-record.md   |  10 +-
 skills/external/sdd-loop-driver/SKILL.md           |   6 +-
 .../sdd-loop-driver/references/dispatch-recipes.md |   4 +-
 .../sdd-loop-driver/references/efficiency-model.md |   6 +-
 .../sdd-loop-driver/references/stage-prompts.md    |   4 +-
 .../sdd-loop-driver/references/watch-model.md      |   2 +-
 .../sdd-loop-driver/scripts/admission-check.py     |   4 +-
 .../sdd-loop-driver/scripts/decomposition-check.py |   4 +-
 .../external/sdd-loop-driver/scripts/loop-state.py |  15 +-
 skills/external/sdd-project-setup/SKILL.md         |   6 +-
 .../sdd-project-setup/references/setup-recipes.md  |  18 +-
 skills/external/ssh-utils/SKILL.md                 | 131 +++
 skills/external/ssh-utils/references/pitfalls.md   |  77 ++
 skills/external/ssh-utils/references/recipes.md    |  98 +++
 skills/external/ssh-utils/scripts/ssh-exec.py      | 349 ++++++++
 .../agent-capacity-knowledge-manager-template.md   |   2 +-
 .../agent-capacity-module-designer-template.md     |   2 +-
 .../agent-capacity-qa-engineer-template.md         |   2 +-
 ...agent-capacity-requirements-analyst-template.md |   2 +-
 .../agent-capacity-system-designer-template.md     |   2 +-
 .../agent-capacity-test-engineer-template.md       |   2 +-
 .../agent-capacity-ux-analyst-template.md          |   2 +-
 .../templates/agent-project-custom-template.md     |   2 +-
 .../agents/agent-team-supervisor-template.md       |   2 +-
 skills/internal/run-agent/SKILL.md                 |   2 +-
 skills/internal/run-skills/SKILL.md                |   4 +-
 tests/contract/skill_reference_matrix.py           | 493 +++++++++++
 tests/contract/test_bilingual_expression.py        |   7 +
 tests/contract/test_coaching_wiring_contract.py    |   8 +-
 tests/contract/test_expression_compatibility.py    |  83 +-
 tests/contract/test_expression_gate_wiring.py      |   9 +-
 tests/contract/test_flow_class_ledger.py           |  37 +-
 tests/contract/test_ledger_reconciliation.py       |   6 +-
 .../contract/test_mechanism_policy_decidability.py | 317 +++++++
 tests/contract/test_mechanism_policy_guard.py      | 676 +++++++++++++++
 .../test_mechanism_policy_missing_policy.py        | 269 ++++++
 tests/contract/test_mechanism_policy_owner_doc.py  | 307 +++++++
 tests/contract/test_mechanism_policy_ownership.py  | 462 +++++++++++
 .../contract/test_mechanism_policy_skill_wiring.py | 917 +++++++++++++++++++++
 tests/contract/test_migration_distribution.py      |  12 +-
 tests/contract/test_probe_nonentity_catalog.py     |   4 +-
 tests/contract/test_run_skills_wiring.py           |   9 +-
 tests/contract/test_sdd_loop_driver_efficiency.py  |   4 +-
 tests/contract/test_sdd_loop_driver_gates.py       |   4 +-
 tests/contract/test_sdd_loop_driver_skill.py       |   2 +-
 .../contract/test_skill_layer_visibility_guards.py |   8 +-
 .../test_skill_reference_command_surface.py        | 144 ++++
 tests/contract/test_skill_reference_consumers.py   | 457 ++++++++++
 tests/contract/test_skill_reference_failures.py    | 335 ++++++++
 tests/contract/test_skill_reference_grammar.py     | 453 ++++++++++
 tests/contract/test_skill_reference_matrix.py      | 241 ++++++
 tests/contract/test_ssh_utils_skill.py             | 139 ++++
 .../large/.specify/specs/013-large/tasks.md        |  30 +
 .../skill-reference/normalization-matrix.json      | 550 ++++++++++++
 tests/unit/test_admission_check.py                 |   8 +-
 tests/unit/test_decomposition_check.py             |  24 +-
 tests/unit/test_pre_analyze_check.py               |   2 +-
 246 files changed, 18620 insertions(+), 254 deletions(-)
```

---

## Review 意见


### 🟠 [IMPORTANT] tests/contract/skill_reference_matrix.py (Line 371)

> The normalization projection was repaired during review (875be2c7): a dev-canonical hit and its installed mirror now collapse to ONE hit before the layer test (FR-023(c) / V-33), and the dual-layer fixture was rebuilt from skills/internal + .specify/skills instead of a source-and-mirror pair. Residual risk: the live-tree rows (R07/R08/R17) still depend on the current layer distribution, so moving a skill between layers flips them; that fragility is disclosed in review.md F-082-RV-01.

<sub>19:09:45</sub>


### 🟠 [IMPORTANT] skills/external/coaching-skills/SKILL.md (Line 21)

> T032 had renamed the 078-owned parameter from trainee-name to trainee-reference, turning both 078 C1 contract tests red at the baseline. The review restored the owner's name in the source and regenerated the mirror; the 078 C1 pair is green again (review-078-coaching-regression.txt). The 078 contract remains the owner of this parameter; 082 must not rename it again.

<sub>19:09:45</sub>


### 🟢 [SUGGESTION] tests/fixtures/skill-reference/normalization-matrix.json (Line 1)

> The live rows are intentionally tree-state dependent (they read the repository's layer distribution). Keep the maintenance note in test_skill_reference_matrix.py and re-run SC-006 after any skill moves between the source and installed trees; a scratch-only matrix would remove the fragility but would stop testing the live ladder.

<sub>19:09:45</sub>


### 🟢 [SUGGESTION] shared/definitions/skill-reference-definitions.md (Line 89)

> Rule (c)'s example ('improve-skills present both in the dev canonical tree and in the installed mirror -> one hit') is the only statement that a source-plus-mirror pair is one hit, and the executable projection originally read it the other way. Consider promoting the example into an explicit 'mirror pair = one hit' sentence in the rule's first line so a future implementer cannot read the layer names as two hits.

<sub>19:09:45</sub>


### 👍 [PRAISE] tests/contract/test_mechanism_policy_guard.py (Line 140)

> The SC-003 guard is a strong closed-set carrier: baseline blobs by SHA, a comparison unit read from git, explicit disclosures for absorbed co-worktree paths, and three negative cases that each turn a named assertion red.

<sub>19:09:45</sub>


### 👍 [PRAISE] tests/contract/test_mechanism_policy_missing_policy.py (Line 206)

> The zero-write leg snapshots every file's sha256 plus the directory set before and after, and its negative case actually injects a write; the deterministic face mirrors the owner's read-judge-stop without pretending to execute the meta-skill.

<sub>19:09:45</sub>


### ⚪ [NITPICK] tests/contract/test_mechanism_policy_ownership.py (Line 204)

> The V-19 assertion still messages 'GM-03 rows 1-8' as if that were the whole in-unit set; rows 19-20 are in-unit too (absorbed coaching files). The logic is correct (V-19 needs only the member skill directories); the wording and the module docstring at line 17 are stale.

<sub>19:09:45</sub>






> **未提交范围（未评审）**: 28 个未提交路径未计入本次评审对象（.specify/memory/evidence/ev-20261105-065313-sdd-project-setup/, .specify/memory/exec-quant/records/20261105T034151386780Z-daca16a4.json, .specify/memory/exec-quant/records/20261105T034532226069Z-96d1a028.json, .specify/memory/exec-quant/records/20261105T041200397349Z-a9009299.json, .specify/memory/exec-quant/records/20261105T063435844961Z-07328654.json, .specify/memory/exec-quant/records/20261105T064151381207Z-e872cc64.json, .specify/memory/exec-quant/records/20261105T064501480379Z-39045a33.json, .specify/memory/exec-quant/records/20261105T070126815174Z-7b76709d.json, .specify/memory/feedback/20261105T034201Z-speckit-requirements.md, .specify/memory/feedback/20261105T034532Z-speckit-clarify.md, .specify/memory/feedback/20261105T041200Z-speckit-plan.md, .specify/memory/feedback/20261105T063435Z-speckit-tasks.md, .specify/memory/feedback/20261105T064151Z-speckit-checklist.md, .specify/memory/feedback/20261105T064512Z-speckit-analyze.md, .specify/memory/feedback/20261105T064532Z-speckit-analyze.md, .specify/memory/feedback/20261105T070132Z-speckit-analyze.md, .specify/memory/session/20261105T034151Z-run-determination-speckit-requirements-r20261105t033420z-082.md, .specify/memory/session/20261105T034532Z-run-determination-speckit-clarify-r20261105t033420z-082a.md, .specify/memory/session/20261105T041200Z-run-determination-speckit-plan-r20261105t033420z-082a.md, .specify/memory/session/20261105T063435Z-run-determination-speckit-tasks-r20261105t033420z-082a.md, .specify/memory/session/20261105T064151Z-run-determination-speckit-checklist-r20261105t033420z-082a.md, .specify/memory/session/20261105T064459Z-run-determination-speckit-analyze-r20261105t033420z-082a.md, .specify/memory/session/20261105T070114Z-run-determination-speckit-analyze-082-mechanism-policy-separ.md, .specify/specs/082-mechanism-policy-separation/test-evidence/implement-part3b-stage-status.jsonl, .specify/state/082-mechanism-policy-separation.md, .specify/state/083-budget-calibration-tests.txt, .specify/state/083-budget-calibration.md, .specify/state/083-loop-state-self-test.txt）；本回执不对该范围给出任何结论。

<!-- coverage-receipt:begin -->
receipt_version=1
base=3ffeb26e4880f134f7a5e220ecbffb869f165632
head=875be2c7f73679a0d1ec108afed1df4e32c8a766
base_source=feature-first-commit
renderer=text
changed_files=246
judged_files=29
skipped_files=217
gap_files=0
lines_added=18620
lines_deleted=254
file.001.path=.opencode/agents/dogfood-executor.md
file.001.verdict=skipped
file.001.reason=generated
file.002.path=.opencode/agents/framework-engineer.md
file.002.verdict=skipped
file.002.reason=generated
file.003.path=.opencode/agents/sdd-executor.md
file.003.verdict=skipped
file.003.reason=generated
file.004.path=.opencode/agents/sdd-requirements-executor.md
file.004.verdict=skipped
file.004.reason=generated
file.005.path=.opencode/agents/sdd-setup-executor.md
file.005.verdict=skipped
file.005.reason=generated
file.006.path=.opencode/agents/skill-verifier.md
file.006.verdict=skipped
file.006.reason=generated
file.007.path=.opencode/agents/structure-adjuster.md
file.007.verdict=skipped
file.007.reason=generated
file.008.path=.qoder/agents/dogfood-executor.agent.md
file.008.verdict=skipped
file.008.reason=generated
file.009.path=.qoder/agents/framework-engineer.agent.md
file.009.verdict=skipped
file.009.reason=generated
file.010.path=.qoder/agents/sdd-executor.agent.md
file.010.verdict=skipped
file.010.reason=generated
file.011.path=.qoder/agents/sdd-requirements-executor.agent.md
file.011.verdict=skipped
file.011.reason=generated
file.012.path=.qoder/agents/sdd-setup-executor.agent.md
file.012.verdict=skipped
file.012.reason=generated
file.013.path=.qoder/agents/skill-verifier.agent.md
file.013.verdict=skipped
file.013.reason=generated
file.014.path=.qoder/agents/structure-adjuster.agent.md
file.014.verdict=skipped
file.014.reason=generated
file.015.path=.specify/agents/.render-manifest.json
file.015.verdict=skipped
file.015.reason=generated
file.016.path=.specify/agents/instances/dogfood-executor.agent.md
file.016.verdict=skipped
file.016.reason=generated
file.017.path=.specify/agents/instances/framework-engineer.agent.md
file.017.verdict=skipped
file.017.reason=generated
file.018.path=.specify/agents/instances/sdd-requirements-executor.agent.md
file.018.verdict=skipped
file.018.reason=generated
file.019.path=.specify/agents/instances/sdd-setup-executor.agent.md
file.019.verdict=skipped
file.019.reason=generated
file.020.path=.specify/agents/templates/sdd-executor.agent.md
file.020.verdict=skipped
file.020.reason=generated
file.021.path=.specify/agents/templates/skill-verifier.agent.md
file.021.verdict=skipped
file.021.reason=generated
file.022.path=.specify/agents/templates/structure-adjuster.agent.md
file.022.verdict=skipped
file.022.reason=generated
file.023.path=.specify/memory/features.md
file.023.verdict=skipped
file.023.reason=non-code-file
file.024.path=.specify/memory/features/082.md
file.024.verdict=skipped
file.024.reason=non-code-file
file.025.path=.specify/memory/glossary.md
file.025.verdict=skipped
file.025.reason=non-code-file
file.026.path=.specify/shared/definitions/flow-class-definitions.md
file.026.verdict=skipped
file.026.reason=generated
file.027.path=.specify/shared/definitions/framework-map.md
file.027.verdict=skipped
file.027.reason=generated
file.028.path=.specify/shared/definitions/mechanism-policy-definitions.md
file.028.verdict=skipped
file.028.reason=generated
file.029.path=.specify/shared/definitions/probe-definitions.md
file.029.verdict=skipped
file.029.reason=generated
file.030.path=.specify/shared/definitions/skill-reference-definitions.md
file.030.verdict=skipped
file.030.reason=generated
file.031.path=.specify/shared/workflow/execution-topology.md
file.031.verdict=skipped
file.031.reason=generated
file.032.path=.specify/shared/workflow/external-dispatch-recipes.md
file.032.verdict=skipped
file.032.reason=generated
file.033.path=.specify/skills/coaching-skills/SKILL.md
file.033.verdict=skipped
file.033.reason=generated
file.034.path=.specify/skills/coaching-skills/data-model.md
file.034.verdict=skipped
file.034.reason=generated
file.035.path=.specify/skills/coaching-skills/references/prompt-templates.md
file.035.verdict=skipped
file.035.reason=generated
file.036.path=.specify/skills/create-skills/SKILL.md
file.036.verdict=skipped
file.036.reason=generated
file.037.path=.specify/skills/create-skills/references/mechanism-policy-check.md
file.037.verdict=skipped
file.037.reason=generated
file.038.path=.specify/skills/improve-skills/SKILL.md
file.038.verdict=skipped
file.038.reason=generated
file.039.path=.specify/skills/improve-skills/references/loop-playbook.md
file.039.verdict=skipped
file.039.reason=generated
file.040.path=.specify/skills/internal/create-agent/templates/agent-capacity-knowledge-manager-template.md
file.040.verdict=skipped
file.040.reason=generated
file.041.path=.specify/skills/internal/create-agent/templates/agent-capacity-module-designer-template.md
file.041.verdict=skipped
file.041.reason=generated
file.042.path=.specify/skills/internal/create-agent/templates/agent-capacity-qa-engineer-template.md
file.042.verdict=skipped
file.042.reason=generated
file.043.path=.specify/skills/internal/create-agent/templates/agent-capacity-requirements-analyst-template.md
file.043.verdict=skipped
file.043.reason=generated
file.044.path=.specify/skills/internal/create-agent/templates/agent-capacity-system-designer-template.md
file.044.verdict=skipped
file.044.reason=generated
file.045.path=.specify/skills/internal/create-agent/templates/agent-capacity-test-engineer-template.md
file.045.verdict=skipped
file.045.reason=generated
file.046.path=.specify/skills/internal/create-agent/templates/agent-capacity-ux-analyst-template.md
file.046.verdict=skipped
file.046.reason=generated
file.047.path=.specify/skills/internal/create-agent/templates/agent-project-custom-template.md
file.047.verdict=skipped
file.047.reason=generated
file.048.path=.specify/skills/internal/create-team/templates/agents/agent-team-supervisor-template.md
file.048.verdict=skipped
file.048.reason=generated
file.049.path=.specify/skills/internal/run-agent/SKILL.md
file.049.verdict=skipped
file.049.reason=generated
file.050.path=.specify/skills/internal/run-skills/SKILL.md
file.050.verdict=skipped
file.050.reason=generated
file.051.path=.specify/skills/merge-skills/SKILL.md
file.051.verdict=skipped
file.051.reason=generated
file.052.path=.specify/skills/merge-skills/references/provenance-record.md
file.052.verdict=skipped
file.052.reason=generated
file.053.path=.specify/skills/sdd-loop-driver/SKILL.md
file.053.verdict=skipped
file.053.reason=generated
file.054.path=.specify/skills/sdd-loop-driver/references/dispatch-recipes.md
file.054.verdict=skipped
file.054.reason=generated
file.055.path=.specify/skills/sdd-loop-driver/references/efficiency-model.md
file.055.verdict=skipped
file.055.reason=generated
file.056.path=.specify/skills/sdd-loop-driver/references/stage-prompts.md
file.056.verdict=skipped
file.056.reason=generated
file.057.path=.specify/skills/sdd-loop-driver/references/watch-model.md
file.057.verdict=skipped
file.057.reason=generated
file.058.path=.specify/skills/sdd-loop-driver/scripts/admission-check.py
file.058.verdict=skipped
file.058.reason=generated
file.059.path=.specify/skills/sdd-loop-driver/scripts/decomposition-check.py
file.059.verdict=skipped
file.059.reason=generated
file.060.path=.specify/skills/sdd-loop-driver/scripts/loop-state.py
file.060.verdict=skipped
file.060.reason=generated
file.061.path=.specify/skills/sdd-project-setup/SKILL.md
file.061.verdict=skipped
file.061.reason=generated
file.062.path=.specify/skills/sdd-project-setup/references/setup-recipes.md
file.062.verdict=skipped
file.062.reason=generated
file.063.path=.specify/skills/ssh-utils/SKILL.md
file.063.verdict=skipped
file.063.reason=generated
file.064.path=.specify/skills/ssh-utils/references/pitfalls.md
file.064.verdict=skipped
file.064.reason=generated
file.065.path=.specify/skills/ssh-utils/references/recipes.md
file.065.verdict=skipped
file.065.reason=generated
file.066.path=.specify/skills/ssh-utils/scripts/ssh-exec.py
file.066.verdict=skipped
file.066.reason=generated
file.067.path=.specify/specs/082-mechanism-policy-separation/baseline-failed.txt
file.067.verdict=skipped
file.067.reason=non-code-file
file.068.path=.specify/specs/082-mechanism-policy-separation/checklists/quality-scope-update.md
file.068.verdict=skipped
file.068.reason=non-code-file
file.069.path=.specify/specs/082-mechanism-policy-separation/checklists/requirements.md
file.069.verdict=skipped
file.069.reason=non-code-file
file.070.path=.specify/specs/082-mechanism-policy-separation/contracts/guard-and-measurement.contract.md
file.070.verdict=skipped
file.070.reason=non-code-file
file.071.path=.specify/specs/082-mechanism-policy-separation/contracts/owner-document.contract.md
file.071.verdict=skipped
file.071.reason=non-code-file
file.072.path=.specify/specs/082-mechanism-policy-separation/contracts/skill-reference.contract.md
file.072.verdict=skipped
file.072.reason=non-code-file
file.073.path=.specify/specs/082-mechanism-policy-separation/contracts/skill-wiring.contract.md
file.073.verdict=skipped
file.073.reason=non-code-file
file.074.path=.specify/specs/082-mechanism-policy-separation/coverage-baseline.txt
file.074.verdict=skipped
file.074.reason=non-code-file
file.075.path=.specify/specs/082-mechanism-policy-separation/data-model.md
file.075.verdict=skipped
file.075.reason=non-code-file
file.076.path=.specify/specs/082-mechanism-policy-separation/feature-ref.md
file.076.verdict=skipped
file.076.reason=non-code-file
file.077.path=.specify/specs/082-mechanism-policy-separation/notes/pre-change-measurements.md
file.077.verdict=skipped
file.077.reason=non-code-file
file.078.path=.specify/specs/082-mechanism-policy-separation/plan.md
file.078.verdict=skipped
file.078.reason=non-code-file
file.079.path=.specify/specs/082-mechanism-policy-separation/quickstart.md
file.079.verdict=skipped
file.079.reason=non-code-file
file.080.path=.specify/specs/082-mechanism-policy-separation/requirements.md
file.080.verdict=skipped
file.080.reason=non-code-file
file.081.path=.specify/specs/082-mechanism-policy-separation/research.md
file.081.verdict=skipped
file.081.reason=non-code-file
file.082.path=.specify/specs/082-mechanism-policy-separation/tasks.md
file.082.verdict=skipped
file.082.reason=non-code-file
file.083.path=.specify/specs/082-mechanism-policy-separation/test-evidence/analyze-repair-gates.txt
file.083.verdict=skipped
file.083.reason=non-code-file
file.084.path=.specify/specs/082-mechanism-policy-separation/test-evidence/analyze-repair-stage-status.jsonl
file.084.verdict=skipped
file.084.reason=non-code-file
file.085.path=.specify/specs/082-mechanism-policy-separation/test-evidence/checklist-scope-update-gates.txt
file.085.verdict=skipped
file.085.reason=non-code-file
file.086.path=.specify/specs/082-mechanism-policy-separation/test-evidence/checklist-scope-update-stage-status.jsonl
file.086.verdict=skipped
file.086.reason=non-code-file
file.087.path=.specify/specs/082-mechanism-policy-separation/test-evidence/clarify-gates.txt
file.087.verdict=skipped
file.087.reason=non-code-file
file.088.path=.specify/specs/082-mechanism-policy-separation/test-evidence/clarify-scope-update-fixture-probe.txt
file.088.verdict=skipped
file.088.reason=non-code-file
file.089.path=.specify/specs/082-mechanism-policy-separation/test-evidence/clarify-scope-update-fixture.json
file.089.verdict=skipped
file.089.reason=non-code-file
file.090.path=.specify/specs/082-mechanism-policy-separation/test-evidence/clarify-scope-update-gates.txt
file.090.verdict=skipped
file.090.reason=non-code-file
file.091.path=.specify/specs/082-mechanism-policy-separation/test-evidence/clarify-scope-update-stage-status.jsonl
file.091.verdict=skipped
file.091.reason=non-code-file
file.092.path=.specify/specs/082-mechanism-policy-separation/test-evidence/final-gates.txt
file.092.verdict=skipped
file.092.reason=non-code-file
file.093.path=.specify/specs/082-mechanism-policy-separation/test-evidence/flow-class-lookup.txt
file.093.verdict=skipped
file.093.reason=non-code-file
file.094.path=.specify/specs/082-mechanism-policy-separation/test-evidence/fr-027-starting-point-verification.txt
file.094.verdict=skipped
file.094.reason=non-code-file
file.095.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part1-baseline.txt
file.095.verdict=skipped
file.095.reason=non-code-file
file.096.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part1-stage-status.jsonl
file.096.verdict=skipped
file.096.reason=non-code-file
file.097.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part2-green.txt
file.097.verdict=skipped
file.097.reason=non-code-file
file.098.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part2-red.txt
file.098.verdict=skipped
file.098.reason=non-code-file
file.099.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part2-stage-status.jsonl
file.099.verdict=skipped
file.099.reason=non-code-file
file.100.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part2-stage-status.txt
file.100.verdict=skipped
file.100.reason=non-code-file
file.101.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part2-targeted.txt
file.101.verdict=skipped
file.101.reason=non-code-file
file.102.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part3-t017-red.txt
file.102.verdict=skipped
file.102.reason=non-code-file
file.103.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part3-t020-red.txt
file.103.verdict=skipped
file.103.reason=non-code-file
file.104.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part3a-stage-status.jsonl
file.104.verdict=skipped
file.104.reason=non-code-file
file.105.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part3a-t017-green.txt
file.105.verdict=skipped
file.105.reason=non-code-file
file.106.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part3a-t018-consumption-wiring.txt
file.106.verdict=skipped
file.106.reason=non-code-file
file.107.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part3a-t019-green.txt
file.107.verdict=skipped
file.107.reason=non-code-file
file.108.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part3a-t020-green.txt
file.108.verdict=skipped
file.108.reason=non-code-file
file.109.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part3a-targeted-green.txt
file.109.verdict=skipped
file.109.reason=non-code-file
file.110.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part3a-targeted.txt
file.110.verdict=skipped
file.110.reason=non-code-file
file.111.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part3b-t022.txt
file.111.verdict=skipped
file.111.reason=non-code-file
file.112.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part3b-t023-red.txt
file.112.verdict=skipped
file.112.reason=non-code-file
file.113.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part3b-t024-green.txt
file.113.verdict=skipped
file.113.reason=non-code-file
file.114.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part3b-targeted.txt
file.114.verdict=skipped
file.114.reason=non-code-file
file.115.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part4-red.txt
file.115.verdict=skipped
file.115.reason=non-code-file
file.116.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part4a-gm12-predicate-check.txt
file.116.verdict=skipped
file.116.reason=non-code-file
file.117.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part4a-stage-status.jsonl
file.117.verdict=skipped
file.117.reason=non-code-file
file.118.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part4a-targeted.txt
file.118.verdict=skipped
file.118.reason=non-code-file
file.119.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part4b-mirrors.txt
file.119.verdict=skipped
file.119.reason=non-code-file
file.120.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part4b-stage-status.jsonl
file.120.verdict=skipped
file.120.reason=non-code-file
file.121.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part4b-t029-green.txt
file.121.verdict=skipped
file.121.reason=non-code-file
file.122.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part4b-t029-red.txt
file.122.verdict=skipped
file.122.reason=non-code-file
file.123.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part4b-targeted-pre.txt
file.123.verdict=skipped
file.123.reason=non-code-file
file.124.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part4b-targeted.txt
file.124.verdict=skipped
file.124.reason=non-code-file
file.125.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part4b-wiring.txt
file.125.verdict=skipped
file.125.reason=non-code-file
file.126.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part5-red.txt
file.126.verdict=skipped
file.126.reason=non-code-file
file.127.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part5-stage-status.jsonl
file.127.verdict=skipped
file.127.reason=non-code-file
file.128.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part5-t035-green.txt
file.128.verdict=skipped
file.128.reason=non-code-file
file.129.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part5-t035-pre.txt
file.129.verdict=skipped
file.129.reason=non-code-file
file.130.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part5-t036-t037.txt
file.130.verdict=skipped
file.130.reason=non-code-file
file.131.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part5-t038.txt
file.131.verdict=skipped
file.131.reason=non-code-file
file.132.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part5-t039.txt
file.132.verdict=skipped
file.132.reason=non-code-file
file.133.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part5-targeted.txt
file.133.verdict=skipped
file.133.reason=non-code-file
file.134.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part6-stage-status.jsonl
file.134.verdict=skipped
file.134.reason=non-code-file
file.135.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part6-t041-t045-red.txt
file.135.verdict=skipped
file.135.reason=non-code-file
file.136.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part6-targeted.txt
file.136.verdict=skipped
file.136.reason=non-code-file
file.137.path=.specify/specs/082-mechanism-policy-separation/test-evidence/implement-part7-stage-status.jsonl
file.137.verdict=skipped
file.137.reason=non-code-file
file.138.path=.specify/specs/082-mechanism-policy-separation/test-evidence/plan-scope-update-gates.txt
file.138.verdict=skipped
file.138.reason=non-code-file
file.139.path=.specify/specs/082-mechanism-policy-separation/test-evidence/plan-scope-update-stage-status.jsonl
file.139.verdict=skipped
file.139.reason=non-code-file
file.140.path=.specify/specs/082-mechanism-policy-separation/test-evidence/plan2026-11-05-baseline.txt
file.140.verdict=skipped
file.140.reason=non-code-file
file.141.path=.specify/specs/082-mechanism-policy-separation/test-evidence/plan2026-11-05-plan-gates.txt
file.141.verdict=skipped
file.141.reason=non-code-file
file.142.path=.specify/specs/082-mechanism-policy-separation/test-evidence/plan2026-11-05-stage-status.jsonl
file.142.verdict=skipped
file.142.reason=non-code-file
file.143.path=.specify/specs/082-mechanism-policy-separation/test-evidence/requirements-scope-update-concurrent-impl-readout.txt
file.143.verdict=skipped
file.143.reason=non-code-file
file.144.path=.specify/specs/082-mechanism-policy-separation/test-evidence/requirements-scope-update-gates.txt
file.144.verdict=skipped
file.144.reason=non-code-file
file.145.path=.specify/specs/082-mechanism-policy-separation/test-evidence/requirements-scope-update-mirror-observation.txt
file.145.verdict=skipped
file.145.reason=non-code-file
file.146.path=.specify/specs/082-mechanism-policy-separation/test-evidence/requirements-scope-update-probe-tests.txt
file.146.verdict=skipped
file.146.reason=non-code-file
file.147.path=.specify/specs/082-mechanism-policy-separation/test-evidence/requirements-scope-update-stage-status.jsonl
file.147.verdict=skipped
file.147.reason=non-code-file
file.148.path=.specify/specs/082-mechanism-policy-separation/test-evidence/requirements-stage-status.jsonl
file.148.verdict=skipped
file.148.reason=non-code-file
file.149.path=.specify/specs/082-mechanism-policy-separation/test-evidence/requirements-u4-gates.txt
file.149.verdict=skipped
file.149.reason=non-code-file
file.150.path=.specify/specs/082-mechanism-policy-separation/test-evidence/review-078-coaching-regression.txt
file.150.verdict=skipped
file.150.reason=non-code-file
file.151.path=.specify/specs/082-mechanism-policy-separation/test-evidence/review-mirror-and-command-copies.txt
file.151.verdict=skipped
file.151.reason=non-code-file
file.152.path=.specify/specs/082-mechanism-policy-separation/test-evidence/review-sc-006-sc-009.txt
file.152.verdict=skipped
file.152.reason=non-code-file
file.153.path=.specify/specs/082-mechanism-policy-separation/test-evidence/review-smoke-and-targeted.txt
file.153.verdict=skipped
file.153.reason=non-code-file
file.154.path=.specify/specs/082-mechanism-policy-separation/test-evidence/sc-001-2026-11-05.txt
file.154.verdict=skipped
file.154.reason=non-code-file
file.155.path=.specify/specs/082-mechanism-policy-separation/test-evidence/sc-002-2026-11-05.txt
file.155.verdict=skipped
file.155.reason=non-code-file
file.156.path=.specify/specs/082-mechanism-policy-separation/test-evidence/sc-003-2026-11-05.txt
file.156.verdict=skipped
file.156.reason=non-code-file
file.157.path=.specify/specs/082-mechanism-policy-separation/test-evidence/sc-004-2026-11-05.txt
file.157.verdict=skipped
file.157.reason=non-code-file
file.158.path=.specify/specs/082-mechanism-policy-separation/test-evidence/sc-005-2026-11-05.txt
file.158.verdict=skipped
file.158.reason=non-code-file
file.159.path=.specify/specs/082-mechanism-policy-separation/test-evidence/sc-006-2026-11-05.txt
file.159.verdict=skipped
file.159.reason=non-code-file
file.160.path=.specify/specs/082-mechanism-policy-separation/test-evidence/sc-007-2026-11-05.txt
file.160.verdict=skipped
file.160.reason=non-code-file
file.161.path=.specify/specs/082-mechanism-policy-separation/test-evidence/sc-008-2026-11-05.txt
file.161.verdict=skipped
file.161.reason=non-code-file
file.162.path=.specify/specs/082-mechanism-policy-separation/test-evidence/sc-009-2026-11-05.txt
file.162.verdict=skipped
file.162.reason=non-code-file
file.163.path=.specify/specs/082-mechanism-policy-separation/test-evidence/skill-shape-before-after.txt
file.163.verdict=skipped
file.163.reason=non-code-file
file.164.path=.specify/specs/082-mechanism-policy-separation/test-evidence/tasks-scope-update-gates.txt
file.164.verdict=skipped
file.164.reason=non-code-file
file.165.path=.specify/specs/082-mechanism-policy-separation/test-evidence/tasks-scope-update-stage-status.jsonl
file.165.verdict=skipped
file.165.reason=non-code-file
file.166.path=.specify/specs/082-mechanism-policy-separation/test-evidence/validate-requirements-scope-update.txt
file.166.verdict=skipped
file.166.reason=non-code-file
file.167.path=.specify/specs/082-mechanism-policy-separation/test-evidence/validate-requirements.txt
file.167.verdict=skipped
file.167.reason=non-code-file
file.168.path=.specify/specs/082-mechanism-policy-separation/verification.md
file.168.verdict=skipped
file.168.reason=non-code-file
file.169.path=CHANGELOG.md
file.169.verdict=reviewed
file.170.path=agents/sdd-executor.agent.md
file.170.verdict=skipped
file.170.reason=non-code-file
file.171.path=agents/skill-verifier.agent.md
file.171.verdict=skipped
file.171.reason=non-code-file
file.172.path=agents/structure-adjuster.agent.md
file.172.verdict=skipped
file.172.reason=non-code-file
file.173.path=docs/reference/skills/sdd-loop-driver.md
file.173.verdict=skipped
file.173.reason=out-of-scope-per-explicit-user-ruling
file.174.path=docs/reference/skills/sdd-project-setup.md
file.174.verdict=skipped
file.174.reason=out-of-scope-per-explicit-user-ruling
file.175.path=shared/definitions/flow-class-definitions.md
file.175.verdict=skipped
file.175.reason=out-of-scope-per-explicit-user-ruling
file.176.path=shared/definitions/framework-map.md
file.176.verdict=reviewed
file.177.path=shared/definitions/mechanism-policy-definitions.md
file.177.verdict=reviewed
file.178.path=shared/definitions/probe-definitions.md
file.178.verdict=skipped
file.178.reason=out-of-scope-per-explicit-user-ruling
file.179.path=shared/definitions/skill-reference-definitions.md
file.179.verdict=reviewed
file.180.path=shared/workflow/execution-topology.md
file.180.verdict=skipped
file.180.reason=out-of-scope-per-explicit-user-ruling
file.181.path=shared/workflow/external-dispatch-recipes.md
file.181.verdict=skipped
file.181.reason=out-of-scope-per-explicit-user-ruling
file.182.path=skills/external/coaching-skills/SKILL.md
file.182.verdict=reviewed
file.183.path=skills/external/coaching-skills/data-model.md
file.183.verdict=reviewed
file.184.path=skills/external/coaching-skills/references/prompt-templates.md
file.184.verdict=reviewed
file.185.path=skills/external/create-skills/SKILL.md
file.185.verdict=reviewed
file.186.path=skills/external/create-skills/references/mechanism-policy-check.md
file.186.verdict=reviewed
file.187.path=skills/external/improve-skills/SKILL.md
file.187.verdict=reviewed
file.188.path=skills/external/improve-skills/references/loop-playbook.md
file.188.verdict=reviewed
file.189.path=skills/external/merge-skills/SKILL.md
file.189.verdict=reviewed
file.190.path=skills/external/merge-skills/references/provenance-record.md
file.190.verdict=reviewed
file.191.path=skills/external/sdd-loop-driver/SKILL.md
file.191.verdict=skipped
file.191.reason=out-of-scope-per-explicit-user-ruling
file.192.path=skills/external/sdd-loop-driver/references/dispatch-recipes.md
file.192.verdict=skipped
file.192.reason=out-of-scope-per-explicit-user-ruling
file.193.path=skills/external/sdd-loop-driver/references/efficiency-model.md
file.193.verdict=skipped
file.193.reason=out-of-scope-per-explicit-user-ruling
file.194.path=skills/external/sdd-loop-driver/references/stage-prompts.md
file.194.verdict=skipped
file.194.reason=out-of-scope-per-explicit-user-ruling
file.195.path=skills/external/sdd-loop-driver/references/watch-model.md
file.195.verdict=skipped
file.195.reason=out-of-scope-per-explicit-user-ruling
file.196.path=skills/external/sdd-loop-driver/scripts/admission-check.py
file.196.verdict=skipped
file.196.reason=out-of-scope-per-explicit-user-ruling
file.197.path=skills/external/sdd-loop-driver/scripts/decomposition-check.py
file.197.verdict=skipped
file.197.reason=out-of-scope-per-explicit-user-ruling
file.198.path=skills/external/sdd-loop-driver/scripts/loop-state.py
file.198.verdict=skipped
file.198.reason=out-of-scope-per-explicit-user-ruling
file.199.path=skills/external/sdd-project-setup/SKILL.md
file.199.verdict=skipped
file.199.reason=out-of-scope-per-explicit-user-ruling
file.200.path=skills/external/sdd-project-setup/references/setup-recipes.md
file.200.verdict=skipped
file.200.reason=out-of-scope-per-explicit-user-ruling
file.201.path=skills/external/ssh-utils/SKILL.md
file.201.verdict=skipped
file.201.reason=out-of-scope-per-explicit-user-ruling
file.202.path=skills/external/ssh-utils/references/pitfalls.md
file.202.verdict=skipped
file.202.reason=out-of-scope-per-explicit-user-ruling
file.203.path=skills/external/ssh-utils/references/recipes.md
file.203.verdict=skipped
file.203.reason=out-of-scope-per-explicit-user-ruling
file.204.path=skills/external/ssh-utils/scripts/ssh-exec.py
file.204.verdict=skipped
file.204.reason=out-of-scope-per-explicit-user-ruling
file.205.path=skills/internal/create-agent/templates/agent-capacity-knowledge-manager-template.md
file.205.verdict=skipped
file.205.reason=out-of-scope-per-explicit-user-ruling
file.206.path=skills/internal/create-agent/templates/agent-capacity-module-designer-template.md
file.206.verdict=skipped
file.206.reason=out-of-scope-per-explicit-user-ruling
file.207.path=skills/internal/create-agent/templates/agent-capacity-qa-engineer-template.md
file.207.verdict=skipped
file.207.reason=out-of-scope-per-explicit-user-ruling
file.208.path=skills/internal/create-agent/templates/agent-capacity-requirements-analyst-template.md
file.208.verdict=skipped
file.208.reason=out-of-scope-per-explicit-user-ruling
file.209.path=skills/internal/create-agent/templates/agent-capacity-system-designer-template.md
file.209.verdict=skipped
file.209.reason=out-of-scope-per-explicit-user-ruling
file.210.path=skills/internal/create-agent/templates/agent-capacity-test-engineer-template.md
file.210.verdict=skipped
file.210.reason=out-of-scope-per-explicit-user-ruling
file.211.path=skills/internal/create-agent/templates/agent-capacity-ux-analyst-template.md
file.211.verdict=skipped
file.211.reason=out-of-scope-per-explicit-user-ruling
file.212.path=skills/internal/create-agent/templates/agent-project-custom-template.md
file.212.verdict=skipped
file.212.reason=out-of-scope-per-explicit-user-ruling
file.213.path=skills/internal/create-team/templates/agents/agent-team-supervisor-template.md
file.213.verdict=skipped
file.213.reason=out-of-scope-per-explicit-user-ruling
file.214.path=skills/internal/run-agent/SKILL.md
file.214.verdict=skipped
file.214.reason=out-of-scope-per-explicit-user-ruling
file.215.path=skills/internal/run-skills/SKILL.md
file.215.verdict=reviewed
file.216.path=tests/contract/skill_reference_matrix.py
file.216.verdict=reviewed
file.217.path=tests/contract/test_bilingual_expression.py
file.217.verdict=reviewed
file.218.path=tests/contract/test_coaching_wiring_contract.py
file.218.verdict=skipped
file.218.reason=out-of-scope-per-explicit-user-ruling
file.219.path=tests/contract/test_expression_compatibility.py
file.219.verdict=reviewed
file.220.path=tests/contract/test_expression_gate_wiring.py
file.220.verdict=skipped
file.220.reason=out-of-scope-per-explicit-user-ruling
file.221.path=tests/contract/test_flow_class_ledger.py
file.221.verdict=skipped
file.221.reason=out-of-scope-per-explicit-user-ruling
file.222.path=tests/contract/test_ledger_reconciliation.py
file.222.verdict=skipped
file.222.reason=out-of-scope-per-explicit-user-ruling
file.223.path=tests/contract/test_mechanism_policy_decidability.py
file.223.verdict=reviewed
file.224.path=tests/contract/test_mechanism_policy_guard.py
file.224.verdict=reviewed
file.225.path=tests/contract/test_mechanism_policy_missing_policy.py
file.225.verdict=reviewed
file.226.path=tests/contract/test_mechanism_policy_owner_doc.py
file.226.verdict=reviewed
file.227.path=tests/contract/test_mechanism_policy_ownership.py
file.227.verdict=reviewed
file.228.path=tests/contract/test_mechanism_policy_skill_wiring.py
file.228.verdict=reviewed
file.229.path=tests/contract/test_migration_distribution.py
file.229.verdict=skipped
file.229.reason=out-of-scope-per-explicit-user-ruling
file.230.path=tests/contract/test_probe_nonentity_catalog.py
file.230.verdict=skipped
file.230.reason=out-of-scope-per-explicit-user-ruling
file.231.path=tests/contract/test_run_skills_wiring.py
file.231.verdict=skipped
file.231.reason=out-of-scope-per-explicit-user-ruling
file.232.path=tests/contract/test_sdd_loop_driver_efficiency.py
file.232.verdict=skipped
file.232.reason=out-of-scope-per-explicit-user-ruling
file.233.path=tests/contract/test_sdd_loop_driver_gates.py
file.233.verdict=skipped
file.233.reason=out-of-scope-per-explicit-user-ruling
file.234.path=tests/contract/test_sdd_loop_driver_skill.py
file.234.verdict=skipped
file.234.reason=out-of-scope-per-explicit-user-ruling
file.235.path=tests/contract/test_skill_layer_visibility_guards.py
file.235.verdict=skipped
file.235.reason=out-of-scope-per-explicit-user-ruling
file.236.path=tests/contract/test_skill_reference_command_surface.py
file.236.verdict=reviewed
file.237.path=tests/contract/test_skill_reference_consumers.py
file.237.verdict=reviewed
file.238.path=tests/contract/test_skill_reference_failures.py
file.238.verdict=reviewed
file.239.path=tests/contract/test_skill_reference_grammar.py
file.239.verdict=reviewed
file.240.path=tests/contract/test_skill_reference_matrix.py
file.240.verdict=reviewed
file.241.path=tests/contract/test_ssh_utils_skill.py
file.241.verdict=skipped
file.241.reason=out-of-scope-per-explicit-user-ruling
file.242.path=tests/fixtures/sdd_loop_efficiency/large/.specify/specs/013-large/tasks.md
file.242.verdict=skipped
file.242.reason=out-of-scope-per-explicit-user-ruling
file.243.path=tests/fixtures/skill-reference/normalization-matrix.json
file.243.verdict=reviewed
file.244.path=tests/unit/test_admission_check.py
file.244.verdict=skipped
file.244.reason=out-of-scope-per-explicit-user-ruling
file.245.path=tests/unit/test_decomposition_check.py
file.245.verdict=skipped
file.245.reason=out-of-scope-per-explicit-user-ruling
file.246.path=tests/unit/test_pre_analyze_check.py
file.246.verdict=skipped
file.246.reason=out-of-scope-per-explicit-user-ruling
<!-- coverage-receipt:end -->
