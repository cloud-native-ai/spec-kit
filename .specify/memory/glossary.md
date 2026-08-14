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
| Constitution | - | Project governance principles at .specify/memory/constitution.md | auto | proposed |
| Feature Index | - | Single source of truth for project capabilities at .specify/memory/features.md | auto | proposed |
| Reconcile Engine | - | Diff-and-converge engine used by Spec Kit commands to align artifacts with desired state | auto | proposed |
| Task Complexity Rubric | - | Tiered effort-calibration framework embedded in .specify/instructions.md | auto | proposed |
| 程序优先 (Program-First) | program first, 程序优先原则 | Token 效率纪律之一:可用固定规则表达的文本/数据判断交由确定性程序执行,不送入大模型 | auto | proposed |
| 摘要优先 (Summary-First) | summary first, 摘要化访问 | Token 效率纪律之一:机器管理数据文件原文不整体注入大模型上下文,例行消费摘要/投影/节选 | auto | proposed |
| 升级阶梯 (Escalation Ladder) | escalation ladder, 访问升级阶梯 | 数据访问逐级放宽路径:摘要 → 定向节选 → 有界整读(整读须满足例外情形或记录理由) | auto | proposed |
| Static Structure | 静态结构 | 团队的 Role × Stage × Type 成员名册 | auto | proposed |
| Dynamic Structure | 动态结构, 拓扑结构, topology | 团队的协作模式(parallel/serial/iteration/continuous),即成员间的运行时协作关系 | auto | proposed |
| Goal | 项目级目标, 目标定义, project goal | 项目级一等概念:归档于 .specify/goal/<goal-slug>/ 的目标定义(目标叙述 + 可验证成功判据 + 生命周期状态),作用对象不限于本项目代码(可指向框架自身/代码规范收敛/能力运行结果等任意维度);与 Requirement(只描述本项目源码/配置要实现的 feature)分属不同层面、无必然上下层关系;真源 shared/definitions/goal-definitions.md | user | confirmed |
| Goal Archive | 目标归档, goal 归档 | .specify/goal/ 下全部 goal 定义的集合,即「项目当前与历史目标清单」的物化形态;终态 goal 保留不删 | user | confirmed |
| Goal–Team Binding | 目标—团队绑定, goal 引用 | 团队到 goal 的单向引用(N 团队 : 1 goal),以 goal_slug 声明;团队侧只存身份不存目标副本;一个团队同时只绑一个 goal | user | confirmed |
| Team Goal | 团队目标, team 目标 | 团队服务于哪个项目级 Goal 的**引用**(经 goal_slug);未迁移团队可退化为内联副本,定义存在时以 Goal 定义为权威 | user | confirmed |
| Goal Target | 目标切片, target 切片, 切片 | Goal 之下的 run 级可指派范围切片:身份 T-&lt;nnn&gt;、三态(open/done/dropped)、引擎渲染于 goal.md 的 ## Targets 节;授权只经 /speckit.goal targets,run 经 --target 消费;台账经可选 target_ref 归属;概念真源 shared/definitions/goal-definitions.md → Target Decomposition([[STR-004]]) | auto | proposed |
| target(消歧) | - | 以下既有 "target" 用法与 Goal Target **无关**,均不改名:团队 territory 的 optimization_target/co_targets(优化对象)、evidence-utils / interview-utils 的 --target 参数(取证/访谈对象) | auto | proposed |
| Team Summary | 团队总结 | 把团队自身视作项目而产出的累积式状态总结(**派生物**);按 goal 索引落在 .specify/goal/&lt;goal-slug&gt;/summary/ 子树内,与同目录下被撰写的 goal.md 定义结构分离——刷新只写 summary/,不写定义 | auto | proposed |
| Team Territory | 团队级范围, 团队 territory, team territory | 团队在 team.md 声明的覆盖范围(write/read/forbidden 路径 + 类型化 non_path 条目);把成员级 Territory Division 抬到团队级,四种协作模式通用;缺省该键即「未声明」,不等于空 | auto | proposed |
| Team Roster | 参与团队名册, goal 名册, roster | 同一 goal 下全部引用团队的**派生**清单(team slug + 声明范围 + 身份类型 + 是否推进),落在 summary/roster.md;每次刷新整体重算,不改 goal 定义 | auto | proposed |
| Overlap Finding | 重叠发现, 范围重叠, overlap | 同一 goal 下两团队范围的比对结论:overlap(写-写相交,指名路径)/ no-overlap(双方均声明且不相交)/ undecidable(有一方未声明或仅非路径声明) | auto | proposed |
| Contested Area | 争用区, 写重叠区, contested area | 被两个及以上团队写入的重叠区(write-write finding);MUST 归给唯一团队或转为该 goal 的禁写区,不得停留在双方都可写 | auto | proposed |
| Coordination Round | 协调轮, 协调机制, coordination round | 针对已检出重叠的一次重划:机制**只检测并提议**(附依据),人裁定后把划分写回各 team.md;机制自身无改写权,提议阶段对 team.md 零写入 | auto | proposed |
| 工作项四态色板 | 四态色板, work item four-state palette | 已完成/进行中/延期/未开始 四态的统一颜色与冗余符号编码,颜色之外必配符号 | auto | proposed |
| Agent Template | agent模板, 能力模板, 抽象agent类, capacity template | Agent 三层分类法第一层:能力与行为框架描述,源码 agents/ 角色集由 specify init 安装到 .specify/agents/templates/;真源 shared/definitions/agent-definitions.md | user | confirmed |
| Agent Instance | agent实例, 落地定义, agent definition | Agent 三层分类法第二层:职责描述定义(.specify/agents/instances/*.agent.md、team 名册席位),引用 Agent Template 并绑定具体职责,由命令/技能实例化产生 | user | confirmed |
| Qwen Code CLI | qwen, qwen-code, qwen cli, QWEN.md, .qwen/ | **Agent CLI 工具名**(非模型):曾为 Tier 2 支持的编码 agent,已随 0c300bc8 下线;当前 AGENT_CONFIG 只含 claude/codex/copilot/hermes/opencode/qoder 六工具。与 qwen3 系列模型 ID 是两个不同概念,勿混淆 | user | confirmed |
| qwen3 系列模型 ID | qwen3.7-max, qwen3.7-plus, qwen3-coder-plus, qwen3-rerank | **百炼大模型 ID**(非工具名):cli-setup 的模型四元组仍在使用,状态为活跃。与已下线的 Qwen Code CLI 仅名称形近、语义无关;清理 qwen 工具时 MUST NOT 按 `grep -i qwen` 整体删除,否则会误删 supported-tuples.md / config-agent.sh 中生效的模型配置 | user | confirmed |
| iFlow CLI | iflow, iflow-cli, .iflow/ | **Agent CLI 工具名**:曾为 Tier 2 支持,已随 0c300bc8 下线;不存在与之对应的同名模型 ID | user | confirmed |
| Agent Execution | agent执行, 运行实例, subagent, 子代理 | Agent 三层分类法第三层:定义真正执行时的运行形态,持久产物在 .specify/agents/execution/(configs/scripts 归档,logs 不入库);三种模式(native/virtual/external)见 shared/definitions/subagent-definitions.md | user | confirmed |
| Feedback Probe | 反馈插点, feedback probe, 插点 | 两层建模的显式反馈插点:Probe Class 定义一类插点的特征(收集内容/目标系统切片/收集后处理流程/适用插入位置类型),Probe Object 为其在当前系统中的实例化(绑定具体流程单元×生命周期点);既有 49 个 wrap-up 埋点重构为 Object 并归类到 Class(需求 041) | auto | proposed |
| System Slice | 系统切片, feedback slice | 反馈针对的框架部位,沿框架既有组成维度(命令/技能/脚本/模板/文档)取值;由 Probe Class 声明为目标、条目经 Object→Class 继承,作为反馈过滤与统计维度;与 Goal Target 的「目标切片」无关 | auto | proposed |
