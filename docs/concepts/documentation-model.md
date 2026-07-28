# Documentation Model (What & Why)

> Formal home of the documentation-space design distilled from the retired notes `docs/notes/docs-design.md` and `docs/notes/notes-design.md` (spec 033, Feature 037, ADR-0001). Operated by the `/speckit.docs` reconcile command — see [../reference/commands/docs.md](../reference/commands/docs.md).

## Two-layer model

- **Root = thin layer (entry + index)**: never more than one screen. When a root file grows, its content sinks into `docs/` and the root keeps a summary + links.
- **`docs/` = thick layer (full content)**, split by document type, each answering one reader question:

| Directory | Question answered | Writing style |
|-----------|-------------------|---------------|
| `concepts/` | What is it? Why does it exist? | explanatory, narrative |
| `tutorials/` | How do I get started? | hand-holding, linear, clear endpoint |
| `tasks/` | How do I accomplish X? | step-wise, skimmable |
| `reference/` | What are the exact specs? | structured, complete, no narrative |
| `decisions/` | Why X over Y? | argumentative ADRs, append-only |
| `contribute/` | How do I work on this project? | procedural |
| `notes/` | (temporary holding) | no stability guarantee, lifecycle-bound |

## Uppercase special names (filename IS semantics)

`README.md` → indexes all of `docs/`; `ARCHITECTURE.md` → one-page summary of concepts + decisions; `CONTRIBUTING.md` → summary of contribute; `CHANGELOG.md` → self-contained timeline. ALL-CAPS names are reserved; ordinary docs are lowercase kebab-case. The registry is extensible — a new special name must register its fixed semantics.

## Document lifecycle

```
idea/research → decisions/ (Proposed)
      ↓ Accepted
concepts/ or reference/ reflect the design
      ↓ users need operating guidance
tasks/ or tutorials/
      ↓ project evolves
decisions/ annotated Deprecated / Superseded
```

Formal directories are **append/archive-only** (stable knowledge, exits to `docs/archive/`); `notes/` is **flow-through** (in and out); root files are **one-screen signposts**.

## Notes lifecycle (exit mechanism)

Every note carries frontmatter (`title / created / expires — default created + 60 days / status: draft|expired|archived / target / tags`). State machine:

```
draft --merge into target--> archived (annotated with destination)
draft --past expires-------> expired --confirmed delete--> removed (notes zone only)
expired --renew------------> draft (new expires)
```

Deterministic automation: `python3 scripts/python/docs-utils.py --action scan|expire|clean|archive-check|stats|validate|audit` (contract: `.specify/specs/033-docs-command/contracts/docs-utils-cli.md`). Three safeguards — frontmatter metadata, engine automation, and the `/speckit.docs` reconcile loop — keep `notes/` from becoming a landfill.

## Consistency maintenance

- **Incremental**: every complex `/speckit.*` command ends with the docs-sync evaluation step (`shared/workflow/docs-step.md`): 需记录（目标文档 + 要点） or 无需记录.
- **Convergent**: `/speckit.docs` reconciles the whole space on demand (tolerance band, dry-run plan, tiered confirmation, archive-not-delete, audit trail in `.specify/docs/`).
