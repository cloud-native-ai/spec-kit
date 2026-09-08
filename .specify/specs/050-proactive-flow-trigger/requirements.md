# Requirements Specification: 主动触发机制——必经路径埋点、情境评估建议与阈值晋升自动执行(Proactive Flow Trigger)

**Requirement Branch**: `050-proactive-flow-trigger`
**Created**: 2026-09-07
**Status**: Draft
**Input**: User description: "需要为框架引入自动化触发流程,当前很多流程都是由用户手动执行/speckit.*命令或者具体的skill名进行触发的,这要求用户必须明确记得每个命令和技能的名称和大体的参数结构,才能主动的进行调用执行,对于用户的心智负担太大. 需要引入一种机制,让用户不必记得具体的命令和技能即可使用speckit框架丰富的功能. 需要执行init命令时在支持的agent工具执行的必经路径上进行埋点(比如AGENTS.md文件),在埋点的地方触发speckit框架的自省机制,提示用户可以执行哪个流程,并持续记录和优化这个埋点逻辑,当前每次用户都选择一个选项超过阈值(比如3次)后续就不用用户再进行确认,直接执行相应的流程即可."

## Related Feature *(mandatory)*

**Feature ID**: 050  
**Feature Name**: Proactive Flow Trigger(主动触发机制)

绑定依据(clarify 2026-09-07):**新建 Feature 050**,不绑定既有 Feature。按绑定先例启发式逐个核验候选的同胞吸收证据与主题归属后,结论是**无既有 Feature 拥有本需求引入的能力**——每个候选只匹配一个侧面:

| 候选 Feature | Status | 已吸收同胞 specs | 与 050 的实际关系 |
|---|---|---|---|
| 032 Task Complexity Rubric | Implemented | 1(自身) | **最接近的结构先例**:同为嵌入 `.specify/instructions.md`、经 `/speckit.instructions` 非破坏投递的行为指令。但主题是"思考深度校准",非"流程选取" |
| 008 Instructions Command | Completed | 1(自身) | 仅投递载体(生成 050 段落所落文件) |
| 001 Unify Command Handoffs | Completed | 1(自身) | 最近的能力前身("下一步做什么"),但静态、命令域;050 的 Out of Scope 明确不改命令模板 Handoffs |
| 022 AI Tools Support | Implemented | 4(011/019/021/018) | 只拥有 FR-003 议题(全 agent init 覆盖);其余 22 条 FR 与之无关 |
| 028 Feedback Mechanism | Implemented | 3(027/041/047) | 计数-阈值机制与事件记录的**先例**,主题是 feedback 而非触发 |
| 046 Confirmation Gate Governance | Implemented | 1(044) | 050 消费其破坏性判据(FR-011),不扩展其治理范围 |

决定性先例是 **032**:投递载体与本需求完全相同,却仍自成一个 Feature 而非绑 008 Instructions Command——这确立了"以指令段形式嵌入"**是投递事实,不是归属事实**。此外 050 引入三个既有 Feature 范围均不覆盖的持久面(规则集 / 晋升态 / 事件与回合遥测),归属新建。上表六个 Feature 以**交叉引用**(消费关系)记入 `.specify/memory/features/050.md`,不构成归属。Feature 总数 49 → 50,权威计数以 `.specify/memory/features.md` 自动派生头部为准。

## Overview

把"用户必须记得命令名与技能名才能用上框架能力"这一心智负担,反转为**框架主动出现在 agent 的必经路径上**:

1. **埋点**:`specify init` / `/speckit.instructions` 生成指令文件时,把一段**主动触发指令**写入 canonical 指令源 `.specify/instructions.md`,经既有 symlink 模型抵达每个受支持 agent 的必读文件(根 `AGENTS.md`/`CLAUDE.md`/`QODER.md` 等)。**指令文件是唯一触发通道**(clarify 2026-09-07 裁定),不引入 agent 原生 hook。
2. **情境评估与建议**:agent 在**每个用户回合**对当前项目状态做评估——默认只消费已在上下文中的环境信息(近零增量成本),不足以判定时才升级到确定性探测程序的摘要输出;判断"现在可以/应该执行哪个流程"后,以**一行非阻塞建议**给出用途说明 + **确切可复制的调用形式**。用户只需说"好"或忽略,不必回忆任何名称。这趟评估**挂在既有 constitution 合规分析之后**——框架今天已要求"每个请求先查相关文档"(Documentation Map 常驻指令),本特性在同一趟里接续做流程选取,不新造平行分析。**评估节奏 ≠ 建议节奏**:评估每回合静默执行,建议输出另受频次约束。
3. **学习与晋升**:每次建议的采纳/拒绝被记录;同一(情境→流程)规则**连续采纳**达阈值(默认 3,可配置)后**晋升为免确认自动执行**。硬边界:**破坏性/不可逆流程永不晋升**。
4. **规则自我优化**:触发规则是**数据而非散文**;依记录证据(命中率、拒绝率、误报、漏报)提议收紧/抑制/新增,经用户确认后生效,使埋点逻辑可回溯演进。

该机制最终围绕两个不可分割的判定:

1. **该不该提**:情境证据支持某个流程有实际价值时才提;无适用流程即如实沉默,MUST NOT 为凑数推荐(反噪声)。
2. **该不该直接做**:只有既被稳定偏好证明(连续采纳达阈值)、又不属破坏性类别的流程才免确认执行;二者缺一即回到"只建议"。

### 现状锚点(以源码实测为准)

- **指令生成链**:`scripts/bash/generate-instructions.sh` 渲染 `templates/instructions-template.md`(124 行)→ `.specify/instructions.md`(canonical),并建 symlink:根 `AGENTS.md` / `CLAUDE.md` / `QODER.md` → `.specify/instructions.md`(L210–212),另 `.github/copilot-instructions.md`(L193)、`.qoder/project_rules.md`(L199;Qoder IDE 专用,Qoder CLI 读根 `AGENTS.md`)、`.claude/project_rules.md`(L205)。刷新走 additive section reconcile(缺失 `## ` 章节注入,既有内容保留)并先备份、不覆盖。
- **模板现有 14 个 `## ` 章节(合计 17 个标题,含 H1 与 1 个 `###`),其中无任何主动触发/建议章节**;唯一近似物是 `## Suggested Tooling Scope (High-Level)`(L87),属**被动指引**(告诉 agent 优先复用脚本),不构成对用户的流程建议。**14 是关键数字**:`generate-instructions.sh` 的 additive reconcile 只按 `(?m)^(## .+)$` 切分,故只有 `## ` 级章节会被注入既有 `.specify/instructions.md`,`###` 子节与既有 `##` 章节内部的文案改动**不传播**(深度刷新是 `/speckit.instructions` 的职责)。
- **覆盖缺口**:`_INSTRUCTIONS_FILE_MAP`(`src/specify_cli/__init__.py:1090–1097`)声明 6 个 agent 的指令路径,但 `generate-instructions.sh` 只创建其中 4 条——`hermes → HERMES.md`、`opencode → .opencode/instructions.md` **声明却未生成**,`_check_instructions`(L1115–1121)对这两者恒报 `fail`。埋点若只挂在已生成路径上,这两个 agent 收不到触发指令。
- **每回合分析义务已有先例(constitution)**:`templates/instructions-template.md` 的 Documentation Map 把 `.specify/memory/constitution.md` 列为首行(L13),并在表尾挂**环境常驻指令**(L22):「When answering questions or generating code, ALWAYS check the relevant document from the map above first」;L90 另有「Treat Constitution as the authority for architecture and workflow constraints」。也就是说,**"每个请求都要做一趟合规分析"这一义务今天已经存在,且正是靠必经指令路径投递的**——本特性的每回合评估不是新造义务,而是搭在既有义务上。
- **但形式化的 Constitution Check 门控是 plan 期而非每回合**:`.specify/templates/plan-template.md:31–33` 的 `## Constitution Check` 标注为「*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*」,由 `/speckit.plan` **动态枚举** constitution 全部原则逐条成表(`templates/commands/plan.md:63–66`,禁止硬编码原则名),`templates/commands/tasks.md:119` 再引用之。故存在**两级**:每回合的轻量"先查相关文档"义务,与 plan 期的完整逐原则枚举门控。本特性只能挂前者——把后者搬到每回合既付不起也违反 Principle IX(拒绝投机基础设施)与 token 效率纪律。
- **今天没有任何主动建议机制**(每回合分析义务虽已存在,却从不产出"该执行哪个流程"的建议)。既有近似物及其局限:① **25 个命令模板全部带 `## Handoffs`**(Feature 001),但那是"已调用某命令之后"的下一步提示——恰是本特性要解决的先有鸡还是先有蛋问题:不记得命令名就永远读不到 Handoffs;② `implement` 长跑模式(`templates/commands/implement.md:86–94`)用 git-ignored 状态文件 `implement-loop.local.md` 驱动有界循环,明示 "no Stop-hook required";③ feedback 阈值提示(count ≥ 阈值时一行非阻塞提示);④ better-harness(`scripts/js/better-harness/`)只对会话日志中的 hook/SessionStart/UserPromptSubmit 事件做**只读法证分析**,不是运行时触发器。
- **计数-阈值机制已有可复用先例**:`feedback-utils.py` 的 `DEFAULT_THRESHOLD = 10`(L52)、`should_prompt(count, threshold)`(L101–102)、`resolve_threshold`(优先级:显式 CLI > 环境变量 > 存储 index > 默认,L105–116)。本特性的"N 次晋升"与之同构。
- **确认门控治理是本特性的硬边界**:`.specify/shared/guidelines/confirmation-gates.md` 两级分类(破坏性/不可逆 → 前置确认;可逆 → 自动执行 + 三段式执行报告 L54–66)、破坏性清单(L14–22:删除、搬迁/归档、远端推送/外部权威写入、覆盖用户内容)、存疑从严(L43–45)、**回流约束**(L47–52:新命令/技能 MUST NOT 引入非破坏性阻塞门控),由 `scan-confirmation-gates.py` + 结构契约测试强制。
- **机器维护状态的既有落盘范式**(学习状态可复用):`.specify/git-workflow.md`(`<!-- GIT_WORKFLOW_START/END -->` 受管块,指令文件只放指针)、`.specify/memory/features.md`(自动派生头部)、`.specify/memory/tools.md`(`refresh-tools.sh` 再生的发现清单)、`.specify/memory/feedback/index.json` + `probe-map.md`(引擎再生派生视图)。
- **框架当前不掌握各 agent 的 hook 能力**:`AGENT_CONFIG`(L64–101)唯一能力位是 `requires_cli`;`_ASSISTANT_TIERS`(L851–858)只区分 CLI 形态(Tier 1: claude/codex/qoder/opencode;Tier 2: hermes/copilot);仓库与模板中**无任何 hooks 配置**(`.claude/settings.local.json`、`.qoder/settings.local.json` 仅含 `permissions.allow`,且为用户本地、非模板产物)。

