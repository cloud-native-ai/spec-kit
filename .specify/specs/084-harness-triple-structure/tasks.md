# Tasks: Harness 三重结构（markdown + yaml + script）

**Requirement ID**: 084
**Requirement Key**: 084-harness-triple-structure
**Related Feature**: 084 Harness 三重结构（markdown + yaml + script）
**Input**: Design documents from `.specify/specs/084-harness-triple-structure/` — plan.md, requirements.md (19 FR / 6 SC / 14 STR), data-model.md (E-1…E-10 + 6 fixture families), contracts/ (5 files, 59 clauses), research.md (R1–R10), quickstart.md (S1–S8)
**Prerequisites**: plan.md (required), requirements.md (required for the user stories), data-model.md, contracts/, research.md, quickstart.md

**Tests Mode**: ON — Constitution Principle IV "Test-First & Contract-Driven Implementation" is MUST-level ("Pure functions/utilities MUST have unit tests"; "Critical flows MUST have automated regression coverage"), and `plan.md` § D10 fixes the test surface by name (`tests/contract/test_harness_triple_structure.py` plus `tests/fixtures/harness-triple-structure/`). The **template-only gate does not apply**: Principle VII's "template-only features … judge Test-First as Partial (justified)" is scoped to features with **no executable runtime code**, and this feature ships two new stdlib-only Python modules and migrates five engines — every clause here has something to run against.

**Green-point tags (`[green: <contract>#<clause>]`) are not used in this file, and the reason is measured rather than stylistic**: the five contract documents name their clauses `DS-nn` / `HC-nn` / `SR-nn` / `MB-nn` / `DM-nn`, while the clause-syntax owner (`scripts/python/clause_extract.py`, whose ids are the `C-\d+` form) classifies all five as `form_of → md-none` (measured on this branch 2026-11-05: `md-none` for each of the five, `resolvable(...) == False` for every id family). A tag on such a contract is a hard `green-dangling` ERROR, not a claim anyone can honour. Traceability therefore travels in § Traceability below — one row per task, naming the exact clause ids and the carrier — so the clause partition is stated once, not twice.

**Organization**: four user stories in the priority order `requirements.md` gives them (US1 P1, US2 P1, US3 P2, US4 P2). Setup freezes the readings everything is compared against; Foundational builds the layer, the reader, the checker and their red-first test module; the story phases consume them; the Polish phase takes the feature-level readings and never invents a mechanism.

## Definition of Done (DoD)

- DoD-1: The declaration layer exists in the framework source with exactly three members (`contract.yaml`, `facts/`, `exclusions/`), is registered in `shared/definitions/framework-map.md` in the same change that creates it, and every fact file passes the subset and required-key checks — with no aggregate ledger, index, manifest or cache anywhere at any level (C-001, C-011, C-012, FR-014)
- DoD-2: `scripts/python/declaration_reader.py` is the only file under `scripts/` and `skills/` that parses declaration YAML (the two grandfathered inline parsers sit in an explicit allowlist carrying their N4 reason), and `pyproject.toml`'s dependency list is byte-identical to the baseline (C-052, C-054, C-058, SC-006)
- DoD-3: `scripts/python/harness-triple-check.py` is read-only, offers exactly three actions, exits `0`/`1`/`2`, emits the six reasons verbatim after placeholder substitution, leaves the judged tree byte-identical, and degrades on a legacy project with an explicit exit-2 label — never `0`, never a traceback (C-026, C-027, C-035…C-039)
- DoD-4: Batch 1's nine facts each have exactly one declaration, each engine's inline constant is gone, each carrier's restatement is a pointer, and the reused `duplicate-fact` reading is zero for every one of them; 081's two acceptance files show zero diff and zero new failures (C-042, C-048, FR-018, SC-006)
- DoD-5: Batch 2's and batch 3's rosters are migrated by the same six-step procedure and each batch is independently acceptable — an unfinished later batch is never reported as an earlier batch's failure, and every row whose faces had already drifted names the corrected face in its declaration `note` (C-044…C-047, C-050)
- DoD-6: Every candidate unit has exactly one disposition; every exclusion row carries a reason from the closed three-value set and an anchor that resolves in the tree; `coverage` reports zero unclassified candidates and zero duplicated-fact literals (FR-002, FR-005, SC-001, SC-004)
- DoD-7: Distribution and mirrors are readings rather than claims — the source-route init in a sanctioned temp root delivers the roster and the copied checker runs on the client copy, and `sync-mirrors.py --check` shows no NEW drift against the recorded baseline (C-013…C-023, SC-005)
- DoD-8: The owner document's delivered chapters equal `plan.md` § Document Structure's chapter tree in both directions, the `docs/` pointer page restates no value domain, and `CHANGELOG.md` carries one entry (FR-001, C-025)

**DoD Status**: pending

## Completion Gate

- GATE-1: The contract test module is green — check: `bash scripts/bash/run-tests.sh tests/contract/test_harness_triple_structure.py -q`
- GATE-2: Zero new failures on the five frozen gate scripts' existing tests, read at id level — check: `bash scripts/bash/run-tests.sh --names-out .specify/specs/084-harness-triple-structure/test-evidence/head-failed.txt -q`, then `comm -13 <implement-start baseline> head-failed.txt` prints nothing (the baseline is captured at implement start, never inherited from this file)
- GATE-3: Mirrors and the strict pair hold — check: `python3 scripts/python/sync-mirrors.py --check` exits 0 with no NEW drift against the baseline recorded in `notes/pre-change-measurements.md`
- GATE-4: Coverage is clean and deterministic — check: `python3 scripts/python/harness-triple-check.py --action coverage` exits 0, prints zero `unclassified-candidate:` lines, and two consecutive runs are byte-identical
- GATE-5: The 081 acceptance surface did not move — check: `git diff --stat 4b65517c -- tests/contract/test_requirements_checker.py tests/contract/test_checker_form.py` prints nothing, and `python3 -m pytest --collect-only -q` still collects 40 and 37 respectively
- GATE-6: The non-goals hold — check: `git diff 4b65517c -- pyproject.toml` prints nothing, and `ls templates/commands/*.md | wc -l` still returns the count recorded in `notes/pre-change-measurements.md`
- GATE-7: No `[ ]` or `[>]` row remains — check: `grep -cE '^- \[[ >]\]' .specify/specs/084-harness-triple-structure/tasks.md` returns 0

