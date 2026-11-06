# Requirements Specification: Speckit 框架可视化（Speckit Framework Visualization）

**Requirement Branch**: `087-speckit-visualization`
**Created**: 2026-11-06
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Input**: User description: "以 087- 为前缀开发一个新特性: speckit框架可视化. 当前speckit框架中合入了大量的并发,异步操作流程,随着并发度增大和越来越多的异步流程, 用户也越来越难以获取到当前正在进行的任务的信息.  需要将speckit可视化提升到一个重要的基础特性. 重点在于用户使用speckit的时候能够随时掌握现状. 具体做法需要在启动异步流程的时候给用户留一个信息输出机制,例如 每个team都应该有一个reporter subagent, 以固定周期(每30秒)向控制台输出当前整体进展和状态;  启动带监视架构的主从结构时(如skills/external/coaching-skills技能),主流程也应该随时汇报子流程的状态和进展."

## Related Feature *(mandatory)*

**Feature ID**: 087
**Feature Name**: Speckit 框架可视化（Speckit Framework Visualization）

## Overview

As the framework accumulates concurrent and asynchronous flows, a user watching a run can no
longer tell what is happening: many agents run at once, each works inside its own context, and
nothing reaches the user's screen until a task finishes or fails. The information a user needs is
produced continuously — records already exist on disk and dispatch wrappers already stream
progress — but it is neither surfaced at a known cadence nor reachable from the surface the user
is actually looking at.

This feature makes **current-state visibility a first-class framework capability** rather than a
property each flow implements or forgets. Three surfaces become non-optional for every flow that
introduces concurrency or an asynchronous delegation:

1. **A declared periodic status line** — every team carries a reporter seat (a subagent bound to a
   purpose-built template) that emits one short status line to the host console on a fixed
   cadence, default every 30 seconds.
2. **A master-reporting duty** — every supervising structure (a master that dispatches and watches
   sub-flows, e.g. `skills/external/coaching-skills`) reports the state of the sub-flows it
   watches on the same cadence instead of going silent while they run.
3. **A reachability floor** — the user can always obtain a current-state digest on demand, without
   reading raw logs, so "what is running right now?" has a one-question answer.

The three surfaces reuse what exists. Progress Reporting already owns the cadence discipline and
the four-element content floor (`shared/guidelines/progress-reporting.md`); the External Dispatch
Visibility Contract already owns the artifact triplet and liveness monitoring
(`shared/definitions/subagent-definitions.md`); the team store, the agent template store and the
line registry already own the state these lines report. **No new store, scheduler, daemon, console
channel or second registry is introduced** — this feature wires existing owners into a declared,
testable reporting obligation.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A team run reports its overall state every 30 seconds (Priority: P1)

A user launches a team run of many minutes. While it runs, the session shows one short status line
every 30 seconds: where the run stands, what changed since the last line, what remains, and any
blocker (or an explicit "no blocker"). The line comes from a dedicated reporter seat on the team,
not from the working members, so no member's silent work turns into the user's blackout.

**Why this priority**: This is the user's stated core case and the one every other surface
generalizes from; without it the feature has no observable deliverable.

**Independent Test**: Run a fixture team with a stub member that sleeps past two cadence
intervals; assert that a reporter seat exists in the roster, that status lines appear at the
declared cadence with all four content elements, and that the lines name the team slug and the
run stamp so a reader can attribute them.

**Acceptance Scenarios**:

1. **Given** a team whose run lasts longer than two cadence intervals, **When** the run executes,
   **Then** at least three status lines reach the host console, each stamped with the team slug and
   run stamp and each carrying position, delta, remainder and blocker status.
2. **Given** a run that reaches a stage boundary between two ticks, **When** the boundary is
   crossed, **Then** an extra line is emitted at the boundary and the periodic cadence is not reset
   by it.
3. **Given** a team definition created after this feature lands, **When** its roster is validated,
   **Then** a missing reporter seat is reported as a named defect naming the seat, and a team that
   cannot run a reporter records the declared reason instead of silently omitting it.

---

### User Story 2 - A supervising master reports the state of the sub-flows it watches (Priority: P1)

A user starts a monitored master/subordinate structure — a master that dispatches worker
sub-flows and watches them, such as the coaching loop over a trainee skill — then walks away. The
master keeps reporting: how many sub-flows it dispatched, which ones are running, which finished,
which stalled or failed, and how long each has been running without progress. The subordinate work
happens out of sight; the master's report is what keeps it observable.

**Why this priority**: The user named this case explicitly, and it is the case where silence is
most costly: a monitoring structure whose own monitoring is invisible to the user is
indistinguishable from a hang.

