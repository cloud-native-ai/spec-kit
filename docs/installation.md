# Installation Guide

## Prerequisites

- **Linux/macOS** (or Windows)
- AI coding agent: [Claude Code](https://www.anthropic.com/claude-code), [GitHub Copilot](https://code.visualstudio.com/), [Qwen Code](https://github.com/alibaba/Qwen), [opencode](https://github.com/opencode), or [Qoder](https://qoder.com/cli)
- [uv](https://docs.astral.sh/uv/) for package management
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## Installation

### Initialize a New Project

The easiest way to get started is to initialize a new project:

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init <PROJECT_NAME>
```

Or initialize in the current directory:

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init .
# or use the --here flag
uvx --from git+https://github.com/github/spec-kit.git specify init --here
```

### Specify AI Agent

You can proactively specify your AI agent during initialization:

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init <project_name> --ai copilot
uvx --from git+https://github.com/github/spec-kit.git specify init <project_name> --ai claude
uvx --from git+https://github.com/github/spec-kit.git specify init <project_name> --ai qwen
uvx --from git+https://github.com/github/spec-kit.git specify init <project_name> --ai opencode
uvx --from git+https://github.com/github/spec-kit.git specify init <project_name> --ai qoder
```

### Specify Script Type (Shell)

All automation scripts now have Bash (`.sh`) variants.

Auto behavior:

- All OS default: `sh`

Force a specific script type:

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init <project_name> --script sh
```

### Ignore Agent Tools Check

If you prefer to get the templates without checking for the right tools:

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init <project_name> --ai copilot --ignore-agent-tools
```

## Verification

After initialization, you should see the following structure and commands:

**Directory structure**:
- `.specify/scripts/` — Automation scripts (`.sh`)
- `.specify/templates/` — Spec/plan/task templates
- `.specify/skills/` — Installed skills (symlinked to tool-specific paths)
- `.specify/agents/` — Agent workspace with bundled agents (symlinked to `.github/agents/`, `.qoder/agents/`, etc.)
- `.specify/memory/` — Project memory (constitution, features)

**All 15 commands available in your AI agent**:

| Command | Purpose |
|---------|---------|
| `/speckit.constitution` | Establish project governance principles |
| `/speckit.feature` | Manage feature lifecycle and registry |
| `/speckit.requirements` | Create/update the requirements specification (WHAT/WHY) |
| `/speckit.clarify` | Resolve ambiguities in specifications |
| `/speckit.research` | Conduct technical research to inform decisions |
| `/speckit.plan` | Generate implementation plans from specs |
| `/speckit.tasks` | Break down plans into actionable tasks |
| `/speckit.checklist` | Generate quality gate checklists |
| `/speckit.analyze` | Cross-artifact consistency checks |
| `/speckit.implement` | Execute tasks with built-in validation |
| `/speckit.review` | Review implementation against specs and plan |
| `/speckit.agents` | Generate role-based agents or create custom agents |
| `/speckit.skills` | Create or refresh project skills |
| `/speckit.tools` | Define or discover reusable tools |
| `/speckit.instructions` | Generate/update AI agent instructions and symlinks |

**Next step**: Run `/speckit.agents` (no arguments) in your AI agent to generate six role-based development workflow agents tailored to your project's context.

## Troubleshooting

### Git Credential Manager on Linux

If you're having issues with Git authentication on Linux, you can install Git Credential Manager:

```bash
#!/usr/bin/env bash
set -e
echo "Downloading Git Credential Manager v2.6.1..."
wget https://github.com/git-ecosystem/git-credential-manager/releases/download/v2.6.1/gcm-linux_amd64.2.6.1.deb
echo "Installing Git Credential Manager..."
sudo dpkg -i gcm-linux_amd64.2.6.1.deb
echo "Configuring Git to use GCM..."
git config --global credential.helper manager
echo "Cleaning up..."
rm gcm-linux_amd64.2.6.1.deb
```
