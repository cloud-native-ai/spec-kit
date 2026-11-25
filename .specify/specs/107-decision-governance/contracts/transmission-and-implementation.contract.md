# Contract: 传递与实施（transmission-and-implementation）

**Feature**: 107-decision-governance → Feature 107 Decision Governance（AI Agent 决策项治理）
**FR 覆盖**: FR-018…FR-021
**载体**: `shared/definitions/decision-definitions.md`（决策块、确认与回执形态）；通道与上行规则归 `shared/definitions/superagent-definitions.md`（七角色字段 + 四项注入 + 五要素上行）。

本契约规定「superagent 的决策如何完整跨过角色边、实施结果如何被钉回决策编号」。不新建传输机制：决策块是既有派发载荷中的任务权威内容。

## 条款

- **C-301** (decision block, existing channel): a decision delegated for implementation MUST travel as a `decision_block` inside the existing dispatch payload, carrying `decision_id`, `decision_class`, the chosen option's full label, implementation constraints and the archive pointer; the seven role fields and the four pre-existing injections MUST remain unchanged, and the block MUST NOT be treated as an eighth role field. (FR-018, A-7)
- **C-302** (refusal at construction): a decision-backed dispatch without a block, or with a block missing any of the five fields, MUST be refused at payload construction (M-06); a non-decision dispatch without a block is legal (BC-02 bridge). (FR-018)
- **C-303** (acknowledgement): the child's return MUST contain an acknowledgement that echoes the `decision_id` and states acceptance for implementation (or the anomaly escalation); the acknowledgement rides the existing return, and no new message class or channel is introduced; on the parent side it drives the record's `acknowledged_at` and advances `transmission_status` to `acknowledged` (C-202). (FR-019)
- **C-304** (implementation receipt): the return MUST contain an `implementation_receipt` with `decision_id`, an implementation summary, evidence pointers and a divergence declaration (`none` or `diverged` + reason); a missing item makes the return incomplete, and the parent MUST NOT consume the conclusion or backfill the missing fields (existing uplink rule); the receipt MUST drive the record's `implemented_at`, the implementation-result dimension on `transmission_status` and the `diverged` phase per C-202. (FR-019)
- **C-305** (no silent re-decision): a child MUST NOT silently re-decide; when the context invalidates the decision it MUST stop at the anomaly point and escalate in the fast-fail surface-report form; neither a decision without a record/id nor an unparseable `decision_id` may be implemented. (FR-020)
- **C-306** (auditable chain): every transmitted decision MUST leave an auditable chain — decision record → dispatch attempt (role-edge identity / run report) → implementation receipt; a broken link MUST be a reportable explicit anomaly and MUST NOT be silent. (FR-021)
- **C-307** (multi-hop): in a multi-hop chain every hop's payload carries the decision block and every hop's receipt references the same `decision_id`; the final receipt and the original record MUST join into one chain. (FR-021 edge case)
- **C-308** (re-decision after invalidation): the parent re-decides and leaves a new record; the old record and the old receipt are preserved, and the new record supersedes the old one by `superseded_by`. (FR-020 edge case)

## 可追溯性

| 条款 | FR | 计划测试 |
|------|-----|----------|
| C-301 | FR-018 | `test_decision_governance_guards.py::test_m06_block_completeness` |
| C-302 | FR-018 | `test_decision_governance_guards.py::test_m06_dispatch_without_block_refused` |
| C-303 | FR-019 | `test_decision_governance_guards.py::test_acknowledgement_present` |
| C-304 | FR-019 | `test_decision_governance_guards.py::test_m05_receipt_reverse_samples` |
| C-305 | FR-020 | `test_decision_governance_guards.py::test_silent_redecision_is_anomaly` |
| C-306 | FR-021 | `test_decision_governance_guards.py::test_m07_chain_three_segments` |
| C-307 | FR-021 | `test_decision_governance_guards.py::test_multi_hop_same_id` |
| C-308 | FR-020 | `test_decision_governance_guards.py::test_supersession_preserves_old` |

## FR 覆盖核对

- FR-018…FR-021 由本文件 C-301…C-308 承接。
- 角色边身份、上行五要素、消息类别与重试归 `superagent-definitions.md`；本契约只新增决策块与回执的内容义务，不复述通道规则。
