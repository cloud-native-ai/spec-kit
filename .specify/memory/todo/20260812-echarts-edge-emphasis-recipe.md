---
title: ECharts 图谱交互与状态机 recipe
status: parked
parked_at: 2026-08-12
origin: 反馈积压处置(2026-08-07 draw-echarts viz-skill-arena 运行)
tags: [draw-echarts, recipe]
---

两点:① graph 系列边标签默认常显在力导向布局中造成遮挡——建议 `edgeLabel.show` 仅在 `emphasis`(悬停)时显示,或提供全局开关变量一键切换;② 状态机类图配置组合(`layout:'none'` + 手工坐标 + roundRect 节点 + 分类着色边)高频复用,可沉淀为 `references/echarts-guide.md` 的 recipe。

## Evolution Log

- 2026-08-12 parked(自反馈批次 20260807T091115Z)。属技能内容增强,待 draw-echarts 下次迭代窗口。
