---
name: 可视化技能竞技场团队
slug: viz-skill-arena
description: 语义/语法分离的六技能绘图体系竞技——draw-diagram 产出语义绘图规格(SDS: 逻辑模型+几何+视觉权重)，draw-{d3js,echarts,excalidraw,mermaid,plantuml} 并行做语法实现，两轮多裁判评审 + 一次重绘，持续优化整个绘图技能体系
goal: >
  通过「用户下发图表任务 → draw-diagram 构建语义绘图规格 SDS(逻辑图模型 + 图元几何 + 视觉权重语义) →
  5 个语法引擎并行按 SDS 实现同一图表 → 第一轮 3 名裁判从不同角度打分 → 根据评审意见优化对应技能
  (工作副本)并重绘 → 第二轮 2 名新裁判评审并选出冠军 → 记录结论」的循环，逐步建立「需求类型 → 最优技能」
  的匹配知识(结论账本)，并持续优化语义层(draw-diagram)与六个语法层技能。
  成功标准(每轮)：(1) 产出该任务冠军技能与匹配结论，追加至结论账本
  .specify/memory/knowledge/visualization-skill-selection.md；(2) 被采纳的技能变更(经第二轮独立裁判接受、
  无回退)合并回对应 canonical 技能目录并同步镜像；(3) 加权评分维度：语义保真 0.30 / 视觉质量 0.30 /
  需求契合 0.25 / 可复现可维护 0.15，冠军 = 该轮最高加权分(≥0.85 采纳线)；技能变更采纳门 = 重绘后加权分
  ≥ 第一轮自身分(无回退)；(4) 分离纪律：SDS 不得含引擎语法，语法层不得自行改写语义(几何/权重偏离必须声明)。
