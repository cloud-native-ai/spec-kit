# `/speckit.goal`

Author and manage **project-level goal definitions**: the sole entry for creating, viewing, modifying, and migrating a goal, plus coordinating teams that share one.

- **Source of truth**: `templates/commands/goal.md`
- **Engine**: `scripts/python/goal-utils.py`
- **Concept authority**: `.specify/shared/definitions/goal-definitions.md` (read-only — the command links to it and never restates it)
- **Feature**: 041 Goal Registry · **Requirement**: `037-goal-registry`

## What a goal is, in one paragraph

A goal is a project-level **authored fact source** stating a desired end outcome and how to tell it has been reached. It is composed of exactly three parts — objective narrative, zero-or-more verifiable success criteria, and lifecycle state — with identity carried by its directory name. It is not a requirement: a requirement binds what this project's code must implement, while a goal's object is unrestricted and may target the framework itself, codebase-wide convention convergence, or a runtime outcome. The two sit on different planes with no hierarchy and no connecting field.

## Archive layout

```text
.specify/goal/
└── <goal-slug>/
    ├── goal.md        # authored definition — never written by a derived flow
    └── summary/       # derived: the goal-indexed summary, roster, and charts
```

`goal.md` and `summary/` are two faces of one object. The summary refresh's write-set is an allow-list of `summary/**`, which is what makes "the definition is never rewritten" mechanically checkable.

## Modes

| Mode | Purpose | Writes |
|------|---------|--------|
| `create` | archive a new definition | `goal.md` |
| `view` | list the archive or show one goal | nothing |
| `modify` | change objective, criteria, lifecycle state, or Targets | `goal.md` |
| `targets` | add / list / transition the goal's Targets (scope slices) | `goal.md` |
| `migrate` | derive a definition from a team's inline goal and switch the team to a reference | `goal.md` + that `team.md` |
| `coordinate` | propose a territory re-division across teams sharing a goal | nothing until ratified |

Every write passes a preview → confirm gate. `view` is read-only and is the fallback when input is ambiguous.

## Identity

The identity is the directory name: first character alphanumeric, remaining characters limited to `[A-Za-z0-9_.-]`, and a safe path segment. This is the same `goal_slug` grammar the summary generator enforces — one grammar, deliberately not two.

## Lifecycle

```text
(none) ──create──▶ active ──achieve──▶ achieved   (terminal, retained)
                     └─────abandon──▶ abandoned   (terminal, retained)
```

There is no `superseded` state, and deletion is not a transition — terminal goals remain in the archive as the project's goal history.

## Engine reference

```bash
# archive a goal
python3 scripts/python/goal-utils.py create framework-stays-current \
  --objective "The framework this project consumes stays continuously current." \
  --criterion "No pending upstream release older than 30 days." --json

python3 scripts/python/goal-utils.py list                       # enumerate the archive
python3 scripts/python/goal-utils.py validate <goal-slug>        # check one definition
python3 scripts/python/goal-utils.py status   <goal-slug> --set achieved
python3 scripts/python/goal-utils.py criteria <goal-slug> --criterion "<new criterion>"
python3 scripts/python/goal-utils.py targets  <goal-slug> --add "<sub-outcome statement>"
python3 scripts/python/goal-utils.py targets  <goal-slug> --list
python3 scripts/python/goal-utils.py targets  <goal-slug> --set done --id T-001
```

`--repo-root` and `--json` are accepted both before and after the subcommand.

| Exit | Meaning |
|------|---------|
| `0` | ok |
| `2` | input error — invalid identity, duplicate, or a rejected objective |
| `3` | goal not found |
| `4` | validation failed |

## Rejections you should expect

| Situation | Result |
|-----------|--------|
| identity already exists | refused, pointing at the modify path; the existing definition is never overwritten |
| identity breaks the grammar or path safety | refused, naming the rule |
| objective written as a task list | refused as **GD-2** — state the outcome, not the steps |
| objective bundling several objectives | refused as **GD-3** — split into separate goals |
| reopening a terminal goal | refused; terminal goals are retained, not reopened |

Changing criteria never silently replaces them: the prior value is appended to `## History`, so drift stays traceable.

## Empty criteria are legal

A goal may carry an objective and no criteria. The archive records `None provided.`, and consumers must declare the absence rather than inventing criteria. Milestones derived from that goal will be an empty group, honestly labelled.

## Relationship to teams

A team references a goal by declaring `goal_slug` in its `team.md` — identity only, never a copy of the objective. The binding is **N teams : 1 goal**, one-way; the goal side learns its teams by derivation, not by storage. A team serves exactly one goal at a time.

Once two or more teams share a goal, their declared territories must not overlap on writes. `coordinate` detects overlap and proposes a re-division; a human ratifies it, and the ratified division is written back into each `team.md`.

## Targets (scope slices)

A goal MAY additionally carry **Targets** — run-assignable scope slices (`T-<nnn>`, three states, engine-rendered `## Targets` section). The concept — identity grammar, lifecycle, boundary against the criteria axis — is defined once in the concept authority (Target Decomposition); this command owns only the operations: `targets <slug> --add/--list/--set`. Statements pass the same GD-2/GD-3 shape check at slice scale and must not restate a success criterion; terminal goals are read-only; terminal identities are never reused. Runs consume an authorized slice via `/speckit.team run <team> --target T-<nnn>`; a terminal-state reference triggers the review bifurcation (verify by hand; reopen via `--set open` if evidence contradicts) — there is no terminal-execution bypass.

## Out of scope

Driving a host CLI's own goal mechanism from an archived definition is deliberately **not** part of this command. Official documentation confirms the host CLI's `/goal set` accepts inline text only, with no file or identity option, so that integration needs its own requirement.

## See also

- `.specify/shared/definitions/goal-definitions.md` — the concept authority
- `docs/reference/commands/team.md` — the team side of the binding
- `.specify/memory/features/041.md` — Feature detail
