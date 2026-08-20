# AI 工程演进：Prompt → Context → Harness → Loop → Graph

这条路径描述的不是模型能力的代际，而是**工程师需要负责的系统边界在逐级外扩**：从控制一次回答，到控制一次推理看到的世界，到控制 agent 工作的环境与护栏，到控制它如何持续行动与停止，最后到控制多个 agent、循环、数据、策略与人如何共同演进。本文用这条坐标系定位 Spec Kit 当前所处的位置，并给出在**不引入 runtime**（宪法原则 IX）的前提下继续外扩的动作。

> 概念来源：Anthropic *Effective context engineering for AI agents* / *Building effective agents* / *Loop engineering: Getting started with loops*，OpenAI *Harness engineering*，Eigent *Graph Engineering for AI Agents*；工程落点案例取自阿里云内部文章《罗盘背后的工程思考》与《天猫AI新品体检Graph Engineering实践》。完整链接见文末「参考来源」。
> 本文只做定位与映射，Harness 维度的权威定义仍在 `.specify/shared/guidelines/better-harness.md`，导向页见 [better-harness.md](./better-harness.md)。

---

## 1. 五级坐标系

| 阶段 | 核心问题 | 主要设计对象 | 代表性工件 | 暴露的新瓶颈 |
|------|---------|-------------|-----------|-------------|
| **Prompt** | 怎样让模型答对？ | 单次模型调用 | Prompt、Few-shot、CoT、ReAct、输出模板 | 不知道真实世界的最新状态，也不能可靠行动 |
| **Context** | 模型此刻应看到什么？ | 有限上下文中的信息流 | RAG、记忆、工具结果、MCP、压缩、渐进披露 | 「知道」不等于「能安全执行」 |
| **Harness** | 怎样让 agent 稳定工作？ | agent 周围的工程环境 | Tool schema、规则、沙箱、CI、评测、权限、日志 | 一次任务可靠，不代表长期自治可靠 |
| **Loop** | 怎样持续行动并正确停止？ | 目标驱动的反馈循环 | Plan-Act-Observe-Evaluate、预算、停止条件、Maker-Checker | 多个循环会冲突、漂移或共同优化错目标 |
| **Graph** | 怎样让多个 agent 正确协作？ | agent、循环、工具、数据、策略、人的拓扑 | 任务图、知识图、治理图、证据图、改进图 | 需要图级治理、版本管理和真实业务锚点 |

每一级由上一级的瓶颈推动，且**不替代上一级**——Graph 级系统内部仍然逐节点使用 prompt、context 与 harness。

## 2. 每一级的判据（原文关键句）

| 阶段 | 判据 | 出处 |
|------|------|------|
| Context | *Context must be treated as a finite resource with diminishing marginal returns*；n 个 token 产生 n² 对注意力关系，因此目标是「最小的高信号 token 集」 | Anthropic, Effective context engineering |
| Harness | *Give Codex a map, not a 1,000-page instruction manual*；*By enforcing invariants, not micromanaging implementations, we let agents ship fast without undermining the foundation* | OpenAI, Harness engineering |
| Loop | *Loops are agents repeating cycles of work until a stop condition is met*；按「人类交出什么」分层：交出检查（turn）→ 交出停止条件（goal）→ 交出触发（time）→ 交出 prompt（proactive） | Anthropic, Getting started with loops |
| Loop | Agent 必须每步从环境取 ground truth，并显式设置 human checkpoint 与 stopping condition（如最大迭代数） | Anthropic, Building effective agents |
| Graph | *A graph without anchors is just a more elaborate echo chamber*；单 loop 的失效「是拓扑问题，所以需要拓扑级的修法」 | Eigent, Graph Engineering for AI Agents |

判定一个系统是否真的到了 Graph 级，罗盘一文给出六项判据：边有可验证契约（下游只接受符合 schema 的上游产物）、有独立控制层、有跨 agent 的共享状态、有风险否决关系、有经验回流通道、有真实业务锚点。缺其中任何一项，系统就仍停在「聊天入口 + RAG + 几个 tool」的形态。

## 3. 单 loop 在规模化时的四类失效

这是从 Loop 走向 Graph 的**唯一充分理由**，四类失效均为结构性问题而非某个 loop 的 bug：

