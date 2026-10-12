---
status: achieved
created: 2026-09-16
updated: 2026-10-12
---

# Goal: draw-two-layer-structure

## Objective

绘图能力由单一技能 draw-diagram 承载:用户不必告知「画什么」——它据上下文与用户的补充说明自行分析语义,辨识层级、依赖与上下关系,抽象出图表并选定合适的结构类型,再交由其内置的唯一最合适的引擎层渲染;用户面对各引擎层(d3js、drawio、echarts、excalidraw、mermaid、plantuml,均位于 draw-diagram 的 references/types/ 下)时不必告知布局、线段绘制与渲染等实现细节,语法知识各自归位于引擎层;每次出图后用户的评价被主动征询并据以调整,使一次绘图请求的完成不依赖用户补齐任何一层的知识。

## Success Criteria

1. 绘图入口只有一个技能 draw-diagram:它在交付产物后主动征询用户评价,评价以 evaluation form 承载,且条目内记明本次实际使用的引擎层(d3js、drawio、echarts、excalidraw、mermaid、plantuml 之一),使原先按技能分立的评价粒度不因六引擎内置化而丢失;复用 speckit 现有 feedback 链路与机制,但与该技能内遵循 .specify/shared/workflow/feedback-step.md 红线与规则的标准 feedback 分立为两物,不混称。
2. 用户未提出评价即视为本次绘制满意;用户提出评价则该条目经 feedback probe 进入 .specify/memory/feedback 并被持续处置,处置结论反哺对应引擎层。
3. 达成程度以「绘制运行中无评价(=满意)的占比」与「已提出评价中被处置的占比」按程度衡量,不设固定阈值:本目标为长期目标,achieved 是一次刻意的人工判定而非算出的结论。

## Targets

| ID | Target | Status |
|----|--------|--------|
| T-001 | 重构阶段:把现有结构打碎重组,自验证条件如 mermaid/plantuml 各自一整套语义层整体挪进 skills/draw-diagram | done |
| T-002 | 自测阶段:重构完成后用干净的 context + subagent 调用技能绘制,评估结果是否符合预期 | dropped |
| T-003 | 公测阶段:用户反馈持续采集、无反馈=满意、长期逼近不设阈值 | dropped |

## History

- 2026-09-16 — created.
- 2026-09-16 target T-001 added: 重构阶段:把现有结构打碎重组,自验证条件如 mermaid/plantuml 各自一整套语义层整体挪进 skills/draw-diagram
- 2026-09-16 target T-002 added: 自测阶段:重构完成后用干净的 context + subagent 调用技能绘制,评估结果是否符合预期
- 2026-09-16 target T-003 added: 公测阶段:用户反馈持续采集、无反馈=满意、长期逼近不设阈值
- 2026-09-16 target T-001 open→dropped
- 2026-09-16 target T-002 open→dropped
- 2026-09-16 target T-003 open→dropped
- 2026-09-16 — criteria changed; prior value: 六个绘图技能（draw-diagram 与 draw-{d3js,echarts,excalidraw,mermaid,plantuml}）在交付产物后都主动征询用户评价，评价以 evaluation form 承载：复用 speckit 现有 feedback 链路与机制，但与该技能内遵循 .specify/shared/workflow/feedback-step.md 红线与规则的标准 feedback 分立为两物，不混称。 | 用户未提出评价即视为本次绘制满意；用户提出评价则该条目经 feedback probe 进入 .specify/memory/feedback 并被持续处置，处置结论反哺对应技能。 | 达成程度以「绘制运行中无评价（=满意）的占比」与「已提出评价中被处置的占比」按程度衡量，不设固定阈值：本目标为长期目标，achieved 是一次刻意的人工判定而非算出的结论。
- 2026-09-17 — criteria changed; prior value: 七个绘图技能（draw-diagram 与 draw-{d3js,drawio,echarts,excalidraw,mermaid,plantuml}）在交付产物后都主动征询用户评价，评价以 evaluation form 承载：复用 speckit 现有 feedback 链路与机制，但与该技能内遵循 .specify/shared/workflow/feedback-step.md 红线与规则的标准 feedback 分立为两物，不混称。 | 用户未提出评价即视为本次绘制满意；用户提出评价则该条目经 feedback probe 进入 .specify/memory/feedback 并被持续处置，处置结论反哺对应技能。 | 达成程度以「绘制运行中无评价（=满意）的占比」与「已提出评价中被处置的占比」按程度衡量，不设固定阈值：本目标为长期目标，achieved 是一次刻意的人工判定而非算出的结论。
- 2026-09-17 — criteria changed; prior value: None provided.
- 2026-10-12 target T-001 dropped→open
- 2026-10-12 target T-001 open→done
- 2026-10-12 — objective changed; prior value: 绘图能力呈两层自治结构：skills/draw-diagram 是唯一绘图入口，用户不必告知「画什么」—— 它据上下文与用户的补充说明自行分析语义，辨识层级、依赖与上下关系，抽象出图表并选定合适的结构类型，再把渲染委派给唯一最合适的引擎；用户面对 skills/draw-{d3js,echarts,excalidraw,mermaid,plantuml} 时不必告知布局、线段绘制与渲染等实现细节，语法知识各自归位于引擎层；每次出图后用户的评价被主动征询并据以调整，使一次绘图请求的完成不依赖用户补齐任何一层的知识。
- 2026-10-12 — criteria changed; prior value: 七个绘图技能（draw-diagram 与 draw-{d3js,drawio,echarts,excalidraw,mermaid,plantuml}）在交付产物后都主动征询用户评价，评价以 evaluation form 承载：复用 speckit 现有 feedback 链路与机制，但与该技能内遵循 .specify/shared/workflow/feedback-step.md 红线与规则的标准 feedback 分立为两物，不混称。 | 用户未提出评价即视为本次绘制满意；用户提出评价则该条目经 feedback probe 进入 .specify/memory/feedback 并被持续处置，处置结论反哺对应技能。 | 达成程度以「绘制运行中无评价（=满意）的占比」与「已提出评价中被处置的占比」按程度衡量，不设固定阈值：本目标为长期目标，achieved 是一次刻意的人工判定而非算出的结论。
- 2026-10-12 — status active -> achieved.
