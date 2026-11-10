# Code Review Report — 代码段 (code segment)

| 属性 | 值 |
|------|-----|
| **分支** | `097-speckit-migrate-command` |
| **基准** | `b3da3a26dfba209057f65c2b17962b9516812c39` (`b3da3a26d`) |
| **目标** | `3195519e28401fbb14def6d25cf17e4133311142` (`3195519e2`) |
| **基准来源** | `feature-first-commit` |
| **渲染模式** | `renderer: text` |
| **Reviewer** | `Qiming Liu (John)` |
| **日期** | `2026-11-10T15:36:54Z` |

## 变更概览

```
 .claude/commands/speckit.migrate.md                |   53 +
 .github/prompts/speckit.migrate.prompt.md          |   53 +
 .gitignore                                         |    1 +
 .opencode/command/speckit.migrate.md               |   53 +
 .qoder/commands/speckit.migrate.md                 |   56 +
 .specify/constitution.md                           |   16 +-
 .specify/features.md                               |    4 +-
 .../024-specification-workspace-versioning.md      |   30 +-
 .specify/glossary.md                               |    1 +
 .../records/20261110T082839436644Z-53d14cf3.json   |    1 +
 .../records/20261110T082846141283Z-405b4d90.json   |    1 +
 .../records/20261110T091915833571Z-15415ec2.json   |    1 +
 .../records/20261110T092846104188Z-9c45d0a6.json   |    1 +
 .../records/20261110T094505845818Z-0077ef43.json   |    1 +
 .../20261110T082853Z-speckit-requirements.md       |   19 +
 .../20261110T082855Z-skill-create-requirements.md  |   19 +
 .../feedback/20261110T091920Z-speckit-tasks.md     |   19 +
 .../feedback/20261110T092854Z-speckit-checklist.md |   19 +
 .../20261110T094516Z-skill-analyze-artifacts.md    |   21 +
 .../20261110T083120Z-r20261110T081104Z-b097.json   |   38 +
 .../20261110T091952Z-r20261110T081104Z-b097.json   |   24 +
 .../20261110T092942Z-r20261110T081104Z-b097.json   |   24 +
 .../20261110T094542Z-r20261110T081104Z-b097.json   |   29 +
 ...on-skill-analyze-artifacts-r20261109t064500z.md |   10 +-
 ...n-speckit-requirements-r20261110t081104z-b09.md |  200 +
 ...n-skill-create-requirements-r20261110t081104.md |  200 +
 ...ination-speckit-tasks-r20261110t081104z-b097.md |  200 +
 ...ion-speckit-checklist-r20261110t081104z-b097.md |  200 +
 ...on-skill-analyze-artifacts-r20261110t081104z.md |  202 +
 .../shared/definitions/flow-class-definitions.md   |    1 +
 .specify/shared/definitions/framework-map.md       |    3 +-
 .specify/shared/guidelines/better-harness.md       |    4 +-
 .../skills/internal/sanitize-materials/SKILL.md    |   20 +-
 .../contracts/command-classification.md            |    6 +-
 .../baseline-failed.txt                            |  278 +
 .../checklists/requirements-quality-2026-11-10.md  |   80 +
 .../checklists/requirements.md                     |   39 +
 .../checkpoints/03-plan.md                         |   11 +
 .../contracts/migrate-cli.md                       |   87 +
 .../contracts/migrate-engine.md                    |   90 +
 .../contracts/migrate-template.md                  |   59 +
 .../coverage-baseline.txt                          |  642 ++
 .../097-speckit-migrate-command/data-model.md      |  143 +
 .../097-speckit-migrate-command/feature-ref.md     |   53 +
 .../notes/pre-change-measurements.md               |   83 +
 .../notes/quickstart-run.md                        |  300 +
 .../notes/red-first-evidence.md                    |  228 +
 .specify/specs/097-speckit-migrate-command/plan.md |  202 +
 .../097-speckit-migrate-command/quickstart.md      |   84 +
 .../097-speckit-migrate-command/requirements.md    |  236 +
 .../specs/097-speckit-migrate-command/research.md  |  101 +
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
 .../test-evidence/final-suite.txt                  |   69 +
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
 .../requirements-flow-class-lookup.txt             |    7 +
 .../test-evidence/requirements-glossary-add.txt    |    5 +
 .../requirements-glossary-conflict.txt             |    5 +
 .../test-evidence/requirements-validator.txt       |   10 +
 .../test-evidence/tasks-validator.txt              |   22 +
 .../test-evidence/us1-converge.txt                 |   52 +
 .../test-evidence/us2-safety.txt                   |   68 +
 .../test-evidence/us3-crossversion.txt             |   68 +
 .../test-evidence/us4-equivalence.txt              |   86 +
 .../097-speckit-migrate-command/verification.md    |  165 +
 docs/reference/commands/migrate.md                 |   59 +
 shared/definitions/flow-class-definitions.md       |    1 +
 shared/definitions/framework-map.md                |    3 +-
 shared/guidelines/better-harness.md                |    4 +-
 skills/internal/sanitize-materials/SKILL.md        |   20 +-
 src/specify_cli/__init__.py                        | 2439 ++++-
 templates/commands/migrate.md                      |   57 +
 tests/contract/test_delegation_classes.py          |    6 +-
 tests/contract/test_expression_compatibility.py    |    3 +
 tests/contract/test_expression_gate_wiring.py      |    4 +-
 tests/contract/test_fast_fail_discipline.py        |    5 +-
 .../test_feedback_command_classification.py        |    6 +-
 tests/contract/test_flow_class_ledger.py           |   25 +-
 tests/contract/test_humanize_command_surface.py    |   13 +-
 tests/contract/test_migrate_cli_surface.py         |  200 +
 .../contract/test_migrate_distribution_assembly.py |  163 +
 tests/contract/test_migrate_engine_contract.py     |  265 +
 tests/contract/test_migrate_template.py            |  202 +
 tests/contract/test_migration_distribution.py      |    8 +-
 tests/fixtures/migrate-097/builders.py             |  236 +
 tests/integration/test_migrate_us1_converge.py     |  342 +
 tests/integration/test_migrate_us2_safety.py       |  618 ++
 tests/integration/test_migrate_us3_crossversion.py |  508 ++
 tests/integration/test_migrate_us4_equivalence.py  |  280 +
 tests/unit/test_migrate_planner.py                 |  325 +
 tests/unit/test_migrate_receipts.py                |  153 +
 123 files changed, 34244 insertions(+), 306 deletions(-)
```

