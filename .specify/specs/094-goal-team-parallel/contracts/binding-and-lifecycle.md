# Contract — Binding Record, Scope Values and Writability

Owner of the executable rules: `scripts/python/goal-utils.py` (actions `resolve-scope`, `bind`, `create`,
`set-*`, `list`). Consumers: `/speckit.goal`, `/speckit.team`, `sdd-route.py authorize`, `create-team`,
`run-team`, `improve-team`, the SDD loop driver. Concept owner (what these words mean):
`shared/definitions/goal-definitions.md` and `skills/internal/create-team/references/conceptual-model.md`
(FR-024) — this contract fixes behaviour and never re-defines a concept.

Clause ids are `C-NNN` inside this specification's contract namespace and are contiguous across the five
files in `contracts/` (C-1…C-111).

## 1. The binding record ([[STR-001]] `binding`)

- **C-1**: A goal definition and a team definition MUST each carry exactly one binding record in its YAML
  frontmatter under the key `binding`, with exactly three keys: `owner`, `owner_id`, `origin`. A definition
  without a complete binding record MUST be rejected as uninterpretable (exit 2, reason `binding-missing`).

(FR-001, FR-002, FR-003, FR-004)
- **C-2**: `owner` MUST be one of the closed three values `sdd-run` / `command-run` / `human`. Any other value
  is an input error naming the value and the closed set.

(FR-001, FR-002, FR-003, FR-004)
- **C-3**: `owner_id` MUST be a non-empty token matching the state-spine `run_id` form
  (`r<YYYYMMDD>T<HHMMSS>Z-<slice-token>`). The engine MUST NOT re-declare the `run_id` grammar; it MUST validate
  the shape only (R-09) and MUST cite `skills/external/sdd-loop-driver/references/state-awareness.md` as the
  grammar owner. `owner: human` MAY use `owner_id: human`.

(FR-001, FR-002, FR-003, FR-004)
- **C-4**: `origin` MUST be `null` or the basename of an existing directory under `.specify/specs/`. A value
  naming a spec directory that does not exist MUST be refused (exit 2, reason `origin-unresolvable`), never
  silently dropped and never auto-created.

(FR-001, FR-002, FR-003, FR-004)
- **C-5**: `owner`, `owner_id` and `origin` MUST be written only by the engine (FR-003). A command template,
  skill or driver MUST NOT instruct a direct edit of the binding block, and a direct edit MUST be detected by the
  binding validator and reported as `binding-hand-edited`.

(FR-003)
- **C-6**: A binding rewrite action (`bind <kind> <slug> --owner <v> --owner-id <v> [--origin <v>]`) MUST
  change only the three binding lines; every other byte of the definition file MUST stay identical. The
  comparison the rewrite guarantees is defined by SC-009 and measured as "hash of the file minus the binding
  block equals the pre-rewrite hash of the same subtraction".

(FR-003)
- **C-7**: A binding rewrite MUST be refused when the definition is terminal: goal `achieved` / `abandoned`
  refuses a new team binding (the terminal-goal rule), team `archived` refuses any rewrite. The refusal names the
  terminal state.

(FR-026)
- **C-8**: The engine MUST provide one read action that answers "who owns this definition" without reading the
  filesystem layout: `binding <kind> <slug> --json` returns `{kind, slug, owner, owner_id, origin, path,
  archive_layer, lifecycle}`. Every consumer that today infers ownership from a directory MUST switch to this
  action (FR-015).
## 2. Archive layers ([[STR-002]] `archive-scope`)

- **C-9**: The archive-layer value set MUST be the closed set `goal`, `teams`, `auto`. The member named by a
  directory position (`spec`) MUST NOT exist: `--scope spec` MUST fail with argparse's `invalid choice` form and
  exit 2, and the engine MUST NOT offer any alias for it (T-004).

(FR-008, FR-025)
- **C-10**: `--scope goal` MUST resolve the goal root to `.specify/goal`; `--scope teams` MUST resolve the team
  root to `.specify/teams`; both MUST resolve both roots in one `Scope` object so a caller never needs two calls.

(FR-008, FR-025)
- **C-11**: `--scope auto` MUST be read-only and MUST resolve to the single archive layer that contains the
  requested slug; when zero layers contain it the engine exits 2 (`not-found`), when more than one does it exits 2
  (`scope-ambiguous`) naming both layers. `auto` MUST NOT create, rewrite or migrate.

(FR-008, FR-025)
- **C-12**: `--spec-dir` MUST keep being accepted, MUST be used to resolve `origin` and to validate `auto`
  inputs, and MUST NOT decide where a definition lands. Passing `--spec-dir` with a path outside `.specify/specs/`
  MUST be refused (`spec-dir-unresolvable`, exit 2).

(FR-008)
- **C-13**: The engine MUST NOT expose a write target outside `.specify/goal/<slug>/` and
  `.specify/teams/<slug>/` . A caller that asks for a write with `--scope auto` MUST be refused
  (`scope-read-only`, exit 2) — the existing 085 rule survives with the new value names.

