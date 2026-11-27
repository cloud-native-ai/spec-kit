# Code Review Report — 代码段 (code segment)

| 属性 | 值 |
|------|-----|
| **分支** | `109-prompt-adherence` |
| **基准** | `0419adae5e6e0e208ad6bcb443e45be8d266f04a` (`0419adae5`) |
| **目标** | `25e8b3eacd24407efbf6a306e2f0f8ed79b1279d` (`25e8b3eac`) |
| **基准来源** | `feature-first-commit` |
| **渲染模式** | `renderer: text` |
| **Reviewer** | `Qiming Liu (John)` |
| **日期** | `2026-11-27T08:07:12Z` |

## 变更概览

```
 .../records/20261127T054447252159Z-3c48a908.json   |    1 +
 .../records/20261127T055640170250Z-96fd49d0.json   |    1 +
 .../records/20261127T060915830390Z-e22164b6.json   |    1 +
 .../records/20261127T062302648446Z-7f6063e0.json   |    1 +
 .../records/20261127T063442224599Z-22ac8269.json   |    1 +
 .../records/20261127T065027570009Z-5ac90f32.json   |    1 +
 .../records/20261127T070449750379Z-d92f15f7.json   |    1 +
 .../records/20261127T071712784179Z-14903c95.json   |    1 +
 .../records/20261127T073148915979Z-8cc82e52.json   |    1 +
 .../records/20261127T075951088894Z-4765ee70.json   |    1 +
 .specify/features.md                               |    5 +-
 .specify/features/028-feedback-mechanism.md        |    1 +
 .specify/features/109-prompt-adherence.md          |   72 +
 .../20261127T054453Z-skill-create-requirements.md  |   21 +
 .../20261127T055653Z-skill-clarify-artifact.md     |   22 +
 .specify/feedback/20261127T060931Z-speckit-plan.md |   21 +
 .../feedback/20261127T062316Z-speckit-tasks.md     |   21 +
 .../feedback/20261127T063453Z-speckit-checklist.md |   21 +
 .../feedback/20261127T065038Z-speckit-analyze.md   |   21 +
 .../feedback/20261127T070457Z-speckit-implement.md |   21 +
 .../feedback/20261127T071725Z-speckit-implement.md |   26 +
 .../feedback/20261127T073155Z-speckit-implement.md |   21 +
 .../feedback/20261127T074122Z-speckit-implement.md |   95 ++
 .../feedback/20261127T075958Z-speckit-implement.md |   23 +
 .specify/glossary.md                               |    3 +
 ...27T054508Z-109-prompt-adherence-requirements.md |   29 +
 ...0261127T055653Z-109-prompt-adherence-clarify.md |   30 +
 .specify/scripts/python/prompt-adherence.py        | 1587 ++++++++++++++++++++
 ...ination-speckit-tasks-r20261126t071500z-108a.md |   10 +-
 ...n-skill-create-requirements-r20261127t053750.md |  227 +++
 ...n-skill-clarify-artifact-r20261127t053750z-1.md |  207 +++
 ...mination-speckit-plan-r20261127t053750z-109a.md |  202 +++
 ...ination-speckit-tasks-r20261127t053750z-109a.md |  202 +++
 ...ion-speckit-checklist-r20261127t053750z-109a.md |  202 +++
 ...ation-speckit-analyze-r20261127t053750z-109a.md |  202 +++
 ...ion-speckit-implement-r20261127t053750z-109a.md |  207 +++
 ...n-speckit-implement-r20261127t053750z-109a-p.md |  209 +++
 ...n-speckit-implement-r20261127t053750z-109a-p.md |  209 +++
 ...n-speckit-implement-r20261127t053750z-109a-p.md |  195 +++
 .../facts/prompt-adherence-deviation-classes.yaml  |   13 +
 .../facts/prompt-adherence-layers.yaml             |   12 +
 .../facts/prompt-adherence-reading-status.yaml     |   16 +
 .../facts/prompt-adherence-signals.yaml            |   17 +
 .../facts/prompt-adherence-strengths.yaml          |   12 +
 .../declarations/facts/runtime-store-layout.yaml   |    1 +
 .specify/shared/definitions/framework-map.md       |    2 +
 .../definitions/prompt-adherence-definitions.md    |  186 +++
 .../specs/109-prompt-adherence/baseline-failed.txt |  222 +++
 .../checklists/requirements-quality-2026-11-27.md  |   94 ++
 .../checklists/requirements.md                     |   79 +
 .../checkpoints/01-requirements.md                 |   42 +
 .../109-prompt-adherence/checkpoints/02-clarify.md |   41 +
 .../109-prompt-adherence/checkpoints/03-plan.md    |   40 +
 .../109-prompt-adherence/checkpoints/04-tasks.md   |   43 +
 .../checkpoints/05-checklist.md                    |   42 +
 .../109-prompt-adherence/checkpoints/06-analyze.md |   42 +
 .../checkpoints/07-implement.md                    |   10 +
 .../declarations-and-vocabularies.contract.md      |  111 ++
 .../contracts/distribution.contract.md             |   51 +
 .../contracts/engine-and-read.contract.md          |   87 ++
 .../contracts/guards-and-boundaries.contract.md    |  113 ++
 .../contracts/owner-and-catalog.contract.md        |  122 ++
 .../contracts/reading-semantics.contract.md        |  155 ++
 .../109-prompt-adherence/coverage-baseline.txt     |  787 ++++++++++
 .specify/specs/109-prompt-adherence/data-model.md  |  206 +++
 .specify/specs/109-prompt-adherence/feature-ref.md |   99 ++
 .../specs/109-prompt-adherence/final-failed.txt    |  222 +++
 .../notes/pre-change-measurements.md               |  222 +++
 .../109-prompt-adherence/notes/quickstart-run.md   |  281 ++++
 .../notes/red-first-evidence.md                    |  737 +++++++++
 .specify/specs/109-prompt-adherence/plan.md        |  284 ++++
 .specify/specs/109-prompt-adherence/quickstart.md  |  200 +++
 .../specs/109-prompt-adherence/requirements.md     |  310 ++++
 .specify/specs/109-prompt-adherence/research.md    |  190 +++
 .specify/specs/109-prompt-adherence/tasks.md       |  355 +++++
 .../test-evidence/analyze-round1-findings.jsonl    |   20 +
 .../test-evidence/analyze-round1-report.md         |  163 ++
 .../test-evidence/boundary-readings.txt            |  112 ++
 .../checklist-requirements-validator.txt           |   11 +
 .../test-evidence/checklist-selfcheck.txt          |   98 ++
 .../test-evidence/checklist-spec-readings.txt      |   43 +
 .../test-evidence/checklist-stage-2026-11-27.md    |   67 +
 .../test-evidence/checklist.jsonl                  |    1 +
 .../test-evidence/clarify-stage-2026-11-27.md      |   56 +
 .../test-evidence/clarify-validator-postcommit.txt |   16 +
 .../test-evidence/clarify-validator.txt            |   16 +
 .../test-evidence/decomposition-tasks.json         |   12 +
 .../test-evidence/decomposition-tasks.txt          |    1 +
 .../test-evidence/implementation-gates.txt         |  278 ++++
 .../test-evidence/plan-decision-tensions.txt       |   11 +
 .../test-evidence/plan-integrity.txt               |   10 +
 .../test-evidence/plan-stage-2026-11-27.md         |  192 +++
 .../test-evidence/plan-validate-requirements.txt   |   10 +
 .../test-evidence/pre-analyze-checklist.txt        |    7 +
 .../test-evidence/pre-analyze-plan-postcommit.json |  738 +++++++++
 .../test-evidence/pre-analyze-plan-postcommit.txt  |    2 +
 .../test-evidence/pre-analyze-plan.json            |  738 +++++++++
 .../test-evidence/pre-analyze-plan.txt             |    2 +
 .../test-evidence/pre-analyze-tasks.json           |  906 +++++++++++
 .../test-evidence/pre-analyze-tasks.txt            |    2 +
 .../test-evidence/requirements-stage-2026-11-27.md |  119 ++
 .../test-evidence/smoke-run.txt                    |    8 +
 .../test-evidence/tasks-stage-2026-11-27.md        |  150 ++
 .../test-evidence/tasks-validator.txt              |    1 +
 .../test-evidence/us3-red-init.txt                 |   43 +
 .../test-evidence/us3-red-readonly.txt             |   44 +
 .../workspace-checklist-postcommit.json            |  312 ++++
 .../test-evidence/workspace-checklist-readings.txt |    8 +
 .../test-evidence/workspace-checklist.json         |  312 ++++
 .../test-evidence/workspace-implement-p1.json      |  312 ++++
 .../test-evidence/workspace-implement-p2-post.json |  314 ++++
 .../workspace-implement-p2-readings.txt            |   57 +
 .../test-evidence/workspace-implement-p2.json      |  313 ++++
 .../workspace-implement-p3-readings.txt            |   40 +
 .../test-evidence/workspace-implement-p3.json      |  314 ++++
 .../workspace-implement-p4-readings.txt            |   37 +
 .../test-evidence/workspace-implement-p4.json      |  314 ++++
 .../test-evidence/workspace-plan-postcommit.txt    |    1 +
 .../test-evidence/workspace-plan.json              |  312 ++++
 .../test-evidence/workspace-requirements.json      |  312 ++++
 .../test-evidence/workspace-tasks.json             |  312 ++++
 .../specs/109-prompt-adherence/verification.md     |   80 +
 scripts/python/prompt-adherence.py                 | 1587 ++++++++++++++++++++
 .../facts/prompt-adherence-deviation-classes.yaml  |   13 +
 .../facts/prompt-adherence-layers.yaml             |   12 +
 .../facts/prompt-adherence-reading-status.yaml     |   16 +
 .../facts/prompt-adherence-signals.yaml            |   17 +
 .../facts/prompt-adherence-strengths.yaml          |   12 +
 .../declarations/facts/runtime-store-layout.yaml   |    1 +
 shared/definitions/framework-map.md                |    2 +
 shared/definitions/prompt-adherence-definitions.md |  186 +++
 tests/contract/test_bilingual_expression.py        |    5 +
 .../contract/test_prompt_adherence_declarations.py |  420 ++++++
 tests/contract/test_prompt_adherence_engine.py     | 1288 ++++++++++++++++
 tests/contract/test_prompt_adherence_owner.py      |  590 ++++++++
 tests/contract/test_prompt_adherence_readonly.py   |  353 +++++
 .../evidence/ev-20261126-indirect/findings.json    |   19 +
 .../evidence/ev-20261126-indirect/manifest.json    |    8 +
 .../records/20261126T000200000000Z-00000001.json   |    9 +
 ...000100Z-run-determination-speckit-plan-ridir.md |   29 +
 .../shared/definitions/probe-definitions.md        |   13 +
 .../.specify/evidence/ev-multi-a/findings.json     |   19 +
 .../.specify/evidence/ev-multi-a/manifest.json     |    8 +
 .../.specify/evidence/ev-multi-b/findings.json     |   19 +
 .../.specify/evidence/ev-multi-b/manifest.json     |    8 +
 .../records/20261124T100000000000Z-00000001.json   |    9 +
 .../records/20261125T100000000000Z-00000002.json   |    9 +
 .../feedback/20261124T110000Z-multi-plan-a.md      |   21 +
 .../feedback/20261125T110000Z-multi-plan-b.md      |   21 +
 .../feedback/20261125T120000Z-multi-gate.md        |   21 +
 ...0000Z-run-determination-speckit-plan-multi-a.md |   29 +
 ...0000Z-run-determination-speckit-plan-multi-b.md |   29 +
 ...00Z-run-determination-speckit-review-multi-d.md |   29 +
 ...0000Z-run-determination-speckit-plan-multi-c.md |   29 +
 .../shared/definitions/probe-definitions.md        |   16 +
 .../.specify/evidence/ev-neg-broken/findings.json  |    1 +
 .../evidence/ev-neg-nomanifest/findings.json       |   19 +
 .../.specify/evidence/ev-neg-schema/findings.json  |   19 +
 .../.specify/evidence/ev-neg-schema/manifest.json  |    8 +
 .../records/20261126T000200000000Z-00000001.json   |    9 +
 .../exec-quant/records/broken-unparsable.json      |    1 +
 .../exec-quant/records/unknown-version.json        |    9 +
 .../.specify/feedback/20261126T000300Z-neg-a.md    |   21 +
 .../.specify/feedback/20261126T000300Z-neg-b.md    |   21 +
 .../feedback/20261126T000310Z-neg-badtime.md       |   21 +
 ...T000100Z-run-determination-speckit-plan-rneg.md |   29 +
 .../shared/definitions/probe-definitions.md        |   13 +
 .../records/20261126T000200000000Z-00000001.json   |    9 +
 .../feedback/20261126T000300Z-project-plan.md      |   21 +
 .../project-only/.specify/session/.gitkeep         |    1 +
 .../shared/definitions/probe-definitions.md        |   13 +
 .../recordless/.specify/session/.gitkeep           |    1 +
 .../shared/definitions/probe-definitions.md        |   16 +
 .../evidence/ev-20261126-fixture/findings.json     |   33 +
 .../evidence/ev-20261126-fixture/manifest.json     |    8 +
 .../records/20261126T000200000000Z-00000001.json   |    9 +
 .../feedback/20261126T000300Z-fixture-plan.md      |   21 +
 .../feedback/20261126T000400Z-fixture-gate.md      |   21 +
 ...00030Z-run-determination-speckit-review-rdev.md |   29 +
 ...100Z-run-determination-speckit-plan-rfixture.md |   29 +
 .../shared/definitions/probe-definitions.md        |   16 +
 tests/integration/test_prompt_adherence_init.py    |  265 ++++
 182 files changed, 22298 insertions(+), 7 deletions(-)
```

