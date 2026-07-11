# GitHub Copilot

- **Agent key:** `copilot`
- **Tier:** 1
- **Agent folder:** `.github/` (prompts in `.github/prompts`, `*.prompt.md` files)
- **Requires CLI:** no — IDE / web based
- **Official docs:** https://docs.github.com/en/copilot
- **Captured:** 2026-07-11

## Overview

GitHub Copilot is GitHub's AI pair programmer. It answers coding questions, explains
code, suggests fixes, and generates code. It runs in many environments: the GitHub
website, IDEs (VS Code, Visual Studio, JetBrains, etc.), GitHub Mobile, and the
command line via the GitHub CLI Copilot extension.

## Plans & access

Requires a personal GitHub account with a Copilot plan:

- **Copilot Free** — limited features, no subscription.
- **Copilot Pro / Pro+ / Max** — more features, models, and higher request limits.
- Business/Enterprise plans for organizations.

See https://docs.github.com/en/copilot/get-started/plans.

## Usage highlights

- **Copilot Chat** on GitHub: open a file, click the Copilot icon, and ask
  questions like "Explain this file." or "How could I improve this code?"
- Ask about repositories, pull requests, issues, and commits.
- **Inline suggestions** in your IDE as you type.
- **Command line**: use the GitHub CLI Copilot extension
  (https://docs.github.com/en/copilot/how-tos/use-copilot-for-common-tasks/use-copilot-in-the-cli).

## Spec Kit integration

Because Copilot is IDE/web based, Spec Kit skips the CLI install check for this
agent. `/speckit.*` commands render into `.github/prompts/*.prompt.md`, and the
canonical `.specify/instructions.md` is surfaced via `.github/copilot-instructions.md`.
