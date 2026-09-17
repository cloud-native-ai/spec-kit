---
name: 绘图双层结构重构团队
slug: draw-two-layer-structure
description: 以 serial 三阶段链（重构 → 净室自测 → 评价采集）推进 skills/draw-diagram 语义前门与 skills/draw-{d3js,drawio,echarts,excalidraw,mermaid,plantuml} 语法引擎的两层自治结构；每次交接有独立验证门
goal: >
  承接已定义 Goal `draw-two-layer-structure`（权威定义：.specify/goal/draw-two-layer-structure/goal.md）。
  本字段仅为可读性渲染，与定义不一致时以定义为准。终态：调用 draw-diagram 不必告知「画什么」（它据上下文
  与补充说明自行分析语义、辨识层级/依赖/上下关系、抽象图表并选定结构类型后委派渲染）；调用五个 draw-* 引擎
  不必告知布局、线段绘制与渲染等实现细节；每次出图后主动征询用户评价并据以调整。
goal_slug: draw-two-layer-structure
territory:
  write:
    - skills/draw-diagram/**
    - skills/draw-d3js/**
    - skills/draw-drawio/**
    - skills/draw-echarts/**
    - skills/draw-excalidraw/**
    - skills/draw-mermaid/**
    - skills/draw-plantuml/**
    - .specify/teams/draw-two-layer-structure/**
    - .specify/memory/feedback/**
    - shared/definitions/probe-definitions.md    # evaluation form 的 probe Class/Object 注册面（internal probe 真源）
  read:
    - skills/**
    - .specify/skills/**
    - .specify/shared/**
    - .specify/agents/**
    - .specify/goal/draw-two-layer-structure/**
    - .specify/memory/knowledge/visualization-skill-selection.md
    - .specify/memory/feedback/**
  forbidden:
    - .specify/teams/viz-skill-arena/**          # 保留的 arena 团队（D5：逐步不用、不废弃），本团队不得触碰
    - .specify/goal/draw-two-layer-structure/goal.md   # authored：只经 /speckit.goal 的引擎渲染
    - shared/definitions/goal-definitions.md    # Goal 概念 owner；用户裁定属性 2 遵循原设定，本次明确不改
    - .specify/shared/definitions/goal-definitions.md   # 同上（镜像）
    - .specify/shared/definitions/probe-definitions.md  # 镜像由 sync-mirrors 生成，不手改
    - .specify/memory/feedback/probe-map.md     # 派生物：由 feedback-utils.py --action map 重建，禁手编
    - templates/**                              # 框架模板中立性
  non_path:
    - { type: skill-invocation, target: 七个绘图技能的净室调用（draw-diagram 前门 + 六引擎） }
    - { type: framework-convention, target: feedback-step.md 的 never-solicit 条款保持不动；用户评价另立 evaluation form 承载面 }
pattern: serial
created: 2026-09-16
updated: 2026-09-16
members:
  - agent: agent-team-supervisor-template
    role: team-supervisor
    stage: meta
    type: Meta
    lifecycle: persistent
    responsibility: serial Lead 与唯一 Meta。读 goal.md 判据 + progress 文件 → 按拓扑序派发三阶段 → 每次交接跑轻量验证门 → 唯一有权把变更写入 canonical skills/draw-*/ 与团队配置 → 写 run report / progress 文件 / summary 输入
  - agent: structure-adjuster
    role: structure-refactorer
    stage: executor
    type: Worker
    lifecycle: temporary
    responsibility: S1 重构——产出文件层面的打碎重组方案与补丁集到工作区（语义层归位 draw-diagram、清理引擎侧语义残留与独立语义规划回退、收敛 frontmatter 路由级触发词、为 evaluation form 落承载面）；并承接 draw-drawio 的**新建**（经 create-skills，出生即合规于语法层）与七引擎**能力轴路由判据**的落稿；不直接写 canonical 技能目录
    blockedBy: []
  - agent: skill-verifier
    role: cleanroom-verifier
    stage: evaluator
    type: Worker
    lifecycle: temporary
    responsibility: S2 净室自测——干净 context + subagent 调用技能绘制，判产物是否符合预期（前门未被告知「画什么」是否仍能自行分析语义；引擎未被告知布局/线段/渲染是否仍能兑现）；并按四条能力轴出**判别性用例**（动态图表诉求、本地渲染自由图表诉求、远端渲染强语义诉求各至少一例，验前门是否选对引擎）；写验证报告，与 S1 不同席、不同会话
    blockedBy: [structure-refactorer]
  - agent: agent-stage-executor-template
    role: evaluation-intake
    stage: executor
    type: Worker
    lifecycle: temporary
    responsibility: S3 评价采集——核验七个技能交付后都主动征询用户评价；按「无评价 = 本次满意」口径入账，有评价则经 feedback probe 送入 .specify/memory/feedback 处置流程并回写处置结论
    blockedBy: [cleanroom-verifier]
