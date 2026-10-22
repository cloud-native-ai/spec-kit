# Requirements Specification: 执行量化数据反馈回传与汇总（Exec-Quant Feedback Channel）

**Requirement Branch**: `068-exec-quant-feedback-channel`  
**Created**: 2026-10-22  
**Status**: Draft  
**Input**: User description: "需要开发一个 068-* 新需求，这个需求是 .specify/specs/059-exec-quant-recording 的后续，需求内容是借助 feedback 通道机制，将各个客户项目中的 .specify/memory/exec-quant 数据收集回来进行分析和汇总。以 cws-lib-python 项目的 /storage/project/cloud-native-tools/cws-lib-python/.specify/memory/exec-quant 为例，在执行 /speckit.feedback package 命令的流程时需要将 exec-quant 数据一并收回，然后在 speckit 项目中进行分析和汇总。经过这个需求之后 /speckit.feedback 命令就会作为 speckit 框架的一个更通用的反馈机制。"

## Related Feature *(mandatory)*

**Feature ID**: 068（2026-10-22 由 `/speckit.clarify` 新建并绑定；注册状态 Draft）
**Feature Name**: 执行量化数据反馈回传与汇总（Exec-Quant Feedback Channel）

**Related features**:

- **059 — 执行量化记录（Exec-Quant Recording）**: 本特性的**前序与被修订对象,不是吸收者**。059 定义记录采集、专属存储、遮蔽与封顶;068 在其上增加回传与聚合层,并显式修订其 FR-011 的仅打包一条腿（修订关系见上文对照表,零静默矛盾）。059 的规格与登记条目零改写。

## Overview

为 spec-kit 增加「**执行量化数据回传与汇总**」能力,使 `/speckit.feedback` 从「只回传框架摩擦条目」升级为「**更通用的框架反馈通道**」:客户项目在执行 `/speckit.feedback package` 打包流程时,把本项目的 `.specify/memory/exec-quant` 执行量化数据(059 特性的记录产物)作为**一等载荷**一并收回;包经人工送达 spec-kit 上游后,spec-kit 侧把载荷中的记录**解出、归因、汇总**,在本地形成跨项目聚合分析层。全程零自动传输——打包是用户手动触发,送达是用户手动投递,汇总产物留在 spec-kit 本地。

本特性是 059(执行量化记录,Recording Only)的直接后续:059 显式排除的「量化分析、报表、跨 run 聚合口径」在本特性进入范围;059 的 FR-011(量化存储结构性排除于反馈打包)被本特性**显式修订**——修订只针对「打包」这一条腿,且包仅经人工投递路径流动,零自动传输红线(feedback-step.md § Positioning & Red Lines 第 3 条)**原样保留不放宽**。安全底线继承 059:凭据零出现、采集侧白名单与封顶不变、记录只读不重写、打包/接收/汇总全部非阻塞。

### 现状锚点（2026-10-22 同机实测;dated record,仅作可行性输入,非运行时保证）

- **打包写侧**: `.specify/scripts/python/feedback-utils.py` 的 `write_package` / `action_package`(约 1098–1234 行)当前把 feedback 条目 `.md` 打入 zip 根部,可选携带 `introspection/` 自省报告与 `SUBMISSION-NOTES.md`,并写入 `MANIFEST.md`;`kind: external` 条目按既有契约排除。包内今天**没有任何 exec-quant 内容**。
- **真实入站包基线**: `feedback/feedback-20261022T062525Z.zip` 含 20 条 feedback 条目 + MANIFEST,零 exec-quant 内容(068 前基线,只读参考)。
- **存储布局存在两类**: spec-kit 本仓 `.specify/memory/exec-quant/` 同时有 `records/` 逐条 JSON(15 个,schema_version=2)与遗留 `records.jsonl`(59 行,schema_version=1)与 `scores.jsonl`;样例客户项目 cws-lib-python 的 exec-quant 只有 `records/`(7 条,schema_version=2)+ 空 `scores/` 目录,无 jsonl。
- **字段形态混合**(同一条记录内部): 已测字段为 `{value, provenance}` 对象,未测字段为裸 `"not_evaluated"` 字符串;schema v1 记录缺 `config` 组与 `quality.exit_code`(引擎已有输出侧形态升级先例 `normalize_record_view`)。记录含 `llm.endpoint_candidates`(端点 URL,属环境细节、非凭据)。
- 上述差异意味着聚合侧 MUST 容忍版本/布局/字段形态差异(见 FR-007),运行时一切以动态探测为准,锚点不写死任何计数。

