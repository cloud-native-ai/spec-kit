# Data Model: 074a-authorized-routing

**Requirement → Feature**: `074a-authorized-routing` → Feature 074 Goal/Team/Agent 与 SDD 开发流程统一

本切片实体 E1–E9、校验规则 V-1…V-29、三个状态机（授权解析、嵌套运行生命周期、裁决失效与取代）。
实体是父设计 `.specify/specs/074-goal-team-sdd-unification/data-model.md`（父 E1–E11）按本切片需求条目
的裁剪；**父 E6（`## Nested SDD Runs` 报告段）与父 E8（ledger 归因行）不在本切片**，由
`074b-nested-governance` 承接（见 § 迁移与裁剪）。

由更早特性拥有的实体（line registry 条目、state spine、ledger item、team run report、Goal/Target 定义、
中性元数据键表）**按路径引用，不复述**：本切片只在 FR 明确要求处向其中加入字段，并在下列 E 节逐项标出 owner。

**本文件的一条声明规则**：路由输入的名称在此出现，因为 handoff 与裁决记录携带它们；它们的
**封闭取值域、三值裁决表、优先级与理由码词表由 `shared/definitions/sdd-routing-definitions.md` 拥有**，
本文件与任何其它位置 MUST NOT 复述（V-19 是机械守卫）。

---

## E1 SDD Invocation（嵌套 SDD 调用）· 父 E1

一次由授权席位启动的有界嵌套运行。它不是新存储：身份是既有 line id，持久状态是既有 state spine。

| 字段 | 来源 | 规则 |
|------|------|------|
| `line_id` | 既有 line registry | 嵌套运行**就是**一条写线；不得另造 id 族（V-1） |
| `run_id` | 既有 state spine / envelope | 与 line_id 配对；一线一 spine（V-2） |
| `goal_ref` | 调用方声明 | 必填；指向已定义的 Goal（V-3） |
| `target_ref` | 调用方声明（可选） | 缺省 = 对 Goal 整体运行；非空时必须是该 Goal 下的 `open` Target（V-4） |
| `team_slug` | 派发载荷 | 必填；授权解析的坐标之一（V-5） |
| `seat_slug` | 派发载荷 | 必填；授权解析的坐标之一（V-5） |
| `scope` | 调用方声明 | 授权的工件/领域范围；必须落在该席位 territory 内（V-6） |
| `verdict_ref` | 路由裁决记录（E4） | 必须引用一条裁决，且其 verdict 为 [[STR-004]]（V-7） |
| `outcome` | 运行结束时确定 | [[STR-007]] / [[STR-008]] / [[STR-009]]（V-8） |
| `stages_reached` | 驱动自身 | 阶段名以驱动 owner 为准，本文件不复述名册（V-9） |
| `artifact_paths` / `evidence_paths` | 驱动自身 | 路径列表，逐项可定位（V-10） |
| `findings` | review 阶段 | 未决 findings；空集与「未评估」不是同义（V-11） |
| `anomaly_line` | 快速失败纪律 | `未发现异常` 或行首 `ANOMALY:` 行（V-12） |
| `integration_identity` | E6 | 缺一即 handoff 不完整（V-13） |

