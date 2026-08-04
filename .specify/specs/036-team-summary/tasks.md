# Tasks: Team Summary 信息管理机制

**Requirement ID**: 036
**Requirement Key**: 036-team-summary
**Related Feature**: 027 Team Management
**Input**: Design documents from `.specify/specs/036-team-summary/`
**Prerequisites**: plan.md ✓, requirements.md ✓, research.md ✓, data-model.md ✓, contracts/ ✓ (4), quickstart.md ✓, feature-ref.md ✓

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" mandates tests BEFORE behavior; Principle VII's *template-only features* gate applies to the prompt/template artifacts, so those get **structural contract tests** — heading/content/mirror-parity assertions — while the one executable deliverable `build-summary-input.py` gets real unit + integration tests. Both layers are emitted.)

**Organization**: Tasks are grouped by user story (US1…US5) to enable independent implementation and testing.

## Definition of Done (DoD)

- DoD-1: Every FR-001…FR-036 has at least one task that implements it and one check that proves it
- DoD-2: All automated tests pass with zero NEW failures versus the T001 baseline
- DoD-3: `summarize-project` is byte-identical to its pre-change state (FR-024 / SC-003)
- DoD-4: Every Mirror Obligations row in plan.md verified — `sync-mirrors.py --check` exits 0
- DoD-5: A real summary produced for at least one team per collaboration pattern plus one two-team shared-goal aggregation, with zero manual form editing
- DoD-6: Every SC-001…SC-015 recorded with a status in `verification.md`
- DoD-7: The two research.md § O carry-forwards (always-emit `coverage`; `DISPATCH_LOG_DIR` path discrepancy) are resolved or explicitly deferred with reasons

**DoD Status**: pending

## Completion Gate

- GATE-1: Full suite has zero NEW failures vs the T001 baseline — check: `python3 -m pytest -q > /tmp/036-current.txt` then `comm -13 /tmp/036-baseline.txt /tmp/036-current.txt`
- GATE-2: Mirror parity holds for all 6 obligation rows — check: `python3 scripts/python/sync-mirrors.py --check` exits 0
- GATE-3: No `[ ]` or `[>]` task rows remain — check: `grep -cE '^- \[[ >]\]' tasks.md` returns 0
- GATE-4: `verification.md` lists every SC-NNN with a status — check: grep SC ids against requirements.md
- GATE-5: Invoked skill untouched — check: `git diff --exit-code -- skills/summarize-project .specify/skills/summarize-project`
- GATE-7: Pre-existing `.specify/project/` artifacts untouched (FR-036) — check: `git diff --exit-code -- .specify/project/project.md .specify/project/wbs.* .specify/project/gantt.* .specify/project/milestones.*`
- GATE-8: Exactly one current summary per goal directory — check: `find .specify/project/goal -maxdepth 2 -name summary.md | wc -l` equals the number of goal directories
- GATE-6: Real end-to-end summary exists and its form validates — check: `validate-project-input.py --input <delivery_dir>/data/project-input.yaml --json` exits 0 with `missing_required: []`

## Format: `[ID] [P?] [Story] Description`

Sigils, `[P]`, `[Story]`, and `[blockedBy: …]` semantics follow `.specify/templates/tasks-template.md` § Format / § Task State Sigil. A run is complete when zero `[ ]` / `[>]` rows remain; `[~]` rows are allowed and surface as deferred.

## Path Conventions

This is a **code-generator / framework** repo (see plan.md § Structure Decision). Canonical sources live in `skills/`, `templates/`, and `scripts/`; `.specify/**` copies are **mirrors** maintained only by `scripts/python/sync-mirrors.py --write`. Never hand-edit a mirror or a per-tool command copy.

## Environment Prerequisites (probed 2026-08-04)

| Prerequisite | Probe result | Affects |
|--------------|--------------|---------|
| `python3` + `pytest` | ✓ pytest 8.4.2, markers `contract` / `integration` present | all test tasks |
| `summarize-project` script chain | ✓ `validate → load → check → engine` all exit 0 against a real team | US1, US3, US5 |
| `sync-mirrors.py` | ✓ `--check` exits 0 (no pre-existing drift) | all mirror tasks |
| PlantUML rendering | ✓ real render verified (SVG 1987×1687 + PNG produced) via server `http://xuanji-plantuml.aliyun-inc.com:9696/plantuml`; `java` 21 present but **no local jar**, so there is no offline fallback | T052 render-verify only |

**Render invocation caveat (measured)**: `render-plantuml.sh <input.puml> <output_dir> <prefix>` — omitting `output_dir` writes `diagram.{puml,svg,png}` into the **current working directory**. T052 MUST pass an explicit output directory and MUST NOT run from the repo root.

---

## Phase 1: Setup

- [X] T001 Record the full-suite baseline before any edit: run `python3 -m pytest -q` and save the failing-test list to `/tmp/036-baseline.txt`, then copy it into `.specify/specs/036-team-summary/verification.md` under a `baseline=` line (pre-existing unrelated failures exist long-term; GATE-1 compares against this, not against zero)
- [X] T002 [P] Create the fixture workspace `tests/fixtures/teams/` with a README.md stating that these are synthetic teams used because the repo has no `serial` or `parallel` team (measured: 4 real teams = 2 continuous + 2 iteration)
- [X] T003 [P] Record the probed environment prerequisites table (above) into `.specify/specs/036-team-summary/verification.md` so `/speckit.implement` does not re-probe

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Item identity, the ledger, and the corrected directory assertions. Every user story reads the ledger, so nothing can proceed until its schema and identifier grammar are fixed and tested.

**⚠️ CRITICAL**: No user story work begins until this phase completes.

### Tests (MANDATORY, before implementation)

