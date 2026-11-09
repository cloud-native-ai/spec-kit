# Directive record — merge 092 into 090 and rename goal → anchoring (2026-11-09)

**User directive (verbatim intent)**: merge `.specify/specs/092-non-disposable` into
`.specify/specs/090-re-anchoring` concurrently; replace the original "goal" concept with
**anchoring** (锚点); the "temporary goal/team" wording from 085 is inaccurate — goals and teams
have no "temporary" property, only a scope property; the former "global goal" becomes
**anchoring**, all former "temporary goals" become ordinary goals, and `.specify/goal/` becomes
`.specify/anchoring/`.

## Inventory (measured 2026-11-09)
- 46 files reference `092-non-disposable`.
- 262 files reference one of `.specify/goal`, `spec/goal`, `goal_slug`, "temporary goal", "临时 goal", `temp_goal`.
- `.specify/goal/` holds the global archive (3+ slug directories); spec-local stores live at `<spec>/goal/<slug>/goal.md` and `<spec>/team/<slug>/team.md`.

## Closed rename map (proposed, one owner each)
| old | new | owner |
|---|---|---|
| `.specify/goal/<slug>/goal.md` (global archive) | `.specify/anchoring/<slug>/anchor.md` | `goal-utils.py` + `goal-definitions.md` |
| "global goal" phrasing | "anchoring (锚点)" | `goal-definitions.md` (single owner) |
| "temporary goal" | "goal" (scope = spec) | 085 contracts + create-team/create-agent refs |
| "temporary team" | "team" (scope = spec) | same |
| `temp_goal_slug` / `temp_team_slug` (state spine) | `goal_slug` / `team_slug` | driver spine writer |
| spec-local `goal/` and `team/` paths | unchanged | — |

## Execution waves (concurrent, disjoint territories)
1. **W1 engine/owner (serial gate)**: `goal-utils.py` (paths + scope resolution + migration of the archive), `goal-definitions.md`, `shared/declarations/facts/` goal facts; one atomic commit so the old path never coexists half-renamed.
2. **W2 docs+tests (parallel, after W1)**: 085 contracts/team refs; 090/092 contracts; `templates/commands/{goal,team}.md`; driver references; tests split by directory (`tests/contract`, `tests/unit`, `tests/integration`).
3. **W3 spec merge**: move 092's artifacts into `090-re-anchoring` as additional sections (requirements FRs appended with a subsection, contracts merged with clause-id namespacing, tasks renumbered, evidence copied), delete the 092 directory, and update the registry to one feature.
4. **W4 verification**: shrink the 262 references to zero for the renamed spellings, run the sharded suite against the baseline.

## Defaults taken unless the user redirects
- Slug kept: `090-re-anchoring`; 092 is absorbed (its FR/SC/clauses are appended, not renumbered away).
- Archive file name: `anchor.md` (parallel to `goal.md`), keeping `goal_slug` as the field name for spec-local goals (only the global archive concept is renamed).
- The rename is a breaking change and needs a MINOR constitution/instruction note only if a principle text names the old path (currently only the owner docs do).
