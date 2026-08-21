---
name: 可视化技能竞技场团队
slug: viz-skill-arena
description: 四技能（draw-d3js / draw-echarts / draw-mermaid / draw-plantuml）同图竞技 + 两轮多裁判评审 + 一次重绘，持续区分「需求→技能」匹配并优化四个绘制技能
goal: >
  通过「用户下发图表任务 → 4 个技能并行绘制同一图表 → 第一轮 3 名裁判从不同角度打分 →
  根据评审意见优化对应技能（工作副本）并重绘 → 第二轮 2 名新裁判评审并选出冠军 →
  记录结论」的循环，逐步建立「需求类型 → 最优技能」的匹配知识（结论账本），
  并持续优化四个绘制技能（skills/draw-d3js、draw-echarts、draw-mermaid、draw-plantuml）。
  成功标准（每轮）：(1) 产出该任务冠军技能与匹配结论，追加至结论账本
  .specify/memory/knowledge/visualization-skill-selection.md；(2) 被采纳的技能变更
  （经第二轮独立裁判接受、无回退）合并回对应 canonical 技能目录并同步镜像；
  (3) 加权评分维度：语义保真 0.30 / 视觉质量 0.30 / 需求契合 0.25 / 可复现可维护 0.15，
  冠军 = 该轮最高加权分（≥0.85 采纳线）；技能变更采纳门 = 重绘后加权分 ≥ 第一轮自身分（无回退）。