**与现状的差异(本需求要闭合的缺口)**:

| 缺口 | 现状 | 目标 |
|------|------|------|
| 能力可见性 | 命令/技能只能靠用户回忆名称调用;`## Handoffs` 只在调用之后可见 | 触发指令进入 agent 必经路径,框架能力在会话内主动可见 |
| 下一步判断 | 无;由用户自行推断当前该做什么 | 情境评估产出"当前可执行流程" + 确切调用形式 |
| 覆盖完整性 | 6 条声明路径中 2 条未生成(hermes/opencode) | 全部受支持 agent 的必经路径收到同一触发指令 |
| 重复确认 | 每次都要用户主动发起同一流程 | 同一(情境→流程)连续采纳达阈值后免确认自动执行(破坏性除外) |
| 触发逻辑演进 | 无规则可言,亦无记录 | 规则为数据;依采纳/拒绝证据提议调优,经确认生效并可回查 |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 触发点埋设与全 agent 覆盖 (Priority: P1)

用户在项目上运行 `specify init`(或 `/speckit.instructions` 刷新)后,一段**主动触发指令**被写入 canonical 指令源,并经既有 symlink/生成模型抵达每个受支持 agent 的必经文件。该段是**引用式**的:它声明"在此处做情境评估并建议流程"这一行为契约,并以引用指向流程清单的权威源,MUST NOT 把命令名/技能名/参数结构枚举复制进指令文件(单一事实源 + token 效率)。用户自定义内容在刷新时按既有 additive reconcile 语义保留。**指令文件常驻指令是唯一触发通道**(clarify 2026-09-07):全 agent 通用、零适配成本、init 即得,不引入 agent 原生 hook。由此接受的代价是触发依赖 agent 遵守指令、无确定性保证——**漏报为已接受风险**,补偿控制是 US4 的漏报检测(用户手动调用了某流程而当时无建议 → 提议新增/收紧规则)。也正因如此,必经路径的全覆盖从"审计整洁"升级为**硬前置**:指令文件既是唯一通道,当前声明却未生成的 hermes/opencode 路径缺失,就等于这两个 agent 完全没有本机制。

**Why this priority**: 这是整套机制的物理落点。没有必经路径上的常驻指令,后续的情境评估、建议、学习都无从被触发,用户依然必须自己记得去调用某个命令。仅这一段落地,框架能力第一次出现在 agent 的必读上下文里。

**Independent Test**: 在一个干净项目上运行 init,逐一检查每个受支持 agent 的必经文件:(a) 都含触发指令且语义一致(同一 canonical 源,非各自复制);(b) 触发段不重复命令/技能清单(与权威源交叉文本检查,枚举复制计数为 0);(c) 运行 `/speckit.instructions` 刷新后触发段仍在、用户自定义章节未被吞掉;(d) 声明的指令路径全部实际存在(含当前恒 fail 的两条)。

**Acceptance Scenarios**:

1. **Given** 一个未初始化的项目,**When** 用户运行 init 并选择任一受支持 agent,**Then** 该 agent 的必经指令文件存在且含主动触发指令段
2. **Given** 项目已初始化,**When** 用户运行 `/speckit.instructions` 刷新,**Then** 触发段被再生且既有自定义章节保留(additive reconcile 语义不变)
3. **Given** 两个不同 agent(如 Claude Code 与 Qoder CLI),**When** 分别读取各自必经文件,**Then** 二者所见触发指令语义相同(同源 symlink/生成,非分叉副本)
4. **Given** 触发段以引用表达流程清单,**When** 检查指令文件内容,**Then** 其中不含命令名/技能名/参数结构的枚举复制,只有指向权威源的引用
5. **Given** 当前 `hermes`/`opencode` 的指令路径声明却未生成,**When** 本特性落地后运行 init,**Then** 这两条路径同样收到触发指令(或经裁定显式记为不支持并从声明中移除,不留恒 fail 的审计项)
6. **Given** 用户在指令文件中手写了与触发段矛盾的自定义内容,**When** 刷新,**Then** 用户内容保留且其显式意图优先于框架默认

---

### User Story 2 - 情境评估与流程建议:用户不必记得命令名 (Priority: P1)

用户像平常一样向 agent 描述意图("我想给这个特性做规划"、"这批反馈该处理一下"、"文档有点乱"),或只是继续手上的任何工作;agent 依触发段在**每个用户回合**做情境评估。**证据预算是两级的**(clarify 2026-09-07):默认只消费已在上下文中的环境信息(哪些制品已存在、当前特性处于 spec→plan→tasks→implement 的哪一站、是否有待处理 feedback/自省报告、是否有寄存 TODO、指令文件是否陈旧)——近零增量成本;仅当环境信息不足以判定时,才升级到确定性探测程序输出的**状态摘要**(仍守摘要优先,不注入制品原文)。据此判断"现在可以/应该执行哪个流程",并以**一行非阻塞建议**给出:流程用途 + 确切可复制的调用形式。用户只需说"好"或直接忽略,不需要回忆任何命令名或参数结构。建议是**提示,不是门**:MUST NOT 阻塞用户当前请求的执行。**每回合评估只有在默认证据预算近零时才付得起**,且评估本身是静默的——**评估节奏 ≠ 建议节奏**:评估每回合做,建议输出仍受频次约束(状态未变不重复刷屏)。该趟评估**接续既有 constitution 合规分析**(框架今天已要求每个请求先查相关文档),在同一趟里完成"先合规、再选流程",不新造平行分析。

**Why this priority**: 这是本特性的价值本体——直接消除用户描述的心智负担。US1 只把指令放上必经路径,真正让用户"不记名字也能用上丰富功能"的是这一段。二者合起来构成 MVP。

**Independent Test**: 构造一组覆盖生命周期的代表性项目状态(仅 requirements、requirements 含未决澄清、已澄清未规划、plan 就绪无 tasks、tasks 就绪未实现、feedback 条目达阈值、docs 空间漂移),在每种状态下开启会话并提出一个中性请求,验证:(a) 建议指向该状态下正确的下一流程;(b) 建议含确切可复制的调用形式;(c) 用户全程未说出任何命令名;(d) 建议不阻塞当前请求;(e) 状态无对应流程时如实"无建议",不硬凑;(f) **零学习记录的全新项目**靠出厂种子规则即产出正确建议(无冷启动);(g) 连续多个无关回合中评估静默、探测升级率有界(回合遥测可核)。

**Acceptance Scenarios**:

1. **Given** 项目只有 `requirements.md` 且含未决澄清标记,**When** 用户提出任一回合请求(首个或后续),**Then** 建议指向澄清流程并给出确切调用形式
2. **Given** 用户用自然语言描述意图("我想把这个特性拆成任务"),**When** agent 评估,**Then** 建议对应流程,用户无需知道其命令名
3. **Given** 当前项目状态没有任何适用流程,**When** 评估完成,**Then** agent 如实不提出建议(MUST NOT 为凑数推荐无关流程)
4. **Given** agent 已给出建议,**When** 用户忽略它并继续原请求,**Then** 原请求照常执行,建议不构成阻塞门
5. **Given** 情境评估需要项目状态证据,**When** 评估执行,**Then** 消费的是摘要/字段投影而非制品原文全量注入(token 效率纪律)
6. **Given** 同一次会话内已给过建议且状态未变,**When** 后续回合继续,**Then** 不重复刷屏(建议频次有界)
7. **Given** 多条规则同时命中,**When** 产出建议,**Then** 收敛为一条最高优先建议(或有界数量),不逐条罗列
8. **Given** 用户连续进行多个与框架能力无关的回合,**When** 每回合都执行评估,**Then** 评估静默完成、该机制的用户可见输出为 0(评估节奏 ≠ 建议节奏)
9. **Given** 环境信息不足以判定当前项目状态,**When** 评估执行,**Then** 升级到确定性探测程序的摘要输出,且探测仍不注入制品原文
10. **Given** 环境信息已足以判定,**When** 评估执行,**Then** 不触发探测升级("按需升级"MUST NOT 退化为"每回合升级")
11. **Given** 某回合的 constitution 合规分析尚未完成,**When** 流程选取产出建议,**Then** 建议不早于合规分析(顺序契约);且合规分析与流程选取是**同一趟**,未新造并列的第二趟分析
12. **Given** 一个全新项目、从未积累任何学习记录,**When** 用户提出首个生命周期相关请求,**Then** 出厂种子规则即产出正确建议(第一天即有价值,无冷启动)
13. **Given** 当前情境无法被受控词表表达,**When** 评估完成,**Then** 当回合如实无建议,MUST NOT 由 agent 临场造词凑一条身份;该缺口作为漏报证据进入 US4 的词表扩展提议

---

