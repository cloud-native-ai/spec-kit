# Team Fixtures

Synthetic teams used by the `036-team-summary` test suite. They exist because the
repository's four real teams do not cover the matrix the success criteria require:

| Need | Real-team coverage | Fixture required |
|------|--------------------|------------------|
| `continuous` pattern | ✅ `cws-workspace-cluster`, `requirement-implement-monitor` | — |
| `iteration` pattern | ✅ `draw-plantuml-optimizer`, `summarize-project-optimizer` | — |
| `serial` pattern | ❌ none | `serial-fixture/` |
| `parallel` pattern | ❌ none | `parallel-fixture/` |
| Two teams sharing one `goal_slug` | ❌ all four goals are distinct, none declares `goal_slug` | `goal-share-a/`, `goal-share-b/` |

SC-001 requires one team per collaboration pattern; SC-013/SC-014/SC-015 require a
goal with more than one contributing team. Fixtures supply exactly those gaps and
nothing else.

## Rules

- Fixtures are **inputs**, never outputs. Tests MUST NOT write into this directory;
  point the generator's `--out` at a temporary path instead.
- Each fixture carries the minimum tracked surface the generator reads: `team.md`
  (frontmatter + `## Goal`), `items.jsonl`, and at least one `runs/<UTC>-report.md`.
- Fixture content is illustrative and MUST NOT be copied into real team definitions.
- Keep fixtures small. They are read by deterministic parsing, not by a model, so
  volume buys nothing.
