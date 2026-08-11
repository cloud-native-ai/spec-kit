---
id: "20260811T182415Z-speckit-implement"
unit_id: "/speckit.implement"
unit_type: "command"
run_id: "038-goal-target-20260812-implement"
scope: "local"
feature: "038-goal-target"
partial: false
created: "2026-08-11T18:24:15Z"
summary: "Full 038 implementation run: 32/32 tasks across 7 phases, test-first throughout (unit data layer → CLI contract → structural template pins → fold/milestone integration), every claim evidence-backed wi"
---

## Review
Full 038 implementation run: 32/32 tasks across 7 phases, test-first throughout (unit data layer → CLI contract → structural template pins → fold/milestone integration), every claim evidence-backed with fresh command output. Phase-boundary name-level regression diffs stayed empty except one residue-attributed item. Gate.yaml pre-checked per phase; mirrors fanned exclusively via sync-mirrors.py; quickstart walked end-to-end twice (first-run + refresh-verify). Smooth run; two process optimizations noted.

## Optimization Points
- ## Optimization Points
- **Full-suite residue should be cleaned before the baseline freeze, not discovered after**: the baseline run itself generated `__pycache__`/integration fixtures that later surfaced as two order-dependent failures; a pre-run residue sweep (`find skills .specify/skills -name __pycache__ -o -name 'layout-int-*'`) belongs in the T001 task text so attribution costs nothing at phase boundaries.
- **Per-phase full-suite re-runs are expensive for a 32-task run**: phase-boundary regression can run only the touched test families (goal/team/fold suites) and reserve the full suite for the final gate — the name-level `comm -13` discipline stays intact because the final run still diffs against the frozen baseline.
