# Requirements Specification: Session 导出与导出侧重命名(/speckit.session + export-session 通用化)

**Requirement Branch**: `039-session-export`  
**Created**: 2026-08-12  
**Status**: Draft  
**Input**: User description: "实现一个 /speckit.session 命令,包含 export 子命令:将当前 AI agent CLI 的会话(session)导出到一个目录中,目录使用用户指定的名称。不再尝试对 session 本身重命名(宿主 CLI 无官方会话命名机制),退一步改为「导出后在导出的文件/目录上重命名」。需要支持六家 AI agent CLI:Claude Code / Codex CLI / Qoder CLI / GitHub Copilot / opencode / Hermes Agent。session 导出的主要工作由 skills/export-session 技能完成;需要对该技能进行彻底改造:只支持上述六种工具,其他支持一律移除,并将技能改造为通用技能(不绑定单一宿主)。最后针对导出的 session 总结一个描述文档,描述文档中包含 session 的元信息和对该 session 的结构化总结。"
**背景承接**: 前序暂存 todo「Agent 会话自定义命名适配」(已按「已合入即删除」纪律随本需求合并处置)。原诉求为对 Agent 当前 Session 自定义命名,替代系统自动生成的 Session 名;范围裁定为 AI agent CLI 会话——例如 /speckit.team run 派发外部 CLI 成员时给会话命名便于追溯;不包括 Spec Kit 记忆会话层(.specify/memory/session/)。研究结论:六家 CLI 均无官方会话命名/重命名机制(会话为自动生成 ID,仅按 ID resume/continue),故本需求采用「导出 + 导出侧重命名」的降级路线。

## Related Feature *(mandatory)*

**Feature ID**: 043
**Feature Name**: Session Export

## Overview

AI agent CLI 的会话只有系统自动生成的 ID,既不能命名,也难以跨工具归档与追溯——团队 run 派发外部 CLI 成员后,产物三元组能追溯"哪次派发",却追溯不到"那个会话里发生了什么"。本需求提供**导出侧命名**路线:`/speckit.session export --name <名称>` 把当前(或指定)会话连同其原始记录导出为一个**以用户名称命名的目录**,并附带一份**会话描述文档**(元信息 + 结构化总结),使会话成为可命名、可归档、可检索的项目资产。

导出的重活由 `export-session` 技能承担;该技能现有支持面(10 个产品,源码实测 2093 行单脚本)彻底收敛为**恰好六家** AI agent CLI——Claude Code / Codex CLI / Qoder CLI / GitHub Copilot / opencode / Hermes Agent——其余适配器全部移除,并改造为不绑定单一宿主的通用 Spec Kit 技能。

### 现状锚点(以源码实测为准)

- `skills/export-session` 已在库(SKILL.md v1.3.0 + `scripts/export.py`),来源标记 `x-source: aone-open`,含平台专属使用上报段(非通用,须移除)。
- 现支持 10 产品:`qoder-cli / qoder / qoderwork / qwen-code / oh-my-pi / kimi-code / codex-cli / codex-app / opencode / claude-code`。目标六家中 **claude-code / codex-cli / qoder-cli / opencode 已有适配器**;**copilot / hermes 无适配器,需新增**;`qoder(IDE)/ qoderwork / qwen-code / oh-my-pi / kimi-code / codex-app` 六项**移除**。
- 现产物形态:`<项目根>/.session-export/{tool}+{model}+{sessionId}.zip` 单 zip;本需求改为**目录**形态且名称由用户指定。
- 会话定位现有机制:`--verify`(用户最近一句内容跨工具重定位)、`--session <id>`、`--tool <name>` 自动识别优先级——保留并适配新形态。
- Copilot / Hermes 的会话落盘形态在本环境**未探测**(Hermes 为非 CLI 形态 Tier 2);其可导出性以实现期运行时探测为准,规格只约定行为契约(有源则导出、无源则诚实声明),不预设结论。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 当前会话被导出为用户命名的目录 (Priority: P1)

