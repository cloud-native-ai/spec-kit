# Data Model: 项目文档的 SDD 接入（特性级类别与文档型阶段门禁）

**Feature**: 077-doc-sdd-integration → Feature 077 项目文档的 SDD 接入（特性级类别与文档型阶段门禁）
**Spec**: [requirements.md](requirements.md)
**Note**: 本特性不新增数据库、台账或存储。九个实体全部搭在既有载体上：`requirements.md` 的头部区、
`flow-class-check.py --action lookup` 的返回记录、表达类 `plan.md` 的 `## Document Structure`、
状态脊的 `<!-- test-budget:begin -->` 围栏、`test-evidence/` 下的门禁输出、派发提示词的第①段。
本文件登记**字段面与判定规则**，是契约与测试的判定对象；字段取值域以本文件为 plan 期权威，
实现后由脚本常量与契约测试共同钉住。语义（类别判据、六面、算子表、槽位时点）不在此定义，只给 owner 指针。

## 实体一览

| # | 实体 | 承载 | 本特性变更 |
|---|------|------|------------|
| E1 | Flow Class Declaration Line（类别声明行） | 特性线 `requirements.md` 头部区 | 新增字段 |
| E2 | Class Resolution Record（类别解析记录） | `flow-class-check.py --action lookup` 的 stdout | 新增键族（同形记录） |
| E3 | Declaration Finding（声明形态发现） | 同命令的 stderr + 退出码 | 新增码 |
| E4 | Stage Wiring Card（阶段接线卡） | 七个命令模板内的一个子节 | 新增子节 |
| E5 | Document Structure Plan（文档结构产物） | 表达类 `plan.md` 的 `## Document Structure` | 新增章节 |
| E6 | Structure Violation（结构违规） | `doc-consistency-check.py --action structure` 的 findings | 新增动作与码 |
| E7 | Operator Result Record（算子结果记录） | 阶段门禁输出文件（`test-evidence/`） | 新增记录形态 |
| E8 | Docs Gate Slot Row（文档门禁槽位行） | 状态脊 `test-budget` 围栏的 JSONL 行 | 新增 `selection_basis` 取值 |
| E9 | Dispatch Class Payload（派发类别载荷） | 阶段提示词第①段 | 新增三元组 |

## E1 — Flow Class Declaration Line

**定位**：特性线声明自己类别的唯一载体。一条特性线（一条 spec 目录）恰好一行；索引与详情至多留指针。

**行形态**（逐字，字段名与取值大小写敏感）：

```text
**Flow Class**: <execution|expression>
```

**位置**：`## Related Feature` 标题之前的头部区；`requirements-template.md` 中位于 `**Status**:` 行之后、
`**Input**:` 行之前。

| 属性 | 取值 / 约束 |
|------|-------------|
| 字段名 | `**Flow Class**`（[[STR-001]]，requirements § Shared Strings） |
| 冒号与分隔 | 半角冒号 + **一个**空格 |
| 值域 | 封闭二值 `execution` / `expression` |
| 行数 | 头部区内恰 1 行；全文第二次出现即 `declaration-duplicate` |
| 行尾 | 无尾随空白；附加注释即 `declaration-malformed` |
| 缺省语义 | 全文无该行 → 类别按 `execution`，`source: default`，带 069 登记的默认标记 |
| 判定主体 | 作者手写；脚本 MUST NOT 从路径、文件名、内容或提交信息推断 |

**状态迁移**（本实体唯一的状态机）：

```text
absent ──作者写入──▶ declared ──作者改写（requirements 门禁通过之后）──▶ declared'
   │                    │                                              │
   └─(默认类运行)────────┘                          记 re-baseline 事件并按新类别
                                                    重跑 requirements 门禁集
```

`declared → absent`（删行）与 `declared → declared'`（改值）同属 re-baseline，不得静默翻转；
`declared` 的取值非法不进入本状态机（它是 E3 的阻断，不产生任何类别）。

## E2 — Class Resolution Record

**定位**：解析引擎对 `spec:<spec 目录名>` 键返回的记录。**与单元键逐字段同形**（八项键集，不新增第九项）。

