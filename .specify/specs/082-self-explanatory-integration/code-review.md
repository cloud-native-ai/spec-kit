# Code Review Report — 代码段 (code segment)

| 属性 | 值 |
|------|-----|
| **分支** | `082-self-explanatory-integration` |
| **基准** | `2f6b8bbbb061563769d6953371714b3494811795` (`2f6b8bbb`) |
| **目标** | `b2880fa081a52b53b3a6b8411c8dcc5c4493db27` (`b2880fa0`) |
| **基准来源** | `feature-first-commit` |
| **渲染模式** | `renderer: text` |
| **Reviewer** | `Qiming Liu (John)` |
| **日期** | `2026-11-05T06:44:08Z` |

## 变更概览

```
 .specify/instructions.md                           |   6 +
 .specify/memory/constitution.md                    |  41 +-
 .../records/20261105T063815894632Z-d9e6df67.json   |   1 +
 .specify/memory/features.md                        |   4 +-
 .specify/memory/features/082.md                    |  34 +-
 .../feedback/20261105T063820Z-speckit-implement.md |  20 +
 .specify/memory/glossary.md                        |   1 +
 .specify/memory/register.md                        |   1 +
 ...ion-speckit-implement-r20261105t032102z-c139.md | 225 +++++++
 .specify/scripts/bash/generate-instructions.sh     |  17 +-
 .../definitions/self-explanatory-definitions.md    |  56 ++
 .specify/shared/guidelines/self-explanatory.md     |  94 +++
 .../shared/workflow/best-practice-optimization.md  |  71 +++
 .../skills/internal/manage-constitution/SKILL.md   |  13 +
 .specify/skills/sdd-loop-driver/SKILL.md           |   2 +-
 .../sdd-loop-driver/references/efficiency-model.md |   6 +-
 .../sdd-loop-driver/scripts/admission-check.py     |   2 +-
 .../sdd-loop-driver/scripts/decomposition-check.py |   2 +-
 .../baseline-failed.txt                            |  26 +
 .../checklists/requirements-quality-20261105.md    | 204 ++++++
 .../checklists/requirements.md                     |  39 ++
 .../coverage-baseline.txt                          | 515 +++++++++++++++
 .../notes/pre-change-measurements.md               | 670 ++++++++++++++++++++
 .../notes/quickstart-run.md                        | 481 ++++++++++++++
 .../notes/red-first-evidence.md                    | 700 +++++++++++++++++++++
 .../requirements.md                                | 193 ++++++
 .../082-self-explanatory-integration/tasks.md      | 302 +++++++++
 .../test-evidence/analyze-stage-checks.md          |  85 +++
 .../test-evidence/checklist-stage-checks.md        | 113 ++++
 .../test-evidence/implement-part-10a.md            | 164 +++++
 .../test-evidence/implement-part-10b.md            | 124 ++++
 .../test-evidence/implement-part-2.md              |  15 +
 .../test-evidence/implement-part-3.md              | 113 ++++
 .../test-evidence/implement-part-4.md              |  97 +++
 .../test-evidence/implement-part-5.md              |  17 +
 .../test-evidence/implement-part-6.md              | 142 +++++
 .../test-evidence/implement-part-7.md              | 110 ++++
 .../test-evidence/implement-part-8.md              | 138 ++++
 .../test-evidence/implement-part-9.md              | 126 ++++
 .../test-evidence/smoke-20261105.txt               |  30 +
 .../test-evidence/tasks-stage-premises.md          | 158 +++++
 .../verification.md                                | 144 +++++
 .specify/state/082-self-explanatory-integration.md | 655 +++++++++++++++++++
 .specify/templates/constitution-template.md        |  22 +
 .specify/templates/instructions-template.md        |   6 +
 docs/concepts/self-explanatory.md                  |  37 ++
 docs/reference/skills/sdd-loop-driver.md           |   2 +-
 scripts/bash/generate-instructions.sh              |  17 +-
 shared/definitions/self-explanatory-definitions.md |  56 ++
 shared/guidelines/self-explanatory.md              |  94 +++
 shared/workflow/best-practice-optimization.md      |  71 +++
 skills/external/sdd-loop-driver/SKILL.md           |   2 +-
 .../sdd-loop-driver/references/efficiency-model.md |   6 +-
 .../sdd-loop-driver/scripts/admission-check.py     |   2 +-
 .../sdd-loop-driver/scripts/decomposition-check.py |   2 +-
 skills/internal/manage-constitution/SKILL.md       |  13 +
 templates/constitution-template.md                 |  22 +
 templates/instructions-template.md                 |   6 +
 tests/contract/test_constitution_double_landing.py |  15 +-
 tests/contract/test_fast_fail_discipline.py        |  56 +-
 .../test_instructions_section_propagation.py       | 190 ++++++
 tests/contract/test_instructions_size_budget.py    |  25 +
 tests/contract/test_sdd_loop_driver_efficiency.py  |   2 +-
 tests/contract/test_sdd_loop_driver_gates.py       |   2 +-
 .../contract/test_self_explanatory_constitution.py | 503 +++++++++++++++
 .../contract/test_self_explanatory_distribution.py | 625 ++++++++++++++++++
 tests/contract/test_self_explanatory_glossary.py   | 470 ++++++++++++++
 tests/unit/test_decomposition_check.py             |  12 +-
 tests/unit/test_pre_analyze_check.py               |   2 +-
 69 files changed, 8169 insertions(+), 48 deletions(-)
```

