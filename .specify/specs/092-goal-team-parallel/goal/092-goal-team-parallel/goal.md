---
status: active
created: 2026-11-09
updated: 2026-11-09
---

# Goal: 092-goal-team-parallel

## Objective

让 goal/team 与 spec(SDD) 成为平行执行线：goal/team 可在 /speckit.* 命令运行中创建并归档到 .specify/goal|teams；spec 与 goal+team 各自可设计/执行，复杂工作由 spec 设计、goal+team 执行；用 owner/lifecycle/write-scope 绑定模型替代「临时/全局」。

## Success Criteria

1. goal/team 可由 /speckit.* 命令运行创建并归档到 .specify/goal|teams。
2. 不存在 .specify/specs/<spec>/goal|team 的新写入路径；旧数据 archive-not-delete 迁移。
3. spec 与 goal+team 的平行关系与复杂工作交接契约可判定。
4. 「临时/全局」由绑定/生命周期模型替代，且路由、驱动、目录地图与命令模板各 owner 同步。

## Boundaries

- 不新增 /speckit.* 命令、第二个 goal/team 引擎；不破坏性迁移；不改 SDD 阶段链与哨兵。

## History

- 2026-11-09 — created.
