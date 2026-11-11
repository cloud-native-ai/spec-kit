# Code Review Report — 代码段 (code segment)

| 属性 | 值 |
|------|-----|
| **分支** | `100-seal-slice-archive` |
| **基准** | `48e273d7395d949656099c596161ac9210687cfa` (`48e273d73`) |
| **目标** | `7aa624e4c8d28f36e0b320f57c558f8f849ab1e8` (`7aa624e4c`) |
| **基准来源** | `feature-first-commit` |
| **渲染模式** | `renderer: text` |
| **Reviewer** | `Qiming Liu (John)` |
| **日期** | `2026-11-11T06:23:20Z` |

## 变更概览

```
 .claude/commands/speckit.seal.md                   |   12 +-
 .github/prompts/speckit.seal.prompt.md             |   12 +-
 .opencode/command/speckit.seal.md                  |   12 +-
 .qoder/commands/speckit.seal.md                    |   14 +-
 .specify/features.md                               |    4 +-
 .specify/features/074-goal-team-sdd-unification.md |   20 +-
 .specify/features/099-speckit-seal.md              |   18 +-
 .../records/20261111T024124389486Z-258bc966.json   |    1 +
 .../records/20261111T025219170277Z-25d4e8df.json   |    1 +
 .../records/20261111T034446399229Z-12f02d26.json   |    1 +
 .../feedback/20261111T024128Z-speckit-tasks.md     |   19 +
 .../feedback/20261111T025219Z-speckit-checklist.md |   21 +
 .../feedback/20261111T034446Z-speckit-analyze.md   |   21 +
 ...0261111T024300Z-r20261111T024200Z-b100-tasks.md |   43 +
 ...111T025239Z-r20261111T025146Z-b100-checklist.md |   43 +
 ...n-speckit-tasks-r20261111t024200z-b100-tasks.md |  200 +
 ...n-speckit-checklist-r20261111t025146z-b100-c.md |  204 +
 ...n-speckit-analyze-r20261111t034400z-b100-ana.md |  202 +
 .specify/register.md                               |   18 +-
 .specify/scripts/python/seal-utils.py              | 1699 ++++-
 .specify/shared/definitions/framework-map.md       |    2 +-
 .../definitions/non-disposable-definitions.md      |   16 +-
 .../shared/definitions/sdd-routing-definitions.md  |    2 +-
 .../skills/internal/analyze-artifacts/SKILL.md     |    7 +
 .specify/skills/internal/seal-artifact/SKILL.md    |   61 +-
 .../archive-manifest.json                          | 8057 ++++++++++++++++++++
 .../074-goal-team-sdd-unification/code-review.md   |    4 +-
 .../contracts/bootstrap-and-maintenance.md         |    2 +-
 .../contracts/compat-and-safety.md                 |    2 +-
 .../contracts/diffusion.md                         |    2 +-
 .../contracts/hierarchy-and-authorization.md       |    2 +-
 .../contracts/routing-decision.md                  |    2 +-
 .../merge-manifest.json                            |  250 +-
 .../specs/074-goal-team-sdd-unification/plan.md    |   12 +-
 .../074-goal-team-sdd-unification/research.md      |   12 +-
 .../specs/074-goal-team-sdd-unification/review.md  |    4 +-
 .../074a-authorized-routing/baseline-failed.txt    |    0
 .../checklists/readiness-2026-10-29.md             |    0
 .../recheck-2026-10-29-implement-start.md          |    0
 .../checklists/requirements.md                     |    0
 .../slices}/074a-authorized-routing/code-review.md |    0
 .../contracts/bootstrap-and-maintenance.md         |    0
 .../contracts/hierarchy-and-authorization.md       |    0
 .../contracts/nested-invocation.md                 |    0
 .../contracts/routing-decision.md                  |    0
 .../074a-authorized-routing/coverage-baseline.txt  |    0
 .../slices}/074a-authorized-routing/data-model.md  |    0
 .../slices}/074a-authorized-routing/feature-ref.md |    0
 .../074a-authorized-routing/final-failed-2.txt     |    0
 .../074a-authorized-routing/final-failed-3.txt     |    0
 .../074a-authorized-routing/final-failed.txt       |    0
 .../notes/closure-full-run-2.txt                   |    0
 .../notes/closure-full-run-3.txt                   |    0
 .../notes/closure-full-run.txt                     |    0
 .../notes/full-baseline-run.txt                    |    0
 .../074a-authorized-routing/notes/golden-rows.txt  |    0
 .../074a-authorized-routing/notes/golden-run1.json |    0
 .../074a-authorized-routing/notes/golden-run2.json |    0
 .../notes/green-t016-demo.txt                      |    0
 .../074a-authorized-routing/notes/green-t016.txt   |    0
 .../074a-authorized-routing/notes/green-t017.txt   |    0
 .../074a-authorized-routing/notes/green-t021.txt   |    0
 .../notes/green-t025-targeted.txt                  |    0
 .../074a-authorized-routing/notes/green-t025.txt   |    0
 .../074a-authorized-routing/notes/part5-failed.txt |    0
 .../notes/part5-regression.txt                     |    0
 .../notes/pre-change-measurements.md               |    0
 .../notes/quickstart-run.md                        |    0
 .../notes/red-first-evidence.md                    |    0
 .../074a-authorized-routing/notes/red-t005.txt     |    0
 .../074a-authorized-routing/notes/red-t007.txt     |    0
 .../074a-authorized-routing/notes/red-t012.txt     |    0
 .../074a-authorized-routing/notes/red-t018.txt     |    0
 .../074a-authorized-routing/notes/red-t022.txt     |    0
 .../notes/targeted-set-v1-failed.txt               |    0
 .../slices}/074a-authorized-routing/plan.md        |    0
 .../slices}/074a-authorized-routing/quickstart.md  |    0
 .../074a-authorized-routing/requirements.md        |    0
 .../slices}/074a-authorized-routing/research.md    |    0
 .../slices}/074a-authorized-routing/review.md      |    0
 .../slices}/074a-authorized-routing/tasks.md       |    0
 .../test-evidence/analyze-fix-checks.md            |    0
 .../test-evidence/analyze.jsonl                    |    0
 .../test-evidence/checklist-stage-checks.md        |    0
 .../test-evidence/checklist.jsonl                  |    0
 .../test-evidence/clarify.jsonl                    |    0
 .../test-evidence/implement.jsonl                  |    0
 .../test-evidence/plan-stage-checks.md             |    0
 .../test-evidence/plan.jsonl                       |    0
 .../test-evidence/review.jsonl                     |    0
 .../test-evidence/targeted-set-v1-baseline.txt     |    0
 .../test-evidence/tasks-stage-checks.md            |    0
 .../test-evidence/tasks.jsonl                      |    0
 .../074a-authorized-routing/verification.md        |    0
 .../074b-nested-governance/baseline-failed.txt     |    0
 .../checklists/readiness-2026-10-29.md             |    0
 .../checklists/requirements.md                     |    0
 .../slices}/074b-nested-governance/code-review.md  |    0
 .../contracts/compat-and-safety.md                 |    0
 .../074b-nested-governance/contracts/diffusion.md  |    0
 .../contracts/report-and-attribution.md            |    0
 .../074b-nested-governance/coverage-baseline.txt   |    0
 .../slices}/074b-nested-governance/data-model.md   |    0
 .../slices}/074b-nested-governance/feature-ref.md  |    0
 .../074b-nested-governance/final-failed-2.txt      |    0
 .../074b-nested-governance/final-failed.txt        |    0
 .../notes/closure-full-run-2.txt                   |    0
 .../notes/closure-full-run.txt                     |    0
 .../notes/pre-change-file-sets.txt                 |    0
 .../notes/pre-change-measurements.md               |    0
 .../074b-nested-governance/notes/quickstart-run.md |    0
 .../notes/red-first-evidence.md                    |    0
 .../slices}/074b-nested-governance/plan.md         |    0
 .../slices}/074b-nested-governance/quickstart.md   |    0
 .../slices}/074b-nested-governance/requirements.md |    0
 .../slices}/074b-nested-governance/research.md     |    0
 .../slices}/074b-nested-governance/review.md       |    0
 .../slices}/074b-nested-governance/tasks.md        |    0
 .../test-evidence/analyze-fix-checks.md            |    0
 .../test-evidence/analyze.jsonl                    |    0
 .../test-evidence/checklist-stage-checks.md        |    0
 .../test-evidence/checklist.jsonl                  |    0
 .../test-evidence/clarify.jsonl                    |    0
 .../test-evidence/compat-baseline-nodeids.txt      |    0
 .../containment-post-change-collect.txt            |    0
 .../test-evidence/containment-post-change-run.txt  |    0
 .../test-evidence/implement-baseline-run.txt       |    0
 .../implement-targeted-part1-failed.txt            |    0
 .../test-evidence/implement-targeted-part1-run.txt |    0
 .../implement-targeted-part1-supp-failed.txt       |    0
 .../implement-targeted-part1-supp-run.txt          |    0
 .../implement-targeted-part2-failed.txt            |    0
 .../test-evidence/implement-targeted-part2-run.txt |    0
 .../implement-targeted-part2-supp-failed.txt       |    0
 .../implement-targeted-part2-supp-run.txt          |    0
 .../implement-targeted-part3-failed.txt            |    0
 .../test-evidence/implement-targeted-part3-run.txt |    0
 .../implement-targeted-part4-failed.txt            |    0
 .../test-evidence/implement-targeted-part4-run.txt |    0
 .../test-evidence/implement.jsonl                  |    0
 .../test-evidence/plan-stage-checks.md             |    0
 .../test-evidence/plan.jsonl                       |    0
 .../test-evidence/requirements-checks.txt          |    0
 .../test-evidence/review.jsonl                     |    0
 .../test-evidence/targeted-set-v1-baseline.txt     |    0
 .../test-evidence/tasks-stage-checks.md            |    0
 .../test-evidence/tasks.jsonl                      |    0
 .../slices}/074b-nested-governance/verification.md |    0
 .../specs/074-goal-team-sdd-unification/tasks.md   |  138 +-
 .../074-goal-team-sdd-unification/verification.md  |   32 +-
 .../contracts/merge-back.contract.md               |   12 +-
 .../contracts/records-and-boundaries.contract.md   |   11 +-
 .../contracts/seal-engine.contract.md              |   17 +-
 .../checklists/2026-11-11-requirements-quality.md  |   67 +
 .../checklists/requirements.md                     |   45 +
 .../specs/100-seal-slice-archive/code-review.md    | 1470 ++++
 .../contracts/archive-actions.contract.md          |  113 +
 .../contracts/archive-manifest.contract.md         |   95 +
 .../contracts/reference-classification.contract.md |   97 +
 .../100-seal-slice-archive/coverage-baseline.txt   |  675 ++
 .../specs/100-seal-slice-archive/data-model.md     |  158 +
 .../specs/100-seal-slice-archive/feature-ref.md    |  124 +
 .../notes/pre-change-measurements.md               |  130 +
 .../100-seal-slice-archive/notes/quickstart-run.md |  196 +
 .../notes/red-first-evidence.md                    |  556 ++
 .../notes/requirements-research.md                 |  105 +
 .specify/specs/100-seal-slice-archive/plan.md      |  275 +
 .../specs/100-seal-slice-archive/quickstart.md     |  169 +
 .../specs/100-seal-slice-archive/requirements.md   |  231 +
 .specify/specs/100-seal-slice-archive/research.md  |  186 +
 .specify/specs/100-seal-slice-archive/review.md    |  350 +
 .specify/specs/100-seal-slice-archive/tasks.md     |  368 +
 .../test-evidence/074-archive-round.txt            | 1026 +++
 .../test-evidence/analyze-coverage-round2.json     |  886 +++
 .../test-evidence/analyze-coverage.json            |  886 +++
 .../test-evidence/analyze-dispositions.md          |  142 +
 .../test-evidence/analyze-findings.jsonl           |   73 +
 .../test-evidence/analyze-gates-round2.txt         |   39 +
 .../test-evidence/analyze-gates.txt                |   41 +
 .../test-evidence/analyze-merged-2026-11-11.md     |  304 +
 .../analyze-precheck-decomp-tensions.txt           |   17 +
 .../test-evidence/analyze-precheck-plan-tasks.txt  |    9 +
 .../test-evidence/analyze-precheck-validators.txt  |   16 +
 .../test-evidence/checklist-stage-checks.txt       |   11 +
 .../test-evidence/clarify-gates.txt                |   47 +
 .../test-evidence/closure-verdict-100.json         |   38 +
 .../test-evidence/coverage-final.txt               |  725 ++
 .../test-evidence/decomposition-plan.txt           |    1 +
 .../test-evidence/decomposition-tasks.json         |   12 +
 .../test-evidence/final-failed.txt                 |  207 +
 .../test-evidence/final-mirrors.txt                |   37 +
 .../test-evidence/final-suite.txt                  |   63 +
 .../test-evidence/flow-class-lookup.txt            |    7 +
 .../test-evidence/foundational-checks.txt          |  224 +
 .../test-evidence/p2-discovery.txt                 |  242 +
 .../test-evidence/p3-fixtures.txt                  |  105 +
 .../test-evidence/p3-green.txt                     |   22 +
 .../test-evidence/p3-red-first.txt                 | 1425 ++++
 .../test-evidence/p3-regression.txt                |   89 +
 .../test-evidence/p4-green.txt                     |    7 +
 .../test-evidence/p4-red-first.txt                 |  273 +
 .../test-evidence/p4-regression.txt                |  146 +
 .../test-evidence/p5-owner-revision.txt            |   76 +
 .../test-evidence/p6-command-surface.txt           |   95 +
 .../test-evidence/plan-stage-checks.txt            |  158 +
 .../test-evidence/pre-analyze-requirements.txt     |    2 +
 .../test-evidence/requirements-measurements.txt    |   40 +
 .../review-repair-dispositions-r1-2026-11-11.md    |   48 +
 .../test-evidence/review-repair-r1-red-first.txt   |   35 +
 .../test-evidence/review-repair-r1-suite.txt       |   68 +
 .../test-evidence/sc-trace.txt                     |   24 +
 .../test-evidence/structure-audit.txt              |   29 +
 .../test-evidence/tasks-stage-checks.txt           |  100 +
 .../test-evidence/us1-checkpoint.txt               |   22 +
 .../test-evidence/us2-checkpoint.txt               |   58 +
 .../test-evidence/us3-checkpoint.txt               |   46 +
 .../test-evidence/us4-checkpoint.txt               |  203 +
 .../test-evidence/validate-requirements.txt        |   10 +
 .../test-evidence/validate-tasks-final.txt         |   14 +
 .../specs/100-seal-slice-archive/verification.md   |   65 +
 docs/reference/commands/seal.md                    |  113 +-
 scripts/python/seal-utils.py                       | 1699 ++++-
 shared/definitions/framework-map.md                |    2 +-
 shared/definitions/non-disposable-definitions.md   |   16 +-
 shared/definitions/sdd-routing-definitions.md      |    2 +-
 skills/internal/analyze-artifacts/SKILL.md         |    7 +
 skills/internal/seal-artifact/SKILL.md             |   61 +-
 templates/commands/seal.md                         |   20 +-
 tests/contract/test_sdd_compat_containment.py      |    2 +-
 tests/contract/test_sdd_diffusion.py               |    2 +-
 tests/contract/test_seal_archive_apply.py          |  513 ++
 tests/contract/test_seal_archive_manifest.py       |  328 +
 tests/contract/test_seal_archive_plan.py           |  553 ++
 tests/contract/test_seal_boundaries.py             |  400 +-
 tests/contract/test_seal_engine_contract.py        |  109 +-
 tests/contract/test_seal_merge_apply.py            |  105 +
 tests/contract/test_seal_merge_plan.py             |  103 +
 tests/fixtures/nested_sdd.py                       |    2 +-
 .../specs/100-fixture-parent/archive-manifest.json |  106 +
 .../specs/100-fixture-parent/merge-manifest.json   |   26 +
 .../specs/100-fixture-parent/requirements.md       |   13 +
 .../slices/100a-fixture-alpha/requirements.md      |   22 +
 .../slices/100a-fixture-alpha/tasks.md             |    4 +
 .../slices/100b-fixture-beta/requirements.md       |   17 +
 .../slices/100b-fixture-beta/tasks.md              |    3 +
 .../.specify/state/100-fixture-parent.md           |    9 +
 .../seal-archive/blocked-pair/.specify/features.md |    5 +
 .../.specify/features/100-fixture-parent.md        |    6 +
 .../specs/100-fixture-parent/code-review.md        |    6 +
 .../specs/100-fixture-parent/merge-manifest.json   |   26 +
 .../specs/100-fixture-parent/requirements.md       |    3 +
 .../.specify/specs/100-fixture-parent/review.md    |   12 +
 .../specs/100a-fixture-alpha/requirements.md       |    8 +
 .../.specify/specs/100a-fixture-alpha/tasks.md     |    3 +
 .../specs/100b-fixture-beta/requirements.md        |    8 +
 .../.specify/specs/100b-fixture-beta/tasks.md      |    3 +
 .../specs/100-fixture-parent/merge-manifest.json   |   26 +
 .../specs/100-fixture-parent/requirements.md       |    3 +
 .../.specify/specs/100-fixture-parent/seal.md      |    4 +
 .../specs/100a-fixture-alpha/requirements.md       |    8 +
 .../.specify/specs/100a-fixture-alpha/tasks.md     |    3 +
 .../specs/100b-fixture-beta/requirements.md        |    8 +
 .../.specify/specs/100b-fixture-beta/tasks.md      |    3 +
 .../.specify/state/100-fixture-parent.md           |    9 +
 .../specs/110-fixture-north/merge-manifest.json    |   18 +
 .../specs/110-fixture-north/requirements.md        |    3 +
 .../specs/110a-fixture-north-slice/requirements.md |    7 +
 .../specs/110a-fixture-north-slice/tasks.md        |    3 +
 .../specs/120-fixture-south/merge-manifest.json    |   18 +
 .../specs/120-fixture-south/requirements.md        |    3 +
 .../specs/120a-fixture-south-slice/requirements.md |    7 +
 .../specs/120a-fixture-south-slice/tasks.md        |    3 +
 .../concurrent/.specify/state/110-fixture-north.md |    8 +
 .../concurrent/.specify/state/120-fixture-south.md |    8 +
 .../specs/100-fixture-empty/merge-manifest.json    |   10 +
 .../specs/100-fixture-empty/requirements.md        |    3 +
 .../specs/100-fixture-parent/merge-manifest.json   |   22 +
 .../specs/100-fixture-parent/requirements.md       |    3 +
 .../slices/100b-fixture-beta/requirements.md       |    8 +
 .../slices/100b-fixture-beta/tasks.md              |    3 +
 .../specs/100a-fixture-alpha/requirements.md       |    8 +
 .../.specify/specs/100a-fixture-alpha/tasks.md     |    3 +
 .../.specify/state/100-fixture-parent.md           |    9 +
 .../.specify/features.md                           |    5 +
 .../.specify/features/100-fixture-parent.md        |   14 +
 .../.specify/glossary.md                           |    3 +
 .../.specify/history/topic.md                      |    3 +
 .../.specify/instructions.md                       |    3 +
 .../.specify/memory/session/entry.md               |    3 +
 .../.specify/register.md                           |    3 +
 .../.specify/shared/definitions/example.md         |    3 +
 .../100-fixture-parent/checklists/checklist.md     |    3 +
 .../100-fixture-parent/contracts/core.contract.md  |    3 +
 .../specs/100-fixture-parent/merge-manifest.json   |   26 +
 .../specs/100-fixture-parent/notes/note.md         |    3 +
 .../.specify/specs/100-fixture-parent/plan.md      |    4 +
 .../specs/100-fixture-parent/requirements.md       |    3 +
 .../.specify/specs/100-fixture-parent/seal.md      |    4 +
 .../.specify/specs/100-fixture-parent/tasks.md     |    3 +
 .../100-fixture-parent/test-evidence/evidence.txt  |    1 +
 .../specs/100-fixture-parent/unsorted/random.md    |    4 +
 .../specs/100-fixture-parent/verification.md       |    3 +
 .../.specify/specs/100a-fixture-alpha/notes.md     |    3 +
 .../.specify/specs/100a-fixture-alpha/plan.md      |    3 +
 .../specs/100a-fixture-alpha/requirements.md       |    8 +
 .../.specify/specs/100a-fixture-alpha/review.md    |    3 +
 .../.specify/specs/100a-fixture-alpha/tasks.md     |    3 +
 .../.specify/specs/100b-fixture-beta/notes.md      |    3 +
 .../specs/100b-fixture-beta/requirements.md        |    8 +
 .../.specify/specs/100b-fixture-beta/tasks.md      |    3 +
 .../.specify/state/100-fixture-parent.md           |    9 +
 .../shared/definitions/example.md                  |    3 +
 .../tests/contract/fixture_refs.py                 |    5 +
 .../reference-matrix/.specify/features.md          |    5 +
 .../.specify/features/100-fixture-parent.md        |   14 +
 .../reference-matrix/.specify/glossary.md          |    3 +
 .../reference-matrix/.specify/history/topic.md     |    3 +
 .../reference-matrix/.specify/instructions.md      |    3 +
 .../.specify/memory/session/entry.md               |    3 +
 .../reference-matrix/.specify/register.md          |    3 +
 .../.specify/shared/definitions/example.md         |    3 +
 .../100-fixture-parent/checklists/checklist.md     |    3 +
 .../100-fixture-parent/contracts/core.contract.md  |    3 +
 .../specs/100-fixture-parent/merge-manifest.json   |   26 +
 .../specs/100-fixture-parent/notes/note.md         |    3 +
 .../.specify/specs/100-fixture-parent/plan.md      |    4 +
 .../specs/100-fixture-parent/requirements.md       |    3 +
 .../.specify/specs/100-fixture-parent/seal.md      |    4 +
 .../.specify/specs/100-fixture-parent/tasks.md     |    3 +
 .../100-fixture-parent/test-evidence/evidence.txt  |    1 +
 .../test-evidence/loose-forms.txt                  |    4 +
 .../test-evidence/split-forms.txt                  |    3 +
 .../specs/100-fixture-parent/verification.md       |    3 +
 .../.specify/specs/100a-fixture-alpha/notes.md     |    3 +
 .../.specify/specs/100a-fixture-alpha/plan.md      |    3 +
 .../specs/100a-fixture-alpha/requirements.md       |    8 +
 .../.specify/specs/100a-fixture-alpha/review.md    |    3 +
 .../.specify/specs/100a-fixture-alpha/tasks.md     |    3 +
 .../.specify/specs/100b-fixture-beta/notes.md      |    3 +
 .../specs/100b-fixture-beta/requirements.md        |    8 +
 .../.specify/specs/100b-fixture-beta/tasks.md      |    3 +
 .../.specify/state/100-fixture-parent.md           |    9 +
 .../reference-matrix/shared/definitions/example.md |    3 +
 .../tests/contract/fixture_refs.py                 |    5 +
 .../seal-archive/runtime-present/.gitignore        |    1 +
 .../specs/100-fixture-parent/merge-manifest.json   |   26 +
 .../specs/100-fixture-parent/requirements.md       |    3 +
 .../.specify/specs/100-fixture-parent/seal.md      |    4 +
 .../specs/100a-fixture-alpha/requirements.md       |    8 +
 .../.specify/specs/100a-fixture-alpha/tasks.md     |    3 +
 .../specs/100b-fixture-beta/requirements.md        |    8 +
 .../.specify/specs/100b-fixture-beta/tasks.md      |    3 +
 .../.specify/state/100-fixture-parent.md           |   13 +
 .../.specify/state/100a-fixture-alpha.md           |    8 +
 tests/integration/test_seal_074_round.py           |  279 +
 tests/integration/test_seal_archive_idempotency.py |  274 +
 tests/integration/test_seal_archive_rollback.py    |  241 +
 tests/integration/test_seal_archive_round.py       |  334 +
 tests/unit/test_seal_archive_classify.py           |  186 +
 tests/unit/test_seal_archive_manifest_math.py      |  107 +
 tests/unit/test_seal_archive_schema.py             |  179 +
 361 files changed, 30887 insertions(+), 446 deletions(-)
```

