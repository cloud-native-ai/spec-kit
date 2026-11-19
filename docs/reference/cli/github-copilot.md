# GitHub Copilot

- **Agent key:** `copilot`
- **Tier:** 1
- **Agent folder:** `.github/` (prompts in `.github/prompts`, `*.prompt.md` files)
- **Requires CLI:** no — IDE / web based
- **Official docs:** https://docs.github.com/en/copilot
- **Plans:** https://docs.github.com/en/copilot/get-started/plans
- **Copilot in the CLI:** https://docs.github.com/en/copilot/how-tos/use-copilot-for-common-tasks/use-copilot-in-the-cli
- **Captured:** 2026-07-11

> **Link + summary page.** Original summary written for this project; no GitHub
> documentation text is reproduced here. Plan names, limits and surfaces change
> often — read the official sources above before acting on a detail. `Captured`
> records when this project last reviewed them.

## What it is (summary)

GitHub Copilot is GitHub's AI pair-programming product. It answers questions
about code, explains and suggests changes, and is reachable from several
environments: the GitHub website, IDEs, GitHub Mobile, and a command-line
extension. Access is tied to a GitHub account with a Copilot entitlement; the
free tier and the paid individual tiers differ in feature scope and request
limits, and organizations have their own plans.

For Agent Skills specifically — how Copilot loads packaged skills, and how that
differs from custom instructions — see
[../skills/copilot.md](../skills/copilot.md).

## Read the official documentation for

- Current plans, entitlements and request limits.
- Chat on GitHub, inline suggestions, and IDE-specific setup.
- The GitHub CLI Copilot extension.
- Custom instructions, Agent Skills and other customization mechanisms.

## Spec Kit integration

Because Copilot is IDE/web based, Spec Kit skips the CLI install check for this
agent. `/speckit.*` commands render into `.github/prompts/*.prompt.md`, and the
canonical `.specify/instructions.md` is surfaced via `.github/copilot-instructions.md`.
