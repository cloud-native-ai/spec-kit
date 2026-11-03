# Tasks: Stricter Acceptance & Artifact Review（更严格的验收与产物审查）— Slice 081b

**Requirement ID**: 081
**Requirement Key**: 081-acceptance-hardening
**Related Feature**: 081 更严格的验收与产物审查（Stricter Acceptance & Artifact Review）
**Input**: Design documents from `.specify/specs/081-acceptance-hardening/`
**Prerequisites**: plan.md (required), requirements.md (required), data-model.md, contracts/ (5 files), `tasks-081a.md` (archived precedent slice)

**Tests Mode**: ON — Constitution Principle IV "Test-First & Contract-Driven Implementation" is MUST-level (`Pure functions/utilities MUST have unit tests`, `Critical flows MUST have automated regression coverage`), and plan.md § D10 assigns this slice a single test carrier that MUST be named in its row set: `tests/contract/test_acceptance_premises.py`. The four new deterministic findings are a gate surface, so they land with a contract test that goes red before their implementation rows close.

**Scope**: this file covers **slice 081b only** (plan.md § D10: "US2 — runtime stack, execution premises, inherited blockers, the four `pre-analyze` findings, the A13 boundary"). Slices 081c–081d are recorded in `## Deferred Slices` as future work, not as tasks. The slice boundary and its status consequence are stated once in `## Slice Boundary`.

## Parent Context

This slice belongs to **parent Feature 081** and changes no requirement. Every FR/SC below is the parent's own numbering — this file renumbers nothing, re-derives nothing, and states no threshold of its own.

- **Parent requirements**: `.specify/specs/081-acceptance-hardening/requirements.md` — § B "运行时栈／依赖所有权、执行前提与继承 blocker" is this slice's whole scope: FR-009 (runtime-stack table + the three `in-scope` duties), FR-010 (Execution Premises), FR-011 (Inherited Blockers + the `inherited` carrier obligation), FR-012 (the four closed findings, no fifth class, no eighth reason). Its § Success Criteria SC-005 is the one criterion this slice moves. § Shared Strings stays the only spelling owner for `runtime-dependency-not-owned: RS-NNN` / `falsified-premise-undecided: EP-NNN` / `inherited-blocker-undisposed: <feature>:<row>`.
- **Parent plan**: `.specify/specs/081-acceptance-hardening/plan.md` § D4 (the landing map for these three tables and the absorbed obligations), § D10 081b row (slice scope and the three carriers it MUST name), § Execution Premises (EP-001…EP-009 — the parent's planning-time premises; **not** re-tabulated here), § Inherited Blockers (IB-001…IB-008 — the parent's dependency dispositions; **not** re-tabulated here), § Project Structure (the exact paths this slice fills), § Mirror Obligations (the pairs and the measured pre-change parity).
- **Contracts**: `contracts/artifact-schemas.contract.md` AS-05…AS-12 (the two tables, the `in-scope` duties, the carrier rule, the A13 boundary) and AS-13/AS-15 (one owner, skeleton without domains); `contracts/gate-wiring.contract.md` GW-05…GW-07 (the four findings in the existing checker and gate rows, waivable in the existing grammar) and GW-10 (A13 landing point); `contracts/closure-acceptance-check.contract.md` C-13/C-14/C-17 (the external-source extraction the checker still owes). `contracts/review-composition.contract.md` and `contracts/state-vocabulary.contract.md` are out of scope — 081c / 081a.
- **Data model**: `data-model.md` § E-5 (Runtime Stack Row), § E-6 (Execution Premise), § E-7 (Inherited Blocker) and § Fixture set, whose `Slice` column already assigns `premise-mutation` and `runtime-gap-mutation` to 081b.
- **Precedent slice**: `tasks-081a.md` (archived; **MUST NOT** be modified by this slice). It closed with the feature `Blocked` and left the owner doc's extension points in place for this slice to fill.

**The parent feature's status is `Blocked` today and MUST still be `Blocked` when this slice closes.** 081b wires no closure call site and turns no `final`-path criterion to `pass`; a slice that closes its own row set has not made the feature `Implemented`.

## Definition of Done (DoD)

