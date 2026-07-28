# Qwen Code

- **Agent key:** `qwen`
- **Tier:** 2
- **Agent folder:** `.qwen/` (commands in `.qwen/commands`, `.toml` files, `{{args}}` placeholder)
- **Official repo / docs:** https://github.com/QwenLM/qwen-code
- **Captured:** 2026-07-11

## Overview

Qwen Code is an open-source AI coding agent that lives in your terminal. Originally
based on Google Gemini CLI, it has evolved into an independent multi-protocol,
multi-platform agent framework. It supports OpenAI, Anthropic, Gemini, and Qwen
APIs — plus any third-party provider or local model (Ollama / vLLM) — switchable at
runtime. Features include Auto-Memory, Auto-Skills, SubAgents, Agent Teams, and MCP.

## Installation

```bash
# Linux / macOS standalone installer
curl -fsSL https://qwen-code-assets.oss-cn-hangzhou.aliyuncs.com/installation/install-qwen-standalone.sh | bash

# Windows (PowerShell)
irm https://qwen-code-assets.oss-cn-hangzhou.aliyuncs.com/installation/install-qwen-standalone.ps1 | iex

# npm (Node.js 22+)
npm install -g @qwen-code/qwen-code@latest

# Homebrew
brew install qwen-code
```

## Quick start

```bash
qwen            # launch interactive terminal UI
/auth           # configure provider and API key
```

## Usage modes

| Mode | Command | Use case |
|------|---------|----------|
| Interactive | `qwen` | Terminal UI, `@file` references, slash commands |
| Headless | `qwen -p "..."` | Scripts, CI/CD, batch processing |
| Daemon | `qwen serve` | Shared agent over HTTP+SSE (ACP), multi-client (experimental) |
| IM Bot | `qwen channel` | Telegram, DingTalk, WeChat, Feishu |

Also offers IDE plugins (VS Code / JetBrains / Zed), a desktop app, and SDKs
(TypeScript, Python, Java).

## Capabilities

SubAgents, Agent Teams, dynamic workflows, Auto-Memory, Auto-Skills, hooks, built-in
skills (`/review`, `/batch`, `/loop`, `/bugfix`…), MCP, Plan Mode, LSP integration,
Auto Mode, sandbox, Git worktrees, computer use, headless mode, and session
management. Open-source model and framework with multi-protocol support.

## Spec Kit integration

Qwen Code is the only Spec Kit target that uses **TOML** command files with the
`{{args}}` placeholder. `/speckit.*` commands render into `.qwen/commands/*.toml`;
the canonical `.specify/instructions.md` is surfaced via `QWEN.md`.
