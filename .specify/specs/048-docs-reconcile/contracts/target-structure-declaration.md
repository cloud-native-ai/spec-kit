# Contract: 目标结构声明

**Requirement**: `048-docs-reconcile` → Feature 037 Docs Command
**Target artifacts**: `.specify/docs/target-structure.md`(运行时实例)、`templates/docs-target-structure-template.md`(骨架)
**Date**: 2026-09-01

## T-1 路径与可区分性

声明 MUST 位于 `.specify/docs/target-structure.md` —— 运行工作区的**根级单文件**。按次运行产物 MUST 继续留在子目录 `plans/`、`audit/`。此层级差异即 FR-002a 的"可区分"实现:按目录处理按次产物的任何操作都不触及根级文件。

声明 MUST NOT 被放入 `plans/` 或 `audit/`;MUST NOT 采用带时间戳的按次命名。

## T-2 不随按次产物轮转

声明 MUST NOT 被任何轮转/清理逻辑覆盖。现状核验(实现时须复核仍然成立):`sanitize-utils.py` 的 `MATERIAL_ROOTS` 不含 `.specify/docs`;`docs-utils.py` 不枚举该目录;仓内唯一保留期逻辑 `memory-utils.py --action prune` 只作用于 `.specify/memory/`。

若未来引入针对 `.specify/docs/` 的清理能力,该能力 MUST 显式排除本文件。

## T-3 受管块标记

声明 MUST 使用成对 HTML 注释标记界定机器维护区:

```
<!-- DOCS_TARGET_STRUCTURE_START -->
<!-- DOCS_TARGET_STRUCTURE_END -->
```

写入规则(沿用 `.specify/git-workflow.md` 先例):文件已存在且标记成对时,MUST **只替换标记之间的内容**,标记本身与块外内容 MUST 字节保持。

## T-4 必填字段

受管块内 MUST 含以下字段(形态见 `data-model.md` § 1):`项目形态`、`目标读者`、`静态基线引用`、`项目专属扩展`、`内容盘点摘要`、`固定检索入口`、`最后确认`。

`项目专属扩展` 为空时 MUST 写显式"无扩展"行,MUST NOT 省略该字段。

## T-5 引用而非复制(单一事实源)

`静态基线引用` MUST 指向 `.specify/skills/create-docs/SKILL.md` § Desired-State Baseline。该节是文档空间静态基线及其枚举、字段、状态与阈值的唯一 owner；声明、骨架、命令和本契约 MUST NOT 重述其中任何完整表格、枚举项或阈值字面量。需要判断或生成项目结构的执行者 MUST 打开 owner，而不是依赖消费侧摘要。

验证(SC-005):契约测试 MUST 从 owner 的对应章节动态提取受管事实，并断言骨架与 dogfood 声明未复制这些事实；测试代码可按宪法 XIV 的“用于检测漂移的测试字面量”例外固定必要哨兵，但本契约不保存其副本。

## T-6 项目专属性

`项目形态`、`目标读者`、`内容盘点摘要` MUST 反映目标项目实测事实(现有文档清单与主题聚类),MUST NOT 是模板措辞的复述。信息不足时 MUST 提问(≤3 问)而非虚构(FR-003)。

## T-7 生命周期与确认

- 声明不存在 → 设计后与干跑计划**合并为一次确认**呈现;经确认后写入并记 `最后确认`。
- 声明已存在且用户未要求重设 → MUST 直接复用,MUST NOT 重新设计(FR-004 防抖)。
- 检测到与项目实态实质性脱节 → MUST 仅**提议**重设计并进入计划待确认项(FR-015),MUST NOT 静默重设。
- 用户输入隐含结构变更 → 经确认后回写(FR-010);未确认 MUST NOT 改动持久目标。

## T-8 标记残缺处理

标记缺失、不成对或块内不可解析时,MUST 视为"存在但不可用":停止收敛、报告标记状态、请求人工处置或显式授权重建。MUST NOT 静默重写整个文件(会覆盖块外人工加注)。

## T-9 骨架模板

`templates/docs-target-structure-template.md` MUST:遵循 `<name>-template.md` 命名约定;含成对标记;为每个 T-4 字段提供占位符;不含任何 T-5 禁止的基线枚举;经 templates 镜像对同步到 `.specify/templates/`。验证以 `sync-mirrors.py --check` 中 templates 对报 `ok`、无新 `MISS`/`DIFF`,且两文件 `diff -q` 字节一致为准;全局命令当前因无关的既有 `git-fleet` 漂移 exit 2,不得误写为本特性须达 exit 0。

## T-10 消歧

本声明与 **Goal Target(目标切片)** 无关——后者是 goal 域的 run 级指派范围概念(`shared/definitions/goal-definitions.md`)。词汇表已登记两者的区分。

`improve-docs` 现有约束行把 `.specify/docs/**` 整体描述为 "run artifacts";实现阶段 MUST 订正该措辞以涵盖跨运行声明,同时保持 improve-docs **不得编辑**该文件的效果不变(它不是文档)。