config:
  handoff_protocol: file-path-only
  progress_file: .specify/teams/.work/draw-two-layer-structure/progress.md
  failure_strategy: retry-once-then-escalate
  verification: independent            # S2 与 S1 不同席；验证者默认 REJECT 立场
  co_targets:
    - skills/draw-diagram
    - skills/draw-d3js
    - skills/draw-drawio
    - skills/draw-echarts
    - skills/draw-excalidraw
    - skills/draw-mermaid
    - skills/draw-plantuml
  layering: >
    语义层（draw-diagram）只承载语义绘图知识——层级、结构、关联、样式、配色等高阶概念与路由判据；
    语法层（draw-*）只承载语法绘图知识——布局、线段、脚本、渲染等底层实现方法。
    用户评价以 evaluation form 承载，复用 feedback 链路但不等同于 feedback；
    标准 feedback（agent 自省、守 feedback-step.md 红线）与 evaluation form 在同一技能内分立为两物。
  capability_axes: >
    引擎选择除既有的「图种独占 / artifact_intent tie-break」外，还须沿四条能力轴判别：
    ① 动态图表能力（可交互/可随数据刷新）；② 渲染位置（本地渲染 vs 远端渲染）；
    ③ 版面自由度（可绘自由图表 vs 文本语法生图、版面受语法约束）；
    ④ 语义强度与绘图约束的正相关（语义越强、约束越强）。
    **本字段只登记「存在这四条轴」这一分层事实；每条轴上各引擎的取值、判据与红线由
    `skills/draw-diagram/references/routing-matrix.md` 独占承载（One Source Of Truth，
    team.md MUST NOT 复写其表格或取值）。** 轴与既有独占登记是正交维度，不是替代关系。
  summary:
    enabled: true
    every: 1                           # bounded pattern 默认每阶段边界刷新一次
    delivery_dir: .specify/goal/draw-two-layer-structure/summary/
    interactive: false
---

## Goal

**权威定义**：`.specify/goal/draw-two-layer-structure/goal.md`（`goal_slug` 引用，非内容副本）。以下为本团队视角的渲染，与定义冲突时以定义为准。

**终态**：绘图能力呈两层自治结构 —— `skills/draw-diagram` 是唯一入口且自行完成语义分析，`skills/draw-{d3js,echarts,excalidraw,mermaid,plantuml}` 各自归位语法实现，用户两层都不必补齐细节；出图后主动征询评价并据以调整。

**成功判据**：3 条，全部归 goal.md `## Success Criteria` 所有（判据权威在 Goal，本团队不复制、不另立第二套）。

**本团队承接的范围**：D9 裁定「重构 → 自测 → 公测」三段工作及其**先后依赖关系**归 team 承载，不进 Goal 的 Target（Goal Target 遵循无序、无依赖边的原约定）。三段落在下面的 stage 上：**重构** = S1a–S1e（因单次派发预算所限拆为五个 stage，见 Dynamic Structure 的粒度依据），**自测** = S2，**公测** = S3。

**明确不在范围内**：arena 竞技不再作为优化手段，但 `viz-skill-arena` 团队与结论账本 `.specify/memory/knowledge/visualization-skill-selection.md` 予以保留（列入 `territory.forbidden` 与 `read`）；前门对账本的三处活引用（`routing-matrix.md:3-4`、`draw-diagram/SKILL.md:66`、`:79`）不要求迁移或摘除。

## Static Structure

| Agent | Role | Stage | Type | Lifecycle | blockedBy |
|-------|------|-------|------|-----------|-----------|
| agent-team-supervisor-template | team-supervisor（serial Lead） | meta | **Meta**（唯一；唯一写 canonical 技能定义与团队配置） | persistent | — |
| structure-adjuster | structure-refactorer | executor | Worker（产出重构方案/补丁集到工作区） | temporary | — |
| skill-verifier | cleanroom-verifier | evaluator | Worker（判对象 = 技能实际运行产物） | temporary | structure-refactorer |
| agent-stage-executor-template | evaluation-intake | executor | Worker（写 feedback 条目 = 数据制品） | temporary | cleanroom-verifier |

**Type 判定依据**（按「写什么」判，不按角色名判）：只有 supervisor 写 canonical `skills/draw-*/` 技能定义与团队配置 → 唯一 Meta。三席 stage agent 分别产出补丁集（工作区制品）、验证报告（证据制品）、feedback 条目（数据制品），均为业务制品 → Worker。`structure-adjuster` 与 `skill-verifier` 复用 `.specify/agents/templates/` 下已存在的 agent 定义，未新造 capacity 制品。

