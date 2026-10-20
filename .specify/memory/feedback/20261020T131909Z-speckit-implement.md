---
id: "20261020T131909Z-speckit-implement"
unit_id: "/speckit.implement"
unit_type: "command"
run_id: "063-postreview-repair-20261020"
scope: "local"
probe: "speckit-implement-wrapup"
kind: "internal"
slice: "commands"
feature: "063-sdd-loop-efficiency"
partial: false
created: "2026-10-20T13:19:09Z"
summary: "Post-review repair of 063-sdd-loop-efficiency. Fixed P0 F1 (audit denominator), P1 F2 (closure pending rules), P1 F3/F7 (dispatch observability + durable evidence) and P1 F6 (watcher determinism). The"
---

## Review
Post-review repair of 063-sdd-loop-efficiency. Fixed P0 F1 (audit denominator), P1 F2 (closure pending rules), P1 F3/F7 (dispatch observability + durable evidence) and P1 F6 (watcher determinism). The dated efficiency case study notes/efficiency-case-study-2026-10-20.md records 063 wall-clock ~20.5h, three analyze runs and three repair passes. Markers: sdd-loop-efficiency, token-efficiency.

## Optimization Points
- Add a large-feature decomposition gate before plan (>30 FR or >40 tasks must split into subfeatures instead of driving one oversized full chain).
- Add a cross-feature overlap pre-check at requirements/clarify for shared skill assets, CLI profiles, and probe objects; the 063/064 late overlap caused repair churn.
- Commit per task group; keep stream-json/grace; treat TIMEOUT as a budget verdict, not a kill signal; treat hook timeouts as non-blocking warnings.
- Move deterministic checks (counts, references, clause/task mapping) earlier into requirements/plan/tasks to reduce analyze repair loops.
- Dogfood the two-slot test budget with targeted sets between the two full runs, and pin the audit denominator with missing/empty evidence cases (063 F1 fix).
- Keep independent review: it found a real P0; do not merge with a P0 open.
- token-efficiency: 063 wall-clock was about 20.5h, dominated by full-suite runs, long subagent stages and three analyze/repair passes; decomposition and earlier machine checks are the main savings.
- sdd-loop-efficiency: the dated case study is .specify/specs/063-sdd-loop-efficiency/notes/efficiency-case-study-2026-10-20.md.
