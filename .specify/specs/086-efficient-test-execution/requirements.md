# Requirements Specification: 测试高效执行（默认并发）

**Requirement Branch**: `086-efficient-test-execution`
**Created**: 2026-11-06
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Input**: User description: "spec-kit 测试套件串行执行太慢，要让测试并发执行；只有覆盖不够，测试还必须能高效执行——任何构建测试框架/用例的项目都要考虑这一点；把该原则固化进 constitution 与 instructions（template + live）随框架分发。本次运行用 sdd-loop-driver 无人值守走 SDD，保留并使用 085 的临时 Goal/Team 与多 agent 并发机制，作为它们的真实场景 dogfood。"

## Related Feature *(mandatory)*

**Feature ID**: Need clarification
**Feature Name**: Need clarification

## Overview

本特性有两条彼此独立、都必须成立的交付线，加一条贯穿两者的保留义务：

1. **本仓自己的测试套件必须默认并发执行**。当前 canonical 运行器以单进程串行跑完整套件；改造后有可用并行引擎时默认并行，无可用引擎或显式要求时回退到串行，两条路径都必须是完整可跑的一次运行，且失败按**名称**可比。
2. **「测试不仅要覆盖，还必须能高效执行」必须成为框架原则**，随 constitution 与 instructions 一起分发给下游项目，并有一份 owner 文档区分进程级并行与异步并发两个分支。
3. **保留义务**：085 的临时 Goal/Team、阶段专用 agent、默认 24 并发、worktree + 集成队列与 checkpoints 不得被本特性删除、禁用或重写；本特性自身这次运行就是它们的真实场景 dogfood，为 085 SC-010 提供证据。

本特性不是"把测试改快一点的若干局部技巧"，而是一次**执行模型升级 + 原则固化**：串行默认改为并行默认（保留串行逃生口），并把这条执行模型写进随框架出厂的原则层。

## Context and Current State *(measured, not asserted)*

以下事实来自本特性 U0/U1 的实测与仓库现状，是后续 FR/SC 的前提；任何运行时重测值取代此处数值时，以重测记录为准。

| 事实 | 值 | 来源 |
|---|---|---|
| 异步测试函数数量 | 0 | `grep` 全 `tests/`；本套件不存在 async 可并行的对象 |
| 使用 `subprocess` 的测试文件数 | 167 | 同上 |
| 完整套件串行（post-pull） | 7475 passed / **19 failed** / 7 skipped，**1031.48 s** | `run-tests.sh --names-out … -q` |
| 完整套件并行（post-pull，`-n auto`） | 7474 passed / **20 failed** / 7 skipped，**201.87 s** | 同一 runner、同一 `--names-out` 口径；加速比 ≈ **5.1×** |
| 并行相对串行的唯一新增失败名 | `tests/contract/test_sdd_loop_driver_skill.py::test_c22_watch_target_hook_selftest` | `comm -13` 差集；该自测在并行负载下超过 60 s 超时，串行约 28 s |
| 并行相对串行的修复项 | 无 | `comm -23` 差集为空 |
| 上游 `run-tests.sh` / `pyproject.toml` | 无 xdist，无 dev 依赖组 | 文件内容 |
| 已登记但未采用的提速建议 | xdist / `-n auto` / slow marker / 会话缓存 / 去 sleep / 进程内直调 | `.specify/memory/todo/20261030-suite-speed-optimizations.md`（parked） |
| 067 RC-03 | 串行是默认且始终可跑路径；xdist 准入但未采用 | `.specify/specs/067-loop-efficiency-hardening/contracts/runner-contract.md` |
| 运行时 Python 下限 | `>=3.8`（`pyproject.toml`） | 下游项目可能只有 3.8 解释器 |

**并行安全的真实差距是一处，不是一套**：本次实测的失败名差集只有 watch-target 自测一项。requirements 因此把"并行安全"写成**开放清单 + 判据**（见 FR-010 与 `## Assumptions` A6），而不是预先罗列一串假设会坏的测试；实现必须用实测差集决定修哪些，最终 closure 差集必须为空。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 开发者以默认并发运行 canonical 套件，得到与串行同名的失败 (Priority: P1)

一位开发者在干净检出上跑一条命令（canonical runner，无额外参数）。套件并行执行；结束时通过/失败/跳过计数与失败**名称清单**可与串行运行逐项比对；失败名集合与同一树上串行运行一致（既存失败按名称排除），墙钟时间显著下降。

**Why this priority**: 这是用户的第一条诉求，也是本特性唯一直接改变日常开发体验的交付；没有它，后面所有原则都是纸面文字。

**Independent Test**: 在同一棵树、同一 selection、同一 `--names-out` 口径下分别跑一次串行与一次默认（并行）运行，用 `comm` 比对两份失败名清单；断言差集为空（仅既存失败）且并行墙钟显著低于串行。只做这一条，开发者已经获得一个更快且可信的默认运行器。

**Acceptance Scenarios**:

1. **Given** 装了并行引擎的环境与一棵未改动的树，**When** 开发者运行 canonical runner 且不传任何并行参数，**Then** 套件以多个工作进程并行执行，且运行结束时打印的失败名清单与串行运行的名清单相同。
2. **Given** 同一棵树，**When** 先跑串行、再跑默认并发，**Then** 并行墙钟相对串行有可测量且被记录的下降，且该下降来自同一 selection（不是缩小了测试集）。
3. **Given** 一份既存失败名基线，**When** 并行运行结束，**Then** 相对基线的新增失败名为零；任何新增失败名都被逐个归因，而不是被计数相等掩盖。
4. **Given** 并行运行完成，**When** 开发者检查工作树，**Then** 除运行前已存在的改动外没有新增污染（无镜像漂移、无生成物残留、无临时工作树）。

---

### User Story 2 - 下游项目收到「测试必须高效执行」的原则 (Priority: P1)

下游项目的维护者用 CLI 初始化一个新项目，拿到出厂 constitution 与 instructions。两者都包含一条原则：测试覆盖只是必要条件，测试的执行效率是同一层级的质量属性；被覆盖的测试若慢到没人跑，等于没有覆盖。原则附有 owner 指南，说明什么情形走进程级并行、什么情形走异步并发、什么情形两者都不是，以及如何测量"高效"。

**Why this priority**: 用户明确要求"任何构建测试框架/用例的项目都要考虑这一点"，且要求写进随框架分发的那一层。只改本仓运行器不满足这条诉求——下游拿不到。

**Independent Test**: 在临时目录用 CLI 初始化一个新项目，在生成的 constitution 与 instructions 中检出该原则及其指向 owner 指南的指针；改动 owner 指南中的一条判据后，检查原则文本不发生重复定义（只有指针）。只做这一条，下游项目已经获得该原则；它与 US1 的实现相互独立。

**Acceptance Scenarios**:

1. **Given** 出厂 constitution 模板与 live constitution，**When** 读取原则清单，**Then** 两者都包含该原则（编号各自独立），条款含"覆盖必要但不充分"与"效率是质量属性"两条可判定表述。
2. **Given** 出厂 instructions 模板与 live instructions，**When** 读取章节结构，**Then** 两者都有该原则的常驻章节（摘要 + 指向 owner 指南的路径），且该章节逐字不含 owner 指南的二级标题。
3. **Given** 下游项目既有 constitution 已有自己的测试原则，**When** 该原则与既有测试原则同时存在，**Then** 两者的分工是明确可判的（一个谈测试**做什么**，一个谈测试**以什么代价执行**），不产生相互矛盾的指令。
4. **Given** owner 指南被修改（例如某个判据取值变更），**When** 检查 constitution、instructions、changelog 与文档站，**Then** 这些位置无需随之改动即可保持一致（它们只持有指针）。

---

### User Story 3 - 运行器保留串行逃生口、缺失依赖时的安全回退与嵌套保护 (Priority: P1)

有开发者必须复现一个时序问题、有下游项目的解释器版本拿不到并行引擎、也有脚本会在一个已经并行的运行里再次调用运行器。这三种情形都必须得到确定的行为，而不是"并行是默认所以自己想办法"。

**Why this priority**: 并行默认若没有这三条出口，会制造三类静默故障：无法复现、无法安装、进程爆炸。067 的 RC-03 已经把"串行必须是完整可跑路径"钉成契约，本特性不能因为采用并行而违反它。

**Independent Test**: 逐个场景跑一次：`--serial` 完整跑、在没有并行引擎的解释器上完整跑、在已由并行引擎派生的进程里再调运行器。断言三者都完成且不重复创建进程池，失败名捕获在三者中都有效。

**Acceptance Scenarios**:

1. **Given** 默认已并行，**When** 开发者传显式串行开关，**Then** 套件以单进程完整运行，失败名清单照常写出，退出码语义不变。
2. **Given** 环境里没有并行引擎（例如 Python 3.8 下游），**When** 运行 canonical runner 不带参数，**Then** 套件以串行完整跑完（不报错、不空跑），并在 stderr 输出一条具名的回退说明，说明它为什么串行。
3. **Given** 进程已经处在一个并行工作进程内，**When** 该进程再次调用 canonical runner，**Then** 内层运行不再派生第二个工作进程池，且内层运行的失败名清单仍然有效。
4. **Given** 调用者自己已经传了并行参数，**When** 运行器再处理默认值，**Then** 命令里不会出现重复的进程数开关。
5. **Given** 任何一次运行，**When** 检查 stderr，**Then** 头部行仍然如实描述真实执行的命令（不含未实际生效的参数）。

---

### User Story 4 - 085 的临时 Goal/Team 与并发机制被保留，并由本次运行实测 (Priority: P1)

本次 086 运行本身就是一个真实 SDD 运行。它必须经临时 Goal、临时 Team、阶段专用 agent、多 agent 并发、写入隔离与阶段 checkpoint 走完，留下可核查证据；085 的这些机制、契约与历史记录不得被本特性删除、禁用、绕过或重写。

