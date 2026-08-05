# Qoder CLI

- **Agent key:** `qoder`
- **Tier:** 1
- **Agent folder:** `.qoder/` (commands in `.qoder/commands`, `.md` files)
- **Official docs:** https://docs.qoder.com/en/cli/quick-start
- **Product page:** https://qoder.com/
- **Captured:** 2026-07-11 (memory sources corrected 2026-08-05 per docs.qoder.com/cli/memory)

> **Qoder CLI ≠ Qoder IDE.** They are two distinct tools that share the `.qoder/` folder. Spec Kit's `qoder` agent key targets the **CLI** (`qodercli` binary). The IDE's instruction format (`.qoder/project_rules.md`) is NOT read by the CLI — see "Project rules & memory sources" below.

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

## Project rules & memory sources (CLI)

Per the CLI memory docs (docs.qoder.com/cli/memory), `qodercli` loads project-level rules from:

| File | Scope |
|------|-------|
| `~/.qoder/AGENTS.md` | User level |
| `<project>/AGENTS.md` | Project level (searched upward from the working directory to the directory containing `.git`) |
| `<project>/AGENTS.local.md` | Project-local, private |
| `<project>/.qoder/rules/**/*.md` | Rule files; frontmatter controls triggering (`alwaysApply`, glob, …) |

- When `AGENTS.md` and `.qoder/rules/` coexist, **both are injected** (additive context). The CLI docs define **no override priority** between them; the "rules win on conflict" statement exists only in the **IDE** docs.
- **`.qoder/project_rules.md` is not a CLI source.** It is the Qoder IDE's old format and does not appear in the CLI docs — there is no CLI-side priority relationship between it and `AGENTS.md`, because the CLI simply never reads it.

## Spec Kit integration

Spec Kit renders `/speckit.*` commands into `.qoder/commands/*.md`. The canonical
instructions file `.specify/instructions.md` is surfaced to the **CLI** via the root
`AGENTS.md` symlink. The `.qoder/project_rules.md` symlink points at the same canonical
file, but it exists only for **Qoder IDE** compatibility — it is redundant for the CLI.
Because both are aliases of `.specify/instructions.md`, no content divergence or
conflict is possible in a Spec Kit project.
