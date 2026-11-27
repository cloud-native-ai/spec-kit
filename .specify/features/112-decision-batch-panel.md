# Feature Detail: Batch Decision Panel（批量决策面板）

**Feature ID**: 112
**Name**: Batch Decision Panel（批量决策面板）
**Description**: 决策管理的集中裁决面：一次调用聚合封闭来源清单中的全部待决策项，按 107 完整信息模板逐项呈现，附确定性接地的建议默认值（无证据时明示 `no-evidence`），用户只对异议项发声，其余合格项按建议默认值结案；处置经既有载体记录（knowledge 批次记录 + 107 决策记录 + register 登记 + 来源状态更新），整批可只凭记录重放；只服务人持有的决策，零新存储、零网络、零自动传输。
**Status**: Ready for Review
**Created**: 2026-11-27
**Last Updated**: 2026-11-27

## Overview

Registered as a standalone Feature at the requirements stage (2026-11-27) on line `decision-batch-panel` (run `r20261127T081500Z-112a`). The user's requirement — aggregate every pending decision item, present complete information, attach a recommended default grounded in prior experience, take objections only, and let every uncontested item take its default — is delivered as an additive extension of Feature 107's owner page, not a second decision system.

Scope: one owner-page extension (`shared/definitions/decision-definitions.md`: pending-item form, closed two-source roster, batch presentation and grounding contracts, batch dispositions, batch record contract, batch family fields, P-13 producer row, human/ai boundary, completeness/refusal, replay); one thin command `/speckit.decide` (`templates/commands/decide.md`); one internal skill `decide-batch`; one deterministic stdlib engine `scripts/python/decision-batch.py` with closed actions `scan` / `record` / `replay`; one dated batch record per batch in the existing knowledge store; the existing 107 record grammar extended by three conditional batch-family fields. No new store root, no second registry, no second record schema, no scheduler, no network, no automatic transmission.

Measured baseline (2026-11-27, base `c3489e52c`; corrected by the clarify ruling A-21): the register carries **seventeen** open OI-/D-family rows (OI-3, OI-4, OI-7, OI-9, OI-069b-01, OI-073-01, OI-082-01, D-001, D-001-a, D-1 (092), D-2 (092), D-3 (092), D-4 (092), D-5 (092), D-6 (092), D-7 (092), D-8 (092)) — the requirements-stage hand list recorded eight and omitted D-001, D-001-a and D-1/D-3…D-8 (092); the predicate-derived reading is authoritative. Zero `### PENDING —` blocks exist in the four scan roots; the producer inventory ends at P-12; no `decide` command or skill exists. The first honest batch therefore presents those seventeen rows as `incomplete` with named missing elements — completing them is the producer/user obligation (A-16), never invented by the panel.

## Latest Review