**Why this priority**: 这是用户明确追加的指令，也是 085 SC-010 至今为 `partial` 的唯一缺口（缺一次带 LLM 阶段 agent 的完整驱动运行）。若本特性顺手重写或绕过这些机制，缺口会被"做绿"而不是被补上。

**Independent Test**: 检查本特性 spec 目录下的 goal/team/checkpoints 与运行证据：临时 Goal 与 Team 存在且绑定关系可解析、至少一个阶段实际并发派发多于一个 agent、每阶段 checkpoint 存在、085 的契约与集成测试在改动后仍全绿。只做这一条，085 SC-010 的缺口得到真实证据。

**Acceptance Scenarios**:

1. **Given** 本次 086 运行，**When** 检查 spec 目录，**Then** `goal/` 与 `team/` 按 085 的时机与 schema 落地，临时 Team 绑定到临时 Goal，且全局 `.specify/goal/**` 与 `.specify/teams/**` 未被写入。
2. **Given** 一次阶段派发，**When** 检查运行证据，**Then** 该阶段记录了 requested/effective 并发与具名理由，且至少一个阶段实际并发派发数大于一。
3. **Given** 本特性全部改动，**When** 跑 085 的契约与集成测试，**Then** 无新增失败；085 的 goal/team/checkpoints/contracts 与历史记录字节未变。
4. **Given** 本次运行结束，**When** 评估 085 SC-010，**Then** 只有在证据完整（全阶段链 + LLM 阶段 agent + 并发 + checkpoints）时才记 `pass`，否则保持 `partial` 并写明缺口。

---

### User Story 5 - 预算台账不因并行参数而丢账 (Priority: P2)

驱动用它自己的预算台账判断一个阶段是否真的跑了测试、跑了哪一档。若台账解析器不认识并行参数，一次"显式并行的全量运行"会被判成非全量或被丢弃，台账就会静默少记一次真实运行。

**Why this priority**: 它不改变开发者体验，却决定后续所有基于台账的效率判断是否可信——一个会漏账的传感器比没有传感器更糟。

**Independent Test**: 给台账解析器喂一条带并行参数的全量运行命令，断言它被识别为全量运行而不是被丢弃；再喂一条带取值的被误认参数，断言取值不会被当成路径。

**Acceptance Scenarios**:

1. **Given** 一条带进程数开关的全量测试命令，**When** 台账解析器分类，**Then** 它被记为全量运行，不被判为非全量或被丢弃。
2. **Given** 一条带分布式策略开关的命令，**When** 解析器跳参数，**Then** 该开关的取值不被当作位置参数路径。
3. **Given** 既有台账行，**When** 解析器升级后重放，**Then** 既有行的分类结果不变。

---

### Edge Cases

- **watch-target 自测在并行负载下超时**：本次实测的唯一新增失败。要求是"具名的显式串行例外或超时修复"二选一，二者都必须可复核；**不得**用 skip/xfail 掩盖，也不得靠"跑两次碰运气"。
- **既存失败本身是时序敏感的**：并行可能让某个既存失败在某些运行中变绿或变红。差集比较必须同时报告"新增"与"消失"两侧，消失项不得被宣称成本特性的修复。
- **`--names-out` 在并行下写出空清单**：当并行运行整体崩在启动阶段时，空清单与"没有任何失败"不可区分。必须让"空且可疑"与"确实零失败"可区分。
- **调用者已在自己的命令里传了进程数**：既不能重复注入，也不能忽略调用者意图。
- **工作进程数与测试数严重不匹配**（例如 1 个测试、很多工作进程）：不得因此报错或空跑。
- **运行器在只读/受限环境下无法写临时目录**：并行引擎的临时协调需要可写位置，失败必须具名，不得静默串行兜底后仍宣称并行。
- **一次运行里既改了 conftest 又并行**：并行工作进程之间共享的文件系统副作用（同一路径写同一文件）必须被识别为并行安全缺陷，而不是靠"重跑通过"了事。
- **原则落地到既有下游项目**：这些项目的 constitution 已有测试相关原则，新增原则必须与之可共存、可判定分工，不得形成互相矛盾的指令。

## Requirements *(mandatory)*

### Functional Requirements

#### A. 运行器执行模型（US1, US3）

