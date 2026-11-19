# Claude Code

- **Agent key:** `claude`
- **Tier:** 1
- **Agent folder:** `.claude/` (commands in `.claude/commands`, `.md` files)
- **Official docs:** https://docs.claude.com/en/docs/claude-code/overview
- **Product page:** https://code.claude.com/
- **Captured:** 2026-07-11

> **Link + summary page.** The text below is an original summary written for this
> project, not a reproduction of Anthropic's documentation. Installation routes,
> flags and feature lists change frequently: read the official source above for
> anything you will act on. `Captured` records when this project last reviewed it.

## What it is (summary)

Claude Code is Anthropic's agentic coding tool. It works against a real
repository — reading code, editing files and running commands — and is reachable
from several surfaces (terminal, IDE extensions, desktop and web) that share one
engine, so project instructions, settings and MCP configuration carry across
them. Beyond interactive use it supports non-interactive invocation for
scripting and CI, and it can be extended with project memory files, skills and
hooks.

## Read the official documentation for

- Installation routes per operating system, and update behaviour.
- Authentication and first-run setup.
- The current flag set, non-interactive usage, hooks, skills and MCP support.
- Sub-agent / agent-team and SDK capabilities.

## Spec Kit integration

Spec Kit renders `/speckit.*` commands into `.claude/commands/*.md`. The canonical
instructions file `.specify/instructions.md` is exposed to Claude via the `CLAUDE.md`
symlink.
