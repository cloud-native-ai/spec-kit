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