**V-1**: 嵌套运行 MUST 复用既有 line registry 与 worktree-per-write-line；`line_id` 不是本特性新开的编号族。
**V-2**: 状态脊落 `.specify/state/`，与独立驱动同形；MUST NOT 新增第二脊。
**V-3**: `goal_ref` 缺失 → 入口校验拒绝（不进入 U0）。
**V-4**: 终态 Goal 或终态/关闭 Target → 拒绝并回述 goal 引擎裁决，MUST NOT 静默改范围。
**V-5**: `team_slug` 或 `seat_slug` 缺失 → 拒绝；授权 MUST 按 (team, seat) 解析（E2）。
**V-6**: `scope` 超出该席位 territory → 拒绝；并发判定交给既有 line registry，不新增第二套并发机制。
**V-7**: `verdict_ref` 缺失或其 verdict 不是 [[STR-004]] → 拒绝启动（[[STR-005]] 不产生 SDD 运行；
[[STR-006]] 停等裁定）。
**V-8**: 三值封闭：[[STR-007]]（review 后交接成功）/ [[STR-008]]（授权或前置条件失败）/
[[STR-009]]（运行失败、卡死、超时、预算触顶）。四值以上一律非法。
**V-9**: 阶段名册 owner 是驱动；本切片只记录「到达了哪些」，不复制名册。
**V-10**: 每个路径 MUST 在交接时存在；不存在者按缺失处理，不用占位符替代。
**V-11**: `findings = []` 表示「review 后无未决发现」；无 review 证据时 MUST 记 `not-evaluated` 语义的显式文本，
不得用空集冒充。
**V-12**: 缺异常行即交接不完整，`outcome` MUST NOT 为 [[STR-007]]。
**V-13**: `integration_identity` 四字段（line id / branch / worktree path / HEAD commit）齐备且 branch 被点名保留；
缺项即不完整。

---

## E2 Authorization（有效授权）· 父 E2

按 (team, seat) 解析的一对值，其有效值是两个半边的 AND。

| 字段 | 来源 | 规则 |
|------|------|------|
| `agent_capability` | Agent 定义 frontmatter（E3 侧） | 缺省 [[STR-003]]（V-14） |
| `seat_policy` | `team.md` frontmatter `[[STR-010]]`（E3） | 缺省 [[STR-003]]（V-15） |
| `effective` | 引擎 | 二者的逻辑 AND（V-16） |
| `supplying` | 引擎 | 记录哪一半供了什么值，失败时点名失败的一半（V-17） |
| `basis` | 引擎 | 解析所用的两个来源路径 + seat slug，逐项可定位（V-18） |

**V-14**: Agent 定义未声明键 → [[STR-003]]（不因缺省而放行）；值只允许 [[STR-002]] / [[STR-003]]。
**V-15**: `team.md` 无 `[[STR-010]]` 键、或其中无该 seat 条目、或该条目无键 → [[STR-003]]。
**V-16**: 只有两半都为 [[STR-002]] 时 `effective` 为 [[STR-002]]；任何一半为 [[STR-003]] 即 [[STR-003]]。
**V-17**: 拒绝时 MUST 点名失败的那一半（`agent` / `seat` / `both`），MUST NOT 只报「未授权」。
**V-18**: 记录 MUST 含两个来源文件路径与 seat slug；无来源路径的裁决不可复核。
**V-19**: 本文件与任何其它位置 MUST NOT 出现第二份「输入取值域 / 三值裁决表 / 理由码词表」；唯一 owner 是
`shared/definitions/sdd-routing-definitions.md`。审计方式：按落盘短语反向计数
（`.specify/shared/guidelines/one-source-of-truth.md` § Reference, don't copy）。

---

## E3 Seat Policy（席位策略）与 Agent Capability · 父 E3

一个键的两种存储形态；两者各由既有 owner 拥有，本切片各增加恰好一个键。

| 载体 | owner | 本切片的增量 |
|------|-------|--------------|
| Agent 定义 frontmatter（`.agent.md`） | 中性元数据键集 `NEUTRAL_AGENT_METADATA_KEYS`（`src/specify_cli/__init__.py`） | 新增一键：值域 [[STR-002]] / [[STR-003]]、缺省 [[STR-003]]、不渲染到任何宿主工具，并纳入框架装配键集 |
| `team.md` frontmatter | `skills/internal/create-team/references/create-mode.md` § Persisted `team.md` schema | 新增 `[[STR-010]]` 块映射，按 seat slug 键控，条目内为同一键 |

**V-20**: 席位块映射只接受块式写法；流式映射判为畸形输入，点名席位后拒绝，MUST NOT 尽力解析。
**V-21**: 席位 slug MUST 与 `members[].role` 或席位实例 slug 之一对应；不对应的条目被报告为悬空，不静默忽略。
**V-22**: 既有团队无该键时行为逐字节不变（缺省 [[STR-003]]），创建流程 MUST NOT 为存量团队自动补键。
**V-23**: Agent 侧的值 MUST 为扁平标量——该载体不支持嵌套 YAML（`parse_agent_frontmatter` 对缩进行报错），
故不接受列表或映射形态的声明。

