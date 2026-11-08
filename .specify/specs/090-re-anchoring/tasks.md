# Tasks: Re-Anchoring（不忘初心 · 温故而知新）

**Requirement ID**: 090
**Requirement Key**: 090-re-anchoring
**Related Feature**: 090 Re-Anchoring（不忘初心 · 温故而知新）
**Input**: Design documents from `.specify/specs/090-re-anchoring/`
**Prerequisites**: requirements.md (10 FR / 4 SC, clarify settled 2026-11-09), plan.md (T-001/T-002, EP-001…EP-004, D-1…D-6), research.md (R1…R9), data-model.md (E-1…E-6 / V-1…V-12), contracts/ (re-anchoring-faces C-1…C-8, direction-audit C-1…C-9, governance-landing C-1…C-6, guard-tests C-1…C-8), quickstart.md (S-0…S-6), feature-ref.md

**Tests Mode**: ON — Constitution Principle IV "Test-First & Contract-Driven Implementation" is test-mandating, and this feature's whole verification surface is contract guards over governance artifacts (Constitution Check row IV is the one Partial row, carried by `guard-tests.contract.md` C-7 with a red-first obligation). Every guard row lands BEFORE the implementation row that turns it green; verification rows that only read an existing guard sit AFTER it and carry `[blockedBy:]`.

**Tests**: MANDATORY for the guard rows. Red-first captures and guard-run evidence land in `test-evidence/`; the mutated-copy fixtures live under `test-evidence/tmp/` (directory governance: the evidence dir already exists, so no new top-level directory is created).

**Organization**: this feature is **verification-shaped, not build-shaped**. The implementation is pre-landed (commits `5a1041e4`, `55776937`, reconciled as `137adb7f`); `plan.md` § Summary states this plan's job is to *describe and anchor the tree that exists, measure it, and hand `/speckit.tasks` a work list whose deliverables are the still-missing guards and the closure evidence — not a re-implementation*. `requirements.md` carries **no user stories**, so the phases below are grouped by the four success criteria plus a Setup and a Polish phase; no `[US*]` label is emitted, which is what the structural validator's story-label rule requires for non-story phases.

**Assumption recorded at generation (interview ruling, no user turn)**: the SC grouping in § Phase Map is this stage's own organization choice, because `requirements.md` declares no stories and `plan.md` names no story slicing. Recorded here per the run's "interview-style question ruled by the agent, assumption recorded in tasks.md" instruction.

## Phase Map

| Phase | Purpose | Rows | Success criterion |
|-------|---------|------|-------------------|
| 1 Setup | freeze the baselines the closure rows compare against | T001–T005 | all |
| 2 SC-001 | five owner-facing rule faces exist and point at one owner | T006–T013 | SC-001 |
| 3 SC-002 | the rule-first ordering gap (`guard-tests.contract.md` C-7 OPEN) is closed red-first | T014–T021 | SC-002 |
| 4 SC-003 | the count pins and their guards agree with the artifacts | T022–T026 | SC-003 |
| 5 SC-004 | the T0/T1/T2 tiers agree across owner page and protocol | T027–T029 | SC-004 |
| 6 Polish | the carried rulings, the FR citation groups, the mirror sweep | T030–T038 | FR-010, closure |

## Definition of Done (DoD)

- DoD-1: Every FR-001…FR-010 is discharged by at least one row naming the artifact it is judged against, and the four contract pages' clause-level citation groups resolve all ten (check: `account-clause-coverage.py` reports zero uncovered FRs).
- DoD-2: Every contract clause of the four pages is claimed exactly once by a `[green:]` tag on a row that names the file it writes: `re-anchoring-faces` C-1…C-8, `direction-audit` C-1…C-9, `governance-landing` C-1…C-6, `guard-tests` C-1…C-8 (31 clauses, 0 collisions, 0 dangling, 0 cross-phase).
- DoD-3: `guard-tests.contract.md` C-7 is closed: one test function asserts the rule-first ordering, reds on all three stated mutations, and the landed-pass / mutated-fail pair is captured in `test-evidence/`.
- DoD-4: The four named guard modules carry zero NEW failures against the frozen baseline — `test_reanchoring_contract.py` 4 passed, `test_sdd_loop_driver_reanchor.py` 5 passed after the new row, `test_constitution_double_landing.py` 19 passed, `test_fast_fail_discipline.py` 104 passed 2 failed (both pre-existing, see § Environment Prerequisites).
- DoD-5: Every mirror obligation of `plan.md` § Mirror Obligations holds — `sync-mirrors.py --check` exits 0 with all six pairs byte-identical, including the protocol pair the ordering guard reads.
- DoD-6: SC-001…SC-004 each carry a `test-evidence/` file whose command and reading were produced in this feature's run, and no `final`-path criterion is left in `blocked` / `deferred` / `fail` without an explicit waiver.
- DoD-7: Every ruling this stage had to make is disclosed in § Notes — never folded silently into green.

