# Requirements Specification: 预置 Agent 定义的元信息中立化与按工具渲染分发

**Requirement Branch**: `040-agent-metadata-portability`  
**Created**: 2026-08-13  
**Status**: Draft  
**Input**: User description: "需要彻底优化一下./agents目录中的预置的agent定义, 需要明确的将agent定义中的元信息和对于agent自身的信息分离出来,另外元信息使用一个更通用的方式组织而不是针对特定的agent工具(如qoder),在init命令进行分发的时候在将元数据转换为对应目标工具的格式,比如执行specify init "${project_name}" --ai qoder的时候在将agent定义的元数据转为qoder支持的格式,然后输出到.qoder/agents/*.agent.md文件中(取消当前的软链接模式). 最后需要明确skills/create-agent/templates目录,skills/create-team/templates/agents目录和./agents目录中所定义的agent的差别."

## Related Feature *(mandatory)*

**Feature ID**: 044  
**Feature Name**: Agent Metadata Portability

## Overview

预置 agent 定义当前把三件事压在同一个文件的同一段 frontmatter 里:框架自身需要的装配信息、某一家 agent CLI 工具(Qoder)才认识的运行参数、以及 agent "是谁、做什么" 的正文。结果是:元信息与正文没有边界、元信息带着一家工具的方言、分发靠软链接把同一份 Qoder 味道的文件塞给所有工具。本需求把元信息抽成工具中立的一层,在 `specify init --ai <tool>` 时把它渲染成目标工具支持的真实文件,并顺带把三个"看起来都在放 agent"的目录之间的差别定义清楚。

### 现状锚点(以源码实测为准)

- **预置 agent**: `agents/*.agent.md` 共 7 个角色(requirements-analyst、ux-analyst、system-designer、module-designer、test-engineer、qa-engineer、knowledge-manager),全部为无占位符的可直接运行定义。
- **frontmatter 键集 7 个文件完全一致**,共 11 键:`name`、`description`、`user-invocable`、`disable-model-invocation`、`supervisor`、`capacity-scope`、`model`、`tools`、`skills`、`maxTurns`、`color`;文件间只有取值差异(`tools`/`skills`/`maxTurns` 取 10/12/15/25 /`color`)。
- **工具方言已渗入**: `docs/reference/agents/templates-and-agents.md:80-83` 明确把 `model`/`tools`/`maxTurns`/`color` 称作 "Qoder-compatible fields",并列出 7 个"可用但默认不设"的 Qoder 字段(`disallowedTools`、`timeoutMins`、`skills`、`mcpServers`、`permissionMode`、`background`、`isolation`);同文件另有 `## Qoder expert crosswalk` 小节。命名风格也混杂:框架键用 kebab-case,`maxTurns` 用 Qoder 的 camelCase。
- **两个契约测试直接以工具命名断言**: `tests/contract/test_shipped_agent_presets.py` 的 `test_preset_has_qoder_frontmatter`、`tests/contract/test_role_templates.py:68` 的 `test_template_has_qoder_frontmatter`(断言 `model`/`tools`/`maxTurns` 存在)。
- **分发为逐文件软链接、无任何转换**: `src/specify_cli/__init__.py:1512-1525` 把 `agents/` 原样 `copytree` 到 `.specify/agents/templates/`;`:1599-1617` 的 `_AGENT_LINK_DIRS = {copilot: .github, claude: .github, qoder: .qoder, opencode: .opencode, hermes: .hermes}` 再调 `ensure_per_file_agent_links()`(`:1136-1191`),把 `.specify/agents/{templates,instances}/*.agent.md` 逐个建成相对软链接;实测 `.qoder/agents/*.agent.md -> ../../.specify/agents/templates/*.agent.md`。
- **该链接函数已承载的语义**(改造须保住):instance 同名压过 template、清理失效链接、把真实文件视为工具侧 override 而保留、迁移历史上的整目录软链接。
- **覆盖面缺口**: `codex` 不在 `_AGENT_LINK_DIRS` 中,完全不发 agent;`claude` 被映射到 `.github` 而非 `.claude`。
- **本仓库没有任何"每工具 agent frontmatter 格式"文档**: `docs/reference/cli/` 下六个工具参考文档均不描述 agent/subagent 字段;唯一成文的格式是那份 Qoder 口味的基线。历史依据见 `docs/reference/history/01-agent-system-evolution.md:18`("Claude Code 的 subagent 格式兼容 VS Code Copilot custom agent 规范"),这正是当初用软链接桥接、不做每工具副本的理由。
- **三个目录的实际形态**(2026-08-13 第二轮澄清已裁定改造方向,见 FR-023:7 个角色定义迁往 Worker 能力模板,`agents/` 改放框架维护型 Meta Agent):
  - `agents/`(7 文件):具体、无占位符、可直接运行;经 `sync-mirrors.py` 的 `MIRROR_PAIRS`(`:56`,`("agents", ".specify/agents/templates", False)`)镜像到 `.specify/agents/templates/`,即术语表的 **Agent Template** 层。
  - `skills/create-agent/templates/`(10 文件):7 个 `agent-capacity-<slug>-template.md` 是带 `{{AGENT_NAME}}`/`{{PROJECT_NAME}}` 占位符的完整单 agent 授权模板 + `agent-project-custom-template.md`(自定义脚手架,frontmatter 用 `project:` 标记,无 `supervisor`/`capacity-scope`)+ 2 个可组合片段(`agent-skill-enablement.md`、`agent-supervision-delegation.md`)。
  - `skills/create-team/templates/agents/`(8 文件):团队域授权模板 —— 阶段角色(executor/evaluator/optimizer,`user-invocable: false`、无 `tools`/`maxTurns`/`color`)、`agent-team-supervisor-template.md`(用 `role-scope: team-supervisor` 而非 `capacity-scope`)、三个编排模板(parallel/serial/triad)、`agent-workflow-schema.md`。
