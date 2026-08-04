# Tool: build-summary-input.py

| Field | Value |
|-------|-------|
| **Tool Name** | build-summary-input.py |
| **Tool ID** | `<TOOL:.specify/memory/tools/build-summary-input.py.md>` |
| **Tool Type** | project-script |
| **Source Identifier** | skills/create-team/scripts/build-summary-input.py |
| **Aliases** | build-summary-input |
| **Status** | Draft |
| **Last Updated** | 2026-08-04 |

## Description

Derives a `summarize-project` input form from team artifacts, aggregating every team that
declares the same `goal_slug` into one goal-level form. Proposed for promotion per
Constitution Principle XII now that it is a verified repeatable capability.

## Contract

```
build-summary-input.py (--goal <goal-slug> | --team <team-slug>)
                       [--out <path>] [--baseline <iso8601>] [--repo-root <path>] [--json]
```

Exit codes: `0` form written | `2` input error (unknown slug, unresolvable goal) |
`3` declined — no execution material anywhere in the goal | `4` serialized — another
refresh of the same goal holds the lock.

## Behavioral Rules

- MUST be invoked with `--repo-root` when the working directory is not the repository root.
- Reads ONLY: `.specify/teams/*/team.md`, `<team>/items.jsonl`, `<team>/runs/*-report.md`,
  `<team>/run-log.jsonl`, `.specify/agents/{templates,instances}/*.agent.md`.
- Writes ONLY `--out` (default `.specify/project/goal/<goal-slug>/data/project-input.yaml`)
  and its parent directory. Never writes into `.specify/teams/**`.
- Output is deterministic: identical inputs produce byte-identical forms. Safe to re-run.
- Work-item and phase identifiers are namespaced `<team-slug>.` because `entity_ids` is a
  global namespace — two teams' unprefixed `TI-0001` values collide (upstream exit 3).
- Emits a `coverage` block on every run; omitting it fails the upstream CG-COVERAGE gate.
- Concurrency-safe: takes a directory lock and writes atomically via temp-file replace.

## Environment Applicability

- **Verified on**: Linux 5.10 (x86_64), Python 3.11.11, PyYAML present.
- **Requires**: PyYAML. No other third-party dependency.
- **Verified against**: all 4 real teams in this repository plus 4 fixture teams; the
  produced forms pass `validate-project-input.py` (`status=ready`, `missing_required=[]`),
  `project-db.py --load`, and `--check`.
- **Not verified on**: Windows; Python < 3.11.

## Promotion Note

Status is `Draft` because Principle XII forbids a record claiming environments it was not
verified against. Promote to `Verified` after a second reviewer confirms the contract and
after use on a repository other than this one.