作为项目维护者,我执行 `/speckit.session export --name <名称>`,当前 AI agent CLI 会话的原始记录被导出到一个以我指定名称命名的目录中,使我可以按自己的命名体系归档、检索和转述会话,替代不可控的系统自动生成会话名。

**Why this priority**: 这是整个降级路线的落地主体——没有导出,命名与追溯都无从谈起。

**Independent Test**: 在当前 CLI 会话中执行导出,得到以指定名称命名的目录,内含该会话的原始记录文件;目录名即用户指定值。

**Acceptance Scenarios**:

1. **Given** 一个正在进行中的 CLI 会话,**When** 执行 `/speckit.session export --name arena-run-01`,**Then** 生成目录 `arena-run-01`(位于导出根下),内含该会话的主记录(jsonl 或该 CLI 的原生形态)、子代理日志与超大工具结果等原始内容(以该 CLI 实际落盘为准)。
2. **Given** 用户给出 `--session <id>` 显式会话 ID,**When** 执行导出,**Then** 导出该 ID 对应的会话而非自动识别的当前会话。
3. **Given** 用户给出 `--tool <name>` 显式工具,**When** 执行导出,**Then** 跳过自动识别直接在该工具的会话存储中定位。
4. **Given** 当前项目下没有匹配会话,**When** 执行导出,**Then** 明确报出"未找到会话"(沿用既有退出码语义),不产生半成品目录。
5. **Given** 同名导出目录已存在,**When** 再次以相同名称导出,**Then** 拒绝覆盖并报错,由用户换名或显式确认覆盖(不静默覆盖既有导出)。

### User Story 2 - 技能支持面收敛为恰好六家且通用化 (Priority: P1)

作为框架维护者,`export-session` 技能只支持六家 AI agent CLI(Claude Code / Codex CLI / Qoder CLI / GitHub Copilot / opencode / Hermes Agent),其余产品的适配代码与文档全部移除,技能不再绑定单一宿主平台(移除平台专属上报等外部依赖),成为任何受支持 AI agent CLI 下都可直接使用的通用技能。

**Why this priority**: 命令面(US1)委托技能执行;支持面不收敛,命令的"六家"承诺就是空话。与 US1 同为 P1,构成 MVP。

**Independent Test**: 技能源码与文档全文扫描——目标六家之外零残留;支持矩阵逐家可调用;在无原宿主平台环境(无平台专属命令/凭证)下技能可完整执行导出。

**Acceptance Scenarios**:

1. **Given** 改造后的技能源,**When** 全文扫描被移除产品(qoder IDE / qoderwork / qwen-code / oh-my-pi / kimi-code / codex-app)的标识,**Then** 零残留(代码、文档、示例、退出码表均不含)。
2. **Given** 六家支持矩阵,**When** 逐家执行导出(已安装者真跑,未安装者按声明缺席降级),**Then** 行为与支持矩阵一致;Copilot / Hermes 的落盘形态以实现期探测为准——有会话存储则导出,探测无源则诚实声明"该平台会话存储未探测到"并给出退出码,不臆造、不静默。
3. **Given** 技能在无 aone-open 平台环境的项目中运行,**When** 执行导出,**Then** 全流程不依赖任何平台专属命令(如使用上报),无网络调用、无外部凭证。
4. **Given** 既有能力(主记录 + 子代理日志 + 状态目录 + 超大工具结果 + 可提取 requestId 的 CLI 附带 request-ids),**When** 对保留的四家执行导出,**Then** 产物内容面不削弱(zip→目录的形态迁移不丢内容)。

### User Story 3 - 导出的会话附带描述文档 (Priority: P2)

作为会话的消费者(未来的自己、团队主管、评审者),导出目录内有一份**会话描述文档**,包含该会话的元信息(CLI、会话 ID、模型、时间窗、工作区等)与对会话内容的结构化总结(任务脉络、关键决策、产物清单),使我无需读完全部原始记录即可判断这个会话做了什么、值不值得深读。

**Why this priority**: 导出原始记录已可用(P1);描述文档是"可读性增值",缺失不阻塞导出本身。

**Independent Test**: 对一次真实导出的会话,打开描述文档:元信息字段与真实会话一致;结构化总结与原始记录内容相符(抽查对照)。