- **"templates" 一词当前三义**:Agent Template 层(`.specify/agents/templates/`)、单 agent 授权模板目录、团队授权模板目录 —— 这是本需求要消除的歧义。
- **相邻在办项**: `.specify/memory/features.md:41` 的 Feature 033(Draft,Agent Project Context Parameterization)提议在 init/refresh 时按目标项目渲染 agent 正文的 `## Project Context` 段;它作用于**正文**,本需求作用于**元信息与分发**,两者需保持可叠加。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 元信息与 agent 自身内容有明确边界 (Priority: P1)

作为 agent 定义的维护者,我打开任一预置 agent 文件时,能一眼分清"这是给框架/分发用的元信息"和"这是描述这个 agent 是谁、怎么工作的内容",改其中一类不会被迫连带理解另一类。

**Why this priority**: 边界是后续一切的前提 —— 不先把元信息圈出来,就无法对它单独做中立化和格式转换。

**Independent Test**: 对 7 个预置 agent 逐一检查,可以在不解析正文的前提下,仅凭结构规则提取出完整元信息集合;也可以在不读元信息的前提下阅读正文而不遇到分发相关字段。

**Acceptance Scenarios**:

1. **Given** 任一预置 agent 定义,**When** 由程序按结构规则提取元信息,**Then** 得到完整元信息集合,且提取过程不需要理解正文语义。
2. **Given** 任一预置 agent 定义,**When** 阅读其正文,**Then** 正文中不出现分发/运行参数(轮次上限、配色、工具白名单等),这些只出现在元信息一侧。
3. **Given** 维护者只想调整某 agent 的职责描述,**When** 编辑正文,**Then** 无需触碰任何元信息字段。

---

### User Story 2 - 元信息用通用词汇表达,不绑定任何一家工具 (Priority: P1)

作为框架维护者,我希望 agent 的元信息用与工具无关的通用词汇描述意图(该 agent 能被谁调用、允许用哪些能力、单次运行的规模上限等),而不是直接书写某一家工具的字段名和取值枚举,这样新增或更换支持的工具时不必回头改每个 agent 文件。

**Why this priority**: 这是"彻底优化"的核心诉求,也是消除现有 Qoder 方言(`maxTurns` camelCase、"Qoder-compatible fields"、Qoder crosswalk、以 qoder 命名的契约测试)的唯一途径。

**Independent Test**: 对全部预置 agent 与授权模板做一次字段名扫描,不出现任何工具专属字段名;同时新增一个假想工具的支持时,agent 定义文件零改动。

**Acceptance Scenarios**:

