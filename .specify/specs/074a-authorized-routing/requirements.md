# Requirements Specification: 授权席位的有界嵌套 SDD 调用与确定性分流（Authorized Routing & Nested SDD Invocation）— Feature 074 / Slice 074a

**Requirement Branch**: `074-goal-team-sdd-unification`
**Slice**: `074a-authorized-routing`
**Created**: 2026-10-28
**Status**: Draft
**编号口径**: 切片内连续本地编号（FR-001–FR-020、SC-001–SC-006、STR-001–STR-010）；父条目逐条映射见 `## Parent Mapping`。父规格仍是权威，切片编号只是投影，编号变化不构成删除、合并或重排。
**Input**: 父 Feature 074 的 `US1 + US2 + US3` 切片（MVP）。父权威：`.specify/specs/074-goal-team-sdd-unification/requirements.md`（2026-10-28 requirements + clarify 已裁定）；父设计：同目录 `plan.md` / `data-model.md` / `contracts/` / `quickstart.md` / `research.md` / `feature-ref.md`（已提交 @6297c14f6，本切片是其投影，不重新设计）；拆分记录：`.specify/state/074-goal-team-sdd-unification.md` § 拆分记录（tasks U4，2026-10-28，confirmed-user）。切片定义：把 Goal → Team → Agent 立为顶层控制链，授权席位可有界地启动嵌套 SDD 运行；用确定性三值分流判据把「何时走 SDD、何时直接修改」定死；把既有反嵌套义务收窄为可判定谓词（深度 2 链）。外层消费与交接报告段、概念扩散、兼容与安全由 `074b-nested-governance` 承接。

## Related Feature *(mandatory)*

**Feature ID**: 074
**Feature Name**: Goal/Team/Agent 与 SDD 开发流程统一（父特性；Unified Goal/Team/Agent Control Hierarchy with SDD Invocation）
**Slice**: `074a-authorized-routing`（Feature 074 的切片；不新建 Feature ID，不新增注册行）

绑定说明：Feature 074 已于 `2026-10-28` 由 `/speckit.clarify` Mode A 注册（`.specify/memory/features.md` 索引行与 `.specify/memory/features/074.md` 详情文件）。本切片只复用该绑定：不新建 Feature ID、不新增注册行；Draft→Planned 的状态推进由 plan 阶段按 `.specify/shared/workflow/feature-integration.md` § Status State Machine 拥有。

## Slice Scope（分解边界）

本切片是 Feature 074 两切片计划的第一个切片（MVP），来源是 tasks U4 分解门 `split-required`（tasks 57 行 > 上限 40；见 `.specify/state/074-goal-team-sdd-unification.md` § 拆分记录（tasks U4，2026-10-28））。切片内采用连续本地编号；父条目逐条映射见 `## Parent Mapping`；**父规格仍是权威**。

| 范围 | 父条目（父编号） | 本切片处理 |
|------|------------------|------------|
| 用户故事 | `US1`、`US2`、`US3` | 全部纳入（授权席位启动嵌套运行 / 确定性分流 / 治理嵌套） |
| 控制层级与授权 | `FR-001`–`FR-006` | 全部纳入并定义（本地 `FR-001`–`FR-006`） |
| 分流裁决 | `FR-007`–`FR-014` | 全部纳入并定义（本地 `FR-007`–`FR-014`） |
| 嵌套调用契约 | `FR-015`–`FR-019` | 全部纳入并定义（本地 `FR-015`–`FR-019`） |
| 引导/维护路径分流面 | `FR 025` | 纳入并定义（本地 `FR-020`） |
| 成功判据 | `SC-001`–`SC-004`、`SC-006`、`SC 007` | 全部纳入（本地 `SC-001`–`SC-006`） |
| 共享字符串 | `STR-001`–`STR-009`、`STR-011` | 全部纳入（本地 `STR-001`–`STR-010`） |
| 外层消费与交接 | `US4`、`FR-020`–`FR 024` | 不在本切片；由 `074b-nested-governance` 承接 |
| team report 嵌套段 | 父 `STR-010` | 不在本切片；由 `074b-nested-governance` 承接 |
| 兼容与安全 | `SC-005`、`SC 008`、`FR 026`–`FR 028` | 不在本切片；由 `074b-nested-governance` 承接 |

本切片 FR 定义总数 = 20（本地 `FR-001`–`FR-020`），落在分解门 8–30 区间内；`074b` = 8 条，同区间。

## Parent Mapping（父条目逐条映射）

**读法**: 左列是本切片的本地编号（定义行在本文件内），右列是父规格 `.specify/specs/074-goal-team-sdd-unification/requirements.md` 的原编号。父规格仍是权威；本表只记录投影关系，不复述父条文的规范内容。

### Slice FR → Parent FR

