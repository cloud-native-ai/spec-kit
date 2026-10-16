# Requirements Specification: Agent+LLM 执行量化记录能力（Agent-LLM Execution Quant Recording）

**Requirement Branch**: `059-exec-quant-recording`  
**Created**: 2026-10-16  
**Status**: Draft  
**Input**: User description: "基于需求简报 /tmp/llm-quant-sdd-brief.md 创建特性 059 的 requirements.md:agent+LLM 执行量化数据记录能力(Recording Only)"

## Related Feature *(mandatory)*

**Feature ID**: 059  
**Feature Name**: Agent+LLM 执行量化记录(Execution Quant Recording)

## Overview

为 spec-kit 增加「agent 程序 + LLM」执行的**量化数据记录**能力:每个受测单元每次执行时,采集 (a) 执行所用的 **agent 程序信息**、(b) **LLM 详细信息**、(c) **任务完成质量指标**(时长、token 消耗、错误次数)与可选打分,经既有 probe + wrap-up 机制自动落库。**本期只做记录(Recording Only)**:积累可机读的执行遥测数据集,为后续量化分析特性供数;分析、报表、可视化、跨 run 聚合口径均不在本期(见显式排除项)。

采集由确定性程序执行(Token 效率纪律 Program-First,Constitution XII 复用门:复用既有 probe 注册表、wrap-up 挂点与运行判定测量,不另起炉灶);数值禁臆造(运行判定「测量而非印象」原则的延伸);采不到的字段以显式标记落库,可行性分级如实呈现,不许诺采不到的值。本特性是 Constitution VI(持续质量与可观测)的观测面扩充:只增观测,不改既有机制的契约(见 FR-015)。

### 现状锚点（2026-10-16 同机实测;dated record,仅作可行性输入,非运行时保证）

- **agent 程序信息:可全采。** 宿主 CLI 进程与实际二进制可见,版本号、启动参数、环境、工作目录均可读(实测 qodercli 1.1.72)。
- **LLM 详细信息:分级可采(难点所在)。** 进程环境中的端点变量均为「候选」而非「生效」——实测活跃连接指向 qoder.sh 系网关,env 中其他供应商端点无活跃连接;模型名 / context window / reasoning effort 自宿主 CLI 配置面可读,但未设置的 effort 生效值为 CLI 默认且配置面不回显(不可直接测得)。
- **质量量:** 时长与 token 消耗已有运行判定通道;错误次数与用户打分为新字段,来源由本规格定义(FR-007 / FR-014)。
- 运行时采集按**动态探测**设计:上述锚点不写死任何时点数值;任何字段在具体宿主上采不到,即显式降级落标记(见 Edge Cases、FR-005 / FR-006)。

### Assumptions（简报四个开放点的裁决记录）

- **A1 单元粒度 = 运行判定同语义。** 一次受测单元完成的执行 = 一条记录,身份三元组 `(unit_id, unit_type, run_id)`,不细化到子步骤。理由:与既有四轴记录同锚点、可按 run 关联;子步骤粒度留待后续特性。
- **A2 记录存放 = 独立持久存储,不入 feedback store。** 理由:feedback 红线 1(定位为「框架摩擦」的改进条目,非中性遥测)与红线 3(打包上送路径——量化记录含执行环境细节,永不自动上送);运行判定记录落 session 短期存储、身份是改进流程的改点 sensor,且其四轴契约已登记于多处真源,不宜膨胀承载环境遥测。故新设专属 durable 存储,由记录引擎自有,append-only、机器可读。
- **A3 触发挂点 = 既有 wrap-up probe 点。** 经 HandlerBinding 注册 engine-kind 非阻塞 handler(同 h-run-determination 模式),不新增每命令模板面、不新增确认门(确认门控预算零消耗)。
- **A4 打分输入通道 = 两者并存、按来源区分。** 用户手动(经引擎显式动作对既有记录补录打分)+ 运行判定推导(同 run 记录的 satisfaction 判定按 run_id 关联);两者凭字段来源标注区分,无打分即显式无,不臆造。
- **A5 引擎定名 `exec-quant.py`(scripts 层,框架源 → 运行时镜像)。** 2026-10-16 clarify Q2 锁定,plan 阶段不再重开命名(全仓同名冲突实测为零;如实现期发现冲突按快速失败上抛,不静默改名);跨制品引用的记录类型字面量以 Shared Strings 为唯一锚点。
- **A6 与运行判定的组合 = 并行携带、标注来源。** token 消耗与时长**不重复测量**:记录字段自同 run 的运行判定记录携带并标注来源;无对应记录时落显式未采标记。运行判定记录的 schema 与改进流程契约不变;运行判定记录仍是这两个量的唯一权威,量化记录中的携带值是程序写入、标注来源的机器副本(dated execution artifact),不作为现行事实被引用。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 每次执行自动落一条量化记录 (Priority: P1)

