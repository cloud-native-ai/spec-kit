# Quickstart: Goal Registry (037)

**Requirement → Feature**: `037-goal-registry` → Feature 041 Goal Registry

Each shell command below is marked **[verified]** (executed against this repository during planning, output as shown) or **[target]** (behavior this requirement introduces; not yet runnable). `/speckit.*` entries are chat instructions, never shell commands.

## 0. Baseline — what is true before any change

**[verified]** The old delivery directory is not materialized, and the new archive does not exist:

```bash
ls .specify/                      # → agents docs memory project review scripts shared skills specs teams templates
ls .specify/project/              # → project.md + wbs/gantt/milestones .puml/.png/.svg  (no goal/)
ls .specify/goal/ 2>&1            # → No such file or directory
```

**[verified]** Mirrors are clean and the test baseline is frozen:

```bash
python3 scripts/python/sync-mirrors.py --check    # exit 0
pytest -q                                         # 40 failed, 1308 passed, 1 skipped
```

The 40 failures are pre-existing and named in `baseline-failed.txt`. Any new failure name is a regression introduced by this work.

**[verified]** The generator today writes under the old path, and already knows which teams share a goal:

```bash
python3 skills/create-team/scripts/build-summary-input.py \
  --goal shared-harvest-goal --repo-root . --json
```

Run against the `goal-share-a` / `goal-share-b` fixtures it reports `delivery_dir = .specify/project/goal/shared-harvest-goal` and `contributing_teams = ["goal-share-a", "goal-share-b"]`. That team set is the proto-roster this requirement materializes.

## 1. Archive a goal (US1)

**[target]** In chat:

```text
/speckit.goal create
```

The command interviews for the objective and criteria, then writes:

```text
.specify/goal/framework-stays-current/
└── goal.md
```

with `status: active`, an `## Objective` stating an outcome, `## Success Criteria`, and a `## History` line.

Verify the archive is enumerable without reading any team file:

```bash
ls .specify/goal/                                    # one directory per goal
grep -h '^status:' .specify/goal/*/goal.md           # one lifecycle state per goal
```

Two rejections to expect: creating the same identity twice is refused and points at `modify`; an objective written as a task list is refused naming the outcome rule.

## 2. Point a team at it (US2)

**[target]** Add one line to the team's frontmatter — the identity only, never a copy of the objective:

```yaml
goal_slug: framework-stays-current
```

Two teams declaring the same value resolve to the same definition, word for word. A team declaring an identity with no archived definition is reported as a broken link naming the missing identity — never silently degraded to an empty goal. A team with only an inline goal keeps working with zero edits.

## 3. Refresh the summary (US3)

**[target]** The refresh now writes under the goal archive, structurally separated from the definition:

```text
.specify/goal/framework-stays-current/
├── goal.md                    # authored — never written by the refresh
└── summary/                   # the only writable face
    ├── project.md
    ├── roster.md
    └── data/project-input.yaml
```

Verify the definition was untouched:

```bash
sha256sum .specify/goal/framework-stays-current/goal.md   # identical before and after a refresh
```

Project narrative and milestones now come from the definition rather than from whichever team's `## Goal` body was picked, so the "goal body disagrees" arbitration item disappears.

## 4. Declare territory and detect overlap (US5)

**[target]** Give each team a team-level scope:

```yaml
# .specify/teams/goal-share-a/team.md
goal_slug: shared-harvest-goal
territory:
  write:
    - docs/reference/**
  read:
    - skills/**
```

```yaml
# .specify/teams/goal-share-b/team.md
goal_slug: shared-harvest-goal
territory:
  write:
    - docs/**              # collides with team a
```

On the next refresh the roster lists both teams and names the collision down to concrete paths. Three verdicts are distinguishable:

| Situation | Verdict |
|-----------|---------|
| write sets intersect | `overlap`, with the intersecting entries named |
| both declared, no write intersection | `no-overlap` |
| either team declared nothing | `undecidable` — never reported as `no-overlap` |

A pair that intersects only on `read` is not an overlap.

## 5. Run a coordination round (US5)

**[target]** In chat:

```text
/speckit.goal coordinate shared-harvest-goal
```

The mechanism proposes a re-division with its rationale and writes nothing. Verify that:

```bash
sha256sum .specify/teams/*/team.md    # unchanged during the proposal stage
```

After you ratify, the division is written back into each `team.md` — the team stays the sole declaring party, and no authored coordination file appears inside the goal directory. Any contested area ends as either a single team's property or an entry on the goal's forbidden-write list; it never stays multi-writable.

## 6. Migrate a legacy team (US4)

**[target]** In chat:

```text
/speckit.goal migrate <team-slug>
```

The team's inline objective becomes an archived definition and the team switches to a reference. Whether the inline copy stays is your call. Migration is per-team; the other teams are unaffected and require no edits.

## 7. Verification gates

**[verified]** commands, **[target]** expectations:

```bash
# live residual references to the old path — must reach 0 on the live face
grep -rl 'project/goal' --exclude-dir=.git --exclude-dir=.venv . \
  | grep -vE '^\./\.specify/(specs/03[67]|memory/(feedback|features))' \
  | grep -v __pycache__

# mirrors and generated command copies must be in lockstep
python3 scripts/python/sync-mirrors.py --check          # exit 0

# no regression against the frozen baseline
pytest -q                                               # no new failure names
```

Historical files (036's spec artifacts, 037's own spec, feedback records, feature memory) also contain the old string and MUST NOT be rewritten — the 2026-08-04 clarification quotes it verbatim as the user's directive.