goal_slug: visualization-skill-selection
territory:
  write:
    - skills/draw-diagram/**
    - skills/draw-d3js/**
    - skills/draw-echarts/**
    - skills/draw-excalidraw/**
    - skills/draw-mermaid/**
    - skills/draw-plantuml/**
    - .specify/memory/knowledge/visualization-skill-selection.md
    - docs/figures/**
  read:
    - skills/**
    - .specify/skills/**
    - .qoder/skills/draw-*
    - .specify/teams/viz-skill-arena/**
    - .specify/shared/**
  forbidden:
    - .specify/teams/other-slug/**
  non_path:
    - { type: skill-invocation, target: 六个绘图技能的运行(SDS 建模、渲染脚本执行、技能工作副本重载) }
pattern: continuous
preset: capability-arena   # 竞技模式实例(语义层+5语法引擎同题竞技);preset 由原 skills-arena 泛化而来
created: 2026-08-07
updated: 2026-09-15
members:
  - agent: agent-team-supervisor-template
    role: team-supervisor
    stage: meta
    type: Meta
    lifecycle: persistent
    responsibility: 唯一 Meta。读任务 → 派发 semantic-modeler → 并行派发 5 语法实现者 → 派发 R1 三裁判 → 聚合反馈并把改进写入 6 个技能工作副本(target，不改被评图)→ 派发 5 重绘 → 派发 R2 两裁判 → 冠军裁定 → 采纳的技能变更合并回 canonical + 镜像同步 → 追加结论账本 → 写 run report / STATE / run-log
  - agent: agent-stage-executor-template
    role: semantic-modeler
    stage: executor
    type: Worker
    lifecycle: temporary
    responsibility: 加载 skills/draw-diagram，吃透任务上下文/目标图，产出语义绘图规格 SDS(逻辑图模型 + 图元几何 x/y/w/h + 分区盒 + 视觉权重语义 + 排版层级)，落盘 run workspace 供 5 个语法实现者消费；R1 后按裁判对语义层的意见修订 SDS 一次
  - agent: agent-stage-executor-template
    role: drawer-d3js
    stage: executor
    type: Worker
    lifecycle: temporary
    responsibility: 语法实现者：读 SDS，用 draw-d3js 的语法与渲染管线精确实现几何与视觉权重(绝对坐标引擎，零偏离)；R1 后重载更新后的技能重绘一次；偏离必须声明(本引擎预期零偏离)
  - agent: agent-stage-executor-template
    role: drawer-echarts
    stage: executor
    type: Worker
    lifecycle: temporary
    responsibility: 同上(skills/draw-echarts；固定坐标 config 管线实现 SDS 几何)
  - agent: agent-stage-executor-template
    role: drawer-excalidraw
    stage: executor
    type: Worker
    lifecycle: temporary
    responsibility: 同上(skills/draw-excalidraw；场景 JSON 按 SDS 几何落坐标 + 手绘美学开关)
  - agent: agent-stage-executor-template
    role: drawer-mermaid
    stage: executor
    type: Worker
    lifecycle: temporary
    responsibility: 同上(skills/draw-mermaid；自动布局引擎：以脚手架逼近 SDS 几何，偏离必须量化声明)
  - agent: agent-stage-executor-template
    role: drawer-plantuml
    stage: executor
    type: Worker
    lifecycle: temporary
    responsibility: 同上(skills/draw-plantuml；自动布局引擎：以 skinparam/hidden-link 逼近 SDS 几何，偏离必须量化声明)
  - agent: agent-stage-evaluator-template
    role: judge-r1-technical
    stage: evaluator
    type: Worker
    lifecycle: temporary
    responsibility: 第一轮裁判·技术角度——SDS 覆盖(元素/关系/分区/几何/权重是否被实现)/渲染成功(按 4 维打分，输出 [DIM]_SCORE/WEIGHTED_TOTAL/SUGGESTIONS，建议区分语义层与语法层归属)
  - agent: agent-stage-evaluator-template
    role: judge-r1-visual
    stage: evaluator
    type: Worker
    lifecycle: temporary
    responsibility: 第一轮裁判·视觉角度——美观/排版/对齐/配色/清晰度/视觉权重层级是否兑现
  - agent: agent-stage-evaluator-template
    role: judge-r1-semantic
    stage: evaluator
    type: Worker
    lifecycle: temporary
    responsibility: 第一轮裁判·需求角度——需求契合度/表达适切性/信息组织/SDS 建模质量
  - agent: agent-stage-evaluator-template
    role: judge-r2-quality
    stage: evaluator
    type: Worker
    lifecycle: temporary
    responsibility: 第二轮裁判(与 R1 不同成员)·综合质量——对重绘后 5 图按同一 4 维加权打分，裁定冠军
  - agent: agent-stage-evaluator-template
    role: judge-r2-match
    stage: evaluator
    type: Worker
    lifecycle: temporary
    responsibility: 第二轮裁判·匹配裁定——确认冠军、复核无回退门、给出「需求类型→技能」匹配结论草稿(供 supervisor 写入账本)
config:
  maturity: L2                 # 用户明确要求循环内修改技能(重绘=改技能工作副本+重绘)；独立验证 = R2 裁判组(独立 sub-agent，默认 REJECT)
  cadence: on-demand           # 用户下发图表任务即触发一个 cycle(非定时)
  verifier: independent
  max_attempts_per_item: 1     # 每位实现者恰好一次重绘(用户规则)
  quality_dimensions:
    - name: semantic-fidelity  # SDS 覆盖:元素/关系/分区/几何/视觉权重是否被忠实实现
      weight: 0.30
    - name: visual-quality     # 视觉美观/排版清晰/权重层级兑现
      weight: 0.30
    - name: requirement-fit    # 需求契合/表达适切
      weight: 0.25
    - name: reproducibility    # 可复现/可维护(SDS 与语法源清晰、可重渲)
      weight: 0.15
  threshold: 0.85              # 冠军采纳线(R2 加权分)
  no_regression: true          # 技能变更采纳门:重绘后加权分 ≥ R1 自身分
  co_targets:
    - skills/draw-diagram
    - skills/draw-d3js
    - skills/draw-echarts
    - skills/draw-excalidraw
    - skills/draw-mermaid
    - skills/draw-plantuml
  layering: 语义层(draw-diagram)只产 SDS(逻辑模型+几何+视觉权重+排版层级)，不含引擎语法；语法层(draw-*)只实现 SDS(语法结构+引擎渲染质量实践)，不改写语义——几何/权重偏离必须量化声明；「需求→技能匹配」结论归结论账本；被评图与运行中间件只进 .specify/teams/.work/viz-skill-arena/
  conclusion_ledger: .specify/memory/knowledge/visualization-skill-selection.md
  deliverables_dir: .specify/teams/.work/viz-skill-arena/   # 每轮冠军图默认交付路径(git-ignored，单轮任务可覆盖)
  budget:
    max_cycles_per_day: 3
    max_tokens_per_day: 200000
    max_subagents_per_cycle: 16
    on_80pct: report-only
    on_100pct: halt
  kill_switch: loop-pause-all
  constraints_file: .specify/teams/viz-skill-arena/constraints.md
  state_spine: .specify/teams/viz-skill-arena/STATE.md
  run_log: .specify/teams/viz-skill-arena/run-log.jsonl
  summary:
    enabled: true
    every: 5
    interactive: false
---

## Goal

**目标**：通过「语义/语法分离的六技能绘图体系竞技 + 两轮多裁判评审 + 一次重绘」的循环，逐步建立「需求类型 → 最优绘制技能」的匹配知识，并持续优化语义层（draw-diagram）与五个语法层技能（draw-d3js / draw-echarts / draw-excalidraw / draw-mermaid / draw-plantuml）。

**成功标准（每轮 cycle）**：
1. 冠军裁定：第二轮裁判按加权维度（语义保真 0.30 / 视觉质量 0.30 / 需求契合 0.25 / 可复现可维护 0.15）打分，最高加权分且 ≥0.85 者为冠军；
2. 结论记录：冠军 + 「该任务类型 → 推荐技能」匹配结论追加至 `.specify/memory/knowledge/visualization-skill-selection.md`（结论账本，跨轮累积）；
3. 技能优化：R1 评审意见 → supervisor 将改进写入对应技能**工作副本**（target）→ 实现者重载后重绘 → R2 接受（重绘分 ≥ R1 自身分，无回退）→ 变更合并回 canonical `skills/draw-*/` 并同步 `.specify/skills/` 与 `.qoder/skills/` 副本；
4. 分离纪律：SDS 不含引擎语法；语法层不自行改写语义，几何/视觉权重偏离必须量化声明（自动布局引擎的逼近偏离计入其语法实现质量，不计为语义层缺陷）；
5. 每轮产出 run report（`.specify/teams/viz-skill-arena/runs/`）+ STATE.md 更新 + run-log 一行。

## Static Structure

| Agent | Role | Stage | Type | Lifecycle |
|-------|------|-------|------|-----------|
| agent-team-supervisor-template | team-supervisor | meta | **Meta**（唯一；写技能定义/配置/账本） | persistent |
| agent-stage-executor-template | semantic-modeler | executor | Worker（产出 SDS=业务语义产物） | temporary |
| agent-stage-executor-template | drawer-d3js | executor | Worker（语法实现=渲染业务产物） | temporary |
| agent-stage-executor-template | drawer-echarts | executor | Worker | temporary |
| agent-stage-executor-template | drawer-excalidraw | executor | Worker | temporary |
| agent-stage-executor-template | drawer-mermaid | executor | Worker | temporary |
| agent-stage-executor-template | drawer-plantuml | executor | Worker | temporary |
| agent-stage-evaluator-template | judge-r1-technical | evaluator | Worker（评分对象=渲染出的图 vs SDS） | temporary |
| agent-stage-evaluator-template | judge-r1-visual | evaluator | Worker | temporary |
| agent-stage-evaluator-template | judge-r1-semantic | evaluator | Worker | temporary |
| agent-stage-evaluator-template | judge-r2-quality | evaluator | Worker | temporary |
| agent-stage-evaluator-template | judge-r2-match | evaluator | Worker | temporary |

Type 判定说明：裁判评分对象是渲染出的图表（业务产物）→ Worker；semantic-modeler 产出 SDS（业务语义产物）→ Worker；唯一 Meta 是 Team Supervisor。

## Dynamic Structure

**Pattern**：continuous（长期运营）。优先级：长期改进（需求-技能匹配知识 + 语义/语法两层技能质量），用户每下发一个图表任务 = 一个 cycle；cycle 内部是「语义建模 → 并行语法实现 → 并行评审 → 定向重绘 → 独立复审」的锦标赛结构。

**Per-cycle 执行流**：

```
用户下发图表任务 T(含目标路径)
  │
  ▼
