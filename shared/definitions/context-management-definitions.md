# Context Management(上下文管理)

owns: umbrella-term, categories, layers, forms, landing-contract, layout-table, composition-protocol, trigger-set, composer-roles, concept-pointer-slot, presence-vocabulary, red-lines

本文档是**上下文的声明、组合与只读审计**的唯一含义 owner：术语、两类（category）、三层（layer）、五种物化形态（form）、层级落点（landing contract）、布局表（layout table）、组合协议（composition protocol）、触发集（trigger set）、组合者角色（composer roles）、概念指针槽位（concept pointer slot）、在场词表（presence vocabulary）与红线（red lines）都在这里定义一次；其他表面（四个声明事实、审计引擎、守卫、ambient 指令段、framework map）只按指针抵达，不复制本文件的规则。机器值域（封闭成员与花名册）由 `shared/declarations/facts/context-*.yaml` 拥有，本文件的布局表只拥有逐行数据（source / form / owner / cap reference）。

## Terms

**Context Management(上下文管理)** 是「一会话/一任务实际把哪些事实带进上下文、以何种形态物化、由谁在何时组合、以及如何只读审计其声明质量」的机制名。它不新造事实，只声明既有来源的层、形态、指针与在场读数。

六个定义点在首次出现处一次定义：

- **Invariant(不变)**：任务变化而环境与项目不变时保持不变的事实类别。
- **Variable(可变)**：随当前工作项变化的事实类别。
- **System(系统级)**：owner 在执行环境（运行时、可用命令、权限、现实约束）的层。
- **Project(项目级)**：owner 在项目 `.specify/` 工作区（治理、词汇、概念定义、能力清单、状态锚点、工作区地图）的层。
- **Task(任务级)**：owner 在当前工作项（制品、能力、共享文档、docs、记忆、陈述、增量）的层。

**成员判据（只陈述一次）**：若任务改变而环境与项目不变，该事实是否会变？会变 → variable；不变 → invariant。判据只决定类别，不授权任何内容复制。

## Categories

类别是**从层推导**的两个封闭值：`invariant`（system 与 project 层）与 `variable`（task 层）。类别**绝不是布局表的一列**：布局表只记录 class id / layer / form / source / owner / cap reference，任何 `category` 列都是审计的 `category-column` finding。推导规则与落点见 § Landing Contract。

## Layers

三层按**owner 所在位置**判定，并按组合顺序声明为 `system` → `project` → `task`：

- `system`：执行环境的事实——运行时身份、可用命令、操作权限、现实约束；使用期发现或指向既有 owner，永不书写、永不持久化。
- `project`：项目 `.specify/` 工作区内书写或生成的事实，在任务周期内不变；治理基线、词汇、概念定义与解释、能力清单、状态锚点、工作区地图。
- `task`：当前工作项的事实，逐任务选择并在任务结束时丢弃。

三层的成员与顺序由 `shared/declarations/facts/context-layers.yaml` 机器拥有；本节只声明判据与含义。

## Forms

五种物化形态构成封闭集，按层合法性由下表钉死（矩阵的成员由 `shared/declarations/facts/context-forms.yaml` 与 `context-layers.yaml` 机器拥有）：

| form | legal layers |
|------|--------------|
| `pointer` | system, project, task |
| `read-in-full` | project |
| `bounded-index` | project, task |
| `runtime-discovery` | system |
| `inline-digest` | task |

- `pointer`：只携带路径引用，按需打开；不携带内容。
- `read-in-full`：canonical 指针，消费者完整加载文档；**零复制字节**；仅限 project 层。
- `bounded-index`：逐条路径加一行相关性，保持在 owner 声明的 cap 之内；cap 以 `<path> § <section>` 引用，绝不写数值。
- `runtime-discovery`：使用期只读观测，永不存储；仅限 system 层，探针 id 属引擎 schema。
- `inline-digest`：指针形态不可达时可携带的有界摘要；仅限 task 层。两条常驻 `inline-digest` 行（`task-statement`、`task-delta`）以常驻 owner 路径为在场见证，其摘要针对瞬态输入，绝不转述不变来源。

## Landing Contract

三个合法（category, layer）落点与三条被点名禁止的组合。允许形态一律按 § Forms（C-005）引用，本表不复述形态值表：

| cell | definition | carriers | allowed forms | content vs pointer |
|------|------------|----------|---------------|--------------------|
| invariant × system | 环境与现实事实：使用期发现，或指向其约束 owner；永不书写、永不持久化 | 根会话的基线行；执行代理的使用期观测 | § Forms (C-005) | 只观测或引用，零内容复制 |
| invariant × project | 项目 `.specify/` 内书写或生成、任务周期内不变的事实 | 基线行；派发时经既有载荷的 `authority_ref` 字段与子代理 ambient 的 Documentation Map 承载 | § Forms (C-005) | 治理基线是 canonical 指针、零复制字节；其余只引用或有界索引 |
| variable × task | 当前工作项的事实：逐任务选择，任务结束丢弃 | 任务层行；派发时为派发简报，阶段边界刷新 `task-delta` | § Forms (C-005) | 按任务范围与关键词选择；不变来源只以指针引用 |

