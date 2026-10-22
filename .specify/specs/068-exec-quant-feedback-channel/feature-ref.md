# Feature Reference — 068

**Phase 1 output** (`/speckit.plan`, 2026-10-22).

## Bound Feature

| Field | Value |
|-------|-------|
| Feature ID | **Feature 068** |
| Name | 执行量化数据反馈回传与汇总（Exec-Quant Feedback Channel） |
| Registry row | `.specify/memory/features.md`（068 行，本阶段 Draft → Planned） |
| Detail file | `.specify/memory/features/068.md` |
| Spec path | `.specify/specs/068-exec-quant-feedback-channel/requirements.md`（unchanged） |
| Related | **059** — 前序与被修订对象（FR-011 仅打包腿修订）；零改写 059 制品 |

## Requirement → Feature stamp

`068-exec-quant-feedback-channel` → **Feature 068** 执行量化数据反馈回传与汇总。

## FR → Design Artifact Mapping

| FR | 腿 | Design 落点 | Contract clauses | 测试面（D11） |
|----|----|-------------|------------------|---------------|
| FR-001 | 打包 | research D1/D2 | C-PL-01/03 | test_feedback_exec_quant_payload |
| FR-002 | 打包 | D1/D2（只读扫描） | C-PL-01 | 同上（源存储零改动断言） |
| FR-003 | 打包 | D3（身份） | C-PL-05 | 同上（身份用例） |
| FR-004 | 打包 | D9 | C-PL-07 | 同上（输出报告断言） |
| FR-005 | 打包 | D7（封顶/降级） | C-PL-02/06/09 | 同上（降级用例） |
| FR-006 | 接收 | D4/D5 | C-IN-01/02/03/05 | test_feedback_intake_exec_quant |
| FR-007 | 接收 | D5/D6（归一） | C-IN-06, C-CS-05 | 同上 + aggregate 契约 |
| FR-008 | 接收 | D6（identity key） | C-IN-04 | 同上（幂等用例） |
| FR-009 | 接收 | D10 | C-IN-02, C-CS-04 | 同上（无载荷用例）+ 场景 5 |
| FR-010 | 接收 | D10 | C-IN-07 | 同上（损坏计数用例） |
| FR-011 | 汇总 | D8 | C-AG-02/03/06 | test_exec_quant_aggregate |
| FR-012 | 汇总 | D5/D8 | C-AG-05, C-IN-05 | 同上（落盘形态断言） |
| FR-013 | 汇总 | D8 | C-AG-04 | 同上（零臆造审计断言） |
| FR-014 | 汇总 | D8 | C-AG-06, C-CS-01 | 同上（零网络/本地断言） |
| FR-015 | 边界 | D12（继承 059 遮蔽） | C-CS-02 | 契约（凭据扫描用例） |
| FR-016 | 边界 | D12 | C-CS-01 | 契约（零网络断言） |
| FR-017 | 边界 | D1/D4/D8（动作面只增不改） | C-CS-03 | 既有套件全量比对 |
| FR-018 | 边界 | D11 | C-CS-03 | 基线逐名比对（场景 4） |
| FR-019 | 打包 | D9 | C-PL-08 | payload 契约（空条目用例） |

## SC → Measurement Mapping

| SC | 测量源（requirements § Measurement Sources） | 本阶段已落地证据 |
|----|---------------------------------------------|------------------|
| SC-001 | 样例项目实测打包 + 双侧清点 | 场景 1（route b 钉住）；清点形态 = C-PL-01/03 |
| SC-002 | 双形态实测打包 | 场景 0 route a 实测布局差异；契约双布局用例 |
| SC-003 | 接收对账 + 幂等增量 | 场景 2（route b）；C-IN-04/05 |
| SC-004 | 汇总 + 抽检对账 + 臆造审计 | 场景 3（route b）；C-AG-03/04 |
| SC-005 | 凭据扫描 + 网络零次 | C-CS-01/02；契约扫描用例 |
| SC-006 | 套件全量 + 名字级基线 + 基线包零差异 | **基线已冻结**（test-evidence/log-baseline-pre-impl.txt）；场景 4/5 |

## Feature list review（create-plan § Feature Integration duty）

- 本 plan **不新增** Feature、不废弃/合并既有 Feature——068 已于 clarify 注册
  （Draft），本阶段仅推进状态。
- 功能/非功能分类零变化；059 行零触碰（派发约束 + Binding Rules 偏离已披露于
  features/068.md）。
- 状态机：`Draft → Planned`（canonical state machine，`.specify/templates/`
  feature-details-template.md § Canonical Status State Machine）；**不得**落
  `Implemented`（该转移属 `/speckit.implement`）。
