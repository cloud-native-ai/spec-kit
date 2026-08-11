---
id: "20260811T145026Z-speckit-clarify"
unit_id: "/speckit.clarify"
unit_type: "command"
run_id: "038-goal-target-clarify-2026-08-11"
scope: "local"
feature: "038-goal-target"
partial: false
created: "2026-08-11T14:50:26Z"
summary: "Mode A run on 038-goal-target. Coverage scan found one material ambiguity (terminal Target reference path after preview confirmation) resolved via one closed question with a user-custom ruling (review"
---

## Review
Mode A run on 038-goal-target. Coverage scan found one material ambiguity (terminal Target reference path after preview confirmation) resolved via one closed question with a user-custom ruling (review bifurcation: genuine terminal -> report-and-end; evidence contradiction -> reopen via /speckit.goal then re-issue). Integrated into US2 scenario 3 + FR-009, appended Session 2026-08-11 row. Also caught and fixed an internal cross-reference defect (FR-009 cited FR-016 where FR-017 carries the option-name collision constraint). Two plan-phase deferrals (engine action names, CLI option spelling) left as-is per house convention — they are plan-level decisions, not requirement ambiguities.

## Optimization Points
- Mode A clarification on a spec that already carried five legacy loose-bullet clarifications: the taxonomy mandates new entries under `### Session YYYY-MM-DD` but is silent on how to coexist with pre-session-format rows. Resolution was append-only (leave legacy rows, add session heading). The taxonomy could state this coexistence rule explicitly to prevent agents from "normalizing" history rows into session headings (a rewrite hazard).
