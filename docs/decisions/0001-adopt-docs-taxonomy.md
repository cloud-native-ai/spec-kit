# ADR-0001: Adopt six-type docs taxonomy with uppercase special-name registry and notes lifecycle

- **Status:** Accepted
- **Date:** 2026-07-28
- **Deciders:** Spec Kit maintainers (spec 033, Feature 037)

## Context

Spec Kit's `docs/` had grown organically (8 subdirectories + 8 loose files, no temporary-document discipline, a 110-line README). Two design notes (`docs/notes/docs-design.md`, `docs/notes/notes-design.md`) proposed a K8s-style documentation model; spec 033 turned it into the `/speckit.docs` reconcile command. Dogfooding (Constitution Principle XI) requires applying the model to Spec Kit itself.

## Decision

1. **Thin root layer** of uppercase special names with fixed semantics (filename IS semantics): `README.md` (index), `ARCHITECTURE.md` (one-page summary), `CONTRIBUTING.md` (contribution entry), `CHANGELOG.md` (timeline); each ≤ one screen; registry extensible; ordinary docs use kebab-case.
2. **Thick `docs/` layer** by document type: `concepts/ tutorials/ tasks/ reference/ decisions/ contribute/` (formal, archive-not-delete via `docs/archive/`) + `notes/` (temporary, frontmatter lifecycle draft/expired/archived, deterministic automation via `scripts/python/docs-utils.py`).
3. `docs/` managed by the `/speckit.docs` reconcile engine (tolerance band, dry-run plan, tiered confirmation); docs consistency maintained incrementally by the `## Documentation` step on complex commands.
4. This reorganization itself executed as the first aggressive full-sweep reconcile (plan: `.specify/docs/plans/20260728-dogfood-plan.md`).

## Alternatives

- **Keep the organic layout** (local conventions outrank templates): rejected by explicit user direction — user input is the highest-precedence desired-state source for this run.
- **Replace notes/ with Proposed ADRs** (docs-design.md Option B): rejected in favor of Option A + lifecycle constraints; the "graduation path" spirit is kept via the mandatory `target` field.

## Consequences

- Positive: predictable reader navigation (type-based), enforceable deterministic checks, temporary docs can no longer rot silently.
- Negative: historical inbound links to old paths (e.g. `docs/quickstart.md`) break outside this repo; internal references, tests, and the Documentation Map were updated in the same change.