| 字段 | 类型 | `spec:` 键的取值 | 说明 |
|------|------|------------------|------|
| `action` | 常量 | `lookup` | 与既有记录一致 |
| `checked_at` | ISO-8601 UTC | 运行时刻 | 与既有记录一致 |
| `unit_id` | string | 键原文（含 `spec:` 前缀） | 不剥前缀，便于与台账键区分 |
| `flow_class` | `execution` \| `expression` \| `null` | 已声明取声明值；未声明取 `execution`；取值非法取 `null` | `null` 只出现在退出码 1 |
| `source` | `declaration` \| `default` | 声明行在场即 `declaration`（含非法取值） | 与 `marker` 互斥（见下） |
| `marker` | string \| `null` | 未声明时为 069 登记的默认标记；否则 `null` | 字面量归 069 § Shared Strings |
| `basis` | `null` | 恒 `null` | 特性线的判定依据是声明行，不是台账列 |
| `neutral` | bool | 恒 `false` | 类中立清单只登记框架技能 |
| `error` | object \| `null` | `{label, detail}` 或 `null` | `label` 取 E3 的码 |

**互斥约束**：`source: declaration` 与 `marker: <默认标记>` MUST NOT 同时出现（requirements FR-004 的第三态缺陷）；
`flow_class: null` 与 `source: default` MUST NOT 同时出现（那会把作者错误读成未声明）。

**键文法**：`^spec:[a-z0-9][a-z0-9-]*$`。裸目录名、`feature:<ID>`、含 `/` 的路径都保持 `invalid-unit-id`（E3）。

## E3 — Declaration Finding

**定位**：解析在形态层发现的问题。三个码是**作者输入错误**（阻断），一个码是**机制缺席**（降级）。

| 码 | 触发 | 退出码 | 记录 | 处置 |
|----|------|--------|------|------|
| `invalid-class` | 声明行合法但取值在封闭集外 | **1** | `flow_class: null` / `source: declaration` | 阻断；stderr 点名文件:行号与取值 |
| `declaration-malformed` | 字段在场但形态不合规范（全角冒号 / 字段名大小写变体 / 尾随空白 / 行内注释） | **1** | 同上 | 同上；MUST NOT 落成「无该行」 |
| `declaration-duplicate` | 头部区/全文出现第二行同字段 | **1** | 同上 | 阻断；点名两处行号 |
| `declaration-misplaced` | 唯一一行位于 `## Related Feature` 之后 | **1** | 同上 | 阻断；点名行号 |
| `invalid-unit-id` | 键不合文法 | **2** | `flow_class: execution` / `source: default` | 降级标签同 `owner-unavailable` 的行为面 |
| `owner-unavailable` | owner 不可解析 / 引擎不可执行 | **2** | 同上 | 保持既有门禁集，不中断，不记通过 |

**优先级**：`owner-unavailable` 先于键文法判断（owner 先解析，与既有 `action_lookup` 顺序一致）；
同一文件既重复又错位时只报 `declaration-duplicate`（同一根因只报一次）。

**stderr 形态**（唯一新增的错误文本，`invalid-class` 与三个声明码共用）：

```text
<code>: <repo 相对路径>:<行号> carries '<值或形态摘要>', <判据一句话>
```

## E4 — Stage Wiring Card

**定位**：七个阶段命令模板里的一个三级子节，是该阶段「读一次类别、按类执行算子」的指令载体。
它**不承载**判据、取值定义、六面表或算子表——只出现一次 lookup 调用与两条 owner 指针。

| 属性 | 约束 |
|------|------|
| 承载文件 | `templates/commands/{requirements,clarify,plan,tasks,checklist,analyze,implement}.md`，各一处 |
| 子节数 | 每模板恰 1 个子节；子节内恰 1 次 lookup 调用 |
| 调用形态 | `flow-class-check.py --action lookup --unit-id "spec:<spec 目录名>"` |
| 必须出现 | 判据 owner 路径、门禁 owner 路径、分支句（表达类按阶段算子表执行本阶段登记的行；其余既有门禁集逐字不变）、降级可见句 |
| 禁止出现 | 任何 `G-` 算子 id、任何 face id 表、任何 `flow_class=` / `flow_class:` 赋值形、任何按特性号/路径/关键词的允许列表 |
| 时点 | 六个阶段 = 阶段入口（早于第一件依赖类别的动作）；`requirements` = 声明行写入之后、`validate-requirements.py` 之前 |
| 复用 | 委派技能 MUST NOT 再读一次；跨阶段不缓存、跨线不复用 |
| 子节边界 | 以固定三级标题起头、独占一个块（供 execution 反向守卫剥离，见 R-9） |

