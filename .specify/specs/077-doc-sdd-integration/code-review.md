# Code Review Report — 代码段 (code segment)

| 属性 | 值 |
|------|-----|
| **分支** | `077-doc-sdd-integration` |
| **基准** | `c1cd46002db62a1565c4ab0a23178e9fe7f149ef` (`c1cd4600`) |
| **目标** | `794a7f2b285289e125da514f84b18f40835fb52f` (`794a7f2b`) |
| **基准来源** | `feature-first-commit` |
| **渲染模式** | `renderer: text` |
| **Reviewer** | `Qiming, Liu` |
| **日期** | `2026-10-29T19:55:59Z` |

## 变更概览

```
 .claude/commands/speckit.analyze.md                |    8 +
 .claude/commands/speckit.checklist.md              |    8 +
 .claude/commands/speckit.clarify.md                |    8 +
 .claude/commands/speckit.implement.md              |    8 +
 .claude/commands/speckit.plan.md                   |    8 +
 .claude/commands/speckit.requirements.md           |   10 +
 .claude/commands/speckit.tasks.md                  |    8 +
 .github/prompts/speckit.analyze.prompt.md          |    8 +
 .github/prompts/speckit.checklist.prompt.md        |    8 +
 .github/prompts/speckit.clarify.prompt.md          |    8 +
 .github/prompts/speckit.implement.prompt.md        |    8 +
 .github/prompts/speckit.plan.prompt.md             |    8 +
 .github/prompts/speckit.requirements.prompt.md     |   10 +
 .github/prompts/speckit.tasks.prompt.md            |    8 +
 .opencode/command/speckit.analyze.md               |    8 +
 .opencode/command/speckit.checklist.md             |    8 +
 .opencode/command/speckit.clarify.md               |    8 +
 .opencode/command/speckit.implement.md             |    8 +
 .opencode/command/speckit.plan.md                  |    8 +
 .opencode/command/speckit.requirements.md          |   10 +
 .opencode/command/speckit.tasks.md                 |    8 +
 .qoder/commands/speckit.analyze.md                 |    8 +
 .qoder/commands/speckit.checklist.md               |    8 +
 .qoder/commands/speckit.clarify.md                 |    8 +
 .qoder/commands/speckit.implement.md               |    8 +
 .qoder/commands/speckit.plan.md                    |    8 +
 .qoder/commands/speckit.requirements.md            |   10 +
 .qoder/commands/speckit.tasks.md                   |    8 +
 .../records/20261029T171000858951Z-ad4a4625.json   |    1 +
 .../records/20261029T171908361077Z-cc3b82c2.json   |    1 +
 .../records/20261029T173208404124Z-4ca01b03.json   |    1 +
 .../records/20261029T174143320900Z-8af20635.json   |    1 +
 .../records/20261029T175253931395Z-6ece5de4.json   |    1 +
 .../records/20261029T195020625181Z-26783fdb.json   |    1 +
 .specify/memory/features.md                        |    6 +-
 .specify/memory/features/077.md                    |   99 +
 .../20261029T171009Z-speckit-requirements.md       |   21 +
 .../feedback/20261029T171908Z-speckit-clarify.md   |   20 +
 .../feedback/20261029T173208Z-speckit-plan.md      |   20 +
 .../feedback/20261029T174153Z-speckit-tasks.md     |   21 +
 .../feedback/20261029T175254Z-speckit-checklist.md |   20 +
 .../feedback/20261029T195020Z-speckit-implement.md |   20 +
 ...n-speckit-tasks-r20261029t172918z-076a-tasks.md |   31 +-
 ...n-speckit-requirements-r20261030t010236z-077.md |  202 ++
 ...n-speckit-clarify-r20261030t010236z-077a-cla.md |  202 ++
 ...ion-speckit-plan-r20261030t010236z-077a-plan.md |  202 ++
 ...ination-speckit-tasks-r20261030t010236z-077a.md |  202 ++
 ...n-speckit-checklist-r20261030t010236z-077a-c.md |  202 ++
 ...n-speckit-implement-r20261030t010236z-077a-i.md |  202 ++
 .specify/scripts/python/doc-consistency-check.py   |  667 ++++++-
 .specify/scripts/python/flow-class-check.py        |  303 ++-
 .../shared/definitions/flow-class-definitions.md   |   10 +
 .specify/shared/workflow/expression-gates.md       |   18 +
 .specify/skills/sdd-loop-driver/SKILL.md           |    1 +
 .../sdd-loop-driver/references/efficiency-model.md |   21 +-
 .../sdd-loop-driver/references/stage-prompts.md    |   34 +
 .../077-doc-sdd-integration/baseline-failed.txt    |   39 +
 .../checklists/readiness-2026-10-30.md             |  269 +++
 .../checklists/requirements.md                     |   45 +
 .../contracts/class-declaration.md                 |   62 +
 .../contracts/class-resolution.md                  |   63 +
 .../contracts/document-structure.md                |  107 ++
 .../contracts/driver-integration.md                |   71 +
 .../contracts/invariants-and-distribution.md       |   43 +
 .../contracts/stage-wiring.md                      |   74 +
 .../077-doc-sdd-integration/coverage-baseline.txt  |  497 +++++
 .../specs/077-doc-sdd-integration/data-model.md    |  248 +++
 .../specs/077-doc-sdd-integration/feature-ref.md   |   65 +
 .../notes/pre-change-measurements.md               |   70 +
 .../notes/quickstart-run.md                        |  112 ++
 .../notes/red-first-evidence.md                    |  346 ++++
 .specify/specs/077-doc-sdd-integration/plan.md     |  255 +++
 .../specs/077-doc-sdd-integration/quickstart.md    |  171 ++
 .../specs/077-doc-sdd-integration/requirements.md  |  263 +++
 .specify/specs/077-doc-sdd-integration/research.md |  246 +++
 .specify/specs/077-doc-sdd-integration/tasks.md    |  344 ++++
 .../test-evidence/account-clause-coverage-fix1.txt |  531 ++++++
 .../test-evidence/account-clause-coverage-fix2.txt |  534 ++++++
 .../test-evidence/account-clause-coverage-fix3.txt |  534 ++++++
 .../test-evidence/checklist-stage-checks.md        |  224 +++
 .../test-evidence/clarify-pre-analyze-check.txt    |    3 +
 .../test-evidence/clarify-reader-face.txt          |    6 +
 .../clarify-validate-requirements.txt              |   10 +
 .../test-evidence/decomposition-check.json         |    1 +
 .../test-evidence/p1-t002-red.txt                  |  166 ++
 .../test-evidence/p1-t003-red.txt                  |  630 +++++++
 .../test-evidence/p1-t004-partial-green.txt        |   10 +
 .../test-evidence/p1-t005-partial-green.txt        |   13 +
 .../test-evidence/p1-t006-partial-green.txt        |   14 +
 .../test-evidence/p1-t007-green.txt                |   24 +
 .../test-evidence/p2-t009-red.txt                  | 1985 ++++++++++++++++++++
 .../test-evidence/p2-t009-t015-green.txt           |    3 +
 .../test-evidence/p2-t013-red.txt                  |  447 +++++
 .../test-evidence/p2-t015-green.txt                |    2 +
 .../test-evidence/p3-t016-red.txt                  |  718 +++++++
 .../test-evidence/p3-t016-t020-green.txt           |   44 +
 .../test-evidence/plan-a6-mutation-probe.txt       |   18 +
 .../test-evidence/plan-account-clause-coverage.txt | 1176 ++++++++++++
 .../plan-audit-test-budget-docs-gate-probe.txt     |   29 +
 .../test-evidence/plan-clause-extract.txt          |   84 +
 .../test-evidence/plan-decision-tensions.txt       |   14 +
 .../test-evidence/plan-distribution-postcheck.txt  |   12 +
 .../test-evidence/plan-pre-analyze-check.txt       |    5 +
 .../plan-regen-command-copies-baseline.txt         |    2 +
 .../test-evidence/plan-resolution-baseline.txt     |   28 +
 .../test-evidence/plan-scan-confirmation-gates.txt |    6 +
 .../test-evidence/plan-stage-template-zero-hit.txt |   15 +
 .../test-evidence/plan-sync-mirrors-baseline.txt   |    8 +
 .../test-evidence/plan-targeted-tests-baseline.txt |   16 +
 .../test-evidence/pre-analyze-check.txt            |    1 +
 .../test-evidence/pre-analyze-tasks-fix1.txt       |    9 +
 .../test-evidence/pre-analyze-tasks-fix2.txt       |   12 +
 .../test-evidence/pre-analyze-tasks-fix3.txt       |   12 +
 .../test-evidence/r01-na-arithmetic-fix2.txt       |  118 ++
 .../test-evidence/regen-command-copies-fix1.txt    |    8 +
 .../test-evidence/regen-command-copies-fix2.txt    |   11 +
 .../test-evidence/regen-command-copies-fix3.txt    |   11 +
 .../test-evidence/sync-mirrors-check-after.txt     |   20 +
 .../test-evidence/sync-mirrors-fix1.txt            |   14 +
 .../test-evidence/sync-mirrors-fix2.txt            |   17 +
 .../test-evidence/sync-mirrors-fix3.txt            |   17 +
 .../test-evidence/tasks-069-invariants.txt         |   65 +
 .../tasks-account-clause-coverage-final.txt        |  528 ++++++
 .../tasks-account-clause-coverage.txt              |  529 ++++++
 .../test-evidence/tasks-closing-suites.txt         |    8 +
 .../tasks-decomposition-check-final.txt            |    5 +
 .../test-evidence/tasks-decomposition-check.txt    |    4 +
 .../test-evidence/tasks-distribution-after.txt     |   40 +
 .../test-evidence/tasks-distribution-two-state.txt |  184 ++
 .../test-evidence/tasks-ledger-boundary.txt        |   16 +
 .../test-evidence/tasks-owner-append-delta.txt     |   64 +
 .../test-evidence/tasks-plan-template-skeleton.txt |   90 +
 .../tasks-pre-analyze-check-final.txt              |    6 +
 .../test-evidence/tasks-pre-analyze-check.txt      |    5 +
 .../test-evidence/tasks-quickstart-s1-s7.txt       |  260 +++
 .../test-evidence/tasks-scope-set-difference.txt   |   55 +
 .../test-evidence/tasks-stage-integrity.txt        |   10 +
 .../test-evidence/tasks-validate-tasks-final.txt   |    5 +
 .../test-evidence/tasks-validate-tasks.txt         |   13 +
 .../validate-decision-tensions-fix1.txt            |   18 +
 .../validate-decision-tensions-fix2.txt            |   21 +
 .../validate-decision-tensions-fix3.txt            |   21 +
 .../test-evidence/validate-requirements-fix1.txt   |   16 +
 .../test-evidence/validate-requirements-fix2.txt   |   19 +
 .../test-evidence/validate-requirements-fix3.txt   |   19 +
 .../test-evidence/validate-requirements.txt        |    9 +
 .../test-evidence/validate-tasks-fix1.txt          |    8 +
 .../test-evidence/validate-tasks-fix2.txt          |   11 +
 .../test-evidence/validate-tasks-fix3.txt          |   11 +
 .../test-evidence/zero-new-mechanism.txt           |   15 +
 .../specs/077-doc-sdd-integration/verification.md  |  112 ++
 .specify/state/077-doc-sdd-integration.md          |  178 ++
 .specify/templates/plan-template.md                |   61 +
 .specify/templates/requirements-template.md        |    2 +
 scripts/python/doc-consistency-check.py            |  667 ++++++-
 scripts/python/flow-class-check.py                 |  303 ++-
 shared/definitions/flow-class-definitions.md       |   10 +
 shared/workflow/expression-gates.md                |   18 +
 skills/external/sdd-loop-driver/SKILL.md           |    1 +
 .../sdd-loop-driver/references/efficiency-model.md |   21 +-
 .../sdd-loop-driver/references/stage-prompts.md    |   34 +
 templates/commands/analyze.md                      |    8 +
 templates/commands/checklist.md                    |    8 +
 templates/commands/clarify.md                      |    8 +
 templates/commands/implement.md                    |    8 +
 templates/commands/plan.md                         |    8 +
 templates/commands/requirements.md                 |   10 +
 templates/commands/tasks.md                        |    8 +
 templates/plan-template.md                         |   61 +
 templates/requirements-template.md                 |    2 +
 tests/contract/test_docs_gate_driver.py            |  495 +++++
 tests/contract/test_document_structure_gate.py     |  720 +++++++
 tests/contract/test_expression_compatibility.py    |   28 +-
 tests/contract/test_expression_gate_wiring.py      |   27 +-
 tests/contract/test_flow_class_spec_declaration.py |  458 +++++
 tests/contract/test_stage_class_wiring.py          |  432 +++++
 tests/unit/test_flow_class_spec_key.py             |  440 +++++
 177 files changed, 19830 insertions(+), 67 deletions(-)
```

