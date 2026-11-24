# Quickstart — Team View (103-team-view)

**Entry**: `/speckit.team view [team-slug]` (routes to the `view-team` skill, which runs `scripts/python/team-view.py`).
**Read-only**: none of the scenarios below writes to the repository. The read-only oracle is a path+sha256 snapshot.

The program surface (`team-view.py …`) does not exist until implementation lands. Each program example carries (a) its own premises and (b) the name of the pinning test that will assert it. The engine examples are executed surfaces and were run on 2026-11-24.

## S-0 — Executed engine reads (the facts a single view composes)

```bash
python3 scripts/python/goal-utils.py binding team 086-efficient-test-execution --json
python3 scripts/python/goal-utils.py list --json | python3 -c "import json,sys; print([g for g in json.load(sys.stdin)['goals'] if g['slug']=='086-efficient-test-execution'])"
python3 scripts/python/goal-utils.py targets 086-efficient-test-execution --list --json
```

Captured stdout (2026-11-24, exit 0 for all three; complete output of each command as written, not a projection):

```json
{
  "kind": "teams",
  "slug": "086-efficient-test-execution",
  "owner": "human",
  "owner_id": "human",
  "origin": "086-efficient-test-execution",
  "path": ".specify/teams/086-efficient-test-execution/team.md",
  "archive_layer": "teams",
  "lifecycle": "active"
}
```

```text
[{'slug': '086-efficient-test-execution', 'status': 'active', 'criteria_count': 5, 'updated': '2026-11-06'}]
```

```json
{
  "targets": []
}
```

Premises: `.specify/teams/086-efficient-test-execution/team.md` exists with `anchor_slug: 086-efficient-test-execution`; `scripts/python/goal-utils.py` is `0.0.22`. Re-measure with the three commands before relying on the values.

## S-1 — One team, six groups

```bash
python3 scripts/python/team-view.py cws-workspace-cluster
```

Expected shape (pinned by `tests/integration/test_team_view_program.py::test_single_team_renders_six_groups`):
`## 1. 身份与绑定` … `## 6. 其他归档层引用` appear in order; every `members[]` row and every `runs/*-report.md` filename of the fixture appears exactly once; the `as-of:` line is present; exit 0.

Premises: `.specify/teams/cws-workspace-cluster/team.md` exists (measured 2026-11-24) and declares `pattern: continuous`; the fixture variant is what the test asserts; `team-view.py` resolves its sibling `goal-utils.py`.

## S-2 — No slug: overview

```bash
python3 scripts/python/team-view.py
```

Expected shape (pinned by `::test_overview_lists_every_team_sorted`): a table with one row per fixture team, slug ascending, columns slug / name / pattern / lifecycle / 绑定锚点 / updated / 最近运行; exit 0.

Premises: the fixture archive contains ≥2 teams including one with a corrupt definition; the corrupt row is present and labelled `定义损坏`; a live run reports `overview.total` and `overview.corrupt_total` in the `--json` envelope.

## S-3 — Unknown slug

```bash
python3 scripts/python/team-view.py no-such-team
```

Expected shape (pinned by `::test_unknown_slug_reports_not_found`): the output contains `team not found` ([[STR-001]]), the available-slug list with an omitted count when it exceeds 20, and a `/speckit.team create` suggestion; exit 3. For an empty archive the same command additionally contains `No teams found` ([[STR-002]]).

Premises: the fixture team archive is non-empty (or empty for the second leg); the slug `no-such-team` has no directory and no near-miss sibling.

## S-4 — Corrupt definition

```bash
python3 scripts/python/team-view.py broken-team
```

Expected shape (pinned by `::test_corrupt_definition_is_not_not_found`): the output contains `定义损坏` and the exact path `.specify/teams/broken-team/team.md`, does **not** contain `team not found`, and does not render a six-group body; exit 4.

Premises: the fixture creates `.specify/teams/broken-team/` without `team.md`; a second variant creates `team.md` with unparseable frontmatter; both exit 4.

## S-5 — `--target` is a mode conflict

```bash
python3 scripts/python/team-view.py some-team --target T-001
```

Expected shape (pinned by `tests/contract/test_team_view_program_contract.py::test_undeclared_target_option_rejected`): exit 2 and a recognizable undeclared-option error; no rendering, no write. At the command level the same invocation is reported as a mode/parameter conflict by `tests/contract/test_team_view_command.py::test_view_target_conflict_declared`.

Premises: `--target` is not declared by `team-view.py`; the command template's View Mode section states the conflict.

## S-6 — Read-only proof

The oracle is `tests/integration/test_team_view_program.py::test_view_leaves_tree_byte_identical` (executed through the project's unique entry `scripts/bash/run-tests.sh` once the test file exists). It snapshots the fixture tree as a path+sha256 map before and after one view invocation and asserts equality: no new file, no removed file, no changed byte. This scenario exposes no separate command example — the test itself is the executable surface, so there is no unrun command to pin here.

Premises: the fixture lives under pytest `tmp_path`; `team-view.py` is invoked with `--repo-root <tmp>`, so the real repository is untouched; the engine reads resolve against the same fixture root or against a stubbed sibling recorded by the test.
