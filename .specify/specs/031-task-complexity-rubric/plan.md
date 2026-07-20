# Implementation Plan: Task Complexity Rubric in Generated Instructions

**Branch**: `031-task-complexity-rubric` | **Date**: 2026-07-20 | **Spec**: [requirements.md](./requirements.md)
**Requirement → Feature**: `031-task-complexity-rubric` → Feature 032 Task Complexity Rubric
**Input**: Specification from `.specify/specs/031-task-complexity-rubric/requirements.md`

## Summary

Add a technology-agnostic **Task Complexity Rubric** to the shared instructions template so that every generated `.specify/instructions.md` carries an agent-facing decision table mapping observable task signals → complexity tiers → prescribed thinking depth. The rubric lets an AI agent right-size its effort (avoiding both under-thinking complex/high-stakes work and over-thinking trivial work), balancing efficiency and quality.

Technical approach: this is a **documentation/prompt-framework** change (Constitution Principle IX), not runtime code. The single source-of-truth edit is a new `## Task Complexity Rubric` section in `templates/instructions-template.md`, dual-written to `.specify/templates/instructions-template.md`. Fresh generation renders the section directly (via `generate-instructions.sh`); existing documents acquire it through the `/speckit.instructions` command's **existing** generic "add missing scaffolding" refresh step, and the command's existing conflict policy already preserves any user-customized rubric — so **no change to the command template or its per-tool runtime mirrors is required**. Acceptance is guarded by a small pytest module that asserts the rubric section and its required structural elements are present and mirror-consistent.

## Technical Context

**Language/Version**: Markdown templates (no runtime language); repository tests run on Python `>=3.8` via `pytest`  
**Primary Dependencies**: None new. Rendering path uses the existing `scripts/bash/generate-instructions.sh`; verification uses the existing `pytest` harness (stdlib only)  
**Storage**: N/A — file/template content only  
**Testing**: `pytest` contract/unit test asserting the instructions template contains the `## Task Complexity Rubric` section and its required elements (tiers, signals, per-tier depth, tie-break rule, default tier, efficiency-vs-quality statement), plus a `templates/` ↔ `.specify/templates/` mirror-parity assertion  
**Target Platform**: Developer tooling; output consumed by AI agents reading `.specify/instructions.md`  
**Project Type**: single (code-generator / prompt framework)  
**Performance Goals**: N/A (static template content)  
**Constraints**: Template neutrality (project-agnostic, no spec-kit-specific prose); non-destructive refresh (existing user-authored content preserved byte-for-byte; user-customized rubric never overwritten); mirror-sync parity between `templates/` and `.specify/templates/`; stable heading `## Task Complexity Rubric` (STR-001)  
**Scale/Scope**: One new template section (~1 table + short prose) in two mirrored files; one new test module; zero new dependencies; zero runtime code

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`, v1.5.0.1):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every design element traces to `requirements.md` FR-001…FR-012; the template section is generated from the spec, not vice versa |
| II | Feature-Centric Development | ✅ Pass | Bound to Feature 032; `.specify/memory/features.md` row + `.specify/memory/features/032.md` created (clarify) and advanced to `Planned` (this plan) |
| III | Intent-Driven Development | ✅ Pass | Plan states the "what/why" of effort calibration before the "how"; rubric content is intent guidance, refined multi-step (requirements → clarify → plan) |
| IV | Test-First & Contract-Driven Implementation | ⚠ Partial — see Complexity Tracking | Template-only feature: no executable runtime code. Per Principle VII, "tests" verify template content/structure/mirror-parity instead of runtime behavior; the test module is written before the template edit |
| V | AI Agent Integration Standards | ✅ Pass | Rubric is provider-neutral guidance for the approved agents; introduces no new provider and no provider-specific keyword dependency |
| VI | Continuous Quality & Observability | ✅ Pass | YAGNI honored (template-only, no infra); pytest gate runs in CI; docs/feature memory updated alongside the change |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Following spec→clarify→plan; feature reuse-first evaluated in clarify (new Feature 032 justified); template-only Test-First Partial explicitly acknowledged |
| VIII | Code as the Single Source of Truth | ✅ Pass | The instructions template file is the authoritative source for generated content; tests assert against the file, not against docs |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | Simplest satisfying artifact: a template section + reliance on existing generic refresh logic; explicitly rejects editing the command doc / per-tool mirrors and any runtime mechanism |
| X | Documentation Naming & Location Conventions | ✅ Pass | Rubric lives under a conventional `##` heading inside an existing template; no reserved ALL-CAPS names introduced; spec artifacts are lowercase kebab-case |

**Gates Status**: ✅ All gates pass — one justified Partial (Principle IV, template-only feature; see Complexity Tracking).

**Re-check after Phase 1**: 2026-07-20 — re-ran the table against the generated `data-model.md`, `contracts/`, and `quickstart.md`. No new violations; Principle IV remains a justified Partial. Design confirms IX (no command/mirror/runtime changes needed).