**Independent Test**: Run a fixture supervising flow over two stubbed sub-flows (one completing,
one stalling past the declared stall threshold); assert that the master emits a per-sub-flow status
report on the cadence, that the stalled sub-flow is reported as stalled rather than as running, and
that no sub-flow is omitted from the report.

**Acceptance Scenarios**:

1. **Given** a supervising flow with two running sub-flows, **When** one cadence interval elapses,
   **Then** the master's next report names both sub-flows with their states and elapsed times, and
   reports every dispatched sub-flow at least once.
2. **Given** a sub-flow whose progress output has not grown beyond the declared stall threshold,
   **When** the next report is due, **Then** the report marks it stalled and names the threshold and
   the measured silence, instead of repeating its last known state as current.
3. **Given** a supervising flow that observes a subordinate fail, **When** the failure is detected,
   **Then** the report is emitted immediately, before the next cadence tick.

---

### User Story 3 - The user can ask for a current-state digest at any moment (Priority: P2)

At any point during a long unattended run the user asks "where is this?" — and gets one digest:
which lines and work packages are active, which agents are dispatched, what each is doing, how long
each has been quiet, and what finished most recently. The digest is a projection of the state the
framework already records; it does not require the user to open logs or worktrees.

**Why this priority**: The cadence line covers "keep me informed without asking"; the digest covers
"let me ask". Both were named by the user as "随时掌握现状", but the cadence line alone already
satisfies the core need.

**Independent Test**: Mid-run, invoke the digest entry; assert it returns a bounded summary within
a stated size, that every entry it lists resolves to a state artifact on disk, and that a run with
no dispatch in flight renders an explicit "nothing running" rather than an empty result.

**Acceptance Scenarios**:

1. **Given** an active multi-line run, **When** the user requests the digest, **Then** one bounded
   summary is returned naming active lines, dispatched agents and their last observed activity.
2. **Given** a state artifact that has not been updated since an earlier tick, **When** the digest
   is rendered, **Then** its age is shown rather than its data being presented as current.
3. **Given** a repository with no active run, **When** the digest is requested, **Then** it reports
   that nothing is running, and exits with the declared "nothing active" status.

---

### User Story 4 - The cadence, content and attribution rules have one owner (Priority: P3)

A maintainer changes the reporting interval, the content elements or the obligation's scope in one
place and every consumer follows: the reporter definition, the supervisory masters, the digest and
the existing wrap-up flows. No consumer carries a second copy of the interval or of the content
floor.

**Why this priority**: Without single ownership this feature immediately becomes the second
progress discipline beside the existing Progress Reporting, and the two drift — the exact failure
the framework's one-source rule exists to prevent.

**Independent Test**: Change the declared default interval in the owner; assert every consumer
reads the changed value with no source edit outside the owner, and that a guard fails if the
literal is reintroduced elsewhere.

**Acceptance Scenarios**:

1. **Given** the declared owner of the cadence and the content floor, **When** a consumer renders a
   status line, **Then** it reaches that owner by path rather than restating its rules.
2. **Given** the owner's default interval, **When** the framework is scanned for that literal,
   **Then** the only definition site is the owner, and every other occurrence is an input the user
   supplied for that run or a dated record.

---

### Edge Cases

- **Silence is an event, not a liveness proof**: a reporter whose own tick fails or whose runner
  cannot emit must report the failure as a status line and stop claiming the run is healthy;
  "no line" MUST NOT be readable as "progressing".
- **Cadence versus atomic steps**: a tick that falls inside an indivisible step is delivered at
  that step's next boundary with the delay stated, per the progress-reporting owner; the reporter
  MUST NOT split the step to keep the clock.
- **Stall versus slow**: a sub-flow quiet below the declared threshold is "slow", not "stalled", and
  the report says which threshold it is judged against; the threshold is never inferred from a
  wall-clock guess per run.
- **Reporter without a console**: a host or a subagent mode with no live console surface renders
  the same lines into its declared stream artifact instead, and the run records which carrier was
  used, so the cadence obligation holds in every execution mode.
- **Several teams in one session**: interleaved status lines stay attributable — each line names
  its team slug and run stamp, and two teams MUST NOT be able to produce an identical unattributed
  line.
- **Reporting budget exhaustion**: a run whose budget policy drops to report-only still reports —
  the status line is the cheapest thing the run does and is not the first thing to be dropped.
- **A reporting seat that becomes a second orchestrator**: the reporter observes and reports; it
  MUST NOT dispatch, authorize, retry or terminate work, and a reporter observed mutating anything
  outside its own stream artifact is a defect.
