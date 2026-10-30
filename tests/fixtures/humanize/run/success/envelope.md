---
status: completed
final_output: humanize-fixture-ok
products: []
evidence:
  - pointer: python3 -c print('humanize-fixture-ok')
    kind: command
  - pointer: exit code 0
    kind: reading
failures: []
blocked_at: null
anomaly_line: 未发现异常
---

# Envelope — success

一次可确定产出的运行：执行体打印 `humanize-fixture-ok` 并以退出码 0 结束，没有产物、没有失败、没有卡点。

判读要点（对应 `data-model.md` § E5 不变量）：

- `status: completed` 且 `final_output` 非空 ⇒ `## Conclusion` 的 verdict 取 `success`（映射 owner 是 requirements FR-019）。
- `evidence` 的 `command` 项与 `exit code 0` 的 `reading` 项成对，构成 `## Evidence` 的可定位指针。
- 顶层派发恰好一次；派发记录行由主会话在报告里写为 `dispatches: 1`（EX-21 的计数口径）。