**DoD Status**: pending

## Completion Gate

- GATE-1: No NEW failures in the four named guard modules versus the frozen baseline — check: `SPECKIT_PYTHON=/usr/bin/python3 /usr/bin/python3 -m pytest tests/contract/test_reanchoring_contract.py tests/contract/test_sdd_loop_driver_reanchor.py tests/contract/test_constitution_double_landing.py tests/contract/test_fast_fail_discipline.py -q --tb=no -rA` and compare the `FAILED` node ids against `.specify/specs/090-re-anchoring/test-evidence/tasks-baseline-failed.txt` with `LC_ALL=C comm -13` printing nothing.
- GATE-2: The ordering guard reds when the protocol is reverted to goal-first — check: `.specify/specs/090-re-anchoring/test-evidence/ordering-red-control.txt` holds one landed-pass arm and three mutant-fail arms.
- GATE-3: Every mirror obligation from `plan.md` § Mirror Obligations is byte-identical — check: `/usr/bin/python3 scripts/python/sync-mirrors.py --check` exits 0.
- GATE-4: No open task rows — check: `grep -cE '^- \[[ >]\]' .specify/specs/090-re-anchoring/tasks.md` returns 0.
- GATE-5: Every `final`-path success criterion is `pass` **and** the feature's smoke record is present — check: in `.specify/specs/090-re-anchoring/verification.md`, every criterion whose `**Path**` marker reads `final` has `SC-NNN_status=pass`, and `smoke_command=`, `smoke_exit_code=0` and `smoke_evidence_path=` (a path that exists and is non-empty) are all present; a `final`-path criterion in `blocked` / `deferred` / `fail` fails this gate unless an explicit user waiver names that criterion. Condition set owner: `shared/workflow/acceptance-hardening.md` § Gates — this row carries the check, not a second schema.
- GATE-6: Structure and clause accounting are silent — check: `/usr/bin/python3 .specify/scripts/python/validate-tasks.py .specify/specs/090-re-anchoring/tasks.md` exits 0 with zero ERROR, and `/usr/bin/python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/090-re-anchoring` reports zero uncovered clauses and zero uncovered FRs against the frozen baseline.

## Environment Prerequisites

Probed 2026-11-09 in `/cws_data/cloud-native-ai/spec-kit` on `master` (base `6060b3cb`). Every row that depends on one of these verdicts references THIS section; no row restates a verdict. Re-probe at implement entry — never cached across runs.

- `pytest` on the `PATH` `python3`: **unavailable** — probe: `python3 -c 'import pytest'` @ 2026-11-09 → `No module named pytest`; affected: every guard row, which therefore pins `SPECKIT_PYTHON=/usr/bin/python3`.
- `pytest` on `/usr/bin/python3`: **available** (9.0.3) — probe: `/usr/bin/python3 -m pytest --version` @ 2026-11-09; affected: every guard row.
- `contract`-marked collection: **available** — probe: `SPECKIT_PYTHON=/usr/bin/python3 /usr/bin/python3 -m pytest -m contract -q --collect-only` @ 2026-11-09 → `4715/8063 tests collected (3348 deselected) in 2.04s`; affected: the new ordering test's collection and the no-new-failure comparison.
- The four named guard modules on the untouched tree: **green except two** — probe: `pytest <four modules> -q` @ 2026-11-09 → `2 failed, 129 passed in 1.91s`; the two are `test_fast_fail_discipline.py::test_i11_channel_two_mirrors_and_per_tool_copies` and `::test_g9_total_equals_frozen_baseline`, both pre-existing (`plan.md` EP-003, `research.md` R6); affected: every no-new-failure row, so acceptance is "no NEW failure", never "green".
- Mirror parity: **clean** — probe: `/usr/bin/python3 scripts/python/sync-mirrors.py --check` @ 2026-11-09 → exit 0, six pairs byte-identical; affected: the mirror rows.
- Mutation fixture root: **available under the spec, unavailable under the system temp root** — probe: `mount | grep -E ' /tmp '` @ 2026-11-09 (`noexec`) and the sanctioned roots in `shared/guidelines/temp-directory-discipline.md`; affected: every mutation row, whose fixture lives under `test-evidence/tmp/`, never `/tmp` (`quickstart.md` S-6 uses `/var/tmp` for its shell scenario).

**A13 boundary** (owner: `shared/workflow/acceptance-hardening.md` § Gates — this note is a pointer, not a second rule): this section records **task-generation probe verdicts** only, each with its probe command and an ISO date. A planning-time load-bearing premise belongs to `plan.md` § Execution Premises (EP-001…EP-004); the two pre-existing guard failures are cited from `research.md` R6 as the comparison baseline, not re-derived here.

