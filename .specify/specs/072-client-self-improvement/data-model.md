# Data Model: 072-client-self-improvement

**Requirement → Feature**: `072-client-self-improvement` → Feature 072 客户项目的持续反馈与自我提升

实体 E1–E10；校验规则 V1–V24；状态迁移两则（武装态解析、条目生命周期）。被前序特性拥有的实体（代码段记录、覆盖率回执、反馈存储）只引用、不复制。

## E1 客户条目（client finding entry）

复用既有反馈条目形态与一文一件布局（`.specify/memory/feedback/<entry-id>.md`），不新建存储、不新增字段族。

| 字段 | 来源 | 规则 |
|------|------|------|
| `unit_id` | capture 解析 | 必须是 `custom:<owner>/<name>`（V1） |
| `unit_type` | 引擎 | 必须是 `custom-unit`（V2） |
| `run_id` | 记录头日期戳 | ISO-8601 UTC 秒级，与归档名同源（V3） |
| `probe` | 引擎解析 | 外部探针对象，引擎在记录时解析，调用方不得设置（V4） |
| `kind` / `slice` | 引擎解析 | 外部探针对象决定 `external` / `host-custom`（V5） |
| `review`（载荷） | capture 拼装 | 指针形态，字段集封闭（见 E6，V6–V9） |
| `points` | capture 拼装 | 指向记录的后续动作行（V10） |
| `disposition` | 引擎 | 沿用既有处置语义；处置标记不构成闭环证据（V11） |
| `created` | 引擎 | 条目创建时间戳；度量口径的边界依据（V12） |

**校验规则**
- V1–V2：非 `custom:` 单元或类型不匹配时引擎拒绝（exit 2），capture 不得预改单元以绕过。
- V3：`run_id` 唯一对应一份代码段记录；重复 capture 命中引擎 `(unit, run)` 幂等键。
- V6：载荷字段集封闭为五项——记录路径、适用性取值、六项按严重度计数（含零）、运行标识、所属单元。
- V7：载荷 MUST NOT 含意见正文、逐文件裁决清单、回执逐文件字段、变更文件总数、非代码文件数。
- V8：六项计数逐项抄自 `report --summary` 机读输出，不得重数、估算、省零或并级。
- V9：适用性取值只抄 `run`（V14 保证其余情形不产生条目）。
- V10：points 是后续动作指引（去读记录），不复制记录内容。
- V11：`processed`/`ignored` 只是本地元数据（「路由≠完成」锚点之一）。
- V12：`created` 是闭环证据（owner 文件 mtime 晚于它）与捕获覆盖边界（通道武装时刻）的依据。

## E2 客户单元（client unit）

客户项目自定的耐久主体标识 `custom:<owner>/<name>`；`<owner>`/`<name>` 由客户项目自定（词法由引擎 `_CUSTOM_UNIT_RE` 约束）。可编辑定义在客户项目内部，不在框架侧。生命周期：声明（探针注入时进入注册表）→ 在场（可被解析）→ 消失（注册表中删除；其条目仍可读，V13）。

- V13：单元消失后条目不得重写、删除或重新归属；消化路径报告解析失败（C-31）。

## E3 外部探针对象（external probe object）

载体：`.specify/memory/feedback/probes/` 下的探针文件，由 `probe-utils.py --action probe-inject` 产出；本特性只引用其存在性，不另造登记面，不改注册表。

| 字段 | 规则 |
|------|------|
| `object_id` | 以 `ext-` 开头（引擎校验，V14） |
| 所属 class | `kind: external`（引擎校验） |
| `unit` | 匹配 `custom:<owner>/<name>`（V15） |
| 数量 | 0 / 1 / ≥2 直接决定武装态三值（V16） |

- V14–V15：探针文件形态校验归引擎；capture 只消费机读清单。
- V16：武装态只由外部探针对象计数 + 显式参数决定，不得由条目历史推断。

## E4 武装态（armed state）

一次运行对「能否采集」的显式判定结果（解析一次、全程复用，V17）：

| 值 | 字面量 | 条件 |
|----|--------|------|
| 已武装 | `client-channel-armed` | 恰有一个外部探针对象，或显式 `--client-unit` 且该单元有外部探针对象 |
| 未武装 | `client-channel-unarmed` | 零个外部探针对象；或显式单元无对应探针对象；或注册表不可用 |
| 歧义 | `client-unit-ambiguous` | ≥2 个外部探针对象且无显式单元 |

- V17：同一运行内武装态解析一次；capture 与消化呈报各自解析各自的运行，不共享运行间状态。
- V18：显式单元只消解歧义，永不豁免探针存在检查（无探针对象 → 未武装，不是计数不可得）。
- V19：注册表不可用 → 未武装 + 不调用 record + 无 `kind`/`slice` 遗留条目（fail closed）。

## E5 采集结论行（capture outcome line）

非交互路径第五步输出 exactly one 行：`client-capture: <token> [detail]`。