- **Digest during a stall**: the digest must remain answerable when the escalated line stream is
  stalled — it reads state artifacts, not the reporter's process.
- **Two cadence profiles in one session**: a run that starts with a live receiver and later loses it
  (every team lane finished, the master stops) switches to the interactive profile at the next
  boundary and says so; the switch is recorded, never silent, and a run MUST NOT report both
  profiles' ticks as if they were one cadence.
- **A reporter that dies mid-run**: the reporter is a dispatch like any other, so its own silence is
  judged by the orchestrator's existing liveness signal and the existing threshold table, and the
  orchestrator's report names it as stalled rather than continuing to claim the run is healthy.
  FR-016 is satisfied through that existing signal, not through a second detector.
- **A single-dispatch supervisor judged against the predicate**: the coaching skill dispatches
  exactly one subordinate per run, which the FR-002 wording "keeps one or more asynchronous
  delegations past their dispatch" already covers; it is therefore in scope without needing a
  special case, and its report names that one subordinate rather than reporting an empty set.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The framework MUST declare current-state visibility as a first-class capability with
  a single owning document under `shared/`, which owns: the obligation's scope (which flows must
  report), the default cadence value, the reporter-seat obligation, the master-reporting duty and
  the digest's contract. The owner MUST reference the existing progress-reporting discipline and
  the existing visibility contract rather than restating either.
- **FR-002**: The owning document MUST define the obligation's **scope as a decidable predicate**:
  a flow is in scope when it dispatches two or more concurrent units, or holds one or more
  asynchronous delegations it continues past their dispatch. A single synchronous step is out of
  scope, and an out-of-scope flow MUST be able to say so in one line rather than emitting an empty
  report.
- **FR-003**: Every in-scope supervised structure — a team, or a master that dispatches and watches
  sub-flows — MUST emit a status report on a fixed cadence, using the cadence profile FR-020 selects
  for its run, and the cadence MUST remain configurable per run and per structure without a source
  edit. This requirement names no interval value: FR-020 is the single definition site of both
  profiles' defaults.
- **FR-004**: Every status report MUST carry, in the progress-reporting discipline's content
  terms: the structure's identity (slug and run stamp), the current position in its plan, the
  change since the previous report, what remains with a rough estimate or the stated reason none
  can be given, and the blocker status with "no blocker" written explicitly when none exists. The
  element set is reached from the discipline owner by path; this requirement names no second set.
- **FR-005**: The framework MUST ship an agent **Template** for the reporting role, distributed in
  the framework's agent template source and usable by any team or supervisory structure; its
  capability surface MUST be sufficient to read the state it reports and MUST NOT include the
  authority to dispatch, authorize, retry, terminate or write outside its own stream artifact.
- **FR-006**: The population the reporter-seat obligation binds is exactly two sets and no third:
  **(a)** every team roster created or modified through the framework's team-creation entry
  (`skills/internal/create-team/` invoked by `/speckit.team`) **from the commit that delivers this
  feature onward**, and **(b)** every roster handed to validation or run explicitly by path. Every
  roster in that population MUST carry one **reporter seat** bound to the template of FR-005 with
  the reporter's territory declared; roster validation MUST report a missing reporter seat as a
  named defect naming the seat, and MUST accept an explicit, recorded reason when a team
  legitimately cannot host one. Every roster outside that population — notably the rosters that
  already exist in the repository when this feature lands — is **not** bound by this requirement:
  this feature MUST NOT retroactively amend them, they MUST NOT be judged against the seat
  obligation at their pre-existing revision, and they MUST NOT become unrunnable because of it.
  Inside the population, the only accepted escape remains the recorded reason (the FR-021 channel,
  `all-lanes-in-session-single-interval` or `host-cannot-host-reporter`); outside it, no
  disposition is owed at all, and no per-roster backfill is a deliverable of this feature.
- **FR-007**: Every team run MUST emit the reports FR-003/FR-004 require, with each line attributed
  to its team slug and run stamp, and MUST record which carrier (live console, or the declared
  stream artifact when no live console exists) actually received them.
- **FR-008**: A supervising flow that dispatches and watches sub-flows MUST report the state of
  **every** dispatched sub-flow rather than of itself alone: each sub-flow's identity, its state
  (running / completed / stalled / failed), and the age of its last observed activity.
- **FR-009**: The supervising report MUST judge each sub-flow against a **declared stall
  threshold**, MUST distinguish "slower than the threshold" from "stalled", and MUST state which
  threshold the judgement used. The threshold MUST be a declared value, not a per-run guess.
- **FR-010**: A supervising flow MUST emit an out-of-cadence report when it observes a state
  transition of significance (sub-flow failure, stall crossing, dispatch failure), before the next
  tick, and MUST NOT let the transition wait for the clock.
