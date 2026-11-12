# `/speckit.goal`

Author and manage **action-level Goal definitions** — the sole entry for creating, viewing, modifying, and reporting or transitioning the lifecycle state of short-horizon practical guidance.

- **Source of truth**: `templates/commands/goal.md`
- **Engine**: `scripts/python/goal-utils.py` (sole definition writer)
- **Concept authority**: `.specify/shared/definitions/goal-definitions.md` (read-only — the command links to it and never restates it)
- **Delegated skill**: `skills/internal/manage-goal/SKILL.md` (mode mechanics)

## What a Goal is, in one paragraph

A Goal is an **action-level, short-horizon authored fact source**: the executable practical guidance a run follows next, plus at least one verifiable completion condition and a lifecycle state. Guidance **may be step-shaped** — a numbered sequence is a legitimate Goal shape here, because a Goal tells a run what to do rather than where the project ends up. The project-level, long-horizon end state is a different concept with a different entry: `/speckit.anchor`. Composition, identity, the store, the section layout and the neighbours are owned by the concept authority above; this page describes only the command surface and links there for every fact.

## Archive layout

```text
.specify/goals/
└── <goal-slug>/
    └── goal.md        # authored definition — never written by a derived flow
```

The store and the identity grammar are owned by the concept authority; the engine is the only writer.

## Modes (exactly four)

| Mode | Purpose | Writes |
|------|---------|--------|
| `create` | archive a new action-level Goal | `goal.md` |
| `view` | list the Goal archive, or show one Goal | nothing |
| `modify` | change the guidance narrative or the completion conditions | `goal.md` |
| `status` | report lifecycle state, or transition it | `goal.md` (`--set` only) |

Every write is previewed before it lands (preview is disclosure, not a blocking gate); `view` and a `status` report are read-only, and `view` is the fallback when input is ambiguous.

## Anchor-only modes are refused by name

`targets`, `migrate`, `migrate-archive` and `coordinate` belong to `/speckit.anchor`. Naming one of them on `/speckit.goal` fails with a **named refusal** (`anchor-only-mode`), exits `2`, writes nothing, and points at `/speckit.anchor` — it never silently falls back to `view`. The executable subject of that refusal is the engine's read-only `command-mode --command goal --mode <mode>` action; the declared mode set itself is read from this command's `argument-hint`.

## Identity

The identity is the directory name (`goal-slug`). The grammar and path-safety rules are the engine's (`python3 scripts/python/goal-utils.py --help`); there is one identity grammar shared by the archive layers, not one per command.

## Lifecycle

`active` / `achieved` / `abandoned` — the shared value set and its transition discipline are owned by `.specify/shared/definitions/anchor-definitions.md` and cited from the concept authority. Terminal Goals are retained in the archive; deletion is not a lifecycle transition. Reopening a terminal Goal (`--set active`) is allowed only for a human-owned Goal — the engine enforces it and every transition appends a history line.

## Engine reference

```bash
# archive a Goal
python3 scripts/python/goal-utils.py goal-create tighten-local-loops \
  --guidance "1. Collect the slow-loop samples. 2. Cut the per-cycle overhead." \
  --done "All sampled loops finish under one second." --json

python3 scripts/python/goal-utils.py goal-list                      # enumerate the Goal archive
python3 scripts/python/goal-utils.py goal-view <goal-slug>          # render one Goal
python3 scripts/python/goal-utils.py goal-status <goal-slug>        # report lifecycle state
python3 scripts/python/goal-utils.py goal-status <goal-slug> --set achieved
python3 scripts/python/goal-utils.py goal-modify <goal-slug> --guidance "<revised guidance>"
python3 scripts/python/goal-utils.py goal-modify <goal-slug> --done "<replacement condition>"
```

`--repo-root` and `--json` are accepted both before and after the subcommand. `--scope` accepts the closed member set owned by `.specify/shared/definitions/anchor-definitions.md` § Archive Layers — this page does not enumerate it; `--scope auto` is read-only and every write action refuses under it. For a bare slug the engine resolves the Goal layer with `--scope goals`.

| Exit | Meaning |
|------|---------|
| `0` | ok |
| `2` | input error — invalid identity, duplicate, undeclared key, or a refusal |
| `3` | not found |
| `4` | validation failed |
| `5` | blocked |

## Rejections you should expect

| Situation | Result |
|-----------|---------|
| identity already exists | refused, pointing at the modify path; the existing definition is never overwritten |
| `create` without a completion condition | refused — at least one `--done` is required |
| an argument-less `goal-modify` | exits `2`; it is never read as a view entry and never empties anything |
| emptying the completion conditions | requires the explicit `--clear-done` flag **and** the user's approval (`--clear-done` together with `--done` also exits `2`) |
| reopening a terminal Goal owned by a tool | refused; only a human-owned Goal may be reopened |
| an undeclared key such as `anchor_ref` | refused with exit `2` — a Goal carries no pointer to an Anchor |
| naming an Anchor-only mode | named refusal, exit `2`, zero writes, pointing at `/speckit.anchor` |

Changing the guidance or the conditions never silently replaces them: the prior value is appended to `## History`, so drift stays traceable.

## Step-shaped guidance is legal

A Goal's guidance is practical instruction — it may be a sequence of steps, and no `outcome, not steps` check runs on it. The shape check applies to the completion conditions only, which must be verifiable and non-empty at create time. A condition whose measurement route is a named human reviewer is as legitimate as one a program measures.

## Relationship to SDD and teams

A Goal is **parallel to** SDD, not above it: spec/plan/tasks carry deliverable design, a Goal carries action-level guidance, and neither parses the other's identity. A Goal does not enter the control hierarchy, is never bound by a team, and never substitutes for spec artifacts. Team binding and slice coordination are always carried by Anchor + Team (`/speckit.anchor`, `/speckit.team`).

## Write boundary

`.specify/goals/<goal-slug>/goal.md` definitions are written only through this command and the engine. This command never writes the anchor archive or any team definition; those belong to `/speckit.anchor`'s surface.

## See also

- `.specify/shared/definitions/goal-definitions.md` — the concept authority
- `docs/reference/commands/anchor.md` — the Anchor command (seven modes)
- `docs/reference/commands/team.md` — team definition and binding
