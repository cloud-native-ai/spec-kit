# Requirements Specification: Feedback 自省流程(Feedback Introspection)

**Requirement Branch**: `047-feedback-introspection`  
**Created**: 2026-08-27  
**Status**: Draft  
**Input**: User description: "在 feedback 系统中增加一个 "Introspection（自省）" 流程。背景与动机：现有的 feedback 流程以记录事实为主（通过 feedback-utils.py 记录，达到阈值后打包提交给消费方），然后由 feedback 的消费方进行整体优化的设计；但这样的处理流程往往脱离了真实场景。Introspection 流程就是为了解决这个问题：在客户项目（Client Project）中执行 introspection 流程，可以基于真实场景针对 feedback 进行更深层次的思考，找到真正的问题和最合适的优化方案。"

## Related Feature *(mandatory)*

<!--
  ACTION REQUIRED: Keep the default values as "Need clarification" in the initial draft.
  /speckit.clarify must resolve this section to the final Feature binding before planning.
-->

**Feature ID**: 028  
**Feature Name**: Feedback Mechanism

## Overview

### 现状锚点(以源码实测为准)

现有 feedback 本地闭环(以 `feedback-utils.py` 引擎与 `/speckit.feedback` 命令为准)为**事实记录 + 远端设计**的两段式:

1. **记录(事实层)**:各命令/技能 wrap-up 的 `## Feedback` 步骤做 agent 自评,经 `--action record` 落条目(scope: local;内容 = `## Review` + `## Optimization Points`),条目经 Probe Object→Class 继承 kind/slice 归属。
2. **本地管理**:`/speckit.feedback` 提供 status/list/dispose(处置)/package(打包,仅 internal 条目)/cleanup/mark-submitted;外部 probe 条目恒为本项目本地(Loop B),永不入上行包。
3. **消费(设计层)**:框架项目侧 `/speckit.feedback consume`(Mode 4)对 `feedback/` 目录下的 zip 做跨包对账、核验与路由(直接修复 / `/speckit.requirements` / improve-* / 仅记录)。

**问题**:优化设计发生在消费方——消费方拿到的只有条目的**事实陈述**(记录时刻的 review 与优化点),而条目诞生的**真实场景**(被评单元的当前形态、引用文件、运行上下文、环境差异)留在客户项目里、不随包上行。消费方脱离场景做整体设计,容易产出浅薄、错位或无法落地的优化方案;大量本可在源头核验清楚的事实(如"该问题是否仍存在""根因是单元缺陷还是用法错误")被推迟到消费侧冷分析。

**本特性的解法**:在记录与上行之间插入 **Introspection(自省)** 阶段——在**客户项目**(Client Project,术语见 `.specify/shared/definitions/dogfooding-definitions.md` §2)内、基于真实场景对已积累的 feedback 条目做深度思考:核验事实、聚类同根因条目、定位真正的问题、给出最适配的优化方案并做分流决定(本地下沉 Loop B vs 随包上行 Loop A)。上行包由"裸事实"升级为"事实 + 场景证据 + 根因 + 方案",消费侧专注跨项目对账而非冷启动分析。

**与既有能力的边界**:record = 事实捕获(wrap-up 埋点,本特性不改);introspection = 事实的深加工(按需触发,本特性新增);package/consume = 传输与上游对账(本特性只做输入富化,不改其批处理纪律);`/speckit.review` = 单 feature SDD 过程质量全局评审(对象不同,不重叠);improve-* 技能 = 改进的执行方(introspection 只产出经验证的输入,不代替执行)。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 场景化自省:从事实条目到根因发现 (Priority: P1)

客户项目中的用户(本仓 dogfooding 时即框架维护者本人)在积累了一批待处理 feedback 条目后,发起一次自省。agent 面向**每一条在范围内的条目**回到其真实场景:调出被评单元的当前定义/源码、条目引用的文件与上下文,核验条目的事实主张在当前状态下是否成立(成立/部分成立/已过时/不成立),把同根因的条目聚成一个"问题",并为每个问题给出根因、场景证据、影响面与具体优化方案。最终产出一份持久化的自省报告——报告的主体是**问题清单**而非条目流水。

**Why this priority**: 这是自省流程的核心价值与 MVP——仅这一个故事落地,客户项目就已能把"裸事实"加工成"经过场景核验的根因发现",本地改进(Loop B)即刻受益,后续分流与上行富化都建立在这份报告之上。

