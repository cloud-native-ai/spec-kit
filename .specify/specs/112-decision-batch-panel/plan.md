# Implementation Plan: Batch Decision Panel（批量决策面板）

**Branch**: `112-decision-batch-panel` | **Date**: 2026-11-27 | **Spec**: `.specify/specs/112-decision-batch-panel/requirements.md`
**Requirement → Feature**: `112-decision-batch-panel` → Feature 112 Batch Decision Panel（批量决策面板）
**Input**: Specification from `.specify/specs/112-decision-batch-panel/requirements.md` (45 FR / 10 SC; Assumptions A-1…A-25; 13 clarification rows), the 107 owner page `shared/definitions/decision-definitions.md`, and the adjacent owners named by pointer (confirmation gates, decision tension, closed-set claims, user-facing comprehension, script interface, memory engine, ID Register).

## Summary

Extend the existing decision-governance owner page (never a second owner, registry, store or schema) with the **batch decision capability**: a closed two-source roster of pending decision items, a `### PENDING —` item-block grammar, one complete information presentation per invocation, a recommended default that is the item's own declared default plus a deterministic grounding join over a closed prior-experience carrier set (or an explicit `no-evidence`), objection-only interaction where silence settles only eligible items in a completed interactive batch, recording through the existing carriers (one dated batch record in the existing knowledge store, 107 decision records carrying three conditional batch-family fields, register registration and status updates, `resolution` annotations), and a read-only deterministic replay from the recorded carriers alone. The delivery surface is one thin command `/speckit.decide` (`templates/commands/decide.md`), one internal skill `decide-batch`, and one stdlib engine `scripts/python/decision-batch.py` with closed actions `scan` / `record` / `replay`. `ai-autonomous` decisions never enter the panel; unattended runs may scan but never record acceptance; zero network, zero feedback-store write, zero automatic transmission, zero new runtime store root. The measurable first batch on this tree is 17 open register rows with zero authored blocks — presented `incomplete`, settling nothing; authoring the missing content is the producer/user obligation (A-16), never the panel's.

## Technical Context

**Language/Version**: Python >= 3.8, standard library only for the new engine; Markdown for the owner page, command, skill and docs
**Primary Dependencies**: none new — the engine consumes the CPython stdlib, the existing memory engine CLI (`scripts/python/memory-utils.py --action record --scope knowledge`), the existing decision checker surface (`scripts/python/validate-decisions.py`), and the existing mirror/copy/test toolchain
**Storage**: no new store — the batch record is one dated entry in the existing `.specify/knowledge/` store written through the memory engine; decision records live inside the batch record (producer P-13 carrier); `.specify/register.md` stays the sole id index; no `.specify/.gitignore` change and no runtime-store-layout change
**Testing**: `bash scripts/bash/run-tests.sh` (pytest, parallel default, `SPECKIT_PYTHON` ladder, targeted selection forwarded); red-first fixtures under `tests/fixtures/decision-batch/`. This stage is documentation-only and the worktree carries no pytest interpreter, so the test entry is not run — recorded with the measured runner error (research M-14)
**Target Platform**: framework repository (framework sources + client-runtime mirrors); downstream projects receive the command, skill, engine and owner page through the existing publish → install → `specify init` flow
**Project Type**: CLI / documentation framework — no application runtime, no scheduler, no UI
**Performance Goals**: N/A for service load; scan/record/replay are single-pass reads over text carriers; presentation must render every item with no truncation (FR-025); repeated scans are field-identical except the scan timestamp
**Constraints**: owner-page extension only (FR-001…FR-005); no second registry/store/schema; zero network, zero feedback write, zero automatic transmission; no alignment with ai-harness 091; `.specify/instructions.md` § Decision Items (1,276 B of a 1,500 B cap) is not edited; gate-scanner neutrality against the measured baseline (30 gates / 0 violations); script-interface compliance for the new engine; frozen command/skill baseline moves 32 → 33 and 60 → 61 in the same change; probe census pin moves with the new skill's probe object
**Scale/Scope**: 1 owner-page extension (new batch face + vocabulary 9 → 17 + P-13 + 3 conditional fields + batch M/B rows), 1 command template, 1 internal skill (+ probe object + compiled wrap-up), 1 stdlib engine, 1 command doc, 1 framework-map row update, 6 design contracts, 10 guard/fixture surfaces, 7 execution premises, 1 inherited-blockers disposition