- [X] T004 [P] Write `tests/contract/test_team_item_ledger.py` asserting the ledger line schema and rules LC-1…LC-10 from `contracts/items-ledger.contract.md`: required keys present, `state` in the five-value domain, `identity` in {explicit,inferred}, and `TI-[0-9]{4}` / `TIX-[0-9a-f]{8}` grammar per `identity` [blockedBy: T001]
- [X] T005 [P] Extend `tests/contract/test_team_item_ledger.py` with an LC-5 case that feeds an identifier containing a space and an identifier containing CJK characters through `skills/summarize-project/scripts/project-db.py --load` and asserts **exit code 3** — pinning the upstream DDL grammar rather than restating it (measured behavior, research.md E-2) [blockedBy: T004]
- [X] T006 [P] Write `tests/contract/test_summary_writeset.py` asserting the WS-5/WS-6/WS-7 provenance admissibility rules: `.specify/teams/.work/**`, `.specify/agents/execution/logs/**`, and any absolute path outside the repo are rejected; `.specify/agents/execution/{configs,scripts}/**` are accepted [blockedBy: T001]

### Implementation

- [X] T007 Create `skills/create-team/references/summary-mapping.md` with the FR-001 concept-mapping single source of truth: the seven-entity source table and the four-pattern phase/work-item matrix from `data-model.md` § 2 [blockedBy: T004]
- [X] T008 Add an `## Item Ledger` section to `skills/create-team/references/summary-mapping.md` carrying the line schema, invariants IL-1…IL-5, and the identifier grammar table from `data-model.md` § 1.1 and § 3 (the ledger lives here rather than in a separate reference file, to avoid file proliferation per Constitution Principle IX) [blockedBy: T007]
- [X] T009 Correct the output-discipline assertion in `skills/create-team/SKILL.md` — the "team directory holds **only** `team.md` and `runs/`" claim in the Run Workspace Rules bullet and in the Hard Constraints bullet — to enumerate `constraints.md` / `STATE.md` / `run-log.jsonl` (already true for continuous teams today) plus the new `items.jsonl` (TG-15；总结产物不再落团队目录,改落 goal 交付目录) [blockedBy: T004]
- [X] T010 Correct the same assertion in the **Output discipline** line of `templates/commands/team.md` (TG-15) [blockedBy: T004]
- [X] T011 Add `config.summary` (`enabled` / `every` / `delivery_dir` / `interactive`) to the persisted `team.md` schema section of `skills/create-team/SKILL.md`, documenting the per-pattern `every` defaults and the opt-out semantics, and stating explicitly that the key nests under `config` to avoid colliding with the top-level one-line `summary:` field already used by preset files ([[STR-002]], TG-11) [blockedBy: T004]
- [X] T102 [P] Write `tests/contract/test_goal_identity.py` asserting invariants GI-1…GI-4 from `data-model.md` § 1.3: explicit `goal_slug` wins, absent `goal_slug` falls back to the team slug marked `inferred`, goal-prose edits never change the resolved value, and the resolved value satisfies both the DDL identifier grammar and path-segment safety (FR-031, FR-034, SC-013) [blockedBy: T004]
- [X] T103 Add the `goal_slug` field ([[STR-006]]) to the persisted `team.md` frontmatter schema in `skills/create-team/SKILL.md`, documenting that it is optional with the team-slug inference fallback, that it is distinct from the existing `slug` (team slug), and that goal-prose edits must not change it (FR-031, FR-019) [blockedBy: T102]
- [X] T012 Run `python3 scripts/python/sync-mirrors.py --write`, then verify with `--check` (exit 0) [blockedBy: T007,T008,T009,T010,T011,T103]
- [X] T013 Run `python3 -m pytest -m contract -q tests/contract/test_team_item_ledger.py tests/contract/test_summary_writeset.py tests/contract/test_goal_identity.py` and confirm the Phase 2 contract tests now pass [blockedBy: T012]

**Checkpoint**: Item identity and the corrected directory contract are in place; user stories can begin.

---

## Phase 3: User Story 1 — 概念映射与表单自动生成 (Priority: P1) 🎯 MVP

**Goal**: Any team's existing tracked artifacts become a `summarize-project`-valid project input form with zero manual form entry.

**Independent Test**: For one team per collaboration pattern, generate a form from tracked artifacts alone; input validation exits 0 with `missing_required: []`, the database load and integrity check both exit 0, and a summary containing the five presentation sections plus the breakdown diagram is produced.

### Tests for User Story 1 (MANDATORY) ⚠️

- [ ] T014 [P] [US1] Write `tests/contract/test_summary_form_generator.py` asserting the FG-1…FG-18 interface contract from `contracts/team-project-form.contract.md`: the CLI accepts `--goal`/`--team`/`--out`/`--baseline`/`--json`, exits 3 when the whole goal has no material, exits 2 on an unknown slug or unresolvable goal [blockedBy: T013]
- [ ] T015 [P] [US1] Add an FG-1 determinism case to `tests/contract/test_summary_form_generator.py`: two runs over identical inputs produce byte-identical forms [blockedBy: T014]
- [ ] T016 [P] [US1] Add an FG-2 input-surface case asserting the generator never opens a path under `.specify/teams/.work/`, `.specify/agents/execution/logs/`, or outside the repository [blockedBy: T014]
- [ ] T017 [P] [US1] Add an FG-8 case asserting the emitted form **always** contains a `coverage` block with all five keys — this is the research.md § O carry-forward that has no FR: an absent `coverage` makes every work-breakdown report fail the upstream CG-COVERAGE gate (measured, research.md E-5) [blockedBy: T014]
- [ ] T018 [P] [US1] Add an FG-6 case to `tests/contract/test_summary_form_generator.py` asserting `project.baseline_date` is always populated from the ledger/run timestamp, never left for the invoked skill to infer (FR-005) [blockedBy: T014]
- [ ] T019 [US1] Write `tests/integration/test_summary_four_patterns.py` driving the full chain per pattern — generator (`--team <slug>`, resolving to its goal) → `validate-project-input.py` → `project-db.py --load` → `--check` — and asserting all four exit 0 with `missing_required: []` (SC-001, SC-002) [blockedBy: T014]

