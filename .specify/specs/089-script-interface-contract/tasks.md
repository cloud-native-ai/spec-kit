# Tasks: 脚本接口契约（Script Interface Contract）

**Requirement ID**: 089
**Requirement Key**: 089-script-interface-contract
**Related Feature**: 089 脚本接口契约（Script Interface Contract）
**Input**: Design documents from `.specify/specs/089-script-interface-contract/`
**Prerequisites**: plan.md (required), requirements.md (required), research.md (R1–R13), data-model.md (E-1…E-8 / V-1…V-22), contracts/ (C-1…C-38), quickstart.md (S-0…S-8), feature-ref.md

**Tests Mode**: ON — Constitution Principle IV "Test-First & Contract-Driven Implementation" is test-mandating (`grep -nE 'MUST|MANDATORY|NON-NEGOTIABLE|Test-First|TDD|Contract-Driven' .specify/memory/constitution.md` matches it), and the feature is real code delivery (one engine + one contract test + a 737-candidate backfill). Every contract assertion lands BEFORE the implementation row that turns it green; the migration rows (the two count pins, the mirror parity suite) carry `[blockedBy:]` and sit AFTER the surfaces they count.

**Tests**: MANDATORY. Red-first evidence lands in `notes/red-first-evidence.md`; execution and closure evidence lands in `test-evidence/`.

**Organization**: grouped by the seven user stories of `requirements.md` (P1: US1–US5; P2: US6–US7).

## Delivery Slice Map

`plan.md` § Implementation Slicing names eight slices. They map onto the phases below: **S0** → Phase 1 · **S1** → Phase 2 (the owner page is foundational, not a story) · **S2** → Phase 4 US5 (the checker engine and its surfaces) · **S3** → Phase 6 US1 + Phase 8 US3 (one guard block) · **S4** → Phase 3 US4 (governance) · **S5/S6/S7** → Phase 4 US5 (backfill) · **S8** → Phase 9 (Polish). The plan has no slice for the classification mutants or the two count pins, which is why Phase 5 (US6) and the Polish pins sit outside the S-numbers: those rows are what stops the rule decaying into prose (FR-016 / FR-021 / FR-031).

## Definition of Done (DoD)

- DoD-1: Every FR-001…FR-031 has its implementation row closed (FR-028 is the tombstone; the traceability table satisfies it, not code).
- DoD-2: Every contract clause C-1…C-38 is claimed exactly once by a `[green:]` attribution on a row that names the file it writes.
- DoD-3: `python3 scripts/python/script-interface-check.py --json` reports `violations=0`, `applicable + exempt == candidates`, every `exemptions[]` row carrying `basis` + `evidence`, and no `unknown` state counted as a pass.
- DoD-4: All new and changed tests pass and the full suite has zero NEW failed node ids versus the implement-entry baseline.
- DoD-5: `sync-mirrors.py --check` exits 0 with byte equality on every unprojected pair and `mirror == project(source)` on the declared projected pairs; `--check-projection` is green.
- DoD-6: The five governance landings and their count pins move in ONE commit (19/20/12, watchlist 7, 33/34).
- DoD-7: `.specify/instructions.md` grew by exactly one `##` section and stays byte-unchanged across every `-h` / `--help` / `--version` / unknown-option run of `generate-instructions.sh` on a cloned scratch tree.
- DoD-8: SC-001…SC-012 each have a `test-evidence/` file; any `final`-path criterion in `blocked` / `deferred` / `fail` is waived explicitly in text, never folded silently into green.

**DoD Status**: pending

## Completion Gate

- GATE-1: Full suite has zero NEW failures versus the implement-entry baseline — check: `SPECKIT_PYTHON=/usr/bin/python3 scripts/bash/run-tests.sh --names-out .specify/specs/089-script-interface-contract/test-evidence/final-failed.txt` then `comm -13 .specify/specs/089-script-interface-contract/test-evidence/baseline-failed.txt .specify/specs/089-script-interface-contract/test-evidence/final-failed.txt` prints nothing.
- GATE-2: Every mirror obligation from plan.md § Mirror Obligations is clean — check: `/usr/bin/python3 scripts/python/sync-mirrors.py --check` exits 0 and `/usr/bin/python3 scripts/python/script-interface-check.py --check-projection` reports zero mismatch.
- GATE-3: No open task rows — check: `grep -cE '^- \[[ >]\]' .specify/specs/089-script-interface-contract/tasks.md` returns 0.
- GATE-4: Every `final`-path success criterion is `pass` and the feature's smoke record is present — check: in `.specify/specs/089-script-interface-contract/verification.md`, every criterion whose `**Path**` marker reads `final` has `SC-NNN_status=pass`, and `smoke_command=`, `smoke_exit_code=0` and `smoke_evidence_path=` (a path that exists and is non-empty) are all present; a `final`-path criterion in `blocked` / `deferred` / `fail` fails this gate unless an explicit user waiver names that criterion.
- GATE-5: The contract holds on this tree — check: `/usr/bin/python3 scripts/python/script-interface-check.py --json | /usr/bin/python3 -c 'import json,sys;d=json.load(sys.stdin);assert d["violations"]==0 and d["applicable"]+d["exempt"]==d["candidates"] and not d["findings"], d["findings"]'` exits 0.
- GATE-6: The structural validator is silent — check: `/usr/bin/python3 .specify/scripts/python/validate-tasks.py .specify/specs/089-script-interface-contract/tasks.md` exits 0 with zero ERROR.

## Environment Prerequisites

Probed 2026-11-06 in `/cws_data/cloud-native-ai/spec-kit` on branch `089-script-interface-contract` (base `780652a4`). Every row that depends on one of these verdicts references THIS section; no row restates a verdict. Re-probe at implement entry — never cached across runs.

