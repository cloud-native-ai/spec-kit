# Skills System Guide

> **Note**: This file is shipped by Spec Kit and created by `/speckit.instructions` only when absent — your local edits are preserved. It is an explanation document, **not** a registry: nothing here needs to be updated when skills are added or removed.

## Where skills live

Skills ship in two layers, each one directory per skill — `SKILL.md` (YAML frontmatter `name` / `description` + body) plus optional `references/`, `scripts/`, `assets/`:

- **External skills** (for consuming projects and their agents): installed flat at `.specify/skills/<name>/`.
- **Internal skills** (Spec Kit workflow machinery): installed nested at `.specify/skills/internal/<name>/`; not agent-visible — `/speckit.*` workflows consume them via explicit paths only.
- `.github/skills` is a compatibility symlink to `.specify/skills/` for tools that discover skills there.

## Discovery — no registration table

Supported AI agent CLIs discover skills natively (directory scan / skill loaders); Spec Kit maintains **no skill registry** in `instructions.md`. A skill exists iff its directory contains a valid `SKILL.md`. A one-level scan of `.specify/skills/` therefore sees external skills only; internal skills are never registered or discovered by agents. To enumerate installed external skills:

```bash
ls .specify/skills/                       # external skill directories (one level)
head -n 8 .specify/skills/*/SKILL.md      # frontmatter name/description per external skill
```

## Creating & improving

- **Create**: the `create-skills` skill (also powers `/speckit.skills`). Name-collision checks scan existing skill directories and their frontmatter `name` fields — not a registry.
- **Improve**: the `improve-skills` skill, driven by execution feedback and failure cases.
- Generic CLI skills (non–Spec Kit) are loaded by the host agent as-is; Spec-Kit-specific blocks (e.g. the engine-backed `## Feedback` step) follow `.specify/shared/workflow/runtime-mode.md` gating.

## Mirrors (Spec Kit development repositories only)

In repositories that develop skills upstream, canonical sources live in the two root layers `skills/external/<name>/` and `skills/internal/<name>/`, mirrored to `.specify/skills/` by `scripts/python/sync-mirrors.py` (external flat, internal nested). Edit the canonical source, never the mirror; run the sync engine after every change.