---

## Review 意见


### 🟠 [IMPORTANT] scripts/python/flow-class-check.py (Line 917)

> 退出码 2 的标签是 `invalid-unit-id`，而七个阶段模板的接线子节与 contracts/class-resolution.md C-012 都把退出码 2 说成 `owner-unavailable`。实测：`lookup --unit-id spec:does-not-exist` → stderr `invalid-unit-id: spec input not found: .specify/specs/does-not-exist/requirements.md`、记录 `error.label: invalid-unit-id`、rc=2。后果：读者按接线子节「原样显示该标签」照抄得到 `invalid-unit-id`，而 references/stage-prompts.md 把派发载荷 `error` 的值域钉死为 `{owner-unavailable, -}`，U4(c) 只认「非 `-` ⇒ owner-unavailable 分支」——照抄标签的派发会产出值域外的键，U4 无分支可走。修法二选一：`spec_input_error` 记 `owner-unavailable` 并把原因放进 detail；或把载荷值域扩到 `{owner-unavailable, invalid-unit-id, -}` 并给卡片补第三条分支。

<sub>03:56:14</sub>


### 🟠 [IMPORTANT] scripts/python/flow-class-check.py (Line 910)

> C-003 写「spec 目录不存在时 MUST 退出码 2，且 MUST NOT 返回任何类别值」，但该路径实测返回 `flow_class: execution` + `source: default`（default_lookup_record 的降级形态），rc=2。C-007 的立论是「只看记录不看退出码的消费方不得看到已决类别」——同一立论在 exit 2 上失效：一个拼错的 spec 键会给消费方一个确定的 execution 判定。两条自洽读法（降级形态带默认类别 + error.label 区分 / 该路径 flow_class 写 null）必须择一并登记，现在的条文与实现各占一半。

