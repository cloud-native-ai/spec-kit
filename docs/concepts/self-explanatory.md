# Self-Explanatory Structure (不言自明)

Self-Explanatory Structure is a **people-first** principle: names, paths, and
structures should convey the system information a human user needs at a glance,
or through one simple command, instead of requiring the user to open files,
read implementation, or ask a maintainer.

## Where it lives

| Layer | Location | Role |
|-------|----------|------|
| Concept owner | `shared/definitions/self-explanatory-definitions.md` | Single source of truth: definition, ceiling/floor, authority/projection, dimension order |
| Practice owner | `shared/guidelines/self-explanatory.md` | Applying the principle, migration, impact assessment, example accumulation |
| Optimization workflow | `shared/workflow/best-practice-optimization.md` | Best-practice lookup and application; two-hat output mapping |
| Related governance | Constitution X (Documentation Naming & Location), XVIII (Grounded Naming) | Path semantics and naming-source precedence |

> Runtime mirror: `.specify/shared/...` follows the framework-source paths above
> after the normal mirror/install step.

## In one glance

- **User perspective**, not program-internal clarity.
- **Ceiling**: the user sees the information directly. **Floor**: one simple
  command. The floor is sufficient to justify a change.
- **Not preventive optimization**: a concrete user information need must exist.
- At most **one dimension per optimization task**; reconciliation may take
  multiple steps to implement that one dimension.
- An encoded attribute keeps its **original source of truth** (for example,
  goal `status` in YAML frontmatter); the path is a projection maintained by
  `/speckit.sanitize` with eventual consistency.
- Existing structures migrate gradually under the reconcile pattern; renames
  require reference discovery, effort estimation, and backward-compatibility
  assessment.

## Naming history

Introduced as 望文生义; the canonical term is now 不言自明 (Self-explanatory). The retired name survives only as a synonym in the glossary entry (`望文生义`), never as a second canonical term.
