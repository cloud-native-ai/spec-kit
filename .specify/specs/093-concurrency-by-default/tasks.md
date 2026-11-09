# Tasks: Concurrency by Default（subagent 并发作为框架基本属性）

**Requirement ID**: 093
**Requirement Key**: 093-concurrency-by-default
**Related Feature**: Feature 093 Concurrency by Default (`.specify/memory/features/093.md`)
**Input**: Design documents from `.specify/specs/093-concurrency-by-default/`
**Prerequisites**: plan.md (required), requirements.md (required for user stories), research.md, data-model.md, contracts/, quickstart.md, feature-ref.md — all present and validated 2026-11-09

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" is non-negotiable: "Pure functions/utilities MUST have unit tests", "Critical flows MUST have automated regression coverage", "Integration/contract tests MUST cover cross-service communication and external APIs"; plan.md § Constitution Check row IV is Pass). Every user-story phase therefore opens with its red-first test rows, and each test row turns a named contract clause green rather than restating it.

**Tests**: MANDATORY. Each phase's test rows are written first and MUST fail before their implementation rows land; the red run is pasted into `notes/red-first-evidence.md` (landing point fixed by `create-tasks` SKILL.md § Runtime-evidence landing points).

**Organization**: tasks are grouped by the five user stories of `requirements.md` (US1–US5; the four P1 stories form one MVP increment), plus a Setup phase, a Foundational phase that blocks every story, and a final Polish & Release phase. This feature is doc-feature shaped in part (declaration facts, concept owners, agent definitions, command templates) and engine shaped in part (one Python checker plus ten test modules); `references/phase-shapes.md` was consulted and the doc-feature taxonomy (author-section → mirror-parity → render-verify → refresh-verify) is applied inside US1 for the declaration facts, while the engine keeps the ordinary models → services shape.

## Definition of Done (DoD)

- DoD-1: The FR-001…FR-035 rows of `feature-ref.md` each resolve to at least one implementation row, and every contract clause C-001…C-094 is owned by at least one row. `[green: <contract>#<clause>]` is used as a **red-first marker**, not as a clause-registration table: every row carrying it claims a distinct contract clause, exactly one row per test-module path carries it, and a row that only refines an already-marked surface carries none — the machine form of this sentence is `validate-tasks.py` exiting 0 with zero WARN (`green-clause-collision` / `green-path-divergence` / `green-cross-phase`), never a hand count. The complete clause→row delivery map lives in `feature-ref.md` § FR→clause delivery map and is not duplicated here. `validate-tasks.py` exits 0 with zero ERROR and zero WARN
- DoD-2: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/093-concurrency-by-default/tasks.md` exits 0 with zero ERROR and zero WARN — the run is recorded in `test-evidence/validate-tasks.txt`
- DoD-3: `pytest -m contract` on CPython `>=3.8` is green with zero NEW failures against the frozen name baseline, and the nine new contract modules plus one unit module are in the suite
- DoD-4: `python3 scripts/python/sync-mirrors.py --check` reports no NEW drift against `test-evidence/mirror-baseline-plan.txt`, and the per-tool command copies were regenerated rather than hand-edited
- DoD-5: `scripts/python/concurrency-check.py` satisfies the script interface contract (Principle XXI): `-h` / `--help` and `--version` act on nothing, an undeclared option is rejected non-zero, and each of the five actions has at least one unit assertion
- DoD-6: The concurrency reading of this feature's own implement run is recorded with `effective` taken from interval overlap — `>= 2` with a coordination report if the executor dispatched, otherwise the literal `not_evaluated` plus reason code `mechanism-not-yet-landed` (never `0`, never an estimate, never a serial run presented as concurrent)
- DoD-7: Every `final`-path success criterion (SC-001…SC-006) carries `SC-NNN_status=` in `verification.md` with a fresh-context verifier verdict, and every `supporting` one (SC-007…SC-012) carries its own or an explicit waiver
- DoD-8: 064 / 070 / 086 / 092 affected assertions each carry a disposition record (`owner-moved` / `pointer` / `dated-record` / `retained` / `explicitly-removed`) and no existing module was edited to make a new module pass
- DoD-9: The coordinator dispatch verdict (`coordinator-dispatch-verdict.yaml`) reads `allow` or `forbid` from its owner, and no row in this file adjudicated it by itself

**DoD Status**: pending

## Completion Gate

- GATE-1: Full test suite has zero NEW failures vs the frozen baseline — check: `python3 -m pytest -q > .specify/specs/093-concurrency-by-default/test-evidence/suite-after-implement.txt 2>&1` then compare the sorted `FAILED`-prefixed names against `.specify/specs/093-concurrency-by-default/notes/test-baseline.txt` with `comm -13`
- GATE-2: Every mirror obligation from `plan.md` § Mirror Obligations verified byte-identical — check: `python3 scripts/python/sync-mirrors.py --check` (must match `test-evidence/mirror-baseline-plan.txt` on every pair) plus `python3 scripts/python/regen-command-copies.py --check`
- GATE-3: No open or claimed task rows remain — check: `grep -cE '^- \[[ >]\]' .specify/specs/093-concurrency-by-default/tasks.md` returns 0
- GATE-4: Every `final`-path success criterion is `pass` **and** the feature's smoke record is present — check: in `.specify/specs/093-concurrency-by-default/verification.md`, every criterion whose `**Path**` marker reads `final` (SC-001…SC-006) has `SC-NNN_status=pass`, and `smoke_command=`, `smoke_exit_code=0` and `smoke_evidence_path=` (an existing non-empty path) are all present. Condition set owner: `shared/workflow/acceptance-hardening.md` § Gates — this row carries the check, not a second schema
- GATE-5: The new engine obeys the script interface contract — check: `python3 .specify/scripts/python/script-interface-check.py scripts/python/concurrency-check.py`
- GATE-7: The inherited `086:SC-010` gap keeps a named owner — the acceptance record cites 086's existing gate and asserts 093 neither closes nor inherits it (FR-033); check: `grep -n "086:SC-010" .specify/specs/093-concurrency-by-default/verification.md` resolves to a row naming 086's gate
- GATE-6: This artifact keeps its structural guarantee — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/093-concurrency-by-default/tasks.md` exits 0

## Environment Prerequisites

