# Tasks: Speckit 框架可视化（Speckit Framework Visualization）

**Requirement ID**: 087
**Requirement Key**: 087-speckit-visualization
**Related Feature**: 087 Speckit 框架可视化（Speckit Framework Visualization）
**Input**: Design documents from `.specify/specs/087-speckit-visualization/`
**Prerequisites**: plan.md (required), requirements.md (required for user stories), research.md, data-model.md, contracts/, quickstart.md, feature-ref.md

**Tests Mode**: ON — Constitution Principle IV "Test-First & Contract-Driven Implementation" is mandatory ("Pure functions/utilities MUST have unit tests", "Critical flows MUST have automated regression coverage", "Integration/contract tests MUST cover ... external APIs"), and the Workflow Gates block is `NON-NEGOTIABLE`. Layer mapping for this feature: **Layer-1** = importable-script unit tests (`tests/unit/test_status_digest_unit.py`), **Layer-2** = contract tests over the delivered artifacts, report shapes and renderers (`tests/contract/test_*.py`), **Layer-3** = real-render smoke with real output captured into `test-evidence/` (the shipped scripts, the roster guard, the owner-literal scan). The template-only exemption in Principle VII does NOT apply: this feature ships executable runtime code (`scripts/python/status-digest.py`, `skills/internal/create-team/scripts/validate-roster.py`), so its tests are ordinary unit + contract tests.

**Tests**: Every `Tests for User Story N` block below is MANDATORY. Each new-behavior test row precedes its implementation row and is expected to go RED first (recorded in `notes/red-first-evidence.md`). Only the two *regression-guard* rows (T036, T043) are green-after: they guard pre-existing behavior and can only pass once the corresponding change lands — they carry `[blockedBy:]` on that implementation row, per the migration/regression exception in the Task Generation Rules.

**Organization**: Tasks are grouped by user story (requirements.md § User Story Scenarios) so each story is independently implementable and testable. Phases run in priority order P1 → P2 → P3. This is a **doc-feature-shaped** feature (`skills/internal/create-tasks/references/phase-shapes.md`): within each story the order is author-section → mirror-parity → render-verify → refresh-verify, with the contract test that pins the authored section placed first (red-first).

## Definition of Done (DoD)