1. **Given** 全部预置 agent 定义,**When** 扫描元信息字段名与取值,**Then** 不存在只有某一家工具认识的字段名或枚举值。
2. **Given** 每一个中立元信息字段,**When** 查阅其定义,**Then** 能在单一真源中找到该字段的语义、取值域与缺省值。
3. **Given** 需要为一个新的目标工具输出 agent,**When** 完成该工具的支持,**Then** 改动只落在"中立字段 → 该工具字段"的映射一侧,7 个 agent 定义文件与授权模板均无需修改。
4. **Given** 文档与测试中现存的工具专属命名(如以 qoder 命名的断言、"Qoder-compatible fields" 表述),**When** 本需求交付,**Then** 它们被替换为中立表述,不再暗示某一家工具是格式基准。

---

### User Story 3 - init 按目标工具渲染出真实 agent 文件 (Priority: P1)

作为使用者,我执行 `specify init <project> --ai qoder` 后,`.qoder/agents/` 下得到的是按 Qoder 支持格式渲染出来的真实 `*.agent.md` 文件,而不是指回 `.specify/agents/` 的软链接;换成别的工具时,得到的是那家工具支持的格式。

**Why this priority**: 这是用户可直接观察到的行为改变,也是元信息中立化的价值兑现点 —— 中立源 + 每工具渲染,取代"一份 Qoder 味文件软链接给所有人"。

**Independent Test**: 用同一工具 init 一个新项目,检查该工具 agent 目录下每个条目都是常规文件(非符号链接),且其 frontmatter 只含该工具支持的字段。

**Acceptance Scenarios**:

1. **Given** 一个新项目,**When** 执行 `specify init <project> --ai qoder`,**Then** `.qoder/agents/` 下每个 `*.agent.md` 都是真实文件而非符号链接,frontmatter 为 Qoder 支持的字段形态。
2. **Given** 同一份中立源,**When** 分别以两个不同工具 init,**Then** 两次产物的字段形态各自符合对应工具,而承载的意图(可调用性、能力白名单、规模上限等)保持等价。
3. **Given** 某个中立字段在目标工具中没有对应物,**When** 渲染,**Then** 按既定策略处理(不静默产出该工具无法解析的字段),且该处理结果可被观测到。
4. **Given** 目标工具不具备 agent 概念,**When** init,**Then** 跳过 agent 渲染且不报错、不生成空目录。
5. **Given** 同一中立源与同一目标工具,**When** 重复渲染,**Then** 产物确定性一致(可重现)。
6. **Given** 渲染完成,**When** 查看 init 输出,**Then** 能看到"为哪个工具渲染了多少个 agent"的明确反馈。

---

### User Story 4 - 已有项目平滑迁移且不吞用户改动 (Priority: P2)

作为已经用旧版本初始化过项目的使用者,我升级后重新 init/刷新时,原来的 agent 软链接被替换为渲染出的真实文件,而我自己写的 agent 和我手工改过的内容不会因此丢失。

**Why this priority**: 取消软链接是破坏性结构变更;现有链接函数已经积累了 override 保留、失效清理、同名冲突等语义,迁移路径没交代清楚就会造成用户资产损失。

**Independent Test**: 在一个含旧软链接、含用户自写 agent、含手工改过的 agent 文件的项目上执行升级路径,核对三类内容的最终状态。

**Acceptance Scenarios**:

1. **Given** 项目中已存在旧的逐文件 agent 软链接,**When** 执行升级路径,**Then** 这些链接被替换为渲染出的真实文件,不残留悬空链接。
2. **Given** 用户在项目内自写了 agent 定义,**When** 渲染,**Then** 它与预置 agent 一并被渲染分发,且在与预置同名时以用户侧为准(沿用现有 instance 优先语义)。
3. **Given** 用户手工修改过某个已渲染产物,**When** 再次 init/刷新,**Then** 该改动不被静默覆盖丢失(以明确、可预期的方式处理并告知)。
4. **Given** 中立源中已删除某 agent,**When** 再次渲染,**Then** 上一轮留下的对应产物被清理(沿用现有失效清理语义)。
5. **Given** 项目先以工具 A 初始化、后改用工具 B,**When** 渲染,**Then** 不因残留 A 的产物而让 B 读到不兼容格式。

---

### User Story 5 - 三个 agent 目录的差别被明确定义 (Priority: P2)