| Slice FR | Parent FR | 一行含义 |
|----------|-----------|----------|
| `FR-001` | `FR-001` | 唯一控制层级：Goal 最高、Team 编排、Agent 执行职责、SDD 运行是从属执行路径，且不得反向改动上层 |
| `FR-002` | `FR-002` | 定义「直接修改」= 无 SDD 工件链但仍受全部适用质量门与确认门约束，并在分流 owner 文档中与 SDD 运行区分 |
| `FR-003` | `FR-003` | Agent 定义可用中立键声明 SDD 调用能力（closed 值 allowed/forbidden，缺省 forbidden），且不向任何宿主渲染 |
| `FR-004` | `FR-004` | Team 席位用同一键在 `team.md` frontmatter 的 `seats` 映射按席位 slug 声明策略；有效授权 = Agent 能力 AND 席位策略 |
| `FR-005` | `FR-005` | 反嵌套义务收窄为一个可判定谓词（定义声明 allowed + 席位策略 allowed + 任务为 SDD 指派），前置探针 fail-closed 并指明失败条件 |
| `FR-006` | `FR-006` | 允许的嵌套链深度为 2；virtual 成员不得承载 SDD；阶段执行者是叶子；禁止 SDD-within-SDD；每成员默认一运行 |
| `FR-007` | `FR-007` | 提供唯一权威分流裁决：sdd / direct / adjudicate 三值，由确定性引擎对相同输入返回相同裁决 |
| `FR-008` | `FR-008` | 分流只消费声明输入（变更性质、可追溯性、影响面、可逆性、复杂度层级），取值域封闭；definition-class 面默认 cross-cutting |
| `FR-009` | `FR-009` | 任一 sdd 条件命中（新增/改变能力或契约、需可追溯、cross-cutting、不可逆、Complex/High-stakes）即返回 sdd |
| `FR-010` | `FR-010` | 仅当全部 direct 条件同时成立才返回 direct；definition-class 面另需声明为有界修正并记录理由 |
| `FR-011` | `FR-011` | 固定优先级 adjudicate > sdd > direct；不得静默默认 direct；每次裁决携带输入与封闭词表中的理由码 |
| `FR-012` | `FR-012` | 用户显式指示覆盖裁决，并记录为带用户指示与被覆盖裁决的 adjudication；引擎不得覆盖用户 |
| `FR-013` | `FR-013` | 分流按「每成员职责一次」执行，裁决复用至输入变化；裁决与输入、理由码记录在 team run report 或 Agent 执行证据中 |
| `FR-014` | `FR-014` | 分流规则唯一 owner = `shared/definitions/sdd-routing-definitions.md`；其他面只按引用抵达，不得复述输入集、门限或裁决表 |
| `FR-015` | `FR-015` | `sdd-loop-driver` 支持「由团队调用」的入口形态：绑定 Goal、可选 Target、team slug、调用席位、授权工件/领域范围、分流裁决，并在 U0 前校验 |
| `FR-016` | `FR-016` | 嵌套运行止于 review 完成，返回结构化 handoff（outcome、到达阶段、工件与证据路径、未解决 finding、异常行、集成身份），不得 merge 或 push |
| `FR-017` | `FR-017` | 调用方 Agent 必须把 handoff 原样或按稳定路径带入自身结果与 team run report；嵌套 outcome 为 blocked/failed 时不得报成功 |
| `FR-018` | `FR-018` | 嵌套运行以「一条写线」注册到既有 line registry 与 worktree/ownership 机制；领域重叠须串行化或拒绝；不得新建第二套机制 |
| `FR-019` | `FR-019` | stall / 超时 / 预算耗尽时停止、持久化状态脊、返回 failed handoff，并套用外层失败隔离与上报；不得静默等待 |
| `FR-020` | `FR 025` | `sdd-project-setup` 与 `sdd-house-keeping` 在同一分流面被归类为引导/维护路径（区别于 SDD 开发流程）；派发子代理时适用同一有效授权谓词；只有 `sdd-loop-driver` 构成 SDD 调用 |

### Slice SC → Parent SC

| Slice SC | Parent SC | 一行含义 |
|----------|-----------|----------|
| `SC-001` | `SC-001` | 授权/未授权两席 fixture：同一 SDD 分流职责只从授权席启动一次嵌套运行，未授权席在派发前被阻断且两侧记录都点名失败的那一半 |
| `SC-002` | `SC-002` | 分流引擎对黄金表每一行返回文档化裁决与理由码；相同输入重复求值结果一致 |
| `SC-003` | `SC-003` | 嵌套运行到达 review、产出完整 SDD 工件链、零 merge 零 push，且 report 嵌套段引用每条工件与证据路径 |
| `SC-004` | `SC-004` | 阶段执行者不能启动 SDD 运行；任何未满足三项授权条件却点名 driver 的派发提示在派发前被阻断；既有反嵌套契约测试对非授权路径保持绿 |
| `SC-005` | `SC-006` | 不引入第二套 registry / ledger / 状态脊 / ownership 模型 / 集成队列；嵌套运行的记录落在既有 line 与状态工件上 |
| `SC-006` | `SC 007` | 任何歧义或冲突输入集产出 adjudicate 而绝不产出 direct，且在黄金表全部用例上成立 |

### Slice STR → Parent STR

| Slice STR | Parent STR | 一行含义 |
|-----------|------------|----------|
| STR-001 | STR-001 | 授权能力键名 `"sdd-invocation"` |
| STR-002 | STR-002 | 能力/策略允许值 `"allowed"` |
| STR-003 | STR-003 | 能力/策略禁止值与缺省值 `"forbidden"` |
| STR-004 | STR-004 | 分流裁决值 `"sdd"` |
| STR-005 | STR-005 | 分流裁决值 `"direct"` |
| STR-006 | STR-006 | 分流裁决值 `"adjudicate"` |
| STR-007 | STR-007 | 嵌套运行 outcome `"completed"` |
| STR-008 | STR-008 | 嵌套运行 outcome `"blocked"` |
| STR-009 | STR-009 | 嵌套运行 outcome `"failed"` |
| STR-010 | STR-011 | 席位策略映射键名 `"seats"` |