**Role ↔ Stage 关系**：`structure-refactorer` 一个 role 服务 S1a–S1e **五个 stage**（同一 capacity，五次派发），故其 role 级 `blockedBy` 仍为 `[]`；stage 间的依赖边只在 workflow JSON 的 `blockedBy` 上表达，不下沉到 roster。roster 的 `blockedBy` 是 **role 级**的粗粒度依赖，不是 stage DAG。

## Dynamic Structure

**Pattern**：serial（质量优先）。选择依据：Pattern 决策树 Q1 对本目标的**主体工作**为否（重构与自测是有界的一次性工程，不是 cadence 驱动的流式工作），Q2 为否（三阶段共享同一批可变状态：六个技能目录），**Q3 命中**（任务构成严格序列，S1 的产出是 S2 的输入，S2 的产出是 S3 的输入；信号词「阶段」「依次」）。

> **为何不是 continuous**：Goal 本身是长期目标（D7：不设终止阈值），但 `operating-loops.md` §1 规定 continuous **必须从 L1 报告态起步、不可跳级**，而 L1 的写权限仅为「读、评、写 STATE.md 与 run report」且 `max_subagents_per_cycle: 0` —— 选 continuous 意味着本团队在晋级 L2 之前无法改动任何 `skills/draw-*/` 文件，即做不了 S1。长期性由 Goal 的 lifecycle 承载（`active` 不轻率转 `achieved`），不必由团队 pattern 承载。

**Workflow**：

