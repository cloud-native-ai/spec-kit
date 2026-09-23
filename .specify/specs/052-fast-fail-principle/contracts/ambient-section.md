# Contract: 常驻章节与实例收敛 (ambient-section)

**Feature**: 052 快速失败纪律(Fast Fail)  
**Guards**: `requirements.md` FR-005, FR-006, FR-029, FR-030, FR-062, FR-077  
**Test file**: `tests/contract/test_fast_fail_discipline.py`(函数名 `test_aN_*`;条款号在本文件内独立编号,跨文件引用 MUST 写作 `ambient-section.md C-N`)  
**Date**: 2026-09-23

---

## 章节存在与唯一性

**C-1** `templates/instructions-template.md` MUST 含标题 `## Fast Fail Discipline`,且 `text.count(该标题) == 1`。

**C-2** `.specify/instructions.md`(活动文件)MUST 含同一标题,且 `count == 1`。该活动文件由 `generate-instructions.sh` 再生,MUST NOT 手工编辑。

**C-3** 两处 MUST 各含**恰好一行**指向 `.specify/shared/guidelines/fast-fail.md` 的指针(运行时副本路径,即读者解析的那一份)。

**C-4** 反空真哨兵:断言指针行数为 1 时,MUST 同时断言该章节正文长度非零(例如 ≥ 3 行),使"指针恰好一行"不因章节整体缺失而空真。

## 位置约束

**C-5** 模板中四个纪律章节的索引 MUST 满足**严格排序**:`## Token Efficiency Discipline` < `## User-Facing Comprehension` < `## Fast Fail Discipline` < `## Dogfooding Practice`。

> 依据实测:`test_user_facing_comprehension_section.py:207-218` 的 `test_c8` 断言的是 `i_prev < i_new < i_next`(严格排序),**不是相邻**。故在 UFC 与 Dogfooding 之间插入本章节不破坏该钉子。本条 MUST 与既有 `test_c8` 同时成立,即插入后 UFC 仍满足 `Token Efficiency < UFC < Dogfooding`。

**C-6** 本章节 MUST NOT 落在既有三节连续窗口内:`## Documentation Map` / `## Proactive Flow Trigger` / `## Fact, Correctness & Logic Checks (Input Sanity)` 三者 MUST 保持连续且有序,本章节 MUST NOT 插入其间任何位置。

**C-7** 模板的顶级 `## ` 章节数由实测 **18** 增至 **19**;活动文件由 **19** 增至 **20**(活动文件多一节 `## Recurring Operational Lessons`)。二者 MUST 满足既有 `test_instructions_section_propagation.py` 的"模板章节集 ⊆ 活动文件章节集"断言。

> 本条的两个数字是**改前实测值 + 1**,不是凭空写的期望:改前实测 `grep -c '^## '` 模板 = 18、活动 = 19(2026-09-23)。

## 不内联与形态

**C-8** 模板的本章节 MUST NOT 内联真源文档的任何 H2 节名(即 `discipline-doc.md` C-7 的 9 个节名一律 MUST NOT 出现在模板本章节内)。该条防止常驻章节退化为真源文档的副本。

**C-9** 本章节 MUST 沿用既有纪律章节的固定引导句式形态:`The full discipline is defined in a single source of truth — ` + 反引号路径 + `(do NOT copy its rules; reference the file) — and binds all commands, skills, and agents:`。

**C-10** 本章节 MUST NOT 含引擎调用形态(裸 `--action` 旗标、`$ARGUMENTS`、`<占位符>`),形态对齐既有 `PARAM_PATTERNS` 约束(`test_user_facing_comprehension_section.py:65`,其使用点在 `:170`)。

**C-11** 本章节 MUST 项目中立:MUST NOT 含 `spec-kit` / `specify-cli` / `specify_cli` / `cloud-native-ai`。

**C-12** 本章节 MUST NOT 含任何 `/speckit.` 命令调用形态(它是常驻纪律摘要,不是流程步骤)。

## 恢复路径的真实性(FR-077)