## Overview

The parent Feature 074 requirement establishes one control hierarchy — Goal → Team → Agent — inside which an SDD run is a subordinate execution path that an authorized team member may start. This slice delivers the MVP half of that requirement: the hierarchy statement itself, the two-half authorization (Agent capability AND Team seat policy), the deterministic routing verdict that separates an SDD run from a direct modification, the governed depth-2 nesting predicate, and the nested invocation contract that ends at review with a structured handoff.

What the outer layer does with that handoff — the mandatory team run-report section, the Goal-level observational attribution, the vocabulary diffusion into every Goal/Team/Agent surface, and the additivity and containment guarantees — belongs to the second slice, `074b-nested-governance`. Concept ownership stays where it already lives: this slice references the SDD stage roster, the Goal/Target model, the Team model, and the line/ownership primitives; it does not re-create them.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - An authorized team member starts a nested SDD run (Priority: P1)

A team is running against a bound Goal and Target. One seat's agent definition declares
that it may host an SDD run, and the team roster permits that seat to do so. When the seat
receives a duty whose routing verdict is SDD, it starts an SDD run for the declared scope,
keeps the outer team informed, and returns a handoff when the run reaches review.

**Why this priority**: This is the value the feature exists to deliver — the two delivery
paths become one hierarchy instead of two disconnected workflows.

**Independent Test**: Build a fixture team with one authorized seat and one unauthorized
seat, assign both the same SDD-routed duty, and confirm the authorized seat starts a nested
run while the unauthorized seat is blocked with the failed predicate named.

**Acceptance Scenarios**:

1. **Given** an agent definition with [[STR-001]] set to [[STR-002]] and a roster seat with
   the same policy, **When** an SDD-routed duty is assigned, **Then** the seat starts exactly
   one nested SDD run for the declared Goal/Target and scope.
2. **Given** an agent definition without the capability or a seat policy of [[STR-003]],
   **When** the same duty is assigned, **Then** no SDD run starts and the rejection names
   which half of the authorization failed.
3. **Given** a nested run that reaches review, **When** it returns, **Then** the handoff
   carries its artifact and evidence paths and performs no merge or push.

---

### User Story 2 - A deterministic decision separates SDD from direct modification (Priority: P1)

Before an agent writes, it classifies the proposed change against declared inputs and gets a
verdict: run SDD, modify directly, or adjudicate. The verdict is produced by one deterministic
engine, records the inputs and the matched reason, and cannot return "direct" when the change
is feature-scale, cross-cutting, irreversible, traceability-bound, or Complex/High-stakes.

**Why this priority**: Without an unambiguous rule, every agent invents its own threshold and
the hierarchy produces inconsistent behaviour. This is the "明确的定义" the user asked for.

**Independent Test**: Feed a golden table of representative changes (feature, maintenance,
cross-cutting, irreversible, ambiguous, bounded definition correction) to the routing engine
and assert each documented verdict and reason code; repeat the same inputs and assert
identical verdicts.

**Acceptance Scenarios**:

1. **Given** a feature-scale or irreversible change, **When** routing runs, **Then** the
   verdict is [[STR-004]] with the triggering inputs recorded.
2. **Given** a bounded, reversible maintenance change with no traceability need, **When**
   routing runs, **Then** the verdict is [[STR-005]] and the change proceeds under the
   applicable quality and confirmation gates.
3. **Given** a missing or conflicting input, **When** routing runs, **Then** the verdict is
   [[STR-006]] and never [[STR-005]].
4. **Given** an explicit user instruction that differs from the verdict, **When** the change
   proceeds, **Then** the override is recorded as an adjudication with the user's instruction
   and the overridden verdict.

---

### User Story 3 - Nesting is governed, not escaped (Priority: P2)

The existing anti-nesting obligation forbids any dispatch prompt from naming a driver skill.
This feature narrows that prohibition to a decidable predicate: only an agent that declares
the capability, whose seat policy allows it, and that is receiving an SDD assignment may host
a driver. Stage executors remain leaves and can never start a driver; an SDD run cannot
contain another SDD run; every other dispatch keeps the original prohibition.

**Why this priority**: The previous invariant exists because an ungoverned second driver
escapes the hierarchy. Removing it wholesale would reintroduce that defect; narrowing it to a
checked predicate is what makes the new capability safe.

**Independent Test**: Run the pre-dispatch governance probe against four dispatch shapes —
authorized SDD assignment, unauthorized prompt naming a driver, stage executor attempting to
load a driver, and a nested SDD attempt inside a stage — and confirm only the first is
dispatched.

**Acceptance Scenarios**:

1. **Given** an authorized seat receiving an SDD assignment, **When** the pre-dispatch probe
   runs, **Then** the dispatch is allowed and the authorization basis is recorded.
