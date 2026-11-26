# Feature Detail: Decision Governance（AI Agent 决策项治理）

**Feature ID**: 107
**Name**: Decision Governance（AI Agent 决策项治理）
**Description**: 面向 AI Agent 工作流的一般决策项契约：完整名称/同名定位与两类强调的决策文本、封闭选项集、封闭决策生产者清单与既有载体归档投影、superagent→subagent 决策块传递与实施回执，以及机器可判（M-01…M-09）/行为类（B-01…B-07）强制边界与落地兼容收口。
**Status**: Ready for Review
**Created**: 2026-11-25
**Last Updated**: 2026-11-26

## Overview

Registered as Draft during `/speckit.clarify` for requirement 107 (2026-11-25), which resolved the binding decision: **new Feature** rather than a slice of any adjacent owner. The candidate owners — 046 Confirmation Gate Governance, 076 Decision Tension, 053 Machine-Decidable Artifacts, 095 Super Agent Role, 090 Re-Anchoring — each own a narrow adjacent fact (gate taxonomy / `T-NNN` six fields / machine-decidable boundary / role-edge payload / re-anchoring reload); none owns a general decision-item contract, and each candidate's sibling spec set is a single topical spec, so the binding-precedent heuristic points to create. The spec declares a new concept with a new single owner page `shared/definitions/decision-definitions.md` (A-2); adjacent owners keep their facts and gain pointer lines only (FR-002).

Scope: one owner page (closed vocabulary, class-specific presentation, option-set contract, record field closure, transmission and implementation-receipt obligations, machine/behavior boundary); a closed Decision Producer Inventory mapping every producer to an existing carrier (no second registry or store — `.specify/register.md` stays the sole id index); the two production rules (full names; full resource location on same-name conflicts) as a minimum bar in the owner page, the instruction template, the decision template and guards/review; decision-block transmission on the existing dispatch payload with acknowledgment and `implementation_receipt`; machine guards with reverse samples (M-01…M-09) and named review surfaces for behavior rules (B-01…B-07); mirrors, per-tool copies, client init receipt and migration/refusal closure.

## Latest Review

