# Requirements Specification: 外层消费、概念扩散与兼容安全（Nested Consumption, Diffusion & Compatibility）— Feature 074 / Slice 074b

**Requirement Branch**: `074b-nested-governance`
**Parent Feature Branch**: `074-goal-team-sdd-unification`
**Slice**: `074b-nested-governance`
**Created**: 2026-10-29
**Status**: Draft
**编号口径**: 切片内连续本地编号（FR-001–FR-008、SC-001–SC-002、STR-001–STR-007）；父条目逐条映射见 `## Parent Mapping`。父规格仍是权威，切片编号只是投影，编号变化不构成删除、合并或重排。
**Input**: 父 Feature 074 的 `US4 + US5` 切片（两片拆分中的第二片）。父权威：`.specify/specs/074-goal-team-sdd-unification/requirements.md`（2026-10-28 requirements + clarify 已裁定）；父设计：同目录 `plan.md` / `data-model.md` / `contracts/` / `quickstart.md` / `research.md` / `feature-ref.md`（本切片是其投影，不重新设计）；拆分记录：`.specify/state/074-goal-team-sdd-unification.md` § 拆分记录（tasks U4，2026-10-28，confirmed-user）。切片定义：把 074a 交付的嵌套 SDD 运行结果纳入外层 Goal/Team 消费面——团队运行报告强制嵌套段、Goal 侧观察性归因（经既有 ledger 引用、不新增 Goal 字段）、Team Stage 维度与 SDD 阶段名册消歧、SDD-host Agent 责任声明、项目指令的指针级分流面，并给出兼容与安全的可判定包含性声明。控制层级、双层授权、三值分流与嵌套调用核心由 `074a-authorized-routing` 已实现面承载，本切片只读引用，不重定义。

## Related Feature *(mandatory)*

**Feature ID**: 074
**Feature Name**: Goal/Team/Agent 与 SDD 开发流程统一（父特性；Unified Goal/Team/Agent Control Hierarchy with SDD Invocation）
**Slice**: `074b-nested-governance`（Feature 074 的切片；不新建 Feature ID，不新增注册行）

绑定说明：Feature 074 已于 `2026-10-28` 由 `/speckit.clarify` Mode A 注册（`.specify/memory/features.md` 索引行与 `.specify/memory/features/074.md` 详情文件）。本切片只复用该绑定：不新建 Feature ID、不新增注册行；状态推进由 plan 阶段按 `.specify/shared/workflow/feature-integration.md` § Status State Machine 拥有。

## Slice Scope（分解边界）

本切片是 Feature 074 两切片计划的第二个切片，来源是 tasks U4 分解门 `split-required`（tasks 57 行 > 上限 40；见 `.specify/state/074-goal-team-sdd-unification.md` § 拆分记录（tasks U4，2026-10-28））。切片内采用连续本地编号；父条目逐条映射见 `## Parent Mapping`；**父规格仍是权威**。两片 FR 集合互斥且并集 = 父 28 条：第一片 `074a-authorized-routing`（父 FR 001–019 + 父 FR 025）已实现并合入 `master`，本切片承接其余 8 条。

| 范围 | 父条目（父编号） | 本切片处理 |
|------|------------------|------------|
| 用户故事 | Parent US4、Parent US5 | 全部纳入（外层消费与交接 / SDD 概念扩散），本地 `US1`、`US2` |
| 外层消费与交接 | Parent FR 020、Parent FR 021 | 纳入并定义（本地 `FR-001`、`FR-002`） |
| 概念扩散 | Parent FR 022、Parent FR 023、Parent FR 024 | 纳入并定义（本地 `FR-003`、`FR-004`、`FR-005`） |
| 兼容与安全 | Parent FR 026、Parent FR 027、Parent FR 028 | 纳入并定义（本地 `FR-006`、`FR-007`、`FR-008`） |
| 成功判据 | Parent SC 005、Parent SC 008 | 全部纳入（本地 `SC-001`、`SC-002`） |
| 共享字符串 | Parent STR 001–Parent STR 003、Parent STR 007–Parent STR 010 | 纳入本切片实际引用者（本地 `STR-001`–`STR-007`） |
| 控制层级与授权 | Parent FR 001–Parent FR 006 | 不在本切片；由 `074a-authorized-routing` 已实现面承载，只读引用 |
| 分流裁决 | Parent FR 007–Parent FR 014 | 不在本切片；由 `074a-authorized-routing` 已实现面承载，只读引用 |
| 嵌套调用契约 | Parent FR 015–Parent FR 019 | 不在本切片；由 `074a-authorized-routing` 已实现面承载，只读引用 |
| 引导/维护路径分流面 | Parent FR 025 | 不在本切片；由 `074a` 本地 FR 020 承载，只读引用 |