任何受测单元(命令/技能/自定义单元)完成一次执行后,一条量化记录自动落入专属存储:含 agent 程序信息、LLM 详细信息、质量指标三字段组;每个字段或为带来源标注的测量值,或为显式未采标记——零空缺、零臆造。采集失败不阻塞、不劣化单元运行本身。

**Why this priority**: 这是本特性存在的核心——没有自动落库,后续一切量化分析都无数据可分析。

**Independent Test**: 完整执行一次任一受测单元,查询专属存储可找到该次执行的记录并逐字段审计;独立于消费/打分能力即可交付价值(数据已开始积累)。

**Acceptance Scenarios**:

1. **Given** 任一受测单元完成一次执行, **When** wrap-up 执行, **Then** 专属存储中恰好新增一条该次 `(unit_id, unit_type, run_id)` 的量化记录,三字段组齐备,每字段或为带来源的值、或为显式未采标记
2. **Given** 当前宿主存在已知采不到的字段(如未设置的 reasoning effort、生效端点的权威值), **When** 记录写入, **Then** 这些字段以显式未采标记落库——零空缺、零臆造值
3. **Given** 采集程序执行失败(如宿主配置面不可读), **When** wrap-up 执行, **Then** 单元运行照常完成(非阻塞),采集失败在运行输出中可见

---

### User Story 2 - 记录可列出、可追溯、可补打分 (Priority: P1)

积累的记录可经引擎动作列出(按单元/类型/时间过滤、机器可读输出),每条可追溯到其 `(unit_id, unit_type, run_id)`;用户可对既有记录补录手动打分,手动打分与运行判定推导的满意度按来源区分。

**Why this priority**: 记录只有可列出、可追溯才成为「数据集」而非散落文件;打分通道本期只收数据,不做任何打分模型。

**Independent Test**: 落库若干记录后执行列出动作并验证过滤与追溯;对一条记录执行打分动作并验证来源标注;独立于 US1 的采集实现即可测试。

**Acceptance Scenarios**:

1. **Given** 存储中已有 ≥1 条记录, **When** 列出动作带单元过滤执行, **Then** 输出恰好枚举匹配记录,每条含身份三元组,且提供机器可读输出形态
2. **Given** 一条无手动打分的既有记录, **When** 打分动作以分值对该记录执行, **Then** 该记录携带用户打分且来源标注为用户给出,其余已测字段不变
3. **Given** 一条记录的满意度来自运行判定推导, **When** 该记录被列出, **Then** 其打分来源(用户给出 vs 运行判定推导)可区分

---

### User Story 3 - 既有机制零回归与边界隔离 (Priority: P2)

新增采集不得改变既有 feedback / probe / 运行判定引擎的行为;量化存储结构性地排除在反馈打包与一切自动上送路径之外;任何凭据型环境值不得进入任何记录。

**Why this priority**: 守护既有机制与安全边界是本特性可合入的前提;核心记录路径(US1/US2)先行,此为并行守护项。

**Independent Test**: 跑既有契约/集成套件比对失败名单;产出一个反馈打包产物并核对其不含量化记录;对全部记录做凭据变量名扫描。

**Acceptance Scenarios**:

1. **Given** 特性已实现, **When** 既有 feedback/probe/运行判定的契约与集成套件执行, **Then** 全部通过,失败名单与基线逐名比对零新增
2. **Given** 存储中已有量化记录, **When** 反馈打包动作执行, **Then** 打包产物含零条量化记录
3. **Given** 宿主环境中存在凭据型变量(密钥/token/鉴权头), **When** 采集执行, **Then** 任何记录中出现零个凭据值

---

### Edge Cases

- **宿主进程不可识别或多宿主并行**:agent 归属含糊时,记录可确定的部分并显式标注归属含糊,MUST NOT 猜测唯一进程。
- **宿主配置面缺失或不可读**:LLM 配置字段(模型名 / context window / effort)显式未采标记,记录其余字段照常落库。
- **未适配的宿主种类**:该宿主专属字段落显式未采标记,通用字段照常采集;适配缺口不阻塞记录落库。
- **执行中途失败或中止**:按运行判定的 qualification 语义——wrap-up 仍执行时记录照落并携带 qualification(含 partial 标注);wrap-up 未达则无记录,不补记。
- **存储写入失败(权限/磁盘)**:非阻塞跳过,失败在运行输出可见,不影响单元结果(同 feedback 红线 2 的非阻塞语义)。
- **记录体异常庞大(环境异常复杂)**:按封顶截断并在记录内标注截断,MUST NOT 整体转储环境(兼顾存储与泄密面)。

