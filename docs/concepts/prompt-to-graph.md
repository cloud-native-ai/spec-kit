# AI 工程演进：Prompt → Context → Harness → Loop → Graph

这条路径描述的不是模型能力的代际，而是**工程师需要负责的系统边界在逐级外扩**：从控制一次回答，到控制一次推理看到的世界，到控制 agent 工作的环境与护栏，到控制它如何持续行动与停止，最后到控制多个 agent、循环、数据、策略与人如何共同演进。本文用这条坐标系定位 Spec Kit 当前所处的位置，并给出在**不引入 runtime**（宪法原则 IX）的前提下继续外扩的动作。

> 概念来源：Anthropic *Effective context engineering for AI agents* / *Building effective agents* / *Loop engineering: Getting started with loops*，OpenAI *Harness engineering*，Eigent *Graph Engineering for AI Agents*；工程落点案例取自阿里云内部文章《罗盘背后的工程思考》。完整链接见文末「参考来源」。
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

| 失效模式 | 表现 | 修法（对应 §5 动作） |
|---------|------|-------------------|
| **Goodhart** | 指标与业务真相脱钩：工单解决率上升而续约流失翻倍，bot 学会把未解决单标为 solved | 指标成对 + 锚点（动作 1） |
| **Blindness upward** | loop 无法质疑自己的 reference：恒温器不能问 68°F 是否合适，eval loop 不能问 benchmark 是否匹配业务 | reference 有 owner（动作 2） |
| **Conflict** | 独立 loop 互相拆台而各自 dashboard 全绿：速度 loop 拆掉彻底性 loop | 速度分层、稀疏连边（动作 3） |
| **Measurement decay** | 没人监视监视者：报告只与其他报告对账，不与现实对账 | 冻结节点与只读 ground truth（动作 4） |

## 4. Spec Kit 当前位置

结论：**Harness 级已成体系，Loop 级部分具备，Graph 级只有雏形。**

| 阶段 | Spec Kit 中的承载资产 | 成熟度 |
|------|---------------------|-------|
| Prompt | `templates/commands/*.md`（21 个 `/speckit.*` 命令模板）、`shared/` 片段 | 成熟——命令是稳定契约而非一次性提示 |
| Context | `instructions.md`（AGENTS.md）、glossary、feature index、memory 两层（[memory.md](../reference/skills/memory.md)）、skills 的 `references/` 渐进披露 | 成熟——已采用「入口薄、真相下沉」的结构 |
| Harness | Better Harness 目标锚点（五维模型；七态 evidenceState 定义在 `collect-evidence/references/evidence-discipline.md`，锚点文件只声明不可重定义）、workflow gates、Test-First、`scripts/` 确定性引擎、`gate-check.py` | 成熟——见 [better-harness.md](./better-harness.md) |
| Loop | EEI 三段质量闭环（[quality-loop.md](../reference/agents/quality-loop.md)）、`iteration` / `continuous` 团队与独立 verifier（[continuous-operations.md](../reference/teams/continuous-operations.md)）、feedback 与 `improve-*` 技能族 | 部分——循环形态齐备，但预算/停止条件散落各处，未成统一契约 |
| Graph | serial 模式的 `blockedBy` DAG 语义与环依赖拒绝（[orchestration.md](../reference/teams/orchestration.md)）、Team Supervisor 作为唯一 Meta **Role**（`evaluator` / `optimizer` 是它的 Stage，不是独立角色）、evidence 五泳道作为证据图雏形 | 雏形——有任务图与监督者，缺指标拓扑与锚点契约 |

三处明确缺口：**指标没有强制成对**（无 counter-metric / anchor 的显式契约）；**阈值与门禁的 owner 关系未显式化**（`gate.yaml` 的写路径清单、team 的 `threshold` / `max_iterations`、continuous 的 `budget` / `max_attempts` 分散在各处，谁可以改、改动是否留痕没有统一说法）；**跨层 cadence 契约缺失**（单个 continuous 团队已有 `config.cadence` 字段，但 `session` / `knowledge` / `constitution` 三层之间没有 daily / weekly / quarterly 的层级绑定）。

## 5. 五条可落地动作（不加 runtime）

| # | 动作 | 在 Spec Kit 里怎么做 | 触及维度 |
|---|------|-------------------|---------|
| 1 | **指标成对上线** | 任何改进断言必须同时给出优化指标、反指标与不可 game 的锚点；证据层已有的「配置 ≠ 使用」与 `Unobserved` 红线就是锚点纪律，只需在 `improve-*` 的断言格式中强制成对 | Change Validation |
| 2 | **reference 归属化** | 门禁与阈值都要有 owner：写路径门禁在 `gate.yaml`（`deny` / `confirm` / `allow` 通配清单，由 `gate-check.py` 判定），收敛阈值在 team 的 `threshold` / `max_iterations` 与 continuous 的 `budget` / `max_attempts`。执行中的循环不得自改这两类值；改动走 `/speckit.constitution` 或 ADR，并留痕 | Reliable Delivery |
| 3 | **速度分层、稀疏连边** | 显式区分快慢层：session memory（每次任务）→ knowledge memory（跨任务）→ constitution / features（治理层）；快层只能向上升级信号，不得覆盖慢层决定 | Learning Capture |
| 4 | **显式冻结节点** | 把「有意不可调」的东西列出来并技术性阻断写入：宪法原则、feedback 四条红线、verifier 默认 REJECT、真实测试结果为唯一 ground truth | Reliable Delivery |
| 5 | **区分 work graph 与 improvement graph** | `tasks.md` / `blockedBy` / handoff 链是 work graph，**保持无环**；`improve-*` / evidence / memory / feedback 是 improvement graph，**允许有环**。两张图混在一起就会出现「循环里自证成功」 | Controlled Execution |