本切片 FR 定义总数 = 8（本地 `FR-001`–`FR-008`），落在分解门 8–30 区间内。

## Parent Mapping（父条目逐条映射）

**读法**: 左列是本切片的本地编号（定义行在本文件内），右列是父规格 `.specify/specs/074-goal-team-sdd-unification/requirements.md` 的原编号。父规格仍是权威；本表只记录投影关系，不复述父条文的规范内容。

### Slice FR → Parent FR

| Slice FR | Parent FR | 一行含义 |
|----------|-----------|----------|
| `FR-001` | Parent FR 020 | Goal 不新增强制 SDD 字段、不与需求规格建立结构链接；嵌套运行的贡献是观察性的（经团队运行报告与摘要），报告期由团队 supervisor 追加一条携带既有 Target 引用的 ledger 条目，嵌套运行不写任何 tracked 工件 |
| `FR-002` | Parent FR 021 | 团队运行报告契约新增一个强制嵌套段（段标题字面量为 `[[STR-007]]`），逐次列出 outcome、工件与证据路径、分流裁决引用与异常；无嵌套调用的运行必须显式声明而非省略该段 |
| `FR-003` | Parent FR 022 | 团队概念模型必须把自身 Stage 维度（executor/evaluator/optimizer）与 SDD 阶段名册区分开；不得重命名或复用 SDD 阶段名，SDD 阶段名册仍归驱动拥有 |
| `FR-004` | Parent FR 023 | 承载 SDD 的 Agent Template/Instance 必须声明 `[[STR-002]]` 并在职责中写明：它承载驱动、自身不执行阶段命令、止于 review；SDD 阶段执行者能力仍是叶子，不得声明 `[[STR-002]]` |
| `FR-005` | Parent FR 024 | 项目指令只承载指针级分流面：出现写留存变更时到 owner 路径执行裁决；不得复述输入集或裁决表，proactive trigger 不得在缺少分流裁决与有效授权之一时启动 SDD 运行 |
| `FR-006` | Parent FR 026 | 未声明 `[[STR-001]]` 的 Agent 定义或 Team 席位解析为 `[[STR-003]]`，前置探针必须拒绝该接收方点名 SDD driver 的派发；包含性声明：相对验证记录所指基线提交捕获的用例集，前置治理套件用例集必须为超集且既有用例裁决不变 |
| `FR-007` | Parent FR 027 | 对四个既有面（独立 driver 入口契约、070 阶段团队预设契约、064 线/工作树/归属契约、058 U0–U6 契约）保持可加性：不删除、不重命名、不改变既有键/段/入口形态/退出码含义，允许新增；包含性声明：各面契约套件用例集为基线超集且既有用例全通过 |
| `FR-008` | Parent FR 028 | 框架不得新增自动 merge 或 push、调度器或守护进程、自动 feedback 传输、或第二个确认门 |

### Slice SC → Parent SC

| Slice SC | Parent SC | 一行含义 |
|----------|-----------|----------|
| `SC-001` | Parent SC 005 | 相对验证记录所指基线提交捕获的变更前用例集，变更后的 team、Agent 与独立 driver 契约套件用例集为超集，且每条变更前用例裁决不变 |
| `SC-002` | Parent SC 008 | 相对嵌套运行之前捕获的 goal 夹具，运行后解析出的 Goal 字段集完全一致，且任何 Target 归因只经既有 ledger 引用解析 |

### Slice STR → Parent STR

| Slice STR | Parent STR | 一行含义 |
|-----------|------------|----------|
| STR-001 | STR-001 | 授权能力键名 `"sdd-invocation"` |
| STR-002 | STR-002 | 能力/策略允许值 `"allowed"` |
| STR-003 | STR-003 | 能力/策略禁止值与缺省值 `"forbidden"` |
| STR-004 | STR-007 | 嵌套运行 outcome `"completed"` |
| STR-005 | STR-008 | 嵌套运行 outcome `"blocked"` |
| STR-006 | STR-009 | 嵌套运行 outcome `"failed"` |
| STR-007 | STR-010 | 团队运行报告嵌套段标题字面量 `"## Nested SDD Runs"` |

