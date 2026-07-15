---
id: "20260715T064131Z-skill-create-team"
unit_id: "skill:create-team"
unit_type: "skill"
run_id: "run-draw-plantuml-optimizer-20260715"
scope: "local"
feature: "team-draw-plantuml-optimizer"
partial: false
created: "2026-07-15T06:41:31Z"
summary: "执行 team draw-plantuml-optimizer（team-loop/淘汰）：baseline 0.57，2 代收敛至 0.859≥0.85。每代 3 变体并行→查看渲染打分→锦标赛留优汰劣→注入改进点。产出优胜图 + 将验证过的『复杂大图五步技术栈』落为 large-diagram-playbook.md 并同步镜像。流程顺畅，3 处可固化经验。"
---

## Review
执行 team draw-plantuml-optimizer（team-loop/淘汰）：baseline 0.57，2 代收敛至 0.859≥0.85。每代 3 变体并行→查看渲染打分→锦标赛留优汰劣→注入改进点。产出优胜图 + 将验证过的『复杂大图五步技术栈』落为 large-diagram-playbook.md 并同步镜像。流程顺畅，3 处可固化经验。

## Optimization Points
- team-loop 执行时，被派发的变体子代理无法写 report.md（harness 策略只允许返回文本/写 .puml 交付物），而团队动态结构约定「每变体写打分卡/report 到工作区」。建议：在 create-team 的 team-loop 执行指引中明确「子代理以最终消息返回结构化数据，report/score 由 orchestrator 落盘」，避免子代理反复尝试被阻断的写操作。
- 淘汰策略「种子=赢家 + 注入次优者最佳点」极有效：gen-1(0.763)→gen-2(0.859) 两代即收敛。可在 optimization-goals.md 淘汰策略要点补一句「gen-2 起显式让变体嫁接上一代次优者的最佳单点」，把这条经验固化。
- 大图渲染必须用 SVG（PNG 触 4096 硬上限被裁剪），评分应基于 SVG/按比例缩放的 PNG；已在 playbook 与 report 记录。