2. **Given** any dispatch whose recipient lacks either half of the authorization, **When** a
   prompt names an SDD driver, **Then** the dispatch is blocked before it leaves and the
   failed condition is named.
3. **Given** an SDD stage executor, **When** it attempts to start or host an SDD run, **Then**
   the attempt is refused and reported as an anomaly.
4. **Given** two authorized seats whose territories overlap, **When** both attempt an SDD run
   concurrently, **Then** the runs are serialized or one is rejected, and the decision cites
   the existing line/ownership mechanism.

---

### Edge Cases

- **Seat allows, agent lacks the capability** (or the reverse): effective authorization is the
  AND of both halves; the run is refused and the report names the failing half.
- **Terminal Goal or terminal/closed Target**: no nested run may start; the invocation is
  refused with the goal-engine verdict, never silently re-scoped.
- **Target project lacks a `.specify/` structure**: route to the setup path; the framework
  MUST NOT degrade an SDD-routed change into a direct modification.
- **Two authorized seats, overlapping territory**: the existing line registry and ownership
  mechanism decide serialization or rejection; no second concurrency mechanism is introduced.
- **Review returns unresolved findings**: the nested run repairs within its own loop; if it
  cannot, it returns a failed handoff carrying the findings, and the outer layer adjudicates.
- **Stall, timeout, or budget exhaustion**: the nested run stops, persists its state spine, and
  returns a failed handoff with the required elements; the outer team's failure isolation and
  reporting apply.
- **The invoking agent is itself a stage executor of another run**: refusal; a stage executor
  is a leaf by definition.
- **A member executed in virtual mode attempts to host SDD**: refused before dispatch; virtual
  execution would merge the orchestrating session with the driver.
- **The seat has no [[STR-010]] entry**: the policy resolves to [[STR-003]]; the run is refused
  even when the Agent declares [[STR-002]].
- **A duty's inputs change after its verdict**: the routing decision is re-applied; the earlier
  verdict is retained in the record and the new verdict supersedes it.
- **The handoff lacks its integration identity**: the outer layer cannot integrate; the handoff
  is incomplete and the run MUST NOT be reported successful.
- **A declared input is knowingly misclassified** (e.g. a feature reported as maintenance):
  the deterministic engine cannot detect a dishonest declaration; the review surface audits
  the classification and records the discrepancy. The engine's determinism is over declared
  inputs, not over the truthfulness of the declaration.
- **User explicitly directs the opposite path**: user authority wins; the override is recorded
  as an adjudication.

## Requirements *(mandatory)*

### Functional Requirements

**Control hierarchy and vocabulary**

- **FR-001**: The framework MUST define one control hierarchy in which the Goal is the highest
  layer, a Team bound to one Goal orchestrates Agent members, an Agent executes a duty, and an
  SDD run is a subordinate execution path an authorized Agent may start. No SDD run may
  create, rebind, re-scope, or terminate a Goal, Target, Team, or roster.
- **FR-002**: The framework MUST define direct modification as executing a change without an
  SDD artifact chain while remaining subject to every applicable quality and confirmation
  gate, and MUST distinguish it from an SDD run in the routing owner document.

**Authorization**

- **FR-003**: An Agent definition MUST be able to declare SDD invocation capability through the
  neutral metadata key [[STR-001]], whose closed values are [[STR-002]] and [[STR-003]]; an
  absent key means [[STR-003]]. The key is framework-level and MUST NOT be rendered to any
  host tool.
- **FR-004**: A Team roster seat MUST be able to declare SDD invocation policy through the same
  key [[STR-001]] with the same closed values, stored as a `team.md` frontmatter map under the
  key [[STR-010]] keyed by seat slug; an absent seat entry or key means [[STR-003]]. The
  dispatch payload MUST carry the team slug, and the authorization probe MUST resolve the
  policy by (team, seat). Effective authorization is the logical AND of the Agent capability
  and the seat policy; an SDD run MUST NOT start unless the effective value is [[STR-002]].
- **FR-005**: The existing anti-nesting obligation MUST be narrowed to a decidable predicate: a
  dispatch prompt may name or assign an SDD driver only when the recipient resolves to an Agent
  definition declaring [[STR-002]], its seat policy declares [[STR-002]], and the assigned
  task is an SDD assignment. Every dispatch that does not satisfy all three conditions keeps
  the original prohibition. The pre-dispatch probe MUST enforce the predicate and fail closed,
  naming the condition that failed.
- **FR-006**: The permitted nesting chain MUST be depth 2: team orchestrator → invoking member
  (driver host) → stage executor (leaf). A member executed in virtual mode MUST NOT host an SDD
  run, because virtual execution occupies the orchestrating session and collapses the outer
  layer into the driver. A stage executor MUST NOT start or host any SDD run; an SDD stage
  executor MUST NOT itself be an SDD invocation host; SDD-within-SDD recursion is prohibited.
  A member MUST host at most one SDD run at a time unless the team declares a higher per-member
  cap within the existing line mechanism. The anti-nesting owner document MUST be amended to
  state this depth-2 chain and the virtual prohibition; FR-005 is the closed form of that
  amendment.

**Routing decision**

- **FR-007**: The framework MUST provide one authoritative routing decision that classifies a
  write-bearing change as [[STR-004]] (run the SDD flow), [[STR-005]] (direct modification),
  or [[STR-006]] (adjudicate), implemented by a deterministic engine that returns the same
  verdict for the same inputs.