- **FR-011**: The framework MUST provide a **current-state digest** entry whose output is one
  bounded summary of the active state: active lines and their states, dispatched agents with their
  last observed activity and its age, and the most recent completions. The digest MUST read state
  artifacts rather than require a reporter process to be alive, MUST mark stale data with its age,
  and MUST render an explicit "nothing running" state. **Workspace rule**: the digest MUST list only
  the registry entries whose `project_dir` equals the current workspace, and MUST NOT list entries
  belonging to another project at all — this exclusion is the chosen reading of the two options the
  analyze report left open, so no `other-project` label is rendered and no entry outside the current
  workspace is counted against the FR-012 cap.
- **FR-012**: The digest's size MUST be bounded by a declared cap, with the number of entries it
  omitted stated when it truncates, so that the answer to "what is running?" is one screen and not
  a log dump.
- **FR-013**: The framework's existing supervised delegation path MUST carry the reporting
  obligation into every dispatch payload, in the same way the fast-fail clause and the progress
  obligation already are, and the shipped examples that the user named MUST demonstrate the
  subordinate-state report. The owner document, not the shipped example, defines the duty.
- **FR-014**: The reporting obligation MUST hold in every execution mode of the subagent model; a
  mode with no native live surface MUST use its already-declared stream carrier, and the run record
  MUST say which mode and which carrier were used. No fourth mode or second carrier is introduced.
- **FR-015**: A status report MUST NOT become an approval request: it is a one-way statement, it
  never waits for a response, and its presence never authorizes an action.
- **FR-016**: The **emitting flow's own** reporting loop MUST NOT swallow its own failure: a run whose
  reporting loop cannot emit MUST surface that as a named condition, and MUST NOT leave the user
  reading absence as health. This requirement governs that loop only; a reporter that stops growing
  after a successful emission is a different event and is adjudicated by the visibility contract's
  existing liveness signal (A15), not by this requirement and not by a second detector.
- **FR-017**: The framework MUST ship a deterministic guard that judges the mechanically decidable
  propositions of this obligation — reporter seat present or an explicit recorded reason, cadence
  value present and read from the owner, report lines carrying the identity and the element set,
  digest bounded and naming staleness — and returns a verdict with named statuses.
- **FR-018**: The feature MUST NOT introduce a scheduler, a timer service, a daemon, a third-party
  dependency, a new persistent store, a new console channel, or a second registry, state spine or
  ledger; every state the reporting reads MUST already have an owner, and a fact that would need
  one is declared a new concept instead of being defined inline.
- **FR-019**: The shipped supervising structure the user named — `skills/external/coaching-skills` —
  MUST carry the subordinate-state report: its `## Dispatch Payload` closed field set MUST gain the
  reporting fields the supervision duty requires, and its subordinate's state MUST be reported on
  the cadence rather than only at return. The amendment MUST keep the closed-set invariant (the
  field list stays closed and is extended, never widened to "anything"), and the example MUST NOT
  become the definition of the duty — FR-008/FR-009/FR-010 remain owned by the owner document.
- **FR-020**: The framework MUST read **two declared cadence profiles from one owner** and select
  between them by one declared condition: a long-run profile whose default is **30 seconds**, used
  whenever the run has at least one live status receiver, and the existing interactive profile
  already owned by the progress-reporting discipline, used when it has none. The two profiles MUST
  NOT compete inside one run, and the long-run value MUST have exactly one definition site.
- **FR-021**: Where a structure's lanes are all executed by the current session and the whole run is
  expected to finish inside one cadence interval, the reporter seat MAY be runtime-omitted, and the
  omission MUST be recorded as a declared reason (the same recorded-reason channel FR-006 defines)
  rather than as a silent absence; the orchestrating session then carries the reporting duty itself.
  Outside that condition a reporter execution is required.
- **FR-022**: The current-state digest MUST ship as a thin `speckit.*` command backed by a
  deterministic script, sharing its state reads with the FR-017 guard, so that one reading backs both
  the digest and the guard's verdicts. The command and script names are fixed by the plan stage; this
  requirement fixes only the shape (one command, one script, one reading).

### Key Entities *(include if data involved)*

- **Reporter Seat**: the team-roster seat bound to the reporting template; carries the template
  reference, the reporter's read territory and its write territory (its own stream artifact only).
- **Status Report**: one emitted line or record carrying the structure identity, position, delta,
  remainder, blocker status, cadence tick or trigger reason, and the carrier it was written to.
