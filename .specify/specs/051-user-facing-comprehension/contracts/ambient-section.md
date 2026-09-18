# Contract: ambient-section — 常驻章节投递契约

**Feature**: 051 面向用户可理解性纪律  
**Guards**: `templates/instructions-template.md` 的 `## User-Facing Comprehension` 章节(STR-004)及其再生面  
**Test file**: `tests/contract/test_user_facing_comprehension_section.py`  
**Date**: 2026-09-17

本契约钉死常驻章节的**唯一性、镜像字节相等、活动指令文件抵达、节体自约束、非内联、位置窗口避让、中立性与零阻塞模式命中**。条款编号 C-1…C-11 由测试函数名 `test_cN_*` 一一对应。

章节形态取自房子先例:一段引出核心主张与固定指针短语 → 2–5 条子规则要点 → 可选收尾指针行(参照 `templates/instructions-template.md:49-57` 的 One Source Of Truth 与 `:65-71` 的 Token Efficiency Discipline)。

---

## 唯一性与镜像

**C-1** `templates/instructions-template.md` MUST 含**恰好一次** STR-004 标题行 `## User-Facing Comprehension`;该章节体 MUST 含 STR-001 指针 `.specify/shared/guidelines/user-facing-comprehension.md`。

**C-2** `.specify/templates/instructions-template.md` MUST 同样含**恰好一次** STR-004 标题与 STR-001 指针,且与 `templates/instructions-template.md` `read_bytes()` **逐字节相等**。

**C-3** `.specify/instructions.md` MUST 含逐字的 STR-004 标题行(增量调谐已重跑)。断言方向为**模板 ⊆ 活动文件**,只比标题不比节体——与既有 `test_instructions_section_propagation.py:34-42`(C-1)同形,活动文件多出项目自有章节 MUST 被容忍。

## 节体自约束

**C-4** 章节体 MUST ≤ **25 行**,且 MUST NOT 含任何 `###` 子标题。

**C-5** 章节体 MUST NOT 含 `/speckit.` 命令形式,亦 MUST NOT 含参数形式(如 `--action`、`--only`)。本纪律的主题是"不把引擎表面暴露给读者",章节自身 MUST 率先遵守。

**C-6** 章节体 MUST NOT **内联**真源文档的七个 H2 节名(即 `discipline-doc.md` C-6 钉死的七个节名 MUST NOT 出现在章节体内)。摘要可提及子规则**名**,但 MUST NOT 复述其条件表、阈值字面量或枚举——判定标准取 `ask-record-repeat.md:97` 的机械测试:一个打算据此行动的读者 MUST 仍需打开真源文档。

## 位置窗口避让

**C-7** 新章节 MUST NOT 落在被钉死的位置窗口内。具体:`## Documentation Map`、`## Proactive Flow Trigger`、`## Fact, Correctness & Logic Checks (Input Sanity)` 三者的**相对顺序与相邻关系** MUST 与本特性改动前一致(该窗口由 `test_proactive_trigger_section.py:141-152` 与 `test_ask_record_repeat.py:220-227` 双向钉死)。

**C-8** 新章节 MUST 位于 `## Token Efficiency Discipline` **之后**、`## Dogfooding Practice` **之前**——与同类纪律相邻,且在 C-7 的窗口之外。

## 中立性与预算

**C-9** 章节体 MUST NOT 含本仓专有名称:`spec-kit`、`specify-cli`、`specify_cli`、`cloud-native-ai`(大小写不敏感)。

**C-10** 章节体对 `BLOCKING_RE` 的命中数 MUST 为 **0**。测试 MUST 以 `importlib` 内联加载真实扫描器并复用其 `BLOCKING_RE`,MUST NOT 重写模式副本。

## 悬空指针防护(FR-038)

**C-11** 悬空指针断言 MUST 同时遍历**两个**指令面:`templates/instructions-template.md`(随包分发的源)与 `.specify/instructions.md`(本仓生成物)。对其中**每一个**指向 `.specify/shared/guidelines/<name>.md` 的指针,其对应的 `shared/guidelines/<name>.md` MUST 存在。该断言 MUST 遍历全部此类指针,MUST NOT 只检查新文档——FR-038 与 SC-017 要求把既有的投递窗口变成**受测**的,而不是只保护新增面。

**C-11(a) 覆盖分母 MUST 实测、MUST NOT 假定**(A-02/B-05 订正):遍历只能抵达**有指针**的 guideline,故"覆盖既有 11 份 guideline"这一原表述为假。2026-09-18 实测——`ls -1 shared/guidelines/*.md` = **11** 份;`grep -oE 'shared/guidelines/[a-z-]+\.md' <面> | sed 's|.*/||' | sort -u` 得模板面 **7** 份、活动文件面 **8** 份(后者多出 `better-harness.md`,即两面本身就不一致,这也是 MUST 遍历两面的理由),两面并集 **8** 份;`checklist-methodology.md`、`requirements-guidelines.md`、`self-improvement.md` 这 **3** 份在**两面都无指针**,结构上不可能从指令面悬空,因而不在指针存在性断言的可达范围内。

**C-11(b) 余集断言(使该边界不成为静默缺口)**:断言 MUST 另从 `shared/guidelines/*.md` 派生全集、减去被指向的集合,并断言余集 **⊆** {`checklist-methodology.md`, `requirements-guidelines.md`, `self-improvement.md`}——即余集 MUST NOT 出现第 4 个名字。取**子集**语义而非相等语义,方向才对:任何一份既有 guideline 的指针被删除都会让余集多出一个名字而**失败**(覆盖率无法静默缩小),而日后为这 3 份补上指针只会让余集变小、**不误报**。如此 11 份全部被本条核算——8 份经指针存在性、3 份经具名余集——"覆盖全部 11 份"的意图以**可实现**的形式成立。本特性新增的第 12 份(`user-facing-comprehension.md`)落地后必有指针,故余集不变、指针面 +1。

---

## 同批义务(非条款,实现顺序约束)

C-2 与 C-3 无法靠只改源文件满足。实现 MUST 在同一批内**按下列顺序**执行(顺序不可颠倒:`generate-instructions.sh:22` 的 `TEMPLATE_FILE` 指向 `.specify/templates/instructions-template.md`,即它读的是**镜像**而非源文件,故镜像同步 MUST 先于指令再生,否则再生结果不含新章节):

1. 编辑 `templates/instructions-template.md`;
2. 运行 `python3 scripts/python/sync-mirrors.py --write` 同步 `.specify/templates/` 与 `.specify/shared/`(满足 C-2);
3. 运行 `bash scripts/bash/generate-instructions.sh` 再生 `.specify/instructions.md`(满足 C-3);
4. 核验 8 条 symlink 别名仍为符号链接而非被替换成普通文件(根 `AGENTS.md` / `CLAUDE.md` / `QODER.md` / `HERMES.md`、`.github/copilot-instructions.md`、`.qoder/project_rules.md`、`.claude/project_rules.md`、`.opencode/instructions.md`,创建于 `generate-instructions.sh:235-267`)。

---

## 条款 → FR / SC 映射

| 条款 | FR | SC |
|---|---|---|
| C-1, C-2, C-3 | FR-003 | — |
| C-4, C-5, C-6 | FR-003, FR-029 ④ | SC-007 |
| C-7, C-8 | FR-003 | — |
| C-9 | FR-030 | SC-010 |
| C-10 | FR-032 | SC-012 |
| C-11 | FR-038 | SC-017 |
