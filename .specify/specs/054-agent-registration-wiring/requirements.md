# Requirements Specification: Agent 定义到宿主注册面的接线(Agent Registration Wiring)

**Requirement Branch**: `054-agent-registration-wiring`  
**Created**: 2026-10-08  
**Status**: Draft  
**Input**: User description: "agent 定义到宿主注册面的链路断裂（三处断点 + Qoder IDE 缺适配）：渲染器 load_project_agent_definitions 只读 .specify/agents/{templates,instances}/，而 create-agent 的 capacity 类与 create-team 的 8 个 stage/orchestration 帧无任何安装步骤（实测 instances/ 为空、.qoder/agents/ 仅 2 个出厂类型）；render_agents_for_tool 只从 specify CLI 内部可达，无任何 /speckit.* 命令或脚本能触发渲染；templates/commands/agents.md:25 仍教已退役的 symlink 模型（F-A02 死信复发，已扩散至命令模板）；Qoder IDE 的 agent 面无适配也无文档。设计裁定三选一（spec 须迫使选择而非重新推导）：(a) specify init/refresh 安装帧与 capacity 类进 .specify/agents/templates/；(b) create-team 建队时经 create-agent 实例化实际用到的席位；(c) 承认席位永不可原生派发，加 seat_kind 判别字段并撤回 create-mode.md:128 的 broken-references 承诺。输入见 .specify/memory/feedback/backlog.md 两条 2026-10-07 行。"

## Related Feature *(mandatory)*

**Feature ID**: Need clarification  
**Feature Name**: Need clarification

## Overview

### 现状锚点(以源码与官方文档实测为准,2026-10-08)

本特性修复「用户在 speckit 框架中定义的 agent 能力 —— 无论团队席位还是独立 agent —— 到不了宿主可派发注册面」的链路断裂。调查源头为 backlog.md 两条 2026-10-07 行;以下每一条本轮起草时均已重新实测:

- **渲染链本体(完好段)**:`load_project_agent_definitions`(`src/specify_cli/__init__.py:310`)只读 `.specify/agents/templates/` 与 `instances/`(同名时 instance 优先),逐文件校验中性元数据契约;`render_agents_for_tool`(`:615`,docstring 明写「Real files only (no symlinks)」——含 drift 检测、陈旧产物修剪、legacy 符号链接替换迁移)把定义渲染为宿主真文件。qoder 行 `fields` 映射覆盖 `name`/`description`/`model-tier→model`/`capability-tools→tools`/`skills`/`run-turn-budget→maxTurns`/`display-color→color`,`provenance` 已钉官方文档 URL。渲染模式工具共 4 个:qoder、claude、copilot、opencode(codex/hermes 为 annotated 模式)。
- **断点 1(可达性)**:框架的 agent **类**另存两处且无任何安装步骤 —— `skills/create-agent/templates/`(7 个 capacity 类 + 4 个其他模板)与 `skills/create-team/templates/agents/`(7 个 stage/orchestration 帧 + 1 个 workflow schema);全仓对席位模板名的引用只有 `__init__.py:135` 一条注释与 `agent-definitions.md` taxonomy 表的一行,无安装代码。实测:`.specify/agents/instances/` 为空、`templates/` 仅出厂 2 件(skill-verifier、structure-adjuster),故 `.qoder/agents/` 同样只有这 2 个原生类型。
- **断点 2(触发面)**:`render_agents_for_tool` 全仓唯一调用点是 `:2283`(specify CLI 的 init/update 流程);对 `templates/commands/*.md` 与 `scripts/python/*.py` 的 `grep -rn` 零命中 —— 没有任何 `/speckit.*` 命令或项目脚本能触发渲染,也没有任何文档告知「create-agent 之后须经一次 specify CLI 运行才能上宿主面」。
- **断点 3(教学面)**:已退役的 per-file 符号链接模型仍被三个面教授 —— `templates/commands/agents.md:25`(「Tool-specific directories are symlinks — never write to them directly」)、`skills/create-agent/SKILL.md:122` 表行(「Per-file symlinked into every officially supported tool's agent config directory on initialization (FR-010/012)」)与 `:127` 段落(详述 CLI 建立逐文件符号链接)。这是 **F-A02 死信**:2026-09-11 分流 improve-skills 从未执行,跨 ≥3 轮 consume,已从技能扩散进命令模板。同时 `templates/commands/agents.md:72` 要求派发「with its configured `capability-tools`, `model-tier`, and `run-turn-budget`, and system prompt」—— 四样只有宿主已注册类型携带得动,未注册即必然退化为 `general-purpose` 通用载体 + 角色散文注入简报。
- **Qoder IDE 侧(本轮已官方取证,原悬念解除)**:Qoder IDE 与 Qoder CLI **共享同一项目级 agent 目录** `.qoder/agents/`——IDE 读 `${project}/.qoder/agents/<name>.md`(另有用户级 `~/.qoder/agents/`),CLI 读 `.qoder/agents/*.md`,官方 CLI 文档明写「The path `.qoder/agents/` is shared between Qoder CLI and the Qoder IDE」;文件名不决定 agent 名(名字来自 frontmatter `name` 字段);CLI 侧另支持 `permissionMode`/`disallowedTools`/`timeoutMins`/`isolation` 等字段。来源:`https://docs.qoder.com/extensions/subagent`(IDE 页)与 `https://docs.qoder.com/cli/subagent`(CLI 页),取证日期 2026-10-08。backlog 50 行「取证前 MUST NOT 假定 IDE 与 CLI 同路径」的门槛由此满足:**同路径是已验证事实,不是假设**。
- **一条既有硬约束(裁定前约束选项 (a),方案 (b) 天然满足)**:渲染器对带未解析 `{{PLACEHOLDER}}` 的定义**直接拒绝**(`:303-307`,「authoring templates must not enter the render input」)。stage 帧与 capacity 类恰恰是带占位符的作者模板 —— 方案 (b) 在建队实例化时填掉占位符,产出可入渲染输入的实例;方案 (a) 的「安装原始帧」则与该不变量直接冲突。

净效应:编排者派发团队席位或任何未注册角色时,唯一可用的原生载体是 `general-purpose`,定义里声明的工具面、模型档、回合预算全部丢失;使用者从历史记录观察到「永远只有 general-purpose 子代理」。

### Assumptions

- **设计裁定已落定**:断点 1+2 采用方案 (b) —— `create-team` 建队时经 `create-agent` 把实际用到的席位实例化到 `.specify/agents/instances/`(2026-10-08 用户于本 spec 起草流程裁定,理由见 FR-007 与 ## Clarifications);本 spec 其余部分按裁定后形态书写,plan 阶段直接实现、不再重新推导。
- **qoder 字段映射不在范围**:`run-turn-budget→maxTurns` 等映射已完备,本特性不触碰 `_AGENT_METADATA_MAPPING` 的字段面。
- **F-03 的 validate-team-md.py 是相邻件**:backlog 42 行的校验器(标题唯一性、引用断裂、文件计数)归该行所有,本 spec 只要求「create-mode.md:128 的承诺在本特性落地后可判定」,不吸收校验器本体。
- **两层既有语义不变**:instance 优先于 template、渲染 manifest 的备份/修剪/迁移语义、`.specify/agents/execution/` 运行时产物边界,均沿用现状。
- **渲染面 = 4 个渲染模式工具**:qoder/claude/copilot/opencode;codex/hermes(annotated 模式)与无 agent 机制的工具不在本特性范围。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 三个教学面改教真实渲染机制,F-A02 死信终结 (Priority: P1)

使用者(或代理)今天读 `templates/commands/agents.md` 与 `skills/create-agent/SKILL.md` 学到的是已退役的 per-file 符号链接模型,而渲染器实际行为是「真文件渲染、替换 legacy 链接」。本故事把三个教学面(agents.md:25、SKILL.md:122、SKILL.md:127)全部改为与真实机制一致:宿主 agent 目录是渲染产出的真实文件、由 specify CLI 渲染、legacy 符号链接被替换;同时在 create 流程终点教授触发真相 —— 定义落在 `.specify/agents/{templates,instances}/`,上宿主注册面需要一次渲染触发。

**Why this priority**: 三项里最便宜、零设计依赖、且死信已在 ≥3 轮 consume 中复发并从一个面扩散到三个面 —— 每多存活一天就可能再扩散一个面;同时它是纯文档/模板修正,不阻塞也不被阻塞于设计裁定。

**Independent Test**: 对三个面 grep 退役表述(per-file 符号链接模型的教学句)应零命中(历史档案类文件除外);以变异演练把任一面改回旧表述,契约测试必须转红。

**Acceptance Scenarios**:

1. **Given** 三个教学面已修正,**When** 全仓 grep 退役表述,**Then** 除历史记录(feedback/history/consume-log 等档案)外零命中。
2. **Given** 使用者走完 `/speckit.agents create` 流程,**When** 阅读该流程终点的命令/技能文本,**Then** 能得知:定义落在 `.specify/agents/{templates,instances}/`,以及上宿主面的触发步骤(与当时已落地的触发面一致;若 US2 未落地,则如实教授现行的「跑一次 specify CLI init/update」)。
3. **Given** 变异守卫已接好,**When** 任一教学面回退为符号链接表述,**Then** 契约测试转红。
4. **Given** 三个面均已修正,**When** 复核 backlog 的 F-A02 行,**Then** 该死信具备核销条件(修正落地 + 守卫钉住)。

---

### User Story 2 - 建队即实例化:席位与独立 agent 定义到达宿主注册面,派发携带真实容量 (Priority: P1)

使用者经 `/speckit.team create` 建立了一个引用 stage 帧的团队,或经 `/speckit.agents create` 产生了一个持久 agent 定义;今天这条定义到不了任何渲染模式工具的宿主注册面,编排者派发时只能用 `general-purpose` 载体 + 散文注入。本故事按已裁定的方案 (b) 闭合断点 1+2:`create-team` 建队时经 `create-agent` 把 team.md 实际用到的每个席位实例化到 `.specify/agents/instances/`,使「定义 → 中性层 → 渲染触发 → 宿主注册面」整条链可达,派发时席位以自己的注册类型出现,携带其 `capability-tools`、`model-tier`、`run-turn-budget` 与 system prompt。

**Why this priority**: 这是本特性的核心损失所在 —— 框架定义的 agent 能力(无论 team 席位还是独立 agent)实际不可原生派发,观察面上的「永远只有 general-purpose」正是其症状。与 US1 同为 P1;设计裁定已在本 spec 起草时由用户落定(选 b),plan 阶段直接实现。

**Independent Test**: 在一个演示项目里建一个引用 stage 帧的团队,确认每个被引用席位已实例化(`.specify/agents/instances/` 出现对应文件且占位符已填、带所属团队来源追溯),再走文档所述渲染触发,断言 4 个渲染模式工具的宿主 agent 目录出现该席位的注册类型;对经 `/speckit.agents create` 产生的持久定义重复同样的注册面断言。

**Acceptance Scenarios**:

1. **Given** 一个 team.md `agent:` 字段引用 stage 帧的团队经 `/speckit.team create` 建立,**When** 建队流程完成,**Then** 每个被引用的席位已实例化为 `.specify/agents/instances/` 下的定义(占位符全部解析),且经文档所述渲染触发后,4 个渲染模式工具的宿主注册面出现该席位的注册类型。
2. **Given** 席位已上注册面,**When** 编排者派发该席位,**Then** 派发以其注册类型进行,`capability-tools`/`model-tier`/`run-turn-budget` 与 system prompt 由注册类型承载(如 `.qoder/agents/` 产物的 frontmatter 所示),而非 `general-purpose` + 散文注入。
3. **Given** 任一带未解析 `{{PLACEHOLDER}}` 的作者模板,**When** 它将进入渲染输入,**Then** 渲染器拒绝并点名(既有不变量保持)。
4. **Given** 由建队流程实例化的席位实例,**When** 检查其实例文件,**Then** 其携带可机读的所属团队来源追溯,使团队解散后的孤儿实例可被检测。
5. **Given** 建队前 `.specify/agents/instances/` 为空,**When** `/speckit.team create` 完成,**Then** 只实例化该团队实际用到的席位 —— 未被引用的帧与 capacity 类不被安装。

---

### User Story 3 - Qoder IDE 与 CLI 的 agent 面关系有文档 (Priority: P2)

使用者想知道「Qoder IDE 能不能看到我渲染出的 agent」,今天没有任何文档回答 —— `symlink-model.md` 为**指令**面建立了 CLI/IDE 二分,agent 面却无对应条目。本特性起草时已官方取证(见 Overview):两 IDE 与 CLI 共享项目级 `.qoder/agents/`。本故事把这个已验证事实写进 owner 文档,并钉上取证来源。

**Why this priority**: 取证已完成,剩下的是文档级落地 —— 便宜但不阻塞核心链路,且其答案(共享路径)意味着**无需**给 `_AGENT_METADATA_MAPPING` 增 IDE 行,方案面因此收窄。

**Independent Test**: 读 `shared/workflow/symlink-model.md` 与 `docs/reference/cli/supported-agent-tools.md`,agent 面的 CLI/IDE 关系陈述存在、与取证事实一致、标注来源 URL。

**Acceptance Scenarios**:

1. **Given** `symlink-model.md` 已增补,**When** 阅读其 agent 面条目,**Then** 陈述为:Qoder IDE 与 CLI 共享项目级 `.qoder/agents/`,IDE 另有用户级 `~/.qoder/agents/`(框架不触碰),并标注官方文档来源与取证日期。
2. **Given** `docs/reference/cli/supported-agent-tools.md` 已更新,**When** 查 qoder 工具条目,**Then** 其 agent 面说明包含共享路径与用户级作用域的边界陈述。
3. **Given** 官方文档未来变化,**When** 复核 provenance URL,**Then** 文档中的陈述可追溯到来源(不依赖记忆)。

---

### User Story 4 - 链路有漂移守卫,回退即转红 (Priority: P2)

三个断点今天没有任何测试看守:教学面回退不会红,注册链断裂不会红,IDE 关系文档失实不会红。本故事按仓库既有三面纪律(owner 文档 → 执行面 → 契约测试)为 US1–US3 落地的内容补契约测试,且每个守卫自带变异演练取证。

**Why this priority**: 守卫必须在被守内容落地后成形,排序天然靠后;但没有守卫,本特性修好的三处会以 F-A02 同样的方式死信复发。

**Independent Test**: 对每个守卫执行变异演练:植错一字 → 断言转红 → 精确复原 → `diff -q` 字节相等。

**Acceptance Scenarios**:

1. **Given** 教学面守卫,**When** 把任一教学面改回 [[STR-001]] 的退役表述,**Then** 契约测试转红。
2. **Given** 链路守卫(按 FR-007 裁定形态),**When** 链路任一环断开(渲染不可达 / 席位未上注册面 / 判别声明缺失),**Then** 对应契约测试转红。
3. **Given** 任一守卫,**When** 执行变异演练(植错一字 → 红 → 复原),**Then** 断言先红后绿且复原后与原文件字节相等 —— 无变异演练取证的守卫视为未交付。

---

### Edge Cases

- 建队实例化时占位符未填全 → 渲染器拒绝(`:303-307` 既有行为);实例化步骤 MUST 产出占位符全部解析的实例(FR-006)。
- **(b) 落地前已存在的团队**(team.md 引用未实例化的 stage 帧)→ 其成员不自动可解析;是否提供刷新/重建路径补实例化由 plan 阶段裁定,本 spec 不强制回填(存量团队仍按现行 general-purpose 载体派发,与现状一致)。
- 团队解散/退役后的席位实例成为孤儿 → FR-013 的来源追溯使其可检测;清理形态由 plan 决定。
- 实例与模板同名 slug 冲突 → instance 优先(既有语义,不因本特性改变);建队实例化遇到与既有持久定义同名时 MUST 冲突披露而非静默覆写。
- 用户手改渲染产物(如直接编辑 `.qoder/agents/` 文件)→ 渲染 manifest 备份后覆写(既有语义);守卫不得把用户资产当作待修复漂移。
- 并发会话同时在写 `.specify/agents/` → 实例化步骤须沿用「写入时现查」纪律(同 feature 编号分配的防碰撞做法)。
- IDE 用户级 `~/.qoder/agents/` 存在与项目级同名的 agent → 优先级属宿主行为;框架只管理项目级,文档须说明该边界,守卫不跨作用域断言。
- `.qoder/agents/` 中存在非框架产出的第三方 agent(用户自装)→ 渲染只修剪自己 manifest 记录的陈旧产物,不动用户资产(既有语义,守卫覆盖)。

## Requirements *(mandatory)*

### Functional Requirements

#### 教学面修正(US1)

- **FR-001**: `templates/commands/agents.md` MUST 描述真实渲染模型 —— 宿主 agent 目录是渲染产出的真实文件、由 specify CLI 渲染、legacy 符号链接被替换 —— 且 MUST NOT 再教授 per-file 符号链接模型([[STR-001]] 所示的退役表述 MUST 被移除)。
- **FR-002**: `skills/create-agent/SKILL.md` 的持久化说明(现 :122 表行与 :127 段落)MUST 同步修正,其引用的初始化行为陈述 MUST 与渲染器实际语义一致。
- **FR-003**: 在 create 流程的终点(agents 命令模板与 create-agent 技能),触发真相 MUST 被教授:定义落 `.specify/agents/{templates,instances}/`,上宿主注册面须经渲染触发;所教触发步骤 MUST 与当时已落地的触发面一致。

#### 注册链闭合(US2,方案 (b) 已裁定)

- **FR-004**: `create-team` 建队流程 MUST 经 `create-agent` 把 team.md `agent:` 字段实际引用的每个席位实例化到 `.specify/agents/instances/`;经 `/speckit.agents create` 产生的持久定义天然落中性层,无需额外步骤。建队流程的终点 MUST 使使用者得知(或直接执行)使实例到达宿主注册面所需的渲染触发步骤。
- **FR-005**: 闭合后的派发 MUST 保留 `templates/commands/agents.md` 既有派发要求所列容量 —— `capability-tools`、`model-tier`、`run-turn-budget` 与 system prompt 由宿主注册类型承载,而非散文注入。
- **FR-006**: 带未解析 `{{PLACEHOLDER}}` 的作者模板 MUST NOT 进入渲染输入(既有不变量);建队实例化路径 MUST 产出占位符全部解析的实例(方案 (b) 天然满足)。
- **FR-007**: 断点 1+2 的修法采用方案 (b)(2026-10-08 用户裁定):`create-team` 建队时经 `create-agent` 实例化实际用到的席位,不采用 (a) 的 init 预安装、也不采用 (c) 的判别降级。裁定理由:与三层分类法自带的 Template→Instance 转化链一致;占位符在建队时被填掉,天然满足渲染器对作者模板的拒绝不变量;只实例化实际用到的席位,不向每个项目预装全部帧与 capacity 类。

#### 引用可判定(US2)

- **FR-008**: 建队流程完成后,team.md 的每个 `agent:` 成员 MUST 可解析到 `.specify/agents/{templates,instances}/<slug>.agent.md`(席位经 FR-004 实例化);由此 `create-mode.md` 的「unresolved members are surfaced as broken references」承诺变为可判定 —— 不可解析的成员即真断裂,两类工件(注册定义 vs stage 帧)共用一字段的歧义在建队路径上消除。create-mode.md 的 schema notes MUST 相应更新(成员引用的合法形态 = 注册定义或建队时实例化的席位)。

#### IDE 关系文档(US3)

- **FR-009**: `shared/workflow/symlink-model.md` MUST 增补 agent 面的 CLI/IDE 关系陈述,内容与已验证事实一致(Qoder IDE 与 CLI 共享项目级 `.qoder/agents/`,IDE 另有用户级作用域),并标注官方文档来源与取证日期。
- **FR-010**: `docs/reference/cli/supported-agent-tools.md` MUST 为 qoder 条目补 agent 面说明:共享路径、文件名不决定 agent 名(frontmatter `name` 为准)、用户级作用域的边界。

#### 漂移守卫(US4)

- **FR-011**: MUST 有契约测试钉住教学面:任一教学面回退为 [[STR-001]] 的退役表述即转红。
- **FR-012**: MUST 有契约测试钉住链路闭合:断言「建队 → 席位实例化(`.specify/agents/instances/` 出现占位符已填的席位定义)→ 渲染触发 → 宿主注册面出现席位类型」;守卫 MUST 附变异演练取证(植错一字 → 红 → 精确复原 → 字节相等)。
- **FR-013**: 由建队流程实例化的席位实例 MUST 携带可机读的所属团队来源追溯,使团队解散/退役后的孤儿实例可被检测;检测与清理的执行形态由 plan 阶段决定。

### Key Entities *(include if requirement involves data)*

- **Agent Template / Agent Instance / Agent Execution**: 三层分类法由 `.specify/shared/definitions/agent-definitions.md` 拥有(词汇表已确认),本 spec 引用不重定义。
- **席位实例 (seat instance)**: Agent Instance 的一种 —— 由 `create-team` 建队流程从 stage 帧实例化而来,携带所属团队来源追溯(FR-013);分类法归属 agent-definitions.md。
- **宿主注册面 (host registration surface)**: **新概念** —— 某工具实际读取 agent 定义的目录(如 qoder 的项目级 `.qoder/agents/`,CLI 与 IDE 共享),渲染的目标面;现无 owner,建议 plan 阶段归入 agent-definitions.md 或 symlink-model.md。
- **渲染清单 (render manifest)**: 既有机制(`.render-manifest.json`),drift 检测/备份/修剪语义由渲染器 docstring 拥有,本特性沿用。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 教学三面零处教授已退役的 per-file 符号链接模型 —— grep 断言由契约测试钉住(基线:agents.md:25、SKILL.md:122、SKILL.md:127 三处)。
- **SC-002**: 「建一个引用 stage 帧的团队 → 走文档所述渲染触发 → 派发该席位」的端到端演示中,席位以其注册类型被派发(占位符已填、容量由注册类型承载),`general-purpose` 通用载体不再是席位派发的必需路径。
- **SC-003**: 修复后渲染模式工具的宿主 agent 目录内容与 `.specify/agents/{templates,instances}/` 的持久定义集一一对应(渲染产物 = 定义集的投影),抽样核对无「定义存在而注册面缺失」项。
- **SC-004**: F-A02 死信(backlog 2026-10-07 行)在验收时具备核销条件:三个面的修正均已落地、各有守卫钉住、核销动作可在 feedback 台账留痕。

### Measurement Sources & Collection Methods

- **SC-001 Source**: 契约测试(FR-011)对教学三面的 grep 断言 + 变异演练记录;基线三处,验收时零处。
- **SC-002 Source**: 端到端演示项目(或本仓 dogfooding 团队)的宿主 agent 目录清单 + 派发记录(如 run report 的席位派发面),对照 FR-007 裁定形态。
- **SC-003 Source**: `.specify/agents/{templates,instances}/` 与 `.qoder/agents/` 的目录对照脚本(可复用渲染器 stats 输出),抽样断言。
- **SC-004 Source**: feedback 台账的核销记录与 backlog 行状态;契约测试全绿。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "Tool-specific directories are symlinks — never write to them directly" | FR-001(否定面)、FR-011(守卫的禁用子串) |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

- Q: 断点 1+2 的修法选 (a) init 安装、(b) create-team 实例化、还是 (c) seat_kind 判别 + 撤回承诺? → A: **(b) create-team 建队时经 create-agent 实例化实际用到的席位**(2026-10-08,用户于本 spec 起草流程裁定;理由记录于 FR-007)。