- **2026-11-27 — review round 2**: four segments + ARC in one consolidation pass on the repaired tree (`e319f265b`; round-1 records archived as `review-r1.md` / `code-review-r1.md`). Process pass (0 P0 / 4 P1 carried from round 1 — framework targets); artifact pass (12/12 expected set; 0 P0 / 2 P1 / 3 P2 open, F7 closed by this round's detail update); implementation pass (round-1 P1 findings F11/F12 closed — the C-204 guard reds on the baseline engine `1 failed` and greens on the repaired tree `10 passed`; smoke re-run exit 0 — `108 passed in 8.51s`; mirror byte-identical); code segment `not-evaluated` — a non-conclusion with 0 coverage gaps (receipt 349 changed / 19 judged / 330 declared legal skips; 0 blocking / 1 important answered / 2 suggestions / 1 praise; gate `allow`; capture skipped — framework hat); ARC `accept` — `final_path` pass 7 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 7, four completion conditions true; Feature 112 `Implemented → Ready for Review`. Reports: `review.md`, `code-review.md`.
- **2026-11-27 — review round 1**: four segments + ARC; code segment `blocked` — gate `blocking-unresolved` with 2 blocking entries (the user-facing completeness disclosure printed roster source ids and the `read` presence token; the missing-field sentence printed raw field names; the C-204 guard was blind to both), so the status transition was refused and Feature 112 stayed `Implemented`. The blocking gap was repaired at `e319f265b` (plain-language display maps; widened guard with reverse samples; mirror re-synced; two in-passing corrections disclosed). ARC `agree` (`final_path` 7/7). Reports archived: `review-r1.md`, `code-review-r1.md`.
- **2026-11-27 — implement stage**: tasks T001–T058 closed across four packages; the owner-page extension, the `decide` command, the `decide-batch` skill and the deterministic engine landed in framework sources and ride the mirror projection byte-identically; GATE-1…GATE-8 green; `verification.md` derived spec-side with the three in-scope RS joint-acceptance rows; the closure checker returned `accept` (`final_path` pass 7/7, four conditions true) before the `Planned → Implemented` flip. Evidence: `.specify/specs/112-decision-batch-panel/test-evidence/`.
- **2026-11-27 — analyze stage**: round 1 found 0 CRITICAL / 2 HIGH (batch isolation vs prior-batch read; supersession write-back vs batch immutability); the repair resolved both at the owner surfaces as A-26/A-27 with one-hop carrier alignment, and round 2 re-read the full declared domain with no open CRITICAL/HIGH.
- **2026-11-27 — checklist stage**: the 40-item requirements-quality instrument landed with 45/45 FR, 10/10 SC and 54/54 clause coverage; the disclosed residues (count drift, final-set wording) became round-1 review findings F9/F10.
- **2026-11-27 — tasks stage**: 58 dependency-ordered task rows (tests mode ON), 54 clauses partitioned across eight gates; the stage's `[green:]` claims later backed by the implement evidence set.
- **2026-11-27 — requirements stage**: spec authored with FR-001…FR-045 and SC-001…SC-010; the brief's six ambiguities adjudicated in A-3…A-9 plus the heavy-decision shape for silence semantics (A-10); validator `status: ok` (0 error / 0 warning; 408 lines / 55 definition rows / 15 shared strings); `pre-analyze-check --stage requirements` `pass` (0 errors, 7 missing-path advisories naming this feature's not-yet-created deliverables; `fr=45 sc=10`); `decomposition-check --mode plan` `proceed` (45 FR / ceiling 120); workspace guard snapshot + check clean. Evidence: `.specify/specs/112-decision-batch-panel/test-evidence/`.
- **2026-11-27 — plan stage**: `plan.md` (23-row dynamic Constitution Check, Decision Tensions `N/A` with the four-trigger justification, 7 execution premises incl. the falsified first-batch premise with `fallback`, declared dependency set with one `not-applicable` row), `research.md` (14 measured baselines + 12 resolved design points), `data-model.md` (13 entities / 22 invariants / 5 state domains), `contracts/` ×6 (**54 clauses**), `quickstart.md` (7 scenarios; engine examples pinned by named tests with premises), `feature-ref.md` (FR-001…FR-045 → clause map). `pre-analyze-check --stage plan` **pass** (0 errors / 39 missing-path advisories for implementation deliverables; `fr=45 sc=10 clauses=54 files=13`); `validate-decision-tensions.py` `status: ok` (0 records, N/A form); plan integrity: exactly one `# Implementation Plan:` heading, Requirement → Feature stamp present, 0 residual placeholders; workspace guard snapshot + check clean. Test entry not run: documentation-only stage and this worktree carries no pytest interpreter (measured runner error); the constrained-baseline test is unavailable for the same reason. Evidence: `.specify/specs/112-decision-batch-panel/test-evidence/plan-stage-2026-11-27.md`.

## Key Changes

1. Owner-page extension only: pending decision item + `### PENDING —` block grammar, closed two-source roster, batch presentation/grounding/disposition/record contracts, batch family fields via the conditional layer, P-13 producer row.
2. New `/speckit.decide` entry + `decide-batch` skill + deterministic `decision-batch.py` engine (scan / record / replay); fixed-rule judgements stay in the engine.
3. Recommended default = the item's declared default option; deterministic grounding join over a closed prior-experience roster; honest `no-evidence` label; no invented preference or option.
4. Objection-only interaction: silence accepts only eligible (human, complete, exactly-one-default, reversible, conflict-free) items in a completed interactive batch; parked items stay pending; unattended runs cannot record acceptance.
5. Recording through existing carriers: one dated batch record in the knowledge store (one file per batch), 107 decision records with batch-family fields, register registration + resolution status updates, pending-block `resolution` field; replay from recorded carriers alone.
6. Redecision routes through 107 supersession; human vs `ai-autonomous` split preserved; zero new store, zero network, zero automatic transmission.

## Implementation Notes

- The batch record is a memory-engine-written knowledge entry, one per batch, never overwritten; the same-batch-id second write is a refusal (A-11, FR-032, FR-037).
- The batch family (`batch_id` / `batch_disposition` / `recommendation_grounding`) is a conditional-layer addition owned only by the owner page; existing records keep their grammar and are never rewritten (A-12).
- Grounding is literal and deterministic: default-option evidence pointers that resolve to prior-experience carriers, plus prior records whose `context` contains the subject string verbatim, plus their `T-NNN`; no semantic search at presentation time (A-6, FR-022).
- Prior-decision conflicts and redecisions are judged before presentation; the old record gets `superseded_by` and keeps its content byte-for-byte (A-7, FR-029).
- Completeness is a closed-set claim (referent = this scan; allowed delta = empty); a present-but-unreadable source refuses the whole batch; an absent source is a named absence, and zero items answer `nothing-pending` (A-8, FR-015…FR-018).
- The frozen command/skill baseline in `tests/contract/test_migration_distribution.py` and the decision-inventory guards move in the same change as the new command/skill and P-13 (A-15, FR-042, FR-044).
- The ambient `## Decision Items` instruction section is deliberately not edited (1,276 B of a 1,500 B cap); discoverability rides the command template, command docs and the framework map (A-15).
- Existing open OI rows without pending blocks are presented `incomplete`, not auto-completed; curation/authoring of missing elements is out of scope (A-16).
- No `.specify/.gitignore` rule and no `runtime-store-layout.yaml` change: the feature adds no runtime directory.
- Plan-stage mechanics fixed for implementation: the engine pre-checks the target path and refuses a duplicate batch id **before** calling the memory engine, because the knowledge scope is upsert-by-slug (research M-6); qualification precedence and named reasons are fixed in `data-model.md` § 2; explicit settlement of ineligible items is bounded by record formability (`objection-reply` C-407).
- Distribution duties land together: the new skill needs its probe object + bindings and a compiled wrap-up (census pin 122 → 123), and the frozen command/skill baseline moves 32 → 33 / 60 → 61 in the same change.

