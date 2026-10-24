# Feature Reference — 069a（Feature 069 切片）

**Phase 1 output**（`/speckit.plan`，2026-10-24）。

## Bound Feature

| Field | Value |
|-------|-------|
| Feature ID | **Feature 069** |
| Name | 执行/表达二元分类与文档型 SDD 同构（Execution/Expression Classes & Document-Form SDD） |
| Slice | `069a-flow-classification-docs-gates` |
| Registry row | `.specify/memory/features.md`（069 行，本阶段 Draft → Planned；零新增行） |
| Detail file | `.specify/memory/features/069.md`（本阶段追加切片计划记录） |
| Spec path | `.specify/specs/069a-flow-classification-docs-gates/requirements.md`（**零改动**） |
| Parent authority | `.specify/specs/069-execution-expression-sdd/requirements.md`（父规格的 FR / SC 定义不变；定义数以父文件为准） |

## Requirement → Feature stamp

`069a-flow-classification-docs-gates` → **Feature 069** 执行/表达二元分类与文档型 SDD 同构（切片 069a）。

## FR → Design Artifact Mapping

| FR | 设计落点（文件 / owner 章节） | 契约条款 | 测试面 |
|----|------------------------------|----------|--------|
| FR-001 | `shared/definitions/flow-class-definitions.md` § 判据/取值 + § 台账 | `flow-class-ledger.md` C-1 / C-3 / C-4 | `test_flow_class_ledger` |
| FR-002 | 同上 § 判据（唯一问题 + oracle 二分） | C-2 | `test_flow_class_ledger`（basis 枚举）+ `test_expression_gates_doc`（判据不被复述） |
| FR-003 | 同上 § 边界例（契约→执行、架构文档→表达、构建不改判定） | C-2 / C-4 | `test_flow_class_ledger`（`/speckit.docs` 与 `create-pages` 对照行） |
| FR-004 | `shared/workflow/feedback-step.md` **+1 行正交指针**；`expression-gates.md` § 边界 | `expression-gate-operators.md` C-13 | `test_expression_gates_doc` |
| FR-005 | owner 单文件；两引擎只读 | `flow-class-ledger.md` C-1 / C-2 | `test_flow_class_ledger`（第二份分类数据文件负向断言） |
| FR-006 | owner § 判据（两次独立判定的一致率要求由 SC-001 测量） | C-2 | `test_expression_gates_doc`（单一 owner 指针 ⇒ 单一读法） |
| FR-007 | `scripts/python/flow-class-check.py --action check` | `flow-class-ledger.md` C-5 | `test_flow_class_ledger`（缺口/unknown + 反空真下限） |
| FR-008 | 台账主键 = 单元 id | C-6 | `test_flow_class_ledger`（duplicate / dual-class） |
| FR-009 | `--action lookup` 默认分支 + `marker` | C-7 | `test_flow_class_ledger`（默认 + 标记，且不得呈现为已判定） |
| FR-010 | owner § 类中立清单 | C-8 | `test_flow_class_ledger`（清单封闭 / 枚举 / rationale） |
| FR-011 | owner 抬头（所有权归框架） | C-14 | `test_flow_class_ledger`（客户项目侧形态） |
| FR-012 | `expression-gates.md` § 阶段不变量 | C-10 / C-11 | `test_expression_gates_doc` |
| FR-013 | `expression-gates.md` § 阶段算子表（只换算子） | `expression-gate-operators.md` C-1 / C-2 / C-3 | 同上 |
| FR-014 | 同上 § 阶段完整性不读类别 | C-11 | 同上（负向：无跳过表述） |
| FR-015 | `flow-class-check.py --action lookup` 为唯一读取点 | `flow-class-ledger.md` C-9 | `test_flow_class_ledger`（模板/技能零类别字面量） |
| FR-016 | `lookup` 降级分支（`source=default` + `marker` + stderr `owner-unparsable`） | C-7 | `test_flow_class_ledger` |
| FR-017 | owner § 变更记录 | C-12 | `test_flow_class_ledger`（变更记录行形态） |
| FR-018 | `expression-gates.md` § 六面 | `expression-gate-operators.md` C-1 | `test_expression_gates_doc` |
| FR-019 | 同上 § 读者声明；检查器 `reader` 面 | C-4 + `doc-consistency-checker.md` C-4 | `test_doc_consistency_checker`（缺失即阻断） |
| FR-020 | 同上 § 证据等级与 as-of；检查器 `evidence` 面 | C-5 + `doc-consistency-checker.md` C-3 | `test_doc_consistency_checker`（配对 / 畸形 / 过期） |
| FR-021 | 同上 § 构建只是必要条件 | C-6 | `test_expression_gates_doc`（负向条款在场） |
| FR-022 | 同上 § 事实唯一性；检查器 `duplicate` 面 | C-7 + `doc-consistency-checker.md` C-5 | `test_doc_consistency_checker`（副本聚类 + 修复方向） |
| FR-023 | 同上 § 评审面 | C-8 | `test_expression_gates_doc` |
| FR-024 | 同上 § 三项基线；记录形态 E8 | C-9 | `test_expression_gates_doc` + 场景 3 |
| FR-025 | owner 首批成员两行；零改动约束 | C-11 + `expression-gate-operators.md` C-12 + `compatibility-distribution.md` C-5 | `test_expression_compatibility` |
| FR-026 | 只引用前序三特性 | `compatibility-distribution.md` C-5 / C-9 | `test_expression_compatibility`（三份哈希） |
| FR-027 | 复用既有通道 | `compatibility-distribution.md` C-8 | `test_expression_compatibility`（无新存储路径） |

