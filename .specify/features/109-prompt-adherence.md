# Feature Detail: Prompt Adherence Evaluation（提示遵从度评价）

**Feature ID**: 109
**Name**: Prompt Adherence Evaluation（提示遵从度评价）
**Description**: 只读、确定、可离线的提示遵从度评价机制：只消费既有传感器（feedback 条目与门控观察族、exec-quant 记录、run-determination 四轴记录、evidence findings、probe 注册表声明），读时派生按运行与纵向两种读取，双层模型 + 六行信号目录 + 六类盲区 + 机器可检的假定行为覆盖图，零新增存储/采集点/评分，经既有 init 分发。
**Status**: Planned
**Created**: 2026-11-27
**Last Updated**: 2026-11-27

## Overview

Registered as Draft during `/speckit.clarify` for requirement `109-prompt-adherence` (2026-11-27), which confirmed the binding decision recorded at the requirements stage: **new Feature** rather than a slice of any adjacent owner. The candidate owners — 056 Probe-Handler 体系 (probe registry and `Wired` semantics), 059 exec-quant (execution measurement records), 028 Feedback Mechanism (feedback store, gate-observation family and red lines), 105 Runtime Store Layout (managed store roots), 038 Evidence Infrastructure (evidence lanes and findings), plus `run-determination.py` whose schema lives in `shared/workflow/feedback-step.md` § Run Determination — each own one sensor surface; none owns an adherence-reading mechanism, and each candidate's sibling spec set holds no adherence-reading spec, so the binding-precedent heuristic supports create. The capability is an additive port of ai-harness `092-prompt-adherence` (Feature 097); the source Feature ID is not reused and no unrelated hunk (the source's tasks-template change) rides along (A-8).

Scope: one owner document `shared/definitions/prompt-adherence-definitions.md` (premise chain, two-layer model, six-row signal catalog, assumed-behavior coverage map, six-class blind-spot register, reading-contract field meanings and red lines); exactly five declaration facts (`prompt-adherence-layers/strengths/signals/deviation-classes/reading-status.yaml`), no sixth; one deterministic stdlib read-only engine `scripts/python/prompt-adherence.py`; per-run and longitudinal readings derived at read time; read-only containment and determinism guards; distribution through the existing mirror pairs and `specify init`. No new store, capture point, record-schema change, composite score, ranking or network access.

## Latest Review

- **2026-11-27 — plan stage**: plan set landed (`plan.md` with the dynamically derived 23-row Constitution Check and 8 verified execution premises, `research.md` R-1…R-11, `data-model.md` E-1…E-11 + I-1…I-14, six contract files / 39 clauses keeping the source ids C-001…C-046, `quickstart.md` 6 scenarios, `feature-ref.md`); Feature 109 advanced `Draft → Planned` with no add / merge / split. Integration decisions of the plan: store roots derive from `runtime-store-layout.yaml#/statement` through `declaration_reader.py` (no ported `store_layout.py`, no second root table); five closed-set facts, no sixth; reason taxonomy owner/engine split pinned by a bidirectional test; two framework-map rows; no `.gitignore` rule and no store-layout change; decision tensions recorded as N/A with the three design-shape records consumed by reference from the source plan. Gates: `pre-analyze-check --stage plan` pass (0 errors; deliverable-path advisories only), `validate-decision-tensions` ok, plan integrity (no placeholders, single H1, stamp present) ok, mirror and command-copy baselines rc 0.
- **2026-11-27 — clarify stage**: `Related Feature` bound to Feature 109 and this detail registered `Draft`; the six-area scan (sensor mapping, reading semantics, coverage map, engine contract, distribution, tests) adjudicated in the spec's `## Clarifications` Session 2026-11-27, with in-place refinements to the Overview, Related Feature, FR-004, FR-005, FR-011, FR-014, FR-015, FR-023, FR-024, FR-026, A-6 and the Edge Cases; live counts unchanged (FR-001…FR-030 / SC-001…SC-009); validator `status: ok` (0 error / 0 warning).

## Key Changes

1. New single owner document `shared/definitions/prompt-adherence-definitions.md`; every other surface reaches it by pointer (no restated catalog, register or coverage map).
2. Exactly five declaration facts under `shared/declarations/facts/`; observation states compose the existing evidence seven-state domain with the run-determination `not_evaluated` literal — no sixth fact, no verdict tokens.
3. Initial signal catalog of six rows, each defined by a machine-checkable predicate over an existing store and read through its owning engine's read surface; `measure.py` is a read-only projection over the exec-quant store and gets no separate row (FR-005).
4. Per-run and longitudinal readings from one deterministic computation structure (JSON sorted keys, bounded output, no clock fields), replayable from source references and honest about absence (four-way absence derivation, four-state reading status).
5. Assumed-behavior coverage map with a two-way machine check (`--check-coverage`), plus a six-class blind-spot register for behaviors no persisted sensor observes today.
6. Read-only containment claim with a hash-manifest referent, determinism judged separately, mirror/init distribution, and one dated baseline reading through the existing feedback channel.