<sub>03:56:14</sub>


### 🟠 [IMPORTANT] templates/plan-template.md (Line 179)

> `[[STR-002]] … [[STR-006]]` 只在本仓 077 的 requirements.md 里解析得到；STR id 是每个 spec 私有的命名空间（077 自己的规格里就注明 069 已占用 STR-003 / STR-004）。这份模板随 specify init 下发到每个项目，下游作者照这句话去自己 spec 的 § Shared Strings 找 STR-002..006，只会找到无关字面量或什么都找不到。可执行的 owner 其实同一段后半句已经给出（doc-consistency-check.py 的 STRUCTURE_HEADING / STRUCTURE_SUBSECTIONS / 三个 COLUMNS 常量）——建议删掉 [[STR-NNN]] 括号引用，只留常量名与「本模板是骨架产出方」。

<sub>03:56:14</sub>


### 🟢 [SUGGESTION] skills/external/sdd-loop-driver/references/stage-prompts.md (Line 25)

> `owner：contracts/driver-integration.md C-001…C-003` 是相对路径，只在 077 的 spec 目录里可解；同目录既有先例都带 spec 前缀（state-awareness.md 用 `.specify/specs/065a-state-awareness/contracts/…`，decomposition-model.md 用 `.specify/specs/070-subagent-task-teams/contracts/`）。补前缀即可保持一致且可解。

<sub>03:56:21</sub>


### 🟢 [SUGGESTION] scripts/python/doc-consistency-check.py (Line 1423)

> 降级（ verdict==2，如类别引擎缺席 / owner 不可解析）与真正的执行类共用 `status: not-applicable` 与退出码 0，两者只由 payload 的 `error` 位区分。文本模式能看到 error 行，但 `--format json` 且只看 status/rc 的消费方无法把「类别引擎不可用」与「本线是执行类」分开——正是 FR-009 要的「降级可见」在机器面上打了折。建议给降级一个独立 status 值（或让 rc 非 0），不新增面。

<sub>03:56:22</sub>


### 🟢 [SUGGESTION] templates/requirements-template.md (Line 6)

> 占位符 `[FLOW CLASS]` 含空格，原样保留即落进 DECLARATION_LINE_RE 失败 → `declaration-malformed` → 七个阶段都在门禁前 exit 1 停下（test_template_placeholder_does_not_prefill_a_class 已把「不预填封闭值」钉住，方向是对的）。但注释没写「不填即全阶段阻断」，而同一文件里其它占位符（`[###-requirement-name]`、`[DATE]`）不阻断任何东西——作者会合理推断它也可以留。建议注释补一句后果。

<sub>03:56:22</sub>


### 🟢 [SUGGESTION] scripts/python/doc-consistency-check.py (Line 1360)

> `any(needle in norm for needle in listed)` 是子串包含：证据清单里一条极短断言（如「兼容性」）会让任何带标注的正文行都被判「已列」。这是 fail-open 方向——C-014 要的是「每条标注断言都有证据行」，被吞掉的是缺证据的断言。建议等值或 token 边界匹配，至少在断言长度低于阈值时退化为等值。

<sub>03:56:22</sub>


### ⚪ [NITPICK] scripts/python/doc-consistency-check.py (Line 1418)

> `files_scanned = len(paths) + (1 if plan_path.is_file() else 0)` 在类别不是表达类、plan.md 从未被读取时也计 1（本次 `--action structure --spec-dir …077` 输出 `files_scanned: 1`，实际读的是 requirements.md 判类）。作为「检查了什么」的伴随量这是虚数，建议按实际读入的文件计。

<sub>03:56:22</sub>


### ⚪ [NITPICK] tests/contract/test_docs_gate_driver.py (Line 256)

> U4 一组断言多为「段落里出现『四项』/『表达类』/『blocking』字样」级别的存在性检查：把 U4 那一段整体改写成语义相反的文字，仍可能同时含这三个 token。_mentions 要求同段多 token 已强于单词 grep，但修饰语义（全部 blocking、四项各自独立）只靠词在场。建议给四条校验加 (a)…(d) 编号锚与否定词禁入断言。

<sub>03:56:22</sub>


### ❓ [QUESTION] scripts/python/flow-class-check.py (Line 954)

> `field_lines` 对整个文件扫描（含代码围栏与正文示例），重复计数与错位判定都基于它。一条表达类规格若在正文里演示声明行（文档型线做这件事很自然），会被判 `declaration-duplicate` → exit 1 阻断。C-004 说「只读计数、不管两值是否一致」，所以这可能是有意为之——请明确：围栏内的示例行算不算第二处声明？

<sub>03:56:22</sub>


### 👍 [PRAISE] tests/contract/test_stage_class_wiring.py (Line 393)

> 剥离守卫不是空绿：先断言块非空、再断言 stripped != text、最后才比 SHA-256 与基线提交；文件未接线与块被截空两种空转都挡在比较之前。这是「执行类零变化」这条最强主张能被机器核对的唯一形态，值得保留。

<sub>03:56:22</sub>


### 👍 [PRAISE] tests/contract/test_expression_compatibility.py (Line 527)

> 向既有 allow-list 登记七模板时同时登记了 markers，登记即被断言内容必须在场——白名单不会退化成静默放行；且 WIRING_TEMPLATES 与 POST_077_WIRING_TEMPLATES 分开，069a 的 25 模板冻结哈希腿仍按原语义读。

<sub>03:56:22</sub>