- DoD-1: Every row's stated artifact exists at the path the row names, and every edited framework source has its regenerated mirror (`.specify/shared/workflow/`, `.specify/templates/`, `.specify/skills/sdd-loop-driver/`, `.specify/scripts/python/`) with both `--check` runs at exit 0
- DoD-2: `tests/contract/test_acceptance_premises.py` is green, and red-first is claimed **only if a red run was actually recorded** in `.specify/specs/081-acceptance-hardening/notes/red-first-evidence-081b.md` with command, real output, exit status and failing count; if the module was authored against a subject that landed in the same part, the note says that instead of claiming a red
- DoD-3: The four findings fire from the two mutation fixtures, each reason an **instance** of a `requirements.md` § Shared Strings template by the two-part membership test (template match plus a well-formed argument) — no fifth finding class, no eighth reason, no re-spelled literal
- DoD-4: `shared/workflow/acceptance-hardening.md` is the **only** definition point for the two new tables' column sets, value domains and invalid-row rules; `templates/plan-template.md` carries the column sets and a pointer and **no** domain literal and **no** invalid-row rule
- DoD-5: The A13 boundary is stated exactly once (owner § Gates) and pointed at from the two new owner sections and the plan skeleton; `tasks.md` § Environment Prerequisites stays the probe-verdict carrier and does not become a second landing point for a planning-time premise
- DoD-6: `verification.md`'s SC-005 row states exactly what the evidence supports (`pass`, or a precise `partial` naming the 081c/081d remainder) with its five `SC-005_`-prefixed ladder fields when it is not `pass`; SC-001 and SC-002 are unchanged; the acceptance summary is **copied** from a fresh checker payload, never recomputed
- DoD-7: No requirement was dropped, renumbered, or softened: the four finding classes stay four, the reason set stays seven templates, the eight-stage operator coverage in `shared/workflow/expression-gates.md` is unchanged, and no new command template, skill, gate id or gate registry row is introduced

## Completion Gate

- GATE-1: The slice's single test carrier is green — check: `bash scripts/bash/run-tests.sh tests/contract/test_acceptance_premises.py -q`
- GATE-2: The adjacent frozen guards are green too (this slice edits their subjects) — check: `bash scripts/bash/run-tests.sh tests/contract/test_closure_acceptance_check.py tests/contract/test_expression_gates_doc.py tests/contract/test_expression_gate_wiring.py tests/contract/test_premise_carrier_contract.py -q`
- GATE-3: Mirror and per-tool-copy parity holds — check: `python3 scripts/python/sync-mirrors.py --check` and `python3 scripts/python/regen-command-copies.py --check` both exit 0
- GATE-4: No `[ ]` or `[>]` row remains — check: `grep -cE '^- \[[ >]\]' .specify/specs/081-acceptance-hardening/tasks.md` returns 0
- GATE-5: Both mutation fixtures are refused by **both** producers with the same reason instance — `premise-mutation` → `falsified-premise-undecided: EP-NNN`, `runtime-gap-mutation` → `runtime-dependency-not-owned: RS-NNN` — check: the legs in `tests/contract/test_acceptance_premises.py` (the direct command is informational only: `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir tests/fixtures/acceptance-hardening/runtime-gap-mutation --stage plan --repo .` is expected to exit 1)
- GATE-6: The slice did not move the feature's status — check: `awk -F'|' '$2 ~ /^ *081 *$/ {print $5}' .specify/memory/features.md` still prints ` Blocked ` and `.specify/memory/features/081.md` `**Status**` still reads `Blocked`
- GATE-7: The feature's single smoke command still passes twice with the same exit code — check: `bash scripts/bash/run-tests.sh tests/integration/test_acceptance_smoke.py -q` run twice, identical exit status, refreshed evidence at `.specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt`

## Environment Prerequisites

Probe verdicts are **this section's** to own (A13, owner: `shared/workflow/acceptance-hardening.md` § Gates § The A13 boundary). Planning-time premises are **not** restated here — they live in `plan.md` § Execution Premises (EP-001…EP-009), and dependency-inherited records live in `plan.md` § Inherited Blockers. A verdict below carries its probe command and the date it was run; none of them is a premise.

