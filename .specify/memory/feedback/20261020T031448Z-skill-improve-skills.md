---
id: "20261020T031448Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "improve-skills-sdd-project-setup-20261020T031448Z"
scope: "local"
probe: "skill-improve-skills-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-10-20T03:14:48Z"
summary: "improve-skills sdd-project-setup: instruction budget overrun addressed via S3 trigger + S3.4 R3 fallback; evidence ev-018; docs/tests/mirrors green; cross-skill R3 ownership noted."
---

## Review
improve-skills sdd-project-setup: instruction budget overrun addressed via S3 trigger + S3.4 R3 fallback; evidence ev-018; docs/tests/mirrors green; cross-skill R3 ownership noted.

## Optimization Points
- `sdd-project-setup` S3 now treats the `BUDGET ... over` report as a convergence trigger and routes to S3.4 R3 (project-filled section externalization) when the owner R1/R2 have no legal candidates; content migration is mechanical and pending escalation is explicit. Evidence: `ev-018` (14 recurring feedback entries) plus current `.specify/instructions.md` 37,415 B > 32,768 B.
- `manage-instructions` remains the R1/R2 owner and is still over the skill-shape budget; the setup-side R3 fallback is recorded as a cross-skill dependency. Follow-up: decide whether the manager should absorb R3 as its own route.
- Contract guard added: `tests/contract/test_sdd_project_setup_skill.py::test_c13_instruction_budget_convergence_is_wired`; mirrors synced; 18 + 12 + 16 contract tests green.