<!-- coverage-receipt:begin -->
receipt_version=1
base=c1cd46002db62a1565c4ab0a23178e9fe7f149ef
head=794a7f2b285289e125da514f84b18f40835fb52f
base_source=feature-first-commit
renderer=text
changed_files=177
judged_files=23
skipped_files=154
gap_files=0
lines_added=19830
lines_deleted=67
file.001.path=.claude/commands/speckit.analyze.md
file.001.verdict=skipped
file.001.reason=generated
file.002.path=.claude/commands/speckit.checklist.md
file.002.verdict=skipped
file.002.reason=generated
file.003.path=.claude/commands/speckit.clarify.md
file.003.verdict=skipped
file.003.reason=generated
file.004.path=.claude/commands/speckit.implement.md
file.004.verdict=skipped
file.004.reason=generated
file.005.path=.claude/commands/speckit.plan.md
file.005.verdict=skipped
file.005.reason=generated
file.006.path=.claude/commands/speckit.requirements.md
file.006.verdict=skipped
file.006.reason=generated
file.007.path=.claude/commands/speckit.tasks.md
file.007.verdict=skipped
file.007.reason=generated
file.008.path=.github/prompts/speckit.analyze.prompt.md
file.008.verdict=skipped
file.008.reason=generated
file.009.path=.github/prompts/speckit.checklist.prompt.md
file.009.verdict=skipped
file.009.reason=generated
file.010.path=.github/prompts/speckit.clarify.prompt.md
file.010.verdict=skipped
file.010.reason=generated
file.011.path=.github/prompts/speckit.implement.prompt.md
file.011.verdict=skipped
file.011.reason=generated
file.012.path=.github/prompts/speckit.plan.prompt.md
file.012.verdict=skipped
file.012.reason=generated
file.013.path=.github/prompts/speckit.requirements.prompt.md
file.013.verdict=skipped
file.013.reason=generated
file.014.path=.github/prompts/speckit.tasks.prompt.md
file.014.verdict=skipped
file.014.reason=generated
file.015.path=.opencode/command/speckit.analyze.md
file.015.verdict=skipped
file.015.reason=generated
file.016.path=.opencode/command/speckit.checklist.md
file.016.verdict=skipped
file.016.reason=generated
file.017.path=.opencode/command/speckit.clarify.md
file.017.verdict=skipped
file.017.reason=generated
file.018.path=.opencode/command/speckit.implement.md
file.018.verdict=skipped
file.018.reason=generated
file.019.path=.opencode/command/speckit.plan.md
file.019.verdict=skipped
file.019.reason=generated
file.020.path=.opencode/command/speckit.requirements.md
file.020.verdict=skipped
file.020.reason=generated
file.021.path=.opencode/command/speckit.tasks.md
file.021.verdict=skipped
file.021.reason=generated
file.022.path=.qoder/commands/speckit.analyze.md
file.022.verdict=skipped
file.022.reason=generated
file.023.path=.qoder/commands/speckit.checklist.md
file.023.verdict=skipped
file.023.reason=generated
file.024.path=.qoder/commands/speckit.clarify.md
file.024.verdict=skipped
file.024.reason=generated
file.025.path=.qoder/commands/speckit.implement.md
file.025.verdict=skipped
file.025.reason=generated
file.026.path=.qoder/commands/speckit.plan.md
file.026.verdict=skipped
file.026.reason=generated
file.027.path=.qoder/commands/speckit.requirements.md
file.027.verdict=skipped
file.027.reason=generated
file.028.path=.qoder/commands/speckit.tasks.md
file.028.verdict=skipped
file.028.reason=generated
file.029.path=.specify/memory/exec-quant/records/20261029T171000858951Z-ad4a4625.json
file.029.verdict=skipped
file.029.reason=non-code-file
file.030.path=.specify/memory/exec-quant/records/20261029T171908361077Z-cc3b82c2.json
file.030.verdict=skipped
file.030.reason=non-code-file
file.031.path=.specify/memory/exec-quant/records/20261029T173208404124Z-4ca01b03.json
file.031.verdict=skipped
file.031.reason=non-code-file
file.032.path=.specify/memory/exec-quant/records/20261029T174143320900Z-8af20635.json
file.032.verdict=skipped
file.032.reason=non-code-file
file.033.path=.specify/memory/exec-quant/records/20261029T175253931395Z-6ece5de4.json
file.033.verdict=skipped
file.033.reason=non-code-file
file.034.path=.specify/memory/exec-quant/records/20261029T195020625181Z-26783fdb.json
file.034.verdict=skipped
file.034.reason=non-code-file
file.035.path=.specify/memory/features.md
file.035.verdict=skipped
file.035.reason=non-code-file
file.036.path=.specify/memory/features/077.md
file.036.verdict=skipped
file.036.reason=non-code-file
file.037.path=.specify/memory/feedback/20261029T171009Z-speckit-requirements.md
file.037.verdict=skipped
file.037.reason=non-code-file
file.038.path=.specify/memory/feedback/20261029T171908Z-speckit-clarify.md
file.038.verdict=skipped
file.038.reason=non-code-file
file.039.path=.specify/memory/feedback/20261029T173208Z-speckit-plan.md
file.039.verdict=skipped
file.039.reason=non-code-file
file.040.path=.specify/memory/feedback/20261029T174153Z-speckit-tasks.md
file.040.verdict=skipped
file.040.reason=non-code-file
file.041.path=.specify/memory/feedback/20261029T175254Z-speckit-checklist.md
file.041.verdict=skipped
file.041.reason=non-code-file
file.042.path=.specify/memory/feedback/20261029T195020Z-speckit-implement.md
file.042.verdict=skipped
file.042.reason=non-code-file
file.043.path=.specify/memory/session/20261029T100933Z-run-determination-speckit-tasks-r20261029t172918z-076a-tasks.md
file.043.verdict=skipped
file.043.reason=non-code-file
file.044.path=.specify/memory/session/20261029T170958Z-run-determination-speckit-requirements-r20261030t010236z-077.md
file.044.verdict=skipped
file.044.reason=non-code-file
file.045.path=.specify/memory/session/20261029T171908Z-run-determination-speckit-clarify-r20261030t010236z-077a-cla.md
file.045.verdict=skipped
file.045.reason=non-code-file
file.046.path=.specify/memory/session/20261029T173208Z-run-determination-speckit-plan-r20261030t010236z-077a-plan.md
file.046.verdict=skipped
file.046.reason=non-code-file
file.047.path=.specify/memory/session/20261029T174139Z-run-determination-speckit-tasks-r20261030t010236z-077a.md
file.047.verdict=skipped
file.047.reason=non-code-file
file.048.path=.specify/memory/session/20261029T175253Z-run-determination-speckit-checklist-r20261030t010236z-077a-c.md
file.048.verdict=skipped
file.048.reason=non-code-file
file.049.path=.specify/memory/session/20261029T195020Z-run-determination-speckit-implement-r20261030t010236z-077a-i.md
file.049.verdict=skipped
file.049.reason=non-code-file
file.050.path=.specify/scripts/python/doc-consistency-check.py
file.050.verdict=skipped
file.050.reason=generated
file.051.path=.specify/scripts/python/flow-class-check.py
file.051.verdict=skipped
file.051.reason=generated
file.052.path=.specify/shared/definitions/flow-class-definitions.md
file.052.verdict=skipped
file.052.reason=generated
file.053.path=.specify/shared/workflow/expression-gates.md
file.053.verdict=skipped
file.053.reason=generated
file.054.path=.specify/skills/sdd-loop-driver/SKILL.md
file.054.verdict=skipped
file.054.reason=generated
file.055.path=.specify/skills/sdd-loop-driver/references/efficiency-model.md
file.055.verdict=skipped
file.055.reason=generated
file.056.path=.specify/skills/sdd-loop-driver/references/stage-prompts.md
file.056.verdict=skipped
file.056.reason=generated
file.057.path=.specify/specs/077-doc-sdd-integration/baseline-failed.txt
file.057.verdict=skipped
file.057.reason=non-code-file
file.058.path=.specify/specs/077-doc-sdd-integration/checklists/readiness-2026-10-30.md
file.058.verdict=skipped
file.058.reason=non-code-file
file.059.path=.specify/specs/077-doc-sdd-integration/checklists/requirements.md
file.059.verdict=skipped
file.059.reason=non-code-file
file.060.path=.specify/specs/077-doc-sdd-integration/contracts/class-declaration.md
file.060.verdict=skipped
file.060.reason=non-code-file
file.061.path=.specify/specs/077-doc-sdd-integration/contracts/class-resolution.md
file.061.verdict=skipped
file.061.reason=non-code-file
file.062.path=.specify/specs/077-doc-sdd-integration/contracts/document-structure.md
file.062.verdict=skipped
file.062.reason=non-code-file
file.063.path=.specify/specs/077-doc-sdd-integration/contracts/driver-integration.md
file.063.verdict=skipped
file.063.reason=non-code-file
file.064.path=.specify/specs/077-doc-sdd-integration/contracts/invariants-and-distribution.md
file.064.verdict=skipped
file.064.reason=non-code-file
file.065.path=.specify/specs/077-doc-sdd-integration/contracts/stage-wiring.md
file.065.verdict=skipped
file.065.reason=non-code-file
file.066.path=.specify/specs/077-doc-sdd-integration/coverage-baseline.txt
file.066.verdict=skipped
file.066.reason=non-code-file
file.067.path=.specify/specs/077-doc-sdd-integration/data-model.md
file.067.verdict=skipped
file.067.reason=non-code-file
file.068.path=.specify/specs/077-doc-sdd-integration/feature-ref.md
file.068.verdict=skipped
file.068.reason=non-code-file
file.069.path=.specify/specs/077-doc-sdd-integration/notes/pre-change-measurements.md
file.069.verdict=skipped
file.069.reason=non-code-file
file.070.path=.specify/specs/077-doc-sdd-integration/notes/quickstart-run.md
file.070.verdict=skipped
file.070.reason=non-code-file
file.071.path=.specify/specs/077-doc-sdd-integration/notes/red-first-evidence.md
file.071.verdict=skipped
file.071.reason=non-code-file
file.072.path=.specify/specs/077-doc-sdd-integration/plan.md
file.072.verdict=skipped
file.072.reason=non-code-file
file.073.path=.specify/specs/077-doc-sdd-integration/quickstart.md
file.073.verdict=skipped
file.073.reason=non-code-file
file.074.path=.specify/specs/077-doc-sdd-integration/requirements.md
file.074.verdict=skipped
file.074.reason=non-code-file
file.075.path=.specify/specs/077-doc-sdd-integration/research.md
file.075.verdict=skipped
file.075.reason=non-code-file
file.076.path=.specify/specs/077-doc-sdd-integration/tasks.md
file.076.verdict=skipped
file.076.reason=non-code-file
file.077.path=.specify/specs/077-doc-sdd-integration/test-evidence/account-clause-coverage-fix1.txt
file.077.verdict=skipped
file.077.reason=non-code-file
file.078.path=.specify/specs/077-doc-sdd-integration/test-evidence/account-clause-coverage-fix2.txt
file.078.verdict=skipped
file.078.reason=non-code-file
file.079.path=.specify/specs/077-doc-sdd-integration/test-evidence/account-clause-coverage-fix3.txt
file.079.verdict=skipped
file.079.reason=non-code-file
file.080.path=.specify/specs/077-doc-sdd-integration/test-evidence/checklist-stage-checks.md
file.080.verdict=skipped
file.080.reason=non-code-file
file.081.path=.specify/specs/077-doc-sdd-integration/test-evidence/clarify-pre-analyze-check.txt
file.081.verdict=skipped
file.081.reason=non-code-file
file.082.path=.specify/specs/077-doc-sdd-integration/test-evidence/clarify-reader-face.txt
file.082.verdict=skipped
file.082.reason=non-code-file
file.083.path=.specify/specs/077-doc-sdd-integration/test-evidence/clarify-validate-requirements.txt
file.083.verdict=skipped
file.083.reason=non-code-file
file.084.path=.specify/specs/077-doc-sdd-integration/test-evidence/decomposition-check.json
file.084.verdict=skipped
file.084.reason=non-code-file
file.085.path=.specify/specs/077-doc-sdd-integration/test-evidence/p1-t002-red.txt
file.085.verdict=skipped
file.085.reason=non-code-file
file.086.path=.specify/specs/077-doc-sdd-integration/test-evidence/p1-t003-red.txt
file.086.verdict=skipped
file.086.reason=non-code-file
file.087.path=.specify/specs/077-doc-sdd-integration/test-evidence/p1-t004-partial-green.txt
file.087.verdict=skipped
file.087.reason=non-code-file
file.088.path=.specify/specs/077-doc-sdd-integration/test-evidence/p1-t005-partial-green.txt
file.088.verdict=skipped
file.088.reason=non-code-file
file.089.path=.specify/specs/077-doc-sdd-integration/test-evidence/p1-t006-partial-green.txt
file.089.verdict=skipped
file.089.reason=non-code-file
file.090.path=.specify/specs/077-doc-sdd-integration/test-evidence/p1-t007-green.txt
file.090.verdict=skipped
file.090.reason=non-code-file
file.091.path=.specify/specs/077-doc-sdd-integration/test-evidence/p2-t009-red.txt
file.091.verdict=skipped
file.091.reason=non-code-file
file.092.path=.specify/specs/077-doc-sdd-integration/test-evidence/p2-t009-t015-green.txt
file.092.verdict=skipped
file.092.reason=non-code-file
file.093.path=.specify/specs/077-doc-sdd-integration/test-evidence/p2-t013-red.txt
file.093.verdict=skipped
file.093.reason=non-code-file
file.094.path=.specify/specs/077-doc-sdd-integration/test-evidence/p2-t015-green.txt
file.094.verdict=skipped
file.094.reason=non-code-file
file.095.path=.specify/specs/077-doc-sdd-integration/test-evidence/p3-t016-red.txt
file.095.verdict=skipped
file.095.reason=non-code-file
file.096.path=.specify/specs/077-doc-sdd-integration/test-evidence/p3-t016-t020-green.txt
file.096.verdict=skipped
file.096.reason=non-code-file
file.097.path=.specify/specs/077-doc-sdd-integration/test-evidence/plan-a6-mutation-probe.txt
file.097.verdict=skipped
file.097.reason=non-code-file
file.098.path=.specify/specs/077-doc-sdd-integration/test-evidence/plan-account-clause-coverage.txt
file.098.verdict=skipped
file.098.reason=non-code-file
file.099.path=.specify/specs/077-doc-sdd-integration/test-evidence/plan-audit-test-budget-docs-gate-probe.txt
file.099.verdict=skipped
file.099.reason=non-code-file
file.100.path=.specify/specs/077-doc-sdd-integration/test-evidence/plan-clause-extract.txt
file.100.verdict=skipped
file.100.reason=non-code-file
file.101.path=.specify/specs/077-doc-sdd-integration/test-evidence/plan-decision-tensions.txt
file.101.verdict=skipped
file.101.reason=non-code-file
file.102.path=.specify/specs/077-doc-sdd-integration/test-evidence/plan-distribution-postcheck.txt
file.102.verdict=skipped
file.102.reason=non-code-file
file.103.path=.specify/specs/077-doc-sdd-integration/test-evidence/plan-pre-analyze-check.txt
file.103.verdict=skipped
file.103.reason=non-code-file
file.104.path=.specify/specs/077-doc-sdd-integration/test-evidence/plan-regen-command-copies-baseline.txt
file.104.verdict=skipped
file.104.reason=non-code-file
file.105.path=.specify/specs/077-doc-sdd-integration/test-evidence/plan-resolution-baseline.txt
file.105.verdict=skipped
file.105.reason=non-code-file
file.106.path=.specify/specs/077-doc-sdd-integration/test-evidence/plan-scan-confirmation-gates.txt
file.106.verdict=skipped
file.106.reason=non-code-file
file.107.path=.specify/specs/077-doc-sdd-integration/test-evidence/plan-stage-template-zero-hit.txt
file.107.verdict=skipped
file.107.reason=non-code-file
file.108.path=.specify/specs/077-doc-sdd-integration/test-evidence/plan-sync-mirrors-baseline.txt
file.108.verdict=skipped
file.108.reason=non-code-file
file.109.path=.specify/specs/077-doc-sdd-integration/test-evidence/plan-targeted-tests-baseline.txt
file.109.verdict=skipped
file.109.reason=non-code-file
file.110.path=.specify/specs/077-doc-sdd-integration/test-evidence/pre-analyze-check.txt
file.110.verdict=skipped
file.110.reason=non-code-file
file.111.path=.specify/specs/077-doc-sdd-integration/test-evidence/pre-analyze-tasks-fix1.txt
file.111.verdict=skipped
file.111.reason=non-code-file
file.112.path=.specify/specs/077-doc-sdd-integration/test-evidence/pre-analyze-tasks-fix2.txt
file.112.verdict=skipped
file.112.reason=non-code-file
file.113.path=.specify/specs/077-doc-sdd-integration/test-evidence/pre-analyze-tasks-fix3.txt
file.113.verdict=skipped
file.113.reason=non-code-file
file.114.path=.specify/specs/077-doc-sdd-integration/test-evidence/r01-na-arithmetic-fix2.txt
file.114.verdict=skipped
file.114.reason=non-code-file
file.115.path=.specify/specs/077-doc-sdd-integration/test-evidence/regen-command-copies-fix1.txt
file.115.verdict=skipped
file.115.reason=non-code-file
file.116.path=.specify/specs/077-doc-sdd-integration/test-evidence/regen-command-copies-fix2.txt
file.116.verdict=skipped
file.116.reason=non-code-file
file.117.path=.specify/specs/077-doc-sdd-integration/test-evidence/regen-command-copies-fix3.txt
file.117.verdict=skipped
file.117.reason=non-code-file
file.118.path=.specify/specs/077-doc-sdd-integration/test-evidence/sync-mirrors-check-after.txt
file.118.verdict=skipped
file.118.reason=non-code-file
file.119.path=.specify/specs/077-doc-sdd-integration/test-evidence/sync-mirrors-fix1.txt
file.119.verdict=skipped
file.119.reason=non-code-file
file.120.path=.specify/specs/077-doc-sdd-integration/test-evidence/sync-mirrors-fix2.txt
file.120.verdict=skipped
file.120.reason=non-code-file
file.121.path=.specify/specs/077-doc-sdd-integration/test-evidence/sync-mirrors-fix3.txt
file.121.verdict=skipped
file.121.reason=non-code-file
file.122.path=.specify/specs/077-doc-sdd-integration/test-evidence/tasks-069-invariants.txt
file.122.verdict=skipped
file.122.reason=non-code-file
file.123.path=.specify/specs/077-doc-sdd-integration/test-evidence/tasks-account-clause-coverage-final.txt
file.123.verdict=skipped
file.123.reason=non-code-file
file.124.path=.specify/specs/077-doc-sdd-integration/test-evidence/tasks-account-clause-coverage.txt
file.124.verdict=skipped
file.124.reason=non-code-file
file.125.path=.specify/specs/077-doc-sdd-integration/test-evidence/tasks-closing-suites.txt
file.125.verdict=skipped
file.125.reason=non-code-file
file.126.path=.specify/specs/077-doc-sdd-integration/test-evidence/tasks-decomposition-check-final.txt
file.126.verdict=skipped
file.126.reason=non-code-file
file.127.path=.specify/specs/077-doc-sdd-integration/test-evidence/tasks-decomposition-check.txt
file.127.verdict=skipped
file.127.reason=non-code-file
file.128.path=.specify/specs/077-doc-sdd-integration/test-evidence/tasks-distribution-after.txt
file.128.verdict=skipped
file.128.reason=non-code-file
file.129.path=.specify/specs/077-doc-sdd-integration/test-evidence/tasks-distribution-two-state.txt
file.129.verdict=skipped
file.129.reason=non-code-file
file.130.path=.specify/specs/077-doc-sdd-integration/test-evidence/tasks-ledger-boundary.txt
file.130.verdict=skipped
file.130.reason=non-code-file
file.131.path=.specify/specs/077-doc-sdd-integration/test-evidence/tasks-owner-append-delta.txt
file.131.verdict=skipped
file.131.reason=non-code-file
file.132.path=.specify/specs/077-doc-sdd-integration/test-evidence/tasks-plan-template-skeleton.txt
file.132.verdict=skipped
file.132.reason=non-code-file
file.133.path=.specify/specs/077-doc-sdd-integration/test-evidence/tasks-pre-analyze-check-final.txt
file.133.verdict=skipped
file.133.reason=non-code-file
file.134.path=.specify/specs/077-doc-sdd-integration/test-evidence/tasks-pre-analyze-check.txt
file.134.verdict=skipped
file.134.reason=non-code-file
file.135.path=.specify/specs/077-doc-sdd-integration/test-evidence/tasks-quickstart-s1-s7.txt
file.135.verdict=skipped
file.135.reason=non-code-file
file.136.path=.specify/specs/077-doc-sdd-integration/test-evidence/tasks-scope-set-difference.txt
file.136.verdict=skipped
file.136.reason=non-code-file
file.137.path=.specify/specs/077-doc-sdd-integration/test-evidence/tasks-stage-integrity.txt
file.137.verdict=skipped
file.137.reason=non-code-file
file.138.path=.specify/specs/077-doc-sdd-integration/test-evidence/tasks-validate-tasks-final.txt
file.138.verdict=skipped
file.138.reason=non-code-file
file.139.path=.specify/specs/077-doc-sdd-integration/test-evidence/tasks-validate-tasks.txt
file.139.verdict=skipped
file.139.reason=non-code-file
file.140.path=.specify/specs/077-doc-sdd-integration/test-evidence/validate-decision-tensions-fix1.txt
file.140.verdict=skipped
file.140.reason=non-code-file
file.141.path=.specify/specs/077-doc-sdd-integration/test-evidence/validate-decision-tensions-fix2.txt
file.141.verdict=skipped
file.141.reason=non-code-file
file.142.path=.specify/specs/077-doc-sdd-integration/test-evidence/validate-decision-tensions-fix3.txt
file.142.verdict=skipped
file.142.reason=non-code-file
file.143.path=.specify/specs/077-doc-sdd-integration/test-evidence/validate-requirements-fix1.txt
file.143.verdict=skipped
file.143.reason=non-code-file
file.144.path=.specify/specs/077-doc-sdd-integration/test-evidence/validate-requirements-fix2.txt
file.144.verdict=skipped
file.144.reason=non-code-file
file.145.path=.specify/specs/077-doc-sdd-integration/test-evidence/validate-requirements-fix3.txt
file.145.verdict=skipped
file.145.reason=non-code-file
file.146.path=.specify/specs/077-doc-sdd-integration/test-evidence/validate-requirements.txt
file.146.verdict=skipped
file.146.reason=non-code-file
file.147.path=.specify/specs/077-doc-sdd-integration/test-evidence/validate-tasks-fix1.txt
file.147.verdict=skipped
file.147.reason=non-code-file
file.148.path=.specify/specs/077-doc-sdd-integration/test-evidence/validate-tasks-fix2.txt
file.148.verdict=skipped
file.148.reason=non-code-file
file.149.path=.specify/specs/077-doc-sdd-integration/test-evidence/validate-tasks-fix3.txt
file.149.verdict=skipped
file.149.reason=non-code-file
file.150.path=.specify/specs/077-doc-sdd-integration/test-evidence/zero-new-mechanism.txt
file.150.verdict=skipped
file.150.reason=non-code-file
file.151.path=.specify/specs/077-doc-sdd-integration/verification.md
file.151.verdict=skipped
file.151.reason=non-code-file
file.152.path=.specify/state/077-doc-sdd-integration.md
file.152.verdict=skipped
file.152.reason=non-code-file
file.153.path=.specify/templates/plan-template.md
file.153.verdict=skipped
file.153.reason=generated
file.154.path=.specify/templates/requirements-template.md
file.154.verdict=skipped
file.154.reason=generated
file.155.path=scripts/python/doc-consistency-check.py
file.155.verdict=reviewed
file.156.path=scripts/python/flow-class-check.py
file.156.verdict=reviewed
file.157.path=shared/definitions/flow-class-definitions.md
file.157.verdict=reviewed
file.158.path=shared/workflow/expression-gates.md
file.158.verdict=reviewed
file.159.path=skills/external/sdd-loop-driver/SKILL.md
file.159.verdict=reviewed
file.160.path=skills/external/sdd-loop-driver/references/efficiency-model.md
file.160.verdict=reviewed
file.161.path=skills/external/sdd-loop-driver/references/stage-prompts.md
file.161.verdict=reviewed
file.162.path=templates/commands/analyze.md
file.162.verdict=reviewed
file.163.path=templates/commands/checklist.md
file.163.verdict=reviewed
file.164.path=templates/commands/clarify.md
file.164.verdict=reviewed
file.165.path=templates/commands/implement.md
file.165.verdict=reviewed
file.166.path=templates/commands/plan.md
file.166.verdict=reviewed
file.167.path=templates/commands/requirements.md
file.167.verdict=reviewed
file.168.path=templates/commands/tasks.md
file.168.verdict=reviewed
file.169.path=templates/plan-template.md
file.169.verdict=reviewed
file.170.path=templates/requirements-template.md
file.170.verdict=reviewed
file.171.path=tests/contract/test_docs_gate_driver.py
file.171.verdict=reviewed
file.172.path=tests/contract/test_document_structure_gate.py
file.172.verdict=reviewed
file.173.path=tests/contract/test_expression_compatibility.py
file.173.verdict=reviewed
file.174.path=tests/contract/test_expression_gate_wiring.py
file.174.verdict=reviewed
file.175.path=tests/contract/test_flow_class_spec_declaration.py
file.175.verdict=reviewed
file.176.path=tests/contract/test_stage_class_wiring.py
file.176.verdict=reviewed
file.177.path=tests/unit/test_flow_class_spec_key.py
file.177.verdict=reviewed
<!-- coverage-receipt:end -->