- DoD-1: Every delivered path in `feature-ref.md` § Delivered paths (#1–#28) exists, and its mirror or generated copy is produced by the framework's own engine, never by hand (plan.md § Mirror Obligations)
- DoD-2: `pytest -m contract tests/contract/test_reporting_obligations.py tests/contract/test_roster_reporter_seat.py tests/contract/test_coaching_reporting_duty.py tests/contract/test_status_digest.py` and `pytest tests/unit/test_status_digest_unit.py` are green
- DoD-3: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/087-speckit-visualization/tasks.md` exits 0 and `/speckit.implement`'s re-run of it still exits 0
- DoD-4: The 30-second long-run default has exactly one framework-source definition site and the guard's RO-03 proposition fails when a second one is seeded (SC-006)
- DoD-5: Every `final`-path success criterion (SC-001…SC-007) reads `pass` in `verification.md`, each backed by a captured artifact under `test-evidence/`; no SC is claimed from a green check alone
- DoD-6: No scheduler, timer service, daemon, new dependency, new persistent store, new console channel, second registry, state spine or ledger appears in `git diff --name-only 56f3f881..HEAD` (SC-010, contract OM-03/OM-04)

**DoD Status**: pending

## Completion Gate

- GATE-1: Zero NEW failures vs the recorded pre-change baseline, measured by node-id set — check: `bash scripts/bash/run-tests.sh -q --deselect <docker/hugo suites recorded in notes/pre-change-measurements.md>` with the pre-change node-id list captured by `/speckit.implement` step 6's `**Test runs**` bullet (owner of the baseline path, name-list form and capture flag — not restated here), then `comm -13 baseline current`
- GATE-2: Every row of plan.md § Mirror Obligations is byte-identical source↔mirror with no NEW drift — check: `python3 scripts/python/sync-mirrors.py --check` exits 0 with `ok` for all six pairs, and `python3 scripts/python/regen-command-copies.py --check` prints `OK: all per-tool command copies match the source templates.`
- GATE-3: No `[ ]` or `[>]` task rows remain — check: `grep -cE '^- \[[ >]\]' .specify/specs/087-speckit-visualization/tasks.md` returns `0`
- GATE-4: Every `final`-path success criterion is `pass` **and** the feature's smoke record is present — check: in `verification.md`, every criterion whose `**Path**` marker reads `final` has `SC-NNN_status=pass`, and `smoke_command=`, `smoke_exit_code=0` and `smoke_evidence_path=` (a path that exists and is non-empty) are all present; a `final`-path criterion in `blocked` / `deferred` / `fail` fails this gate unless an explicit user waiver names that criterion. Condition set owner: `shared/workflow/acceptance-hardening.md` § Gates — this row carries the check, not a second schema

## Environment Prerequisites

- plain `python3` interpreter (the two delivered scripts are stdlib-only) — **available**, probed `python3 --version` → `Python 3.11.11` @ 2026-11-06; affected phases/tasks: Phase 2 (T006, T008), Phase 3 (T011, T012), Phase 5 (T023…T026), Phase 6 (T037)
- `pytest` (contract + unit suites) — **available** (declared in `pyproject.toml`; run through `scripts/bash/run-tests.sh`); fixed version string is captured at implementation time @ 2026-11-06; affected phases/tasks: every `Tests for …` block
- registry directory `~/.local/state/spec-kit/lines` (read-only digest input) — **partial**, probed `ls ~/.local/state/spec-kit/lines/*.json` → one or more `<line_id>.json` entries present @ 2026-11-06; a caller may override with `SPECIFY_LINE_REGISTRY_DIR`; affected phases/tasks: Phase 5 render rows (T024, T025) and Phase 6 (T037)
- per-tool command directories for generated copies — **partial**, probed `ls -d .claude/commands .github/prompts .opencode/command .qoder/commands` → all four exist, while `.hermes/` and `.codex/` do not @ 2026-11-06 (`_ASSISTANT_COMMAND_DIRS` configures six tools, the generator writes only existing directories); affected phases/tasks: T028, T029
- agent host console (a live conversation surface that renders a dispatched agent) — **available** (this run is itself executing on one); the concrete host name + version string is recorded into `test-evidence/` at execution time; affected phases/tasks: T016, T017

**A13 boundary** (owner: `shared/workflow/acceptance-hardening.md` § Gates — this note is a pointer, not a second rule): this section records **task-generation probe verdicts** only, each with its probe command and an ISO date. A planning-time load-bearing premise belongs to `plan.md` § Execution Premises; a record inherited from a dependency feature belongs to `plan.md` § Inherited Blockers. The same fact written into two of the three carriers is a defect: the second occurrence MUST be converted into a pointer (`see § …`), never kept as a copy.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- **[blockedBy: T001,T002]**: explicit dependency tag — the task MUST NOT start until every listed task is `[X]`
- **[green: <contract>#<clause>]**: the row that turns that contract clause green; each clause id is claimed exactly once across the file (条款分区 (Clause Partition), `.specify/memory/glossary.md`)
- Every row names its exact file path and stays on ONE line

## Path Conventions

- Framework sources live at the repository root: `shared/`, `agents/`, `skills/`, `scripts/`, `templates/`.
- `.specify/…` and the per-tool trees (`.claude/`, `.github/`, `.opencode/`, `.qoder/`) are **generated** by `scripts/python/sync-mirrors.py` and `scripts/python/regen-command-copies.py`; no row edits them directly (plan.md § Mirror Obligations, constitution XI).
- Feature evidence and captured render output land under `.specify/specs/087-speckit-visualization/test-evidence/` with a `notes/` sibling created in Phase 1.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: establish the feature's scratch areas and re-measure every frozen baseline this run will diff against. No user-story work may cite a measurement this phase did not take.

- [ ] T001 Create the feature's evidence and notes directories in `.specify/specs/087-speckit-visualization/notes/` (with `.gitkeep`) so Phase 2 rows have a landing point, per `.specify/skills/internal/create-tasks/SKILL.md` § Runtime-evidence landing points — this row creates infrastructure only, so it claims no contract clause
- [ ] T002 [P] Capture the pre-change progress-reporting suite node-id baseline into `.specify/specs/087-speckit-visualization/notes/pre-change-measurements.md` by running `pytest -q --collect-only tests/contract/test_progress_reporting.py` and pasting the real output plus the capture date and command (the implement-stage consumer re-captures per `/speckit.implement` step 6's `**Test runs**` bullet — that bullet owns the baseline name-list form, so this row only points at it)
- [ ] T003 [P] Capture the team-roster baseline into `.specify/specs/087-speckit-visualization/test-evidence/roster-baseline.txt` by running `ls .specify/teams/*/team.md | wc -l` and `ls .specify/specs/*/team/*/team.md | wc -l` (2026-11-06 generation-time probe: `12` and `1`; the merged glob form `ls .specify/teams/ .specify/specs/*/team/` would double-count, which is why the two counts are separate) — this is the population invariant the guard's roster proposition re-measures, so it MUST NOT be re-derived by hand there; this row takes the measurement only and claims no clause
- [ ] T004 Re-run the owner-literal baseline into `.specify/specs/087-speckit-visualization/test-evidence/owner-literal-baseline.txt` by running `grep -rn "30 秒\|30 seconds" shared/ templates/ skills/ agents/` and pasting the complete output (2026-11-06 generation-time reading: exactly 2 hits, both unrelated prose — `skills/external/draw-diagram/references/types/plantuml/references/howto/19-salt-diagram.md:12` and `skills/external/improve-skills/references/skill-slimming-principles.md:73`); the naive claim "zero hits anywhere" is falsified by the tree, so the scan's post-change assertion is "exactly one definition site plus these two whitelisted prose hits". This row takes the measurement only; the clause it feeds is turned green by `shared/guidelines/reporting-obligations.md`
- [ ] T005 Re-run the mirror and copy baseline into `.specify/specs/087-speckit-visualization/test-evidence/mirror-baseline-tasks.txt` by running `python3 scripts/python/sync-mirrors.py --check` and `python3 scripts/python/regen-command-copies.py --check` (2026-11-06 generation-time reading: both exit 0, `ok` for all six pairs — `templates/` 22, `skills/external/` 415, `skills/internal/` 138, `agents/` 16, `scripts/` 121, `shared/` 94 — and `OK: all per-tool command copies match the source templates.`); the pass criterion for every later mirror row is therefore **no NEW drift**, never a bare exit code

**Checkpoint**: Scratch areas exist and every frozen baseline has a dated, re-derivable measurement.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: the two authorities every other phase reaches — the obligation's owner document and the shared reader both the digest and the guard import. Nothing in Phase 3+ is writable before this phase is complete.

**⚠️ CRITICAL**: no user-story work may begin until T006–T010 are `[X]`.

### Tests for the Foundational layer (MANDATORY)

- [ ] T006 Create `tests/unit/test_status_digest_unit.py` with the reader-level fixtures and RED tests for the shared state reading: registry directory resolution order (`$SPECIFY_LINE_REGISTRY_DIR` → `$XDG_STATE_HOME/spec-kit/lines` → `~/.local/state/spec-kit/lines`), per-entry triplet path projection (absent → `-`), `STATE_VALUES` / `ACTIVE_STATES` quoted from the engine rather than re-enumerated (pin the values by importing them from `skills/external/sdd-loop-driver/scripts/line-registry.py` at authoring time, floor-style: assert the projected state is a member of the imported set, never a hard-coded list), and no-write assertion over every opened path — the file MUST fail before T008 exists
- [ ] T007 [P] Create `tests/contract/test_reporting_obligations.py` with the owner-document assertions RED: file exists at both paths, opens with a single-source-of-truth declaration naming exactly the five owned facts and the four pointed-at owners, carries the scope predicate verbatim-shaped, the cadence anchor, the four content-element labels, the transition classes, the prohibition clause, and contains no copy of `progress-reporting.md`'s element descriptions

### Implementation for the Foundational layer

- [ ] T008 Author the obligation's owner `shared/guidelines/reporting-obligations.md`: the single-source-of-truth declaration (five owned facts + four named non-owned owners by path), the scope predicate (two or more concurrent units, or one or more asynchronous delegations continued past dispatch; one synchronous step out of scope), the long-run cadence profile with its **one** 30-second definition site and per-run/per-structure override statement, the reporter-seat obligation with its two recorded-reason escapes, the master-reporting duty over every dispatched sub-flow with the stall judgement reached by path plus anchor to `skills/internal/create-team/references/patterns.md` § Monitoring → Stall Detection, the out-of-cadence transition triggers, the three-mode carrier rule, the not-a-gate clause, the reporter-failure clause, the digest contract by shape, and the zero-new-machinery prohibition — every borrowed discipline reached by section anchor, never restated — [blockedBy: T007] [green: contracts/reporting-obligations.contract.md#C-01]
- [ ] T009 Author `scripts/python/status-digest.py` as one stdlib-only file with two actions over one shared reader: `--action digest` (bounded, deterministic ordering, staleness with age, explicit `nothing-running`, `omitted=<n>`, declared cap default plus `--cap` override) and `--action guard` (the thirteen RO propositions each reported `pass` / `fail` / `not-evaluated` with a reason, `not-evaluated` never counted as pass), carrying a docstring that marks the registry-resolution restatement as the one legal duplicate (contract C-47) and importing nothing outside the standard library — [blockedBy: T006] [green: contracts/status-digest.contract.md#C-41]
- [ ] T010 [P] Extend the owner's pointer surfaces with one line each, no restatement: `shared/definitions/subagent-definitions.md` § Dispatch-Time Governance Obligation gains a pointer to `shared/guidelines/reporting-obligations.md` for the reporting duty, and `shared/workflow/external-dispatch-recipes.md` gains the same one-line pointer while its recipes stay byte-identical — [blockedBy: T008] [green: contracts/reporting-obligations.contract.md#C-12]

**Checkpoint**: The owner exists with its single cadence definition site, the shared reader exists behind both script actions, and both pointer surfaces resolve. Guardian of this checkpoint: `python3 scripts/python/status-digest.py --action guard` must report RO-01/RO-02/RO-03 `pass` and never `fail`.

---

## Phase 3: User Story 1 — A team run reports its overall state every 30 seconds (Priority: P1) 🎯 MVP

**Goal**: a long team run emits one attributed status line per cadence tick carrying the four content elements, from a dedicated reporter seat rather than from the working members; a stage boundary emits an extra line without resetting the cadence; a missing seat is a named defect.

**Independent Test**: run `skills/internal/create-team/scripts/validate-roster.py` over the three roster fixtures (compliant / missing-seat / unresolvable-agent) and then drive `scripts/python/status-digest.py --action guard` proposition RO-04 over a captured line set; assert the seat appears in the roster, the line set carries attribution plus all four elements, the boundary line exists without a cadence reset, and the missing-seat fixture yields a defect naming `reporter` and the team slug.

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: write these FIRST and confirm they FAIL before the implementation rows below**

- [ ] T011 [P] [US1] Author the roster-guard contract test `tests/contract/test_roster_reporter_seat.py`: three fixtures (compliant, missing seat, reporter whose `agent` does not resolve to the shipped template) asserting the exact named-defect text, plus the recorded-reason fixtures (`all-lanes-in-session-single-interval`, `host-cannot-host-reporter`, and one out-of-domain value) and the stdlib-import audit — this file claims `reporter-seat.contract.md` clauses C-14…C-21 in total across the rows that write it; its own green point is the named-defect clause — [blockedBy: T003] [green: contracts/reporter-seat.contract.md#C-16]
- [ ] T012 [P] [US1] Author the status-report assertions for User Story 1 in `tests/contract/test_reporting_obligations.py` against a captured line-set fixture: attribution present and two structures distinguishable, four content elements present with `no blocker` written explicitly, `boundary` trigger present while the tick stamps show no cadence reset, and the reporter Template's authority deny-list over `agents/reporter.agent.md` — this file carries clauses of three contracts (status-report, supervision-report, ownership-map) across the rows that write it; its own green point is the attribution clause — [blockedBy: T007] [green: contracts/status-report.contract.md#C-22]
- [ ] T013 [US1] Author the roster guard `skills/internal/create-team/scripts/validate-roster.py` as a single stdlib-only file: one positional team-file path, exit `0` conforming / `1` named defect / `2` input error, accepting a `role: reporter` member or a closed-set `reporting-reason` and echoing the reason, and reporting a missing seat as a single-line defect that names `reporter` and the team slug — [blockedBy: T011] [green: contracts/reporter-seat.contract.md#C-17]
- [ ] T014 [US1] Author the reporting Agent Template `agents/reporter.agent.md`: the neutral sibling key set with `user-invocable: false`, `capability-tools` limited to read-class tools plus the write surface for its own stream artifact, a body that states the observe-and-report boundary and the defect condition for writing outside that artifact, and by-anchor references (not copies) to the fast-fail dispatch injection and the progress-reporting dispatch-payload duty — [blockedBy: T008] [green: contracts/reporter-seat.contract.md#C-19]
- [ ] T015 [US1] Extend the team-creation entry so the seat obligation is reachable without a new command: `skills/internal/create-team/SKILL.md` gains the reporter-seat obligation and the guard's call site, and `skills/internal/create-team/references/create-mode.md` § Team Schema gains the `role: reporter` discriminator, the two seat-specific keys (`reporting-territory`, `reporting-cadence`), the `reporting-reason` closed set, and the FR-021 runtime-omission condition stated as two conjunctive facts with "the orchestrating session carries the duty itself" — no parallel top-level `reporter:` key is introduced — [blockedBy: T008] [green: contracts/reporter-seat.contract.md#C-15]
- [ ] T016 [US1] Author the status-line renderer into `scripts/python/status-digest.py` as a third action (`--action report`) that emits one line from the owner's four labels plus attribution, whether the carrier is the console or the declared stream artifact, and the profile in force; the emitting flow records the carrier in the run record it already writes, and no per-line artifact is created — [blockedBy: T008] [green: contracts/status-report.contract.md#C-24]
- [ ] T017 [US1] Author the two out-of-cadence triggers into the same renderer: a crossed stage boundary emits an extra line at the boundary without restarting the periodic cadence, a tick landing inside an indivisible step is delivered at that step's next boundary with the delay stated, and a reporting loop that cannot emit renders a `reporter-failure` line instead of falling silent — [blockedBy: T016] [green: contracts/status-report.contract.md#C-29]
- [ ] T017A [US1] Implement the reporter Template's two dispatch-injection duties by reference, not by copy: `agents/reporter.agent.md` reaches `shared/guidelines/fast-fail.md` § 子代理派发注入 for the anomaly-return line and `shared/guidelines/progress-reporting.md` § 子代理与委托（派发时注入） for the duty's own further-dispatch injection, and contains neither clause's text — [blockedBy: T014] [green: contracts/reporter-seat.contract.md#C-20]
- [ ] T018 [US1] Render-verify the seat and the line on a real roster and a real console: run `python3 skills/internal/create-team/scripts/validate-roster.py .specify/teams/command-logic-as-classified-skills/team.md` plus the feature's compliant fixture, and emit ≥3 attributed status lines from a fixture run lasting more than two cadence intervals, capturing verbatim output, exit codes and the receiving carrier into `.specify/specs/087-speckit-visualization/test-evidence/us1-team-cadence.txt` — [blockedBy: T013,T016,T017] [green: contracts/status-report.contract.md#C-26]
- [ ] T019 [US1] Judge every captured US1 line for readability by a reader who did not take part in the run: no internal engine identifier where a user-facing name exists, the facts needed to act present, everything else reached by path reference — recorded as a verdict line in the same evidence file — [blockedBy: T018] [green: contracts/status-report.contract.md#C-31]

**Checkpoint**: A team run reports on cadence with attribution and the four elements, a boundary adds a line without resetting the clock, and a missing seat is a named defect. This is the MVP's observable core.

---

## Phase 4: User Story 2 — A supervising master reports the state of the sub-flows it watches (Priority: P1)

**Goal**: a master that dispatches and watches sub-flows reports every dispatched sub-flow on the cadence — identity, state, age of last observed activity — judges each against the declared stall threshold, distinguishes slow from stalled, and reports a significant transition before the next tick. The shipped `skills/external/coaching-skills` demonstrates it through its payload.

**Independent Test**: drive the supervision projection over a two-sub-flow fixture (one completing, one silent past the declared threshold); assert both sub-flows are named on each tick with their states and ages, the stalled one is reported `stalled` with the threshold row and measured silence named while the just-under fixture is `slow`, the non-zero-exit sub-flow's report lands before the next tick, and the coaching skill's `## Dispatch Payload` still reads as a closed field set that now includes `reporting-cadence`.

### Tests for User Story 2 (MANDATORY) ⚠️

- [ ] T020 [P] [US2] Author `tests/contract/test_coaching_reporting_duty.py`: the skill names the single Trainee dispatch as the reported sub-flow, the four pre-existing forbidden-content classes survive alongside the newly added one, the return contract still names every pre-existing item plus the added self-reported-state item, and a scan over the skill for the owner's exclusive literals (cadence value, threshold numbers) finds zero hits — [blockedBy: T008] [green: contracts/supervision-report.contract.md#C-32]
- [ ] T021 [P] [US2] Author the supervision assertions in `tests/contract/test_reporting_obligations.py`: an exactly-one-dispatch supervisor names that subordinate rather than an empty set, presence is closure (every dispatched sub-flow appears at least once per tick, and an omission is named by its label), the three transition classes each produce a pre-tick report, and `slow` versus `stalled` is decided by the declared threshold row with that row named — [blockedBy: T020] [green: contracts/supervision-report.contract.md#C-33]
- [ ] T022 [US2] Author the supervision projection into `scripts/python/status-digest.py` behind `--action guard`/`--action digest`: per-sub-flow identity from the label convention, state from the triplet plus the exit record, age from the newest triplet mtime, the threshold row read from `skills/internal/create-team/references/patterns.md` at render time with no number copied, and the pre-tick transition rule — the same reader used by the digest, so no second parser appears — [blockedBy: T020,T021] [green: contracts/supervision-report.contract.md#C-34]
- [ ] T023 [US2] Amend `skills/external/coaching-skills/SKILL.md` § Dispatch Payload by exactly one row (`reporting-cadence`: tick value in force plus the attribution pair), one added forbidden-content class (the coach's own status lines or its expected subordinate-state conclusions) and one added return-handling clause (the subordinate's own reported state at return, so the coach cites `self-report` rather than inferring); the preamble "closed field set; anything not listed below is forbidden" stays byte-identical and the set is extended, never widened — [blockedBy: T022] [green: contracts/supervision-report.contract.md#C-37]
- [ ] T024 [US2] Point the amended skill at the duty's owner instead of defining it: `skills/external/coaching-skills/SKILL.md` references `shared/guidelines/reporting-obligations.md` for scope, cadence, threshold and transition classes and restates none of them — [blockedBy: T023] [green: contracts/supervision-report.contract.md#C-39]
- [ ] T025 [US2] Extend the existing payload pin in `tests/contract/test_coaching_dispatch_contract.py`: its `REQUIRED_FIELDS` tuple gains `reporting-cadence` in the same change as T023 (this is the ONE declared expected delta of the compatibility baseline, contract OM-05 — not a regression), and the one compliant + four counterexample payloads are updated to the new closed set; the change stays an extension of the tuple, never a widening — [blockedBy: T023] [green: contracts/supervision-report.contract.md#C-38]
- [ ] T026 [US2] Render-verify the supervision report over the two-sub-flow fixture and the coaching payload: capture both ticks, the just-under (`slow`) and just-over (`stalled`) threshold fixtures, and the pre-tick failure report verbatim into `.specify/specs/087-speckit-visualization/test-evidence/us2-supervision-report.txt` — [blockedBy: T022,T025] [green: contracts/supervision-report.contract.md#C-35]
- [ ] T026A [US2] Capture the three-mode carrier mapping as real render output: one dispatch per execution mode (native console, virtual inline, external stream artifact) with the carrier file of the mode-3 dispatch listed, plus the run record naming mode and carrier together, into `.specify/specs/087-speckit-visualization/test-evidence/us2-execution-modes.txt` — the mapping asserted is the one contract SR-06's premises state, and the carrier is the mode's own declared stream artifact, never a second one; the agent host is per § Environment Prerequisites — [blockedBy: T016] [green: contracts/status-report.contract.md#C-27]
- [ ] T026B [US2] Verify the two out-of-cadence triggers and the profile rule against the captured US2 line set: the `boundary` and `transition:*` trigger kinds are both present while the tick stamps show the cadence was not reset, and every line carries the profile in force with a recorded switch (never a silent one) where the live receiver is lost mid-run — [blockedBy: T026] [green: contracts/status-report.contract.md#C-25]
- [ ] T026C [US2] Verify the captured line set contains no question, approval request or waiver solicitation, and that emitting a line authorizes nothing — the gate discipline itself is reached by path and not restated here — [blockedBy: T026] [green: contracts/status-report.contract.md#C-28]

**Checkpoint**: A master's silence while it watches is impossible: every watched sub-flow is named with its state and age on each tick, slow and stalled are separated by a named threshold, and a failure reports before the clock. The coaching skill demonstrates the duty while the owner defines it.

---

## Phase 5: User Story 3 — The user can ask for a current-state digest at any moment (Priority: P2)

**Goal**: one invocation returns one bounded summary of what is running right now — active lines and their states, dispatched agents with the age of their last activity, the most recent completions — reading state artifacts rather than requiring a live reporter, marking stale entries with their age, and rendering an explicit `nothing-running` when nothing is active.

**Independent Test**: run `python3 scripts/python/status-digest.py --action digest --cap 5` over a 12-entry fixture and over an empty registry; assert 5 entries plus `omitted=7`, a byte-identical second render, a stale entry marked with its age, and the idle run printing `nothing-running` with exit `3` rather than an empty digest with exit `0`.

### Tests for User Story 3 (MANDATORY) ⚠️

- [ ] T027 [P] [US3] Author the digest-fixture tests in `tests/unit/test_status_digest_unit.py` for `--action digest`: a 12-entry fixture under a temp registry renders exactly 5 with `omitted=7` and two renders are byte-identical; an entry older than the stale bound is marked stale with its age; an empty registry renders `nothing-running`; an unreadable registry exits `2`; the script opens no file for writing — [blockedBy: T006] [green: contracts/status-digest.contract.md#C-44]
- [ ] T028 [P] [US3] Author `tests/contract/test_status_digest.py` for the entry and its copies: `templates/commands/status.md` names `scripts/python/status-digest.py` and the delegated action and carries no rendering logic of its own, and the four existing per-tool copies (`speckit.status.md` / `speckit.status.prompt.md` in `.claude/commands/`, `.github/prompts/`, `.opencode/command/`, `.qoder/commands/`) are present and match the source — [blockedBy: T005] [green: contracts/status-digest.contract.md#C-42]
- [ ] T029 [US3] Author the thin command `templates/commands/status.md` with `/speckit.status` front matter and a body that only names the script path, the two actions and the exit-status set — no rendering, no state reading, no second projection
- [ ] T030 [US3] Author the digest's bounded projection and staleness rules into `scripts/python/status-digest.py`: deterministic ordering (active lines first, then descending last activity, ties by `line_id` ascending), the declared cap default with `--cap` override, `omitted=<n>` on truncation, per-entry age always rendered, stale marking with the age, the packed projection of per-entry agent activity where the entry declares triplet paths, and the single most recent completion — the registry is opened read-only and nothing is written anywhere — [blockedBy: T027,T029] [green: contracts/status-digest.contract.md#C-43]
- [ ] T031 [US3] Render-verify the two real digest runs and capture them verbatim: an active run (`--cap 5` over the real registry, whose directory is resolved per § Environment Prerequisites) into `.specify/specs/087-speckit-visualization/test-evidence/us3-digest-active.txt` and an idle run with `SPECIFY_LINE_REGISTRY_DIR="$(mktemp -d)"` into `us3-digest-idle.txt`, both with exit codes, entry counts, the omitted count and per-entry ages — [blockedBy: T030] [green: contracts/status-digest.contract.md#C-45]

**Checkpoint**: "What is running right now?" is one invocation away, bounded to a cap, honest about age, and explicit when the answer is "nothing".

---

## Phase 6: User Story 4 — The cadence, content and attribution rules have one owner (Priority: P3)

**Goal**: the interval, the content floor and the obligation's scope each have exactly one definition site; every consumer reaches them by path, and a deterministic guard fails when a consumer reintroduces the literal or when a decidable proposition is violated.

**Independent Test**: seed a second copy of the `30 秒` / `30 seconds` literal into a framework-source file and assert `python3 scripts/python/status-digest.py --action guard` turns RO-03 red; run the guard over the delivered artifacts with no seeding and assert all thirteen propositions are `pass` or a reason-bearing `not-evaluated`; and classify a seeded flow sample against the owner's scope predicate with zero unclassifiable cases.

### Tests for User Story 4 (MANDATORY) ⚠️

- [ ] T032 [P] [US4] Author the ownership-map assertions in `tests/contract/test_reporting_obligations.py`: the ownership table's one-definition-site-per-fact scan derives its query set from the delivered files themselves and reports exactly one definition site per row; the relation table (owns/consumes/amends/preserves/extends) matches `feature-ref.md` § Consuming / Consumed Owners with no relation present in only one of the two — this file carries clauses of three contracts across the rows that write it; its own green point is the one-definition-site clause — [blockedBy: T008] [green: contracts/ownership-map.contract.md#C-47]
- [ ] T033 [P] [US4] Author the guard-proposition tests in `tests/contract/test_status_digest.py`: all thirteen proposition names appear in `--action guard` output for a compliant fixture, each with a named status; eight mutation fixtures (seat removed, second cadence literal seeded, omission count removed, stale marker removed, annotation dropped, interrogative line injected, suppressed tick, carrier value altered) each turn their matching proposition red; a proposition with no readable input reports `not-evaluated` with a reason and never `pass` — this file's own green point is the proposition-set clause — [blockedBy: T009] [green: contracts/status-digest.contract.md#C-46]
- [ ] T034 [US4] Implement the RO-03 owner-literal scan inside `scripts/python/status-digest.py`'s guard action: exactly one definition site in the framework sources, the two known unrelated prose hits whitelisted by path from `test-evidence/owner-literal-baseline.txt`, and a second seeded site producing `fail` with the second path named — the scan MUST NOT be written as "zero hits anywhere", a claim the tree already falsifies — the one-definition-site clause this scan judges is claimed where that owner is authored — [blockedBy: T004,T033]
- [ ] T035 [US4] Implement the read-only boundary of the guard: every proposition decidable from files on disk with no network and no process spawn, the roster population read from the T003 baseline rather than re-globbed by hand, and an unavailable input reported as `not-evaluated` with its reason — [blockedBy: T034]
- [ ] T036 [US4] Reach and cross the zero-new-machinery boundary: `shared/guidelines/reporting-obligations.md` states the nine prohibitions as one testable clause and the delivered `.py` files import nothing outside the standard library and spawn nothing — audited by an AST-level import-and-call scan plus a `pyproject.toml` dependency-list pin against the pre-change values — [blockedBy: T008,T009] [green: contracts/ownership-map.contract.md#C-50]
- [ ] T037 [US4] Render-verify the guard end to end and capture it verbatim: run `python3 scripts/python/status-digest.py --action guard` over the delivered artifacts, paste every proposition line plus the summary and exit code into `.specify/specs/087-speckit-visualization/test-evidence/us4-guard-verdict.txt`, then run the seeded-duplicate drill (copy the literal into a scratch framework-source file, re-run, capture the red RO-03 verdict, delete the seeded copy) and paste that reading too — [blockedBy: T035,T036] [green: contracts/ownership-map.contract.md#C-49]
- [ ] T038 [US4] Classify the seeded flow sample against the owner's scope predicate and record the verdict: ten framework flows spanning team runs, supervising masters, single-dispatch chains and single synchronous commands, each classified in-scope or out-of-scope with zero unclassifiable cases and zero silently exempted flows, into `.specify/specs/087-speckit-visualization/test-evidence/us4-scope-sample.txt` — [blockedBy: T008] [green: contracts/reporting-obligations.contract.md#C-04]

**Checkpoint**: Changing the interval, the elements or the scope happens in one file; every consumer follows by path; and the guard goes red when anyone copies a value instead of referencing it.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: land the generated copies no hand may write, close the acceptance surface, and hand the feature to the next stage with measured evidence.

- [ ] T039 [P] Regenerate and chase every mirror for this feature's source files, then prove no NEW drift against the T005 baseline: `python3 scripts/python/sync-mirrors.py --write --only shared/guidelines/reporting-obligations.md`, the same for `shared/definitions/subagent-definitions.md`, `shared/workflow/external-dispatch-recipes.md`, `agents/reporter.agent.md`, `skills/internal/create-team`, `skills/external/coaching-skills` and `scripts/python/status-digest.py` (this `scripts/` pair is STRICT, so both sides must exist or `--check` fails), then `python3 scripts/python/sync-mirrors.py --check` and paste both readings into `.specify/specs/087-speckit-visualization/test-evidence/polish-mirror-check.txt` — the eight rows of plan.md § Mirror Obligations are the coverage this row is judged against — [blockedBy: T010,T015,T024,T030] [green: contracts/reporting-obligations.contract.md#C-13]
- [ ] T040 Generate the four per-tool copies of the new command and prove the generator is repeatable: `python3 scripts/python/regen-command-copies.py` then `python3 scripts/python/regen-command-copies.py --check` (expected `OK: all per-tool command copies match the source templates.`, exit 0), then `ls` the four `speckit.status.*` paths and paste all readings into `.specify/specs/087-speckit-visualization/test-evidence/polish-command-copies.txt` — no `.hermes/` or `.codex/` path is asserted (see § Environment Prerequisites) — [blockedBy: T029]
- [ ] T041 Run the closure baseline diff and the zero-new-machinery audit over the delivered change: capture the node-id-level before/after comparison for the affected pre-existing suites (the six named in `contracts/ownership-map.contract.md` § C-51) using `/speckit.implement`'s `**Test runs**` baseline form, and audit `git diff --name-only 56f3f881..HEAD` for process-spawn, scheduler, store and channel sites plus the `scan-confirmation-gates.py --summary` count (measured 2026-11-06 baseline: 27 blocking gates, and a compliant change leaves it at 27) — both readings into `.specify/specs/087-speckit-visualization/test-evidence/cl-01-closure.txt` — [blockedBy: T040] [green: contracts/ownership-map.contract.md#C-51]
- [ ] T042 Record the feature's success-criterion evidence table: for SC-001…SC-007 (each `final`-path) name the capture file that proves it and the command that produced it, and for SC-008/SC-009/SC-010 (`supporting`) name the measurements T041 and the guard produced, all into `.specify/specs/087-speckit-visualization/test-evidence/success-criteria.txt`, marking any criterion whose evidence is a green check without a captured reading as `not-measured` rather than `pass` — [blockedBy: T037,T038,T041] [green: contracts/ownership-map.contract.md#C-52]
- [ ] T043 Implement the remaining named guard propositions RO-05…RO-12 as decidable reads over the captured artifacts (content labels plus explicit blocker, supervision closure, stall anchor resolution with zero second numeric set, the three transition classes with pre-tick timing, profile plus recorded switch, no interrogative or approval line, suppressed-tick `reporter-failure` line, carrier value from the two legal forms) — each returns `pass` / `fail` / `not-evaluated` plus a reason, and each is exercised by its mutation fixture from T033 — [blockedBy: T022,T031,T033,T037] [green: contracts/supervision-report.contract.md#C-40]
- [ ] T044 Re-run the whole guard over the delivered tree after T039/T040/T043 and confirm GATE-2 plus DoD-2 hold: `python3 scripts/python/status-digest.py --action guard`, `pytest -m contract tests/contract/test_reporting_obligations.py tests/contract/test_roster_reporter_seat.py tests/contract/test_coaching_reporting_duty.py tests/contract/test_status_digest.py`, `pytest tests/unit/test_status_digest_unit.py`, all readings appended to `.specify/specs/087-speckit-visualization/test-evidence/us4-guard-verdict.txt` with a dated closing section — this row re-runs the suite and owns no clause of its own — [blockedBy: T039,T040,T043]
- [ ] T045 Record the compatibility baseline outcome and the feature's stage state: append the before/after node-id verdict plus the one declared expected delta (`REQUIRED_FIELDS` gaining `reporting-cadence`) to `.specify/specs/087-speckit-visualization/test-evidence/cl-01-closure.txt`, and update `.specify/memory/features.md` row 087 and `.specify/memory/features/087.md` to the state `/speckit.implement` legitimately lands (never claiming `Implemented` from this stage) — [blockedBy: T041] — plus one `status=not-run-docs-only` line in `test-evidence/pre-change-measurements.md` closing the pre-change side
- [ ] T046 Sweep the cross-artifact environment and premise claims for drift after implementation: grep the feature's artifacts for environment verdicts that contradict the § Environment Prerequisites probes and for counts that no longer match the tree, correct the stale side in the SAME run, and record the sweep's queried set plus its zero-or-n findings in `.specify/specs/087-speckit-visualization/test-evidence/premise-drift-sweep.txt` — [blockedBy: T045]

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: no dependencies, starts immediately. T002–T005 are parallel-safe (four distinct capture files).
- **Foundational (Phase 2)**: depends on Setup; **blocks Phase 3, 4, 5 and 6**. T006/T007 are the red-first tests, T008/T009 the implementations they turn green, T010 the pointer surfaces.
- **User Stories (Phases 3–6)**: all depend on Phase 2. In this feature they are also **serialized** by a shared write target: Phases 3, 4 and 6 all extend `scripts/python/status-digest.py`, and Phases 3, 4 and 6 all extend `tests/contract/test_reporting_obligations.py`, so their implementation rows carry `[blockedBy:]` on the predecessor rather than `[P]`. Each phase's own test rows stay parallel with their siblings.
- **Polish (Phase 7)**: depends on every story phase it mirrors and closes (T039 on T010/T015/T024/T030; T040 on T029; T043 on T022/T026/T031/T033/T037; T041 on T040; T042 on T037/T038/T041; T044 on T039/T040/T043; T045 on T041; T046 on T045).

### User Story Dependencies

- **US1 (P1)**: starts after Phase 2. No dependency on other stories.
- **US2 (P1)**: starts after Phase 2; its implementation rows sequence behind US1's renderer extension (`status-digest.py` and the reporter Template T014) but its acceptance surface (the coaching payload and the supervision report) is independently testable without US1's cadence lines.
- **US3 (P2)**: starts after Phase 2; consumes the reader T006/T009 pinned and extends the same script, so it queues behind US2's script edits.
- **US4 (P3)**: starts after Phase 2; the guard's proposition set is complete only once the artifacts of US1–US3 exist (T043 depends on T022/T026/T031/T033/T037).

### Within Each User Story

Tests before implementation (red first) → the authored section → its mirror/generated copies → render-verify with captured output → refresh/readability verify. No row ticks a criterion against a check it did not run.

> **WARNING ADJUDICATION (author's verdict — `scripts/python/validate-tasks.py` reports 0 errors and 13 warnings: 9 `green-cross-phase`, 4 `green-path-divergence`; no `green-dangling`, no `green-clause-collision`)**
>
> The clause ids in this feature's contracts are dense per file but were partitioned **across five documents by subject** (the owner document, the seat, the status line, the supervision report, the digest, the ownership map), and the contract ids follow the *design* reading order while task IDs follow *execution* order. Two consequences follow, and both are intended, not defects:
>
> 1. **`green-cross-phase` — accepted, 9 occurrences.** A row claims the clause its own phase actually turns green. E.g. T014 (US1) turns the Template's authority clause green while T015 (same phase, one row later) turns the seat-schema clause green; T036 turns the zero-new-machinery prohibition green while T037 renders the guard verdict over it. Collapsing these into ascending clause order would force a row to claim a clause it does not turn green, which is the defect this tag exists to prevent. The authoritative statement of the partition is the per-phase distribution, not a numeric monotonicity.
> 2. **`green-path-divergence` — accepted, 4 occurrences, all against `tests/contract/test_reporting_obligations.py`.** This one test file legitimately carries clauses of THREE contracts (status-report, supervision-report, ownership-map) because they are all assertions about the same delivered artifacts. Per the create-tasks rule for this exact case, the file's clause ranges are **partitioned across rows** — T012 (US1, `status-report`), T021 (US2, `supervision-report`), T032 (US4, `ownership-map`) each name the clauses they are responsible for turning green. The check is scoped to a *whole test path per row*, which a partitioned file necessarily trips; the partition, not the warning, is the satisfiable form.
>
> **What is NOT accepted**: no clause id is claimed twice (verified: 0 duplicates) and every claimed clause resolves against its contract (0 `green-dangling`). This partition does NOT claim all 52 clauses: 15 are consciously left unclaimed on the principle that a row must not claim a clause it does not turn green in its own phase — `reporter-seat#C-14` (the Template's file existence and frontmatter keys land in Phase 1's baseline plus T014), `reporter-seat#C-21` (the guard's stdlib-only, single-file property is judged at closure, T041), `status-report#C-23` and `#C-30`, `supervision-report#C-36`, `ownership-map#C-48`, and the nine `reporting-obligations` clauses whose subject is a rule stated inside the owner text rather than an artifact a single row produces (they are exercised through T007 and T038 instead). A later `/speckit.analyze` pass SHOULD read this list as the coverage question to settle — an unclaimed clause is a clause nobody is scheduled to prove.

### Parallel Opportunities

- Setup: T002, T003, T004, T005 — four different evidence files.
- Foundational: T006 and T007 are two different test files; T010 is a third and fourth file (the two pointer surfaces) and can land with T009.
- US1: T011 and T012 (two test files) in parallel; then T013 and T014 (guard script and Template) in parallel; T015 after T008; T016 → T017 → T018 → T019 are sequential on one script.
- US2: T020 and T021 in parallel; T022 → T023 → T024 → T025 sequential on the script then one skill file and its test; T026 → T026A/T026B/T026C.
- US3: T027 and T028 in parallel; T029 → T030 → T031 sequential.
- US4: T032 and T033 in parallel; T034 → T035 → T036 → T037 → T038.
- Polish: T039 and T040 are different generated trees; T043 then closes over both.

---

## Parallel Example: User Story 1

```text
# Two independent red-first test files, launched together:
Task: "Author tests/contract/test_roster_reporter_seat.py (three roster fixtures + reason set)"
Task: "Author the US1 status-report assertions in tests/contract/test_reporting_obligations.py"

# Then the two independent implementation files:
Task: "Author skills/internal/create-team/scripts/validate-roster.py"
Task: "Author agents/reporter.agent.md"
```

---

## Implementation Strategy

### MVP First

**MVP scope rule**: the MVP is the smallest set of same-priority user stories whose checkpoints are each independently testable. Here **both P1 stories (US1 + US2) form the MVP**: US1 alone emits cadence lines but the user's stated core complaint is equally about supervised silence, and US2 is the case where an invisible monitor is indistinguishable from a hang (`requirements.md` US2 "Why this priority"). US1 and US2 together are one independently valuable increment; US3 (the on-demand digest) and US4 (the ownership guard) follow.

1. Complete Phase 1: Setup (baselines re-measured, scratch areas exist)
2. Complete Phase 2: Foundational (owner document + shared reader) — **this gates everything**
3. Complete US1 + US2 → **STOP and VALIDATE** at both checkpoints (cadence lines with attribution; supervision report over two sub-flows)
4. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → the owner exists and one cadence definition site is declared
2. + US1 → teams report on cadence, a missing seat is a named defect → validate → demo
3. + US2 → supervising masters report every sub-flow, slow ≠ stalled, failures beat the clock → validate → demo
4. + US3 → `/speckit.status` answers "what is running right now?" on demand, bounded and honest about age
5. + US4 → the guard judges the obligation mechanically and goes red on a copied literal
6. Polish → mirrors and per-tool copies regenerated, closure diff taken, success criteria each backed by a captured reading

---

## Notes

- `[P]` marks different write targets only; the four phases that extend `scripts/python/status-digest.py` and `tests/contract/test_reporting_obligations.py` are sequenced with `[blockedBy:]` instead.
- No clause id is claimed twice (`[green:]` partition): 37 of the contracts' 52 clauses are claimed by a row, and the 15 unclaimed ones are enumerated with their reasons in § Dependencies & Execution Order — an unclaimed clause is a coverage question for `/speckit.analyze`, never silently dropped.
- The 30-second value is authored once (T008) and every other row reaches it by anchor; T034 exists to make a copy fail.
- Deferral discipline: a `[~]` row is a deliberate, recorded handoff in `verification.md` (`deferred_tasks=`), never a silent open row. Two rows are the plausible candidates and both must still be attempted first: T031 (needs a live registry) and T018 (needs a live console) — see § Environment Prerequisites.
- The two evidence sinks `test-evidence/us4-guard-verdict.txt` and `test-evidence/cl-01-closure.txt` are append-only: rows may add sections, no row owns them as its green point.
- IDs `T017A`, `T026A/T026B/T026C` were appended inside their own phase instead of renumbering T018 onward: the ordering still reads top to bottom, and no existing id moved.