## Overview

The parent Feature 074 requirement establishes one control hierarchy — Goal → Team → Agent — inside which an SDD run is a subordinate execution path that an authorized team member may start. The first slice, `074a-authorized-routing`, delivered the hierarchy statement, the two-half authorization, the deterministic routing verdict, the governed depth-2 nesting predicate, and the nested invocation contract that ends at review with a structured handoff. This second slice delivers what the outer layer does with that handoff: it makes the nested result consumable and auditable by the Team and Goal layers, and it diffuses the SDD vocabulary into every Goal/Team/Agent surface without duplicating a single fact.

Concretely, the slice (a) fixes the attribution boundary — the Goal gains no mandatory SDD field and no structural link to a requirements specification, and a nested run's contribution is observational through the team run report plus one ledger item carrying the existing Target reference written by the supervisor, (b) makes the team run-report contract's nested section mandatory (with the verbatim heading literal) and explicit-when-empty, (c) disambiguates the team's own Stage dimension from the SDD stage roster, (d) fixes the responsibility statement an SDD-hosting Agent declaration must carry and the prohibition on a stage executor declaring the hosting capability, (e) keeps the project instructions at pointer level and forbids the proactive trigger from starting a run without both a routing verdict and effective authorization, and (f) states the two compatibility obligations — the `forbidden` default with its pre-dispatch suite containment claim, and additivity on the four named predecessor surfaces — as decidable containment claims rather than assurances.

Every concept this slice touches keeps its existing owner: the routing owner document, the anti-nesting owner, the neutral metadata key set, the team report contract, the Goal/Target model, the line/ownership primitives, and the driver's stage roster are all reached by reference. This slice creates no new command, no new skill, no new store, and no second definition point.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - The outer layer consumes the nested result (Priority: P2)（父 US4）

A nested run ends at review and hands back its outcome, artifacts, evidence, and any unresolved review findings. The invoking agent and the team run report surface that handoff verbatim or by stable path; a blocked or failed nested run can never be reported as success; the Goal layer sees the contribution observationally, attributed through the existing ledger Target reference, with no new mandatory Goal field.

**Why this priority**: "Goal/Team above SDD" is only real if the upper layer owns the result and the decision to merge. Without the handoff the hierarchy is nominal; within this slice it is the higher-priority story because the diffusion story (US2) delivers value only once the consumption surface exists.

**Independent Test**: Run a fixture team with one nested SDD run to review; inspect the team run report and the Goal archives, and assert the nested section, the evidence paths, the absence of merge/push, and the absence of any new Goal field.

**Acceptance Scenarios**:

1. **Given** a nested run that completes review, **When** the team run report is written,
   **Then** it contains the nested-SDD section with outcome [[STR-004]], artifact paths, and
   evidence paths.
2. **Given** a nested run that is blocked or fails, **When** the invoking agent reports,
   **Then** the report carries [[STR-005]] or [[STR-006]] and the outer run is not marked
   successful.
3. **Given** a nested run attributed to a Target, **When** the goal archive is inspected,
   **Then** attribution appears only through the existing ledger reference and no new
   mandatory Goal field exists.

---

### User Story 2 - SDD concepts are diffused without being duplicated (Priority: P3)（父 US5）

Goal, Team, Agent, and instruction surfaces each gain the minimum vocabulary they need to reason about SDD: the team report can describe a nested run, agent definitions can declare the capability, the instructions can point at the routing rule, and the team's own Stage dimension is explicitly disambiguated from SDD stages. Every fact is referenced from its existing owner rather than copied.

**Why this priority**: Diffusion is what makes the hierarchy usable day to day, but it delivers value only after the invocation, routing, and governance slices exist — and after the consumption surface of US1 exists. Its lower priority within this slice reflects that ordering, not lower importance to the feature.

**Independent Test**: Run the documentation/contract checks that detect duplicated stage rosters and unknown keys, and confirm every new surface cites its owner and the team Stage vocabulary is unchanged.

**Acceptance Scenarios**:

