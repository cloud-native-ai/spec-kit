# Feature Reference: Requirement ↔ Feature Linkage

**Requirement Key**: `031-task-complexity-rubric`  
**Feature**: 032 — Task Complexity Rubric  
**Status**: Planned (advanced from Draft by `/speckit.plan` on 2026-07-20)  
**Feature Detail**: `.specify/memory/features/032.md`  
**Feature Index Row**: `.specify/memory/features.md`

## Binding

This requirement is bound to **Feature 032** (a new feature minted during `/speckit.clarify`, Session 2026-07-20). The rubric is tracked as a distinct cross-cutting agent-behavior mechanism delivered via the instructions document — mirroring how Glossary (031) and Feedback (028) are their own features though wired through existing commands — rather than folded into the Instructions Command feature (008).

## Classification

- **Type**: Functional capability (agent-facing guidance content), delivered as documentation/prompt-framework (Constitution Principle IX).
- **Reuse decision**: New feature justified (no existing feature covers task-complexity-driven thinking-depth calibration).
- **No status regression**: N/A — new feature starting at Draft → Planned.

## Coverage Map

| Requirement | Design artefact |
|-------------|-----------------|
| FR-001…FR-008, FR-012 | `data-model.md` (rubric content) + `contracts/rubric-section.md` (C-1…C-10) |
| FR-009 | Fresh generation renders the template section (`quickstart.md` §fresh) |
| FR-010, FR-011 | Existing-doc refresh via the command's generic "add missing scaffolding" + conflict policy (`plan.md` Phase 0 finding 2) |
| SC-001 | Contract C-1 (presence after generation) |
| SC-002 | Refresh before/after diff (contract Verification Notes) |
| SC-003, SC-004 | Review artefact at acceptance (out of scope for unit test) |
| SC-005 | Single self-contained section under one heading (`data-model.md`) |
