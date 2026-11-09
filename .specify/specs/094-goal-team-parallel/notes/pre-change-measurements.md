# Pre-change measurements — implement entry (wp01-foundation, T004)

Date: 2026-11-09 (UTC morning session)
Host tree: `/storage/project/cloud-native-ai/spec-kit`, branch `master`
Base commit: `124759e3` (checkpoint 06-analyze, open implement wave 1)
Probe root for throwaway trees: `.specify/.tmp/s094/` (T003 record: `test-evidence/T003-fixture-probe.txt`)

Each row below re-derives the quantity with the command the tasks table names, at **implement
entry**, before any engine edit of this package. The recorded value from the tasks/plan stage is
kept beside the fresh reading; a difference is a dated reading, not a silently-updated constant.

| # | Quantity | Stage-recorded premise | Implement-entry reading | Command | Delta |
|---|----------|------------------------|-------------------------|---------|-------|
| 1 | Spec-local goal definitions | 8 (tasks.md § premises, "8 (085–092)") | **9** | `ls -d .specify/specs/*/goal/*/goal.md \| wc -l` | +1 — the ninth is 094's own spec-local goal, exactly the case requirements A6 round-4 anticipated (probe form goal 9 / team 8 = 17); it is part of the migration subject per tasks.md N-4 / A8 |
| 2 | Spec-local team definitions | 8 | **8** | `ls -d .specify/specs/*/team/*/team.md \| wc -l` | 0 |
| 3 | Unified-archive goal entries | 6 | **6** | `basename -a .specify/anchoring/*/ \| wc -l` | 0 |
| 4 | Unified-archive team entries | 12 | **12** | `basename -a .specify/teams/*/ \| wc -l` | 0 |
| 5 | Serial baseline failed ids | 46 | **46** (plan-stage `plan-baseline-names.txt`); implement-entry re-capture recorded below | `wc -l < .specify/specs/094-goal-team-parallel/test-evidence/plan-baseline-names.txt` | 0 against the plan record; the entry re-capture is `test-evidence/implementation-baseline-names.txt` (T002) |
| 6 | `--scope` closed set | `(global, spec, auto)` | **`("global", "spec", "auto")`** at `goal-utils.py:1339`; `resolve_scope` default `scope: str = "global"` at `:135`; seven `"global"` literals at `:135, :146, :173, :174, :188, :1339, :1447` | `grep -n 'common.add_argument("--scope"' scripts/python/goal-utils.py` | 0 (the seven-literal measurement of tasks.md T013 reproduced: `:135 :146 :173 :174 :188 :1339 :1447`) |
| 7 | Engine actions | 10 + `run-checks` | **11** `sub.add_parser(` calls = the 10 listed actions + `run-checks` | `grep -c 'sub.add_parser(' scripts/python/goal-utils.py` | 0 |
| 8 | Declaration fact files on disk | 23 | **24** | `ls shared/declarations/facts/*.yaml \| wc -l` | +1 — the premise count is stale by one; the fact listing is reproduced in the appendix and the delta is dated here rather than absorbed |

## Appendix — measured listings

### Spec-local goal definitions (9)

```text
.specify/specs/085-sdd-temporary-goal-team/goal/085-sdd-temporary-goal-team/goal.md
.specify/specs/086-efficient-test-execution/goal/086-efficient-test-execution/goal.md
.specify/specs/087-arch-diagram-docs/goal/087-arch-diagram-docs/goal.md
.specify/specs/088-speckit-visualization/goal/088-speckit-visualization/goal.md
.specify/specs/089-script-interface-contract/goal/script-interface-contract/goal.md
.specify/specs/090-re-anchoring/goal/090-re-anchoring/goal.md
.specify/specs/091-auto-git-closeout/goal/091-auto-git-closeout/goal.md
.specify/specs/092-non-disposable/goal/092-non-disposable/goal.md
.specify/specs/094-goal-team-parallel/goal/094-goal-team-parallel/goal.md
```

### Spec-local team definitions (8)

```text
.specify/specs/085-sdd-temporary-goal-team/team/085-sdd-temporary-goal-team/team.md
.specify/specs/086-efficient-test-execution/team/086-efficient-test-execution/team.md
.specify/specs/087-arch-diagram-docs/team/087-arch-diagram-docs/team.md
.specify/specs/088-speckit-visualization/team/088-reporting-dogfood/team.md
.specify/specs/089-script-interface-contract/team/089-script-interface-contract/team.md
.specify/specs/090-re-anchoring/team/090-re-anchoring/team.md
.specify/specs/091-auto-git-closeout/team/091-auto-git-closeout/team.md
.specify/specs/094-goal-team-parallel/team/094-goal-team-parallel/team.md
```

### Unified-archive entries (6 goal / 12 team)

```text
goal:  command-logic-as-classified-skills  draw-diagram-interactive  draw-two-layer-structure
       post-refactor-mechanism-integrity  session-driven-self-improvement  skill-layer-install-separation
teams: 12 directories under .specify/teams/
```

### Engine actions (11 `sub.add_parser` calls)

```text
resolve-scope  create  validate  check-statement  list  status  objective  criteria  migrate  targets  run-checks
```

### `--scope` occurrences that a value-set change must sweep

```text
135:def resolve_scope(repo_root: Path, scope: str = "global",
146:    if scope not in ("global", "spec", "auto"):
173:    if scope == "global":
174:        return Scope("global", repo_root, None, global_goal, global_team)
188:    return Scope("global", repo_root, None, global_goal, global_team)
1339:    common.add_argument("--scope", choices=("global", "spec", "auto"), default=None,
1447:        requested_scope = "auto" if args.action == "resolve-scope" else "global"
plus the user-facing guidance strings at :185 and :1449 and the --spec-dir help at :1343
```

### Declaration fact files (24)

```text
arc-verdict-mapping.yaml                    driver-completion-sentinels.yaml
driver-gate-roster.yaml                     driver-stage-artifacts.yaml
driver-stage-sequence.yaml                  evidence-lanes.yaml
evidence-seven-states.yaml                  expression-gate-faces.yaml
expression-stage-operator-table.yaml        feedback-prompt-threshold.yaml
flow-class-basis.yaml                       flow-class-classes.yaml
flow-class-document-types.yaml              flow-class-ledger-columns.yaml
flow-class-neutral-categories.yaml          history-manifest-schema.yaml
memory-retention-thresholds.yaml            memory-types.yaml
non-disposable-review-surface.yaml          probe-class-values.yaml
probe-object-binding-map.yaml               quant-record-schema.yaml
success-criterion-path-values.yaml          trigger-state-schema.yaml
```

## Serial baseline re-capture (T002)

Implement entry, clean run against the HEAD engine with this package's test module absent:
**113 failing ids** (`113 failed, 8187 passed, 2 skipped in 679.29s`, exit 1) — against the
plan-recorded 46 (`69` names new, `2` plan names no longer failing). The full reading and its
classification live in `test-evidence/wp01-T002-baseline.txt`,
`test-evidence/implementation-baseline-ids.txt` and
`test-evidence/implementation-baseline-full.out`; they are not duplicated here (single
definition point). The plan baseline is stale relative to this tree; the driver owns the
re-baseline ruling (see `notes/implement-wp01.md` § Residual risks 1).
