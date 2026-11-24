# Tasks Stage Evidence — 103-team-view (2026-11-24)

Stage: tasks (attempt 1). Artifact: `.specify/specs/103-team-view/tasks.md`. Docs-only stage: no executable or test path changed, so no test run was performed (the unique entry remains `scripts/bash/run-tests.sh`).

## Gates (all rc 0 unless stated)

| Gate | Command | Verdict |
|------|---------|---------|
| G-structure | `python3 .specify/scripts/python/validate-tasks.py .specify/specs/103-team-view/tasks.md` | `PASS: 0 error(s), 0 warning(s)` |
| G-stage | `python3 .qoder/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/103-team-view --stage tasks --repo .` | `decision=pass`, `errors=0`, `advisories=115`, `fr=21`, `sc=7`, `tasks=44`, `clauses=38`, `files=11` (advisories: missing-path for not-yet-created delivery paths; external-clause for `INV-NN` namespaces) |
| G-decomposition | `python3 .qoder/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/103-team-view/requirements.md --tasks .specify/specs/103-team-view/tasks.md` | `{"decision": "proceed", "measured": {"fr_count": 21, "task_count": 44, "fr_ceiling": 120, "task_ceiling": 160}, "reasons": []}` |
| G-clause-census | `python3 scripts/python/clause_extract.py .specify/specs/103-team-view/contracts/*.contract.md` (plan-stage reading, unchanged here) | 38 clauses `C-01…C-38` (12 + 11 + 15), all resolve; pre-analyze reports 0 dangling clause ids |

Task rows: 44 definitions (`T001`…`T044`), 4 user-story phases, 1 Foundational row, 6 `[P]` rows across three phases (Setup ×2, US1 tests ×2, US2 tests ×2), zero `[green:]` claims (rationale in tasks.md § Notes N-1).

## Premises re-measured at generation time (2026-11-24)

- teams: 20 directories / 20 `team.md`; run dirs 12; `runs/*.md` 46 vs `runs/*-report.md` 41 (5 contract-external names); `items.jsonl` 5 (one zero-line); `constraints.md` 3.
- `exactly three modes`: 1 occurrence in each of 6 files (`templates/commands/team.md`, `docs/reference/commands/team.md`, four per-tool copies).
- `argument-hint`: 0 in `templates/commands/team.md`; sibling precedent present in `templates/commands/anchor.md` and `goal.md`.
- Deliverables absent: `scripts/python/team-view.py`, `skills/internal/view-team/`, `tests/fixtures/team_view_fixtures.py`, `tests/unit/test_team_view_parsers.py`, `tests/contract/test_team_view_command.py`, `tests/contract/test_team_view_program_contract.py`, `tests/integration/test_team_view_program.py`.
- docs drift literals: `never executes before you confirm`, `Only then does orchestration run`, `Declining stops without executing` — 1 each; run delegation cell is `` `create-team` (execution path) ``.
- Runtime probes: CPython 3.11.11 (`pyproject.toml` floor `>=3.8`), pytest 8.4.2 + xdist 3.8.0, bash 4.4.20, git 2.43.5, `goal-utils.py 0.0.22`.
- Distribution baseline: `sync-mirrors.py --check` rc 0; `regen-command-copies.py --check` rc 0; `probe-utils.py --action compile-embeds --check` → 85 units, zero drift; `probes --validate` rc 0; `probes --reconcile` zero-gap (129 internal objects / 86 embeds).

## Corrections applied in passing

1. **Plan delivery-surface omission (declared PLAN-EDIT, minor)**: `feature-ref.md` § Delivery surface gained item 19 (`shared/definitions/probe-definitions.md` + its mirror). Reason: contract C-22 requires the new skill's compiled `## Wrap-up`, and `probe-utils.py --action probes --reconcile` rejects an embed whose unit has no probe object; `tasks.md` T015 implements the registration. Classified minor (reference completeness, no capability or architecture change).
2. **Report-count trap recorded rather than collapsed**: the plan's "46 reports" was re-measured as 46 `runs/*.md` / 41 `runs/*-report.md`; both readings are written in `tasks.md` § Premises with the naive-form trap.

## Anomalies

None. No anomaly was found and no in-passing repair other than the two corrections above was needed.
