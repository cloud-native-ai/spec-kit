# Feature Reference

**Spec**: [requirements.md](./requirements.md) | **Plan**: [plan.md](./plan.md)

## Bound Feature

| Field | Value |
|-------|-------|
| Feature ID | 019 |
| Feature Name | Agents Command |
| Feature Detail | `.specify/memory/features/019.md` |
| Relationship | Evolution/refactor of the existing (Implemented) feature |
| Status action | Keep `Implemented` (Decision D4 — do not regress); add spec-023 evolution note |

## Rationale

Spec 023 refactors the Agent framework that Feature 019 owns. Prior specs under 019 include `003-speckit-agents-command`, `014-agent-framework-refactor`, `015-role-based-agents`, and `022-eei-agent-triad`. This spec unifies the conceptual model (Role/Stage/Type/Team/Loop), unifies terminology, merges the supervisor role, canonicalizes templates, and regenerates docs.

## Feature Index Changes

- No new Feature created; no Feature merged or deprecated.
- `.specify/memory/features/019.md`: append spec-023 evolution note.
- `.specify/memory/features.md`: update Feature 019 `Last Updated` → 2026-07-10.