goal_slug: visualization-skill-selection
territory:
  write:
    - skills/draw-d3js/**
    - skills/draw-echarts/**
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
    - { type: skill-invocation, target: 四个绘制技能的运行（渲染脚本执行、技能工作副本重载） }
pattern: continuous
preset: capability-arena   # 竞技模式实例(4 技能同题竞技);preset 由原 skills-arena 泛化而来
created: 2026-08-07
updated: 2026-08-20
members:
  - agent: agent-team-supervisor-template
    role: team-supervisor
    stage: meta
    type: Meta
    lifecycle: persistent
    responsibility: 唯一 Meta。读任务 → 并行派发 4 绘制者 → 派发 R1 三裁判 → 聚合反馈并把改进写入 4 个技能工作副本（target，不改被评图）→ 派发 4 重绘 → 派发 R2 两裁判 → 冠军裁定 → 采纳的技能变更合并回 canonical + 镜像同步 → 追加结论账本 → 写 run report / STATE / run-log
  - agent: agent-stage-executor-template
    role: drawer-d3js
    stage: executor
    type: Worker
    lifecycle: temporary
    responsibility: 加载 skills/draw-d3js 最新工作副本，用 draw-d3js 技能渲染任务图；R1 后重载更新后的技能重绘一次；产出图与结果清单到 run workspace
  - agent: agent-stage-executor-template
    role: drawer-echarts
    stage: executor
    type: Worker
    lifecycle: temporary
    responsibility: 同上（skills/draw-echarts）
  - agent: agent-stage-executor-template
    role: drawer-mermaid
    stage: executor
    type: Worker
    lifecycle: temporary
    responsibility: 同上（skills/draw-mermaid，render-mermaid.sh）
  - agent: agent-stage-executor-template
    role: drawer-plantuml
    stage: executor
    type: Worker
    lifecycle: temporary
    responsibility: 同上（skills/draw-plantuml，render-plantuml.sh）
  - agent: agent-stage-evaluator-template
    role: judge-r1-technical
    stage: evaluator
    type: Worker
    lifecycle: temporary
    responsibility: 第一轮裁判·技术角度——语义正确性/信息保真/渲染成功（按 4 维打分，输出 [DIM]_SCORE/WEIGHTED_TOTAL/SUGGESTIONS）
  - agent: agent-stage-evaluator-template
    role: judge-r1-visual
    stage: evaluator
    type: Worker
    lifecycle: temporary
    responsibility: 第一轮裁判·视觉角度——美观/排版/对齐/配色/清晰度
  - agent: agent-stage-evaluator-template
    role: judge-r1-semantic
    stage: evaluator
    type: Worker
    lifecycle: temporary
    responsibility: 第一轮裁判·需求角度——需求契合度/表达适切性/信息组织
  - agent: agent-stage-evaluator-template
    role: judge-r2-quality
    stage: evaluator
    type: Worker
    lifecycle: temporary
    responsibility: 第二轮裁判（与 R1 不同成员）·综合质量——对重绘后 4 图按同一 4 维加权打分，裁定冠军
  - agent: agent-stage-evaluator-template
    role: judge-r2-match
    stage: evaluator
    type: Worker
    lifecycle: temporary
    responsibility: 第二轮裁判·匹配裁定——确认冠军、复核无回退门、给出「需求类型→技能」匹配结论草稿（供 supervisor 写入账本）
config:
  maturity: L2                 # 用户明确要求循环内修改技能（重绘=改技能工作副本+重绘）；独立验证 = R2 裁判组（独立 sub-agent，默认 REJECT）
  cadence: on-demand           # 用户下发图表任务即触发一个 cycle（非定时）
  verifier: independent
  max_attempts_per_item: 1     # 每位绘制者恰好一次重绘（用户规则）
  quality_dimensions:
    - name: semantic-fidelity  # 语义正确/信息保真
      weight: 0.30
    - name: visual-quality     # 视觉美观/排版清晰
      weight: 0.30
    - name: requirement-fit    # 需求契合/表达适切
      weight: 0.25
    - name: reproducibility    # 可复现/可维护（源文件清晰、可重渲）
      weight: 0.15
  threshold: 0.85              # 冠军采纳线（R2 加权分）
  no_regression: true          # 技能变更采纳门：重绘后加权分 ≥ R1 自身分
  co_targets:
    - skills/draw-d3js
    - skills/draw-echarts
    - skills/draw-mermaid
    - skills/draw-plantuml
  layering: 每个技能目录（SKILL.md + references/ + scripts/）只归对应技能的变更；「需求→技能匹配」结论归结论账本 .specify/memory/knowledge/visualization-skill-selection.md；被评图与运行中间件只进 .specify/teams/.work/viz-skill-arena/
  conclusion_ledger: .specify/memory/knowledge/visualization-skill-selection.md
  deliverables_dir: .specify/teams/.work/viz-skill-arena/   # 每轮冠军图默认交付路径（git-ignored，单轮任务可覆盖）
  budget:
    max_cycles_per_day: 3
    max_tokens_per_day: 200000
    max_subagents_per_cycle: 12
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

**目标**：通过「四技能同图竞技 + 两轮多裁判评审 + 一次重绘」的循环，逐步建立「需求类型 → 最优绘制技能」的匹配知识，并持续优化四个绘制技能（draw-d3js / draw-echarts / draw-mermaid / draw-plantuml）。

**成功标准（每轮 cycle）**：
1. 冠军裁定：第二轮裁判按加权维度（语义保真 0.30 / 视觉质量 0.30 / 需求契合 0.25 / 可复现可维护 0.15）打分，最高加权分且 ≥0.85 者为冠军；
2. 结论记录：冠军 + 「该任务类型 → 推荐技能」匹配结论追加至 `.specify/memory/knowledge/visualization-skill-selection.md`（结论账本，跨轮累积）；
3. 技能优化：R1 评审意见 → supervisor 将改进写入对应技能**工作副本**（target）→ 绘制者重载后重绘 → R2 接受（重绘分 ≥ R1 自身分，无回退）→ 变更合并回 canonical `skills/draw-*/` 并同步 `.specify/skills/` 与 `.qoder/skills/` 副本；
4. 每轮产出 run report（`.specify/teams/viz-skill-arena/runs/`）+ STATE.md 更新 + run-log 一行。

## Static Structure

| Agent | Role | Stage | Type | Lifecycle |
|-------|------|-------|------|-----------|
| agent-team-supervisor-template | team-supervisor | meta | **Meta**（唯一；写技能定义/配置/账本） | persistent |
| agent-stage-executor-template | drawer-d3js | executor | Worker（渲染业务产物=图） | temporary |
| agent-stage-executor-template | drawer-echarts | executor | Worker | temporary |
| agent-stage-executor-template | drawer-mermaid | executor | Worker | temporary |
| agent-stage-executor-template | drawer-plantuml | executor | Worker | temporary |
| agent-stage-evaluator-template | judge-r1-technical | evaluator | Worker（评分对象=渲染出的图） | temporary |
| agent-stage-evaluator-template | judge-r1-visual | evaluator | Worker | temporary |
| agent-stage-evaluator-template | judge-r1-semantic | evaluator | Worker | temporary |
| agent-stage-evaluator-template | judge-r2-quality | evaluator | Worker | temporary |
| agent-stage-evaluator-template | judge-r2-match | evaluator | Worker | temporary |

Type 判定说明：裁判评分对象是渲染出的图表（业务产物）→ Worker；唯一 Meta 是 Team Supervisor（它写技能定义与团队/目标配置）。绘制者只调用技能渲染、不写技能定义 → Worker。

## Dynamic Structure

**Pattern**：continuous（长期运营）。优先级：长期改进（需求-技能匹配知识 + 四技能质量），用户每下发一个图表任务 = 一个 cycle；cycle 内部是「并行绘制 → 并行评审 → 定向重绘 → 独立复审」的锦标赛结构。

**Per-cycle 执行流**：

```
用户下发图表任务 T（含目标路径）
  │
  ▼
