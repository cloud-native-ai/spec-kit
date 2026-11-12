---
status: achieved
created: 2026-11-06
updated: 2026-11-06
binding:
  owner: human
  owner_id: human
  origin: 087-arch-diagram-docs
---

# Anchor: 087 — Architecture-Diagram-Centric Documentation

## Objective

把 /speckit.docs 与 create-docs/improve-docs 驱动的文档空间改造为以架构图为核心：每份经流程新建或改进的正式文档都带配套架构图或具名豁免，图的缺失与失步由既有验证步骤确定性报出；绘图能力只经 draw-diagram 前门复用。

## Success Criteria

1. 每份经文档流程新建/改进的正式文档都带有配套架构图（可再编辑源 + 渲染产物 + 解析引用），或留下具名豁免；缺失与失步在既有验证步骤中被确定性报出。
2. 架构图配套义务写入 create-docs / improve-docs 的既有步骤与收尾判定，不新增 /speckit.* 命令，也不引入第二套文档分类。
3. 绘图能力只经 draw-diagram 前门复用：引擎选择、交付契约与验收归该技能；本特性不新增引擎、路由表或交付契约。
4. 存量文档按 reconcile 的残余报告与容忍带渐进收敛，不回溯强制全量补图；框架源与 .specify/ 镜像保持一致。

## Boundaries

- 不改 draw-diagram 的引擎层、路由矩阵与交付契约内部。
- 不对本仓 docs/ 树做一次性全量补图；存量按 reconcile 渐进收敛。
- 不新增 /speckit.* 命令或文档类型目录。

## History

- 2026-11-06 — created.
- 2026-11-06 — status active -> achieved.
