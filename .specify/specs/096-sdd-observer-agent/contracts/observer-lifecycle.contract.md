# Contract — Observer Lifecycle（启动、记录节、重启与收束）

Scope: `skills/external/sdd-loop-driver/SKILL.md` § SDD Observer, `skills/external/sdd-loop-driver/references/observer-lifecycle.md`, and the one pointer line in `references/stage-prompts.md` § 状态脊. Requirements: FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-020, FR-021, FR-023.

## C-01 — Entry switch

The U0 entry declaration accepts `observer: on|off`, default `on`. `off` is recorded in the state spine observer record section as `state: disabled` with a reason and disclosed in the U6 close-out report; it is never a silent absence.

## C-02 — Startup point is the driver's, mechanically decidable

The driver starts the observer after the line is registered and the state spine exists, and **before** the first stage's U2 dispatch (before the first stage prompt is issued). The judgment is exactly: spine exists + line registered + U2 not yet dispatched. The startup step MUST NOT be placed inside any stage command.

## C-03 — Startup outcome is recorded

The startup attempt and its result (`started` / `failed` / `disabled`) are written to the state spine observer record section by the driver, with the identity fields of C-04. A failed start carries a one-line reason.

## C-04 — State spine observer record section (key and shape owner)

The section shape is owned by `SKILL.md` § SDD Observer and is exactly:

```text
## Observer Record — <YYYY-MM-DDTHH:MM:SSZ>
- state: started | failed | disabled | closed
- line_id: <value>
- run_id: <value>
- spec: <NNN-slug>
- instance: <instance slug>
- execution_label: <label or ->
- started_at: <UTC ISO-8601 or ->
- reason: <one line or ->
```

Sections are append-only; the latest wins for current state. The observer itself MUST NOT write the state spine.

## C-05 — One dedicated instance, one journal

The line owns exactly one Observer Instance (identity = `line_id` + spec key) and one journal at `.specify/specs/<NNN-slug>/journal.md`. Two lines MUST NOT share an instance or a journal. The observer is not registered as a write line (not in the closed write-role set `root` / `coordinator` / `agent-write`), occupies no worktree and enters no integration queue.

## C-06 — Bounded execution, at most one live execution

An observer execution is a bounded window whose boundaries are the existing dispatch turn budget and stage deadline. At most one unresolved execution exists per line: the driver MUST NOT dispatch a next execution while the previous `.status` record is unsettled, and the journal engine refuses a second concurrent writer. No scheduler, timer service, daemon or resident service is introduced.

## C-07 — Restart at stage boundaries

When an execution ends before the line terminal (failure, stall, window expiry), the driver MAY start the next execution from the same instance at the next stage boundary. A restart appends to the same journal and produces one `observer-gap` for the uncovered window. Restart MUST NOT change any stage's retry count, timeout judgment or completion-sentinel judgment.

## C-08 — Line-terminal close and the final execution

At the line terminal (after the last declared stage, before the outer close-out), the driver starts one final observer execution whose assignment settles the journal: it appends `line-terminal` and `observer-settle` via `journal-utils.py --action append --final`. If that execution cannot start or fails, the driver records `state: failed` plus the reason in the spine; the journal is never rewritten to fake a closure.

## C-09 — Non-blocking, disclosure-only

Observer existence, absence, health, conclusions and journal content MUST NOT gate any stage advance (U4), checkpoint, review or merge. Failures are recorded in the spine record section and disclosed in the existing U6 close-out report; that disclosure obligation is the only closure duty. The observer emits no user-visible report, question or approval request.

## C-10 — Scope

The mechanism applies to driver-driven SDD lines, including nested runs called from a team seat; a nested run owns its own observer and journal and its observer MUST NOT observe the outer team run. Non-SDD command runs and team runs that carry no SDD line produce no observer and no journal.

## C-11 — Dispatch brief carries its obligations

The observer dispatch prompt carries: the assignment (line, spec, spine, state dir, journal path, label, window), the fast-fail injection clause, the concurrency obligation pointer, the read domain, the write surface, the forbidden capabilities, and the requirement that its return carries an explicit anomaly line (`未发现异常` or `ANOMALY:`). The brief MUST NOT reference the driver skill and MUST NOT contain loop logic.

## C-12 — Driver text remains the single owner; references point

The SKILL.md section owns C-01…C-10; `references/observer-lifecycle.md` owns the dispatch brief template, the engine invocation loop and the failure semantics; `references/stage-prompts.md` § 状态脊 carries one pointer line to the record section and no copy of its keys.