## Format: `[ID] [P?] [Story] Description`

- **[P]**: can run in parallel — a disjoint set of write targets, no dependency on an incomplete task. Two rows that merely cite the same owner are not a conflict; two rows that both write a file are, and the pair then carries no `[P]`
- **[Story]**: required inside a User Story phase (`[US1]`…`[US4]`), forbidden everywhere else — placeholder labels such as `[US-none]` are format violations
- **[blockedBy: T001,T002]**: this row MUST NOT start until every listed task is `[X]`; the tag replaces prose such as "depends on T012"
- Every row keeps its whole text on **one line**, so the file paths stay visible to `/speckit.implement` and to the structural validator
- `[green: <contract>#<clause>]` is **not** used here — the measured reason is in the banner above; the clause partition lives in § Traceability

## Task State Sigil

`- [ ]` open · `- [>]` claimed · `- [X]` closed · `- [~]` deferred (reason recorded in `verification.md` `deferred_tasks=`). This file is generated with **every row open**: the tasks stage does not execute work.

## Path Conventions

Single project, framework-source layout: `shared/`, `scripts/`, `templates/`, `skills/`, `src/` are the sources; `.specify/` holds generated mirrors (`.specify/shared/`, `.specify/scripts/`, `.specify/skills/`) that are produced by `scripts/python/sync-mirrors.py` and never hand-edited. New material lands in `shared/declarations/`, `shared/definitions/`, `scripts/python/`, `tests/contract/`, `tests/fixtures/harness-triple-structure/`, `docs/`. Scratch work uses `.specify/.tmp/` (sanctioned root, matched by `.specify/.gitignore`) and is torn down in the same task.

**No `## Environment Prerequisites` section**: this feature depends on no external environment (no container runtime, no network pull, no live cluster, no special hardware). Toolchain and `specify init` route premises are owned by `plan.md` § Execution Premises (EP-001…EP-007) and are referenced, not restated; the task-generation-time re-measurements are recorded in `test-evidence/tasks-readings.txt`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: freeze the readings every later row is compared against, and open this feature's own evidence sinks — before any source file is touched.

- [ ] T001 [P] (FR-023, SC-006, C-047 step 1) Capture this feature's pre-change readings into `.specify/specs/084-harness-triple-structure/notes/pre-change-measurements.md` (creating `notes/` here), each with its command and its real output: (a) `python3 scripts/python/sync-mirrors.py --check` — exit code plus the per-pair counts, the drift baseline every later mirror claim is relative to; (b) the nine batch-1 constants' `file:line` via `grep -n "DEFAULT_THRESHOLD\|SEVEN_STATES\|LANE_NAMES\|CLASS_VALUES\|BASIS_VALUES\|FLOW_TYPE_VALUES\|REQUIRED_LEDGER_COLUMNS\|NEUTRAL_CATEGORIES\|PATH_VALUES" scripts/python/*.py` (30 hits today: 9 definition lines plus 21 usage sites — the number to compare against is the definition set, not the hit count) — re-measured here, never inherited from `research.md` § R5; (c) the candidate-surface counts `ls templates/commands/*.md | wc -l`, `ls skills/external/*/SKILL.md skills/internal/*/SKILL.md | wc -l`, `ls shared/workflow/*.md | wc -l`, `ls shared/definitions/*.md | wc -l`; (d) `git diff --stat 4b65517c -- tests/contract/test_requirements_checker.py tests/contract/test_checker_form.py` (empty output is A8(a)'s zero-diff premise holding at tasks entry) together with the two collect counts from `python3 -m pytest --collect-only -q`; (e) `git diff --name-only 4b65517c -- pyproject.toml` (empty is SC-006's byte-identical premise). These are frozen comparison values, not pass marks — a later empty result is only meaningful against them
- [ ] T002 [P] (FR-019, SC-001, SC-002) Freeze the clause/FR coverage baseline: `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/084-harness-triple-structure --freeze > .specify/specs/084-harness-triple-structure/coverage-baseline.txt`, then record the same run's stdout, exit code and the freeze file's name list length in `test-evidence/tasks-readings.txt`. If the accountant reports the FR lane `uncovered` on this branch, that reading is kept verbatim as the starting point — it is not discarded and no green is fabricated in its place

**Checkpoint**: every later "it used to read X" and "no NEW drift" claim has a recorded value behind it, and the coverage lane has a frozen comparison set rather than an assumed one.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: build the layer, its single parser, its judging engine and the red-first test module every user story is measured by. Nothing in Phases 3–7 can start before T007 exists.

**⚠️ CRITICAL**: T005 authors the assertions **first**; T006 and T007 close them. A green assertion written after its subject cannot show that the subject was ever missing.