```json
{
  "workflow_id": "draw-two-layer-structure-chain",
  "name": "绘图双层结构重构链",
  "stages": [
    {
      "stage_id": "S1a-mermaid",
      "agent_kind": "structure-refactorer",
      "task": "draw-mermaid（60 文件）目录级层级归属 + 例外清单。目录级整批判定：references/document/(13)、references/howto/(20)、scripts/(3)、server/(7)、best-practices/(2)、references/guide/(6)、references/ 顶层(index.md、sds-realization.md、cycle3-reproduction-lessons.md)。例外走文件/章节级：SKILL.md（按节，尤其 ~line 120 的独立语义规划回退）、references/guide/{diagram-principles,layout,style,content}.md（语义层，与 plantuml 那份已漂移）、references/howto/00-semantic-analysis.md、references/howto/10-layout-planning.md、references/cycle3-reproduction-lessons.md（dated record，不改写）",
      "inputs_from": [],
      "outputs": [".specify/teams/.work/draw-two-layer-structure/S1-refactor/ownership-mermaid.md"],
      "blockedBy": [],
      "quality_gate": "draw-mermaid 每个目录都有层级判定；例外清单里每个文件有判定，判 MIGRATE 的附源→目的路径；不含对 territory.forbidden 的改动"
    },
    {
      "stage_id": "S1b-plantuml",
      "agent_kind": "structure-refactorer",
      "task": "draw-plantuml（52 文件 / 6 目录）**纯 attribution**：目录级层级归属 + 例外清单，形同 S1a。例外含 SKILL.md:29 的视觉权重层级规则（大模块边框 > 小模块边框 > 流线，属语义层）、~line 78 的独立语义规划回退、references/guide/ 六个文件（逐个判定，并**标记哪些有 mermaid  counterpart**供下游对照，但本 stage 不做对照裁定）、references/howto/00-semantic-analysis.md、references/howto/10-layout-planning.md、references/cycle4-improvements.md（dated action record，run 2026-09-16T102026Z 查实存在于 plantuml/d3js/excalidraw/echarts 四个技能，原例外清单漏列）、references/document/ 16 个文件（不得预设整批语法：S1a 在 mermaid 同名目录查出 5 个引擎无关建模文件）。**不含 guide/ 合并裁定**——该项已移交 S1d（run 2026-09-16T102026Z 诊断：attribution 与 reconciliation 是两种任务类型，预算量级不同，MUST NOT 同 stage）",
      "inputs_from": ["S1a-mermaid"],
      "outputs": [".specify/teams/.work/draw-two-layer-structure/S1-refactor/ownership-plantuml.md"],
      "blockedBy": ["S1a-mermaid"],
      "quality_gate": "① draw-plantuml 6 个目录 + 顶层 SKILL.md + references/ 顶层 4 文件全部有层级判定；② 例外清单逐文件有判定，判 MIGRATE 的附源→目的路径；③ **任何整批（wholesale）目录判定必须点名 ≥2 个实际打开过的文件**——覆盖型 gate 检不出「判定错了」，只检得出「没判定」，故强制附实读证据；④ **增量落盘为 gate 条件而非 brief 建议**：每个判完的目录立即写盘，产物中每个已声明判定的目录名必须可检索（run 2026-09-16T102026Z 教训：S1b 未增量落盘，撞顶后自述已完成的 document/ 分类全损，产物只剩 10 行图例桩，而 VALIDATE 的「outputs exist」对桩文件为真）；⑤ 不含对 territory.forbidden 的改动"
    },
    {
      "stage_id": "S1c-rest-three",
      "agent_kind": "structure-refactorer",
      "task": "draw-excalidraw(25) + draw-d3js(9) + draw-echarts(13) 共 47 文件的目录级归属 + 例外清单。例外含 excalidraw references/howto/00-semantic-analysis.md 与 SKILL.md:49-53 的独立语义步、d3js SKILL.md:122-134 标注〔决策归语义层〕的残留决策文字、echarts 是否存在同类残留（需实测确认，不预设无）。三者 frontmatter description 仍自称的路由级触发词（架构图/流程图等）逐条列出并给收敛建议——「什么请求该用我」归前门路由回答",
      "inputs_from": [],
      "outputs": [".specify/teams/.work/draw-two-layer-structure/S1-refactor/ownership-rest-three.md"],
      "blockedBy": [],
      "quality_gate": "三个技能每个目录都有层级判定；例外清单逐文件有判定；三条 frontmatter 触发词收敛建议齐备"
    },
    {
      "stage_id": "S1d-frontdoor-destination",
      "agent_kind": "structure-refactorer",
      "task": "两件事，同属「什么落到前门哪里」这一种任务类型：(A) 汇总 S1a/S1b/S1c 的全部 MIGRATE 条目，为 skills/draw-diagram/（当前仅 SKILL.md + references/semantic-model.md + references/routing-matrix.md）设计迁入目的地结构，把每个迁入文件映射到唯一槽位，并标明 draw-diagram 现有 3 个文件自身的归属；(B) **guide/ 合并裁定**（自 S1b 移入）：mermaid 与 plantuml 的 references/guide/ 六个同名文件（content / diagram-principles / large-diagram-playbook / layout / style / syntax-reference）已互相漂移，逐对给出「哪份为基 + 每处差异如何处置（取基/取另一份/合并/丢弃）」，且**必须是章节级**——S1a 查实这些文件不是整批迁移，内含 engine-carrier 章节（mermaid/plantuml 专有语法嵌在 otherwise 语义的文档里）必须留在引擎侧，不得把冲突原样搬进前门。",
      "inputs_from": ["S1a-mermaid", "S1b-plantuml", "S1c-rest-three"],
      "outputs": [
        ".specify/teams/.work/draw-two-layer-structure/S1-refactor/frontdoor-destination.md",
        ".specify/teams/.work/draw-two-layer-structure/S1-refactor/guide-merge-ruling.md"
      ],
      "blockedBy": ["S1a-mermaid", "S1b-plantuml", "S1c-rest-three"],
      "quality_gate": "① 每条 MIGRATE 都有唯一目的地槽位（无重复槽位、无未安置项）；② 六个技能的目录级归属汇总为一张全表；③ draw-diagram 现有 3 文件归属已标；④ guide/ 六对文件**逐对**有合并裁定，且每对都点名了须留在引擎侧的 engine-carrier 章节；⑤ 增量落盘为 gate 条件：两份产物分文件写、每完成一对/一批立即落盘，任一产物的每个已声明条目名必须可检索（桩文件不得通过）。**预算预案（预先约定，不再事后争）**：本 stage 需消化约 60KB 上游产物 + 6 对文件的章节级裁定，若撞派发轮次上限，约定的拆法是把它分为 S1d-1（A：聚合与目的地结构）与 S1d-2（B：guide/ 合并裁定），S1d-2 blockedBy S1d-1，两者各自一次派发；不得靠降低 ④ 的章节级要求来塞进一次派发。"
    },
    {
      "stage_id": "S1e-evaluation-form",
      "agent_kind": "structure-refactorer",
      "task": "设计 evaluation form 的承载面（Goal 判据 1）：新 probe **Class** 定义（收集内容 / 目标系统切片 / 收集后处理流程 / 适用插入位置类型 / internal-or-external kind）+ 六个 probe **Object**（含今天完全缺失的 draw-diagram 与 draw-excalidraw）+ 六个 SKILL.md 可直接嵌入的 evaluation-form 段文本。硬约束：MUST NOT 提议修改 .specify/shared/workflow/feedback-step.md 的 never-solicit 条款；新段须与该技能既有的 canonical `## Feedback` 段并存且互不混称；internal probe 真源是 shared/definitions/probe-definitions.md，probe-map.md 是派生物不得手编；external-custom 不可用（其 object_id 须 ext- 前缀、unit 须匹配 ^custom:，而这些是框架 skill:* 单元）",
      "inputs_from": ["S1d-frontdoor-destination"],
      "outputs": [
        ".specify/teams/.work/draw-two-layer-structure/S1-refactor/evaluation-form-design.md",
        ".specify/teams/.work/draw-two-layer-structure/S1-refactor/probe-class-proposal.md"
      ],
      "blockedBy": ["S1d-frontdoor-destination"],
      "quality_gate": "Class 五要素齐全；六个 Object 齐备（含补上缺失的两个）；嵌入文本与 canonical `## Feedback` 段分立不混称；未提议改 feedback-step.md；判定口径「无评价=满意、有评价经 probe 入 .specify/memory/feedback」在文本中可执行"
    },
    {
      "stage_id": "S1f-drawio-bootstrap",
      "agent_kind": "structure-refactorer",
      "task": "**新建 draw-drawio 技能**（今日 `skills/draw-drawio/` 不存在；仓内既有 drawio 提及仅为 plantuml 文档的旁述与 node_modules 噪声，无可复用素材）。与前五个引擎不同：新技能**没有待归属的存量文件**，故本 stage 不是 attribution 形，而是 **born-conforming 创建形**——出生即合规于语法层，不做事后搬迁。产出完整技能包草稿到工作区，**以 `create-skills` 的模板与约定为权威形态**（Worker MUST NOT 直接写 `skills/`；由 Meta 落地时经 `create-skills` 生成 canonical 骨架）。语法层内容（用户提供的一手参考已核实为引擎实现知识，全部归本技能）：① 产物格式 `mxGraph XML` / `.drawio`，生成用**未压缩 XML**（`<diagram>` 内 Base64 是压缩态，生成器无需处理）；② 必备结构 `mxCell id=\"0\"` 与 `mxCell id=\"1\" parent=\"0\"` 两根节点、vertex 用 `vertex=\"1\" parent=\"1\"` + `mxGeometry x/y/width/height`、edge 用 `edge=\"1\" source= target=` + `mxGeometry relative=\"1\"`、样式走 `style=\"rounded=1;whiteSpace=wrap;html=1;fillColor=…;strokeColor=…\"` 串语法；③ **本地渲染**四路：draw.io Desktop（Electron）/ 自托管 webapp / `viewer-static.min.js` 只读 HTML / embed iframe + postMessage（`action: load|export|save`）；④ **CLI 导出成熟**：`drawio -x -f svg|png|pdf -o <out> <in>`，Linux 无图形环境需 `xvfb-run -a`，macOS `/Applications/draw.io.app/Contents/MacOS/draw.io`、Windows `C:\\Program Files\\draw.io\\draw.io.exe`；⑤ **不含自动布局**——调用方必须自算 x/y/width/height（Node 侧 dagre/elkjs/graphlib，Python 侧 networkx/pygraphviz/graphviz），edge 仅需 source/target 即自动连线。硬约束：**语义层内容一律不内置**（层级/结构/关联/样式/配色/图类选择/版面自由度判据全部指向 draw-diagram 的 owner 文件，MUST NOT 复写）；与 draw-excalidraw 同属「本地渲染自由图表」，二者的**取舍判据属前门**，本技能 MUST NOT 自带「何时该选我」的路由叙事；frontmatter 触发词**出生即收敛**为引擎身份（`drawio` / `draw.io` / `.drawio` / `mxgraph` 一类），MUST NOT 声明 架构图/流程图/UML 等通用图类词（否则会重演 mermaid 63 条 / plantuml 65 条越界的老问题）；须含 `## Evaluation Form(绘制评价单)` 与 canonical `## Feedback` 两段并存不混称，Feedback 段取**多数派紧凑指针形**（2534 字节形，指向 `.specify/shared/workflow/feedback-step.md`），MUST NOT 取 draw-mermaid 的 3633 字节内联复述变体；须登记 2 个 probe Object（`skill-draw-drawio-wrapup` @ wrap-up、`skill-draw-drawio-evaluation-form` @ evaluation-form，均挂既有 Class，无需新 Class）。",
      "inputs_from": ["S1e-evaluation-form"],
      "outputs": [
        ".specify/teams/.work/draw-two-layer-structure/S1-refactor/drawio-skill-package.md",
        ".specify/teams/.work/draw-two-layer-structure/S1-refactor/drawio-probe-objects.md"
      ],
      "blockedBy": ["S1e-evaluation-form"],
      "quality_gate": "① 技能包草稿含 SKILL.md 全文 + 所需 references/ 文件清单与各文件职责，形态符合 `create-skills` 约定；② 上述 ①–⑤ 五类引擎实现知识逐类有着落，且**每类点名承载它的文件**；③ 语义层零内置——凡涉及层级/结构/关联/样式/配色/图类选择处均为指向 draw-diagram owner 的指针，抽查 ≥3 处证实为指针而非复写；④ frontmatter 触发词全为引擎身份，通用图类词计数为 **0**（机械抽取核验，不采信自述）；⑤ `## Evaluation Form(绘制评价单)` 与 `## Feedback` 两段并存、顺序为评价单在前、互不混称，且 Feedback 段为指针形（与 draw-diagram/d3js/echarts/plantuml 四技能同形）；⑥ 2 个 probe Object 行以注册表实际列格式给出（`object_id | class_id | unit | lifecycle_point`），且声明插入位置遵守「wrap-up 行在前」的行序即解析优先级约束；⑦ **增量落盘为 gate 条件**：SKILL.md 与各 references 草稿分文件写、每完成一个立即落盘，桩文件不得通过"
    },
    {
      "stage_id": "S1g-routing-axis",
      "agent_kind": "structure-refactorer",
      "task": "把用户裁定的**四条能力轴**落进整个套件的选择逻辑，owner 是 `skills/draw-diagram/references/routing-matrix.md`（team.md 的 `capability_axes` 只登记「轴存在」，取值与判据 MUST 只在本文件承载，禁第二处复写）。四轴：① **动态图表能力**（draw-d3js / draw-echarts 具备：可交互、可随数据刷新）；② **渲染位置**（draw-drawio / draw-excalidraw / draw-mermaid 本地渲染，**draw-plantuml 是唯一远端渲染**）；③ **版面自由度**（draw-drawio / draw-excalidraw / draw-d3js 可绘自由图表；**draw-mermaid 是文本生图**——文本须遵循语法、语法自身即携带语义，故**无法绘自由图表**；draw-echarts 受系列目录约束）；④ **语义强度与绘图约束正相关**（draw-plantuml 语义最强、约束亦最强）。要求：**(A)** **六引擎** × 四轴一张全表（d3js / drawio / echarts / excalidraw / mermaid / plantuml），每格有取值与一句依据，MUST NOT 留空或写 unknown。**draw-diagram 是前门、不是引擎**——它不渲染，故「渲染位置」「动态图表能力」等轴对它无取值，MUST NOT 为凑格数给它编造轴值；它在四轴上的角色是**据轴选引擎**，见 (D)；**(B)** 四轴与既有「独占登记 / 图类矩阵 / artifact_intent tie-break」是**正交维度而非替代**——既有三节保留，draw-drawio 补进独占登记（`.drawio` 可编辑产物、成熟 CLI 导出、标准流程图/架构图/UML 观感）、图类矩阵与 tie-break 顺序；**(C)** **draw-drawio 与 draw-excalidraw 的同轴竞争必须有判据**——二者同处「本地渲染 + 自由图表」，区分点为观感（标准工程图 vs 手绘白板）、产物（`.drawio` XML vs `.excalidraw` JSON）、导出成熟度（官方 CLI vs 需 Playwright/headless）、嵌入形态（viewer/iframe vs React 组件），须给出可判的优先序而非「皆可」；**(D)** 六个 specialist 的 frontmatter description 各自**陈述自己在四轴上的位置**并只声明引擎身份触发词，与前门不争通用图类词；draw-diagram 前门的 description 须说明它**以四轴为选引擎判据**（而非声称自己有轴位置）。硬约束：`routing-matrix.md` 行 3–4 指向竞技场结论账本 `${SKILL_WORKDIR}/.specify/memory/knowledge/visualization-skill-selection.md` 的证据源声明、以及既有 cycle 冠军与分值（如 cycle 3 R2 0.95 / 0.94、mermaid 0.755）是**dated 证据记录，MUST 逐字保留**——用户裁定 arena 团队与账本「逐步不再使用、不彻底废弃」，MUST NOT 删除或改写；新增四轴是**追加维度**，MUST NOT 以「四轴已覆盖」为由删既有判据；三条反路由红线保留并按需增补（如：不得把要求自由版面的诉求路由到 draw-mermaid/draw-plantuml）。",
      "inputs_from": ["S1f-drawio-bootstrap", "S1d-frontdoor-destination"],
      "outputs": [
        ".specify/teams/.work/draw-two-layer-structure/S1-refactor/routing-axis-matrix.md",
        ".specify/teams/.work/draw-two-layer-structure/S1-refactor/frontmatter-convergence.md"
      ],
      "blockedBy": ["S1f-drawio-bootstrap"],
      "quality_gate": "① **六引擎** × 四轴 = **24 格**全部有取值 + 一句依据，空格数 **0**（机械核验）；draw-diagram **不得**出现在轴值表中（出现即不过——它不是引擎）；② draw-drawio 已入独占登记、图类矩阵、tie-break 三处，缺一不过；③ drawio ↔ excalidraw 同轴竞争给出**可判优先序**，出现「皆可/视情况」字样即不过；④ 既有 arena 证据行（证据源声明 + cycle 冠军分值）逐字保留——以 `diff` 核验被保留行未被改写；⑤ 七技能 frontmatter 全部到位——六个 specialist 各陈述自身四轴位置、前门陈述以四轴为判据，且七者通用图类触发词计数为 0（机械抽取核验，不采信自述；前门 draw-diagram 例外：它**必须**持有通用图类词，那是它的职责，故本条对它只核「不因四轴新增而丢失既有通用词」）；⑥ 四轴取值只在 `routing-axis-matrix.md`（落地后进 `routing-matrix.md`）承载，team.md / 各 specialist SKILL.md 内**无取值复写**（One Source Of Truth，抽查证实为指针）；⑦ 增量落盘为 gate 条件：两份产物分文件写、每完成一轴/一引擎立即落盘，桩文件不得通过；**预算预案（预先约定）**：本 stage 需消化七引擎现状 + 改写 routing-matrix.md + 收敛七份 frontmatter，若撞派发轮次上限，约定拆为 S1g-1（A+B+C：四轴全表与矩阵改写）与 S1g-2（D：七份 frontmatter 收敛），S1g-2 blockedBy S1g-1，MUST NOT 靠降低 ③ 的可判性要求塞进一次派发"
    },
    {
      "stage_id": "S2-cleanroom-verify",
      "agent_kind": "cleanroom-verifier",
      "task": "干净 context + subagent 调用技能绘制，评估结果是否符合预期：只给绘图意图、不给「画什么」的细节，看前门能否自行分析语义并正确委派；只给语义规格、不给布局/线段/渲染指示，看引擎能否自行兑现。**并须含四条能力轴的判别性用例**：(a) 动态/可交互图表诉求 → 应落 d3js 或 echarts；(b) 本地渲染的自由版面图表诉求 → 应落 drawio 或 excalidraw，且二者取舍须与 S1g 的优先序一致；(c) 明确要求文本生图、进仓库免工具链直渲 → 应落 mermaid，且 MUST NOT 被要求绘自由版面；(d) 最强 UML 语义且可接受远端渲染与更强约束 → 应落 plantuml。每例记录前门实际选择的引擎与理由，选错即为不通过。",
      "inputs_from": ["S1g-routing-axis"],
      "outputs": [".specify/teams/.work/draw-two-layer-structure/S2-cleanroom-verify/report.md"],
      "blockedBy": ["S1g-routing-axis"],
      "quality_gate": "**七个技能**每个被调一条 通过/不通过 + 证据产物路径；四条能力轴判别用例 (a)–(d) 各至少一条且各有明确的引擎选择结论；任何不通过项回退对应 S1x（failure_strategy: retry-once-then-escalate）"
    },
    {
      "stage_id": "S3-evaluation-intake",
      "agent_kind": "evaluation-intake",
      "task": "核验**七个技能**在交付产物后都主动征询用户评价；按「无评价 = 本次绘制满意」口径入账；有评价则经 feedback probe 送入 .specify/memory/feedback 并跟踪处置结论反哺对应技能",
      "inputs_from": ["S2-cleanroom-verify"],
      "outputs": [".specify/teams/.work/draw-two-layer-structure/S3-evaluation-intake/channel-check.md"],
      "blockedBy": ["S2-cleanroom-verify"],
      "quality_gate": "**七个技能**各有一条征询面证据（技能文件里的 evaluation form 段落 + 已注册 probe 对象）；.specify/memory/feedback/index.json 出现对应条目，或显式声明缺口而非静默略过"
    }
  ],
  "handoff_protocol": "file-path-only",
  "progress_file": ".specify/teams/.work/draw-two-layer-structure/progress.md"
}
```

**DAG 校验（无环）**：7 个 stage，边集 = `S1a→S1b`、`{S1a,S1b,S1c}→S1d`、`S1d→S1e`、`S1e→S2`、`S2→S3`。拓扑序：`{S1a, S1c}`（可并发，无数据依赖）→ `S1b` → `S1d` → `S1e` → `S2` → `S3`。无环。这是 `patterns.md` 场景表的「Mix of independent + dependent → Serial Chain with parallel stages」形态，不是单线链。

> **粒度与拆分依据（证据驱动的结构编辑，2026-09-16）**：原 S1 为单 stage，run `2026-09-16T060815Z` 实测两次派发均撞 15 轮上限、gate 判 FAIL。订正后的量化：六技能合计 162 文件，**单次派发只能完成约 13 个文件的逐文件归属**，逐文件粒度需 12–14 次派发。故本次同时改两件事——(1) 交付粒度从「逐文件」改为「**目录级归属 + 例外清单**」：`references/document/*`、`references/howto/*` 这类整目录都是引擎语法文档，按目录用途整批判定即可，只有已知混杂项（六个 `SKILL.md`、两个 `references/guide/` 语义层、`howto/00-semantic-analysis.md`、`howto/10-layout-planning.md`）走文件/章节级；(2) 按此粒度把 S1 拆成 S1a–S1e 五个 stage，每个装得进一次派发预算。详见该 run report 的「根因（可量化，已订正）」节。

**执行流**：

```
SUPERVISOR: 读 goal.md 判据 + progress 文件 → 取拓扑序中全部 blockedBy 已满足的 stage
  │
  ├─▶ S1a-mermaid（structure-adjuster）      ── 60 文件，目录级 + 例外
  │     └─ 交接门 A：mermaid 每目录有判定？例外逐文件有判定？MIGRATE 有源→目的？
  │        └─ 通过 → 解锁 S1b
  │
  └─▶ S1c-rest-three（structure-adjuster，与 S1a 并发）── excalidraw+d3js+echarts 47 文件
        └─ 交接门 C：三技能每目录有判定？三条 frontmatter 触发词收敛建议齐？
  │
  ▼ S1b-plantuml（读 S1a 产物做 guide/ 漂移对照）── 52 文件
  │  交接门 B：plantuml 每目录有判定？**两份漂移 guide/ 有合并裁定**？
  │
  ▼ S1d-frontdoor-destination（需 S1a+S1b+S1c 全通过）
  │  汇总全部 MIGRATE → 为 draw-diagram 设计目的地结构，每条映射唯一槽位
  │  交接门 D：无未安置项、无重复槽位？六技能目录级归属汇成全表？
  │
  ▼ S1e-evaluation-form
  │  probe Class 五要素 + 六个 Object（补 draw-diagram / draw-excalidraw）+ 六段可嵌入文本
  │  交接门 E：未提议改 feedback-step.md？与 canonical `## Feedback` 分立不混称？
  │
  ▼ SUPERVISOR（唯一 Meta）把 S1a–S1e 通过的方案落入 canonical skills/draw-*/
  │  + shared/definitions/probe-definitions.md，再跑 sync-mirrors.py --write
  │
  ▼ S2-cleanroom-verify（skill-verifier，独立会话）
  │  干净 context 调用技能 → report.md（逐技能 通过/不通过 + 证据路径）
  │  交接门 F：S2 通过项是否覆盖 S3 需核验的六个征询面？不通过 → 回对应 S1x
  │
  ▼ S3-evaluation-intake（agent-stage-executor-template）
  │  核验征询面就位 + 入账口径可执行 → channel-check.md
  │
  ▼ SUPERVISOR: 写 run report（runs/<UTC>-report.md）+ progress 文件
                + summary 输入（.specify/goal/draw-two-layer-structure/summary/）
