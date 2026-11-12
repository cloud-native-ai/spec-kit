# Fixtures — anchor-goal-realignment (Feature 101, WP-05 T061)

Inputs only. No reading here is an expected value: every count and verdict a test asserts is
produced by the code under test when it reads these files. Copy the trees to a scratch
directory before mutating them; never point a write action at the fixture itself.

| Fixture | Supplies | Consumer |
|---------|----------|----------|
| `classification/classification.json` | the 14-entry / 7-team classification in the shape the cleanup action adjudicates (schema, `mapping_version`, resolvable `baseline_commit`) | G-7a / G-7b (idempotency, resume) |
| `pre-convergence/.specify/anchoring/<slug>/goal.md` | the pre-cleanup anchor store: 14 entries, all still holding the retired `goal.md` file name and `# Goal:` heading; 3 of them classified `action-goal` and 2 `obsolete` | G-3, G-5, G-9 |
| `pre-convergence/.specify/teams/<slug>/team.md` | 20 team definitions: 16 carry `goal_slug`, 4 carry none, 2 of the 16 bind a slug that has no definition (the dangling pair) | G-5, G-9 |
| `protected-paths/tree/` + `protected-paths/baseline.txt` | a two-file dated-record set plus its recorded digest list — the input a protected-path scan compares against | G-8 (injection case) |

The pre-convergence tree is deliberately *un-converged*: one action-level entry still lives in
the anchor store, retired `goal_slug` keys are still on the teams, one delivery path still names
`.specify/goal/<slug>/summary/`, and two bindings resolve to nothing. A guard that cannot see
those defects here cannot see them on a live tree either.
