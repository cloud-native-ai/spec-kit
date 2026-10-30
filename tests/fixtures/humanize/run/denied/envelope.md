---
status: denied
final_output: null
products: []
evidence:
  - pointer: "user reply: 不要删除，停止"
    kind: reading
failures:
  - where: "step: delete stale fixture outputs"
    what: "用户拒绝确认：该步未执行，未执行任何替代动作；未执行范围 = tests/fixtures/humanize/run/needs-confirmation/ 的清理"
blocked_at: "step: delete stale fixture outputs (denied by the user)"
anomaly_line: 未发现异常
---

# Envelope — denied

用户**明确拒绝**确认那个破坏性步骤：该步未执行，也没有执行任何替代动作；拒绝原因与未执行范围记入 `failures`。

判读要点：

- `status: denied` ⇒ verdict 取 `aborted`（requirements FR-019），`## Conclusion` 文案写明「用户拒绝确认」与未执行范围。
- 零副作用：`products: []`，且运行前后 `git status --porcelain` 与目标哈希不变（SC-004）。
- humanize 只转达请求与答复，不等于代答（FR-008）。
