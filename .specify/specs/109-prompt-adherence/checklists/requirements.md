# Specification Quality Checklist: Prompt Adherence Evaluation — 提示遵从度评价（Prompt Adherence Evaluation）

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-11-27
**Feature**: [.specify/specs/109-prompt-adherence/requirements.md](../requirements.md)

## Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Stability / containment claims name a baseline referent and a derivable allowed-delta set (owner: `.specify/shared/guidelines/closed-set-claims.md`)
- [x] Success criteria are measurable
- [x] Success criteria are technology-agnostic (no implementation details)
- [x] All acceptance scenarios are defined
- [x] Edge cases are identified
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria
- [x] User scenarios cover primary flows
- [x] Feature meets measurable outcomes defined in Success Criteria
- [x] No implementation details leak into specification

## Notes

- Deterministic checker (2026-11-27): `status: ok`; all six labels pass —
  `id-contiguous`, `doc-order`, `ref-resolvable`, `marker-count`, `dup-id`, `path-marker`;
  scanned 296 lines, 39 definition rows, 2 shared strings; 0 error(s), 0 warning(s).
  These counts are read from the checker run, not hand-typed. The checklist is stamped
  after that run; the re-run after this write-back is recorded in
  `test-evidence/requirements-stage-2026-11-27.md` § Gate-1.
- Flow-class read: the dispatch quartet is `flow_class=execution; source=default;
  marker=; error=owner-unavailable`; the local lookup
  `flow-class-check.py --action lookup --unit-id "/speckit.requirements"` returns
  `flow_class: execution`, `source: ledger`, `error: null`. The spec header declares
  `**Flow Class**: execution` / `**Flow Type**: -` (the unique declaration point);
  both readings agree on the class, and the divergence is in the source field only.
- Containment claim: SC-002 and FR-024 name their referent (a hash manifest over the
  managed store roots owned by `shared/declarations/facts/runtime-store-layout.yaml#/statement`,
  resolved in this tree as the `.specify/<store-name>/` projections of the declared store
  names, FR-030) and the derivable allowed-delta set (none; interpreter bytecode caches
  `__pycache__/`, `*.pyc` excluded by name). Determinism is a separate claim and never
  cited as containment evidence.
- Reader baseline: framework maintainers and customer-project maintainers; every domain
  term is either reached by owner pointer (instructions surface via
  `shared/workflow/symlink-model.md`, host-vs-project harness via
  `shared/guidelines/better-harness.md`, evidence seven states, run-determination axes,
  feedback red lines) or carries its bilingual definition in this spec (宿主提示层 /
  项目规则文件层 / 提示遵从度).
- Deliberate adjudications recorded rather than guessed silently (see the spec's
  Assumptions): A-2 Feature 109 binding (new, independent; registry registration deferred
  to clarify); A-5 store-layout read-surface divergence (no `store_layout.py` in this
  tree; `declaration_reader.py` direct read); A-6 no new runtime store; A-8 the source's
  tasks-template hunk is excluded as an unrelated convention line; A-9 the dated baseline
  is required; A-11 no composite score (load-bearing, with antithesis, discriminating
  evidence, anti-metric and reopening condition); A-13 manual scaffold deviation (branch
  numbering collision).
- Source adaptation: ported from ai-harness `092-prompt-adherence` (Feature 097); the
  source Feature ID is not reused, and every sensor path, record kind token, CLI form and
  mirror pair is adapted to and verified against this tree (A-3/A-4; evidence in
  `test-evidence/requirements-stage-2026-11-27.md` § R-1).
- Clarify stage (2026-11-27): six-area scan adjudicated in the spec's `## Clarifications`
  Session 2026-11-27 (sensor mapping incl. measure-as-projection, absence-state and
  reading-status derivations, catalog add/retire procedure, workspace resolution / Two Hats,
  distribution none-list, source-contract-to-test roster); write-back touched Overview,
  Related Feature, FR-004/005/011/014/015/023/024/026, A-6 and the Edge Cases; live counts
  unchanged (30 FR / 9 SC / 2 STR). Post-write validator reading (dated history; supersedes
  the requirements-stage line count only): `status: ok`, 0 error / 0 warning, 310 lines /
  39 definition rows / 2 shared strings — `test-evidence/clarify-validator.txt`.
- Items marked incomplete require spec updates before `/speckit.clarify` or `/speckit.plan`.