# Data Model — Feature 069 / Slice 069b

**Date**: 2026-10-25 · **Spec**: [requirements.md](requirements.md) · **Contracts**: [contracts/](contracts/)
**Owner boundary**: 本文件是**设计视图**，不是任何判据或取值的所有者。分类判据、两个取值、六面门禁判据、阶段名册分别归
`shared/definitions/flow-class-definitions.md`、`shared/workflow/expression-gates.md`、
`skills/external/sdd-loop-driver/scripts/loop-state.py`。字段名中的机器键 `flow_class` 是 `[[STR-003]]` 的固定副本。

本切片无运行时数据库、无持久化状态。下列实体全部是**文件内结构**或**只读检查的输出**；唯一的「记录类」实体是
基线记录与迁移样本，落在本 spec 的 `notes/`（每特性一份的 dated 记录）。

---

## E1 — Isomorphism Row（同构映射行）

| 字段 | 类型 | 约束 | 来源 |
|------|------|------|------|
| `stage` | enum | 属于 E2 的 `stage_set`；恰好一次 | FR-001 / contract C-2 |
| `structure_cell` | text | 形如 `代码型：… ↔ 文档型：…`，一个 `↔`，两侧 ≥ 8 字符 | FR-001 / C-3 |
| `process_cell` | text | 同上 | FR-001 / C-3 |
| `logic_cell` | text | 同上 | FR-001 / C-3 |
| `enforcing_faces` | list[face_id] | `已强制` 时 ≥ 1；`已声明未强制` 时为空 | FR-002 / C-4 |
| `enforcement_status` | enum | `已强制` \| `已声明未强制` | FR-002 / C-4 |

**校验**：`enforcement_status = 已强制` ⟹ 每个 `face` 满足 `(stage, face)` 在 E6 的 blocking 行集合内（C-5）；
`已声明未强制` ⟹ `stage` 不在 E6 的 blocking 阶段集合内（C-6）。违反分别产出
`annotation-false-enforced` / `annotation-false-unenforced`；两者皆空 → `slogan-row`（C-7）。

**状态**：无状态迁移。行随阶段名册变化而增删（C-2），不另立版本。

## E2 — Isomorphism Map（同构映射表）

| 字段 | 类型 | 约束 | 来源 |
|------|------|------|------|
| `carrier` | path | 唯一：`shared/definitions/flow-class-definitions.md` § 同构映射 | FR-001 / C-1 |
| `header` | tuple[str,6] | 逐字匹配 C-2 的表头 | C-2 |
| `rows` | list[E1] | 恰好 8 行、零空行 | FR-001 / C-2 |
| `stage_set` | set[str] | 等于名册 owner 的 `STAGE_ARTIFACTS` 键集 | FR-001 / C-2 |
| `face_legend` | text | 表前一段，声明结构 / 流程 / 逻辑三面的含义一次 | C-3 |
| `boundary_ref` | path#anchor | 指向同文档 § 不可同构边界 | FR-003 / C-9 |

**派生计数**：`cells = rows × 3 = 24`；`enforced_rows + declared_unenforced_rows = 8`。计数由制品导出，
不得手写进需求或契约（事实一致性面）。

## E3 — Non-Isomorphism Boundary（不可同构边界）

| 字段 | 类型 | 约束 | 来源 |
|------|------|------|------|
| `boundary_id` | enum | `a` \| `b` \| `c` \| `d`，各一次 | FR-003 / C-8 |
| `axis` | text | 验收 oracle / 验证算子 / 失败可见性 / 语义 oracle 缺失 | FR-003 |
| `why_not_interchangeable` | text | 非空 | C-8 |
| `gate_handling` | text | 含 ≥ 1 个 E7 的 `face_id`，并说明处理方式 | FR-003 / C-9 |

**校验**：缺行/重复 → `boundary-missing`；无 face id → `boundary-unbound`；只列 face id 无说明 → `boundary-malformed`。

## E4 — Ledger Version Declaration（台账生效版本声明）

