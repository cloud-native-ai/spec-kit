---
id: "20260807T091115Z-skill-draw-echarts"
unit_id: "skill:draw-echarts"
unit_type: "skill"
run_id: "substrate-echarts-20260807-1710"
scope: "local"
feature: "viz-skill-arena"
partial: false
created: "2026-08-07T09:11:15Z"
summary: "Substrate 架构三图（力导向关系图 / 手工布局状态机 / 横向树图）均输出为独立暗色主题 HTML，并通过 node mock 校验（link 引用完整性 + 语法）。本次运行干净。"
---

## Review
Substrate 架构三图（力导向关系图 / 手工布局状态机 / 横向树图）均输出为独立暗色主题 HTML，并通过 node mock 校验（link 引用完整性 + 语法）。本次运行干净。

## Optimization Points
- ## Review
- Substrate 架构三图（力导向关系图 / 手工布局状态机 / 横向树图）均输出为独立暗色主题 HTML，并通过 node mock 校验（link 引用完整性 + 语法）。本次运行干净。
- ## Optimization Points
- 对 graph 系列边标签：默认常显会在力导向布局中造成遮挡，建议将 `edgeLabel.show` 设为仅在 `emphasis`（悬停）时显示，或提供全局开关变量便于一键切换。
- 状态机类图可沉淀为模板：`layout:'none'` + 手工坐标 + roundRect 节点 + 分类着色边的配置组合在架构图中高频复用，可加入 references/echarts-guide.md 作为 recipe。