---

## Review 意见


### 🟠 [IMPORTANT] tests/contract/test_fast_fail_discipline.py (Line 724)

> The a7 section-count pin was raised 30/31 -> 31/32, but the subject it measures had already been at 31/32 since 878c03ab, so the pre-change pin was stale and a7 was RED at the reviewed base. Verified independently: at 878c03ab the test reads 'template has 31 ... expected 30' (FAILED). Reproduced the generator's injection on a live file missing exactly one section: with a 32-section template it injects 1 section, not 33. Either the stale pin was hit live during part 4 and was repaired in passing and is nowhere disclosed in this delta's evidence, or T024's 'import the section additively' obligation (a precondition of SC-003 and the R-4 pair) was discharged by an unconditional rewrite of the live file. Neither is decidable from the artifacts, and the first reading would mean a defect was masked with no leave-behind assertion. Needs: the transcript of the part-4 generator run that first injected the section, and either (a) the stale-pin repair stated as an in-passing repair with its red captured, or (b) the live-reconcile evidence re-taken.

<sub>14:45:12</sub>


### ❓ [QUESTION] .specify/memory/features.md (Line 90)

> Delta hygiene: the Feature 082 row's status went Planned -> Implemented in commit 1f6ab51c ('close implement'), yet the diff stat for that commit reports 4 changed lines and the post-implementation closure commit b2880fa0 has an EMPTY diff, so the state spine's per-part checkpoint discipline (a spine write per part) was not honoured for part 10b. Additionally the spine's part-8 checkpoint was committed at 5085f46f, after the part-9 code carrier 32fc3e70 landed, so commit order does not reconstruct part attribution. Every evidence file does declare its stage_base, so the per-part timeline stays recoverable from artifacts — this degradation is recorded rather than treated as missing history. Which commit carried the status flip is the question the table cannot answer on its own.

<sub>14:45:15</sub>


### 🟠 [IMPORTANT] .specify/specs/082-self-explanatory-integration/notes/red-first-evidence.md (Line 534)

> The mutation-leg identifier M-1..M-6 is re-used for two different closed sets. commands/constitution-double-landing.contract.md and instructions-propagation.contract.md define M-1..M-4 (principle block, mandate entry, template section, generator non-injection), while lines 534-576 of this file apply the SAME ids to part-8 legs (second canonical row, duplicate canonical, owner-path, MIRROR_PAIRS emptied, mirror byte flip). C-21's red was also produced by a part-4 run the contract table never names. The R-3/R-6 rows above at line 534 point at 'M-1 / M-2 (part 8)' and 'M-4 / M-5 (part 8)', which read as references to the contract's legs and are not: a reader tracing which contract leg proves which guard follows the wrong row. Needs a separate id family for the part-8 legs (e.g. G-1..G-5) and the C-21 red named in the instructions contract's mutation table.