### User Story 3 - 选择记录与阈值晋升:重复确认后自动执行 (Priority: P2)

每次建议的结果(采纳/拒绝/忽略,以及命中哪条规则、当时情境)被记录到一份**机器维护的项目本地学习状态**中。当同一(情境→流程)规则被**连续采纳**达到阈值(默认 3,可配置)后,该规则**晋升**:此后情境再次命中时,agent 直接执行对应流程,不再询问。晋升有硬边界:**破坏性/不可逆流程永不晋升**——确认门控治理的两级分类与破坏性清单是唯一判据,学习计数 MUST NOT 覆盖它;分类存疑时按"存疑从严"默认破坏性。一次拒绝即重置该规则的连续计数(晋升需稳定偏好,而非历史累计)。用户随时可查看晋升态、复位单条规则、或全局降级为"只建议"。

**Why this priority**: 这是用户明确要求的"超过阈值就不用再确认"。它建立在 US2 的建议与记录之上——没有建议就没有选择,没有选择就无从学习。它把机制从"提醒"升级为"代办",但价值增量小于 US1+US2,且引入需要严格安全边界的新风险面(误自动执行),故列 P2。

**Independent Test**: 对同一情境连续采纳同一建议 3 次,验证第 4 次情境命中时流程被自动执行且零确认询问;对一条属破坏性的流程重复采纳 5 次,验证第 6 次仍前置确认(自动执行数为 0);在第 2 次采纳后插入一次拒绝,验证计数重置、晋升未发生;运行 `/speckit.instructions` 刷新后验证学习状态(计数与晋升态)零丢失。

**Acceptance Scenarios**:

1. **Given** 某规则已连续被采纳 3 次,**When** 情境再次命中,**Then** 对应流程自动执行,用户看到执行报告而非询问
2. **Given** 某规则对应流程属破坏性/不可逆类,**When** 该规则被采纳任意多次,**Then** 永不晋升,每次仍前置确认
3. **Given** 某规则连续采纳 2 次后用户拒绝一次,**When** 后续再采纳,**Then** 计数从 0 重新累计,不发生晋升
4. **Given** 用户想查看或复位学习结果,**When** 用户提出,**Then** 可查看每条规则的计数与晋升态,并可复位单条或全局降级为"只建议不自动执行"
5. **Given** 学习状态已积累,**When** 指令文件被再生,**Then** 学习状态完整保留(受管块/独立文件范式,再生不吞状态)
6. **Given** 自动执行发生了,**When** 执行结束,**Then** 产出既有三段式执行报告(执行内容/产出工件/修改途径),使用户可事后纠正
7. **Given** 学习状态缺失、损坏或来自不兼容版本,**When** 触发点被读取,**Then** 降级为"只建议"并从零重学,不中断会话、不臆测晋升态
8. **Given** 情境命中但用户正在执行其他任务,**When** 规则已晋升,**Then** 自动执行不抢占用户当前请求

---

### User Story 4 - 触发规则的证据驱动优化 (Priority: P2)

触发规则本身是**数据而非硬编码散文**:每条规则含情境条件、目标流程、确认类别、状态与计数。框架依记录证据评估规则质量——命中率、拒绝率、误报情境(建议了但用户明确不需要)、漏报情境(用户手动调用了某流程而当时无建议)——并据此**提议**调优:收紧过宽的条件、抑制噪声规则、为反复漏报的情境新增规则。调优提议 MUST 附证据(指标与样本数)且经用户确认后生效(规则变更影响后续所有会话,属治理性变更);生效的调优与其证据、确认痕迹一并记录,使触发逻辑可回溯演进。

**Why this priority**: 用户明确要求"持续记录和优化这个埋点逻辑"。它让机制自我修正而非静态腐烂,但依赖 US3 的记录数据积累——无数据则无优化可言,故列 P2 且排在 US3 之后。

**Independent Test**: 注入一段含已知噪声规则(高拒绝率)与已知漏报情境(用户多次手动调用而无建议)的记录历史,运行优化评估,验证:(a) 噪声规则被提议抑制且附证据(拒绝率与样本数);(b) 漏报情境被提议新增规则且附证据;(c) 未经确认时规则集零变更;(d) 确认后变更生效且变更-证据关联可回查;(e) 样本不足的规则未被提议变更。

**Acceptance Scenarios**:

1. **Given** 某规则拒绝率显著偏高且样本充足,**When** 优化评估运行,**Then** 产出附证据的抑制/收紧提议,而非静默改动
2. **Given** 用户多次手动调用某流程而当时情境未触发任何建议,**When** 优化评估运行,**Then** 该漏报情境被识别并提议新增规则
3. **Given** 优化提议已产出,**When** 用户未确认,**Then** 规则集零变更
4. **Given** 用户确认了调优,**When** 变更生效,**Then** 变更内容与其证据、确认痕迹一并可回查
5. **Given** 证据样本不足(如某规则仅命中 1 次),**When** 优化评估运行,**Then** 该规则 MUST NOT 被提议变更(小样本抖动防护)

### Edge Cases

