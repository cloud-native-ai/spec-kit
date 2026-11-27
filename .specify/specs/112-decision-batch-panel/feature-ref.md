# Feature Reference — Batch Decision Panel（批量决策面板）

**Requirement → Feature**: `112-decision-batch-panel` → **Feature 112** Batch Decision Panel（批量决策面板）
**Status**: Planned (advanced by this plan from Draft; ceiling `Planned`)
**Spec**: `.specify/specs/112-decision-batch-panel/requirements.md` (45 FR / 10 SC, A-1…A-25, 13 clarification rows)
**Plan**: `.specify/specs/112-decision-batch-panel/plan.md`
**Extended owner**: `shared/definitions/decision-definitions.md` (Feature 107) — additive batch extension only

## 1. Binding

Feature 112 is a standalone feature, not a slice of Feature 107. It extends 107's single owner page with the batch decision capability and adds no second owner, registry, store, schema or scheduler. The registry row and the detail file `.specify/features/112-decision-batch-panel.md` are the tracking carriers; this plan advances both to `Planned`.

## 2. Delivery surfaces

| Surface | Path | Form | FR |
|---------|------|------|-----|
| Owner-page extension | `shared/definitions/decision-definitions.md` | additive sections + vocabulary 9 → 17 + P-13 + batch-family conditional layer + batch M/B rows | FR-001…FR-005, FR-011, FR-015…FR-018, FR-032…FR-038, FR-042 |
| Command | `templates/commands/decide.md` | thin entry `/speckit.decide` | FR-039, FR-042 |
| Skill | `skills/internal/decide-batch/SKILL.md` | internal skill: presentation relay + reply capture + engine calls | FR-039 |
| Engine | `scripts/python/decision-batch.py` | stdlib; actions `scan` / `record` / `replay` | FR-039, FR-040 |
| Checker extension | `scripts/python/validate-decisions.py` | field closure + batch-family rule | FR-033, FR-044 |
| Command doc | `docs/reference/commands/decide.md` | entry, actions, exit semantics | FR-043 |
| Framework map | `shared/definitions/framework-map.md` | decision-governance row update (P-13, batch capability, consumers) | FR-042 |
| Probe registry | `shared/definitions/probe-definitions.md` | probe object + bindings for the new skill's wrap-up | FR-042 |
| Fixtures / guards | `tests/fixtures/decision-batch/`, `tests/unit/test_decision_batch_engine.py`, `tests/contract/test_decision_batch_contract.py`, `tests/contract/test_decision_governance_guards.py` (roster), `tests/contract/test_migration_distribution.py` (baseline), `tests/contract/test_probe_nonentity_catalog.py` (census) | red-first guards + reverse samples | FR-044 |

## 3. Mirror and generated-copy map

| Source | Copies | Verify |
|--------|--------|--------|
| `shared/definitions/decision-definitions.md` | `.specify/shared/definitions/decision-definitions.md` | `sync-mirrors.py --check` — no NEW drift vs baseline (rc 0 measured 2026-11-27) |
| `shared/definitions/framework-map.md`, `shared/definitions/probe-definitions.md` | same relative paths under `.specify/shared/` | same |
| `skills/internal/decide-batch/SKILL.md` (new) | `.specify/skills/internal/decide-batch/SKILL.md` | same; wrap-up compiled by `probe-utils.py --action compile-embeds` |
| `scripts/python/decision-batch.py` (new) | `.specify/scripts/python/decision-batch.py` | same; both copies answer `--help` / `--version` |
| `templates/commands/decide.md` (new) | `.claude/commands/speckit.decide.md`, `.github/prompts/speckit.decide.prompt.md`, `.qoder/commands/speckit.decide.md`, `.opencode/command/speckit.decide.md` | `regen-command-copies.py --check` rc 0 before and after regeneration |
| `docs/reference/commands/decide.md` | none (`docs/` is not shipped) | no mirror duty |

## 4. Requirement → design coverage

