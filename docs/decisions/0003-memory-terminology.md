# ADR-0003: Memory terminology — session vs knowledge scopes under the umbrella "memory system"

- **Status:** Accepted
- **Date:** 2026-08-03
- **Deciders:** Spec Kit maintainers (user directive 2026-08-03)

## Context

An architecture review of the dynamic memory layer surfaced a naming collision. Users naturally describe the two archive tiers as "knowledge (long-term) vs memory (short-term, forgettable)". But in the codebase **"memory" is already the umbrella name for the whole system** — the `memory-as-files` layer, `memory-utils.py`, the `memory-record` / `memory-recall` skills, and the `.specify/memory/` directory. Using "memory" again for the short-term tier makes "memory vs knowledge" ambiguous: it is unclear whether "memory" means the entire system or only its short-term half.

## Decision

1. **"Memory system" is the umbrella term** for the entire dynamic memory-as-files layer (engine, skills, store). It is never the name of one tier.
2. The two archive tiers are named by their scopes:
   - **session — short-term memory** (working context: progress, in-flight state). Append-only, safe to prune — this is the *forgettable* tier.
   - **knowledge — long-term memory** (cross-session, project-global: stable preferences, conventions, lasting decisions). Upsert by slug — this is the *durable* tier.
   The tiers are always referred to as "session vs knowledge", never "memory vs knowledge".
3. **Maturity promotion chain:** `session → knowledge → constitution/features`. Entries mature from working notes (session) into distilled knowledge (knowledge); knowledge that becomes durable project truth is promoted into the static memory assets (`constitution.md`, `features.md`, `features/<ID>.md`, `tools.md`) and must not be duplicated in `knowledge/` afterwards.
4. The terminology note and the promotion chain are written into the canonical reference doc `docs/reference/skills/memory.md`.

## Alternatives

- **Adopt the user's framing literally ("knowledge vs memory" as two peer systems)** — matches intuition but collides with the umbrella usage of "memory" already established in code, file layout, and skill names. Rejected: renaming the umbrella system would churn the engine, skills, docs, and user mental model for no functional gain.
- **Rename the on-disk scopes** (e.g. `session/` → `short-term/`) — the scope names already match the chosen terminology; directory churn would break engine paths and existing entries. Rejected.

## Consequences

- Positive: one unambiguous vocabulary — "memory system" (whole), "session" (short-term), "knowledge" (long-term); the promotion chain makes the relationship to the static memory assets explicit.
- Negative: "memory" remains overloaded in casual speech; mitigated by the terminology note in the reference doc.
