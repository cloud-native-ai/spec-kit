# Feature Detail: Batch Decision Panel（批量决策面板）

**Feature ID**: 112
**Name**: Batch Decision Panel（批量决策面板）
**Description**: 决策管理的集中裁决面：一次调用聚合封闭来源清单中的全部待决策项，按 107 完整信息模板逐项呈现，附确定性接地的建议默认值（无证据时明示 `no-evidence`），用户只对异议项发声，其余合格项按建议默认值结案；处置经既有载体记录（knowledge 批次记录 + 107 决策记录 + register 登记 + 来源状态更新），整批可只凭记录重放；只服务人持有的决策，零新存储、零网络、零自动传输。
**Status**: Draft
**Created**: 2026-11-27
**Last Updated**: 2026-11-27

## Overview

Registered as a standalone Feature at the requirements stage (2026-11-27) on line `decision-batch-panel` (run `r20261127T081500Z-112a`). The user's requirement — aggregate every pending decision item, present complete information, attach a recommended default grounded in prior experience, take objections only, and let every uncontested item take its default — is delivered as an additive extension of Feature 107's owner page, not a second decision system.

Scope: one owner-page extension (`shared/definitions/decision-definitions.md`: pending-item form, closed two-source roster, batch presentation and grounding contracts, batch dispositions, batch record contract, batch family fields, P-13 producer row, human/ai boundary, completeness/refusal, replay); one thin command `/speckit.decide` (`templates/commands/decide.md`); one internal skill `decide-batch`; one deterministic stdlib engine `scripts/python/decision-batch.py` with closed actions `scan` / `record` / `replay`; one dated batch record per batch in the existing knowledge store; the existing 107 record grammar extended by three conditional batch-family fields. No new store root, no second registry, no second record schema, no scheduler, no network, no automatic transmission.

Measured baseline (2026-11-27, base `c3489e52c`): the register carries eight open OI-/D-family rows (OI-3, OI-4, OI-7, OI-9, OI-069b-01, OI-073-01, OI-082-01, D-2 (092)); zero `### PENDING —` blocks exist in the four scan roots; the producer inventory ends at P-12; no `decide` command or skill exists. The first honest batch therefore presents those rows as `incomplete` with named missing elements — completing them is the producer/user obligation (A-16), never invented by the panel.

## Latest Review

- **2026-11-27 — requirements stage**: spec authored with FR-001…FR-045 and SC-001…SC-010; the brief's six ambiguities adjudicated in A-3…A-9 plus the heavy-decision shape for silence semantics (A-10); validator `status: ok` (0 error / 0 warning; 408 lines / 55 definition rows / 15 shared strings); `pre-analyze-check --stage requirements` `pass` (0 errors, 7 missing-path advisories naming this feature's not-yet-created deliverables; `fr=45 sc=10`); `decomposition-check --mode plan` `proceed` (45 FR / ceiling 120); workspace guard snapshot + check clean. Evidence: `.specify/specs/112-decision-batch-panel/test-evidence/`.

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

## Future Evolution Suggestions

- A curation capability that drafts a pending-item block from an authority carrier (with evidence pointers) for the user to confirm — a separate decision, because it authors the content the panel must present neutrally (A-16).
- A `/speckit.decide replay` UX refinement or a status view of recent batches — only if a recorded user need appears; no dashboard (A-17).
- Broadening the prior-experience grounding beyond literal subject containment would need a deterministic identity rule, not semantic matching (A-6).

## Related Files

- Feature Index: `.specify/features.md`
- Feature Detail: `.specify/features/112-decision-batch-panel.md`
- Specification: `.specify/specs/112-decision-batch-panel/requirements.md`
- Quality Checklist: `.specify/specs/112-decision-batch-panel/checklists/requirements.md`
- Stage evidence: `.specify/specs/112-decision-batch-panel/test-evidence/requirements-stage-2026-11-27.md`
- Extended owner (pointer only, no fact moved): `shared/definitions/decision-definitions.md` (107)
- Adjacent owners reached by pointer: `shared/guidelines/confirmation-gates.md` (destructive list + gate signals), `shared/guidelines/decision-tension.md` (`T-NNN`), `shared/guidelines/closed-set-claims.md`, `shared/guidelines/user-facing-comprehension.md`, `.specify/register.md` (ID index)
- Batch record store (existing): `.specify/knowledge/` via `scripts/python/memory-utils.py`

## Status Tracking

- **Draft**: requirements 112 bound; spec + quality checklist landed; validator and driver gates green. (current — 2026-11-27)
- **Planned**: plan/design artifacts exist for the bound spec and the Constitution Check has no unjustified Fail rows.
- **Implemented**: tasks are closed and the guard roster lands green.
- **Blocked**: tasks are closed and at least one final-path criterion is not `pass`.
- **Ready for Review**: review evidence exists and the current code-review record has no blocking entry.
- **Sealed**: review concluded with zero unhandled P0, acceptance records complete, and merge-back done when slices exist.
- **Completed** (legacy — closed for new work): historical terminal record only; not used for this feature.

## Related Specifications/Requirements

- Specification: `.specify/specs/112-decision-batch-panel/requirements.md`
  Quality Checklist: `.specify/specs/112-decision-batch-panel/checklists/requirements.md`
- Parent capability (pointer, not a slice relation): Feature 107 Decision Governance — `.specify/features/107-decision-governance.md`
- Parked source: `.specify/todo/20261127-decision-batch-panel.md` (retire at merge per the Park lifecycle)