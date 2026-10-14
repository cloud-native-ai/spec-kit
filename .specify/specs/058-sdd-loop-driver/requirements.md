# Requirements Specification: 无人值守 SDD 循环驱动机制（Unattended SDD Loop Driver）

**Requirement Branch**: `[058-sdd-loop-driver]`  
**Created**: 2026-10-14  
**Status**: Draft  
**Input**: User description: "特性输入：/tmp/sdd-loop-team-brief.md（无人值守 SDD 循环驱动机制，建议短名 sdd-loop-driver）。目标仓库：/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit。简报 §7 G1–G6 为用户已拍板裁决，访谈一律直接采纳。"

## Related Feature *(mandatory)*

<!--
  ACTION REQUIRED: Keep the default values as "Need clarification" in the initial draft.
  /speckit.clarify must resolve this section to the final Feature binding before planning.
-->

**Feature ID**: Need clarification  
**Feature Name**: Need clarification

## Overview

在 spec-kit 框架中新增一套**可复用、跨项目、无人值守**的「SDD 循环驱动」机制：以一条**一遍性提示词**驱动主代理完成「登录环境 → 以 qodercli 为子代理 → 按阶段推进 SDD 全流程 → 合并 main」的完整闭环，全程循环自推进，不需要用户逐次提醒「重试」或「继续」。入口话术只声明**目标与起点**（哪个项目、断点在哪、终态权威文档），执行细节全部由机制内部承接。

**定性**：这是 spec-kit 框架的能力补全需求——把 2026-10-14 在多个项目里被反复手工验证有效的驱动模式，固化为**一等公民机制**，使任何项目都能一键发起无人值守的 SDD 推进。

**承载形态（G1/G2 裁决，见 Clarifications）**：机制主体由 **Team** 承载——自迭代环（iteration pattern）+ 独立 verifier + budget/cadence，这是无人值守的三个硬需求（自迭代、阶段校验、卡死处置）的原生能力面；知识层退居 **Skill**——阶段提示词模板、五大执行机制、已验证变体、纪律条款固化为手册（skill），供 team 成员引用。知识归 skill、无人值守运行归 team；单 skill（循环纪律靠模型自觉、长跑后断环）与单 agent（本模式的工人已是远端 qodercli，跨项目并行 + 循环编排不是单 agent 形态）均不满足硬需求——选型对比全文见需求简报 §6，此处不再复述。

**来源**：2026-10-14 从本机全天会话历史（84 个会话段 / 67 个有效会话）提炼；代表执行包括 profiles-04 一条提示词并行驱动两条线全程无提醒、isv-substrate 本地 loop 驱动远端容器内 qodercli 约 6 小时持续推进（长时无人值守已实证可行）、xuanji-images 两条 SDD 线并行全链路沉淀的并发隔离/窄读法授权/审后提交纪律、profiles-12 用户明确表达的循环诉求原话（「需要使用一个循环来完成这项工作，而不是每次由我提醒你『重试』或者『继续』」）。

### 现状锚点（以源码实测为准，2026-10-14）

- 团队预设现有 2 个：`capability-arena`、`project-cluster`（`skills/internal/create-team/templates/teams/`）；预设机制真源为 `skills/internal/create-team/references/team-presets.md`（preset_id / pattern ∈ {parallel, serial, iteration, continuous} / signals / config / provenance 契约）。**无任何 SDD 流程驱动类预设**。
- 外部子代理派发已有可见性契约：`.specify/shared/definitions/subagent-definitions.md` External Dispatch Visibility Contract（明令禁止 `qodercli -p "<prompt>" > agent.log 2>&1 &` 缓冲至退出式派发），参考实现 `skills/internal/create-team/scripts/dispatch.sh` + `stream-filter.py`（`DISPATCH_CLI` 缺省 `qodercli`）。
- 确认门控：**push / force-push / 远程分支操作在破坏性动作清单**（`confirmation-gates.md` § 破坏性动作清单第 3 条）——任何远程推送属门控对象，与 G5「不要 push（除非明确授权）」一致。
- 六阶段命令模板齐备：`templates/commands/` 下 `requirements.md` / `clarify.md` / `plan.md` / `tasks.md` / `implement.md` / `review.md` 全部存在。
- 名字核验：全仓 grep 无 `sdd-loop` / `sdd_loop` 占用；预设 id、skill 名、阶段尾标后缀 [[STR-001]] 均无既有占用（reserved identifier check 通过）。
- 编号空间：`.specify/specs/` 现至 056（无 `.archive/`），带编号分支仅 `048-derive-command`；下一编号 057。**改号记录（2026-10-14）**：上游 057-decompose-command-skills 先行合入占用 057，本特性 rebase 时依 feature-integration.md「Never create duplicate Feature IDs」（框架不支持同号不同名：features/<ID>.md 按裸编号键控、detect-feature-context.sh 仅取数字前缀）改号为 058，规格目录与本分支名同步改名。
- 相邻既有机制（均不承载本能力）：039 P10 Loop Card（技能/团队模板内的循环纪律卡，无派发与校验面）、039 P12 implement 长跑模式（单命令进程内循环，非跨项目外部子代理编排）、`project-cluster` 预设（continuous 巡检协作，不驱动 SDD 阶段链）。