**C-13** 本章节若含"真源文档缺失时如何恢复"的表述,MUST 指名**真实的恢复路径**——CLI 的资产复制(`copy_local_templates()`,由 `specify init` 调用,实测 `src/specify_cli/__init__.py:2202-2216` 把 `shared/` 复制到 `.specify/shared/`;`_CORE_SPECIFY_ASSETS` 于 `:1081` 含 `.specify/shared`)。

**C-14** 本章节 MUST NOT 含"刷新项目指令即连同其镜像副本一并恢复"一类句式。依据:`scripts/bash/generate-instructions.sh` 全文无镜像同步调用,`templates/commands/instructions.md` 亦只把自身描述为对**指令空间**的调谐引擎;该句式经实测**不成立**,照抄会把一条假承诺送进每个下游项目,而悬空指针按房子规则会使命中它的命令中止。

**C-15** 本条为**负面命题**,故 MUST 配变异演练取证:临时把 C-14 禁止的句式插入本章节 → 断言变红 → 移除 → 断言恢复绿。演练用临时改动 MUST 复原并复核(`git diff` 对该文件为空)。

## 既有实例点位的指针收敛(FR-029)

**C-16** FR-029 点名的既有实例点位 MUST **各含且仅含一行**指向真源文档的指针,且其**原有行为正文逐字未变**。点位集合(封闭枚举,守卫按文件名而非行号定位——新增行会使行号静默错位):

| 文件 | 被点名的既有规则 |
|---|---|
| `templates/commands/implement.md` | 可写性预探针、任务前提证伪回写、门禁判定不得绕、非并行失败即停、两振停滞升级 |
| `templates/commands/todo.md` | 任务失败即停并报告 |
| `templates/commands/analyze.md` | 必需文件缺失即中止 |
| `templates/commands/docs.md` | 标记缺失/不配对/不可解析即停;尾部 MUST NOT 静默延迟 |
| `templates/commands/clarify.md` | 无 requirements.md 即中止;超上限即停并建议 interview |
| `templates/commands/interview.md` | 冲突 MUST 呈现、MUST NOT 静默解决 |
| `skills/create-team/references/create-mode.md` | 悬空引用 MUST NOT 静默降级为内联目标创建 |
| `skills/draw-diagram/SKILL.md` | MUST NOT 静默降级、MUST NOT 即兴绕过 |

**C-17** 反空真哨兵:断言"上述点位的正文改动行数为 0"时,MUST 同时断言"上述点位中至少一个确实新增了指针行",使"零改动因为只加了指针"与"零改动因为整条收敛没做"可区分。

**C-18** 收敛范围 MUST 有界:MUST NOT 对 `docs/`、`agents/`、其余技能正文做全仓措辞清扫(FR-030 / FR-062)。守卫形态为**余集断言**——除 C-16 枚举的点位与本特性自身的落点外,`shared/` 与 `templates/` 下 MUST NOT 出现第二处判据复述(单源扫描,形态同 `test_one_source_of_truth.py:142-153`)。

**C-19** **通道一的合规性不可被契约测试观测**(编排者当场撰写的内联提示不落盘),故本文件 MUST NOT 声称三通道均由守卫覆盖;该边界由 FR-062 与 `plan.md` 如实标注,属**评审**强制面。本条本身即该标注的守卫:断言真源文档载有这一自陈。

---

## 条款 → FR / SC 映射

| 条款 | FR | SC | 备注 |
|---|---|---|---|
| C-1…C-4 | FR-005, FR-006 | SC-004 | 各出现且仅出现一次 + 反空真哨兵 |
| C-5, C-6 | FR-005 | SC-004 | 位置受两处既有钉子约束(D-1) |
| C-7 | FR-005 | SC-004 | 18→19 / 19→20,改前实测 |
| C-8, C-9, C-10, C-11, C-12 | FR-006, FR-007, FR-008 | SC-003, SC-004 | 不内联 + 房式形态 + 中立 |
| C-13, C-14, C-15 | FR-077 | — | C-15 为负面命题,须变异演练 |
| C-16, C-17 | FR-029 | SC-010 | 按文件名定位,不按行号 |
| C-18 | FR-030, FR-062 | SC-003 | 余集断言 |
| C-19 | FR-062 | — | 诚实标注不可测面 |