---

## Review 意见


### 🟠 [IMPORTANT] scripts/python/seal-utils.py (Line 1322)

> `amended_merge_document` pops `digest` and re-adds it after the walk (1322-1324), so the serialized merge manifest moves the digest line to the end; the ledger rows for the merge manifest were computed against the pre-write text, leaving 117 of 123 rows with a stale `line` in the 074 archive manifest. Preserve the key position (compute on a copy) or recompute those rows against the serialized document; add a 074 regression asserting each row's `after` text sits at its recorded line. Open as review.md F3 / REC-100-2.

<sub>14:23:48</sub>


### 🟠 [IMPORTANT] scripts/python/seal-utils.py (Line 4342)

> FR-015 / C-307 require a post-apply re-verification that unresolved references are still 0. The candidate is built with literal `0, 0` for `unresolved_before` / `unresolved_after` (4342-4343) and `_archive_apply_batch` never re-scans the archived tree after the writes, so `already-archived` re-quotes the plan-time value rather than a fresh measurement. Re-run the scan over the archived tree, fail + restore the batch on a non-zero count, and record the measured `unresolved_after`. Open as review.md F4 / REC-100-3.

<sub>14:23:48</sub>


### 🟢 [SUGGESTION] scripts/python/seal-utils.py (Line 506)