- system `python3` — available — probe: `python3 --version` @ 2026-11-03 → `Python 3.9.6`; both checkers this slice edits are stdlib-only and claim `>= 3.8` (runtime-stack row `RS-001`), so the interpreter that actually runs `pre-analyze-check.py` and `closure-acceptance-check.py` in this repo is 3.9.6, not the venv's; affected rows: T006, T008, T012
- pytest runner — available — probe: `.venv/bin/python -m pytest --version` @ 2026-11-03 → `pytest 9.2.0` on `CPython 3.14.6`, matching `test-evidence/plan-runner-pins.txt` (the pin this comparison rides is valid only while re-reading reproduces it — FR-023); affected rows: T005, T012
- `git` — available — probe: `git --version` @ 2026-11-03 → `git version 2.54.0 (Apple Git-157)`, matching `test-evidence/plan-runner-pins.txt`; affected rows: T009
- mirror engines — available — probe: `python3 scripts/python/regen-command-copies.py --check` → exit 0 (`OK: all per-tool command copies match the source templates.`) and `python3 scripts/python/sync-mirrors.py --check` → exit 0 (six pairs; `shared` 62 files, `scripts` 119 files — 081a added `shared/workflow/acceptance-hardening.md` and `scripts/python/closure-acceptance-check.py`, which is why the pair counts moved from the plan-time 61/118); affected rows: T009

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (`[US2]` only in this slice — 081b is the US2 slice)
- **[blockedBy: T001,T002]**: this row MUST NOT start until every listed task is `[X]`
- Include exact file paths in descriptions; keep each task row on ONE line
- `[green: <contract>#<clause>]` is not used in this slice: each contract this slice touches is claimed by one row set inside a single slice, so there is no cross-phase green point to partition

## Task State Sigil

`- [ ]` open · `- [>]` claimed · `- [X]` closed · `- [~]` deferred (reason recorded in `verification.md` `deferred_tasks=`).

## Path Conventions

Single project: framework sources at repository root (`templates/`, `shared/`, `skills/`, `scripts/`, `tests/`); `.specify/` copies are generated mirrors (`.specify/templates/`, `.specify/shared/`, `.specify/skills/`, `.specify/scripts/`); per-tool command copies live in `.claude/commands/`, `.github/prompts/`, `.qoder/commands/`, `.opencode/command/` and are regenerated, never hand-edited.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Author the declarative fixture inputs the four findings are proved on, and open this slice's own evidence landing point without touching 081a's record.

- [ ] T001 [P] Author the two mutation fixtures as declarative minimal file sets on the shape of `tests/fixtures/acceptance-hardening/positive/` — `tests/fixtures/acceptance-hardening/premise-mutation/` (`EP-001` carries `Status: falsified` with the `Decision` cell emptied, everything else as in `positive`) and `tests/fixtures/acceptance-hardening/runtime-gap-mutation/` (one capability declared in prose carrying its own `RS-NNN` with **no** table row, plus one `signed-contract` row whose `Pin` cell is empty) — each set holding `requirements.md`, `plan.md`, `tasks.md`, `verification.md`, `feature-detail.md`, `feature-registry.md`, none referencing a real feature directory (shape per `data-model.md` § Fixture set, whose `Slice` column assigns both cases here; AS-07, AS-08, AS-09, AS-10)
- [ ] T002 [P] Open this slice's red-first landing point at `.specify/specs/081-acceptance-hardening/notes/red-first-evidence-081b.md` — per-test command line, real output, exit status and failing count for `tests/contract/test_acceptance_premises.py`, plus the section the Polish rows write their readings into; 081a's `.specify/specs/081-acceptance-hardening/notes/red-first-evidence.md` is a dated record of a different slice and MUST NOT be rewritten or merged into

**Checkpoint**: every later assertion has a deterministic fixture to read, and this slice has its own evidence sink.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The two schema definition points — the owner doc's two sections and the plan template's two skeletons. No US2 row can start before them, because every checker row judges against the schema and every template row points at it.

**⚠️ CRITICAL**: No user-story row may start until T003 and T004 are closed.

