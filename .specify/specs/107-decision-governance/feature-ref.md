# Feature Reference — 107-decision-governance

**Requirement → Feature**: `107-decision-governance` → **Feature 107 Decision Governance（AI Agent 决策项治理）**
**Spec**: `.specify/specs/107-decision-governance/requirements.md` · **Index row**: `.specify/features.md` (row `107`) · **Detail**: `.specify/features/107-decision-governance.md`

## 1. Binding

Feature 107 was created at `/speckit.clarify` (2026-11-25) as a **standalone** feature — not a slice of any adjacent owner. The binding ruling and the candidate analysis (046 / 076 / 053 / 095 / 090) are recorded in `requirements.md` § Clarifications; the feature detail carries the ruling summary. This plan maps entirely onto Feature 107; it introduces no additional Feature and deprecates or merges none.

## 2. What this plan delivers

| Deliverable | Path | Role in the feature |
|---|---|---|
| Decision owner page (new) | `shared/definitions/decision-definitions.md` | Single owner of vocabulary, classes, text/option contracts, record closure, archive inventory, transmission, M/B boundary, legacy rules |
| Pointer lines | `shared/definitions/framework-map.md`; `shared/guidelines/{confirmation-gates,decision-tension,fast-fail}.md`; `shared/definitions/{superagent,goal,anchor,agent}-definitions.md` | Adjacent owners keep their facts; each gains one pointer (FR-002) |
| Producer surfaces | `skills/internal/run-agent/SKILL.md`; `skills/internal/run-team/SKILL.md`; `skills/external/sdd-loop-driver/references/{checkpoint-protocol,dispatch-recipes,stage-prompts}.md`; `skills/internal/{analyze-artifacts,review-feature-quality,review-sdd-process}/SKILL.md` | P-04/P-05/P-06/P-09 carriers and B-rule review surfaces |
| Ambient instruction section | `templates/instructions-template.md` → generated `.specify/instructions.md` | Two production rules + class emphasis + owner pointer, ≤1,500 B (A-13) |
| Budget ruling | `scripts/bash/generate-instructions.sh` | `INSTRUCTIONS_BUDGET_BYTES` 38,912 → 40,960 (T-001) |
| Deterministic checker (new) | `scripts/python/validate-decisions.py` | M-01…M-08 judge; read-only; script-interface contract |
| Docs pointer | `docs/concepts/spec-driven.md` | One pointer line to the owner page (FR-030) |
| Guard suites (new) | `tests/fixtures/decision-governance/`; `tests/unit/test_validate_decisions.py`; `tests/contract/test_decision_governance_{guards,contracts,migration_map}.py`; `tests/integration/test_decision_governance_migrate_dryrun.py` | Red-first M-rule fixtures with reverse samples; BC-row mapping; migrate dry-run |

## 3. Delivery surfaces declared for the overlap pre-check

Shared delivery roots this plan writes (repo-relative; pointer-only touches marked `→pointer`):

```text
shared/definitions/decision-definitions.md
shared/definitions/framework-map.md
shared/guidelines/confirmation-gates.md            # →pointer
shared/guidelines/decision-tension.md              # →pointer
shared/guidelines/fast-fail.md                     # →pointer
shared/definitions/superagent-definitions.md       # →pointer
shared/definitions/goal-definitions.md             # →pointer
shared/definitions/anchor-definitions.md           # →pointer
shared/definitions/agent-definitions.md            # →pointer
skills/external/sdd-loop-driver/references/checkpoint-protocol.md   # →pointer
skills/external/sdd-loop-driver/references/dispatch-recipes.md      # →pointer
skills/external/sdd-loop-driver/references/stage-prompts.md         # →pointer
skills/internal/run-agent/SKILL.md
skills/internal/run-team/SKILL.md
skills/internal/analyze-artifacts/SKILL.md         # →pointer
skills/internal/review-feature-quality/SKILL.md    # →pointer
skills/internal/review-sdd-process/SKILL.md        # →pointer
templates/instructions-template.md
scripts/bash/generate-instructions.sh
scripts/python/validate-decisions.py
docs/concepts/spec-driven.md                       # →pointer
```

**Overlap posture**: a `same-path` hit on a `→pointer` file is expected and already adjudicated by the architecture: the **existing feature remains the owner** of that path and its facts; Feature 107 adds a pointer line only (FR-002, A-2) and must not change the owner's criteria tables. A hit on a non-pointer path (new files) has no prior owner. The post-plan `overlap-check.py` reading is recorded in this stage's evidence.

**Measured post-plan reading (2026-11-25)**: `overlap-check.py --spec-dir .specify/specs/107-decision-governance` → `decision=overlap`, `overlaps=117`, all against **long-completed** features (no active parallel line in this worktree carries a spec dir). Two classes only: (i) `same-path` on owner files this feature touches by pointer or by one additive section — the existing feature stays the owner and 107 changes no owner criterion; (ii) `nested-path` from the new `scripts/python/validate-decisions.py` and the driver-reference files against predecessors that declared a parent directory token (`scripts/python`, `skills/external/sdd-loop-driver`) — the new files have no prior owner. The overlap pre-check is a clarify-stage gate and ran `clear` there (no declaration artifact existed); this reading is the driver's dated record, and the disposition is the ownership split above. Surfaces are not removed: the pointer-only landing is mandated by FR-002/FR-026, and removing it would contradict the spec.

## 4. Mirror map

| Framework source | Runtime mirror / generated copy |
|---|---|
| `shared/**` (page + pointer files) | `.specify/shared/**` |
| `skills/external/**`, `skills/internal/**` | `.specify/skills/**` |
| `templates/instructions-template.md` | `.specify/templates/instructions-template.md`; generated `.specify/instructions.md` (+ per-tool instruction symlinks) |
| `scripts/bash/generate-instructions.sh`, `scripts/python/validate-decisions.py` | `.specify/scripts/**` (strict pair; projected guard block preserved) |
| `docs/**` | none — not shipped |

## 5. Compatibility and migration

The closed inventory is `plan.md` § Backward-Incompatible Change Inventory (BC-01…BC-06). All rows are compatibility bridges; BC-02 adds a deterministic refusal at payload construction, and BC-04 rides `/speckit.migrate`'s existing `templates-generated` dimension. No new migrate dimension, no retroactive rewrite of the base corpus, no fallback-only resolution.

## 6. Handoff

- **Next stage**: `/speckit.tasks` decomposes this plan; the red-first fixtures and contracts above become task rows.
- **Plan-stage evidence**: `test-evidence/` (baselines, gates, targeted-set stage-status row, stage record).
- **Open item for the tasks stage**: none — all design obligations are resolved in `plan.md` / `contracts/`; the plan's own load-bearing decisions use `T-NNN` because the `D-NNN` contract binds only post-landing records (A-10).
