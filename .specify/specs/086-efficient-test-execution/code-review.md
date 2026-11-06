# Code Review Report — 代码段 (code segment)

| 属性 | 值 |
|------|-----|
| **分支** | `086-efficient-test-execution` |
| **基准** | `24cb4edcc53db3cfc86f574e5e6d627c78b2ca08` (`24cb4edc`) |
| **目标** | `a0426644f9ad0520cdc75cb9273621de8e66f7f7` (`a0426644`) |
| **基准来源** | `feature-first-commit` |
| **渲染模式** | `renderer: text` |
| **Reviewer** | `Qiming, Liu` |
| **日期** | `2026-11-06T07:46:40Z` |

## 变更概览

```
 .specify/instructions.md                           |   9 +
 .specify/memory/constitution.md                    |  52 +-
 .../records/20261106T040443520576Z-7ea40fdc.json   |   1 +
 .../records/20261106T041126041004Z-9ee5cd24.json   |   1 +
 .../records/20261106T041126235213Z-a90323ad.json   |   1 +
 .../records/20261106T042142979790Z-f4d01a22.json   |   1 +
 .../records/20261106T042146057460Z-444ea05b.json   |   1 +
 .../records/20261106T044156696711Z-aead8092.json   |   1 +
 .../records/20261106T044619831151Z-34e5daa6.json   |   1 +
 .../records/20261106T045636924465Z-7f117c26.json   |   1 +
 .specify/memory/features.md                        |   3 +-
 .specify/memory/features/086.md                    | 139 ++++
 .../20261106T040443Z-skill-create-requirements.md  |  21 +
 .../20261106T041131Z-skill-clarify-artifact.md     |  21 +
 .../feedback/20261106T041131Z-speckit-clarify.md   |  21 +
 .../feedback/20261106T042143Z-speckit-plan.md      |  19 +
 .../feedback/20261106T042146Z-skill-create-plan.md |  19 +
 .../20261106T044156Z-skill-create-tasks.md         |  21 +
 .../20261106T044619Z-skill-create-checklist.md     |  21 +
 .../20261106T045642Z-skill-analyze-artifacts.md    |  19 +
 ...on-skill-analyze-artifacts-r20261027t061144z.md |  29 +-
 ...n-skill-create-requirements-r20261106t033959.md | 202 +++++
 ...n-skill-clarify-artifact-r20261106t033959z-0.md | 203 +++++
 ...ation-speckit-clarify-r20261106t033959z-086a.md | 207 +++++
 ...mination-speckit-plan-r20261106t033959z-086a.md | 200 +++++
 ...ion-skill-create-plan-r20261106t033959z-086a.md | 200 +++++
 ...on-skill-create-tasks-r20261106t033959z-086a.md | 202 +++++
 ...ination-speckit-tasks-r20261106t033959z-086a.md | 202 +++++
 ...n-skill-create-checklist-r20261106t033959z-0.md | 202 +++++
 ...on-skill-analyze-artifacts-r20261106t033959z.md | 202 +++++
 .specify/scripts/bash/run-tests.sh                 | 270 ++++++-
 .../shared/guidelines/test-execution-efficiency.md | 129 +++
 .../skills/internal/manage-constitution/SKILL.md   |  16 +
 .../sdd-loop-driver/scripts/audit-test-budget.py   |  33 +-
 .../085-sdd-temporary-goal-team/verification.md    |   6 +-
 .../checklists/requirements-quality-2026-11-06.md  |  87 +++
 .../checklists/requirements.md                     |  38 +
 .../checkpoints/01-requirements.md                 |  50 ++
 .../checkpoints/02-clarify.md                      |  42 +
 .../checkpoints/03-plan.md                         |  42 +
 .../checkpoints/04-tasks.md                        |  45 ++
 .../checkpoints/05-checklist.md                    |  46 ++
 .../checkpoints/06-analyze.md                      |  41 +
 .../checkpoints/07-implement-preflight.md          |  42 +
 .../checkpoints/08-implement-wave1.md              |  36 +
 .../checkpoints/09-implement-wave2.md              |  37 +
 .../checkpoints/10-implement-wave3.md              |  36 +
 .../checkpoints/11-implement-wave4.md              |  52 ++
 .../checkpoints/12-implement-closure.md            |  83 ++
 .../contracts/budget-ledger-parser.contract.md     |  58 ++
 .../contracts/dogfood-and-preservation.contract.md |  90 +++
 .../contracts/principle-landing.contract.md        | 110 +++
 .../contracts/runner-contract-086.contract.md      | 102 +++
 .../coverage-baseline.txt                          | 575 ++++++++++++++
 .../086-efficient-test-execution/data-model.md     | 199 +++++
 .../086-efficient-test-execution/feature-ref.md    |  62 ++
 .../goal/086-efficient-test-execution/goal.md      |  23 +
 .../notes/red-first-evidence.md                    |  56 ++
 .../specs/086-efficient-test-execution/plan.md     | 339 ++++++++
 .../086-efficient-test-execution/quickstart.md     | 196 +++++
 .../086-efficient-test-execution/requirements.md   | 334 ++++++++
 .../specs/086-efficient-test-execution/research.md | 195 +++++
 .../specs/086-efficient-test-execution/tasks.md    | 338 ++++++++
 .../team/086-efficient-test-execution/team.md      | 183 +++++
 .../test-evidence/analyze-findings.md              |  85 ++
 .../test-evidence/baseline-failed.txt              |  19 +
 .../test-evidence/baseline.txt                     | 582 ++++++++++++++
 .../test-evidence/budget-ledger.txt                |  94 +++
 .../test-evidence/checklist-gates.txt              | 339 ++++++++
 .../test-evidence/clarify-gates.txt                | 102 +++
 .../test-evidence/closure-diff.txt                 | 148 ++++
 .../test-evidence/completion-gate.txt              | 297 +++++++
 .../test-evidence/dogfood-record.md                | 146 ++++
 .../test-evidence/downstream-init.txt              |  90 +++
 .../test-evidence/escape-hatch.txt                 | 127 +++
 .../test-evidence/final-failed.txt                 |  19 +
 .../test-evidence/full-run-budget.md               | 104 +++
 .../test-evidence/ledger-parallel-flags.txt        | 105 +++
 .../test-evidence/mirror-parity.txt                | 110 +++
 .../test-evidence/mutation-legs-runner.txt         | 133 ++++
 .../test-evidence/no-new-machinery.txt             | 131 ++++
 .../test-evidence/parallel-safety-attribution.md   | 216 +++++
 .../test-evidence/parallel-safety.txt              |  82 ++
 .../test-evidence/plan-gates.txt                   | 229 ++++++
 .../test-evidence/preservation-085.txt             | 183 +++++
 .../test-evidence/repair-gates.txt                 | 156 ++++
 .../test-evidence/requirements-gates.txt           |  58 ++
 .../test-evidence/scheduling-experiment.txt        | 104 +++
 .../test-evidence/serial-exceptions.txt            | 187 +++++
 .../test-evidence/smoke-086.txt                    |  41 +
 .../test-evidence/tasks-gates.txt                  |  95 +++
 .../test-evidence/worktree-clean.txt               |  86 ++
 .../086-efficient-test-execution/verification.md   |  90 +++
 .specify/state/086-efficient-test-execution.md     | 266 +++++++
 .specify/templates/constitution-template.md        |  31 +
 .specify/templates/instructions-template.md        |   9 +
 CHANGELOG.md                                       |  13 +
 CONTRIBUTING.md                                    |   6 +
 docs/contribute/dev-setup.md                       |  27 +-
 pyproject.toml                                     |  11 +
 scripts/bash/run-tests.sh                          | 270 ++++++-
 shared/guidelines/test-execution-efficiency.md     | 129 +++
 .../sdd-loop-driver/scripts/audit-test-budget.py   |  33 +-
 skills/internal/manage-constitution/SKILL.md       |  16 +
 templates/constitution-template.md                 |  31 +
 templates/instructions-template.md                 |   9 +
 tests/contract/test_constitution_double_landing.py |  22 +-
 tests/contract/test_fast_fail_discipline.py        |  66 +-
 tests/contract/test_run_tests_runner_contract.py   | 868 +++++++++++++++++++++
 tests/contract/test_sdd_loop_driver_skill.py       |   6 +
 tests/contract/test_test_execution_efficiency.py   | 533 +++++++++++++
 .../test_sdd_loop_efficiency_regression.py         |  76 +-
 tests/unit/test_audit_test_budget.py               | 191 ++++-
 113 files changed, 12901 insertions(+), 83 deletions(-)
```