作为贡献者,当我看到 `agents/`、`skills/create-agent/templates/`、`skills/create-team/templates/agents/` 三个都在放 `*.agent.md` 的位置时,我能立刻判断某个文件属于哪一类、由谁生产、被谁消费、能否直接运行,不再被 "templates" 一词的多重含义误导。

**Why this priority**: 这是独立于代码改造的认知债务,当前 "templates" 同时指 Agent Template 层、单 agent 授权模板、团队授权模板,极易导致改错位置;但它不阻塞前三个故事,故列 P2。

**Independent Test**: 随机抽取三个目录中的任意文件,依据成文规则在一步内判定其类别与定位,判定结果与文档一致。

**Acceptance Scenarios**:

1. **Given** 三个目录中的任一文件,**When** 依据成文的判别规则检查,**Then** 能唯一确定它属于"Meta Agent 预置集(操作其他技能/agent,可独立运行)"、"Worker 能力模板(面向问题域,沿能力维度)"、还是"Worker 职责模板(面向问题域,沿团队职责维度)"。
2. **Given** 文档中的类别说明,**When** 核对每一类,**Then** 均写明:是否含占位符、是否可直接运行、生产者与消费者、命名规则、落地位置。
3. **Given** "templates" 一词的三处用法,**When** 本需求交付,**Then** 每处用法都有可区分的限定表述,读者不需要靠上下文猜测指代哪一个。
4. **Given** 三类之间存在的实际不一致(如团队 supervisor 模板用 `role-scope` 而单 agent 模板用 `capacity-scope`、阶段模板缺少运行参数字段),**When** 差别被定义,**Then** 这些不一致被明确记录为"有意为之"或"待收敛",不留悬念。

---

### Edge Cases

- 中立元信息中的字段在目标工具里**没有**对应物(例如规模上限只有部分工具支持):丢弃?降级?写进正文说明?策略必须显式且一致。
- 目标工具**独有**某能力而中立层没有对应表达(例如权限模式、隔离级别):是扩展中立层,还是允许该工具的映射侧补默认值?
- 中立取值落在目标工具枚举之外(例如模型档位命名不同):必须有映射或明确的失败/回退表现,不能产出该工具无法解析的取值。
- 目标工具的 agent 目录已存在同名真实文件,但它是**用户手写的 override** 而非上一轮渲染产物 —— **已裁定(2026-08-13)**:凭渲染清单区分;不在清单中的文件视为用户资产不覆盖,在清单中但内容不一致的先备份再覆盖(FR-021)。
- `.github/agents` 曾同时服务 copilot 与 claude 两个工具 —— **已裁定(2026-08-13)**:claude 改落 `.claude/agents/`,copilot 保留 `.github/agents/`,共用冲突消除。
- 中立源里 template 与 instance 同名冲突。
- 元信息缺失必填字段、或正文缺少必备章节时的渲染行为。
- 预置角色集与文档/注册表不同步(现状:仓库有 7 个预置 agent,而 `AGENTS.md` 的 Agents 注册表只列了 6 行,缺 ux-analyst)。
- 授权模板中的占位符若误入渲染路径,会把 `{{AGENT_NAME}}` 之类的字面量输出给目标工具。

## Requirements *(mandatory)*

### Functional Requirements

**元信息与正文的分离**

- **FR-001**: 系统 MUST 在 agent 定义中明确区分两类信息:用于分发与装配的**元信息**,和描述该 agent 自身身份/职责/工作方式的**正文**;两者的边界 MUST 可由程序判定,不依赖语义理解。
- **FR-002**: 元信息的载体形态 MUST 为单文件结构 —— 一个 `*.agent.md` 同时承载中立元信息块与正文,二者边界 MUST 仅凭 frontmatter 键归属即可由程序判定,MUST NOT 依赖将定义物理拆分为多个文件。
- **FR-003**: 正文 MUST NOT 承载任何工具专属语法或分发/运行参数;元信息 MUST NOT 承载角色职责叙述。
- **FR-004**: 分离后的结构 MUST 保持现有 agent 发现机制可用(按名称/描述枚举可用 agent),不要求消费方读取正文即可完成发现。

**元信息的中立化**

