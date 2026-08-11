---
title: sync-mirrors 逐文件错误收集
status: parked
parked_at: 2026-08-12
origin: 反馈积压处置(2026-08-10 improve-skills git-workflow 运行)
tags: [sync-mirrors, engine, robustness]
---

`sync-mirrors.py --write` 在首个 PermissionError 处中止但仍打印后续计划的 DIFF 行,导致若干镜像文件静默保持陈旧(案例:5 个 root-owned 的 `.specify/skills/git-workflow/*` 文件)。改进方向:逐文件收集错误、继续处理其余文件、结尾非零退出并汇总失败清单;同时在 AGENTS.md 常犯教训中把 root-owned 目录条目扩展至镜像文件。

## Evolution Log

- 2026-08-12 parked(自反馈批次 20260810T120039Z)。引擎健壮性改造,需配套测试,走独立小需求。
