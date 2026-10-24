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
| Spec path | `.specify/specs/069a-flow-classification-docs-gates/requirements.md`（本阶段零改动；最小接线由 FR-015「判定前从唯一所有者读取」与 FR-025「只允许按 FR-018 补强」授权，不新增/不削弱条款） |
| Parent authority | `.specify/specs/069-execution-expression-sdd/requirements.md`（父规格的 FR / SC 定义不变；定义数以父文件为准） |

## Requirement → Feature stamp

`069a-flow-classification-docs-gates` → **Feature 069** 执行/表达二元分类与文档型 SDD 同构（切片 069a）。

## FR → Design Artifact Mapping

| FR | 设计落点（文件 / owner 章节） | 契约条款 | 测试面 |
|----|------------------------------|----------|--------|
| FR-001 | `shared/definitions/flow-class-definitions.md` § 判据/取值 + § 台账 | `flow-class-ledger.md` C-1 / C-3 / C-4 | `test_flow_class_ledger` |
| FR-002 | 同上 § 判据（唯一问题 + oracle 二分）+ 台账 `basis` 列（`behavior-oracle` / `reader-oracle` / `mixed-oracle`） | C-2 / C-4 | `test_flow_class_ledger`（basis 枚举）+ `test_expression_gates_doc`（判据不被复述） |
| FR-003 | 同上 § 边界例（契约→执行、架构文档→表达、构建不改判定） | C-2 / C-4 | `test_flow_class_ledger`（`/speckit.docs` 与 `create-pages` 对照行） |
| FR-004 | `shared/workflow/feedback-step.md` **+1 行正交指针**；`expression-gates.md` § 边界 | `expression-gate-operators.md` C-13 | `test_expression_gates_doc` |
| FR-005 | owner 单文件；两引擎只读 | `flow-class-ledger.md` C-1 / C-2 | `test_flow_class_ledger`（第二份分类数据文件负向断言） |
| FR-006 | owner § 判据（两次独立判定的一致率要求由 SC-001 测量；固定 fixture 的机器比对由 `test_flow_class_correctness` 钉住） | C-2 | `test_flow_class_correctness`（oracle 比对 + 变异断言）+ `test_expression_gates_doc`（单一 owner 指针 ⇒ 单一读法） |
| FR-007 | `scripts/python/flow-class-check.py --action check` | `flow-class-ledger.md` C-5 | `test_flow_class_ledger`（缺口/unknown + 反空真下限） |
| FR-008 | 台账主键 = 单元 id | C-6 | `test_flow_class_ledger`（duplicate / dual-class） |
| FR-009 | `--action lookup` 默认分支 + `marker` | C-7 | `test_flow_class_ledger`（默认 + 标记，且不得呈现为已判定） |
| FR-010 | owner § 类中立清单 | C-8 | `test_flow_class_ledger`（清单封闭 / 枚举 / rationale） |
| FR-011 | owner 抬头（所有权归框架） | C-14 | `test_flow_class_ledger`（客户项目侧形态） |
| FR-012 | `expression-gates.md` § 阶段不变量 | C-10 / C-11 | `test_expression_gates_doc` |
| FR-013 | `expression-gates.md` § 阶段算子表（只换算子）+ § 调用点表（入口 → 阶段 → 算子） | `expression-gate-operators.md` C-1 / C-2 / C-3 / C-14 | `test_expression_gates_doc` |
| FR-014 | 同上 § 阶段完整性不读类别 | C-11 | 同上（负向：无跳过表述） |
| FR-015 | `flow-class-check.py --action lookup` 为唯一读取点；`/speckit.docs` 在命令模板内调用（W1），`/speckit.humanize` 在其委派技能 Stage 6 调用（W4，命令模板只给 owner 指针 W2），`create-docs` 技能只引 owner（W3） | `flow-class-ledger.md` C-9 / C-15 | `test_flow_class_ledger`（零类别字面量）+ `test_expression_gate_wiring`（A1–A6，含 humanize 模板零脚本调用） |
| FR-016 | `lookup` 两条互斥降级路径（未登记：`source=default` + `marker`；owner 不可解析：默认类语义 + `marker` null + stderr `owner-unavailable`）+ 调用点降级（`owner-unavailable`，保持既有门禁） | C-7 + `expression-gate-operators.md` C-15 | `test_flow_class_ledger` + `test_expression_gate_wiring`（降级字面量在场） |
| FR-017 | owner § 变更记录 | C-12 | `test_flow_class_ledger`（变更记录行形态） |
| FR-018 | `expression-gates.md` § 六面（封闭，恰好 6，每面一个 face id）+ § 调用点表；`/speckit.docs` 与 `create-docs` R6 实际执行文档型算子 | C-1 + C-14 | `test_expression_gates_doc`（exactly 6 + face id 一一对应）+ `test_expression_gate_wiring`（A1/A3） |
| FR-019 | 同上 § 读者声明；检查器 `reader` 面；docs 路径实际调用检查器 | C-4 + `doc-consistency-checker.md` C-4 / C-10 | `test_doc_consistency_checker`（缺失即阻断）+ `test_expression_gate_wiring`（docs 含 checker） |
| FR-020 | 同上 § 证据等级与 as-of 与 `source`（三件套成组）；检查器 `evidence` 面（含 `source-missing`） | C-5 + `doc-consistency-checker.md` C-3 | `test_doc_consistency_checker`（配对 / 畸形 / 过期 / 缺来源） |
| FR-021 | 同上 § 构建只是必要条件 | C-6 | `test_expression_gates_doc`（负向条款在场） |
| FR-022 | 同上 § 事实唯一性 + 检测下限的承认；检查器 `duplicate` 面 | C-7 + `doc-consistency-checker.md` C-5 | `test_doc_consistency_checker`（副本聚类 + 修复方向 + 下限说明） |
| FR-023 | 同上 § 评审面（判定者与判定对象）；humanize 最小集保留 `062-reviewer-report` | C-8 + C-14 | `test_expression_gates_doc` + `test_expression_gate_wiring`（A2/A3：062 保真与报告不被削弱） |
| FR-024 | 同上 § 三项基线（冻结时点 + 单阶段确认 ≤3）；记录形态 E8 | C-9 | `test_expression_gates_doc` + 场景 3 |
| FR-025 | owner 首批成员两行 + 最小指定接线（4 入口，见 § Wiring Points；humanize 命令保持 Simple） | C-11 + C-15 + `expression-gate-operators.md` C-12 / C-14 + `compatibility-distribution.md` C-5 / C-6 / C-10 | `test_expression_gate_wiring` + `test_expression_compatibility` |
| FR-026 | 只引用前序三特性 | `compatibility-distribution.md` C-5 / C-9 | `test_expression_compatibility`（三份哈希） |
| FR-027 | 复用既有通道 | `compatibility-distribution.md` C-8 | `test_expression_compatibility`（无新存储路径） |