| 字段 | 类型 | 约束 | 来源 |
|------|------|------|------|
| `doc_version` | int | 正整数；在 § 逐流程台账 内声明恰好一次 | FR-010 / C-5 |
| `declared_at` | date | `YYYY-MM-DD` | C-5 |
| `carrier_form` | enum | 固定 `doc-version+change-log`（本切片选择；无行级列） | FR-010 / R6 |
| `change_log_ref` | path#anchor | 指向同文档 § 变更记录 | C-5 |

**禁止**：行级 `effective_version` 列、`version` 字段、第二个版本信号（C-5）。

## E5 — Reconcile Result（对账结果）

| 字段 | 类型 | 约束 | 来源 |
|------|------|------|------|
| `action` | literal | `check` | 069a C-13 + 本切片 C-2 |
| `units` | int | `inventory_units` 的同值投影 | 069a |
| `coverage.ledger_rows` | int | 解析出的台账行数 | FR-010 / C-2 |
| `coverage.inventory_units` | int | 清单单元数 | C-2 |
| `coverage.matched` | int | 台账 ∩ 清单 | C-2 |
| `coverage.gaps` | int | `missing + unknown` finding 数 | C-2 |
| `coverage.parse_errors` | int | `row-malformed + ledger-truncated` finding 数 | C-2 |
| `coverage.floor` | int | `78`（实测常量） | C-1 |
| `red_kind` | enum | `clean` \| `gap` \| `parse-failure` \| `owner-unavailable` \| `framework-source-required` | C-3 |
| `findings[]` | list[Finding] | `kind` / `unit_id` / `message` / `line?` | 069a + 本切片 |

**不变量**：`red_kind = clean` ⟺ `findings == []` ∧ `matched == inventory_units` ∧ `parse_errors == 0` ∧ `ledger_rows ≥ floor`。
`red_kind` 优先级见 C-3。

## E6 — Gate Operator Row（门禁算子行，只读视图）

| 字段 | 类型 | 说明 |
|------|------|------|
| `stage` | enum | E2 的 8 阶段之一 |
| `face_id` | face_id | 封闭六面之一 |
| `blocking` | bool | 阻断级别是否为 `blocking` |

**来源**：`shared/workflow/expression-gates.md` § 阶段算子表（owner）。本实体是**解析视图**，不是第二份算子表：
本切片 MUST NOT 复制其算子文本，只读取 `(stage, face_id, blocking)` 三元组。
**实测基线（2026-10-25）**：16 行；blocking 行按阶段 = requirements 2 / clarify 2 / plan 2 / tasks 2 / checklist 2 / analyze 2 / implement 1 / review 2。

## E7 — Face Binding（六面绑定，只读视图）

| 字段 | 类型 | 约束 | 来源 |
|------|------|------|------|
| `face_id` | slug | 恰好 6 个、唯一 | FR-013 / C-11 |
| `pointer_cell` | text | 非空；一个绑定格；MAY 用 `+` 连接多个路径 | C-11 |
| `owner_paths` | list[path] | 每个可在源码根或 `.specify/` 镜像解析 | C-11 |
| `anchors_ok` | bool | 带 `§ <anchor>` 时该文件存在标题文本包含锚 | C-11 |

**违规 kind**：`faces-count` / `faces-duplicate` / `faces-pointer-missing` / `faces-unresolvable` / `faces-second-table`。

## E8 — Delegation Edge（委托边）

| 字段 | 类型 | 约束 | 来源 |
|------|------|------|------|
| `command` | unit_id | `/speckit.<stem>` | FR-012 / C-8 |
| `skill` | unit_id | `skill:<name>` | C-8 |
| `command_class` | enum | 来自 E4 所属台账的 `flow_class` | FR-012 |
| `skill_class` | enum | 同上 | FR-012 |
| `verdict` | enum | `same-class` \| `neutral-exempt` \| `mismatch` \| `unknown-skill` | C-8 |
| `source_line` | int | 模板中的行号 | C-8 |

