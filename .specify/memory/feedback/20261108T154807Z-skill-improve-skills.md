---
id: "20261108T154807Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "improve-skills-sdd-batch-20261108T154752Z"
scope: "local"
probe: "skill-improve-skills-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-11-08T15:48:07Z"
summary: "Batch improvement of sdd-* skills: run artifacts now archive under the target project's .specify/ (housekeeping reports -> .specify/memory/housekeeping/; loop-driver local brief -> .specify/.tmp/sdd-l"
---

## Review
Batch improvement of sdd-* skills: run artifacts now archive under the target project's .specify/ (housekeeping reports -> .specify/memory/housekeeping/; loop-driver local brief -> .specify/.tmp/sdd-loop/tmp/<line_id>/). Gates: skill-shape exit 0 (4961->4987/5000), redline pass, 82 focused contract tests pass; one pre-existing baseline failure reproduced at HEAD.

## Optimization Points
- HK-1 report store registered in framework-map; LD-1 brief path aligned with HR11; PS-1 has no persistent files (no change); deferred remote dispatch scratch under /home/<run-user>/ (shared dispatch owner); open: housekeeping/ not yet in the retention closed roster.
