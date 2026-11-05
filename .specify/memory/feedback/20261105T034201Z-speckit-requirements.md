---
id: "20261105T034201Z-speckit-requirements"
unit_id: "/speckit.requirements"
unit_type: "command"
run_id: "r20261105T033420Z-082a"
scope: "local"
probe: "speckit-requirements-wrapup"
kind: "internal"
slice: "commands"
feature: "082-mechanism-policy-separation"
partial: false
created: "2026-11-05T03:42:01Z"
summary: "082 requirements: user entry distilled into a mechanism/policy separation principle for the meta-layer (create-skills/improve-skills/merge-skills/coaching-skills routed by a single predicate); 18 FR /"
---

## Review
082 requirements: user entry distilled into a mechanism/policy separation principle for the meta-layer (create-skills/improve-skills/merge-skills/coaching-skills routed by a single predicate); 18 FR / 5 SC / 3 STR; validator ok; pre-analyze pass (3 expected advisories); decomposition proceed (18/30); flow-class declaration execution. Attempt 1 hit the instance's 40-turn budget; a 120-turn executor completed it. Driver-side U4 corrections: added the mandatory Runtime Stack table and replaced full-width SC colons with ASCII.

## Optimization Points
- 1) requirements executor instance run-turn-budget=40 is too small for a full spec; the completion pass needed a 120-turn executor. 2) pre-analyze --stage requirements requires the Runtime Stack & Dependency Ownership table but create-requirements never mentions it, so a fresh spec fails the gate by default. 3) the checker SC-definition regex requires an ASCII colon; full-width Chinese punctuation silently yields 0 SCs and many dangling ids. 4) audit-test-budget.py names stages by *.jsonl filename stem, so requirements-stage-status.jsonl is skipped; the naming convention needs an owner decision.
