---
name: sdd-loop-driver
description: 无人值守 SDD 循环驱动手册——以一条一遍性提示词驱动主代理完成「登录环境 → 以 qodercli 为子代理 → 按阶段推进 SDD 完整流程（requirements → clarify → plan → tasks → checklist → analyze → implement → review）→ 合并 main」的完整闭环，全程循环自推进、零用户提醒。当用户说「使用SDD开发模式推动 <项目>」「无人值守推进」「sdd-loop-driver」「需要使用一个循环来完成这项工作，而不是每次由我提醒你重试或继续」时加载本手册。执行细节（断点探测 / 阶段化 prompt 文件 / runner 与派生 / 后台执行+统一监听 / 收尾纪律）全部由本手册承接，入口只声明目标与起点。当以本技能名给出功能/改进描述时，视为 SDD 目标（目标项目可为本技能自身所在仓库），先做 U0/U1 并走阶段链，不得就地改代码或切换为技能维护路径。
skill_id: "<SKILL:.specify/skills/sdd-loop-driver/SKILL.md>"
classification: external
---

> **分类注解**：本 skill 依**依赖轴**判定为 external——自身零 spec-kit 依赖、任何宿主 agent 可直接加载（手动放置即可用）；其内容编排 spec-kit 的 SDD 流程（语义耦合在此显式声明），该耦合只体现在它指挥子代理在目标项目中执行 `/speckit.*` 阶段命令，不构成本 skill 的运行时依赖。

## What This Skill Does

把 2026-10-14 起在多个项目被反复手工验证有效的「无人值守 SDD 驱动」模式固化为可执行手册：宿主 agent（不需要安装 spec-kit）加载本手册后，对每条项目线执行「断点探测 → 阶段派发 → 统一监听 → 独立校验 → 续环」的循环，直到 review 完成并合并收尾。三条硬需求——自迭代、独立校验、卡死处置——的运行规则全部内置于本手册（见下文与 references/）。监听语义（等待/监控/轮询/wait/monitor）的唯一权威落点是 `references/watch-model.md`：子代理进程、异步脚本、日志、心跳、退出记录与多线批量共用同一套信号与判定模型。

**触发语义与路由（2026-10-19 修订）**：以本技能名加载并给出功能/改进描述 = SDD 目标；目标项目可以是任意仓库，**包括本技能自身所在的仓库**。改进对象即使是 sdd-loop-driver 本身，也必须走 U0/U1 → 阶段链。只有入口显式声明「只做技能维护、不走 SDD」时，才允许 improve-skills/create-skills 等维护路径；不得因为缺少目标/权威文档等参数而改走别的流程（缺省解析见 When to Load）。

**主导流程唯一**：本技能加载后，本轮主导流程是 SDD 循环；其他技能只能作为被调用工具，不能成为主导流程。**加载后的第一个动作**是写出 U0 入口声明与阶段计划；在此之前不得加载其他技能、不得直接编辑文件、不得派发 subagent。

**完整流程纪律（2026-10-17 修订）**：本手册编排的是**完整版** SDD 流程——`speckit.checklist`、`speckit.analyze`、`speckit.review` 等日常手动开发常被省略的非必须质量门，在无人值守循环中一律必经、不可省略、不可跳阶段（编排与门判据见 dispatch-recipes.md Recipe 4）。

**软协同关系**：本技能与 sdd-project-setup **非强绑定、各自可独立运行**。本技能保留自有的必要 preflight（五族前置检查，见 dispatch-recipes.md）；检查不通过且属框架安装/调协问题时，handoff 给 sdd-project-setup 处置，处置完成后回到循环。sdd-project-setup 调协完成后产出的候选工作清单（未完成 feature / 大改进 feedback / TODO 事项）是本技能建议的输入来源之一，但未经用户或上游流程确认不自动启动循环。

**职责切分线**：框架调协（install/reconcile/verify/候选清单）= sdd-project-setup；SDD 完整阶段循环（含 checklist/analyze 质量门）= 本技能。

## Driver Topology（驱动拓扑——义务真源：run-agent 派发治理）