- CI runner: **not required** — probe: `ls .github/workflows` @ 2026-11-09 lists the repo's workflows, none of which this feature's gates ride; affected phases/tasks: none
- New third-party dependency or package index: **not required** — probe: `grep -nE '^(dependencies|requires-python)' pyproject.toml` @ 2026-11-09 (plan.md RS-001/RS-002 add zero dependency); affected phases/tasks: none
- Container runtime, live cluster or special hardware: **not required** — probe: `ls tests/fixtures` @ 2026-11-09 (declarative fixture sets only, no runtime probe in this feature's rows); affected phases/tasks: none
- Host parallel dispatch capability: **runtime-dependent, probed per run, never frozen** — probe: the executing body's own tool list at dispatch @ 2026-11-09; **corrected at analyze 2026-11-09 (F-093-012): the executing body holds a host dispatch tool** — the earlier reading ("no dispatch tool") was a false constant, and the analyze stage itself held the tool. This line's stages did not dispatch, and the `mechanism-not-yet-landed` code rides on the feature's own deliverable (the facts, the engine, and the FR-035 fork runner path), not on the host's tool set. Affected phases/tasks: T101 / T103 / T105 and the SC-006 evidence plan (T106 / T110), plus the FR-005(d) condition. This is the only externally dependent verdict in this file; every row that depends on it points here.
- CPython lower bound: **available** — probe: `python3 --version` @ 2026-11-09, against `pyproject.toml` `requires-python` `>=3.8` (plan.md EP-001); affected phases/tasks: every engine and test row

**A13 boundary** (owner: `shared/workflow/acceptance-hardening.md` § Gates — this pointer, not a second rule): this section records task-generation probe verdicts only, each with its probe command and an ISO date. A planning-time premise belongs to `plan.md` § Execution Premises; an inherited record belongs to `plan.md` § Inherited Blockers.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: can run in parallel — different files, no dependency on an incomplete row
- **[Story]**: `US1`…`US5`; story phases carry exactly one, non-story phases carry none
- **[blockedBy: Txxx,Tyyy]**: the row MUST NOT start until every listed row is `[X]`
- **[green: <contract>#<clause>]**: the row that turns that clause green. Each clause a row claims (C-001…C-094) is claimed exactly once across this file — a strict subset of the clause space may stay unclaimed outside the test-module and fact-file rows — so the attribution **is** the clause partition over claimed clauses (`feature-ref.md` § Delivery map maps FR → clause; this file maps clause → row). Each of the ten test-module paths appears in exactly one row.
- Contract paths resolve relative to this file's own directory (`contracts/…`)

### Task State Sigil (REQUIRED)

`- [ ]` open · `- [>]` claimed / in progress (multi-agent runs flip it when picking a row up) · `- [X]` closed · `- [~]` deferred with a recorded reason. A run is not complete while any `[ ]` or `[>]` remains.

## Path Conventions

- Framework sources (the "source" hat): `shared/`, `scripts/`, `skills/`, `agents/`, `templates/`, `tests/`
- Client runtime projections (the "runtime" hat, never hand-edited): `.specify/shared/`, `.specify/scripts/`, `.specify/skills/`, `.specify/agents/templates/`, plus the per-tool command copies under `.claude/commands/` and `.qoder/commands/`
- Spec dir: `.specify/specs/093-concurrency-by-default/`
- All paths are repository-root relative

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: create the landing points and freeze the measurements every later row reads. No row here changes behaviour.

- [ ] T001 Create `.specify/specs/093-concurrency-by-default/notes/` and seed `notes/red-first-evidence.md` with its header only (command / real output / exit status) as the fixed landing point for every red-first row
- [ ] T002 Capture the pre-change test baseline by FAILURE NAME into `notes/test-baseline.txt` — run `python3 -m pytest -q`, keep the whole record in `test-evidence/suite-baseline-093.txt`, derive the name list from it; the comparison form is owned by `/speckit.implement` step 6 `**Test runs**` (pointer, not restated) — covers FR-002
- [ ] T003 Measure the pre-change enumeration counts (trap form included) into `notes/pre-change-measurements.md` — measured 2026-11-09: `ls -d skills/internal/*/` → **38**, `ls -d skills/external/*/` → **16**, `ls templates/commands/*.md` → **29**, `ls agents/*.md` → **17**, `ls -d .specify/teams/*/` → **12**, `ls -d .specify/anchoring/*/` → **6** (the former `.specify/goal` tree, renamed by 090 and merged 2026-11-09; enumerable bodies **118**); trap form: `ls -d .specify/skills/*/` yields **16** flat *external projections* on top of the 38 `internal` dirs, so counting the projection tree gives 54 entries on a different reading — the roots are the five patterns in `shared/declarations/facts/executor-enumeration-roots.yaml`, not the projection tree
- [ ] T004 Author the eight fact files under `shared/declarations/facts/` (`concurrency-class`, `serial-reason`, `effective-concurrency`, `concurrency-slot-and-reserve`, `decomposition-coverage`, `executor-enumeration-roots`, `concurrency-contract`, `coordinator-dispatch-verdict`) as parseable block-subset stubs — exactly eight files, slug equal to stem [green: contracts/declaration-facts.contract.md#C-001]
- [ ] T005 Register the eight slugs in `shared/declarations/contract.yaml` (append-only, existing keys untouched) so `python3 .specify/scripts/python/declaration_reader.py --action list` lists all eight under `facts` — measured baseline 2026-11-09: `facts` **23** entries, `contract` **9** keys, and `--action get --fact concurrency-class` exits **1** with `no declaration for fact 'concurrency-class'` (the unregistered shape, quickstart S-0)
- [ ] T006 Freeze the contract coverage baseline — `python3 scripts/python/account-clause-coverage.py .specify/specs/093-concurrency-by-default --freeze > .specify/specs/093-concurrency-by-default/coverage-baseline.txt`; confirm **92** clauses by `grep -c '^- \*\*C-[0-9][0-9][0-9]\*\*'` over the five clause-bearing files (trap form: the same grep without the `^- ` anchor also matches ids cited inside prose and returns a larger number — the unit is a clause *definition*)
- [ ] T007 [P] Re-read the untouched mirror baseline as `test-evidence/mirror-baseline-tasks.txt` — pointer: the pairs and counts stay owned by `test-evidence/mirror-baseline-plan.txt` and `plan.md` § Mirror Obligations

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: the declaration layer's values and the engine's I/O contract — every user story reads these.

**⚠️ CRITICAL**: no user-story row may start before this phase is closed.

- [ ] T008 Author `shared/declarations/facts/concurrency-class.yaml` — the closed class member set with each member's semantic name, `applies_to`, `obligation`, `unit_form`, `owner_anchor`, plus the FR-004 decision rule (layer + produced shape)
- [ ] T009 Author `shared/declarations/facts/executor-enumeration-roots.yaml` — exactly five roots, each a **path pattern** (never a count), each mapped to the class ids it may receive members from (V-4)
- [ ] T010 Author `shared/declarations/facts/serial-reason.yaml` — the closed code vocabulary grouped into `condition-bound` and `factual`, each code with its one-line meaning, its bound FR-005 condition, its evidence form and the declared order (FR-006)
- [ ] T011 Author `shared/declarations/facts/effective-concurrency.yaml` — the fields `requested` / `effective` / `effective_reason`, the `not_evaluated` literal and the maximum-interval-overlap rule with its tie-break (FR-008)
- [ ] T012 Author `shared/declarations/facts/concurrency-slot-and-reserve.yaml` — `slot_cap_default`, `verifier_reserve`, the per-unit budget and round ceiling, the `min(slot_cap, ceiling, remaining)` formula, with the ceiling named as a projection of `wp-gate.py` rather than a second value (FR-014, FR-015, FR-020)
- [ ] T013 Author `shared/declarations/facts/decomposition-coverage.yaml` — per-stage coverage (`auto` / `on` / `off` plus the named decision), the `analyze` default override required by FR-034 (N-way concurrent; N read from the stage team configuration / spine key, never frozen), and the explicit relation to the spine's `decomposition` / `decomposition_stages` / `decomposition_slot_cap` keys (FR-029, FR-034)
- [ ] T014 Validate every fact against the declaration schema before anything reads it — mandatory keys from `required_fact_keys`, a `kind` from `fact_kinds`, `fact:` equal to the stem, inside `block-subset/v1`; run `declaration_reader.py --action get --fact <slug>` for all eight and paste the exits [green: contracts/declaration-facts.contract.md#C-002] — covers FR-002 and FR-033 (the registration and disposal faces of the declaration layer)
- [ ] T015 Assert the kind assignment per fact in `tests/unit/test_concurrency_check_engine.py` — every fact's `kind` is a member of `fact_kinds` read from `shared/declarations/contract.yaml`, and the eight stems equal their `fact:` values [green: contracts/declaration-facts.contract.md#C-003]
- [ ] T016 Author the "registration is a read behaviour" judgement in `tests/contract/test_concurrency_declarations.py` — a slug is registered only when `--action get` resolves it AND it appears in `--action list`'s `facts` array; the mutation renames the file / breaks the `fact:` key, never merely deletes it — covers FR-010
- [ ] T017 Assert the unregistered shape is reported as `owner-unavailable` with a non-zero exit and a named message, never a default — measured 2026-11-09 the reader exits **1** for an absent fact while `script-interface-definitions.md` reserves 1 for a failed check and 2 for an input/environment error, so the consumer translates rather than propagates (recorded in `research.md` R-1) [green: contracts/declaration-facts.contract.md#C-011]
- [ ] T018 Reject a malformed fact in `tests/contract/test_concurrency_declarations.py` — a `fact:` / stem disagreement or a construct outside the YAML subset is reported, not silently dropped from the list
- [ ] T019 Prove the removal direction of registration — a fact hidden from the read surface makes the consumer report `owner-unavailable` and never fall back to a default (SC-009's mutation form) [green: contracts/declaration-facts.contract.md#C-013]
- [ ] T020 Assert source↔projection reachability in `tests/contract/test_concurrency_declarations.py` — each fact is readable from both `shared/declarations/facts/` and `.specify/shared/declarations/facts/` after the mirror sync, with identical bytes
- [ ] T021 Write the interface skeleton of `scripts/python/concurrency-check.py` — `argparse` with `-h` / `--help`, `--version`, the five actions `classify` / `serial-reason` / `reading` / `coverage` / `capability`, `--repo` and `--json-out`, and rejection of any undeclared option with a non-zero exit before any action runs [green: contracts/judgement-engine.contract.md#C-019]
- [ ] T022 Implement the five-action dispatch table in `scripts/python/concurrency-check.py` — exactly five read-only actions, no action writing anything outside `--json-out` [green: contracts/judgement-engine.contract.md#C-020]
- [ ] T023 Implement `--repo` resolution in `scripts/python/concurrency-check.py` — the root is the repository whose `shared/declarations/` is read, never an ancestor-walk guess (the self-matching trap in `plan.md` F-093-002 and `AGENTS.md` § Two Hats) [green: contracts/judgement-engine.contract.md#C-021]
- [ ] T024 Implement the JSON envelope in `scripts/python/concurrency-check.py` — every action emits `action`, `decision`, `measured` and `findings`, each finding carrying `code` and `subject` [green: contracts/judgement-engine.contract.md#C-022]
- [ ] T025 Close the engine skeleton's own gates — `python3 .specify/scripts/python/script-interface-check.py scripts/python/concurrency-check.py` exits 0 and `python3 -m pytest tests/unit/test_concurrency_check_engine.py -q` collects the new module
- [ ] T026 Author the red-first evidence for this phase into `notes/red-first-evidence.md` — for each of T015–T020 and T025 the command, its real failing output and its exit status, quoting the gate row verbatim (id + name + check command) when it binds a gate

**Checkpoint**: the declaration layer holds its values and the engine answers its interface; US1–US5 can start, US1 and US3 first.

---

## Phase 3: User Story 1 - 任何技能、命令、goal、team、loop 都默认并发 (Priority: P1)

**Goal**: the execution-body universe is derived by enumeration and every member maps to exactly one declaration class whose concurrency obligation is reachable.

**Independent Test**: `python3 scripts/python/concurrency-check.py classify --repo .` reports `decision: pass`, zero `uncovered` / `ambiguous` findings and `measured` listing each root's member count as enumerated; adding a body to a root without a class turns it red, and removing one keeps a red assertion (both directions).

### Tests for User Story 1 (MANDATORY) ⚠️

> Write these first; each MUST fail before its implementation row lands, and the red run goes into `notes/red-first-evidence.md`.

- [ ] T027 [US1] Author the enumeration-and-class contract in `tests/contract/test_concurrency_class_table.py` — every body under the five roots resolves to exactly one class and the uncovered list is empty, and the both-directions drift guard holds: a body added to a root without a class turns it red, and a body removed from the enumeration still leaves a red assertion (V-2; closed-set claim shape owner `.specify/shared/guidelines/closed-set-claims.md`) [green: contracts/declaration-facts.contract.md#C-014]
- [ ] T028 [US1] Author the both-directions drift guard's mutation record in `test-evidence/` — the two mutations of T027 run and pasted (add-without-class red, remove-still-red) with their exit statuses [green: contracts/declaration-facts.contract.md#C-015]
- [ ] T029 [US1] Author the obligation-presence contract in `tests/contract/test_concurrency_high_order.py` — each class's obligation text is reachable from the body's own text or its declared owner anchor, and an owner anchor that does not resolve is red

### Implementation for User Story 1

- [ ] T030 [US1] Implement `classify` in `scripts/python/concurrency-check.py` — build the body universe by enumerating the five roots from the enumeration-roots fact through the declaration reader, reporting per-root member counts as measured and never against a stored copy of a count [green: contracts/judgement-engine.contract.md#C-023]
- [ ] T031 [US1] Implement the class-resolution rule in `scripts/python/concurrency-check.py` — a single candidate class is assigned, multiple candidates are judged by produced shape per the FR-004 rule, an undecidable body is `uncovered` (red) and never lands in a catch-all [green: contracts/judgement-engine.contract.md#C-024]
- [ ] T032 [US1] Implement the obligation-presence read in `scripts/python/concurrency-check.py` — the text is read from the body itself or from the owner anchor its class names, and the two sources are reported distinctly [green: contracts/judgement-engine.contract.md#C-025]
- [ ] T033 [US1] Implement the `measured` block in `scripts/python/concurrency-check.py` — counts and member identities are reported as measured, never compared against a stored copy
- [ ] T034 [US1] Write the class obligation for `concurrent-by-default` into its single owning anchor named by the concurrency-class fact's `owner_anchor` — serial requires a reason code and a reviewable basis, and the basis is the form-matching evidence this same row binds (a non-empty string is not a basis)
- [ ] T035 [US1] Write the class obligation for `partition-required` — a single-unit execution is itself a decision that must be recorded, never a silent default
- [ ] T036 [US1] Write the class obligation for `serial-only` — it names which host or dependency condition applies by pointing at the reason-code fact rather than restating the vocabulary, so the class is not a free pass
- [ ] T037 [US1] Author the three-part obligation in `shared/definitions/subagent-definitions.md` — (i) consider concurrency first, (ii) name the reason code when serial, (iii) record the reading triple — each part separately checkable, at every grain (a skill or command body, a goal slice, a team, a loop stage) as one statement with grain-specific examples beneath it [green: contracts/executor-obligations.contract.md#C-042]
- [ ] T038 [US1] Keep the obligation free of scheduling internals — it MUST NOT require a body to know the slot cap, the ceiling, the budget formula or the class table; it names them by pointer only [green: contracts/executor-obligations.contract.md#C-043]
- [ ] T039 [US1] Give each grain its own pointer rather than its own rule text — `skills/internal/**`, `skills/external/**`, the 29 command surfaces and the goal/team/loop surfaces each reach the single anchor, so a fifth grain would need no fifth copy
- [ ] T040 [US1] Place the obligation in every execution body of the roots it applies to, pointing at its class owner rather than restating the obligation text
- [ ] T041 [US1] Prove the three projection trees carry the obligation identically — `skills/external/**` against `.specify/skills/**`, `templates/commands/*.md` against the regenerated per-tool copies, `agents/*.md` against `.specify/agents/templates/*.md`; the mirror engine shows no NEW drift

**Checkpoint**: US1 is independently testable — the closed set classifies cleanly, and a body added or removed moves the verdict.

---

## Phase 4: User Story 2 - 默认并发，串行必须携带具名理由 (Priority: P1)

**Goal**: the default is concurrent whenever the five conditions hold, and every serial result carries a closed-set reason code with form-matching evidence; the condition↔code pair covers in both directions.

**Independent Test**: a two-unit, dependency-free, disjoint-write, host-parallel fixture runs concurrently with `effective >= 2`; the same fixture with an injected dependency edge runs serially with `dependency-edge` and a resolvable edge; emptying or corrupting the code list turns the gate red.

### Tests for User Story 2 (MANDATORY) ⚠️

- [ ] T042 [US2] Author the serial-reason and default-concurrency contracts in `tests/contract/test_concurrency_serial_reason.py` — a two-unit dependency-free disjoint-write host-parallel fixture runs concurrently with `effective >= 2`, every serial record carries a non-empty ordered code list drawn from the closed vocabulary with no duplicates, and the condition↔code bijection is asserted in both directions against the FR-005 clause ids carried by the fact
- [ ] T043 [US2] Author the condition↔code bijection mutation in `test-evidence/` — drop one condition's code and drop one code's condition; both directions must go red, bidirectional gap zero [green: contracts/judgement-engine.contract.md#C-028]
- [ ] T044 [US2] Author the per-code evidence-shape contract in `tests/contract/test_concurrency_serial_reason.py` — evidence is judged against the code's declared evidence form, a `.` is rejected for every code, and the form/reason inconsistency is caught in both directions (concurrent pattern with codes, serial pattern with none)
- [ ] T045 [US2] Author the form/reason inconsistency mutation in `test-evidence/` — the two inconsistent shapes are injected and each is reported inconsistent with the field that is wrong named [green: contracts/judgement-engine.contract.md#C-030]
- [ ] T046 [US2] Author the evidence-form fixtures for the four condition-bound codes in `tests/contract/test_concurrency_serial_reason.py` — a dependency code needs a resolvable edge plus the blocking verdict pointer, a write-conflict code needs the intersecting path set, a host code needs the probe reading and its landing point, a budget code needs the before/after slot-and-budget readings
- [ ] T047 [US2] Author the budget-code contract in `tests/contract/test_concurrency_serial_reason.py` — a budget code is rejected when the run never measured remaining budget
- [ ] T048 [US2] Author the host-code contract in `tests/contract/test_concurrency_serial_reason.py` — a host code is never reusable across runs; it carries a landing point recording that run's probe
- [ ] T049 [US2] Author the simplicity-is-not-a-code contract in `tests/contract/test_concurrency_serial_reason.py` — "simpler", "more controllable" and "historically serial" are rejected with the vocabulary named
- [ ] T050 [US2] Author the ordered-list and no-loss contract in `tests/contract/test_concurrency_serial_reason.py` — a two-condition serial records both codes in declared order, and the list length is never reported as concurrency (FR-006's second paragraph)

### Implementation for User Story 2

- [ ] T051 [US2] Implement the code-list validation in `scripts/python/concurrency-check.py` — every code drawn from the closed vocabulary, no duplicates, declared order preserved, and the list length never reported as concurrency
- [ ] T052 [US2] Implement the evidence-form dispatcher in `scripts/python/concurrency-check.py` — each condition-bound code (dependency / write-conflict / host / budget) is judged against its own declared evidence form, and a bare `.` is rejected for every code
- [ ] T053 [US2] Implement the closed-vocabulary refusal at read time in `scripts/python/concurrency-check.py` — a code outside the `serial-reason` fact's closed set, or a duplicated code, is reported `inconsistency` naming the offending string rather than silently dropped
- [ ] T054 [US2] Implement the simplicity-is-not-a-code refusal in `scripts/python/concurrency-check.py` — a record naming simplicity, speed or cleanliness as its serial reason is reported as `inconsistency`, never accepted as a valid code
- [ ] T055 [US2] Wire the implemented branches into the `serial-reason` action envelope in `scripts/python/concurrency-check.py` — one finding per offending record, each naming its code, its condition and its evidence pointer
- [ ] T056 [US2] Implement the condition↔code bijection check in `scripts/python/concurrency-check.py` — read the condition index from the serial-reason fact and report a code without a condition, or a condition without a code, as `inconsistency` naming both
- [ ] T057 [US2] Run the red-first check for this story — `python3 -m pytest tests/contract/test_concurrency_serial_reason.py -q` fails by name before the branches land; record the failure list into `notes/red-first-evidence.md`
- [ ] T058 [US2] Implement the inconsistency finding's independence — a record may carry both a code and a condition that disagree; the reading reports the disagreement and never silently prefers one side
- [ ] T059 [US2] Record the verifier reserve as a pre-dispatch deduction in `shared/declarations/facts/concurrency-slot-and-reserve.yaml` and its reader path — under two available slots after deduction the body degrades to serial with a budget code
- [ ] T060 [US2] State the default and the exception in the owner documents this phase touches — `shared/definitions/subagent-definitions.md` states the default-concurrent obligation and `skills/external/sdd-loop-driver/references/decomposition-model.md` states that serial carries a named reason
- [ ] T061 [US2] Extend the existing `WG-15` write-domain check in `skills/external/sdd-loop-driver/scripts/wp-gate.py` with the unit-level form only — a non-read-only unit with an empty or directory-level write domain is red, no other check in that file changes
- [ ] T062 [US2] Add the per-unit reading requirement to the executor obligation text — requested, effective and the effective reason, recorded per advancing unit rather than per stage round
- [ ] T063 [US2] Require a coordinator that plans parallel packages to emit the packages and state the execution shape actually used, including a serial shape
- [ ] T064 [US2] Add the unit-record falsifiability requirement — a body that declares concurrency must be falsifiable against its run record, and the record is the evidence

- [ ] T065 [US2] State the partial-settlement rule in the decomposition model § failure isolation — a failed or timed-out unit leaves unrelated siblings uncancelled and dependents blocked with a recorded reason, and two consecutive failures escalate

---

## Phase 5: User Story 3 - 并发单元必须可划分、可隔离、可独立校验、可确定性集成、可失败隔离与重入 (Priority: P1)

**Goal**: the seven unit obligations are decided by rule — partition determinism, file-level write domains, isolation form, slot cap with verifier reserve, independent verification, declared-order integration, failure isolation and re-entry.

**Independent Test**: one fixture with two independent write units, one dependent unit and one failing unit shows writes isolated, `effective` never above the recomputed bound, verifier ids disjoint from executor ids, integration order equal on replay, the failing unit's siblings still settled, and a re-entry re-dispatch count of zero.

### Tests for User Story 3 (MANDATORY) ⚠️

- [ ] T066 [US3] Author the reading contract in `tests/contract/test_concurrency_units.py` — `effective` equals the maximum overlap count of the units' dispatch/settle intervals, requested / effective / effective-reason are judged together, and a record missing one of the three reports an incomplete reading
- [ ] T067 [US3] Author the missing-interval contract in `tests/contract/test_concurrency_units.py` — a missing interval yields the literal `not_evaluated`, the record refuses to pass, and the unit whose interval is missing is named
- [ ] T068 [US3] Author the tri-field contract in `tests/contract/test_concurrency_units.py` — one or two of the three reading fields alone is incomplete, and the effective reason must explain any shortfall against the recomputed bound
- [ ] T069 [US3] Author the bound-recomputation contract in `tests/contract/test_concurrency_units.py` — the engine recomputes the bound from the slot fact plus the ceiling reading minus the verifier reserve and reports the arithmetic it used
- [ ] T070 [US3] Author the partition-determinism contract in `tests/contract/test_concurrency_units.py` — same inputs and same rule id yield the same unit ids, layers and dependency edges (V-17)
- [ ] T071 [US3] Author the write-domain contract in `tests/contract/test_concurrency_units.py` — a non-read-only unit without a write domain is red, a directory-level write domain is red, a read-only unit's domain is empty (V-19, V-20)
- [ ] T072 [US3] Author the verifier-independence contract in `tests/contract/test_concurrency_units.py` — executor and verifier ids both present, different, and the two sets disjoint; a prose "independent verification passed" alone is red (V-21)
- [ ] T073 [US3] Author the deterministic-integration contract in `tests/contract/test_concurrency_units.py` — integration order equals the declared layer-flattened order including the tie-break and is identical on replay (V-22)


### Implementation for User Story 3

- [ ] T074 [US3] Implement the interval-overlap computation of the `reading` action in `scripts/python/concurrency-check.py` — maximum overlap count over the dispatch/settle intervals, integer only [green: contracts/judgement-engine.contract.md#C-031]
- [ ] T075 [US3] Implement tri-state and the missing-interval judgement in `scripts/python/concurrency-check.py` — `not_evaluated` as a literal, the unit's identity in the finding [green: contracts/judgement-engine.contract.md#C-032]
- [ ] T076 [US3] Implement the tri-field judgement in `scripts/python/concurrency-check.py` — an incomplete reading when any of requested / effective / effective-reason is absent [green: contracts/judgement-engine.contract.md#C-033]
- [ ] T077 [US3] Implement the bound recomputation in `scripts/python/concurrency-check.py` — read the slot fact, read the ceiling from the existing gate script's declared default, subtract the verifier reserve, and report the arithmetic
- [ ] T078 [US3] Enforce file-level write domains in `skills/external/sdd-loop-driver/scripts/wp-gate.py`'s write-domain check (`WG-15`) only — no other check in that file changes, and read-only units keep their empty domain
- [ ] T079 [US3] Record the verifier reserve as a pre-dispatch deduction in the slot fact and its reader path — under two available slots after deduction the body degrades to serial with a budget code
- [ ] T080 [US3] Add the per-unit reading requirement to the obligation text — requested, effective and the effective reason, recorded per advancing unit rather than per stage round
- [ ] T081 [US3] Require a coordinator that plans parallel packages to emit the packages and state the execution shape actually used, including a serial shape
- [ ] T082 [US3] Add the unit-record falsifiability requirement — a body that declares concurrency must be falsifiable against its run record, and the record is the evidence
- [ ] T083 [US3] Make every unit's readiness answerable only from a recorded verdict plus an evidence pointer, in the decomposition model's readiness section — the pointer is named there once, the partition rule itself stays owned by the class fact
- [ ] T084 [US3] State the integration order as declared-order in the decomposition model § integration order — the tie-break and replay equality are named there once — covers FR-017
- [ ] T085 [US3] State failure isolation and re-entry in the decomposition model — re-entry continues from recorded state and the re-dispatch count derives from records rather than a counter file, while the existing assertions of the earlier concurrency features are dispositioned in place

**Checkpoint**: US3 is independently testable — the seven obligations each have a fixture and each turns red when its implementation is missing.

---

## Phase 6: User Story 4 - 具备派发能力的执行体才允许声明并发；禁止「声明并行、实际串行」 (Priority: P1)

**Goal**: a body declaring `N >= 2` units must carry dispatch capability, declare a handoff, or use the external-process form; the 092 shape is a red defect reproduced by a fixture.

**Independent Test**: `python3 -m pytest tests/contract/test_concurrency_reproduction_092.py -q` is red before the repair and green after; the `capability` action emits a verdict per agent definition using only the existing frontmatter key; with the coordinator verdict fact absent the action exits 2 with `owner-unavailable`.

### Tests for User Story 4 (MANDATORY) ⚠️

- [ ] T086 [US4] Author the capability contract in `tests/contract/test_concurrency_dispatch_capability.py` — each agent definition's existing `capability-tools` list is read and judged, the verdict names the reading it used, and the engine introduces no frontmatter key (a new key is a defect finding)
- [ ] T087 [US4] Author the no-new-key and verdict-read contracts in `tests/contract/test_concurrency_dispatch_capability.py` — the engine introduces no frontmatter key, and the coordinator verdict is read from its fact; absent ⇒ exit 2 `owner-unavailable`, never a default
- [ ] T088 [US4] Author the coordinator-verdict-read mutation in `test-evidence/` — remove the fact and the action must exit 2 with `owner-unavailable`; restore it and the verdict is reported verbatim
- [ ] T089 [US4] Author the inconsistency-shape contract in `tests/contract/test_concurrency_dispatch_capability.py` — the statement-by-statement shape (a capability list without a dispatch tool while the body forbids dispatching; declared concurrency while the record shows one executor in order) is reported as a finding, not repaired silently, and the verdict fact's own decided value is carried in the report
- [ ] T090 [US4] Author the 092 reproduction fixture in `tests/contract/test_concurrency_reproduction_092.py` — six packages, an executor whose capability list has no dispatch tool and no declared handoff, all units returned by one executor: red before the repair, green after (V-25); "092" here is **092-goal-team-parallel** (the 6-package plan), not the 092-non-disposable row absorbed into 090 by the 2026-11-09 merge — the numbering collision is recorded as F-093-019 and the filename is kept (renaming would break every reference)
- [ ] T091 [US4] Author the anti-nesting preservation contract in `tests/contract/test_concurrency_high_order.py` — dispatch depth stays 2 and a stage body made able to carry the driver turns the test red (SC-011), while the existing subagent taxonomy keeps its current shape and the obligation attaches to it rather than replacing it
- [ ] T092 [US4] Author the shared-string ownership and registration contracts in `tests/contract/test_concurrency_declarations.py` — every shared string has exactly one owner, is written once, and the string table is registered as a closed set so a new string must revise an owner; the role separation (a reason code is not a class name, a class name is not a string id) is asserted against the same landing discipline
- [ ] T093 [US4] Author the string-registration mutation in `test-evidence/` — add a string without an owner; the closed-set check must go red
- [ ] T094 [US4] Author the role-separation and landing-discipline contract in `tests/contract/test_concurrency_declarations.py` — each string is used in its declared role only, and the discipline both live under is reachable by path

### Implementation for User Story 4

- [ ] T095 [US4] Implement the `capability` action in `scripts/python/concurrency-check.py` — read each agent definition's existing capability list, classify it capable / handoff / external / red using the existing frontmatter key only
- [ ] T096 [US4] Implement the coordinator-verdict reader in `scripts/python/concurrency-check.py` — exit 2 with `owner-unavailable` when the fact is absent, and report the verdict verbatim when present
- [ ] T097 [US4] Implement the finding envelope's detail fields in `scripts/python/concurrency-check.py` — an inconsistency finding names both statements it compared and the record it read, and the envelope carries the verdict value the fact decided
- [ ] T098 [US4] Author `shared/declarations/facts/coordinator-dispatch-verdict.yaml` with a value from its closed set and the entry condition that would change it — the row registers the verdict question and does not answer it (T-004, the coordinator-dispatch string, F-093-003) [green: contracts/declaration-facts.contract.md#C-016]
- [ ] T099 [US4] Write the dispatch-capability definition into the subagent definitions' new section — what "can create a sibling executor" means and the three execution modes; the anti-nesting depth statement is authored beside it
- [ ] T100 [US4] Add the dispatch preflight and the routing rule to `skills/internal/run-agent/SKILL.md` — a multi-unit duty assigned to an incapable body is routed to a capable one and the routing decision is recorded (FR-024)
- [ ] T101 [US4] Add the partition-before-dispatch obligation to the coordinator surfaces — a coordinator that dispatches ad hoc packages violates it, and the partition stays usable when its own toolset lacks dispatch
- [ ] T102 [US4] Require the coordinator to report the real execution shape even when serial, naming the missing capability explicitly
- [ ] T103 [US4] Require every dispatched sub-agent's brief to carry the concurrency obligation, injected at dispatch rather than inherited from an ambient layer (Constitution XVI)
- [ ] T104 [US4] Require every sub-agent return to carry its own concurrency triple, and treat a return without it as incomplete
- [ ] T105 [US4] Add the capability-verdict and slot-cap pass-down to `skills/external/sdd-loop-driver/SKILL.md` — the driver passes the verdict and the cap to each dispatch and changes no step order (FR-028 c), so a dispatch never inherits the previous one's reading

**Checkpoint**: US4 is independently testable — the 092 reproduction is red before the repair and green after, and the static capability verdict covers every agent definition.

---

## Phase 7: User Story 5 - 并发有效性被真实验收：至少一个真实执行体跑出并发与确定性集成 (Priority: P2)

**Goal**: at least one real, non-fixture run leaves a decidable concurrency reading — units, per-unit verdicts, deterministic integration order, duration and the comparison with the serial baseline.

**Independent Test**: `tests/contract/test_concurrency_real_run_evidence.py` passes on a real run's coordination report whose effective value is `>= 2` and whose per-unit verdicts exist; it fails on a report that claims concurrency without intervals or that writes `0` for a missing quantity.

### Tests for User Story 5 (MANDATORY) ⚠️

- [ ] T106 [US5] Author the real-run evidence contract in `tests/contract/test_concurrency_real_run_evidence.py` — a coordination report is accepted only with effective `>= 2` on a non-fixture run, per-unit verdicts, the deterministic integration order, the duration and the 091 baseline comparison; a missing quantity must read `not_evaluated`, and a report claiming concurrency without intervals is red
- [ ] T107 [US5] Author the exit-code disposition contract in `tests/contract/test_concurrency_disposal.py` — `owner-unavailable` and `inconsistency` are distinguishable by exit code alone, so the engine's non-convention reading of the framework rule is asserted rather than assumed
- [ ] T108 [US5] Author the fabricated-number and cost-benefit mutation in `test-evidence/` — replace a missing quantity with `0` and then with an estimate (both must turn the contract red), and record the fixture's concurrent-vs-serial result-set identity

### Implementation for User Story 5

- [ ] T109 [US5] Implement the run-record read in `scripts/python/concurrency-check.py` — the record is parsed through the same block subset as the facts, so a run cannot smuggle a shape the declaration layer would reject
- [ ] T110 [US5] Produce this feature's own coordination report for the implement run and record its reading — if the executor dispatched, the report carries effective `>= 2` with intervals, per-unit verdicts and the integration order; if it did not, it records the not-yet-landed reason code with effective `not_evaluated` and names the missing dispatch capability (never `0`, never an estimate, never a serial run described as concurrent)
- [ ] T111 [US5] Write the 091 serial-baseline comparison row from its existing record — 62 tasks, one agent, 116 minutes, cited from the 091 run record rather than re-measured; a quantity 091 did not produce is marked `not_evaluated`, so the comparison is never filled by inference

**Checkpoint**: US5 is independently testable — a real-run report is either decidable or explicitly `not_evaluated`, and both forms pass the contract while a fabricated number fails.

---

## Phase 8: Polish & Release (Cross-Cutting)

**Purpose**: the high-order executors, the per-stage coverage rule, the disposal table, the unit module, the mirror release and the quickstart verification that make the feature releasable.

- [ ] T112 Implement goal-slice decomposition recording in the coverage fact and the `coverage` action — a goal slice records per stage whether it decomposes, resolved through the fact, and a goal does not declare a target covered until the slice's deliverables exist
- [ ] T113 Implement the goal target partition under the slot cap in `scripts/python/concurrency-check.py` — targets are partitioned into work packages bounded by the cap minus reserve for concurrent goals only [green: contracts/high-order-executors.contract.md#C-063]
- [ ] T114 Require a team member class and a stated concurrency capability in `skills/internal/create-team/SKILL.md` — the team states how many members can run concurrently and is not instantiated above that
- [ ] T115 Judge seat territories at binding time in `skills/internal/create-team/references/conceptual-model.md` — intersecting or undeclared territories are red before any run (V-26; measured 2026-11-09: 2 of 12 team definitions declare no territory) [green: contracts/high-order-executors.contract.md#C-067]
- [ ] T116 Move the team obligation into the stage-team preset rather than into each instantiated team text — the preset carries the obligation and one slot-cap projection line [green: contracts/high-order-executors.contract.md#C-068]
- [ ] T117 Require each loop stage to declare its own decomposition coverage, forbid inheriting the previous stage's, and require the per-unit reading (stage/package for the driver, entry for house-keeping, step for project-setup; never "per round") in `skills/external/sdd-loop-driver/SKILL.md` (FR-028 b) [green: contracts/high-order-executors.contract.md#C-070]
- [ ] T118 Make the per-stage default decomposition explicit in the decomposition model — a stage with concurrent units decomposes by default absent a named decision (FR-029, SM-2) [green: contracts/judgement-engine.contract.md#C-035]
- [ ] T119 Implement the `coverage` action in `scripts/python/concurrency-check.py` — per-stage decision resolved from the coverage fact with a named decision record for a stage that stays serial, and the observed relation between the fact and the three spine keys reported, a fourth source being a failure [green: contracts/judgement-engine.contract.md#C-036]
- [ ] T120 Make the plan stage default-concurrent in `skills/internal/create-plan/SKILL.md` — the plan stage partitions and records its own reading
- [ ] T121 Make the team executor default-concurrent in `skills/internal/run-team/SKILL.md` — seats are units and the reading is recorded [green: contracts/executor-obligations.contract.md#C-046]
- [ ] T122 Carry the obligation into `templates/plan-template.md` and the 29 command surfaces under `templates/commands/*.md` through one authored text referenced by pointer — no repo-specific fact enters a shipped template (FR-031) [green: contracts/executor-obligations.contract.md#C-061] [green: contracts/high-order-executors.contract.md#C-072]
- [ ] T123 Author the disposal table's disposition domain in `tests/contract/test_concurrency_disposal.py` — every pre-existing concurrency statement gets exactly one disposition from the closed set, and each pre-existing statement's disposition is readable [green: contracts/existing-semantics-disposal.contract.md#C-079]
- [ ] T124 Dispose the slot-cap and ceiling owner collapse — the numeric cap lives in the slot fact and nowhere else, the ceiling stays with the existing gate script's declared default, the spine key is recorded as a run-scoped projection of the cap, and every other site becomes a pointer (one disposition, not two values) [green: contracts/existing-semantics-disposal.contract.md#C-082]
- [ ] T125 Assert the ceiling owner in `tests/contract/test_concurrency_disposal.py` — the existing gate script's declared default remains the ceiling owner and no second assignable site exists
- [ ] T126 Assert the spine's slot key is a run-scoped projection of the fact, never a second value, and that the dated-record disposition carries its date and reason [green: contracts/existing-semantics-disposal.contract.md#C-084]
- [ ] T127 Key every new fact's kind from the existing five-member set in `shared/declarations/contract.yaml` — no new kind value — and keep the existing keys unrenamed, adding a new reading rather than re-cutting an old one
- [ ] T128 Assert no existing declaration key was renamed where a new reading was needed — the reading is added rather than re-cut
- [ ] T129 Register each new fact in the same change that adds the file and assert the pair in `tests/contract/test_concurrency_declarations.py` — a file without a registration line is red
- [ ] T130 Edit only the sources and verify the release parity — `sync-mirrors.py --check` against the frozen baseline plus `regen-command-copies.py --check`; no projection hand-edited
- [ ] T131 Regenerate the per-tool command copies instead of hand-editing them, and keep the retired command-template mirror retired — a hand edit to a generated copy is a defect, and no row in this feature revives the retired tree
- [ ] T132 Retain the four concept owners — `shared/definitions/subagent-definitions.md`, `shared/definitions/goal-definitions.md`, `skills/internal/create-team/references/conceptual-model.md` and `skills/external/sdd-loop-driver/references/decomposition-model.md` are rewritten to reach the facts by path rather than restating them (Constitution XIV)
- [ ] T133 Assert that a pointer disposition leaves a resolving path and never a deleted statement — including the stage-team preset's slot sentence, which becomes a pointer while the seat structure stays
- [ ] T134 Dispose the 064 / 070 / 086 / 092 assertions — write-line and worktree assertions retained, gate assertions retained with the ceiling owner recorded, 092's "plan parallelism not delivered" resolved by the reproduction fixture, 086's efficiency criterion left with its owner, and every collision recorded with both paths before implement [green: contracts/existing-semantics-disposal.contract.md#C-092]
- [ ] T135 Keep the goal/target model intact in `shared/definitions/goal-definitions.md` and add only the target-concurrency paragraph — the spec-local temporary goal layer stays owned by the earlier goal/team feature (FR-032)
- [ ] T136 Run the unit module for the engine's own actions — `python3 -m pytest tests/unit/test_concurrency_check_engine.py -q` covers each of the five actions' argument surface, and the cost-benefit measurement asserts an identical result set with lower wall-clock on the fixture (SC-012)
- [ ] T137 Run `quickstart.md` end to end against the live tree and record the real output with teardown in `notes/quickstart-run.md` — S-0 through S-6, each scenario's passer criteria and command list read from that file (pointer, not restated), and implement any artifact a scenario surfaces as unrunnable
- [ ] T138 Repair the `[green:]` semantics in the framework source only (F-093-004 ruling) — word `green-clause-collision` in `scripts/python/validate-tasks.py` (rule block ~L44-46 and the emitted message ~L501-516) to the marker reading ("a claimed clause belongs to one row; a feature MAY claim a strict subset of its contract clauses"), mirror it into the module's `--help` banner, and add `tests/contract/test_validate_tasks_green_semantics.py` that goes red if the message or docstring re-acquires a totality claim, plus a green-partition assertion on this feature's own `tasks.md` (at least one claim, zero double-claimed, zero dangling); the tag's definition stays in `templates/tasks-template.md` (owner named by `glossary.md` 绿点归属), and `.specify/scripts/python/validate-tasks.py` is regenerated by the mirror engine, never hand-edited. In the same owner file, re-point the dead one-line-per-task owner in L110 (and its `.specify/templates/` mirror) from `.specify/templates/commands/tasks.md` — a path that exists in no worktree — to `.specify/skills/internal/create-tasks/SKILL.md` § "One line per task (mechanical-validation contract)" (F-093-015)
- [ ] T139 Make the `analyze` stage default-concurrent in the driver surfaces — `skills/external/sdd-loop-driver/SKILL.md` and `references/dispatch-recipes.md` (§ 本地原生拓扑) state N concurrent SDD Analysis Workers (`agents/sdd-analysis-worker.agent.md`) with a pre-dispatch declared read domain per Worker (file-level; intersection red before dispatch), deterministic consolidation (read-domain order → finding id order; duplicate ids broken by first declaration with a pointer to the suppressed copy), and the requested/effective/effective-reason triple plus `executor_id` / `verifier_id` per Worker (FR-034) [green: contracts/high-order-executors.contract.md#C-093]
- [ ] T140 Revise `skills/external/sdd-loop-driver/references/decomposition-model.md` § 20.1 so `analyze` no longer defaults to `off` — it decomposes by default and resolves N through the `decomposition-coverage.yaml` [[STR-007]] entry authored by T013; feature-level `off` stays the hard opt-out and the precedence rule is recorded (FR-034, FR-029)
- [ ] T141 Author the analyze-wave contract in `tests/contract/test_concurrency_high_order.py` — the analyze default is N >= 2 concurrent Workers, a read-domain intersection is red before dispatch, consolidation is deterministic under reordered return times, the reading triple and executor/verifier ids are required, and a mutation that reverts the default to `off` turns the test red (FR-034, C-093)
- [ ] T142 Rewrite the concurrency mechanism into the local topology surfaces — `references/dispatch-recipes.md` (§ 本地原生拓扑 and the § Recipe 2 usage note) and the matching statements in `SKILL.md` state the fork model: separate `qodercli` child processes through `scripts/stage-runner.sh` (stdin prompt, `--output-format stream-json`, stage sentinel), pool bounded by the runtime `nproc` reading, host-in-process fan-out not counted as concurrency (FR-035) [green: contracts/high-order-executors.contract.md#C-094]
- [ ] T143 Author the fork-mechanism contract in `tests/contract/test_concurrency_high_order.py` — the runner invocation shape (stdin prompt, stream-json, sentinel) is asserted against `stage-runner.sh --help`, the pool bound is read at dispatch (freezing `nproc` into a file turns the test red), and an in-process fan-out record is rejected as the concurrency mechanism (FR-035, C-094)

---

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: no prerequisites. T004/T005 gate every row that reads a fact; T002/T003 gate the comparisons and the counts
- **Foundational (Phase 2)**: T008–T013 block every row that reads one of the eight facts; T014 validates them before anything reads; T015–T020 pin the declaration read behaviour; T021–T025 build the engine interface; T026 opens the phase's red-first record
- **US1 (Phase 3)**: T027–T029 need T008, T009, T037; T030–T033 need T021–T025; T034–T041 need T037
- **US2 (Phase 4)**: the contract rows T042–T050 need the code fact (T010); the implementation rows T051–T065 need the US1 class resolution (T031) and the write-domain shape from US3 (T078)
- **US3 (Phase 5)**: the contract rows T066–T073 need the slot fact (T012) and the unit fields (T011); the implementation rows T074–T085 need the US2 bindings (T057–T061)
- **US4 (Phase 6)**: the contract rows T086–T094 need the engine (T021–T025); the implementation rows T095–T105 need US1's `classify` (T030); T090 (the 092 reproduction fixture) is authored before the capability action (T097) that must turn it green
- **US5 (Phase 7)**: needs US2's reading (T069–T073) and US3's interval computation (T074); T106 is the only row that depends on the runtime host capability probe in § Environment Prerequisites
- **Polish (Phase 8)**: needs US1–US5 closed; T130 is the release gate; T138 lands the F-093-004 rule-text repair with no dependency on the facts, and T139–T143 (FR-034 / FR-035) are gated on T013 (the coverage fact) and T117 / T119 (loop coverage + the coverage action)

### User Story Dependencies

- **US1 (P1)**: independent of every other story
- **US2 (P1)**: consumes US1's class resolution; otherwise independent
- **US3 (P1)**: consumes US2's bindings and the class fact's unit form; otherwise independent
- **US4 (P1)**: consumes the engine and US1's enumeration; **its verdict reading is blocked on the coordinator adjudication** (T098 authors the verdict fact and does not answer it)
- **US5 (P2)**: consumes the US2 and US3 readings; its real-run evidence depends on the *next* run being able to dispatch, which this feature's own implement run may not be — recorded honestly as `not_evaluated`

**MVP scope**: all four P1 stories (US1–US4). The rule is "the smallest same-priority set whose checkpoints are each independently testable"; here authoring the declaration layer (US1) without the judgement (US2/US3) or the capability judgement (US4) would be half a mechanism, so the MVP covers all four P1 stories. US5 is P2 and lands after.

---

## Work Packages (default-concurrent implement plan)

This line's session instruction requires the tasks artifact itself to organize implement as **concurrent packages**. Each package below is a unit of the kind `decomposition-model.md` § 2 defines, carrying that model's fields plus the two this feature adds: `write_domain` at file level (FR-012) and `isolation_form` (FR-013). The model's own rules stay owned by that file; this table carries this run's concrete package set only. Every one of the 143 rows appears in exactly one package.

| Package | User stories | Rows | Declared-order fold | `write_domain` (file level) | `isolation_form` | `blockedBy` |
|---|---|---|---|---|---|---|
| `WP1-facts` | setup + Foundational + the fact rows | T001–T013, T014, T026, T098 | 1 | `shared/declarations/facts/*.yaml` (the eight files), `shared/declarations/contract.yaml`, `.specify/memory/register.md` | worktree | — |
| `WP2-engine` | US1–US5 engine rows | T021–T025, T030–T033, T051–T056, T074–T077, T095–T097, T109, T113, T119, T138 | 2 | `scripts/python/concurrency-check.py`, `scripts/python/validate-tasks.py`, `tests/contract/test_validate_tasks_green_semantics.py` | worktree | WP1 |
| `WP3-owners` | US1/US2/US3/US4/Polish document rows | T037, T041, T060, T061, T078, T100, T114–T115, T120–T122, T132, T135, T139–T140, T142 | 3 | `shared/definitions/subagent-definitions.md`, `shared/definitions/goal-definitions.md`, `skills/internal/create-plan/SKILL.md`, `skills/internal/create-team/SKILL.md`, `skills/internal/create-team/references/conceptual-model.md`, `skills/internal/run-agent/SKILL.md`, `skills/internal/run-team/SKILL.md`, `skills/external/sdd-loop-driver/SKILL.md`, `skills/external/sdd-loop-driver/references/decomposition-model.md`, `skills/external/sdd-loop-driver/references/dispatch-recipes.md`, `skills/external/sdd-loop-driver/templates/stage-team-preset.md`, `skills/external/sdd-loop-driver/scripts/wp-gate.py`, `templates/plan-template.md`, `templates/commands/*.md`, `agents/*.md` | worktree | WP1 |
| `WP4-tests` | every red-first module row | T015–T016, T018, T020, T027, T029, T042, T044, T046–T050, T057, T066–T073, T086–T087, T089, T091, T092, T094, T106–T107, T123, T125, T129, T136, T141, T143 | 4 | `tests/contract/test_concurrency_class_table.py`, `tests/contract/test_concurrency_serial_reason.py`, `tests/contract/test_concurrency_units.py`, `tests/contract/test_concurrency_dispatch_capability.py`, `tests/contract/test_concurrency_high_order.py`, `tests/contract/test_concurrency_declarations.py`, `tests/contract/test_concurrency_disposal.py`, `tests/contract/test_concurrency_reproduction_092.py`, `tests/contract/test_concurrency_real_run_evidence.py`, `tests/unit/test_concurrency_check_engine.py` | worktree | WP1 |
| `WP5-release` | Polish + cross-cutting evidence rows | T017, T019, T028, T034–T036, T038–T040, T043, T045, T058–T059, T062–T065, T079–T085, T088, T090, T093, T099, T101–T105, T108, T110–T112, T116–T118, T124, T126–T128, T130–T131, T133–T134, T137 | 5 | `.specify/specs/093-concurrency-by-default/notes/*`, `.specify/specs/093-concurrency-by-default/test-evidence/*`, `.specify/specs/093-concurrency-by-default/coverage-baseline.txt`, `.specify/specs/093-concurrency-by-default/verification.md` | worktree | WP1, WP2, WP3, WP4 |

**Why this partition is genuinely parallel**: the three edges that matter are `WP1 → WP2` (the engine reads the facts), `WP1 → WP4` (the tests pin the fact slugs and clause ids), and `WP2/WP3/WP4 → WP5` (release). `WP2` writes only `scripts/python/concurrency-check.py`, `WP3` writes only documents and agent definitions, `WP4` writes only `tests/`, `WP5` writes only evidence files. Their file-level write domains are pairwise disjoint, so `WP2`, `WP3` and `WP4` are **ready together** once `WP1` closes — three concurrent units at a cap measured at dispatch time (never copied: the value is owned by `shared/declarations/facts/concurrency-slot-and-reserve.yaml`, the ceiling by the existing gate script).

**Package size**: 143 rows over 5 packages, above the ~10 rows/package guidance. The package boundary here is the **write domain**, not the row count: splitting further would put two packages on the same file and reintroduce exactly the write conflict FR-012 forbids at directory level. Recorded as a deliberate deviation, not an oversight.

**Concurrency conditions at dispatch** (FR-005): (a) ready packages `>= 2` — yes, three after WP1; (b) no unsatisfied dependency edge among them — yes; (c) file-level write domains pairwise disjoint — yes by the table above; (d) host parallel dispatch capability — **the open condition**, probed at dispatch and recorded per § Environment Prerequisites; (e) `min(slot_cap, ceiling, remaining) - verifier_reserve >= 2` — measured at dispatch, never asserted.

**SC-006 evidence plan for this line (the real-concurrency proof)**:

- The table above **is** the partition. An executor that can dispatch launches `WP2`, `WP3` and `WP4` in one round as three sibling executors — under FR-035, three separate `qodercli` child processes through `stage-runner.sh`, each in its own worktree write line, with the integration order fixed by the declared-order fold (`WP2 → WP3 → WP4 → WP5`) regardless of which returns first.
- With the fork mechanism in place, T106 records requested `= 3`, effective `=` the maximum interval overlap of the three units' dispatch/settle intervals, per-unit verdicts from three distinct verifier ids, the integration order, the duration and the serial-baseline comparison — that is SC-006 satisfied on a real run. T105 authors the run record, T107 supplies the baseline row.
- **Measured today (2026-11-09, this worktree)**: the executing body **holds a host dispatch tool** — the earlier "no Agent/Task tool" reading was wrong (corrected at analyze 2026-11-09, F-093-012). The planning stages nonetheless ran serial, one executor, and their own record is effective `not_evaluated` with the not-yet-landed reason code: what is missing is the feature's own mechanism — the facts, the engine, and the FR-035 fork runner path (T142) — not a host tool. The gap is named here rather than discovered at implement: **if the implement executor runs serially, SC-006 MUST be recorded `not_evaluated` — not `0`, not an estimate, not "concurrency proven by fixtures" — and the gap is the missing mechanism, not missing work.** The 092 lesson is that this disclosure *is* the deliverable.

---

## Parallel Example: closing WP1 and opening WP2 / WP3 / WP4

```text
# after WP1 (declaration facts + registration) is closed, in ONE dispatch round:
Executor A (WP2): scripts/python/concurrency-check.py — classify / serial-reason / reading / coverage / capability
Executor B (WP3): agents/*.md, skills/**, shared/definitions/**, templates/** — obligation text and pointers
Executor C (WP4): tests/contract/test_concurrency_*.py — red-first modules, each pinned to a clause id
# integration: serial queue in declared-order fold WP2 -> WP3 -> WP4 -> WP5, never return order
```

---

## Implementation Strategy

### MVP First

US1–US4 (all P1) close together: the closed set, the default-plus-reason judgement, the seven unit obligations, and the dispatch-capability judgement. Validate each story's checkpoint independently, then US5's real-run evidence and Phase 8's release rows.

### Incremental Delivery

1. Setup + Foundational → the declaration layer and the engine interface exist and are testable
2. US1 → a body added without a class goes red (the closed set is real)
3. US2 → the serial path cannot pass without a code
4. US3 → the unit obligations judge real records
5. US4 → the 092 shape is red before the repair and green after
6. US5 → a real run's reading is decidable or explicitly `not_evaluated`
7. Polish → high-order executors, coverage, disposal, mirrors, quickstart

### Parallel Team Strategy

With a dispatching team: one executor per package `WP2` / `WP3` / `WP4` after `WP1`, `WP5` serial at the end, one verifier reserved out of the slot budget. Without dispatch capability: one executor in declared-order fold, and the honest record is serial with the not-yet-landed reason code.

---

## Notes

- [P] rows write different files from every other [P] row in their phase — verified against the `write_domain` column above, not only against the prose
- `[green: <contract>#<clause>]` is a **red-first marker**, not a clause-registration table: it marks the row that first turns a module or a fact file green, it appears at most once per (module path, clause) pair, and no two rows carrying it write the same test module. The full clause→row delivery map is `feature-ref.md` § FR→clause delivery map
- `agents/*.md` edits are gated on T098's verdict only in so far as the verdict changes what the file must say; the verdict itself is read from its owner and is never decided in this file
- `templates/commands/*.md` stay project-neutral: the obligation text reaches its owner by path, so no repo-specific fact enters a shipped template
- Deferral discipline: prefer `[~]` with a recorded reason over leaving a row `[ ]`; SC-006's real-run evidence is the one item that may legitimately land `not_evaluated` rather than deferred, because its premise (a dispatching executor) is a runtime fact, not missing work
- The eight facts, the engine and the ten test modules do not exist yet, so every path carrying one of them is a **creation target**, not a dangling reference — that is why `pre-analyze-check.py` reports them as advisories

### Validator adjudication (re-run and filled on each run)

- **Run of 2026-11-09 (this stage)**: `validate-tasks.py` → `PASS — 0 error(s), 0 warning(s)`; the captured output is `test-evidence/validate-tasks.txt`. Preceding runs started at 2 ERROR + 277 WARN and were driven to zero by renumbering, not by deleting tags.
- **Run of 2026-11-09 (analyze-repair)**: `validate-tasks.py` → `PASS — 0 error(s), 0 warning(s)` over 143 rows; the captured output is `test-evidence/analyze-repair-validate-tasks.txt`. Six rows were added in this pass — T138 (the F-093-004 rule-text repair) and T139–T143 (the two dated user rulings, FR-034 / FR-035); the two new clauses C-093 / C-094 are claimed once each (T139 / T142), and DoD-1's hand count was replaced by this validator's own verdict (F-093-017).
- WARN `parallel-safe`: every `[P]` row now writes a file no other `[P]` row in the same phase writes; the remaining rows share module paths inside a phase and therefore carry no `[P]`.
- WARN `green-clause-collision` / `green-cross-phase`: a clause is claimed at most once, and within each contract file the clause ordinals ascend against row order. The rows that carried a second claim were the ones whose work was already marked by an earlier row; they now carry no tag and keep their red-first evidence in their own step.
- WARN `green-path-divergence`: each of the ten test modules is marked green by exactly one row; the other rows that write that module are refinements, not the turning point.
- The two runs that a later stage must repeat are `python3 .specify/scripts/python/validate-tasks.py .specify/specs/093-concurrency-by-default/tasks.md` (expect exit 0) and `python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/093-concurrency-by-default/requirements.md --tasks .specify/specs/093-concurrency-by-default/tasks.md` — both are wired into GATE-6.