- **FR-001**: canonical 运行器 MUST 在并行引擎可用且调用者未显式要求串行时**默认并行**执行完整 selection。默认行为的变化 MUST 记录在运行器自身的注释与开发文档中，并保留一次"为什么并行是默认"的依据指针。
- **FR-002**: 运行器 MUST 提供**显式串行开关**（[[STR-007]]）。带该开关的运行 MUST 是一次完整、可跑的运行，其 selection 与默认运行相同；它 MUST NOT 被当作"降级"或被标注为不完整。
- **FR-003**: 运行器 MUST 提供进程数控制：显式参数（`--workers N|auto`）优先于环境变量（[[STR-006]]），二者都缺省时取自动值。解析失败（非数字、负数、零）MUST 以具名错误退出，MUST NOT 静默回退到 1。
- **FR-004**: 当调用者已经在自己传入的参数里给了进程数开关时，运行器 MUST NOT 再追加一个，避免同一开关出现两次导致的未定义行为。
- **FR-005**: 当进程环境已表明自己处在一个并行工作进程内（由并行引擎派生的环境标识）时，运行器 MUST 自动走串行，MUST NOT 派生第二个工作进程池；该自动串行 MUST 与 FR-002 的显式串行同样是一次完整运行。
- **FR-006**: 当并行引擎不可用时（例如下游 Python 3.8 解释器），运行器 MUST 回退到串行并完整跑完，MUST 在 stderr 输出一条**具名回退说明**（说明缺什么、因此串行），且退出码语义不变。MUST NOT 报错退出，MUST NOT 空跑。
- **FR-007**: 运行器 MUST 保留既有契约面：`--names-out` 的语义（排序后的 FAILED 名清单、一行一个 id、正常运行的附加产物、失败退出码等于测试框架自身结果）、stderr 头部行、退出码、以及"注释行不参与差集"的 `comm -13` 口径。
- **FR-008**: `--names-out` MUST 在并行运行下同样正确写出；当一次运行**没有任何失败**（清单为空）时，运行器 MUST 让"确实零失败"与"清单没有写成功"可区分（例如在 stderr 记录清单条目数与来源），使空清单不被误读。[[STR-002]]
- **FR-009**: 运行器的两份载体（框架源与项目运行时镜像，[[STR-004]]）MUST 逐字节一致，且 MUST 有契约测试守住这一对等关系；实现 MUST NOT 只改一侧。

#### B. 并行安全（US1）

- **FR-010**: 默认并行运行相对同一棵树串行运行的失败名差集 MUST 为空（既存失败按名称排除）。任何非空差集 MUST 被逐项处置为以下三者之一：(a) 修掉并行不安全的根因；(b) 为该测试声明**具名显式串行例外**并说明理由；(c) 记为既存失败（其名称同时出现在串行基线与并行结果中）。MUST NOT 使用 skip / xfail / 重跑碰运气 / 缩小 selection 中的任何一种来消除差集。
- **FR-011**: 每一项被声明的串行例外 MUST 是可复核的具名标记（能按名称列出全部例外），MUST NOT 是一个"静默关掉并行"的全局开关；例外集合的大小 MUST 在证据中如实记录。
- **FR-012**: 本次实测确认的唯一并行不安全项（watch-target 自测在并行负载下超过其 60 s 超时）MUST 按 FR-010 的 (a) 或 (b) 处置；若取 (b)，该例外 MUST 只覆盖该测试，不影响其余测试的并行。
- **FR-013**: 任何测试若因其自身与被测对象共享可变状态而在并行下不稳定，MUST 通过修根因（隔离临时目录、幂等写、独立仓库根）解决；MUST NOT 通过"让它只在特定工作进程上跑"来规避。
- **FR-014**: 并行安全性的判定 MUST 由**名称差集实测**给出，而不是由阅读代码推断；差集两侧（新增与消失）MUST 一并记录。

#### C. 依赖与运行时边界（US1, US3）

- **FR-015**: 并行引擎（[[STR-005]]）MUST 作为**仅开发侧**依赖引入；CLI 包的运行时依赖集合 MUST 保持不变。Python 3.8 下游拿不到并行引擎属正常路径，由 FR-006 承接。
- **FR-016**: 新增依赖（[[STR-005]]）MUST 遵守既有的版本标记约定（按解释器版本划定可用范围），且 MUST NOT 引入网络服务、常驻进程或新的外部系统依赖。
- **FR-017**: 本特性 MUST NOT 新增任何 `/speckit.*` 命令、技能入口模板或运行时服务。

#### D. 原则固化与分发（US2）

- **FR-018**: 框架 MUST 新增一份 **owner 指南**（[[STR-003]]；文件名为 [[STR-001]]），单一持有该原则的完整定义：为什么覆盖不充分、效率的判据、进程级并行 vs 异步并发的选择规则、何时两者都不适用、如何在真实套件上测量、以及不可用的反模式（用缩小 selection 或跳过换取"更快"）。
- **FR-019**: constitution 的**出厂模板与 live 文件** MUST 各新增一条原则条目，且该条目 MUST 以指针方式引用 [[STR-003]]：(a) 覆盖是必要条件而非充分条件；(b) 测试执行效率是与覆盖同层级的质量属性；(c) 该原则适用于任何构建测试框架或测试用例的项目，而不只是本项目。编号由各自名册自行决定（模板与 live 编号不要求相同），条款 MUST 以指针方式引用 owner 指南，MUST NOT 复述其判据表。
- **FR-020**: instructions 的**出厂模板与 live 文件** MUST 各新增一个常驻章节（摘要 + 指向 [[STR-003]] 的路径），且 MUST NOT 内联 owner 指南的二级标题。
- **FR-021**: 生成 constitution 的 MUST-include 候选清单 MUST 增加该原则的条目，使下游项目由生成器而非由本项目人工投递获得该原则。
- **FR-022**: 本特性 MUST 在同一变更中更新所有因新增原则而变化的计数守卫与预算守卫（原则数、常驻章节数、指令字节预算、MUST-include 条目数），而不是让守卫先红后补。
- **FR-023**: 该原则 MUST 与既有测试相关原则形成可判定的分工（一个规定测试**做什么与何时写**，一个规定测试**以什么代价执行**），MUST NOT 产生互相矛盾的指令。

