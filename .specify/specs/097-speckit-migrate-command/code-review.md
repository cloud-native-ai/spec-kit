# Code Review Report — 代码段 (code segment)

| 属性 | 值 |
|------|-----|
| **分支** | `097-speckit-migrate-command` |
| **基准** | `b3da3a26dfba209057f65c2b17962b9516812c39` (`b3da3a26d`) |
| **目标** | `da34a3d44132852a348b61ba0be64ea8efcffef9` (`da34a3d44`) |
| **基准来源** | `feature-first-commit` |
| **渲染模式** | `renderer: text` |
| **Reviewer** | `Qiming Liu (John)` |
| **日期** | `2026-11-10T16:14:19Z` |

## 变更概览

```
 .claude/commands/speckit.migrate.md                |   53 +
 .github/prompts/speckit.migrate.prompt.md          |   53 +
 .gitignore                                         |    1 +
 .opencode/command/speckit.migrate.md               |   53 +
 .qoder/commands/speckit.migrate.md                 |   56 +
 .specify/constitution.md                           |   16 +-
 .specify/features.md                               |    4 +-
 .../024-specification-workspace-versioning.md      |   39 +-
 .specify/glossary.md                               |    1 +
 .../records/20261110T082839436644Z-53d14cf3.json   |    1 +
 .../records/20261110T082846141283Z-405b4d90.json   |    1 +
 .../records/20261110T091915833571Z-15415ec2.json   |    1 +
 .../records/20261110T092846104188Z-9c45d0a6.json   |    1 +
 .../records/20261110T094505845818Z-0077ef43.json   |    1 +
 .../records/20261110T155444460533Z-450cd970.json   |    1 +
 .../records/20261110T155444794098Z-76bf4398.json   |    1 +
 .../records/20261110T155445130293Z-03d131db.json   |    1 +
 .../records/20261110T155445461083Z-9a313aa5.json   |    1 +
 .../20261110T082853Z-speckit-requirements.md       |   19 +
 .../20261110T082855Z-skill-create-requirements.md  |   19 +
 .../feedback/20261110T091920Z-speckit-tasks.md     |   19 +
 .../feedback/20261110T092854Z-speckit-checklist.md |   19 +
 .../20261110T094516Z-skill-analyze-artifacts.md    |   21 +
 .../feedback/20261110T155453Z-skill-code-review.md |   20 +
 ...0261110T155453Z-skill-review-feature-quality.md |   20 +
 .../20261110T155453Z-skill-review-sdd-process.md   |   20 +
 .../feedback/20261110T155453Z-speckit-review.md    |   22 +
 .../20261110T083120Z-r20261110T081104Z-b097.json   |   38 +
 .../20261110T091952Z-r20261110T081104Z-b097.json   |   24 +
 .../20261110T092942Z-r20261110T081104Z-b097.json   |   24 +
 .../20261110T094542Z-r20261110T081104Z-b097.json   |   29 +
 .../20261110T155531Z-r20261110T081104Z-b097.json   |   94 +
 ...nation-speckit-review-r20261106t040353z-087a.md |   34 +-
 ...n-skill-code-review-r20261106t105429z-087rev.md |   31 +-
 ...nation-speckit-review-r20261108t220214z-8647.md |   14 +-
 ...n-skill-review-feature-quality-r20261109t023.md |   31 +-
 ...n-skill-review-sdd-process-r20261109t023000z.md |   31 +-
 ...on-skill-analyze-artifacts-r20261109t064500z.md |   10 +-
 ...n-speckit-requirements-r20261110t081104z-b09.md |  200 +
 ...n-skill-create-requirements-r20261110t081104.md |  200 +
 ...ination-speckit-tasks-r20261110t081104z-b097.md |  200 +
 ...ion-speckit-checklist-r20261110t081104z-b097.md |  200 +
 ...on-skill-analyze-artifacts-r20261110t081104z.md |  202 +
 ...ion-skill-code-review-r20261110t081104z-b097.md |  210 +
 ...n-skill-review-feature-quality-r20261110t081.md |  210 +
 ...n-skill-review-sdd-process-r20261110t081104z.md |  210 +
 ...nation-speckit-review-r20261110t081104z-b097.md |  210 +
 .../shared/definitions/flow-class-definitions.md   |    1 +
 .specify/shared/definitions/framework-map.md       |    3 +-
 .specify/shared/guidelines/better-harness.md       |    4 +-
 .../skills/internal/sanitize-materials/SKILL.md    |   20 +-
 .../contracts/command-classification.md            |    6 +-
 .../baseline-failed.txt                            |  278 +
 .../checklists/requirements-quality-2026-11-10.md  |   80 +
 .../checklists/requirements.md                     |   39 +
 .../checkpoints/03-plan.md                         |   11 +
 .../097-speckit-migrate-command/code-review.md     |  524 ++
 .../contracts/migrate-cli.md                       |   87 +
 .../contracts/migrate-engine.md                    |   90 +
 .../contracts/migrate-template.md                  |   59 +
 .../coverage-baseline.txt                          |  642 ++
 .../097-speckit-migrate-command/data-model.md      |  144 +
 .../097-speckit-migrate-command/feature-ref.md     |   53 +
 .../notes/pre-change-measurements.md               |   83 +
 .../notes/quickstart-run.md                        |  300 +
 .../notes/red-first-evidence.md                    |  228 +
 .specify/specs/097-speckit-migrate-command/plan.md |  202 +
 .../097-speckit-migrate-command/quickstart.md      |   84 +
 .../097-speckit-migrate-command/requirements.md    |  236 +
 .../specs/097-speckit-migrate-command/research.md  |  101 +
 .../specs/097-speckit-migrate-command/review.md    |  313 +
 .../specs/097-speckit-migrate-command/tasks.md     |  380 +
 .../test-evidence/analyze-findings-W1.md           |  129 +
 .../test-evidence/analyze-findings-W2.md           |   39 +
 .../test-evidence/analyze-findings-W3.md           |   36 +
 .../test-evidence/analyze-findings-round2-W1.md    |  151 +
 .../test-evidence/analyze-findings-round2-W2.md    |   58 +
 .../test-evidence/analyze-findings-round2-W3.md    |   62 +
 .../test-evidence/analyze-gates-r3-2026-11-10.txt  |  757 ++
 .../test-evidence/analyze-merged-2026-11-10.md     |  295 +
 .../test-evidence/analyze-merged-r3-2026-11-10.md  |  308 +
 .../analyze-merged-round2-2026-11-10.md            |  385 +
 .../analyze-repair-dispositions-2026-11-10.md      |   35 +
 .../analyze-repair-dispositions-r3-2026-11-10.md   |   31 +
 .../analyze-repair-gates-2026-11-10.txt            |   37 +
 .../analyze-repair-gates-r3-2026-11-10.txt         |   73 +
 .../checklist-readings-2026-11-10.txt              |   43 +
 .../closure-verdict-implemented-2026-11-10.json    |   38 +
 .../closure-verdict-pre-flip-2026-11-10.json       |   38 +
 .../test-evidence/final-suite.txt                  |   65 +
 .../implement-carrier-repair-2026-11-10.md         |   15 +
 .../implement-entry-baseline-suite.txt             | 9560 ++++++++++++++++++++
 .../implement-entry-coverage-live.txt              |  701 ++
 .../test-evidence/implement-env-probe.txt          |   43 +
 .../test-evidence/mirror-verify.txt                |   59 +
 .../test-evidence/pkg02-baseline-attribution.txt   |   52 +
 .../test-evidence/pkg02-c20-post-stage.txt         |    7 +
 .../test-evidence/pkg02-engine-contract.txt        |    7 +
 .../test-evidence/pkg02-foundation-suite.txt       |    7 +
 .../test-evidence/pkg02-full-failed.txt            |  277 +
 .../test-evidence/pkg02-full-suite.txt             | 9489 +++++++++++++++++++
 .../test-evidence/pkg02-new-failures.txt           |    4 +
 .../test-evidence/pkg02-tasks-validator.txt        |    1 +
 .../test-evidence/pkg03-baseline-attribution.txt   |   42 +
 .../test-evidence/pkg03-full-failed.txt            |  277 +
 .../test-evidence/pkg04-baseline-attribution.txt   |   46 +
 .../test-evidence/pkg04-full-failed.txt            |  276 +
 .../test-evidence/plan-audit.md                    |   29 +
 .../test-evidence/plan-gates.txt                   |   91 +
 .../red-base-probe-guard-2026-11-10.txt            |  143 +
 .../requirements-flow-class-lookup.txt             |    7 +
 .../test-evidence/requirements-glossary-add.txt    |    5 +
 .../requirements-glossary-conflict.txt             |    5 +
 .../test-evidence/requirements-validator.txt       |   10 +
 .../review-repair-dispositions-r1-2026-11-10.md    |   43 +
 .../test-evidence/tasks-validator.txt              |   22 +
 .../test-evidence/us1-converge.txt                 |   52 +
 .../test-evidence/us2-safety.txt                   |   88 +
 .../test-evidence/us3-crossversion.txt             |   68 +
 .../test-evidence/us4-equivalence.txt              |   86 +
 .../097-speckit-migrate-command/verification.md    |  177 +
 docs/reference/commands/migrate.md                 |   59 +
 shared/definitions/flow-class-definitions.md       |    1 +
 shared/definitions/framework-map.md                |    3 +-
 shared/guidelines/better-harness.md                |    4 +-
 skills/internal/sanitize-materials/SKILL.md        |   20 +-
 src/specify_cli/__init__.py                        | 2441 ++++-
 templates/commands/migrate.md                      |   57 +
 tests/contract/test_delegation_classes.py          |    6 +-
 tests/contract/test_expression_compatibility.py    |    3 +
 tests/contract/test_expression_gate_wiring.py      |    4 +-
 tests/contract/test_fast_fail_discipline.py        |    5 +-
 .../test_feedback_command_classification.py        |    6 +-
 tests/contract/test_flow_class_ledger.py           |   25 +-
 tests/contract/test_humanize_command_surface.py    |   13 +-
 tests/contract/test_migrate_cli_surface.py         |  208 +
 .../contract/test_migrate_distribution_assembly.py |  163 +
 tests/contract/test_migrate_engine_contract.py     |  265 +
 tests/contract/test_migrate_template.py            |  202 +
 tests/contract/test_migration_distribution.py      |    8 +-
 tests/fixtures/migrate-097/builders.py             |  236 +
 tests/integration/test_migrate_us1_converge.py     |  342 +
 tests/integration/test_migrate_us2_safety.py       |  685 ++
 tests/integration/test_migrate_us3_crossversion.py |  508 ++
 tests/integration/test_migrate_us4_equivalence.py  |  280 +
 tests/unit/test_migrate_planner.py                 |  325 +
 tests/unit/test_migrate_receipts.py                |  154 +
 147 files changed, 36522 insertions(+), 404 deletions(-)
```