### Implementation for User Story 1

- [ ] T020 [US1] Create `skills/create-team/scripts/build-summary-input.py` with the `--goal` / `--team` selector pair, exit-code semantics (0/2/3), and `--json` generation report (resolved goal identity + explicit-or-inferred + contributing team list) per `contracts/team-project-form.contract.md` § Interface [blockedBy: T014]
- [ ] T021 [US1] Implement the **goal-level** `project` entity mapping in `build-summary-input.py`: `project_name` ← resolved goal identity, `project_desc` ← that goal's prose (differences across teams recorded in metadata per GI-4), `baseline_date` ← latest ledger event `ts` across aggregated teams (or `--baseline`), `repos` always empty (FG-5, FR-005) [blockedBy: T020]
- [ ] T022 [US1] Implement the `people` mapping as a **union across aggregated teams** (same agent slug in two teams merges to one person): one person per roster row; `owner_id` ← roster agent slug; `owner_name` ← frontmatter `name` of the referenced definition resolved as `.specify/agents/instances/<slug>.agent.md` then `.specify/agents/templates/<slug>.agent.md` (instance wins); unresolvable → `未记录`, never fabricated (FR-004, plan.md pre-seeded constraint 1) [blockedBy: T020]
- [ ] T023 [US1] Implement the `phases` mapping in `skills/create-team/scripts/build-summary-input.py` with the four per-pattern units — continuous→cycle, iteration→generation, serial→stage, parallel→dispatch batch — emitting **team-namespaced** `<team-slug>.PH-<nnnn>` identifiers and `<team-slug> · <unit>` names, so teams on different patterns under one goal are never merged into a single ordered sequence (FR-002, FG-16) [blockedBy: T020]
- [ ] T024 [US1] Implement the `work_items` mapping in `skills/create-team/scripts/build-summary-input.py` by folding **every aggregated team's** `items.jsonl` per invariant IL-2 (last event per `item_id` wins), prefixing ids as `<team-slug>.TI-nnnn` for global uniqueness, and carrying `source` from each event's `provenance` (FR-002, FR-010, FG-15) [blockedBy: T020,T008]
- [ ] T025 [US1] Implement the `milestones` mapping in `skills/create-team/scripts/build-summary-input.py`: each verifiable success criterion in the **goal's** `## Goal` becomes one `MS-<nnnn>` milestone anchored via `anchor_item_id`, emitted **once per goal** rather than once per team (FR-003, FR-032) — this is what makes the R-tier group constraint satisfiable on a goal's very first summary [blockedBy: T020]
- [ ] T026 [US1] Implement the `features` and `sources` mappings in `skills/create-team/scripts/build-summary-input.py`, with `sources` emitting one declaration per information group referencing a tracked team artifact path (FR-007) [blockedBy: T020]
- [ ] T027 [US1] Implement the absence-degradation branch in `skills/create-team/scripts/build-summary-input.py` so all seven entities are either populated or emitted empty **with** a recorded absence declaration — no entity may be silently left blank (FR-007) [blockedBy: T021,T022,T023,T024,T025,T026]
- [ ] T028 [US1] Implement the always-on `coverage` block (`candidate_total` / `excluded` / `granularity_truncated` / `unattributed` / `source_label`) per `data-model.md` § 2.1 (FG-8, resolves a research.md § O carry-forward) [blockedBy: T024]
- [ ] T029 [US1] Implement the summary-invocation wrapper documented in `skills/create-team/references/summary-mapping.md`: call the invoked skill in **non-interactive** mode (its four per-layer confirmation gates must be explicitly skipped and that fact noted in the report metadata), using `--load` rather than `--update` per research.md D-1 [blockedBy: T027,T028]
- [ ] T030 [US1] Build fixture teams `tests/fixtures/teams/serial-fixture/` and `tests/fixtures/teams/parallel-fixture/` (each with `team.md` + `items.jsonl` + one `runs/` report) so SC-001's four-pattern coverage is achievable [blockedBy: T002,T008]
- [ ] T031 [US1] Run `python3 scripts/python/sync-mirrors.py --write` then `--check`, confirming `build-summary-input.py` and `summary-mapping.md` landed in `.specify/skills/create-team/` [blockedBy: T020,T029]
- [ ] T032 [US1] Execute the US1 independent test for real: generate summaries for `cws-workspace-cluster` (continuous), `summarize-project-optimizer` (iteration), and both fixtures; record exit codes and `missing_required` per team in `verification.md` (SC-001, SC-002) [blockedBy: T019,T029,T030,T031]

**Checkpoint**: US1 is independently functional — a summary can be produced on demand for any team, zero manual form entry.

---

## Phase 4: User Story 2 — 阶段性触发 (Priority: P1)

**Goal**: The summary refreshes automatically at each pattern's phase boundary, gated by budget then cadence, with the outcome always declared in the run report.

**Independent Test**: Run a team twice — the summary refreshes at the declared boundary; then raise budget usage to the report-only tier and run again — the summary is skipped, the cycle still completes normally, and the run report carries an explicit skip record.

### Tests for User Story 2 (MANDATORY) ⚠️

