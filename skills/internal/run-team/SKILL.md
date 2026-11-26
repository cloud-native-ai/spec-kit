---
name: run-team
description: 执行一个已建代理团队(/speckit.team run 的承载技能)——五查预检经 goal-utils 引擎唯一判定,目标重述、双结构渲染、present & execute、按 pattern 编排派发,运行报告落 runs/
classification: internal
skill_id: "<SKILL:.specify/skills/internal/run-team/SKILL.md>"
---

# run-team — 团队运行(从 /speckit.team run 提取)

> **Concurrency obligation（执行义务，按指针抵达）**: this skill is an execution body — before the first real action, run the one-shot assessment (class → carrier → partition), default to concurrent execution for two or more independent units, and when serial name a reason code and record the `requested` / `effective` / `effective_reason` reading. Authored text: `shared/definitions/subagent-definitions.md` § The Concurrency Obligation; class table: `shared/declarations/facts/concurrency-class.yaml`; reason codes: `shared/declarations/facts/serial-reason.yaml`; reading fields: `shared/declarations/facts/effective-concurrency.yaml`. This body restates none of their rules.


## Goal

执行一个已建团队的完整运行流程,承接 `/speckit.team` run 语义的全部程序性义务——五查预检经引擎唯一判定、目标重述、双结构渲染、present & execute、按 pattern 编排派发、运行报告(每次运行强制);每条义务以同等强度落于本技能对应节。概念语义:团队 = anchor + Static Structure(Role × Stage × Type)+ Dynamic Structure(四种协作模式),真源 `skills/internal/create-team/references/conceptual-model.md`;Anchor–Team 绑定与 Target 语义真源 `.specify/shared/definitions/anchor-definitions.md`。单代理操作归 `/speckit.agents`;create/modify 语义归 create-team / improve-team。

## Input Contract

- **输入**:`run <team-slug> [--target <T-<nnn> | <goal-slug>.T-<nnn>>]`(经 `/speckit.team` 路由);local 形 `T-<nnn>` 为规范形,qualified 形仅当其 `<goal-slug>` 等于绑定 goal 时接受。
- **目标团队不存在**(`.specify/teams/` 下无匹配 slug):报告 **"team not found"** 并提示 create 路径,不猜测。

## Workflow

### 1. Load

加载 `.specify/teams/<slug>/team.md`(定义:frontmatter + `## Goal` + `## Static Structure` + `## Dynamic Structure`,schema 真源 create-team `references/create-mode.md`)。

### 2. Preview — Target 解析与五查预检(引擎唯一判定点)

**解析顺序(不变量)**:显式 `--target` > `focus_target` > 无;非法 `focus_target` 报 `source=input-error` 并停止(修复经 improve-team),不静默忽略。`focus_target` 是 run 级 `--target` 的**预填**——不是写域声明、不是 Goal–Team 绑定变更、不参与 goal 身份解析;未声明且未显式指定(`source=none`)时全流程与引入前逐字节等价。

判定一律经引擎,不在散文中重推:

```bash
python3 .specify/scripts/python/goal-utils.py run-checks <team-slug> [--target <T-<nnn>>] --json
```

一次调用返回 `team_slug` / `goal_slug`(引擎载荷键名,值即锚点身份)/ `identity_kind` / `{effective, source, declared_focus}` / 五条 `checks`(1..5,各含 `id`/`name`/`verdict`/`message`)/ `verdict` / `blocked`,自 094 起另带**加性** `binding` 键(`{owner, owner_id, origin}`;predates-model 的 team 为 `null`,既有 `resolution` 子键与取值不变)(内部经 `parse_goal` / `preview_target_check` / `resolve_effective_target`);无前提可评的 check 记 `not-evaluated`——**从不**记 `ok`。`blocked` 是"本次必须停止"的字段。退出码:`0` 通过 / `2` 输入非法 / `3` 团队不存在 / `4` goal 不可解析 / `5` blocked——旗标、载荷与退出码归引擎的动作表(`python3 .specify/scripts/python/goal-utils.py --help`),本技能不复述。五查覆盖:绑定 anchor 解析(带 `--target` 时缺锚点定义即停并指向 `/speckit.anchor migrate`)、悬空 `T-<nnn>` 引用(停;补救 `/speckit.anchor targets --add`)、终态 Target 引用(停;重开经 `/speckit.anchor targets --set open --id <T-nnn>`,无执行旁路)、跨 anchor 引用(拒)、锚点自身终态(拒)。

### 3. Restate

把 **goal** 置于最前重述,使两个结构都被读作达成该目标的手段。

### 4. Render

渲染 **Static Structure**(Role × Stage × Type 矩阵:每个成员 agent、role、type(Worker/Meta)、lifecycle(persistent/temporary))与 **Dynamic Structure**(pattern、并行度/DAG/阈值/运行设置、执行流图——textual / mermaid / PlantUML)。