禁止组合（在任何布局行之外点名，永不作为合法行出现）：`invariant × task`、`variable × system`、`variable × project`。

## Presence Vocabulary

在场词表在本节定义一次：五个 token 与含义，其余表面只引用。语义按来源实际类型判定（普通文件看大小、目录看条目数；类型判定只消费元数据，绝不打开被审计来源的内容）：

| token | meaning |
|-------|---------|
| `present` | 该行的每个常驻来源都可解析、可读且非空；`runtime-discovery` 行在其声明的探针成功时读此词 |
| `absent` | 常驻来源路径不存在 |
| `unreachable` | 目录项存在但目标不可读——含悬空符号链接（链接存在、目标不解析），或实际类型既非普通文件也非目录 |
| `empty` | 可解析但存储为空——0 字节文件、空目录，或只含 0 字节文件的目录存储 |
| `not-evaluated` | 没有可读的常驻来源：该行只有瞬态/使用期来源，或花名册类没有布局行（原因点名缺失的布局行）；运行期探针失败也读此词并带原因 |

多来源行按声明来源次序报告**第一个失败来源**；每次缺席都带点名来源（或缺失布局行）的原因——静默省略与编造默认都是缺陷。

**一致性读数**：由某受治理结构导出的**一致性声称**在其承载行并非全部 `present` 时读 `Unobserved`（证据态 owner 按指针抵达 `shared/declarations/facts/evidence-seven-states.yaml#/statement`）；永不一致，永不读作 `present`。该读数的承载是守卫与证据记录（AN-05 裁定：manifest 面不新增派生字段，行集与在场 token 是唯一观测面）。

## Terminology Boundary

本机制与四个邻接概念的边界；每个邻接以指针抵达其 owner，本文件不复述对方规则：

| neighbour | owner pointer | distinction |
|-----------|---------------|-------------|
| Project Context | `src/specify_cli/__init__.py` 的 `render_agents_for_tool`：agent 文件 `## Project Context` 渲染路径 | 那是**渲染进 agent 文件的静态项目上下文块**；本机制是运行期的上下文声明与组合协议，不扩展也不改写该渲染 |
| super↔sub dispatch payload | `shared/definitions/superagent-definitions.md` § The super↔sub Protocol | 派发载荷的七角色字段与四项注入由该 owner 拥有；本机制只把概念指针槽位映射到既有通道，载荷字段集不变 |
| ambient instructions | `templates/instructions-template.md` 经 `scripts/bash/generate-instructions.sh` 生成 live 指令 | 那是**每个会话都加载的摘要加指针段**；本文件是其详细 owner，ambient 段只携带三条规则摘要 |
| model context window | not a framework artifact——模型自身的上下文窗口不是框架工件 | 窗口大小与裁剪由宿主模型决定；本机制只声明“组合什么、以何种形态、何时刷新”，不承诺容量 |

## Red Lines

red_lines: no-persistence, no-owner-replacement, no-new-command, no-new-gate, no-watcher

- **No persistence**：组合是瞬态的，随工作项消亡；不创建 store、缓存、索引、渲染产物或数据库，也不改变既有存储 schema。
- **No owner replacement**：本机制只引用既有 owner（治理文档、声明层、协议、渲染路径、记忆召回、token 经济、确认门、重锚定）；不复制其规则文本，不重定义其值域。
- **No new command / gate / watcher**：不新增 `/speckit.*` 命令、技能包装、门或红线；`source-drift` 是已记录的记录变更，绝无 watcher、daemon 或轮询。
## Layout

本表是逐行数据（source / form / owner / cap reference）的唯一书写处；class id 列是 `shared/declarations/facts/context-classes.yaml` 花名册的投影，两层逐层逐行核对，不匹配即审计 finding。`source` 单元格是逗号分隔的 workspace 相对路径列表，或 `runtime-discovery:<probe-id>` 形态；`cap reference` 单元格取 `<path> § <section>` 形态——`bounded-index` 行引用其 cap owner，`read-in-full` 与 `inline-digest` 行引用同一内容承载例外 owner，其余行为 `—`；任何数值 cap 都不出现在本表。安装形态（`.specify/…`）在框架源树与客户项目树上同样解析。