- [ ] T033 [P] [US2] Write `tests/contract/test_summary_trigger.py` asserting the trigger-point table and the **budget → cadence → material** gate order from `contracts/summary-trigger.contract.md`, including TG-1 (budget outranks cadence even at a cadence point) [blockedBy: T013]
- [ ] T034 [P] [US2] Add a TG-5…TG-8 status-line case to `tests/contract/test_summary_trigger.py` asserting exactly one of the four [[STR-005]] states appears per run report, that `produced` names the delivery directory, and that `declined(no-material)` never co-occurs with a chart artifact [blockedBy: T033]
- [ ] T035 [P] [US2] Add a TG-9/TG-10 case to `tests/contract/test_summary_trigger.py` asserting a team with no `config.summary` is treated as enabled, and that the `continuous` default cadence is **not** every cycle [blockedBy: T033]
- [ ] T036 [P] [US2] Add a TG-13/TG-14 structural case asserting the run-mode confirmation gate in `templates/commands/team.md` discloses the summary decision **before** execution, and that all five per-tool copies carry the same disclosure [blockedBy: T033]

### Implementation for User Story 2

- [ ] T037 [US2] Add phase **9. SUMMARIZE** to the continuous per-cycle loop in `skills/create-team/SKILL.md` § Per-Cycle Loop, placed after the existing phase 8 REPORT so the run report is available as a provenance source (FR-012) [blockedBy: T033]
- [ ] T038 [US2] Add the summary trigger point to the iteration pattern section of `skills/create-team/SKILL.md` — after each generation's DECIDE phase (FR-012) [blockedBy: T033]
- [ ] T039 [US2] Add the summary trigger point to the serial pattern section of `skills/create-team/SKILL.md` — after each stage handoff verification passes (FR-012) [blockedBy: T033]
- [ ] T040 [US2] Add the summary trigger point to the parallel pattern section of `skills/create-team/SKILL.md` — after cross-verification and Result Aggregation complete (FR-012) [blockedBy: T033]
- [ ] T041 [US2] Add the terminal-summary rule (goal met / converged / halt / manual stop) to `skills/create-team/SKILL.md` § Stop / Halt, excluding the case where budget has already been exceeded (FR-012) [blockedBy: T037]
- [ ] T042 [US2] Implement budget-ladder gating in the SUMMARIZE step of `skills/create-team/SKILL.md`: at report-only tier or kill-switch, skip and record `[[STR-003]]`; the summary must be the first step dropped and must not be retried in the same run (FR-014, TG-2, TG-3) [blockedBy: T037]
- [ ] T043 [US2] Add the status-line requirement to the Report contract in `skills/create-team/SKILL.md` so every run report carries exactly one [[STR-005]] summary line (FR-015) [blockedBy: T037]
- [ ] T044 [US2] Add the first-run activation disclosure to the Report contract in `skills/create-team/SKILL.md`: the first summary ever produced for a team declares that the mechanism has activated and names the cadence now in force, so the opt-out default is not a silent behavior change for the 4 pre-existing teams (FR-028, TG-12) [blockedBy: T043]
- [ ] T045 [US2] Add the summary-cost disclosure to run-mode step 5 in `templates/commands/team.md`, stating whether this run will produce a summary and, when it will not, which gate suppresses it (FR-016, TG-13) [blockedBy: T033]
- [ ] T046 [US2] Add boundary coalescing to the SUMMARIZE step of `skills/create-team/SKILL.md` so two boundaries reached in rapid succession produce one refresh, not one per boundary (TG-4) [blockedBy: T042]
- [ ] T047 [US2] Declare per-pattern `config.summary` defaults in the three presets `skills/create-team/templates/teams/{artifact-optimizer,process-monitor,workspace-cluster}.md` (FR-013) [blockedBy: T011]
- [ ] T048 [US2] Run `python3 scripts/python/sync-mirrors.py --write` then `--check`, confirming the 5 per-tool copies of `speckit.team` carry the disclosure edit and the 3 presets mirrored [blockedBy: T037,T038,T039,T040,T041,T042,T043,T044,T045,T046,T047]
- [ ] T049 [US2] Execute the US2 independent test for real on `requirement-implement-monitor`: run at a cadence point (expect `produced`), then simulate the report-only tier and run again (expect `skipped(budget)`, cycle still completes); record both status lines in `verification.md` (SC-006) [blockedBy: T034,T048]

**Checkpoint**: US1 + US2 both work independently — summaries are produced by the flow itself, and skipping is visible.

---

## Phase 5: User Story 3 — 累积式团队总结 (Priority: P2)

**Goal**: One current summary per team reflecting all runs to date, with human annotations surviving refresh.

**Independent Test**: Refresh twice with a manual annotation added after the first; the second reflects both runs' work items, preserves the annotation verbatim, and the delivery directory still holds exactly one current summary.

### Tests for User Story 3 (MANDATORY) ⚠️

- [ ] T050 [P] [US3] Write `tests/integration/test_summary_accumulation.py` asserting that after two refreshes the delivery directory holds exactly one `summary.md`, both runs' work items appear, and the `## 附注` section is preserved byte-for-byte (FR-017, FR-018, SC-007) [blockedBy: T032]
- [ ] T051 [P] [US3] Add a reproducibility case asserting that deleting the entire delivery directory and regenerating yields an equivalent summary — proving cumulative state is authoritative in `items.jsonl`, not in the derived database (research.md D-1) [blockedBy: T050]
- [ ] T052 [P] [US3] Add an identity-stability case to `tests/integration/test_summary_accumulation.py` asserting zero duplicated and zero silently-dropped work items across refreshes, and that an item crossing from inferred to explicit identity folds into exactly one record (FR-018, FR-027, SC-011) [blockedBy: T050]
- [ ] T053 [P] [US3] Add an FR-029/SC-012 case to `tests/integration/test_summary_accumulation.py` asserting that for a team whose cumulative item count exceeds the threshold, breakdown-diagram nodes stay within the upstream CG-6 limit of 15 at depth ≥2 while data-layer retention is 100% [blockedBy: T050]

### Implementation for User Story 3