- [ ] T003 (FR-003, FR-005, FR-014, C-001, C-002, C-011, C-023) Create `shared/declarations/contract.yaml` — the single owner of every machine-read value domain of this feature: `schema`, `yaml_subset`, `fact_kinds` (the closed five), `completeness_states` (the closed two), `exclusion_reasons` (the closed three), `exit_codes` (0/1/2 with their meanings), `required_fact_keys`, `required_exclusion_keys`, `gate_call_sites` (E-10's two rows) — written only in the C-008 subset, with the members of each closed set taken from `requirements.md` § Shared Strings rather than retyped from memory; and in the **same** change register `shared/declarations/`, `shared/declarations/facts/` and `shared/declarations/exclusions/` in `shared/definitions/framework-map.md` with kebab-case names and a one-line meaning each (Directory Governance). No ledger, index, manifest or cache is created at any level (C-012), and no other file restates a value this contract owns
- [ ] T004 [P] (FR-001, FR-018, plan § Document Structure) Author `shared/definitions/harness-triple-definitions.md` — the feature's single owner document for the three-layer discipline — with exactly the seven chapters of `plan.md` § Document Structure § Chapter Tree (本文档的地位与读者 / 三层各自拥有什么 / 归 yaml 的判据 / 候选屏幕 S 与流程单元 / 范围判据与排除理由的语义 / 迁移时的权威取值顺序 / 非目标), each respecting the boundary that table states (no value tables, no facts roster, no FR restatement, no batch roster), and reach every value-domain question by `<path>#/<key>` into `shared/declarations/contract.yaml`. Then read it back with `python3 scripts/python/doc-consistency-check.py --action structure --spec-dir .specify/specs/084-harness-triple-structure --path shared/definitions/harness-triple-definitions.md` and record the reading — the chapter tree compared both ways, `chapter-unexpected` empty
- [ ] T005 [P] [blockedBy: T003] (FR-017, FR-019, SC-003, C-041, C-058, FR-015) Author `tests/contract/test_harness_triple_structure.py` and its fixtures under `tests/fixtures/harness-triple-structure/` (one directory per feature; the families are `data-model.md` § Fixture set): `positive/`, one `negative-<reason>/` per reason template, `subset-violation/`, `dual-writer/`, `legacy-project/` and `screen-boundary/`, each negative carrying its expected `(exit code, reason instance)` as data so the test compares strings instead of re-deriving a template. Legs to write, all red before T006/T007 close: the six reasons verbatim after placeholder substitution; the three exit codes; the subset rejection with no best-effort parse; the dual-writer property (two branches each adding one fact file land on two distinct paths and coverage exits 0 on both trees, with no reordering of existing exclusion rows); the coverage three-state readings; the C-039 zero-write leg (`git status --porcelain` before/after a run); and the C-058 boundary leg asserting mechanically that the shared read entry is the only subset parser under `scripts/` and `skills/`, with the two grandfathered inline parsers in an explicit allowlist carrying their N4 reason. Record the red run in `notes/red-first-evidence.md`, quoting verbatim any gate row it binds (id + name + check command — a bare id is not a quote)
- [ ] T006 [blockedBy: T003,T005] (FR-009, C-052…C-058, C-008, C-009, C-010) Implement `scripts/python/declaration_reader.py`: stdlib-only, Python `>= 3.8`, both importable and CLI-callable (every consumer is invoked as `python3 scripts/python/<name>.py`, so the script's own directory is `sys.path[0]`); it owns the whole subset grammar and the single path normalization, exposing `load_contract(repo)`, `load_fact(repo, slug)`, `load_facts(repo)`, `load_exclusions(repo)` and `normalize_path(value)` (strip exactly one optional leading `.specify/`, then resolve against the repo root); each failure raises one typed error carrying the finding template id, the caller maps it to an exit code, and no function prints; the degraded case (layer absent) travels through that same typed error, never a bespoke exception (C-056)
- [ ] T007 [blockedBy: T006] (FR-016, FR-017, C-026…C-041, SC-001, SC-003) Implement `scripts/python/harness-triple-check.py`: one file, read-only, stdlib-only, no model judgement, no network, no subprocess; exactly three actions `coverage` / `verify` / `lookup` (`--repo`, `--format`, `--json-out` common; `lookup` takes `--unit-id` XOR `--fact`, both or neither being an input error); candidate screen S recomputed by text over the three carrier surfaces with `shared/definitions/*.md` excluded; fixed disposition order (a declaration naming the unit ⇒ in-scope; else an exclusion row ⇒ that reason; else `[[STR-013]]`, and a unit named by both is a finding, never resolved by file order); completeness as the three-condition conjunction with the false-green red line stated in the code (a declaration file existing is never evidence for (a), and a missing read point keeps the unit `pending`); the six reasons emitted verbatim; exit 0/1/2 per the contract; degraded layer ⇒ an exit-2 input-error label naming the missing directory, never a traceback and never 0; and the read point is a **textual** locator (a reference to the read entry plus the fact slug) with the contract's own sentence in the module docstring saying it is not a proof of semantics

**Checkpoint**: the layer, its one parser and its one judging engine exist and are pinned by a module whose legs were red first; every later phase consumes them instead of re-implementing any part.

---

## Phase 3: User Story 1 - 一条事实只有一个机器读得到的定义点 (Priority: P1)

**Goal**: the original pain — a value that today lives in an engine constant **and** in prose — ends up in exactly one declaration, with the engine reading it and the prose pointing at it. One fact, end to end, is the whole story; the remaining batch-1 facts follow it in US2 because they are closed sets read by gates.

**Independent Test**: change only the declaration file's value, then run the checker and the engine: the engine reports the new value and the carrier side's literal hits are zero — `python3 scripts/python/harness-triple-check.py --action lookup --unit-id shared/workflow/feedback-step.md` names the slug, `--action verify` exits 0 for it, and `python3 scripts/python/doc-consistency-check.py --action verify --faces duplicate --owner-path shared/workflow/feedback-step.md --spec-dir .specify/specs/084-harness-triple-structure` reports zero `duplicate-fact` hits (the reused face, no second scanner).

### Implementation for User Story 1

- [ ] T008 [US1] (FR-005, FR-006, C-042 row 1, C-047 steps 1–2) Write `shared/declarations/facts/feedback-prompt-threshold.yaml`: `fact: feedback-prompt-threshold` matching the filename stem, `kind` from the contract's five-value set, the value picked by the authority order (code > generated > authored) with any correction recorded in `note` when the two faces had already drifted, `consumers: [scripts/python/feedback-utils.py, shared/workflow/feedback-step.md]` and `former_carriers: [shared/workflow/feedback-step.md]` — the two keys disjoint, both resolving after normalization. This row is the **exemplar** every later fact row imitates, so its shape is the shape `data-model.md` § E-1 defines, not a local variant
- [ ] T009 [US1] [blockedBy: T008] (FR-009, FR-012, C-049) Replace `scripts/python/feedback-utils.py`'s `DEFAULT_THRESHOLD` inline constant with a read through the shared entry: declaration present ⇒ the constant is **deleted**, never kept as a second read; declaration absent ⇒ the output line carries `[[STR-014]]` verbatim beside the fallback value. The compatibility path is bounded — it MUST NOT be readable as a pass, and no other copy of the value survives in the file
- [ ] T010 [US1] [blockedBy: T008] (FR-007(b), FR-010, SC-002) Turn the restatement in `shared/workflow/feedback-step.md` § threshold protocol into a pointer (`<path>#/<key-path>`), complete the fact's `former_carriers` to name every carrier that used to spell the literal, then take US1's independent reading and record all three outputs verbatim in `test-evidence/us1-single-definition-point.txt`: the `lookup` line naming the slug, the `verify` exit, and the reused `duplicate` face reporting zero `duplicate-fact` hits for it. A non-zero hit count is the finding, not a reason to soften the pointer

**Checkpoint**: one fact demonstrably lives in one place; changing it updates the engine and leaves the prose with nothing to drift. The mechanism is now proved before it is applied nineteen more times.

---

## Phase 4: User Story 2 - 封闭集与映射被门禁读取，而不是被脚本抄一份 (Priority: P1)

**Goal**: every closed set, ordered operator table and mapping that a gate consumes exists once, in the declaration layer: the prose owner keeps the criterion and loses the value table, the engine reads the declaration, and the refusal text comes from the same source. This phase carries the remaining eight batch-1 facts plus batch 2 and batch 3 by `contracts/migration-batches.contract.md`'s rosters.

**Independent Test**: for one migrated set, drive an out-of-domain value through the gate and read `(exit code, reason)`; add one legal value to the declaration alone and re-drive it with no script edit; then make a declaration and a prose owner disagree and read `verify`'s exit. Three readings, no prose in the verdict.

### Implementation for User Story 2

- [ ] T011 [P] [US2] (FR-006(i), FR-018, C-042 rows 2–3) Migrate the evidence closed sets by C-047's six steps: write `shared/declarations/facts/evidence-seven-states.yaml` and `shared/declarations/facts/evidence-lanes.yaml`; delete `SEVEN_STATES` and `LANE_NAMES` from `scripts/python/evidence-utils.py` and read both through the shared entry, so the out-of-lane refusal message is drawn from the declaration rather than a second tuple; turn the restatements into pointers in `skills/internal/collect-evidence/references/evidence-discipline.md`, `shared/guidelines/better-harness.md` § 证据纪律 item 2, `shared/workflow/evidence-step.md` and `skills/internal/collect-evidence/SKILL.md`, filling `former_carriers` with every one of them. The five-dimension table in `shared/guidelines/better-harness.md` **stays** — no engine reads it, so by FR-006 (i) it is not a candidate (A7); only the seven-state re-listing migrates
- [ ] T012 [P] [US2] (FR-006(i), FR-018, C-042 rows 4–8) Migrate the flow-class closed sets by the same six steps: write `shared/declarations/facts/flow-class-classes.yaml`, `shared/declarations/facts/flow-class-basis.yaml`, `shared/declarations/facts/flow-class-document-types.yaml`, `shared/declarations/facts/flow-class-ledger-columns.yaml` and `shared/declarations/facts/flow-class-neutral-categories.yaml`; delete `CLASS_VALUES`, `BASIS_VALUES`, `FLOW_TYPE_VALUES`, `REQUIRED_LEDGER_COLUMNS` and `NEUTRAL_CATEGORIES` from `scripts/python/flow-class-check.py` and read each through the shared entry while its **executable semantics stay put** (the ledger-column header check keeps comparing the same ordered tuple, the class comparison keeps comparing the same members); turn the value tables in `shared/definitions/flow-class-definitions.md` into pointers while its criteria, ledger semantics and invariant pointers stay. The file MUST NOT gain a `flow_class` ledger row for any unit it does not already carry (A3), and no gate criterion or exit code moves (N5)
- [ ] T013 [US2] [blockedBy: T007] (FR-018, A8(a), C-042 row 9, SC-006) Migrate the `Path` value domain on 081's accepted surface, refusing scope creep in both directions: write `shared/declarations/facts/success-criterion-path-values.yaml`; delete `PATH_VALUES` from `scripts/python/validate-requirements.py` **and** the inline tuple from `scripts/python/closure-acceptance-check.py`, both reading the declaration, so the member set stays exactly the two values it is today; give `shared/workflow/acceptance-hardening.md` § Closure Verdict § Input contract a pointer while its judgement prose, refusal message template and exit-code meaning stay byte-identical, and point `templates/commands/requirements.md` and `skills/internal/create-requirements/SKILL.md` at the same declaration. Hard constraint carried by this row: `tests/contract/test_requirements_checker.py` and `tests/contract/test_checker_form.py` are **not edited at all** and show zero new failures; the six check-label set is **not** migrated (N7, an over-scope ruling recorded in `requirements.md` § Non-Goals, not an exemption pocket)
- [ ] T014 [US2] [blockedBy: T007] (FR-006(i), C-044) Migrate batch 2's gate-shaped value sets over the tree rather than over a remembered list: `expression-gate-faces` and `expression-stage-operator-table` (carrier `shared/workflow/expression-gates.md`; the engine side is `scripts/python/flow-class-check.py`'s header tuple, located with `grep -n "required = (" scripts/python/flow-class-check.py` before editing) plus `driver-stage-sequence`, `driver-gate-roster`, `driver-completion-sentinels` and `driver-stage-artifacts` (carriers `skills/external/sdd-loop-driver/SKILL.md` and `skills/external/sdd-loop-driver/references/dispatch-recipes.md`; engine side `skills/external/sdd-loop-driver/scripts/loop-state.py`, located with `grep -n "STAGE_ARTIFACTS\|write_log(\[" skills/external/sdd-loop-driver/scripts/loop-state.py`). Each fact follows C-047, and a fact whose engine side is not at the location the roster suggests is recorded as a corrected `note`, not silently re-pointed
- [ ] T015 [US2] [blockedBy: T007] (FR-006(i), C-044) Migrate batch 2's mapping-shaped sets by the same procedure: `analyze-severity-values` and the analysis finding-channel set (carriers `templates/commands/analyze.md`, `skills/internal/analyze-artifacts/SKILL.md`; locate the engine side before editing rather than naming it from memory), `review-segment-sequence` and the ARC verdict mapping (carrier `templates/review-template.md`), `self-improvement-stage-sequence` and the track-to-executor mapping (carriers `shared/workflow/self-improvement-workflow.md`, `shared/definitions/self-improvement-definitions.md`, `skills/internal/self-improvement/SKILL.md`), and `improvement-track-values` with its changed-asset-category mapping (carriers `skills/internal/improve-agent/`, `skills/internal/improve-team/`, `skills/internal/improve-tools/`, `skills/external/improve-docs/`, `skills/external/improve-skills/`). A carrier whose mapping is prose-only and consumed by nothing stays where it is and is recorded as out of scope by the FR-006 (ii) test rather than migrated for symmetry
- [ ] T016 [US2] [blockedBy: T007] (FR-006(i), C-045) Migrate batch 3's record schemas: `memory-types` and `memory-retention-thresholds` (engine `scripts/python/memory-utils.py`, whose `SCOPES` tuple is the live copy; carriers the memory skills), `history-categories` and `history-manifest-schema` (engine `scripts/python/history-utils.py`; carrier `skills/internal/manage-history/SKILL.md`), and `probe-class-values`, `probe-object-binding-map`, `quant-record-schema`, `trigger-state-schema` (carrier `shared/definitions/probe-definitions.md`; engines `scripts/python/probe-utils.py`, `scripts/python/exec-quant.py`, `scripts/python/trigger-utils.py`). Same six steps, same `former_carriers` completion — batch 3 changes the shape of what gets recorded and nothing else
- [ ] T017 [US2] [blockedBy: T013] (SC-002, SC-003, US2 acceptance 1–3) Take US2's three closed-set readings on the migrated tree and record them verbatim, each with command and exit code: (a) an out-of-domain value driven through a migrated gate is refused with that gate's existing reason and exit code, and the reason's membership test resolves against the declaration rather than a surviving inline tuple — a second tuple anywhere is the finding this reading exists to expose; (b) adding one legal member to the declaration alone makes the gate accept it with **no script edit** (if the gate still refuses, FR-007's (c) leg is unproven and the row stays open); (c) a declaration and a prose owner that disagree make `verify` exit 1 instead of settling the conflict by "prose wins" or "code wins"

