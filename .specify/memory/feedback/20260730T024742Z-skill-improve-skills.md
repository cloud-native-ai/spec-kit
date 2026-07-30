---
id: "20260730T024742Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "improve-skills-20260730-create-team-presets"
scope: "local"
partial: false
created: "2026-07-30T02:47:42Z"
summary: "Improved create-team by resolving the capacity-vs-responsibility ownership boundary between the two agent-template sets and adding a predefined team-preset library with a deterministic matcher, driven"
---

## Review
Improved create-team by resolving the capacity-vs-responsibility ownership boundary between the two agent-template sets and adding a predefined team-preset library with a deterministic matcher, driven by explicit user emphasis plus a fresh evidence run (no prior evidence existed for either skill; session lane Unobserved, runs lane Exercised for 2 real teams). All three presets were distilled from real evidence (draft/Code Workspace.md session + the two teams' run reports). Matcher was executed against 5 goals before wiring. Zero test regression proven by a clean-worktree failure-set diff (84 == 84 identical).

## Optimization Points
- The stash-based baseline failure-set diff mandated by step 6 is unsafe in this repo: a concurrently running continuous team (`requirement-implement-monitor`) writes into `.specify/teams/` mid-run, which blocked `git stash pop` and left a redundant stash entry. improve-skills should prefer a clean `git worktree add <tmp> HEAD` for the baseline run — it is read-only with respect to the working tree and immune to concurrent writers — and mention stash only as a fallback when worktrees are unavailable.
- Step 3's analysis groupings have no bucket for "two sibling skills own overlapping artifact types with no documented boundary". This run's root cause was ownership ambiguity between `create-agent/templates/` (capacity) and `create-team/templates/` (responsibility), not any single failing step. Adding a "cross-skill ownership boundary" failure mode would let the analysis reach that class directly instead of arriving at it from user emphasis alone.
- Step 4's "codify deterministic logic" guidance covers extracting prose into scripts, but says nothing about the complementary move used here: when a skill repeatedly re-derives a whole artifact shape from vague user input, the fix is a **preset/template catalog plus a deterministic matcher**, not a longer prose decision tree. Naming that pattern would make it reachable in future loops.