```

**交接验证纪律**：serial 的每次交接**必须**有一次轻量验证（针对下游 `inputs_from` 契约的定向检查，不是重新全面评估）；验证失败先走 `failure_strategy`，再决定是否解锁下游。全程 file-path-only handoff，不传递上下文正文。

**两条适用于全部 stage 的通用 gate 条款**（本小节是这两条的 owner；各 stage 的 `quality_gate` 只在需要附证据时引用，不重述）：

1. **增量落盘是 gate 条件，不是 brief 建议。** 每完成一个判定单元（一个目录 / 一对文件 / 一个技能）立即写盘；产物中每个已声明判定的条目名必须可检索。**桩文件不得通过 VALIDATE** —— `patterns.md` 的 Stage Execution Protocol 只检「outputs exist」，而一个只有标题与图例的 10 行桩文件对「exist」为真。证据：run `2026-09-16T102026Z` 的 S1b 撞顶后自述已完成的 `document/` 分类全损。
2. **整批判定必须附实读证据。** 任何 wholesale（整目录 / 整批文件）判定必须点名 **≥2 个实际打开过的文件**。覆盖型 gate 只检得出「没判定」，检不出「判定错了」。证据：同一次 run 中，S1a 若照 brief 字面把 `references/document/` 整批判为引擎语法，gate 会通过，而该目录实含 5 个引擎无关的建模知识文件；S1c 据此纪律才发现 echarts 并不干净。


**链终止之后**：本团队是有界链，跑完即止。Goal 的长期性（D7）由两件不属于本团队的事承载 —— 六个技能自身的 evaluation form 步骤在每次绘制时征询评价，以及 `/speckit.feedback` 的处置流程持续消化这些条目。若日后需要一个常驻循环来盯这两条，那是另立 continuous 团队的事（届时按 L1 报告态起步），不由本团队 pattern 承担。

## Self-Improvement Contract

- Subject: this persisted team definition; member executions are evidence.
- Observe: completed run reports and Post-Run Critique.
- Improve: follow `.specify/shared/workflow/self-improvement-workflow.md`; route through `improve-team`.
- Boundary: preserve team authority, maturity gates, budget, kill-switch, and verifier independence.
- Verify: validate now and wait for a comparable later run before claiming improvement.