## Requirements *(mandatory)*

### Functional Requirements

#### 承载与触发（US1）

- **FR-001**: System MUST, for every completed execution of a covered unit (command / skill / custom-unit — the same unit semantics as Run Determination), produce exactly one execution quant record (record kind [[STR-001]]), identified by `(unit_id, unit_type, run_id)`
- **FR-002**: 采集 MUST 由 scripts 层的确定性程序执行(定名 `exec-quant.py`),不得由 LLM 判断替代(Program-First)
- **FR-003**: 采集 MUST 挂既有 wrap-up probe 点、经 HandlerBinding 注册 engine-kind 非阻塞 handler 触发;MUST 在同一 lifecycle point 上于运行判定 handler 之后执行,使携带值反映同 run 的判定记录;MUST NOT 新增每命令模板面, MUST NOT 新增确认门
- **FR-004**: 新增 probe 实体(scripts 切片的 Class + Objects)MUST 按伞形 probe 注册表真源的登记契约入册,派生视图重建而非手抄

#### 采集内容（US1）

- **FR-005**: agent 程序字段(宿主 CLI 身份、版本、启动参数、工作目录)在宿主可解析时 MUST 采集;任一字段在具体宿主不可解析时 MUST 以显式未采标记落库(按宿主如实降级)
- **FR-006**: LLM 详细字段 MUST 区分「候选值」(环境中可见的端点变量等)与「生效值」:模型名 / context window / reasoning effort 自宿主 CLI 配置面可解析时 MUST 采集;生效端点仅记录可判定的证据;一切不可获得的值 MUST 以显式未采标记([[STR-002]])落库;采集程序 MUST NOT 记录猜测的「生效」值(如对未设置 effort 推断 CLI 默认)
- **FR-007**: 质量字段:时长与 token 消耗在同 run 运行判定记录存在时 MUST 自该记录携带并标注来源,不存在时以显式未采标记([[STR-002]])落库;错误次数 MUST 自已枚举的声明来源采集(同 run 运行判定记录的异常/红色信号、单元声明的测试失败计数),逐记录标注所用来源,无可用来源时落显式未采标记;MUST NOT 臆造任何数值
- **FR-008**: 记录 MUST 携带逐字段来源标注(测量/携带/用户给出/未采),使后续分析可区分各值的取得方式

#### 存储与边界（US1 / US3）

- **FR-009**: 记录 MUST 落入项目 memory 层下由记录引擎自有的专属 durable 存储,机器可读、append-only;MUST NOT 写入 feedback store
- **FR-010**: 采集 MUST 仅捕获非敏感环境值的白名单;凭据型值(API 密钥、token、鉴权头)MUST NOT 出现在任何记录中;记录体 MUST 有尺寸封顶并在截断时于记录内标注
- **FR-011**: 量化存储 MUST 结构性排除于反馈打包与一切上送路径之外(零自动传输);任何流程 MUST NOT 将记录传送到任何外部目的地
- **FR-012**: 记录 MUST 非阻塞——采集失败 MUST NOT 使单元运行失败或劣化,且失败 MUST 在运行输出中可见

#### 消费与打分（US2）

- **FR-013**: Users MUST be able to list execution quant records (record kind [[STR-001]]) with unit / unit-type / time filters and a machine-readable output form, and trace every record to its `(unit_id, unit_type, run_id)`
- **FR-014**: Users MUST be able to attach a user-given score to an existing record via an explicit engine action; user-given score and Run-Determination-derived satisfaction MUST be distinguishable by provenance; absence of score MUST be explicit

#### 非回归（US3）

- **FR-015**: 既有 feedback / probe / 运行判定引擎行为 MUST 不变——feedback 的 record/list/package 等动作、probe 注册表校验、运行判定的 determine/settle/history 与其四轴记录 schema 及反馈路由推导,均不受本特性影响

### 显式排除项（Out of Scope）

- 量化分析、报表与可视化;跨 run 聚合口径
- 打分模型与阈值(自动判分);本期只收打分数据,不产判分
- 自动上送——feedback 上送永远手动,量化记录无任何上送路径
- 记录保留/清理策略(存储无界增长治理留待后续特性)
- feedback store schema 变更;既有四轴语义变更
- 新增阻断式确认门
- 会话/对话内容采集——只采元数据与遥测字段,MUST NOT 采集 prompt/response 文本