> C-102 says conditions that cannot be evaluated because an earlier input defect stopped the run MUST be reported as `not-evaluated (blocked-by <reason>)`. `_archive_manifest_error` emits exactly one condition for the raised error and the payload condition schema has no status field to carry the blocked-by rows. Either add the blocked-by rows or narrow C-102 to the observable behavior. Open as review.md F9 / REC-100-5.

<sub>14:23:48</sub>


### 👍 [PRAISE] scripts/python/seal-utils.py (Line 1261)

> The r1 repair's mixed-carrier guard is the right shape: `mixed_dated_sections` compares a mixed carrier's dated H2 blocks byte-for-byte while its live section is rewritten per ledger (C-306(c)/C-308), covered by a permitted-case test and a sabotage test that ends at 2 with a byte restore; red-first evidence and source/mirror parity are recorded in `test-evidence/review-repair-r1-*`. Preserve this repair pattern.

<sub>14:23:48</sub>


> **未提交范围（未评审）**: 15 个未提交路径未计入本次评审对象（.specify/specs/100-seal-slice-archive/review.md, .specify/templates/gitignore-specify-template, .specify/memory/exec-quant/records/20261111T061002731745Z-c16c0110.json, .specify/memory/exec-quant/records/20261111T061003197722Z-9a5863cc.json, .specify/memory/exec-quant/records/20261111T061003661020Z-337c8cb3.json, .specify/memory/exec-quant/records/20261111T061004127027Z-0b8e8637.json, .specify/memory/feedback/20261111T061010Z-skill-review-feature-quality.md, .specify/memory/feedback/20261111T061010Z-skill-review-sdd-process.md, .specify/memory/feedback/20261111T061010Z-speckit-review.md, .specify/memory/session/20261111T061002Z-run-determination-skill-review-sdd-process-r20261111t060957z.md, .specify/memory/session/20261111T061002Z-run-determination-speckit-review-r20261111t060957z-b100-revi.md, .specify/memory/session/20261111T061003Z-run-determination-skill-code-review-r20261111t060957z-b100-r.md, .specify/memory/session/20261111T061003Z-run-determination-skill-review-feature-quality-r20261111t060.md, .specify/specs/100-seal-slice-archive/review-100.md, .specify/specs/100-seal-slice-archive/test-evidence/review-r2-smoke.txt）；本回执不对该范围给出任何结论。

