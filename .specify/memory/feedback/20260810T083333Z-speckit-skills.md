---
id: "20260810T083333Z-speckit-skills"
unit_id: "/speckit.skills"
unit_type: "command"
run_id: "create-docs-extraction-20260810"
scope: "local"
feature: "037"
partial: false
created: "2026-08-10T08:33:33Z"
summary: "Extracted the /speckit.docs engine into the create-docs skill and rewrote the command as a thin mandatory delegator; re-pinned spec-033 contract clauses C-4/C-5/C-6/C-9 onto the skill and added C-4a/C"
---

## Review
Extracted the /speckit.docs engine into the create-docs skill and rewrote the command as a thin mandatory delegator; re-pinned spec-033 contract clauses C-4/C-5/C-6/C-9 onto the skill and added C-4a/C-12; registered the skill, synced mirrors (check exit 0), propagated to knowledge-manager; 13/13 docs-command contract tests and 91 agent/template tests green; remaining failures verified pre-existing (root-owned .git objects blocked a stash-based baseline check, so attribution was done by change-set inspection).

## Optimization Points
- When the extraction source is a contract-pinned command, re-point the spec contract + contract test FIRST (C-4/C-5/C-6/C-9 were pinned on templates/commands/docs.md), then write the skill — avoids a red-test window and makes the delegation shape explicit up front.
- token-efficiency: reading the 157-line source command + 258-line create-skills SKILL.md + contract/test files was necessary and proportional; no avoidable whole-file re-reads occurred (targeted greps used elsewhere).
