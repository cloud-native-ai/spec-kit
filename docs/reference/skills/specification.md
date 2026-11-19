# Agent Skills Specification — source and summary

- **Authoritative source:** <https://agentskills.io/specification>
- **Upstream repository:** <https://github.com/agentskills/agentskills> (Apache-2.0)
- **Validation tool:** [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref)
- **Licence of this page:** MIT (original work of the ai-engine project)

> This page is an **original summary** written for this project. It reproduces no
> upstream specification text. The upstream specification owns every exact
> constraint — field lengths, character rules, required/optional status — so read
> it there before you rely on a detail. Nothing here is a substitute for it.

## What the format is, in outline

Agent Skills is an open, agent-neutral packaging format for a capability an AI
agent can load on demand. A skill is a directory whose entry point is a single
`SKILL.md`: YAML frontmatter declaring the skill's identity and activation
description, followed by Markdown instructions the agent reads once it decides
the skill applies. Optional sibling directories hold executable scripts,
reference material the agent reads only when needed, and static assets such as
templates or data files.

The design intent is progressive disclosure: a small always-loaded identity
layer, a larger instruction layer loaded on activation, and resources loaded
only when a step actually needs them. That is why the format favours a short
entry file with references one level deep over a single large document.

## How this project uses the format

| Surface | Role |
|---------|------|
| `skills/external/<name>/`, `skills/internal/<name>/` | authored skills (framework source) |
| `.specify/skills/` | runtime projection installed into a project |
| `create-skills` / `improve-skills` skills | authoring and revision workflow |
| `docs/reference/skills/` | this project's own skill documentation |

Project-side conventions that go beyond the upstream format (classification,
`skill_id`, concurrency obligations, mirror parity) are owned by this repository,
not by the specification — see `shared/definitions/skill-reference-definitions.md`
and the `create-skills` skill.

## Attribution

The Agent Skills specification is published by the agentskills project at
<https://agentskills.io/specification> under Apache-2.0. This project links to it
and summarises it in its own words; the earlier verbatim snapshot of that
specification was removed in the 2026-11-19 licence review so that no
third-party specification text is redistributed here.
