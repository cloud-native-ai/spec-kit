# Data Model: Probe-Handler 体系（056）

**Spec**: `.specify/specs/056-probe-handler-system/requirements.md` | **Date**: 2026-10-13
**Registry truth source**: `shared/definitions/probe-definitions.md`（+ `.specify/` 镜像）

## Entity Inventory

| # | Entity | Status | Source FR |
|---|--------|--------|-----------|
| 1 | ProbeClass | 既有，升格伞形 | FR-001 |
| 2 | ProbeObject | 既有 + 新增行 | FR-001 / FR-002 / FR-003 |
| 3 | 非实体 probe 目录条目 | NEW（纯指针，非对账实体） | FR-004 |
| 4 | Handler | NEW | FR-005 / FR-007 |
| 5 | HandlerBinding | NEW | FR-006 |
| 6 | CompiledEmbed | NEW（派生产物，非注册实体） | FR-010 / FR-012 / FR-016 / FR-017 |
| 7 | ExternalProbe | 既有，零迁移 | FR-009 |

## Entity Definitions

### 1. ProbeClass（既有，6 Class）

字段封闭集（feedback-utils.py `_CLASS_FIELDS`，L1176）：`class_id`、`kind`、`collection`、`target_slice`、`processing`、`insertion_type`。

- 既有 6 Class 的语义与行序**不变**（FR-001）。
- 伞形扩格：文件头部声明伞形定位，Feedback Probe 降为域实例表述（词汇表义务见 FR-019）；`Slices` 启用 `scripts` 切片。
- 新增 Class（FR-002，每行携带代码锚点 = 函数/常量名，五特征完备性校验沿用 041 C-2）：
  - 050 升级探测（P1–P5）→ trigger-utils.py `run_probes`（L565–639）
  - 运行判定可用性探测（四轴 + session store / evidence lane 两个）→ run-determination.py（`AXES` L96、`probe_session_store` L322–337、`probe_evidence_lane` L1061–1088）
  - 证据引擎 lane 探测（probe_node / probe_session_store / probe_platforms）→ evidence-utils.py（L194 / L220 / L241，平台存储清单 L41）
- 锚点对账：契约测试与源码双向（锚点在源码存在；源码具名探测在注册表有行），变异演练证明能红（FR-003）。

### 2. ProbeObject（既有 72 Object + 新增）

字段封闭集（`_OBJECT_FIELDS`，L1178）：`object_id`、`class_id`、`unit`、`lifecycle_point`。

- 既有 72 Object 行序不变；新增 Object 归入上述新 Class，`unit` 指向引擎脚本路径，`lifecycle_point` 取所属机制的真实触发点。
- 关系：`class_id` → 恰一个 ProbeClass；一个 ProbeClass 1—N ProbeObject。

### 3. 非实体 probe 目录条目（NEW，纯指针）

- 真源新章「非实体 probe 目录」：每条目 = **路径 + 一行语义**（code-internal 微探针：writability / probe-links / git probe / 会话分析平台预读 / clause mutual-exclusion / read-only probe 等）。
- 硬约束：MUST NOT 复述行为规则（One Source Of Truth）；MUST NOT 参与任何对账计数（probes --validate / reconcile 的计数断言排除本节）。

### 4. Handler（NEW，六字段封闭集）

| 字段 | 值域 / 规则 | 依据 |
|------|-------------|------|
| `handler_id` | 全局唯一，`h-` 前缀（[[STR-004]]） | FR-005 |
| `kind` | `engine` / `agent` / `gate`（封闭集） | FR-005 |
| `action` | kind=engine：真实引擎 action（封闭集对账，见 contracts/engine-action-sets.md）；kind=agent：行为真源锚点名；kind=gate：confirmation-gates.md 治理条目名 | FR-007 |
| `mode` | `non-blocking`（缺省，fail-open）/ `blocking` | FR-005 |
| `order` | 整数；冲突错误仅适用于**不同** Handler 之间 | FR-005 / FR-006 |
| `behavior_owner` | 行为真源路径指针，MUST 可达（validate exit 2 指名不可达路径）；按 kind 取真源面：engine → 引擎脚本路径，agent → 文档路径 + `#` 锚（锚 = 该文件 `##` 级标题原文），gate → confirmation-gates.md 条目锚 | FR-005 / FR-007 |

- 注册表 MUST NOT 复述 behavior_owner 的行为规则（One Source Of Truth）。
- Handler 为静态注册行，无状态机。