---

## Review 意见


### 🔴 [BLOCKING] tests/integration/test_migrate_us2_safety.py (Line 273)

> test_symlink_support_probe_is_zero_write cannot fail: migrate_symlink_supported() takes no workspace and probes tempfile.gettempdir(), so _tree_digest(workspace) can never move, and isinstance(verdict, bool) is trivially true. The FR-006/C-7 'probe is zero-write' claim has a fake guard. Fix: make the probe observable (e.g. monkeypatch tempfile.TemporaryDirectory to a sentinel path and assert the probe's link target lives there, or add a workspace-scoped probe wrapper) and assert that a deliberately workspace-writing probe variant turns this test red.

<sub>23:51:33</sub>


### 🟠 [IMPORTANT] tests/contract/test_migrate_cli_surface.py (Line 81)

> The C-6 zero-side-effect limb of test_help_exits_zero_declares_outcomes_and_has_zero_side_effects is unfailable: the command is invoked without --workspace and CliRunner does not chdir, so workspace.iterdir() inspects a directory the command cannot reach. A future --help that writes into cwd would pass. Fix: monkeypatch.chdir(workspace) before _invoke, or pass --workspace workspace, then snapshot that same directory.

<sub>23:51:33</sub>


### 🟠 [IMPORTANT] .specify/specs/097-speckit-migrate-command/contracts/migrate-cli.md (Line 19)

> C-1 declares '--help / -h' accepted, but the Typer surface registers only --help: 'specify migrate -h' exits 2 with "No such option '-h'" (verified 2026-11-10). docs/reference/commands/migrate.md:25 repeats the claim. Fix one side: change the contract row and docs to --help, or register help_option_names=['-h','--help']; then re-run the cli-surface contract. Related: templates/commands/migrate.md:24 points at '--help' for the JSON envelope keys, which --help does not list; point at contract C-4 or the docs page instead.

<sub>23:51:33</sub>


### 🟢 [SUGGESTION] tests/integration/test_migrate_us2_safety.py (Line 247)

> The 'pointer is not restated' assertion scans the same file that defines MIGRATE_DESTRUCTIVE_CRITERIA_POINTER, so it is trivially true whenever the equality assertion above it passes. Assert instead that the owner file .specify/shared/guidelines/confirmation-gates.md exists, or that the migrate segment carries no destructive-list literal.

<sub>23:51:33</sub>


### 🟢 [SUGGESTION] tests/integration/test_migrate_us2_safety.py (Line 513)

> Mutation 1 wraps the whole _assert_noninteractive_blocked helper in pytest.raises(AssertionError); the helper's first statement (_json_payload(result, 3)) would also fire on a crash or a different failure, so the red-ability proof can be green for the wrong reason. Same shape at :554, :593 and tests/integration/test_migrate_us3_crossversion.py:505. Narrow each wrapper to the specific assertion (or assert the failure message).

<sub>23:51:33</sub>


### 🟢 [SUGGESTION] tests/integration/test_migrate_us2_safety.py (Line 604)

> Mutation 4 exercises only test-local helpers (_user_content_exists / _assert_user_content_intact) and never calls the engine, so it proves the check helper's power, not the product's. verification.md:87 presents it as one of four product mutations ('four in-suite mutations ... each turn the corresponding assertion red'). Either relocate it as an explicit check-power drill and reword the verification note, or add a product-level weakening mutation.

<sub>23:51:33</sub>


### 🟢 [SUGGESTION] tests/contract/test_migrate_engine_contract.py (Line 231)

> Only test_init_and_migrate_share_one_decision_function carries @pytest.mark.contract and the module declares no pytestmark, so the other 12 contract tests are invisible to the documented '-m contract' selection. Add pytestmark = pytest.mark.contract at module level and drop the per-test marker.

<sub>23:51:33</sub>


### 🟢 [SUGGESTION] tests/contract/test_migrate_cli_surface.py (Line 150)

> C-1's closed option set is sampled with four names; an added --quiet/--verbose would pass both this test and the --help presence test. Derive the declared option set from the Typer command params and assert equality with {--dry-run, --apply, --workspace, --format, --help}.

<sub>23:51:33</sub>


### 🟢 [SUGGESTION] tests/contract/test_migrate_template.py (Line 197)

> The T-4 'generic coverage' test is a two-substring existence check on the generic Qoder contract; it does not prove the generic test still globs every copy. Parametrize the copy list from the .qoder/commands directory listing or assert the generic test's glob pattern still resolves the migrate copy.

<sub>23:51:33</sub>


### 🟢 [SUGGESTION] tests/integration/test_migrate_us4_equivalence.py (Line 262)

> The inlining drill's subprocess line hardcodes 'python3'; use sys.executable so the drill runs on the interpreter under test.

<sub>23:51:33</sub>


### 🟢 [SUGGESTION] tests/integration/test_migrate_us3_crossversion.py (Line 301)

> if stamp['commit'] != 'unavailable' silently degrades the 'recorded verbatim' assertion when the fixture runs without git; the claim then collapses to the same default on both sides. Skip with a named reason or pin the fixture's commit value so the assertion always runs.

<sub>23:51:33</sub>


### ⚪ [NITPICK] .gitignore (Line 38)

> The comment 'Constitution VII closure carriers are versioned records, not runtime logs' outlived the negation rule it described; no '!.specify/specs/*/verification.log' remains and git check-ignore still ignores that path. Remove the orphan comment or restore the rule if the carrier ever moves back to .log.

<sub>23:51:33</sub>


### 👍 [PRAISE] src/specify_cli/__init__.py (Line 2731)

> Engine strengths worth preserving: single-table closed domains (dimensions/dispositions/mechanisms), byte-identical deterministic plan payload with volatile fields excluded, exclusive O_EXCL receipt creation, archive-before-write on every replace, resume judged from the old receipt's own archiveTo paths, and the destructured init decision functions keeping one implementation for two entries.

<sub>23:51:33</sub>


> **未提交范围（未评审）**: 4 个未提交路径未计入本次评审对象（.specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt, .specify/specs/097-speckit-migrate-command/checkpoints/01-requirements.md, .specify/specs/097-speckit-migrate-command/checkpoints/02-clarify.md, .specify/specs/097-speckit-migrate-command/test-evidence/analyze-validation-round2-2026-11-10.md）；本回执不对该范围给出任何结论。

<!-- coverage-receipt:begin -->
receipt_version=1
base=b3da3a26dfba209057f65c2b17962b9516812c39
head=3195519e28401fbb14def6d25cf17e4133311142
base_source=feature-first-commit
renderer=text
changed_files=123
judged_files=97
skipped_files=26
gap_files=0
lines_added=34244
lines_deleted=306
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
file.015.path=.specify/memory/feedback/20261110T082853Z-speckit-requirements.md
file.015.verdict=reviewed
file.016.path=.specify/memory/feedback/20261110T082855Z-skill-create-requirements.md
file.016.verdict=reviewed
file.017.path=.specify/memory/feedback/20261110T091920Z-speckit-tasks.md
file.017.verdict=reviewed
file.018.path=.specify/memory/feedback/20261110T092854Z-speckit-checklist.md
file.018.verdict=reviewed
file.019.path=.specify/memory/feedback/20261110T094516Z-skill-analyze-artifacts.md
file.019.verdict=reviewed
file.020.path=.specify/memory/retention/closeout/20261110T083120Z-r20261110T081104Z-b097.json
file.020.verdict=skipped
file.020.reason=generated
file.021.path=.specify/memory/retention/closeout/20261110T091952Z-r20261110T081104Z-b097.json
file.021.verdict=skipped
file.021.reason=generated
file.022.path=.specify/memory/retention/closeout/20261110T092942Z-r20261110T081104Z-b097.json
file.022.verdict=skipped
file.022.reason=generated
file.023.path=.specify/memory/retention/closeout/20261110T094542Z-r20261110T081104Z-b097.json
file.023.verdict=skipped
file.023.reason=generated
file.024.path=.specify/memory/session/20261109T080217Z-run-determination-skill-analyze-artifacts-r20261109t064500z.md
file.024.verdict=skipped
file.024.reason=generated
file.025.path=.specify/memory/session/20261110T082837Z-run-determination-speckit-requirements-r20261110t081104z-b09.md
file.025.verdict=skipped
file.025.reason=generated
file.026.path=.specify/memory/session/20261110T082845Z-run-determination-skill-create-requirements-r20261110t081104.md
file.026.verdict=skipped
file.026.reason=generated
file.027.path=.specify/memory/session/20261110T091913Z-run-determination-speckit-tasks-r20261110t081104z-b097.md
file.027.verdict=skipped
file.027.reason=generated
file.028.path=.specify/memory/session/20261110T092821Z-run-determination-speckit-checklist-r20261110t081104z-b097.md
file.028.verdict=skipped
file.028.reason=generated
file.029.path=.specify/memory/session/20261110T094500Z-run-determination-skill-analyze-artifacts-r20261110t081104z.md
file.029.verdict=skipped
file.029.reason=generated
file.030.path=.specify/shared/definitions/flow-class-definitions.md
file.030.verdict=reviewed
file.031.path=.specify/shared/definitions/framework-map.md
file.031.verdict=reviewed
file.032.path=.specify/shared/guidelines/better-harness.md
file.032.verdict=reviewed
file.033.path=.specify/skills/internal/sanitize-materials/SKILL.md
file.033.verdict=reviewed
file.034.path=.specify/specs/027-feedback-mechanism/contracts/command-classification.md
file.034.verdict=reviewed
file.035.path=.specify/specs/097-speckit-migrate-command/baseline-failed.txt
file.035.verdict=skipped
file.035.reason=generated
file.036.path=.specify/specs/097-speckit-migrate-command/checklists/requirements-quality-2026-11-10.md
file.036.verdict=reviewed
file.037.path=.specify/specs/097-speckit-migrate-command/checklists/requirements.md
file.037.verdict=reviewed
file.038.path=.specify/specs/097-speckit-migrate-command/checkpoints/03-plan.md
file.038.verdict=reviewed
file.039.path=.specify/specs/097-speckit-migrate-command/contracts/migrate-cli.md
file.039.verdict=reviewed
file.040.path=.specify/specs/097-speckit-migrate-command/contracts/migrate-engine.md
file.040.verdict=reviewed
file.041.path=.specify/specs/097-speckit-migrate-command/contracts/migrate-template.md
file.041.verdict=reviewed
file.042.path=.specify/specs/097-speckit-migrate-command/coverage-baseline.txt
file.042.verdict=skipped
file.042.reason=generated
file.043.path=.specify/specs/097-speckit-migrate-command/data-model.md
file.043.verdict=reviewed
file.044.path=.specify/specs/097-speckit-migrate-command/feature-ref.md
file.044.verdict=reviewed
file.045.path=.specify/specs/097-speckit-migrate-command/notes/pre-change-measurements.md
file.045.verdict=reviewed
file.046.path=.specify/specs/097-speckit-migrate-command/notes/quickstart-run.md
file.046.verdict=reviewed
file.047.path=.specify/specs/097-speckit-migrate-command/notes/red-first-evidence.md
file.047.verdict=reviewed
file.048.path=.specify/specs/097-speckit-migrate-command/plan.md
file.048.verdict=reviewed
file.049.path=.specify/specs/097-speckit-migrate-command/quickstart.md
file.049.verdict=reviewed
file.050.path=.specify/specs/097-speckit-migrate-command/requirements.md
file.050.verdict=reviewed
file.051.path=.specify/specs/097-speckit-migrate-command/research.md
file.051.verdict=reviewed
file.052.path=.specify/specs/097-speckit-migrate-command/tasks.md
file.052.verdict=reviewed
file.053.path=.specify/specs/097-speckit-migrate-command/test-evidence/analyze-findings-W1.md
file.053.verdict=reviewed
file.054.path=.specify/specs/097-speckit-migrate-command/test-evidence/analyze-findings-W2.md
file.054.verdict=reviewed
file.055.path=.specify/specs/097-speckit-migrate-command/test-evidence/analyze-findings-W3.md
file.055.verdict=reviewed
file.056.path=.specify/specs/097-speckit-migrate-command/test-evidence/analyze-findings-round2-W1.md
file.056.verdict=reviewed
file.057.path=.specify/specs/097-speckit-migrate-command/test-evidence/analyze-findings-round2-W2.md
file.057.verdict=reviewed
file.058.path=.specify/specs/097-speckit-migrate-command/test-evidence/analyze-findings-round2-W3.md
file.058.verdict=reviewed
file.059.path=.specify/specs/097-speckit-migrate-command/test-evidence/analyze-gates-r3-2026-11-10.txt
file.059.verdict=skipped
file.059.reason=generated
file.060.path=.specify/specs/097-speckit-migrate-command/test-evidence/analyze-merged-2026-11-10.md
file.060.verdict=reviewed
file.061.path=.specify/specs/097-speckit-migrate-command/test-evidence/analyze-merged-r3-2026-11-10.md
file.061.verdict=reviewed
file.062.path=.specify/specs/097-speckit-migrate-command/test-evidence/analyze-merged-round2-2026-11-10.md
file.062.verdict=reviewed
file.063.path=.specify/specs/097-speckit-migrate-command/test-evidence/analyze-repair-dispositions-2026-11-10.md
file.063.verdict=reviewed
file.064.path=.specify/specs/097-speckit-migrate-command/test-evidence/analyze-repair-dispositions-r3-2026-11-10.md
file.064.verdict=reviewed
file.065.path=.specify/specs/097-speckit-migrate-command/test-evidence/analyze-repair-gates-2026-11-10.txt
file.065.verdict=skipped
file.065.reason=generated
file.066.path=.specify/specs/097-speckit-migrate-command/test-evidence/analyze-repair-gates-r3-2026-11-10.txt
file.066.verdict=skipped
file.066.reason=generated
file.067.path=.specify/specs/097-speckit-migrate-command/test-evidence/checklist-readings-2026-11-10.txt
file.067.verdict=reviewed
file.068.path=.specify/specs/097-speckit-migrate-command/test-evidence/final-suite.txt
file.068.verdict=reviewed
file.069.path=.specify/specs/097-speckit-migrate-command/test-evidence/implement-carrier-repair-2026-11-10.md
file.069.verdict=reviewed
file.070.path=.specify/specs/097-speckit-migrate-command/test-evidence/implement-entry-baseline-suite.txt
file.070.verdict=skipped
file.070.reason=generated
file.071.path=.specify/specs/097-speckit-migrate-command/test-evidence/implement-entry-coverage-live.txt
file.071.verdict=skipped
file.071.reason=generated
file.072.path=.specify/specs/097-speckit-migrate-command/test-evidence/implement-env-probe.txt
file.072.verdict=reviewed
file.073.path=.specify/specs/097-speckit-migrate-command/test-evidence/mirror-verify.txt
file.073.verdict=reviewed
file.074.path=.specify/specs/097-speckit-migrate-command/test-evidence/pkg02-baseline-attribution.txt
file.074.verdict=reviewed
file.075.path=.specify/specs/097-speckit-migrate-command/test-evidence/pkg02-c20-post-stage.txt
file.075.verdict=reviewed
file.076.path=.specify/specs/097-speckit-migrate-command/test-evidence/pkg02-engine-contract.txt
file.076.verdict=reviewed
file.077.path=.specify/specs/097-speckit-migrate-command/test-evidence/pkg02-foundation-suite.txt
file.077.verdict=reviewed
file.078.path=.specify/specs/097-speckit-migrate-command/test-evidence/pkg02-full-failed.txt
file.078.verdict=skipped
file.078.reason=generated
file.079.path=.specify/specs/097-speckit-migrate-command/test-evidence/pkg02-full-suite.txt
file.079.verdict=skipped
file.079.reason=generated
file.080.path=.specify/specs/097-speckit-migrate-command/test-evidence/pkg02-new-failures.txt
file.080.verdict=reviewed
file.081.path=.specify/specs/097-speckit-migrate-command/test-evidence/pkg02-tasks-validator.txt
file.081.verdict=reviewed
file.082.path=.specify/specs/097-speckit-migrate-command/test-evidence/pkg03-baseline-attribution.txt
file.082.verdict=reviewed
file.083.path=.specify/specs/097-speckit-migrate-command/test-evidence/pkg03-full-failed.txt
file.083.verdict=skipped
file.083.reason=generated
file.084.path=.specify/specs/097-speckit-migrate-command/test-evidence/pkg04-baseline-attribution.txt
file.084.verdict=reviewed
file.085.path=.specify/specs/097-speckit-migrate-command/test-evidence/pkg04-full-failed.txt
file.085.verdict=skipped
file.085.reason=generated
file.086.path=.specify/specs/097-speckit-migrate-command/test-evidence/plan-audit.md
file.086.verdict=reviewed
file.087.path=.specify/specs/097-speckit-migrate-command/test-evidence/plan-gates.txt
file.087.verdict=reviewed
file.088.path=.specify/specs/097-speckit-migrate-command/test-evidence/requirements-flow-class-lookup.txt
file.088.verdict=reviewed
file.089.path=.specify/specs/097-speckit-migrate-command/test-evidence/requirements-glossary-add.txt
file.089.verdict=reviewed
file.090.path=.specify/specs/097-speckit-migrate-command/test-evidence/requirements-glossary-conflict.txt
file.090.verdict=reviewed
file.091.path=.specify/specs/097-speckit-migrate-command/test-evidence/requirements-validator.txt
file.091.verdict=reviewed
file.092.path=.specify/specs/097-speckit-migrate-command/test-evidence/tasks-validator.txt
file.092.verdict=reviewed
file.093.path=.specify/specs/097-speckit-migrate-command/test-evidence/us1-converge.txt
file.093.verdict=reviewed
file.094.path=.specify/specs/097-speckit-migrate-command/test-evidence/us2-safety.txt
file.094.verdict=reviewed
file.095.path=.specify/specs/097-speckit-migrate-command/test-evidence/us3-crossversion.txt
file.095.verdict=reviewed
file.096.path=.specify/specs/097-speckit-migrate-command/test-evidence/us4-equivalence.txt
file.096.verdict=reviewed
file.097.path=.specify/specs/097-speckit-migrate-command/verification.md
file.097.verdict=reviewed
file.098.path=docs/reference/commands/migrate.md
file.098.verdict=reviewed
file.099.path=shared/definitions/flow-class-definitions.md
file.099.verdict=reviewed
file.100.path=shared/definitions/framework-map.md
file.100.verdict=reviewed
file.101.path=shared/guidelines/better-harness.md
file.101.verdict=reviewed
file.102.path=skills/internal/sanitize-materials/SKILL.md
file.102.verdict=reviewed
file.103.path=src/specify_cli/__init__.py
file.103.verdict=reviewed
file.104.path=templates/commands/migrate.md
file.104.verdict=reviewed
file.105.path=tests/contract/test_delegation_classes.py
file.105.verdict=reviewed
file.106.path=tests/contract/test_expression_compatibility.py
file.106.verdict=reviewed
file.107.path=tests/contract/test_expression_gate_wiring.py
file.107.verdict=reviewed
file.108.path=tests/contract/test_fast_fail_discipline.py
file.108.verdict=reviewed
file.109.path=tests/contract/test_feedback_command_classification.py
file.109.verdict=reviewed
file.110.path=tests/contract/test_flow_class_ledger.py
file.110.verdict=reviewed
file.111.path=tests/contract/test_humanize_command_surface.py
file.111.verdict=reviewed
file.112.path=tests/contract/test_migrate_cli_surface.py
file.112.verdict=reviewed
file.113.path=tests/contract/test_migrate_distribution_assembly.py
file.113.verdict=reviewed
file.114.path=tests/contract/test_migrate_engine_contract.py
file.114.verdict=reviewed
file.115.path=tests/contract/test_migrate_template.py
file.115.verdict=reviewed
file.116.path=tests/contract/test_migration_distribution.py
file.116.verdict=reviewed
file.117.path=tests/fixtures/migrate-097/builders.py
file.117.verdict=reviewed
file.118.path=tests/integration/test_migrate_us1_converge.py
file.118.verdict=reviewed
file.119.path=tests/integration/test_migrate_us2_safety.py
file.119.verdict=reviewed
file.120.path=tests/integration/test_migrate_us3_crossversion.py
file.120.verdict=reviewed
file.121.path=tests/integration/test_migrate_us4_equivalence.py
file.121.verdict=reviewed
file.122.path=tests/unit/test_migrate_planner.py
file.122.verdict=reviewed
file.123.path=tests/unit/test_migrate_receipts.py
file.123.verdict=reviewed
<!-- coverage-receipt:end -->