**Checkpoint**: the closed sets a gate decides with have one home, one refusal source and one member set; a drifted copy anywhere now fails a program rather than waiting for a reader to notice.

---

## Phase 5: User Story 3 - 新增 harness 流程时三层结构被强制，未被排除的也说得清 (Priority: P2)

**Goal**: the discipline survives the next contributor. The candidate set is recomputed on the tree on every run, so a new command either carries a declaration or an exclusion record, and the absence of both is a named finding rather than a silent pass.

**Independent Test**: on a scratch fixture tree, add a command carrier that references a framework engine and write no record; run coverage and read the naming finding and the exit code; add one declaration or one exclusion row and re-read.

### Implementation for User Story 3

- [ ] T018 [US3] [blockedBy: T012,T013] (FR-004, FR-016, SC-001) Take coverage's deterministic reading on the repository tree with batch 1 landed, capturing the full stdout/stderr, exit code and duration of **both** runs (single-run evidence discipline: the record is the evidence, a re-run is not): the two runs are byte-identical (the comparison object is not the previous run itself); `unclassified-candidate:` appears zero times; a declaration outside the candidate set appears zero times; and the two directions of consistency are counted separately — every path in a fact's `consumers` is actually referenced on its carrier or engine side, and every carrier that references a fact is named in that fact's `consumers`
- [ ] T019 [US3] [blockedBy: T018] (FR-004, FR-015, SC-001, SC-004) Prove the discipline survives new work, in `.specify/.tmp/` and nowhere else: (a) add a command carrier whose text references a framework engine and write no record for it → coverage exits 1 and names that unit with `unclassified-candidate:`; (b) add exactly one declaration → the same tree exits 0; (c) write the dual-writer case (two branches each adding one fact file) → two distinct paths, coverage exits 0 on both trees, and an appended exclusion row lands at the end of its file with no reordering of existing rows. Tear the scratch root down and record the four readings with their commands