---

## Review 意见


### 🟠 [IMPORTANT] templates/constitution-template.md (Line 331)

> The principle's primary pointer names the .specify-runtime form of the owner path, not the framework-source form the feature declares as the pointer target: requirements.md STR-003 (and FR-018/019/020/SC-002/SC-003) fix 'shared/guidelines/test-execution-efficiency.md'. src/specify_cli/__init__.py _render_specify_local_paths rewrites `.specify/` prefixes only, so the template's literal survives verbatim into the downstream tree. Measured on a fresh 'specify init' at HEAD: the generated shared/guidelines/test-execution-efficiency.md opens with '文件路径:.specify/shared/guidelines/test-execution-efficiency.md' while the clause beside it points at .specify/shared/guidelines/test-execution-efficiency.md -- the two disagree about where the owner lives. Answer: accept the runtime form as correct for a downstream tree (a project-initialised pointer to a framework-source path is itself the defect, and FR-018/FR-020 use the runtime form), and re-pin STR-003 and the SC-002/SC-003 readings in a follow-up rather than by editing 086 post-closure.

<sub>15:46:49</sub>


### 🟠 [IMPORTANT] tests/contract/test_test_execution_efficiency.py (Line 1)

> The six-surface principle guard asserts the pointer literal is 'shared/guidelines/test-execution-efficiency.md' on every surface, but the shipped template carries the '.specify/'-prefixed form and the downstream copy contains neither literal form. The guard is therefore anchored on the framework-source spelling only and cannot see the drift the previous note records. Answer: run the guard's pointer assertion over both spellings (source form for templates/, runtime form for .specify/ and downstream), which is the missing half the current case does not measure.

