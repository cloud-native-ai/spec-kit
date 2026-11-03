# Tasks: Stricter Acceptance & Artifact Review（更严格的验收与产物审查）— Slice 081a

**Requirement ID**: 081
**Requirement Key**: 081-acceptance-hardening
**Related Feature**: 081 更严格的验收与产物审查（Stricter Acceptance & Artifact Review）
**Input**: Design documents from `.specify/specs/081-acceptance-hardening/`
**Prerequisites**: plan.md (required), requirements.md (required), research.md, data-model.md, contracts/ (5 files), quickstart.md, baseline-failed.txt

**Tests Mode**: ON — Constitution Principle IV "Test-First & Contract-Driven Implementation" is MUST-level (`Pure functions/utilities MUST have unit tests`, `Critical flows MUST have automated regression coverage`, `Integration/contract tests MUST cover cross-service communication`), and plan.md § Constitution Check row IV already commits the five red-first contract test paths. Every new deterministic judgement therefore lands with a contract test that goes red before its implementation row closes.

**Scope**: this file covers **slice 081a only** (plan.md § D10: "US1 + the shared core"). Slices 081b–081d are recorded in `## Deferred Slices` as future work, not as tasks. The slice boundary and its status consequence are stated once in `## Slice Boundary`.

## Definition of Done (DoD)

- DoD-1: Every 081a row's stated artifact exists at the path the row names, and every edited framework source has a regenerated mirror / per-tool copy
- DoD-2: The 081a contract tests (`test_closure_acceptance_check.py`, `test_requirements_checker.py` path-marker cases, `test_acceptance_state_machine.py`, `test_gate_wiring_081.py`) are green, and none of the four was green before its implementation row
- DoD-3: The closure checker is stdlib-only, read-only, and exits 0 / 1 / 2 with no fourth verdict and no reason outside the seven-value closed set
- DoD-4: `python3 scripts/python/regen-command-copies.py --check` and `python3 scripts/python/sync-mirrors.py --check` both exit 0 on the post-change tree
- DoD-5: The feature status is exactly `Blocked` at the end of this slice — never `Implemented`, and never the pre-slice `Planned`: both the `.specify/memory/features.md` row (column 5) and `.specify/memory/features/081.md` `**Status**` read `Blocked` (T020 lands the `Planned → Blocked` transition), and the reason is visible in `verification.md` (see `## Slice Boundary`)
- DoD-6: No new failing test at **set level** — `head 失败集 − 基线失败集` is empty, and `基线失败集 − head 失败集` is enumerated row by row as fixed items, against `baseline-failed.txt` (39 ids, plan-stage capture). The comparison unit is the failing test **id set**, never a count and never a byte diff (SC-009 ②). It is **assessable at this slice's close**: T022 runs the full suite with `--names-out` and performs the id-level set difference (the baseline is the plan-stage capture and is not re-run). The slice's own narrower observation — GATE-1's four modules green — is recorded separately and MUST NOT stand in for the set-level invariant; 081d re-runs the same comparison over the final tree for the feature-level claim (FR-023)

**DoD Status**: pending

## Completion Gate

- GATE-1: The four 081a contract modules are green — check: `bash scripts/bash/run-tests.sh tests/contract/test_closure_acceptance_check.py tests/contract/test_requirements_checker.py tests/contract/test_acceptance_state_machine.py tests/contract/test_gate_wiring_081.py -q`
- GATE-2: Mirror and per-tool-copy parity holds — check: `python3 scripts/python/regen-command-copies.py --check` and `python3 scripts/python/sync-mirrors.py --check` both exit 0
- GATE-3: No `[ ]` or `[>]` task rows remain — check: `grep -cE '^- \[[ >]\]' .specify/specs/081-acceptance-hardening/tasks.md` returns 0
- GATE-4: The slice's single smoke command passes twice with the same exit code — check: `bash scripts/bash/run-tests.sh tests/integration/test_acceptance_smoke.py -q` run twice, identical exit status, evidence at `.specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt`
- GATE-5: The registry status reads exactly `Blocked` after this slice — check: `awk -F'|' '$2 ~ /^ *081 *$/ {print $5}' .specify/memory/features.md` prints ` Blocked ` (the padded cell, asserted by exact match). `Implemented` **and** the pre-slice `Planned` both FAIL this check, so an untouched registry can no longer pass it
- GATE-6: The checker refuses this feature and does not read it as accepted — check: `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/081-acceptance-hardening` exits 1 with `zero-final-path-pass` once T020 has seeded `verification.md` (before T020 it exits 2 as an input error, never 0)
- GATE-7: No new failing test id appears at set level — check: T022's `head` id set minus `baseline-failed.txt` is empty, and the pins re-read before the comparison still match `test-evidence/plan-runner-pins.txt` (a mismatch invalidates the comparison as an input error, it is never read as new failures — FR-023)

## Environment Prerequisites

- pytest runner — available — probe: `.venv/bin/python -m pytest --version` @ 2026-11-03 → `pytest 9.2.0` on CPython 3.14.6; affected phases/tasks: all test rows (T007–T010, T017)
- `specify` console script — available — probe: `ls -l .venv/bin/specify && .venv/bin/specify --help` @ 2026-11-03 → executable present, Typer help exits 0; affected phases/tasks: T002, T017 (smoke sub-check A)
- `git` — available — probe: `git --version` @ 2026-11-03 → `git version 2.54.0 (Apple Git-157)`; affected phases/tasks: T018, T019 (tree-difference and porcelain checks)
- mirror engines — available — probe: `python3 scripts/python/regen-command-copies.py --check` and `python3 scripts/python/sync-mirrors.py --check` @ 2026-11-03 → both exit 0 on the pre-change tree; affected phases/tasks: T018