---

## Review 意见


### 🟢 [SUGGESTION] scripts/python/prompt-adherence.py (Line 1227)

> The --check-coverage action refuses with exit 2 whenever run-determination.py or evidence-utils.py is absent (lines 1225-1229), although the coverage check needs only the owner document and the declaration layer. The owner document's exit-code closure (prompt-adherence-definitions.md, Reading Contract) does not list a sibling-engine absence among the coverage check's failure causes, and the two readers' own 'engine is None -> _unavailable()' branches become unreachable. Suggested fix: take the check-coverage branch before the sensor layer is required (the check's inputs are the owner document plus the five facts), or degrade a missing sibling per row, so the coverage check answers 0/1/2 for its own inputs only.

<sub>16:07:26</sub>


### 🟢 [SUGGESTION] scripts/python/prompt-adherence.py (Line 789)

> _read_exec_quant binds every body returned by the owning load_records back to a file by dict equality; two byte-equal records in different files both resolve to the first matching path, and a body with no equal node falls back to the store label row["store"] (for example .specify/exec-quant), which is not a file a citation-only replay can open. Suggested fix: have the surfaces pass yield (path, body) pairs keyed by file and identity, and treat an unbound body as schema-violation instead of writing a store label into sources[].path.

<sub>16:07:26</sub>