**Execution record (concurrency)**: `requested=1`; `effective=not_evaluated`; `effective_reason=single-unit`. The stage's units were enumerated before the shape was chosen: research; `plan.md`; `data-model.md`; the six contracts; `quickstart.md`; `feature-ref.md`; the Feature Integration edits; the gate runs and the wrap-up records. The representable unit set has size 1 — the executor role forbids dispatching other agents, and the driver partitions the plan as one serial work package (checkpoint 02: `Next (plan): single-unit`). The reason code `single-unit` is read from `shared/declarations/facts/serial-reason.yaml` (the representable unit set has size 0 or 1). No dispatch intervals exist, so `effective` is `not_evaluated`, never a number.

## Plan Assumptions

Plan-stage adjudications under the unattended assignment (not user questions):

- **PA1 — Same-author scoring fallback**: the Constitution Check and the Post-Generation Quality Gate would ideally be delegated to fresh-context read-only subagents, but this executor carries no dispatch capability and the role forbids dispatching. Both are a disclosed direct self-read against the landed artifacts (the objective-analysis gate's fallback path), recorded here rather than silently claimed as independent review.
- **PA2 — Qualification precedence**: the spec's closed presentation states are made deterministic by the precedence `incomplete` → `source-conflict` → `no-default` → `irreversible-default` → `prior-decision-conflict` → `eligible` (research D-4). No new state is invented; every candidate gets exactly one classification and every reason is named.
- **PA3 — Explicit settlement boundary**: alternatives for ineligible items are accepted where a valid 107 record can be formed (`no-default`, `irreversible-default`, `source-conflict`, `prior-decision-conflict`); an `incomplete` item accepts an alternative only when its option set is grammatically complete and `subject`/`context` resolve — otherwise the engine refuses with a named reason (research D-9). This is the only reading consistent with FR-033's unchanged record grammar and the spec's edge case.
- **PA4 — Batch-record identity and create-only semantics**: batch records are recognised in the knowledge store by the title prefix `decision-batch-<batch_id>`; the memory engine's knowledge scope is upsert-by-slug, so create-only is enforced by the batch engine pre-checking the target path and refusing a duplicate batch id (research D-2/M-6). An entry matching the prefix but unparseable is a named refusal, never a guess.
- **PA5 — Docs-only stage**: no executable artifact changes at this stage; the applicable deterministic gates are the validators and the workspace guard. The test entry is additionally unavailable in this worktree (no pytest interpreter) — the measured runner error is recorded.
- **PA6 — Stale reading correction**: the Feature 112 detail still quotes the requirements-stage "eight open rows"; the clarify ruling (A-21) corrected it to the predicate-derived 17. The Feature Integration edit corrects the detail and discloses the correction.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/constitution.md` v1.20.0 — one row per principle in document order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every design surface traces to FRs: owner extension ← FR-001…FR-005; roster/qualification ← FR-006…FR-013; aggregation/completeness ← FR-014…FR-018; presentation/grounding ← FR-019…FR-025; interaction ← FR-026…FR-031; recording ← FR-032…FR-038; entry/boundaries ← FR-039…FR-045 (contracts' traceability tables and § Project Structure) |
| II | Feature-Centric Development | ✅ Pass | Feature 112 advances Draft → Planned in both carriers with its detail refreshed (Feature Integration); no other feature changes status |
| III | Intent-Driven Development | ✅ Pass | What/why precede how: `research.md` records measured carriers and resolved design points; contracts state normative interfaces; PA1…PA6 disclose adjudications |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Red-first guard obligations are named per contract (reverse samples); fixtures live under `tests/fixtures/decision-batch/`; tasks will order tests before implementation; every guarantee names the test that pins it |
| V | AI Agent Integration Standards | ✅ Pass | No provider/config/tier change; the new command fans out to the four existing per-tool trees through the canonical generator |
| VI | Continuous Quality & Observability | ✅ Pass | Refusals over half-batches; drift and pointer failures are surfaced, never skipped; no `.bak` copies; guards are designed to go red on doctored subjects |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Plan set produced from the validated spec; Feature Index updated; status ceiling `Planned` respected (never `Implemented`) |
| VIII | Code as the Single Source of Truth | ✅ Pass | Measurements taken from engines/code: validator field closure (research M-5), memory-engine upsert semantics (M-6), frozen baselines (M-3), gate-scan baseline (M-7) |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | One on-demand stdlib engine; no scheduler, daemon, UI, dashboard or notification surface; no second store or schema (§ Out of Scope honored) |
| X | Documentation Naming & Location Conventions | ✅ Pass | `docs/reference/commands/decide.md` follows the one-file-per-command lowercase convention; no reserved filename reused |
| XI | Dogfooding (Self-Application) | ✅ Pass | Two hats named: edits land in framework sources (`shared/`, `templates/`, `skills/`, `scripts/`) and ride mirror/init; the feature detail/detail correction is the client-runtime side; mechanism fixes land in the owner page and probe registry, not instance patches |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | Reuses the memory engine write surface, the decision checker, the mirror/copy generators, the single test entry and the probe compile pipeline; the engine MUST NOT reimplement the memory frontmatter format |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | Strengthens Task Understanding (complete, comparable presentation) and Reliable Delivery (append-only batch records, replay); claims rest on measured evidence in `research.md`; no score or tracking surface added |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | Rules live only in the extended owner page; command, skill, engine and docs reach it by pointer; the three batch-family fields join the existing conditional layer instead of a second schema; register remains the sole id index |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | The presentation carries the batch-level context floor (why now, silence meaning, objection method, pending reasons, completeness disclosure) and keeps internal identifiers out of the user-facing body (contract presentation C-203/C-204; B-08 review surface) |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | Unreadable carriers refuse the batch; source drift between scan and record refuses with the diff and zero writes; unparseable batch-prefixed entries are refusals — no silent repair path exists |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | No new top-level or runtime directory; `tests/fixtures/decision-batch/` follows the declared per-feature fixtures convention; the batch record reuses `.specify/knowledge/` |
| XVIII | Grounded Naming | ✅ Pass | `/speckit.decide` follows the single-word command family; `decide-batch` follows the `<verb>-<object>` skill siblings; field names and states are the spec's Shared Strings, not improvised |
| XIX | Self-Explanatory Structure (不言自明) | ✅ Pass | Names carry meaning: `decision-batch-<batch_id>` titles identify batch records; `resolution`, `batch_disposition` and `recommendation_grounding` state their content; ids and paths are projections of the owner page |
| XX | Efficient Test Execution (Concurrent by Default) | ✅ Pass | New tests run through the single entry with the runner's default parallel form and a targeted selection; no new full-suite step and no second runner |
| XXI | Script Interface Contract (Declared, Zero-Side-Effect) | ✅ Pass | The new engine answers `-h`/`--help`/`--version`, rejects undeclared options non-zero, declares read-only/write surfaces and exit codes (record-replay C-508, completeness C-608) |
| XXII | Re-Anchoring (不忘初心 · 温故而知新) | ✅ Pass | The stage anchor and rules were reloaded before each core step; verdicts recorded `on-track` in the stage evidence |
| XXIII | AI-Generated Code Review Policy | ✅ Pass | The change is AI-written, so the AI review flow applies at the review stage (direct merge to trunk + AI review of merged history); this plan adds no review ledger |

**Gates Status**: ✅ All 23 gates pass — no Fail or Partial row; Complexity Tracking is N/A.

**Re-check after Phase 1**: 2026-11-27 — refreshed against the landed design artifacts (`data-model.md`, `contracts/` ×6, `quickstart.md`, `feature-ref.md`, § Phase 1 summary). No row changed status; the design artifacts carry the evidence named above.

## Decision Tensions

*Owner of the record shape, the admissibility criteria, the rejection forms and the load-bearing threshold: `.specify/shared/guidelines/decision-tension.md` — one pointer, read from the repository root; a plan artifact lives under `.specify/specs/<key>/`, so a plan-directory-relative link would resolve to a path that does not exist. This section lists the field names and points at that file — it MUST NOT restate the criteria table, the rejection list or the threshold table.*

Fields: `decision`, `antithesis`, `binding_constraints` (with `pole_a` and `pole_b`), `discriminating_evidence`, `expected_sacrifice`, `revision_trigger`; record identifier `tension_id` (`T-NNN`).

N/A

本计划无承重决策：下列四类触发均不成立，逐类说明如下。

- 不可逆：本计划的全部改动都是版本控制中的增量文本、只读引擎动作与单写记录路径；没有数据迁移、没有既有记录 schema 变更，回滚即 revert 本特性提交，运行期只追加新记录。
- 跨团队：本计划没有新增他人依赖的契约变更；所有者页扩展、批次族字段与 P-13 生产者行已在 requirements A-2/A-12 裁定并固定在 FR-001…FR-045，本计划只把它们落成设计条款，未另造接口。
- 高爆炸半径：批次机制按需运行，写入面限于本批次自己的记录、具名 register 行与来源状态单元格；一次失败只影响本次调用，不触及他批记录或运行时服务。
- 与宪法原则相关：宪法检查逐条核对 23 条原则均为 Pass，本计划不在两种宪法读法之间取舍，也不修改任何 MUST 条款。

The requirements-stage load-bearing decision on silence semantics (A-10, recorded in the owner's decision-tension shape) is inherited by pointer — its six fields live in `requirements.md`, are not restated here, and its `expected_sacrifice` measurement source is SC-005 in that file.

## Project Structure

### Documentation (this spec)

```text
.specify/specs/112-decision-batch-panel/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (standalone: measured baselines + resolved design points)
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (6 contracts)
├── feature-ref.md       # Phase 1 output
├── test-evidence/       # Gate captures, baselines and stage records
├── tasks.md             # Phase 2 output (/speckit.tasks — NOT created by /speckit.plan)
└── verification.md      # Implementation output (/speckit.implement command)
```

### Source Code (repository root)

```text
shared/definitions/decision-definitions.md      # 107 owner page — additive batch extension (FR-001…FR-005, FR-011, FR-015…FR-018, FR-032…FR-038)
shared/definitions/framework-map.md             # decision-governance row: P-13, batch capability, consumers
shared/definitions/probe-definitions.md         # probe object + bindings for the new skill's wrap-up
templates/commands/decide.md                    # new thin entry /speckit.decide (FR-039)
skills/internal/decide-batch/SKILL.md           # new internal skill: interaction + presentation relay (FR-039)
scripts/python/decision-batch.py                # new deterministic engine: scan / record / replay (FR-039)
scripts/python/validate-decisions.py            # extend field closure + batch-family rule (RS-005)
docs/reference/commands/decide.md               # command reference: entry, actions, exit semantics (FR-043)

tests/fixtures/decision-batch/                  # red-first fixtures + reverse samples (FR-044)
tests/unit/test_decision_batch_engine.py        # engine unit tests: scan/record/replay, refusals, zero-write
tests/contract/test_decision_batch_contract.py  # owner extension / pointer-only / distribution guards
tests/contract/test_decision_governance_guards.py  # GUARD_ROSTER gains the batch M rows (parity)
tests/contract/test_migration_distribution.py   # frozen baseline 32 → 33 commands, 60 → 61 skills
tests/contract/test_probe_nonentity_catalog.py  # probe census pin follows the new skill object
```

**Structure Decision**: extends the existing framework layering (definitions → templates/commands → skills → scripts → tests) rather than creating a new layer. The owner page is extended in place; the command fans out through the canonical per-tool generator; the skill and engine are new files in their existing trees; no new top-level directory, runtime directory or store root is added. The only new non-spec directory is the per-feature fixture directory `tests/fixtures/decision-batch/`, following the declared `tests/fixtures/` convention.

### Mirror Obligations

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `shared/definitions/decision-definitions.md` | `.specify/shared/definitions/decision-definitions.md` | `python3 scripts/python/sync-mirrors.py --check`: no NEW drift vs the pre-edit baseline (rc 0 measured 2026-11-27, research M-10) |
| `shared/definitions/framework-map.md`, `shared/definitions/probe-definitions.md` | each file's same relative path under `.specify/shared/` | same mirror check — no NEW drift on the pairs touched here |
| `skills/internal/decide-batch/SKILL.md` (new) | `.specify/skills/internal/decide-batch/SKILL.md` | same mirror check — no NEW drift; the wrap-up block is compiled by `probe-utils.py --action compile-embeds`, never hand-written |
| `scripts/python/decision-batch.py` (new) | `.specify/scripts/python/decision-batch.py` | same mirror check — no NEW drift; the engine answers `--help` / `--version` from both copies |
| `templates/commands/decide.md` (new) | `.claude/commands/speckit.decide.md`; `.github/prompts/speckit.decide.prompt.md`; `.qoder/commands/speckit.decide.md`; `.opencode/command/speckit.decide.md` — via `regen-command-copies.py`; NO `.specify/templates/commands/` mirror (retired) | `regen-command-copies.py --check` rc 0 at baseline (M-10) and rc 0 after regeneration; regenerated copies contain the edit |
| `docs/reference/commands/decide.md` (new) | none — `docs/` is this project's development documentation, never shipped | no mirror duty |
| test files (new/changed under `tests/`) | none — tests are not distributed | no mirror duty |

## Execution Premises

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | The existing CPython ≥3.8 stdlib stack (engine imports nothing third-party) and the single test entry can carry the new engine and its guards | `pyproject.toml` `requires-python`; `scripts/bash/run-tests.sh:63-74` (interpreter ladder); engine design uses stdlib only (research D-1) | verified | — |
| EP-002 | The existing memory engine's `record` action can carry one dated batch record per batch in the knowledge store with compliant frontmatter (one file per entry, atomic write, stable slug) and its write surface is callable as documented | `scripts/python/memory-utils.py:382-440`; `--action list --scope knowledge --format json` reading (research M-6) | verified | — |
| EP-003 | The existing decision checker can host the batch-family field closure and a batch rule, and it never judges a `### PENDING —` block as a record (record detection starts at `### D-NNN` headings) | `scripts/python/validate-decisions.py:95-140,455-485`; record heading detection (research M-5) | verified | — |
| EP-004 | The mirror and per-tool copy toolchain projects the new files and regenerates copies with no new drift; the generator discovers `templates/commands/decide.md` without a hardcoded list | `MIRROR_PAIRS`; `regen-command-copies.py` source scan; both checks rc 0 at baseline (research M-10) | verified | — |
| EP-005 | The ID Register and the register table accept a new batch-id family, grouped decision-id rows and status-cell updates, and a missing register can be created from the existing header form before registration | `.specify/register.md` header (four-column table, hand-maintained); `.specify/instructions.md` § ID Register | verified | — |
| EP-006 | The frozen command/skill baselines and the probe census can be extended in the same change as the new command, skill and probe object | `tests/contract/test_migration_distribution.py:125-156`; `tests/contract/test_probe_nonentity_catalog.py:105-117` (research M-3/M-11) | verified | — |
| EP-007 | The 17 currently-open register rows resolve to complete pending-item blocks and can be batch-settled as-is | Predicate measurement: 17 open rows; authored `### PENDING —` blocks in the four scan roots: 0 (research M-1/M-2) | falsified | fallback |

EP-007 is a known-bad fact recorded with its decision (`fallback`): the first batch presents the 17 rows as `incomplete` with named missing elements and settles none; authoring the missing content is the producer/user obligation (A-16), and the panel never invents options, defaults or evidence.

## Inherited Blockers

**Dependency artifacts (declared, never implied)** — the checker reads only the paths in this block:
- `107`: `.specify/features/107-decision-governance.md`, `.specify/specs/107-decision-governance/verification.md`

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|
| 1 | — | not-applicable | — | — | The declared dependency (Feature 107) carries no `## Deferred` section in its detail and no `blocked` / `deferred` / `partial` status row in its verification (`closure_final_path=pass 7 / blocked 0 / deferred 0 / partial 0`); the extraction set is empty, so there is nothing to disposition. |

Feature 055 (conflict-free stores) owns the memory engine consumed as a signed-contract interface (RS-004); it is excluded from the blocker source set because its detail carries no `## Deferred` section and the plan inherits no blocked/deferred/partial row from it.

## Complexity Tracking

N/A — no Constitution Check row is Fail or Partial.

## Phase 1: Design Artifacts Summary

Filled after the artifacts landed (counts read from the written files):

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`](./data-model.md) | 13 entities, 22 invariants, 5 state domains |
| Contracts | [`contracts/`](./contracts/) | 6 files: `source-roster.contract.md`, `presentation.contract.md`, `default-derivation.contract.md`, `objection-reply.contract.md`, `record-replay.contract.md`, `completeness-refusal.contract.md` |
| Quickstart | [`quickstart.md`](./quickstart.md) | 7 scenarios (source inspection, scan, objection+record, replay, refusal/nothing-pending, recorded-batch inspection, maintainer guards) |
| Feature reference | [`feature-ref.md`](./feature-ref.md) | Feature 112 binding, delivery surfaces, mirror map, requirement→contract map |
| Research | [`research.md`](./research.md) | 14 baseline measurements + 12 resolved design points |