<sub>15:46:49</sub>


### ❓ [QUESTION] scripts/bash/run-tests.sh (Line 196)

> In parallel mode without --names-out, a failed parallel pass is masked whenever the serial pass is green: 'if [ "$SERIAL_STATUS" -ne 0 ]; then exit ... ; fi; exit "$PARALLEL_STATUS"' returns the PARALLEL_STATUS it already holds, so a combined run can exit 0 with failures printed. The --names-out path normalizes exit 5 there but returns any other serial status first, which is correct. Question: is the no-names-out asymmetry intended (a convenience path that is not the comparison surface), or should both paths compose the exit code one way? The closure and smoke runs all used --names-out, so no recorded reading is affected.

<sub>15:46:49</sub>


### 🟢 [SUGGESTION] .specify/specs/086-efficient-test-execution/test-evidence/downstream-init.txt (Line 90)

> The evidence file says the generated constitution is 'the two-line placeholder' and the generated instructions 'is not generated at init time at all'; both are true at HEAD, but the file does not record that a re-run today would now find the principle in the generated constitution, because src/specify_cli/__init__.py copies the packaged constitution-template.md when local templates are present. A later reader comparing the record against a fresh init sees a contradiction that is really a difference between the packaged source template and the nested .specify/templates copy. Proposed fix: record which of the two copies the init used, or reword the row to say the placeholder is what the run observed at its own commit.

<sub>15:46:49</sub>


