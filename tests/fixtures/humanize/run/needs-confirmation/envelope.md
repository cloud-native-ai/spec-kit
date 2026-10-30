---
status: needs-confirmation
final_output: 已完成只读检查；删除步骤未执行
products: []
evidence:
  - pointer: "in-session observation: read-only inventory of run/needs-confirmation/ completed"
    kind: reading
failures: []
blocked_at: "step: delete stale fixture outputs (awaiting user confirmation; no answer available)"
anomaly_line: 未发现异常
---

# Envelope — needs-confirmation

指令执行到一个需要用户确认的步骤，而执行体无法取得答复：该步**不执行**，`blocked_at` 记录卡点，此前已完成的部分照常报告。

判读要点：

- `status: needs-confirmation` ⇒ `blocked_at` 必须非空；`products` 只含该步之前已完成的写入（本例为零）。
- verdict 取 `needs-confirmation`；`## Conclusion` 写「需要确认，未获答复」（EX-15）。
- 主会话不得代答、不得以「用户可能同意」继续、不得换等价动作绕开（EX-16）。
