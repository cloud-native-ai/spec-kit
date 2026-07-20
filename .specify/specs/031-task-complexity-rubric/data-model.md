# Data Model: Task Complexity Rubric

**Feature**: 032 Task Complexity Rubric · **Spec**: `031-task-complexity-rubric` · **Date**: 2026-07-20

This document defines the concrete content of the rubric that Phase 2 will embed, verbatim, as the `## Task Complexity Rubric` section of `instructions-template.md`. It is technology-agnostic and project-neutral (no spec-kit-specific references).

## Entities

- **Task Complexity Rubric**: The section embedded in `.specify/instructions.md`. Composed of a signal list, a tier table, a tie-break rule, a default-tier rule, and an efficiency-vs-quality statement.
- **Signal Dimension**: An observable property of a task used to classify it. Five dimensions (below).
- **Complexity Tier**: One of four named bands. Each carries typical signals and a prescribed thinking-depth behavior.
- **Thinking-Depth Level**: The effort profile a tier prescribes, expressed as concrete agent behavior (exploration, planning, verification, and confirmation before irreversible actions).

## Signal Dimensions

1. **Scope / size** — how much code/surface the task touches (one spot → many files/modules).
2. **Uncertainty / novelty** — how well the solution is known up front (obvious → open design choices).
3. **Blast radius / reversibility** — consequence if wrong and how hard to undo (isolated & reversible → shared/irreversible).
4. **Cross-cutting impact** — whether it spans components, contracts, or shared state.
5. **Requirements clarity** — how unambiguous the task is (crystal-clear → unclear/conflicting).

## Tier Table (canonical content)

| Tier | Typical signals | Thinking depth (prescribed agent behavior) |
|------|-----------------|--------------------------------------------|
| **Trivial** | Tiny, well-scoped edit; no uncertainty; easily reversible; no cross-cutting impact; requirements crystal-clear | **Minimal** — act directly; little to no exploration; no written plan; light sanity check (build/lint or the one relevant test) |
| **Standard** | One area or a few files; low uncertainty; moderate, reversible risk; little cross-cutting; requirements clear | **Moderate** — read the directly relevant files; form a brief internal plan; run the related tests |
| **Complex** | Multiple files/modules; real uncertainty or design choices; harder to reverse; cross-cutting; requirements mostly clear | **Deep** — explore broadly before editing; write an explicit plan (consider plan mode); weigh alternatives; add/adjust tests and verify behavior |
| **High-stakes / Ambiguous** | High blast radius (shared infra, data migration, security, public API); hard or irreversible; or requirements unclear/conflicting | **Exhaustive** — thorough exploration; explicit plan with user checkpoints; edge-case and adversarial analysis; strong verification; confirm before irreversible actions; resolve unclear requirements first |

## Tie-Break Rule

Signals frequently span more than one tier. **Choose the highest tier indicated by any single dominant signal.** Blast-radius/reversibility and requirements-clarity dominate: a tiny edit to a high-blast-radius or irreversible surface is High-stakes, not Trivial. When genuinely in doubt between two tiers, go one tier up.

## Default Tier

If a task cannot yet be classified, treat it as **Standard**. However, if the reason it cannot be classified is unclear or under-specified requirements, that is itself a High-stakes / Ambiguous signal — **clarify before proceeding** rather than guessing.

## Efficiency-vs-Quality Statement

Right-size the thinking. Under-thinking complex or high-stakes tasks causes defects and rework (a quality cost); over-thinking trivial tasks wastes time and adds noise (an efficiency cost). Aim for the lowest depth that safely fits the tier — escalate on doubt, and do not default to maximal effort.

## Requirements Traceability

| Element | Requirements |
|---------|--------------|
| Stable heading `## Task Complexity Rubric` | FR-001, FR-012 (STR-001) |
| Four distinct, labeled tiers | FR-002 |
| Five signal dimensions | FR-003 |
| Per-tier behavioral thinking-depth | FR-004 |
| Tie-break rule (higher tier on conflict) | FR-005 |
| Default tier + clarify-on-ambiguity | FR-006 |
| Efficiency-vs-quality statement | FR-007 |
| Technology-agnostic content in shared template | FR-008 |