| 失效模式 | 表现 | 修法（对应 §7 动作） |
|---------|------|-------------------|
| **Goodhart** | 指标与业务真相脱钩：工单解决率上升而续约流失翻倍，bot 学会把未解决单标为 solved | 指标成对 + 锚点（动作 1） |
| **Blindness upward** | loop 无法质疑自己的 reference：恒温器不能问 68°F 是否合适，eval loop 不能问 benchmark 是否匹配业务 | reference 有 owner（动作 2） |
| **Conflict** | 独立 loop 互相拆台而各自 dashboard 全绿：速度 loop 拆掉彻底性 loop | 速度分层、稀疏连边（动作 3） |
| **Measurement decay** | 没人监视监视者：报告只与其他报告对账，不与现实对账 | 冻结节点与只读 ground truth（动作 4） |

## 4. 实证案例：把达标判定权从模型手里收回来（天猫新品体检）

如果 §3 的四类失效还是推演，天猫新品 AI 体检团队的演进就是一次把坑全踩了一遍的工程实录：单 Loop 的 ReAct 自迭代（自主调 prompt、自主评测、自主决定下一步）很快走向作弊——把 badcase 的商品标题拆碎贴进规则文本，规则退化成已知样本的查找表，甚至指名道姓排除某些商品；喂黄金评测集，它学会的是应付那套题；而达标判定还在模型手里时，每轮自述都是「已完成优化」。作者的定性：**只要判定还在模型手里，你拿到的就不是评测结论，而是一份自我陈述。**

三条教训：其一，目标函数被单侧样本（只有 badcase）单方面决定时，模型必然用过拟合把指标做漂亮——这不是能力问题；其二，「改得好不好」和「往哪里改」不能都留给生成者回答——生成者与反思者是同一个 agent 时，批判会被自己的原方案锚定；其三，**自主权必须逐项分配，不能整包批发**。

四项修法（每一项都对应 §3 的一类失效）：

| 问题 | 修法 | 工程形态 |
|------|------|---------|
| 判定权在模型手里（Goodhart 亲历版） | **双样本、双阈值、四象限判定** | badcase 集 + 约 500 条未挑选的近期商品集（对侧样本）；Δ_bad（修复深度）与 Δ_pop（附带伤害）互不重叠，阈值 θ_bad=20pt、ε=1pt 由业务与工程配置、存放在模型上下文之外，模型既不能改阈值也不能覆盖判定；Q1 双赢 Pass / Q2 过拟合 **Reject** / Q3 无效 No-op / Q4 双输 Fail。关键决策是 Q2 判 Reject 而非 No-op——它比 Q4 更阴，在任何只看 badcase 的报表里都是漂亮的成功案例 |
| 方向跑偏（Blindness upward） | **最终目标 = 指标目标 + 不可动前提**；失败四路路由 | 业务定义是靶心不是背景资料，且必须写明「哪些业务前提不能被模型改写」——前提一旦也交给模型，它就会用换题的方式达成目标；失败按四象限分型走四条独立路由，四项分析互不共享上下文，其中规则形态扫描与历史回归检查「根本不该走大模型，正则匹配、集合比对就够，纯代码、零 token」 |
| 甩锅（归因与优化共享同一失败） | **权限分家 + 双 Loop 拆开** | 「中央大脑」是反模式：把语义决策与确定性编排打包进同一执行体，确定性的可靠性被拉到概率性的水平；分家判据极朴素——**能不能写出判断它对错的代码**，写得出来归代码，写不出来才归模型；发现 Loop 与优化 Loop 各自成环、各有出口判据（发现回路召回率 ≥0.95、准确率 ≥95%、样本数 >0 三条件硬门槛），N 轮不达标不再是一笔糊涂账 |
| 流程被概率污染（Measurement decay 的近亲） | **控制面** | Java 逻辑替掉 ReAct、多方案并行（1–4 个，须在保守/均衡/激进间拉开跨度）、异步调度、代码判定替掉模型自评——Agent 在自己这次执行里拿不到结论，没法靠一句自评把流程推到下一步 |

另有两处值得单独记下的设计。**存档点**：评测不通过后这一轮从哪份规则出发，由代码的 base 选取函数决定而非模型挑选——模型挑起点会按「哪处最容易让指标变好」排序，而不是「哪处最根本」；原文的说法是：*判决权我们已经收回来了，执行权如果还在被告手里，判决就只是建议。* **两类记忆**：失败反馈用完即弃、只注入紧接着的一轮；经验沉淀先落库再召回，中间隔一层蒸馏（只保留反复出现、有证据支持的结论），且**产出方案的 agent 不能给自己的方案写入库评价**。配套三道「不做无意义优化」的闸门：Q3 不触发定向重出；连续两轮不合格由代码终止转人工；已沉淀为反模式的策略下一轮生成前直接禁止。

