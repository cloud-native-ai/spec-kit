---
title: Agent 会话自定义命名适配
status: parked
parked_at: 2026-08-12
origin: /speckit.todo 运行期间临时产生(038-goal-target SDD 流程会话中)
tags: [agent-integration, session, cli-adaptation]
---

设计 Agent 适配方案,支持在执行命令的特定阶段或采用特定方法时,对 Agent 当前执行的 Session 进行自定义命名,替代系统自动生成的 Session 名。

范围裁定(用户确认 2026-08-12):对象是 **AI agent CLI 会话**(Claude Code / Codex CLI / Qoder CLI / GitHub Copilot / opencode / Hermes Agent 各自的会话标识与名称)——例如 `/speckit.team run` 派发外部 CLI 成员时给会话命名,便于追溯;不包括 Spec Kit 记忆会话层(`.specify/memory/session/`)。

待研究(晋升前必须完成):各家 CLI 是否暴露会话命名/重命名的官方机制(查官方文档,不猜 flag);若无官方机制,降级方案(如首条 prompt 约定前缀、工作目录命名、run report 记录映射表)的取舍。

## Evolution Log

- 2026-08-12 parked。与当前代码和实践暂无直接挂接,随项目演进再评估是否晋升为 TODO 块或需求规格。