- **加载本手册的宿主 agent 就是驱动者**：U0–U6（探测/派发/轮询/校验/续环/收尾）全部由加载者在自己的会话里亲自执行，不得委托给任何 subagent。
- **流程不可替换**：加载者不得用 improve-skills/create-skills 等技能维护路径替代 U0–U6；详见 Hard Requirement 7。
- **派发治理义务已上收（analyze C-26）**：子代理提示词不引用驱动/循环技能、不指示加载技能、不含循环逻辑；嵌套驱动禁止、循环层级恒为 1——义务全文与派发前拦截见 `skills/internal/run-agent/SKILL.md` 派发治理节与 `.specify/shared/definitions/subagent-definitions.md` § Dispatch-Time Governance Obligation（本节改为引用，义务本体单一落点）。
- **自检**：若加载本手册时发现自己处于 subagent 上下文且被赋予的任务是「代为驱动循环」，按显式异常行上报并停在前置阶段——嵌套驱动永不是合法形态。
- **两侧环境模型**：本手册（编排侧）与阶段子代理（执行侧）通常运行在不同环境——speckit 框架（specify CLI / `.specify/`）只要求存在于执行侧（目标项目所在环境），编排侧宿主不需要安装 spec-kit、缺之不构成缺口；两侧角色划分、安装归属与误读纠正的真源见 `.specify/shared/workflow/execution-topology.md`（执行拓扑模型）。

## When to Load

- 入口话术只声明**目标与起点**：目标项目（含登录别名/用户/路径）、断点位置（可不声明——机制自动探测）、终态权威文档路径、特性切片（由入口声明或按终态权威文档推导——本技能不自动选题）。
- 宿主环境**无** `.specify/` 也可运行本手册（SC 可移植场景）；仅当子代理要在目标项目执行 `/speckit.*` 阶段命令时，目标项目才需要具备 `.specify/` 结构。
- 本手册**不**适用于：需要用户逐轮拍板的探索式会话（那是访谈模式）；单命令进程内长跑（那是 implement 长跑模式）。

### U0 入口解析（缺省 + 强制自检）

入口可以只给功能描述；缺省按下表解析，**不得因参数不全而切换流程**：

| 入口缺省 | 解析规则 |
|----------|----------|
| 目标项目 | 当前工作目录含 `.specify/` → 当前仓库；否则问一个澄清问题，不猜 |
| 执行拓扑 | 未给 ssh 别名/run-user/远端路径 → 本地直驱；给全 → 远端 |
| 终态权威文档 | 入口功能描述 + 现有 `docs/` + 项目宪法；选择写入 U0 状态脊 |
| 断点 | U1 自动探测，禁止猜测 |
| 特性切片 | 入口功能描述；未给则按终态权威文档推导，本技能不自动选题 |

**U0.5 自检（进入 U2 前必须通过）**：

1. 目标、拓扑、权威、切片、断点是否已写入状态脊？
2. 我是否正准备直接编辑目标仓库？是 → **停下**：这不是 U2 派发，是流程绕过。
3. 我是否正准备加载 improve-skills/create-skills 等维护技能？是 → 除非入口显式声明「只做技能维护」，否则**停下**并回到 U1。
4. 阶段计划（下一阶段 + 派发形态）是否已写出？否 → 先写，再派发。

### 常见误路由（入口 → 正确路由）

| 入口形态 | 正确路由 | 禁止 |
|----------|----------|------|
| 以本技能名 + 功能/改进描述 | SDD 阶段链；目标可为本仓库 | 直接改代码；改走 improve-skills |
| 以本技能名 + 明确「只改技能文档/不走 SDD」 | 技能维护路径 | 强制派发阶段 |
| 纯提问/咨询 | 回答并停 | 自动启动循环 |

## The Loop (U0–U6)

```text
U0 ENTRY     一遍性入口：目标、线、断点（或"探测"）、终态权威文档
U1 PROBE     每线：断点探测（git 分支 + 近期提交 + specs 目录 + 终态文档）判定续跑阶段
U2 DISPATCH  写阶段提示词文件 + runner，后台派发（配方见 references/dispatch-recipes.md）
U3 WATCH     统一监听：单次调用内长轮询信号（退出记录/哨兵/PID/心跳）至终止判定或窗口到期；窗口到期只返回 RUNNING 并立即重入，只有阶段 deadline 产生 TIMEOUT（见 references/watch-model.md）
U4 VERIFY    独立校验：哨兵（必要）+ 产物核验 + 纪律抽查（充分）→ 通过才续环
U5 STALL     超时/重试上限/预算触顶 → 停线、状态脊落盘、出上送件（绝不静默等待）
U6 LEAVE     全线收束：逐线合并收尾（git 状态判定 + 工作树归档清扫，缺省本地合并）+ 一份收尾汇总
```