### 对 059 的修订关系（显式声明，无静默矛盾）

059 的边界原文见 `.specify/specs/059-exec-quant-recording/requirements.md`(FR-009 / FR-011 / SC-004 / 显式排除项)。本特性对它的修订**逐条显式**如下:

| 059 条目 | 原义 | 068 处置 |
|----------|------|----------|
| FR-011 量化存储结构性排除于反馈打包 | 打包产物含零条量化记录 | **修订**:量化记录可进入**手动触发**的打包产物;「一切自动上送路径排除」原样保留。修订后的安全边界见 FR-015 ~ FR-018 |
| 显式排除项「量化分析、报表与可视化;跨 run 聚合口径」 | 分析聚合不做 | **修订**:跨项目聚合与汇总分析进入本特性范围(US3),落 spec-kit 本地派生层 |
| FR-009 记录落专属 durable 存储、不入 feedback store | 存储拓扑 | **保留不变**:接收侧解出的记录进聚合层,MUST NOT 混入 feedback store |
| FR-010 凭据零出现、白名单、尺寸封顶 | 采集安全 | **保留不变**:打包与接收不新增采集面、不削弱遮蔽 |
| FR-012 非阻塞 | 采集失败不劣化运行 | **保留并延伸**:打包/接收/汇总各环节失败同样非阻塞、可见 |
| SC-004 打包产物含零条量化记录 | 验收判据 | **由 059 验收期语义废止**:068 落地后以本特性 SC-003/SC-005 替代该判据(059 的验收属其自身生命周期,不被追溯重写) |

### Assumptions（无人值守裁决记录,已由 clarify 裁决固化）

> 2026-10-22 `/speckit.clarify` 对 A1–A5 逐条裁决:**全部成立**,其中 A1（退出开关边界）、A2（子目录定名 `aggregated/`）、A3（字段形态）、A4（未知字段保留/跳过计数）有细化——权威表述以 `## Clarifications` Session 2026-10-22 与相应 FR 行为准,本节保留为裁决前的推理记录。

- **A1 载荷包含策略 = 有记录即包含,不新增开关与确认门。** 依据:入口明确要求 package 流程「将 exec-quant 数据一并收回」,语义是默认随包;打包本身已是用户手动动作,再叠一道确认门与确认门治理(可逆动作自动执行 + 执行报告)相悖。载荷是否提供退出开关属 plan 层细节,不影响本裁决。存储为空时按 FR-005 显式降级,不报错。（2026-10-22 clarify 更正:原文误引 FR-006,打包侧空存储降级的规范条目是 FR-005。）
- **A2 聚合层落点 = exec-quant 存储内、记录路径之外的引擎自有派生子目录(本仓即 `.specify/memory/exec-quant/` 下与 `records/`、`scores/` 平行的新子目录)。** 依据:一个域一个所有者(量化引擎已自有该存储);子目录隔离使入站/派生数据不与本地记录路径混淆;按并发开发安全纪律,派生产物按条落盘、可重建,绝不做成多流程并发重写的可变聚合单文件。
- **A3 跨项目身份 = 包级显式携带,记录级 `agent.cwd` 仅作佐证。** 依据:现包格式不含源项目标识,而记录的 `agent.cwd` 只在部分字段组存在且属采集面数据;归因是被依赖的一等事实,不得靠推断链。包级身份字段缺失时按显式 unknown 分组,不猜(见 Edge Cases)。
- **A4 兼容策略 = 聚合侧容忍,不改写源。** 布局(`records/` vs 遗留 jsonl)、schema(v1/v2)、字段形态(`{value, provenance}` vs 裸 `not_evaluated`)差异全部在**读取与派生视图**侧归一;遗留流保持只读可解析,永不重写(并发开发安全:遗留单体存储只读回退)。不可解析项跳过并计数,零臆造值。
- **A5 汇总产物只本地。** 聚合层与汇总报告留在 spec-kit 项目内,无任何自动外发路径;对外共享(如发布到 docs)只能由用户显式发起,且属后续特性/人工流程,不在本特性范围。

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently

  SCAFFOLDING IS OPEN-ENDED: the three story slots below are illustrative, not a quota.
  Write exactly as many stories as the feature genuinely decomposes into, with whatever
  priority distribution fits (e.g. two P1 stories, or four stories, or just one) —
  duplicate a slot for more stories and DELETE any unused slots. Do not invent filler
  stories to reach three, nor merge distinct journeys to stay at three.

  CROSS-CUTTING CONTEXT: if the feature hinges on a specific input modality or
  consumption channel (voice/dictated input vs typed, file import, API-only), record it
  explicitly as a first-class assumption alongside the stories — modality shapes both
  acceptance scenarios and edge cases, and surfacing it here beats burying it later.