<sub>14:45:19</sub>


### 🟢 [SUGGESTION] tests/contract/test_fast_fail_discipline.py (Line 1117)

> test_x13_double_landing_three_count_pins now hard-codes ("TEMPLATE_COUNT", 18), ("LIVE_COUNT", 19), ("COMMAND_COUNT", 11). That is exactly the class this feature's own A4 assumption declares MUST NOT happen ('MUST NOT hardcode the template numeral into live or tests' — here the equivalent: the count values), and it is the second-order copy of the fact that .specify/specs/082-self-explanatory-integration/contracts/constitution-double-landing.contract.md#C-5 already owns. Derive the three values from the artifacts they describe (len(PRINCIPLE_RE.findall(template)) / live / the mandate-entry count the same test already computes) so the next amendment does not have to edit a pin in a foreign feature's guard.

<sub>14:45:23</sub>


> **未提交范围（未评审）**: 31 个未提交路径未计入本次评审对象（.specify/memory/session/20261019T184302Z-run-determination-speckit-implement-063-implement-attempt2-2.md, .specify/memory/session/20261030T102937Z-run-determination-speckit-implement-r20261030t081645z-078a.md, .specify/memory/session/20261030T130915Z-run-determination-speckit-tasks-r20261030t110000z-079a-tasks.md, .specify/memory/session/20261030T161739Z-run-determination-speckit-implement-r20261030t110000z-079a.md, .specify/memory/session/20261102T234434Z-run-determination-speckit-tasks-r20261102t225758z-081a.md, .specify/memory/session/20261103T050136Z-run-determination-speckit-analyze-r20261103t043000z-081b.md, .specify/specs/082-self-explanatory-integration/notes/red-first-evidence.md, .specify/specs/082-self-explanatory-integration/test-evidence/implement-part-8.md, tests/contract/test_fast_fail_discipline.py, .specify/memory/exec-quant/records/20261104T064101087309Z-72e14493.json, .specify/memory/exec-quant/records/20261104T080021522767Z-9c34974b.json, .specify/memory/exec-quant/records/20261105T030823449585Z-93411926.json, .specify/memory/exec-quant/records/20261105T033022907426Z-2932d61f.json, .specify/memory/exec-quant/records/20261105T033630408551Z-b337d0f2.json, .specify/memory/exec-quant/records/20261105T035525387720Z-9e2fbd29.json, .specify/memory/exec-quant/records/20261105T040449355071Z-b07129a1.json, .specify/memory/feedback/20261104T064101Z-speckit-interview.md, .specify/memory/feedback/20261104T080021Z-speckit-requirements.md, .specify/memory/feedback/20261105T030823Z-speckit-clarify.md, .specify/memory/feedback/20261105T033022Z-speckit-plan.md, .specify/memory/feedback/20261105T033635Z-speckit-tasks.md, .specify/memory/feedback/20261105T035530Z-speckit-checklist.md, .specify/memory/feedback/20261105T040452Z-speckit-analyze.md, .specify/memory/session/20261104T064100Z-run-determination-speckit-interview-20261104t064100z.md, .specify/memory/session/20261104T080021Z-run-determination-speckit-requirements-20261104t080021z.md, .specify/memory/session/20261105T030823Z-run-determination-speckit-clarify-20261105t030823z.md, .specify/memory/session/20261105T033022Z-run-determination-speckit-plan-r20261105t033022z-e4a7.md, .specify/memory/session/20261105T033628Z-run-determination-speckit-tasks-r20261105t033022z-082tasks.md, .specify/memory/session/20261105T040447Z-run-determination-speckit-analyze-r20261105t032102z-c139-ana.md, .specify/memory/session/interview-wangwenshengyi.dag.json, .specify/specs/082-self-explanatory-integration/test-evidence/implement-part2-stage-checks.md）；本回执不对该范围给出任何结论。

