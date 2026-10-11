---
name: 技能分层与安装分流团队
slug: skill-layer-install-separation
description: 以 serial 五阶段链（S-A 技能对去 .specify 化 → S-B 源树重家与引用适配 → S-C 镜像/安装/打包工具链分流 → S-D 测试适配与守卫 → S-E 运行时刷新与终验）把「internal/external 分层 + 安装/可见性分流」从设计落到全绿；每阶段内多个 **native subagent 并发派发**（一响应块多调用、同席位多重 Execution），每次交接有独立验证门
goal: >
  承接已定义 Goal `skill-layer-install-separation`（权威定义：.specify/goal/skill-layer-install-separation/goal.md）。
  本字段仅为可读性渲染，与定义不一致时以定义为准。终态：技能源树按 internal/external 两层组织且全仓引用一致；
  客户项目只获得并注册 external 技能（internal 以 .specify/skills/internal/ 嵌套下发、对客户 agent 不可见、
  仅供 /speckit.* 工作流按显式路径消费）；框架自身两态齐备，镜像、安装、打包与测试工具链整链适配。
  **成功判据以定义为准，本团队不复述其文本**（定义持有 2 条）。
goal_slug: skill-layer-install-separation
territory:
  write:
    - skills/**                    # 技能源树（B2c 技能对改写 + 后续重家）；draw-mermaid server 子树为 vendored 面、不视为技能契约面
    - templates/**                 # 命令模板/指令模板/技能引导模板等（定义类文件经 Meta 落盘）
    - scripts/python/**            # 工具链引擎（B3 sync-mirrors 层映射等；承接旧团队「不改引擎」收窄的解除——本目标以引擎改动为主体之一）
    - src/specify_cli/**           # B4 安装/升级两层映射与迁移；经 in-tree 模块验证
    - src/hatch_build.py           # B5 打包暂存适配
    - pyproject.toml               # 仅在打包清单确实需要时
    - tests/**                     # B6 测试适配与守卫测试
    - docs/**                      # 文档空间（.speckit 机器区、reference 页；docs/public 构建产物不直改）
    - shared/**                    # 框架 shared（定义/工作流文档的引用面）
    - .specify/skills/**           # 仅由 sync-mirrors.py 再生成写入；MUST NOT 手改
    - .specify/shared/**           # 同上（受控投影）
    - .specify/templates/**        # 同上
    - .specify/instructions.md     # 经既有生成脚本同步指针面；结构性再生仍走 /speckit.instructions
    - .claude/commands/**          # 四副本树仅由 regen-command-copies.py 写入；MUST NOT 手改
    - .github/prompts/**
    - .qoder/commands/**
    - .opencode/command/**
    - .specify/teams/skill-layer-install-separation/**   # 团队自身 run 信息
    - .specify/memory/feedback/**  # 反馈条目
    - .specify/memory/glossary.md  # 条目级最小更新
    - .specify/memory/register.md  # 编号登记追加（指针行）
  read:
    - .specify/goal/skill-layer-install-separation/**
    - .specify/shared/**
    - skills/**
    - scripts/**
    - src/**
    - tests/**
    - docs/**
  forbidden:
    - .specify/goal/**             # authored：只经 /speckit.goal 引擎渲染
    - skills/self-improvement/**   # 归 session-driven-self-improvement 团队（其 goal 已终态）。分层迁移面（重家/rename + 路径形态引用适配，零内容语义改动）经 2026-10-09 modify 裁定纳入本团队授权——S-B 交付后由 verifier G1 检出、事后裁定并披露（条款自带 remedy 的履行）；内容级改动仍需先经 /speckit.team modify 裁定
    - templates/commands/improve.md  # 同上归属与同一迁移面裁定（S-B B1 已交付路径形态适配）
    - .qoder/agents/**             # 宿主 agent 注册面：仅由 `render-agents` 渲染器写；禁手改
    - .qoder/skills/**             # 与 .specify/skills 的同源符号链接面
    - .qoder/settings.local.json
    - .github/skills               # 符号链接
    - AGENTS.md, CLAUDE.md, QODER.md, .github/copilot-instructions.md   # 兼容符号链接，经 /speckit.instructions 再生
    - .specify/memory/feedback/probe-map.md   # 派生物：由 feedback-utils.py --action map 重建，禁手编
  non_path:
    - { type: dispatch-modality, target: 并发是硬要求（用户 2026-10-09 指令「team 需要进行多 subagent 协作，并发处理」）：framework-engineer / structure-adjuster / skill-verifier 三席均已安装到宿主注册面（.qoder/agents/），MUST 以 **native** 派发；阶段内独立单元 MUST 在**同一响应块内并发派发**（多调用）；同一席位的多重 Execution 并发合法（各自独立 territory）。virtual 仅作宿主不可用时的降级并须披露。supervisor 由编排会话承担（virtual 角色、不发任务给自身） }
    - { type: write-authority, target: 消解条款（skills/create-team/references/conceptual-model.md §消解条款）在本团队的落法：业务路径（engines/CLI/tests/docs）由 Worker 在 territory 内**直写**；**定义类文件**（SKILL.md / team.md / agent 定义 / 命令模板）由 Worker 产出**工作区补丁**、MUST 由唯一 Meta supervisor 落 canonical。违反即越权 }
    - { type: handover, target: 本团队承接旧团队 command-logic-as-classified-skills 的「run-2 扩展切片」剩余批次 B2c/B2e/B3/B4/B5/B6/B7（用户 2026-10-09 指令转换为新 goal+team）。已完成批次 B1/B2a/B2b/B2d 的产线与记录留在旧团队；旧团队保留 S1–S3（其 S1 起点依赖本团队 S-B 落地，跨团队交接以旧团队 progress 为准） }
    - { type: ceiling, target: 门控预算——`python3 .specify/scripts/python/scan-confirmation-gates.py` 的 total MUST 保持 ≤ 23（as-of 2026-10-09 实测 23；不写字面量当常量，以重跑命令为准）。易变测量值（技能数、测试数）一律以可重跑命令 + as-of 基线表达 }
    - { type: regeneration, target: canonical 落盘（含本团队任一业务路径写入）后 MUST 依序跑两再生成引擎并 `--check` 退出 0：`scripts/python/sync-mirrors.py` 与 `scripts/python/regen-command-copies.py`（自 canonical 副本调用）；镜像不删旧投影——退役/改名条目按「回收操作」手工清除并在报告披露（缺口已记入 feedback 20261009T064957Z） }
    - { type: checkpoint, target: 起步状态（2026-10-09 移交时）：树全绿（两引擎 --check 0、门控 23、docs/sanitize 套件 99P、宽子集 703P、关联子集 305P）；B2b 批次未提交（40 项），提交时点由用户定 }
pattern: serial
created: 2026-10-09
updated: 2026-10-09
members:
  - agent: agent-team-supervisor-template
    role: team-supervisor
    stage: meta
    type: Meta
    lifecycle: temporary                 # 只解析为 skills/create-team/templates/agents/ 下的临时模板；由编排会话承担
    responsibility: 唯一 Meta 与 Lead：读 goal 判据 + progress 文件 → 按拓扑序派发阶段；阶段内把独立单元**并发派发**给 native 席位（一响应块多调用）→ 消费 skill-verifier 的判定表跑交接验证门 → **唯一有权把定义类补丁落到 canonical**（业务路径 Worker 直写）→ 每次 canonical 落盘/收批后依 config.regeneration 跑再生成并核实 --check 0 → 每阶段收尾跑门控扫描与测试子集 → 写 run report / progress；**永不亲自执行单位任务**
    blockedBy: []
  - agent: framework-engineer
    role: framework-engineer
    stage: executor
    type: Worker
    lifecycle: temporary                 # 席位生命周期为单次运行；其**容量定义**持久于 .specify/agents/instances/framework-engineer.agent.md（已渲染至 .qoder/agents/）
    responsibility: 单位执行者（可并发多重 Execution）：技能包改写补丁、引擎/CLI/打包代码、测试适配、引用面批量改写——均限派发 territory 内；定义类文件只产补丁
    blockedBy: []
  - agent: structure-adjuster
    role: structure-aligner
    stage: executor
    type: Worker
    lifecycle: temporary                 # 容量定义持久于 .specify/agents/templates/structure-adjuster.agent.md
    responsibility: S-B 重家手术：git mv 批量归位（32 实体 → skills/{internal,external}/）、布局校验、镜像/副本面查漏；业务路径直写、不产定义类补丁
    blockedBy: [framework-engineer]
  - agent: skill-verifier
    role: contract-checker
    stage: evaluator
    type: Meta
    lifecycle: temporary                 # 容量定义持久于 .specify/agents/templates/skill-verifier.agent.md（已渲染至 .qoder/agents/）
    responsibility: 每次交接的独立判定席（默认 REJECT）：跑/审本阶段证据（命令实跑、路径可解析、守卫测试红绿演练），出逐项判定表；判定 MUST 附实读证据（路径 + 具体事实）；只写判定报告到工作区，不落 canonical
    blockedBy: [framework-engineer]
config:
  handoff_protocol: file-path-only
  progress_file: .specify/teams/.work/skill-layer-install-separation/progress.md
  failure_strategy: retry-once-then-escalate
  verification: independent
  dispatch: native-concurrent            # 阶段内并发（一响应块多调用）；同席位多重 Execution 合法
  progression: T-001 → T-002 → T-003 → T-004
  target_map:
    T-001: [S-A-skill-pair-decouple]
    T-002: [S-B-rehome-and-refs]
    T-003: [S-C-toolchain-split]
    T-004: [S-D-tests-and-guards, S-E-runtime-refresh]
  regeneration: >
    每次 canonical 落盘后由 supervisor 依序执行（并核实 --check 退出 0）：
    ① `python3 scripts/python/sync-mirrors.py`；② `python3 scripts/python/regen-command-copies.py`。
    镜像不删旧投影：退役/改名条目手工回收 + 披露。MUST 自 canonical 副本调用。
  invariants: >
    每个 stage 的 quality_gate MUST 复核：① 门控扫描 total ≤ 23；② 补丁不触碰 territory.forbidden；
    ③ 有 canonical 落盘者，两再生成引擎已跑且 --check 0；④ 并发单元的 territory 两两不相交（派发载荷逐单元声明）。
summary:
    enabled: true
    every: 1
    delivery_dir: .specify/goal/skill-layer-install-separation/summary/
    interactive: false
---

## Goal

**权威定义**：`.specify/goal/skill-layer-install-separation/goal.md`（`goal_slug` 引用，非内容副本）。终态与判据以定义为准；本文件不复述判据文本。判据覆盖缺口的如实记账：目标判据 2 条覆盖双布局一致与分流可验证两面；各 stage 级 `quality_gate` 承担其余面（如技能对解耦的如实性、测试同口径 A/B），与 goal 级判据权威层级不同，MUST NOT 混称。

## Static Structure

| Agent | Role | Stage | Type | Lifecycle | 派发模态 | 写面（显式） |
|-------|------|-------|------|-----------|----------|--------------|
| `agent-team-supervisor-template` | team-supervisor | meta | **Meta** | temporary | virtual（编排会话承担） | canonical 定义类落盘、两引擎输出、团队目录、progress、report |
| `framework-engineer` | framework-engineer | executor | Worker | temporary（容量持久） | **native（并发）** | territory 内业务路径直写；定义类仅工作区补丁 |
| `structure-adjuster` | structure-aligner | executor | Worker | temporary（容量持久） | **native** | territory 内业务路径直写（重家手术） |
| `skill-verifier` | contract-checker | evaluator | **Meta** | temporary（容量持久） | **native** | 仅工作区（判定报告） |

**并发设计（本团队的硬要求）**：阶段内的独立单元 MUST 并发派发——同一响应块内多个 Agent 调用，各自携带独立 task_brief + territory + fast-fail 注入子句；同席位（framework-engineer）的多重 Execution 并发合法。territory 逐单元声明且两两不相交（写面互斥）；交接点串行收敛。

## Dynamic Structure

**Pattern**：serial（质量优先）。选择依据：五阶段强依赖（S-B 消费 S-A 产物、S-C 消费 S-B 布局、S-D 消费 S-C 引擎、S-E 收口），DAG `S-A → S-B → S-C → S-D → S-E`；并发性体现在**阶段内单元级**（见上），不改变链式的质量优先语义。

**Workflow**：

```json
{
  "workflow_id": "skill-layer-install-separation-chain",
  "name": "技能分层与安装分流链",
  "stages": [
    {
      "stage_id": "S-A-skill-pair-decouple",
      "agent_kind": "framework-engineer",
      "target_ref": "T-001",
      "task": "create-skills 与 improve-skills 去 .specify 化（承旧团队 B2c）：以通用 skills 根为主形态、`.specify/skills` 降为可选集成；含 11 个 references 与 2 个 scripts 的适配；「Skill Enablement 传播步」保留为可选集成（用户未改判时的默认）——单元 A1=create-skills、A2=improve-skills，两单元并发派发（文件面互斥），共享引用由 supervisor 收尾。",
      "inputs_from": [],
      "outputs": [".specify/teams/.work/skill-layer-install-separation/S-A/"],
      "blockedBy": [],
      "quality_gate": "① 两技能 SKILL.md 各自：通用根为主、.specify 出现次数全部为可选/降级语境（逐处列出）；② 11 references 与 2 scripts 引用面无悬挂；③ sync/regen 两引擎 --check 0；④ 门控 ≤ 23；⑤ 不含 forbidden 改动"
    },
    {
      "stage_id": "S-B-rehome-and-refs",
      "agent_kind": "structure-adjuster",
      "target_ref": "T-002",
      "task": "源树重家与引用适配（承 B2e）：structure-adjuster 先跑重家手术（32 实体 → skills/{internal,external}/，git mv + 布局校验）；随后 framework-engineer 三地形**并发**适配引用面：B1=命令树（templates/commands + 四副本经 regen）、B2=技能自引与互引、B3=docs/instructions/其他文档面；内部技能「按名引用 → 按路径引用」清单闭合（.specify/skills/internal/<name>/…）。",
      "inputs_from": ["S-A-skill-pair-decouple"],
      "outputs": [".specify/teams/.work/skill-layer-install-separation/S-B/"],
      "blockedBy": ["S-A-skill-pair-decouple"],
      "quality_gate": "① 32 实体在两层齐全且无重复（find 计数 = 32）；② 全仓无指向旧平铺源的悬挂引用（grep 复核）；③ 内部技能按名引用清单归零或全部具名说明；④ 两引擎 --check 0；⑤ 门控 ≤ 23；⑥ 不含 forbidden 改动"
    },
    {
      "stage_id": "S-C-toolchain-split",
      "agent_kind": "framework-engineer",
      "target_ref": "T-003",
      "task": "工具链分流（承 B3/B4/B5）：三单元**并发**——C1=sync-mirrors 层映射（两源层 → 运行时 external 平铺/internal 嵌套）+ 自用镜像重建；C2=CLI `copy_local_templates` 两源层复制 + 升级迁移清理（平铺 internal → 内嵌；不触用户自建技能）+ 相关 CLI 测试；C3=hatch_build 暂存 + rewrite_paths 两分支。文件面：scripts/python/sync-mirrors.py ∥ src/specify_cli/__init__.py ∥ src/hatch_build.py（互斥）。",
      "inputs_from": ["S-B-rehome-and-refs"],
      "outputs": [".specify/teams/.work/skill-layer-install-separation/S-C/"],
      "blockedBy": ["S-B-rehome-and-refs"],
      "quality_gate": "① 运行时镜像呈两布局且 sync --check 0；② 模拟客户安装的迁移测试（平铺 internal → 内嵌）通过；③ rewrite 两分支单测过；④ 门控 ≤ 23；⑤ 不含 forbidden 改动"
    },
    {
      "stage_id": "S-D-tests-and-guards",
      "agent_kind": "framework-engineer",
      "target_ref": "T-004",
      "task": "测试适配与守卫（承 B6）：D1/D2/D3=测试面按三组目录**并发**适配（167 引用面）；D4=两条守卫测试原创：平铺发现面只注册 external（internal 不可见）、internal 路径可解析；收官跑全量测试同口径 A/B（--names-out 名字级差集）。",
      "inputs_from": ["S-C-toolchain-split"],
      "outputs": [".specify/teams/.work/skill-layer-install-separation/S-D/"],
      "blockedBy": ["S-C-toolchain-split"],
      "quality_gate": "① 守卫测试两条在场且做过红绿演练（红先行证据）；② 全量 A/B 差集逐项归因、零新增；③ 门控 ≤ 23；④ 不含 forbidden 改动"
    },
    {
      "stage_id": "S-E-runtime-refresh",
      "agent_kind": "framework-engineer",
      "target_ref": "T-004",
      "task": "自用运行时刷新与终验（承 B7）：镜像重建（两布局）+ skill-verifier 独立终验（跑 goal 判据 2 条的可验证面：平铺发现面、internal 路径解析、三引擎 --check、门控）+ 报告。",
      "inputs_from": ["S-D-tests-and-guards"],
      "outputs": [".specify/teams/.work/skill-layer-install-separation/S-E/"],
      "blockedBy": ["S-D-tests-and-guards"],
      "quality_gate": "① 终验判定表全 PASS（附实读证据）；② 本仓 .specify/skills 呈两状态；③ goal 判据 2 条逐条落到可复算证据"
    }
  ],
  "handoff_protocol": "file-path-only",
  "progress_file": ".specify/teams/.work/skill-layer-install-separation/progress.md"
}
```

**DAG（无环）**：`S-A → S-B → S-C → S-D → S-E`；阶段内单元并发（响应块级并行），交接串行。

**并发纪律**：派发单元的 payload 逐单元声明 {task_brief, territory(write 互斥), forbidden, outputs, incremental_landing, fast_fail_clause}；任一单元触碰他单元 territory 即判越权；完成以工作区产物 + 回传异常行为准。

**跨团队交接**：本团队 S-B 完成后，旧团队 command-logic-as-classified-skills 的 S1（新技能直落分层树）方可启动；交接时旧团队读本团队 progress + run report。

**失败策略**：retry-once-then-escalate（每单元一次重试，仍败即上送用户）；MUST NOT 用 retry 承载单元累积。

**Summary 刷新**：每阶段交接验证通过后刷新一次（`every: 1`）→ `.specify/goal/skill-layer-install-separation/summary/`；门控顺序与状态行口径由 `skills/create-team/SKILL.md` §Summary Refresh 持有。

## Self-Improvement Contract

- Subject: this persisted team definition; member executions are evidence.
- Observe: completed run reports and Post-Run Critique.
- Improve: follow `.specify/shared/workflow/self-improvement-workflow.md`; route through `improve-team`.
- Boundary: preserve team authority, dispatch-concurrency mandate, budget, kill-switch, and verifier independence.
- Verify: validate now and wait for a comparable later run before claiming improvement.
