# /speckit.instructions

Generate or update project instructions and compatibility symlinks, ensuring a consistent AI context across all supported tools.

## When to Use

- After `specify init` to generate the initial project instructions
- After template, documentation, or configuration updates to refresh AI context
- When compatibility symlinks need to be recreated
- To sync project-wide AI instructions across Claude Code, GitHub Copilot, Qwen Code, opencode, and Qoder

## Syntax

```text
/speckit.instructions [instruction scope or audience]
```

`[instruction scope or audience]` is optional:
- Empty: comprehensive creation/update of the full instructions file
- With content: update only the requested sections, keeping unrelated sections untouched

## Execution Flow

1. **Setup** — Runs `generate-instructions.sh` to ensure the basic directory structure, `.copilotignore`, and template `.specify/instructions.md` exist. Creates symlinks for supported AI tools.

2. **Analyze project context**:
   - Reads `README.md` for project purpose and features
   - Inspects configuration files (`pyproject.toml`, `package.json`, etc.) for tech stack
   - Checks `.specify/memory/constitution.md` for mandated project rules
   - Checks `.specify/memory/features.md` for feature status
   - Only considers `.specify/` at the project root (ignores subdirectory instances)

3. **Update instructions content**:
   - Fills placeholders with concrete details from analysis
   - Updates Documentation Map with correct file references
   - Preserves Tools and Skills managed ranges (marker comments intact)
   - Incorporates user input for targeted sections

4. **Validation** — Ensures well-formatted Markdown that clearly describes the project to a fresh AI instance.

5. **Report** — Outputs the instructions file path and confirms symlink status for all supported AI tools.

## Update Strategy

| Mode | Behavior |
|------|----------|
| Full update (no arguments) | Auto-updates Documentation Map, Tech Stack, Key Directories, Build/Test commands. Preserves custom notes and registries. |
| Partial update (with arguments) | Modifies only requested sections, leaves everything else untouched. |

## Symlink Model

The canonical file is `.specify/instructions.md`. Compatibility files are symlinks:

| Symlink | Target Tool |
|---------|-------------|
| `CLAUDE.md` | Claude Code |
| `.github/copilot-instructions.md` | GitHub Copilot |
| `QWEN.md` | Qwen Code |
| `QODER.md` | Qoder |

## Output Artifacts

| Artifact | Location |
|----------|----------|
| Instructions file | `.specify/instructions.md` |
| Compatibility symlinks | `CLAUDE.md`, `.github/copilot-instructions.md`, etc. |

## Error Handling

- **Critical (stops)**: Cannot write instructions file, required metadata unreadable, permission denied
- **Warning (continues)**: Setup script non-zero but prerequisites exist, empty tool/skill docs, symlinks already valid

## Prerequisites

- Run when you need to (re)generate project-wide AI instructions or compatibility symlinks

## Next Steps

- Run [`/speckit.skills`](skills.md) to populate the Tools and Skills sections based on the project scan