### 5. HandlerBinding（NEW）

| 字段 | 值域 / 规则 | 依据 |
|------|-------------|------|
| `handler_id` | 恰指一个 Handler | FR-006 |
| `selector` | 字面语法 `@point:<lifecycle_point>`；`lifecycle_point` 封闭集 `wrap-up` / `situation` / `phase-boundary` / `confirm-gate`（Q4） | FR-006 |
| `scope` | `complex-commands` / `skills` / `all`，**或**逐 `object_id`（二选一） | FR-006 |
| 覆盖 | per-unit 覆盖（排除/变体）MUST 显式登记为 Binding 行（scope 取该 unit 的 object_id） | FR-006 |

- **Binding 身份** = (`handler_id`, `selector`, `scope`) 三元组；validate MUST 拒绝完全重复。
- **1 ⇒ N**：一个 Probe Object 可被多个 Binding 订阅；每 Binding 恰指一个 Handler。
- **合并规则**：同一 Handler 经多条 selector 命中同一单元同一生命周期点 → 合并为单一编译条目（位于该 Handler 自身 order 位置）；order 冲突错误仅适用于不同 Handler。
- Binding 为静态注册行，无状态机。

### 6. CompiledEmbed（NEW，派生产物）

| 属性 | 规则 | 依据 |
|------|------|------|
| 段标题 | `## Wrap-up`（[[STR-001]]），AUTO-GENERATED 横幅标记 | FR-010 / FR-012 |
| 内容形态 | 按 order 顶序列出该单元生效 handler 的调用形式；调用形式按 kind 固定派生（Q4）：engine → 一行 CLI 调用（引擎文件 + action）；agent → 一行行为真源锚点引用；gate → 一行治理条目引用 | FR-010 |
| 确定性 | 真源未变时两次编译逐字节一致（041 C-6 同型派生不变量） | FR-010 |
| 零段语义 | 零生效 handler 的单元不输出任何段（Q5） | FR-016 |
| 唯一形态 | 迁移完成态：凡有收尾段的单元，该段必为编译产出；手工 `## Feedback` 段与 docs-sync 手工段源面清零 | FR-016 |
| 措辞安全 | 生成措辞零 BLOCKING_PATTERNS（17 正则）命中；命中即拒写（exit 2） | FR-015 |

**生命周期**：无段 →（编译）有段 →（注册表/单元变化）stale →（--check exit 1 报漂移）重编译 → 有段。漂移错误类（全部 exit 2，FR-017）：孤儿 handler（产物有注册表无）、缺失 handler（注册表有产物无）、非法 action、order 冲突。

### 7. ExternalProbe（既有，零迁移）

- 存储 `.specify/memory/feedback/probes/`（`EXTERNAL_PROBES_DIRNAME`，feedback-utils.py L1172）仍归 feedback 域；[[STR-002]] 仅读写，零迁移（FR-009）。

## 注册表文件布局（真源章节）

`shared/definitions/probe-definitions.md`（135 行既有基础）扩格后章节序：

```text
# Probe Definitions（伞形真源头部声明：伞形定位 + Feedback Probe 域实例关系）
## Probe Classes        # 既有 6 Class 行序不变
## Probe Objects        # 既有 72 Object + 新增行
## Slices               # 启用 scripts 切片
## Handler              # NEW：六列表（handler_id/kind/action/mode/order/behavior_owner）
## HandlerBinding       # NEW：订阅行（handler_id/selector/scope/覆盖说明）
## 非实体 probe 目录     # NEW：纯指针条目（路径 + 一行语义）
## External Probe 契约  # 既有 L120 契约不变
```

## 解析与编译算法（compile-embeds 设计）

对每个编译单元（scan_embed_units 同语义枚举，实测 69 单元）：

1. **Selector 命中**：收集 selector.point 命中该单元生命周期点的 Binding；scope 匹配 = `all`（任意单元）/ `complex-commands`（命令面复杂命令单元）/ `skills`（技能面单元）；逐 `object_id` scope 仅命中该 ProbeObject 所属单元。
2. **扣减覆盖**：移除显式登记的 per-unit 排除/变体行。
3. **解析 Handler**：Binding → Handler；非法 action / 不可达 behavior_owner 在 validate 阶段已拒绝（exit 2）。
4. **排序合并**：按 Handler.order 升序；同一 Handler 多 selector 命中合并为单条目。
5. **渲染**：kind 固定派生调用形式（见 CompiledEmbed 内容形态）；skill 面单元保留 runtime-mode gate 判定结构（FR-013）。
6. **发射**：零生效 → 不输出段；否则写单段 `## Wrap-up`（原子写，命中 BLOCKING_PATTERNS 拒写）。
7. **传播**：compile → regen → sync 固定次序（FR-011）。

