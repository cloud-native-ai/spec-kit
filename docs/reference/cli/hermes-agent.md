# Hermes Agent

- **Agent key:** `hermes`
- **Tier:** 2
- **Agent folder:** `.hermes/` (commands in `.hermes/commands`, `.md` files)
- **Official docs:** https://hermes-agent.nousresearch.com/docs/
- **GitHub:** https://github.com/NousResearch/hermes-agent
- **Captured:** 2026-07-11

## Overview

Hermes Agent is a self-improving autonomous AI agent built by Nous Research. Unlike
an IDE-tethered copilot, it is designed to run anywhere — a $5 VPS, a GPU cluster,
or serverless infrastructure (Daytona, Modal) — and grow more capable the longer it
runs via a built-in **learning loop** that creates and improves skills from
experience and builds persistent, cross-session memory.

## Installation

Desktop (Windows / macOS): download the Hermes Desktop installer from the website.

Command-line only:

```bash
# Linux / macOS / WSL2 / Android (Termux)
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# Windows (native, PowerShell)
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

Fastest path to a working agent — one OAuth covers a model plus the four Tool
Gateway tools (web search, image generation, TTS, browser):

```bash
hermes setup --portal
```

## Key features

- **Closed learning loop** — agent-curated memory with periodic nudges, autonomous
  skill creation, skill self-improvement during use, FTS5 cross-session recall, and
  Honcho dialectic user modeling.
- **Runs anywhere** — 6 terminal backends: local, Docker, SSH, Daytona, Singularity,
  Modal (Daytona/Modal offer serverless hibernation).
- **Lives where you do** — 20+ messaging platforms from one gateway (Telegram,
  Discord, Slack, WhatsApp, Signal, Matrix, Email, SMS, Feishu, WeCom, Teams…).
- **Delegates & parallelizes** — spawn isolated subagents; Programmatic Tool Calling
  via `execute_code`.
- **Open standard skills** — compatible with agentskills.io; portable and shareable.
- **MCP support**, voice mode, scheduled automations (built-in cron), and 60+
  built-in tools.

## Resources for LLMs

- `/llms.txt` — curated index of doc pages (~17 KB).
- `/llms-full.txt` — all doc pages concatenated (~1.8 MB).

## Spec Kit integration

Spec Kit renders `/speckit.*` commands into `.hermes/commands/*.md` with the
`$ARGUMENTS` placeholder convention.
