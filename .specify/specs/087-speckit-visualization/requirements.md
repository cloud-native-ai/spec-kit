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

### Revision 2026-11-06 — efficiency visibility and `/speckit.measure`

A second bounded slice was authorized after the first review round. It adds **two** capabilities
and modifies no existing clause's semantics (FR-001…FR-022 and SC-001…SC-010 are extended by
addition only):

4. **An efficiency dimension on the same surfaces** — the status line and the digest say not only
   *what* is running but *how long each measured unit took*, read from the exec-quant store
   (`.specify/memory/exec-quant/`), whose writer stays the existing exec-quant engine (FR-023,
   FR-024, FR-025).
5. **A dedicated measurement-reading command** — `/speckit.measure` analyses and summarises that
   store: per-unit elapsed time, token and call counts, distributions and baselines, for one
   window and one or more units (FR-026, FR-027, FR-028).

The two additions reuse the same owners as the rest of the feature: the store's schema, layout and
write path stay with `scripts/python/exec-quant.py` and its declaration
(`shared/declarations/facts/quant-record-schema.yaml`); the reading is one new read-only,
stdlib-only engine consumed by both the visibility surfaces and the command. **Still no new store,
scheduler, daemon, console channel or second registry**, and no second analysis store.

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

### User Story 5 - The status surfaces also say how long things took (Priority: P2)

While a long run is in progress the user does not only want to know *that* a step is running — they
want to know what it has cost so far. The status line, and the on-demand digest, therefore carry one
bounded efficiency element per measured unit: its elapsed time (and, where the store already holds
them, its token count and its call count), each marked with how it was obtained — measured, carried,
or not evaluated. The numbers come from the exec-quant store the framework already writes; the
feature adds no timer and no second measurement path.

**Why this priority**: The user named efficiency visibility explicitly in the revision, and the
surfaces that must carry it (the cadence line and the digest) already exist in this feature — so the
addition is a projection, not a new mechanism. It ranks under the core "what is running" surfaces
because it answers a second question about the same units.

**Independent Test**: Run the status renderer against a store containing units with a measured
elapsed time, units whose time is `not_evaluated`, and a legacy record; assert each rendered line
carries the elapsed element with its provenance marker, that the `not_evaluated` case renders as
"not evaluated" rather than as zero or as an omission, and that an absent store yields the explicit
"no measurements" state.

**Acceptance Scenarios**:

1. **Given** a run whose measured units have elapsed times in the exec-quant store, **When** a
   status line or a digest is rendered, **Then** it carries one bounded efficiency element per unit
   listed, each naming the unit and its elapsed time, within the same declared entry bound as the
   rest of the line or digest.
2. **Given** a unit whose record says `not_evaluated` for elapsed time, **When** it is rendered,
   **Then** the element says the quantity was not evaluated and MUST NOT be printed as `0` and MUST
   NOT be silently dropped.
3. **Given** a workspace with no exec-quant store at all, **When** either surface renders, **Then**
   the efficiency element renders as an explicit "no measurements" statement and the rest of the
   line or digest is unchanged.
4. **Given** a unit for which the store holds several records of different ages, **When** a status
   line or a digest renders that unit, **Then** the element reports the record with the latest
   `collected_at` and no figure is averaged, summed or ranked across the older ones; **and given**
   a unit the surface lists for which the store holds no record at all, **Then** the element is
   still present and says the quantity was not measured.

---

### User Story 6 - The user can analyse what the run cost, on demand (Priority: P2)

The user — or a maintainer comparing two branches, or a driver deciding whether a stage is getting
slower — asks one question: "how long did each unit take, how many times did it run, and how does
that compare to the baseline?" `/speckit.measure` answers it from the exec-quant store: one bounded
report over a declared window and a declared unit selection, with per-unit elapsed time, token and
call counts, distribution statistics, and the historical window the comparison used. The command is
read-only, deterministic, and introduces no second store.

**Why this priority**: The user asked for a dedicated analysis command in the revision, and the
store already holds the data. It ranks beside the efficiency projection because it is the deep
question of the same data; it is not P1 because a reader can already see the current numbers on the
status line.

**Independent Test**: Run the command against a fixture store (three units, several records each,
plus one unreadable record and one legacy record); assert the per-unit elapsed/token/call figures
match a hand-computed expectation, that the unreadable and legacy records appear as declared
degradations rather than as zeros, that two runs over the same store and window produce byte-identical
output, and that the store's files are unchanged after the run.

**Acceptance Scenarios**:

1. **Given** a store with records for three units over a window, **When** the command runs with that
   window and the whole unit set, **Then** it reports per unit the record count, the elapsed time and
   token figures with their provenance, and the window it actually selected.
2. **Given** an unreadable record and a legacy-format record in the store, **When** the command runs,
   **Then** both are reported as named degradations with counts, the readable records are still
   analysed, and the run does not fail on them.
3. **Given** an empty or absent store, **When** the command runs, **Then** it reports "no measurements"
   explicitly and exits with the declared "nothing to analyse" status rather than printing zeros.
4. **Given** two adjacent windows whose boundary falls exactly on one record's `collected_at`, **When**
   each window is reported, **Then** that record is counted in exactly one of them — the later
   window, by the half-open rule — and the two reports together account for every record in the
   store; **and given** a record the engine cannot parse and a record whose schema version reaches
   it only through the compatibility path, **Then** each is counted once under its own class and
   never twice.
