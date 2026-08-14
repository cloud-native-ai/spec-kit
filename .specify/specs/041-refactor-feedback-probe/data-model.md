# Data Model — Feedback Probe 化重构

**Requirement**: `041-refactor-feedback-probe` → Feature 028  
**Date**: 2026-08-14

## 实体

### 1. Probe Class(插点类)

一类反馈插点的特征定义,真源 `shared/definitions/probe-definitions.md` 的 `## Classes` 表。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `class_id` | string | 是 | 项目内唯一,kebab-case(如 `command-wrapup`) |
| `kind` | enum | 是 | `internal` / `external` 二值 |
| `collection` | string | 是 | 收集内容声明(该类点收集什么信息),非空 |
| `target_slice` | string | 是 | 目标系统切片;内部类取框架组成维度(commands/skills/scripts/templates/docs),外部类为宿主自定义单元域 |
| `processing` | string | 是 | 收集后处理流程(内部:record→threshold→package→manual→mark-submitted;外部:record→local-consumption),非空 |
| `insertion_type` | string | 是 | 适用插入位置类型(如 wrap-up),非空 |

校验(引擎 `probes --validate`):五字段全部非空、`kind` 合法、`class_id` 唯一;任一失败 → 无效 Class(FR-001)。

初始实例:3 行 —— `command-wrapup`(internal/commands)、`skill-wrapup`(internal/skills)、`external-custom`(external/host-custom)。

### 2. Probe Object(插点实例)

Class 在系统中的实例化,真源 `## Objects` 表(内部)或 `.specify/memory/feedback/probes/*.md`(外部)。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `object_id` | string | 是 | 项目内唯一,kebab-case(内部如 `speckit-requirements-wrapup`;外部以 `ext-` 前缀强制命名空间隔离) |
| `class_id` | string | 是 | 归属且仅归属一个 Class(唯一外键) |
| `unit` | string | 是 | 绑定流程单元(`unit-id` 语法:`/speckit.<cmd>` 或 `skill:<name>`;外部对象指向宿主自定义单元,`custom:<owner>/<name>` 语法) |
| `lifecycle_point` | string | 是 | 生命周期点(当前全部为 `wrap-up`) |

派生(只读,不落盘):`kind`、`target_slice` 自所属 Class 继承。校验:`unit` 语法合法、`class_id` 存在、内部 Object 的 unit 与嵌入点对账(SC-001)。

初始实例:49 行(18 command + 31 skill,与嵌入点一一对应)。

### 3. External Probe(外部 probe)

类别为 `external` 的 probe(实体 2 的子集,由 `kind` 派生,不单独建表)。载体:`.specify/memory/feedback/probes/<object_id>.md`,YAML frontmatter 字段与实体 2 相同(强制 `object_id` 以 `ext-` 开头、`class_id=external-custom` 或运行时新建外部类),正文为自由描述。由模式三写入,遵循同四项特征完备校验。

### 4. System Slice(系统切片)

无独立载体 —— 内部取值为框架组成维度枚举(commands/skills/scripts/templates/docs,真源 `probe-definitions.md` 的 `## Slices` 节);外部为宿主自定义单元域(`host-custom`)。条目经 Object→Class 继承切片,作为过滤/统计维度(FR-005~007)。

### 5. Feedback Entry(反馈条目)

既有实体(`.specify/memory/feedback/<ts>-<unit-slug>.md`),frontmatter 扩展:

| 字段 | 类型 | 说明 |
|------|------|------|
| `probe` | string | 新增:所属 Object 的 `object_id`(引擎按 `unit_id` 自真源解析;解析失败 → 退出码 2) |
| `kind` | enum | 新增:`internal`/`external`(自 Class 继承,不手工传) |
| `slice` | string | 新增:目标切片(自 Class 继承) |
| `disposition` | enum? | 新增(可选):`processed`/`ignored`/缺省;仅 `/speckit.feedback` 处置动作写入,不改正文(FR-011) |
| 既有字段 | — | `id/unit_id/unit_type/run_id/scope/feature/feature-id/partial/created/summary` 不变;`(unit_id, run_id)` 去重不变 |

状态迁移:`undisposed`(缺省)→ `processed` / `ignored`(处置动作);不可逆回退不做(重置经删除重录)。

### 6. Probe Map(Probe 结构图)

派生物 `.specify/memory/feedback/probe-map.md`,由 `--action map` 从真源整体重建:Class→Object 树状总览(含内外类别标注)+ Mermaid 图源码块 + 明细表(每 Object 的插入位置/收集内容/处理流程)。非独立维护实体;真源未变时两次重建零差异(FR-013)。

## 关系图(Mermaid)

```mermaid
erDiagram
    PROBE_CLASS ||--o{ PROBE_OBJECT : "class_id"
    PROBE_OBJECT ||--o{ FEEDBACK_ENTRY : "probe=object_id"
    PROBE_CLASS }o--|| SYSTEM_SLICE : "target_slice"
    PROBE_OBJECT : "object_id, class_id, unit, lifecycle_point"
    PROBE_CLASS : "class_id, kind, collection, processing, insertion_type"
    FEEDBACK_ENTRY : "id, unit_id, run_id, probe, kind, slice, disposition"
```

## 存储清单

| 载体 | 内容 | 写入者 |
|------|------|--------|
| `shared/definitions/probe-definitions.md`(镜像 `.specify/shared/definitions/`) | Classes 表 + 内部 Objects 表(49)+ Slices 枚举 + 外部登记契约 | 框架维护者(源)/sync-mirrors(镜像) |
| `.specify/memory/feedback/probes/*.md` | 宿主项目外部 probe(一文件一 probe) | 模式三 / `--action probe-inject` |
| `.specify/memory/feedback/<ts>-*.md` | 条目(扩展 frontmatter) | `--action record` |
| `.specify/memory/feedback/index.json` | 条目镜像 + 计数(threshold/count_since_submission/submitted_at) | 引擎 |
| `.specify/memory/feedback/probe-map.md` | 派生结构图 | `--action map` |
| `.specify/memory/feedback/migration-log.md` | 旧条目收敛处置记录(逐条:删除/重登记 + 依据) | 迁移流程(一次性) |
| `.specify/memory/feedback/packages/feedback-<ts>.zip` | 上送包(仅内部条目)+ MANIFEST | `--action package` |
