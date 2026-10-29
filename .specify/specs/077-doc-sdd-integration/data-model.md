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
| E9 | Dispatch Class Payload（派发类别载荷） | 阶段提示词第①段 | 新增四元组 |

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
| 缺省语义 | 无该行 → 类别按 `execution`，`source: default`，带 069 登记的默认标记；存量线另可获 advisory 码 `declaration-absent`（退出码 0、不计缺陷，见 E3） |
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

**定位**：解析引擎对 `spec:<spec 目录名>` 键返回的记录。**与单元键逐字段同形**（九项键集，不新增第十项——`error` 早在单元键记录里就有，本特性只是让它对 `spec:` 键也有取值）。

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

**定位**：解析在形态层发现的问题。四个码是**作者输入错误**（阻断，退出码 1）；一个码是**存量缺省**（advisory，退出码 0）；两个码是**机制缺席 / 输入非法**（降级，退出码 2）。

| 码 | 触发 | 退出码 | 记录 | 处置 |
|----|------|--------|------|------|
| `invalid-class` | 声明行合法但取值在封闭集外 | **1** | `flow_class: null` / `source: declaration` | 阻断；stderr 点名文件:行号与取值 |
| `declaration-malformed` | 字段在场但形态不合规范（全角冒号 / 字段名大小写变体 / 尾随空白 / 行内注释） | **1** | 同上 | 同上；MUST NOT 落成「无该行」 |
| `declaration-duplicate` | 头部区/全文出现第二行同字段 | **1** | 同上 | 阻断；点名两处行号 |
| `declaration-misplaced` | 唯一一行位于 `## Related Feature` 之后 | **1** | 同上 | 阻断；点名行号 |
| `declaration-absent` | **存量线**头部区无该字段（FR-001 的作用域之外） | **0** | `flow_class: execution` / `source: default` / `marker: <默认标记>` / `error: {label: declaration-absent}` | advisory：提示可补声明；不阻断、不计缺陷、不进判定集合 |
| `invalid-unit-id` | 键不合文法 | **2** | `flow_class: execution` / `source: default` | 降级标签同 `owner-unavailable` 的行为面 |
| `owner-unavailable` | owner 不可解析；或**调用方无法执行引擎**（可观察触发：引擎文件不存在 / 操作系统拒绝执行 / 进程未产出记录——此时标签由调用方写下，引擎不在场自然无记录） | **2** | 同上 | 保持既有门禁集，不中断，不记通过；载荷 `error` 位取同一标签 |

**优先级**：`owner-unavailable` 先于键文法判断（**本特性把 owner 解析提前到键文法之前——这是相对既有 `action_lookup` 的登记变更**：既有顺序是先 `UNIT_ID_RE` 后 `parse_owner`，因此「键非法 **且** owner 不可解析」这一输入过去报 `invalid-unit-id`，此后报 `owner-unavailable`。两者同为退出码 2、门禁集不变，差异登记在 requirements FR-011 的豁免①）；同一文件既重复又错位时只报 `declaration-duplicate`（同一根因只报一次）。`declaration-absent` 与 `owner-unavailable` 互斥：前者要求「引擎与 owner 都可用」这一前提成立。

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
| 子节标题 | 逐字取 `research.md` R-9 登记的唯一字面量（该字面量的登记处就是 R-9，MUST NOT 在别处再登记一份；模板、契约、测试、剥离器都从它取值） |
| 调用形态 | `flow-class-check.py --action lookup --unit-id "spec:<spec 目录名>"` |
| 必须出现 | 判据 owner 路径、门禁 owner 路径、分支句（表达类按阶段算子表执行本阶段登记的行；其余既有门禁集逐字不变）、降级可见句、**退出码 1 的停止句**（解析报作者输入错误时本阶段停下，并以阶段协议的异常行形态作最后一行输出；MUST NOT 落入「既有门禁集逐字不变」那支） |
| 禁止出现 | 任何 `G-` 算子 id、任何 face id 表、任何 `flow_class=` / `flow_class:` 赋值形、任何按特性号/路径/关键词的允许列表 |
| 时点 | 六个阶段 = 阶段入口（早于第一件依赖类别的动作）；`requirements` = 声明行写入之后、`validate-requirements.py` 之前 |
| 复用 | 委派技能 MUST NOT 再读一次；跨阶段不缓存、跨线不复用 |
| 子节边界 | 以 R-9 登记的字面量标题起头、独占一个块，且**块末与下一个标题之间恰一个空行**（否则剥离不可复算，见 R-9 的算法） |