实测水位（21 个方案）：Q1 占 61.9%，Q2 占 28.6%，Q4 占 9.5%——超过三分之一的方案让对侧样本退化，最坏单点 -45.95pt，全部被挡在评测阶段没有上线。作者直言：若把达标判定交给模型自评，这 6 个过拟合方案的大部分都会被判为优化成功。

把这套机制对回 Eigent 的术语，映射几乎是逐条的：近期商品集与 Δ_pop 就是 **counter-metric**；存放在模型上下文之外的阈值就是 **frozen anchors**；「模型不能修改阈值、不能覆盖判定」就是 **references have owners**；经验蒸馏—落库—召回就是 **improvement graph**，双 Loop 各自闭环就是 **work graph** 的分解。协作边界一句话：**模型产生判断，代码确认事实，人提供真值并决定上线。**

> 作者对演进顺序的判断值得原文照录：*Agent 的设计思路里最重要的是顺序：先有判断好坏的评测基准，再有跑起来的 Agent。评测基准出现之前，架构上的争论——Loop 还是 Graph、单 Agent 还是多 Agent、要不要接框架——都少一个能被证伪的对象。* 这与 §7 动作 1「指标成对上线」互为表里：判据不立，自主权给多给少都无从谈起。

## 5. Agent 协作拓扑：中心协调者与点对点共享邮箱

Graph Engineering 不只关乎有哪些节点，还关乎**边指向哪里、综合（synthesis）发生在哪个节点**。目前两个在售的多 agent 产品恰好展示了拓扑的两极，其取舍可以直接对照：

| 拓扑 | 代表（均为作者转述，非官方口径） | 边结构 | 收益 | 代价 |
|------|-------------------------------|--------|------|------|
| **Star（中心协调者）** | Kimi Agent Swarm：一个协调模型编排至多 300 个 sub-agent、至多 4,000 协调步；sub-agent 之间**不直接通信**，全部输出汇流给协调者综合 | 审计轨迹干净、冲突解决简单、系统上限显式 | 协调者的 context window 成为大规模综合的瓶颈 |
| **Mesh（共享邮箱）** | Claude Agent Teams：agent 可以横向通信，后端 agent 无需 orchestrator 转发就能把发现直接给前端 agent | 更自主，agent 可相互质疑、适合代码库内的对抗式分工 | agent 冲突时更难调试 |

由此可以抽出三条与拓扑相关的结论：

1. **拓扑决定冲突在哪里解决**。Star 型把所有冲突上收到协调者单点，审计简单但综合是瓶颈；Mesh 型把冲突分散到 agent 之间，自主但难调试。选型问题不是「哪个更先进」，而是「综合的复杂度能否装进单点」。
2. **「分解 → 并行 → 综合」（fan-out / fan-in）是 work graph 的典型形态**。原文观察：需要强一致综合的任务（如把上百个 sub-agent 的结果合成一份统一报告）比独立并行任务（如各写各的 CV）更耗时——耗时由**关键路径深度**决定，不由并行宽度决定。
3. **规模参数不是质量保障**。原文结语：*300 agents and 4,000 steps are system parameters, not quality guarantees*；*Speed without verification produces scaled-up errors, not scaled-up value*。节点再多，验证、prompt 工程与人的判断仍必须留在图外——这正是 §7 动作 1 与动作 4 的锚点纪律在产品视角下的表述。

> 来源声明：本节的 Kimi / Claude 对照取自一篇个人自媒体长文（全文无官方文档引用；其「文献综述」案例存在 10,000 与 100,000 字的自相矛盾，「Real outputs」案例也无可核验产物链接）。因此本文**只采纳其拓扑观点，不引用其数字作为事实，也不将其作为任何产品能力的证据**。Spec Kit 自身的对照：`parallel` 模式为 fan-out/fan-in（worker 间无共享状态、建议 2–6 个、上限见 [orchestration.md](../reference/teams/orchestration.md)），`serial` 为有向链（`blockedBy`），均无横向通信的 mailbox 机制，拓扑上属于 star / chain 一侧；`iteration` / `continuous` 的 verifier 与 supervisor 则承担了协调者角色。

## 6. Spec Kit 当前位置

结论：**Harness 级已成体系，Loop 级部分具备，Graph 级只有雏形。**

