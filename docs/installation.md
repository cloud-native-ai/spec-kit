# Installation Guide

## Prerequisites

- **Linux/macOS** (or Windows)
- AI coding agent: [GitHub Copilot](https://code.visualstudio.com/), [Qwen Code](https://github.com/alibaba/Qwen), or [opencode](https://github.com/opencode)
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
uvx --from git+https://github.com/github/spec-kit.git specify init <project_name> --ai qwen
uvx --from git+https://github.com/github/spec-kit.git specify init <project_name> --ai opencode
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

After initialization, you should see the following commands available in your AI agent:

- `/speckit.requirements` - Create/update the requirements specification (WHAT/WHY) for a feature
- `/speckit.plan` - Generate implementation plans  
- `/speckit.tasks` - Break down into actionable tasks

The `.specify/scripts` directory will contain `.sh` scripts.

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