---

## Review 意见


### 🟢 [SUGGESTION] tests/integration/test_migrate_us2_safety.py (Line 250)

> The 'pointer is not restated' assertion scans the same file that defines MIGRATE_DESTRUCTIVE_CRITERIA_POINTER, so it is trivially true whenever the equality assertion above it passes. Assert instead that the owner file .specify/shared/guidelines/confirmation-gates.md exists, or that the migrate segment carries no destructive-list literal.

<sub>00:14:54</sub>


### 🟢 [SUGGESTION] tests/integration/test_migrate_us2_safety.py (Line 580)

> Mutations 1-3 wrap whole _assert_* helpers in pytest.raises(AssertionError) (also :621, :660, :662); the helper's first statement can raise AssertionError on a crash or a different failure, so the red-ability proof can be green for the wrong reason. Same shape at tests/integration/test_migrate_us3_crossversion.py:505. Narrow each wrapper to the specific assertion or assert the failure message.

<sub>00:14:54</sub>


### 🟢 [SUGGESTION] tests/contract/test_migrate_engine_contract.py (Line 231)

> Only test_init_and_migrate_share_one_decision_function carries @pytest.mark.contract and the module declares no pytestmark, so the other contract tests are invisible to the documented '-m contract' selection. Add pytestmark = pytest.mark.contract at module level and drop the per-test marker.

