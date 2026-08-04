# Data Model: Team Summary 信息管理机制

**Requirement → Feature**: `036-team-summary` → Feature 027 Team Management
**Date**: 2026-08-04
**Upstream authority**: 被调技能的字段定义与约束唯一权威是 `skills/summarize-project/schema/project.sql`(DDL)。本文件**不复写**该 schema,只定义(a) 团队侧新增的持久结构,(b) 团队词汇 → 七实体的映射,(c) 身份与状态的判定规则。

## 1. 新增持久结构

### 1.1 Item Ledger — `.specify/teams/<slug>/items.jsonl`

tracked、append-only、JSON Lines。每行一个**条目状态事件**。只由团队主管写入(FR-021)。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `item_id` | string | 是 | 条目身份。文法见 §3。重命名时不变(FR-026) |
| `title` | string | 是 | 条目标题(可含中文;**不**作为身份键) |
| `phase_ref` | string | 是 | 所属阶段 ID(`PH-<nnnn>`),对应模式的阶段单位 |
| `state` | enum | 是 | `completed` / `in-progress` / `delayed` / `not-started` / `unknown`(FR-006) |
| `provenance` | string | 是 | tracked 工件路径(可带 `#anchor` 或 `:line`)。无出处则本行非法(FR-010/FR-011) |
| `ts` | string | 是 | 事件时间戳(ISO-8601 UTC),同时是基线日期来源(FR-005) |
| `identity` | enum | 是 | `explicit`(团队发放) / `inferred`(历史回填,FR-027) |
| `supersedes` | string | 否 | 被本行归并的推断身份 ID;用于两态交接(FR-027) |
| `excluded_reason` | string | 否 | 计入被排除口径的理由(如 iteration 被淘汰变体),非空即不计入延期/未完成(US5 场景 5) |
| `maturity_at_event` | string | 否 | 事件发生时的成熟度(L1/L2/L3),用于锚定状态语义,防止升级后追溯改写(Edge Case) |

**不变式**
- **IL-1**:append-only。既有行 MUST NOT 被改写或删除;状态推进以追加新行表达。
- **IL-2**:同一 `item_id` 的**最后一行**(按 `ts`,同 `ts` 按文件顺序)决定其当前状态。
- **IL-3**:`provenance` MUST 指向 tracked 路径。`.specify/teams/.work/**`、`.specify/agents/execution/logs/**` 及仓库外路径(如 `${TMPDIR}/spec-kit-dispatch/**`)一律非法。
- **IL-4**:`identity: explicit` 的行,其 `item_id` MUST 匹配 `TI-<nnnn>`;`inferred` MUST 匹配 `TIX-<8hex>`。
- **IL-5**:`supersedes` 非空时,被指向的 ID MUST 在本台账中出现过,且折叠后 MUST 只产生一条记录(FR-027)。

### 1.2 Goal Summary Delivery Directory — `.specify/project/goal/<goal-slug>/` ([[STR-001]])

以 **goal** 为索引的唯一完整总结。结构由被调技能规定(目录自包含),团队侧只负责生成 `data/project-input.yaml`:

```text
.specify/project/goal/<goal-slug>/
├── summary.md            # 主报告(含 ## 附注 人工批注节,刷新时保留)
├── assets/               # 每图 .puml + .svg + .png 同名三件套
└── data/
    ├── project-input.yaml    # [[STR-004]] 团队侧唯一交付面(由生成器产出)
    ├── project.db            # 派生;被调技能每次 --load 重建
    └── engine-out.json       # 派生;引擎输出
```

**与既有产物共存(FR-036)**:`.specify/project/` 已存在 tracked 的历史产物——`project.md` 与 wbs / gantt / milestones 三组 `.puml`/`.svg`/`.png`(2026-07-25 由已重构的 `manage-project` 建立)。`goal/` 子树与它们平级新增,MUST NOT 覆盖或迁移既有内容。被调技能对 SpecKit 项目的默认交付目录 `.specify/project/summary/` 亦为平级,互不冲突。

### 1.3 Goal Identity — `goal_slug` ([[STR-006]])

