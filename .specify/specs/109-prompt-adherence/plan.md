# Implementation Plan: Prompt Adherence Evaluation（提示遵从度评价）— Spec Kit Port

**Branch**: `109-prompt-adherence` | **Date**: 2026-11-27 | **Spec**: `.specify/specs/109-prompt-adherence/requirements.md`
**Requirement → Feature**: `109-prompt-adherence` → Feature 109 Prompt Adherence Evaluation（提示遵从度评价）
**Input**: Specification from `.specify/specs/109-prompt-adherence/requirements.md` (30 FRs / 9 SCs; Assumptions and Clarifications of 2026-11-27), the closed behavior authority at `/storage/project/cloud-native-ai/ai-harness/.ah/specs/092-prompt-adherence/` (plan, research, data-model, five contract files, quickstart), and this tree's owners for integration.

## Summary

Land prompt adherence evaluation as one owner document plus one read-only engine over the stores that
already exist: a machine-parsed registry in `shared/definitions/prompt-adherence-definitions.md`
(premise chain, two-layer model, six-row signal catalog with declared attribution, six blind-spot
classes, the two-way coverage map, the reading contract's field meanings); exactly five closed-set
declaration facts (layers, strengths, signals, deviation classes, reading status); and the
deterministic stdlib engine `scripts/python/prompt-adherence.py` producing per-run and longitudinal
readings from the session (run-determination), exec-quant, feedback (including the `gate:` observation
family), evidence and probe registry stores. Every reading cites resolvable sources, discloses invalid
sources and duplicates, states its scope and window, carries a mandatory coverage section, and never
turns absence into adherence or breach. No new store, capture point, schema change, score, ranking,
network path, command or skill wrapper ships; the artifacts ride the existing publish → install → init
flow and are guarded by five new test files. The port adapts every source naming (`.ah` → `.specify`,
`/ah.*` → `/speckit.*`, `ai-harness init` → `specify init`, `ah.*` kind tokens → `speckit.*`) and
replaces the source-only `store_layout.py` read with the layout fact read through
`declaration_reader.py` (A-5).

## Technical Context

**Language/Version**: Python >= 3.8, standard library only for the new engine; Markdown + the YAML declaration subset for the owner document and facts
**Primary Dependencies**: none new — the engine imports the existing engines' read paths in process (`measure.py` precedent): `run-determination.py`, `exec-quant.py`, `feedback-utils.py`, `evidence-utils.py`, `probe-utils.py`, plus `declaration_reader.py`. The tree has no `scripts/python/store_layout.py`; the runtime store layout fact is read through `declaration_reader.py` (A-5)
**Storage**: no new store — reads `.specify/session/` (memory-tier run-determination entries), `.specify/exec-quant/`, `.specify/feedback/`, `.specify/evidence/`, and the probe registry `.specify/shared/definitions/probe-definitions.md`; writes nothing
**Testing**: `bash scripts/bash/run-tests.sh` (pytest; parallel default; `SPECKIT_PYTHON` ladder); five new guard files authored red-first (contract C-040). This plan stage is docs-only and records `not-run-docs-only` in its stage record
**Target Platform**: repository tooling (OS-agnostic Python); no per-CLI code
**Project Type**: framework / toolkit (templates + shared docs + scripts + tests), single repository
**Performance Goals**: linear in retained records; readings bounded (per-observation sources capped at 20, invalid sources at 50, duplicates at 20, each with shown/total); byte-identical output across reruns
**Constraints**: read-only over the runtime store layout (containment claim C-041); zero network; no writes anywhere; exit 0 whenever a reading is emitted; exit 2 when no reading can be produced; no `.specify/.gitignore` rule and no `runtime-store-layout.yaml` change; no decision-governance alignment (107 stays independent)
**Scale/Scope**: 1 owner document, 5 declaration facts, 1 read-only engine, 6 design-contract files (39 clauses), 5 guard files, 2 framework-map rows, 8 execution premises, 1 inherited-blockers disposition

**Execution record (concurrency)**: `requested=1`; `effective=not_evaluated`; `effective_reason=single-unit`. The stage's units were enumerated before the shape was chosen: research; `plan.md`; `data-model.md`; the six contract files; `quickstart.md`; `feature-ref.md`; the Feature Integration row/detail edit; the gate runs and the wrap-up records. The representable unit set has size 1: the stage assignment forbids dispatching other agents (the executor role's "do not dispatch" boundary) and the driver partitions the plan as one serial work package (checkpoint 02 § 4). The reason code `single-unit` is read from `shared/declarations/facts/serial-reason.yaml` (factual group: the representable unit set has size 0 or 1). No dispatch intervals were produced, so `effective` is `not_evaluated` — never a number.