**Checkpoint**: a new harness-shaped unit can no longer be added without a record, and the failure is a named line rather than a reviewer's memory.

---

## Phase 6: User Story 4 - 不属于 harness 的流程完全不受影响 (Priority: P2)

**Goal**: keep the discipline from becoming a ritual. Units with no harness asset and no machine-consumed value owe one exclusion record with a reason from the closed set and an anchor a reader can follow — and nothing else changes for them.

**Independent Test**: run the reading over the excluded units (zero errors, one disposition each, every anchor resolving), over an unmigrated unit (`pending`, not an error), and over a skill that ships its own YAML input template (not mistaken for a declaration fact).

### Implementation for User Story 4

- [ ] T020 [US4] [blockedBy: T007] (FR-002, FR-005, SC-004, C-006, C-007) Write the exclusion records the candidate set requires and only those: `shared/declarations/exclusions/no-harness-asset.yaml` for `skills/external/draw-diagram/SKILL.md` and `skills/external/database-utils/SKILL.md`, and `shared/declarations/exclusions/no-machine-fact.yaml` for `skills/internal/summarize-project/SKILL.md` and `skills/external/humanize/SKILL.md` — each row carrying `unit`, `carrier` and `anchor`, with the anchor a path plus a locatable line or section that resolves in the tree. One disposition per unit, no unit named twice, a new row appended and never reordered, and no third file created for a reason with zero rows (a reason file that would be empty MUST NOT be created to satisfy the shape)
- [ ] T021 [US4] [blockedBy: T020] (SC-001, SC-002, US4 acceptance 2–3) Take the "unaffected stays legal" readings and record each with its command: an unmigrated two-layer unit reads `pending` (`[[STR-005]]`) rather than an error and reads `complete` (`[[STR-004]]`) only once its fact migrates; and a skill that ships its own structured-input template (`skills/internal/summarize-project/templates/project-input.template.yaml`) is **not** mistaken for a declaration-layer fact, because the reader only ever opens files under the declaration directory — the assertion is about the reader's input face, not about the template's shape
- [ ] T022 [US4] [blockedBy: T020] (FR-013, C-017, C-037, C-056) Take the legacy-project degradation reading on `tests/fixtures/harness-triple-structure/legacy-project/`: the checker exits 2 with an explicit input-error label naming the missing directory, prints no traceback, and never exits 0; a migrated engine reading an absent declaration emits `[[STR-014]]` and the consuming flow continues; and neither shape may be read as a pass — the reading is recorded, not argued
- [ ] T023 [US4] [blockedBy: T020] (FR-002, Edge Cases 末条) Retire the screen's conservative side by record rather than by a second judgement: the `screen-boundary` carrier that only mentions a script path in prose stays **in** the candidate set (the text test's accepted blind side) and is retired by exactly one exclusion row with a resolvable anchor — the row MUST NOT introduce a "does it really call it" semantic test, which would be the second mechanism the screen exists to avoid