- **触发段与用户自定义内容冲突**:用户可能在指令文件里手写了矛盾段落(如"绝不主动建议")。刷新按 additive reconcile 保留用户内容;用户显式关闭优先于框架默认,MUST NOT 用再生覆盖用户意图(FR-004/FR-018)。
- **多 agent 并存 / 同一项目被不同 agent 打开**:学习状态是**项目本地单一状态**,不按 agent 分叉;需明确并发写入语义,以及某 agent 不支持自动执行时的降级(退回"只建议")。
- **情境评估误判**:建议了错误流程。代价被限制为"一行可忽略的建议"——绝不因误判自动执行未晋升流程;误判作为拒绝证据进入 US4 优化闭环。
- **晋升后用户改主意**:自动执行结果不符预期。既有三段式执行报告 + "先执行后修改"语义(需求 044 US3)提供修改途径;用户可复位该规则晋升态。
- **破坏性分类存疑**:某流程是否属破坏性不明确时,按"存疑从严"默认破坏性 → 不晋升。
- **建议风暴**:多条规则同时命中。MUST 收敛为一条最高优先建议(或有界数量),不逐条罗列刷屏。
- **自动执行与用户当前请求冲突**:情境命中但用户正在做别的事。自动执行 MUST NOT 抢占当前请求(FR-019)。
- **阈值配置为 0 或 1**:等于"首次即自动执行"。破坏性豁免仍生效;需明确阈值下限与默认值语义。
- **无 `.specify/` 的独立技能模式**:触发段依赖项目运行时;缺失时机制不适用,如实静默,不报错刷屏。
- **学习状态损坏/缺失/版本不兼容**:降级为"只建议"(从零重学),MUST NOT 中断会话或臆测晋升态。
- **规则集被手工编辑破坏**:学习状态是机器维护面;手工编辑导致的不可解析内容按状态损坏处理(降级 + 如实报告),不静默丢弃用户痕迹。
- **"按需升级"退化为"每回合升级"**:每回合评估(首轮 Q3=B)叠加探测升级(首轮 Q2=C)的最大风险是升级判据过松,导致每回合都跑探测——那就变成了首轮 Q2 选项 B 的成本配上选项 C 的复杂度。护栏:升级判据 MUST 显式声明(FR-005)、探测调用率 MUST 有界并可测(SC-011)。
- **plan 期完整 Constitution Check 被误搬到每回合**:FR-005b 只允许挂每回合的轻量"先查相关文档"义务;若实现把 `plan-template.md` 的逐原则枚举门控搬到每回合,成本不可负担且违反 Principle IX(拒绝投机基础设施)与 token 效率纪律。该误挂 MUST 视为实现缺陷。
- **agent 未遵守指令 → 完全不触发**:指令文件是唯一通道(首轮 Q1=A),没有确定性触发保证。长上下文稀释、agent 忽略常驻指令都会导致整回合零评估。这是**已接受风险**;补偿控制是 US4 的漏报检测(用户手动调用了某流程而当时无建议 → 提议新增/收紧规则),使漏报可观察、可收敛,而非静默失效。
- **种子更新与用户调优冲突**:用户已抑制或收紧某条种子规则,模板升级又带来该规则的新版本。用户已确认的调优 MUST 优先,MUST NOT 被种子覆盖回退(FR-022)——这要求状态里能区分"种子内容"与"用户调优"两个来源,否则一次升级就静默撤销了用户的决定。
- **受控词表覆盖不足**:新情境无法用现有词表表达。当回合如实无建议,该缺口作为漏报证据进入 US4 的词表扩展提议(经 FR-016 用户确认);MUST NOT 由 agent 临场造词——造词会使情境身份不稳定,FR-010 的连续计数随之失效。
- **遥测轮转与晋升计数**:轮转丢弃原始回合行是预期行为。晋升计数 MUST 作为规则上的聚合态而不受影响(FR-009a);若实现把计数做成从原始行重算,一次轮转即等于清空全部学习结果——SC-015 正是为判别该缺陷而设。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `specify init` 与 `/speckit.instructions` MUST 把**主动触发指令段**写入 canonical 指令源(`.specify/instructions.md`),使其经既有 symlink/生成模型抵达每个受支持 agent 的必经指令文件;MUST NOT 要求各 agent 单独维护副本。
- **FR-002**: 触发指令段 MUST 以**引用**表达流程清单(指向命令/技能清单的权威源),MUST NOT 复制命令名、技能名或参数结构的枚举(单一事实源 + token 效率纪律)。
- **FR-003**: 受支持 agent 的必经指令路径 MUST 全覆盖:当前声明却未生成的路径(hermes、opencode)MUST 被补齐生成,或经显式裁定标记为不支持并从声明中移除——MUST NOT 保留"声明存在、审计恒 fail"的状态。
- **FR-004**: 指令文件再生 MUST 同时保留触发段与用户自定义内容(沿用既有 additive reconcile 语义);MUST NOT 因再生丢失任一方。
- **FR-005**: 情境评估 MUST 采用**两级证据预算**(clarify 2026-09-07 裁定):默认只消费已在上下文中的环境信息(近零增量成本);仅当环境信息不足以判定时 MUST 升级到确定性探测程序输出的**状态摘要**。两级都 MUST NOT 全量注入制品原文(token 效率:程序优先 + 摘要优先)。**升级判据 MUST 显式声明**,MUST NOT 交由 agent 临场自由裁量。证据至少覆盖:制品存在性与生命周期阶段、待处理 feedback/自省状态、指令文件时效。
- **FR-005a**: agent MUST 在**每个用户回合**执行情境评估(clarify 2026-09-07 裁定)。评估本身 MUST 静默——无适用流程或状态未变时 MUST NOT 产生任何用户可见输出。**评估节奏与建议节奏 MUST 分离**:每回合评估 MUST NOT 被理解为每回合建议。该裁定的可负担性以 FR-005 的默认近零证据预算为前提,二者 MUST 作为一组约束同时落地,不得只实现其一。
- **FR-005b**: 每回合评估 MUST 作为**既有 constitution 合规分析的后续阶段**挂载,MUST NOT 并列新造一趟独立分析(用户 2026-09-07 指示):先完成 Documentation Map 的"先查相关文档"义务(constitution 合规),再在**同一趟**里进行 speckit 流程选取。挂载 MUST 满足两条边界:① 只挂**每回合轻量义务**,MUST NOT 把 plan 期的完整逐原则枚举门控(`plan-template.md` 的 Constitution Check)搬到每回合;② 顺序 MUST 为 constitution 先行、流程选取在后——被建议的流程本身必须合规,建议 MUST NOT 早于合规分析产出。
- **FR-006**: 情境命中时,agent MUST 产出建议,且每条建议 MUST 含:目标流程的用途说明 + **确切可复制的调用形式**;用户 MUST NOT 需要回忆命令名或参数结构即可采纳。
- **FR-007**: 建议 MUST 为**非阻塞提示**:MUST NOT 阻塞或延后用户当前请求的执行,MUST NOT 引入新的阻塞门控(确认门控回流约束)。
- **FR-008**: 情境无适用流程时,agent MUST 如实不提出建议;MUST NOT 为凑数推荐无关流程。**建议输出**频次 MUST 有界(与 FR-005a 的每回合评估相对照):状态未变不重复产出;多规则同时命中 MUST 收敛为一条最高优先建议或有界数量。
- **FR-009**: 系统 MUST 记录**两类**事件(clarify 2026-09-07 第二轮 R2-Q5 裁定):① **建议事件**——每次建议的结果(命中规则、情境身份、情境快照(摘要级)、用户响应(采纳/拒绝/忽略)、时间);② **每回合最小遥测行**——回合标识、是否升级探测、是否产出建议、constitution 合规分析是否已完成。②是 SC-011(探测升级率)与 SC-012(顺序契约)的**唯一分母来源**:静默回合若不落痕迹,这两条护栏即不可测。两类记录 MUST 落在**项目本地机器维护状态**中,与指令文件分离,使 FR-004 的再生不影响它。
- **FR-009a**: 每回合遥测 MUST 有界:行格式紧凑、**保留窗口显式声明并可轮转**,MUST NOT 成为无限增长的存储面。轮转 MUST NOT 影响晋升计数——晋升计数 MUST 作为规则上的**聚合态**维护,MUST NOT 依赖从原始遥测行重算(否则轮转即等于清空学习结果)。
- **FR-010**: 同一(情境→流程)规则被**连续采纳**达阈值(默认 3,可配置)后 MUST 晋升为免确认自动执行;**一次拒绝 MUST 重置该规则的连续计数**(clarify 2026-09-07 第二轮 R2-Q3 裁定:晋升编码的是**稳定的当前偏好**而非历史累计——拒绝本身即偏好已变的证据)。阈值下限与默认值语义 MUST 显式声明。该计数的良定义以 FR-023 的受控情境身份为前提:身份不稳定则"同一情境"无从判定,计数失去意义。
- **FR-011**: **破坏性/不可逆流程 MUST NOT 晋升**,无论采纳次数。破坏性判据 MUST 以 `.specify/shared/guidelines/confirmation-gates.md` 的两级分类与破坏性清单为唯一权威;分类存疑时 MUST 按"存疑从严"默认破坏性(不晋升)。本特性 MUST NOT 新增或改写该分类判据。
- **FR-012**: 自动执行 MUST 产出既有三段式执行报告(执行内容/产出工件/修改途径),MUST NOT 静默执行;用户 MUST 能复位单条规则的晋升态或全局降级为"只建议"。
- **FR-013**: 学习状态 MUST 跨会话持久、可读、可复位;状态缺失/损坏/版本不兼容时 MUST 降级为"只建议"(从零重学),MUST NOT 中断会话或臆测晋升态。
- **FR-014**: 触发规则 MUST 以**数据形态**存在(每条含:情境身份(取自 FR-023 的受控词表)、目标流程、确切调用形式、确认类别、**来源(种子/学习)**、状态、连续采纳计数、命中与拒绝统计),MUST NOT 硬编码为不可修订的散文。
- **FR-015**: 系统 MUST 依记录证据评估规则质量(命中率、拒绝率、误报、漏报——用户手动调用了某流程而当时无建议),并据此**提议**调优(收紧/抑制/新增);提议 MUST 附证据(指标与样本数)。
- **FR-016**: 规则调优 MUST 经用户确认后生效;未经确认 MUST NOT 变更规则集。生效的调优 MUST 与其证据、确认痕迹建立可回查关联。
- **FR-017**: 证据样本不足时 MUST NOT 提议变更对应规则(小样本抖动防护);样本量下限 MUST 显式声明。
- **FR-018**: 用户 MUST 能全局关闭主动触发(关闭后不产出建议、不自动执行);用户显式关闭 MUST 优先于框架默认,MUST NOT 被指令再生覆盖。
- **FR-019**: 自动执行 MUST NOT 抢占用户当前请求;情境命中但用户正在执行其他任务时 MUST 让位或延后。
- **FR-020**: 学习状态与触发机制 MUST 保持**项目本地**:MUST NOT 自动传输任何内容到项目外(与 feedback 上行同纪律——仅人工送达),MUST NOT 跨项目共享学习结果。
- **FR-021**: 计数-阈值-晋升机制 MUST 优先复用既有引擎范式(与 `feedback-utils.py` 的阈值解析/提示判定同构),MUST NOT 新建平行机制(单引擎坍缩纪律)。
- **FR-022**: 系统 MUST 随 `templates/` 分发一份**出厂种子规则集**,使新项目**第一天即产出建议**(无冷启动;clarify 2026-09-07 第二轮 R2-Q2 裁定,来源范围经 analyze 2026-09-08 订正)。种子规则 MUST **从框架既有文面派生**,MUST NOT 另行撰写第二份流程知识(单一事实源纪律)。派生来源有两类,且每条规则的 provenance MUST 声明其类别(`anchorKind`):① **`handoffs`** —— 25 个命令模板的 `## Handoffs` 条件式(situation→flow 知识的主要载体);② **`owning-section`** —— 当**没有任何** `## Handoffs` 段点名该流程时,取拥有该流程触发条件的文档段落。**订正依据(实测)**:全部 25 个 Handoffs 段的交叉扫描表明,`/speckit.feedback`、`/speckit.history`、`/speckit.todo`、`/speckit.sanitize`、`/speckit.session`、`/speckit.interview`、`/speckit.research`、`/speckit.derive` 在**任何** Handoffs 段中都不出现;其中 `/speckit.feedback` 的触发条件("record 输出的 `should_prompt` 为真 → 邀请用户走 `/speckit.feedback package`")确实存在,但其 owner 是 `shared/workflow/feedback-step.md`(L79–84、L101–113),不是任何 Handoffs 段。故原判"种子规则全部从 Handoffs 派生"对这一类流程**不成立**;订正后仍守住 FR-022 的实质义务:**知识来自框架既有文面,零新撰写**。种子规则 MUST 与学习所得规则**同构**(携带 FR-014 全部字段,含确认类别),FR-011 的破坏性豁免对种子规则同样生效。项目学习 MUST 在种子之上调优/抑制/新增;**用户已确认的调优 MUST NOT 被后续种子更新覆盖回退**。
- **FR-023**: 情境身份 MUST 取自一个**小型受控词表**:情境 = (特性生命周期阶段, 待处理信号集)。同一项目状态 MUST 跨会话稳定解析到同一身份,使 FR-010 的连续计数良定义。MUST NOT 以完整制品状态指纹作为身份——指纹近乎每次唯一,计数器永不到阈值,晋升与 US3 整体失效。词表 MUST 可扩展,但扩展 MUST 经 FR-016 的用户确认通道,MUST NOT 由 agent 临场造词;词表未覆盖的情境当回合如实无建议(FR-008)。

### Key Entities *(include if requirement involves data)*