**Acceptance Scenarios**:

1. **Given** 一次成功导出,**When** 查看导出目录,**Then** 存在描述文档(固定文件名),含元信息节(CLI 工具、会话 ID、模型、起止时间、工作区路径、消息/轮次规模)与结构化总结节(任务脉络、关键决策、产物清单)。
2. **Given** 元信息由脚本从会话记录确定性提取,**When** 对照真实会话,**Then** 元信息逐字段一致(程序提取,不由模型臆测)。
3. **Given** 会话规模超出总结预算(过长 transcript),**When** 生成描述文档,**Then** 元信息完整,结构化总结降级为骨架并显式声明降级原因(不静默省略,不伪造总结)。
4. **Given** 结构化总结由 agent 在导出时读取原始记录生成,**When** 导出完成,**Then** 总结内容忠实于记录——不虚构未发生的决策与产物。

### User Story 4 - 团队 run 的派发会话可追溯 (Priority: P3)

作为团队主管,`/speckit.team run` 派发外部 CLI 成员产生的会话,可以在 run 结束后按派发 label 导出为用户命名目录,使 run report 的派发映射表(label → CLI → 成员)能进一步落到"会话原文 + 描述文档",完成从派发到会话的完整追溯链。

**Why this priority**: 消费场景扩展,依赖 US1–US3 全部就绪;追溯链的前两段(label 三元组 + 映射表)已就绪,本段是增值延伸。

**Independent Test**: 一次含外部派发的 run 结束后,按 label 命名导出派成员会话;run report 映射表与导出目录一一对应。

**Acceptance Scenarios**:

1. **Given** 一次含外部 CLI 派发的 run,**When** 以派发 label 作为 `--name` 导出该派成员的会话,**Then** 导出目录名与 label 一致,可被 run report 映射表引用。
2. **Given** 派成员会话仍在运行(未结束),**When** 导出,**Then** 按"截至当前"语义导出已有记录并声明快照时点(不因会话未结束而失败)。

### Edge Cases

- **会话定位歧义**:自动识别命中多个候选会话时,沿用既有 `--verify`(用户最近一句内容)机制消歧;仍无法确定时报错并提示 `--session` 显式指定,不猜。
- **运行中会话导出**:主记录仍在写入——导出取截至当前的快照,描述文档声明快照时点。
- **目录名非法或含路径分隔符**:导出目录名 MUST 是安全路径段(首字符字母/数字,其余 `[A-Za-z0-9_.-]`);越界即拒。
- **目标工具未安装或无会话存储**:明确声明该平台不可导出(区分"未安装"与"安装了但无会话落盘"),不产生空目录。
- **原始记录含敏感内容**:导出是原文复制,描述文档 MUST NOT 额外扩散敏感内容;导出目录落在项目内由用户自管(不改 `.gitignore`、不代用户决定入库与否)。
- **大文件**:超大工具结果沿用既有分段/段日志机制迁移到目录形态,不因体积静默丢弃。

## Requirements *(mandatory)*

### Functional Requirements

**命令面(/speckit.session)**

- **FR-001**: MUST 提供 `/speckit.session` 命令,首版含 `export` 子命令;命令模板经 `templates/commands/` 单一事实源扇出至既有 per-tool 副本(不新增工具表面)。
- **FR-002**: `export` MUST 接受用户指定的目录名称(`--name`);名称文法为安全路径段(同 goal 身份文法);未提供 `--name` 时 MUST 要求补给(不自动生成名称——命名是本需求的目的本身)。
- **FR-003**: `export` MUST 支持 `--session <id>`(显式会话 ID)与 `--tool <name>`(显式工具)参数;缺省时自动识别当前工具与会话,沿用 `--verify` 跨工具重定位机制。
- **FR-004**: 命令 MUST 遵循 preview → confirm → execute 门禁:导出前披露(工具、会话 ID、目标目录路径、预估规模),确认后方执行;执行委托 `export-session` 技能,命令自身不重复实现导出逻辑。
- **FR-005**: 同名导出目录已存在时 MUST 拒绝默认路径,并在 preview 门禁内**交互式确认**后方可覆盖(覆盖即先清空该目录再写入,不残留旧文件);不提供 `--force` 类旁路标志——覆盖是显式的人的决策,非交互场景下同名重导直接失败并提示换名。