- **FR-005**: 元信息字段名与取值 MUST 使用工具无关的通用词汇,MUST NOT 直接采用任一具体 agent CLI 工具的专属字段名或取值枚举(含消除现存的 camelCase 工具方言键 [[STR-004]])。
- **FR-006**: 每个中立元信息字段 MUST 在单一真源中定义其语义、取值域、缺省值,以及"未提供时的行为"。
- **FR-007**: 中立字段集 MUST 覆盖现有 7 个预置 agent 已表达的全部意图(身份与描述、可被谁调用、能力/技能白名单、模型档位偏好、单次运行规模上限、角色作用域、督导关系、展示标识),不得在中立化过程中丢失既有语义。
- **FR-008**: 项目文档与契约测试 MUST 以中立表述描述该格式,不再把某一家工具作为格式基准(包括改掉以 qoder 命名的断言 [[STR-001]]、[[STR-002]] 与 [[STR-003]] 类表述)。

**按目标工具渲染分发**

- **FR-009**: 系统 MUST 维护一张"中立字段 → 各受支持工具字段"的映射,作为单一真源,并覆盖全部受支持的 AI agent CLI。
- **FR-010**: 映射内容 MUST 以各工具**官方文档**为依据;任何尚未核实的映射条目 MUST 被显式标注为待核实,MUST NOT 以猜测的字段名/枚举值充当已知事实。
- **FR-011**: `specify init <project> --ai <tool>` MUST 把中立元信息渲染为该工具支持的格式,并以**真实文件**写入该工具的 agent 目录,替代当前的逐文件软链接模式。
- **FR-012**: 各工具的目标目录 MUST 遵循已核定矩阵:`qoder` → `.qoder/agents/`、`claude` → `.claude/agents/`、`copilot` → `.github/agents/`、`opencode` → `.opencode/agents/`(复数);`codex` 本轮 MUST NOT 渲染 agent 输出 —— 其格式为 TOML 且落点在用户级 config 层,越出项目作用域 —— 但映射真源 MUST 保留其**标注行**(记录格式与落点证据);`hermes` MUST 按 FR-014 静默跳过。矩阵变更 MUST 经映射真源单点修改,MUST NOT 分散硬编码。
- **FR-013**: 渲染 MUST 只输出目标工具支持的字段;无对应物的中立字段 MUST 按一条记录在映射真源中的统一策略处理,并对所有工具一致适用;该处理 MUST 可被观测(不静默丢弃)。
- **FR-014**: 对不具备 agent 概念、或缺乏成文的项目级 agent 输出约定的目标工具,系统 MUST 静默跳过 agent 渲染而不报错、不产生空目录。
- **FR-015**: 渲染 MUST 是确定性的:相同中立源与相同目标工具产出逐字节一致的结果。
- **FR-016**: 中立源 MUST 保持 agent 定义的唯一真源;渲染产物 MUST 被视为派生件,MUST NOT 成为二次编辑的事实来源。
- **FR-017**: 渲染 MUST 覆盖用户在项目内自写的 agent,而非仅限预置角色;与预置同名时 MUST 以用户侧为准(沿用现有 instance 优先语义)。
- **FR-018**: init MUST 反馈本次为哪个工具渲染了多少个 agent。

**迁移与安全**

- **FR-019**: 升级路径 MUST 把既有的逐文件 agent 软链接替换为渲染产物,且不残留悬空链接或历史整目录链接。
- **FR-020**: 中立源中已不存在的 agent,其上一轮渲染产物 MUST 被清理(沿用现有失效清理语义)。
- **FR-021**: 用户手工修改过的渲染产物 MUST NOT 被静默覆盖丢失;系统 MUST 借助渲染清单(对每个产物最近一次渲染的哈希比对)检测手改,并执行一条成文的统一行为:未改动的产物直接覆盖刷新;已改动的产物先备份至可取回位置再覆盖新渲染,且备份路径 MUST 在 init 反馈中明示;不在渲染清单中、且无中立源对应的文件 MUST 视为用户资产而不得覆盖。
- **FR-022**: 切换目标工具后,MUST NOT 因上一工具的残留产物导致新工具读到不兼容格式。

**三类 agent 目录的差别定义**