- **Supervised Sub-flow**: a dispatched asynchronous delegation as seen by its master — identity,
  state, last observed activity and the age of that observation.
- **Stall Threshold**: the declared silence duration beyond which a sub-flow is judged stalled
  rather than slow.
- **Current-State Digest**: the on-demand bounded projection of active lines, dispatched agents and
  recent completions, with per-entry ages and the omitted-entry count.

### Runtime Stack & Dependency Ownership

本特性交付的运行时能力是状态汇报义务的 owner 文本、reporter 席位义务、主从汇报义务、当前态摘要入口与确定性守卫；
其余项由外部供给、本仓只消费，按 `signed-contract` 记。该表是 SC-001、SC-004、SC-005、SC-007、SC-009 的运行时前提。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | Python 3 解释器（运行确定性守卫与契约测试） | signed-contract | CPython 上游（本仓只消费） | `requires-python >= "3.8"`（`pyproject.toml` 已声明，不新增 pin） | `pyproject.toml` | 新增守卫与其测试在 `>=3.8` 解释器上通过；新增脚本 stdlib-only | FR-017 | EP-001 |
| RS-002 | pytest（守卫测试运行器） | signed-contract | pytest 上游（本仓只消费） | 无声明 pin；执行时以 `pytest --version` 原文记录进 test-evidence | `scripts/bash/run-tests.sh` | 基线差集为空且新增守卫测试全绿 | FR-017 | EP-001 |
| RS-003 | agent 宿主（渲染 agent template、承载 reporter 的 live console） | signed-contract | 各受支持 agent 工具上游（本仓只消费） | 无声明 pin；执行时以宿主名 + 版本原文记录进 test-evidence | `docs/reference/cli/supported-agent-tools.md` | SC-001、SC-009 在至少一个受支持宿主上真实运行 reporter 并取原始输出 | FR-005, FR-007, FR-014 | EP-003 |
| RS-004 | line registry 与状态脊（摘要读取的活动状态来源） | signed-contract | 本仓 `skills/external/sdd-loop-driver/scripts/line-registry.py`（消费方，只读） | 同一提交 | `skills/external/sdd-loop-driver/scripts/line-registry.py` | SC-005 的摘要条目逐条解析到该引擎写出的状态文件 | FR-011, FR-012 | EP-001 |
| RS-005 | 状态汇报义务 owner、reporter 模板、reporter 席位义务、主从汇报义务与摘要入口（本特性交付） | in-scope | 本特性 | 同一提交 | `shared/guidelines/progress-reporting.md` | SC-004、SC-007 | FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016, FR-017, FR-018, FR-019, FR-020, FR-021, FR-022 | EP-002 |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A fixture team run lasting more than 90 seconds produces at least three attributed status lines, each naming the team slug and run stamp and carrying all four content elements, and each line's carrier is recorded in the run record. **Path**: final
- **SC-002**: Every roster in FR-006's population — created or modified through the framework's team-creation entry after this feature, or passed explicitly by path — either carries a reporter seat resolvable to the shipped template, or records an explicit reason; a roster in that population missing the seat without a reason fails validation with the seat named, and no roster outside that population is judged. **Path**: final
- **SC-003**: A fixture supervising flow over two stubbed sub-flows — one quiet **beyond** the declared stall threshold, one just under it — reports both sub-flows on each cadence tick, marks the beyond-threshold one `stalled` and the just-under one `slow` with the threshold and measured silence named in both cases, and emits the failure report before the next tick. **Path**: final
- **SC-004**: In every execution mode of the subagent model, a dispatched reporter's output reaches its declared carrier and the mode plus carrier are recorded; no mode is left with neither a live surface nor a declared stream artifact. **Path**: final
- **SC-005**: The current-state digest answers a mid-run request within one bounded summary of at most the declared cap of entries, states the omitted-entry count when truncated, marks stale entries with their age, and renders an explicit "nothing running" state with the declared exit status when no run is active. **Path**: final
- **SC-006**: The default cadence value has exactly one definition site in the framework sources — the scan domain is `shared/`, `templates/`, `skills/` and `agents/`; every other occurrence is either a user-supplied value for one run or a dated record, and the guard fails when the literal is reintroduced elsewhere. **Path**: final
- **SC-007**: The reporting owner document states its scope as a decidable predicate, and a seeded sample of framework flows is classified against it with zero unclassifiable cases and zero flows silently exempted. **Path**: final
- **SC-008**: Pre-existing progress-reporting and dispatch-visibility behavior produces no new failures against the pre-change baseline. **Path**: supporting
- **SC-009**: The full chain runs end to end on the dogfood line: a real multi-minute run reports on cadence, a supervised subordinate flow is reported by its master, a mid-run digest request is answered, and the guard returns a verdict on the line's own artifacts. **Path**: supporting
- **SC-010**: The feature's changed-file set introduces no scheduler, timer service, daemon, new runtime dependency, new persistent store, new console channel, new registry, new state spine or new ledger. **Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**: The fixture team run's captured output and its run record; count lines, parse attribution fields and the four content elements per line; evidence under the feature's `test-evidence/`.
- **SC-002 Source**: The team-creation fixture roster plus the roster-validation guard's verdict and named statuses, stored verbatim in `test-evidence/`.
- **SC-003 Source**: The fixture supervising run's captured reports; the stall-threshold declaration and the measured silence are read from the same record.
- **SC-004 Source**: One dispatch per execution mode with its carrier file and the run record's mode/carrier fields; the artifact triplet paths are recorded as evidence.
- **SC-005 Source**: Two digest runs (active and idle) with exit codes, entry counts, the omitted-entry count and per-entry ages; stored in `test-evidence/`.
- **SC-006 Source**: The owner-literal scan over framework sources plus a seeded-dup drill showing the guard failing; both outputs stored verbatim.
- **SC-007 Source**: The seeded flow sample and the classification result, with the predicate quoted from the owner by path.
- **SC-008 Source**: Pre-change baseline node-id set and the post-change run of the affected progress-reporting and dispatch contract suites.
- **SC-009 Source**: The dogfood run record, the captured cadence lines, the master's subordinate report and the digest output, plus the guard's payload.
- **SC-010 Source**: The changed-file set from `base..head` and a scan for new process-spawn, scheduler and store-creation sites.

