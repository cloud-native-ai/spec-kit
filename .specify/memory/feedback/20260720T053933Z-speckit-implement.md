---
id: "20260720T053933Z-speckit-implement"
unit_id: "/speckit.implement"
unit_type: "command"
run_id: "031-task-complexity-rubric-implement-20260720T133933"
scope: "local"
feature: "031-task-complexity-rubric"
partial: false
created: "2026-07-20T05:39:33Z"
summary: "Clean TDD implementation run. Red: authored tests/contract/test_task_complexity_rubric.py (10/10 fail, section absent). Green: inserted the ## Task Complexity Rubric section into templates/instruction"
---

## Review
Clean TDD implementation run. Red: authored tests/contract/test_task_complexity_rubric.py (10/10 fail, section absent). Green: inserted the ## Task Complexity Rubric section into templates/instructions-template.md and dual-wrote a byte-identical mirror to .specify/templates/; contract test 10/10 pass (C-1..C-10). Verified SC-001 via the generator render path, SC-002/FR-010/FR-011 via before/after fixture diffs (additive-only insert; user-customized rubric preserved). Full suite 720P/106F/13E/1S = +10 passed, zero new failures vs the recorded baseline. Pre-Status-Flip Gate passed (0 open tasks; SC-001..005 rows; deferred_tasks=T013). Advanced Feature 032 -> Implemented in features.md + features/032.md; DoD flipped green. Honored the plan's Principle IX decision — no edits to templates/commands/instructions.md or per-tool mirrors.

## Optimization Points
- End-to-end SC-001 verification of a template-render feature is awkward: running the real generate-instructions.sh from a throwaway CWD fails under `set -e` because refresh-tools.sh resolves tools-utils.py relative to CWD (not the repo scripts dir) and aborts BEFORE the render step (line 94). The check had to fall back to reproducing render_template() by hand. /speckit.implement (or the generator) should offer an isolated "render-only"/dry-run path — or make the tool-manifest generation non-fatal / repo-anchored — so instruction-template features can be verified in a temp workspace without reimplementing the render.
