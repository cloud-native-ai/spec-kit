---
id: "20261110T155453Z-skill-code-review"
unit_id: "skill:code-review"
unit_type: "skill"
run_id: "r20261110T081104Z-b097"
scope: "local"
probe: "skill-code-review-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-11-10T15:54:53Z"
summary: "Text-mode code review of 123 files: 97 judged, 26 skipped (generated), 0 gap. Counts: blocking 1 (us2:273 unfailable zero-write test), important 2 (help zero-side-effect limb; -h contract/docs drift),"
---

## Review
Text-mode code review of 123 files: 97 judged, 26 skipped (generated), 0 gap. Counts: blocking 1 (us2:273 unfailable zero-write test), important 2 (help zero-side-effect limb; -h contract/docs drift), suggestion 8, nitpick 1, praise 1. Merge gate deny (exit 1).

## Optimization Points
- The receipt verdict precedence is documented but the printed summary does not say which rule fired when both a blocking entry and skips exist.
- First-write receipts treat every unmatched changed file as reviewed; there is no way to mark a specific file deliberately out of scope with a reason outside the five legal skip values.
