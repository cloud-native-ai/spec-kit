# Recheck: implementation-readiness checklist items answered by later stages

**Append-only record** — shape per `skills/internal/implement-feature/SKILL.md` § Step 2 (third
branch: "an item whose subject a later stage resolved and recorded in `checklists/recheck-<date>-<topic>.md`
counts as answered — not incomplete, no waiver needed").
**Checklist rechecked**: [`readiness-2026-10-29.md`](readiness-2026-10-29.md) (32 items, 18 pass / 14 fail at creation)
**Date**: 2026-10-29, at implement start (`HEAD=71954e31a1ff`)
**Scope**: judgement only — this file edits no requirement, plan, contract or task text.

The 14 items below were marked `fail` by the checklist against the requirement text as it stood at
`312b37017`. The driver's plan/tasks loop then repaired or dispositioned each one; the analyse stage
ran twice after the repairs and closed with 0 CRITICAL / 0 HIGH (commit `71954e31a`). This record
subtracts each item by naming **where its answer is now recorded**, so the gate does not fire on
already-answered items. Nothing here re-scores the checklist.

## A. Answered by an edit to the requirement text itself (6)

| Item | Answer now recorded at | Verdict |
|------|------------------------|---------|
| CHK002 (definition-class not closed) | `requirements.md` FR-008 — the class roots are now an enumerated path list plus the multi-path rule; class membership is path-derived | answered |
| CHK003 (`write-bearing change` undefined) | `requirements.md` FR-007 — defined as any change writing a tracked file, with the read-only analysis carve-out | answered |
| CHK004 (`SDD assignment` undefined) | `requirements.md` FR-005 — defined as a member duty whose routing decision is recorded as `[[STR-004]]` | answered |
| CHK009 (raised per-member cap has no declaration site) | `requirements.md` FR-006 — "no higher per-member cap is declarable" (the exception was removed, not given a site) | answered |
| CHK010 (second concurrent duty has no disposition) | `requirements.md` FR-006 — serialized or rejected by the existing line/ownership mechanism (FR-018) | answered |
| CHK013 (override record vs FR-011 reason code) | `requirements.md` FR-012 — the adjudication MUST carry the FR-011 reason code | answered |

## B. Answered on the design face the requirement delegates to (5)

| Item | Answer now recorded at | Verdict |
|------|------------------------|---------|
| CHK007 (`ambiguous` / `conflicting` undefined) | `contracts/routing-decision.md` C-23 (out-of-domain value = ambiguous) and C-24 (one closed conflict pair); the golden-table rows are authored from the owner document (tasks T020) | answered for implementation; residual: FR-011 still delegates only the reason-code vocabulary, so the decision's closed forms live in the design face |
| CHK008 (goal-only run undefined) | `data-model.md` E1 `target_ref` — absent Target means the run is scoped to the whole Goal; `contracts/nested-invocation.md` C-31 / C-32 validate a Target only when one is supplied | answered |
| CHK011 (SC-001's "both records" has no named carriers) | `contracts/hierarchy-and-authorization.md` C-8 (authorization probe record) + C-14 (the same record carried into the team run report written under the existing `create-team` contract) | answered |
| CHK025 (FR-003 host-rendering prohibition has no SC) | `contracts/hierarchy-and-authorization.md` C-3; pinned mechanically by `tests/contract/test_neutral_metadata_schema.py:130` / `:137` (equality + membership cross-check) and delivered by tasks T008 | answered |
| CHK026 (FR-014 no-restatement obligation has no SC) | `contracts/routing-decision.md` C-17 / C-30; measured by tasks T027 (reverse-count audit) and `tests/contract/test_sdd_routing_definitions.py` | answered |

## C. Answered on the task/measurement face (3)

| Item | Answer now recorded at | Verdict |
|------|------------------------|---------|
| CHK012 ("the review surface" unbound to a mechanism) | `tasks.md` T029 — `/speckit.review` is named as this slice's classification-honesty audit face, with the engine's determinism scoped to declared inputs only | answered |
| CHK021 (SC-004 containment claim void — no baseline referent) | `tasks.md` GATE-5 + `test-evidence/targeted-set-v1-baseline.txt` — a named 13-file set, a name-level comparison form (`comm -13` over failed nodeids), and the zero-delta criterion; re-captured at implement start by T002 | answered |
| CHK024 (FR-020 has no scenario or SC) | `tasks.md` § Requirement Coverage Map — FR-020 carries the recorded implement waiver ("no new SC, no renumbering"), with C-44…C-47 as its decidable face and the waiver accounted in `verification.md` | answered (waived, not silently dropped) |

## Subtraction result

genuinely unresolved items remaining after the subtraction: **0** (14 fails − 14 answered). The gate
therefore does not fire: every item the
checklist raised has a recorded answer at one of the three faces above, and no item was answered by
this record itself. The three category-B items carry a residual note (the requirement sentence was
not rewritten where the answer lives in the design face); each residual is already the subject of a
design clause this slice must implement, so none of them blocks any implement task.
