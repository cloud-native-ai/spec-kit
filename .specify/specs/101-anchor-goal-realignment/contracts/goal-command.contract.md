# Contract — `/speckit.goal` (four modes)

**Owner of the concept**: `shared/definitions/goal-definitions.md` (rewritten by this feature).
**Owner of the mode mechanics**: `skills/internal/manage-goal/SKILL.md` (rewritten by this feature).
This contract fixes the **command surface** only.

## C-13 — Delivery surface

| Artifact | Path | Notes |
|----------|------|-------|
| Canonical template | `templates/commands/goal.md` (rewritten) | the only authored copy |
| Per-tool copies | `.claude/commands/speckit.goal.md`, `.github/prompts/speckit.goal.prompt.md`, `.qoder/commands/speckit.goal.md`, `.opencode/command/speckit.goal.md` | regenerated |
| Delegated skill | `skills/internal/manage-goal/SKILL.md` (rewritten) → `.specify/skills/internal/manage-goal/**` | mirrored |
| Reference page | `docs/reference/commands/goal.md` (rewritten) | authored |

## C-14 — Mode set (exactly four)

`argument-hint` lists, and the body exposes, exactly `create` · `view` · `modify` · `status`. No
fifth mode, no alias to an anchor mode.

## C-15 — Named rejection ([[STR-007]])

An invocation naming any Anchor-only mode — `targets`, `migrate`, `migrate-archive`,
`coordinate` — MUST fail with the literal string `anchor-only-mode`, MUST name `/speckit.anchor`
as the correct entry, MUST exit non-zero (2), and MUST write nothing. It MUST NOT fall back to
`view` or to any read rendering (FR-020, SC-002).

The rejection is the **command's** behaviour; a contract test invokes
`/speckit.goal <anchor-only-mode>` in a fixture repository, asserts exit ≠ 0, asserts stderr
contains both `anchor-only-mode` and `/speckit.anchor`, and asserts the store trees are unchanged
(mtime + content digest).

## C-16 — Mode behaviours

| Mode | Surface obligation |
|------|--------------------|
| `create` | writes `.specify/goals/<goal-slug>/goal.md` through the engine; guidance may be step-shaped; ≥1 completion condition required |
| `view` | read-only; no slug lists the Goal store and nothing else |
| `modify` | edits guidance / completion conditions through the engine; prior value recorded in `## History`; emptying the condition set requires explicit user approval |
| `status` | with no `--set`, reports lifecycle state; with `--set active\|achieved\|abandoned`, transitions it; terminal states are retained, and reopening is limited to a `human`-owned definition |

## C-17 — Write boundary

`/speckit.goal` writes only `.specify/goals/**` definition files (through the engine). It MUST NOT
write the anchor store or any team definition (FR-021). A caller naming `--scope anchor` gets the
engine's `cross-layer-write` refusal (exit 2); the command never silently redirects the write.

## C-18 — Skill surface

`manage-goal` exposes the four modes only. It MUST NOT expose Targets, migration, `coordinate`, or
any team operation (FR-022). The skill's previous seven-mode table is deleted, not annotated.

## C-19 — Positioning text

The template and the reference page describe the command as the authoring entry for **action-level,
step-shaped practical guidance** stored in `.specify/goals/`; neither page may describe it as
project-level or as the anchor-archive entry (FR-026, FR-067). A live page that does turns the
residue scan red (class C3).

## C-20 — Refusal to resolve as an Anchor

No command path may make a Goal resolvable through `anchor_slug`: the engine's team-binding
resolution reads the anchor store only (FR-023). A team declaring a Goal slug gets a named failure
from `run-checks`; the disposition step never repoints a binding to a Goal.

A Goal carries **no Anchor pointer**: its schema declares no `anchor_ref` (nor any key naming an
Anchor), and an undeclared key is rejected by the engine's declared-option guard (exit 2, C-34).
The only cross-reference a Goal records is its binding `origin` — the source spec directory. A Goal
is never team-bound, sits outside the control hierarchy, and does not replace the SDD spec / plan /
tasks artifacts; Anchors bind teams, Goals guide action (FR-004, FR-023).

## C-21 — Wrap-up and registration

The `/speckit.goal` probe object and binding are **retained** (unit-id unchanged); the compiled
wrap-up block is regenerated after the registry change. The flow-class ledger row for
`/speckit.goal` and `skill:manage-goal` is updated to the four-mode surface (FR-054, FR-055).

## C-22 — Handoffs

Before: none — a Goal needs no team. After: none by design; work that needs slices or coordination
belongs to an Anchor + Team, and the handoff text points there (FR-016).