SUPERVISOR: 读 constraints.md + 预算 + STATE.md 最近结论;确定任务目标路径
  │
  ▼ PHASE A0 — 语义建模(单 agent, draw-diagram)
  semantic-modeler: 吃透 T → 产出 SDS(逻辑模型 + 图元几何 + 分区盒 + 视觉权重 + 排版层级)
  → run workspace: cycle-N/sds.md(或 sds.json)
  │
  ▼ PHASE A — 并行语法实现(5 个实现者同时派发, territory 无写重叠)
  drawer-d3js / drawer-echarts / drawer-excalidraw / drawer-mermaid / drawer-plantuml
  各读 SDS + 最新技能工作副本 → 以引擎语法实现 SDS → 结果清单(图路径/偏离声明)→ run workspace
  │
  ▼ PHASE B — 第一轮评审(3 名裁判并行, 不同角度; 对照 SDS 判覆盖)
  judge-r1-technical / judge-r1-visual / judge-r1-semantic
  对 5 张图按 4 维加权打分 + 每技能 SUGGESTIONS(标注语义层/语法层归属)
  │
  ▼ PHASE C — 技能优化(score = f(target) 不变式)
  SUPERVISOR 聚合 R1 反馈 → 语义层意见改 draw-diagram 工作副本(SDS 建模规则),
  语法层意见改对应 draw-* 工作副本(语法实现规则); 只改 target, 不手改被评图
  │
  ▼ PHASE D — 重绘(semantic-modeler 修订 SDS 一次 + 5 实现者再次并行, 每人恰好一次)
  │
  ▼ PHASE E — 第二轮评审(2 名新裁判并行, 独立验证, 默认 REJECT)
  judge-r2-quality(综合加权打分)+ judge-r2-match(冠军裁定 + 无回退复核 + 匹配结论草稿)
  │
  ▼ PHASE F — 收尾(supervisor 独占写)
  冠军宣布 → 被采纳技能变更合并回 canonical + sync-mirrors.py --write + .qoder 副本
  → 结论账本追加(需求类型→技能 + 理由 + 本轮技能改动摘要)
  → run report + STATE.md 更新 + run-log 一行
