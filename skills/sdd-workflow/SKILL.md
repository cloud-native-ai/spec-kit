---
name: sdd-workflow
description: |
  Shared knowledge base for Spec Kit SDD (Specification-Driven Development) lifecycle commands.
  Contains common protocols, guidelines, and reference material used across multiple /speckit.* commands.
  This skill is NOT invoked directly — it provides reference documents that commands load on demand.
  Use this when the user mentions ["SDD workflow", "speckit protocols", "command shared references"]
---

# SDD Workflow — Shared Command Protocols

This skill provides shared reference documents consumed by `/speckit.*` commands during execution. Commands reference specific files from `${SKILL_HOME}/references/` to avoid duplicating common logic.

## Reference Index

| File | Used By | Purpose |
|------|---------|---------|
| `user-input-protocol.md` | All commands | Standard `$ARGUMENTS` processing rules |
| `feature-integration.md` | requirements, plan, tasks, implement, checklist, feature | Feature tracking system integration protocol |
| `agent-configuration.md` | agents, tools, skills | Agent detection, per-agent guidance, feedback capture |
| `checklist-methodology.md` | checklist | Detailed examples, anti-examples, quality dimension methodology |
| `requirements-guidelines.md` | requirements | Spec quality validation, success criteria guidelines |
| `dfx-catalog.md` | feature | Design-For-X category catalog for future feature discovery |
| `clarify-taxonomy.md` | clarify | Three-mode taxonomy coverage categories and integration rules |
| `ignore-patterns.md` | implement | Technology-specific ignore file patterns |
| `tool-definitions.md` | tools | Behavioral rules format, edge cases, tool type details |

## Usage Convention

Commands reference these files with:
```
See ${SKILL_HOME}/references/<filename>.md for full details.
```

The AI agent MUST load the referenced file when it needs the detailed protocol. The command itself contains only the minimal workflow steps and command-specific logic.