-->

### User Story 1 - 客户项目打包时量化数据随包收回 (Priority: P1)

客户项目(如 cws-lib-python)的用户执行 `/speckit.feedback package` 打包流程:产物 zip 除既有 feedback 条目外,还包含本项目 exec-quant 存储的记录副本作为一等载荷,包清单(MANIFEST)显式声明载荷的存在、条数与降级情况。打包对本项目 exec-quant 存储与 feedback 存储全部只读;用户随后**手动**把包送达上游——与今天投递 feedback 包完全同一动作、同一通道。

**Why this priority**: 没有打包腿,数据永远出不了客户项目,后续一切汇总无从谈起;且它是 `/speckit.feedback` 升级为通用反馈通道的第一半。

**Independent Test**: 在含 exec-quant 记录的项目里执行打包流程,核对 zip 内容与 MANIFEST 声明;独立于接收/汇总能力即可交付价值(数据已可被收回)。

**Acceptance Scenarios**:

1. **Given** 客户项目 exec-quant 存储含 ≥1 条可读记录, **When** 用户执行打包流程, **Then** 产物 zip 含 exec-quant 载荷(记录条数与存储可读记录数一致),MANIFEST 显式声明载荷及其条数
2. **Given** 打包流程执行完成, **When** 核对客户项目两侧存储(feedback store 与 exec-quant store), **Then** 全部源文件零改动(只读打包),条目不因打包而移动或删除
3. **Given** 用户查看打包流程的输出报告, **When** 载荷被包含, **Then** 报告可见载荷条数——用户在手动投递前对包内数据范围知情
4. **Given** feedback 条目为空而 exec-quant 存储含 ≥1 条可读记录, **When** 用户执行打包流程, **Then** 仍产出包:包内零 feedback 条目(MANIFEST 显式计数 0)而 exec-quant 载荷照常纳入——载荷独立成包,不依附 feedback 条目(见 FR-019)

---

### User Story 2 - spec-kit 接收包并解出量化数据 (Priority: P1)

spec-kit 侧按既有入站包流程收到一个手工送达的 zip 后,处理流程识别其中的 exec-quant 载荷,把记录解出到本仓聚合层并按源项目归因;feedback 条目按既有消化路径处理,两条数据通路互不混流。对不含 exec-quant 载荷的既有形态入站包(如 068 前的真实基线包),处理行为与今天完全一致。

**Why this priority**: 数据回到了 spec-kit 但进不了聚合层,US1 的价值就止步于一个 zip;接收腿与打包腿共同构成闭环的最小可用版本。

**Independent Test**: 用一个含载荷的包执行接收流程,核对聚合层新增记录与 feedback store 零混入;再对一个无载荷既有包执行,核对行为零变化。

**Acceptance Scenarios**:

1. **Given** 一个含 exec-quant 载荷与 feedback 条目的入站包, **When** spec-kit 侧接收流程执行, **Then** 载荷记录进入聚合层并带源项目归因,feedback 条目进入既有消化路径,exec-quant 记录零条混入 feedback store
2. **Given** 同一个包被接收两次, **When** 第二次接收完成, **Then** 聚合层零重复条目(幂等)
3. **Given** 一个不含 exec-quant 载荷的既有形态入站包(基线包同构), **When** 接收流程执行, **Then** feedback 条目处理行为与 068 之前零差异,流程不因缺载荷而报错
4. **Given** 两个不同包因全量包含策略携带重叠记录(同一源项目同一记录), **When** 先后接收完成, **Then** 聚合层零重复条目——重叠记录按源记录身份(源项目 + unit_id + run_id + 采集时间戳)幂等合并,全量包含的重复代价由接收侧幂等吸收

---

### User Story 3 - 跨项目量化汇总可在本地查看 (Priority: P2)