### 5. Present & Execute

**Run line 登记（任何席位派发之前）**: 呈现 anchor 与两个结构之前，先为本轮登记一条 run line。run-id 按本仓 requirements 102 的 A-18 生成——形如 `r<UTC yyyymmdd>T<UTC hhmmss>Z-<4 位小写十六进制>`，MUST 匹配引擎的 `RUN_ID_RE`；本技能既有的裸 UTC 时间戳 MUST NOT 充当 run-id（§7 报告文件名里的时间戳只是文件名成分，不是 run-id）。registry `line_id` 按 A-18 合成为 `<team-slug>-<run-id>`。引擎按 A-17 的有序候选解析：先 `skills/external/sdd-loop-driver/scripts/line-registry.py`，其次 `.specify/skills/sdd-loop-driver/scripts/line-registry.py`（下游项目只持有后者）。用引擎的 `register` 动作把该 line 登记为 `active`；动作、参数与退出码一律从引擎 `--help` 读取，本技能不复述参数表。**登记失败即 fail-closed**：具名引擎退出码后停下，不派发任何席位。§2 五查判 `blocked` 时流程在 §2 停止，不进入本步骤、不登记，避免留下悬空 line。

呈现 **anchor** 与两个结构后**直接执行**——呈现是披露,不是阻断门禁(事后修改途径:`/speckit.team` modify / improve-team;判据:`.specify/shared/guidelines/confirmation-gates.md`)。同时披露 summary 判定(refresh 或 suppressed;周期总结落锚点档案的 `.specify/anchoring/<anchor-slug>/summary/`,**从不**落团队目录;档案层归 `.specify/shared/definitions/anchor-definitions.md` § Archive Layers)与 Target 指派行,逐字形态:

- `本次 Target: T-<nnn> — <statement>(open)`
- `本次 Target: 无(对 goal 整体运行)`
- 解析来源为 `team-default` 时:`本次 Target: T-<nnn> — <statement>(open)(团队默认)`

(表单真源:`skills/internal/create-team/SKILL.md` → Summary Refresh)

**User-facing output channel**: when this run dispatches seats, this root is the only writer of user-facing output; seat activity is not user-facing; an echo command's product is emitted at a presentation boundary inside the stable envelope owned by `.specify/shared/guidelines/user-facing-output.md` (disclosure, not a gate). The run report and the periodic reporting line are the user-facing output; seat streams stay in their artifact paths. A tool result is not user-facing presentation.

### 6. Orchestrate(按团队 pattern 编排)

- **默认并发（team 执行体，席位即单元）**:只要席位之间无依赖、写领地（文件级路径集）互不相交、存在合法进程承载（fork / subprocess，定义 owner：`.specify/shared/definitions/subagent-definitions.md` § Three Execution Modes）且预算允许，本次运行 MUST 并发派发席位；串行 MUST 给出 `shared/declarations/facts/serial-reason.yaml` 的具名理由码与依据。运行报告 MUST 记录 `requested` / `effective` / `effective_reason` 三元组（字段 owner：`shared/declarations/facts/effective-concurrency.yaml`；`effective` 取席位派发/返回区间的最大重叠数，区间缺失记字面量 `not_evaluated`，MUST NOT 写 0 或估计值）。宿主内建 in-process subagent 路径 BANNED，不计为并发机制。
- 并行(parallel):派发前做 territory 校验(团队范围声明,真源 `skills/internal/create-team/references/` 与词汇表 Team Territory);未声明或相交的领地按绑定期判定判红,不带病运行。
- 串行链(serial):DAG 无环校验 + 逐交接(harness)验证。
- 迭代(iteration):强制最大迭代上限。
- 持续(continuous):每轮 run 一个 cycle,按声明成熟度运行,独立校验者(独立 verifier)在 L2+ 常驻。
- 成员派发模态按 `.specify/shared/definitions/subagent-definitions.md`;外部 CLI 派发遵守其 Visibility Contract;派发携带快速失败注入子句并要求显式异常回传行(沉默不读作干净,判据 `.specify/shared/guidelines/fast-fail.md`)。
- **Run line 刷新（每步边界一次）**: 在 §5 登记的同一条 line 上（引擎为 §5 按有序候选解析到的 `line-registry.py`），每个编排步骤边界调一次引擎 `update --last-event <step-label>`（步骤标签取当前编排步骤名），刷新该 line 的最近活动；不存在定时器、守护进程、心跳文件或第二 liveness 通道——line 的活动只由这些显式刷新写入。
- **结算义务（每个席位，owner 按指针）**: 席位派发之前 MUST 写起点记录 —— 一条 carrier `c3-team-seat` 的 `<label>.attempt`（含 `started_at`，写入既有派发日志目录），或经 C1/C2 派发时复用同 label 的既有载体起点证据（不重复写入）；每个席位的结算值、逐值证据、反应与违例集合归 `.specify/shared/definitions/superagent-definitions.md` § Termination（按指针，本节不复制值表或证据矩阵）；报告行的 `end_state` / `evidence` 列归 `skills/internal/create-team/SKILL.md` § Report。叶子执行者模板不获得第二套结算逻辑。
- 用户可在执行中随时中止。