---

## Author Responses（实现方逐条答复，2026-10-30）

*范围：三条 `important` 逐条答复（同意／不同意 + 理由 + 修复位置）；四条 `suggestion`、两条 `nitpick`、一条 `question` 本轮不处置，仍留在上面各自的条目里，未静默丢弃。披露口径：本轮实现面只改了 `important-1/2` 点名的那一处引擎行为（把已登记的 C-003 执行到位）与 `important-3` 的模板指引，其余为规格、证据与登记面的对齐。*

### [IMPORTANT] scripts/python/flow-class-check.py (Line 917) — exit 2 的标签与载荷 `error` 值域不符

**同意。取「把输入缺失并入 `owner-unavailable`」这一支，不取「扩载荷值域」那一支。**

**理由**：`requirements.md` FR-003 与 FR-009 ③ 早已把「键或输入非法（退出码 2）」写进同一个降级分支，`contracts/class-resolution.md` C-006 也把「spec 目录不存在」列在该段；实现却把它记成 `invalid-unit-id`——键是合法的，缺的是它指向的输入，这个标签指向了错的东西。扩值域要同时改三处（FR-018 的值域、`data-model.md` E9、U4(c) 加第三条分支），而收窄标签只要改一处，且让载荷值域继续是封闭二值 `{owner-unavailable, -}`：U4 无需新分支，接线子节「原样显示该标签」也不会再产出值域外的键。`invalid-unit-id` 保留给**不属于任何已登记键族**的调用方缺陷（裸目录名、`feature:<ID>`、路径形、`spec:` 文法之外）。