多条线并行 = 多个独立循环实例：一线一连接、一线一状态脊。**U0.5 线路登记**：首次派发前把该线登记进环境级 Line Registry（`scripts/line-registry.py --action register`），此后每个事件携带 `(line_id, run_id)` 归属信封；U6 收尾后注销（`deregister`）。无标识消息一律经 `resolve-message` 判定，禁止用进程扫描推断线路。

U0 的产物是入口声明（目标/拓扑/权威/切片/断点）与阶段计划；未产出前不得进入 U2，更不得直接编辑目标仓库——目标项目为本仓库时同样适用。

## Hard Requirements

1. **自迭代**：U4 通过后立即派发下一阶段（U2），不等用户任何形式的「继续」。
2. **独立校验**：阶段完成判定不由执行者自报——校验者不是该阶段执行子代理；哨兵在而产物缺 = 伪完成，判未完成。
3. **卡死处置**：达重试上限（缺省 2 次）或阶段超时（缺省 90 分钟）→ 停环、落状态脊、出上送件四要素（发现了什么 / 为何吃重 / 已产生的中间产物逐项可定位 / 可选处置）。
4. **状态脊**：每线状态文件在 U2 派发前、U3 终止判定时、U4 校验后、U5 停线时先写后动；续环与重入只认状态脊，不依赖会话记忆。
5. **驱动者生命周期**：U3 是驱动者当前运行内的有界等待（缺省长轮询窗口，见 `references/watch-model.md`），驱动者必须存活到全线收束或显式停线上送；独立 `sleep` 回合与「挂监视器后等待通知/恢复」都不是合法形态——除非宿主已被探针证明能在通知后自动恢复同一运行（watch-model §6）。会话式宿主中驱动者确须结束时，唯一合法路径是把状态脊写为 stalled/reentry-required 并显式上报（重入是常态路径，程序见 stage-prompts.md）。
6. **驱动拓扑**：加载者即驱动者，亲自执行 U0–U6；阶段执行子代理只收三段骨架提示词；反嵌套义务（不引用驱动/循环技能、不指示加载技能、不含循环逻辑）的真源在 run-agent 派发治理——本手册于 U2 派发前按其自检，全文见「Driver Topology」节。
7. **流程不可替换（no workflow substitution）**：完成 U0/U1 并写出阶段计划前，禁止直接编辑目标仓库；禁止用 improve-skills/create-skills 等技能维护路径替代 SDD 阶段链。目标项目为本技能所在仓库时同样适用。唯一例外：入口显式声明「只做技能维护、不走 SDD」。

## Discipline Defaults

阶段提示词骨架的第二段把以下默认纪律写进每一次派发（全文见 references/stage-prompts.md）：直接执行不要确认、访谈式问题自行裁决并记录假设、只提交本特性产物、既有脏文件不提交不还原、不要 push（除非明确授权）。

## References

- `references/dispatch-recipes.md` — 五大执行机制的命令形态：断点探测、阶段化 prompt 文件、runner 与派生、后台执行 + 统一监听（长轮询窗口/批量多线）、收尾纪律；阶段链与哨兵字面量；派发可见性操作规则；线路登记/归属信封/消息入口（Recipe 6）。
- `references/watch-model.md` — 统一监听模型：信号源、判定状态机、事件优先机制阶梯、窗口与阶段期限的区分、`pgrep -c` 零匹配陷阱、多线 manifest、宿主适配与自测要求；归属层消费规则与重接线快照（§11）。
- `references/stage-prompts.md` — 阶段提示词三段骨架全文、独立校验程序、Line Registration/Envelope/Ingress 程序、重接线/重复启动/orphan/stale/U6 程序、已验证变体（本地简报先行 / 构建固化分线）、多线并发隔离与窄读法授权、卡死处置与状态脊程序。
- `scripts/watch-target.sh` — 无框架依赖的长轮询 watcher 参考实现（单目标/多目标、快照与自测模式、`--line-id/--run-id/--meta` 归属过滤、窗口内 lease 续租钩子）。
- `scripts/line-registry.py` — Python 3 stdlib-only 引擎：环境级 Registry、原子写/同线锁、信封分类、消息入口、所有权/集成队列、lease/reservation/身份校验。

## Boundary

