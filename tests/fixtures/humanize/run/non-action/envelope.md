---
status: not-an-action
final_output: null
products: []
evidence: []
failures: []
blocked_at: null
anomaly_line: 未发现异常
---

# Envelope — non-action

指令之后的文本是散文/聊天式提问，不是一个可执行动作；执行体没有执行任何动作，也没有输出或产物。

判读要点：

- `status: not-an-action` ⇒ verdict 按 requirements FR-019 取 `success`，但 `## Conclusion` 写「未执行任何动作」，**不得**称为执行成功。
- 无可报告输出：`## Evidence` 写 `none`，派发记录行仍须出现（`dispatches: 1`）。
- 裸文本调用仍需迁移提示整句一次（A4 / IP-09）。