## E5 — Document Structure Plan

**定位**：表达类特性线 `plan.md` 内的 `## Document Structure` 章节，四项内容各落一个固定子节。

| 子节 | 字面量 | 行/列结构 | 判据 |
|------|--------|-----------|------|
| 章节树 | [[STR-003]] | 表 4 列：节名 / 父节 / 目的 / 边界 | 父节取顶层标记 `—` 或本表另一行节名；目的与边界非空 |
| 基准读者 | [[STR-004]] | 2 行：`**Readers**:` 与 `**Reading scenario**:` | 读者定义沿用 `shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议 |
| 证据清单 | [[STR-005]] | 表 4 列：断言 / 证据等级 / as-of / source | 三件套成组；语法归门禁 owner § 证据分级与 as-of |
| 事实 owner | [[STR-006]] | 表 3 列：事实 / owner 路径 / 章节锚 | 每条事实恰一个 owner；路径必须存在于仓库 |

**列名解析**：按表头名匹配，MUST NOT 猜列位；列名常量由检查器持有（code-first owner），测试从常量读取、不手抄。

**产出侧**：本实体的骨架由 `templates/plan-template.md` 的 `## Document Structure` 章节提供（四个三级子节 + 三张表的表头列 + 两行读者标记）。该章节对表达类是必要产出，对执行类 MUST NOT 构成必填项——否则执行类会新增必填章节，违反 requirements FR-011。模板是四个子节标题的**产出方**，登记处仍只有 requirements § Shared Strings 一处。

**章节树的语义**：它是 implement 落文的**唯一结构来源**。顶层行 = `父节` 为 `—` 的行。

## E6 — Structure Violation

**定位**：`doc-consistency-check.py --action structure` 的 finding。码集封闭，**四族**（结构语法 / 两向比对 / 证据面 / owner 面）。这些 finding 属「文档结构产物与落文结构」的判定，**不等于**门禁 owner 的 `structure-links-build` 面——后者的判据与基线归 `skills/external/create-docs/scripts/docs-utils.py`，本动作不读也不改。

| 族 | 码 | 触发 | 判据 owner |
|----|----|------|-----------|
| 结构语法 | `document-structure-missing` | 表达类 `plan.md` 无 `## Document Structure` 整章 | requirements FR-013 |
| 结构语法 | `subsection-missing` | 四个子节缺任一；finding 以 `name=` 携带缺失子节的登记字面量（取值域恰为 [[STR-003]]…[[STR-006]]） | requirements FR-013 |
| 结构语法 | `parent-unknown` | `父节` 指向本表不存在的节名 | requirements FR-014 |
| 结构语法 | `chapter-duplicate` | 节名在同一份结构里重复 | 同上 |
| 结构语法 | `chapter-purpose-missing` | `目的` 为空 | 同上 |
| 结构语法 | `chapter-boundary-missing` | `边界` 为空 | 同上 |
| 两向比对 | `chapter-missing` | 落文缺计划中的节 | requirements FR-014 |
| 两向比对 | `chapter-unexpected` | 落文出现计划外的**顶层**章节 | 同上（非顶层不因本条转红） |
| 证据面 | `evidence-unlisted` | 带证据标记的断言在清单里无对应行 | requirements FR-015 |
| 证据面 | `grade-invalid` / `as-of-malformed` / `source-missing` / `grade-asof-unpaired` | 复用既有证据码，不自造同义码 | 门禁 owner § 证据分级与 as-of |
| owner 面 | `owner-duplicate` / `owner-path-missing` / `owner-anchor-missing` | 同一事实两行 owner / 路径不存在 / 锚为空 | requirements FR-016 |