### Key Entities *(include if requirement involves data)*

- **执行量化记录 (Execution Quant Record)**: 一次受测单元执行的量化快照;身份 `(unit_id, unit_type, run_id)`;字段组:agent 程序 / LLM 详细 / 质量(时长、token、错误次数、打分)/ 采集来源标注与采集时间;记录类型 [[STR-001]];不可采字段以 [[STR-002]] 类显式标记呈现
- **执行量化存储 (Execution Quant Store)**: 项目 memory 层下的专属 durable 存储,append-only、机器可读,由量化引擎自有;位于 feedback store 之外,不入打包路径
- **量化引擎 (Recording Engine)**: scripts 层确定性采集程序(提议名 `exec-quant.py`),承担采集(挂 wrap-up 点)、列出(过滤/机器可读)、打分补录三个动作面
- **Probe 注册行**: 伞形 probe 注册表中 scripts 切片的新 Class + Objects 行,声明性元数据,行为真源在引擎代码

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 真实执行任一受测单元(如一个 /speckit.* 命令)后,查询专属存储可查到**恰好一条**该次 `(unit_id, run_id)` 的量化记录,且 agent 程序 / LLM 详细 / 质量三字段组齐备——每字段或为带来源标注的值、或为显式未采标记,零空缺
- **SC-002**: 在已实测宿主上,已知采不到的字段(生效端点权威值、未设置的 effort 等)100% 以显式未采标记落库;抽检记录中零臆造值
- **SC-003**: 既有 feedback / probe / 运行判定的契约与集成测试套件全部通过,失败名单与实现前基线逐名比对零新增(name-level)
- **SC-004**: 边界隔离零违例:反馈打包产物含零条量化记录;全部记录中凭据型环境变量值零出现

### Measurement Sources & Collection Methods

- **SC-001 Source**: 真实执行一个受测单元后,经列出动作(机器可读形态)与存储记录审计核对——记录数 = 1、三字段组齐备性由校验程序判定,逐字段核对值/来源/标记
- **SC-002 Source**: 以现状锚点的 dated 实测清单为「该宿主可得性」基准,校验程序统计显式未采标记覆盖率(目标 100%)并扫描零臆造值
- **SC-003 Source**: 既有测试套件(契约 + 集成标记)全量运行,以排序后失败 nodeid 名单对冻结基线做逐名比对(房式判据,非失败条数)
- **SC-004 Source**: 打包动作产物的清单核对(量化记录计数 = 0)+ 对全部记录做凭据型变量名扫描(计数 = 0)

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "speckit.exec-quant" | FR-001, FR-013 |
| `STR-002` | "not_evaluated" | FR-006, FR-007 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section. STR-001 已随 A5 定名锁定(clarify Q2);旋转仍只需编辑本节一行。STR-002 复用运行判定既有「未评」值域词形,不新造第三套标记词表;下游 contracts/tests 引用同一锚点。

## Clarifications

### Session 2026-10-16

<!-- 无人值守运行:封闭式澄清问题由执行代理按简报 §4(Recording Only)与「测量而非印象」原则自行裁决,裁决理由随行记录。 -->

- Q: Related Feature 绑定到哪个 Feature? → A: **本 Feature 059 自身**(新建落册)。编号已由分支 `059-exec-quant-recording` 与规格目录预分配;注册表当时无 059 行(requirements 会话仅提交规格 + 清单、未落注册行,登记义务顺延本轮补齐,记为上游偏差并披露)。绑定先例启发式核验:候选 028(Feedback 域)、055(存储拓扑)、056(Probe-Handler 基础设施)无一拥有「执行环境遥测采集」同类同胞——056 的同胞吸收面是 handler 注册类改动而非本能力;运行判定经注册表全文核验无归属特性行,无可绑定对象。按 feature-integration § Feature Binding Rules 走 create 分支:索引行(Draft)+ `features/059.md` 详情 + 表头计数同批更新。
- Q: 引擎命名(A5)维持「plan 阶段可调」还是本阶段锁定? → A: **本阶段定名 `exec-quant.py` 锁定**,plan 阶段不再重开。理由:全仓(scripts / src / .specify/scripts)同名冲突实测为零;记录类型字面量已由 STR-001 锚定;锁定消除本规格唯一一处「以 plan 为裁决者」的欠指定(tasks 生成期直接引用定名,消除改名返工面)。
