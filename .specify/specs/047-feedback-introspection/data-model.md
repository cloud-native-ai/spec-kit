# Data Model: Feedback 自省流程(047)

> 存储介质全部为 feedback-as-files(Markdown + YAML frontmatter + index.json)。本文件只定义逻辑实体与字段契约;文件级字节格式见 `contracts/introspection-report.md`。

## 实体总览

| 实体 | 载体 | 新建/扩展 |
|------|------|-----------|
| IntrospectionReport(自省报告) | `.specify/memory/feedback/introspection/<report-id>.md` | 新建 |
| Finding(问题/发现) | 报告正文内的结构区块 | 新建 |
| RoutingDecision(分流决定) | Finding 的字段 | 新建(逻辑) |
| FeedbackEntry(反馈条目) | `.specify/memory/feedback/<entry-id>.md` + `index.json` | 扩展(2 个可选字段) |
| index.json(存储索引) | `.specify/memory/feedback/index.json` | 扩展(`introspections` 数组) |

## IntrospectionReport(自省报告)

一次自省运行的持久产物。

| 字段 | 类型 | 约束 |
|------|------|------|
| `id` | string | `introspection-<UTC 紧凑时间戳>`(与条目/包同命名风);全局唯一 |
| `created` | ISO-8601 UTC | 引擎写入 |
| `status` | enum | `draft`(已落盘未确认)→ `confirmed`(用户确认,处置写回已生效)→ `superseded`(被后续报告承继);终态保留不删 |
| `scope_filter` | string | 范围快照的自然语言投影(如 `disposition=open, kind=internal, since=...`) |
| `scope_entries` | list[string] | 发起时刻范围内条目 id 全集(快照;执行期间新写入的条目不进入本次) |
| `supersedes` | string? | 承继的上一份报告 id(重复自省时) |
| `confirmed_at` | ISO-8601? | 用户确认时刻 |

正文 = 问题清单(见 Finding)。报告必须落在 `introspection/` 子目录,**禁止**落在存储根(`reindex` 对根目录 `*.md` glob,落根会被误索引为条目)。

## Finding(问题/发现)

报告的主体单元;同根因条目聚类的结果。每条范围内条目恰好归属一个 Finding 或被显式排除(排除项列于报告 `## Excluded`,附理由)。

| 字段 | 约束 |
|------|------|
| `finding_id` | 报告内局部 `F-<nn>`;全局引用形 `<report-id>#F-<nn>` |
| 问题陈述 | 非空 |
| 根因 | 非空 |
| 证据锚点 | ≥1 条,指向真实场景的具体位置(文件:行 / 单元定义锚点);核验结论(成立/部分成立/已过时/不成立)逐成员条目记录 |
| 分流决定 | 见 RoutingDecision |
| 优化方案 | 非空、具体可执行 |
| `member_entries` | ≥1 个条目 id |
| 用户覆盖痕迹 | 可选;用户改判分流方向时记录原决定与覆盖后决定 |

## RoutingDecision(分流决定)

| 字段 | 约束 |
|------|------|
| `direction` | `local-sink`(Loop B,本项目改进通道)| `upstream-bound`(Loop A,上行候选) |
| `channel` | local-sink: `direct-fix` / `improve-skills` / `improve-agent` / `improve-tools` / `improve-docs` / `requirements`;upstream-bound: `package-attachment` |
| 硬约束 | 任一成员条目 `kind=external` ⇒ direction 恒为 `local-sink`(引擎在 register 时强制校验,违反即拒绝) |

## FeedbackEntry(既有实体扩展)

既有字段不动(id/unit_id/unit_type/run_id/scope/probe/kind/slice/feature/partial/created/summary/disposition)。新增 2 个**可选** frontmatter 字段(同步镜像进 `index.json` 条目记录):

| 字段 | 类型 | 写入时机 |
|------|------|----------|
| `introspection_ref` | string(`<report-id>#F-<nn>`) | `introspect-register` 建立条目↔问题关联时 |
| `disposition_reason` | string | `dispose --reason` 写回处置理由(自省来源时为报告引用+简述) |

条目正文(`## Review` / `## Optimization Points`)依然永不改写(红线)。

**Excluded 条目的关联语义**: 报告 `## Excluded` 中的条目计入 `scope_entries`(V-1 覆盖完备)但无 Finding 可指,MUST NOT 写 `introspection_ref`;其范围归属仅由报告 Excluded 节表达。

## index.json 扩展

```jsonc
{
  // 既有字段不动 …
  "introspections": [
    { "id": "introspection-<ts>", "file": "introspection/introspection-<ts>.md",
      "created": "...", "status": "draft|confirmed|superseded",
      "supersedes": null, "entries": ["<entry-id>", ...] }
  ]
}
```

缺席时按空数组处理(向后兼容,老索引无需迁移)。

## 状态迁移

- 报告:`draft → confirmed`(用户确认后,引擎批量生效处置);`draft|confirmed → superseded`(新报告 register 且声明 `supersedes` 时,旧报告由引擎置为 superseded)。`superseded` 为终态。
- 已确认处置不被新报告自动翻案(Edge Case);翻案只能经显式 `dispose` 调用。
- 条目 `disposition` 词表不变:`open / processed / ignored`。

## 校验规则(引擎在 register 时强制)

- V-1 覆盖完备:`scope_entries` = 各 finding 的 `member_entries` 并集 ∪ `## Excluded` 条目集(差集为空,且无重复归属)。
- V-2 五要素齐备:每个 finding 五要素字段均非空,证据锚点 ≥1。
- V-3 引用存在:所有引用条目 id 在索引中存在。
- V-4 外部条目约束:R-决策含 external 成员时 direction 必须为 `local-sink`。
- V-5 幂等:同 `id` 重复 register = 更新(条目关联重链),不产生第二份报告记录。