- 收尾动作的合并/push 维持确认门控破坏性分类：缺省本地合并；push 须经入口显式授权。
- 本手册编排阶段为不透明单元：不改 requirements/clarify/plan/tasks/checklist/analyze/implement/review 各命令的内部流程。
- 不绑定特定项目族或工作区命名规则：别名、用户、路径、CLI、断点阶段全部入口参数化。
- 同仓多写线：worktree-per-write-line + Ownership Manifest + 确定性集成队列（单一协调者、每批一次镜像）；规则见 `references/dispatch-recipes.md` Recipe 7 与 `references/stage-prompts.md` Concurrency Isolation。worktree 只在合并成功后移除，未合并/未提交时保留并上送。
- 目标项目未安装 spec-kit（无 `.specify/`）时：**委托 sdd-project-setup** 处置（本技能不执行初始化），处置完成并取得就绪凭证后重入循环。

## Subagent Create & Dispatch Delegation（子代理创建与派发委派）

本手册是**编排者**：它不自带派发机制，而是委派两个承接技能完成驱动子代理的任务（2026-10-16 委派化裁定）：

- **实例创建 → create-agent**（`skills/internal/create-agent/SKILL.md`）：从 `agents/sdd-executor.agent.md` 能力模板按职责实例化阶段执行实例（一实例一职责，`capacity-scope` 引用绑定）；输入=职责声明，产出=`.specify/agents/instances/<slug>.agent.md`。
- **阶段派发 → run-agent**（`skills/internal/run-agent/SKILL.md`）：以 Execution 拓扑声明（本地/远端，见 subagent-definitions § Execution Topology Declaration）+ 实例引用发起执行；输入=实例+拓扑+阶段提示词，产出=执行结果或可见性三元组。前置检查（五族）与失败处置链见其 `references/dispatch-preflight.md`。
- **编排本体在本手册**：阶段序列（U0–U6）、状态脊、哨兵与独立校验、卡死处置、收尾合并——三技能不承接这些（职责切分线见 agent-definitions § Driving Subagents via the Three Layers）。

## Feedback & Probe Points（反馈与探针采集点）

本技能频繁驱动完整 SDD 流程，是 speckit 框架摩擦的最佳观察者——框架级观察 MUST 有落点，MUST NOT 随收尾汇总蒸发。三个采集点（本技能不加新采集机器——状态脊、收尾汇总与既有引擎就是载体，IX）：

1. **每线观察点（U4/U6）**：独立校验与收尾时，把观察到的 **speckit 框架级摩擦**记入该线状态脊的「框架观察」段——结构化三要素：现象 / 框架位置（哪个阶段命令、模板、命令面）/ 对驱动的影响。范围限框架本身（阶段命令行为、模板缺口、哨兵与校验误报）；目标项目的业务问题不属此类。
2. **收尾落库点（U6）**：收尾汇总携带「框架反馈候选」清单（自各线「框架观察」段聚合）。落库形态分两种：宿主工作区具备规格库结构（specify init 产物在位）时，候选逐条经 `feedback-utils.py --action record --unit-id "skill:sdd-loop-driver" --unit-type skill` 落宿主反馈库（runtime-mode 门控沿用编译 Wrap-up 节的 gate）；standalone（无该结构）时，候选清单随收尾汇总交付用户，由用户决定投递去向——**不自动上送**（feedback 红线：manual 投递，绝不自动传输）。
3. **skill 收尾点（run 结束）**：编译 `## Wrap-up` 节既有的五步引擎链（run determination → exec quant → feedback record → threshold notice → token reflection；probe-registry `@point:wrap-up scope=all` 绑定，73 units 全覆盖）——run 结束照单执行，本节不重复其步骤。

## Wrap-up

<!-- AUTO-GENERATED by probe-utils.py --action compile-embeds — truth source: .specify/shared/definitions/probe-definitions.md (## Handler / ## HandlerBinding) — fingerprint: 7877db82c58c — do not edit; edit the registry, then recompile -->

**Runtime-mode gate.** If `${SKILL_WORKDIR}/.specify/` does not exist, this skill is running in standalone mode (a non–Spec Kit deployment, e.g. a global agent skills directory) — skip this entire Wrap-up step: no engine call, no feedback entry.

1. Run Determination — `python3 .specify/scripts/python/run-determination.py --action determine --unit-id "skill:sdd-loop-driver" --unit-type skill`
2. Exec Quant — `python3 .specify/scripts/python/exec-quant.py --action collect --unit-id "skill:sdd-loop-driver" --unit-type skill`
3. Feedback Record — `python3 .specify/scripts/python/feedback-utils.py --action record --unit-id "skill:sdd-loop-driver" --unit-type skill`
4. Threshold Notice — `.specify/shared/workflow/feedback-step.md` § "Threshold prompt protocol (canonical semantics for step 6)"
5. Token Reflection — `.specify/shared/workflow/feedback-step.md` § "Reflection procedure (the embedded step points here)"
