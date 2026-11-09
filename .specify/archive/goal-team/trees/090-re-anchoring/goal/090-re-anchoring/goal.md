---
status: active
created: 2026-11-08
updated: 2026-11-08
---

# Goal: Re-Anchoring（不忘初心 · 温故而知新）

## Objective

把「开局加载一次规则」改为「每核心步骤按 T0/T1/T2 分层重载并评估」：入口固化任务锚 + 规则锚，五问规则优先，三值判定；owner 文档、两侧宪法、两侧指令面、agent 义务五处同时存在且以指针互引。

## Success Criteria

1. SC-001 五处落点同时存在且以指针互引（契约测试）
2. SC-002 五问顺序在 checkpoint 协议中明确为规则优先，并有契约测试钉住
3. SC-003 双落地计数与 watchlist 同批移动，计数守卫与基线失败集对齐
4. SC-004 T0/T1/T2 分层在 owner 文档与 checkpoint 协议中一致

## Boundaries

- 不新增评分器、日志服务、调度器或第二个 checkpoint 系统
- 不改变阶段序列、哨兵字面量、watcher 判定与退出码

## History

- 2026-11-08 — created.