- [ ] T054 [US3] Implement per-item cumulative folding in `build-summary-input.py` keyed on work-item identity per invariant IL-2, so a refresh advances existing records rather than rebuilding from empty (FR-018) [blockedBy: T024,T050]
- [ ] T055 [US3] Implement the presentation-level aggregation in `skills/create-team/scripts/build-summary-input.py` of completed and archived items into per-phase counts via `coverage.granularity_truncated`, keeping full retention in the data layer (FR-029) [blockedBy: T028,T054]
- [ ] T056 [US3] Implement goal-change handling in `skills/create-team/scripts/build-summary-input.py`: record the change in report metadata and retain historical work items rather than silently rewriting history (FR-019) [blockedBy: T054]
- [ ] T057 [US3] Document in `skills/create-team/references/summary-mapping.md` that annotation preservation is provided by the invoked skill's existing `## 附注` refresh behavior and MUST NOT be reimplemented team-side (FR-018, WS-10) [blockedBy: T008]
- [ ] T058 [US3] Run `python3 scripts/python/sync-mirrors.py --write` then `--check` [blockedBy: T054,T055,T056,T057]
- [ ] T059 [US3] Execute the US3 independent test for real: refresh `cws-workspace-cluster` twice with a manual `## 附注` entry added in between; record the annotation-preservation and single-summary results in `verification.md` (SC-007) [blockedBy: T050,T058]

**Checkpoint**: The summary is a cumulative current view, not another pile of reports.

---

## Phase 6: User Story 4 — 只读与出处纪律 (Priority: P2)

**Goal**: The summary step is purely derivative — it writes only its own delivery directory, and every number it shows points at a tracked artifact.

**Independent Test**: Audit file changes across a refresh — the change set falls only inside the delivery directory (and feedback store); every percentage's provenance field resolves to a tracked team artifact; an item with no progress basis renders as unknown rather than 0%.

### Tests for User Story 4 (MANDATORY) ⚠️

- [ ] T060 [P] [US4] Extend `tests/contract/test_summary_writeset.py` with the W-1/W-2 write-whitelist assertion and the four-group byte-invariance assertion — team fact sources, monitored targets, the invoked skill, and all of `.specify/agents/**` (FR-020, WS-1…WS-3, plan.md pre-seeded constraint 4, SC-003) [blockedBy: T006,T032]
- [ ] T061 [P] [US4] Add a provenance-coverage case to `tests/contract/test_summary_writeset.py` asserting 100% of emitted status/progress values carry a resolvable, tracked provenance path and that valueless-provenance rows are rejected rather than defaulted (FR-010, SC-004) [blockedBy: T060]
- [ ] T062 [P] [US4] Add a WS-12 reader-hygiene case to `tests/contract/test_summary_writeset.py` scanning the five presentation sections for team-internal identifiers — agent identifiers, result-manifest paths, run-intermediate paths, `.live.log` references (FR-022, SC-010) [blockedBy: T060]
- [ ] T063 [P] [US4] Add an FR-021/WS-4 case to `tests/contract/test_summary_writeset.py` asserting a sub-agent write to a tracked summary artifact is rejected — only the Team Supervisor writes them [blockedBy: T060]
- [ ] T064 [P] [US4] Add an SC-005 consumption case to `tests/contract/test_summary_writeset.py` measuring the generator's team-artifact intake (lines/bytes) at run-count K and 2K and asserting it does not double (FR-009) [blockedBy: T060]

### Implementation for User Story 4

- [ ] T065 [US4] Enforce the write whitelist in the SUMMARIZE step documentation and in `build-summary-input.py` (FG-11): writes restricted to `--out` and its parent `data/` directory (FR-020) [blockedBy: T060]
- [ ] T066 [US4] Implement provenance admissibility in `build-summary-input.py` per WS-5/WS-6/WS-7, rejecting `.specify/teams/.work/**`, `.specify/agents/execution/logs/**`, and out-of-repo paths while accepting tracked `.specify/agents/execution/{configs,scripts}/**` (FR-011) [blockedBy: T060,T024]
- [ ] T067 [US4] Implement the unknown-state degradation in `skills/create-team/scripts/build-summary-input.py` so an item with no status signal emits `unknown` with no `progress_pct` — relying on the invoked engine's measured `progress_pct = null` behavior rather than reimplementing it (FR-006, research.md E-3) [blockedBy: T024]
- [ ] T068 [US4] Implement summary-step invariance for the agent layers in `skills/create-team/scripts/build-summary-input.py` and document it in `skills/create-team/references/summary-mapping.md`: the step MUST NOT touch `.specify/agents/**` at any of its three levels (plan.md pre-seeded constraint 4, WS-3) [blockedBy: T065]
- [ ] T069 [US4] Document in `skills/create-team/references/summary-mapping.md` the FR-020 scoping distinction — byte-invariance binds the **summary step**, while the Supervisor's ordinary cycle writes (appending to `items.jsonl`, issuing identifiers into `STATE.md`, writing the run report) remain permitted in their own phases (WS-1) [blockedBy: T008]
- [ ] T070 [US4] Add the `[TI-nnnn]` inline cross-reference convention for `STATE.md` tracked entries to `skills/create-team/SKILL.md`, satisfying FR-026's `STATE.md` coverage without imposing a schema on its prose form [blockedBy: T008]
- [ ] T071 [US4] Run `python3 scripts/python/sync-mirrors.py --write` then `--check` [blockedBy: T065,T066,T067,T068,T069,T070]
- [ ] T072 [US4] Execute the US4 independent test for real: audit a refresh with `git status --porcelain` before/after, verify the change set and the **five** byte-invariance groups enumerated by SC-003 (team tree / monitored targets / invoked skill / agent layers / pre-existing `.specify/project/` artifacts), and record results in `verification.md` (SC-003, SC-004) [blockedBy: T060,T071]