---

## E4 Routing Verdict（路由裁决记录）· 父 E4

| 字段 | 来源 | 规则 |
|------|------|------|
| `inputs` | 调用方声明（5 项） | 逐项记录原值；缺项即 [[STR-006]]（V-24） |
| `verdict` | 引擎 | 三值之一，取值由 owner 定义（不在此复述） |
| `reason_code` | 引擎 | 来自 owner 的封闭词表；多条命中时按固定次序取第一条（V-25） |
| `actor` | 调用方 | 作出声明的单元标识（席位或 agent） |
| `override` | 用户裁决（可选） | 含用户指令原文与被覆盖的 verdict（V-26） |
| `recorded_at` | 引擎 | 时间戳；同一裁决复用到输入变化为止（V-27） |

**Record carrier in this slice**（`../requirements.md` § Cross-Slice Design Attribution D-2）：本切片不定义
team run report 的固定段，故上表六个字段落在 **Agent 执行证据**里；handoff 与调用方结果按稳定路径引用该记录。
team report 段的 verdict reference 随 `074b-nested-governance` 的段契约落地时读同一条记录、不得重算。

**V-24**: 任何输入缺失 → [[STR-006]]；任何输入值落在 owner 声明的封闭取值域之外 → [[STR-006]]；
MUST NOT 补默认值后继续。
**V-25**: 固定优先级 [[STR-006]] > [[STR-004]] > [[STR-005]]；同一分支内多条件命中时按声明次序取首条理由码，
输出 MUST 同时携带全部命中条件，使复算可复现。
**V-26**: 用户指令覆盖裁决时 MUST 记为裁定（用户指令 + 被覆盖 verdict），引擎 MUST NOT 反向覆盖用户。
**V-27**: 裁决 unit = 一次成员职责；输入变化即失效并重新裁决，旧裁决保留在记录中，新裁决取代其效力。

---

## E5 Nested Run Handoff（交接件）· 父 E5

E1 的对外投影，也是外层唯一消费形态。字段集封闭：outcome、stages reached、artifact paths、evidence
paths、unresolved findings、anomaly line、integration identity（含被点名的保留 branch）。

**V-28**: 字段集封闭——不得以自由散文替代任一必填项；缺任一项即 `incomplete`，外层 MUST NOT 报成功。
**V-29**: handoff MUST NOT 触发 merge 或 push；出现二者任一即判定为越权（外层确认门 owner 不变）。

---

## E6 Integration Identity（集成身份）· 父 E7

| 字段 | owner |
|------|-------|
| line id | 既有 line registry |
| branch | 既有 line registry（`branch` 字段） |
| worktree path | 既有 line registry（`worktree_path` 字段） |
| HEAD commit | 交接时从工作树读取（不落第二份状态） |

**Retained branch**: handoff MUST 点名该 branch，使外层知道合并在哪里发生。本实体不新增存储字段——
四值全部来自既有 line 条目与一次 git 读取。

---

## E7 深度 2 嵌套链与派发谓词（governance entity）· 父 E9

| 层 | 允许承载 | 禁止 |
|----|----------|------|
| 团队编排者 | 派发成员 | — |
| 成员 driver host | 承载**一个** SDD 运行（有效授权 [[STR-002]] 且为 SDD 指派） | 承载第二个（除非团队在既有 line 机制内声明更高上限）；virtual 模态承载 |
| 阶段执行者 | 执行单个阶段 | 启动/承载任何 SDD 运行；自身声明 [[STR-002]] |

**Predicate（三条件同时成立才允许提示词点名/指派驱动）**: 收件 Agent 定义声明 [[STR-002]] ∧ 其席位策略声明
[[STR-002]] ∧ 所指派任务是 SDD 指派。任一不成立 → 保持原禁令并点名失败条件。
**Additional prohibitions**: SDD-within-SDD；阶段执行者启动运行；virtual 成员承载。

---

## E8 Golden Case Row（黄金用例行）· 父 E10