- `pytest` on the `PATH` `python3`: **unavailable** — probe: `python3 -c 'import pytest; print(pytest.__version__)' @ 2026-11-06` → `ModuleNotFoundError: No module named 'pytest'`; affected: every test row, which therefore pins `SPECKIT_PYTHON=/usr/bin/python3`.
- `pytest` on `/usr/bin/python3`: **available** (9.0.3) — probe: `/usr/bin/python3 -m pytest --version @ 2026-11-06`; affected: the same rows; `scripts/bash/run-tests.sh` resolves `SPECKIT_PYTHON` first (its line 7, measured).
- `contract`-marked collection: **available** — probe: `SPECKIT_PYTHON=/usr/bin/python3 /usr/bin/python3 -m pytest -m contract -q --collect-only @ 2026-11-06` → `4303/7501 tests collected (3198 deselected) in 1.92s`; affected: the new test file's rows.
- `git` work tree and `git worktree add`: **available** — probe: `git --version` and `git worktree list @ 2026-11-06` → one entry (the plan-stage probe was removed); affected: the sandbox rows.
- Execution under the system temp root: **unavailable** (`noexec`) — probe: `mount | grep -E ' /tmp ' @ 2026-11-06`; affected: every sandbox row — the sandbox lives under `.specify/.tmp/` or `/var/tmp`, never `/tmp` (plan § Risks 1, feature-ref F-7).
- The framework CLI entrypoint for the downstream leg: **available** — probe: `specify --version @ 2026-11-06`; affected: T027 (SC-004, the downstream-project row). If unavailable at implement entry that row is `[~]`-eligible with the reason recorded in `verification.md`.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: can run in parallel — different write targets, no dependency on an incomplete row of the SAME phase (the structural validator scores `[P]` per phase).
- **[Story]**: US1…US7 from `requirements.md`. Setup / Foundational / Polish phases carry NO `[US]` label.
- **[blockedBy: Txxx]**: a real dependency; **[green: <contract>#<clause>]**: this row is the one that turns that clause green (one row per clause; see `templates/tasks-template.md` § Format).
- One line per row, exact file paths, no wrapped continuations.

### Task State Sigil

`- [ ]` open · `- [>]` claimed (multi-agent only) · `- [X]` closed · `- [~]` deferred with a reason recorded in `verification.md` (`deferred_tasks=`).

## Path Conventions

Framework-source shape (`plan.md` § Structure Decision): sources live at `shared/`, `scripts/`, `skills/`, `templates/`, `tests/`; their `.specify/` counterparts are generated by `sync-mirrors.py` and never hand-edited. All paths below are repo-relative.

### Premises measured at generation time (2026-11-06)

Every count below was re-derived this stage; the re-derivation command is given, and the trap form is named wherever a naive measurement returns a different number.

| Quantity | Measured | Re-derivation | Naive form that disagrees |
|---|---|---|---|
| FR definitions | **31** | `grep -cE '^- \*\*FR-[0-9]{3}\*\*:' requirements.md` | `grep -c 'FR-0'` → 52 (counts cross-references) |
| Tracked `*.sh` / `*.py` candidates | **737** = 71 sh + 666 py, 0 ignored | `git ls-files '*.sh' '*.py' \| wc -l`; same minus `git check-ignore` → 737 | work-tree `find` → also 737; the two sources coincide TODAY, which is exactly why the coverage assertion exists |
| Candidate split by root | tests/ 449 · .specify/ 146 · skills/ 87 · scripts/ 51 · src/ 3 · install.sh 1 | `git ls-files '*.sh' '*.py' \| awk -F/ '{print $1"/"}' \| sort \| uniq -c` | — |
| `__main__`-carrying `.py` | **207** of 666 | per-file loop with `grep -qE 'if __name__[[:space:]]*==[[:space:]]*["'\'']__main__["'\'']'` | `grep -qF 'if __name__ == "__main__":'` → **205** (two files quote `'__main__'`); `grep -c '__name__'` → 210 lines, and the unit here is files, not lines |
| `tests/` corpus | 2 `.sh` + 447 `.py`; **6** `.py` carry `__main__` (5 under `tests/fixtures/` plus `tests/contract/test_migration_distribution.py`); 441 do not | the same per-file loop scoped to `git ls-files 'tests/*'` | counting `grep -c` lines over-counts; counting the repo-wide 207 attributes the wrong tail to `tests/` |
| `scripts/bash/*.sh` | **14** (13 after excluding the incident script = the S5 backfill set) | `git ls-files 'scripts/bash/*.sh' \| wc -l` | — |
| `scripts/python/*.py` | **37** (36 after excluding the checker = the S6 backfill set) | `git ls-files 'scripts/python/*.py' \| wc -l` | `requirements.md` A2 was corrected to 37 in analyze round 1; feature-ref F-1 records the correction |
| `skills/` script candidates | 87 = 60 `.py` + 13 `.sh` under `skills/external/` and 11 `.py` + 3 `.sh` under `skills/internal/` | `git ls-files 'skills/*' \| grep -cE '\.py$'` (and the `.sh` counterpart) | counting `skills/*/*/scripts/*.sh` → 15, not 16 (one `.sh` sits outside a `scripts/` directory) |
| Skill source classification | 16 `skills/external/*/` skills declare `classification: external`; 38 `skills/internal/*/` declare `internal` | per-skill `grep -m1 '^classification:' <skill>/SKILL.md` | judging by directory name is what FR-027 forbids |
| Contract clauses | **38** (C-1…C-13, C-14…C-22, C-23…C-32, C-33…C-38) | `grep -c '^## C-' contracts/*.md` | counting `C-` mentions anywhere over-counts |
| Principle pins today | template **18** roman principles, live **19**; `###` heading totals are 18 on the template and 24 on the live file (the live file adds sub-headings) | `grep -cE '^### [IVX]+\. ' templates/constitution-template.md` / `.specify/memory/constitution.md` | counting every `###` heading mixes principles with sub-headings |
| `manage-constitution` mandate entries | **11** | sub-entry counter over the `- **MUST include**` block | counting `MUST include` occurrences → 1 |
| Instruction top-level sections | template **32**, live **33** (the `test_a7` pins) | `grep -c '^## ' templates/instructions-template.md` / `.specify/instructions.md` | — |
| Instructions size vs budget | live **33 357 B** vs `INSTRUCTIONS_BUDGET_BYTES=34816` → 1 459 B headroom | `wc -c .specify/instructions.md`; `grep -n INSTRUCTIONS_BUDGET_BYTES scripts/bash/generate-instructions.sh` | — |
| `-h` merged with `--help` | **7** scripts (`check-prerequisites`, `create-new-plan`, `create-new-requirements`, `create-new-skill`, `create-new-tools`, `implement-plan`, `research-project`) | grep the merged arm over `scripts/bash/*.sh` | — |
| Mirror baseline | `sync-mirrors.py --check` → exit **0**, six pairs ok, zero pre-existing drift | `/usr/bin/python3 scripts/python/sync-mirrors.py --check` | — |
| Missing `argparse` in `scripts/python/` | **2** (`clause_extract.py`, `gate-check.py`); the other three verdict-validators named in `plan.md` § Risks 9 import `argparse` and call `parse_args(sys.argv[1:])` | `grep -c 'import argparse'` per file | `plan.md` § Risks 9 formerly said five; corrected 2026-11-06 — see `ANOMALY A-1` in Notes |
| New artifacts absent today | `shared/definitions/script-interface-definitions.md`, `scripts/python/script-interface-check.py`, `scripts/python/script_interface_cli.py`, `scripts/bash/script-interface.sh`, `tests/contract/test_script_interface_contract.py` | `ls` each path | — |

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: freeze the baselines this feature is judged against and create the notes directory every red-first / measurement row writes into.

- [X] T001 Create the runtime-evidence landing points and record the generation-time premises in `.specify/specs/089-script-interface-contract/notes/premises.md`
- [X] T002 Capture the pre-change measurements (instructions size, budget constant, the `-h`-merged script list, candidate counts) with commands and date in `.specify/specs/089-script-interface-contract/notes/pre-change-measurements.md` [blockedBy: T001]
- [X] T003 Capture the implement-entry full-suite failed node ids into `.specify/specs/089-script-interface-contract/test-evidence/baseline-failed.txt` via `scripts/bash/run-tests.sh --names-out` [blockedBy: T001]
- [X] T004 Re-freeze the contract-clause coverage baseline with `scripts/python/account-clause-coverage.py .specify/specs/089-script-interface-contract --freeze` and assert the re-frozen name set is identical to the tasks-stage baseline committed at `.specify/specs/089-script-interface-contract/coverage-baseline.txt` (a difference is a changed clause corpus, not a silent pass) [blockedBy: T002]
- [X] T005 Prove the sandbox mechanism: `git worktree add --detach` under `.specify/.tmp/086-sandbox/`, assert `git worktree list` returns to one entry after removal, record timing in `.specify/specs/089-script-interface-contract/test-evidence/T005-sandbox-probe.txt` [blockedBy: T001]

**Checkpoint**: every later row can name the baseline it is compared against, and the sandbox is proven on this host before any classification row depends on it.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: the one owner page — four of the five landings are pointers to it (C-29 forbids restating its content anywhere else), so nothing story-shaped can land first.

- [X] T006 Author the owner page header `shared/definitions/script-interface-definitions.md`: title, self-declared single-source opening listing the five owned items, and the five section headings
- [X] T007 Split the canonical table in `shared/definitions/script-interface-definitions.md`: the four mandatory help-content labels and the classification step list live ONLY there, published in a form the checker's banned-literal scan can read [blockedBy: T006]
- [X] T008 Add the `## Declared Exceptions` table (`path` / `skill` / `unsatisfied clause` / `handling`, one row per script, literal `none` when empty) to `shared/definitions/script-interface-definitions.md` [blockedBy: T007]
- [X] T009 Record the projection declaration shape this feature will consume (the two kinds and the marker line) in `shared/definitions/script-interface-definitions.md` [blockedBy: T007]
- [X] T010 Register the new owner page in the definition index `shared/definitions/framework-map.md` so a reader reaches it without knowing its name [blockedBy: T006]
- [X] T011 Author the shared Python version helper `scripts/python/script_interface_cli.py`: one module-level constants table read by both the emitted rule and the executed rule, plus the version text/resolve API the checker consumes

**Checkpoint**: owner page + helper exist; every remaining row either points at the page, imports the helper, or writes an artifact the checker reads.

---

## Phase 3: User Story 4 - 规则随框架分发给下游项目 (Priority: P1) 🎯 MVP part 1

**Goal**: a downstream project initialised from this framework receives the rule — in its constitution template, in its `instructions.md`, and as a MUST-include item for its constitution generator.

**Independent Test**: `specify init` into a clean temp dir; assert the generated constitution carries the principle title, the generated `instructions.md` carries `## Script Interface Contract`, and the generator's MUST-include list names the principle.

**Checkpoint**: three of the five landings plus the mandate entry, all pointing at one owner page and none restating its labels. This story is file-disjoint from US1–US3, so it is the natural parallel track.

### Tests for User Story 4 (MANDATORY) ⚠️

- [X] T012 [P] [US4] Contract test for the owner page declaring itself the single source and listing its five owned items at the top, in `tests/contract/test_script_interface_contract.py` [blockedBy: T006] [green: contracts/governance-landing.contract.md#C-23]
- [X] T013 [P] [US4] Contract test for the template principle shape in `templates/constitution-template.md` — house shape, no line ≥100 chars, no residual placeholder, pointer rather than a copy of the owner page's steps [blockedBy: T006] [green: contracts/governance-landing.contract.md#C-24]
- [X] T014 [P] [US4] Contract test for the live principle landing in `.specify/memory/constitution.md` — title present, Sync Impact Report block, MINOR version line, `Last Amended` — with numeral-agnostic matchers [blockedBy: T006] [green: contracts/governance-landing.contract.md#C-25]
- [X] T015 [P] [US4] Contract test for the mandate-list entry shape inside the `- **MUST include**` block of `skills/internal/manage-constitution/SKILL.md` [blockedBy: T006] [green: contracts/governance-landing.contract.md#C-26]
- [X] T016 [P] [US4] Contract test for the ambient section shape — ≤2 sentences plus the owner path, zero `--action` / `$ARGUMENTS` / `<placeholder>` forms — in `tests/contract/test_script_interface_contract.py` [blockedBy: T012] [green: contracts/governance-landing.contract.md#C-27]
- [X] T017 [US4] Extend the double-landing guard in `tests/contract/test_constitution_double_landing.py`: `TEMPLATE_COUNT` 18 → 19, `LIVE_COUNT` 19 → 20, `COMMAND_COUNT` 11 → 12, `DOUBLE_LANDING_WATCHLIST` 6 → 7, and re-assert that the `c10` mutation probe still catches a missing landing [blockedBy: T013,T014,T015] [green: contracts/governance-landing.contract.md#C-28]
- [X] T018 [US4] Contract test asserting the banned-literal list is READ OUT of the owner page — grep the list back out of the page rather than re-declaring it — and that no other landing surface carries it, in `tests/contract/test_script_interface_contract.py` [blockedBy: T006] [green: contracts/governance-landing.contract.md#C-29]
- [x] T019 [US4] Contract test that the owner page's exemption table and the checker's `exceptions[]` payload agree row for row (declared path / unsatisfied clause / handling), in `tests/contract/test_script_interface_contract.py` [blockedBy: T018,T065] [green: contracts/governance-landing.contract.md#C-30] — evidence: `tests/contract/test_script_interface_contract.py::test_c30_owner_table_and_checker_payload_agree_row_for_row`

### Implementation for User Story 4

- [X] T020 [US4] Land the new principle in `templates/constitution-template.md` — `### <next numeral>. Script Interface Contract (Declared, Zero-Side-Effect)`, claim sentence ending in a colon, `MUST`/`MUST NOT` bullets, a `Rationale:` paragraph, pointer plus non-delegable points, and the rule's own scope wording (framework, downstream and third-party alike; no repository-limited phrasing) [blockedBy: T013,T014,T017] [green: contracts/governance-landing.contract.md#C-31]
- [X] T021 [US4] Land the mandate entry in `skills/internal/manage-constitution/SKILL.md` inside the `- **MUST include**` block, naming the owner path (11 → 12 entries) [blockedBy: T015]
- [X] T022 [US4] Land the ambient section `## Script Interface Contract` in `templates/instructions-template.md` (summary + owner path, project-neutral, no engine-invocation forms, the same scope wording) [blockedBy: T018,T020]
- [X] T023 [US4] Land the live principle in `.specify/memory/constitution.md` — next free numeral (20), the Sync Impact Report block at the top, `1.16.0 → 1.17.0`, `Last Amended` 2026-11-06, all in one edit [blockedBy: T020]
- [X] T024 [US4] Backfill the live instructions file ON A CLONED SCRATCH TREE via `generate-instructions.sh` (never on the live tree) and land the single new `## Script Interface Contract` section in `.specify/instructions.md`, recording the generator run in `.specify/specs/089-script-interface-contract/test-evidence/T024-instructions-reconcile.txt` [blockedBy: T022]
- [X] T025 [US4] Re-project the governance mirrors with `/usr/bin/python3 scripts/python/sync-mirrors.py --write --only shared --only templates --only skills/internal/manage-constitution` and confirm `--check` exits 0 — runtime coverage: FR-011, FR-012, FR-013, FR-014, FR-016 [blockedBy: T010,T020,T021,T022,T024]
- [X] T026 [US4] Update `tests/contract/test_fast_fail_discipline.py::test_a7_section_counts_20_to_21_and_21_to_22` to `TPL_EXPECTED = 33` and `LIVE_EXPECTED = 34`, keeping the live-minus-template delta pairing [blockedBy: T023,T024]
- [X] T027 [US4] Prove SC-004 on a clean downstream project: `specify init` into a temp dir under `/var/tmp`, then assert the generated constitution carries the principle title and the generated `instructions.md` carries the ambient heading, into `.specify/specs/089-script-interface-contract/test-evidence/SC-004-downstream.txt` [blockedBy: T023,T025]
- [X] T028 [US4] Prove SC-005 with `git show` of the amendment commit — version line 1.16.0 → 1.17.0, Sync Impact Report block, `Last Amended` — into `.specify/specs/089-script-interface-contract/test-evidence/SC-005-constitution-diff.txt` [blockedBy: T023]
- [X] T029 [US4] Record the C-21 owner-page / `--emit-rule` label-set and class-vocabulary agreement (both directions) as the Phase 3 half of that assertion, in `.specify/specs/089-script-interface-contract/test-evidence/T029-owner-page-emit-rule.txt` [blockedBy: T007,T025]

---

## Phase 4: User Story 5 - 本仓现存脚本补齐到契约 (Priority: P1) 🎯 MVP part 2

**Goal**: every applicable script in this repository is compliant — 14 bash files and 37 python files under `scripts/`, 87 under `skills/`, and the 449 under `tests/` judged file by file rather than exempted by directory.

**Independent Test**: one full checker run reports `violations=0`, prints the exemption list with `basis` + `evidence` per row, and shows all four conclusions true for every applicable row.

**Checkpoint (engine)**: `script-interface-check.py --json` runs, `--emit-rule` agrees with a full run, and every degraded path is a named finding rather than a pass.
**Checkpoint (bash half)**: `generate-instructions.sh --help` leaves the clone's `.specify/instructions.md` and `.gitignore` byte-identical, and the damaged-copy control proves the pair discriminates.
**Checkpoint (python half)**: `sync-mirrors.py --version` and `goal-utils.py --version` both exit 0 with one line, and the literal scan stays at zero.

### Tests for User Story 5 (MANDATORY) ⚠️

- [x] T030 [US5] Contract test for the candidate screen's two sources and the `source=walk-only` degradation, in `tests/contract/test_script_interface_contract.py` [blockedBy: T005] [green: contracts/script-interface-criteria.contract.md#C-1]
- [x] T031 [US5] Contract test for the coverage finding `candidate-not-collected` naming the file at exit 1, in `tests/contract/test_script_interface_contract.py` [blockedBy: T030] [green: contracts/script-interface-criteria.contract.md#C-2]
- [x] T032 [US5] Implement the engine skeleton in `scripts/python/script-interface-check.py`: screen (git enumeration + `check-ignore`, walk-only fallback reported as `source`), coverage assertion, report assembly, and the classification pipeline's `basis` / `evidence` emission — runtime coverage: FR-002, FR-009, FR-010 [blockedBy: T030,T031] [green: contracts/script-interface-criteria.contract.md#C-4]
- [x] T033 [US5] Contract test for mirror-copy class inheritance and "no unevaluated state counts as pass" — a projected mirror inherits the source's class, is never judged twice and is never exempted for being a copy — in `tests/contract/test_script_interface_contract.py`  [blockedBy: T032,T040]
- [x] T034 [US5] Implement the exempt-side and mirror-copy handling in `scripts/python/script-interface-check.py`: every exempt row carries a basis, and a projected mirror is judged once, on its source's class [blockedBy: T032] [green: contracts/script-interface-criteria.contract.md#C-6]
- [x] T035 [US5] Implement the both-uses rule in `scripts/python/script-interface-check.py`: a file that is sourced/imported AND acts on direct run is applicable, and "it is also a library" is never grounds for exemption [blockedBy: T031] [green: contracts/script-interface-criteria.contract.md#C-5]
- [x] T036 [US5] Implement the help-content labels as four separate assertions over the probed output in `scripts/python/script-interface-check.py`, so a text mentioning only "usage" cannot satisfy the clause [blockedBy: T031] [green: contracts/script-interface-criteria.contract.md#C-7]
- [x] T037 [US5] Implement the version probe in `scripts/python/script-interface-check.py`: one line `<script-name> <framework-version>`, the `unknown` observation kept distinct from a violation, and no literal version accepted from a script body [blockedBy: T031] [green: contracts/script-interface-criteria.contract.md#C-8]
- [x] T038 [US5] Implement the rejection probe in `scripts/python/script-interface-check.py`: non-zero exit, output produced before the main action, a recognized option present must not let an unknown one through, and a token after a bare `--` is not unknown [blockedBy: T031] [green: contracts/script-interface-criteria.contract.md#C-9]
- [x] T039 [US5] Implement the zero-side-effect and help-wins probes in `scripts/python/script-interface-check.py`: create the copy outside the measured tree (`.specify/.tmp/` or `/var/tmp`, never `/tmp`), remove it on success AND failure, turn a creation failure into `probe-unavailable`, and with a flag plus a write-triggering option both present require the exit before the main action in either order [blockedBy: T031] [green: contracts/script-interface-criteria.contract.md#C-10]
- [x] T040 [US5] Implement help-wins ranking in `scripts/python/script-interface-check.py`: the flag's verdict outranks the main action's in every ordering the probe can construct, reported as its own conclusion rather than folded into the zero-side-effect one [blockedBy: T038] [green: contracts/script-interface-criteria.contract.md#C-11]
- [x] T041 [US5] Contract test for the four degraded paths (`probe-unavailable`, `probe-budget-exhausted`, `probe-inconclusive`, `projection-mismatch`) each naming its finding at exit 1, in `tests/contract/test_script_interface_contract.py` [blockedBy: T040] [green: contracts/script-interface-criteria.contract.md#C-13]
### Implementation for User Story 5 — checker CLI and report (S2)

- [x] T042 [US5] Implement the engine's own contract conformance in `scripts/python/script-interface-check.py`: shebang, docstring naming usage and exit codes, `from __future__ import annotations`, `main(argv=None) -> int`, the `__main__` tail, module resolution from `REPO_ROOT`, sorted `candidates[]` with `elapsed_ms` the only differing field, no write inside the repository — and its own `--help` / `--version` green [blockedBy: T032] [green: contracts/contract-checker-cli.contract.md#C-14] [green: contracts/contract-checker-cli.contract.md#C-15]
- [x] T043 [US5] Implement the CLI arguments `--root`, `--json`, `--files`, `--emit-rule`, `--skip-probe`, `--sandbox`, `--budget-seconds`, `--check-projection`, with `--emit-rule` + `--files` an exit-2 argument error, in `scripts/python/script-interface-check.py` [blockedBy: T032] [green: contracts/contract-checker-cli.contract.md#C-16]
- [x] T044 [US5] Implement exit-code derivation from the report's own findings in `scripts/python/script-interface-check.py` — 0 / 1 / 2, nothing computed that the report cannot explain [blockedBy: T041] [green: contracts/contract-checker-cli.contract.md#C-17]
- [x] T045 [US5] Implement the `--json` payload in `scripts/python/script-interface-check.py`: `schema`, `mode`, `source`, `root`, the four counts, `elapsed_ms`, and the `candidates[]` / `exemptions[]` / `exceptions[]` / `findings[]` / `projection[]` arrays with every required row field [blockedBy: T032] [green: contracts/contract-checker-cli.contract.md#C-18]
- [x] T046 [US5] Implement the human face in `scripts/python/script-interface-check.py`: one `<path>: <missing limbs>` line per violation plus the always-printed `candidates=N applicable=N exempt=N violations=N` summary [blockedBy: T043] [green: contracts/contract-checker-cli.contract.md#C-19]
- [x] T047 [US5] Pin the deterministic-invocation discipline in `tests/contract/test_script_interface_contract.py`: two consecutive `--json` runs on the same tree differ only in `elapsed_ms`, the invocation writes nothing inside the repository, and `REPO_ROOT` resolves the `.specify/` mirror copy to its own root [blockedBy: T037,T043] [green: contracts/contract-checker-cli.contract.md#C-20]
- [x] T048 [US5] Implement `--emit-rule` in `scripts/python/script-interface-check.py`, generated from the same module-level constants table the classifier executes, carrying its eight keys [blockedBy: T011,T032] — the clause that owns this surface (C-21) is claimed once, by its guard row T082
- [x] T049 [US5] Implement `--check-projection` in `scripts/python/script-interface-check.py`: every declared projected mirror equals `source + declared projection`, re-applying is idempotent, a mismatch names the pair and exits 1 [blockedBy: T009,T041] [green: contracts/contract-checker-cli.contract.md#C-22]

### Implementation for User Story 5 — mirror projection (S2/S5)

- [x] T050 [US5] Implement the declared projection in `scripts/python/sync-mirrors.py`: one declaration table naming each projected mirror path and its kind (`python-version-bridge` before the `__main__` anchor, `bash-version-guard` after the shebang), idempotent, loud at exit 1 when an anchor is missing [blockedBy: T009] [green: contracts/mirror-projection.contract.md#C-34]
- [x] T051 [US5] Make `--check` assert `mirror == project(source)` for projected files (byte equality elsewhere) and name the projection kind per pair in `scripts/python/sync-mirrors.py` [blockedBy: T045] [green: contracts/mirror-projection.contract.md#C-35]
- [x] T052 [US5] Implement the self-sufficiency rule in `scripts/python/script_interface_cli.py`: re-derive the version from a `pyproject.toml` found beside the script, print `unknown` when there is none, and never walk up into a foreign checkout [blockedBy: T011] [green: contracts/mirror-projection.contract.md#C-36]
- [x] T053 [US5] Keep `MIRROR_PAIRS`' `strict_extras` flags unchanged and exercise the frame rule (no byte-identity claim on a projected mirror, no source claiming to be the mirror's whole surface) in `scripts/python/sync-mirrors.py` [blockedBy: T045] [green: contracts/mirror-projection.contract.md#C-37]
- [x] T054 [US5] Establish the hand-edit prohibition and the in-place marker: no `.specify/scripts/` or `.specify/skills/` file may be hand-edited, and every projected mirror carries exactly one marker line — grep the marker back out of the mirrors rather than authoring them — asserted in `tests/contract/test_script_interface_contract.py` [blockedBy: T009,T045] [green: contracts/mirror-projection.contract.md#C-33] [green: contracts/mirror-projection.contract.md#C-38]

### Implementation for User Story 5 — backfill (S5 bash, S6 python, S7 reconcile)

- [X] T055 [US5] Author the sourceable guard-block body in `scripts/bash/script-interface.sh` — a `case` loop over `"$@"` with an internal `--` terminator, no `getopts`, `-h|--help` exit 0 before any `source` [blockedBy: T049]
- [X] T056 [US5] Author the Python guard shape in `scripts/python/script_interface_cli.py` — the `VersionAction` subclass registered on the top parser AND every subparser (the required-subparsers trap) plus a pre-parse guard for the parsers that read `sys.argv` by hand [blockedBy: T011,T032]
- [X] T057 [US5] Make the incident script's help path free in `scripts/bash/generate-instructions.sh` — guard block first, ahead of `source common.sh` and ahead of the `.gitignore` writes at lines 66 and 216 [blockedBy: T053,T054]
- [X] T058 [US5] Prove SC-002 on a cloned scratch tree: `.specify/instructions.md` and `.gitignore` both byte-unchanged across `-h`, `--help`, `--version` and one unknown option, plus the damaged-copy red control that proves the pair discriminates, into `.specify/specs/089-script-interface-contract/test-evidence/SC-002-incident-script.txt` [blockedBy: T056]
- [X] T059 [US5] Generate the guard block into every applicable `.sh` under `scripts/bash/` (13 files; `common.sh` is exempt by measurement, not by name) through a one-shot generator recorded in `.specify/specs/089-script-interface-contract/test-evidence/T056-bash-backfill.txt`, merging into the existing `--help|-h` arm of the seven scripts that already carry one rather than adding a second `-h` branch [blockedBy: T052]
- [X] T060 [US5] Wire `--version` on every applicable `.py` under `scripts/python/` (36 files, the checker excluded) via `scripts/python/script_interface_cli.py`, with the parse-order guard for every argparse and hand-rolled parser [blockedBy: T054,T033]
- [X] T061 [US5] Backfill the applicable scripts under `skills/*/*/scripts/` (16 `.sh` + 71 `.py` measured) through the same two mechanisms, leaving `scripts/` untouched and recording the per-file list in `.specify/specs/089-script-interface-contract/test-evidence/T058-skills-backfill.txt` [blockedBy: T057,T058]
- [X] T062 [US5] Raise `INSTRUCTIONS_BUDGET_BYTES` in `scripts/bash/generate-instructions.sh` only if the ambient section does not fit the measured 1 459 B headroom, by the smallest multiple of 1024 leaving ≥ 1024 B, recording old/new/measured/reason in the commit body [blockedBy: T022,T057] and re-pin every consumer count in `tests/contract/test_fast_fail_discipline.py` in the same edit
- [X] T063 [US5] Re-project every touched mirror with `sync-mirrors.py --write` and assert `--check` exits 0 with `--check-projection` green, including `tests/contract/test_mirror_parity_suite.py` which derives its parameters from the same declaration — runtime coverage: FR-022 [blockedBy: T024,T059]
- [X] T064 [US5] Prove SC-007 zero regression: capture one representative declared call per script family before and after the backfill and assert the diff is empty except added flag paths, into `.specify/specs/089-script-interface-contract/test-evidence/SC-007-zero-regression.txt` [blockedBy: T059,T024]
- [X] T065 [US5] Prove SC-011 on a copy tree: edit `pyproject.toml`, re-run every applicable `--version`, assert every line changes and is still `<script-name> <version>`, and the repository-wide literal scan stays at zero, into `.specify/specs/089-script-interface-contract/test-evidence/SC-011-version-source.txt` [blockedBy: T055]
- [X] T066 [US5] Pin the rejected-unknown-option limb on the incident script while both snapshot files stay untouched, into `.specify/specs/089-script-interface-contract/test-evidence/T068-incident-unknown-option.txt` [blockedBy: T055]
---

## Phase 5: User Story 6 - 豁免判据可机械判定，不被当逃生门 (Priority: P2)

**Goal**: the exempt set is the result of a run, not an author's claim — a bash library and an imported-only module land exempt, a module that acts on direct run lands applicable, and a mutation flips the verdict.

**Independent Test**: M-2 (bash library + guard + action → applicable), M-3 (python module's `__main__` removed → stays exempt), M-4 (python module given a real action → applicable), each read from the `applicable` field of the `--json` payload.

**Checkpoint**: `common.sh` and `declaration_reader.py` carry `applicable=false` with an evidence string, `generate-instructions.sh` carries `applicable=true` with a marker hit — the T-001 discriminating evidence.

- [X] T067 [US6] Implement the "must be a run, not a read" enforcement in `scripts/python/script-interface-check.py`: reject the three forbidden criteria (top-level statements, shebang word, self-description) and record which observation decided each file [blockedBy: T031] [green: contracts/script-interface-criteria.contract.md#C-3]
- [X] T068 [US6] Implement the silent-omission rule in `scripts/python/script-interface-check.py`: a candidate neither compliant nor exempt is a violation naming the missing limbs, and no "unevaluated" state may be counted as compliant [blockedBy: T066,T043] [green: contracts/script-interface-criteria.contract.md#C-12]
- [X] T069 [US6] Implement the exception-register recomputation in `scripts/python/script-interface-check.py`: path exists, path under `skills/external/<skill>/`, that `SKILL.md` declares `classification: external`, and all four columns present; any failing limb is `exception-unverifiable` at exit 1, and an unregistered third-party candidate is judged as an ordinary candidate [blockedBy: T008,T033,T067]
- [X] T070 [US6] Prove SC-009: `touch probe.sh` untracked and unignored in a copy tree → exit 1 naming it; add it to that tree's `.gitignore` → green and unnamed, into `.specify/specs/089-script-interface-contract/test-evidence/SC-009-candidate-coverage.txt` [blockedBy: T032,T039]
- [X] T071 [US6] Prove SC-010 with the three classification mutants on a sandbox copy, reading `applicable` before and after each, into `.specify/specs/089-script-interface-contract/test-evidence/SC-010-classification-mutants.txt` [blockedBy: T066]
- [X] T072 [US6] Prove SC-012 with the three exception-register mutants (a forged row with a missing path, an injected row whose skill does not declare `classification: external`, and the empty-register baseline) reading the exit code and the `exceptions[]` segment, into `.specify/specs/089-script-interface-contract/test-evidence/SC-012-declared-exceptions.txt` [blockedBy: T068]

---

## Phase 6: User Story 1 - 用 `--help` 看接口不再触发任何写盘 (Priority: P1)

**Goal**: `-h` / `--help` answers "what does this script do and what does it write" and changes nothing — proved on a sandbox copy, with help winning over any main action in either argument order.

**Independent Test**: on a sandbox copy of a writing script, run `-h` then `--help`; assert exit 0 for both, identical output bodies, and a byte-identical before/after snapshot pair (`git status --porcelain`, `sha256` of every `*.sh`/`*.py`, `.specify/` manifest).

**Checkpoint**: the incident's own memory (C-11) — a flag present anywhere on the command line beats the main action.

- [X] T073 [US1] Make the guard block the first executable block of `scripts/bash/script-interface.sh` consumers and record the insertion rule (before any `source`, before any `mkdir`/`git` write/manifest generation) in `shared/definitions/script-interface-definitions.md` [blockedBy: T055]
- [X] T074 [US1] Extract the one shared snapshot-and-compare function the zero-side-effect assertion runs on (status output + every `*.sh`/`*.py` hash + the `.specify/` manifest), in `tests/contract/test_script_interface_contract.py` [blockedBy: T036] — the same pair carries the help-wins-order comparison in both argument orders
- [X] T075 [US1] Prove SC-001 at closure scale — the before/after snapshot pair identical across `-h`, `--help`, `--version` and one unknown-option run for every applicable script, with the help-wins-order comparison read from the same pair — into `.specify/specs/089-script-interface-contract/test-evidence/SC-001-zero-side-effect.txt` [blockedBy: T033,T062,T073]

---

## Phase 7: User Story 2 - `--version` 让脚本身份可回答 (Priority: P1)

**Goal**: `--version` prints one line `<script-name> <framework-version>`, the version read from `pyproject.toml` at run time, exit 0, no action.

**Independent Test**: run `--version` on one bash and one python script; edit the copy tree's `pyproject.toml` version; assert both lines change and stay single-line; assert a zero-hit scan for a version-shaped literal inside any script body.

**Checkpoint**: exactly one source of the version (C-8); a copy with no reachable `pyproject.toml` prints `unknown` and still exits 0.

- [X] T076 [US2] Implement `script_interface_version_text` in the sourceable helper `scripts/bash/script-interface.sh`, its body inlined into the guard block through the `__SCRIPT_INTERFACE_VERSION_BODY__` sentinel so a script that cannot `source` still answers [blockedBy: T047,T050]

---

## Phase 8: User Story 3 - 未知选项被拒绝，而不是被执行 (Priority: P1)

**Goal**: an undeclared `-*` token exits non-zero, before the main action, printing an error and usage — including after a bare `--` boundary and including scripts that accept free-text positionals.

**Independent Test**: pass `--no-such-flag` to a writing script on a sandbox copy; assert non-zero exit, an error line plus usage on stderr, and the target untouched; repeat with a recognized option present (must still reject); then exercise the `--` boundary.

**Checkpoint**: `refresh-tools.sh`'s "usage printed then continued" shape and `getopts`'s stop-at-`--` behaviour are both excluded by construction.

- [X] T077 [US3] Verify the rejection limb on the live (non-probing) face: `--no-such-flag` exits non-zero, prints an error and usage on stderr, and no writing script's target changes on the sandbox copy, recorded in `.specify/specs/089-script-interface-contract/test-evidence/T075-rejection-face.txt` [blockedBy: T065,T075]

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: US7 (the guards that make a violation visible on an existing surface), the two count pins, the `tests/` dispositions, closure evidence and the feature records. The pins are migrations — they can only go green after the surfaces they count exist.

- [x] T078 Assert the wiring discipline in `tests/contract/test_script_interface_contract.py`: the new file is selected by the existing `pytest -m contract`, and no driver stage gate, confirmation gate or second checker was added — the only new executable artifacts are the five named in the clause [blockedBy: T040] [green: contracts/governance-landing.contract.md#C-32]
- [x] T079 Implement the mutation leg M-1 in `tests/contract/test_script_interface_contract.py`: delete one compliant script's `--help` arm in a sandbox copy, assert the check exits 1 and names that path on its own line, and that the finding is attributable to the mutation by inverting the pair — a finding the pair misses is a false green, recorded in `.specify/specs/089-script-interface-contract/test-evidence/SC-008-mutation.txt` [blockedBy: T077]
- [X] T080 Prove SC-003 at closure: full `--json` run with `violations=0`, `applicable + exempt == candidates`, every exemption carrying `basis` + `evidence`, into `.specify/specs/089-script-interface-contract/test-evidence/closure-check.json` [blockedBy: T063,T074,T079]
- [x] T081 Update `.specify/memory/features.md` (089 row status and stage record) and the feature detail `.specify/memory/features/089.md` in one edit [blockedBy: T080] — evidence: `.specify/memory/features.md` row 089 reads `Implemented` and `.specify/memory/features/089.md` exists
- [x] T082 [P] Assert that the owner page and `--emit-rule` agree on the label set and the class vocabulary in both directions, in `tests/contract/test_script_interface_contract.py` [blockedBy: T046,T066] [green: contracts/contract-checker-cli.contract.md#C-21]
- [X] T083 Read and judge every `tests/` candidate the classifier reports as carrying a `__main__` block (6 measured) plus `tests/conftest.py`, recording per-file disposition in `.specify/specs/089-script-interface-contract/test-evidence/T082-tests-disposition.txt` [blockedBy: T066,T070]
- [x] T084 Record the positional-flag regression guard (the `goal-utils.py` class: an option placed before the subcommand silently ignored) plus its position-independence assertion in `tests/contract/test_script_interface_contract.py` [blockedBy: T058,T077]
- [x] T085 Record the SC-005 / SC-006 readings and the smoke record in `.specify/specs/089-script-interface-contract/verification.md` with one `SC-NNN_status=` row per criterion, `deferred_tasks=` and the smoke fields [blockedBy: T018,T023,T026,T080] — evidence: .specify/specs/089-script-interface-contract/verification.md
- [x] T086 Run the closure full-suite comparison (`run-tests.sh --names-out` against `test-evidence/baseline-failed.txt`) and record it in `.specify/specs/089-script-interface-contract/test-evidence/closure-suite.txt` [blockedBy: T062,T080] — evidence: .specify/specs/089-script-interface-contract/verification.md
- [x] T087 Update the developer documentation that enumerates `scripts/python/` engines so the new checker is reachable from the documentation map, in `docs/reference/` [blockedBy: T040] — immediately followed by one final `sync-mirrors.py --write --only shared --only templates --only skills/internal` after every owner-page edit, with `--check` exiting 0 everywhere — evidence: .specify/specs/089-script-interface-contract/verification.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: starts immediately; T002 gates T004; T005 proves the sandbox every classification row depends on.
- **Phase 2 (Foundational)**: depends on Phase 1; blocks every story because four of the five landings are pointers to the owner page.
- **Phase 3 (US4)**: depends on Phase 2 only; file-disjoint from the rest, so it runs as a second track. T023 (live principle) gates T026 (section-count pin) and T028 (SC-005); T024 (instructions reconcile) gates T025 (mirror re-projection) and T026.
- **Phase 4 (US5)**: the engine rows depend on Phase 2 only; the mirror-projection rows (T050–T054) on T009/T011; the backfill rows (T055–T066) on the guard shapes and the engine's probes.
- **Phase 5 (US6)**: depends on Phase 4's engine — classification is a mode of that engine, not a second program.
- **Phase 6 (US1)**: depends on the guard body (T055) and the probe rows (T037); its closure row depends on the backfill projection (T063).
- **Phase 7 (US2)**: depends on Phase 4's CLI rows (T048) and the mirror projection (T051).
- **Phase 8 (US3)**: depends on Phase 6/7 (same guard block) and on the incident-script probe (T065).
- **Phase 9 (Polish)**: the closure and pin rows depend on Phase 3–6 surfaces; T085 records the readings the rest of the closure depends on.

### User Story Dependencies

- US1, US2, US3 are one mechanism in three limbs (one guard block, one bridge) — sequenced, not independent.
- US4 is independent of the others (governance surfaces only): an early deliverable even if the backfill stalls.
- US5 owns the engine and the backfill; US6 and US7 read its verdict fields.
- Phase order ≠ delivery order: the four P1 stories US1–US4 are the MVP (see § Implementation Strategy); US5 is the largest single story and ships after them.

### Within Each Story

- Test rows come first and must be red before the implementation row that turns them green.
- Migration rows (T017 double-landing counts, T026 section counts, T063 mirror re-projection, T062 the budget pin) sit AFTER the surfaces they count, carrying an explicit `[blockedBy:]` — the tests-mode migration exception. This is also why they are row-order-late and not row-order-early: a pin that moves first is a pin that measures nothing.
- The models→services→endpoints order does not apply here; the doc-feature taxonomy (author-section → mirror-parity → render-verify → refresh-verify) is what Phase 3 follows.

### Parallel Opportunities

- Phase 3 tests: T012–T016 are the parallel band (four different-file rows plus the shared test file adjudicated in Notes); T017–T019 are sequenced after them because they read back what T012/T015 land.
- Phase 4: T059 (bash generator) and T060 (python wiring) are parallel (disjoint file trees) and are the only true parallel pair in that phase — every other row either writes the engine or the one shared contract test.
- Phase 9: T082 is the sole `[P]` row (`tests/contract/test_constitution_double_landing.py` sits outside it; its write target is written by no other parallel row).
- Whole-story: US4 runs parallel to the US1–US3 track whenever two people are available.

## Parallel Example: Phase 3 (US4)

```bash
# Six clause-partitioned assertion groups, one row each, one test file:
SPECKIT_PYTHON=/usr/bin/python3 /usr/bin/python3 -m pytest -m contract \
  tests/contract/test_script_interface_contract.py -q \
  -k "owner_page or template_principle or live_principle or mandate or ambient"

# Then three file-disjoint landings:
#   T020 templates/constitution-template.md
#   T021 skills/internal/manage-constitution/SKILL.md
#   T022 templates/instructions-template.md
```

## Implementation Strategy

### MVP First

**MVP scope rule**: the MVP is the smallest set of same-priority stories whose checkpoints are each independently testable. This feature has five P1 stories, and the incident-class defect (an unknown option silently executed) is only closed by three of them together:

1. Phase 1 + Phase 2 (Setup + Foundational) — nothing ships before the owner page exists.
2. **MVP = US4 + US1 + US3**: the rule reaches downstream projects (US4), flags are free (US1), and unknown options are rejected (US3). After this, `generate-instructions.sh --help` is safe and the failure class is gone.
3. Then US2 (version identity), US5 (engine + backfill), US6 (classification mutants), US7 + Polish (guards and closure).

**STOP and VALIDATE at the MVP boundary**: T057 (incident script), T065 (unknown option), T027 (downstream init) and T028 (`git show` on the amendment) are the four independent checks.

### Incremental Delivery

1. Phase 1 + 2 → owner page + helper → the checker can read the rule.
2. US4 → templates and live constitution carry the rule; downstream projects receive it.
3. US1 + US3 → the incident script stops being an incident.
4. US2 → every script answers `--version` from one source.
5. US5 → the engine exists, the backfill lands through generators, `violations=0`.
6. US6 → the basis vocabulary is falsifiable by mutation.
7. US7 + Polish → pins move, closure evidence lands, feature records update.

### Parallel Team Strategy

- Developer A: US4 (the governance surfaces + their contract tests) — file-disjoint from everyone else.
- Developer B: the checker engine (Phase 4's engine and CLI rows) once the owner page exists.
- Developer C: the guard block and bridge (T055–T057) after the engine's help probe exists.
- After B and C land: one developer owns the bash backfill (T059), another the python backfill (T060) — disjoint file trees.

## Tasks → Traceability (FR / SC)

Every FR-001…FR-031 and SC-001…SC-012 is claimed by at least one row. FR-028 is the tombstone (`requirements.md` § 承重定义条款): it carries no obligation and is satisfied by this table naming it, never by code.

| FR | Requirement (short) | Task rows |
|----|---------------------|-----------|
| FR-001 | One general governance rule, as a principle on both constitution sides plus an ambient section | T020, T022, T023 |
| FR-002 | Candidate set from machine-readable sources, never a hand list | T025, T030, T067 |
| FR-003 | `-h`/`--help` with usage, options, side effects, exit codes | T036, T055, T058, T060 |
| FR-004 | `--version`, one parseable line, single source | T037, T052, T076 |
| FR-005 | Flags present ⇒ no action, no write, no backup, judgement before any side effect | T070, T071, T072 |
| FR-006 | Unknown options rejected non-zero, never silently ignored | T038, T055, T065, T077 |
| FR-007 | `*` tokens rejected even for free-text scripts; `--` boundary respected | T038, T077, T084 |
| FR-008 | No-argument call prints usage and exits non-zero | T038, T055 |
| FR-009 | Exemption decided by run semantics, not source literals | T033, T034, T068 |
| FR-010 | Deterministic repository check with four conclusions and a violation count | T032, T041, T044, T080 |
| FR-011 | New principle in `templates/constitution-template.md`, pointer plus points | T013, T020 |
| FR-012 | Ambient section in `templates/instructions-template.md` and the live file, same shape | T016, T022, T024 |
| FR-013 | Live constitution: principle + Sync Impact Report + MINOR + Last Amended | T014, T023, T026 |
| FR-014 | `manage-constitution` MUST-include entry | T015, T021 |
| FR-015 | Exactly one owner document; other surfaces reference it | T006, T007, T009, T012 |
| FR-016 | Five landings consistent, judged by the existing guard's pins and watchlist | T017, T079, T085 |
| FR-017 | Existing applicable scripts backfilled; violations 0; exemptions carry evidence | T058, T059, T060, T061, T080 |
| FR-018 | Existing option semantics, JSON shapes and exit codes unchanged | T062, T064, T084 |
| FR-019 | The incident script: `--help` free, unknown option rejected | T057, T058, T065, T066 |
| FR-020 | Third-party scripts via minimal entry layers or named declared exceptions | T069, T072 |
| FR-021 | Check wired into the existing verification surface, no new gate step | T078, T079 |
| FR-022 | Mirrors re-projected, zero drift | T025, T063, T087 |
| FR-023 | Rule wording covers framework + downstream + third-party | T020, T022 |
| FR-024 | Candidate derivation + coverage assertion + no silent exclusion + mirror copies judged | T010, T025, T030, T031, T067 |
| FR-025 | bash entry-point criterion: code after the guard executes | T034, T068 |
| FR-026 | python entry-point criterion: a run that really acts | T034, T068, T069 |
| FR-027 | Third-party criterion (two conditions at once) and the two-hats rule | T007, T069 |
| FR-028 | Tombstone — no obligation carried | this table only (no code row) |
| FR-029 | Zero-side-effect capture on a sandbox copy; flag judgement before any side effect | T039, T070, T071, T072 |
| FR-030 | Mirror equality as `source ≡ mirror`; downstream side self-sufficient | T050, T051, T063 |
| FR-031 | New stdlib engine plus new contract test, no driver gate | T032, T042, T078 |
| SC-001 | Every applicable script: three flags exit 0, tree fingerprint zero diff | T073, T075 |
| SC-002 | Incident script: zero byte change to instructions and `.gitignore`; unknown option non-zero | T058 |
| SC-003 | Check reports every candidate, violations 0, exemptions with evidence | T080 |
| SC-004 | Clean downstream project gets the principle and the ambient section from the generators | T027 |
| SC-005 | MINOR bump + Sync Impact Report + Last Amended in one commit | T023, T028, T085 |
| SC-006 | Existing guard pins and watchlist pass; mandate count matches the rosters | T017, T021, T026, T085 |
| SC-007 | Zero regression in declared options, JSON shapes, exit codes | T064 |
| SC-008 | Deleting a help arm goes red and names the script; zero false greens | T079 |
| SC-009 | Untracked, unignored file ⇒ error naming it; ignored ⇒ green | T070 |
| SC-010 | Three classification mutants flip `applicable` | T071 |
| SC-011 | `pyproject.toml` edit changes every `--version`; zero literal hits | T065 |
| SC-012 | Forged or injected-unrecomputable exception rows produce an error and a visible `exceptions[]` | T072 |
## Phase 10: Supplementary — probe sandbox boundary (2026-11-08 RCA)

- [X] T088 Pin the probe sandbox's repository boundary in `scripts/python/script-interface-check.py`: `_probe_env` sets `GIT_CEILING_DIRECTORIES` to the sandbox tree and `TMPDIR`/`TMP` inside the sandbox, and the measured-tree copy gets a `.git` marker at its root so `git rev-parse --show-toplevel` cannot walk above the copy. [blockedBy: T039] [green: contracts/script-interface-criteria.contract.md#C-10]
- [X] T089 Add a real-repository escape assertion in `scripts/python/script-interface-check.py`: snapshot `git for-each-ref` + the `.specify/specs` listing before and after the probe phase; any difference is a `probe-escaped` finding at exit 1, never a silent continue. [blockedBy: T088] [green: contracts/script-interface-criteria.contract.md#C-13]
- [X] T090 Contract tests: (a) `_probe_env` carries the git ceiling and a sandbox-local TMP; (b) a fixture script that resolves its repo root and writes a branch/spec leaves the measured tree unchanged after a probed run; (c) a forced absolute-path escape is reported as `probe-escaped` at exit 1. [blockedBy: T089] [green: contracts/script-interface-criteria.contract.md#C-10] [green: contracts/script-interface-criteria.contract.md#C-13]
- [X] T091 Add a deterministic workspace guard `scripts/python/workspace-guard.py` (`--snapshot FILE`, `--check FILE`, stdlib, `-h/--help`, `--version`) and make it a fixed checkpoint item: after every stage/package the current branch and `.specify/specs` listing MUST match the pre-stage snapshot. [blockedBy: T088]
- [X] T092 Re-measure SC-001 with the contained checker and replace the unsafe-harness evidence: every proof run MUST execute only the sandbox copy and MUST NOT pass an operand to a write-on-operand script. Record the denominator, the per-family readings and the workspace-guard snapshot pair. [blockedBy: T088,T089]
- [X] T093 Make `scripts/bash/create-new-requirements.sh` honour a bare `--` non-interactively: a token after `--` is an operand (the feature description), a run with no usable input MUST exit non-zero with usage instead of waiting on stdin, and a regression test pins both. [blockedBy: T077]

**RCA addendum (2026-11-08, recurrence).** The first containment attempt seeded `.git` in the sandbox and pinned `GIT_CEILING_DIRECTORIES`, but the flag probes still ran the script IN PLACE (the measured path), so the candidate's own `find_repo_root` walked up from the real `scripts/bash/` to the measured repository. A controlled run created 40 branches; the 5b package created 113 more. The fix is that every executable probe now runs the sandbox COPY (which carries `.specify/`, `pyproject.toml` and the seeded `.git`) and fingerprints that copy; a fresh controlled run leaves the measured repository unchanged. The 5b SC-001 evidence was produced by a harness that passed the separator operand to scripts; T092 re-measures it under the contained checker.

- [X] T094 Sweep every backfilled shell script that had its own `usage()` body and make the guard print THAT body (plus the four labels): the generic `_sig_usage` replaced `watch-target.sh`'s and `stage-runner.sh`'s original help text and broke the pre-existing driver efficiency tests. Add a contract test that each such script's help still contains its original option/exit-code tokens. [blockedBy: T059]

## Root-cause record (2026-11-08)

The 2026-11-07 incident created 40 branches/spec dirs because the probe ran a candidate that writes on an operand (`create-new-requirements.sh`) inside a sandbox that had no `.git`; the candidate's `git rev-parse --show-toplevel` escaped to the measured repository. T088/T089/T090 close the mechanism, T091 makes the state drift visible after every package.


## Notes

- **Assumptions taken this stage** (unattended run — recorded, not asked):
  1. `feature-ref.md` § 3's FR→contract mapping was mis-keyed at generation time; it was rewritten against `requirements.md` during analyze round 2 (2026-11-06) and now matches the FR owner.
  2. SC-005 is `supporting` on every surface (`requirements.md`, `feature-ref.md`); `plan.md`'s measurement table has no Path column. GATE-4 therefore does not gate on it.
  3. `plan.md` § Implementation Slicing names eight slices while the delivery brief names nine faces (the instructions reconcile is a face of S5/S7). Mapped in § Delivery Slice Map rather than by re-slicing the plan.
  4. The checks my brief names (`validate-tasks` decomposition output, `stage-status`) resolve to `.specify/scripts/python/validate-tasks.py`, `.specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks`, and this file's own GATE-3 plus the checkpoint the driver writes. No `stage-status` engine exists in this tree; the driver owns that record and this stage does not write the state spine.
- **`[P]` discipline**: `[P]` is declared only inside a phase, because `validate-tasks.py` scores it per phase. Where several rows legitimately write one shared test file (`tests/contract/test_script_interface_contract.py`), the rows carry NO `[P]` — two `[P]` rows writing one file is a false parallel claim — and are sequenced by `[blockedBy:]` instead. One residual `parallel-safe` WARN survives by adjudication: T012 and T016 both cite that shared file, and T012 is the first row that creates it. The only `[P]` row in Phase 9 (T082) writes a file no other `[P]` row in its phase writes.
- **Deferral discipline**: prefer `[~]` with a recorded reason over leaving a row `[ ]`; T027 (downstream `specify init`) is the one row with a declared degraded path if the CLI entrypoint is unavailable at implement entry.
- Commit after each task or logical group; never commit a hand-edited mirror.
- **Two phases keep their contract clauses without a dedicated validator row**: Phase 6 (US1) and Phase 7 (US2) carry no dedicated `[green:]` row — their assertions were written as probe rows inside the engine (T036, T037, T038, T039, T040) because the engine IS the mechanism that turns C-7/C-8/C-9/C-10/C-11 green; the phase rows there are the evidence rows that prove it at closure scale. Phase 8 (US3) is in the same position: T038 is the rejection probe and T077 is its live-face verification.
- **Residual `green-cross-phase` WARNs are structural, not defects**: the validator compares every `[green:]` claim inside one contract across the *whole file* in row order, while this feature re-cut its two large contracts into one test file per document. Three consequences are irreducible without inventing a second test file per story: (a) a red-first contract test that must precede the engine work can carry a higher clause ordinal than the engine row it is red against (T033/C-6 before T034/C-4; T053/C-37 before T054/C-33); (b) a Phase 4 criteria claim (T041/C-13) precedes a Phase 5 criteria claim (T067/C-12) because US6 is a later priority; (c) the C-21 guard row (T082, Phase 9) follows the C-22 implementation row (T049, Phase 4) because the both-directions agreement is asserted at closure, not during engine construction. Every one of the 38 clauses is claimed exactly once, and each sits on the row that owns its work — `--emit-rule`'s own implementation row (T048) therefore carries no `[green:]`, since C-21 is claimed by the guard that falsifies it.
- **Validator residue measured after the design repair (2026-11-06)**: `validate-tasks.py` → `PASS (with warnings)`, 0 error(s), **62 warning(s)** = 55 `green-path-divergence` (11 claim rows legitimately write the one shared contract-test file → C(11,2) pairs), 4 `green-cross-phase` (the structural classes above), 2 forward `blockedBy` (T019→T065, T033→T040, both intentional sequencing), 1 `parallel-safe` (T012/T016, adjudicated). The 73 reading was superseded when analyze round 2 moved C-6 from T033 to T034.
- This file is the 87-row numbering; the Delivery Slice Map, § Dependencies, § Implementation Strategy and the traceability table all name rows by ID, so any later re-cut MUST amend them together (rerun = validate-and-amend, never renumber).
- **US7 placement**: US7 (「违规在已有面上可见」) has no code of its own — its two obligations are assertions that the check sits on the existing surface (T078) and that a removed help arm goes red (T079). Both are assertion rows over files owned by US5's engine, so they live in Phase 9 next to the closure evidence they enable, and GATE/DoD carry the US7 acceptance reading. `validate-tasks.py` requires non-story phases to carry zero `[US…]` markers, so the rows are unlabelled there; an `[US7]` marker in Phase 9 is a structural error, not a stricter trace.
- **The decomposition ceiling vs this file's 87 rows** — *superseded by b6bb7356 (ceiling 120/160); re-measured 2026-11-06 → proceed.* Dated record of what happened (2026-11-06, at generation, against the then-current ceilings): `.specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks` reported `split-required` because `task rows=87 exceeds ceiling 80` (FR definitions measured: 31, ceiling 60 — that limb passed). That stage neither split nor padded, because `plan.md` fixes nine delivery faces and `contracts/` fixes 38 must-hold clauses, so one row per clause plus the setup/baseline, backfill and closure rows lands at 87, and `efficiency-model.md` § 5.4 forbids the producing stage from deleting, merging or reordering requirements to duck a limit. Commit `b6bb7356` then raised the ceilings to `FR_CEILING = 120` / `TASK_CEILING = 160`; re-measured on 2026-11-06 the same command returns `proceed` (`fr_count=31`, `task_count=87`), recorded in `test-evidence/tasks-decomposition.json`. The `split-required` verdict is history, not the current state.

### Anomalies surfaced (not repaired here)

- `ANOMALY A-1` — *repaired 2026-11-06 in `plan.md`.* At generation, `plan.md` § Risks 9 stated that **five** python scripts have hand-rolled parsers. Measured: **two** have no `argparse` (`clause_extract.py`, `gate-check.py`); `validate-decision-tensions.py`, `validate-falsification-quartet.py` and `validate-requirements.py` import `argparse` and call `parse_args(sys.argv[1:])`, i.e. ordinary `argparse` users. `requirements.md` had already carried the corrected reading (35 `argparse` + 2 self-parsing); `plan.md` § Risks 9 and its S6 slice now carry it too, and `quickstart.md` S-6 states the same. T056 and T060 cover whichever set the classifier measures. No uncorrected statement of this premise remains.
- `ANOMALY A-2`: the `tests/` corpus counts quoted by `research.md` R7 and `plan.md` § Risks 11 (431 without a `__main__` block, 7 modules carrying one) differ from this stage's measurement and from `requirements.md`: 447 `.py` under `tests/` (449 candidates with the 2 `.sh`), **6** carrying a `__main__` block — 5 of them under `tests/fixtures/` plus `tests/contract/test_migration_distribution.py` — and **441** without. `research.md` R7 and `plan.md` § Risks 11 were corrected on 2026-11-06; T083 judges the measured set.
- `ANOMALY A-3`: `requirements.md` FR-030's older wording required mirror copies to be byte-identical, which the declared projection (T050–T054, C-34…C-38) deliberately weakens to `mirror == project(source)`. FR-030 now carries the two-class reading (unprojected ⇒ byte-equal; projected ⇒ `source + declared projection`), so the plan's C-33…C-38 and the requirement agree.