**Checkpoint**: The derived report cannot contaminate its own fact sources or invent precision.

---

## Phase 7: User Story 5 — 存量团队回填与材料缺口降级 (Priority: P3)

**Goal**: Pre-existing teams summarize from what they already have, and thin-material teams degrade honestly instead of fabricating dates.

**Independent Test**: Summarize an iteration team that has only `runs/` — historical generations backfill as phases and work items; with no schedule material the Gantt is omitted and the task-progress section degrades to a declaration plus the reused breakdown diagram; gaps are listed as a material-gap structure.

### Tests for User Story 5 (MANDATORY) ⚠️

- [ ] T073 [P] [US5] Write `tests/integration/test_summary_legacy_backfill.py` asserting a team with only `team.md` + `runs/` (no ledger, no `STATE.md`, no `run-log.jsonl`) still produces a summary without requiring team rebuild or history rewriting (FR-025) [blockedBy: T032]
- [ ] T074 [P] [US5] Add an FR-027 case to `tests/integration/test_summary_legacy_backfill.py` asserting historical items backfill with `TIX-<8hex>` derived identities, are marked as inferred in the derived data, and that the derivation is the documented `sha256(title + "\u0000" + phase_ref)` truncation — never the raw title, which the DDL rejects [blockedBy: T073]
- [ ] T075 [P] [US5] Add an FR-023/SC-009 degradation case to `tests/integration/test_summary_legacy_backfill.py` asserting zero fabricated dates, durations, or percentages, and that no chart is drawn when its plotting criterion is false [blockedBy: T073]
- [ ] T076 [P] [US5] Add an FR-027 rename case to `tests/integration/test_summary_legacy_backfill.py` asserting that a rename during the inferred era surfaces the prior identity as "not seen this run" in the material-gap declaration rather than dropping it silently [blockedBy: T074]
- [ ] T077 [P] [US5] Add a US5-scenario-5 case to `tests/integration/test_summary_legacy_backfill.py` asserting an eliminated iteration variant counts into the excluded bucket via `excluded_reason` and is not scored as delayed or incomplete [blockedBy: T073]

### Implementation for User Story 5

- [ ] T078 [US5] Implement the run-report backfill path in `build-summary-input.py`, parsing only the fixed sections of the Report contract (header bullets, `## Deliverables` table, `## Result Summary`) by targeted extraction — never whole-file ingestion, so intake stays sublinear in run count (FR-025, FG-3) [blockedBy: T024,T073]
- [ ] T079 [US5] Implement inferred-identity derivation in `skills/create-team/scripts/build-summary-input.py` and the `inferred` marking that lands in the form's `inferred_fields` with a non-empty `inferred_from` basis, which the DDL enforces (FR-027) [blockedBy: T078]
- [ ] T080 [US5] Implement the identity handover per `data-model.md` § 3.1: an item carrying `supersedes` folds into a single record authoritative on the explicit identifier while retaining the inferred identifier's history (FR-027) [blockedBy: T079,T054]
- [ ] T081 [US5] Implement the material-gap declaration listing absent sources (for example an iteration team with no `STATE.md` / `run-log.jsonl`) so the source limitation is stated in the report (FR-023) [blockedBy: T078]
- [ ] T082 [US5] Implement the `declined(no-material)` refusal in `skills/create-team/scripts/build-summary-input.py` for a team that has crossed no phase boundary: no empty charts, and goal criteria alone must not be used to manufacture an apparently complete report (FG-12, Edge Cases) [blockedBy: T078]
- [ ] T083 [US5] Implement `excluded_reason` handling in `skills/create-team/scripts/build-summary-input.py` so eliminated variants enter the excluded bucket rather than the delayed bucket (FR-029, LC-9) [blockedBy: T078]
- [ ] T084 [US5] Implement maturity anchoring in `skills/create-team/scripts/build-summary-input.py` so `maturity_at_event` fixes each event's state semantics and an L1→L2 promotion cannot retroactively reinterpret report-only-era items (LC-10, Edge Cases) [blockedBy: T078]
- [ ] T085 [US5] Run `python3 scripts/python/sync-mirrors.py --write` then `--check` [blockedBy: T078,T079,T080,T081,T082,T083,T084]
- [ ] T086 [US5] Execute the US5 independent test for real on `draw-plantuml-optimizer` (iteration, `runs/` only): confirm generation backfills, the Gantt is omitted for want of schedule material, and gaps are declared; record in `verification.md` (SC-009) [blockedBy: T073,T085]

**Checkpoint**: All five stories are independently functional.

---

## Phase 8: User Story 6 — goal 索引与跨团队聚合 (Priority: P2)

**Goal**: One goal directory aggregates every team pursuing that goal, with per-team attribution and safe concurrent refresh.

**Independent Test**: Two fixture teams declaring the same `goal_slug` (different patterns) each run once — both teams' work items appear in one goal delivery directory, each attributable to its producing team, milestones not duplicated; refreshing only one team leaves the other's prior contributions intact; editing goal prose does not move the directory.

### Tests for User Story 6 (MANDATORY) ⚠️

