# Feature Reference — 104-agents-run

**Bound Feature**: 019 — Agents Command (`Implemented`; no status regression).
**Binding basis**: 019 owns the `/speckit.agents` command surface (create / refine / run) and the layered agent store. This feature adds the explicit run subcommand and its dispatch wiring to the same surface — the same direct-follow-on relation 003 / 014 / 022 / 023 already have to 019. Binding record and rationale: `.specify/specs/104-agents-run/requirements.md` § Related Feature / § Clarifications (2026-11-24 clarify).
**Parent detail**: `.specify/features/019-agents-command.md`.

## How this plan maps to Feature 019

| Plan element | Feature 019 element it serves | Direction |
|--------------|-------------------------------|-----------|
| `argument-hint` + explicit-verb routing in `templates/commands/agents.md` | the single `/speckit.agents` entry and its three-skill delegation | additive: fixes the grammar and adds stop paths; create / refine semantics unchanged |
| Role wiring in `run-agent` (presentation, seven-field downlink, five-element uplink, label, probe condition) | the run mode of the same command and its 095-owned role model | additive: makes the existing protocol apply at dispatch time; no second definition |
| Run-command reference merge + drift correction | the command's user-facing reference | correction: one body follows the template/skill; stale "two capabilities" and "no-arg generates seven agents" claims removed |
| Multi-child identity/visibility pointers | the existing artifact triplet, `exec-quant` records and `status-digest` role view | presentation only; no new store, registry or renderer |
| Contract tests + behavior-class evidence plan | the feature's quality gate and mutation evidence | new tests; behavior claims stay honestly classified |

The feature does **not** change `role-edge-check.py`, `execution-config.py`, `dispatch.sh`, `exec-quant.py` (zero modification, RS-004…RS-007) or `status-digest.py` (likewise unchanged, consumed read-only; no RS row), does not change create / refine semantics or write authority, and does not add a glossary entry, a Feature row or a schema key.

## Delivery surface

Authored framework sources:

1. `templates/commands/agents.md` (edit: `argument-hint`, explicit-verb priority, `missing agent name` stop, team redirect, no fourth verb alias)
2. `skills/internal/run-agent/SKILL.md` (edit: input-contract syntax, presentation role disclosure, seven-field downlink, four injections by pointer, five-element uplink, label convention, visibility pointers, SDD probe applicability, single-unit reading)

Documentation (edit):

3. `docs/reference/commands/agents.md` (merge three bodies into one; three capabilities; run syntax and intent row; third skill; no-argument correction)
4. `docs/reference/agents/command-and-skills.md` (three capabilities; run row; routing flow; `run-agent` section)
5. `docs/reference/agents/overview.md` (capability line, skill-count statement, diagram)
6. `docs/reference/agents/design.md` (capability line, workflow step, single-agent skill list)
7. `docs/tutorials/installation.md` (command-table row; stale next-step correction)
8. `docs/tutorials/quickstart.md` (command-table row; three stale no-argument passages corrected)
9. `tests/scenarios/agents-command/single-entry-routing-scenario.md` (three-capability scope + explicit run routing samples — the FR-020 plan-stage amendment)

Tests (new):

10. `tests/contract/test_agents_run_command_contract.py`
11. `tests/contract/test_agents_run_docs_contract.py`
12. `tests/contract/test_agents_run_skill_wiring.py`
13. `tests/contract/test_agents_run_multi_child_edges.py`
14. `tests/contract/test_agents_run_scope_contract.py`

Generated mirrors and copies (never hand-edited):

15. `.specify/skills/internal/run-agent/**` (`sync-mirrors.py --only skills/internal`)
16. `.claude/commands/speckit.agents.md`
17. `.github/prompts/speckit.agents.prompt.md`
18. `.qoder/commands/speckit.agents.md`
19. `.opencode/command/speckit.agents.md` (`regen-command-copies.py`)

This spec directory:

20. `.specify/specs/104-agents-run/**` (plan stage: plan / research / data-model / contracts / quickstart / feature-ref / test-evidence; requirements.md carries the plan-stage FR-020 amendment)

Lifecycle registration:

21. `.specify/features.md` (019 row note: plan artifacts landed; status stays `Implemented`)
22. `.specify/features/019-agents-command.md` (plan note; status unchanged)

## Unit registration verdict

**No new unit is registered.** The feature adds no skill and no command; it edits the existing `/speckit.agents` command and the existing `skill:run-agent`. Their per-unit registrations already exist:

- `shared/definitions/flow-class-definitions.md:145` — `/speckit.agents` (execution / behavior-oracle)
- `shared/definitions/flow-class-definitions.md:225` — `skill:run-agent` (execution / behavior-oracle)
- `shared/definitions/probe-definitions.md:203` — `skill-run-agent-wrapup`

Therefore no probe row, flow-class row, glossary entry or Feature row is added or removed; only the existing Feature 019 registry/detail notes are updated (item 21–22).

**Explicitly outside the delta**: `scripts/python/role-edge-check.py`, `scripts/python/execution-config.py`, `scripts/python/exec-quant.py`, `scripts/python/status-digest.py`, `skills/internal/create-team/scripts/dispatch.sh` (all consumed read-only, zero modification), `.specify/shared/definitions/superagent-definitions.md` and `subagent-definitions.md` (owners, unchanged), `skills/internal/create-agent/**`, `skills/internal/improve-agent/**`, `README.md` (no capability row, FR-020), `.specify/glossary.md` (no new entry, FR-021), `docs/reference/history/**` (dated records, unchanged), and the pre-existing dirty files under `.specify/skills/coaching-skills/` (neither committed nor reverted).