**输入面**：判定对象是 `--spec-dir` 下的 `plan.md`（plan 侧语法）；两向比对另需**落文输入**，载体是既有 `--path`（verify 动作在用的同一 flag、同一解析器，MUST NOT 新增参数）。缺省（不给 `--path`）只做 plan 侧，输出显式标注 `two-way: not-run`，MUST NOT 被读作两向通过；给了 `--path` 才执行两向比对。族内 `chapter-missing` / `chapter-unexpected` 只在给了落文输入时可能产生。

**输出与判定**：`status` ∈ {`ok`, `not-applicable`} + 退出码 0；有 finding 或 `status: fail` → 退出码 1；
输入错误 → 2。主体为执行类/未声明 → `status: not-applicable` 并打印 `class=` / `source=` 与非空伴生量
（被检查文件数），MUST NOT 呈现为「0 违规通过」。重跑同一份 `plan.md` MUST 得同一违规集（顺序稳定）。

## E7 — Operator Result Record

**定位**：一次文档门禁运行里每个 blocking 算子的结果行，写在 `test-evidence/` 的输出文件中；它是 U4 第 (a)/(b)
两项与槽位 `passed`/`failed` 计数的唯一来源。

| 字段 | 取值 | 说明 |
|------|------|------|
| `operator_id` | `G-…` | 取自门禁 owner 的算子表，不在此重列 |
| `face` | 六面 face id 之一，或 CLI 输出面的 face id（`reader` / `evidence` / `duplicate` / `count`） | 两者不是同一集合：六面是判据面（owner 是门禁文档），四面是工具输出面（owner 是 `doc-consistency-check.py` 的 `FACES` 常量）；记录 MUST 写明取的是哪一种（`face_scope=gate|cli`） |
| `verdict` | `pass` \| `fail` \| `not-evaluated` \| `not-applicable` | 封闭四值 |
| `entry` | 命令串或「人工/受委托代理」 | 算子入口 |
| `rc` | 整数或 `null` | 该条命令自身的原始退出码（槽位行的 `rc` 是聚合值，见 E8） |
| `evidence_path` | 仓库相对路径 | 指向该算子的原始输出 |

**字段集止于此**：本实体 MUST NOT 新增 `evidence_sha256` 之类的记账字段。U4 的 (b) 项判据是「证据文件存在且非空」，不做哈希比对——既有 `gate-implement-evidence-binding` 的哈希绑定只约束 `verification.md` 的 SC 样本行，且其 owner 明写非 `pass` 判定不承担绑定义务，给算子记录加哈希会把该规则反转（requirements FR-019(b)）。

**计数规则**（槽位的 `passed`/`failed` 由此导出）：`pass` 计 `passed`；`fail` 与 `not-evaluated` 计 `failed`；**`not-applicable` 单列**——MUST NOT 计入 `passed`、MUST NOT 计入 `failed`（与门禁 owner「站点层不存在时记 `not-applicable`，不得记为通过」一致），其条数从本实体的 `verdict` 列直接数，并由等式「算子总数 − (`passed`+`failed`) = `not-applicable` 条数」约束槽位行；逐面的 `not-evaluated` 原因写进 `evidence_ptr` 指向的门禁输出，MUST NOT 并入 `passed`、MUST NOT 以 0 表示未运行。

## E8 — Docs Gate Slot Row

**定位**：表达类线上替换两槽位测试预算的两个文档门禁槽位行，落在既有状态脊 `test-budget` JSONL 围栏内。

