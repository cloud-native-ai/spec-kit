# Feature Reference: 071-review-code-integration

**Requirement → Feature**: `071-review-code-integration` → Feature 071 Review 命令与代码评审技能的组合与治理（Review × Code-Review Composition）
**Feature row**: `.specify/memory/features.md` (ID 071) | **Feature detail**: `.specify/memory/features/071.md`
**Date**: 2026-10-27

## 1. Binding

| Item | Value |
|------|-------|
| Feature ID | 071 |
| Binding point | `/speckit.requirements` (deviation from the default clarify-time binding — recorded in the requirements' Assumptions A2 and in the feature detail) |
| Status this stage | `Draft` → `Planned` |
| New Feature created | no — the row and the detail already exist from the requirements stage |
| Specification path | `.specify/specs/071-review-code-integration/requirements.md` (unchanged) |
| Slices | none — one slice; the decomposition gate returned `proceed` (`fr_count=28`, ceiling 30) |

The requirements' `Related Feature` section already names Feature 071 and the Feature Index row already points at this specification, so this stage advances status and records the plan's key changes rather than creating a second row (Feature Binding Rules in `shared/workflow/feature-integration.md` forbid duplicate Feature IDs).

## 2. Delivery surface

Framework sources only. Every projected copy is produced by an existing generator (see § 6).

| File | Change |
|------|--------|
| `templates/commands/review.md` | the two segments, the applicability triage, the failure-propagation rule, the severity non-collapse rule, and pointers to both skills; no methodology inlined; closing face and handoffs untouched |
| `templates/review-template.md` | a `### 2.1` code-segment subsection (verdict plus pointers only) and the matching placeholder-glossary rows; existing section numbers unchanged |
| `templates/feature-details-template.md` | the `Implemented → Ready for Review` row gains its third condition and the direct six-level read; this file stays the normative owner |
| `shared/workflow/feature-integration.md` | the `/speckit.review` row and the `/speckit.checklist` row become references to that owner |
| `skills/internal/code-review/SKILL.md` | non-interactive path, base resolution, record header and rotation, the rewritten renderer clause, the receipt as sole evidence, the sibling-boundary declaration, the feedback classification duty |
| `skills/internal/code-review/scripts/git-delta-review.sh` | new subcommands: base resolution, record creation/rotation, coverage receipt with exit codes, explicit-input verdict |
| `skills/internal/code-review/references/delta-setup.md` | renderer-absence wording aligned with the rewritten clause (no "stop when missing" assertion survives) |
| `skills/internal/review-sdd-process/SKILL.md` | `description` and `## Boundaries` rewritten to "distinct judgment objects, composed by the command"; the process judgement itself unchanged |
| `docs/reference/commands/review.md` | the composed surface: two segments, two artifacts, two vocabularies, three applicability values, the transition pointer |
| `tests/contract/test_review_code_composition.py` | NEW — command template: segments, order, triage values, failure propagation, no inlined methodology |
| `tests/contract/test_code_review_skill_contract.py` | NEW — skill body and script surface: non-interactive path, base tiers, header, renderer rewrite, boundary wording |
| `tests/contract/test_coverage_receipt.py` | NEW — receipt grammar, set equality, exit codes, skip semantics, verdict derivation, gap drill |
| `tests/contract/test_status_gate_owner.py` | NEW — owner row content, convergence, both initiators, waiver rule |
| `tests/contract/test_review_feedback_boundary.py` | NEW — feedback classification, nested units, wrap-up invariance, expression boundary |
| `tests/contract/test_review_docs_isomorphism.py` | NEW — docs page ↔ template surface, mirror projections present |
| `tests/contract/test_review_p1_review_loop.py` | ONE pin updated (disclosed § 5) |

Not in the delivery surface: `shared/workflow/expression-gates.md` (the expression review face is unchanged by design — see C-62), the probe registry (both wrap-up faces already registered), `src/specify_cli/`, and any `.specify/` runtime copy.

## 3. Requirement coverage

Every functional requirement is cited from at least one contract clause's citation group; the table below is the publishing view of that mapping, not a second accounting.

| FR | Clause(s) | FR | Clause(s) |
|----|-----------|----|-----------|
| FR-001 | C-1, C-2 | FR-015 | C-25 |
| FR-002 | C-3, C-4, C-5 | FR-016 | C-16, C-55 |
| FR-003 | C-6, C-7, C-39 | FR-017 | C-56, C-57 |
| FR-004 | C-8, C-18, C-19, C-20 | FR-018 | C-58, C-59 |
| FR-005 | C-8, C-43, C-44 | FR-019 | C-14, C-52 |
| FR-006 | C-20, C-35 | FR-020 | C-15, C-60, C-61 |
| FR-007 | C-2, C-50 | FR-021 | C-17 |
| FR-008 | C-45 … C-49, C-52, C-53, C-54 | FR-022 | C-18, C-19, C-21 |
| FR-009 | C-51 | FR-023 | C-26, C-27 |
| FR-010 | C-11, C-12 | FR-024 | C-28 |
| FR-011 | C-9, C-10, C-39 | FR-025 | C-29 |
| FR-012 | C-13 | FR-026 | C-30, C-72, C-73 |
| FR-013 | C-22, C-23, C-24, C-40 | FR-027 | C-62, C-63, C-64 |
| FR-014 | C-31 … C-43 | FR-028 | C-42, C-65 … C-71 |

Success criteria:

| SC | Clause(s) / evidence |
|----|---------------------|
| SC-001 | C-9, C-14 — one file carries both conclusions |
| SC-002 | C-33, C-34, C-37, C-42 — set equality, non-zero gap exit, skip semantics, gap drill |
| SC-003 | C-22, C-23, C-24, C-40 — text mode marker, no rendered claim |
| SC-004 | C-46, C-49 — gate denies on unresolved `blocking`, allows with `important` only |
| SC-005 | C-6, C-62 — `not-applicable` for a code-less feature; expression assertions untouched |
| SC-006 | C-65, C-66, C-67, C-70, C-71 — six test groups, red-first, one pin update, no new drift |
| SC-007 | C-56, C-57 — the classification duty is written, so a defect-as-feedback sample is detectable |

## 4. Overlap

- Clarify-stage overlap check: `decision=clear`, `overlaps=0` (`test-evidence/overlap-check.json`, 2026-10-27).
- This plan introduces no live writer on any other feature's surface: `skills/internal/code-review/**` and `skills/internal/review-sdd-process/**` are edited in place by their own feature's successor; `templates/commands/review.md` is edited by this feature alone; `templates/review-template.md`, `templates/feature-details-template.md` and `shared/workflow/feature-integration.md` receive additions or a convergence edit and no ownership transfer.
- Feature 063 (review P1 governance) owns the recommendation-registration duty and the transition row's existence; this feature references both (C-60, C-45) and transfers neither.

## 5. Disclosed deviations and the one intentional pin change

1. **Feature binding at the requirements stage** (not clarify) — carried from the requirements' Assumptions A2; the Feature row exists, so this stage only advances status.
2. **No branch creation or switch** — the plan setup script resolved the spec directory by numeric prefix on the current branch and copied the template; no branch operation was performed by this stage (requirements Assumption A1, `research.md` § R13).
3. **One pin updated** — `tests/contract/test_review_p1_review_loop.py::test_c15_review_owns_the_ready_for_review_transition` asserts two literals (`review.md committed`, `deferred item resolved or waived`) inside the feature-integration status table. Clause C-47 removes that duplicated wording, so the pin follows the fact's new location instead of preserving the copy: the test keeps its subject, adds an assertion of the owner path, and adds a negative assertion that the duplicated wording is gone. Net assertions increase; the reason and the rejected alternatives are recorded in `research.md` § R5.
4. **Same-author analysis gate not delegated** — this environment exposes no subagent dispatch. Every Constitution Check row carries `(direct read, subagent unavailable)` and `research.md` § R12 records the weaker evidence path; the program-derivable checks were actually run instead.
5. **Expression gate document deliberately untouched** — its existing contract test is re-run as evidence rather than reworded (`research.md` § R14).

## 6. Mirror and projection obligations

The authoritative per-pair table is `plan.md` § Mirror Obligations. Summary of the criterion: every edited source lands its projected copy through the existing generators, and the acceptance test is **no NEW drift** against measured clean baselines (templates 22 files, skills/internal 136 files, shared 55 files, per-tool command copies matching). No `.specify/` runtime copy is hand-edited.

## 7. Required artifacts before this stage closes

| Artifact | Owner |
|----------|-------|
| `plan.md` (filled in place, one top-level heading, the Requirement → Feature stamp) | this stage |
| `research.md` (decisions R1–R14 with measured evidence) | this stage |
| `data-model.md` (entities E1–E13, validation rules V1–V28) | this stage |
| `contracts/` (6 files, clauses C-1 … C-73) | this stage |
| `quickstart.md` (scenarios A–H plus the regression block, each with execution status and premises) | this stage |
| `feature-ref.md` (this file) | this stage |
| `tasks.md` | `/speckit.tasks` (later stage) |
| `verification.md` | `/speckit.implement` (later stage) |