#### E. 预算台账与效率测量（US5）

- **FR-024**: 驱动的预算台账解析器 MUST 认识并行相关参数（进程数开关及其长形式、分布式策略开关、最大进程数开关），使**显式并行的全量运行**被正确分类为全量运行，MUST NOT 被丢弃或降级。
- **FR-025**: 台账解析器 MUST 把这些开关当作**带取值**的参数处理，其取值 MUST NOT 被当作位置参数（路径）参与分类。
- **FR-026**: 台账解析器的升级 MUST 保持既有记录的解析结果不变（回归等价性）。

#### F. 085 机制保留与实测（US4）

- **FR-027**: 本特性 MUST NOT 删除、禁用、绕过或重写 085 的临时 Goal/Team 机制、阶段专用 agent 角色、默认并发度、worktree 写入隔离、集成队列、checkpoint 协议、契约文件与历史记录。所有改动对 085 面 MUST 是 additive。
- **FR-028**: 本特性自身的这次运行 MUST 走完整 SDD 阶段链，并留下：临时 Goal 与临时 Team（绑定可解析）、各阶段 checkpoint、requested/effective 并发与具名理由、以及至少一个阶段实际并发派发多于一个 agent 的证据。
- **FR-029**: 本特性落地后 MUST 重跑 085 的契约与集成测试并记录结果；零新增失败是保留义务的判定依据。
- **FR-030**: 085 SC-010 的验收状态 MUST 依据本特性取得的实际证据更新：证据完整才记 `pass`，否则保持 `partial` 并写明仍缺什么。MUST NOT 以"本特性已跑过一次"为由默认判 pass。

#### G. 记录与文档（US1, US2）

- **FR-031**: 本特性 MUST 在特性索引与特性详情中登记（新增一行 + 详情文件），并在 `CHANGELOG.md` 记录本次变更。
- **FR-032**: 开发文档中关于"如何跑套件"的说明 MUST 与新的默认行为一致（默认并行、如何串行、如何指定进程数、缺引擎时会发生什么），且 MUST NOT 给出与新运行器矛盾的命令。
- **FR-033**: 效率结论 MUST 以**同口径实测**支撑：串行与并行的命令、selection 依据、墙钟、失败名清单与差集 MUST 落在本特性的证据目录中；计数相等 MUST NOT 被当作成员相同。

### Key Entities

