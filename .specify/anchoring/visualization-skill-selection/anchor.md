---
status: active
created: 2026-11-12
updated: 2026-11-12
---

# Anchor: visualization-skill-selection

## Objective

通过「用户下发图表任务 → draw-diagram 构建语义绘图规格 SDS(逻辑图模型 + 图元几何 + 视觉权重语义) → 5 个语法引擎并行按 SDS 实现同一图表 → 第一轮 3 名裁判从不同角度打分 → 根据评审意见优化对应技能 (工作副本)并重绘 → 第二轮 2 名新裁判评审并选出冠军 → 记录结论」的循环，逐步建立「需求类型 → 最优技能」 的匹配知识(结论账本)，并持续优化语义层(draw-diagram)与六个语法层技能。 成功标准(每轮)：(1) 产出该任务冠军技能与匹配结论，追加至结论账本 .specify/memory/knowledge/visualization-skill-selection.md；(2) 被采纳的技能变更(经第二轮独立裁判接受、 无回退)合并回对应 canonical 技能目录并同步镜像；(3) 加权评分维度：语义保真 0.30 / 视觉质量 0.30 / 需求契合 0.25 / 可复现可维护 0.15，冠军 = 该轮最高加权分(≥0.85 采纳线)；技能变更采纳门 = 重绘后加权分 ≥ 第一轮自身分(无回退)；(4) 分离纪律：SDS 不得含引擎语法，语法层不得自行改写语义(几何/权重偏离必须声明)。

## Success Criteria

1. 冠军裁定：第二轮裁判按加权维度（语义保真 0.30 / 视觉质量 0.30 / 需求契合 0.25 / 可复现可维护 0.15）打分，最高加权分且 ≥0.85 者为冠军；
2. 结论记录：冠军 + 「该任务类型 → 推荐技能」匹配结论追加至 `.specify/memory/knowledge/visualization-skill-selection.md`（结论账本，跨轮累积）；
3. 技能优化：R1 评审意见 → supervisor 将改进写入对应技能**工作副本**（target）→ 实现者重载后重绘 → R2 接受（重绘分 ≥ R1 自身分，无回退）→ 变更合并回 canonical `skills/draw-*/` 并同步 `.specify/skills/` 与 `.qoder/skills/` 副本；
4. 分离纪律：SDS 不含引擎语法；语法层不自行改写语义，几何/视觉权重偏离必须量化声明（自动布局引擎的逼近偏离计入其语法实现质量，不计为语义层缺陷）；
5. 每轮产出 run report（`.specify/teams/viz-skill-arena/runs/`）+ STATE.md 更新 + run-log 一行。

## History

- 2026-11-12 — created.