### 👍 [PRAISE] tests/contract/test_prompt_adherence_readonly.py

> The containment claim is decided rather than asserted: the manifest comparison unit is derived from the runtime-store-layout fact through the declaration reader (no second root table), bytecode caches are excluded by name, the complement runs after both per-run and longitudinal readings, and test_manifest_comparison_would_detect_a_store_write proves the comparator goes red on a byte change, a new file and a new root. This is the evidence shape a declared containment claim asks for.

<sub>16:07:30</sub>


### ❓ [QUESTION] scripts/python/prompt-adherence.py (Line 1572)

> The JSON flag is accepted together with --check-coverage, but the coverage branch prints the text finding list (or the clean line) regardless and never a JSON object (main, lines 1572-1583). The owner document's Entry section lists --json without a scope, and quickstart Scenario 5 records both calls printing the same text line. Is ignoring --json in check mode intended? If so, record the scoping in the owner document Entry and the quickstart so a machine consumer is not surprised; otherwise emit a JSON result object (findings, ok) in check mode.

<sub>16:07:34</sub>


<!-- coverage-receipt:begin -->
receipt_version=1
base=0419adae5e6e0e208ad6bcb443e45be8d266f04a
head=25e8b3eacd24407efbf6a306e2f0f8ed79b1279d
base_source=feature-first-commit
renderer=text
changed_files=182
judged_files=19
skipped_files=163
gap_files=0
lines_added=4846
lines_deleted=2
file.001.path=.specify/exec-quant/records/20261127T054447252159Z-3c48a908.json
file.001.verdict=skipped
file.001.reason=generated
file.002.path=.specify/exec-quant/records/20261127T055640170250Z-96fd49d0.json
file.002.verdict=skipped
file.002.reason=generated
file.003.path=.specify/exec-quant/records/20261127T060915830390Z-e22164b6.json
file.003.verdict=skipped
file.003.reason=generated
file.004.path=.specify/exec-quant/records/20261127T062302648446Z-7f6063e0.json
file.004.verdict=skipped
file.004.reason=generated
file.005.path=.specify/exec-quant/records/20261127T063442224599Z-22ac8269.json
file.005.verdict=skipped
file.005.reason=generated
file.006.path=.specify/exec-quant/records/20261127T065027570009Z-5ac90f32.json
file.006.verdict=skipped
file.006.reason=generated
file.007.path=.specify/exec-quant/records/20261127T070449750379Z-d92f15f7.json
file.007.verdict=skipped
file.007.reason=generated
file.008.path=.specify/exec-quant/records/20261127T071712784179Z-14903c95.json
file.008.verdict=skipped
file.008.reason=generated
file.009.path=.specify/exec-quant/records/20261127T073148915979Z-8cc82e52.json
file.009.verdict=skipped
file.009.reason=generated
file.010.path=.specify/exec-quant/records/20261127T075951088894Z-4765ee70.json
file.010.verdict=skipped
file.010.reason=generated
file.011.path=.specify/features.md
file.011.verdict=reviewed
file.012.path=.specify/features/028-feedback-mechanism.md
file.012.verdict=reviewed
file.013.path=.specify/features/109-prompt-adherence.md
file.013.verdict=reviewed
file.014.path=.specify/feedback/20261127T054453Z-skill-create-requirements.md
file.014.verdict=skipped
file.014.reason=generated
file.015.path=.specify/feedback/20261127T055653Z-skill-clarify-artifact.md
file.015.verdict=skipped
file.015.reason=generated
file.016.path=.specify/feedback/20261127T060931Z-speckit-plan.md
file.016.verdict=skipped
file.016.reason=generated
file.017.path=.specify/feedback/20261127T062316Z-speckit-tasks.md
file.017.verdict=skipped
file.017.reason=generated
file.018.path=.specify/feedback/20261127T063453Z-speckit-checklist.md
file.018.verdict=skipped
file.018.reason=generated
file.019.path=.specify/feedback/20261127T065038Z-speckit-analyze.md
file.019.verdict=skipped
file.019.reason=generated
file.020.path=.specify/feedback/20261127T070457Z-speckit-implement.md
file.020.verdict=skipped
file.020.reason=generated
file.021.path=.specify/feedback/20261127T071725Z-speckit-implement.md
file.021.verdict=skipped
file.021.reason=generated
file.022.path=.specify/feedback/20261127T073155Z-speckit-implement.md
file.022.verdict=skipped
file.022.reason=generated
file.023.path=.specify/feedback/20261127T074122Z-speckit-implement.md
file.023.verdict=skipped
file.023.reason=generated
file.024.path=.specify/feedback/20261127T075958Z-speckit-implement.md
file.024.verdict=skipped
file.024.reason=generated
file.025.path=.specify/glossary.md
file.025.verdict=reviewed
file.026.path=.specify/retention/closeout/20261127T054508Z-109-prompt-adherence-requirements.md
file.026.verdict=skipped
file.026.reason=generated
file.027.path=.specify/retention/closeout/20261127T055653Z-109-prompt-adherence-clarify.md
file.027.verdict=skipped
file.027.reason=generated
file.028.path=.specify/scripts/python/prompt-adherence.py
file.028.verdict=skipped
file.028.reason=generated
file.029.path=.specify/session/20261126T084427Z-run-determination-speckit-tasks-r20261126t071500z-108a.md
file.029.verdict=skipped
file.029.reason=generated
file.030.path=.specify/session/20261127T054441Z-run-determination-skill-create-requirements-r20261127t053750.md
file.030.verdict=skipped
file.030.reason=generated
file.031.path=.specify/session/20261127T055636Z-run-determination-skill-clarify-artifact-r20261127t053750z-1.md
file.031.verdict=skipped
file.031.reason=generated
file.032.path=.specify/session/20261127T060910Z-run-determination-speckit-plan-r20261127t053750z-109a.md
file.032.verdict=skipped
file.032.reason=generated
file.033.path=.specify/session/20261127T062255Z-run-determination-speckit-tasks-r20261127t053750z-109a.md
file.033.verdict=skipped
file.033.reason=generated
file.034.path=.specify/session/20261127T063431Z-run-determination-speckit-checklist-r20261127t053750z-109a.md
file.034.verdict=skipped
file.034.reason=generated
file.035.path=.specify/session/20261127T065022Z-run-determination-speckit-analyze-r20261127t053750z-109a.md
file.035.verdict=skipped
file.035.reason=generated
file.036.path=.specify/session/20261127T070444Z-run-determination-speckit-implement-r20261127t053750z-109a.md
file.036.verdict=skipped
file.036.reason=generated
file.037.path=.specify/session/20261127T071703Z-run-determination-speckit-implement-r20261127t053750z-109a-p.md
file.037.verdict=skipped
file.037.reason=generated
file.038.path=.specify/session/20261127T073141Z-run-determination-speckit-implement-r20261127t053750z-109a-p.md
file.038.verdict=skipped
file.038.reason=generated
file.039.path=.specify/session/20261127T075943Z-run-determination-speckit-implement-r20261127t053750z-109a-p.md
file.039.verdict=skipped
file.039.reason=generated
file.040.path=.specify/shared/declarations/facts/prompt-adherence-deviation-classes.yaml
file.040.verdict=skipped
file.040.reason=generated
file.041.path=.specify/shared/declarations/facts/prompt-adherence-layers.yaml
file.041.verdict=skipped
file.041.reason=generated
file.042.path=.specify/shared/declarations/facts/prompt-adherence-reading-status.yaml
file.042.verdict=skipped
file.042.reason=generated
file.043.path=.specify/shared/declarations/facts/prompt-adherence-signals.yaml
file.043.verdict=skipped
file.043.reason=generated
file.044.path=.specify/shared/declarations/facts/prompt-adherence-strengths.yaml
file.044.verdict=skipped
file.044.reason=generated
file.045.path=.specify/shared/declarations/facts/runtime-store-layout.yaml
file.045.verdict=skipped
file.045.reason=generated
file.046.path=.specify/shared/definitions/framework-map.md
file.046.verdict=skipped
file.046.reason=generated
file.047.path=.specify/shared/definitions/prompt-adherence-definitions.md
file.047.verdict=skipped
file.047.reason=generated
file.048.path=.specify/specs/109-prompt-adherence/baseline-failed.txt
file.048.verdict=skipped
file.048.reason=non-code-file
file.049.path=.specify/specs/109-prompt-adherence/checklists/requirements-quality-2026-11-27.md
file.049.verdict=skipped
file.049.reason=non-code-file
file.050.path=.specify/specs/109-prompt-adherence/checklists/requirements.md
file.050.verdict=skipped
file.050.reason=non-code-file
file.051.path=.specify/specs/109-prompt-adherence/checkpoints/01-requirements.md
file.051.verdict=skipped
file.051.reason=non-code-file
file.052.path=.specify/specs/109-prompt-adherence/checkpoints/02-clarify.md
file.052.verdict=skipped
file.052.reason=non-code-file
file.053.path=.specify/specs/109-prompt-adherence/checkpoints/03-plan.md
file.053.verdict=skipped
file.053.reason=non-code-file
file.054.path=.specify/specs/109-prompt-adherence/checkpoints/04-tasks.md
file.054.verdict=skipped
file.054.reason=non-code-file
file.055.path=.specify/specs/109-prompt-adherence/checkpoints/05-checklist.md
file.055.verdict=skipped
file.055.reason=non-code-file
file.056.path=.specify/specs/109-prompt-adherence/checkpoints/06-analyze.md
file.056.verdict=skipped
file.056.reason=non-code-file
file.057.path=.specify/specs/109-prompt-adherence/checkpoints/07-implement.md
file.057.verdict=skipped
file.057.reason=non-code-file
file.058.path=.specify/specs/109-prompt-adherence/contracts/declarations-and-vocabularies.contract.md
file.058.verdict=skipped
file.058.reason=non-code-file
file.059.path=.specify/specs/109-prompt-adherence/contracts/distribution.contract.md
file.059.verdict=skipped
file.059.reason=non-code-file
file.060.path=.specify/specs/109-prompt-adherence/contracts/engine-and-read.contract.md
file.060.verdict=skipped
file.060.reason=non-code-file
file.061.path=.specify/specs/109-prompt-adherence/contracts/guards-and-boundaries.contract.md
file.061.verdict=skipped
file.061.reason=non-code-file
file.062.path=.specify/specs/109-prompt-adherence/contracts/owner-and-catalog.contract.md
file.062.verdict=skipped
file.062.reason=non-code-file
file.063.path=.specify/specs/109-prompt-adherence/contracts/reading-semantics.contract.md
file.063.verdict=skipped
file.063.reason=non-code-file
file.064.path=.specify/specs/109-prompt-adherence/coverage-baseline.txt
file.064.verdict=skipped
file.064.reason=non-code-file
file.065.path=.specify/specs/109-prompt-adherence/data-model.md
file.065.verdict=skipped
file.065.reason=non-code-file
file.066.path=.specify/specs/109-prompt-adherence/feature-ref.md
file.066.verdict=skipped
file.066.reason=non-code-file
file.067.path=.specify/specs/109-prompt-adherence/final-failed.txt
file.067.verdict=skipped
file.067.reason=non-code-file
file.068.path=.specify/specs/109-prompt-adherence/notes/pre-change-measurements.md
file.068.verdict=skipped
file.068.reason=non-code-file
file.069.path=.specify/specs/109-prompt-adherence/notes/quickstart-run.md
file.069.verdict=skipped
file.069.reason=non-code-file
file.070.path=.specify/specs/109-prompt-adherence/notes/red-first-evidence.md
file.070.verdict=skipped
file.070.reason=non-code-file
file.071.path=.specify/specs/109-prompt-adherence/plan.md
file.071.verdict=skipped
file.071.reason=non-code-file
file.072.path=.specify/specs/109-prompt-adherence/quickstart.md
file.072.verdict=skipped
file.072.reason=non-code-file
file.073.path=.specify/specs/109-prompt-adherence/requirements.md
file.073.verdict=skipped
file.073.reason=non-code-file
file.074.path=.specify/specs/109-prompt-adherence/research.md
file.074.verdict=skipped
file.074.reason=non-code-file
file.075.path=.specify/specs/109-prompt-adherence/tasks.md
file.075.verdict=skipped
file.075.reason=non-code-file
file.076.path=.specify/specs/109-prompt-adherence/test-evidence/analyze-round1-findings.jsonl
file.076.verdict=skipped
file.076.reason=non-code-file
file.077.path=.specify/specs/109-prompt-adherence/test-evidence/analyze-round1-report.md
file.077.verdict=skipped
file.077.reason=non-code-file
file.078.path=.specify/specs/109-prompt-adherence/test-evidence/boundary-readings.txt
file.078.verdict=skipped
file.078.reason=non-code-file
file.079.path=.specify/specs/109-prompt-adherence/test-evidence/checklist-requirements-validator.txt
file.079.verdict=skipped
file.079.reason=non-code-file
file.080.path=.specify/specs/109-prompt-adherence/test-evidence/checklist-selfcheck.txt
file.080.verdict=skipped
file.080.reason=non-code-file
file.081.path=.specify/specs/109-prompt-adherence/test-evidence/checklist-spec-readings.txt
file.081.verdict=skipped
file.081.reason=non-code-file
file.082.path=.specify/specs/109-prompt-adherence/test-evidence/checklist-stage-2026-11-27.md
file.082.verdict=skipped
file.082.reason=non-code-file
file.083.path=.specify/specs/109-prompt-adherence/test-evidence/checklist.jsonl
file.083.verdict=skipped
file.083.reason=non-code-file
file.084.path=.specify/specs/109-prompt-adherence/test-evidence/clarify-stage-2026-11-27.md
file.084.verdict=skipped
file.084.reason=non-code-file
file.085.path=.specify/specs/109-prompt-adherence/test-evidence/clarify-validator-postcommit.txt
file.085.verdict=skipped
file.085.reason=non-code-file
file.086.path=.specify/specs/109-prompt-adherence/test-evidence/clarify-validator.txt
file.086.verdict=skipped
file.086.reason=non-code-file
file.087.path=.specify/specs/109-prompt-adherence/test-evidence/decomposition-tasks.json
file.087.verdict=skipped
file.087.reason=non-code-file
file.088.path=.specify/specs/109-prompt-adherence/test-evidence/decomposition-tasks.txt
file.088.verdict=skipped
file.088.reason=non-code-file
file.089.path=.specify/specs/109-prompt-adherence/test-evidence/implementation-gates.txt
file.089.verdict=skipped
file.089.reason=non-code-file
file.090.path=.specify/specs/109-prompt-adherence/test-evidence/plan-decision-tensions.txt
file.090.verdict=skipped
file.090.reason=non-code-file
file.091.path=.specify/specs/109-prompt-adherence/test-evidence/plan-integrity.txt
file.091.verdict=skipped
file.091.reason=non-code-file
file.092.path=.specify/specs/109-prompt-adherence/test-evidence/plan-stage-2026-11-27.md
file.092.verdict=skipped
file.092.reason=non-code-file
file.093.path=.specify/specs/109-prompt-adherence/test-evidence/plan-validate-requirements.txt
file.093.verdict=skipped
file.093.reason=non-code-file
file.094.path=.specify/specs/109-prompt-adherence/test-evidence/pre-analyze-checklist.txt
file.094.verdict=skipped
file.094.reason=non-code-file
file.095.path=.specify/specs/109-prompt-adherence/test-evidence/pre-analyze-plan-postcommit.json
file.095.verdict=skipped
file.095.reason=non-code-file
file.096.path=.specify/specs/109-prompt-adherence/test-evidence/pre-analyze-plan-postcommit.txt
file.096.verdict=skipped
file.096.reason=non-code-file
file.097.path=.specify/specs/109-prompt-adherence/test-evidence/pre-analyze-plan.json
file.097.verdict=skipped
file.097.reason=non-code-file
file.098.path=.specify/specs/109-prompt-adherence/test-evidence/pre-analyze-plan.txt
file.098.verdict=skipped
file.098.reason=non-code-file
file.099.path=.specify/specs/109-prompt-adherence/test-evidence/pre-analyze-tasks.json
file.099.verdict=skipped
file.099.reason=non-code-file
file.100.path=.specify/specs/109-prompt-adherence/test-evidence/pre-analyze-tasks.txt
file.100.verdict=skipped
file.100.reason=non-code-file
file.101.path=.specify/specs/109-prompt-adherence/test-evidence/requirements-stage-2026-11-27.md
file.101.verdict=skipped
file.101.reason=non-code-file
file.102.path=.specify/specs/109-prompt-adherence/test-evidence/smoke-run.txt
file.102.verdict=skipped
file.102.reason=non-code-file
file.103.path=.specify/specs/109-prompt-adherence/test-evidence/tasks-stage-2026-11-27.md
file.103.verdict=skipped
file.103.reason=non-code-file
file.104.path=.specify/specs/109-prompt-adherence/test-evidence/tasks-validator.txt
file.104.verdict=skipped
file.104.reason=non-code-file
file.105.path=.specify/specs/109-prompt-adherence/test-evidence/us3-red-init.txt
file.105.verdict=skipped
file.105.reason=non-code-file
file.106.path=.specify/specs/109-prompt-adherence/test-evidence/us3-red-readonly.txt
file.106.verdict=skipped
file.106.reason=non-code-file
file.107.path=.specify/specs/109-prompt-adherence/test-evidence/workspace-checklist-postcommit.json
file.107.verdict=skipped
file.107.reason=non-code-file
file.108.path=.specify/specs/109-prompt-adherence/test-evidence/workspace-checklist-readings.txt
file.108.verdict=skipped
file.108.reason=non-code-file
file.109.path=.specify/specs/109-prompt-adherence/test-evidence/workspace-checklist.json
file.109.verdict=skipped
file.109.reason=non-code-file
file.110.path=.specify/specs/109-prompt-adherence/test-evidence/workspace-implement-p1.json
file.110.verdict=skipped
file.110.reason=non-code-file
file.111.path=.specify/specs/109-prompt-adherence/test-evidence/workspace-implement-p2-post.json
file.111.verdict=skipped
file.111.reason=non-code-file
file.112.path=.specify/specs/109-prompt-adherence/test-evidence/workspace-implement-p2-readings.txt
file.112.verdict=skipped
file.112.reason=non-code-file
file.113.path=.specify/specs/109-prompt-adherence/test-evidence/workspace-implement-p2.json
file.113.verdict=skipped
file.113.reason=non-code-file
file.114.path=.specify/specs/109-prompt-adherence/test-evidence/workspace-implement-p3-readings.txt
file.114.verdict=skipped
file.114.reason=non-code-file
file.115.path=.specify/specs/109-prompt-adherence/test-evidence/workspace-implement-p3.json
file.115.verdict=skipped
file.115.reason=non-code-file
file.116.path=.specify/specs/109-prompt-adherence/test-evidence/workspace-implement-p4-readings.txt
file.116.verdict=skipped
file.116.reason=non-code-file
file.117.path=.specify/specs/109-prompt-adherence/test-evidence/workspace-implement-p4.json
file.117.verdict=skipped
file.117.reason=non-code-file
file.118.path=.specify/specs/109-prompt-adherence/test-evidence/workspace-plan-postcommit.txt
file.118.verdict=skipped
file.118.reason=non-code-file
file.119.path=.specify/specs/109-prompt-adherence/test-evidence/workspace-plan.json
file.119.verdict=skipped
file.119.reason=non-code-file
file.120.path=.specify/specs/109-prompt-adherence/test-evidence/workspace-requirements.json
file.120.verdict=skipped
file.120.reason=non-code-file
file.121.path=.specify/specs/109-prompt-adherence/test-evidence/workspace-tasks.json
file.121.verdict=skipped
file.121.reason=non-code-file
file.122.path=.specify/specs/109-prompt-adherence/verification.md
file.122.verdict=skipped
file.122.reason=non-code-file
file.123.path=scripts/python/prompt-adherence.py
file.123.verdict=reviewed
file.124.path=shared/declarations/facts/prompt-adherence-deviation-classes.yaml
file.124.verdict=reviewed
file.125.path=shared/declarations/facts/prompt-adherence-layers.yaml
file.125.verdict=reviewed
file.126.path=shared/declarations/facts/prompt-adherence-reading-status.yaml
file.126.verdict=reviewed
file.127.path=shared/declarations/facts/prompt-adherence-signals.yaml
file.127.verdict=reviewed
file.128.path=shared/declarations/facts/prompt-adherence-strengths.yaml
file.128.verdict=reviewed
file.129.path=shared/declarations/facts/runtime-store-layout.yaml
file.129.verdict=reviewed
file.130.path=shared/definitions/framework-map.md
file.130.verdict=reviewed
file.131.path=shared/definitions/prompt-adherence-definitions.md
file.131.verdict=reviewed
file.132.path=tests/contract/test_bilingual_expression.py
file.132.verdict=reviewed
file.133.path=tests/contract/test_prompt_adherence_declarations.py
file.133.verdict=reviewed
file.134.path=tests/contract/test_prompt_adherence_engine.py
file.134.verdict=reviewed
file.135.path=tests/contract/test_prompt_adherence_owner.py
file.135.verdict=reviewed
file.136.path=tests/contract/test_prompt_adherence_readonly.py
file.136.verdict=reviewed
file.137.path=tests/fixtures/prompt-adherence/indirect-only/.specify/evidence/ev-20261126-indirect/findings.json
file.137.verdict=skipped
file.137.reason=non-code-file
file.138.path=tests/fixtures/prompt-adherence/indirect-only/.specify/evidence/ev-20261126-indirect/manifest.json
file.138.verdict=skipped
file.138.reason=non-code-file
file.139.path=tests/fixtures/prompt-adherence/indirect-only/.specify/exec-quant/records/20261126T000200000000Z-00000001.json
file.139.verdict=skipped
file.139.reason=non-code-file
file.140.path=tests/fixtures/prompt-adherence/indirect-only/.specify/session/20261126T000100Z-run-determination-speckit-plan-ridir.md
file.140.verdict=skipped
file.140.reason=non-code-file
file.141.path=tests/fixtures/prompt-adherence/indirect-only/.specify/shared/definitions/probe-definitions.md
file.141.verdict=skipped
file.141.reason=non-code-file
file.142.path=tests/fixtures/prompt-adherence/multi-run/.specify/evidence/ev-multi-a/findings.json
file.142.verdict=skipped
file.142.reason=non-code-file
file.143.path=tests/fixtures/prompt-adherence/multi-run/.specify/evidence/ev-multi-a/manifest.json
file.143.verdict=skipped
file.143.reason=non-code-file
file.144.path=tests/fixtures/prompt-adherence/multi-run/.specify/evidence/ev-multi-b/findings.json
file.144.verdict=skipped
file.144.reason=non-code-file
file.145.path=tests/fixtures/prompt-adherence/multi-run/.specify/evidence/ev-multi-b/manifest.json
file.145.verdict=skipped
file.145.reason=non-code-file
file.146.path=tests/fixtures/prompt-adherence/multi-run/.specify/exec-quant/records/20261124T100000000000Z-00000001.json
file.146.verdict=skipped
file.146.reason=non-code-file
file.147.path=tests/fixtures/prompt-adherence/multi-run/.specify/exec-quant/records/20261125T100000000000Z-00000002.json
file.147.verdict=skipped
file.147.reason=non-code-file
file.148.path=tests/fixtures/prompt-adherence/multi-run/.specify/feedback/20261124T110000Z-multi-plan-a.md
file.148.verdict=skipped
file.148.reason=non-code-file
file.149.path=tests/fixtures/prompt-adherence/multi-run/.specify/feedback/20261125T110000Z-multi-plan-b.md
file.149.verdict=skipped
file.149.reason=non-code-file
file.150.path=tests/fixtures/prompt-adherence/multi-run/.specify/feedback/20261125T120000Z-multi-gate.md
file.150.verdict=skipped
file.150.reason=non-code-file
file.151.path=tests/fixtures/prompt-adherence/multi-run/.specify/session/20261123T090000Z-run-determination-speckit-plan-multi-a.md
file.151.verdict=skipped
file.151.reason=non-code-file
file.152.path=tests/fixtures/prompt-adherence/multi-run/.specify/session/20261125T000000Z-run-determination-speckit-plan-multi-b.md
file.152.verdict=skipped
file.152.reason=non-code-file
file.153.path=tests/fixtures/prompt-adherence/multi-run/.specify/session/20261125T060000Z-run-determination-speckit-review-multi-d.md
file.153.verdict=skipped
file.153.reason=non-code-file
file.154.path=tests/fixtures/prompt-adherence/multi-run/.specify/session/20261126T000000Z-run-determination-speckit-plan-multi-c.md
file.154.verdict=skipped
file.154.reason=non-code-file
file.155.path=tests/fixtures/prompt-adherence/multi-run/.specify/shared/definitions/probe-definitions.md
file.155.verdict=skipped
file.155.reason=non-code-file
file.156.path=tests/fixtures/prompt-adherence/negative/.specify/evidence/ev-neg-broken/findings.json
file.156.verdict=skipped
file.156.reason=non-code-file
file.157.path=tests/fixtures/prompt-adherence/negative/.specify/evidence/ev-neg-nomanifest/findings.json
file.157.verdict=skipped
file.157.reason=non-code-file
file.158.path=tests/fixtures/prompt-adherence/negative/.specify/evidence/ev-neg-schema/findings.json
file.158.verdict=skipped
file.158.reason=non-code-file
file.159.path=tests/fixtures/prompt-adherence/negative/.specify/evidence/ev-neg-schema/manifest.json
file.159.verdict=skipped
file.159.reason=non-code-file
file.160.path=tests/fixtures/prompt-adherence/negative/.specify/exec-quant/records/20261126T000200000000Z-00000001.json
file.160.verdict=skipped
file.160.reason=non-code-file
file.161.path=tests/fixtures/prompt-adherence/negative/.specify/exec-quant/records/broken-unparsable.json
file.161.verdict=skipped
file.161.reason=non-code-file
file.162.path=tests/fixtures/prompt-adherence/negative/.specify/exec-quant/records/unknown-version.json
file.162.verdict=skipped
file.162.reason=non-code-file
file.163.path=tests/fixtures/prompt-adherence/negative/.specify/feedback/20261126T000300Z-neg-a.md
file.163.verdict=skipped
file.163.reason=non-code-file
file.164.path=tests/fixtures/prompt-adherence/negative/.specify/feedback/20261126T000300Z-neg-b.md
file.164.verdict=skipped
file.164.reason=non-code-file
file.165.path=tests/fixtures/prompt-adherence/negative/.specify/feedback/20261126T000310Z-neg-badtime.md
file.165.verdict=skipped
file.165.reason=non-code-file
file.166.path=tests/fixtures/prompt-adherence/negative/.specify/session/20261126T000100Z-run-determination-speckit-plan-rneg.md
file.166.verdict=skipped
file.166.reason=non-code-file
file.167.path=tests/fixtures/prompt-adherence/negative/.specify/shared/definitions/probe-definitions.md
file.167.verdict=skipped
file.167.reason=non-code-file
file.168.path=tests/fixtures/prompt-adherence/project-only/.specify/exec-quant/records/20261126T000200000000Z-00000001.json
file.168.verdict=skipped
file.168.reason=non-code-file
file.169.path=tests/fixtures/prompt-adherence/project-only/.specify/feedback/20261126T000300Z-project-plan.md
file.169.verdict=skipped
file.169.reason=non-code-file
file.170.path=tests/fixtures/prompt-adherence/project-only/.specify/session/.gitkeep
file.170.verdict=skipped
file.170.reason=non-code-file
file.171.path=tests/fixtures/prompt-adherence/project-only/.specify/shared/definitions/probe-definitions.md
file.171.verdict=skipped
file.171.reason=non-code-file
file.172.path=tests/fixtures/prompt-adherence/recordless/.specify/session/.gitkeep
file.172.verdict=skipped
file.172.reason=non-code-file
file.173.path=tests/fixtures/prompt-adherence/recordless/.specify/shared/definitions/probe-definitions.md
file.173.verdict=skipped
file.173.reason=non-code-file
file.174.path=tests/fixtures/prompt-adherence/seeded/.specify/evidence/ev-20261126-fixture/findings.json
file.174.verdict=skipped
file.174.reason=non-code-file
file.175.path=tests/fixtures/prompt-adherence/seeded/.specify/evidence/ev-20261126-fixture/manifest.json
file.175.verdict=skipped
file.175.reason=non-code-file
file.176.path=tests/fixtures/prompt-adherence/seeded/.specify/exec-quant/records/20261126T000200000000Z-00000001.json
file.176.verdict=skipped
file.176.reason=non-code-file
file.177.path=tests/fixtures/prompt-adherence/seeded/.specify/feedback/20261126T000300Z-fixture-plan.md
file.177.verdict=skipped
file.177.reason=non-code-file
file.178.path=tests/fixtures/prompt-adherence/seeded/.specify/feedback/20261126T000400Z-fixture-gate.md
file.178.verdict=skipped
file.178.reason=non-code-file
file.179.path=tests/fixtures/prompt-adherence/seeded/.specify/session/20261126T000030Z-run-determination-speckit-review-rdev.md
file.179.verdict=skipped
file.179.reason=non-code-file
file.180.path=tests/fixtures/prompt-adherence/seeded/.specify/session/20261126T000100Z-run-determination-speckit-plan-rfixture.md
file.180.verdict=skipped
file.180.reason=non-code-file
file.181.path=tests/fixtures/prompt-adherence/seeded/.specify/shared/definitions/probe-definitions.md
file.181.verdict=skipped
file.181.reason=non-code-file
file.182.path=tests/integration/test_prompt_adherence_init.py
file.182.verdict=reviewed
<!-- coverage-receipt:end -->