**技能面(export-session 改造)**

- **FR-006**: 技能支持面 MUST 收敛为恰好六家:Claude Code / Codex CLI / Qoder CLI / GitHub Copilot / opencode / Hermes Agent;其余产品(qoder IDE / qoderwork / qwen-code / oh-my-pi / kimi-code / codex-app)的适配代码与文档 MUST 全部移除,全文零残留。
- **FR-007**: 技能 MUST 改造为通用 Spec Kit 技能:移除平台专属依赖(aone-open 使用上报、宿主专属路径探测中的平台私有项),保留跨平台解释器探测纪律;无网络调用、无外部凭证。
- **FR-008**: 产物形态 MUST 从单 zip 改为**目录**:导出根下以用户名称命名的目录,内含该会话全部原始记录(主记录、子代理日志、状态目录与段日志、超大工具结果);可提取 requestId 的 CLI 附带 request-ids 文件置于目录内。
- **FR-009**: 会话定位机制(自动识别优先级、`--verify` 重定位、`--session`/`--tool` 显式指定)MUST 保留并适配目录形态;退出码语义(0 成功 / 2 参数无效 / 3 未找到会话 / 4 前置失败 / 5 IO 错)MUST 保持。
- **FR-010**: Copilot / Hermes 的会话存储形态 MUST 以实现期运行时探测为准:探测到有落盘 → 实现适配器;探测无源 → 在支持矩阵中声明"未探测到会话存储"并给出诚实的不可导出提示;MUST NOT 臆造适配器行为。
- **FR-011**: 对保留四家(claude-code / codex-cli / qoder-cli / opencode),既有产物内容面(主记录 + 子代理日志 + 状态 + 大结果 + requestId)MUST 不削弱。

**描述文档面**

- **FR-012**: 每次成功导出 MUST 在导出目录内生成会话描述文档(固定文件名),含两节:**元信息**(CLI 工具、会话 ID、模型、起止时间、工作区路径、规模计数——全部由脚本从原始记录确定性提取)与**结构化总结**(任务脉络、关键决策、产物清单)。
- **FR-013**: 结构化总结 MUST 由执行导出的 agent 读取原始记录后生成,忠实于记录;**预算由程序判定**:原始记录规模(行数与字节数双阈值,常量化,具体数值由计划阶段冻结)超限时 MUST 降级为骨架总结并显式声明降级原因与触发阈值;MUST NOT 虚构未发生的决策与产物。
- **FR-014**: 描述文档 MUST NOT 包含原始记录之外的新事实来源;其每一节可追溯至原始记录(元信息字段对应记录字段,总结对应记录内容)。

**集成面**

- **FR-015**: `/speckit.team` run 的外部派发追溯 MUST 可衔接:以派发 label 作为 `--name` 导出派成员会话为合法用法;运行中会话按"截至当前"快照导出并声明时点。
- **FR-016**: 导出 MUST NOT 修改宿主 CLI 的任何会话存储(只读取);MUST NOT 改 `.gitignore`(导出目录入库与否由用户自管)。

### Key Entities *(include if requirement involves data)*

