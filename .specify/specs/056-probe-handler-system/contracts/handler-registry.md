# Contract: Handler / HandlerBinding 注册表（真源 schema + handlers 动作）

**Spec**: `.specify/specs/056-probe-handler-system/requirements.md` | **Date**: 2026-10-13
**Registry file**: `shared/definitions/probe-definitions.md`（+ `.specify/` 镜像，shared↔.specify/shared 对）
**Query engine**: `probe-utils.py --action handlers`（STR-002）

## 真源章节 schema

在既有 `## Probe Classes` / `## Probe Objects` / `## Slices` / External Probe 契约（L120）之外新增三章（章节序见 data-model.md § 注册表文件布局）：

### `## Handler` 章（六列 markdown 表）

| 列 | 规则 |
|----|------|
| handler_id | 全局唯一，`h-` 前缀（[[STR-004]]） |
| kind | `engine` / `agent` / `gate` |
| action | kind=engine：真实引擎 action 名（封闭集对账）；kind=agent：行为真源锚点名（该文件 `##` 级标题原文）；kind=gate：confirmation-gates.md 治理条目名 |
| mode | `non-blocking`（缺省可省列值）/ `blocking` |
| order | 整数 |
| behavior_owner | 路径指针；kind=engine → 引擎脚本路径；kind=agent → 文档路径（`#` 锚可选）；kind=gate → confirmation-gates.md 条目锚 |

行示例（MVP 种子，完整表见 data-model.md § MVP Seed Data）：

```text
| h-run-determination | engine | determine | non-blocking | 10 | scripts/python/run-determination.py |
| h-feedback-record   | engine | record    | non-blocking | 20 | scripts/python/feedback-utils.py |
```

硬约束：本表 MUST NOT 复述 behavior_owner 的行为规则（One Source Of Truth）；order 冲突错误仅适用于不同 Handler。

### `## HandlerBinding` 章（订阅表）

| 列 | 规则 |
|----|------|
| handler_id | 恰指一个 Handler 行 |
| selector | 字面 `@point:<lifecycle_point>`；值域封闭集 `wrap-up` / `situation` / `phase-boundary` / `confirm-gate`（Q4） |
| scope | `complex-commands` / `skills` / `all`，或逐 `object_id`（二选一） |
| 覆盖说明 | per-unit 排除/变体的自然语言登记位（机器语义由行本身承载） |

身份 = (`handler_id`, `selector`, `scope`) 三元组；validate 拒绝完全重复（exit 2）。一个 Probe Object 可被多个 Binding 订阅（1 ⇒ N）。

### `## 非实体 probe 目录` 章（纯指针）

- 条目形态 = 路径 + 一行语义；MUST NOT 复述行为规则；MUST NOT 参与任何对账计数（probes/handlers validate 计数断言显式排除本节）。

## `--action handlers` 契约（FR-012）

- **列表**：默认输出全部 Handler 行；Binding 视图经 `--bindings` 输出（或等效过滤旗标，实现期定名并在本契约回填）。
- **过滤**：`--point <lifecycle_point>`、`--scope <scope>`、`--kind <kind>`、`--mode <mode>` 可组合，交集语义。
- **`--validate`**：全量校验，错误类与退出码见 data-model.md § 漂移与对账错误类；输出逐条指名（非法 action / 不可达 owner 路径 / 重复三元组 / order 冲突）。
- **只读**：宿主项目可运行查询与 validate，不可注册（Q6 / FR-021）；注册 = 编辑真源表行 + 重编译。
- `--format text|json` 同公共旗标。

## 校验规则（封闭集）

1. handler_id 唯一 + `h-` 前缀。
2. kind/action/mode/scope/lifecycle_point 封闭集。
3. Binding 三元组唯一。
4. behavior_owner 路径可达；带 `#` 锚时锚必须匹配该文件 `##` 级标题原文（exit 2 指名不可达路径，与非法 action 同级，FR-007）。
5. kind=engine action 必须命中引擎真实 action 封闭集（contracts/engine-action-sets.md）。
6. 次序约束：h-run-determination.order < h-feedback-record.order 且 < h-threshold-notice.order（FR-008/FR-014，契约测试钉住）。

## 词汇表义务（FR-019，本契约的伴随更新面）

- `.specify/memory/glossary.md`：新增 Probe（伞形）/ Handler / HandlerBinding 三术语（origin=auto, status=proposed）；改写 Probe Class / Probe Object / Feedback Probe / 「埋点」消歧条目。无镜像对（finding ②：memory/ 不在 MIRROR_PAIRS），host-side 编辑。
