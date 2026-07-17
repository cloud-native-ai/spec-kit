---
id: "20260716T175027Z-speckit-implement"
unit_id: "/speckit.implement"
unit_type: "command"
run_id: "029-glossary-mechanism-implement-20260716"
scope: "local"
feature: "029-glossary-mechanism"
partial: false
created: "2026-07-16T17:50:27Z"
summary: "Implemented Feature 031 Glossary Mechanism end-to-end as a doc/prompt-framework capability. Built glossary-utils.py (stdlib engine: init/list/validate/detect-conflict/add/remove) with a conflict/prece"
---

## Review
Implemented Feature 031 Glossary Mechanism end-to-end as a doc/prompt-framework capability. Built glossary-utils.py (stdlib engine: init/list/validate/detect-conflict/add/remove) with a conflict/precedence choke point; glossary-template.md; shared/workflow/glossary.md protocol; generate-instructions.sh non-destructive init hook; Documentation Map wiring (template + live instructions); ## Glossary step on 4 command templates + instructions seeding guidance, propagated across all mirrors and per-tool copies (44 files). 23 new tests (10 unit + 13 contract) all pass; caught+fixed a real engine bug (table-header regex matched the Column-Definitions row) and a hard-coded 'ten docs' gate broken by the legitimate new shared doc. Full suite: 97 failed/683 passed vs baseline 97/660 — zero regressions. verification.md: SC-001..005 pass, SC-006 deferred (post-adoption usage metric). Feature status flipped Planned→Implemented per gate.

## Optimization Points
- The `.venv` had no `pytest` while system `pytest` (8.4.2) did; the first baseline run silently reported "No module named pytest". `/speckit.implement`'s "validate every build/test command" step should probe for a *runnable* test runner (system vs venv) up front, so a template-heavy feature does not proceed on a false empty baseline.
- A legitimate additive change (adding `shared/workflow/glossary.md`) broke another feature's hard-coded exact-count gate (`test_shared_workflow_directory_has_ten_docs`). When `/speckit.implement` adds a file to a directory, it should proactively grep the test tree for brittle count/enumeration assertions naming that directory and update them as part of the same change, rather than discovering the regression only at the final full-suite run.
- Mirror fan-out for a command-template edit touched 4 surfaces × 5 commands (templates + .specify mirror + .claude + .github + .qoder). A helper that regenerates the per-tool copies from a single source template would make this deterministic and remove the hand-sync risk that dominates this repo's rework.