5. **Given** a window whose every contributing record carries the not-evaluated elapsed quantity,
   **When** the command runs, **Then** it produces the per-unit report with the explicit
   not-evaluated marker and exits with the success status, not the nothing-to-analyse status.

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
- **A quantity with no source**: an efficiency element whose record says `not_evaluated` renders as
  "not evaluated" with that marker — never as `0`, never as an averaged-over substitute, and never
  as an omission, because an omission reads as "fast" to a reader comparing two runs. A record that
  carries the quantity as a `{"value", "provenance"}` object renders with that provenance, not as a
  bare number.
- **A store that is absent, empty or half-written**: the efficiency projection and the measurement
  report both degrade explicitly — "no measurements" for an absent or empty store, a named
  degradation count for an unreadable record — and neither invents a value nor fails the surrounding
  run. A partially written record is judged by the store's own reader, never re-parsed here.
- **A legacy store file**: the engine's own compatibility path (per-record files plus the legacy
  stream) is read through that engine, read-only; the feature MUST NOT rewrite, migrate or compact
  the legacy form, and a legacy-only window is still analysable if the engine can read it.
- **A measurement window with no overlap**: a report over a window in which no unit ran is the
  explicit "nothing in this window" result, not an empty table and not an error; the window actually
  selected is always printed so the reader can see why.
- **Two analysts at once**: the report is read-only and writes nothing, so concurrent invocations
  cannot interfere; a report that would need a cache file is out of bounds by FR-027, and the
  reader's own shell redirection is the only place output lands.
- **A unit whose elapsed time straddles two runs**: elapsed time is reported per record with the
  record's run identity preserved, and aggregate figures name how many records they covered; the
  report never silently merges two runs into one figure without saying so.
- **A report whose window selects records but no figure**: a window can hold records while every
  contributing `elapsed_ms` is the not-evaluated literal — the ordinary case in this repository's
  store today. That is a produced report, not the nothing-to-analyse case: it renders each unit's
  record count and the not-evaluated marker, states how many records it covered, and exits `0`. The
  `3` status is reserved for a store that is absent or holds no record in the window at all, so a
  reader can tell "measured nothing here" from "did not look here".
- **Efficiency text on the cadence line**: the efficiency element is part of the line's bounded
  content, not an extra line and not a second cadence — a line that doubles in length to carry it
  has broken the bound in FR-012 and must be truncated with the omitted count stated. Truncation
  degrades the element in one declared order: the elapsed quantity stays, and the token and
  invocation quantities are withdrawn from every unit on that render together, with the withdrawn
  quantity named in the line's existing omitted summary — never dropped for one unit and kept for
  another, because two units described to different depths is the ambiguity the bound exists to
  prevent.
- **A unit the store knows under two types**: the store holds one `unit_id` under more than one
  `unit_type`, so a figure keyed by the bare id would silently merge two different units. The
  measurement report's unit identity is the pair `(unit_id, unit_type)`, and two rows sharing an id
  are reported as two rows; a selection naming the bare id is an input error rather than an
  ambiguous match.
- **A unit that renders but has no record**: the status line and the digest list units from their
  own state sources, not from the exec-quant store, so a listed unit with no record is the ordinary
  case on a fresh run. It renders the not-evaluated marker — the element is never omitted, because
  an omission next to a neighbouring unit's number reads as "faster", which is the one inference
  FR-023 forbids.
- **Two windows that share a boundary record**: the window is half-open on the end
  (`start ≤ collected_at < end`), so a record whose `collected_at` equals a boundary belongs to the
  window that starts there. Two adjacent reports therefore partition the store exactly: no record is
  counted twice and none falls between them, which is what makes a two-window comparison readable
  without a footnote.
- **A store whose elapsed coverage is thin**: the engine's `collect` path leaves `elapsed_ms` as
  `not_evaluated` whenever it has nothing to carry, so a window may hold many records and few
  figures. Both surfaces and the report state the record count their figure covered beside the
  figure itself; reading a thin window as "the run was cheap" is a reader error this feature
  refuses to make easier by printing a zero.
- **The same record reached twice**: the store's legacy stream and its per-record directory can
  describe the same measurement, exactly as the engine's own reader already allows. Both new
  readings go through that reader's own record identity, so one measurement is one record in the
  counts; this feature adds no second de-duplication rule of its own.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The framework MUST declare current-state visibility as a first-class capability with
  a single owning document under `shared/`, which owns exactly eight facts and no others: the
  obligation's **scope predicate** (which flows must report), the **long-run cadence default**, the
  **reporter-seat obligation**, the **master-reporting duty**, the **stall judgement reference**,
  the **out-of-cadence transition triggers**, the **digest contract**, and the **zero-new-machinery
  prohibition**. The owner MUST name what it does not own, with the owner path for each, and MUST
  reference the existing progress-reporting discipline and the existing visibility contract rather
  than restating either.
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
- **FR-023**: The **efficiency dimension** MUST be carried on exactly two existing surfaces of this
  feature and no third: the periodic status line (FR-003/FR-004) and the current-state digest
  (FR-011/FR-012). For every unit a surface already lists, it MUST carry at most one bounded
  efficiency element naming the unit, its **elapsed time**, and — where the source record carries
  them — its token count and its invocation count, each marked with the provenance the record
  states (`measured` / `carried` / `user-given` / `configured`). A quantity the record does not
  carry MUST render as the explicit not-evaluated marker, never as `0`, never as an averaged
  substitute and never as an omission. The element is content of the line or digest, not an extra
  line and not a second surface, and it is subject to FR-012's entry bound unchanged. Within an
  element the **elapsed quantity is unconditional and comes first**; the token and invocation
  quantities are appended only while the whole element stays inside the entry bound the surface
  already applies, and when they cannot fit they are dropped from **every** unit on that render
  uniformly, with the dropped quantity named as not rendered in that render's existing omitted
  summary — never per-unit, so two statements of one render never disagree.
