---
name: 命令逻辑技能化与分类标注团队
slug: command-logic-as-classified-skills
description: 以 serial 五阶段链（命令普查裁定 → 提炼建技能并标注 → 契约齐备 → 结构对齐 → 命令瘦身）把 25 个命令模板的核心逻辑下沉为技能，并给每个技能打 internal / external 标注；每次交接有独立验证门
goal: >
  承接已定义 Goal `command-logic-as-classified-skills`（权威定义：.specify/goal/command-logic-as-classified-skills/goal.md）。
  本字段仅为可读性渲染，与定义不一致时以定义为准。终态：spec-kit 的命令核心逻辑尽可能由技能承载——
  命令模板只保留入口与委派，可执行的核心逻辑落在 skills/ 下的技能里；每个技能的元数据都带 internal 或
  external 标注，标注如实表达它与 spec-kit 的依赖关系（internal 只服务框架自身逻辑、external 与 spec-kit
  无依赖任何项目皆可直接使用），使后续按标注分流的处理有据可依。判据（定义持有，此处不复写口径）：
  command 中只包含该调用哪些 skill 以及如何调用 skill，不含具体实现细节，所有细节都在 skill 中。
goal_slug: command-logic-as-classified-skills
territory:
  write:
    - templates/commands/*.md              # T-003 瘦身写面；受模板中立性约束（见 non_path）
    - skills/*/SKILL.md                    # T-001 标注字段 + T-002 名称/描述/触发定义
    - skills/*/references/**               # 命令实现细节下沉的目的地
    - skills/*/templates/**
    - skills/*/scripts/**
    - .specify/teams/command-logic-as-classified-skills/**   # 团队自身 run 信息
    - .specify/memory/feedback/**          # 反馈条目
  read:
    - .specify/goal/command-logic-as-classified-skills/**
    - .specify/shared/**
    - .specify/memory/glossary.md
    - .specify/skills/**                   # 生成镜像，只读比对，不手改
    - templates/**
    - skills/**
    - docs/reference/commands/**
    - scripts/python/**
  forbidden:
    - .specify/skills/**                   # 镜像由安装/再生成同步，手改会被覆盖（两顶帽子）
    - .specify/goal/command-logic-as-classified-skills/goal.md   # authored：只经 /speckit.goal 引擎渲染
    - templates/constitution-template.md   # 模板中立性 + 不在本目标范围
    - templates/skills-template.md
    - templates/agents/**
    - templates/commands/improve.md        # 跨 goal 写权裁定 2026-10-06（用户明示授权本次修改）：该文件归 session-driven-self-improvement 团队 S4；本团队 T-003 命令瘦身扫 templates/commands/*.md 时 MUST 跳过它，其薄壳形态已在对方 S4 responsibility 中按本团队 T-003 约定预对齐
    - skills/draw-mermaid/server/**        # vendored（13232 文件），非技能契约面
    - scripts/**                           # 引擎：本目标不改引擎
    - .specify/scripts/**
    - .specify/memory/feedback/probe-map.md   # 派生物：由 feedback-utils.py --action map 重建，禁手编
    - .qoder/**                            # 兼容层：经 /speckit.instructions 再生
    - AGENTS.md
    - CLAUDE.md
    - QODER.md
    - .github/copilot-instructions.md
  non_path:
    - { type: framework-convention, target: 命令=编排、技能=实现的职责边界；瘦身后的命令模板 MUST NOT 嵌入本仓专属内容（模板中立性，真源 docs/reference/history/00-cross-cutting-lessons.md:124） }
    - { type: ceiling, target: 确认门控预算——scan-confirmation-gates.py 的 total MUST 保持 ≤ 23（as-of 2026-10-06 实测 23，余量 0）；本团队写面全在 SCAN_DIRS 内，任何新增 BLOCKING_PATTERNS 命中会同时打爆两个契约测试 }
    - { type: classification, target: internal / external 只是标识、不对外呈现；与需求 039「通用技能=宿主中立」不同义（真源 .specify/memory/glossary.md 技能分类标注条） }
    - { type: progression, target: T-001 → T-002 → T-003 的递进序由本团队计划承载；goal 层的 Target 集无序、无依赖边，顺序在那里没有落点 }
pattern: serial
created: 2026-10-06
updated: 2026-10-06
members:
  - agent: agent-team-supervisor-template
    role: team-supervisor
    stage: meta
    type: Meta
    lifecycle: temporary                 # 该 agent 只解析为 skills/create-team/templates/agents/ 下的临时模板；.specify/agents/{templates,instances}/ 无此持久定义，标 persistent 即断引用
    responsibility: serial Lead 与唯一 Meta。读 goal.md 判据 + progress 文件 → 按拓扑序派发五个 stage → 每次交接消费 contract-checker 的判定表跑轻量验证门 → **唯一有权把 Worker 补丁落到 canonical skills/ 与 templates/commands/**（交付物是技能定义，故 Worker MUST NOT 直写 canonical，依据 conceptual-model.md §消解条款）→ 每 stage 收尾跑门控扫描与契约测试 → 写 run report / progress 文件 / summary 输入，并把本次 run 的 items.jsonl 条目打上 target_ref
    blockedBy: []
  - agent: agent-stage-executor-template
    role: skill-author
    stage: executor
    type: Worker
    lifecycle: temporary
    responsibility: S0/S1/S2a/S3 的产出者。按 stage 派发：裁定命令核心逻辑的去向、把逻辑提炼为技能包草稿并写入 internal / external 标注、补齐名称/描述/触发定义、把命令模板瘦身为「调用哪些技能 + 各自输入与产出」。**只写运行工作区补丁** .specify/teams/.work/command-logic-as-classified-skills/，MUST NOT 直写 canonical 路径
    blockedBy: []
  - agent: structure-adjuster
    role: structure-aligner
    stage: executor
    type: Worker
    lifecycle: temporary
    responsibility: S2b 结构对齐——逐技能判定 internal 技能与 .specify 目录结构的配合是否成立、external 技能是否对 .specify 零依赖（含只读比对 .specify/skills/ 镜像与 skills/ 源的对应关系），产出对齐补丁到工作区；不直接写 canonical
    blockedBy: [skill-author]
  - agent: agent-stage-evaluator-template
    role: contract-checker
    stage: evaluator
    type: Meta
    lifecycle: temporary
    responsibility: 每次交接的独立判定席（与 skill-author 不同席、不同会话，默认 REJECT 立场）。以 goal 判据原文与 T-002 质量条为口径出**逐条目判定表**；整批（wholesale）判定 MUST 附 ≥2 个实读文件的证据（路径 + 从该文件读到的具体事实），MUST NOT 以产物条目数或子代理自述充当覆盖度（substance floor，真源 patterns.md §Serial Chain）。Type 判为 Meta 的依据是其操作对象为技能定义本身（conceptual-model.md §Type criterion 明列 skills）；但它**只写判定报告到工作区**，不落 canonical——落盘权归 team-supervisor
    blockedBy: [skill-author]
config:
  handoff_protocol: file-path-only
  progress_file: .specify/teams/.work/command-logic-as-classified-skills/progress.md
  failure_strategy: retry-once-then-escalate
  verification: independent
  progression: T-001 → T-002 → T-003
  target_map:
    T-001: [S0-command-census, S1-extract-annotate]
    T-002: [S2a-contract-conformance, S2b-structure-alignment]
    T-003: [S3-command-thinning]
  invariants: >
    每个 stage 的 quality_gate MUST 复核两条不变量，二者都是程序可判定：
    ① 门控预算——`python3 .specify/scripts/python/scan-confirmation-gates.py` 的 total ≤ 23
    （as-of 2026-10-06 基线 23，余量 0；不写字面量当常量，以重跑命令为准）；
    ② 补丁不触碰 territory.forbidden 的任何路径。
    易变测量值（技能数、命令数）MUST NOT 以字面量写死为判据，一律以可重跑命令 + as-of 基线表达。
  summary:
    enabled: true
    every: 1                             # bounded pattern 默认每阶段边界刷新一次
    delivery_dir: .specify/goal/command-logic-as-classified-skills/summary/
    interactive: false
---

## Goal

**权威定义**：`.specify/goal/command-logic-as-classified-skills/goal.md`（`goal_slug` 引用，非内容副本）。以下为本团队视角的渲染，与定义冲突时以定义为准。

- **终态**：命令核心逻辑尽可能由技能承载；每个技能元数据带 internal / external 标注，标注如实表达它与 spec-kit 的依赖关系。
- **判据**：定义持有 1 条（command 只含调用哪些 skill 及如何调用，不含实现细节）。判据是 `achieved` 的唯一权威，本团队 MUST NOT 自行增补或复写口径。
- **覆盖缺口（分析所得，非门禁）**：该判据只覆盖 T-003 那一面；T-001 的「标注如实性」与 T-002 的「契约齐备性」在 goal 层没有判据。本团队以 stage 级 `quality_gate` 承担这两面的判定，并如实记录这是团队级判据、不是 goal 级判据——两者的权威层级不同，MUST NOT 混称。
- **范围外**：依据 internal / external 标注进行的任何差异化处理（定义的 `## Boundaries` 持有，用户明示留待后续）。

## Static Structure

Role × Stage × Type 矩阵。Type 依「操作对象」判定，不由 Stage 推出；写面逐席显式声明，不从 Type 推断。

| Agent | Role | Stage | Type | Lifecycle | 写面（显式） |
|-------|------|-------|------|-----------|--------------|
| `agent-team-supervisor-template` | team-supervisor | meta | **Meta** | temporary | canonical `skills/`、`templates/commands/`、团队目录、progress、run report、summary 输入 |
| `agent-stage-executor-template` | skill-author | executor | Worker | temporary | **仅** `.specify/teams/.work/command-logic-as-classified-skills/`（补丁） |
| `structure-adjuster` | structure-aligner | executor | Worker | temporary | **仅** 运行工作区（对齐补丁） |
| `agent-stage-evaluator-template` | contract-checker | evaluator | **Meta** | temporary | **仅** 运行工作区（判定报告）；Meta 身份允许改技能定义，但本席不落 canonical |

**为何必须有 Meta supervisor**：本团队交付物本身就是技能定义（`SKILL.md` 及其 references/templates/scripts），依 `conceptual-model.md` §消解条款，此时 Lead 席位不是可选质量门而是**必需的 Meta 落盘者**——Worker 只产补丁到工作区，由唯一 Meta 把它们落到 canonical 路径。

## Dynamic Structure

**Pattern**：serial（质量优先）。选择依据：决策树 Q1 对本目标的**主体工作**为否（25 个命令模板的技能化与瘦身是有界的一次性交付物改动，不是按 cadence 到达的流；「尽可能」这一长期性由 Goal lifecycle 承载——goal 长期 `active`、其下三条 Target 逐个关闭——不必由团队形态承载，真源 `patterns.md` §Q1 判据）；Q2 为否（各 stage 共享同一批可变状态：技能清单、`skills/` 与 `.specify/skills/` 的对应关系、标注词表）；**Q3 命中**（严格序列：S3 瘦身后的命令要引用的技能由 S1 产出，S2 的质量条施加于 S1 的产物）。

> **为何不是 continuous**：continuous 强制 L1 报告态起步且不可跳级，L1 的 `max_subagents_per_cycle: 0` 意味着晋级前改不了任何 `skills/` 文件，即做不了 S1。

**Workflow**：

```json
{
  "workflow_id": "command-logic-as-classified-skills-chain",
  "name": "命令逻辑技能化与分类标注链",
  "stages": [
    {
      "stage_id": "S0-command-census",
      "agent_kind": "skill-author",
      "target_ref": "T-001",
      "task": "命令普查与技能化裁定（纯 attribution，不含建技能）：对 templates/commands/ 下每个命令模板逐个裁定三件事——① 其核心逻辑是否应下沉为技能（判否的须给理由，如该命令本就是纯编排）；② 下沉到哪个技能（新建 / 并入既有，须点名既有技能目录）；③ 该技能属 internal 还是 external（口径见 .specify/memory/glossary.md 技能分类标注条）。产出裁定表，每行一个命令。**本 stage 由 N 次派发累积：N = `find templates/commands -name '*.md' | wc -l` ÷ 5 向上取整（as-of 2026-10-06 基线 25 ⇒ 5 批），每批 5 个命令、按文件名字母序切分，每批判完立即写盘。** 累积是设计，MUST NOT 用 retry 预算承载。",
      "inputs_from": [],
      "outputs": [".specify/teams/.work/command-logic-as-classified-skills/S0-census/ruling.md"],
      "blockedBy": [],
      "quality_gate": "① 裁定表行数 == 实扫命令数（重跑 `find templates/commands -name '*.md' | wc -l` 取分母，不用字面量）；② 每行三项裁定齐备，判「不下沉」的附理由；③ 每个已声明批次的命令名在产物中可检索（`grep -c`）；④ 整批判定附 ≥2 个实读文件证据；⑤ 不含对 territory.forbidden 的改动"
    },
    {
      "stage_id": "S1-extract-annotate",
      "agent_kind": "skill-author",
      "target_ref": "T-001",
      "task": "按 S0 裁定表把命令核心逻辑提炼为技能包草稿（SKILL.md + 必要 references/templates/scripts），并在每个技能的元数据里写入 internal / external 标注字段。已委派技能的 7 个命令只做增量补齐，不重复建技能。以 create-skills 的模板与约定为权威形态（Worker MUST NOT 直写 skills/，由 Meta 落地时经 create-skills 生成 canonical 骨架）。**本 stage 由 N 次派发累积：N = S0 裁定表中判「下沉且需新建」的行数（以裁定表为分母，不预设字面量；as-of 2026-10-06 的上界是 18 个尚未委派技能的命令），每批一个命令 → 一个技能包，每批完成立即写盘。**",
      "inputs_from": ["S0-command-census"],
      "outputs": [".specify/teams/.work/command-logic-as-classified-skills/S1-skills/"],
      "blockedBy": ["S0-command-census"],
      "quality_gate": "① 裁定表里每个判「下沉」的命令都有对应技能包草稿或指向既有技能的并入说明；② 每个新技能包 frontmatter 含 name / description / 标注字段三项，标注取值只允许 internal 或 external；③ 产物字节数 ≥ 由批规模推出的下限（桩文件不得通过）；④ 每个已声明技能名在产物中可检索；⑤ 门控扫描 total ≤ 23；⑥ 不含对 territory.forbidden 的改动"
    },
    {
      "stage_id": "S2a-contract-conformance",
      "agent_kind": "skill-author",
      "target_ref": "T-002",
      "task": "契约齐备性核查与修补（一种任务类型：逐技能契约 attribution，不含目录结构裁定——后者属 S2b，二者预算量级不同 MUST NOT 同 stage）：对 skills/ 下每个技能判定名称是否明确、描述是否说明「什么请求该用我」、触发定义是否可判定，缺项出补丁。范围含 S1 新建的技能。**本 stage 由 N 次派发累积：N = `find skills -name SKILL.md -not -path '*/server/*' | wc -l` ÷ 10 向上取整（as-of 2026-10-06 基线 34，另加 S1 新增数），每批 10 个技能，每批判完立即写盘。**",
      "inputs_from": ["S1-extract-annotate"],
      "outputs": [".specify/teams/.work/command-logic-as-classified-skills/S2a-contract/conformance.md"],
      "blockedBy": ["S1-extract-annotate"],
      "quality_gate": "① 逐技能判定表行数 == 实扫 SKILL.md 数（重跑命令取分母）；② 每行三项（名称/描述/触发定义）各有判定，判缺项的附补丁路径；③ 整批判定附 ≥2 个实读文件证据；④ 每个已声明批次内的技能名可检索；⑤ 不含对 territory.forbidden 的改动"
    },
    {
      "stage_id": "S2b-structure-alignment",
      "agent_kind": "structure-aligner",
      "target_ref": "T-002",
      "task": "结构对齐（一种任务类型：技能与 .specify 目录结构的依赖关系裁定）：逐技能判定——标为 internal 的技能是否确实配合 .specify 目录结构（其读写面落在 .specify/ 内且路径存在）；标为 external 的技能是否对 .specify 零依赖（其 SKILL.md 与 references 中不出现 .specify/ 路径依赖，或出现处均可降级为可选）。含只读比对 skills/ 源与 .specify/skills/ 镜像的对应关系（镜像本身禁写）。不符项出对齐补丁。",
      "inputs_from": ["S2a-contract-conformance"],
      "outputs": [".specify/teams/.work/command-logic-as-classified-skills/S2b-structure/alignment.md"],
      "blockedBy": ["S2a-contract-conformance"],
      "quality_gate": "① 逐技能有 internal/external 与 .specify 依赖关系的判定，判定附实际检索到的路径证据（`grep -c` 计数 + 至少两处实读引用）；② 每个判「不符」的技能有对齐补丁路径；③ 整批判定附 ≥2 个实读文件证据；④ 未写入 .specify/skills/ 镜像；⑤ 不含对 territory.forbidden 的改动"
    },
    {
      "stage_id": "S3-command-thinning",
      "agent_kind": "skill-author",
      "target_ref": "T-003",
      "task": "命令瘦身：把 templates/commands/*.md 改写为更高层次的建模——每个命令模板只记录该调用哪些技能、如何调用、以及每个技能的输入与产出，实现细节全部下沉到技能。受**模板中立性**约束：瘦身后的模板 MUST NOT 嵌入本仓专属内容（真源 docs/reference/history/00-cross-cutting-lessons.md:124）。逐个命令改写，每个命令的 AUTO-GENERATED 头与再生成链（regen-command-copies.py）保持完好。**本 stage 由 N 次派发累积：N = `find templates/commands -name '*.md' | wc -l` ÷ 5 向上取整（as-of 2026-10-06 基线 25 ⇒ 5 批），每批 5 个命令，每批改完立即写盘。**",
      "inputs_from": ["S2b-structure-alignment"],
      "outputs": [".specify/teams/.work/command-logic-as-classified-skills/S3-thinning/"],
      "blockedBy": ["S2b-structure-alignment"],
      "quality_gate": "① 以 goal 判据原文为口径逐命令判定「是否只含技能调用与其输入产出、不含实现细节」，每行附判定与残留细节的具体位置；② 整批判定附 ≥2 个实读文件证据；③ 每个被点名技能的目录在仓内存在（`test -d`）；④ 门控扫描 total ≤ 23；⑤ `pytest -m contract` 不新增失败（同口径 A/B 失败集求差 + 差集逐项归因，不比绝对数字）；⑥ 不含对 territory.forbidden 的改动"
    }
  ],
  "handoff_protocol": "file-path-only",
  "progress_file": ".specify/teams/.work/command-logic-as-classified-skills/progress.md"
}
```

**DAG（无环）**：`S0 → S1 → S2a → S2b → S3`，线性链，拓扑序即派发序。

```mermaid
flowchart LR
  S0[S0 命令普查裁定<br/>T-001] --> S1[S1 提炼建技能+标注<br/>T-001]
  S1 --> S2a[S2a 契约齐备<br/>T-002]
  S2a --> S2b[S2b 结构对齐<br/>T-002]
  S2b --> S3[S3 命令瘦身<br/>T-003]
  CC[contract-checker<br/>独立判定席] -.判定表.-> S1
  CC -.判定表.-> S2a
  CC -.判定表.-> S2b
  CC -.判定表.-> S3
  TS[team-supervisor<br/>唯一 Meta 落盘者] ==> CC
```

**每次交接的验证门（serial 的强制项）**：supervisor 消费 contract-checker 的判定表跑一次轻量检查——下游 stage 的 `inputs_from` 契约是否被上游产物满足（如 S1 需要 S0 裁定表非空且每行可解析；S3 需要 S2b 判定表覆盖全部技能且每个待引用技能目录存在）。验证保持轻量，不做上游的全量重评。失败走 `failure_strategy: retry-once-then-escalate`，重试上限 2 次；MUST NOT 用 retry 预算承载 stage 的累积批数。

**Target 指派与递进序**：goal 层的 Target 集**无序**、切片间**无依赖边**，所以 `T-001 → T-002 → T-003` 的递进序只存在于本团队计划（`config.progression` + `config.target_map` + 上面的 DAG）。一次运行经 `/speckit.team run command-logic-as-classified-skills --target T-<nnn>` 聚焦一条切片，对应执行 `target_map` 里映射的 stage；不带 `--target` 时对 goal 整体运行（走完整条链）。本团队**不声明 `focus_target`**：它只是 run 级 `--target` 的预填，而三条切片会依次关闭，一旦 T-001 转 done，预填会让后续不带 `--target` 的运行撞上 run-checks 的「终态引用」而阻塞。显式逐次指派没有这个陷阱。

**跨会话续跑**：progress 文件存在即解析 stage 表定位状态，从第一个未完成 stage 继续；每个 stage 的累积批次以「已声明批次名在产物中可检索」为准，桩文件不算完成。

**Summary 刷新**：每个 stage 交接验证通过后刷新一次（`every: 1`），交付目录 `.specify/goal/command-logic-as-classified-skills/summary/`（由 `goal_slug` 派生，不由团队 slug 派生），非交互调用。门控顺序与状态行口径由 `skills/create-team/SKILL.md` §Summary Refresh 持有，run report 里 MUST 出现且只出现一条 `Summary:` 状态行。

## Self-Improvement Contract

- Subject: this persisted team definition; member executions are evidence.
- Observe: completed run reports and Post-Run Critique.
- Improve: follow `.specify/shared/workflow/self-improvement-workflow.md`; route through `improve-team`.
- Boundary: preserve team authority, maturity gates, budget, kill-switch, and verifier independence.
- Verify: validate now and wait for a comparable later run before claiming improvement.