## Boundary and Ownership (non-duplication)

| Concern | Existing owner | This feature's relationship |
|---------|----------------|-----------------------------|
| Cadence discipline, four-element content floor, "reporting is not a gate", atomic-step deferral | `shared/guidelines/progress-reporting.md` | This feature's owner consumes it by path; it does not restate the interval rule, the element set or the deferral rule. The long-run 30-second profile of FR-020 is a **declared profile beside** the existing interactive default, not a replacement of it |
| External dispatch visibility: artifact triplet, liveness monitoring, label convention | `shared/definitions/subagent-definitions.md` § External Dispatch Visibility Contract | Reused as the observable carrier; the feature adds the reporting cadence on top and introduces no second carrier |
| Subagent execution modes and mode selection | `shared/definitions/subagent-definitions.md` § Three Execution Modes | Constrains the obligation to hold in all three modes; adds no fourth mode |
| Agent Template / Instance / Execution taxonomy and storage | `shared/definitions/agent-definitions.md` | The shipped reporting definition is a Template in the existing template store; no new layer |
| Team roster schema, seats, territory, patterns, run reports | `skills/internal/create-team/` and `/speckit.team` | Adds the reporter seat obligation to roster creation and validation; keeps the schema |
| Line registry, state spine, per-entry records | `skills/external/sdd-loop-driver/scripts/line-registry.py`, `.specify/state/` | The **line registry is the digest's machine-readable source** — entries resolved exactly as `line-registry.py` resolves them (`$SPECIFY_LINE_REGISTRY_DIR` → XDG `$XDG_STATE_HOME/spec-kit/lines` → `~/.local/state/spec-kit/lines`), read-only; the state spine under `.specify/state/` stays human-readable only. No new store and no second registry |
| Fast-fail clause injection at dispatch | `shared/guidelines/fast-fail.md` § 子代理派发注入 | The reporting obligation rides the same dispatch-payload channel; the clause itself is unchanged |
| Token efficiency, summary-first consumption | `shared/guidelines/token-efficiency.md` | The status line and the digest are summary projections; no raw-log injection is introduced |
| User-facing comprehension of every emitted line | `shared/guidelines/user-facing-comprehension.md` | The emitted lines are a governed surface; the discipline applies unchanged |

## Assumptions

- **A1 — flow class**: Judged `execution` by the acceptance oracle, not by medium. The main
  deliverable is runtime reporting behavior: cadence lines, master-to-subordinate reports, the
  digest entry and its exit status. A defect in it surfaces as observable behavior — no line at the
  expected tick, a sub-flow missing from its master's report, a digest that is empty or unbounded,
  a guard that stays green when the seat is missing — not as a reader misreading a document. The
  `Flow Type` axis applies only to `expression` lines and is written `-`.
- **A2 — the user's stated design decisions are authoritative**: the 30-second cadence, the
  reporter subagent per team, and the master-must-report-subordinates duty are requirements, not
  options. Where this spec narrows them (per-run configurability, declared stall thresholds), it
  adds a declaration point rather than relaxing the decision.