## Plan Assumptions

Plan-stage adjudications made under the unattended assignment (questions that would otherwise be asked
are answered here so later stages can proceed):

- **PA1 — Scope identity joins on existing identity fields**: a run scope joins each row on that row's
  declared identity fields (`run_id` for run-determination, exec-quant, feedback and gate observations;
  the evidence run's own `runId` for evidence findings). The gate-observation family is identified by the
  `gate:` run-identity prefix its protocol declares. The probe row is a declaration row: it evaluates once
  against current state in every reading and is run-identity-exempt and window-exempt (recorded in the
  scope notes). No proximity or unit-clustering inference exists.
- **PA2 — Unobserved versus not_evaluated**: an unreadable or absent source reads `not_evaluated` with
  cause `source-unavailable`; matching records that are all uninterpretable read `not_evaluated` with
  cause `invalid-source`; zero matching records read `not_evaluated` with cause `no-matching-records`
  under an explicit run scope and `Unobserved` with the same cause under a default or window scope. This
  is the complete four-way split (data-model E-6). A row whose source ships with init — the probe row's
  `probe-definitions.md` — therefore reads `Wired`/`Unobserved` on a fresh project, never
  `not_evaluated` except under an explicit `--run` scope (requirements § Edge Cases).
- **PA3 — Reason taxonomy is not a sixth declaration fact**: the three row-reason causes and the four
  invalid-source causes are owned as meanings by the owner document and as tokens by the engine's
  schema, with a bidirectional contract test pinning the two faces (contract C-015).
- **PA4 — The owner document is the machine-read registry**: the catalog, blind-spot and coverage-map
  tables have fixed shapes, pinned by the owner guard; the engine parses them and validates every cell
  against the declaration sets, aborting on an unknown token (contracts C-003/C-005/C-006/C-013).
- **PA5 — Baseline channel**: the dated baseline reading (FR-026) lands as one feedback entry through
  `feedback-utils.py --action record` at implementation time, under the implementing stage's unit and
  run, carrying the reading's status, per-row states, declaration-set digest and source references
  (contract C-035). The entry is an ordinary dated record, not an aggregate.
- **PA6 — Same-author scoring fallback**: the no-dispatch assignment makes a fresh-context delegated
  review impossible for this run; the Constitution Check and the Post-Generation review are a disclosed
  direct self-read (the objective-analysis gate's fallback path), recorded per row.
- **PA7 — The FR-003 machine check is an engine action**: `--check-coverage` runs the coverage-map check
  over the owner document (exit 0 clean, 1 findings, 2 unreadable). No `/speckit.*` wrapper ships.
- **PA8 — Positive-state caps**: record-bearing rows stop at `Exercised`; the probe row stops at
  `Wired`; the absence states (`Unobserved`, `not_evaluated`) are available to every row (data-model
  I-6). The evidence row's own finding states travel only as the `evidence-missing` deviation class,
  never as the row's state.
- **PA9 — Evidence item read**: no owning function returns finding items; the engine reads the item
  fields after `load_index`, and a contract test pins the field names against the owning engines'
  constants (`FINDINGS_KIND`, `SCHEMA_VERSION`, `FINDINGS_PROJECTION_FIELDS`) so drift is a red test,
  not a silent misread.
- **PA10 — No instructions change**: the mechanism carries no per-session agent obligation; discovery is
  the framework-map rows plus the owner document § Entry. A `docs/` page is a wrap-up documentation
  evaluation item, not a plan deliverable.
- **PA11 — Privacy surfaces**: feedback entries are read through `scan_entries` (frontmatter metadata
  only); gate decision prose and finding summaries never cross into a reading output; no body-reading
  filter is used.
- **PA12 — Output caps**: per-observation source references cap at 20, invalid sources at 50,
  duplicates at 20, each with a truncation disclosure and a total count; the coverage section always
  carries all six blind-spot classes. Caps are output bounds, never judgement thresholds.
- **PA13 — Window arguments**: `--since` / `--until` accept `YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SSZ`
  (UTC); an invalid value exits 2; `--run` combined with either is an input error.
- **PA14 — Declaration-set version**: the reading stamps a SHA-256 over the five fact files (sorted
  repo-relative paths plus bytes), computed at read time; no stored version counter exists.
- **PA15 — Store roots derive from the layout fact (A-5)**: the engine reads
  `runtime-store-layout.yaml#/statement` through `declaration_reader.py`, derives each root as the
  documented `.specify/<store-name>/` projection (the fact carries no per-store `root` key), and holds no
  second root table; a catalog row naming an undeclared store is a hard error (exit 2). Precedent for
  this read pattern: `concurrency-check.py`, `sanitize-utils.py`, `seal-utils.py`.
- **PA16 — Registry posture**: the Feature Integration Protocol duty of this stage is the
  `Draft → Planned` advance in `.specify/features.md` plus the plan note in
  `.specify/features/109-prompt-adherence.md`; the stage brief's "spine/registry" boundary is read as the
  driver state spine and `.specify/register.md` (the ID register), which stay untouched. No new durable
  identifier is coined by this plan.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/constitution.md` v1.20.0 — one row per principle in document order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every contract clause serves an FR (Serves lines across `contracts/`); `feature-ref.md` maps all 30 FRs and 9 SCs to delivering surfaces; no untraced file |
| II | Feature-Centric Development | ✅ Pass | Bound to new Feature 109; this stage reviews the feature list (no add / merge / split beyond the registered feature) and advances the row `Draft → Planned` with a plan note (PA16) |
| III | Intent-Driven Development | ✅ Pass | Requirements plus the 2026-11-27 clarifications drive the plan; `research.md` records measured premises R-1…R-11; contracts are declarative |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Five guard files planned red-first (contract C-040); every acceptance scenario maps to a fixture test (`feature-ref.md` SC map) |
| V | AI Agent Integration Standards | ✅ Pass | No agent roster, tier or config key changes; ships shared docs + one stdlib engine |
| VI | Continuous Quality & Observability | ✅ Pass | Deterministic output, documented exit codes, drift guards; no `.bak` copies; whole-run acceptance via the full suite (SC-009) |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Plan advances Feature 109 to `Planned` only; the Pre-Status-Flip Gate belongs to implement; feature index review recorded in `feature-ref.md` |
| VIII | Code as the Single Source of Truth | ✅ Pass | Value domains read from declarations and owning engines at run time; every behavior claim in `research.md` measured from code (file:line) |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | One read-only engine + docs + facts; explicitly no store, score, dashboard, scheduler or network (Out of Scope) |
| X | Documentation Naming & Location Conventions | ✅ Pass | Owner doc lowercase kebab-case under `shared/definitions/`; fact files `<fact-slug>.yaml`; no reserved names; standard spec-dir artifacts |
| XI | Dogfooding (Self-Application) | ✅ Pass | Two hats named: edits land in framework sources (`shared/`, `scripts/`) and ride publish → install → init; `.specify/` copies are generated mirrors; guards pin the mechanism |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | Reuses six existing engines' read surfaces, the declaration reader, `run-tests.sh` and `sync-mirrors.py`; one new read-only engine is the requirement's own entry (FR-023) |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | Strengthens Change Validation (evidence-backed readings) and Learning Capture (blind-spot register); evidence states stay honest (`Unobserved`) |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | Owner doc (meanings) + five facts (domains) + engine (schema) split declared in C-001/C-011/C-015; every other surface points by path |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | The human reading form is designed against `shared/guidelines/user-facing-comprehension.md` by pointer; C-020/C-027 bound its content and privacy |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | Triage owner untouched; no anomaly-detection engine; the stage records its anomaly line explicitly |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | No new top-level directory; the only new directories are the spec's standard `contracts/` and the per-feature fixtures directory under the declared `tests/fixtures/` convention |
| XVIII | Grounded Naming | ✅ Pass | Names carried verbatim from the requirements and the closed source (prompt adherence, 宿主提示层, 项目规则文件层, the fixed owner/fact/engine paths); remaining names imitate siblings |
| XIX | Self-Explanatory Structure (不言自明) | ✅ Pass | One documented invocation (the floor); names state meaning (`prompt-adherence.py`, fact slugs, reading fields); one information dimension added (the reading) |
| XX | Efficient Test Execution (Concurrent by Default) | ✅ Pass | Guards are fixture-scoped and run through `scripts/bash/run-tests.sh`; no serial-only new file; this docs-only stage records `not-run-docs-only` |
| XXI | Script Interface Contract (Declared, Zero-Side-Effect) | ✅ Pass | Engine answers `-h`/`--help`/`--version`, rejects undeclared options non-zero, writes nothing (C-031); `script-interface-check.py` stays green |
| XXII | Re-Anchoring (不忘初心 · 温故而知新) | ✅ Pass | Stage anchor and rule digest reloaded at step boundaries; verdicts recorded in the stage record; no approval request emitted |
| XXIII | AI-Generated Code Review Policy | ✅ Pass | AI-written change → direct merge to the declared trunk + AI review of the merged history; this plan adds no review ledger; the git workflow owner stays `.specify/workflow/git.md` |

**Gates Status**: ✅ All 23 gates pass — no Fail or Partial row; Complexity Tracking is N/A.

**Re-check after Phase 1**: 2026-11-27 — refreshed against the landed design artifacts (`data-model.md`, the six contract files, `quickstart.md`, `feature-ref.md`, `research.md`, § Phase 1 summary). No row changed status. Scoring was a direct self-read under the no-dispatch assignment (PA6), not a delegated fresh-context pass.

## Decision Tensions

*Owner of the record shape, the admissibility criteria, the rejection forms and the load-bearing
threshold: `.specify/shared/guidelines/decision-tension.md` — one pointer, read from the repository
root; a plan artifact lives under `.specify/specs/<key>/`, so a plan-directory-relative link would
resolve to a path that does not exist. This section lists the field names and points at that file — it
MUST NOT restate the criteria table, the rejection list or the threshold table.*

Fields: `decision`, `antithesis`, `binding_constraints` (with `pole_a` and `pole_b`),
`discriminating_evidence`, `expected_sacrifice`, `revision_trigger`; record identifier `tension_id`
(`T-NNN`).

N/A

本计划无承重决策：下列四类触发均不成立，逐类说明如下。

- 不可逆：本特性不迁移数据、不改既有记录 schema、不换契约载体；回滚就是 revert 本次提交，新增引擎只读（C-029/C-041），新增文件删除即恢复原状，镜像按改动前测得的基线判新漂移。
- 跨团队：本特性不改任何既有引擎的 CLI 面、退出码、记录格式或共享契约；五个声明事实与 owner 文档是本特性新增的独立面，既有消费方不引用它们（FR-007），没有他人依赖的接口被移动。
- 高爆炸半径：一次读取失败只影响本次输出；引擎零写入（C-029）、不派发、不登记、不缓存，故障面不出本特性边界。
- 与宪法原则相关：设计逐条遵守而非取舍宪法 MUST（单一事实源按 owner＋五事实＋引擎 schema 三分，测试先行按 C-040 红先，零新机制按原则 IX），没有以放宽任一 MUST 换取方案成立。

本特性设计形状的三条上游张力记录——owner 文档即机器读取注册表、按运行身份在既有身份字段上严格连接、原因词表不入第六声明事实——由源规格计划的 § Decision Tensions 作为日期化记录拥有（`/storage/project/cloud-native-ai/ai-harness/.ah/specs/092-prompt-adherence/plan.md`）；本计划按引用消费，不另立编号、不复制字段内容。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/109-prompt-adherence/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (standalone: findings R-1…R-11 + residual unknowns)
├── data-model.md        # Phase 1 output (entities E-1…E-11, invariants I-1…I-14)
├── quickstart.md        # Phase 1 output (single invocation + scenario set, per-example premises)
├── contracts/           # Phase 1 output (6 contract files, 39 clauses — this feature's contract face)
├── feature-ref.md       # Phase 1 output (Feature 109 binding + delivery surface + FR/SC maps)
├── checklists/          # requirements-quality checklist
├── test-evidence/       # gate captures, plan-stage record, workspace signatures
├── tasks.md             # Phase 2 output (/speckit.tasks — NOT created by /speckit.plan)
└── verification.md      # Implementation output (/speckit.implement — NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
shared/definitions/                    # NEW prompt-adherence-definitions.md (the owner document; machine-parsed registry)
                                       # EDIT framework-map.md (owner-doc row + reading-entry row)
shared/declarations/facts/             # NEW prompt-adherence-layers.yaml, prompt-adherence-strengths.yaml,
                                       #     prompt-adherence-signals.yaml, prompt-adherence-deviation-classes.yaml,
                                       #     prompt-adherence-reading-status.yaml
scripts/python/                        # NEW prompt-adherence.py (read-only engine + --check-coverage)
.specify/shared/, .specify/scripts/    # generated mirrors of the above (never hand-edited)
tests/fixtures/prompt-adherence/       # NEW declarative fixture sets (repo-internal development assets, not shipped)
tests/contract/                        # NEW test_prompt_adherence_owner.py, test_prompt_adherence_declarations.py,
                                       #     test_prompt_adherence_engine.py, test_prompt_adherence_readonly.py
tests/integration/                     # NEW test_prompt_adherence_init.py (fresh init fixture)
.specify/features.md                   # Feature 109 row: Draft → Planned (plan-stage Feature Integration)
.specify/features/109-prompt-adherence.md  # detail: status + plan note
```

**Structure Decision**: extends the existing framework-source layout (shared docs + declarations +
scripts + tests); no new top-level directory is created, no new runtime store root appears, and
`.specify/` gains only mirror copies. The two hats rule applies: every content edit lands in the
framework sources and rides publish → install → init; `.specify/` copies are generated. The store-root
derivation is a read of the declared layout fact (PA15), not a new roster.

### Mirror Obligations

Baseline measured before the edit (2026-11-27): `python3 scripts/python/sync-mirrors.py --check` exit 0
— all six pairs byte-identical, six projections `ok`; `python3 scripts/python/regen-command-copies.py
--check` exit 0 (captured in `test-evidence/plan-stage-2026-11-27.md`). The implementation-time
criterion is **no NEW drift on the pairs this spec touches**, judged against that baseline — never a
pre-written absolute exit code.

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `shared/definitions/prompt-adherence-definitions.md` (new) | `.specify/shared/definitions/prompt-adherence-definitions.md` | `sync-mirrors.py --check` — no NEW drift vs the 2026-11-27 baseline |
| `shared/definitions/framework-map.md` (edit) | `.specify/shared/definitions/framework-map.md` | pair check; the two new rows appear in both copies |
| `shared/declarations/facts/prompt-adherence-layers.yaml`, `-strengths.yaml`, `-signals.yaml`, `-deviation-classes.yaml`, `-reading-status.yaml` (new) | the same five paths under `.specify/shared/declarations/facts/` | pair check; the engine reads the installed copy through `declaration_reader` |
| `scripts/python/prompt-adherence.py` (new) | `.specify/scripts/python/prompt-adherence.py` | pair check; `--version` answers on both copies and the workspace-resolution leg passes for each |
| no `templates/commands/` change | per-tool command copies | `regen-command-copies.py --check` rc 0 (baseline `OK`, measured 2026-11-27) |

## Execution Premises

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | The existing Python-stdlib script layer can host the read-only engine and its five declaration facts, distributed through publish → install → init (RS-001's cited premise) | `scripts/python/measure.py` (in-process engine read precedent); `shared/declarations/contract.yaml` (required keys and kinds); mirror baseline exit 0, 2026-11-27 | verified | — |
| EP-002 | The six sensor read surfaces exist and expose the fields the catalog predicates need | `research.md` R-2 (functions and line pointers) plus live readings captured in `test-evidence/plan-stage-2026-11-27.md` | verified | — |
| EP-003 | The declaration reader and the triple check accept five new `closed-set` facts with no code change, and the engine's read point is locatable | `shared/declarations/contract.yaml` `required_fact_keys` / `fact_kinds`; `scripts/python/harness-triple-check.py` `has_read_point`; sibling `evidence-seven-states.yaml` | verified | — |
| EP-004 | The owner document can serve as a machine-parsed registry with fixed table shapes | `scripts/python/probe-utils.py` parses the table registry in `shared/definitions/probe-definitions.md` (11 classes / 130 objects / 0 errors, measured 2026-11-27) | verified | — |
| EP-005 | Mirrors and `specify init` deliver the new artifacts downstream with no additional setup | `scripts/python/sync-mirrors.py` `MIRROR_PAIRS`; `src/specify_cli/__init__.py` shared/scripts copy; baseline `--check` exit 0, 2026-11-27 | verified | — |
| EP-006 | The feedback store can host the dated baseline record through the existing engine under a framework unit id | `scripts/python/feedback-utils.py` `record` requires `/speckit.*` or `skill:*`; this stage's own `/speckit.plan` records measured 2026-11-27 | verified | — |
| EP-007 | The runtime store layout enumerates the complete managed root set for the containment claim, and a hash manifest over the derived roots is computable | `shared/declarations/facts/runtime-store-layout.yaml#/statement` (14 stores, no `root` key — measured); `tests/contract/test_runtime_store_layout.py` | verified | — |
| EP-008 | Reading the layout fact through `declaration_reader.py` directly (A-5) is an established pattern and yields the declared store-name set | `concurrency-check.py` `STORE_LAYOUT_FACT`; `sanitize-utils.py`; `seal-utils.py`; measured store list in `research.md` R-8 | verified | — |

No premise is `falsified`; the `Decision` column is `—` throughout.

## Inherited Blockers

**Dependency artifacts (declared, never implied)** — the checker reads only the paths in this block:
- `028`: `.specify/features/028-feedback-mechanism.md`, `.specify/specs/027-feedback-mechanism/verification.md`
- `038`: `.specify/features/038-evidence-infrastructure.md`, `.specify/specs/034-evidence-infra/verification.md`
- `056`: `.specify/features/056-probe-handler-system.md`, `.specify/specs/056-probe-handler-system/verification.md`
- `059`: `.specify/features/059-exec-quant-recording.md`, `.specify/specs/059-exec-quant-recording/verification.md`
- `105`: `.specify/features/024-specification-workspace-versioning.md`, `.specify/specs/105-runtime-store-layout/verification.md`

Excluded, with basis: Feature 107 (decision governance) is read as a boundary reference only — this
feature consumes no record from it and does not align with it (A-16). Feature 109's own artifacts are
never dependencies of itself.

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|
| 1 | — | not-applicable | — | — | Measured 2026-11-27: none of the declared dependency artifacts carries a non-empty `## Deferred` section; their verification logs contain no `blocked` / `deferred` / `partial` status row and only empty `deferred_tasks=` values (059, 105) — the extraction set is empty, so there is nothing to disposition. The five owners are consumed as stable read interfaces. |

## Complexity Tracking

N/A — no Constitution Check row is Fail or Partial.

## Phase 0: Research Review

Phase 0 findings are recorded in `research.md` (standalone): R-1 source-to-target adaptation verified;
R-2 the six sensor read surfaces and their identity/timestamp fields (live readings captured); R-3 the
declaration layer's five-fact fit; R-4 the machine-parsed owner-document precedent (probe registry
measured); R-5 the mirror/init distribution route with its measured baselines; R-6 the evidence findings
shape and its lack of an SDD run identity; R-7 the feedback metadata surface and the `gate:` family; R-8
the containment oracle over the declared store roster and the `.specify/<name>/` root projection (A-5);
R-9 the script-interface and exit-code rules; R-10 the same-author fallback and the baseline channel;
R-11 the test entry, markers and plan-stage evidence discipline. Residual unknowns are listed there as
RU-1…RU-3. No unresolved clarification marker remains.

## Phase 1: Design Artifacts Summary

Counts below were taken from the landed files on disk (grep enumeration, 2026-11-27), after the
artifacts were written — never pre-written.

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | `data-model.md` | 11 entities (E-1…E-11) + 14 cross-entity invariants (I-1…I-14) |
| Contracts | `contracts/` | 6 files, 39 clauses: owner-and-catalog (C-001…C-007), declarations-and-vocabularies (C-010…C-016), reading-semantics (C-020…C-029), engine-and-read (C-030, C-031, C-032, C-034, C-036), distribution (C-033, C-035, C-037), guards-and-boundaries (C-040…C-046) |
| Quickstart | `quickstart.md` | 6 scenarios + a measured sensor-read block + a distribution/suite check block |
| Feature reference | `feature-ref.md` | 30 FR deliveries, 9 SC evidence rows, delivery surface, registry posture |
| Phase 0 research | `research.md` | 11 findings (R-1…R-11) + 3 residual unknowns |

**Drift from the Phase 0 expectation**: none material. The contract set was partitioned into six files
per the stage brief's six areas (engine/read and distribution separated), while keeping the source
clause ids stable at C-001…C-046; the count of clauses (39) equals the source set.