spec-kit 维护者可对本仓聚合层执行汇总:得到跨项目、跨单元的聚合视图(各源项目记录数、各单元质量量分布、未测覆盖率等),机器可读;汇总只读本仓数据,产物落本地派生层,零外发。

**Why this priority**: 这是「分析和汇总」入口诉求的直接兑现,但它消费的是 US2 落地的数据,故排在 P1 两腿之后;没有它,收回的数据只是堆积。

**Independent Test**: 在聚合层已有 ≥2 个来源项目数据时执行汇总动作,核对聚合视图逐项可对账到原始记录;独立于打包腿即可测试(可直接构造聚合层数据)。

**Acceptance Scenarios**:

1. **Given** 聚合层含来自 ≥2 个源项目的记录, **When** 汇总执行, **Then** 聚合视图按源项目与单元维度给出记录计数与质量量分布,机器可读,且每个数字可对账到具体记录
2. **Given** 记录中存在未测字段([[STR-002]] 形态), **When** 汇总执行, **Then** 未测以显式未测计数呈现,任何缺失字段零臆造、零填补
3. **Given** 汇总执行完成, **When** 检查产物位置与传输面, **Then** 产物全部落本仓派生层,零网络操作、零自动外发

---

### User Story 4 - 通道升级不破坏既有边界与行为 (Priority: P2)

通道升级后,既有安全边界(凭据零出现、零自动传输)与既有行为(feedback 条目的 record/list/package/dispose 等动作、既有契约测试)全部保持:量化载荷不新增任何采集面,不触碰 059 的记录遮蔽与封顶;既有 feedback 打包对 feedback 条目的处理语义不变。

**Why this priority**: 守护边界是特性可合入前提;与前三条并行,不阻塞 MVP。

**Independent Test**: 产出一个含载荷的包并对其与聚合层做凭据扫描;跑既有 feedback/exec-quant 契约与集成套件比对失败名单;独立于前三条即可测试。

**Acceptance Scenarios**:

1. **Given** 打包产物与聚合层全部数据, **When** 凭据型值扫描执行, **Then** 零凭据出现(API 密钥/token/鉴权头零命中)
2. **Given** 打包、接收、汇总三个流程, **When** 审查其行为面, **Then** 零网络操作,一切流动都由用户手动发起
3. **Given** 既有 feedback 与 exec-quant 契约/集成测试套件, **When** 本特性实现后运行, **Then** 失败名单与实现前基线逐名比对零新增

---

### Edge Cases

- **客户存储为空或目录缺失**:包不含 exec-quant 载荷,MANIFEST/输出显式注明「无量化数据」,打包流程照常成功(非阻塞,零报错)。
- **feedback 条目为空而量化记录存在**:包仍产出,只含 exec-quant 载荷,feedback 条目计数显式为 0;两者都空才不产出(见 FR-019)。
- **部分记录损坏或不可解析**:可读记录照常入包,不可解析项在 MANIFEST 中显式计数跳过;零部分写入、零臆造。
- **仅存遗留布局**(只有 schema v1 的 `records.jsonl`、无 `records/` 目录):遗留流按只读方式纳入载荷并标注来源形态,源文件永不重写;接收侧按兼容策略归一(A4)。
- **载荷超过合理包体**:按显式封顶截断,MANIFEST 记录纳入数/截断数与截断标注,不静默丢弃也不无界膨胀。
- **包级源项目身份缺失**:记录归入显式 unknown-project 分组并在汇总中可见,MUST NOT 从文件路径或内容猜测身份。
- **同一包重复投递**:接收幂等,按源记录身份去重,零重复聚合条目(同 US2-3)。
- **入站包损坏**(zip 成员不可读):可读部分照常处理,不可读成员显式计数上报,feedback 条目处理不受阻(非阻塞)。
- **客户项目 exec-quant 引擎版本更老/更新**:以动态探测为准,未知新字段原样保留进聚合层,未知形态按未测处理;零版本号硬编码。

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

#### 打包腿——量化数据随包收回（US1）