**Checkpoint**: the boundary is writable and checkable in both directions — in-scope by declaration, out-of-scope by record, and nothing silently in between.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: wire the one new call site, land the pointer surfaces, project the mirrors, and take the feature-level readings that turn all of it into evidence. No new mechanism lands here.

- [ ] T024 [P] [blockedBy: T007] (FR-010, C-040, C-021, D8) Wire the gate host as an **opt-in** delegation: `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` gains `--triple-structure`, default **off**, delegating once to the checker's `verify` action and forwarding each finding line verbatim under one check name. Turning it on by default is forbidden by measurement, not taste: `tests/contract/test_acceptance_premises.py` asserts the produced finding names stay a subset of the existing four, so a default-on delegation would turn an 081 assertion red (T-003 records the trade-off). Correct the host's module docstring in the same change so it no longer claims a self-containment the delegation contradicts while its real mechanism — no framework imports — stays true
- [ ] T025 [P] [blockedBy: T004] (FR-018, C-025) Land the documentation entry and the release note: a `docs/` pointer page registered per `docs/concepts/documentation-model.md` that states what the layer is and routes to `shared/definitions/harness-triple-definitions.md` **without** restating any value domain, and one `CHANGELOG.md` entry naming feature 084 and the two-layer-to-three-layer change
- [ ] T026 [blockedBy: T009,T010,T011,T012,T013,T014,T015,T016,T020,T023,T024] (C-019…C-023, SC-005 first limb) Project the mirrors from the framework sources and verify them: run `python3 scripts/python/sync-mirrors.py` (write), then `--check`, and confirm no **NEW** drift on the pairs this feature touches against the baseline recorded in `notes/pre-change-measurements.md` (the `scripts/` pair is strict, so a mirror-only extra file fails; the `skills/external` pair flattens the layer name). Run the projection a second time and confirm it changes nothing — a repeatable generator, not a one-shot copy — and confirm no `.specify/` file was hand-edited as part of any earlier row
- [ ] T027 [blockedBy: T026] (C-043, C-048, SC-001, SC-002) Take batch 1's five closure readings mechanically, each with its command and verbatim output: (a) every batch-1 fact has exactly one declaration passing subset and required keys; (b) the carrier side shows zero `duplicate-fact` hits for each fact; (c) every engine reaches its value through the shared entry and its inline constant is gone (`grep` for the literal returns only the declaration); (d) coverage reports zero `unclassified-candidate:` and zero `duplicated-fact-literal:` for batch-1 units while unmigrated units stay `pending` without turning red; (e) the existing gate tests show zero new failures. The exit-0 criterion reads "zero unclassified", never "zero pending" — `pending` on an unmigrated unit is a reading, not a failure
- [ ] T028 [blockedBy: T027] (C-044…C-047, C-050, SC-002) Take batch 2's and batch 3's closure readings in the same five-measurement shape, and state the independence claim explicitly: closing batch 2 requires nothing from batch 3, and an unfinished batch 3 MUST NOT be reported as a batch-2 failure. Every fact whose faces had already drifted names the corrected face in its declaration `note`; a row that cannot name the corrected face is incomplete rather than "close enough"
- [ ] T029 [blockedBy: T026] (SC-006, N5, FR-010) Take SC-006's non-goal readings: `git diff 4b65517c -- pyproject.toml` prints nothing; `git diff --stat 4b65517c -- tests/contract/test_requirements_checker.py tests/contract/test_checker_form.py` prints nothing and the two collect counts are unchanged from `notes/pre-change-measurements.md`; the five frozen gate scripts' existing tests show zero new failures by an id-level set difference against the implement-start baseline (`comm -13`); and the command-template count and the feature-status value count are unchanged against the recorded readings. A count that moved is reported as a moved count, not absorbed
- [ ] T030 [blockedBy: T026] (FR-013, C-013…C-018, SC-005) Take the distribution reading on the **source route**, in a sanctioned scratch root: create `.specify/.tmp/084-init/`, initialise a project there with the source checkout ahead of the installed package, assert the roster per file (`contract.yaml`, `facts/*.yaml`, `exclusions/*.yaml` and the owner document all present under `.specify/`), run the copied checker against the client copy and read its exit — `0`, or the C-017 degraded label with exit 2, recorded as it is and never retried until green. Tear the scratch root down and verify the teardown, so a second run cannot inherit state from the first
- [ ] T031 [blockedBy: T027,T028,T030] (SC-001…SC-006, quickstart S5–S8) Run `quickstart.md`'s S5–S8 on the final tree and record the real output in `notes/quickstart-run.md`, teardown steps included, so the quickstart is rendered rather than asserted. Any scenario whose premise no longer holds is recorded as a reading against that premise — `quickstart.md` is a plan-owned artifact and is not rewritten from the tasks or implement stage; a stale premise is reported to its owner, never silently edited around