- **Canonical Runner（canonical 运行器）**: 项目唯一的规范测试入口脚本；解析解释器、处理 `--names-out`、执行 selection。本特性改变的是它的**执行模型**（串行默认 → 并行默认 + 串行出口），不是它的 selection 语义。
- **Parallel Engine（并行引擎）**: 按进程分发测试的测试框架插件；缺省时可缺席，缺席是正常路径。
- **Serial Escape Hatch（串行逃生口）**: 显式开关 + 嵌套自动串行 + 缺引擎自动回退三者共同构成的"始终可完整跑完"路径。
- **Failure-Name Set（失败名清单）**: 一次运行的失败测试 id 集合，是"是否引入回归"的唯一比较口径。
- **Serial Exception（串行例外）**: 一项被具名声明、可枚举、可复核的"该测试不参与并行"的标记。
- **Test Execution Efficiency（测试执行效率原则）**: "覆盖必要但不充分 + 效率是同层级质量属性"的原则条目，owner 是新增指南文档，constitution 与 instructions 只持指针。
- **Budget Ledger（预算台账）**: 驱动记录每次测试运行档位的记录；本特性使其认识并行参数。
- **Baseline / Closure Slot（基线/收口槽位）**: 一次运行线上恰好两次全量运行的记录位置，名称级比较在两者之间进行。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 同一棵树上，默认并发运行的失败名集合与串行运行的失败名集合差集为空（既存失败按名称排除，新增项计数为 0），且并行墙钟相对串行有被记录的下降。**Path**: final
- **SC-002**: 出厂 constitution 模板与 live constitution 各含该原则条目；出厂 instructions 模板与 live instructions 各含其常驻章节（指向 [[STR-003]]）；一处都不缺。**Path**: final
- **SC-003**: 在临时目录用 CLI 初始化的新项目里，生成的 constitution 与 instructions 中都能检出该原则、其 owner 指南指针（[[STR-003]]）与文件名（[[STR-001]]），读者不需要读本仓即可理解原则适用范围。**Path**: final
- **SC-004**: 串行逃生口三种情形（显式开关 [[STR-007]]、缺引擎回退、嵌套调用）各自完成一次完整运行且失败名清单有效；从命令与 stderr 可判定实际走了哪条路径。**Path**: final
- **SC-005**: 显式并行的全量运行被预算台账分类为全量运行（不是被丢弃、不是被降级），且既有记录的解析结果不变。**Path**: final
- **SC-006**: successor 的全量收口运行相对同口径串行基线的失败名差集为空；差集的"新增"与"消失"两侧都被记录。**Path**: final
- **SC-007**: 085 的临时 Goal/Team、阶段 agent、并发、worktree 隔离、集成队列与 checkpoint 机制全部保留，085 的契约与集成测试零新增失败。**Path**: final
- **SC-008**: 本特性这次运行留下完整 dogfood 证据：临时 Goal/Team 存在且绑定可解析、每阶段 checkpoint 存在、requested/effective 并发与具名理由、至少一个阶段实际并发数 > 1。**Path**: final
- **SC-009**: 运行器两份载体（[[STR-004]]）字节一致，镜像检查与命令副本检查通过；新增原则引起的计数守卫与预算守卫在同一变更中通过。**Path**: supporting
- **SC-010**: CLI 包运行时依赖集合相对改动前为空差集；新增依赖（[[STR-005]]）仅落在开发侧。**Path**: supporting
- **SC-011**: 一次完整默认并发运行结束后，工作树除运行前已存在的改动外无新增污染。**Path**: supporting
- **SC-012**: 085 SC-010 的验收状态依据证据更新为 `pass` 或保持 `partial` 并具名缺口，不存在"无证据的 pass"。**Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**: 同一棵树、同一 selection、同一 `--names-out` 口径下的两次运行（串行 / 默认并发）；墙钟取自两次运行的框架摘要行，失败名清单取自 `--names-out` 文件，差集用 `comm -13` / `comm -23` 双向计算；两者命令、退出码、清单与差集落在 `.specify/specs/086-efficient-test-execution/test-evidence/`。
- **SC-002 Source**: 对出厂模板与 live 文件的确定性检索（原则名册、常驻章节计数）与既有计数守卫测试的实际运行结果。
- **SC-003 Source**: 在临时目录执行 CLI 初始化后，在生成的 `.specify/memory/constitution.md` 与 `.specify/instructions.md` 中检索原则标题与 owner 指南路径；记录命令、退出码与命中行。
- **SC-004 Source**: 三次实跑的命令、退出码、stderr 头部与回退说明行、`--names-out` 条目数；嵌套场景另记"未派生第二个进程池"的判据（例如工作进程环境标识未被子运行继承或子运行显式串行）。
- **SC-005 Source**: 台账解析器对构造命令与既有记录的运行结果（分类值 + 退出码），保存输入命令与判定输出。
- **SC-006 Source**: 收口槽位的全量运行记录与同口径串行基线记录；两侧失败名清单与双向差集。
- **SC-007 Source**: 085 契约与集成测试的实际运行输出；085 目录下 goal/team/checkpoints/contracts 与历史文件的改动面清单（应为空）。
- **SC-008 Source**: 本特性 spec 目录下的 `goal/`、`checkpoints/`、状态脊字段与阶段派发证据；并发数取自实际派发记录而非声明值。
- **SC-009 Source**: 镜像检查命令与命令副本检查命令的退出码与输出；计数/预算守卫测试的运行结果。
- **SC-010 Source**: `pyproject.toml` 改动前后的运行时依赖集合差集。
- **SC-011 Source**: 完整运行前后的工作树状态快照对比；只把运行前已存在的改动视为允许残留。
- **SC-012 Source**: 085 验证记录中的 SC-010 行与其证据指针；证据完整性按 SC-008 的取得结果判定。

## Boundary and Ownership (non-duplication)