(FR-007, FR-008, FR-025)
## 3. Writability (FR-038) and the retired forbidden-path rule

- **C-14**: Writability MUST be computed, never declared: `writable(kind, binding, bound_teams)` returns allowed
  / refused with a reason token. For `kind=teams` it MUST allow the definition's own `owner`; for `kind=goal` it
  MUST allow `owner: human` always and MUST allow any other owner only while zero teams (in any archive layer)
  name that `goal_slug`. A refusal MUST be an exit-2 error whose text names the binding team slug(s).

(FR-038)
- **C-15**: `territory` on a team MUST NOT be able to authorize a write into `.specify/goal/**` or
  `.specify/teams/**`; such an entry MUST be refused when the team definition is validated (`territory-reserved`,
  exit 2), because those trees obey the function above rather than a territory grant.

(FR-036, FR-038)
- **C-16**: A write that targets an archive layer other than the one the definition resolves to MUST be refused
  (`cross-layer-write`, exit 2) and the refusal MUST name both layers. This replaces the 085
  "forbidden paths" prohibition in the routing carve-out ; the hierarchy prohibition itself is unchanged.

(FR-027, FR-038)
## 4. Lifecycle

- **C-17**: A goal's lifecycle MUST stay the existing closed three values `active` / `achieved` / `abandoned`
  with the existing transition table; a terminal goal MUST be retained, never deleted, never relocated.

(FR-026)
- **C-18**: A team's lifecycle MUST stay `active` / `archived`; an `archived` team MUST be refused by `run-team`
  (`team-archived`, exit 2). The goal's three values MUST NOT be imposed on a team.

(FR-023, FR-026)
- **C-19**: Re-opening a terminal goal MUST require an explicit lifecycle action (`reopen`), MUST be permitted
  only for `owner: human`, and MUST append a history line. It MUST NOT be a side effect of any other action.

(FR-026)
- **C-20**: Lifecycle changes MUST NOT touch `owner` / `owner_id` / `origin` (C-6's byte rule applies to the
  binding block, not the status block).

(FR-026)
## 5. Legacy state-spine keys (FR-028)

- **C-21**: The engine MUST accept the three legacy keys `temp_goal_slug` / `temp_team_slug` /
  `temp_scope_spec_dir` as a **read-only migration alias** on every action that takes a slug or spec dir from the
  spine; a value arriving through a legacy key MUST be treated exactly as its new counterpart.

(FR-028)
- **C-22**: Every write MUST land on the new keys only (`goal_slug` / `team_slug` / `origin_spec_dir`). A tool
  that emits a legacy key on write MUST be reported as `legacy-key-written` (advisory at CLI, error in the
  contract test).

(FR-028)
- **C-23**: The alias MUST be removable at a declared version point; the version point MUST be recorded in
  `shared/definitions/goal-definitions.md` § Terminology Boundaries in the same change. Removing the alias is
  therefore one edit plus one documentation line, not a search.

(FR-028)
- **C-24**: A legacy key that does not resolve to a definition MUST fail with `legacy-key-dangling` naming the
  key — never silently ignored, never treated as absent.

(FR-028)
## 6. Parallelism invariants

- **C-25**: No action, check or driver instruction MUST require a goal or team to exist for an SDD run to
  proceed, nor a spec to exist for a goal/team to proceed (FR-014). The contract test asserts the negative: with
  the other line absent, every command of one line still exits 0.

(FR-014)
- **C-26**: Ownership queries MUST go through C-8's action; a code path that derives an owner from a path
  prefix MUST be reported by the structural invariant in `owner-rewrites-and-tests.md` C-106 .

(FR-015, FR-038)
- **C-27**: A second creation of an existing slug MUST be refused by the engine (the existing `create_goal`
  existence check, EP-003) with the path of the existing definition and, where known, its `owner` / `owner_id`;
  the two-archive split MUST NOT be used to justify coexisting duplicates (FR-021).
- **C-28**: N teams : 1 goal MUST remain legal and MUST be expressed only by `goal_slug` on the team side; a team
  MUST NOT store a copy of the goal's objective or criteria. Territory overlap across the teams bound to one goal
  MUST be reported by `improve-team`'s existing overlap check, not silently allowed.

(FR-026)
- **C-29**: `sdd-route.py authorize` MUST record `archive_layer` (the C-9 value) instead of the retired scope
  names, and MUST resolve the team path through C-8/C-10 rather than through a second path implementation.

(FR-008, FR-025)
- **C-30**: `run-checks` MUST carry the binding record of the team it loads and MUST NOT change its existing
  `resolution` keys; any new key MUST be additive and documented in `skills/internal/run-team/SKILL.md`.

(FR-002)
## Requirement coverage

FR-001, FR-002, FR-003, FR-004, FR-005, FR-008, FR-014, FR-015, FR-021, FR-023, FR-025, FR-026, FR-027,
FR-028, FR-038.
