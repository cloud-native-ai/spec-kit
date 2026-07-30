# Feature 039: Harvested Harness Improvements

## Overview

Twelve improvements (P1–P12) harvested from the 10 reference open-source projects in the `/cws_work` workspace, identified by the `cws-workspace-cluster` insight-harvest team (cycle 1 report: `.specify/teams/cws-workspace-cluster/runs/20260730T094500Z-report.md`) and adopted in three phases on 2026-07-30.

## Key Changes

### Phase 1 — small doc/template edits
- **P4** (superpowers + intellegix): `templates/commands/implement.md` evidence-backed closure upgraded to a Gate Function (IDENTIFY→RUN→READ→VERIFY→CLAIM, fresh output in the claiming message, "should pass" banned); `templates/tasks-template.md` gained a `## Completion Gate` section (GATE-N rows) re-validated before completion with a 3-strike rejection escalation.
- **P9** (superpowers): description = capability + triggers only, never a workflow summary — `templates/skills-template.md`, `create-skills` SKILL + quality checklist.
- **P11** (loop-engineering): operating-loops.md L1→L2 gate 5 "cannot self-mark green" — promotion evidence from run-log machine aggregation, improve-team re-runs verification itself.
- **P8** (ai-website-cloner-template): `generate_commands()` now prepends AUTO-GENERATED markers to every per-tool command copy.

### Phase 2 — medium mechanisms
- **P1** (ai-website-cloner-template): `scripts/python/sync-mirrors.py` — single-source fan-out for templates/skills/agents/scripts/shared + delegated command regen; `--check` CI gate (exit 2 on drift); Tool record `.specify/memory/tools/sync-mirrors.py.md`; Mirror-sync map in instructions rewritten around it.
- **P2** (loop-engineering + intellegix + claw-code-agent): `templates/gate-template.yaml` → `.specify/gate.yaml` + `scripts/python/gate-check.py` (deny>confirm>allow, exit 0/1/2/3); wired into implement.md step 6 and operating-loops ACT step.
- **P3** (superpowers): pressure-test TDD (RED-GREEN-REFACTOR) — new `create-skills/references/pressure-testing.md`, step 6.5 in create-skills, behavior-edit re-test rule in improve-skills.
- **P5** (claude-code-py code-review plugin): finding-validation subagent pass in analyze.md (§5.5) and review.md (§4.5) — CRITICAL/HIGH/P0 findings independently confirmed; DO-NOT-FLAG noise lists; rejected findings go to an Unvalidated appendix.
- **P10** (better-harness Loop Spec Card): `## Loop Card` (WHEN→SEE→DO→CHECK→STOP→LEAVE) optional in skills-template, REQUIRED in team Dynamic Structure for iteration/continuous patterns.

### Phase 3 — structural
- **P6** (learn-claude-code s12 + OpenSpec): task DAG — `[blockedBy: Txxx]` tag (tasks-template grammar + tasks.md format component 6), `[>]` claim sigil for multi-agent runs, topological execution in implement.md step 5.
- **P7** (learn-claude-code s18 + intellegix): optional `isolation: worktree` for parallel teams — per-writer worktrees, Lead-only merge, conflict = repartition signal, dirty-tree refusal (create-team SKILL + parallel orchestration template).
- **P12** (claude-code-py ralph-wiggum): implement Long-Run Mode — `implement-loop.local.md` state file, max_iterations cap, 2-strike stagnation exit, Completion-Gate-green as the only success promise; pure prompt flow (works on all 8 supported tools).

## Implementation Notes

- Test baseline discipline: 38 pre-existing failures recorded before changes; all three phases verified 38F/1040P — zero new failures.
- All mirrors synced via the new sync-mirrors.py itself (dogfooded during its own rollout); `--check` exits 0.
- gate-check.py verdicts unit-verified (allow/deny/confirm/mixed/stdin; dotfile normalization bug found and fixed during verification).
- Sources analyzed at pinned HEADs (see team STATE.md roster); per-point evidence paths in the cycle report.

## Status Criteria

Implemented: all 12 points landed with mirrors synced and zero test regressions. Follow-ups deferred to usage: first pressure-test run on a real new skill, first worktree-isolated team run, first long-run implement session.