| 阶段 | Spec Kit 中的承载资产 | 成熟度 |
|------|---------------------|-------|
| Prompt | `templates/commands/*.md`（21 个 `/speckit.*` 命令模板）、`shared/` 片段 | 成熟——命令是稳定契约而非一次性提示 |
| Context | `instructions.md`（AGENTS.md）、glossary、feature index、memory 两层（[memory.md](../reference/skills/memory.md)）、skills 的 `references/` 渐进披露 | 成熟——已采用「入口薄、真相下沉」的结构 |
| Harness | Better Harness 目标锚点（五维模型；七态 evidenceState 定义在 `collect-evidence/references/evidence-discipline.md`，锚点文件只声明不可重定义）、workflow gates、Test-First、`scripts/` 确定性引擎、`gate-check.py` | 成熟——见 [better-harness.md](./better-harness.md) |
| Loop | EEI 三段质量闭环（[quality-loop.md](../reference/agents/quality-loop.md)）、`iteration` / `continuous` 团队与独立 verifier（[continuous-operations.md](../reference/teams/continuous-operations.md)）、feedback 与 `improve-*` 技能族 | 部分——循环形态齐备，但预算/停止条件散落各处，未成统一契约 |
| Graph | serial 模式的 `blockedBy` DAG 语义与环依赖拒绝（[orchestration.md](../reference/teams/orchestration.md)）、Team Supervisor 作为唯一 Meta **Role**（`evaluator` / `optimizer` 是它的 Stage，不是独立角色）、evidence 五泳道作为证据图雏形 | 雏形——有任务图与监督者，缺指标拓扑与锚点契约 |

三处明确缺口：**指标没有强制成对**（无 counter-metric / anchor 的显式契约）；**阈值与门禁的 owner 关系未显式化**（`gate.yaml` 的写路径清单、team 的 `threshold` / `max_iterations`、continuous 的 `budget` / `max_attempts` 分散在各处，谁可以改、改动是否留痕没有统一说法）；**跨层 cadence 契约缺失**（单个 continuous 团队已有 `config.cadence` 字段，但 `session` / `knowledge` / `constitution` 三层之间没有 daily / weekly / quarterly 的层级绑定）。

## 7. 五条可落地动作（不加 runtime）

| # | 动作 | 在 Spec Kit 里怎么做 | 触及维度 |
|---|------|-------------------|---------|
| 1 | **指标成对上线** | 任何改进断言必须同时给出优化指标、反指标与不可 game 的锚点；证据层已有的「配置 ≠ 使用」与 `Unobserved` 红线就是锚点纪律，只需在 `improve-*` 的断言格式中强制成对 | Change Validation |
| 2 | **reference 归属化** | 门禁与阈值都要有 owner：写路径门禁在 `gate.yaml`（`deny` / `confirm` / `allow` 通配清单，由 `gate-check.py` 判定），收敛阈值在 team 的 `threshold` / `max_iterations` 与 continuous 的 `budget` / `max_attempts`。执行中的循环不得自改这两类值；改动走 `/speckit.constitution` 或 ADR，并留痕 | Reliable Delivery |
| 3 | **速度分层、稀疏连边** | 显式区分快慢层：session memory（每次任务）→ knowledge memory（跨任务）→ constitution / features（治理层）；快层只能向上升级信号，不得覆盖慢层决定 | Learning Capture |
| 4 | **显式冻结节点** | 把「有意不可调」的东西列出来并技术性阻断写入：宪法原则、feedback 四条红线、verifier 默认 REJECT、真实测试结果为唯一 ground truth | Reliable Delivery |
| 5 | **区分 work graph 与 improvement graph** | `tasks.md` / `blockedBy` / handoff 链是 work graph，**保持无环**；`improve-*` / evidence / memory / feedback 是 improvement graph，**允许有环**。两张图混在一起就会出现「循环里自证成功」 | Controlled Execution |

动作 5 的分层与罗盘的工程边界同源：**执行图保持 DAG 以获得并行与依赖表达的确定性；学习与运营闭环允许有环，以实现持续改进。**

## 8. 反模式清单

- **单巨型入口文件**。`AGENTS.md` 当百科全书会同时踩四个坑：指导过多即等于没有指导、瞬间过期、难以验证、挤占稀缺的 context。应当是目录而非百科（OpenAI 实践中约 100 行）。
- **单指标飞轮**。自动化率越高不一定越好；确定性路由命中率越高也不一定越安全。指标绝不单独出行。
- **同一个 agent 既判断根因、又生成方案、又执行、又宣布成功**。一旦前序判断错误，后续会沿着同一错误自证。诊断、规划、授权、执行、验证必须分开，下游独立校验上游产物。
- **让模型直接生成最终可执行编排文件**。复杂依赖、回滚路径与审批节点一旦遗漏很难在执行前发现；应让模型输出结构简单的中间表示（IR），由代码做结构校验与图编译。
- **框架先行**。抽象层会遮蔽 prompt 与响应、难以调试，并诱发不必要的复杂度；先用最简方案，只在复杂度可证明改善结果时才增加。
- **靠推理代替确定性脚本**。跑脚本比推导步骤更便宜，也更可复现。
- **把 anchor 变成图内可优化节点**。「什么算更好」的判断必须外生于图，否则整套改进机器可以自洽地漂离现实。
- **中央大脑型 agent**。把语义决策与重试、调度、判定、编排打包进同一执行体，确定性部分的可靠性会被拉到概率性部分的水平，系统稳定性挂在最不稳定的一环上；天猫实证的修法是逐项分家而不是补提示词。
- **用提示词兜底目标函数的缺陷**。样本只有 badcase 时在提示词里写「不要过拟合」是无效的自我要求——对侧样本只能补进评测，补不进提示词。