`team.md` frontmatter 新增字段,与既有 `slug`(team slug)并存且语义不同。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `goal_slug` | string | 否(缺省走推断) | goal 的显式身份。同值即同一 goal,无论声明者是哪个团队(FR-031) |

**解析顺序(确定性)**:

1. `team.md` frontmatter 声明了 `goal_slug` → 取其值,`goal_identity: explicit`。
2. 未声明 → 取该团队自身的 `slug` 作为 goal 身份,`goal_identity: inferred`,并在派生数据的 `inferred_fields` 与报告元信息中标记为推断(FR-034)。

**文法**:`goal_slug` MUST 满足与条目 ID 相同的 DDL 字面量约束(见 §3)——首字符字母或数字,其余仅 `[A-Za-z0-9_.-]`。它同时是目录名,故亦 MUST 是合法路径片段(不含 `/`、不为 `.` / `..`)。

**不变式**:
- **GI-1**:`goal_slug` 的取值 MUST NOT 由 goal 正文派生。goal 正文改写不改变它,因而不迁移交付目录(FR-019)。
- **GI-2**:一个团队在任一时刻 MUST 只属于一个 goal。改绑(`goal_slug` 被改写)时,原 goal 目录 MUST 保留其历史贡献并标注该团队已不再参与;新 goal 目录自改绑时点起接收新贡献。
- **GI-3**:推断身份升为显式身份时,MUST 归并到显式 goal 目录并保留历史贡献,MUST NOT 留下推断目录与显式目录两份并列总结(FR-034)。
- **GI-4**:两个团队声明同一 `goal_slug` 但 goal 正文实质不同时,以显式声明为准(声明即同一 goal),正文差异记入元信息供人裁决——机制不自行判定"其实不是同一目标"。

### 1.4 Team Config — `config.summary` ([[STR-002]])

嵌套于 `team.md` frontmatter 的 `config` 之下(避免与预设文件顶层一行式 `summary:` 冲突)。

| 键 | 类型 | 默认 | 说明 |
|----|------|------|------|
| `enabled` | bool | `true` | 缺省即启用(opt-out 语义,FR-013) |
| `every` | int | continuous `5`;其余模式 `1` | 每 N 个阶段边界刷新一次。continuous MUST NOT 默认为 1(FR-013) |
| `delivery_dir` | string | `.specify/project/goal/<goal-slug>/` | 交付目录([[STR-001]]);由解析出的 goal 身份决定,不随 team slug 变动 |
| `interactive` | bool | `false` | 团队触发为自动流程,MUST 以非交互模式调用被调技能 |

**整节缺省**等价于 `{enabled: true, every: <模式默认>, delivery_dir: <默认>, interactive: false}`。

## 2. 概念映射:团队词汇 → 七个项目管理实体

`project` / `people` / `phases` / `work_items` / `milestones` / `features` / `sources` 逐一有来源或显式缺席降级(FR-007)。

**聚合范围**:映射的对象是**一个 goal**(而非一个团队)。设该 goal 下有 N 个团队(N ≥ 1,即声明了同一 [[STR-006]] 的全部团队),下表的来源均在这 N 个团队上取并集,除 `project` 与 `milestones` 取自 goal 本身。