## Wiring Points（本切片唯一的既有表面改动）

分类与门禁必须被入口读取才成立。四处接线（形态与禁止项见 plan § Minimal Designated Wiring 与 `flow-class-ledger.md` C-15）：

| # | 入口 | 时点 | 增补（封闭清单） | 钉住它的测试 |
|---|------|------|------------------|--------------|
| W1 | `templates/commands/docs.md` | `## Outline` 内、分派之前 | lookup `/speckit.docs` + 两个 owner 指针（含 docs 调用点行 → `doc-consistency-check.py`） | `test_expression_gate_wiring` A1 |
| W2 | `templates/commands/humanize.md` | `## Outline` 内、委派之前 | **仅**两个 owner 指针（不调用脚本；humanize 保持 Simple） | A2（零脚本调用断言） |
| W3 | `skills/external/create-docs/SKILL.md` | R6 verify（reconcile + authoring） | owner 指针 + checker 调用要求 | A3 |
| W4 | `skills/external/humanize/SKILL.md` | Stage 6 保真自检之前 | lookup `/speckit.humanize`（该流程唯一读取）+ owner 指针（062 细则不变） | A3 |

生成物：8 个每工具命令副本由 `regen-command-copies.py` 从 W1/W2 重生成（A6）：docs 副本含 lookup + owner 指针，humanize 副本只含 owner 指针。接线封闭：其余 25 模板与 49 技能零调用点（A5）。

## Test Mapping（FR/SC → 测试文件）

| 测试文件 | 覆盖的 FR/SC | 形式 |
|----------|--------------|------|
| `tests/contract/test_flow_class_ledger.py` | FR-001/002/005/007/008/009/010/011/015/016/017/025；SC-002 | 契约（静态 + 台账对账夹具） |
| `tests/contract/test_flow_class_correctness.py` | FR-006；SC-001 | 契约（正确性：≥10 单元 oracle 比对 + 变异断言） |
| `tests/contract/test_expression_gates_doc.py` | FR-012/013/014/018/021/023/024 | 契约（owner 结构 + 调用点表） |
| `tests/contract/test_doc_consistency_checker.py` | FR-019/020/022；SC-007 | 契约（注入夹具） |
| `tests/contract/test_expression_gate_wiring.py` | FR-015/016/018/019/023/025；SC-002 | 契约（接线点 + 副本内容 + 接线封闭） |
| `tests/contract/test_expression_compatibility.py` | FR-011/025/026/027；SC-008 | 契约（哈希 + 文件集 + 白名单） |
| `tests/unit/test_flow_class_check.py` / `tests/unit/test_doc_consistency_rules.py` | 引擎实现细则（C-13 退出码、C-3/C-6 归一化与降级） | 单元 |

## SC → Measurement Mapping

| SC | 测量源（requirements § Measurement Sources） | 本阶段已落地证据 / 待实现面 |
|----|---------------------------------------------|------------------------------|
| SC-001 | 两名独立判定者结论落盘后逐条比对；机械核验 = 固定 fixture（≥10 单元）oracle 比对 + 变异断言 | 判据单一 owner + 台账；`test_flow_class_correctness` 使本条可被机器核验；两人演练为并列人工证据（未执行记 not-evaluated） |
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

### tasks 阶段复核（2026-10-24）

- `/speckit.tasks` 再次复核 Feature list：零新增、零废弃、零合并；Feature 069 的注册行与详情文件本阶段零改动（`tasks.md` 指针由 T036 在实现期回填）。
- 任务规模 36 任务行（Setup 3 · US1 9 · US2 15 · US3 4 · Polish 5）；四份契约共 50 条款，每条恰被一个 `[green:]` 行认领（`account-clause-coverage.py` 实测 claimed = 50）。
- 状态仍为 `Planned`：`tasks.md` 落盘不推进生命周期，`Implemented` 转移属 `/speckit.implement`。
- checklist 修复轮（2026-10-24）：新增 T005（分类正确性测试，US1 第 9 行）并把后续任务号顺延一位；条款分区与 `[green:]` 认领随号平移，claimed 仍为 50。