## Future Evolution Suggestions

- A curation capability that drafts a pending-item block from an authority carrier (with evidence pointers) for the user to confirm — a separate decision, because it authors the content the panel must present neutrally (A-16).
- A `/speckit.decide replay` UX refinement or a status view of recent batches — only if a recorded user need appears; no dashboard (A-17).
- Broadening the prior-experience grounding beyond literal subject containment would need a deterministic identity rule, not semantic matching (A-6).

## Related Files

- Feature Index: `.specify/features.md`
- Feature Detail: `.specify/features/112-decision-batch-panel.md`
- Specification: `.specify/specs/112-decision-batch-panel/requirements.md`
- Plan: `.specify/specs/112-decision-batch-panel/plan.md`
- Research: `.specify/specs/112-decision-batch-panel/research.md`
- Data model: `.specify/specs/112-decision-batch-panel/data-model.md`
- Contracts: `.specify/specs/112-decision-batch-panel/contracts/` (6 files, 54 clauses)
- Quickstart: `.specify/specs/112-decision-batch-panel/quickstart.md`
- Feature reference: `.specify/specs/112-decision-batch-panel/feature-ref.md`
- Quality Checklist: `.specify/specs/112-decision-batch-panel/checklists/requirements.md`
- Stage evidence: `.specify/specs/112-decision-batch-panel/test-evidence/requirements-stage-2026-11-27.md`, `.specify/specs/112-decision-batch-panel/test-evidence/clarify-stage-2026-11-27.md`, `.specify/specs/112-decision-batch-panel/test-evidence/plan-stage-2026-11-27.md`
- Extended owner (pointer only, no fact moved): `shared/definitions/decision-definitions.md` (107)
- Adjacent owners reached by pointer: `shared/guidelines/confirmation-gates.md` (destructive list + gate signals), `shared/guidelines/decision-tension.md` (`T-NNN`), `shared/guidelines/closed-set-claims.md`, `shared/guidelines/user-facing-comprehension.md`, `.specify/register.md` (ID index)
- Batch record store (existing): `.specify/knowledge/` via `scripts/python/memory-utils.py`

## Status Tracking

- **Draft**: requirements 112 bound; spec + quality checklist landed; validator and driver gates green. (historical — 2026-11-27)
- **Planned**: plan/design artifacts exist for the bound spec and the Constitution Check has no unjustified Fail rows. (historical — 2026-11-27)
- **Implemented**: tasks are closed and the guard roster lands green. (historical — 2026-11-27; closure checker `accept`, `final_path` pass 7/7, before the flip)
- **Blocked**: tasks are closed and at least one final-path criterion is not `pass`. (not occupied)
- **Ready for Review**: review evidence exists and the current code-review record has no blocking entry. (current — 2026-11-27; review round 2 accepted: four segments + ARC, code record 0 blocking, gate `allow`)
- **Sealed**: review concluded with zero unhandled P0, acceptance records complete, and merge-back done when slices exist.
- **Completed** (legacy — closed for new work): historical terminal record only; not used for this feature.

## Related Specifications/Requirements

- Specification: `.specify/specs/112-decision-batch-panel/requirements.md`
  Quality Checklist: `.specify/specs/112-decision-batch-panel/checklists/requirements.md`
  Plan set: `.specify/specs/112-decision-batch-panel/plan.md` (+ `research.md`, `data-model.md`, `contracts/`, `quickstart.md`, `feature-ref.md`)
- Parent capability (pointer, not a slice relation): Feature 107 Decision Governance — `.specify/features/107-decision-governance.md`
- Parked source: `.specify/todo/20261127-decision-batch-panel.md` (retire at merge per the Park lifecycle)

## Status Criteria

- Implemented: tasks closed, verification derived spec-side, gates green (met 2026-11-27).
- Ready for Review requires the four-segment review + ARC acceptance (met 2026-11-27, review round 2 — see `review.md` § 2.5).