<sub>00:14:54</sub>


### 🟢 [SUGGESTION] tests/contract/test_migrate_cli_surface.py (Line 94)

> C-1's closed option set is sampled by the presence of four names in --help output; an added --quiet/--verbose would pass both this test and the --help presence test. Derive the declared option set from the Typer command params and assert equality with the expected closed set.

<sub>00:14:54</sub>


### 🟢 [SUGGESTION] tests/contract/test_migrate_template.py (Line 197)

> The T-4 'generic coverage' test is a two-substring existence check on the generic Qoder contract; it does not prove the generic test still globs every copy. Parametrize the copy list from the .qoder/commands directory listing or assert the generic test's glob pattern still resolves the migrate copy.

<sub>00:14:54</sub>


### 🟢 [SUGGESTION] tests/integration/test_migrate_us3_crossversion.py (Line 301)

> if stamp['commit'] != 'unavailable' silently degrades the 'recorded verbatim' assertion when the fixture runs without git; the claim then collapses to the same default on both sides. Skip with a named reason or pin the fixture's commit value so the assertion always runs.

<sub>00:14:54</sub>


### ⚪ [NITPICK] .gitignore (Line 38)

> The comment 'Constitution VII closure carriers are versioned records, not runtime logs' outlived the negation rule it described; no '!.specify/specs/*/verification.log' remains and git check-ignore still ignores that path. Remove the orphan comment or restore the rule if the carrier ever moves back to .log.

