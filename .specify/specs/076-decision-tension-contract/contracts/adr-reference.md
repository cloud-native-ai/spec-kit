# Contract: ADR 张力引用位（adr-reference）

**Feature**: 076-decision-tension-contract → Feature 076 决策反题与反指标契约（Decision Tension Record）
**FR 覆盖**: FR-015
**载体**: `docs/decisions/template.md`（无镜像：`docs/` 不在 `MIRROR_PAIRS`）

本契约让三处（计划、ADR、测量来源）互相可达而互不复制。引用失败必须是一个错误，不是一个
「读者自己去对照」的提示：断链的引用比没有引用更糟，因为它看起来已经追溯过了。

## 条款

- **C-1** (slot in Alternatives): `## Alternatives` MUST gain a `tension_id` reference slot that points to a `T-NNN` record in the same feature's plan, MUST NOT copy any field of that record, and MUST require an explicit statement plus the threshold verdict when the decision has no load-bearing record rather than leaving the slot empty. (FR-015)
- **C-2** (dangling reference is an error): a `tension_id` that does not resolve to a record in the referenced plan MUST be reported as a broken-link error and MUST NOT be silently passed; resolution MUST reuse the record-index function of the deterministic validator so that one implementation serves both the validator's identifier check and this link check, and the check MUST be exercised by a contract test over a fixture pair containing a deliberately unresolvable id. (FR-015)

## 可追溯性

| 条款 | FR | 计划测试 |
|------|-----|----------|
| C-1 | FR-015 | test_adr_template_has_tension_slot_without_copy |
| C-2 | FR-015 | test_dangling_tension_id_is_an_error |

## FR 覆盖核对

- FR-015 由本文件 C-1…C-2 承接。
- 「无承重张力记录」这一处置的触发判据属 owner；本契约只断言该槽位必须要求它，不复述判据。