1. **Given** the team conceptual model, **When** SDD stages are discussed, **Then** the model
   states that its Stage dimension is not the SDD stage roster and no value is renamed.
2. **Given** the project instructions, **When** an agent considers a write-bearing change,
   **Then** the instructions point at the routing owner and do not restate its input set or
   verdict table.
3. **Given** an agent definition that hosts SDD, **When** it is validated, **Then** it
   declares the capability and states that it hosts the driver, never executes stage commands
   itself, and ends at review.

---

### Edge Cases

- **Review returns unresolved findings**: the nested run repairs within its own loop; if it
  cannot, it returns a failed handoff carrying the findings, and the outer layer adjudicates.
- **The handoff lacks its integration identity**: the outer layer cannot integrate; the handoff
  is incomplete and the run MUST NOT be reported successful.
- **Stall, timeout, or budget exhaustion**: the nested run stops, persists its state spine, and
  returns a failed handoff with the required elements; the outer team's failure isolation and
  reporting apply.
- **A team run with no nested invocation**: the nested section is present and states that no
  invocation occurred; omitting the section is a contract violation even when the correct
  content would have been "none" (parent FR 021, second sentence).
- **The recorded routing verdict cannot be located for the section's reference**: the section
  records the reference as missing and the outer layer MUST NOT re-derive a verdict; a
  fabricated or re-computed reference is a contract violation (parent contract C-54; the
  verdict itself is 074a's record).

## Requirements *(mandatory)*

### Functional Requirements

**Outer-layer consumption and handoff**

- **FR-001**: A Goal MUST NOT gain a mandatory SDD field or a structural link to a
  Requirements spec. A nested run's contribution to a Goal is observational through the team
  run report and summary. At report time, the team supervisor — the sole writer of tracked
  artifacts — MUST append one ledger item carrying the existing Target reference; the nested
  run MUST NOT write tracked artifacts, and no new Goal field is introduced.
- **FR-002**: The team run-report contract, owned by `create-team/SKILL.md` § Report contract, MUST gain a mandatory nested-SDD section ([[STR-007]]) that lists, per invocation, an outcome of [[STR-004]], [[STR-005]], or [[STR-006]],
  together with its artifact and evidence paths, its routing-verdict reference, and its
  anomalies. A run with no invocation MUST state that explicitly rather than omitting the
  section.

**Diffusion into the Goal/Team/Agent system**

- **FR-003**: The team conceptual model MUST disambiguate its Stage dimension
  (executor/evaluator/optimizer) from the SDD stage roster. No team Stage value may be renamed
  or overloaded with an SDD stage name, and the SDD stage roster remains owned by the driver.
- **FR-004**: An Agent Template or Instance that hosts SDD MUST declare [[STR-002]] and state in
  its responsibilities that it hosts the driver, does not execute stage commands itself, and
  ends at review. The SDD stage-executor capacity remains a leaf and MUST NOT declare
  [[STR-002]].
- **FR-005**: The project instructions MUST carry a pointer-level routing surface: when a
  write-bearing change is proposed, run the decision at the owner's path. The instructions MUST
  NOT restate the input set or verdict table, and the proactive trigger MUST NOT start an SDD
  run without both a routing verdict and effective authorization.

**Compatibility and safety**

- **FR-006**: An Agent definition or Team seat that carries no [[STR-001]] declaration MUST resolve to [[STR-003]], and the pre-dispatch probe MUST reject any dispatch for that recipient that names an SDD driver.
  As a decidable containment claim: relative to the baseline case set captured at the
  pre-change commit named in the verification record, the post-change case set of the
  pre-dispatch governance suite MUST be a superset, and every pre-change case MUST return the
  same verdict.
- **FR-007**: The feature MUST be additive on the four named surfaces: the standalone
  `sdd-loop-driver` entry contract, the Feature 070 stage-team preset contract, the Feature 064
  line/worktree/ownership contract, and the Feature 058 U0–U6 contract. On each surface it
  MUST NOT remove, rename, or change the meaning of an existing key, section, entry form, or
  exit code; additions are permitted. As a decidable containment claim: for each surface, the
  post-change contract-suite case set MUST be a superset of the pre-change case set captured
  at the baseline commit in the verification record, and every pre-change case MUST pass.
- **FR-008**: The framework MUST NOT add automatic merge or push, a scheduler or daemon,
  automatic feedback transmission, or a second confirmation gate.

### Key Entities *(include if requirement involves data)*

- **Control Layer**: One rung of the hierarchy — Goal, Team, Agent, or SDD Invocation. Each
  layer has an owner and a boundary; a lower layer never mutates an upper layer's definition.
- **SDD Invocation**: A bounded nested SDD run started by an authorized seat. Carries the
  invoking team and seat, the Goal/Target, the authorized scope, the routing verdict, the line
  identity, the integration identity, the outcome, and the artifact/evidence paths.
- **Routing Verdict**: The decision record — declared inputs, verdict, reason code from the
  closed vocabulary, actor, and any user override. This slice consumes a recorded verdict by
  reference; it never produces one.
- **Integration Identity**: The line id, branch, worktree path, and HEAD commit that let the
  outer layer locate and integrate a completed nested run.
- **Nested Run Handoff**: The structured return from a nested run — outcome, stages reached,
  artifact and evidence paths, unresolved findings, integration identity, and an anomaly line.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Relative to the pre-change case set captured at the baseline commit named in the
  verification record, the post-change team, Agent, and standalone-driver contract suites have
  a superset case set, and every pre-change case returns the same verdict.
- **SC-002**: Relative to the goal fixture captured before the nested run, the post-run parsed
  Goal field set is identical, and any Target attribution resolves only through the existing
  ledger reference.

### Measurement Sources & Collection Methods

- **SC-001 Source**: The existing team, Agent, and `sdd-loop-driver` contract suites, run
  unchanged against the pre-change baseline and the post-change tree; the case set of each
  suite is its collected test-node-id set, frozen at the pre-change commit before any edit, and
  the check asserts set containment (post ⊇ pre) plus identical verdicts for the shared ids
  (parent contract C-62).
- **SC-002 Source**: A goal fixture validated with the goal engine before and after a scripted
  nested run; the contract test compares the parsed goal field set.

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `"sdd-invocation"` | schema-default and pre-dispatch governance tests; local FR-006 default resolution |
| `STR-002` | `"allowed"` | SDD-host Agent responsibility contract; local FR-004 declaration requirement |
| `STR-003` | `"forbidden"` | schema-default and backward-compatibility tests; local FR-006 absent-declaration resolution |
| `STR-004` | `"completed"` | team run-report contract test; local FR-002 outcome value |
| `STR-005` | `"blocked"` | team run-report contract test; local FR-002 outcome value |
| `STR-006` | `"failed"` | team run-report contract test; local FR-002 outcome value |
| `STR-007` | `"## Nested SDD Runs"` | team run-report contract test; local FR-002 mandatory heading literal |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Boundary and Ownership (non-duplication)

| Concern | Existing owner | This slice's relationship |
|---------|----------------|-----------------------------|
| Goal, Target, and Goal–Team binding | `goal-definitions.md` | Reference; no structural link and no new mandatory field (FR-001) |
| Team conceptual model, patterns, run report | `create-team` / `run-team`; report contract in `create-team/SKILL.md` § Report contract | Amend in place exactly once: one mandatory section added; the Stage dimension disambiguated with no value renamed (FR-002, FR-003) |
| Anti-nesting obligation, depth-2 chain, virtual prohibition, authorization predicate | `subagent-definitions.md` § Dispatch-Time Governance Obligation; amended by `074a-authorized-routing` | Reference only; this slice adds no second amendment and restates no predicate |
| Routing decision, its input domains, verdict table, reason codes | `shared/definitions/sdd-routing-definitions.md`; engine `scripts/python/sdd-route.py` (both delivered by `074a`) | Reference by path; the instructions surface points at the owner and restates nothing (FR-005) |
| Neutral metadata key set and host-rendering exclusion | `src/specify_cli/__init__.py` (`NEUTRAL_AGENT_METADATA_KEYS`); key registered by `074a` | Reference; the authoring baseline entry points at the key set rather than redefining its values (FR-004) |
| Agent Template / Instance / Execution definitions | Feature 060 / `agent-definitions.md`; `run-agent` authoring baseline | Reference; one responsibility clause added to hosting declarations (FR-004) |
| U0–U6, state spine, stage sentinels, stall handling, stage roster | Feature 058 / `sdd-loop-driver` | Reference and preserve; the roster stays the driver's (FR-003, FR-007) |
| Line registry, worktree-per-write-line, ownership, integration queue | Feature 064 / `sdd-loop-driver/SKILL.md` Hard Requirement 11 | Reference; one of the four additivity surfaces (FR-007) |
| Stage-team preset and work-package decomposition | Feature 070 | Preserve; one of the four additivity surfaces (FR-007) |
| Flow class, fast-fail, confirmation gates, Task Complexity Rubric, proactive trigger | Features 069 / 052 and the shared guidelines; `shared/guidelines/proactive-trigger.md` | Reference by path; the trigger gains one pointer sentence, no rule copy (FR-005) |

## Assumptions

*Assumption identifiers retain the parent labels. Parent `A2`, `A3`, `A4`, `A6`, `A7`, `A9`, `A11` and `A12` describe the authorization, routing and nesting-predicate faces delivered by `074a-authorized-routing`; they are not restated here.*

- **A1**: This is a framework-source change under the two-hats rule; it lands in the sources and
  reaches client projects through the normal publish/install/init flow.
- **A5**: A nested SDD run is the only sanctioned nesting. Feature 070 work packages remain the
  only in-run decomposition; no third nesting form is introduced.
- **A8**: Goal and Requirement remain on different planes with no structural link; observational
  attribution is the only connection.
- **A10**: The nested run's review stage may include the driver's existing review-repair loop of
  Feature 063; ending "at review" means after that loop settles, not before findings are
  addressed — which is why an unresolved-findings handoff reaches the outer layer already
  repaired-once or explicitly failed.
- **A13**: The team supervisor writes the ledger attribution row; the nested run writes no
  tracked artifacts.

## Out of Scope

- **074a 承接（显式记录，只读引用）**: 父 `FR 001`–`FR 006`（控制层级 + 双层授权 + 深度 2 嵌套谓词）、父 `FR 007`–`FR 014`（三值分流裁决与路由 owner 文档）、父 `FR 015`–`FR 019`（nested invocation 入口与 handoff 核心）、父 `FR 025`（引导/维护路径分流面，`074a` 本地 FR 020）、父 `SC 001`–`SC 004`、父 `SC 006`、父 `SC 007`，以及父 `STR 004`–`STR 006`、`STR 011`。以上已由 `074a-authorized-routing` 实现并合入 `master`；本切片**不定义、不实现、不改写**它们，只在需要处按路径引用其已实现面（`scripts/python/sdd-route.py`、`shared/definitions/sdd-routing-definitions.md`、`skills/external/sdd-loop-driver/references/nested-invocation.md`、`sdd-invocation` 中立键、`subagent-definitions.md` 深度 2 链）。
- Automatic merge or push by a nested run.
- Changing the internal workflow of any individual `/speckit.*` stage command.
- Allowing stage executors to drive, dispatch, or load any driver.
- Multiple levels of SDD nesting (SDD inside SDD).
- Replacing the Feature 070 work-package model or the Feature 064 line/ownership model.
- Automatically making every Agent SDD-capable.
- Adding a scheduler, daemon, second confirmation gate, or automatic feedback transmission.
- Rewriting the anti-nesting rule for dispatches that do not satisfy the authorization predicate
  (that predicate is `074a`'s closed form; this slice only asserts its containment behaviour).
- Re-deriving, re-computing, or writing back a routing verdict inside the report section; the
  outer layer reads 074a's recorded verdict by reference.

## Cross-Slice Design Attribution（跨切片交付归属）

**读法**: 本节裁定本切片与 `074a-authorized-routing`、父设计（`.specify/specs/074-goal-team-sdd-unification/plan.md` 与同目录 `contracts/`）之间的交付归属。它不改写 `## Requirements`、`## Success Criteria`、`## Out of Scope` 的任何条文，只说明本切片如何兑现它们；父设计文件是投影来源，不是切片边界。

- **D-1 归属按需求条目切分，不按父设计文件的物理分组**：本切片的设计集覆盖本地 `FR-001`–`FR-008` 与 `SC-001`–`SC-002`。凡对应父条款，无论落在哪个父 contract 文件，都整体继承为来源并保留父条款编号作来源标注——本切片主要读 `report-and-attribution.md`（父 C-47–C-54）与 `diffusion-and-compat.md`（父 C-55–C-67），并只取其中属于本切片 8 条父 FR 的条款；`diffusion-and-compat.md` 里属 `074a` 的条款（例如父 C-58、C-59 的 invocation-kind 分类与引导/维护授权面，以及 C-64、C-66 中涉及 074a 本地 FR 018、FR 014 的部分）由 `074a` 已继承并实现，本切片不重复认领。
  理由：拆分记录（`.specify/state/074-goal-team-sdd-unification.md` § 拆分记录，`confirmed-user`）按需求条目切分，并声明两片 FR 集互斥、并集 = 28。父 contract 文件按主题而非按切片组织，按文件分组会让归属漂移。
- **D-2 分流裁决的引用面在本切片只读，不重算**：本地 `FR-002` 要求的 routing-verdict reference 指向 `074a` 在 Agent 执行证据中记录的那条裁决（输入、裁决、理由码、actor、用户覆盖），由 handoff 与调用方结果按稳定路径引用。本切片不得重算该裁决、不得在段内复制其输入集或裁决表（父 contract C-54）。
  理由：`074a` 的 D-2 已裁定切片内的裁决记录面为 Agent 执行证据，并声明 report 段的 verdict reference 在 074b 落地时读同一条记录、不得重算。本条是那次交接的接收端。
- **D-3 `## Nested SDD Runs` 段标题字面量与段语义归本切片**：父 `STR 010` 的固定标题（本地 `STR-007`）与「每次运行强制存在、无嵌套则显式声明 none」的段语义由本切片兑现；`074a` 的 D-3 明确把该标题与段语义留给 074b，因此本切片的契约与夹具是这两项的唯一落点。
  理由：与 `074a` 的 D-3 互补；两片合起来恰好覆盖父 `SC 003`（内容面在 074a，段格式面在此），不产生第二定义点。

## Clarifications

### Session 2026-10-29

- Q: 本切片的编号为何与父规格 074 不同？ → A: 本切片是父规格 074 的两片拆分投影（用户 2026-10-28 确认，`confirmed-user`，见 `.specify/state/074-goal-team-sdd-unification.md` § 拆分记录（tasks U4，2026-10-28）），不是新的需求裁定。切片内 FR / SC / STR 采用连续本地编号，逐条父映射见 `## Parent Mapping`；父规格仍是权威，编号变化不构成删除、合并或重排。
- Q: 父规格既有裁定对本切片是否仍然生效？ → A: 生效，且不重开裁定。父规格 `## Clarifications` > `### Session 2026-10-28` 与父 `### Session 2026-10-29` 的裁定对纳入本切片的条目原样适用：嵌套止于 review 交接；合并 main 与 push 由外层 goal/team 层按确认门决定；Goal 与 Requirements 保持不同平面、只经既有 ledger Target 引用观察性归因；team report 段标题为固定字面量且无嵌套时显式声明；四面可加性与包含性声明按基线用例集判定。
- Q: `074a` 的 D-2（分流裁决记录面 = Agent 执行证据）在本切片如何落地？ → A: 本切片只接收引用，不重算（见 `## Cross-Slice Design Attribution` D-2）。本地 `FR-002` 的 routing-verdict reference 与 `074a` 在 Agent 执行证据中记录的同一条裁决绑定，段内只承载引用；不得在段内复制输入集、裁决表或理由码词表。**无人值守自裁**——`074a` 的 D-2 原文已明确「随 074b 的段契约落地时读同一条记录，不得重算」，只有一种与已记录意图一致的读法，属纠正而非裁定。
- Q: `## Nested SDD Runs` 段标题字面量与「无嵌套则显式声明」的段语义归哪一片？ → A: 归本切片（见 D-3）。父 `STR 010` 在本切片重编号为 `STR-007` 并作为段标题唯一字面量；`074a` 的 D-3 把该标题与段语义明确留给 074b，故本切片是该面的唯一落点。**无人值守自裁**——两片 D-3 的边界已由 `confirmed-user` 的拆分记录与 `074a` 已提交文本共同钉死，无第二种读法。
- Q: 父 `FR 025`（引导/维护路径分流面）是否需在本切片重新承接？ → A: 不需要。它已由 `074a` 的本地 FR 020 承接并实现；本切片 `## Slice Scope` 与 `## Out of Scope` 均把它列为只读引用项，避免两片各自定义同一条裁决面（两片 FR 集互斥且并集 = 父 28 条）。
