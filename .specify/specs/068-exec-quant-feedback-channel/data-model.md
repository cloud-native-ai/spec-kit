# Data Model — 068 Exec-Quant Feedback Channel

**Phase 1 output** (`/speckit.plan`, 2026-10-22). Entities this feature adds or touches;
059 既有记录实体（Exec-Quant Record）原样复用、零 schema 变更（Explicit Exclusions）。
`[[STR-001]]` = record kind 字面量，`[[STR-002]]` = 未测标记字面量（见 requirements.md
§ Shared Strings；本文件不重抄字面值）。

## E1 — Exec-Quant Record（既有，不新增）

059/061 已定形的采集记录；068 只读它。

| Field | Type | Notes |
|-------|------|-------|
| `kind` | string | 恒 `[[STR-001]]`；载荷识别锚点 |
| `schema_version` | int | 实测 1（遗留 jsonl）与 2（records/）并存 |
| `unit_id` | string | `/speckit.*` / `skill:*` / `custom:*/*` / `agent:*` |
| `unit_type` | string | command / skill / custom-unit / agent |
| `run_id` | string | 运行标识 |
| `run_id_resolution` | string | explicit / adopted / synthesized / agent 三态（v2） |
| `collected_at` | string | ISO-8601 Z |
| `agent` / `config` / `llm` / `quality` / `qualification` | object | 字段值 = `{value, provenance}` 对象或裸 `[[STR-002]]` 字符串（混合形态，FR-007 容忍） |
| `truncated` | array | 采集侧截断标记 |

**Validation（068 视角）**: 载荷侧不校验、不改写内部字段——只要求 `kind == [[STR-001]]`
且整体可 `json.loads` 为 object；其余一切形态差异由读取侧归一（FR-007 / D6）。
未知字段原样保留（零丢弃）；不可解析 → 跳过并计数。

## E2 — Source Project Identity（新增，包级）

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `project_name` | string | 条件必选 | 见 identity_status；非空时 MUST 非绝对路径形态（不以 `/` 开头）、零凭据形态 |
| `source_commit` | string \| null | 可选 | 40-hex 或 null；仅佐证 |
| `identity_status` | enum | 必选 | `identified` / `unknown-project` |

**State transition**: 打包时一次性写入 → 此后不可变（载荷不可变，spec Key Entities）。
`project_name` 缺失（instructions.md 无 Project Name 行且目录基名不可得）→
`identity_status = "unknown-project"`，接收侧落 unknown-project 分组（FR-003 / D3）。

## E3 — Exec-Quant Payload（新增，包内）

包内 `exec-quant/` 目录整体；一次写入、不可变。

| Field / Member | Type | Validation |
|----------------|------|------------|
| `payload-manifest.json` | object | 见 E4；载荷的机器可读声明 |
| `records/<name>.json` | file | 逐条记录的**原样字节拷贝**；name 沿用源文件名；遗留流条目名 `legacy-records-L%04d.json` |
| 条数上限 | int | `included ≤ 1000`（FR-005 封顶） |
| 字节上限 | int | 载荷总字节 ≤ 16 MiB |

**Relationships**: Payload *来自* 客户项目 Exec-Quant Store（只读，FR-002）；
Payload *归因到* 恰一个 Source Project Identity；Payload *声明于* MANIFEST.md
§ Exec-Quant Payload。

## E4 — Payload Manifest（新增，包内机器可读清单）

`exec-quant/payload-manifest.json` 字段：

| Field | Type | Validation |
|-------|-----|------------|
| `schema_version` | int | `1`（载荷清单自身版本） |
| `kind` | string | `"speckit.exec-quant-payload"` |
| `identity` | object | E2 |
| `record_count` | int | = included 数 = records/ 文件数 |
| `source_form_counts` | object | `{"records-dir": N, "legacy-jsonl": M}`，N+M = record_count |
| `skipped_unreadable` | int | 不可解析计数 |
| `truncated_count` | int | 封顶截断计数 |
| `cap_records` / `cap_bytes` | int | 本次生效的上限值（确定性取证） |
| `collected_at_range` | [string, string] | 首末记录 collected_at；空载荷为 null |

