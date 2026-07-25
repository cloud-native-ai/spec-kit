---
name: manage-project
description: |
  轻量级项目管理技能（由 summarize-project 进化而来）。以一份 Markdown 项目管理文档为单一事实源，覆盖项目管理四要素：项目背景介绍（文本）、项目里程碑（里程碑视图）、项目主要工作（WBS 工作分解图）、项目进度追踪（甘特图）。所有图表以文本形态的 PlantUML 源码直接嵌入管理文档（可编辑、可 diff、可版本管理），渲染校验一律委托 draw-plantuml 技能完成，本技能不含渲染脚本。支持重复运行以增量更新进度。
  Use when the user mentions "项目管理", "管理项目", "项目背景", "项目里程碑", "里程碑", "进度追踪", "项目进度", "项目总结", "项目汇报", "进展报告", "项目进展", "manage project", "project management", "milestone", "progress tracking", "summarize project", "project summary", "project report", "WBS", "工作分解", "甘特图".
skill_id: "<SKILL:.specify/skills/manage-project/SKILL.md>"
---

# 轻量级项目管理技能

以**一份 Markdown 项目管理文档**（默认 `docs/project-management/project.md`，用户可指定其他位置）作为项目的单一事实源，持续管理项目管理的四个核心要素：

| 要素 | 载体 | 形态 |
|------|------|------|
| 1. 项目背景介绍 | 管理文档 `## 项目背景` 节 | Markdown 文本（背景、目标、干系人、范围） |
| 2. 项目里程碑 | 管理文档 `## 项目里程碑` 节 | 里程碑视图：仅含 `happens` 里程碑条目的 `@startgantt` 图（PlantUML 源码嵌入）+ 跟踪表格 |
| 3. 项目主要工作 | 管理文档 `## 主要工作` 节 | WBS 工作分解图：`@startwbs`（PlantUML 源码嵌入） |
| 4. 项目进度追踪 | 管理文档 `## 进度追踪` 节 | 甘特图：`@startgantt`，三态进度 + 当前日期参照线（PlantUML 源码嵌入） |

**图表即文本**：所有图表以 PlantUML 源码形式写在管理文档的 ```` ```plantuml ```` 代码块中——源码是唯一权威形态，可直接编辑、可 diff、可随 git 演进；渲染出的图片只是派生产物。这是与一次性"汇报文档"的本质区别：管理文档要被**持续修改与跟踪**，而不是一次性输出。

图表语法、渲染与产物约定全部委托 **draw-plantuml** 技能；本技能只做信息组织、文档管理与进度维护，不含渲染脚本。

## 核心原则

- **单一事实源**：一份管理文档承载全部四要素；重复运行本技能时**增量更新**该文档（刷新进度、追加里程碑、修订分解），绝不推倒重写用户已有的人工编辑内容。
- **单一分解口径**：先产出一棵**工作分解树**（阶段 → 任务 →（可选）子任务），WBS 图、甘特图、里程碑视图都由它派生——三处工作项/里程碑命名逐字一致，无孤儿条目。
- **可溯源，不臆造**：每个工作项与里程碑必须能溯源到输入材料（文档、`.specify/specs/` 规格、任务清单、git 历史、用户描述）。材料里没有的工作，宁可提问也绝不编造。
- **图源嵌入，渲染委托**：PlantUML 源码嵌入管理文档；WBS 走 draw-plantuml 的 `@startwbs` 能力，里程碑视图与甘特图走 `@startgantt` 能力。渲染仅用于**语法校验与可选配图**，产物机制以 draw-plantuml 为准。
- **管理者与读者兼顾**：命名用业务语言，避免内部黑话；每张图配一段简要说明，外部读者不读代码也能看懂。

## 工作流

按以下 6 个步骤顺序执行。

### Step 1: 加载或初始化管理文档

检查目标位置（默认 `docs/project-management/project.md`）是否已有管理文档：

- **已存在 → 更新模式**：读取现有文档，解析四要素现状（背景文本、里程碑清单、WBS 树、甘特条目与状态），本次运行只做增量更新；保留用户手工修改的措辞与补充内容。
- **不存在 → 初始化模式**：按管理文档结构（见 [references/management-playbook.md](references/management-playbook.md) §1）创建骨架，再进入后续步骤填充。

### Step 2: 收集项目材料与溯源

从用户提供或工作区可用的材料中收集：项目背景信息（目标、干系人、范围）、工作项、里程碑事件。为每个工作项记录：**名称、来源出处、状态（completed / in-progress / not-started）、进度百分比（in-progress 时必填）、时间信息（若有）、负责人（若有）**；为每个里程碑记录：**名称、锚定方式（绝对日期或关联工作项结束点）、达成状态**。材料不足时按「信息不足与澄清」节处理，不臆造。

### Step 3: 工作分解与里程碑定稿

把工作项自顶向下组织为**阶段 → 任务 →（可选）子任务**的单一分解树，并确定里程碑清单（关键评审、发布、验收节点）。这棵树与这份清单是后续所有图表的唯一数据源：先在上下文中定稿（命名、层级、归属、锚定），再进入绘图步骤。分解深度与命名规范见 [references/management-playbook.md](references/management-playbook.md)。

### Step 4: 生成或更新嵌入式图表源码

在管理文档对应章节内以 ```` ```plantuml ```` 代码块写入/更新三类图表源码：

