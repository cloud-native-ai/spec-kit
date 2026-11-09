---
id: "20261106T094456Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "r20261106T090000Z-086a-r3"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
feature: "086-script-interface-contract"
partial: false
created: "2026-11-06T09:44:56Z"
summary: "086 analyze round 3 (closure): CRITICAL 0 / HIGH 0 / MEDIUM 8 / LOW 10; gate GREEN. Round-2 HIGH H-01..H-04 all closed (SC-012 mutants, feature-ref FR map, FR-028 tombstone citation, sandbox exit 1). "
---

## Review
086 analyze round 3 (closure): CRITICAL 0 / HIGH 0 / MEDIUM 8 / LOW 10; gate GREEN. Round-2 HIGH H-01..H-04 all closed (SC-012 mutants, feature-ref FR map, FR-028 tombstone citation, sandbox exit 1). Residual: data-model E-4 payload drift, exception-limb count 3 vs 4, 73-vs-81 unpaired mirrors, stale validator residue 73 vs 62, quickstart mirror-as-exempt, T067/C-4 claim misalignment, version-resolution wording, FR-005/FR-029 traceability rows

## Optimization Points
- E-4 omits mode/root/projection[] and rule.findings; recomputation limbs 3 (C-30/T069) vs 4 (FR-020b); requirements 73 vs measured 81 unpaired .specify copies; validator residue 73 (66/4/2/1) vs 62 (55/4/2/1) in tasks Notes + features.md + features/086.md; quickstart exempt includes projected mirror (contradicts C-6); T067 claims C-4 while enumerating C-3 three non-criteria and T032 claims C-3 with FR-002/009/010; C-8 'own directory' vs EP-005/SC-011 root pyproject read; traceability FR-005/FR-029 -> T070/T071/T072
