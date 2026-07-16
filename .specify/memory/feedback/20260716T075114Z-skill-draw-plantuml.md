---
id: "20260716T075114Z-skill-draw-plantuml"
unit_id: "skill:draw-plantuml"
unit_type: "skill"
run_id: "gen23-final-d5-text-decoration"
scope: "local"
feature: "arc4-context-split"
partial: false
created: "2026-07-16T07:51:14Z"
summary: "将图5(Build+Serverless 序列图)提升到最新技能标准，重点应用 §3 文字修饰步骤：参与者标题剥离冗长副标题(控制面/构建节点/:3002等)，改用 «角色» 构造型承载身份，详解外置为 2 个布局安全的 note(快照货币锚 + 黑箱交叉引用)。保留核心点(快照即通用货币)、两个片段(构建/Serverless)、3 条指向 Object storage 的快照货币锚箭头、通道色"
---

## Review
将图5(Build+Serverless 序列图)提升到最新技能标准，重点应用 §3 文字修饰步骤：参与者标题剥离冗长副标题(控制面/构建节点/:3002等)，改用 «角色» 构造型承载身份，详解外置为 2 个布局安全的 note(快照货币锚 + 黑箱交叉引用)。保留核心点(快照即通用货币)、两个片段(构建/Serverless)、3 条指向 Object storage 的快照货币锚箭头、通道色、页脚与跨图引用。首轮渲染即非空且干净(viewBox 21887×17475)，« 计数=10 证实 5 个构造型正确渲染。

## Optimization Points
- 序列图参与者的「角色构造型」用 `participant "Name" as x <<角色>> #color`（stereotype 在 color 前）可稳定渲染为 «角色» 上标，是落地 §3.1「简洁标题+角色构造型」的最干净手段——比 `\n<size:11>副标题</size>` 更符合文字修饰步骤，应在序列图 howto 中作为推荐范式列出。
- 序列图的 note 天然贴 lifeline、布局安全，是 §3.2「外置详解」的理想载体；但仍需守「数量宜少(≤5)」——本图仅保留 2 个 note（货币锚 + 黑箱交叉引用），其余靠构造型自解释。