**Validation**: `record_count == len(records/)`（接收侧逐条对账依据，SC-003）；
`skipped_unreadable + truncated_count + record_count == 探测总数`。

## E5 — MANIFEST.md § Exec-Quant Payload（新增段，人可读）

既有 `MANIFEST.md` 追加一节（Markdown，不破坏既有段落）：载荷有无、条数、来源形态
计数、跳过/截断计数、源项目身份（project_name 或 "unknown-project"）、封顶是否触发。
人读段与 E4 机器段**内容同源**（同一函数渲染，零手抄——One Source of Truth）。

## E6 — Aggregated Record Envelope（新增，接收产物）

`aggregated/<source-slug>/records/<entry-filename>.json`：

| Field | Type | Validation |
|-------|------|------------|
| `aggregation_envelope.schema_version` | int | `1` |
| `aggregation_envelope.kind` | string | `"speckit.exec-quant-aggregated"` |
| `aggregation_envelope.source_project` | string | E2.project_name；缺失 = `"unknown-project"` 字面量 |
| `aggregation_envelope.source_commit` | string \| null | E2 佐证 |
| `aggregation_envelope.identity_status` | enum | E2 |
| `aggregation_envelope.identity_key` | string | 64-hex；D6 五元组哈希（不含 content_hash） |
| `aggregation_envelope.content_hash` | string | 64-hex canonical sha256；独立比较字段，不进入 identity_key |
| `aggregation_envelope.package_file` | string | 来源 zip 文件名（不含路径） |
| `aggregation_envelope.ingested_at` | string | ISO-8601 Z |
| `record` | object | 源记录 verbatim（未知字段零丢弃） |

**Validation**: 信封不可变（落盘后不更新）；`identity_key` 唯一性由接收动作在
flock 去重检查下保证；同 key 异 content_hash 不入库（keep-first，`identity_conflicts`
计数）；`source-slug` = `slug(project_name) + "-" + hash8(identity串)`
或字面 `unknown-project`。

## E7 — Aggregate View（新增，汇总产物）

`aggregated/summaries/<summary-id>.json`；summary-id = 时间戳-uuid（沿用
`entry_filename()` 形态）。每次显式汇总一个新文件，旧文件永不改写（可重建 =
重跑产生新文件）：

| Field | Type | Validation |
|-------|------|------------|
| `kind` | string | `"speckit.exec-quant-aggregate-view"` |
| `schema_version` | int | `1` |
| `generated_at` | string | ISO-8601 Z |
| `sources[]` | array | 每源项目一组：`project`、`identity_status`、`record_count`、`units{unit_id: count}`、`quality{field: {evaluated, not_evaluated}}`、`coverage{not_evaluated_total, evaluated_total}`、`record_files[]`（对账名单） |
| `totals` | object | 全局计数 + 未测总占比 |
| `store_digest` | object | `{record_files_total, identity_keys_total}` 重建校验锚 |

**Validation（零臆造，FR-013）**: 每个计数字段可由 `record_files` 名单重放核对；
`[[STR-002]]` 字段一律计入 `not_evaluated`，禁止出现任何填补值；缺字段 = 显式
`not_evaluated` 计数呈现（读取侧归一，D8）。产物零网络、仅本地（FR-014）。

## E8 — Consume-log / Backlog（既有，零变化）

Path A 既有对账面；exec-quant 载荷接收计数写入 digest report，feedback 条目
路由语义零变化（FR-009）。载荷接收事实的持久锚 = 聚合层信封文件自身 +
`payload-manifest` 对账，不新增日志面（Framework Scope：零新机制）。

## Entity Relationship（文字图）

```text
客户项目 Exec-Quant Store (E1, 只读)
   └─(打包: package, 全量含封顶)→ Exec-Quant Payload (E3)
        ├─ 声明于 → Payload Manifest (E4) ─ 渲染同源 → MANIFEST § Exec-Quant Payload (E5)
        ├─ 归因到 → Source Project Identity (E2)
        └─(人工送达 → 接收: ingest-exec-quant, 幂等 D6)
             └→ Aggregated Record Envelope (E6)  @ aggregated/<source-slug>/records/
                  └─(显式汇总: aggregate)→ Aggregate View (E7) @ aggregated/summaries/
```
