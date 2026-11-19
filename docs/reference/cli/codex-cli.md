# Codex CLI

- **Agent key:** `codex`
- **Tier:** 1
- **Agent folder:** `.codex/` (commands in `.codex/commands`, `.md` files)
- **Official repo / docs:** https://github.com/openai/codex
- **Documentation:** https://developers.openai.com/codex
- **IDE extension:** https://developers.openai.com/codex/ide
- **Cloud agent (Codex Web):** https://chatgpt.com/codex
- **Upstream licence:** Apache-2.0 (the product, not this page)
- **Captured:** 2026-07-11

> **Link + summary page.** Original summary written for this project; no OpenAI
> documentation text is reproduced here. Install routes, authentication options
> and flags drift — read the official sources above before acting on a detail.
> `Captured` records when this project last reviewed them.

## What it is (summary)

Codex CLI is OpenAI's lightweight coding agent for the terminal: it runs locally
against the working repository and is driven by natural-language requests.
Companion surfaces exist around the same agent — an IDE extension, a desktop
app, and a cloud-hosted web agent — so a task can move between local and hosted
execution. Authentication is oriented around a ChatGPT plan, with API-key usage
also possible.

## Read the official documentation for

- Installation routes (install script, package managers, prebuilt release binaries).
- Sign-in options and the differences between plan-based and API-key access.
- The current command/flag set, sandboxing and approval behaviour.
- Contributing and building from source.

## Spec Kit integration

Spec Kit renders `/speckit.*` commands into `.codex/commands/*.md` with the
`$ARGUMENTS` placeholder convention.