### Assumptions

- **子代理 CLI**：qodercli 为缺省子代理（入口话术明示），但机制不把它硬编码为唯一——遵循框架既有派发抽象（`DISPATCH_CLI` 可覆盖）；本地拓扑即主代理本机直驱 qodercli。
- **收尾哨兵**：合并 main 完成以 `MERGE-DONE` 尾标标记——简报只定义了 `<STAGE>-DONE` 阶段哨兵，合并是阶段链（[[STR-002]]）之外的收尾步，沿用同一哨兵约定（informed guess，实现期可修正）。
- **默认预算与节奏**（G1 要求 preset 携默认值；简报未给数值，按相邻先例 informed guess，全部可经入口覆盖）：阶段超时缺省 90 分钟（isv-substrate 约 6 小时 / 34 turns 的多阶段实测，单阶段为数十分钟量级）；同阶段重试上限缺省 2 次（承 039 P12 两振停滞先例）；预算降级语义沿用 `project-cluster` 形态（on_80pct report-only / on_100pct halt）。
- **skill 分类标注**：本特性新增 skill 按 `internal` 处理（它编排 spec-kit 自身的 SDD 流程，与 spec-kit 语义强耦合；分类定义见 glossary「技能分类标注」条），最终以 plan 阶段裁决为准。
- **Feature 登记**：按用户指令，本特性于 requirements 阶段先行落册（features.md Draft 行 + 详情文件）；spec 内 `Related Feature` 仍按 create-requirements 缺省值保留，由 `/speckit.clarify` 复核确认绑定。
- **review 未过的循环语义**：review 阶段判定未通过 = 该阶段未完成，按重试语义回到修复（受重试上限约束），达上限后走卡死处置上报，不无限返工。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 一遍性入口驱动远端项目 SDD 全流程闭环（含断点续跑默认） (Priority: P1)

用户给出一条一遍性提示词（下面的话术形态，来自需求简报 §3 模板）：

```text
使用SDD开发模式推动 <项目A> 和 <项目B> 模块的特性开发。

1）针对<项目A>：通过 ssh root@<workspace别名A> 登录环境，然后使用 su develop 用户，
   驱动 qodercli 作为子代理，在 /cws_work/<项目A> 项目中推动项目逐步向终态演进
   （终态文档 /cws_work/<项目A>/docs/design/target-state.md）。先选取一个终态切片作为需求，
   在子代理中执行 /speckit.requirements 创建，然后驱动子代理依次完成
   /speckit.clarify -> /speckit.plan -> /speckit.tasks -> /speckit.implement -> /speckit.review，
   然后再合并到 main 分支。

2）针对<项目B>：通过 ssh root@<workspace别名B> 登录环境，然后使用 su develop 用户，
   驱动 qodercli 作为子代理，在 /cws_work/<项目B> 项目中继续完成 SDD 剩余流程
   （该项目已执行到 /speckit.plan 步骤，从断点续跑），完成后合并到 main 分支。

需要使用一个循环来完成这项工作，而不是每次由我提醒你"重试"或者"继续"。
```

主代理据此实例化 SDD 循环驱动团队：对每条项目线，先做断点探测（G6 默认能力——入口不声明阶段时自动探测），再按阶段链（[[STR-002]]）逐阶段派发远端 qodercli 子代理，阶段完成后自动写下一阶段提示词并续环，直到 review 完成并合并回 main，全程零用户提醒。

**Why this priority**: 这是用户核心诉求的直接落点（profiles-12 原话）与验收主场景（简报 §8 验收方向）；G1/G4/G6 三条裁决共同指向此切片。

**Independent Test**: 在演练环境注入已知断点状态，从一句话入口发起，全程统计用户「重试/继续」类提醒次数并核对各阶段产物与合并结果。

**Acceptance Scenarios**:

1. **Given** 远端目标项目处于已知断点状态（如已完成 /speckit.plan），**When** 用户仅发出一句话入口（不声明阶段），**Then** 机制自动探测断点、从正确阶段续跑直至合并 main，期间无任何用户提醒。
2. **Given** 入口声明了两个目标项目，**When** 机制运行，**Then** 每条线的每个阶段都产出可核对产物（阶段提交、spec 文件、尾标日志），最终汇总各线终态。
3. **Given** 目标项目尚无任何 SDD 制品（首次推进），**When** 入口给出终态权威文档路径，**Then** 机制从阶段链起点（requirements，含切片选取）开始推进而非误判断点。

---

### User Story 2 - 独立 verifier 阶段校验与默认安全纪律 (Priority: P1)

每个阶段的「完成」不由执行者自报：阶段尾标（[[STR-001]]）出现只是必要条件，独立 verifier 还须核验产物（git log 新增阶段提交、spec 文件存在性）与纪律合规，双条件齐备才判定阶段完成并续环。阶段提示词骨架把默认安全纪律（G5）固化进每一次派发：直接执行不要确认、访谈式问题自行裁决并记录假设、只提交本特性产物、既有脏文件不提交不还原、不 push（除非明确授权）。

**Why this priority**: 阶段校验是无人值守三硬需求之一（简报 §6）——没有独立校验，循环会在伪完成上静默推进；G5 纪律是机制默认行为而非可选附件。

**Independent Test**: 构造「尾标在而产物缺」的伪完成样本与「尾标在且产物齐」的真完成样本各若干，verifier 判定结果可由第二位复核者独立复现；对演练全程做 git 审计核对纪律合规。

**Acceptance Scenarios**:

1. **Given** 某阶段子代理输出了完成尾标但未产生该阶段的任何提交或产物文件，**When** verifier 校验，**Then** 判定为未完成，循环不写下一阶段提示词。
2. **Given** 某阶段子代理在推进中遇到本应自行裁决的访谈式问题，**When** 阶段完成被校验，**Then** 该阶段的假设记录存在于其产物或提示词要求的位置，且未发生等待用户的行为。
3. **Given** 目标仓库存在与本项目无关的既有脏文件，**When** 全部阶段跑完，**Then** git 审计显示脏文件既未被提交也未被还原。

---

### User Story 3 - 卡死处置与状态落盘上报 (Priority: P1)

阶段超时、同阶段反复失败、预算触顶时，机制自动重试至上限；达上限后停环、把该线状态落盘（当前阶段、已试次数、证据指针），并向用户出具可处置的上送件（发现什么/为何吃重/已产生的中间产物/可选处置——052 上送件四要素）。循环绝不停留在静默等待，也绝不静默修平异常后继续（快速失败纪律，真源 `shared/guidelines/fast-fail.md`）。

**Why this priority**: 卡死处置是无人值守三硬需求之三——无人值守不是无监督，异常必须转化为可见状态与可处置报告，否则「零提醒」退化为「永久卡死」。

**Independent Test**: 注入超时与反复失败两类异常场景，观察重试次数是否恰达上限、状态是否落盘、上送件四要素是否齐备、循环是否停止推进该线。

**Acceptance Scenarios**:

1. **Given** 某阶段子代理持续超时，**When** 达到重试上限，**Then** 机制停止该线推进、状态落盘、上送件产出，且不静默丢弃已产生的中间产物。
2. **Given** 预算在中途触顶，**When** 降级语义生效（on_80pct / on_100pct），**Then** 行为与 preset config 声明一致且对用户可见。
3. **Given** 一次异常被处置完毕，**When** 另一个 Agent 无上下文接手该线，**Then** 仅凭落盘状态即可恢复推进（零上下文可接手）。

---

### User Story 4 - 知识层 Skill 手册固化（G2） (Priority: P1)

阶段提示词骨架（背景与权威文档 / 执行要求 / 完成尾标三段）、五大执行机制（断点探测、阶段化 prompt 文件、runner 与派生、后台执行 + 日志回传 + 轮询、收尾纪律）、已验证变体、纪律条款固化为一个 skill（手册层），供 team 成员与主代理引用。Team preset 引用 skill 而不内联复制行为知识——知识归 skill、无人值守运行归 team（G2 裁决）；新项目/新线的实例化只读手册、只填参数，不改机制。

**Why this priority**: G2 是六条用户裁决之一，且 skill 是本特性两大交付物之一（简报 §8 范围：team 定义 + 配套 skill）；没有知识层，team 成员无提示词骨架可引用，US1–US3 无法按裁决形态运行。