| 字段 | 规则 |
|------|------|
| `case_id` | 稳定短 id，golden 表内唯一 |
| 5 项输入 | 原值（取自 owner 的封闭取值域，不复述域） |
| `expected_verdict` / `expected_reason_code` | 来自 owner 的封闭词表 |
| `note` | 该行覆盖的需求面（feature / maintenance / cross-cutting / irreversible / ambiguous / conflicting / bounded definition-correction） |

用例行集合的 owner 是 owner 文档 § Golden case table；本实体只声明行的字段面，MUST NOT 复制行。

---

## E9 派发载荷增量（dispatch payload）· 父 E11

既有派发载荷新增两个字段：`team_slug` 与 `seat_slug`（缺一即授权不可解析）。载荷其余字段面由
`shared/definitions/subagent-definitions.md` § Execution Topology Declaration 拥有，本切片不增改。

---

## 状态机 1 — Authorization resolution

```text
agent side:  declared "allowed" ──┐
             absent / "forbidden" ┴─► agent_capability = allowed | forbidden
seat side:   seats[seat] = "allowed" ──┐
             no seats / no entry / no key ┴─► seat_policy = allowed | forbidden

effective = agent_capability AND seat_policy
  allowed  → dispatch may name the driver (predicate condition 1+2 met)
  forbidden → dispatch refuses, names the failing half (agent | seat | both)
```

Terminal states: [[STR-002]]、[[STR-003]]。没有第三值，也没有 "unknown"——不可读的输入是畸形输入错误，
永不作为策略值。

## 状态机 2 — Nested run lifecycle

```text
declared duty
   │  routing verdict = sdd (E4)
   ▼
entry validation (E1 V-3…V-7) ── fail ──► outcome = blocked (handoff, failing condition named)
   │  pass
   ▼
line registration (existing registry) → U0 … review (driver stages)
   │                                   │
   │ timeout / stall / budget          │ review settles
   ▼                                   ▼
outcome = failed                     outcome = completed
   └──────────► handoff (E5) ◄──────────┘
                    │
                    ▼
   invoking Agent's own result carries the handoff by stable path (FR-017)
                    │
                    ▼
   outer layer writes the report section + ledger row (074b) and adjudicates merge/push
                                                        (never the nested run)
```

状态机在本切片止于「调用方结果按稳定路径携带 handoff」；`## Nested SDD Runs` 段与 ledger 归因行的写入属
`074b-nested-governance`（父 E6 / 父 E8），本切片不实现、其夹具不断言该标题字面量。

## 状态机 3 — Verdict supersession

```text
verdict V1 recorded (inputs I1)
   │  an input changes → I2
   ▼
re-route → V2 ; V1 retained in the record, V2 supersedes its effect
   │  inputs unchanged
   ▼
V1 reused for this duty (no re-evaluation, no re-recording)
```

---

## 迁移与裁剪

| 本地实体 | 父实体 | 处置 |
|----------|--------|------|
| E1 SDD Invocation | 父 E1 | 继承 |
| E2 Authorization | 父 E2 | 继承 |
| E3 Seat Policy 与 Agent Capability | 父 E3 | 继承 |
| E4 Routing Verdict | 父 E4 | 继承；记录面按 D-2 收窄为 Agent 执行证据 |
| E5 Nested Run Handoff | 父 E5 | 继承 |
| E6 Integration Identity | 父 E7 | 继承（本地重排号） |
| E7 深度 2 链与派发谓词 | 父 E9 | 继承（本地重排号） |
| E8 Golden Case Row | 父 E10 | 继承（本地重排号） |
| E9 派发载荷增量 | 父 E11 | 继承（本地重排号） |
| — | 父 E6 `## Nested SDD Runs` 报告段 | **不继承**：`074b-nested-governance` |
| — | 父 E8 Ledger Attribution Row | **不继承**：`074b-nested-governance` |

校验规则 V-1…V-29 全部落在上表继承的实体上，故**编号与父文件逐一对应、不做重排**——父规则集在本切片
范围内是完整集合，重排只会制造两套编号。