| Concern | Existing owner | This feature's relationship |
|---|---|---|
| 运行器契约（RC-01…RC-08，串行默认/始终可跑） | `.specify/specs/067-loop-efficiency-hardening/contracts/runner-contract.md` | 067 的结论不改写；本特性在其授权的"后续记录的范围决策"位置上记录**采用并行的决策**，并保留"同一命令去掉并行参数仍是完整可跑运行" |
| 两槽位测试预算、台账字段、定向选择程序 | `skills/external/sdd-loop-driver/references/efficiency-model.md` + `contracts/test-budget.md` | 只扩展台账解析器对并行参数的识别；不动槽位语义与 selection 算法 |
| 测试执行效率原则的定义 | **新增** owner 指南 `shared/guidelines/test-execution-efficiency.md`（本特性创建） | 本特性创建并单一持有；constitution/instructions/CHANGELOG/文档站只持指针 |
| 宪法原则名册与计数 | `.specify/memory/constitution.md` 与 `templates/constitution-template.md` | 各加一条并各自编号；计数守卫在同一变更更新 |
| 指令常驻章节与字节预算 | `templates/instructions-template.md` 与 `.specify/instructions.md` | 各加一个章节；预算与计数更新 |
| MUST-include 候选清单 | `skills/internal/manage-constitution/SKILL.md` | 增加一条 |
| 临时 Goal/Team、阶段 agent、并发、checkpoint | `.specify/specs/085-sdd-temporary-goal-team/{requirements.md,plan.md,contracts/}` | 只使用与保留；不修改、不删除、不重写 |
| 测试并行安全的具体修法 | 各测试文件自身 | 本特性只在差集证明有需要时修改，且不改变其断言所证明的命题 |
| 历史记录 | `.specify/state/`、`.specify/memory/evidence/`、已日期化的 review/feedback 条目、085 全部记录 | 只读；不改写 |

## Runtime Stack & Dependency Ownership

本特性交付的运行时能力是"运行器执行模型 + 并行引擎（仅开发侧）+ 台账解析器识别"。其余项由外部供给、本仓只消费，按 `signed-contract` 记。该表是 SC-001、SC-004、SC-005、SC-006 的运行时前提。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | Python 解释器（运行运行器、测试与确定性检查） | signed-contract | CPython 上游（本仓只消费） | `requires-python >= "3.8"`（`pyproject.toml` 已声明，不改变下限） | `pyproject.toml` | 新增脚本 stdlib-only；新增测试在 `>=3.8` 上通过；并行引擎的缺席路径由 FR-006 覆盖 | FR-015, FR-016 | EP-001 |
| RS-002 | 测试框架（守卫测试运行器）与并行引擎（[[STR-005]]；开发侧依赖） | signed-contract | pytest / pytest-xdist 上游（本仓只消费） | 无声明 pin；执行时以 `pytest --version` 等原文记录进 `test-evidence/` | `pyproject.toml` | 并行运行与串行运行在同一版本组合下得到 SC-001 的空差集 | FR-001, FR-015 | EP-001 |
| RS-003 | canonical 运行器与其项目运行时镜像 | in-scope | 本仓 `scripts/bash/run-tests.sh` | 同一提交 | `tests/contract/` 中的运行器契约测试 | SC-004, SC-009 | FR-001–FR-009 | EP-001 |
| RS-004 | 预算台账解析器 | in-scope | 本仓 `skills/external/sdd-loop-driver/scripts/audit-test-budget.py` | 同一提交 | 同目录单元测试 | SC-005 | FR-024–FR-026 | EP-001 |
| RS-005 | 宿主操作系统与文件系统（并行工作进程的临时目录、进程派生） | signed-contract | 宿主环境（本仓只消费） | 无声明 pin；执行时记录宿主平台与核数 | `.specify/specs/086-efficient-test-execution/requirements.md` | SC-001, SC-004, SC-011 | FR-005, FR-013 | EP-002 |

## Assumptions

- **A1（类别判定理由）**：判为 `execution` 的依据是验收 oracle——交付物（运行器、原则文件、台账解析器）在验收时被机器执行或解析（跑测试、跑检查器、检索计数），缺陷只在程序行为或机器可检索的结构上暴露；不以"仓库里有文档"作为 `expression` 的理由。文档类产物（原则指南、CHANGELOG）在此只承担分发与解释，判定 oracle 仍是机器执行。
- **A2（技术方向）**：异步不是本套件的并发机制。实测 0 个 async 测试函数、167 个测试文件使用子进程；本套件是进程/子进程与 CPU/IO 混合负载，适用**进程级并行**。原则层面仍须写出 async 分支，因为下游项目的 I/O 密集测试适用它。
- **A3（失败比较口径）**：既存失败按**名称**比较，不按计数比较。计数相等可能掩盖成员变化（仓库既有教训），因此"零新增失败"一律以名称差集表述。消失的失败不追认为本特性的修复。
- **A4（并行默认的边界）**：默认并行只在并行引擎可用且调用者未要求串行时生效；"同一命令去掉并行参数仍是完整可跑运行"是硬约束（067 RC-03 的授权形式），降级串行运行不得作为预算证据。
- **A5（依赖边界）**：并行引擎是仅开发侧依赖；CLI 运行时依赖集合不变；不新增运行时服务、网络调用或新命令。
- **A6（并行安全的开放清单）**：本次实测的差集只暴露**一项**并行不安全测试（watch-target 自测超时）。requirements 因此把并行安全写成"判据 + 实测差集"（FR-010/FR-014），而不是预先假设一串会坏的测试清单。U0 记录中提到的镜像探针、幂等写、嵌套运行器等项，只有在并行差集或实际运行中证明有问题时才成为 MUST 修复项；证明无问题的，不修。
- **A7（串行例外的形态）**：任何串行例外必须具名、可枚举、可复核，绝不以 skip/xfail 或"静默关掉并行"实现。例外的理由必须是并行特有的（负载、共享状态、超时），不是"它偶尔红"。
- **A8（原则的落地形态）**：原则以"owner 指南 + constitution 条目 + instructions 常驻章节 + MUST-include 条目"四件套落地；四处都是指针形态，事实只有一份。
- **A9（基线时点）**：U0 记录的串行/并行对照是方向性与差距证据；收口槽位的比较基线取实现起点那一刻的 SDD 基线槽位失败名，而不是 U0 的名单（两次之间可能已有变化）。
- **A10（085 保留的读法）**：保留义务是"不改 085 面"，不是"不用 085 面"。本特性运行必须**使用**这些机制（否则 085 SC-010 无证据），但不得修改其定义、契约、checkpoint 记录或历史。
- **A11（自应用例外）**：本仓开发自身的运行按完整链执行（含 checklist / analyze / review），不因并行默认而跳过质量阶段。
- **A12（不改写历史）**：`.specify/state/`、`.specify/memory/evidence/`、已日期化的 review/feedback 条目与 085 全部记录都是只读输入；只更新存活引用与存活定义。

