# Code Review Report — 代码段 (code segment)

| 属性 | 值 |
|------|-----|
| **分支** | `078-bilingual-expression` |
| **基准** | `7c835ba60705bf30f82bffa1cde50d845a015ccc` (`7c835ba6`) |
| **目标** | `04b32f87bc7adcd555bf4dc0a73701d9413fd5f6` (`04b32f87`) |
| **基准来源** | `feature-first-commit` |
| **渲染模式** | `renderer: text` |
| **Reviewer** | `Qiming Liu (John)` |
| **日期** | `2026-10-30T11:51:42Z` |

## 变更概览

```
 .specify/instructions.md                           |    5 +-
 .specify/memory/features.md                        |    3 +-
 .specify/memory/features/078.md                    |   27 +
 .specify/memory/register.md                        |    5 +
 .../scripts/python/bilingual-expression-check.py   |  627 ++++++++++++
 .specify/shared/guidelines/bilingual-expression.md |  113 +++
 .../078-bilingual-expression/baseline-failed.txt   |   21 +
 .../checklists/bilingual-convention-2026-10-30.md  |   77 ++
 .../checklists/requirements.md                     |   39 +
 .../078-bilingual-expression/contracts/checker.md  |   38 +
 .../contracts/distribution.md                      |   27 +
 .../contracts/measurement.md                       |   32 +
 .../contracts/owner-document.md                    |   34 +
 .../078-bilingual-expression/coverage-baseline.txt |  497 +++++++++
 .../specs/078-bilingual-expression/data-model.md   |   64 ++
 .../specs/078-bilingual-expression/feature-ref.md  |   44 +
 .../notes/pre-change-measurements.md               |   35 +
 .../notes/quickstart-run.md                        |   85 ++
 .../notes/red-first-evidence.md                    |   18 +
 .specify/specs/078-bilingual-expression/plan.md    |  236 +++++
 .../specs/078-bilingual-expression/quickstart.md   |   64 ++
 .../specs/078-bilingual-expression/requirements.md |  229 +++++
 .../specs/078-bilingual-expression/research.md     |   83 ++
 .specify/specs/078-bilingual-expression/tasks.md   |  303 ++++++
 .../checklist-doc-consistency-duplicate.txt        |    6 +
 .../checklist-doc-consistency-reader.txt           |    6 +
 .../test-evidence/checklist.jsonl                  |    1 +
 .../test-evidence/clarify.jsonl                    |    1 +
 .../test-evidence/implement-part1-gates.txt        |   74 ++
 .../test-evidence/implement-part1.jsonl            |    1 +
 .../test-evidence/implement-part2-gates.txt        |  108 ++
 .../test-evidence/implement-part2.jsonl            |    1 +
 .../test-evidence/implement-part3-gates.txt        |   42 +
 .../test-evidence/implement-part3.jsonl            |    1 +
 .../test-evidence/implement-part4-gates.txt        |   53 +
 .../test-evidence/implement-part4.jsonl            |    1 +
 .../test-evidence/plan-account-clause-coverage.txt |  595 +++++++++++
 .../test-evidence/plan-clause-extract.txt          |   40 +
 .../test-evidence/plan-decision-tensions.txt       |   12 +
 .../plan-docs-utils-validate-baseline.txt          |   24 +
 .../plan-docs-utils-validate-postedit.txt          |   25 +
 .../test-evidence/plan-pre-analyze-check.txt       |    3 +
 .../test-evidence/plan-scan-confirmation-gates.txt |    4 +
 .../test-evidence/plan-structure-judgement.txt     |   14 +
 .../test-evidence/plan-sync-mirrors-baseline.txt   |    7 +
 .../test-evidence/plan.jsonl                       |    1 +
 .../test-evidence/s4-pilot-pipeline-smoke.txt      |   52 +
 .../tasks-account-clause-coverage.txt              | 1055 ++++++++++++++++++++
 .../test-evidence/tasks-decomposition-check.txt    |    9 +
 .../tasks-doc-consistency-evidence.txt             |   17 +
 .../test-evidence/tasks-pre-analyze-check.txt      |   11 +
 .../test-evidence/tasks-validate-tasks.txt         |   11 +
 .../test-evidence/tasks.jsonl                      |    1 +
 .../test-evidence/us10-e6-legacy-divergence.txt    |  734 ++++++++++++++
 .../test-evidence/us10-sc002-changed-scope.txt     |   55 +
 .../test-evidence/us11-review-sample.txt           |   26 +
 .../test-evidence/us12-instructions-refresh.txt    |   58 ++
 .../test-evidence/us13-sc003-pilot.txt             |   11 +
 .../test-evidence/us14-sc004-diff-audit.txt        |   44 +
 .../test-evidence/us15-census-controlled.txt       |   39 +
 .../test-evidence/us16-register-check.txt          |   25 +
 .../test-evidence/us17-drift-guard-green.txt       |    6 +
 .../test-evidence/us2-census-denominator.txt       |   32 +
 .../test-evidence/us2-glossary-drill.txt           |   42 +
 .../test-evidence/us3-ambient-template-check.txt   |   33 +
 .../test-evidence/us8-distribution-after.txt       |   19 +
 .../test-evidence/us9-sc001-keyword-snapshot.txt   |   34 +
 .../specs/078-bilingual-expression/verification.md |   93 ++
 .specify/specs/078-bilingual-expression/waivers.md |   65 ++
 .specify/templates/instructions-template.md        |    4 +
 scripts/python/bilingual-expression-check.py       |  627 ++++++++++++
 shared/guidelines/bilingual-expression.md          |  113 +++
 templates/instructions-template.md                 |    4 +
 tests/contract/test_bilingual_expression.py        |  411 ++++++++
 tests/fixtures/bilingual/compliant-definition.md   |    9 +
 tests/fixtures/bilingual/fullwidth-definition.md   |    3 +
 .../fixtures/bilingual/same-language-definition.md |    3 +
 77 files changed, 7370 insertions(+), 2 deletions(-)
```

