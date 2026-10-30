---
title: 测试套件提速五项优化（xdist / slow marker / 会话缓存 / 去 sleep / 进程内直调）
status: parked
parked_at: 2026-10-30
origin: user message during sdd-loop-driver run for 078-bilingual-expression (mid-implement)
tags: [test-infrastructure, performance, pytest]
---

用户提出的 5 条优化建议（原文要点，收益/风险视角）：

1. **引入 pytest-xdist，`-n auto`**：测试都不写仓库根（实测 0 处）、临时目录隔离，具备并行条件。按 8–12 核估算，612s 有望降到 2–3 分钟。建议先只并行 `tests/contract` 验证。
2. **给慢测试打 `slow` marker**：integration 的进程/队列类 + 少数全语料扫描型 contract；PR 默认 `-m "not slow"`，全量留给每日或 closure。
3. **会话级缓存全语料扫描结果**：`coverage_receipt` / `clause_coverage` 的仓库遍历改为 session fixture。
4. **去固定 sleep**：`client_metrics` 的 1.1s×8 换成注入时钟/单调序号；runner 测试用事件文件替代固定等待。
5. **能走进程内 API 的不要起子进程**：319 次 `subprocess.run` 里有一部分是 specify CLI / 纯 Python 引擎调用，改直调可省掉解释器启动成本。

## Evolution Log

- 2026-10-30 parked（mid-loop；未在 078 运行中实施，以免改变 baseline/closure 测试口径）。