<!-- coverage-receipt:begin -->
receipt_version=1
base=48e273d7395d949656099c596161ac9210687cfa
head=7aa624e4c8d28f36e0b320f57c558f8f849ab1e8
base_source=feature-first-commit
renderer=text
changed_files=361
judged_files=27
skipped_files=334
gap_files=0
lines_added=5534
lines_deleted=113
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
file.005.path=.specify/features.md
file.005.verdict=skipped
file.005.reason=non-code-file
file.006.path=.specify/features/074-goal-team-sdd-unification.md
file.006.verdict=skipped
file.006.reason=non-code-file
file.007.path=.specify/features/099-speckit-seal.md
file.007.verdict=skipped
file.007.reason=non-code-file
file.008.path=.specify/memory/exec-quant/records/20261111T024124389486Z-258bc966.json
file.008.verdict=skipped
file.008.reason=generated
file.009.path=.specify/memory/exec-quant/records/20261111T025219170277Z-25d4e8df.json
file.009.verdict=skipped
file.009.reason=generated
file.010.path=.specify/memory/exec-quant/records/20261111T034446399229Z-12f02d26.json
file.010.verdict=skipped
file.010.reason=generated
file.011.path=.specify/memory/feedback/20261111T024128Z-speckit-tasks.md
file.011.verdict=skipped
file.011.reason=generated
file.012.path=.specify/memory/feedback/20261111T025219Z-speckit-checklist.md
file.012.verdict=skipped
file.012.reason=generated
file.013.path=.specify/memory/feedback/20261111T034446Z-speckit-analyze.md
file.013.verdict=skipped
file.013.reason=generated
file.014.path=.specify/memory/retention/closeout/20261111T024300Z-r20261111T024200Z-b100-tasks.md
file.014.verdict=skipped
file.014.reason=generated
file.015.path=.specify/memory/retention/closeout/20261111T025239Z-r20261111T025146Z-b100-checklist.md
file.015.verdict=skipped
file.015.reason=generated
file.016.path=.specify/memory/session/20261111T024044Z-run-determination-speckit-tasks-r20261111t024200z-b100-tasks.md
file.016.verdict=skipped
file.016.reason=generated
file.017.path=.specify/memory/session/20261111T025211Z-run-determination-speckit-checklist-r20261111t025146z-b100-c.md
file.017.verdict=skipped
file.017.reason=generated
file.018.path=.specify/memory/session/20261111T034440Z-run-determination-speckit-analyze-r20261111t034400z-b100-ana.md
file.018.verdict=skipped
file.018.reason=generated
file.019.path=.specify/register.md
file.019.verdict=skipped
file.019.reason=non-code-file
file.020.path=.specify/scripts/python/seal-utils.py
file.020.verdict=skipped
file.020.reason=generated
file.021.path=.specify/shared/definitions/framework-map.md
file.021.verdict=skipped
file.021.reason=generated
file.022.path=.specify/shared/definitions/non-disposable-definitions.md
file.022.verdict=skipped
file.022.reason=generated
file.023.path=.specify/shared/definitions/sdd-routing-definitions.md
file.023.verdict=skipped
file.023.reason=generated
file.024.path=.specify/skills/internal/analyze-artifacts/SKILL.md
file.024.verdict=skipped
file.024.reason=generated
file.025.path=.specify/skills/internal/seal-artifact/SKILL.md
file.025.verdict=skipped
file.025.reason=generated
file.026.path=.specify/specs/074-goal-team-sdd-unification/archive-manifest.json
file.026.verdict=skipped
file.026.reason=non-code-file
file.027.path=.specify/specs/074-goal-team-sdd-unification/code-review.md
file.027.verdict=skipped
file.027.reason=non-code-file
file.028.path=.specify/specs/074-goal-team-sdd-unification/contracts/bootstrap-and-maintenance.md
file.028.verdict=skipped
file.028.reason=non-code-file
file.029.path=.specify/specs/074-goal-team-sdd-unification/contracts/compat-and-safety.md
file.029.verdict=skipped
file.029.reason=non-code-file
file.030.path=.specify/specs/074-goal-team-sdd-unification/contracts/diffusion.md
file.030.verdict=skipped
file.030.reason=non-code-file
file.031.path=.specify/specs/074-goal-team-sdd-unification/contracts/hierarchy-and-authorization.md
file.031.verdict=skipped
file.031.reason=non-code-file
file.032.path=.specify/specs/074-goal-team-sdd-unification/contracts/routing-decision.md
file.032.verdict=skipped
file.032.reason=non-code-file
file.033.path=.specify/specs/074-goal-team-sdd-unification/merge-manifest.json
file.033.verdict=skipped
file.033.reason=non-code-file
file.034.path=.specify/specs/074-goal-team-sdd-unification/plan.md
file.034.verdict=skipped
file.034.reason=non-code-file
file.035.path=.specify/specs/074-goal-team-sdd-unification/research.md
file.035.verdict=skipped
file.035.reason=non-code-file
file.036.path=.specify/specs/074-goal-team-sdd-unification/review.md
file.036.verdict=skipped
file.036.reason=non-code-file
file.037.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/baseline-failed.txt
file.037.verdict=skipped
file.037.reason=non-code-file
file.038.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/checklists/readiness-2026-10-29.md
file.038.verdict=skipped
file.038.reason=non-code-file
file.039.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/checklists/recheck-2026-10-29-implement-start.md
file.039.verdict=skipped
file.039.reason=non-code-file
file.040.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/checklists/requirements.md
file.040.verdict=skipped
file.040.reason=non-code-file
file.041.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/code-review.md
file.041.verdict=skipped
file.041.reason=non-code-file
file.042.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/contracts/bootstrap-and-maintenance.md
file.042.verdict=skipped
file.042.reason=non-code-file
file.043.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/contracts/hierarchy-and-authorization.md
file.043.verdict=skipped
file.043.reason=non-code-file
file.044.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/contracts/nested-invocation.md
file.044.verdict=skipped
file.044.reason=non-code-file
file.045.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/contracts/routing-decision.md
file.045.verdict=skipped
file.045.reason=non-code-file
file.046.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/coverage-baseline.txt
file.046.verdict=skipped
file.046.reason=non-code-file
file.047.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/data-model.md
file.047.verdict=skipped
file.047.reason=non-code-file
file.048.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/feature-ref.md
file.048.verdict=skipped
file.048.reason=non-code-file
file.049.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/final-failed-2.txt
file.049.verdict=skipped
file.049.reason=non-code-file
file.050.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/final-failed-3.txt
file.050.verdict=skipped
file.050.reason=non-code-file
file.051.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/final-failed.txt
file.051.verdict=skipped
file.051.reason=non-code-file
file.052.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/notes/closure-full-run-2.txt
file.052.verdict=skipped
file.052.reason=non-code-file
file.053.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/notes/closure-full-run-3.txt
file.053.verdict=skipped
file.053.reason=non-code-file
file.054.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/notes/closure-full-run.txt
file.054.verdict=skipped
file.054.reason=non-code-file
file.055.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/notes/full-baseline-run.txt
file.055.verdict=skipped
file.055.reason=non-code-file
file.056.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/notes/golden-rows.txt
file.056.verdict=skipped
file.056.reason=non-code-file
file.057.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/notes/golden-run1.json
file.057.verdict=skipped
file.057.reason=non-code-file
file.058.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/notes/golden-run2.json
file.058.verdict=skipped
file.058.reason=non-code-file
file.059.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/notes/green-t016-demo.txt
file.059.verdict=skipped
file.059.reason=non-code-file
file.060.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/notes/green-t016.txt
file.060.verdict=skipped
file.060.reason=non-code-file
file.061.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/notes/green-t017.txt
file.061.verdict=skipped
file.061.reason=non-code-file
file.062.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/notes/green-t021.txt
file.062.verdict=skipped
file.062.reason=non-code-file
file.063.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/notes/green-t025-targeted.txt
file.063.verdict=skipped
file.063.reason=non-code-file
file.064.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/notes/green-t025.txt
file.064.verdict=skipped
file.064.reason=non-code-file
file.065.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/notes/part5-failed.txt
file.065.verdict=skipped
file.065.reason=non-code-file
file.066.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/notes/part5-regression.txt
file.066.verdict=skipped
file.066.reason=non-code-file
file.067.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/notes/pre-change-measurements.md
file.067.verdict=skipped
file.067.reason=non-code-file
file.068.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/notes/quickstart-run.md
file.068.verdict=skipped
file.068.reason=non-code-file
file.069.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/notes/red-first-evidence.md
file.069.verdict=skipped
file.069.reason=non-code-file
file.070.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/notes/red-t005.txt
file.070.verdict=skipped
file.070.reason=non-code-file
file.071.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/notes/red-t007.txt
file.071.verdict=skipped
file.071.reason=non-code-file
file.072.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/notes/red-t012.txt
file.072.verdict=skipped
file.072.reason=non-code-file
file.073.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/notes/red-t018.txt
file.073.verdict=skipped
file.073.reason=non-code-file
file.074.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/notes/red-t022.txt
file.074.verdict=skipped
file.074.reason=non-code-file
file.075.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/notes/targeted-set-v1-failed.txt
file.075.verdict=skipped
file.075.reason=non-code-file
file.076.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/plan.md
file.076.verdict=skipped
file.076.reason=non-code-file
file.077.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/quickstart.md
file.077.verdict=skipped
file.077.reason=non-code-file
file.078.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/requirements.md
file.078.verdict=skipped
file.078.reason=non-code-file
file.079.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/research.md
file.079.verdict=skipped
file.079.reason=non-code-file
file.080.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/review.md
file.080.verdict=skipped
file.080.reason=non-code-file
file.081.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/tasks.md
file.081.verdict=skipped
file.081.reason=non-code-file
file.082.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/test-evidence/analyze-fix-checks.md
file.082.verdict=skipped
file.082.reason=non-code-file
file.083.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/test-evidence/analyze.jsonl
file.083.verdict=skipped
file.083.reason=non-code-file
file.084.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/test-evidence/checklist-stage-checks.md
file.084.verdict=skipped
file.084.reason=non-code-file
file.085.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/test-evidence/checklist.jsonl
file.085.verdict=skipped
file.085.reason=non-code-file
file.086.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/test-evidence/clarify.jsonl
file.086.verdict=skipped
file.086.reason=non-code-file
file.087.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/test-evidence/implement.jsonl
file.087.verdict=skipped
file.087.reason=non-code-file
file.088.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/test-evidence/plan-stage-checks.md
file.088.verdict=skipped
file.088.reason=non-code-file
file.089.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/test-evidence/plan.jsonl
file.089.verdict=skipped
file.089.reason=non-code-file
file.090.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/test-evidence/review.jsonl
file.090.verdict=skipped
file.090.reason=non-code-file
file.091.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/test-evidence/targeted-set-v1-baseline.txt
file.091.verdict=skipped
file.091.reason=non-code-file
file.092.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/test-evidence/tasks-stage-checks.md
file.092.verdict=skipped
file.092.reason=non-code-file
file.093.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/test-evidence/tasks.jsonl
file.093.verdict=skipped
file.093.reason=non-code-file
file.094.path=.specify/specs/074-goal-team-sdd-unification/slices/074a-authorized-routing/verification.md
file.094.verdict=skipped
file.094.reason=non-code-file
file.095.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/baseline-failed.txt
file.095.verdict=skipped
file.095.reason=non-code-file
file.096.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/checklists/readiness-2026-10-29.md
file.096.verdict=skipped
file.096.reason=non-code-file
file.097.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/checklists/requirements.md
file.097.verdict=skipped
file.097.reason=non-code-file
file.098.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/code-review.md
file.098.verdict=skipped
file.098.reason=non-code-file
file.099.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/contracts/compat-and-safety.md
file.099.verdict=skipped
file.099.reason=non-code-file
file.100.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/contracts/diffusion.md
file.100.verdict=skipped
file.100.reason=non-code-file
file.101.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/contracts/report-and-attribution.md
file.101.verdict=skipped
file.101.reason=non-code-file
file.102.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/coverage-baseline.txt
file.102.verdict=skipped
file.102.reason=non-code-file
file.103.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/data-model.md
file.103.verdict=skipped
file.103.reason=non-code-file
file.104.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/feature-ref.md
file.104.verdict=skipped
file.104.reason=non-code-file
file.105.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/final-failed-2.txt
file.105.verdict=skipped
file.105.reason=non-code-file
file.106.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/final-failed.txt
file.106.verdict=skipped
file.106.reason=non-code-file
file.107.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/notes/closure-full-run-2.txt
file.107.verdict=skipped
file.107.reason=non-code-file
file.108.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/notes/closure-full-run.txt
file.108.verdict=skipped
file.108.reason=non-code-file
file.109.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/notes/pre-change-file-sets.txt
file.109.verdict=skipped
file.109.reason=non-code-file
file.110.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/notes/pre-change-measurements.md
file.110.verdict=skipped
file.110.reason=non-code-file
file.111.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/notes/quickstart-run.md
file.111.verdict=skipped
file.111.reason=non-code-file
file.112.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/notes/red-first-evidence.md
file.112.verdict=skipped
file.112.reason=non-code-file
file.113.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/plan.md
file.113.verdict=skipped
file.113.reason=non-code-file
file.114.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/quickstart.md
file.114.verdict=skipped
file.114.reason=non-code-file
file.115.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/requirements.md
file.115.verdict=skipped
file.115.reason=non-code-file
file.116.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/research.md
file.116.verdict=skipped
file.116.reason=non-code-file
file.117.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/review.md
file.117.verdict=skipped
file.117.reason=non-code-file
file.118.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/tasks.md
file.118.verdict=skipped
file.118.reason=non-code-file
file.119.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/analyze-fix-checks.md
file.119.verdict=skipped
file.119.reason=non-code-file
file.120.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/analyze.jsonl
file.120.verdict=skipped
file.120.reason=non-code-file
file.121.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/checklist-stage-checks.md
file.121.verdict=skipped
file.121.reason=non-code-file
file.122.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/checklist.jsonl
file.122.verdict=skipped
file.122.reason=non-code-file
file.123.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/clarify.jsonl
file.123.verdict=skipped
file.123.reason=non-code-file
file.124.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/compat-baseline-nodeids.txt
file.124.verdict=skipped
file.124.reason=non-code-file
file.125.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/containment-post-change-collect.txt
file.125.verdict=skipped
file.125.reason=non-code-file
file.126.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/containment-post-change-run.txt
file.126.verdict=skipped
file.126.reason=non-code-file
file.127.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/implement-baseline-run.txt
file.127.verdict=skipped
file.127.reason=non-code-file
file.128.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/implement-targeted-part1-failed.txt
file.128.verdict=skipped
file.128.reason=non-code-file
file.129.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/implement-targeted-part1-run.txt
file.129.verdict=skipped
file.129.reason=non-code-file
file.130.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/implement-targeted-part1-supp-failed.txt
file.130.verdict=skipped
file.130.reason=non-code-file
file.131.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/implement-targeted-part1-supp-run.txt
file.131.verdict=skipped
file.131.reason=non-code-file
file.132.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/implement-targeted-part2-failed.txt
file.132.verdict=skipped
file.132.reason=non-code-file
file.133.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/implement-targeted-part2-run.txt
file.133.verdict=skipped
file.133.reason=non-code-file
file.134.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/implement-targeted-part2-supp-failed.txt
file.134.verdict=skipped
file.134.reason=non-code-file
file.135.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/implement-targeted-part2-supp-run.txt
file.135.verdict=skipped
file.135.reason=non-code-file
file.136.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/implement-targeted-part3-failed.txt
file.136.verdict=skipped
file.136.reason=non-code-file
file.137.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/implement-targeted-part3-run.txt
file.137.verdict=skipped
file.137.reason=non-code-file
file.138.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/implement-targeted-part4-failed.txt
file.138.verdict=skipped
file.138.reason=non-code-file
file.139.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/implement-targeted-part4-run.txt
file.139.verdict=skipped
file.139.reason=non-code-file
file.140.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/implement.jsonl
file.140.verdict=skipped
file.140.reason=non-code-file
file.141.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/plan-stage-checks.md
file.141.verdict=skipped
file.141.reason=non-code-file
file.142.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/plan.jsonl
file.142.verdict=skipped
file.142.reason=non-code-file
file.143.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/requirements-checks.txt
file.143.verdict=skipped
file.143.reason=non-code-file
file.144.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/review.jsonl
file.144.verdict=skipped
file.144.reason=non-code-file
file.145.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/targeted-set-v1-baseline.txt
file.145.verdict=skipped
file.145.reason=non-code-file
file.146.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/tasks-stage-checks.md
file.146.verdict=skipped
file.146.reason=non-code-file
file.147.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/test-evidence/tasks.jsonl
file.147.verdict=skipped
file.147.reason=non-code-file
file.148.path=.specify/specs/074-goal-team-sdd-unification/slices/074b-nested-governance/verification.md
file.148.verdict=skipped
file.148.reason=non-code-file
file.149.path=.specify/specs/074-goal-team-sdd-unification/tasks.md
file.149.verdict=skipped
file.149.reason=non-code-file
file.150.path=.specify/specs/074-goal-team-sdd-unification/verification.md
file.150.verdict=skipped
file.150.reason=non-code-file
file.151.path=.specify/specs/099-speckit-seal/contracts/merge-back.contract.md
file.151.verdict=skipped
file.151.reason=non-code-file
file.152.path=.specify/specs/099-speckit-seal/contracts/records-and-boundaries.contract.md
file.152.verdict=skipped
file.152.reason=non-code-file
file.153.path=.specify/specs/099-speckit-seal/contracts/seal-engine.contract.md
file.153.verdict=skipped
file.153.reason=non-code-file
file.154.path=.specify/specs/100-seal-slice-archive/checklists/2026-11-11-requirements-quality.md
file.154.verdict=skipped
file.154.reason=non-code-file
file.155.path=.specify/specs/100-seal-slice-archive/checklists/requirements.md
file.155.verdict=skipped
file.155.reason=non-code-file
file.156.path=.specify/specs/100-seal-slice-archive/code-review.md
file.156.verdict=skipped
file.156.reason=non-code-file
file.157.path=.specify/specs/100-seal-slice-archive/contracts/archive-actions.contract.md
file.157.verdict=skipped
file.157.reason=non-code-file
file.158.path=.specify/specs/100-seal-slice-archive/contracts/archive-manifest.contract.md
file.158.verdict=skipped
file.158.reason=non-code-file
file.159.path=.specify/specs/100-seal-slice-archive/contracts/reference-classification.contract.md
file.159.verdict=skipped
file.159.reason=non-code-file
file.160.path=.specify/specs/100-seal-slice-archive/coverage-baseline.txt
file.160.verdict=skipped
file.160.reason=non-code-file
file.161.path=.specify/specs/100-seal-slice-archive/data-model.md
file.161.verdict=skipped
file.161.reason=non-code-file
file.162.path=.specify/specs/100-seal-slice-archive/feature-ref.md
file.162.verdict=skipped
file.162.reason=non-code-file
file.163.path=.specify/specs/100-seal-slice-archive/notes/pre-change-measurements.md
file.163.verdict=skipped
file.163.reason=non-code-file
file.164.path=.specify/specs/100-seal-slice-archive/notes/quickstart-run.md
file.164.verdict=skipped
file.164.reason=non-code-file
file.165.path=.specify/specs/100-seal-slice-archive/notes/red-first-evidence.md
file.165.verdict=skipped
file.165.reason=non-code-file
file.166.path=.specify/specs/100-seal-slice-archive/notes/requirements-research.md
file.166.verdict=skipped
file.166.reason=non-code-file
file.167.path=.specify/specs/100-seal-slice-archive/plan.md
file.167.verdict=skipped
file.167.reason=non-code-file
file.168.path=.specify/specs/100-seal-slice-archive/quickstart.md
file.168.verdict=skipped
file.168.reason=non-code-file
file.169.path=.specify/specs/100-seal-slice-archive/requirements.md
file.169.verdict=skipped
file.169.reason=non-code-file
file.170.path=.specify/specs/100-seal-slice-archive/research.md
file.170.verdict=skipped
file.170.reason=non-code-file
file.171.path=.specify/specs/100-seal-slice-archive/review.md
file.171.verdict=skipped
file.171.reason=non-code-file
file.172.path=.specify/specs/100-seal-slice-archive/tasks.md
file.172.verdict=skipped
file.172.reason=non-code-file
file.173.path=.specify/specs/100-seal-slice-archive/test-evidence/074-archive-round.txt
file.173.verdict=skipped
file.173.reason=non-code-file
file.174.path=.specify/specs/100-seal-slice-archive/test-evidence/analyze-coverage-round2.json
file.174.verdict=skipped
file.174.reason=non-code-file
file.175.path=.specify/specs/100-seal-slice-archive/test-evidence/analyze-coverage.json
file.175.verdict=skipped
file.175.reason=non-code-file
file.176.path=.specify/specs/100-seal-slice-archive/test-evidence/analyze-dispositions.md
file.176.verdict=skipped
file.176.reason=non-code-file
file.177.path=.specify/specs/100-seal-slice-archive/test-evidence/analyze-findings.jsonl
file.177.verdict=skipped
file.177.reason=non-code-file
file.178.path=.specify/specs/100-seal-slice-archive/test-evidence/analyze-gates-round2.txt
file.178.verdict=skipped
file.178.reason=non-code-file
file.179.path=.specify/specs/100-seal-slice-archive/test-evidence/analyze-gates.txt
file.179.verdict=skipped
file.179.reason=non-code-file
file.180.path=.specify/specs/100-seal-slice-archive/test-evidence/analyze-merged-2026-11-11.md
file.180.verdict=skipped
file.180.reason=non-code-file
file.181.path=.specify/specs/100-seal-slice-archive/test-evidence/analyze-precheck-decomp-tensions.txt
file.181.verdict=skipped
file.181.reason=non-code-file
file.182.path=.specify/specs/100-seal-slice-archive/test-evidence/analyze-precheck-plan-tasks.txt
file.182.verdict=skipped
file.182.reason=non-code-file
file.183.path=.specify/specs/100-seal-slice-archive/test-evidence/analyze-precheck-validators.txt
file.183.verdict=skipped
file.183.reason=non-code-file
file.184.path=.specify/specs/100-seal-slice-archive/test-evidence/checklist-stage-checks.txt
file.184.verdict=skipped
file.184.reason=non-code-file
file.185.path=.specify/specs/100-seal-slice-archive/test-evidence/clarify-gates.txt
file.185.verdict=skipped
file.185.reason=non-code-file
file.186.path=.specify/specs/100-seal-slice-archive/test-evidence/closure-verdict-100.json
file.186.verdict=skipped
file.186.reason=non-code-file
file.187.path=.specify/specs/100-seal-slice-archive/test-evidence/coverage-final.txt
file.187.verdict=skipped
file.187.reason=non-code-file
file.188.path=.specify/specs/100-seal-slice-archive/test-evidence/decomposition-plan.txt
file.188.verdict=skipped
file.188.reason=non-code-file
file.189.path=.specify/specs/100-seal-slice-archive/test-evidence/decomposition-tasks.json
file.189.verdict=skipped
file.189.reason=non-code-file
file.190.path=.specify/specs/100-seal-slice-archive/test-evidence/final-failed.txt
file.190.verdict=skipped
file.190.reason=non-code-file
file.191.path=.specify/specs/100-seal-slice-archive/test-evidence/final-mirrors.txt
file.191.verdict=skipped
file.191.reason=non-code-file
file.192.path=.specify/specs/100-seal-slice-archive/test-evidence/final-suite.txt
file.192.verdict=skipped
file.192.reason=non-code-file
file.193.path=.specify/specs/100-seal-slice-archive/test-evidence/flow-class-lookup.txt
file.193.verdict=skipped
file.193.reason=non-code-file
file.194.path=.specify/specs/100-seal-slice-archive/test-evidence/foundational-checks.txt
file.194.verdict=skipped
file.194.reason=non-code-file
file.195.path=.specify/specs/100-seal-slice-archive/test-evidence/p2-discovery.txt
file.195.verdict=skipped
file.195.reason=non-code-file
file.196.path=.specify/specs/100-seal-slice-archive/test-evidence/p3-fixtures.txt
file.196.verdict=skipped
file.196.reason=non-code-file
file.197.path=.specify/specs/100-seal-slice-archive/test-evidence/p3-green.txt
file.197.verdict=skipped
file.197.reason=non-code-file
file.198.path=.specify/specs/100-seal-slice-archive/test-evidence/p3-red-first.txt
file.198.verdict=skipped
file.198.reason=non-code-file
file.199.path=.specify/specs/100-seal-slice-archive/test-evidence/p3-regression.txt
file.199.verdict=skipped
file.199.reason=non-code-file
file.200.path=.specify/specs/100-seal-slice-archive/test-evidence/p4-green.txt
file.200.verdict=skipped
file.200.reason=non-code-file
file.201.path=.specify/specs/100-seal-slice-archive/test-evidence/p4-red-first.txt
file.201.verdict=skipped
file.201.reason=non-code-file
file.202.path=.specify/specs/100-seal-slice-archive/test-evidence/p4-regression.txt
file.202.verdict=skipped
file.202.reason=non-code-file
file.203.path=.specify/specs/100-seal-slice-archive/test-evidence/p5-owner-revision.txt
file.203.verdict=skipped
file.203.reason=non-code-file
file.204.path=.specify/specs/100-seal-slice-archive/test-evidence/p6-command-surface.txt
file.204.verdict=skipped
file.204.reason=non-code-file
file.205.path=.specify/specs/100-seal-slice-archive/test-evidence/plan-stage-checks.txt
file.205.verdict=skipped
file.205.reason=non-code-file
file.206.path=.specify/specs/100-seal-slice-archive/test-evidence/pre-analyze-requirements.txt
file.206.verdict=skipped
file.206.reason=non-code-file
file.207.path=.specify/specs/100-seal-slice-archive/test-evidence/requirements-measurements.txt
file.207.verdict=skipped
file.207.reason=non-code-file
file.208.path=.specify/specs/100-seal-slice-archive/test-evidence/review-repair-dispositions-r1-2026-11-11.md
file.208.verdict=skipped
file.208.reason=non-code-file
file.209.path=.specify/specs/100-seal-slice-archive/test-evidence/review-repair-r1-red-first.txt
file.209.verdict=skipped
file.209.reason=non-code-file
file.210.path=.specify/specs/100-seal-slice-archive/test-evidence/review-repair-r1-suite.txt
file.210.verdict=skipped
file.210.reason=non-code-file
file.211.path=.specify/specs/100-seal-slice-archive/test-evidence/sc-trace.txt
file.211.verdict=skipped
file.211.reason=non-code-file
file.212.path=.specify/specs/100-seal-slice-archive/test-evidence/structure-audit.txt
file.212.verdict=skipped
file.212.reason=non-code-file
file.213.path=.specify/specs/100-seal-slice-archive/test-evidence/tasks-stage-checks.txt
file.213.verdict=skipped
file.213.reason=non-code-file
file.214.path=.specify/specs/100-seal-slice-archive/test-evidence/us1-checkpoint.txt
file.214.verdict=skipped
file.214.reason=non-code-file
file.215.path=.specify/specs/100-seal-slice-archive/test-evidence/us2-checkpoint.txt
file.215.verdict=skipped
file.215.reason=non-code-file
file.216.path=.specify/specs/100-seal-slice-archive/test-evidence/us3-checkpoint.txt
file.216.verdict=skipped
file.216.reason=non-code-file
file.217.path=.specify/specs/100-seal-slice-archive/test-evidence/us4-checkpoint.txt
file.217.verdict=skipped
file.217.reason=non-code-file
file.218.path=.specify/specs/100-seal-slice-archive/test-evidence/validate-requirements.txt
file.218.verdict=skipped
file.218.reason=non-code-file
file.219.path=.specify/specs/100-seal-slice-archive/test-evidence/validate-tasks-final.txt
file.219.verdict=skipped
file.219.reason=non-code-file
file.220.path=.specify/specs/100-seal-slice-archive/verification.md
file.220.verdict=skipped
file.220.reason=non-code-file
file.221.path=docs/reference/commands/seal.md
file.221.verdict=reviewed
file.222.path=scripts/python/seal-utils.py
file.222.verdict=reviewed
file.223.path=shared/definitions/framework-map.md
file.223.verdict=reviewed
file.224.path=shared/definitions/non-disposable-definitions.md
file.224.verdict=reviewed
file.225.path=shared/definitions/sdd-routing-definitions.md
file.225.verdict=reviewed
file.226.path=skills/internal/analyze-artifacts/SKILL.md
file.226.verdict=reviewed
file.227.path=skills/internal/seal-artifact/SKILL.md
file.227.verdict=reviewed
file.228.path=templates/commands/seal.md
file.228.verdict=reviewed
file.229.path=tests/contract/test_sdd_compat_containment.py
file.229.verdict=reviewed
file.230.path=tests/contract/test_sdd_diffusion.py
file.230.verdict=reviewed
file.231.path=tests/contract/test_seal_archive_apply.py
file.231.verdict=reviewed
file.232.path=tests/contract/test_seal_archive_manifest.py
file.232.verdict=reviewed
file.233.path=tests/contract/test_seal_archive_plan.py
file.233.verdict=reviewed
file.234.path=tests/contract/test_seal_boundaries.py
file.234.verdict=reviewed
file.235.path=tests/contract/test_seal_engine_contract.py
file.235.verdict=reviewed
file.236.path=tests/contract/test_seal_merge_apply.py
file.236.verdict=reviewed
file.237.path=tests/contract/test_seal_merge_plan.py
file.237.verdict=reviewed
file.238.path=tests/fixtures/nested_sdd.py
file.238.verdict=reviewed
file.239.path=tests/fixtures/seal-archive/archived-pair/.specify/specs/100-fixture-parent/archive-manifest.json
file.239.verdict=skipped
file.239.reason=non-code-file
file.240.path=tests/fixtures/seal-archive/archived-pair/.specify/specs/100-fixture-parent/merge-manifest.json
file.240.verdict=skipped
file.240.reason=non-code-file
file.241.path=tests/fixtures/seal-archive/archived-pair/.specify/specs/100-fixture-parent/requirements.md
file.241.verdict=skipped
file.241.reason=non-code-file
file.242.path=tests/fixtures/seal-archive/archived-pair/.specify/specs/100-fixture-parent/slices/100a-fixture-alpha/requirements.md
file.242.verdict=skipped
file.242.reason=non-code-file
file.243.path=tests/fixtures/seal-archive/archived-pair/.specify/specs/100-fixture-parent/slices/100a-fixture-alpha/tasks.md
file.243.verdict=skipped
file.243.reason=non-code-file
file.244.path=tests/fixtures/seal-archive/archived-pair/.specify/specs/100-fixture-parent/slices/100b-fixture-beta/requirements.md
file.244.verdict=skipped
file.244.reason=non-code-file
file.245.path=tests/fixtures/seal-archive/archived-pair/.specify/specs/100-fixture-parent/slices/100b-fixture-beta/tasks.md
file.245.verdict=skipped
file.245.reason=non-code-file
file.246.path=tests/fixtures/seal-archive/archived-pair/.specify/state/100-fixture-parent.md
file.246.verdict=skipped
file.246.reason=non-code-file
file.247.path=tests/fixtures/seal-archive/blocked-pair/.specify/features.md
file.247.verdict=skipped
file.247.reason=non-code-file
file.248.path=tests/fixtures/seal-archive/blocked-pair/.specify/features/100-fixture-parent.md
file.248.verdict=skipped
file.248.reason=non-code-file
file.249.path=tests/fixtures/seal-archive/blocked-pair/.specify/specs/100-fixture-parent/code-review.md
file.249.verdict=skipped
file.249.reason=non-code-file
file.250.path=tests/fixtures/seal-archive/blocked-pair/.specify/specs/100-fixture-parent/merge-manifest.json
file.250.verdict=skipped
file.250.reason=non-code-file
file.251.path=tests/fixtures/seal-archive/blocked-pair/.specify/specs/100-fixture-parent/requirements.md
file.251.verdict=skipped
file.251.reason=non-code-file
file.252.path=tests/fixtures/seal-archive/blocked-pair/.specify/specs/100-fixture-parent/review.md
file.252.verdict=skipped
file.252.reason=non-code-file
file.253.path=tests/fixtures/seal-archive/blocked-pair/.specify/specs/100a-fixture-alpha/requirements.md
file.253.verdict=skipped
file.253.reason=non-code-file
file.254.path=tests/fixtures/seal-archive/blocked-pair/.specify/specs/100a-fixture-alpha/tasks.md
file.254.verdict=skipped
file.254.reason=non-code-file
file.255.path=tests/fixtures/seal-archive/blocked-pair/.specify/specs/100b-fixture-beta/requirements.md
file.255.verdict=skipped
file.255.reason=non-code-file
file.256.path=tests/fixtures/seal-archive/blocked-pair/.specify/specs/100b-fixture-beta/tasks.md
file.256.verdict=skipped
file.256.reason=non-code-file
file.257.path=tests/fixtures/seal-archive/clean-pair/.specify/specs/100-fixture-parent/merge-manifest.json
file.257.verdict=skipped
file.257.reason=non-code-file
file.258.path=tests/fixtures/seal-archive/clean-pair/.specify/specs/100-fixture-parent/requirements.md
file.258.verdict=skipped
file.258.reason=non-code-file
file.259.path=tests/fixtures/seal-archive/clean-pair/.specify/specs/100-fixture-parent/seal.md
file.259.verdict=skipped
file.259.reason=non-code-file
file.260.path=tests/fixtures/seal-archive/clean-pair/.specify/specs/100a-fixture-alpha/requirements.md
file.260.verdict=skipped
file.260.reason=non-code-file
file.261.path=tests/fixtures/seal-archive/clean-pair/.specify/specs/100a-fixture-alpha/tasks.md
file.261.verdict=skipped
file.261.reason=non-code-file
file.262.path=tests/fixtures/seal-archive/clean-pair/.specify/specs/100b-fixture-beta/requirements.md
file.262.verdict=skipped
file.262.reason=non-code-file
file.263.path=tests/fixtures/seal-archive/clean-pair/.specify/specs/100b-fixture-beta/tasks.md
file.263.verdict=skipped
file.263.reason=non-code-file
file.264.path=tests/fixtures/seal-archive/clean-pair/.specify/state/100-fixture-parent.md
file.264.verdict=skipped
file.264.reason=non-code-file
file.265.path=tests/fixtures/seal-archive/concurrent/.specify/specs/110-fixture-north/merge-manifest.json
file.265.verdict=skipped
file.265.reason=non-code-file
file.266.path=tests/fixtures/seal-archive/concurrent/.specify/specs/110-fixture-north/requirements.md
file.266.verdict=skipped
file.266.reason=non-code-file
file.267.path=tests/fixtures/seal-archive/concurrent/.specify/specs/110a-fixture-north-slice/requirements.md
file.267.verdict=skipped
file.267.reason=non-code-file
file.268.path=tests/fixtures/seal-archive/concurrent/.specify/specs/110a-fixture-north-slice/tasks.md
file.268.verdict=skipped
file.268.reason=non-code-file
file.269.path=tests/fixtures/seal-archive/concurrent/.specify/specs/120-fixture-south/merge-manifest.json
file.269.verdict=skipped
file.269.reason=non-code-file
file.270.path=tests/fixtures/seal-archive/concurrent/.specify/specs/120-fixture-south/requirements.md
file.270.verdict=skipped
file.270.reason=non-code-file
file.271.path=tests/fixtures/seal-archive/concurrent/.specify/specs/120a-fixture-south-slice/requirements.md
file.271.verdict=skipped
file.271.reason=non-code-file
file.272.path=tests/fixtures/seal-archive/concurrent/.specify/specs/120a-fixture-south-slice/tasks.md
file.272.verdict=skipped
file.272.reason=non-code-file
file.273.path=tests/fixtures/seal-archive/concurrent/.specify/state/110-fixture-north.md
file.273.verdict=skipped
file.273.reason=non-code-file
file.274.path=tests/fixtures/seal-archive/concurrent/.specify/state/120-fixture-south.md
file.274.verdict=skipped
file.274.reason=non-code-file
file.275.path=tests/fixtures/seal-archive/empty/.specify/specs/100-fixture-empty/merge-manifest.json
file.275.verdict=skipped
file.275.reason=non-code-file
file.276.path=tests/fixtures/seal-archive/empty/.specify/specs/100-fixture-empty/requirements.md
file.276.verdict=skipped
file.276.reason=non-code-file
file.277.path=tests/fixtures/seal-archive/partial-pair/.specify/specs/100-fixture-parent/merge-manifest.json
file.277.verdict=skipped
file.277.reason=non-code-file
file.278.path=tests/fixtures/seal-archive/partial-pair/.specify/specs/100-fixture-parent/requirements.md
file.278.verdict=skipped
file.278.reason=non-code-file
file.279.path=tests/fixtures/seal-archive/partial-pair/.specify/specs/100-fixture-parent/slices/100b-fixture-beta/requirements.md
file.279.verdict=skipped
file.279.reason=non-code-file
file.280.path=tests/fixtures/seal-archive/partial-pair/.specify/specs/100-fixture-parent/slices/100b-fixture-beta/tasks.md
file.280.verdict=skipped
file.280.reason=non-code-file
file.281.path=tests/fixtures/seal-archive/partial-pair/.specify/specs/100a-fixture-alpha/requirements.md
file.281.verdict=skipped
file.281.reason=non-code-file
file.282.path=tests/fixtures/seal-archive/partial-pair/.specify/specs/100a-fixture-alpha/tasks.md
file.282.verdict=skipped
file.282.reason=non-code-file
file.283.path=tests/fixtures/seal-archive/partial-pair/.specify/state/100-fixture-parent.md
file.283.verdict=skipped
file.283.reason=non-code-file
file.284.path=tests/fixtures/seal-archive/reference-matrix-unclassified/.specify/features.md
file.284.verdict=skipped
file.284.reason=non-code-file
file.285.path=tests/fixtures/seal-archive/reference-matrix-unclassified/.specify/features/100-fixture-parent.md
file.285.verdict=skipped
file.285.reason=non-code-file
file.286.path=tests/fixtures/seal-archive/reference-matrix-unclassified/.specify/glossary.md
file.286.verdict=skipped
file.286.reason=non-code-file
file.287.path=tests/fixtures/seal-archive/reference-matrix-unclassified/.specify/history/topic.md
file.287.verdict=skipped
file.287.reason=non-code-file
file.288.path=tests/fixtures/seal-archive/reference-matrix-unclassified/.specify/instructions.md
file.288.verdict=skipped
file.288.reason=non-code-file
file.289.path=tests/fixtures/seal-archive/reference-matrix-unclassified/.specify/memory/session/entry.md
file.289.verdict=skipped
file.289.reason=non-code-file
file.290.path=tests/fixtures/seal-archive/reference-matrix-unclassified/.specify/register.md
file.290.verdict=skipped
file.290.reason=non-code-file
file.291.path=tests/fixtures/seal-archive/reference-matrix-unclassified/.specify/shared/definitions/example.md
file.291.verdict=skipped
file.291.reason=non-code-file
file.292.path=tests/fixtures/seal-archive/reference-matrix-unclassified/.specify/specs/100-fixture-parent/checklists/checklist.md
file.292.verdict=skipped
file.292.reason=non-code-file
file.293.path=tests/fixtures/seal-archive/reference-matrix-unclassified/.specify/specs/100-fixture-parent/contracts/core.contract.md
file.293.verdict=skipped
file.293.reason=non-code-file
file.294.path=tests/fixtures/seal-archive/reference-matrix-unclassified/.specify/specs/100-fixture-parent/merge-manifest.json
file.294.verdict=skipped
file.294.reason=non-code-file
file.295.path=tests/fixtures/seal-archive/reference-matrix-unclassified/.specify/specs/100-fixture-parent/notes/note.md
file.295.verdict=skipped
file.295.reason=non-code-file
file.296.path=tests/fixtures/seal-archive/reference-matrix-unclassified/.specify/specs/100-fixture-parent/plan.md
file.296.verdict=skipped
file.296.reason=non-code-file
file.297.path=tests/fixtures/seal-archive/reference-matrix-unclassified/.specify/specs/100-fixture-parent/requirements.md
file.297.verdict=skipped
file.297.reason=non-code-file
file.298.path=tests/fixtures/seal-archive/reference-matrix-unclassified/.specify/specs/100-fixture-parent/seal.md
file.298.verdict=skipped
file.298.reason=non-code-file
file.299.path=tests/fixtures/seal-archive/reference-matrix-unclassified/.specify/specs/100-fixture-parent/tasks.md
file.299.verdict=skipped
file.299.reason=non-code-file
file.300.path=tests/fixtures/seal-archive/reference-matrix-unclassified/.specify/specs/100-fixture-parent/test-evidence/evidence.txt
file.300.verdict=skipped
file.300.reason=non-code-file
file.301.path=tests/fixtures/seal-archive/reference-matrix-unclassified/.specify/specs/100-fixture-parent/unsorted/random.md
file.301.verdict=skipped
file.301.reason=non-code-file
file.302.path=tests/fixtures/seal-archive/reference-matrix-unclassified/.specify/specs/100-fixture-parent/verification.md
file.302.verdict=skipped
file.302.reason=non-code-file
file.303.path=tests/fixtures/seal-archive/reference-matrix-unclassified/.specify/specs/100a-fixture-alpha/notes.md
file.303.verdict=skipped
file.303.reason=non-code-file
file.304.path=tests/fixtures/seal-archive/reference-matrix-unclassified/.specify/specs/100a-fixture-alpha/plan.md
file.304.verdict=skipped
file.304.reason=non-code-file
file.305.path=tests/fixtures/seal-archive/reference-matrix-unclassified/.specify/specs/100a-fixture-alpha/requirements.md
file.305.verdict=skipped
file.305.reason=non-code-file
file.306.path=tests/fixtures/seal-archive/reference-matrix-unclassified/.specify/specs/100a-fixture-alpha/review.md
file.306.verdict=skipped
file.306.reason=non-code-file
file.307.path=tests/fixtures/seal-archive/reference-matrix-unclassified/.specify/specs/100a-fixture-alpha/tasks.md
file.307.verdict=skipped
file.307.reason=non-code-file
file.308.path=tests/fixtures/seal-archive/reference-matrix-unclassified/.specify/specs/100b-fixture-beta/notes.md
file.308.verdict=skipped
file.308.reason=non-code-file
file.309.path=tests/fixtures/seal-archive/reference-matrix-unclassified/.specify/specs/100b-fixture-beta/requirements.md
file.309.verdict=skipped
file.309.reason=non-code-file
file.310.path=tests/fixtures/seal-archive/reference-matrix-unclassified/.specify/specs/100b-fixture-beta/tasks.md
file.310.verdict=skipped
file.310.reason=non-code-file
file.311.path=tests/fixtures/seal-archive/reference-matrix-unclassified/.specify/state/100-fixture-parent.md
file.311.verdict=skipped
file.311.reason=non-code-file
file.312.path=tests/fixtures/seal-archive/reference-matrix-unclassified/shared/definitions/example.md
file.312.verdict=skipped
file.312.reason=non-code-file
file.313.path=tests/fixtures/seal-archive/reference-matrix-unclassified/tests/contract/fixture_refs.py
file.313.verdict=reviewed
file.314.path=tests/fixtures/seal-archive/reference-matrix/.specify/features.md
file.314.verdict=skipped
file.314.reason=non-code-file
file.315.path=tests/fixtures/seal-archive/reference-matrix/.specify/features/100-fixture-parent.md
file.315.verdict=skipped
file.315.reason=non-code-file
file.316.path=tests/fixtures/seal-archive/reference-matrix/.specify/glossary.md
file.316.verdict=skipped
file.316.reason=non-code-file
file.317.path=tests/fixtures/seal-archive/reference-matrix/.specify/history/topic.md
file.317.verdict=skipped
file.317.reason=non-code-file
file.318.path=tests/fixtures/seal-archive/reference-matrix/.specify/instructions.md
file.318.verdict=skipped
file.318.reason=non-code-file
file.319.path=tests/fixtures/seal-archive/reference-matrix/.specify/memory/session/entry.md
file.319.verdict=skipped
file.319.reason=non-code-file
file.320.path=tests/fixtures/seal-archive/reference-matrix/.specify/register.md
file.320.verdict=skipped
file.320.reason=non-code-file
file.321.path=tests/fixtures/seal-archive/reference-matrix/.specify/shared/definitions/example.md
file.321.verdict=skipped
file.321.reason=non-code-file
file.322.path=tests/fixtures/seal-archive/reference-matrix/.specify/specs/100-fixture-parent/checklists/checklist.md
file.322.verdict=skipped
file.322.reason=non-code-file
file.323.path=tests/fixtures/seal-archive/reference-matrix/.specify/specs/100-fixture-parent/contracts/core.contract.md
file.323.verdict=skipped
file.323.reason=non-code-file
file.324.path=tests/fixtures/seal-archive/reference-matrix/.specify/specs/100-fixture-parent/merge-manifest.json
file.324.verdict=skipped
file.324.reason=non-code-file
file.325.path=tests/fixtures/seal-archive/reference-matrix/.specify/specs/100-fixture-parent/notes/note.md
file.325.verdict=skipped
file.325.reason=non-code-file
file.326.path=tests/fixtures/seal-archive/reference-matrix/.specify/specs/100-fixture-parent/plan.md
file.326.verdict=skipped
file.326.reason=non-code-file
file.327.path=tests/fixtures/seal-archive/reference-matrix/.specify/specs/100-fixture-parent/requirements.md
file.327.verdict=skipped
file.327.reason=non-code-file
file.328.path=tests/fixtures/seal-archive/reference-matrix/.specify/specs/100-fixture-parent/seal.md
file.328.verdict=skipped
file.328.reason=non-code-file
file.329.path=tests/fixtures/seal-archive/reference-matrix/.specify/specs/100-fixture-parent/tasks.md
file.329.verdict=skipped
file.329.reason=non-code-file
file.330.path=tests/fixtures/seal-archive/reference-matrix/.specify/specs/100-fixture-parent/test-evidence/evidence.txt
file.330.verdict=skipped
file.330.reason=non-code-file
file.331.path=tests/fixtures/seal-archive/reference-matrix/.specify/specs/100-fixture-parent/test-evidence/loose-forms.txt
file.331.verdict=skipped
file.331.reason=non-code-file
file.332.path=tests/fixtures/seal-archive/reference-matrix/.specify/specs/100-fixture-parent/test-evidence/split-forms.txt
file.332.verdict=skipped
file.332.reason=non-code-file
file.333.path=tests/fixtures/seal-archive/reference-matrix/.specify/specs/100-fixture-parent/verification.md
file.333.verdict=skipped
file.333.reason=non-code-file
file.334.path=tests/fixtures/seal-archive/reference-matrix/.specify/specs/100a-fixture-alpha/notes.md
file.334.verdict=skipped
file.334.reason=non-code-file
file.335.path=tests/fixtures/seal-archive/reference-matrix/.specify/specs/100a-fixture-alpha/plan.md
file.335.verdict=skipped
file.335.reason=non-code-file
file.336.path=tests/fixtures/seal-archive/reference-matrix/.specify/specs/100a-fixture-alpha/requirements.md
file.336.verdict=skipped
file.336.reason=non-code-file
file.337.path=tests/fixtures/seal-archive/reference-matrix/.specify/specs/100a-fixture-alpha/review.md
file.337.verdict=skipped
file.337.reason=non-code-file
file.338.path=tests/fixtures/seal-archive/reference-matrix/.specify/specs/100a-fixture-alpha/tasks.md
file.338.verdict=skipped
file.338.reason=non-code-file
file.339.path=tests/fixtures/seal-archive/reference-matrix/.specify/specs/100b-fixture-beta/notes.md
file.339.verdict=skipped
file.339.reason=non-code-file
file.340.path=tests/fixtures/seal-archive/reference-matrix/.specify/specs/100b-fixture-beta/requirements.md
file.340.verdict=skipped
file.340.reason=non-code-file
file.341.path=tests/fixtures/seal-archive/reference-matrix/.specify/specs/100b-fixture-beta/tasks.md
file.341.verdict=skipped
file.341.reason=non-code-file
file.342.path=tests/fixtures/seal-archive/reference-matrix/.specify/state/100-fixture-parent.md
file.342.verdict=skipped
file.342.reason=non-code-file
file.343.path=tests/fixtures/seal-archive/reference-matrix/shared/definitions/example.md
file.343.verdict=skipped
file.343.reason=non-code-file
file.344.path=tests/fixtures/seal-archive/reference-matrix/tests/contract/fixture_refs.py
file.344.verdict=reviewed
file.345.path=tests/fixtures/seal-archive/runtime-present/.gitignore
file.345.verdict=skipped
file.345.reason=non-code-file
file.346.path=tests/fixtures/seal-archive/runtime-present/.specify/specs/100-fixture-parent/merge-manifest.json
file.346.verdict=skipped
file.346.reason=non-code-file
file.347.path=tests/fixtures/seal-archive/runtime-present/.specify/specs/100-fixture-parent/requirements.md
file.347.verdict=skipped
file.347.reason=non-code-file
file.348.path=tests/fixtures/seal-archive/runtime-present/.specify/specs/100-fixture-parent/seal.md
file.348.verdict=skipped
file.348.reason=non-code-file
file.349.path=tests/fixtures/seal-archive/runtime-present/.specify/specs/100a-fixture-alpha/requirements.md
file.349.verdict=skipped
file.349.reason=non-code-file
file.350.path=tests/fixtures/seal-archive/runtime-present/.specify/specs/100a-fixture-alpha/tasks.md
file.350.verdict=skipped
file.350.reason=non-code-file
file.351.path=tests/fixtures/seal-archive/runtime-present/.specify/specs/100b-fixture-beta/requirements.md
file.351.verdict=skipped
file.351.reason=non-code-file
file.352.path=tests/fixtures/seal-archive/runtime-present/.specify/specs/100b-fixture-beta/tasks.md
file.352.verdict=skipped
file.352.reason=non-code-file
file.353.path=tests/fixtures/seal-archive/runtime-present/.specify/state/100-fixture-parent.md
file.353.verdict=skipped
file.353.reason=non-code-file
file.354.path=tests/fixtures/seal-archive/runtime-present/.specify/state/100a-fixture-alpha.md
file.354.verdict=skipped
file.354.reason=non-code-file
file.355.path=tests/integration/test_seal_074_round.py
file.355.verdict=reviewed
file.356.path=tests/integration/test_seal_archive_idempotency.py
file.356.verdict=reviewed
file.357.path=tests/integration/test_seal_archive_rollback.py
file.357.verdict=reviewed
file.358.path=tests/integration/test_seal_archive_round.py
file.358.verdict=reviewed
file.359.path=tests/unit/test_seal_archive_classify.py
file.359.verdict=reviewed
file.360.path=tests/unit/test_seal_archive_manifest_math.py
file.360.verdict=reviewed
file.361.path=tests/unit/test_seal_archive_schema.py
file.361.verdict=reviewed
<!-- coverage-receipt:end -->