Planning-time premises are NOT restated here — they live in `plan.md` § Execution Premises (EP-001…EP-009). Boundary owner: `shared/workflow/acceptance-hardening.md` § Gates (A13).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (`[US1]` only in this slice — 081a is the US1 slice)
- **[blockedBy: T001,T002]**: this row MUST NOT start until every listed task is `[X]`
- Include exact file paths in descriptions; keep each task row on ONE line
- `[green: <contract>#<clause>]` is not used in this slice: every contract it touches is claimed by exactly one row set inside a single slice, so there is no cross-phase green point to partition

**Tests Mode note**: the four test rows below come before their implementation rows. Tests for *new* behaviour are strictly red-first; the gate-wiring test (T010) asserts the runtime-reachable invocation, so it is red until T016 lands — that ordering is deliberate and is why T016 carries T007 and T010 as blockers.

## Task State Sigil

`- [ ]` open · `- [>]` claimed · `- [X]` closed · `- [~]` deferred (reason recorded in `verification.md` `deferred_tasks=`).

## Path Conventions

Single project: framework sources at repository root (`templates/`, `shared/`, `skills/`, `scripts/`, `src/`, `tests/`); `.specify/` copies are generated mirrors (`.specify/templates/`, `.specify/shared/`, `.specify/skills/`, `.specify/scripts/`); per-tool command copies live in `.claude/commands/`, `.github/prompts/`, `.qoder/commands/`, `.opencode/command/`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Freeze the slice's measurement points, remove the one measured environment blocker, and author the declarative fixture inputs every later row is proved on.

