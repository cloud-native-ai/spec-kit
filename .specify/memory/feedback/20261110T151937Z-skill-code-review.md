---
id: "20261110T151937Z-skill-code-review"
unit_id: "skill:code-review"
unit_type: "skill"
run_id: "r20261110T055657Z-b095-review"
scope: "local"
probe: "skill-code-review-wrapup"
kind: "internal"
slice: "skills"
feature: "095-superagent-role"
feature_id: "095"
partial: false
created: "2026-11-10T15:19:37Z"
summary: "Code segment over b3da3a26d..6c48e9c25: 313 changed files, 13 judged, 300 skipped with legal reasons, 0 gaps; 2 blocking, 6 important, 5 suggestion, 1 praise; gate deny (blocking-unresolved); capture "
---

## Review
Code segment over b3da3a26d..6c48e9c25: 313 changed files, 13 judged, 300 skipped with legal reasons, 0 gaps; 2 blocking, 6 important, 5 suggestion, 1 praise; gate deny (blocking-unresolved); capture skipped under the framework hat; 44 uncommitted paths disclosed and not concluded over.

## Optimization Points
- The script help says four steps while the skill says five (capture); update the usage text so the non-interactive path has one census.
- The 18 red guards from the in-range digest redesign were masked by the reconstructed baseline; a baseline built after in-range commits must disclose per-module guard health.
- token-efficiency: the 313-file changed set contained 300 non-code/generated paths; the skip selectors classified them programmatically instead of opening them — keep that path the default for large doc-heavy deltas.