- **主动触发点 (Proactive Trigger Point)**: agent 必经指令路径上的常驻行为契约落点。属性:canonical 源、各 agent 抵达路径、内容形态(引用式)、开关状态。与 **Feedback Probe**(反馈插点,wrap-up 事实捕获点)是不同概念——后者记录**已发生运行**的自评,前者在运行**之前**提议该运行什么;二者 MUST NOT 混用术语。
- **情境身份 (Situation Identity)**: 受控词表中的一个取值,形如 (特性生命周期阶段, 待处理信号集)。它是"同一情境"的判定单位,因而也是 FR-010 连续计数得以良定义的前提;词表可扩展但只能经用户确认通道扩展。与**情境快照**不同:快照是某次评估的摘要级证据留痕,身份是可跨会话复现的粗粒度标签。
- **建议规则 (Suggestion Rule)**: 一条(情境身份 → 目标流程)映射,是触发逻辑的最小可优化单元。属性:标识、情境身份、目标流程(命令或技能)、确切调用形式、确认类别(可逆/破坏性)、**来源(种子/学习)**、状态(active/suppressed/promoted)、连续采纳计数、命中/拒绝统计。规则集整体构成可修订的数据面;种子规则与学习规则**同构**,只在来源与可覆盖性上有别。
- **建议事件 (Suggestion Event)**: 一次建议的发生记录。属性:命中规则、情境身份、情境快照(摘要级)、用户响应(采纳/拒绝/忽略)、时间。是**计数晋升与规则优化的唯一证据来源**。
- **回合遥测 (Turn Telemetry)**: 每个用户回合的最小遥测行(无论该回合是否产出建议)。属性:回合标识、是否升级探测、是否产出建议、constitution 合规分析是否已完成。是 **SC-011(探测升级率)与 SC-012(顺序契约)的唯一分母来源**;有保留窗口、可轮转,轮转不影响晋升计数。
- **晋升态 (Promotion State)**: 规则的自动执行资格。属性:连续采纳计数、生效阈值、是否晋升、破坏性豁免标记(恒不晋升)、用户复位痕迹。它是规则上的**聚合态**,MUST NOT 由原始遥测行重算——故遥测轮转不清空学习结果。
- **触发学习状态 (Trigger Learning State)**: 承载规则集、晋升态、建议事件与回合遥测的项目本地机器维护状态。与指令文件分离(再生不影响);跨会话持久;可复位、可全局关闭;遥测部分有界可轮转;损坏时降级为"只建议"。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 在一个新初始化的项目上,受支持 agent 的必经指令路径**覆盖率 100%**(含当前声明却未生成的路径),且各路径所见触发指令语义一致(同源,分叉副本数为 0)。
- **SC-002**: 触发指令段中命令名/技能名/参数结构枚举的**复制计数为 0**——均以引用表达。
- **SC-003**: 在一组覆盖生命周期的代表性项目状态样本上(≥6 种:仅 requirements、requirements 含未决澄清、已澄清未规划、plan 就绪无 tasks、tasks 就绪未实现、feedback 达阈值),建议指向正确下一流程的**准确率 ≥ 90%**,且 **100%** 的建议含确切可复制调用形式;用户全程需回忆的命令名数为 **0**。
- **SC-004**: 在"无适用流程"样本上,**无关建议产出数为 0**(不硬凑);单次会话内状态未变时的**重复建议数为 0**。
- **SC-005**: 同一规则连续采纳达阈值后,下一次情境命中的**确认询问数为 0**(自动执行生效);被归类破坏性的流程在**连续采纳 ≥5 次后的自动执行数为 0**(硬安全判据,零容忍)。度量方法取更强判据:契约与测试一律以**连续 10 次采纳**执行该断言(`trigger-engine.md` C-17 / `quickstart.md` 场景 4),覆盖并强于本条的 ≥5 次下限。
- **SC-006**: 一次拒绝后连续计数重置的**正确率 100%**;指令文件再生后学习状态(计数与晋升态)的**丢失数为 0**。
- **SC-007**: 在注入已知噪声规则(高拒绝率)与已知漏报情境的记录历史上,优化评估**识别二者并附证据**的命中率 100%;未经确认时**规则集变更数为 0**;样本不足规则被误提议变更的次数为 **0**。
- **SC-008**: 建议对既有工作流的侵入度:因建议导致用户当前请求被阻塞或延后的**次数为 0**(回流约束);门控扫描的**新增违规数为 0**,**且扫描总数不超过既有契约上限**——上限由 `tests/contract/test_confirmation_gates_sweep.py` 依 `.specify/specs/044-reduce-confirmation-flows/baseline.json` 派生(total × 25%),实测**当前余量为 0**;而 `templates/*.md` 在扫描范围内,故触发段文案 MUST NOT 命中任何 BLOCKING 模式,否则同时打爆该契约测试。
- **SC-009**: 全局关闭后,**建议产出数与自动执行数均为 0**;关闭状态在指令再生后仍生效。
- **SC-010**: 学习状态不可读(缺失/损坏/版本不兼容)时,**会话中断数为 0**且降级为"只建议"的行为可观察。
- **SC-011**: 在一段连续 ≥20 个回合的普通工作中,确定性探测程序的**调用次数 / 评估调用次数 ≤ 20%**(默认上限;实现可调整但 MUST 显式声明),证明"按需升级"未退化为"每回合升级";且其中无适用流程的回合,本机制的**用户可见输出数为 0**。**分母口径(诚实声明)**:遥测行只在 `assess` 被调用时产生,故分母是**评估调用数**而非原始用户回合数;若 agent 整回合跳过评估,该回合不留痕,FR-005a 的"每回合"义务**无法仅凭遥测证明**,须辅以会话侧观察(见 Measurement Sources)。
- **SC-012**: 建议在 constitution 合规分析完成之前产出的**次数为 0**(顺序契约);合规分析与流程选取合并为**同一趟**而非并列两趟的可观察证据成立(每回合分析趟数为 1)。
- **SC-013**: 出厂种子规则集中,可在**框架既有文面**定位到来源的比例为 **100%**——按 FR-022 的两类来源分别计:`anchorKind=handoffs` 的规则须能在其 `provenance.file` 的 `## Handoffs` 段内定位,`anchorKind=owning-section` 的规则须能在其 `provenance.file` 的对应段落内定位;**新撰写的 situation→flow 知识条数为 0**(单一事实源)。且一个**从未积累任何学习记录**的全新项目,在首个生命周期情境上即产出正确建议(冷启动建议数为 0 即不达标)。
- **SC-014**: 同一项目状态在跨会话的 ≥5 次独立评估中解析到**同一情境身份的一致率为 100%**(FR-010 连续计数良定义的前提);以完整制品状态指纹作身份的实现,其晋升触发率恒为 0(该反模式的判别证据)。
- **SC-015**: 回合遥测的**存储行数在每次追加后恒 ≤ 显式声明的保留窗口**(追加即截断,故为**恒真不变量**而非仅轮转后成立);在窗口 50 下制造 ≥60 行(`quickstart.md` 场景 5 的实际口径)后,行数 ≤50;执行一次显式 `rotate` 或任意一次追加后,晋升计数与规则状态的**丢失数为 0**。

### Measurement Sources & Collection Methods

- **SC-001 Source**: 干净临时根上 `specify init` 后的路径存在性与内容一致性检查(逐 agent 路径比对 canonical 源),由 `trigger-section.md` C-1/C-10/C-12 结构契约测试固化。**产出任务:T013(自动化)+ T015(人工走查 `quickstart.md` 场景 1)**。
- **SC-002 Source**: 触发段文本与命令/技能清单权威源的交叉文本检查——枚举字符串出现计数(同需求 049 SC-005 手法),由 `trigger-section.md` C-5 固化(检测模式见该条款)。**产出任务:T008/T014(契约测试)+ T015**。
- **SC-003 Source**: 隔离 worktree 构造的 **≥6 种生命周期状态矩阵**(仅 requirements、requirements 含未决澄清、已澄清未规划、plan 就绪无 tasks、tasks 就绪未实现、feedback 达阈值),逐状态记录建议内容、正确性人工判定、调用形式可复制性,准确率按状态汇总;基线为 0%(机制不存在)。**产出任务:T028(状态矩阵走查,本条为其显式交付物)**。
- **SC-004 Source**: 两部分 —— ① "无适用流程"状态(如 `non-feature` 且无信号)的无关建议计数,取 `quickstart.md` 场景 3 的 20 回合遥测;② 同会话内同一情境重复评估时的**重复建议计数**,依赖引擎的会话级去重(`trigger-engine.md` C-20)。**产出任务:T028(①)+ T030/T050(②,含跨回合观察)**。
- **SC-005 Source**: 触发学习状态中的事件记录与晋升态字段回查;破坏性流程以**连续 10 次采纳**实测(强于本条 ≥5 次下限),由 `trigger-engine.md` C-17 与 `tests/integration/test_trigger_promotion.py` 固化。**产出任务:T029(自动化)+ T036(人工走查场景 4)**。
- **SC-006 Source**: ① 事件记录序列的计数核对(一次拒绝后归零),由 `tests/integration/test_trigger_promotion.py` 固化;② 指令文件再生前后的学习状态 diff(零丢失),须在走查中**实际运行** `generate-instructions.sh` 后比对 `.specify/memory/trigger/index.json`。**产出任务:T029(①)+ T036(②,本条为其显式交付物)**。
- **SC-007 Source**: 注入构造的历史记录(高拒绝率规则 + 漏报情境)+ `tune` 产物的提议清单与证据字段人工核对;批准前后的规则集 diff;小样本守卫由被跳过规则的 `notes[]` 具名回显证明。**产出任务:T037(自动化)+ T043(人工走查场景 6)**。
- **SC-008 Source**: ① `scan-confirmation-gates.py --summary` 的 violations 计数与 total(须 ≤ T002 冻结的前值)+ `tests/contract/test_confirmation_gates_sweep.py` 绿;② 因建议导致用户当前请求被阻塞/延后的**事件计数**,取 dogfood 会话观察。**产出任务:T047(①)+ T050(②,本条为其显式交付物)**。
- **SC-009 Source**: `config --enabled false` 后的会话实测(建议产出数与自动执行数均为 0)+ 指令再生后复测关闭仍生效,由 `tests/integration/test_trigger_promotion.py` 固化。**产出任务:T029(自动化)+ T036(人工走查场景 4 末段)**。
- **SC-010 Source**: 人为构造三态(状态文件缺失 / JSON 损坏 / `schemaVersion` 不兼容)后调用 `assess`,观察退出码为 0、`warnings` 含 `state-unreadable`、`payload.degraded="suggest-only"` 且会话不中断,由 `trigger-engine.md` C-8 固化。**产出任务:T036(三态走查,本条为其显式交付物)**。
- **SC-011 Source**: **FR-009② 的回合遥测行**(机制自产)——按 `escalated` 字段汇总比值,**分母为 `assess` 调用数**(见 SC-011 的口径声明);无适用流程回合的用户可见输出由 `suggested`/`visibleOutput` 字段交叉核对。**产出任务:T028(场景 3 的 20 回合)+ T050(≥20 真实回合 dogfood 读数)**。
- **SC-012 Source**: 同一回合遥测中 `complianceDone` 与 `suggested` 两字段的时序核对(该字段由 `--compliance-done` 传入,见 `trigger-engine.md` C-10/C-14);每回合分析趟数计数,并由触发段在指令文件中的挂载位置(`trigger-section.md` C-3)作结构性佐证。**产出任务:T029/T050**。
- **SC-013 Source**: 种子规则集按 `anchorKind` 分两类做**交叉文本核对** —— `handoffs` 类逐条回溯其 `provenance.file` 的 `## Handoffs` 段,`owning-section` 类回溯其对应段落(如 `shared/workflow/feedback-step.md`),由 `seed-derivation.md` C-6/C-7 固化;另在全新初始化的隔离根上实测首个生命周期情境的建议产出。**产出任务:T016/T019(契约与种子)+ T028(冷启动实测,场景 2)**。
- **SC-014 Source**: 同一构造状态在 **≥5 个独立会话**中的 `assess` 结果比对(`payload.situationId` 一致率),由 `tests/unit/test_trigger_utils_units.py` 的纯函数解析用例覆盖跨会话稳定性;反模式判别取"以制品指纹为身份"实现的晋升触发率(恒 0)。**产出任务:T018(单元)+ T028(≥5 会话实测,本条为其显式交付物)**。
- **SC-015 Source**: 在窗口 50 下制造 ≥60 行遥测,读取行数与声明窗口比对(**追加即截断**,故每次调用后都须 ≤ 窗口);执行显式 `rotate` 与再追加各一次,diff 前后 `rules --format json` 断言晋升计数与规则状态零丢失。**产出任务:T030(自动化)+ T036(人工走查场景 5)**。

