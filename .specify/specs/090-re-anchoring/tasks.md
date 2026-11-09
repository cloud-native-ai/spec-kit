# Tasks: Re-Anchoring（不忘初心 · 温故而知新）

**Requirement ID**: 090
**Requirement Key**: 090-re-anchoring
**Related Feature**: 090 Re-Anchoring（不忘初心 · 温故而知新）
**Input**: Design documents from `.specify/specs/090-re-anchoring/`
**Prerequisites**: requirements.md (10 FR / 4 SC, clarify settled 2026-11-09), plan.md (T-001/T-002, EP-001…EP-004, D-1…D-6), research.md (R1…R9), data-model.md (E-1…E-6 / V-1…V-12), contracts/ (re-anchoring-faces C-1…C-8, direction-audit C-1…C-9, governance-landing C-1…C-6, guard-tests C-1…C-8), quickstart.md (S-0…S-6), feature-ref.md

**Tests Mode**: ON — Constitution Principle IV "Test-First & Contract-Driven Implementation" is test-mandating, and this feature's whole verification surface is contract guards over governance artifacts (Constitution Check row IV is the one Partial row, carried by `guard-tests.contract.md` C-7 with a red-first obligation). Every guard row lands BEFORE the implementation row that turns it green; verification rows that only read an existing guard sit AFTER it and carry `[blockedBy:]`.

**Repair provenance**: this file, the four `contracts/` pages, `research.md` R9 and `feature-ref.md` F-1/F-2 were repaired at the analyze gate on 2026-11-09 against the analyze report's three HIGH findings — F-01 (T032's citation move would have emptied the FR lane and made DoD-1 unreachable), F-02 (two mis-assigned `[green:]` groups with no exported partition) and F-03 (DoD-1 and DoD-2 demanding completeness over one clause space under two readings) — and the MEDIUM F-05 recovery (T039). Requirements and plan bodies were not edited.

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
| 6 Polish | the carried rulings, the FR citation groups, the mirror sweep, the resolved markers | T030–T039 | FR-010, closure |

## Definition of Done (DoD)

- DoD-1: **FR lane** — every FR-001…FR-010 is cited from the citation group of at least one clause block **on the page that truly carries it** (§ FR → citation group), so the accountant's FR lane reads no uncovered FR. Check: `/usr/bin/python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/090-re-anchoring --json` reports `fr.uncovered == []` (`10 of 10`). This lane is a set relation over citation groups and is **disjoint** from DoD-2: an FR is never a legal `[green:]` target — the FR lane reads citation groups only, never task rows (engine docstring, head of `account-clause-coverage.py`).
- DoD-2: **clause lane** — every contract clause of the four pages is claimed exactly once by a `[green:]` tag on a row that names the file it writes: `re-anchoring-faces` C-1…C-8, `direction-audit` C-1…C-9, `governance-landing` C-1…C-6, `guard-tests` C-1…C-8 (31 clauses, 31 claims, 0 duplicates). Check: `/usr/bin/python3 .specify/scripts/python/validate-tasks.py .specify/specs/090-re-anchoring/tasks.md` prints `0 error(s), 0 warning(s)` (zero `green-dangling`, `green-clause-collision`, `green-cross-phase`) **and** the § Green Partition table is reproduced exactly from the rows of this file. Only 5 of this file's 38 rows carry a `[green:]` tag, and none of those five is a citation-group row: one row may claim several clauses of one page, and the other 23 rows turn nothing green.
- DoD-3: `guard-tests.contract.md` C-7 is closed: one test function asserts the rule-first ordering, reds on all three stated mutations, and the landed-pass / mutated-fail pair is captured in `test-evidence/`.
- DoD-4: The four named guard modules carry zero NEW failures against the frozen baseline — `test_reanchoring_contract.py` 4 passed, `test_sdd_loop_driver_reanchor.py` 5 passed after the new row, `test_constitution_double_landing.py` 19 passed, `test_fast_fail_discipline.py` 104 passed 2 failed (both pre-existing, see § Environment Prerequisites).
- DoD-5: Every mirror obligation of `plan.md` § Mirror Obligations holds — `sync-mirrors.py --check` exits 0 with all six pairs byte-identical, including the protocol pair the ordering guard reads.
- DoD-6: SC-001…SC-004 each carry a `test-evidence/` file whose command and reading were produced in this feature's run, and no `final`-path criterion is left in `blocked` / `deferred` / `fail` without an explicit waiver.
- DoD-7: Every ruling this stage had to make is disclosed in § Notes — never folded silently into green.

**DoD Status**: pending

**DoD ↔ GATE consistency (re-checked at the analyze repair, 2026-11-09)**: each DoD item names exactly one check and exactly one code path, and each GATE runs that same path, so no pair can disagree. DoD-1 ↔ GATE-6 (`account-clause-coverage.py --json` → `fr.uncovered == []`); DoD-2 ↔ GATE-6 (`validate-tasks.py` → `0 error(s), 0 warning(s)` plus the § Green Partition export); DoD-3 ↔ GATE-2 (`ordering-red-control.txt`, four arms); DoD-4 ↔ GATE-1 (the four modules against `tasks-baseline-failed.txt`); DoD-5 ↔ GATE-3 (`sync-mirrors.py --check` exit 0); DoD-6 ↔ GATE-5 (`verification.md` readings); DoD-7 is a disclosure duty with no machine check, and § Notes is where it discharges. The former contradiction — DoD-1 and DoD-2 demanding completeness over the *same* clause space under two incompatible readings — is gone because the two lanes now have disjoint universes: clause groups for DoD-1, `[green:]` tags for DoD-2.

## Completion Gate

