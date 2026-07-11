# opencode

- **Agent key:** `opencode`
- **Tier:** 1
- **Agent folder:** `.opencode/` (commands in `.opencode/command`, `.md` files)
- **Official docs:** https://opencode.ai/docs/
- **Captured:** 2026-07-11

## Overview

opencode is an open-source AI coding agent built for the terminal. It is also
available as a desktop app and IDE extension, and works with any LLM provider you
configure. A modern terminal emulator (WezTerm, Alacritty, Ghostty, Kitty) is
recommended.

## Installation

```bash
# install script
curl -fsSL https://opencode.ai/install | bash
```

Also available via Node package managers (`npm install -g opencode-ai`, Bun, pnpm,
Yarn), Homebrew (`brew install anomalyco/tap/opencode`), Arch (`pacman`/AUR), and on
Windows via Chocolatey, Scoop, npm, Mise, or Docker.

## Configure & initialize

opencode works with any LLM provider via API keys; OpenCode Zen is a curated,
verified model list for newcomers.

```bash
# inside the TUI, connect a provider
/connect

cd /path/to/project
opencode
/init            # analyzes the project and writes AGENTS.md
```

## Usage highlights

- **Ask questions** about the codebase using `@file` references.
- **Plan mode** (toggle with `Tab`): proposes an implementation without making
  changes; switch back to **Build mode** to apply it.
- **Undo/redo** changes with `/undo` and `/redo`.
- **Share** a conversation with `/share` (copies a link to your clipboard).
- Customize themes, keybinds, formatters, and custom commands.

## Spec Kit integration

Note opencode uses the singular `command` directory. Spec Kit renders `/speckit.*`
into `.opencode/command/*.md`. opencode's own `/init` writes an `AGENTS.md`, which
in this repo is a symlink to the canonical `.specify/instructions.md`.