- **FR-024**: The efficiency dimension MUST be read **only** from the exec-quant store at
  `.specify/memory/exec-quant/`, through the engine that owns it
  (`scripts/python/exec-quant.py`: its record directory, its legacy-stream compatibility path and
  its record schema declaration `shared/declarations/facts/quant-record-schema.yaml`). This feature
  MUST treat that store as **read-only** and MUST NOT create, migrate, rewrite, compact or delete a
  record; it MUST NOT introduce a second store, a second record format, a cache file or a derived
  database for the dimension. Store availability is never a precondition of the visibility surfaces:
  an absent or empty store renders the explicit "no measurements" state and leaves the rest of the
  line or digest unchanged. **Record selection** is one declared rule and no second one: the element
  reports the latest record **by `collected_at`** for the unit the surface is already listing, and
  older records of that unit are not folded into it — no ranking, no averaging and no lifetime
  aggregate is computed on a visibility surface. A unit limit applies and is the surface's own: the
  element is rendered for at most the entries that surface already lists, so no additional unit is
  introduced by this dimension. If one unit carries more than one record with the same latest
  `collected_at`, the tie is resolved by the record's own identity in an ascending, byte-stable
  order, never by filesystem enumeration order. A surface that lists units but finds no record for
  one of them is covered by FR-023's not-evaluated rule: the element says the quantity was not
  measured, and it is never omitted so that a reader mistakes absence for speed.
- **FR-025**: The efficiency element's **elapsed-time source MUST NOT require a new recorder**. The
  exec-quant record's elapsed quantity is populated by the existing collection path and its existing
  per-unit hooks; where that path leaves the quantity as `not_evaluated`, FR-023's not-evaluated
  rule applies unchanged. If, and only if, populating elapsed time needs a field the declared
  schema does not carry, the extension MUST be declared by the schema's existing owner (the
  declaration fact above plus the engine that reads it), MUST keep the record's existing keys and
  provenance discipline intact, and MUST be stated as a schema-version consequence for readers.
  This requirement adds no recorder of its own and no second write path to the store. **No extension
  is needed to read elapsed time.** The declared schema already carries
  `quality.elapsed_ms` (`shared/declarations/facts/quant-record-schema.yaml`; schema version 2), and
  the engine's own collection paths already populate it — `collect-dispatch` as `measured`, and
  `collect` as `carried` when the neighbouring run-determination record supplies it. What the store
  does not guarantee is **coverage**: the `collect` path leaves the quantity `not_evaluated` when it
  has nothing to carry, and inspection of the store on 2026-11-06 found the great majority of
  records in exactly that state. That is a data condition, not a schema gap: it is rendered under
  FR-023's not-evaluated rule and this feature opens no recorder to fill it. A schema extension is
  therefore **out of scope for this feature**; if a later stage finds one genuinely required, it is
  that schema owner's change under the conditions stated above and never a private field added here.
- **FR-026**: The framework MUST ship `/speckit.measure` — a thin `speckit.*` command backed by one
  deterministic, stdlib-only analysis engine that is **read-only** over the exec-quant store and
  MUST NOT spawn a subprocess, open a network connection, write any file, or mutate the store. It
  MUST NOT be a scheduler, a watcher, a daemon or a background process: it runs when invoked and
  exits.
- **FR-027**: `/speckit.measure` MUST analyse and summarise the exec-quant store over a **declared
  window** (a start, and an end that defaults to now) and a **declared unit selection** (one or
  more unit identities, or all units the store holds), producing per selected unit: the record
  count, the elapsed-time figures with their provenance, the token figure with its provenance, the
  invocation count, and — where the selected window holds two or more records — the distribution
  summary the engine declares (minimum, maximum and a central value, each named). It MUST state the
  window and the unit selection it actually used, and MUST state the record count it excluded with
  the reason class (`unreadable`, `legacy-format`, `outside-window`, `unknown-unit`), so that a
  figure is never silently computed over a subset. No threshold verdict, no scoring and no
  comparison-to-baseline recommendation is issued: the report presents measurements. **Window
  semantics** are one declared pair and reuse the store engine's own input form rather than a second
  one: `--since` carries the **start**, `--window` carries the **span** and resolves the end as start
  plus span, an invocation with neither covers **all records the store holds** (stated as such in the
  report, never as an implied 24-hour day), and a start later than the resolved end is an input
  error. The window is half-open — `start ≤ collected_at < end` — so two adjacent windows over one
  store partition it without double-counting or dropping a record. **Selection**: one or more
  `--unit` values, each an exact unit identity, matched as a set; an identity the store does not
  hold is an input error naming it, not an empty section. **Cap**: per-unit record contribution is
  bounded by a declared default cap with the omitted count stated in the **same** classes as above
  (`outside-cap` is not a fourth class — the omitted-events count is reported beside the existing
  four), and truncation is applied by the record's own identity in ascending order so it is stable.
  **Default cap**: the engine declares it in exactly one place and prints the value it used on every
  run, so a reader never has to infer which cap produced a table; `--cap` overrides it per
  invocation and the printed value follows the override.
  **Aggregation**: the per-unit elapsed figure is the **median** over the in-window records, with
  the minimum and the maximum named alongside it; record counts, token figures and invocation counts
  are **sums**; a quantity absent from **every** contributing record is reported as not evaluated for
  that unit rather than as `0`, and a quantity present on only some records reports its figure
  together with the number of records it covered, so a partial figure is never read as a whole one.
  **Unit identity is `(unit_id, unit_type)`**, because the store holds one `unit_id` under more than
  one type and a bare id would merge two different units into one row. **Legacy records** are those
  the engine's legacy stream path can read; a record the engine cannot parse is `unreadable`, and a
  record whose schema version the engine reads only through its compatibility path is
  `legacy-format`. All four classes are counted **once per record**, never twice for one record.
