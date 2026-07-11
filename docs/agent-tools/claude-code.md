# Claude Code

- **Agent key:** `claude`
- **Tier:** 1
- **Agent folder:** `.claude/` (commands in `.claude/commands`, `.md` files)
- **Official docs:** https://docs.claude.com/en/docs/claude-code/overview
- **Product page:** https://code.claude.com/
- **Captured:** 2026-07-11

## Overview

Claude Code is Anthropic's agentic coding tool. It reads your codebase, edits
files, runs commands, and integrates with your development tools. It works across
multiple files and surfaces: **terminal (CLI), IDE extensions (VS Code / JetBrains),
desktop app, and the web**. Each surface connects to the same underlying engine, so
`CLAUDE.md`, settings, and MCP servers work everywhere.

## Installation

Terminal (native install — recommended):

```bash
# macOS, Linux, WSL
curl -fsSL https://claude.ai/install.sh | bash

# Windows PowerShell
irm https://claude.ai/install.ps1 | iex
```

Other options: Homebrew (`brew install --cask claude-code`), WinGet
(`winget install Anthropic.ClaudeCode`), and Linux package managers (apt/dnf/apk).
Native installs auto-update in the background.

IDE: install the "Claude Code" extension for VS Code / Cursor / JetBrains.

## Getting started

```bash
cd your-project
claude          # prompts for login on first use
```

## Key capabilities

- Build features and fix bugs from natural-language descriptions.
- Automate tedious work (write tests, fix lint, resolve conflicts, update deps).
- Git integration: stage changes, write commit messages, branch, open PRs.
- **MCP** (Model Context Protocol) to connect external data/tools.
- Customize with `CLAUDE.md` (memory), **skills** (`/review-pr`), and **hooks**.
- Agent teams / sub-agents; background agents; the Agent SDK for custom agents.
- Composable CLI (`claude -p "..."`) for piping, scripting, and CI use.
- Scheduling via routines / `/loop`; multi-surface handoff (web, mobile, Slack).

## Spec Kit integration

Spec Kit renders `/speckit.*` commands into `.claude/commands/*.md`. The canonical
instructions file `.specify/instructions.md` is exposed to Claude via the `CLAUDE.md`
symlink.
