# Contract: Initialization at Instruction Generation

Covers the hook that satisfies FR-001, FR-013, FR-015 during `/speckit.instructions` (script `scripts/bash/generate-instructions.sh` + `templates/instructions-template.md`).

## C-1 Seed on generation

- When instruction generation runs, `generate-instructions.sh` MUST ensure `.specify/memory/glossary.md` exists, creating it from `templates/glossary-template.md` when absent (delegating to `glossary-utils.py --action init`).
- Creation MUST be non-destructive: an existing glossary is preserved (C-3), never re-scaffolded.

## C-2 Domain-term seeding (prompt step)

- The instructions command SHOULD propose project-specific domain terms observed from existing material (constitution, `features.md`, feature names, high-frequency doc phrases) as `origin=auto`, `status=proposed` entries.
- Common everyday words MUST be excluded (FR-002).
- Each proposed term that collides with an existing entry MUST follow the conflict protocol (see `glossary-protocol.md`) — no silent writes.

## C-3 Non-destructive re-run

- Re-running instruction generation MUST preserve all existing rows, especially `origin=user` rows (FR-013). This mirrors the script's existing `## Project Overview` preservation behavior.

## C-4 Ambient wiring (makes the glossary available to all commands — FR-015)

- `templates/instructions-template.md` MUST include a **Documentation Map** row for the glossary:

  ```
  | **Glossary** | `.specify/memory/glossary.md` | Project vocabulary anchor & domain dictionary | Canonical terms, homophone/confusable variants, meanings; voice-input correction source |
  ```

- Because `generate-instructions.sh` renders `.specify/instructions.md` and symlinks it to `CLAUDE.md`, `QWEN.md`, `QODER.md`, `AGENTS.md`, and `.github/copilot-instructions.md`, this single row makes the glossary ambient context for every supported agent — the same mechanism that makes the constitution ambient. No per-command runtime change is required for reading.

## C-5 Mirror discipline

- `templates/glossary-template.md` and `templates/instructions-template.md` edits MUST be dual-written to their `.specify/templates/` mirrors per the project mirror-sync map.