SUPERVISOR: 读 constraints.md + 预算 + STATE.md 最近结论；确定任务目标路径
  │
  ▼ PHASE A — 并行绘制（4 个 drawer 同时派发，territory 无写重叠）
  drawer-d3js / drawer-echarts / drawer-mermaid / drawer-plantuml
  各加载最新技能工作副本 → 渲染同一任务 T → 结果清单（图路径/成败）→ run workspace
  │
  ▼ PHASE B — 第一轮评审（3 名裁判并行，不同角度）
  judge-r1-technical / judge-r1-visual / judge-r1-semantic
  对 4 张图按 4 维加权打分 + 每技能 SUGGESTIONS
  │
  ▼ PHASE C — 技能优化（score = f(target) 不变式）
  SUPERVISOR 聚合 R1 反馈 → 将改进写入 4 个技能**工作副本**（只改 target，不手改被评图）
  │
  ▼ PHASE D — 重绘（4 个 drawer 再次并行，每人恰好一次）
  重载更新后的技能 → 重绘任务 T → 结果清单
  │
  ▼ PHASE E — 第二轮评审（2 名新裁判并行，独立验证，默认 REJECT）
  judge-r2-quality（综合加权打分）+ judge-r2-match（冠军裁定 + 无回退复核 + 匹配结论草稿）
  │
  ▼ PHASE F — 收尾（supervisor 独占写）
  冠军宣布 → 被采纳技能变更合并回 canonical + sync-mirrors.py --write + .qoder 副本
  → 结论账本追加（需求类型→技能 + 理由 + 本轮技能改动摘要）
  → run report + STATE.md 更新 + run-log 一行
```

**关键机制**：
- **score = f(target) 不变式**：每轮优化的对象是技能（target 工作副本），被评图由「最新 target 重生成」——绝不手改被评图；采纳的最优 target 落真实路径为标准输出。
- **独立验证**：R2 裁判是与 R1 完全不同的 sub-agent，默认 REJECT；无回退门（重绘分 ≥ R1 自身分）未过 → 该技能变更不合并。
- **上下文隔离**：每个 sub-agent 全新派发；只给路径（file-path-only handoff），不传内容。
- **派发方式**：native subagent（当前运行时支持 Agent 工具）；长任务用 scripts/dispatch.sh 外部派发时遵守 stream-json + .live.log/.jsonl/.status 三元组。

### Loop Card

| 环节 | 内容 |
|------|------|
| **WHEN** | 用户下发一个图表绘制任务（on-demand，无固定定时） |
| **SEE** | 先读 constraints.md + 预算 + STATE.md（最近结论/采纳记录）+ 技能当前版本 |
| **DO** | 一个 cycle = A 并行绘制 → B R1 三裁判 → C 技能工作副本优化 → D 并行重绘（每人一次）→ E R2 两裁判 → F 冠军/合并/记录 |
| **CHECK** | R2 加权分表（4 维权重 0.30/0.30/0.25/0.15）；冠军 = 最高分且 ≥0.85；技能采纳门 = 重绘 ≥ R1 自身分；冠军图存在且可渲染 |
| **STOP** | 本轮完成即停；预算 80% → report-only、100% → halt；kill-switch `loop-pause-all`；任务无实质内容 → no-op 早退（<5k tokens） |
| **LEAVE** | run report（runs/<UTC>-report.md）+ STATE.md 更新 + run-log.jsonl 一行 + 结论账本追加 + 采纳的技能变更合并 canonical 并同步镜像 |
