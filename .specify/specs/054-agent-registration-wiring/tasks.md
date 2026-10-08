# Tasks: Agent 定义到宿主注册面的接线(Agent Registration Wiring)

**Requirement ID**: 054
**Requirement Key**: 054-agent-registration-wiring
**Related Feature**: 044 Agent Metadata Portability
**Input**: Design documents from `.specify/specs/054-agent-registration-wiring/`
**Prerequisites**: plan.md (required), requirements.md (required), data-model.md, contracts/, quickstart.md

**Tests Mode**: ON — Constitution Principle IV "Test-First & Contract-Driven Implementation" (NON-NEGOTIABLE) mandates red-first tests for new behavior; Principle VII's *template-only features* gate applies to the doc/skill/template surfaces (structural contract tests on content/canonical paths/mirror parity, not unit tests). This feature is mixed: runtime code (CLI subcommand + frontmatter key) gets real pytest contract tests red-first; template/skill/doc surfaces get structural contract tests red-first (asserting target content BEFORE the authoring task lands it).

**Organization**: Tasks grouped by user story. Story phases in priority order (US1, US2 = P1; US3, US4 = P2). Mirror obligations from plan.md are first-class paired write+verify tasks.

## Definition of Done

- DoD-1: All 14 FR satisfied (FR-001..FR-014) — spec `.specify/specs/054-agent-registration-wiring/requirements.md` validator exit 0 and every FR maps to a closed task or `[green: ...]` attribution
- DoD-2: All automated tests pass — full suite has zero NEW failures vs the name-level baseline (comm -13 empty), including the new contract tests
- DoD-3: Manual verification completed — quickstart.md scenario 3 executed with real output into `notes/quickstart-run.md`; mutation-drill evidence for every guard recorded under `notes/red-first-evidence.md`
- DoD-4: Documentation updated — agent-definitions.md / symlink-model.md / supported-agent-tools.md carry their FR-009/010 additions; teaching surfaces re-teach the real model
- DoD-5: Code reviewed and approved — mirror obligations all verified (sync-mirrors --check no NEW drift vs 2026-10-08 baseline; per-tool copies regenerated and contain the edit)
- DoD-6: Changes validated against success criteria SC-001..SC-004 from requirements.md, recorded in verification.md

**DoD Status**: pending

## Completion Gate

- GATE-1: Zero NEW test failures vs name-level baseline — check: `scripts/bash/run-tests.sh tests/contract/ --names-out .specify/specs/054-agent-registration-wiring/baseline-failed.txt` then `comm -13 <baseline> <current>` empty (baseline owner: implement.md § Test runs)
- GATE-2: Mirror obligations clean — check: `python3 scripts/python/sync-mirrors.py --check` (no NEW drift vs the 2026-10-08 exit-0 baseline recorded in plan.md Phase 0) AND `python3 scripts/python/regen-command-copies.py` regenerates the 4 tool copies of `templates/commands/agents.md` containing the edit
- GATE-3: No `[ ]`/`[>]` rows remain — check: `grep -cE '^- \[[ >]\]' .specify/specs/054-agent-registration-wiring/tasks.md` returns 0
- GATE-4: verification.md lists every SC-001..SC-004 with a status — check: `grep -cE 'SC-00[1-4]' .specify/specs/054-agent-registration-wiring/verification.md` >= 4
- GATE-5: Retired-model wording absent — check: grep for the two retired literal classes (STR-001 verbatim + SKILL.md-specific phrases) over `templates/commands/agents.md`, `skills/create-agent/SKILL.md`, and the 4 tool copies returns zero hits (the teaching guard encodes this; gate re-runs the guard: `scripts/bash/run-tests.sh tests/contract/test_teaching_surfaces.py`)

## Environment Prerequisites