- **FR-023**: 系统 MUST 沿 Worker/Meta 类型划分成文定义三者的差别 —— `agents/` **仅**定义 **Meta Agent(元 Agent)**:操作对象是其他技能与其他 agent,均可**独立运行**(无特定团队需求时已具备自身职责,如调整目录结构、验证技能执行效果);`skills/create-agent/templates/` 与 `skills/create-team/templates/agents/` 定义的都是 **Worker Agent(面向问题域操作的 agent 模板)**,前者沿**能力**维度、后者沿**职责**维度(团队席位与编排契约);每类 MUST 写明:是否含占位符、是否可直接运行、生产者与消费者、命名规则、落地位置。现有 7 个角色定义按"操作对象为业务工件"判据实为 **Worker**,MUST 从 `agents/` 迁入 `skills/create-agent/templates/` 的 Worker 能力模板序列;`agents/` MUST 由新作的框架维护型 Meta Agent 定义填充。
- **FR-023a**: 差别定义 MUST 成文给出**组队取件规则**:组建 Team 时,Meta Agent 从 `agents/` 选取,Worker Agent 从技能模板实例化选取;迁移完成后,7 个角色定义 MUST 不再以预置形态随 init 分发,而是经 Worker 能力模板按需实例化。
- **FR-024**: 系统 MUST 以 Worker/Meta 目录划分及其配套文档消除 "templates" 一词的多义:三处用法 MUST 各有可区分的限定表述(Meta Agent 预置集 / Worker 能力模板 / Worker 职责模板),读者无需依赖上下文即可判断指代;MUST NOT 为此物理重命名现有目录。
- **FR-025**: 差别定义 MUST 被术语表锚定(与既有 Agent Template / Agent Instance / Agent Execution 三层分类法一致,并新增目录级 Worker/Meta 划分条目),并 MUST 记录三类之间现存的不一致([[STR-005]] 与 [[STR-006]] 并存、阶段模板缺运行参数)是"有意为之"还是"待收敛"。
- **FR-026**: 授权模板中的占位符 MUST NOT 出现在任何渲染产物中。

**验证**

- **FR-027**: 契约测试 MUST 覆盖:元信息中不含工具专属字段名、渲染产物为真实文件而非符号链接、映射覆盖全部受支持工具、渲染确定性、以及用户自写与手改内容的保全。

### Key Entities *(include if requirement involves data)*

- **Agent Definition(agent 定义)**:一个角色的完整描述,由元信息与正文两部分构成;唯一真源。
- **Neutral Agent Metadata(中立元信息)**:工具无关的意图声明集合(身份、可调用性、能力白名单、模型档位、规模上限、角色作用域、督导关系、展示标识);渲染的输入。
- **Agent Body(正文)**:角色身份、职责、工作流、上下游、输出格式等叙述内容;渲染时原则上按原样承载。
- **Tool Metadata Mapping(工具映射)**:中立字段 → 某工具字段的对应关系,含取值转换、无对应物的处理策略、目标目录、以及依据来源(官方文档或"待核实")。
- **Rendered Agent File(渲染产物)**:按某工具格式写入其 agent 目录的派生文件;可从中立源确定性重建。
- **Authoring Template(授权模板)**:带占位符、不可直接运行、用于**创作**新 agent 的脚手架;分能力模板(create-agent 域)与职责模板(create-team 域)两类,均为 **Worker Agent 模板**,与 `agents/` 的 Meta Agent 定义构成目录级 Worker/Meta 划分。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `agents/` 全部 Meta Agent 定义与全部 Worker 模板(含迁入后的 7 个角色定义)的元信息中,工具专属字段名/取值的出现次数为 **0**。
- **SC-002**: 对本轮渲染的每个工具(当前为 qoder / claude / copilot / opencode 四家),init 后其 agent 目录中符号链接数为 **0**、渲染真实文件数等于中立源中的 agent 数。
- **SC-003**: 工具映射覆盖 **全部**受支持 AI agent CLI(当前 6 家),每家为**渲染行**(4 家)或**标注行**(记录不渲染的依据,2 家),每条均标注依据来源;标注为"待核实"的条目数在交付时为 **0**。
- **SC-004**: 为一个新目标工具增加 agent 输出支持,所需改动的 agent 定义文件数为 **0**(改动全部落在映射一侧)。
- **SC-005**: 同一中立源、同一目标工具连续渲染两次,产物差异为 **0** 字节。
- **SC-006**: 在含旧软链接 + 用户自写 agent + 用户手改产物的项目上跑升级路径,用户内容丢失数为 **0**,悬空链接数为 **0**。
- **SC-007**: 从三个目录中抽样任意文件,依据成文规则判定类别的正确率 **100%**,且判定不超过 1 步查表。
- **SC-008**: 全量测试相对改造前基线的回归失败数为 **0**(以改造前记录的基线为对照,区分既有失败与新引入失败)。