- **导出目录(Export Bundle)**:用户命名的一次会话导出——目录,内含原始记录文件集合 + request-ids(如可提取)+ 描述文档;身份 = 导出根下的目录名。
- **会话描述文档(Session Description)**:导出目录内的固定文件名文档;元信息节(确定性提取)+ 结构化总结节(agent 生成,可降级)。
- **支持矩阵(Support Matrix)**:恰好六家的工具 → 会话存储形态 → 可导出性映射;实现期探测填充,探测无源显式声明。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 对已安装的目标 CLI,`/speckit.session export --name <名称>` 成功生成以该名称命名的目录,内含会话原始记录与描述文档;六家支持矩阵逐家行为与声明一致(可导出者真跑通过,无源者诚实声明),矩阵外产品零残留(全文扫描 0 处)。
- **SC-002**: 描述文档元信息与真实会话逐字段一致(程序提取,抽查 100% 相符);结构化总结忠实于记录(抽查对照无虚构)。
- **SC-003**: 既有定位能力不回归:`--verify` 消歧、`--session`/`--tool` 显式定位在保留四家上行为与改造前一致;退出码语义五值不变。
- **SC-004**: 通用化验证:在无平台专属命令/凭证的干净环境下,技能完整执行导出成功;技能全文无平台专属依赖残留(扫描 0 处)。
- **SC-005**: 导出对宿主会话存储零写入(只读);同名目录冲突 100% 拒绝(无静默覆盖)。
- **SC-006**: 团队 run 追溯链闭合:以派发 label 命名的导出目录可与 run report 映射表一一对应(US4 场景演练通过)。

### Measurement Sources & Collection Methods

- **SC-001 Source**: 集成测试——逐家构造/探测会话存储夹具执行导出,断言目录名与内容面;全文扫描断言被移除产品标识计数为 0。
- **SC-002 Source**: 真实会话导出后人工抽查 + 契约测试(元信息字段与记录字段对照)。
- **SC-003 Source**: 改造前后同夹具回归对比(定位/退出码逐项)。
- **SC-004 Source**: 干净环境(或模拟剥离平台命令)真跑 + 依赖扫描。
- **SC-005 Source**: 集成测试断言会话存储文件字节不变(mtime/hash 前后一致);同名冲突用例。
- **SC-006 Source**: US4 场景端到端演练记录。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| ID | 字符串 | 说明 |
|----|--------|------|
| STR-001 | `.session-export/` | 导出根目录(项目根下) |
| STR-002 | `claude-code / codex-cli / qoder-cli / copilot / opencode / hermes` | 支持矩阵六家的规范工具名(命令 `--tool` 取值) |
| STR-003 | `session-export:<tool>/<session-id>` | 描述文档内的会话标识行格式 |

## Out of Scope

- 对 session 本身重命名/改名(宿主无机制,已被导出侧命名替代)。
- Spec Kit 记忆会话层(`.specify/memory/session/`)——不同概念,不涉及。
- 六家之外任何产品的支持(含既有但被移除的六项)。
- 导出目录的入库策略(是否 git 跟踪由用户自管)、压缩/上传/分享形态(首版只出目录)。
- 会话内容的隐私脱敏(导出为原文复制;脱敏若未来需要属独立需求)。
- 宿主的 resume/continue 行为变更——导出只读,不影响会话本身。

## Assumptions

- 六家 CLI 的会话存储位置与形态以实现期运行时探测为准(其中 claude-code / codex-cli / qoder-cli / opencode 已有被验证的适配器;copilot / hermes 待探测)。
- 描述文档的结构化总结在执行导出的 agent 上下文内生成,预算受限时按 FR-013 降级。
- 导出目录默认落在项目根 `.session-export/` 下(沿用现有导出根);`--name` 只命名子目录。
- 本需求不改变 `/speckit.team` 的派发机制本身,只在其下游提供会话导出衔接。

## Clarifications

### Session 2026-08-12

- Q: 本需求绑定既有 Feature 还是新建? → A: **新建 Feature 043「Session Export」**(Draft)。导出 + 导出侧命名 + 描述文档是独立一等能力;与 022 AI Tools Support / 026 Agent Skill Enablement 是消费关系而非组成关系,不绑定。
- Q: FR-013「会话规模超出总结预算」如何判定? → A: **程序判定阈值**——行数与字节数双阈值(常量化,计划阶段冻结数值),超限即元信息完整 + 骨架总结 + 声明降级原因;降级行为契约可测(程序优先原则)。
- Q: 同名导出目录已存在时「显式确认覆盖」用什么机制? → A: **交互式确认**——preview 门禁内再次确认后方可覆盖(先清空再写入);不设 `--force` 旁路标志,非交互场景同名重导直接失败并提示换名(覆盖是显式的人的决策)。
