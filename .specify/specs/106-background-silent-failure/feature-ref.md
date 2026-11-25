# Feature Reference — 106-background-silent-failure

**Bound Feature**: 095 — Super Agent Role（`Ready for Review`; slice row 106 advances `Draft → Planned`; the parent status stays unchanged — no status regression).
**Binding basis**: 095 owns the settlement contract's single owner (`shared/definitions/superagent-definitions.md` § Termination) and the judgment engine being extended (`scripts/python/role-edge-check.py`). Feature 058 owns the C1 carrier and the watcher judgments (explicitly unchanged), 064 owns lifecycle/attribution, and 065 owns interruption recovery — none owns the settlement contract. Binding decision and rationale: `.specify/specs/106-background-silent-failure/requirements.md` § Clarifications (Session 2026-11-25).
**Parent detail**: `.specify/features/095-superagent-role.md`.

## How this plan maps to Feature 095

| Plan element | Feature 095 element it serves | Direction |
|--------------|-------------------------------|-----------|
| § Termination amendment (closed set, evidence per value, reaction, version/legacy, extended violation set) | the owner page's edge protocol and its role-edge model | amend: the existing "silent orphaning is a defect" sentence becomes an observable, evidenced settlement contract; four edge violation kinds unchanged |
| `role-edge-check.py` `--action settle` | the 095 judgment engine over existing carriers | additive: new action + new input readers; `report` / `query` schemas byte-identical |
| C2 additive attempt/end records + trap/pid | the dispatch carrier the role edges already ride | additive: carrier evidence becomes settlement-capable; `.status` format unchanged |
| C3 report `end_state` + verification coverage | the seat-side edge evidence the engine already parses | additive: 7-column new header, 5-column legacy still accepted |
| C4 native attempt record / C5 exclusion / C6 recipes | the parent-side edge and the dispatch modes | additive text + one parent-side record; no new role or mechanism |
| Contract tests + mutation drill | the feature's quality gate and evidence honesty | new tests; behavior-class clauses stay honestly classified |

The feature does **not** change `watch-target.sh`, `stage-runner.sh`, `exec-quant.py`, `sync-mirrors.py`, `regen-command-copies.py` or `scan-confirmation-gates.py`, does not change the five-element uplink or the seven-field downlink, does not add a scheduler/registry/queue/store/notification channel, and does not add a second value table or evidence matrix anywhere.

## Delivery surface

Owner and shared surfaces (framework sources):

1. `shared/definitions/superagent-definitions.md` — § Termination amendment + § Role Edges violation-set extension reference.
2. `shared/definitions/subagent-definitions.md` — virtual exclusion + settlement pointer in § Three Execution Modes.
3. `shared/workflow/external-dispatch-recipes.md` — Recipe 4 per-value dispositions; Recipe 7 wave settlement.

Engine and carrier:

4. `scripts/python/role-edge-check.py` — additive `--action settle`.
5. `skills/internal/create-team/scripts/dispatch.sh` — additive `.attempt` / `.end`, pid, TERM/INT/HUP trap.

Report and skill contracts:

6. `skills/internal/create-team/SKILL.md` — 7-column mapping table + `## Verification` settlement coverage.
7. `skills/internal/run-team/SKILL.md` — settlement-owner pointer line.
8. `skills/internal/run-agent/SKILL.md` — attempt record, settle-before-report, native background/foreground branches, virtual exclusion.
9. `skills/external/sdd-loop-driver/SKILL.md` — settlement-owner pointer line (C1 mapping consumed).

Command-entry and coordinator pointers (one line each):

10. `templates/commands/agents.md`
11. `templates/commands/team.md`
12. `agents/sdd-plan-coordinator.agent.md`
13. `agents/sdd-task-coordinator.agent.md`
14. `agents/sdd-implement-coordinator.agent.md`
15. `agents/sdd-review-coordinator.agent.md`

Documentation (existing pages, pointer + explanation only):

16. `docs/reference/skills/sdd-loop-driver.md`
17. `docs/reference/commands/agents.md`
18. `docs/reference/teams/orchestration.md`

Tests (new):

19. `tests/fixtures/settlement/` (per-carrier fixture trees: C1 state, C2 logs, C3 reports, legacy/versioned pair)
20. `tests/contract/test_settlement_contract_definitions.py`
21. `tests/contract/test_settlement_engine.py`
22. `tests/contract/test_settlement_carriers.py`
23. `tests/contract/test_settlement_migration.py`
24. `tests/contract/test_settlement_preservation.py`
25. `tests/contract/test_settlement_scope.py`

