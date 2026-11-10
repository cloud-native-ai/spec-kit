# Feature Reference — 081

**Requirement key**: `081-acceptance-hardening`
**Bound Feature**: **Feature 081** — 更严格的验收与产物审查（Stricter Acceptance & Artifact Review）
**Feature index row**: `.specify/features.md` (row `| 081 |`, same-pass `Total Features` recomputation)
**Feature detail**: `.specify/features/081-acceptance-hardening.md`
**Binding basis**: `/speckit.clarify` Mode A on 2026-11-03 scanned the registry and found no owner — the pre-existing candidates (Feature 026 is "Agent Skill Enablement", 055 is storage-conflict, 062 is Humanize, 071 governs only the *existing two-segment* review composition, 077 governs document-stage gates, 079 governs bilingual expression) do not cover the combination "final-path threshold + smoke hard condition + one shared verdict across three call sites + artifact/implementation review". Decision: **create**, recorded in `requirements.md` § Clarifications § Session 2026-11-03 (including why the ID is 081 rather than the next empty slot).

## How this plan maps onto the Feature

| Feature element | This plan's carrier |
|---|---|
| Status transition owned by this stage | `Draft → Planned` only; `plan.md`, `data-model.md`, `contracts/` (5 files), `quickstart.md`, `research.md`, this file are the artifacts that satisfy the `Draft → Planned` row (plus a Constitution Check with no unjustified Fail) |
| Key changes (7 items in the feature detail) | `plan.md` § Summary + § Design Decisions D1–D10; the requirement mapping is in `contracts/*.contract.md` § Traceability |
| Implementation notes | `plan.md` § Design Decisions (the "why", including the rejected alternatives) and `data-model.md` (the invariants) |
| Related files | `requirements.md` (25 FR / 9 SC / 17 STR), `checklists/requirements.md`, `baseline-failed.txt`, `test-evidence/` |
| Feature's own new thresholds (self-application) | This feature's `final`-path SCs are SC-001 and SC-002; its smoke is `bash scripts/bash/run-tests.sh tests/integration/test_acceptance_smoke.py -q`. The feature cannot reach `Implemented` until both are true — i.e. Feature 081 is the first feature gated by the rules it delivers |

## Delivery surface (what the Feature row's "Last Updated" will have to report)

- **New files**: `shared/workflow/acceptance-hardening.md`, `scripts/python/closure-acceptance-check.py`, `skills/internal/review-feature-quality/SKILL.md`, `tests/contract/{test_closure_acceptance_check,test_acceptance_state_machine,test_acceptance_premises,test_acceptance_review_composition,test_line_state_blocked,test_gate_wiring_081,test_acceptance_schema_ownership}.py`, `tests/integration/test_acceptance_smoke.py`, `tests/fixtures/acceptance-hardening/**`.
- **Edited framework sources**: `templates/{feature-details,verification-log,tasks,feature-index,plan,review}-template.md`, `templates/commands/{review,implement,tasks,checklist}.md`, `shared/workflow/{feature-integration,expression-gates}.md`, `skills/internal/{review-sdd-process,manage-features,implement-feature,code-review}/SKILL.md`, `skills/external/sdd-loop-driver/{SKILL.md,references/stage-prompts.md,references/dispatch-recipes.md,skills/external/sdd-loop-driver/scripts/pre-analyze-check.py,skills/external/sdd-loop-driver/scripts/line-registry.py,skills/external/sdd-loop-driver/scripts/integrate-lines.py}`, `scripts/python/validate-requirements.py`, `src/specify_cli/__init__.py`, `docs/reference/commands/review.md`, `CHANGELOG.md`, `.specify/instructions.md` (§ Key Directories).
- **Deliberate guard updates** (7): `test_review_code_composition.py`, `test_review_feedback_boundary.py`, `test_skill_layer_visibility_guards.py`, `test_expression_compatibility.py`, `test_migration_distribution.py`, `test_measurement_instruments.py`, `test_requirements_checker.py` — each with its reason in `research.md` § R3; none is deleted or silenced.
- **Regeneration entries** (2): `python3 scripts/python/regen-command-copies.py`, `python3 scripts/python/sync-mirrors.py` (both then `--check`).
- **No new**: command, runtime dependency, gate registry row, checker script beyond the one above, storage, or service.

## Slices

The natural task count (~52) exceeds the ceiling of 40, so the implementation is sliced `081a` (US1 + shared core) → `081b` (US2) → `081c` (US3) → `081d` (US4 + remaining wiring). No FR or SC is dropped by the slicing; the per-slice assignment table lands in `tasks.md` (see `plan.md` § Design Decisions D10).