- **FR-001**: 客户项目的 `/speckit.feedback package` 打包流程在 exec-quant 存储含 ≥1 条可读记录时 MUST 将存储中**全部可读记录**纳入包内 exec-quant 载荷(record kind [[STR-001]])——**全量包含,不引入增量水位**(clarify 裁决,代价与理由见 Clarifications);载荷作为包的一等组成在 MANIFEST 中显式声明(条数、来源形态、降级计数),MUST NOT 以临时附加文件等未声明形态混入
- **FR-002**: 打包 MUST 对 exec-quant 存储与 feedback store 严格只读——源记录文件零改动、零移动、零删除;记录的读取按来源形态(逐条 `records/` 目录、遗留 jsonl 流)分别容忍,遗留流保持只读不重写
- **FR-003**: 包 MUST 携带包级源项目身份字段,使接收侧可把载荷记录归因到源项目;身份字段形态为**源项目的项目名或稳定标识(必选)+ 框架 source commit(可选佐证)**,MUST NOT 以文件系统绝对路径作为身份载体,MUST NOT 新增凭据面;记录级环境字段(如 `agent.cwd`)仅作佐证,MUST NOT 作为唯一归因依据
- **FR-004**: 打包输出报告 MUST 向用户可见地报告载荷纳入情况(条数、降级计数),使用户在手动投递前对包内量化数据范围知情
- **FR-005**: 存储为空/目录缺失时包 MUST 显式降级为无载荷(注明「无量化数据」)并照常成功;部分记录不可解析时 MUST 纳入可读项并在 MANIFEST 显式计数跳过项;载荷体量 MUST 有显式封顶,截断时在 MANIFEST 记录纳入数/截断数;以上一切降级 MUST NOT 使打包流程失败(非阻塞)

#### 接收腿——解出与归因（US2）

- **FR-006**: spec-kit 侧入站包接收流程 MUST 识别 exec-quant 载荷(record kind [[STR-001]])并把载荷记录解出到本仓聚合层、按包级源项目身份归因;**接收由既有 `/speckit.feedback` 入站包处理路径承接,不新增命令**;识别/解出/归因/聚合的行为归属接收流程(引擎动作名留 plan),feedback 条目处理语义不变;exec-quant 记录 MUST NOT 进入 feedback store(059 FR-009 存储分界保留);身份缺失时归入显式 unknown-project 分组,MUST NOT 猜测
- **FR-007**: 接收与聚合层 MUST 容忍既有版本/布局/字段形态差异:逐条 `records/` 目录与遗留 jsonl 流并存、schema v1 与 v2 并存、已测字段 `{value, provenance}` 对象与未测字段裸 [[STR-002]] 字符串并存;读取侧归一为派生视图,缺失字段以显式未测标记呈现,**源记录中的未知字段 MUST 原样保留进聚合层(零丢弃)**,MUST NOT 推断或填补;不可解析项跳过并计数;源数据零改写
- **FR-008**: 接收 MUST 按源记录身份(源项目 + unit_id + run_id + 采集时间戳)幂等:同一包重复接收零重复聚合条目
- **FR-009**: 不含 exec-quant 载荷的既有形态入站包 MUST 与 068 之前行为零差异——feedback 条目处理语义、MANIFEST 语义、清理与对账动作全部不变,流程不因缺载荷报错
- **FR-010**: 接收过程的损坏与不可读(zip 成员、单条记录)MUST 显式计数上报且非阻塞——feedback 条目处理 MUST NOT 因量化载荷问题受阻或劣化

#### 汇总腿——本地聚合分析（US3）

- **FR-011**: spec-kit MUST 能对聚合层执行跨项目汇总,产出按源项目与单元维度的聚合视图(记录计数、质量量分布、未测覆盖率——以 [[STR-002]] 标记计数),提供机器可读输出形态,每个聚合数字可对账到具体记录;**汇总为显式动作**(可重复、可审计),由 `/speckit.feedback` 或量化引擎动作触发,MUST NOT 随接收自动执行(clarify 裁决)
- **FR-012**: 聚合层与汇总产物 MUST 落 exec-quant 存储内、本地记录路径之外的引擎自有派生子目录 **`aggregated/`**(即本仓 `.specify/memory/exec-quant/aggregated/`,与 `records/`、`scores/` 平行;接收记录与汇总产物均落其下,内部细分留 plan)(A2),按条落盘、可重建,形成多流程可并写形态;MUST NOT 造出多流程并发重写的可变聚合单文件(并发开发安全纪律)
- **FR-013**: 汇总 MUST 零臆造:未测/缺失字段以 [[STR-002]] 显式标记计数呈现,禁止任何填补、外推或基线杜撰(「测量而非印象」延伸)
- **FR-014**: 聚合层与汇总产物 MUST 仅存 spec-kit 本地,零自动传输、零网络操作;对外共享只能由用户显式发起且不属于本特性范围