## Out of Scope

- 引入异步测试执行框架，或把现有同步测试改写为 async。
- 缩小测试 selection（`-m` / `-k` 过滤层、去掉整层测试、默认跳过慢测试）以换取更快的数字。
- 把并行失败改写成 skip / xfail / "已知不稳定"清单来处理。
- 改变测试框架的收集范围、退出码语义，或改变失败名清单的格式。
- 为保证并行而重构被测业务代码（运行器与测试侧改动即可达成目标）。
- 引入新的调度服务、常驻进程、缓存服务或遥测端点。
- 修改 067 的 RC 结论本身（本特性只在其授权位置记录自己的采用决策）。
- 修改、删除或重写 085 的 goal/team/checkpoints/contracts 与任何日期化历史记录。
- 在本特性内实现 parked TODO 中的其余提速项（slow marker、会话缓存、去 sleep、进程内直调）。
- 推广或改写其他项目的测试原则；本特性只交付一条原则与其 owner。

## Shared Strings

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `"test-execution-efficiency.md"` | FR-018, SC-003, owner 指南文件名 |
| `STR-002` | `"# failed-name list written"` | FR-008, 运行器 stderr 清单写出行前缀 |
| `STR-003` | `"shared/guidelines/test-execution-efficiency.md"` | FR-018, FR-019, FR-020, SC-002, SC-003, 指针形态的唯一路径 |
| `STR-004` | `"scripts/bash/run-tests.sh"` | FR-009, SC-009, 运行器载体路径 |
| `STR-005` | `"pytest-xdist"` | FR-015, FR-016, SC-010, 开发侧依赖名 |
| `STR-006` | `"SPECKIT_TEST_WORKERS"` | FR-003, 进程数环境变量名 |
| `STR-007` | `"--serial"` | FR-002, SC-004, 显式串行开关 |

**Citation convention**: 本规格内的引用一律写作 `[[STR-NNN]]`（见 FR/SC 行内引用），下游契约与任务 MUST 沿用同一记号而不是复制字面量。

## Clarifications

### Session 2026-11-06

- Q: 并发用什么机制——异步还是进程级并行？ → A: 进程级并行。实测 0 个 async 测试函数、167 个测试文件使用子进程；本套件的瓶颈是进程/子进程与 CPU 负载，不是等待。async 仍是原则里必须写出的另一分支，因为下游项目的 I/O 密集测试适用它（对应 A2、FR-018）。
- Q: 并行是默认还是可选？ → A: 默认并行，但串行必须是完整可跑的逃生口。067 RC-03 已授权"后续记录的范围决策可以采纳并行参数，条件是同一命令去掉并行参数仍是完整可跑运行"；本规格在此记录该采用决策（A4、FR-001、FR-002）。
- Q: 并行引入的新失败怎么处理？ → A: 本次实测差集只有一项（watch-target 自测在并行负载下超 60 s）。可以修根因，也可以为它声明具名串行例外；不得 skip/xfail，不得靠重跑（FR-010、FR-011、FR-012、A7）。
- Q: 原则写到哪里，下游怎么拿到？ → A: 四件套——owner 指南 + constitution（模板与 live 各一条，编号各自独立）+ instructions（模板与 live 各一个常驻章节）+ 生成器的 MUST-include 条目；四处都是指针（FR-018–FR-022、A8）。
- Q: 085 的机制要保留到什么程度？ → A: 不改动 085 面（goal/team/checkpoints/contracts/历史），但必须**使用**它们跑完本次运行以补齐 085 SC-010 的证据；证据不完整则保持 `partial`（FR-027–FR-030、A10）。
- Q: 既存失败如何对待？ → A: 按名称比较，两侧差集（新增/消失）都记录；消失项不追认为本特性修复（A3、FR-014、SC-006）。