## Implementation Notes

- The catalog is closed at six rows and the blind-spot register at six classes until an owner revision; adding or retiring a row is one owner revision plus the `prompt-adherence-signals.yaml` member edit in the same change — no second mapping table or registry (FR-004).
- Absence reads as `not_evaluated` / `Unobserved` with a `{cause, source}` reason; `reason` causes are closed at `{source-unavailable, no-matching-records, invalid-source}` and invalid-source causes at `{unparsable, schema-violation, unknown-schema-version, invalid-timestamp}` — meanings owner-side, tokens engine-side, pinned by a bidirectional test (FR-018).
- Layer and strength are declared, never reassigned at read time; no indirect-only input produces a layer-level verdict (FR-009, FR-010).
- Workspace resolution: `--workspace-root`, else the nearest ancestor holding `.specify/`; owner/declaration layer through `declaration_reader.find_repo`; a framework-source copy is never treated as the installed copy (FR-023).
- Tests ride `scripts/bash/run-tests.sh` with `contract` / `integration` markers; fixtures under `tests/fixtures/prompt-adherence/`; docs and fixtures do not ship (FR-020, FR-024).
- Glossary terms (提示遵从度 / 宿主提示层 / 项目规则文件层) remain proposals (`origin=auto`, `status=proposed`) per A-14 until registered through the glossary protocol.

## Future Evolution Suggestions

- A `/speckit.*` wrapper or scheduled surface for the reading — a separate future decision (A-18).
- Owner-sanctioned persistence for instruction-reconcile observations would retire the `instruction-drift-between-reconciles` blind spot; it is not part of this feature.
- A dated before/after study if any composite metric is ever proposed; today the mechanism deliberately produces no score (A-11).

## Related Files

- Feature Index: `.specify/features.md`
- Feature Detail: `.specify/features/109-prompt-adherence.md`
- Specification: `.specify/specs/109-prompt-adherence/requirements.md`
- Quality Checklist: `.specify/specs/109-prompt-adherence/checklists/requirements.md`
- Source capability (ai-harness, external to this repository): `.ah/specs/092-prompt-adherence/` — ported additively; not a runtime dependency
- Adjacent owners (pointer only, no fact moved): `shared/definitions/probe-definitions.md` (056), `scripts/python/exec-quant.py` (059), `shared/workflow/feedback-step.md` (028), `shared/declarations/facts/runtime-store-layout.yaml` (105), `scripts/python/evidence-utils.py` + `shared/declarations/facts/evidence-lanes.yaml` (038), `scripts/python/run-determination.py`, `shared/workflow/symlink-model.md`, `shared/guidelines/better-harness.md`
- Cross-referenced Features: `.specify/features/028-feedback-mechanism.md` (reverse cross-reference recorded there), `.specify/features/056-probe-handler-system.md`, `.specify/features/059-exec-quant-recording.md`, `.specify/features/038-evidence-infrastructure.md`

## Status Tracking

- **Draft**: requirements 109 is bound and `/speckit.clarify` completed. (current — 2026-11-27)
- **Planned**: plan/design artifacts exist for the bound spec and the Constitution Check has no unjustified Fail rows.
- **Implemented**: tasks are closed and the guard roster lands green.
- **Blocked**: tasks are closed and at least one final-path criterion is not `pass`.
- **Ready for Review**: review evidence exists and the current code-review record has no blocking entry.
- **Sealed**: review concluded with zero unhandled P0, acceptance records complete, and merge-back done when slices exist.
- **Completed** (legacy — closed for new work): historical terminal record only; not used for this feature.

## Related Specifications/Requirements

- Specification: `.specify/specs/109-prompt-adherence/requirements.md`
  Quality Checklist: `.specify/specs/109-prompt-adherence/checklists/requirements.md`
- Source specification (ai-harness 092, external): `.ah/specs/092-prompt-adherence/requirements.md` — binding basis and port mapping recorded in the spec's `## Related Feature` and Clarifications Session 2026-11-27.
- Reverse cross-reference: Feature 028 Feedback Mechanism — `.specify/features/028-feedback-mechanism.md` (feedback entries and the gate-observation family are consumed read-only through `feedback-utils.py scan_entries` metadata).
- Adjacent Feature with no detail file: Feature 105 Runtime Store Layout — only an index row and the declaration `shared/declarations/facts/runtime-store-layout.yaml` exist; the read-surface relation (FR-030 resolves row stores against that declaration) is recorded here instead of creating a detail file, per the Feature Integration Protocol's legacy-entry rule.