**Independent Test**: 单独核验 skill 存在且四类内容（骨架/五机制/变体/纪律）齐备；核验 preset 与阶段派发引用 skill 而非复制其内容（改 skill 一处即全局生效，无第二真源）。

**Acceptance Scenarios**:

1. **Given** 机制安装完毕，**When** 打开 skill 手册，**Then** 阶段提示词骨架、五大执行机制、已验证变体、纪律条款四类内容齐备且与需求简报 §3–§5 一致。
2. **Given** 需要调整某阶段的提示词骨架，**When** 只编辑 skill 一处，**Then** 后续所有线/所有项目的阶段派发使用新骨架（无散落副本需要逐一修改）。
3. **Given** 一个新目标项目首次接入，**When** 用户只提供入口参数，**Then** 实例化过程不修改机制文件（preset/skill 零改动）。

---

### User Story 5 - 多线并行与并发隔离 (Priority: P2)

多条项目线并行推进：每条线各占一条独立执行流（如各自一条 ssh 流）与各自的任务跟踪条目，互不串扰。多 spec / 多线并行时，机制在提示词中显式声明并发隔离（哪些既有未提交内容不读、不改、不提交）；被隔离项确需追加操作时，经「窄读法授权」显式放行——授权是显式、逐项、有界的，不存在隐式放行。

**Why this priority**: 入口话术（§3 模板）天然含两线并行（项目 A 新切片 + 项目 B 断点续跑），但单线闭环（US1）已独立交付价值；并行是其在多目标场景的扩展。

**Independent Test**: 以两条线并行演练，核对各自的产物、提交与日志按线隔离，无跨线写入；构造一条线触碰另一线隔离项的场景验证窄读法授权的显式性。

**Acceptance Scenarios**:

1. **Given** 两条线并行推进，**When** 各自阶段完成，**Then** 两线的提交、日志、状态互不混淆，任一线的失败不阻塞另一线。
2. **Given** 某线的既有未提交内容被声明为并发隔离项，**When** 该线需要对其进行操作，**Then** 仅在出现显式窄读法授权后操作，且授权范围有界。

---

### User Story 6 - 本地拓扑与已验证变体 (Priority: P2)

同一机制支持两种拓扑与已验证变体（G3）：**本地拓扑**——项目在本机时 qodercli 子代理直接以本地项目为工作目录，需求上下文先写成简报文件（形如 `/tmp/<特性>-sdd-brief.md`），子代理提示词只指示「先完整阅读简报，再执行 /speckit.requirements」（比在提示词里内联全部上下文更稳）；**构建固化变体**——同一主机按角色分线（如一个系统用户在宿主侧项目固化基础设施、另一系统用户在项目目录固化构建配置），两条线分别推进，经入口参数（用户、路径、目标差异）实例化，不新增机制分支。

**Why this priority**: G3 要求两种拓扑都必须支持，但远端拓扑（US1）是原始验证场景；本地与变体是同一机制在参数化后的等价实例。

**Independent Test**: 以本地项目演练一遍性入口闭环（简报文件先行）；以参数化方式实例化构建固化变体并核对两线互不干扰。

**Acceptance Scenarios**:

1. **Given** 目标项目在本机，**When** 发起一句话入口，**Then** 机制以本地直驱方式完成与远端拓扑等价的阶段闭环。
2. **Given** 本地拓扑的首次推进，**When** 机制准备需求上下文，**Then** 上下文先落为简报文件、子代理提示词只指示阅读简报后执行对应阶段命令。
3. **Given** 构建固化场景（同主机双角色分线），**When** 两条线并行推进，**Then** 机制仅经参数区分两线（系统用户、路径、目标），机制文件零改动。

---

### Edge Cases

- 断点探测无法判定（无特性分支、无 specs 目录、无终态权威文档可参照）时，机制停下并上送用户裁定，不猜测起步阶段。
- 目标项目未安装 spec-kit 运行时（无 `.specify/`）时，机制报告并停线等待处置，不自动执行初始化。
- 远端不可达、凭证失效或执行身份不符时，派发前预检失败给修复动作（承 `project-cluster` 派发前预检先例），不裸报错后弃线。
- 子代理 CLI 不存在、不在执行身份的可执行路径或版本不匹配时，预检拦截并给出修复动作。
- 同一目标项目被两条线同时指向时，机制检出写重叠并拒绝第二线（写重叠不得停留在双方都可写）。
- 合并 main 遇冲突时，停线上报冲突详情，不自动强合、不静默丢弃任一侧。
- 完成尾标出现在日志正文（如历史回显）而非本次阶段输出末尾时，verifier 以产物核验为准，尾标仅作必要条件——防止以 grep 尾标判完成的假阳性。
- 轮询日志无限增长时，消费侧按有界窗口（tail）读取，不整读无限日志。
- 预算在阶段中段耗尽时，落状态保留中间产物后停止，不弃中途产物也不继续消耗。
- 用户在循环进行中插入新指令时，当前阶段完成后尊重新指令（循环可中断、可改道），已派发阶段不被半途撕毁。
- 全部阶段已完成但尚未合并 main 时被中断，重入时断点探测命中收尾场景，仅执行合并收尾（G6 收尾场景）。