**Independent Test**: 在一个含有若干 open 条目的 feedback 存储上执行一次自省,验证:(a) 产出的报告覆盖了范围内 100% 条目(每条要么归属某个问题、要么显式说明排除理由);(b) 每个问题都含根因、至少一条指向真实场景的证据锚点、分流决定与优化方案;(c) 报告落盘为持久产物,可在后续会话中被查阅与引用。

**Acceptance Scenarios**:

1. **Given** 存储中存在多条 open internal 条目(其中两条指向同一单元的同类摩擦),**When** 用户发起自省,**Then** 产出自省报告:这两条被聚为一个问题,问题含根因陈述、证据锚点(指向当前单元定义/文件的具体位置)、分流决定与优化方案
2. **Given** 某条目主张"单元 X 存在缺陷 Y",**When** 自省核验发现当前源码中 Y 已不存在(期间已被修复),**Then** 该条目被标注"已过时"并附核验依据,而不是原样进入问题清单
3. **Given** 某条目引用的文件/路径已不存在,**When** 自省执行到该条目,**Then** 自省不中断,该条目被标注"无法复现/已过时"并给出处置建议
4. **Given** 存储中没有 open 条目,**When** 用户发起自省,**Then** 明确报告"无可自省条目"并正常结束,不产生空报告文件

---

### User Story 2 - 分流与处置:本地下沉 vs 随包上行 (Priority: P2)

自省报告中的每个问题都带有分流决定:**本地下沉**(属客户项目自有资产/用法问题,走 Loop B,路由到本项目的直接修复或 improve-* 等既有改进通道)或**随包上行**(属框架机制问题,走 Loop A,纳入下次上行包)。外部 probe 条目(客户自定义单元)恒为本地下沉,不破既有"永不上行"红线。用户确认报告后,条目侧的处置联动生效:被自省覆盖的条目按建议批量处置(processed/ignored 并附自省来源理由),条目与其所属问题/报告建立可回查的关联。

**Why this priority**: 自省的价值必须通过"决定去向"兑现——没有分流,报告只是又一份文档;有了分流,本地问题就地闭环、框架问题带着分析上行,两条 dogfooding 环路各得其所。它依赖故事 1 的报告产物,故列 P2。

**Independent Test**: 对一份含混合分流决定(至少一条本地下沉、一条随包上行)的自省报告执行确认,验证:(a) 覆盖条目的处置状态与理由被批量写回;(b) 条目可回查到所属问题与报告;(c) 外部 probe 条目不出现在任何上行候选中;(d) 未经用户确认,任何分流建议不生效、不做任何代码/配置改动。

**Acceptance Scenarios**:

1. **Given** 自省报告含一个问题被判定为"本项目用法错误"(本地下沉),**When** 用户确认报告,**Then** 该问题被路由到本项目的改进动作建议(如直接修复或 improve-* 运行),且其成员条目被处置为 processed 并附自省报告引用
2. **Given** 自省报告含一个问题被判定为"框架机制缺陷"(随包上行),**When** 用户确认报告,**Then** 该问题被标记为上行候选,其成员条目不被 dispose 为 processed 以外的上行阻断态,等待打包
3. **Given** 范围内混入外部 probe 条目,**When** 自省完成分流,**Then** 外部条目只获得本地下沉路由,任何上行候选清单中均无外部条目
4. **Given** 用户对报告中某个问题的分流决定改为相反方向,**When** 确认时覆盖该决定,**Then** 以用户决定为准并记录覆盖痕迹

---

### User Story 3 - 上行包富化:事实+分析一起抵达消费方 (Priority: P2)

自省之后执行打包时,打包流程默认提议把覆盖这些条目的自省报告一并纳入上行包;用户确认后,消费方收到的不再只是条目事实,而是"事实 + 场景核验结论 + 根因 + 优化方案"的完整输入。消费侧(Mode 4)的既有批处理纪律不变,但面对自省过的条目可直接采信其核验结论,把精力集中在跨项目对账与冲突裁决上。

**Why this priority**: 这直接回应了用户的原始痛点——"消费方脱离真实场景做整体设计"。它依赖故事 1(报告存在)与既有 package 通道,不改变传输与人工送达红线,故列 P2。

**Independent Test**: 在自省完成后执行一次打包,验证:(a) 打包流程默认提议附入覆盖本批条目的自省报告;(b) 确认后产出的 zip 内同时含条目与自省报告,且报告可独立于条目被读取;(c) 用户选择不附报告时打包仍可完成(向后兼容)。

**Acceptance Scenarios**:

1. **Given** 本批待打包条目已被某次自省覆盖,**When** 用户发起打包,**Then** 流程提示将附入对应自省报告,确认后 zip 内含该报告
2. **Given** 待打包条目未被任何自省覆盖,**When** 用户发起打包,**Then** 打包按现有行为完成,不强制要求先自省
3. **Given** 消费方收到含自省报告的包,**When** 执行 consume,**Then** 消费报告能区分"已经源头核验"的发现与"仅事实陈述"的条目,并对前者减少重复核验

---

### Edge Cases

- 自省执行期间有新条目写入(wrap-up 埋点仍在运转):自省以发起时刻的范围快照为准,新条目留给下一次,不追逐移动目标。
- 同一批条目被重复自省:新报告与旧报告建立承继关系(标注 supersedes/基于),不制造重复问题;已确认的处置不被自动翻案。
- 条目记录于旧版本框架、期间项目已升级:核验一律针对**当前**状态,已被升级修复的主张标"已过时"。
- 存储条目量大:遵循 Token 效率纪律(摘要优先、升级阶梯),支持按 slice/kind/since 收窄范围,禁止整库原文注入。
- 报告落盘后用户手动删改了条目:条目↔问题关联以条目 id 为准,缺失条目在引用处标注失效而非报错。
- 客户项目即框架项目本身(本仓 two-hats):自省流程不变,分流决定按"客户项目自有资产 vs 框架机制"如实判定。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST 提供按需触发的自省流程,可在任意客户项目内对已积累的 feedback 条目执行;默认范围为 open 状态的 internal 条目,用户可按需收窄或扩大范围(如按 slice/kind/since 过滤、显式包含外部条目)。
- **FR-002**: 自省 MUST 基于真实场景分析每条范围内条目:调出被评单元的当前定义/源码及条目引用的相关上下文,禁止仅凭条目文本做孤立判断。
- **FR-003**: 自省 MUST 对每条条目的事实主张做当前状态核验,并给出带证据的核验结论(成立/部分成立/已过时/不成立)。
- **FR-004**: 自省 MUST 把同根因的条目聚类为"问题",报告以问题为主体组织,而非条目流水;每条范围内条目恰好归属一个问题或被显式排除(附理由)。
- **FR-005**: 每个问题 MUST 含齐五要素:问题陈述、根因、场景证据锚点(指向具体单元/文件/位置)、分流决定、具体优化方案。
- **FR-006**: 分流决定 MUST 二选一:本地下沉(Loop B,路由到本项目改进通道)或随包上行(Loop A,纳入上行候选);外部 probe 条目的发现 MUST 恒为本地下沉,永不进入上行候选。
- **FR-007**: 自省产物 MUST 持久化为可跨会话查阅、可被条目与上行包引用的报告 artifact,存放于 feedback 存储域内。
- **FR-008**: 经用户确认报告后,被覆盖条目 MUST 按报告建议批量写回处置状态(processed/ignored)并附自省来源理由,且条目与其所属问题/报告建立可回查关联;未经确认,任何分流与处置建议不生效。
- **FR-009**: 打包上行时,若待打包条目已被自省覆盖,流程 MUST 默认提议将覆盖它们的自省报告一并入包;用户可拒绝,拒绝不阻断打包。
- **FR-010**: 自省全流程 MUST NOT 自动修改代码/配置、MUST NOT 自动传输任何内容;所有落地动作(直接修复、improve-* 运行、打包与人工送达)均经既有通道由用户确认后执行。
- **FR-011**: 自省消费 feedback 存储时 MUST 遵循 Token 效率纪律(程序优先、摘要优先、升级阶梯),不做整库原文注入。
- **FR-012**: 自省 MUST 对边界态给出明确行为:零范围条目时报"无可自省条目"正常结束;引用物已失的条目标注"已过时/无法复现"而非中断;重复自省时新报告与旧报告建立承继关系、不重复造问题。

### Key Entities *(include if requirement involves data)*