1. **WBS 工作分解图**（`## 主要工作`）：`@startwbs` 渲染分解树，遵循 draw-plantuml 的 `references/howto/13-wbs-diagram.md`。项目过大时按「大项目与图集拆分」节拆分。
2. **里程碑视图**（`## 项目里程碑`）：仅含里程碑条目的紧凑 `@startgantt` 图——每个里程碑用 `[名称] happens <日期>` 或 `happens at [工作项]'s end` 声明为零工期菱形节点，配套一张「里程碑 | 锚定 | 状态」Markdown 表格，使里程碑既可视又可逐行跟踪。
3. **进度甘特图**（`## 进度追踪`）：`@startgantt` 渲染带时间信息的工作项，遵循 `references/howto/14-gantt-diagram.md`。必须包含：
   - **进度状态语义**：completed / in-progress（带完成百分比）/ not-started 三态视觉可辨；项目进行期须标出当前日期参照线；
   - **里程碑**：与里程碑视图同名同锚定的 `happens` 菱形节点；
   - **依赖关系**：工作项间先后依赖按材料呈现，无依据时不虚构依赖。

更新模式下只改动受影响的条目（状态、百分比、新增/移除行），保持其余源码稳定以便 diff 审阅。

### Step 5: 渲染校验（委托 draw-plantuml）

将文档中每个 PlantUML 代码块交给 draw-plantuml 技能渲染一次，验证语法正确、版面可读（布局与输出约定见其 `references/howto/12-rendering-and-output.md`）。校验失败则修正源码后重试。渲染出的 PNG/SVG 图片为**可选配套产物**：存放于管理文档同目录，文档中可在源码块之后以相对路径引用图片，但嵌入的源码始终保留、始终是权威形态。

### Step 6: 一致性自检与文档落盘

执行**三图一致性自检**：WBS 叶子工作项（带时间信息的）与甘特条目一一对应、命名一致；里程碑视图与甘特图中的里程碑同名同锚定；三态口径在图与叙述间一致。清单见 [references/management-playbook.md](references/management-playbook.md)。通过后写入管理文档，并刷新元信息（最后更新日期、本次变更摘要、估计假设逐条显式标注）。

## 信息不足与澄清

材料不足以支撑背景叙述、分解或排期时，二选一：(a) 给出合理默认并在管理文档中**显式标注为估计假设**；(b) 当猜测会实质性误导范围/时间/状态时，最多发起**一轮**澄清提问（不超过 4 个问题），随后继续执行。猜测不得静默扭曲工作范围、日期或状态。

## 大项目与图集拆分

单图放不下时做图集拆分：一张概览图（只到阶段层）+ 每个阶段一张下钻子图，每张子图都是文档内独立的 PlantUML 源码块，图间命名/配色/编号一致并互相交叉引用。拆分规则与阈值见 [references/management-playbook.md](references/management-playbook.md)。

## 管理范围与受众粒度

用户可限定**管理周期**（如本迭代/本季度）或**受众粒度**（如高管层只看阶段级）：周期受限时甘特时间轴与叙述只覆盖该范围，范围外工作省略或明显弱化；粒度受限时分解到指定深度即止，保持阶段级结构完整。详见 [references/management-playbook.md](references/management-playbook.md)。

## 参考文档

- [references/management-playbook.md](references/management-playbook.md) — 管理文档结构、更新模式规则、分解深度、估计默认与假设标注、状态推断、里程碑跟踪、图集拆分、三图一致性清单、范围/粒度控制
- draw-plantuml 技能：`references/howto/13-wbs-diagram.md`（WBS）、`references/howto/14-gantt-diagram.md`（甘特图与里程碑）、`references/howto/12-rendering-and-output.md`（渲染与输出约定）

## Feedback

At the end of a substantial run of this skill, perform an agent self-reflection step (never solicit feedback content from the user), following the canonical convention in `.specify/shared/workflow/feedback-step.md`:

1. **Gate on qualification & completion.** Only proceed if this run reached a meaningful wrap-up. Skip trivial/no-op runs; for an aborted run use the abort/partial rule below.
2. **Reflect (no user input).** Review this run against this skill's declared purpose and produce a short review plus ≥1 concrete, skill-specific optimization point. If the run was clean, use exactly: `No significant optimization points identified this run.`
3. **Scope guard.** Keep strictly to this skill's operation; do NOT produce a global/whole-project assessment (that is `/speckit.review`'s job). Entries are `scope: local`.
4. **Dedup guard.** Use a stable `run_id`; if a parent flow already recorded feedback for this same `(unit_id, run_id)`, the engine no-ops.
5. **Persist** via the engine:
   ```bash
   python3 "${SKILL_WORKDIR:-.}/.specify/scripts/python/feedback-utils.py" --action record \
     --unit-id "skill:manage-project" --unit-type skill \
     --run-id "<stable-run-id>" --feature "<feature-key-if-any>" \
     --review "<review prose>" --points-file "<points file>"
   ```
6. **Consolidated submission prompt.** If the returned `should_prompt` is `true`, surface a single consolidated prompt inviting the user to submit collected feedback to the Spec Kit developers; on confirmation run `--action mark-submitted`. Below threshold, do not prompt.

**Abort / partial-run rule.** If the run failed before wrap-up, either skip recording or record with `--partial` and a `## Review` beginning `**Partial run** — `.
