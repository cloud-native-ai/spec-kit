# Contract — High-order executors (C-063…C-078, C-093…C-094)

**Scope**: the three grains above a single body — goal, team and loop — and the coordinator that sits at each of
them. These clauses bind the owner documents already named by the existing definitions and do not invent a
parallel hierarchy.

---

## A. Goal grain

- **C-063** — A goal slice MUST record, per stage, whether it decomposes; the record MUST resolve through
  `decomposition-coverage.yaml` rather than restating a stage list. ([[STR-007]], FR-029)
- **C-064** — A goal MUST NOT declare a target covered until the slice's own deliverables exist; a covered stage
  with a missing deliverable is `coverage-hollow`. (FR-029)
- **C-065** — A goal's targets MUST be partitioned into work packages whose count is limited by the slot cap read
  at execution time, not by a number copied into the goal text. (FR-015, T-001)

## B. Team grain

- **C-066** — A team's members MUST each carry a class, and the team MUST state how many of its members can run at
  once; the statement MUST be derivable from the member classes and the slot cap, not asserted independently.
  (FR-020, FR-027, C-064 family)
- **C-067** — A team MUST NOT be instantiated with more concurrent members than its declared capability supports;
  the instantiation step MUST read the capability verdict per agent (C-037) and MUST report the reduction when it
  applies. (FR-021, FR-022, FR-027)
- **C-068** — The stage-team preset MUST carry the obligation rather than the instantiated team text carrying a
  hand-written parallel section; a preset that omits it is `preset-gap`. (FR-026, C-061)

## C. Loop grain

- **C-069** — A loop stage MUST declare its own decomposition coverage and MUST NOT inherit the previous stage's
  coverage by adjacency. (FR-017, FR-028, FR-029, C-063)
- **C-070** — A loop MUST record per stage the requested and effective concurrency in the run record, so two stages
  of the same run can be compared. (FR-008, FR-028, C-058)
- **C-071** — The loop driver MUST pass the capability verdict and the slot cap down to each dispatch, so a
  sub-stage cannot be dispatched to an incapable executor because the top-level caller forgot. (FR-022, FR-028,
  C-037)

## D. Coordinator dispatch

- **C-072** — The coordinator's dispatch verdict (whether this coordinator may dispatch at all) MUST be read from
  its registered fact, and the coordinator MUST behave identically when the verdict is absent: refuse to claim
  concurrency, declare serial with the `mechanism-not-yet-landed` string. (FR-021, FR-023, [[STR-010]], [[STR-011]],
  C-016, T-004)
- **C-073** — The coordinator MUST partition before it dispatches; a coordinator that dispatches ad hoc packages has
  no package count to report and is `unpartitioned`. (FR-024, [[STR-006]])
- **C-074** — The coordinator MUST report the real execution shape even when it is serial, naming the missing
  mechanism as the reason code. (FR-024, C-059)
- **C-075** — When the coordinator's own toolset lacks dispatch, the partition it produces MUST remain a usable
  artifact: each package MUST name its scope, its inputs and its output path, so a later capable executor can run
  the packages without re-deriving them. (FR-024, R-10)

## E. Sub-agent obligation inheritance

- **C-076** — A dispatched sub-agent MUST receive the concurrency obligation as part of its brief, not inherit it
  implicitly; an implicit obligation is not checkable at the sub-agent boundary. (FR-002, C-044)
- **C-077** — A sub-agent's return MUST carry its own concurrency triple; a sub-agent report with the triple absent
  is `report-incomplete` and MUST be reported by the coordinator rather than filled in by the coordinator.
  (C-058, FR-023)
- **C-078** — The existing subagent definitions MUST keep their current taxonomy; the obligation attaches to the
  execution bodies, and the definition layer only names the obligation's anchor. No new subagent type is created.
  (FR-025, Constitution IX, R-3)

## F. The analyze wave and its mechanism

- **C-093** — The `analyze` stage MUST default to N concurrent SDD Analysis Workers
  (`agents/sdd-analysis-worker.agent.md`), N taken from the stage's team configuration / the spine's
  `agent_concurrency_requested`; a serial analyze (`N = 1`) is admissible only with a code from the closed
  vocabulary. The wave MUST declare each Worker's read domain as a file-level path set before dispatch (the FR-012
  form) and MUST go red on any pre-dispatch read-domain intersection; it MUST consolidate the N findings by one
  deterministic rule (declared read-domain order, then finding id lexicographic order, cross-Worker duplicate ids
  broken by first declaration with a pointer to the suppressed copy); and it MUST record the
  requested / effective / effective-reason triple plus each Worker's `executor_id` and its verdict's `verifier_id`.
  The stage's default value is owned by `decomposition-coverage.yaml` ([[STR-007]]) and MUST NOT be restated here.
  (FR-034, FR-028, FR-016)
- **C-094** — The concurrency mechanism MUST be the fork model: each concurrent unit is a separate `qodercli` child
  process launched through `skills/external/sdd-loop-driver/scripts/stage-runner.sh` (prompt through stdin,
  `--output-format stream-json`, completion judged by the stage sentinel), and the process pool's upper bound MUST be
  the host's `nproc` reading taken at dispatch — never a frozen constant. Host-internal agent fan-out (in-process
  subagents sharing one process and one CPU core) MUST NOT be recorded as the concurrency mechanism and MUST NOT be
  counted as satisfying FR-005(d); the external-process branch of FR-005(d) is what this clause fixes. The runner's
  own `--help` contract and `references/dispatch-recipes.md` are the mechanism's owners; no second runner rule is
  introduced. (FR-035, FR-021, FR-008)