### 7. Report

**先关闭 run line，再写报告**: 经引擎 `line-registry.py` 的 `deregister` 动作关闭 §5 登记的那条 line（`reason` 取值按引擎 `--help` 的动作表读取），报告正文 MUST 携带该 line 合成的 `line_id`（`<team-slug>-<run-id>`，即 STR-007 的值）。关闭失败 MUST NOT 被吞掉——在报告中写明关闭失败与引擎退出码，报告照常落盘。

执行结束后把带日期的运行报告写入 `.specify/teams/<slug>/runs/<UTC-timestamp>-report.md`(**每次运行强制**,报告契约真源:create-team SKILL.md → Report;含 `## Verification` 节)。Target 指派的运行报告带固定字段,逐字形态:`**Target 指派**: T-<nnn>(<statement>)` 或 `无(goal 整体)`,团队默认路径追加 `(团队默认)`;新台账条目带 `"target_ref": "T-<nnn>"`。

## Constraints(不变量)

- **`--target` 不变量**:Goal–Team 绑定、身份解析、summary 送达目录不因 `--target` 改变——它只是本次运行的聚焦切片,不是重绑或写域声明。
- **输出纪律**:run 中间产物留在 git-ignored `.specify/teams/.work/<slug>/`;交付物只到声明的目标路径(完整纪律:`skills/internal/create-team/SKILL.md` → Run Workspace, Reports & Output Discipline)。
- **continuous 例外门控**:`skills/internal/create-team/references/operating-loops.md` 与 `templates/teams/project-cluster.md` 的分级门保持,不因提取而放开。

## Boundaries

- 不承接 create/modify 语义(那是 create-team / improve-team 的职责);不服务单代理操作(那是 `/speckit.agents`)。
- 执行引擎与 references 全部引用 create-team 既有资产,不复制其内容。

## Wrap-up

<!-- AUTO-GENERATED by probe-utils.py --action compile-embeds — truth source: .specify/shared/definitions/probe-definitions.md (## Handler / ## HandlerBinding) — fingerprint: 2845f5641171 — do not edit; edit the registry, then recompile -->

**Runtime-mode gate.** If `${SKILL_WORKDIR}/.specify/` does not exist, this skill is running in standalone mode (a non–Spec Kit deployment, e.g. a global agent skills directory) — skip this entire Wrap-up step: no engine call, no feedback entry.

1. Run Determination — `python3 .specify/scripts/python/run-determination.py --action determine --unit-id "skill:run-team" --unit-type skill --run-id <RUN_ID> --complexity <COMPLEXITY>`；source args when available: `--session-file <SESSION_FILE> --session-rows <SESSION_ROWS> --tool <TOOL> --proxy-paths <PROXY_PATHS> --token-note <TOKEN_NOTE> --elapsed-ms <ELAPSED_MS> --elapsed-note <ELAPSED_NOTE> --names-current <NAMES_CURRENT> --names-baseline <NAMES_BASELINE> --declared-check <DECLARED_CHECK> --green-check <GREEN_CHECK> --red-first-refs <RED_FIRST_REFS> --collected <COLLECTED> --prev-user-turn-class <PREV_USER_TURN_CLASS> --unresolved-red <UNRESOLVED_RED> --red-source <RED_SOURCE>`
   尖括号为本轮运行时值——代入后照抄执行(占位 = 参数名去 --、转下划线、全大写;渲染集 = 引擎 manifest required + source,身份对已带实值)
2. Exec Quant — `python3 .specify/scripts/python/exec-quant.py --action collect --unit-id "skill:run-team" --unit-type skill`；source args when available: `--run-id <RUN_ID>`
3. Feedback Record — `python3 .specify/scripts/python/feedback-utils.py --action record --unit-id "skill:run-team" --unit-type skill --run-id <RUN_ID> --review <REVIEW> --points <POINTS>`
4. Threshold Notice — `.specify/shared/workflow/feedback-step.md` § "Threshold prompt protocol (canonical semantics for step 6)"
5. Token Reflection — `.specify/shared/workflow/feedback-step.md` § "Reflection procedure (the embedded step points here)"
6. Closeout — `.specify/shared/workflow/artifact-commit-step.md` § "The `## Close-out` step"
