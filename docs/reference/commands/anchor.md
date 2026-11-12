# `/speckit.anchor`

Author and manage **Anchor definitions** — the sole authoring entry for the anchor archive: create, view, modify, and manage the Targets of a project-level anchor, migrate a team's inline goal into an Anchor, move spec-local legacy trees into the unified archive, and coordinate teams that serve one Anchor.

- **Source of truth**: `templates/commands/anchor.md`
- **Engine**: `scripts/python/goal-utils.py` (sole definition writer)
- **Concept authority**: `.specify/shared/definitions/anchor-definitions.md` (read-only — the command links to it and never restates it)
- **Delegated skill**: `skills/internal/manage-anchor/SKILL.md` (mode mechanics)

## What an Anchor is, in one paragraph

An Anchor is a **project-level, long-horizon, cross-deliverable authored end state** — a first-class fact source, never a derived artifact — answering *whither*: toward what end state, and to what degree it has been reached. Its composition, the shape rules that govern the objective and its slices, the archive layers, the binding record and the lifecycle are owned by the concept authority above; this page describes only the command surface and links there for every fact. An action-level, step-shaped Goal is a different concept with a different entry: `/speckit.goal`.

## Archive layout

```text
.specify/anchoring/
└── <anchor-slug>/
    ├── anchor.md      # authored definition — never written by a derived flow
    └── summary/       # derived: the anchor-indexed summary, roster, and charts
```

`anchor.md` and `summary/` are two faces of one object. The summary refresh writes only the derived subtree; the definition itself is authored through this command and the engine alone.

## Modes (exactly seven)

| Mode | Purpose | Writes |
|------|---------|--------|
| `create` | archive a new anchor definition | `anchor.md` |
| `view` | list the anchor archive or show one Anchor | nothing |
| `modify` | change the objective narrative, success criteria, or lifecycle state | `anchor.md` |
| `targets` | add / list / transition the Anchor's Targets (run-assignable slices) | `anchor.md` |
| `migrate` | derive an Anchor from a team's inline goal and switch the team to a reference | `anchor.md` + that `team.md` |
| `migrate-archive` | move spec-local legacy goal/team trees into the unified archive | the archive layers + receipts |
| `coordinate` | propose a territory re-division across teams serving one Anchor | nothing until ratified |

Every write is previewed before it lands (preview is disclosure, not a blocking gate); `view` is read-only and is the fallback when input is ambiguous.

**Anchor-only modes have no Goal form.** Naming `targets`, `migrate`, `migrate-archive` or `coordinate` on `/speckit.goal` is refused by name, exits `2`, writes nothing, and points here — it never falls back to a read view. The executable subject of that refusal is the engine's read-only `command-mode --command goal --mode <mode>` action.

## Identity

The identity is the directory name (`anchor-slug`). The grammar and path-safety rules are the engine's (`python3 scripts/python/goal-utils.py --help`); there is one identity grammar shared by the archive layers, not one per command.

## Lifecycle

`active` / `achieved` / `abandoned` — the shared value set and its transition discipline are owned by the concept authority (link, never restate). Terminal Anchors are retained in the archive; deletion is not a lifecycle transition.

## Engine reference

```bash
# archive an anchor
python3 scripts/python/goal-utils.py create framework-stays-current \
  --objective "The framework this project consumes stays continuously current." \
  --criterion "No pending upstream release older than 30 days." --json

python3 scripts/python/goal-utils.py list                          # enumerate the anchor archive
python3 scripts/python/goal-utils.py validate <anchor-slug>        # check one definition
python3 scripts/python/goal-utils.py status   <anchor-slug> --set achieved
python3 scripts/python/goal-utils.py objective <anchor-slug> --set "<revised outcome>"
python3 scripts/python/goal-utils.py criteria <anchor-slug> --criterion "<new criterion>"
python3 scripts/python/goal-utils.py targets  <anchor-slug> --check "<slice statement>"
python3 scripts/python/goal-utils.py targets  <anchor-slug> --add "<slice statement>"
python3 scripts/python/goal-utils.py targets  <anchor-slug> --list
python3 scripts/python/goal-utils.py targets  <anchor-slug> --set done --id T-001
python3 scripts/python/goal-utils.py migrate  <team-slug>
python3 scripts/python/goal-utils.py migrate-archive --dry-run     # then --apply
```

