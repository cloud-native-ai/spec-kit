---
status: failed
final_output: null
products: []
evidence:
  - pointer: python3 -c raise SystemExit(3)
    kind: command
  - pointer: exit code 3
    kind: reading
failures:
  - where: "step: run fixture command"
    what: "exit code 3 — command aborted before producing output"
blocked_at: null
anomaly_line: "ANOMALY: 夹具命令以退出码 3 结束；执行体未重试，humanize 未补发"
---

# Envelope — failure

一次失败的运行：命令以退出码 3 结束，没有输出与产物，失败坐标（载体 / 阶段 / 错误信息）齐备。

判读要点：

- `status: failed` ⇒ verdict 取 `failure`（requirements FR-019）；`## Conclusion` 不得使用成功措辞。
- `## Evidence` 必须给出失败证据（命令 + 退出码），而不是只写「执行失败」。
- 失败**不重试**：本信封只代表一次执行尝试；出现第二个顶层派发即判违反（EX-01 / EX-12）。