- **FR-028**: `/speckit.measure` MUST be **deterministic** — two invocations over an unchanged store
  with the same window and selection produce byte-identical output, with no wall-clock-dependent
  text beyond the window's stated end and no ordering left to a hash or to filesystem enumeration —
  and MUST expose a **closed action set** and a **closed exit-status set** it owns: at minimum a
  summary render and a machine-readable render of the same figures, an input-error status, a
  "nothing to analyse in this window" status distinct from an error, and the success status. It
  MUST NOT add a fourth analysis store, a summary file it persists, or a second reading path beside
  the one the visibility surfaces use (FR-023): one engine and one reading, reached by path. **The
  closed exit-status set** is exactly four values: `0` a report was produced (including a report whose
  window selected some records but none contributed a figure, which is stated as such and is not the
  nothing-to-analyse case); `2` input error (an unparseable `--since`/`--window`, a start after the
  end, an unknown `--unit`); `3` nothing to analyse, meaning the store is absent
  or holds no record inside the resolved window — printed as an explicit "no measurements" statement,
  never as a zero row; `1` any other failure, which MUST be a plain-language single line and MUST NOT
  be used for either of the two statuses above. **One reading**: the same in-process reader module —
  the store engine's own read path reached by path — serves both the visibility surfaces and this
  command; this command adds no parser of the record format and no second store engine. Where the
  visibility surfaces already hold the latest-record-per-unit selection rule (FR-024), that rule stays
  theirs and this command does not restate it: the command aggregates over the window, the surfaces
  show the latest record.
- **FR-029**: `/speckit.measure` MUST ship in the same shape as this feature's other entries and the
  framework's existing commands — one command template in the template layer, one deterministic
  script in the script layer, and the per-tool command copies the framework already regenerates —
  and MUST carry the standard wrap-up delegation the other commands carry. It MUST NOT acquire its
  own store, its own registry entry, its own long-running process, or an authority the read-only
  obligation of FR-026 excludes.

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
- **Efficiency Element**: the bounded statement carried per listed unit on a status line or in the
  digest — the unit identity, its elapsed time, and (when carried) its token and invocation counts,
  each with the provenance the source record states. Exactly one per listed unit, taken from that
  unit's record with the latest `collected_at`, and part of the line's existing content bound.
- **Exec-Quant Record**: one measurement the framework already writes for a measured unit — its unit
  identity and type, its run identity, its collection time, and its quality quantities
  (elapsed time, tokens, exit code, satisfaction) each either a value with a provenance or the
  not-evaluated marker. `quality.elapsed_ms` is present in the declared schema; its **presence in a
  given record** is not guaranteed, because the collection path may have had nothing to carry. The
  record's schema, layout and write path stay with its existing owners; this feature is a reader.
- **Measured Unit Selection**: the set of `(unit_id, unit_type)` pairs a `/speckit.measure` run
  analyses — named explicitly by the caller or defaulted to every pair the store holds.
- **Measurement Window**: the declared start and end a `/speckit.measure` report covers — half-open
  as `start ≤ collected_at < end` — always printed with the report so a reader can see which records
  were in scope, and stated as the whole store rather than as an implied span when neither bound was
  supplied.
- **Measurement Report**: the bounded, read-only, deterministic output of `/speckit.measure` — per
  selected unit the record count, elapsed/token/invocation figures with provenance and the number of
  records each covered, the declared distribution summary, and the excluded-record counts by reason.

### Runtime Stack & Dependency Ownership

