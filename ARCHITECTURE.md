# Architecture Overview

> One-page entry to Spec Kit's architecture. Full detail lives in [docs/concepts/](docs/concepts/) and decision records in [docs/decisions/](docs/decisions/).

## System Shape

Spec Kit is a **documentation/prompt framework, not a runtime platform** (Constitution Principle IX): a Python CLI (`specify-cli`) scaffolds a `.specify/` workspace and distributes `/speckit.*` command prompts, skills, and agents to eight supported AI tools.

## Core Components

| Component | Responsibility | Detail |
|-----------|----------------|--------|
| `src/specify_cli/` | Typer CLI: init, template packaging, per-tool command generation | [concepts/overview.md](docs/concepts/overview.md) |
| `templates/` | Source of truth for commands, plans, specs, instructions | [concepts/spec-driven.md](docs/concepts/spec-driven.md) |
| `scripts/` | Deterministic engines (feedback, history, glossary, docs, …) | [reference/commands/](docs/reference/commands/) |
| `skills/`, `agents/` | Installable skills and role agents | [reference/skills/](docs/reference/skills/), [reference/agents/](docs/reference/agents/) |
| `.specify/` | Per-project runtime workspace (memory, specs, instructions) | [concepts/overview.md](docs/concepts/overview.md) |

## Key Decisions

| Decision | Status | Record |
|----------|--------|--------|
| Adopt six-type docs taxonomy + notes lifecycle | Accepted | [ADR-0001](docs/decisions/0001-adopt-docs-taxonomy.md) |

## Deeper Reading

- Concepts → [docs/concepts/](docs/concepts/)
- Decisions → [docs/decisions/index.md](docs/decisions/index.md)