| 实体 | 团队侧来源 | 缺席降级 |
|------|-----------|---------|
| `project` | **goal 级**:`project_name` ← goal 的显式标识(`goal_slug`,推断时为 team slug);`project_desc` ← 该 goal 的 goal 正文(多团队声明不一致时取任一并把差异记入元信息,GI-4);`baseline_date` ← 本次触发运行/cycle 的时间戳(FR-005);`repos` 恒为空(不 opt-in 扫仓) | 不可缺席(R 档) |
| `people` | N 个团队名册行的**并集**;`owner_id` ← 名册 agent slug;`owner_name` ← 所引用 agent 定义的 frontmatter `name`(`.specify/agents/{templates,instances}/`,instance 优先);`owner_role` ← 名册 `role`。同一 agent slug 出现在多个团队 → 归并为一人 | 解析不到定义 → `owner_name` 记 `未记录`,不臆造 |
| `phases` | N 个团队各自的阶段单位,**按团队命名空间化**:`phase_name` 形如 `<team-slug> · <单位>`(continuous → cycle;iteration → generation;serial → stage;parallel → 派发批次,FR-002)。不同模式的阶段 MUST NOT 混为同一条序列 | 无阶段材料 → 该团队单一阶段并声明 |
| `work_items` | N 个团队台账的**并集**(权威结构面为 §1.1)。每条的 `phase_id` 指向其所属团队的阶段,`source` 出处路径以 `.specify/teams/<team-slug>/` 开头,**归属因此机器可判定**(FR-033) | 全部团队台账为空且 `runs/` 亦无交付物 → 拒绝出总结(`declined(no-material)`) |
| `milestones` | **goal 级,只一套**:该 goal 的可验证成功判据逐条映射为里程碑(FR-003),`anchor_item_id` 锚到任一团队的对应工作项;MUST NOT 逐团队重复同一判据(FR-032) | goal 无可验证判据 → 该组为空,依赖 `work_items` 满足 R 档组级约束 |
| `features` | N 个团队产出的能力/交付物类目并集 | 无类目材料 → 空,`## 需求与特性` 按既有降级只留声明 |
| `sources` | 每个团队每组信息一条声明,`source_kind: user-form`,`source_ref` 指向该团队的 tracked 工件路径 | 不可缺席(否则条目 `source` 无法推断) |

**未参与本次刷新的团队(FR-032)**:goal 总结每次从该 goal 下**全部**团队的台账重新折叠,因此某团队本次未触发刷新不会使其历史贡献消失——它的条目照常出现,状态停留在其最后一次事件。

### 2.1 `coverage` 块(恒定产出)

生成器 MUST 恒定产出 `coverage`,否则含 `@startwbs` 的报告在落盘门禁 CG-COVERAGE 必 FAIL(research.md E-5)。

| 字段 | 团队侧口径 |
|------|-----------|
| `candidate_total` | 台账中出现过的**全部** `item_id` 去重计数 |
| `excluded` | `excluded_reason` 非空的条目数(被淘汰变体等) |
| `granularity_truncated` | 已完成/已归档且在呈现层被聚合为计数的条目数(FR-029) |
| `unattributed` | 有交付物证据但无法归属到任何阶段的条目数 |
| `source_label` | `团队条目台账 items.jsonl` |

闭合等式由引擎产出(`coverage.closure_equation`),报告照抄,团队侧不做减法。

## 3. 身份文法(受 DDL 硬约束)

`entity_ids.entity_id` 的 DDL CHECK 为 `GLOB '[A-Za-z0-9]*' AND NOT GLOB '*[^A-Za-z0-9_.-]*'`——首字符字母或数字,其余仅 `[A-Za-z0-9_.-]`。实测越界(含空格)以 **exit 3** 被拒(research.md E-2)。

| 实体 | 文法 | 发放者 |
|------|------|--------|
| 工作项(显式) | `TI-<nnnn>`,零填充四位,团队内单调递增 | 团队主管,写台账时发放 |
| 工作项(推断) | `TIX-<8hex>`,`sha256(title + "\u0000" + phase_ref)` 前 8 位小写十六进制 | 生成器,回填历史条目时确定性计算 |
| 阶段 | `PH-<nnnn>` | 生成器,按阶段单位序号 |
| 里程碑 | `MS-<nnnn>` | 生成器,按 goal 判据序号 |
| 人员 | 名册 agent slug 原文 | 既有(已合法) |
| goal | `goal_slug` 原文([[STR-006]]);推断时为 team slug | 用户在 `team.md` frontmatter 声明 |

**中文标题 MUST NOT 直接作为 ID**——越界字符会被 DDL 拒绝;推断身份必须先经上述哈希。

**聚合下的唯一性(重要)**:N 个团队的台账装载进**同一个** `project.db`,而 `entity_ids` 是**全局** ID 命名空间(跨实体唯一,由 `AFTER INSERT` 触发器强制)。团队内单调递增的 `TI-<nnnn>` 因此会在聚合时**跨团队撞号**。生成器 MUST 在折叠时为工作项与阶段 ID 加团队命名空间前缀(形如 `<team-slug>.TI-0007` / `<team-slug>.PH-0002`;`.` 属 DDL 允许字符),使聚合后仍全局唯一;该前缀同时承载 FR-033 的机器可判定归属。**此约束只作用于聚合层——团队台账内部仍写不带前缀的 `TI-<nnnn>`**,以免团队侧的发放逻辑依赖 goal 拓扑。