<!-- coverage-receipt:begin -->
receipt_version=1
base=24cb4edcc53db3cfc86f574e5e6d627c78b2ca08
head=a0426644f9ad0520cdc75cb9273621de8e66f7f7
base_source=trunk-merge-base
renderer=text
changed_files=113
judged_files=113
skipped_files=0
gap_files=0
lines_added=12901
lines_deleted=83
file.001.path=.specify/instructions.md
file.001.verdict=reviewed
file.002.path=.specify/memory/constitution.md
file.002.verdict=reviewed
file.003.path=.specify/memory/exec-quant/records/20261106T040443520576Z-7ea40fdc.json
file.003.verdict=reviewed
file.004.path=.specify/memory/exec-quant/records/20261106T041126041004Z-9ee5cd24.json
file.004.verdict=reviewed
file.005.path=.specify/memory/exec-quant/records/20261106T041126235213Z-a90323ad.json
file.005.verdict=reviewed
file.006.path=.specify/memory/exec-quant/records/20261106T042142979790Z-f4d01a22.json
file.006.verdict=reviewed
file.007.path=.specify/memory/exec-quant/records/20261106T042146057460Z-444ea05b.json
file.007.verdict=reviewed
file.008.path=.specify/memory/exec-quant/records/20261106T044156696711Z-aead8092.json
file.008.verdict=reviewed
file.009.path=.specify/memory/exec-quant/records/20261106T044619831151Z-34e5daa6.json
file.009.verdict=reviewed
file.010.path=.specify/memory/exec-quant/records/20261106T045636924465Z-7f117c26.json
file.010.verdict=reviewed
file.011.path=.specify/memory/features.md
file.011.verdict=reviewed
file.012.path=.specify/memory/features/086.md
file.012.verdict=reviewed
file.013.path=.specify/memory/feedback/20261106T040443Z-skill-create-requirements.md
file.013.verdict=reviewed
file.014.path=.specify/memory/feedback/20261106T041131Z-skill-clarify-artifact.md
file.014.verdict=reviewed
file.015.path=.specify/memory/feedback/20261106T041131Z-speckit-clarify.md
file.015.verdict=reviewed
file.016.path=.specify/memory/feedback/20261106T042143Z-speckit-plan.md
file.016.verdict=reviewed
file.017.path=.specify/memory/feedback/20261106T042146Z-skill-create-plan.md
file.017.verdict=reviewed
file.018.path=.specify/memory/feedback/20261106T044156Z-skill-create-tasks.md
file.018.verdict=reviewed
file.019.path=.specify/memory/feedback/20261106T044619Z-skill-create-checklist.md
file.019.verdict=reviewed
file.020.path=.specify/memory/feedback/20261106T045642Z-skill-analyze-artifacts.md
file.020.verdict=reviewed
file.021.path=.specify/memory/session/20261027T070336Z-run-determination-skill-analyze-artifacts-r20261027t061144z.md
file.021.verdict=reviewed
file.022.path=.specify/memory/session/20261106T040443Z-run-determination-skill-create-requirements-r20261106t033959.md
file.022.verdict=reviewed
file.023.path=.specify/memory/session/20261106T041123Z-run-determination-skill-clarify-artifact-r20261106t033959z-0.md
file.023.verdict=reviewed
file.024.path=.specify/memory/session/20261106T041125Z-run-determination-speckit-clarify-r20261106t033959z-086a.md
file.024.verdict=reviewed
file.025.path=.specify/memory/session/20261106T042132Z-run-determination-speckit-plan-r20261106t033959z-086a.md
file.025.verdict=reviewed
file.026.path=.specify/memory/session/20261106T042145Z-run-determination-skill-create-plan-r20261106t033959z-086a.md
file.026.verdict=reviewed
file.027.path=.specify/memory/session/20261106T042740Z-run-determination-skill-create-tasks-r20261106t033959z-086a.md
file.027.verdict=reviewed
file.028.path=.specify/memory/session/20261106T042740Z-run-determination-speckit-tasks-r20261106t033959z-086a.md
file.028.verdict=reviewed
file.029.path=.specify/memory/session/20261106T044619Z-run-determination-skill-create-checklist-r20261106t033959z-0.md
file.029.verdict=reviewed
file.030.path=.specify/memory/session/20261106T045626Z-run-determination-skill-analyze-artifacts-r20261106t033959z.md
file.030.verdict=reviewed
file.031.path=.specify/scripts/bash/run-tests.sh
file.031.verdict=reviewed
file.032.path=.specify/shared/guidelines/test-execution-efficiency.md
file.032.verdict=reviewed
file.033.path=.specify/skills/internal/manage-constitution/SKILL.md
file.033.verdict=reviewed
file.034.path=.specify/skills/sdd-loop-driver/scripts/audit-test-budget.py
file.034.verdict=reviewed
file.035.path=.specify/specs/085-sdd-temporary-goal-team/verification.md
file.035.verdict=reviewed
file.036.path=.specify/specs/086-efficient-test-execution/checklists/requirements-quality-2026-11-06.md
file.036.verdict=reviewed
file.037.path=.specify/specs/086-efficient-test-execution/checklists/requirements.md
file.037.verdict=reviewed
file.038.path=.specify/specs/086-efficient-test-execution/checkpoints/01-requirements.md
file.038.verdict=reviewed
file.039.path=.specify/specs/086-efficient-test-execution/checkpoints/02-clarify.md
file.039.verdict=reviewed
file.040.path=.specify/specs/086-efficient-test-execution/checkpoints/03-plan.md
file.040.verdict=reviewed
file.041.path=.specify/specs/086-efficient-test-execution/checkpoints/04-tasks.md
file.041.verdict=reviewed
file.042.path=.specify/specs/086-efficient-test-execution/checkpoints/05-checklist.md
file.042.verdict=reviewed
file.043.path=.specify/specs/086-efficient-test-execution/checkpoints/06-analyze.md
file.043.verdict=reviewed
file.044.path=.specify/specs/086-efficient-test-execution/checkpoints/07-implement-preflight.md
file.044.verdict=reviewed
file.045.path=.specify/specs/086-efficient-test-execution/checkpoints/08-implement-wave1.md
file.045.verdict=reviewed
file.046.path=.specify/specs/086-efficient-test-execution/checkpoints/09-implement-wave2.md
file.046.verdict=reviewed
file.047.path=.specify/specs/086-efficient-test-execution/checkpoints/10-implement-wave3.md
file.047.verdict=reviewed
file.048.path=.specify/specs/086-efficient-test-execution/checkpoints/11-implement-wave4.md
file.048.verdict=reviewed
file.049.path=.specify/specs/086-efficient-test-execution/checkpoints/12-implement-closure.md
file.049.verdict=reviewed
file.050.path=.specify/specs/086-efficient-test-execution/contracts/budget-ledger-parser.contract.md
file.050.verdict=reviewed
file.051.path=.specify/specs/086-efficient-test-execution/contracts/dogfood-and-preservation.contract.md
file.051.verdict=reviewed
file.052.path=.specify/specs/086-efficient-test-execution/contracts/principle-landing.contract.md
file.052.verdict=reviewed
file.053.path=.specify/specs/086-efficient-test-execution/contracts/runner-contract-086.contract.md
file.053.verdict=reviewed
file.054.path=.specify/specs/086-efficient-test-execution/coverage-baseline.txt
file.054.verdict=reviewed
file.055.path=.specify/specs/086-efficient-test-execution/data-model.md
file.055.verdict=reviewed
file.056.path=.specify/specs/086-efficient-test-execution/feature-ref.md
file.056.verdict=reviewed
file.057.path=.specify/specs/086-efficient-test-execution/goal/086-efficient-test-execution/goal.md
file.057.verdict=reviewed
file.058.path=.specify/specs/086-efficient-test-execution/notes/red-first-evidence.md
file.058.verdict=reviewed
file.059.path=.specify/specs/086-efficient-test-execution/plan.md
file.059.verdict=reviewed
file.060.path=.specify/specs/086-efficient-test-execution/quickstart.md
file.060.verdict=reviewed
file.061.path=.specify/specs/086-efficient-test-execution/requirements.md
file.061.verdict=reviewed
file.062.path=.specify/specs/086-efficient-test-execution/research.md
file.062.verdict=reviewed
file.063.path=.specify/specs/086-efficient-test-execution/tasks.md
file.063.verdict=reviewed
file.064.path=.specify/specs/086-efficient-test-execution/team/086-efficient-test-execution/team.md
file.064.verdict=reviewed
file.065.path=.specify/specs/086-efficient-test-execution/test-evidence/analyze-findings.md
file.065.verdict=reviewed
file.066.path=.specify/specs/086-efficient-test-execution/test-evidence/baseline-failed.txt
file.066.verdict=reviewed
file.067.path=.specify/specs/086-efficient-test-execution/test-evidence/baseline.txt
file.067.verdict=reviewed
file.068.path=.specify/specs/086-efficient-test-execution/test-evidence/budget-ledger.txt
file.068.verdict=reviewed
file.069.path=.specify/specs/086-efficient-test-execution/test-evidence/checklist-gates.txt
file.069.verdict=reviewed
file.070.path=.specify/specs/086-efficient-test-execution/test-evidence/clarify-gates.txt
file.070.verdict=reviewed
file.071.path=.specify/specs/086-efficient-test-execution/test-evidence/closure-diff.txt
file.071.verdict=reviewed
file.072.path=.specify/specs/086-efficient-test-execution/test-evidence/completion-gate.txt
file.072.verdict=reviewed
file.073.path=.specify/specs/086-efficient-test-execution/test-evidence/dogfood-record.md
file.073.verdict=reviewed
file.074.path=.specify/specs/086-efficient-test-execution/test-evidence/downstream-init.txt
file.074.verdict=reviewed
file.075.path=.specify/specs/086-efficient-test-execution/test-evidence/escape-hatch.txt
file.075.verdict=reviewed
file.076.path=.specify/specs/086-efficient-test-execution/test-evidence/final-failed.txt
file.076.verdict=reviewed
file.077.path=.specify/specs/086-efficient-test-execution/test-evidence/full-run-budget.md
file.077.verdict=reviewed
file.078.path=.specify/specs/086-efficient-test-execution/test-evidence/ledger-parallel-flags.txt
file.078.verdict=reviewed
file.079.path=.specify/specs/086-efficient-test-execution/test-evidence/mirror-parity.txt
file.079.verdict=reviewed
file.080.path=.specify/specs/086-efficient-test-execution/test-evidence/mutation-legs-runner.txt
file.080.verdict=reviewed
file.081.path=.specify/specs/086-efficient-test-execution/test-evidence/no-new-machinery.txt
file.081.verdict=reviewed
file.082.path=.specify/specs/086-efficient-test-execution/test-evidence/parallel-safety-attribution.md
file.082.verdict=reviewed
file.083.path=.specify/specs/086-efficient-test-execution/test-evidence/parallel-safety.txt
file.083.verdict=reviewed
file.084.path=.specify/specs/086-efficient-test-execution/test-evidence/plan-gates.txt
file.084.verdict=reviewed
file.085.path=.specify/specs/086-efficient-test-execution/test-evidence/preservation-085.txt
file.085.verdict=reviewed
file.086.path=.specify/specs/086-efficient-test-execution/test-evidence/repair-gates.txt
file.086.verdict=reviewed
file.087.path=.specify/specs/086-efficient-test-execution/test-evidence/requirements-gates.txt
file.087.verdict=reviewed
file.088.path=.specify/specs/086-efficient-test-execution/test-evidence/scheduling-experiment.txt
file.088.verdict=reviewed
file.089.path=.specify/specs/086-efficient-test-execution/test-evidence/serial-exceptions.txt
file.089.verdict=reviewed
file.090.path=.specify/specs/086-efficient-test-execution/test-evidence/smoke-086.txt
file.090.verdict=reviewed
file.091.path=.specify/specs/086-efficient-test-execution/test-evidence/tasks-gates.txt
file.091.verdict=reviewed
file.092.path=.specify/specs/086-efficient-test-execution/test-evidence/worktree-clean.txt
file.092.verdict=reviewed
file.093.path=.specify/specs/086-efficient-test-execution/verification.md
file.093.verdict=reviewed
file.094.path=.specify/state/086-efficient-test-execution.md
file.094.verdict=reviewed
file.095.path=.specify/templates/constitution-template.md
file.095.verdict=reviewed
file.096.path=.specify/templates/instructions-template.md
file.096.verdict=reviewed
file.097.path=CHANGELOG.md
file.097.verdict=reviewed
file.098.path=CONTRIBUTING.md
file.098.verdict=reviewed
file.099.path=docs/contribute/dev-setup.md
file.099.verdict=reviewed
file.100.path=pyproject.toml
file.100.verdict=reviewed
file.101.path=scripts/bash/run-tests.sh
file.101.verdict=reviewed
file.102.path=shared/guidelines/test-execution-efficiency.md
file.102.verdict=reviewed
file.103.path=skills/external/sdd-loop-driver/scripts/audit-test-budget.py
file.103.verdict=reviewed
file.104.path=skills/internal/manage-constitution/SKILL.md
file.104.verdict=reviewed
file.105.path=templates/constitution-template.md
file.105.verdict=reviewed
file.106.path=templates/instructions-template.md
file.106.verdict=reviewed
file.107.path=tests/contract/test_constitution_double_landing.py
file.107.verdict=reviewed
file.108.path=tests/contract/test_fast_fail_discipline.py
file.108.verdict=reviewed
file.109.path=tests/contract/test_run_tests_runner_contract.py
file.109.verdict=reviewed
file.110.path=tests/contract/test_sdd_loop_driver_skill.py
file.110.verdict=reviewed
file.111.path=tests/contract/test_test_execution_efficiency.py
file.111.verdict=reviewed
file.112.path=tests/integration/test_sdd_loop_efficiency_regression.py
file.112.verdict=reviewed
file.113.path=tests/unit/test_audit_test_budget.py
file.113.verdict=reviewed
<!-- coverage-receipt:end -->