**Checkpoint**: the layer is distributed, mirrored, wired into exactly one existing gate host behind a flag, and every feature-level criterion reads from a run rather than from a summary.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: no dependencies; T001 and T002 are path-disjoint and run together
- **Phase 2 (Foundational)**: **blocks every story phase** — T003 defines the value domains, T004 the owner document, T005 authors the red-first assertions, T006 the single parser, T007 the judging engine
- **Phases 3–6 (User Stories)**: all start after T007; they consume the layer rather than extend it
- **Phase 7 (Polish)**: depends on every source edit having landed, because T026 projects mirrors and T027–T031 measure the whole feature

### User Story Dependencies

- **US1 (P1, MVP)**: after Phase 2 — no dependency on another story
- **US2 (P1)**: after Phase 2 — independent of US1 in files, but shares US1's C-047 procedure; T013 is the only row on 081's accepted surface and carries its own zero-diff constraint
- **US3 (P2)**: reads the tree after batch 1 (T012, T013), because a coverage run before any declaration exists can only report `pending`, which is not the reading US3 exists to take
- **US4 (P2)**: after T007 only; its exclusion records are independent of the migration work

### Within Each Story

- US1: declaration before the engine read (T009) and the carrier pointer (T010), so the engine never reads a file that does not exist yet
- US2: T013 waits on T007 alone; T017's gate readings come after the set they read (T013) and are the story's verdict rather than a comment on it
- US3: T019 waits on T018, because the new-unit case is meaningful only on a tree whose existing candidates are already classified
- US4: T021–T023 wait on T020, since each of them reads the exclusion set that row creates
- Polish: T026 waits on every source edit; each reading row waits on the projection, and T031 waits on the readings it re-walks

### Parallel Opportunities

