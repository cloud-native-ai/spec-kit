---
status: active
created: 2026-11-09
updated: 2026-11-09
---

# Goal: 093-concurrency-by-default

## Objective

所有 skills、/speckit.* 命令、goal、team、loop 把 subagent 并发作为基本属性：依赖、写域、宿主与预算允许时默认并发；串行须具名理由并可判别；执行体具备派发能力或由驱动者直接派发。

## Success Criteria

1. 各执行体声明 default-concurrent 与具名串行例外。
2. 契约测试可判别 default-concurrent / serial-exception。
3. 至少一个真实执行体完成 6 包 worktree 并发与确定性集成。
4. 派发能力在 agent/阶段席位/执行体中在位，禁止声明并行而实际串行。

## Boundaries

- 不新增 /speckit.* 命令、第二个派发引擎；无条件并行不允许；不改 SDD 阶段链与哨兵。

## History

- 2026-11-09 — created.