本特性交付的运行时能力是状态汇报义务的 owner 文本、reporter 席位义务、主从汇报义务、当前态摘要入口与确定性守卫；
效率维度是对既有 exec-quant 存储的只读投影，`/speckit.measure` 是一个只读分析入口。
其余项由外部供给、本仓只消费，按 `signed-contract` 记。该表是 SC-001、SC-004、SC-005、SC-007、SC-009 的运行时前提。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | Python 3 解释器（运行确定性守卫、效率投影与 measure 分析引擎、契约测试） | signed-contract | CPython 上游（本仓只消费） | `requires-python >= "3.8"`（`pyproject.toml` 已声明，不新增 pin） | `pyproject.toml` | 新增守卫、`status-digest.py` 的效率投影与 measure 引擎及其测试在 `>=3.8` 解释器上通过；新增脚本 stdlib-only | FR-017, FR-023, FR-026, FR-027, FR-028 | EP-001 |
| RS-002 | pytest（守卫、效率投影与 measure 引擎测试运行器） | signed-contract | pytest 上游（本仓只消费） | 无声明 pin；执行时以 `pytest --version` 原文记录进 test-evidence | `scripts/bash/run-tests.sh` | 基线差集为空且新增守卫测试全绿 | FR-017, FR-023, FR-026 | EP-001 |
| RS-003 | agent 宿主（渲染 agent template、承载 reporter 的 live console） | signed-contract | 各受支持 agent 工具上游（本仓只消费） | 无声明 pin；执行时以宿主名 + 版本原文记录进 test-evidence | `docs/reference/cli/supported-agent-tools.md` | SC-001、SC-009 在至少一个受支持宿主上真实运行 reporter 并取原始输出 | FR-005, FR-007, FR-014 | EP-003 |
| RS-004 | line registry 与状态脊（摘要读取的活动状态来源） | signed-contract | 本仓 `skills/external/sdd-loop-driver/scripts/line-registry.py`（消费方，只读） | 同一提交 | `skills/external/sdd-loop-driver/scripts/line-registry.py` | SC-005 的摘要条目逐条解析到该引擎写出的状态文件 | FR-011, FR-012 | EP-001 |
| RS-005 | 状态汇报义务 owner、reporter 模板、reporter 席位义务、主从汇报义务与摘要入口（本特性交付） | in-scope | 本特性 | 同一提交 | `shared/guidelines/progress-reporting.md` | SC-004、SC-007 | FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016, FR-017, FR-018, FR-019, FR-020, FR-021, FR-022 | EP-002 |
| RS-006 | exec-quant 存储、其记录 schema **及其读路径**（效率维度与 measure 报告的只读来源；写入方仍是该引擎自身） | signed-contract | 本仓 `scripts/python/exec-quant.py`（写入 owner、读路径 owner）＋ `shared/declarations/facts/quant-record-schema.yaml`（schema owner）；本特性只读消费 | 同一提交 | `shared/declarations/facts/quant-record-schema.yaml` | SC-011、SC-012、SC-013：两个消费面在进程内 import 同一读路径、取同一组记录，只读前后存储逐文件零差异；引擎自测（`tests/contract/test_exec_quant_engine.py`）保持全绿 | FR-023, FR-024, FR-025, FR-027, FR-028 | EP-001 |
| RS-007 | `/speckit.measure` 入口：命令模板 + 确定性只读分析引擎 + 四工具命令副本（本特性交付） | in-scope | 本特性 | 同一提交 | `shared/guidelines/reporting-obligations.md` | SC-013、SC-014 | FR-026, FR-027, FR-028, FR-029 | EP-002 |

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
- **SC-011**: A status line and a digest rendered over the same fixture store each carry one efficiency element per listed unit within the existing entry bound; a unit whose record says `not_evaluated` renders the explicit not-evaluated marker and neither `0` nor an omission; an absent or empty store renders the explicit "no measurements" state with the rest of the line and digest unchanged; a unit the surface lists with no record at all still carries the not-evaluated marker rather than losing the element, and when the token/invocation quantities cannot fit the bound they are withdrawn from every unit on that render together. **Path**: final
- **SC-012**: Reading the exec-quant store for the efficiency dimension and for the measure report leaves it byte-identical — every file under `.specify/memory/exec-quant/` compares equal before and after both reads, including the legacy stream files, and no new path is created anywhere under it by either read. **Path**: final
- **SC-013**: `/speckit.measure` over a fixture store of three units (several records each, plus one unreadable record and one legacy-format record) reports per unit the record count and the elapsed/token/invocation figures with their provenance, states the window and selection actually used, and reports the excluded-record counts by reason class; on an empty or absent store it reports "no measurements" and exits with the declared nothing-to-analyse status distinct from both success and error; two adjacent windows over one fixture store partition it — each record counted in exactly one of them — and a unit the store holds under two types is reported as two rows, not one. **Path**: final
- **SC-014**: Two `/speckit.measure` runs over an unchanged store with the same window and selection produce byte-identical output, the command exits with only statuses from its declared closed set, and its changed-file set adds no process spawn, network call, written file or scheduled process — the additions are one command template, one stdlib-only script, the regenerated per-tool command copies and their tests. **Path**: supporting

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
- **SC-011 Source**: One status-line render and one digest render over the same fixture store (measured, `not_evaluated`, and absent-store cases); their captured output plus the fixture store's record paths, stored verbatim in `test-evidence/`.
- **SC-012 Source**: A per-file digest of `.specify/memory/exec-quant/` taken before and after both reads, plus a directory listing of it taken after; the two digests and the listing stored verbatim.
- **SC-013 Source**: One command run over the fixture store with its full output, its exit status, the hand-computed expectation table and the per-reason exclusion counts; plus one run over an empty store with its exit status.
- **SC-014 Source**: Two consecutive runs' captured outputs compared with a byte-level diff, the command's declared exit-status table, and the changed-file set from `base..head` with the process-spawn / network / write scan.

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
| Exec-quant record schema: version, closed vocabularies, the eleven config fields, per-action argument manifest | `shared/declarations/facts/quant-record-schema.yaml#/statement`, read by `scripts/python/exec-quant.py` | The efficiency dimension and the measure report read records this declaration shapes; they restate no field name, enum or version, and a schema change is that owner's business (FR-025 admits the extension only there) |
| Exec-quant store layout and write path: `.specify/memory/exec-quant/`, per-record files under `records/`, the legacy stream, `scores/`, `aggregated/` | `scripts/python/exec-quant.py` (`storage_dir` / `records_dir` / `scores_dir`) and the retention lane that consumes it (`scripts/python/record-retention.py`) | Read-only consumption for both new capabilities. The feature adds no subdirectory, no cache, no second format, no migration; the store's `aggregated/` layer stays feedback's channel and is not repurposed here |
| Record reading and record ordering: the per-record directory plus the legacy stream, their de-duplication by record identity, and the "latest record" resolution | `scripts/python/exec-quant.py` — its read path (`load_store` and the reader it composes) is the one reading, and its existing `list-records` action is the one entry already exposed over it | Both new capabilities read **through** that path by import, in-process; neither re-parses the format, re-implements the ordering nor shells out to the engine's command line. The measure entry is a second **projection** over the same reader, not a second reader (FR-028) |
| Record retention, receipt-gated deletion, grace | `scripts/python/record-retention.py` and `shared/declarations/facts/memory-retention-thresholds.yaml#/statement` | Not touched: `/speckit.measure` presents figures over whatever records the store still holds and states its window; it retires nothing and offers no "delete these records" action |
| "Measured, not impressed" — a quantity with no source reports itself as not evaluated | `shared/guidelines/single-run-evidence.md` § Run Determination and the exec-quant record's provenance discipline | The efficiency element and the measurement report carry the record's provenance verbatim; neither fills a missing quantity with `0`, an average or a guess |
| Summary-first consumption of machine-managed data | `shared/guidelines/token-efficiency.md` § Escalation Ladder | The efficiency element is a summary projection and `/speckit.measure` is the digest entry for this store — the ladder's first rung, never a raw-record injection |

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
  the reporter-seat obligation, the master-reporting duty and stall judgement, the out-of-cadence
  transition triggers, the digest contract and the zero-new-machinery prohibition — the eight
  facts, enumerated in full by FR-001. The existing `shared/guidelines/progress-reporting.md` keeps ownership of the anchoring
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
- **A16 — the efficiency store is exec-quant, and the feature is its reader**: the user named
  `.specify/memory/exec-quant` directly, so no store choice is open. Its **schema** is owned by
  `shared/declarations/facts/quant-record-schema.yaml#/statement` and its **layout and write path**
  by `scripts/python/exec-quant.py` (`storage_dir` / `records_dir` / `scores_dir`); this feature
  reads through that engine and restates neither. One consequence is accepted explicitly: the
  record's elapsed-time quantity is populated by that engine's existing collection path, so where it
  is `not_evaluated` the surfaces say so (FR-023) and FR-025 forbids inventing a second recorder.
  A schema extension, if the plan proves one is needed, is the schema owner's change and is carried
  as a compatibility consequence for readers — never as a private field or a parallel record.
