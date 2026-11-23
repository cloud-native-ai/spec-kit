---
id: "20261123T023550Z-skill-git-utils"
unit_id: "skill:git-utils"
unit_type: "skill"
run_id: "git-closeout-feature-compare-20261123"
scope: "local"
probe: "skill-git-utils-wrapup"
kind: "internal"
slice: "skills"
feature_id: "091"
partial: false
created: "2026-11-23T02:35:50Z"
summary: "Committed and pushed the registry artifacts and records to github, gitlab and gitee at 7d8201ba1. Compared 100 shared IDs plus eight AI-only rows, verified all eight capability families exist in spec-"
---

## Review
Committed and pushed the registry artifacts and records to github, gitlab and gitee at 7d8201ba1. Compared 100 shared IDs plus eight AI-only rows, verified all eight capability families exist in spec-kit, and confirmed 078 is 12 failed / 21 passed in both repositories. No ai-harness files were modified; unresolved red remains declared and no full-suite claim was made.

## Optimization Points
- token-efficiency: normalized ID/status/spec-path comparison should precede semantic reading; the 81 differing descriptions are not 81 capability differences, so only the eight AI-only rows and the few load-bearing field conflicts required full detail reads.
- Run each repository's test command with an explicit target-directory change. The first 078 check ran in spec-kit rather than ai-harness; this was caught with `pwd` and corrected before any comparison claim, avoiding wrong-repo evidence.