- **A3 — scope is a declared predicate, not a list**: the user's phrase "启动异步流程的时候" is
  read as a decidable condition (FR-002) so that both an auditor and a machine reach the same
  answer for an unlisted flow; the predicate lives in one owner and no per-flow roster of exempt
  flows is maintained.
- **A4 — console is the host conversation surface**: the "host console" is the visible session
  surface the user is already watching. A mode without one writes to its declared stream artifact,
  which is the carrier the visibility contract already defines.
- **A5 — reuse over invention**: no scheduler, timer service, daemon or new store is introduced.
  The cadence is executed by the running flow between its own steps, exactly as the progress-reporting
  discipline already requires; a resident reporter process is explicitly not the mechanism.
- **A6 — one owner**: the new obligation's owner lives in `shared/`; the existing progress-reporting
  document keeps ownership of the cadence discipline and content floor, and this feature's owner
  points at it. The default interval is a single declared literal and is referenced, never copied.
- **A7 — existing behavior is the compatibility baseline**: the pre-change progress-reporting,
  subagent-dispatch and team-creation contract suites are the regression baseline; the feature is
  additive. The reporter-seat obligation's population is exactly FR-006's two sets — the rosters this
  feature creates or modifies through the team-creation entry from its delivering commit onward,
  plus rosters passed explicitly by path — so **no pre-existing team roster is amended, judged or
  made unrunnable by this feature**, and no backfill of `reporting-reason` into an existing roster is
  a deliverable. Inside the population a run that legitimately cannot host a reporter records the
  declared reason instead. This population is the one the plan's RO-04 group must state; the two
  MUST NOT diverge.
- **A8 — historical records are immutable inputs**: dated evidence, prior specs and `.specify/state/`
  records are read, never rewritten.