- 客户项目 token 闭集五值：`client-channel-armed` / `client-channel-unarmed` / `client-unit-ambiguous` / `no-capture-object` / `counts-unavailable`（V20）。
- 框架帽形态：`client-capture: skipped: <帽子依据句>`——不属于五值闭集，不写成五值之一（V21）。
- V22：该行与本次适用性取值同时出现在运行结论中；该行永不缺失、永不由「本次无发现」替代。
- V23：capture 步骤恒退出 0；步骤输出一行，不多不少。

## E6 代码段记录（code segment record）——引用实体

Feature 071 所有。本特性消费其三个事实：文件路径（指针指向）、记录头日期戳（运行标识）、`report --summary` 的六项计数（载荷抄录）。本特性不改其形态、轮转与回执（V24）。

- V24：对记录/回执/报告代码段小节的任何改动都是违规；唯一授权修订是步骤枚举（E5 的上游，C-10）。

## E7 后续载体（carrier）

一条被消化客户条目的唯一后续机，闭集三值：

| 值 | 触发条件 | owner（引用） |
|----|----------|----------------|
| todo Park 模式 | 自由漂浮的改进想法（默认落点） | todo-in-context 指南 |
| 新需求规格 | 发现约束本项目源码必须实现什么 | requirements 流程 |
| 改进循环主体 | 发现落到满足执行主体判据的客户工件 | 自我提升流程 |

规则：恰好一个（V25）；指派写入路由台账行并在呈报列出（V26）；无法裁决 → 报为 undecided、留给下次消化，不静默丢弃（V27）。

## E8 路由台账行（routing backlog row）——引用实体

`.specify/memory/feedback/backlog.md`，既有载体。本特性消费的行语义：`carried-by-spec-*` = 被承接 ≠ 已完成；`open-unverified` = 先复测再行动；`open` = 未指派。闭环判定（V28）：行形态为承接类 **且** 指名 owner 文件存在 **且** 其 mtime 晚于条目 `created`。

## E9 循环度量视图（metrics view）

即读即建、不落盘的四指标视图（引擎只读动作 `client-metrics` 的输出）：

| 指标 | 分子 | 分母 | 来源 | 特殊标注 |
|------|------|------|------|----------|
| 捕获覆盖率 | 有对应外部条目的记录运行戳去重数 | 武装时刻之后的记录运行戳总数 | 记录文件 + 条目 | 排除数披露 |
| 进入回路比例 | 有承接类台账行的条目数 | 外部条目总数 | 条目 + 台账 | — |
| 闭环比例 | 有 owner 文件变更证据的条目数 | 外部条目总数 | 条目 + 台账 + 文件 mtime | 路由≠完成 |
| 重复发现率 | 任一 (文件,严重度) 对在该单元更早记录里已出现的条目数 | 外部条目总数 − 不可读记录排除数 | 条目所指记录正文 | 粗代理 |

- V29：任一分母为零或缺数据 → 该指标 `not-evaluated` + 原因；永不显示 0/100%。
- V30：四指标永不合成单一数字；永不写盘；永不作为门禁/状态转换/阈值输入。
- V31：重复率 (文件,严重度) 对从记录正文确定性抽取；记录不可读 → 分子分母同排除并披露计数。

## E10 帽子判定（hat verdict）——引用实体

两顶帽子 owner（`shared/definitions/dogfooding-definitions.md` § 2.1）判定：根级拥有 `templates` / `skills` / `shared` / `scripts` / `src/specify_cli` 五目录 → 框架项目；否则客户项目。`feedback/` 目录不参与判定。

- V32：capture 与消化呈报读取该判定，不得各自实现变体判据。

## 状态迁移

**武装态解析**（每次 capture 运行一次）：
```
[显式 --client-unit?] --语法错--> skipped 行（零条目，exit 0）
    |合法
    v
[注册表可用?] --否--> client-channel-unarmed（不调用 record）+ 升级指引
    |是
    v
[显式单元有探针对象?] --否--> client-channel-unarmed + 注入指引
    |是
    v
[显式单元?] --是--> client-channel-armed
    |否
    v
[外部探针对象数] 0 --> client-channel-unarmed + 注入指引
              1 --> client-channel-armed
             ≥2 --> client-unit-ambiguous（不猜/不轮/不选最近）
```

**采集执行**（armed 之后）：
```
[triage == run?] --否--> no-capture-object（零条目）
    |是（且帽子=客户）
    v
[report --summary 可得计数?] --否(exit 2)--> counts-unavailable（零条目）
    |是（exit 0/1 均照常）
    v
record(unit, run=记录戳, 指针载荷)
    |--duplicate--> 视为已记录，exit 0，无第二条
    |--exit 2----> counts-unavailable（零条目，运行不阻断）
    v
client-channel-armed + 条目 id
```

**条目生命周期**（经消化路径，既有机制承载）：
```
open（已采集未消化）--消化+指派载体--> carried（backlog 行：carried-by-*）
carried --owner 文件确有变更证据--> closed（呈报计入闭环）
carried --复测不通过-------------> open-unverified（先复测再行动）
任何状态 --单元从注册表消失-----> 仍可读、不重写、不删除（呈报解析失败）
```