## E5 — Document Structure Plan

**定位**：表达类特性线 `plan.md` 内的 `## Document Structure` 章节，四项内容各落一个固定子节。

| 子节 | 字面量 | 行/列结构 | 判据 |
|------|--------|-----------|------|
| 章节树 | [[STR-003]] | 表 4 列：节名 / 父节 / 目的 / 边界 | 父节取顶层标记 `—` 或本表另一行节名；目的与边界非空 |
| 基准读者 | [[STR-004]] | 2 行：`**Readers**:` 与 `**Reading scenario**:` | 读者定义沿用 `shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议 |
| 证据清单 | [[STR-005]] | 表 4 列：断言 / 证据等级 / as-of / source | 三件套成组；语法归门禁 owner § 证据分级与 as-of |
| 事实 owner | [[STR-006]] | 表 3 列：事实 / owner 路径 / 章节锚 | 每条事实恰一个 owner；路径必须存在于仓库 |

**列名解析**：按表头名匹配，MUST NOT 猜列位；列名常量由检查器持有（code-first owner），测试从常量读取、不手抄。

**章节树的语义**：它是 implement 落文的**唯一结构来源**。顶层行 = `父节` 为 `—` 的行。

## E6 — Structure Violation

**定位**：`doc-consistency-check.py --action structure` 的 finding。码集封闭，分三族。

| 族 | 码 | 触发 | 判据 owner |
|----|----|------|-----------|
| 章节树语法 | `parent-unknown` | `父节` 指向本表不存在的节名 | requirements FR-014 |
| 章节树语法 | `chapter-duplicate` | 节名在同一份结构里重复 | 同上 |
| 章节树语法 | `chapter-purpose-missing` | `目的` 为空 | 同上 |
| 章节树语法 | `chapter-boundary-missing` | `边界` 为空 | 同上 |
| 章节树语法 | `chapter-tree-missing` | 表达类 `plan.md` 无 `## Document Structure` 或缺章节树子节 | requirements FR-013 |
| 两向比对 | `chapter-missing` | 落文缺计划中的节 | requirements FR-014 |
| 两向比对 | `chapter-unexpected` | 落文出现计划外的**顶层**章节 | 同上（非顶层不因本条转红） |
| 证据面 | `evidence-unlisted` | 带证据标记的断言在清单里无对应行 | requirements FR-015 |
| 证据面 | `grade-invalid` / `as-of-malformed` / `source-missing` / `grade-asof-unpaired` | 复用既有证据码，不自造同义码 | 门禁 owner § 证据分级与 as-of |
| owner 面 | `owner-duplicate` / `owner-path-missing` / `owner-anchor-missing` | 同一事实两行 owner / 路径不存在 / 锚为空 | requirements FR-016 |

**输出与判定**：`status` ∈ {`ok`, `not-applicable`} + 退出码 0；有 finding 或 `status: fail` → 退出码 1；
输入错误 → 2。主体为执行类/未声明 → `status: not-applicable` 并打印 `class=` / `source=` 与非空伴生量
（被检查文件数），MUST NOT 呈现为「0 违规通过」。重跑同一份 `plan.md` MUST 得同一违规集（顺序稳定）。

## E7 — Operator Result Record

**定位**：一次文档门禁运行里每个 blocking 算子的结果行，写在 `test-evidence/` 的输出文件中；它是 U4 第 (a)/(b)
两项与槽位 `passed`/`failed` 计数的唯一来源。

| 字段 | 取值 | 说明 |
|------|------|------|
| `operator_id` | `G-…` | 取自门禁 owner 的算子表，不在此重列 |
| `face` | 六面 face id 之一 | 同上 |
| `verdict` | `pass` \| `fail` \| `not-evaluated` \| `not-applicable` | 封闭四值 |
| `entry` | 命令串或「人工/受委托代理」 | 算子入口 |
| `rc` | 整数或 `null` | 可执行算子的退出码 |
| `evidence_path` | 仓库相对路径 | 指向该算子的原始输出 |