| class id | layer | form | source | owner | cap reference |
|----------|-------|------|--------|-------|---------------|
| `runtime-environment` | system | `runtime-discovery` | runtime-discovery:platform | 引擎探针（`context-audit.py`） | — |
| `available-commands` | system | `runtime-discovery` | runtime-discovery:path-tools | 引擎探针；有 Tool 记录时优先 `.specify/tools/` | — |
| `operation-permissions` | system | `runtime-discovery` | runtime-discovery:fs-access | 引擎探针 | — |
| `reality-constraints` | system | `pointer` | .specify/shared/guidelines/confirmation-gates.md, .specify/shared/guidelines/fast-fail.md, .specify/shared/guidelines/temp-directory-discipline.md, .specify/workflow/git.md | 各 owner 文档 | — |
| `governance-baseline` | project | `read-in-full` | .specify/constitution.md, .specify/instructions.md | 治理文档生成器 | .specify/shared/guidelines/token-efficiency.md § 摘要优先(Summary-First) |
| `project-vocabulary` | project | `pointer` | .specify/glossary.md | `shared/workflow/glossary.md`（glossary 协议） | — |
| `concept-definitions` | project | `bounded-index` | .specify/shared/definitions/ | 各定义 owner | .specify/shared/guidelines/token-efficiency.md § 摘要优先(Summary-First) |
| `concept-explanations` | project | `pointer` | .specify/skills.md, .specify/tools.md | 各 guide；`docs/concepts/documentation-model.md` 声明解释型文档 | — |
| `capability-inventories` | project | `bounded-index` | .specify/skills/, .specify/agents/templates/, .specify/agents/instances/, .specify/tools/, .specify/skills.md, .specify/tools.md | 各 owner | .specify/shared/guidelines/token-efficiency.md § 摘要优先(Summary-First) |
| `project-state-anchors` | project | `pointer` | .specify/features.md, .specify/features/, .specify/register.md, .specify/workflow/git.md, .specify/shared/declarations/facts/runtime-store-layout.yaml | 各 owner | — |
| `workspace-map` | project | `pointer` | .specify/shared/definitions/framework-map.md, .specify/shared/guidelines/directory-governance.md | 各 owner | — |
| `task-artifacts` | task | `bounded-index` | .specify/specs/, .specify/features/ | 规格制品 | .specify/shared/guidelines/token-efficiency.md § 摘要优先(Summary-First) |
| `task-capabilities` | task | `bounded-index` | .specify/skills/, .specify/agents/templates/ | 各 owner | .specify/shared/guidelines/token-efficiency.md § 摘要优先(Summary-First) |
| `task-shared-docs` | task | `bounded-index` | .specify/shared/ | 共享 owner | .specify/shared/guidelines/token-efficiency.md § 摘要优先(Summary-First) |
| `task-docs` | task | `bounded-index` | docs/ | 文档空间 | .specify/shared/guidelines/token-efficiency.md § 摘要优先(Summary-First) |
| `task-memory` | task | `bounded-index` | .specify/session/, .specify/knowledge/ | `scripts/python/memory-utils.py` | .specify/shared/guidelines/token-efficiency.md § 摘要优先(Summary-First) |
| `task-statement` | task | `inline-digest` | .specify/shared/workflow/user-input-protocol.md | .specify/shared/workflow/user-input-protocol.md | .specify/shared/guidelines/token-efficiency.md § 摘要优先(Summary-First) |
| `task-delta` | task | `inline-digest` | .specify/register.md, .specify/state/ | 各 owner | .specify/shared/guidelines/token-efficiency.md § 摘要优先(Summary-First) |

## Composition Protocol

baseline_composition: 基线在每个会话或线的入口组合一次（once），由根会话在 session-entry 组合；任务变化绝不触发基线重组。
baseline_refresh_triggers: session-entry, source-drift
task_composition_triggers: task-entry, task-switch, stage-boundary
baseline_scope: session, line

- **Session（会话）**：一次 agent 会话的上下文窗口生命周期。压缩（compaction）或重入不产生新会话——它走 `reentry`（§ Triggers）。**Line（线）**：同一 state spine 下的连续阶段系列；跨阶段提交仍是同一线。
- **线入口的基线**：一条线在已组合的会话内启动时，线入口复用该会话基线，不重组；作为独立运行入口且无既有会话基线时，按 `session-entry` 组合一次（AN-02 裁定：线入口不新增第八个触发）。
- **系统层**：使用期发现加约束 owner 指针；**项目层**：治理基线以 `read-in-full` canonical 指针完整加载、零复制字节，其余行只以 pointer 或有界索引携带。
- **任务层**：在声明的三个任务组合触发点按任务范围与关键词选择；不变来源只以 pointer 引用；组合保持在 owner 声明的 cap 之内，绝不加宽形态；任务结束时 discard 任务内容，任务内容绝不保留到下一任务。
- **确定性**：行按花名册顺序打印与组合；审计读数不含时间戳与宿主值。
