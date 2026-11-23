# 🌱 Spec Kit

*Build high-quality software faster.*

**An open source toolkit built around Spec-Driven Development (SDD): requirements, plans, tasks, and implementation connect through structured templates and `/speckit.*` commands, so AI progresses around clear intent instead of one-off vague prompts.**

spec-kit is an independent fork of [github/spec-kit](https://github.com/github/spec-kit)
(MIT, Copyright GitHub, Inc.), forked at 926836e0f (2025-10-21).
It is not affiliated with or endorsed by GitHub. Thanks to the original Spec Kit contributors.

## 📚 Documentation Navigation

| I want to... | Go to |
|--------------|-------|
| Install the `specify` CLI | [docs/tutorials/installation.md](docs/tutorials/installation.md) |
| Follow the quick start walkthrough | [docs/tutorials/quickstart.md](docs/tutorials/quickstart.md) |
| Understand concepts & methodology (SDD, vibe coding, better harness, prompt-to-graph evolution, docs model, upstream, security) | [docs/concepts/](docs/concepts/) |
| Accomplish a specific task | [docs/tasks/](docs/tasks/) |
| Look up exact references (commands, CLI tools, skills, agents, teams, glossary) | [docs/reference/](docs/reference/) |
| Understand why a design decision was made | [docs/decisions/](docs/decisions/) |
| Contribute to the project | [CONTRIBUTING.md](CONTRIBUTING.md) |

## 🏗 Architecture

→ See [ARCHITECTURE.md](ARCHITECTURE.md) (one page) and [docs/concepts/](docs/concepts/).

## 🔧 Feature List

### Functional

- **Specification-Driven Development**: requirements → plan → tasks → implementation → review → seal
- **AI Agent Integration**: 6 supported AI coding assistants with shared-core initialization and real agent rendering
- **Extensible Skills, Agents & Teams**: authoring, improvement, execution, and host-specific projections through `/speckit.*` commands
- **Research & Knowledge Studies**: source-code, project knowledge-base, and online research carriers
- **Documentation & Visualization**: documentation reconciliation, architecture diagrams, project summaries, and line-level status visibility
- **Technical Debt Governance**: read-only debt inventory and phased governance planning, with cleanup routed to authorized flows

### Non-functional

- **Evidence-Backed Acceptance**: deterministic closure, four-segment review, acceptance reality checks, and archive admission
- **Conflict-Free Records**: per-entry feedback and memory records with derived indexes and atomic writes
- **Concurrency & Recovery**: explicit concurrency contracts, effective-overlap readings, stage evidence, and interruption snapshots
- **Execution Efficiency & Security**: parallel-capable test runner, bounded input reads, and a local Ruff shell-security gate

Full feature registry: `.specify/features.md` (single source of truth).

## 🤖 Supported AI Agents

**Tier 1** (CLI 形态): [Claude Code](https://www.anthropic.com/claude-code) · [Codex CLI](https://github.com/openai/codex) · [Qoder CLI](https://qoder.com/cli) · [opencode](https://opencode.ai/)
**Tier 2** (非 CLI 形态): Hermes Agent · [GitHub Copilot](https://code.visualstudio.com/)

## 📦 Installation

See [docs/tutorials/installation.md](docs/tutorials/installation.md).

## 🤝 Contributing & Support

See [CONTRIBUTING.md](CONTRIBUTING.md); support channels are listed in [SUPPORT.md](SUPPORT.md), and security reports go through [SECURITY.md](SECURITY.md).

## 📄 License

MIT — see [LICENSE](LICENSE) and [NOTICE](NOTICE).