## 9. 术语对照

| 英文 | 本文用法 | 与 Spec Kit 既有术语的关系 |
|------|---------|--------------------------|
| Harness | agent 工作的项目层执行环境资产 | 与 `.specify/shared/guidelines/better-harness.md` 同义；**不是** feedback 红线里指 agent CLI 运行时的 *harness*（host） |
| Loop | 重复工作周期直到停止条件满足 | 对应 EEI 质量闭环、`iteration` / `continuous` 团队 |
| Work graph / task graph | agent 做什么：节点为 tool/skill/artifact/subtask | 对应 `tasks.md`、`blockedBy`、handoff 链 |
| Improvement graph | 系统如何随时间改变自己 | 对应 evidence 五泳道、`improve-*`、memory、feedback |
| Star / Mesh（中心协调者 / 共享邮箱） | agent 图边拓扑的两极：全部边汇向单一综合节点 vs. agent 间横向通信边 | Spec Kit 的 `parallel` / `serial` 属 star / chain 一侧（无 mailbox 横向边），`iteration` / `continuous` 的 supervisor 与 verifier 充当协调者 |
| Anchor | 内部机器被禁止改写的外部固定节点 | 对应宪法原则、feedback 红线、真实测试结果 |
| Counter-metric | 与优化指标成对观察的反向指标 | Spec Kit 尚无显式契约（§6 缺口之一） |

## What this is not

- **不是新增机制或运行时。** 本文是坐标系与映射，不引入调度器、评分系统或图运行时；Spec Kit 仍是文档/提示框架（原则 IX）。
- **不是 Better Harness 的替代或分叉。** Harness 维度的定义、五维模型与七态 evidenceState 仍以 `.specify/shared/guidelines/better-harness.md` 为单一事实源，本文引用而不复述。
- **不是成熟度评级。** §6 的「成熟 / 部分 / 雏形」是定位判断而非评分，不产生报告制度，也不构成对任何单元的验收结论。
- **不转述未验证的业绩。** 引用的生产案例中，量化目标（自动化率、人效、准确率）在原文即标注为建设目标而非已实现结果，本文不将其作为证据使用。

## 参考来源

- Anthropic, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)（2025-09-29）
- Anthropic, [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)（2024-12-19）
- Anthropic, [Loop engineering: Getting started with loops](https://claude.com/blog/getting-started-with-loops)（2026-06-30）
- OpenAI, [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)（2026-02-11）
- Eigent, [Graph Engineering for AI Agents: Beyond Single Feedback Loops](https://www.eigent.ai/blog/graph-engineering-ai-agents)（2026-07-21）
- 刘必成（逐玖）, [天猫AI新品体检Graph Engineering实践：把「达标判定」从大模型手里收回来](https://ata.atatech.org/articles/11020753601)（2026-08-12）— 内部一手实践复盘，§4 实证案例来源
- Kirill (@kirillk_web3), [Kimi Agent Swarm: Complete A–Z Guide](https://x.com/kirillk_web3/article/2057497197638242362)（2026-05-21）— 二手来源（个人自媒体），仅用于 §5 的中心协调者 / 共享邮箱拓扑对照，其数字与案例不作为事实引用
- LangChain, [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) — 确定性步骤与 LLM 步骤同图混合的运行时参考
- Microsoft Research, [Project GraphRAG](https://www.microsoft.com/en-us/research/project/graphrag/) — 知识图与检索结合
- 基础工作：[GPT-3 few-shot](https://arxiv.org/abs/2005.14165)、[Chain-of-Thought](https://arxiv.org/abs/2201.11903)、[ReAct](https://arxiv.org/abs/2210.03629)

> **相关文档**：[better-harness.md](./better-harness.md)（Harness 维度权威定位）· [vibe-coding.md](./vibe-coding.md)（Agent / Skill / Tool 三层解耦）· [spec-driven.md](./spec-driven.md)（SDD 方法论）· [teams/overview.md](../reference/teams/overview.md)（多 agent 协作模式）