## MVP Seed Data（首批 5 Handler + 5 Binding）

Handler（order 值为本设计选定，满足 FR-008/FR-014 次序约束：run-determination 先于 feedback-record 与 threshold-notice）：

| handler_id | kind | action | mode | order | behavior_owner |
|------------|------|--------|------|-------|----------------|
| `h-run-determination` | engine | `determine` | non-blocking | 10 | `scripts/python/run-determination.py` |
| `h-feedback-record` | engine | `record` | non-blocking | 20 | `scripts/python/feedback-utils.py` |
| `h-threshold-notice` | agent | `Threshold prompt protocol (canonical semantics for step 6)` | non-blocking | 30 | `shared/workflow/feedback-step.md` |
| `h-token-reflection` | agent | `Reflection procedure (the embedded step points here)` | non-blocking | 40 | `shared/workflow/feedback-step.md` |
| `h-docs-sync-eval` | agent | `Evaluation procedure (the embedded step points here)` | non-blocking | 50 | `shared/workflow/docs-step.md` |

- kind=engine 的 behavior_owner 取引擎脚本（Constitution VIII：代码 = 行为真源）；kind=agent 取文档锚（行为真源冻结于 FR-020）。
- 锚点名为 feedback-step.md / docs-step.md 实测 `##` 级标题原文（2026-10-13 实测）。

Binding（全部 `@point:wrap-up`，Q4 封闭集值域内的 MVP 点）：

| handler_id | selector | scope |
|------------|----------|-------|
| h-run-determination | `@point:wrap-up` | complex-commands + skills 两条（或 `all` 减简单命令覆盖，以实现期实测现状矩阵定界） |
| h-feedback-record | `@point:wrap-up` | `all`（69 单元现均有反馈记录面） |
| h-threshold-notice | `@point:wrap-up` | `all`（消费 run-determination 判定结果） |
| h-token-reflection | `@point:wrap-up` | `all` |
| h-docs-sync-eval | `@point:wrap-up` | complex-commands + skills 两条 |

- **定界纪律**：各 Binding 的 scope 与 per-unit 覆盖行（简单命令排除集 agents/constitution/feature、feedback 技能 runtime-mode gate 变体）以**实现期对现状嵌入矩阵的实测 diff** 为准落行，由 FR-013 既有契约测试零回退钉住；本表给出机制与种子，不预写未经实测的单元矩阵。

## 漂移与对账错误类（封闭集）

| 错误类 | 方向 | 退出码 |
|--------|------|--------|
| 孤儿 handler（产物有、注册表无） | 产物 ↔ 真源 | exit 2 |
| 缺失 handler（注册表有、产物无） | 产物 ↔ 真源 | exit 2 |
| 非法 action（kind=engine 不在封闭集） | Handler ↔ 引擎 argparse | exit 2 |
| order 冲突（不同 Handler 同点同序） | Handler 内部 | exit 2 |
| behavior_owner 不可达 | Handler ↔ 文件系统 | exit 2 |
| 完全重复 Binding 三元组 | HandlerBinding 内部 | exit 2 |
| 产物措辞命中 BLOCKING_PATTERNS | 产物 ↔ 门控契约 | exit 2（拒写） |
| 产物与注册表可再生成内容不一致 | 产物 ↔ 真源 | exit 1（--check 预检） |

## Validation Rules Summary

1. handler_id 唯一 + `h-` 前缀（FR-005）。
2. kind/action/mode/scope/lifecycle_point 全封闭集（FR-005/006/007）。
3. Binding 三元组唯一；多 selector 合并规则（FR-006）。
4. behavior_owner 可达（路径存在；`#` 锚存在时与 `##` 级标题匹配）（FR-007）。
5. 注册表不复述行为规则；非实体目录不参与计数（FR-004/005）。
6. 确定性编译不变量 + 零漂移对账（FR-010/017）。
7. 次序约束：h-run-determination.order < h-feedback-record.order 且 < h-threshold-notice.order（FR-008/FR-014，契约测试钉住）。
