---
name: summarize-project
description: |
  项目总结与可视化汇报技能。收集项目工作项并自顶向下分解，生成 WBS 工作分解结构图与甘特图（里程碑、时间安排、进度状态），输出自包含 HTML 汇报文档，让外部人员通过图表直观了解当前项目进展。图表渲染一律委托 draw-plantuml 技能完成，本技能不含渲染脚本。
  Use when the user mentions "项目总结", "项目汇报", "进展报告", "项目进展", "summarize project", "project summary", "project report", "WBS", "工作分解", "甘特图", "项目进度汇报", "对外汇报".
skill_id: "<SKILL:.specify/skills/summarize-project/SKILL.md>"
---

# 项目可视化总结技能

面向外部人员（非项目团队的管理者、客户、协作方）的项目总结与汇报：把项目材料整理为一棵**单一工作分解树**，用 WBS 图回答"项目由哪些工作组成"，用甘特图回答"各项工作的里程碑、时间安排与当前进度"，最终输出一份自包含 HTML 汇报文档。图表渲染（PlantUML 语法、渲染、图片约定）全部委托 **draw-plantuml** 技能；本技能只做信息组织与叙事，不含渲染脚本。

## 核心原则

- **单一分解口径**：先产出一棵工作分解树，WBS 图与甘特图都由它派生——两图工作项命名完全一致，每个带时间信息的叶子工作项都出现在甘特图中（反之亦然，无孤儿条目）。
- **可溯源，不臆造**：每个工作项必须能溯源到输入材料（文档、规格、任务清单、git 历史、用户描述）。材料里没有的工作，宁可提问也绝不编造。
- **渲染委托**：WBS 走 draw-plantuml 的 `@startwbs` 能力，甘特图走 `@startgantt` 能力；渲染脚本、PNG/SVG 产出、HTML 组装约定均以 draw-plantuml 为准，本技能不重复实现。
- **外部读者优先**：图和文字都为"没参与项目的人"服务——命名用业务语言，避免内部黑话；每张图配一段简要说明。

## 工作流

按以下 5 个步骤顺序执行。

### Step 1: 收集项目材料与工作项溯源

从用户提供或工作区可用的材料中收集工作项：项目文档、`.specify/specs/` 规格、任务清单、计划文档、git 提交/标签历史、对话描述。为每个工作项记录：**名称、来源出处、状态（completed / in-progress / not-started）、进度百分比（in-progress 时必填）、时间信息（若有）、负责人（若有）**。材料不足时按「信息不足与澄清」节处理，不臆造。

### Step 2: 工作分解（单一分解树）

把工作项自顶向下组织为**阶段 → 任务 →（可选）子任务**的层级树。这棵树是后续两张图的唯一数据源：先在上下文中把它定稿（命名、层级、归属），再进入绘图步骤。分解深度与命名规范见 [references/reporting-playbook.md](references/reporting-playbook.md)。

### Step 3: 渲染 WBS 图（委托 draw-plantuml）

将分解树渲染为 WBS 工作分解结构图：使用 draw-plantuml 技能的 `@startwbs` 能力，遵循其操作指南 `draw-plantuml/references/howto/13-wbs-diagram.md` 的语法与美观要点。项目过大时按「大项目与图集拆分」节拆为概览图 + 下钻子图。

### Step 4: 渲染甘特图（委托 draw-plantuml）

将同一分解树中带时间信息的工作项渲染为甘特图：使用 draw-plantuml 技能的 `@startgantt` 能力，遵循 `draw-plantuml/references/howto/14-gantt-diagram.md`。必须包含：
- **里程碑（milestone）**：关键节点（评审、发布、验收）以零工期菱形标记，锚定到日期或关联工作项结束点；
- **进度状态语义**：completed / in-progress（带完成百分比）/ not-started 三态在图上视觉可辨（颜色/百分比标注），项目进行期须标出当前日期参照线；
- **依赖关系**：工作项间的先后依赖按材料呈现，无依据时不虚构依赖。

完成后执行**两图一致性自检**：WBS 叶子工作项（带时间信息的）与甘特条目一一对应、命名一致；清单见 [references/reporting-playbook.md](references/reporting-playbook.md)。