**修复位置**：
- `scripts/python/flow-class-check.py`：`spec_input_error()` 改为记 `owner-unavailable` + `flow_class: null`，原因进 `detail`；`action_lookup_spec()` 的不可读分支走同一函数（不再各自写 `invalid-unit-id`）。镜像 `.specify/scripts/python/flow-class-check.py` 由 `sync-mirrors.py --write` 生成。
- `tests/unit/test_flow_class_spec_key.py`：`test_missing_spec_directory_exits_2_without_a_decided_class` 改为断言标签 `owner-unavailable`、`flow_class is None`、`detail` 含 `spec input not found`、stderr 以标签起头（原断言 `invalid-unit-id` 与其理由一并删除——那条理由本身与 FR-009 ③ 相反）。
- 规格面：`requirements.md` FR-003 / FR-004 / FR-018 / FR-019(c)；`data-model.md` E3 / E2 / E9；`contracts/class-resolution.md` C-003 / C-005 / C-006 / C-012；`contracts/driver-integration.md` C-001 / C-004(c)；`skills/external/sdd-loop-driver/references/stage-prompts.md`（载荷纪律段 + U4(c) 段）。
- 证据：`test-evidence/pilot-expression-line.txt` § 5（实跑记录：`flow_class: null` / `owner-unavailable` / `spec input not found: …` / exit 2）。

