---
id: "20261106T045642Z-skill-analyze-artifacts"
unit_id: "skill:analyze-artifacts"
unit_type: "skill"
run_id: "r20261106T033959Z-086a"
scope: "local"
probe: "skill-analyze-artifacts-wrapup"
kind: "internal"
slice: "skills"
disposition: "ignored"
partial: false
created: "2026-11-06T04:56:42Z"
summary: "analyze read-only pass: coverage accountant red (fr-uncovered 0/33, status=uncovered, 33 errors); findings 1 CRITICAL / 5 HIGH / 12 MEDIUM / 7 LOW; 085 diff empty; no source/template/test edits; CRITI"
disposition_reason: "introspection:introspection-20261106T084116Z#Excluded"
---

## Review
analyze read-only pass: coverage accountant red (fr-uncovered 0/33, status=uncovered, 33 errors); findings 1 CRITICAL / 5 HIGH / 12 MEDIUM / 7 LOW; 085 diff empty; no source/template/test edits; CRITICAL/HIGH validation via direct evidence re-read (subagent dispatch unavailable), driver verifier pending

## Optimization Points
- C-01 contracts carry no (FR-NNN) citation groups; H-01 CHK017 FR-027/FR-030 carve-out vs C-041/GATE-5/M-16; H-02 CHK036 inherited PYTHONPATH breaks every run-derived SC; H-03 mutation legs M-8..M-15/M-18/M-19 unassigned and T042 inverted; H-04 baseline slot taken after T007/T008; H-05 nine full-suite runs vs two-slot budget; M-01 CHK007 two-pass no FR; M-02 CHK008 mode line no FR; M-03 C-044..C-050 carrier mapping wrong; M-04 C-014 omits pass count; M-05 T010 corrupted command; M-06 plan count/reference drift; M-07 FR-017 no carrier; M-08 Phase 7 empty; M-09 registry stage record stale; M-10 T032 S-3 misreference; M-11 WP-C2 additive assertion missing; M-12 SC-001 magnitude; M-13 C-037/C-038 no FR parent
