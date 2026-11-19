# Agent Skills in GitHub Copilot (VS Code) — source and summary

- **Official documentation:** <https://code.visualstudio.com/docs> (Copilot → customization / Agent Skills)
- **Copilot documentation:** <https://docs.github.com/en/copilot>
- **Open standard:** <https://agentskills.io>
- **Source licence:** VS Code documentation is published under its own Creative
  Commons attribution terms (recorded as CC-BY-3.0-US at review time; confirm
  against the source when online)
- **Source reviewed:** 2026-11-19 (licence review). The earlier snapshot carried
  no capture date.
- **Licence of this page:** MIT (original work of the ai-engine project)

> This page is an **original summary**, not a copy of the vendor's documentation.
> It reproduces no upstream documentation text. Preview status, setting names and
> storage paths drift — verify anything you will act on against the official
> documentation above.

## What the capability is, in outline

GitHub Copilot can load Agent Skills: packaged instructions plus optional scripts
and resources that it pulls into context when a request matches a skill's
description. Because the format is the open Agent Skills standard, the same skill
directory is portable across Copilot in VS Code, Copilot CLI and other
compatible agents.

The distinction that matters when choosing between the two customization
mechanisms: custom instructions state standing preferences (style, conventions)
and apply broadly, while a skill teaches a task-specific capability and is
loaded only when relevant. Skills compose — several can contribute to one
workflow — and their resources are read on demand rather than up front.

## Storage locations in a Spec Kit project

These are **this project's** conventions, not the vendor's defaults:

| Location | Role |
|----------|------|
| `.specify/skills/` | primary copy of every project skill |
| `.github/skills/` | compatibility entry point only; never hosts primary content |
| `${HOME}/.copilot/skills/` | user-level skills, outside the project |

The alias model and its regeneration are owned by
`shared/workflow/symlink-model.md`; never hand-edit a compatibility link.

## Recorded at capture (verify upstream)

- Agent Skills support in VS Code was in preview and gated by the
  `chat.useAgentSkills` setting.
- Copilot selects a skill from its `name` and `description` frontmatter, then
  reads the body, then reads referenced resources only when a step needs them.

## Attribution

VS Code and GitHub Copilot are products of Microsoft / GitHub. Their
documentation is referenced here by link with attribution; the earlier verbatim
snapshot was removed in the 2026-11-19 licence review so that no third-party
documentation text is redistributed in this repository.