#### 边界腿——修订后的安全边界与非回归（US4）

- **FR-015**: 凭据零出现贯穿全链路:打包产物、聚合层、汇总产物中凭据型值(API 密钥、token、鉴权头)MUST 零出现;打包与接收 MUST NOT 新增采集面、MUST NOT 削弱 059 采集侧的遮蔽与封顶(载荷只携带采集时已遮蔽/封顶的数据)
- **FR-016**: 零自动传输红线原样保留:打包、接收、汇总全部由用户手动发起、纯本地执行。059 FR-011 的修订**按子句拆开处置,零整条放宽**:其「结构性排除于反馈打包」子句修订为「量化记录可进入**手动触发**的打包产物」;其「排除于一切上送路径(零自动传输)」子句原样保留——任何流程仍 MUST NOT 将记录传送到任何外部目的地,本特性 MUST NOT 被解释为对该子句的放宽
- **FR-017**: 既有 feedback 引擎行为(record/list/status/dispose/mark-submitted/reindex/cleanup、external 条目排除、SUBMISSION-NOTES)与既有 exec-quant 引擎行为(collect/list-records/score)MUST 不受本特性影响
- **FR-018**: 既有 feedback / exec-quant 契约与集成测试套件 MUST 全部通过,失败名单与实现前基线逐名比对零新增(name-level)

#### 打包腿补充裁定——空反馈条目时载荷独立成包（US1，clarify 新增）

- **FR-019**: feedback 条目为空而 exec-quant 存储含 ≥1 条可读记录时,打包流程 MUST **仍产出包**:包内 feedback 条目计数为 0(MANIFEST 显式声明)而 exec-quant 载荷照常纳入;**仅当 feedback 条目与 exec-quant 可读记录都为空时**,包才不产出(显式降级说明)。既有引擎在 feedback 条目为空时的提前返回行为 MUST 依此修订——载荷可独立成包,不依附于 feedback 条目存在(本条按 doc-order 追加于 FR 列表末尾,语义属打包腿)

### 显式排除项（Out of Scope）

- 汇总产物的对外发布/自动化共享(发布到 docs、自动开 issue 等)——属后续特性或人工流程
- 打分模型、阈值判分、报表可视化界面
- 记录采集 schema 变更与采集面扩展(059 采集语义原样;载荷只回传既有记录)
- 记录/聚合数据的保留与清理策略(存储无界增长治理留待后续特性)
- 实时/在线遥测通道(仍为手工包批量回传,零守护进程、零常驻连接)
- feedback store schema 变更;既有四轴运行判定语义变更
- 新增阻断式确认门

### Key Entities *(include if requirement involves data)*

- **反馈包 (Feedback Package)**: 手工投递的 zip 产物;068 起布局为:feedback 条目(根部,不变)+ 可选 `introspection/`(不变)+ **exec-quant 载荷段(新增)** + MANIFEST.md(新增载荷声明段)+ 可选 SUBMISSION-NOTES.md(不变)
- **执行量化载荷 (Exec-Quant Payload)**: 包内 exec-quant 记录副本的统称:源项目身份 + 逐条记录(读自客户存储,含遗留形态)+ 载荷级降级计数;由打包流程一次写入、此后不可变
- **源项目身份 (Source Project Identity)**: 包级归因字段,把载荷记录绑定到来源客户项目;缺失时落显式 unknown-project 分组
- **聚合层 (Aggregation Store)**: spec-kit 本仓 exec-quant 存储内的引擎自有派生子目录 `aggregated/`(与本地 `records/`、`scores/` 平行):接收解出的记录(带归因)按条落盘、幂等去重、可重建
- **聚合视图 (Aggregate View)**: 汇总动作的机器可读产物:按源项目/单元维度的计数、质量量分布、未测覆盖率;每次汇总按条落盘于 `aggregated/` 之下,零臆造
- **量化引擎 (Exec-Quant Engine)**: `exec-quant.py`(059 已定名),本特性只扩展其回传/聚合相关动作面,采集/列出/打分语义不变;打包/接收侧改动落 feedback 引擎与接收流程

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: 在含 ≥1 条可读 exec-quant 记录的客户项目中执行打包流程:产物 zip 含 exec-quant 载荷且 MANIFEST 显式声明,载荷记录条数与存储可读记录数一致;打包后两侧存储源文件零改动(逐一核对零差异)
- **SC-002**: 两类既有存储形态均可打包——样例客户项目形态(仅 `records/` + 空 `scores/`,字段形态混合)与 spec-kit 本仓形态(`records/` + 遗留 jsonl 流并存),各自产出载荷且遗留流标注来源形态,零报错
- **SC-003**: 含载荷入站包接收后:聚合层新增记录逐条带源项目归因且与载荷逐条对账一致;feedback store 中 exec-quant 记录零条混入;同一包二次接收零重复条目
- **SC-004**: 聚合层含 ≥2 个来源项目时执行汇总:聚合视图按源项目/单元维度给出计数与分布,机器可读;抽检任意聚合数字可对账到具体记录;未测字段以显式未测计数呈现,零臆造值(审计通过)
- **SC-005**: 边界零违例:打包产物、聚合层、汇总产物中凭据型值扫描零命中;打包/接收/汇总流程网络操作零次
- **SC-006**: 既有 feedback 与 exec-quant 契约/集成测试套件全部通过,失败名单与实现前基线逐名比对零新增;一个 068 前形态入站包(基线包同构)接收行为与 068 之前零差异