---

## Review 意见


### 🟠 [IMPORTANT] scripts/python/bilingual-expression-check.py (Line 320)

> S1 词汇表解析缺口：header_re '^\|\s*Canonical\s*\|' 先命中词汇表文件前面的 Column Definitions 行（'| Canonical | The agreed project term ... |'，2 列），in_table=True 后在 '## Glossary' 处 break，真正的 5 列词条表从未进入判定——missing-bilingual 的机械落点对真实词汇表整体失效。实测：scan --path .specify/memory/glossary.md rc=0，但 :48 '工作项四态色板' 与 :52 'qwen3 系列模型 ID' 均为含 CJK 无括号 Canonical，按 owner 文档机械边界应判 missing-bilingual。契约测试只经 census（独立 parser）触碰真词汇表，scan 动作无真实词汇表形状的覆盖，红先行未捕获。本轮修复（review 阶段内）：header 判定要求 >=5 列 + 新增契约腿钉住该形状。

<sub>19:53:30</sub>


### 🟢 [SUGGESTION] scripts/python/bilingual-expression-check.py (Line 71)

> 半角松括号形态（词条与 '(' 之间有空格，如词汇表 '程序优先 (Program-First)'）不被任何机械判定评估：judge_segments 只对全角紧贴判 red、对半角同脚本判 red；唯一形态条款的'紧贴'要求对此形态无机械落点，码封闭四值也无对应码。补判须先修订 contracts/checker.md 的封闭码集（本特性纪律：封闭集增删只能经 owner/契约修订），故仅登记为未来契约修订候选，不在本轮扩码。

<sub>19:53:30</sub>


### 👍 [PRAISE] tests/contract/test_bilingual_expression.py

> 漂移守卫三腿设计扎实：镜像路径从 sync-mirrors.py MIRROR_PAIRS 派生而非硬编码；STR 字面量消费点白名单覆盖框架源+镜像+夹具；ambient 小节'摘要+指针'形态用程序派生关键词表验证零枚举泄漏。红先行四字段齐备，与宪法 IV 一致。

