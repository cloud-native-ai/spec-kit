# iFlow CLI

- **Agent key:** `iflow`
- **Tier:** 2
- **Agent folder:** `.iflow/` (commands in `.iflow/commands`, `.md` files)
- **Official docs:** https://platform.iflow.cn/en/cli/quickstart
- **GitHub:** https://github.com/iflow-ai/iflow-cli
- **Captured:** 2026-07-11

## Overview

iFlow CLI is a terminal-based AI assistant (from an Alibaba-affiliated team) that
analyzes code, executes programming tasks, and handles file operations. It supports
slash commands, `@file` references, shell passthrough (`!`), subagents (`$`), MCP
extensions, and a "yolo" mode for autonomous execution.

## Installation

System requirements: Node.js 22+, 4GB+ RAM, internet connection.

```bash
# macOS / Linux — one-click installer
bash -c "$(curl -fsSL https://gitee.com/iflow-ai/iflow-cli/raw/main/install.sh)"

# If Node.js 22+ is already installed
npm i -g @iflow-ai/iflow-cli@latest
```

Windows: install Node.js 22+, then `npm install -g @iflow-ai/iflow-cli@latest`
(Windows Terminal recommended). Verify with `iflow --version`.

## Setup & sign in

```bash
iflow           # start the CLI, then choose a login method
```

Login methods:

1. **Login with iFlow** (recommended) — full features (WebSearch, WebFetch,
   multimodal, tool-calling optimization) via browser OAuth.
2. **iFlow API Key** — same features; key expires in 7 days (good for servers).
3. **OpenAI-compatible API** — use your own endpoint; WebSearch/WebFetch/multimodal
   not available.

## First tasks

```bash
cd your-project/
iflow
/init                                   # analyze project structure
!ls -la                                 # run a shell command inside the CLI
```

## Common commands

| Command | Function |
|---------|----------|
| `/help`   | View help |
| `/init`   | Analyze project structure |
| `/clear`  | Clear conversation history |
| `/exit`   | Exit the CLI |
| `!command`| Execute a system command |

iFlow CLI auto-checks and updates on start; manual update: `npm i -g @iflow-ai/iflow-cli`.

## Spec Kit integration

Spec Kit renders `/speckit.*` commands into `.iflow/commands/*.md` with the
`$ARGUMENTS` placeholder convention.
