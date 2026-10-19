# Contract: Plan 阶段「只小修、不重审」约束（plan-constraint）

**Feature**: 063 → Feature 058（演化）
**FR 覆盖**: FR-020…FR-025
**载体**: `references/efficiency-model.md`、`references/stage-prompts.md`、`scripts/audit-plan-changes.py`、`docs/reference/skills/sdd-loop-driver.md`

- **PC-01（生效点与制品面）**: `plan` 阶段 U4 通过后，驱动 MUST 在状态脊把约束登记为 `plan_constraint=active`，记录 `activated_at` 与 `plan_commit`；约束覆盖的 plan 拥有制品 = `plan.md`、`data-model.md`、`contracts/`、`quickstart.md`、`research.md`、`feature-ref.md`（FR-020/FR-024）。`plan_commit` 同时是「已批准需求基线」的锚点（FR-022，见 PC-06）。
- **PC-02（小修定义）**: 小修 MUST 限于：错别字/措辞、断链/引用修复、格式、行级一致性；MUST NOT 改变范围、架构方向、数据模型语义、契约语义、FR/SC 内容或任务分解范围（FR-020）。
- **PC-03（实质改动定义）**: 实质改动 = 改变上述任一项、引入新能力/安全面，或多处小修合并后按最终 diff 判定为改变语义。分类 MUST 按最终差异判定，MUST NOT 按单次编辑的措辞规避（FR-022，edge case）。
- **PC-04（下游提示词块）**: 约束 active 后，`tasks` / `analyze` / `implement` / `review` 的提示词 MUST 携带只小修块，并规定：任何 plan 制品改动 MUST 在完成哨兵前的回传中包含 `PLAN-EDIT:` 声明行；声明行的完整格式由 `references/efficiency-model.md` §3.2 单一 owner 定义（本契约只钉住前缀 token）。需要实质改动且无法在约束下继续时，MUST 以显式异常行 [[STR-005]] 回传建议改动与实质性理由，MUST NOT 静默改写 plan 或自行重跑 plan 阶段（FR-020/FR-021）。
- **PC-05（U4 校验）**: 驱动 MUST 在每个下游阶段 U4 检查 `git diff --name-only <stage-base>..HEAD -- <plan-owned paths>` 与 `git status --porcelain -- <plan-owned paths>`（未提交改动）；两者合并为触碰集合。凡触碰 plan 制品的改动 MUST 被分类为 `minor` / `substantive` / `undeclared`。`undeclared` 或 `substantive` MUST 先判该阶段门失败，再进入 PC-06 分流（FR-022）。
- **PC-06（确定性两分支）**: 门失败后的分流 MUST 为：
  - (a) 改动为修复既有缺陷所必需，且不改变已批准的需求范围/FR/SC 语义、架构方向、数据模型语义、契约语义或任务分解范围 → 驱动派发完整 plan 重审，记录触发与证据；重审通过后对门失败阶段做一次 U4 复验，不做静默无限重审。
  - (b) 改动改变上述任一项、引入新能力/安全面，或驱动无法确定 → 作为决策以四要素上送，MUST NOT 自行重审。
  - 「已批准需求基线」= E4 `plan_commit` 提交中 `requirements.md` 的 FR/SC 定义集合与语义；每次分类记录 MUST 写入 `approved_baseline_commit`（= `plan_commit`），分支 (a)/(b) 的判定 MUST 以该提交为比较对象，MUST NOT 以工作树当前文本或其它提交替代（FR-022）。
  - 每一次 `substantive`/`undeclared` 改动都 MUST 按其所属分支处置并留痕，MUST NOT 因次数而跳过分流；若同类改动反复出现，沿用既有 stall/retry 纪律（阶段超时与重试上限）停环上送，而不是静默循环（FR-022）。
- **PC-07（analyze 修复路由不变）**: 本约束 MUST NOT 取消或削弱 analyze 门的上游修复路由：analyze 发现仍须回到所属制品修复并重过该门；约束只限制修复规模与重审开销（FR-023）。
- **PC-08（收口报告）**: 每个运行 MUST 在收尾汇总报告约束是否 active、是否发生过 plan 制品改动、每项分类与处置去向（FR-024）。
- **PC-09（显式排除与设计代价）**: 框架命令内部的硬执行 MUST 作为显式排除项；约束是编排层纪律，驱动是执行点。已接受的设计代价 MUST 明确记录：非驱动手工调用阶段命令不受约束；若后续证明编排层实现不安全，MUST 另立特性修订，不得静默扩大范围（FR-025）。
- **PC-10（确定性辅助脚本）**: `scripts/audit-plan-changes.py` MUST 机械输出：`touched_paths[]`（提交区间 + 未提交改动）、`declaration_lines[]`、`undeclared` 判定（触碰但无声明）、diff 统计；语义 `minor`/`substantive` 分类由驱动在状态脊记录理由。脚本 MUST 自包含（Python 标准库）、MUST NOT 修改工作树。

## 可追溯性

| 条款 | FR | 计划测试 |
|------|-----|----------|
| PC-01 | FR-020, FR-024 | `test_pc_01_activation_point` |
| PC-02 | FR-020 | `test_pc_02_minor_definition` |
| PC-03 | FR-022 | `test_pc_03_substantive_final_diff` |
| PC-04 | FR-020, FR-021 | `test_pc_04_prompt_block_and_plan_edit` |
| PC-05 | FR-022, SC-006 | `test_pc_05_u4_diff_check` |
| PC-06 | FR-022 | `test_pc_06_routing_branches` |
| PC-07 | FR-023 | `test_pc_07_analyze_repair_unchanged` |
| PC-08 | FR-024 | `test_pc_08_wrapup_reporting` |
| PC-09 | FR-025 | `test_pc_09_explicit_exclusion` |
| PC-10 | FR-022 | `test_pc_10_audit_script_interface`；单测 `test_audit_plan_changes.py` |