### Measurement Sources & Collection Methods

- **SC-001 Source**: 样例客户项目实测打包:执行打包动作后列出 zip 内容与 MANIFEST 载荷段,存储目录打包前后各做一次逐文件清点比对(条数 + 内容零差异)
- **SC-002 Source**: 双形态实测——cws-lib-python 样例存储(7 条记录、`scores/` 空,dated 实测基线)与本仓存储(`records/` + 遗留流)各打包一次;形态标注从 MANIFEST 载荷段核对,不以硬编码计数为准(动态探测)
- **SC-003 Source**: 构造含载荷测试包执行接收动作,以聚合层清单与 feedback store 清单逐一核对归因与混入计数;幂等以同一包二次接收后的聚合层条目增量为零判定
- **SC-004 Source**: 以 ≥2 个来源项目的聚合层数据执行汇总动作,机器可读输出;对账抽检(任选数字→追到记录)与臆造值审计(未测字段不得出现具体数值)由校验程序判定
- **SC-005 Source**: 对产物 zip、聚合层目录、汇总产物分别执行凭据型变量名扫描(计数 = 0);流程网络操作以引擎代码审查 + 运行面观察判定(引擎零网络为既有红线延续)
- **SC-006 Source**: 既有测试套件(契约 + 集成标记)全量运行,以排序后失败 nodeid 名单对冻结基线做逐名比对(房式判据);基线包行为比对以同一包在实现前后各接收一次的输出与存储增量比对判定

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "speckit.exec-quant" | FR-001, FR-006 |
| `STR-002` | "not_evaluated" | FR-007, FR-011, FR-013 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section. 两个字符串均为**沿用既有锚点**:STR-001 复用 059 的记录类型字面量(其 Shared Strings STR-001 同值),STR-002 复用运行判定/量化引擎既有「未评」词形;本特性不新造词表,下游 contracts/tests 引用同一锚点。

## Clarifications

<!-- 
This section will be populated by /speckit.clarify command with questions and answers.
Format: - Q: <question> → A: <answer>
-->

### Session 2026-10-22 — clarify（无人值守,Mode A）

> 本阶段为无人值守运行,未向用户发起访谈;以下裁决按入口指令、059 既有边界与仓库现状自行作出并标注推荐依据,已同步落入相应 FR/SC/Edge Cases。裁决对象 = requirements 阶段留下的 Assumptions A1–A5 与派发方明确列出的追加裁定项。