- **2026-11-26 — `/speckit.review` slice 107 (run `r20261125T134500Z-107a`)** — Report: `.specify/specs/107-decision-governance/review.md`; code record: `.specify/specs/107-decision-governance/code-review.md`.
  - **Process segment**: `pass` with 1 P0 (repaired in-run), 4 P1 and 1 P2 findings — the P0: the implement U4 flipped `Planned → Implemented` while `verification.md` was absent and no closure-checker record existed anywhere in the stage evidence; the review derived the carrier spec-side from `test-evidence/verification-input.md` (10 SC rows + six `RS-NNN_joint_acceptance=` rows + smoke triple) and ran the ARC to `accept`. The P0 rows carry the documented `(validated: direct re-read, subagent unavailable)` fallback (this assignment prohibits validation dispatch).
  - **Artifact segment**: `pass` — coverage 10/10 after the repair (9/10 at review start; missing member `verification.md`); A2 P1 (registry `Implemented` vs detail `Planned` — repaired with this flip), A3 P1 (SC-001 note overstated the documented scan; corrected in the derived carrier, semantic question open as I1), A4 P2 (SC-008's "blocking count unchanged" literal vs the recorded 31→30 re-baseline), A5 P2 (M-01 supersession conditional leg has no machine-detectable trigger).
  - **Implementation segment**: `pass` — smoke `43 passed` exit 0 (evidence `.specify/specs/107-decision-governance/test-evidence/review-evidence.txt`), scope confined to the declared landing surface plus the declared line-106 merge, regression re-measured (preservation sweep 5 failed / 241 passed, all five names inside `baseline-failed.txt`, zero new names; FR-025 three-path diff rc 0); I1 P1 (inventory observed-set augmentation), I2 P2 (stale figure in the generator's raise record).
  - **Code segment**: `not-evaluated` (receipt 684 changed / 27 judged / 657 legally skipped / 0 gap; skips earn no coverage credit) — 0 `blocking`, 1 `important` (answered), 1 `suggestion`, 1 `question`, 1 `praise`; merge gate `allow`.
  - **Acceptance Reality Check**: `final_path` record copied verbatim — pass 7 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 7; claimed status `Implemented` at check time; ARC verdict `agree`; no fixed item.
  - **Status transition `Implemented → Ready for Review`: allowed** — review evidence exists and the code record has no blocking entry; the registry row 107 and this entry carry the flip.
- **2026-11-25 — clarify stage**: `Related Feature` bound to Feature 107 and the binding ruling recorded in the spec's `## Clarifications`.
- **2026-11-25 — plan stage**: full plan set landed — `plan.md` (23-principle Constitution Check, all pass; 3 load-bearing tensions T-001…T-003 registered as T-019…T-021; Execution Premises EP-001…EP-007 with EP-005 falsified and `resolve-in-scope`; closed BC inventory BC-01…BC-06), `research.md` (16 measured baselines + 8 resolved design points), `data-model.md` (9 entities, 14 invariants), 5 contracts, `quickstart.md` (6 scenarios), `feature-ref.md`. Deterministic gates: pre-analyze `pass` (0 errors / 67 expected advisories), decision-tension validator green, mirror/copy/gate baselines green.

## Key Changes

1. New single owner page `shared/definitions/decision-definitions.md` for the decision vocabulary, class emphases, option contract, record field closure, transmission obligations and the machine/behavior boundary; adjacent owners add pointer lines only.
2. Closed Decision Producer Inventory (P-01…P-12) with `record` / `record-when-decision` / `exempt` obligations and existing carriers; archive-as-projection, no second registry.
3. Two decision classes by holder (`human-interactive` / `ai-autonomous`) with distinct presentation emphases, plus the minimum text bar (full names; `resource_locator` and `same_name_conflict` on same-name risk).
4. Closed, enumerable option sets with five elements, an `other` path and the `forced` degenerate case.
5. Decision block on the existing superagent→subagent payload (seven role fields unchanged) plus acknowledgment and `implementation_receipt`; no silent re-decision; decision → dispatch → receipt audit chain.
6. Machine guards M-01…M-09 with reverse samples and behavior rules B-01…B-07 with named review surfaces; framework sources, instruction pointer section (≤1,500 B), mirrors/per-tool copies, client receipt, legacy read-only tolerance and a plan-owned migration/refusal inventory.

## Implementation Notes

- The Decision Producer Inventory is closed; a producer outside it that emits a decision item is a defect and MUST extend the inventory (FR-003).
- `D-NNN` ids are per-carrier dense and registered in `.specify/register.md` at creation; cross-carrier references carry the carrier pointer; superseded ids stay with a `superseded` mark (FR-015).
- Load-bearing decisions append a decision record that cross-references the `T-NNN` record owned by `shared/guidelines/decision-tension.md`; the six tension fields are never duplicated (FR-017).
- `implementation status` is the implementation-result dimension carried on the record's `transmission_status` surface, driven by the receipt and guarded by M-05 — it is not an additional record field (FR-014's closed set is unchanged).
- Existing records are read-only: new shape for new records, old records parse and report `legacy`; incompatible record-shape changes close through `/speckit.migrate` migration or deterministic refusal (FR-028, FR-029).
- Glossary terms are proposal-only (`origin=auto`, `status=proposed`) until user confirmation (FR-005).

## Future Evolution Suggestions

- A read-only reconstruction runbook/checker for decision archives once real records exist.
- Refine the named review surfaces for B-01…B-07 with real review dispositions.
- Write the glossary proposal into `.specify/glossary.md` after user confirmation.

## Related Files

- Feature Index: `.specify/features.md`
- Feature Detail: `.specify/features/107-decision-governance.md`
- Specification: `.specify/specs/107-decision-governance/requirements.md`
- Quality Checklist: `.specify/specs/107-decision-governance/checklists/requirements.md`
- Adjacent owners (pointer only, no fact moved): `.specify/shared/guidelines/confirmation-gates.md` (046), `.specify/shared/guidelines/decision-tension.md` (076), `.specify/shared/definitions/superagent-definitions.md` (095), `.specify/shared/guidelines/fast-fail.md` (052), `.specify/register.md`, `.specify/shared/definitions/goal-definitions.md`, `.specify/shared/definitions/anchor-definitions.md`
- Cross-referenced Features: `.specify/features/046-confirmation-gate-governance.md`, `.specify/features/053-machine-decidable-artifacts.md`, `.specify/features/076-decision-tension-contract.md`, `.specify/features/090-re-anchoring.md`, `.specify/features/095-superagent-role.md`

## Status Tracking

- **Draft**: requirements 107 is bound and `/speckit.clarify` completed.
- **Planned**: plan/design artifacts exist for the bound spec and the Constitution Check has no unjustified Fail rows. (historical — plan landed 2026-11-25; superseded by Implemented on 2026-11-26)
- **Implemented**: the owner page, instruction section, producer surfaces, payload contract, guards and tests land in framework sources with mirrors regenerated. (reached 2026-11-26 at implement U4; its closure gate and `verification.md` were missing and were supplied by the review, which re-ran the ARC to `accept`)
- **Blocked**: tasks are closed and at least one final-path criterion is not `pass`.
- **Ready for Review**: review evidence exists and the current code-review record has no blocking entry. (current — 2026-11-26: four segments + ARC `accept`; code record 0 blocking)
- **Sealed**: review concluded with zero unhandled P0, acceptance records complete, and merge-back done when slices exist.
- **Completed** (legacy — closed for new work): historical terminal record only; not used for this feature.

## Related Specifications/Requirements

- Specification: `.specify/specs/107-decision-governance/requirements.md`
  Quality Checklist: `.specify/specs/107-decision-governance/checklists/requirements.md`
