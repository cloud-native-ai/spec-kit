# opencode

- **Agent key:** `opencode`
- **Tier:** 1
- **Agent folder:** `.opencode/` (commands in `.opencode/command`, `.md` files)
- **Official docs:** https://opencode.ai/docs/
- **Captured:** 2026-07-11

> **Link + summary page.** Original summary written for this project; no opencode
> documentation text is reproduced here. Install routes, provider setup and
> keybindings drift — read the official documentation above before acting on a
> detail. `Captured` records when this project last reviewed it.

## What it is (summary)

opencode is an open-source AI coding agent built for the terminal, also offered
as a desktop app and an IDE extension. It is provider-agnostic: you configure the
LLM provider you want, and a curated model list is available for newcomers. The
interaction model separates proposing a change from applying it (a plan mode and
a build mode), and it keeps conversation-level undo/redo and sharing. Themes,
keybindings, formatters and custom commands are configurable.

## Read the official documentation for

- Installation routes per operating system and package manager.
- Provider configuration and authentication.
- Project initialization and the instruction file it writes.
- Modes, custom commands, keybindings and sharing behaviour.

## Spec Kit integration

Note opencode uses the singular `command` directory. Spec Kit renders `/speckit.*`
into `.opencode/command/*.md`. opencode's own `/init` writes an `AGENTS.md`, which
in this repo is a symlink to the canonical `.specify/instructions.md`.