- **A17 — the efficiency projection is bounded to the surfaces that already exist**: the user asked
  for efficiency "在可视化信息里", so it lands where this feature's own visibility already lands —
  the cadence status line and the on-demand digest — and nowhere else. No third surface, no extra
  line, no per-step line per unit; the element is content within the existing entry bound (FR-012),
  which is what keeps the status line one screen.
- **A18 — `/speckit.measure` is an analysis entry, not a watcher**: it is the store's analogue of the
  digest — invoked, reads, prints, exits. The existing engine's own `list-records` / `aggregate`
  actions stay exactly as they are (feedback's channel owns `aggregate`'s semantics); `/speckit.measure`
  is a distinct **read-only analysis** entry owned by this feature, and it reuses the store and its
  reader rather than the feedback channel. `aggregate`'s `aggregated/` layer is NOT repurposed: it
  remains feedback's received-package summary view.
- **A19 — the analysis dimensions are chosen from what the record already carries**: per-unit record
  count, elapsed time, token figure, invocation count, and the declared distribution summary
  (minimum / maximum / central value) over the selected window, plus the excluded-record counts by
  reason class. Trends are read as a window comparison the caller selects (this window against an
  earlier one it names), never as a stored baseline series: persisting a baseline would be the second
  store FR-024 excludes, and a "too slow" verdict would smuggle a threshold owner into this feature.
- **A20 — the command's shape is the framework's existing command shape**: one command template in
  the template layer, one stdlib-only deterministic script, the regenerated per-tool copies, and the
  standard wrap-up delegation — the same shape `/speckit.status` ships in. The command name
  (`/speckit.measure`) is the user's, so Grounded Naming carries it unchanged; the script's file name
  and the exact action identifiers stay the plan stage's decision (A13).
- **A21 — the blocked closure verdict is preserved, not erased**: this revision is a scope addition
  (`Draft`, requirements stage) and asserts nothing about delivery. The prior `Blocked` verdict for
  SC-001 and SC-002 survives verbatim in the feature registry and in `verification.md`; only a later
  closure re-check may re-judge it. Adding criteria here does not unblock, re-open or re-close them.