- **A9 — scope is a union of a predicate and two named surfaces**: the user's two named surfaces —
  the team run and the supervising master/subordinate structure (including
  `skills/external/coaching-skills`) — are a flat minimum set that MUST be covered; the FR-002
  predicate widens the scope beyond them. A flow that implements a supervisor of its own (a pattern
  or skill that dispatches and watches) consumes the shared obligation; a single-dispatch chain
  (the coaching skill's own one-`Trainee`-per-run rule) sits inside that supervisor, so the coach
  reports the state of the one dispatch it actually watches rather than being read out of scope.
  Every other concurrent or asynchronous flow is judged by the predicate alone — no per-flow roster
  of in-scope or exempt flows is maintained.
- **A10 — structure chosen for the owner**: the obligation's owner is a new document
  `shared/guidelines/reporting-obligations.md`, which owns cadence-and-override, obligation scope,
  the reporter-seat obligation, the master-reporting duty and stall judgement, and the digest
  contract. The existing `shared/guidelines/progress-reporting.md` keeps ownership of the anchoring
  rule, the content floor, the late-report rule, the not-a-gate rule, the measured-figures rule and
  the dispatch-payload channel; the new owner references those by section anchor. This keeps A6's
  boundary and SC-008's baseline intact: the pre-existing discipline's clauses are not rewritten.
- **A11 — no register exists for flow states**: the digest's line and agent states are read from the
  **line registry** — owner `skills/external/sdd-loop-driver/scripts/line-registry.py`, entries
  resolved exactly as that engine resolves them (`$SPECIFY_LINE_REGISTRY_DIR`, then XDG
  `$XDG_STATE_HOME/spec-kit/lines`, then `~/.local/state/spec-kit/lines`) — as the machine-readable
  source; the state spine and its per-entry Markdown are read for a human, never to recover a field
  the registry already carries. No flow-state register table is created, and no second state spine is
  introduced.
- **A12 — report lines are visible console output, not a required artifact**: the received carrier is
  recorded in whichever run record the emitting run already writes (team run report, dispatch record,
  supervision record). No line-persistence requirement is added on top, because the no-machinery
  boundary rejects one.
- **A13 — this spec chooses no file paths**: template file names, script paths and entry-point names
  are the plan stage's decisions; the requirements state the store (`agents/` template layer), the
  entry kind (a thin `speckit.*` command backed by a deterministic script) and the guard's
  propositions only.
- **A14 — `Draft` is the feature status this stage lands**: `.specify/shared/workflow/feature-integration.md`
  § Feature Binding Rules § 3 owns that `/speckit.requirements` lands `Draft`, and this stage performs
  the binding without flipping it; the pre-flip transition belongs to a later stage.
- **A15 — a stalled reporter is detected by the orchestrator's existing liveness signal**: the
  orchestrator already monitors a dispatched member's artifact-triplet growth
  (`shared/definitions/subagent-definitions.md` § External Dispatch Visibility Contract point 4) and
  the existing threshold table in `skills/internal/create-team/references/patterns.md` owns the
  numeric stall values. The owner references that table and adds no second threshold set; the
  reporter is a dispatch like any other, so a reporter that stops growing is judged stalled by that
  same signal.

## Out of Scope

- A scheduler, timer service, daemon, background reporting process, or a resident reporter runtime.
- A new persistent store, console channel, registry, state spine, ledger or event bus; a
  second progress discipline beside the existing one.
- A web UI, dashboard, TUI, or any rendering surface beyond the host conversation surface and the
  already-declared stream artifacts.
- Making the reporter an orchestrator: no dispatch, authorization, retry, termination or approval
  authority, and no ability to alter another unit's territory.
- Guaranteed delivery of a status line when the host session is closed; a run with no live surface
  uses its stream artifact and records that fact.
- Rewriting dated historical records, evidence archives, or prior feature specs.
- Replacing the existing interactive progress-reporting default; FR-020 adds a declared long-run
  profile beside it and never removes the interactive one.
- Compressing or deleting the raw artifacts the digest reads; the digest is a projection, not a
  retention change.
- Requiring a status line to be persisted as an artifact of its own; only the carrier that received
  it is recorded, in a run record the emitting flow already writes.
- Renaming or re-specifying the reporter seat's host tool surface; the reporter is a Template in the
  existing template layer and renders through the existing agent rendering path.

## Clarifications

### Session 2026-11-06

<!--
  Reserved for /speckit.clarify. The binding of `Related Feature`, the exact shape of the shipped
  reporter Template's content, and whether the digest ships as a script entry or a thin skill entry
  are left to that stage.
-->

**Mode A — post-requirements; target `.specify/specs/087-speckit-visualization/requirements.md`.
Zero-question mode: the driver authorized self-adjudication, so each entry below records the question
it answers, the adjudicated answer, and the reasoning it rests on. The five-question budget was met
with five closed questions; the reasoning is recorded because the user was not asked.**

- Q: Which Feature does this spec bind to — an existing Feature or a new one? → A: A new Feature,
  **087 · Speckit 框架可视化（Speckit Framework Visualization）**, status `Draft`. Scan result: no
  existing Feature owns "current-state visibility of concurrent/asynchronous flows". The nearest
  neighbours are 070 (task decomposition / coordination), 074 (Goal/Team/Agent × SDD unification),
  085 (temporary Goal/Team and multi-agent concurrency — it owns *how many* agents run, never *what
  the user sees*) and 066/079 (progress-reporting and humanized output at the wrap-up end); each has
  a different subject, so none is a binding precedent.
- Q: Does the verified 30-second cadence replace the existing 15-minute default, or sit beside it? →
  A: Neither. `shared/guidelines/progress-reporting.md` owns the interactive default and keeps it;
  the new owner adds exactly one **long-run cadence profile** whose default is **30 seconds**.
  Selection between the two is decided by one declared condition: the run has at least one live
  status receiver (a reporter seat or a supervising master) → the 30-second profile; no live receiver
  → the existing interactive default. Two defaults therefore never compete inside one run.
- Q: What may the receiving console entry be called? → A: A **thin `speckit.*` command backed by a
  deterministic script** — the existing command + script shape the framework already uses for its
  other deterministic read-only verdicts. One layer, because the guard (FR-017) and the digest
  (FR-011) share the same state reads and two renderers would duplicate the projection. The command
  name itself is fixed in the plan stage (A13).
- Q: What happens to the user's "every team gets a reporter subagent" when the team fits in one
  model call through virtual mode and has no independent execution to report on? → A: The seat
  remains mandatory as **structure** and becomes optional as **runtime** under one declared
  condition: the team's lanes are all executed by the current session and the whole run is expected
  to finish inside one cadence interval. Under that condition the team records the declared reason
  (FR-021), and the orchestrator itself carries the reporting duty; outside it a reporter execution
  is created. The user's decision is preserved, and a recorded reason is the only accepted escape —
  no silent omission.
- Q: Can the shipped `skills/external/coaching-skills` satisfy the master-reporting duty as it
  stands? → A: No — not without an amendment. Its `## Dispatch Payload` is a **closed field set**
  whose "anything not listed below is forbidden" clause excludes a reporting-cadence field, it
  dispatches exactly one subagent per run, and it has no subordinate-state report. The required
  amendment is therefore written as a requirement (FR-019), and the payload's closed-set invariant is
  kept, not silently widened. This is the only pre-existing owner document the feature amends.