- [X] T001 [P] Create the slice's runtime-evidence landing points at `.specify/specs/081-acceptance-hardening/notes/red-first-evidence.md` (per-test command, real output, exit status for each red-first contract test) and `.specify/specs/081-acceptance-hardening/notes/pre-change-measurements.md` (the frozen pre-change side, recorded by pointer to `test-evidence/plan-baseline-run.txt` for the 39 failed / 6970 passed / 7 skipped baseline and to `test-evidence/plan-runner-pins.txt` for the pytest and git pins — do not re-run the full suite)
- [X] T002 [P] Add the repo-root fallback to `get_resource_path()` in `src/specify_cli/__init__.py` so a development checkout resolves working-tree templates while the installed layout keeps precedence (plan § T-005; EP-002 is `falsified` with `Decision: resolve-in-scope`); no mirror duty (`src/` is outside `MIRROR_PAIRS`)
- [X] T003 [P] Author the two declarative fixture sets `tests/fixtures/acceptance-hardening/negative/` (the 026 shape: zero `[ ]`, a status row per SC, every `final`-path SC `blocked`/`deferred`) and `tests/fixtures/acceptance-hardening/positive/` (every `final`-path SC `pass`, complete three-field smoke record, valid runtime rows, all premises `verified`) — each a minimal file set (`requirements.md`, `plan.md`, `tasks.md`, `verification.md`, a feature detail, a registry row) and neither referencing a real feature directory (shape per the fixture-set table in this slice's data model, § Fixture set)
- [X] T004 [P] Author the two mutation fixtures `tests/fixtures/acceptance-hardening/ladder-mutation/` (a `blocked` row carrying all five required ladder fields with `SC-NNN_reduced_measurement` non-empty while `SC-NNN_reduced_measurement_run=no`) and `tests/fixtures/acceptance-hardening/smoke-mutation/` (`positive` with the smoke record deleted **and the claimed status set to `Implemented`**, so the claimed-but-not-accepted reason has a counter-example — `zero-final-path-pass` cannot fire here, since every `final`-path SC still passes), as minimal file sets on the same shape as T003
- [X] T021 [P] Author the three path-mix fixtures that give the `final` / `supporting` boundary rule a counter-example (Edge Case "final 与 supporting 混合"; V-1, V-11): `tests/fixtures/acceptance-hardening/mixed-path/` (an `execution` feature with `SC-001` `final` `pass`, `SC-002` `final` `fail`, `SC-003` `supporting` `deferred` carrying the full ladder), `tests/fixtures/acceptance-hardening/expr-supporting-only/` (an `expression` feature whose SCs are all `supporting`, one `deferred` with the full ladder) and `tests/fixtures/acceptance-hardening/execution-without-final/` (an `execution` feature whose SCs are all `supporting`) — each a minimal file set on the same shape as T003, none referencing a real feature directory (shape per the fixture-set table in this slice's data model, § Fixture set)

**Checkpoint**: the fixture inputs and the measurement landing points exist; every later assertion has something deterministic to read.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The single schema owner and the checker's calling surface. No US1 row can start before these two exist, because every other row either points at the owner doc or exercises the checker.

**⚠️ CRITICAL**: No user-story row may start until T005 and T006 are closed.

- [X] T005 Create the schema owner document `shared/workflow/acceptance-hardening.md` carrying ONLY the sections this slice owns — `§ Feature Status` (the `Blocked` value + the four transitions + the narrow `Implemented → Blocked` audit-correction exception + the four conjunctive `Planned → Implemented` conditions), `§ Verification Vocabulary` (the six-value status set, the five measurement-ladder fields, the illegal-row rule, the three-field smoke record), `§ Gates` (the fourth `Implemented → Ready for Review` condition, the A13 three-carrier boundary), `§ Closure Verdict` (the binary verdict, the seven-value closed reason set as templates + the instance/membership rule, the three exit codes, the `final_path` counts, and the **feature-line-closure** timing of the judgement) — plus clearly marked extension points for the sections 081b/081c/081d add: `§ Execution Premises` and `§ Inherited Blockers` (081b — **the `inherited` disposition's carrier obligation is owned by `requirements.md` FR-011 and lands in that section; this slice leaves only the extension point and MUST NOT leave the obligation undefined anywhere**), `§ Review Composition` (081c). Mirror: `.specify/shared/workflow/acceptance-hardening.md` via `python3 scripts/python/sync-mirrors.py`
- [X] T006 Create `scripts/python/closure-acceptance-check.py` with its stable calling surface only — `--spec-dir` (required), `--repo`, `--feature-detail` / `--feature-registry`, `--audit-existing`, `--json` / `--json-out`, repeatable `--waive CODE:TARGET`; exit `2` with a message naming the path when an input is missing or unparsable; no verdict logic yet (contracts/closure-acceptance-check.contract.md C-01…C-06, C-10); mirror: `.specify/scripts/python/closure-acceptance-check.py` (that pair is `STRICT` — an extra mirror-only file fails `--check`)

**Checkpoint**: the owner doc and the CLI surface exist; US1 rows can now be written against them.

---

## Phase 3: User Story 1 - final 路径没通过就不叫「实现了」，而且必须有 smoke test (Priority: P1)

**Goal**: `Planned → Implemented` becomes four conjunctive conditions (zero `[ ]`; a status row per SC; every `final`-path SC `pass`; the smoke record `pass`), `Blocked` becomes a first-class feature status, the verification vocabulary gains `blocked` with its five-field measurement ladder, and one deterministic script — `scripts/python/closure-acceptance-check.py` — produces the shared verdict at the **implement** call site.

**Independent Test**: run `python3 scripts/python/closure-acceptance-check.py --spec-dir tests/fixtures/acceptance-hardening/negative --json` at the implement gate path and observe `verdict: block` with `zero-final-path-pass` in a reason set drawn from the seven-value closed set, exit 1; run the same command on `tests/fixtures/acceptance-hardening/positive` and observe `accept`, exit 0. This proves 1 of SC-001's 3 required call points — see `## Slice Boundary`.

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: write these FIRST; each MUST fail before its implementation row closes.**

- [X] T007 [P] [US1] [blockedBy: T003,T004,T021] Author the checker contract test `tests/contract/test_closure_acceptance_check.py` covering `positive` → `accept` / exit 0, `negative` → `block` / exit 1 with `zero-final-path-pass`, `ladder-mutation` → `blocked-without-measurement-ladder: SC-NNN`, **`smoke-mutation` → `block` / exit 1 with `status-claims-implemented-but-blocked`** (the claimed status is `Implemented` and the smoke record is gone, so this is the only fixture that exercises the claimed-but-not-accepted reason), **`execution-without-final` → `block` / exit 1 with `zero-final-path-pass`** (`final_path.total = 0`), `mixed-path` → `block` whose reason is `final-path-not-pass: SC-NNN` naming `SC-002` and **not** `zero-final-path-pass`, with the lone non-`pass` `supporting` SC producing no reason of its own, `expr-supporting-only` → no `final`-path reason and no requirement to invent a `final` SC, a missing input → exit 2 (never `block`), **every reported reason satisfying the two-part membership test of requirements § Shared Strings (template match plus a well-formed argument of the template's grammar), not a byte-equality test against a table cell**, `final_path` counts computed once by the script, and the `--waive CODE:TARGET` grammar removing a reason from the blocking set while counting it as waived (clauses C-01…C-09, C-13…C-16; V-5, V-6, V-11, V-12, V-14)
- [X] T008 [P] [US1] Extend `tests/contract/test_requirements_checker.py` with the sixth check label `path-marker`: a missing marker, a second `**Path**` on the same line, and a value outside `final` / `supporting` each fail with file and line; the existing five labels keep their meanings; an `execution`-class feature with zero `final`-path SC fails while an `expression`-class one is not forced to invent one (clauses AS-01…AS-04; V-1…V-3)
- [X] T009 [P] [US1] Author the state-machine and vocabulary contract test `tests/contract/test_acceptance_state_machine.py` asserting, in `templates/feature-details-template.md` § Canonical Status State Machine, the four conjunctive `Planned → Implemented` conditions, the four `Blocked` rows including the explicitly **illegal** `Blocked → Ready for Review`, the narrow `Implemented → Blocked` audit exception with its cited-evidence requirement, the fourth `Implemented → Ready for Review` condition, and the `[FEATURE_STATUS]` token carrying `Blocked`; plus, in `templates/verification-log-template.md`, the six-value status set with the one-sentence `blocked` vs `deferred` distinction, the five ladder fields, the illegal-row rule, and the exactly-one three-field smoke record (clauses SV-03…SV-11; V-4…V-10, V-23, V-24)
- [X] T010 [P] [US1] Author the gate-wiring contract test `tests/contract/test_gate_wiring_081.py` covering the **implement call site only**: the invocation `scripts/python/closure-acceptance-check.py` is named by `skills/internal/implement-feature/SKILL.md` **Step 9 — Pre-Status-Flip Gate and Verification Log** (the step where the status is actually landed) and by `shared/workflow/feature-integration.md` § Pre-Status-Flip Gate, the same invocation extracts and runs against `tests/fixtures/acceptance-hardening/negative` (block, and the gate must then land `Blocked`, never `Implemented`) and against `positive` (accept), and no second judgement source (a different script, an ad-hoc grep, a model call) is offered by either carrier; the review and driver call sites are asserted as absent-with-reason here and are 081c / 081d work (clauses GW-01, GW-04)

### Implementation for User Story 1

- [X] T011 [US1] [blockedBy: T008] Add the `path-marker` check as the sixth label in `scripts/python/validate-requirements.py`, reporting file and line and leaving the existing five labels untouched (clauses AS-02; V-2); mirror: `.specify/scripts/python/validate-requirements.py` via `python3 scripts/python/sync-mirrors.py`
- [X] T012 [US1] [blockedBy: T009] Rewrite `templates/feature-details-template.md` § Canonical Status State Machine: four conjunctive `Planned → Implemented` conditions, the `Planned → Blocked` / `Blocked → Implemented` / `Blocked → Ready for Review` (illegal) / `Implemented → Blocked` (audit correction, must cite evidence) rows, the fourth `Implemented → Ready for Review` condition stated **in this owner block only**, and `Blocked` in the `[FEATURE_STATUS]` glossary token; every other artifact reaches these by pointer, never by copy (D3 row 1; SV-03…SV-07); mirror: `.specify/templates/feature-details-template.md`
- [X] T013 [US1] [blockedBy: T009] Rewrite `templates/verification-log-template.md`: the six-value status set `pass|fail|partial|blocked|deferred|unknown`, the `blocked` vs `deferred` distinction (feature not acceptable vs feature still acceptable on a `supporting` path), the five ladder fields under their `SC-NNN_`-prefixed names (`SC-NNN_blocked_at`, `SC-NNN_reduced_measurement`, `SC-NNN_reduced_measurement_run`, `SC-NNN_why_reduced_insufficient`, `SC-NNN_unblock`) for `blocked`/`deferred`/`partial`, the illegal-row rule (`SC-NNN_reduced_measurement` non-empty AND `SC-NNN_reduced_measurement_run=no`), and the exactly-one three-field smoke record (`smoke_command`, `smoke_exit_code`, `smoke_evidence_path`) (D3 row 2; SV-08…SV-11); mirror: `.specify/templates/verification-log-template.md`
- [X] T014 [US1] [blockedBy: T013] Upgrade GATE-4 in `templates/tasks-template.md` to require, for every `final`-path SC, a `pass` status **and** a present smoke record (or an explicit user waiver naming the SC), and add the A13 boundary note to its § Environment Prerequisites; add the matching GATE-4 obligation sentence to `templates/commands/tasks.md` so `/speckit.tasks` emits the upgraded gate (GW-09, GW-10); mirrors: `.specify/templates/tasks-template.md` and the four per-tool copies of `tasks.md` via `python3 scripts/python/regen-command-copies.py`
- [X] T015 [US1] [blockedBy: T006,T007,T011] Complete `scripts/python/closure-acceptance-check.py`: parse the SC definition lines and their `**Path**` markers plus the runtime-stack rows from `requirements.md`, the premises and inherited-blocker rows from `plan.md`, the `[ ]` / `[>]` / `[~]` counts from `tasks.md`, the status and ladder and smoke fields from `verification.md`, and the claimed status from the feature detail / registry; emit `accept|block`, the named reasons from the seven-value closed set (`zero-final-path-pass`, `final-path-not-pass: SC-NNN`, `blocked-without-measurement-ladder: SC-NNN`, `runtime-dependency-not-owned: RS-NNN`, `falsified-premise-undecided: EP-NNN`, `inherited-blocker-undisposed: <feature>:<row>`, `status-claims-implemented-but-blocked`), and the `final_path` counts computed once here; exit 0/1/2; the three external-source reasons are emitted from the rows present today and their full source extraction lands in 081b (§ Deferred Slices), so the closed set is never silently narrowed (C-07…C-09, C-13…C-17; V-11, V-12, V-14)
- [X] T016 [US1] [blockedBy: T007,T010,T015] Wire the implement call site: `skills/internal/implement-feature/SKILL.md` **Step 8 — Completion validation** (re-validation at the completion gate) and **Step 9 — Pre-Status-Flip Gate and Verification Log** (the status-landing step, where the checker runs before the flip) plus `shared/workflow/feature-integration.md` § Pre-Status-Flip Gate run the checker before the flip and land `Blocked` on `block` (never a zero-final-pass `Implemented`), with one pointer to the owner doc and no restated criteria; `templates/commands/implement.md` carries the invocation and the `Blocked` landing rule (GW-01, GW-04); mirrors: `.specify/skills/internal/implement-feature/SKILL.md`, `.specify/shared/workflow/feature-integration.md`, and the four per-tool copies of `implement.md` via `python3 scripts/python/regen-command-copies.py`
- [X] T017 [US1] [blockedBy: T002,T003,T015] Author the feature's single smoke test `tests/integration/test_acceptance_smoke.py` covering exactly three sub-checks — `specify init` on a `tmp_path` fixture asserting exit 0 and a generated `.specify/` tree; the closure checker on `tests/fixtures/acceptance-hardening/positive` (accept, exit 0) and `negative` (block, exit 1, `zero-final-path-pass`); `python3 scripts/python/regen-command-copies.py --check` exit 0 — with no network and no wall-clock in the assertions, writing the three sub-commands and exit codes to `.specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt` (D7; FR-005's three required subjects)
- [X] T018 [US1] [blockedBy: T012,T013,T014,T015,T016] Regenerate every mirror and per-tool copy after the source edits: `python3 scripts/python/regen-command-copies.py` then `--check` (exit 0), `python3 scripts/python/sync-mirrors.py` then `--check` (exit 0); in the same row register the new fixture directory — add `fixtures/` to the `tests/` row of `.specify/instructions.md` § Key Directories, so directory governance closes inside this slice instead of deferring to 081d; update any frozen count pinned by a guard test that the new files move, stating the reason inline, and never edit a `.specify/` copy by hand as the primary change (GW-11…GW-13; FR-024, FR-025)
- [~] T024 [US1] [blockedBy: T012] Add `Blocked` to the third status-vocabulary carrier that must admit it before the registry can hold it — `skills/internal/manage-features/SKILL.md`'s status vocabulary, one line plus the narrow `Implemented → Blocked` audit-correction exception with a pointer to the owner block (no criteria copy). Doing it here, ahead of T018's regeneration and ahead of T020's `Planned → Blocked` transition, is what keeps the registry from holding a value its own owner does not admit (FR-018); `templates/feature-index-template.md` is **not** touched here — it carries only a `Status` column header today, so its obligation is to **add** a closed vocabulary, and that stays with 081d (SV-06) <!-- deferred: 081d owns the third vocabulary owner; WC-14 freezes tests/contract/test_expression_compatibility.py, so its C-5 allowlist cannot land in 081a -->

**Checkpoint**: the checker, the state machine, the vocabulary, the gate wiring, the fixtures and the smoke exist; the negative fixture is refused at 1 of the 3 required call sites and the positive fixture is accepted.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Close the slice with its own recorded evidence — including the set-level zero-new-failure comparison — and record honestly that the feature is `Blocked`.

- [X] T019 [blockedBy: T017,T018] Run the slice's smoke command twice — `bash scripts/bash/run-tests.sh tests/integration/test_acceptance_smoke.py -q` — confirm both runs return the same exit status, and record command, exit code, evidence path and the two identical exit codes in `.specify/specs/081-acceptance-hardening/notes/quickstart-run.md`
- [X] T020 [blockedBy: T013,T019] Land the honest closing state: seed `.specify/specs/081-acceptance-hardening/verification.md` from the upgraded `templates/verification-log-template.md` — one status row for each of SC-001…SC-009, all five `SC-NNN_`-prefixed ladder fields on every `blocked` / `deferred` / `partial` row, and the three smoke fields from T019; SC-001 and SC-002 MUST be recorded `blocked` with the reason "1 of 3 call sites wired; 081c/081d own the review and driver sites". Then perform the `Planned → Blocked` transition in both status carriers — `.specify/memory/features.md` row 081 column 5 and `.specify/memory/features/081.md` `**Status**` MUST both read `Blocked` — because a zero-`final`-path-pass slice is `Blocked` and never `Implemented` (FR-003; GATE-5 asserts the registry value)
- [X] T022 [blockedBy: T018] Run the slice-close set-level comparison (GATE-7, DoD-6): re-read `pytest --version` and `git --version` and compare them against `test-evidence/plan-runner-pins.txt` (a mismatch invalidates the comparison as an input error — never read it as new failures); then run `bash scripts/bash/run-tests.sh --names-out .specify/.tmp/081a-head-failed.txt -q` over the **full** suite on the post-change tree and diff the id sets against `baseline-failed.txt` — `head − baseline` MUST be empty and `baseline − head` MUST be enumerated row by row as fixed items; record both diffs, the two pin readings and the exit status in `.specify/specs/081-acceptance-hardening/notes/red-first-evidence.md`. The temporary id set lives under `.specify/.tmp/` (FR-025) and is not committed; the baseline is **not** re-collected (FR-023)
- [X] T023 [blockedBy: T018] Own the contract-clause coverage lane that this slice's tasks stage left as `baseline-missing`: freeze the exemption baseline with `python3 scripts/python/account-clause-coverage.py .specify/specs/081-acceptance-hardening --freeze > .specify/specs/081-acceptance-hardening/coverage-baseline.txt` (the accountant excludes this spec's own contracts from the frozen face, so the name set is repo-wide pre-existing debt), then run the read-only accounting `python3 scripts/python/account-clause-coverage.py --spec .specify/specs/081-acceptance-hardening` and record its verdict in `notes/pre-change-measurements.md`. Measured before the freeze (2026-11-03): `status=baseline-missing`, `claimed clauses 0`, `[fr-uncovered] fail (25) — 0 of 25 FRs cited from citation groups`. The FR lane has no baseline by design, so freezing does not make it green: this row records the verdict and keeps the absence explained; the citation-group form for this spec's five contracts is a separate obligation to be decided before that lane can go green, and MUST NOT be papered over by an empty or hand-edited baseline

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: starts immediately; its four rows are mutually independent
- **Phase 2 (Foundational)**: T005 and T006 block every US1 row (T005 owns the schemas the tests read; T006 owns the CLI the tests invoke)
- **Phase 3 (US1)**: after Phase 2. Tests T007–T010 first; then T011 → T012 → T013 → T014 → T015 → T016 → T017 → T018
- **Phase 4 (Polish)**: after Phase 3; T019 needs the smoke test and the regenerated tree, T020 needs the upgraded vocabulary template and T019's measured exit codes, T022 and T023 need the regenerated tree (T018) so the sets they record describe the tree that will actually close

### User Story Dependencies

- **US1 (P1)**: no dependency on another story — this slice is US1 plus the shared core

### Within This Slice

- Tests MUST fail before the implementation row that answers them closes
- Owner doc → state machine / vocabulary templates → gate wiring → regeneration
- The checker's skeleton (T006) precedes its contract test (T007); the test precedes its completion (T015)

### Parallel Opportunities

- Phase 1: T001–T004 and T021 all run in parallel (five disjoint path sets)
- Phase 3 tests: T007–T010 all run in parallel (four disjoint test modules), once the fixtures their inputs come from (T003, T004, T021) exist
- T011 and T012 are independent of each other once their tests exist; T013 depends on T009 only

---

## Parallel Example: User Story 1

```bash
# Launch the four red-first contract tests together:
Task: "checker contract test in tests/contract/test_closure_acceptance_check.py"
Task: "path-marker cases in tests/contract/test_requirements_checker.py"
Task: "state machine + vocabulary test in tests/contract/test_acceptance_state_machine.py"
Task: "implement call-site test in tests/contract/test_gate_wiring_081.py"
```

---

## Implementation Strategy

### MVP First

**MVP scope**: US1 alone — it is the whole of slice 081a. It is independently testable through the checker on the positive/negative fixtures plus the state-machine contract test, and it is the threshold without which no later slice has a verdict to share.

1. Complete Phase 1 (Setup) and Phase 2 (Foundational)
2. Complete US1 in the order given: tests → `validate-requirements` → state machine → vocabulary → GATE-4 → checker → implement wiring → smoke → regeneration
3. **STOP and VALIDATE**: run the checkpoint's two checker invocations and the four contract modules
4. Land the status as `Blocked` (T020) and do not advance it past that — see `## Slice Boundary`

### Incremental Delivery

`081a` (this slice) → `081b` (ownership tables and the four deterministic findings) → `081c` (review composition + ARC + the review call site) → `081d` (vocabulary owners, audit mode, driver line state and closure/merge site, mirrors, docs, smoke evidence). Each later slice depends on 081a's owner doc sections and on 081a's checker; the FR/SC mapping is in `## Slice Boundary`.

---

## Slice Boundary

**Slice**: `081a` — plan.md § D10 "US1 + the shared core". Boundaries are cut at plan entry; **no requirement is dropped**, each FR and SC below is assigned to exactly one slice.

### FR / SC coverage in this slice

| FR / SC | 081a status | What 081a delivers | Remainder and owner |
|---|---|---|---|
| FR-001 (`Path` marker) | **covered** | marker form + last-token rule in the owner doc; sixth `path-marker` check label in `scripts/python/validate-requirements.py`; `final ≥ 1` for `execution`, exempt for `expression` | — |
| FR-002 (four conjunctive conditions) | **covered** | owner block rewrite + contract test | — |
| FR-003 (`Blocked` transitions) | **covered** | four transitions including the illegal one and the audit-correction exception | — |
| FR-004 (verification vocabulary + ladder) | **covered** | six-value set, five `SC-NNN_`-prefixed ladder fields, illegal-row rule, `blocked-without-measurement-ladder: SC-NNN` reason | — |
| FR-005 (one smoke command, three subjects) | **partial** | the smoke **test** exists and covers the three required subjects; the command is recorded in `tasks.md` | the recorded `smoke_command` / `smoke_exit_code` / `smoke_evidence_path` triple is an implement-stage output (T019, T020) |
| FR-006 (checker: verdict, closed set, exit codes, counts) | **partial** | script, seven-value closed set, three exit codes, single-computation `final_path` counts | full source extraction for `runtime-dependency-not-owned: RS-NNN`, `falsified-premise-undecided: EP-NNN`, `inherited-blocker-undisposed: <feature>:<row>` → **081b** (the codes exist and are emitted from today's rows; the extraction checks land there) |
| FR-007 (pytest tests + positive/negative fixtures) | **covered for 081a's subject set** | `test_closure_acceptance_check.py` + the `positive` / `negative` / `ladder-mutation` / `smoke-mutation` / `mixed-path` / `expr-supporting-only` / `execution-without-final` fixtures, **all seven asserted by T007** — in particular `smoke-mutation` (claimed `Implemented`, smoke record gone → `block` + `status-claims-implemented-but-blocked`, exit 1) and `execution-without-final` (`final_path.total = 0` → `block` + `zero-final-path-pass`, exit 1), so neither fixture is merely "delivered" | 081b adds the premise / runtime-gap fixtures for its three reasons |
| FR-008 (three call sites) | **partial — 1 of 3** | the **implement** call site is wired and asserted | `/speckit.review` site → **081c**; `sdd-loop-driver` site → **081d**, where the judgement runs at the **feature line's closure** (081a–081d are one line) — per-slice merges are judged by the review gate, not by that step (FR-017 / GW-03) |
| FR-009…FR-012 (ownership / premises / inherited blockers / four findings) | **deferred** | — | **081b** (its row set carries the `in-scope` three obligations and the `inherited` carrier check, both absorbed by the existing four finding classes — no fifth class, no eighth reason) |
| FR-013…FR-016 (artifact review, implementation review, ARC, fourth condition at the review gate) | **deferred** | — | **081c** (the fourth condition's *owner text* is written in 081a as part of FR-002/FR-003's owner block; the review-side enforcement is 081c) |
| FR-017 (driver line state + closure/merge) | **deferred** | — | **081d** |
| FR-018 (three vocabulary owners + never-regress narrow exception) | **partial — two of three owners** | `templates/feature-details-template.md` carries `Blocked` and the narrow exception; `skills/internal/manage-features/SKILL.md` gains `Blocked` in **T024**, ahead of the `Planned → Blocked` transition, so the registry never holds a value its own owner does not admit | `templates/feature-index-template.md` → **081d** (measured: 21 lines, `Status` column header only, no value-domain list — the obligation is to **add** a closed vocabulary, not to insert one value, SV-06) |
| FR-019 (four `blocked` literals reconciled once) | **deferred** | — | **081d** |
| FR-020 (`--audit-existing`) | **deferred** (CLI flag present, mode unimplemented) | the flag is on the stable surface (T006) | **081d** |
| FR-021 (command templates + regeneration) | **partial** | `templates/commands/implement.md` and `templates/commands/tasks.md` wired and regenerated | `templates/commands/review.md` → **081c**; the final two `--check` sweeps → **081d** |
| FR-022 (single schema owner + owner pointers + CHANGELOG) | **partial** | the owner document exists with its 081a sections and extension points | owner pointers for the 081b/c/d sections, CHANGELOG, docs → **081d** |
| FR-023 (tests + baseline compare) | **partial — set level assessed here** | the four contract modules + the smoke exist; baseline is the plan-stage capture; **T022 runs the full suite at this slice's close with `--names-out` and performs the id-level set difference** (GATE-7), so DoD-6 is assessable now rather than later | the feature-level claim over the final tree (081c/081d edits) re-runs the same comparison → **081d** |
| FR-024 (source not mirror) | **covered for 081a's edits** | every edit lands in `templates/` / `shared/` / `skills/` / `scripts/` / `src/` / `tests/`, then T018 regenerates | later slices repeat the rule for their own edits |
| FR-025 (registration + deterministic-only gates) | **covered** | every new gate in this slice is a deterministic script verdict; new temp artifacts go to `.specify/.tmp/`; directory registration of `tests/fixtures/` in `.specify/instructions.md` § Key Directories is landed by **T018** in this slice (not deferred) | — |
| SC-001 (3/3 call sites refuse the 026 shape) | **partial — 1/3** | the implement site refuses, with a named reason from the closed set | review site (081c) and driver closure/merge site (081d) — **SC-001 cannot pass until all three are wired** |
| SC-002 (positive path not killed; smoke is a hard condition) | **partial** | positive fixture `accept`; the `Planned → Implemented` half of the walk; `smoke-mutation` → `Blocked` | the `Implemented → Ready for Review` leg needs the fourth-condition gate at the review site (081c) |
| SC-003 (vocabulary + state machine alignment) | **partial — two of three owners** | the feature-details owner and its four transition rows; `manage-features`' vocabulary by T024 | `templates/feature-index-template.md` → **081d** |
| SC-004 (vocabulary + measurement ladder judgeable) | **partial** | six-value set, five `SC-NNN_`-prefixed fields, illegal-row rule, `blocked-without-measurement-ladder: SC-NNN` reason and its `ladder-mutation` fixture | no remainder |
| SC-005 (ownership + premises are first-class artifacts) | **deferred** | — | **081b** — including the two measures this slice cannot produce: the `in-scope` three obligations and the `inherited` carrier-existence check (its single test carrier is `tests/contract/test_acceptance_premises.py`) |
| SC-006 (review four segments + ARC) | **deferred** | — | **081c** |
| SC-007 (audit read-only) | **deferred** | — | **081d** |
| SC-008 (smoke record present and reproducible) | **partial** | exactly one smoke command exists and its two-run determinism is a slice gate (GATE-4) | the recorded triple in `verification.md` closes with T020; final claim in **081d** |
| SC-009 (framework hygiene + the containment claim) | **partial** | both `--check` runs exit 0 on the 081a tree | `CHANGELOG` entry and the schema-uniqueness guard test `tests/contract/test_acceptance_schema_ownership.py` (SC-009 ④, named in plan.md § Source Code) → **081d** |

### Status consequence (load-bearing — do not soften)

**After 081a the feature is `Blocked`, not `Implemented`.** SC-001 requires the negative fixture to be rejected at **three** call sites (implement, review, driver closure/merge); 081a wires **one** (implement) and therefore satisfies 1/3. SC-001 and SC-002 are the feature's two `final`-path criteria, and `Planned → Implemented` requires **every** `final`-path SC to be `pass`. `Blocked → Ready for Review` is illegal by design (FR-003). Consequently:

- `Implemented` requires the 081c (review) and 081d (driver closure/merge) call sites **and** final-path SC-001 / SC-002 all pass; no artifact of this slice may claim otherwise.
- `verification.md` records SC-001 and SC-002 as `blocked` with the 1-of-3 reason (T020), so the honest state is visible at the gate rather than inferred from this paragraph.
- GATE-5 makes the claim machine-checkable: the registry row for Feature 081 must read **exactly `Blocked`** when this slice closes (T020 lands that value; `Planned` no longer passes the gate).

## Deferred Slices

Not tasks. Listed so nothing is silently dropped and so `/speckit.tasks` for those slices starts from the plan's D10 scope.

- **081b — US2, ownership and premises** (plan § D10: runtime stack table, Execution Premises + Inherited Blockers, four `pre-analyze-check.py` findings, `expression-gates.md` rows, A13 boundary). FR-009, FR-010, FR-011, FR-012; SC-005; the checker's full source extraction for `runtime-dependency-not-owned: RS-NNN`, `falsified-premise-undecided: EP-NNN`, `inherited-blocker-undisposed: <feature>:<row>`; the `premise-mutation` / `runtime-gap-mutation` fixtures. Its row set MUST name three carriers that this slice does not create: **`tests/contract/test_acceptance_premises.py`** (the single test module for the four findings plus the `in-scope` three obligations and the `inherited` carrier check), **`templates/plan-template.md`** (the two table skeletons, fixed column sets only, no value domains and no invalid-row rules — AS-15), and the owner doc's `§ Execution Premises` / `§ Inherited Blockers` sections (whose extension points 081a's T005 leaves in place). One of its rows MUST land the `inherited` carrier check, because FR-011 makes that an obligation no later slice can absorb. Depends on 081a's owner-doc sections.
- **081c — US3, review composition and ARC** (plan § D10: `review-feature-quality` skill, review-template slots `### 2.2`–`### 2.4`, `templates/commands/review.md` composition rewrite, ARC, census 3→4 plus its guard, the checker at the **review** call site). FR-013, FR-014, FR-015, FR-016; SC-002's second leg; SC-006; **`tests/contract/test_acceptance_review_composition.py`** (the new module) and the deliberate updates of **`tests/contract/test_review_code_composition.py`** (the pinned "exactly two segments" sentence), **`tests/contract/test_review_feedback_boundary.py`** (C-58's three-unit census → four) and **`tests/contract/test_status_gate_owner.py`** (C-46's conjunctive-condition count, `all required` phrasing preserved), plus **`templates/commands/checklist.md`** (owner pointer only — no criteria copy). It also lands FR-013's **expected-artifact denominator** (the artifact segment's coverage base). Depends on 081a's `final_path` counts.
- **081d — US4 and all remaining wiring** (plan § D10: the last vocabulary owner, `--audit-existing`, driver line state `blocked` and its A6 items 1–8, the closure/merge call site, mirrors, docs / CHANGELOG, smoke evidence, the feature-level baseline re-run). FR-017, FR-018's remaining owner (`templates/feature-index-template.md`), FR-019, FR-020, FR-022's pointers, FR-023's feature-level id-level differencing, FR-025 for the paths this slice and 081c add; SC-001's third site, SC-003, SC-007, SC-008's final claim, SC-009. Its row set MUST name **`tests/contract/test_acceptance_schema_ownership.py`** — the SC-009 ④ uniqueness guard (owner-literal zero-hit assertion plus the three declaration-site exemptions of SC-009 ④: `data-model.md` and `requirements.md` carry 0 transition rows, projection domains ⊆ owner domains) — **`tests/contract/test_line_state_blocked.py`** (the single carrier pinning A6's eight dispositions; `data-model.md` § E-9 and `plan.md` § D6 are pointers, so this module is where the obligations become measurable), and the final re-run of **`tests/contract/test_status_gate_owner.py`** and **`templates/commands/checklist.md`** in the sweeping `--check` pass. Also carried here: `templates/feature-index-template.md` is measured at 21 lines carrying only the `Status` column **header** with no value-domain list, so FR-018's obligation for that file is to **add** a closed status vocabulary containing `Blocked`, not to insert one value into a list that does not exist (SV-06). The closure judgement this slice wires runs at the **feature line's closure**, not at each slice merge (FR-017 / GW-03). Depends on 081a's checker and 081c's composition text.

## Notes

- [P] rows write disjoint path sets; any row that writes a file another row also writes carries no `[P]` and an explicit `[blockedBy:]`
- Two Hats: every edit lands in `templates/`, `shared/`, `skills/`, `scripts/`, `src/` or `tests/`; `.specify/` copies are regenerated by T018, never hand-edited. Exact pairs: plan.md § Mirror Obligations
- The pre-change side of every "diff against pre-change output" premise is already frozen at plan stage — `test-evidence/plan-baseline-run.txt` (39 failed / 6970 passed / 7 skipped), `test-evidence/plan-runner-pins.txt` (pytest 9.2.0 / CPython 3.14.6 / git 2.54.0), `test-evidence/plan-gates.txt`. Do not re-run the full suite to re-derive them; T022 runs it once at slice close for the **head** side of the comparison — a different artifact from the baseline, and the baseline is never re-collected
- The feature's single smoke command, recorded verbatim: `bash scripts/bash/run-tests.sh tests/integration/test_acceptance_smoke.py -q`
- Deferral discipline: prefer `[~]` with a recorded reason over leaving a row `[ ]`
