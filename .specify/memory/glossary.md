# Project Glossary (项目词汇表)

> **Note**: This file is initialized by `/speckit.instructions` and lives beside `constitution.md` / `features.md`. It is the project's single, project-wide vocabulary anchor: it corrects voice/dictated input (homophones, easily-confused words) and doubles as a lightweight domain-knowledge dictionary. It is loaded as ambient context by every `/speckit.*` command via the Documentation Map. See `.specify/shared/workflow/glossary.md` for the correction / enrichment / conflict protocol.

## Authoring Rules

- **Common words are NOT recorded** — only project-specific / domain terms that carry special meaning here.
- **User edits are authoritative (以用户输入为准)** — manual entries win over automatic proposals and are preserved across regenerations; automatic proposals MUST NOT silently overwrite a `user` entry.
- **Conflicts require confirmation** — a new term that collides with an existing entry (same term/different meaning, or a homophone/near-duplicate) is written only after the user confirms the resolution.

## Column Definitions

| Column | Meaning |
|--------|---------|
| Canonical | The agreed project term (unique, case-insensitive). |
| Variants | Comma-separated homophones / easily-confused / dictation-error forms that anchor back to Canonical; `-` when none. |
| Meaning | Brief one-line domain definition. |
| Origin | `auto` (framework-proposed) or `user` (manually authored/confirmed). |
| Status | `proposed` (awaiting confirmation) or `confirmed`. |

## Glossary

