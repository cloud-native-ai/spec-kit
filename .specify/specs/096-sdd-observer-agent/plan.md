# Implementation Plan: SDD Observer Agent（sdd-observer 专用观察者与线级 journal）

**Branch**: `096-sdd-observer-agent` | **Date**: 2026-11-10 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `096-sdd-observer-agent` → Feature 096 SDD 专用观察者与线级观察记录（sdd-observer）
**Input**: Specification from `.specify/specs/096-sdd-observer-agent/requirements.md` (23 FR / 7 SC; clarify settled with 6 pre-plan rulings and 13 assumptions)

## Summary

Every driver-driven SDD line gains one third-party observer that records what happened, without becoming a participant:

```text
definition   agents/sdd-observer.agent.md  (Agent Template; observation-only role face)          owner: this feature
lifecycle    driver U0 switch -> startup before first U2 -> bounded executions -> line-terminal   owner: SKILL.md § SDD Observer
record       <spec-dir>/journal.md, one file per line, nine-field rows, closed event classes      owner: shared/declarations/facts/journal-format.yaml
writer       scripts/python/journal-utils.py  (deterministic projection + checker + flock)        owner: this feature
edge         existing spine / quartet / checkpoints / git / triplet                               owner: unchanged carriers
```

The feature adds **one agent template, one declaration fact, one stdlib engine, one driver reference and one driver SKILL section**, plus their guards and fixtures. It creates no command, no scheduler, no daemon, no second registry, no second state store, and it changes neither `status-digest.py` nor any stage command. The observer's failure is a recorded, disclosed non-observation — never a gate.

## Technical Context

