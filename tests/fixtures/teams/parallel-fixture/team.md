---
name: parallel-fixture display name
slug: parallel-fixture
description: synthetic parallel team — fixture for SC-001 pattern coverage
goal: >
  验证 parallel 模式的团队能仅凭 tracked 工件产出目标级总结。
  成功标准:表单校验通过且无需人工补填;每个工作项可归属到产出团队;阶段按团队命名空间化。
goal_slug: parallel-fixture-goal
pattern: parallel
created: 2026-08-01
updated: 2026-08-04
members:
  - agent: agent-team-supervisor-template
    role: team-supervisor
    lifecycle: persistent
  - agent: agent-stage-executor-template
    role: stage-executor
    lifecycle: temporary
config:
  maturity: L1
---

## Goal
验证 parallel 模式的团队能仅凭 tracked 工件产出目标级总结。

## Static Structure
| Role | Stage | Type | Lifecycle |
|------|-------|------|-----------|
| team-supervisor | optimizer | Meta | persistent |
| stage-executor | executor | Worker | temporary |

## Dynamic Structure
pattern: parallel
