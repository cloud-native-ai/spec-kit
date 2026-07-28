# ADR-0002: Reserved Filenames — strict blocking outside registered locations

- **Status:** Accepted
- **Date:** 2026-07-28
- **Deciders:** Spec Kit maintainers (spec 033, Feature 037; user directive 2026-07-28)

## Context

After the ADR-0001 reorganization, `docs/decisions/README.md` (and three other nested `README.md` files) reused an uppercase special name outside the project root. The uppercase registry (README/ARCHITECTURE/CONTRIBUTING/CHANGELOG) defines fixed semantics, so a nested reuse silently claims the wrong meaning.

## Decision

Treat uppercase special names as **Reserved Filenames**, analogous to reserved keywords in a programming language:

1. Each reserved name registers **fixed semantics AND a registered location** (currently all at project root) and may appear ONLY there with that meaning — strict blocking.
2. User documents MUST NOT use a reserved name; same-semantics documents elsewhere use lowercase alternatives — **directory indexes are `index.md`**, never a nested `README.md`.
3. The constraint is written into the constitution (Principle X, v1.7.0) and enforced deterministically by `docs-utils.py --action validate` (violation kind `reserved-name-misplaced`).
4. Tool/framework-mandated names (`CLAUDE.md`, `AGENTS.md`, `LICENSE`, `skills/*/SKILL.md`, `.github/prompts/*.prompt.md`, …) are exempt.

Applied immediately: `docs/decisions/README.md`, `docs/notes/README.md`, `docs/tasks/README.md`, `docs/reference/history/README.md` → `index.md`.

## Alternatives

- **Scoped reuse (README.md allowed as directory index)** — GitHub renders nested READMEs automatically and the prior Principle X wording allowed it. Rejected by explicit user decision: name = semantics contract must be unambiguous; losing nested auto-render is an accepted cost.

## Consequences

- Positive: zero ambiguity about what any ALL-CAPS filename means; deterministic, machine-checkable rule.
- Negative: GitHub no longer auto-renders directory landing pages for `index.md`; readers follow explicit links from the root README instead.