## SC → Measurement Mapping

| SC | 测量源（requirements § Measurement Sources） | 本阶段已落地证据 / 待实现面 |
|----|---------------------------------------------|------------------------------|
| SC-001 | 两名独立判定者结论落盘后逐条比对 | 判据单一 owner + 台账；判定演练属实现期（测试钉住「判据不被复述」以排除第二种读法） |
| SC-002 | 台账 ↔ 清单机械对账；消费点标注率 | 场景 1 route b；`check`/`lookup` 契约（C-5/C-7） |
| SC-003 | 3 个文档型特性的阶段记录与 review 报告 | 阶段不变量（gates C-11）；样本选取属实现期 |
| SC-004 | 冻结基线 vs 收尾复测（门禁调用次数） | 基线来源实测可用（场景 3）；判据 gates C-9 |
| SC-005 | 人工确认次数 | 同上（门控观察记录 + clarify 轮次） |
| SC-006 | requirements→analyze 墙钟 | 同上（`git log` + 运行判定记录） |
| SC-007 | 注入式演练（副本 / as-of / 手打计数） | 检查器契约 C-9 的三类注入夹具；场景 2 |
| SC-008 | `062/067/068` `requirements.md` 字节比对 | **已实测分母**：`987b24ea…` / `29e26b70…` / `ec20d5e2…`（场景 4） |

**基线边界（诚实披露）**：SC-004 / SC-005 / SC-006 的**仪器口径与 `not-evaluated` 降级**归 069b（父编号 041）。本切片交付「能取数 + 记录形态 + 冻结/对照要求」；
若实现期可用的真实表达类特性不足 3 个，记 `not-evaluated` 并写明原因，不记达成（不留 0）。

## Feature list review（create-plan § Feature Integration duty）

- 本 plan **不新增** Feature、不废弃/合并既有 Feature。Feature 069 已由 2026-10-24 clarify 注册；切片复用同一 Feature ID 与同一注册行。
- 功能 / 非功能分类零变化；062 / 067 / 068 的注册行与记忆文件零触碰（只引用）。
- 切片登记写在 `.specify/memory/features/069.md` § Related Specifications/Requirements（既有行，本阶段补 plan 产物指针）。
- 状态机：`Draft → Planned`（canonical state machine，`.specify/templates/feature-details-template.md` § Canonical Status State Machine）；
  本阶段**不得**落 `Implemented`（该转移属 `/speckit.implement`）。判据满足：`plan.md` / `data-model.md` / `contracts/` / `quickstart.md` 四件齐备 + Constitution Check 无未证成 Fail。
- 069b **不预建**：本阶段不创建 `069b-isomorphism-migration-metrics` 目录、不复制其 FR 正文（SA-6）。