- **FR-008**: The decision MUST consume declared inputs only: change nature, whether durable
  traceability is required, blast radius, reversibility, and the existing Task Complexity
  Rubric tier. Each input MUST have a closed value domain defined in the routing owner
  document. It MUST NOT use implementation medium, file extension, language, artifact count,
  or author identity. Changes to definition-class surfaces (constitution, instructions,
  Agent/Skill/Team definitions, and templates that generate them) are treated as cross-cutting
  by default.
- **FR-009**: The decision MUST return [[STR-004]] when any of the following holds: the change
  adds or alters a capability or contract; durable traceability is required; the blast radius
  is cross-cutting; the change is irreversible or hard to reverse; or the complexity tier is
  Complex or High-stakes.
- **FR-010**: The decision MUST return [[STR-005]] only when all of the following hold: the
  change preserves every existing capability and contract; no durable traceability is
  required; the blast radius is local; the change is reversible; the complexity tier is
  Trivial or Standard; and, for a definition-class surface, the change is declared a bounded
  correction with a recorded rationale.
- **FR-011**: The decision MUST apply one fixed precedence: [[STR-006]] first, then
  [[STR-004]], then [[STR-005]]. It MUST return [[STR-006]] whenever a required input is
  missing or ambiguous or the inputs conflict; otherwise it MUST return [[STR-004]] if any
  FR-009 condition holds; it MUST return [[STR-005]] only if all FR-010 conditions hold. The
  definition-class cross-cutting default applies only in the non-adjudicate branch. It MUST
  NOT silently default to [[STR-005]]. Every verdict MUST carry its inputs and a reason code
  from a closed vocabulary owned by the routing owner document.
- **FR-012**: An explicit user instruction overrides the verdict; the override MUST be recorded
  as an adjudication containing the user's instruction and the overridden verdict. The engine
  MUST NOT override the user.
- **FR-013**: The decision MUST be applied once per declared member duty before that duty
  performs a write-bearing change; the verdict is reused for that duty until one of its inputs
  changes. The verdict with its inputs and reason code MUST be recorded in the team run report
  or the Agent execution evidence, consumable by the outer layer.
- **FR-014**: The routing rule MUST have exactly one authoritative owner document at
  `shared/definitions/sdd-routing-definitions.md`, which owns the input value domains, the
  verdict table, the precedence, and the reason-code vocabulary. The driver's own entry-routing
  guidance, the project instructions, team and Agent guidance, and tests MUST reach that owner
  by reference and MUST NOT restate its input set, thresholds, or verdict table.

**Nested invocation contract**

- **FR-015**: `sdd-loop-driver` MUST support an invoked-from-team entry form that accepts the
  bound Goal reference, an optional Target, the team slug, the invoking seat, the authorized
  artifact/territory scope, and the routing verdict, and MUST validate them before U0 begins.
- **FR-016**: The nested run MUST end at review completion and return a structured handoff
  carrying an outcome of [[STR-007]], [[STR-008]], or [[STR-009]], the stages reached, the
  artifact paths, the evidence paths, unresolved review findings, an explicit anomaly line,
  and the integration identity: line id, branch, worktree path, and HEAD commit. The retained
  branch MUST be named in the handoff. It MUST NOT merge or push.
- **FR-017**: The invoking Agent MUST include the nested run's handoff in its own result and in
  the team run report, verbatim or by stable path. It MUST NOT report success when the nested
  outcome is [[STR-008]] or [[STR-009]].
- **FR-018**: A nested run MUST register with the existing line registry and the existing
  worktree-per-write-line and ownership mechanism as one write line. Concurrent nested runs
  whose territories overlap MUST be serialized or rejected. No second registry, ownership
  model, integration queue, or state spine may be created.
- **FR-019**: On stall, timeout, or budget exhaustion, the nested run MUST stop, persist its
  state spine, and return a [[STR-009]] handoff carrying what was found, why the run was
  costly, the intermediate artifacts by path, and the available dispositions. The outer
  team's failure isolation and reporting MUST apply; the run MUST NOT wait silently.

**Bootstrap and maintenance classification**

- **FR-020**: `sdd-project-setup` and `sdd-house-keeping` MUST be classified in the same
  routing surface as bootstrap and maintenance paths, distinct from the SDD development flow,
  so an Agent can choose among them. An invocation of either skill MUST satisfy the same
  effective-authorization predicate as an SDD invocation when it dispatches subagents. Only
  `sdd-loop-driver` constitutes an SDD invocation under FR-015.

### Key Entities *(include if requirement involves data)*

- **Control Layer**: One rung of the hierarchy — Goal, Team, Agent, or SDD Invocation. Each
  layer has an owner and a boundary; a lower layer never mutates an upper layer's definition.
- **SDD Invocation**: A bounded nested SDD run started by an authorized seat. Carries the
  invoking team and seat, the Goal/Target, the authorized scope, the routing verdict, the line
  identity, the integration identity, the outcome, and the artifact/evidence paths.
- **Seat Policy**: The `team.md` frontmatter entry under [[STR-010]], keyed by seat slug; it
  resolves together with the Agent capability to the effective authorization.