- pytest runner: available — probe: `scripts/bash/run-tests.sh --version` equivalent (`python3 -m pytest --version` → pytest present; `.venv` not required) @ 2026-10-08; affected: all test tasks
- `specify` CLI on PATH: available — probe: `which specify` → `/usr/local/bin/specify`; `python3 -c "import specify_cli"` → importable in-tree @ 2026-10-08; affected: render-agents subcommand tasks (T008..T012) — in-tree tests import the module; PATH CLI used only for demo scenarios
- git worktree/branch: on `054-agent-registration-wiring` — probe: `git rev-parse --abbrev-ref HEAD` @ 2026-10-08; affected: all commits
- no external environment (docker/cluster/network) is required by any task

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1..US4)
- **[blockedBy: Txxx]**: explicit dependency tag — MUST NOT start until listed tasks are `[X]`
- **[green: <contract>#<clause>]**: green-point attribution — this row turns that contract clause green

## Path Conventions

Single project: `src/`, `tests/`, `templates/`, `skills/`, `shared/`, `docs/` at repository root. Mirrors under `.specify/` are generated (never hand-edited).

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Freeze measurements and evidence scaffolding so later phases cite measured values, not claims.

- [X] T001 Create `notes/` evidence scaffolding in `.specify/specs/054-agent-registration-wiring/notes/` (empty red-first-evidence.md, quickstart-run.md, pre-change-measurements.md with headers)
- [X] T002 Capture name-level failing-test baseline into `.specify/specs/054-agent-registration-wiring/baseline-failed.txt` — command: `scripts/bash/run-tests.sh tests/contract/ --names-out .specify/specs/054-agent-registration-wiring/baseline-failed.txt`; record the summary line (N failed / M passed) verbatim into `notes/pre-change-measurements.md` with the capture date. [DONE AT GENERATION: captured 2026-10-08 — 49 failed / 2574 passed / 2 skipped in 58.52s; baseline-failed.txt holds 49 entries. Re-capture at implement start if the tree has advanced (never-cache rule).]
- [X] T003 [P] Record pre-change measurements into `notes/pre-change-measurements.md`: (a) `grep -rn "Tool-specific directories are symlinks"` over templates/commands/agents.md + 4 tool copies (paste real hits with line numbers — measured 2026-10-08: source :25 and copies present); (b) `sed -n '122p;127p' skills/create-agent/SKILL.md` (paste the two retired phrases verbatim); (c) `python3 scripts/python/sync-mirrors.py --check` (paste exit 0 output); (d) `ls .specify/agents/instances/` (empty)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The runtime half of the chain — the render trigger CLI subcommand and the `team-scope` neutral key — blocks both P1 stories (US1 teaching cites the command; US2 instantiation writes the key and invokes the command).

### Tests (red-first)

- [X] T004 [P] Red-first contract tests for the `render-agents` subcommand AND the `team-scope` neutral key in `tests/contract/test_render_trigger_cli.py`: (a) `--ai qoder` renders instance definitions into a tmp project's `.qoder/agents/` (real files, frontmatter `name`/`tools`/`maxTurns` mapped from neutral keys); (b) `--ai codex` and `--ai unknown-tool` exit non-zero naming legal values; (c) empty neutral layers → exit 0 with rendered=0; (d) placeholder-carrying definition → non-zero exit naming file+key; (e) a definition whose frontmatter carries `team-scope: some-team` passes `load_project_agent_definitions`; (f) `team-scope` is NOT rendered into tool output (`renders_to_tools=False`); (g) unknown-key rejection (:273-279) still holds for a genuinely unknown key (e.g. `bogus-key:`). Fixture: minimal tmp project with one valid + one invalid definition. Confirm red on current tree (subcommand absent, key rejected → both red), record into notes/red-first-evidence.md. [green: contracts/render-trigger-cli.md#C-1] [green: contracts/render-trigger-cli.md#C-2] [green: contracts/render-trigger-cli.md#C-3] [green: contracts/render-trigger-cli.md#C-4] [green: contracts/render-trigger-cli.md#C-5] [green: contracts/render-trigger-cli.md#C-6] [green: contracts/seat-instantiation.md#C-1] [green: contracts/seat-instantiation.md#C-2]
- [X] T005 [blockedBy: T004] Extend `tests/contract/test_render_trigger_cli.py` with the failure-path test functions covering C-5's error table end-to-end (AgentMetadataError exit code captured, legal-values listing on bad `--ai`) — authored red where the behavior is absent, kept as a separate row from T004 for review granularity; green claims for this file live on T004 (single green point per test file). Evidence to notes/red-first-evidence.md.

### Implementation

- [X] T006 Add `team-scope` to the neutral metadata key set (`NEUTRAL_AGENT_METADATA_KEYS`, framework-only block beside `role-scope` at src/specify_cli/__init__.py:139 area; `renders_to_tools=False`) in `src/specify_cli/__init__.py`
- [X] T007 Implement `render-agents` subcommand in `src/specify_cli/__init__.py`: `@app.command()` beside init(:2653)/check(:2993); `--ai` required; value domain = render-mode tools from `_AGENT_METADATA_MAPPING`; delegates `render_agents_for_tool(project_path, tool)`; stats summary line; `AgentMetadataError` → non-zero exit with its existing file+key message; annotated/unknown tool → error listing legal values. [blockedBy: T006]
- [X] T008 Make T004+T005 green: run `scripts/bash/run-tests.sh tests/contract/test_render_trigger_cli.py` — every test from T004/T005 passes; paste real output into notes/red-first-evidence.md (red→green transition). [blockedBy: T007]

---

## Phase 3: User Story 1 — 教学面改教真实渲染模型 (Priority: P1) 🎆 MVP

**Goal**: The three teaching surfaces (agents.md command template, create-agent SKILL.md :122/:127) stop teaching the retired per-file symlink model and teach the real render model + the render-trigger truth (FR-001..FR-003), with an absence-pin guard (FR-011) so a regression goes red.

**Independent Test**: Grep the retired literals (STR-001 class + SKILL.md-specific class) over source + mirrors + 4 tool copies → zero hits; the C-7 guard test passes; mutation drill (re-introduce one phrase → guard red → restore → byte-equal) recorded.

### Tests (red-first)

- [X] T009 [US1] Red-first absence-pin guard in `tests/contract/test_teaching_surfaces.py`: asserts the STR-001 literal ("Tool-specific directories are symlinks — never write to them directly") is ABSENT from `templates/commands/agents.md`, `.claude/commands/speckit.agents.md`, `.github/prompts/speckit.agents.prompt.md`, `.opencode/command/speckit.agents.md`, `.qoder/commands/speckit.agents.md`; the SKILL.md retired phrases ("Per-file symlinked into every officially supported tool's agent config directory", "the CLI (re)creates a **per-file** symlink for each") ABSENT from `skills/create-agent/SKILL.md` + `.specify/skills/create-agent/SKILL.md`; the trigger-truth phrase (`specify render-agents`) PRESENT in both teaching sources; and the `team-scope` key listed in `skills/create-agent/SKILL.md`'s authoring key section. Red on current tree (literals present — measured in T003), evidence to notes/red-first-evidence.md. [green: contracts/teaching-and-guards.md#C-1] [green: contracts/teaching-and-guards.md#C-2] [green: contracts/teaching-and-guards.md#C-3] [green: contracts/teaching-and-guards.md#C-4] [green: contracts/seat-instantiation.md#C-3] [blockedBy: T005]

### Implementation

- [X] T010 [P] [US1] Rewrite `templates/commands/agents.md` teaching (was :25): real render model — host agent dirs are renderer-produced REAL files written by the specify CLI, legacy symlinks replaced; replace the "or advise `specify init`" re-render phrasing with the render-trigger truth: definitions land in `.specify/agents/{templates,instances}/`, reaching the host registration surface = run `specify render-agents --ai <tool>` (init remains the first-install entry, keep its mention for that role only). [blockedBy: T007]
- [X] T011 [P] [US1] Rewrite `skills/create-agent/SKILL.md` :122 table row + :127 paragraph: same real-model semantics as T010; update the FR-010/012 references to spec 040's current contract semantics; add the render-trigger truth line to the persistence rules; add `team-scope` to the authoring key list (instance layer, framework-only, seat provenance — pointer to agent-definitions.md, no key-set restatement). [blockedBy: T006]
- [X] T012 [US1] Regenerate per-tool command copies: `python3 scripts/python/regen-command-copies.py` — the 4 tool copies of speckit.agents contain the T010 edit; verify by grep for a T010-added phrase in each copy; paste output into notes/red-first-evidence.md. [blockedBy: T010]
- [X] T013 [US1] Make T009 green + mutation drill: guard passes; then plant one retired phrase back into `templates/commands/agents.md` → guard RED → restore exactly → `diff -q` against pre-mutation copy byte-equal → record drill (red output + restore proof) in notes/red-first-evidence.md. [blockedBy: T010,T011,T012]

---

## Phase 4: User Story 2 — 建队即实例化 + modify 回填 (Priority: P1) 🎆 MVP

**Goal**: `/speckit.team create` instantiates each referenced seat via create-agent's delegation (placeholders resolved, `team-scope` set), then directly executes the render trigger (FR-004/006/008/013); `/speckit.team modify` (improve-team) backfills missing seats opt-in (FR-014). With US1 this closes the observed "only general-purpose subagents" chain.

**Independent Test**: In a scratch project (or this repo's dogfood team), create a team referencing a stage frame → seat instance exists in `.specify/agents/instances/` with `team-scope` and resolved placeholders → `specify render-agents --ai qoder` → seat appears in `.qoder/agents/`; conflict case (existing same-slug definition) disclosed not overwritten.

### Tests (red-first)

- [X] T014 [US2] Red-first structural contract test in `tests/contract/test_seat_instantiation_flow.py` (guard set B): (a) `skills/create-team/SKILL.md` create flow contains a seat-instantiation step naming `create-agent` delegation and a render-trigger step naming `specify render-agents` (machine-checkable markers, prose-agnostic per test_team_command_routing.py precedent); (b) `skills/create-team/references/create-mode.md` schema note states the two legitimate member forms + `team-scope`; (c) `skills/improve-team/SKILL.md` modify flow contains the opt-in backfill step + render trigger; (d) failure-disclosure wording present (render trigger failure MUST be surfaced); (e) the one-line guidance「存量团队经一次 modify 即可让席位上注册面」present in create-team and improve-team modify docs. Red on current tree (steps absent), evidence recorded. [green: contracts/seat-instantiation.md#C-4] [green: contracts/seat-instantiation.md#C-5] [green: contracts/seat-instantiation.md#C-6] [green: contracts/seat-instantiation.md#C-7] [green: contracts/seat-instantiation.md#C-8] [green: contracts/seat-instantiation.md#C-9] [green: contracts/modify-backfill.md#C-1] [green: contracts/modify-backfill.md#C-2] [green: contracts/modify-backfill.md#C-3] [green: contracts/modify-backfill.md#C-8] [blockedBy: T009]

### Implementation

- [X] T015 [P] [US2] Author the seat-instantiation + render-trigger steps into `skills/create-team/SKILL.md` and `skills/create-team/references/create-mode.md` (create flow): new step between roster step (:14) and landing step (:16) — for each `agent:` reference: resolve existing persistent definition first (instance wins), else delegate to `create-agent` via its `AgentAuthoringRequest` convention (kind: instance; fill ALL frame placeholders; set `team-scope: <team-slug>`; no `capacity-scope` for stage-frame seats; same-slug collision → disclose and halt that seat); flow end: run `specify render-agents --ai <current-tool>`, stats summary in report, failure disclosed not skipped. Update create-mode.md Schema notes member-resolution clause (:128 area) per contract C-3.1/C-3.2. [blockedBy: T007]
- [X] T016 [P] [US2] Author the opt-in backfill step into `skills/improve-team/SKILL.md` (modify flow): for the modify-target team only, resolve each `agent:` reference, instantiate missing seats (same constraints as T015 — shared clauses per contract modify-backfill C-3.1), run the render trigger, report distinguishes existing/ instantiated/ render-stats; plus the one-line guidance「存量团队经一次 modify 即可让席位上注册面」in create-team and improve-team modify docs (contract modify-backfill C-4.2). [blockedBy: T007]
- [X] T017 [US2] Mirror-parity write for skills: `python3 scripts/python/sync-mirrors.py --write --only skills` regenerates `.specify/skills/create-team/**`, `.specify/skills/create-agent/**`, `.specify/skills/improve-team/**` mirrors (covers plan.md Mirror Obligations rows 1-4 + 6); then `--check` shows no NEW drift vs the 2026-10-08 exit-0 baseline. [blockedBy: T015,T016,T011]
- [X] T018 [US2] Make T014 green + mutation drill on the create-team step marker: plant-err → red → restore → byte-equal, recorded in notes/red-first-evidence.md. [blockedBy: T015,T016,T017]

---

## Phase 5: User Story 3 — Qoder IDE 与 CLI 的 agent 面关系文档 (Priority: P2)

**Goal**: The officially-verified IDE/CLI shared-path fact lands in its owner docs with provenance (FR-009/010), pointer-shaped (no triple restatement).

**Independent Test**: The three docs each carry their addition; symlink-model.md and supported-agent-tools.md reference (not restate) agent-definitions.md's concept; provenance URL + verification date present.

### Tests (red-first)

- [X] T019 [US3] Red-first structural contract test in `tests/contract/test_agent_surface_docs.py` (guard set C): (a) `shared/definitions/agent-definitions.md` contains a "Host Registration Surface" definition section; (b) `shared/workflow/symlink-model.md` contains the agent-surface CLI/IDE entry with both provenance URLs and the 2026-10-08 verification date; (c) `docs/reference/cli/supported-agent-tools.md` qoder entry states the shared path + frontmatter-name rule + user-level scope boundary; (d) pointer discipline: the concept definition appears once in agent-definitions.md and the other two docs reference it without restating the full definition. Red on current tree, evidence recorded. [green: contracts/teaching-and-guards.md#C-5] [green: contracts/teaching-and-guards.md#C-6] [green: contracts/teaching-and-guards.md#C-7] [green: contracts/teaching-and-guards.md#C-8] [blockedBy: T014]

### Implementation

- [X] T020 [P] [US3] Author the "宿主注册面 (Host Registration Surface)" definition into `shared/definitions/agent-definitions.md` (concept owner): per-render-mode-tool directory read for agent definitions, path from the code mapping table, real-file render products; plus the Seat Instance subtype taxonomy entry and `team-scope` (pointer to the code key set as semantics owner). [blockedBy: T006]
- [X] T021 [US3] Author the agent-surface CLI/IDE entry into `shared/workflow/symlink-model.md`: Qoder IDE and CLI share the project-level `.qoder/agents/` (provenance: https://docs.qoder.com/extensions/subagent + https://docs.qoder.com/cli/subagent, verified 2026-10-08); user-level `~/.qoder/agents/` untouched by the framework; cross-reference agent-definitions.md for the concept, no restatement. [blockedBy: T020]
- [X] T022 [US3] Author the qoder agent-surface note into `docs/reference/cli/supported-agent-tools.md`: shared path, filename-does-not-define-name (frontmatter `name` is authoritative), user-level scope boundary; reference agent-definitions.md for the concept. [blockedBy: T020]
- [X] T023 [US3] Mirror-parity write for shared: `python3 scripts/python/sync-mirrors.py --write --only shared` (agent-definitions.md + symlink-model.md mirrors; docs/ is NOT mirrored); `--check` no NEW drift. [blockedBy: T020,T021]
- [X] T024 [US3] Make T019 green + mutation drill (remove the symlink-model.md entry heading → red → restore → byte-equal), evidence recorded. [blockedBy: T021,T022,T023]

---

## Phase 6: User Story 4 — 漂移守卫与变异演练取证 (Priority: P2)

**Goal**: Chain-closure guard (FR-012) + manifest-correspondence guard (SC-003's guard form, contract C-10) with mutation-drill evidence for every guard; the guard set is complete when US1/US2/US3 surfaces are all landed.

**Independent Test**: all five guard files (`test_render_trigger_cli.py`, `test_teaching_surfaces.py`, `test_seat_instantiation_flow.py`, `test_agent_surface_docs.py`, `test_agent_chain_guards.py`) green via `scripts/bash/run-tests.sh`; every guard has a recorded mutation drill in notes/red-first-evidence.md; full-suite comm -13 vs baseline empty.

### Tests + evidence

- [ ] T025 [US4] Aggregate guards in `tests/contract/test_agent_chain_guards.py`: (a) chain-closure — the create-flow's programmatic core is NOT runtime (prompt skill), so the guard asserts the landed *wiring*, not a live run: create-team SKILL step markers present AND `specify render-agents --ai qoder` on a fixture project with an instantiated seat definition produces the seat file in `.qoder/agents/` with `tools`/`maxTurns` frontmatter (the runtime half of the chain) AND the manifest records the rendered file (`.specify/agents/.render-manifest.json` entry for the seat); (b) manifest-correspondence (read-only) — every manifest entry's source resolves to a definition in `.specify/agents/{templates,instances}/` and every definition file (from glob, not a hand list — pin-hygiene count rule) has a manifest entry after a render pass; user-added foreign files in the tool dir are NOT flagged (third-party edge case). [green: contracts/teaching-and-guards.md#C-9] [green: contracts/teaching-and-guards.md#C-10] [blockedBy: T008,T015,T019]
- [ ] T026 [US4] Mutation-drill evidence for every guard (T004 CLI guard, T009 teaching guard, T014 wiring guard, T019 doc guard, T025 aggregate guards — any not yet drilled at their own make-green rows): plant-err → red → restore → byte-equal for each, all recorded in notes/red-first-evidence.md with real outputs. [green: contracts/teaching-and-guards.md#C-11] [blockedBy: T025]
- [ ] T027 [US4] Guard-suite green run: `scripts/bash/run-tests.sh tests/contract/test_render_trigger_cli.py tests/contract/test_teaching_surfaces.py tests/contract/test_seat_instantiation_flow.py tests/contract/test_agent_surface_docs.py tests/contract/test_agent_chain_guards.py` — all green, summary pasted into notes/red-first-evidence.md. [blockedBy: T026]

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Full-suite regression, quickstart validation, feature registry sync, F-A02 dead-letter closure conditions.

- [ ] T028 Full-suite regression: `scripts/bash/run-tests.sh tests/contract/ --names-out <current>` then `comm -13 baseline-failed.txt current` — empty (zero NEW failures); paste summary into verification.md. [blockedBy: T027]
- [ ] T029 [P] Execute quickstart.md scenario 3 (executable part) with real output into `notes/quickstart-run.md` (mirror check + retired-literal grep + guard run); teardown = none (read-only checks). [blockedBy: T027]
- [ ] T030 [P] Update Feature registry: `features/044.md` Key Changes notes gain the implementation outcome; `features.md` 044 row Last Updated; status stays Implemented (no regression — Principle VII). [blockedBy: T028]
- [ ] T031 Record F-A02 dead-letter closure condition in verification.md: three surfaces fixed (T010/T011/T012), guard pinned (T013), closure actionable in the feedback ledger (consumption-side step, not code). [green: contracts/teaching-and-guards.md#C-12] [blockedBy: T028]

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: no dependencies; T002's baseline number is re-captured at implement start if the tree advanced
- **Phase 2 (Foundational)**: after Setup; BLOCKS US1/US2/US3 (T010 cites the command, T015/T016 invoke it, T020 needs the key)
- **Phase 3 (US1)** / **Phase 4 (US2)**: after Phase 2; independent of each other except T017 (mirror write) covers skills files from BOTH stories — run after T015+T016+T011 all land
- **Phase 5 (US3)**: after Phase 2 (T020 needs T006); independent of US1/US2
- **Phase 6 (US4)**: guards aggregate — T025 needs T008+T015; T027 needs all guards
- **Phase 7 (Polish)**: after all stories

### User Story Dependencies

- **US1 (P1)**: Foundational only. MVP half #1.
- **US2 (P1)**: Foundational only (T015/T016 block on T007 for the command's existence; not on US1 tasks). MVP half #2.
- **US3 (P2)**: Foundational only (T020 blocks on T006).
- **US4 (P2)**: blocks on US2's wiring (T015) and Phase 2 runtime (T008).

### Within Each User Story

- Tests red-first → implementation → mirror-parity → green + mutation drill
- Models before services does not apply (doc-feature taxonomy: author-section → mirror-parity → render-verify → refresh-verify)

### Parallel Opportunities

- Five guard files, one per contract family (validator's single-green-point-per-test-file rule): `test_render_trigger_cli.py` (T004 claim row, T005 appends), `test_teaching_surfaces.py` (T009), `test_seat_instantiation_flow.py` (T014), `test_agent_surface_docs.py` (T019), `test_agent_chain_guards.py` (T025) — each file has exactly ONE claim-carrying row; T005/T026/T027 write into or mutate these files but carry no per-file green claims (T005's claims live on T004; T026's C-11 drill claim's write target is the evidence file, not a test path)
- T010 ∥ T011 (different teaching sources: agents.md vs SKILL.md); T015 ∥ T016 (create-team vs improve-team); T020 alone then T021, T022 serial (both reference agent-definitions.md, heuristic crossfire — kept [P]-free)
- T003 ∥ T002 (Setup measurements, distinct outputs)
- T017 (skills mirror write) after its four source rows land; T023 (shared mirror write) after T020/T021
- T029 ∥ T030 ∥ T031 (Polish, different files)

---

## Parallel Example: User Story 1

```bash
# After Phase 2 (T007 green):
Task: T010 "Rewrite agents.md teaching in templates/commands/agents.md"
Task: T011 "Rewrite SKILL.md :122/:127 in skills/create-agent/SKILL.md"
# then serially: T012 regen copies → T013 guard green + drill
```

---

## Implementation Strategy

### MVP First

**MVP scope**: US1 + US2 (both P1). Teaching-surface fixes without the render trigger (US1 alone) would teach a command that does not exist; seat instantiation without the trigger reaching the host surface (US2 minus Phase 2) is the status quo. US1+US2 together with Phase 2 form the independently valuable increment that closes the observed "only general-purpose" chain — the MVP covers Phase 1-4.

1. Complete Phase 1 (Setup: baseline + measurements)
2. Complete Phase 2 (Foundational: subcommand + key, red-first)
3. Complete Phase 3 (US1) → checkpoint: retired literals zero, guard green
4. Complete Phase 4 (US2) → checkpoint: seat instance + host surface demo passes
5. **STOP and VALIDATE** both P1 stories per their Independent Tests
6. Phase 5 (US3 docs) → Phase 6 (US4 guards aggregate) → Phase 7 (Polish)

### Incremental Delivery

Each phase boundary commit's criterion: name-level regression diff (comm -13) empty for the increment.

---

## Notes

- Green-point attributions ([green: ...] tags) partition the contract clauses across the claim rows — each clause claimed exactly once, claim order matches clause order per contract (contracts renumbered 2026-10-08 during generation to the `md-bold-closed` canonical clause form per `shared/definitions/contract-clause-definitions.md`, with clause ids ordered to match claim-row order for the green-cross-phase monotonicity rule; one claim-carrying row per test file for the green-path-divergence rule)
- Baseline number in T002 is the generation-time capture (2026-10-08: 49 failed / 2574 passed / 2 skipped in 58.52s, name list 49 entries); /speckit.implement re-captures per the never-cache rule
- Deferral discipline: no task is a natural [~] candidate; the only environment-dependent row would be a live Qoder IDE check, which the spec explicitly scoped out (verify-before-design satisfied via official docs at spec time)
- Quickstart scenario 1/2 examples are teaching-flow descriptions executed by an agent during /speckit.implement's manual QA, not shell one-liners