**计数规则**（槽位的 `passed`/`failed` 由此导出）：`pass` 与 `not-applicable` 计 `passed`；
`fail` 与 `not-evaluated` 计 `failed`；逐面的 `not-evaluated` 原因写进 `evidence_ptr` 指向的门禁输出，
MUST NOT 并入 `passed`、MUST NOT 以 0 表示未运行。

## E8 — Docs Gate Slot Row

**定位**：表达类线上替换两槽位测试预算的两个文档门禁槽位行，落在既有状态脊 `test-budget` JSONL 围栏内。

| 字段 | 表达类取值 | 执行类取值（不变） |
|------|-----------|--------------------|
| `seq` | 严格递增 | 同 |
| `slot` | `baseline`（implement 起点）/ `closure`（review 通过后） | 同 |
| `stage` | `implement` / `closure` | 同 |
| `selection_basis` | **`docs-gate-full`** | `full-suite` |
| `command` | 该次文档门禁命令串（四面 + 结构两向；站点层存在时加构建算子） | `run-tests.sh …` |
| `rc` | 门禁进程退出码 | 同 |
| `passed` | verdict ∈ {`pass`, `not-applicable`} 的 blocking 算子数 | 通过用例数 |
| `failed` | verdict ∈ {`fail`, `not-evaluated`} 的算子数 | 失败用例数 |
| `failed_names_path` | 失败算子 id 名单文件 | 失败用例名单 |
| `baseline_compare` | closure：算子 id 集合的名称级差集（`comm -13` 形态） | closure：失败名单名称级差集 |
| `evidence_ptr` | 门禁输出文件 | 测试输出 |

**不变量**：槽位数（2）、时点、槽位顺序、closure 名称级差集形态与 `audit-test-budget.py` 的判定**全部不变**；
未运行时 MUST NOT 写槽位行，MUST NOT 记 0。字段集不新增（见 R-5 的实测：审计对本表的变化零感知）。

## E9 — Dispatch Class Payload

**定位**：每次阶段派发时写进提示词第①段的三元组。它是类别的**唯一载体**（环境变量不被远端子代理继承）。

| 键 | 取值 | 缺失后果 |
|----|------|----------|
| `flow_class` | `execution` / `expression` | 派发构造缺陷，U4 不放行 |
| `source` | `declaration` / `default` | 同上 |
| `marker` | 默认标记字面量或空 | 同上（`source: default` 时空值即缺字段） |

**取值来源**：该线 `requirements.md` 的声明行，经 E2 记录取得，**每次派发前解析一次**。
状态脊里的类别行只是带日期的观测，MUST NOT 充当取值来源；重入时重新解析并与观测比对，不一致记 re-baseline。

## 关系视图

```text
E1 声明行 ──(解析)──▶ E2 记录 ──(分支)──▶ E4 接线卡（七模板，读一次）
   │                       │
   │                       ├─ 形态错误 ──▶ E3 发现（阻断/降级）
   │                       └─ 表达类 ──┬─▶ E5 结构产物（plan）
   │                                    ├─▶ E6 结构违规（--action structure）
   │                                    ├─▶ E7 算子结果 ──▶ E8 槽位行
   │                                    └─▶ E9 派发载荷 ──▶ U4 四项
   └──(re-baseline)──▶ 重跑 requirements 门禁集
```

## 校验规则汇总（可判定面）

| 规则 | 判定器 | 形态 |
|------|--------|------|
| E1 行文法与位置 | `flow-class-check.py --action lookup`（`spec:` 键） | 退出码 0/1/2 + E2/E3 |
| E1 单一性 | 同上（`declaration-duplicate`） | 退出码 1 |
| E2 记录形态 | 单元测试断言字段集与互斥约束 | 字段相等 / 不存在 |
| E4 接线形态 | 契约测试（每模板恰一次 lookup、零副本、剥离后与基线字节相同） | 计数 / 字符串 / SHA-256 |
| E5 四子节 | `doc-consistency-check.py --action structure` | 退出码 + findings |
| E6 码集封闭 | 同上（码常量由检查器持有，测试从常量读） | 集合相等 |
| E7 计数规则 | 槽位行 + U4 校验 | 整数与 verdict 集合 |
| E8 槽位不变量 | `audit-test-budget.py`（不改） | `slots=baseline:N closure:N` |
| E9 载荷在场 | 驱动技能契约测试 + U4 (c) | 三元组解析 |
