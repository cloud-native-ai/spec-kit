# Qoder CLI

- **Agent key:** `qoder`
- **Tier:** 1
- **Agent folder:** `.qoder/` (commands in `.qoder/commands`, `.md` files)
- **Official docs:** https://docs.qoder.com/en/cli/quick-start
- **Product page:** https://qoder.com/
- **Captured:** 2026-07-11

## Overview

Qoder ( /ˈkoʊdər/ ) is an agentic coding platform for real software development,
combining context engineering with intelligent agents. Beyond its Editor and Quest
workspaces (IDE experience), the **Qoder CLI** lets you build, code, and automate
complex tasks directly from the terminal.

## Installation

```bash
# macOS / Linux
curl -fsSL https://qoder.com/install | bash

# Windows PowerShell
irm https://qoder.com/install.ps1 | iex

# Windows CMD
curl -fsSL https://qoder.com/install.cmd -o install.cmd && install.cmd
```

Supported OS: macOS, Linux, Windows (Windows Terminal). Architectures: arm64, amd64
(Windows on Arm not yet supported). Verify:

```bash
qodercli --version
```

## Sign in

```bash
qodercli
/login          # then: login with browser OR personal access token
```

For automation, set an environment variable:

```bash
export QODER_PERSONAL_ACCESS_TOKEN="your_personal_access_token_here"
```

Get a token at https://qoder.com/account/integrations. `/logout` signs out.

## Upgrade

Auto-update is on by default. Manual: re-run the install script with `-s -- --force`,
or `qodercli update`. Disable via `general.enableAutoUpdate: false` in
`~/.qoder/settings.json`.

## Key capabilities

- Agentic, multi-file code generation, Q&A, and edits.
- **Quest** autonomous delegation for long-running, multi-step tasks.
- **MCP** support and a **Knowledge Engine** that accumulates business knowledge.

## Spec Kit integration

Spec Kit renders `/speckit.*` commands into `.qoder/commands/*.md`. The canonical
instructions file `.specify/instructions.md` is surfaced via `.qoder/project_rules.md`.
