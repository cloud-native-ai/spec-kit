---
status: completed
final_output: humanize-fixture-ok（会话内执行）
products: []
evidence:
  - pointer: "in-session observation: ran python3 -c print('humanize-fixture-ok') in the main session; stdout = humanize-fixture-ok"
    kind: reading
failures: []
blocked_at: null
anomaly_line: 未发现异常
---

# Envelope — degraded（in-session）

宿主没有原生派发通道：执行降级为 humanize 会话内执行（不是可选）。本信封只包含**会话内可观察的结果**。

判读要点：

- 载体标记写 `mode: in-session-degraded`，派发记录为 `dispatches: 0`；不得冒充原生子代理载体（EX-05 / EX-17）。
- 只把可观察结果当事实：不得把推断描述为子代理的观测，不得声称独立上下文或独立工具集。
- 降级不改五节、证据义务与保真底线（EX-18）。