## Requirements *(mandatory)*

### Functional Requirements

#### 承载与入口（G1/G2/G3/G4）

- **FR-001**: 框架 MUST 新增 team preset [[STR-003]]（落位与契约遵循预设机制真源 `skills/internal/create-team/references/team-presets.md`）：`pattern: iteration`（自迭代环）；成员角色封闭集至少含循环主导者（编排断点探测、阶段派发、续环与收尾）、线执行者（单条项目线的阶段派发载体）、线校验者（独立 verifier，见 FR-015）；config MUST 携带 `verifier: independent`、budget/cadence 默认值（FR-017）与 kill_switch 键。provenance MUST 引用 2026-10-14 实测运行（需求简报 §2 的真实会话记录），满足「预设只从真实运行过的团队蒸馏」的预设契约。
- **FR-002**: 框架 MUST 新增配套 skill [[STR-003]]（知识层手册）：固化阶段提示词骨架（FR-008）、五大执行机制（FR-005/FR-007/FR-010/FR-011/FR-013）、已验证变体（FR-022/FR-023）、纪律条款（FR-008）；team preset 与阶段派发 MUST 引用该 skill 而非内联复制其内容——知识归 skill、无人值守运行归 team（G2 裁决），无第二真源。
- **FR-003**: 机制 MUST 不绑定特定项目族或工作区命名规则：登录别名、登录用户、项目路径、执行身份、终态权威文档路径、断点阶段全部经入口参数声明（G3 裁决）；机制文件（preset/skill）MUST 零硬编码项目名、主机别名或路径。
- **FR-004**: 机制 MUST 以需求简报 §3 的一句话模板为一遍性入口（G4 裁决：入口不变）：入口只声明目标与起点（目标项目、登录方式、断点位置、终态权威文档），不要求用户学新话术，不要求用户声明执行细节。

#### 断点探测与阶段推进（US1）

- **FR-005**: 断点续跑 MUST 是默认能力（G6 裁决）：入口未声明阶段时，机制 MUST 自动探测项目当前所处 SDD 阶段并从该阶段续跑。已验证探测形态（示例）：登录后执行 `git branch --show-current`、`git log --oneline -3`、`ls .specify/specs/`，结合终态权威文档与 specs 目录判定续跑阶段（阶段全集与顺序见 [[STR-002]]）；探测 MUST 覆盖「已到 review 后只剩合并 main」的收尾场景。
- **FR-006**: 断点探测与切片选取 MUST 消费终态权威文档（如入口声明的 target-state.md）：首次推进（无断点）时以它为终态切片的选取依据；探测判定 MUST 在无法判定时停下上送（对应 Edge Case 第 1 条），不得猜测。
- **FR-007**: 阶段推进 MUST 沿阶段链 [[STR-002]] 顺序进行，每阶段把该阶段完整指令经 heredoc 写为远端阶段化提示词文件（形如 `/home/develop/prompt-<项目>-<阶段>.md`），再经 runner 派发（FR-010）——提示词不内联进命令行，落文件后引用（已验证形态）。
- **FR-008**: 阶段提示词 MUST 遵循固定三段骨架（固化于 FR-002 的 skill）：① 背景与权威文档（终态文档 / 宪法 / 上一阶段提交号）；② 执行要求（G5 默认纪律）：直接执行不要确认、访谈式问题自行裁决并记录假设、只提交本特性产物、仓库既有脏文件不提交不还原、不要 push（除非明确授权）；③ 完成尾标要求：最后一行输出 `<STAGE>-DONE`（后缀 [[STR-001]]）。
- **FR-009**: 每阶段完成判定 MUST 消费阶段尾标：子代理提示词要求其最后一行输出大写阶段名 + [[STR-001]]（如 PLAN-DONE）；尾标是阶段完成的必要条件（充分条件由 FR-015 的独立校验补齐）。
- **FR-010**: 阶段执行 MUST 经 runner 脚本派发，已验证形态（示例）：runner 内容为 `cd /cws_work/<项目> && qodercli -w /cws_work/<项目> --permission-mode auto -p "$(cat /home/develop/prompt-<项目>-<阶段>.md)"`；下一阶段 runner MUST 由上一阶段 runner 经文件名替换派生（如 sed 替换提示词文件名），避免重复维护整套脚本。
- **FR-011**: 阶段执行 MUST 后台化并以日志轮询驱动续环（已验证形态）：远端经 `ssh ... "su - develop -c 'bash /home/develop/run-<项目>-<阶段>.sh'"` 把输出回传到本地日志文件，主代理轮询日志尾部，出现完成尾标即进入校验（FR-015）与下一阶段派发（FR-012）；派发形态 MUST 遵守既有 External Dispatch Visibility Contract（真源 `.specify/shared/definitions/subagent-definitions.md`）——禁止缓冲至退出、进度不可见的派发（该契约四观测点到 ssh + su 远端形态的映射在 plan 阶段核对）。
- **FR-012**: 阶段完成经校验通过后，机制 MUST 立即写下一阶段提示词并派发（自迭代），不等用户任何形式的「继续」指令（G1 裁决：自迭代）。