- GATE-1: No NEW failures in the four named guard modules versus the frozen baseline — check: `SPECKIT_PYTHON=/usr/bin/python3 /usr/bin/python3 -m pytest tests/contract/test_reanchoring_contract.py tests/contract/test_sdd_loop_driver_reanchor.py tests/contract/test_constitution_double_landing.py tests/contract/test_fast_fail_discipline.py -q --tb=no -rA` and compare the `FAILED` node ids against `.specify/specs/090-re-anchoring/test-evidence/tasks-baseline-failed.txt` with `LC_ALL=C comm -13` printing nothing.
- GATE-2: The ordering guard reds when the protocol is reverted to goal-first — check: `.specify/specs/090-re-anchoring/test-evidence/ordering-red-control.txt` holds one landed-pass arm and three mutant-fail arms.
- GATE-3: Every mirror obligation from `plan.md` § Mirror Obligations is byte-identical — check: `/usr/bin/python3 scripts/python/sync-mirrors.py --check` exits 0.
- GATE-4: No open task rows — check: `grep -cE '^- \[[ >]\]' .specify/specs/090-re-anchoring/tasks.md` returns 0.
- GATE-5: Every `final`-path success criterion is `pass` **and** the feature's smoke record is present — check: in `.specify/specs/090-re-anchoring/verification.md`, every criterion whose `**Path**` marker reads `final` has `SC-NNN_status=pass`, and `smoke_command=`, `smoke_exit_code=0` and `smoke_evidence_path=` (a path that exists and is non-empty) are all present; a `final`-path criterion in `blocked` / `deferred` / `fail` fails this gate unless an explicit user waiver names that criterion. Condition set owner: `shared/workflow/acceptance-hardening.md` § Gates — this row carries the check, not a second schema.
- GATE-6: Structure and clause accounting are silent, and the FR lane is empty — check: `/usr/bin/python3 .specify/scripts/python/validate-tasks.py .specify/specs/090-re-anchoring/tasks.md` exits 0 with `0 error(s), 0 warning(s)` (a `green-*` warning is a clause-lane failure, not noise); then `/usr/bin/python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/090-re-anchoring` exits 0, which it only does when `coverage-baseline-delta` holds **and** the FR lane is empty — the clause lane's baseline-internal residual (598 names now, all belonging to other specs) is reported, never repaired here, because the frozen baseline excludes this feature's own clauses by construction (§ Notes F-6).

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
- **[green: <contract>#<clause>]**: this row is the one that turns that clause green. Contract paths resolve relative to this file's own directory first; every row below cites the `contracts/<page>.md` form for that reason. One CLAIM per clause — not one row per clause: the 31 clauses of the four pages are claimed exactly once across **five** rows (T006, T014, T019, T020, T032), and § Green Partition is the mechanical export of that mapping.
- **Two disjoint lanes**: a `[green:]` tag covers the **clause** lane (DoD-2); an FR is covered by the **citation group** of a clause block inside the contract page (DoD-1), never by a tag on a row. Writing a citation group and claiming a clause are two different edits on two different files, which is why they are two rows (T032 and T033).
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
| FR coverage from contract citation groups | **10 of 10 now** (was **0 of 10** at generation time) | `account-clause-coverage.py --spec-dir .specify/specs/090-re-anchoring --json` → `fr.claimed=10`, `fr.uncovered=[]`; the generation-time reading was `claimed=0`, `uncovered=['FR-001'…'FR-010']` | reading each page's introduction line as a citation — the owner's rule § 4.2 puts the citation group inside a clause block, and the introduction line is not one; § FR → citation group is the mapping T032 lands |
| Contract clauses in the four pages | **31** (`re-anchoring-faces` 8, `direction-audit` 9, `governance-landing` 6, `guard-tests` 8) | `clause_extract.extract_clauses()` per page; `form_of()` → `md-heading` on all four **at generation time**, re-measured `md-bold-closed` after the analyze repair of 2026-11-09 canonicalised them (ids unchanged at 31) | `grep -c 'C-'` anywhere over-counts (the pages cross-reference each other's clauses); `grep -c '^## C-'` agreed at 31 before the repair and now returns 0, which is why the id set — not a grep form — is the reading |
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


## Green Partition (clause lane, mechanically exported)

The single export of every `[green:]` tag in this file, produced by parsing this file's own rows with `[green: <page>#<clause>]` and collapsing each page's claims into a contiguous range. It is a **derived view, never a second authority**: if this table and the rows disagree, the rows win and this table is stale. Re-derive with a one-line program over the rows; never hand-edit a cell to make it agree.

| Row | Clauses it claims | Claims |
|-----|-------------------|--------|
| T006 | re-anchoring-faces C-1 | 1 |
| T007 | re-anchoring-faces C-2 | 1 |
| T008 | re-anchoring-faces C-3 | 1 |
| T009 | re-anchoring-faces C-4 | 1 |
| T010 | re-anchoring-faces C-5 | 1 |
| T011 | re-anchoring-faces C-6 | 1 |
| T012 | re-anchoring-faces C-7 | 1 |
| T013 | re-anchoring-faces C-8 | 1 |
| T014 | direction-audit C-1–C-3, guard-tests C-1–C-4 | 7 |
| T019 | direction-audit C-4–C-6 | 3 |
| T020 | direction-audit C-7–C-9 | 3 |
| T022 | governance-landing C-1–C-2 | 2 |
| T023 | governance-landing C-3 | 1 |
| T024 | governance-landing C-4 | 1 |
| T025 | governance-landing C-5 | 1 |
| T026 | governance-landing C-6 | 1 |
| T031 | guard-tests C-5 | 1 |
| T032 | guard-tests C-6 | 1 |
| T033 | guard-tests C-7 | 1 |
| T036 | guard-tests C-8 | 1 |
| T039 | — (no green: a resolved-marker closure row) | 0 |
| **Total** | 20 claiming rows (T039 is listed to show it claims none), 4 pages, every clause once | **31** |

Recomputation line: `20 rows + 31 claims + 4 pages` — the row count, the claim count and the page count are each read off this file, and `31` must equal the sum of the four pages' clause counts (8 + 9 + 6 + 8). A row that claims nothing appears in no line of this table; that is 19 of the file's 39 rows, not an omission.

**Why each page's claims land where they do** (the F-02 repair, recorded as the reason rather than as a rule):

- `direction-audit` C-1…C-3 are **presence propositions** about the protocol's own text (a mandatory fifth part, the minimal shape carrying it, the primary object being the rules). The row that turns them green is the one that writes the guard reading that text — T014, the ordering test, which is also the first row in the file that asserts anything about the protocol. They are **not** claimed by T020 (an evidence-synthesis row that writes `sc002-ordering.txt` and lands no assertion).
- `direction-audit` C-4…C-6 are **text propositions about the protocol as it is landed** — Q1 asks the rules and names the eight-rule set, the verdict is one of three values, and rule verdict plus licensed action precede any goal statement. Their green point is the row that verifies the protocol against them and records path and line: T019.
- `direction-audit` C-7 (the audit is a statement, never an approval request), C-8 (the reload is tiered and bounded) and C-9 (repeated drift escalates) are the clauses whose evidence is assembled end to end by T020; no earlier row measures them.

## FR → citation group (FR lane)

The FR lane's mapping, one row per FR, each naming **the page and clause block that truly owns the proposition** — not the page whose introduction mentions the number (owner: `shared/definitions/contract-clause-definitions.md` § 4.2; § Notes F-7). A page-introduction line is a *mention* and never satisfies DoD-1.

| FR | Proposition | Page | Clause block | Co-cited with |
|----|-------------|------|--------------|---------------|
| FR-001 | One owner document owns the two concepts, the tiers and the agent obligation, and introduces no machinery | `contracts/re-anchoring-faces.contract.md` | C-1, C-8 | — |
| FR-002 | The same principle title lands on both constitution surfaces | `contracts/re-anchoring-faces.contract.md` | C-3 | `governance-landing` C-1 |
| FR-003 | Both instruction surfaces carry the ambient section and the owner pointer | `contracts/re-anchoring-faces.contract.md` | C-4 | — |
| FR-004 | The anchor carries the task anchor **and** the rule anchor | `contracts/direction-audit.contract.md` | C-4 (the rule set named inline) | — |
| FR-005 | The five questions are rules-first, with the verdict preceding any goal restatement | `contracts/direction-audit.contract.md` | C-6 | — |
| FR-006 | The reload is tiered T0/T1/T2 and no full reload runs per tool call | `contracts/direction-audit.contract.md` | C-8 | — |
| FR-007 | The audit is a statement, never an approval request; only `decision-needed` is surfaced | `contracts/direction-audit.contract.md` | C-7 | — |
| FR-008 | `agent-definitions.md` declares the agent-side obligation and the brief carries the anchor | `contracts/re-anchoring-faces.contract.md` | C-5 | — |
| FR-009 | The generator's MUST-include list gains the principle | `contracts/re-anchoring-faces.contract.md` | C-6 | `governance-landing` C-3 |
| FR-010 | The counting pins move in the same batch, guarded | `contracts/governance-landing.contract.md` | C-4 | `guard-tests` C-1, C-2, C-8 |

Ten FRs, ten distinct `(FR, page, block)` targets, of which FR-002, FR-009 and FR-010 are cited twice because each proposition lands on two surfaces. Nothing in this table is a `[green:]` tag and no row claims an FR: this is the lane DoD-1 measures and the five claim rows never touch it.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: freeze the three baselines the closure rows are compared against and land the evidence landing points. Nothing here writes an artifact this feature is judged on.

- [X] T001 Create the evidence landing points for this stage and record the generation-time premises of § Premises measured at generation time in `.specify/specs/090-re-anchoring/test-evidence/tasks-premises.md`
- [X] T002 Capture the four named guard modules' pre-change node-id baseline into `.specify/specs/090-re-anchoring/test-evidence/tasks-baseline-failed.txt` with `/usr/bin/python3 -m pytest <the four modules> -q --tb=no -rA`, recording the exit code and the two pre-existing failures [blockedBy: T001]
- [X] T003 Capture the contract-suite collection reading into `.specify/specs/090-re-anchoring/test-evidence/tasks-collect.txt` with `/usr/bin/python3 -m pytest -m contract -q --collect-only` [blockedBy: T001]
- [X] T004 Capture the six-pair mirror baseline into `.specify/specs/090-re-anchoring/test-evidence/mirrors-tasks.txt` with `/usr/bin/python3 scripts/python/sync-mirrors.py --check`, which must read exit 0 with six `ok` lines [blockedBy: T001]
- [X] T005 Create the mutation-fixture root `.specify/specs/090-re-anchoring/test-evidence/tmp/.gitkeep` and assert the resolved path stays inside the sanctioned evidence dir, never under the system temp root (see § Environment Prerequisites) [blockedBy: T001]

**Checkpoint**: every closure row can name the baseline it is compared against, and the mutation root is proven writable on this host.

---

## Phase 2: SC-001 — the five rule faces exist and point at one owner

**Goal**: the owner page plus the five consumer faces (two constitutions, two instruction surfaces, one agent obligation) and the generator mandate entry simultaneously exist and cross-reference by pointer.
**Independent Test**: `pytest tests/contract/test_reanchoring_contract.py -q` → 4 passed on the landed tree, and each consumer's pointer resolves to the owner page's declared ownership.

- [X] T006 [SC-001] Verify the owner page `shared/definitions/re-anchoring-definitions.md` owns exactly the concept definitions, the reload tiers and the agent obligation, delegates the executable procedure to `skills/external/sdd-loop-driver/references/checkpoint-protocol.md` by path without restating it, and defines no store, ledger, score or schedule [green: contracts/re-anchoring-faces.contract.md#C-1]
- [X] T007 [SC-001] Verify the owner page `shared/definitions/re-anchoring-definitions.md` carries the two concepts, the rule anchor, the three tiers and the three verdict literals, recording path plus line anchors in `.specify/specs/090-re-anchoring/test-evidence/sc001-faces.txt` [blockedBy: T006] [green: contracts/re-anchoring-faces.contract.md#C-2]
- [X] T008 [SC-001] Verify both constitution surfaces carry the principle under one title with the permitted numeral difference and none of the other consumer obligations, appending path and line to `test-evidence/sc001-faces.txt` [green: contracts/re-anchoring-faces.contract.md#C-3]
- [X] T009 [SC-001] Verify both instruction surfaces carry the ambient section and the owner pointer, with the live file produced from the template by `scripts/bash/generate-instructions.sh`, appending path and line to `test-evidence/sc001-faces.txt` [green: contracts/re-anchoring-faces.contract.md#C-4]
- [X] T010 [SC-001] Verify the agent obligation section in `shared/definitions/agent-definitions.md` names the owner page, states the entry-restatement duty and the after-each-core-step rules-first duty, and states that the dispatcher carries the anchor summary into the brief, appending path and line to `test-evidence/sc001-faces.txt` [green: contracts/re-anchoring-faces.contract.md#C-5]
- [X] T011 [SC-001] Verify `skills/internal/manage-constitution/SKILL.md` carries the principle as a sub-entry inside its MUST include block with the owner pointer, appending path and line to `test-evidence/sc001-faces.txt` [green: contracts/re-anchoring-faces.contract.md#C-6]
- [X] T012 [SC-001] Verify every consumer face named by T008…T011 points at the owner instead of restating its tier table or question list, appending the per-face judgment to `test-evidence/sc001-faces.txt` [blockedBy: T008,T009,T010,T011] [green: contracts/re-anchoring-faces.contract.md#C-7]

**Checkpoint**: each of the four face-guard assertions is attributed to a landed face, and no consumer restates the owner's content.

---

## Phase 3: SC-002 — the rule-first ordering gap closed red-first (guard-tests C-7)

**Goal**: one test function in `tests/contract/test_sdd_loop_driver_reanchor.py` asserts that the audit asks the RULES first and states the rule verdict before any goal restatement, and reds when the protocol is reverted to goal-first.
**Independent Test**: on the landed protocol the new test passes; on the `Q1`-reworded copy, on the minimal-shape reword and on the primary-object-reworded copy it fails — four arms in one captured evidence file.

- [X] T013 [SC-002] Record the red-first capture into `.specify/specs/090-re-anchoring/test-evidence/red-first-090-c7.txt`: run the four named modules before any edit and record the reading proving no ordering assertion exists today (the modal module holds 4 tests, none ordering) [blockedBy: T002] [green: contracts/re-anchoring-faces.contract.md#C-8]
- [X] T014 [SC-002] Add the ordering guard to `tests/contract/test_sdd_loop_driver_reanchor.py` as exactly one test function asserting, inside the protocol's direction-audit block, that the rules-first statement is present, that the first of the five questions asks which rules govern the step, and that in the minimal shape the first question line is the rules line, so a goal-first rewrite fails on all three legs, and stating that the rule verdict precedes the goal restatement with the goal implicit in the third question [blockedBy: T013] [green: contracts/guard-tests.contract.md#C-1] [green: contracts/guard-tests.contract.md#C-2] [green: contracts/guard-tests.contract.md#C-3] [green: contracts/guard-tests.contract.md#C-4] [green: contracts/direction-audit.contract.md#C-1] [green: contracts/direction-audit.contract.md#C-2] [green: contracts/direction-audit.contract.md#C-3]
- [X] T015 [SC-002] Confirm the four pre-existing tests of `tests/contract/test_sdd_loop_driver_reanchor.py` carry only structural assertions and that the face guard carries only presence and pointer assertions, so no green of either is read as ordering evidence [blockedBy: T014]
- [X] T016 [SC-002] Mutate a copy under `.specify/specs/090-re-anchoring/test-evidence/tmp/` by replacing `1. Which rules govern this step` with `1. Which goal governs this step`, run the module against the copy, assert the new test FAILS, and record raw output in `.specify/specs/090-re-anchoring/test-evidence/ordering-red-control.txt` [blockedBy: T014]
- [X] T017 [SC-002] Mutate a second copy by replacing the minimal shape's first question label with a goal label, run the module, assert the new test FAILS, and append raw output to `test-evidence/ordering-red-control.txt` [blockedBy: T016]
- [X] T018 [SC-002] Mutate a third copy by rewording the primary-object sentence to name the goal instead of the rules, run the module, assert the new test FAILS, and append raw output to `test-evidence/ordering-red-control.txt` [blockedBy: T017]
- [X] T019 [SC-002] Verify the landed checkpoint protocol against its audit contract — mandatory fifth part plus the protocol's own defect rule, the first question naming the eight rules inline, exactly three verdict values with only the surfaced one surfaced, the primary-object statement giving the rules as the audit object with its reason **and stating that the rule verdict and the action it licenses precede any goal statement, with the goal implicit in Q3 rather than asked**, the no-question-to-the-user prohibition mirrored in the driver Hard Requirements block, the tier triggers with the full-reload ban and its reason — recording path and line numbers in `test-evidence/sc004-tiers.txt` [green: contracts/direction-audit.contract.md#C-4] [green: contracts/direction-audit.contract.md#C-5] [green: contracts/direction-audit.contract.md#C-6]
- [X] T020 [SC-002] Verify the ordering proposition end to end and record the landed-versus-mutated pair as SC-002's evidence in `.specify/specs/090-re-anchoring/test-evidence/sc002-ordering.txt`, citing the four arms and the self-falsifying premise that both former greens still pass on a goal-first rewrite [blockedBy: T016,T017,T018] [green: contracts/direction-audit.contract.md#C-7] [green: contracts/direction-audit.contract.md#C-8] [green: contracts/direction-audit.contract.md#C-9]
- [X] T021 [SC-002] Record the red-when-broken obligation for every clause the guard suite asserts — deleted surface, renamed title, dropped part, mutated order — in `.specify/specs/090-re-anchoring/test-evidence/guard-red-controls.txt`, naming the demonstrated failure mode per clause [blockedBy: T016]

**Checkpoint**: SC-002 is satisfiable from the tree alone — the ordering assertion exists, its red control is captured, and no green cited for it predates it.

---

## Phase 4: SC-003 — the count pins and their guards agree with the artifacts

**Goal**: the double-landing pins (21 / 22 / 14), the nine-entry watchlist and the fast-fail guard's entry-length pin agree with the counts the guard derives independently.
**Independent Test**: `pytest tests/contract/test_constitution_double_landing.py -q` → 19 passed, and the fast-fail watchlist guard reports 9 entries with the newest one a template title.

- [X] T022 [SC-003] Verify the one-title landing on both constitution surfaces, the Sync Impact Report naming the amendment with its version change and Last Amended date, and that no dated record or past checkpoint was rewritten, recording paths and line numbers in `.specify/specs/090-re-anchoring/test-evidence/sc003-counts.txt` [green: contracts/governance-landing.contract.md#C-1] [green: contracts/governance-landing.contract.md#C-2]
- [X] T023 [SC-003] Verify `skills/internal/manage-constitution/SKILL.md` gained exactly one mandate sub-entry for the principle, appending the block reading to `test-evidence/sc003-counts.txt` [blockedBy: T022] [green: contracts/governance-landing.contract.md#C-3]
- [X] T024 [SC-003] Verify the three count pins and the watchlist entry against the artifacts they describe — template principles, live principles, mandate entries, watchlist last entry equal to the template title — recording both the literal and the derived reading in `test-evidence/sc003-counts.txt` [blockedBy: T023] [green: contracts/governance-landing.contract.md#C-4]
- [X] T025 [SC-003] Verify the fast-fail guard pins the watchlist length at its new value and asserts the newest entry is a template title, appending the reading to `test-evidence/sc003-counts.txt` [blockedBy: T024] [green: contracts/governance-landing.contract.md#C-5]
- [X] T026 [SC-003] Verify the incident the discipline answers is cited rather than rewritten on both the owner page and the protocol, appending the citation readings to `test-evidence/sc003-counts.txt` [blockedBy: T025] [green: contracts/governance-landing.contract.md#C-6]

**Checkpoint**: SC-003 is decidable by two independent measurements that agree, and neither is a restatement of the other.

---

## Phase 5: SC-004 — the reload tiers agree across the owner page and the protocol

**Goal**: the three reload tiers carry the same triggers and the same cost shape in the owner page and in the protocol, and the anchor they load carries both halves.
**Independent Test**: the tiers-bounded guard passes and the two documents' tier rows agree when read against each other line by line.

- [X] T027 [SC-004] Verify the tier agreement by reading the owner page's tier table against the protocol's tier bullet, recording both sides' paths and line numbers plus any legitimate asymmetry in `.specify/specs/090-re-anchoring/test-evidence/sc004-tiers.txt` [blockedBy: T019]
- [X] T028 [SC-004] Verify the anchor carries both halves and is persisted in the spine or the brief, never conversation-only, recording the carrier for each half in `test-evidence/sc004-tiers.txt` [blockedBy: T027]
- [X] T029 [SC-004] Verify the four-kind core-step set is closed and that the tier is chosen by position rather than preference, appending the reading to `test-evidence/sc004-tiers.txt` [blockedBy: T028]

**Checkpoint**: SC-004 holds in both directions — neither side adds a tier the other lacks.

---

## Phase 6: Polish — the carried rulings and the closure ledger

**Purpose**: give the rulings the plan carried an explicit outcome, land the FR citation groups and the canonical clause form, and run the closure sweep.

- [X] T030 Verify the assertions themselves are falsifiable as a set: re-run the four named modules, inject each clause's failure mode in a scratch copy, and assert the corresponding assertion reds, appending the per-clause arm to `.specify/specs/090-re-anchoring/test-evidence/guard-red-controls.txt` [blockedBy: T021]
- [X] T031 Verify the four guard modules are pure reads — no subprocess, no write, no network — by reading each module's imports and calls, appending the reading to `test-evidence/guard-red-controls.txt` [blockedBy: T030] [green: contracts/guard-tests.contract.md#C-5]
- [X] T032 Add, to **the clause block of the page that truly carries it** (§ FR → citation group), a trailing citation group `(FR-00N)` covering FR-001…FR-010 — ten groups over seven clause blocks: `contracts/re-anchoring-faces.contract.md` C-1 (FR-001), C-3 (FR-002), C-4 (FR-003), C-5 (FR-008), C-6 (FR-009), C-8 (FR-001); `contracts/direction-audit.contract.md` C-4 (FR-004), C-6 (FR-005), C-8 (FR-006), C-7 (FR-007); `contracts/governance-landing.contract.md` C-1 (FR-002), C-3 (FR-009), C-4 (FR-010); `contracts/guard-tests.contract.md` C-1 (FR-010), C-2 (FR-010), C-8 (FR-010) — adding **no** `[green:]` tag and moving `re-anchoring-faces` C-1…C-8, `direction-audit` C-7…C-9 and `guard-tests` C-1…C-2 out of no row (a citation is a property of the page, a claim is a property of a row; § Green Partition holds the latter unchanged), then record in `.specify/specs/090-re-anchoring/test-evidence/account-clause-coverage.txt` the command `/usr/bin/python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/090-re-anchoring --json` and the reading `fr.universe 10 / fr.claimed 10 / fr.uncovered []` [blockedBy: T012,T020,T026,T029] [green: contracts/guard-tests.contract.md#C-6]
- [X] T033 Convert the four contract pages' clause markers from the legacy heading form (`## C-N — title`) to the owner's canonical single-line form (`**C-N** — title`), asserting before and after that each page's extracted id set is identical (`clause_extract.py extract_clauses`, exit 0, 31 ids) and that the citation groups written by T032 survive the conversion (`clause_citations` maps the same ten FRs), then record both readings in `test-evidence/account-clause-coverage.txt` [blockedBy: T032] [green: contracts/guard-tests.contract.md#C-7]
- [X] T034 Freeze the coverage baseline by running `account-clause-coverage.py .specify/specs/090-re-anchoring --freeze` into `.specify/specs/090-re-anchoring/coverage-baseline.txt`, recording in § Notes that the freeze corpus and the live corpus differ (F-6) [blockedBy: T033]
- [X] T035 Re-run the accountant live against the frozen baseline and record the reading, the residual uncovered count and its cause in `.specify/specs/090-re-anchoring/test-evidence/account-clause-coverage.txt` [blockedBy: T034]
- [X] T036 Re-run the four named guard modules and diff the failed node ids against `test-evidence/tasks-baseline-failed.txt`, recording no-new-failure or the delta in `.specify/specs/090-re-anchoring/test-evidence/closure-guards.txt` [green: contracts/guard-tests.contract.md#C-8] [blockedBy: T014,T024]
- [X] T037 Re-run `/usr/bin/python3 scripts/python/sync-mirrors.py --check` after every edit of this stage and record the six-pair reading in `test-evidence/mirrors-tasks.txt`, treating new drift on those six pairs as a failure of this stage rather than of the tree [blockedBy: T036]
- [X] T038 Re-author `shared/definitions/re-anchoring-definitions.md` only if a row above measured a divergence from its own contract, and re-project the mirror with `sync-mirrors.py`; if no divergence is measured this row closes as a no-op citing that reading [blockedBy: T037]
- [X] T039 Close the two MEDIUM follow-ups this stage inherits by marking them **resolved** at their own owners (F-05 recovery): in `.specify/specs/090-re-anchoring/research.md` set R9's heading to `## R9 — … (RESOLVED 2026-11-09)` with the evidence pointer `requirements.md` SC-001…SC-004 all carrying an inline `**Path**: final` marker, and in `.specify/specs/090-re-anchoring/feature-ref.md` § 7 mark F-1 and F-2 resolved with the same evidence line, leaving their original text in place (a dated record is appended to, never rewritten) [blockedBy: T035]

**Checkpoint**: every carried ruling has an explicit outcome, the clause accounting is green against a frozen baseline, and the mirror pairs are byte-identical after the full sweep.

---

## Non-Disposable slice (092)

Appended from `.specify/specs/092-non-disposable/tasks.md` (T001…T158, all 158 rows, same order, same states) at the 092→090 merge, wave W3, seat M3. The 092 file is **not** deleted: it stays the original this slice was derived from, and this section is a **derived copy**, not a second authority for the 092 rows.

**The two mechanical edits, and nothing else**:
- **ID namespace**: every task id and every `[blockedBy:]` / prose cross-reference became `T<NNN>A` (`T001A`…`T158A`). `ND-T001` was the brief's first spelling, but `validate-tasks.py`'s `VALID_ID` is a closed `^T\d{3}[A-Za-z]?$`, so a two-letter prefix is a `row-format` error on all 158 rows; the single-letter suffix rides the declared optional-letter slot, keeps one id space, and shadows none of this file's own T001…T039.
- **Green-point namespace**: every `[green: contracts/<page>.contract.md#<clause>]` now reads `[green: contracts/nd-<page>.contract.md#<clause>]` — the merged clause namespace the W3 contract lane carries beside this file. Clause ids, task states, `[blockedBy:]` targets and row text are otherwise unchanged.

**Read caveat (disclosed, not repaired here; blocking for a closure reading)**: the `contracts/nd-*` pages this slice cites do not exist yet under `.specify/specs/090-re-anchoring/contracts/`, so `validate-tasks.py` reports each `nd-*` claim `green-dangling` until that lane lands them. Measured on this tree: **62 errors, 0 warnings — all 62 are that one pre-declared class**, every other check is silent. Retargeting at 092's own `contracts/` pages was rejected: it would leave a second clause namespace in this file after the merge, and `tasks.md` is not the shell that may decide which namespace the merged feature keeps.

**Phases keep the 092 heading text** (`## Phase N: Pn — …`), so the `order` rows are contiguous and `[blockedBy:]` targets always point backwards. No row above was re-ordered to fit this file's own Phase 1–6 headings.

**Checkpoint P1**: the owner page exists and declares what it owns; the fact loads through the single read entry; the
registry row says `Planned`; the eight decisions are registered; the corpus and the frozen baseline exist.

- [X] T001A Author § Status Readability of `shared/definitions/non-disposable-definitions.md` — the objects a status claim rests on (registry row; `verification.md` machine-block and smoke fields; `tasks.md` structure; decision-tension records), what makes each red, and the explicit statement that `requirements.md` `**Path**:` markers are judged by `validate-requirements.py`'s `path-marker` check and never by `status-unreadable` [green: contracts/nd-acceptance-readability.contract.md#C-801]
- [X] T002A Author the closed status × verdict contradiction table in `shared/definitions/non-disposable-definitions.md` § Status Readability — seven registry values (`Draft` / `Planned` / `Implemented` / `Blocked` / `Ready for Review` / `Completed`, plus `Relocated` excluded by name with its `count: 0` reason) crossed with `accept` / `block`, the reason code only on the two completion-claim cells, empty `reasons` plus `evidence_refs` on the rest, and the three prohibitions (unknown spelling exits 2; `Completed` / `Relocated` not out of scope beyond the named exclusion; a third verdict value fails the guard) [green: contracts/nd-acceptance-readability.contract.md#C-802]
- [X] T003A State in `shared/definitions/non-disposable-definitions.md` § Status Readability which corpus rows and fixture legs prove each cell — A3 for `Planned × accept`, A1 for `Implemented × block` and `Ready for Review × block`, a clash fixture and a separate consistent fixture for the rest — and that A3 MUST land red, not merely described [green: contracts/nd-acceptance-readability.contract.md#C-803]
- [X] T004A State in `shared/definitions/non-disposable-definitions.md` § Status Readability that a `requirements.md` success-criterion row carrying no `**Path**:` marker is reported by `scripts/python/validate-requirements.py`'s `path-marker` check — never by `status-unreadable` — and that the engine only carries that reading as an `evidence_refs` element [green: contracts/nd-acceptance-readability.contract.md#C-804]
- [X] T005A State the 档 II handoff marker's form (one line per receiving body, corpus id from the 档 II set, receiving feature from `plan.md` § Shift List), its count (`12` rows = `12` receiving bodies = `12` markers), and record in `team/092-non-disposable/team.md` § Handoff boundary which surface lands it — P7 cross-line write with the `forbidden` list narrowed to the marker lines, or the receiving body's own line [green: contracts/nd-acceptance-readability.contract.md#C-805]
- [X] T006A Create the owner page skeleton at `shared/definitions/non-disposable-definitions.md` — a header declaring the entries it owns (concept, disposition set + exemption forms, detection-class closed set, review-surface definition, supersede protocol, renumber predicate face, report schema, boundary with sanitize/history, relation to the constitution) [green: contracts/nd-detection-categories.contract.md#C-101]
- [X] T007A Author § Detection Categories of `shared/definitions/non-disposable-definitions.md` — the eight-member closed set — and the § Detection Subject rule that binds each member's predicate to a program-readable reading (file / line / field / literal / count / path / resolvable reference) [green: contracts/nd-detection-categories.contract.md#C-102]
- [X] T008A Author the four structure classes' predicates (`superseded-live`, `multi-owner`, `orphan-path`, `renumber-live-binding`) with their evidence obligations in `shared/definitions/non-disposable-definitions.md` [green: contracts/nd-detection-categories.contract.md#C-103]
- [X] T009A Author the four state classes' predicates (`status-unreadable`, `false-closed-set`, `stale-constant`, `deferral-marker`) with their evidence obligations in `shared/definitions/non-disposable-definitions.md` [green: contracts/nd-detection-categories.contract.md#C-104]
- [X] T010A State in `shared/definitions/non-disposable-definitions.md` that the reviewed corpus carries no `deferral-marker` row and that the class MUST be proven by construction instead [green: contracts/nd-detection-categories.contract.md#C-105]
- [X] T011A State the per-class mutation-leg obligation (one defect-creating leg per class plus the inverse) in `shared/definitions/non-disposable-definitions.md` [green: contracts/nd-detection-categories.contract.md#C-106]
- [X] T012A State the "a class that finds nothing reports `count: 0` over a declared surface" rule in `shared/definitions/non-disposable-definitions.md` [green: contracts/nd-detection-categories.contract.md#C-107]
- [X] T013A Record in `shared/definitions/non-disposable-definitions.md` that a class name outside the eight-member set is an `unknown-class` finding, never a silent extra class [green: contracts/nd-detection-categories.contract.md#C-108]
- [X] T014A Author § Disposition Set of `shared/definitions/non-disposable-definitions.md` — four members, one owner, and the "do nothing is not a disposition" prohibition [green: contracts/nd-disposition.contract.md#C-301]
- [X] T015A State the rejected values explicitly in `shared/definitions/non-disposable-definitions.md` (`null` / `""` / `keep` / `leave` / `none` / free text are findings, emitted as open) [green: contracts/nd-disposition.contract.md#C-302]
- [X] T016A Author § Exemption in `shared/definitions/non-disposable-definitions.md` — the four required fields (`reason`, `expiry_kind`, `expiry_value`, `expiry_recheck`) and the rejection of a missing member or a constant-true condition [green: contracts/nd-disposition.contract.md#C-303]
- [X] T017A Author § Exemption expiry semantics in `shared/definitions/non-disposable-definitions.md` — `on-date` / `on-review` date comparison, `on-condition` engine evaluation, and "unevaluable = `unevaluated`, never still valid" [green: contracts/nd-disposition.contract.md#C-304]
- [X] T018A Author § Disposition Bridge in `shared/definitions/non-disposable-definitions.md` — the per-value mapping table and the unmappable table whose row count is the Cartesian product of the two closed sets [green: contracts/nd-disposition.contract.md#C-305]
- [X] T019A Author the two explicit prohibitions (`exempt` has no material-hygiene counterpart; `dismiss` MUST NOT be read as deferred) with a named receiving surface per unmappable row, and the single adjudication rule ("the detecting engine decides the disposition vocabulary") exactly once, in `shared/definitions/non-disposable-definitions.md` [green: contracts/nd-disposition.contract.md#C-306]
- [X] T020A Author § Disposal Pathways in `shared/definitions/non-disposable-definitions.md` — archive is a move, deletion is never a disposition, no batch rewrite channel [green: contracts/nd-disposition.contract.md#C-307]
- [X] T021A State in `shared/definitions/non-disposable-definitions.md` the archive disposition's requirements — `archive` is a move with the source → archive mapping recorded, the superseded text is kept, and a deletion is never a disposition [green: contracts/nd-disposition.contract.md#C-308]
- [X] T022A Author § Supersede Protocol of `shared/definitions/non-disposable-definitions.md` — the three landing faces (body / guard / evidence path) a superseding side MUST recover [green: contracts/nd-renumber-and-supersede.contract.md#C-501]
- [X] T023A Author the mechanical detection of incomplete recovery (missing pointer, stale guard, second evidence spelling) in `shared/definitions/non-disposable-definitions.md` [green: contracts/nd-renumber-and-supersede.contract.md#C-502]
- [X] T024A Author the supersede registry row form (superseded → superseding → disposition → evidence) in `shared/definitions/non-disposable-definitions.md` [green: contracts/nd-renumber-and-supersede.contract.md#C-503]
- [X] T025A Author § Renumber-Face of `shared/definitions/non-disposable-definitions.md` — the four live-binding shapes and the closed history-record predicate enumeration, quoted from `scripts/python/renumber-utils.py` by pointer [green: contracts/nd-renumber-and-supersede.contract.md#C-504]
- [X] T026A Author the owner page's history-record rule (never rewritten to suit a renumber; a rewrite is reported red) while keeping every predicate in `scripts/python/renumber-utils.py` [green: contracts/nd-renumber-and-supersede.contract.md#C-505]
- [X] T027A Author the owner page's single-predicate rule (the engine consumes `renumber-utils.py`'s `EXCLUDED_PREFIXES` / `MACHINE_PREFIXES` / `EVIDENCE_SEGMENTS` / `DATED_RE`, never a copy) [green: contracts/nd-renumber-and-supersede.contract.md#C-506]
- [X] T028A Author § Report Entry in `shared/definitions/non-disposable-definitions.md` — the entry fields (`entry_id`, `path`, `line`, `class`, `detection`, `state`, `disposition`, `evidence_refs`) and the two `detection` values, with the `semantic` evidence minimum stated [green: contracts/nd-report-schema.contract.md#C-701]
- [X] T029A Author § Report Envelope in `shared/definitions/non-disposable-definitions.md` — the coverage declaration as the first block, the four reader questions, and the "no unprovable closure" rule that makes `closed` a derived value [green: contracts/nd-report-schema.contract.md#C-702]
- [X] T030A Create `shared/declarations/facts/non-disposable-review-surface.yaml` as a `kind: closed-set` fact carrying the five required keys and the ten roots in their declared order [green: contracts/nd-detection-engine-cli.contract.md#C-601]
- [X] T031A Register the owner page in `shared/definitions/framework-map.md` with one directory-registration row [green: contracts/nd-detection-engine-cli.contract.md#C-602]
- [X] T032A Declare in the owner page § Engine Contract that the engine resolves every root through `scripts/python/declaration_reader.py`, that a missing or invalid declaration exits 2 naming the path or key `STR-014`, and that an undeclared sibling produces a hint only [green: contracts/nd-detection-engine-cli.contract.md#C-603]
- [X] T033A Declare in the owner page § Engine Contract the argument set (the eight declared options and no other) and the three-valued exit-code surface with the empty-surface prohibition [green: contracts/nd-detection-engine-cli.contract.md#C-604]
- [X] T034A Declare in the owner page § Engine Contract the sharding rule (membership a pure function of the sorted path list, disjoint union equal to the candidate set, no empty shard), deterministic serialisation, and the single mirror-projection block placement [green: contracts/nd-detection-engine-cli.contract.md#C-605]
- [X] T035A Add the four glossary terms to `.specify/memory/glossary.md` — `Non-Disposable` / `Disposition（处置）` / `Review Surface（回顾面）` / `Exemption（豁免）` — each a pointer that restates no owner criterion
- [X] T036A Author the owner page's capture rule for the "diff against pre-change output" premises — which four readings a run MUST take before an edit (the `sync-mirrors.py --check` baseline, `wc -c .specify/instructions.md`, the two constitution pin readings, `git status --porcelain`) — in `shared/definitions/non-disposable-definitions.md` [green: contracts/nd-four-stage-command.contract.md#C-401]
- [X] T037A Write `.specify/specs/092-non-disposable/notes/pre-change-measurements.md` with those four readings taken on this tree at generation time, recording each command and its raw output, **and** freeze `notes/baseline-failed-tests.txt` (the failed node-id name list, before any edit — the designation GATE-1 compares against, never a count) [blockedBy: T036A]
- [X] T038A Create the 092 row in `.specify/memory/features.md` at status `Planned` and re-read the `Total Features` header in the same pass (the index is hand-maintained; header and rows move together) [blockedBy: T001A]
- [X] T039A Create `.specify/memory/features/092.md` from `.specify/templates/feature-details-template.md` — Overview / Latest Review / Key Changes / Implementation Notes / Future Evolution Suggestions / Related Files, including the constitution-XI boundary line [blockedBy: T038A]
- [X] T040A Register the eight clarify decisions `D-1`…`D-8` in `.specify/memory/register.md` as pointer-shaped rows (id → one-line meaning → authority path → status), placed where the table's existing `D-…` rows sit
- [X] T041A Create `.specify/specs/092-non-disposable/notes/measurement-corpus.md` — the 35 A–H entries with their 档 I / 档 II tier and reproduction source, read from `notes/input-review-080-090.md`
- [X] T042A Freeze `.specify/specs/092-non-disposable/coverage-baseline.txt` by redirecting `python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/092-non-disposable --freeze` at the first full-tree accounting run (not the first green one) [blockedBy: T030A]

**Checkpoint P1**: `declaration_reader.py --action list` loads the new fact; the owner page declares its owned
entries and carries both disposition tables; the registry row reads `Planned` with a detail file beside it; the
eight decisions are in `register.md`; `coverage-baseline.txt` exists.

**Checkpoint**: `scripts/python/non-disposable-check.py` answers `-h`, `--help`, `--version`, rejects an undeclared
option with exit 2, scans the whole declared surface read-only, emits the coverage declaration first, and reproduces
corpus A2 and F2 on this tree.
- [ ] T043A Create the `scripts/python/non-disposable-check.py` skeleton — stdlib only, shebang, module docstring stating usage and exit codes, `from __future__ import annotations`, `main(argv=None) -> int`, `if __name__ == "__main__": sys.exit(main())`
- [ ] T044A Implement the script-interface surface in `scripts/python/non-disposable-check.py` — `-h` / `--help` / `--version` answer without acting, and the argument set is exactly `--root`, `--json`, `--scope`, `--roots`, `--emit-categories`, `--declaration`, `-h`/`--help`, `--version`, every other option exiting 2 [green: contracts/nd-detection-engine-cli.contract.md#C-606]
- [ ] T045A Implement the three-valued exit-code surface in `scripts/python/non-disposable-check.py` (`0` = no findings over a stated non-empty surface; `1` = findings; `2` = argument/environment error) with the empty-surface prohibition [green: contracts/nd-detection-engine-cli.contract.md#C-607]
- [ ] T046A Implement the read-through-declaration surface in `scripts/python/non-disposable-check.py` — ten roots and their order via `scripts/python/declaration_reader.py`, absent-root reporting with a reason, unregistered-sibling hint, `STR-014` for a degraded read [green: contracts/nd-detection-engine-cli.contract.md#C-608]
- [ ] T047A Implement the zero-write guarantee in `scripts/python/non-disposable-check.py` — no repository write in any mode, and root resolution from the `.specify/scripts/python/` mirror to the parent of `.specify`
- [ ] T048A Implement `--scope` sharding in `scripts/python/non-disposable-check.py` — membership as a pure function of the sorted path list, disjoint union equal to the candidate set, no empty shard
- [ ] T049A Implement deterministic serialisation in `scripts/python/non-disposable-check.py` — entries sorted by `entry_id`, roots in declaration order, mappings sorted by key
- [ ] T050A Implement the mirror-safe projection block placement in `scripts/python/non-disposable-check.py` so `scripts/python/sync-mirrors.py` inserts exactly one projection marker before the `__main__` guard, and confirm the mirror carries it once
- [ ] T051A Implement the `status-unreadable` class in `scripts/python/non-disposable-check.py` by invoking `scripts/python/closure-acceptance-check.py --json` as a subprocess and reading `verdict` + `reasons`, carrying the checker path and the feature id in every entry's `evidence_refs` [green: contracts/nd-status-and-verification.contract.md#C-201]
- [ ] T052A Emit the checker's verbatim reason code `status-claims-implemented-but-blocked` in `scripts/python/non-disposable-check.py`, naming the feature, and report nothing when status and verdict agree [green: contracts/nd-status-and-verification.contract.md#C-202]
- [ ] T053A Report the **missing field names** of `verification.md` (machine-readable block, smoke fields) in `scripts/python/non-disposable-check.py`, reading the field names from the owner document [green: contracts/nd-status-and-verification.contract.md#C-203]
- [ ] T054A Recompute a claimed closed-set identity in `scripts/python/non-disposable-check.py` and report both readings on disagreement, treating "declared but never recomputed" as its own finding [green: contracts/nd-status-and-verification.contract.md#C-204]
- [ ] T055A Keep `scripts/python/non-disposable-check.py` free of any private reason-code table, status enum or closure ladder, and prove it by the module's own import surface [green: contracts/nd-status-and-verification.contract.md#C-205]
- [ ] T056A Make the status reading reproducible from the entry alone in `scripts/python/non-disposable-check.py` — `evidence_refs` names the command and the feature, and the emitted state does not depend on run order or concurrency degree [green: contracts/nd-status-and-verification.contract.md#C-206]
- [ ] T057A Make the merged `status-unreadable` emission carry every observable the contract requires — the missing field names, the recomputed closed-set readings and the checker-call identity — so no one of them is reported alone, and supply the leg that substitutes `closure-acceptance-check.py` with a stub emitting a chosen verdict (the report MUST reflect the stub, and MUST fail if the engine re-derived the verdict) [green: contracts/nd-status-and-verification.contract.md#C-207]
- [ ] T058A Implement the eight-class judgement loop in `scripts/python/non-disposable-check.py` by reading the class set from the owner page rather than from a local literal, and emitting `unknown-class` for any class absent there
- [ ] T059A Implement the `superseded-live`, `multi-owner`, `orphan-path` and `renumber-live-binding` classes in `scripts/python/non-disposable-check.py`, each naming both sides of the defect, with one class per entry (a two-class defect is two entries, never a joined class string)
- [ ] T060A Implement the four state classes in `scripts/python/non-disposable-check.py`, including `deferral-marker`'s retention statement with no expiry condition
- [ ] T061A Implement entry evidence emission in `scripts/python/non-disposable-check.py` — `path`, `line` (1-based, `0` reserved for file-level facts), and at least one resolvable `evidence_refs` element per entry (≥ 2 for a `semantic` entry), with a duplicate `entry_id` merged and `path` normalised per `declaration_reader.normalize_path`
- [ ] T062A Implement the `multi-owner`, `orphan-path` and `renumber-live-binding` reproduction arms over the A–H corpus in `scripts/python/non-disposable-check.py`, and run the engine against the real tree to record the first coverage declaration (per-root counts, candidate total) into `.specify/specs/092-non-disposable/notes/quickstart-run.md`
- [ ] T063A Implement the per-class zero-reporting arm in `scripts/python/non-disposable-check.py` — `count: 0` accompanied by the roots searched, never an omitted class
- [ ] T064A Implement the unified `--json` and human projections of one in-memory run in `scripts/python/non-disposable-check.py` so every human-form count appears in the JSON
- [ ] T065A Implement the mandatory coverage declaration as the first block of every report (roots in declared order with presence and count, candidate total, exclusions with reasons, missing roots, unregistered siblings, declaration path and status)
- [ ] T066A Emit `unevaluated` entries and `unevaluated` shards as counted, visible states in `scripts/python/non-disposable-check.py` and include them in the not-closed totals [green: contracts/nd-report-schema.contract.md#C-703]
- [ ] T067A Derive `closed` in `scripts/python/non-disposable-check.py` and forbid any "kept as is" / "reviewed by a human" field [green: contracts/nd-report-schema.contract.md#C-704]
- [ ] T068A Make the four reader questions answerable from the report alone in `scripts/python/non-disposable-check.py` (what was looked at, what was found, what is proposed, what is not done) [green: contracts/nd-report-schema.contract.md#C-705]
- [ ] T069A Generate `.specify/scripts/python/non-disposable-check.py` from `scripts/python/non-disposable-check.py` by running `python3 scripts/python/sync-mirrors.py`, and confirm the pair carries the projection marker and no new drift [green: contracts/nd-report-schema.contract.md#C-706]
- [ ] T070A Emit a `status-unreadable` entry's verdict and reason-code spelling verbatim, plus the checker-call identity, in the machine fields of every `--json` run, asserted on the corpus A2 reading [green: contracts/nd-report-schema.contract.md#C-707]
- [ ] T071A Verify the engine reproduces corpus A2 and `quickstart.md` § 2's two readings on this tree, recording exit codes and hit lines in `.specify/specs/092-non-disposable/notes/quickstart-run.md` [blockedBy: T062A]

**Checkpoint P2**: the engine runs read-only, exits 0/1/2 meaning three different things, writes nothing, and its
coverage declaration agrees with an independent enumeration over the ten roots.

**Checkpoint**: both seam faces name the four stages in order; review and design write nothing; a confirmation is
required before any write; unconfirmed entries are visible; evidence lands one file per run in four segments.
- [ ] T072A Add seam steps 0 / A / B to `skills/internal/manage-history/SKILL.md` naming the four stages in order — review → design（方案）→ user confirm → execute — inserted around the existing **Steps 1–6** (review as Step 0, design as Step A, confirmation as Step B, execute taking Step 6's position), leaving that list's own numbering intact [green: contracts/nd-four-stage-command.contract.md#C-402]
- [ ] T073A Implement the zero-write reading for the review and design segments in `skills/internal/manage-history/SKILL.md` — two snapshots (`git status --porcelain=v1` full text + content hashes over the managed path set), taken before the review and after the design, required byte-identical [green: contracts/nd-four-stage-command.contract.md#C-403]
- [ ] T074A Constrain a temporary design plan to `.specify/.tmp/` in `skills/internal/manage-history/SKILL.md`, with removal mandated by the execute segment, and prove it by a copy-tree write that stays inside that path [green: contracts/nd-four-stage-command.contract.md#C-404]
- [ ] T075A Implement the closed three-value confirmation granularity (`group` / `item` / `none-of`, absent input resolves to `group`, no "one confirmation = execute everything") in `skills/internal/manage-history/SKILL.md` [green: contracts/nd-four-stage-command.contract.md#C-405]
- [ ] T076A Implement the `unconfirmed` visible state in `skills/internal/manage-history/SKILL.md` — not dropped, not retried next round, not counted toward this round's closure; a partial confirmation leaves the rest visible and outside the closure count [green: contracts/nd-four-stage-command.contract.md#C-406]
- [ ] T077A Implement the group-boundary execute ordering in `skills/internal/manage-history/SKILL.md` — start only on the confirmed set, write at group boundaries, never mid-entry [green: contracts/nd-four-stage-command.contract.md#C-407]
- [ ] T078A Implement the four-segment evidence file contract in `skills/internal/manage-history/SKILL.md` — one file per run under `.specify/specs/<spec-dir>/test-evidence/`, segments `readings` / `paths` / `corpus` / `dispositions`, and no write to `.specify/memory/sanitize/findings.json` or `.specify/history/` [green: contracts/nd-four-stage-command.contract.md#C-408]
- [ ] T079A Add the four-stage delegation bullet list plus the seam pointer to `templates/commands/history.md`, retaining the existing distill capability and incremental manifest [green: contracts/nd-four-stage-command.contract.md#C-409]
- [ ] T155A In the execute segment of `skills/internal/manage-history/SKILL.md`, handle the archive disposition as `git mv` semantics with the source → archive mapping recorded, keeping the superseded text and showing a rename pair rather than a deletion [green: contracts/nd-renumber-and-supersede.contract.md#C-507]
- [ ] T080A Regenerate the per-tool command copies from `templates/commands/history.md` with `python3 scripts/python/regen-command-copies.py`, then confirm `pytest -m contract tests/contract/test_docs_command_template.py::test_c10_runtime_copies_exist_for_every_present_tool` is green [blockedBy: T079A]
- [ ] T081A Generate `.specify/skills/internal/manage-history/SKILL.md` from its source by running `python3 scripts/python/sync-mirrors.py`, confirm the pair is byte-identical, and register the two edited frozen sources in `tests/contract/test_expression_compatibility.py`'s `ALLOWED_POST_BASELINE_CHANGES` with markers **added by this change** and a reason naming Feature 092 [blockedBy: T072A,T079A]
- [ ] T082A Run the `quickstart.md` § 8 seam walk against a copy tree and record the two snapshots' byte comparison, the confirmation reading and the four evidence segments in `.specify/specs/092-non-disposable/notes/quickstart-run.md` [blockedBy: T080A]

**Checkpoint P3**: deleting the seam from either face makes the P5 guard go red; on a copy tree, review and design
leave `git status --porcelain` byte-identical, and execute writes only after a confirmation.
- [ ] T156A Add the seam-bypass leg to `tests/contract/test_non_disposable_contract.py` and to the owner page's statement of the rule — an execute run touching a path that no confirmed design row names is red, and a confirmed-row path is green; the before/after readings are required on every edit the seam makes [green: contracts/nd-four-stage-command.contract.md#C-410]

**Checkpoint**: one pointer line lands inside an existing `##` section of the template; the live instructions are
regenerated within budget; the compatibility files are still symlinks; no count pin moves.
- [ ] T083A Append exactly one pointer line into an existing `##` section of `templates/instructions-template.md`, adding no top-level section and no restated owner criterion
- [ ] T084A Regenerate `.specify/instructions.md` by running `scripts/bash/generate-instructions.sh`, then confirm `wc -c .specify/instructions.md` is within `INSTRUCTIONS_BUDGET_BYTES` and that `AGENTS.md` / `CLAUDE.md` / `QODER.md` / `.github/copilot-instructions.md` are still symlinks [blockedBy: T083A]
- [ ] T085A Run `pytest -m contract tests/contract/test_fast_fail_discipline.py` and confirm the top-level `##` count pin is unmoved after the regeneration [blockedBy: T084A]

**Checkpoint P4**: the instructions face points at the owner page without a second definition of it, and no count
pin moves.

**Checkpoint**: the guard is green, every closed set has a mutation leg, and substituting the closure checker with a
stub makes the `status-unreadable` leg fail.
- [ ] T086A Create the contract-test group files under `tests/contract/` (`test_non_disposable_contract.py` plus one file per later clause group, so clause groups can be authored in parallel) with each file's fixture data stated in itself — the seven-face existence legs and the `deferral-marker` fixture tree
- [ ] T087A Add the mutation-leg harness to `tests/contract/test_non_disposable_contract.py` — one defect-creating copy-tree edit per class, asserting red with the expected path:line, plus the inverse asserting green
- [ ] T088A Add the engine CLI legs to `tests/contract/test_non_disposable_contract.py` — `-h`/`--help`/`--version` answer without acting and an undeclared option exits 2; every declared option is accepted and no other one is exposed
- [ ] T089A Add the read-only leg to `tests/contract/test_non_disposable_contract.py` — a `git status --porcelain` comparison around a full run is byte-identical, with a mutation leg that touches a tracked path and asserts red
- [ ] T090A Add the empty-surface, unknown-option and declaration-surface legs to `tests/contract/test_non_disposable_contract.py` — the empty candidate set is never `closed: true`, a missing declaration exits 2 naming the path, an invalid key exits 2 naming the key, an absent root is reported and excluded with a reason, and an undeclared sibling only hints
- [ ] T091A Add the sharding leg to `tests/contract/test_non_disposable_contract.py` — shards are disjoint, their union equals the candidate set, and a mutation leg duplicates one path across two scopes and asserts red
- [ ] T092A Add the determinism and projection legs to `tests/contract/test_non_disposable_contract.py` — two runs on one tree produce byte-identical `--json` after the run identifier is removed, and the `_bridge_*` block sits before the `__main__` guard
- [ ] T093A Add the disposition-set and "do nothing is not a disposition" legs to `tests/contract/test_non_disposable_contract.py`, reading the four member spellings through the owner page and asserting red when a mutation leg injects `"keep"` into a report
- [ ] T094A Add the exemption-field and expiry-evaluation legs to `tests/contract/test_non_disposable_contract.py` — each of the four fields removed in turn names the missing member, an unevaluable `on-condition` predicate lands `unevaluated`, and a passed `expiry_recheck` re-opens the entry
- [ ] T095A Add the bridge-exhaustiveness leg to `tests/contract/test_non_disposable_contract.py`, computing the expected pair count from the two sets' lengths at test time and failing on a duplicate pair
- [ ] T096A Add the prohibition and adjudication legs to `tests/contract/test_non_disposable_contract.py` — both explicit prohibitions are stated in the owner page, no bridge row contradicts them, and the adjudication rule appears exactly once
- [ ] T097A Add the pathway and archive leg to `tests/contract/test_non_disposable_contract.py` — every `archive` record carries `moved`, `irreversible` appears only where the router says so, and a wrong archive landing face is reported as a finding
- [ ] T098A Add the three-recovery leg to `tests/contract/test_non_disposable_contract.py` — a body, a guard and an evidence path recovered together are green, and two of three is red
- [ ] T099A Add the per-landing-face mutation legs to `tests/contract/test_non_disposable_contract.py` — body / guard / evidence path each asserting red on a copy tree and green after synchronised recovery
- [ ] T100A Add the supersede-registry leg to `tests/contract/test_non_disposable_contract.py` — a supersede traced only in a commit message or session record fails
- [ ] T101A Add the live-binding leg to `tests/contract/test_non_disposable_contract.py` — each of the four shapes reported red with file and line
- [ ] T102A Add the history-record leg to `tests/contract/test_non_disposable_contract.py` — an old number inside the predicate face is green, and a rewritten history record is red
- [ ] T103A Add the single-predicate leg to `tests/contract/test_non_disposable_contract.py` — the engine carries no duplicate of the four predicate literals, and a mutation leg edits the predicate module and expects the classification to move with it
- [ ] T104A Add the entry-field leg to `tests/contract/test_non_disposable_contract.py` — a duplicate `entry_id` is merged, `path` is normalised per `declaration_reader.normalize_path`, `line` is 1-based, and a `semantic` entry carries at least two evidence refs
- [ ] T105A Add the two-projection and coverage-declaration legs to `tests/contract/test_non_disposable_contract.py` — every human-form count appears in the parsed JSON, and a findings-bearing report without a declaration is invalid
- [ ] T106A Add the unevaluated-count leg to `tests/contract/test_non_disposable_contract.py` — an unparseable deterministic input and a malformed semantic shard each grow the not-closed total
- [ ] T107A Add the no-unprovable-closure leg to `tests/contract/test_non_disposable_contract.py` — a mutation leg writes `closed: true` over an open entry and asserts red
- [ ] T108A Add the four-reader-questions leg to `tests/contract/test_non_disposable_contract.py` — each answer is derivable from the report and the design face invents no fifth form
- [ ] T109A Add the mirror-generation leg to `tests/contract/test_non_disposable_contract.py` — the generated mirror carries the projection marker exactly once and the pair shows no drift
- [ ] T110A Add the vocabulary-quoting leg to `tests/contract/test_non_disposable_contract.py` — a status finding carries the verdict and the reason-code spelling verbatim plus the checker-call identity, and the consumption legs assert that substituting `closure-acceptance-check.py` with a stub returning a chosen verdict makes the report reflect the stub, that `status-claims-implemented-but-blocked` is emitted with the checker's spelling while an agreeing feature is not reported, that a missing machine-readable field is named rather than called "unreadable", that both closed-set readings are reported on disagreement, that no literal reason-code table exists in the engine module, that the evidence refs reproduce the verdict in one command, and that a concurrent run gives the same status reading
- [ ] T111A Add the four-stage ordering leg to `tests/contract/test_non_disposable_contract.py` — both faces name the stages in order, and a mutation leg deletes one stage name from one file and asserts red
- [ ] T112A Add the zero-write leg to `tests/contract/test_non_disposable_contract.py` — the two snapshots around review and design are byte-identical
- [ ] T113A Add the temporary-plan leg to `tests/contract/test_non_disposable_contract.py` — a mutation leg writes the design plan to a tracked path and asserts red
- [ ] T114A Add the confirmation-granularity and unconfirmed-visibility legs to `tests/contract/test_non_disposable_contract.py` — three values with `group` as the default and no fourth value, and a partial confirmation leaves the rest visible as `unconfirmed` and outside the closure count
- [ ] T115A Add the group-boundary and non-bypass legs to `tests/contract/test_non_disposable_contract.py` — a one-group confirmation touches no path outside that group, the mutation leg touches one and asserts red, and a path outside the confirmed design rows touched by an execute run is a violation
- [ ] T116A Add the evidence-shape and preservation legs to `tests/contract/test_non_disposable_contract.py` — one file per run in the spec's `test-evidence/`, all four segments present, the distill capability and incremental manifest still present, and `.specify/history/` stays read-only to this feature
- [ ] T117A Add the archive-is-a-move leg to `tests/contract/test_non_disposable_contract.py` — `git status --porcelain` after a repair run shows a rename pair and never a deletion
- [ ] T118A Add the four-closed-set immutability leg to `tests/contract/test_non_disposable_contract.py` — `sanitize-utils.py`'s `CATEGORIES` / `DISPOSITIONS` / `STATES` / `DETECTIONS` are byte-unchanged, and both constitution count pins are unmoved

**Checkpoint P5**: `pytest -m contract tests/contract/test_non_disposable_contract.py` is green, and each mutation
leg was observed to go red when its subject was broken.
- [ ] T119A Record the **before** engine reading for the 档 I scope in `.specify/specs/092-non-disposable/test-evidence/repair-corpus.md` (`--json`, exit code, per-class counts) as the first evidence segment [blockedBy: T086A]
- [ ] T120A Repair A1 by completing `.specify/specs/089-script-interface-contract/verification.md` with the machine-readable per-criterion block and smoke fields, and reconciling its registry row against `closure-acceptance-check.py`'s verdict — the record's fields, not its conclusions, are what change
- [ ] T121A Repair A2 by completing `.specify/specs/084-harness-triple-structure/verification.md` so its `unclassified` claim is taken from `harness-triple-check.py --action verify` rather than asserted
- [ ] T122A Repair A3 by moving 090's registry row in `.specify/memory/features.md` from `Planned` to its closure-consistent value (closure verdict `accept`, 4/4 SC) [blockedBy: T038A]
- [ ] T123A Repair A4 by completing the structural record of `.specify/specs/089-script-interface-contract/tasks.md` so its non-story-phase user-story labels and its status block agree
- [ ] T124A Repair A5 by completing the decision-tension records of `.specify/specs/085-sdd-temporary-goal-team/plan.md` to the owner's six-field form [green: contracts/nd-acceptance-readability.contract.md#C-806]
- [ ] T125A Repair A6 by adding the post-081 common schema fields (`**Path**:` markers, `smoke_command`) to `.specify/specs/080-humanize-run-output/requirements.md` as a record completion [green: contracts/nd-acceptance-readability.contract.md#C-807]
- [ ] T126A Repair B1 by marking `C-016` in `.specify/specs/086-efficient-test-execution/contracts/runner-contract-086.contract.md` superseded with a pointer to the 089 mirror-projection contract, keeping the old text, and retiring or replacing the `byte_identical` guard in `tests/contract/test_run_tests_runner_contract.py` in the same change
- [ ] T127A Repair B2 by following the owner in `.specify/specs/085-sdd-temporary-goal-team/contracts/temporary-goal-team.md` — its **C-007** (the team path form `.specify/specs/<NNN-slug>/team/team.md`) and **C-008** (creation timing), not a paraphrased copy — and in `contracts/checkpoint-and-agents.md`'s **C-001** (the four-part checkpoint) — with markers and pointers, old text retained
- [ ] T128A Repair B3 by marking `.specify/specs/067-*/contracts/runner-contract.md` "Serial is the default" superseded by 086's parallel default (marker + pointer, old text retained)
- [ ] T129A Repair B4 by re-pointing the evidence path in `.specify/specs/088-*/efficiency-model.md` § evidence-path to the owner spelling that exists, retaining the original text inside the disposition record
- [ ] T130A Repair B5 by choosing one owner spelling for the two-slot evidence path and adding pointer rows for the other two spellings in the same disposition record
- [ ] T131A Repair C1 by correcting the live bindings in `.specify/specs/089-script-interface-contract/requirements.md` (Feature ID), `089/tasks.md` (headers) and `089/feature-ref.md` (its binding lines) to 089
- [ ] T132A Repair C2 by correcting the live instruction in `.specify/specs/089-script-interface-contract/tasks.md` so it names the 089 registry row and `features/089.md`, and by renaming `.specify/specs/089-script-interface-contract/team/086-script-interface-contract/` to the 089 slug with `git mv` semantics, correcting its `name:` line [blockedBy: T131A]
- [ ] T133A Repair C4 by correcting 088's eight contract headers, its main team name and its dogfood slug to 088
- [ ] T134A Repair G1 by adding the goal-first mutation leg to `tests/contract/test_sdd_loop_driver_reanchor.py` (asserting red when the ordering is broken)
- [ ] T135A Repair G2 by replacing the tautological `first_no` assertion in `tests/contract/test_sdd_loop_driver_reanchor.py` with an assertion that reads the actual first item
- [ ] T136A Repair G3 by completing `RULE_SET` in `tests/contract/test_sdd_loop_driver_reanchor.py` against the owner's rule anchor so deleting a rule member turns it red
- [ ] T137A Record the **after** engine reading over the same scope in `.specify/specs/092-non-disposable/test-evidence/repair-corpus.md`, with the changed-path list (`git diff --name-only` scope), the corpus entry ids and one disposition record per entry — the four segments of E-7 [blockedBy: T119A]
- [ ] T138A Confirm that no 档 II receiving body (D1–D6, E1–E6, F1–F5, H1–H2) appears in the changed-path list of this feature's diff, and record that reading beside the evidence file [blockedBy: T137A]

**Checkpoint P6**: the second reading shows 档 I at zero by name; each repaired entry's evidence file carries the
four segments; RK-5's check (no 档 II body touched) reads clean.

**Checkpoint**: the 15 档 II entries are detected, each receiving body carries exactly one handoff marker, and the
"zero" statistic excludes 档 II by construction.
- [ ] T139A Run the engine's `multi-owner` class over the D-row carriers (081, 084, 088, 090 and the 082/083 owners) and record the detection readings in `.specify/specs/092-non-disposable/test-evidence/shift-092.md` [blockedBy: T059A]
- [ ] T140A Run the engine's `false-closed-set` class over the E-row carriers (083, 089, 084, 087) and append the readings to `.specify/specs/092-non-disposable/test-evidence/shift-092.md`
- [ ] T141A Run the engine's `stale-constant` class over the F-row carriers (the ceiling owner, `scripts/bash/generate-instructions.sh`, the copying plans, the registry, 083) and append the readings to `.specify/specs/092-non-disposable/test-evidence/shift-092.md`
- [ ] T142A Run the engine's `orphan-path` class over the H-row carriers (086's mirror spelling, 082's session file, 085's GATE-1 path) and confirm `.specify/.tmp/086-*` (H3) produces no entry as a recorded exclusion, appending the reading to `.specify/specs/092-non-disposable/test-evidence/shift-092.md`
- [ ] T143A Declare the 12 Shift List rows in the owner page § Handoff Rows (`plan.md` § Shift List face) as pointer-shaped rows naming corpus id → receiving feature → landing face, so the marker form has a single owner
- [ ] T144A Land one handoff marker line per receiving body of `plan.md` § Shift List (12 rows, the `<!-- 092 handoff: <corpus id> → <receiving feature> -->` form, placed where the defect is) and change nothing else in those bodies [blockedBy: T143A]
- [ ] T145A Confirm the shift list carries one row per 档 II entry (15) and that the feature's own zero statistic counts 档 I only, recording both readings in `.specify/specs/092-non-disposable/test-evidence/shift-092.md` [blockedBy: T144A]
- [ ] T146A Record the two-way coverage reading FR-056 requires in `.specify/specs/092-non-disposable/test-evidence/shift-092.md` — every corpus group has a carrier, and `deferral-marker` plus FR-023's rewrite limb are proven by construction rather than by a corpus row

**Checkpoint P7**: each 档 II receiving body carries exactly one marker, the receiving lines' owners are named, and
the feature's reported zero excludes 档 II.

**Checkpoint**: the closure run, the evidence index, `verification.md` and the gate readings all exist and agree; no
`[ ]` row remains; the status flip is the closure engine's verdict, not this file's claim.
- [ ] T147A Write `.specify/specs/092-non-disposable/verification.md` from `.specify/templates/verification-log-template.md` — one status row per success criterion (20), the smoke record, `deferred_tasks=`, and the engine reading behind each row
- [ ] T148A Run the stage gates and paste the raw output into `.specify/specs/092-non-disposable/test-evidence/tasks-gates.txt` — `validate-tasks.py`, `decomposition-check.py --mode tasks`, `account-clause-coverage.py --spec-dir`, and `pytest -m contract tests/contract/test_non_disposable_contract.py`
- [ ] T149A Run the mirror verification and paste it into `.specify/specs/092-non-disposable/test-evidence/tasks-gates.txt` — `python3 scripts/python/sync-mirrors.py --check`, the `diff -q` readings for every byte-equal pair in `plan.md` § Mirror Obligations, and the `regen-command-copies.py` re-run result
- [ ] T150A Run `closure-acceptance-check.py --spec-dir .specify/specs/092-non-disposable` and record its `verdict` and `reasons` verbatim in `verification.md`; the registry status flip is written only on `accept`
- [ ] T151A Flip the 092 row of `.specify/memory/features.md` per the closure verdict and re-read the `Total Features` header in the same pass, appending a `(deferred: …)` suffix only if a `[~]` row exists [blockedBy: T147A]
- [ ] T152A Update `.specify/memory/features/092.md` § Latest Review and § Key Changes with this run's measured outcome [blockedBy: T151A]
- [ ] T153A Index the run's evidence files in `.specify/specs/092-non-disposable/test-evidence/INDEX.md` (one line per file, its producer row and its reading date)
- [ ] T154A Register the run's own durable identifiers (any finding `F-…`, open item `OI-…`, recommendation `REC-…` coined after this stage, plus the `F-1 (092)` row for the post-freeze clause delta) in `.specify/memory/register.md`, in the pointer shape

**Checkpoint P8**: zero open rows remain, the closure verdict is recorded verbatim, and every gate reading is on
disk with the command that produced it.
- [ ] T157A Migrate the sibling spec-local teams that still nest the default team under its own spec slug (`085/086/087/089`) to `team/team.md`, keeping named extra teams under `team/<team-slug>/team.md`; re-run `goal-utils.py run-checks` per spec and record the before/after paths in `test-evidence/team-path-migration.txt` (the engine now resolves the default file first, so the migration is a rename, not a behavioural change).
- [ ] T158A Root-fix the intermediate next-work narration: `shared/guidelines/progress-reporting.md` gains `## 无人值守模式（Unattended Mode）` (periodic reports suppressed; one final-state report; anomalies still immediate), the ambient section in both instruction surfaces points at it, and the change is recorded in `test-evidence/unattended-reporting-root-fix.md`.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: no dependencies; T001 first, then T002…T005.
- **SC-001 … SC-004 (Phases 2–5)**: all depend on Setup. They are subject-disjoint but not fully parallel: Phases 3 and 5 chain on measurement, and Phases 2, 4, 5 all append to their own evidence file, so each phase is internally serial and the phases themselves may be dispatched as separate packages.
- **Polish (Phase 6)**: depends on every phase above, because it re-verifies their clauses as one falsifiable set; T032 → T033 → T034 → T035 and T036 → T037 → T038 are each a chain, and T039 reads T035's reading.

### Row Dependencies (machine-checkable)

- T002, T003, T004, T005 ← T001
- T007 ← T006; T012 ← T008, T009, T010, T011
- T013 ← T002; T014 ← T013; T015 ← T014; T016 ← T014; T017 ← T016; T018 ← T017; T020 ← T016, T017, T018; T021 ← T016
- T019 has no in-phase blocker: it reads the landed protocol, and T027 depends on it
- T023 ← T022; T024 ← T023; T025 ← T024; T026 ← T025
- T027 ← T019; T028 ← T027; T029 ← T028
- T030 ← T021; T031 ← T030; T032 ← T012, T020, T026, T029; T033 ← T032; T034 ← T033; T035 ← T034; T039 ← T035; T036 ← T014, T024; T037 ← T036; T038 ← T037

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

- **F-6 (baseline algorithm conflict, disclosed, not repaired here)**: the accountant's `--freeze` PRINTS a baseline over the corpus **excluding** the target spec, while the live run judges the feature's own clauses against that baseline. The consequence is concrete and unchanged: the live `clause-uncovered` check reports `598 uncovered, 0 beyond the frozen baseline`, and those 598 names all belong to *other* specs; this feature's own 31 clauses are claimed, so they never reach the uncovered set — the clause lane reads green for a reason the baseline does not explain on its own (the claims do). Resolving the asymmetry touches a shared engine outside this feature's clauses, so it is named here rather than patched; GATE-6 states the decidable form.
- **F-7 / F-8 (contract-form defects found at generation, repaired by T032/T033, and already applied at the analyze gate on 2026-11-09)**: (a) each contract page opened with an introduction line naming the FRs and the SC; under the owner's § 4.2 that is a *mention* because it sits outside every clause block, so the FR lane read `0 of 10` even though the map in `feature-ref.md` § 3 was complete. Repaired: T032's citation groups are the clause-level fix, and their **targets are now landed** — the four pages carry them and the accountant reads `10 of 10` (§ Premises re-measured row). (b) The four pages used the legacy `md-heading` form, whose body boundary stops at the next section heading, so text placed under a sub-heading inside a clause is silently excluded. Repaired: T033's canonical `**C-N** — title` conversion is **now landed** on all four pages, ids unchanged at 31, and the citation groups survive it (measured: `clause_citations` maps the same ten FRs on the converted pages). Both rows stay open as the implement-stage duty to **re-measure on the implement tree**: the numbers above were produced on this stage's working tree, and a row that re-reads a landed repair is still the row that carries its evidence.
- **Pre-existing red set (carried from `plan.md` EP-003)**: the repo-wide contract suite is red before this feature touches anything (49 failed, 6368 passed, 2 skipped at plan time; measured this stage as 2 failed, 129 passed over the four named modules). Acceptance is **no NEW failure against the measured baseline**, never "the suite is green".
- **089's pre-existing contract failures are not attributable to this stage**: `scripts/python/sync-mirrors.py`, `scripts/python/clause_extract.py` and `scripts/python/validate-requirements.py` are the three engines T032–T035 consume, and all three are already committed with no working-tree modification (measured this stage). `tests/contract/test_script_interface_contract.py` still reports violations for two of them — that is Feature 089's surface, outside this feature's territory, recorded here so a later reader does not attribute it to 090.
- **Interview-style rulings recorded** (unattended run, no user turn): (1) the phase grouping follows the four success criteria because `requirements.md` declares no user stories, and the `[SC-00N]` label records that mapping; (2) every `[green:]` tag cites the `contracts/<page>.md` form so it resolves relative to this file's own directory first; (3) clause partitions inside each contract page follow the page's own clause order, so `green-cross-phase` never fires for this file; (4) two further mutants (T017, T018) are added beyond the single mutation the open clause names, because two of its sibling clauses are otherwise documented propositions only, and the clarify tightening asks for a falsifiable pair; (5) `guard-tests.contract.md` C-5 is claimed by the row that re-measures the modules' purity (T031) rather than by the ordering row, because that clause is about what the face guard does NOT assert, and asserting its absence is a measurement, not a landing; (6) **the analyze repair of 2026-11-09** installed the FR citation groups and the canonical clause form on the four pages instead of leaving them to implement time, because an FR lane reading `0 of 10` makes DoD-1 unreachable for a reason the rows cannot fix later without re-cutting the row set; the contract pages are this stage's own artifacts, so the repair belongs here, while every row above stays open for its implement-tree re-measurement; (7) the same repair **re-cut the `[green:]` partition** (F-02): `direction-audit` C-1…C-3 moved from T020 to T014 and C-6 was added to T019, so each clause's green point is the row that actually asserts it — T020 keeps C-7…C-9 because it assembles their evidence, not because it asserts them; (8) `guard-tests` C-7 stays on T033, whose whole job is the conversion the clause's own acceptance form rests on, while the ordering guard itself is carried by T014 and red-controlled by T016–T018 — the clause is about the guard existing and being red-capable, and T033 is the row that makes its reading decidable on every page.
- **Clause partition (the file's own rule, and how it was reached)**: each page's clauses are claimed by rows that run in the page's own clause order (C-1 first, C-n last), never backwards, and no clause is claimed twice — § Green Partition is the mechanical export of exactly that: 20 rows, 31 claims, 4 pages. Where a page's clause order conflicted with a natural row order the row was re-cut rather than the tag dropped, and the F-02 repair moved two groups for the same reason: `direction-audit` C-1…C-3 are presence propositions about the protocol's text and belong to the row that first asserts that text (T014), while C-4…C-6 are text propositions about the landed protocol and belong to the row that verifies it line by line (T019); C-7…C-9 stay on T020. `validate-tasks.py` reports 0 errors and 0 warnings on this file.
- **Scope boundary**: this stage produced `tasks.md`, its coverage baseline, and — at the analyze repair of 2026-11-09 — the four contract pages' citation groups and canonical clause form, plus the two resolved markers in `research.md` / `feature-ref.md`. No framework source, test or governance file is edited here; every row above remains an implement-stage row, including the ones whose repair is already visible on this stage's tree (T032/T033), because their evidence must be re-measured on the implement tree.
- **Deferral discipline**: prefer `[~]` over leaving a row `[ ]` "for now" — `[~]` is a deliberate handoff with a reason recorded in `verification.md`; `[ ]` blocks completion.
