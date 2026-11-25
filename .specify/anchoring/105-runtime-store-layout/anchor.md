---
status: active
created: 2026-11-25
updated: 2026-11-25
handoff_ref: .specify/specs/105-runtime-store-layout/handoff.md
---

# Anchor: Runtime Store Layout

## Objective

The framework's runtime-state layout is semantically partitioned: .specify/memory/ no longer exists as a catch-all, agent memory lives in two first-class top-level stores, every other runtime store has a named top-level home, and existing workspaces upgrade without data loss or a second authority.

## Success Criteria

1. All 27 FRs and 9 SCs of spec 105 are sealed with passing verification, including migration/refusal tests and zero old-path live references outside the declared allowlist.
2. Existing client workspaces migrate through /speckit.migrate with byte-preserved data, deterministic conflict refusal, and idempotent reruns.
3. Temporary/session memory and super-agent to sub-agent context-injection behavior remain unchanged except for storage roots.

## Boundaries

- No push; no downgrade of prior features; no runtime dual-path fallback; no manual-only migration.

## History

- 2026-11-25 — created.