| FR | Contract clause / plan location |
|----|--------------------------------|
| FR-001 | record-replay C-511 |
| FR-002 | record-replay C-511 |
| FR-003 | record-replay C-511 |
| FR-004 | record-replay C-511 |
| FR-005 | record-replay C-512 |
| FR-006 | source-roster C-101 |
| FR-007 | source-roster C-108 |
| FR-008 | source-roster C-102, C-103 |
| FR-009 | source-roster C-104 |
| FR-010 | source-roster C-105 |
| FR-011 | source-roster C-106; presentation C-207 |
| FR-012 | source-roster C-107 |
| FR-013 | source-roster C-110 |
| FR-014 | presentation C-201, C-206 |
| FR-015 | completeness-refusal C-601, C-602 |
| FR-016 | completeness-refusal C-603, C-606, C-607; source-roster C-109 |
| FR-017 | completeness-refusal C-604 |
| FR-018 | completeness-refusal C-605 |
| FR-019 | presentation C-202 |
| FR-020 | presentation C-203, C-204 |
| FR-021 | default-derivation C-301, C-302 |
| FR-022 | default-derivation C-303, C-304, C-305 |
| FR-023 | default-derivation C-306 |
| FR-024 | objection-reply C-404; default-derivation C-302 |
| FR-025 | presentation C-205 |
| FR-026 | objection-reply C-402, C-403 |
| FR-027 | objection-reply C-401, C-404 |
| FR-028 | objection-reply C-405 |
| FR-029 | record-replay C-510 |
| FR-030 | objection-reply C-408 |
| FR-031 | objection-reply C-409 |
| FR-032 | record-replay C-503; objection-reply C-402 |
| FR-033 | record-replay C-504; objection-reply C-407 |
| FR-034 | record-replay C-505 |
| FR-035 | record-replay C-506 |
| FR-036 | record-replay C-508 |
| FR-037 | record-replay C-501, C-502, C-507 |
| FR-038 | record-replay C-509 |
| FR-039 | completeness-refusal C-608; default-derivation C-307 |
| FR-040 | objection-reply C-406 |
| FR-041 | record-replay C-512; presentation C-207 |
| FR-042 | plan § Project Structure, § Mirror Obligations; record-replay C-511 |
| FR-043 | plan § Source Code (`docs/reference/commands/decide.md`) |
| FR-044 | plan § Source Code tests; every contract's § 守卫义务 |
| FR-045 | presentation C-208; default-derivation C-304/C-307; record-replay C-512 |

## 5. Success-criterion evidence map

| SC | Evidence carrier (planned) |
|----|----------------------------|
| SC-001 | engine scan fixtures (two-source/duplicate/incomplete/autonomous; unreadable register; empty project) + bookkeeping assertions |
| SC-002 | presentation payload slot assertions + incomplete missing-list snapshot + autonomous count zero |
| SC-003 | two grounding fixtures + pointer resolver output (100% resolvable, zero fabricated) |
| SC-004 | four reply-shape batches (one objection / zero objections / abort / non-member) row snapshots + exit codes |
| SC-005 | batch record content + `validate-decisions.py` output + register diff + replay output and broken-pointer exit |
| SC-006 | prior-conflict fixture states + two-record supersession text (old record zero rewrite) + unwritable-carrier refusal |
| SC-007 | exclusion bookkeeping + unattended refusal output + `decision_class` assertions over records |
| SC-008 | presentation text + `/speckit.review` artifact-segment check (behaviour-class, no scorer) |
| SC-009 | `sync-mirrors --check`, `regen-command-copies --check`, fresh `specify init` fixture tree, zero-network/zero-feedback assertions, frozen-baseline test |
| SC-010 | two-scan field comparison (timestamp separated) + duplicate-id refusal + concurrent-path set |

## 6. Dependencies and boundaries

- **Depends on**: Feature 107 (owner page, record grammar, validator, guard roster) and Feature 055 (conflict-free stores / memory engine) as consumed interfaces; neither contributes inherited blockers (plan § Inherited Blockers).
- **Does not touch**: ai-harness 091 or any external decision governance; `.specify/instructions.md` § Decision Items (1,276 B / 1,500 B); `.specify/.gitignore`; the runtime store layout; any second store/registry/schema.
- **Explicit non-goals**: scheduler, notifications, resident scanning, UI/dashboard, automatic authoring of pending items, `ai-autonomous` batch settlement, cross-batch standing defaults, network access, automatic transmission.

## 7. Handoff

Next command: `/speckit.tasks` — decompose the 6 contracts and the guard obligations into dependency-ordered tasks, with red-first fixtures under `tests/fixtures/decision-batch/` and the frozen-baseline / probe-census updates in the same implementation change. Review handoff: B-08/B-09 are the named behaviour-class review surfaces for the batch presentation and the recommendation reason.