## Clarifications

<!-- 
This section will be populated by /speckit.clarify command with questions and answers.
Format: - Q: <question> → A: <answer>
-->

### Session 2026-09-07

- Q: 触发通道范围——仅指令文件常驻指令,还是同时为支持原生 hook 的 agent 增设确定性触发? → A: **仅指令文件常驻指令**(全 6 agent 通用、零适配成本、init 即得;亦最契合 Principle IX「优先最简制品、拒绝投机基础设施」)。接受其代价:触发依赖 agent 遵守指令、无确定性保证,**漏报为已接受风险**,补偿控制是 FR-015 的漏报检测(用户手动调用某流程而当时无建议 → 提议新增/收紧规则),使漏报可观察可收敛而非静默失效。原生 hook 适配层与各 agent hook 能力矩阵移入 Out of Scope。**连带升级**:FR-003 的必经路径全覆盖从"审计整洁"变为**硬前置**——指令文件既是唯一通道,hermes/opencode 路径缺失即等于这两个 agent 完全没有本机制。落地:Overview 1、US1 叙述、FR-003、Edge Cases「agent 未遵守指令」、Out of Scope。
- Q: 情境评估的证据预算——仅用环境信息,还是引入确定性探测程序? → A: **环境信息为主 + 按需升级确定性探测**(两级)。默认只消费已在上下文中的环境信息(近零增量成本,这是 Q3 每回合评估付得起的前提);仅当环境信息不足以判定时升级到确定性探测程序的**状态摘要**,探测仍守摘要优先、不注入制品原文。**升级判据 MUST 显式声明**,不得交由 agent 临场裁量。新增护栏 SC-011(探测调用率 ≤ 20%)防止"按需升级"退化为"每回合升级"。落地:Overview 2、US2 叙述与场景 9/10、FR-005、Edge Cases、SC-011。
- Q: 评估触发时机——每会话一次、每回合、还是仅能力匹配时? → A: **每个用户回合都评估**。与 Q2 裁定互为前提:每回合评估只有在默认证据预算近零时才付得起,故 FR-005 与 FR-005a MUST 作为一组约束同时落地、不得只实现其一。关键区分——**评估节奏 ≠ 建议节奏**:评估每回合**静默**执行(无适用流程或状态未变时零用户可见输出),建议输出仍受 FR-008 频次约束。落地:Overview 2、US2 叙述与场景 1/8、FR-005a、FR-008 措辞、SC-011。
- 用户追加指示(同日):框架已有类似埋点先例——`.specify/memory/constitution.md` 的遵守要求**每个请求都进行分析处理**;处理完 constitution 清单之后可进一步做 speckit 流程选取。→ **核实结论(部分成立,已按实测收敛)**:每回合分析义务确实已存在且正靠必经指令路径投递(`templates/instructions-template.md` Documentation Map 首行 L13 + 常驻指令 L22「ALWAYS check the relevant document from the map above first」+ L90),但**形式化的 Constitution Check 门控是 plan 期而非每回合**(`.specify/templates/plan-template.md:31–33` GATE + `/speckit.plan` 动态枚举全部原则 `templates/commands/plan.md:63–66`)。故存在两级,本特性**只挂轻量的每回合义务**。据此新增 **FR-005b**(顺序契约:constitution 合规先行、流程选取在同一趟接续;禁止把 plan 期完整枚举门控搬到每回合)、US2 场景 11、SC-012、Edge Cases「plan 期完整 Constitution Check 被误搬到每回合」,并补两条现状锚点。该指示同时**强化了 Q1=A 与 Q3=B 的可行性**:每回合触发在实践中已有先例可循,不是新造纪律。

### Session 2026-09-07(第二轮 — `/speckit.clarify` Mode A)

> 标号约定:本轮用 **R2-Qn** 前缀,以区别同日首轮(requirements 阶段)的 Q1–Q3。首轮三项见上一 session 块;两块均为历史记录,只追加不改写。

- R2-Q1: Feature 绑定——新建 Feature 还是绑既有 Feature? → A: **新建 Feature 050 Proactive Flow Trigger**。按绑定先例启发式核验 6 个候选的同胞吸收证据(022 吸收 4 个、028 吸收 3 个,均强吸收但主题不符;032/008/001/046 各 1 个),结论是无既有 Feature 拥有本能力——每个候选只匹配一个侧面(032/008=投递载体、001=能力前身但静态命令域、022=仅 FR-003 议题、028=计数机制先例、046=破坏性判据消费)。决定性先例是 **032**:投递载体完全相同却仍自成 Feature,确立"以指令段形式嵌入是投递事实、非归属事实"。落地:`Related Feature` 解析 + 绑定依据表;新建 `.specify/memory/features/050.md`;`features.md` 索引行 + 总数 49→50;相邻 Feature 032 加反向交叉引用。
- R2-Q2: 规则集冷启动——出厂是否带种子规则? → A: **带种子,且从既有 `## Handoffs` 条件式派生**。理由:若从空开始,新项目第一天零建议,与"用户不记得命令名也能用上框架"的特性目的自相矛盾。关键约束是**派生而非撰写**——25 个命令模板的 Handoffs 已是 situation→flow 知识的既有真源(实测例:`templates/commands/requirements.md` 的「若含 `[NEEDS CLARIFICATION]` 或 `Related Feature: Need clarification` → `/speckit.clarify`;否则 → `/speckit.plan`」),另撰一份即造出第二真源。落地:**新增 FR-022**、FR-014 增"来源(种子/学习)"字段、Key Entities 建议规则增来源、US2 场景 12 与 Independent Test (f)、**新增 SC-013**(派生比例 100% / 新撰写 0 条 / 冷启动建议数 >0)、新增 Edge Case「种子更新与用户调优冲突」、Assumptions 一条。
- R2-Q3: 阈值语义——连续采纳还是累计? → A: **连续采纳,一次拒绝即重置**(首轮遗留未决项,本轮裁定)。晋升编码稳定的**当前**偏好而非历史累计;拒绝本身即偏好已变的证据。累计语义会让一条跨月被采纳 3 次、其间被拒 10 次的规则也自动执行。落地:FR-010 去掉"推断默认待确认"标注并写入裁定理由;Assumptions 阈值语义条改为已决;US3 场景 3 据此成立(无需改动)。
- R2-Q4: 情境身份——什么算"同一个情境"? → A: **粗粒度受控词表**:情境 = (特性生命周期阶段, 待处理信号集)。该问题是 FR-010 计数良定义的前提:若以完整制品状态指纹为身份,指纹近乎每次唯一 → 计数器永不到阈值 → 晋升与 US3 整体失效。粗粒度与 R2-Q2 的 Handoffs 派生天然对齐(那些条件式本就是粗粒度的)。词表扩展只经 FR-016 确认通道,禁止 agent 临场造词。升级路径(粗身份计数 + 细条件触发)留待 plan 发现粗粒度确实抹平关键差异时再付。落地:**新增 FR-023**、FR-014/FR-010 引用、**新增 Key Entity 情境身份**(并与其区分"情境快照")、US2 场景 13、**新增 SC-014**(跨会话一致率 100% + 指纹反模式判别)、新增 Edge Case「受控词表覆盖不足」、Assumptions 一条。
- R2-Q5: SC-011/SC-012 的遥测缺口——两条 SC 引用的"回合级观察记录"无 FR 生产 → A: **扩展 FR-009,每回合记一行最小遥测**(回合标识、是否升级探测、是否产出建议、合规分析是否已完成)。SC-011 是"按需升级"退化为"每回合跑脚本"的**唯一护栏**,不可测即等于无护栏;事后法证(会话日志分析)路线因只读且 per-CLI 分叉(现有适配器仅 codex/qoder/cursor,不覆盖 hermes/copilot)与首轮 Q1=A 的全 agent 通用取向冲突,故不取。附带裁定:遥测 MUST 有界(紧凑行 + 显式保留窗口 + 可轮转),且晋升计数 MUST 是规则上的聚合态、不由原始行重算——否则轮转即清空学习结果。落地:**FR-009 改写为两类记录** + **新增 FR-009a**、**新增 Key Entity 回合遥测**、晋升态实体补"聚合态"约束、SC-011/SC-012 Source 改为指向自产遥测、**新增 SC-015**(有界 + 轮转零丢失)、新增 Edge Case「遥测轮转与晋升计数」。