| Canonical | Variants | Meaning | Origin | Status |
|-----------|----------|---------|--------|--------|
| Spec Kit | speckit, spec-kit, speck it | The SDD CLI toolkit distributed as specify-cli | user | confirmed |
| SDD | - | Spec-Driven Development: specifications drive implementation | user | confirmed |
| Constitution | - | Project governance principles at .specify/memory/constitution.md | auto | confirmed |
| Feature Index | - | Single source of truth for project capabilities at .specify/memory/features.md | auto | confirmed |
| Reconcile Engine | - | Diff-and-converge engine used by Spec Kit commands to align artifacts with desired state | auto | confirmed |
| Task Complexity Rubric | - | Tiered effort-calibration framework embedded in .specify/instructions.md | auto | confirmed |
| 程序优先 (Program-First) | program first, 程序优先原则 | Token 效率纪律之一:可用固定规则表达的文本/数据判断交由确定性程序执行,不送入大模型 | auto | confirmed |
| 摘要优先 (Summary-First) | summary first, 摘要化访问 | Token 效率纪律之一:机器管理数据文件原文不整体注入大模型上下文,例行消费摘要/投影/节选 | auto | confirmed |
| 升级阶梯 (Escalation Ladder) | escalation ladder, 访问升级阶梯 | 数据访问逐级放宽路径:摘要 → 定向节选 → 有界整读(整读须满足例外情形或记录理由) | auto | confirmed |
| Static Structure | 静态结构 | 团队的 Role × Stage × Type 成员名册 | auto | confirmed |
| Dynamic Structure | 动态结构, 拓扑结构, topology | 团队的协作模式(parallel/serial/iteration/continuous),即成员间的运行时协作关系 | auto | confirmed |
| Goal | 项目级目标, 目标定义, project goal | 项目级一等概念:归档于 .specify/goal/<goal-slug>/ 的目标定义(目标叙述 + 可验证成功判据 + 生命周期状态),作用对象不限于本项目代码(可指向框架自身/代码规范收敛/能力运行结果等任意维度);与 Requirement(只描述本项目源码/配置要实现的 feature)分属不同层面、无必然上下层关系;真源 shared/definitions/goal-definitions.md | user | confirmed |
| Goal Archive | 目标归档, goal 归档 | .specify/goal/ 下全部 goal 定义的集合,即「项目当前与历史目标清单」的物化形态;终态 goal 保留不删 | user | confirmed |
| Goal–Team Binding | 目标—团队绑定, goal 引用 | 团队到 goal 的单向引用(N 团队 : 1 goal),以 goal_slug 声明;团队侧只存身份不存目标副本;一个团队同时只绑一个 goal | user | confirmed |
| Team Goal | 团队目标, team 目标 | 团队服务于哪个项目级 Goal 的**引用**(经 goal_slug);未迁移团队可退化为内联副本,定义存在时以 Goal 定义为权威 | user | confirmed |
| Goal Target | 目标切片, target 切片, 切片 | Goal 之下的 run 级可指派范围切片:身份 T-&lt;nnn&gt;、三态(open/done/dropped)、引擎渲染于 goal.md 的 ## Targets 节;授权只经 /speckit.goal targets,run 经 --target 消费;台账经可选 target_ref 归属;概念真源 shared/definitions/goal-definitions.md → Target Decomposition([[STR-004]]) | auto | confirmed |
| target(消歧) | - | 以下既有 "target" 用法与 Goal Target **无关**,均不改名:团队 territory 的 optimization_target/co_targets(优化对象)、evidence-utils / interview-utils 的 --target 参数(取证/访谈对象) | auto | confirmed |
| Team Summary | 团队总结 | 把团队自身视作项目而产出的累积式状态总结(**派生物**);按 goal 索引落在 .specify/goal/&lt;goal-slug&gt;/summary/ 子树内,与同目录下被撰写的 goal.md 定义结构分离——刷新只写 summary/,不写定义 | auto | confirmed |
| Team Territory | 团队级范围, 团队 territory, team territory | 团队在 team.md 声明的覆盖范围(write/read/forbidden 路径 + 类型化 non_path 条目);把成员级 Territory Division 抬到团队级,四种协作模式通用;缺省该键即「未声明」,不等于空 | auto | confirmed |
| Team Roster | 参与团队名册, goal 名册, roster | 同一 goal 下全部引用团队的**派生**清单(team slug + 声明范围 + 身份类型 + 是否推进),落在 summary/roster.md;每次刷新整体重算,不改 goal 定义 | auto | confirmed |
| Overlap Finding | 重叠发现, 范围重叠, overlap | 同一 goal 下两团队范围的比对结论:overlap(写-写相交,指名路径)/ no-overlap(双方均声明且不相交)/ undecidable(有一方未声明或仅非路径声明) | auto | confirmed |
| Contested Area | 争用区, 写重叠区, contested area | 被两个及以上团队写入的重叠区(write-write finding);MUST 归给唯一团队或转为该 goal 的禁写区,不得停留在双方都可写 | auto | confirmed |
| Coordination Round | 协调轮, 协调机制, coordination round | 针对已检出重叠的一次重划:机制**只检测并提议**(附依据),人裁定后把划分写回各 team.md;机制自身无改写权,提议阶段对 team.md 零写入 | auto | confirmed |
| 工作项四态色板 | 四态色板, work item four-state palette | 已完成/进行中/延期/未开始 四态的统一颜色与冗余符号编码,颜色之外必配符号 | auto | confirmed |
| Agent Template | agent模板, 能力模板, 抽象agent类, capacity template | Agent 三层分类法第一层:能力与行为框架描述,源码 agents/ 角色集由 specify init 安装到 .specify/agents/templates/;真源 shared/definitions/agent-definitions.md | user | confirmed |
| Agent Instance | agent实例, 落地定义, agent definition | Agent 三层分类法第二层:职责描述定义(.specify/agents/instances/*.agent.md、team 名册席位),引用 Agent Template 并绑定具体职责,由命令/技能实例化产生 | user | confirmed |
| Qwen Code CLI | qwen, qwen-code, qwen cli, QWEN.md, .qwen/ | **Agent CLI 工具名**(非模型):曾为 Tier 2 支持的编码 agent,已随 0c300bc8 下线;当前 AGENT_CONFIG 只含 claude/codex/copilot/hermes/opencode/qoder 六工具。与 qwen3 系列模型 ID 是两个不同概念,勿混淆 | user | confirmed |
| qwen3 系列模型 ID | qwen3.7-max, qwen3.7-plus, qwen3-coder-plus, qwen3-rerank | **百炼大模型 ID**(非工具名):cli-setup 的模型四元组仍在使用,状态为活跃。与已下线的 Qwen Code CLI 仅名称形近、语义无关;清理 qwen 工具时 MUST NOT 按 `grep -i qwen` 整体删除,否则会误删 supported-tuples.md / config-agent.sh 中生效的模型配置 | user | confirmed |
| iFlow CLI | iflow, iflow-cli, .iflow/ | **Agent CLI 工具名**:曾为 Tier 2 支持,已随 0c300bc8 下线;不存在与之对应的同名模型 ID | user | confirmed |
| Agent Execution | agent执行, 运行实例, subagent, 子代理 | Agent 三层分类法第三层:定义真正执行时的运行形态,持久产物在 .specify/agents/execution/(configs/scripts 归档,logs 不入库);三种模式(native/virtual/external)见 shared/definitions/subagent-definitions.md | user | confirmed |
| Probe Class(插点类) | probe class, 插点类 | Feedback Probe 两层建模第一层:一类反馈插点的特征定义(收集内容/目标系统切片/收集后处理流程/适用插入位置类型 + internal/external 类别);承载特征,Object 承载落点;真源 shared/definitions/probe-definitions.md § Classes | user | confirmed |
| Probe Object(插点实例) | probe object, 插点实例 | Feedback Probe 两层建模第二层:Probe Class 在当前系统中的实例化(绑定具体流程单元 × 生命周期点);反馈条目经 Object→Class 继承切片与类别;外部 Object 以 ext- 前缀命名空间隔离 | user | confirmed |
| Feedback Probe | 反馈插点, feedback probe, 插点 | 两层建模的显式反馈插点:Probe Class 定义一类插点的特征(收集内容/目标系统切片/收集后处理流程/适用插入位置类型),Probe Object 为其在当前系统中的实例化(绑定具体流程单元×生命周期点);既有 49 个 wrap-up 埋点重构为 Object 并归类到 Class(需求 041) | auto | confirmed |
| Dogfooding | dogfooding, 吃自己的狗粮, 自举, self-hosting, 自食其力, 木匠最顺手的工具都是自己造的, 第一手反馈 | **使用自身(作为开发工具/框架)开发自身**的工程实践,常见于工具/框架类项目;语义三层:吃狗粮(字面层,浅)→木匠自造工具最顺手(契合层,制造者即使用者)→第一手反馈驱动持续改进(目的层,本义);类比编译器自举——用编译器编译其自身源码,只有自身工程表现良好的工具才赢得辅助他人的可信度;Spec Kit 语境=本仓既是框架源又是自己的客户项目(用 /speckit.* 开发 /speckit.* 本身);提及即承载完整语义束(语义三层/自举证明/两顶帽子/Loop A-B/修复落机制侧);真源 shared/definitions/dogfooding-definitions.md §0 | user | confirmed |
| System Slice | 系统切片, feedback slice | 反馈针对的框架部位,沿框架既有组成维度(命令/技能/脚本/模板/文档)取值;由 Probe Class 声明为目标、条目经 Object→Class 继承,作为反馈过滤与统计维度;与 Goal Target 的「目标切片」无关 | auto | confirmed |
| 问题修复 (Problem Fix) | problem fix, 实例修复, 问题侧修复 | 修补机制产生的具体缺陷**实例**(改这份文件/这次输出/这条测试);修复不传播,同机制下次运行复现同类问题;仅允许作机制修复落地前的临时止血且 MUST 留痕;真源 shared/definitions/dogfooding-definitions.md §1 | user | confirmed |
| 机制修复 (Mechanism Fix) | mechanism fix, 机制侧修复, 最机智的修复 | 修补产生实例的**源头**(模板/生成命令注入规则/reconcile 流程/守护契约),下次执行对应命令时修复自然传播到本仓活动文件与全部下游项目;宪法 XI 规定非一次性工件的修复 MUST 落机制侧 | user | confirmed |
| 框架项目 (Framework Project) | framework project, 框架源, 框架作者帽 | 作为 Spec Kit 源代码的仓库角色:skills/、templates/、scripts/、shared/、src/specify_cli/ 为框架源,经发布(git push/打包)供用户安装;影响所有客户项目的修复 MUST 落此侧 | user | confirmed |
| 客户项目 (Client Project) | client project, 宿主项目, 框架用户帽 | 经 specify init 把框架装进自身 .specify/ 的任意项目;本仓库同时是自己的客户项目(自用运行时=本仓 .specify/,三副本拓扑之第二副本);对其运行副本的直接修改属客户侧问题修复,不传播 | user | confirmed |
| History KB (历史知识库) | history, 历史库, .specify/history/ | 当前工具历史会话的**阶段性总结**(/speckit.history 按时间跨度做五维蒸馏:决策/教训/待办/流程/分歧,主题聚合);定位=**时间层面的消息传递**——沿时间轴向前传递阶段成果;**不用于**跨 Session 或跨工序共享(那是 Memory Layer 的职责);数据源天然按工具隔离(每工具各自的会话库) | user | confirmed |
| Memory Layer (记忆层) | memory, 记忆, memory-as-files, session/ + knowledge/ | **跨 Session、跨工具**的通用知识共享层:.specify/memory/session/(短期工作笔记)+ knowledge/(长期蒸馏),经文件系统介质对任意 agent CLI(Qoder/Codex/Claude 等)可读;定位=**空间层面的消息传递**——知识在同一项目空间内对任何会话、任何工具可得;与 History KB(时间层面)正交互补,不互替 | user | confirmed |
| Session(消歧) | - | 以下两种 "session" 无关:(1) **宿主 CLI 会话**——AI agent CLI 的对话运行实例,存于宿主会话库(如 ~/.qoder/projects),由 /speckit.session export 导出、/speckit.history 蒸馏;(2) **memory/session/ 目录**——Memory Layer 的短期记忆存储,与宿主会话无对应关系 | auto | confirmed |
| 三查命令(消歧) | review vs analyze vs checklist | 三个质量检查命令各司其职:**/speckit.review**=单 feature 的 SDD 过程质量事后评审(改进报告);**/speckit.analyze**=实现前 requirements/plan/tasks 跨工件一致性漂移分析(严格只读);**/speckit.checklist**=为当前 feature 生成领域需求质量检查单(如 security 域)。review 全局 vs feedback 条目 scope:local 的区分不变 | auto | confirmed |
| 三捕获机制(消歧) | TODO block vs parked idea vs feedback entry | 三种"记下以后处理"的机制:**SPECKIT TODO block**=嵌在文件里、面向执行的行动项(/speckit.todo 收集);**Parked Idea**=.specify/memory/todo/ 里的自由想法(捕获非承诺,成熟后再晋升);**Feedback Entry**=wrap-up 时 agent 自评的单元级优化点(经 Feedback Probe,面向改进)。层级:idea(想法)<TODO(行动)<feedback(改进反思) | auto | confirmed |
| Feature ↔ Requirement 编号空间 | feature id vs requirement key | **Feature registry ID**(features/0NN.md,如 028)与 **requirement key**(specs/NNN-slug/,如 041-refactor-feedback-probe)是两套独立编号空间,永不互相覆写(引擎 --feature-id 与 --feature 分离);一个 Feature 可被多个 requirement 递进实现(如 028 ← 027 与 041) | auto | confirmed |
| specify-cli | specify-cli, 分发名, wheel | Spec Kit 的**分发包名**(PyPI/wheel 名,入口命令 `specify`);与项目名 spec-kit(仓库)与运行时目录 .specify/(工作区)三名一体、各指一层:仓库开发→打包为 specify-cli→init 装出 .specify/ | auto | confirmed |
| .specify 工作区 | .specify/, workspace, 项目运行时 | specify init 在客户项目内装出的框架运行时目录(instructions.md/memory/skills/agents/scripts/templates);本仓的 .specify/ 同时是自用运行时(dogfooding 三副本第二副本);对其直接修改=客户侧问题修复 | auto | confirmed |
| Focus Target(默认聚焦引用) | 默认聚焦, focus_target, default focus, 默认 Target | team.md frontmatter 可选字段 focus_target:该团队默认聚焦的 Goal Target(局部形 T-<nnn>);是 run 级 --target 的预填——未显式指定时 run 解析到它,显式 --target 可覆盖;不改 Goal–Team 绑定、不构成写域声明;与台账逐条字段 target_ref 消歧(需求 042) | auto | proposed |
| Decomposition Proposal(分解提议集) | 分解提议, 目标分解提议, decomposition proposal set | goal→Target 分解的成组提议:N 条成果形候选语句 + 各自理由,一次性呈现、一次合并确认;team 侧只提议(propose→ratify),落盘逐条经 /speckit.goal targets --add;goal 已有 open Target 时以既有集合为复用基线(需求 042) | auto | proposed |
| 框架资料卫生 (Framework Material Hygiene) | sanitize, 资料卫生, hygiene, 框架清理 | 对**框架自有资料**(memory 层 parked/draft/索引、specs、镜像目录、兼容符号链接、docs 树)的系统性治理:过期残留/冗余检测 + 正确性检查(死引用/索引一致/链接/镜像漂移)+ 确认后清理;治理对象不含用户代码/脚本/测试;由 /speckit.sanitize 承载(需求 045) | auto | proposed |
| 站点记忆 (Site Memory) | site memory, 站点记忆目录, 网页记忆机制 | browser-utils 的按站点持久化层:以 domain(host:port) 为 key 在技能 site/ 目录下建目录,内含站点状态机文件、探索期操作记录、请求级步骤集与验证证据;三个 Tier 可读写的结构化、agent 中立格式(需求 046) | auto | proposed |
| 站点状态机 (Site State Machine) | 站点状态, 探索期, 优化期, 验证期, sealed, site state | browser-utils 站点记忆的四态生命周期:exploration(探索期)→optimization(优化期)→validation(验证期)→sealed(固化);验证失败或 sealed 执行失败回退 optimization;状态变更由确定性程序依证据判定,任一状态都完整完成用户任务(需求 046) | auto | proposed |
| 请求级方向 (Request-Level Direction) | 请求级自动化, 底层请求调用, 泛型调用 | 浏览器脚本自动化两方向之一:在页面上下文中直接发起底层网络请求(如 fetch),自动继承会话;相对物为页面级方向(模拟真实用户 DOM 操作);对已有请求级步骤集的站点优先使用(需求 046) | auto | proposed |
| 请求级步骤集 (Request Recipe) | 请求配方, 固化流程, 请求步骤集 | 优化期从探索期记录蒸馏出的有序请求步骤列表:每步含方法/URL/参数模板/动态字段解析方式/预期响应特征;无法请求化的步骤显式标注保留为页面级,形成混合形态(需求 046) | auto | proposed |
| Feedback Introspection (反馈自省) | introspection, 自省, 自省流程 | 在客户项目内对已积累 feedback 条目做场景化深加工的按需流程:回到真实场景核验事实→同根因条目聚类为问题→产出自省报告(问题五要素:陈述/根因/证据锚点/分流决定/优化方案)→分流本地下沉(Loop B)或随包上行(Loop A),上行包由裸事实富化为事实+证据+根因+方案;介于 record(事实捕获)与 package/consume(传输对账)之间(需求 047) | auto | proposed |
| 自省报告 (Introspection Report) | introspection report, 自省报告文件 | Feedback Introspection 的持久产物:`.specify/memory/feedback/introspection/<report-id>.md`,frontmatter(id/created/status/scope_filter/scope_entries/supersedes/confirmed_at)+ Findings/Excluded 正文;生命周期 draft→confirmed→superseded,终态保留;必须落子目录隔离 reindex 根部 glob(需求 047) | auto | proposed |
| 调谐 (Reconcile) | 调协, reconcile 模式, reconcile | 期望态 vs 当前态的差异收敛语义(R0–R6 调谐环、容忍带、只归档不删除、单引擎坍缩);真源 shared/patterns/reconcile-pattern.md;与 Reconcile Engine(引擎实例)是模式/实例关系;语音/转写输入的「调协」按变体校正到此规范词(需求 048 注册) | auto | proposed |
| 目标结构声明 (Target Structure Declaration) | target structure declaration, 文档目标结构 | docs 域的项目专属文档结构持久化契约:引用 create-docs 静态基线 + 仅声明项目扩展(不复制基线事实);生命周期设计→确认→实质性修订;是 /speckit.docs 每次调协的期望态锚点(需求 048);与 Goal Target(目标切片)无关 | auto | proposed |
| 调协动作 (Reconcile Action) | reconcile action, 动作分解 | /speckit.docs 一次运行中从现状-目标差异分解出的最小执行单元:类型(结构/内容/用户委托)× 目标对象 × owning 技能(create-docs/improve-docs)× 确认层级;聚合为干跑计划,执行后进入审计日志与残差报告(需求 048) | auto | proposed |
| 受管块 (Managed Block) | managed block, 托管块, 标记块 | 成对 HTML 注释界定的机器维护区约定:写入时**只替换标记之间的内容**,标记本身与块外内容字节保持(块外为人工可加注区);标记残缺时视为不可用并请求人工处置,不静默重写。既有实例 `<!-- GIT_WORKFLOW_START/END -->`(.specify/git-workflow.md),需求 048 新增 `<!-- DOCS_TARGET_STRUCTURE_START/END -->`(目标结构声明) | auto | proposed |
| 分发批次 (Dispatch Batch) | dispatch batch, 分发批 | /speckit.docs 一次运行中按 owning 技能聚合的调协动作集合;承载「分发前告知计划动作数」与「可中止点」两项语义;内容批次逐文档顺序分发、不设上限、禁止隐式截断,中止后已完成项保留、未开始项转 pending(需求 048) | auto | proposed |
| Derivation | derive, 推导档案, derivation archive | 以**重放权威源的推理方法**(而非摘录其结论)得出架构的项目级产物:对象是一个主题(topic),由 Source → Reasoning Move → Derivation Step → Architecture Element 四类记录构成,落盘 `.specify/derive/<topic-slug>/derive.md`;与按特性收集结论的 /speckit.research 分属方法层与结论层;真源 shared/definitions/derivation-definitions.md | auto | confirmed |
| Reasoning Move | 思维算子, reasoning operator, move, 算子 | 从来源**论证方式**(不是其主张)中抽取的可复用推理形状:`inference_form` 带命名槽位故可跨领域套用,另附它防住的失败模式、适用条件与过度使用护栏、展示该论证方式的来源锚点;身份 M-<nnn> 项目级单调发放,累积于 `.specify/derive/moves.md`(引擎 moves-add 独写);真源 shared/definitions/derivation-definitions.md | auto | confirmed |
| Provenance Grade | 溯源等级, source grade, 来源等级 | 经线上核实的来源的**权威性分级**(取值集与各级能否为推导步骤供前提、抑或只能作 leads 线索,归真源 §Provenance Grades):等级由内容判定、不因被存档救回而升级,证据由引擎供给、判定归 agent;真源 shared/definitions/derivation-definitions.md | auto | confirmed |
| Derivation Chain | 推导链, 思维链路, reasoning chain | 推理方法被实际重放之处:每个 Derivation Step(D-<k>)把一个 Reasoning Move 套用到显式前提(已核实来源 + **更早**的步骤)上,得出一句可证伪结论供后续步骤消费,步骤序上构成有向无环图;完整性规则 C1–C7 归真源 §Chain Integrity Rules;真源 shared/definitions/derivation-definitions.md | auto | confirmed |
| 主动触发点 (Proactive Trigger Point) | 触发点, proactive trigger point, trigger point | agent 必经指令路径上的常驻行为契约落点(init / /speckit.instructions 写入 .specify/instructions.md,经既有 symlink 模型抵达各 agent);在运行**之前**提议该运行什么,与 Feedback Probe(wrap-up 事实捕获点,记录**已发生**运行的自评)分属不同概念;用户口语的「埋点」在本语境指此,不与 Feedback Probe 混用(需求 050) | auto | proposed |
| 情境评估 (Situational Assessment) | situational assessment, 状态评估 | 在主动触发点对当前项目状态做的低成本判断(制品生命周期阶段 / 待处理 feedback / 指令时效),产出「现在可执行哪个流程」+ 确切可复制调用形式;消费摘要式证据、不注入制品原文(token 效率);与 Feedback Introspection(对已积累 feedback 条目的场景化深加工)对象不同,用户口语的「自省」在本语境指此(需求 050) | auto | proposed |
| 建议规则 (Suggestion Rule) | suggestion rule, 触发规则 | 一条(情境条件 → 目标流程)映射,触发逻辑的最小可优化单元:标识 / 情境条件信号 / 目标流程(命令或技能)/ 确切调用形式 / 确认类别(可逆·破坏性)/ 状态(active·suppressed·promoted)/ 连续采纳计数 / 命中与拒绝统计;规则集为可修订数据面,非硬编码散文(需求 050) | auto | proposed |
| 阈值晋升 (Threshold Promotion) | threshold promotion, 免确认晋升, auto-execution promotion | 同一建议规则被**连续采纳**达阈值(默认 3,可配置;一次拒绝即重置计数)后转为免确认自动执行;硬边界——破坏性/不可逆流程永不晋升(判据归 confirmation-gates.md,存疑从严默认破坏性),自动执行仍须出三段式执行报告(需求 050) | auto | proposed |
| 触发学习状态 (Trigger Learning State) | trigger learning state, 学习状态 | 承载建议规则集、晋升态与建议事件的项目本地机器维护状态;与指令文件分离(再生不吞状态),跨会话持久、可复位、可全局关闭;缺失/损坏/版本不兼容时降级为「只建议」而非中断会话;不跨项目共享、不自动外传(需求 050) | auto | proposed |
| 情境身份 (Situation Identity) | situation identity, 情境标识 | 主动触发机制中「同一情境」的判定单位:取自小型受控词表的粗粒度二元组(特性生命周期阶段 × 待处理信号集),跨会话可稳定复现,因而使阈值晋升的连续计数良定义;词表只能经用户确认通道扩展,禁止 agent 临场造词。**不取完整制品状态指纹**——指纹近乎每次唯一会使计数永不到阈值、晋升机制整体失效。与「情境快照」不同:快照是某次评估的摘要级证据留痕,身份是可复现的标签(需求 050) | auto | proposed |
| 回合遥测 (Turn Telemetry) | turn telemetry, 每回合遥测 | 主动触发机制在**每个用户回合**落一行最小遥测(无论该回合是否产出建议):回合标识 / 是否升级探测 / 是否产出建议 / constitution 合规分析是否已完成。是探测升级率与顺序契约两条度量的**唯一分母来源**——静默回合若不落痕,这两条护栏即不可测;有显式保留窗口、可轮转,轮转不影响晋升计数(计数是规则上的聚合态,不由原始行重算)(需求 050) | auto | proposed |
| 种子规则 (Seed Rule) | seed rule, 出厂规则, 派生规则 | 随 templates/ 分发的出厂建议规则,使新项目第一天即产出建议(无冷启动);**从 25 个命令模板既有 `## Handoffs` 条件式派生而非另行撰写**——Handoffs 已是 situation→flow 知识的既有真源,另撰一份即造出第二真源。与学习所得规则同构(同字段、同受破坏性豁免约束),只在来源与可覆盖性上有别;**用户已确认的调优不得被后续种子更新覆盖回退**(需求 050) | auto | proposed |
| 名字级基线 (Name-Level Baseline) | name-level baseline, 名字级回归, 节点级基线 | 回归比对的房式判据:比较**排序后的 FAILED pytest nodeid 列表**(由 `scripts/bash/run-tests.sh --names-out <file>` 产出,再以 `comm -13 baseline current` 断言输出为空),而**不是比较失败条数**——条数相等时失败集合仍可能已换手(旧失败被修好、新失败被引入,计数不变而实际回归)。开工前冻结 `baseline-failed.txt` 于特性目录,收尾时逐名比对;需求 044/047/048/049 的验收均用此判据 | auto | proposed |
| Ask, Record, Repeat | 问一次记下来说三遍, 问好过于猜, 好记性不如烂笔头, 重要的事情说三遍, 举一反三, 触类旁通, ask don't guess, 知识生命周期 | 知识生命周期理念(非宪法原则):获取(吃重事实未知或有歧义时提问而非猜测,但先自查、成组问、带推荐)→保留(从用户处得到的答案 MUST 落在下一回合会读到的地方,记规则不记实例并举一反三)→保活(只在一处出现过的规矩等于不存在,归属正确≠可达);三者都安静失效;真源 shared/guidelines/ask-record-repeat.md | user | confirmed |
| 指针形态重复 (Pointer-shaped Repetition) | pointer-shaped repetition, 说三遍的合规形态, 路标式重复 | 同一规矩在多个表面出现但每处只放短规范提醒+指向 owner 的路径,细节不搬;与 Principle XIV 相容的重复形态,房式三层表面(真源文档→常驻章节→契约测试)即此;判别法=改该事实只需编辑 owner 一个文件;真源 shared/guidelines/ask-record-repeat.md §3 | user | confirmed |
| 内容形态重复 (Content-shaped Duplication) | content-shaped duplication, 抄本式重复, 漂移副本 | 复述 owner 的表格/阈值字面量/枚举清单/判据正文,使读者无需打开 owner 即可行动;Principle XIV 禁止的重复形态,「说三遍」不构成其许可;判别法=改该事实需编辑多个文件即已违约,修复方向是改回引用而非把措辞改到一致 | user | confirmed |
