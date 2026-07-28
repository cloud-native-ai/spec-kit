# Contributing

> Entry point for contributing to Spec Kit. Deep contributor docs live in [docs/contribute/](docs/contribute/).

## Quick Path

1. Set up the dev environment → [docs/contribute/dev-setup.md](docs/contribute/dev-setup.md)
2. Follow the SDD workflow: every change goes spec → plan → tasks → implement (`/speckit.*` commands; Constitution Principle XI Dogfooding).
3. Run the tests: `.specify/scripts/bash/run-tests.sh` (record the baseline first; pre-existing failures exist).
4. Keep mirrors in sync: after editing `templates/commands/`, run `python3 scripts/python/regen-command-copies.py --check`.

## Ground Rules

- Constitution (`.specify/memory/constitution.md`) governs architecture and workflow constraints.
- Docs follow the six-type taxonomy + uppercase special-name registry (see [ADR-0001](docs/decisions/0001-adopt-docs-taxonomy.md)); manage them with `/speckit.docs`.

## Deeper Reading

- Dev setup → [docs/contribute/dev-setup.md](docs/contribute/dev-setup.md)
- Decision records → [docs/decisions/](docs/decisions/)
