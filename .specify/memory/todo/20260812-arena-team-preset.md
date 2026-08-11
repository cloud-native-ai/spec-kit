---
title: 锦标赛竞技场团队预置形状
status: parked
parked_at: 2026-08-12
origin: 反馈积压处置(2026-08-07 create-team viz-skill-arena 运行)
tags: [create-team, preset, continuous]
---

给 `match-team-preset.py` 增加「锦标赛竞技场」continuous 预置形状(多技能同题竞技 + 双轮裁判 + 重绘)。viz-skill-arena 创建时 preset 匹配为 low(artifact-optimizer 是 iteration 收敛形状,不匹配长期多任务持续优化),从零推导成本高。

## Evolution Log

- 2026-08-12 parked(自反馈批次 20260807T051529Z)。涉及预置库与匹配引擎扩展,需独立评估。