- Q: Related Feature 绑定既有 Feature 还是新建? → A: **新建 Feature 068(本规格自身)**,不绑定 059;059 是前序与被修订对象,不是吸收者。依据:本特性引入新能力面(回传+聚合,横跨 feedback 与 exec-quant 两个既有引擎),而 059 的采集语义与边界原文零改写。注册义务已履行:`.specify/memory/features.md` 新增 068 行(Draft)+ `features/068.md` 详情;按 feature-integration § Binding Rules 本应向邻接 Feature 写逆向交叉引用,但派发约束明确「不要改写 059 制品」,故承接关系只记录于 068.md 的 Related Specifications(偏离已披露)。
- Q: A1 载荷包含策略——默认包含还是显式开关/确认门? → A: **默认「有记录即随包包含」,不新增阻断式确认门**;如实现层提供退出开关,只能是非阻断的可选参数,且不构成确认门(可逆动作自动执行+执行报告,与确认门治理边界一致)。依据:打包本身已是用户手动动作,入口语义是「一并收回」;FR-004 的知情报告承担可观测性。已固化进 FR-001。
- Q: feedback 条目为空而 exec-quant 记录存在时,打包行为? → A: **仍产出包,只含 exec-quant 载荷**(MANIFEST 显式声明 feedback 条目计数 0);两者都空才不产出。依据:现状引擎在 feedback 为空时提前返回「No feedback entries」,该行为会使量化数据在纯量化场景下无法收回,与「载荷是一等组成」矛盾。已固化为新 FR-019 + US1 验收场景 4 + Edge Case 条目。
- Q: 每次打包携带全部可读记录,还是只携带自上次打包以来的新记录(水位)? → A: **全量包含,不引入水位**。依据:接收侧幂等去重(FR-008,按源记录身份)使重复载荷无害;水位是新增可变状态,须定义存储、更新时机与并发安全形态(违反并发开发安全纪律的成本高于重复传输),而全量包含零新增状态、零丢数风险(漏标水位即丢数据)。代价 = 相邻多次打包重复携带同一批记录,由接收幂等吸收;体量由 FR-005 封顶约束。已固化进 FR-001 + US2 验收场景 4。
- Q: A3 包级源项目身份字段的形态? → A: **项目名/稳定标识(必选)+ 框架 source commit(可选佐证)**;MUST NOT 以绝对路径作身份载体(跨机不稳定、属环境细节),MUST NOT 新增凭据面;缺失时落显式 unknown-project 分组,不猜。已固化进 FR-003。
- Q: A2 聚合层落点的具体子目录名? → A: **`aggregated/`**(本仓即 `.specify/memory/exec-quant/aggregated/`,与 `records/`、`scores/` 平行),接收记录与汇总产物均落其下,按条落盘、可重建、幂等去重;内部细分布局留 plan。依据:一个域一个所有者(量化引擎自有该存储);子目录隔离派生数据与本地记录路径。已固化进 FR-012 + Key Entities。
- Q: 接收走新命令还是既有路径? → A: **既有 `/speckit.feedback` 入站包处理路径(Path A intake)承接,不新增命令**;feedback 条目处理语义不变;识别/解出/归因/聚合的行为归属接收流程(引擎动作名留 plan,行为边界以 FR-006~FR-010 为准)。已固化进 FR-006。
- Q: 汇总是接收后自动执行还是显式动作? → A: **显式动作**(可重复、可审计),由 `/speckit.feedback` 或量化引擎动作触发;接收只负责解出归因,MUST NOT 自动汇总。依据:自动触发会把派生写混入接收路径(两流程并发写同一面,违反并发隔离);显式动作让每次汇总产出独立可对账条目。产物机器可读、按条落盘于 `aggregated/`、仅本地零外发。已固化进 FR-011/FR-012/FR-014。
- Q: A4 兼容策略的读取侧归一细则? → A: schema v1/v2、`records/` 目录 vs 遗留 jsonl、`{value, provenance}` vs 裸 [[STR-002]] 三类差异全部在**读取与派生视图**侧归一;**源记录中的未知字段原样保留进聚合层(零丢弃)**;不可解析项跳过并计数,零臆造值;源数据零改写(遗留单体流只读回退)。已固化进 FR-007(FR-005/FR-010 承接计数)。
- Q: A5 边界复核——修订 059 FR-011 会不会被读成放宽零自动传输? → A: **不会**:修订按子句拆开处置——「结构性排除于反馈打包」修订为仅限手动触发打包;「排除于一切上送路径(零自动传输)」原样保留,任何流程仍 MUST NOT 外送;059 的采集遮蔽与封顶不变;本特性不新增确认门。已固化进 FR-016(子句拆分表述)+ FR-015。
- Q: Feature 注册的既有计数状态? → A: `features.md` 表头 `Total Features`=64 与实际行数 64 一致,本次新增 068 行后同步更新为 65,零漂移;披露一个**既有**缺口(非本特性引入,不在本阶段修复):specs 066/067 存在但注册表无对应行(066/067 的注册义务属其自身特性线),本阶段不代为补录。

