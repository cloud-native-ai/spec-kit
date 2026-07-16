# 编辑团队 Goal（modify 操作规范）

**Owner**: `improve-team`. 本文规范 `modify` 模式下对团队 **goal** 的编辑行为。goal 概念本身的定义见 [`../../create-team/references/goal.md`](../../create-team/references/goal.md)（单一真相源）。

## 原则

- **goal 是一等可修改对象**：`modify` 可编辑团队三部分中的任意一个——**goal / 静态结构 / 动态结构**。
- **可刻意修改，但不会漂移**：goal 不因重构结构而作为副作用改动；重定义 goal 是**明确、刻意**的编辑动作。
- **goal 变更级联结构重对齐**：因为静态与动态结构只为 goal 存在，**goal 一旦改变，必须重新评估并对齐花名册与协作模式**，使其服务于新 goal。

## 编辑流程

1. **Resolve target**——加载 `.specify/teams/<slug>/team.md`；不存在则报 "team not found" 并提议 `create`（绝不静默创建）。
2. **Classify the edit**——判断本次改动属于：
   - **结构编辑**（加/减成员、换模式、调阈值/并行度/维度）→ 保结构、证据驱动的最小改动，且**保持服务于当前 goal**；
   - **goal 编辑**（重定义总体目标）→ 进入下一步。
3. **Redefine the goal**——把新 goal 写成可验证形式（含成功标准/阈值），更新 frontmatter `goal` 字段与 `## Goal` 小节。
4. **Realign structure to the new goal**——重新评估花名册与协作模式是否仍能达成新 goal：
   - 新 goal 是否需要新增/移除角色或阶段？
   - 协作模式是否仍合适（parallel / serial / iteration / continuous）？
   - 若新 goal 主题为「优化」，按 [`../../create-team/references/optimization-goals.md`](../../create-team/references/optimization-goals.md) 重新区分一次性/持续并选择淘汰/渐进策略与其 `config`。
   - 仅做**必要**的结构改动；未受影响的成员/字段保持逐字节不变。
5. **Re-persist & report**——写回 `.specify/teams/<slug>/team.md`，**bump `updated`**（保留 `created`），并报告：goal 前后对比、因 goal 变更而做的结构对齐、以及各改动的动机证据。建议随后 `run` 验证。

## Refinement Map（goal 相关）

| 症状 | 可能原因 | 团队编辑 |
|------|----------|----------|
| goal 与实际产出不符 / 团队在做「偏题」的事 | goal 陈旧或从未明确 | 重定义 goal 为可验证形式，并按新 goal 对齐结构 |
| goal 由一次性升级为持续 | 需求从「达标即止」变为「不断提升」 | 改 goal 语义；从 **iteration** 切换到 **continuous** 运营循环，补齐 `maturity`(L1 起步)/`cadence`/`budget`/`constraints`/独立验证者 — 见 [`../../create-team/references/operating-loops.md`](../../create-team/references/operating-loops.md) |
| 持续优化久不收敛 | 策略不匹配 | 在淘汰/渐进间切换，或重划子目标（渐进）/调收敛判据（淘汰） |

## MUST / MUST NOT

- MUST 仅在**明确的 goal 编辑请求**下改动 goal；MUST NOT 在结构重构时顺手改 goal。
- goal 变更后 MUST 重新对齐结构，且 MUST NOT 遗留与新 goal 冲突的旧结构。
- MUST bump `updated`；MUST 保持未受影响字段逐字节不变。