<!-- coverage-receipt:begin -->
receipt_version=1
base=2f6b8bbbb061563769d6953371714b3494811795
head=b2880fa081a52b53b3a6b8411c8dcc5c4493db27
base_source=feature-first-commit
renderer=text
changed_files=69
judged_files=69
skipped_files=0
gap_files=0
lines_added=8169
lines_deleted=48
file.01.path=.specify/instructions.md
file.01.verdict=reviewed
file.02.path=.specify/memory/constitution.md
file.02.verdict=reviewed
file.03.path=.specify/memory/exec-quant/records/20261105T063815894632Z-d9e6df67.json
file.03.verdict=reviewed
file.04.path=.specify/memory/features.md
file.04.verdict=reviewed
file.05.path=.specify/memory/features/082.md
file.05.verdict=reviewed
file.06.path=.specify/memory/feedback/20261105T063820Z-speckit-implement.md
file.06.verdict=reviewed
file.07.path=.specify/memory/glossary.md
file.07.verdict=reviewed
file.08.path=.specify/memory/register.md
file.08.verdict=reviewed
file.09.path=.specify/memory/session/20261105T063813Z-run-determination-speckit-implement-r20261105t032102z-c139.md
file.09.verdict=reviewed
file.10.path=.specify/scripts/bash/generate-instructions.sh
file.10.verdict=reviewed
file.11.path=.specify/shared/definitions/self-explanatory-definitions.md
file.11.verdict=reviewed
file.12.path=.specify/shared/guidelines/self-explanatory.md
file.12.verdict=reviewed
file.13.path=.specify/shared/workflow/best-practice-optimization.md
file.13.verdict=reviewed
file.14.path=.specify/skills/internal/manage-constitution/SKILL.md
file.14.verdict=reviewed
file.15.path=.specify/skills/sdd-loop-driver/SKILL.md
file.15.verdict=reviewed
file.16.path=.specify/skills/sdd-loop-driver/references/efficiency-model.md
file.16.verdict=reviewed
file.17.path=.specify/skills/sdd-loop-driver/scripts/admission-check.py
file.17.verdict=reviewed
file.18.path=.specify/skills/sdd-loop-driver/scripts/decomposition-check.py
file.18.verdict=reviewed
file.19.path=.specify/specs/082-self-explanatory-integration/baseline-failed.txt
file.19.verdict=reviewed
file.20.path=.specify/specs/082-self-explanatory-integration/checklists/requirements-quality-20261105.md
file.20.verdict=reviewed
file.21.path=.specify/specs/082-self-explanatory-integration/checklists/requirements.md
file.21.verdict=reviewed
file.22.path=.specify/specs/082-self-explanatory-integration/coverage-baseline.txt
file.22.verdict=reviewed
file.23.path=.specify/specs/082-self-explanatory-integration/notes/pre-change-measurements.md
file.23.verdict=reviewed
file.24.path=.specify/specs/082-self-explanatory-integration/notes/quickstart-run.md
file.24.verdict=reviewed
file.25.path=.specify/specs/082-self-explanatory-integration/notes/red-first-evidence.md
file.25.verdict=reviewed
file.26.path=.specify/specs/082-self-explanatory-integration/requirements.md
file.26.verdict=reviewed
file.27.path=.specify/specs/082-self-explanatory-integration/tasks.md
file.27.verdict=reviewed
file.28.path=.specify/specs/082-self-explanatory-integration/test-evidence/analyze-stage-checks.md
file.28.verdict=reviewed
file.29.path=.specify/specs/082-self-explanatory-integration/test-evidence/checklist-stage-checks.md
file.29.verdict=reviewed
file.30.path=.specify/specs/082-self-explanatory-integration/test-evidence/implement-part-10a.md
file.30.verdict=reviewed
file.31.path=.specify/specs/082-self-explanatory-integration/test-evidence/implement-part-10b.md
file.31.verdict=reviewed
file.32.path=.specify/specs/082-self-explanatory-integration/test-evidence/implement-part-2.md
file.32.verdict=reviewed
file.33.path=.specify/specs/082-self-explanatory-integration/test-evidence/implement-part-3.md
file.33.verdict=reviewed
file.34.path=.specify/specs/082-self-explanatory-integration/test-evidence/implement-part-4.md
file.34.verdict=reviewed
file.35.path=.specify/specs/082-self-explanatory-integration/test-evidence/implement-part-5.md
file.35.verdict=reviewed
file.36.path=.specify/specs/082-self-explanatory-integration/test-evidence/implement-part-6.md
file.36.verdict=reviewed
file.37.path=.specify/specs/082-self-explanatory-integration/test-evidence/implement-part-7.md
file.37.verdict=reviewed
file.38.path=.specify/specs/082-self-explanatory-integration/test-evidence/implement-part-8.md
file.38.verdict=reviewed
file.39.path=.specify/specs/082-self-explanatory-integration/test-evidence/implement-part-9.md
file.39.verdict=reviewed
file.40.path=.specify/specs/082-self-explanatory-integration/test-evidence/smoke-20261105.txt
file.40.verdict=reviewed
file.41.path=.specify/specs/082-self-explanatory-integration/test-evidence/tasks-stage-premises.md
file.41.verdict=reviewed
file.42.path=.specify/specs/082-self-explanatory-integration/verification.md
file.42.verdict=reviewed
file.43.path=.specify/state/082-self-explanatory-integration.md
file.43.verdict=reviewed
file.44.path=.specify/templates/constitution-template.md
file.44.verdict=reviewed
file.45.path=.specify/templates/instructions-template.md
file.45.verdict=reviewed
file.46.path=docs/concepts/self-explanatory.md
file.46.verdict=reviewed
file.47.path=docs/reference/skills/sdd-loop-driver.md
file.47.verdict=reviewed
file.48.path=scripts/bash/generate-instructions.sh
file.48.verdict=reviewed
file.49.path=shared/definitions/self-explanatory-definitions.md
file.49.verdict=reviewed
file.50.path=shared/guidelines/self-explanatory.md
file.50.verdict=reviewed
file.51.path=shared/workflow/best-practice-optimization.md
file.51.verdict=reviewed
file.52.path=skills/external/sdd-loop-driver/SKILL.md
file.52.verdict=reviewed
file.53.path=skills/external/sdd-loop-driver/references/efficiency-model.md
file.53.verdict=reviewed
file.54.path=skills/external/sdd-loop-driver/scripts/admission-check.py
file.54.verdict=reviewed
file.55.path=skills/external/sdd-loop-driver/scripts/decomposition-check.py
file.55.verdict=reviewed
file.56.path=skills/internal/manage-constitution/SKILL.md
file.56.verdict=reviewed
file.57.path=templates/constitution-template.md
file.57.verdict=reviewed
file.58.path=templates/instructions-template.md
file.58.verdict=reviewed
file.59.path=tests/contract/test_constitution_double_landing.py
file.59.verdict=reviewed
file.60.path=tests/contract/test_fast_fail_discipline.py
file.60.verdict=reviewed
file.61.path=tests/contract/test_instructions_section_propagation.py
file.61.verdict=reviewed
file.62.path=tests/contract/test_instructions_size_budget.py
file.62.verdict=reviewed
file.63.path=tests/contract/test_sdd_loop_driver_efficiency.py
file.63.verdict=reviewed
file.64.path=tests/contract/test_sdd_loop_driver_gates.py
file.64.verdict=reviewed
file.65.path=tests/contract/test_self_explanatory_constitution.py
file.65.verdict=reviewed
file.66.path=tests/contract/test_self_explanatory_distribution.py
file.66.verdict=reviewed
file.67.path=tests/contract/test_self_explanatory_glossary.py
file.67.verdict=reviewed
file.68.path=tests/unit/test_decomposition_check.py
file.68.verdict=reviewed
file.69.path=tests/unit/test_pre_analyze_check.py
file.69.verdict=reviewed
<!-- coverage-receipt:end -->