- [ ] T104 [P] [US6] Write `tests/integration/test_goal_aggregation.py` asserting FG-14: two teams sharing a `goal_slug` produce one delivery directory containing both teams' work items, with milestones emitted once per goal rather than once per team (FR-032, SC-014) [blockedBy: T032]
- [ ] T105 [P] [US6] Add an FG-15 collision case to `tests/integration/test_goal_aggregation.py` asserting that unprefixed per-team ids would collide (upstream exit 3, message `在本实体内重复`) and that the generator's `<team-slug>.` prefixing makes the aggregate load succeed — pinning the measured DDL behavior rather than restating it [blockedBy: T104]
- [ ] T106 [P] [US6] Add an FG-17 attribution case to `tests/integration/test_goal_aggregation.py` asserting every work item resolves to its producing team by machine, and that reader sections still contain zero team-internal identifiers (FR-033, SC-014) [blockedBy: T104]
- [ ] T107 [P] [US6] Add an FR-032 persistence case to `tests/integration/test_goal_aggregation.py` asserting that refreshing via team A leaves team B's prior contributions present and unmodified [blockedBy: T104]
- [ ] T108 [P] [US6] Add an FR-034 migration case to `tests/integration/test_goal_aggregation.py` asserting a team without `goal_slug` lands in an inferred goal directory marked inferred, and that declaring an explicit `goal_slug` afterwards merges its history with zero parallel directories left behind (SC-013) [blockedBy: T104]
- [ ] T109 [P] [US6] Write `tests/integration/test_goal_concurrent_refresh.py` asserting FR-035 / TG-16 / WS-13: two near-simultaneous refreshes of one goal serialize into exactly one current summary, zero lost updates, zero half-written directories, and the suppressed one records a status line (SC-015) [blockedBy: T032]

### Implementation for User Story 6

- [ ] T110 [US6] Implement goal-identity resolution in `skills/create-team/scripts/build-summary-input.py` per FG-13 — explicit `goal_slug` else team-slug inference marked in `inferred_fields` — and derive `delivery_dir` from it (FR-031, FR-034) [blockedBy: T020,T102]
- [ ] T111 [US6] Implement goal-membership discovery in `skills/create-team/scripts/build-summary-input.py`: scan `.specify/teams/*/team.md` frontmatter for every team resolving to the same goal identity, reading only the frontmatter (FG-14, FG-2) [blockedBy: T110]
- [ ] T112 [US6] Implement the cross-team fold in `skills/create-team/scripts/build-summary-input.py` — union of work items, phases and people across the discovered teams, with `<team-slug>.` id namespacing and goal-level milestones emitted once (FR-032, FG-15, FG-16) [blockedBy: T111,T024]
- [ ] T113 [US6] Implement machine-decidable team attribution in `skills/create-team/scripts/build-summary-input.py` carried by both the id prefix and the `source` provenance path, and surface it in presentation without leaking internal identifiers (FR-033, FG-17) [blockedBy: T112]
- [ ] T114 [US6] Implement the rebinding and deletion rules in `skills/create-team/scripts/build-summary-input.py` per WS-11 / WS-12: a rebound team's prior contributions stay in the original goal directory annotated as no longer contributing; a deleted team's history is retained without dangling provenance [blockedBy: T112]
- [ ] T115 [US6] Implement refresh serialization for the goal delivery directory in `skills/create-team/SKILL.md`'s SUMMARIZE step — single-writer discipline, complete-or-leave-previous, and a status line for the suppressed refresh (FR-035, TG-16, WS-13) [blockedBy: T042]
- [ ] T116 [US6] Add goal-identity and target-directory disclosure to the confirmation gate in `templates/commands/team.md` per TG-18 (which goal, explicit or inferred, and where the summary lands) [blockedBy: T045]
- [ ] T117 [US6] Build the aggregation fixture pair in `tests/fixtures/teams/` — two teams declaring one shared `goal_slug` on different patterns — since no two existing teams share a goal (measured: all four have distinct goals and none declares `goal_slug`) [blockedBy: T030]
- [ ] T118 [US6] Document the goal index in `skills/create-team/references/summary-mapping.md`: the dual-index split, the aggregation scope table from `data-model.md` § 2, and the `.specify/project/` coexistence rule (FR-030, FR-036) [blockedBy: T008]
- [ ] T119 [US6] Run `python3 scripts/python/sync-mirrors.py --write` then `--check` [blockedBy: T110,T111,T112,T113,T114,T115,T116,T118]
- [ ] T120 [US6] Execute the US6 independent test for real on the fixture pair: verify one delivery directory, both teams' items present and attributable, milestones once, and that editing one team's goal prose leaves the directory path unchanged; record in `verification.md` (SC-013, SC-014) [blockedBy: T104,T119]

**Checkpoint**: The goal index answers "how far has this goal progressed" across teams; the team index still answers "how is this team running".

---

## Phase 9: Polish & Cross-Cutting Concerns

### Mirror Parity (one verify task per plan.md Mirror Obligations row)

- [ ] T087 [P] Verify row 1 — `templates/commands/team.md` against `.specify/templates/commands/team.md` (`diff -q`) and confirm the disclosure edit is present in all five per-tool copies: `.claude/commands/speckit.team.md`, `.github/prompts/speckit.team.prompt.md`, `.qoder/commands/speckit.team.md`, `.qwen/commands/speckit.team.toml`, `.opencode/command/speckit.team.md` [blockedBy: T048]
- [ ] T088 [P] Verify row 2 — `skills/create-team/SKILL.md` against `.specify/skills/create-team/SKILL.md` (`diff -q`) [blockedBy: T071]
- [ ] T089 [P] Verify row 3 — `skills/create-team/references/summary-mapping.md` against its mirror (`diff -q`) [blockedBy: T071]
- [ ] T090 [P] Verify row 4 — `skills/create-team/scripts/build-summary-input.py` against its mirror (`diff -q`) and confirm `--help` is identical on both copies [blockedBy: T085]
- [ ] T091 [P] Verify row 5 — `skills/improve-team/SKILL.md` against its mirror (`diff -q`) [blockedBy: T093]
- [ ] T092 [P] Verify row 6 — the three `skills/create-team/templates/teams/*.md` presets against their mirrors `.specify/skills/create-team/templates/teams/*.md` (`diff -q`) [blockedBy: T048]

### Cross-cutting

