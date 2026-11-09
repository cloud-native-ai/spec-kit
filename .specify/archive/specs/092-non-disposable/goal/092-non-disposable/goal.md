---
status: active
created: 2026-11-09
updated: 2026-11-09
---

# Goal: Non-Disposable（历史回顾与处置机制）

## Objective

引入 Non-Disposable 理念并用机制杜绝『用过即丢』：把 /speckit.history 扩展为『回顾 → 设计 → 用户确认 → 执行』，回顾当前 HEAD 工作树 .specify/ 下十类历史目录；以 080–090 回顾的 A–H 为验证语料，并把检出驱动到零。

## Success Criteria

1. SC 覆盖 A–H 八类检出（回顾、处置、取代、单 owner、重编号、状态可读、命令形态、修复 lane）
2. 机制可复现 A–H 检出：在语料树上跑出全部八类发现
3. 修复 lane 经用户确认后执行，并留下逐条证据

## Boundaries

- 不删除历史证据、不改写 git 历史、不建第二套历史存储

## History

- 2026-11-09 — created.