Generated mirrors and copies (never hand-edited):

26. `.specify/shared/definitions/…`, `.specify/shared/workflow/…` (`sync-mirrors.py --only shared`)
27. `.specify/scripts/python/role-edge-check.py` (`sync-mirrors.py --only scripts`)
28. `.specify/skills/internal/…` (`sync-mirrors.py --only skills/internal`)
29. `.specify/skills/sdd-loop-driver/SKILL.md` (`sync-mirrors.py --only skills/external`)
30. `.specify/agents/templates/sdd-{plan,task,implement,review}-coordinator.agent.md` (`sync-mirrors.py --only agents`)
31. `.claude/commands/speckit.{agents,team}.md`; `.github/prompts/speckit.{agents,team}.prompt.md`; `.qoder/commands/speckit.{agents,team}.md`; `.opencode/command/speckit.{agents,team}.md` (`regen-command-copies.py`)

This spec directory and lifecycle registration:

32. `.specify/specs/106-background-silent-failure/**` (plan set + test-evidence)
33. `.specify/features.md` (row 106 → `Planned`; date/clause note)
34. `.specify/features/095-superagent-role.md` (plan note; parent status unchanged)
35. `.specify/glossary.md` (`silent-end` proposal, `origin=auto`, `status=proposed` — wrap-up)

## Unit registration verdict

**No new unit is registered.** The feature adds no skill and no command. The edited surfaces keep their existing per-unit registrations:

- `templates/commands/agents.md` / `/speckit.agents` and `templates/commands/team.md` / `/speckit.team` — existing command units.
- `run-agent`, `run-team`, `create-team`, `sdd-loop-driver` — existing skill units (their flow-class rows already exist).
- `scripts/python/role-edge-check.py` — an engine, not a unit row.
- `dispatch.sh` — a carrier script, not a unit row.

Consequently no flow-class row, probe row, `flow-class` declaration or new Feature row is added; Feature 095's row and the slice row 106 are the only registry changes.

## Explicitly outside the delta

`skills/external/sdd-loop-driver/scripts/watch-target.sh` and `stage-runner.sh` (byte-stable, sha-verified), `scripts/python/exec-quant.py`, `scripts/python/sync-mirrors.py`, `scripts/python/regen-command-copies.py`, `scripts/python/scan-confirmation-gates.py`, `shared/guidelines/confirmation-gates.md`, `templates/instructions-template.md`, the five-element uplink text, the seven-field downlink text, `README.md`, and the pre-existing dirty files under `.specify/skills/coaching-skills/` (neither committed nor reverted).

## Overlap Adjudication (driver record, plan U4, 2026-11-25)

- **Trigger**: post-plan `overlap-check.py --spec-dir .specify/specs/106-background-silent-failure --repo .` returned `decision=overlap`, `checked_specs=88`, `overlaps=201` (132 `same-path`, 69 `nested-path`). The clarify-time run was vacuous (`overlaps=0`, no declaration artifact existed yet), so this is the first non-vacuous reading.
- **Reading**: the relations are path declarations from historical specs whose delivery surfaces already include these shared framework files (top sources: 088 ×16, 093 ×12, 089 ×11, 056 ×10, 085 ×9). They are not evidence of a concurrent writer: the environment registry has exactly one executing line for this project (106); the other `active` entry (101) is stale since 2026-11-12 with no runner, and no other line is writing the settlement paths.
- **Ruling**: **106 is the sole current writer** for the settlement-contract additions (`shared/definitions/superagent-definitions.md` § Termination, `scripts/python/role-edge-check.py` `settle` action, `dispatch.sh` additive attempt records, the team/agent report columns, and their tests/docs). Prior features retain ownership of their already-delivered behavior and dated records; no scope is removed, narrowed or reassigned. The additions are additive and pointer-based; the owner sections those specs delivered stay intact.
- **Residual**: `overlap=201, historical/non-concurrent`. The engine can only clear by falsifying a delivery surface or deleting historical ownership, both forbidden. Tasks MUST NOT start if a new concurrent writer activates on these paths; if that happens, this adjudication is re-opened before dispatch.
- **Evidence**: `.specify/state/u4-background-silent-failure-plan.txt` (full relation list + gate readings).
