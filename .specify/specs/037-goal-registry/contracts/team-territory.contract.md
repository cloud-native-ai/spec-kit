# Contract: Team Territory and Overlap Detection

**Requirement**: 037-goal-registry | **FRs**: FR-033…FR-042
**Artifacts**: `team.md` frontmatter `territory` (authored); `summary/roster.md` + generation report (derived)
**Prior art lifted**: `skills/create-team/SKILL.md` § "Territory Division" (member-level, parallel pattern, prose-only, zero executable validation today)

## Territory declaration

Declared in `team.md` frontmatter immediately after `goal_slug`:

```yaml
goal_slug: shared-harvest-goal
territory:
  write:
    - docs/reference/**
    - skills/create-team/references/*.md
  read:
    - skills/**
  forbidden:
    - skills/create-team/SKILL.md
  non_path:
    - type: framework
      target: the spec-kit framework this project consumes
```

| Key | Type | Required | Meaning |
|-----|------|----------|---------|
| `territory.write` | list of path patterns | no | paths this team may create or modify |
| `territory.read` | list of path patterns | no | paths this team may read |
| `territory.forbidden` | list of path patterns | no | shared paths this team MUST NOT modify |
| `territory.non_path` | list of `{type, target}` | no | coverage dimensions that are not file-shaped |

## Normative rules

- **TT-1** The declaration applies to all four collaboration patterns — `parallel`, `serial`, `iteration`, `continuous`. An implementation that honors it only for `parallel` violates this contract.
- **TT-2** A team-level territory is not derivable from member-level territories, because member `territory` exists only in the parallel pattern. Absence of member territories MUST NOT be read as an empty team territory.
- **TT-3** Path patterns MUST be normalized before any comparison, in this order: brace expansion (`{a,b}` → `a`, `b`); `./` and `../` resolution to repo-relative canonical form; trailing-slash removal; glob retention (`**`, `*` are kept as patterns, not expanded against the filesystem).
- **TT-4** Two path entries overlap when their normalized forms can match a common path. Pattern-vs-pattern comparison MUST treat `a/**` and `a/b/c.md` as overlapping.
- **TT-5** An absent `territory` key means **undecidable**, never empty.
- **TT-6** A member-level territory whose write scope is not contained in its team-level write scope is an out-of-bounds violation and MUST be reported.

## Overlap verdicts

For each unordered pair of teams sharing one `goal_slug`:

| Verdict | Condition |
|---------|-----------|
| `overlap` | normalized `write` sets intersect (`write-write`) |
| `no-overlap` | both teams declared territory and no `write` intersection exists |
| `undecidable` | either team declared no territory, or the only intersection is between `non_path` entries |

- **OV-1** Zero write overlap is the invariant: no two teams sharing a goal may have intersecting `write` sets.
- **OV-2** Read overlap is permitted. A pair intersecting only on `read` — or on one team's `read` against another's `write` — MUST NOT be reported as `overlap`.
- **OV-3** `overlap` findings MUST name the concrete intersecting entries.
- **OV-4** `non_path` entries are listed side by side for human arbitration. The mechanism MUST NOT judge two `non_path` declarations equivalent, even when their `type` matches.
- **OV-5** `no-overlap` and `undecidable` are distinct outcomes and MUST NOT be collapsed. Reporting `no-overlap` for a team that declared nothing is a contract violation.

## Contested areas

A `write-write` finding is a **contested area**. Resolution is one of exactly two terminal outcomes:

| Outcome | Meaning |
|---------|---------|
| single owner | the area is assigned to exactly one team; the other teams' declarations are narrowed |
| forbidden | the area enters the goal's forbidden-write list and is thereafter modified only by a human |

A contested area MUST NOT remain in a multi-writable state after a ratified coordination round.

## Detection trigger

- **DT-1** Detection rides the existing goal summary refresh. It runs after the Material gate and before the refresh write, so it executes only when a refresh actually happens.
- **DT-2** Exactly one trigger point exists. No second scheduler, hook, or pre-cycle check is introduced.
- **DT-3** The refresh already enumerates every team sharing the `goal_slug`; detection consumes that same set and MUST NOT re-scan independently.
- **DT-4** Findings surface in two places: the goal's derived roster, and the triggering team's run report status line.

## Roster

Derived to `.specify/goal/<goal-slug>/summary/roster.md`, with the machine-readable form in the generation report.

| Field | Value |
|-------|-------|
| team slug | the team's `slug`; attribution is presented as the slug, never an internal agent id |
| declared territory | verbatim, or `undeclared` |
| identity type | `explicit` when `goal_slug` is declared; `inferred` when derived from the team's own slug |
| advancing | whether recent ledger or run activity exists |
| participation | `active`, or `departed` for a team that rebound to another goal |

- **RO-1** The roster is derived. It MUST NOT become a field of `goal.md`, and it MUST NOT create a goal→team stored reference.
- **RO-2** The roster is regenerated wholesale on each refresh, never incrementally patched.
- **RO-3** Completeness is verified by diffing the roster against a filesystem scan of teams declaring the `goal_slug`. The scan is the truth set.
- **RO-4** A departed team is marked, not removed — its historical participation remains visible.

The current generation report already emits `contributing_teams` for exactly this team set (verified by execution against the `goal-share-a` / `goal-share-b` fixtures, which both declare `shared-harvest-goal`). The roster extends that existing field with territory, identity type, advancing, and participation rather than introducing a separate collection pass.

## Coordination round

```text
detect (rides refresh) → propose (with rationale) → human ratifies → write back to team.md
```

- **CR-1** The mechanism detects and proposes only. It MUST NOT rewrite any team's territory.
- **CR-2** During the proposal stage, writes to every `team.md` are zero.
- **CR-3** Each proposal carries its rationale — which entries collide and why the proposed division resolves them.
- **CR-4** A ratified division is written back into each affected `team.md`. No authored coordination record is created inside the goal directory.
- **CR-5** For a goal with one team, the overlap set is empty and the round is not initiated.