- **A22 — the elapsed quantity is read, not measured, and its coverage is a data condition**: the
  declared schema already carries `quality.elapsed_ms` at schema version 2, so no extension is
  required to *read* it (measured 2026-11-06 against
  `shared/declarations/facts/quant-record-schema.yaml` and the engine's two population sites,
  `collect` → `carried`, `collect-dispatch` → `measured`). What varies is coverage: of the 186
  per-record files in this repository's store, 151 carried `elapsed_ms` as the not-evaluated literal
  and 35 as a `{value, provenance}` object, and the tokens quantity was absent on all 186. Those
  readings are the schema-population reality, not a defect this feature repairs: the surfaces and the
  report are obliged to state the record count behind each figure, and filling a gap is explicitly
  out of scope. An extension, should one ever be proved necessary, remains the schema owner's change
  — this assumption fixes only that it is not this feature's.
- **A23 — the visibility surfaces and the measurement report answer different questions over one
  reading**: the surfaces show **what the latest record for this unit said**, because the user's
  question there is "what is it costing right now"; the report aggregates **every record in the
  window**, because the question there is "what did this cost over the period". One reader module
  serves both; the two selections are different projections of it, not two implementations of it, and
  neither is allowed to leak into the other — a lifetime average on a status line, or a
  latest-record-only figure in a window report, would each answer the wrong question.
- **A24 — the measure entry's argument shape mirrors the store engine's own input**: `--since` (start)
  and `--window` (span) reuse the form the store's existing `list-records` already accepts for its
  start, so a caller who knows one entry knows the other, and no new date dialect is introduced. The
  half-open interval and the "no bounds means the whole store" default are the two decisions that
  form leaves open; they are fixed by FR-027 rather than left to the plan, because they decide whether
  two adjacent reports can partition one store — a property a reader relies on and cannot recover
  after the fact.
- **A25 — one command copy source, four generated copies**: `/speckit.measure` ships exactly as this
  feature's other entry does — one command template in the template layer and the per-tool copies the
  existing regeneration step writes for the four tool directories this repository actually has. The
  copy count is a consequence of that step, not a number this spec pins; a fifth tool becoming
  configured adds a copy without a requirement change.
- **A26 — the arguments this stage fixes are those a reader could not recover afterwards**: window
  semantics, aggregation statistic, unit identity, cap behaviour, exit-status meaning and element
  degradation order are fixed here because each changes what a rendered number *means*. What stays
  open is deliberately mechanical — action identifiers, the script's file name, the human-readable
  layout of the summary render — and belongs to the plan under A13.
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
- **A second measurement store, record format, cache file or derived database** for the efficiency
  dimension or the measure report; both read `.specify/memory/exec-quant/` through its owning engine
  and write nothing.
- **A second recorder or timer**: populating elapsed time is the exec-quant engine's existing
  collection path; this feature adds no instrumentation of its own and no per-step timing hook.
  Where the store leaves a quantity `not_evaluated`, the surface says so.
- **Migrating, compacting, rewriting or retiring exec-quant records**: record retention stays with the
  retention lane and its receipt gate. `/speckit.measure` offers no delete, prune or migrate action.
- **A threshold verdict, scoring or "too slow" recommendation**: the measure report presents
  measurements and their window; judging them is the reader's, and a threshold owner is not created.
  The engine's existing `score` action is unchanged and is not extended by this feature.
- **A stored trend series or persisted baseline index**: a trend is the caller's two selected windows
  compared at read time; nothing is accumulated on disk.
- **A scheduler, watcher, daemon, polling loop or exported metric endpoint** for efficiency data:
  `/speckit.measure` runs on invocation and exits, exactly like the digest.
- **Repurposing feedback's `aggregated/` layer** or changing the existing `aggregate` action's
  semantics: that layer remains the received-package summary channel owned by the feedback flow.
- **Efficiency on a surface this feature does not already own** — no web/dashboard panel, no TUI
  column, no per-step line per unit, no second cadence for measurements.
- **Estimating a missing measurement**: no interpolation, no extrapolation from a neighbouring run,
  no filling a `not_evaluated` quantity with a zero or an average.
- **Extending the exec-quant record schema for this feature**: no new field, no new record version,
  no private sidecar key. The quantities this feature reads are already declared and already
  populated by the engine (measured 2026-11-06); an extension, were one ever proved necessary, is
  that schema owner's change and not a deliverable here.
- **De-duplicating, reordering or re-reading the store by a second rule**: record identity, ordering
  and the latest-record resolution stay with the store engine's read path. A second reader, a shelled
  call back into the engine's command line, or a re-parse of the record format inside either new
  entry is the duplication this exclusion forbids.

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

### Revision 2026-11-06 (second slice) — recorded adjudications

The user's revision input is two sentences; where they leave a choice open it was adjudicated in this
stage rather than deferred, and the adjudication is recorded here because the user was not asked:

- Q: Whose store is `.specify/memory/exec-quant/`, and may this feature extend it? → A: The user
  named the path, so the store is fixed. Its schema and write path stay with
  `shared/declarations/facts/quant-record-schema.yaml#/statement` and
  `scripts/python/exec-quant.py`; this feature is a **reader** (A16, FR-024). An extension needed to
  carry elapsed time is that owner's declared change, with a stated compatibility consequence —
  never a private field and never a second record format.
- Q: Which user-visible surface carries efficiency? → A: The two this feature already owns — the
  cadence status line and the digest — as one bounded element **per listed unit**, inside the
  existing entry bound (A17, FR-023). No third surface, no extra line, no second cadence.