| 字段 | 表达类取值 | 执行类取值（不变） |
|------|-----------|--------------------|
| `seq` | 严格递增 | 同 |
| `slot` | `baseline`（implement 起点）/ `closure`（review 通过后） | 同 |
| `stage` | `implement` / `closure` | 同 |
| `selection_basis` | **`docs-gate-full`** | `full-suite` |
| `command` | 该次文档门禁命令串（一次四面调用 + 结构子步；站点层存在时加构建算子） | `run-tests.sh …` |
| `rc` | **聚合退出码**：该次门禁的命令串逐命令取非零优先（任一命令非零则非零，全为 0 才 0） | 同（单条命令的 rc 即聚合值） |
| `passed` | verdict = **`pass`** 的 blocking 算子数（`not-applicable` 不计入） | 通过用例数 |
| `failed` | verdict ∈ {`fail`, `not-evaluated`} 的算子数 | 失败用例数 |
| `failed_names_path` | 失败算子 id 名单文件 | 失败用例名单 |
| `baseline_compare` | closure：算子 id 集合的名称级差集（`comm -13` 形态） | closure：失败名单名称级差集 |
| `evidence_ptr` | 门禁输出文件 | 测试输出 |

**不变量**：槽位数（2）、时点、槽位顺序、closure 名称级差集形态与 `audit-test-budget.py` 的判定**全部不变**；
未运行时 MUST NOT 写槽位行，MUST NOT 记 0。字段集不新增（见 R-5 的实测：审计对本表的变化零感知）。**`rc` 无单一进程的解法**：不引入聚合脚本（那会扩大接线面，违反 requirements FR-023），而是把 `rc` 定义为「命令串逐命令非零优先」的**聚合值**，并把逐命令原始 rc 留在 `evidence_ptr` 指向的门禁输出里；因此 `passed + failed` 可以小于算子总数，差额必须等于 `not-applicable` 条数（U4 校验该等式）。

## E9 — Dispatch Class Payload

**定位**：每次阶段派发时写进提示词第①段的**四元组**。它是类别的**唯一载体**（环境变量不被远端子代理继承）。

| 键 | 取值 | 缺失后果 |
|----|------|----------|
| `flow_class` | `execution` / `expression` | 派发构造缺陷，U4 不放行 |
| `source` | `declaration` / `default` | 同上 |
| `marker` | 默认标记字面量或空 | 同上（`source: default` 时空值即缺字段） |
| `error` | E3 登记的码（`owner-unavailable` / `declaration-absent` / …）或 `-`（无错误位） | 同上 |

**两个可区分的未声明形态**（本表存在的理由）：`source=default` + `marker=<默认标记>` + `error=-` = 作者没写声明（`declaration-absent` 的冷形态）；`source=default` + `marker` 空 + `error=owner-unavailable` = 机制降级。U4 必须能把二者分开：后者 MUST 走 `owner-unavailable` 分支（记降级观测、保持既有门禁集），MUST NOT 当作「作者未声明」放行，也 MUST NOT 按表达类四项校验（requirements FR-019(c)）。

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
| E1 存量缺省 | 同上（`declaration-absent`） | 退出码 0 + advisory（不计缺陷） |
| E2 记录形态 | 单元测试断言字段集（九项）与互斥约束 | 字段相等 / 不存在 |
| E4 接线形态 | 契约测试（每模板恰一次 lookup、零副本、退出码 1 停止句在场、剥离后与基线字节相同） | 计数 / 字符串 / SHA-256 |
| E5 四子节（plan 侧） | `doc-consistency-check.py --action structure --spec-dir` | 退出码 + findings |
| E5 骨架产出侧 | 模板静态检查（四子节骨架在场、执行类不构成必填） | 字符串 / 计数 |
| E6 码集封闭（四族） | 同上（码常量由检查器持有，测试从常量读） | 集合相等 |
| E6 两向比对输入 | 同上（缺 `--path` → `two-way: not-run`） | 字符串 / 退出码 |
| E7 计数规则 | 槽位行 + U4 校验（含 `not-applicable` 条数等式） | 整数与 verdict 集合 |
| E8 槽位不变量 | `audit-test-budget.py`（不改） | `slots=baseline:N closure:N` |
| E9 载荷在场（四元组） | 驱动技能契约测试 + U4 (c) | 四元组解析 |