- [ ] T003 Land the two schema sections in `shared/workflow/acceptance-hardening.md` — `## Execution Premises` (columns `ID | Premise | Evidence | Status | Decision`; `Status` closed over `verified | unverified | falsified`; `Decision` required and drawn from `resolve-in-scope | fallback | user-waiver` whenever `Status` is `falsified`; the duty that every FR consuming a runtime capability cites a premise ID; and the rule that a known negative conclusion becomes a `falsified` premise rather than an out-of-scope note) and `## Inherited Blockers` (row locator `<feature>:<row>`; `Disposition` closed over `resolved | inherited | not-applicable`; the three dispositions' obligations, including the `inherited` carrier requirement — a mandatory task row of the slice plus its test module, or a mandatory gate, and **MUST NOT** be a deferrable `supporting`-path SC — with undisposed, blank-carrier, unresolvable-carrier and deferrable-carrier all judged under the **one** existing reason; and the rule that the dependency set is declared, never implied) — then **delete the matching bullet from `## Extension Points`** so the file never carries both a section and a promise of it; the A13 three-carrier boundary stays stated once in `## Gates` and the two new sections point at it instead of restating it (AS-09, AS-10, AS-11, AS-12; V-18…V-22); mirror: `.specify/shared/workflow/acceptance-hardening.md` via `python3 scripts/python/sync-mirrors.py`
- [ ] T004 Add the two table skeletons to `templates/plan-template.md` — `## Execution Premises` and `## Inherited Blockers`, each an empty table carrying exactly the fixed column set of T003 plus one pointer line naming the owner's section, and **no** value domain, **no** invalid-row rule and **no** threshold, placed after `### Mirror Obligations` and before `## Document Structure` so a plan reads structure → premises → presentation; `templates/commands/plan.md` needs no pointer and is left untouched — measured 2026-11-03: `grep -n "Execution Premises\|Inherited Blockers" templates/commands/plan.md` has zero hits and the command delegates in-place template fill to `skills/internal/create-plan/SKILL.md`, which enumerates no plan-section list, so the skeleton heading is itself the trigger; mirror: `.specify/templates/plan-template.md` (AS-13, AS-15)

**Checkpoint**: one owner for the schema, one skeleton per table, no domain literal outside the owner.

---

## Phase 3: User Story 2 - 「运行时由 X 提供」必须是一行可验收的记录，已知的坏前提必须被继承 (Priority: P1)

**Goal**: the two tables become structured first-class artifacts with a schema owner, and the four deterministic defects in them are caught by the existing pre-analyze gate — runtime-stack row missing or empty, `signed-contract` without pin or contract path, `falsified` premise without a `Decision`, inherited blocker undisposed (including the `inherited` carrier's existence and eligibility) — with the `in-scope` three duties absorbed by the existing runtime-row class, never as a fifth finding.

**Independent Test**: run `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --stage plan` against the two mutation fixtures and observe exit 1 with `falsified-premise-undecided: EP-NNN` and `runtime-dependency-not-owned: RS-NNN`; run `python3 scripts/python/closure-acceptance-check.py` against the same two and observe the same reason instances; run both against `tests/fixtures/acceptance-hardening/positive` and observe no new reason. That is the whole of SC-005's 4/4 clause — see `## Slice Boundary`.

### Tests for User Story 2 (MANDATORY) ⚠️

> **NOTE: write this FIRST; it MUST fail before T006 and T008 close.**

- [ ] T005 [US2] Author `tests/contract/test_acceptance_premises.py` — the slice's single test carrier — with legs (a) the four findings through `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` on the two mutation fixtures, every emitted instance passing the two-part membership test of `requirements.md` § Shared Strings; (b) the `in-scope` three duties judged **separately**: an empty or unresolvable `FR` cell is an input error (exit 2) and never a block, while a missing `tasks.md` row quoting that FR and a missing joint-acceptance row naming that `RS-NNN` both yield `runtime-dependency-not-owned: RS-NNN`; (c) the `inherited` carrier rule on purpose-built row sets: missing carrier, carrier that does not resolve, and carrier naming a `supporting`-path SC are judged as one undisposed row under the one reason, while a carrier naming a mandatory test module or a mandatory gate passes; (d) cross-producer agreement — for both mutation fixtures the closure checker and the pre-analyze gate name the **same** reason instance (two producers, one closed set of templates, no second spelling); (e) pin validity — a `pytest --version` / `git --version` reading that differs from `test-evidence/plan-runner-pins.txt` makes that comparison an input error (exit 2), never new failures; (f) the A13 one-fact rule — the owner states the three carriers once and the plan skeletons carry pointers only; the module's subject must be able to break, so every leg asserts a verdict, not a string presence alone (AS-07…AS-12; GW-05, GW-06, GW-07; V-18…V-22)
- [ ] T006 [US2] [blockedBy: T005] Implement the four deterministic findings in `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` using the script's existing `check` / `severity` / `path` / `line` / `message` shape and its existing `--waive CHECK:REL_PATH:LINE` grammar: (1) a runtime-stack row missing or empty, and (2) a `signed-contract` row missing its pin or its contract path, both mapping onto `runtime-dependency-not-owned: RS-NNN` — the class also absorbs the two `in-scope` duties that need the other artifacts (a `tasks.md` row quoting the `FR`, and a joint-acceptance row naming the `RS-NNN`), so the prose-only case and the unquoted/unaccepted case share one reason; (3) a `falsified` premise with no `Decision` → `falsified-premise-undecided: EP-NNN`; (4) an inherited blocker undisposed, including the `inherited` row whose carrier is blank, unresolvable, or a deferrable `supporting`-path SC → `inherited-blocker-undisposed: <feature>:<row>`; the prose-only instance argument is the `RS-NNN` the prose declares (the reason's argument grammar admits only `RS-\d{3}`, so a declaration carrying no id cannot produce a valid instance and MUST be reported as an input error naming that line — never a silent pass, and never an eighth reason, following FR-009's own precedent that a defective cell is a conclusion about the artifact); read `verification.md` and the dependency features' details directly, outside `formal_files`, whose live-line scans keep exactly their current scope; stage-gate the plan-side findings so a requirements-stage run does not demand an artifact that is not due yet; and keep the four **closed** — no fifth finding class, no gate registry row (FR-009's three duties are absorbed, not added); mirror: `.specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py`
- [ ] T007 [US2] [blockedBy: T006] Extend the operator rows of `shared/workflow/expression-gates.md` for the four findings — `G-req-clarity` (requirements stage) carries findings 1 and 2, `G-plan-fact` (plan stage) carries all four — keeping both gate ids, the eight-stage coverage, the blocking levels and the face table unchanged: no new gate id, no new registry row, no second checker and no parallel blocking path (GW-06); mirror: `.specify/shared/workflow/expression-gates.md`
- [ ] T008 [US2] [blockedBy: T001,T005] Complete the closure checker's external-source extraction in `scripts/python/closure-acceptance-check.py`: C-17's dependency-feature record extraction (a dependency's `## Deferred` rows, its `blocked` / `deferred` verification rows, and its `deferred_tasks=` list, read from the dependency details that the plan's declared set names) so an undisposed row is discovered rather than merely judged; the `inherited` carrier eligibility rule (resolve the named carrier, refuse a deferrable `supporting`-path SC as carrier, judge both under the existing reason); and the `signed-contract` contract-path presence check alongside pin and joint acceptance — keeping the seven templates, the exit tri-state 0/1/2, the single `final_path` computation and `--audit-existing`'s explicit not-implemented exit 2 (081d owns the mode), and keeping every 081a assertion in `tests/contract/test_closure_acceptance_check.py` green (extended, never deleted); mirror: `.specify/scripts/python/closure-acceptance-check.py` (that pair is `STRICT` — an extra mirror-only file fails `--check`)
- [ ] T009 [US2] [blockedBy: T003,T004,T006,T007,T008] Regenerate every touched mirror and per-tool copy — `python3 scripts/python/sync-mirrors.py` then `--check` exit 0, `python3 scripts/python/regen-command-copies.py` then `--check` exit 0 (no command template is edited by this slice, so that leg is a parity re-assertion) — and, with the reason stated inline, re-read the frozen guards this slice's files move before declaring parity: `tests/contract/test_expression_gates_doc.py` (eight-stage coverage, no empty operator cell, the blocking faces) and `tests/contract/test_premise_carrier_contract.py` (the Environment Prerequisites carrier rule); never edit a `.specify/` copy by hand as the primary change (GW-11, GW-12, GW-13; FR-024)

**Checkpoint**: the schema has one owner and one skeleton, the four findings fire from both producers on both fixtures, and no fifth class exists.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Close the slice on recorded evidence, keep the parent's `in-scope` duty true after this file replaces 081a's, and state SC-005 exactly as far as the evidence reaches.

- [ ] T010 [blockedBy: T005,T009] Update SC-005's row in `.specify/specs/081-acceptance-hardening/verification.md` to exactly what the evidence supports, with the five `SC-005_`-prefixed ladder fields when the status is not `pass` — name the four findings (4/4 through both producers), the `in-scope` three duties for `RS-004` (`FR-005` defined, quoted by this file's T011 row, joint-acceptance row present — 3/3), the two plan tables and the 8/8 disposition rate, and the carrier readings: IB-006 and IB-007 resolve to `tests/contract/test_acceptance_premises.py`, while IB-004's carrier is 081c's module and therefore resolves only when 081c lands, so the honest value is a precise `partial` naming that remainder rather than a `pass`; leave SC-001 `blocked` and SC-002 `partial` unchanged (this slice adds no call site); then re-run `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/081-acceptance-hardening --json-out .specify/.tmp/081b-closure-verdict.json` and **copy** the acceptance summary block from that payload — the counts are computed once by the checker and never recomputed here (C-08)
- [ ] T011 [blockedBy: T008] Preserve 081a's smoke evidence as `.specify/specs/081-acceptance-hardening/test-evidence/smoke-081a.txt`, then re-run the feature's single smoke command (FR-005) twice — `bash scripts/bash/run-tests.sh tests/integration/test_acceptance_smoke.py -q` — and record both exit codes plus the refreshed `.specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt` content in `notes/red-first-evidence-081b.md`; the smoke must be re-run rather than inherited because this slice edits `scripts/python/closure-acceptance-check.py`, one of its three sub-checks, and because this row is what keeps `RS-004`'s "a `tasks.md` row quotes that FR" duty true after this file replaced `tasks-081a.md`; SC-008 stays `partial` (its final claim is 081d's)
- [ ] T012 [blockedBy: T005,T009,T010] Close the slice on recorded verification: run `bash scripts/bash/run-tests.sh tests/contract/test_acceptance_premises.py tests/contract/test_closure_acceptance_check.py tests/contract/test_expression_gates_doc.py tests/contract/test_expression_gate_wiring.py tests/contract/test_premise_carrier_contract.py -q` and write the console output to `.specify/specs/081-acceptance-hardening/test-evidence/tasks-081b-slice-tests.txt`; no full-suite run in this slice — the feature-level id-level baseline comparison is 081d's (FR-023), and this slice's narrower observation MUST NOT stand in for it

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: starts immediately; its two rows write disjoint paths
- **Phase 2 (Foundational)**: T003 and T004 block every US2 row — T003 owns the schema the tests judge against, T004 owns the skeleton that must not carry it
- **Phase 3 (US2)**: after Phase 2. T005 first (red), then T006 → T007, and T008 in parallel with T006/T007 once T005 exists; T009 collects every source edit and runs last in the phase
- **Phase 4 (Polish)**: after Phase 3; T010 needs the checker and the regenerated tree, T011 needs T008's checker, T012 needs the tests and T010's verification row

### User Story Dependencies

- **US2 (P1)**: no dependency on another story — 081b is the US2 slice; US1's shared core closed in 081a and is consumed, not rebuilt

### Within This Slice

- Tests MUST fail before the implementation rows that answer them close — T005 precedes T006 and T008
- Owner doc → plan skeleton → fixtures-driven findings → gate rows → closure-checker extraction → regeneration
- Polish rows record readings; they never re-derive a count the checker owns

### Parallel Opportunities

- Phase 1: T001 and T002 run in parallel (disjoint path sets)
- Phase 3: T006 and T007 touch different files and can be sequenced in either order after T005; T008 needs T001's fixtures and T005's assertions but not T006's code, so it can run beside them

---

## Parallel Example: User Story 2

```bash
# Launch the fixture authoring and the evidence sink together:
Task: "author premise-mutation and runtime-gap-mutation fixtures in tests/fixtures/acceptance-hardening/"
Task: "open the red-first landing point at notes/red-first-evidence-081b.md"
```

---

## Implementation Strategy

### MVP First

**MVP scope**: US2 alone — it is the whole of slice 081b. It is independently testable through the two mutation fixtures plus the contract module, and it is what makes the parent's SC-005 measurable instead of aspirational.

### Incremental Delivery

1. Phase 1 → fixtures exist, nothing claims anything yet
2. Phase 2 → the schema has exactly one owner and one skeleton
3. Phase 3 → the four findings fire, from two producers, under one closed set
4. Phase 4 → the slice's claims are written down at the strength the evidence supports

---

## Slice Boundary

**Slice**: `081b` — plan.md § D10 "US2 — runtime stack, execution premises, inherited blockers, the four `pre-analyze` findings, the A13 boundary". Boundaries are cut at plan entry; **no requirement is dropped**, each FR and SC below is assigned to exactly one slice.

### FR / SC coverage in this slice

| FR / SC | 081b status | What 081b delivers | Remainder and owner |
|---|---|---|---|
| FR-009 (runtime-stack table + `in-scope` three duties) | **covered** | the table itself was authored in the parent requirements at requirements stage; 081b lands the **judged** form: duties ① (input error), ② and ③ (one reason) are asserted by `tests/contract/test_acceptance_premises.py` and enforced by both producers, and the prose-only declaration is caught inside the same class | — |
| FR-010 (Execution Premises) | **covered** | owner § Execution Premises (columns, closed `Status`, `Decision` domain, the FR-cites-a-premise duty, the "no out-of-scope parking" rule) + the plan skeleton + the `falsified`-without-`Decision` finding | — |
| FR-011 (Inherited Blockers + carrier obligation) | **covered** | owner § Inherited Blockers (locator, three dispositions, the carrier requirement and its eligibility rule, the declared-dependency-set rule) + the plan skeleton + the undisposed finding, with undeclared/blank/unresolvable/deferrable carriers judged under the one reason | — |
| FR-012 (four closed findings) | **covered** | four findings in `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py`, surfaced by the existing `G-req-clarity` / `G-plan-fact` rows; the `in-scope` task/joint-acceptance duties and the `inherited` carrier rule are **absorbed**, so the count stays four and the reason set stays seven | — |
| FR-006 (closure checker) | **completed from `partial`** | the C-17 dependency-feature extraction, the carrier eligibility rule and the `signed-contract` contract-path check land here; the verdict surface, exit tri-state and single `final_path` computation were 081a's | `--audit-existing` → **081d** (unchanged, still an explicit not-implemented exit 2) |
| FR-019 (the four `blocked` literals reconciled once) | **not touched** | — | **081d** |
| FR-022 (single schema owner) | **partial** | the two remaining schema sections land in the one owner doc, and the plan skeleton reaches them by pointer | owner pointers across the command/skill surfaces, `CHANGELOG.md`, docs → **081d** |
| FR-023 (tests + baseline compare) | **partial** | this slice's new module joins the suite; the pin re-read before any comparison is asserted as an input-error rule | the feature-level id-level id diff over the final tree → **081d** |
| FR-024 (source not mirror) | **covered for 081b's edits** | every edit lands in `shared/`, `templates/`, `skills/` or `scripts/`, then T009 regenerates both surfaces | later slices repeat the rule for their own edits |
| FR-025 (registration + deterministic-only gates) | **covered** | all four findings are program verdicts; the new fixtures live under the already-registered `tests/fixtures/`; temp artifacts go to `.specify/.tmp/` | — |
| SC-005 (ownership + premises are first-class artifacts) | **partial, precisely** | four findings caught 4/4; `in-scope` duties 3/3 for `RS-004`; both plan tables present with 8/8 dispositions; carrier readings 2 of 3 resolvable | **IB-004's carrier is 081c's module** (`tests/contract/test_acceptance_review_composition.py`), so the carrier measure resolves at 081c and is re-read at line closure in 081d — this is why the row reads `partial`, not `pass`, and why T010 records that remainder instead of claiming it |
| SC-001 (3/3 call sites refuse the 026 shape) | **unchanged — `blocked`** | no call site added | review site → **081c**, driver closure/merge site → **081d** |
| SC-002 (positive path not killed; smoke is a hard condition) | **unchanged — `partial`** | no call site added; the smoke is re-run (T011) but the review-site leg is untouched | fourth-condition leg at the review site → **081c** |
| SC-008 (smoke record present and reproducible) | **unchanged — `partial`** | the smoke is re-run twice on this slice's tree and its evidence refreshed | the final claim over the 081d tree |
| SC-003, SC-004, SC-006, SC-007, SC-009 | **not touched** | — | 081d / 081c / 081d / 081d / 081d |

### Status consequence (load-bearing — do not soften)

**After 081b the feature is still `Blocked`, and this slice MUST NOT move it.** SC-001 and SC-002 are the parent's two `final`-path criteria; 081b adds no call site and turns neither to `pass`, `Blocked → Ready for Review` is illegal by design, and 081c / 081d own the two remaining call sites. Consequently:

- no artifact of this slice may read as `Implemented`, and GATE-6 asserts the registry still prints ` Blocked `
- SC-005 moves from `deferred` to a **precise `partial`** — the four findings, the `in-scope` three duties and the disposition rate are measured here, while one `inherited` carrier cannot resolve before 081c exists; claiming `pass` would be the same class of overstatement this feature exists to catch
- SC-001 stays `blocked` and SC-002 stays `partial` — a slice that re-runs a smoke does not thereby satisfy a criterion about call sites

## Deferred Slices

Not tasks. Listed so nothing is silently dropped and so `/speckit.tasks` for those slices starts from the plan's D10 scope.

- **081c — US3, review composition and ARC** (plan § D10: the `review-feature-quality` skill, review-template slots `### 2.2`–`### 2.4`, the `templates/commands/review.md` composition rewrite, ARC, the feedback census 3→4 plus its guard, the checker at the **review** call site, and FR-013's expected-artifact denominator). Its row set MUST name `tests/contract/test_acceptance_review_composition.py` and the deliberate updates of `tests/contract/test_review_code_composition.py`, `tests/contract/test_review_feedback_boundary.py` and `tests/contract/test_status_gate_owner.py`. It also closes IB-004's carrier: `tests/contract/test_acceptance_review_composition.py` is the module this slice's T010 names as the unresolved remainder.
- **081d — US4 and all remaining wiring** (plan § D10: the two remaining vocabulary owners, `--audit-existing` and its `audit-history` fixture, driver line state `blocked` with A6's eight dispositions, the closure/merge call site at the **feature line's closure**, mirrors, docs / `CHANGELOG.md`, the final smoke claim and the feature-level baseline re-run). Its row set MUST name `tests/contract/test_acceptance_schema_ownership.py` (SC-009 ④) and `tests/contract/test_line_state_blocked.py` (A6's eight items). It is also where the schema-owner pointers of FR-022 and the `CHANGELOG.md` entry land.

## Notes

- `[P]` rows write disjoint path sets; any row that writes a file another row also writes carries no `[P]` and an explicit `[blockedBy:]`
- Two Hats: every edit lands in `shared/`, `templates/`, `skills/` or `scripts/`; `.specify/` copies are regenerated by T009, never hand-edited. Exact pairs: plan.md § Mirror Obligations
- **One closed set, two producers**: the closure checker and the pre-analyze gate both emit `runtime-dependency-not-owned` / `falsified-premise-undecided` / `inherited-blocker-undisposed`. That is accepted (the literals' owner is `requirements.md` § Shared Strings, and the reasons must be emittable at both a stage gate and a closure gate), and T005's cross-producer agreement leg is what keeps the two from drifting into two spellings
- **Four, not five**: the `in-scope` task/joint-acceptance duties ride the runtime-row class and the `inherited` carrier rule rides the blocker class. A fifth finding class, or an eighth reason, is a defect of this slice, not a feature request
- The parent's own two tables already exist in `plan.md` and are **not** re-authored here: § Execution Premises (EP-001…EP-009) and § Inherited Blockers (IB-001…IB-008). This slice gives them a schema owner and a plan-time skeleton, and proves the rules on fixtures — a second copy of those tables in a slice artifact is the exact defect A13 forbids
- The feature-level id-level baseline comparison is **not** run in this slice; T012's narrower observation is recorded as narrower
- Deferral discipline: prefer `[~]` with a recorded reason over leaving a row `[ ]`