**第二轮后置校验**:`Related Feature` 已解析(不再是 `Need clarification`);FR 由 23 增至 **26**(FR-001…FR-023 + FR-005a / FR-005b / FR-009a);SC 由 12 增至 **15**;Key Entities 由 5 增至 **7**(新增 情境身份、回合遥测);Acceptance Scenario 由 30 增至 **32**;Edge Case 由 14 增至 **17**;首轮 session 块 4 行**逐字保留**,本轮追加 5 行(条目计数 4→9,严格递增,符合 append-only 不变式)。

### Session 2026-09-07(第三轮 — `/speckit.plan` Phase 0 设计访谈)

> 标号约定:本轮用 **P-Qn** 前缀(首轮 Q1–Q3、第二轮 R2-Q1…R2-Q5 见上两块)。本轮属**设计层裁定**,不改变任何 FR/SC 的义务内容,只裁定其制品形态;唯一对规格正文的改动是一处事实订正。

- P-Q1: FR-012 / FR-016 / FR-018 的用户可见管理面取何种形态? → A: **不新增命令、不新增技能;只落一个 stdlib 引擎,管理意图由 agent 依触发段路由到引擎 action**——与 **glossary 域完全同构**(glossary 无命令,`glossary-utils.py` 由嵌在其他命令里的 `## Glossary` 步骤调用)。理由:① 三个候选里唯一对已钉死计数(复杂命令 19、docs-step 16)、probe 注册表(internal objects 73)与确认门控预算(整数余量 0)**全部零扰动**的方案;② Principle IX 要求优先最简制品;③ **与本特性自身论点一致**——特性目的是"用户不必记得名字",若管理面又是一个必须记住的命令名则自相矛盾,"别再建议这个"/"复位它"本就是自然语言。已否决 B(新增 `/speckit.trigger`:需命令模板 + 4 份 per-tool 副本 + `docs/reference/commands/` + 分类 19→20 + docs-step 16→17 + probe 21→22 + 两个计数契约测试改写)与 C(新增技能:probe skill-wrapup 31→32,且 git-workflow 先例只是单一状态文件的块维护,不含证据聚合与调优提议)。
- P-Q2: FR-022 的"从既有 `## Handoffs` 派生"取何种制品形态? → A: **一次性撰写种子文件,但每条规则携带 provenance(指回具体 `templates/commands/<x>.md` 的 Handoffs 行)+ 一个漂移检出契约测试**。该形态落在 `.specify/shared/guidelines/one-source-of-truth.md` 明确许可的**合法副本**类别("a literal pinned in a test to detect drift"):漂移是**被检出**而非被防止,某条 Handoffs 改了而种子未跟即测试失败并指出具体规则。**冲突根源已核实**:`## Handoffs` 是自然语言散文,确定性解析不可行,而 Program-First 不允许把散文解析交给 LLM 再称之为"确定性派生"——FR-022 的字面("派生")与理由("不造第二真源")在此张力下,取"可检出漂移的 provenance 副本"为最小代价满足理由的形态。已否决 B(给 25 个模板加结构化 frontmatter 键:需改 25 模板 + 再生 100 份 per-tool 副本 + 扩 `src/specify_cli/__init__.py:1466–1473` 块终止符元组,且与既有 `handoffs:` 键**同名不同义**易混淆)与 C(正则启发式解析散文:脆弱,改措辞即静默漏规则)。
- **事实订正(计划期发现的规格缺陷)**:现状锚点原写「模板现有 **17** 个章节」,实测 `templates/instructions-template.md` 为 **14 个 `## ` 章节 / 合计 17 个标题**(含 H1 与 1 个 `###`)。**14 才是关键数字**——`generate-instructions.sh` 的 additive reconcile 只按 `(?m)^(## .+)$` 切分,故只有 `## ` 级章节会注入既有 `.specify/instructions.md`,`###` 子节与既有 `##` 章节内部的文案改动不传播。已就地订正该条锚点(属事实修正,非 scope 变更,不触及任何 FR/SC)。
- **本轮探索核实的关键事实**(修正/确认了此前记录):
  - 既有 `handoffs:` frontmatter(**20/25** 模板)编码的是 **agent dispatch**(`label` / `agent` / `prompt` / `send`),与 `## Handoffs` 散文段**同名不同义**;`src/specify_cli/__init__.py:1471` 仅把它当作 `scripts:` 块的**终止符 token**,从不消费其条目内容 → situation→flow 知识确实只存在于散文段(P-Q2 冲突根源的直接证据)。
  - `sync-mirrors.py --check` 当前 **exit 0 全绿**(templates 21 / skills 448 / agents 2 / scripts 102 / shared 33,零 MISS/DIFF/ORPHAN)。**Feature 049 记录的 git-fleet 6 MISS 基线已失效**,故全树 exit-0 门禁可用,049 的 `--only` 范围化 workaround 不再需要。
  - additive reconcile **会**把新增 `## ` 章节注入既有 `.specify/instructions.md`(精确整行集合差 + 按模板顺序锚定插入),由 `tests/contract/test_instructions_section_propagation.py` 守卫 → 触发段自动传播到已初始化项目,无需逐项目手工添加(FR-001/FR-004 的可行性得证)。
  - `scripts` 镜像对为 **STRICT**(mirror-only 文件报 ORPHAN 并 exit 2),故新引擎必须同时落 `scripts/python/` 与 `.specify/scripts/python/`。

**第三轮后置校验**:FR 计数 **26**、SC **15**、Key Entities **7**、User Story **4** 均**未变**(本轮只裁定制品形态);现状锚点 1 条就地订正;Clarifications 条目计数 **9 → 13**(严格递增,前两轮 4 + 5 行逐字保留);session 标题 2 → 3。

### Session 2026-09-08(第四轮 — `/speckit.analyze` 发现项的订正)

> 标号约定:本轮用 **A-Qn** 前缀(首轮 Q1–Q3、第二轮 R2-Q1…R2-Q5、第三轮 P-Q1…P-Q2 见上三块)。本轮不是新的用户裁定,而是 analyze 只读分析(37 条发现:1 CRITICAL / 7 HIGH / 19 MEDIUM / 10 LOW,其中 CRITICAL 与 HIGH 全部经 fresh-context 独立验证)后、经用户授权对工件做的订正。以下仅记**触及 requirements.md 本身**的三项;其余落在 plan / data-model / contracts / tasks / quickstart / feature-ref / Feature 记录,由各自文件的订正承载。

- A-Q1: FR-022 声称种子规则"从既有 `## Handoffs` 条件式派生",但实测 **9/14 条 provenance anchor 不成立** → A: **订正 FR-022 的派生来源为两类**,并要求 provenance 声明 `anchorKind`。实测依据(对全部 25 个 `templates/commands/*.md` 的 `## Handoffs` 段做逐流程交叉扫描):`/speckit.checklist` 仅见于 plan·tasks 的 Handoffs、`/speckit.analyze` 仅见于 implement·tasks、`/speckit.review` 仅见于 implement·todo、`/speckit.docs` 仅见于 sanitize、`/speckit.instructions` 见于 agents·docs·feedback·history·sanitize·skills·team、`/speckit.constitution` 见于 feature·history、`/speckit.skills` 仅见于 agents(且该处是"若 agent 依赖新技能"的**意图驱动**而非状态驱动);而 `/speckit.feedback`、`/speckit.history`、`/speckit.todo`、`/speckit.sanitize`、`/speckit.session`、`/speckit.interview`、`/speckit.research`、`/speckit.derive` 在**任何** Handoffs 段中都不出现。其中 `/speckit.feedback` 的触发条件确实存在于框架文面,owner 是 `shared/workflow/feedback-step.md`(L79–84、L101–113:`should_prompt` 为真 → 邀请 `/speckit.feedback package`)。**故订正为两类来源(`handoffs` / `owning-section`),FR-022 的实质义务不变**:知识一律来自框架既有文面、零新撰写。连带:命名情境由 14 收敛为 **13**(删除 s14 → `/speckit.skills`,因无状态可触发它,其原锚点 `skills.md:36,41` 亦落在 Handoffs 段之外),其余 7 条 anchor 改指真实点名该流程的模板。
- A-Q2: SC-005 / SC-011 / SC-013 / SC-015 与下游契约、测试、走查的口径不一致 → A: **四条就地订正,取更强或更诚实的口径**。SC-005 破坏性采纳次数由 5 改为"≥5,度量取契约与测试实际使用的 **10 次**"(`trigger-engine.md` C-17);SC-011 显式声明**分母为 `assess` 调用数而非原始用户回合数**——遥测行只在 `assess` 被调用时产生,agent 整回合跳过评估即不留痕,故 FR-005a 的"每回合"义务无法仅凭遥测证明(诚实口径,不掩盖度量边界);SC-013 改为按 `anchorKind` 分两类核对(与 A-Q1 一致);SC-015 由"轮转后不超窗口"改为**"每次追加后恒 ≤ 窗口"的恒真不变量**(追加即截断),并把测试口径写明为窗口 50 / 制造 ≥60 行,与 `quickstart.md` 场景 5 实际执行的一致。
- A-Q3: 15 条 SC 中 **7 条没有任何产出其度量的任务**(SC-003 需 ≥6 状态矩阵而走查只覆盖 1 种、SC-004 的重复建议半边、SC-006 的再生 diff 半边、SC-008 的阻塞事件计数、SC-010 的三态降级、SC-012 因 A-Q4 而空洞、SC-014 的 ≥5 会话比对)→ A: **重写 Measurement Sources,为每条 SC 具名产出任务**(T013/T015、T028、T029/T036、T037/T043、T047/T050、T018/T028、T030/T036 等),并把此前只写"人工观察"的 SC-008 ②、SC-011、SC-012 明确挂到 T050 的 dogfood 读数上。tasks.md 侧相应扩写 T028 / T036 / T050 的交付物清单,使"SC 有度量源"从声明变为可核对。
- 关联订正(不落本文件,记录于此以备追溯):**A-Q4** `complianceDone` 原先无输入通道(C-10 的封闭 flag 集不含任何合规标志)致 SC-012 空洞、C-14 的 `ordering-violation` 分支为死代码 → 契约新增 `--compliance-done`(封闭 flag 集 19 → **20**);**A-Q5** 情境身份 `s03`/`s13` 同为 `(no-spec, ∅)` 违反 data-model 自身的 V1.3 且使 C-12 的"唯一身份"不可满足 → 信号枚举由 9 扩为 **12**(新增 `checklist-absent`、`feature-index-absent`、`constitution-absent`),`s05` 的 `checklist-absent` 越界问题一并消解;**A-Q6** FR-019(不抢占当前请求)与 FR-020(项目本地、不自动外传)原先**零机械覆盖**且 feature-ref 的映射指向不相干条款 → `discipline-doc.md` 把原先无编号的"各章节必须承载的规范内容"表提升为编号条款 C-8…C-15(含 FR-019 的不抢占),`trigger-engine.md` 新增 C-19(禁网络能力 import,机械断言 FR-020)与 C-20(会话级重复建议抑制,补 FR-008 的频次有界);**A-Q7** plan.md 把 Principle XIV 记为 Pass 的依据(种子属 `one-source-of-truth.md` 的"a literal pinned in a test to detect drift")经逐字核对该指南 L35–43 判定**文本上不成立**(guard copy 须"pinned inside a test"且"serves the build, never the reader",而种子是 `templates/` 下随包分发、被引擎每回合消费的运行时制品,守卫它的是另一个文件;三类合法副本均不符)→ plan.md 改记 **XIV ⚠ Partial** 并补 Complexity Tracking 论证,Constitution Check 由 14/14 Pass 变为 **13 Pass / 1 Partial**;设计本身保留(分歧由 C-7 变为响亮失败、散文不可确定性解析使替代方案确实被封死),不通过重新解释指南来清账。