- **Authorization**: The pair of Agent capability and Team seat policy for the same key,
  resolved by (team, seat); its effective value is their AND, and the record names which half
  supplied which value.
- **Routing Verdict**: The decision record — declared inputs, verdict, reason code from the
  closed vocabulary, actor, and any user override.
- **Direct Modification**: A change executed without an SDD artifact chain, still subject to
  the applicable quality and confirmation gates.
- **Integration Identity**: The line id, branch, worktree path, and HEAD commit that let the
  outer layer locate and integrate a completed nested run.
- **Nested Run Handoff**: The structured return from a nested run — outcome, stages reached,
  artifact and evidence paths, unresolved findings, integration identity, and an anomaly line.
- **Stage Executor**: A leaf execution that runs one assigned stage inside a nested run; it
  cannot drive, dispatch, or start another run.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In a fixture team with one authorized and one unauthorized seat, the same
  SDD-routed duty starts exactly one nested run from the authorized seat and is blocked before
  dispatch for the unauthorized seat, with the failing authorization half named in both
  records.
- **SC-002**: The routing engine returns the documented verdict and reason code for every row
  of a golden case table covering feature, maintenance, cross-cutting, irreversible, ambiguous,
  conflicting, and bounded definition-correction changes; ambiguous and conflicting rows expect
  [[STR-006]], and the bounded definition-correction row expects [[STR-005]] only when all
  FR-010 conditions hold. Repeated evaluation of identical inputs returns identical verdicts.
- **SC-003**: A nested run reaches review, produces the complete SDD artifact chain, performs
  zero merge and zero push, and the team run report's nested section cites every artifact and
  evidence path.
- **SC-004**: Stage executors cannot start an SDD run, and every dispatch prompt that names a
  driver without satisfying all three authorization conditions is blocked before dispatch;
  all pre-existing anti-nesting contract tests remain green for non-authorized paths.
- **SC-005**: No second registry, ledger, state spine, ownership model, or integration queue is
  introduced; the nested run's records resolve to the existing line and state artifacts.
- **SC-006**: Every ambiguous or conflicting input set produces [[STR-006]] and never
  [[STR-005]]; the property holds across all cases in the golden table.

### Measurement Sources & Collection Methods

- **SC-001 Source**: Fixture-team integration test under `tests/`, plus the generated team run
  report; inspected by the contract test for the authorization predicate.
- **SC-002 Source**: Routing-engine unit tests driven by a checked-in golden table; an
  idempotence test evaluates each row twice and compares verdicts and reason codes.
- **SC-003 Source**: A scripted integration fixture that runs one nested SDD invocation to
  review; assertions read the artifact paths, the team run report, `git log`, and `git status`.
- **SC-004 Source**: The pre-dispatch governance test suite and the existing anti-nesting
  contract tests; each blocked dispatch record is inspected for the named condition.
- **SC-005 Source**: A structure/grep contract test over the changed tree plus the line-registry
  contract test; both assert reuse of existing artifacts and absence of new stores.
- **SC-006 Source**: The same golden-table and property test as SC-002, filtered to ambiguous
  and conflicting rows; the expected value is fixed to [[STR-006]].

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `"sdd-invocation"` | authorization schema checks (Agent definition + Team seat), pre-dispatch governance tests |
| `STR-002` | `"allowed"` | authorization schema checks, pre-dispatch governance tests, SDD-host Agent responsibility contract |
| `STR-003` | `"forbidden"` | schema-default tests, backward-compatibility tests |
| `STR-004` | `"sdd"` | routing golden table, routing-engine unit tests |
| `STR-005` | `"direct"` | routing golden table, direct-modification gate tests |
| `STR-006` | `"adjudicate"` | routing golden table, ambiguity and conflict property test |
| `STR-007` | `"completed"` | nested-run handoff contract test, team run-report contract test |
| `STR-008` | `"blocked"` | nested-run handoff contract test, authorization-failure tests |
| `STR-009` | `"failed"` | nested-run handoff contract test, stall and timeout tests |
| `STR-010` | `"seats"` | team.md seat-policy schema tests, authorization contract tests |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Boundary and Ownership (non-duplication)

| Concern | Existing owner | This slice's relationship |
|---------|----------------|---------------------------|
| U0–U6, state spine, stage sentinels, U4 verification, watcher, stall handling | Feature 058 / `sdd-loop-driver` | Reference and preserve; the nested entry is additive |
| Agent Template / Instance / Execution; create/dispatch/improve skills | Feature 060 / `agent-definitions.md`; neutral key set in `src/specify_cli/__init__.py` (`NEUTRAL_AGENT_METADATA_KEYS`) | Reuse; the capability key extends the neutral metadata set and its validator allowlist |
| Line registry, worktree-per-write-line, ownership, integration queue | Feature 064 / `sdd-loop-driver/SKILL.md` Hard Requirement 11 and `references/dispatch-recipes.md` | Reuse as the only concurrency primitives; no second model |
| Stage-team preset and work-package decomposition | Feature 070 | Preserve; it is the in-run decomposition mechanism, not a substitute for nested invocation |
| Flow class, fast-fail, confirmation gates, Task Complexity Rubric | Features 069 / 052 and the shared guidelines | Reference by path; no restatement |
| Goal, Target, and Goal–Team binding | `goal-definitions.md` | Reference; no structural link or new mandatory field |
| Team conceptual model, patterns, run report | `create-team` / `run-team`; report contract in `create-team/SKILL.md` § Report contract | Reference; the nested-SDD report section itself is parent `FR 021` and belongs to `074b-nested-governance` |
| Anti-nesting obligation | `subagent-definitions.md` § Dispatch-Time Governance Obligation | Amend the predicate once to the depth-2 chain and the virtual prohibition; do not duplicate it |