### Step 5: 组装自包含 HTML 汇报

输出**单个自包含 HTML 文档**，默认写入目标工作区的 `docs/project-summary/` 目录（用户可指定其他位置覆盖），内容包括：
1. **概览叙述**：项目背景、目标、当前进展摘要——外部读者不看代码也能读懂；
2. **WBS 图 + 简要说明**；3. **甘特图 + 简要说明**；
4. **元信息**：报告生成日期、汇报范围（scope，默认全项目生命周期）、所有估计性假设（assumptions，逐条显式标注）。

输出约定（与 draw-plantuml 一致）：每张图同时产出 **PNG 与 SVG**（默认引用 PNG，过大/需缩放时 SVG），HTML 以相对路径引用同目录图片，`.puml` 源文件保留在同目录以备后续编辑，报告中**不内嵌原始图源码**。HTML 组装方式与图片引用机制遵循 draw-plantuml 的输出要求与其 `references/howto/12-rendering-and-output.md`。

## 信息不足与澄清

材料不足以支撑分解或排期时，二选一：(a) 给出合理默认并在报告中**显式标注为估计假设**；(b) 当猜测会实质性误导范围/时间/状态时，最多发起**一轮**澄清提问（不超过 4 个问题），随后继续执行。猜测不得静默扭曲工作范围、日期或状态。

## 大项目与图集拆分

单图放不下时做图集拆分：一张概览图（只到阶段层）+ 每个阶段一张下钻子图，图间命名/配色/编号一致并互相交叉引用。拆分规则与阈值见 [references/reporting-playbook.md](references/reporting-playbook.md)。

## 汇报范围与受众粒度

用户可限定**汇报周期**（如本迭代/本季度）或**受众粒度**（如高管层只看阶段级）：周期受限时甘特时间轴与叙述只覆盖该范围，范围外工作省略或明显弱化；粒度受限时分解到指定深度即止，保持阶段级结构完整。详见 [references/reporting-playbook.md](references/reporting-playbook.md)。

## 参考文档

- [references/reporting-playbook.md](references/reporting-playbook.md) — 分解深度、估计默认与假设标注、状态推断、图集拆分、两图一致性清单、范围/粒度控制
- draw-plantuml 技能：`references/howto/13-wbs-diagram.md`（WBS）、`references/howto/14-gantt-diagram.md`（甘特图）、`references/howto/12-rendering-and-output.md`（渲染与输出约定）

## Feedback

At the end of a substantial run of this skill, perform an agent self-reflection step (never solicit feedback content from the user), following the canonical convention in `.specify/shared/workflow/feedback-step.md`:

1. **Gate on qualification & completion.** Only proceed if this run reached a meaningful wrap-up. Skip trivial/no-op runs; for an aborted run use the abort/partial rule below.
2. **Reflect (no user input).** Review this run against this skill's declared purpose and produce a short review plus ≥1 concrete, skill-specific optimization point. If the run was clean, use exactly: `No significant optimization points identified this run.`
3. **Scope guard.** Keep strictly to this skill's operation; do NOT produce a global/whole-project assessment (that is `/speckit.review`'s job). Entries are `scope: local`.
4. **Dedup guard.** Use a stable `run_id`; if a parent flow already recorded feedback for this same `(unit_id, run_id)`, the engine no-ops.
5. **Persist** via the engine:
   ```bash
   python3 "${SKILL_WORKDIR:-.}/.specify/scripts/python/feedback-utils.py" --action record \
     --unit-id "skill:summarize-project" --unit-type skill \
     --run-id "<stable-run-id>" --feature "<feature-key-if-any>" \
     --review "<review prose>" --points-file "<points file>"
   ```
6. **Consolidated submission prompt.** If the returned `should_prompt` is `true`, surface a single consolidated prompt inviting the user to submit collected feedback to the Spec Kit developers; on confirmation run `--action mark-submitted`. Below threshold, do not prompt.

**Abort / partial-run rule.** If the run failed before wrap-up, either skip recording or record with `--partial` and a `## Review` beginning `**Partial run** — `.
