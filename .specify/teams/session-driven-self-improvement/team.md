---
name: 自我提升流程建立团队
slug: session-driven-self-improvement
description: >
  以 serial 五阶段链（运行判定契约 → 运行判定实现 → 被动触发接线 → 主动触发命令 → 独立验证）
  在框架源码中建立一套 improve 流程；交付物是定义类文件，故 Worker 只产补丁到工作区，
  canonical 落盘由唯一 Meta supervisor 执行，每次交接有独立验证门
goal: >
  承接已定义 Goal `session-driven-self-improvement`（权威定义：.specify/goal/session-driven-self-improvement/goal.md）。
  本字段仅为可读性渲染，与定义不一致时以定义为准。终态：框架中有一套 improve 流程，含两个方面 ——
  主动触发（通过 improve 命令）与被动触发（通过运行判定的结果触发 feedback 流程）。
  成功判据以定义为准，本团队不复述其文本；其主体是「一套新的运行判定，统一 token 消耗、耗时、
  正确性与满意度四个量」。本目标只**建立**该流程，不**进行**提升 —— 提升的发生由流程建成后的
  日常运行承载，不是本团队的交付物。
goal_slug: session-driven-self-improvement
territory:
  write:
    - templates/commands/improve.md                # S4 主动触发入口（尚不存在，本团队创建）
    - shared/workflow/feedback-step.md             # S3 被动触发接线（运行判定结果 → feedback 流程）
    - shared/workflow/self-improvement-workflow.md # S3/S4：SI-2 悬空的 /better-harness 引用、SI-4 路由表缺命令与 memory 归口
    - templates/instructions-template.md           # 运行判定规则的框架源落点（Two Hats：不是 .specify/instructions.md）
    - scripts/python/**                            # 运行判定引擎的 canonical 家；本团队新增一个引擎，MUST NOT 改动契约外的既有引擎
    - tests/contract/**                            # 新机制的结构契约测试
    - .specify/teams/session-driven-self-improvement/**
  read:
    - .specify/memory/session/**                   # 证据来源 1：session 历史记录（10 文件）
    - .specify/memory/evidence/**                  # 证据来源 3：大语言模型调查结论（106 文件）—— MUST 消费摘要/字段投影，禁止原文转储（Summary-First）
    - .specify/memory/feedback/**                  # 被接线的 feedback 存储（26 文件）
    - .specify/memory/session/2026-10-05-goal-session-driven-self-improvement-interview.md
    - .specify/memory/session/2026-10-05-goal-session-driven-self-improvement-interview.dag.json
    - .specify/goal/session-driven-self-improvement/**
    - .specify/goal/command-logic-as-classified-skills/**   # 交互目标：T-003 要求命令只做入口+委派
    - shared/**                                    # 框架源码（definitions / guidelines / patterns / workflow）
    - .specify/shared/**                           # 运行时镜像，只读
    - .specify/agents/**
  forbidden:
    - .specify/goal/session-driven-self-improvement/goal.md   # authored：只经 /speckit.goal 的引擎渲染
    - .specify/shared/**                           # 镜像：由 sync-mirrors 生成，不手改
    - .specify/templates/**                        # 镜像：同上
    - .specify/scripts/**                          # 镜像：同上
    - .specify/instructions.md                     # 由 /speckit.instructions 生成，不手改
    - .specify/memory/feedback/probe-map.md        # 派生物：由 feedback-utils.py --action map 重建，禁手编
    - shared/guidelines/proactive-trigger.md       # 情境/信号词表的扩展 MUST 走用户批准通道，本团队不得自行扩表
    - shared/definitions/goal-definitions.md       # Goal 概念 owner；D3 已裁定属性 2 不改
    - .specify/teams/draw-two-layer-structure/**   # 他团队目录
    - .specify/teams/viz-skill-arena/**            # 他团队目录
    - .specify/teams/command-logic-as-classified-skills/**
  non_path:
    - { type: scope-set, target: 提升对象的开放集合 —— 包括但不限于命令、skills、memory（D9 细节 4）。命令与 memory 今天在 SI-4 路由表里无归口，归口方式由 S1 契约决定，不在本文件预设 }
    - { type: framework-convention, target: feedback 四条红线保持不动；改点是流程内的观察 sensor，不充当干预台账 —— SI-7 的 intervention.json 留在基线证据运行目录。wholesale 归一 self-improvement→feedback 不做（三处结构冲突：红线 2 可删除性、红线 3 打包上送会把仅本仓可解析的 run id 带进上游 bundle、sensor never a mutation authority） }
    - { type: naming, target: 机制已定名「运行判定 (Run Determination)」—— 经用户批准通道定名（2026-10-06），glossary 词条 origin=user / status=confirmed。占位形「判断逻辑」退役为变体；「断言」因与本仓契约测试断言（四条归因轴之一、空真断言、反空真哨兵、可断言面、053 特性主题）冲突而弃用，且刻意不登记为变体，以免词汇表把契约测试语境的正当用法误纠过来。英文形避开 assessment，因 情境评估 (Situational Assessment) 已被 proactive-trigger 占用 }
    - { type: ceiling, target: 确认门控预算 —— scan-confirmation-gates.py 的 total MUST 保持 ≤ 23（as-of 2026-10-06 实测 23，余量 0，violations 0）。本团队 6 个 write 目标里有 4 个落在 SCAN_DIRS（templates/commands、skills、shared）或 SCAN_ROOT_FILES（templates/*.md）内，故 S3/S4 任何新增 BLOCKING_PATTERNS 命中会同时打爆两个契约测试。易误踩的模式：confirmation gate、确认门禁、确认门控、after confirmation、Confirm before、inviting the user to submit collected feedback。落盘前 MUST 跑一次扫描器并附 total 读数 }
    - { type: cross-goal-write, target: templates/commands/improve.md 的写权归本团队 S4。command-logic-as-classified-skills 团队的 templates/commands/*.md 经用户明示授权（2026-10-06）已在其 territory.forbidden 中排除该文件，其 T-003 命令瘦身 MUST 跳过它；本团队 S4 则按其 T-003 约定出生即为入口+委派薄壳，两个目标互相合成而非互相覆盖。**该裁定对机器不可见** —— build-summary-input.py 的 _write_intersections 只比 write×write、从不减 forbidden，故 create-mode schema 允许的「forbidden-write entry」解法在 shipped 校验器下仍会报 overlap；此缺口已记入 feedback }
    - { type: cross-goal, target: /speckit.improve 命令属 Requirement 平面（litmus test 5：约束本项目源码实现什么），其规格入口是 /speckit.requirements；本团队只按既有约定落其框架源文本，不代替该平面做需求决策 }
pattern: serial
created: 2026-10-06
updated: 2026-10-06
members:
  - agent: agent-team-supervisor-template
    role: team-supervisor
    stage: meta
    type: Meta
    lifecycle: persistent
    responsibility: >
      serial Lead 与唯一 Meta。读 goal.md 判据 + progress 文件 → 按拓扑序派发五阶段 →
      每次交接跑轻量验证门 → 唯一有权把 Worker 补丁落到 canonical 路径（templates/、shared/、
      scripts/、tests/）并触发镜像再生 → 写 run report / progress 文件 / items.jsonl / summary 输入。
      交付物是定义类文件，故本席位由可选质量门变为必需的 Meta 落盘者（conceptual-model.md § 消解条款）；
      缺它时 Worker 只能越权写 canonical。
  - agent: agent-stage-executor-template
    role: judgment-contract-designer
    stage: executor
    type: Worker
    lifecycle: temporary
    responsibility: >
      S1 运行判定契约——产出契约文档补丁到工作区：统一 token 消耗 / 耗时 / 正确性 / 满意度四个量的
      判定口径与输出形态；三个证据来源（session 历史记录、用户输入、大语言模型调查结论）各自的读取面
      与摘要口径；被动触发与主动触发分别在哪一点消费该输出；该逻辑如何推广 feedback-step.md 里既有
      的三层无名判断（complex iff 分类、Gate on qualification & completion、should_prompt）；
      以及命令与 memory 在 SI-4 路由表里的归口方式。不直接写 canonical。
    blockedBy: []
  - agent: agent-stage-executor-template
    role: judgment-engine-implementer
    stage: executor
    type: Worker
    lifecycle: temporary
    responsibility: >
      S2 运行判定实现——按 S1 契约把固定规则判断实现为 scripts/python/ 下的确定性程序（Program-First：
      可表达为固定规则的判断交程序，LLM 只收裁决或摘要）。对 .specify/memory/evidence/ 的 106 个文件
      MUST 走摘要/字段投影，禁止原文转储（Summary-First）。产出引擎补丁 + 单测补丁到工作区。
    blockedBy: [judgment-contract-designer]
  - agent: agent-stage-executor-template
    role: passive-trigger-wirer
    stage: executor
    type: Worker
    lifecycle: temporary
    responsibility: >
      S3 被动触发接线——产出 shared/workflow/feedback-step.md 与 templates/instructions-template.md
      的补丁：运行判定的结果如何触发 feedback 流程。MUST 守 feedback 四条红线（被动推断而非征询，
      故不触 never-solicit）。MUST 落 D9 细节 3：被动触发不得面面俱到以免干扰当前流程，
      超出者经新建 spec 或 todo 记录，留待主动触发处置。产出改点作为流程内观察 sensor 的落点，
      不新建平行自我提升库。
    blockedBy: [judgment-engine-implementer]
  - agent: agent-stage-executor-template
    role: active-trigger-author
    stage: executor
    type: Worker
    lifecycle: temporary
    responsibility: >
      S4 主动触发命令——产出 templates/commands/improve.md 补丁，实现 D9 细节 2 的 why → what → how
      （why：当前问题是什么，由 session 历史获取；what：需提升哪些方面；how：分析问题、探索思路、
      实施改造），消费 S2 的运行判定引擎。按 command-logic-as-classified-skills T-003 出生即为
      入口+委派的薄壳：命令文本只记录该调用哪些技能、如何调用、**以及每个技能的输入与产出**，
      实现细节全部落技能侧（T-003 原文含「每个技能的输入和产出」子句；2026-10-07 补齐——此前
      本文件四处渲染 T-003 均漏该子句，而对方团队 S3 按裁定跳过 improve.md，本 stage 是该文件
      唯一的判定门，漏掉即无人守）。本 stage 由 2 次派发累积（N=2 的依据见动态结构小节的
      粒度声明）。不直接写 canonical。
    blockedBy: [judgment-engine-implementer]
  - agent: agent-stage-evaluator-template
    role: contract-verifier
    stage: evaluator
    type: Worker
    lifecycle: temporary
    responsibility: >
      S5 独立验证——判定 S3/S4 落盘结果：feedback 四条红线未被破坏；镜像与框架源一致（不手改镜像）；
      tests/contract/ 下的结构契约测试先红后绿并留红先行取证；每个 stage 的产物过实质下限
      （字节下限或声明范围可检索），不以桩文件充当完成；SI-2 的 /better-harness 悬空引用已处置。
      判定对象是业务制品（落盘的定义文件与测试结果），故为 evaluator 阶段的 Worker，不是 Meta。
      不用 skill-verifier：其容量是「审技能执行证据」，窄于本席所需的红线/镜像/契约三类判定。
    blockedBy: [passive-trigger-wirer, active-trigger-author]
config:
  handoff_protocol: file-path-only
  progress_file: .specify/teams/.work/session-driven-self-improvement/progress.md
  failure_strategy: retry-then-halt
  per_handoff_verification: true
  max_retries: 2
  dag:
    - { stage: judgment-contract-designer, blockedBy: [] }
    - { stage: judgment-engine-implementer, blockedBy: [judgment-contract-designer] }
    - { stage: passive-trigger-wirer, blockedBy: [judgment-engine-implementer] }
    - { stage: active-trigger-author, blockedBy: [judgment-engine-implementer] }
    - { stage: contract-verifier, blockedBy: [passive-trigger-wirer, active-trigger-author] }
  summary:
    enabled: true
    every: 1
    delivery_dir: .specify/goal/session-driven-self-improvement/summary/
    interactive: false
---

## Goal

**权威定义**：`.specify/goal/session-driven-self-improvement/goal.md`（`goal_slug` 引用，非内容副本）。以下为本团队视角的渲染，与定义冲突时以定义为准。

终态是框架中有一套 improve 流程，含两个方面：**主动触发**（通过 improve 命令）与**被动触发**（通过运行判定的结果触发 feedback 流程）。本目标只**建立**该流程，不**进行**提升。

### 本团队承接的四项细节（D9）

这四项在 `/speckit.goal` 收窄终态时被刻意从 `## Objective` 移出（决策 D9，账本：`.specify/memory/session/2026-10-05-goal-session-driven-self-improvement-interview.md`），由本团队承接。D1 全文仍逐字保存在 goal.md 的 `## History`，但那是 dated record，不作为当前现实被引用 —— 故在此落为团队的可执行输入。

1. **证据来源（三个）** — Session 历史记录（`.specify/memory/session/`）、用户输入、大语言模型调查结论（`.specify/memory/evidence/`，106 文件，MUST 走摘要/字段投影）。三者是运行判定的读取面，由 S1 契约规定各自口径。
2. **主动流程的内部形状 why → what → how** — why：当前的问题是什么（如 token 消耗过多、耗时过长、问题没有解决、用户不满意），即为什么要触发自我提升，由 session 历史获取；what：需要进行哪些提升，分析哪些方面需要提升；how：该如何进行提升 —— 分析问题、探索思路、实施改造。**这三段是主动 improve 流程自身的内部结构，不是本团队的 stage 计划，也不是 Goal 的 Target**（D3 裁定：阶段不进 Goal，`goal-definitions.md` 属性 2 不改）。本团队的 stage 是「建立这套流程」的工序，与流程内部的三段不同轴。
3. **被动模式的约束** — 被动触发不得面面俱到，以免干扰当前流程；超出当轮处置范围的发现，经新建 spec 或 todo 记录，留待主动触发处置。落点由 S3 承接。
4. **开放范围集合** — 提升对象包括但不限于命令、skills、memory。这是一个开放集合，登记在 frontmatter 的 `territory.non_path`（`type: scope-set`）而非 `write` 路径里 —— 因为它不是文件形状，且命令与 memory 今天在 SI-4 路由表里无归口，归口方式由 S1 契约决定。

### 四量口径裁定（B1–B4，2026-10-06，用户裁定）

本节是 S1 契约的**已定输入**，不是待议项。S1 MUST 据此撰写，MUST NOT 重新发明。

**B1 — 名称已定**：机制名为 **运行判定 (Run Determination)**，经用户批准通道定名。详见 `territory.non_path` 的 `type: naming` 与 `.specify/memory/glossary.md` 的 `运行判定` 词条（`origin=user`、`status=confirmed`）。S1..S5 的产物标识符、引擎文件名、字段名一律用此名。

**B2 —「正确性」拆两半，只做第一半**：

- **制品正确性（程序可判定，本轮实现）** — 口径 = 本 run 声明的检查里，**名字级失败集差集为空**，且每条返回绿的检查都留有**红先行取证或变异演练**。三件机械均已存在，不新造：`scripts/bash/run-tests.sh --names-out <file>`（第 22、29 行）产出排序后的 FAILED nodeid 列表，配合 `comm -13 baseline current` 求差；`red-first-evidence.md` 已在 051 / 052 / 053 三个特性目录实际存在；引擎退出码表全仓一致（0 / 2 / 3 / 4）。真源：`.specify/memory/glossary.md` 的 `名字级基线`、`Red-First 取证`、`变异演练` 三条。
- **语义正确性（不可程序判定，本轮不做）** — 「有没有答对用户的问题」这一类。要么交 LLM 评审、要么交指名人工评审；两者都合法（人工评审是同等形式的判据），但**破坏 Program-First**。若将来要做，MUST 作为**独立一轴**显式声明，MUST NOT 与制品正确性混进同一个数 —— 混了就无法打分。
- **边界（诚实声明）** — 只覆盖**声明了检查**的 run。未声明检查的 run 在这一轴 MUST 报 `not-evaluated`，**MUST NOT 报 `ok`**（与 053 已确立的 `NOT_EVALUATED` 口径、`run-checks` 对 check 2/3/4 的处理一致：未被评估的检查报绿与通过不可区分）。

**B3 — 满意度规则存活，改两处**：

1. **删掉「大部分情况」** —— 那是个对冲词，程序需要的是决策规则而不是概率表述。改为无条件规则，或给出可判定的例外条件（本裁定选后者，见下）。
2. **保留默认接受，加一条窄例外** —— 换话题 / 结束 session 仍默认视为接受（这是压低噪声底、让被动触发可用的要点，不可整个换成 `not-evaluated`，否则满意度轴长期无输入、机制等于不触发）；但若该换话题或结束**紧邻一个未解决的红**（某引擎非零退出，或某个已上报而用户始终未回应的异常），则记 `not-evaluated` 而非接受。
   - **不需要新存储**：`proactive-trigger` 每回合已写一行遥测到 `.specify/memory/trigger/telemetry.jsonl`（默认窗口 200 回合、追加即截断），「本回合是否存在未解决的红」是可导出的，MUST NOT 为此新建平行状态。
   - **已知代价（用户知情采纳）**：这条例外使满意度依赖正确性轴，四个量不再互相独立。若将来要解耦，把触发条件收窄到「仅引擎非零退出」—— 耦合更弱，但堵不住「上报了异常、用户没回应就换话题」那一类。

**B4 — `templates/commands/improve.md` 写权归本团队**：详见 `territory.non_path` 的 `type: cross-goal-write`。对方团队的排除条目已落盘，故 S4 照常交付薄壳本身，不再降级为「只交技能 + 薄壳规格」。

> **待办（不在本团队权限内）**：goal 定义的判据文本仍写「一套新的**判断逻辑**」、objective 仍写「通过**判断逻辑**的结果触发 feedback 流程」—— 二者都需经 `/speckit.goal` modify 采纳新名「运行判定」，并按 B2 收窄「正确性」。本团队 **MUST NOT** 写 `goal.md`：它在 `territory.forbidden` 内，且 `/speckit.goal` 是 goal 归档的唯一作者入口。在该修正落地前，本文件与 goal 定义之间存在一处**已知的术语分歧**，以本节的用户裁定为准。

### 判据

以 goal 定义为准，本文件不复述其文本（判据权威规则）。团队级只声明度量口径：判据按程度测，不渲染成二值勾选框；可用的程度读数是四个量中实际收归同一运行判定的数目（0→4）。**注意：goal 定义当前没有任何条款说明 `achieved` 如何判定**，这是本团队无法自行补齐的缺口，需经 `/speckit.goal` modify 由人裁定。

## Static Structure

Role × Stage × Type（Type 按**写目标**判定，不按 stage 名判定）：

| Role | Stage | Type | Lifecycle | 写目标（决定 Type） |
|------|-------|------|-----------|---------------------|
| team-supervisor | meta | **Meta** | persistent | canonical 定义文件 + 团队配置 → 必为 Meta |
| judgment-contract-designer | executor | Worker | temporary | 工作区补丁 |
| judgment-engine-implementer | executor | Worker | temporary | 工作区补丁 |
| passive-trigger-wirer | executor | Worker | temporary | 工作区补丁 |
| active-trigger-author | executor | Worker | temporary | 工作区补丁 |
| contract-verifier | evaluator | Worker | temporary | 验证记录（判定业务制品，不写 agent/skill/team 定义） |

**为什么必须有唯一 Meta**：本团队交付物是**定义类文件**（命令模板、workflow 规范、instructions 模板、引擎、契约测试）。按 `references/conceptual-model.md` § 消解条款，此时「每席皆 Worker」不成立 —— Worker 只产补丁到工作区，canonical 落盘由唯一 Meta supervisor 执行，Worker MUST NOT 直接写 canonical 定义文件。

## Dynamic Structure

**Pattern：serial（质量优先）** —— 派生依据（`references/patterns.md` 决策树，逐问留痕）：

- **Q1 长期/按 cadence？否。** 工作主体是**一次性交付物改动**（建立一套流程），长期性只体现在 goal 不设终止阈值 —— 该长期性由 Goal lifecycle 承载，不由团队形态承载。误判为 continuous 会强制 L1 起步（仅报告、不派 worker），有界交付工作于是停在报告态。
- **Q2 子任务独立、无共享可变态？否。** 各阶段共享同一批制品：运行判定契约、feedback 接线、instructions 模板。
- **Q3 严格序列（A 的输出喂 B 的输入）？是。** 契约 → 引擎 → 两个触发器 → 验证。→ **Serial Chain**。
- 非「优化」类 goal：本目标是**能力建立**（造一套流程），不是把某个既有制品从 A 提升到 B，故不设 `optimization_target` / `co_targets`。
- **preset 匹配**：`match-team-preset.py --goal "<终态+四项细节>"` → `confidence: none`，`matches: []`（扫描 2 个 preset）。无 preset 可复用，roster 与 pattern 均由 goal 派生。

**DAG**（已验无环，拓扑序 = S1 → S2 → {S3, S4} → S5）：

```mermaid
graph LR
  S1[judgment-contract-designer<br/>运行判定契约] --> S2[judgment-engine-implementer<br/>运行判定实现]
  S2 --> S3[passive-trigger-wirer<br/>被动触发接线]
  S2 --> S4[active-trigger-author<br/>主动触发命令]
  S3 --> S5[contract-verifier<br/>独立验证]
  S4 --> S5
  SUP[team-supervisor · Meta<br/>派发 / 交接门 / canonical 落盘] -.-> S1
  SUP -.-> S2
  SUP -.-> S3
  SUP -.-> S4
  SUP -.-> S5
```

**Stage 定义**（| Stage ID | Agent Kind | Task | Inputs From | Outputs | Blocked By | Quality Gate |）：

| Stage ID | Agent Kind | Task | Inputs From | Outputs | Blocked By | Quality Gate |
|----------|-----------|------|-------------|---------|------------|--------------|
| judgment-contract-designer | executor | 运行判定契约：四个量的判定口径与输出形态、三个证据来源的读取面与摘要口径、两个触发器各自的消费点、对 feedback-step 三层无名判断的推广方式、命令与 memory 的 SI-4 归口 | goal.md、interview 账本、`shared/workflow/feedback-step.md`、`shared/workflow/self-improvement-workflow.md` | `.specify/teams/.work/session-driven-self-improvement/outputs/judgment-contract.md` | — | 契约同时点名四个量与三个来源，且为被动/主动各指明一个消费点；四量口径与「四量口径裁定」小节逐条一致（正确性只做制品正确性、满意度含窄例外、名称用运行判定），MUST NOT 重新发明；命令与 memory 的归口有明确结论或明确记为待定并说明由谁裁定 |
| judgment-engine-implementer | executor | 按契约把固定规则判断实现为 `scripts/python/` 下的确定性程序 + 单测 | judgment-contract.md | `.specify/teams/.work/session-driven-self-improvement/outputs/engine.patch`、`outputs/engine-tests.patch` | judgment-contract-designer | 程序可判定（非 LLM 估读）；对 evidence/ 的读取走摘要而非原文转储，产物中可检索到该口径的声明 |
| passive-trigger-wirer | executor | 运行判定结果 → feedback 流程的接线补丁，含被动模式「不得面面俱到、超出者落 spec/todo」的约束 | judgment-contract.md、engine.patch | `.specify/teams/.work/session-driven-self-improvement/outputs/passive.patch` | judgment-engine-implementer | 四条红线逐条对照未被破坏（尤其 never-solicit 与零自动传输）；改点落为 sensor 而非平行干预台账；约束条款可在补丁中检索到；**落盘前跑 `python3 scripts/python/scan-confirmation-gates.py` 且 total ≤ 23**（本文件落在 SCAN_DIRS 内，预算余量 0） |
| active-trigger-author | executor | `templates/commands/improve.md` 薄壳 + 承载逻辑的技能侧文本，实现 why → what → how | judgment-contract.md、engine.patch | `.specify/teams/.work/session-driven-self-improvement/outputs/active-command.patch`、`outputs/active-skill.patch` | judgment-engine-implementer | why/what/how 三段各有落点且消费运行判定引擎；命令文本为入口+委派（无实现细节内联），且**逐个记录被调用技能的输入与产出**，完整符合 command-logic-as-classified-skills T-003 原文（「每个技能的输入和产出」子句于 2026-10-07 补齐，此前四处渲染均漏；对方团队 S3 已裁定跳过 improve.md，故本 gate 是该文件唯一的 T-003 判定门）；**落盘前跑 `python3 scripts/python/scan-confirmation-gates.py` 且 total ≤ 23**（templates/commands 在 SCAN_DIRS 内，预算余量 0）；技能侧落点名经 S1 契约定下后，MUST 先经 `/speckit.team` modify 把该**具名**目录追加进本团队 write **并**在对方团队 forbidden 中排除它，才可派发第二次累积 —— 对方 write 含 `skills/*/SKILL.md`、`skills/*/references|templates|scripts/**`，与本团队将来的具名技能目录构成**已知的前向冲突**，处置路径与 improve.md 同（用户授权 + forbidden 排除），MUST NOT 静默双写 |
| contract-verifier | evaluator | 独立验证 S3/S4 落盘结果 | passive.patch、active-command.patch、active-skill.patch、progress.md | `.specify/teams/session-driven-self-improvement/runs/<UTC>-verification.md` | passive-trigger-wirer, active-trigger-author | 见 Verification 口径（回归数字注明全量/子集；既存失败走同口径 A/B 差集归因；One-Source-Of-Truth 类验收从落盘产物反查） |

**粒度声明**（`references/patterns.md` § Serial Chain → Stage granularity discipline，落盘前已按文件计数校验）：

- 计数依据（程序步骤，非估读）：`templates/commands` 25 · `scripts/python` 39 · `shared/workflow` 14 · `shared/guidelines` 13 · `shared/definitions` 10 · `shared/patterns` 4 · `agents` 2 · **`skills` 13687**。
- **`skills/` 的 13687 文件是本表唯一的规模风险**：故 `territory.write` 不含 `skills/**`；S4 若需在技能侧落文本，其目录名由 S1 契约决定后，经 `/speckit.team` modify 追加**具名**技能目录，MUST NOT 以 `skills/**` 通配承接。
- **`active-trigger-author` 由 2 次派发累积**（N=2）。依据：`command-logic-as-classified-skills` T-003 要求命令只保留入口与委派、实现细节落技能侧，故交付物天然是两个制品（命令薄壳 + 技能文本），一次派发无法同时承载两种任务类型。派发载荷 MUST 带 `incremental_landing` 字段。**累积不是 retry**：本链 `max_retries: 2` 只承载失败恢复，MUST NOT 用 retry 预算承载这 2 次累积。
- **一个 stage 一种任务类型**：S1 设计 / S2 实现 / S3 接线 / S4 撰写 / S5 验证，互不混装；attribution 与 reconciliation 未同 stage。

**Handoff**：file-path-only —— 下游只收路径清单，不接收文件内容；下游 MUST NOT 修改上游产物。

**每交接验证**（serial 的强制门，保持轻量）：验证本步产物满足下游 `inputs_from` 契约，而非重跑全量评估。失败时按 `retry-then-halt`：产物缺失/agent 崩溃 → retry（≤2）；质量门轻微失败 → 对产物调 `improve-agent`；质量门严重失败 → halt 并报告。

**Substance floor**：`outputs exist` 是必要非充分 —— 桩文件同样「存在」，同样能解锁下游。每个 stage 的 VALIDATE MUST 至少跑一条程序可判定检查（字节下限，或声明范围目录名在产物中可检索）。S5 声称「整批完成」时 MUST 附 ≥2 个实读文件的证据（路径 + 从该文件读到的具体事实），MUST NOT 以产物条目数或子代理自述充当覆盖度。

**Progress**：`.specify/teams/.work/session-driven-self-improvement/progress.md`（stage 表 + Handoff Log）。跨 session 续跑时先解析该表，从第一个未完成 stage 继续。

**Summary 边界**：每个 stage 交接验证通过后刷新 goal summary，交付目录 `.specify/goal/session-driven-self-improvement/summary/`（由 `goal_slug` 派生，不由团队 slug 派生）；门序为 Budget → Cadence → Material → Overlap，两次交接紧邻时合并为一次刷新；有界 pattern 默认 `every: 1`。首次刷新需声明 summary 机制已激活及其生效 cadence。

## Self-Improvement Contract

- Subject: this persisted team definition; member executions are evidence.
- Observe: completed run reports and Post-Run Critique.
- Improve: follow `.specify/shared/workflow/self-improvement-workflow.md`; route through `improve-team`.
- Boundary: preserve team authority, maturity gates, budget, kill-switch, and verifier independence.
- Verify: validate now and wait for a comparable later run before claiming improvement.