- [ ] T093 Add `config.summary` tuning (enable/disable, cadence, delivery directory) to the modify surface of `skills/improve-team/SKILL.md`, keeping maturity promotion as the existing separate action [blockedBy: T011]
- [ ] T094 Resolve the second research.md § O carry-forward: `skills/create-team/scripts/dispatch.sh` defaults `DISPATCH_LOG_DIR` to `${TMPDIR:-/tmp}/spec-kit-dispatch` (outside the repo) while plan.md's pre-seeded block and requirements.md FR-011 both describe the visibility triplet as living in `.specify/agents/execution/logs/`. Either change the script default to that path or correct the two documents; both readings already forbid the triplet as provenance, so this is a documentation/code consistency fix, not a behavior change [blockedBy: T066]
- [ ] T095 [P] Render-verify: produce the breakdown diagram for one real team's summary and inspect the output — invoke as `bash skills/draw-plantuml/scripts/render-plantuml.sh <delivery_dir>/assets/wbs.puml <delivery_dir>/assets wbs` from a directory other than the repo root, since omitting the output directory writes `diagram.*` into the current working directory (measured) [blockedBy: T032]
- [ ] T096 [P] Refresh-verify: re-run the goal summary refresh twice consecutively via `cws-workspace-cluster` and confirm repeatability against its resolved `.specify/project/goal/<goal-slug>/` — identical artifact set, one current summary, `## 附注` preserved [blockedBy: T059]
- [ ] T097 Update `docs/reference/commands/team.md` with the summary mechanism: trigger points, `config.summary`, the delivery directory, and the run-report status line [blockedBy: T048]
- [ ] T098 Add a `## Team Summary` subsection to `docs/reference/skills/` coverage for `create-team`, documenting the concept mapping and pointing at `summary-mapping.md` as the single source of truth [blockedBy: T097]
- [ ] T099 Run the full suite and compare against the T001 baseline: `python3 -m pytest -q > /tmp/036-current.txt` then `comm -13 /tmp/036-baseline.txt /tmp/036-current.txt` must show zero new failures (GATE-1) [blockedBy: T086,T093,T094]
- [ ] T100 Write `verification.md` with a status row for every SC-001…SC-015, citing the task and captured evidence that proves each (GATE-4, DoD-6) [blockedBy: T032,T049,T059,T072,T086,T095,T096,T099]
- [ ] T101 Propose `build-summary-input.py` for promotion to a Tool record under `.specify/memory/tools/` per Constitution Principle XII, now that it is a verified repeatable capability [blockedBy: T099]

---

## Dependencies & Execution Order

```text
Phase 1 Setup (T001-T003)
      ↓
Phase 2 Foundational (T004-T013, T102-T103)  ← blocks everything
      ↓
Phase 3 US1 (T014-T032) 🎯 MVP ── independently deliverable
      ↓
Phase 4 US2 (T033-T049) ── needs US1's generator to have something to trigger
      ↓
   ┌──┴──────────────┐
Phase 5 US3        Phase 6 US4      ← both build on US1; largely parallel
(T050-T059)        (T060-T072)
   └──┬──────────────┘
      ↓
Phase 7 US5 (T073-T086) ── needs US3's folding for identity handover
      ↓
Phase 8 US6 (T104-T120) ── goal 索引与跨团队聚合;需 US1 的生成器与 US2 的触发点
      ↓
Phase 9 Polish (T087-T101)
```

**Story independence**: US1 is the only story that must land first — it is the MVP and every other story acts on its output. US3 and US4 are independent of each other. US5 depends on US3 only for the identity-handover fold (T080 ← T054).

## Parallel Execution Examples

- **Phase 2 tests**: T004, T005, T006 run in parallel (three distinct test files/cases).
- **Phase 3 tests**: T014 creates the file; T015-T018 then append independent cases and can be written in parallel by separate workers; T019 is a different file and is fully parallel.
- **Phase 3 entity mappings**: T021-T026 touch six independent mapping functions in one module — parallelizable with care, or serialize if a single worker owns the file.
- **Phase 5 + Phase 6**: whole phases run concurrently once US1 closes.
- **Phase 9 mirror verification**: T087-T092 are six independent `diff -q` checks, fully parallel.

## Implementation Strategy

**MVP = Phase 1 + Phase 2 + Phase 3 (US1)**. That alone delivers value that does not exist today: any team can be summarized on demand from its existing artifacts, with zero manual form entry. The mechanism is not yet automatic, which is exactly what US2 adds.

**Incremental delivery**: US1 (on-demand summary) → US2 (automatic at boundaries, budget-gated) → US3 (cumulative, annotations preserved) → US4 (provenance and read-only discipline enforced) → US5 (legacy backfill and honest degradation) → US6 (goal index aggregating across teams).

**Task count**: 120 total — Setup 3, Foundational 12, US1 19, US2 17, US3 10, US4 13, US5 14, US6 17, Polish 15.

**Revision note (2026-08-04 dual index)**: T102/T103 added to Foundational (goal identity); Phase 8 US6 added (T104-T120); T009/T014/T019/T020/T021/T022/T023/T024/T025/T096 amended for goal scoping. Task IDs are not renumbered — the T102+ block is the revision increment, which keeps prior IDs stable for anything already referencing them.

## Notes

- `[~]`-eligible: T095 (render-verify) depends on the PlantUML server; `java` is present but no local jar exists, so there is no offline fallback. If the server is unreachable at implement time, defer with a reason rather than skipping the verification silently.
- Pin hygiene: T053's node-count assertion hard-codes 15 because that count **is** the upstream CG-6 contract; if the upstream threshold changes, it must be updated in the same task that changes it. T005's identifier-grammar assertion derives its expectation from `project-db.py`'s actual exit code, not from a restated regex, so an upstream DDL change surfaces as a failure rather than a false pass.
- Do not hand-edit `.specify/**` mirrors or per-tool command copies; every mirror task routes through `sync-mirrors.py --write`.
