---
id: "20261030T123438Z-skill-sdd-loop-driver"
unit_id: "skill:sdd-loop-driver"
unit_type: "skill"
run_id: "r20261030T081645Z-078a"
scope: "local"
probe: "skill-sdd-loop-driver-cli-profile"
kind: "internal"
slice: "skills"
feature: "078-bilingual-expression"
partial: false
created: "2026-10-30T12:34:38Z"
summary: "positive"
---

## Review
positive

## Optimization Points
- Unattended 8-stage loop for 078 passed with zero new failures after one closure-repair. Framework friction observed: (1) sdd-requirements-executor run-turn-budget 40 is too small for a 19-FR spec (exhausted after scaffolding); 120 works. (2) doc-consistency-check --action structure scans the whole spec dir and reports pre-existing spec boilerplate as findings; scope it to the delivered path or support a baseline. (3) G-checklist-reader returns operator-level not-applicable, clashing with the 'not-applicable only in face=build sub-row' rule; U4 needs manual adjudication. (4) validate-tasks parallel-safe flags two [P] tasks that only read the same shared path. (5) E2 seq and E3 status are closed domains not stated in dispatch blocks; executors invented values (seq 'E2', status 'review-targeted'). (6) analyze has no E3 status for a read-only stage; the completeness audit counts it unknown. (7) generate-instructions.sh additive reconcile leaves stale section bodies in live instructions, forcing a manual line edit. (8) spec-local [[STR-NNN]] tokens leaked into a shipped template and caused 3 closure failures (neutrality, pointer, section-count); add a shipped-text no-[[STR- token guard. (9) Adding an ambient instructions section requires test_fast_fail_discipline, test_client_guard_sweep and test_user_facing_comprehension_section in the implement targeted set.
