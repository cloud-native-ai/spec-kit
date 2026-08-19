---
id: "20260819T072439Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "improve-skills-2026-08-19-misuse-vs-pitfall-gate"
scope: "local"
probe: "skill-improve-skills-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-08-19T07:24:39Z"
summary: "Loop added the misuse-vs-pitfall reflection gate (SKILL.md Step-3 decision branch + loop-playbook detail section with worked case + 2 quality-checklist items), driven by a real incident where expected"
---

## Review
Loop added the misuse-vs-pitfall reflection gate (SKILL.md Step-3 decision branch + loop-playbook detail section with worked case + 2 quality-checklist items), driven by a real incident where expected tool behavior under a wrong method was recorded as a pitfall. Validated: skill-shape.py exit 0 (4998/5000), contract failure-set identical to HEAD baseline (10 pre-existing, zero regression), RED-GREEN pressure re-test passed (fresh agent under the gate correctly refuses the pitfall record and prescribes a method-selection branch). Hit the cp -i alias gotcha mid-loop (AGENTS.md lesson confirmed) and initially broke an FR-010 inline content assertion by slimming a contract-mandated bullet — both recovered within the loop.

## Optimization Points
- # Optimization Points
- token-efficiency: shape-gate token budget was checked only after final wording; the loop needed 4+ micro-trim iterations to land under 5000. Next loop: run skill-shape.py on the draft bullet wording first when the body is within ~100 tokens of budget, then write final prose.
- Gap found this run: the "never slim a contract-mandated section" rule speaks of named headings, but a contract test (FR-010, test_skill_home_workdir_template.py) asserts inline *content* (the three legacy-idiom strings) inside a bullet — trimming that bullet caused a regression. The pre-trim contract grep (.specify/specs/** + tests/contract/**) should be stated to cover content-level assertions in bullets, not only heading-presence.
