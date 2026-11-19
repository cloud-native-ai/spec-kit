# Hermes Agent

- **Agent key:** `hermes`
- **Tier:** 2
- **Agent folder:** `.hermes/` (commands in `.hermes/commands`, `.md` files)
- **Official docs:** https://hermes-agent.nousresearch.com/docs/
- **GitHub:** https://github.com/NousResearch/hermes-agent
- **Captured:** 2026-07-11

> **Link + summary page.** Original summary written for this project; no Nous
> Research documentation text is reproduced here. Install routes, backends,
> integrations and tool counts drift — read the official sources above before
> acting on a detail. `Captured` records when this project last reviewed them.

## What it is (summary)

Hermes Agent is Nous Research's autonomous agent, designed to run unattended on
infrastructure you choose — from a small VPS to a GPU cluster or a serverless
runtime — rather than being tethered to an editor. Its distinguishing idea is a
learning loop: the agent curates its own memory, creates and improves skills from
experience, and recalls across sessions. It reaches users through messaging
platforms via a gateway, can delegate work to isolated sub-agents, supports MCP
and scheduled automations, and consumes skills in the open Agent Skills format.

## Read the official documentation for

- Desktop and command-line installation, and the guided setup path.
- Terminal backends and hosted/serverless execution options.
- Messaging-platform integrations and the tool gateway.
- Memory, skill creation and the learning loop.
- Sub-agent delegation, MCP support and scheduling.

## Spec Kit integration

Spec Kit renders `/speckit.*` commands into `.hermes/commands/*.md` with the
`$ARGUMENTS` placeholder convention.