**不变量**：`verdict = neutral-exempt` ⟺ `skill ∈ 类中立清单`；`mismatch` 与 `unknown-skill` 必产出 finding。
**实测基线（2026-10-25）**：26/27 个模板声明 ≥1 条边（`/speckit.tools` 无）；全部边 `same-class` 或 `neutral-exempt`（6 条豁免）。

## E9 — Baseline Record（基线记录）

| 字段 | 类型 | 约束 | 来源 |
|------|------|------|------|
| `quantity` | enum | `gate_calls` \| `confirmations` \| `wall_clock` | FR-014 / C-1 |
| `frozen_value` | scalar | `0` / `null` / 实测绝对值 | C-6 |
| `frozen_at` | date | 记录落盘日 | C-8 |
| `frozen_commit` | sha | `f0df3d0b` | C-1 |
| `instrument` | text | 四个既有通道之一 | C-2 |
| `source_command` | text | 可复算命令 | C-8 |
| `verdict` | enum | `not-evaluated` \| `measured` | C-6 / C-8 |

**禁止**：`0` 冒充无样本、绝对量冒充降幅、结论写成「达成」。记录形态见 `notes/expression-baseline.md`。

## E10 — Migration Sample（迁移样本）

| 字段 | 类型 | 约束 | 来源 |
|------|------|------|------|
| `project` | slug | 三个样本之一 | FR-007 / C-6 |
| `head` | sha | `git rev-parse HEAD` 的短 sha | C-6 |
| `branch` | text | 实际分支 | C-6 |
| `dirty_files` | int | 工作树脏文件数（快照排除，仅记录） | C-6 |
| `payload_state` | enum | `unrefreshed` \| `refreshed` | FR-006 |
| `suite_command` | text | 原样可执行 | C-7 |
| `names_before` / `names_after` | path | 失败名集产物（按套件原生失败输出提取；C-7） | C-7 |
| `delta` | set | `comm -13` 结果，MUST 为空或 `not-evaluated` | SC-002 |

**冻结值**：见 `notes/migration-samples.md`（三个未刷新项目 + HEAD + 套件命令）。

---

## 关系图（文本）

```
E2 Isomorphism Map ──1:N──▶ E1 Isomorphism Row ──N:M──▶ E7 Face Binding
        │                        └──reads──▶ E6 Gate Operator Row
        └──1:1──▶ E3 Non-Isomorphism Boundary ──N:M──▶ E7

E4 Ledger Version ──declares──▶ (owner ledger, 069a)
E5 Reconcile Result ──reads──▶ (owner ledger + inventory + E4)
E8 Delegation Edge ──reads──▶ (command templates + owner ledger + neutral list)
E9 Baseline Record ──reads──▶ (exec-quant / feedback / run-determination / git)
E10 Migration Sample ──reads──▶ (client repos + E5's name-level suite runs)
```

## 验证规则汇总

| 规则 | 机械判据 | 契约 |
|------|----------|------|
| 24 格齐全且两侧成对 | 8 行 × 3 格，每格一个 `↔` | C-2 / C-3 |
| 强制标注真实性 | `(stage, face)` blocking 存在性 | C-5 / C-6 |
| 四类边界齐全且绑面 | `a`–`d` 各一次，`门禁处理` 含 face id | C-8 / C-9 |
| 零缺口 vs 解析失败 | `red_kind` 不同 | C-3 |
| 反空真 | `ledger_rows ≥ 78` 且 `matched == inventory_units` | C-1 / C-2 |
| 混合 oracle | `basis = mixed-oracle ⟹ flow_class = execution` | C-7 |
| 委托同类 | `verdict ∈ {same-class, neutral-exempt}` | C-8 |
| 六面绑定 | 6 行、1 格/行、指针可解析 | C-11 |
| 判据不搬家 | duplicate 面 findings = 0（封闭主体集） | C-13 |
| 无样本不记零 | `verdict = not-evaluated` + reason | E9 / C-6 |