#### 收尾（US1）

- **FR-013**: 每条线 MUST 以合并回 main 收尾（review 完成后）；**push 与远程分支操作缺省不执行**——它们属确认门控破坏性动作清单（真源 `confirmation-gates.md`），仅当入口显式授权 push 时才推送特性分支到远程再合并（G5 裁决：不要 push 除非明确授权；需求简报 §4.5「推特性分支到 origin 再合并」的缺省读法据此修正，本地合并为缺省收尾）。
- **FR-014**: 全部线收束后，机制 MUST 向用户汇总各线终态（每线：终态阶段、合并结果、遗留异常与证据指针）——无人值守结束于一份可处置的汇总，而非沉默。

#### 独立校验（US2）

- **FR-015**: 阶段完成判定 MUST 由独立 verifier 执行，不靠执行者自报（G1 裁决：阶段校验）：判定条件 = [[STR-001]] 尾标出现（FR-009）+ 产物核验（git log 新增该阶段提交、该阶段 spec 文件存在性）+ 纪律合规抽查（FR-008 的执行要求段未被违反），多条件同时成立方判完成。
- **FR-016**: verifier 判据 MUST 可被第二位复核者独立复现（承 052 异常分流的可复现性要求）；「尾标在而产物缺」的伪完成 MUST 判未完成——判据以产物为准，[[STR-001]] 尾标仅是必要条件（对应 Edge Case 第 7 条）。

#### 卡死处置（US3）

- **FR-017**: preset config MUST 承载卡死处置四类缺省值键并可经入口参数覆盖：阶段超时（缺省 90 分钟）、同阶段重试上限（缺省 2 次）、预算（budget：单线阶段推进上限与每日上限，降级语义沿用 on_80pct report-only / on_100pct halt 形态）、节奏（cadence：连续循环模式的轮询间隔与空闲上限）；数值为 informed guess（见 Assumptions），plan 阶段可修正。
- **FR-018**: 异常处置 MUST 对齐快速失败纪律（真源 `shared/guidelines/fast-fail.md`）：达重试上限后停环、落线状态、出上送件（052 上送件四要素：发现了什么 / 为何吃重 / 已产生的中间产物逐项可定位 / 可选处置）；MUST NOT 静默等待、MUST NOT 静默修平异常后继续。
- **FR-019**: 线状态 MUST 落盘为状态脊（当前阶段、已试次数、断点判定、证据指针），跨阶段持久、零上下文可接手（承 `project-cluster`「状态脊是跨周期唯一记忆」约束）——循环 MUST NOT 依赖会话记忆续环。

#### 多线并行（US5）

- **FR-020**: 多条项目线 MUST 可并行推进：每线各占一条独立执行流（如各自一条 ssh 流）与各自的任务跟踪条目；任一线的失败不阻塞其他线。
- **FR-021**: 多 spec / 多线并行时，机制 MUST 在派发提示词中显式声明并发隔离（哪些既有未提交内容不读、不改、不提交）；被隔离项确需追加操作时 MUST 经「窄读法授权」显式放行——授权显式、逐项、有界，不存在隐式放行。

#### 变体与拓扑（US6）

