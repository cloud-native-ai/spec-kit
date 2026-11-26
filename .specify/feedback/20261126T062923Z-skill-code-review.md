---
id: "20261126T062923Z-skill-code-review"
unit_id: "skill:code-review"
unit_type: "skill"
run_id: "r20261125T134500Z-107a"
scope: "local"
probe: "skill-code-review-wrapup"
kind: "internal"
slice: "skills"
feature: "107-decision-governance"
feature_id: "107"
partial: false
created: "2026-11-26T06:29:23Z"
summary: "Code segment of 107-decision-governance at base fbab7a45c..head 3f0200b42 (feature-first-commit), renderer text. Receipt: changed 684 / judged 27 / skipped 657 / gap 0; segment not-evaluated (skips ea"
---

## Review
Code segment of 107-decision-governance at base fbab7a45c..head 3f0200b42 (feature-first-commit), renderer text. Receipt: changed 684 / judged 27 / skipped 657 / gap 0; segment not-evaluated (skips earn no coverage credit); merge gate allow (0 blocking; 1 important answered, 1 suggestion, 1 question, 1 praise). Judged set = the feature's own code and test surfaces plus pointer-shaped edits; the line-106 merge scope was legally skipped (size-guard focus) with the 106 record cited and byte-identity verified for 321/322 files.

## Optimization Points
- 1. start recorded base/head from --spec (feature-first-commit), but receipt invoked without --spec re-resolved a different base and hit an unrelated binary (.specify/archive/.../wbs.png) before any skip selector applied; receipt/note should carry the record's resolved range instead of silently re-resolving, or warn when the pair differs from the header. 2. The any-skip -> not-evaluated rule makes an honest mixed delta unable to assert pass; a per-class coverage reading (code-path files vs records vs generated) would let the code conclusion stand on what it judged. 3. The inventory action's observed set augments scan hits with declared-path existence (validate-decisions.py:1064-1071); a declared face that stops referencing the owner page while its file remains is still counted observed — make observation strict or document the augmentation. 4. The generator's budget-raise comment records 1,274 B while the section measures 1,276 B.
