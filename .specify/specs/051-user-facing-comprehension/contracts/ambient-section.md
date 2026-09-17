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

**C-11** 指令模板中**每一个**指向 `.specify/shared/guidelines/<name>.md` 的指针,其对应的 `shared/guidelines/<name>.md` MUST 存在。该断言 MUST 遍历全部此类指针(覆盖既有 11 份 guideline + 本特性新增的第 12 份),MUST NOT 只检查新文档——FR-038 与 SC-017 要求把既有的投递窗口变成**受测**的,而不是只保护新增面。

---

## 同批义务(非条款,实现顺序约束)

C-2 与 C-3 无法靠只改源文件满足。实现 MUST 在同一批内:

1. 编辑 `templates/instructions-template.md`;
2. 运行 `bash scripts/bash/generate-instructions.sh` 再生 `.specify/instructions.md`(满足 C-3);
3. 运行 `python3 scripts/python/sync-mirrors.py --write` 同步 `.specify/templates/`(满足 C-2);
4. 核验 8 条 symlink 别名仍为符号链接而非被替换成普通文件(根 `AGENTS.md` / `CLAUDE.md` / `QODER.md` / `HERMES.md`、`.github/copilot-instructions.md`、`.qoder/project_rules.md`、`.claude/project_rules.md`、`.opencode/instructions.md`,创建于 `generate-instructions.sh:235-267`)。

步骤 2 与 3 的顺序不可颠倒:`generate-instructions.sh` 从 `.specify/templates/instructions-template.md` 读取模板,故 MUST 先同步镜像再再生指令文件,否则再生结果不含新章节。

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