## Assumptions

*Assumption identifiers retain the parent labels. Parent `A8` and `A13` concern the outer-layer attribution surface and belong to `074b-nested-governance`.*

- **A1**: This is a framework-source change under the two-hats rule; it lands in the sources and
  reaches client projects through the normal publish/install/init flow.
- **A2**: [[STR-001]] is a new neutral framework key registered in the neutral metadata set and
  excluded from host rendering, so host rendering differences do not change authorization.
- **A3**: The team seat policy is a backwards-compatible `team.md` frontmatter extension under
  [[STR-010]], keyed by seat slug; an absent entry means [[STR-003]] for every existing team.
- **A4**: The routing engine is deterministic over declared inputs, whose closed value domains
  and mechanical classification tests are owned by
  `shared/definitions/sdd-routing-definitions.md`. Honest classification remains the caller's
  duty, audited by the review surface; the engine never invents an input.
- **A5**: A nested SDD run is the only sanctioned nesting. Feature 070 work packages remain the
  only in-run decomposition; no third nesting form is introduced.
- **A6**: Of the `sdd-*` skills, only `sdd-loop-driver` constitutes the SDD development flow;
  `sdd-project-setup` and `sdd-house-keeping` are routed bootstrap/maintenance paths.
- **A7**: An explicit user instruction overrides the routing verdict and is recorded as an
  adjudication.
- **A9**: The default concurrency cap is one nested run per member; a higher per-member cap is
  permitted only within the existing line registry and territory constraints.
- **A10**: The nested run's review stage may include the driver's existing review-repair loop of
  Feature 063; ending "at review" means after that loop settles, not before findings are
  addressed.
- **A11**: The permitted nesting chain is depth 2 (team orchestrator → member driver host →
  stage executor); a virtual-mode member cannot host SDD.
- **A12**: The routing unit is one declared member duty; the verdict is reused until one of its
  inputs changes.

## Out of Scope

- **074b 承接（显式记录）**: 父 `US4`、父 `US5`；父 `FR-020`–`FR 024`（Goal 侧观察性归因与 ledger 归因、team report 强制嵌套段、Team Stage 维度消歧、SDD-host Agent 责任声明、项目指令指针面）；父 `FR 026`–`FR 028`（兼容与安全、四面可加性、不新增调度/守护/自动传输/第二确认门）；父 `STR-010`（team report 的 `## Nested SDD Runs` 段标题）；父 `SC-005`、父 `SC 008`。以上全部由 `074b-nested-governance` 承接，本切片不定义、不实现。
- Automatic merge or push by a nested run.
- Changing the internal workflow of any individual `/speckit.*` stage command.
- Allowing stage executors to drive, dispatch, or load any driver.
- Multiple levels of SDD nesting (SDD inside SDD).
- Replacing the Feature 070 work-package model or the Feature 064 line/ownership model.
- Automatically making every Agent SDD-capable.
- Adding a scheduler, daemon, second confirmation gate, or automatic feedback transmission.
- Rewriting the anti-nesting rule for dispatches that do not satisfy FR-005.

## Cross-Slice Design Attribution（跨切片交付归属）

**读法**: 本节裁定 074a 在父设计（`.specify/specs/074-goal-team-sdd-unification/plan.md` 与同目录 `contracts/`）与 `074b-nested-governance` 之间的交付归属。它不改写 `## Requirements`、`## Success Criteria`、`## Out of Scope` 的任何条文，只说明本切片如何兑现它们；父设计文件是投影来源，不是切片边界。

- **D-1 归属按需求条目切分，不按父设计文件的物理分组**：本切片的设计集覆盖本地 `FR-001`–`FR-020` 与 `SC-001`–`SC-006`。凡对应父条款，无论落在哪个父 contract 文件，都整体继承为来源并保留父条款编号作来源标注——例如 `nested-invocation.md` 的父 C-45，以及 `diffusion-and-compat.md` 的父 C-58 / C-59 / C-67 与 C-64、C-66 中涉及本地 `FR-018`、`FR-014` 的部分；`074b-nested-governance` 只重 derive 其自有的父 `FR 020`–`FR 024`、`FR 026`–`FR 028` 与父 `SC 005`、`SC 008` 面。
  理由：拆分记录（`.specify/state/074-goal-team-sdd-unification.md` § 拆分记录，`confirmed-user`）按需求条目切分，并声明两片 FR 集互斥、并集 = 28。若改按父文件物理分组，本地 `FR-020`（父 `FR 025`）与 `FR-018` / `FR-014` 的条款面会漂到 074b，与本切片 20 FR 的声明直接冲突。