- **Introspection Report(自省报告)**:一次自省运行的持久产物——标识、创建时间、范围快照(条目过滤条件与覆盖条目清单)、问题列表、与既有报告的承继关系(若有)。
- **Finding(问题/发现)**:报告的主体单元——问题陈述、根因、证据锚点、分流决定(本地下沉/随包上行 + 目标通道)、优化方案、成员条目 id 集、用户覆盖痕迹(若有)。
- **Routing Decision(分流决定)**:finding 的方向属性——本地下沉(Loop B,本项目改进通道)或随包上行(Loop A,上行候选);外部条目恒为本地下沉。
- **Feedback Entry(反馈条目,既有实体)**:自省的分析对象;新增与所属 finding/报告的关联及自省来源的处置理由。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 范围内 open 条目 100% 被自省报告覆盖——每条要么归属唯一问题,要么带理由的显式排除;抽查任意条目均可回查到其问题归属或排除理由。
- **SC-002**: 报告中 100% 的问题含齐五要素(问题陈述/根因/证据锚点/分流决定/优化方案);可由结构性校验程序判定,无需人工判读。
- **SC-003**: 对报告中所有含事实主张的发现,100% 带有针对当前项目状态的核验结论与证据;"仅凭条目文本直接采信"的发现数为 0。
- **SC-004**: 自省覆盖过的条目被打包上行时,经确认路径产出的包 100% 含对应自省报告;未被自省覆盖的打包行为与现状一致(零回归)。
- **SC-005**: 消费侧处理"随包上行且经自省"的发现时,无需重复事实核验即可路由的比例 ≥80%(以消费报告中的路由记录度量);基线 = 现状 consume 对每条目均需冷核验(0%)。
- **SC-006**: 对 ≤50 条范围内条目的自省可在单次会话内完成,期间无需用户手工搜集/粘贴任何场景材料。

### Measurement Sources & Collection Methods

- **SC-001 Source**: 自省报告的覆盖清单 vs feedback 存储的条目清单,经确定性程序比对(覆盖差集为空);每次自省运行后度量。
- **SC-002 Source**: 报告结构性校验(五要素字段存在性检查)的输出;随每次报告产出一并给出。
- **SC-003 Source**: 报告内核验结论字段 + 证据锚点抽查;抽样复核锚点可解析到真实位置。
- **SC-004 Source**: 上行包清单(MANIFEST)内容检查,统计含自省报告的包占比;基线为当前 0 附报告。
- **SC-005 Source**: 框架侧 consume 运行产出的消费报告(路由记录中"采信源头核验"vs"重复核验"计数);随每次 consume 度量,与自省前基线对比。
- **SC-006 Source**: 自省运行的会话观察(是否发生用户手工补给材料的交互);按运行抽察。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "introspect" | `/speckit.feedback` 命令模板的自省触发关键字(`$ARGUMENTS` 匹配)、docs/reference/commands/feedback.md、契约测试断言 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Out of Scope

- **自动修复/自动落地**:自省只产出经验证的分流与方案,任何代码/配置改动仍由既有通道(直接修复、improve-* 等)经用户确认后执行。
- **自动传输**:上行包的人工送达红线不变,自省不引入任何网络行为。
- **Mode 4 批处理纪律变更**:consume 的一次一批、读后清理等纪律不动;自省只是让包的内容更富。
- **跨项目聚合分析**:每个客户项目自省自己的存储;跨项目对账仍是消费侧(Mode 4)的职责。
- **`## Feedback` 埋点与 record 动作改造**:事实捕获层保持现状。

## Assumptions

- **入口形态**(已经 2026-08-27 clarify 确认为决策,见 Clarifications):自省作为既有 `/speckit.feedback` 统一入口的一个新执行模式(以 `introspect` [[STR-001]] 关键字触发),不新增顶层命令;与 Mode 1-4 并列,符合"反馈机制本地管理统一入口"定位。
- **触发方式**:纯按需(on-demand);达到阈值时的非阻塞提示语可顺带建议先自省再打包,但绝不强制。
- **适用范围**:任意客户项目(含本仓自用 `.specify/`,two-hats 下照常);外部 probe 条目可被自省,但分流恒为本地下沉。
- **报告存放**:落在既有 feedback 存储域(`.specify/memory/feedback/`)内,具体命名/格式在规划阶段定。
- **确认门槛**:报告确认、处置批量写回、打包附报告、任何落地修复——四处均沿用既有确认门规范(可逆动作自动执行+报告、不可逆动作前置确认),不自创新门槛。
- **语言**:报告与交互沿用项目惯例(中文为主,标识符英文)。

## Clarifications

<!-- 
This section will be populated by /speckit.clarify command with questions and answers.
Format: - Q: <question> → A: <answer>
-->

### Session 2026-08-27

- Q: 需求 047 的 Related Feature 如何绑定(候选 Feature 028 «Feedback Mechanism»,Implemented;027 初建、041 递进)? → A: 绑定 Feature 028,不新建 Feature;与 027/041 同族递进,028 详情文件登记 047 递进记录
- Q: 自省流程的入口形态(/speckit.feedback 新增模式 vs 独立顶层命令 vs 独立 Skill)? → A: /speckit.feedback 新增 introspect [[STR-001]] 模式,与 Mode 1-4 并列;复用反馈管理统一入口,不新增命令注册面