<sub>00:14:54</sub>


### 👍 [PRAISE] src/specify_cli/__init__.py (Line 3400)

> The rebuilt zero-write probe guard is observable on both limbs (sentinel transient directory + workspace digest) and carries a red-base drill; engine strengths preserved: single-table closed domains, byte-identical deterministic plan payload, exclusive O_EXCL receipt creation, archive-before-write on every replace, resume judged from the old receipt's own archiveTo paths, and one init/migrate decision implementation.

<sub>00:14:54</sub>

> **Repair verification (this run)**: the two prior `important` items are fixed and were re-checked — the `--help` zero-side-effect limb now chdirs into and snapshots the workspace it inspects, and C-1/docs/template converged to `--help` with `-h` pinned as an undeclared option (exit 2). The prior `blocking` item (unfailable zero-write probe) was rebuilt into an observable guard plus a fifth red-ability mutation; `test-evidence/red-base-probe-guard-2026-11-10.txt` records both red variants and the reverted green run. No `blocking` entry stands in this record.



> **未提交范围（未评审）**: 6 个未提交路径未计入本次评审对象（.specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt, .specify/specs/097-speckit-migrate-command/review.md, .specify/specs/097-speckit-migrate-command/checkpoints/01-requirements.md, .specify/specs/097-speckit-migrate-command/checkpoints/02-clarify.md, .specify/specs/097-speckit-migrate-command/review-097-speckit-migrate-command.md, .specify/specs/097-speckit-migrate-command/test-evidence/analyze-validation-round2-2026-11-10.md）；本回执不对该范围给出任何结论。