### [IMPORTANT] scripts/python/flow-class-check.py (Line 910) — C-003 与引擎行为各占一半

**同意。取「该路径 `flow_class` 写 `null`」这一支。**

**理由**：C-003 的原文是「spec 目录不存在时 MUST 退出码 2，且 MUST NOT 返回任何类别值」，而实测给的是 `execution` + `source: default`——一个拼错的 spec 键会让「只看记录不看退出码」的消费方拿到一个确定的执行类判定，正是 C-007 的立论在 exit 2 上失效的形态。另一支（保留默认类别、靠 `error.label` 区分）会让同一族在 exit 1 与 exit 2 上对「有没有类别值」给两种答案；既然 C-003 只对**输入缺失**这一路径写死了「不带类别值」，就把这一路径执行到位。**同时把「两种形态」写清楚**（这是本条必须一起做的部分）：owner 不可解析 / 调用方无法执行引擎仍沿用既有默认记录（`execution` + `error.label`，语义是「保持既有执行类门禁集」，C-012），只有输入缺失取 `null`；这样 C-005 的互斥规则被收窄成「`null` + `default` 的唯一合法形态是输入缺失且必带 `owner-unavailable`」，而不是被悄悄放宽。

**修复位置**：
- `scripts/python/flow-class-check.py`：与上一条同一处（`spec_input_error` 写 `record[CLASS_KEY] = None`）。
- `tests/unit/test_flow_class_spec_key.py`：新增断言 `record["flow_class"] is None`（C-003 的机器可判形态）；`test_existing_spec_directory_without_requirements_exits_2` 同步加一条同样断言，使该义务在两个输入路径上各被钉一次。
- 规格面：`contracts/class-resolution.md` C-003 / C-005；`data-model.md` E2（`flow_class` 取值域与 `null` 的两处来源）；`requirements.md` FR-003 的「两种形态」段。
- 证据：`test-evidence/pilot-expression-line.txt` § 5；`quickstart.md` § S2 的「裸树形态」实测（形态②的现成样例）。