### 3.1 两态交接(FR-027)

1. 历史条目(团队开始发放显式 ID 之前)以 `TIX-<8hex>` 回填,`identity: inferred`,并在表单 `inferred_fields` 留痕(`inferred_from` 非空,由 DDL 强制)。
2. 同一条目其后获得显式 ID 时,追加一行 `identity: explicit` + `supersedes: TIX-<hex>`。
3. 折叠时以显式 ID 为权威并合并其历史事件为**一条**记录;MUST NOT 同时呈现两条(IL-5)。
4. 推断身份时代发生重命名 → 哈希改变,旧 ID 按"本次未见"处理并进入材料缺口声明,不静默消失(Edge Case)。

## 4. 状态判定

团队条目生命周期 → 工作项四态 + 降级终态(FR-006):

| 团队侧信号 | 归一状态 |
|-----------|---------|
| 条目已解决/已归档/已采纳落地 | `completed` |
| 条目在本阶段被处理中、或 L2+ 已提交变更待验证 | `in-progress` |
| 有计划完成日且已越过、仍未完成 | `delayed` |
| 已入台账但尚未被任何阶段处理 | `not-started` |
| **无任何状态信号** | `unknown` — MUST NOT 记 `not-started`,MUST NOT 记 `0%`(FR-006) |

**引擎已兜住的两条**(团队侧无需另建防线,只需不伪造输入):
- 无勾选比、无明写百分比 → `project.progress.progress_pct = null` + `reason` 说明(实测,research.md E-3)。
- 无排期材料 → `gantt.bar_count = 0`、`has_planned_dates = false`,甘特不出图(实测,E-4)。
- 阶段聚合**排除** `unknown` 条目,不拖累也不虚增(实测,E-6)。

**成熟度锚定**:`state` 语义按 `maturity_at_event` 解释。L1(report-only)期间的条目 MUST NOT 因团队升级到 L2/L3 而被追溯改写为"已行动"(Edge Case)。

## 5. 派生实体关系

```text
              ┌─ team A ────────────────────────────┐
              │ team.md(goal_slug + Goal + members) │
              │ items.jsonl(append-only)            │──┐
              │ runs/*-report.md(仅历史回填)        │  │
              │ STATE.md(内联 [TI-nnnn] 标记)       │  │
              └─────────────────────────────────────┘  │
              ┌─ team B(声明同一 goal_slug) ───────┐  │   确定性折叠(FR-008/FR-032)
              │ team.md / items.jsonl / runs/ …      │──┼──▶ build-summary-input.py
              └─────────────────────────────────────┘  │        --goal <goal-slug>
                              …(该 goal 下全部 N 个团队)┘                │
                                                                          ▼
                                    .specify/project/goal/<goal-slug>/data/project-input.yaml
                                                                          │
                                                                          ▼
                                              summarize-project(零改动,FR-024,非交互模式)
                                              validate → project-db --load → --check → progress-engine
                                                                          │
                                                                          ▼
                              .specify/project/goal/<goal-slug>/{summary.md, assets/, data/}
```

**方向单一**:团队工件 → 表单 → 数据库 → 报告。反向零写入——总结步骤期间 `.specify/teams/**` 字节不变(FR-020)。`project.db` 为派生物,每次 `--load` 重建;累积状态的权威在各团队的 `items.jsonl`,不在数据库(research.md D-1),故"删除 goal 交付目录后重跑得同一份总结"成立。

**两个索引的分工**:
- `.specify/teams/<team-slug>/` —— **team 索引**,运行信息(事实源),回答"这个团队在怎么运行"。
- `.specify/project/goal/<goal-slug>/` —— **goal 索引**,唯一完整总结(派生物),回答"这个目标推进到哪里"。

**触发与写入者**:任一团队到达其阶段边界即触发该 goal 的刷新;写入者恒为该团队的主管(FR-021)。同 goal 下两个团队邻近触发时串行化为一次成功刷新,禁半写产物(FR-035)。