### Measurement Sources & Collection Methods

- **SC-001 Source**: 对 `agents/`、`skills/create-agent/templates/`、`skills/create-team/templates/agents/` 做字段名扫描的契约测试,断言禁用词表命中数为 0;每次 CI 运行采集。
- **SC-002 Source**: 集成测试在临时目录执行 init 后统计目标 agent 目录下的符号链接数与常规文件数;每次 CI 运行采集。
- **SC-003 Source**: 映射真源文件自身的条目与来源标注列,由契约测试对照受支持工具清单(`AGENT_CONFIG`)校验完备性;每次 CI 运行采集。
- **SC-004 Source**: 交付时以一次"新增假想工具"的演练记录改动文件清单;一次性验收采集。
- **SC-005 Source**: 集成测试连续渲染两次并做逐字节比对;每次 CI 运行采集。
- **SC-006 Source**: 迁移场景集成测试,预置三类内容后执行升级路径并核对最终状态;每次 CI 运行采集。
- **SC-007 Source**: 交付评审时对三目录各抽样若干文件按文档规则人工判定;一次性验收采集。
- **SC-008 Source**: 改造前先运行全量 `pytest` 记录基线失败清单,交付后再次运行做集合差比对;改造前后各一次。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "test_preset_has_qoder_frontmatter" | FR-008(须更名为中立断言);现存于 `tests/contract/test_shipped_agent_presets.py` |
| `STR-002` | "test_template_has_qoder_frontmatter" | FR-008(须更名为中立断言);现存于 `tests/contract/test_role_templates.py:68` |
| `STR-003` | "Qoder-compatible fields" | FR-008(须替换为中立表述);现存于 `docs/reference/agents/templates-and-agents.md:80-83` |
| `STR-004` | "maxTurns" | FR-005(工具方言键,须中立化);现存于全部 7 个预置 agent frontmatter |
| `STR-005` | "capacity-scope" | FR-025(与 `role-scope` 并存的不一致须裁定) |
| `STR-006` | "role-scope" | FR-025(同上);现存于 `skills/create-team/templates/agents/agent-team-supervisor-template.md` |

**Citation convention**: 下游 FR/契约/任务/测试引用上述字符串时写 `[[STR-NNN]]`,不要复制字面量,便于一次轮换。

## Out of Scope

- 不新增、不删除、不重命名 7 个角色定义的**角色内容**(Role 正文、工作流、技能使能);但其**归属与分类**按 FR-023 迁移(预置集 → Worker 能力模板),相应文档/注册表/测试的机械性联动更新在本需求范围内。
- 不重写 agent 正文的六大必备章节内容;正文只在"剥离分发参数"这一点上被触及。
- 不实现 Feature 033(按项目渲染 `## Project Context`);本需求只要求与之可叠加,不代其落地。
- 不改动 skills 的分发方式(`.specify/skills` 的整目录软链接模型保持)。
- 不改动 commands 的分发链路(`regen-command-copies.py` 及各工具 commands 目录)。
- 不新增受支持的 AI agent CLI 工具;仅要求"新增时改动面收敛到映射一侧"。
- 不修复"预置 agent 7 个 vs `AGENTS.md` 注册表 6 行"的既有漂移(仅作为边界情形记录)。

## Assumptions

- 中立源仍位于 `.specify/agents/{templates,instances}`,`agents/` 仍是仓库内的上游真源并经 `sync-mirrors.py` 镜像。
- 渲染发生在 init 时;若已有刷新入口(如 `/speckit.instructions`、`/speckit.agents`)需要产出同类文件,复用同一渲染逻辑而非另写一份。
- 受支持工具清单以 `AGENT_CONFIG` / `_ASSISTANT_TIERS` 为准(当前 6 家),不在本需求内变更。
- 各工具的 agent 字段格式以官方文档为准;由于本仓库现无该类文档,映射需在 plan 阶段逐一核实后落地(FR-010)。
- 渲染产物是派生件,可被安全重建;用户若要长期定制,应改中立源而非产物。
- "元信息 / metadata / 元数据"在本文档中同义,统一以"元信息"表述。