<!-- coverage-receipt:begin -->
receipt_version=1
base=b3da3a26dfba209057f65c2b17962b9516812c39
head=da34a3d44132852a348b61ba0be64ea8efcffef9
base_source=feature-first-commit
renderer=text
changed_files=147
judged_files=107
skipped_files=40
gap_files=0
lines_added=36522
lines_deleted=404
file.001.path=.claude/commands/speckit.migrate.md
file.001.verdict=reviewed
file.002.path=.github/prompts/speckit.migrate.prompt.md
file.002.verdict=reviewed
file.003.path=.gitignore
file.003.verdict=reviewed
file.004.path=.opencode/command/speckit.migrate.md
file.004.verdict=reviewed
file.005.path=.qoder/commands/speckit.migrate.md
file.005.verdict=reviewed
file.006.path=.specify/constitution.md
file.006.verdict=reviewed
file.007.path=.specify/features.md
file.007.verdict=reviewed
file.008.path=.specify/features/024-specification-workspace-versioning.md
file.008.verdict=reviewed
file.009.path=.specify/glossary.md
file.009.verdict=reviewed
file.010.path=.specify/memory/exec-quant/records/20261110T082839436644Z-53d14cf3.json
file.010.verdict=skipped
file.010.reason=generated
file.011.path=.specify/memory/exec-quant/records/20261110T082846141283Z-405b4d90.json
file.011.verdict=skipped
file.011.reason=generated
file.012.path=.specify/memory/exec-quant/records/20261110T091915833571Z-15415ec2.json
file.012.verdict=skipped
file.012.reason=generated
file.013.path=.specify/memory/exec-quant/records/20261110T092846104188Z-9c45d0a6.json
file.013.verdict=skipped
file.013.reason=generated
file.014.path=.specify/memory/exec-quant/records/20261110T094505845818Z-0077ef43.json
file.014.verdict=skipped
file.014.reason=generated
file.015.path=.specify/memory/exec-quant/records/20261110T155444460533Z-450cd970.json
file.015.verdict=skipped
file.015.reason=generated
file.016.path=.specify/memory/exec-quant/records/20261110T155444794098Z-76bf4398.json
file.016.verdict=skipped
file.016.reason=generated
file.017.path=.specify/memory/exec-quant/records/20261110T155445130293Z-03d131db.json
file.017.verdict=skipped
file.017.reason=generated
file.018.path=.specify/memory/exec-quant/records/20261110T155445461083Z-9a313aa5.json
file.018.verdict=skipped
file.018.reason=generated
file.019.path=.specify/memory/feedback/20261110T082853Z-speckit-requirements.md
file.019.verdict=reviewed
file.020.path=.specify/memory/feedback/20261110T082855Z-skill-create-requirements.md
file.020.verdict=reviewed
file.021.path=.specify/memory/feedback/20261110T091920Z-speckit-tasks.md
file.021.verdict=reviewed
file.022.path=.specify/memory/feedback/20261110T092854Z-speckit-checklist.md
file.022.verdict=reviewed
file.023.path=.specify/memory/feedback/20261110T094516Z-skill-analyze-artifacts.md
file.023.verdict=reviewed
file.024.path=.specify/memory/feedback/20261110T155453Z-skill-code-review.md
file.024.verdict=reviewed
file.025.path=.specify/memory/feedback/20261110T155453Z-skill-review-feature-quality.md
file.025.verdict=reviewed
file.026.path=.specify/memory/feedback/20261110T155453Z-skill-review-sdd-process.md
file.026.verdict=reviewed
file.027.path=.specify/memory/feedback/20261110T155453Z-speckit-review.md
file.027.verdict=reviewed
file.028.path=.specify/memory/retention/closeout/20261110T083120Z-r20261110T081104Z-b097.json
file.028.verdict=skipped
file.028.reason=generated
file.029.path=.specify/memory/retention/closeout/20261110T091952Z-r20261110T081104Z-b097.json
file.029.verdict=skipped
file.029.reason=generated
file.030.path=.specify/memory/retention/closeout/20261110T092942Z-r20261110T081104Z-b097.json
file.030.verdict=skipped
file.030.reason=generated
file.031.path=.specify/memory/retention/closeout/20261110T094542Z-r20261110T081104Z-b097.json
file.031.verdict=skipped
file.031.reason=generated
file.032.path=.specify/memory/retention/closeout/20261110T155531Z-r20261110T081104Z-b097.json
file.032.verdict=skipped
file.032.reason=generated
file.033.path=.specify/memory/session/20261106T080226Z-run-determination-speckit-review-r20261106t040353z-087a.md
file.033.verdict=skipped
file.033.reason=generated
file.034.path=.specify/memory/session/20261106T105438Z-run-determination-skill-code-review-r20261106t105429z-087rev.md
file.034.verdict=skipped
file.034.reason=generated
file.035.path=.specify/memory/session/20261109T003341Z-run-determination-speckit-review-r20261108t220214z-8647.md
file.035.verdict=skipped
file.035.reason=generated
file.036.path=.specify/memory/session/20261109T053527Z-run-determination-skill-review-feature-quality-r20261109t023.md
file.036.verdict=skipped
file.036.reason=generated
file.037.path=.specify/memory/session/20261109T053545Z-run-determination-skill-review-sdd-process-r20261109t023000z.md
file.037.verdict=skipped
file.037.reason=generated
file.038.path=.specify/memory/session/20261109T080217Z-run-determination-skill-analyze-artifacts-r20261109t064500z.md
file.038.verdict=skipped
file.038.reason=generated
file.039.path=.specify/memory/session/20261110T082837Z-run-determination-speckit-requirements-r20261110t081104z-b09.md
file.039.verdict=skipped
file.039.reason=generated
file.040.path=.specify/memory/session/20261110T082845Z-run-determination-skill-create-requirements-r20261110t081104.md
file.040.verdict=skipped
file.040.reason=generated
file.041.path=.specify/memory/session/20261110T091913Z-run-determination-speckit-tasks-r20261110t081104z-b097.md
file.041.verdict=skipped
file.041.reason=generated
file.042.path=.specify/memory/session/20261110T092821Z-run-determination-speckit-checklist-r20261110t081104z-b097.md
file.042.verdict=skipped
file.042.reason=generated
file.043.path=.specify/memory/session/20261110T094500Z-run-determination-skill-analyze-artifacts-r20261110t081104z.md
file.043.verdict=skipped
file.043.reason=generated
file.044.path=.specify/memory/session/20261110T155439Z-run-determination-skill-code-review-r20261110t081104z-b097.md
file.044.verdict=skipped
file.044.reason=generated
file.045.path=.specify/memory/session/20261110T155439Z-run-determination-skill-review-feature-quality-r20261110t081.md
file.045.verdict=skipped
file.045.reason=generated
file.046.path=.specify/memory/session/20261110T155439Z-run-determination-skill-review-sdd-process-r20261110t081104z.md
file.046.verdict=skipped
file.046.reason=generated
file.047.path=.specify/memory/session/20261110T155439Z-run-determination-speckit-review-r20261110t081104z-b097.md
file.047.verdict=skipped
file.047.reason=generated
file.048.path=.specify/shared/definitions/flow-class-definitions.md
file.048.verdict=reviewed
file.049.path=.specify/shared/definitions/framework-map.md
file.049.verdict=reviewed
file.050.path=.specify/shared/guidelines/better-harness.md
file.050.verdict=reviewed
file.051.path=.specify/skills/internal/sanitize-materials/SKILL.md
file.051.verdict=reviewed
file.052.path=.specify/specs/027-feedback-mechanism/contracts/command-classification.md
file.052.verdict=reviewed
file.053.path=.specify/specs/097-speckit-migrate-command/baseline-failed.txt
file.053.verdict=skipped
file.053.reason=generated
file.054.path=.specify/specs/097-speckit-migrate-command/checklists/requirements-quality-2026-11-10.md
file.054.verdict=reviewed
file.055.path=.specify/specs/097-speckit-migrate-command/checklists/requirements.md
file.055.verdict=reviewed
file.056.path=.specify/specs/097-speckit-migrate-command/checkpoints/03-plan.md
file.056.verdict=reviewed
file.057.path=.specify/specs/097-speckit-migrate-command/code-review.md
file.057.verdict=reviewed
file.058.path=.specify/specs/097-speckit-migrate-command/contracts/migrate-cli.md
file.058.verdict=reviewed
file.059.path=.specify/specs/097-speckit-migrate-command/contracts/migrate-engine.md
file.059.verdict=reviewed
file.060.path=.specify/specs/097-speckit-migrate-command/contracts/migrate-template.md
file.060.verdict=reviewed
file.061.path=.specify/specs/097-speckit-migrate-command/coverage-baseline.txt
file.061.verdict=skipped
file.061.reason=generated
file.062.path=.specify/specs/097-speckit-migrate-command/data-model.md
file.062.verdict=reviewed
file.063.path=.specify/specs/097-speckit-migrate-command/feature-ref.md
file.063.verdict=reviewed
file.064.path=.specify/specs/097-speckit-migrate-command/notes/pre-change-measurements.md
file.064.verdict=reviewed
file.065.path=.specify/specs/097-speckit-migrate-command/notes/quickstart-run.md
file.065.verdict=reviewed
file.066.path=.specify/specs/097-speckit-migrate-command/notes/red-first-evidence.md
file.066.verdict=reviewed
file.067.path=.specify/specs/097-speckit-migrate-command/plan.md
file.067.verdict=reviewed
file.068.path=.specify/specs/097-speckit-migrate-command/quickstart.md
file.068.verdict=reviewed
file.069.path=.specify/specs/097-speckit-migrate-command/requirements.md
file.069.verdict=reviewed
file.070.path=.specify/specs/097-speckit-migrate-command/research.md
file.070.verdict=reviewed
file.071.path=.specify/specs/097-speckit-migrate-command/review.md
file.071.verdict=reviewed
file.072.path=.specify/specs/097-speckit-migrate-command/tasks.md
file.072.verdict=reviewed
file.073.path=.specify/specs/097-speckit-migrate-command/test-evidence/analyze-findings-W1.md
file.073.verdict=reviewed
file.074.path=.specify/specs/097-speckit-migrate-command/test-evidence/analyze-findings-W2.md
file.074.verdict=reviewed
file.075.path=.specify/specs/097-speckit-migrate-command/test-evidence/analyze-findings-W3.md
file.075.verdict=reviewed
file.076.path=.specify/specs/097-speckit-migrate-command/test-evidence/analyze-findings-round2-W1.md
file.076.verdict=reviewed
file.077.path=.specify/specs/097-speckit-migrate-command/test-evidence/analyze-findings-round2-W2.md
file.077.verdict=reviewed
file.078.path=.specify/specs/097-speckit-migrate-command/test-evidence/analyze-findings-round2-W3.md
file.078.verdict=reviewed
file.079.path=.specify/specs/097-speckit-migrate-command/test-evidence/analyze-gates-r3-2026-11-10.txt
file.079.verdict=skipped
file.079.reason=generated
file.080.path=.specify/specs/097-speckit-migrate-command/test-evidence/analyze-merged-2026-11-10.md
file.080.verdict=reviewed
file.081.path=.specify/specs/097-speckit-migrate-command/test-evidence/analyze-merged-r3-2026-11-10.md
file.081.verdict=reviewed
file.082.path=.specify/specs/097-speckit-migrate-command/test-evidence/analyze-merged-round2-2026-11-10.md
file.082.verdict=reviewed
file.083.path=.specify/specs/097-speckit-migrate-command/test-evidence/analyze-repair-dispositions-2026-11-10.md
file.083.verdict=reviewed
file.084.path=.specify/specs/097-speckit-migrate-command/test-evidence/analyze-repair-dispositions-r3-2026-11-10.md
file.084.verdict=reviewed
file.085.path=.specify/specs/097-speckit-migrate-command/test-evidence/analyze-repair-gates-2026-11-10.txt
file.085.verdict=skipped
file.085.reason=generated
file.086.path=.specify/specs/097-speckit-migrate-command/test-evidence/analyze-repair-gates-r3-2026-11-10.txt
file.086.verdict=skipped
file.086.reason=generated
file.087.path=.specify/specs/097-speckit-migrate-command/test-evidence/checklist-readings-2026-11-10.txt
file.087.verdict=reviewed
file.088.path=.specify/specs/097-speckit-migrate-command/test-evidence/closure-verdict-implemented-2026-11-10.json
file.088.verdict=reviewed
file.089.path=.specify/specs/097-speckit-migrate-command/test-evidence/closure-verdict-pre-flip-2026-11-10.json
file.089.verdict=reviewed
file.090.path=.specify/specs/097-speckit-migrate-command/test-evidence/final-suite.txt
file.090.verdict=reviewed
file.091.path=.specify/specs/097-speckit-migrate-command/test-evidence/implement-carrier-repair-2026-11-10.md
file.091.verdict=reviewed
file.092.path=.specify/specs/097-speckit-migrate-command/test-evidence/implement-entry-baseline-suite.txt
file.092.verdict=skipped
file.092.reason=generated
file.093.path=.specify/specs/097-speckit-migrate-command/test-evidence/implement-entry-coverage-live.txt
file.093.verdict=skipped
file.093.reason=generated
file.094.path=.specify/specs/097-speckit-migrate-command/test-evidence/implement-env-probe.txt
file.094.verdict=reviewed
file.095.path=.specify/specs/097-speckit-migrate-command/test-evidence/mirror-verify.txt
file.095.verdict=reviewed
file.096.path=.specify/specs/097-speckit-migrate-command/test-evidence/pkg02-baseline-attribution.txt
file.096.verdict=reviewed
file.097.path=.specify/specs/097-speckit-migrate-command/test-evidence/pkg02-c20-post-stage.txt
file.097.verdict=reviewed
file.098.path=.specify/specs/097-speckit-migrate-command/test-evidence/pkg02-engine-contract.txt
file.098.verdict=reviewed
file.099.path=.specify/specs/097-speckit-migrate-command/test-evidence/pkg02-foundation-suite.txt
file.099.verdict=reviewed
file.100.path=.specify/specs/097-speckit-migrate-command/test-evidence/pkg02-full-failed.txt
file.100.verdict=skipped
file.100.reason=generated
file.101.path=.specify/specs/097-speckit-migrate-command/test-evidence/pkg02-full-suite.txt
file.101.verdict=skipped
file.101.reason=generated
file.102.path=.specify/specs/097-speckit-migrate-command/test-evidence/pkg02-new-failures.txt
file.102.verdict=reviewed
file.103.path=.specify/specs/097-speckit-migrate-command/test-evidence/pkg02-tasks-validator.txt
file.103.verdict=reviewed
file.104.path=.specify/specs/097-speckit-migrate-command/test-evidence/pkg03-baseline-attribution.txt
file.104.verdict=reviewed
file.105.path=.specify/specs/097-speckit-migrate-command/test-evidence/pkg03-full-failed.txt
file.105.verdict=skipped
file.105.reason=generated
file.106.path=.specify/specs/097-speckit-migrate-command/test-evidence/pkg04-baseline-attribution.txt
file.106.verdict=reviewed
file.107.path=.specify/specs/097-speckit-migrate-command/test-evidence/pkg04-full-failed.txt
file.107.verdict=skipped
file.107.reason=generated
file.108.path=.specify/specs/097-speckit-migrate-command/test-evidence/plan-audit.md
file.108.verdict=reviewed
file.109.path=.specify/specs/097-speckit-migrate-command/test-evidence/plan-gates.txt
file.109.verdict=reviewed
file.110.path=.specify/specs/097-speckit-migrate-command/test-evidence/red-base-probe-guard-2026-11-10.txt
file.110.verdict=reviewed
file.111.path=.specify/specs/097-speckit-migrate-command/test-evidence/requirements-flow-class-lookup.txt
file.111.verdict=reviewed
file.112.path=.specify/specs/097-speckit-migrate-command/test-evidence/requirements-glossary-add.txt
file.112.verdict=reviewed
file.113.path=.specify/specs/097-speckit-migrate-command/test-evidence/requirements-glossary-conflict.txt
file.113.verdict=reviewed
file.114.path=.specify/specs/097-speckit-migrate-command/test-evidence/requirements-validator.txt
file.114.verdict=reviewed
file.115.path=.specify/specs/097-speckit-migrate-command/test-evidence/review-repair-dispositions-r1-2026-11-10.md
file.115.verdict=reviewed
file.116.path=.specify/specs/097-speckit-migrate-command/test-evidence/tasks-validator.txt
file.116.verdict=reviewed
file.117.path=.specify/specs/097-speckit-migrate-command/test-evidence/us1-converge.txt
file.117.verdict=reviewed
file.118.path=.specify/specs/097-speckit-migrate-command/test-evidence/us2-safety.txt
file.118.verdict=reviewed
file.119.path=.specify/specs/097-speckit-migrate-command/test-evidence/us3-crossversion.txt
file.119.verdict=reviewed
file.120.path=.specify/specs/097-speckit-migrate-command/test-evidence/us4-equivalence.txt
file.120.verdict=reviewed
file.121.path=.specify/specs/097-speckit-migrate-command/verification.md
file.121.verdict=reviewed
file.122.path=docs/reference/commands/migrate.md
file.122.verdict=reviewed
file.123.path=shared/definitions/flow-class-definitions.md
file.123.verdict=reviewed
file.124.path=shared/definitions/framework-map.md
file.124.verdict=reviewed
file.125.path=shared/guidelines/better-harness.md
file.125.verdict=reviewed
file.126.path=skills/internal/sanitize-materials/SKILL.md
file.126.verdict=reviewed
file.127.path=src/specify_cli/__init__.py
file.127.verdict=reviewed
file.128.path=templates/commands/migrate.md
file.128.verdict=reviewed
file.129.path=tests/contract/test_delegation_classes.py
file.129.verdict=reviewed
file.130.path=tests/contract/test_expression_compatibility.py
file.130.verdict=reviewed
file.131.path=tests/contract/test_expression_gate_wiring.py
file.131.verdict=reviewed
file.132.path=tests/contract/test_fast_fail_discipline.py
file.132.verdict=reviewed
file.133.path=tests/contract/test_feedback_command_classification.py
file.133.verdict=reviewed
file.134.path=tests/contract/test_flow_class_ledger.py
file.134.verdict=reviewed
file.135.path=tests/contract/test_humanize_command_surface.py
file.135.verdict=reviewed
file.136.path=tests/contract/test_migrate_cli_surface.py
file.136.verdict=reviewed
file.137.path=tests/contract/test_migrate_distribution_assembly.py
file.137.verdict=reviewed
file.138.path=tests/contract/test_migrate_engine_contract.py
file.138.verdict=reviewed
file.139.path=tests/contract/test_migrate_template.py
file.139.verdict=reviewed
file.140.path=tests/contract/test_migration_distribution.py
file.140.verdict=reviewed
file.141.path=tests/fixtures/migrate-097/builders.py
file.141.verdict=reviewed
file.142.path=tests/integration/test_migrate_us1_converge.py
file.142.verdict=reviewed
file.143.path=tests/integration/test_migrate_us2_safety.py
file.143.verdict=reviewed
file.144.path=tests/integration/test_migrate_us3_crossversion.py
file.144.verdict=reviewed
file.145.path=tests/integration/test_migrate_us4_equivalence.py
file.145.verdict=reviewed
file.146.path=tests/unit/test_migrate_planner.py
file.146.verdict=reviewed
file.147.path=tests/unit/test_migrate_receipts.py
file.147.verdict=reviewed
<!-- coverage-receipt:end -->
