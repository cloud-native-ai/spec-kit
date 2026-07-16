# Contract: Glossary Protocol (Ambient Correction, Enrichment, Conflict)

Defines the prompt-side protocol documented in `shared/workflow/glossary.md` (mirrored to `.specify/shared/workflow/glossary.md`) and referenced by a lightweight `## Glossary` step on the workflow command templates (`requirements`, `plan`, `tasks`, `implement`) — modeled on the existing `## Feedback` step. These are PROMPT INSTRUCTIONS interpreted by the AI agent (Principle IX), not runtime code.

## C-1 Input correction & anchoring (FR-005, FR-006, FR-007)

- When a command interprets user input, it MUST consult the ambient glossary and map any recorded `variant` to its `canonical` term for interpretation.
- A correction MUST be surfaced to the user (e.g. "interpreted 『X』as canonical term 『Y』per glossary") so it is traceable and overridable (FR-006).
- The correction MUST NOT destructively rewrite the user's literal input.
- If a variant is ambiguous (maps to >1 canonical) or unrecognized, the agent MUST NOT guess and MUST defer to the user (FR-007).

## C-2 Progressive enrichment (FR-004)

- At natural workflow checkpoints (`requirements`, `plan`, `tasks`, `implement` wrap-up), the agent MUST detect newly-appearing project-specific terms and propose them as `origin=auto`, `status=proposed`.
- Common everyday words MUST NOT be proposed (FR-002).

## C-3 Conflict detection & confirmation (FR-008, FR-009)

- Before writing any proposed or manually-entered term, the agent MUST run conflict detection (`glossary-utils.py --action detect-conflict` for structural collisions, plus prompt-side phonetic/meaning judgment).
- On any detected or plausible conflict, the agent MUST present the conflict (candidate, colliding entries, kind) and obtain an explicit user resolution BEFORE writing.
- No conflicting change may be written without user confirmation. Writes go through `glossary-utils.py --action add … --confirmed-resolution <choice>`.

## C-4 User precedence (FR-010, FR-011)

- Users MAY edit `.specify/memory/glossary.md` directly at any time.
- `origin=user` entries are authoritative: automatic proposals MUST NOT overwrite them without explicit user confirmation. Manual edits survive regeneration (FR-013).

## C-5 Scope

- The protocol applies project-wide to the single glossary (FR-014) and is available to all `/speckit.*` commands via ambient context (FR-015).