**第四轮后置校验**:FR 计数 **26**(FR-022 就地订正,未增删)、SC **15**(SC-005/011/013/015 就地订正)、Key Entities **7**、User Story **4** 均未变;Measurement Sources 15 条全部具名产出任务;前三轮 session 块 **13 行逐字保留**,本轮追加 4 行(条目计数 **13 → 17**,严格递增);session 标题 3 → 4。

## Out of Scope

- 既有命令/技能被**直接调用**时的行为变更——本特性只新增"提议与晋升"层,不改被提议流程的内部语义。
- Feedback Introspection(需求 047)内部流程的改写——本特性可消费其状态作为情境证据,不重定义自省。
- 确认门控两级分类、破坏性清单与回流约束的改写——以 `.specify/shared/guidelines/confirmation-gates.md` 为唯一权威判据,本特性只消费不修改。
- 跨项目/全局的学习与规则共享;任何自动对外传输(人工送达纪律不变)。
- 各 agent **原生 hook 适配层与 hook 能力矩阵**——clarify 2026-09-07 已裁定指令文件为**唯一**触发通道,本特性不建任何 agent 原生 hook;若未来需要确定性触发保证,另立特性。
- **plan 期完整 Constitution Check 门控的每回合化**——本特性只挂每回合的轻量合规义务(FR-005b);逐原则枚举门控仍限 plan 期,其语义与位置不变。
- constitution 本身的改写(原则增删、版本变更、Sync Impact Report)——走 `/speckit.constitution`,本特性只消费其既有的每回合合规义务。
- 语音/输入模态的特殊处理(沿用既有 glossary 协议)。
- 触发逻辑的可视化仪表盘/图形呈现。
- 破坏性流程的自动执行——永久排除,非阶段性取舍。

## Assumptions

- **交付通道**复用既有 symlink 模型与 `generate-instructions.sh`,不新增兼容文件类型。
- **学习状态落盘**采用既有"机器维护 + 受管块/独立文件"范式(参照 `.specify/git-workflow.md`、`.specify/memory/features.md`、`implement-loop.local.md`),与指令文件分离,使再生与学习互不干扰。确切路径、格式与是否引擎化管理由 `/speckit.plan` 决定。
- **阈值语义**(clarify 2026-09-07 第二轮 R2-Q3 裁定,**已决**):默认 3,可配置;计数为**连续采纳**、一次拒绝即重置——晋升编码稳定的当前偏好而非历史累计。已落 FR-010;此前的"推断默认、待确认"标注随之失效。
- **出厂种子规则集**(clarify 2026-09-07 第二轮 R2-Q2 裁定):随 `templates/` 分发,使新项目第一天即有价值。**派生而非撰写**——来源是 25 个 `templates/commands/*.md` 既有的 `## Handoffs` 条件式(框架已持有的 situation→flow 知识真源);in-package `memory/` 已有出厂默认数据先例(constitution/features/knowledge/session)。种子的确切制品形态(独立文件 / 由脚本从 Handoffs 派生 / 引擎生成)由 `/speckit.plan` 决定,但"不得另撰第二份流程知识"是 FR-022 的硬约束。
- **情境受控词表**(clarify 2026-09-07 第二轮 R2-Q4 裁定):粗粒度二元组 (特性生命周期阶段, 待处理信号集),小而稳定,与 Handoffs 条件式的粒度天然对齐。词表的具体取值集由 `/speckit.plan` 定义;扩展只经 FR-016 的用户确认通道。若 plan 阶段发现粗粒度抹平了关键差异,升级路径是"粗身份计数 + 细条件触发"的两级形态,而不是一开始就付该复杂度。
- **破坏性判据、存疑从严、回流约束**沿用确认门控治理,不新造分类。
- **计数-阈值机制**与 `feedback-utils.py` 的阈值解析/提示判定同构,优先复用既有引擎范式(FR-021)。
- **挂载位置**:触发段应挂在 Documentation Map 常驻指令的邻近/后续位置,使"先合规、再选流程"成为**同一趟分析的两个阶段**(FR-005b),而不是指令文件里两段互不相干的文字。确切章节位置与措辞由 `/speckit.plan` 决定,且 MUST 遵循既有 additive reconcile 语义(不吞既有章节)。
- **首轮三项裁定相互依赖,不可拆分实现**:首轮 Q1=A(指令文件为唯一通道)、首轮 Q2=C(默认近零证据预算)、首轮 Q3=B(每回合评估)构成一组互相支撑的约束——每回合评估的可负担性依赖近零默认预算;唯一通道的漏报风险依赖 US4 漏报检测补偿;按需升级的纪律依赖 SC-011 的比率上限。**单独实现任一项都会使另外两项的代价失控**(如只做每回合评估而默认走探测,即每回合跑脚本)。已写入 FR-005a 的同时落地约束。
- **与 Constitution 的一致性**:首轮三项裁定共同选择"最简制品"路线(指令文件常驻指令 + 非阻塞建议 + 数据化规则),不引入 agent 运行时、调度器或新执行引擎——符合 Principle IX(框架非运行时平台;优先最简制品、拒绝投机基础设施)与 Principle V(supervisor/编排构造是 agent 解释的提示指令,而非运行时调度器)。
- **术语冲突已识别并显式避让**:项目词汇表中"埋点/插点"当前锚定 **Feedback Probe**(wrap-up 事实捕获点),"自省"当前锚定 **Feedback Introspection**(需求 047)。用户本次输入中的"埋点"指必经路径上的触发落点、"自省"指对当前项目状态的判断,语义不同。本规格采用**主动触发点 / 情境评估**作为独立术语,MUST NOT 复用或覆盖既有两词;新词条按 glossary 协议以 `origin=auto`、`status=proposed` 提交,冲突项待用户确认。
- **标识符预留核查已执行**:`PROACTIVE` / `AUTO_TRIGGER` / `SUGGEST*` 在 `src/`、`scripts/`、`templates/`、`.specify/` 中零占用(可用)。已占用需避让:`SPECKIT_FEEDBACK_THRESHOLD`(环境变量)、`should_prompt` / `resolve_threshold`(函数)、`--action introspect-register` / `INTROSPECTION_DIRNAME` / `introspection_ref`、`AUTO-GENERATED` 标记、`GIT_WORKFLOW_START/END` 标记、`chat.promptFilesRecommendations`。
- **落地层级**:触发段与**出厂种子规则集**随 `templates/` 分发,框架自身与下游采纳项目**同一机制同时受益**(init 即得);**学习所得规则、用户调优与遥测记录不随模板分发**(项目本地,FR-020)。
- **输入模态**:本次为中文键入文本(非语音),glossary 校正协议已先行;上述术语冲突按"歧义从用户"原则显式提交而非静默改写。
- **Feature 绑定已裁定**(clarify 2026-09-07 第二轮 R2-Q1):**新建 Feature 050 Proactive Flow Trigger**,不绑既有 Feature;绑定依据与候选核验见 `Related Feature`。当前 Feature 总数以 `.specify/memory/features.md` 的头部计数为权威,本规格不复制。
- 命令/指令模板改动后,各工具镜像经既有再生脚本处理;`docs/reference/` 下相应参考文档随实现同步更新。