`--repo-root` and `--json` are accepted both before and after the subcommand. `--scope` accepts the closed member set owned by the concept authority (§ Archive Layers) — this page does not enumerate it; `--scope auto` is read-only and every write action refuses under it.

| Exit | Meaning |
|------|---------|
| `0` | ok |
| `2` | input error — invalid identity, duplicate, rejected objective/slice, or a refusal |
| `3` | not found (or a migration interrupted between its steps) |
| `4` | validation failed (or a migration conflict) |
| `5` | blocked |

## Rejections you should expect

| Situation | Result |
|-----------|---------|
| identity already exists | refused, pointing at the modify path; the existing definition is never overwritten |
| objective written as a task list, plan, or phase sequence | refused as **GD-2** — state the outcome, not the steps |
| objective bundling several objectives | refused as **GD-3** — split into separate Anchors |
| a Target statement that would stand as its own end state | refused as **GD-3** — it is a separate Anchor, not a slice |
| emptying the success criteria | requires the explicit `--clear` flag **and** the user's approval; an argument-less `criteria` call exits `2` and never empties anything |

Changing the objective or the criteria never silently replaces them: the prior value is appended to `## History`, so drift stays traceable.

## Success criteria

At least one verifiable criterion — a definition carrying zero is not an Anchor. Criteria are measured **by degree** (thresholds, evaluator scores, progress), never as per-clause pass/fail, and they are **cross-feature**: they are never copied to or from a requirements spec's `SC-xxx`. A criterion whose measurement route is a named human reviewer is as legitimate as one a program measures.

## Targets (optional annex)

An Anchor MAY carry **Targets** — run-assignable scope slices (`T-<nnn>`, engine-rendered `## Targets` section). Targets are an annex, never a fourth composition part: an Anchor without Targets is fully valid. The concept — identity, states, the boundary against the criteria axis — is owned by the concept authority (Target Decomposition). This command owns only the operations: `targets <slug> --add/--list/--check/--set`. Statements pass the same shape rules at slice scale and never restate a criterion; terminal Anchors are read-only; terminal identities are never reused.

## Moving spec-local trees

`migrate-archive` is the one explicit entry that moves spec-local legacy goal/team trees into the unified archive: both kinds in a single call, archive-not-delete, never triggered implicitly by another command. Read the `--dry-run` plan before `--apply`; an interrupted run is resumed by a second call rather than restarted, and a per-definition conflict is a verdict.

## Relationship to teams

A team references its Anchor by declaring `anchor_slug` in its `team.md` — identity only, never a copy of the objective or criteria. The binding is **N teams : 1 Anchor**, one-way; the Anchor side learns its teams by derivation, not by storage. A team serves exactly one Anchor at a time. Once two or more teams serve one Anchor, their declared territories must not overlap on writes: `coordinate` detects overlap and proposes a re-division, a human ratifies it, and the ratified division is written back into each `team.md`.

## Write boundary

`.specify/anchor.md` definitions are written only through this command and the engine. No other command, skill, script or run writes an anchor definition, and this command never writes the action-level Goal store (`.specify/goals/**`) or any team definition except through `migrate`'s declared inline-goal reference. Action-level guidance is `/speckit.goal`'s surface.

## See also

- `.specify/shared/definitions/anchor-definitions.md` — the concept authority
- `docs/reference/commands/goal.md` — the action-level Goal command (four modes)
- `docs/reference/commands/team.md` — the team side of the binding