<sub>19:53:30</sub>


> **未提交范围（未评审）**: 24 个未提交路径未计入本次评审对象（.specify/memory/glossary.md, .specify/memory/exec-quant/records/20261030T083918790503Z-f8939806.json, .specify/memory/exec-quant/records/20261030T085107907633Z-a7bab550.json, .specify/memory/exec-quant/records/20261030T092645260580Z-5971aa00.json, .specify/memory/exec-quant/records/20261030T094938860069Z-de43de63.json, .specify/memory/exec-quant/records/20261030T095702898652Z-99db466a.json, .specify/memory/exec-quant/records/20261030T100808443372Z-d2dde88a.json, .specify/memory/exec-quant/records/20261030T102951042752Z-d9a89927.json, .specify/memory/feedback/20261030T083930Z-speckit-requirements.md, .specify/memory/feedback/20261030T085125Z-speckit-clarify.md, .specify/memory/feedback/20261030T092645Z-speckit-plan.md, .specify/memory/feedback/20261030T095006Z-speckit-tasks.md, .specify/memory/feedback/20261030T095742Z-speckit-checklist.md, .specify/memory/feedback/20261030T100808Z-speckit-analyze.md, .specify/memory/feedback/20261030T103034Z-speckit-implement.md, .specify/memory/session/20261030T083906Z-run-determination-speckit-requirements-r20261030t081645z-078.md, .specify/memory/session/20261030T085107Z-run-determination-speckit-clarify-r20261030t081645z-078a.md, .specify/memory/session/20261030T092629Z-run-determination-speckit-plan-r20261030t081645z-078a.md, .specify/memory/session/20261030T094953Z-run-determination-speckit-tasks-r20261030t081645z-078a.md, .specify/memory/session/20261030T095733Z-run-determination-speckit-checklist-r20261030t081645z-078a.md, .specify/memory/session/20261030T100757Z-run-determination-speckit-analyze-r20261030t081645z-078a.md, .specify/memory/session/20261030T102937Z-run-determination-speckit-implement-r20261030t081645z-078a.md, .specify/memory/todo/, .specify/state/078-bilingual-expression.md）；本回执不对该范围给出任何结论。

