# 🌱 Spec Kit

*Build high-quality software faster.*

**An open source toolkit built around Spec-Driven Development (SDD): requirements, plans, tasks, and implementation connect through structured templates and `/speckit.*` commands, so AI progresses around clear intent instead of one-off vague prompts.**

Based on [github.com/github/spec-kit](https://github.com/github/spec-kit.git) with multiple custom extensions — thanks to the original contributors.

## 📚 Documentation Navigation

| I want to... | Go to |
|--------------|-------|
| Install the `specify` CLI | [docs/tutorials/installation.md](docs/tutorials/installation.md) |
| Follow the quick start walkthrough | [docs/tutorials/quickstart.md](docs/tutorials/quickstart.md) |
| Understand concepts & methodology (SDD, vibe coding, better harness, docs model, upstream, security) | [docs/concepts/](docs/concepts/) |
| Accomplish a specific task | [docs/tasks/](docs/tasks/) |
| Look up exact references (commands, CLI tools, skills, agents, teams, glossary) | [docs/reference/](docs/reference/) |
| Understand why a design decision was made | [docs/decisions/](docs/decisions/) |
| Contribute to the project | [CONTRIBUTING.md](CONTRIBUTING.md) |

## 🏗 Architecture

→ See [ARCHITECTURE.md](ARCHITECTURE.md) (one page) and [docs/concepts/](docs/concepts/).

## 🔧 Core Features

- **Specification-Driven Development**: requirements → plan → tasks → implementation workflow
- **AI Agent Integration**: 8 supported AI coding assistants
- **Extensible Skills & Agents**: managed via `/speckit.skills` / `/speckit.agents`
- **Documentation Management**: `/speckit.docs` reconcile engine ([ADR-0001](docs/decisions/0001-adopt-docs-taxonomy.md))

Full feature roadmap: `.specify/memory/features.md` (single source of truth).

## 🤖 Supported AI Agents

**Tier 1**: [Claude Code](https://www.anthropic.com/claude-code) · [Codex CLI](https://github.com/openai/codex) · [Qoder CLI](https://qoder.com/cli) · [GitHub Copilot](https://code.visualstudio.com/) · [opencode](https://opencode.ai/)
**Tier 2**: [Qwen Code](https://github.com/QwenLM/qwen-code) · Hermes Agent · iFlow

## 📦 Installation

See [docs/tutorials/installation.md](docs/tutorials/installation.md).

## 🤝 Contributing & Support

See [CONTRIBUTING.md](CONTRIBUTING.md); support via the [upstream support guide](https://github.com/github/spec-kit/blob/main/SUPPORT.md).

## 📄 License

MIT — see [LICENSE](LICENSE).