- Q: How is elapsed time populated if the record leaves it `not_evaluated`? → A: It is not populated
  here. FR-025 forbids a second recorder; FR-023 renders the not-evaluated marker explicitly. A
  plan-stage finding that the existing path cannot populate it becomes a schema-owner request, not a
  new timing hook in this feature.
- Q: Is `/speckit.measure` the same thing as the engine's existing `aggregate`? → A: No. `aggregate`
  is feedback's received-package summary view over `aggregated/`; `/speckit.measure` is this
  feature's read-only analysis entry over the local store (A18). The two are not merged and
  `aggregate` is not repurposed.
- Q: Does the measure command compute trends and baselines itself? → A: Trends are a read-time
  comparison of two caller-selected windows; a persisted baseline series would be the second store
  FR-024 excludes (A19). Threshold verdicts are excluded outright — the report presents measurements,
  the reader judges them.
- Q: What happens to the existing `Blocked` verdict now that scope grew? → A: Nothing. The revision
  is a requirements-stage scope addition at `Draft`; the SC-001 / SC-002 `partial` readings and the
  block verdict remain recorded unchanged, to be re-judged only by a later closure check (A21).

### Session 2026-11-06 (clarify, post-revision)

**Mode override: A — post-requirements; target `.specify/specs/087-speckit-visualization/requirements.md`.**
The phase table would have selected C because `plan.md` and `tasks.md` exist; the driver's assignment
explicitly names `requirements.md`, and the previous slice already ran the revision here, so the
override is taken and logged. Zero-question mode: the driver authorized self-adjudication, so each entry
records the question it answers, the adjudicated answer, and the evidence it rests on. Six questions
were resolved against the owners rather than put to the user; none of them changes a pre-existing
clause's meaning — the FR-001…FR-022 / SC-001…SC-010 text is untouched and no FR/SC id was added,
removed or renumbered (29 FR / 14 SC before and after).

- Q: Does the exec-quant store already carry a per-step elapsed-time field, or does this feature need a
  schema extension? → A: **It already carries it.** `quality.elapsed_ms` is in the declared schema
  (version 2) and the engine populates it in two places — `collect` writes `carried` when the adjacent
  run-determination record supplies it, `collect-dispatch` writes `measured`. No extension is required
  to read it, so FR-025 is amended to say so explicitly and to close the extension route for this
  feature. What the store does not guarantee is coverage — measured 2026-11-06 over the 186 per-record
  files: 151 `not_evaluated`, 35 valued, and tokens absent on all 186 — and that is a data condition
  rendered under FR-023's not-evaluated rule, never a number to invent (A22).
- Q: Where on the visibility surfaces does the efficiency element go, and what happens when the line's
  bound cannot hold it? → A: FR-023's two named surfaces stand (status line + digest) and no third is
  opened. Inside an element the **elapsed quantity is unconditional and comes first**, and the token
  and invocation quantities are additive but degradable: when they do not fit the surface's existing
  entry bound they are withdrawn from **every** unit on that render together and named in that
  render's existing omitted summary. Per-unit depth differences are the one outcome the bound must not
  produce, because two units described to different depths cannot be compared (A17 unchanged; the
  degradation order is new).
- Q: Which record does a surface show when the store holds several for one unit? → A: The latest by
  `collected_at`, and nothing is folded in — no average, no sum, no ranking — because the surface's
  question is "what is it costing now". A listed unit with no record at all renders the not-evaluated
  marker rather than dropping the element, since an omission beside a neighbouring unit's number reads
  as "faster". Ties on `collected_at` are broken by record identity in ascending byte-stable order,
  never by enumeration order (FR-024; A23).
- Q: What does `/speckit.measure` mean by "a declared window"? → A: One pair reusing the store
  engine's own input form: `--since` is the start, `--window` is the span resolving the end as
  start plus span, no bound at all means the whole store (stated as such, never an implied span), a
  start after the end is an input error, and the interval is **half-open** — `start ≤ collected_at <
  end` — so two adjacent windows partition a store with no double-count and no gap. Aggregation is
  fixed here too: the per-unit elapsed figure is the **median** with minimum and maximum named,
  counts and tokens are **sums**, and a quantity missing from every contributing record is reported
  as not evaluated while a partially covered one states how many records it covered. Unit identity is
  the pair `(unit_id, unit_type)` because the store holds one id under more than one type (A24).
- Q: What is the command's exit-status contract, and how does it bound a large store? → A: Four
  statuses and no more — `0` a report was produced, `2` input error, `3` nothing to analyse (absent
  store, or no record inside the resolved window; printed as an explicit "no measurements" statement,
  never a zero row), `1` any other failure. A per-unit record cap has one declared default printed on
  every run with `--cap` as the per-invocation override, truncation applied by record identity in
  ascending order, and the omitted count reported beside the existing four exclusion classes rather
  than as a fifth class (FR-028).
- Q: Does `/speckit.measure` share its reading with the visibility surfaces, or may it read the store
  independently? → A: **One reading.** The same in-process reader module — the store engine's own read
  path, reached by path — serves both; the measure entry adds no second parser of the record format
  and no second store engine. The two consumers are two projections of that one reader, and neither
  may borrow the other's selection: a lifetime figure on a status line, or a latest-record-only figure
  in a window report, would each answer the wrong question (A23, A26).