## Clarifications

<!-- 
This section will be populated by /speckit.clarify command with questions and answers.
Format: - Q: <question> → A: <answer>
-->

### Session 2026-08-13

- Q: Related Feature 绑定 —— 绑定既有 Feature 033(Agent Project Context Parameterization)还是创建新 Feature? → A: 创建新 Feature **044 Agent Metadata Portability**。本需求交付的是一条独立的渲染管线(中立元信息 → 每工具真实文件),是 033 这类正文渲染的宿主能力而非其一部分;两者互补并交叉引用(044 管元信息与分发,033 管正文 Project Context 参数化)。
- Q: 元信息载体形态(FR-002)—— 单文件内的中立元信息块,还是正文文件 + 独立元信息文件的物理分离? → A: **单文件结构** —— 一个 `*.agent.md` 同时承载元信息块与正文,边界凭 frontmatter 键归属判定;发现机制、镜像对、迁移面均保持不变。
- Q: 每工具目标目录矩阵(FR-012)—— codex 是否纳入?claude 与 copilot 是否维持共用 `.github/agents`? → A: **矩阵核定为四家项目级渲染**:`qoder` → `.qoder/agents/`、`claude` → `.claude/agents/`(VS Code 亦读此位置)、`copilot` → `.github/agents/`、`opencode` → `.opencode/agents/`(复数)。`codex` 本轮不渲染(格式为 TOML、落点在用户级 config 层,越出项目作用域),映射真源保留标注行;`hermes` 按 FR-014 静默跳过。矩阵变更经映射真源单点修改。
- Q: 用户手改渲染产物后的再渲染行为(FR-021)—— 备份替换、跳过保留还是冲突文件? → A: **备份替换 + 报告** —— 用渲染清单(哈希比对)检测手改;未改直接覆盖刷新,已改先备份至可取回位置再覆盖并在 init 反馈中明示备份路径;不在清单中且无中立源对应的文件视为用户资产不覆盖。
- Q: "templates" 三义消除与三目录差别定义(FR-023/FR-024) → A: (用户指示)三目录沿**三个组合维度**划分:`skills/create-agent/templates/` 定义 Agent 的**能力**,`skills/create-team/templates/agents/` 定义 Agent 的**职责**,`agents/` 定义**元 Agent**(agent 类型定义本身)。经确认取"维度读法":"元"指定义 agent 类型的元层,与 Worker/Meta 阶段判型正交不变;agent 正文不重写、不做物理目录重命名,消歧由三维度模型 + 文档/术语表承载。

### Session 2026-08-13(第二轮)

- 用户修订指示(原文):"./agents这个目录中应该定义所有的Meta Agent(元Agent),这些 Agent 是用来操作其他技能和其他 Agent,而无论是skills/create-agent还是skills/create-team技能中模板都是所谓的 Worker Agent,即真正面向问题域进行操作的 Agent。通过这种划分,Agent 体系更加清晰。组建 Team 时,需从 Process 中选取原 Agent,从技能模板中选取 Worker Agent。所有原 Agent 均可独立运行,因其在无特定需求时已具备自身职责。例如,启动 Agent 调整目录结构,或启动 Server Agent 验证技能执行效果。" —— 以此**目录级 Worker/Meta 划分**取代第一轮的"三维度正交"读法(第一轮的 能力/职责 子维度保留为 Worker 模板内部的组织方式)。
- Q: 语音误写更正(术语表协议) → A: 用户确认两处均为语音误写,按建议更正:"从 Process 中选取原 Agent" = **从预置(`agents/`)中选取 Meta Agent**("原"≈"元");"Server Agent" 为笔误,不存在的概念,上下文语义为"某个验证技能执行效果的 Meta Agent"。
- Q: 现有 7 个预置角色按新判据的归属 —— 双上下文读法(留在 agents/)还是严格判据迁移? → A: **B 严格判据迁移** —— 7 个角色定义按"操作对象为业务工件"判据实为 Worker,从 `agents/` 迁入 `skills/create-agent/templates/` 的 Worker 能力模板序列;`agents/` 由新作的框架维护型 Meta Agent 定义填充;迁移后 7 个角色定义不再以预置形态随 init 分发,经模板按需实例化(FR-023/FR-023a/SC-001/Out of Scope 已联动改写)。