**Language/Version**: Markdown for the template, driver section and reference; Python `>=3.8` stdlib-only for the journal engine and tests; measured interpreter CPython 3.11.11, `git version 2.43.5`.
**Primary Dependencies**: none new — stdlib only (`argparse`, `fcntl`, `pathlib`, `datetime`, `subprocess` for `git`); the declaration read entry `scripts/python/declaration_reader.py`; the script-interface helper `scripts/python/script_interface_cli.py`; pytest for tests.
**Storage**: the only new persistent artifact is `journal.md` (STR-001) under the line's spec directory, append-only, one file per line (clarify A5). No index, ledger, database or second store.
**Testing**: `bash scripts/bash/run-tests.sh` (targeted selection at plan/implement; two full-run budget slots per the driver). New modules: `test_sdd_observer_agent.py`, `test_sdd_observer_lifecycle.py`, `test_journal_engine.py`; fixture directory `tests/fixtures/sdd-observer/`; two deliberate pin updates in existing modules.
**Target Platform**: any host with CPython `>=3.8` and `git`; the fork/subprocess carriers already required by the driver; no network.
**Project Type**: SDD framework (agents + declarations + engine + skill references + tests), self-hosting repository. Two hats: rows 1–10 of `feature-ref.md` are framework-source edits reaching `.specify/` through `sync-mirrors.py` / `specify render-agents`; the observer instance and the journal are client-project runtime artifacts produced per line.
**Performance Goals**: an observer refresh pass is a bounded read of a few small files plus one append; a no-change pass appends nothing (idempotent identity). The observer never blocks a stage; its absence costs the line nothing.
**Constraints**: zero new commands/skills/registries/daemons (FR-006, FR-017); the observer writes only the journal and its own execution artifacts (FR-016); journal rows carry no evaluation/suggestion/causal/severity field (FR-013); no change to `status-digest.py`, reporting-obligations, stage sequence or `STAGE_ARTIFACTS` (FR-017, A12); one live observer execution per line (FR-007).
**Scale/Scope**: 23 FR / 7 SC; 19 delivery rows in `feature-ref.md`; 5 contract pages (58 clauses); 8 quickstart scenarios (S-0…S-7); 10 data-model entities and 20 validation rules; 4 work packages (19 items).
**Stage execution record (concurrency obligation)**: `requested=24` (driver's U0 reading in the state spine), `effective=1`, `effective_reason=mechanism-not-yet-landed` — this stage execution's brief carries no dispatch capability and the stage executor is a leaf under the anti-nesting obligation; the enumerated unit set is § Work Packages below. Replayable partition rule: `decompose-plan-v1`.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Rendered by enumerating every `### <numeral>. <name>` heading of `.specify/constitution.md` (v1.19.1) in file order; annotations carried verbatim (Principle VII is NON-NEGOTIABLE).

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every contract clause cites an FR; the § FR → Contract map covers FR-001…FR-023 with no orphan. |
| II | Feature-Centric Development | ✅ Pass | This plan creates Feature 096's row and detail and lands `Planned` only (§ Feature Integration); no existing feature is merged or split. |
| III | Intent-Driven Development | ✅ Pass | The user's verbatim goal (third-party observation, objective record, no evaluation) is the § Summary shape and every clarify ruling; T-001…T-005 record the accepted trade-offs. |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Every SC names its module and red leg (`observer-verification.contract.md` C-01…C-07); the pre-edit baselines are measured (25 + 2 passed, mirror exit 0) so the implement criterion is *no NEW failure*. |
| V | AI Agent Integration Standards | ✅ Pass | The new agent template uses the neutral frontmatter vocabulary and rides `sync-mirrors.py` + `specify render-agents`; no tool-specific field is hand-written. |
| VI | Continuous Quality & Observability | ✅ Pass | The journal is the observability surface; every row is a carrier projection with a resolvable pointer, and an unreadable carrier is recorded, never fabricated (journal-engine C-04). |
| VII | Specification-Plan-Task-Implementation Workflow (NON-NEGOTIABLE) | ✅ Pass | requirements → clarify (U4 pass) → this plan → tasks/checklist/analyze/implement/review; feature status advances at most to `Planned`. Feature reuse-first: no existing feature owns an observer/journal (searched: 064 concurrency, 074 goal/team unification, 085 temporary goal/team — none covers it). |
| VIII | Code as the Single Source of Truth | ✅ Pass | Phase 0 measured the real formats (runner envelopes, label pattern, declaration schema, pinned enumerations) instead of assuming them; § Phase 0 cites each file/line. |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | One stdlib engine + declarations + text; no scheduler, daemon, second registry, second state store or new command (FR-006, T-003 antithesis rejected). |
| X | Documentation Naming & Location Conventions | ✅ Pass | `journal.md` is a user-mandated name (STR-001); the reference follows the skill's `references/<topic>.md` convention; fixtures live under `tests/fixtures/<feature>/`; no new top-level directory. |
| XI | Dogfooding (Self-Application) | ✅ Pass | Two hats named in § Technical Context; the fix lands in framework sources (`agents/`, `shared/`, `scripts/`, `skills/external/`) and reaches `.specify/` through the generators; the instance/journal are client-runtime rows. |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | Reuses `declaration_reader.py`, `script_interface_cli.py`, `sync-mirrors.py`, `specify render-agents`, `run-tests.sh`; the engine is the only new script and is the feature's deliverable, not a re-improvisation. |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | Targets **Learning Capture / Change Validation**: an independent, objective, evidence-linked record of what happened, produced without weakening delivery. |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | Spellings in `journal-format.yaml`; stage names in `driver-stage-sequence.yaml`; record-section shape in SKILL.md § SDD Observer; label convention in `subagent-definitions.md`; the plan restates none of them (R-05, R-07). |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | The quickstart defines journal / observer / gap at first use, names the exact commands, and carries per-example premises; the driver section is written for a reader who did not run the line. |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | § Phase 0 records the measured constraints (R-01/R-04/R-05/R-09) that would otherwise break pinned guards; the observer's own fast-fail duty is injected at dispatch (observer-lifecycle C-11). |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | The only new directory is `tests/fixtures/sdd-observer/` (existing fixture convention); fixture temp roots use `tmp_path` (sanctioned); `test-evidence/` already exists. |
| XVIII | Grounded Naming | ✅ Pass | `journal.md` / `sdd-observer` / `observer-gap` are the user's own words (STR-001…003); `journal-utils.py` follows the `memory-utils.py` / `history-utils.py` siblings; `observer-lifecycle.md` follows the reference naming. |
| XIX | Self-Explanatory Structure (不言自明) | ✅ Pass | Execution class ⇒ § Document Structure is not produced (template: expression-class only). The one user-visible addition is the journal, whose columns name exactly what a reader needs. |
| XX | Efficient Test Execution (Concurrent by Default) | ✅ Pass | New tests are pure-read or `tmp_path`-isolated and xdist-safe; the runner stays the only entry (observer-verification C-10); no serial-only resource is introduced. |
| XXI | Script Interface Contract (Declared, Zero-Side-Effect) | ✅ Pass | The new engine passes `-h`/`--help`/`--version` through `script_interface_cli.guard_argv` before any action and rejects undeclared options (journal-engine C-02, C-10). |
| XXII | Re-Anchoring (不忘初心 · 温故而知新) | ✅ Pass | The plan re-read the rules at each section (unattended / no approval / spine-before-action / fast-fail / gates / budget); the stage spine receives the plan record; no approval request is emitted. |

**Gates Status**: ✅ All 22 principles pass; no `Fail` and no `Partial` ⇒ § Complexity Tracking records `N/A`.

**Re-check after Phase 1** (2026-11-10, after `research.md` / `data-model.md` / `contracts/` / `quickstart.md` / `feature-ref.md` landed): no row moved. Row IV gained the measured pre-edit baseline; row XIV gained the explicit owner split in the fact file (R-05); row XIX is unchanged because the section remains legitimately absent for an execution-class line.

## Decision Tensions

*Owner of the record shape, the admissibility criteria, the rejection forms and the load-bearing threshold: `.specify/shared/guidelines/decision-tension.md` — read from the repository root. This section lists the field names and points at that file; it does not restate the criteria table, the rejection list or the threshold table.*

Five decisions clear the owner's load-bearing threshold (user-mandated shape, cross-cutting blast radius, a documented prohibition, or a constitution MUST). `T-004` touches the non-blocking duty the user stated explicitly.

### T-001 — Journal is one append-only file per line, not per-entry files

- **decision**: `.specify/specs/<key>/journal.md` (STR-001), one file per line, rows appended by the engine; concurrency safety is a single live writer plus a non-blocking flock on the file itself.
- **antithesis**: store one file per observation under `.specify/specs/<key>/journal/` (aligns with the project's "records are per-entry files" default and lets two branches add different paths).
- **binding_constraints**:
  - pole_a: the user named `journal.md` as the artifact (STR-001); clarify A5 ranks the user instruction above the project default.
  - pole_b: Concurrent Development Safety exists because multi-writer branches share files; the same spec directory written by two lines is not a supported state (line registry serializes same-line work).
- **discriminating_evidence**: the dual-line fixture — two lines, two spec dirs, two journals, zero shared path; and the same-journal second writer exits `3`. Binary: any shared path (fail) / none (pass).
- **expected_sacrifice**: SC-005 Source ↓ the isolation criterion can assert separate paths and identities, but cannot assert a merge order for two writers of one journal, because that state is excluded by the single-file decision.
- **revision_trigger**: ≥2 incidents where two concurrent writers legitimately need the same journal (e.g. two lines on one spec) → reopen and split into per-entry files with a generated index.

### T-002 — Objectivity by construction, not by semantic detection

- **decision**: entries are produced only by the deterministic engine from closed carriers; the structure has no field able to carry evaluation, suggestion, causal inference, severity or recommendation; the checker validates structure, order and pointers.
- **antithesis**: let the observer agent write prose entries and run a language-based evaluative-phrase detector over them.
- **binding_constraints**:
  - pole_a: SC-004 requires a machine-decidable verdict with reproducible outcomes (constitution XV's reproducibility logic applied to structure).
  - pole_b: A6 records that a semantic detector is a second judgment surface with unpredictable false positives/negatives, and no artifact can make its verdict reproducible.
- **discriminating_evidence**: engine output passes `check`; three tamper fixtures (extra key, unknown event, free narrative) each turn it red; the template carries the verbatim prohibition. Binary per fixture.
- **expected_sacrifice**: SC-004 Source ↓ the objectivity verdict is structural only: a fact recorded solely in the driver's reasoning or a stage prompt body stays permanently unrecordable, so the journal under-records rather than over-records.
- **revision_trigger**: ≥2 incidents where a genuinely needed fact class has a machine carrier that the engine cannot project → extend the carrier map and event set, never add a free-text field.

### T-003 — Bounded external executions restarted at stage boundaries, not a resident process

- **decision**: the observer runs as bounded Agent Executions on the existing fork/subprocess carriers, window bounded by the dispatch turn budget and stage deadline, restarted at stage boundaries; one live execution per line.
- **antithesis**: a single long-lived observer process per line that watches the whole run.
- **binding_constraints**:
  - pole_a: `reporting-obligations.md` § 十一 prohibits schedulers, timer services and daemons; constitution IX rejects new runtime machinery.
  - pole_b: FR-007 requires at most one live execution and bounded windows; the only available clock is the existing dispatch budget/deadline, so a resident process would need a new timer.
- **discriminating_evidence**: kill-mid-run fixture — the line reaches its terminal stage, the restart appends, and exactly one `observer-gap` names the window; no process survives the line. Binary.
- **expected_sacrifice**: SC-007 Source ↓ observation is not continuous; every restart leaves an explicitly named gap, so coverage is judged as "each stage started-or-gap-named" rather than as continuous watching.
- **revision_trigger**: if healthy lines routinely carry gaps for more than half their stages (≥2 measured lines) → revisit the window sizing inside the existing budget, still without a daemon.

### T-004 — Non-blocking: observer state is disclosure, never a gate

- **decision**: observer existence, absence, health and journal content never gate any stage advance, checkpoint, review or merge; failures are recorded in the spine record section and disclosed in the existing U6 close-out report.
- **antithesis**: make observer liveness a stage gate (guarantees complete journals).
- **binding_constraints**:
  - pole_a: FR-020 and the user's own statement — a non-delivering role must not hold the delivery line.
  - pole_b: SC-003's red leg requires that a stage gate depending on the observer makes a test red; the property must be provable, not incidental.
- **discriminating_evidence**: two failure fixtures (start failure, mid-run kill) reach terminal; a structural predicate over the driver text rejects a doctored gate sentence. Binary per fixture.
- **expected_sacrifice**: SC-003 Source ↓ a line may close with an incomplete journal; the only remaining obligation is the spine record plus the U6 disclosure, because no gate may depend on the observer.
- **revision_trigger**: a user-facing compliance need for "journal required" → model it as an explicit entry switch value (a later feature's decision), never as the default; reopening requires revisiting FR-020.

### T-005 — Visibility rides the existing supervision projection; zero digest change

- **decision**: observer executions appear through the existing `--sub-flow <label>=<triplet-dir>` supervision projection and the existing master-reporting duty; `status-digest.py` and its field set are untouched.
- **antithesis**: add an observer-specific row/section/field to the status digest so an operator can see observation health at a glance.
- **binding_constraints**:
  - pole_a: SC-006 requires zero new fields, rows or sections in the digest and the observer only in the existing dispatched-agent semantics.
  - pole_b: FR-017 forbids a second state surface or reporting channel.
- **discriminating_evidence**: digest field-set baseline captured before the first implementation commit vs the post-implementation reading — empty delta; plus a token scan showing `status-digest.py` carries no observer/journal token. Binary.
- **expected_sacrifice**: SC-006 Source ↓ a supervising reader distinguishes the observer from stage sub-flows only by its label, and journal content stays reachable only through the journal file.
- **revision_trigger**: if operators repeatedly misread the observer sub-flow as a stage, add label interpretation to the driver docs — not a digest field.

## Project Structure

### Documentation (this spec)

```text
.specify/specs/096-sdd-observer-agent/
├── plan.md              # This file
├── research.md          # Phase 0 — R-01…R-14 measurement record
├── data-model.md        # Phase 1 — 10 entities (E-1…E-10), 20 validation rules (V-1…V-20)
├── quickstart.md        # Phase 1 — 8 scenarios (S-0…S-7)
├── contracts/           # Phase 1 — 5 pages, 58 clauses
│   ├── observer-role.contract.md          # C-01…C-10
│   ├── observer-lifecycle.contract.md     # C-01…C-12
│   ├── journal-format.contract.md         # C-01…C-13
│   ├── journal-engine.contract.md         # C-01…C-13
│   └── observer-verification.contract.md  # C-01…C-10
├── feature-ref.md       # Phase 1 — delivery surface, FR/SC maps, overlap adjudication
├── verification.md      # Implement close — one SC status row per criterion + smoke record (GATE-4 input)
├── test-evidence/       # gate readings and baseline captures
└── tasks.md             # Phase 2 (/speckit.tasks — not created here)
```

### Source Code (repository root)

Only the directories this spec actually changes, one line each:

```text
agents/                                  # sdd-observer.agent.md — new Agent Template (shipped)
shared/declarations/facts/               # journal-format.yaml — new format owner (no contract.yaml change)
scripts/python/                          # journal-utils.py — new deterministic engine
skills/external/sdd-loop-driver/         # SKILL.md (new § SDD Observer) + references/observer-lifecycle.md (new) + references/stage-prompts.md (one pointer)
tests/contract/                          # three new guard modules + two deliberate pin updates
tests/fixtures/sdd-observer/             # new fixture directory: line builder, dual-line builder, failure builder
docs/reference/skills/                   # sdd-loop-driver.md — one additive observer section
.specify/                                # generated mirrors + rendered agent copies + feature registry row/detail
```

**Structure Decision**: the feature extends four existing framework trees by additive files/sections and adds exactly one engine and one fixture directory. It creates no new top-level directory and no new skill. The only new runtime path class is the per-line `journal.md`, which lives in the existing spec directory.

### Mirror Obligations

Baseline measured **before** this plan's edits: `sync-mirrors.py --check` → every pair `ok`, exit 0 (`test-evidence/plan-mirror-baseline.txt`). The criterion for every row is **no NEW drift**, never an absolute exit code.

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `agents/sdd-observer.agent.md` | `.specify/agents/templates/sdd-observer.agent.md`; plus four render copies `.claude/agents/sdd-observer.md`, `.qoder/agents/sdd-observer.agent.md`, `.github/agents/sdd-observer.agent.md`, `.opencode/agents/sdd-observer.md` via `specify render-agents --ai <t>` | `sync-mirrors.py --check` no NEW drift; the four copies exist and carry the fast-fail clause (test_fast_fail_discipline i10/i11) |
| `shared/declarations/facts/journal-format.yaml` | `.specify/shared/declarations/facts/journal-format.yaml` | `sync-mirrors.py --check`; `harness-triple-check.py --action verify` reads the fact |
| `scripts/python/journal-utils.py` | `.specify/scripts/python/journal-utils.py` (the `scripts/` pair is strict: no mirror-only files) | `sync-mirrors.py --check` no NEW drift; `script-interface-check.py` accepts the engine |
| `skills/external/sdd-loop-driver/SKILL.md` | `.specify/skills/sdd-loop-driver/SKILL.md` | `sync-mirrors.py --check`; `test_sdd_loop_driver_skill.py` mirror guard extended with the new reference |
| `skills/external/sdd-loop-driver/references/observer-lifecycle.md` | `.specify/skills/sdd-loop-driver/references/observer-lifecycle.md` | same; the new file must appear in `MIRROR_FILES` |
| `skills/external/sdd-loop-driver/references/stage-prompts.md` | `.specify/skills/sdd-loop-driver/references/stage-prompts.md` | same |

`docs/reference/skills/sdd-loop-driver.md` and `tests/` are not mirrored. No `probe-definitions.md` edit is planned, so no `compile-embeds` face changes.

## Execution Premises

Owner of this table's shape, the `Status` and `Decision` value domains and the invalid-row rule: `shared/workflow/acceptance-hardening.md` § Execution Premises — this table carries the column set and nothing else.

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | CPython `>=3.8` with stdlib filesystem, JSON and time capabilities runs the engine and the tests (RS-001) | `pyproject.toml` `requires-python`; measured CPython 3.11.11 (`test-evidence/plan-gates-baseline.txt`) | verified | — |
| EP-002 | `pytest` executes the new modules through `run-tests.sh` with zero new third-party imports (RS-002) | `pyproject.toml` pytest dependency; pre-edit baseline `25 passed` / `2 passed` through the runner (`test-evidence/plan-baseline-suites.txt`) | verified | — |
| EP-003 | The existing driver skill, agent template set and dispatch surfaces are present and editable, and their guards are green before the edit (RS-003) | `test_sdd_loop_driver_skill.py` 25 passed; `test_fast_fail_discipline.py -k "i10 or i11"` 2 passed; `sync-mirrors.py --check` exit 0 | verified | — |
| EP-004 | The host `git` supports the read forms the journal uses (`log --format`, `show --name-only`, `cat-file -e`, `rev-parse`) (RS-004) | `git version 2.43.5`; `git log -1 --format=…` and `git rev-parse --verify HEAD` ran successfully (`test-evidence/plan-baseline-suites.txt`) | verified | — |
| EP-005 | The per-tool agent render entry is available and needs no new mechanism | `specify render-agents --help` lists qoder, claude, copilot and opencode; `import specify_cli` succeeds | verified | — |
| EP-006 | The runner quartet envelopes have the formats the engine parses (R-02) | `stage-runner.sh` lines 222 / 223 / 350; `watch-model` thresholds untouched | verified | — |
| EP-007 | The supervised-label convention accepts `<line>--<run>--observer` with no new pattern | `status-digest.py` `SUPERVISION_LABEL_PATTERN` matches the three-segment form; verified by the engine's pattern check in the new test | verified | — |
| EP-008 | The feature registry has no 096 row, so this plan creates it | `.specify/features.md` 89 rows, highest 094; `.specify/features/096.md` absent (R-10) | verified | — |

## Inherited Blockers

**Dependency artifacts (declared, never implied)**: none — this feature consumes only existing framework owners and adds no dependency on another feature's open work. Feature 093 is `Blocked` on its own SC-006 (no real concurrent run of *its* feature), which is not a premise this plan rests on; this plan cites 093's declared concurrency vocabulary as existing owners, not as inherited deliverable rows.

Dependency set: none.

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|
| — | (none) | not-applicable | — | — | No dependency record with an open disposition is inherited. |

## Document Structure

Not produced: this is an `execution`-class line (`flow-class-check.py --action lookup --unit-id spec:096-sdd-observer-agent` → `flow_class: execution`, exit 0; `test-evidence/plan-gates-baseline.txt`), and the `## Document Structure` section is required of expression-class lines only. The section is omitted rather than left empty.

## Complexity Tracking

N/A — no ❌ Fail and no ⚠ Partial row in the Constitution Check. No table is carried.

## Phase 0: Research Review

Findings are recorded in [research.md](research.md) as R-01…R-14. The rulings that shaped the design:

1. **R-01 / R-07**: the driver SKILL.md has no observer carrier; the H2 set is pinned, so the new section is one deliberate pin update. The record-section shape is fixed in the new H2; the engine parses only two narrow state-spine prose grammars and never infers.
2. **R-02 / R-03**: stage life, verdict, anomaly, retry and dispatch events are projected from the runner quartet envelopes; the observer execution's visibility uses the existing triplet and the existing three-segment label convention.
3. **R-04**: the agent template must carry the byte-identical fast-fail clause and join the pinned preset enumeration (17 → 18); the four per-tool copies are render-produced.
4. **R-05**: the new declaration fact is read by file through `declaration_reader`; `contract.yaml` is deliberately untouched so the 094 C-86 closed-set pin stays valid.
5. **R-09**: `overlap-check` on a freshly copied plan template is polluted by template examples; the adjudication lives in `feature-ref.md` § Overlap adjudication, the raw reading stays in evidence.
6. **R-13**: the single-writer protocol uses `flock` on the journal itself — no lock file, so the observer's write surface stays exactly "journal + own execution artifacts".

## Phase 1: Design Artifacts Summary

Counts below were backfilled **after** the artifacts landed on disk.

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Research | [`research.md`](research.md) | `R-01`…`R-14` |
| Data model | [`data-model.md`](data-model.md) | 10 entities (`E-1`…`E-10`), 20 validation rules (`V-1`…`V-20`) |
| Contracts | [`contracts/`](contracts/) | 5 files, **58 clauses**: `observer-role` (C-01…C-10), `observer-lifecycle` (C-01…C-12), `journal-format` (C-01…C-13), `journal-engine` (C-01…C-13), `observer-verification` (C-01…C-10) |
| Quickstart | [`quickstart.md`](quickstart.md) | 8 scenarios (`S-0`…`S-7`) |
| Feature ref | [`feature-ref.md`](feature-ref.md) | 19 delivery rows, FR-001…FR-023 → contract map, SC-001…SC-007 → measurement map, overlap adjudication |

### Work Packages (input to `/speckit.tasks`; ≤16 items each)

| Package | Items | Write domain |
|---------|-------|--------------|
| `WP-1 journal-core` | 4 — journal-format.yaml; journal-utils.py; fixture builder; `test_journal_engine.py` | `shared/declarations/facts/`, `scripts/python/`, `tests/fixtures/sdd-observer/`, `tests/contract/test_journal_engine.py` |
| `WP-2 observer-definition` | 4 — agent template; FAST_FAIL preset-enumeration update; `test_sdd_observer_agent.py`; per-tool render | `agents/`, `tests/contract/test_fast_fail_discipline.py`, `tests/contract/test_sdd_observer_agent.py`, `.claude|.qoder|.github|.opencode agents/` |
| `WP-3 driver-lifecycle` | 6 — SKILL.md section; observer-lifecycle.md; stage-prompts.md pointer; SKILL pin update; `test_sdd_observer_lifecycle.py`; docs page | `skills/external/sdd-loop-driver/`, `tests/contract/test_sdd_loop_driver_skill.py`, `tests/contract/test_sdd_observer_lifecycle.py`, `docs/reference/skills/` |
| `WP-4 release-and-evidence` | 5 — feature registry row/detail; mirror sync; SC baseline capture; full runner pass; evidence record | `.specify/features.md`, `.specify/features/096.md`, generated mirrors, `test-evidence/` |

Dependencies: WP-1 and WP-2/write domains are pairwise disjoint and may run concurrently; WP-3's SKILL test references the reference file from WP-3 only; WP-4 integrates last. Each package stays far below the 16-item ceiling.

### Stage gate readings (run during this stage; verbatim record under `test-evidence/`)

| Command | Reading |
|---------|---------|
| `python3 scripts/python/validate-requirements.py .specify/specs/096-sdd-observer-agent/requirements.md` | `0 error(s), 0 warning(s)` (254 lines / 30 definitions / 3 shared strings) |
| `python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode plan --requirements .specify/specs/096-sdd-observer-agent/requirements.md` | `{"decision": "proceed", "fr_count": 23}` |
| `python3 .specify/skills/sdd-loop-driver/scripts/overlap-check.py --spec-dir .specify/specs/096-sdd-observer-agent --repo .` | `decision=overlap`, 55 relations — adjudicated in `feature-ref.md` (R-09) |
| `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --stage plan` | see § Plan-stage check below |
| `python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/096-sdd-observer-agent` | see `test-evidence/decision-tensions-plan.txt` |
| `bash scripts/bash/run-tests.sh tests/contract/test_sdd_loop_driver_skill.py -q` (pre-edit baseline) | `25 passed` |
| `bash scripts/bash/run-tests.sh tests/contract/test_fast_fail_discipline.py -q -k "i10 or i11"` (pre-edit baseline) | `2 passed` |
| `python3 scripts/python/sync-mirrors.py --check` (pre-edit baseline) | all pairs `ok`, exit 0 |

## Plan-stage check (filled by the gate run)

- `pre-analyze-check.py --stage plan`: recorded in `test-evidence/pre-analyze-plan.txt`; the post-artifact run is the authority, not this line.
- `validate-decision-tensions.py`: recorded in `test-evidence/decision-tensions-plan.txt`.
- Plan integrity: no residual upper-snake placeholder token; exactly one `# Implementation Plan:` heading; the Requirement → Feature stamp present.

## Risks and Mitigations

| Risk | Mitigation |
|------|-----------|
| Spine prose grammars drift and the engine silently stops seeing an event | the engine emits nothing for unparseable prose and the checker/test fixtures pin the grammars; driver text keeps them stable; any new grammar is a contract change |
| The observer's write surface grows (lock files, cursors) | flock on the journal itself; no cursor (journal is the cursor); test asserts the declared surface |
| The pinned enumerations (H2 list, preset set) drift in an unrelated change | the two pin updates in this feature are deliberate and commented; the guards fail loudly |
| The journal engine becomes a second judgment surface | structure-only validation; no semantic checks; tamper fixtures are structural |
| A line closes with no journal and nobody notices | spine `state=failed`/`disabled` + U6 close-out disclosure; SC-001's failure-path criterion names the gap |