- T001 ∥ T002 (Setup), T004 ∥ T005 (owner document vs test module), T011 ∥ T012 (evidence sets vs flow-class sets — disjoint write targets), T024 ∥ T025 (gate host vs docs/CHANGELOG)
- T014, T015 and T016 are **not** parallel in practice: each one migrates facts whose carriers overlap the others' report surfaces, and all three end by needing one `verify` run over the same tree
- Not parallel by construction: T005 → T006 → T007 (the parser and the engine close the assertions the module states), T026 → T027 → T028 (each reading compares against the previous one's tree)

---

## Traceability

Every row's requirement and success-criterion references, and the contract clause or carrier that answers them. A clause is green only when the row's carrier is green; the clause partition here is the file's single statement of it (the measured reason the `[green:]` tag is unusable on these contracts is in the banner).

| Row | FR | SC | Contract clauses / evidence carrier |
|---|---|---|---|
| T001 | FR-023 | SC-006 | C-047 step 1 (the value to migrate is picked from a measured tree) — `notes/pre-change-measurements.md` |
| T002 | FR-019 | SC-001, SC-002 | coverage accountant's own freeze — `coverage-baseline.txt` |
| T003 | FR-003, FR-005, FR-014 | SC-002, SC-004 | C-001, C-002, C-011, C-012 — `shared/declarations/contract.yaml` + `shared/definitions/framework-map.md` |
| T004 | FR-001, FR-018 | SC-001 | plan § Document Structure chapter tree, both directions — `shared/definitions/harness-triple-definitions.md` |
| T005 | FR-008, FR-015, FR-017, FR-019 | SC-003, SC-004 | C-041, C-058, C-007, C-008 (the subset's negative fixture) — `tests/contract/test_harness_triple_structure.py` + fixture families |
| T006 | FR-008, FR-009 | SC-002, SC-006 | C-052…C-058, C-008, C-009, C-010 — `scripts/python/declaration_reader.py` |
| T007 | FR-016, FR-017 | SC-001, SC-003 | C-026…C-041 — `scripts/python/harness-triple-check.py` |
| T008 | FR-005, FR-006 | SC-002 | C-042 row 1, C-047 steps 1–2 — `shared/declarations/facts/feedback-prompt-threshold.yaml` |
| T009 | FR-009, FR-012 | SC-002 | C-049 (bounded compatibility) — `scripts/python/feedback-utils.py` |
| T010 | FR-007(b), FR-010 | SC-002 | the reused `duplicate-fact` face — `shared/workflow/feedback-step.md` |
| T011 | FR-006(i), FR-018 | SC-002 | C-042 rows 2–3, A7 (five-dimension table stays) — evidence facts, `scripts/python/evidence-utils.py`, four carriers |
| T012 | FR-006(i), FR-018 | SC-002 | C-042 rows 4–8, A3 (no new ledger row) — flow-class facts, `scripts/python/flow-class-check.py`, `shared/definitions/flow-class-definitions.md` |
| T013 | FR-018 | SC-002, SC-006 | C-042 row 9, A8(a), N7 — Path fact, `scripts/python/validate-requirements.py`, `scripts/python/closure-acceptance-check.py`, `shared/workflow/acceptance-hardening.md` |
| T014 | FR-006(i) | SC-002 | C-044 (gate-shaped sets) — expression facts, driver facts, `shared/workflow/expression-gates.md`, `skills/external/sdd-loop-driver/SKILL.md` |
| T015 | FR-006(i) | SC-002 | C-044 (mapping-shaped sets) — analyze / review / self-improvement / improvement facts and their carriers |
| T016 | FR-006(i) | SC-002 | C-045 (record schemas) — memory / history / probe facts, `shared/definitions/probe-definitions.md` |
| T017 | FR-007 | SC-002, SC-003 | US2 acceptance 1–3 — the three closed-set gate readings |
| T018 | FR-004, FR-016 | SC-001 | C-029, C-030, C-031, C-033 — the two deterministic coverage runs |
| T019 | FR-004, FR-015 | SC-001, SC-004 | C-030 (conservative screen), C-012 (no ledger) — the new-unit and dual-writer readings |
| T020 | FR-002, FR-005 | SC-004 | C-006, C-007, C-012 — the two exclusion files and their anchors |
| T021 | FR-002, FR-007 | SC-001, SC-002 | E-6 (`complete` / `pending`), C-001 (the reader's input face) — the unaffected-unit readings |
| T022 | FR-013 | SC-005 | C-017, C-037, C-056 — the legacy-project degradation reading |
| T023 | FR-002 | SC-004 | C-030's accepted conservative side, C-007 — the screen-boundary retirement |
| T024 | FR-010 | SC-003 | C-040 (two call sites), C-021, D8, T-003 — the opt-in gate delegation |
| T025 | FR-018 | SC-006 | C-025 — the `docs/` pointer page and the `CHANGELOG.md` entry |
| T026 | FR-013 | SC-005 | C-019…C-023 — the mirror projection and its second, no-op run |
| T027 | FR-011 | SC-001, SC-002 | C-043, C-048 (a)–(e) — batch 1's five closure readings |
| T028 | FR-011 | SC-002 | C-044…C-047, C-050 — batch 2's and batch 3's readings plus the independence claim |
| T029 | FR-010 | SC-006 | N5, FR-018's zero-diff clause — the non-goal readings |
| T030 | FR-013 | SC-005 | C-013…C-018 — the source-route distribution reading and its teardown |
| T031 | all 19 FR | SC-001…SC-006 | quickstart S5–S8 rendered on the final tree — `notes/quickstart-run.md` |

**Coverage statement**: all 19 functional requirements and all 6 success criteria are named by at least one row; FR-008 is carried twice on purpose (T005 as its negative fixture, T006 as its implementation), because a subset rule that only one of the two carries is exactly the "rule implemented once, asserted nowhere" shape this feature removes. SC-002's three named segments are carried by three different rows (T010 the residual segment, T011–T016 the declaration side, T018 the state side) and no row claims the criterion on the strength of one segment.

---

## Notes

- **Story-to-batch mapping, stated once**: US1 carries batch 1's first fact end to end because the *mechanism* is the story; US2 carries the other eight batch-1 facts plus batch 2 and batch 3 because each of them is a value a gate decides with. No fact is assigned twice and none is dropped — the authoritative roster is `contracts/migration-batches.contract.md` C-042/C-044/C-045, and this file cites it rather than copying it
- **Premises are re-measured, not inherited**: every count and `file:line` this file cites lives in `notes/pre-change-measurements.md` with the command that produced it (T001). Where a row tells the implementer to locate an engine side with a `grep`, that is deliberate — the location is a measurement at edit time, not a fact this file may assert. The trap shape this avoids: a printed re-derivation command that was never run is a claim, not a measurement.
- **`[P]` is a path fact, not an intention**: each marked pair writes disjoint files; the two rows that both write the exclusion files carry no `[P]`, and neither does any row that closes an assertion another row opened
- **Two Hats**: every edit in this file lands in the framework sources (`shared/`, `scripts/`, `templates/`, `skills/`, `docs/`, `tests/`, `CHANGELOG.md`). `.specify/` copies arrive only through T026's projection — a hand-edited mirror is a defect even when it makes the tree look green (FF-12)
- **No environment section, and the omission is deliberate**: this feature has no external environment dependency, so the section the template reserves for probe verdicts would be empty; toolchain and distribution-route premises are owned by `plan.md` § Execution Premises and the task-generation re-measurements are in `test-evidence/tasks-readings.txt` (A13 boundary: one landing point per fact, and this file is not a second one)
- **Deferral discipline**: prefer `[~]` with its reason recorded in `verification.md` `deferred_tasks=` over leaving a row `[ ]` "for now"; and prefer a stated remainder over a rounded-up green — a reading that did not happen is reported as not having happened, which is the whole point of the layer this feature builds
- **This file is generated, not executed**: every row is open by design. The tasks stage produces the plan of work plus the evidence of § Traceability's completeness; it does not tick, defer or implement anything