- **FR-022**: 本地拓扑 MUST 支持：项目在本机时 qodercli 子代理直接以本地项目为工作目录；需求上下文 MUST 先写成简报文件（形如 `/tmp/<特性>-sdd-brief.md`），子代理提示词只指示「先完整阅读简报，再执行对应阶段命令」——不把全部上下文内联进提示词（已验证变体）。
- **FR-023**: 构建固化变体 MUST 经参数实例化：同一主机按角色分线（不同系统用户在各自目录固化不同层，如基础设施侧与构建配置侧），机制仅经入口参数（执行身份、路径、目标差异）区分两线，MUST NOT 为变体新增机制分支或硬编码角色名。
- **FR-024**: 机制 MUST 完成注册面与文档面同步：preset 与 skill（[[STR-003]]）进入既有预设/技能注册与匹配机制（`match-team-preset.py` 的匹配面），docs 参考面增补机制说明（双拓扑实例化指引）；注册与文档同步方式遵循框架既有传播机制，不新建传播器。

### 显式排除项（Out of Scope）

以下各项**显式排除**在本特性范围之外（需求简报 §8）：

- **不实现任何具体业务项目的推进**——具体项目（如某业务仓库的特性开发）是本机制的使用场景与验收演练载体，不是交付物。
- **不改动 spec-kit 现有 requirements / clarify / plan / tasks / implement / review 各技能与命令的内部流程**——机制只编排它们的调用次序与派发形态，不修改其内部行为。
- **不引入对特定 workspace 命名规则的硬编码**——登录别名、用户、路径、断点阶段全部入口化（FR-003），机制对任何命名规则的目标环境均可实例化。
- **不新增 push 自动化**——push / 远程分支操作维持确认门控破坏性分类（FR-013），机制不提供绕过该门控的缺省自动化。

### Key Entities *(include if requirement involves data)*

- **循环驱动团队（Loop Driver Team）**：preset [[STR-003]] 的实例，承载自迭代环运行；成员含循环主导者、线执行者（每线一个）、线校验者；config 携带校验/预算/节奏默认值。
- **项目线（Project Line）**：一条目标项目的一次无人值守推进；属性含登录参数、项目路径、终态权威文档、断点判定结果、当前阶段、已试次数；多线并行时彼此隔离（FR-020/FR-021）。
- **断点（Breakpoint）**：目标项目当前所处的 SDD 阶段判定；由断点探测（FR-005）产出，含「全部阶段已完成仅剩合并」的收尾形态。
- **阶段提示词文件（Stage Prompt File）**：单阶段的完整指令落盘文件，三段骨架（FR-008）；每阶段一份，随线与阶段命名区分。
- **Runner 脚本（Runner Script）**：单阶段的子代理执行包装；下一阶段由上一阶段派生（FR-010）。
- **线状态（Line State）**：状态脊实体（FR-019），落盘持久、零上下文可接手；卡死处置与重入都消费它。
- **校验结论（Verification Verdict）**：verifier 对单阶段完成判定的可复现结论（FR-015/FR-016），含证据指针。
- **收尾汇总（Final Summary）**：全部线收束后的终态报告（FR-014），逐线给出阶段终态、合并结果与遗留异常。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 以一次真实或演练驱动作验收（简报 §8 验收方向）：一句话入口发起后到全部线收束，用户「重试/继续」类提醒次数 = 0。
- **SC-002**: 断点探测正确率 100%：演练注入 ≥3 种断点形态（含「review 后只剩合并 main」收尾场景与「无任何 SDD 制品」首推场景），判定的续跑阶段全部正确。
- **SC-003**: 伪完成拒绝率 100%：对「尾标在而产物缺」的构造样本，verifier 全部判未完成（变异演练证明校验能红，非恒绿盲检）。
- **SC-004**: 卡死处置闭环率 100%：注入超时与反复失败场景后，机制自动重试恰达上限、状态落盘、上送件四要素齐备，静默等待时长 = 0。
- **SC-005**: 双拓扑等价：同一形态的一句话入口在远端（ssh + su + 远端 qodercli）与本地（直驱）两种拓扑下均完成闭环演练。
- **SC-006**: 纪律合规 100%：演练全程 git 审计显示零越界提交（无关脏文件未被提交/未被还原）、零未授权 push 与远程分支操作。
- **SC-007**: 多线并行零串扰：≥2 条线并行演练中，各线提交、日志、状态按线隔离，跨线写次数 = 0。
- **SC-008**: 跨项目零改动实例化：新目标项目仅经入口参数接入并完成演练，机制文件（preset/skill）改动数 = 0。

### Measurement Sources & Collection Methods