## Format: `[ID] [P?] Description`

- **[P]**: can run in parallel — different write targets, no dependency on an incomplete row of the SAME phase (the structural validator scores `[P]` per phase).
- **[blockedBy: Txxx]**: a real dependency, machine-checkable. Omitted when only phase order applies.
- **[green: <contract>#<clause>]**: this row is the one that turns that clause green. Contract paths resolve relative to this file's own directory first; every row below cites the `contracts/<page>.md` form for that reason. One row per clause: the 31 clauses of the four pages are partitioned across T006–T028, each claimed exactly once.
- One line per row, exact file paths, no wrapped continuations.

### Task State Sigil

`- [ ]` open · `- [>]` claimed (multi-agent only) · `- [X]` closed · `- [~]` deferred with a reason recorded in `verification.md` (`deferred_tasks=`).

## Path Conventions

Framework-source shape (`plan.md` § Structure Decision): sources live in `shared/`, `skills/`, `templates/`, `tests/`; their `.specify/` counterparts are generated by `sync-mirrors.py` and never hand-edited. `.specify/memory/constitution.md` and `.specify/instructions.md` are single copies (live governance file / generated by `scripts/bash/generate-instructions.sh`). All paths below are repo-relative from `/cws_data/cloud-native-ai/spec-kit`.

### Premises measured at generation time (2026-11-09)

Every count below was re-derived this stage with the re-derivation command actually executed; the trap form is named wherever a naive measurement returns a different number.

| Quantity | Measured | Re-derivation | Naive form that disagrees |
|---|---|---|---|
| FR definitions | **10** | `validate-requirements._definitions` over `requirements.md`, fence- and code-span-blind → `FR-001`…`FR-010` | counting `FR-0` anywhere → far more (cross-references); a bare `^- \*\*FR-` grep also matches the clarify prose unless fences are stripped first |
| FR coverage from contract citation groups | **0 of 10 today** | `account-clause-coverage.py --spec-dir .specify/specs/090-re-anchoring --json` → `fr.claimed=0`, `uncovered=['FR-001'…'FR-010']` | reading each page's introduction line as a citation — the owner's rule § 4.2 puts the citation group inside a clause block, and the introduction line is not one |
| Contract clauses in the four pages | **31** (`re-anchoring-faces` 8, `direction-audit` 9, `governance-landing` 6, `guard-tests` 8) | `clause_extract.extract_clauses()` per page; `form_of()` → `md-heading` on all four | `grep -c 'C-'` anywhere over-counts (the pages cross-reference each other's clauses); `grep -c '^## C-'` agrees at 31 today but breaks the moment T023 canonicalises the form |
| Clause universe (whole corpus) | **1908** names from 288 files (181 parsed + 107 named) | the same run's `scanned.total` / `scanned.parsed` / `scanned.named_unparseable` | counting files instead of names under-counts by the collapse (24 duplicate OpenAPI method keys, owner doc § 2) |
| Guard modules this feature names | **4** | `ls tests/contract/test_reanchoring_contract.py tests/contract/test_sdd_loop_driver_reanchor.py tests/contract/test_constitution_double_landing.py tests/contract/test_fast_fail_discipline.py` | counting the two the SC lines name → 2, which is the clarify A5 defect already repaired |
| Guard assertions today | **4 / 4 / 19 / 104 passed, 2 failed** | `pytest <four modules> -q` @ 2026-11-09 → `2 failed, 129 passed in 1.91s` | calling the suite "green" — the two failures are the pre-existing EP-003 entries |
| Ordering assertions in the tree today | **0** | `grep -rnE "primary object is the RULES\|Q1 rules" tests/` → no hit outside the presence assertions; `test_sdd_loop_driver_reanchor.py` holds 4 tests, none ordering | `grep -rn "Q1" tests/` → hits in `tests/unit/test_measure_unit.py` and humanize fixtures, all unrelated quarter labels |
| Constitution principles | template **21** (`XXI`), live **22** (`XXII`) | `grep -cE '^### [IVXLC]+\. ' templates/constitution-template.md` → 21; `.specify/memory/constitution.md` → 22 | forcing the numerals equal (clarify A2: the live roster carries 13 project-specific principles the template does not) |
| Count pins | `TEMPLATE_COUNT = 21`, `LIVE_COUNT = 22`, `COMMAND_COUNT = 14`, watchlist **9** | `grep -nE '^(TEMPLATE_COUNT\|LIVE_COUNT\|COMMAND_COUNT) = ' tests/contract/test_constitution_double_landing.py`; watchlist last entry `"Re-Anchoring (不忘初心 · 温故而知新)"` | reading the pins' `# stale-pin update` comments as the authority instead of the artifact counts above |
| Instructions size vs budget | live **35 790 B** vs `INSTRUCTIONS_BUDGET_BYTES=37888` → **2 098 B** headroom | `wc -c .specify/instructions.md`; `grep -n INSTRUCTIONS_BUDGET_BYTES scripts/bash/generate-instructions.sh` → line 100 | the 33 357 B / 34 816 figures in `feature-ref.md` F-5-era text predate the 089 and 090 raises; the 090 raise is commit `f234de7d` |
| Owner page size | **63** lines, tier table at :39–:45 | `wc -l shared/definitions/re-anchoring-definitions.md` | `wc -c` → bytes, not lines, and the page is UTF-8 with CJK, so the two numbers are unrelated |
| Mirror pairs this feature owns | **6** identity pairs, all byte-equal | `/usr/bin/python3 scripts/python/sync-mirrors.py --check` → exit 0 | `diff -r` on the *directories* reports every deliberately unmirrored file as a difference |
| Sibling coverage baselines | **25** of 26 spec dirs carried `coverage-baseline.txt` before this stage (26 now that this stage froze 090's own) | `ls .specify/specs/*/coverage-baseline.txt \| wc -l` → 26 after the freeze, 25 before it | treating an absent baseline as an empty exemption list — the accountant reports `baseline-missing` explicitly and so does this feature (see § Notes F-6) |

---

## Phase 1: Setup (Shared Infrastructure)


---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: freeze the three baselines the closure rows are compared against and land the evidence landing points. Nothing here writes an artifact this feature is judged on.

- [ ] T001 Create the evidence landing points for this stage and record the generation-time premises of § Premises measured at generation time in `.specify/specs/090-re-anchoring/test-evidence/tasks-premises.md`
- [ ] T002 Capture the four named guard modules' pre-change node-id baseline into `.specify/specs/090-re-anchoring/test-evidence/tasks-baseline-failed.txt` with `/usr/bin/python3 -m pytest <the four modules> -q --tb=no -rA`, recording the exit code and the two pre-existing failures [blockedBy: T001]
- [ ] T003 Capture the contract-suite collection reading into `.specify/specs/090-re-anchoring/test-evidence/tasks-collect.txt` with `/usr/bin/python3 -m pytest -m contract -q --collect-only` [blockedBy: T001]
- [ ] T004 Capture the six-pair mirror baseline into `.specify/specs/090-re-anchoring/test-evidence/mirrors-tasks.txt` with `/usr/bin/python3 scripts/python/sync-mirrors.py --check`, which must read exit 0 with six `ok` lines [blockedBy: T001]
- [ ] T005 Create the mutation-fixture root `.specify/specs/090-re-anchoring/test-evidence/tmp/.gitkeep` and assert the resolved path stays inside the sanctioned evidence dir, never under the system temp root (see § Environment Prerequisites) [blockedBy: T001]

**Checkpoint**: every closure row can name the baseline it is compared against, and the mutation root is proven writable on this host.

---

## Phase 2: SC-001 — the five rule faces exist and point at one owner

**Goal**: the owner page plus the five consumer faces (two constitutions, two instruction surfaces, one agent obligation) and the generator mandate entry simultaneously exist and cross-reference by pointer.
**Independent Test**: `pytest tests/contract/test_reanchoring_contract.py -q` → 4 passed on the landed tree, and each consumer's pointer resolves to the owner page's declared ownership.

- [ ] T006 [SC-001] Verify the owner page `shared/definitions/re-anchoring-definitions.md` owns exactly the concept definitions, the reload tiers and the agent obligation, delegates the executable procedure to `skills/external/sdd-loop-driver/references/checkpoint-protocol.md` by path without restating it, and defines no store, ledger, score or schedule [green: contracts/re-anchoring-faces.contract.md#C-1]
- [ ] T007 [SC-001] Verify the owner page `shared/definitions/re-anchoring-definitions.md` carries the two concepts, the rule anchor, the three tiers and the three verdict literals, recording path plus line anchors in `.specify/specs/090-re-anchoring/test-evidence/sc001-faces.txt` [blockedBy: T006] [green: contracts/re-anchoring-faces.contract.md#C-2]
- [ ] T008 [SC-001] Verify both constitution surfaces carry the principle under one title with the permitted numeral difference and none of the other consumer obligations, appending path and line to `test-evidence/sc001-faces.txt` [green: contracts/re-anchoring-faces.contract.md#C-3]
- [ ] T009 [SC-001] Verify both instruction surfaces carry the ambient section and the owner pointer, with the live file produced from the template by `scripts/bash/generate-instructions.sh`, appending path and line to `test-evidence/sc001-faces.txt` [green: contracts/re-anchoring-faces.contract.md#C-4]
- [ ] T010 [SC-001] Verify the agent obligation section in `shared/definitions/agent-definitions.md` names the owner page, states the entry-restatement duty and the after-each-core-step rules-first duty, and states that the dispatcher carries the anchor summary into the brief, appending path and line to `test-evidence/sc001-faces.txt` [green: contracts/re-anchoring-faces.contract.md#C-5]
- [ ] T011 [SC-001] Verify `skills/internal/manage-constitution/SKILL.md` carries the principle as a sub-entry inside its MUST include block with the owner pointer, appending path and line to `test-evidence/sc001-faces.txt` [green: contracts/re-anchoring-faces.contract.md#C-6]
- [ ] T012 [SC-001] Verify every consumer face named by T008…T011 points at the owner instead of restating its tier table or question list, appending the per-face judgment to `test-evidence/sc001-faces.txt` [blockedBy: T008,T009,T010,T011] [green: contracts/re-anchoring-faces.contract.md#C-7]

**Checkpoint**: each of the four face-guard assertions is attributed to a landed face, and no consumer restates the owner's content.

---

## Phase 3: SC-002 — the rule-first ordering gap closed red-first (guard-tests C-7)

**Goal**: one test function in `tests/contract/test_sdd_loop_driver_reanchor.py` asserts that the audit asks the RULES first and states the rule verdict before any goal restatement, and reds when the protocol is reverted to goal-first.
**Independent Test**: on the landed protocol the new test passes; on the `Q1`-reworded copy, on the minimal-shape reword and on the primary-object-reworded copy it fails — four arms in one captured evidence file.

- [ ] T013 [SC-002] Record the red-first capture into `.specify/specs/090-re-anchoring/test-evidence/red-first-090-c7.txt`: run the four named modules before any edit and record the reading proving no ordering assertion exists today (the modal module holds 4 tests, none ordering) [blockedBy: T002] [green: contracts/re-anchoring-faces.contract.md#C-8]
- [ ] T014 [SC-002] Add the ordering guard to `tests/contract/test_sdd_loop_driver_reanchor.py` as exactly one test function asserting, inside the protocol's direction-audit block, that the rules-first statement is present, that the first of the five questions asks which rules govern the step, and that in the minimal shape the first question line is the rules line, so a goal-first rewrite fails on all three legs, and stating that the rule verdict precedes the goal restatement with the goal implicit in the third question [blockedBy: T013] [green: contracts/guard-tests.contract.md#C-1] [green: contracts/guard-tests.contract.md#C-2] [green: contracts/guard-tests.contract.md#C-3] [green: contracts/guard-tests.contract.md#C-4] [green: contracts/direction-audit.contract.md#C-1] [green: contracts/direction-audit.contract.md#C-2] [green: contracts/direction-audit.contract.md#C-3] [green: contracts/direction-audit.contract.md#C-4] [green: contracts/direction-audit.contract.md#C-5]
- [ ] T015 [SC-002] Confirm the four pre-existing tests of `tests/contract/test_sdd_loop_driver_reanchor.py` carry only structural assertions and that the face guard carries only presence and pointer assertions, so no green of either is read as ordering evidence [blockedBy: T014]
- [ ] T016 [SC-002] Mutate a copy under `.specify/specs/090-re-anchoring/test-evidence/tmp/` by replacing `1. Which rules govern this step` with `1. Which goal governs this step`, run the module against the copy, assert the new test FAILS, and record raw output in `.specify/specs/090-re-anchoring/test-evidence/ordering-red-control.txt` [blockedBy: T014]
- [ ] T017 [SC-002] Mutate a second copy by replacing the minimal shape's first question label with a goal label, run the module, assert the new test FAILS, and append raw output to `test-evidence/ordering-red-control.txt` [blockedBy: T016]
- [ ] T018 [SC-002] Mutate a third copy by rewording the primary-object sentence to name the goal instead of the rules, run the module, assert the new test FAILS, and append raw output to `test-evidence/ordering-red-control.txt` [blockedBy: T017]
- [ ] T019 [SC-002] Verify the landed checkpoint protocol against its audit contract — mandatory fifth part plus the protocol's own defect rule, the first question naming the eight rules inline, exactly three verdict values with only the surfaced one surfaced, the primary-object statement giving the rules as the audit object with its reason, the no-question-to-the-user prohibition mirrored in the driver Hard Requirements block, the tier triggers with the full-reload ban and its reason — recording path and line numbers in `test-evidence/sc004-tiers.txt`
- [ ] T020 [SC-002] Verify the ordering proposition end to end and record the landed-versus-mutated pair as SC-002's evidence in `.specify/specs/090-re-anchoring/test-evidence/sc002-ordering.txt`, citing the four arms and the self-falsifying premise that both former greens still pass on a goal-first rewrite [blockedBy: T016,T017,T018] [green: contracts/direction-audit.contract.md#C-6] [green: contracts/direction-audit.contract.md#C-7] [green: contracts/direction-audit.contract.md#C-8] [green: contracts/direction-audit.contract.md#C-9]
- [ ] T021 [SC-002] Record the red-when-broken obligation for every clause the guard suite asserts — deleted surface, renamed title, dropped part, mutated order — in `.specify/specs/090-re-anchoring/test-evidence/guard-red-controls.txt`, naming the demonstrated failure mode per clause [blockedBy: T016]

**Checkpoint**: SC-002 is satisfiable from the tree alone — the ordering assertion exists, its red control is captured, and no green cited for it predates it.

---

## Phase 4: SC-003 — the count pins and their guards agree with the artifacts

**Goal**: the double-landing pins (21 / 22 / 14), the nine-entry watchlist and the fast-fail guard's entry-length pin agree with the counts the guard derives independently.
**Independent Test**: `pytest tests/contract/test_constitution_double_landing.py -q` → 19 passed, and the fast-fail watchlist guard reports 9 entries with the newest one a template title.

- [ ] T022 [SC-003] Verify the one-title landing on both constitution surfaces, the Sync Impact Report naming the amendment with its version change and Last Amended date, and that no dated record or past checkpoint was rewritten, recording paths and line numbers in `.specify/specs/090-re-anchoring/test-evidence/sc003-counts.txt` [green: contracts/governance-landing.contract.md#C-1] [green: contracts/governance-landing.contract.md#C-2]
- [ ] T023 [SC-003] Verify `skills/internal/manage-constitution/SKILL.md` gained exactly one mandate sub-entry for the principle, appending the block reading to `test-evidence/sc003-counts.txt` [blockedBy: T022] [green: contracts/governance-landing.contract.md#C-3]
- [ ] T024 [SC-003] Verify the three count pins and the watchlist entry against the artifacts they describe — template principles, live principles, mandate entries, watchlist last entry equal to the template title — recording both the literal and the derived reading in `test-evidence/sc003-counts.txt` [blockedBy: T023] [green: contracts/governance-landing.contract.md#C-4]
- [ ] T025 [SC-003] Verify the fast-fail guard pins the watchlist length at its new value and asserts the newest entry is a template title, appending the reading to `test-evidence/sc003-counts.txt` [blockedBy: T024] [green: contracts/governance-landing.contract.md#C-5]
- [ ] T026 [SC-003] Verify the incident the discipline answers is cited rather than rewritten on both the owner page and the protocol, appending the citation readings to `test-evidence/sc003-counts.txt` [blockedBy: T025] [green: contracts/governance-landing.contract.md#C-6]

**Checkpoint**: SC-003 is decidable by two independent measurements that agree, and neither is a restatement of the other.

---

## Phase 5: SC-004 — the reload tiers agree across the owner page and the protocol

**Goal**: the three reload tiers carry the same triggers and the same cost shape in the owner page and in the protocol, and the anchor they load carries both halves.
**Independent Test**: the tiers-bounded guard passes and the two documents' tier rows agree when read against each other line by line.

- [ ] T027 [SC-004] Verify the tier agreement by reading the owner page's tier table against the protocol's tier bullet, recording both sides' paths and line numbers plus any legitimate asymmetry in `.specify/specs/090-re-anchoring/test-evidence/sc004-tiers.txt` [blockedBy: T019]
- [ ] T028 [SC-004] Verify the anchor carries both halves and is persisted in the spine or the brief, never conversation-only, recording the carrier for each half in `test-evidence/sc004-tiers.txt` [blockedBy: T027]
- [ ] T029 [SC-004] Verify the four-kind core-step set is closed and that the tier is chosen by position rather than preference, appending the reading to `test-evidence/sc004-tiers.txt` [blockedBy: T028]

**Checkpoint**: SC-004 holds in both directions — neither side adds a tier the other lacks.

---

## Phase 6: Polish — the carried rulings and the closure ledger

**Purpose**: give the rulings the plan carried an explicit outcome, land the FR citation groups and the canonical clause form, and run the closure sweep.

- [ ] T030 Verify the assertions themselves are falsifiable as a set: re-run the four named modules, inject each clause's failure mode in a scratch copy, and assert the corresponding assertion reds, appending the per-clause arm to `.specify/specs/090-re-anchoring/test-evidence/guard-red-controls.txt` [blockedBy: T021]
- [ ] T031 Verify the four guard modules are pure reads — no subprocess, no write, no network — by reading each module's imports and calls, appending the reading to `test-evidence/guard-red-controls.txt` [blockedBy: T030] [green: contracts/guard-tests.contract.md#C-5]
- [ ] T032 Add the FR-001…FR-010 citation group to the clause blocks of `contracts/re-anchoring-faces.contract.md`, `contracts/direction-audit.contract.md`, `contracts/governance-landing.contract.md` and `contracts/guard-tests.contract.md` so every FR is cited from a clause-level group (owner: `shared/definitions/contract-clause-definitions.md` § 4.2), then re-run the accountant and record the uncovered-FR count [blockedBy: T012,T020,T026,T029] [green: contracts/guard-tests.contract.md#C-6]
- [ ] T033 Convert the four contract pages' clause markers from the legacy heading form to the owner's canonical single-line form, asserting each page's extracted id set is unchanged before and after [blockedBy: T032] [green: contracts/guard-tests.contract.md#C-7]
- [ ] T034 Freeze the coverage baseline by running `account-clause-coverage.py .specify/specs/090-re-anchoring --freeze` into `.specify/specs/090-re-anchoring/coverage-baseline.txt`, recording in § Notes that the freeze corpus and the live corpus differ (F-6) [blockedBy: T033]
- [ ] T035 Re-run the accountant live against the frozen baseline and record the reading, the residual uncovered count and its cause in `.specify/specs/090-re-anchoring/test-evidence/account-clause-coverage.txt` [blockedBy: T034]
- [ ] T036 Re-run the four named guard modules and diff the failed node ids against `test-evidence/tasks-baseline-failed.txt`, recording no-new-failure or the delta in `.specify/specs/090-re-anchoring/test-evidence/closure-guards.txt` [green: contracts/guard-tests.contract.md#C-8] [blockedBy: T014,T024]
- [ ] T037 Re-run `/usr/bin/python3 scripts/python/sync-mirrors.py --check` after every edit of this stage and record the six-pair reading in `test-evidence/mirrors-tasks.txt`, treating new drift on those six pairs as a failure of this stage rather than of the tree [blockedBy: T036]
- [ ] T038 Re-author `shared/definitions/re-anchoring-definitions.md` only if a row above measured a divergence from its own contract, and re-project the mirror with `sync-mirrors.py`; if no divergence is measured this row closes as a no-op citing that reading [blockedBy: T037]

**Checkpoint**: every carried ruling has an explicit outcome, the clause accounting is green against a frozen baseline, and the mirror pairs are byte-identical after the full sweep.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: no dependencies; T001 first, then T002…T005.
- **SC-001 … SC-004 (Phases 2–5)**: all depend on Setup. They are subject-disjoint but not fully parallel: Phases 3 and 5 chain on measurement, and Phases 2, 4, 5 all append to their own evidence file, so each phase is internally serial and the phases themselves may be dispatched as separate packages.
- **Polish (Phase 6)**: depends on every phase above, because it re-verifies their clauses as one falsifiable set; T032 → T033 → T034 → T035 and T036 → T037 → T038 are each a chain.

### Row Dependencies (machine-checkable)

- T002, T003, T004, T005 ← T001
- T007 ← T006; T012 ← T008, T009, T010, T011
- T013 ← T002; T014 ← T013; T015 ← T014; T016 ← T014; T017 ← T016; T018 ← T017; T020 ← T016, T017, T018; T021 ← T016
- T019 has no in-phase blocker: it reads the landed protocol, and T027 depends on it
- T023 ← T022; T024 ← T023; T025 ← T024; T026 ← T025
- T027 ← T019; T028 ← T027; T029 ← T028
- T030 ← T021; T031 ← T030; T032 ← T012, T020, T026, T029; T033 ← T032; T034 ← T033; T035 ← T034; T036 ← T014, T024; T037 ← T036; T038 ← T037

### Parallel Opportunities

- No `[P]` marker is emitted anywhere in this file, deliberately: every phase's rows append to ONE evidence file per success criterion, so no two rows in a phase have different write targets. The parallel unit is therefore the phase, not the row — Phase 2 (faces) and Phase 4 (counts) are subject-disjoint and may be dispatched as two packages under `stage_seats.tasks.max_parallel: 2`, provided the one verifier reserve is kept.
- The mechanism that would have admitted `[P]` is worth naming for the implement stage: one `--junitxml` artifact per row would give each row a distinct target; it is not adopted here because the spec asks for one measured evidence file per criterion, and a split file set is a weaker reading of that.
- WARN class deliberately not suppressed: the structural validator's `parallel-safe` heuristic reads an interpreter path in two rows as a shared write target. No `[P]` marker exists in this file, so the class cannot fire; the cited paths were never removed to make it quiet.

---

## Implementation Strategy

### MVP First

**MVP scope rule** (owner: `.specify/templates/tasks-template.md` § Implementation Strategy): the MVP is the smallest same-priority set whose checkpoint is independently testable. Here the priority set is a single one — **Phase 3, SC-002**. It is the feature's only real gap: the other three criteria are already green over a landed tree, while SC-002's ordering clause has no guard at all. A run that lands nothing else but leaves the ordering assertion red-first-captured has closed the one proposition the feature exists to make falsifiable.

1. Complete Phase 1 (baselines frozen).
2. Complete Phase 3 (T013 → T021): red-first capture, the one ordering test, three mutants, the four-arm evidence pair.
3. **STOP and VALIDATE**: re-run the modal module on the landed tree (must pass) and on each mutant (must fail).
4. Then Phases 2, 4, 5 (independent verification), then Polish.

### Incremental Delivery

1. Baselines + MVP (Phases 1 and 3) → SC-002 satisfiable.
2. Phases 2, 4, 5 → SC-001 / SC-003 / SC-004 each carry their own measured evidence file.
3. Polish → the red-control set, FR citation groups, canonical clause form, frozen baseline, closure sweep, mirror parity.

---

## Notes

- **F-6 (baseline algorithm conflict, disclosed, not repaired here)**: the accountant's `--freeze` documents that it PRINTS a baseline over the corpus **excluding** the target spec, while the live run judges the feature's own clauses against that baseline. Measured this stage: the live run reports `baseline-missing` and, with a freeze written as documented, this feature's own 31 clauses would land in the live delta as uncovered. T034 records the freeze as the 25 sibling specs do; T035 records the residual so the discrepancy is measured rather than hidden. Resolving it touches a shared engine, which is outside this feature's clauses, so it is named here rather than patched.
- **F-7 / F-8 (contract-form defects found this stage)**: (a) each contract page opens with an introduction line naming the FRs and the SC; under the owner's § 4.2 that is a *mention*, because it sits outside every clause block, so the page-level FR coverage reads 0 of 10 even though the FR-to-contract map in `feature-ref.md` § 3 is complete — T032 lands the clause-level citation groups that fix the machine reading. (b) The four pages use the legacy heading form, whose body boundary stops a block at the next section heading, so text placed under a sub-heading inside a clause is silently excluded from that clause's body — T033 converts them to the canonical single-line form and asserts each page's id set is unchanged.
- **Pre-existing red set (carried from `plan.md` EP-003)**: the repo-wide contract suite is red before this feature touches anything (49 failed, 6368 passed, 2 skipped at plan time; measured this stage as 2 failed, 129 passed over the four named modules). Acceptance is **no NEW failure against the measured baseline**, never "the suite is green".
- **089's pre-existing contract failures are not attributable to this stage**: `scripts/python/sync-mirrors.py`, `scripts/python/clause_extract.py` and `scripts/python/validate-requirements.py` are the three engines T032–T035 consume, and all three are already committed with no working-tree modification (measured this stage). `tests/contract/test_script_interface_contract.py` still reports violations for two of them — that is Feature 089's surface, outside this feature's territory, recorded here so a later reader does not attribute it to 090.
- **Interview-style rulings recorded** (unattended run, no user turn): (1) the phase grouping follows the four success criteria because `requirements.md` declares no user stories, and the `[SC-00N]` label records that mapping; (2) every `[green:]` tag cites the `contracts/<page>.md` form so it resolves relative to this file's own directory first; (3) clause partitions inside each contract page follow the page's own clause order, so `green-cross-phase` never fires for this file; (4) two further mutants (T017, T018) are added beyond the single mutation the open clause names, because two of its sibling clauses are otherwise documented propositions only, and the clarify tightening asks for a falsifiable pair; (5) `guard-tests.contract.md` C-5 is claimed by the row that re-measures the modules' purity (T031) rather than by the ordering row, because that clause is about what the face guard does NOT assert, and asserting its absence is a measurement, not a landing.
- **Clause partition (the file's own rule, and how it was reached)**: each page's clauses are claimed by rows that run in the page's own clause order (C-1 first, C-n last), never backwards, and no clause is claimed twice. Where a page's clause order conflicted with a natural row order, the row was re-cut rather than the tag dropped: the modal test file is claimed by exactly one row (T014 owns the four guard clauses and the five direction-audit clauses it lands), and the descriptive clauses follow on their own evidence rows. `validate-tasks.py` reports 0 errors and 0 warnings on this file.
- **Scope boundary**: this stage produced `tasks.md` and its coverage baseline only. No framework source, test, contract or governance file is edited here; every edit above is an implement-stage row.
- **Deferral discipline**: prefer `[~]` over leaving a row `[ ]` "for now" — `[~]` is a deliberate handoff with a reason recorded in `verification.md`; `[ ]` blocks completion.
