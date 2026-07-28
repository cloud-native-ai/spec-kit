# Codex CLI

- **Agent key:** `codex`
- **Tier:** 1
- **Agent folder:** `.codex/` (commands in `.codex/commands`, `.md` files)
- **Official repo / docs:** https://github.com/openai/codex
- **Documentation:** https://developers.openai.com/codex
- **Captured:** 2026-07-11

## Overview

Codex CLI is a lightweight coding agent from OpenAI that runs locally in your
terminal. Companion surfaces exist: an IDE extension (VS Code, Cursor, Windsurf —
see https://developers.openai.com/codex/ide), a desktop app (`codex app`), and the
cloud-based **Codex Web** agent at https://chatgpt.com/codex.

## Installation

```bash
# macOS / Linux install script
curl -fsSL https://chatgpt.com/codex/install.sh | sh

# Windows PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"
```

Package managers:

```bash
npm install -g @openai/codex        # npm
brew install --cask codex           # Homebrew
```

Prebuilt binaries are also available on the latest GitHub Release (rename the
extracted platform-specific binary to `codex`).

## Getting started

```bash
codex           # select "Sign in with ChatGPT"
```

Recommended auth is signing in with a ChatGPT plan (Plus, Pro, Business, Edu, or
Enterprise). Using an API key is also supported but requires extra setup.

## Docs & resources

- Codex Documentation, Contributing, and "Installing & building" guides linked
  from the repository.
- Licensed under Apache-2.0.

## Spec Kit integration

Spec Kit renders `/speckit.*` commands into `.codex/commands/*.md` with the
`$ARGUMENTS` placeholder convention.