动作 5 的分层与罗盘的工程边界同源：**执行图保持 DAG 以获得并行与依赖表达的确定性；学习与运营闭环允许有环，以实现持续改进。**

## 6. 反模式清单

- **单巨型入口文件**。`AGENTS.md` 当百科全书会同时踩四个坑：指导过多即等于没有指导、瞬间过期、难以验证、挤占稀缺的 context。应当是目录而非百科（OpenAI 实践中约 100 行）。
- **单指标飞轮**。自动化率越高不一定越好；确定性路由命中率越高也不一定越安全。指标绝不单独出行。
- **同一个 agent 既判断根因、又生成方案、又执行、又宣布成功**。一旦前序判断错误，后续会沿着同一错误自证。诊断、规划、授权、执行、验证必须分开，下游独立校验上游产物。
- **让模型直接生成最终可执行编排文件**。复杂依赖、回滚路径与审批节点一旦遗漏很难在执行前发现；应让模型输出结构简单的中间表示（IR），由代码做结构校验与图编译。
- **框架先行**。抽象层会遮蔽 prompt 与响应、难以调试，并诱发不必要的复杂度；先用最简方案，只在复杂度可证明改善结果时才增加。
- **靠推理代替确定性脚本**。跑脚本比推导步骤更便宜，也更可复现。
- **把 anchor 变成图内可优化节点**。「什么算更好」的判断必须外生于图，否则整套改进机器可以自洽地漂离现实。

## 7. 术语对照

| 英文 | 本文用法 | 与 Spec Kit 既有术语的关系 |
|------|---------|--------------------------|
| Harness | agent 工作的项目层执行环境资产 | 与 `.specify/shared/guidelines/better-harness.md` 同义；**不是** feedback 红线里指 agent CLI 运行时的 *harness*（host） |
| Loop | 重复工作周期直到停止条件满足 | 对应 EEI 质量闭环、`iteration` / `continuous` 团队 |
| Work graph / task graph | agent 做什么：节点为 tool/skill/artifact/subtask | 对应 `tasks.md`、`blockedBy`、handoff 链 |
| Improvement graph | 系统如何随时间改变自己 | 对应 evidence 五泳道、`improve-*`、memory、feedback |
| Anchor | 内部机器被禁止改写的外部固定节点 | 对应宪法原则、feedback 红线、真实测试结果 |
| Counter-metric | 与优化指标成对观察的反向指标 | Spec Kit 尚无显式契约（§4 缺口之一） |

## What this is not

- **不是新增机制或运行时。** 本文是坐标系与映射，不引入调度器、评分系统或图运行时；Spec Kit 仍是文档/提示框架（原则 IX）。
- **不是 Better Harness 的替代或分叉。** Harness 维度的定义、五维模型与七态 evidenceState 仍以 `.specify/shared/guidelines/better-harness.md` 为单一事实源，本文引用而不复述。
- **不是成熟度评级。** §4 的「成熟 / 部分 / 雏形」是定位判断而非评分，不产生报告制度，也不构成对任何单元的验收结论。
- **不转述未验证的业绩。** 引用的生产案例中，量化目标（自动化率、人效、准确率）在原文即标注为建设目标而非已实现结果，本文不将其作为证据使用。

## 参考来源

- Anthropic, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)（2025-09-29）
- Anthropic, [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)（2024-12-19）
- Anthropic, [Loop engineering: Getting started with loops](https://claude.com/blog/getting-started-with-loops)（2026-06-30）
- OpenAI, [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)（2026-02-11）
- Eigent, [Graph Engineering for AI Agents: Beyond Single Feedback Loops](https://www.eigent.ai/blog/graph-engineering-ai-agents)（2026-07-21）
- LangChain, [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) — 确定性步骤与 LLM 步骤同图混合的运行时参考
- Microsoft Research, [Project GraphRAG](https://www.microsoft.com/en-us/research/project/graphrag/) — 知识图与检索结合
- 基础工作：[GPT-3 few-shot](https://arxiv.org/abs/2005.14165)、[Chain-of-Thought](https://arxiv.org/abs/2201.11903)、[ReAct](https://arxiv.org/abs/2210.03629)

> **相关文档**：[better-harness.md](./better-harness.md)（Harness 维度权威定位）· [vibe-coding.md](./vibe-coding.md)（Agent / Skill / Tool 三层解耦）· [spec-driven.md](./spec-driven.md)（SDD 方法论）· [teams/overview.md](../reference/teams/overview.md)（多 agent 协作模式）