### [IMPORTANT] templates/plan-template.md (Line 179) — `[[STR-002]]`…`[[STR-006]]` 在下游不可解

**同意。删掉 `[[STR-NNN]]` 引用，改成「逐字标题 + code-first owner 指针」。**

**理由**：STR id 是每个 spec 私有的命名空间（077 自己的规格里就注明 069 已占用 `STR-003` / `STR-004`），而这份模板随 `specify init` 下发到每个项目——下游作者照这句话去自己 spec 的 § Shared Strings 找 `STR-002..006`，只会找到无关字面量或什么都找不到。可执行的 owner 在同一段里本来就有：检查器的 `STRUCTURE_HEADING` / `STRUCTURE_SUBSECTIONS` 与三个列集合常量；模板自身则是骨架的**产出方**，五个标题在模板里逐字可见，下游照抄即可，无需任何 STR 注册表。

**修复位置**：
- `templates/plan-template.md`：`## Document Structure` 注释块改写为——五个标题逐字列出 + 「读本文件，不要读别的项目的 spec 制品」+ 检查器常量名作为 code-first owner + 「本特性规格可自留 STR 表并按 id 引用，那是本规格的便利，不是 owner」。
- `.specify/templates/plan-template.md`：镜像由 `sync-mirrors.py --write --only templates/plan-template.md` 生成，`--check` 后六对 `ok`。
- 未动的部分（有意）：`tests/contract/test_document_structure_gate.py::test_plan_template_carries_the_document_structure_skeleton` 仍从 077 的 § Shared Strings 读字面量、与模板逐字比对——那是**本仓**的漂移守卫，不是下游的解析路径；模板不再引用 STR id 之后，该守卫的断言依然成立（27 passed）。

### 静默项（未采纳但已登记，不属本轮）

- 四条 `suggestion`（`stage-prompts.md` 的 `owner:` 相对路径、降级与执行类共用 `not-applicable`、`requirements-template.md` 的 `[FLOW CLASS]` 注释、证据清单的子串匹配）与两条 `nitpick`（`files_scanned` 的虚数、U4 存在性断言）、一条 `question`（围栏内的示例声明行算不算第二处声明）：本轮未改，仍以原条目为准。
- 框架级字面量的 owner 归位（过程报告 F6 / REC_T1）本轮不改，登记为 roadmap：`.specify/memory/features/077.md` § Future Evolution Suggestions。