- **D-2 分流裁决的记录面在本切片内是 Agent 执行证据**：本地 `FR-013` 的「team run report 或 Agent 执行证据」在本切片由 Agent 执行证据兑现（输入、裁决、理由码、actor、用户覆盖记录），并由 handoff 与调用方结果按稳定路径引用。父 contract C-54 的 report 段 verdict reference 随 074b 的段契约落地时读同一条记录，不得重算。
  理由：本切片不定义 team report 的固定段（父 `STR 010` 的标题字面量），故唯一可交付的记录面是 Agent 执行证据；`FR-013` 原文的「或」已允许该读法，父条文不改写。
- **D-3 `SC-003` 在本切片交付内容面，不交付段标题格式**：一次嵌套运行止于 review、产出完整 SDD 工件链、零 merge 零 push（`git log` / `git status` 可断言），且调用方结果与 team supervisor 按既有 report 契约写下的记录携带每条工件与证据路径的引用（本地 `FR-017` 已要求）。父 `STR 010` 的固定标题与「每次运行强制存在、无嵌套则声明 none」的段语义由 `074b-nested-governance` 兑现，本切片的夹具因此不断言该标题字面量。
  理由：`SC-003` 的工件链、零 merge/push、路径引用三项都可由本切片的可交付面机械断言，只有段标题与段语义属 074b——这与 `## Out of Scope` 的「team report 嵌套段」行一致：不在本切片的是段标题与段语义，不是路径引用的内容面。越界建段等于把 074b 的契约拉进本切片。

## Clarifications

### Session 2026-10-28

- Q: 本切片的编号为何与父规格 074 不同？ → A: 本切片是父规格 074 的两片拆分投影（用户 2026-10-28 确认，`confirmed-user`），不是新的需求裁定。切片内 FR / SC / STR 采用连续本地编号，逐条父映射见 `## Parent Mapping`；父规格仍是权威，编号变化不构成删除、合并或重排。拆分依据与边界见 `.specify/state/074-goal-team-sdd-unification.md` § 拆分记录（tasks U4，2026-10-28）。
- Q: 父规格既有裁定对本切片是否仍然生效？ → A: 生效，且不重开裁定。父规格 `## Clarifications` > `### Session 2026-10-28` 的裁定与同轮边界回修，对纳入本切片的条目原样适用：授权面 = Agent 能力 + Team 席位策略；分流判据 = 复合确定性判据；嵌套止于 review 交接；分流规则唯一 owner 文件 `shared/definitions/sdd-routing-definitions.md`；优先级 `adjudicate > sdd > direct`；深度 2 嵌套链与 virtual 禁用；席位策略存于 `team.md` frontmatter 的 `seats` 映射并按 (team, seat) 解析；routing unit = 每成员职责一次并复用至输入变化；并发上限 = 每成员一；handoff 携带集成身份；ledger 归因由 team supervisor 写入。

### Session 2026-10-29

- Q: 074a 的设计条款是否按本切片自己的需求集重新 derive，包括那些在父设计里被放在 074b 侧重文件中的条款（`diffusion-and-compat.md` 的父 C-58 / C-59 / C-67，以及 C-64、C-66 中涉及本地 `FR-018`、`FR-014` 的部分）？ → A: 按需求条目重 derive。归属以 `.specify/state/074-goal-team-sdd-unification.md` § 拆分记录（`confirmed-user`）划分的需求集为准，不以父 contract 文件的物理分组为准：本切片覆盖本地 `FR-001`–`FR-020` 与 `SC-001`–`SC-006`，继承对应父条款并保留父编号作来源标注；074b 只重 derive 其自有条目（整合为 `## Cross-Slice Design Attribution` D-1）。**无人值守自裁**——拆分记录已声明两片 FR 集互斥、并集 = 28，且父设计文件按主题而非按切片组织；若按文件分组，本地 `FR-020`（父 `FR 025`）与 `FR-018` / `FR-014` 的条款面会漂出本切片，与 20 FR 的声明直接冲突，故只有一种与已记录意图一致的读法，属纠正而非裁定。
- Q: 本地 `FR-013` 的裁决记录面在本切片落在哪里（team run report 还是 Agent 执行证据），已知 team report 的固定段（父 `STR 010` 标题）不在本切片？ → A: 本切片由 Agent 执行证据承载（输入、裁决、理由码、actor、用户覆盖记录），handoff 与调用方结果按稳定路径引用；team report 段的 verdict reference 随 074b 段契约落地时读同一条记录、不得重算（D-2）。**无人值守自裁**——本切片不定义 report 固定段，可交付记录面只有 Agent 执行证据；`FR-013` 原文的「或」已允许该读法，父条文一句不改，未证伪任何下游前提。
- Q: 本地 `SC-003` 要求 team run report 的嵌套段引用每条工件与证据路径，而该段的固定标题与强制语义属 074b——本切片如何交付 `SC-003`？ → A: 交付内容面：嵌套运行止于 review、完整 SDD 工件链、零 merge 零 push、调用方结果与既有 report 记录携带路径引用；固定标题字面量与段语义交 074b，本切片夹具不断言该标题（D-3）。**无人值守自裁**——`SC-003` 的三项均可由本切片可交付面机械断言；若不划分，本切片要么越界实现 074b 的段契约，要么 `SC-003` 无落点，两种读法里只有一种与本切片 `## Out of Scope` 的「team report 嵌套段」行相容。