## Project Structure

### Documentation (this spec)

```text
.specify/specs/031-task-complexity-rubric/
├── plan.md              # This file (/speckit.plan command output)
├── requirements.md      # Feature spec (/speckit.requirements + /speckit.clarify)
├── data-model.md        # Phase 1 output — the concrete rubric design (tiers/signals/depth)
├── quickstart.md        # Phase 1 output — how to see the rubric appear & how to verify
├── feature-ref.md       # Phase 1 output — requirement ↔ Feature 032 linkage
├── contracts/
│   └── rubric-section.md # Phase 1 output — structural contract the tests assert
├── checklists/
│   └── requirements.md   # Spec quality checklist (all items pass)
├── tasks.md             # Phase 2 output (/speckit.tasks — NOT created here)
└── verification.md      # Implementation output (/speckit.implement)
```

No standalone `research.md` — Phase 0 findings are brief and fully internal; inlined below under "Phase 0".

### Source Code (repository root)

```text
templates/                 # add `## Task Complexity Rubric` section to instructions-template.md (source of truth)
.specify/templates/        # mirror the same edit into instructions-template.md (dual-write, must match templates/)
tests/                     # add a contract/unit test asserting rubric presence, required elements, and mirror parity
```

**Structure Decision**: This spec lands in the existing **code-generator / prompt-framework** shape. It extends `instructions-template.md` (in both mirror locations) with one new section and adds one pytest module verifying that section's presence, required structural elements, and cross-mirror parity. No new top-level directory; no runtime code; no change to `templates/commands/instructions.md` or its per-tool runtime copies (the command's existing generic refresh + conflict policy already deliver FR-009/FR-010/FR-011).

## Phase 0: Research & Context (inlined)

**Findings (all resolved from project docs, constitution, and existing templates — no external research needed):**

1. **Generation path is template-driven.** `generate-instructions.sh` renders `instructions-template.md` only when no `.specify/instructions.md` exists; therefore a new section placed in the template appears verbatim in freshly generated docs (satisfies FR-009).
2. **Existing-doc insertion is already generic.** `templates/commands/instructions.md` → "Section-by-section refresh" → "Add missing scaffolding" already instructs the agent to insert any template-defined section absent from the base at the structurally appropriate place (satisfies FR-010). Its "Conflict policy" already preserves user-authored content (satisfies FR-011). ⇒ **No command-doc edit needed** — the minimal, YAGNI-aligned choice (Principle IX).
3. **Mirror-sync is mandatory.** `templates/` and `.specify/templates/` are independent real copies; the recurring-lessons log flags mirror drift as a top rework source. The edit MUST be dual-written and asserted equal for the new section.
4. **Template neutrality constraint.** Per recurring lessons, shared templates stay project-agnostic; the rubric content must contain no spec-kit-specific references.
5. **Placement decision.** Insert the rubric after "Fact, Correctness & Logic Checks (Input Sanity)" and before "Tech Stack & Resources" — it is cross-cutting agent-behavior guidance, peer to the input-sanity guidance, and precedes project-specific facts. (Confirmed against the current template ordering.)

**Unknowns resolved:** thinking-depth is expressed as **behavioral prescriptions** (exploration/planning/verification effort), not tool-specific reasoning keywords — keeps the rubric provider-neutral (Principle V). Explicit per-agent keyword mapping is recorded as a future evolution, not built now (YAGNI).

## Phase 1: Design & Contracts (outputs)

- **`data-model.md`** — the concrete rubric: 4 complexity tiers (Trivial / Standard / Complex / High-stakes-or-Ambiguous), the signal dimensions used to classify (scope, uncertainty/novelty, blast-radius/reversibility, cross-cutting impact, requirements clarity), each tier's prescribed thinking-depth behavior, the tie-break rule (choose the higher tier when signals conflict), the default tier for unclassifiable input, and the efficiency-vs-quality statement.
- **`contracts/rubric-section.md`** — the structural contract the tests assert: the exact stable heading (STR-001), presence of a tier table, the required number/labels of tiers, and the required presence of signals, per-tier depth, tie-break, default tier, and tradeoff statement; plus the mirror-parity requirement.
- **`quickstart.md`** — how to observe the rubric (fresh generation and existing-doc refresh) and how to run the verification test.
- **`feature-ref.md`** — requirement ↔ Feature 032 linkage record.

**Post-design Constitution re-check**: completed above (no new violations).

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Principle IV (Test-First) is **Partial**, not full | The feature ships only template/prose content — there is no executable runtime unit to drive via Red-Green-Refactor. Coverage is provided by a contract/unit test that asserts the rendered template contains the rubric section, its required structural elements, and cross-mirror parity; the test is authored before the template edit. | A full runtime TDD cycle was rejected because it would require inventing runtime code (a parser/validator) that the feature does not need — over-engineering explicitly barred by Principle IX. Structural assertions on the template are the appropriate and sufficient verification for a template-only change. |
