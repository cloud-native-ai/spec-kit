---
id: "20260730T022515Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "20260730T022200Z-agent-template-monitor"
scope: "local"
partial: false
created: "2026-07-30T02:25:15Z"
summary: "以 /improve-skills 入口收到监控类任务，判定与技能输入契约失配后改走 requirement-implement-monitor 团队 Cycle 1（新目标 agent-template-consolidation 全量基线，SCORE 0.8775，HP-1 一项待人工决策），对监控对象零写入。"
---

## Review
以 /improve-skills 入口收到监控类任务，判定与技能输入契约失配后改走 requirement-implement-monitor 团队 Cycle 1（新目标 agent-template-consolidation 全量基线，SCORE 0.8775，HP-1 一项待人工决策），对监控对象零写入。

## Optimization Points
- 触发/路由失配：用户经 /improve-skills 下达的是"持续监控并评价另一 agent 表现"任务，不满足本技能"定位单一目标 Skill 并编辑"的输入契约；且 L1 监控红线（对监控对象零写入）与本技能的"编辑 skill"目的直接冲突。本次按既有 requirement-implement-monitor 团队 run 处理并向用户说明。建议：improve-skills 的 Input Contract 增加一条显式分流指引——当描述的意图是"监控/评价执行过程"而非"修改某个 skill"时，指向 create-team/improve-team（continuous 监控团队）而不是继续解析目标 Skill。
