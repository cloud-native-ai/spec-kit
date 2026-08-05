# Contract: `/speckit.goal` Command

**Requirement**: 037-goal-registry | **FRs**: FR-016…FR-019, FR-021, FR-025, FR-026
**Source of truth**: `templates/commands/goal.md`
**Classification**: complex (process-interaction) command — carries the `## Feedback` and `## Documentation` wrap-up steps, like `/speckit.team`

## Positioning

`/speckit.goal` is the sole authoring entry for project-level goal definitions. It owns create, modify, view, and migrate. No second authoring path exists — not a skill, not a script, not `/speckit.team`.

## Modes

| Mode | Purpose | Primary output |
|------|---------|----------------|
| `create` | archive a new goal definition | `.specify/goal/<goal-slug>/goal.md` |
| `modify` | change an existing definition's objective, criteria, or lifecycle state | the same file, with a `## History` entry when criteria change |
| `view` | list the archive, or show one goal with its state and criteria count | terminal output only; no writes |
| `migrate` | derive a definition from a team's inline goal and switch that team to a reference | new `goal.md` + edited `team.md` |

Mode is inferred from the invocation and confirmed with the user before any write. Ambiguous input resolves to `view`, which is read-only.

## Normative rules

- **GC-1** Exactly one authoring entry. Any additional write path to `.specify/goal/**` is a contract violation.
- **GC-2** `view` performs zero writes.
- **GC-3** `create` with an existing identity is rejected and points at `modify`. The existing definition is never overwritten.
- **GC-4** `migrate` is per-team and optional. It MUST NOT require a full migration of all teams before the mechanism is usable, and it MUST NOT force removal of the team's inline goal — retention is the user's choice.
- **GC-5** `migrate` preserves meaning: the team's resolved objective and criteria before and after are semantically equivalent.
- **GC-6** The command distinguishes "defined but not yet advanced" from "in progress" when reporting a goal's state.
- **GC-7** Any new command-line option MUST avoid the name `--goal`, which is already claimed with two different meanings — `build-summary-input.py --goal` is a goal identity to aggregate, `match-team-preset.py --goal` is objective text. Goal identity is passed positionally, so no colliding option is introduced.
- **GC-8** Concept-level statements in the command's own prose link to `shared/definitions/goal-definitions.md`. The command MUST NOT restate the Goal concept as a second account.
- **GC-9** The command never writes a team's territory. Ratifying a coordination proposal is the only path to a territory edit, and it writes `team.md`.

## Delivery

| Artifact | Path | Nature |
|----------|------|--------|
| source of truth | `templates/commands/goal.md` | authored |
| runtime mirror | `.specify/templates/commands/goal.md` | generated |
| Claude Code | `.claude/commands/speckit.goal.md` | generated |
| GitHub Copilot | `.github/prompts/speckit.goal.prompt.md` | generated |
| Qoder CLI | `.qoder/commands/speckit.goal.md` | generated |
| opencode | `.opencode/command/speckit.goal.md` | generated |
| Qwen Code | `.qwen/commands/speckit.goal.toml` | generated, TOML form, `{{args}}` argument style |
| reference doc | `docs/reference/commands/goal.md` | authored |

- **GD-1** Fan-out is performed only by `python3 scripts/python/sync-mirrors.py --write` (which delegates per-tool copies to `regen-command-copies.py`). Manual dual-writing of any copy is a contract violation.
- **GD-2** Every generated copy carries the `AUTO-GENERATED` header naming `templates/commands/goal.md`.
- **GD-3** Only the five tool directories above are produced, because the regeneration script targets directories that already exist. `.hermes/commands`, `.iflow/commands`, and `.codex/commands` are absent in this repository and are correctly skipped.
- **GD-4** `docs/reference/commands/` holds one file per command with no index; `goal.md` joins that 1:1 set. Command tables in `docs/tutorials/quickstart.md` and `docs/tutorials/installation.md` each gain one row.
- **GD-5** `tests/contract/test_feedback_command_classification.py` hard-codes the complex/simple command sets with length assertions. `goal` is added to the complex set and the assertion count is advanced accordingly.

## Verification

| Check | Command | Expected |
|-------|---------|----------|
| mirror + copy parity | `python3 scripts/python/sync-mirrors.py --check` | exit 0 |
| generated headers | grep `AUTO-GENERATED` in each of the 5 copies | present, naming the source template |
| dynamic command coverage | `pytest tests/integration/test_ai_tools_command_coverage.py` | passes without edits (the suite globs `templates/commands/`) |
| classification pin | `pytest tests/contract/test_feedback_command_classification.py` | passes with the advanced count |
| single entry | count of write paths into `.specify/goal/**` across commands, skills, and scripts | exactly 1 |