<!-- coverage-receipt:begin -->
receipt_version=1
base=7c835ba60705bf30f82bffa1cde50d845a015ccc
head=04b32f87bc7adcd555bf4dc0a73701d9413fd5f6
base_source=explicit
renderer=text
changed_files=77
judged_files=77
skipped_files=0
gap_files=0
lines_added=7370
lines_deleted=2
file.01.path=.specify/instructions.md
file.01.verdict=reviewed
file.02.path=.specify/memory/features.md
file.02.verdict=reviewed
file.03.path=.specify/memory/features/078.md
file.03.verdict=reviewed
file.04.path=.specify/memory/register.md
file.04.verdict=reviewed
file.05.path=.specify/scripts/python/bilingual-expression-check.py
file.05.verdict=reviewed
file.06.path=.specify/shared/guidelines/bilingual-expression.md
file.06.verdict=reviewed
file.07.path=.specify/specs/078-bilingual-expression/baseline-failed.txt
file.07.verdict=reviewed
file.08.path=.specify/specs/078-bilingual-expression/checklists/bilingual-convention-2026-10-30.md
file.08.verdict=reviewed
file.09.path=.specify/specs/078-bilingual-expression/checklists/requirements.md
file.09.verdict=reviewed
file.10.path=.specify/specs/078-bilingual-expression/contracts/checker.md
file.10.verdict=reviewed
file.11.path=.specify/specs/078-bilingual-expression/contracts/distribution.md
file.11.verdict=reviewed
file.12.path=.specify/specs/078-bilingual-expression/contracts/measurement.md
file.12.verdict=reviewed
file.13.path=.specify/specs/078-bilingual-expression/contracts/owner-document.md
file.13.verdict=reviewed
file.14.path=.specify/specs/078-bilingual-expression/coverage-baseline.txt
file.14.verdict=reviewed
file.15.path=.specify/specs/078-bilingual-expression/data-model.md
file.15.verdict=reviewed
file.16.path=.specify/specs/078-bilingual-expression/feature-ref.md
file.16.verdict=reviewed
file.17.path=.specify/specs/078-bilingual-expression/notes/pre-change-measurements.md
file.17.verdict=reviewed
file.18.path=.specify/specs/078-bilingual-expression/notes/quickstart-run.md
file.18.verdict=reviewed
file.19.path=.specify/specs/078-bilingual-expression/notes/red-first-evidence.md
file.19.verdict=reviewed
file.20.path=.specify/specs/078-bilingual-expression/plan.md
file.20.verdict=reviewed
file.21.path=.specify/specs/078-bilingual-expression/quickstart.md
file.21.verdict=reviewed
file.22.path=.specify/specs/078-bilingual-expression/requirements.md
file.22.verdict=reviewed
file.23.path=.specify/specs/078-bilingual-expression/research.md
file.23.verdict=reviewed
file.24.path=.specify/specs/078-bilingual-expression/tasks.md
file.24.verdict=reviewed
file.25.path=.specify/specs/078-bilingual-expression/test-evidence/checklist-doc-consistency-duplicate.txt
file.25.verdict=reviewed
file.26.path=.specify/specs/078-bilingual-expression/test-evidence/checklist-doc-consistency-reader.txt
file.26.verdict=reviewed
file.27.path=.specify/specs/078-bilingual-expression/test-evidence/checklist.jsonl
file.27.verdict=reviewed
file.28.path=.specify/specs/078-bilingual-expression/test-evidence/clarify.jsonl
file.28.verdict=reviewed
file.29.path=.specify/specs/078-bilingual-expression/test-evidence/implement-part1-gates.txt
file.29.verdict=reviewed
file.30.path=.specify/specs/078-bilingual-expression/test-evidence/implement-part1.jsonl
file.30.verdict=reviewed
file.31.path=.specify/specs/078-bilingual-expression/test-evidence/implement-part2-gates.txt
file.31.verdict=reviewed
file.32.path=.specify/specs/078-bilingual-expression/test-evidence/implement-part2.jsonl
file.32.verdict=reviewed
file.33.path=.specify/specs/078-bilingual-expression/test-evidence/implement-part3-gates.txt
file.33.verdict=reviewed
file.34.path=.specify/specs/078-bilingual-expression/test-evidence/implement-part3.jsonl
file.34.verdict=reviewed
file.35.path=.specify/specs/078-bilingual-expression/test-evidence/implement-part4-gates.txt
file.35.verdict=reviewed
file.36.path=.specify/specs/078-bilingual-expression/test-evidence/implement-part4.jsonl
file.36.verdict=reviewed
file.37.path=.specify/specs/078-bilingual-expression/test-evidence/plan-account-clause-coverage.txt
file.37.verdict=reviewed
file.38.path=.specify/specs/078-bilingual-expression/test-evidence/plan-clause-extract.txt
file.38.verdict=reviewed
file.39.path=.specify/specs/078-bilingual-expression/test-evidence/plan-decision-tensions.txt
file.39.verdict=reviewed
file.40.path=.specify/specs/078-bilingual-expression/test-evidence/plan-docs-utils-validate-baseline.txt
file.40.verdict=reviewed
file.41.path=.specify/specs/078-bilingual-expression/test-evidence/plan-docs-utils-validate-postedit.txt
file.41.verdict=reviewed
file.42.path=.specify/specs/078-bilingual-expression/test-evidence/plan-pre-analyze-check.txt
file.42.verdict=reviewed
file.43.path=.specify/specs/078-bilingual-expression/test-evidence/plan-scan-confirmation-gates.txt
file.43.verdict=reviewed
file.44.path=.specify/specs/078-bilingual-expression/test-evidence/plan-structure-judgement.txt
file.44.verdict=reviewed
file.45.path=.specify/specs/078-bilingual-expression/test-evidence/plan-sync-mirrors-baseline.txt
file.45.verdict=reviewed
file.46.path=.specify/specs/078-bilingual-expression/test-evidence/plan.jsonl
file.46.verdict=reviewed
file.47.path=.specify/specs/078-bilingual-expression/test-evidence/s4-pilot-pipeline-smoke.txt
file.47.verdict=reviewed
file.48.path=.specify/specs/078-bilingual-expression/test-evidence/tasks-account-clause-coverage.txt
file.48.verdict=reviewed
file.49.path=.specify/specs/078-bilingual-expression/test-evidence/tasks-decomposition-check.txt
file.49.verdict=reviewed
file.50.path=.specify/specs/078-bilingual-expression/test-evidence/tasks-doc-consistency-evidence.txt
file.50.verdict=reviewed
file.51.path=.specify/specs/078-bilingual-expression/test-evidence/tasks-pre-analyze-check.txt
file.51.verdict=reviewed
file.52.path=.specify/specs/078-bilingual-expression/test-evidence/tasks-validate-tasks.txt
file.52.verdict=reviewed
file.53.path=.specify/specs/078-bilingual-expression/test-evidence/tasks.jsonl
file.53.verdict=reviewed
file.54.path=.specify/specs/078-bilingual-expression/test-evidence/us10-e6-legacy-divergence.txt
file.54.verdict=reviewed
file.55.path=.specify/specs/078-bilingual-expression/test-evidence/us10-sc002-changed-scope.txt
file.55.verdict=reviewed
file.56.path=.specify/specs/078-bilingual-expression/test-evidence/us11-review-sample.txt
file.56.verdict=reviewed
file.57.path=.specify/specs/078-bilingual-expression/test-evidence/us12-instructions-refresh.txt
file.57.verdict=reviewed
file.58.path=.specify/specs/078-bilingual-expression/test-evidence/us13-sc003-pilot.txt
file.58.verdict=reviewed
file.59.path=.specify/specs/078-bilingual-expression/test-evidence/us14-sc004-diff-audit.txt
file.59.verdict=reviewed
file.60.path=.specify/specs/078-bilingual-expression/test-evidence/us15-census-controlled.txt
file.60.verdict=reviewed
file.61.path=.specify/specs/078-bilingual-expression/test-evidence/us16-register-check.txt
file.61.verdict=reviewed
file.62.path=.specify/specs/078-bilingual-expression/test-evidence/us17-drift-guard-green.txt
file.62.verdict=reviewed
file.63.path=.specify/specs/078-bilingual-expression/test-evidence/us2-census-denominator.txt
file.63.verdict=reviewed
file.64.path=.specify/specs/078-bilingual-expression/test-evidence/us2-glossary-drill.txt
file.64.verdict=reviewed
file.65.path=.specify/specs/078-bilingual-expression/test-evidence/us3-ambient-template-check.txt
file.65.verdict=reviewed
file.66.path=.specify/specs/078-bilingual-expression/test-evidence/us8-distribution-after.txt
file.66.verdict=reviewed
file.67.path=.specify/specs/078-bilingual-expression/test-evidence/us9-sc001-keyword-snapshot.txt
file.67.verdict=reviewed
file.68.path=.specify/specs/078-bilingual-expression/verification.md
file.68.verdict=reviewed
file.69.path=.specify/specs/078-bilingual-expression/waivers.md
file.69.verdict=reviewed
file.70.path=.specify/templates/instructions-template.md
file.70.verdict=reviewed
file.71.path=scripts/python/bilingual-expression-check.py
file.71.verdict=reviewed
file.72.path=shared/guidelines/bilingual-expression.md
file.72.verdict=reviewed
file.73.path=templates/instructions-template.md
file.73.verdict=reviewed
file.74.path=tests/contract/test_bilingual_expression.py
file.74.verdict=reviewed
file.75.path=tests/fixtures/bilingual/compliant-definition.md
file.75.verdict=reviewed
file.76.path=tests/fixtures/bilingual/fullwidth-definition.md
file.76.verdict=reviewed
file.77.path=tests/fixtures/bilingual/same-language-definition.md
file.77.verdict=reviewed
<!-- coverage-receipt:end -->