- **SC-001 Source**: 验收演练的会话记录与循环日志——统计入口发出后到收尾汇总之间用户介入次数；验收演练记录归档于特性目录 verification 材料。
- **SC-002 Source**: 演练前注入的断点状态清单与机制断点判定记录逐项比对（判定记录来自线状态落盘，FR-019）。
- **SC-003 Source**: 构造伪完成样本的校验结论记录 + 变异演练取证（破坏产物 → 校验转红 → 复原 → 转绿），结论可由第二位复核者独立复现（FR-016）。
- **SC-004 Source**: 异常注入演练的计时与产物核对——重试计数来自线状态、上送件四要素逐项核对、静默等待以轮询日志与时间戳审计。
- **SC-005 Source**: 两次拓扑各一次演练的闭环记录（各阶段尾标日志 + 合并结果），归档于特性目录。
- **SC-006 Source**: 演练前后 git 状态审计（脏文件清单比对 + 远程分支操作审计）。
- **SC-007 Source**: 并行演练的逐线日志与提交归属核对（每笔提交归属唯一线）。
- **SC-008 Source**: 实例化前后机制文件（preset/skill）的 diff 审计 + 新项目演练闭环记录。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `-DONE` | FR-008, FR-009, FR-015, FR-016, preset（config/骨架引用）, skill 手册（完成尾标哨兵后缀；完整哨兵 = 大写阶段名 + 本值） |
| `STR-002` | `requirements → clarify → plan → tasks → implement → review` | FR-005, FR-007, preset（Dynamic Structure 阶段链）, skill 手册（SDD 阶段链规范顺序） |
| `STR-003` | `sdd-loop-driver` | FR-001, FR-002, FR-024, docs（preset id 与 skill 名共用的机制标识） |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

<!-- 
This section will be populated by /speckit.clarify command with questions and answers.
Format: - Q: <question> → A: <answer>
-->

### Session 2026-10-14

> 本轮访谈的需求输入为需求简报（/tmp/sdd-loop-team-brief.md）；简报 §7 的六条裁决为用户已拍板结论，按用户指令直接采纳、不再发问。以下逐条记录裁决与其落点。

- Q1: 机制承载选型——单 skill、单 agent 还是 team？（简报 §6 三机制对比） → A: **G1 承载机制选 Team**——无人值守是硬约束，机制主体用 team（自迭代环 + verifier + budget/cadence）承载；无人值守的三个硬需求（自迭代：阶段完成后自动派发下一阶段；阶段校验：尾标 + 产物核验由独立 verifier 执行、不靠执行者自报；卡死处置：超时/重试上限/预算/节奏，异常落状态并上报）是选型的决定性约束，单 skill（循环纪律靠模型自觉、长跑后可能断环）与单 agent（本模式的工人已是远端 qodercli）均不满足。**G2 知识层退居 Skill**——阶段提示词模板、执行机制五条、变体、纪律条款固化为 skill 手册供 team 成员引用；知识归 skill、无人值守运行归 team。落点：FR-001（team preset）、FR-002（skill）、FR-012（自迭代）、FR-015（独立校验）、FR-017/FR-018（卡死处置）。
- Q2: 机制是否绑定特定项目族（如 xuanji 系）？ → A: **G3 跨项目通用**——机制不绑定 xuanji 系项目；远端（ssh + su + 远端 qodercli）与本地（qodercli 直驱）两种拓扑都必须支持；参数（登录别名、用户、路径、断点阶段）全部入口化。落点：FR-003、FR-022、FR-023。
- Q3: 用户入口是否需要一套新话术？ → A: **G4 一遍性入口不变**——用户入口就是简报 §3 的一句话模板；机制内部承接全部执行细节，不要求用户学新话术。落点：FR-004。
- Q4: 机制的默认安全纪律是什么？ → A: **G5 安全纪律继承**——阶段提示词骨架中的「只提交本特性产物、既有脏文件不提交不还原、不要 push（除非明确授权）、访谈问题自行裁决并记录假设」必须成为机制的默认纪律。与框架既有门控一致：push 属确认门控破坏性动作清单条目，缺省不自动执行——简报 §4.5「review 后推特性分支到 origin 再合并」的缺省读法据此修正为「本地合并为缺省收尾，push 须经入口显式授权」。落点：FR-008、FR-013。
- Q5: 入口不声明阶段时机制的行为？ → A: **G6 断点续跑是默认能力**——机制必须能自动探测断点并从该阶段继续，含「已到 review 后只剩合并 main」的收尾场景。落点：FR-005、FR-006、FR-019。

> 残留待澄清项：0。全文无活动澄清标记；本轮六条裁决覆盖简报全部开放决策，剩余数值类缺省（阶段超时/重试上限等）以 informed guess 记录于 Assumptions 与 FR-017，属 plan 阶段可修正项而非用户待决项。