```

**关键机制**：
- **score = f(target) 不变式**：每轮优化的对象是技能（target 工作副本），被评图由「最新 target 重生成」——绝不手改被评图；采纳的最优 target 落真实路径为标准输出。
- **分离纪律**：SDS 是语义层与语法层的唯一交接契约（schema 见 `skills/draw-diagram/references/semantic-model.md`）；语法层偏离 SDS 几何/权重必须量化声明，未声明的偏离按语义保真扣分。
- **独立验证**：R2 裁判是与 R1 完全不同的 sub-agent，默认 REJECT；无回退门（重绘分 ≥ R1 自身分）未过 → 该技能变更不合并。
- **上下文隔离**：每个 sub-agent 全新派发；只给路径（file-path-only handoff），不传内容。
- **派发方式**：native subagent（当前运行时支持 Agent 工具）；长任务用 scripts/dispatch.sh 外部派发时遵守 stream-json + .live.log/.jsonl/.status 三元组。

### Loop Card

| 环节 | 内容 |
|------|------|
| **WHEN** | 用户下发一个图表绘制任务（on-demand，无固定定时） |
| **SEE** | 先读 constraints.md + 预算 + STATE.md（最近结论/采纳记录）+ 技能当前版本 |
| **DO** | 一个 cycle = A0 语义建模 → A 并行语法实现 → B R1 三裁判 → C 技能工作副本优化 → D 并行重绘（每人一次）→ E R2 两裁判 → F 冠军/合并/记录 |
| **CHECK** | R2 加权分表（4 维权重 0.30/0.30/0.25/0.15）；冠军 = 最高分且 ≥0.85；技能采纳门 = 重绘 ≥ R1 自身分；冠军图存在且可渲染；SDS 覆盖检查通过 |
| **STOP** | 本轮完成即停；预算 80% → report-only、100% → halt；kill-switch `loop-pause-all`；任务无实质内容 → no-op 早退（<5k tokens） |
| **LEAVE** | run report（runs/<UTC>-report.md）+ STATE.md 更新 + run-log.jsonl 一行 + 结论账本追加 + 采纳的技能变更合并 canonical 并同步镜像 |
