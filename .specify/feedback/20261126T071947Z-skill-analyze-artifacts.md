---
id: "20261126T071947Z-skill-analyze-artifacts"
unit_id: "skill:analyze-artifacts"
unit_type: "skill"
run_id: "r20261126T071500Z-fb"
scope: "local"
probe: "skill-analyze-artifacts-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-11-26T07:19:47Z"
summary: "Analyze worker dispatch carries no output budget: in line 107 a 9-file analyze domain, run without strict output discipline, hit the model's 48k output-token ceiling three times and produced an incomp"
---

## Review
Analyze worker dispatch carries no output budget: in line 107 a 9-file analyze domain, run without strict output discipline, hit the model's 48k output-token ceiling three times and produced an incomplete unit with no findings file (review F5, spine F-OBS-107-3). The mitigation applied in that line — split domains to 2–3 files and enforce "findings file + counts only, no narration" — settled every later worker, but it exists only in the spine, not in the skill, so the next run can silently produce an empty domain that a careless integrator reads as clean.

## Optimization Points
- 1. Add the output-budget clause to the analyze worker dispatch template: 2–3 files per domain and "write the findings file; report counts only, no narration".
- 2. Make an incomplete unit a hard dispatch failure (no findings file or truncated output = FAILED), never an empty result that can be mistaken for a clean domain.
- 3. Record the applied budget in the round record so reuse and re-run decisions can see how much of a domain was actually read.
